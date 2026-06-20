import threading
import ai
import db

# In-memory fallback caches (reset on restart — good enough for MVP)
_sel_counters: dict[int, int] = {}
_language_cache: dict[str, str] = {}   # chat_id → language, mirrors DB within the session
_feedback_state: dict[str, dict] = {}  # chat_id → {step, topic, q1, q2}

# ── Onboarding ─────────────────────────────────────────────────────────────────

ONBOARDING_WELCOME = (
    "👋 Welcome to Padhai Bot!\n\n"
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

_FEEDBACK_QUESTIONS = {
    1: {
        "text": {
            "en": "📊 Quick feedback on today's lesson:\n\nWas the content aligned with NCERT?",
            "hi": "📊 आज के पाठ पर त्वरित प्रतिक्रिया:\n\nक्या सामग्री NCERT के अनुरूप थी?",
            "ta": "📊 இன்றைய பாடம் பற்றிய கருத்து:\n\nதிருத்தம் NCERT உடன் ஒத்திருந்ததா?",
            "te": "📊 నేటి పాఠంపై అభిప్రాయం:\n\nకంటెంట్ NCERT కి అనుగుణంగా ఉందా?",
        },
        "buttons": [
            {"label": "✅ Yes, fully",  "data": "fb_1_full"},
            {"label": "🟡 Partially",   "data": "fb_1_partial"},
            {"label": "❌ No",           "data": "fb_1_no"},
        ],
    },
    2: {
        "text": {
            "en": "Was the SEL integration helpful for teaching?",
            "hi": "क्या SEL एकीकरण पढ़ाने में सहायक था?",
            "ta": "SEL ஒருங்கிணைப்பு கற்பிக்க உதவியதா?",
            "te": "SEL ఇంటిగ్రేషన్ బోధనలో సహాయపడిందా?",
        },
        "buttons": [
            {"label": "✅ Yes",       "data": "fb_2_yes"},
            {"label": "🟡 Somewhat", "data": "fb_2_partial"},
            {"label": "❌ No",        "data": "fb_2_no"},
        ],
    },
    3: {
        "text": {
            "en": "Did students participate in the group activity?",
            "hi": "क्या छात्रों ने समूह गतिविधि में भाग लिया?",
            "ta": "மாணவர்கள் குழு செயல்பாட்டில் பங்கேற்றனரா?",
            "te": "విద్యార్థులు గ్రూప్ యాక్టివిటీలో పాల్గొన్నారా?",
        },
        "buttons": [
            {"label": "✅ Yes, actively", "data": "fb_3_yes"},
            {"label": "🟡 Some students", "data": "fb_3_partial"},
            {"label": "❌ Not much",       "data": "fb_3_no"},
        ],
    },
}

_FEEDBACK_THANKS = {
    "en": "Thank you! Your feedback helps us improve Padhai Bot. 🙏",
    "hi": "धन्यवाद! आपकी प्रतिक्रिया से हम बेहतर होते हैं। 🙏",
    "ta": "நன்றி! உங்கள் கருத்து மேம்படுத்த உதவுகிறது. 🙏",
    "te": "ధన్యవాదాలు! మీ అభిప్రాయం మెరుగుపరచడంలో సహాయపడుతుంది. 🙏",
}

def _feedback_q(step: int, language: str) -> dict:
    q = _FEEDBACK_QUESTIONS[step]
    text = q["text"].get(language, q["text"]["en"])
    return _buttons(text, q["buttons"])


OUT_OF_SERVICE_MSG = {
    "en": "I'm Padhai Bot — I help with NCERT classroom teaching (Classes 1–10). I can't help with JEE/NEET prep, stock markets, coding, or other topics outside school teaching. Try asking me for a lesson plan or a curriculum question!",
    "hi": "मैं Padhai Bot हूँ — मैं NCERT कक्षा शिक्षण (कक्षा 1–10) में मदद करता हूँ। JEE/NEET, शेयर बाज़ार, कोडिंग या अन्य विषयों में मैं मदद नहीं कर सकता। पाठ योजना या पाठ्यक्रम से जुड़ा कोई सवाल पूछें!",
    "ta": "நான் Padhai Bot — NCERT வகுப்பு கற்பித்தலில் (1–10 வகுப்பு) உதவுகிறேன். JEE/NEET, பங்கு சந்தை, coding போன்ற தலைப்புகளில் உதவ முடியாது. பாட திட்டம் அல்லது பாடத்திட்ட கேள்வி கேளுங்கள்!",
    "te": "నేను Padhai Bot — NCERT తరగతి బోధనలో (1–10 తరగతులు) సహాయం చేస్తాను. JEE/NEET, స్టాక్ మార్కెట్, కోడింగ్ వంటి అంశాలలో సహాయం చేయలేను. పాఠ్య ప్రణాళిక లేదా పాఠ్యక్రమ ప్రశ్న అడగండి!",
}

LANGUAGE_CHANGED_MSG = {
    "en": "Done! I'll respond in English from now on.",
    "hi": "ठीक है! अब मैं हिंदी में जवाब दूँगा।",
    "ta": "சரி! இனி நான் தமிழில் பதில் தருவேன்.",
    "te": "సరే! ఇకపై నేను తెలుగులో సమాధానం ఇస్తాను.",
    "mr": "ठीक आहे! आता मी मराठीत उत्तर देईन.",
    "kn": "ಸರಿ! ಇನ್ನು ಮುಂದೆ ನಾನು ಕನ್ನಡದಲ್ಲಿ ಉತ್ತರಿಸುತ್ತೇನೆ.",
    "bn": "ঠিক আছে! এখন থেকে আমি বাংলায় উত্তর দেব।",
}

# ── Response helpers ────────────────────────────────────────────────────────────

def _text(msg: str) -> dict:
    return {"type": "text", "text": msg}

def _buttons(msg: str, buttons: list[dict]) -> dict:
    return {"type": "buttons", "text": msg, "buttons": buttons}

# ── Public handlers ─────────────────────────────────────────────────────────────

def handle_message(chat_id: int, text: str, user_name: str, channel: str = "telegram") -> dict:
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
    intent = classification.get("intent", "query_resolution_academic")
    grade  = classification.get("grade", "")

    if intent == "content_generation":
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

        # Schedule feedback Q1 for next 2 PM IST — do not send immediately
        topic_label = f"{subject} — {topic}".strip(" —")
        db.schedule_feedback_q1(uid, language, topic_label, channel)
        db.log_message(uid, text, intent, response)
        return _text(response)

    elif intent == "feedback":
        db.log_message(uid, text, intent, "")
        return _text("Thank you for the feedback! It helps us improve Padhai Bot.")

    elif intent == "query_resolution_sel":
        try:
            response = ai.resolve_sel_observation(text, grade, language, chat_id=uid)
        except Exception as e:
            print(f"[sel_obs error] {e}", flush=True)
            response = {
                "en": "I'm having trouble connecting right now. Please try again in a moment.",
                "hi": "अभी कनेक्शन में समस्या है। कृपया थोड़ी देर बाद फिर कोशिश करें।",
                "ta": "தற்போது இணைப்பில் சிக்கல் உள்ளது. சற்று நேரம் கழித்து மீண்டும் முயற்சிக்கவும்.",
                "te": "ప్రస్తుతం కనెక్షన్‌లో సమస్య ఉంది. దయచేసి కొంత సేపటి తర్వాత మళ్ళీ ప్రయత్నించండి.",
            }.get(language, "I'm having trouble connecting right now. Please try again in a moment.")

    elif intent == "out_of_service":
        db.log_message(uid, text, intent, "")
        return _text(OUT_OF_SERVICE_MSG.get(language, OUT_OF_SERVICE_MSG["en"]))

    elif intent == "language_change":
        new_lang = classification.get("language", language)
        _language_cache[uid] = new_lang
        db.complete_onboarding(uid, "", new_lang)
        db.log_message(uid, text, intent, "")
        return _text(LANGUAGE_CHANGED_MSG.get(new_lang, LANGUAGE_CHANGED_MSG["en"]))

    else:  # query_resolution_academic
        response = ai.resolve_query(text, grade, language, chat_id=uid)

    # If a new content request arrives while feedback is pending, clear stale state
    _feedback_state.pop(uid, None)

    db.log_message(uid, text, intent, response)
    return _text(response)


def handle_callback(chat_id: int, data: str, user_name: str) -> dict:
    uid = str(chat_id)

    # Language selection
    lang_map = {"lang_en": "en", "lang_hi": "hi", "lang_ta": "ta", "lang_te": "te"}
    lang = lang_map.get(data)
    if lang:
        _language_cache[uid] = lang
        db.complete_onboarding(uid, user_name, lang)
        return _text(FEATURE_INTRO[lang])

    # Feedback buttons
    if data.startswith("fb_"):
        return _handle_feedback_callback(uid, data)

    return _text("")


def _handle_feedback_callback(uid: str, data: str) -> dict:
    state = _feedback_state.get(uid)
    language = _language_cache.get(uid, "en")

    if not state:
        return _text("")

    if state["step"] == 1 and data.startswith("fb_1_"):
        state["q1"] = data[5:]   # "full" | "partial" | "no"
        state["step"] = 2
        return _feedback_q(2, language)

    if state["step"] == 2 and data.startswith("fb_2_"):
        state["q2"] = data[5:]   # "yes" | "partial" | "no"
        state["step"] = 3
        return _feedback_q(3, language)

    if state["step"] == 3 and data.startswith("fb_3_"):
        q3 = data[5:]            # "yes" | "partial" | "no"
        db.log_usage_feedback(uid, state["topic"], state["q1"], state["q2"], q3)
        del _feedback_state[uid]
        return _text(_FEEDBACK_THANKS.get(language, _FEEDBACK_THANKS["en"]))

    return _text("")
