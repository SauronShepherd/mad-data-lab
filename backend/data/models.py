from __future__ import annotations

from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class ObservationResult(BaseModel):
    model_config = ConfigDict(extra='forbid')
    case_id: str
    datapoint_id: str
    entity_id: str
    period_id: str
    expected_value: Decimal
    observed_value: Decimal
    deviation: Decimal
    formula_id: str
    formula_hash: str

class ComponentResult(BaseModel):
    model_config = ConfigDict(extra='forbid')
    component: str
    previous_value: Decimal
    current_value: Decimal
    contribution_delta: Decimal
    abs_contribution: Decimal = Field(default=Decimal('0.00'))
    share_of_abs_deviation: Decimal = Field(default=Decimal('0.00'))
    abs_contribution_rank: int = 0

class SnapshotGroup(BaseModel):
    model_config = ConfigDict(extra='forbid')
    case_id: str
    component: str
    change_type: str
    record_count: int
    total_impact: Decimal

class FormulaValidationResult(BaseModel):
    model_config = ConfigDict(extra='forbid')
    case_id: str
    previous_formula_id: str
    current_formula_id: str
    previous_formula_hash: str
    current_formula_hash: str
    formula_changed: bool

class SourceRecordResult(BaseModel):
    model_config = ConfigDict(extra='forbid')
    business_key: str
    component: str
    old_value: Decimal | None = None
    new_value: Decimal | None = None
    impact: Decimal
    change_type: str

class QualityResult(BaseModel):
    model_config = ConfigDict(extra='forbid')
    issue_id: str
    rule_name: str
    affected_keys: list[str]
    affected_row_count: int
    estimated_impact: Decimal
    impact_is_overlapping: bool
    severity: str = 'MEDIUM'
    deviation_share: Decimal | None = None

class LineageResult(BaseModel):
    model_config = ConfigDict(extra='forbid')
    case_id: str
    node_id: str
    node_type: str
    parent_node_id: str | None = None
    sequence_no: int

class ReconciliationResult(BaseModel):
    model_config = ConfigDict(extra='forbid')
    case_id: str
    expected_deviation: Decimal
    reconciled_deviation: Decimal
    residual: Decimal
