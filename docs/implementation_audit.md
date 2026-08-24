# MAD DATA LAB implementation audit

Updated after the final aligned deployment and authenticated smoke.

## Verified implementation

| Area | Evidence |
|---|---|
| Case #042 deterministic reconciliation | `tests/test_domain.py`, golden values and hash stability |
| Seven-case catalog/contracts | `server/catalog.py`, `scripts/local_e2e.py` |
| Closed Genie protocol | `server/genie.py`, contract tests, live Genie benchmark |
| Hidden-truth boundary | security gate, curated projections, Genie resource manifest |
| Server-authoritative state | `server/state.py`, session event tests, restart test |
| Scoring/badges/hints | score DTO tests, progressive hint tests, browser debrief |
| Progression graph | catalog dependencies and availability tests |
| Evidence explorer | bounded/filterable evidence API and browser flow |
| Accessibility | runtime axe: 0 violations / 29 passes; static gate |
| Security/assets/dependencies | security gate, asset gate, npm audit |
| Local and Docker validation | 41 tests, 12 local gates, Docker same-origin smoke |
| Live SQL/Genie | `scripts/live_sql_check.py`, `scripts/live_genie_check.py`, profile `sda` |
| Deployed runtime | deployment `01f19f9af34c19e2a70395d32935717c`, current smoke PASS; 10-run soak PASS on the prior functionally equivalent snapshot |
| Secondary deterministic coverage | six secondary Cases × five review-mode journeys |

## External or intentionally out-of-scope evidence

- Contest article publication and final article URL.
- 2–3 minute video recording/publication and video URL.
- Registration/submission form completion.
- Production live Genie Spaces for secondary Cases. They remain deterministic
  fixture/review-mode Cases until separately curated and live-evaluated.
- Final human submission decision and deadline confirmation.

These items cannot be truthfully marked complete from repository or workspace
automation alone. The repository includes drafts and a checklist for handoff.
