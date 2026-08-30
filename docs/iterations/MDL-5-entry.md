# MDL-5 Iteration Entry and Release Contract

status: IN_PROGRESS
iteration: MDL-5
branch: MDL-5
predecessor_iteration: MDL-4
predecessor_branch: MDL-5 (accepted predecessor content carried from MDL-4)
predecessor_accepted_sha: f7d2f4d7255373bbed4d036561ea2ff3342ba4a7
predecessor_ci_run: 33082673080 (green)
rollback_point: f7d2f4d7255373bbed4d036561ea2ff3342ba4a7

## Purpose

Make the Case #042 investigation analytically legible through validated,
registry-controlled Instruments and an auditable Evidence Explorer, while
preserving the server-authoritative MDL-4 game flow.

## Allowed scope

- Semantic visual tokens, typography, responsive Investigation shell, and reduced-motion behavior.
- Registry-controlled KPI, waterfall, snapshot, evidence, DQ, formula, lineage, and reconciliation Instruments.
- API-backed Evidence Explorer filtering, record inspection, pagination, and lineage drill-down.
- Component, contract, browser, accessibility, visual, asset-preflight, and deployment-smoke coverage.
- MDL-5 artwork A08-A13 and its manifest, previews, and human approval record.

## Prohibited scope

- Changing MDL-4 scoring, completion, private-truth, Genie protocol, or predecessor evidence semantics except for regression fixes.
- Adding secondary playable Cases or arbitrary Genie/model-driven component imports.
- Treating generated artwork as functional UI or embedding analytical claims in images/CSS.
- Marking human approval, GitHub settings, live Genie evaluation, or deployment acceptance from local tests alone.

## Release blockers

- Any failed mandatory local or CI gate.
- Any stale or identity-inconsistent MDL-5 manifest/evidence artifact.
- Missing/invalid Instrument or Evidence Explorer contract.
- Serious/critical accessibility violation, critical responsive clipping, or evidence N+1 behavior.
- Missing exact-byte human approval for A08-A13.
- Missing accepted staging deployment and live Genie evidence.

## Automated gates

- Full pytest through `scripts/pytest_gate.py` with JUnit output.
- Security, frontend contract, OpenAPI, MDL-1 traceability, production architecture.
- MDL-2 contract, MDL-3 strict contract/benchmark, MDL-4 local gate.
- Frontend build/typecheck, Playwright browser contract, visual and accessibility gates.
- Databricks bundle validation/deployment and authenticated smoke/soak where available.

## External and human blockers

- GitHub exact-head CI for the accepted MDL-5 commit.
- Databricks live Genie five-experiment smoke/soak and evaluation.
- Human exact-byte artwork approval for MDL-5 A08-A13 and inherited approvals.
- Confirmation of the intended staging identity for Databricks profile `mdl`.

## Evidence rule

Every requirement is tracked in `docs/traceability/mdl5-requirements.csv` and
must point to implementation, tests, and a release artifact. A report sentence
alone is not completion evidence.
