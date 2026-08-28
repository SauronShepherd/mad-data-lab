import json
from pathlib import Path

from server.case_data import CASE042_EXPERIMENTS, experiment_payload

ROOT = Path(__file__).resolve().parents[1]


def test_case042_experiment_payloads_include_data_backed_instrument_models():
    payloads = [experiment_payload(item, index) for index, item in enumerate(CASE042_EXPERIMENTS)]
    assert [item["instrument"] for item in payloads] == ["WATERFALL", "SNAPSHOT_DIFF", "DQ_PANEL", "FORMULA_CHECK", "RECONCILIATION"]
    waterfall = payloads[0]["instrument_model"]
    assert abs(sum(row["delta"] for row in waterfall["components"]) - (-6.8)) < 0.001
    snapshot = payloads[1]["instrument_model"]
    assert snapshot["net_impact"] == -5.9
    assert [row["count"] for row in snapshot["groups"]] == [23, 2, 5]
    assert payloads[2]["instrument_model"]["overlap"] is True
    assert payloads[3]["instrument_model"]["changed"] is False
    assert payloads[4]["instrument_model"]["unreconciled"] == 0.0


def test_instrument_renderer_has_closed_registry_and_no_case_specific_route():
    source = (ROOT / "src/instruments.jsx").read_text(encoding="utf-8")
    for instrument in ("KPI_DELTA", "WATERFALL", "SNAPSHOT_DIFF", "EVIDENCE_TABLE", "DQ_PANEL", "FORMULA_DIFF", "LINEAGE_GRAPH", "RECONCILIATION"):
        assert instrument in source
    assert "eval(" not in source
    assert "CASE_0042" not in source


def test_css_does_not_generate_analytical_evidence_claims():
    assert "DQ SIGNAL" not in (ROOT / "src/evidence-polish.css").read_text(encoding="utf-8")
