"""Pure MDL-4 score projection for Case #042.

Scores are projections of append-only score-bearing events; callers never
provide points directly.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable, Mapping


class ScoreType(StrEnum):
    START_INVESTIGATION = "START_INVESTIGATION"
    INITIAL_PREDICTION_SUBMITTED = "INITIAL_PREDICTION_SUBMITTED"
    INITIAL_PREDICTION_CORRECT = "INITIAL_PREDICTION_CORRECT"
    REQUIRED_EXPERIMENT_COMPLETED = "REQUIRED_EXPERIMENT_COMPLETED"
    HIGH_VALUE_EVIDENCE_INSPECTED = "HIGH_VALUE_EVIDENCE_INSPECTED"
    REQUIRED_LINEAGE_OPENED = "REQUIRED_LINEAGE_OPENED"
    FINAL_PREDICTION_CORRECT = "FINAL_PREDICTION_CORRECT"
    FINISH_DEBRIEF = "FINISH_DEBRIEF"
    HINT_REVEALED = "HINT_REVEALED"
    EARLY_REVEAL = "EARLY_REVEAL"


POINTS: Mapping[str, int] = {
    ScoreType.START_INVESTIGATION: 50, ScoreType.INITIAL_PREDICTION_SUBMITTED: 50,
    ScoreType.INITIAL_PREDICTION_CORRECT: 100, ScoreType.REQUIRED_EXPERIMENT_COMPLETED: 100,
    ScoreType.HIGH_VALUE_EVIDENCE_INSPECTED: 100, ScoreType.REQUIRED_LINEAGE_OPENED: 75,
    ScoreType.FINAL_PREDICTION_CORRECT: 200, ScoreType.FINISH_DEBRIEF: 125,
    ScoreType.HINT_REVEALED: -50, ScoreType.EARLY_REVEAL: -150,
}


@dataclass(frozen=True)
class ScoreEvent:
    score_type: str
    eligibility_key: str
    sequence: int = 0


def reduce_score(events: Iterable[ScoreEvent | Mapping[str, object]]) -> int:
    seen: set[str] = set()
    total = 0
    experiment_count = 0
    for raw in sorted(events, key=lambda e: int(e.sequence if isinstance(e, ScoreEvent) else e.get("sequence", 0))):
        kind = raw.score_type if isinstance(raw, ScoreEvent) else str(raw.get("score_type", raw.get("type", "")))
        key = raw.eligibility_key if isinstance(raw, ScoreEvent) else str(raw.get("eligibility_key", kind))
        if key in seen or kind not in POINTS:
            continue
        if kind == ScoreType.REQUIRED_EXPERIMENT_COMPLETED:
            if experiment_count >= 3:
                continue
            experiment_count += 1
        seen.add(key)
        total += POINTS[kind]
    return max(0, min(1000, total))
