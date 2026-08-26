import pytest

from backend.genie.query_registry import render_query, resolve_query, validate_result


def test_trusted_query_is_closed_case_scoped_and_bounded():
    query = render_query("snapshot_evidence", case_id="CASE_0042")
    assert "snapshot_evidence" in query
    assert "CASE_0042" in query
    assert "LIMIT 50" in query
    assert validate_result("snapshot_evidence", case_id="CASE_0042", rows=[{"case_id": "CASE_0042", "impact": -5.9}])


def test_arbitrary_query_and_cross_case_result_are_rejected():
    with pytest.raises(ValueError):
        resolve_query("SELECT * FROM case_truth")
    with pytest.raises(ValueError):
        render_query("snapshot_evidence", case_id="CASE_0042' OR '1'='1")
    with pytest.raises(ValueError, match="Case boundary"):
        validate_result("snapshot_evidence", case_id="CASE_0042", rows=[{"case_id": "CASE_0107"}])
    with pytest.raises(ValueError, match="row cap"):
        validate_result("snapshot_evidence", case_id="CASE_0042", rows=[{"case_id": "CASE_0042"}] * 51)
