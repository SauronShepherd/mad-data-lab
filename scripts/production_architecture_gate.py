"""Reject accidental production imports of the retired fixture domain."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_ROOTS = (ROOT / "server", ROOT / "backend")
FORBIDDEN = ("from .domain", "import server.domain", "from server.domain", "from .mutation", "import server.mutation")
RETIRED_ANALYTICAL_MARKERS = ("EXP-01", "EXP-02", "EXP-03", "Promo effect?", "Data bug?", "Pricing change?", "Seasonal factor?")
EXCLUDED = {ROOT / "server" / "domain.py", ROOT / "server" / "mutation.py"}


def main() -> None:
    violations = []
    for base in PRODUCTION_ROOTS:
        for path in base.rglob("*.py"):
            if path in EXCLUDED:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for marker in FORBIDDEN:
                if marker in text:
                    violations.append(f"{path.relative_to(ROOT)}: {marker}")
            for marker in RETIRED_ANALYTICAL_MARKERS:
                if marker in text:
                    violations.append(f"{path.relative_to(ROOT)}: retired analytical marker {marker}")
    if violations:
        raise SystemExit("production architecture gate: FAIL\n" + "\n".join(violations))
    print("production architecture gate: PASS (canonical runtime has no retired-domain imports)")


if __name__ == "__main__":
    main()
