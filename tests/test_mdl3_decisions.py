import pytest

from backend.genie.decisions import PendingDecisionStore, make_pending_decision


def test_pending_decision_is_not_consumed_until_next_action():
    allowed = {"COMPONENT_DECOMPOSITION", "SNAPSHOT_DIFF"}
    decision = make_pending_decision(message_id="m1", experiment_id="COMPONENT_DECOMPOSITION", instrument_id="WATERFALL", target=None, allowed=allowed, protocol_json='{"schema_version":"1.0"}')
    store = PendingDecisionStore()
    store.put(decision)
    assert store.peek() == decision
    assert store.consume(current_allowed=allowed) == decision
    assert store.peek() is None


def test_stale_pending_decision_is_rejected_and_concurrent_put_is_blocked():
    allowed = {"SNAPSHOT_DIFF"}
    decision = make_pending_decision(message_id="m1", experiment_id="SNAPSHOT_DIFF", instrument_id="SNAPSHOT_DIFF", target="V2", allowed=allowed, protocol_json='{}')
    store = PendingDecisionStore()
    store.put(decision)
    with pytest.raises(ValueError, match="stale"):
        store.consume(current_allowed={"FORMULA_VALIDATION"})
    with pytest.raises(ValueError, match="already exists"):
        store.put(decision)
