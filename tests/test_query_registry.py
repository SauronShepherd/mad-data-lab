import pytest

from backend.genie.query_registry import render_query, resolve_query, validate_reconciliation, validate_result


def test_trusted_query_is_closed_case_scoped_and_bounded():
    query = render_query("snapshot_evidence", case_id="CASE_0042")
    assert "snapshot_evidence" in query
    assert "workspace.mad_data_lab_curated" in query
    assert "CASE_0042" in query
    assert "LIMIT 50" in query
    assert validate_result("snapshot_evidence", case_id="CASE_0042", rows=[{"case_id": "CASE_0042", "business_key": "TX-1", "impact": -5.9}])


def test_arbitrary_query_and_cross_case_result_are_rejected():
    with pytest.raises(ValueError):
        resolve_query("SELECT * FROM case_truth")
    with pytest.raises(ValueError):
        render_query("snapshot_evidence", case_id="CASE_0042' OR '1'='1")
    with pytest.raises(ValueError, match="Case boundary"):
        validate_result("snapshot_evidence", case_id="CASE_0042", rows=[{"case_id": "CASE_0107"}])
    with pytest.raises(ValueError, match="row cap"):
        validate_result("snapshot_evidence", case_id="CASE_0042", rows=[{"case_id": "CASE_0042", "business_key": "TX-1", "impact": -5.9}] * 51)


def test_empty_and_wrong_column_results_fail_closed():
    with pytest.raises(ValueError, match="empty"):
        validate_result("snapshot_evidence", case_id="CASE_0042", rows=[])
    with pytest.raises(ValueError, match="schema"):
        validate_result("snapshot_evidence", case_id="CASE_0042", rows=[{"case_id": "CASE_0042"}])


def test_reconciliation_mismatch_fails_closed_with_tolerance():
    validate_reconciliation(expected="-6.80", reconciled="-6.805", tolerance="0.01")
    with pytest.raises(ValueError, match="residual"):
        validate_reconciliation(expected="-6.80", reconciled="-6.60")
