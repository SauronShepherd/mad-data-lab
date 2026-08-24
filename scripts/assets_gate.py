"""Automated asset preflight for the deployed challenge payload."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    images = list((ROOT / "public" / "assets").glob("*.png"))
    assert images, "no raster assets"
    for path in images:
        with Image.open(path) as image:
            image.verify()
        width, height = Image.open(path).size
        assert width <= 2560 and height <= 1440, f"oversized dimensions: {path}"
        assert path.stat().st_size <= 2_000_000, f"oversized image: {path}"

    audio = ROOT / "public" / "audio" / "mad_data_lab_curiosity.mp3"
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-of", "json", str(audio)], capture_output=True, text=True, check=True)
    fmt = json.loads(probe.stdout)["format"]
    duration = float(fmt["duration"])
    size = int(fmt["size"])
    assert 330 <= duration <= 510, f"audio duration outside 330-510 seconds: {duration}"
    assert size < 8_500_000, f"audio exceeds 8.5 MB: {size}"
    print(f"assets gate: PASS ({len(images)} images, {duration:.1f}s audio, {size} bytes)")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, OSError, subprocess.CalledProcessError) as exc:
        print(f"assets gate: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
