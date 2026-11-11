# MODE USED: manual text, automatic video + posting
You message Claude daily (see DAILY_PROMPT.md), paste the JSON into content/today.json on GitHub, and the workflow
.github/workflows/manual.yml renders and posts the 12 reels. No Anthropic API key is needed.
(The fully automatic API version is kept in optional/daily_api.yml; copy it to .github/workflows/ to use it.)
Secrets needed: IG_USER_ID, IG_ACCESS_TOKEN, S3_BUCKET, S3_ENDPOINT, S3_KEY, S3_SECRET, PUBLIC_BASE_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID.
Test: Actions > Rashifal Reels > Run workflow with dry_run=1 (after putting a real day's JSON in content/today.json).

---
# Daily Rashifal Reels (fully automatic, music only, 18 sec each)

Every day at 5:00 AM IST, GitHub Actions will:
1. Ask Claude (with web search) for the Delhi panchang, twice from two different sources. If tithi, nakshatra or Moon sign do not match, it STOPS and sends you a Telegram alert (nothing is posted).
2. Ask Claude for all 12 rashis in your format (Moon house is computed by code, not guessed). Lengths, rating variety and repeated remedies are checked automatically.
3. Render 12 vertical 1080x1920 reels (18 s, music only) with Remotion.
4. Upload them to your storage and publish one reel every 20 minutes to Instagram (full reading + disclaimer + hashtags in the caption).

## One-time setup
1. Create a GitHub repo (public repos have free Actions minutes) and push this folder.
2. `cd remotion && npm install`, then commit the generated `package-lock.json`.
3. Put 10-15 royalty-free MP3s in `remotion/public/music/` (YouTube Audio Library, Pixabay Music). Keep a licence note. They rotate daily.
4. Instagram: Business or Creator account linked to a Facebook Page; create a Meta developer app with `instagram_content_publish`; get your IG user id and a long-lived access token.
5. Storage with public URLs (Cloudflare R2 is the cheapest; any S3 works). Instagram must be able to download the video from a public link.
6. Telegram: make a bot with @BotFather, get your chat id.
7. Add these repository secrets: ANTHROPIC_API_KEY, IG_USER_ID, IG_ACCESS_TOKEN, S3_BUCKET, S3_ENDPOINT, S3_KEY, S3_SECRET, PUBLIC_BASE_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID.

## Test first (important)
- Actions tab > "Daily Rashifal Reels" > Run workflow > enter a date and `dry_run` = 1. It renders and uploads but does NOT post. Download-check the MP4s.
- Preview the design locally: `cd remotion && npm run preview`.

## Maintenance
- Instagram tokens expire (about every 60 days). Refresh and update the secret; you will get a Telegram alert when posting fails.
- Posting time: the last reel goes out about 4 hours after the first (12 x 20 min). Change GAP_MINUTES in the workflow.
- To change the look, edit `remotion/src/Reel.tsx` (colours, fonts, timing).
