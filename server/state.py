"""Server-authoritative investigation state machine."""
from __future__ import annotations

from enum import StrEnum


class InvestigationState(StrEnum):
    BRIEFING = "BRIEFING"
    INVESTIGATION = "INVESTIGATION"
    EXPERIMENT_RESULT = "EXPERIMENT_RESULT"
    VERDICT = "VERDICT"
    DEBRIEF = "DEBRIEF"
    ERROR = "ERROR"


TRANSITIONS: dict[InvestigationState, frozenset[InvestigationState]] = {
    InvestigationState.BRIEFING: frozenset({InvestigationState.INVESTIGATION, InvestigationState.ERROR}),
    InvestigationState.INVESTIGATION: frozenset({InvestigationState.EXPERIMENT_RESULT, InvestigationState.VERDICT, InvestigationState.ERROR}),
    InvestigationState.EXPERIMENT_RESULT: frozenset({InvestigationState.INVESTIGATION, InvestigationState.EXPERIMENT_RESULT, InvestigationState.VERDICT, InvestigationState.ERROR}),
    InvestigationState.VERDICT: frozenset({InvestigationState.DEBRIEF}),
    InvestigationState.DEBRIEF: frozenset(),
    InvestigationState.ERROR: frozenset({InvestigationState.BRIEFING, InvestigationState.INVESTIGATION}),
}


def transition(current: str, target: InvestigationState) -> str:
    state = InvestigationState(current)
    if target not in TRANSITIONS[state]:
        raise ValueError(f"illegal investigation transition: {state} -> {target}")
    return target.value
