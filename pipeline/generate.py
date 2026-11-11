"""Step 1: panchang (checked from two searches) -> Step 2: 12 rashis as JSON."""
import os, re, sys, json, datetime as dt
from common import RASHIS, LORDS, DISCLAIMER, notify, save, load

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")
_client = None
def get_client():
    global _client
    if _client is None:
        import anthropic
        _client = anthropic.Anthropic()
    return _client
WEEKDAYS = ["सोमवार","मंगलवार","बुधवार","गुरुवार","शुक्रवार","शनिवार","रविवार"]
VAAR_LORD = ["चंद्र","मंगल","बुध","गुरु","शुक्र","शनि","सूर्य"]
HINDI_MONTHS = ["जनवरी","फ़रवरी","मार्च","अप्रैल","मई","जून","जुलाई","अगस्त","सितंबर","अक्टूबर","नवंबर","दिसंबर"]

def ask(system, user, max_tokens=16000, search=False):
    tools = [{"type": "web_search_20250305", "name": "web_search", "max_uses": 8}] if search else []
    messages = [{"role": "user", "content": user}]
    for _ in range(6):
        kwargs = dict(model=MODEL, max_tokens=max_tokens, system=system, messages=messages)
        if tools: kwargs["tools"] = tools
        with get_client().messages.stream(**kwargs) as s:
            r = s.get_final_message()
        if r.stop_reason == "pause_turn":
            messages = [messages[0], {"role": "assistant", "content": r.content}]
            continue
        return "".join(b.text for b in r.content if b.type == "text")
    raise RuntimeError("Model did not finish")

def parse_json(text):
    m = re.search(r"[\[{].*[\]}]", text, re.S)
    if not m:
        raise ValueError("No JSON in reply")
    return json.loads(m.group(0))

# ---------- STEP 1: panchang ----------
PANCHANG_SYS = "You are a careful Vedic panchang researcher. Use web search. Never guess or invent times. Reply with JSON only."

def panchang_prompt(date, avoid_hint):
    return f"""Find the Hindu panchang for {date} for New Delhi (IST). {avoid_hint}
Return ONLY this JSON (Hindi/Devanagari strings; times like "रात 09:15 तक"):
{{"tithi":"","tithi_end":"","paksha":"","nakshatra":"","nakshatra_end":"",
"moon_sign_number":1,"moon_sign_change_time":null,"next_moon_sign_number":null,
"yoga":"","karana":"","rahu_kaal":"","abhijit":"","varjya":"","special":"festival/vrat/Panchak/Bhadra/eclipse or empty",
"sources":["url1"]}}
moon_sign_number: 1=Mesha ... 12=Meen (Vedic/sidereal chandra rashi at sunrise). If the Moon changes sign that day, fill moon_sign_change_time and next_moon_sign_number.
If you cannot find reliable data return {{"error":"reason"}}."""

def get_panchang(date):
    a = parse_json(ask(PANCHANG_SYS, panchang_prompt(date, "Prefer drikpanchang.org."), 4000, True))
    b = parse_json(ask(PANCHANG_SYS, panchang_prompt(date, "Use a DIFFERENT website than drikpanchang.org (for example prokerala.com)."), 4000, True))
    if "error" in a or "error" in b:
        raise RuntimeError(f"Panchang not found: {a.get('error')} / {b.get('error')}")
    for k in ("tithi", "nakshatra", "moon_sign_number"):
        if str(a.get(k)).strip() != str(b.get(k)).strip():
            raise RuntimeError(f"Panchang mismatch on '{k}': {a.get(k)} vs {b.get(k)}. Not posting.")
    return a

# ---------- STEP 2: rashifal ----------
def houses(moon_no):
    return [((moon_no - i) % 12) + 1 for i in range(1, 13)]

RASHI_SYS = """You are an experienced Indian Vedic astrologer and Hindi writer for an Instagram channel. Very simple, warm Hindi (Devanagari), short sentences, address reader as "आप". Everyday words; English words like boss, phone, meeting are fine.
RULES: no fear, no doom, no guaranteed results in money/health/marriage/exams/court; no medical/legal/investment advice; remedies free or very low cost (a mantra, water for a plant, feeding birds, etc.); respect all religions; original text. Make every rashi clearly different (different tips, examples, remedies, colours, numbers, directions). Give honest variety in ratings (not all 4-5; use 2 and 3 too on tense days). Rotate practical tips across money, communication, time management, anger control, study habits, routine and relationships.
Moon house meanings: 1 self,health,mood | 2 money,speech,family | 3 effort,courage,communication | 4 home,mother,peace of mind | 5 intellect,children,creativity,romance | 6 work pressure,competition,health,debts | 7 spouse,partnership | 8 sudden changes,caution | 9 luck,elders,travel,learning | 10 career,status | 11 gains,friends | 12 expenses,rest,sleep.
Reply with JSON only."""

def rashi_prompt(date_str, p, history):
    moon = int(p["moon_sign_number"])
    h = houses(moon)
    h2 = houses(int(p["next_moon_sign_number"])) if p.get("next_moon_sign_number") else None
    rows = "\n".join(
        f"{i+1}. {RASHIS[i]} (स्वामी {LORDS[i]}): Moon house {h[i]}" + (f", after Moon sign change: house {h2[i]}" if h2 else "")
        for i in range(12))
    return f"""Date: {date_str}. Panchang: {json.dumps(p, ensure_ascii=False)}
Vaar lord: {p['vaar_lord']}.
Computed Moon houses (use exactly these):
{rows}

Recent days' lines (do NOT repeat any of these tips, remedies or sentences):
{json.dumps(history, ensure_ascii=False)[:3000]}

Return ONLY a JSON array of 12 objects in rashi order, each with keys:
"index" (1-12), "rating" (integer 1-5),
"khaas" (on-screen line linking Moon house/nakshatra/vaar to this rashi, MAX 9 words),
"work","money","family","health" (on-screen, each MAX 8 words, a clear message + tiny tip),
"color","number" (string),"direction","time" (lucky; vary across rashis),
"upay" (one easy remedy, MAX 9 words),
"detail": full caption text, 700-1000 characters, with these labelled parts in simple Hindi:
 आज की ख़ास बात; 🌟 पूरे दिन का हाल (with stars); 💼 नौकरी और काम; 💰 पैसा; ❤️ परिवार और रिश्ते; 🧘 सेहत; 📚 विद्यार्थियों के लिए;
 each with "क्या हो सकता है" and "आप क्या करें"; then 🍀 शुभ संकेत (रंग, अंक, दिशा, समय, सावधानी); 🙏 आसान उपाय (2-3); ✨ आज की सीख (one line)."""

def validate(items):
    if not isinstance(items, list) or len(items) != 12:
        return ["Need an array of exactly 12 items"]
    errs = []
    limits = {"khaas": 9, "work": 8, "money": 8, "family": 8, "health": 8, "upay": 9}
    for i, it in enumerate(items):
        r = RASHIS[i]
        if int(it.get("index", 0)) != i + 1: errs.append(f"{r}: wrong index")
        if not (1 <= int(it.get("rating", 0)) <= 5): errs.append(f"{r}: rating must be 1-5")
        for k, n in limits.items():
            if not it.get(k) or len(str(it[k]).split()) > n:
                errs.append(f"{r}: '{k}' empty or longer than {n} words")
        for k in ("color", "number", "direction", "time", "detail"):
            if not it.get(k): errs.append(f"{r}: missing {k}")
        if len(str(it.get("detail", ""))) > 1200: errs.append(f"{r}: detail too long")
    if len({int(x.get("rating", 0)) for x in items}) < 3: errs.append("Ratings need more variety (at least 3 different values)")
    if len({x.get("upay") for x in items}) < 12: errs.append("Remedies must all be different")
    return errs

def make_caption(i, it, date_str, p):
    tags = f"#राशिफल #आजकाराशिफल #{RASHIS[i]}राशि #Rashifal #Horoscope #DailyHoroscope #Astrology #Panchang"
    head = f"{RASHIS[i]} राशि | {date_str} | स्वामी: {LORDS[i]}"
    pan = (f"📅 आज: {p['vaar']}, {p['paksha']} {p['tithi']} ({p['tithi_end']}), "
           f"नक्षत्र {p['nakshatra']} ({p['nakshatra_end']})\n(समय शहर के अनुसार बदलते हैं)")
    return f"{head}\n\n{it['detail']}\n\n{pan}\n\n{DISCLAIMER}\n\n{tags}"[:2200]

def main():
    ist = dt.timezone(dt.timedelta(hours=5, minutes=30))
    date = sys.argv[1] if len(sys.argv) > 1 else dt.datetime.now(ist).strftime("%Y-%m-%d")
    d = dt.date.fromisoformat(date)
    date_str = f"{d.day} {HINDI_MONTHS[d.month-1]} {d.year}"

    p = get_panchang(date)
    p["vaar"], p["vaar_lord"] = WEEKDAYS[d.weekday()], VAAR_LORD[d.weekday()]

    history = load("history/last.json") if os.path.exists("history/last.json") else []
    prompt = rashi_prompt(date_str, p, history)
    for attempt in range(3):
        items = parse_json(ask(RASHI_SYS, prompt))
        errs = validate(items)
        if not errs: break
        prompt += "\n\nFix these problems and return the full JSON array again:\n- " + "\n- ".join(errs)
    else:
        raise RuntimeError("Rashifal validation failed:\n" + "\n".join(errs))

    for i, it in enumerate(items):
        it["name"], it["lord"] = RASHIS[i], LORDS[i]
        it["caption"] = make_caption(i, it, date_str, p)
    save(f"out/{date}/content.json", {"date": date, "date_str": date_str, "panchang": p, "rashis": items})
    save("history/last.json", [{k: x[k] for k in ("work", "money", "family", "health", "upay")} for x in items])
    print("Saved content for", date)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        notify(f"❌ Rashifal generation failed: {e}")
        raise
