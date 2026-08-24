"""Deterministic, synthetic analytical domain for MAD DATA LAB.

The generator intentionally keeps private truth in a separate object.  Public
curated projections are built explicitly and never serialize that object.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Any


STATUSES = frozenset({"CONFIRMED", "SUPPORTED", "POSSIBLE", "RULED_OUT"})
EXPERIMENTS = frozenset({"COMPONENT_DECOMPOSITION", "SNAPSHOT_DIFF", "RECONCILIATION"})
INSTRUMENTS = frozenset({"WATERFALL", "SNAPSHOT_DIFF", "EVIDENCE_TABLE", "DQ_PANEL", "LINEAGE_GRAPH", "RECONCILIATION"})

CASE_SPECS: dict[str, dict[str, Any]] = {
    "CASE_0042": {"seed": 42, "expected": 125.0, "observed": 118.2, "primary_component": "V2", "primary_cause": "SOURCE_RECORD_CHANGE"},
    "CASE_0107": {"seed": 107, "expected": 42.0, "observed": 43.8, "primary_component": None, "primary_cause": "DUPLICATE_INGESTION"},
    "CASE_0213": {"seed": 213, "expected": 41.2, "observed": 34.7, "primary_component": None, "primary_cause": "FILTER_CHANGE"},
    "CASE_0314": {"seed": 314, "expected": 78.6, "observed": 73.4, "primary_component": None, "primary_cause": "MISSING_RECORDS"},
    "CASE_0441": {"seed": 441, "expected": 52.4, "observed": 45.0, "primary_component": None, "primary_cause": "SOURCE_RECORD_CHANGE"},
    "CASE_0520": {"seed": 520, "expected": 46.0, "observed": 83.0, "primary_component": None, "primary_cause": "JOIN_CARDINALITY"},
    "CASE_0812": {"seed": 812, "expected": 90.0, "observed": 83.8, "primary_component": None, "primary_cause": "MULTI_CAUSE"},
}


@dataclass(frozen=True)
class Component:
    component_id: str
    label: str
    previous: float
    current: float

    @property
    def delta(self) -> float:
        # V3 is a subtractive term in Capital Available = V1 + V2 - V3 + V4.
        raw = self.current - self.previous
        return round(-raw if self.component_id == "V3" else raw, 2)


@dataclass(frozen=True)
class SnapshotRecord:
    business_key: str
    old_value: float | None
    new_value: float | None
    change_type: str

    @property
    def impact(self) -> float:
        return round((self.new_value or 0.0) - (self.old_value or 0.0), 2)


@dataclass(frozen=True)
class CaseTruth:
    primary_component: str
    primary_cause: str
    formula_ids_equal: bool
    formula_hashes_equal: bool


@dataclass(frozen=True)
class CaseFixture:
    case_id: str
    seed: int
    generator_version: int
    expected: float
    observed: float
    components: tuple[Component, ...]
    records: tuple[SnapshotRecord, ...]
    dq_affected_rows: int
    dq_estimated_impact: float
    dq_overlap: bool
    truth: CaseTruth

    @property
    def deviation(self) -> float:
        return round(self.observed - self.expected, 2)

    @property
    def component_total(self) -> float:
        return round(sum(c.delta for c in self.components), 2)

    @property
    def snapshot_total(self) -> float:
        return round(sum(r.impact for r in self.records), 2)

    def curated_projection(self) -> dict[str, Any]:
        """Return only Genie-facing evidence; never include ``truth``."""
        return {
            "case_id": self.case_id,
            "seed": self.seed,
            "generator_version": self.generator_version,
            "observation": {"expected": self.expected, "observed": self.observed, "deviation": self.deviation, "unit": "EUR_M"},
            "components": [asdict(c) | {"delta": c.delta} for c in self.components],
            "snapshot": {
                "modified": sum(r.change_type == "MODIFIED" for r in self.records),
                "removed": sum(r.change_type == "REMOVED" for r in self.records),
                "added": sum(r.change_type == "ADDED" for r in self.records),
                "impact": self.snapshot_total,
            },
            "records": [asdict(r) | {"impact": r.impact} for r in sorted(self.records, key=lambda item: item.business_key)],
            "quality": {"affected_rows": self.dq_affected_rows, "estimated_impact": self.dq_estimated_impact, "overlap": self.dq_overlap},
            "formula": {"ids_equal": self.truth.formula_ids_equal, "hashes_equal": self.truth.formula_hashes_equal},
            "lineage": [{"node_type": "METRIC", "node_id": "CAPITAL_AVAILABLE"}, {"node_type": "COMPONENT", "node_id": "V2"}, {"node_type": "SOURCE_RECORD", "node_id": "TX-004291"}],
        }


def _records() -> tuple[SnapshotRecord, ...]:
    records = [SnapshotRecord(f"TX-{i:06d}", 1.0, 1.0, "MODIFIED") for i in range(1, 24)]
    records[0] = SnapshotRecord("TX-004291", 4.2, 0.0, "MODIFIED")
    # The remaining modified rows sum to -1.0, for a modified total of -5.2.
    records[1] = SnapshotRecord("TX-000002", 1.0, 0.0, "MODIFIED")
    records[2] = SnapshotRecord("TX-000003", 1.0, 1.0, "MODIFIED")
    records.extend((SnapshotRecord("TX-000024", 0.4, None, "REMOVED"), SnapshotRecord("TX-000025", 0.4, None, "REMOVED")))
    records.extend((SnapshotRecord("TX-000026", None, 0.05, "ADDED"), SnapshotRecord("TX-000027", None, 0.05, "ADDED"), SnapshotRecord("TX-000028", None, 0.0, "ADDED"), SnapshotRecord("TX-000029", None, 0.0, "ADDED"), SnapshotRecord("TX-000030", None, 0.0, "ADDED")))
    return tuple(records)


def generate_case(case_id: str = "CASE_0042", seed: int = 42, version: int = 2) -> CaseFixture:
    spec = CASE_SPECS.get(case_id)
    if spec is None:
        raise ValueError(f"Unknown case fixture: {case_id}")
    if case_id != "CASE_0042" or seed != 42 or version != 2:
        # Non-demo cases use exact catalog observations and a deterministic
        # evidence row so every Case has a materialized analytical contract.
        expected = float(spec["expected"])
        observed = float(spec["observed"])
        deviation = round(observed - expected, 2)
        if deviation < 0:
            records = (SnapshotRecord(f"{case_id}-PRIMARY", abs(deviation), 0.0, "REMOVED"),)
        else:
            records = (SnapshotRecord(f"{case_id}-PRIMARY", 0.0, deviation, "ADDED"),)
        # Materialize a minimal component ledger for every catalog Case so the
        # same reconciliation invariant applies to the full game, not only the
        # challenge fixture.
        generic_components: tuple[Component, ...] = (Component("PRIMARY", "Primary anomaly movement", 0.0, deviation),)
        return CaseFixture(case_id, seed if seed != 42 else int(spec["seed"]), version, expected, observed, generic_components, records, 0, 0.0, False, CaseTruth(str(spec["primary_component"] or "NONE"), str(spec["primary_cause"]), True, True))
    demo_components: tuple[Component, ...] = (Component("V1", "Core balance", 100.1, 98.9), Component("V2", "Promotional reserve", 30.0, 24.1), Component("V3", "Offset", 5.1, 4.8), Component("V4", "Stable adjustment", 0.0, 0.0))
    return CaseFixture("CASE_0042", 42, 2, 125.0, 118.2, demo_components, _records(), 5, -0.3, True, CaseTruth("V2", "SOURCE_RECORD_CHANGE", True, True))


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def fixture_hash(fixture: CaseFixture) -> str:
    return sha256(canonical_json(fixture.curated_projection()).encode()).hexdigest()


def validate_fixture(fixture: CaseFixture) -> None:
    if round(fixture.component_total - fixture.deviation, 2) != 0:
        raise ValueError("component reconciliation failed")
    if fixture.case_id == "CASE_0042" and round(fixture.snapshot_total, 2) != -5.9:
        raise ValueError("snapshot reconciliation failed")
    if len({r.business_key for r in fixture.records}) != len(fixture.records):
        raise ValueError("duplicate business key")
