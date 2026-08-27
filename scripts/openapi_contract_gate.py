"""Validate the public FastAPI route surface against the release contract."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from server.main import app


REQUIRED = {
    ("GET", "/health"),
    ("GET", "/api/health"),
    ("GET", "/api/config"),
    ("GET", "/api/cases"),
    ("GET", "/api/cases/{case_id}"),
    ("GET", "/api/cases/{case_id}/experiments"),
    ("GET", "/api/progression"),
    ("POST", "/api/sessions"),
    ("GET", "/api/sessions/{session_id}"),
    ("POST", "/api/sessions/{session_id}/start"),
    ("POST", "/api/sessions/{session_id}/next"),
    ("GET", "/api/sessions/{session_id}/evidence"),
    ("POST", "/api/sessions/{session_id}/evidence/inspect"),
    ("POST", "/api/sessions/{session_id}/hint"),
    ("POST", "/api/sessions/{session_id}/conclude"),
    ("POST", "/api/sessions/{session_id}/debrief"),
    ("POST", "/api/sessions/{session_id}/chat"),
    ("POST", "/api/genie/ask"),
}


def main() -> None:
    schema = app.openapi()
    routes = {(method.upper(), path) for path, operations in schema["paths"].items() for method in operations}
    missing = sorted(REQUIRED - routes)
    private = sorted(path for path in schema["paths"] if any(marker in path.lower() for marker in ("truth", "oracle", "private")))
    if missing or private:
        raise SystemExit(f"openapi contract gate: FAIL missing={missing} private_routes={private}")
    print(f"openapi contract gate: PASS ({len(routes)} public operations)")


if __name__ == "__main__":
    main()
