"""Validate the single production audio derivative against MDL-6 budgets."""
from __future__ import annotations
import json, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "public" / "audio" / "mad_data_lab_curiosity.mp3"
def main() -> None:
    if not AUDIO.is_file(): raise AssertionError(f"missing audio: {AUDIO}")
    if AUDIO.stat().st_size >= 8_500_000: raise AssertionError("audio exceeds 8.5 MB")
    if not shutil.which("ffprobe"): raise RuntimeError("ffprobe is required for audio preflight")
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=sample_rate,channels", "-of", "json", str(AUDIO)], capture_output=True, text=True, check=True)
    payload = json.loads(result.stdout); fmt = payload.get("format", {}); streams = payload.get("streams", [])
    duration = float(fmt.get("duration", 0)); assert 330 <= duration <= 510, f"duration {duration:.2f}s outside 330-510s"
    assert streams and int(streams[0].get("channels", 0)) in (1, 2), "audio must be mono or stereo"
    assert int(streams[0].get("sample_rate", 0)) >= 44100, "sample rate below 44.1 kHz"
    print(json.dumps({"status":"PASS", "path":str(AUDIO.relative_to(ROOT)), "duration_seconds":duration, "bytes":AUDIO.stat().st_size}, indent=2))
if __name__ == "__main__":
    try: main()
    except (AssertionError, OSError, RuntimeError, subprocess.CalledProcessError) as exc: print(f"audio preflight: FAIL: {exc}", file=sys.stderr); raise SystemExit(1)
