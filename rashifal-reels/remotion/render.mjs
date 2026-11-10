import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";
import fs from "fs";
import path from "path";

const date = process.argv[2];
if (!date) throw new Error("Usage: node render.mjs YYYY-MM-DD");
const content = JSON.parse(fs.readFileSync(`../out/${date}/content.json`, "utf-8"));

const musicDir = "public/music";
const tracks = fs.existsSync(musicDir)
  ? fs.readdirSync(musicDir).filter((f) => /\.(mp3|m4a|wav)$/i.test(f)).sort() : [];
if (!tracks.length) console.warn("WARNING: no music in public/music, reels will be silent.");
const dayNum = Math.floor(new Date(date).getTime() / 86400000);

const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });

for (const r of content.rashis) {
  const inputProps = {
    index: r.index, name: r.name, lord: r.lord, dateStr: content.date_str, rating: r.rating,
    khaas: r.khaas, work: r.work, money: r.money, family: r.family, health: r.health,
    color: r.color, number: String(r.number), time: r.time, upay: r.upay,
    track: tracks.length ? tracks[(dayNum + r.index) % tracks.length] : "",
  };
  const composition = await selectComposition({ serveUrl, id: "Reel", inputProps });
  await renderMedia({
    composition, serveUrl, codec: "h264", audioCodec: "aac", inputProps,
    outputLocation: `../out/${date}/reel_${r.index}.mp4`,
  });
  console.log("Rendered", r.name);
}
