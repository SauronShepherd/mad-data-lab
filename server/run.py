"""Databricks Apps-compatible ASGI launcher."""

from __future__ import annotations

import uvicorn
from .config import settings


if __name__ == "__main__":
    uvicorn.run(
        "server.main:app",
        host=settings.host,
        port=settings.port,
    )
