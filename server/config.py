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

    @classmethod
    def from_env(cls) -> "Settings":
        deployed = bool(os.getenv("DATABRICKS_APP_PORT"))
        return cls(
            host=os.getenv("UVICORN_HOST", "0.0.0.0"),
            port=int(os.getenv("DATABRICKS_APP_PORT", os.getenv("UVICORN_PORT", "8000"))),
            allow_fixture_mode=_flag("ALLOW_FIXTURE_MODE", default=not deployed),
            challenge_review_mode=_flag("CHALLENGE_REVIEW_MODE"),
            local_a11y_test=_flag("LOCAL_A11Y_TEST"),
            genie_space_id=os.getenv("GENIE_SPACE_ID") or os.getenv("DATABRICKS_GENIE_SPACE_ID"),
        )


def load_settings() -> Settings:
    """Read the current process environment into an immutable settings value."""
    return Settings.from_env()


settings = load_settings()
