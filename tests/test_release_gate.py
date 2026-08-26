import subprocess

from scripts import release_gate


def test_release_gate_converts_hung_gate_to_failure(monkeypatch):
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(kwargs.get("args", args[0]), 300, output="partial")

    monkeypatch.setattr(release_gate.subprocess, "run", timeout)
    result = release_gate.run("browser", ["npm.cmd", "run", "test:browser"])
    assert result["status"] == "FAIL"
    assert "timed out after" in result["output"]
