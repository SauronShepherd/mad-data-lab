import json
from pathlib import Path

from scripts import release_candidate


def test_release_candidate_gate_order_is_deterministic():
    assert release_candidate.ORDER == tuple(release_candidate.release_gate.GATES)


def test_release_candidate_never_reuses_stale_live_pass(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(release_candidate, "OUTPUT", tmp_path / "release-candidate.json")
    monkeypatch.setattr(release_candidate, "identity", lambda: {"branch": "MDL-5", "commit_sha": "a" * 40, "tree_sha": "b" * 40, "runtime_digest": "c" * 64, "data_contract_digest": "d" * 64})
    monkeypatch.setattr(release_candidate, "asset_hashes", lambda: {})
    monkeypatch.setattr(release_candidate, "test_counts", lambda: {"tests": 1, "skipped": 0, "failures": 0, "errors": 0})
    monkeypatch.setattr(release_candidate, "run_gate", lambda name: calls.append(name) or {"name": name, "status": "PASS"})
    monkeypatch.delenv("RUN_LIVE_GATES", raising=False)
    assert release_candidate.main() == 1
    payload = json.loads((tmp_path / "release-candidate.json").read_text())
    assert payload["status"] == "FAIL"
    assert all(payload[key]["status"] == "BLOCKED_EXTERNAL" for key in ("genie_result", "deployment_result", "soak_result"))
    assert calls == list(release_candidate.ORDER)
