import pytest

from backend.domain.orchestration import DecisionOrchestrator
from backend.genie.decisions import make_pending_decision


def test_first_experiment_is_claimed_once_and_not_reselectable():
    service = DecisionOrchestrator()
    service.persist(make_pending_decision(
        message_id="m1", experiment_id="SNAPSHOT_DIFF", instrument_id="SNAPSHOT_DIFF",
        target="V2", allowed={"SNAPSHOT_DIFF"}, protocol_json='{"schema_version":"1.0"}',
    ))
    claimed = service.claim_first_experiment(current_allowed={"SNAPSHOT_DIFF"})
    assert claimed.experiment_id == "SNAPSHOT_DIFF"
    with pytest.raises(ValueError, match="no pending decision"):
        service.claim_first_experiment(current_allowed={"SNAPSHOT_DIFF"})


def test_stale_allowed_set_cannot_claim_pending_experiment():
    service = DecisionOrchestrator()
    service.persist(make_pending_decision(
        message_id="m1", experiment_id="SNAPSHOT_DIFF", instrument_id="SNAPSHOT_DIFF",
        target=None, allowed={"SNAPSHOT_DIFF"}, protocol_json='{}',
    ))
    with pytest.raises(ValueError, match="stale pending decision"):
        service.claim_first_experiment(current_allowed={"COMPONENT_DECOMPOSITION"})
