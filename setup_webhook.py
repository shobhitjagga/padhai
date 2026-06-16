"""Run once after deploying to set the Telegram webhook.
Usage: python setup_webhook.py https://your-app.railway.app
"""
import sys
import httpx
import config

def set_webhook(base_url: str):
    url = f"{base_url.rstrip('/')}/telegram/webhook"
    resp = httpx.post(
        f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/setWebhook",
        json={"url": url},
    )
    print(resp.json())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python setup_webhook.py https://your-app.railway.app")
        sys.exit(1)
    set_webhook(sys.argv[1])
