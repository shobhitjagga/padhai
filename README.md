# PadhAI — AI Teaching Assistant for NCERT Classrooms

PadhAI (PadhaiBot) is a WhatsApp and Telegram chatbot that helps government school teachers in India prepare SEL-integrated NCERT lesson plans, answer curriculum questions, and get student support strategies — in Hindi, English.

## Features

- **Lesson plan generation** — NCERT-aligned plans with embedded SEL (Social-Emotional Learning) activities
- **Curriculum Q&A** — answers to subject questions grounded in NCERT content
- **Student support** — strategies for classroom challenges (low participation, conflict, etc.)
- **Feedback collection** — scheduled follow-up questions after lesson delivery
- **Voice note support** — WhatsApp audio messages transcribed via Groq Whisper
- **Multilingual** — Hindi, English (user selects on onboarding)

## Architecture

```
main.py          FastAPI app — Telegram webhook + Twilio WhatsApp endpoint
handlers.py      Intent routing, onboarding, feedback state machine
ai.py            LLM calls (Groq / OpenAI) — lesson gen, intent classification, Q&A
ncert_data.py    NCERT curriculum data by subject/grade
db.py            Supabase client — users, messages, feedback_jobs, content_evals
config.py        Env var loading
schema.sql       Supabase table definitions
eval/            Offline evaluation scripts (intent classifier, content quality)
```

## Setup

### Prerequisites

- Python 3.11+
- A [Supabase](https://supabase.com) project
- A [Groq](https://console.groq.com) API key (LLM + Whisper transcription)
- An [OpenAI](https://platform.openai.com) API key (used as fallback / judge)
- A Telegram bot token (from [@BotFather](https://t.me/BotFather))
- A Twilio account with WhatsApp sandbox enabled (optional — for WhatsApp channel)

### 1. Clone and install

```bash
git clone <repo-url>
cd shikshabot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and fill in all values:

| Variable | Description |
|---|---|
| `TELEGRAM_TOKEN` | Bot token from BotFather |
| `GROQ_API_KEY` | Groq API key (LLM + Whisper) |
| `OPENAI_API_KEY` | OpenAI API key |
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_KEY` | Supabase anon/service key |
| `TWILIO_ACCOUNT_SID` | Twilio Account SID (WhatsApp only) |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token (WhatsApp only) |
| `TWILIO_WA_NUMBER` | Your Twilio WhatsApp number (e.g. `+91xxxxxxxxxx`) |
| `TWILIO_LANG_TEMPLATE_SID` | Content Template SID for language selection buttons |
| `TWILIO_FEEDBACK_Q1_SID` | Content Template SID for feedback question 1 |
| `TWILIO_FEEDBACK_Q2_SID` | Content Template SID for feedback question 2 |
| `TWILIO_FEEDBACK_Q3_SID` | Content Template SID for feedback question 3 |

### 3. Set up the database

Run `schema.sql` in your Supabase SQL Editor (Dashboard → SQL Editor → New query):

```bash
# Or paste the contents of schema.sql directly into the Supabase SQL Editor
```

This creates five tables: `users`, `messages`, `ai_calls`, `content_evals`, `feedback_jobs`.

### 4. Run locally

```bash
uvicorn main:app --reload --port 8000
```

Check the server is up: `http://localhost:8000/health`

To verify all credentials are loaded: `http://localhost:8000/config-check`

### 5. Expose locally for webhook testing

Use [ngrok](https://ngrok.com) or similar:

```bash
ngrok http 8000
```

### 6. Register webhooks

**Telegram:**

```bash
python setup_webhook.py
# or manually:
curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://<your-ngrok-url>/telegram/webhook"
```

**Twilio WhatsApp:**

In the Twilio Console → Messaging → Sandbox settings, set the webhook URL to:
```
https://<your-domain>/twilio/whatsapp
```

## Deployment

The app is configured for [Railway](https://railway.app) via `Procfile`:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Set all environment variables in your hosting platform's dashboard (equivalent to `.env` values).

## Evaluation

The `eval/` directory contains offline evaluation scripts:

```bash
# Run intent classification eval
python eval/run_intent_eval.py

# Run content generation eval
python eval/run_content_eval.py

# Compare content models
python eval/compare_content_models.py
```

Datasets and checkpoint results are stored under `eval/checkpoints/`.
