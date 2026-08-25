"""Server-owned analytical experiment contracts for the generated evidence package."""
from __future__ import annotations
from dataclasses import dataclass
from data.generation import generate_case

@dataclass(frozen=True)
class Experiment:
    id: str
    name: str
    instrument: str
    rationale: str
    evidence: str
    updates: tuple[tuple[str, str], ...] = ()

CASE042_EXPERIMENTS = (
    Experiment("COMPONENT_DECOMPOSITION", "Component Decomposer", "WATERFALL", "Split the metric into signed component movements.", ""),
    Experiment("SNAPSHOT_DIFF", "Snapshot Reactor", "SNAPSHOT_DIFF", "Compare previous and current source snapshots.", ""),
    Experiment("DQ_MATERIALITY", "Data Quality Scanner", "DQ_PANEL", "Measure the quality warning and test whether it overlaps the primary signal.", ""),
    Experiment("FORMULA_VALIDATION", "Formula Validator", "FORMULA_CHECK", "Verify formula identity and normalized hash across runs.", ""),
    Experiment("RECONCILIATION", "Reconciliation Ledger", "RECONCILIATION", "Reconcile every component and evidence contribution to zero residual.", ""),
)
EXPERIMENTS_BY_CASE = {"CASE_0042": CASE042_EXPERIMENTS}
PLANNED_EXPERIMENTS_BY_CASE: dict[str, tuple[Experiment, ...]] = {}

EVIDENCE_BY_ID = {
    "COMPONENT_DECOMPOSITION": lambda c: "V2 contributes -€5.90M of the -€6.80M deviation; all four components reconcile.",
    "SNAPSHOT_DIFF": lambda c: "V2 changed through 23 modified, 2 removed, and 5 added logical records for -€5.90M.",
    "DQ_MATERIALITY": lambda c: "DQ_0042_01 affects 5 overlapping keys with estimated impact -€0.30M; it is non-additive.",
    "FORMULA_VALIDATION": lambda c: f"CAPITAL_AVAILABLE_V1 is unchanged; normalized formula hash is {c.public['formula_hash']}.",
    "RECONCILIATION": lambda c: "Expected 125.00, observed 118.20, deviation -6.80; reconciliation residual is 0.00.",
}

def experiment_payload(experiment: Experiment, index: int, case_id: str = "CASE_0042") -> dict:
    evidence = EVIDENCE_BY_ID.get(experiment.id, lambda c: experiment.evidence)(generate_case()) if case_id == "CASE_0042" else experiment.evidence
    return {"case_id": case_id, "experiment_id": experiment.id, "experiment_number": index + 1, "name": experiment.name, "instrument": experiment.instrument, "rationale": experiment.rationale, "evidence": evidence, "hypothesis_updates": [{"name": n, "status": s} for n, s in experiment.updates], "source": "generated_case_data" if case_id == "CASE_0042" else "contract"}
