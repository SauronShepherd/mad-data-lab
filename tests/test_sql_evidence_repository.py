from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from backend.data.repositories import SqlEvidenceRepository


class _Cursor:
    description = [SimpleNamespace(name="case_id"), SimpleNamespace(name="business_key"), SimpleNamespace(name="component"), SimpleNamespace(name="old_value"), SimpleNamespace(name="new_value"), SimpleNamespace(name="impact"), SimpleNamespace(name="change_type")]

    def __init__(self):
        self.calls = []

    def execute(self, sql, params):
        self.calls.append((sql, params))

    def fetchall(self):
        return [["CASE_0042", "TX-004291", "V2", Decimal("4.20"), Decimal("0.00"), Decimal("-4.20"), "MODIFIED"]]


class _Connection:
    def __init__(self, cursor):
        self._cursor = cursor

    def cursor(self):
        return self._cursor

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_sql_repository_uses_registered_native_query_and_validates_public_rows():
    cursor = _Cursor()
    with patch("backend.data.repositories.connect_from_env", return_value=_Connection(cursor)):
        rows = SqlEvidenceRepository().records("CASE_0042", limit=10)
    assert rows[0].business_key == "TX-004291"
    sql, params = cursor.calls[0]
    assert "snapshot_evidence" in sql
    assert "?" in sql and params == ("CASE_0042", 10)
    assert "CASE_0042' OR" not in sql


def test_production_repository_has_no_generator_dependency_on_user_visible_path():
    repo = SqlEvidenceRepository()
    with patch("backend.data.repositories.generate_case", side_effect=AssertionError("generator used in production")):
        cursor = _Cursor()
        with patch("backend.data.repositories.connect_from_env", return_value=_Connection(cursor)):
            repo.records("CASE_0042", limit=1)
