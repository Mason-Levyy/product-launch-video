"""Run make_soundtrack.py on a short arrangement and check the beat grid and files it writes."""

import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOUNDTRACK_SCRIPT = REPO_ROOT / "product-launch-video" / "scripts" / "make_soundtrack.py"
EXPECTED_SFX = {"whoosh", "riser", "impact", "pop", "slap", "tick", "shutter", "stamp"}
BPM, FPS = 120, 30
SECTIONS = "intro:1,drop:1,break:1,groove:1,outro:1"
SECTION_COUNT = 5
FRAMES_PER_BAR_AT_120_BPM_30_FPS = 60


def main() -> int:
    with tempfile.TemporaryDirectory() as output_directory:
        subprocess.run(
            [sys.executable, str(SOUNDTRACK_SCRIPT), "--bpm", str(BPM), "--fps", str(FPS),
             "--sections", SECTIONS, "--key", "Eb", "--mode", "major", "--out", output_directory],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        output_path = Path(output_directory)
        grid = json.loads((output_path / "beats.json").read_text())

        expected_duration = SECTION_COUNT * FRAMES_PER_BAR_AT_120_BPM_30_FPS
        assert grid["framesPerBeat"] == 15, grid["framesPerBeat"]
        assert grid["durationInFrames"] == expected_duration, grid["durationInFrames"]
        assert [section["section"] for section in grid["sections"]] == ["intro", "drop", "break", "groove", "outro"]
        assert grid["sections"][-1]["endFrame"] == expected_duration

        with wave.open(str(output_path / "music.wav")) as music:
            assert music.getnchannels() == 2
            music_frames = round(music.getnframes() / music.getframerate() * FPS)
            assert music_frames == expected_duration, music_frames

        written_sfx = {path.stem for path in (output_path / "sfx").glob("*.wav")}
        assert written_sfx == EXPECTED_SFX, written_sfx ^ EXPECTED_SFX

    print(f"ok   soundtrack: {expected_duration} frames, {len(EXPECTED_SFX)} sfx, beat grid consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
