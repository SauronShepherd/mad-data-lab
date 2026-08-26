import json
import subprocess
import sys
from types import SimpleNamespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_fixture_benchmark_emits_30_attempts_and_junit():
    result = subprocess.run([sys.executable, "scripts/run_mdl3_benchmark.py"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads((ROOT / "release-report/MDL-3/benchmark.json").read_text(encoding="utf-8"))
    assert payload["status"] == "PASS"
    assert payload["summary"] == {"total": 30, "passed": 30, "failed": 0}
    assert payload["attempts"][0]["conversation_id"] == "fixture-obs-01"
    assert payload["started_at_utc"] == "FIXTURE_DETERMINISTIC"
    assert (ROOT / "release-report/MDL-3/benchmark.junit.xml").is_file()


def test_live_mode_does_not_silently_use_fixture():
    result = subprocess.run([sys.executable, "scripts/run_mdl3_benchmark.py", "--no-fixture"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode != 0
    assert "GENIE_SPACE_ID" in result.stderr


def test_live_benchmark_uses_two_turn_protocol_for_gnext_cases():
    source = (ROOT / "scripts/run_mdl3_benchmark.py").read_text(encoding="utf-8")
    assert 'item["turn_type"] == "fresh-2-turn"' in source
        assert "create_message(" in source


def test_benchmark_polling_accepts_asking_ai_with_answer_attachment():
    from scripts.run_mdl3_benchmark import wait_for_message

    message = SimpleNamespace(status="ASKING_AI", attachments=[SimpleNamespace(text=object(), query=None)])
    client = SimpleNamespace(genie=SimpleNamespace(get_message=lambda **_: message))
    assert wait_for_message(client, "space", "conversation", "message", 1) is message


def test_live_identity_uses_canonical_case_hash():
    from data.generation.case_0042 import generate_case
    from scripts.run_mdl3_benchmark import current_evidence_identity

    assert current_evidence_identity()["case_hash"] == generate_case().content_hash
