from supabase import create_client
import config

_client = None

def client():
    global _client
    if _client is None and config.SUPABASE_URL and config.SUPABASE_KEY:
        _client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    return _client


def log_message(chat_id: str, text: str, intent: str, response: str):
    try:
        c = client()
        if c:
            c.table("messages").insert({
                "chat_id":  str(chat_id),
                "text":     text,
                "intent":   intent,
                "response": response,
            }).execute()
    except Exception:
        pass  # logging must never break the bot


def upsert_user(chat_id: str, name: str):
    try:
        c = client()
        if c:
            c.table("users").upsert({
                "chat_id": str(chat_id),
                "name":    name,
            }).execute()
    except Exception:
        pass


def get_language(chat_id: str) -> str | None:
    try:
        c = client()
        if c:
            result = c.table("users").select("language").eq("chat_id", str(chat_id)).execute()
            if result.data:
                return result.data[0].get("language")
    except Exception:
        pass
    return None


def set_language(chat_id: str, language: str):
    try:
        c = client()
        if c:
            c.table("users").upsert({"chat_id": str(chat_id), "language": language}).execute()
    except Exception:
        pass


def complete_onboarding(chat_id: str, name: str, language: str):
    try:
        c = client()
        if c:
            c.table("users").upsert({
                "chat_id":  str(chat_id),
                "name":     name,
                "language": language,
            }).execute()
    except Exception:
        pass


def log_ai_call(chat_id: str, function: str, model: str, input: str, output: str,
                prompt_tokens: int = 0, completion_tokens: int = 0):
    try:
        c = client()
        if c:
            c.table("ai_calls").insert({
                "chat_id":           str(chat_id),
                "function":          function,
                "model":             model,
                "input":             input,
                "output":            output,
                "prompt_tokens":     prompt_tokens,
                "completion_tokens": completion_tokens,
            }).execute()
    except Exception:
        pass


def log_content_eval(chat_id: str, subject: str, topic: str, grade: str,
                     sel_dimension: str, scores: dict):
    try:
        c = client()
        if c:
            failed = [m for m, v in scores.items() if not v.get("verdict", True)]
            c.table("content_evals").insert({
                "chat_id":        str(chat_id),
                "subject":        subject,
                "topic":          topic,
                "grade":          grade,
                "sel_dimension":  sel_dimension,
                "scores":         scores,
                "failed_metrics": failed,
                "passed":         len(failed) == 0,
            }).execute()
    except Exception:
        pass


def log_usage_feedback(chat_id: str, topic: str, ncert_aligned: str,
                       sel_helpful: str, students_participated: str):
    try:
        c = client()
        if c:
            import json
            c.table("messages").insert({
                "chat_id": str(chat_id),
                "text":    f"[feedback] {topic}",
                "intent":  "usage_feedback",
                "response": json.dumps({
                    "topic":                 topic,
                    "ncert_aligned":         ncert_aligned,
                    "sel_helpful":           sel_helpful,
                    "students_participated": students_participated,
                }),
            }).execute()
    except Exception:
        pass


def get_content_count(chat_id: str) -> int:
    try:
        c = client()
        if c:
            result = (
                c.table("messages")
                .select("id", count="exact")
                .eq("chat_id", str(chat_id))
                .eq("intent", "content")
                .execute()
            )
            return result.count or 0
    except Exception:
        pass
    return 0
