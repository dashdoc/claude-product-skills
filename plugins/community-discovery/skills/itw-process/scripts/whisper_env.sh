#!/usr/bin/env bash
# Locate or install a local faster-whisper environment for itw-process.
# Usage: whisper_env.sh check | install
# Env:   ITW_WHISPER_DIR  where the venv lives (default: ~/tools/whisper)
set -u
DIR="${ITW_WHISPER_DIR:-$HOME/tools/whisper}"
PY="$DIR/.venv/bin/python"

check() {
  local missing=()
  command -v ffmpeg >/dev/null 2>&1 || missing+=("ffmpeg (brew install ffmpeg)")
  if [ ! -x "$PY" ]; then
    missing+=("python venv at $DIR/.venv")
  elif ! "$PY" -c "import faster_whisper, numpy" >/dev/null 2>&1; then
    missing+=("faster-whisper / numpy in $DIR/.venv")
  fi
  if [ ${#missing[@]} -eq 0 ]; then echo "OK $DIR"; return 0; fi
  echo "MISSING: ${missing[*]}"; return 1
}

install() {
  command -v python3 >/dev/null 2>&1 || { echo "python3 not found — install Python 3.9+ first"; exit 1; }
  command -v ffmpeg >/dev/null 2>&1 || { echo "ffmpeg not found — run: brew install ffmpeg (then re-run)"; exit 1; }
  mkdir -p "$DIR" && python3 -m venv "$DIR/.venv" || exit 1
  "$PY" -m pip install --quiet --upgrade pip faster-whisper numpy || exit 1
  echo "Installed in $DIR (the ~1.5 GB 'medium' model downloads on the first transcription)."
  check
}

case "${1:-check}" in
  check) check ;;
  install) install ;;
  *) echo "usage: $0 check|install"; exit 2 ;;
esac
