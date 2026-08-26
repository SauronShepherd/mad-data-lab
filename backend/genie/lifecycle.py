"""Bounded Genie turn lifecycle independent of the Databricks SDK."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Callable

from .protocol import ControlResponse, validate_control_response


class TurnFailure(StrEnum):
    PROTOCOL_INVALID_AFTER_REPAIR = "GENIE_PROTOCOL_INVALID_AFTER_REPAIR"
    QUERY_FAILED_AFTER_VALID_SELECTION = "GENIE_QUERY_FAILED_AFTER_VALID_SELECTION"
    TIMEOUT = "GENIE_TURN_TIMEOUT"


@dataclass(frozen=True)
class TurnResult:
    response: ControlResponse | None
    raw_response: str | None
    repair_count: int
    failure: TurnFailure | None = None
    query_result: Any = None


class GenieTurn:
    """Execute one protocol turn with exactly one repair opportunity.

    ``request`` and ``repair`` are injected callables so the same lifecycle is
    used by fixtures and the live Conversation API. The class never calls a
    trusted query until a valid Experiment has been selected and validated.
    """

    def __init__(
        self,
        *,
        active_case_id: str,
        allowed_experiments: set[str],
        instrument_for_experiment: Callable[[str], set[str]],
        request: Callable[[str | None], str],
        repair: Callable[[str], str],
        trusted_query: Callable[[ControlResponse], Any] | None = None,
    ) -> None:
        self.active_case_id = active_case_id
        self.allowed_experiments = allowed_experiments
        self.instrument_for_experiment = instrument_for_experiment
        self.request = request
        self.repair = repair
        self.trusted_query = trusted_query

    def run(self) -> TurnResult:
        raw = self.request(None)
        for repair_count in (0, 1):
            try:
                response = validate_control_response(
                    raw,
                    active_case_id=self.active_case_id,
                    allowed_experiments=self.allowed_experiments,
                    instrument_for_experiment=self.instrument_for_experiment,
                )
            except (TypeError, ValueError) as exc:
                if repair_count == 1:
                    return TurnResult(None, raw, repair_count, TurnFailure.PROTOCOL_INVALID_AFTER_REPAIR)
                raw = self.repair(f"Protocol violation: {exc}. Return one valid schema_version 1.0 object for {self.active_case_id}.")
                continue
            if response.next_action.value != "RUN_EXPERIMENT" or self.trusted_query is None:
                return TurnResult(response, raw, repair_count)
            try:
                query_result = self.trusted_query(response)
            except Exception:
                return TurnResult(response, raw, repair_count, TurnFailure.QUERY_FAILED_AFTER_VALID_SELECTION)
            return TurnResult(response, raw, repair_count, query_result=query_result)
        raise AssertionError("unreachable")
