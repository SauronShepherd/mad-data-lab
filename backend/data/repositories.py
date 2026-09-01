from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from data.generation import generate_case
from .models import ComponentResult, QualityResult, SourceRecordResult
from .queries import QUERIES, get_query
from .sql_client import connect_from_env, execute_native, validate_case_id
from backend.genie.query_registry import validate_result

ROOT = Path(__file__).resolve().parents[2]

class EvidenceRepository:
    """Public/curated repository. It has no dependency on private truth."""
    def components(self, case_id: str) -> list[ComponentResult]:
        case = generate_case(case_id)
        return [ComponentResult(component=x['component'], previous_value=x['previous_value'], current_value=x['current_value'], contribution_delta=x['contribution_delta']) for x in case.public['component_evidence']]

    def records(self, case_id: str, *, limit: int = 100, business_key: str | None = None) -> list[SourceRecordResult]:
        if not 1 <= limit <= 100: raise ValueError('limit must be between 1 and 100')
        case = generate_case(case_id)
        rows = case.public['snapshot_evidence']
        if business_key is not None: rows = [x for x in rows if x['business_key'] == business_key]
        return [SourceRecordResult(**x) for x in sorted(rows, key=lambda x: x['business_key'])[:limit]]

    def quality(self, case_id: str) -> list[QualityResult]:
        case = generate_case(case_id)
        return [QualityResult(**x) for x in case.public['quality_evidence']]


class SqlEvidenceRepository:
    """Production evidence repository backed only by registered curated SQL."""

    source = "databricks_sql"

    def _query(self, query_id: str, case_id: str, *, limit: int | None = None) -> list[dict[str, Any]]:
        validate_case_id(case_id)
        spec = get_query(query_id)
        sql_path = ROOT / "sql" / "trusted" / spec.sql_path
        sql = sql_path.read_text(encoding="utf-8").replace("{{CURATED}}", _curated_schema())
        params: tuple[Any, ...] = (case_id, limit) if spec.parameter_names == ("case_id", "limit") else (case_id,)
        with connect_from_env() as connection:
            cursor = connection.cursor()
            execute_native(cursor, sql, params)
            columns = [str(getattr(item, "name", item)).strip().lower() for item in (cursor.description or ())]
            rows = cursor.fetchall()
        result = [dict(zip(columns, row)) for row in rows]
        # Some Databricks SQL result metadata paths can expose the filtered
        # view's case_id as NULL after a SELECT * over a joined view. The
        # predicate above already binds the result to the requested case;
        # restore that transport-only field before the closed-registry check.
        for row in result:
            if row.get("case_id") is None:
                row["case_id"] = case_id
        return validate_result(_query_registry_name(query_id), case_id=case_id, rows=result)

    def components(self, case_id: str) -> list[ComponentResult]:
        rows = self._query("Q2", case_id)
        return [ComponentResult(component=row["component"], previous_value=row["previous_value"], current_value=row["current_value"], contribution_delta=row["contribution_delta"], abs_contribution=row.get("abs_contribution", 0), share_of_abs_deviation=row.get("share_of_abs_deviation", 0), abs_contribution_rank=row.get("abs_contribution_rank", 0)) for row in rows]

    def records(self, case_id: str, *, limit: int = 100, business_key: str | None = None) -> list[SourceRecordResult]:
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        # Apply the business-key predicate after retrieving the bounded public
        # snapshot set; otherwise a requested key outside the top-N impact
        # window can be reported as missing even though it is valid evidence.
        rows = self._query("Q4", case_id, limit=100 if business_key is not None else limit)
        if business_key is not None:
            rows = [row for row in rows if row.get("business_key") == business_key]
        return [SourceRecordResult(business_key=row["business_key"], component=row["component"], old_value=row.get("old_value"), new_value=row.get("new_value"), impact=row["impact"], change_type=row["change_type"]) for row in rows[:limit]]

    def quality(self, case_id: str) -> list[QualityResult]:
        rows = self._query("Q5", case_id)
        return [QualityResult(issue_id=row["issue_id"], rule_name=row["rule_name"], affected_keys=row["affected_keys"], affected_row_count=row["affected_row_count"], estimated_impact=row["estimated_impact"], impact_is_overlapping=row["impact_is_overlapping"], severity=row.get("severity", "MEDIUM"), deviation_share=row.get("deviation_share")) for row in rows]

    def experiment_payload(self, experiment: Any, index: int, case_id: str) -> dict[str, Any]:
        """Build the user-visible instrument model from curated SQL only."""
        observation = self._query("Q1", case_id)[0]
        # Accommodate connector aliases emitted by older curated-view
        # snapshots while retaining the same curated SQL source.
        expected_value = observation.get("expected_value", observation.get("expected"))
        observed_value = observation.get("observed_value", observation.get("observed"))
        model: dict[str, Any] = {"expected": float(expected_value), "observed": float(observed_value), "deviation": float(observation["deviation"])}
        if experiment.instrument == "WATERFALL":
            model["components"] = [{"component_id": row.component, "label": row.component, "delta": float(row.contribution_delta)} for row in self.components(case_id)]
        elif experiment.instrument == "SNAPSHOT_DIFF":
            rows = self.records(case_id, limit=100)
            model["groups"] = [{"change_type": kind, "count": sum(row.change_type == kind for row in rows), "impact": round(sum(float(row.impact) for row in rows if row.change_type == kind), 2)} for kind in ("MODIFIED", "REMOVED", "ADDED")]
            model["net_impact"] = round(sum(float(row.impact) for row in rows), 2)
        elif experiment.instrument == "EVIDENCE_TABLE":
            model["records"] = [row.model_dump() for row in self.records(case_id, limit=100)]
        elif experiment.instrument == "DQ_PANEL":
            quality = self.quality(case_id)[0]
            model.update({"rule_name": quality.rule_name, "severity": quality.severity, "affected_rows": quality.affected_row_count, "estimated_impact": float(quality.estimated_impact), "overlap": quality.impact_is_overlapping})
        elif experiment.instrument in {"FORMULA_CHECK", "FORMULA_DIFF"}:
            model.update(self._query("Q6", case_id)[0])
        return {"case_id": case_id, "experiment_id": experiment.id, "experiment_number": index + 1, "name": experiment.name, "instrument": experiment.instrument, "rationale": experiment.rationale, "evidence": "Curated Databricks SQL evidence loaded for this instrument.", "hypothesis_updates": [{"name": n, "status": s} for n, s in experiment.updates], "instrument_model": model, "source": self.source}


def _curated_schema() -> str:
    catalog = os.getenv("MDL_CATALOG", "workspace")
    schema = os.getenv("MDL_CURATED_SCHEMA", "mad_data_lab_curated")
    for value in (catalog, schema):
        if not value.replace("_", "a").isalnum() or not value[0].isalpha():
            raise ValueError("invalid curated SQL schema configuration")
    return f"{catalog}.{schema}"


def _query_registry_name(query_id: str) -> str:
    return {"Q1": "case_summary", "Q2": "component_evidence", "Q4": "snapshot_evidence", "Q5": "quality_evidence", "Q6": "formula_validation"}[query_id]
