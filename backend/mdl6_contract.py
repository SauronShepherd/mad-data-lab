"""Machine-readable MDL-6 test catalogue and coverage accounting."""
from __future__ import annotations

ACCESSIBILITY_IDS = tuple(f"AX-{index:03d}" for index in range(1, 16))
PERFORMANCE_IDS = tuple(f"PF-{index:03d}" for index in range(1, 9))
ASSET_IDS = tuple(f"AS-{index:03d}" for index in range(1, 16))
SECURITY_IDS = tuple(f"SEC-{index:03d}" for index in range(1, 21))
CHAOS_IDS = tuple(f"CH-{index:03d}" for index in range(1, 26))

REQUIRED_TEST_IDS = ACCESSIBILITY_IDS + PERFORMANCE_IDS + ASSET_IDS + SECURITY_IDS + CHAOS_IDS

# Acceptance criteria copied into the executable contract from section
# 44.14–44.17 of the complete game specification. Keeping these labels here
# prevents the coverage matrix from collapsing distinct requirements into a
# generic category placeholder.
REQUIREMENT_EXPECTATIONS = {
    **dict(zip(ACCESSIBILITY_IDS, (
        "lab entrance has 0 serious/critical axe violations",
        "hypothesis board has 0 serious/critical axe violations",
        "experiment result has 0 serious/critical axe violations",
        "evidence explorer has 0 serious/critical axe violations",
        "verdict has 0 serious/critical axe violations",
        "all interactive controls are keyboard reachable",
        "focus order is logical",
        "buttons have accessible names",
        "data table headers are associated",
        "status is not color-only",
        "chart has textual equivalent",
        "reduced-motion preference is honored",
        "minimum contrast passes axe where supported",
        "audio toggle state is announced",
        "loading state uses an appropriate live region",
    ))),
    **dict(zip(PERFORMANCE_IDS, (
        "frontend build stays within size budgets",
        "local fixture first meaningful UI is under 2 seconds",
        "local interaction feedback is under 100ms",
        "fixture chart render is under 300ms",
        "100-row evidence table render is under 500ms",
        "warm deployed health response is under 1 second",
        "warm deployed shell p50/p95 are recorded",
        "one evidence view does not create API N+1 calls",
    ))),
    **dict(zip(ASSET_IDS, (
        "all manifest assets exist",
        "image dimensions match expectations",
        "transparent assets have required alpha",
        "all images decode",
        "images stay within file-size budgets",
        "no giant unoptimized source is packaged",
        "final audio exists",
        "audio duration is at least 330 seconds",
        "audio duration is at most 510 seconds",
        "audio is smaller than 8.5MB",
        "audio decodes successfully",
        "audio loudness is acceptable",
        "audio true peak is safe",
        "no mid-track silence exceeds 4 seconds",
        "production build references only production asset paths",
    ))),
    **dict(zip(SECURITY_IDS, (
        "secret scan passes",
        "dependency vulnerability scan passes threshold",
        "case truth is absent from Genie config",
        "case truth is absent from curated SQL definitions",
        "case truth is absent from frontend bundle strings",
        "prompt injection cannot reveal hidden truth",
        "prompt injection cannot alter allowed control enum",
        "arbitrary HTML response is escaped",
        "arbitrary JavaScript response is escaped",
        "SQL injection business-key filter is handled safely",
        "oversized chat input is rejected",
        "path-traversal-like case ID is rejected",
        "CORS/default proxy is not widened",
        "API config contains no secrets",
        "API health contains no secrets",
        "structured error logs contain no secrets",
        "direct private endpoint is absent",
        "arbitrary table cannot be selected through API",
        "Genie query path stays in configured resource context",
        "production cannot enable fixture mode through a public query parameter",
    ))),
}

CHAOS_SCENARIOS = (
    ("CH-001", "Genie latency 5s", "bounded response or retryable error"),
    ("CH-002", "Genie latency 30s", "bounded timeout without state commit"),
    ("CH-003", "Genie timeout", "GENIE_TIMEOUT and retryable envelope"),
    ("CH-004", "transient Genie 500", "retry then success or bounded failure"),
    ("CH-005", "persistent Genie 500", "circuit opens and state is preserved"),
    ("CH-006", "malformed Genie JSON", "GENIE_MALFORMED_PROTOCOL"),
    ("CH-007", "wrong Case protocol", "reject without cross-Case data"),
    ("CH-008", "unsupported Experiment", "registered-set rejection"),
    ("CH-009", "missing query", "stable validation error"),
    ("CH-010", "SQL timeout", "retryable data error without commit"),
    ("CH-011", "SQL empty result", "explicit empty-result handling"),
    ("CH-012", "SQL wrong columns", "EVIDENCE_SCHEMA_MISMATCH"),
    ("CH-013", "reconciliation mismatch", "RECONCILIATION_FAILED"),
    ("CH-014", "warehouse pending", "WAREHOUSE_PENDING"),
    ("CH-015", "quota unavailable", "WAREHOUSE_QUOTA_EXHAUSTED"),
    ("CH-016", "browser network loss", "recoverable UI state"),
    ("CH-017", "network restoration", "retry succeeds after restoration"),
    ("CH-018", "illustration 404", "usable layout and decorative fallback"),
    ("CH-019", "audio 404", "functional muted/unavailable control"),
    ("CH-020", "autoplay rejected", "no blocking error loop"),
    ("CH-021", "duplicate POST race", "single logical commit"),
    ("CH-022", "backend restart/session loss", "explicit non-corrupt recovery"),
    ("CH-023", "corrupted local preferences", "safe defaults"),
    ("CH-024", "long evidence field", "bounded rendering and safe storage"),
    ("CH-025", "Unicode business key/title", "preserved and safely rendered"),
)

E2E_SCENARIOS = (
    ("E2E-015", "Genie timeout"),
    ("E2E-016", "Genie failed"),
    ("E2E-017", "missing query"),
    ("E2E-018", "expired result recovery"),
    ("E2E-021", "mobile-width operation"),
    ("E2E-022", "1440x900 layout"),
    ("E2E-023", "1280x720 layout"),
    ("E2E-024", "keyboard-only flow"),
    ("E2E-027", "double click"),
    ("E2E-029", "explicit non-production fixture mode"),
    ("E2E-030", "production fixture mode disabled"),
)

def validate_catalog() -> None:
    assert len(ACCESSIBILITY_IDS) == 15
    assert len(PERFORMANCE_IDS) == 8
    assert len(ASSET_IDS) == 15
    assert len(SECURITY_IDS) == 20
    assert len(CHAOS_IDS) == 25
    assert len(REQUIRED_TEST_IDS) == len(set(REQUIRED_TEST_IDS)) == 83
    assert tuple(item[0] for item in CHAOS_SCENARIOS) == CHAOS_IDS
    assert len({item[0] for item in E2E_SCENARIOS}) == len(E2E_SCENARIOS)
