"""Canonical progression badge definitions."""
BADGES = {
    "DATA_APPRENTICE": "Complete one Case.", "METRIC_SCIENTIST": "Complete any Case with score >= 800.",
    "EVIDENCE_ANALYST": "Inspect required source evidence and lineage before verdict.",
    "SKEPTICAL_SCIENTIST": "Reject an insufficient high-salience signal.", "CASE_COLLECTOR": "Complete three different Cases.",
    "LAB_VETERAN": "Complete five different Cases.", "RECONCILIATION_MASTER": "Complete a Level 3 Case with zero residual and no reveal penalty.",
}

def derive_badges(completed_case_ids, score: int, *, evidence_analyst=False, skeptical_scientist=False, reconciliation_master=False):
    result = set()
    count = len(set(completed_case_ids))
    if count >= 1: result.add("DATA_APPRENTICE")
    if score >= 800: result.add("METRIC_SCIENTIST")
    if evidence_analyst: result.add("EVIDENCE_ANALYST")
    if skeptical_scientist: result.add("SKEPTICAL_SCIENTIST")
    if count >= 3: result.add("CASE_COLLECTOR")
    if count >= 5: result.add("LAB_VETERAN")
    if reconciliation_master: result.add("RECONCILIATION_MASTER")
    return sorted(result)
