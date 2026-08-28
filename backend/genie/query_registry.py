"""Closed trusted-query registry for validated Genie Experiment selections."""
from __future__ import annotations

from dataclasses import dataclass
import re
import os
from decimal import Decimal, InvalidOperation
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class TrustedQuery:
    query_id: str
    view: str
    row_cap: int
    required_case_filter: bool = True


TRUSTED_QUERIES = {
    "component_evidence": TrustedQuery("component_evidence", "component_evidence", 50),
    "snapshot_evidence": TrustedQuery("snapshot_evidence", "snapshot_evidence", 50),
    "quality_evidence": TrustedQuery("quality_evidence", "quality_evidence", 20),
    "semantic_evidence": TrustedQuery("semantic_evidence", "semantic_evidence", 20),
    "case_summary": TrustedQuery("case_summary", "case_summary", 20),
}

REQUIRED_RESULT_COLUMNS = {
    "component_evidence": {"case_id", "component", "contribution_delta"},
    "snapshot_evidence": {"case_id", "business_key", "impact"},
    "quality_evidence": {"case_id", "issue_id", "estimated_impact"},
    "semantic_evidence": {"case_id"},
    "case_summary": {"case_id"},
}


def resolve_query(query_id: str) -> TrustedQuery:
    try:
        return TRUSTED_QUERIES[query_id]
    except KeyError as exc:
        raise ValueError("query is not trusted") from exc


def render_query(query_id: str, *, case_id: str) -> str:
    query = resolve_query(query_id)
    if not re.fullmatch(r"CASE_[0-9]{4}", case_id):
        raise ValueError("invalid Case ID")
    # The view and query ID come exclusively from the closed registry; the
    # only interpolated value is a validated Case identifier.
    catalog = os.getenv("MDL_CATALOG", "workspace")
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", catalog):
        raise ValueError("invalid catalog")
    return f"SELECT * FROM {catalog}.mad_data_lab_curated.{query.view} WHERE case_id = '{case_id}' LIMIT {query.row_cap}"


def validate_result(query_id: str, *, case_id: str, rows: list[dict]) -> list[dict]:
    query = resolve_query(query_id)
    if len(rows) > query.row_cap:
        raise ValueError("trusted query result exceeds row cap")
    if not rows:
        raise ValueError("trusted query returned empty result")
    required = REQUIRED_RESULT_COLUMNS[query_id]
    for row in rows:
        if isinstance(row, dict) and row.get("case_id") != case_id:
            raise ValueError("trusted query result crossed Case boundary")
        if not isinstance(row, dict) or not required.issubset(row):
            raise ValueError("trusted query result schema mismatch")
    return rows


def validate_reconciliation(*, expected: str | Decimal, reconciled: str | Decimal,
                            tolerance: str | Decimal = "0.01") -> None:
    try:
        residual = abs(Decimal(str(reconciled)) - Decimal(str(expected)))
        allowed = Decimal(str(tolerance))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("reconciliation result is not numeric") from exc
    if residual > allowed:
        raise ValueError("reconciliation residual exceeds tolerance")
