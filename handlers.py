import threading
import ai
import db
import ncert_lecture_map

# ── Feature flags ───────────────────────────────────────────────────────────────
IMMEDIATE_FEEDBACK = True   # send Q1 right after content (testing); False = 2 PM IST scheduler
Q4_INTERVAL        = 4      # show Q4 every N sessions, starting from session 0 (first ever)

# In-memory fallback caches (reset on restart — good enough for MVP)
_sel_counters: dict[int, int] = {}
_language_cache: dict[str, str] = {}    # chat_id → language, mirrors DB within the session
_feedback_state: dict[str, dict] = {}   # chat_id → {step, topic, q1, q2}
_lecture_pending: dict[str, dict] = {}  # chat_id → {subject, topic, grade, sel_dim, channel}

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
        # Quality signal — was the lesson factually right?
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
        # Class dynamics — how did students engage with SEL?
        "text": {
            "en": "How did students respond to today's SEL reflection?",
            "hi": "छात्रों ने आज की SEL गतिविधि पर कैसी प्रतिक्रिया दी?",
            "ta": "மாணவர்கள் SEL செயல்பாட்டில் எவ்வாறு பதிலளித்தனர்?",
            "te": "విద్యార్థులు SEL రిఫ్లెక్షన్‌కు ఎలా స్పందించారు?",
        },
        "buttons": [
            {"label": "🗣️ Many shared openly",        "data": "fb_2_verbal"},
            {"label": "✍️ Some verbal, some written",  "data": "fb_2_mixed"},
            {"label": "🤫 Mostly quiet",               "data": "fb_2_quiet"},
        ],
    },
    3: {
        # Class dynamics — energy level
        "text": {
            "en": "What was the class energy like today?",
            "hi": "आज कक्षा का माहौल कैसा था?",
            "ta": "இன்று வகுப்பின் ஆற்றல் எப்படி இருந்தது?",
            "te": "నేడు తరగతి శక్తి స్థాయి ఎలా ఉంది?",
        },
        "buttons": [
            {"label": "🎯 Focused and calm",    "data": "fb_3_focused"},
            {"label": "⚡ Energetic / restless", "data": "fb_3_high"},
            {"label": "😴 Tired or distracted",  "data": "fb_3_low"},
        ],
    },
}

# Rotating Q4 — shown every Q4_INTERVAL sessions, cycles through all 4 questions.
# Grounded in PARAKH survey findings on government school classroom dynamics.
_Q4_QUESTIONS = [
    {
        "key": "persona",
        "text": {
            "en": "One more question about your class 🙏\n\nWhat best describes most of your students?",
            "hi": "आपकी कक्षा के बारे में एक और सवाल 🙏\n\nअधिकांश छात्र कैसे हैं?",
        },
        "buttons": [
            {"label": "🙈 Shy — rarely raise hands",      "data": "fb_4_persona_shy"},
            {"label": "⚖️ Mixed — some active, some quiet", "data": "fb_4_persona_mixed"},
            {"label": "🙋 Most want to participate",       "data": "fb_4_persona_assertive"},
        ],
    },
    {
        "key": "home_context",
        "text": {
            "en": "One more question 🙏\n\nHow many students have parents who are daily wage workers or often away from home?",
            "hi": "एक और सवाल 🙏\n\nकितने छात्रों के माता-पिता दिहाड़ी मज़दूर हैं या अक्सर घर से बाहर रहते हैं?",
        },
        "buttons": [
            {"label": "👥 Most of them",  "data": "fb_4_home_difficult"},
            {"label": "⚖️ About half",    "data": "fb_4_home_mixed"},
            {"label": "🏡 Very few",       "data": "fb_4_home_stable"},
        ],
    },
    {
        "key": "gender_gap",
        "text": {
            "en": "One more question 🙏\n\nDo girls and boys participate equally in discussions?",
            "hi": "एक और सवाल 🙏\n\nक्या लड़कियाँ और लड़के चर्चाओं में बराबर भाग लेते हैं?",
        },
        "buttons": [
            {"label": "🙍 Girls are usually quieter",      "data": "fb_4_gender_gap"},
            {"label": "⚖️ Both, but differently",          "data": "fb_4_gender_partial"},
            {"label": "✅ Roughly equal",                   "data": "fb_4_gender_equal"},
        ],
    },
    {
        "key": "group_pref",
        "text": {
            "en": "One more question 🙏\n\nHow comfortable is this class with group work?",
            "hi": "एक और सवाल 🙏\n\nक्या यह कक्षा समूह कार्य में सहज है?",
        },
        "buttons": [
            {"label": "🤝 Love it — energized by groups",  "data": "fb_4_group_high"},
            {"label": "⚖️ Mixed — some like it, some not", "data": "fb_4_group_mixed"},
            {"label": "👤 Prefer individual work",          "data": "fb_4_group_low"},
        ],
    },
]

_FEEDBACK_THANKS = {
    "en": "Thank you! Your feedback helps personalise future lessons. 🙏",
    "hi": "धन्यवाद! आपकी प्रतिक्रिया से अगले पाठ बेहतर बनेंगे। 🙏",
    "ta": "நன்றி! உங்கள் கருத்து எதிர்கால பாடங்களை மேம்படுத்துகிறது. 🙏",
    "te": "ధన్యవాదాలు! మీ అభిప్రాయం భవిష్యత్తు పాఠాలను మెరుగుపరచడంలో సహాయపడుతుంది. 🙏",
}

def _feedback_q(step: int, language: str) -> dict:
    q = _FEEDBACK_QUESTIONS[step]
    text = q["text"].get(language, q["text"]["en"])
    return _buttons(text, q["buttons"])

def _q4_question(index: int, language: str) -> dict:
    q = _Q4_QUESTIONS[index % len(_Q4_QUESTIONS)]
    text = q["text"].get(language, q["text"]["en"])
    return _buttons(text, q["buttons"])

def _post_content_feedback(uid: str, response: str, subject: str, topic_label: str,
                            grade: str, language: str, channel: str,
                            sel_dim: str, count: int) -> "dict | list":
    """Start background eval and return either [plan, Q1] (immediate) or just the plan (scheduled)."""
    def _eval_bg(r=response, s=subject, t=topic_label, g=grade, sd=sel_dim, l=language, c=uid):
        scores = ai.evaluate_content(s, t, g, sd, l, r, chat_id=c)
        if scores:
            db.log_content_eval(c, s, t, g, sd, scores)
            failed = [m for m, v in scores.items() if not v.get("verdict", True)]
            if failed:
                print(f"[content_eval] FLAGGED chat={c} topic={t!r} failed={failed}")
    threading.Thread(target=_eval_bg, daemon=True).start()

    q4_due   = True
    q4_index = count % len(_Q4_QUESTIONS)

    if IMMEDIATE_FEEDBACK:
        _feedback_state[uid] = {
            "step": 1, "topic": topic_label, "grade": grade, "subject": subject,
            "sel_dim": sel_dim, "q1": None, "q2": None, "q3": None,
            "q4_due": q4_due, "q4_index": q4_index,
        }
        return [_text(response), _feedback_q(1, language)]

    db.schedule_feedback_q1(uid, language, topic_label, channel,
                            grade, subject, q4_due, q4_index)
    return _text(response)


def _save_feedback(uid: str, state: dict):
    """Persist Q2/Q3/Q4 signals to class_profiles and log the full response."""
    import json
    grade   = state.get("grade", "")
    subject = state.get("subject", "")
    verbal  = state.get("q2", "")
    energy  = state.get("q3", "")

    signals = {
        "verbal": verbal, "energy": energy,
        "q4a": state.get("q4a", ""),
        "q4b": state.get("q4b", ""),
        "q4c": state.get("q4c", ""),
        "q4d": state.get("q4d", ""),
    }
    db.update_class_profile(uid, grade, subject, signals)
    q4_summary = json.dumps({k: state.get(k, "") for k in ("q4a", "q4b", "q4c", "q4d")})
    db.log_usage_feedback(uid, state.get("topic", ""), grade, subject,
                          state.get("q1", ""), verbal, energy, q4_summary)


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

# ── Lecture selection helpers ───────────────────────────────────────────────────

_LECTURE_SELECT_MSG = {
    "en": "📚 {name} (Class {grade}) spans {num} lessons.\n\nWhich lecture do you want a plan for?",
    "hi": "📚 {name} (कक्षा {grade}) में {num} पाठ हैं।\n\nकिस पाठ की योजना चाहिए?",
}

def _build_lecture_buttons(grade: str, subject_key: str, chapter_key: str, chapter: dict) -> list[dict]:
    return [
        {
            "label": lec["title"],
            "data": f"lec_{grade}_{subject_key}_{chapter_key}_{lec['num']}",
        }
        for lec in chapter["breakdown"]
    ]

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

        # Check if this is a full-chapter request — ask teacher to pick a lecture
        ch_key, s_key, chapter, lecture = ai.detect_lecture_scope(subject, topic, grade)
        if chapter is not None and lecture is None:
            _lecture_pending[uid] = {
                "subject": subject, "topic": topic, "grade": grade,
                "sel_dim": sel_dim, "channel": channel,
                "s_key": s_key, "ch_key": ch_key,
                "count": count,
            }
            buttons = _build_lecture_buttons(grade, s_key, ch_key, chapter)
            tmpl = _LECTURE_SELECT_MSG.get(language, _LECTURE_SELECT_MSG["en"])
            msg = tmpl.format(name=chapter["display_name"], grade=grade, num=chapter["num_lectures"])
            return _buttons(msg, buttons)

        response = ai.generate_content(subject, topic, grade, sel_dim, language, chat_id=uid, lecture=lecture)
        topic_label = f"{subject} — {topic}".strip(" —")
        db.log_message(uid, text, intent, response)
        return _post_content_feedback(uid, response, subject, topic_label, grade, language, channel, sel_dim, count)

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

    # Clear any stale pending states when a new message arrives
    _feedback_state.pop(uid, None)
    _lecture_pending.pop(uid, None)

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

    # Lecture selection
    if data.startswith("lec_"):
        return _handle_lecture_callback(uid, data)

    return _text("")


def _handle_feedback_callback(uid: str, data: str) -> dict:
    state = _feedback_state.get(uid)
    language = _language_cache.get(uid, "en")
    if not state:
        return _text("")

    step = state["step"]

    if step == 1 and data.startswith("fb_1_"):
        state["q1"] = data[5:]
        state["step"] = 2
        return _feedback_q(2, language)

    if step == 2 and data.startswith("fb_2_"):
        state["q2"] = data[5:]
        state["step"] = 3
        return _feedback_q(3, language)

    if step == 3 and data.startswith("fb_3_"):
        state["q3"] = data[5:]
        state["step"] = 4
        return _q4_question(0, language)  # persona

    if step == 4 and data.startswith("fb_4_"):
        state["q4a"] = data
        state["step"] = 5
        return _q4_question(1, language)  # home_context

    if step == 5 and data.startswith("fb_4_"):
        state["q4b"] = data
        state["step"] = 6
        return _q4_question(2, language)  # gender_gap

    if step == 6 and data.startswith("fb_4_"):
        state["q4c"] = data
        state["step"] = 7
        return _q4_question(3, language)  # group_pref

    if step == 7 and data.startswith("fb_4_"):
        state["q4d"] = data
        _save_feedback(uid, state)
        del _feedback_state[uid]
        return _text(_FEEDBACK_THANKS.get(language, _FEEDBACK_THANKS["en"]))

    return _text("")


def _handle_lecture_callback(uid: str, data: str) -> "dict | list":
    # data format: lec_<grade>_<subject_key>_<chapter_key>_<num>
    parts = data.split("_")
    if len(parts) < 5:
        return _text("")

    grade, subject_key, chapter_key, lec_num_str = parts[1], parts[2], parts[3], parts[4]
    try:
        lec_num = int(lec_num_str)
    except ValueError:
        return _text("")

    pending  = _lecture_pending.pop(uid, None)
    language = _language_cache.get(uid, "en")

    chapter = ncert_lecture_map.LECTURE_MAP.get(grade, {}).get(subject_key, {}).get(chapter_key)
    if not chapter:
        return _text("Sorry, I couldn't find that chapter. Please try again.")

    lecture = next((l for l in chapter["breakdown"] if l["num"] == lec_num), None)
    if not lecture:
        return _text("")

    subject = pending["subject"]            if pending else subject_key.title()
    topic   = pending["topic"]              if pending else chapter["display_name"]
    sel_dim = pending["sel_dim"]            if pending else ai.SEL_DIMENSIONS[0]
    channel = pending.get("channel", "telegram") if pending else "telegram"
    count   = pending.get("count", 0)      if pending else 0

    response    = ai.generate_content(subject, topic, grade, sel_dim, language, chat_id=uid, lecture=lecture)
    topic_label = f"{subject} — {lecture['title']}"
    db.log_message(uid, f"[lecture:{lec_num}] {data}", "content_generation", response)
    return _post_content_feedback(uid, response, subject, topic_label, grade, language, channel, sel_dim, count)
