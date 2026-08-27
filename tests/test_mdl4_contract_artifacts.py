import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_mdl4_contract_validator_passes():
    result = subprocess.run([sys.executable, "scripts/validate_mdl4_contract.py"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr

def test_mdl4_art_review_contains_all_candidates_and_contact_sheets():
    plan = __import__("json").loads((ROOT / "assets/review/MDL-4/art-generation-plan.json").read_text())
    assert sum(len(item["candidates"]) for item in plan["assets"]) == 10
    for asset_id, count in (("A03", 6), ("A06", 4)):
        sheet = ROOT / f"assets/review/MDL-4/contact-sheets/{asset_id}.png"
        assert sheet.is_file() and sheet.stat().st_size > 0
        item = next(x for x in plan["assets"] if x["asset_id"] == asset_id)
        assert len(item["candidates"]) == count
