"""Machine-readable MDL-6 test catalogue and coverage accounting."""
from __future__ import annotations

ACCESSIBILITY_IDS = tuple(f"AX-{index:03d}" for index in range(1, 16))
PERFORMANCE_IDS = tuple(f"PF-{index:03d}" for index in range(1, 9))
ASSET_IDS = tuple(f"AS-{index:03d}" for index in range(1, 16))
SECURITY_IDS = tuple(f"SEC-{index:03d}" for index in range(1, 21))
CHAOS_IDS = tuple(f"CH-{index:03d}" for index in range(1, 26))

REQUIRED_TEST_IDS = ACCESSIBILITY_IDS + PERFORMANCE_IDS + ASSET_IDS + SECURITY_IDS + CHAOS_IDS

def validate_catalog() -> None:
    assert len(ACCESSIBILITY_IDS) == 15
    assert len(PERFORMANCE_IDS) == 8
    assert len(ASSET_IDS) == 15
    assert len(SECURITY_IDS) == 20
    assert len(CHAOS_IDS) == 25
    assert len(REQUIRED_TEST_IDS) == len(set(REQUIRED_TEST_IDS)) == 83
