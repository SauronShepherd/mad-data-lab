# Combined Audit Note

This file consolidates two independent repository-vs-specification audits of the same MAD DATA LAB project state.

- **Primary audit:** the original `MAD_DATA_LAB_spec_gap_audit.md`.
- **Additional audit:** the subsequently supplied `MAD_DATA_LAB_gap_analysis.md`.
- Where the audits overlap, the second audit should be read as corroborating and, in several places, sharpening the first audit with additional repository/process evidence.
- No finding from either source has been removed merely because it overlaps another finding.
- In case of different wording, the stricter conclusion should be used until the repository is re-audited after remediation.

## Combined highest-priority conclusions

The two audits converge on the following release-blocking conclusions:

1. **Private Case #042 truth is exposed in a file under `data/fixtures/public/`**, while the guard test checks the wrong object and therefore passes despite the leak.
2. **The repository's green/PASS evidence cannot currently be trusted as specification closure evidence.** There is no GitHub Actions CI/CD, and the additional audit identifies `scripts/release_gate.py` behavior that can reuse prior PASS JSON instead of re-running live gates unless explicitly enabled.
3. **MDL-1 is not closed.** The repository still exhibits the exact prototype characteristics MDL-1 was meant to replace: plain JSX, monolithic `server/`, `"latest"` dependencies, root `requirements.txt`, missing canonical architecture/traceability, legacy experiments/hypotheses, and missing artwork approval pipeline.
4. **MDL-2 is not closed.** Although several Case #042 golden numbers and some new data-generation artifacts are correct, the deterministic generator/mutation/data/SQL/deployment contract is incomplete, contradictory in places, and not connected to a proven runtime path.
5. **The shipped frontend hardcodes Case #042 analytical content and verdict behavior and can fall back locally when live calls fail**, undermining the required Genie-at-the-Core execution model.
6. **The existing automated tests are green against the wrong model.** They validate the legacy three-experiment scaffold and do not prove the canonical V3/MDL-1/MDL-2 contracts.
7. **The required browser-based test tier and canonical traceability system are absent**: no TypeScript/Vitest/Testing Library/Playwright stack, no complete canonical test-ID ledger, and no reproducible exact-head CI proof.
8. **Git/process closure requirements are unmet**, including incorrect/missing iteration branches, missing PR/entry/predecessor evidence, and uncommitted MDL-2 work according to the additional audit's repository snapshot.
9. **Databricks data deployment and SQL proof are not specification-complete.** The additional audit identifies incomplete/contradictory DDL/views, a stub MDL-2 SQL client, missing migration/rollback/permission tooling, and a superseded demonstrative formula hash in one setup script.
10. **Artwork/media closure is absent for MDL-1 and MDL-2**, while legacy artwork is still being treated as release-required by an existing check.

**Combined disposition: NO-GO for claiming MDL-1 complete, MDL-2 complete, or overall V3 release compliance.**

---

# MAD DATA LAB — Specification Compliance, Implementation Gap, and Test Coverage Audit

**Audit date:** 2026-08-24  
**Audited archive:** `mad-data-lab(1).zip`  
**Definitive product source:** `MAD_DATA_LAB_Complete_Game_Specification_and_Manual(2).md`, V3.0, 2026-08-23  
**Iteration contracts audited in detail:** `MDL-1_FOUNDATION_CANONICAL_DOMAIN_AND_CI_READY_TO_IMPLEMENT(1).md`, `MDL-2_CASE042_DATA_EVIDENCE_GENERATOR_AND_SQL_READY_TO_IMPLEMENT(1).md`  
**Audit objective:** identify requirements that are **missing**, **partially implemented**, **implemented incorrectly**, **implemented but not tested**, or **claimed/tested in a way that does not prove the specification**.

---

## 1. Executive verdict

### Overall status: **NO-GO / NOT SPECIFICATION-COMPLIANT**

The archive is not a V3-compliant MAD DATA LAB implementation and cannot legitimately be treated as MDL-1 or MDL-2 complete.

The most important point is that the repository is capable of producing a green local release report while materially violating the supplied specifications. The local Python suite passes **45 tests**, and `release-report/summary.md` claims all 12 local gates plus live/deployed gates pass, but several tests and gates certify the **legacy three-experiment prototype** rather than the locked V3 contracts. The current green status is therefore not valid release evidence.

The project contains useful prototype work, especially around Case #042 aggregate values, basic API/session handling, a Genie SDK adapter, an early deterministic data generator, and an audio asset. However, the architecture, runtime wiring, test traceability, truth isolation, Genie orchestration, frontend state, assets, CI/CD evidence, and MDL-2 data deployment path are still far from the required contracts.

### Immediate stop-the-line failures

1. **Private truth is committed inside a file under `data/fixtures/public/`.** `case_0042.bundle.json` begins with a `private` object containing `primary_cause`, `primary_component`, and other truth metadata. This directly violates V3 D-006 and MDL-2 truth isolation.
2. **The production experience can progress without Genie/backend authority.** Frontend error handlers advance the experiment index locally and the verdict screen can be opened with hardcoded conclusion copy even when no server session exists. This fails the “Genie at the Core” gut-check and the no-hidden-analytical-fallback rule.
3. **Case #042 is still the old `EXP-01` / `EXP-02` / `EXP-03` prototype** with legacy hypotheses such as “Promo effect?”, “Data bug?”, and “Pricing change?”. It omits required Case #042 experiments including DQ materiality, formula validation, and reconciliation.
4. **The MDL-2 canonical data package is not the runtime data source.** The server uses `server.domain.generate_case`, while a second generator exists under `data/generation`, and the live SQL script uses an older static `sda_dev.mad_data_lab` dataset. There is no single source of truth.
5. **No GitHub Actions workflow is present.** MDL-1 requires exact-head CI, required check topology, deployment, protected-branch evidence, runtime digest provenance, and post-merge verification.
6. **MDL-1 closure evidence is absent.** No `MDL-1-entry.md`, `MDL-1-report.md`, challenge/platform verification, exact-byte art approvals, runtime digest scripts, or required GitHub check evidence exists. MDL-2’s own report correctly says its predecessor is not provable.
7. **MDL-2 closure evidence is explicitly incomplete.** The checked-in MDL-2 report says `status: IN_PROGRESS`, `sql_integration_status: NOT_RUN`, `deployment_status: NOT_RUN`, and `art_status: GENERATION_PENDING`.
8. **Release evidence can be stale.** `scripts/release_gate.py` reuses an existing `PASS` live report when `RUN_LIVE_GATES != 1`, with no binding to the current Git SHA, runtime digest, data hash, Genie instruction hash, or deployment source.
9. **Artwork fails the locked art/character contract.** The two PNGs bake readable UI/text/numbers into generated-looking artwork and depict Dr. Genie as a blue fantasy genie. Required A01/A02/A21/A28 and A08–A12 provenance/approval records are absent.
10. **Secondary Cases are not implemented under D-011 but can become available in review mode.** They lack deterministic full fixtures, private truth contracts, golden SQL oracles, fake-Genie paths, browser E2E, live benchmarks, visual/a11y coverage, and case-specific release reports.

---

## 2. Audit scope and method

### 2.1 What was inspected

The archive was unpacked and the full repository tree was reviewed. The original ZIP contains **166 files**. The audit covered:

- Python backend/runtime code;
- React/Vite frontend code and checked-in production build;
- Case catalog/domain/generator/mutation code;
- Genie adapter/protocol logic and Genie resource JSON;
- trusted and legacy SQL;
- test files and custom release gates;
- release-report artifacts and iteration reports;
- app/runtime/dependency configuration;
- production images and audio;
- repository hygiene and expected CI/CD files.

### 2.2 Executed checks

- `python -m pytest -q` → **45 passed**.
- Static source and repository inventory.
- Inspection of all Python test sources.
- Inspection of generated release-report artifacts.
- Search for canonical V3/MDL requirement and test IDs in repository source/docs.
- Image inspection of both PNG assets.
- Audio technical inspection with FFmpeg/ffprobe.
- Attempted clean `npm ci`; the command did not complete in this sandbox before timeout, so a clean Node install/build is classified **NOT INDEPENDENTLY PROVEN**, not as a project failure caused by that timeout.

### 2.3 Test traceability result

V3 §44 contains **412 unique named test IDs** across the canonical catalog when all defined prefixes are counted. The repository contains **zero** of those IDs in source/test/CI traceability. Likewise, none of the sampled explicit `MDL1-*` or `MDL2-*` contract IDs appears in repository traceability.

This does not mean every required behavior is absent; it means the project has no machine-auditable mapping showing which canonical requirement a test closes, and current tests demonstrably validate behavior that contradicts V3.

### 2.4 Status legend

| Status | Meaning |
|---|---|
| **FAIL** | implementation directly contradicts a locked requirement |
| **MISSING** | required implementation/artifact is absent |
| **PARTIAL** | some relevant implementation exists, but required behavior is incomplete |
| **WRONG TEST** | a test exists but asserts behavior that contradicts the specification |
| **UNTESTED** | implementation exists but no meaningful automated coverage proves the contract |
| **NOT PROVEN** | may exist externally, but supplied archive contains no valid source-bound evidence |
| **DEFERRED** | V3 requires it, but MDL-1/MDL-2 explicitly assign it to a later iteration; still absent from the current ZIP |
| **PASS / PARTIAL PASS** | requirement is substantially present, with limitations noted |

---

# 3. Critical cross-cutting findings

## P0-001 — Public Case #042 bundle contains private truth — **FAIL**

**Spec:** V3 D-006; MDL-2 R2-001/R2-007; MDL-2 requires `CASE_TRUTH` to be absent from browser/public/curated outputs and says the canonical public bundle excludes private truth.

**Repository evidence:** `data/fixtures/public/case_0042.bundle.json` has a top-level `private` object with:

```text
primary_cause: SOURCE_RECORD_CHANGE
primary_component: V2
secondary_cause: DUPLICATE_BUSINESS_KEY
truth_json: private
```

`data/generation/generator.py` explicitly builds:

```python
canonical = {'public': public, 'source_records': rows, 'private': private}
```

and hashes that combined object.

**Why current tests miss it:** `tests/test_mdl2_data.py::test_truth_is_not_in_public_projection` checks only `c.public`, not `c.canonical` and not the committed file under `fixtures/public`. `scripts/security_gate.py` does not scan this public fixture path deeply enough to catch the leak.

**Required correction:** public canonical bundle contains public evidence only; private oracle is separate; add static/package tests that inspect every browser/public fixture and built bundle for truth markers.

---

## P0-002 — Genie can be removed and the main investigation still progresses — **FAIL**

**Spec:** V3 §§3,7,11,24,36; MDL-1 D-003/D-009 and `MDL1-ARCH-004/007`. Genie must form hypotheses, choose Experiments, and drive analytical transitions. Frontend cannot contain an analytical fallback that makes the production game playable without Genie/backend authority.

**Repository evidence:** `src/main.jsx`:

- ships a full `CASES` fallback containing #042 values;
- ships a full `EXPERIMENTS` fallback containing answer evidence and hypothesis updates;
- when experiment API calls fail, increments `exp` locally and continues;
- when no session exists, `revealVerdict()` still switches to the verdict screen;
- the verdict text hardcodes `V2 source-record change is the primary explanation.`

`server/main.py` also silently swallows live Genie exceptions and returns fixture experiments.

**Impact:** the challenge’s “Genie at the Core” requirement is not structurally demonstrated. The current product is a scripted visualization with optional Genie involvement.

---

## P0-003 — Case #042 canonical investigation contract is replaced by a legacy 3-step prototype — **FAIL / WRONG TEST**

**Spec:** Case #042 requires at minimum component decomposition, snapshot diff, DQ/formula validation, and reconciliation; the canonical hypothesis families are H1 Source values changed, H2 Formula changed, H3 Data quality issue.

**Repository:** `server/case_data.py` and `src/main.jsx` use:

```text
EXP-01 Deviation Decomposer
EXP-02 Snapshot Reactor
EXP-03 Evidence Microscope
```

with legacy hypotheses:

```text
Promo effect?
Data bug?
Pricing change?
Seasonal factor?
```

**Tests deliberately certify the wrong behavior:** `tests/test_case_contract.py` expects the exact sequence `['EXP-01', 'EXP-02', 'EXP-03']` and expects the live allowlist for Case #042 to be those IDs.

**Missing:** DQ materiality Experiment, formula validation Experiment, reconciliation Experiment, H1/H2/H3 identity and priority model, final evidence reconciliation before verdict.

---

## P0-004 — Three competing analytical data implementations; no single source of truth — **FAIL**

The project contains at least three incompatible Case #042 analytical paths:

1. `server/domain.py` — runtime fixture generator, floats, generator version 2, used by `/evidence`.
2. `data/generation/generator.py` — MDL-2-style Decimal/string generator, generator version 1, not wired into runtime.
3. `sql/case_0042_setup.sql` + `resources/genie/case_0042.space.json` — legacy static Databricks dataset used by live SQL/Genie checks.

The MDL-2 trusted SQL repository under `sql/trusted/` is not the actual runtime query path. This violates MDL-2’s “one deterministic source-of-truth data package” objective.

---

## P0-005 — Local release report can certify stale live/deployment success — **FAIL**

`scripts/release_gate.py` reuses an existing `PASS` `genie-eval.json`, `deployed-smoke.json`, or `deployed-soak.json` if `RUN_LIVE_GATES != 1`. It does not verify:

- current commit SHA/tree;
- runtime digest;
- data-contract digest;
- canonical Case hash;
- Genie instruction/prompt hash;
- deployment resolved commit;
- app version/source identity.

As a result, a prior PASS survives later code/data changes.

The current `release-report/summary.md` says live Genie/deployed gates PASS while `docs/iterations/MDL-2-report.md` says SQL integration and deployment were not run. These artifacts cannot simultaneously be valid closure evidence.

---

## P0-006 — No GitHub CI/CD implementation or exact-head provenance — **MISSING**

No `.github/workflows` exists in the archive. Missing MDL-1 requirements include:

- required check topology;
- PR/latest-head proof;
- branch protection/ruleset evidence;
- GitHub OIDC Databricks deployment workflow;
- exact commit deployment;
- post-deploy smoke tied to implementation SHA/runtime digest;
- post-merge `main` validation;
- change classifier and runtime digest tooling.

A local `release_gate.py` is not a substitute for GitHub CI/CD.

---

## P0-007 — MDL-1 is not provably closed, so MDL-2 should not have started — **MISSING / NOT PROVEN**

Required MDL-1 closure files/evidence are absent, including:

```text
docs/iterations/MDL-1-entry.md
docs/iterations/MDL-1-report.md
docs/challenge/verified-rules.md
docs/platform/databricks-apps-verified.md
docs/architecture/locked-decisions.md or equivalent traceability
scripts/classify_change.py
scripts/compute_runtime_digest.py
GitHub required-check evidence
Databricks deployment identity/evidence
A01/A02/A21/A28 exact-byte human approvals
```

MDL-2 itself records `predecessor_record: NOT_PROVABLE_IN_LOCAL_REPOSITORY`.

---

## P0-008 — Required art approvals/provenance absent and existing art violates the visual contract — **FAIL / MISSING**

The ZIP contains only:

```text
public/assets/Mad_Data_Lab.png
public/assets/board.png
public/audio/mad_data_lab_curiosity.mp3
```

No asset manifest, prompt provenance, candidate slots, contact sheets, production derivative hashes, rights basis, or human exact-byte approvals are present.

The images themselves violate locked rules:

- readable UI/text/numbers are baked into the art;
- the “board” is effectively a generated full UI screenshot, which the specs prohibit for decorative artwork;
- legacy hypotheses appear in the art;
- Dr. Genie is represented as a blue fantasy genie/smoke identity, explicitly prohibited by MDL-1 A02.

Required MDL-2 A08–A12 analytical instrument candidates are absent.

---

## P0-009 — Secondary Cases can be enabled without their mandatory analytical contracts — **FAIL**

`case_availability()` makes `COMING_SOON`, `TARGET`, `FULL_GAME`, and `STRETCH` cases `AVAILABLE` when `CHALLENGE_REVIEW_MODE=1`.

But secondary Cases do not satisfy D-011. They lack, per Case:

- full deterministic template/package;
- isolated private truth;
- exact reconciliation invariants;
- golden SQL oracle;
- fake-Genie fixture path;
- true browser E2E completion path;
- live Genie benchmark coverage;
- visual/accessibility coverage;
- case-specific release report.

The “planned experiments” for several Cases are generic strings such as “Deterministic fixture evidence is available for this experiment.” This is scaffolding, not an implemented analytical contract.

---

## P0-010 — Deployed SQL/Genie verification targets the legacy schema, not the MDL-2 model — **FAIL / NOT PROVEN**

`scripts/live_sql_check.py` hardcodes:

```text
catalog = sda_dev
schema = mad_data_lab
```

and queries old objects such as:

```text
case_observations
v_case042_experiment_decomposition
v_case042_snapshot_diff
v_case042_formula_check
dq_signals
```

MDL-2 requires configured three-level public/private/curated schemas, Q1–Q8 trusted query implementations, typed result contracts, permission tests, truth-denial checks, and a real seed/migration/rollback process. Current live SQL evidence therefore does not prove MDL-2.

---

# 4. MDL-1 compliance audit

## 4.1 Repository, dependencies, and build architecture

| ID | Requirement | Status | Repository evidence / gap |
|---|---|---|---|
| M1-01 | React + **TypeScript** + Vite frontend | **FAIL** | `src/main.jsx` and `src/api.js`; no TS baseline or `tsconfig.json`. |
| M1-02 | Python managed with `pyproject.toml` + `uv.lock`; no production `requirements.txt` shadow | **FAIL** | `requirements.txt` is the production dependency source; `pyproject.toml`/`uv.lock` missing. |
| M1-03 | Reproducible Node dependencies; no `latest` | **FAIL** | `package.json` sets React, ReactDOM, Vite and plugin to `latest`. |
| M1-04 | Clean frontend build into canonical backend static path | **FAIL** | checked-in `dist/` is served directly; no `backend/static` architecture. |
| M1-05 | `dist/` not authoritative/checked-in stale build | **FAIL** | archive contains committed `dist/`. |
| M1-06 | Canonical modular `backend/` and `frontend/` responsibility structure | **FAIL** | runtime remains concentrated in `server/`; frontend is monolithic `src/main.jsx`. A small `backend/data` folder exists but is not runtime-authoritative. |
| M1-07 | No caches/personal IDE state in repository | **FAIL** | ZIP contains `.idea/` and multiple committed `__pycache__/*.pyc`. |
| M1-08 | Python runtime compatible with locked Databricks Python 3.11 target | **FAIL** | Dockerfile uses `python:3.13-slim`. |
| M1-09 | Vite/browser API uses same-origin `/api` and dev proxy | **FAIL** | `src/api.js` hardcodes `http://localhost:8000` in dev; backend adds localhost CORS. |
| M1-10 | Build/test tooling: Ruff, mypy, Vitest/Testing Library, Playwright | **PARTIAL / MISSING** | local gate runs mypy only on `server`; “lint” is `compileall`; no Vitest/Testing Library/Playwright. |
| M1-11 | Generated OpenAPI TypeScript types | **MISSING** | no generated API type pipeline. |
| M1-12 | Root build package compatible with Databricks deployment semantics | **PARTIAL** | root package/build exists, but build output/dependency/runtime contracts do not match MDL-1. |

### Build evidence problem

The archive contains a built `dist/`, so the server can appear deployable without proving a clean frontend build. MDL-1 explicitly required a clean lockfile build and a startup/package smoke that does not rely on stale checked-in output.

---

## 4.2 Runtime and configuration

| ID | Requirement | Status | Gap |
|---|---|---|---|
| M1-13 | Central typed settings (`pydantic-settings`) | **MISSING** | env access is scattered via `os.getenv`. |
| M1-14 | `DATABRICKS_APP_PORT` support | **FAIL** | launcher reads only `UVICORN_PORT`, defaulting to 8000. |
| M1-15 | Production must reject accidental local port fallback | **FAIL** | unconditional `8000` fallback. |
| M1-16 | Stable env contract incl. APP_ENV, default Case, offline/demo flags, warehouse | **MISSING / PARTIAL** | `app.yaml` provides only `GENIE_SPACE_ID`; no warehouse/config flags. |
| M1-17 | Production offline fixture mode disabled | **FAIL** | fixture is automatic whenever Genie is absent/fails; frontend continues locally. |
| M1-18 | Graceful shutdown bounded to platform window | **UNTESTED / NOT PROVEN** | no required production-package SIGTERM smoke. |
| M1-19 | Databricks bundle/deployment config | **MISSING** | `databricks.yml` absent. |
| M1-20 | Deployment/runtime service-principal separation and permission evidence | **NOT PROVEN** | no source-bound permission/identity evidence. |

---

## 4.3 Canonical domain language and product foundation

| ID | Requirement | Status | Gap |
|---|---|---|---|
| M1-21 | Canonical Case / Investigation / Experiment / Evidence / Verdict vocabulary | **PARTIAL / FAIL** | some naming exists, but production Case #042 is driven by legacy `EXP-01..03`; old semantics remain. |
| M1-22 | Centralized canonical brand/tagline/subtitle copy | **MISSING / INCORRECT** | UI line is “Turn suspicious numbers into explainable experiments.” rather than approved “unexpected numbers…”; no single copy registry. |
| M1-23 | 12 learning objectives in registry | **MISSING** | no canonical objective registry. |
| M1-24 | Dr. Genie character metadata/version | **MISSING** | no canonical character registry/reference hash. |
| M1-25 | No fantasy Genie identity | **FAIL** | frontend uses `🧞‍♂️`; art uses blue fantasy-genie imagery. |
| M1-26 | Canonical active-play lines / dialogue constraints | **PARTIAL / INCORRECT** | canonical lines largely absent; UI introduces unrelated “data detective” copy. |
| M1-27 | Case #042 public hook/copy aligned with canonical | **INCORRECT** | hook is “A trusted metric is €6.8M below expectation.” rather than locked “€6.8M vanished from Capital Available.” |
| M1-28 | Legacy hypotheses absent | **FAIL** | legacy retail hypotheses exist in frontend, backend fixtures, tests, and artwork. |

---

## 4.4 Case catalog and multi-Case architecture

| ID | Requirement | Status | Gap |
|---|---|---|---|
| M1-29 | Case catalog server-controlled and data/config-driven | **PARTIAL** | server controls availability, but catalog is hardcoded Python rather than validated YAML/config. |
| M1-30 | Case #042 `CORE`; secondary Cases non-playable until contracts pass | **PARTIAL / FAIL** | normal mode locks them, but review mode enables all FULL_GAME/STRETCH cases without D-011 contracts. |
| M1-31 | #107 difficulty LEVEL_1 | **FAIL** | server/frontend declare LEVEL 2. |
| M1-32 | #107/#213 preserve TARGET release-state semantics | **FAIL** | represented as `COMING_SOON`; distinction is lost. |
| M1-33 | Generic control paths do not hardcode `CASE_0042` | **FAIL** | scoring, hints, verdict, frontend defaults/fallbacks and several control paths special-case #042. |
| M1-34 | Enabling secondary Case fails closed if 12 artifacts/gates absent | **FAIL** | review mode bypasses this. |
| M1-35 | Progression cosmetic, never authorization | **PARTIAL** | server controls session availability, but local/server progression sources are inconsistent and no forged-progression authorization tests map to spec IDs. |

---

## 4.5 State machine and server authority

| ID | Requirement | Status | Gap |
|---|---|---|---|
| M1-36 | Canonical shell states | **FAIL** | server has only BRIEFING, INVESTIGATION, EXPERIMENT_RESULT, VERDICT, DEBRIEF, ERROR. Missing CASE_CATALOG, CASE_BRIEFING, STARTING_INVESTIGATION, HYPOTHESES_READY, PLAYER_PREDICTION, SELECTING_EXPERIMENT, RUNNING_EXPERIMENT, EVIDENCE_EXPLORATION, PLAYER_PREDICTION_FINAL, CONCLUDING, recoverable waiting/fallback states, etc. |
| M1-37 | Client cannot advance analytical state optimistically | **FAIL** | frontend increments experiment index on API failure. |
| M1-38 | Case switching creates isolated session/evidence | **PARTIAL** | sessions carry case ID, but global progression and generic fixtures are simplistic; no canonical cross-case ISO suite. |
| M1-39 | Every live Genie transition associated with conversation/message identity | **PARTIAL / MISSING** | conversation ID stored, but message ID/evidence provenance is not modeled per event. |
| M1-40 | Fallback transition records reason | **PARTIAL** | server appends `SAFE_FALLBACK` in one case, but live start failures are silently swallowed and frontend fallback is not authoritative. |

---

## 4.6 API foundation

V3 §35 requires a common `{ok,data,error,request_id}` envelope. The current endpoints mostly return raw/flat JSON and default FastAPI `detail` errors.

| ID | Requirement | Status | Gap |
|---|---|---|---|
| M1-41 | Common response/error envelope + stable error codes | **FAIL** | not implemented. |
| M1-42 | `/api/health` exposes version + Genie/warehouse config | **PARTIAL** | only `status` and `genie_mode`. |
| M1-43 | `/api/config` exposes default Case, app version, flags, audio path, instrument IDs | **PARTIAL** | returns protocol/fixture/review/enabled cases only. |
| M1-44 | `POST /api/sessions` creates `CASE_BRIEFING`, score 0, no Genie start | **FAIL** | it aliases `start_investigation`, starts Genie immediately when configured and initializes score 50. |
| M1-45 | `/sessions/{id}/start` starts Genie and returns observation, hypotheses, conversation, HYPOTHESES_READY | **FAIL** | only transitions to generic `INVESTIGATION`; Genie was already started at creation. |
| M1-46 | Prediction request validates stage + hypothesis/choice contract | **FAIL** | accepts an arbitrary dict/string, no stage/hypothesis ID validation. |
| M1-47 | Conclude validates completion contract/evidence/reconciliation/epistemic rules | **FAIL** | only checks number of registered experiments and then hardcodes a generic verdict. |
| M1-48 | Public unavailable Case returns stable `CASE_UNAVAILABLE` | **FAIL** | detail endpoint returns metadata for unreleased valid Cases; no common stable error envelope. |
| M1-49 | Free-form chat bounded/scoped | **PARTIAL / FAIL** | max 2000 instead of V3 1000; no rate limit; `GenieAdapter.ask()` forwards user text without the required Case-evidence wrapper. |
| M1-50 | Idempotency/race/double-click protection | **PARTIAL / UNTESTED** | server derives completion itself, but no defined idempotency key/concurrency contract or browser double-click E2E. |

---

## 4.7 CI, provenance, challenge/platform verification

All of the following are **MISSING / NOT PROVEN**:

- GitHub Actions CI workflows;
- exact required-check names and branch protection evidence;
- OIDC/workload-identity deployment job;
- `implementation_sha`, tree SHA and runtime digest chain;
- `scripts/classify_change.py` fail-closed path classifier;
- `scripts/compute_runtime_digest.py`;
- report-only diff validation;
- exact deployed `resolved_commit` proof;
- challenge-rule verification file;
- platform verification file;
- Free Edition deployment attestation;
- post-merge `main` CI/deploy evidence;
- MDL-1 entry and completion reports;
- sanitized immutable CI evidence.

**Additional contradiction:** README deployment guidance uses `--skip-validation`, contrary to the no-waiver/deployment validation contract.

---

# 5. MDL-2 compliance audit

## 5.1 Required target repository surface

A small subset of the MDL-2 target tree exists, but most required artifacts are absent.

### Present or partially present

```text
cases/templates/case_0042.yaml
cases/completion_contracts/case_0042_v1.yaml
data/ddl/001_schemas.sql
data/generation/models.py
data/generation/canonical.py
data/generation/stable_rng.py
data/generation/generator.py
data/generation/mutations.py
data/generation/validators.py
data/generation/private_specs/case_0042_v1.yaml
data/fixtures/public/case_0042.bundle.json
data/validation/case_0042.py
backend/data/queries.py
backend/data/sql_client.py
sql/trusted/observation.sql
sql/trusted/component_decomposition.sql
sql/trusted/snapshot_summary.sql
sql/trusted/highest_impact_records.sql
sql/trusted/dq_materiality.sql
sql/trusted/formula_validation.sql
sql/trusted/value_lineage.sql
sql/trusted/reconciliation.sql
```

### Required MDL-2 artifacts missing

```text
cases/templates/case_0107.yaml
cases/templates/case_0213.yaml
cases/templates/case_0314.yaml
cases/templates/case_0441.yaml
cases/templates/case_0520.yaml
cases/templates/case_0812.yaml
cases/schemas/case_template.schema.json
cases/schemas/completion_contract.schema.json

data/ddl/010_case_definition.sql
data/ddl/011_datapoint_result.sql
data/ddl/012_calculation_trace.sql
data/ddl/013_source_snapshot.sql
data/ddl/014_source_record.sql
data/ddl/015_snapshot_diff.sql
data/ddl/016_quality_issue.sql
data/ddl/017_pipeline_run_evidence.sql
data/ddl/018_semantic_change_evidence.sql
data/ddl/019_technical_lineage_curated.sql
data/ddl/020_private_case_truth.sql

data/views/100_case_summary.sql
data/views/110_component_evidence.sql
data/views/120_snapshot_evidence.sql
data/views/130_quality_evidence.sql
data/views/140_semantic_evidence.sql
data/views/150_pipeline_evidence.sql
data/views/160_population_evidence.sql
data/views/170_lineage_evidence.sql

data/generation/case_0042.py
data/generation/property_templates/level1_clean.yaml
data/generation/property_templates/level2_noisy.yaml

data/fixtures/public/case_0042_public.json
data/fixtures/public/case_0042_component_evidence.json
data/fixtures/public/case_0042_snapshot_evidence.json
data/fixtures/public/case_0042_quality_evidence.json
data/fixtures/public/case_0042_semantic_evidence.json
data/fixtures/public/case_0042_lineage_evidence.json
data/fixtures/hashes/case_0042.sha256

data/validation/schema_privacy.py
data/validation/sql_contracts.py
backend/data/models.py
backend/data/repositories.py
backend/data/validators.py
backend/data/private_truth_repository.py

scripts/verify_databricks_data.py
scripts/snapshot_case_data.py
scripts/restore_case_data.py
scripts/compute_mdl2_data_digest.py
scripts/fingerprint_databricks_objects.py
scripts/verify_databricks_permissions.py
scripts/build_mdl2_art_review.py
scripts/validate_mdl2_contract.py
scripts/run_iteration_gate.py

assets/review/MDL-2/A08..A12
assets/review/MDL-2/contact-sheets
assets/review/MDL-2/previews
assets/review/MDL-2/art-generation-plan.json
assets/production/images/instruments
assets/image_prompts.md
assets/art_source_manifest.yaml

docs/approvals/MDL-2-art.md
docs/traceability/MDL-2-predecessor.json
docs/traceability/mdl2-tests.csv
docs/traceability/mdl2-platform-verification.md
docs/traceability/mdl2-data-contract.json
release-report/MDL-2/*
```

---

## 5.2 Case #042 public template / private oracle

| ID | Requirement | Status | Gap |
|---|---|---|---|
| M2-01 | Public template schema-valid through shared JSON schema | **PARTIAL / UNTESTED** | YAML exists; required JSON schema files absent. |
| M2-02 | No public hidden-truth reference/field | **PARTIAL PASS** | public YAML itself appears separated, but the public canonical bundle later reintroduces private truth. |
| M2-03 | Completion contract requires all canonical experiment families | **PARTIAL** | completion YAML exists, but runtime catalog omits FORMULA_VALIDATION and uses legacy EXP IDs. |
| M2-04 | Private generation/oracle spec isolated from browser/Genie/runtime | **FAIL** | private truth is mixed into canonical public bundle. |
| M2-05 | Formula hash canonical SHA | **PARTIAL PASS** | MDL-2 generator uses the required `d1b885...` hash; legacy SQL/other path still uses old/demo semantics. |

---

## 5.3 Deterministic generator

The early MDL-2 generator gets several locked Case #042 numbers right, but it is not the specified generator architecture.

| Requirement | Status | Gap |
|---|---|---|
| Load validated public Case template | **FAIL** | generator hardcodes values; does not load `case_0042.yaml`. |
| Load separate private spec | **FAIL** | private facts are hardcoded in Python; private YAML is not authoritative. |
| Honor generator version | **FAIL** | function accepts `generator_version` but ignores it. |
| `mode=property_test` semantics | **FAIL** | parameter exists but no property mode is implemented. |
| Stable hash-derived RNG | **MISSING / UNUSED** | `stable_rng.py` exists but generator’s Case #042 path does not use it. |
| Observable phase pipeline | **MISSING** | no phase state/failures as required by MDL-2. |
| Decimal arithmetic | **PARTIAL PASS** | MDL-2 generator uses Decimal helpers. Runtime `server/domain.py` still uses floats. |
| Deterministic run/creation timestamps | **MISSING** | canonical full timestamp/run model not generated. |
| Deterministic IDs/source snapshots | **PARTIAL** | snapshot IDs/counts exist in public dict, but full source snapshot/source record model is absent. |
| Population hashes | **MISSING** | required algorithm not implemented. |
| Semantic/filter evidence | **MISSING** | not in generated canonical package. |
| Pipeline run evidence | **MISSING** | not in generated canonical package. |
| Calculation/value lineage graph | **MISSING** | not generated. |
| Technical-lineage fallback | **MISSING** | not generated. |
| Canonical serialization with NFC + explicit stable array sort | **PARTIAL / UNTESTED** | helper exists but required full policy is not proven; canonical object incorrectly includes private data. |
| Separate committed public hash file | **MISSING** | no `case_0042.sha256`. |

### Important positive partial implementation

`data/generation/generator.py` does implement the **exact MDL-2 V2 changed-row plan** much more accurately than the runtime generator:

- TX-004291: 4.20 → 0.00;
- TX-004292..296: 0.50 → 0.44;
- TX-004297..311: 0.50 → 0.46;
- TX-004312..313: 0.50 → 0.45;
- removed TX-004314 0.50 and TX-004315 0.30;
- added TX-004316..320 at 0.02;
- unchanged TX-004321..334 at 1.00.

However, because this generator is not the server/runtime/data-deployment authority and its canonical bundle leaks private truth, it does not close MDL-2.

---

## 5.4 Runtime generator contradicts exact Case #042 record plan — **FAIL**

`server/domain.py`, which is what `/api/sessions/{id}/evidence` actually uses, differs from MDL-2’s exact row contract. Among the observed mismatches:

- generic/non-canonical business keys for much of the fixture;
- different removed-row allocation (aggregate can still total -0.8 while record identities/amounts differ);
- different added-row allocation;
- changed/unchanged semantics do not match the exact curated snapshot convention;
- no canonical DQ overlap-key representation;
- no full previous/current physical snapshot rows and population hashes.

This is a classic “aggregate test passes while record-level specification is wrong” problem.

---

## 5.5 Mutation engine

`data/generation/mutations.py` declares all 10 required operator names, but only `VALUE_CHANGE` has a real effect. All other operators simply return copied records with generic evidence.

Required but not implemented to contract:

- MISSING_ROWS;
- NEW_ROWS;
- DUPLICATE_KEYS;
- PIPELINE_REPLAY;
- FORMULA_CHANGE;
- FILTER_CHANGE;
- ENTITY_MIX;
- JOIN_CARDINALITY;
- MULTI_CAUSE.

A separate `server/mutation.py` implements a few structural operations, creating another split source of truth. There are no required MDL-2 property templates or 500-sample PR property suite.

---

## 5.6 Data dictionary / DDL / curated views

The MDL-2 data model is not implemented as specified.

Problems include:

- only `data/ddl/001_schemas.sql` exists from the required numbered DDL set;
- `sql/canonical_schema.sql` is a different/incomplete schema rather than the exact MDL-2 DDL surface;
- required columns are missing/different across case definition, datapoint result, source snapshot and pipeline evidence;
- required curated views such as `case_summary`, `component_evidence`, and `population_evidence` are not provided under the MDL-2 view contract;
- some trusted SQL files reference curated views that are not actually created by the available schema scripts;
- no configured `${MDL_CATALOG}.mad_data_lab_public/private/curated` deployment path is wired end to end;
- no least-privilege grant/denial verification exists.

---

## 5.7 Trusted SQL Q1–Q8

Eight files exist under `sql/trusted/`, which is a useful partial implementation. They are **not sufficient** because:

1. runtime code does not call them;
2. live SQL verification does not execute them;
3. typed result models are missing;
4. query registry is metadata-only;
5. no native-parameterization integration suite proves inputs are safely bound;
6. no Databricks object fingerprint/data-contract digest ties live results to source;
7. required curated objects are incomplete;
8. no private-truth denial query is part of the live gate.

Therefore status is **PARTIAL / UNWIRED / UNTESTED**.

---

## 5.8 Seeding, migration, rollback, and permissions

`scripts/seed_databricks.py` does not seed Databricks. `--apply` prints a canonical hash; it does not:

- create/alter schemas/tables/views;
- load Case data;
- validate idempotence;
- record seed run ID;
- snapshot prior state;
- provide rollback manifest;
- restore prior state;
- verify app runtime grants;
- verify explicit denial of private schema;
- fingerprint deployed objects.

This entire MDL-2 deployment/migration gate is **MISSING**.

---

## 5.9 MDL-2 tests

Only four tests specifically target `data/generation`. Missing/insufficient coverage includes:

- G42-001..G42-030 named traceability;
- DG-001..DG-010;
- DP-001..DP-020;
- SQ-001..SQ-020;
- 500-sample PR property suite;
- full canonical serialization/golden hash test;
- public-bundle privacy scan;
- exact population hash test;
- exact source-record state semantics;
- pipeline evidence;
- semantic/filter evidence;
- lineage graph invariants;
- technical lineage labeling;
- private schema/view reference static scan;
- real Q1–Q8 SQL integration;
- least-privilege runtime permission denial;
- seed/idempotence/rollback tests;
- data-contract digest staleness tests.

There is also a committed `.pyc` for `tests/test_sql_contract.py` with no corresponding `.py` source in the ZIP; it is not a collected test and cannot be audit evidence.

---

# 6. V3 functional/gameplay gaps

## 6.1 Full player journey

The current UI implements a simplified Board → Briefing → Investigation → Verdict → Debrief path. Compared with V3 §§11–18, the following are missing or materially incorrect:

- initial Genie-generated H1/H2/H3 with priorities;
- dedicated initial prediction stage including **Insufficient evidence**;
- visible “Genie is choosing the next Experiment” transition;
- server-provided candidate/allowed experiment context;
- real Waterfall instrument for component decomposition;
- real Snapshot Reactor result instrument;
- actual DQ materiality stage;
- actual formula validation stage;
- lineage drill-down;
- reconciliation instrument;
- final player prediction stage;
- server-validated conclusion eligibility;
- calibrated final H1/H2/H3 statuses;
- required five debrief cards;
- Open Next Case progression action;
- dedicated valid-but-unreleased Case screen;
- unknown-case state differentiated from unavailable Case;
- robust evidence filters/sorting/pagination/detail panel.

---

## 6.2 Scoring and badges

### Implemented fragments

- +50-ish start behavior;
- +50 first prediction;
- +100 initial “correct” prediction heuristic;
- +100 evidence inspection;
- -50 hints;
- +100 per completed experiment capped at +300;
- +125 finish;
- Data Apprentice / Metric Scientist / Evidence Analyst.

### Incorrect/missing

- score starts at 50 at session creation instead of 0 then +50 Start Investigation event;
- initial correctness is detected by substring `"component"`, not canonical hypothesis/choice ID;
- no +75 required lineage/comparison evidence;
- no +200 correct final prediction;
- no -150 early reveal penalty;
- no actual final prediction;
- evidence inspection bonus is awarded automatically on first evidence endpoint call, while the UI calls that endpoint after experiments; it is not a deliberate high-value evidence action;
- score is not continuously represented as authoritative gameplay state;
- missing badges: Skeptical Scientist, Case Collector, Lab Veteran, Reconciliation Master;
- no associated canonical scoring/badge test suite.

---

## 6.3 Progression

- localStorage progression and server in-memory progression are two separate truths;
- server progression is a process-global object shared by all users/sessions;
- `/api/cases` hardcodes `completed=false` and `best_score=null` in catalog payload rather than integrating actual progression;
- badges persisted locally are not reconciled with server progression;
- secondary unlock/review logic can bypass analytical-contract readiness;
- no full progression DTO/signing/normalization contract;
- no PRG canonical test traceability.

---

# 7. Genie Agent and orchestration gaps

## 7.1 Protocol is not V3 schema 1.0 — **FAIL**

Current parser expects:

```text
experiment_id
name
instrument
rationale
evidence
hypothesis_updates
```

V3 requires structured fields including:

```text
schema_version
case_id
observation
hypotheses[{id,title,status,evidence}]
selected_experiment{id,question,target_component}
instrument{id,title}
next_action
scientist_line
```

Missing validation includes:

- schema version;
- active Case ID equality;
- H1/H2/H3 identity contract;
- target component validation;
- next-action enum;
- strict extra-field rejection;
- full recursive HTML/control safety;
- action-specific invariants.

---

## 7.2 “Repair” logic is actually deterministic substitution — **FAIL**

V3 permits one repair prompt after malformed protocol. Current `normalise_control_response()` instead catches parse failure and calls `infer_control_payload(text, expected_experiment_id)`, which inserts the experiment the application already expected.

`GenieAdapter.next()` determines `expected` as the next uncompleted registry item. Therefore malformed/natural-language Genie output is promoted into a preselected scripted experiment rather than repaired and revalidated.

This weakens the claim that **Genie decides how to investigate**.

---

## 7.3 Query attachment execution absent — **MISSING**

V3 requires Genie/query orchestration with validated query attachments/results and trusted SQL fallback only **after Genie has selected a valid Experiment**. Current code extracts text content only. Missing:

- query attachment detection;
- execution/polling;
- typed result validation;
- row/column limits;
- query failure taxonomy;
- expired result re-execution;
- safe trusted-SQL fallback after valid model selection;
- provenance linking experiment event → message/query/evidence IDs.

---

## 7.4 Initial hypotheses are not actually Genie-generated — **FAIL**

Even on a successful live Genie start, `server/main.py` ignores the returned message’s hypotheses and returns names taken from the first registered fixture experiment updates. Thus the initial game-facing hypotheses do not demonstrate Genie hypothesis formation.

---

## 7.5 Silent fallback policy violates spec — **FAIL**

Live `start` and `next` catch broad `Exception` and silently drop into fixture mode. No production feature flag prevents this. The user-facing frontend also invites the player to “continue with the verified fixture.”

V3 allows offline fixture mode as a controlled catastrophic-outage/development capability, not as an invisible normal production substitute for Genie.

---

## 7.6 Free-form Ask Dr. Genie safety/context — **PARTIAL**

The UI is correctly secondary/collapsible, but:

- server question limit is 2000, not 1000;
- no session rate limit;
- no required Case-scoped curated-evidence wrapper in `GenieAdapter.ask()`;
- no explicit refusal test for out-of-scope evidence in ordinary chat;
- no prompt-injection suite mapped to V3 IDs.

---

## 7.7 Genie configuration uses legacy data contract — **FAIL**

The checked-in Genie resource configuration/instructions target the old six-table `sda_dev.mad_data_lab` setup and legacy experiment flow. They are not the MDL-2 curated three-schema model and do not represent the full 15 Experiment / 14 Instrument registries.

---

## 7.8 Automated Genie evaluation insufficient — **FAIL / NOT PROVEN**

Current live Genie check is a tiny smoke, not the V3 benchmark. Missing:

- 10 critical PR live prompts when enabled;
- 40–80 nightly/release prompt suite;
- 100% deterministic numeric grading;
- 100% hidden-truth security prompts;
- ≥95% valid experiment-selection quality;
- enum/protocol grading after at most one repair;
- fallback-rate measurement;
- 10 consecutive full Case #042 release investigations;
- enabled-secondary-Case benchmark/soak gates.

---

# 8. Frontend, instruments, and Evidence Explorer

## 8.1 Frontend architecture — **FAIL**

V3 requires typed frontend models/state and deterministic registered Instruments. Current frontend is one large JSX file with hardcoded analytical fallback content and CSS-driven mock instruments.

Missing:

- TypeScript DTO/domain types;
- generated API types;
- reducer/context server-authoritative state model;
- typed ExperimentEvent rendering;
- instrument registry/component mapping;
- explicit loading/waiting/error/fallback state handling;
- prevention of stale/mismatched session updates.

---

## 8.2 Instruments — **MISSING / MOCKED**

The investigation stage renders four decorative bars irrespective of experiment. Required production instruments are not implemented:

- KPI delta / Anomaly-O-Meter contract;
- Waterfall / Deviation Decomposer;
- Snapshot Diff / Reactor;
- Evidence Table/Microscope;
- DQ Panel/Contamination Scanner;
- Lineage Graph/Telescope;
- Row count delta;
- Duplicate cluster;
- Run comparison;
- Formula diff;
- Filter diff;
- Entity comparison;
- Cardinality matrix;
- Reconciliation.

No schema-driven render-model validation or per-instrument visual/accessibility tests exist.

---

## 8.3 Evidence Explorer — **PARTIAL / INCORRECT**

Current UI shows a paragraph and, on the third legacy experiment, one hardcoded TX-004291 detail. Missing required Explorer behavior:

- component filter;
- change-type filter;
- business-key search backed by server contract;
- entity/segment filters where relevant;
- min/absolute impact filter;
- snapshot/source run filter;
- deterministic sort;
- pagination/cursor model in UI;
- selected row detail panel;
- lineage/comparison drill-down;
- accessible table headers/semantics;
- earned-evidence entitlement enforcement.

The backend endpoint exposes all fixture records immediately, violating MDL-2 R2-006 (existence of evidence is not entitlement).

---

# 9. Error handling, resilience, and observability

## 9.1 Error taxonomy — **MISSING**

The app uses generic FastAPI details and generic frontend strings. Missing stable codes/retryability handling for the V3 classes such as Genie timeout/invalid protocol/query failure, warehouse unavailable, invalid state, Case unavailable, evidence unavailable, etc.

## 9.2 Retry/repair — **INCORRECT**

- no bounded network retry policy tied to error classes;
- protocol repair is substitution, not one actual repair attempt;
- broad exception swallowing makes failures invisible.

## 9.3 Recoverability — **PARTIAL**

Restart and diagnostic IDs exist, which is positive. However:

- no true UNRECOVERABLE_ERROR state;
- no verified offline snapshot permission/state;
- no source-bound diagnostic structured telemetry;
- frontend can keep advancing after analytical service failure.

## 9.4 Observability — **MISSING / PARTIAL**

Only an `X-Request-ID` middleware exists. Missing V3 requirements include:

- structured JSON logs;
- session/case/experiment fields;
- Genie latency/status/retry metrics;
- SQL latency/result metrics;
- fallback rate;
- error taxonomy counters;
- no-secret logging tests;
- deploy/version/runtime identity in health/logs.

---

# 10. Security and governance

## 10.1 Positive fragments

- no obvious arbitrary `eval` or model-provided React code execution;
- unknown Case IDs are rejected;
- session IDs are server-created;
- Genie resource does not visibly point to a `case_truth` table name;
- model-selected experiment is at least checked against a local allowlist in the current parser.

## 10.2 Blocking gaps

- public fixture contains private truth;
- no deployed public/private/curated least-privilege grant proof;
- no app runtime private-schema denial test;
- no static curated-view reference scan to private schema;
- no full built-frontend truth scan;
- no dependency/security package audit in `release_gate.py`;
- no complete prompt injection/security suite;
- no CI secret scan tied to artifact/report paths;
- reports contain environment-specific/personal local paths, contrary to sanitization guidance;
- broad CORS localhost allowance exists only to accommodate the current dev topology rather than using the locked same-origin/Vite proxy approach.

---

# 11. Asset and audio audit

## 11.1 Images — **FAIL**

### Existing files

- `public/assets/Mad_Data_Lab.png` — 1280×720.
- `public/assets/board.png` — 1280×720.

### Violations

- not identified by canonical Axx asset IDs;
- no source prompt/model/version/date/right-to-use record;
- no SHA-bound human approval;
- generated readable text and data;
- generated UI controls/layout rather than decoration with HTML UI over it;
- legacy hypotheses and percentages/labels baked into the picture;
- fantasy-blue Genie identity contradicting the character bible and MDL-1 A02 hard negatives;
- insufficient separate asset system for Case Board, Dr. Genie master, key art, and instruments.

### Missing required early assets

MDL-1:

- A01 app icon;
- A02 master Dr. Genie;
- A21 Case #042 key art;
- A28 Case Board hub art.

MDL-2:

- A08 Deviation Decomposer;
- A09 Snapshot Reactor;
- A10 Data Microscope;
- A11 Lineage Telescope;
- A12 DQ Contamination Scanner;
- three candidate slots each;
- contact sheets;
- 1440×900 overlay previews;
- selected-source and final-production approval chain.

## 11.2 Audio — **PARTIAL PASS for file, FAIL for full system**

The supplied MP3 is technically much healthier than the image assets:

- duration: approximately **417.5 s**;
- 48 kHz stereo;
- integrated loudness measured approximately **-14.3 LUFS**;
- true peak approximately **-1.9 dBFS**.

Those measurements are compatible with the V3 technical loudness/peak targets.

Still missing/incorrect:

- canonical candidate/provenance/Suno selection process and source records;
- exact-byte human approval;
- gate does not actually measure LUFS/true peak/sample rate/channels/silence;
- UI does not set the specified low background playback volume (~18–25%);
- no required fade-in/fade-out behavior;
- audio preference can be restored as `on` in UI without necessarily having resumed actual browser playback;
- no full browser/autoplay/accessibility test.

---

# 12. Automated test audit

## 12.1 Existing test reality

The repository contains five Python test files and **45 passing Python tests**. These provide some real regression value, especially for:

- basic #042 aggregate reconciliation;
- server case/session rejection;
- basic state transition rejection;
- deterministic repeats in two generator implementations;
- hint bounds;
- event sequencing;
- a few parser allowlist checks.

However, a large fraction of this coverage is not aligned with V3.

## 12.2 Tests that actively lock in wrong behavior

Examples from `tests/test_case_contract.py`:

- expects first Case #042 experiment to be `EXP-01`;
- expects full sequence `EXP-01`, `EXP-02`, `EXP-03`;
- expects the Case #042 live allowlist to be exactly those three IDs;
- expects the browser dev API to contain the hardcoded localhost URL;
- tests “natural language answer promotion” into a predetermined experiment, which is not the required one-repair protocol;
- treats simple nonempty planned experiment strings as evidence that secondary Cases have explicit contracts.

These should be classified as **prototype tests requiring replacement**, not as V3 acceptance tests.

## 12.3 Canonical test-ID traceability absent

No V3 canonical named test ID appears in the repository. No MDL-1/MDL-2 traceability ledger maps current tests to requirements. Consequently:

- CI cannot detect canonical test inventory shrinkage;
- the release report cannot show which spec gates were exercised;
- conditional future Case coverage is not machine-readable;
- a green `pytest` result can hide wholesale requirement drift.

## 12.4 “E2E” is not browser E2E — **FAIL**

`scripts/local_e2e.py` exercises API/TestClient-style paths rather than Playwright browser journeys. It does not prove:

- Case Board interaction;
- keyboard navigation;
- focus behavior;
- frontend state/server synchronization;
- actual instrument rendering;
- Evidence Explorer interaction;
- final prediction;
- browser persistence/reload;
- responsive viewport behavior;
- audio/autoplay behavior;
- client double-click/race behavior.

## 12.5 Visual gate is not visual regression — **FAIL**

The visual gate checks source/build markers/selectors/assets, not screenshots against approved baselines. Missing:

- deterministic screenshot capture;
- pixel/structural visual diff;
- approved baseline policy;
- per-screen viewport coverage;
- instrument visual regression;
- approved-art hash binding.

## 12.6 Accessibility gate is insufficient — **PARTIAL**

There is some regex/static checking and an optional axe harness, but no canonical per-screen browser accessibility suite. Missing/weak areas include:

- keyboard-only Case Board and full investigation;
- visible focus order;
- modal focus trap and focus return;
- accessible table semantics;
- chart textual equivalents;
- dynamic status announcements across all transitions;
- required viewport/accessibility matrix;
- serious/critical axe gate tied to exact production screenshots/pages.

The current modal uses `role=dialog` but no actual focus trapping is implemented.

## 12.7 Security gate is insufficient — **FAIL**

The current static scanner missed the actual private-truth leak under a **public** fixture path. It also does not prove dependency security, permission boundaries, SQL/view privacy, prompt injection, or deployment artifact sanitization.

## 12.8 Chaos suite is underspecified — **PARTIAL**

The project has a small local chaos script, but V3 defines a much broader CH suite. Critical conditions such as query attachment failures, stale session actions, warehouse failures, malformed protocol/repair failure, delayed Genie, duplicate actions, cross-case leakage, and deployment/resource failures are not comprehensively covered.

## 12.9 Performance suite — **MISSING**

No meaningful V3 PF performance gate is implemented for:

- initial load/build asset budget;
- API latency with fakes;
- instrument render time;
- Evidence Explorer large-page behavior;
- Genie timeout UX;
- deployed smoke responsiveness.

## 12.10 Property/generator suite — **MISSING / PARTIAL**

No required 500-sample PR property tier or larger release/nightly property suite. No property templates exercise the mutation families and difficulty semantics.

## 12.11 SQL integration — **WRONG TARGET / INCOMPLETE**

A live SQL script exists, but it validates the legacy static schema rather than Q1–Q8 against the MDL-2 data contract and does not test permissions/private denial.

## 12.12 Live Genie evaluation — **INSUFFICIENT**

A tiny smoke is not the 10-prompt critical / 40–80 prompt release evaluation, and current grading is too permissive to prove the required analytical path.

---

# 13. Release report and gate integrity audit

## 13.1 `test-results.xml` is not a real test report

`release_gate.py` writes a single self-closing `<testsuite>` whose `tests` value is the number of **gates** (12), not the number of tests/assertions. It contains no testcase-level failures/skips/timings and cannot be used to prove canonical test execution.

## 13.2 Local “lint” is not the specified lint gate

The `lint` gate runs `compileall`, not Ruff. The typecheck gate covers only `server` and ignores missing imports/no site packages; it does not cover the planned full backend/data architecture.

## 13.3 No zero-test / test inventory protection

There is no canonical collected-test inventory check or stable-ID coverage check, so suites/files can disappear while the release report remains green.

## 13.4 Stale live PASS reuse

As described in P0-005, existing live PASS JSON is reused without validating current source. This is incompatible with the exact-commit rule.

## 13.5 Contradictory closure artifacts

- `release-report/summary.md`: live/deployed PASS.
- `docs/iterations/MDL-2-report.md`: SQL NOT_RUN, deployment NOT_RUN, art pending, predecessor unprovable.

The stricter contract says the latter blockers prevent closure. The summary should not render the build release-green.

---

# 14. V3 section-by-section compliance matrix

This matrix covers all top-level V3 sections. A **DEFERRED** item is still unimplemented in the ZIP, but is not necessarily an MDL-1/MDL-2 defect if V3 explicitly assigns it to a later iteration.

| V3 § | Area | Status | Audit finding |
|---:|---|---|---|
| 1 | Executive Decision | **PARTIAL / FAIL** | Brand exists and #042 values appear, but canonical product language/Genie centrality/multi-Case gating are not consistently implemented. |
| 2 | Consolidation Decisions | **FAIL** | D-001 partly present; D-002 aggregate intent present; D-006 truth isolation fails; D-008 legacy EXP public behavior remains; D-009 hardcoding; D-011 secondary Cases not gated by full contracts. |
| 3 | Challenge/Judging alignment | **FAIL** | removing Genie still leaves a playable scripted route; centrality not structurally proven. |
| 4 | Product vision/pitch | **PARTIAL** | concept visible but UI copy drifts from canonical strings. |
| 5 | Target audience | **NOT FORMALLY IMPLEMENTED/TESTED** | no requirement registry/UX acceptance mapping; current UI does not require SQL, which is positive. |
| 6 | Learning objectives | **MISSING/PARTIAL** | no 12-objective registry; debrief has only three cards. |
| 7 | Design pillars | **FAIL** | evidence rigor partly present, but Genie centrality, reusable Case contract, controlled adaptivity and demo-safe fallback are violated. |
| 8 | Non-goals | **PARTIAL PASS** | no major scope explosion observed. |
| 9 | World/theme/narrative | **PARTIAL** | lab theme exists; fantasy/legacy art and “data detective” copy deviate from locked scientific identity. |
| 10 | Dr. Genie character bible | **FAIL** | blue fantasy Genie/emoji contradicts explicit visual constraints; character reference system absent. |
| 11 | Core game loop | **PARTIAL/FAIL** | basic loop exists, but Genie is not genuinely selecting the full Case path and final prediction/reconciliation are absent. |
| 12 | Full player journey | **PARTIAL** | many stages collapsed or missing; required DQ/formula/lineage/reconciliation/final prediction flow absent. |
| 13 | State machine | **FAIL** | canonical states/transient states not implemented; client can advance locally. |
| 14 | Gamification/scoring | **PARTIAL/INCORRECT** | several point events/badges missing or implemented with wrong triggers. |
| 15 | Case system/catalog/progression | **PARTIAL/FAIL** | catalog exists, but metadata is wrong in places and secondary analytical contracts are not complete. |
| 16 | Definitive #042 Case | **PARTIAL/FAIL** | main aggregates correct; exact runtime records, full evidence path, private isolation and lineage are wrong/missing. |
| 17 | Educational/debrief | **PARTIAL** | epistemic statuses exist in code, but final hypothesis/debrief model is incomplete. |
| 18 | Screen-by-screen UX | **PARTIAL** | board/briefing/investigation/verdict/debrief exist; experiment selection, real Explorer, unavailable screen, instruments are missing. |
| 19 | Motion | **PARTIAL/UNTESTED** | reduced-motion CSS exists, but specified transition semantics/durations and selection animation are not systematically implemented/tested. |
| 20 | Visual design system | **PARTIAL** | themed CSS exists; current imagery/functional text approach violates art/UI separation. |
| 21 | Audio system | **PARTIAL** | audio asset file passes basic technical measures; playback volume/fades/provenance/testing incomplete. |
| 22 | Graphical asset plan | **FAIL** | asset catalog/candidates/manifest/provenance/human approvals absent; current art violates prompts/negatives. |
| 23 | Suno music plan | **MISSING/PARTIAL** | final-looking MP3 exists, but candidate generation/selection/provenance/approval process is absent. |
| 24 | Technical architecture | **PARTIAL/FAIL** | FastAPI/React/Genie SDK exist, but data/Genie/runtime responsibility flow is not the specified architecture. |
| 25 | Repository/component architecture | **FAIL** | old `server/` + monolithic JS remains; canonical modular TS/backend tree not reached. |
| 26 | Runtime/config | **FAIL** | env/config/port/offline/warehouse/deploy contracts not implemented. |
| 27 | Data architecture/dictionary | **FAIL/PARTIAL** | fragments exist; full public/private/curated tables/columns and deployed model absent. |
| 28 | Curated Genie model | **FAIL** | Genie/live SQL use legacy schema; required curated views incomplete. |
| 29 | Deterministic generator | **PARTIAL/INCORRECT** | early generator exists but hardcodes inputs, leaks private truth in canonical bundle, lacks phases/property system/full evidence. |
| 30 | Mutation engine | **PARTIAL/FAIL** | operators named, most not implemented; duplicate mutation implementations. |
| 31 | Genie Agent design | **PARTIAL/FAIL** | SDK/resource exists but uses legacy data/instructions and does not prove central adaptive role. |
| 32 | Genie instructions | **PARTIAL/INCORRECT** | current prompt is much smaller/different than canonical instruction contract and uses legacy protocol. |
| 33 | Trusted SQL | **PARTIAL/UNWIRED** | Q1–Q8 files exist but are not runtime/live-test authority; secondary queries missing. |
| 34 | Orchestration protocol | **FAIL** | wrong schema; no one-repair attempt; deterministic substitution; query attachments missing. |
| 35 | Backend API | **PARTIAL/FAIL** | endpoints exist but envelope, states, request/response DTOs, validation and conclusion semantics diverge. |
| 36 | Frontend architecture/state | **FAIL** | JS hardcoded analytical fallback; optimistic local progression; no typed server-derived analytical state. |
| 37 | Visualization instruments | **MISSING** | mock bars instead of registered data-driven instruments. |
| 38 | Evidence Explorer | **PARTIAL/FAIL** | endpoint/simple UI exists; filters/detail/entitlements/lineage/accessibility absent. |
| 39 | Error/resilience | **PARTIAL/FAIL** | recovery UI exists; taxonomy/retries/repair/fallback policy incorrect. |
| 40 | Security/governance | **FAIL** | private truth leak and no deployed least-privilege proof are blockers. |
| 41 | Observability/telemetry | **MISSING/PARTIAL** | request ID only; no structured logs/metrics/fallback/latency telemetry. |
| 42 | Testing philosophy | **PARTIAL/FAIL** | automation exists, but tests are not spec-traceable and several certify wrong behavior. |
| 43 | Test environments/doubles | **PARTIAL/MISSING** | fixtures exist, but canonical fake Genie/SQL/browser environments and boundaries are incomplete. |
| 44 | Detailed automated test catalog | **FAIL** | 412 named IDs in V3 section; zero repository traceability; many entire test layers absent. |
| 45 | Automated Genie evaluation | **FAIL/NOT PROVEN** | required benchmark and soak thresholds not implemented. |
| 46 | CI/CD | **FAIL** | no GitHub workflows; local script cannot substitute. |
| 47 | Build plan | **NOT FOLLOWED / EVIDENCE ABSENT** | required iteration evidence/closure order not demonstrated; MDL-2 started without provable MDL-1. |
| 48 | Release gates | **FAIL** | R1–R8 are not all satisfied/proven; current summary is unreliable. |
| 49 | Demo/submission plan | **DEFERRED / NOT PROVEN** | submission artifacts are not expected yet, but no current build is ready to record. |
| 50 | Player manual | **PARTIAL/OUT OF SYNC** | implemented play flow differs materially from V3 manual. |
| 51 | Developer/operator manual | **FAIL/PARTIAL** | README documents legacy install/deploy/runtime path and includes `--skip-validation`. |
| 52 | Final manual acceptance | **DEFERRED / MISSING** | no final RC acceptance, appropriately should only happen after R1–R7. |
| 53 | Definition of Done | **FAIL** | multiple mandatory requirements/gates unresolved. |
| 54 | Reference notes | **N/A as runtime feature** | source references do not require implementation, but source-verification evidence required by MDL-1 is absent. |

---

# 15. Release Gates R1–R8 assessment

| Gate | Status | Reason |
|---|---|---|
| **R1 Build integrity** | **NOT PROVEN / FAIL against MDL-1** | Python tests/imports pass, but dependency/runtime architecture is noncompliant; clean Node install/build not independently proven; no real CI exact-head build. |
| **R2 Data integrity** | **FAIL** | public truth leak; no complete G42/property suite; runtime data differs from MDL-2 canonical path; secondary cases lack golden contracts. |
| **R3 Guided flow integrity** | **FAIL** | legacy three-experiment flow; no Playwright fake-Genie journey; client fallback state bypass; no canonical cross-case suite. |
| **R4 UX integrity** | **FAIL / NOT PROVEN** | no real visual regression; incomplete accessibility browser tests; instrument/screens incomplete. |
| **R5 Asset integrity** | **FAIL** | missing manifest/approvals/assets; image content violates contract; audio gate does not measure all required properties. |
| **R6 Genie quality** | **FAIL / NOT PROVEN** | wrong protocol, weak live eval, silent fallback, missing full benchmark/query attachment path. |
| **R7 Deployed app** | **NOT PROVEN** | checked-in PASS reports are not source-bound and conflict with MDL-2 report; legacy SQL target; no exact accepted implementation identity. |
| **R8 Demo readiness** | **FAIL / DEFERRED** | no final manual acceptance; offline fixture effectively available; required visual/gameplay flow incomplete. |

---

# 16. Per-Case implementation status

| Case | V3 requirement | Current status |
|---|---|---|
| **#042 The Missing €6.8M** | full challenge blocker, deterministic evidence, Genie path, E2E, verdict | **PARTIAL / NOT COMPLIANT** — correct aggregate numbers and some exact MDL-2 rows exist, but runtime uses wrong three-step path, truth leaks, lineage/full validations absent. |
| **#107 Attack of the Clones** | TARGET if all contracts pass; L1; duplicate/pipeline route | **SCAFFOLD ONLY** — wrong difficulty, planned strings, no full data/private truth/SQL/Genie/E2E/live/visual release contract. |
| **#213 The Vanishing Revenue** | TARGET if all contracts pass; filter/lineage route | **SCAFFOLD ONLY** — no deterministic data contract or full required route. |
| **#314 The Ghost Records** | full-game gated | **SCAFFOLD ONLY** — generic fixture evidence strings. |
| **#441 The Red Herring** | full-game gated | **SCAFFOLD ONLY** — generic DQ/reconciliation strings; no analytical package. |
| **#520 The Impossible Forecast** | full-game gated | **SCAFFOLD ONLY** — no join/cardinality data/evidence implementation. |
| **#812 Double Trouble** | L3 multi-cause stretch | **SCAFFOLD ONLY** — no two-cause deterministic attribution/reconciliation implementation. |

**Required action:** do not expose secondary Cases as playable/reviewer-ready until D-011’s 12 artifacts/gates exist for each one.

---

# 17. What is genuinely implemented and worth preserving

The audit should not discard useful work. The following are legitimate building blocks, provided they are migrated into the correct architecture and tests:

- Case #042 expected/observed/deviation and four component aggregate values are represented correctly in several places.
- The early `data/generation/generator.py` contains a strong approximation of the exact MDL-2 V2 record plan.
- DQ overlap is represented as non-additive conceptually in the MDL-2 data generator.
- Server allocates session IDs and keeps an append-only sequence-numbered event list.
- Unknown Case/session requests are rejected.
- Server is authoritative over its own `completed` experiment list for `/sessions/{id}/next` rather than trusting the client’s list.
- Hints are progressive and bounded to three.
- Request IDs are generated and returned as headers.
- A closed experiment allowlist is attempted in the current Genie parser.
- No arbitrary model-provided code execution mechanism was observed.
- The MP3’s actual loudness/true-peak/sample-rate characteristics are suitable as a candidate production track.

These are **implementation fragments**, not release closure.

---

# 18. Recommended remediation order

The safest order is to repair the foundation rather than layering more UI or Cases on top of the prototype.

1. **Stop treating current release-report PASS as authoritative.** Mark current release evidence invalid/stale until tied to exact source/runtime/data identities.
2. **Repair MDL-1 first.** Move to locked TS/FastAPI architecture, locked dependencies, configuration, canonical states/registries, no analytical browser fallback, CI/CD/provenance, and exact-byte art approval.
3. **Remove all legacy Case #042 `EXP-01/02/03` and retail hypotheses from production and tests.** Replace tests with canonical IDs/traceability.
4. **Establish one Case/data source of truth.** Runtime, trusted SQL, Genie, and tests must consume the MDL-2 package/repositories, not three separate implementations.
5. **Fix truth isolation before any deployment.** Split private oracle out of public bundle; scan source/build/fixtures/views/Genie config; add negative permission tests.
6. **Finish MDL-2 generator/data model.** Template/private spec loading, full source snapshots, semantic/pipeline/lineage evidence, canonical hash, property tests, exact DDL/views.
7. **Wire and live-test Q1–Q8.** Typed result schemas, native parameters, data-contract digest, live SQL and permissions/private denial.
8. **Implement real seed/migration/rollback.** No manual workspace edits and no print-only “apply.”
9. **Only then implement MDL-3 orchestration.** Exact schema 1.0, actual one-repair attempt, Genie query attachments, safe SQL fallback only after a valid Genie choice, full benchmark.
10. **Then MDL-4/5 gameplay/instruments/Explorer**, followed by MDL-6 hardening, MDL-7 RC acceptance, MDL-8 submission.
11. **Keep secondary Cases disabled** until each independently meets D-011.

---

# 19. High-priority test worklist

The following should be created before trusting another green release report:

### Foundation/meta

- canonical V3 test-ID ledger and section traceability;
- canonical MDL-1/MDL-2 ID mapping;
- zero-test / test-inventory shrink guard;
- runtime-content digest and exact SHA checks;
- stale release-report rejection;
- CI workflow required-check topology tests.

### Truth/security

- scan every `public/`, Vite output, public fixture and API response for private truth markers;
- verify curated SQL/view definitions cannot reference private schema;
- verify app runtime identity receives permission denied on private truth;
- cross-Case evidence isolation.

### Case #042 data

- all G42 canonical cases;
- exact source record identities/amounts/null semantics;
- previous/current snapshot row counts 42/45;
- DQ five-key subset = exactly -0.30 overlap;
- formula/filter hashes;
- population hashes;
- calculation graph acyclic/reaches source;
- technical-lineage fallback label;
- zero reconciliation residual;
- byte-stable public canonical hash excluding private truth.

### Generator/mutations

- DG/DP named suites;
- 500-sample PR property run;
- every mutation operator has effect/semantics/preconditions/evidence/truth attribution;
- Level 1/2 property templates;
- multi-cause attribution property checks.

### Genie

- full strict protocol parser with unknown fields forbidden;
- active case/hypothesis/target/experiment/instrument/next-action validation;
- one repair and then safe fallback;
- ensure repair never injects expected answer/experiment;
- query attachment/result schema tests;
- hidden truth/injection suite;
- golden Case #042 selection path;
- 40–80 release prompt suite and 10-run deployed soak.

### API/gameplay

- common envelope/error codes;
- create vs start state semantics;
- prediction stage validation;
- evidence entitlement;
- conclusion eligibility and reconciliation;
- idempotency/double-click/race tests;
- progression/badge/scoring exact formula.

### Frontend/browser

- Vitest component tests;
- Playwright Case Board → #042 completion path;
- keyboard-only flow;
- modal focus trap/return;
- Evidence Explorer filters/detail;
- actual instruments;
- responsive 1280×720 + target desktop and narrow viewport;
- visual regression screenshots;
- axe per critical screen;
- audio autoplay/volume/persistence/fade tests.

---

# 20. Repository evidence index

Key files supporting the findings:

| Repository path | Relevant observation |
|---|---|
| `package.json` | `latest` dependencies; no frontend test/build quality scripts |
| `requirements.txt` | production pip requirements instead of uv lock strategy |
| `Dockerfile` | Python 3.13; copies checked-in `dist` |
| `server/run.py` | `UVICORN_PORT` only; 8000 fallback |
| `src/api.js` | hardcoded localhost API in dev |
| `src/main.jsx` | hardcoded Cases/Experiments/answers, client fallback, fantasy emoji, partial scoring/UI |
| `server/main.py` | flat API responses, early Genie start, silent fixture fallback, weak conclude validation, global progression |
| `server/state.py` | simplified non-canonical state machine |
| `server/catalog.py` | hardcoded catalog, wrong #107 difficulty, legacy #042 experiment IDs, review-mode bypass |
| `server/case_data.py` | EXP-01..03 and legacy retail hypotheses |
| `server/genie.py` | non-V3 protocol, deterministic substitution instead of repair, no query attachments |
| `server/domain.py` | runtime Case generator inconsistent with MDL-2 exact package |
| `data/generation/generator.py` | useful exact row plan but hardcoded; canonical object includes private truth |
| `data/generation/mutations.py` | only VALUE_CHANGE real; other operators no-op copies |
| `data/fixtures/public/case_0042.bundle.json` | private truth leak |
| `sql/trusted/*.sql` | Q1–Q8 source files exist but are not runtime/live-test authority |
| `sql/case_0042_setup.sql` | legacy static data path |
| `scripts/live_sql_check.py` | legacy hardcoded catalog/schema and non-Q1–Q8 queries |
| `scripts/seed_databricks.py` | print-only plan/apply; no actual seed/migration/rollback |
| `scripts/release_gate.py` | stale live PASS reuse; fake JUnit gate summary |
| `tests/test_case_contract.py` | passes while explicitly locking legacy EXP-01..03 behavior |
| `tests/test_mdl2_data.py` | privacy test checks only public dict, misses canonical/public file leak |
| `release-report/summary.md` | claims local + live/deployed PASS |
| `docs/iterations/MDL-2-report.md` | simultaneously says predecessor unprovable, art pending, SQL/deployment NOT_RUN |
| `public/assets/Mad_Data_Lab.png` | baked text/UI and fantasy Genie identity |
| `public/assets/board.png` | baked full-board UI, legacy hypotheses, text/numbers |
| `public/audio/mad_data_lab_curiosity.mp3` | technically usable audio candidate, but approval/provenance/playback contract incomplete |

---

# 21. Final conclusion

The ZIP should be treated as an **advanced prototype / partial implementation**, not as a completed iteration or submission-ready build.

The central problem is not merely that “some features are missing.” The more serious issue is that multiple green tests and release artifacts validate an architecture and Case flow that the supplied specification explicitly replaced. Before adding more features, the project needs its foundation, source-of-truth boundaries, canonical Case #042 path, and test/CI evidence model corrected so that **green actually means V3-compliant**.

### Closure classification from this audit

```text
MDL-1: NOT COMPLETE / BLOCKED
MDL-2: IN PROGRESS / NOT CLOSABLE
V3 full product: SUBSTANTIALLY INCOMPLETE
Current local pytest: 45 PASS, but not acceptance evidence for V3
Current release-report PASS: INVALID AS SPECIFICATION CLOSURE EVIDENCE
```



---

# Supplemental Independent Audit

# Appendix A — Additional Specification Compliance Gap Analysis

**Scope:** Compares the current repository state (`C:\Users\angel.alvarez\PycharmProjects\mad-data-lab`, branch `MDL-01`, single commit `25e4cec`, plus a batch of uncommitted MDL-2 working-tree files) against the three governing documents:
- `MDL-1_FOUNDATION_CANONICAL_DOMAIN_AND_CI_READY_TO_IMPLEMENT.md`
- `MDL-2_CASE042_DATA_EVIDENCE_GENERATOR_AND_SQL_READY_TO_IMPLEMENT.md`
- `MAD_DATA_LAB_Complete_Game_Specification_and_Manual.md` (V3.0)

Status tags used throughout: **NOT_IMPLEMENTED** (nothing addresses it), **PARTIAL/INCORRECT** (exists but diverges from spec), **NOT_TESTED** (code may exist but nothing proves it's correct), **DONE** (verified correct).

---

## 0. Executive Summary

The repository is **not** where its own documentation claims it is. Three independent, evidence-based audits converge on the same picture:

1. **The project's self-reported status is contradicted by the project's own files.** `docs/implementation_audit.md`, `release-report/*.json`, and `docs/submission_checklist.md` claim "PASS" for live Genie, live SQL, deployed runtime (with a specific deployment ID), a 10-run soak, full accessibility, and a 7-Case catalog — while `docs/iterations/MDL-2-report.md`, in the same repo, says SQL integration and deployment are `NOT_RUN` and art is `GENERATION_PENDING`. There is a mechanism (`scripts/release_gate.py:44-56`) that silently **republishes old "PASS" JSON from disk** instead of re-running live gates unless `RUN_LIVE_GATES=1` is set — meaning those claims are stale/unverifiable, not current evidence.
2. **MDL-1 (foundation) was not actually built.** The single commit on the repo is a monolithic prototype (`server/` package, plain `.jsx` frontend, `package.json` pinned to `"latest"`, checked-in legacy art) — this is exactly the "current early-stage scaffold" MDL-1 was supposed to replace. The branch is even misnamed (`MDL-01` instead of the contractually required `MDL-1`). There is **no GitHub Actions CI/CD at all** (`.github/` doesn't exist).
3. **MDL-2 (Case #042 data) work is real in places but critically broken in one respect and process-noncompliant in all respects.** It exists only as uncommitted working-tree files (no `MDL-2` branch, no PR). The generator produces the correct golden numbers, but as hardcoded literals rather than a working mutation-engine pipeline. Most seriously: **the "public" fixture file (`data/fixtures/public/case_0042.bundle.json`) contains the private `CASE_TRUTH` data in plaintext**, and the one test meant to catch this checks the wrong object and passes anyway.
4. **The shipped frontend hardcodes the answer.** `src/main.jsx` bakes Case #042's evidence and verdict text directly into JS instead of rendering the backend's actual response, and silently falls back to this fixture data on any API/Genie failure with no visible "offline mode" indicator — undermining the "Genie at the Core" premise the whole product is judged on.
5. **The real browser-based test tier does not exist.** No TypeScript, no Playwright, no Vitest — the "41 tests / 12 gates / 0 accessibility violations" claims rest on Python-only regex scripts and a one-off manual browser check, not reproducible automated coverage.

**Bottom line:** engineering has produced some genuinely working pieces (a real Databricks SDK Genie client, a real deployed-smoke script, correct golden Case #042 numbers, 8 SQL query files, working pytest suites for the legacy model) — but almost none of it is wired together the way the specs require, none of it is committed under the correct branch/PR workflow, and the documentation actively overstates what's done. Both MDL-1 and MDL-2 are far from their respective closure criteria.

---

## 1. Process & Git Workflow Violations (cross-cutting)

| Requirement | Reality | Status |
|---|---|---|
| Branch named exactly `MDL-1` | Branch is `MDL-01` | PARTIAL/INCORRECT |
| Branch named exactly `MDL-2`, created from clean `main` | No `MDL-2` branch exists at all; all MDL-2 files are untracked on `MDL-01` | NOT_IMPLEMENTED |
| PR opened for each iteration (`gh pr create`) | No PR exists for either iteration | NOT_IMPLEMENTED |
| `docs/iterations/MDL-1-entry.md`, `MDL-1-report.md` | Neither exists | NOT_IMPLEMENTED |
| `docs/iterations/MDL-2-report.md` | Exists, 10 lines, honestly self-reports `IN_PROGRESS` with blockers | PARTIAL (honest but structurally thin) |
| `docs/traceability/MDL-2-predecessor.json` (MDL-1 closure proof before MDL-2 starts) | Absent; report literally says `predecessor_record: NOT_PROVABLE_IN_LOCAL_REPOSITORY` | NOT_IMPLEMENTED |
| GitHub Actions CI (`.github/workflows/*.yml`) | Directory does not exist | NOT_IMPLEMENTED |
| `docs/decisions/` ADRs for D-001–D-011 and R2-001–R2-007 | Absent | NOT_IMPLEMENTED |
| `docs/traceability/*.csv` (V3 test-coverage ledgers) | Absent | NOT_IMPLEMENTED |
| No-fabrication / re-verification discipline | Violated — see §2.4 below | PARTIAL/INCORRECT |

**Implication:** even the parts of the codebase that are functionally correct cannot be considered "closed" under either contract, because the entry gates, branch/PR discipline, and traceability records that make closure provable simply don't exist.

---

## 2. MDL-1 — Foundation, Domain Model, CI/CD

### 2.1 Domain model & terminology
- State machine has 6 states (`server/state.py:7-13`) vs. the canonical 14-phase machine (`BOOT` → … → `UNRECOVERABLE_ERROR`). **PARTIAL/INCORRECT**
- `EXPERIMENTS`/`INSTRUMENTS` registries (`server/domain.py:15-16`) have 3/15 and 6/14 of the required IDs. **PARTIAL/INCORRECT**
- Case #042's registered experiments use legacy IDs `EXP-01/02/03` (`server/case_data.py:16-41`), not the canonical `ExperimentId` enum — exactly the "three-experiment scaffold" the spec calls out by name for removal. **PARTIAL/INCORRECT**
- **Banned legacy hypothesis strings are still live in production code**: `case_data.py` hardcodes `"Promo effect?"`, `"Data bug?"`, `"Pricing change?"`, `"Seasonal factor?"` instead of the locked H1/H2/H3 contract (`Source values changed` / `Formula changed` / `Data quality issue`). The spec explicitly requires a static scan test rejecting these strings; none exists. **PARTIAL/INCORRECT (severe)**
- No typed domain classes anywhere (`CaseDefinition`, `Investigation`, `ScientificVerdict`, etc.) — state is untyped `dict[str, dict]` (`server/main.py:39`). **NOT_IMPLEMENTED**
- Session score initializes to 50, not the required 0 (`server/main.py:158,163,207`). **PARTIAL/INCORRECT**
- `EpistemicStatus` enum is correctly closed and matches spec exactly (`server/domain.py:14`). **DONE**

### 2.2 Decisions D-001 through D-011
- None of `MDL1-DEC-001` through `MDL1-DEC-011` exist as named, runnable automated checks anywhere. **NOT_IMPLEMENTED** (as formal checks), even though a few of the underlying behaviors partially exist informally (e.g., D-001's four-component shape is present as one hardcoded fixture, D-006's truth-hiding has a shallow regex scan over `src/**` only).
- D-011 (12-artifact contract per Case): none of the 7 catalog Cases has the full contract; secondary Cases have a single hardcoded fallback row, no golden SQL oracle, no fake-Genie fixture, no E2E path. **NOT_IMPLEMENTED**

### 2.3 Product/brand/character contract
- No centralized brand/copy module, no learning-objective registry (12 IDs), no Dr. Genie character-bible metadata. **NOT_IMPLEMENTED**
- Case #042 hook text diverges from the locked copy ("A trusted metric is €6.8M below expectation." vs. required "€6.8M vanished from Capital Available."). **PARTIAL/INCORRECT**
- Legacy pre-MDL-1 art (`public/assets/Mad_Data_Lab.png`, `board.png`) is still tracked and is actively certified as *required* by `scripts/release_check.py:24-25` — the release gate is validating the wrong, explicitly-retired art. **PARTIAL/INCORRECT (severe — inverted gate)**

### 2.4 Repository architecture & tech stack
- No `frontend/` directory; frontend is a single 765-line plain `src/main.jsx`, no TypeScript anywhere. **NOT_IMPLEMENTED**
- No `backend/` production package (domain/api/genie/data split); backend is still the monolithic `server/` package. **NOT_IMPLEMENTED**
- `package.json` still pins `react`, `react-dom`, `vite`, `@vitejs/plugin-react` to `"latest"` — the exact problem the spec names first. **NOT_IMPLEMENTED**
- Root `requirements.txt` exists — this is **explicitly forbidden** (it would take precedence over the required `pyproject.toml` + `uv.lock`, neither of which exist). **PARTIAL/INCORRECT (direct violation)**
- `Dockerfile` uses `python:3.13-slim` vs. the locked Python 3.11 target. **PARTIAL/INCORRECT**
- No centralized config (`os.getenv` scattered through `server/main.py`/`genie.py`); launcher only reads `UVICORN_PORT`, never `DATABRICKS_APP_PORT`. **NOT_IMPLEMENTED**
- No `databricks.yml` Bundle; deployment is an ad hoc `databricks apps deploy --skip-validation` CLI sequence in the README, explicitly bypassing required bundle validation. **NOT_IMPLEMENTED**
- API envelope contract (`{ok, data, error, request_id}`), `/health`, and `/api/config` schemas all diverge from the locked field names. **PARTIAL/INCORRECT**

### 2.5 GitHub CI/CD & release-gate integrity
- `.github/` does not exist — every required check, branch protection rule, and OIDC deploy path is categorically missing. **NOT_IMPLEMENTED**
- **`scripts/release_gate.py:44-58` reuses previously-written `PASS` JSON from disk for live Genie/deployed-smoke/soak gates** instead of re-running them unless `RUN_LIVE_GATES=1` is explicitly set — the mechanical cause of the fabricated-evidence problem in §0. **PARTIAL/INCORRECT (severe)**
- Committed `release-report/*.json` files contain a hardcoded personal developer filesystem path, violating the "no developer-specific paths in evidence" rule.
- `scripts/security_gate.py` and `scripts/a11y_gate.py` are shallow regex scans, not real secret-scanning/accessibility tools, and never scan the actual shipped `dist/assets/index-*.js` bundle for leaked truth strings (spec §40.3/§44 SEC-005 explicitly requires this). **PARTIAL/INCORRECT**

### 2.6 Databricks deployment
- No OIDC/GitHub Environment config, no Bundle, no Free Edition attestation record. **NOT_IMPLEMENTED**
- `scripts/deployed_smoke.py` is a genuinely real, credible authenticated smoke script (obtains a token, exercises `/api/health`, `/api/cases`, a session flow) — a real positive — but it's run manually/locally, not CI-wired, and not tied to a specific commit's `resolved_commit`. **NOT_TESTED** (code is real; verification chain is not)
- No rollback/pre-deploy-snapshot contract exists. **NOT_IMPLEMENTED**

### 2.7 Artwork A01/A02/A21/A28
- No `assets/` directory, no prompts/manifest, no candidate generation, no human approval record of any kind exists. **NOT_IMPLEMENTED (entire section)**

### 2.8 Testing
- Existing pytest suites (`tests/test_case_contract.py`, `test_domain.py`, `test_mutation.py`, `test_state.py`) are real and plausibly run, but test the **legacy 3-experiment/EXP-01..03 model**, not the canonical domain — they'll need rewriting, not migrating. **PARTIAL/INCORRECT**
- No Vitest/Testing-Library/Playwright anywhere — no frontend test tooling exists at all. **NOT_IMPLEMENTED**
- No `docs/traceability/v3-test-coverage.csv` or equivalent — no way to verify any canonical V3 test ID's status. **NOT_IMPLEMENTED**

### MDL-1 top blocking gaps
1. No GitHub Actions CI/CD exists at all.
2. Branch is misnamed (`MDL-01` vs. required `MDL-1`).
3. Banned legacy hypothesis strings and legacy Experiment IDs are still live in production code for the release-blocking Case.
4. Self-reported "PASS" evidence is stale/carried-over, not re-verified against the current commit.
5. Wrong architecture entirely: monolithic backend, zero-TypeScript frontend, no `frontend/` directory.
6. Forbidden `requirements.txt` at root with no `pyproject.toml`/`uv.lock`; `package.json` still pins `"latest"`.
7. No artwork pipeline exists; the release gate actively certifies the wrong (legacy, pre-MDL-1) art as required.
8. No traceability/evidence infrastructure exists, so even genuine engineering work (real SDK calls in the smoke/live-check scripts) can't be tied to a verified commit.

---

## 3. MDL-2 — Case #042 Data, Generator, SQL

### 3.1 Case templates & completion contract
- `cases/templates/case_0042.yaml` broadly matches spec but is missing `sort_order: 10`. **PARTIAL**
- `cases/completion_contracts/case_0042_v1.yaml` matches spec exactly, including `allows_insufficient_evidence_verdict: false`. **DONE**
- No JSON-schema files (`cases/schemas/*.schema.json`) exist anywhere — nothing enforces "schema-valid" as the DoD claims. **NOT_IMPLEMENTED**
- Only Case #042's template exists (acceptable for this iteration's scope, but not recorded via ADR as an intentional scope reduction).

### 3.2 Private generation/oracle spec
- `data/generation/private_specs/case_0042_v1.yaml` matches the spec's logical content essentially verbatim. **DONE** for content — but see §3.6, the isolation guarantee it depends on is broken downstream.

### 3.3 Deterministic generator & mutation engine
- `generator.py` is a flat function — **none of the 21 required pipeline phases** (`LOAD_TEMPLATE` → … → `PERSIST_FIXTURES`) exist as observable stages. **NOT_IMPLEMENTED**
- Release-seed lock (reject non-42 in release mode) is correctly implemented. **DONE**
- `stable_rng.py` implements the correct SHA-256 digest scheme from spec — but is **never called anywhere**; the generator hardcodes all rows as literals instead. **NOT_TESTED (dead code)**
- `mutations.py` defines the correct 10-operator enum, but only `VALUE_CHANGE` has any real logic, and `apply_operator()` is never called by the generator at all. **NOT_IMPLEMENTED** for 9 of 10 operators; the "engine" doesn't drive generation.
- Money quantization uses `Decimal` correctly but with **no explicit rounding mode**, as the spec explicitly requires. **PARTIAL/INCORRECT**
- No deterministic timestamps/run IDs (`RUN_0042_PREVIOUS/CURRENT`, `previous_run_ts`/`current_run_ts`, `created_at`) exist in generator output. **NOT_IMPLEMENTED**
- No `property_templates/level1_clean.yaml` / `level2_noisy.yaml` exist. **NOT_IMPLEMENTED**

### 3.4 Case #042 golden values
- All headline numbers match the spec exactly as **static literals**: V1/V2/V3/V4 previous/current, the 23/2/5 V2 record-count plan, `TX-004291`, the 5-key DQ overlap summing to `-0.30`, the formula hash. **DONE**, but unverified by derivation — nothing recomputes the formula hash from `"V1 + V2 - V3 + V4"` or reconstructs the numbers from real source rows; they're copy-pasted constants. **NOT_TESTED against the actual algorithms**
- Only V2 has real per-record rows; V1/V3/V4 have no source records at all (`V1-BASE-001` etc. required by §12.4 don't exist) — the 42/45 snapshot row counts are asserted, not derived. **PARTIAL/INCORRECT**
- The population-hash algorithm (§12.9) is entirely unimplemented — no `population_hash` field exists anywhere. **NOT_IMPLEMENTED**
- Filter hash/`filter_id` (§14) is entirely absent. **NOT_IMPLEMENTED**
- `data/generation/validators.py` covers roughly 6 of the 12 required invariant checks (§26); no test IDs G42-001–027 are individually mapped or traceable anywhere. **PARTIAL / NOT_TESTED**
- No property-based (Hypothesis) tests exist at all — the DP-001–020 suite, including the 500/10,000-sample volume requirements, is entirely absent. **NOT_IMPLEMENTED**

### 3.5 Databricks DDL/views & trusted SQL
- Only `data/ddl/001_schemas.sql` (3 `CREATE SCHEMA` statements) exists; the other ~10 required DDL files and all 8 `data/views/*.sql` files are absent. **NOT_IMPLEMENTED**
- Two competing, non-conformant SQL artifacts exist instead:
  - `sql/canonical_schema.sql` — hardcoded, catalog-less naming; missing `seed`/`created_at` columns on `case_definition`; curated views are naive `SELECT *` pass-throughs missing all required derived columns (`contribution_delta`, `abs_contribution_rank`, `share_of_abs_deviation`, grouped snapshot totals) — 3 of 8 required views (`case_summary`, `component_evidence`, `population_evidence`) don't exist at all. **PARTIAL/INCORRECT**
  - `sql/case_0042_setup.sql` — a hand-written `INSERT OVERWRITE` script against an unrelated schema (`sda_dev.mad_data_lab`) that **hardcodes the old demonstrative formula hash `58d7_demo_case042`** instead of the locked production hash — a direct violation of decision R2-004, and itself one of the spec's named "does not count as implementation" anti-patterns. **INCORRECT**
- No private `case_truth` table is actually stood up anywhere. **NOT_IMPLEMENTED**
- All 8 required `sql/trusted/*.sql` files exist by name, but every one is a materially simplified/incorrect rewrite of the spec's exact query: `snapshot_summary.sql` performs no aggregation at all despite being the grouped-summary query; `formula_validation.sql` never compares formula IDs, only hashes (silently wrong if they ever diverge); several are missing required `ORDER BY` clauses. **INCORRECT**
- All 8 queries use named `:param` placeholders instead of the spec-mandated native positional `?` parameters, and `databricks-sql-connector` isn't even a declared dependency (only `databricks-sdk` is). **PARTIAL/NOT_TESTED**
- `backend/data/sql_client.py` is a 5-line stub with **no actual Databricks connection logic** (no `Config()`/`WorkspaceClient`/warehouse resolution) — nothing here could run against real Databricks today. **NOT_IMPLEMENTED**
- No typed Pydantic result models, no `repositories.py`, no `private_truth_repository.py`, no `backend/api/` exist. **NOT_IMPLEMENTED**

### 3.6 Canonical serialization, hashing & truth isolation — most severe finding
- `canonical.py` sorts keys and uses compact separators, but has no NFC normalization, no required top-level domain structure (`case_definition`, `datapoint_results`, etc.), and no stable array sort keys — structurally non-conformant with §16. **PARTIAL/INCORRECT**
- **CRITICAL: `data/fixtures/public/case_0042.bundle.json` contains the full private-truth block** (`primary_cause`, `primary_component`, `secondary_cause`, `expected_total_deviation`, `truth_json`) in plaintext, inside a file/directory literally named "public," in direct contradiction of the spec's explicit requirement that private truth be excluded from this exact artifact. The content hash is computed over this contaminated object, meaning the "canonical Case hash" is itself contaminated by secret material.
- The one test that should catch this (`tests/test_mdl2_data.py:15-16`) checks `'truth_json' not in c.public` — the **wrong, nested object** — and passes while the actual on-disk bundle leaks the data. **INCORRECT (data-security defect, not just a documentation gap)**

### 3.7 Seed/migration/rollback
- `scripts/seed_databricks.py` is an 8-line stub that only prints a dict — never touches a database, never snapshots rollback state. **NOT_IMPLEMENTED**
- `restore_case_data.py`, `snapshot_case_data.py`, `verify_databricks_data.py`, `fingerprint_databricks_objects.py`, `verify_databricks_permissions.py` — all absent. **NOT_IMPLEMENTED**

### 3.8 Artwork A08–A12 & CI/deployment
- No `assets/` directory of any kind; no human approval evidence. Self-consistent with the report's own `art_status: GENERATION_PENDING`, though the required `BLOCKED_HUMAN_ART_GENERATION` status vocabulary isn't used. **NOT_IMPLEMENTED**
- No MDL-2 CI checks, no `release-report/MDL-2/*` artifacts, no staging deployment or deployed-smoke evidence — consistent with the report's own `NOT_RUN` fields. **NOT_IMPLEMENTED**

### MDL-2 top blocking gaps
1. **Private truth leaks into the committed "public" fixture** (`data/fixtures/public/case_0042.bundle.json`), and the guard test checks the wrong object.
2. No git workflow compliance — no `MDL-2` branch, no PR, no predecessor-gate record; everything is uncommitted.
3. No real Databricks connectivity anywhere (`sql_client.py` is a stub; the SQL connector isn't even a dependency).
4. Generator/mutation engine is hardcoded literals, not a working pipeline — property-based testing across seeds is structurally impossible.
5. DDL/views are incomplete, duplicated, and contradictory, including one file with the *wrong* (superseded demonstrative) formula hash.
6. Trusted SQL Q1–Q8 don't match the spec templates and use the wrong SQL parameter style.
7. Zero property-based tests and zero G42-ID-traceable test coverage.
8. No artwork generation or human approval evidence.
9. Seed/migration/rollback scripts are non-functional stubs.
10. Backend architecture (repositories, typed models, truth boundary) is entirely absent.

---

## 4. Master Spec — Scope Violations & Fake-Completion Risks

- **Contradictory self-reported evidence**: `docs/implementation_audit.md` / `release-report/*.json` / `docs/submission_checklist.md` claim PASS for live Genie, live SQL, a specific deployment ID, and a 10-run soak — while `docs/iterations/MDL-2-report.md` (same repo) says these are `NOT_RUN`. This is the "self-reported success with no real evidence" pattern the spec's own testing philosophy exists to prevent.
- **`scripts/release_gate.py:44-56`** republishes prior "PASS" JSON instead of re-running live gates by default — a mechanism for perpetuating unverified claims indefinitely.
- **No CI/CD anywhere** — every "green gate" claimed was self-run and self-reported, not reproducible by a third party.
- **Hardcoded verdict/answer content in the shipped frontend**: `src/main.jsx` bakes Case #042's evidence prose and verdict text into JS (`active.id === "CASE_0042"` branch) instead of rendering the backend's actual computed `verdict` string — a direct violation of decision D-009 ("no control path may hardcode CASE_0042"). Compounded by silent fallback to this fixture data on any Genie/API failure, with no visible offline-mode indicator (spec explicitly requires one).
- **The entire browser-based test tier doesn't exist** (no Playwright E2E, no visual regression, no real automated axe accessibility run) despite being described in the audit docs as covered ("41 tests, 12 gates," "0 accessibility violations").
- Work spanning MDL-3 through MDL-8 (7-Case catalog with progression/badges/scoring/hints/evidence explorer, full security/a11y/visual/chaos coverage) is presented as "Verified implementation" in `docs/implementation_audit.md`, while the project's own next-iteration record is still `IN_PROGRESS` with open blockers.
- **Numeric/terminology consistency check: no mismatches found.** All Case #042 values (125.00/118.20/-6.80, component previous/current/delta, TX-004291, the 5-key DQ overlap, the expected Experiment path) agree exactly across the templates, private spec, generator, serialized Genie resource, and even the hardcoded frontend fallback — the values are consistently correct everywhere; the problem is *where* and *how* they're used (hardcoded vs. data-driven, leaked vs. isolated), not their correctness as numbers.

---

## 5. Consolidated Priority List (worst first)

1. **Private `CASE_TRUTH` data leaks into the public Case #042 fixture** (`data/fixtures/public/case_0042.bundle.json`) — a real data-security defect with a guard test that checks the wrong object.
2. **No GitHub Actions CI/CD exists at all** — nothing claimed as "green" or "PASS" anywhere in the repo's documentation can be independently verified.
3. **Self-reported completion documents contradict the repo's own iteration record** — `docs/implementation_audit.md` / `release-report/*.json` claim live Genie/SQL/deployment success that `docs/iterations/MDL-2-report.md` says never ran; `scripts/release_gate.py` mechanically perpetuates stale "PASS" results.
4. **Neither iteration follows the required git workflow** — wrong/missing branch names, no PRs, no predecessor-gate evidence; MDL-2 work is entirely uncommitted.
5. **The shipped frontend hardcodes Case #042's answer** instead of rendering the backend's real response, undermining "Genie at the Core" and violating decision D-009.
6. **MDL-1's architecture requirements are unmet wholesale** — monolithic backend, zero-TypeScript JSX frontend, forbidden `requirements.txt`, `package.json` pinned to `"latest"`, no `frontend/` directory.
7. **Legacy banned strings/IDs are still live in production code** for the release-blocking Case (`Promo effect?`, `EXP-01/02/03`) instead of the canonical H1/H2/H3 + 15-ID Experiment contract.
8. **MDL-2's generator and mutation engine don't actually generate anything** — golden numbers are hardcoded literals; the mutation operators, stable RNG, and 21-phase pipeline required for reproducibility/property-testing are unused or absent.
9. **No real Databricks connectivity exists in the MDL-2 SQL layer** — the SQL client is a 5-line stub, the connector isn't a dependency, and two contradictory/incorrect SQL schema files exist (one with the wrong, superseded formula hash).
10. **No artwork pipeline for either iteration** — A01/A02/A21/A28 (MDL-1) and A08–A12 (MDL-2) were never generated; the release gate instead certifies the legacy, explicitly-retired art as required.
11. **The real browser-based test tier (TypeScript, Playwright, visual regression, live accessibility) doesn't exist**, despite being reported as covered.
12. **Traceability infrastructure is entirely missing** for both iterations — no entry/report files, no ADRs, no test-ID ledgers — so even the genuinely working pieces (real SDK-based Genie client, real deployed-smoke script, correct golden numbers, correct completion contract, correct private spec content) can't be tied to a verified, reproducible state.
