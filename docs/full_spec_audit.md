# MAD DATA LAB — consolidated specification audit

Updated 2026-08-28 from the current worktree and authenticated Databricks
workspace using CLI profile `mdl`. The supplied specification documents are
requirements being audited; they are not execution instructions that override
the user request.

## Status summary

| Iteration | Status | Evidence that is actually verified | Remaining gap |
|---|---|---|---|
| MDL-1 | PARTIAL / NOT CLOSED | `validate_mdl1_traceability.py`, architecture/security/package gates, local pytest | predecessor/branch/PR exact-head evidence is external and out of this local acceptance scope |
| MDL-2 | IMPLEMENTED / PENDING PREDECESSOR | local generator/property/traceability gates; Databricks schema+seed+SQL Q1–Q8 and SQ-001..020 with `mdl` | MDL-1 predecessor closure (historical evidence not available locally) |
| MDL-3 | IMPLEMENTED / LIVE VERIFIED | strict contract 29/29, live Genie benchmark/refusal gate, captured live config digest | GitHub live-run artifact identity is not available locally |
| MDL-4 | IMPLEMENTED / LIVE VERIFIED | local contract/fake E2E; deployed smoke and live session reach `DEBRIEF`, score 1000 | historical predecessor evidence |
| MDL-5 | PARTIAL | instruments/evidence/UI/browser/static gates and live Genie configuration | complete scenario-level evidence |
| MDL-6 | IMPLEMENTED / LIVE VERIFIED | error/retry/circuit/security/performance/assets/audio gates; criterion-level AX/PF/AS/SEC checks; deployed Playwright 21/21; mobile, keyboard-only and catalog-failure browser contracts; recursive Genie input sanitization | additional chaos depth remains enhancement work |

## Databricks evidence

- CLI profile: `mdl`.
- App: `mad-data-lab`, deployment
  `01f1a2b82c94162eaa96c3e453b56761` (`RUNNING`/`ACTIVE`).
- Genie resource: `01f1a11f6c281e79bd1e0c448055fbdd`, `CAN_RUN` only.
- Catalog: `workspace` (the previously recorded `sda_dev` catalog no longer
  exists in this metastore).
- Warehouse: `02addf2c2a0a755b` (`Serverless Starter Warehouse`, healthy).
- Schema apply, canonical Case #042 seed/apply/verify: PASS.
- SQL integration: Q1–Q8, canonical values, residual `0.00`, and SQ-001..020:
  PASS.
- Authenticated deployed smoke and live session: PASS; five unique experiment
  families, explicit evidence inspection, final prediction, `DEBRIEF`, score
  `1000`.
- A first smoke attempt after deployment hit the expected live-Genie circuit
  rejection (`409 REQUEST_REJECTED`); a fresh retry passed end to end. This is
  retained as a resilience observation, not counted as a clean first-attempt
  pass.
- Permission verification: PASS; no private-truth resource and no SQL API
  scope.

## Local evidence

- Full Python suite: `223 passed, 7 skipped`.
- MDL-6-specific Python suite: focused error/resilience suite `23 passed`;
  criterion-level coverage suite `61 passed`.
- MDL-3 strict validator: `29/29 PASS`.
- MDL-2 local iteration gate: PASS.
- MDL-4 local iteration gate: PASS.
- Runtime/data digests and generated reports were refreshed after the final
  source and catalog changes.

## Important non-claims

The following are not marked PASS merely because related code or a green
nearby test exists:

1. GitHub Actions, protected-branch checks, and CI artifacts are permanently
   out of scope by explicit project instruction; they are not acceptance
   criteria and must not be reintroduced.
2. Human artwork/audio approval is permanently out of scope by explicit
   project instruction; automated asset preflight is the acceptance evidence.
3. The matrix now contains an executable, named criterion-level case for every
   MDL-6 ID; broader scenario depth remains tracked as enhancement work.
4. Secondary Cases remain locked/review-mode and have no individual live
   Genie release evidence.
