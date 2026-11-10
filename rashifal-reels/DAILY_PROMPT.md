# Message to send Claude every day

Use ONE chat for all days (so Claude remembers earlier days and does not repeat tips).
Turn web search ON. Change the date part only.

---
Date: 9 Nov 2026 (YYYY-MM-DD: 2026-11-09). Make today's Rashifal for all 12 rashis for my Instagram reels.

1. Search the panchang for New Delhi (IST) from TWO different websites. If tithi, nakshatra or Moon sign differ, tell me and do not write the rashis.
2. Work out each rashi's Moon house (house = Moon sign number minus rashi number, plus 1; count 12 back to 1) and use it, plus vaar lord, nakshatra and tithi, to write a DIFFERENT reading for every rashi. Honest ratings (use 2 and 3 on tense days). No fear, no guaranteed results, no medical/legal/investment advice, free remedies only, simple warm Hindi, nothing repeated from earlier days.
3. Reply with ONLY one JSON code block (no other text):

{"date":"YYYY-MM-DD",
 "panchang":{"tithi":"","tithi_end":"","paksha":"","nakshatra":"","nakshatra_end":"","moon_sign_number":1,"moon_sign_change_time":null,"next_moon_sign_number":null,"yoga":"","karana":"","rahu_kaal":"","abhijit":"","varjya":"","special":""},
 "rashis":[ 12 objects in order Mesha to Meen, each:
  {"index":1,"rating":3,
   "khaas":"max 9 words: Moon house/nakshatra/vaar link",
   "work":"max 8 words","money":"max 8 words","family":"max 8 words","health":"max 8 words",
   "color":"","number":"","direction":"","time":"",
   "upay":"one easy free remedy, max 9 words, different for every rashi",
   "detail":"700-1000 characters in Hindi: आज की ख़ास बात; 🌟 पूरे दिन का हाल (stars); 💼 नौकरी और काम; 💰 पैसा; ❤️ परिवार और रिश्ते; 🧘 सेहत; 📚 विद्यार्थियों के लिए (each with क्या हो सकता है + आप क्या करें); 🍀 शुभ संकेत; 🙏 आसान उपाय (2-3); ✨ आज की सीख"}
 ]}
---

# Then (about 1 minute)
1. Copy ONLY the JSON from the code block (use the copy button).
2. GitHub > your repository > `content` folder > `today.json` > pencil icon (Edit) > select all > paste > "Commit changes".
3. Done. The reels are made and posted automatically, one every 20 minutes. You get a Telegram message when finished.

If the JSON has a mistake, Telegram tells you what to fix. Ask Claude to correct it and paste again.
