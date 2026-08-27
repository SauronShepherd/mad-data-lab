"""Case completion predicate with no dependency on private truth."""
from __future__ import annotations
from dataclasses import dataclass, field

REQUIRED_FAMILIES = ("COMPONENT_DECOMPOSITION", "SNAPSHOT_DIFF", "DQ_MATERIALITY", "FORMULA_VALIDATION", "RECONCILIATION")
REQUIRED_EVIDENCE = ("COMPONENT_IMPACT", "SNAPSHOT_IMPACT", "DQ_MATERIALITY", "FORMULA_VERSION", "RECONCILIATION")

@dataclass(frozen=True)
class CompletionEligibility:
    ready_for_final_prediction: bool
    missing_required_experiments: list[str] = field(default_factory=list)
    missing_required_evidence_actions: list[str] = field(default_factory=list)
    failed_reconciliations: list[str] = field(default_factory=list)
    blocking_reason_codes: list[str] = field(default_factory=list)

def evaluate_case_completion(completed_experiments, evidence_tags=(), inspected_capabilities=(), *, residual=0.0) -> CompletionEligibility:
    completed = set(completed_experiments)
    tags = set(evidence_tags)
    inspected = set(inspected_capabilities)
    missing_exp = [x for x in REQUIRED_FAMILIES if x not in completed]
    missing_evidence = [x for x in REQUIRED_EVIDENCE if x not in tags]
    if "CASE_0042:LINEAGE:V2_SOURCE_PATH" not in inspected:
        missing_evidence.append("OPEN_REQUIRED_LINEAGE")
    failed = ["V2_RESIDUAL_OUT_OF_TOLERANCE"] if abs(float(residual)) > 0.01 else []
    reasons = [f"{x}_REQUIRED" for x in missing_exp] + failed
    if missing_evidence:
        reasons.append("REQUIRED_EVIDENCE_ACTIONS_PENDING")
    return CompletionEligibility(not (missing_exp or missing_evidence or failed), missing_exp, missing_evidence, failed, reasons)
