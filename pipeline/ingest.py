"""Manual mode: read the JSON you pasted from the Claude chat (content/today.json),
check it, build captions, and prepare out/<date>/content.json for rendering."""
import os, datetime as dt
from common import RASHIS, LORDS, notify, save, load
from generate import validate, make_caption, WEEKDAYS, VAAR_LORD, HINDI_MONTHS

def main():
    raw = load("content/today.json")
    date = raw["date"]
    d = dt.date.fromisoformat(date)
    p = raw["panchang"]
    p["vaar"], p["vaar_lord"] = WEEKDAYS[d.weekday()], VAAR_LORD[d.weekday()]
    for k in ("tithi", "tithi_end", "paksha", "nakshatra", "nakshatra_end"):
        if not p.get(k): raise RuntimeError(f"Panchang field missing: {k}")
    items = raw["rashis"]
    errs = validate(items)
    if errs: raise RuntimeError("content/today.json problems:\n- " + "\n- ".join(errs))
    date_str = f"{d.day} {HINDI_MONTHS[d.month-1]} {d.year}"
    for i, it in enumerate(items):
        it["name"], it["lord"] = RASHIS[i], LORDS[i]
        it["caption"] = make_caption(i, it, date_str, p)
    save(f"out/{date}/content.json", {"date": date, "date_str": date_str, "panchang": p, "rashis": items})
    if os.getenv("GITHUB_ENV"):
        with open(os.environ["GITHUB_ENV"], "a") as f: f.write(f"RDATE={date}\n")
    print("Ready:", date)

if __name__ == "__main__":
    try: main()
    except Exception as e:
        notify(f"❌ Could not read today's rashifal file: {e}")
        raise
