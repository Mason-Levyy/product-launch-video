import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// Use these inside <TransitionSeries.Overlay durationInFrames={N}> — they cover the cut at their midpoint,
// so the scene change is hidden behind brand graphics instead of a generic fade.

// A giant marker stroke sweeps across the frame (brand-native "highlighter" wipe).
export const MarkerWipe: React.FC<{ color: string; angle?: number }> = ({ color, angle = -8 }) => {
  const frame = useCurrentFrame();
  const { durationInFrames, width } = useVideoConfig();
  const x = interpolate(frame, [0, durationInFrames - 1], [-1.6 * width, 1.6 * width], { ...clamp, easing: Easing.bezier(0.7, 0, 0.3, 1) });
  return (
    <AbsoluteFill style={{ pointerEvents: "none", overflow: "hidden" }}>
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "-40%",
          width: width * 1.5,
          height: "180%",
          marginLeft: -width * 0.75,
          background: color,
          borderRadius: 60,
          rotate: `${angle}deg`,
          translate: `${x}px 0px`,
          boxShadow: `0 0 0 24px ${color}55`,
        }}
      />
    </AbsoluteFill>
  );
};

// Camera-shutter blades close to black, then open. Pairs with a shutter/impact sound.
export const ShutterCut: React.FC<{ color?: string; flash?: string }> = ({ color = "#111", flash = "#fff" }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const mid = (durationInFrames - 1) / 2;
  const close = interpolate(frame, [0, mid, durationInFrames - 1], [0, 1, 0], { ...clamp, easing: Easing.bezier(0.65, 0, 0.35, 1) });
  const flashOpacity = interpolate(frame, [mid, mid + 2, mid + 6], [0, 0.9, 0], clamp);
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: `${close * 50.5}%`, background: color }} />
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: `${close * 50.5}%`, background: color }} />
      <AbsoluteFill style={{ background: flash, opacity: flashOpacity }} />
    </AbsoluteFill>
  );
};

// A sticky note slaps over the whole frame, then peels away up-right.
export const StickySlap: React.FC<{ color: string; label?: string; labelColor?: string; font?: string }> = ({ color, label, labelColor = "#14161a", font }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const mid = (durationInFrames - 1) / 2;
  // slaps up from below-left with a spin, lands at the cut, then peels off up-right
  const enter = interpolate(frame, [0, mid], [1, 0], { ...clamp, easing: Easing.bezier(0.2, 0, 0, 1) });
  const scale = 1 + enter * 0.15;
  const inOpacity = 1;
  const peel = interpolate(frame, [mid + 1, durationInFrames - 1], [0, 1], { ...clamp, easing: Easing.bezier(0.6, 0, 1, 1) });
  return (
    <AbsoluteFill style={{ pointerEvents: "none", overflow: "hidden" }}>
      <div
        style={{
          position: "absolute",
          inset: "-10%",
          background: color,
          opacity: inOpacity,
          scale: `${scale}`,
          rotate: `${-4 - enter * 20 + peel * 18}deg`,
          translate: `${-enter * 60 + peel * 120}% ${enter * 120 - peel * 120}%`,
          boxShadow: "0 40px 80px rgba(0,0,0,0.25)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {label ? <div style={{ fontFamily: font, fontSize: 160, fontWeight: 900, color: labelColor, rotate: "-3deg" }}>{label}</div> : null}
      </div>
    </AbsoluteFill>
  );
};
