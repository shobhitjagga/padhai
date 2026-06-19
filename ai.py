import json
from groq import Groq
from openai import OpenAI
import config
import db
from ncert_data import get_hindi9_context

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
  "grade":   "grade number as string, default 8 if not mentioned",
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
{chapter_context}
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

---

(Next 5 minutes) Mindfulness: [title linked to lesson theme]
[Brief guided imagination/mindfulness activity with 2-3 guiding questions connected to the topic. No physical props needed — imagination only.]
SEL Skill: [skill name]

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
Reflection Questions:
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
Answer based on NCERT curriculum for Class {grade}. Be accurate, concise, and grade-appropriate.
Keep answer under 150 words. Respond in {language}."""

SEL_OBS_PROMPT = """You are Padhai Bot, a supportive assistant for Indian school teachers.
A teacher has shared an observation about a student's behaviour or emotional state.
{grade_line}
Respond with:
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
        output = _groq_call(
            chat_id=chat_id,
            function="classify_intent",
            model="llama-3.1-8b-instant",
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
        return {"intent": "query_resolution_academic", "subject": "General", "topic": "", "grade": "8", "language": "en"}


GROQ_CONTENT_MODELS = [
    "llama-3.3-70b-versatile",
    "meta-llama/llama-4-scout-17b-16e-instruct",
]

def generate_content(subject: str, topic: str, grade: str, sel_dim: str,
                     language: str = "en", chat_id: str = "") -> str:
    guidance = SEL_GUIDANCE.get(sel_dim, {})

    is_hindi9 = grade == "9" and subject.strip().lower() in ["hindi", "हिंदी"]
    chapter_context = "\n" + get_hindi9_context(topic) + "\n" if is_hindi9 else ""

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
        chapter_context=chapter_context,
    )
    # Primary: OpenAI GPT-4.1 (better NCERT knowledge)
    if _oa_client():
        try:
            return _openai_call(
                chat_id=chat_id,
                function="generate_content",
                model="gpt-4.1",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000,
            )
        except Exception as e:
            print(f"[generate_content] OpenAI failed ({e}), falling back to Groq")
    # Fallback: Groq
    last_err = None
    for model in GROQ_CONTENT_MODELS:
        try:
            return _groq_call(
                chat_id=chat_id,
                function="generate_content",
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1800,
            )
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                print(f"[generate_content] {model} rate-limited, trying next model")
                last_err = e
                continue
            raise
    raise last_err


def resolve_query(question: str, grade: str = "8", language: str = "en", chat_id: str = "") -> str:
    return _groq_call(
        chat_id=chat_id,
        function="resolve_query",
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": QUERY_PROMPT.format(grade=grade, language=_lang_name(language))},
            {"role": "user",   "content": question},
        ],
        temperature=0.3,
        max_tokens=250,
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


def resolve_sel_observation(observation: str, grade: str = "8", language: str = "en", chat_id: str = "") -> str:
    grade_line = f"The student is in Class {grade}." if grade and grade != "8" else ""
    return _groq_call(
        chat_id=chat_id,
        function="resolve_sel_observation",
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SEL_OBS_PROMPT.format(grade_line=grade_line, language=_lang_name(language))},
            {"role": "user",   "content": observation},
        ],
        temperature=0.5,
        max_tokens=350,
    )
