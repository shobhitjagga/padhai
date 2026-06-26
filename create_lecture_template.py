"""
One-time script: creates the generic 1/2/3 lecture-selection WhatsApp template
via Twilio Content API and prints the SID to add to .env.

Run once from the shikshabot/ directory:
    python3 create_lecture_template.py

Then add to .env:
    TWILIO_LECTURE_SELECT_SID=<printed SID>
"""
import json, sys
import httpx
import config

CONTENT_API = "https://content.twilio.com/v1/Content"

template = {
    "friendly_name": "lecture_select",
    "language": "en",
    "variables": {"1": "Sound (Class 9) spans 3 lessons.\n\n1. Production & Propagation\n2. Echo & Reverberation\n3. Ultrasound & Human Ear"},
    "types": {
        "twilio/quick-reply": {
            "body": "{{1}}",
            "actions": [
                {"title": "1", "id": "1"},
                {"title": "2", "id": "2"},
                {"title": "3", "id": "3"},
            ],
        }
    },
}

print("Creating template via Twilio Content API...")
r = httpx.post(
    CONTENT_API,
    auth=(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN),
    json=template,
    timeout=15.0,
)

if r.status_code not in (200, 201):
    print(f"ERROR {r.status_code}: {r.text}")
    sys.exit(1)

data = r.json()
sid = data["sid"]
print(f"\n✅ Template created: {sid}")
print(f"\nAdd to .env:\n  TWILIO_LECTURE_SELECT_SID={sid}")

# Submit for WhatsApp approval (needed for production; sandbox doesn't require it)
print("\nSubmitting for WhatsApp approval...")
approval_url = f"{CONTENT_API}/{sid}/ApprovalRequests"
ar = httpx.post(
    approval_url,
    auth=(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN),
    json={"name": "lecture_select", "category": "UTILITY"},
    timeout=15.0,
)
if ar.status_code in (200, 201):
    print(f"Approval request submitted. Status: {ar.json().get('status', 'pending')}")
    print("Approval is usually instant for utility templates in sandbox.")
else:
    print(f"Approval request failed ({ar.status_code}) — sandbox usage still works without it.")
