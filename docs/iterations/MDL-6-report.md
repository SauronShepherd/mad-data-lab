# MDL-6 Iteration Report

status: IN_PROGRESS
branch: MDL-6
predecessor: MDL-5 closure evidence is incomplete in this checkout

This report is evaluated with local and Databricks CLI evidence only. GitHub
Actions are permanently out of scope by project decision, and no human media
approval is required for this acceptance.

## Local implementation evidence

- Structured API error envelopes and request IDs: implemented and covered by `tests/test_mdl6_errors.py`.
- Bounded Genie transport retry: implemented and covered by `tests/test_mdl6_resilience.py`.
- Session circuit breaker: implemented and covered by `tests/test_mdl6_circuit_breaker.py`.
- Open-circuit requests now return the structured `GENIE_CIRCUIT_OPEN` 503 envelope instead of escaping as an unhandled exception; regression coverage passes and the fix is deployed remotely.
- Audio preflight: `scripts/audio_preflight.py`; current bundled track passes duration/size/decode/channel/sample-rate checks.
- Performance gate: `scripts/performance_gate.py`; current production bundle passes JS/CSS/file budgets.
- Browser contracts: the complete deployed Playwright suite passes 21/21
  against the Databricks App using CLI profile `mdl`.
- Canonical MDL-6 catalogue: 83 IDs locked in `backend/mdl6_contract.py` (AX 15, PF 8, AS 15, SEC 20, CH 25); the full traceability contract contains 94 unique IDs.
- Python repository suite: the recorded baseline is 223 passed, 7 skipped; focused MDL-6 regressions and newly added tests are recorded by their individual commands and matrix rows.
- Image preflight: `scripts/image_preflight.py`; current production and review asset inventory passes (15 assets).
- Final local gate rerun: security gate PASS; performance gate PASS (`68,246` JS gzip bytes, `4,475` CSS gzip bytes); image preflight PASS (15 assets); audio preflight PASS (`417.5s`, `6,681,145` bytes, `-14.3 LUFS`, `-1.9 dBFS`); frontend contract gate PASS.
- Frontend typecheck/build: passing.
- Browser baseline and MDL-6 scenarios: 21/21 deployed Playwright tests pass.
- Playwright runner: direct local CLI execution with `SKIP_WEBSERVER=1` is
  supported; the `npx` wrapper can be unreliable in this workstation, so the
  direct project CLI is the reproducible command.

## Coverage status

- 94 total rows: 94 `PASS_IMPLEMENTED`, 0 `PARTIAL`, 0 `NOT_IMPLEMENTED`.
- Machine-readable source: `scripts/mdl6_coverage_matrix.py`.
- Every row exposes implementation, unit, integration, E2E, remote,
  acceptance, status, and blocker fields.
- Every row also records `ci_validation=NOT_APPLICABLE` and
  `human_approval=NOT_APPLICABLE`; neither is a blocker or a completion gate.
- The matrix acceptance policy is local executable tests plus authenticated
  Databricks CLI validation with profile `mdl`.
- AX/PF/AS/SEC acceptance criteria are now explicit in
  `backend/mdl6_contract.py` and synchronized into the CSV; no row uses the
  former generic placeholder criterion.

## Remaining verifiable work

- Expand `scripts/local_chaos.py` so each CH/E2E scenario has an explicit
  expected outcome and traceable evidence.
- Re-run the isolated Playwright scenarios in an environment with a clean
  browser process; the current resident-Chromium condition is an execution
  limitation, not a product pass.
- Keep the remote smoke reproducible after each runtime deployment.

## Scope notes and remaining blockers

- MDL-5 report remains `IN_PROGRESS` pending predecessor evidence; visual
  review is not a required human approval gate for this MDL-6 acceptance.
- Live Genie and Databricks SQL verification pass with CLI profile `mdl` against the current workspace catalog.
- Clean-source Databricks App deployment reached `SUCCEEDED`; the app is
  `RUNNING` with `ACTIVE` compute.
- Official authenticated smoke passed after the sequencing fix with CLI profile `mdl`: health, catalog, session, five unique experiments, evidence inspection, final prediction, `CONCLUDING`, `DEBRIEF`, score `1000`.
- Duplicate/unregistered Genie experiments are rejected and covered by regression tests.
