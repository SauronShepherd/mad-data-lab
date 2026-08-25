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

## Live Genie smoke test

Set the Databricks CLI profile and Genie Space before starting the API:

```powershell
$env:DATABRICKS_CONFIG_PROFILE = "sda"
$env:GENIE_SPACE_ID = "01f19eb4ac691d2c88e7b18a6da39b3b"
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
`docs/community_article_draft.md`, `docs/submission_checklist.md`, and
`docs/implementation_audit.md`.

## Audio assets

The source audio pack contains five music themes, each with A/B variants. The current challenge build bundles the lightweight `mad_data_lab_curiosity.mp3` track and keeps playback muted until the player opts in. The remaining source tracks stay outside the deployment payload until a soundtrack selector is added.
