import json

import pytest

from backend.genie.protocol import Action, Instrument, extract_control_object, validate_control_response


def payload(**overrides):
    value = {
        "schema_version": "1.0",
        "case_id": "CASE_0042",
        "observation": "V2 is the strongest current signal.",
        "hypotheses": [{"id": "H1", "title": "Source values changed", "status": "POSSIBLE", "evidence": []}],
        "selected_experiment": {"id": "SNAPSHOT_DIFF", "question": "What changed in V2?", "target_component": "V2"},
        "instrument": {"id": "SNAPSHOT_DIFF", "title": "Snapshot Reactor"},
        "next_action": "RUN_EXPERIMENT",
        "scientist_line": "Compare the V2 snapshots.",
    }
    value.update(overrides)
    return value


def test_accepts_direct_and_single_fenced_json():
    raw = json.dumps(payload())
    assert extract_control_object(raw)["case_id"] == "CASE_0042"
    assert extract_control_object("Here is the result:\n```json\n" + raw + "\n```\nDone") == payload()


@pytest.mark.parametrize("raw", ["", "plain prose", "{}\n{}", "```json\n{}\n```\n```json\n{}\n```"])
def test_rejects_ambiguous_or_missing_control(raw):
    with pytest.raises(ValueError):
        extract_control_object(raw)


def test_strict_domain_validation_rejects_wrong_case_unknown_fields_and_completed():
    with pytest.raises(ValueError):
        validate_control_response(payload(case_id="CASE_0107"), active_case_id="CASE_0042", allowed_experiments={"SNAPSHOT_DIFF"})
    with pytest.raises(ValueError):
        validate_control_response(payload(extra="nope"), active_case_id="CASE_0042", allowed_experiments={"SNAPSHOT_DIFF"})
    with pytest.raises(ValueError):
        validate_control_response(payload(), active_case_id="CASE_0042", allowed_experiments={"SNAPSHOT_DIFF"}, completed_experiments={"SNAPSHOT_DIFF"})


def test_action_semantics_and_instrument_allowlist():
    response = validate_control_response(
        payload(),
        active_case_id="CASE_0042",
        allowed_experiments={"SNAPSHOT_DIFF"},
        instrument_for_experiment=lambda _: {Instrument.SNAPSHOT_DIFF.value},
    )
    assert response.next_action == Action.RUN_EXPERIMENT
    with pytest.raises(ValueError):
        validate_control_response(payload(instrument={"id": "DQ_PANEL", "title": "wrong"}), active_case_id="CASE_0042", allowed_experiments={"SNAPSHOT_DIFF"}, instrument_for_experiment=lambda _: {"SNAPSHOT_DIFF"})
    with pytest.raises(ValueError):
        validate_control_response(payload(next_action="CONCLUDE"), active_case_id="CASE_0042", allowed_experiments={"SNAPSHOT_DIFF"})


def test_duplicate_hypotheses_and_unknown_targets_are_rejected():
    duplicate = payload(hypotheses=[
        {"id": "H1", "title": "one", "status": "POSSIBLE", "evidence": []},
        {"id": "H1", "title": "again", "status": "POSSIBLE", "evidence": []},
    ])
    with pytest.raises(ValueError, match="duplicate"):
        validate_control_response(duplicate, active_case_id="CASE_0042", allowed_experiments={"SNAPSHOT_DIFF"})
    with pytest.raises(ValueError, match="target"):
        validate_control_response(payload(), active_case_id="CASE_0042", allowed_experiments={"SNAPSHOT_DIFF"}, valid_targets=lambda _: {"V1", "V3"})


def test_assertive_hypothesis_status_requires_evidence():
    with pytest.raises(ValueError, match="requires visible evidence"):
        validate_control_response(payload(hypotheses=[{"id": "H1", "title": "Source", "status": "SUPPORTED", "evidence": []}]), active_case_id="CASE_0042", allowed_experiments={"SNAPSHOT_DIFF"})
    response = validate_control_response(payload(hypotheses=[{"id": "H1", "title": "Source", "status": "SUPPORTED", "evidence": ["Visible row evidence"]}]), active_case_id="CASE_0042", allowed_experiments={"SNAPSHOT_DIFF"})
    assert response.hypotheses[0].status.value == "SUPPORTED"


def test_unknown_hypothesis_id_is_rejected_for_active_case():
    with pytest.raises(ValueError, match="unknown hypothesis"):
        validate_control_response(payload(hypotheses=[{"id": "H9", "title": "Unknown", "status": "POSSIBLE", "evidence": []}]), active_case_id="CASE_0042", allowed_experiments={"SNAPSHOT_DIFF"}, allowed_hypothesis_ids={"H1", "H2", "H3"})


def test_sql_control_text_is_rejected():
    with pytest.raises(ValueError, match="unsafe"):
        validate_control_response(payload(observation="SELECT secret FROM case_truth"), active_case_id="CASE_0042", allowed_experiments={"SNAPSHOT_DIFF"})
