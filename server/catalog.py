from __future__ import annotations

from dataclasses import asdict, dataclass
import re

from backend.domain.catalog import load_catalog


# Validate the canonical public artifact at the runtime boundary.  The legacy
# Python records below remain a compatibility projection until all secondary
# cases carry the complete accepted contract.
CANONICAL_PUBLIC_CATALOG = load_catalog()
DEFAULT_CASE_ID = next(item["id"] for item in CANONICAL_PUBLIC_CATALOG["cases"] if item["playable"])


CASE_CONTRACT_METADATA = {
    "CASE_0042": {
        "required_experiment_families": ["COMPONENT_DECOMPOSITION", "SNAPSHOT_DIFF", "DQ_MATERIALITY", "FORMULA_VALIDATION", "RECONCILIATION"],
        "required_evidence_tags": ["COMPONENT_IMPACT", "SNAPSHOT_IMPACT", "FORMULA_VERSION"],
    },
    "CASE_0107": {
        "required_experiment_families": ["ROW_COUNT_ANALYSIS", "DUPLICATE_KEY_ANALYSIS", "PIPELINE_RUN_COMPARISON", "RECONCILIATION"],
        "required_evidence_tags": ["ROW_COUNT_DELTA", "DUPLICATE_IMPACT", "PIPELINE_REPLAY"],
    },
    "CASE_0213": {
        "required_experiment_families": ["FILTER_VALIDATION", "RECONCILIATION"],
        "required_evidence_tags": ["FILTER_HASH_CHANGE", "EXCLUDED_POPULATION", "EXCLUDED_IMPACT"],
    },
    "CASE_0314": {
        "required_experiment_families": ["ROW_COUNT_ANALYSIS", "MISSING_RECORD_IMPACT", "RECONCILIATION"],
        "required_evidence_tags": ["MISSING_ROW_COUNT", "MISSING_IMPACT"],
    },
    "CASE_0441": {
        "required_experiment_families": ["DQ_MATERIALITY", "RECONCILIATION"],
        "required_evidence_tags": ["DQ_IMPACT", "PRIMARY_SOURCE_IMPACT"],
    },
    "CASE_0520": {
        "required_experiment_families": ["ENTITY_COMPARISON", "JOIN_CARDINALITY_ANALYSIS", "RECONCILIATION"],
        "required_evidence_tags": ["ENTITY_OUTLIER", "JOIN_MULTIPLICITY", "JOIN_IMPACT"],
    },
    "CASE_0812": {
        "required_experiment_families": ["COMPONENT_DECOMPOSITION", "SNAPSHOT_DIFF", "FILTER_VALIDATION", "RECONCILIATION"],
        "required_evidence_tags": ["SOURCE_CAUSE_IMPACT", "FILTER_CAUSE_IMPACT", "MULTI_CAUSE_RECONCILIATION"],
    },
}


@dataclass(frozen=True)
class CaseContract:
    id: str
    number: int
    title: str
    metric: str
    hook: str
    difficulty: str
    concepts: tuple[str, ...]
    state: str
    required_experiments: tuple[str, ...]
    expected: float
    observed: float
    deviation: float
    required_case_ids: tuple[str, ...] = ()

    def public_payload(self) -> dict:
        payload = asdict(self)
        payload["number"] = f"{self.number:03d}"
        payload["public_number"] = self.number
        payload["release_state"] = self.state
        payload["slug"] = re.sub(r"[^a-z0-9]+", "-", self.title.lower().replace("€", "")).strip("-")
        payload["learning_objectives"] = [concept.upper().replace(" ", "_") for concept in self.concepts]
        payload["completed"] = False
        payload["best_score"] = None
        payload["concepts"] = list(self.concepts)
        payload["required_experiments"] = list(self.required_experiments)
        payload["required_case_ids"] = list(self.required_case_ids)
        payload.update(CASE_CONTRACT_METADATA[self.id])
        payload["completion"] = {"max_unreconciled_abs": 0.01, "require_final_prediction": True, "allow_insufficient_evidence": False}
        return payload


CASE_CATALOG = (
    CaseContract(
        "CASE_0042", 42, "The Missing €6.8M", "Capital Available",
        "A trusted metric is €6.8M below expectation.", "LEVEL 2",
        ("Decomposition", "Snapshots", "Evidence"), "CORE",
        ("COMPONENT_DECOMPOSITION", "SNAPSHOT_DIFF", "DQ_MATERIALITY", "FORMULA_VALIDATION", "RECONCILIATION"), 125.0, 118.2, -6.8,
    ),
    CaseContract(
        "CASE_0107", 107, "Attack of the Clones", "Net Revenue",
        "Duplicate keys are inflating the total.", "LEVEL 2",
        ("Duplicates", "Pipeline replay"), "COMING_SOON",
        ("ROW_COUNT_ANALYSIS", "DUPLICATE_KEY_ANALYSIS", "PIPELINE_RUN_COMPARISON"), 42.0, 43.8, 1.8, ("CASE_0042",),
    ),
    CaseContract(
        "CASE_0213", 213, "The Vanishing Revenue", "Recognized Revenue",
        "A filter quietly removed the population.", "LEVEL 2",
        ("Filters", "Reconciliation"), "COMING_SOON",
        ("FILTER_VALIDATION", "RECONCILIATION"), 41.2, 34.7, -6.5, ("CASE_0107",),
    ),
)

# The first three entries are the challenge-facing catalog retained for backwards
# compatibility with the original prototype.  The complete game catalog is
# exported separately so release configuration can enable cases independently.
FULL_CASE_CATALOG = CASE_CATALOG + (
    CaseContract("CASE_0314", 314, "The Ghost Records", "Eligible Exposure", "Records disappeared from the eligible population.", "LEVEL 2", ("Missing records",), "FULL_GAME", ("ROW_COUNT_ANALYSIS", "MISSING_RECORD_IMPACT", "RECONCILIATION"), 78.6, 73.4, -5.2, ("CASE_0042",)),
    CaseContract("CASE_0441", 441, "The Red Herring", "Operating Margin Contribution", "A quality warning may be a misleading signal.", "LEVEL 2", ("Data quality",), "FULL_GAME", ("DQ_MATERIALITY", "RECONCILIATION"), 52.4, 45.0, -7.4, ("CASE_0213", "CASE_0314")),
    CaseContract("CASE_0520", 520, "The Impossible Forecast", "Forecast Revenue", "A join may have multiplied the forecast.", "LEVEL 2", ("Entities", "Joins"), "FULL_GAME", ("ENTITY_COMPARISON", "JOIN_CARDINALITY_ANALYSIS", "RECONCILIATION"), 46.0, 83.0, 37.0, ("CASE_0441",)),
    CaseContract("CASE_0812", 812, "Double Trouble", "Liquidity Buffer", "Two causes may be hiding in one anomaly.", "LEVEL 3", ("Multi-cause",), "STRETCH", ("COMPONENT_DECOMPOSITION", "SNAPSHOT_DIFF", "FILTER_VALIDATION", "RECONCILIATION"), 90.0, 83.8, -6.2, ("CASE_0520",)),
)

CASE_BY_ID = {case.id: case for case in CASE_CATALOG}
ALL_CASE_BY_ID = {case.id: case for case in FULL_CASE_CATALOG}


def _assert_canonical_projection() -> None:
    """Fail closed if the runtime compatibility projection drifts from YAML."""
    canonical = {item["id"]: item for item in CANONICAL_PUBLIC_CATALOG["cases"]}
    for case_id, item in canonical.items():
        projected = ALL_CASE_BY_ID.get(case_id)
        if projected is None:
            continue
        for field in ("number", "title", "metric", "state", "expected", "observed", "deviation"):
            if getattr(projected, field) != item[field]:
                raise RuntimeError(f"canonical catalog drift for {case_id}: {field}")


_assert_canonical_projection()


def get_case(case_id: str) -> CaseContract:
    try:
        return ALL_CASE_BY_ID[case_id]
    except KeyError as exc:
        raise ValueError(f"Unknown case: {case_id}") from exc


def get_any_case(case_id: str) -> CaseContract:
    try:
        return ALL_CASE_BY_ID[case_id]
    except KeyError as exc:
        raise ValueError(f"Unknown case: {case_id}") from exc


def case_availability(case: CaseContract, *, review_mode: bool = False, completed_case_ids: set[str] | None = None) -> str:
    """Server-side availability; frontend never reimplements release logic."""
    if case.state == "CORE": return "AVAILABLE"
    # MDL-2 does not own secondary Case contracts. They remain unavailable in
    # normal and review mode until their own deterministic data/Genie gates
    # exist; metadata visibility is not analytical entitlement.
    return "LOCKED"
