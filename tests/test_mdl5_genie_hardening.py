import json
from pathlib import Path

import pytest

from backend.genie.protocol import validate_control_response
from backend.genie.query_registry import render_query, validate_result
from server.genie import parse_control_json


ROOT = Path(__file__).resolve().parents[1]


def _payload(**changes):
    value = {
        "schema_version": "1.0", "case_id": "CASE_0042",
        "observation": "Current evidence identifies a material V2 movement.",
        "hypotheses": [{"id": "H1", "title": "Source movement", "status": "POSSIBLE", "evidence": []}],
        "selected_experiment": {"id": "SNAPSHOT_DIFF", "question": "Compare V2 snapshots", "target_component": "V2"},
        "instrument": {"id": "SNAPSHOT_DIFF", "title": "Snapshot comparison"},
        "next_action": "RUN_EXPERIMENT", "scientist_line": "This isolates changed source records.",
    }
    value.update(changes)
    return value


def test_protocol_rejects_version_identifier_instrument_and_state_tampering():
    for changes in (
        {"schema_version": "2.0"},
        {"selected_experiment": {"id": "bad-id", "question": "x", "target_component": "V2"}},
        {"instrument": {"id": "UNKNOWN", "title": "x"}},
        {"hypotheses": [{"id": "H1", "title": "x", "status": "PROBABLE", "evidence": []}]},
    ):
        with pytest.raises(ValueError):
            validate_control_response(_payload(**changes), active_case_id="CASE_0042", allowed_experiments={"SNAPSHOT_DIFF"})


def test_protocol_and_query_boundary_reject_cross_case_evidence_and_invalid_filters():
    with pytest.raises(ValueError):
        validate_result("snapshot_evidence", case_id="CASE_0042", rows=[{"case_id": "CASE_0107"}])
    with pytest.raises(ValueError):
        render_query("snapshot_evidence", case_id="CASE_0042' OR '1'='1")
    with pytest.raises(ValueError):
        render_query("not-registered", case_id="CASE_0042")


def test_protocol_rejects_a_valid_payload_for_the_wrong_active_case():
    with pytest.raises(ValueError, match="Case ID"):
        validate_control_response(_payload(case_id="CASE_0107"), active_case_id="CASE_0042", allowed_experiments={"SNAPSHOT_DIFF"})


def test_public_genie_boundaries_exclude_private_truth_and_scoring_oracle():
    source = (ROOT / "server/genie.py").read_text(encoding="utf-8")
    assert "backend.private" not in source
    assert "case_oracle" not in source
    assert "verdict_validator" not in source
    instructions = (ROOT / "genie/instructions.md").read_text(encoding="utf-8")
    assert "CASE_TRUTH" in instructions
    assert "Never use `CASE_TRUTH`" in instructions
    assert "case_truth" not in json.dumps(json.loads((ROOT / "genie/registry.json").read_text(encoding="utf-8"))).lower()


def test_experiment_rationales_explain_analytical_use_without_private_cause():
    from server.case_data import CASE042_EXPERIMENTS
    for experiment in CASE042_EXPERIMENTS:
        assert len(experiment.rationale) >= 20
        assert experiment.id.lower() not in experiment.rationale.lower()
        assert "SOURCE_RECORD_CHANGE" not in experiment.rationale
        assert "case_truth" not in experiment.rationale.lower()


@pytest.mark.parametrize("failure", [TimeoutError("timeout"), ValueError("invalid json"), RuntimeError("partial response"), ConnectionError("space unavailable"), RuntimeError("rate limit"), OSError("transient http")])
def test_genie_turn_failures_never_become_success(failure):
    from backend.genie.lifecycle import GenieTurn, TurnFailure

    result = GenieTurn(
        active_case_id="CASE_0042", allowed_experiments={"SNAPSHOT_DIFF"},
        instrument_for_experiment=lambda _: {"SNAPSHOT_DIFF"},
        request=lambda _: (_ for _ in ()).throw(failure),
        repair=lambda _: "{}",
    )
    with pytest.raises(type(failure)):
        result.run()


def test_legacy_boundary_rejects_unsafe_nested_hypothesis_content():
    payload = {
        "experiment_id": "SNAPSHOT_DIFF", "name": "Snapshot",
        "instrument": "SNAPSHOT_DIFF", "rationale": "inspect changes",
        "evidence": "curated evidence",
        "hypothesis_updates": [{"name": "H1", "status": "POSSIBLE", "note": "<script>alert(1)</script>"}],
    }
    with pytest.raises(ValueError, match="unsafe"):
        parse_control_json(json.dumps(payload), {"SNAPSHOT_DIFF"})
