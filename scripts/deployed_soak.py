"""Ten authenticated deployed Case #042 journeys."""
from __future__ import annotations

import os
import time

from deployed_smoke import main as deployed_smoke


def main() -> None:
    if not os.getenv("DEPLOYED_APP_URL"):
        raise SystemExit("deployed soak: set DEPLOYED_APP_URL")
    for index in range(10):
        for attempt in range(3):
            try:
                deployed_smoke()
                break
            except RuntimeError as exc:
                # A circuit-open session is intentionally terminal for that
                # session. Start a fresh journey so the soak measures ten
                # successful journeys rather than aborting on one poisoned
                # session; never hide a non-circuit product failure.
                if "GENIE_CIRCUIT_OPEN" not in str(exc) or attempt == 2:
                    raise
                time.sleep(5 * (attempt + 1))
        print(f"deployed soak: completed {index + 1}/10", flush=True)
    print("deployed soak: PASS (10 authenticated Case #042 journeys)", flush=True)


if __name__ == "__main__":
    main()
