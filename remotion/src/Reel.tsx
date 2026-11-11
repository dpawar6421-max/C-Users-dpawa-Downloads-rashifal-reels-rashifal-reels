import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, interpolate, useCurrentFrame } from "remotion";
import { loadFont as loadBody } from "@remotion/google-fonts/Mukta";
import { loadFont as loadDisplay } from "@remotion/google-fonts/TiroDevanagariHindi";

const body = loadBody("normal", { weights: ["500", "700", "800"], subsets: ["devanagari", "latin"] }).fontFamily;
const display = loadDisplay("normal", { weights: ["400"], subsets: ["devanagari", "latin"] }).fontFamily;

export type ReelProps = {
  index: number; name: string; lord: string; dateStr: string; rating: number;
  khaas: string; work: string; money: string; family: string; health: string;
  color: string; number: string; time: string; upay: string; track: string;
};

const GLYPHS = ["♈︎","♉︎","♊︎","♋︎","♌︎","♍︎","♎︎","♏︎","♐︎","♑︎","♒︎","♓︎"];
const SEC = 30; // fps

// One accent hue per rashi on a deep night background; marigold stays constant for stars.
const accent = (i: number) => `hsl(${(i - 1) * 30 + 10}, 80%, 66%)`;
const night = (i: number) => `hsl(${(i - 1) * 30 + 230}, 45%, 11%)`;
const MARIGOLD = "#F6B73C";
const CREAM = "#FFF4E0";

const Scene: React.FC<{ children: React.ReactNode; frames: number }> = ({ children, frames }) => {
  const f = useCurrentFrame();
  const opacity = interpolate(f, [0, 8, frames - 8, frames], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity, padding: "0 90px", justifyContent: "center", fontFamily: body, color: CREAM }}>
      {children}
    </AbsoluteFill>
  );
};

const Stars: React.FC<{ n: number; size?: number }> = ({ n, size = 90 }) => {
  const f = useCurrentFrame();
  return (
    <div style={{ display: "flex", gap: 14 }}>
      {[1, 2, 3, 4, 5].map((s) => {
        const on = s <= n;
        const pop = interpolate(f, [s * 5, s * 5 + 8], [0.4, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        return <span key={s} style={{ fontSize: size, lineHeight: 1, color: on ? MARIGOLD : "rgba(255,244,224,0.2)", transform: `scale(${pop})` }}>★</span>;
      })}
    </div>
  );
};

const Row: React.FC<{ icon: string; label: string; text: string; hue: string }> = ({ icon, label, text, hue }) => (
  <div style={{ marginBottom: 90 }}>
    <div style={{ fontSize: 46, fontWeight: 700, color: hue }}>{icon} {label}</div>
    <div style={{ fontSize: 74, fontWeight: 800, lineHeight: 1.25, marginTop: 14 }}>{text}</div>
  </div>
);

export const Reel: React.FC<ReelProps> = (p) => {
  const f = useCurrentFrame();
  const hue = accent(p.index);
  const glyphDrift = interpolate(f, [0, 540], [0, -60]);
  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 20%, ${night(p.index)} 0%, #0B0D1F 75%)` }}>
      {p.track ? (
        <Audio src={staticFile(`music/${p.track}`)}
          volume={(fr) => interpolate(fr, [0, 30, 510, 540], [0, 0.6, 0.6, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })} />
      ) : null}

      {/* the one memorable element: a huge zodiac glyph that slowly rises behind everything */}
      <div style={{ position: "absolute", top: 330 + glyphDrift, left: 0, right: 0, textAlign: "center",
        fontSize: 1100, lineHeight: 1, color: hue, opacity: 0.1, fontFamily: "sans-serif" }}>{GLYPHS[p.index - 1]}</div>

      {/* 0-2s */}
      <Sequence from={0} durationInFrames={2 * SEC}>
        <Scene frames={2 * SEC}>
          <div style={{ textAlign: "center" }}>
            <div style={{ fontSize: 220, color: hue, fontFamily: "sans-serif" }}>{GLYPHS[p.index - 1]}</div>
            <div style={{ fontFamily: display, fontSize: 210, lineHeight: 1.2 }}>{p.name}</div>
            <div style={{ fontSize: 64, fontWeight: 700, marginTop: 30 }}>राशिफल · {p.dateStr}</div>
            <div style={{ fontSize: 52, marginTop: 14, color: hue }}>स्वामी ग्रह: {p.lord}</div>
          </div>
        </Scene>
      </Sequence>

      {/* 2-5s */}
      <Sequence from={2 * SEC} durationInFrames={3 * SEC}>
        <Scene frames={3 * SEC}>
          <div style={{ fontSize: 50, fontWeight: 700, color: hue, marginBottom: 26 }}>आज की ख़ास बात</div>
          <div style={{ fontSize: 80, fontWeight: 800, lineHeight: 1.3, marginBottom: 70 }}>{p.khaas}</div>
          <Stars n={p.rating} />
        </Scene>
      </Sequence>

      {/* 5-9s */}
      <Sequence from={5 * SEC} durationInFrames={4 * SEC}>
        <Scene frames={4 * SEC}>
          <Row icon="💼" label="नौकरी और काम" text={p.work} hue={hue} />
          <Row icon="💰" label="पैसा" text={p.money} hue={hue} />
        </Scene>
      </Sequence>

      {/* 9-13s */}
      <Sequence from={9 * SEC} durationInFrames={4 * SEC}>
        <Scene frames={4 * SEC}>
          <Row icon="❤️" label="परिवार और रिश्ते" text={p.family} hue={hue} />
          <Row icon="🧘" label="सेहत" text={p.health} hue={hue} />
        </Scene>
      </Sequence>

      {/* 13-16s */}
      <Sequence from={13 * SEC} durationInFrames={3 * SEC}>
        <Scene frames={3 * SEC}>
          <div style={{ fontSize: 50, fontWeight: 700, color: hue, marginBottom: 30 }}>🍀 आज के शुभ संकेत</div>
          <div style={{ fontSize: 72, fontWeight: 800, lineHeight: 1.35 }}>
            रंग: {p.color}<br />अंक: {p.number}<br />समय: {p.time}
          </div>
          <div style={{ fontSize: 50, fontWeight: 700, color: hue, margin: "50px 0 14px" }}>🙏 आसान उपाय</div>
          <div style={{ fontSize: 60, fontWeight: 700, lineHeight: 1.3 }}>{p.upay}</div>
        </Scene>
      </Sequence>

      {/* 16-18s */}
      <Sequence from={16 * SEC} durationInFrames={2 * SEC}>
        <Scene frames={2 * SEC}>
          <div style={{ textAlign: "center" }}>
            <div style={{ fontFamily: display, fontSize: 110, lineHeight: 1.3 }}>रोज़ का राशिफल<br />फ़ॉलो करें</div>
            <div style={{ fontSize: 34, marginTop: 120, opacity: 0.7, lineHeight: 1.5 }}>
              सामान्य मार्गदर्शन है, व्यक्तिगत कुंडली का फल अलग हो सकता है।<br />पूरा राशिफल कैप्शन में पढ़ें।
            </div>
          </div>
        </Scene>
      </Sequence>
    </AbsoluteFill>
  );
};
