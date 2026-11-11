import { Composition } from "remotion";
import { Reel, ReelProps } from "./Reel";

const sample: ReelProps = {
  index: 1, name: "मेष", lord: "मंगल", dateStr: "9 नवंबर 2026", rating: 4,
  khaas: "चंद्र आपके पाँचवें भाव में, मन हल्का रहेगा",
  work: "नया आइडिया बॉस को बताएँ", money: "छोटा ख़र्च टालें",
  family: "शाम को सबके साथ बैठें", health: "पानी ज़्यादा पिएँ",
  color: "केसरिया", number: "5", time: "सुबह 10 बजे", upay: "हनुमान जी को लाल फूल चढ़ाएँ",
  track: "",
};

export const Root = () => (
  <Composition id="Reel" component={Reel} durationInFrames={540} fps={30}
    width={1080} height={1920} defaultProps={sample} />
);
