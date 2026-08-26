"""Atomic pending first-Experiment decision primitives."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from threading import Lock


@dataclass(frozen=True)
class PendingDecision:
    message_id: str
    experiment_id: str
    instrument_id: str
    target: str | None
    allowed_set_digest: str
    protocol_sha256: str
    created_at: str


def allowed_set_digest(allowed: set[str]) -> str:
    return sha256(json.dumps(sorted(allowed), separators=(",", ":")).encode()).hexdigest()


def make_pending_decision(*, message_id: str, experiment_id: str, instrument_id: str, target: str | None, allowed: set[str], protocol_json: str) -> PendingDecision:
    return PendingDecision(
        message_id=message_id,
        experiment_id=experiment_id,
        instrument_id=instrument_id,
        target=target,
        allowed_set_digest=allowed_set_digest(allowed),
        protocol_sha256=sha256(protocol_json.encode()).hexdigest(),
        created_at=datetime.now(timezone.utc).isoformat(),
    )


class PendingDecisionStore:
    """Small atomic store abstraction; production can replace backing storage."""

    def __init__(self) -> None:
        self._value: PendingDecision | None = None
        self._lock = Lock()

    def put(self, decision: PendingDecision) -> None:
        with self._lock:
            if self._value is not None:
                raise ValueError("pending decision already exists")
            self._value = decision

    def peek(self) -> PendingDecision | None:
        with self._lock:
            return self._value

    def consume(self, *, current_allowed: set[str]) -> PendingDecision:
        with self._lock:
            if self._value is None:
                raise ValueError("no pending decision")
            decision = self._value
            if decision.allowed_set_digest != allowed_set_digest(current_allowed):
                raise ValueError("stale pending decision")
            self._value = None
            return decision
