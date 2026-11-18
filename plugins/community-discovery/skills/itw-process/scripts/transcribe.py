#!/usr/bin/env python3
"""High-recall local transcription for faint remote speakers (faster-whisper).

Pipeline: ffmpeg filter (loudnorm + band-pass, or raw x8) -> beam 10, temperature fallback, no VAD.
Output lines: "[mm:ss] text". Progress goes to stderr.

Usage: transcribe.py AUDIO OUT.txt [--variant loud|raw8] [--lang fr] [--model medium] [--prompt TEXT]
Run with the venv python found by whisper_env.sh (needs faster-whisper, numpy, ffmpeg).
"""
import argparse, subprocess, sys

FILTERS = {
    "loud": "highpass=f=100,lowpass=f=4000,loudnorm=I=-14,volume=2",
    "raw8": "volume=8,alimiter=limit=0.95",
}

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio"); ap.add_argument("out")
    ap.add_argument("--variant", choices=FILTERS, default="loud")
    ap.add_argument("--lang", default="fr")
    ap.add_argument("--model", default="medium")
    ap.add_argument("--prompt", default=None, help="domain terms to bias the transcription")
    a = ap.parse_args()

    import numpy as np
    from faster_whisper import WhisperModel

    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", a.audio, "-af", FILTERS[a.variant],
         "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
        capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, dtype=np.float32)
    dur = len(audio) / 16000
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    segs, _ = model.transcribe(
        audio, language=a.lang, vad_filter=False, beam_size=10,
        condition_on_previous_text=False, temperature=[0, 0.2, 0.4],
        no_speech_threshold=0.9, log_prob_threshold=-2.0,
        compression_ratio_threshold=3.0, initial_prompt=a.prompt)
    with open(a.out, "w") as f:
        for s in segs:
            m, sec = divmod(int(s.start), 60)
            f.write(f"[{m:02d}:{sec:02d}] {s.text.strip()}\n"); f.flush()
            print(f"{s.end:.0f}/{dur:.0f}s", file=sys.stderr, flush=True)
    print("done", file=sys.stderr)

if __name__ == "__main__":
    main()
