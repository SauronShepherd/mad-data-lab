# MAD DATA LAB — MDL-8 final audit

Audit date: 2026-08-29  
CI: excluded by owner instruction.  
Authoritative release state: `ENGINEERING_COMPLETE_SUBMISSION_FORM_PENDING`

## Verified engineering requirements

| Scope | Evidence | Result |
|---|---|---:|
| MDL-1 canonical domain and source baseline | `docs/canonical-source/`, `release-report/MDL-1/`, foundation/domain tests | PASS |
| MDL-2 deterministic Case #042 and public/private boundary | `release-report/MDL-8/databricks-remote-verification.json`, SQL/data contract tests | PASS |
| MDL-3 closed Genie protocol and evidence identity | `scripts/validate_mdl3_contract.py --strict` (29/29), live Genie evidence | PASS |
| MDL-4 guided flow, scoring and verdict | `tests/browser/app.spec.ts`, `tests/browser/experiment-rationale.spec.ts`, MDL-4 contract tests | PASS |
| MDL-5 instruments, evidence explorer and visual system | instrument tests, asset preflight, responsive/a11y evidence | PASS |
| MDL-6 resilience, security, accessibility and performance | Python suite: 301 passed, 7 skipped with documented supersession | PASS |
| MDL-8 public routes and controls | `tests/browser/mdl8-public-surfaces.spec.ts`: 36/36 across desktop/tablet/mobile | PASS |
| Article language persistence | authenticated desktop and mobile route tests; reload verification | PASS |
| Removed article entry | regression test confirms `Apache Spark WTF???` is not rendered | PASS |
| Frontend and assets | frontend contract gate, image preflight (15), audio preflight (479.2 s) | PASS |
| Databricks runtime | profile `mdl`; deployment `01f1a3b1a47f16d2af86f0df250dc483`; `SUCCEEDED/RUNNING/ACTIVE` | PASS |
| Remote application behavior | authenticated smoke: health, catalog, session, experiments, evidence, verdict, debrief | PASS |
| Submission archive | `release-report/MDL-8/mad-data-lab-submission-package-v10.zip`; 86 entries; manifest included | PASS |

## Measured UI/UX diagnostics

`release-report/MDL-8/ui-diagnostic.json` records, for desktop, tablet and mobile:

- horizontal overflow: 0;
- off-screen elements: 0;
- broken images: 0;
- empty/unresponsive button findings: 0;
- basic contrast: manual review still required.

The mobile topbar overlap discovered during the final audit was corrected in `src/styles.css`, rebuilt, tested in isolation and redeployed.

## External gates not claimable by automation

The following remain outside the repository:

- external source fingerprint confirmation;
- final public-link confirmation and challenge submission-form acceptance.

No submission ID or public publication status is inferred from local files or simulated by this audit. Human approval gates are excluded by owner instruction.

## Final handoff

Use `docs/MDL-8-submit-runbook.md` and `release-report/MDL-8/mad-data-lab-submission-package-v10.zip`. Re-run the manifest after any content change; do not submit an older archive whose hashes predate the final source or evidence.
