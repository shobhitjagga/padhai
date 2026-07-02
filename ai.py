import json
from groq import Groq
from openai import OpenAI
import config
import db
import ncert_lecture_map
from ncert_data import get_hindi9_context
from ncert_data_class9 import get_class9_context

_groq_client = None
_openai_client = None

def client():
    global _groq_client
    if _groq_client is None:
        _groq_client = Groq(api_key=config.GROQ_API_KEY)
    return _groq_client

def _oa_client():
    global _openai_client
    if _openai_client is None and config.OPENAI_API_KEY:
        _openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
    return _openai_client


SEL_DIMENSIONS = [
    "growth_mindset",
    "persistence",
    "self_awareness",
    "emotional_regulation",
    "social_awareness",
]

SEL_LABELS = {
    "growth_mindset":      "Growth Mindset (विकास की सोच)",
    "persistence":         "Persistence (दृढ़ता)",
    "self_awareness":      "Self-Awareness (आत्म-जागरूकता)",
    "emotional_regulation":"Emotional Regulation (भावना नियंत्रण)",
    "social_awareness":    "Social Awareness (सामाजिक जागरूकता)",
}

# SEL activity guidance sourced from:
# - Delhi Happiness Curriculum (SCERT Delhi, 2019 framework + Class 5/6/7 Teacher Handbooks)
# - CBSE Life Skills Teacher Manual, Classes VI–X (Units 2, 7, 8, 9)
SEL_GUIDANCE = {
    "growth_mindset": {
        "concept": (
            "विकास की सोच (Growth Mindset): The belief that abilities grow through effort and practice. "
            "Mistakes are learning opportunities. Source: CBSE Life Skills IX-X, Unit 2 & 3 (Self-Awareness + Critical Thinking)."
        ),
        "activities": (
            "1. Belief mapping: Write on board — 'गलती करना सीखना है' — ask students 'क्या आप इससे सहमत हैं? अपने जीवन से एक उदाहरण दें।' "
            "2 students share, class responds. "
            "2. Ask: 'कोई एक काम बताएं जो पहले नहीं आता था, लेकिन मेहनत से आने लगा।' "
            "Connect to the academic concept being taught."
        ),
        "reflection_hi": (
            "• जब आप किसी कठिन काम में असफल होते हैं, आप खुद से क्या कहते हैं?\n"
            "• ऐसी एक चीज़ बताएं जो पहले नहीं आती थी, लेकिन मेहनत से आने लगी।\n"
            "• क्या मेहनत से कोई भी काम बेहतर किया जा सकता है?"
        ),
    },
    "persistence": {
        "concept": (
            "दृढ़ता (Persistence): Continuing to try despite difficulty or failure. Building resilience and self-motivation. "
            "Source: CBSE Life Skills Class VIII, Unit 11 (Problem Solving) + Unit 8 (Coping with Stress)."
        ),
        "activities": (
            "1. Obstacle mapping: Students write one learning goal, 2 obstacles, and one strategy for each — "
            "'मैं _______ करूँगा/करूँगी ताकि _______ न हो।' Pairs share strategies. "
            "2. Scenario role-play: 'मेहनत के बावजूद कम नंबर आए — आगे क्या करोगे?' "
            "Act out both giving-up and persisting responses. Debrief: 'किस प्रतिक्रिया ने आगे बढ़ने में मदद की?'"
        ),
        "reflection_hi": (
            "• जब कोई काम बहुत मुश्किल लगता है तो आप क्या करते हैं — छोड़ देते हैं या कोशिश जारी रखते हैं?\n"
            "• असफलता और हार में क्या फर्क है?\n"
            "• आपने इस सप्ताह किस चुनौती का सामना किया? अगली बार आप क्या अलग करेंगे?"
        ),
    },
    "self_awareness": {
        "concept": (
            "आत्म-जागरूकता (Self-Awareness): Understanding one's own feelings, strengths, and reactions. "
            "Source: CBSE Life Skills VIII-X, Unit 1 & 2 ('Me, This Is Me!' + 'Discover Yourself') + Delhi Happiness Curriculum daily check-in."
        ),
        "activities": (
            "1. Emotional check-in (daily Delhi Happiness Curriculum ritual): 'आज आप किस रंग में हैं?' or "
            "'आज आप कैसा महसूस कर रहे हैं — एक शब्द में?' No elaboration required unless student volunteers. "
            "2. Strengths mapping: Students write 'मेरी शक्तियाँ / मेरी कमजोरियाँ / मेरे सपने' (3 entries each), "
            "share one from each in groups of 3."
        ),
        "reflection_hi": (
            "• आज आपने खुद के बारे में क्या नया जाना?\n"
            "• आपकी सबसे बड़ी खूबी क्या है — और आप इसे कक्षा में कैसे इस्तेमाल करते हैं?\n"
            "• जब आप खुश होते हैं — आपके शरीर में क्या बदलाव होता है?"
        ),
    },
    "emotional_regulation": {
        "concept": (
            "भावना नियंत्रण (Emotional Regulation): Identifying, expressing, and managing emotions constructively. "
            "All feelings are valid; behaviors can be chosen. "
            "Source: CBSE Life Skills VIII, Unit 7 (Managing Emotions) + Unit 8 (Coping with Stress); Delhi Happiness Curriculum mindfulness structure."
        ),
        "activities": (
            "1. Emotion identification: Teacher presents scenario — 'परीक्षा में मेहनत के बाद भी कम नंबर आए।' "
            "Students write 'मुझे _______ लगेगा क्योंकि _______.' List on board — teacher affirms all feelings as valid. "
            "2. I-Message practice (CBSE Unit 7): Template — 'जब _______ होता है, मुझे _______ लगता है, क्योंकि _______।' "
            "Students practice 2 real scenarios from their school life."
        ),
        "reflection_hi": (
            "• जब आप बहुत गुस्से में होते हैं, आपके शरीर में क्या बदलाव होता है?\n"
            "• क्या सभी भावनाएँ — जैसे दुख, डर, गुस्सा — ठीक हैं? क्यों?\n"
            "• कोई एक ऐसी स्थिति बताएं जब आपने अपनी भावना को काबू किया — आपने क्या किया?"
        ),
    },
    "social_awareness": {
        "concept": (
            "सामाजिक जागरूकता (Social Awareness): Empathy, understanding others' perspectives, gratitude, and care for community. "
            "Source: CBSE Life Skills IX-X, Unit 9 (Empathy) + Delhi Happiness Curriculum Unit 2 "
            "(Experiencing Happiness in Relationships: care, gratitude, trust, respect)."
        ),
        "activities": (
            "1. Mirror exercise (CBSE Unit 9): Pairs — one leads movement, partner mirrors silently. Switch. "
            "Debrief: 'बिना बोले किसी को समझना कैसा लगा?' Connect to empathy in the lesson topic. "
            "2. 'Who Needs My Help?' mapping: Students draw concentric circles — self, family, class, neighborhood — "
            "identify one person in each ring who might need something. Plan one action: "
            "'मैं इस हफ्ते _______ की मदद करूँगा/करूँगी।'"
        ),
        "reflection_hi": (
            "• आपको कैसे पता चलता है कि कोई दोस्त दुखी है?\n"
            "• किसने इस हफ्ते आपकी मदद की — आपने उन्हें धन्यवाद कहा?\n"
            "• किसी ऐसे व्यक्ति के बारे में सोचें जो आपसे बहुत अलग है। उसकी एक अच्छी बात क्या है?"
        ),
    },
}

SEL_PEDAGOGY = """Pedagogical principles (from Delhi Happiness Curriculum + CBSE Life Skills Manual — mandatory):
- Non-judgmental zone: "कोई भी जवाब गलत नहीं है" — state this before SEL activities
- Open with guided imagination (eyes closed, no props) — connect to the lesson theme
- Pair-share before whole-class — reduces anxiety in Hindi-medium classrooms
- Teacher facilitates, does not lecture — at least half the SEL time is student expression
- Never grade or evaluate SEL responses — qualitative observation only"""

# ── Prompts ────────────────────────────────────────────────────────────────────

INTENT_PROMPT = """You are an intent classifier for an educational bot used by Indian school teachers.

Classify the message into exactly one intent:
- "content_generation"       : teacher wants a lesson, explanation, or activity on a subject/topic
                               e.g. "give me a lesson on fractions", "activity for water cycle"
- "query_resolution_academic": teacher has a specific academic/curriculum question wanting a direct answer
                               e.g. "what is photosynthesis", "explain Newton's laws"
- "feedback"                 : teacher is expressing a reaction to the bot — positive or negative
                               e.g. "I like this", "this was helpful", "not useful", "great response", "I don't like this"
- "query_resolution_sel"     : teacher is sharing an observation about a student's behaviour or emotional state
                               e.g. "student is not engaging", "student not speaking up", "child seems distracted", "student is very shy"
- "out_of_service"           : message is unrelated to NCERT classroom teaching
                               e.g. JEE/NEET/IELTS prep, stock market, coding help, personal advice, college admissions
- "language_change"          : teacher wants to change the bot's response language
                               e.g. "respond in Hindi", "Hindi mein baat karo", "switch to English", "Tamil mein jawab do"
                               For this intent, set "language" to the REQUESTED target language (not the input language)

Return ONLY valid JSON with these keys:
{
  "intent":  "content_generation|query_resolution_academic|feedback|query_resolution_sel|out_of_service|language_change",
  "subject": "Mathematics|Science|Social Science|English|Hindi|General",
  "topic":   "specific topic if mentioned, else empty string",
  "grade":   "grade number as string, or empty string if not mentioned",
  "language":"en|hi|ta|te|mr|kn|bn"
}"""

CONTENT_PROMPT = """You are Padhai Bot, an educational assistant for Indian government school teachers.
Generate a complete 45-minute SEL-integrated lesson plan strictly following NCERT curriculum.

Subject : {subject}
Chapter/Topic: {topic}
Grade   : Class {grade}
SEL Focus: {sel_label}
Language: {language}

--- SEL GROUNDING (from Delhi Happiness Curriculum + CBSE Life Skills Manual) ---
{sel_concept}

Recommended SEL activities for this dimension:
{sel_activities}

Use these reflection questions (adapt to fit the lesson topic):
{sel_reflection}

{sel_pedagogy}
--- END SEL GROUNDING ---
{class_context}{chapter_context}
CRITICAL: Write the ENTIRE lesson plan in {language}. Every word — section headers, time labels, activity descriptions, questions, and the exit ticket — must be in {language}. Do not use any other language.

Structure the lesson plan EXACTLY as follows:

Subject: [chapter name] (Subject + SEL Integration)
Grade: [grade]
Duration: 45 minutes
SEL Skills: [list the SEL skills to be developed]

---

1. Check-in + Mindfulness (10 minutes)

(First 5 minutes) Emotional Check-in: [title]
Activity: [activity name]
Discussion Question: [1 question for the check-in]
SEL Skill: [skill name]
Facilitation note: [Exact phrase to open — e.g. "Close your eyes and think about…". If no one responds: wait 8 seconds silently, then model a response yourself — "For me it was…". Watch for: at least 2–3 students sharing before moving on.]

---

(Next 5 minutes) Mindfulness: [title linked to lesson theme]
[Brief guided imagination/mindfulness activity with 2-3 guiding questions connected to the topic. No physical props needed — imagination only.]
SEL Skill: [skill name]
Facilitation note: [Use a slow, paused voice. If students giggle or fidget: say "That's okay — just try for a moment" and continue. To close: ask one student to share one image that came to mind, then link it to today's lesson topic.]

---

2. NCERT Content Learning (25 minutes)

Concept 1: [concept name] (8 minutes)
NCERT: [one-line NCERT fact]
[Teacher discussion prompts and examples]
SEL Integration Question: [one question linking concept to SEL]

---

Concept 2: [concept name] (8 minutes)
NCERT: [one-line NCERT fact]
Activity: [activity name]
[Activity description and reflection]
SEL Skill: [skill name]

---

Concept 3: [concept name] (9 minutes)
[Discussion with SEL integration]
SEL Skill: [skill name]

---

3. Group Activity + Reflection (10 minutes)

Activity: [activity name]
[Group activity: group size 4-5, task description, step-by-step]
Facilitation note: [Give the task in one sentence before releasing groups. If a group finishes early: ask them to add one more idea. During sharing: invite quiet students with a low-stakes opener — "What did your group decide?" — not "What do you think?"]
{group_differentiation}Reflection Questions:
1. [question]
2. [question]
3. [question]

---

4. Revision + Way Forward (Last 5 minutes)

Quick Recap:
Teacher asks:
1. [question]
2. [question]
3. [question]

Homework:
[One specific, doable homework question or task directly from the NCERT chapter — not generic, tied to today's concepts]

---

Keep SEL woven into academic content throughout — do NOT add a separate SEL section.
Use India-relevant examples (local food, cricket, festivals, everyday objects — NOT pizza or US references).
Mindfulness must be guided imagination only, no physical props."""

QUERY_PROMPT = """You are Padhai Bot, an educational assistant for Indian school teachers.
Answer based on NCERT curriculum{grade_str}. Be accurate, concise, and grade-appropriate.
Keep answer under 150 words. Respond in {language}."""

SEL_OBS_PROMPT = """You are Padhai Bot, a supportive assistant for Indian school teachers.
A teacher has shared an observation about a student's behaviour or emotional state.
{grade_line}

SAFEGUARDING CHECK — READ FIRST BEFORE RESPONDING:
If the teacher's message contains ANY of the following signals, you MUST respond with ONLY the safeguarding message below and nothing else:

Signals that require immediate escalation:
- Any mention of physical marks, bruises, or injuries on the student that the student cannot explain
- Any hint of sexual abuse, inappropriate touching, or sexual behaviour in a child (POCSO)
- Student expressing a wish to die, not wanting to live, or harming themselves
- Student disclosing violence, abuse, or severe neglect at home
- Teacher suspecting a specific adult is harming the child

If ANY of the above are present, respond with EXACTLY this (translated into {language}):

"यह एक गंभीर स्थिति है जिसके लिए तत्काल कार्रवाई की आवश्यकता है।

अभी करें:
1. बच्चे को अकेला न छोड़ें और शांत रखें
2. अपने प्रधानाध्यापक या स्कूल प्रबंधन समिति को तुरंत सूचित करें
3. CHILDLINE को कॉल करें: 1098 (24 घंटे, निःशुल्क, हिंदी सहित सभी भाषाओं में)
4. POCSO अधिनियम के तहत हर वयस्क को संदिग्ध बाल शोषण की रिपोर्ट करना कानूनी रूप से अनिवार्य है

इस स्थिति में कक्षा में अकेले कोई कदम न उठाएं — सही लोगों को शामिल करें।"

---

If NONE of the above signals are present, respond with:
1. Acknowledge: validate the teacher's concern warmly (1 sentence)
2. Possible reasons: 2-3 common reasons this behaviour occurs at this age/grade
3. What to try: 2-3 specific, practical actions the teacher can take in the classroom
4. What to avoid: 1 thing that often makes it worse

Be practical, non-judgmental, and grounded in classroom reality.
Keep under 200 words. Respond in {language}."""

CONTENT_EVAL_PROMPT = """You are a quality evaluator for Padhai Bot, an educational chatbot for Indian school teachers.

Evaluate the lesson plan below on 9 criteria. The lesson plan is in {language}.

Lesson metadata:
- Subject: {subject}
- Topic: {topic}
- Grade: Class {grade}
- Requested SEL Dimension: {sel_dimension}

Criteria:
1. sections_complete — All 4 sections present: (1) Check-in + Mindfulness ~10 min, (2) NCERT Content Learning ~25 min with 3 concepts, (3) Group Activity + Reflection ~10 min, (4) Revision + Way Forward ~5 min
2. time_allocated — Time in minutes is explicitly written next to each section/concept heading (e.g. "8 मिनट", "10 मिनट")
3. content_accurate — All NCERT facts stated are scientifically/academically correct for the subject
4. ncert_aligned — Concepts and terminology match NCERT curriculum for Class {grade} {subject}
5. grade_appropriate — The concepts, depth, and terminology match what is actually taught in the Class {grade} NCERT textbook. Mark FALSE if the content uses concepts introduced in a different grade's NCERT book (either too advanced from a higher grade, or too basic from a lower grade)
6. sel_integrated — SEL is woven into the academic content throughout, NOT added as a separate standalone section
7. sel_dimension_matched — The SEL dimension "{sel_dimension}" is clearly and consistently present (not just mentioned once)
8. sel_has_reflection — At least one explicit reflection question or activity is tied to the SEL dimension
9. culturally_relevant — Examples use Indian context (local food, cricket, festivals, everyday objects) — no exclusively Western references

Return ONLY valid JSON, no other text:
{{
  "sections_complete":     {{"verdict": true, "reason": "one sentence"}},
  "time_allocated":        {{"verdict": true, "reason": "one sentence"}},
  "content_accurate":      {{"verdict": true, "reason": "one sentence"}},
  "ncert_aligned":         {{"verdict": true, "reason": "one sentence"}},
  "grade_appropriate":     {{"verdict": true, "reason": "one sentence"}},
  "sel_integrated":        {{"verdict": true, "reason": "one sentence"}},
  "sel_dimension_matched": {{"verdict": true, "reason": "one sentence"}},
  "sel_has_reflection":    {{"verdict": true, "reason": "one sentence"}},
  "culturally_relevant":   {{"verdict": true, "reason": "one sentence"}}
}}"""

# ── Class profile → prompt guidance mappings ──────────────────────────────────

_VERBAL_GUIDANCE = {
    "high":   "Students participate verbally — use open discussions and pair-share freely.",
    "medium": "Mix verbal and written activities — start with pair-share before whole-class.",
    "low":    "Most students are quiet — prefer written/think-pair-share, avoid cold-calling, provide sentence starters for every response.",
}
_ENERGY_GUIDANCE = {
    "focused": "Class is calm and focused — standard pacing works, mindfulness can be unhurried.",
    "high":    "Class is energetic/restless — use short activity bursts, add physical elements (stand up, sort cards), keep transitions snappy.",
    "low":     "Class is often tired or distracted — open with an energising check-in, keep activities shorter, avoid long monologue stretches.",
}
_PERSONA_GUIDANCE = {
    "shy":       "Most students are shy and rarely raise hands — never cold-call, use anonymous written inputs and sentence starters for every response, pair-share before any whole-class sharing.",
    "mixed":     "Mix of shy and assertive students — pair shy students with supportive peers, assign structured roles in group work so quieter students have a defined contribution.",
    "assertive": "Students are eager to participate — leverage this with leadership roles and challenge tasks, but actively create space so a few voices don't dominate.",
}
_HOME_GUIDANCE = {
    "difficult": "Many students come from daily-wage households or have parents often absent — keep homework minimal and fully self-sufficient (no parental help needed), keep emotional check-ins low-pressure and avoid topics that highlight family differences.",
    "mixed":     "Mixed home situations — all homework must be doable without parental help.",
    "stable":    "Most students have stable home support — can include family-discussion or observation homework.",
}
_GENDER_GUIDANCE = {
    "yes":     "Girls are usually quieter than boys — actively create space: try girls-first sharing, same-gender pairs for initial reflection, and structured turn-taking to prevent boys from dominating.",
    "partial": "Some gender gap in participation — use structured turn-taking and thoughtfully mixed pairs.",
    "no":      "Both genders participate roughly equally — no gender-specific adaptation needed.",
}
_GROUP_GUIDANCE = {
    "high":  "This class loves group work — use collaborative activities freely, assign clear roles (facilitator, note-taker, presenter).",
    "mixed": "Mixed preference for group work — offer individual reflection time before group sharing.",
    "low":   "Students prefer individual work — keep groups small (2–3 max), always give individual reflection time before any group activity.",
}

def _build_class_context(profile: dict) -> str:
    """Convert a class_profiles row into a prompt injection block."""
    if not profile or not profile.get("session_count"):
        return ""
    lines = [
        f"\n--- CLASS PROFILE ({profile['session_count']} sessions of teacher feedback"
        " — adapt SEL activities to fit this specific class) ---"
    ]
    for val, guide in [
        (profile.get("verbal_tendency", ""), _VERBAL_GUIDANCE),
        (profile.get("energy_tendency", ""), _ENERGY_GUIDANCE),
        (profile.get("persona", ""),         _PERSONA_GUIDANCE),
        (profile.get("home_context", ""),    _HOME_GUIDANCE),
        (profile.get("gender_gap", ""),      _GENDER_GUIDANCE),
        (profile.get("group_pref", ""),      _GROUP_GUIDANCE),
    ]:
        if val and val in guide:
            lines.append(f"• {guide[val]}")
    lines.append(
        "Apply ALL of the above adaptations throughout the lesson — "
        "especially in SEL activities, pair-share design, and the group activity section."
    )
    lines.append("--- END CLASS PROFILE ---\n")
    return "\n".join(lines)


# ── Differentiated group activities (feature flag) ─────────────────────────────
# Set to True to ask the model to design three group-type variants in section 3.
# Currently OFF — the standard single group activity is used.
DIFFERENTIATED_GROUPS = False

GROUP_DIFFERENTIATION_INSTRUCTIONS = """
Within the Group Activity section, design THREE parallel variants of the same activity
so the teacher can assign groups by student profile:

Group A — Shy / Quiet students:
• Start with individual written reflection before any sharing
• Pair-share first (not whole group), teacher checks in quietly
• Written / drawn response accepted as an alternative to speaking aloud

Group B — Struggling / Low-confidence students:
• Simplified version of the same task with concrete visual or fill-in-the-blank scaffold
• Assign a supportive peer buddy within the group
• Focus on one concept instead of all three

Group C — Assertive / High-energy students:
• Give a leadership role (facilitator, note-taker, presenter) with clear responsibility
• Add an extension challenge or debate element to the task
• Include a physical / kinesthetic step (stand up, sort cards, draw on board)

All three groups do the same reflection questions at the end.
Label each variant clearly: Group A, Group B, Group C.
"""

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "kn": "Kannada",
    "bn": "Bengali",
}

def _lang_name(code: str) -> str:
    return LANGUAGE_NAMES.get(code, "English")

# ── Functions ──────────────────────────────────────────────────────────────────

def _groq_call(chat_id: str, function: str, model: str, messages: list, **kwargs) -> str:
    resp = client().chat.completions.create(model=model, messages=messages, **kwargs)
    output = resp.choices[0].message.content
    usage  = resp.usage
    db.log_ai_call(
        chat_id=chat_id,
        function=function,
        model=model,
        input=messages[-1]["content"],
        output=output,
        prompt_tokens=usage.prompt_tokens if usage else 0,
        completion_tokens=usage.completion_tokens if usage else 0,
    )
    return output


def _openai_call(chat_id: str, function: str, model: str, messages: list, **kwargs) -> str:
    resp = _oa_client().chat.completions.create(model=model, messages=messages, **kwargs)
    output = resp.choices[0].message.content
    usage  = resp.usage
    db.log_ai_call(
        chat_id=chat_id,
        function=function,
        model=model,
        input=messages[-1]["content"][:500],
        output=output,
        prompt_tokens=usage.prompt_tokens if usage else 0,
        completion_tokens=usage.completion_tokens if usage else 0,
    )
    return output


def classify_intent(text: str, chat_id: str = "") -> dict:
    try:
        output = _openai_call(
            chat_id=chat_id,
            function="classify_intent",
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": INTENT_PROMPT},
                {"role": "user",   "content": text},
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
        )
        return json.loads(output)
    except Exception as e:
        print(f"[classify_intent error] {e}")
        return {"intent": "query_resolution_academic", "subject": "General", "topic": "", "grade": "", "language": "en"}


def detect_lecture_scope(subject: str, topic: str, grade: str) -> tuple:
    """Returns (chapter_key, subject_key, chapter_dict, lecture_dict).
    chapter_dict is None if topic doesn't match any known chapter.
    lecture_dict is None if topic is a whole chapter → teacher must pick a lecture.
    """
    s_key, ch_key, chapter = ncert_lecture_map.get_chapter(grade, subject, topic)
    if chapter is None:
        return None, None, None, None
    lecture = ncert_lecture_map.match_lecture(chapter, topic)
    return ch_key, s_key, chapter, lecture


GROQ_CONTENT_MODELS = [
    "llama-3.3-70b-versatile",
    "meta-llama/llama-4-scout-17b-16e-instruct",
]

def generate_content(subject: str, topic: str, grade: str, sel_dim: str,
                     language: str = "en", chat_id: str = "",
                     lecture: dict | None = None) -> str:
    import hashlib
    guidance = SEL_GUIDANCE.get(sel_dim, {})

    # Personalise based on accumulated class profile
    profile = db.get_class_profile(chat_id, grade, subject) if chat_id else {}
    class_context = _build_class_context(profile)

    # NCERT chapter-level grounding for Class 9 (all subjects)
    if grade == "9":
        if subject.strip().lower() in ["hindi", "हिंदी"]:
            chapter_context = "\n" + get_hindi9_context(topic) + "\n"
        else:
            ctx = get_class9_context(subject, topic)
            chapter_context = "\n" + ctx + "\n" if ctx else ""
    else:
        chapter_context = ""

    if lecture:
        topics_str = "\n".join(f"• {t}" for t in lecture["topics"])
        chapter_context += (
            f"\n--- LECTURE SCOPE (MANDATORY) ---\n"
            f"This plan covers ONLY Lecture {lecture['num']} of this chapter: \"{lecture['title']}\"\n"
            f"Topics to teach:\n{topics_str}\n"
            f"NCERT sections: {lecture.get('ncert_sections', '')}\n"
            f"Do NOT include topics from other lectures of the same chapter.\n"
            f"--- END LECTURE SCOPE ---\n"
        )
        if " — " not in topic:
            topic = f"{topic} — {lecture['title']}"

    group_diff = GROUP_DIFFERENTIATION_INSTRUCTIONS if DIFFERENTIATED_GROUPS else ""

    # Cache key — includes lecture scope and class profile so personalised responses
    # are cached separately from generic ones
    lecture_key = lecture["title"] if lecture else ""
    cache_key = hashlib.sha256(
        f"{subject}|{topic}|{grade}|{sel_dim}|{language}|{lecture_key}|{class_context}".encode()
    ).hexdigest()

    cached = db.get_cached_content(cache_key)
    if cached:
        print(f"[generate_content] cache hit  key={cache_key[:12]}", flush=True)
        return cached

    prompt = CONTENT_PROMPT.format(
        subject=subject,
        topic=topic or subject,
        grade=grade,
        sel_label=SEL_LABELS.get(sel_dim, sel_dim),
        language=_lang_name(language),
        sel_concept=guidance.get("concept", ""),
        sel_activities=guidance.get("activities", ""),
        sel_reflection=guidance.get("reflection_hi", ""),
        sel_pedagogy=SEL_PEDAGOGY,
        class_context=class_context,
        chapter_context=chapter_context,
        group_differentiation=group_diff,
    )
    # Primary: OpenAI GPT-4.1 (better NCERT knowledge)
    if _oa_client():
        try:
            result = _openai_call(
                chat_id=chat_id,
                function="generate_content",
                model="gpt-4.1",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000,
            )
            db.store_cached_content(cache_key, result)
            return result
        except Exception as e:
            print(f"[generate_content] OpenAI failed ({e}), falling back to Groq")
    # Fallback: Groq
    last_err = None
    for model in GROQ_CONTENT_MODELS:
        try:
            result = _groq_call(
                chat_id=chat_id,
                function="generate_content",
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1800,
            )
            db.store_cached_content(cache_key, result)
            return result
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                print(f"[generate_content] {model} rate-limited, trying next model")
                last_err = e
                continue
            raise
    raise last_err


def resolve_query(question: str, grade: str = "", language: str = "en", chat_id: str = "") -> str:
    grade_str = f" for Class {grade}" if grade else ""
    return _openai_call(
        chat_id=chat_id,
        function="resolve_query",
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": QUERY_PROMPT.format(grade_str=grade_str, language=_lang_name(language))},
            {"role": "user",   "content": question},
        ],
        temperature=0.3,
        max_tokens=400,
    )


def evaluate_content(subject: str, topic: str, grade: str, sel_dimension: str,
                     language: str, content: str, chat_id: str = "") -> dict | None:
    prompt = CONTENT_EVAL_PROMPT.format(
        subject=subject,
        topic=topic,
        grade=grade,
        sel_dimension=sel_dimension,
        language=_lang_name(language),
    )
    try:
        output = _groq_call(
            chat_id=chat_id,
            function="evaluate_content",
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user",   "content": content},
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
        )
        return json.loads(output)
    except Exception as e:
        print(f"[evaluate_content error] {e}")
        return None


def resolve_sel_observation(observation: str, grade: str = "", language: str = "en", chat_id: str = "") -> str:
    grade_line = f"The student is in Class {grade}." if grade else ""
    return _openai_call(
        chat_id=chat_id,
        function="resolve_sel_observation",
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SEL_OBS_PROMPT.format(grade_line=grade_line, language=_lang_name(language))},
            {"role": "user",   "content": observation},
        ],
        temperature=0.5,
        max_tokens=350,
    )
