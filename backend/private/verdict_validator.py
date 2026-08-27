"""Independent validation of the public Case #042 scientific verdict."""
from __future__ import annotations

def validate_case042_verdict(*, formula_changed: bool = False, dq_primary: bool = False,
                             v2_source_changes: float = -5.90, unreconciled: float = 0.0,
                             h1_status: str = "SUPPORTED", h2_status: str = "RULED_OUT",
                             h3_status: str = "POSSIBLE") -> tuple[bool, list[str]]:
    errors = []
    if formula_changed: errors.append("FORMULA_MUST_BE_UNCHANGED")
    if dq_primary: errors.append("DQ_MUST_NOT_BE_PRIMARY")
    if abs(v2_source_changes - (-5.90)) > .01: errors.append("V2_SOURCE_RECONCILIATION_INVALID")
    if abs(unreconciled) > .01: errors.append("NONZERO_UNRECONCILED_RESIDUAL")
    if (h1_status, h2_status, h3_status) != ("SUPPORTED", "RULED_OUT", "POSSIBLE"):
        errors.append("INVALID_EPISTEMIC_STATUSES")
    return not errors, errors
