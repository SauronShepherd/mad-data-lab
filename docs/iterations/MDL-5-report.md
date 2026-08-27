# MDL-5 Iteration Report

status: IN_PROGRESS
branch: MDL-5
predecessor: MDL-4 accepted head `f7d2f4d7255373bbed4d036561ea2ff3342ba4a7`
rollback_point: `f7d2f4d7255373bbed4d036561ea2ff3342ba4a7`
deployment_profile: mdl

MDL-5 evidence is isolated under `release-report/MDL-5/`. MDL-4 evidence is
not overwritten. Requirement-level mappings are in
`docs/traceability/mdl5-requirements.csv`.

Observed repository-owned evidence is recorded in `release-report/MDL-5/`:

- local Python gate: 182 collected, 175 passed, 7 allowed compatibility skips;
- strict MDL-3, MDL-4 local, security, frontend, OpenAPI, architecture,
  traceability, accessibility-static, and visual-static gates pass;
- MDL-5 browser contract: 3 passed;
- MDL-5 manifest, runtime digest, deployment, smoke, soak, Genie, artwork,
  and CI evidence are identity-bound and explicitly pending where not observed.

The iteration cannot be marked `COMPLETE` until the MDL-5 accepted head is
recorded and GitHub CI, live Databricks smoke/soak/Genie evidence, visual
regression/axe evidence, and exact-byte human artwork approvals are present.
