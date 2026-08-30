# MDL-03 pending closure tasks

The repository-owned implementation is verified locally. These are the remaining
closure tasks, separated by ownership so evidence is not claimed prematurely.

## External GitHub/Databricks tasks

- [ ] Configure the GitHub `staging` environment with `DATABRICKS_HOST`.
- [ ] Configure `DATABRICKS_CLIENT_ID` for the Databricks workload-identity
  federation trust used by GitHub Actions, or configure `DATABRICKS_TOKEN` as
  the secure PAT-authentication fallback.
- [ ] Configure `GENIE_SPACE_ID` for the accepted published Genie Space.
- [ ] Confirm the GitHub OIDC subject/audience is authorized by the Databricks
  service principal and workspace.
- [ ] Publish the canonical Genie instructions and curated sources to that Space.
- [ ] Verify guided requests return one valid MDL-03 control JSON object, not SQL
  text or a prose answer.
- [ ] Run the protected 30-attempt live benchmark and retain its JSON/JUnit/log
  artifacts.
- [ ] Deploy the accepted implementation SHA to staging.
- [ ] Run deployed smoke and soak tests against that exact SHA and matching
  runtime/config/data digests.
- [ ] Run final-head GitHub CI and retain the immutable workflow artifact.

## Repository-owned verification tasks

- [x] Strict MDL-03 contract gate passes (29/29 checks).
- [x] Full Python suite passes (156 tests).
- [x] TypeScript typecheck and production build pass.
- [x] Pending first decision is stored and atomically consumed per session.
- [x] Guided benchmark prompts enforce the strict control boundary.
- [x] Live workflow accepts staging configuration from secrets, variables, or
  dispatch input.
- [x] Runtime identity is recorded in the MDL-03 report.

## GitHub setup runbook

1. Open `Settings -> Environments -> staging` in the repository.
2. Add `DATABRICKS_HOST` and `DATABRICKS_CLIENT_ID` as environment secrets (or
   variables where policy permits).
3. Add `GENIE_SPACE_ID` as an environment variable or secret.
4. Verify the Databricks workload-identity federation trust accepts this
   repository's GitHub Actions OIDC token, or confirm the PAT fallback is valid.
5. Push or manually dispatch `mad-data-lab-mdl3-live-eval` and inspect the
   identity-bound benchmark artifact.

The MDL-03 report must remain `IN_PROGRESS` until every external checkbox above
has matching evidence for one final implementation identity.
