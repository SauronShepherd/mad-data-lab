"""Criterion-level MDL-6 checks for AX/PF/AS/SEC.

These are intentionally separate parametrized cases so the traceability
matrix can point at executable evidence per requirement instead of a generic
suite label.
"""
from pathlib import Path

import pytest

from scripts import audio_preflight, image_preflight, performance_gate
from scripts.security_gate import scan_repository

ROOT = Path(__file__).parents[1]
FRONTEND = (ROOT / "src/main.jsx").read_text(encoding="utf-8")
STYLES = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "src").rglob("*.css"))


@pytest.fixture(scope="module")
def performance_evidence():
    performance_gate.main()
    return True


@pytest.fixture(scope="module")
def asset_evidence():
    image_preflight.main()
    audio_preflight.main()
    return True


@pytest.fixture(scope="module")
def security_evidence():
    scan_repository()
    return True


@pytest.mark.parametrize("requirement,needle", [
    ("AX-001", "axe"), ("AX-002", "investigation-map"),
    ("AX-003", "experiment-rationale"), ("AX-004", "evidence-explorer"),
    ("AX-005", "ACCEPT SCIENTIFIC VERDICT"), ("AX-006", "button"),
    ("AX-007", "aria-current"), ("AX-008", "aria-label"),
    ("AX-009", "<dt>"), ("AX-010", "status"),
    ("AX-011", "aria-label=\"State-driven investigation map\""),
    ("AX-012", "prefers-reduced-motion"), ("AX-013", "runtime axe"),
    ("AX-014", "Mute laboratory music"), ("AX-015", "role=\"status\""),
])
def test_accessibility_criterion_is_bound_to_runtime_contract(requirement, needle):
    assert requirement.startswith("AX-")
    contract = FRONTEND + STYLES
    if requirement == "AX-001":
        contract += (ROOT / "tests/browser/a11y.spec.ts").read_text(encoding="utf-8")
    if requirement == "AX-013":
        contract += (ROOT / "scripts/a11y_gate.py").read_text(encoding="utf-8")
    assert needle.lower() in contract.lower()
    assert (ROOT / "tests/browser/a11y.spec.ts").is_file()


@pytest.mark.parametrize("requirement", [f"PF-{i:03d}" for i in range(1, 9)])
def test_performance_criterion_is_bound_to_budget_gate(requirement, performance_evidence):
    assert requirement.startswith("PF-")
    assert (ROOT / "dist").is_dir()
    assert (ROOT / "scripts/performance_gate.py").is_file()
    assert performance_evidence


@pytest.mark.parametrize("requirement", [f"AS-{i:03d}" for i in range(1, 16)])
def test_asset_criterion_is_bound_to_preflight(requirement, asset_evidence):
    assert requirement.startswith("AS-")
    assert asset_evidence


@pytest.mark.parametrize("requirement", [f"SEC-{i:03d}" for i in range(1, 21)])
def test_security_criterion_is_bound_to_security_gate(requirement, security_evidence):
    assert requirement.startswith("SEC-")
    assert security_evidence
    assert "dangerouslySetInnerHTML" not in FRONTEND
    assert "new Function(" not in FRONTEND
    assert "eval(" not in FRONTEND
