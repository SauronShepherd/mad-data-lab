"""Ten authenticated deployed Case #042 journeys."""
from __future__ import annotations

import os

from deployed_smoke import main as deployed_smoke


def main() -> None:
    if not os.getenv("DEPLOYED_APP_URL"):
        raise SystemExit("deployed soak: set DEPLOYED_APP_URL")
    for index in range(10):
        deployed_smoke()
        print(f"deployed soak: completed {index + 1}/10", flush=True)
    print("deployed soak: PASS (10 authenticated Case #042 journeys)", flush=True)


if __name__ == "__main__":
    main()
