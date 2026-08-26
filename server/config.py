"""Typed runtime configuration for the application boundary."""
from __future__ import annotations

from dataclasses import dataclass
import os


def _flag(name: str, default: bool = False) -> bool:
    return os.getenv(name, "1" if default else "0").strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    allow_fixture_mode: bool
    challenge_review_mode: bool
    local_a11y_test: bool
    genie_space_id: str | None
    genie_request_timeout_seconds: float
    genie_poll_interval_ms: int

    @classmethod
    def from_env(cls) -> "Settings":
        deployed = bool(os.getenv("DATABRICKS_APP_PORT"))
        genie_timeout = float(os.getenv("GENIE_REQUEST_TIMEOUT_SECONDS", "75"))
        genie_poll = int(os.getenv("GENIE_POLL_INTERVAL_MS", "1000"))
        if genie_timeout <= 0:
            raise ValueError("GENIE_REQUEST_TIMEOUT_SECONDS must be positive")
        if genie_poll <= 0:
            raise ValueError("GENIE_POLL_INTERVAL_MS must be positive")
        return cls(
            host=os.getenv("UVICORN_HOST", "0.0.0.0"),
            port=int(os.getenv("DATABRICKS_APP_PORT", os.getenv("UVICORN_PORT", "8000"))),
            allow_fixture_mode=_flag("ALLOW_FIXTURE_MODE", default=not deployed),
            challenge_review_mode=_flag("CHALLENGE_REVIEW_MODE"),
            local_a11y_test=_flag("LOCAL_A11Y_TEST"),
            genie_space_id=os.getenv("GENIE_SPACE_ID") or os.getenv("DATABRICKS_GENIE_SPACE_ID"),
            genie_request_timeout_seconds=genie_timeout,
            genie_poll_interval_ms=genie_poll,
        )


def load_settings() -> Settings:
    """Read the current process environment into an immutable settings value."""
    return Settings.from_env()


settings = load_settings()
