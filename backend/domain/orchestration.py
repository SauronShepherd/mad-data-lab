"""Domain-level orchestration for the first pending Experiment decision."""
from __future__ import annotations

from dataclasses import dataclass

from backend.genie.decisions import PendingDecision, PendingDecisionStore


@dataclass(frozen=True)
class ClaimedExperiment:
    """The only selection data routes may use after an atomic claim."""

    experiment_id: str
    instrument_id: str
    target: str | None
    message_id: str


class DecisionOrchestrator:
    """Keep pending-decision rules independent from transport handlers."""

    def __init__(self, store: PendingDecisionStore | None = None) -> None:
        self.store = store or PendingDecisionStore()

    def persist(self, decision: PendingDecision) -> None:
        self.store.put(decision)

    def claim_first_experiment(self, *, current_allowed: set[str]) -> ClaimedExperiment:
        decision = self.store.consume(current_allowed=current_allowed)
        if decision.experiment_id not in current_allowed:
            # Defensive check for stores restored from an older implementation.
            raise ValueError("pending Experiment is not currently allowed")
        return ClaimedExperiment(
            experiment_id=decision.experiment_id,
            instrument_id=decision.instrument_id,
            target=decision.target,
            message_id=decision.message_id,
        )
