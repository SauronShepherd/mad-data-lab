from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _metadata(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_challenge_rules_record_genie_core_and_track():
    text = _metadata(ROOT / "docs/challenge/verified-rules.md")
    assert "free_edition_required: true" in text
    assert "genie_at_core_required: true" in text
    assert "track: Track B - Creative Thinking" in text


def test_platform_baseline_records_runtime_boundary():
    text = _metadata(ROOT / "docs/platform/databricks-apps-verified.md")
    assert "runtime_python: \"3.11\"" in text
    assert "port_environment: DATABRICKS_APP_PORT" in text
    assert "genie_environment: GENIE_SPACE_ID" in text


def test_app_manifest_declares_genie_budget_defaults():
    text = (ROOT / "app.yaml").read_text(encoding="utf-8")
    assert 'name: GENIE_REQUEST_TIMEOUT_SECONDS' in text
    assert 'value: "75"' in text
    assert 'name: GENIE_POLL_INTERVAL_MS' in text
    assert 'value: "1000"' in text
