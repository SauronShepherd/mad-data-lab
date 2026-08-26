import pytest

from server.config import Settings


def test_local_defaults_allow_fixture_mode(monkeypatch):
    monkeypatch.delenv("DATABRICKS_APP_PORT", raising=False)
    monkeypatch.delenv("ALLOW_FIXTURE_MODE", raising=False)
    monkeypatch.delenv("CHALLENGE_REVIEW_MODE", raising=False)
    settings = Settings.from_env()
    assert settings.allow_fixture_mode is True
    assert settings.challenge_review_mode is False


def test_deployed_defaults_fail_closed(monkeypatch):
    monkeypatch.setenv("DATABRICKS_APP_PORT", "8000")
    monkeypatch.delenv("ALLOW_FIXTURE_MODE", raising=False)
    assert Settings.from_env().allow_fixture_mode is False


def test_explicit_flags_and_genie_alias(monkeypatch):
    monkeypatch.setenv("ALLOW_FIXTURE_MODE", "yes")
    monkeypatch.setenv("CHALLENGE_REVIEW_MODE", "true")
    monkeypatch.delenv("GENIE_SPACE_ID", raising=False)
    monkeypatch.setenv("DATABRICKS_GENIE_SPACE_ID", "space-123")
    settings = Settings.from_env()
    assert settings.allow_fixture_mode is True
    assert settings.challenge_review_mode is True
    assert settings.genie_space_id == "space-123"
    assert settings.genie_request_timeout_seconds == 75
    assert settings.genie_poll_interval_ms == 1000


def test_genie_budget_can_be_configured(monkeypatch):
    monkeypatch.setenv("GENIE_REQUEST_TIMEOUT_SECONDS", "12.5")
    monkeypatch.setenv("GENIE_POLL_INTERVAL_MS", "250")
    settings = Settings.from_env()
    assert settings.genie_request_timeout_seconds == 12.5
    assert settings.genie_poll_interval_ms == 250


def test_invalid_genie_budget_is_rejected(monkeypatch):
    monkeypatch.setenv("GENIE_REQUEST_TIMEOUT_SECONDS", "0")
    with pytest.raises(ValueError, match="must be positive"):
        Settings.from_env()
    monkeypatch.setenv("GENIE_REQUEST_TIMEOUT_SECONDS", "75")
    monkeypatch.setenv("GENIE_POLL_INTERVAL_MS", "-1")
    with pytest.raises(ValueError, match="must be positive"):
        Settings.from_env()
