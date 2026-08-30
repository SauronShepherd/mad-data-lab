# MAD DATA LAB

Local-first React + FastAPI game foundation for the Databricks Genie-Powered App challenge.

## Local run

```powershell
npm install
python -m pip install -e ".[dev]"
uvicorn server.main:app --reload --port 8000
```

In a second terminal:

```powershell
npm run dev
```

The UI calls the local API at `http://localhost:8000`. Without `GENIE_SPACE_ID`, the API uses the deterministic Case #042 fixture path. In Databricks Apps, `app.yaml` maps the `genie-space` resource to `GENIE_SPACE_ID`; the backend then uses the Genie Conversation API and validates the response against the registered experiments.

Runtime configuration is centralized in `server/config.py`. Local development may set `ALLOW_FIXTURE_MODE=1`; deployed Apps set it to `0` in `app.yaml`, so a missing live Genie binding fails closed. `CHALLENGE_REVIEW_MODE` is `0` by default and does not unlock secondary Cases. `DATABRICKS_APP_PORT` takes precedence over `UVICORN_PORT` when the App launcher selects its listening port.

## Live Genie smoke test

Set the Databricks CLI profile and Genie Space before starting the API:

```powershell
$env:DATABRICKS_CONFIG_PROFILE = "mdl"
$env:GENIE_SPACE_ID = "01f1a11f6c281e79bd1e0c448055fbdd"
uvicorn server.main:app --port 8000
```

The live path starts a stateful Genie conversation and asks Genie to select the next registered Experiment. If the Space is not configured, the same UI remains playable through the deterministic fixture path.

## Databricks App deployment

Build the frontend, import the project, and deploy it to the existing app:

```powershell
npm run build
databricks workspace import-dir . /Workspace/Users/<user-email>/mad-data-lab --overwrite -p sda
databricks apps deploy mad-data-lab `
  --source-code-path /Workspace/Users/<user-email>/mad-data-lab `
  -p sda --timeout 20m
```

For the reproducible Make target, set `DATABRICKS_SOURCE_PATH` to the workspace path and run `make deploy-staging`.

The deployed app must have an App resource named `genie-space` with `CAN_RUN` permission and the Genie Space ID above. Production frontend requests are same-origin; Vite development requests use `http://localhost:8000`.

Useful contracts:

- `GET /api/cases` — catalog and lock state.
- `GET /api/cases/{case_id}/experiments` — required Experiment IDs and readiness.
- `POST /api/investigations` — start a Case conversation.
- `POST /api/experiments/next` — let Genie or the fixture choose the next Experiment.
- `POST /api/genie/ask` — optional free-form Dr. Genie console.

## Checks

```powershell
npm run build
python -m compileall server
python -m unittest discover -s tests -v
python scripts/release_check.py
```

The hidden case truth is not sent to Genie. Only curated experiment context and the player's prediction are included in follow-up prompts.

Submission support artifacts are in `docs/architecture.md`,
`docs/community-article.md`, `docs/submission-checklist.md`,
`docs/iterations/MDL-8-final-audit.md`, and `docs/MDL-8-submit-runbook.md`.

## Audio assets

The source audio pack contains five music themes, each with A/B variants. The current challenge build bundles the lightweight `mad_data_lab_curiosity.mp3` track and keeps playback muted until the player opts in. The remaining source tracks stay outside the deployment payload until a soundtrack selector is added.
# MDL-3 local contract and evidence commands

The deterministic local checks for the Genie-at-the-core boundary are:

```text
python scripts/validate_mdl3_contract.py --strict
python scripts/run_mdl3_benchmark.py
python scripts/configure_genie.py --catalog workspace --schema mad_data_lab
```

`run_mdl3_benchmark.py` is a fixture contract check, not live Genie evidence.
Authenticated evidence must be validated with explicit identities:

```text
make validate-live-evidence LIVE_EVIDENCE=release-report/MDL-3/live.json \
  IMPLEMENTATION_SHA=<sha> \
  GENIE_CONTRACT_DIGEST=<digest> \
  GENIE_LIVE_CONFIG_SHA256=<digest> \
  MDL2_DATA_CONTRACT_DIGEST=<digest> \
  CASE_HASH=<sha256>
```

The release gate includes the strict contract and fixture benchmark checks.
