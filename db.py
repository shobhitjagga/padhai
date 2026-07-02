from datetime import datetime, timezone, timedelta
from supabase import create_client
import config

_IST = timezone(timedelta(hours=5, minutes=30))

def _next_2pm_utc() -> str:
    """Return the next 2:00 PM IST as a UTC ISO string."""
    now_ist = datetime.now(_IST)
    target  = now_ist.replace(hour=14, minute=0, second=0, microsecond=0)
    if now_ist >= target:
        target += timedelta(days=1)
    return target.astimezone(timezone.utc).isoformat()


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


def log_usage_feedback(chat_id: str, topic: str, grade: str, subject: str,
                       ncert_aligned: str, sel_engagement: str,
                       class_energy: str, q4_data: str = ""):
    try:
        c = client()
        if c:
            import json
            c.table("messages").insert({
                "chat_id": str(chat_id),
                "text":    f"[feedback] {topic}",
                "intent":  "usage_feedback",
                "response": json.dumps({
                    "topic":          topic,
                    "grade":          grade,
                    "subject":        subject,
                    "ncert_aligned":  ncert_aligned,   # full | partial | no
                    "sel_engagement": sel_engagement,  # verbal | mixed | quiet
                    "class_energy":   class_energy,    # focused | high | low
                    "q4_data":        q4_data,
                }),
            }).execute()
    except Exception:
        pass


def _majority(a: int, b: int, c: int, labels: list[str]) -> str:
    return labels[[a, b, c].index(max(a, b, c))]


def update_class_profile(chat_id: str, grade: str, subject: str, signals: dict):
    """Upsert incremental session signals into class_profiles."""
    try:
        c = client()
        if not c:
            return
        uid = str(chat_id)
        g   = grade.strip()
        s   = subject.strip().lower()

        verbal  = signals.get("verbal", "")   # verbal | mixed | quiet
        energy  = signals.get("energy", "")   # focused | high | low
        sel_run = signals.get("q5", "")       # fb_5_sel_yes | fb_5_sel_partial | fb_5_sel_no
        quiet   = signals.get("q6", "")       # fb_6_quiet_yes | fb_6_quiet_no | fb_6_quiet_unsure

        vh = 1 if verbal == "verbal"  else 0
        vm = 1 if verbal == "mixed"   else 0
        vl = 1 if verbal == "quiet"   else 0
        ef = 1 if energy == "focused" else 0
        eh = 1 if energy == "high"    else 0
        el = 1 if energy == "low"     else 0
        sry = 1 if "sel_yes"     in sel_run else 0
        srp = 1 if "sel_partial" in sel_run else 0
        srn = 1 if "sel_no"      in sel_run else 0
        qy  = 1 if "quiet_yes"   in quiet   else 0
        qn  = 1 if "quiet_no"    in quiet   else 0
        qu  = 1 if "quiet_unsure"in quiet   else 0

        # Parse stable descriptors from all Q4 answers (q4, q4a–q4d)
        stable: dict = {}
        for key in ("q4", "q4a", "q4b", "q4c", "q4d"):
            val = signals.get(key, "")
            if not val:
                continue
            if "_persona_" in val:
                for v in ("shy", "mixed", "assertive"):
                    if v in val: stable["persona"] = v
            elif "_home_" in val:
                for v in ("difficult", "mixed", "stable"):
                    if v in val: stable["home_context"] = v
            elif "_gender_" in val:
                stable["gender_gap"] = (
                    "yes"     if "gap"     in val else
                    "partial" if "partial" in val else "no"
                )
            elif "_group_" in val:
                for v in ("high", "mixed", "low"):
                    if v in val: stable["group_pref"] = v

        existing = (
            c.table("class_profiles")
            .select("*")
            .eq("chat_id", uid).eq("grade", g).eq("subject", s)
            .execute()
        )

        if existing.data:
            row = existing.data[0]
            nvh = row["verbal_high_count"]  + vh
            nvm = row["verbal_mid_count"]   + vm
            nvl = row["verbal_low_count"]   + vl
            nef = row["energy_focused_count"] + ef
            neh = row["energy_high_count"]  + eh
            nel = row["energy_low_count"]   + el
            update = {
                "session_count":        row["session_count"] + 1,
                "verbal_high_count":    nvh,
                "verbal_mid_count":     nvm,
                "verbal_low_count":     nvl,
                "energy_focused_count": nef,
                "energy_high_count":    neh,
                "energy_low_count":     nel,
                "verbal_tendency":      _majority(nvh, nvm, nvl, ["high", "medium", "low"]),
                "energy_tendency":      _majority(nef, neh, nel, ["focused", "high", "low"]),
                "sel_run_yes_count":     row["sel_run_yes_count"]     + sry,
                "sel_run_partial_count": row["sel_run_partial_count"] + srp,
                "sel_run_no_count":      row["sel_run_no_count"]      + srn,
                "quiet_yes_count":       row["quiet_yes_count"]       + qy,
                "quiet_no_count":        row["quiet_no_count"]        + qn,
                "quiet_unsure_count":    row["quiet_unsure_count"]    + qu,
                "updated_at": datetime.now(timezone.utc).isoformat(),
                **stable,
            }
            (c.table("class_profiles")
             .update(update)
             .eq("chat_id", uid).eq("grade", g).eq("subject", s)
             .execute())
        else:
            insert = {
                "chat_id": uid, "grade": g, "subject": s,
                "session_count": 1,
                "verbal_high_count": vh, "verbal_mid_count": vm, "verbal_low_count": vl,
                "energy_focused_count": ef, "energy_high_count": eh, "energy_low_count": el,
                "verbal_tendency": _majority(vh, vm, vl, ["high", "medium", "low"]),
                "energy_tendency": _majority(ef, eh, el, ["focused", "high", "low"]),
                "sel_run_yes_count": sry, "sel_run_partial_count": srp, "sel_run_no_count": srn,
                "quiet_yes_count": qy, "quiet_no_count": qn, "quiet_unsure_count": qu,
                **stable,
            }
            c.table("class_profiles").insert(insert).execute()
    except Exception as e:
        print(f"[update_class_profile] {e}", flush=True)


def get_class_profile(chat_id: str, grade: str, subject: str) -> dict:
    """Return the class profile dict, or {} if not yet built."""
    try:
        c = client()
        if c:
            result = (
                c.table("class_profiles")
                .select("*")
                .eq("chat_id", str(chat_id))
                .eq("grade", grade.strip())
                .eq("subject", subject.strip().lower())
                .execute()
            )
            if result.data:
                return result.data[0]
    except Exception as e:
        print(f"[get_class_profile] {e}", flush=True)
    return {}


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


def schedule_feedback_q1(chat_id: str, language: str, topic: str, channel: str,
                         grade: str = "", subject: str = "",
                         q4_due: bool = False, q4_index: int = 0):
    """Insert a feedback job scheduled for the next 2 PM IST."""
    try:
        c = client()
        if c:
            c.table("feedback_jobs").insert({
                "chat_id":      str(chat_id),
                "language":     language,
                "topic":        topic,
                "channel":      channel,
                "grade":        grade,
                "subject":      subject,
                "q4_due":       q4_due,
                "q4_index":     q4_index,
                "scheduled_at": _next_2pm_utc(),
            }).execute()
    except Exception as e:
        print(f"[schedule_feedback_q1] {e}", flush=True)


def get_due_feedback_jobs() -> list:
    """Return all unsent jobs whose scheduled_at has passed."""
    try:
        c = client()
        if c:
            now = datetime.now(timezone.utc).isoformat()
            result = (
                c.table("feedback_jobs")
                .select("*")
                .lte("scheduled_at", now)
                .is_("sent_at", "null")
                .execute()
            )
            return result.data or []
    except Exception as e:
        print(f"[get_due_feedback_jobs] {e}", flush=True)
    return []


def mark_feedback_job_sent(job_id: int):
    try:
        c = client()
        if c:
            now = datetime.now(timezone.utc).isoformat()
            c.table("feedback_jobs").update({"sent_at": now}).eq("id", job_id).execute()
    except Exception as e:
        print(f"[mark_feedback_job_sent] {e}", flush=True)


_CACHE_TTL_DAYS = 7

def get_cached_content(cache_key: str) -> str | None:
    try:
        c = client()
        if c:
            cutoff = (datetime.now(timezone.utc) - timedelta(days=_CACHE_TTL_DAYS)).isoformat()
            result = (
                c.table("content_cache")
                .select("response")
                .eq("cache_key", cache_key)
                .gt("created_at", cutoff)
                .limit(1)
                .execute()
            )
            if result.data:
                return result.data[0]["response"]
    except Exception as e:
        print(f"[get_cached_content] {e}", flush=True)
    return None


def store_cached_content(cache_key: str, response: str):
    try:
        c = client()
        if c:
            c.table("content_cache").upsert({"cache_key": cache_key, "response": response}).execute()
    except Exception as e:
        print(f"[store_cached_content] {e}", flush=True)


def get_all_class_profiles(chat_id: str) -> list:
    try:
        c = client()
        if c:
            result = (
                c.table("class_profiles")
                .select("*")
                .eq("chat_id", str(chat_id))
                .order("updated_at", desc=True)
                .execute()
            )
            return result.data or []
    except Exception as e:
        print(f"[get_all_class_profiles] {e}", flush=True)
    return []


def delete_all_class_profiles(chat_id: str):
    try:
        c = client()
        if c:
            c.table("class_profiles").delete().eq("chat_id", str(chat_id)).execute()
    except Exception as e:
        print(f"[delete_all_class_profiles] {e}", flush=True)
