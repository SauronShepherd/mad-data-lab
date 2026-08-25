from __future__ import annotations

from data.generation import generate_case
from .models import ComponentResult, QualityResult, SourceRecordResult

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
