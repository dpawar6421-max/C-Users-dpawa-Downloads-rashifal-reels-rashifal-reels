import os, json, requests

RASHIS = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]
LORDS  = ["मंगल","शुक्र","बुध","चंद्र","सूर्य","बुध","शुक्र","मंगल","गुरु","शनि","शनि","गुरु"]
DISCLAIMER = ("यह राशि और पंचांग पर आधारित सामान्य मार्गदर्शन है, व्यक्तिगत कुंडली का फल अलग हो सकता है। "
              "महत्वपूर्ण निर्णय अपनी समझ और विशेषज्ञ की सलाह से लें।")

def notify(msg: str):
    """Telegram alert. Silently skipped if not configured."""
    tok, chat = os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")
    print(msg)
    if tok and chat:
        try:
            requests.post(f"https://api.telegram.org/bot{tok}/sendMessage",
                          data={"chat_id": chat, "text": msg[:3500]}, timeout=20)
        except Exception as e:
            print("telegram failed:", e)

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
