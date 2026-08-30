# MDL-8 submission package report

Status: IN_PROGRESS — engineering evidence is being generated for the current source tree.

## Scope completed in this iteration

- Corrected the public flow so `OPEN CASE BOARD` opens the Case Board before `OPEN CASE` and briefing.
- Added Chromium-based desktop, tablet and mobile Playwright projects.
- Added repeatable screenshot capture and measurable UI diagnostics in `scripts/capture_mdl8_evidence.mjs`.
- Preserved historical MDL-1 through MDL-7 artifacts and traceability as regression inputs.
- Archived the supplied canonical V3 source and all supplied MDL-1 through MDL-8 specifications under `docs/canonical-source/`; the canonical manual SHA-256 matches the recorded fingerprint.

## Audit findings still open

Implemented and smoke-tested public SPA routes for library, articles, variants, groups, feedback, account/subscription and administration, including deep-link fallback in the server. Language/theme preferences and feedback persist locally. Dedicated comments and authenticated subscription backends remain out of scope for this local release candidate and are explicitly not represented as complete server features.

The historical regression suite initially reported 22 failures, mostly because predecessor evidence was absent from the MDL-8 checkout. Historical artifacts, MDL-2 digest metadata, MDL-3 digest freshness, MDL-6 CSV synchronization and technical-debt explanations have now been reconciled; the full Python suite is green.

## Evidence

- `release-report/MDL-8/screenshots/` — generated per viewport and screen.
- 57 PNG captures currently cover landing, Case Board, briefing, Experiments 1–5, verdict, debrief and all eight public routes across desktop, tablet and mobile.
- `release-report/MDL-8/ui-diagnostic.json` — overflow, off-screen controls, broken images and unlabeled empty buttons.
- `tests/browser/mdl8-public-surfaces.spec.ts` — expanded public-surface navigation/control suite: `36/36 PASS` across desktop, tablet and mobile, including variants, comments, subscription response, administration, language, theme, feedback persistence and the removed-entry regression.
- `npm run build` and `npm run typecheck` — PASS after the flow correction.
- `release-report/MDL-8/databricks-remote-verification.json` — REMOTE_SQL_VERIFIED against profile `mdl`, catalog `workspace`, and the discovered serverless warehouse; canonical Case #042 counts reconciled 5/23/2/14 and private truth excluded.
- `release-report/MDL-8/databricks-app-deployment.json` — deployment against profile `mdl` is SUCCEEDED; app is RUNNING, compute ACTIVE, and root plus all eight public routes returned HTTP 200.
- `release-report/MDL-8/deployed-smoke-live.txt` — authenticated deployed smoke PASS after redeploy.
- `release-report/MDL-8/deployed-soak-live.json` — authenticated 10/10 Case #042 journeys PASS, including live Genie, evidence inspection, verdict and debrief.
- `release-report/MDL-8/MDL-8-demo.mp4` — generated 164-second 1920×1080 H.264/AAC demo using verified desktop evidence; technical format PASS. Human narration/cursor review remains pending.
- `release-report/MDL-8/demo-video-verification.json` — machine-readable video verification.
- `release-report/MDL-8/demo-video-frame-80s.png` — extracted frame reviewed for readable 16:9 composition, no developer tools, no personal secrets and visible snapshot evidence.
- `release-report/MDL-8/MDL-8-demo-narrated.mp4` — 164-second 1920×1080 narrated variant generated with the required MDL-8 narrative and project music mixed underneath; technical format PASS. Human review gate is excluded by owner instruction.
- `release-report/MDL-8/final-acceptance-matrix.md` — requirement-by-requirement acceptance matrix for MDL-1 through MDL-8 with evidence and remaining actions.
- `release-report/MDL-8/submission-manifest.json` — SHA-256 manifest for 85 frozen source/spec/evidence files.
- `release-report/MDL-8/mad-data-lab-submission-package-v2.zip` — 328-entry submission archive; verified to contain the manifest and narrated demo and not contain itself.
- `release-report/MDL-8/mad-data-lab-submission-package-v3.zip` — refreshed freeze package after the final report update; embedded `submission-manifest.json` matches the current manifest byte-for-byte.
- Final responsive fix: moved public navigation controls out of the narrow mobile topbar to prevent overlap with audio/settings controls; isolated mobile regression test passes, and deployment `01f1a3b1a47f16d2af86f0df250dc483` is `SUCCEEDED/RUNNING/ACTIVE`.
- Final authenticated smoke against deployment `01f1a3b1a47f16d2af86f0df250dc483`: PASS (health, catalog, session, experiments, evidence inspection, verdict and debrief); raw output is in `release-report/MDL-8/deployed-smoke-final.txt`.
- `docs/canonical-source/` plus `docs/traceability/source-baseline.json` — canonical-source archive and fingerprint verification PASS.
- Release-candidate orchestration passed all local gates through artwork preflight (lint, typecheck, unit, data, SQL preflight, E2E, visual, assets, security, frontend contract and art preflights). The aggregate browser gate was not completed by the runner within its execution window; its dedicated suites remain the authoritative browser evidence: Case flow PASS, MDL-6 PASS and public surfaces 27/27 PASS.

## External gates not self-approvable

Human artwork approval, public-link validation, demo recording and submission-form acceptance remain PENDING until their external evidence is collected. CI/branch protection are intentionally excluded from this project scope by owner instruction. The comments/subscription surfaces are local-release UI flows; authenticated persistence and payment integration are not claimed. This report does not mark those external capabilities PASS.
