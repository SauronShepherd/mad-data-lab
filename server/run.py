"""Databricks Apps-compatible ASGI launcher."""

from __future__ import annotations

import os

import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "server.main:app",
        host=os.getenv("UVICORN_HOST", "0.0.0.0"),
        port=int(os.getenv("DATABRICKS_APP_PORT", os.getenv("UVICORN_PORT", "8000"))),
    )
