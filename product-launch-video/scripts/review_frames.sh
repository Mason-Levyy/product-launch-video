#!/usr/bin/env bash
# Render still frames for visual review of a Remotion composition, plus a contact sheet.
#
# Usage (run from the Remotion project root):
#   bash review_frames.sh <CompositionId> <fps> <seconds...>
# Example (scene midpoints/ends, transition midpoints and the last frame of a 25s spot at 30fps):
#   bash review_frames.sh Launch-16x9 30 1.5 3.2 4.5 6.2 10 14.2 16.5 19.2 20.5 22.2 24.9
#
# Pass beat midpoints, ~5 frames (0.17s) after each transition starts, and the last frame.
# Output: review/<CompositionId>/f<frame>.png and, if ffmpeg is installed,
#         review/<CompositionId>/contact-sheet.png. Look at the sheet, then open suspicious frames.

set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <CompositionId> <fps> <seconds...>" >&2
  exit 1
fi

COMP="$1"; FPS="$2"; shift 2
OUT="review/${COMP}"
mkdir -p "$OUT"

FRAMES=()
for s in "$@"; do
  frame=$(awk -v s="$s" -v f="$FPS" 'BEGIN { printf "%d", s * f }')
  FRAMES+=("$frame")
  echo "→ ${COMP} @ ${s}s (frame ${frame})"
  npx remotion still "$COMP" "${OUT}/f${frame}.png" --frame="$frame" --log=error
done

if command -v ffmpeg >/dev/null 2>&1; then
  n=${#FRAMES[@]}
  cols=4; rows=$(( (n + cols - 1) / cols ))
  list="${OUT}/.frames.txt"; : > "$list"
  for f in "${FRAMES[@]}"; do echo "file '$(pwd)/${OUT}/f${f}.png'" >> "$list"; done
  ffmpeg -y -loglevel error -f concat -safe 0 -i "$list" \
    -vf "scale=640:-1,drawtext=text='%{n}':x=12:y=12:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.6,tile=${cols}x${rows}:padding=8:color=gray" \
    -frames:v 1 "${OUT}/contact-sheet.png" 2>/dev/null \
  || ffmpeg -y -loglevel error -f concat -safe 0 -i "$list" \
    -vf "scale=640:-1,tile=${cols}x${rows}:padding=8:color=gray" -frames:v 1 "${OUT}/contact-sheet.png"
  rm -f "$list"
  echo "Contact sheet: ${OUT}/contact-sheet.png (tiles in the order you passed the times)"
else
  echo "ffmpeg not found; skipping contact sheet."
fi

echo "Done. Stills in ${OUT}/"
