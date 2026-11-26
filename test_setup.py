import os
import requests

gemini_key = os.environ["GEMINI_API_KEY"]
bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]
model = os.environ.get("GEMINI_MODEL", "gemini-flash-latest")
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
r = requests.post(
    url,
    headers={"x-goog-api-key": gemini_key},
    json={"contents": [{"parts": [{"text": "Write one short Hindi sentence for kids about sharing."}]}]},
    timeout=60,
)
print("Gemini status:", r.status_code)
if r.status_code == 200:
    text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    print("Gemini says:", text)
else:
    print(r.text[:500])
    m = requests.get(
        "https://generativelanguage.googleapis.com/v1beta/models",
        headers={"x-goog-api-key": gemini_key},
        timeout=60,
    )
    print("Available models:", [x["name"] for x in m.json().get("models", [])][:30])
    text = "Gemini failed, see logs"

t = requests.post(
    f"https://api.telegram.org/bot{bot_token}/sendMessage",
    data={"chat_id": chat_id, "text": f"Setup test OK.\n{text}"},
    timeout=60,
)
print("Telegram status:", t.status_code, t.text[:200])