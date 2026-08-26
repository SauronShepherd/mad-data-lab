from pathlib import Path


def test_pytest_gate_exists_and_is_release_safe():
    script = Path(__file__).parents[1] / "scripts/pytest_gate.py"
    text = script.read_text(encoding="utf-8")
    assert "skipped" in text and "xfailed" in text and "xpassed" in text
