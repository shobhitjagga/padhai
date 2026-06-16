import sys, os, csv, time
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from groq import Groq
import config

client = Groq(api_key=config.GROQ_API_KEY)

LESSON_PLAN_PROMPT = """You are ShikshaBot, an educational assistant for Indian government school teachers.
Generate a complete 45-minute SEL-integrated lesson plan strictly following NCERT curriculum.

Subject : {subject}
Chapter/Topic: {topic}
Grade   : Class {grade}
SEL Focus: {sel_dims}
Language: {language}

Structure the lesson plan EXACTLY as follows (in {language}):

विषय: [chapter name] (Subject + SEL Integration)
कक्षा: [grade]
समय: 45 मिनट
SEL Skills: [list the SEL skills to be developed]

---

1. Check-in + Mindfulness (10 मिनट)

(पहले 5 मिनट) भावनात्मक Check-in: [title]
गतिविधि: [activity name]
[2-3 discussion questions for the check-in]
SEL Skill: [skill name]

---

(अगले 5 मिनट) Mindfulness: [title linked to lesson theme]
[Brief guided imagination/mindfulness activity with 2-3 guiding questions connected to the topic. No physical props needed — imagination only.]
SEL Skill: [skill name]

---

2. NCERT Content Learning (25 मिनट)

Concept 1: [concept name] (8 मिनट)
NCERT: [one-line NCERT fact]
[Teacher discussion prompts and examples]
SEL Integration Question: [one question linking concept to SEL]

---

Concept 2: [concept name] (8 मिनट)
NCERT: [one-line NCERT fact]
Activity: [activity name]
[Activity description and reflection]
SEL Skill: [skill name]

---

Concept 3: [concept name] (9 मिनट)
[Discussion with SEL integration]
SEL Skill: [skill name]

---

3. Group Activity + Reflection (10 मिनट)

Activity: [activity name]
[Group activity: group size 4-5, task description, step-by-step]
Reflection Questions:
1. [question]
2. [question]
3. [question]

---

4. Revision + Way Forward (Last 5 मिनट)

Quick Recap:
Teacher पूछें:
1. [question]
2. [question]
3. [question]

Exit Ticket:
बच्चे एक लाइन लिखें: "आज से मैं __ रहूँगा/रहूँगी।"

---

Keep SEL woven into academic content throughout — do NOT add a separate SEL section.
Use India-relevant examples (local food, cricket, festivals, everyday objects — NOT pizza or US references).
Mindfulness must be guided imagination only, no physical props.
"""

SEL_DISPLAY = {
    "growth_mindset":       "Growth Mindset (विकास की सोच)",
    "persistence":          "Persistence (दृढ़ता)",
    "self_awareness":       "Self-awareness (आत्म-जागरूकता)",
    "emotional_regulation": "Emotional Regulation (भावना नियंत्रण)",
    "social_awareness":     "Social Awareness (सामाजिक जागरूकता)",
}

TEST_CASES = [
    # subject, topic, grade, sel_dim, language
    ("Science",       "भोजन: यह कहाँ से आता है?",              "6",  "social_awareness",     "Hindi"),
    ("Mathematics",   "परिमेय संख्याएँ (Rational Numbers)",     "8",  "persistence",           "Hindi"),
    ("Science",       "पौधों में पोषण (Nutrition in Plants)",   "7",  "growth_mindset",        "Hindi"),
    ("Mathematics",   "भिन्न (Fractions)",                      "5",  "self_awareness",        "Hindi"),
    ("Science",       "बल एवं गति के नियम",                    "9",  "persistence",           "Hindi"),
    ("Social Science","पृथ्वी की गतियाँ",                       "6",  "social_awareness",      "Hindi"),
    ("Science",       "कोशिका: जीवन की मूल इकाई",              "8",  "growth_mindset",        "Hindi"),
    ("Science",       "रासायनिक अभिक्रियाएँ एवं समीकरण",       "10", "emotional_regulation",  "Hindi"),
    ("Mathematics",   "त्रिभुज (Triangles)",                    "9",  "growth_mindset",        "Hindi"),
    ("Hindi",         "वन के मार्ग में (कविता)",               "8",  "self_awareness",        "Hindi"),
    ("Social Science","संसाधन एवं विकास",                       "10", "emotional_regulation",  "Hindi"),
    ("Science",       "जल: एक बहुमूल्य संसाधन",                "7",  "social_awareness",      "Hindi"),
    ("Mathematics",   "आँकड़ों का प्रबंधन (Data Handling)",    "6",  "self_awareness",        "Hindi"),
    ("Science",       "प्रकाश – परावर्तन तथा अपवर्तन",         "10", "persistence",           "Hindi"),
    ("Social Science","हमारा पर्यावरण",                         "7",  "social_awareness",      "Hindi"),
]

ANNOTATION_COLS = [
    "sections_complete",
    "time_allocated",
    "content_accurate",
    "ncert_aligned",
    "grade_appropriate",
    "sel_integrated",
    "sel_dimension_matched",
    "sel_has_reflection",
    "culturally_relevant",
]

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "content_generation_eval.csv")

def generate(subject, topic, grade, sel_dim, language):
    prompt = LESSON_PLAN_PROMPT.format(
        subject=subject,
        topic=topic,
        grade=grade,
        sel_dims=SEL_DISPLAY.get(sel_dim, sel_dim),
        language=language,
    )
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1800,
    )
    return resp.choices[0].message.content.strip()

def main():
    rows = []
    for i, (subject, topic, grade, sel_dim, language) in enumerate(TEST_CASES, 1):
        print(f"[{i:02d}/15] {subject} | Class {grade} | {topic[:40]}...", end=" ", flush=True)
        try:
            output = generate(subject, topic, grade, sel_dim, language)
            rows.append({
                "id": i,
                "subject": subject,
                "topic": topic,
                "grade": grade,
                "sel_dimension": sel_dim,
                "language": language,
                "generated_output": output,
                **{col: "" for col in ANNOTATION_COLS},
            })
            print("OK")
        except Exception as e:
            print(f"ERROR: {e}")
            rows.append({
                "id": i,
                "subject": subject,
                "topic": topic,
                "grade": grade,
                "sel_dimension": sel_dim,
                "language": language,
                "generated_output": f"ERROR: {e}",
                **{col: "" for col in ANNOTATION_COLS},
            })
        # avoid hitting rate limits
        if i < len(TEST_CASES):
            time.sleep(1)

    fieldnames = ["id", "subject", "topic", "grade", "sel_dimension", "language",
                  "generated_output"] + ANNOTATION_COLS

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved {len(rows)} rows → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
