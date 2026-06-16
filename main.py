import asyncio
from fastapi import FastAPI, Form, Request, Response
from pydantic import BaseModel
import httpx
import config
from handlers import handle_message, handle_callback

app = FastAPI()


# ── Telegram ────────────────────────────────────────────────────────────────────

@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()

    # Button press (callback_query) — language selection or future actions
    callback = data.get("callback_query")
    if callback:
        chat_id  = callback["message"]["chat"]["id"]
        cb_data  = callback.get("data", "")
        username = callback.get("from", {}).get("first_name", "Teacher")
        await _tg_answer_callback(callback["id"])
        result = await asyncio.to_thread(handle_callback, chat_id, cb_data, username)
        await _tg_send(chat_id, result)
        return {"ok": True}

    # Regular message
    message = data.get("message") or data.get("edited_message")
    if not message:
        return {"ok": True}

    chat_id  = message["chat"]["id"]
    text     = message.get("text", "").strip()
    username = message.get("from", {}).get("first_name", "Teacher")

    if not text:
        return {"ok": True}

    result = await asyncio.to_thread(handle_message, chat_id, text, username)
    await _tg_send(chat_id, result)
    return {"ok": True}


async def _tg_send(chat_id: int, response: dict):
    """Dispatch a handler response dict to the right Telegram API call."""
    if response["type"] == "text":
        await _tg_send_text(chat_id, response["text"])
    elif response["type"] == "buttons":
        await _tg_send_buttons(chat_id, response["text"], response["buttons"])


async def _tg_send_text(chat_id: int, text: str):
    async with httpx.AsyncClient() as c:
        await c.post(
            f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=10.0,
        )


async def _tg_send_buttons(chat_id: int, text: str, buttons: list[dict]):
    """Send a message with an inline keyboard. Each button: {label, data}."""
    keyboard = {"inline_keyboard": [[
        {"text": b["label"], "callback_data": b["data"]} for b in buttons
    ]]}
    async with httpx.AsyncClient() as c:
        await c.post(
            f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": text, "reply_markup": keyboard},
            timeout=10.0,
        )


async def _tg_answer_callback(callback_query_id: str):
    """Dismiss the loading spinner on the button after it's tapped."""
    async with httpx.AsyncClient() as c:
        await c.post(
            f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/answerCallbackQuery",
            json={"callback_query_id": callback_query_id},
            timeout=5.0,
        )


def _wa_split(text: str, limit: int = 1500) -> list[str]:
    """Split lesson plan into one message per --- section; sub-split oversized sections by paragraph."""
    sections = [s.strip() for s in text.split("\n---\n") if s.strip()]
    chunks = []
    for section in sections:
        if len(section) <= limit:
            chunks.append(section)
        else:
            current = ""
            for para in section.split("\n\n"):
                if not current:
                    current = para
                elif len(current) + 2 + len(para) <= limit:
                    current += "\n\n" + para
                else:
                    chunks.append(current)
                    current = para
            if current:
                chunks.append(current)
    return chunks or [text[:limit]]


# ── Twilio WhatsApp (official Meta API) ─────────────────────────────────────────

async def _transcribe_audio(media_url: str) -> str | None:
    """Download a WhatsApp voice note from Twilio and transcribe via Groq Whisper."""
    try:
        import io
        from groq import Groq
        async with httpx.AsyncClient() as c:
            resp = await c.get(
                media_url,
                auth=(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN),
                timeout=30.0,
                follow_redirects=True,
            )
        groq = Groq(api_key=config.GROQ_API_KEY)
        transcription = groq.audio.transcriptions.create(
            file=("audio.ogg", io.BytesIO(resp.content), "audio/ogg"),
            model="whisper-large-v3",
        )
        text = transcription.text.strip()
        print(f"[transcribe] {repr(text)}", flush=True)
        return text or None
    except Exception as e:
        print(f"[transcribe] error: {e}", flush=True)
        return None


@app.post("/twilio/whatsapp")
async def twilio_whatsapp(request: Request):
    form           = await request.form()
    from_          = form.get("From", "")
    body           = form.get("Body", "").strip()
    name           = form.get("ProfileName", "Teacher")
    button_payload = form.get("ButtonPayload", "").strip()
    num_media      = int(form.get("NumMedia", "0") or "0")
    media_url      = form.get("MediaUrl0", "")
    media_type     = form.get("MediaContentType0", "")

    number = from_.removeprefix("whatsapp:").removeprefix("+")

    # Button tap from language selection
    if button_payload:
        result = await asyncio.to_thread(handle_callback, number, button_payload, name)
        await _twilio_wa_send(from_, result)
        return Response(content="<Response/>", media_type="application/xml")

    # Voice note — transcribe and treat as text
    if num_media > 0 and media_type.startswith("audio/"):
        body = await _transcribe_audio(media_url) or ""

    if not body:
        return Response(content="<Response/>", media_type="application/xml")

    result = await asyncio.to_thread(handle_message, number, body, name)
    await _twilio_wa_send(from_, result)
    return Response(content="<Response/>", media_type="application/xml")


def _twilio_buttons_text(response: dict) -> str:
    lines = [response["text"], ""]
    for i, b in enumerate(response["buttons"]):
        lines.append(f"{i + 1}. {b['label']}")
    lines.append("\nReply with the number (e.g. 1)")
    return "\n".join(lines)


async def _twilio_wa_send(to_wa: str, response: dict):
    """Send response via Twilio REST API — uses Content Template for buttons."""
    url = f"https://api.twilio.com/2010-04-01/Accounts/{config.TWILIO_ACCOUNT_SID}/Messages.json"
    async with httpx.AsyncClient() as c:
        if response["type"] == "buttons" and config.TWILIO_LANG_TEMPLATE_SID:
            r = await c.post(
                url,
                auth=(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN),
                data={
                    "From":       f"whatsapp:{config.TWILIO_WA_NUMBER}",
                    "To":         to_wa,
                    "ContentSid": config.TWILIO_LANG_TEMPLATE_SID,
                },
                timeout=15.0,
            )
            if r.status_code >= 400:
                print(f"[twilio] buttons send failed {r.status_code}: {r.text[:300]}", flush=True)
        else:
            for chunk in _wa_split(response["text"]):
                r = await c.post(
                    url,
                    auth=(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN),
                    data={
                        "From": f"whatsapp:{config.TWILIO_WA_NUMBER}",
                        "To":   to_wa,
                        "Body": chunk,
                    },
                    timeout=15.0,
                )
                if r.status_code >= 400:
                    print(f"[twilio] send failed {r.status_code}: {r.text[:300]}", flush=True)


# ── Health / diagnostics ────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/config-check")
def config_check():
    return {
        "TWILIO_ACCOUNT_SID":       bool(config.TWILIO_ACCOUNT_SID),
        "TWILIO_AUTH_TOKEN":        bool(config.TWILIO_AUTH_TOKEN),
        "TWILIO_WA_NUMBER":         bool(config.TWILIO_WA_NUMBER),
        "TWILIO_LANG_TEMPLATE_SID": bool(config.TWILIO_LANG_TEMPLATE_SID),
        "GROQ_API_KEY":             bool(config.GROQ_API_KEY),
        "OPENAI_API_KEY":           bool(config.OPENAI_API_KEY),
        "SUPABASE_URL":             bool(config.SUPABASE_URL),
        "SUPABASE_KEY":             bool(config.SUPABASE_KEY),
        "sid_prefix":               config.TWILIO_ACCOUNT_SID[:6] if config.TWILIO_ACCOUNT_SID else "EMPTY",
    }
