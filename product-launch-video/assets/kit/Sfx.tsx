import React from "react";
import { Audio } from "@remotion/media";
import { Sequence, staticFile } from "remotion";

// One-shot sound effect placed at a frame. Keep SFX on the beat grid.
export const Sfx: React.FC<{ at: number; src: string; volume?: number; name?: string }> = ({ at, src, volume = 0.6, name }) => (
  <Sequence from={at} durationInFrames={90} name={name ?? `sfx ${src}`} layout="none">
    <Audio src={src.startsWith("http") ? src : staticFile(src)} volume={volume} />
  </Sequence>
);
