"""Stable, public domain vocabulary shared by API and orchestration layers."""
from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ExperimentId(StrEnum):
    COMPONENT_DECOMPOSITION = "COMPONENT_DECOMPOSITION"
    SNAPSHOT_DIFF = "SNAPSHOT_DIFF"
    DQ_MATERIALITY = "DQ_MATERIALITY"
    FORMULA_VALIDATION = "FORMULA_VALIDATION"
    RECONCILIATION = "RECONCILIATION"
    ROW_COUNT_ANALYSIS = "ROW_COUNT_ANALYSIS"
    DUPLICATE_KEY_ANALYSIS = "DUPLICATE_KEY_ANALYSIS"
    PIPELINE_RUN_COMPARISON = "PIPELINE_RUN_COMPARISON"
    FILTER_VALIDATION = "FILTER_VALIDATION"
    MISSING_RECORD_IMPACT = "MISSING_RECORD_IMPACT"
    ENTITY_COMPARISON = "ENTITY_COMPARISON"
    JOIN_CARDINALITY_ANALYSIS = "JOIN_CARDINALITY_ANALYSIS"


class InstrumentId(StrEnum):
    WATERFALL = "WATERFALL"
    SNAPSHOT_DIFF = "SNAPSHOT_DIFF"
    DQ_PANEL = "DQ_PANEL"
    FORMULA_CHECK = "FORMULA_CHECK"
    RECONCILIATION = "RECONCILIATION"


class InvestigationState(StrEnum):
    CATALOG = "CATALOG"
    BRIEFING = "BRIEFING"
    IN_PROGRESS = "IN_PROGRESS"
    CONCLUDED = "CONCLUDED"
    ERROR = "ERROR"


class HypothesisStatus(StrEnum):
    POSSIBLE = "POSSIBLE"
    SUPPORTED = "SUPPORTED"
    CONFIRMED = "CONFIRMED"
    RULED_OUT = "RULED_OUT"


class DomainModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Evidence(DomainModel):
    id: str = Field(pattern=r"^[A-Z][A-Z0-9_-]{1,63}$")
    kind: str = Field(min_length=1, max_length=64)
    summary: str = Field(min_length=1, max_length=500)
    source: str = Field(min_length=1, max_length=160)
    values: dict[str, Any] = Field(default_factory=dict)


class HypothesisUpdate(DomainModel):
    hypothesis_id: str = Field(pattern=r"^H[1-8]$")
    status: HypothesisStatus
    evidence_ids: list[str] = Field(default_factory=list, max_length=8)


class Hypothesis(DomainModel):
    id: str = Field(pattern=r"^H[1-8]$")
    title: str = Field(min_length=1, max_length=160)
    status: HypothesisStatus = HypothesisStatus.POSSIBLE
    evidence_ids: list[str] = Field(default_factory=list, max_length=8)


class Experiment(DomainModel):
    id: ExperimentId
    instrument: InstrumentId
    question: str = Field(min_length=1, max_length=240)
    target: str | None = Field(default=None, max_length=64)


class Instrument(DomainModel):
    id: InstrumentId
    title: str = Field(min_length=1, max_length=160)
    query_id: str = Field(pattern=r"^[a-z][a-z0-9_]{1,63}$")
    row_cap: int = Field(ge=1, le=100)


class Investigation(DomainModel):
    id: str = Field(pattern=r"^[A-Za-z0-9_-]{1,80}$")
    case_id: str = Field(pattern=r"^CASE_\d{4}$")
    state: InvestigationState = InvestigationState.CATALOG
    completed_experiment_ids: list[ExperimentId] = Field(default_factory=list, max_length=32)


class Case(DomainModel):
    id: str = Field(pattern=r"^CASE_\d{4}$")
    number: int = Field(ge=1, le=9999)
    title: str = Field(min_length=1, max_length=160)
    metric: str = Field(min_length=1, max_length=120)
    state: str = Field(min_length=1, max_length=32)
    playable: bool
    hypotheses: list[str] = Field(min_length=1, max_length=8)
    required_experiments: list[ExperimentId] = Field(min_length=1, max_length=32)
    expected: float | None = None
    observed: float | None = None
    deviation: float | None = None

    @model_validator(mode="after")
    def validate_identity_and_release(self) -> "Case":
        if f"CASE_{self.number:04d}" != self.id:
            raise ValueError("case number must match case id")
        if self.playable != (self.state == "CORE"):
            raise ValueError("playability must match CORE state")
        return self


class ScientificVerdict(DomainModel):
    case_id: str = Field(pattern=r"^CASE_\d{4}$")
    conclusion: str = Field(min_length=1, max_length=500)
    confidence: float = Field(ge=0, le=1)
    evidence_ids: list[str] = Field(min_length=1, max_length=32)
