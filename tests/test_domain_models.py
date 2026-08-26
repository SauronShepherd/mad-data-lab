import pytest
from pydantic import ValidationError

from backend.domain import Case, Evidence, Experiment, Hypothesis, HypothesisStatus, HypothesisUpdate, Investigation, Instrument, ScientificVerdict


def test_domain_models_use_canonical_vocabulary():
    case = Case(
        id="CASE_0042", number=42, title="The Missing €6.8M", metric="Capital Available",
        state="CORE", playable=True, hypotheses=["H1", "H2", "H3"],
        required_experiments=["COMPONENT_DECOMPOSITION", "RECONCILIATION"],
    )
    assert case.number == 42
    assert Experiment(id="COMPONENT_DECOMPOSITION", instrument="WATERFALL", question="Which component moved?").id == "COMPONENT_DECOMPOSITION"
    assert Instrument(id="WATERFALL", title="Component waterfall", query_id="component_evidence", row_cap=50).row_cap == 50
    assert Investigation(id="session-1", case_id="CASE_0042").state == "CATALOG"
    assert HypothesisUpdate(hypothesis_id="H1", status=HypothesisStatus.POSSIBLE).status == HypothesisStatus.POSSIBLE
    assert Hypothesis(id="H1", title="Source record change").status == HypothesisStatus.POSSIBLE
    assert ScientificVerdict(case_id="CASE_0042", conclusion="Pending evidence", confidence=0, evidence_ids=["E1"]).case_id == "CASE_0042"


def test_domain_models_reject_unknown_fields_and_invalid_ids():
    with pytest.raises(ValidationError):
        Evidence(id="bad id", kind="table", summary="x", source="curated", private_field="no")


def test_case_rejects_identity_and_release_contradictions():
    values = dict(id="CASE_0042", number=42, title="Case", metric="Metric", hypotheses=["H1"], required_experiments=["RECONCILIATION"])
    with pytest.raises(ValidationError, match="playability"):
        Case(**values, state="COMING_SOON", playable=True)
    with pytest.raises(ValidationError, match="number"):
        Case(**(values | {"number": 43}), state="CORE", playable=True)
