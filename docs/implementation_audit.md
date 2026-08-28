# MAD DATA LAB implementation audit

Updated after Databricks deployment `01f1a2b82c94162eaa96c3e453b56761` and authenticated smoke.

The requirement-by-requirement consolidated audit is maintained in
[`docs/full_spec_audit.md`](full_spec_audit.md).

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
| Accessibility | static/runtime gates pass; deployed Playwright suite 21/21, including AX-001..015 criterion coverage |
| Security/assets/dependencies | security gate, asset gate, npm audit |
| Local and Docker validation | 66 tests, 23 local gates, current Docker image build and same-origin smoke |
| Live SQL/Genie | `scripts/live_sql_check.py`, `scripts/live_genie_check.py`, CLI profile `mdl` |
| Deployed runtime | Databricks App `mad-data-lab`; clean-source deployment, 21/21 deployed E2E and authenticated smoke PASS (`DEBRIEF`, score 1000) |
| Secondary deterministic coverage | six secondary Cases × five review-mode journeys |

## External or intentionally out-of-scope evidence

- Contest article publication and final article URL.
- 2–3 minute video recording/publication and video URL.
- Registration/submission form completion.
- Production live Genie Spaces for secondary Cases. They remain deterministic
  fixture/review-mode Cases until separately curated and live-evaluated.
- Final human submission decision and deadline confirmation.
- CI and human artwork/audio approvals are intentionally not acceptance gates
  for this project. Local tests and authenticated Databricks CLI profile `mdl`
  are authoritative.

These items cannot be truthfully marked complete from repository or workspace
automation alone. The repository includes drafts and a checklist for handoff.
