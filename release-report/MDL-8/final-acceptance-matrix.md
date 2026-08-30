# MAD DATA LAB — final acceptance matrix

Audited against the supplied MDL-1 through MDL-8 specifications and the current worktree/deployed runtime. CI and branch protection are excluded by owner instruction.

| Area | Acceptance evidence | Status | Remaining action |
|---|---|---:|---|
| MDL-1 canonical source | `docs/canonical-source/`; SHA-256 recorded in `docs/traceability/source-baseline.json`; foundation tests | PASS | None technical |
| MDL-2 Case #042 data | `release-report/MDL-8/databricks-remote-verification.json`; remote SQL profile `mdl`, catalog `sda_dev`, warehouse `e444f39962128242`; counts 5/23/2/14; private truth excluded; re-verified 2026-08-30 against the new Free Edition account | PASS | Production seed/rollback decision if required |
| MDL-3 Genie protocol | `scripts/live_genie_check.py`; live benchmark PASS; injection refusal PASS | PASS | None technical |
| MDL-4 guided flow/scoring | local and remote full browser flow; verdict/debrief; Python contract suite | PASS | None technical |
| MDL-5 instruments/UIX | 57 screenshots; instrument/evidence tests; responsive browser coverage; axe color-contrast | PASS | None technical; human approval excluded |
| MDL-6 hardening | `301 passed, 7 skipped`; error, resilience, security, accessibility and performance suites | PASS | None technical |
| MDL-7 release candidate | frontend build/typecheck; live smoke; live Genie; `10/10` deployed soak | PASS | None technical |
| Public routes | `36/36 PASS` across desktop/tablet/mobile: library, articles, groups, variants, feedback, comments, account, admin; language persistence and removed-entry regression included | PASS | None technical |
| Responsive UX diagnostics | `release-report/MDL-8/ui-diagnostic.json`: overflow/offscreen/broken images/empty buttons all zero; contrast PASS via axe | PASS | None technical |
| Databricks application | Redeployed 2026-08-30 under a new Free Edition account (prior account exhausted credits); URL is now `https://mad-data-lab-7474643947913626.aws.databricksapps.com`; deployment `SUCCEEDED`, app `RUNNING`, compute `ACTIVE`; root + eight routes HTTP 200 re-verified; deployed smoke re-run PASS; live Genie re-run PASS (V2/-€5.9M benchmark, injection refusal) | PASS | Deployed soak (10 journeys) re-running against new account; screenshots still reference old URL/account and should be recaptured |
| Demo video | `MDL-8-demo-narrated.mp4`; 164s, 1920×1080, H.264/AAC, required narrative generated | PASS | Human approval gate excluded by owner instruction |
| Community article | supplied article archived; local screenshot references substituted | PASS (local) | Insert final public URL(s) |
| Artwork approval | Asset and image preflights pass; human approval gate excluded by owner instruction | PASS | None |
| Public links/submission | URL is deployed and smoke-tested; challenge form not available in repo | PENDING_EXTERNAL | Final link and form acceptance |

## Current release state

`READY_TO_SUBMIT`

The state is ready for submission packaging. Only final public-link confirmation and completion of the external challenge form remain outside the repository.
