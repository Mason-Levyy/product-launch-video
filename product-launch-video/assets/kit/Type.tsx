import React from "react";
import { Easing, interpolate, useCurrentFrame } from "remotion";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// A word/line that slams in on a beat: overshoot scale + tiny rotation, settles in ~8 frames.
export const Slam: React.FC<{ at: number; children: React.ReactNode; style?: React.CSSProperties; from?: number; rotate?: number }> = ({
  at,
  children,
  style,
  from = 1.8,
  rotate = -3,
}) => {
  const frame = useCurrentFrame();
  return (
    <div
      style={{
        opacity: interpolate(frame, [at, at + 1], [0, 1], clamp),
        scale: `${interpolate(frame, [at, at + 8], [from, 1], { ...clamp, easing: Easing.bezier(0.2, 0, 0, 1) })}`,
        rotate: `${interpolate(frame, [at, at + 8], [rotate, 0], { ...clamp, easing: Easing.bezier(0.2, 0, 0, 1) })}deg`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};

// A rubber-stamp label that lands with a small shake.
export const Stamp: React.FC<{ at: number; children: React.ReactNode; style?: React.CSSProperties }> = ({ at, children, style }) => {
  const frame = useCurrentFrame();
  const shake = frame >= at && frame < at + 6 ? Math.sin((frame - at) * 2.6) * 6 * (1 - (frame - at) / 6) : 0;
  return (
    <div
      style={{
        opacity: interpolate(frame, [at, at + 1], [0, 1], clamp),
        scale: `${interpolate(frame, [at, at + 6], [1.5, 1], { ...clamp, easing: Easing.bezier(0.2, 0, 0, 1) })}`,
        translate: `${shake}px 0px`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};

// Hand-drawn curved arrow that draws itself, with a label at the tail.
export const Annotation: React.FC<{
  at: number;
  x: number;
  y: number;
  path: string; // SVG path in a 300x200 box, drawn from the label toward the target
  label: string;
  color: string;
  font?: string;
  labelStyle?: React.CSSProperties;
}> = ({ at, x, y, path, label, color, font, labelStyle }) => {
  const frame = useCurrentFrame();
  const draw = interpolate(frame, [at, at + 12], [1, 0], { ...clamp, easing: Easing.bezier(0.3, 0, 0.2, 1) });
  return (
    <div style={{ position: "absolute", left: x, top: y, pointerEvents: "none" }}>
      <div style={{ fontFamily: font, fontSize: 34, fontWeight: 600, color, whiteSpace: "nowrap", opacity: interpolate(frame, [at, at + 5], [0, 1], clamp), ...labelStyle }}>
        {label}
      </div>
      <svg width={300} height={200} style={{ overflow: "visible" }}>
        <path d={path} fill="none" stroke={color} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={draw} />
      </svg>
    </div>
  );
};

// Figma-style named cursor that travels between keyframes.
export const NamedCursor: React.FC<{
  name: string;
  color: string;
  keys: { f: number; x: number; y: number }[];
  appearAt: number;
  font?: string;
}> = ({ name, color, keys, appearAt, font }) => {
  const frame = useCurrentFrame();
  const fs = keys.map((k) => k.f);
  const ease = Easing.bezier(0.65, 0, 0.35, 1);
  const x = interpolate(frame, fs, keys.map((k) => k.x), { ...clamp, easing: ease });
  const y = interpolate(frame, fs, keys.map((k) => k.y), { ...clamp, easing: ease });
  return (
    <div style={{ position: "absolute", left: x, top: y, opacity: interpolate(frame, [appearAt, appearAt + 4], [0, 1], clamp), pointerEvents: "none", filter: "drop-shadow(0 6px 10px rgba(0,0,0,0.2))" }}>
      <svg width={36} height={40} viewBox="0 0 18 20">
        <path d="M1 1 L1 16 L5 12.5 L8 19 L10.5 18 L7.5 11.5 L13 11.5 Z" fill={color} stroke="#fff" strokeWidth={1.4} strokeLinejoin="round" />
      </svg>
      <div style={{ marginLeft: 26, marginTop: -8, background: color, color: "#fff", fontFamily: font, fontWeight: 700, fontSize: 24, padding: "6px 14px", borderRadius: 10, whiteSpace: "nowrap" }}>{name}</div>
    </div>
  );
};
