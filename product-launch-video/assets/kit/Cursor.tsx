import React from "react";
import { useCurrentFrame } from "remotion";
import { easeInOut, k } from "./anim";

export type CursorKey = { f: number; x: number; y: number };

// Cursor that always travels on eased paths between keyframes (never teleports).
// `clicks` are frames where a ripple + press happens.
export const Cursor: React.FC<{ keys: CursorKey[]; clicks?: number[]; appearAt?: number }> = ({
  keys,
  clicks = [],
  appearAt = 0,
}) => {
  const frame = useCurrentFrame();
  const fs = keys.map((p) => p.f);
  const x = k(frame, fs, keys.map((p) => p.x), easeInOut);
  const y = k(frame, fs, keys.map((p) => p.y), easeInOut);
  const opacity = k(frame, [appearAt, appearAt + 6], [0, 1]);
  const pressing = clicks.some((c) => frame >= c && frame < c + 5);

  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: "100%", height: "100%", pointerEvents: "none" }}>
      {clicks.map((c) => {
        const p = frame - c;
        if (p < 0 || p > 18) return null;
        const cx = k(c, fs, keys.map((q) => q.x), easeInOut);
        const cy = k(c, fs, keys.map((q) => q.y), easeInOut);
        const size = k(p, [0, 18], [10, 90]);
        return (
          <div
            key={c}
            style={{
              position: "absolute",
              left: cx - size / 2,
              top: cy - size / 2,
              width: size,
              height: size,
              borderRadius: "50%",
              border: "4px solid currentColor",
              opacity: k(p, [0, 18], [0.8, 0]),
            }}
          />
        );
      })}
      <svg
        width={44}
        height={52}
        viewBox="0 0 22 26"
        style={{ position: "absolute", left: x - 3, top: y - 2, opacity, scale: pressing ? "0.85" : "1", transformOrigin: "3px 2px", filter: "drop-shadow(0 4px 6px rgba(0,0,0,0.25))" }}
      >
        <path d="M2 2 L2 21 L7 16.5 L10.5 24 L14 22.5 L10.5 15 L17 15 Z" fill="#14161a" stroke="#ffffff" strokeWidth={1.6} strokeLinejoin="round" />
      </svg>
    </div>
  );
};
