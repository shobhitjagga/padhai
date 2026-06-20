import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN           = os.getenv("TELEGRAM_TOKEN", "")
GROQ_API_KEY             = os.getenv("GROQ_API_KEY", "")
SUPABASE_URL             = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY             = os.getenv("SUPABASE_KEY", "")
OPENAI_API_KEY           = os.getenv("OPENAI_API_KEY", "")
TWILIO_ACCOUNT_SID       = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN        = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WA_NUMBER         = os.getenv("TWILIO_WA_NUMBER", "")
TWILIO_LANG_TEMPLATE_SID      = os.getenv("TWILIO_LANG_TEMPLATE_SID", "")
TWILIO_FEEDBACK_Q1_SID        = os.getenv("TWILIO_FEEDBACK_Q1_SID", "")
TWILIO_FEEDBACK_Q2_SID        = os.getenv("TWILIO_FEEDBACK_Q2_SID", "")
TWILIO_FEEDBACK_Q3_SID        = os.getenv("TWILIO_FEEDBACK_Q3_SID", "")
