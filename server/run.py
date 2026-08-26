"""Databricks Apps-compatible ASGI launcher."""

from __future__ import annotations

import os
import uvicorn
from .config import settings


if __name__ == "__main__":
    uvicorn.run(
        "server.main:app",
        host=os.getenv("UVICORN_HOST", settings.host),
        port=int(os.getenv("DATABRICKS_APP_PORT", os.getenv("UVICORN_PORT", str(settings.port)))),
    )
