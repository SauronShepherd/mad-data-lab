# MDL-1 platform verification

verified_at_utc: 2026-08-26T00:00:00Z
verified_by: Codex local implementation audit
challenge_rules_url: https://community.databricks.com/t5/learning-events/databricks-community-contest-genie-powered-app-challenge/ec-p/165825
apps_environment_url: https://docs.databricks.com/aws/en/dev-tools/databricks-apps/system-env
apps_cicd_url: https://docs.databricks.com/aws/en/dev-tools/databricks-apps/cicd-github-actions
genie_conversation_api_url: https://docs.databricks.com/aws/en/genie-agents/conversation-api
agent_mode_api_url: https://docs.databricks.com/aws/en/genie-agents/api
material_drift_detected: false
adr_or_change_reference: docs/architecture/locked-decisions.md

## Facts checked

| Fact | Recorded value | Evidence/status |
|---|---|---|
| App runtime Python | 3.11 | `docs/platform/databricks-apps-verified.md`; local package configuration |
| App runtime Node | 22.16 | `docs/platform/databricks-apps-verified.md` |
| Runtime port | `DATABRICKS_APP_PORT` | launcher and configuration tests pass |
| Genie resource boundary | `GENIE_SPACE_ID` | `app.yaml`; configuration tests pass |
| Authentication | default App identity at runtime; OIDC for CI | workflow and app configuration |
| App file limit | 10 MB per file | platform baseline; clean deployment packaging excludes `.venv` |
| Shutdown budget | 15 seconds | container shutdown smoke passes |
| Free Edition daily app compute | currently exhausted | live CLI start returns the platform quota error; closure blocked |

## Closure notes

The platform contract is recorded and implemented locally. Fresh authenticated verification of app startup, resolved runtime identity, deployed smoke, and live Genie evaluation is still required after Databricks Free Edition compute becomes available. This file must not be interpreted as a successful live deployment attestation.

## Alternate workspace deployment attempt

- Workspace: `7474654810500477` (`https://dbc-916267ef-3b9b.cloud.databricks.com`)
- Authenticated profile: `mdl-new` (`angel.alvarez.pascua@gmail.com`)
- App ID: `fe7c91e9-b565-466f-9e0a-a7dd79926135`
- Deployment ID: `01f1a1196b321dfda686ec5ec1e0a018`
- App state: `RUNNING`; compute: `ACTIVE`
- Source path: `/Workspace/Users/angel.alvarez.pascua@gmail.com/mad-data-lab/codex-clean`
- Deployed smoke result: `FAIL` at `/api/sessions/{id}/start` with HTTP 503, `Live Genie is unavailable`
- Root cause: the workspace exposes only the unrelated `Bakehouse Sales Starter Space`; no MAD DATA LAB Genie space or curated source resources are available.

This evidence proves packaging, deployment, and fail-closed runtime behavior. It does not prove live Genie closure.
