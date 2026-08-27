"""Build an exact-byte MDL-5 artwork handoff; never records human approval."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT / "public/assets/pixelart"
OUT = ROOT / "release-report/MDL-5/artwork-handoff.json"

DESTINATIONS = {
    "dr-genie-mdl3.png": "public/assets/pixelart/dr-genie-mdl3.png",
    "decomposer.png": "public/assets/pixelart/decomposer.png",
    "reactor.png": "public/assets/pixelart/reactor.png",
    "microscope.png": "public/assets/pixelart/microscope.png",
    "telescope.png": "public/assets/pixelart/telescope.png",
    "scanner.png": "public/assets/pixelart/scanner.png",
}


def describe(path: Path, destination: str) -> dict:
    raw = path.read_bytes()
    with Image.open(path) as image:
        width, height = image.size
    return {
        "candidate_filename": path.name,
        "candidate_path": path.relative_to(ROOT).as_posix(),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "dimensions": {"width": width, "height": height},
        "file_size_bytes": len(raw),
        "intended_production_destination": destination,
        "status": "CURRENT_DEPLOYED_COMPARISON",
    }


def main() -> None:
    assets = []
    for filename, destination in DESTINATIONS.items():
        path = PRODUCTION / filename
        if not path.is_file():
            raise SystemExit(f"missing production comparison asset: {path}")
        assets.append(describe(path, destination))
    result = {
        "iteration": "MDL-5",
        "status": "PENDING_HUMAN_APPROVAL",
        "human_approval_required": True,
        "approval_recorded": False,
        "canonical_visual_rule": {
            "genie": "friendly blue Dr. Genie emerging from a scientific tube/probe",
            "production_lamp_origin_for_genie": False,
        },
        "candidate_assets": [],
        "candidate_note": "No new MDL-5 candidate bytes are submitted. Listed assets are exact-byte comparisons against the current production tree.",
        "current_production_comparison": assets,
        "contact_sheets": [
            "assets/review/MDL-3/contact-sheets/A07.png",
            "assets/review/MDL-3/previews/A07-C01-1440x900.png",
            "assets/review/MDL-3/previews/A07-C02-1440x900.png",
        ],
        "next_action": "Human selects exact candidate bytes and records approval before any production copy.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "output": str(OUT.relative_to(ROOT)), "assets": len(assets)}, indent=2))


if __name__ == "__main__":
    main()
