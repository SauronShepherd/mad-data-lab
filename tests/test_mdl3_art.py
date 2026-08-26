import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_mdl3_art_preflight_is_reproducible_and_hash_bound():
    result = subprocess.run([sys.executable, "scripts/build_mdl3_art_review.py"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    artifact = json.loads((ROOT / "release-report/MDL-3/art-preflight.json").read_text(encoding="utf-8"))
    assert artifact["status"] == "CANDIDATES_PREFLIGHT_PASS"
    assert artifact["candidate_count"] == 10
    assert {item["asset_id"] for item in artifact["candidates"]} == {"A05", "A07"}
    assert len({item["candidate_id"] for item in artifact["candidates"]}) == 10
    assert sum(item["asset_id"] == "A05" for item in artifact["candidates"]) == 6
    assert sum(item["asset_id"] == "A07" for item in artifact["candidates"]) == 4
    assert all(len(item["sha256"]) == 64 for item in artifact["candidates"])
    assert all((ROOT / item["path"]).is_file() for item in artifact["candidates"])
    assert all(item["transparent_background"] for item in artifact["candidates"] if item["asset_id"] == "A05")
    assert all(not item["transparent_background"] for item in artifact["candidates"] if item["asset_id"] == "A07")
    assert {item["asset_id"] for item in artifact["production_derivatives"]} == {"A05", "A07"}
    assert all(item["exists"] and len(item["sha256"]) == 64 for item in artifact["production_derivatives"])
    assert (ROOT / "release-report/MDL-3/art-contact-sheet.png").is_file()
    assert (ROOT / "assets/review/MDL-3/contact-sheets/A05.png").is_file()
    assert (ROOT / "assets/review/MDL-3/contact-sheets/A07.png").is_file()
