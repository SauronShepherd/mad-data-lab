"""Validate and summarize MDL-4 review candidates without approving them."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    plan = json.loads((ROOT / "assets/review/MDL-4/art-generation-plan.json").read_text(encoding="utf-8"))
    candidates = []
    for asset in plan["assets"]:
        for item in asset["candidates"]:
            path = ROOT / "assets/review/MDL-4" / item["path"]
            with Image.open(path) as image:
                image.verify()
            with Image.open(path) as image:
                candidates.append({"asset_id": asset["asset_id"], "candidate_id": Path(item["path"]).stem, "path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "width": image.width, "height": image.height, "mode": image.mode, "status": "CANDIDATE"})
    output = {"iteration": "MDL-4", "status": "CANDIDATES_PREFLIGHT_PASS", "approval_status": "DEFERRED_TO_USER_END_REVIEW", "candidate_count": len(candidates), "candidates": candidates}
    destination = ROOT / "release-report/MDL-4/art-preflight.json"
    destination.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
