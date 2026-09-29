#!/usr/bin/env python3
"""
Generate an original, royalty-free launch-video soundtrack + SFX kit, plus a beat grid.

Everything is synthesized from scratch (numpy/scipy), so there are no licensing questions and
the tempo is exact: every beat lands on a known frame, which lets the video cut on the beat.

Usage (from the Remotion project root):
  python3 make_soundtrack.py --bpm 120 --fps 30 \
      --sections "intro:2,drop:7,break:3,drop:2,outro:1" \
      --key A --mode minor --out public/audio

Keys: C C# Db D D# Eb E F F# Gb G G# Ab A A# Bb B. Modes: minor, major.

Section types:
  intro  – ticking hats, filtered pad, riser + snare roll into the next section
  drop   – four-on-the-floor kick, claps, sidechained bass, pluck arp, pad
  groove – like drop without the arp (use under dense visuals / voiceover)
  break  – no kick, half-time clap, pad + sparse pluck, riser into the next section
  outro  – one final chord stab + kick on beat 1, ringing out, fade to silence

Outputs in --out:
  music.wav          stereo 44.1k 16-bit, length = bars * 4 beats exactly
  sfx/*.wav          whoosh, riser, impact, pop, slap, tick, shutter, stamp
  beats.json         bpm, fps, framesPerBeat, bar start frames, section map (frame ranges)

Requires: numpy, scipy (pip install numpy scipy)
"""
import argparse
import json
import os
import wave

import numpy as np
from scipy import signal

SR = 44100
RNG = np.random.default_rng(7)

NOTE = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
FLATS = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}
SECTION_KINDS = ("intro", "drop", "groove", "break", "outro")


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def env_exp(n, decay_s):
    t = np.arange(n) / SR
    return np.exp(-t / max(decay_s, 1e-4))


def lp(x, cutoff, order=2):
    sos = signal.butter(order, min(cutoff, SR / 2 - 100), "low", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def hp(x, cutoff, order=2):
    sos = signal.butter(order, cutoff, "high", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def bp(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, min(hi, SR / 2 - 100)], "band", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def saw(f, n, detune=0.0):
    t = np.arange(n) / SR
    ph = (t * f * (1 + detune)) % 1.0
    return 2 * ph - 1


def noise(n):
    return RNG.uniform(-1, 1, n)


# ---------------------------------------------------------------- instruments
def kick(dur=0.45):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * env_exp(n, 0.16)
    click = hp(noise(n), 3000) * env_exp(n, 0.004) * 0.35
    return np.tanh((body + click) * 1.6) * 0.9


def clap(dur=0.35):
    n = int(SR * dur)
    x = np.zeros(n)
    for off in (0, 0.011, 0.022):
        i = int(off * SR)
        burst = bp(noise(n - i), 900, 5000) * env_exp(n - i, 0.008 if off < 0.02 else 0.12)
        x[i:] += burst
    return x * 0.7


def snare(dur=0.25):
    n = int(SR * dur)
    t = np.arange(n) / SR
    tone = np.sin(2 * np.pi * 190 * t) * env_exp(n, 0.05)
    nz = bp(noise(n), 1500, 9000) * env_exp(n, 0.09)
    return (tone * 0.5 + nz) * 0.6


def hat(open_=False):
    dur = 0.25 if open_ else 0.06
    n = int(SR * dur)
    return hp(noise(n), 7000, 4) * env_exp(n, 0.09 if open_ else 0.018) * 0.35


def tick():
    n = int(SR * 0.03)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2400 * t) + 0.4 * hp(noise(n), 5000)) * env_exp(n, 0.006) * 0.5


def bass_note(midi, dur):
    n = int(SR * dur)
    x = saw(hz(midi), n) + 0.6 * np.sin(2 * np.pi * hz(midi) * np.arange(n) / SR)
    x = lp(x, 380, 4)
    a = np.minimum(1, np.arange(n) / (0.004 * SR))
    return np.tanh(x * 1.4) * a * env_exp(n, dur * 0.9) * 0.55


def pluck(midi, dur=0.28):
    n = int(SR * dur)
    x = 0.6 * saw(hz(midi), n) + 0.4 * saw(hz(midi), n, 0.006)
    bright = lp(x, 5200, 2) * env_exp(n, 0.05)
    dark = lp(x, 1400, 2)
    return (bright + dark * 0.6) * env_exp(n, 0.16) * 0.28


def pad_chord(midis, dur):
    n = int(SR * dur)
    x = np.zeros(n)
    for m in midis:
        for d in (-0.004, 0.0, 0.005):
            x += saw(hz(m), n, d)
    x = lp(x / (len(midis) * 3), 1500, 2)
    att = np.minimum(1, np.arange(n) / (0.35 * SR))
    rel = np.minimum(1, (n - np.arange(n)) / (0.25 * SR))
    return x * att * rel * 0.22


def riser(dur):
    n = int(SR * dur)
    t = np.arange(n) / SR
    prog = t / dur
    chunks = 24
    out = np.zeros(n)
    size = n // chunks
    for c in range(chunks):
        s, e = c * size, min(n, (c + 2) * size)
        lo = 300 + 5000 * (c / chunks) ** 2
        seg = bp(noise(e - s), lo, lo * 3) * np.hanning(e - s)
        out[s:e] += seg
    f = 200 + 900 * prog ** 2
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.15
    return (out * 0.5 + tone) * prog ** 1.8 * 0.6


def whoosh(dur=0.45):
    n = int(SR * dur)
    chunks = 16
    out = np.zeros(n)
    size = n // chunks
    for c in range(chunks):
        s, e = c * size, min(n, (c + 2) * size)
        center = 400 + 3600 * np.sin(np.pi * c / chunks)
        out[s:e] += bp(noise(e - s), center * 0.6, center * 1.6) * np.hanning(e - s)
    shape = np.sin(np.pi * np.arange(n) / n) ** 1.5
    return out * shape * 0.9


def impact(dur=1.4):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = 38 + 60 * np.exp(-t / 0.06)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 0.5)
    crack = lp(noise(n), 3500) * env_exp(n, 0.06) * 0.5
    return np.tanh((boom + crack) * 1.5) * 0.9


def pop():
    n = int(SR * 0.09)
    t = np.arange(n) / SR
    f = 320 + 700 * np.exp(-t / 0.012)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 0.03) * 0.8


def slap():
    n = int(SR * 0.18)
    t = np.arange(n) / SR
    thump = np.sin(2 * np.pi * 95 * t) * env_exp(n, 0.04)
    paper = bp(noise(n), 800, 6000) * env_exp(n, 0.025)
    return np.tanh((thump + paper) * 1.4) * 0.8


def shutter():
    n = int(SR * 0.16)
    x = np.zeros(n)
    for off, g in ((0, 1.0), (0.055, 0.7)):
        i = int(off * SR)
        m = int(0.03 * SR)
        x[i:i + m] += hp(noise(m), 2500) * env_exp(m, 0.006) * g
    return x * 0.8


def stamp():
    n = int(SR * 0.25)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 70 * t) * env_exp(n, 0.07)
    hit = lp(noise(n), 2500) * env_exp(n, 0.015)
    return np.tanh((body + hit * 0.8) * 2) * 0.8


# ---------------------------------------------------------------- helpers
def place(buf, x, at, gain=1.0):
    i = int(at * SR)
    if i >= len(buf):
        return
    e = min(len(buf), i + len(x))
    buf[i:e] += x[: e - i] * gain


def reverb(x, secs=1.1, mix=0.25):
    n = int(SR * secs)
    ir = noise(n) * env_exp(n, secs / 4)
    ir = lp(ir, 6000)
    ir /= np.sqrt(np.sum(ir ** 2))
    wet = signal.fftconvolve(x, ir)[: len(x)]
    return x * (1 - mix) + wet * mix * 2.5


def write_wav(path, stereo):
    stereo = np.clip(stereo, -1, 1)
    data = (stereo * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2 if stereo.ndim == 2 else 1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


def chords_for(key, mode):
    root = 57 + NOTE[key] - 9  # A -> 57 (A3)
    if mode == "minor":  # i - VI - III - VII
        degs = [(0, "m"), (-4, "M"), (3, "M"), (-2, "M")]
    else:  # I - V - vi - IV
        degs = [(0, "M"), (7, "M"), (9, "m"), (5, "M")]
    out = []
    for off, q in degs:
        r = root + off
        third = 3 if q == "m" else 4
        out.append([r, r + third, r + 7])
    return out


# ---------------------------------------------------------------- arrangement
def build(bpm, sections, key, mode, fps):
    beat = 60 / bpm
    bar = beat * 4
    total_bars = sum(b for _, b in sections)
    length = total_bars * bar
    n = int(round(length * SR))
    drums, bass, synth, fx = (np.zeros(n) for _ in range(4))
    duck = np.ones(n)
    prog = chords_for(key, mode)

    K, C, S, CH, OH = kick(), clap(), snare(), hat(), hat(True)
    section_map = []
    bar_i = 0
    for si, (kind, nbars) in enumerate(sections):
        nxt = sections[si + 1][0] if si + 1 < len(sections) else None
        start_bar = bar_i
        for b in range(nbars):
            t0 = bar_i * bar
            chord = prog[bar_i % 4]
            last_bar = b == nbars - 1
            if kind in ("drop", "groove"):
                for q in range(4):
                    place(drums, K, t0 + q * beat)
                    kd = int((t0 + q * beat) * SR)
                    m = int(0.18 * SR)
                    duck[kd:kd + m] = np.minimum(duck[kd:kd + m], 0.25 + 0.75 * np.linspace(0, 1, len(duck[kd:kd + m])) ** 1.5)
                    place(drums, OH, t0 + q * beat + beat / 2, 0.8)
                    for s16 in range(4):
                        place(drums, CH, t0 + q * beat + s16 * beat / 4, 0.5 if s16 % 2 else 0.25)
                place(drums, C, t0 + beat)
                place(drums, C, t0 + 3 * beat)
                for e in range(8):
                    place(bass, bass_note(chord[0] - 24, beat / 2 * 0.95), t0 + e * beat / 2)
                place(synth, pad_chord(chord, bar), t0, 0.8)
                if kind == "drop":
                    pattern = [0, 1, 2, 1, 2, 0, 1, 2]
                    for s16 in range(16):
                        note = chord[pattern[s16 % 8]] + (12 if s16 % 4 == 3 else 0) + 12
                        place(synth, pluck(note), t0 + s16 * beat / 4, 0.9 if s16 % 4 == 0 else 0.6)
            elif kind == "intro":
                for q in range(4):
                    place(drums, tick(), t0 + q * beat, 0.9)
                    for s16 in range(4):
                        place(drums, CH, t0 + q * beat + s16 * beat / 4, 0.18 + 0.1 * (s16 == 2))
                place(synth, lp(pad_chord(chord, bar), 700), t0, 0.9)
            elif kind == "break":
                place(drums, C, t0 + 2 * beat, 0.9)
                for q in range(4):
                    place(drums, CH, t0 + q * beat + beat / 2, 0.3)
                place(synth, pad_chord(chord, bar), t0, 1.0)
                for q in (0, 1.5, 3):
                    place(synth, pluck(chord[int(q) % 3] + 12, 0.4), t0 + q * beat, 0.7)
                place(bass, bass_note(chord[0] - 24, bar * 0.9), t0, 0.6)
            elif kind == "outro":
                if b == 0:
                    place(drums, K, t0)
                    stab = pad_chord(chord + [chord[0] + 12], bar * nbars) * 2.2
                    for m in chord:
                        stab += pluck(m + 12, bar * nbars) * 0.8
                    place(synth, stab, t0)
                    place(fx, impact(), t0, 0.7)
            # transitions into the next section
            if last_bar and nxt in ("drop", "groove") and kind in ("intro", "break", "groove", "drop"):
                if kind in ("intro", "break"):
                    place(fx, riser(bar), t0, 0.9)
                    for r in range(8):  # snare roll on the last two beats
                        place(drums, S, t0 + 2 * beat + r * beat / 4, 0.3 + 0.08 * r)
            if last_bar and nxt == "outro":
                place(fx, riser(bar), t0, 0.7)
            bar_i += 1
        section_map.append({
            "section": kind,
            "startFrame": round(start_bar * bar * fps),
            "endFrame": round(bar_i * bar * fps),
        })

    # mix: sidechain bass + synths to the kick, reverb on synths
    synth = reverb(synth * duck, 1.3, 0.3)
    bass = bass * duck
    mono = drums * 0.9 + bass * 0.9 + synth + fx * 0.8
    # stereo: widen synth with a Haas delay
    d = int(0.012 * SR)
    left = mono.copy()
    right = mono.copy()
    right[d:] += synth[:-d] * 0.25
    left += synth * 0.1
    st = np.stack([hp(left, 32), hp(right, 32)], axis=1)
    # master: soft clip, normalize to -1 dBFS, fade the last 0.5s
    st = np.tanh(st * 1.2)
    st /= np.max(np.abs(st)) / 0.89
    fade = int(0.5 * SR)
    st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    return st, section_map, total_bars


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bpm", type=float, default=120)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--sections", default="intro:2,drop:7,break:3,drop:2,outro:1")
    ap.add_argument("--key", default="A")
    ap.add_argument("--mode", default="minor", choices=["minor", "major"])
    ap.add_argument("--out", default="public/audio")
    a = ap.parse_args()

    key = a.key.strip()
    key = key[0].upper() + key[1:]
    key = FLATS.get(key, key)
    if key not in NOTE:
        ap.error(f"--key must be one of {', '.join(list(NOTE) + list(FLATS))} (got {a.key!r})")
    a.key = key

    sections = []
    for part in a.sections.split(","):
        try:
            kind, nbars = part.strip().split(":")
            nbars = int(nbars)
        except ValueError:
            ap.error(f"bad section {part!r}; use kind:bars, e.g. drop:4")
        if kind not in SECTION_KINDS:
            ap.error(f"unknown section {kind!r}; choose from {', '.join(SECTION_KINDS)}")
        if nbars < 1:
            ap.error(f"section {part!r} needs at least 1 bar")
        sections.append((kind, nbars))

    fpb = a.fps * 60 / a.bpm
    if abs(fpb - round(fpb)) > 1e-6:
        print(f"warning: {a.bpm} BPM at {a.fps}fps = {fpb:.3f} frames per beat, so beats fall between frames "
              f"and cuts will drift up to half a frame. Integer grids at 30fps: 90, 100, 120, 150 BPM.")
    os.makedirs(os.path.join(a.out, "sfx"), exist_ok=True)

    st, section_map, bars = build(a.bpm, sections, a.key, a.mode, a.fps)
    write_wav(os.path.join(a.out, "music.wav"), st)

    kit = {"whoosh": whoosh(), "riser": riser(60 / a.bpm * 4), "impact": impact(), "pop": pop(),
           "slap": slap(), "tick": tick(), "shutter": shutter(), "stamp": stamp()}
    for name, x in kit.items():
        x = x / (np.max(np.abs(x)) + 1e-9) * 0.9
        write_wav(os.path.join(a.out, "sfx", f"{name}.wav"), x)

    grid = {
        "bpm": a.bpm,
        "fps": a.fps,
        "framesPerBeat": fpb,
        "framesPerBar": fpb * 4,
        "bars": bars,
        "durationInFrames": round(bars * 4 * fpb),
        "barStartFrames": [round(i * 4 * fpb) for i in range(bars)],
        "sections": section_map,
    }
    with open(os.path.join(a.out, "beats.json"), "w") as f:
        json.dump(grid, f, indent=2)
    print(json.dumps({k: grid[k] for k in ("bpm", "framesPerBeat", "durationInFrames", "sections")}, indent=2))


if __name__ == "__main__":
    main()
