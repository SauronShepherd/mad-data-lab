"""Fail-closed local MDL-4 contract validator."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
ROOT = Path(__file__).resolve().parents[1]
from backend.domain.badges import BADGES
from backend.domain.completion import REQUIRED_FAMILIES
from backend.domain.scoring import POINTS
from server.catalog import FULL_CASE_CATALOG
from server.main import app

REQUIRED_ROUTES = {
    ("GET", "/api/sessions/{session_id}"),
    ("POST", "/api/sessions/{session_id}/evidence/inspect"),
    ("POST", "/api/sessions/{session_id}/debrief"),
}

def main() -> None:
    assert len(FULL_CASE_CATALOG) == 7
    assert len({c.id for c in FULL_CASE_CATALOG}) == 7
    assert tuple(REQUIRED_FAMILIES) == tuple(FULL_CASE_CATALOG[0].required_experiments)
    assert set(POINTS) == {"START_INVESTIGATION", "INITIAL_PREDICTION_SUBMITTED", "INITIAL_PREDICTION_CORRECT", "REQUIRED_EXPERIMENT_COMPLETED", "HIGH_VALUE_EVIDENCE_INSPECTED", "REQUIRED_LINEAGE_OPENED", "FINAL_PREDICTION_CORRECT", "FINISH_DEBRIEF", "HINT_REVEALED", "EARLY_REVEAL"}
    assert list(BADGES) == ["DATA_APPRENTICE", "METRIC_SCIENTIST", "EVIDENCE_ANALYST", "SKEPTICAL_SCIENTIST", "CASE_COLLECTOR", "LAB_VETERAN", "RECONCILIATION_MASTER"]
    routes = {(m.upper(), path) for path, ops in app.openapi()["paths"].items() for m in ops}
    missing = sorted(REQUIRED_ROUTES - routes)
    if missing: raise SystemExit(json.dumps({"status":"FAIL", "missing_routes":missing}))
    # Private truth is a narrow backend scoring boundary, never a Genie or
    # browser dependency. Fail closed on either source or built package.
    for path in [ROOT / "backend/genie", ROOT / "server/genie.py", ROOT / "src", ROOT / "dist"]:
        files = [path] if path.is_file() else path.rglob("*")
        for candidate in files:
            if candidate.is_file() and candidate.suffix in {".py", ".ts", ".tsx", ".js", ".jsx", ".html"}:
                text = candidate.read_text(encoding="utf-8", errors="ignore")
                assert "case_oracle" not in text, f"private oracle reference leaked into {candidate}"
                assert "case_0042_truth.json" not in text, f"private fixture reference leaked into {candidate}"
    payload = app.openapi()
    assert "private_truth" not in json.dumps(payload), "private truth leaked into OpenAPI"
    digest_artifact = ROOT / "release-report/MDL-4/game-contract-digest.json"
    assert digest_artifact.exists(), "game contract digest artifact is missing"
    digest_payload = json.loads(digest_artifact.read_text(encoding="utf-8"))
    assert digest_payload.get("status") == "PASS" and len(digest_payload.get("digest", "")) == 64, "game contract digest is invalid"
    print(json.dumps({"status":"PASS", "case_count":7, "required_experiment_families":list(REQUIRED_FAMILIES)}))

if __name__ == "__main__": main()
