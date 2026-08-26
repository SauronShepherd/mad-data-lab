"""Deterministic MDL-03 art preflight for implementation-owned review assets."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "assets/review/MDL-3/art-generation-plan.json"


def main() -> None:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    candidates = []
    for slot in plan["slots"]:
        for item in slot["candidates"]:
            path = ROOT / item["path"]
            with Image.open(path) as image:
                image.verify()
            with Image.open(path) as image:
                width, height, mode = image.width, image.height, image.mode
                alpha_present = mode == "RGBA" and image.getchannel("A").getextrema() != (255, 255)
            candidates.append({
                "asset_id": slot["asset_id"],
                "candidate_id": item["id"],
                "path": item["path"],
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "width": width,
                "height": height,
                "mode": mode,
                "transparent_background": alpha_present,
                "status": "CANDIDATE",
            })
    output = {
        "iteration": "MDL-3",
        "status": "CANDIDATES_PREFLIGHT_PASS",
        "approval_status": "IMPLEMENTATION_OWNED",
        "candidate_count": len(candidates),
        "preview_size": "1440x900",
        "candidates": candidates,
        "production_derivatives": [],
    }
    for derivative in plan.get("production_derivatives", []):
        path = ROOT / derivative["path"]
        output["production_derivatives"].append({**derivative, "exists": path.is_file(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        if not path.is_file() or output["production_derivatives"][-1]["sha256"] != derivative["sha256"]:
            raise RuntimeError(f"production derivative drift: {derivative['path']}")
    destination = ROOT / "release-report/MDL-3/art-preflight.json"
    destination.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
