"""Freshness validation for MDL-3 live-evaluation evidence."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EvidenceIdentity:
    implementation_sha: str
    genie_contract_digest: str
    genie_live_config_sha256: str
    mdl2_data_contract_digest: str
    case_hash: str


def validate_evidence_identity(payload: dict[str, Any], expected: EvidenceIdentity) -> None:
    """Fail closed unless every identity and batch field matches exactly."""
    required = {
        "implementation_sha": expected.implementation_sha,
        "genie_contract_digest": expected.genie_contract_digest,
        "genie_live_config_sha256": expected.genie_live_config_sha256,
        "mdl2_data_contract_digest": expected.mdl2_data_contract_digest,
        "case_hash": expected.case_hash,
    }
    mismatches = [key for key, value in required.items() if payload.get(key) != value]
    if mismatches:
        raise ValueError(f"stale live evidence identity: {', '.join(mismatches)}")
    attempts = payload.get("attempts")
    if not isinstance(attempts, list) or len(attempts) != 40:
        raise ValueError("live evidence must contain exactly 40 attempts")
    batch_ids = {item.get("batch_id") for item in attempts if isinstance(item, dict) and item.get("batch_id") is not None}
    if not batch_ids and payload.get("batch_id"):
        batch_ids = {payload["batch_id"]}
    if len(batch_ids) != 1:
        raise ValueError("live evidence mixes benchmark batches")
    expected_ids = {
        *(f"OBS-{i:02d}" for i in range(1, 4)), *(f"CMP-{i:02d}" for i in range(1, 4)),
        *(f"SNP-{i:02d}" for i in range(1, 4)), *(f"DQ-{i:02d}" for i in range(1, 4)),
        *(f"FOR-{i:02d}" for i in range(1, 4)), *(f"LIN-{i:02d}" for i in range(1, 3)),
        *(f"GSTART-{i:02d}" for i in range(1, 6)), *(f"GNEXT-{i:02d}" for i in range(1, 6)),
        *(f"SEC-{i:02d}" for i in range(1, 4)), *(f"ALT-{i:02d}" for i in range(1, 11)),
    }
    actual_ids = {item.get("benchmark_id") for item in attempts if isinstance(item, dict)}
    if actual_ids != expected_ids:
        raise ValueError("live evidence benchmark IDs do not match the locked corpus")
    if payload.get("status") != "PASS" or any(item.get("status") != "PASS" for item in attempts):
        raise ValueError("live evidence contains failed benchmark attempts")
