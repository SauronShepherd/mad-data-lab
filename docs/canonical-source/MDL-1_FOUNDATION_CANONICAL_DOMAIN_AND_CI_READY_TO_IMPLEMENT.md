# MDL-1 - Foundation, Canonical Domain Model, Repository Architecture, and CI/CD

## Iteration contract metadata

| Field | Locked value |
|---|---|
| Iteration | `MDL-1` |
| Required branch | `MDL-1` |
| Depends on | none; starts from accepted current `main` |
| Definitive source | V3.0, 2026-08-23, planning SHA-256 `237570e5d62cee11e78ecced43c8449f62f53e7b547e9fe1bfbf4ed54eb0cc44` unless an approved addendum/replacement is merged |
| Document maturity | `READY_TO_IMPLEMENT` — implementation may start once the Entry Gate is recorded |
| Primary V3 closure sections | §§1,2,4–10,24–26 |
| Secondary V3 slices initialized here | §22 assets A01/A02/A21/A28; §§42–46 test/CI traceability bootstrap |
| Required art/media gate | A01, A02, A21, A28 |
| Deployment target | Free Edition staging/challenge app |
| Human gate before closure | exact-byte artwork/media approval + iteration-specific allowed manual inspection/acceptance |
| Closure status vocabulary | `IN_PROGRESS`, `BLOCKED`, `COMPLETE` (never infer COMPLETE from partial green checks) |

## Purpose

This iteration converts the current early-stage scaffold into a reproducible, testable, branch-driven engineering baseline that future iterations can safely build on. It also replaces the prototype game vocabulary with the canonical MAD DATA LAB domain model and prepares the repository for the automated test pyramid defined in the definitive V3 specification.

This iteration is not finished when the application merely runs locally. It is finished only when:

1. the repository installs and builds from a clean checkout;
2. the canonical Case / Investigation / Experiment vocabulary is represented in code;
3. the Case catalog and state machine are server-authoritative;
4. GitHub CI runs automatically and is green on the `MDL-1` branch and on `main` after merge;
5. a Databricks staging deployment is successful and automatically smoke-tested;
6. every MDL-1 production artwork asset (A01, A02, A21, A28) is generated, technically preflighted, integrated, and explicitly approved by a human on the exact production bytes;
7. all completion evidence is written to an iteration report.

## Entry gate — prerequisites before Codex changes production code

MDL-1 is mature enough to start only when the following entry conditions have been checked. Codex may inspect/read the repository before they are all satisfied, but it must not claim implementation work has started until the entry record exists.

Create `docs/iterations/MDL-1-entry.md` and record `PASS`, `BLOCKED`, or `NOT_APPLICABLE` for each item:

| ID | Entry requirement | Required evidence | Blocking? |
|---|---|---|---|
| `MDL1-ENTRY-001` | Definitive V3 source is available and SHA-256 matches the accepted baseline or approved addendum chain. | source path + SHA-256 + amendment list | yes |
| `MDL1-ENTRY-002` | Git remote is the intended MAD DATA LAB repository and `main` can be fetched. | sanitized `git remote -v`, `origin/main` SHA/tree | yes |
| `MDL1-ENTRY-003` | Codex can create/push `MDL-1` or has a precise GitHub blocker recorded. | push permission probe/PR access | yes for closure; implementation may proceed locally if blocked |
| `MDL1-ENTRY-004` | GitHub Actions are enabled for the repository. | workflow/API/settings evidence | yes for closure |
| `MDL1-ENTRY-005` | Target Databricks workspace/app is identified and the Free Edition attestation process has an owner. | workspace alias/non-secret ID + verifier | yes for platform work |
| `MDL1-ENTRY-006` | Databricks CLI/API access exists for the deployment identity or a human/admin blocker is recorded. | CLI auth probe without secrets | yes for deployment |
| `MDL1-ENTRY-007` | A human artwork approver is identified and understands that Codex cannot self-approve. | approver name/role or explicit pending owner | yes for art closure |
| `MDL1-ENTRY-008` | Image-generation capability or a human generation path is available for A01/A02/A21/A28. | tool/path + rights basis | yes for art closure |
| `MDL1-ENTRY-009` | Existing uncommitted work is absent or safely preserved. | empty `git status --porcelain` | yes |
| `MDL1-ENTRY-010` | Current app can be reproduced enough to establish a migration baseline, or its failure is captured. | current tests/build/release-check baseline | no; failure becomes migration evidence |

The entry record is not a waiver mechanism. A required item that cannot be satisfied receives one of the standard blocker codes and remains open.

### Baseline capture before refactoring

Before moving files, capture the current scaffold behavior so regressions caused by migration are distinguishable from pre-existing defects. Record:

```text
current main SHA/tree
current package manifests/lock presence
current Python test result
current release_check result
current frontend build result from a clean dependency install
current /health payload if runnable
current /api/cases payload if runnable
current production asset inventory and hashes
known pre-existing failures
```

Do not make pre-existing defects disappear from history by rewriting the baseline after the refactor.

## Explicit MDL-1 non-goals / scope guard

MDL-1 establishes the platform on which the remaining iterations can be implemented. It must **not** expand into later-iteration product work merely because a stub is convenient. Unless required to prove an MDL-1 contract, defer these items to their owning iterations:

- full Case #042 deterministic data regeneration, curated SQL views, lineage data, or mutation engine execution — MDL-2;
- live Genie conversation orchestration, protocol parsing/repair, experiment selection, query attachment execution, and live benchmark evaluation — MDL-3;
- full guided Case #042 loop, scoring, badges, hints, final prediction, early reveal, and server-validated verdict — MDL-4;
- production analytical Instruments/Evidence Explorer and full screen polish — MDL-5;
- final accessibility/security/chaos/performance/audio hardening — MDL-6;
- release soak/final manual functional acceptance — MDL-7;
- demo video/community article/submission freeze — MDL-8.

MDL-1 may create typed interfaces, registries, placeholders, and fixture boundaries required by later work, but those placeholders must be obvious, non-analytical, and impossible to mistake for completed production behavior. In particular, MDL-1 must not hardcode future Genie answers, final verdicts, or Case #042 evidence into the browser merely to make the skeleton look finished.

## Mandatory execution order

Codex should execute this iteration in the following order. Later phases may prepare in parallel only when they cannot invalidate an earlier gate; closure order remains strict. The technical focus of MDL-1 is **repository/toolchain + canonical domain/state + CI/CD foundation**.

| Phase | Required action | Exit condition |
|---:|---|---|
| 0 | Read this entire file, the accepted V3 source/addenda, current `main`, predecessor evidence, and current platform-verification record. | No unresolved source/predecessor ambiguity; blockers recorded rather than guessed around. |
| 1 | Verify clean `main`, predecessor/source hashes, then create/inspect branch `MDL-1` exactly as specified. | Correct branch/base/tree recorded; no unrelated local work. |
| 2 | Start this iteration's required artwork/audio production immediately after branch creation using the locked prompt/reference/provenance rules. | Candidate generation request/prompt + manifest state recorded. Human approval may remain pending while engineering continues. |
| 3 | Implement the iteration-owned product/data/Genie/UI/hardening requirements in small test-backed commits. | Owned functionality exists without bypasses/placeholders in production paths. |
| 4 | Run the lowest-layer deterministic/static/contract suites continuously, then the complete local iteration gate. | Mandatory local gates green; no hidden skip/xfail/zero-test condition. |
| 5 | Preflight final candidate artwork/audio and obtain **explicit human approval of the exact production bytes**. | Approval record says `APPROVED`, approver/time/provenance present, recorded SHA-256 matches bytes. Rejection loops back to Phase 2. |
| 6 | Commit all approved runtime-affecting content, push the final head, open/update the PR, and run required GitHub CI on that exact head. | Required GitHub checks green on `implementation_sha`; no stale CI evidence. |
| 7 | Deploy that exact accepted implementation identity to the required Databricks environment and run automated post-deploy validation. | Deployment/build identity matches accepted runtime digest; smoke/integration gates green. |
| 8 | Perform only the manual inspection/acceptance explicitly allowed in this iteration and record objective observations. | No unaddressed manual defect; any defect has regression test + fix + invalidated gates rerun. |
| 9 | Generate sanitized closure evidence/report/manifest, classify any report-only diff, merge through protected GitHub flow, and verify post-merge `main`. | `main` CI/deployment obligations green; iteration closure `COMPLETE`; next iteration predecessor gate can pass. |

**Do not advance merely because engineering code is complete.** Human asset approval, exact-head GitHub CI, Databricks deployment evidence, and post-merge verification are part of the iteration, not administrative follow-up.

## Source-of-truth hierarchy

When implementation details conflict, use this order:

1. Current Databricks Genie-Powered App Challenge requirements.
2. `MAD_DATA_LAB_Complete_Game_Specification_and_Manual.md`, Version 3.0.
3. The current repository only as a migration source, never as a source of product truth.
4. Implementation convenience.

Locked product invariants for this iteration:

- Product brand: `MAD DATA LAB`.
- Track: Track B - Creative Thinking.
- Main release blocker: Case #042 - The Missing EUR 6.8M.
- Canonical hierarchy: MAD DATA LAB -> Case -> Investigation -> Experiment -> Evidence -> Hypothesis Update -> Scientific Verdict.
- Genie remains the adaptive scientist in later iterations; do not create architecture that would prevent that.
- `CASE_TRUTH` remains backend/private and inaccessible to Genie or browser code.
- Secondary Cases may exist in the catalog but must not become playable unless their own automated contracts are later satisfied.
- Functional correctness comes from automation. Human review in this iteration is limited to visual/art approval and deployment/log inspection.

## Current challenge rules snapshot — revalidate before implementation and before final submission

Create `docs/challenge/verified-rules.md`. On 2026-08-24 the official challenge page states that entrants must build a **Databricks App on Free Edition with a Genie Agent at its core**, choose a track, publish a Community Article/project story, create a demo, and submit the registration form. The challenge closes **August 31, 2026 at 11:30 PM PDT**. Judging is 40 points: **Genie at the Core 20**, selected-track execution 10, App Experience 10. MAD DATA LAB is locked to **Track B — Creative Thinking**.

Official rule source to record:

```text
https://community.databricks.com/t5/learning-events/databricks-community-contest-genie-powered-app-challenge/ec-p/165825
```

The architecture implication is non-negotiable even though live Genie orchestration is implemented in MDL-3: MDL-1 must not establish a product path where removing Genie leaves the finished main investigation essentially unchanged. Any fixture/static scaffolding is test/development infrastructure, not an alternative production game.

Record in the verification file:

```text
verified_at_utc
source_url
free_edition_required
genie_at_core_required
track: Track B - Creative Thinking
points_genie_core: 20
points_track: 10
points_app_experience: 10
submission_close_pdt
project_story_requirements
demo_requirement
registration_requirement
source_changed_since_previous_verification: true|false
verifier
```

Add checks:

- `MDL1-CHAL-001` — challenge verification file exists, is current for the iteration start, and identifies Free Edition + Genie-at-Core;
- `MDL1-CHAL-002` — product metadata declares Track B;
- `MDL1-CHAL-003` — architecture ADR explicitly states that fixture/offline mode is not a production substitute for Genie;
- `MDL1-CHAL-004` — a change in official challenge rules invalidates the corresponding planning assumptions until reviewed.

## Current platform assumptions snapshot — revalidate at implementation start

The following platform facts were verified against current official Databricks documentation on 2026-08-24. They are implementation constraints, not eternal assumptions. Codex must record revalidation in `docs/platform/databricks-apps-verified.md`; if current documentation differs, stop and reconcile through the source-of-truth hierarchy before coding around the difference.

| Area | Verified platform contract used by MDL-1 | Implementation consequence |
|---|---|---|
| Apps runtime | Ubuntu 22.04, Python 3.11, Node.js 22.16; current environment also documents `uv`. | target Python 3.11 and Node 22.16; do not depend on unsupported system packages/root operations |
| Hybrid deploy | A root `package.json` triggers Node dependency install/build in addition to Python install. | keep the production `package.json` at app root and define a deterministic `build` script |
| Python dependency precedence | `requirements.txt` takes precedence; `pyproject.toml` + `uv.lock` uses `uv` when `requirements.txt` is absent. | MDL-1 locks on `pyproject.toml` + `uv.lock`; do not leave a stray production `requirements.txt` |
| Node build deps | Deployment can skip `devDependencies` when `NODE_ENV=production`; build-required packages must be available during deployment. | React/Vite/TypeScript/plugin and all packages required by the production build belong in `dependencies`; test-only packages may be dev dependencies |
| Port/runtime env | Databricks provides `DATABRICKS_APP_PORT`; FastAPI/Uvicorn compatibility variables are also supplied. | one launcher resolves runtime port; production cannot silently fall back to local 8000 |
| Genie App resource | Genie Agent App resources expose a Genie **space ID**, conventionally as `GENIE_SPACE_ID` via `valueFrom: genie-space`. | use `GENIE_SPACE_ID` at the platform boundary and one normalized internal setting |
| App identity | Apps receive a dedicated service-principal identity/credentials automatically. | runtime code uses default Databricks authentication; never hardcode or surface those credentials |
| Resource permissions | App SP needs `CAN RUN` on Genie, `CAN USE` on warehouse, and relevant UC `USE`/`SELECT` when those resources are used. | separate deployment-SP permissions from runtime App-SP permissions and verify both |
| Git deploy source | Current Bundle/App schemas support `git_repository` plus `git_source` with branch/tag/commit and expose `resolved_commit`. | prefer commit-pinned staging deployment or fail unless `resolved_commit == implementation_sha` |
| GitHub CI/CD | Databricks recommends GitHub OIDC/workload identity federation and `bundle validate` → `bundle deploy` → `bundle run`. | no long-lived Databricks secret in GitHub when OIDC is available |
| App files | Individual app files must remain under the Databricks Apps file-size limit (currently 10 MB). | internal media budgets are stricter; CI scans every deployable file |
| Shutdown | Databricks Apps best practices require graceful shutdown within the platform window (currently 15 s before forced kill). | launcher/server must not trap SIGTERM indefinitely; add a bounded shutdown smoke test |

Official references to record in the verification file:

```text
https://docs.databricks.com/aws/en/dev-tools/databricks-apps/system-env
https://docs.databricks.com/aws/en/dev-tools/databricks-apps/dependencies
https://docs.databricks.com/aws/en/dev-tools/databricks-apps/app-runtime
https://docs.databricks.com/aws/en/dev-tools/databricks-apps/genie
https://docs.databricks.com/aws/en/dev-tools/databricks-apps/resources
https://docs.databricks.com/aws/en/dev-tools/databricks-apps/cicd-github-actions
https://docs.databricks.com/aws/en/dev-tools/databricks-apps/best-practices
https://docs.databricks.com/aws/en/dev-tools/bundles/resources
https://docs.databricks.com/api/apps/v1
```

A current official-doc change is **platform drift**, not permission to silently weaken the iteration. Record the changed contract and the exact spec-preserving adaptation.

## Locked consolidation decisions D-001 through D-011

MDL-1 owns V3 §2. Codex must preserve these decisions across all later iterations. Put them in `docs/architecture/locked-decisions.md` (or equivalent ADR index) and reference the owning automated gate where possible.

### D-001 — Four calculation components

Case #042 uses:

```text
Capital Available = V1 + V2 - V3 + V4
```

V4 is a stable adjustment with zero delta. Do not simplify the production/golden model back to a three-component formula merely because V4 is zero.

### D-002 — DQ impact is not additive

The Case #042 DQ estimate `-€0.3M` overlaps records already represented in V2 snapshot evidence. It answers whether the DQ issue could plausibly explain the anomaly; it is **not** a fifth contribution and must never be added to `-€6.8M` or `-€5.9M` reconciliation totals.

### D-003 — Guided game first, free-form chat second

The challenge path is button/state-driven and must not depend on a perfect free-form prompt. `Ask Dr. Genie` is secondary/collapsible. The guided Experiment path is the release blocker.

### D-004 — Standard Genie Conversation API is the guaranteed path

The stateful Conversation API is the required challenge integration. Agent-mode-specific preview/Beta API behavior is feature-flagged/stretch only and cannot be a release dependency unless current platform verification explicitly upgrades it and all gates pass.

### D-005 — Controlled Experiment and Instrument catalogs

Genie chooses analytical steps/presentation only from closed, versioned allowlists. No generated arbitrary React/UI/code execution.

### D-006 — Hidden truth inaccessible to Genie

`CASE_TRUTH` is absent from Genie data sources, prompts, curated views, browser payloads, and production frontend assets. Backend-only access is narrow and exists solely for scoring/evaluation/release validation.

### D-007 — No manual functional testing during development

Functional correctness is automated through the iteration gates. Per-iteration human work is limited to required artwork/audio subjective approval and post-automation deployment/log/visual inspection. The first required complete functional human playthrough is MDL-7 after R1–R7/live soak are green. A manually found bug receives regression automation.

### D-008 — Case/Experiment terminology is permanent

```text
whole story = Case
live session = Investigation
individual analytical test = Experiment
rendering component = Instrument
```

Legacy code IDs such as `EXP-*` may exist internally only where intentionally migrated, but public language/control models use the canonical hierarchy.

### D-009 — Multi-Case architecture, narrow challenge release

Case identity is data-driven. Case #042 is the challenge blocker. Secondary Cases remain locked until their complete analytical/Genie/E2E/release contracts pass. Do not hardcode `CASE_0042` into generic control paths.

### D-010 — Progression is cosmetic, not authorization

Case unlock state improves game progression but cannot protect hidden/private data. Backend independently validates Case availability, session identity, evidence access, and truth permissions.

### D-011 — Every Case needs an automated analytical contract

A Case is not “implemented” until it has all of:

1. deterministic seed/template;
2. visible observation;
3. hidden `CASE_TRUTH`;
4. expected hypothesis families;
5. allowed/expected Experiment path constraints;
6. reconciliation invariants;
7. golden SQL oracle;
8. fake-Genie fixture;
9. E2E completion path;
10. live Genie benchmark coverage;
11. visual/accessibility coverage for any new Instrument;
12. case-specific release report entry.

This rule is also the reason secondary Cases remain `CONDITIONAL_NOT_SHIPPED` rather than “mostly implemented”.

### Decision-integrity tests — iteration-specific

Add the following static/domain checks. If a check cannot execute because its owning implementation is intentionally deferred to a later iteration, seed it in traceability as `PENDING_MDL_N`; do not silently omit it:

- `MDL1-DEC-001` — Case #042 formula registry contains V1/V2/V3/V4 and correct signs;
- `MDL1-DEC-002` — DQ overlap cannot be inserted as additive reconciliation contribution;
- `MDL1-DEC-003` — guided route exists independently of free-form chat UI;
- `MDL1-DEC-004` — production default path is standard Conversation API; Agent mode is disabled/non-blocking by default;
- `MDL1-DEC-005` — Experiment/Instrument registries reject unknown IDs;
- `MDL1-DEC-006` — truth boundary static dependency/data-source checks exist;
- `MDL1-DEC-007` — release workflow does not require a manual functional gate before MDL-7, except subjective art/deploy inspection;
- `MDL1-DEC-008` — terminology lint rejects public “Experiment #042” style whole-Case copy;
- `MDL1-DEC-009` — generic Case control paths pass the multi-Case hardcode guard;
- `MDL1-DEC-010` — forged local progression cannot authorize an unreleased Case/evidence request;
- `MDL1-DEC-011` — enabling a secondary Case fails release validation if any of its 12 analytical-contract artifacts/gates are missing.


## Locked product, audience, learning, world, and character contract

MDL-1 owns the foundational product decisions in V3 §§1 and 4–10. These must exist as version-controlled product/config/copy rules, not merely as assumptions in artwork prompts.

### Brand and public copy

Lock the following strings in one reusable public-copy/config source (or an equivalent localization-ready content module) so components do not invent variants:

```text
Primary brand:
MAD DATA LAB

Tagline:
Solve anomalies. Test hypotheses. Follow the evidence.

Secondary explanatory line:
Where suspicious numbers become experiments.

Approved technical/submission line:
Turn unexpected numbers into explainable experiments.

Game-facing subtitle:
Dr. Genie’s Experimental Data Laboratory
```

Rules:

- the game wordmark/submission hero uses uppercase `MAD DATA LAB`;
- ordinary prose may use sentence case only when typography requires it;
- the subtitle never replaces the short brand;
- do not revive old product names or call the complete Case an Experiment;
- important brand/copy text is HTML/text, not generated into artwork.

Canonical public product statement:

> MAD DATA LAB is a guided, replayable analytics investigation game built as a collection of Cases. Each Case begins with an unexpected business metric or suspicious data behavior. Dr. Genie, an eccentric but rigorous AI data scientist, forms competing hypotheses, chooses the next analytical Experiment, queries trusted evidence, selects the most useful analytical instrument, updates hypothesis status, and reaches an evidence-based conclusion.

The one-sentence challenge pitch may be shortened in UI/submission copy, but must retain the core meaning: **the player predicts and inspects; Genie chooses experiments and investigates trusted evidence.**

### Target audience

Preserve the V3 audience assumptions in product docs and UX decisions.

Primary:

- data analysts;
- analytics engineers;
- data scientists;
- business users who consume metrics but do not understand how analytical evidence is assembled;
- Databricks practitioners evaluating Genie.

Secondary:

- managers learning to question anomalous KPIs;
- students learning evidence-based analytics;
- data governance/quality practitioners;
- technical reviewers evaluating Genie beyond chat.

Assume ordinary numerical/chart literacy. Do **not** require SQL, Databricks lineage expertise, or data-quality expertise to finish Case #042.

### Twelve learning objectives

The architecture/content model must be capable of teaching all V3 objectives, even though Case #042 is the only mandatory shipped Case. Record these objective IDs/descriptions in a data/config file so Case templates can reference them instead of duplicating prose:

1. observed versus expected creates the analytical target;
2. multiple plausible explanations can coexist;
3. a hypothesis is not a conclusion;
4. the best next analysis reduces uncertainty;
5. decomposition identifies where deviation is concentrated;
6. snapshot comparison identifies what changed;
7. record-level evidence reconciles aggregate differences;
8. a data-quality warning is not automatically causal;
9. lineage explains provenance, with value lineage more specific than technical lineage;
10. evidence strength is expressed explicitly;
11. insufficient evidence is a valid scientific result;
12. good analytics is iterative, not one prompt-and-answer interaction.

Case #042 public metadata may reference only the objectives it actually demonstrates; do not falsely award every objective on completion.

### Product/game design pillars

Architecture and UX decisions must be reviewable against these V3 pillars:

1. **Genie is the scientist, not a decorative narrator.** Major analytical transitions ultimately depend on Genie in the live production path.
2. **Evidence before causality.** No root-cause claim without material reconciliation.
3. **The player predicts; Genie investigates.** Player choices create learning/tension but do not replace analytical evidence.
4. **Reusable Case system.** Cases are data-driven instances of one engine, not bespoke page flows.
5. **Humor decorates rigor.** Funny lines never replace precise analytical meaning.
6. **Controlled adaptivity.** Genie chooses only from approved Experiment/Instrument registries.
7. **Reproducibility.** Same template/generator/seed gives the same deterministic Case evidence.
8. **Graceful uncertainty.** `Insufficient evidence` is valid.
9. **Demo-safe first.** Unreliable optional features are gated/fallback-tested or removed from the release path.

Add these as design-review criteria in the iteration report template/PR checklist so a future “simplification” that violates them is visible.

### Non-goals

Codex must not expand scope during these eight iterations into:

- general-purpose BI;
- a broad financial application;
- production causal-inference software;
- multiplayer;
- a full detective/adventure engine;
- enterprise DQ suite;
- arbitrary LLM-generated visualization/code execution;
- a replacement for Unity Catalog;
- an unrestricted LLM reasoning benchmark;
- a multi-domain analytics assistant.

A feature is not accepted merely because it is impressive. It must strengthen the Case investigation, challenge scoring, reliability, or submission quality.

### World and narrative contract

The setting is a **retro-futurist analytical laboratory**, where Cases are anomaly dossiers/specimen chambers and instruments inspect data rather than chemicals. The tone is:

```text
curious
precise
intelligent
slightly theatrical
playful
never childish
never reckless with causal language
```

Avoid slapstick, obstructive explosions, “evil scientist” clichés, mockery of wrong answers, or copy that treats fictional financial loss like a joke.

Canonical narrative arc for the demo Case:

```text
Something is wrong
-> several explanations are plausible
-> isolate dominant component
-> identify source changes
-> test tempting DQ signal and show insufficient materiality
-> trace/reconcile source evidence and lineage
-> state a calibrated conclusion
```

### Dr. Genie character bible

Lock the character identity independently of any single image asset.

Name: **Dr. Genie**  
Optional promotional subtitle: **PhD in Suspicious Numbers** — do not display everywhere.

Personality:

- relentlessly curious;
- analytically disciplined;
- excited by anomalies;
- skeptical of easy explanations;
- willing to update conclusions;
- delighted by reconciliation;
- mildly eccentric;
- respectful toward the player.

Visual identity:

```text
adult senior data scientist
silver/white unruly hair
modern data-lab coat, not traditional fantasy/medical costume
subtle smart goggles or transparent analytic visor
small holographic data elements
confident expressive posture
no fantasy genie/lamp/smoke tail/turban/magical costume
no caricature of mental illness
no visual derivation from a known fictional scientist
```

Dialogue guardrails are implemented in MDL-4, but MDL-1 must establish the character/content schema now so Dr. Genie copy and asset metadata reference one canonical character ID/version.

### Product-foundation tests — iteration-specific

Add checks in addition to the canonical V3 ledger:

- `MDL1-PROD-001` — brand/tagline/subtitle canonical strings are centralized and old product names are absent from production UI;
- `MDL1-PROD-002` — learning-objective registry contains all 12 unique objective IDs;
- `MDL1-PROD-003` — Case metadata references only known learning-objective IDs;
- `MDL1-PROD-004` — character metadata contains the locked Dr. Genie visual/personality version;
- `MDL1-PROD-005` — production assets/copy contain no fantasy-lamp/genie emoji as the Dr. Genie identity;
- `MDL1-PROD-006` — no public copy calls a complete Case an Experiment;
- `MDL1-PROD-007` — Case #042 hook/briefing identifies the scenario as fictional/synthetic in appropriate explanatory/help/submission context without spoiling the game opening;
- `MDL1-PROD-008` — PR/product checklist contains all nine design pillars and cannot mark product-foundation closure with an unresolved pillar violation.


## Current repository problems that this iteration must remove

The current ZIP has several baseline problems that must not survive MDL-1:

- `package.json` uses `latest` for React, React DOM, Vite, and the React Vite plugin.
- The frontend is plain JSX/JS instead of the specified React + TypeScript architecture.
- The backend is concentrated in a small `server/` package instead of domain/API/Genie/data modules.
- The production build can depend on an already-checked-in `dist/` rather than proving a clean build.
- The current launcher only reads `UVICORN_PORT`; application configuration is not centralized.
- `.idea/` and Python cache artifacts are present in the reviewed ZIP.
- There is no complete GitHub Actions CI/CD workflow.
- There is no release report structure.
- Current Case #042 experiments use prototype hypotheses and statuses.
- The Case #042 catalog hardcodes three prototype experiments.
- The frontend and backend currently duplicate product state.
- The current release check certifies the three-experiment scaffold rather than the V3 domain model.


<!-- HARDENING-2026-08-23-CODEX-CONTRACT -->
## Codex execution contract - non-negotiable

This file is an **implementation contract**, not a suggestion list. Codex must preserve the source-of-truth hierarchy and may not redefine acceptance criteria simply to make a failing build pass.

### No-waiver rule

Codex must **not** do any of the following unless a human explicitly changes this specification:

- skip, `xfail`, quarantine, delete, weaken, or narrow a required test because production code fails it;
- add `continue-on-error`, `|| true`, shell error suppression, or equivalent behavior to a required CI/deployment gate;
- use `--no-verify`, bypass branch protection, dismiss a required review, or merge with missing/red required checks;
- lower numeric accuracy, visual-diff, accessibility, security, live-Genie, soak, or performance thresholds merely to obtain green status;
- change golden Case #042 values, expected statuses, reconciliation rules, scoring rules, or hidden-truth boundaries to match buggy implementation output;
- make fixture/offline data reachable in production in order to hide a live integration failure;
- replace a required real Databricks/Genie integration check with a mock and call the integration requirement complete;
- update visual-regression baselines automatically after a failure without inspecting and documenting why the visual change is intentional;
- self-approve artwork, screenshots, release acceptance, or any other explicitly human gate;
- force-push a shared iteration branch, delete a remote branch, or rewrite history without explicit human approval;
- run destructive Git cleanup (`git reset --hard`, `git clean -fdx`, destructive checkout of user work) when uncommitted/unknown work exists.

When a required gate cannot run because of an external platform limitation or quota, record the blocker precisely. A blocked mandatory gate is **BLOCKED**, not PASS. Only a source-of-truth rule that explicitly marks a gate conditional may make it non-blocking.

### Failure-first implementation rule

For every defect discovered during this iteration:

1. identify the violated requirement;
2. add or strengthen an automated regression test at the lowest practical layer;
3. reproduce the failure;
4. fix production code/configuration/data;
5. prove the new test passes;
6. rerun every affected broader gate;
7. record the regression test ID or path in the iteration report.

Do not fix tests to accept incorrect production behavior unless the test itself contradicts the locked specification. If a real specification ambiguity exists, record it under `docs/decisions/` and require a human decision before changing locked behavior.

### Exact-commit and exact-tree rule

All local, GitHub, deployment, and approval evidence must identify what source it applies to.

Record at least:

```text
base_main_sha
iteration_branch_head_sha
iteration_branch_tree_sha
pull_request_number
pull_request_url
required_ci_run_ids
deployment_run_id
deployed_app_version_or_git_sha
deployed_tree_or_content_digest_when_available
```

A CI run on an older SHA does not certify a newer SHA. After the last code/config/data/art change, required CI must rerun on the new branch head.

A committed Markdown report cannot safely contain the SHA of the commit that contains that same report without creating a self-reference loop. Therefore use these semantics:

- `implementation_sha`: last substantive implementation commit before closeout-report-only edits;
- `report_commit_sha`: capture in the PR description/comment, CI artifact, GitHub release metadata, or the next iteration's predecessor record;
- `merge_sha`: capture after merge in CI/release metadata or the next iteration's predecessor record;
- when squash/rebase changes commit IDs, compare **Git tree hashes** (`git rev-parse <sha>^{tree}`) to prove the accepted content is unchanged.

Never create an endless "update the report with its own new SHA" commit loop.


### Closure ordering and non-self-referential evidence

Use two identities so reports can contain observed CI/deployment evidence without creating an infinite “commit report -> new SHA -> redeploy -> new report” loop.

**`implementation_sha`** is the final commit whose tree contains everything that can affect runtime, build, deployment behavior, data/Genie behavior, production assets, and the already-human-approved approval records required for this iteration.

**`report_commit_sha`** is optional and may occur later only to finalize non-runtime closure documentation such as the iteration report. It does not become a new `implementation_sha` unless its diff changes runtime-affecting content.

Required order:

1. complete code/data/config/test/art changes;
2. obtain the required human art approval for the exact production bytes;
3. commit the approval record;
4. run the full required GitHub CI against that head;
5. designate that green head as `implementation_sha` and record its Git tree/runtime-content digest;
6. deploy that exact implementation identity;
7. run automated deployed smoke and required manual deployment inspection;
8. store observed CI/deployment evidence first in immutable GitHub workflow artifacts/summaries/PR comments;
9. if the repository requires a finalized committed iteration report, make one **report-only** commit and run the docs/change-classification/release-contract checks again;
10. merge only if a machine check proves the report-only diff did not change runtime-affecting content and all latest required merge checks are green.

Create/maintain `scripts/classify_change.py` (or equivalent) that classifies a diff against `implementation_sha`. It must fail closed: an unknown path is runtime-affecting until explicitly classified. Runtime-affecting categories include at least application/backend/frontend code, Cases/data/SQL, Genie config/prompts, production asset bytes/manifests, dependency manifests/locks, app/bundle config, CI/deployment workflow logic, build/runtime scripts, and security/configuration files. `docs/iterations/*` and generated sanitized release summaries may qualify as report-only only when they are not consumed by build/runtime/Genie configuration.

Create `scripts/compute_runtime_digest.py` from the same fail-closed path classification. It computes a deterministic SHA-256 over sorted runtime-affecting paths plus their bytes (and the path names themselves). Record `implementation_runtime_digest` beside `implementation_sha`. A report-only commit is valid only when its runtime digest is exactly unchanged. After merge, compute the runtime digest on `main`; it must still equal the accepted implementation digest unless a new runtime-affecting commit has intentionally invalidated the iteration and rerun the gates.

This digest is repository-side content provenance; it does not replace Databricks `resolved_commit` for Git-source deployment. It solves the merge/report-commit identity problem without pretending commit IDs must remain identical after squash/rebase/report-only closeout.

If the post-deployment commit changes a runtime-affecting path, the report-only exception is void: set a new `implementation_sha`, rerun every invalidated gate, redeploy, and collect new evidence.

The deployed app is therefore required to match the accepted **implementation identity/runtime digest**, not a later documentation-only report commit. The PR/merge evidence must record both identities when they differ.

### Branch safety and predecessor verification

Before creating or continuing `MDL-1`:

```bash
git fetch origin --prune
git checkout main
git pull --ff-only origin main
git status --porcelain
git rev-parse HEAD
git rev-parse HEAD^{tree}
```

`git status --porcelain` must be empty. Record the main SHA/tree as the base.

If the iteration branch already exists, inspect it rather than replacing it:

```bash
git branch -vv
git log --oneline --decorate --graph --max-count=30 --all
git merge-base origin/main MDL-1
```

Confirm it is the intended active iteration branch and contains no unrelated/stale work. Do not silently recreate it from a different base.

After creating/continuing the branch, verify `origin/main` is an ancestor unless an intentional, documented rebase/merge is in progress:

```bash
git merge-base --is-ancestor origin/main HEAD
```

### Commit quality

Every commit must:

- be focused and reviewable;
- leave the repository buildable unless explicitly labeled as an intermediate WIP commit that will not be pushed for review;
- pass `git diff --check`;
- avoid generated caches, credentials, personal IDE state, local databases, and unapproved large binaries;
- include tests with behavioral changes whenever practical.

Before push, inspect:

```bash
git status --short
git diff --stat origin/main...HEAD
git diff --check origin/main...HEAD
```

### GitHub CI proof

When GitHub CLI is available, do not stop at "a workflow exists". Prove required checks ran against the exact PR head:

```bash
gh pr view --json number,url,headRefOid,baseRefName,mergeStateStatus,statusCheckRollup
gh pr checks --watch
gh run list --commit "$(git rev-parse HEAD)" --limit 50
```

For any failure:

```bash
gh run view <run-id> --log-failed
```

The iteration cannot close when a required job is absent, unexpectedly skipped, cancelled, timed out, neutral when it should be required, or green only because its test command selected zero tests.

### CI workflow anti-bypass requirements

Every required GitHub Actions job must use explicit failure semantics. Prefer:

- minimal `permissions:` at workflow/job level;
- `contents: read` for ordinary CI;
- `id-token: write` only for the Databricks OIDC deployment job that needs it;
- job-level `timeout-minutes` so a hung dependency install/test/deploy eventually fails;
- `concurrency` to prevent stale overlapping deployments to the same environment;
- `set -euo pipefail` in multi-line shell steps;
- lockfile/frozen installs (`npm ci`, `uv sync --frozen`, or the repository's equivalent);
- reviewed, versioned GitHub Actions; third-party actions must be pinned to immutable commit SHAs. A temporary exception is allowed only when no immutable reference exists and must be recorded as a blocking security debt with owner/expiry; moving tags alone are not accepted as release evidence;
- explicit test-report generation so "0 tests collected" can be detected;
- sanitized CI artifacts with a finite retention period.

A deployment workflow must not use `continue-on-error` for bundle validation, bundle deployment, app restart, RUNNING-state polling, or post-deploy smoke.


### Deterministic test rerun, skip, and flake policy

A green rerun does not erase a failed deterministic gate. Codex must distinguish a fixed failure from a flaky/externally transient test.

Rules:

1. Unit, parser, state-machine, golden-data, contract, deterministic fixture E2E, visual baseline, accessibility, security, and static checks must **not** be automatically retried until green.
2. If one of those tests fails, preserve the failing test/log reference, diagnose the cause, add/adjust regression coverage when appropriate, change implementation/test only for a justified reason, and rerun the affected gate plus its invalidated dependents.
3. `skip`, `xfail`, `.only`, focus filters, test-name exclusions, reduced test discovery, and conditional CI expressions are treated as behavior changes. CI must inventory them.
4. A new skip/xfail is allowed only when the V3 specification explicitly makes the capability conditional/unshipped or when a documented external platform limitation makes execution impossible. Record test ID, reason, owner, expiry/revisit iteration, and evidence. Do not skip to hide a product defect.
5. Canonical secondary-Case tests use the traceability status `CONDITIONAL_NOT_SHIPPED` / `NOT_RUN_CONDITIONAL` only while the server-owned Case release state remains disabled. Enabling the Case makes the corresponding tests blocking automatically.
6. Live Genie/Databricks network tests may use only the bounded retries/repair policy explicitly defined for that tier. Report attempts, not merely the final successful attempt.
7. If a deterministic test proves genuinely flaky, treat flakiness as a defect: make timing/data deterministic or fix synchronization. Do not normalize permanent retry wrappers as the solution.
8. CI must fail when a test command unexpectedly discovers/runs zero tests or when the collected canonical test-ID inventory drops without an intentional traceability update.

The iteration report must include any failed-then-fixed gate and any permitted skip/conditional entry; “green” alone is not sufficient audit evidence.

### Human artwork approval semantics

Every iteration has an artwork checkpoint. The approval applies to **exact asset bytes**, not merely a filename or visual concept.

For every candidate/final asset record:

```text
asset_id
source_prompt_or_prompt_file
reference_asset_ids_if_any
generator/tool/model/version if available
generation date
rights_or_license_basis for challenge/public use
source file path
production derivative path
pixel dimensions
format
size_bytes
sha256
crop/alpha requirements
preflight result
human decision
human notes
```

Rules:

1. Codex may prepare prompts, manifests, preflight scripts, and integrate temporary placeholders.
2. If Codex has no image-generation capability, it must stop at the art gate with status `BLOCKED_HUMAN_ART_GENERATION` and provide the exact prompt/specification needed. It must not claim the iteration complete.
3. Codex must never set `APPROVED` based on its own judgment.
4. A human must explicitly approve the final production derivative(s).
5. If approved asset bytes change later, the SHA-256 changes and approval automatically becomes invalid; rerun preflight and obtain approval again.
6. Approval files must identify every approved SHA-256 individually.
7. Rejected candidates may remain outside the deployment bundle for provenance, but must not be referenced by production code.
8. Prompts must not request imitation of a living artist or a copyrighted character/style identity; record the tool/model and the basis on which the project is permitted to use the final asset publicly.
9. Temporary placeholders must be visibly/documentably non-final and must not survive the iteration Definition of Done unless the specification explicitly allows them.

### Evidence retention and sanitization

Each iteration report must link to or identify the evidence used to close it. Preserve enough information to reproduce the decision without publishing secrets.

Never put in reports/CI artifacts:

- PATs, OAuth secrets, cookies, authorization headers;
- private service-principal credentials;
- raw hidden `CASE_TRUTH` payloads beyond the minimal synthetic golden values specifically needed by private test reports;
- personal workspace/user identifiers when unnecessary;
- unrestricted raw model prompts/responses containing sensitive runtime metadata.

Prefer stable summaries, IDs, hashes, timings, pass/fail results, and redacted diagnostic references.

### Stop-the-line conditions

Immediately stop iteration closure and keep the branch open if any of these occurs:

- locked spec and implementation disagree materially;
- Case #042 reconciliation is non-zero outside documented tolerance;
- `CASE_TRUTH` appears in a Genie-facing surface or production browser payload;
- production can silently enter fixture/offline mode;
- Genie is no longer causally central to the main investigation;
- a required CI job is missing/red/skipped/cancelled;
- deployed source/version cannot be tied to the accepted Git content;
- artwork is unapproved or approval hash is stale;
- a critical/high security issue has no explicit reviewed disposition;
- a manual inspection reveals a functional defect without an accompanying regression test and fix.

Do not advance to the next iteration until every non-conditional stop condition is cleared.

### Standard blocker codes

When Codex cannot close a required external/human gate, use a precise blocker instead of inventing a substitute PASS:

```text
BLOCKED_SOURCE_DRIFT                 accepted V3 source/addendum chain changed or is unavailable
BLOCKED_PREDECESSOR_MDL_0            predecessor closure/approval/deploy evidence is not valid (not applicable for MDL-1)
BLOCKED_GITHUB_AUTH                  repository/PR/check evidence cannot be accessed or pushed
BLOCKED_GITHUB_ADMIN_CONFIGURATION   required branch-protection/environment rule needs a human/admin change
BLOCKED_DATABRICKS_AUTH              required Databricks workspace/resource access is unavailable
BLOCKED_DATABRICKS_CONFIGURATION     required App/Genie/warehouse/resource binding is absent or wrong
BLOCKED_EXTERNAL_QUOTA               Free Edition/platform quota prevents a mandatory live gate
BLOCKED_HUMAN_ART_GENERATION         required artwork cannot be generated in the available execution environment
BLOCKED_HUMAN_ART_APPROVAL           final candidate bytes await explicit human approval
BLOCKED_HUMAN_ACCEPTANCE             iteration-specific manual acceptance/inspection has not been performed or failed
BLOCKED_RIGHTS_PROVENANCE            required production media lacks an acceptable usage-rights basis
```

A blocker may coexist with completed engineering work, but the iteration status remains `BLOCKED`/`IN_PROGRESS`, never `COMPLETE`. Record the blocker, evidence, exact next human/external action, and which gates become stale if it is later resolved.


## Branch and Git workflow - mandatory

### Create the iteration report skeleton immediately

As soon as `MDL-1` exists, create `docs/iterations/MDL-1-report.md` with an explicit non-final status such as:

```yaml
iteration: MDL-1
status: IN_PROGRESS
base_main_sha: <observed>
implementation_sha: null
open_blockers: []
```

Add headings/placeholders for the required local tests, CI runs, deployment, artwork approval, manual inspection, decisions, regressions, and remaining blockers. **Do not fill unknown evidence with fake IDs or PASS.** Use `NOT_RUN`, `PENDING`, `BLOCKED`, or `UNKNOWN` until observed.

The early skeleton serves three purposes:

1. `gh pr create --body-file docs/iterations/MDL-1-report.md` always has a real file;
2. reviewers can see progress/blockers before closure;
3. finalization is an update to an existing audit record, not a late invented success narrative.

The report becomes `status: COMPLETE` only after all iteration gates are satisfied and the release-contract validator accepts it.


### 1. Start from a clean, updated main branch

Run:

```bash
git fetch origin --prune
git checkout main
git pull --ff-only origin main
```

Then verify:

```bash
git status --porcelain
```

The result must be empty. If it is not empty, stop and resolve local changes before continuing.

### 2. Create the iteration branch

```bash
git checkout -b MDL-1
```

If `MDL-1` already exists locally or remotely, do not delete or overwrite it automatically. Inspect the existing branch and continue only if it is clearly the active iteration branch.

### 3. Commit discipline

Use small, reviewable commits. Recommended sequence:

```text
MDL-1: add repository architecture and locked dependencies
MDL-1: add canonical domain model and state machine
MDL-1: add GitHub CI and Databricks deploy workflow
MDL-1: add asset manifest and approved visual baseline
MDL-1: add iteration completion report
```

Before every commit:

```bash
git diff --check
```

No whitespace errors are allowed.

### 4. Push the branch

```bash
git push -u origin MDL-1
```

### 5. Open or update a pull request

If GitHub CLI is available:

```bash
gh pr create --base main --head MDL-1 --title "MDL-1 Foundation and canonical domain" --body-file docs/iterations/MDL-1-report.md
```

If a PR already exists, update it rather than opening a duplicate.

### 6. Verify GitHub CI, not only local tests

Required commands when GitHub CLI is available:

```bash
gh run list --branch MDL-1 --limit 20
gh pr checks --watch
```

The iteration is not complete if:

- no CI workflow is triggered;
- any required workflow is skipped unexpectedly;
- any required job is cancelled;
- any required job is red;
- CI uses different lockfiles or commands than local development;
- CI passes only because tests are silently excluded.

After merge, verify the `main` workflow is also green.

### Final branch-freshness gate before declaring `implementation_sha`

The branch was created from clean `main`, but that does not prove it is still current when the implementation is ready. Immediately before declaring the final runtime-affecting commit as `implementation_sha`:

```bash
git fetch origin --prune
git merge-base --is-ancestor origin/main HEAD
git status --porcelain
```

Requirements:

- the current `origin/main` must be an ancestor of the candidate `implementation_sha`;
- if `main` advanced, update `MDL-1` using the repository's normal non-destructive policy (rebase or merge, whichever the project has explicitly chosen), resolve conflicts, and rerun **all invalidated local and GitHub required checks**;
- do not force-push merely to make provenance simpler unless force-push is already an explicitly permitted project policy and no reviewed history would be lost;
- art approval remains valid only if the approved production bytes/hashes are unchanged by the branch update; otherwise the art gate is invalidated and must run again;
- deployment evidence collected before a branch refresh is stale and cannot be used for closure.

Add `MDL1-GIT-001` through `MDL1-GIT-004`: current-main ancestry, clean accepted head, refresh invalidates stale checks, and approved-art hashes survive or deliberately invalidate on refresh.


### Mandatory commit proof

Codex must actually commit the completed work; a clean local working tree with only uncommitted changes is not a deliverable. Before requesting merge/closure, prove:

```bash
test -z "$(git status --porcelain)"
git log --oneline origin/main..HEAD
git diff --check origin/main...HEAD
git rev-parse HEAD
git rev-parse HEAD^{tree}
```

Requirements:

- at least one non-empty `MDL-1: ...` implementation commit exists on the iteration branch;
- behavioral changes and their tests should normally be committed together or in a clearly ordered reviewable sequence;
- generated caches, local reports containing secrets, personal IDE state, and unapproved binary candidates are not committed;
- after the final approved asset/report changes, commit again as needed and push the **new** head; CI evidence from an earlier head is stale;
- `git status --porcelain` is empty at the point the accepted head is declared.

### Post-merge `main` failure recovery

The iteration is not closed until the required post-merge `main` workflow is green. If the already-merged `MDL-1` content exposes a main-only integration/deployment failure:

1. mark MDL-1 closure `REOPENED_POST_MERGE`;
2. do **not** advance to MDL-2;
3. preserve the failed main workflow/deployment evidence;
4. if the original iteration branch cannot be safely reused because it has already been merged, create a narrowly scoped recovery branch named `MDL-1-recovery-<k>` from the failed current `main`; this does not replace the required original `MDL-1` branch;
5. add a regression test/release check reproducing the main-only failure where possible;
6. fix, commit, push, PR, and run the full invalidated required checks for the recovery head;
7. merge only when the recovery PR is green;
8. require the subsequent `main` workflow/deployment smoke to be green and update the iteration/predecessor evidence chain.

Never delete/rewrite the merged history or claim the earlier PR was sufficient because its branch checks were green.

## Technical architecture and responsibility boundaries

MDL-1 is the primary closure owner for V3 §24. The repository/component split below is only valid if responsibility boundaries are also enforced.

### Architecture goals

Optimize in this order:

1. demo reliability;
2. Genie centrality;
3. deterministic data/testability;
4. low operational complexity;
5. graceful degradation;
6. strong automated coverage;
7. Databricks Free Edition compatibility.

Do not add a queue, separate player-profile database, heavy local data-processing framework, arbitrary LLM orchestration framework, or large design system unless a demonstrated blocker cannot be solved by the approved stack.

### Approved stack boundary

**Frontend**

```text
React 18+
TypeScript
Vite
native CSS variables/modules or lightweight equivalent
Recharts only where useful; custom SVG for deterministic lineage/reconciliation
lightweight open-source line icons
Vitest + Testing Library
Playwright
```

**Backend**

```text
Python 3.11
FastAPI
Pydantic v2
Databricks SDK for Python
Databricks SQL Connector for deterministic trusted SQL/fallback path
httpx only where needed for isolated API adaptation
pytest + Hypothesis
Ruff + mypy/Pyright
```

**Data/AI**

```text
Unity Catalog synthetic public/private/curated structures
Databricks SQL Serverless Warehouse where required
Genie Agent resource via standard stateful Conversation API
Agent-mode Beta path feature-flagged only
```

### High-level architecture

```text
Browser
  |
  | HTTPS through Databricks Apps proxy
  v
FastAPI application
  |
  +-- Case catalog / progression service
  +-- Investigation session/state service
  +-- Genie orchestration service
  +-- protocol/evidence validators
  +-- Case template + completion-contract registry
  +-- Experiment / Instrument registries
  +-- trusted SQL/evidence repositories
  +-- scoring / private verdict validator
  +-- structured telemetry
       |
       +----> Genie Agent resource
       |        |
       |        v
       |      Genie Conversation API
       |        |
       |        v
       |      curated Unity Catalog views
       |
       +----> Databricks SQL Warehouse
                |
                +-- curated/public evidence
                +-- deterministic fallback query templates
                +-- private CASE_TRUTH through narrow backend-only repository
```

The browser never talks directly to the warehouse/private tables and never receives credentials.

### Primary analytical responsibility flow

By the time MDL-3/4 are complete, the intended flow is:

1. player selects a Case;
2. backend creates an Investigation bound immutably to that Case;
3. backend starts a fresh Genie conversation;
4. server derives currently allowed next Experiments from the Case contract/current evidence;
5. Genie selects the next valid Experiment and queries curated evidence;
6. backend validates protocol/query result/evidence schema;
7. server appends authoritative evidence/hypothesis events;
8. frontend renders one registered Instrument from a validated render model;
9. cycle repeats until completion prerequisites;
10. Genie synthesizes conclusion from visible evidence;
11. backend independently validates reconciliation/eligibility/private oracle constraints;
12. score/progression/debrief are server-authoritative.

MDL-1 need not implement every step yet, but no architectural choice in this iteration may make that flow impossible.

### Safe fallback boundary

The architecture reserves a trusted SQL fallback repository for a **selected valid Experiment whose Genie query result fails**. It is not an alternate scripted scientist. Experiment selection before fallback remains Genie-controlled in production. Offline/fake mode is test/catastrophic-outage only and visibly distinct.

### Server-authoritative boundary

The backend owns:

```text
Case availability
session Case identity
phase/state transition legality
hypotheses/statuses
Experiment history/evidence
score/hints
completion eligibility
verdict validation
progression acceptance
```

The browser owns presentation-only state such as open panel, selected row/filter, animation completion, audio, and reduced-motion preference.

No frontend constant may become a hidden analytical fallback.

### Architecture enforcement tests — iteration-specific

Add:

- `MDL1-ARCH-001` — frontend production imports cannot access backend private truth/data modules;
- `MDL1-ARCH-002` — browser API contract exposes no warehouse/credential secret field;
- `MDL1-ARCH-003` — analytical state transition endpoint is server-authoritative, not accepted from a client-supplied completed Experiment payload;
- `MDL1-ARCH-004` — generic frontend state contains no canonical #042 evidence/verdict fallback constants;
- `MDL1-ARCH-005` — backend Genie/data/private-validator packages have dependency-direction rules preventing Genie -> private truth import;
- `MDL1-ARCH-006` — the selected stack/build runs without a separate background worker/profile database;
- `MDL1-ARCH-007` — production configuration makes fixture/offline services dependency-injectable for tests but unreachable by public client input.


## MDL-1 implementation decisions — locked to remove avoidable Codex choice

Unless a current platform fact makes one impossible and a human approves an ADR, MDL-1 uses these concrete choices:

| Concern | Locked MDL-1 choice | Why |
|---|---|---|
| Frontend | React + TypeScript + Vite | matches V3 and current scaffold migration |
| Frontend package manager | npm + `package-lock.json` | current repo already uses npm; minimizes migration risk |
| Frontend state | React reducer/context + server responses; no Redux/Zustand dependency in MDL-1 | server is authoritative and current state needs are small |
| API client | native `fetch` wrapper + generated OpenAPI TypeScript types | avoids another runtime dependency |
| Backend | FastAPI + Pydantic v2 | V3 contract |
| Settings | `pydantic-settings` in `backend/config.py` | typed/centralized environment parsing |
| Case YAML | PyYAML parse → Pydantic validation → immutable domain models | deterministic validated catalog |
| Python dependency manager | `uv` + `pyproject.toml` + `uv.lock` | current Databricks recommendation/reproducibility |
| Type checker | mypy | one tool, one CI truth |
| Python lint/format gate | Ruff | one fast deterministic gate |
| Unit tests | pytest / Vitest + Testing Library | V3 test architecture |
| Browser tests | Playwright | V3 E2E architecture |
| Production process | one FastAPI/Uvicorn process serving built Vite assets + API | simplest reliable hybrid Databricks App |
| Structured logging | Python stdlib logging with JSON formatter (or an equivalently tiny implementation) | no heavy observability dependency in foundation |
| Generated API types | `openapi-typescript` | prevents frontend/backend contract drift |
| Production visual assets | `assets/production` copied by Vite `publicDir` | one authoritative asset copy; review candidates stay out of build |

Do not introduce a design system, global state library, ORM, queue, extra database, agent orchestration framework, or animation library in MDL-1 without a concrete requirement and reviewed ADR.

## Repository migration tasks

### Create the target structure

By MDL-1 closure, the repository must converge on this foundation (empty future directories may contain `.gitkeep` only when useful; do not create fake implementations merely to populate the tree):

```text
mad-data-lab/
├── app.yaml
├── databricks.yml
├── package.json
├── package-lock.json
├── pyproject.toml
├── uv.lock
├── README.md
├── CONTRIBUTING.md
├── .env.example
├── .gitignore
│
├── .github/
│   ├── pull_request_template.md
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
│
├── frontend/
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── vitest.config.ts
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── api/
│   │   │   ├── client.ts
│   │   │   └── generated/openapi.d.ts
│   │   ├── state/
│   │   ├── pages/
│   │   ├── components/
│   │   └── styles/
│   │       ├── tokens.css
│   │       └── global.css
│   └── tests/
│
├── backend/
│   ├── main.py
│   ├── run.py
│   ├── config.py
│   ├── telemetry.py
│   ├── api/
│   ├── domain/
│   ├── genie/
│   ├── data/
│   ├── tests/
│   └── static/                  # GENERATED by `npm run build`; ignored, never source authority
│
├── cases/
│   ├── catalog.yaml
│   ├── templates/
│   └── completion_contracts/
│
├── data/
│   ├── ddl/
│   ├── views/
│   ├── seeds/
│   ├── fixtures/
│   ├── generation/
│   └── validation/
│
├── genie/
│   ├── instructions.md
│   ├── benchmarks/
│   └── example_sql/
│
├── assets/
│   ├── image_prompts.md
│   ├── art_source_manifest.yaml
│   ├── production/
│   │   ├── images/
│   │   └── audio/
│   ├── source/                  # selected non-deployed master source only when required
│   ├── review/                  # ignored/non-deployed candidate and preview workspace
│   └── legacy/                  # non-deployed migration references only if retention is justified
│
├── schemas/
│   └── iteration-manifest.schema.json
│
├── scripts/
│   ├── run_iteration_gate.py
│   ├── export_openapi.py
│   ├── check_api_contract.py
│   ├── image_preflight.py
│   ├── build_art_generation_requests.py
│   ├── build_art_review.py
│   ├── validate_art_approval.py
│   ├── validate_mdl1_contract.py
│   ├── validate_iteration_manifest.py
│   ├── validate_traceability.py
│   ├── validate_human_approvals.py
│   ├── classify_change.py
│   ├── compute_runtime_digest.py
│   ├── smoke_deployment.py
│   └── verify_deploy_source.sh or verify_deploy_source.py
│
├── tests/
│   ├── contracts/
│   ├── e2e/
│   ├── visual/
│   ├── accessibility/
│   ├── performance/
│   ├── security/
│   └── chaos/
│
├── docs/
│   ├── api/openapi.json
│   ├── specs/MAD_DATA_LAB_V3.md
│   ├── approvals/MDL-1-art.md
│   ├── architecture/
│   ├── challenge/
│   ├── development/
│   ├── engineering/
│   ├── iterations/
│   ├── operations/
│   ├── platform/
│   │   ├── databricks-apps-verified.md
│   │   ├── free-edition-attestation.md
│   │   ├── github-databricks-oidc.md
│   │   └── deployment-source-strategy.md
│   └── traceability/
│       ├── source-baseline.json
│       ├── v3-test-coverage.csv
│       └── v3-section-coverage.csv
│
└── release-report/             # generated/sanitized CI evidence; ignored unless a tiny declared summary is intentionally committed
```

`backend/static/`, `assets/review/`, raw `release-report/` outputs, Node modules and local virtual environments are generated/non-source paths and must be covered by `.gitignore`/package rules. The canonical V3 source under `docs/specs/` is committed and hash-protected; do not edit it during migration.

### Current scaffold migration map — preserve behavior while removing duplicate authority

Use the reviewed scaffold only as a migration source. Before deleting an old file, identify which new module owns each responsibility. The expected mapping is:

| Current scaffold area | MDL-1 destination / action | Closure rule |
|---|---|---|
| `src/main.jsx` | split into `frontend/src/main.tsx`, `App.tsx`, pages/components/state/API modules | old entrypoint removed from production build |
| `src/styles.css` / ad-hoc CSS | split into `frontend/src/styles/tokens.css`, `global.css`, limited component styles | no duplicate global token source |
| `src/evidence-polish.css` or any CSS-generated evidence | remove from production; analytical evidence may not live in CSS | static scan proves no analytical facts injected with pseudo-elements |
| `server/main.py` | `backend/main.py` + `backend/api/*` | API authority exists only in new backend tree |
| `server/run.py` | `backend/run.py` or equivalent one launcher | runtime port/shutdown behavior covered by tests |
| `server/case_data.py` | public Case metadata into `cases/` + typed domain fixtures; analytical truth deferred to MDL-2 | no browser/server duplicate truth constants |
| `server/genie.py` | preserve only as migration reference; create `backend/genie/` interfaces/stubs without claiming live orchestration | live Genie behavior remains owned by MDL-3 |
| `tests/test_case_contract.py` | migrate/adapt into canonical domain/catalog tests; preserve all still-valid numerical regression knowledge for MDL-2 | no loss of useful regression coverage |
| `scripts/release_check.py` | replace/expand with contract validators; do not keep the three-experiment scaffold gate as release authority | new release check fails old 3-experiment assumptions |
| `sql/case_0042_setup.sql` | preserve unchanged as MDL-2 input/reference unless a migration-only path change is required | no semantic data rewrite in MDL-1 |
| Genie serialized config | preserve/version in `genie/` or a clearly marked migration/reference location | MDL-3 owns semantic refactor |
| `public/assets/Mad_Data_Lab.png`, `public/assets/board.png`, fantasy-genie emoji/art | move to `assets/legacy/not-deployed/` or remove from deployable path; keep provenance if useful | production build contains no reference to legacy fake-board/fantasy-genie art |
| checked-in `dist/` | remove from source control unless a documented platform exception is proven | clean build is authoritative |

Required migration invariant: **at no point may both old and new modules be reachable as competing production authorities for Case state, API routing, or analytical content.** Temporary shims must forward one-way to the new module and must have an explicit removal commit before closure.

Add `MDL1-MIG-001` through `MDL1-MIG-006` checks for: no live old entrypoint, no duplicate API app, no production legacy-art reference, no CSS evidence injection, no checked-in stale build authority, and no old hardcoded three-experiment release check.

### Remove repository noise

Delete from version control if currently tracked:

```text
.idea/
__pycache__/
*.pyc
local .env files
unneeded generated caches
```

Update `.gitignore` for:

```text
.env
.env.*
!.env.example
node_modules/
dist/
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
coverage/
playwright-report/
test-results/
.idea/
.DS_Store
backend/static/
assets/review/
```

### Repository versus CI-evidence retention policy

Keep reviewable source-of-truth artifacts in Git and bulky/ephemeral execution evidence in protected CI artifacts. Default ownership:

**Commit to Git:**

```text
docs/iterations/*.md
docs/approvals/*.md
docs/architecture/**
docs/traceability/*.csv|json
cases/**
genie source-controlled config/prompts/benchmarks
asset manifests and approved production derivatives within budget
source code/tests/scripts/workflows/locks
```

**Generate/archive in CI rather than routinely commit:**

```text
raw JUnit/XML/coverage reports
Playwright traces/videos
large screenshot diff bundles
raw deployment logs
live Genie evaluation execution logs
full SBOM build artifacts when regenerated mechanically
release-report/MDL-N execution evidence unless a small sanitized manifest/summary is intentionally versioned
```

Rules:

- a small sanitized iteration manifest/summary may be committed if the repository uses it as predecessor metadata, but raw logs/binary reports must not bloat Git history;
- GitHub artifact retention must be long enough to survive challenge review/final submission preparation; record retention duration in CI config;
- do not upload hidden truth payloads, secrets, internal Genie reasoning, or personal credentials merely because an artifact is private;
- closure reports must reference immutable workflow/run/artifact IDs or hashes so evidence can be located without checking generated output into Git;
- configure `.gitignore` consistently with the chosen generated-evidence policy.

Whether `dist/` remains tracked must be an explicit decision. Preferred behavior is not to track it; Databricks/GitHub build from source. If platform deployment absolutely requires a committed build artifact, document the reason and add a CI test proving the committed artifact matches a clean build.

### Production frontend build/serve contract

Lock one deterministic production path for the hybrid app. Recommended pattern:

1. root/package build invokes the frontend Vite build from source;
2. Vite emits hashed assets plus `index.html` into one known build directory (for example `frontend/dist` or a packaging directory copied into `backend/static`);
3. the production FastAPI process serves that accepted static build and the `/api` routes from the same Databricks App process;
4. the SPA history fallback serves `index.html` only for intended browser routes and **must never intercept `/api/*`**, static asset errors, health, or other server endpoints;
5. Vite dev server/proxy is development-only and is not required in the deployed App;
6. asset URLs work behind the Databricks Apps proxy/base path without hardcoded localhost/origin assumptions;
7. the build injects/ships the generated accepted build identity; a stale checked-in `dist` cannot override the clean build;
8. missing frontend build output causes startup/build failure, not a fallback to an old bundled page.

The production HTML shell must include at least:

```text
<!doctype html>
html lang attribute
charset
viewport meta
meaningful MAD DATA LAB title
root application mount
no inline secret/config blob
```

#### FastAPI static/SPA serving blueprint

Register `/api` routers before any SPA fallback. Serve the Vite static tree without allowing the fallback to swallow API errors. Equivalent behavior:

```text
/api/...                      FastAPI routers / canonical JSON errors
/assets/...                   built static assets
/known-static-file            serve file when it exists
/anything-else-not-api        return backend/static/index.html for client-side navigation
/unknown/api/path             JSON 404/error semantics, never index.html
```

A safe implementation can use an explicit `/assets` `StaticFiles` mount plus a final GET SPA route that refuses paths beginning with `api/`, or another tested ordering that proves the same behavior. The API exception/error middleware must run before SPA handling. `backend.main` must be importable for OpenAPI/tests even when the static build has not been produced; actual production startup may fail closed when required static output is absent.

Add:

- `MDL1-BUILD-001` — deleting any preexisting build output followed by the documented build produces a complete production static tree;
- `MDL1-BUILD-002` — FastAPI production test serves `/`/SPA route and the generated asset references successfully;
- `MDL1-BUILD-003` — unknown `/api/...` is an API 404/error envelope and is never returned as `index.html`;
- `MDL1-BUILD-004` — missing/stale static build cannot silently start as a valid production release;
- `MDL1-BUILD-005` — production assets contain the accepted build identity and no localhost/dev-server dependency;
- `MDL1-BUILD-006` — `index.html` metadata/`lang`/viewport/title are present and no secret runtime environment data is serialized into the HTML.

## Dependency and toolchain tasks

MDL-1 locks one dependency strategy so local, CI, and Databricks builds do not choose different installers. Changing package manager later is a runtime-affecting architectural change and invalidates build/deploy evidence.

### Node — lock on npm + `package-lock.json`

Use Node `22.16.x` compatibility as the current Databricks Apps baseline. Commit: 

```json
{
  "engines": {"node": ">=22.16 <23"}
}
```

Use **npm** for MDL-1. Commit exactly one Node lockfile: `package-lock.json`. Do not also commit `pnpm-lock.yaml`/`yarn.lock`.

Replace every `latest` dependency. Pin exact tested versions in `package.json` for this challenge week unless a deliberate bounded range is documented; the lockfile remains the install authority.

Production-build dependencies must be under `dependencies` because Databricks Apps can skip `devDependencies` when the deployment environment uses `NODE_ENV=production`. At minimum, packages required to run the Vite production build belong in `dependencies`:

```text
react
react-dom
vite
typescript
@vitejs/plugin-react
@types/react
@types/react-dom
```

Test/development-only packages may live in `devDependencies`, including the selected versions of:

```text
vitest
@testing-library/react
@testing-library/jest-dom
jsdom
eslint
openapi-typescript
Playwright packages
axe integration when its owning tests are introduced
```

Required scripts at repository root:

```text
npm run dev              frontend development only
npm run typecheck        tsc --noEmit or equivalent
npm run lint             frontend lint with non-zero failure
npm run test             deterministic frontend unit/component tests, run once in CI
npm run api:generate     regenerate TypeScript API types from FastAPI OpenAPI
npm run api:check        fail if generated API types/OpenAPI snapshot drift
npm run build            production frontend build consumed by FastAPI
npm run test:e2e         fixture E2E entry point; may initially execute MDL-1 smoke subset
```

CI uses `npm ci`, never `npm install`, to verify the lock. A test must fail when `package.json` and `package-lock.json` drift.

### Python — lock on `uv` + `pyproject.toml` + `uv.lock`

Use Python `>=3.11,<3.12` for the challenge build unless a later approved platform change requires otherwise. MDL-1 uses Databricks' recommended reproducible `uv` path:

```text
pyproject.toml
uv.lock
NO production requirements.txt
```

A `requirements.txt` in the app root would take precedence over the uv lock in Databricks Apps and is therefore forbidden unless an explicit human-approved architecture decision replaces this strategy. Add a CI check for this.

Production dependencies required in MDL-1:

```text
fastapi
pydantic>=2,<3
pydantic-settings
PyYAML
uvicorn
databricks-sdk
httpx
```

Add `databricks-sql-connector` in MDL-2 when direct trusted SQL is implemented unless it is already needed for a verified MDL-1 connectivity stub. Do not add heavy analytical packages merely because they may be useful later.

Development/test group:

```text
pytest
pytest-cov
hypothesis
ruff
mypy (locked as the Python type checker for MDL-1)
Pillow (image decode/dimension/alpha/contact-sheet preflight only)
httpx test support as needed
```

Required commands:

```bash
uv lock --check
uv sync --frozen --all-extras
uv run ruff check .
uv run mypy backend scripts
uv run pytest -m 'not live and not databricks_sql'
```

Codex must not make CI depend on packages preinstalled incidentally on GitHub or Databricks.

### Root `package.json` / Vite command blueprint

Codex may adjust exact pinned version numbers after `npm ci` compatibility testing, but the command topology is locked. The root package should be structurally equivalent to:

```json
{
  "private": true,
  "scripts": {
    "dev": "vite --config frontend/vite.config.ts",
    "typecheck": "tsc -p frontend/tsconfig.json --noEmit",
    "lint": "eslint frontend/src frontend/tests",
    "test": "vitest run --config frontend/vitest.config.ts",
    "api:generate": "uv run python scripts/export_openapi.py && openapi-typescript docs/api/openapi.json -o frontend/src/api/generated/openapi.d.ts",
    "api:check": "uv run python scripts/check_api_contract.py",
    "build": "vite build --config frontend/vite.config.ts",
    "test:e2e": "playwright test"
  }
}
```

Do not add a production `start` script that launches a second Node HTTP server. Databricks runs the Python command from `app.yaml`; the root Node project exists to build the browser bundle.

`frontend/vite.config.ts` must be structurally equivalent to:

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "node:path";

export default defineConfig(({ mode }) => ({
  root: resolve(__dirname),
  plugins: [react()],
  publicDir: resolve(__dirname, "../assets/production"),
  server: {
    host: "127.0.0.1",
    port: 5173,
    proxy: {
      "/api": "http://127.0.0.1:8000"
    }
  },
  build: {
    outDir: resolve(__dirname, "../backend/static"),
    emptyOutDir: true,
    assetsDir: "assets"
  }
}));
```

Use equivalent path handling if the chosen config format differs, but preserve the same source/output/public/proxy responsibilities. Do not include environment-specific workspace URLs in Vite `define`, `.env.production`, or browser constants.

### Exact local-development topology

Keep development and production topology simple and same-origin-compatible:

```text
FastAPI local backend   http://127.0.0.1:8000
Vite local frontend     http://127.0.0.1:5173
Vite /api proxy         -> http://127.0.0.1:8000
Production              one Databricks App origin served by FastAPI
```

Requirements:

- `backend.run` defaults to local port `8000` only when `APP_ENV` is non-production and no Databricks runtime port exists;
- Vite dev server proxies `/api` (and only required API development paths) to the local FastAPI server, so MDL-1 does not add permissive CORS solely for local development;
- application frontend code always calls relative `/api/...` URLs; no `localhost`, workspace hostname or Databricks App URL is hardcoded in browser source;
- `npm run dev` starts only the Vite dev server; start FastAPI separately with `uv run python -m backend.run` unless an explicitly tested cross-platform dev wrapper is later added;
- production does not run Vite's dev server or a second Node server;
- local fixture/stub behavior is explicitly keyed by `APP_ENV=local|test` and cannot be selected by a browser query parameter.

Add `MDL1-DEV-001` — browser production source contains no hardcoded `localhost`/workspace/App URL; `MDL1-DEV-002` — Vite dev proxy routes `/api/health` to local FastAPI; `MDL1-DEV-003` — production config contains no Vite dev-server dependency.

### Exact production build/serve layout

Lock the deployed hybrid application to **one server process** in MDL-1:

1. root `package.json` is present so Databricks detects Node and runs the build step;
2. Vite root is `frontend/`;
3. `npm run build` removes prior output and writes the immutable frontend production tree to `backend/static/` (or another single path chosen once and recorded);
4. Vite `publicDir` points at the authoritative approved production-media directory (recommended `../assets/production`) so approved assets are copied into the build without a second manually synchronized copy; review/rejected assets are outside `publicDir`;
5. generated bundle filenames are content-hashed;
6. FastAPI serves built static files from that directory;
7. FastAPI returns generated `index.html` for intended SPA/browser routes only;
8. `/api/*`, `/api/health`, and unknown API routes are never swallowed by the SPA fallback;
9. startup in production fails if the expected generated `index.html`/asset manifest is missing;
10. Vite dev server/proxy is never required in Databricks;
11. `dist/` is ignored/untracked and cannot shadow `backend/static/`.

A representative Vite contract is:

```text
root = frontend
outDir = ../backend/static
emptyOutDir = true
assetsDir = assets
publicDir = ../assets/production
manifest = true (or equivalent build manifest used by tests)
```

If a different output path is chosen, use it consistently in Vite, FastAPI, tests, `.gitignore`, asset scans, and deployment manifests.

### Runtime command and graceful shutdown

Prefer a Python launcher so platform environment parsing is centralized instead of embedding shell expansion in `app.yaml`. Example:

```yaml
command:
  - uv
  - run
  - python
  - -m
  - backend.run
```

`backend.run` must:

- bind host from `UVICORN_HOST` when provided, otherwise `0.0.0.0`;
- resolve port as `DATABRICKS_APP_PORT` → `UVICORN_PORT` → local `8000`;
- reject the local `8000` fallback when `APP_ENV=production` and no platform port is available;
- start `backend.main:app`;
- not spawn a second Node server in production;
- exit cleanly on SIGTERM and stay inside the Databricks shutdown window.

### Exact clean-install proof

Run the following from a fresh checkout/worktree after deleting generated output/caches:

```bash
node --version
npm --version
npm ci
npm run api:check
npm run typecheck
npm run lint
npm run test -- --run
rm -rf backend/static
npm run build

python --version
uv --version
uv lock --check
uv sync --frozen --all-extras
uv run ruff check .
uv run mypy backend scripts
uv run pytest -m 'not live and not databricks_sql'
```

Then start the production process against a non-default port and smoke it. The exact shell can be implemented in `scripts/smoke_local_production.py` so Windows/shell differences do not weaken the requirement.

Add tests:

- `MDL1-PKG-001` — exactly one Node lockfile and it matches package manifest;
- `MDL1-PKG-002` — `pyproject.toml` + `uv.lock` exist and no root production `requirements.txt` shadows uv;
- `MDL1-PKG-003` — production build dependencies are installed during a production-style Node install/build;
- `MDL1-PKG-004` — clean production build works after generated output deletion;
- `MDL1-PKG-005` — production process serves UI + API from one process;
- `MDL1-PKG-006` — SIGTERM shutdown completes within the platform window;
- `MDL1-PKG-007` — CI/local runtime versions satisfy the locked engine ranges;
- `MDL1-PKG-008` — no dependency uses literal `latest`;
- `MDL1-PKG-009` — no unreviewed duplicate Python/Node dependency source can override the selected lock strategy.

## Challenge Free Edition workspace attestation

Before building platform-dependent features, prove the staging/submission target is a **Databricks Free Edition** workspace as required by the challenge. Do not infer this from a profile name, catalog name, or the fact that serverless/Apps features exist.

Create `docs/iterations/MDL-1-workspace-attestation.md` plus a sanitized machine-readable companion in the release report containing:

```text
verified_at_utc
verification_method
workspace_alias_or_nonsecret_identifier
cloud/region if safely relevant
free_edition_verified: true|false|unknown
apps_available
genie_resource_available
sql_warehouse/resource availability
verifier
evidence_reference (private screenshot/admin page reference if needed; do not publish credentials)
```

Preferred verification is an official workspace/account/API property if one is available and documented. If the platform does not expose an edition flag suitable for automation, a human must verify the edition in the Databricks workspace/account UI and record the method/timestamp. `unknown` is a blocker for challenge closure.

Rules:

- the GitHub deployment environment/profile must resolve to the attested workspace, not a similarly named developer workspace;
- staging and final challenge production may be the same Free Edition workspace if the challenge setup requires it, but resource names/IDs and deployment source must remain explicit;
- no later iteration may silently switch the Databricks target without refreshing the attestation and all environment/resource evidence;
- workspace edition evidence can remain a protected CI/manual artifact if publishing the account page would expose personal data.

Add:

- `MDL1-WS-001` — deployment target identifier matches the workspace attestation;
- `MDL1-WS-002` — `free_edition_verified` must be true before MDL-1 can close;
- `MDL1-WS-003` — changing the deployment workspace invalidates the edition/resource attestation and blocks later deployment evidence until reverified.

## Runtime configuration tasks

### Centralize configuration

Create `backend/config.py` using a validated settings model. Normalize any platform-specific environment names in one place.

Required logical settings and runtime-provided boundaries:

```text
Application-owned/configured:
APP_ENV
DEFAULT_CASE_ID
ENABLE_AGENT_MODE
ENABLE_OFFLINE_DEMO
GENIE_SPACE_ID (official Databricks resource-injected Genie resource identifier)
internal normalized field: genie_agent_id / genie_space_id (choose one internal name and use it consistently)
SQL_WAREHOUSE_ID
GENIE_REQUEST_TIMEOUT_SECONDS
GENIE_POLL_INTERVAL_MS
MAX_GENIE_REPAIR_ATTEMPTS
LOG_LEVEL

Databricks runtime-provided / default-auth inputs:
DATABRICKS_HOST
DATABRICKS_CLIENT_ID
DATABRICKS_CLIENT_SECRET
DATABRICKS_APP_PORT
UVICORN_PORT when supplied by the runtime
UVICORN_HOST / runtime host when supplied
```

Authentication rules:

- application code uses the Databricks SDK/connector default authentication chain for the App service principal; it must not manually copy these credentials into application config files, browser payloads, logs, build artifacts, or test fixtures;
- `DATABRICKS_CLIENT_SECRET` is treated as a secret even though the runtime injects it; it is never exposed through `/api/config`, `/api/health`, diagnostics, stack traces, or structured logs;
- local development may use the developer's normal Databricks profile/default auth mechanism; repository-owned `.env` files containing credentials are forbidden;
- tests must prove that missing runtime credentials fail with the stable configuration/auth error rather than silently switching to fixture/offline mode in production;
- a runtime environment-variable inventory may record whether a variable is present, but never its secret value.

Current Databricks Apps documentation exposes a Genie Agent resource as a **space ID**, conventionally through `GENIE_SPACE_ID` with `valueFrom: genie-space` (or a custom resource key). Follow that platform contract at the `app.yaml` boundary. Internally, normalize it to exactly one validated settings field so the rest of the code does not alternate between Agent/Space environment names. If migrating the current repository from a legacy variable, support the legacy alias only inside `backend/config.py`, emit a deprecation warning in non-test logs, and remove the alias by MDL-6 unless still required by the deployed platform configuration.

### Port handling

The launcher must respect the Databricks app runtime port. Use a single helper with precedence documented and tested. Example logic:

```text
1. DATABRICKS_APP_PORT when present
2. UVICORN_PORT when present
3. 8000 only for local development
```

Do not hardcode port 8000 for production.

### `app.yaml`

Keep the app command simple and production-safe. Ensure resource bindings are explicit. At minimum plan for:

```text
Genie Agent resource with `CAN RUN` and a stable resource key (default platform key is `genie-space`)
`GENIE_SPACE_ID` mapped from that resource key through `valueFrom`
SQL warehouse resource when safe fallback/direct SQL is enabled
```

No secrets in `app.yaml`.

Lock these boundary names for MDL-1:

```text
GENIE_SPACE_ID        platform/app.yaml boundary
SQL_WAREHOUSE_ID      platform/app.yaml boundary
settings.genie_space_id
settings.sql_warehouse_id
```

Do not expose a second production setting named `GENIE_AGENT_ID`. A migration alias may be read only inside `backend/config.py` with a deprecation test/log if the current deployed app still injects that legacy name.

Reference `app.yaml` shape (resource keys must match the actual App resources):

```yaml
command:
  - uv
  - run
  - python
  - -m
  - backend.run
env:
  - name: APP_ENV
    value: production
  - name: DEFAULT_CASE_ID
    value: CASE_0042
  - name: ENABLE_AGENT_MODE
    value: "false"
  - name: ENABLE_OFFLINE_DEMO
    value: "false"
  - name: GENIE_SPACE_ID
    valueFrom: genie-space
  - name: SQL_WAREHOUSE_ID
    valueFrom: sql-warehouse
```

If the warehouse resource is not yet available in the target workspace, MDL-1 may keep the binding out of `app.yaml` only with `BLOCKED_DATABRICKS_CONFIGURATION`; do not invent a warehouse ID. MDL-2 cannot start its SQL work until the binding exists.

Add `MDL1-RUN-001` through `MDL1-RUN-006`: production port precedence, production fallback refusal, config secret exclusion, official Genie env normalization, offline/Agent flags false by default, and SIGTERM shutdown behavior.

The App runtime service principal receives only permissions that exist/are needed at this iteration boundary. In MDL-1, grant/verify `CAN RUN` on the selected Genie Agent resource and `CAN USE` on the selected SQL warehouse resource. Record the intended future Unity Catalog matrix in `docs/security/app-permissions.md`, but do **not** grant broad catalog/schema/table permissions before MDL-2 creates/identifies the exact curated objects. MDL-2 then grants only `USE CATALOG`, `USE SCHEMA`, and `SELECT` on those named curated objects and verifies them. If an existing table must be queried for an MDL-1 connectivity smoke, grant the smallest named read scope and record it as temporary security debt. Never grant `CAN MANAGE` or broad catalog access merely to make development easier.

## Canonical domain model tasks

### Create enums

Implement closed enums or equivalent validated types for every cross-layer vocabulary used by the MDL-1 foundation. Do not represent these as free-form strings in Python or TypeScript.

```text
CaseReleaseState:
  CORE
  TARGET
  FULL_GAME
  STRETCH
  ARCHIVED

CaseAvailability:
  AVAILABLE
  LOCKED
  COMING_SOON

CaseDifficulty:
  LEVEL_1
  LEVEL_2
  LEVEL_3

HypothesisPriority:
  HIGH
  MEDIUM
  LOW

EpistemicStatus:
  CONFIRMED
  SUPPORTED
  POSSIBLE
  RULED_OUT

Phase:
  BOOT
  CASE_CATALOG
  CASE_BRIEFING
  STARTING_INVESTIGATION
  HYPOTHESES_READY
  PLAYER_PREDICTION
  SELECTING_EXPERIMENT
  RUNNING_EXPERIMENT
  EXPERIMENT_RESULT
  EVIDENCE_EXPLORATION
  PLAYER_PREDICTION_FINAL
  CONCLUDING
  DEBRIEF
  UNRECOVERABLE_ERROR

ExperimentId:
  COMPONENT_DECOMPOSITION
  SNAPSHOT_DIFF
  SOURCE_RECORD_INSPECTION
  DQ_MATERIALITY
  FORMULA_VALIDATION
  FILTER_VALIDATION
  ROW_COUNT_ANALYSIS
  DUPLICATE_KEY_ANALYSIS
  PIPELINE_RUN_COMPARISON
  MISSING_RECORD_IMPACT
  ENTITY_COMPARISON
  JOIN_CARDINALITY_ANALYSIS
  VALUE_LINEAGE
  TECHNICAL_LINEAGE
  RECONCILIATION

InstrumentId:
  KPI_DELTA
  WATERFALL
  SNAPSHOT_DIFF
  EVIDENCE_TABLE
  DQ_PANEL
  LINEAGE_GRAPH
  ROW_COUNT_DELTA
  DUPLICATE_CLUSTER
  RUN_COMPARISON
  FORMULA_DIFF
  FILTER_DIFF
  ENTITY_COMPARISON
  CARDINALITY_MATRIX
  RECONCILIATION
```

The fact that `SNAPSHOT_DIFF`, `ENTITY_COMPARISON`, and `RECONCILIATION` occur in both Experiment and Instrument vocabularies is intentional; they are different enum types and must not be collapsed into one generic ID type.

MDL-1 implements the registries/types, not the live Experiment execution semantics. MDL-3/5 consume these exact IDs rather than creating new spellings.

Add iteration-specific enum assertions:

- `MDL1-DOM-001` — `CaseAvailability` is exactly `AVAILABLE|LOCKED|COMING_SOON`;
- `MDL1-DOM-002` — `CaseDifficulty` is exactly `LEVEL_1|LEVEL_2|LEVEL_3`;
- `MDL1-DOM-003` — `HypothesisPriority` is exactly `HIGH|MEDIUM|LOW`;
- `MDL1-DOM-004` — Experiment registry equals the 15 locked V3 IDs above;
- `MDL1-DOM-005` — Instrument registry equals the 14 locked V3 IDs above;
- `MDL1-DOM-006` — Experiment/Instrument enums are separate types even where string values overlap.

### Create domain models

At minimum:

```text
CaseDefinition
CasePublicMetadata
Hypothesis
Prediction
ExperimentDefinition
ExperimentEvent
EvidenceReference
Investigation
ScientificVerdict
ProgressionState
```

Requirements:

- no arbitrary string statuses;
- every model validates identifiers;
- browser-facing payloads exclude private fields;
- `case_id` is immutable within an Investigation;
- events are append-only at the domain layer;
- no model may assume exactly three experiments.

## Case catalog tasks

### Create `cases/catalog.yaml`

Include all seven canonical public Cases as metadata, but only Case #042 must be `CORE` and playable.

Encode the exact public catalog baseline below. MDL-1 deliberately uses `COMING_SOON` for every secondary Case because progression/unlock semantics are not implemented until MDL-4; do not pretend those Cases are merely locked by gameplay when they are not yet release-ready.

| Case ID | Public # | Title | Difficulty | Release state | MDL-1 availability | Public concept tags |
|---|---:|---|---|---|---|---|
| `CASE_0042` | 42 | The Missing €6.8M | `LEVEL_2` | `CORE` | `AVAILABLE` | decomposition, snapshot diff, DQ materiality, lineage |
| `CASE_0107` | 107 | Attack of the Clones | `LEVEL_1` | `TARGET` | `COMING_SOON` | row counts, duplicates, pipeline replay |
| `CASE_0213` | 213 | The Vanishing Revenue | `LEVEL_2` | `TARGET` | `COMING_SOON` | filters, semantic logic, lineage |
| `CASE_0314` | 314 | The Ghost Records | `LEVEL_2` | `FULL_GAME` | `COMING_SOON` | missing rows, business impact |
| `CASE_0441` | 441 | The Red Herring | `LEVEL_2` | `FULL_GAME` | `COMING_SOON` | DQ materiality, skepticism |
| `CASE_0520` | 520 | The Impossible Forecast | `LEVEL_2` | `FULL_GAME` | `COMING_SOON` | joins, entity mix, population |
| `CASE_0812` | 812 | Double Trouble | `LEVEL_3` | `STRETCH` | `COMING_SOON` | multi-cause reconciliation |

For `CASE_0042`, the public hook is locked to: **“€6.8M vanished from Capital Available.”** Other public hooks may be copied from the definitive Case templates when those templates are introduced, but MDL-1 must not invent answer-revealing hooks.

The server, not the frontend, decides availability. MDL-4 may transition shipped secondary Cases from `COMING_SOON` to `LOCKED`/`AVAILABLE` only after progression/release rules exist and their automated Case contracts pass.


#### Exact catalog record contract

Each YAML record must validate through the backend domain schema before it is exposed. Required MDL-1 fields:

```yaml
case_id: CASE_0042              # ^CASE_[0-9]{4}$
public_number: 42               # positive integer; unique
slug: the-missing-6-8m          # lowercase URL-safe; unique
title: The Missing €6.8M
hook: €6.8M vanished from Capital Available.
difficulty: LEVEL_2
release_state: CORE
availability: AVAILABLE
sort_order: 10
required_case_ids: []
learning_objectives:
  - DECOMPOSITION
  - SNAPSHOT_DIFF
  - DQ_MATERIALITY
  - LINEAGE
case_template: templates/case_0042.yaml
```

Rules:

- YAML duplicate keys are rejected rather than silently taking the last value;
- unknown fields are rejected in MDL-1 catalog records unless explicitly versioned later;
- `case_id`, public number and slug are unique;
- sort order is deterministic and unique for visible catalog entries;
- `required_case_ids` reference known Cases and contain no self-reference/cycle (even though MDL-1 secondary Cases are `COMING_SOON`);
- `CORE` does not itself imply browser availability: availability is a separate server decision;
- `COMING_SOON` Cases cannot create sessions;
- template path is server/internal metadata and is not serialized in `CasePublicMetadata`;
- no record contains `primary_cause`, expected path/oracle, hidden-truth link, mutation operator details, or answer-bearing status.

Create a domain loader such as `backend/domain/cases.py` that loads/validates this file once at startup (or under an explicit reload mechanism in development), fails startup on invalid production catalog, and exposes immutable typed records to the API layer.


### No answer leakage

Public catalog payloads must not include:

```text
primary_cause
hidden truth
expected analytical path oracle
private expected status oracle
private mutation metadata
```

### Case #042 hypothesis contract

Replace every current prototype hypothesis with exactly:

```text
H1 - Source values changed
H2 - Formula changed
H3 - Data quality issue
```

For the canonical Case #042 initial Genie analysis, the contract is:

```text
H1 HIGH
H2 LOW
H3 MEDIUM
```

These are initial investigation priorities, not epistemic statuses or probabilities. The live Genie response may explain the priority in its own concise wording, but it must not silently invert the Case #042 golden priority contract in the release path.

Do not reuse:

```text
Promo effect?
Data bug?
Pricing change?
Seasonal factor?
```

Add a static repository scan test that fails if those legacy strings occur in production source.

## Multi-Case genericity and hardcode guard

V3 decision D-009 is structural: Case #042 is the challenge release blocker, not permission to build a single-Case control flow.

Create `scripts/check_case_genericity.py` (or equivalent AST/text-aware check) with an explicit allowlist. The literal `CASE_0042`, public number `42`, and golden values may legitimately appear in:

```text
cases/templates/case_0042.*
data/fixtures/golden Case #042 files
tests explicitly named as Case #042 golden/benchmark tests
genie/benchmarks Case #042 prompt/oracle fixtures
submission/demo documentation that intentionally names the demo Case
```

They must not drive generic runtime control behavior in:

```text
backend API routing
state-machine transition logic
scoring engine
Experiment/Instrument registry logic
frontend page routing
progress calculation
Case availability logic
Evidence Explorer generic filtering
error/retry behavior
```

Case-specific content should arrive through the Case template/catalog/evidence contracts. A generic component may display the literal value it received from the API; it must not branch on `if case_id == CASE_0042` merely to make the demo work unless the branch is part of a formally registered Case completion/validator plug-in boundary.

If a Case-specific completion validator is needed, dispatch it through a versioned registry keyed by completion contract rather than ad-hoc conditionals scattered through controllers/components.

Iteration-specific checks:

- `MDL1-GEN-001` — disallowed frontend/backend runtime paths contain no unapproved `CASE_0042` literal;
- `MDL1-GEN-002` — progress/Experiment count is derived from Investigation/Case state rather than literal 3/5;
- `MDL1-GEN-003` — adding a synthetic second catalog fixture can render Case Board/Briefing without source-code edits;
- `MDL1-GEN-004` — unknown Case IDs use generic not-found/unavailable behavior, not Case #042 fallback;
- `MDL1-GEN-005` — Case-specific validators are reachable only through the explicit completion-contract registry.


## State machine tasks

Create `backend/domain/state_machine.py` or equivalent.

Requirements:

- legal transitions are explicit;
- illegal jumps are rejected;
- transition validation is server-side;
- state change appends an event rather than mutating prior events;
- switching Cases creates a new session;
- no browser field can force a future state;
- analytical fields are never optimistically updated by the frontend.

Minimum legal shell transition path:

```text
BOOT -> CASE_CATALOG
CASE_CATALOG -> CASE_BRIEFING
CASE_BRIEFING -> STARTING_INVESTIGATION
STARTING_INVESTIGATION -> HYPOTHESES_READY
HYPOTHESES_READY -> PLAYER_PREDICTION
PLAYER_PREDICTION -> SELECTING_EXPERIMENT
SELECTING_EXPERIMENT -> RUNNING_EXPERIMENT
RUNNING_EXPERIMENT -> EXPERIMENT_RESULT
EXPERIMENT_RESULT -> EVIDENCE_EXPLORATION or SELECTING_EXPERIMENT or PLAYER_PREDICTION_FINAL
PLAYER_PREDICTION_FINAL -> CONCLUDING
CONCLUDING -> DEBRIEF
DEBRIEF -> CASE_CATALOG
```

Exact conditional transitions should be represented with domain guards rather than client-only logic.

## API skeleton tasks

### Explicit V3 API-envelope reconciliation

V3 §35 states a general application JSON envelope, while V3 §35.1 shows `/api/health` as a flat platform-health payload. MDL-1 resolves this internal source mismatch explicitly:

- `/api/health` is the **only MDL-1 flat JSON exception** because it is a cheap platform probe and should remain easy for deployment tooling to consume;
- all other application JSON endpoints use the V3 success/error envelope;
- record this interpretation in `docs/decisions/ADR-001-health-envelope-exception.md` so it is not mistaken for an accidental inconsistency.

If the human owner wants health enveloped instead, change the ADR/spec and its tests before implementation; do not maintain both shapes.

### Canonical application envelope

Success:

```json
{
  "ok": true,
  "data": {},
  "error": null,
  "request_id": "uuid-or-stable-request-id"
}
```

Error:

```json
{
  "ok": false,
  "data": null,
  "error": {
    "code": "CASE_NOT_FOUND",
    "message": "The requested Case does not exist.",
    "retryable": false
  },
  "request_id": "uuid-or-stable-request-id"
}
```

Rules:

- one middleware/request-context helper creates `request_id` when missing;
- do not reflect arbitrary stack traces/exception repr into `message`;
- validation errors are normalized to the application error contract at the boundary where practical without destroying useful HTTP status codes;
- browser-facing errors never include resource IDs/secrets/hidden truth;
- HTTP status and stable error code both matter; tests assert both.

### `GET /api/health` — flat cheap probe

Target shape:

```json
{
  "status": "ok",
  "version": "0.1.0",
  "app_env": "staging",
  "genie_configured": true,
  "warehouse_configured": true
}
```

Rules:

- 200 when the process/config foundation is healthy;
- no live Genie/warehouse call in ordinary health;
- `genie_configured` means a non-empty validated `GENIE_SPACE_ID` is configured, **not** “Genie is reachable/live”;
- never return the actual Genie/warehouse ID, host credential, client ID/secret, token, profile or hidden truth;
- connectivity/readiness belongs to a separate later probe/integration test.

### `GET /api/config`

Enveloped `data` may contain only non-sensitive UI/runtime facts required by the shell, for example:

```json
{
  "app_name": "MAD DATA LAB",
  "app_version": "0.1.0",
  "app_env": "staging",
  "default_case_id": "CASE_0042",
  "challenge_track": "TRACK_B_CREATIVE_THINKING",
  "offline_demo_enabled": false,
  "agent_mode_enabled": false
}
```

Do not return `GENIE_SPACE_ID`, warehouse ID, workspace host, App SP identifiers/secret, source-table details or filesystem paths.

### `GET /api/cases`

Return public catalog metadata only. Minimum item contract:

```json
{
  "case_id": "CASE_0042",
  "public_number": 42,
  "slug": "the-missing-6-8m",
  "title": "The Missing €6.8M",
  "hook": "€6.8M vanished from Capital Available.",
  "difficulty": "LEVEL_2",
  "release_state": "CORE",
  "availability": "AVAILABLE",
  "learning_objectives": ["DECOMPOSITION", "SNAPSHOT_DIFF", "DQ_MATERIALITY"]
}
```

Completion/best-score fields may be absent/null until progression is implemented, but no truth/path oracle may appear.

### `GET /api/cases/{case_id}`

For a released/available Case return the public briefing/observation contract required by the skeleton. For a known but unreleased Case return a stable `CASE_UNAVAILABLE`; for unknown IDs return `CASE_NOT_FOUND`. Do not leak whether a hidden truth row exists.

### `POST /api/sessions`

Request:

```json
{"case_id":"CASE_0042"}
```

Response `data`:

```json
{
  "session_id": "uuid",
  "case_id": "CASE_0042",
  "state": "CASE_BRIEFING",
  "score": 0
}
```

Rules:

- generate unguessable UUID-like session IDs;
- validate Case availability server-side;
- session `case_id` is immutable;
- score starts at 0;
- no Genie conversation is started yet in MDL-1 unless a later-iteration integration is intentionally pulled forward with its owning tests;
- creating a session never grants access to hidden truth.

### MDL-1 HTTP/status mapping

| Condition | HTTP | Error code |
|---|---:|---|
| invalid request shape | 422 | `VALIDATION_ERROR` |
| unknown Case | 404 | `CASE_NOT_FOUND` |
| known unreleased/unavailable Case/session request | 409 | `CASE_UNAVAILABLE` |
| configuration missing for a required shell operation | 503 | `MISSING_ENVIRONMENT_VARIABLE` or stable config code |
| unexpected internal failure | 500 | `INTERNAL_ERROR` with sanitized message |

Record this mapping in `docs/api/error-contract.md`; generated OpenAPI/tests become authoritative afterward. `CASE_UNAVAILABLE` deliberately uses 409 rather than 403 because V3 progression is cosmetic, not an authorization/security boundary. Do not let endpoints choose independently.

### API skeleton tests — iteration-specific

Add:

- `MDL1-HTTP-001` — health is the documented flat exception and contains no secret/resource ID;
- `MDL1-HTTP-002` — all non-health MDL-1 application JSON endpoints use canonical success/error envelope;
- `MDL1-HTTP-003` — every response/request ID required by the envelope is non-empty and log-correlatable;
- `MDL1-HTTP-004` — known unavailable and unknown Case produce distinct stable codes without answer leakage;
- `MDL1-HTTP-005` — session IDs are UUID-like/unpredictable and Case ID is immutable;
- `MDL1-HTTP-006` — session score begins at zero;
- `MDL1-HTTP-007` — stack traces/secrets do not appear in API errors;
- `MDL1-HTTP-008` — API route errors cannot be converted into SPA HTML by the frontend catch-all.

### API schema/OpenAPI contract — prevent backend/frontend drift

Pydantic/FastAPI response/request models are the authoritative application API schema. MDL-1 must not maintain a second independently invented TypeScript contract by hand.

Implement one reproducible contract path:

1. export FastAPI OpenAPI deterministically with `scripts/export_openapi.py` to **exactly** `docs/api/openapi.json`;
2. normalize nondeterministic metadata/order in the exporter so two exports from the same source are byte-identical;
3. generate TypeScript API types with the pinned `openapi-typescript` package to **exactly** `frontend/src/api/generated/openapi.d.ts`; do not hand-maintain a parallel API interface tree;
4. commit both the reviewed OpenAPI contract and generated TypeScript types because the frontend build consumes the committed contract output;
5. add `npm run api:generate` and `npm run api:check`;
6. `api:generate` exports OpenAPI then regenerates `frontend/src/api/generated/openapi.d.ts`;
7. `api:check` regenerates both into a temporary directory and fails on any diff, so a developer cannot make a backend schema change without updating the committed contract;
8. contract tests assert the application envelope, health exception, and that private fields such as hidden truth never appear in public schemas;
9. `frontend/src/api/client.ts` imports only generated public contract types plus small explicit runtime envelope/type guards; page components do not cast raw JSON with `as SomeType` to bypass validation.

Do not add an unrestricted runtime schema library solely for this if generated types + API contract tests are sufficient. Runtime data received from the server must still be parsed defensively at the API boundary and must never be rendered as trusted HTML.

Add:

- `MDL1-API-SCHEMA-001` — OpenAPI export is deterministic;
- `MDL1-API-SCHEMA-002` — generated frontend API types are current;
- `MDL1-API-SCHEMA-003` — public OpenAPI contains no `CASE_TRUTH`/private oracle fields;
- `MDL1-API-SCHEMA-004` — every non-health MDL-1 application endpoint uses the canonical response/error envelope and health matches its explicit exception;
- `MDL1-API-SCHEMA-005` — unknown `/api/*` returns API JSON semantics, not the SPA HTML shell.

## Frontend migration tasks

### TypeScript

Convert current entrypoints to TypeScript:

```text
frontend/src/main.tsx
frontend/src/App.tsx
frontend/src/api/client.ts
frontend/src/api/schemas.ts
```

Do not use `any` for server response payloads except temporary boundary parsing that is immediately validated.

### Data ownership

Remove frontend hardcoded analytical truth. The frontend may temporarily render fixture APIs, but it must not contain the canonical Case #042 experiment evidence or verdict as hidden fallback constants.

### Case Board skeleton

Render Case cards from `GET /api/cases`.

Case #042 must be clearly available. Other Cases must render their server-provided state.

Do not make availability decisions by checking numeric Case IDs in JSX.

### Case Briefing skeleton

Render from `GET /api/cases/{case_id}`.

No Case #042 copy hardcoded directly inside the page component except generic labels.

### MDL-1 visual-shell contract

MDL-1 is not the full visual-polish iteration, but the skeleton must already stop using the obsolete lime/pink arcade UI and fantasy-genie identity. Establish semantic tokens in `frontend/src/styles/tokens.css`:

```text
--background-deep
--surface-1
--surface-2
--text-primary
--text-secondary
--accent-science       cyan/teal family
--accent-energy        restrained coral family
--accent-evidence      violet family
--status-confirmed     green family
--status-possible      amber family
--status-ruled-out     desaturated neutral/red family
--border-subtle
--focus-ring
```

Requirements:

- functional/body typography uses a clean sans/system family; decorative/pixel type is not the body UI foundation;
- MDL-1 has no runtime dependency on Google Fonts or another third-party font/CDN request; use a system sans stack for the foundation and add any packaged/licensed font only in a later visual iteration with asset/license review;
- numeric values use tabular numerals where supported;
- A28 is a decorative lab background only and cannot provide functional UI;
- A21 is decorative/supporting Case #042 card art; title, hook, difficulty, availability and action remain DOM text;
- A02 may appear in the Genie panel/briefing shell only after its exact production bytes are human-approved; until then use a clearly non-final neutral layout placeholder, never a fantasy-genie emoji;
- images with duplicated adjacent textual meaning use empty/decorative alt as appropriate; functional controls always have semantic accessible names;
- Case Board remains usable when A21/A28 fail to load; art is progressive enhancement, not navigation.

Case Board integration after art approval:

```text
A28 -> atmospheric page/background layer
A21 -> Case #042 featured-card image
A01 -> app/favicon/mark usage where technically appropriate
A02 -> Dr. Genie shell/briefing portrait if that component is present in MDL-1
```

Add `MDL1-UI-001` through `MDL1-UI-008`: no legacy lime/pink primary tokens, no fantasy-genie emoji identity, Case Board works with images disabled, Case text is DOM text, server availability drives controls, 1280×720 has no critical horizontal overflow, 1440×900 integration preview uses approved assets only, and the foundation UI makes no third-party runtime font/CDN request. Full visual regression/a11y closure remains owned by MDL-5/MDL-6.

### Staging-only incomplete-flow behavior

MDL-1 is intentionally not the complete challenge game. The staging deployment must be honest about that without faking later behavior.

- In `APP_ENV=staging`, a small non-intrusive `FOUNDATION BUILD / MDL-1` marker may be shown in the shell.
- The Case Board and Briefing are real. `POST /api/sessions` may create the authoritative session skeleton.
- If the UI reaches a control whose real Genie/game behavior belongs to MDL-3/MDL-4, stop at an explicit non-production development state rather than returning scripted analytical evidence.
- Do **not** show the development marker when `APP_ENV=production`; a release test in later iterations removes/forbids it.
- Do not publish the MDL-1 staging URL/video as the challenge-complete experience.

This rule prevents a temporary scaffold from reintroducing the exact “static game that works without Genie” failure the project is trying to eliminate.

## Logging and observability foundation

Create structured JSON logging. Every API request should produce a `request_id`.

Fields to support as they become available:

```text
ts
level
event
request_id
session_id
case_id
experiment_id
duration_ms
fallback_used
genie_conversation_id
genie_message_id
diagnostic_code
```

Never log secrets or hidden truth in ordinary request logs.

## Developer documentation and one-command execution contract

MDL-1 must leave the repository usable by the next Codex session and by a human reviewer who did not perform the migration. Documentation is part of the executable baseline, not an optional cleanup item.

### Required repository documentation

Create/update these files before the final MDL-1 local gate:

```text
README.md
CONTRIBUTING.md
.env.example
docs/development/local-setup.md
docs/development/architecture.md
docs/operations/staging-deploy.md
docs/operations/rollback.md
docs/engineering/required-github-checks.md
.github/pull_request_template.md
```

`README.md` must contain at least:

- the locked one-sentence product statement and Track B context;
- prerequisites: Node 22.16-compatible runtime, Python 3.11, `uv`, npm, Git, optional Databricks CLI for deployment work;
- exact clean local setup commands using npm + `package-lock.json` and `uv` + `uv.lock`;
- exact frontend/backend development commands;
- exact complete local gate command;
- brief repository map;
- statement that Case #042 is the CORE release blocker and secondary Cases are not production-playable merely because metadata exists;
- statement that Genie live orchestration starts in MDL-3 and fixture/static placeholders are never a production substitute;
- link to the V3 source, locked decisions, platform verification, art approval and iteration report locations;
- no credentials, workspace personal URLs, hidden truth values, or developer-specific absolute paths.

`.env.example` must contain only safe local/configuration **names and non-secret sample values**. It may demonstrate `APP_ENV=local`, `DEFAULT_CASE_ID=CASE_0042`, feature flags and timeouts. It must not contain a Databricks client secret, PAT, personal workspace token, real secret-bearing `.env` material, or a production offline-demo override.

`CONTRIBUTING.md` must state the mandatory branch/CI/art-approval rules, including the rule that Codex cannot self-approve generated art and that a runtime-affecting PR-head change invalidates stale CI/deployment evidence.

### Canonical one-command MDL-1 gate

Create `scripts/run_iteration_gate.py` as the single local/CI orchestration entry point for iteration-level validation. It does not replace the underlying tools; it invokes and records them consistently.

Required interface:

```bash
uv run python scripts/run_iteration_gate.py --iteration MDL-1 --profile local
uv run python scripts/run_iteration_gate.py --iteration MDL-1 --profile pr
uv run python scripts/run_iteration_gate.py --iteration MDL-1 --profile deploy-preflight
```

Required semantics:

- unknown iteration/profile exits non-zero;
- every invoked command and exit code is recorded without leaking secrets;
- deterministic failures stop the gate and cannot be converted to warnings;
- zero collected tests for a required test family is failure;
- new skips/xfails are summarized and checked against the allowlist/traceability policy;
- `local` includes clean/reproducibility-sensitive checks feasible locally, static/type/unit/contracts, OpenAPI drift, production build/package smoke and art preflight; human approval may report `PENDING` while engineering is in progress, but closure mode must fail until it is approved;
- `pr` mirrors the deterministic required PR surfaces and emits machine-readable evidence for CI;
- `deploy-preflight` validates clean Git identity, exact `implementation_sha`, target, source fingerprint, feature flags, bundle/app config and required deployment inputs without printing secrets;
- output is written to `release-report/MDL-1/gate.json` and a human-readable `release-report/MDL-1/gate.md` (or an explicitly equivalent ignored/CI-artifact path);
- exit code is zero only when every requirement for the selected profile is green.

CI jobs may run lower-level commands in parallel for speed, but the repository contract must prove they use the same scripts/configuration/lockfiles as the one-command gate. Do not maintain two subtly different validation definitions.

Add:

- `MDL1-GATE-001` — each supported profile executes a non-empty declared check set;
- `MDL1-GATE-002` — one failing underlying command makes the gate non-zero;
- `MDL1-GATE-003` — required zero-test collection is failure;
- `MDL1-GATE-004` — gate evidence redacts known secret environment values;
- `MDL1-GATE-005` — deploy-preflight rejects dirty working tree, wrong branch/SHA or unknown target;
- `MDL1-GATE-006` — README documented commands execute successfully in CI or a clean validation container/environment.

### Specification/repository contract self-audit

Create `scripts/validate_mdl1_contract.py` and make it part of `mdl1/repository-contract` and the one-command iteration gate. This is a structural guard against the implementation drifting away from this very detailed handoff. At minimum it validates:

- the accepted V3 source fingerprint and MDL-1 source/addendum metadata exist and are syntactically valid;
- required repository files/entrypoints/workflows from the MDL-1 target tree exist;
- Markdown/YAML/JSON files required for closure parse successfully;
- iteration-owned custom IDs are unique; canonical V3 primary ownership stays unique across the eight-iteration ledger;
- required artwork IDs A01/A02/A21/A28, prompts, manifest entries and approval entries are present exactly once;
- no unresolved `TODO`, `TBD`, fake `PASS`, `<PINNED_IMMUTABLE_SHA>` or other documentation metavariable has leaked into executable YAML/code/config;
- source files do not reintroduce legacy `src/main.jsx`, authoritative old `server/` implementations, production `board.png`, fantasy-genie emoji/art references, or checked-in generated caches;
- required GitHub check names in policy match workflow jobs;
- `databricks.yml`, `app.yaml`, `.env.example` and config model agree on resource/env names;
- OpenAPI artifact/generated frontend schema is current after backend API changes;
- the MDL-1 report cannot be `COMPLETE` while blockers/gates/approval fields are pending.

The validator may have an `--allow-in-progress` mode while the branch is under development. The closure/PR required check must run strict mode. It must distinguish intentional documentation metavariables from unresolved placeholders in executable files rather than banning angle brackets globally.

Add `MDL1-CONTRACT-001` through `MDL1-CONTRACT-010` covering the above surfaces.

### Pull-request template

`.github/pull_request_template.md` must make the closure contract visible to reviewers. Include fields/checks for:

```text
Iteration / branch
V3 source SHA/addenda
Implementation SHA/tree
Scope summary
Tests added/changed
Local gate result
Required CI result
Databricks deployment target/result
Artwork required? IDs
Artwork source-selection status
Artwork final approval status + approval evidence refs
Runtime-affecting changes after deployment? yes/no
Known deferrals with owning MDL-N
Security/permission changes
Rollback reference
```

A checked Markdown box is never evidence by itself; the PR template points to the machine/human evidence records required elsewhere in this specification.

## GitHub CI tasks

### Required PR workflow

Create `.github/workflows/ci.yml` triggered on:

```text
pull_request -> main
push -> main
workflow_dispatch
```

At minimum jobs must cover:

1. repository validation;
2. Node clean install;
3. TypeScript typecheck;
4. frontend lint;
5. frontend unit tests;
6. frontend production build;
7. Python install;
8. Ruff;
9. Python type checking;
10. Python unit/domain tests;
11. secret scan;
12. package/asset size sanity check.

Use dependency caches only if they do not bypass lockfile integrity.

### Required MDL-1 CI check names and responsibilities

Use stable check/job names so branch protection can target semantics rather than whatever Codex happens to name a job that day. The workflow may split jobs internally, but the PR must expose at least these required checks (or an explicitly documented one-to-one equivalent):

```text
mdl1/repository-contract
mdl1/frontend
mdl1/backend
mdl1/security-static
mdl1/art-preflight
mdl1/human-approval-gate
mdl1/production-package-smoke
mdl1/release-contract
```

Minimum responsibility:

- `repository-contract`: source fingerprint, branch/base, lockfile strategy, traceability schema, catalog/domain/static scans, zero-test detection;
- `frontend`: `npm ci`, OpenAPI/type-generation drift check, typecheck, lint, unit tests, clean production build;
- `backend`: `uv sync --frozen`, Ruff, mypy, pytest;
- `security-static`: secret scan, unsafe-render/truth/legacy artifact scans, GitHub workflow permission/pinning checks;
- `art-preflight`: manifest/schema/hash/dimensions/size/alpha/production-reference checks;
- `human-approval-gate`: validates exact-byte human `APPROVED` records and intentionally remains red/pending until a human approval exists;
- `production-package-smoke`: launches the clean built FastAPI package on a non-default port and verifies `/`, `/api/health`, `/api/config`, `/api/cases`, static assets, API 404 semantics and graceful shutdown;
- `release-contract`: validates iteration manifest/report closure semantics, V3 test/section traceability, source fingerprint/addenda, human approval consistency and zero unresolved required evidence.

Branch protection should require these checks before merge. If Codex cannot configure GitHub rulesets due to admin permissions, use `BLOCKED_GITHUB_ADMIN_CONFIGURATION`; do not treat a workflow file alone as proof that checks are required.

### Branch naming guard

Add a mandatory iteration-branch validation rule. When a pull request is declared as an MAD DATA LAB iteration, its branch must match exactly:

```text
MDL-1
MDL-2
...
MDL-8
```

A generic maintenance/hotfix branch does not need to match this pattern, but it must not claim to close an iteration. The iteration report/manifest `iteration` value and PR head branch must agree. CI must reject `MDL-01`, `MDL_1`, `mdl-1`, or a reused prior-iteration branch as an iteration-closure branch.

### Test reports

Upload or expose:

```text
JUnit XML
frontend test report if available
build artifact or build summary
```

### GitHub Actions trust-boundary requirements

The deploy workflow carries Databricks OIDC authority and must be treated as a security boundary.

- Do not use `pull_request_target` to check out and execute untrusted PR-head code with repository secrets/OIDC permissions.
- PR validation jobs should use read-only permissions unless a specific write permission is required.
- Grant `id-token: write` only to the trusted deployment job and only under the intended repository/environment conditions.
- A fork/untrusted PR must never be able to trigger a Databricks deployment with project credentials.
- Use protected GitHub Environments for staging/production where available; production must require explicit human/environment authorization by the final iterations.
- Pin third-party actions to immutable commit SHAs; for first-party GitHub actions, prefer immutable pins as well and record/update them deliberately.
- Cache keys must include the relevant lockfile hash; restore caches may accelerate installation but never replace `npm ci`/equivalent lock enforcement.
- Do not upload `.env`, OAuth tokens, Databricks auth files, raw private truth, or unredacted Genie/internal traces as workflow artifacts.
- Configure workflow `concurrency` so deployments to the same environment are serialized. For MDL-1 use `cancel-in-progress: false` once mutation can begin, because cancelling a Databricks deployment/restart mid-flight can leave ambiguous platform state. Newer accepted deployments wait behind the running deployment; immediately before each mutation the job revalidates its exact requested `implementation_sha`/authorization. A stale queued run must be cancelled or fail that pre-mutation freshness check rather than deploy obsolete code.
- Avoid path filters on required checks unless the workflow always emits a conclusive required status. A skipped workflow that leaves branch protection with no required status is not acceptable.

Add workflow-security assertions/lint for the repository's GitHub Actions and capture the effective job `permissions:` blocks in the MDL-1 report. At minimum fail on `pull_request_target` + PR-head checkout/execution, unexpected `id-token: write`, unpinned third-party actions, and deployment jobs without environment/concurrency protection.

### Required-check topology and branch-protection proof

CI existing is not sufficient; the repository must be configured so required iteration gates cannot be merged around. Establish stable job/check names and document them in `docs/engineering/required-github-checks.md`. At MDL-1 closure the protected merge surface must use the **same exact check names defined above**:

```text
mdl1/repository-contract
mdl1/frontend
mdl1/backend
mdl1/security-static
mdl1/art-preflight
mdl1/human-approval-gate
mdl1/production-package-smoke
mdl1/release-contract
```

Store this canonical list once in version control (for example `docs/engineering/required-github-checks.md` or a small machine-readable companion file), generate/validate both workflow expectations and ruleset evidence from it, and reject drift. Do not maintain a second alias list for branch protection.

As later iterations add data, Genie, E2E, visual, accessibility, security, and release jobs, update the required-check document/ruleset deliberately. Do not rename required checks casually because a renamed job can silently stop being protected.

Where repository permissions allow it, configure a GitHub ruleset/branch protection for `main` that requires:

- pull request before merge;
- required status checks on the latest commit;
- conversation resolution where the repository uses review comments;
- no force pushes/deletion of `main`;
- no administrator/bypass path used for ordinary iteration closure;
- stale required checks invalidated when the PR head changes;
- required deployment/environment approval when configured for staging/prod.

Use `gh api` or the GitHub UI/API to capture the observed protection/ruleset state in the MDL-1 report. If Codex lacks permission to create or inspect branch protection, it must report `BLOCKED_GITHUB_ADMIN_CONFIGURATION` and provide the exact required configuration for a human administrator. Do not call MDL-1 fully closed until the required checks are actually protected or an equivalent organization ruleset is demonstrably active.

Add a CI/meta test or script that compares the expected required-check names in version control with the workflow job/check names so a later workflow refactor cannot silently orphan branch protection.

Iteration-specific checks:

- `MDL1-GH-001` — `main` is protected by the expected active ruleset/branch protection;
- `MDL1-GH-002` — required-check names in policy match emitted workflow checks;
- `MDL1-GH-003` — PR-head update invalidates/re-runs relevant required checks;
- `MDL1-GH-004` — `human-approval-gate` is required and cannot pass while required art approval records are missing/stale;
- `MDL1-GH-005` — iteration manifest branch name and actual PR head match exactly.

## GitHub -> Databricks deployment workflow

Create `.github/workflows/deploy.yml` based on the current official Databricks Apps CI/CD pattern.

Authentication is locked to GitHub Actions workload identity federation / OIDC for the MDL-1 compliant path. Do not add a long-lived Databricks PAT/client secret to GitHub just to make deployment easier. If OIDC cannot be configured because of repository/workspace administration, stop with `BLOCKED_DATABRICKS_CONFIGURATION` or `BLOCKED_GITHUB_ADMIN_CONFIGURATION` and record the exact human/admin action required.

### Deployment and runtime identities — do not conflate them

Record two different service-principal roles:

1. **GitHub deployment service principal** — authenticated from GitHub by OIDC/workload identity federation; needs only deployment-management permissions such as `CAN MANAGE` on the App/bundle resources.
2. **Databricks App runtime service principal** — automatically assigned to the running App; needs only the App resources/data permissions required at runtime (eventually Genie `CAN RUN`, warehouse `CAN USE`, and UC `USE`/`SELECT`).

Never make the browser or runtime app depend on the GitHub deployment identity. Never grant the GitHub deployment principal broad data access just because it can deploy.

For an existing App, bind the bundle to the existing resource rather than accidentally creating a second challenge App. Record the binding command/result or equivalent App-resource ID mapping.

For staging deployment from an iteration branch, prefer **commit-pinned Git source**. Current Databricks App/Bundle schemas support `git_source.commit` in recent CLI schemas (the App `git_source` Bundle field was added in the current 0.290-era schema). Pin/test a Databricks CLI version that supports the chosen App resource fields and record `databricks version` in CI. If the installed CLI/schema or repository setup requires branch-based source, the deployment gate must read Databricks' `resolved_commit` and fail unless it equals `implementation_sha`. A branch name by itself is not deployment provenance.

Required workflow behavior:

1. `actions/checkout`;
2. install Databricks CLI;
3. authenticate through OIDC;
4. `databricks bundle validate`;
5. `databricks bundle deploy`;
6. `databricks bundle run <app-resource>` so the new code actually restarts;
7. poll app status until RUNNING or fail;
8. call automated health/smoke script;
9. archive smoke output.

### Staging GitHub Environment and workload-identity configuration — exact admin contract

Create a GitHub Environment named `staging` before the deploy workflow is allowed to pass. This follows the current Databricks Apps CI/CD guidance: GitHub supplies a short-lived OIDC identity; the Databricks deployment service principal has the federation policy and `CAN MANAGE` on the target App; no client secret/PAT is stored for this path.

Required **non-secret** GitHub Environment variables for MDL-1:

| Variable | Meaning | Validation |
|---|---|---|
| `DATABRICKS_HOST` | exact attested Free Edition workspace URL | HTTPS URL; equals workspace-attestation record |
| `DATABRICKS_CLIENT_ID` | GitHub deployment service-principal application ID | UUID/non-empty; not the App runtime SP identity |
| `DATABRICKS_APP_NAME` | target staging/challenge App name | non-empty; resolves through Apps API |
| `GENIE_SPACE_ID` | existing Genie Agent/space resource ID | non-empty; never exposed to frontend |
| `SQL_WAREHOUSE_ID` | trusted SQL warehouse resource ID | non-empty; never exposed to frontend |
| `DATABRICKS_CLI_VERSION` | exact tested CLI version | pinned; satisfies Bundle/App schema minimum |
| `DATABRICKS_BUNDLE_OWNER` | workspace path owner/principal used for bundle root | non-secret; validated path component |
| `DEPLOYMENT_SOURCE_MECHANISM` | `GIT_SOURCE_COMMIT` or `CI_SNAPSHOT` | exact closed enum; matches bundle target behavior |

MDL-1 must not require any long-lived Databricks secret in the GitHub Environment for the compliant deploy path. If the chosen source mechanism needs a separate private-repository Git credential on the **Databricks App side**, that credential is a platform/source-control configuration concern and must follow the deterministic source-selection rule below; do not confuse it with GitHub-to-Databricks OIDC.

The Databricks federation policy must be scoped as narrowly as the current platform supports to this repository and deployment context/environment. Record a sanitized policy identifier/summary and the service-principal application ID in `docs/platform/github-databricks-oidc.md`; do not store tokens or client secrets. The deployment principal requires `CAN MANAGE` on the target App (or only the minimum create permission for an explicitly approved first creation). It does **not** inherit the App runtime service principal's data permissions.

Where repository settings support deployment protection, configure `staging` so only the intended branch/workflow can request the environment. Human approval for every staging deployment is optional in MDL-1; production approval becomes mandatory in the later release iteration. Art approval is a separate required PR check and cannot be replaced by a deployment-environment approval.

Add:

- `MDL1-OIDC-001` — deploy workflow has `id-token: write` only on the trusted deployment job;
- `MDL1-OIDC-002` — `staging` contains all required non-secret variables and no Databricks PAT/client secret;
- `MDL1-OIDC-003` — `DATABRICKS_HOST` equals the Free Edition attested workspace;
- `MDL1-OIDC-004` — deployment SP identity differs from the App runtime SP and has only required App-management permission;
- `MDL1-OIDC-005` — federation policy/evidence is scoped to the intended GitHub repo/context and recorded without secrets;
- `MDL1-OIDC-006` — an untrusted/fork PR cannot obtain the staging Databricks identity or invoke the deploy job.

Current implementation reference to revalidate at start: `https://docs.databricks.com/aws/en/dev-tools/databricks-apps/cicd-github-actions`.

### GitHub deployment workflow blueprint

Create `.github/workflows/deploy.yml` with a **manual** `workflow_dispatch` entry during MDL-1. It must take the exact `implementation_sha` and the frozen deployment-source mechanism (or read that mechanism from validated version-controlled config); it must not deploy “whatever main is now”. The checked-out source is always exactly `implementation_sha`. The bundle resource shape branches only between the two approved source modes above. Conceptual Git-source structure:

```yaml
name: Deploy MAD DATA LAB staging

on:
  workflow_dispatch:
    inputs:
      implementation_sha:
        description: Exact green MDL implementation commit to deploy
        required: true

permissions:
  contents: read
  id-token: write

concurrency:
  group: mdl-databricks-staging
  cancel-in-progress: false

jobs:
  deploy:
    environment: staging
    runs-on: ubuntu-latest
    timeout-minutes: 30
    env:
      DATABRICKS_AUTH_TYPE: github-oidc
      DATABRICKS_HOST: ${{ vars.DATABRICKS_HOST }}
      DATABRICKS_CLIENT_ID: ${{ vars.DATABRICKS_CLIENT_ID }}
      BUNDLE_VAR_app_name: ${{ vars.DATABRICKS_APP_NAME }}
      BUNDLE_VAR_git_repo_url: ${{ github.server_url }}/${{ github.repository }}
      BUNDLE_VAR_git_commit_sha: ${{ inputs.implementation_sha }}
      BUNDLE_VAR_genie_space_id: ${{ vars.GENIE_SPACE_ID }}
      BUNDLE_VAR_sql_warehouse_id: ${{ vars.SQL_WAREHOUSE_ID }}
      BUNDLE_VAR_staging_workspace_host: ${{ vars.DATABRICKS_HOST }}
      BUNDLE_VAR_deployment_owner: ${{ vars.DATABRICKS_BUNDLE_OWNER }}
    steps:
      - uses: actions/checkout@<PINNED_IMMUTABLE_SHA>
        with:
          ref: ${{ inputs.implementation_sha }}
      - name: Verify requested commit and clean source
        run: scripts/verify_deploy_source.sh '${{ inputs.implementation_sha }}'
      - name: Install pinned Databricks CLI
        uses: databricks/setup-cli@<PINNED_IMMUTABLE_SHA>
        with:
          version: ${{ vars.DATABRICKS_CLI_VERSION }}
      - name: Record/validate Databricks CLI version
        run: uv run python scripts/check_databricks_cli.py --minimum 0.290.0
      - name: Validate bundle
        run: databricks bundle validate --target staging
      - name: Deploy bundle
        run: databricks bundle deploy --target staging
      - name: Start/restart app
        run: databricks bundle run mad_data_lab --target staging
      - name: Verify App deployment identity, RUNNING state, and authenticated API smoke
        run: uv run python scripts/smoke_deployment.py --target staging --expected-commit '${{ inputs.implementation_sha }}'
```

The smoke script follows the current Databricks Apps token-auth pattern conceptually: obtain the short-lived workspace OAuth token from the authenticated Databricks CLI/SDK context, discover the App URL from the Apps API, and send `Authorization: Bearer ...` only to `/api/*` routes. Never echo the token or enable shell tracing around token acquisition.

`BUNDLE_VAR_*` is the documented bundle-variable environment convention. `DATABRICKS_CLI_VERSION` is a non-secret GitHub Environment variable containing the exact tested CLI release; it must be at least the version required by the fields used in `databricks.yml` (commit-based App `git_source` requires the current 0.290-era schema or newer). The literal `<PINNED_IMMUTABLE_SHA>` remains a documentation metavariable and **must be resolved to an immutable action commit before the workflow is committed**; the placeholder-resolution validator must reject it in executable YAML.

`scripts/verify_deploy_source.sh`/Python equivalent must check:

- `git rev-parse HEAD == requested implementation_sha`;
- worktree is clean;
- the SHA belongs to the expected PR/branch history;
- required PR CI and human-art approval gate are green for that implementation SHA (query GitHub API/CLI when credentials permit);
- source-spec fingerprint and iteration manifest are valid.

`scripts/smoke_deployment.py` must poll the App/deployment API, verify `resolved_commit` when Git source is used, wait for RUNNING with a bounded timeout, discover the App URL, obtain/use the Databricks OAuth bearer headers through the CLI/SDK authentication context, call only the supported `/api/*` smoke endpoints, enforce per-request timeouts, redact authorization material from logs, and produce sanitized JSON/JUnit evidence. It must never persist the bearer token in artifacts.

For early iterations, deploy to a `staging` GitHub Environment or equivalent protected target. If Free Edition permits only one practical app target, document that the challenge app is being used as iterative staging and preserve rollback information.

Use `workflow_dispatch` initially. Do not enable automatic production deployment on every push until the workflow has several successful runs.

## `databricks.yml` tasks

MDL-1 locks the GitHub-to-Databricks deployment path on **Declarative Automation Bundles** because this is the current documented Databricks Apps GitHub Actions pattern and the App resource schema supports Git source pinned to a commit. Create `databricks.yml` at repository root with:

```text
bundle name
target staging
reserved target prod configuration (no automatic production deploy in MDL-1)
App resource
explicit workspace host per target through variables
root_path
Git repository source pinned to implementation commit
Genie Agent resource
SQL warehouse resource
```

The Databricks CLI used for this contract must be pinned to a version supporting App `git_source` (`0.290.0` or newer under the currently verified schema). If current official Databricks validation proves that Bundles/App Git source is unavailable or incompatible in the actual Free Edition workspace, stop with `BLOCKED_DATABRICKS_CONFIGURATION`, capture the validation output and request a human/platform decision. Do **not** silently downgrade MDL-1 closure to an ad-hoc manual deployment path. A temporary manual deployment may restore service during investigation, but it cannot satisfy the CI/CD Definition of Done.

### Concrete `databricks.yml` blueprint

Use the current Bundle schema as the implementation reference; run `databricks bundle validate` and adjust only fields that current CLI validation proves have changed. A commit-pinned shape is:

```yaml
bundle:
  name: mad-data-lab

variables:
  app_name:
    description: Existing/new Databricks App name
  git_repo_url:
    description: GitHub repository URL
  git_commit_sha:
    description: Exact accepted implementation commit
  genie_space_id:
    description: Existing Genie Agent/space ID
  sql_warehouse_id:
    description: Existing SQL warehouse ID
  staging_workspace_host:
    description: Attested Free Edition workspace URL
  deployment_owner:
    description: Non-secret workspace principal/user path component owning bundle artifacts

resources:
  apps:
    mad_data_lab:
      name: ${var.app_name}
      description: MAD DATA LAB challenge app
      git_repository:
        provider: gitHub
        url: ${var.git_repo_url}
      git_source:
        commit: ${var.git_commit_sha}
        source_code_path: .
      resources:
        - name: genie-space
          description: MAD DATA LAB Genie Agent
          genie_space:
            space_id: ${var.genie_space_id}
            permission: CAN_RUN
        - name: sql-warehouse
          description: MAD DATA LAB trusted SQL warehouse
          sql_warehouse:
            id: ${var.sql_warehouse_id}
            permission: CAN_USE

targets:
  staging:
    mode: development
    workspace:
      host: ${var.staging_workspace_host}
      root_path: /Workspace/Users/${var.deployment_owner}/.bundle/${bundle.name}/${bundle.target}
```

Implementation notes:

- if current Bundle validation requires workspace host/deployment owner to be expressed differently, adapt through a recorded platform-drift decision;
- environment-specific IDs/host are supplied from GitHub Environment variables/bundle variables, never copied into frontend/business code;
- when `deployment_source_mechanism=GIT_SOURCE_COMMIT`, `git_source.commit` is mandatory; if current CLI is too old, upgrade/pin a validated CLI version rather than silently falling back to mutable `main`; when `CI_SNAPSHOT` is selected, use Bundle `source_code_path` from the clean accepted checkout and remove Git-source-only variables from the active target;
- if the App already exists, bind the bundle to it and record the binding instead of creating a duplicate App;
- if the GitHub repository is private and Git-source deployment would require a new long-lived Git credential that the project cannot safely configure, choose the exact-CI-snapshot deployment strategy rather than adding an unreviewed PAT;
- `app.yaml` remains the runtime command/resource-to-env mapping source; Bundle App resources grant/reference the platform resources.

Add `MDL1-BUNDLE-001` through `MDL1-BUNDLE-006`: bundle validates with current pinned CLI, app resource maps Genie/warehouse with least privilege, commit variable is non-empty/full SHA, unknown target rejected, existing-app binding is explicit, and no environment-specific resource ID is emitted into the frontend bundle.

## Tests required to close MDL-1

### Static and build

Implement at least the equivalent of:

- ST-001 Ruff.
- ST-002 Python type checking.
- ST-003 TypeScript type checking.
- ST-004 ESLint.
- ST-005 lockfile integrity.
- ST-006 Python dependency reproducibility.
- ST-007 secret scan.
- ST-008 forbidden unsafe frontend rendering pattern scan.
- ST-009 forbidden hidden-truth reference scan in production frontend/static assets.
- ST-010 package/asset file-size sanity.

### Domain

Implement at least:

- DU-004 score starts at zero, even if scoring is only a skeleton.
- DU-014 epistemic status enum exact closed set.
- DU-015 experiment enum exact closed set.
- DU-016 instrument enum exact closed set.
- DU-019 legal state transitions.
- DU-020 illegal state transitions.
- DU-021 append-only event behavior.
- DU-022 status monotonicity must NOT be assumed.
- DU-026 zero deviation formatting/helper safety if implemented.

### Catalog

Implement at least:

- CAT-001 catalog schema valid.
- CAT-002 public numbers unique.
- CAT-003 Case IDs unique.
- CAT-004 slugs unique.
- CAT-005 deterministic sort order.
- CAT-006 every released Case has a template placeholder.
- CAT-010 unreleased public payload excludes truth/path oracle.
- PRG-001 Case #042 available for a fresh profile.

### API

Implement at least:

- API-001 health 200.
- API-002 config excludes secrets.
- API-003 session creation for valid Case.
- API-004 invalid Case rejected.
- API-026 catalog only returns public metadata.
- API-027 unreleased Case cannot create production session.
- API-029 Case detail excludes expected path and hidden truth.
- API-032 session Case ID immutable.

### Legacy-prototype rejection tests

Add explicit tests that production source does not contain:

```text
Promo effect?
Pricing change?
Seasonal factor?
WEAKENED
OPEN as an epistemic Case status
hardcoded required experiment count of 3 for CASE_0042
```

The DQ source-table field status `OPEN` may still exist in data later; the repository scan must distinguish data-quality issue lifecycle status from the epistemic status enum.

## Artwork checkpoint — complete MDL-1 production art pipeline, with human approval

MDL-1 establishes the visual source of truth. It must generate **all artwork that the MDL-1 UI legitimately needs** and no fake later-game UI art. The mandatory MDL-1 production asset set is:

```text
MDL1-A01  App icon / laboratory mark              V3 A01
MDL1-A02  Master Dr. Genie portrait               V3 A02
MDL1-A21  Case #042 key art                       V3 §22.21
MDL1-A28  Case Board laboratory hub background    V3 §22.28
```

A03–A20/A22–A27 belong to later screens/Cases and remain deferred unless the owning iteration explicitly pulls one forward. Do not generate unneeded art just to make the repository look complete.

The later locked V3 art direction supersedes the earlier exploratory pixel-art/fantasy-genie images. Production MDL-1 artwork is **premium retro-futurist analytical laboratory + polished lightly stylized 3D illustration**, not the blue magical genie, lamp/smoke-tail motif, or fake board-game UI.

### Global art-direction prefix — prepend to environment/instrument/key-art prompts

Store this text verbatim in `assets/image_prompts.md` and hash the prompt file in the manifest:

```text
Premium retro-futurist data science laboratory, sophisticated enterprise analytics meets playful scientific experimentation, dark navy research environment, luminous cyan data traces, restrained coral energy accents, subtle violet evidence glow, precision instruments, clean geometric forms, cinematic but not photorealistic, polished 3D illustration with lightly stylized proportions, trustworthy and intelligent, high detail in machinery but generous negative space for UI overlays, no readable text, no numbers, no logos, no watermarks, no brand marks, no horror, no dangerous chemical imagery.
```

Character prompts use the same palette/quality direction but must preserve the exact Dr. Genie character bible rather than treating the environment prefix as a replacement for character identity.

### Artwork generation operating procedure

#### Generation is an execution task, not a prompt-writing task

MDL-1 is not compliant if Codex only writes prompts and never obtains candidate images. Phase 2 must end in one of two explicit states:

1. **`GENERATION_IN_PROGRESS` / candidates exist** — the execution environment has an image-generation capability, so Codex/human operator actually generates the minimum candidate set and stores the resulting files/provenance; or
2. **`BLOCKED_HUMAN_ART_GENERATION`** — the execution environment cannot generate images, so Codex creates complete, copy/paste-ready generation request packets and stops short of claiming the art gate. A human/ChatGPT image-generation session then produces the candidate images, which are returned to the branch/review workflow before source selection can occur.

Never substitute web-search images, stock art, the obsolete fantasy-genie images, or an unrelated placeholder merely to make the UI look complete. The generator output itself is review material until a human selects it and the exact production derivative is later approved.

For a human handoff, create one file per asset under:

```text
assets/review/MDL-1/generation-requests/MDL1-A01.md
assets/review/MDL-1/generation-requests/MDL1-A02.md
assets/review/MDL-1/generation-requests/MDL1-A21.md
assets/review/MDL-1/generation-requests/MDL1-A28.md
```

Each request packet must contain: asset ID, V3 source section, locked base prompt, exact candidate-variation suffixes below, target dimensions/aspect/alpha, hard negatives, minimum candidate count, filename convention, and the provenance fields the human must return. These request packets are temporary review artifacts and are not served by the production app.

Create `scripts/build_art_generation_requests.py` so the request packets are generated from the version-controlled prompt/manifest definitions instead of being hand-copied differently by different operators. It must also emit a review-only machine plan:

```text
assets/review/MDL-1/generation-requests/art-generation-plan.json
```

The plan must contain **exactly 18 required candidate slots** at MDL-1 start:

```text
A01: C01-C04  = 4
A02: C01-C06  = 6
A21: C01-C04  = 4
A28: C01-C04  = 4
TOTAL          = 18
```

For each slot, store asset ID, candidate ID, full expanded prompt, prompt SHA-256, target aspect/size requirement, alpha requirement, hard-negative set, status (`NOT_GENERATED`, `GENERATED`, `REJECTED_TECHNICAL`, `VALID_FOR_HUMAN_REVIEW`, `HUMAN_REJECTED`, `SOURCE_SELECTED`) and returned generator/file reference when available. Regeneration creates a new attempt record under the same slot (for example `C02-R2`) rather than erasing the failed attempt.

The script itself does not call a proprietary image API unless the execution environment has an explicitly supported image-generation interface. Its purpose is to make every prompt/slot deterministic and copy/paste/tool-call ready. Actual image generation remains mandatory under the generation-state rules below.

#### Candidate-generation batching and image-tool rules

Each candidate ID represents one independently reviewable **full image**, not one cell in a generated 2×2/3×2 contact sheet. If the generation tool supports `n > 1`, its individual returned images may fill multiple candidate slots only when each image is separately addressable/downloadable and receives its own SHA/provenance record. Never use a single four-up collage as the source asset and crop its quadrants into candidates: that changes composition/resolution and makes provenance/approval ambiguous.

Generation rules:

- generate candidates at the largest practical native aspect/size closest to the requested target; deterministic resize/crop belongs to the production-derivative stage, not candidate comparison;
- do not upscale a visibly low-resolution candidate and call it production-ready; reject/regenerate when the source cannot support the target;
- if the tool exposes a seed, generation ID, model/version, reference-image ID, or edit lineage, record it; if it does not, record `null`, never invent one;
- do not rely on an unrecorded chat/image thread as the only source provenance; export/retain the selected source and record its returned tool/file reference plus SHA;
- A02 candidates must be generated from text only for the first master identity unless an explicitly approved project-created reference exists; later character poses must use the approved/frozen A02 reference where tooling permits;
- no candidate may include user/private data, Databricks screenshots, real financial records, protected logos, or copied UI from another product;
- the candidate prompt sent to the image tool is the **global direction + exact asset base prompt + one candidate suffix + hard negatives**. Save that full expanded prompt, not an abbreviated paraphrase.

If an image-generation API/tool changes behavior mid-iteration, keep already valid candidates but record the tool/model drift. Do not silently mix radically different styles: the human contact sheet must clearly identify which candidate came from which generation configuration.

#### Controlled candidate-variation plan

The minimum candidate count is intentional. Candidates must explore **composition and presentation**, not contradict the locked art direction. Generate each candidate from the asset's exact base prompt plus exactly one variation suffix. Record the full resulting prompt and hash; do not record only the suffix.

**A01 — four candidate suffixes**

```text
C01 — Emphasize a simple symmetric flask silhouette; lineage branches stay internal to the silhouette; strongest readability at 32 px.
C02 — Emphasize the branching data-lineage graph while preserving a single compact flask silhouette; slightly more geometric and technical.
C03 — Emphasize the central analytical spark as the focal point; keep all other detail minimal and app-icon friendly.
C04 — Simplify to the fewest possible clean 3D/vector-like forms while retaining flask + lineage + spark; maximize favicon readability.
```

**A02 — six candidate suffixes**

All six must preserve every locked Dr. Genie trait. Variation is limited to facial design nuance, micro-expression, goggles position/style within the smart-goggle constraint, tablet angle, coat seam detail, and torso pose. Do not vary into different character archetypes.

```text
C01 — Calm confident three-quarter portrait; goggles just above the eyes; tablet held low enough to keep the face dominant.
C02 — More curious expression with one raised eyebrow; slightly forward analytical posture; same wardrobe and age.
C03 — Warm skeptical-capable expression; subtle half-smile; cleaner/minimal coat seam pattern.
C04 — More senior/authoritative presence without sternness; transparent goggles worn over the eyes; same silver-white unruly hair.
C05 — Slightly more theatrical scientific presentation gesture while remaining professional; tablet angled toward an invisible chart.
C06 — Most restrained enterprise portrait; neutral confident pose; prioritize a memorable face/silhouette that later poses can reproduce consistently.
```

**A21 — four candidate suffixes**

```text
C01 — Containment chamber on the right third; broad quiet left/top area for the HTML Case title and metadata.
C02 — Chamber centered but visually compact; the missing-energy gap is the focal metaphor; preserve generous peripheral negative space.
C03 — Four streams approach diagonally from lower left toward the chamber; snapshot reel and microscope are secondary background clues only.
C04 — More architectural lab framing with the chamber in the lower-right quadrant; maximize crop safety for both 16:9 and 4:3 Case-card use.
```

**A28 — four candidate suffixes**

```text
C01 — Symmetric wide hub with case chambers around the perimeter and a large calm central floor/upper-title zone.
C02 — Slight three-quarter perspective; case chambers concentrated along left/right walls; center remains visually quiet for HTML cards.
C03 — Circular lab architecture seen from a slightly elevated camera; strong depth but no foreground machinery obstructing UI.
C04 — Most minimal enterprise version: fewer foreground props, clean architectural rhythm, broad negative-space bands for responsive card placement.
```

If a candidate is technically invalid, regenerate **that candidate slot** using the same suffix plus only the minimum corrective instruction needed. If a human rejects the overall concept, change the prompt version explicitly and regenerate a fresh candidate set; do not mutate rejected files in place.

For each required asset:

1. create the prompt/version record in `assets/image_prompts.md` before generation;
2. create a manifest entry in `assets/art_source_manifest.yaml` with `status: GENERATION_PENDING`;
3. generate the required candidate count below using the exact prompt/negative constraints;
4. save candidates under `assets/review/MDL-1/<asset-id>/` using candidate IDs — **not** production filenames;
5. record generator/tool, model/version if available, generation date, prompt hash, source/reference asset IDs, rights basis, dimensions, format, byte size and SHA-256 for every candidate;
6. run technical preflight on all candidates;
7. automatically generate a neutral contact sheet/index showing candidate ID, dimensions and no evaluative ranking text;
8. present technically valid candidates to the human approver;
9. human selects/rejects; Codex must not select by pretending that its own aesthetic judgment is human approval;
10. create the production derivative from the human-selected candidate (crop, alpha cleanup, WebP/PNG conversion, compression only — no semantic redraw unless regenerated);
11. run preflight on the exact production derivative;
12. present the **exact production bytes in their intended UI context** for final human approval;
13. record the approved production SHA-256 and update the manifest to `APPROVED` only from explicit human evidence;
14. commit the approved asset + manifest + approval record and rerun CI.

If the environment cannot generate images, set `BLOCKED_HUMAN_ART_GENERATION`, provide the exact prompts/candidate requirements below, and continue only engineering tasks that do not require pretending final art exists. MDL-1 cannot close.

### Candidate counts and filenames

Minimum generation set:

| Asset | Minimum candidates | Review emphasis |
|---|---:|---|
| A01 | 4 | silhouette/readability at 32/64 px |
| A02 | 6 | character identity; this becomes the master reference for later poses |
| A21 | 4 | non-spoiler Case #042 hook, crop flexibility |
| A28 | 4 | usable UI negative space and hub composition |

Candidate naming example:

```text
assets/review/MDL-1/MDL1-A02/mdl1-a02-c01.png
assets/review/MDL-1/MDL1-A02/mdl1-a02-c02.png
...
```

`assets/review/` is non-production working/review material. Default policy: do **not** deploy it and do not commit all rejected high-resolution candidates merely for history. Review candidates/contact sheets may be supplied as PR/CI artifacts or other approved review attachments. The manifest must still retain candidate IDs, prompt hash, tool/model, dimensions and SHA-256. If the selected source candidate itself must be retained for future reference editing, store only that selected source in a dedicated non-deployed `assets/source/` location and keep it within repository/file budgets.

Production names are stable and semantic:

```text
assets/production/images/mdl_mark.png
assets/production/images/dr_genie_master.png
assets/production/images/case_0042_key_art.webp
assets/production/images/case_board_lab.webp
```

Do not let generated candidate filenames leak into application code.

### MDL1-A01 — App icon / laboratory mark

Target: `1024 × 1024`; final production derivative is transparent PNG. Must remain recognizable at 32 px. If the generator cannot create usable transparency, a human may approve a cutout workflow, but the final approved production bytes are still transparent.

**Exact generation prompt:**

```text
Create a single iconic emblem for a product called MAD DATA LAB without rendering any words. Combine the silhouette of a scientific flask with a branching data-lineage graph and a small sparkling analytical star at the center. Premium retro-futurist data science aesthetic, symmetric enough to work as an app icon, dark navy and luminous cyan with a restrained warm coral accent, clean vector-like 3D shape, strong silhouette at 32 pixels, no letters, no readable text, no numbers, no logos, no lamp, no fantasy genie, no watermark. Square composition, centered object, ample padding.
```

**Reject automatically before human review if:**

- it contains letters, pseudo-text, numerals, external brand marks or watermark;
- the main silhouette disappears at 32×32;
- it reads primarily as a magic lamp/genie symbol;
- critical shape touches crop edges;
- source dimensions/aspect are wrong and cannot be corrected without damaging composition.

**Human approval questions:**

- Does it read as “data laboratory” rather than generic chemistry or fantasy magic?
- Is the silhouette distinct at 32 and 64 px?
- Does it feel compatible with a premium enterprise analytics app?
- Would you accept this as the long-lived MAD DATA LAB mark?

### MDL1-A02 — Master Dr. Genie portrait

Target: `1536 × 1536`; transparent background required for the final production derivative unless the image generator technically cannot provide usable alpha and a human explicitly approves a clean cutout workflow.

This is a **master reference asset**. Later A03/A04/A05 poses must reference the approved A02 identity/hash. Do not generate later Dr. Genie variants before A02 is approved.

**Exact generation prompt:**

```text
Character design for Dr. Genie, an eccentric but highly credible senior data scientist in a futuristic analytics laboratory. Adult scientist with expressive intelligent face, slightly unruly silver-white hair, modern dark laboratory coat with subtle circuit-like seam details, transparent smart goggles resting above the eyes, small holographic data reflections, curious confident expression, one eyebrow slightly raised, holding a compact transparent tablet with abstract charts but no readable text. Professional, warm, analytical, mildly theatrical, not childish, not manic, not a fantasy genie, no lamp, no magical costume, no resemblance to any existing fictional scientist. Premium stylized 3D illustration, clean rim lighting, dark navy/cyan palette with restrained coral accent. Full torso, three-quarter view, isolated transparent background, no text, no logo, no watermark.
```

**Hard negative/identity constraints:**

```text
NO blue fantasy-genie skin identity
NO lamp
NO smoke-tail lower body
NO turban/magical costume
NO gold earring/goatee trope as the defining genie identity
NO evil/mad-scientist caricature
NO mental-illness caricature
NO copyrighted/scientist-character lookalike
NO readable tablet text
```

**Human approval questions:**

- Is this clearly the locked Dr. Genie: silver/white hair, modern lab coat, smart goggles, credible senior data scientist?
- Is the face warm/curious/skeptical-capable rather than manic, childish or villainous?
- Is the silhouette/costume specific enough to keep later poses consistent?
- Does the character look original rather than derivative of a known fictional scientist?
- Is the crop safe for sidebar/panel use at desktop demo sizes?

After approval, record:

```text
character_reference_id: DR_GENIE_V1
character_reference_sha256: <approved A02 production sha>
character_reference_status: FROZEN
```

Any later semantic edit to A02 invalidates this identity version and all derivative approvals that reference it.

### MDL1-A21 — Case #042 key art: The Missing €6.8M

This asset is mandatory in MDL-1 because Case #042 is the CORE/AVAILABLE featured entry Case on the Case Board; the complete investigation is intentionally deferred to MDL-4. It must hint at the anomaly without revealing that V2 source-record changes are the answer.

Target source: 16:9, at least `1600 × 900`; final derivative optimized for Case-card crops (4:3 and responsive variants must be previewed without losing the central metaphor).

**Generation prompt — global art prefix +:**

```text
A transparent analytical containment chamber holding four glowing metric streams that should converge into one bright total orb, but one stream is visibly depleted and leaves a clean gap in the final energy balance. Nearby, a snapshot reel and a microscope tray suggest record-level investigation. The visual should communicate “missing contribution” without showing currency symbols or numbers. Premium retro-futurist analytical laboratory prop design, sophisticated enterprise-game aesthetic, dark navy environment, luminous cyan data energy, restrained coral anomaly accent, violet evidence light, clean readable silhouette, subtle eccentric humor, no humans unless explicitly requested, no readable text, no letters, no numbers, no logos, no watermark, leave negative space for HTML overlay, 16:9 composition suitable for cropping to a 4:3 card.
```

**Reject if it spoils the Case** by explicitly depicting V2, a changed source record, duplicate keys as the cause, formula unchanged, the exact `6.8`, or any other answer/number in generated pixels.

**Human approval questions:**

- Does it create curiosity about a missing contribution without giving away the explanation?
- Does it remain legible in a Case card crop?
- Is there enough quiet space for HTML title/hook/difficulty/tags?
- Does it look like the same world as A02/A28?

### MDL1-A28 — Case Board laboratory hub background

Target: `2560 × 1440`, 16:9; production WebP normally preferred after source approval/compression.

**Exact generation prompt:**

```text
Wide establishing shot of MAD DATA LAB as a premium retro-futurist analytical laboratory hub. Seven sealed case chambers/dossier stations are arranged around a central circular floor, each with a distinct abstract instrument silhouette but absolutely no text. Exactly one chamber is brightly active. Two chambers have a faint low-intensity standby glow that suggests future investigations/coming soon but must not look currently interactive or available; the remaining chambers are dim/inactive without using padlock icons. Dr. Genie is not present. Large quiet center/top region for the HTML title and filters. Dark navy architecture, cyan analytical glow, restrained coral anomaly accents, violet evidence glow, sophisticated game hub, clean perspective, no readable text, no numbers, no logos, no watermark, 16:9.
```

**MDL-1 stage adaptation:** V3 A28's generic/full-game wording allows two softly available chambers, but MDL-1 has only Case #042 `AVAILABLE`; #107/#213 are `COMING_SOON`. The MDL-1 prompt therefore changes those two chamber lights to non-interactive standby/future cues. This is a presentation adaptation, not a change to the canonical Case release states, and it prevents decorative art from contradicting server availability.

**Additional implementation constraint from the project direction:** the background must be atmospheric rather than a bitmap pretending to be the UI. It must contain **no baked-in buttons, hypothesis cards, inventory, action points, round counters, charts, game values or clickable-looking panels**. The real Case cards and controls are HTML.

**Human approval questions:**

- Does the background leave the central/top and Case-card interaction regions visually quiet?
- Does it avoid the earlier problem where ~30%+ of the screen becomes fixed foreground decoration that competes with the game?
- Can the HTML Case Board occupy the majority of useful viewport area at 1440×900 and 1280×720?
- Does it communicate a laboratory hub without looking like another unimplemented board game?
- Does it avoid making #107/#213 look clickable/available before the HTML server state enables them?

### Required production derivative matrix

Human source selection happens on the generator output; final approval happens on the exact production bytes and must include every derivative that will actually ship. Derivatives are deterministic image-processing outputs only — resize/crop/alpha cleanup/compression — and may not introduce or redraw semantic content.

| Source asset | Required deployed derivative(s) in MDL-1 | Rule |
|---|---|---|
| A01 | `mdl_mark.png` 1024×1024 plus browser/app-icon derivatives required by the implemented HTML/manifest (for example 512, 192 and favicon size) | generate from the same selected A01 source; preserve aspect/alpha; include small-size previews in final approval |
| A02 | `dr_genie_master.png` 1536×1536 transparent master; optional UI-size derivative only if the frontend needs it for performance | master is the identity reference; any UI derivative points back to the same frozen A02 source/hash |
| A21 | `case_0042_key_art.webp` | one high-quality responsive source is preferred; use CSS/object positioning for crops unless a separate crop is proven necessary; any separate crop becomes an approved derivative with its own hash |
| A28 | `case_board_lab.webp` | preserve 16:9 composition; responsive presentation is CSS/layout-driven; do not create a separate fake-UI image |

Generated HTML `<link rel="icon">`/web-app manifest references, if present, must point only to approved A01 derivatives. The build must fail on a missing/unapproved derivative.

### Artwork provenance and rights-record vocabulary

For each selected source, `rights_basis` must be a truthful project provenance category, not a legal conclusion invented by Codex. Allowed MDL-1 values:

```text
PROJECT_GENERATED_AI          generated specifically for MAD DATA LAB from the locked prompt
PROJECT_CREATED_HUMAN         created specifically for MAD DATA LAB by a human contributor
LICENSED_PROJECT_ASSET        only if a human supplies/license-verifies an external asset; not expected for A01/A02/A21/A28
```

Also record `generator_provider_or_creator`, `generator_model_or_method` when known, and `terms_or_license_evidence_ref` when applicable. If the generator/provider/model is unknown, do not fabricate it; block final provenance approval until a human supplies enough information to document the source. For A01/A02/A21/A28, do not use an external copyrighted character, logo, stock asset or artist-style imitation as the source/reference.

### Production derivative rules

- Background/key-art production derivatives: WebP unless PNG alpha is needed; target **<1.5 MB per image** and always < Databricks' per-file limit.
- A01/A02 final derivatives: transparent PNG for deterministic alpha/edge quality. Do not convert them to another format after human approval without invalidating the hash and approval.
- Strip unnecessary metadata/color-profile bloat while preserving correct color appearance.
- Never change composition/character identity during “compression.” A semantic edit requires regeneration/reapproval.
- All functional text, numbers, labels and charts remain HTML/SVG, never baked into the image.

### Asset manifest schema — mandatory

`assets/art_source_manifest.yaml` must contain at least:

```yaml
- asset_id: MDL1-A02
  v3_asset: A02
  prompt_file: assets/image_prompts.md
  prompt_sha256: null
  generator_tool: null
  generator_model: null
  generated_at_utc: null
  rights_basis: null
  candidate_ids: []
  selected_candidate_id: null
  source_path: null
  source_sha256: null
  production_path: null
  production_sha256: null
  width: null
  height: null
  format: null
  size_bytes: null
  alpha_required: true
  preflight_status: PENDING
  human_status: PENDING
  approval_record: docs/approvals/MDL-1-art.md
```

Null/unknown fields remain null; Codex must not fabricate provenance.

### Automated art preflight — mandatory before human review and again after selection

Create `scripts/image_preflight.py` (or equivalent) and tests. It must fail the required CI job when a production asset:

- is missing from the manifest;
- is not decodable;
- has unexpected dimensions/aspect outside an explicitly recorded derivative rule;
- exceeds internal size budget or platform 10 MB limit;
- requires alpha but lacks a valid alpha channel;
- hash differs from manifest/approval;
- is still located only in `assets/review/` while production code references it;
- has a production filename not matching the manifest;
- is the legacy `Mad_Data_Lab.png`, `board.png`, fantasy-genie emoji/art or another unapproved asset referenced by production;
- contains EXIF/source metadata that the project policy says should be stripped;
- lacks a rights/provenance field;
- is approved in Markdown but its current bytes no longer match the approved SHA.

Text/watermark detection cannot be trusted solely to automation; flag suspicious candidates for human review rather than claiming machine proof of “no text.”

### Review contact sheet / integration preview

Create `scripts/build_art_review.py` using the locked Pillow dev dependency (or an equally deterministic implementation already present in the repository). It must read candidate/production paths from the manifest rather than hardcoding filenames. The script creates review-only outputs under `assets/review/MDL-1/rendered/` or a CI artifact directory and never writes back into source candidates.

Required command:

```bash
uv run python scripts/build_art_review.py --iteration MDL-1 --manifest assets/art_source_manifest.yaml
```

Create a deterministic review artifact that shows:

- A01 at native preview + 64 px + 32 px;
- A02 on transparent checkerboard + dark UI panel mock crop;
- A21 in 16:9 source + 4:3 Case-card crop with **real HTML/CSS overlay simulation**, not rasterized fake UI text inside the source asset;
- A28 at full 16:9 + 1440×900 and 1280×720 Case Board integration screenshots.

The review artifact is not a production asset and may live in CI artifacts/review directories.

### Exact review-artifact outputs

`build_art_review.py` must emit a machine index plus deterministic visual review files so the human is always approving identifiable evidence:

```text
assets/review/MDL-1/rendered/art-review-index.json
assets/review/MDL-1/rendered/mdl1-a01-contact.webp
assets/review/MDL-1/rendered/mdl1-a02-contact.webp
assets/review/MDL-1/rendered/mdl1-a21-contact.webp
assets/review/MDL-1/rendered/mdl1-a28-contact.webp
assets/review/MDL-1/rendered/case-board-1440x900.png
assets/review/MDL-1/rendered/case-board-1280x720.png
assets/review/MDL-1/rendered/dr-genie-panel-preview.png
```

The JSON index records candidate IDs, candidate SHA-256 values, prompt hashes, tool/model metadata, preflight result, selected-source status, production derivative hashes when present, and the corresponding review-file paths. Contact sheets may include machine-rendered candidate IDs and technical metadata outside the source image; they may not include subjective rankings such as “best”.

Review rendering itself must be reproducible from current manifest + candidate/production bytes. A stale review artifact whose embedded/input hashes do not match current files is invalid and must be regenerated before asking for approval.

### Human approval protocol — two decisions, no self-approval

Create `docs/approvals/MDL-1-art.md` with one entry per asset. The file must start with **parseable YAML front matter** delimited by `---`; prose/screenshots may follow after the closing delimiter. `scripts/validate_art_approval.py` parses only that front matter for the machine gate. This prevents a vague prose comment from being mistaken for structured approval.

Every human decision must also contain an `evidence_ref` identifying where the human decision came from (for example a GitHub PR review/comment URL, a recorded project-review artifact, or another non-secret immutable reference). Codex may transcribe the decision but may not invent the actor, timestamp, evidence reference, or approval wording. The validator should reject `approved_by: codex`, `approved_by: automation`, or a missing evidence reference.

Create `docs/approvals/MDL-1-art.md` with one entry per asset. Use two statuses:

1. `SOURCE_SELECTED` — human chose a candidate as the basis for the final production derivative;
2. `APPROVED` — human saw the exact final production bytes **and** the integration preview and approved them.

Codex must not set either human decision unless it is transcribing explicit human feedback from the PR/conversation. Aesthetic confidence from Codex is not evidence.

Required front-matter schema (the literal file begins and ends the machine section with `---`):

```yaml
---
iteration: MDL-1
status: PENDING
approved_by: null
approved_at: null
approval_evidence_ref: null
assets:
  - id: MDL1-A01
    source_candidate_id: null
    source_candidate_sha256: null
    production_path: assets/production/images/mdl_mark.png
    production_sha256: null
    source_selection: PENDING        # PENDING | SOURCE_SELECTED | REJECTED
    source_selection_evidence_ref: null
    integration_review: PENDING       # PENDING | APPROVED | REJECTED
    integration_review_evidence_ref: null
    final_decision: PENDING           # PENDING | APPROVED | REJECTED
    final_approval_evidence_ref: null
    human_notes: null
  - id: MDL1-A02
    source_candidate_id: null
    source_candidate_sha256: null
    production_path: assets/production/images/dr_genie_master.png
    production_sha256: null
    source_selection: PENDING        # PENDING | SOURCE_SELECTED | REJECTED
    source_selection_evidence_ref: null
    integration_review: PENDING       # PENDING | APPROVED | REJECTED
    integration_review_evidence_ref: null
    final_decision: PENDING           # PENDING | APPROVED | REJECTED
    final_approval_evidence_ref: null
    human_notes: null
  - id: MDL1-A21
    source_candidate_id: null
    source_candidate_sha256: null
    production_path: assets/production/images/case_0042_key_art.webp
    production_sha256: null
    source_selection: PENDING        # PENDING | SOURCE_SELECTED | REJECTED
    source_selection_evidence_ref: null
    integration_review: PENDING       # PENDING | APPROVED | REJECTED
    integration_review_evidence_ref: null
    final_decision: PENDING           # PENDING | APPROVED | REJECTED
    final_approval_evidence_ref: null
    human_notes: null
  - id: MDL1-A28
    source_candidate_id: null
    source_candidate_sha256: null
    production_path: assets/production/images/case_board_lab.webp
    production_sha256: null
    source_selection: PENDING        # PENDING | SOURCE_SELECTED | REJECTED
    source_selection_evidence_ref: null
    integration_review: PENDING       # PENDING | APPROVED | REJECTED
    integration_review_evidence_ref: null
    final_decision: PENDING           # PENDING | APPROVED | REJECTED
    final_approval_evidence_ref: null
    human_notes: null
---
```

Top-level `status` may become `APPROVED` only when every required asset is final `APPROVED` and current SHA validation passes.

If a human says “approve candidate C02 but crop it differently,” that is **source selection, not final approval**. Produce the derivative, recompute hash, show the integration preview, then ask for final approval of those exact bytes.

### Human decision evidence — GitHub is the preferred source of truth

Because MDL-1 already requires a GitHub PR, the preferred human-approval source is a **GitHub PR review or PR comment by the designated human approver**. The human message must contain the asset ID and the relevant candidate or production SHA using the explicit approval syntax below. `evidence_ref` should be the immutable GitHub review/comment URL or API identifier.

`scripts/validate_art_approval.py` running in GitHub CI should, when repository API access is available with read-only metadata/pull-request permissions (`contents: read`, `pull-requests: read` or the minimum equivalent):

1. resolve each recorded GitHub evidence URL/ID;
2. verify it belongs to the current MDL-1 PR/repository;
3. read the actor/login and timestamp;
4. verify the body expresses the expected `APPROVE SOURCE` or `APPROVE` action for the exact asset/hash;
5. reject evidence created by the automation identity, GitHub Actions bot, Codex bot/service account, or an actor not in the designated human-approver allowlist;
6. compare the actor to `approved_by` and preserve only non-secret metadata in the approval record.

If repository/API restrictions make CI verification of the human comment impossible, the iteration is `BLOCKED_HUMAN_APPROVAL` until a human owner supplies an alternative immutable review artifact and explicitly accepts the weaker verification method in the iteration decision log. A plain Markdown value typed by Codex is never sufficient evidence on its own.

### Human approval request template

Codex should make the approval request explicit enough that a friendly comment such as “nice” is not misread as final approval. Use a message substantially like:

```text
MDL-1 ART REVIEW — <ASSET_ID>
Candidate/source: <candidate-id + sha256>
Final production file: <path>
Final production SHA-256: <sha256>
Integration preview: <artifact/link/path>

Please choose one:
- APPROVE <ASSET_ID> <sha256>
- REJECT <ASSET_ID> — <reason>
- APPROVE SOURCE <ASSET_ID> <candidate-id> but request these derivative changes: <changes>
```

Equivalent unambiguous human language is acceptable. Ambiguous praise, silence, emoji reactions, or Codex's own assessment are not approval. If the human approves a source candidate but asks for crop/compression/background changes, final production approval is still pending until the new bytes are shown with their SHA.

### Human rejection/regeneration loop

If any asset is rejected:

1. record `REJECTED` plus the human reason;
2. do not overwrite or rename the rejected candidate into production;
3. modify only the relevant prompt/reference/crop instruction needed to address the rejection;
4. increment the prompt/candidate version;
5. generate a new candidate set or additional candidates as requested;
6. rerun preflight/contact sheet;
7. request source selection again;
8. after derivative creation, request exact-byte final approval again;
9. rerun `human-approval-gate` on the new hashes.

If A02 is rejected after any downstream pose has somehow been created, discard/review those derivatives because the master identity is not frozen.

### Human approval gate in GitHub CI

Create `scripts/validate_art_approval.py`. The required check `mdl1/human-approval-gate` must fail unless:

- all A01/A02/A21/A28 manifest entries exist;
- all production paths exist;
- current SHA-256 values equal manifest values;
- approval record refers to those same hashes;
- `source_selection == SOURCE_SELECTED`;
- `integration_review == APPROVED`;
- `final_decision == APPROVED` for each asset;
- top-level MDL-1 art status is `APPROVED`;
- approver and approval timestamp are non-null;
- top-level approval evidence and the source-selection, integration-review, and final-approval evidence references for every asset are non-null and point to recorded human evidence;
- the approver identity is not Codex/automation and matches the recorded human evidence actor where that can be validated;
- A02's frozen character reference SHA equals its approved production hash.

The validator checks evidence consistency only; it must not manufacture approval.

### MDL-1 art-specific automated tests

Add at least:

- `MDL1-ART-001` — all four required MDL-1 asset IDs exist exactly once in manifest;
- `MDL1-ART-002` — review candidates are never referenced by production code;
- `MDL1-ART-003` — production assets decode and satisfy size/dimension/alpha contracts;
- `MDL1-ART-004` — production SHA values match manifest and approval file;
- `MDL1-ART-005` — legacy fantasy-genie/fake-board asset paths are absent from production bundle references;
- `MDL1-ART-006` — Case #042 key art exists before the CORE card is marked visually complete;
- `MDL1-ART-007` — A02 character reference ID/hash is frozen after approval;
- `MDL1-ART-008` — any post-approval byte change makes `human-approval-gate` fail;
- `MDL1-ART-009` — all functional Case-card/board text remains DOM/HTML and is not sourced from image files;
- `MDL1-ART-010` — final build contains only approved production asset paths, not rejected candidates/review sheets;
- `MDL1-ART-011` — A21/A28 integration previews exist at required demo viewports before final approval;
- `MDL1-ART-012` — manifest contains non-null generator/provenance/rights basis for final selected sources.
- `MDL1-ART-013` — each required asset has at least the minimum number of technically valid candidate records, or the iteration is explicitly blocked in `BLOCKED_HUMAN_ART_GENERATION`;
- `MDL1-ART-014` — candidate full-prompt hashes correspond to the locked base prompt plus the recorded candidate-variation suffix;
- `MDL1-ART-015` — approval front matter is parseable and every human decision has a non-null human evidence reference;
- `MDL1-ART-016` — no production code or build artifact contains `assets/review/` or generation-request files;
- `MDL1-ART-017` — the generated MDL-1 art plan contains exactly 18 required candidate slots (4 A01, 6 A02, 4 A21, 4 A28) with unique candidate IDs and prompt hashes;
- `MDL1-ART-018` — every valid candidate is an independently addressable full image; no selected source is a crop extracted from a multi-candidate collage;
- `MDL1-ART-019` — regeneration preserves prior attempt provenance rather than overwriting failed/rejected candidate history.

### Deferred art policy

A03–A20 and A22–A27 remain deferred; MDL-1 must not silently generate or ship them as unreviewed extras. Use this ownership map so “all artwork” means all art required by the current iteration, while every other V3 asset has an explicit future gate:

| V3 asset(s) | Content | Primary future owner / activation rule |
|---|---|---|
| A03–A05 | Dr. Genie Eureka / skeptical / thinking poses | MDL-5 visual/instrument implementation, derived from frozen A02 |
| A06 | laboratory entrance background | MDL-5 when the complete guided shell needs it |
| A07 | hypothesis chamber plate | MDL-5 |
| A08–A13 | decomposition, snapshot, microscope, lineage, DQ, conclusion chamber art | MDL-5; only alongside real functional HTML/SVG Instruments |
| A14 | badge set | MDL-5 after MDL-4 locks badge behavior/content |
| A15 | social/article hero | MDL-8 submission package |
| A16 | loading/failure background | MDL-6 resilience/error-state polish |
| A22–A27 | secondary-Case key art | only when the corresponding Case is actually enabled and its automated Case contract is green; otherwise remains ungenerated/unshipped |
| A28 | Case Board hub | **MDL-1 mandatory** |

In particular, locked/coming-soon Cases do **not** need misleading bespoke key art in MDL-1. The shared approved hub background plus controlled CSS/icon treatment may render them. Before any secondary Case becomes release-enabled, its V3 key art becomes a blocking asset with the same exact-byte human approval process.

## Local completion gate

Run all required local checks from a clean checkout or clean environment. The final local command sequence must be recorded in `docs/iterations/MDL-1-report.md` with pass/fail status.

At minimum record:

```text
node version
python version
npm ci result
frontend typecheck result
frontend lint result
frontend unit result
frontend build result
Python install result
Ruff result
Python typecheck result
pytest result
secret scan result
asset preflight result
```

No required check may be marked `not run` without a documented blocker and explicit human acceptance. A blocked required check means the iteration is not complete.

## GitHub CI completion gate

After push:

1. verify PR workflow triggered;
2. verify every required job green;
3. inspect at least one CI log to make sure the intended test command actually ran;
4. verify artifacts/reports are uploaded where configured;
5. fix every CI-only issue in the branch;
6. rerun until fully green;
7. do not merge on a red or missing required check.

Record the PR URL and successful workflow run ID in `MDL-1-report.md`.

## Databricks deployment gate

Deploy the branch to the staging Databricks App through the automated workflow.

Required automated checks after deploy:

- deployment target matches the Free Edition workspace attestation;
- GitHub deployment identity is the expected OIDC service principal;
- App metadata identifies the intended App runtime service principal without exposing its secret;
- Databricks App resource bindings include the expected Genie resource key and, when configured, SQL warehouse resource;
- git deployment source resolves to `implementation_sha` (or the documented content/tree digest equivalent);
- bundle/config validation green;
- app restarted on the new code;
- app reaches `RUNNING`;
- the deploy workflow obtains a short-lived Databricks OAuth access token from the already configured OIDC/CLI identity without printing it;
- the workflow discovers the deployed App URL from `databricks apps get`, not from a hardcoded URL;
- authenticated `GET <APP_URL>/api/health` with `Authorization: Bearer <token>` returns 200;
- authenticated `/api/config` returns the expected safe payload and does not expose secrets;
- authenticated `/api/cases` returns Case #042 and non-playable secondary public metadata;
- API smoke validates `Content-Type`, error handling, bounded request timeouts and no accidental HTML SPA fallback for `/api/*`;
- deployed version/commit SHA is identified through Databricks App deployment metadata (`resolved_commit` when using Git source) or an equally strong source proof;
- sanitized `databricks apps logs` output contains no startup traceback/secret and shows the expected application start event;
- the process can be terminated/restarted without exceeding graceful shutdown expectations.

Do **not** fail MDL-1 merely because a CI Bearer token cannot be used to fetch the user-facing `/` route: current Databricks documentation defines token authentication for App API routes. Root/static serving is already validated by `mdl1/production-package-smoke`; the deployed UI root is opened during the permitted human deployment inspection (or by a later explicitly authenticated browser harness). If current platform behavior offers a supported automated UI-auth path, it may be added, but it is not a substitute for the API token smoke.

## Staging rollback and failed-deployment recovery contract

A failed MDL-1 deployment must not leave the shared challenge app unusable, and a successful rollback must not be misreported as a successful validation of the failed implementation.

### Pre-deploy capture

Immediately before changing the staging App, capture a sanitized last-known-good snapshot to `release-report/MDL-1/pre-deploy.json` (or CI artifact) containing when available:

```text
target environment/app identifier (non-secret)
current app state
current deployment ID
current resolved Git commit/source identity
current bundle target/resource name
current public health status
capture timestamp UTC
CI run ID initiating the change
```

If no prior successful deployment exists, record `last_known_good: null`; never invent a rollback source.

### Failure handling

If bundle validation, deployment, app start, source-identity verification, smoke, or graceful-restart validation fails:

1. mark the iteration/deployment `FAILED`/`BLOCKED`; do not continue to manual acceptance;
2. collect sanitized deployment status, app logs, smoke output and exact failing implementation SHA;
3. determine whether the App is unhealthy or whether only the validation assertion failed;
4. if the shared staging/challenge App is unhealthy and a verified last-known-good source exists, restore that exact source through the same controlled deployment mechanism;
5. run the minimal health/root/static smoke against the restored source;
6. record `rollback_performed`, rollback source identity, rollback deployment/run ID and result;
7. fix the failed branch implementation, invalidate stale CI/deployment evidence, and redeploy the new accepted `implementation_sha` from the beginning of the deployment gate.

Rollback is an **operational recovery**, not a release gate pass. MDL-1 remains incomplete until the current MDL-1 implementation itself deploys and passes every required smoke/provenance gate.

### Rollback prohibitions

- no “rollback to previous” command without first resolving the exact known-good commit/content identity;
- no rollback to fixture/offline demo mode as a substitute for the intended deployment;
- no destructive deletion/recreation of workspace data/resources just to restore the app unless an explicit human/platform owner approves that recovery action;
- no force push/rewrite of the `MDL-1` branch to hide the failed deployment;
- no deletion of failure logs/evidence from the iteration report.

Add:

- `MDL1-RB-001` — pre-deploy snapshot is captured before a deployment mutation when a current deployment exists;
- `MDL1-RB-002` — rollback script/workflow requires an explicit known-good source identity and rejects null/ambiguous “previous” input;
- `MDL1-RB-003` — a rolled-back staging app does not mark the failed `implementation_sha` as deployed/green;
- `MDL1-RB-004` — post-rollback smoke proves the restored app is usable;
- `MDL1-RB-005` — iteration report preserves both failed deployment and rollback evidence.

## Manual deployment inspection - allowed and required

After all automated deployment checks pass, a human performs a short subjective/runtime inspection only:

- open the Databricks App URL;
- confirm MAD DATA LAB branding is visible;
- confirm Case #042 appears available;
- confirm other Cases do not appear accidentally playable;
- inspect browser console for obvious errors;
- inspect application logs for startup exceptions;
- confirm approved MDL-1 art is visually acceptable at the intended UI size;
- verify no secrets/debug stack traces are visible.

Do not use this manual pass to discover numerical or state-machine correctness. If a functional bug is seen, first add an automated regression test, then fix it.

## Merge gate

Only after:

- local checks green;
- the PR head is refreshed against current `origin/main` and the final branch-freshness gate is green;
- GitHub CI green on that refreshed accepted head;
- art human-approved and current hashes still match after any branch refresh;
- staging deploy green for the accepted implementation identity;
- manual deployment inspection accepted;

merge `MDL-1` into `main` through the PR.

Then:

1. verify `main` CI is green;
2. verify the merged commit/PR relationship is the one expected;
3. recompute the runtime-content digest on merged `main` and require equality with the accepted `implementation_runtime_digest`; a squash/rebase/merge SHA difference is acceptable only when this content proof is green;
4. if deployment is main-driven, confirm the post-merge deployment is green and represents the same accepted runtime content;
5. capture the merge commit SHA, merged tree SHA, runtime digest and CI/deployment evidence in immutable GitHub/CI metadata (PR comment, workflow summary/artifact, release metadata) and in the MDL-2 predecessor-verification record. Do **not** create a new commit solely to insert a commit SHA into the report that would then become stale again.

## Required iteration report

Create `docs/iterations/MDL-1-report.md` containing:

```text
Iteration objective
Branch name
Base commit
Final branch commit
PR URL
Main merge commit: external metadata reference only; do not self-reference inside the commit that creates the report
Merged tree SHA / evidence reference
Local test summary
GitHub CI run IDs
Databricks deployment ID / app version if available
Automated smoke summary
Art asset IDs and approval record link
Known limitations intentionally deferred to MDL-2+
Rollback reference
Decision log entries for any spec-preserving implementation substitution
```

Never include credentials, tokens, or hidden truth.


## Deployment source, provenance, and environment-isolation contract

This iteration must make it impossible to deploy the wrong branch, the wrong tree, or a stale generated build while still obtaining a green deployment result.

### Staging source strategy — deterministic selection rule

MDL-1 uses Declarative Automation Bundles in all cases, but the **App source mode** is selected by this security-first rule during the Entry/Platform gate and then frozen in `docs/architecture/deployment-source.md` for the iteration:

1. **Use `GIT_SOURCE_COMMIT`** when the GitHub repository is public **or** the Databricks App service principal already has (or a human administrator deliberately provisions) a secure Git credential that can read the private repository without exposing that credential to browser/runtime code. Set `git_source.commit = implementation_sha` and prove `resolved_commit == implementation_sha`.
2. **Use `CI_SNAPSHOT`** when the repository is private and Git-source deployment would require introducing an unreviewed/undesired long-lived Git credential merely for the challenge. The GitHub OIDC deploy job checks out the exact `implementation_sha`, proves a clean tree, and the Bundle App resource uses workspace/source upload (`source_code_path`) from that checkout. The deploy package gets the deterministic source/build metadata/content digest described below.

There is no third “whichever is convenient” path. Record `deployment_source_mechanism: GIT_SOURCE_COMMIT | CI_SNAPSHOT` in the iteration manifest before the first deployment. Changing modes later invalidates bundle/workflow/security/provenance/deployment evidence and requires an ADR/update to this record.

Do not configure a staging deployment that implicitly reads mutable `main` while the CI job is validating an `MDL-*` branch. A PR deployment is valid only when the deployed build identity resolves to the accepted PR implementation SHA/tree.

For final production, `main` may become the deployment source after merge, but the source strategy must remain explicit and auditable. Record the strategy in `docs/architecture/deployment-source.md` and include:

```text
staging source mechanism
production source mechanism
Git ref/commit resolution rule
build location: CI vs Databricks runtime
where dependency installation occurs
how static frontend output is produced
how build metadata is embedded
how rollback source is selected
how the deployed app reports its accepted source identity
```

### Environment isolation

Create a minimal environment matrix and keep environment-dependent identifiers outside business logic:

```text
local        fixture/fake services; no production resources
staging      Free Edition challenge workspace/resources used for iteration validation
production   final accepted challenge app configuration
```

If staging and production must share one physical Free Edition app because of platform limits, emulate isolation with explicit deployment targets/configuration and record that limitation. At minimum:

- production/offline feature flags cannot be inherited accidentally from local fixture mode;
- staging test sessions cannot mutate production progression/configuration unexpectedly;
- environment name appears in safe build metadata and logs;
- secrets/resource identifiers come from runtime/resource binding, not checked-in source;
- deploy workflow requires an explicit target and rejects an unknown target;
- rollback never selects a local/fixture artifact.

### Deterministic deployment/build identity — mechanism-specific

Do **not** invent one build-info mechanism that only works for one deployment source. The identity proof must follow the actual Databricks source mode.

#### Strategy A — Databricks Git-source deployment

When the App resource uses `git_repository` + `git_source`:

- set `git_source.commit` to `implementation_sha` whenever the installed Bundle/App schema supports commit-pinned deployment;
- otherwise deploy the branch/ref and require the Apps deployment metadata `resolved_commit` to equal `implementation_sha`;
- treat Databricks Apps API/deployment metadata as the authoritative source proof;
- if the bundle/app config can inject a non-secret `APP_GIT_SHA`/`APP_BUILD_SHA`, set it from the same commit variable and expose it through a safe `/api/build-info` endpoint, then assert it equals `resolved_commit`;
- **do not** generate an uncommitted CI-only `build-info.json` and claim the Git-source deployment contains it.

Safe `/api/build-info` fields may include:

```text
app_name
app_version
environment_target
app_git_sha / build_sha when injected
build_timestamp only when it is actually part of the deployed artifact/runtime config
```

Never return workspace credentials, client secret, PAT, private resource metadata, or hidden truth.

#### Strategy B — CI/workspace snapshot upload

When CI packages/uploads the exact checked-out source tree rather than asking Databricks to pull Git directly, generate `build/build-info.json` into the **staged deploy package** before upload. It must be generated from observed Git/CI state and included in the package content digest. Example:

```json
{
  "app": "MAD_DATA_LAB",
  "version": "...",
  "git_commit": "...",
  "git_tree": "...",
  "branch_or_ref": "...",
  "ci_run_id": "...",
  "build_timestamp_utc": "...",
  "environment_target": "staging",
  "dirty": false
}
```

The package builder must fail if `dirty=true`, Git identity is missing, or the build-info source differs from the checked-out CI commit.

#### Common identity requirements

Regardless of strategy:

- record `implementation_sha`, Git tree SHA, GitHub run ID, deployment ID and deployment-source mechanism;
- prove the deployed source resolves to the accepted implementation identity;
- no report-only commit may silently become the deployed implementation unless it changes a runtime-affecting path and all invalidated gates are rerun;
- rollback must identify a previously successful deployment/source identity, not merely “previous version”;
- environment target is explicit and unknown targets fail closed.

### Deployment provenance tests — iteration-specific

Add non-canonical MDL-1 tests in addition to the V3 §44 ledger:

- `MDL1-DEP-001` — deploy workflow rejects an unknown target;
- `MDL1-DEP-002` — PR/staging deployment source resolves to the exact PR head/tree;
- `MDL1-DEP-003` — selected deployment strategy produces valid identity evidence: Git-source `resolved_commit` or snapshot package build-info/content digest;
- `MDL1-DEP-004` — deployed identity evidence resolves exactly to the CI-accepted `implementation_sha`/tree under the selected strategy;
- `MDL1-DEP-005` — production configuration cannot enable offline demo through a missing/default environment value;
- `MDL1-DEP-006` — rollback reference resolves to an actually successful prior deployment/source identity;
- `MDL1-DEP-007` — environment-specific resource identifiers are not embedded in frontend production assets.
- `MDL1-DEP-008` — deployed API smoke uses a short-lived OAuth bearer token, discovers the App URL dynamically, never logs/persists the token, and does not treat an unauthenticated UI-root fetch as the API health proof.
- `MDL1-DEP-009` — report-only and merged-main runtime digests equal the accepted implementation runtime digest; unknown-path classification fails closed.

These tests are iteration-specific closure tests and do not replace any canonical V3 §44 test ID.


## Hardening addendum — auditability, traceability, and closure semantics

This section is normative. It exists to prevent a false-positive iteration closure where implementation appears complete but cannot be independently reproduced or mapped back to the definitive V3 specification.

### Canonical traceability ledger

Maintain `docs/traceability/v3-test-coverage.csv` from MDL-1 onward. It is a release artifact, not optional documentation. Required columns:

```text
test_id
title
source_section
owner_iteration
release_applicability
implementation_path
ci_check_name
last_result
last_run_id
evidence_path
notes
```

Canonical-count normalization: V3 §44 spells most IDs individually but expresses the visual range as `VR-001 through VR-012`. The ledger expands that range into twelve concrete rows (`VR-001` … `VR-012`). Under that normalization, the definitive catalog contains **422 canonical test-ID rows**. The validator must use the source parser/range expansion rather than a hand-maintained count so this number cannot drift silently.

Rules:

1. Every stable test ID from V3 §44 must appear exactly once as an **owner**. Rerun references in later iterations do not create a second owner.
2. `release_applicability` is one of `MANDATORY`, `CONDITIONAL_CASE`, or `RERUN_ONLY`.
3. `CONDITIONAL_CASE` is allowed only for a Case whose server-owned release state is not enabled in the challenge build. It is not a waiver. The moment that Case becomes enabled, its conditional tests become blocking.
4. No row may disappear because the implementation was simplified. If a V3 requirement is intentionally superseded by a higher-precedence challenge/platform rule, record an ADR and keep the row with the disposition and rationale.
5. A CI validator must fail when there is an unknown test ID, duplicate owner, missing owner, invalid applicability, missing implementation path for a mandatory implemented test, or a mandatory test whose latest result is not green.
6. Test code should carry the canonical ID in the test name, marker, docstring, metadata, or generated JUnit property so CI reports are traceable without reading prose.
7. The traceability ledger itself must be reviewed in every iteration because moving code between layers can change the correct implementation path or CI job without changing the product requirement.

### Iteration evidence manifest

Create or update `release-report/MDL-1/manifest.json`. The final manifest must be generated by automation after the last content-changing commit rather than hand-edited to claim success.

Minimum schema:

```json
{
  "iteration": "MDL-1",
  "branch": "MDL-1",
  "base_commit_sha": "...",
  "base_tree_sha": "...",
  "accepted_head_commit_sha": "...",
  "accepted_head_tree_sha": "...",
  "implementation_runtime_digest": "...",
  "pull_request_number": 0,
  "required_ci_checks": [],
  "github_workflow_run_ids": [],
  "test_report_sha256": {},
  "deployment_source_mechanism": "GIT_SOURCE_COMMIT | CI_SNAPSHOT",
  "build_artifact_sha256": null,
  "databricks_deployment": {
    "app_name": "...",
    "deployment_or_run_id": "...",
    "resolved_commit": null,
    "snapshot_content_sha256": null,
    "reported_build_sha": null,
    "post_deploy_smoke": "PASS"
  },
  "data_schema_version": "...",
  "genie_config_sha256": "...",
  "asset_sha256": {},
  "human_art_approval_files": [],
  "open_blockers": []
}
```

Use `null` for fields that genuinely do not apply to the selected deployment mechanism; do not invent values. For `GIT_SOURCE_COMMIT`, `resolved_commit` is mandatory and must equal `accepted_head_commit_sha`; `snapshot_content_sha256`/CI-only build-artifact fields may be null. For `CI_SNAPSHOT`, the staged package/content digest is mandatory and must map to the accepted source tree. `open_blockers` must be empty to close the iteration.

The manifest must never contain credentials, OAuth material, PATs, raw hidden-truth payloads, authorization headers, private user identifiers, or unredacted sensitive logs.

### Release-contract validators

MDL-1 must create reusable validators used by every later iteration:

```text
schemas/iteration-manifest.schema.json
scripts/validate_iteration_manifest.py
scripts/validate_traceability.py
scripts/validate_human_approvals.py
```

`validate_iteration_manifest.py` must validate schema/types, required fields, `open_blockers == []`, SHA/hash syntax, iteration/branch consistency, and presence of required evidence references. It must not treat placeholder strings such as `...`, `TBD`, `<run-id>`, or `UNKNOWN` as valid closure values for required fields.

`validate_traceability.py` must validate both `v3-test-coverage.csv` and `v3-section-coverage.csv`, including the 422 canonical §44 test IDs and sections 1–54.

Use the stable required CI check `mdl1/release-contract` to run these validators. The check may permit an iteration manifest to be `IN_PROGRESS` during development, but the merge/closure invocation must require `status=COMPLETE`, zero open blockers, exact human approvals, and no unresolved required evidence.

### Exact deployed-content proof

A successful deployment is not enough, but the proof must match the selected Databricks source mechanism:

- **Git-source commit deployment:** Databricks Apps deployment metadata is authoritative. The post-deploy gate must read `resolved_commit` and require exact equality with `implementation_sha`. The app may expose a safe application version and an injected `APP_GIT_SHA` if that value is genuinely supplied by the deployed configuration, but it must not claim a Git tree/build artifact that Databricks itself rebuilt and that the app cannot independently observe.
- **CI/workspace snapshot deployment:** the staged package must contain deterministic build/source metadata generated from the clean accepted checkout, and the deployment evidence must bind the App's snapshotted source path/content digest to that package.

Do not infer provenance from deployment time, branch name, a report commit, or a CI-only file that was never part of the deployed source. `validate_iteration_manifest.py` must enforce the mechanism-specific required fields.

### Change-invalidation matrix

After any change made after a gate has passed, rerun the affected gates. Minimum invalidation rules:

| Change | Gates invalidated |
|---|---|
| Python/backend/domain code | lint/type/unit/API/contracts + relevant E2E + build + deployment smoke |
| Frontend/TypeScript/CSS | type/lint/component + relevant E2E + visual/a11y when present + build + deployment smoke |
| SQL/schema/seed/generator | data/property/golden + SQL integration + Genie eval when Genie consumes it + deployed smoke |
| Genie instructions/config/protocol/example SQL | protocol/client tests + security prompts + live Genie evaluation + deployed live smoke |
| Case template/catalog | catalog/isolation/golden or case-specific tests + relevant E2E |
| CI/workflow/dependency lock | clean-install + complete affected CI jobs; previous green runs do not certify the new workflow |
| Artwork bytes or compression | image preflight + visual regression where used + human approval hash refresh + build/deploy smoke |
| Audio bytes or encoding | audio preflight + audio E2E/a11y + human approval where required + build/deploy smoke |
| Scoring/verdict/progression | domain + API + fake-Genie E2E + release regression suite |
| Documentation only | docs/link/schema checks; if documentation is executable/config-like, run its owning technical gate too |

When uncertain, rerun the broader gate. Do not choose the narrower gate merely to save time.

### Codex completion response contract

At the end of this iteration Codex must report facts, not intentions. The completion response must include:

- branch name and clean-working-tree confirmation;
- PR number/link (**required at closure; nullable only while the report is `IN_PROGRESS`**);
- accepted head commit SHA and tree SHA;
- exact local commands run and their exit status;
- required GitHub check names and final states;
- workflow/run IDs (**required for every closure-relevant GitHub workflow; nullable only before those workflows have run**);
- deployment/run identifier and safe deployed build identity;
- automated deployed smoke result;
- traceability validator result;
- artwork candidate paths, production asset hash(es), and human approval file/status;
- known limitations or blockers;
- paths to `release-report/MDL-1/` evidence.

Codex must not write “passed”, “deployed”, “approved”, “green”, or “complete” when it could not independently observe that state. Use `NOT_RUN`, `BLOCKED`, `UNKNOWN`, or `AWAITING_HUMAN_APPROVAL` instead.

### Artwork execution failure rule

If the Codex execution environment cannot create the required artwork through an approved image-generation workflow, it must:

1. preserve the exact production prompt and technical requirements in the repository;
2. create/update the asset manifest entry with status `AWAITING_GENERATION`;
3. stop before iteration closure;
4. request human/tool-assisted generation;
5. never substitute emoji, stock art, placeholder gradients, unrelated generated images, or the legacy fantasy-genie/board artwork;
6. never self-approve a candidate.

The iteration can continue to engineering tests while art is pending, but it cannot be merged/closed until the final production bytes have passed preflight and the human approval record matches their SHA-256.

### Machine-enforced human approval gate

From MDL-1 onward, use a repository validator such as:

```bash
python scripts/validate_human_approvals.py --iteration MDL-1
```

The validator must fail unless:

- every artwork/audio asset required by MDL-1 exists in the production asset manifest;
- each required production file hashes to the SHA-256 recorded in its approval record;
- approval status is exactly `APPROVED`;
- `approved_by` and `approved_at` are present and were supplied as the result of an explicit human decision;
- no required asset is still `PENDING`, `REJECTED`, `AWAITING_GENERATION`, or missing;
- a replaced/recompressed asset has obtained fresh approval for its new bytes.

The required GitHub merge check is `mdl1/human-approval-gate`. It is expected to remain red while approval is pending. Do not bypass or mark it optional merely to keep the PR visually green during development. A human approval in chat/PR review is not enough by itself until its exact asset hash has been recorded in the repository approval file; conversely, Codex must not write `APPROVED` without an explicit human decision.



### V3 section-level requirements traceability

In addition to the canonical test ledger, maintain `docs/traceability/v3-section-coverage.csv` with one row for each V3 top-level section `1..54` and these columns:

```text
section_number
section_title
primary_iteration
secondary_iterations
status
evidence_or_implementation_path
notes
```

Rules:

- every section 1–54 has **exactly one primary closure iteration**; earlier bootstrap work or later revalidation is recorded under `secondary_iterations`, not as a second primary owner;
- `status` progresses through `PLANNED`, `IMPLEMENTED`, `VERIFIED`, or `CONDITIONAL_NOT_SHIPPED` as appropriate;
- a product/manual/submission section cannot be marked `VERIFIED` merely because code tests are green; provide the corresponding UX/document/submission evidence;
- a section superseded by current platform/challenge rules remains in the ledger with an ADR reference rather than being deleted;
- CI must validate that sections 1 through 54 are present exactly once as primary owners.

Primary V3 sections whose closure belongs to MDL-1:

| V3 section | Title | Required result |
|---:|---|---|
| §1 | Executive Decision | Lock product name/tagline/demo Case and remove conflicting prototype vocabulary. |
| §2 | Source-of-Truth Hierarchy and Consolidation Decisions | Encode precedence, consolidation decisions, ADR and drift rules. |
| §4 | Product Vision and One-Sentence Pitch | Lock canonical product statement for implementation and later public reuse. |
| §5 | Target Audience | Represent intended users in product/copy constraints. |
| §6 | Learning Objectives | Represent and validate learning-objective IDs in Case metadata. |
| §7 | Product and Game Design Pillars | Translate pillars into architectural guardrails. |
| §8 | Non-Goals | Enforce scope boundaries. |
| §9 | World, Theme, and Narrative | Establish lab/Case universe. |
| §10 | Dr. Genie Character Bible | Approve master character source of truth. |
| §24 | Technical Architecture | Establish final trust/layer architecture. |
| §25 | Repository and Component Architecture | Establish repository/component layout. |
| §26 | Runtime and Configuration | Close baseline runtime/resource/config conventions. |

Sections not listed above may still be touched or rerun in MDL-1; that does not transfer their primary closure ownership.

### Definitive V3 source fingerprint and amendment protocol

The implementation must be traceable to the exact definitive source used to write these iteration contracts. At planning time the uploaded V3 source is:

```text
document: MAD DATA LAB — Complete Game Specification, Build Plan, Automated Test Plan, Asset Production Guide, and Game Manual
status: Definitive build specification
version: 3.0
date: 2026-08-23
sha256: 237570e5d62cee11e78ecced43c8449f62f53e7b547e9fe1bfbf4ed54eb0cc44
```

During MDL-1, place the canonical source in a stable repository documentation path such as `docs/specs/MAD_DATA_LAB_V3.md` **without silently rewriting it**, and create `docs/traceability/source-baseline.json` containing its version/date/SHA-256 plus the eight iteration-spec file hashes. If the source is already present under a different canonical path, record that path instead of duplicating it.

Rules:

- the source hash is checked by `mdl1/release-contract`/traceability CI;
- later iterations verify the same source baseline before starting;
- do not “correct” or reconcile source requirements by editing the definitive source invisibly; use a human-approved ADR/addendum that identifies the exact affected V3 section(s), conflict, precedence reason, approval, and resulting test/traceability changes;
- if the human intentionally replaces/amends the definitive source, increment/identify the addendum or new source version, recompute the baseline, mark affected section/test rows stale, and rerun their owner/dependent gates;
- platform/challenge drift is recorded separately through the platform-verification gate because current official platform rules have higher precedence than the older source when they materially conflict;
- the original source remains available for audit even when an addendum supersedes one of its requirements.

Add iteration-specific checks:

- `MDL1-SOURCE-001` — repository canonical V3 source hash equals the accepted planning baseline or an explicitly human-approved replacement/addendum chain;
- `MDL1-SOURCE-002` — all 54 section rows reference the accepted source version/addendum disposition;
- `MDL1-SOURCE-003` — source-baseline file cannot be regenerated as PASS while an unapproved source change is present;
- `MDL1-SOURCE-004` — the eight iteration contract files are fingerprinted so Codex can prove which handoff version it executed.

### Platform-drift verification gate

The definitive V3 hierarchy gives current challenge/platform rules precedence over older implementation assumptions. Therefore, at both **iteration start** and **iteration closure**, create/update `docs/iterations/MDL-1-platform-verification.md` with:

```text
verified_at_utc
verified_by
challenge_rules_url
apps_environment_url
apps_cicd_url
genie_conversation_api_url
agent_mode_api_url
facts_checked
material_drift_detected
adr_or_change_reference
```

Official sources to re-check:

- challenge: `https://community.databricks.com/t5/learning-events/databricks-community-contest-genie-powered-app-challenge/ec-p/165825`
- Apps runtime: `https://docs.databricks.com/aws/en/dev-tools/databricks-apps/system-env`
- Apps GitHub CI/CD: `https://docs.databricks.com/aws/en/dev-tools/databricks-apps/cicd-github-actions`
- Genie Conversation API: `https://docs.databricks.com/aws/en/genie-agents/conversation-api`
- Agent mode API status: `https://docs.databricks.com/aws/en/genie-agents/api`

Facts externally re-verified on 2026-08-24 and expected to remain true unless the official pages change:

- the challenge is a Databricks **Free Edition** App challenge and requires a **Genie Agent at its core**;
- judging remains 20 points for Genie at the Core, 10 for track execution, 10 for app experience;
- the challenge page currently lists the close as **August 31, 2026, 11:30 PM PDT**;
- the Apps runtime currently provides Python 3.11 and Node.js 22.16, exposes `DATABRICKS_APP_PORT`, and maps the FastAPI/Uvicorn port variables to it;
- Databricks' current GitHub Actions guidance uses workload identity federation/OIDC, `databricks bundle validate`, `databricks bundle deploy`, then **`databricks bundle run`**, followed by polling until the app reaches `RUNNING`;
- the Genie Conversation API is the stable stateful application path; Agent mode APIs are currently Beta and require preview enablement, so Agent mode must remain non-blocking/feature-flagged unless its status and workspace availability are explicitly re-verified.

If an official page changes materially, do not silently preserve this file's older assumption. Record an ADR, update the affected iteration requirements, rerun invalidated tests, and follow the higher-precedence current platform rule.

### Placeholder-resolution rule

Angle-bracket values such as `<app-resource>`, `<run-id>`, `<target>`, or `<existing-app-name>` are **metavariables**, never literal commands. Before executing a documented command, resolve them from version-controlled configuration or observed tool output. Record the resolved non-sensitive value in the iteration report when useful. If the value cannot be determined safely, mark the step `BLOCKED`; do not guess identifiers.

### V3 §44 exact test ownership ledger for MDL-1

This is the self-contained **primary ownership** view for the definitive V3 §44 catalog. The repository `docs/traceability/v3-test-coverage.csv` must contain the same ownership at individual-ID granularity. Primary ownership remains unique across the eight iterations. MDL-1 is allowed—and in several cases required—to implement/run a future-owned canonical test early, but that does not move its final closure owner.

| Canonical ID | Applicability | Source-spec requirement |
|---|---|---|
| `API-001` | MANDATORY | health returns 200 |
| `API-002` | MANDATORY | config excludes secrets |
| `CAT-001` | MANDATORY | catalog schema valid |
| `CAT-002` | MANDATORY | public numbers unique |
| `CAT-003` | MANDATORY | Case IDs unique |
| `CAT-004` | MANDATORY | slugs unique |
| `CAT-005` | MANDATORY | sort order deterministic |
| `CAT-006` | MANDATORY | every released Case has a template |
| `CAT-010` | MANDATORY | unreleased Case public payload excludes truth/path oracle |
| `DU-014` | MANDATORY | epistemic status enum closed set |
| `DU-019` | MANDATORY | legal state transitions |
| `DU-020` | MANDATORY | illegal state transitions |
| `PRG-001` | MANDATORY | Case #042 available for a fresh profile |
| `ST-001` | MANDATORY | Python formatting/lint |
| `ST-002` | MANDATORY | Python type checking |
| `ST-003` | MANDATORY | TypeScript type checking |
| `ST-004` | MANDATORY | ESLint |
| `ST-005` | MANDATORY | lockfile integrity |
| `ST-006` | MANDATORY | Python dependency lock integrity |
| `ST-007` | MANDATORY | secret scan |
| `ST-008` | MANDATORY | forbidden frontend patterns |
| `ST-009` | MANDATORY | forbidden hidden-truth reference in production frontend/static assets |
| `ST-010` | MANDATORY | asset/file size scan |

### Canonical tests implemented early in MDL-1 but primarily owned later

These tests are still mandatory for **MDL-1's local/PR gate** because the foundation exposes the corresponding behavior. They remain primarily owned by the later iteration that completes the feature family, preserving single ownership in the eight-file traceability ledger:

| Canonical ID | MDL-1 obligation | Primary closure owner |
|---|---|---|
| `API-003` | implement/run valid skeleton session creation | MDL-4 |
| `API-004` | implement/run invalid Case rejection | MDL-4 |
| `API-026` | implement/run public catalog privacy assertion | MDL-4 |
| `API-027` | implement/run unreleased Case session rejection | MDL-4 |
| `API-029` | implement/run Case detail truth/path privacy assertion | MDL-4 |
| `API-032` | implement/run session Case immutability assertion | MDL-4 |
| `DU-004` | score skeleton initializes to zero; later scoring semantics remain MDL-4 | MDL-4 |
| `DU-015` | global Experiment enum exists/closed; MDL-3 completes orchestration semantics | MDL-3 |
| `DU-016` | global Instrument enum exists/closed; MDL-3/5 consume it | MDL-3 |
| `DU-021` | event history append-only foundation | MDL-4 |
| `DU-022` | domain does not encode false monotonic-status assumption | MDL-4 |
| `DU-026` | zero-deviation helper safety exists before data generator expansion | MDL-2 |

The traceability validator must support an `implemented_from`/`early_regression_iteration` field (or equivalent) separately from `primary_owner`. It must reject duplicate primary owners while allowing these intentional early regressions.

### MDL-1 additional closure requirements

### MDL-1 documentation/operability tests

Add iteration-specific tests/validators:

- `MDL1-DOC-001` — every required documentation file exists and internal relative links resolve;
- `MDL1-DOC-002` — README names the canonical package managers/commands and contains no stale old-tree run instructions;
- `MDL1-DOC-003` — `.env.example` contains no secret-like values and no production offline-demo enablement;
- `MDL1-DOC-004` — PR template contains the required iteration/CI/deploy/art-approval evidence fields;
- `MDL1-DOC-005` — documented repository tree/entrypoints match files that actually exist;
- `MDL1-DOC-006` — staging deploy/rollback runbooks refer to the selected bundle/app source strategy and not to obsolete manual commands.

#### CI required-check contract

Define stable required check names and document them in `docs/ci/required-checks.md`. Names may adapt to the existing repository, but the categories must remain explicit: repository guard, backend static/type, frontend static/type, unit/contracts, production build, and deployment smoke when deployment is invoked. Later iterations extend this set instead of replacing it.

Mandatory CI jobs must not use `continue-on-error: true`. Path filters must not permit a change to executable configuration, dependency locks, assets, prompts, SQL, or test infrastructure to skip the check that owns that surface. If matrix jobs are used, the required status must represent the whole required matrix rather than a single shard.

Pin third-party GitHub Actions to immutable commit SHAs, use least-privilege workflow `permissions`, and do not make pull-request code able to exfiltrate deployment credentials. Any unavoidable pinning exception is a blocking, explicitly owned security debt and may not remain open at MDL-7. Deployment jobs must use protected GitHub Environment controls or equivalent where supported.

#### Traceability validator bootstrap

Create `scripts/validate_traceability.py` and a CI check that proves all canonical V3 §44 IDs have exactly one ownership disposition. Seed the entire ledger now, including conditional future-Case rows, even though many implementation paths will initially be `PENDING_MDL_N`.

MDL-1 is not complete if the validator only checks the subset implemented in MDL-1.

#### Architectural-debt ledger

Create `docs/iterations/technical-debt.md` with columns `id`, `introduced_in`, `reason`, `risk`, `must_close_by`, `owner`, and `status`. Temporary shims introduced during the repo migration must have a closure iteration no later than MDL-6 unless the definitive spec explicitly permits them in production.

## Codex kickoff checklist — the first working session

Once the entry gate passes, Codex should start with this exact sequence rather than choosing its own order:

1. read the full V3 source and this MDL-1 contract; verify both hashes;
2. capture current `main` baseline and current scaffold test/build failures;
3. create/inspect `MDL-1`, create `MDL-1-report.md` and `MDL-1-entry.md`, commit the report skeleton;
4. create/update `docs/platform/databricks-apps-verified.md` from current official docs;
5. seed `v3-test-coverage.csv`, `v3-section-coverage.csv`, locked decisions and technical-debt ledger;
6. start A01/A02/A21/A28 candidate generation/provenance in parallel, leaving human status pending;
7. lock dependency managers (`npm` + `package-lock`, `uv` + `uv.lock`) and prove clean installs;
8. establish root build → `backend/static` → FastAPI single-process package path;
9. migrate backend/frontend into the canonical tree with tests after each responsibility move;
10. implement domain enums/models/catalog/state machine/API skeleton and server authority;
11. remove production legacy hypotheses/statuses/art/fake board and stale build authority;
12. implement CI check topology + branch protection/admin evidence;
13. implement Databricks bundle/app config/OIDC deployment workflow and exact-commit provenance;
14. finish selected artwork derivatives, integration previews and human approval loop;
15. run the complete local gate, push final runtime head, run required GitHub CI, designate `implementation_sha`;
16. deploy the exact implementation identity, run automated smoke and permitted manual deployment/art integration inspection;
17. finalize report/evidence without creating a self-referential SHA loop;
18. merge through protected PR; verify post-merge `main` CI/deploy obligations;
19. mark MDL-1 `COMPLETE` only when every Definition-of-Done item and validator is green.

If Codex cannot execute one of these steps, it should stop at the corresponding blocker and return the exact human/admin/platform action required. It should not improvise a weaker substitute.

## Definition of Done - MDL-1

All boxes must be true:

- [ ] Branch `MDL-1` created from current clean `main`.
- [ ] Repository migrated to the target modular architecture or an explicitly documented equivalent.
- [ ] Node dependency strategy is locked to npm + `package-lock.json`; production build dependencies are available in Databricks deployment semantics.
- [ ] Python dependency strategy is locked to `pyproject.toml` + `uv.lock`; no shadowing production `requirements.txt` exists.
- [ ] Clean Node install works from lockfile.
- [ ] Clean Python/uv install works reproducibly.
- [ ] TypeScript frontend baseline exists.
- [ ] Canonical Case / Investigation / Experiment vocabulary is implemented.
- [ ] Canonical epistemic statuses are exactly `CONFIRMED`, `SUPPORTED`, `POSSIBLE`, `RULED_OUT`.
- [ ] Legacy retail hypotheses are absent from production source.
- [ ] Case #042 is `release_state=CORE` and server `availability=AVAILABLE`; all secondary Cases are `COMING_SOON` in MDL-1 and cannot create sessions.
- [ ] Secondary Cases are server-controlled and not accidentally playable.
- [ ] Server-authoritative state machine exists and rejects illegal transitions.
- [ ] Public payloads exclude hidden truth.
- [ ] Structured request logging exists.
- [ ] One-process Vite-build + FastAPI-serve production package is proven from a clean build.
- [ ] Runtime port logic supports `DATABRICKS_APP_PORT` and refuses local-port fallback in production.
- [ ] Graceful SIGTERM shutdown stays inside the Databricks platform window.
- [ ] Platform boundary uses official `GENIE_SPACE_ID` and one normalized internal Genie setting.
- [ ] Stable required GitHub PR checks exist with the exact eight-name MDL-1 contract (`mdl1/repository-contract`, `mdl1/frontend`, `mdl1/backend`, `mdl1/security-static`, `mdl1/art-preflight`, `mdl1/human-approval-gate`, `mdl1/production-package-smoke`, `mdl1/release-contract`) and are green on the accepted head.
- [ ] GitHub deployment workflow exists and can deploy/restart/poll the app.
- [ ] Free Edition workspace attestation is `true` and matches the deployment target.
- [ ] GitHub OIDC deployment identity and Databricks App runtime identity are distinct/least-privilege and documented.
- [ ] GitHub `staging` Environment contains the complete validated non-secret variable set; federation policy is scoped to the intended repository/deployment context and no long-lived Databricks credential is used by the compliant deploy path.
- [ ] Final `implementation_sha` was refreshed/proven current against `origin/main`; any refresh invalidated and reran stale gates.
- [ ] Databricks staging deployment is green and `resolved_commit`/runtime digest matches `implementation_sha`.
- [ ] Automated deployed smoke is green.
- [ ] MDL-1 artwork generation plan contains all 18 required candidate slots, and every slot has generated/reviewed evidence or an explicit unresolved blocker (which prevents closure).
- [ ] MDL1-A01 app icon is generated and preflighted.
- [ ] MDL1-A02 master Dr. Genie is generated, preflighted, human-selected, integrated, and its identity hash is frozen.
- [ ] MDL1-A21 Case #042 key art is generated, preflighted, human-selected, and integrated without answer leakage.
- [ ] MDL1-A28 Case Board laboratory hub background is generated, preflighted, human-selected, and integrated without fake UI.
- [ ] Human explicitly approved the exact final bytes and integration previews for A01/A02/A21/A28; current SHA-256 values match the approval record.
- [ ] Human source/final approval evidence resolves to the designated human reviewer (preferably GitHub PR review/comment) and is machine-verified where API access permits.
- [ ] Candidate generation produced independent full-image candidates according to the locked counts/suffixes; no collage-cropping shortcut or untraceable image source was used.
- [ ] `mdl1/human-approval-gate` is green because of valid human evidence, not bypassed.
- [ ] Branch pushed to GitHub.
- [ ] PR merged only after green gates.
- [ ] `main` CI is green after merge.
- [ ] Iteration report is complete.

If any checkbox is false, MDL-1 is not closed and MDL-2 must not start.