import { Easing, interpolate } from "remotion";

// Shared easing + clamped keyframe helper used by the kit components.
export const easeInOut = Easing.bezier(0.65, 0, 0.35, 1);
export const easeOut = Easing.bezier(0.2, 0, 0, 1);

// k(frame, [f0, f1, ...], [v0, v1, ...], easing?) → clamped interpolation between keyframes.
// A single keyframe just holds its value (interpolate() needs at least two points).
export const k = (
  frame: number,
  input: number[],
  output: number[],
  easing?: (t: number) => number,
): number => {
  if (input.length < 2) return output[0] ?? 0;
  return interpolate(frame, input, output, {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing,
  });
};
