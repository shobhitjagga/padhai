import asyncio
import json
from fastapi import FastAPI, Request, Response
import httpx
import config
import db
from handlers import (handle_message, handle_callback,
                       _feedback_state, _feedback_q, _language_cache,
                       _lecture_pending, _Q4_QUESTIONS)

app = FastAPI()


@app.on_event("startup")
async def startup():
    asyncio.create_task(_feedback_scheduler())


async def _feedback_scheduler():
    """Poll every 60 s; send feedback Q1 to any teacher whose 2 PM has arrived."""
    while True:
        await asyncio.sleep(60)
        try:
            jobs = db.get_due_feedback_jobs()
            for job in jobs:
                await _dispatch_feedback_q1(job)
        except Exception as e:
            print(f"[scheduler] {e}", flush=True)


async def _dispatch_feedback_q1(job: dict):
    uid      = job["chat_id"]
    language = job.get("language", "en")
    topic    = job.get("topic", "")
    channel  = job.get("channel", "telegram")

    grade    = job.get("grade", "")
    subject  = job.get("subject", "")
    q4_due   = job.get("q4_due", False)
    q4_index = job.get("q4_index", 0)
    _feedback_state[uid] = {
        "step": 1, "topic": topic, "grade": grade, "subject": subject,
        "sel_dim": "", "q1": None, "q2": None, "q3": None,
        "q4_due": q4_due, "q4_index": q4_index,
    }
    _language_cache[uid] = language

    q1 = _feedback_q(1, language)
    try:
        if channel == "telegram":
            await _tg_send(int(uid), q1)
        else:
            await _twilio_wa_send(f"whatsapp:+{uid}", q1)
        db.mark_feedback_job_sent(job["id"])
        print(f"[scheduler] sent feedback Q1 → {uid} ({channel})", flush=True)
    except Exception as e:
        print(f"[scheduler] failed to send to {uid}: {e}", flush=True)


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
        stop = asyncio.Event()
        typing_task = asyncio.create_task(_tg_typing_loop(chat_id, stop))
        try:
            result = await asyncio.to_thread(handle_callback, chat_id, cb_data, username)
        finally:
            stop.set()
            typing_task.cancel()
        for r in (result if isinstance(result, list) else [result]):
            await _tg_send(chat_id, r)
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

    stop = asyncio.Event()
    typing_task = asyncio.create_task(_tg_typing_loop(chat_id, stop))
    try:
        result = await asyncio.to_thread(handle_message, chat_id, text, username, channel="telegram")
    finally:
        stop.set()
        typing_task.cancel()
    for r in (result if isinstance(result, list) else [result]):
        await _tg_send(chat_id, r)
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
    """Send a message with an inline keyboard.
    Lecture buttons (lec_ prefix): one per row so long titles aren't truncated.
    All others: single row.
    """
    is_lecture = buttons and buttons[0]["data"].startswith("lec_")
    if is_lecture:
        rows = [[{"text": b["label"], "callback_data": b["data"]}] for b in buttons]
    else:
        rows = [[{"text": b["label"], "callback_data": b["data"]} for b in buttons]]
    keyboard = {"inline_keyboard": rows}
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


async def _tg_send_action(chat_id: int):
    async with httpx.AsyncClient() as c:
        await c.post(
            f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendChatAction",
            json={"chat_id": chat_id, "action": "typing"},
            timeout=5.0,
        )


async def _tg_typing_loop(chat_id: int, stop: asyncio.Event):
    """Repeat typing action every 4 s (it expires after 5 s) until stop is set."""
    while not stop.is_set():
        await _tg_send_action(chat_id)
        try:
            await asyncio.wait_for(asyncio.shield(stop.wait()), timeout=4.0)
        except asyncio.TimeoutError:
            pass


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

    # Button tap
    if button_payload:
        cb_data = button_payload
        if button_payload in ("1", "2", "3"):
            num = int(button_payload)
            lec_pending      = _lecture_pending.get(number)
            feedback_pending = _feedback_state.get(number)
            if lec_pending:
                cb_data = f"lec_{lec_pending['grade']}_{lec_pending['s_key']}_{lec_pending['ch_key']}_{num}"
            elif feedback_pending:
                cb_data = _map_numbered_feedback(num, feedback_pending)
            else:
                await _twilio_wa_send(from_, {"type": "text",
                    "text": "This selection has already been used. Please send a new message to generate a different lecture."})
                return Response(content="<Response/>", media_type="application/xml")
        result = await asyncio.to_thread(handle_callback, number, cb_data, name)
        for r in (result if isinstance(result, list) else [result]):
            await _twilio_wa_send(from_, r)
        return Response(content="<Response/>", media_type="application/xml")

    # Voice note — transcribe and treat as text
    if num_media > 0 and media_type.startswith("audio/"):
        body = await _transcribe_audio(media_url) or ""

    if not body:
        return Response(content="<Response/>", media_type="application/xml")

    result = await asyncio.to_thread(handle_message, number, body, name, channel="whatsapp")
    for r in (result if isinstance(result, list) else [result]):
        await _twilio_wa_send(from_, r)
    return Response(content="<Response/>", media_type="application/xml")


def _map_numbered_feedback(num: int, state: dict) -> str:
    """Map a tapped '1'/'2'/'3' button to the right fb_* callback data string."""
    _step_maps = {
        2: {1: "fb_2_verbal",         2: "fb_2_mixed",          3: "fb_2_quiet"},
        3: {1: "fb_3_focused",        2: "fb_3_high",           3: "fb_3_low"},
        4: {1: "fb_4_persona_shy",    2: "fb_4_persona_mixed",  3: "fb_4_persona_assertive"},
        5: {1: "fb_4_home_difficult", 2: "fb_4_home_mixed",     3: "fb_4_home_stable"},
        6: {1: "fb_4_gender_gap",     2: "fb_4_gender_partial", 3: "fb_4_gender_equal"},
        7: {1: "fb_4_group_high",     2: "fb_4_group_mixed",    3: "fb_4_group_low"},
        8: {1: "fb_5_sel_yes",        2: "fb_5_sel_partial",    3: "fb_5_sel_no"},
        9: {1: "fb_6_quiet_yes",      2: "fb_6_quiet_no",       3: "fb_6_quiet_unsure"},
    }
    return _step_maps.get(state.get("step", 0), {}).get(num, "")


def _twilio_buttons_text(response: dict) -> str:
    lines = [response["text"], ""]
    for i, b in enumerate(response["buttons"]):
        lines.append(f"{i + 1}. {b['label']}")
    lines.append("\nReply with the number (e.g. 1)")
    return "\n".join(lines)


async def _twilio_wa_send(to_wa: str, response: dict):
    """Send response via Twilio REST API — uses Content Template for language buttons."""
    url = f"https://api.twilio.com/2010-04-01/Accounts/{config.TWILIO_ACCOUNT_SID}/Messages.json"
    async with httpx.AsyncClient() as c:
        template_sid = None
        content_vars = None  # JSON string for variable-body templates
        if response["type"] == "buttons":
            first_data = response.get("buttons", [{}])[0].get("data", "")
            if first_data.startswith("lang_") and config.TWILIO_LANG_TEMPLATE_SID:
                template_sid = config.TWILIO_LANG_TEMPLATE_SID
            elif first_data.startswith("fb_1_") and config.TWILIO_FEEDBACK_Q1_SID:
                template_sid = config.TWILIO_FEEDBACK_Q1_SID
            elif (first_data.startswith(("lec_", "fb_2_", "fb_3_", "fb_4_"))
                  and config.TWILIO_LECTURE_SELECT_SID):
                # Generic 1/2/3 template with variable body — reused for
                # lecture selection, Q2 (SEL engagement), Q3 (energy), Q4 (class profile)
                template_sid = config.TWILIO_LECTURE_SELECT_SID
                body_lines = [response["text"], ""]
                for i, b in enumerate(response["buttons"], 1):
                    body_lines.append(f"{i}. {b['label']}")
                content_vars = json.dumps({"1": "\n".join(body_lines)})

        if template_sid:
            send_data = {
                "From":       f"whatsapp:{config.TWILIO_WA_NUMBER}",
                "To":         to_wa,
                "ContentSid": template_sid,
            }
            if content_vars:
                send_data["ContentVariables"] = content_vars
            r = await c.post(
                url,
                auth=(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN),
                data=send_data,
                timeout=15.0,
            )
            if r.status_code >= 400:
                print(f"[twilio] buttons send failed {r.status_code}: {r.text[:300]}", flush=True)
        else:
            body = _twilio_buttons_text(response) if response["type"] == "buttons" else response["text"]
            for chunk in _wa_split(body):
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
