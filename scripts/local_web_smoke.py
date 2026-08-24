"""HTTP smoke checks for the built frontend served by FastAPI."""
from __future__ import annotations

import sys
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    with urlopen(base + "/", timeout=5) as response:
        html = response.read().decode("utf-8")
        assert response.status == 200 and 'id="root"' in html and "/assets/" in html
    with urlopen(base + "/api/cases", timeout=5) as response:
        assert response.status == 200 and len(response.read()) > 100
    print("local web smoke: PASS (frontend and API same-origin HTTP)")


if __name__ == "__main__":
    main()
