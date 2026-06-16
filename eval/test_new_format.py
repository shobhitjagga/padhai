import sys, os
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
[Brief guided mindfulness activity with 2-3 guiding questions connected to the topic]
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
[Group activity instructions: group size, task, steps]
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
[One-line completion sentence for students]

---

Keep SEL woven into academic content throughout — do NOT add a separate SEL section.
Each concept section should naturally connect to the SEL theme.
Use India-relevant examples (local food, cricket, festivals, everyday objects).
"""

SEL_DISPLAY = {
    "growth_mindset":       "Growth Mindset (विकास की सोच)",
    "persistence":          "Persistence (दृढ़ता)",
    "self_awareness":       "Self-awareness (आत्म-जागरूकता)",
    "emotional_regulation": "Emotional Regulation (भावना नियंत्रण)",
    "social_awareness":     "Social Awareness (सामाजिक जागरूकता)",
}

test_cases = [
    {
        "subject":  "Science",
        "topic":    "भोजन: यह कहाँ से आता है?",
        "grade":    "6",
        "sel_dim":  "social_awareness",
        "language": "Hindi",
    },
    {
        "subject":  "Mathematics",
        "topic":    "परिमेय संख्याएँ (Rational Numbers)",
        "grade":    "8",
        "sel_dim":  "persistence",
        "language": "Hindi",
    },
]

for i, case in enumerate(test_cases, 1):
    print(f"\n{'='*80}")
    print(f"TEST CASE {i}: Class {case['grade']} {case['subject']} — {case['topic']}")
    print(f"SEL: {case['sel_dim']} | Language: {case['language']}")
    print("="*80)

    prompt = LESSON_PLAN_PROMPT.format(
        subject=case["subject"],
        topic=case["topic"],
        grade=case["grade"],
        sel_dims=SEL_DISPLAY.get(case["sel_dim"], case["sel_dim"]),
        language=case["language"],
    )

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1800,
    )
    print(resp.choices[0].message.content)
    print(f"\n[tokens: {resp.usage.prompt_tokens} in / {resp.usage.completion_tokens} out]")
