import threading
import ai
import db

# In-memory fallback caches (reset on restart — good enough for MVP)
_sel_counters: dict[int, int] = {}
_language_cache: dict[str, str] = {}  # chat_id → language, mirrors DB within the session

# ── Onboarding ─────────────────────────────────────────────────────────────────

ONBOARDING_WELCOME = (
    "👋 Welcome to ShikshaBot!\n\n"
    "I'm your teaching assistant for NCERT classrooms.\n\n"
    "Please choose your preferred language:"
)

LANGUAGE_BUTTONS = [
    {"label": "English", "data": "lang_en"},
    {"label": "हिंदी",   "data": "lang_hi"},
]

FEATURE_INTRO = {
    "en": (
        "✅ You're all set!\n\n"
        "Here's what I can help with:\n\n"
        "📚 Lesson plans\n"
        "\"Class 7 Science — water cycle lesson\"\n\n"
        "❓ Curriculum questions\n"
        "\"Explain Newton's third law for Class 9\"\n\n"
        "🧠 Student support\n"
        "\"A student doesn't participate in class\"\n\n"
        "💬 Feedback\n"
        "\"The last lesson was too long\"\n\n"
        "Just type your request anytime!"
    ),
    "hi": (
        "✅ आप तैयार हैं!\n\n"
        "मैं इन चीज़ों में मदद कर सकता हूँ:\n\n"
        "📚 पाठ योजना\n"
        "\"कक्षा 7 विज्ञान — जल चक्र का पाठ बनाएं\"\n\n"
        "❓ पाठ्यक्रम प्रश्न\n"
        "\"कक्षा 9 के लिए न्यूटन का तीसरा नियम समझाएं\"\n\n"
        "🧠 छात्र सहायता\n"
        "\"एक छात्र कक्षा में भाग नहीं लेता\"\n\n"
        "💬 प्रतिक्रिया\n"
        "\"पिछला पाठ बहुत लंबा था\"\n\n"
        "बस अपना सवाल टाइप करें!"
    ),
    "ta": (
        "✅ பதிவு முடிந்தது!\n\n"
        "நான் இவற்றில் உதவலாம்:\n\n"
        "📚 பாட திட்டம்\n"
        "\"7ஆம் வகுப்பு அறிவியல் — நீர் சுழற்சி பாடம்\"\n\n"
        "❓ பாட கேள்விகள்\n"
        "\"9ஆம் வகுப்புக்கு நியூட்டன் மூன்றாம் விதி விளக்கவும்\"\n\n"
        "🧠 மாணவர் ஆதரவு\n"
        "\"ஒரு மாணவர் வகுப்பில் பங்கேற்பதில்லை\"\n\n"
        "💬 கருத்து\n"
        "\"கடந்த பாடம் மிக நீளமாக இருந்தது\"\n\n"
        "உங்கள் கோரிக்கையை தட்டச்சு செய்யுங்கள்!"
    ),
    "te": (
        "✅ నమోదు పూర్తయింది!\n\n"
        "నేను వీటిలో సహాయం చేయగలను:\n\n"
        "📚 పాఠ ప్రణాళిక\n"
        "\"7వ తరగతి సైన్స్ — నీటి చక్రం పాఠం\"\n\n"
        "❓ పాఠ్యక్రమ ప్రశ్నలు\n"
        "\"9వ తరగతికి న్యూటన్ మూడవ నియమం వివరించండి\"\n\n"
        "🧠 విద్యార్థి సహాయం\n"
        "\"ఒక విద్యార్థి తరగతిలో పాల్గొనడం లేదు\"\n\n"
        "💬 అభిప్రాయం\n"
        "\"చివరి పాఠం చాలా పొడవుగా ఉంది\"\n\n"
        "మీ అభ్యర్థనను టైప్ చేయండి!"
    ),
}

# ── Response helpers ────────────────────────────────────────────────────────────

def _text(msg: str) -> dict:
    return {"type": "text", "text": msg}

def _buttons(msg: str, buttons: list[dict]) -> dict:
    return {"type": "buttons", "text": msg, "buttons": buttons}

# ── Public handlers ─────────────────────────────────────────────────────────────

def handle_message(chat_id: int, text: str, user_name: str) -> dict:
    uid = str(chat_id)

    # Onboarding: any message from an unregistered user triggers language selection
    language = _language_cache.get(uid) or db.get_language(uid)
    if not language:
        db.upsert_user(uid, user_name)
        return _buttons(ONBOARDING_WELCOME, LANGUAGE_BUTTONS)

    _language_cache[uid] = language  # keep cache warm

    # /start or greeting for already-registered users — resend feature intro
    if text.lower() in ["/start", "hi", "hello", "hey"]:
        return _text(FEATURE_INTRO.get(language, FEATURE_INTRO["en"]))

    classification = ai.classify_intent(text, chat_id=uid)
    intent = classification.get("intent", "query")
    grade  = classification.get("grade", "8")

    if intent == "content":
        subject = classification.get("subject", "General")
        topic   = classification.get("topic", "")

        count = db.get_content_count(uid) or _sel_counters.get(chat_id, 0)
        _sel_counters[chat_id] = count + 1
        sel_dim = ai.SEL_DIMENSIONS[count % len(ai.SEL_DIMENSIONS)]

        response = ai.generate_content(subject, topic, grade, sel_dim, language, chat_id=uid)

        # Run eval in background — never block the teacher's response
        def _eval_bg(r=response, s=subject, t=topic, g=grade, sd=sel_dim, l=language, c=uid):
            scores = ai.evaluate_content(s, t, g, sd, l, r, chat_id=c)
            if scores:
                db.log_content_eval(c, s, t, g, sd, scores)
                failed = [m for v_map in [scores] for m, v in v_map.items() if not v.get("verdict", True)]
                if failed:
                    print(f"[content_eval] FLAGGED chat={c} topic={t!r} failed={failed}")
        threading.Thread(target=_eval_bg, daemon=True).start()

    elif intent == "feedback":
        db.log_message(uid, text, intent, "")
        return _text("Thank you for the feedback! It helps us improve ShikshaBot.")

    elif intent == "sel_observation":
        response = ai.resolve_sel_observation(text, grade, language, chat_id=uid)

    else:  # query
        response = ai.resolve_query(text, grade, language, chat_id=uid)

    db.log_message(uid, text, intent, response)
    return _text(response)


def handle_callback(chat_id: int, data: str, user_name: str) -> dict:
    """Handles inline button presses — currently only language selection."""
    uid = str(chat_id)
    lang_map = {"lang_en": "en", "lang_hi": "hi", "lang_ta": "ta", "lang_te": "te"}
    lang = lang_map.get(data)
    if lang:
        _language_cache[uid] = lang  # cache immediately so next message doesn't re-trigger onboarding
        db.complete_onboarding(uid, user_name, lang)
        return _text(FEATURE_INTRO[lang])
    return _text("")
