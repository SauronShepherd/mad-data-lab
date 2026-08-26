"""V3 MAD DATA LAB machine-control protocol.

This module deliberately does not share the legacy prototype parser in
``server.genie``.  Control responses are a strict, bounded interface: prose
may surround one JSON object, but prose is never itself machine control.
"""
from __future__ import annotations

import json
import re
from enum import StrEnum
from typing import Any, Callable

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class HypothesisStatus(StrEnum):
    CONFIRMED = "CONFIRMED"
    SUPPORTED = "SUPPORTED"
    POSSIBLE = "POSSIBLE"
    RULED_OUT = "RULED_OUT"


class Action(StrEnum):
    RUN_EXPERIMENT = "RUN_EXPERIMENT"
    INSPECT_EVIDENCE = "INSPECT_EVIDENCE"
    CONCLUDE = "CONCLUDE"
    REQUEST_MORE_EVIDENCE = "REQUEST_MORE_EVIDENCE"


class Instrument(StrEnum):
    WATERFALL = "WATERFALL"
    SNAPSHOT_DIFF = "SNAPSHOT_DIFF"
    DQ_PANEL = "DQ_PANEL"
    FORMULA_CHECK = "FORMULA_CHECK"
    RECONCILIATION = "RECONCILIATION"


_UNSAFE_CONTROL = re.compile(r"<\s*script|on[a-z]+\s*=|javascript:|```(?:python|sql|bash)|\b(?:select|insert|update|delete|drop)\s+.+\s+from\b", re.I | re.S)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Hypothesis(StrictModel):
    id: str = Field(pattern=r"^H[0-9]+$", max_length=16)
    title: str = Field(min_length=1, max_length=120)
    status: HypothesisStatus
    evidence: list[str] = Field(default_factory=list, max_length=8)

    @model_validator(mode="after")
    def require_evidence_for_assertive_status(self) -> "Hypothesis":
        if self.status in {HypothesisStatus.SUPPORTED, HypothesisStatus.CONFIRMED, HypothesisStatus.RULED_OUT} and not self.evidence:
            raise ValueError(f"{self.status.value} requires visible evidence")
        return self

    @field_validator("title", "evidence")
    @classmethod
    def reject_unsafe_text(cls, value: Any) -> Any:
        values = value if isinstance(value, list) else [value]
        if any(_UNSAFE_CONTROL.search(str(item)) or re.search(r"https?://", str(item), re.I) for item in values):
            raise ValueError("unsafe control text")
        return value


class SelectedExperiment(StrictModel):
    id: str = Field(pattern=r"^[A-Z][A-Z0-9_]+$", max_length=64)
    question: str = Field(min_length=1, max_length=240)
    target_component: str | None = Field(default=None, max_length=64)

    @field_validator("question", "target_component")
    @classmethod
    def reject_unsafe_selection_text(cls, value: str | None) -> str | None:
        if value is not None and (_UNSAFE_CONTROL.search(value) or re.search(r"https?://", value, re.I)):
            raise ValueError("unsafe control text")
        return value


class InstrumentSelection(StrictModel):
    id: Instrument
    title: str = Field(min_length=1, max_length=160)

    @field_validator("title")
    @classmethod
    def reject_unsafe_title(cls, value: str) -> str:
        if _UNSAFE_CONTROL.search(value) or re.search(r"https?://", value, re.I):
            raise ValueError("unsafe control text")
        return value


class ControlResponse(StrictModel):
    schema_version: str = Field(pattern=r"^1\.0$")
    case_id: str = Field(pattern=r"^CASE_[0-9]{4}$")
    observation: str = Field(min_length=1, max_length=500)
    hypotheses: list[Hypothesis] = Field(min_length=1, max_length=8)
    selected_experiment: SelectedExperiment | None = None
    instrument: InstrumentSelection | None = None
    next_action: Action
    scientist_line: str = Field(min_length=1, max_length=300)

    @field_validator("observation", "scientist_line")
    @classmethod
    def reject_unsafe_strings(cls, value: str) -> str:
        if _UNSAFE_CONTROL.search(value) or re.search(r"https?://", value, re.I):
            raise ValueError("unsafe control text")
        return value

    @model_validator(mode="after")
    def validate_action_shape(self) -> "ControlResponse":
        hypothesis_ids = [item.id for item in self.hypotheses]
        if len(hypothesis_ids) != len(set(hypothesis_ids)):
            raise ValueError("duplicate hypothesis IDs")
        if self.next_action == Action.RUN_EXPERIMENT:
            if self.selected_experiment is None or self.instrument is None:
                raise ValueError("RUN_EXPERIMENT requires selected_experiment and instrument")
        elif self.next_action == Action.CONCLUDE and (self.selected_experiment is not None or self.instrument is not None):
            raise ValueError("CONCLUDE cannot select an experiment or instrument")
        return self


def extract_control_object(text: str) -> dict[str, Any]:
    """Extract exactly one accepted control object from final-answer text.

    Accepted forms are the entire trimmed JSON object, or one fenced ``json``
    block.  A greedy scan through arbitrary prose is intentionally forbidden.
    """
    trimmed = text.strip()
    if not trimmed:
        raise ValueError("empty Genie response")
    try:
        direct = json.loads(trimmed)
    except json.JSONDecodeError:
        direct = None
    if isinstance(direct, dict):
        return direct
    if direct is not None:
        raise ValueError("control response must be a JSON object")
    matches = list(re.finditer(r"```[ \t]*json[ \t]*\r?\n(.*?)\r?\n```", trimmed, re.I | re.S))
    if len(matches) != 1:
        raise ValueError("expected exactly one fenced JSON control object")
    before = trimmed[: matches[0].start()].strip()
    after = trimmed[matches[0].end() :].strip()
    # Surrounding player-facing prose is allowed, but another JSON candidate is not.
    if re.search(r"```|\{.*\}", before, re.S) or re.search(r"```|\{.*\}", after, re.S):
        raise ValueError("ambiguous multiple control objects")
    try:
        value = json.loads(matches[0].group(1))
    except json.JSONDecodeError as exc:
        raise ValueError("invalid fenced JSON control object") from exc
    if not isinstance(value, dict):
        raise ValueError("control response must be a JSON object")
    return value


def validate_control_response(
    value: dict[str, Any] | str,
    *,
    active_case_id: str,
    allowed_experiments: set[str],
    completed_experiments: set[str] | None = None,
    instrument_for_experiment: Callable[[str], set[str]] | None = None,
    target_required: Callable[[str], bool] | None = None,
    valid_targets: Callable[[str], set[str]] | None = None,
    allowed_hypothesis_ids: set[str] | None = None,
) -> ControlResponse:
    payload = extract_control_object(value) if isinstance(value, str) else value
    response = ControlResponse.model_validate(payload)
    if response.case_id != active_case_id:
        raise ValueError("wrong active Case ID")
    if allowed_hypothesis_ids is not None:
        actual_hypotheses = {item.id for item in response.hypotheses}
        unknown_hypotheses = actual_hypotheses - allowed_hypothesis_ids
        if unknown_hypotheses:
            raise ValueError("unknown hypothesis ID")
    completed = completed_experiments or set()
    if response.next_action == Action.RUN_EXPERIMENT:
        assert response.selected_experiment is not None
        assert response.instrument is not None
        experiment_id = response.selected_experiment.id
        if experiment_id not in allowed_experiments:
            raise ValueError("Experiment is not currently allowed")
        if experiment_id in completed:
            raise ValueError("Experiment is already complete")
        if instrument_for_experiment and response.instrument.id.value not in instrument_for_experiment(experiment_id):
            raise ValueError("Instrument is not legal for this Experiment")
        if target_required and target_required(experiment_id) and not response.selected_experiment.target_component:
            raise ValueError("Experiment requires a target component")
        if response.selected_experiment.target_component and valid_targets:
            if response.selected_experiment.target_component not in valid_targets(experiment_id):
                raise ValueError("target component is not allowed for this Experiment")
    return response
