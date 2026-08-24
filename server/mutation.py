"""Deterministic synthetic mutation operators used by Case generators/tests."""
from __future__ import annotations

from dataclasses import replace
from enum import StrEnum

from .domain import SnapshotRecord


class MutationOperator(StrEnum):
    VALUE_CHANGE = "VALUE_CHANGE"
    MISSING_ROWS = "MISSING_ROWS"
    NEW_ROWS = "NEW_ROWS"
    DUPLICATE_KEYS = "DUPLICATE_KEYS"
    FORMULA_CHANGE = "FORMULA_CHANGE"
    FILTER_CHANGE = "FILTER_CHANGE"
    ENTITY_MIX = "ENTITY_MIX"
    JOIN_CARDINALITY = "JOIN_CARDINALITY"
    PIPELINE_REPLAY = "PIPELINE_REPLAY"
    MULTI_CAUSE = "MULTI_CAUSE"


def mutate_records(records: tuple[SnapshotRecord, ...], operator: MutationOperator, seed: int) -> tuple[SnapshotRecord, ...]:
    """Apply one closed, reproducible operator; no wall-clock/random state."""
    if operator == MutationOperator.VALUE_CHANGE:
        if not records: return records
        index = seed % len(records)
        item = records[index]
        return records[:index] + (replace(item, new_value=round((item.new_value or 0) + ((seed % 7) - 3) / 10, 2)),) + records[index + 1:]
    if operator == MutationOperator.MISSING_ROWS:
        return tuple(item for index, item in enumerate(records) if index % 5 != seed % 5)
    if operator == MutationOperator.NEW_ROWS:
        return records + (SnapshotRecord(f"TX-NEW-{seed:04d}", None, 0.1, "ADDED"),)
    if operator == MutationOperator.DUPLICATE_KEYS:
        if not records: return records
        return records + (replace(records[seed % len(records)], old_value=None, change_type="ADDED"),)
    # The remaining operators affect semantic metadata in full Case templates;
    # record-level data remains unchanged and therefore safe for this fixture.
    return records
