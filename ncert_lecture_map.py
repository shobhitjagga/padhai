"""
Chapter-to-lecture map for NCERT chapters.
Each chapter entry defines how many 45-minute sessions it needs and what each covers.

Currently: Class 9 Science — Sound.
Add more chapters here as the pilot expands.
"""

LECTURE_MAP = {
    "9": {
        "science": {
            "sound": {
                "display_name": "Sound",
                "num_lectures": 3,
                "breakdown": [
                    {
                        "num": 1,
                        "title": "Production & Propagation of Sound",
                        "keywords": [
                            "production", "propagation", "vibration", "medium",
                            "speed", "amplitude", "frequency", "pitch", "loudness",
                            "wavelength", "longitudinal", "wave",
                        ],
                        "topics": [
                            "How sound is produced — vibration of objects",
                            "Sound needs a medium; cannot travel in vacuum",
                            "Speed of sound in solids, liquids, and gases",
                            "Characteristics: amplitude (loudness), frequency (pitch), wavelength",
                            "Sound as a longitudinal wave — compressions and rarefactions",
                        ],
                        "ncert_sections": "12.1 – 12.4",
                    },
                    {
                        "num": 2,
                        "title": "Reflection of Sound — Echo & Reverberation",
                        "keywords": [
                            "reflection", "echo", "reverberation", "sonar",
                            "megaphone", "horn", "stethoscope", "concert", "hall",
                            "17m", "obstacle", "ceiling",
                        ],
                        "topics": [
                            "Laws of reflection of sound",
                            "Echo — minimum distance condition (17 m), time calculation",
                            "Reverberation — causes and how to reduce it",
                            "Applications: megaphones, bulged ceilings in concert halls",
                            "SONAR — Sound Navigation and Ranging; depth finding",
                        ],
                        "ncert_sections": "12.5 – 12.6",
                    },
                    {
                        "num": 3,
                        "title": "Ultrasound, Range of Hearing & Human Ear",
                        "keywords": [
                            "ultrasound", "infrasound", "range", "hearing",
                            "ear", "audible", "echolocation", "bat", "dolphin",
                            "medical", "cleaning", "20hz", "20000hz", "20 hz",
                        ],
                        "topics": [
                            "Audible range: 20 Hz to 20,000 Hz",
                            "Infrasound (below 20 Hz) — earthquakes, whales, elephants",
                            "Ultrasound (above 20,000 Hz) — bats, dolphins",
                            "Applications of ultrasound: medical imaging (sonography), "
                            "industrial cleaning, echolocation",
                            "Structure of the human ear and how we hear",
                        ],
                        "ncert_sections": "12.7 – 12.9",
                    },
                ],
            }
        }
    }
}

# ── Lookup helpers ─────────────────────────────────────────────────────────────

def _norm(s: str) -> str:
    return s.lower().strip()


def get_chapter(grade: str, subject: str, topic: str) -> tuple:
    """
    Return (subject_key, chapter_key, chapter_dict) if topic matches a known chapter.
    Returns (None, None, None) if no match.
    """
    grade_data = LECTURE_MAP.get(str(grade), {})
    subj_norm = _norm(subject)

    topic_norm = _norm(topic)
    for s_key, chapters in grade_data.items():
        if s_key in subj_norm or subj_norm in s_key:
            for ch_key, ch in chapters.items():
                if ch_key in topic_norm or _norm(ch["display_name"]) in topic_norm:
                    return s_key, ch_key, ch
    return None, None, None


def match_lecture(chapter: dict, topic: str) -> dict | None:
    """
    Given a chapter entry and a topic string, return the specific lecture
    if the topic is specific enough (keyword match), else None (= full chapter).
    """
    topic_norm = _norm(topic)
    best_lec, best_score = None, 0
    for lec in chapter["breakdown"]:
        score = sum(1 for kw in lec["keywords"] if kw in topic_norm)
        if score > best_score:
            best_score, best_lec = score, lec
    # Require at least 1 keyword hit AND that the topic isn't just the chapter name
    if best_score >= 1 and _norm(chapter["display_name"]) != topic_norm:
        return best_lec
    return None
