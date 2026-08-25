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
