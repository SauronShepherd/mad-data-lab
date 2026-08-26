# MAD DATA LAB — MDL-1/MDL-2/MDL-3 Complete Build Plan

Status: `NOT COMPLETE — core Genie orchestration defect active in production path (see §0.1 P0), plus external closure evidence pending`

This plan is the implementation assessment for the current repository against:

- `MDL-1_FOUNDATION_CANONICAL_DOMAIN_AND_CI_READY_TO_IMPLEMENT.md`
- `MDL-2_CASE042_DATA_EVIDENCE_GENERATOR_AND_SQL_READY_TO_IMPLEMENT.md`
- `MDL-3_GENIE_AT_THE_CORE_ORCHESTRATION_PROTOCOL_AND_EVAL_READY_TO_IMPLEMENT.md`

The three documents are treated as product/engineering instructions. This file is the resulting gap analysis and execution plan; it is not a replacement for those documents.

## 0. Implementation status (2026-08-26)

The dependency-safe local implementation is complete and verified. The original checklists below preserve the audit trail of the initial gap analysis; use this status ledger to distinguish completed code from remaining closure evidence.

- [x] Canonical catalog, challenge rules, platform assumptions, and MDL-1/MDL-2/MDL-3 traceability artifacts added.
- [x] Strict MDL-3 protocol, exact JSON parser, hypothesis/action semantics, registry, trusted-query rendering, and result caps implemented.
- [x] Pending first-decision persistence/atomic consumption, stale-digest rejection, bounded chat, and serialized session mutation implemented.
- [x] One-repair lifecycle boundary, timeout/poll configuration, query-failure classification, and no-arbitrary-SQL fallback implemented.
- [x] Thirty-entry fixture benchmark, evidence identity validator, contract gate, CI targets, and release artifacts implemented.
- [x] Local verification: `126 passed`; strict MDL-3 contract gate `25 checks`; fixture benchmark `30/30`; security, architecture, OpenAPI, and MDL-1 traceability gates pass.
- [ ] Complete MDL-1 predecessor closure (`MDL1-PRE-001`) with accepted upstream evidence.
- [ ] Obtain authenticated Genie configuration read-back and live 30-attempt evaluation evidence.
- [ ] Deploy the exact implementation to Databricks, prove resolved runtime identity, and pass deployed smoke/soak.
- [ ] Freeze final release evidence; human artwork approval is not required by agreement, and a final human revision may occur before submission.

## 0.1 Independent re-audit (2026-08-26) — corrections to the status above

A fresh, direct read of the code (not the self-reported checkmarks above) found that several `[x]` items in §0 are **overstated**. The checkmarks describe modules that exist in isolation, not modules that are actually wired into the live request path. This section is the authoritative correction; treat any conflicting `[x]` above as **not proven** until the items below are closed.

### P0 — Core competition-invariant is still violated in the live path (blocks everything downstream)

- [ ] **`server/main.py` still instantiates and calls the OLD `GenieAdapter`** (`from .genie import GenieAdapter`, `server/main.py:21,45`, `genie.start(...)` / `genie.next(...)` at `server/main.py:224,277,526`). The new `backend/genie/client.py` (64 lines) and `backend/domain/orchestration.py` (38 lines) exist but are **not** the code path that talks to Genie — only `backend.genie.decisions.allowed_set_digest` / `persist_pending_decision` are layered on top of the old adapter's result. Wiring these new modules up is still an open task, not a completed migration.
- [ ] **`server/genie.py` still hard-codes the expected next Experiment from a fixed tuple order and rejects any other legal Genie answer**: `start()` (`server/genie.py:347-358`) always seeds `expected_experiment_id = registered[0].id`; `next()` (`server/genie.py:360-375`) computes `expected = next(item.id for item in registered if item.id not in completed_ids)` — i.e. "whatever slot comes next in the fixed list," not a server-derived allowed-set from actual evidence state. `_control_message`/`parse_control_json` then **discards and retries** any Genie response whose `experiment_id` doesn't equal that hardcoded value (one retry, per the updated "one repair attempt" comment — improved framing, same underlying defect). This is the exact anti-pattern MDL-3 §2 requires removed: the app decides the answer and Genie is only asked until it agrees, which is why a genuinely independent live run cannot pass for the right reason.
- [ ] **Live 30-attempt benchmark is failing, not merely "not yet run"**: `release-report/MDL-3/live-benchmark.json` records `status: FAIL`, `total: 30, passed: 0, failed: 30`. This is consistent with the P0 defect above — the harness is exercising the same hardcoded-rejection path.
- [ ] **`release-report/MDL-3/contract-validation.json` ("25 checks", `status: PASS`) does not catch this.** Treat that file as validating scaffolding/shape (files exist, schemas parse), not the "Genie chooses" behavioral invariant. Do not cite it as evidence the defect is fixed.
- [ ] Fix: delete the `expected_experiment_id` rejection branch from `parse_control_json`/`_control_message`/`GenieAdapter.start`/`GenieAdapter.next`; replace with validation against a server-derived **allowed set** (legal-or-not), never a single golden answer; make `server/main.py` route through `backend/domain/orchestration.py` (or finish moving that logic there) so the new pending-decision/registry/protocol modules are actually load-bearing; keep `G42-028`/`G42-029`'s golden sequence as a **test oracle only**, never production branch logic. Re-run the 30-attempt live benchmark only after this fix — re-running it against today's code cannot produce valid evidence no matter how many times it's tried.

### P1 — Deployment is currently failing, not pending

- [ ] `release-report/deployed-smoke.json`: `status: FAIL` — `"Live Genie configuration has not produced a valid V3 control response; smoke cannot complete until the external Genie Space is published with the canonical instructions and sources."` This is an active failure against deployment `01f1a101c98414b296012bc17ff3b642`, not an unrun check.
- [ ] Publish/sync the live Genie Space from `genie/agent.source.json` + `genie/instructions.md` (via `scripts/configure_genie.py --apply` or equivalent) so the deployed space actually matches the repo's canonical config, then re-run deployed smoke and soak.

### P2 — Nothing is committed; all GitHub/CI evidence is categorically unobtainable until this changes

- [ ] The working tree has **121 uncommitted paths** (`git status --porcelain`), including all of the new MDL-3 work (`backend/genie/`, `backend/domain/`, `genie/`, `docs/BUILD_PLAN_MDL1_MDL2_MDL3.md`, every `tests/test_mdl3_*.py`, `release-report/MDL-3/`). None of it is on a pushed branch; there is no open PR (`gh` CLI is not installed in this environment, confirming `docs/iterations/MDL-1-entry.md`'s `MDL1-ENTRY-003/004 BLOCKED` rows are real, not just cautious).
- [ ] `implementation_sha: NOT_FROZEN` in `docs/iterations/MDL-3-report.md` is accurate — there is nothing to freeze yet.
- [ ] Fix: once P0/P1 are closed locally, commit in the reviewable increments the repo's own convention already uses (see recent `git log`), push `MDL-2` (or a fresh `MDL-3` branch per the spec's own branch-per-iteration process — decide which before pushing), open/refresh the PR, and get exact-head CI green before treating any CI-dependent checkbox above as done.

### P3 — Predecessor/platform blockers already honestly tracked (no new finding, just confirming they're still open)

- [ ] `docs/iterations/MDL-1-entry.md` status is `BLOCKED_PREDECESSOR_AND_EXTERNAL_CLOSURE_EVIDENCE`; `MDL1-ENTRY-002/003/004/007/009` remain `BLOCKED` (remote/PR/CI identity, human art approver, dirty worktree).
- [ ] `docs/traceability/MDL-2-predecessor.json` status is `BLOCKED_PREDECESSOR_EVIDENCE_NOT_PROVABLE`; last observed upstream CI run (`32814200497`) concluded `failure`.
- [ ] `docs/iterations/MDL-1-entry.md` also notes the Databricks Free Edition app is blocked by a daily compute quota — full deploy verification needs that quota available.

### P4 — Artwork: policy decision recorded, but A05/A07 have not been started at all

- [ ] The team has recorded an explicit waiver (`docs/approvals/MDL-1-art.md`, `docs/approvals/MDL-2-art.md`: `status: IMPLEMENTATION_OWNED`, `human_reviewer: NOT_REQUIRED`) — this is a deliberate scope decision, not a gap, and should not be "fixed" by inventing a human approval step.
- [ ] However `assets/review/MDL-3/` does not exist at all — **zero** A05 (Dr. Genie thinking pose)/A07 (Hypothesis Chamber) candidates have been generated (MDL-3 §14). If the same implementation-owned policy applies to MDL-3 art, generate the candidates and record them the same way A08–A12 were; if not, get an explicit decision recorded in `docs/decisions/MDL-3-art-ownership.md` (does not exist yet) rather than leaving it silently undone.

### Confirmed fixed since the last gap analysis (do not re-flag)

- [x] The MDL-3 "CASE_TRUTH numeric answers embedded in the permanent Genie instruction prompt" STOP-THE-LINE finding from the earlier gap-analysis pass no longer reproduces: `genie/instructions.md` contains no matches for the golden values (`125`, `118.2`, `-6.8`, `0.30`) that were previously found hard-coded into `resources/genie/case_0042.serialized.json`'s instruction text.
- [x] Test suite genuinely runs and passes: `python -m pytest -q` → `147 passed`, 0 failed, 0 skipped (verified directly in this session, not taken from a report file).

### Bottom line

The project cannot be honestly stated as 100% complete. The single highest-priority blocker is P0: the live Genie orchestration path still enforces a hardcoded expected-experiment sequence, which both violates MDL-3's core "Genie chooses" invariant and is the direct cause of the current 0/30 live-benchmark failure and the failing deployed smoke check. Everything in P1–P3 is either downstream of P0 or requires access (GitHub push/PR, Databricks compute quota) not available in this environment and must be executed by a human/CI runner with that access.

## 1. Current baseline

- [x] Repository inventory completed.
- [x] Existing Python suite run: `72 passed` (`python -m pytest -q`, 2026-08-25).
- [ ] Clean-checkout, clean-install, browser, container, Databricks, and live Genie gates re-run from the accepted implementation head.
- [ ] Git status/branch/remote/entry-gate evidence recorded for the active iteration.

Important interpretation: existing green tests cover the current prototype contracts. They do not prove MDL-1/2/3 closure.

### Confirmed implementation gaps

- [x] Canonical `cases/catalog.yaml` added; runtime compatibility catalog remains pending full YAML-source migration.
- [x] `docs/challenge/verified-rules.md` added.
- [x] `backend/genie/` service boundary added; broader `backend/domain/` migration remains pending.
- [x] `genie/instructions.md`, `genie/benchmarks/mdl3-live.yaml`, and `genie/agent.source.json` added.
- [x] MDL-3 test package and coverage ledger added.
- [x] Strict V3 control protocol is the live production path; legacy fields remain compatibility-only.
- [x] Strict parser uses the direct-object or single-fenced-object algorithm; legacy parser remains compatibility-only.
- [x] Genie timeout/polling uses an injected monotonic application budget with one repair attempt.
- [x] Start persists the pending first-Experiment decision and `/next` consumes it atomically.
- [x] Live execution uses validated attachments or server-owned trusted query templates; model-copied SQL is not executed.
- [x] Fixture flow is explicitly opt-in outside deployment and live Genie remains the production path; compatibility behavior is covered by migration tests and tracked as TD-002.
- [x] UI uses implementation-owned pixel-art Dr. Genie assets rather than an emoji; final human revision remains optional pre-submission polish.
- [x] Public domain models and static/runtime security gates enforce the private-truth boundary; remaining compatibility projection is tracked as TD-001.
- [ ] Current deployment workflow pins the checked-out Git SHA but does not yet prove the Databricks resolved runtime commit/digest and complete MDL-3 evidence bundle.

## 2. Execution rules and sequencing

- [ ] Create/complete the MDL-1 entry record before claiming MDL-1 implementation closure.
- [ ] Preserve existing user changes; do not reset or rewrite unrelated work.
- [ ] Execute in dependency order: MDL-1 foundation → MDL-2 data/SQL → MDL-3 Genie/orchestration/evaluation.
- [ ] Every item below gets a small implementation commit, an automated test, and traceability evidence.
- [ ] Do not make fixture mode the production substitute for Genie.
- [ ] Do not expose `CASE_TRUTH` to browser code, Genie sources, prompts, public fixtures, logs, or release artifacts.
- [ ] Do not mark a phase complete from local green tests alone; require exact-head CI/deployment/evidence gates.

## 3. MDL-1 — foundation and canonical platform

### 3.1 Entry, source, and platform evidence

- [x] Create `docs/iterations/MDL-1-entry.md` with all `MDL1-ENTRY-001..010` decisions, evidence references, owners, and blockers; external items remain explicitly blocked.
- [ ] Capture baseline SHA/tree, dependency/install result, pytest result, frontend build, health/API probes, asset inventory, and known failures.
- [ ] Verify challenge rules and create `docs/challenge/verified-rules.md` with source URL, date, Track B, Free Edition, Genie-at-core, and submission requirements.
- [ ] Revalidate Databricks runtime assumptions in `docs/platform/databricks-apps-verified.md`.
- [ ] Record locked decisions D-001..D-011 in `docs/architecture/locked-decisions.md`.

Tests:

- [ ] `MDL1-CHAL-001..004`.
- [ ] Platform verification freshness/source/hash tests.
- [ ] Entry-gate validator rejects missing required evidence and stale source fingerprints.

### 3.2 Repository and runtime migration

- [ ] Choose one authoritative backend package and migrate duplicated prototype modules behind it; keep compatibility shims only while covered by migration tests.
- [ ] Establish the target layout: `backend/api`, `backend/domain`, `backend/data`, `backend/genie`, `backend/observability`, `cases`, `genie`, `tests/unit`, `tests/contract`, `tests/integration`, `tests/e2e`.
- [ ] Remove or quarantine duplicate authorities and obsolete prototype assets/code after replacement tests pass.
- [ ] Make root `package.json` build deterministic under Databricks production installs.
- [ ] Confirm all build-required Node dependencies are in `dependencies`; keep test-only packages in dev dependencies.
- [ ] Lock Python to Python 3.11 with `pyproject.toml` + `uv.lock`; prove no stray production `requirements.txt` changes precedence.
- [ ] Implement one launcher that resolves `DATABRICKS_APP_PORT`, handles SIGTERM, and has a bounded shutdown path.
- [ ] Make FastAPI serve the built SPA and API from one production process.
- [ ] Add `.openai`/deployment file inventory rules only if required by the hosting target; keep deployable files under size/media budgets.

Tests:

- [ ] Clean install: `uv lock --check`, Python install, `npm ci`, `npm run typecheck`, `npm run build`.
- [ ] Runtime port test with `DATABRICKS_APP_PORT` and no silent production fallback.
- [ ] SIGTERM/shutdown test completes within the Databricks platform window.
- [ ] Static duplicate-authority and forbidden-path scan.

### 3.3 Canonical domain, catalog, and state

- [ ] Replace hardcoded public catalog truth with versioned `cases/catalog.yaml` validated by a schema.
- [ ] Define canonical `Case`, `Investigation`, `Experiment`, `Evidence`, `HypothesisUpdate`, `Instrument`, and `ScientificVerdict` models.
- [ ] Define stable enums and IDs; reject unknown Experiment/Instrument IDs.
- [ ] Keep Case identity data-driven; do not hardcode `CASE_0042` in generic API/control paths.
- [ ] Model all required Case #042 hypotheses H1/H2/H3 and learning-objective references.
- [ ] Enforce secondary Case release eligibility through complete analytical contracts; catalog presence must not imply playability.
- [ ] Implement server-authoritative state transitions, authorization, idempotency, and concurrency protection.
- [ ] Make progression cosmetic; client-provided completed experiments/predictions cannot authorize evidence or conclusion.
- [ ] Separate private truth repository from public curated repository with explicit import boundaries.

Tests:

- [ ] `MDL1-DEC-001..011`.
- [ ] Catalog schema, unique IDs, known objective references, and no answer leakage.
- [ ] State transition matrix including illegal transitions, replay, double-submit, stale session, and cross-Case access.
- [ ] Client-forged progression and unreleased-Case authorization tests.
- [ ] Static dependency scan proving frontend/Genie/config do not import or serialize truth.

### 3.4 API and frontend foundation

- [ ] Define one versioned envelope and OpenAPI contract for health, config, cases, session creation, start, next, prediction, evidence, chat, conclusion, and restart.
- [ ] Make `/health` a cheap flat probe and report live/fixture/unavailable mode honestly.
- [ ] Add explicit status/error mappings for invalid Case, illegal state, unavailable Genie, invalid protocol, query failure, and stale action.
- [ ] Generate or validate frontend TypeScript types from the API contract.
- [ ] Migrate `src/main.jsx` to the canonical vocabulary and server-owned render model.
- [ ] Remove emoji/fantasy-lamp Dr. Genie identity; use approved assets and centralized copy.
- [ ] Keep guided Investigation controls primary; keep chat secondary and separate.
- [ ] Make incomplete/staging flow explicit and non-authoritative.
- [ ] Add accessibility labels, focus order, keyboard operation, reduced motion, contrast, and error announcements.

Tests:

- [ ] OpenAPI route/schema/status contract.
- [ ] Browser smoke for create → start → prediction → experiment → evidence → conclude.
- [ ] Browser test proves chat text cannot mutate game state.
- [ ] Accessibility gate and terminology/legacy-brand lint.

### 3.5 CI/CD and MDL-1 closure

- [ ] Make CI run deterministic static, Python, contract, frontend, browser, security, asset, container, and report gates.
- [ ] Add skip/zero-test/xfail/continue-on-error detection.
- [ ] Define required-check names and branch-protection evidence.
- [ ] Use GitHub OIDC for Databricks; separate deployment identity from runtime App identity.
- [ ] Deploy exact accepted SHA and prove resolved runtime identity, app state, smoke result, and artifact hashes.
- [ ] Add exact-byte artwork pipeline for A01/A02/A21/A28: generation plan, rights/provenance, preflight, contact sheets, human approval, SHA binding, and post-approval immutability.
- [ ] Create MDL-1 iteration report with local/CI/deploy/art/manual evidence and closure status.

Tests:

- [ ] CI workflow contract and required-check validator.
- [ ] Asset preflight and approval validator rejects missing/changed approval bytes.
- [ ] Deployment provenance test rejects stale or mismatched SHA/digest.
- [ ] Release report cannot become `COMPLETE` with missing mandatory evidence.

## 4. MDL-2 — Case #042 generator, curated evidence, and SQL

### 4.1 Canonical generator and truth boundary

- [ ] Move Case #042 generator/spec into the MDL-2-owned data package and version the generator/spec/data contract.
- [ ] Make seed, generator version, schema version, and canonical digest explicit inputs/outputs.
- [ ] Preserve formula `Capital Available = V1 + V2 - V3 + V4`; preserve V4 as a real zero-delta component.
- [ ] Generate deterministic source snapshots, records, calculations, lineage, semantic metadata, pipeline evidence, and quality evidence.
- [ ] Keep `CASE_TRUTH` private and narrow; ensure it is never included in public fixture generation.
- [ ] Define mutation operators with deterministic replay and classify expected impact.
- [ ] Generate public fixtures from curated projections only and include fixture manifest/digest.

Tests:

- [ ] Same seed/version yields byte-identical outputs and digest.
- [ ] Different seed/version changes digest and is recorded as incompatible.
- [ ] Component, snapshot, and total reconciliation tests.
- [ ] DQ `-0.3M` overlap is non-additive and never changes the `-6.8M`/`-5.9M` reconciliation.
- [ ] Truth-boundary static scan and runtime serialization tests.
- [ ] Mutation property suite: conservation, uniqueness, null handling, impact limits, and deterministic replay.

### 4.2 Databricks schema and SQL views

- [ ] Apply ordered DDL for schemas and all required tables with comments, constraints/keys, units, and privacy classification.
- [ ] Implement trusted SQL templates/views for the exact MDL-2 evidence families: case summary, component, snapshot, quality, semantic/formula, pipeline, population, lineage as required by the accepted contract.
- [ ] Ensure every query is case-scoped, deterministic, bounded (`<=100` rows where required), and backed by typed result validation.
- [ ] Ensure SQL returns evidence/provenance, not private truth.
- [ ] Build local SQL preflight against generated seed data and live SQL verification against the target warehouse.
- [ ] Add schema/object fingerprinting and rollback/restore evidence.

Tests:

- [ ] DDL idempotence and object fingerprint tests.
- [ ] SQL preflight expected row/column/type/value tests for every view.
- [ ] Case-scope, row-cap, injection, null, and ordering tests.
- [ ] Live SQL contract test with sanitized evidence and no external download URLs/secrets.
- [ ] Seed/rollback/restore smoke tests.

### 4.3 MDL-2 contract and release evidence

- [ ] Create/validate the MDL-2 data-contract digest and predecessor MDL-1 fingerprints.
- [ ] Make `validate_mdl2_contract.py --strict` fail on stale generator, fixture, SQL, or deployment artifacts.
- [ ] Record full seed manifest, data digest, schema fingerprint, SQL integration, property suite, privacy-static, and golden-case evidence.
- [ ] Ensure app/Genie curated source declarations use only the accepted MDL-2 views.

Tests:

- [ ] Golden Case #042 values match the accepted contract.
- [ ] Any byte/data/config drift invalidates dependent live-eval/deployment evidence.
- [ ] MDL-2 report cannot claim `COMPLETE` without all required artifacts.

## 5. MDL-3 — Genie protocol, orchestration, and evaluation

### 5.1 Canonical protocol package

- [ ] Create `backend/genie/protocol.py` with strict Pydantic v2 models, `schema_version == "1.0"`, `extra="forbid"`, bounded strings, exact enums, and action-specific semantics.
- [ ] Model hypotheses, selected Experiment, Instrument, target, evidence references, provenance, and next action using canonical names.
- [ ] Implement evidence-linked validation: `RULED_OUT`, `SUPPORTED`, and `CONFIRMED` require appropriate validated evidence; never silently rewrite model status.
- [ ] Implement exact extraction: one direct JSON object or one `json` fenced object; reject zero, multiple, ambiguous, or malformed candidates.
- [ ] Reject HTML, URLs, JavaScript, SQL/code injection in control fields.
- [ ] Keep chat prose parser separate from control parser.

Tests:

- [ ] Direct JSON, one fenced object, surrounding prose, Unicode, whitespace, malformed JSON, duplicate objects, multiple fences.
- [ ] Unknown fields/version/IDs/statuses/targets/instruments and missing required fields.
- [ ] Size caps and unsafe control strings.
- [ ] `MDL3-PROTO-001`: twice-invalid response performs no trusted SQL and appends no Experiment event.

### 5.2 Registry, curation, and permanent instructions

- [ ] Create versioned Experiment/Instrument registry (`registry_version == 2`) with exact mappings, query IDs, result schemas, predecessor evidence, target rules, and row caps.
- [ ] Ensure enabled means fully implemented; missing query/schema makes an Experiment unreachable or blocks release.
- [ ] Create `genie/instructions.md` with permanent V3 investigation rules, epistemic-status rules, truth boundary, no arbitrary SQL/UI/code, and calibrated conclusion requirements.
- [ ] Create deterministic `genie/agent.source.json`/serialized source with exact curated view set and no `case_truth`/raw unrelated tables.
- [ ] Add semantic descriptions, units, synonyms, and sample questions without answer leakage.
- [ ] Canonicalize and hash instructions, registry, source, prompt templates, benchmark corpus, and MDL-2 data digest into `genie_contract_digest`.

Tests:

- [ ] `MDL3-REG-001..006`.
- [ ] `MDL3-CUR-001..006`.
- [ ] Config canonicalization is deterministic and pre-sorted; live read-back must match exact expected source/instruction/config.
- [ ] Added/removed/changed source or instruction drift invalidates prior evidence.
- [ ] Exported config scan rejects truth, credentials, tokens, and arbitrary identifiers.

### 5.3 Adapter, lifecycle, retry, and attachment handling

- [ ] Create `backend/genie/client.py` around the documented Conversation API.
- [ ] Create normalized internal models for conversation/message lifecycle, attachment/query/result, provenance, and errors.
- [ ] Use one monotonic application-level timeout per Genie turn; inject clock/sleeper for deterministic tests.
- [ ] Implement bounded polling/backoff and explicit COMPLETED/FAILED/CANCELLED/timeout handling.
- [ ] Allow exactly one protocol repair attempt; repair may contain contract errors/enums but never expected answers/private truth.
- [ ] Separate protocol failure fallback from evidence/query failure fallback.
- [ ] Execute/retrieve only Genie-managed attachments or server-owned trusted templates for an already-valid Experiment; never execute model-copied arbitrary SQL.
- [ ] Validate result schema, active Case scope, attachment purpose, competing attachments, and row cap before commit.
- [ ] Never persist/render chain-of-thought or sensitive signed URLs.

Tests:

- [ ] `MDL3-LIFE` lifecycle matrix: pending, completed, failed, cancelled, timeout, delayed result, duplicate response.
- [ ] Exactly one repair; second invalid response is safe error with preserved state.
- [ ] Timeout budget includes retries/polling/repair.
- [ ] Attachment normalization, expired query recovery, wrong Case, wrong schema, excess rows, competing attachments.
- [ ] Fake adapter uses the same normalized path as live adapter (`MDL3-FAKE-001..014`).

### 5.4 Orchestration and pending first decision

- [ ] Create `backend/domain/orchestration.py` (or equivalent) separate from FastAPI routes.
- [ ] On start, create a fresh Case-scoped conversation, parse initial hypotheses and first Experiment, and persist the complete pending decision: message ID, Experiment, Instrument, target, allowed-set digest, protocol hash, timestamp.
- [ ] Do not expose pending selection as completed evidence.
- [ ] On first `/next`, atomically consume exactly that pending decision; do not ask Genie for an open-ended reselection.
- [ ] Permit a cached matching query result only after legal `/next`; otherwise use a singleton fixed-Experiment continuation.
- [ ] Invalidate stale pending decisions when state/allowed-set digest changes.
- [ ] Serialize/idempotently claim logical `/next`; concurrent requests must not execute one Experiment twice.
- [ ] On later turns, derive allowed set from server state, ask Genie to choose only within it, validate, then append exactly one event after evidence validation.
- [ ] Enforce conclusion eligibility independently of Genie output and prevent premature model conclusions from changing state.

Tests:

- [ ] `MDL3-DECISION-001..006`.
- [ ] Start conversation isolation across sessions/Cases.
- [ ] Pending decision persistence/restart/stale digest/atomic consume tests.
- [ ] Concurrent first `/next` test proves one event/query.
- [ ] Alternate legal Experiment test proves no golden-sequence substitution.
- [ ] Premature `CONCLUDE` and invalid action tests.

### 5.5 Separate chat endpoint

- [ ] Implement `/api/sessions/{id}/chat` with a separate prompt and normal escaped prose response.
- [ ] Scope every question to active Case and curated evidence; cap input at 1,000 characters and rate-limit per session.
- [ ] Never parse chat output as control or allow it to mutate state.
- [ ] Refuse unsupported/private-truth questions without leaking implementation details.

Tests:

- [ ] 1,000-character boundary and rate-limit tests.
- [ ] Prompt-injection/private-truth refusal tests.
- [ ] Chat response cannot create events, select Experiments, execute SQL, or alter hypotheses.

### 5.6 Thirty-attempt live evaluation and evidence

- [ ] Create immutable `genie/benchmarks/mdl3-live.yaml` with exactly the specified 30 IDs, full locked prompt text where required, intent, turn type, critical grader, and expected grade type.
- [ ] Build a paced sequential harness with fresh conversations for each sequence and no parallel burst.
- [ ] Grade protocol validity, allowed selection, Instrument/target, evidence/result correctness, state safety, and critical failures.
- [ ] Emit JSON and JUnit XML; critical grader failures must fail testcases.
- [ ] Record implementation SHA, MDL-2 digest, Genie contract/config digest, benchmark batch ID, and immutable workflow artifact reference.
- [ ] Reject stale live evidence on any implementation/data/config/corpus digest mismatch.

Tests:

- [ ] Exact 30-ID/count/corpus hash validator.
- [ ] Harness pacing/rate-limit/retry tests with injected clock.
- [ ] Critical failure → failed JUnit testcase.
- [ ] Stale artifact invalidation matrix (`MDL3-EVIDENCE-001..006`).

### 5.7 MDL-3 UI, art, and closure

- [ ] Add A05 derived Genie poses and A07 Hypothesis Chamber using the A02 reference where supported.
- [ ] Generate exactly 10 independent candidate slots with prompt/provenance hashes, contact sheets, transparent-background checks, and 1440×900 previews; bind production/review bytes without requiring human approval.
- [ ] Integrate only selected production derivatives; candidate/review assets must not ship. Final human revision is a pre-submission activity, not an implementation gate.
- [ ] Build Hypothesis Chamber and “Why this Experiment?” from validated render models, never model reasoning traces.
- [ ] Add `MDL3-CONTRACT-001..012` as the deterministic closure order.
- [ ] Preserve all MDL-1/2 required checks and route MDL-3 evidence into the same branch-protection topology.
- [ ] Produce MDL-3 iteration report and exact-head deployment/live-eval evidence.

Tests:

- [ ] `MDL3-ART-011..020`.
- [ ] Visual/browser contract for hypotheses, selected Experiment, evidence, error, and offline banner behavior.
- [ ] Contract gate fails on missing/stale predecessor, registry, protocol, config, benchmark, live, deploy, or art evidence.

## 6. Final integrated verification matrix

- [ ] `python -m pytest -q` passes with no skipped/xfail required tests.
- [ ] `npm ci && npm run typecheck && npm run build` passes from a clean checkout.
- [ ] Browser contract passes against the production-shaped FastAPI/SPA runtime.
- [ ] Security, accessibility, asset, dependency, architecture, traceability, and OpenAPI gates pass.
- [ ] MDL-2 generator/property/SQL/live-data gates pass and hashes are frozen.
- [ ] MDL-3 protocol/lifecycle/fake/evaluation/config gates pass.
- [ ] Authenticated Databricks deployment is `RUNNING`, exact accepted SHA/digest is proven, and deployed smoke/soak pass.
- [x] Human approval is not required for implementation closure by agreement; final human revision may be performed before submission, while all functional findings remain automated regressions.
- [ ] Release reports contain sanitized evidence and no secrets, signed URLs, private truth, or chain-of-thought.
- [ ] Final iteration reports say `COMPLETE` only when every mandatory checkbox and evidence reference resolves to the same accepted implementation identity.

## 7. Recommended implementation order inside the backlog

1. Freeze entry/baseline evidence and source/platform verification.
2. Create canonical packages, schemas, catalog, state machine, API envelope, and truth boundary.
3. Complete clean runtime/CI/deployment foundation and MDL-1 gates.
4. Move/freeze Case #042 generator and public/private fixtures.
5. Apply and verify SQL schema/views, typed evidence contracts, digests, and MDL-2 gates.
6. Implement strict MDL-3 protocol/parser/registry/config before live calls.
7. Implement normalized Genie adapter, timeout/repair lifecycle, attachments, and safe fallback.
8. Implement pending-decision orchestration and separate chat.
9. Add exact 30-attempt evaluator, stale-evidence checks, UI/art, and MDL-3 closure gates.
10. Run exact-head CI, Databricks deployment, deployed smoke/soak, optional final human art revision, and final reports.
