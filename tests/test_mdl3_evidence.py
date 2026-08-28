import pytest

from backend.genie.evidence import EvidenceIdentity, validate_evidence_identity


def identity():
    return EvidenceIdentity("impl", "contract", "live-config", "data", "case")


def payload():
    return {
        "implementation_sha": "impl",
        "genie_contract_digest": "contract",
        "genie_live_config_sha256": "live-config",
        "mdl2_data_contract_digest": "data",
        "case_hash": "case",
        "status": "PASS",
        "attempts": [{"batch_id": "batch-1", "benchmark_id": benchmark_id(i), "status": "PASS"} for i in range(40)],
    }


def benchmark_id(i):
    groups = [("OBS", 3), ("CMP", 3), ("SNP", 3), ("DQ", 3), ("FOR", 3), ("LIN", 2), ("GSTART", 5), ("GNEXT", 5), ("SEC", 3), ("ALT", 10)]
    for prefix, count in groups:
        if i < count:
            return f"{prefix}-{i + 1:02d}"
        i -= count
    raise AssertionError(i)


def test_current_evidence_identity_is_accepted():
    validate_evidence_identity(payload(), identity())


@pytest.mark.parametrize("field", ["implementation_sha", "genie_contract_digest", "genie_live_config_sha256", "mdl2_data_contract_digest", "case_hash"])
def test_any_identity_drift_is_rejected(field):
    value = payload()
    value[field] = "stale"
    with pytest.raises(ValueError, match="stale"):
        validate_evidence_identity(value, identity())


def test_mixed_or_incomplete_batches_are_rejected():
    value = payload()
    value["attempts"][-1] = {"batch_id": "batch-2"}
    with pytest.raises(ValueError, match="mixes"):
        validate_evidence_identity(value, identity())
    value = payload()
    value["attempts"] = value["attempts"][:29]
    with pytest.raises(ValueError, match="40"):
        validate_evidence_identity(value, identity())


def test_failed_attempts_and_wrong_benchmark_ids_are_rejected():
    value = payload()
    value["attempts"][0]["status"] = "FAIL"
    with pytest.raises(ValueError, match="failed"):
        validate_evidence_identity(value, identity())
    value = payload()
    value["attempts"][0]["benchmark_id"] = "UNKNOWN"
    with pytest.raises(ValueError, match="benchmark IDs"):
        validate_evidence_identity(value, identity())
