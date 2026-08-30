# MDL-4 - Complete Guided Case #042 Game Flow, Server-Authoritative State, Predictions, Scoring, Badges, and Scientific Verdict

## Iteration contract metadata

| Field | Locked value |
|---|---|
| Iteration | `MDL-4` |
| Required branch | `MDL-4` |
| Depends on | merged/closed MDL-3 |
| Definitive source | V3.0, 2026-08-23, planning SHA-256 `237570e5d62cee11e78ecced43c8449f62f53e7b547e9fe1bfbf4ed54eb0cc44` unless an approved addendum/replacement is merged |
| Primary V3 closure sections | §§11–15,17,35,36 |
| Required art/media gate | A03, A06 |
| Deployment target | Free Edition staging/challenge app |
| Human gate before closure | exact-byte A03/A06 human approval + allowed visual/runtime/log deployment inspection (not the MDL-7 full manual functional acceptance) |
| Closure status vocabulary | `IN_PROGRESS`, `BLOCKED`, `COMPLETE` (never infer COMPLETE from partial green checks) |
| Document maturity | `READY_TO_IMPLEMENT` |


## MDL-4 source reconciliations and ownership addenda

These decisions resolve ambiguities that would otherwise force Codex to invent gameplay semantics. They are binding for MDL-4 and must be recorded in `docs/decisions/` when implemented. They do not weaken V3; they make its requirements executable.

### Gameplay reconciliation G-001 — prediction correctness must not leak through score

V3 requires the first prediction to be stored **without revealing correctness**, while the scoring formula awards `+100` when that prediction is correct. Therefore, before Scientific Verdict/Debrief, public session/API payloads must not expose any score total, score-event list, bonus field, or delta from which the correctness of the initial prediction can be inferred.

The server may calculate and store private score events immediately, but the browser sees only:

```text
score_visibility = HIDDEN_DURING_INVESTIGATION
```

until the verdict is accepted. The first public score breakdown appears at Scientific Verdict/Debrief. Do not display a live running total during Case #042. This also prevents network inspection from turning the score into a correctness oracle.

### Gameplay reconciliation G-002 — explicit Debrief transition is required for the +125 event

The V3 score table contains `Finish debrief +125`, but the minimal endpoint list does not contain a Debrief action. MDL-4 adds the non-breaking endpoint:

```text
POST /api/sessions/{session_id}/debrief
```

This endpoint is legal only after an accepted Scientific Verdict. It appends `DEBRIEF_ENTERED`, awards the `+125` debrief-completion score event once, transitions to `DEBRIEF`, materializes progression/badges, and returns the final score. Repeating the same idempotency key returns the original result.

The Scientific Verdict screen may show `score_before_debrief`; the Debrief screen shows the final score. The UI must label the former clearly so the +125 transition is not surprising.

### Gameplay reconciliation G-003 — evidence rewards require explicit server-validated inspection events

A GET request for an evidence page is not proof that the player inspected a high-value record or lineage. MDL-4 adds:

```text
POST /api/sessions/{session_id}/evidence/inspect
```

with a closed interaction enum. The server validates that the referenced evidence is unlocked, belongs to the active Case/session, and qualifies for any score reward before appending the inspection event.

### Gameplay reconciliation G-004 — refresh requires a session read model endpoint

The V3 minimal endpoint list does not include a session read endpoint, but the selected refresh policy cannot be implemented reliably without one. MDL-4 adds the non-breaking endpoint:

```text
GET /api/sessions/{session_id}
```

It returns the safe authoritative session projection only. It never returns private truth, hidden score correctness during the Investigation, raw Genie reasoning, or private idempotency records.

### Gameplay reconciliation G-005 — early reveal remains a narrow alternate path

Preserve the existing MDL-4 reconciliation: early reveal is legal only after all analytical completion prerequisites except final prediction are satisfied. It applies `-150`, records the final prediction as `SKIPPED_BY_EARLY_REVEAL`, and cannot be used to bypass required Experiments/evidence/reconciliation.

### Artwork ownership addendum

The hardened MDL-1 ownership table originally deferred A03 and A06 to MDL-5. MDL-4 now **pulls A03 and A06 forward** because this iteration makes the complete guided shell, Scientific Verdict, and Debrief playable and therefore needs the production lab entrance plus the positive Eureka pose in-context.

Binding rule:

```text
A03 — primary owner: MDL-4
A06 — primary owner: MDL-4
MDL-5 — re-use/revalidate; do not regenerate competing masters unless a human rejects/reopens the MDL-4 asset
```

A05/A07 remain owned by MDL-3. A04 remains deferred to its later owner. Every later derivative must reference the approved source/production SHA from its owning iteration.

---

## Purpose

This iteration turns the now-trusted data layer and Genie orchestration layer into the complete guided Case #042 game defined by the V3 specification.

By the end of MDL-4, a deterministic fake-Genie test must be able to complete Case #042 automatically from Case Board to Debrief, while the live staging deployment must be able to traverse the same server-authoritative flow with Genie choosing the analytical path.

This iteration also removes remaining prototype logic such as a single prediction, hardcoded scores, hardcoded badges, three-experiment progress, and static frontend verdict text.

MDL-4 is finished only when:

- the full shell state machine is implemented through Debrief;
- initial and final predictions are separate;
- score is computed from the canonical 1,000-point formula;
- all seven canonical badges are implemented;
- conclusion eligibility and numerical correctness are validated on the server;
- no client can skip required analytical state;
- the complete fake-Genie E2E path is green;
- GitHub CI and deployed staging smoke are green;
- this iteration's artwork is generated and human-approved.

## Mandatory execution order

Codex should execute this iteration in the following order. Later phases may prepare in parallel only when they cannot invalidate an earlier gate; closure order remains strict. The technical focus of MDL-4 is **complete server-authoritative guided game/scoring/verdict/progression flow**.

| Phase | Required action | Exit condition |
|---:|---|---|
| 0 | Read this entire file, the accepted V3 source/addenda, current `main`, predecessor evidence, and current platform-verification record. | No unresolved source/predecessor ambiguity; blockers recorded rather than guessed around. |
| 1 | Verify clean `main`, predecessor/source hashes, then create/inspect branch `MDL-4` exactly as specified. | Correct branch/base/tree recorded; no unrelated local work. |
| 2 | Start this iteration's required artwork/audio production immediately after branch creation using the locked prompt/reference/provenance rules. | Candidate generation request/prompt + manifest state recorded. Human approval may remain pending while engineering continues. |
| 3 | Implement the iteration-owned product/data/Genie/UI/hardening requirements in small test-backed commits. | Owned functionality exists without bypasses/placeholders in production paths. |
| 4 | Run the lowest-layer deterministic/static/contract suites continuously, then the complete local iteration gate. | Mandatory local gates green; no hidden skip/xfail/zero-test condition. |
| 5 | Preflight final candidate artwork/audio and obtain **explicit human approval of the exact production bytes**. | Approval record says `APPROVED`, approver/time/provenance present, recorded SHA-256 matches bytes. Rejection loops back to Phase 2. |
| 6 | Commit all approved runtime-affecting content, push the final head, open/update the PR, and run required GitHub CI on that exact head. | Required GitHub checks green on `implementation_sha`; no stale CI evidence. |
| 7 | Deploy that exact accepted implementation identity to the required Databricks environment and run automated post-deploy validation. | Deployment/build identity matches accepted runtime digest; smoke/integration gates green. |
| 8 | Perform only the manual inspection/acceptance explicitly allowed in this iteration and record objective observations. | No unaddressed manual defect; any defect has regression test + fix + invalidated gates rerun. |
| 9 | Generate sanitized closure evidence/report/manifest, classify any report-only diff, merge through protected GitHub flow, and verify post-merge `main`. | `main` CI/deployment obligations green; iteration closure `COMPLETE`; next iteration predecessor gate can pass. |

**Do not advance merely because engineering code is complete.** Human asset approval, exact-head GitHub CI, Databricks deployment evidence, and post-merge verification are part of the iteration, not administrative follow-up.

## Preconditions

Do not start MDL-4 until:

- MDL-3 is merged to `main`;
- `main` CI green;
- live Genie critical evaluation green;
- real Genie can select the first/next Experiment;
- production silent scripted fallback has been removed;
- Case #042 data/curated views remain green;
- MDL-3 art approval is recorded.


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

If the post-deployment commit changes a runtime-affecting path, the report-only exception is void: set a new `implementation_sha`, rerun every invalidated gate, redeploy, and collect new evidence.

The deployed app is therefore required to match the accepted **implementation identity/runtime digest**, not a later documentation-only report commit. The PR/merge evidence must record both identities when they differ.

### Branch safety and predecessor verification

Before creating or continuing `MDL-4`:

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
git merge-base origin/main MDL-4
```

Confirm it is the intended active iteration branch and contains no unrelated/stale work. Do not silently recreate it from a different base.

After creating/continuing the branch, verify `origin/main` is an ancestor unless an intentional, documented rebase/merge is in progress:

```bash
git merge-base --is-ancestor origin/main HEAD
```

### Machine-enforced predecessor gate

The “do not continue until previous artwork is human-approved” rule is executable. Before creating or resuming `MDL-4`, while checked out on the clean updated `main` branch:

```bash
python scripts/validate_human_approvals.py --iteration MDL-3
python scripts/validate_traceability.py
```

Then verify the previous iteration closure evidence from the merged PR/GitHub artifacts:

```text
previous iteration: MDL-3
merged PR number/URL
merge SHA and tree
implementation_sha/runtime digest
final required GitHub checks green
Databricks deployment/smoke PASS
human artwork approval status APPROVED
approved production asset hashes still match current main
open mandatory blockers = 0
```

If the previous iteration manifest is committed, validate it with `validate_iteration_manifest.py`. If the final observed manifest lives as an immutable GitHub workflow artifact to avoid a self-referential report commit, retrieve/inspect that artifact and record its artifact/run ID in `docs/iterations/MDL-4-predecessor.md`.

Do **not** create/continue the new iteration branch when the previous art approval is `PENDING`, `REJECTED`, stale by hash, missing from merged `main`, or when a mandatory prior engineering/deployment gate is red/unknown. The correct state is `BLOCKED_PREDECESSOR_MDL_3` until the prior iteration is repaired/closed.

Also verify the definitive-source baseline before branch creation:

```bash
python scripts/validate_source_baseline.py
```

The accepted baseline is V3.0 dated 2026-08-23 (planning SHA-256 `237570e5d62cee11e78ecced43c8449f62f53e7b547e9fe1bfbf4ed54eb0cc44`) unless merged `main` contains an explicit human-approved replacement/addendum chain. An unexplained source hash change is `BLOCKED_SOURCE_DRIFT`; do not continue using stale iteration assumptions.

The predecessor record is required evidence for MDL-4 closure. It proves the branch did not advance merely because someone verbally said the prior iteration was finished.

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
BLOCKED_PREDECESSOR_MDL_3            predecessor closure/approval/deploy evidence is not valid (not applicable for MDL-1)
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

As soon as `MDL-4` exists, create `docs/iterations/MDL-4-report.md` with an explicit non-final status such as:

```yaml
iteration: MDL-4
status: IN_PROGRESS
base_main_sha: <observed>
implementation_sha: null
open_blockers: []
```

Add headings/placeholders for the required local tests, CI runs, deployment, artwork approval, manual inspection, decisions, regressions, and remaining blockers. **Do not fill unknown evidence with fake IDs or PASS.** Use `NOT_RUN`, `PENDING`, `BLOCKED`, or `UNKNOWN` until observed.

The early skeleton serves three purposes:

1. `gh pr create --body-file docs/iterations/MDL-4-report.md` always has a real file;
2. reviewers can see progress/blockers before closure;
3. finalization is an update to an existing audit record, not a late invented success narrative.

The report becomes `status: COMPLETE` only after all iteration gates are satisfied and the release-contract validator accepts it.


```bash
git fetch origin --prune
git checkout main
git pull --ff-only origin main
test -z "$(git status --porcelain)"
git checkout -b MDL-4
```

Recommended commits:

```text
MDL-4: implement complete investigation session state machine
MDL-4: add initial and final prediction APIs
MDL-4: add scoring badges hints and progression
MDL-4: add server-validated scientific verdict and debrief
MDL-4: add complete fake-Genie E2E flow
MDL-4: integrate approved lab entrance and Genie eureka art
MDL-4: add iteration completion report
```

Push and PR:

```bash
git push -u origin MDL-4
gh pr create --base main --head MDL-4 --title "MDL-4 Complete guided game flow" --body-file docs/iterations/MDL-4-report.md
```


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

- at least one non-empty `MDL-4: ...` implementation commit exists on the iteration branch;
- behavioral changes and their tests should normally be committed together or in a clearly ordered reviewable sequence;
- generated caches, local reports containing secrets, personal IDE state, and unapproved binary candidates are not committed;
- after the final approved asset/report changes, commit again as needed and push the **new** head; CI evidence from an earlier head is stale;
- `git status --porcelain` is empty at the point the accepted head is declared.

### Post-merge `main` failure recovery

The iteration is not closed until the required post-merge `main` workflow is green. If the already-merged `MDL-4` content exposes a main-only integration/deployment failure:

1. mark MDL-4 closure `REOPENED_POST_MERGE`;
2. do **not** advance to MDL-5;
3. preserve the failed main workflow/deployment evidence;
4. if the original iteration branch cannot be safely reused because it has already been merged, create a narrowly scoped recovery branch named `MDL-4-recovery-<k>` from the failed current `main`; this does not replace the required original `MDL-4` branch;
5. add a regression test/release check reproducing the main-only failure where possible;
6. fix, commit, push, PR, and run the full invalidated required checks for the recovery head;
7. merge only when the recovery PR is green;
8. require the subsequent `main` workflow/deployment smoke to be green and update the iteration/predecessor evidence chain.

Never delete/rewrite the merged history or claim the earlier PR was sufficient because its branch checks were green.

## Target MDL-4 repository changes

Preserve the modular architecture created in MDL-1. Exact filenames may vary only when the mapping is documented and the same boundaries remain enforceable.

```text
backend/
  api/
    routes/
      cases.py
      progression.py
      sessions.py
      evidence.py
      chat.py
    schemas/
      cases.py
      sessions.py
      progression.py
      errors.py
  domain/
    investigation.py
    events.py
    state_machine.py
    completion.py
    scoring.py
    badges.py
    progression.py
    evidence_entitlements.py
  sessions/
    store.py
    idempotency.py
    locks.py
  private/
    case_oracle.py
    verdict_validator.py
  genie/
    # MDL-3 package; may consume safe session/evidence context, never private oracle

cases/
  completion_contracts/
    case_0042_v1.yaml
  scoring/
    case_0042.yaml or equivalent private scoring mapping

frontend/src/
  api/
    generated/ or schemas/
    client.ts
  state/
    session.ts
    progression.ts
  pages/
    CaseBoardPage.tsx
    CaseBriefingPage.tsx
    InvestigationPage.tsx
    ScientificVerdictPage.tsx
    DebriefPage.tsx
    CaseUnavailablePage.tsx
  components/
    HypothesisBoard/
    PredictionPanel/
    ExperimentTransition/
    ExperimentResult/
    EvidenceInspection/
    ScoreBreakdown/
    BadgeList/
    DrGeniePanel/

assets/
  review/MDL-4/
    A03/
    A06/
    contact-sheets/
    previews/
    art-generation-plan.json
  production/images/
    dr-genie/
    backgrounds/

docs/
  approvals/MDL-4-art.md
  decisions/
    ADR-early-reveal.md
    ADR-mdl4-api-extensions.md
    ADR-mdl4-private-truth-runtime.md
  iterations/
    MDL-4-report.md
    MDL-4-predecessor.md
  traceability/
    mdl4-tests.csv
    mdl4-game-contract.json

scripts/
  compute_mdl4_game_digest.py
  validate_mdl4_contract.py
  run_mdl4_fake_e2e.py or Playwright equivalent
  run_mdl4_live_session.py
  build_mdl4_art_review.py
  run_iteration_gate.py

release-report/MDL-4/
  game-contract-digest.json
  domain-summary.json
  score-golden.json
  api-contract.json
  replay-summary.json
  truth-isolation.json
  fake-e2e.json
  art-preflight.json
  deployed-smoke.json
  live-session.json
```

Do not leave duplicate production session/scoring implementations in the old `server/` scaffold and new `backend/` tree. Compatibility adapters are temporary branch scaffolding only and must be removed or made a single delegating boundary before closure.

## MDL-4 game-contract digest and stale-evidence rules

Create `scripts/compute_mdl4_game_digest.py`.

The digest includes every committed path that can change guided gameplay behavior, score, verdict eligibility, progression, API semantics, or production flow. At minimum:

```text
cases/catalog.yaml
cases/templates/**
cases/completion_contracts/**
cases/scoring/**
backend/domain/**
backend/sessions/**
backend/private/**
backend/api/**
backend/genie/** protocol/prompt source affecting MDL-4 flow
frontend/src/api/**
frontend/src/state/**
frontend/src/pages/**
frontend/src/components/** gameplay-relevant components
frontend/src/App.tsx
frontend/src/main.tsx
tests/** gameplay/API/E2E fixtures
scripts/run_mdl4_live_session.py
scripts/run_iteration_gate.py
package.json + package lock
pyproject.toml + Python lock
app.yaml
databricks.yml
production asset manifests + approved A03/A06 bytes
```

It also records predecessor identities rather than folding their entire repositories into one opaque hash:

```text
v3_source_sha256
mdl1_accepted_implementation_or_tree
mdl2_data_contract_digest
mdl2_canonical_case_hash
mdl3_genie_contract_digest
mdl3_live_config_sha256
```

Digest algorithm follows the existing project convention:

```text
SHA-256(
  for each included repository-relative POSIX path sorted lexicographically:
    UTF8(path) + NUL + raw_file_bytes + NUL
)
```

Unknown gameplay-affecting paths are included fail-closed until classified.

Any change to the game-contract digest invalidates:

- fake-Genie E2E closure evidence;
- score golden artifact;
- API contract artifact;
- live integrated session evidence;
- deployed smoke evidence when runtime-affecting;
- art approval only when approved asset/reference/preview bytes change.

A report-only Markdown edit may reuse prior runtime evidence only under the inherited runtime-content classifier and only when `game_contract_digest` remains exactly unchanged.

Add `MDL4-EVIDENCE-001..008` for digest determinism, predecessor identity presence, stale E2E rejection, stale live-session rejection, art-only classification, report-only classification, unknown-path fail-closed behavior, and immutable artifact resolution.

## Canonical player journey to implement

The complete Case #042 shell must support:

```text
BOOT
  -> CASE_CATALOG
  -> CASE_BRIEFING
  -> STARTING_INVESTIGATION
  -> HYPOTHESES_READY
  -> PLAYER_PREDICTION (initial)
  -> SELECTING_EXPERIMENT
  -> RUNNING_EXPERIMENT
  -> EXPERIMENT_RESULT
  -> optional EVIDENCE_EXPLORATION
  -> SELECTING_EXPERIMENT
  -> ... repeat until Case completion criteria satisfied ...
  -> PLAYER_PREDICTION_FINAL
  -> CONCLUDING
  -> DEBRIEF
  -> CASE_CATALOG
```

Do not create Case #042-specific global states such as `RESULT_1`, `RESULT_2`, or `DQ_STAGE`. Those are Experiment events.

## Server-authoritative Investigation model

Extend the Investigation domain object to hold at minimum:

```text
session_id
case_id
case_template_version
phase
observation
hypotheses
predictions
experiment_history
current_experiment
collected_evidence_ids/tags
hints_used
hint_ids_used
evidence_inspection markers
score events
current_score
genie_conversation_id
genie_message_ids
fallback events
conclusion
created_at / updated_at if used
```

### Event append-only requirement

Represent state changes as append-only events or an equivalent immutable history.

Example Experiment event:

```json
{
  "sequence": 2,
  "experiment_id": "SNAPSHOT_DIFF",
  "target": "V2",
  "instrument_id": "SNAPSHOT_DIFF",
  "evidence_ids": ["E-021", "E-022"],
  "hypothesis_updates": ["H1:SUPPORTED"],
  "completed": true
}
```

Do not derive completion from a hardcoded number such as `3` or `5`. Derive it from the Case completion contract and required evidence/experiment families.

### Canonical MDL-4 event vocabulary

Implement one closed event enum. Event payloads are typed/versioned and append-only. Minimum event types:

```text
SESSION_CREATED
INVESTIGATION_STARTED
INITIAL_PREDICTION_SUBMITTED
EXPERIMENT_DECISION_QUEUED
EXPERIMENT_STARTED
EXPERIMENT_COMPLETED
EVIDENCE_INSPECTED
HINT_REVEALED
FINAL_PREDICTION_SUBMITTED
EARLY_REVEAL_REQUESTED
SCIENTIFIC_VERDICT_ACCEPTED
DEBRIEF_ENTERED
PROGRESSION_UPDATED
SESSION_ABANDONED
```

Do not create score by mutating a `score` field directly. Score is a deterministic projection from score-bearing events. Do not create a second hidden mutable state machine beside the event history. A cached/materialized session projection is allowed only when replaying the event log yields the same authoritative result.

Every event has at minimum:

```text
event_id             unguessable stable ID
sequence             strictly increasing integer within session
event_type           closed enum
schema_version       event payload version
session_id
case_id
created_at
request_id           when produced by API request
idempotency_key_hash when applicable; never raw secret-like data
payload              typed per event_type
```

`sequence` is the authoritative `state_revision`. It starts at `1` for `SESSION_CREATED` and increases by exactly one per appended event.

### Session projection contract

A safe public projection contains at minimum:

```text
session_id
case_id
case_template_version
phase
state_revision
observation
hypotheses
initial_prediction public choice only
final_prediction public choice or SKIPPED_BY_EARLY_REVEAL
experiment_history safe render summaries
pending_action metadata safe for UI
unlocked_evidence capabilities
hints_revealed
score_visibility
verdict when accepted
debrief/progression when reached
```

Before Scientific Verdict, omit:

```text
initial_prediction_correct
final_prediction_correct
private score events
private score total
CASE_TRUTH
expected next Experiment oracle
raw Genie internal reasoning
private idempotency table
private validation oracle details
```

### Concurrency and state revision

All state-changing endpoints must serialize by session using one of:

1. a per-session async lock in the single-process challenge MVP; or
2. an equivalent shared atomic transaction if a persistent/shared session store is introduced.

Additionally, state-changing requests carry an `expected_state_revision` field or `If-Match`-equivalent header generated from the latest public projection. If the session has moved and the request is not an exact idempotent replay, reject with:

```text
STATE_REVISION_CONFLICT
HTTP 409
retryable: true
```

The client refreshes the session projection before deciding whether to retry.

Until a shared session store exists, production must run exactly one application worker/process for authoritative in-memory sessions. CI must fail if deployment configuration starts multiple independent workers while the session store is process-local.

### Session lifetime and cleanup

Use a configurable challenge-MVP TTL with a default of **2 hours** from last activity. Session/idempotency records expire together. Expiration never converts into a partial resumed session. The API returns `SESSION_EXPIRED`, and the UI offers `Restart Investigation`.

Required configuration:

```text
SESSION_TTL_SECONDS=7200 default
MAX_ACTIVE_SESSIONS=256 default
```

If the configured max is reached, reject new sessions with a stable retryable capacity error; never evict an active session silently.

### Pending Genie decision handoff from MDL-3

MDL-3 may already have a validated first/next Genie Experiment selection. MDL-4 must preserve it instead of re-asking Genie unnecessarily.

Rules:

- `/start` may persist one validated `pending_decision` from the initial Genie response;
- the player still submits the initial prediction before any Experiment executes;
- the first legal `/next` consumes that exact pending decision atomically;
- after an Experiment, if the validated Genie turn already selected the next legal Experiment, persist it as the next `pending_decision`;
- `/next` asks Genie to choose only when no valid pending decision exists;
- stale pending decisions are invalidated if the Case contract/allowed set/state revision changes incompatibly;
- two concurrent `/next` calls cannot consume one pending decision twice;
- a transport/query retry may execute evidence for the already-selected decision but may not silently choose a different Experiment.

Add custom tests `MDL4-DECISION-001..008` covering initial persistence, atomic consumption, no duplicate re-selection, stale invalidation, retry execution, concurrent `/next`, legal no-pending selection, and no client-forced pending decision.

## API completion

Implement the V3 endpoint family with stable response envelopes. The API is an authoritative domain boundary, not a thin proxy for client-owned state.

### Global JSON envelope and HTTP semantics

Every application JSON API endpoint uses the V3 envelope **except `/api/health`, which preserves the narrow flat platform-probe exception locked in MDL-1**:

```json
{
  "ok": true,
  "data": {},
  "error": null,
  "request_id": "req-uuid-or-equivalent"
}
```

Errors use:

```json
{
  "ok": false,
  "data": null,
  "error": {
    "code": "ILLEGAL_STATE_TRANSITION",
    "message": "This action is not available in the current investigation state.",
    "retryable": false
  },
  "request_id": "req-uuid-or-equivalent"
}
```

Rules:

- `request_id` exists on successes and failures and is safe to show/copy;
- validation failures use stable 4xx responses; internal/platform failures use stable 5xx/503 semantics as appropriate without exposing stack traces;
- no API accepts client-supplied score, hypothesis status, completed-experiment state, verdict truth, Genie message IDs, or Case availability as authoritative;
- unknown JSON fields are rejected on state-changing requests unless an explicit forward-compatible schema version says otherwise;
- all state-changing endpoints verify the `session_id` belongs to the Case/state being acted upon;
- evidence/chat filters never allow arbitrary table/view/SQL selection;
- Pydantic/typed response models are used so private fields cannot leak by serializing a broader internal object.

### Idempotency contract

State-changing requests that can be repeated by browser retry/double-click must accept an `Idempotency-Key` header (or an equivalently explicit request-operation ID) and bind it to:

```text
session_id
endpoint/action
normalized request body hash
resulting event/result identity
```

`Idempotency-Key` format:

```text
16..128 printable ASCII characters
recommended client format: UUID v4
case-sensitive opaque value
```

Store only a SHA-256/HMAC-safe digest of the raw key when persistence/logging would otherwise retain it. Request-body equality uses canonical JSON after typed parsing, not raw whitespace/key order. Idempotency scope is `(session_id, endpoint/action, key)` except session creation, which is scoped to the anonymous/request context plus action.

Required behavior:

- same key + same normalized action returns/replays the original accepted result without a second score/event/Genie call;
- same key + different body/action is rejected as `IDEMPOTENCY_CONFLICT`;
- two concurrent `/next` requests cannot produce two Experiment events;
- retries after a transport timeout do not double-charge hints, early-reveal penalty, or score;
- idempotency records must not store secrets/raw chat longer than necessary;
- if the MVP keeps session state in memory, idempotency guarantees are scoped to the lifetime documented for that session, and restart behavior must be explicit/tested.

### Stable MDL-4 error taxonomy and HTTP mapping

Use one closed error-code registry. Endpoint code must not invent ad-hoc strings. Minimum codes:

| Code | HTTP | Retryable | Meaning |
|---|---:|---|---|
| `VALIDATION_ERROR` | 422 | no | request failed typed validation |
| `CASE_NOT_FOUND` | 404 | no | unknown Case ID |
| `CASE_UNAVAILABLE` | 409 | no | known Case not available in current release/review mode |
| `SESSION_NOT_FOUND` | 404 | no | unknown session ID |
| `SESSION_EXPIRED` | 410 | no | known/expired session cannot resume |
| `SESSION_CAPACITY_REACHED` | 503 | yes | bounded in-memory store cannot accept another active session |
| `ILLEGAL_STATE_TRANSITION` | 409 | no | action illegal in current phase |
| `STATE_REVISION_CONFLICT` | 409 | yes | stale non-idempotent action |
| `IDEMPOTENCY_CONFLICT` | 409 | no | same key used for different normalized action |
| `INVALID_PREDICTION` | 422 | no | choice not valid for active Case/stage |
| `EVIDENCE_NOT_UNLOCKED` | 409 | no | evidence exists but current session has not earned access |
| `EVIDENCE_NOT_FOUND` | 404 | no | evidence ID not present/visible for session Case |
| `NO_MORE_HINTS` | 409 | no | Case has no additional hint |
| `HINT_NOT_YET_AVAILABLE` | 409 | no | next hint would reveal evidence not yet visible |
| `CONCLUSION_NOT_READY` | 409 | no | completion/reconciliation prerequisites missing |
| `DEBRIEF_NOT_READY` | 409 | no | verdict not yet accepted |
| `GENIE_UNAVAILABLE` | 503 | yes | control/evidence path unavailable without valid progression |
| `EVIDENCE_UNAVAILABLE` | 503 | yes | selected Experiment evidence could not be validated/retrieved |
| `VERDICT_VALIDATION_FAILED` | 409 | no | proposed conclusion contradicts validated evidence/contract |
| `INTERNAL_ERROR` | 500 | maybe | sanitized unexpected server failure |

`message` is user-safe and stable enough for UI category handling. Debug/stack details remain logs-only and correlated by `request_id`.

### Safe API model separation

Maintain separate internal/private and public response models. Add a serialization test asserting the public schemas contain none of:

```text
CASE_TRUTH fields
primary_cause oracle
expected_path_json
allowed_final_status_json
private mutation metadata
OAuth/service-principal secrets
raw Genie internal reasoning/chain-of-thought
```

### `GET /api/health`

Keep cheap and non-secret. This endpoint is the **flat JSON exception** to the normal `{ok,data,error,request_id}` application envelope, matching the MDL-1 platform-probe reconciliation. It must not make a live Genie/warehouse query in the normal health request. Return at minimum:

```json
{
  "status": "ok",
  "version": "<app-version>",
  "build_id": "<accepted-build-or-runtime-digest>",
  "genie_configured": true,
  "warehouse_configured": true
}
```

`genie_configured` means required configuration/resource binding is present, **not** that a live downstream call just succeeded. Live readiness/integration belongs in deployment smoke/diagnostics, not a cheap liveness probe.

### `GET /api/config`

Return only safe UI configuration, for example:

```text
default_case_id
app_version/build_id
public feature flags
audio asset path
supported Instrument IDs
challenge/review mode flags that are safe to expose
```

Never return Databricks host credentials, client IDs/secrets, raw resource tokens, private schema names, truth metadata, or server-only fallback controls.

### `GET /api/cases`

Public catalog only. Each item is limited to safe fields such as:

```json
{
  "case_id": "CASE_0042",
  "public_number": 42,
  "title": "The Missing €6.8M",
  "hook": "€6.8M vanished from Capital Available.",
  "difficulty": "LEVEL_2",
  "release_state": "CORE",
  "availability": "AVAILABLE",
  "completed": false,
  "best_score": null,
  "learning_objectives": ["DECOMPOSITION", "SNAPSHOT_DIFF", "DQ_MATERIALITY"]
}
```

`include_unreleased=true` is honored only under explicitly server-configured review/development mode; a user-supplied query flag alone cannot unlock unreleased Cases.

### `GET /api/cases/{case_id}`

Return public briefing metadata and the initial observation only for a released/available Case. A known but unavailable Case returns stable `CASE_UNAVAILABLE`; an unknown identifier returns `CASE_NOT_FOUND`. No request may reveal private truth or expected path by changing query parameters.

### `GET /api/progression`

Return normalized completion/best score/badges. A local-first challenge implementation is acceptable if server validation prevents forged unlocks. If client-local progression is submitted for normalization/signing, the server validates Case IDs, maximum score bounds, prerequisite completions, and badge rules; it never trusts a client-supplied `unlocked=true`.

### `POST /api/sessions`

Request:

```json
{ "case_id": "CASE_0042" }
```

Create an unguessable session identity bound immutably to the validated Case and return `CASE_BRIEFING`, score `0`, and safe public Case context. Reject unavailable/unknown Cases. Session creation does not itself award Start Investigation points.

### `GET /api/sessions/{session_id}` — MDL-4 refresh/read-model extension

Return the current safe server projection described above.

Required behavior:

- `404 SESSION_NOT_FOUND` for unknown ID;
- `410 SESSION_EXPIRED` for an expired session when distinguishable;
- never refresh TTL on obviously invalid/forged IDs;
- safe read may refresh last-access TTL only after session identity is valid;
- never call Genie or SQL merely to read the current projection;
- never expose hidden prediction correctness/score during Investigation;
- `state_revision` always equals the latest event sequence;
- response includes enough information for the frontend to reconstruct the current screen after browser refresh.

### `POST /api/sessions/{session_id}/start`

Legal only from the briefing/startable state. It starts a fresh Genie conversation scoped to the session Case, obtains/validates the initial hypothesis protocol, appends the start event, awards the canonical start points once, and returns state `HYPOTHESES_READY`. Duplicate retries are idempotent and must not start a second Genie conversation.

### `POST /api/sessions/{session_id}/prediction`

Initial request shape:

```json
{
  "stage": "INITIAL",
  "hypothesis_id": "H1"
}
```

Final prediction uses `stage: "FINAL"` and the Case-defined final explanation choice ID. Validate that the choice belongs to the active Case/stage. Initial and final predictions are separate immutable events. Repeating the same idempotent request does not award score twice; changing an already-accepted prediction after advancement is rejected unless replay/reset is explicitly part of the Case flow.

Every prediction request also carries `expected_state_revision`. The server returns the new `state_revision`. The response does **not** reveal whether the prediction was correct and does not return a score delta/total that would reveal correctness.

### `POST /api/sessions/{session_id}/next`

Main orchestration endpoint. Required server order:

1. lock/serialize the session action or use an equivalent concurrency guard;
2. verify current state and completion contract;
3. compute the **allowed next Experiment set** from the Case/session;
4. ask Genie to choose from that set;
5. validate the protocol and current-state legality;
6. obtain/validate query evidence or the permitted trusted-SQL fallback for that already-selected Experiment;
7. validate Instrument/evidence schema and numeric invariants;
8. append one Experiment event and hypothesis updates;
9. calculate score effects server-side;
10. return the typed render model.

Representative response data:

```json
{
  "state": "EXPERIMENT_RESULT",
  "experiment": {"id": "COMPONENT_DECOMPOSITION", "title": "Decompose the deviation"},
  "instrument": {
    "id": "WATERFALL",
    "data": [
      {"component": "V1", "impact": -1.2},
      {"component": "V2", "impact": -5.9},
      {"component": "V3", "impact": 0.3},
      {"component": "V4", "impact": 0.0}
    ]
  },
  "hypotheses": [],
  "scientist_line": "Aha. V2 is carrying most of the anomaly.",
  "fallback_used": false
}
```

A Genie/protocol/query failure that has not produced valid evidence must not advance the Experiment sequence.

### `GET /api/sessions/{session_id}/evidence`

Read-only, session-scoped evidence. Support only allowlisted typed filters such as:

```text
component
change_type
business_key
minimum_abs_impact where supported
limit
cursor
```

Server caps `limit` at **100**. Default sort for record evidence is deterministic `ABS(impact) DESC` with a stable business-key tie-breaker. A session cannot request evidence from another Case and a filter value never becomes a raw SQL fragment.

### `POST /api/sessions/{session_id}/evidence/inspect` — MDL-4 scoring/entitlement extension

Request:

```json
{
  "evidence_id": "CASE_0042:RECORD:TX-004291",
  "interaction": "OPEN_DETAIL",
  "expected_state_revision": 12
}
```

Closed interaction enum:

```text
OPEN_DETAIL
OPEN_LINEAGE
OPEN_COMPARISON
```

Rules:

- evidence ID must be namespaced to the active Case;
- evidence must already be unlocked by completed Experiment/evidence capabilities;
- the server resolves evidence metadata itself; client cannot submit `high_value=true` or reward points;
- duplicate inspection of the same qualifying scoring category is idempotent and cannot award twice;
- opening the high-value Case #042 record may create the +100 score event;
- opening the Case-required lineage/comparison may create the +75 event;
- an evidence row fetched in a list but never opened does not count as inspected;
- failed/stale inspection requests do not change score or state.

### `POST /api/sessions/{session_id}/hint`

Return the next server-determined progressive hint based only on visible evidence and safe Case metadata. The client does not choose `hint_number`. For #042 there are exactly three canonical hints. Each hint ID can be charged only once; requesting after hint 3 returns a stable no-more-hints result and no additional score deduction.

### `POST /api/sessions/{session_id}/conclude`

Accept an explicit mode:

```json
{ "mode": "NORMAL", "expected_state_revision": 19 }
```

or the narrowly defined:

```json
{ "mode": "EARLY_REVEAL", "expected_state_revision": 19 }
```

`NORMAL` is legal only after the analytical completion contract and final prediction are satisfied. `EARLY_REVEAL` is legal only after the same analytical evidence/completion prerequisites and before a final prediction, records the one-time `-150` event, and cannot be inferred from missing fields. Both modes obtain/validate the Genie synthesis plus backend numeric/epistemic verdict rules. On success, the session remains in/enters the canonical `CONCLUDING` phase with `SCIENTIFIC_VERDICT_ACCEPTED` in the event projection; only the explicit `/debrief` action transitions to `DEBRIEF`.

### `POST /api/sessions/{session_id}/debrief` — MDL-4 scoring/progression extension

Request:

```json
{
  "action": "OPEN_DEBRIEF",
  "expected_state_revision": 20
}
```

Legal only after `SCIENTIFIC_VERDICT_ACCEPTED`. Required server order:

1. validate verdict already exists;
2. append `DEBRIEF_ENTERED` exactly once;
3. award `FINISH_DEBRIEF +125` exactly once;
4. calculate final clamped score;
5. derive newly earned badges;
6. normalize progression/best score/unlock state;
7. return Debrief DTO plus final score/badges/progression.

Repeated idempotent calls replay the original result. A second different-key call after Debrief is already entered returns the current Debrief projection without another +125.

### `POST /api/sessions/{session_id}/chat`

Optional free-form Dr. Genie console, strictly separate from game-state control. Request:

```json
{ "question": "Why is the DQ warning not enough?" }
```

Rules:

- maximum **1,000 user characters** after normalization;
- server automatically scopes the question to the active Case;
- apply a per-session token bucket with default **6 accepted chat requests/minute and burst 2** (configurable downward/upward only through server config, not client input) so repeated chat cannot exhaust Free Edition quota;
- free-form answers cannot emit/apply Experiment, score, status, progression, or verdict control events;
- hidden-truth/table-access attacks are answered only from Genie-visible evidence;
- render returned prose as escaped text/structured safe Markdown policy, never model-provided raw HTML;
- log IDs/timing/result category, not internal reasoning/chain-of-thought or unnecessary raw user content.

Add an explicit test proving a chat response containing a valid-looking control JSON block does **not** mutate the Investigation state.

## MDL-4 authoritative API action matrix

The OpenAPI document and generated frontend client must encode this matrix. `Idempotency-Key` is required on every state-changing POST. `expected_state_revision` is required except where no session exists yet (`POST /api/sessions`).

| Endpoint | Method | State change | Idempotency | Calls Genie | Can award score | Legal phase(s) |
|---|---|---|---|---|---|---|
| `/api/health` | GET | no | n/a | no | no | any |
| `/api/config` | GET | no | n/a | no | no | any |
| `/api/cases` | GET | no | n/a | no | no | any |
| `/api/cases/{case_id}` | GET | no | n/a | no | no | any |
| `/api/progression` | GET | no | n/a | no | no | any |
| `/api/sessions` | POST | yes | key required | no | no | none |
| `/api/sessions/{id}` | GET | no | n/a | no | no | active session |
| `/api/sessions/{id}/start` | POST | yes | key required | yes | +50 | briefing/startable |
| `/api/sessions/{id}/prediction` | POST | yes | key required | no | +50/+100 or +200 privately | prediction phase |
| `/api/sessions/{id}/next` | POST | yes | key required | maybe/yes | +100 cap events | selecting/experiment-ready |
| `/api/sessions/{id}/evidence` | GET | no | n/a | no | no | evidence-capable states |
| `/api/sessions/{id}/evidence/inspect` | POST | yes | key required | no | +100/+75 | unlocked evidence states |
| `/api/sessions/{id}/hint` | POST | yes | key required | no | -50 | active Investigation before verdict |
| `/api/sessions/{id}/conclude` | POST | yes | key required | yes | -150 if early reveal; final correctness already determined by prediction | conclusion-ready |
| `/api/sessions/{id}/debrief` | POST | yes | key required | no | +125 + badges/progression | accepted verdict |
| `/api/sessions/{id}/chat` | POST | no game mutation | request dedupe/rate limit | yes | no | active session |

Rules:

- `/chat` may have transport dedupe but never appends gameplay/control/score events;
- `prediction` internally records correctness but its public response hides it until verdict;
- `/conclude` cannot award the +200 final-correct bonus because that bonus is tied to the already-accepted final prediction event; early reveal has no final prediction and therefore no +200;
- `/debrief` is the only event that finalizes the +125 and completion/progression mutation;
- GET endpoints cannot mutate score merely because the browser fetched a resource;
- generated OpenAPI/client schemas must document `Idempotency-Key`, revision conflicts, and stable error codes.

Add `MDL4-APIEXT-001..018` for session read, evidence inspect, Debrief action, revision handling, score privacy, error mapping, and the matrix invariants above.

## Exact Case #042 gameplay/completion contract

Create/finish `cases/completion_contracts/case_0042_v1.yaml` (or an equivalent typed source) as the single server-readable Case #042 gameplay contract. The browser may receive only safe derived fields.

### Blocking analytical families

Case #042 cannot reach final prediction until all five unique required Experiment families have completed with validated evidence:

```text
COMPONENT_DECOMPOSITION
SNAPSHOT_DIFF
DQ_MATERIALITY
FORMULA_VALIDATION
RECONCILIATION
```

Their order remains Genie-controlled within the MDL-3 allowed-set rules. The only guided golden expectations are the already-defined MDL-3 first/second decisions; the app must not hardcode the remainder as a frontend sequence.

`SOURCE_RECORD_INSPECTION`, `VALUE_LINEAGE`, and `TECHNICAL_LINEAGE` may be valid additional Experiments when allowed by the server, but Case #042 completion does not require a dedicated `SOURCE_RECORD_INSPECTION` Experiment. This preserves the canonical optional-record-inspection E2E path.

### Blocking evidence/validation conditions

The Case completion projection must also prove:

```text
COMPONENT_IMPACT evidence exists and total = -6.80
SNAPSHOT_IMPACT evidence exists and V2 net = -5.90
DQ_MATERIALITY evidence exists and overlap=true, estimated impact=-0.30
FORMULA_VERSION evidence exists and formula_changed=false
RECONCILIATION evidence exists and residual=0.00 within <=0.01 tolerance
V2 snapshot residual = 0.00 within <=0.01 tolerance
required lineage/comparison evidence has been explicitly opened by the player
```

For MDL-4, define the required lineage action as a stable Case-scoped capability, for example:

```text
CASE_0042:LINEAGE:V2_SOURCE_PATH
```

It resolves to the already-trusted lineage data from MDL-2. The exact raw row/node IDs remain data-layer details; the completion contract references a stable semantic capability/tag.

### Optional but rewarding evidence

The Case #042 high-value evidence item is:

```text
CASE_0042:RECORD:TX-004291
```

Opening its detail after it is unlocked awards the one-time +100 high-value-evidence score event, but **does not block conclusion**. A run can therefore complete without it and score 900 on an otherwise perfect path.

The high-value item becomes inspectable only after the relevant snapshot/source evidence has been unlocked. Never expose it before the session has evidence entitlement merely because the backend knows it exists.

### Evidence entitlement projection

Do not expose MDL-2's entire Case evidence corpus to every session. Derive an entitlement/capability set from completed Experiment events. Example safe capability evolution:

```text
START/HYPOTHESES
  -> observation only

COMPONENT_DECOMPOSITION complete
  -> COMPONENT_IMPACT

SNAPSHOT_DIFF complete
  -> SNAPSHOT_IMPACT
  -> SOURCE_RECORD_DETAIL for V2 changed records
  -> V2_SOURCE_LINEAGE drilldown capability

DQ_MATERIALITY complete
  -> DQ_MATERIALITY

FORMULA_VALIDATION complete
  -> FORMULA_VERSION

RECONCILIATION complete
  -> RECONCILIATION
```

This is an access-to-evidence rule, not a security boundary for hidden truth. The server still validates every evidence ID and Case namespace independently.

### Final hypothesis semantics for Case #042

At conclusion eligibility the canonical broad hypothesis statuses are:

```text
H1 Source values changed   SUPPORTED
H2 Formula changed         RULED_OUT
H3 Data quality issue      POSSIBLE
```

A narrower evidence claim may be `CONFIRMED`, for example:

```text
TX-004291 changed 4.20 -> 0.00 and contributes -4.20
V2 changed-record population reconciles exactly to -5.90
```

Do not upgrade the broader H1 hypothesis to `CONFIRMED` merely because one or more narrower record-impact claims are directly confirmed. Do not set H3 to `RULED_OUT`; the DQ issue is real but insufficient/overlapping as the primary explanation.

### Completion predicate

Implement one pure domain function similar to:

```text
evaluate_case_completion(case_contract, event_log, validated_evidence)
    -> CompletionEligibility
```

It returns:

```text
ready_for_final_prediction
missing_required_experiments[]
missing_required_evidence_actions[]
failed_reconciliations[]
blocking_reason_codes[]
```

The public API may expose safe missing requirements such as `FORMULA_VALIDATION_REQUIRED` or `OPEN_REQUIRED_LINEAGE`, but must not expose an expected root cause or private truth.

Add `MDL4-COMP-001..012` covering the exact five-family contract, optional high-value record, required lineage, residual tolerance, DQ overlap, formula requirement, dynamic order, duplicate Experiment handling, unknown Experiment rejection, safe missing-requirement output, and successful final-prediction eligibility.

## Initial hypotheses and prediction

After starting Case #042, display exactly these hypothesis families:

```text
H1 - Source values changed - priority HIGH
H2 - Formula changed - priority LOW
H3 - Data quality issue - priority MEDIUM
```

The player prediction control must be generated from the Case contract, not hardcoded to a generic retail list.

For Case #042, initial prediction options and stable IDs are:

```text
PRED_SOURCE_VALUES_CHANGED      — Source values changed
PRED_FORMULA_CHANGED            — Formula changed
PRED_DATA_QUALITY_ISSUE         — Data quality issue
PRED_INSUFFICIENT_EVIDENCE      — Insufficient evidence
```

Private Case #042 scoring oracle:

```text
correct_initial_prediction_id = PRED_SOURCE_VALUES_CHANGED
```

Store the initial prediction without revealing correctness. The correctness ID belongs in a private scoring/truth mapping, not the public Case DTO and not Genie-visible data.

Dr. Genie line:

```text
Good. Now earn the conclusion.
```

Do not overwrite this selection when the final prediction is made.

## Experiment progression behavior

### First analytical Experiment

Release target:

```text
COMPONENT_DECOMPOSITION
```

After validated evidence, expected Case #042 statuses are:

```text
H1 SUPPORTED
H2 POSSIBLE
H3 POSSIBLE
```

The application must not set these optimistically before the backend returns validated evidence.

### Subsequent Experiments

The Case contract must ensure the Investigation cannot conclude without evidence covering:

- component decomposition;
- snapshot comparison;
- DQ materiality;
- formula validation;
- reconciliation;
- required source/lineage evidence tags defined by the Case contract.

Source-record inspection and lineage may be encouraged/required by evidence tags even if their exact Experiment order varies.

The UI label `Experiment 01`, `Experiment 02`, etc. is derived from event count, not a fixed set of pages.

## Final prediction

When completion prerequisites are satisfied but before conclusion, transition to `PLAYER_PREDICTION_FINAL`.

Ask:

```text
Which explanation is now best supported by the evidence?
```

Options and stable IDs:

```text
FINAL_CHANGED_V2_SOURCE_RECORDS   — Changed V2 source records
FINAL_FORMULA_MUTATION            — Formula mutation
FINAL_DQ_WARNING                  — DQ warning
FINAL_INSUFFICIENT_EVIDENCE       — Evidence remains insufficient
```

Private Case #042 scoring oracle:

```text
correct_final_prediction_id = FINAL_CHANGED_V2_SOURCE_RECORDS
```

Store separately from initial prediction. No Case code may infer final correctness from label text; compare closed IDs through the private Case scoring oracle.

The Debrief must be able to compare initial and final predictions.

## Explicit V3 reconciliation — early reveal versus final prediction

The definitive V3 source contains two requirements that otherwise conflict if implemented literally:

- the canonical player journey places final prediction before the Scientific Verdict;
- the scoring table defines `Reveal conclusion before final prediction` as a real `-150` event.

Do not silently delete either rule. Preserve both with one narrow alternate path:

1. the Investigation must already satisfy all analytical completion prerequisites (required evidence, blocking Experiments, reconciliation, formula/DQ checks);
2. when the UI reaches the final-prediction stage, offer a secondary explicit action such as `Reveal Scientific Verdict now (-150)`;
3. selecting it requires confirmation because it skips the final prediction and incurs the penalty;
4. send an explicit request mode, for example `{ "mode": "EARLY_REVEAL" }`;
5. the server records an append-only `EARLY_REVEAL` score/event exactly once, subtracts 150, and marks final prediction as `SKIPPED_BY_EARLY_REVEAL` rather than inventing a hypothesis choice;
6. Genie/backend then produce/validate the same evidence-grounded verdict as the normal path;
7. Debrief states that the final prediction was skipped and shows the reveal penalty;
8. the action is impossible before the analytical Case completion prerequisites are met.

Normal `CONCLUDE` with no final prediction remains illegal unless `EARLY_REVEAL` was explicitly requested/recorded. A malformed/retried request cannot accidentally convert into early reveal.

This reconciliation makes the V3 scoring event executable without allowing a player to skip the investigation itself. Record the decision in an ADR (for example `docs/architecture/ADR-early-reveal.md`) so later developers do not remove the penalty as “dead code.”

## Scientific Verdict architecture

### Genie role

Genie provides a concise final synthesis from visible evidence.

### Backend role

The backend independently validates conclusion eligibility and numeric consistency before accepting the verdict.

The backend must validate:

- all required evidence tags collected;
- all blocking Experiments resolved;
- final prediction submitted **or** an explicit valid `EARLY_REVEAL` event exists after analytical completion;
- component reconciliation residual within tolerance;
- V2 snapshot reconciliation within tolerance;
- formula evidence says unchanged;
- DQ overlap/materiality represented correctly;
- conclusion does not claim DQ is primary;
- conclusion does not claim formula changed;
- source evidence supports V2 record-change explanation;
- final hypothesis statuses obey epistemic rules.

### Private truth usage

The backend may use private `CASE_TRUTH` only as a final scoring/evaluation oracle. It must not be injected into the Genie prompt and must not determine which Experiment Genie should choose.

Create a private validator module with a narrow interface. Do not import it into `backend/genie/*`.

Add an automated import/dependency guard test that fails if Genie modules import private truth modules.

### MDL-4 private-truth permission transition

MDL-2 deliberately proved that the App runtime did not need private truth for evidence serving. MDL-4 is the first iteration that needs a narrow server-only truth oracle for prediction scoring and final verdict validation. Make that privilege expansion explicit rather than quietly broadening the App service principal.

Allowed production design:

```text
App backend runtime principal
  -> SELECT only the minimum private CASE_TRUTH object/columns required by the private validator

Genie Agent
  -> NO access to mad_data_lab_private / case_truth

Browser/frontend
  -> NO direct access
```

If the implementation instead packages a server-only private truth fixture/config for the synthetic challenge Case, it must remain outside the frontend/static bundle and Genie configuration and must pass the same dependency/leak scans. Pick **one** truth repository strategy and document it; do not maintain divergent live/fixture truth definitions.

Create a narrow interface such as:

```text
PrivateCaseOracle.get_prediction_key(case_id, stage)
PrivateCaseOracle.get_verdict_constraints(case_id)
```

The normal evidence repository cannot import the oracle. The Genie package cannot import the oracle. Public API DTOs cannot serialize oracle models.

Live staging permission tests must prove:

1. App backend/private validator can obtain the Case #042 truth constraint needed for scoring/validation;
2. Genie still cannot query private truth;
3. public/curated evidence paths continue to work;
4. the frontend/static package contains no truth fixture or private-oracle serialization.

Add `MDL4-TRUTH-001..010` covering dependency boundaries, App allow, Genie deny, frontend deny, public DTO exclusion, prediction correctness lookup, verdict constraint lookup, no Experiment selection access, no logging of truth payload, and no production fixture divergence.

### Scientific Verdict DTO and validation contract

Genie proposes a concise synthesis, but the accepted public verdict is constructed from **validated evidence plus validated Genie synthesis**, not raw model prose. Use a closed server DTO equivalent to:

```json
{
  "primary_explanation": {
    "id": "SOURCE_RECORD_CHANGE",
    "status": "SUPPORTED",
    "summary": "V2 source-record changes are the primary explanation."
  },
  "hypotheses": [
    {"id": "H1", "status": "SUPPORTED"},
    {"id": "H2", "status": "RULED_OUT"},
    {"id": "H3", "status": "POSSIBLE"}
  ],
  "reconciliation": {
    "total_deviation": "-6.80",
    "v2_source_changes": "-5.90",
    "other_component_effects": "-0.90",
    "dq_overlapping_impact": "-0.30",
    "unreconciled": "0.00"
  },
  "formula_changed": false,
  "dq_primary": false,
  "scientist_line": "The formula is ruled out. V2 source changes reconcile to -€5.9M, while the DQ warning is real but too small and overlapping to explain the anomaly."
}
```

Money shown here is illustrative JSON contract text; implementation must use the repository's Decimal serialization convention and one display formatter.

Validation rejects a Genie synthesis that:

- claims formula changed;
- claims DQ is primary;
- says DQ does not exist;
- says V2 explains the full `-6.8M` rather than `-5.9M`;
- treats the overlapping `-0.3M` DQ estimate as additive;
- leaves a non-zero residual when validated evidence reconciles to zero;
- upgrades broad H1 to unsupported certainty;
- contains an unknown status/Experiment/Instrument/control object;
- references evidence not collected/unlocked in the session;
- includes hidden-truth wording not supported by visible evidence.

The server may make a bounded conclusion-repair request through MDL-3's protocol rules when the synthesis is structurally fixable. It must never rewrite a materially contradictory conclusion into the expected answer without a valid Genie synthesis/evidence path and then claim Genie produced it.

Add `MDL4-VERDICT-001..016` covering all fields above, correct Case #042 acceptance, each contradiction class, repair semantics, private-truth boundary, Decimal serialization, and public DTO leakage.

### Canonical Case #042 final status semantics

The V3 specification distinguishes statement granularity:

```text
Changed V2 source records:
  CONFIRMED at record-impact level
  SUPPORTED as the broader primary business explanation if appropriate

Formula changed:
  RULED_OUT

DQ warning:
  POSSIBLE as a real signal
  insufficient/materially unable to explain the primary anomaly
```

Do not simplify the DQ issue to `RULED_OUT` merely because it is not primary. Its existence is real; the causal-primary claim is what is rejected.

## Reconciliation requirement

Before the Scientific Verdict, show/validate:

```text
Total deviation            -6.8M
V2 source changes           -5.9M
Other component effects     -0.9M
Unreconciled                 0.0M
```

Where:

```text
-1.2 + 0.3 = -0.9
```

The DQ -0.3M is not additive because it overlaps V2 evidence.

## Scoring implementation

Replace all hardcoded scores with one deterministic server-side scoring function.

Maximum: 1,000 points.

Implement exactly:

```text
Start Investigation                   +50
First prediction submitted            +50
First prediction correct             +100
Each required Experiment completed   +100, capped at +300
Inspect high-value evidence item      +100
Open required lineage/comparison      +75
Correct final prediction             +200
Finish debrief                        +125
Each hint                              -50
Reveal conclusion before final prediction -150
```

Clamp to `[0, 1000]`.

### Important Experiment scoring interpretation

The scoring spec caps required Experiment completion points at +300 even if Case #042 uses more analytical Experiments. Implement the cap exactly. Do not award +100 for all five and exceed the defined score model.

The scoring projection awards +100 for the **first three unique completed Experiment families that are marked `required_for_completion` by the active Case contract**, in event order. Later required Experiment completions still append normal Experiment events but create a zero-point score audit entry with reason `REQUIRED_EXPERIMENT_CAP_REACHED`. Re-running or revisiting one family never consumes another scoring slot.

### Canonical score-event registry

Implement one closed score-event enum and one pure scoring reducer. For Case #042 the registry is:

| Score event | Points | Eligibility key / rule |
|---|---:|---|
| `START_INVESTIGATION` | +50 | once per session after valid start |
| `INITIAL_PREDICTION_SUBMITTED` | +50 | once when valid initial prediction accepted |
| `INITIAL_PREDICTION_CORRECT` | +100 | once if private oracle says initial choice correct |
| `REQUIRED_EXPERIMENT_COMPLETED` | +100 | max 3 unique required Experiment families |
| `HIGH_VALUE_EVIDENCE_INSPECTED` | +100 | Case #042 exact high-value record capability, once |
| `REQUIRED_LINEAGE_OPENED` | +75 | Case-required lineage/comparison capability, once |
| `FINAL_PREDICTION_CORRECT` | +200 | once if private oracle says final choice correct |
| `FINISH_DEBRIEF` | +125 | once on valid Debrief transition |
| `HINT_REVEALED` | -50 | each unique valid hint, max Case hint count |
| `EARLY_REVEAL` | -150 | once, only on legal early-reveal transition |

Every score event records:

```text
score_event_id
source_event_id
score_type
points
eligibility_key
reason_code
created_at
```

The reducer sorts/consumes events by Investigation event sequence and clamps the final result to `[0,1000]`. It must produce the same score during event replay. There is no route that accepts `points` from the browser.

### Score privacy during the Investigation

Before Scientific Verdict, public responses contain neither score total nor correctness-dependent score events. The UI may show qualitative progress such as `Evidence collected` but not a numerical running score.

At accepted Scientific Verdict, the server may return:

```text
score_before_debrief
score_breakdown_revealed = true
```

At Debrief it returns the final score after +125. This is the first time the initial prediction correctness may be revealed through the score breakdown.

### Exact Case #042 golden score scenarios

These named fixtures are mandatory and are calculated from the locked score formula:

| Scenario | Final score | Notes |
|---|---:|---|
| `PERFECT` | **1000** | correct initial + correct final + first 3 required Experiment points + TX-004291 + required lineage + no hints + Debrief |
| `WRONG_INITIAL_CORRECT_FINAL` | **900** | same as perfect but no +100 initial-correct bonus |
| `ONE_HINT` | **950** | perfect path with one unique hint |
| `ALL_THREE_HINTS` | **850** | perfect path with all three unique hints |
| `SKIP_HIGH_VALUE_RECORD` | **900** | otherwise perfect but TX-004291 detail not opened |
| `EARLY_REVEAL_CORRECT_INITIAL` | **650** | correct initial, all 3 Experiment-scoring slots, high-value evidence, required lineage, no final-prediction +200, -150 early reveal, +125 Debrief |
| `EARLY_REVEAL_WRONG_INITIAL` | **550** | same early-reveal path without initial-correct +100 |

A path that completes all five required Experiments still receives only +300 total Experiment points. Extra optional Experiment runs do not increase score.

Create `tests/golden/score_case_0042.yaml` or equivalent with the exact event sequence/expected total for every scenario above. Add `MDL4-SCORE-001..020` covering registry closure, replay determinism, privacy, cap behavior, all seven golden scenarios, idempotency, clamp behavior, no client points, and score breakdown reveal timing.

### Idempotency

Score events must be idempotent.

Examples:

- refreshing Evidence Explorer does not award +100 twice;
- repeated identical hint request does not subtract twice;
- retrying an Experiment POST with the same idempotency key does not award completion twice;
- revisiting lineage does not award +75 again.

## Hint system

Case #042 has exactly these progressive hints:

1. `Look for the component with the largest absolute contribution.`
2. `V2 explains most of the deviation. What changed underneath it?`
3. `Compare the V2 source snapshot and reconcile its record-level impact.`

Rules:

- derive from visible evidence/Case metadata, not hidden truth fields directly;
- maximum three hints;
- each new hint costs 50 points once;
- repeated retrieval of the same hint is idempotent;
- hints do not automatically change hypothesis status.

Hint availability must never leak future evidence. Encode prerequisites in the Case contract:

```text
HINT_042_01
  text: Look for the component with the largest absolute contribution.
  available_after: INITIAL_PREDICTION_SUBMITTED

HINT_042_02
  text: V2 explains most of the deviation. What changed underneath it?
  available_after: COMPONENT_DECOMPOSITION completed

HINT_042_03
  text: Compare the V2 source snapshot and reconcile its record-level impact.
  available_after: COMPONENT_DECOMPOSITION completed
  requires_prior_hint: HINT_042_02
```

If the next progressive hint is not yet eligible, return `HINT_NOT_YET_AVAILABLE` and charge **0** points. The server never substitutes a hidden-truth-derived alternative hint. Each accepted unique hint appends one `HINT_REVEALED` event and one -50 score event.

Add `MDL4-HINT-001..010` for exact text, prerequisites, progressive order, no early leakage, no fourth hint, zero charge on blocked request, idempotency, replay, no status mutation, and Case namespace isolation.

## Canonical badges

Replace the prototype hardcoded badges with the seven V3 badges:

### Data Apprentice

Complete one Case.

### Metric Scientist

Complete any Case with score >= 800.

### Evidence Analyst

Inspect the Case's required source evidence and lineage/comparison evidence before verdict.

### Skeptical Scientist

Correctly reject a high-salience but materially insufficient signal as the primary explanation.

### Case Collector

Complete three different Cases.

### Lab Veteran

Complete five different Cases.

### Reconciliation Master

Complete the Level 3 multi-cause Case with zero unreconciled amount and no reveal penalty.

For challenge Case #042, only badges whose conditions can genuinely be satisfied should be awarded. Do not display impossible badges as earned.

### Machine-readable badge predicates

Badges are pure functions of validated completion/progression events, not labels sent by the browser. Lock predicates as follows:

```text
DATA_APPRENTICE
  unique completed Cases >= 1

METRIC_SCIENTIST
  any completed Case final_score >= 800

EVIDENCE_ANALYST
  before verdict, player explicitly inspected the Case high-value/source evidence required by this badge
  AND explicitly opened the Case required lineage/comparison evidence

SKEPTICAL_SCIENTIST
  Case contract declares a high-salience materially-insufficient signal
  AND player inspected that signal's evidence
  AND player submitted a final prediction that rejects that signal as primary
  AND accepted verdict validates that the signal is non-primary/insufficient
  (early reveal without a final prediction does not earn this badge)

CASE_COLLECTOR
  unique completed Cases >= 3

LAB_VETERAN
  unique completed Cases >= 5

RECONCILIATION_MASTER
  completed LEVEL_3 multi-cause Case
  AND final unreconciled amount = 0 within Case tolerance
  AND no EARLY_REVEAL event
```

For Case #042 specifically:

- `DATA_APPRENTICE` is earned on first valid completion;
- `METRIC_SCIENTIST` is earned when final score >=800;
- `EVIDENCE_ANALYST` requires TX-004291 detail **and** the required V2 lineage/comparison action before verdict;
- `SKEPTICAL_SCIENTIST` requires DQ evidence inspection plus final `FINAL_CHANGED_V2_SOURCE_RECORDS`;
- `CASE_COLLECTOR`, `LAB_VETERAN`, `RECONCILIATION_MASTER` cannot be earned from #042 alone.

Badge order in DTO/UI is canonical and stable:

```text
DATA_APPRENTICE
METRIC_SCIENTIST
EVIDENCE_ANALYST
SKEPTICAL_SCIENTIST
CASE_COLLECTOR
LAB_VETERAN
RECONCILIATION_MASTER
```

Add `MDL4-BADGE-001..018` covering all predicates, threshold boundaries, early-reveal non-award, unique-Case counting, replay/no duplicate, Case #042 attainable/unattainable set, and stable ordering.

## Case system, difficulty, canonical catalog, and release-state contract

MDL-4 is the primary closure owner for V3 §15. The application must present a reusable Case universe even though challenge reliability takes priority over shipping multiple playable Cases.

### Difficulty semantics

Store difficulty as data, not UI decoration:

**LEVEL_1 — Clean Case**

- one primary cause;
- strong signal;
- little/no misleading noise;
- normally 2–3 Experiments;
- purpose: onboarding/smoke reliability.

**LEVEL_2 — Noisy Case**

- one primary cause;
- at least one plausible secondary signal;
- normally 3–5 Experiments;
- reconciliation plus at least one ruled-out/insufficient competing explanation;
- purpose: core MAD DATA LAB experience; Case #042 is Level 2.

**LEVEL_3 — Multi-Cause Case**

- two independent causes for the first release design;
- several plausible explanations;
- branching investigation;
- 4–7 normal Experiments;
- 100% impact reconciliation;
- purpose: advanced/finale/stretch, not challenge release dependency.

The frontend must not infer difficulty from public number or hardcoded Case IDs.

### Canonical catalog metadata

The server-owned catalog must preserve these V3 identities/states even if only #042 is playable:

| Case | Title | Difficulty | Primary lesson | Primary cause/design | V3 challenge state |
|---|---|---:|---|---|---|
| #042 | The Missing €6.8M | L2 | decomposition + snapshots + skepticism | source-record change | CORE/demo |
| #107 | Attack of the Clones | L1 | duplicates + row counts + pipeline replay | duplicate ingestion | TARGET |
| #213 | The Vanishing Revenue | L2 | filters + semantic logic + lineage | filter change | TARGET |
| #314 | The Ghost Records | L2 | missing rows vs business impact | missing records | FULL_GAME |
| #441 | The Red Herring | L2 | DQ count vs materiality | source change, DQ distractor | FULL_GAME |
| #520 | The Impossible Forecast | L2 | joins + entity mix/population | join cardinality/entity mix | FULL_GAME |
| #812 | Double Trouble | L3 | multi-cause reconciliation | source change + logic change | STRETCH FINALE |

`release_state` is metadata; `availability` is computed server-side from release state, feature flags/review mode, progression, and whether that Case has passed its own implementation gates. A TARGET Case is not automatically AVAILABLE.

### Canonical progression graph

Represent prerequisites in catalog/template data, not frontend conditionals:

```text
Case #042 -> Case #107 -> Case #213
                     \-> Case #314
Case #213 + Case #314 -> Case #441
Case #441 -> Case #520
Case #520 -> Case #812
```

For the challenge build:

- Case #042 is always available;
- an actually shipped/validated secondary Case may be exposed directly in `CHALLENGE_REVIEW_MODE` so judges are not forced to grind unlocks;
- review mode changes availability only, never completion/best-score persistence;
- locked/coming-soon Cases may remain visible as product universe;
- unlock state is cosmetic progression, never a security boundary;
- a deep link to a valid but unreleased Case returns `CASE_UNAVAILABLE`, not evidence/session creation;
- unknown Case ID returns distinct not-found behavior.

### Case completion contract

Generic completion is based on Case/template evidence requirements, not “five Experiments”. A Case may conclude only when:

```text
required evidence tags collected
blocking Experiments resolved
reconciliation residual within tolerance
final epistemic states satisfy Case rules
valid Genie CONCLUDE protocol available/validated
backend independently validates numeric conclusion
```

The explicit MDL-4 early-reveal path may skip the **player's final prediction**, but it does not skip any of the analytical completion requirements above.

`INSUFFICIENT_EVIDENCE` as a scientific conclusion is valid only when the Case/template allows it and the visible/golden oracle intentionally supports that outcome. Do not use it as a generic escape hatch for a broken query.

### Secondary-Case scope rule

Do not implement a secondary Case merely to satisfy the catalog table. A secondary Case becomes challenge-playable only after its own deterministic fixture, Genie path, fake E2E path, live benchmark coverage, instrument coverage, and release soak threshold from V3 are green. Until then, its conditional tests remain `CONDITIONAL_NOT_SHIPPED` and availability remains locked/coming soon.

### Case/progression tests — iteration-specific

Add:

- `MDL4-CASE-001` — canonical seven public Case IDs/numbers/titles are unique and match catalog schema;
- `MDL4-CASE-002` — Case #042 difficulty is LEVEL_2 and always available in challenge build;
- `MDL4-CASE-003` — TARGET release state alone does not make #107/#213 available;
- `MDL4-CASE-004` — canonical prerequisite graph is cycle-free and references known Cases;
- `MDL4-CASE-005` — challenge review mode exposes only independently enabled shipped Cases and does not mutate completion;
- `MDL4-CASE-006` — valid unreleased Case deep-link returns CASE_UNAVAILABLE with no session/evidence creation;
- `MDL4-CASE-007` — unknown Case returns not-found rather than silently falling back to #042;
- `MDL4-CASE-008` — generic completion uses evidence/contract state, not fixed Experiment count;
- `MDL4-CASE-009` — Level 3 fixture can represent two contributions/statuses without forcing single-root-cause UI/state;
- `MDL4-CASE-010` — disabled secondary Case cannot become available merely because local storage/progression is forged.


## Progression

Implement lightweight progression without turning it into authorization.

Persist only:

```text
completed Case IDs
best score by Case
earned badges
audio/motion preferences
```

Do not persist:

```text
hidden truth
raw Genie responses
credentials
secret tokens
```

Server validates actual Case completion before accepting progression/unlock updates.

Challenge Review Mode may expose shipped secondary TARGET Cases later, but it must not mark them completed or alter saved progression.

### Challenge-MVP progression authority

Do not add a database solely for progression in MDL-4. Use the smallest coherent model:

- the active backend process keeps the authoritative progression projection for the current anonymous profile/session context;
- the client may mirror only the safe progression DTO in local storage for presentation continuity;
- the client cannot submit `earned_badges`, `best_score`, or `completed=true` as authoritative facts during a Case;
- completion/badge/best-score changes originate only from a valid `DEBRIEF_ENTERED` transition for a server-validated Investigation;
- after a backend restart, a lost in-memory profile is an acceptable challenge-MVP limitation if documented; the app must fail/recover cleanly rather than trusting arbitrary browser state as analytical truth;
- local progression never bypasses `release_state`, server feature flags, or `CASE_UNAVAILABLE`;
- if a later iteration adds a restore/normalization mechanism, restored state remains cosmetic and must obey known Case IDs, score bounds, unique completions, and prerequisite graph.

Use stable DTO shape compatible with V3:

```json
{
  "completed_case_ids": ["CASE_0042"],
  "best_scores": {"CASE_0042": 900},
  "earned_badges": ["DATA_APPRENTICE", "METRIC_SCIENTIST"],
  "unlocked_case_ids": ["CASE_0042", "CASE_0107"]
}
```

For a fresh profile:

```text
completed_case_ids = []
best_scores = {}
earned_badges = []
unlocked_case_ids includes CASE_0042
```

After a valid #042 Debrief, the default progression graph makes #107 unlocked **only if #107 is independently shipped/enabled**; otherwise its public availability remains `COMING_SOON`/unavailable even though the progression prerequisite is satisfied. This separates progression eligibility from release readiness.

Add `MDL4-PROG-001..014` covering fresh profile, completion mutation source, best-score max, replay no unique increment, #107 prerequisite, release-readiness override, review mode non-persistence, forged client badge/score rejection, restart limitation, unknown Case cleanup, stable ordering, local-cache non-authority, Case Collector threshold, and Lab Veteran threshold.

## Frontend page/component tasks

Implement or complete:

### Case Board

- server-supplied Case cards;
- availability state;
- completion/best score;
- keyboard-accessible full card action;
- Case #042 featured.

### Case Briefing

Show:

```text
CASE #042
THE MISSING EUR 6.8M
Expected 125.0M
Observed 118.2M
Deviation -6.8M
```

All numeric values from API.

### Hypothesis Board

Each card:

```text
ID
title
one-line rationale
initial priority
current status once evidence begins
evidence chips
```

### Prediction UI

Use an accessible group/select/radio implementation with labels and keyboard support.

### Experiment Selection transition

Show:

```text
Genie is choosing the next Experiment
Comparing hypotheses...
Selecting the highest-information test...
```

Then selected Experiment/Instrument and a short externally useful rationale.

Do not expose chain-of-thought.

### Experiment Result shell

Render from Instrument registry data rather than Case-specific page routing.

### Scientific Verdict

Show final hypotheses, reconciliation, evidence stack, score, and Debrief action.

### Debrief

Show:

- score;
- best score;
- initial prediction;
- final prediction;
- hints used;
- evidence inspected;
- learned concepts;
- earned badges;
- actions Back to Case Board / Replay Case / Open Next Case when available.

Required closing line:

```text
We did not ask for an answer. We ran an investigation.
```

### Case unavailable / not-found states

Implement the V3 unavailable screen shell now:

- valid but unreleased/locked Case -> title/public art if safe, release/availability explanation, Back to Case Board;
- unknown Case -> distinct not-found message and Back to Case Board;
- neither state creates a session or fetches Case evidence;
- deep-link browser Back/Forward behavior remains deterministic.

### Score-visibility UI rule

Do not render a live numerical score during the Investigation. Before verdict, the UI may show non-numeric progress only. At Scientific Verdict, render the server-returned `score_before_debrief` and breakdown with prediction correctness now revealed. After the explicit Debrief transition, render the final score including +125.

A client-side arithmetic reconstruction of score is forbidden. The frontend only formats values returned by the server after the appropriate reveal stage.

### Early-reveal confirmation UI

The early-reveal action appears only when the server projection says analytical completion is satisfied and final prediction is still absent.

Button copy must make the consequence explicit, for example:

```text
Reveal Scientific Verdict now (-150)
```

Confirmation must state that the final prediction will be skipped. Cancel causes no event/penalty. The confirm dialog must use the application's accessible dialog/focus behavior; Escape/cancel restores focus to the initiating control.

### Functional shell versus MDL-5 visual polish

MDL-4 must make every required screen **functionally complete** using registry-driven Instrument shells and the approved iteration art. MDL-5 remains responsible for final Instrument visualization design, Evidence Explorer polish, semantic visual tokens, responsive refinements, visual regression baselines, and the full production art/instrument pass.

Do not leave MDL-4 screens as dead placeholders merely because MDL-5 owns polish: every Case #042 action required by E2E must be operable, labeled, typed, and testable now. Conversely, do not duplicate MDL-5 by embedding hardcoded one-off charts directly in MDL-4 pages.

## Client state rules

The server is authoritative for:

```text
phase
hypotheses
experiment history
evidence
score
hints used
verdict
```

The client owns only presentation state:

```text
open panel
selected evidence row
filters
audio
reduced motion
animation finished
```

No optimistic analytical updates.

Disable primary action while a state-changing request is active.

Use idempotency keys for state-changing POSTs if repeated browser submission is possible.

## Refresh behavior — exact MDL-4 policy

Use this policy for the challenge MVP:

1. the browser keeps only the opaque `session_id` and safe presentation preferences needed to reconnect;
2. on page load/refresh inside an active Investigation, call `GET /api/sessions/{session_id}`;
3. if the session exists, render exactly from the returned server projection/state revision;
4. never reconstruct analytical state from browser-local experiment/history arrays;
5. if the process/session expired, receive `SESSION_EXPIRED`/`SESSION_NOT_FOUND` and show a dedicated recovery state with **Restart Investigation** and **Back to Case Board**;
6. restart creates a new session/conversation and never reuses the expired session ID;
7. browser Back/Forward navigation changes presentation route only; it cannot roll the server state backward;
8. a stale page attempting a state-changing action receives `STATE_REVISION_CONFLICT` and refreshes the projection.

Do not add a heavy persistent database just for refresh resilience unless a later iteration deliberately changes the architecture.

Add `MDL4-REFRESH-001..010` for refresh at briefing, hypotheses, after Experiment, evidence detail, final-prediction stage, verdict, Debrief, expired session, browser Back, and stale-state action conflict.

## Tests required to close MDL-4

### Scoring domain tests

Implement:

- DU-004 score starts zero;
- DU-005 clamp minimum;
- DU-006 clamp maximum;
- DU-007 hint deduction exactly once;
- DU-008 duplicate hint idempotency;
- DU-009 early reveal penalty;
- DU-010 Data Apprentice;
- DU-011 Metric Scientist threshold;
- DU-012 Evidence Analyst conditions;
- DU-013 Skeptical Scientist conditions.

Also add tests for Case Collector, Lab Veteran, Reconciliation Master even if not attainable in #042.

### State and verdict tests

Test:

- initial prediction required before normal next Experiment flow;
- initial and final predictions stored separately;
- wrong initial prediction does not block completion;
- final prediction blocked until Case completion prerequisites;
- `Insufficient evidence` accepted as a valid player option;
- conclusion blocked if formula check missing;
- conclusion blocked if reconciliation residual outside tolerance;
- normal conclusion blocked if final prediction missing;
- explicit early reveal allowed only after analytical completion and applies `-150` exactly once;
- early reveal records final prediction as skipped rather than fabricating a choice;
- early reveal before required evidence remains blocked;
- retried/idempotent early reveal cannot double-penalize;
- no DQ double count;
- private truth validator never imported into Genie client/prompt modules;
- verdict rejects invented unsupported causal claim;
- exact #042 final expected statuses accepted;
- score not client-supplied.

### API tests

Implement/complete API-003 through API-033 as applicable, especially:

- start session;
- duplicate start handling;
- prediction legal stage;
- invalid hypothesis rejected;
- next happy path;
- next illegal state;
- evidence pagination and limit;
- hint progression and no fourth hint;
- conclusion blocked early;
- conclusion succeeds when complete;
- stable request ID/error envelope;
- duplicate `/next` race does not duplicate event;
- chat max length now exactly per V3 contract;
- progression best score keeps maximum;
- invalid completion cannot unlock Case;
- session Case immutable;
- evidence cannot cross Case boundary.

### Frontend component tests

Implement/complete:

- Case Board server-driven states;
- Case card accessible name;
- briefing uses selected Case API metadata;
- hypothesis statuses include text;
- prediction labels accessible;
- primary action disabled during request;
- no double submit;
- score renders only server value;
- Debrief shows initial and final predictions;
- impossible badges not falsely shown;
- generic Experiment Result renders registered Instrument model.

### Fake-Genie E2E

Implement at minimum:

- E2E-001 complete best/perfect-style path;
- E2E-002 wrong initial prediction still completes;
- E2E-003 one-hint path;
- E2E-004 all-hints path;
- E2E-005 early reveal penalty path (mandatory; this closes the canonical -150 score event);
- E2E-006 optional source record skip behavior according to Case required tags;
- E2E-007 evidence filter MODIFIED;
- E2E-008 search TX-004291;
- E2E-011/012 refresh policy;
- E2E-013 repair success;
- E2E-014 repair twice -> explicit fallback/error path;
- E2E-019 reconciliation failure blocks conclusion;
- E2E-027 double-click next;
- E2E-028 browser back does not corrupt state;
- E2E-030 offline fixture mode disabled in production build;
- E2E-MC-001 board -> #042 -> verdict -> board;
- E2E-MC-002 completion state visible;
- E2E-MC-005 cross-Case abandonment isolation;
- E2E-MC-006 locked Case UX.

A fake-Genie happy path must be able to run in CI without Databricks network access.

## MDL-4 custom deterministic test registry

Every custom ID below has exactly one canonical definition. Tests may be parameterized, but the release report must map each ID to at least one executed assertion/result. A range reference elsewhere in this document means **all** IDs in the range, not “one representative test.”

### Pending Genie decision integration

| ID | Required assertion |
|---|---|
| `MDL4-DECISION-001` | valid first Genie selection from `/start` is persisted as one pending decision |
| `MDL4-DECISION-002` | first legal `/next` consumes the exact pending decision without a second selection call |
| `MDL4-DECISION-003` | validated next selection returned after an Experiment is queued once for the following action |
| `MDL4-DECISION-004` | pending decision becomes stale/rejected when current allowed-set/state contract no longer permits it |
| `MDL4-DECISION-005` | query/result retry executes evidence for the already-selected Experiment and does not reselect |
| `MDL4-DECISION-006` | concurrent `/next` requests cannot consume/execute one pending decision twice |
| `MDL4-DECISION-007` | when no pending decision exists, `/next` requests exactly one new Genie selection and persists it |
| `MDL4-DECISION-008` | browser request cannot inject/overwrite Experiment or pending-decision identity |

### Completion and evidence entitlement

| ID | Required assertion |
|---|---|
| `MDL4-COMP-001` | Case #042 blocking Experiment set is exactly the five locked required families |
| `MDL4-COMP-002` | legal DQ/formula/other allowed ordering does not change completion correctness |
| `MDL4-COMP-003` | dedicated `SOURCE_RECORD_INSPECTION` Experiment is optional for #042 completion |
| `MDL4-COMP-004` | skipping TX-004291 detail does not block conclusion eligibility |
| `MDL4-COMP-005` | required V2 lineage/comparison inspection does block final-prediction eligibility until opened |
| `MDL4-COMP-006` | missing FORMULA_VALIDATION blocks completion |
| `MDL4-COMP-007` | missing DQ_MATERIALITY blocks completion |
| `MDL4-COMP-008` | total reconciliation residual outside 0.01 tolerance blocks completion |
| `MDL4-COMP-009` | V2 snapshot residual outside 0.01 tolerance blocks completion |
| `MDL4-COMP-010` | duplicate completion of one required Experiment family cannot satisfy another family |
| `MDL4-COMP-011` | public missing-requirement list exposes safe requirement codes but no root-cause/truth oracle |
| `MDL4-COMP-012` | exact valid #042 event/evidence state becomes ready for final prediction |

### Session, event log, revision, TTL, and capacity

| ID | Required assertion |
|---|---|
| `MDL4-SESSION-001` | session IDs are unguessable and Case ID immutable |
| `MDL4-SESSION-002` | event sequence starts at 1 and increases by exactly one per append |
| `MDL4-SESSION-003` | public `state_revision` always equals latest event sequence |
| `MDL4-SESSION-004` | stale non-idempotent state-changing action returns `STATE_REVISION_CONFLICT` |
| `MDL4-SESSION-005` | exact idempotent replay succeeds even when the session revision has advanced because of that original action |
| `MDL4-SESSION-006` | same idempotency key with different canonical action/body returns `IDEMPOTENCY_CONFLICT` |
| `MDL4-SESSION-007` | session expiration returns `SESSION_EXPIRED`/documented equivalent and never partial state |
| `MDL4-SESSION-008` | expired idempotency records cannot resurrect an expired Investigation |
| `MDL4-SESSION-009` | active-session capacity limit fails new creation explicitly and does not evict an active session |
| `MDL4-SESSION-010` | process-local session store plus multi-worker production config fails repository/package guard |
| `MDL4-SESSION-011` | replaying the complete event log reconstructs phase/predictions/evidence/score/completion exactly |
| `MDL4-SESSION-012` | direct mutation of historical event payload/list through domain API is impossible/rejected |

### API extensions and error semantics

| ID | Required assertion |
|---|---|
| `MDL4-APIEXT-001` | `GET /sessions/{id}` reconstructs the safe current screen projection without Genie/SQL call |
| `MDL4-APIEXT-002` | session read returns no correctness/score oracle before verdict |
| `MDL4-APIEXT-003` | unknown session -> stable `SESSION_NOT_FOUND` mapping |
| `MDL4-APIEXT-004` | expired session -> stable `SESSION_EXPIRED` mapping |
| `MDL4-APIEXT-005` | evidence-inspect rejects evidence not unlocked by current session |
| `MDL4-APIEXT-006` | evidence-inspect rejects evidence from another Case/session |
| `MDL4-APIEXT-007` | evidence-inspect resolves high-value/lineage reward server-side; client reward flags ignored/rejected |
| `MDL4-APIEXT-008` | repeated evidence-inspect cannot double-score |
| `MDL4-APIEXT-009` | `/debrief` before accepted verdict returns `DEBRIEF_NOT_READY` |
| `MDL4-APIEXT-010` | valid `/debrief` appends exactly one Debrief event and +125 |
| `MDL4-APIEXT-011` | repeated `/debrief` cannot re-award points/progression |
| `MDL4-APIEXT-012` | normal conclude requires final prediction; early-reveal mode is never inferred from missing fields |
| `MDL4-APIEXT-013` | error registry maps each locked code to the documented HTTP/retryable semantics |
| `MDL4-APIEXT-014` | `Idempotency-Key` length/format/body canonicalization rules enforced |
| `MDL4-APIEXT-015` | state-changing endpoints require revision semantics except session creation |
| `MDL4-APIEXT-016` | `/chat` control-looking JSON cannot mutate gameplay state or score |
| `MDL4-APIEXT-017` | chat token bucket enforces configured rate/burst without affecting Experiment APIs |
| `MDL4-APIEXT-018` | OpenAPI/generated client documents all MDL-4 extension endpoints, headers, enums, and errors |

### Private truth boundary

| ID | Required assertion |
|---|---|
| `MDL4-TRUTH-001` | `backend/genie/**` cannot import private oracle modules |
| `MDL4-TRUTH-002` | normal public/curated evidence repository cannot import/use private oracle for Experiment evidence |
| `MDL4-TRUTH-003` | configured App backend validator can obtain only the required #042 private scoring/verdict constraint |
| `MDL4-TRUTH-004` | Genie identity/resource cannot query private truth after MDL-4 permission change |
| `MDL4-TRUTH-005` | frontend/static production package contains no private truth fixture/oracle serialization |
| `MDL4-TRUTH-006` | public Pydantic/OpenAPI DTOs contain no private oracle fields |
| `MDL4-TRUTH-007` | private initial prediction key resolves to `PRED_SOURCE_VALUES_CHANGED` for #042 |
| `MDL4-TRUTH-008` | private final prediction key resolves to `FINAL_CHANGED_V2_SOURCE_RECORDS` for #042 |
| `MDL4-TRUTH-009` | private oracle is not consulted by allowed-Experiment/Genie-selection code paths |
| `MDL4-TRUTH-010` | logs/release artifacts do not serialize full private truth; live and fixture oracle sources cannot diverge silently |

### Verdict validation

| ID | Required assertion |
|---|---|
| `MDL4-VERDICT-001` | exact evidence-grounded Case #042 verdict is accepted |
| `MDL4-VERDICT-002` | broad H1 accepted final status is `SUPPORTED` |
| `MDL4-VERDICT-003` | H2 final status must be `RULED_OUT` with evidence reason |
| `MDL4-VERDICT-004` | H3 final status remains `POSSIBLE` while non-primary/insufficient |
| `MDL4-VERDICT-005` | V2 source-change amount must be `-5.90`, not total `-6.80` |
| `MDL4-VERDICT-006` | other component effects must reconcile to `-0.90` |
| `MDL4-VERDICT-007` | DQ `-0.30` is represented as overlapping/non-additive |
| `MDL4-VERDICT-008` | final unreconciled amount is `0.00` within tolerance |
| `MDL4-VERDICT-009` | verdict claiming formula changed is rejected |
| `MDL4-VERDICT-010` | verdict claiming DQ is primary is rejected |
| `MDL4-VERDICT-011` | verdict claiming the DQ issue does not exist is rejected/made non-acceptable |
| `MDL4-VERDICT-012` | unsupported broad H1 `CONFIRMED` overclaim is rejected or normalized only through allowed repair path |
| `MDL4-VERDICT-013` | verdict cannot cite evidence not collected/visible in the session |
| `MDL4-VERDICT-014` | one structurally repairable conclusion may be repaired through the MDL-3 bounded protocol and revalidated |
| `MDL4-VERDICT-015` | second/materially contradictory failure returns explicit error; backend does not author the expected answer and attribute it to Genie |
| `MDL4-VERDICT-016` | public verdict Decimal/status serialization is stable and truth-free |

### Scoring

| ID | Required assertion |
|---|---|
| `MDL4-SCORE-001` | closed score-event registry/reducer is deterministic under event replay |
| `MDL4-SCORE-002` | fresh session score projection starts at 0 privately |
| `MDL4-SCORE-003` | `PERFECT` golden scenario final score = 1000 |
| `MDL4-SCORE-004` | `WRONG_INITIAL_CORRECT_FINAL` = 900 |
| `MDL4-SCORE-005` | `ONE_HINT` = 950 |
| `MDL4-SCORE-006` | `ALL_THREE_HINTS` = 850 |
| `MDL4-SCORE-007` | `SKIP_HIGH_VALUE_RECORD` = 900 |
| `MDL4-SCORE-008` | `EARLY_REVEAL_CORRECT_INITIAL` = 650 |
| `MDL4-SCORE-009` | `EARLY_REVEAL_WRONG_INITIAL` = 550 |
| `MDL4-SCORE-010` | five required Experiment completions award at most +300 total |
| `MDL4-SCORE-011` | duplicate same-family Experiment completion awards no duplicate completion points |
| `MDL4-SCORE-012` | TX-004291 high-value reward awards +100 at most once |
| `MDL4-SCORE-013` | required lineage/comparison reward awards +75 at most once |
| `MDL4-SCORE-014` | each unique accepted hint charges -50 once; retries do not double-charge |
| `MDL4-SCORE-015` | Debrief awards +125 once and no navigation/retry awards it again |
| `MDL4-SCORE-016` | score clamps to 0 minimum under penalty stress fixture |
| `MDL4-SCORE-017` | score clamps to 1000 maximum under duplicate/extra-event stress fixture |
| `MDL4-SCORE-018` | public API/network payload does not reveal score/correctness during Investigation |
| `MDL4-SCORE-019` | perfect path Scientific Verdict subtotal before Debrief is exactly 875 |
| `MDL4-SCORE-020` | client-supplied points/score/badge fields are rejected/ignored and cannot affect reducer output |

### Hints

| ID | Required assertion |
|---|---|
| `MDL4-HINT-001` | all three Case #042 hint texts exactly match canonical copy |
| `MDL4-HINT-002` | hint 1 becomes available only after initial prediction |
| `MDL4-HINT-003` | hint 2 cannot appear before component decomposition |
| `MDL4-HINT-004` | hint 3 cannot appear before its evidence/prior-hint prerequisite |
| `MDL4-HINT-005` | hint request that is too early returns `HINT_NOT_YET_AVAILABLE` and zero charge |
| `MDL4-HINT-006` | progressive hint order cannot be client-selected/skipped by ID |
| `MDL4-HINT-007` | after hint 3, next request returns `NO_MORE_HINTS` and zero charge |
| `MDL4-HINT-008` | same idempotency key/retrieval cannot charge the same hint twice |
| `MDL4-HINT-009` | revealing a hint does not directly mutate hypothesis status |
| `MDL4-HINT-010` | hints/evidence prerequisites are Case-namespaced and cannot cross sessions |

### Badges

| ID | Required assertion |
|---|---|
| `MDL4-BADGE-001` | Data Apprentice earned on first valid Case completion |
| `MDL4-BADGE-002` | Data Apprentice not earned before valid completion |
| `MDL4-BADGE-003` | Metric Scientist earned at score 800 |
| `MDL4-BADGE-004` | Metric Scientist not earned at score 799 |
| `MDL4-BADGE-005` | Evidence Analyst earned only when required source/high-value evidence and lineage were both inspected before verdict |
| `MDL4-BADGE-006` | Evidence Analyst not earned when high-value/source evidence inspection missing |
| `MDL4-BADGE-007` | Evidence Analyst not earned when lineage/comparison inspection missing |
| `MDL4-BADGE-008` | Skeptical Scientist earned for #042 when DQ evidence inspected and correct non-DQ final prediction accepted |
| `MDL4-BADGE-009` | early reveal without final prediction does not earn Skeptical Scientist |
| `MDL4-BADGE-010` | final DQ-primary prediction does not earn Skeptical Scientist |
| `MDL4-BADGE-011` | Case Collector earned at three unique completed Cases |
| `MDL4-BADGE-012` | replaying one Case does not increase unique completion count |
| `MDL4-BADGE-013` | Lab Veteran earned at five unique completed Cases |
| `MDL4-BADGE-014` | Reconciliation Master requires completed Level 3 multi-cause Case + zero residual + no reveal penalty |
| `MDL4-BADGE-015` | Reconciliation Master not earned when an early-reveal event exists |
| `MDL4-BADGE-016` | #042 alone cannot award Case Collector/Lab Veteran/Reconciliation Master |
| `MDL4-BADGE-017` | badge DTO order matches the canonical seven-badge ordering |
| `MDL4-BADGE-018` | replay/idempotent Debrief does not duplicate earned-badge events |

### Progression

| ID | Required assertion |
|---|---|
| `MDL4-PROG-001` | fresh profile has no completions/scores/badges and Case #042 progression-eligible |
| `MDL4-PROG-002` | progression mutation originates only from server-validated Debrief transition |
| `MDL4-PROG-003` | best score for a Case monotonically keeps maximum |
| `MDL4-PROG-004` | replaying same Case does not increment unique-completion count |
| `MDL4-PROG-005` | #042 completion satisfies #107 progression prerequisite |
| `MDL4-PROG-006` | #107 remains unavailable when not independently shipped even if prerequisite is satisfied |
| `MDL4-PROG-007` | challenge review mode affects availability only and does not mutate completion/best score |
| `MDL4-PROG-008` | client-supplied forged badges/best-score/completion cannot mutate authoritative active-session progression |
| `MDL4-PROG-009` | documented backend restart/profile-loss behavior is clean and does not create phantom completion |
| `MDL4-PROG-010` | unknown/removed Case ID cannot be persisted as a valid completion/unlock |
| `MDL4-PROG-011` | completed/unlocked/badge arrays use deterministic canonical order |
| `MDL4-PROG-012` | local-storage mirror is never used to bypass server release-state/session validation |
| `MDL4-PROG-013` | three unique completions produce Case Collector predicate exactly once |
| `MDL4-PROG-014` | five unique completions produce Lab Veteran predicate exactly once |

### Refresh/navigation

| ID | Required assertion |
|---|---|
| `MDL4-REFRESH-001` | refresh at Case Briefing reconstructs safe session state |
| `MDL4-REFRESH-002` | refresh after hypotheses/initial prediction preserves server state without replaying start |
| `MDL4-REFRESH-003` | refresh after Experiment result preserves event history/current phase |
| `MDL4-REFRESH-004` | refresh while evidence detail is open restores analytical session and safely resets/preserves presentation selection per UI policy |
| `MDL4-REFRESH-005` | refresh at final-prediction stage does not allow skipping/duplicating prediction |
| `MDL4-REFRESH-006` | refresh at accepted Scientific Verdict preserves verdict and hidden score now revealed appropriately |
| `MDL4-REFRESH-007` | refresh in Debrief does not re-award +125/badges/progression |
| `MDL4-REFRESH-008` | expired/lost session shows clean restart/back recovery, no partial reconstruction from local analytics state |
| `MDL4-REFRESH-009` | browser Back/Forward cannot roll authoritative state backward or duplicate requests |
| `MDL4-REFRESH-010` | stale page action receives revision conflict and recovers by refetching projection |

### Closure evidence freshness

| ID | Required assertion |
|---|---|
| `MDL4-EVIDENCE-001` | game-contract digest deterministic for identical tree/input identities |
| `MDL4-EVIDENCE-002` | digest artifact records MDL-2/MDL-3 predecessor contract identities |
| `MDL4-EVIDENCE-003` | fake-E2E artifact rejected when game-contract digest differs |
| `MDL4-EVIDENCE-004` | live-session artifact rejected when implementation/game digest differs |
| `MDL4-EVIDENCE-005` | art-only diff can reuse unaffected game evidence only when classifier proves game digest/runtime rules allow it |
| `MDL4-EVIDENCE-006` | report-only diff can reuse runtime evidence only through inherited exact-content classifier |
| `MDL4-EVIDENCE-007` | unknown path is runtime/game-affecting fail-closed until classified |
| `MDL4-EVIDENCE-008` | final release contract resolves reused evidence to immutable GitHub run/artifact references |

### Live integrated session

| ID | Required assertion |
|---|---|
| `MDL4-LIVE-001` | deployed live harness uses real Genie/real Case #042 curated data with offline/fake disabled |
| `MDL4-LIVE-002` | live start returns canonical three hypotheses and one valid Genie decision |
| `MDL4-LIVE-003` | Experiment loop accepts legal adaptive order and never substitutes expected choices |
| `MDL4-LIVE-004` | live loop reaches all five blocking Experiment families within configured <=8 Experiment bound |
| `MDL4-LIVE-005` | TX-004291 inspection and required lineage inspection succeed only after entitlement |
| `MDL4-LIVE-006` | live final prediction/conclusion yields accepted #042 hypothesis/status/reconciliation semantics |
| `MDL4-LIVE-007` | live Debrief final score = 1000 on zero-hint perfect scripted-player path |
| `MDL4-LIVE-008` | live progression shows #042 completion/best score without direct client mutation |
| `MDL4-LIVE-009` | any trusted SQL fallback is preceded by valid Genie Experiment selection and is recorded |
| `MDL4-LIVE-010` | live artifact contains no raw reasoning/private truth/token and matches accepted digests |

Canonical V3 IDs that MDL-4 executes as regression but whose **primary owner remains elsewhere** must stay marked that way in the global `v3-test-coverage.csv`; running a regression here must not create duplicate primary ownership.

## One-command MDL-4 local gate

Extend the shared iteration runner so a clean checkout can execute the complete deterministic MDL-4 closure suite with one command:

```bash
python scripts/run_iteration_gate.py --iteration MDL-4 --mode local
```

The command must fail non-zero on any missing/zero-test/skipped mandatory stage and produce a machine-readable summary under `release-report/MDL-4/`.

Minimum ordered stages:

```text
01 source/predecessor contract verification
02 repository/spec self-audit
03 Python install/lock verification
04 Node clean install/lock verification
05 Ruff + Python type check
06 TypeScript typecheck + ESLint
07 canonical domain/state/completion/scoring/badge/hint tests
08 Case #042 golden/reconciliation regression suite inherited from MDL-2
09 Genie protocol/fake-adapter regression suite inherited from MDL-3
10 API/OpenAPI/schema-generation contract tests
11 frontend component/unit tests
12 private-truth/import/static leak scans
13 event-replay/idempotency/concurrency tests
14 full fake-Genie Playwright gameplay suite
15 production frontend build
16 production-package/static truth/obsolete-asset scan
17 A03/A06 art preflight and approval-state validation
18 game-contract digest generation/verification
19 release-contract validation
```

`--mode local` may leave the human approval check in a clearly reported `PENDING_HUMAN` state while development is ongoing, but it cannot produce a closure PASS until approval is real/current.

Add closure mode:

```bash
python scripts/run_iteration_gate.py --iteration MDL-4 --mode closure
```

Closure mode additionally requires the immutable GitHub CI references, current human art approval, deployed smoke, one complete live integrated session, and final-head digest agreement. It must never run a hidden mock instead of those external gates.

## GitHub CI requirements

Extend the existing PR workflow without weakening the inherited MDL-1/2/3 checks.

### Stable required-check names

Use one version-controlled list for both workflow job/check names and GitHub branch protection/ruleset configuration. Required MDL-4 check contexts:

```text
mdl4/repository-contract
mdl4/domain-gameplay
mdl4/api-contract
mdl4/frontend
mdl4/e2e-fake-genie
mdl4/security-truth
mdl4/art-preflight
mdl4/human-approval-gate
mdl4/production-package-smoke
mdl4/release-contract
```

Do not define a second differently named branch-protection list elsewhere.

### Required job contents

`mdl4/repository-contract`

- V3/predecessor fingerprints;
- `validate_mdl4_contract.py --strict` where closure-capable;
- Case/catalog/completion-contract schema validation;
- game-contract digest path policy;
- no unresolved executable placeholders.

`mdl4/domain-gameplay`

- state machine;
- event replay;
- completion predicate;
- scoring golden scenarios;
- hints;
- badges;
- progression;
- state revision/idempotency/concurrency.

`mdl4/api-contract`

- canonical API-003..033 owned by MDL-4;
- MDL4-APIEXT suite;
- OpenAPI generation;
- generated frontend schema/client drift check;
- stable error-code/HTTP mapping.

`mdl4/frontend`

- component tests;
- prediction/early-reveal/debrief behavior;
- score hidden until verdict;
- unavailable/deep-link states;
- production build.

`mdl4/e2e-fake-genie`

- critical/full fake-Genie functional Playwright suite;
- all canonical MDL-4-owned E2E paths;
- exact score scenarios;
- browser refresh/back/double-submit;
- failure traces/screenshots uploaded on failure.

`mdl4/security-truth`

- private-oracle dependency guard;
- frontend/static truth scan;
- Genie-import deny;
- no client-authoritative score/status/verdict constants;
- no raw model HTML rendering.

`mdl4/art-preflight`

- 10 candidate slots/provenance when generated;
- selected production dimensions/alpha/size;
- review contact sheets/previews;
- obsolete asset runtime-reference scan.

`mdl4/human-approval-gate`

- exact approved A03/A06 production and preview hashes;
- external human evidence resolution when available;
- fail while `PENDING`, `REJECTED`, stale, or self-authored without allowed evidence.

`mdl4/production-package-smoke`

- clean source build;
- single-process/session-store compatibility guard;
- start packaged app locally;
- health/config/cases/session shell smoke;
- unknown `/api/*` never returns SPA HTML;
- no private/static fixture exposure.

`mdl4/release-contract`

- current head/tree/digest identity;
- all required upstream check conclusions;
- skip/xfail inventory;
- no stale evidence references;
- human approval current;
- closure artifact consistency.

### CI anti-laundering rules

- Playwright browsers/dependencies are installed explicitly; zero discovered E2E tests is failure;
- deterministic failures are not made green by retry-until-pass;
- a bounded rerun may gather diagnostic trace only; the original deterministic failure remains failure until code/test is fixed;
- new skip/xfail entries require a source requirement, owner, reason, and explicit non-mandatory classification; a mandatory test cannot be skipped for closure;
- `continue-on-error` is forbidden on required jobs;
- all test summaries include discovered/passed/failed/skipped counts;
- CI runs on the final pushed `implementation_sha`, not an earlier art/code head.

Upload sanitized artifacts including JUnit/Playwright reports, score golden report, OpenAPI diff result, truth-isolation summary, art preflight, and game-contract digest. Never upload raw hidden truth or Genie chain-of-thought.

## Artwork production — mandatory MDL-4 gate

MDL-4 owns **A03 Dr. Genie Eureka** and **A06 Laboratory Entrance** under the ownership addendum above. The purpose is not decorative completion for its own sake: A06 establishes the full guided-lab shell and A03 supports positive evidence-discovery/verdict moments.

Artwork production starts immediately after branch creation and may run in parallel with engineering, but final production bytes must be human-approved **before `implementation_sha` is declared**.

### Global art direction prefix — use verbatim

Prepend this V3 direction to every A03/A06 generation request unless the generation interface separates style/reference instructions:

```text
Premium retro-futurist data science laboratory, sophisticated enterprise analytics meets playful scientific experimentation, dark navy research environment, luminous cyan data traces, restrained coral energy accents, subtle violet evidence glow, precision instruments, clean geometric forms, cinematic but not photorealistic, polished 3D illustration with lightly stylized proportions, trustworthy and intelligent, high detail in machinery but generous negative space for UI overlays, no readable text, no numbers, no logos, no watermarks, no brand marks, no horror, no dangerous chemical imagery.
```

Global hard negatives:

```text
no fantasy genie
no lamp
no smoke-body genie
no turban or magical costume
no pixel art
no retro 8-bit UI
no readable AI-generated text
no fake buttons
no fake functional charts
no Databricks logo imitation
no copyrighted character resemblance
no watermark
```

### Approved reference inputs

Before generating anything, resolve and record the exact SHA-256 of:

```text
A02 approved master Dr. Genie production/source reference — mandatory for A03 when reference-image generation is supported
A28/A01/A21 approved MDL-1 visual references — optional style references for A06 when useful
A05/A07 approved MDL-3 assets — optional consistency references; never replace A02 as the character identity authority
```

If the generator cannot consume reference images, include a textual identity lock copied from the approved A02 manifest and mark `reference_image_supported=false` in provenance. Do not silently use a different character source.

### Candidate plan — exactly 10 independent generations

```text
A03 Eureka pose:        C01-C06 = 6 candidates
A06 Laboratory entrance: C01-C04 = 4 candidates
TOTAL                              = 10 independent full-image candidates
```

A candidate is one full generation. A 4-up/6-up collage cropped into separate files does **not** count as multiple candidates.

Stable slot test IDs:

```text
MDL4-ART-001 = A03-C01
MDL4-ART-002 = A03-C02
MDL4-ART-003 = A03-C03
MDL4-ART-004 = A03-C04
MDL4-ART-005 = A03-C05
MDL4-ART-006 = A03-C06
MDL4-ART-007 = A06-C01
MDL4-ART-008 = A06-C02
MDL4-ART-009 = A06-C03
MDL4-ART-010 = A06-C04
```

Each slot test verifies candidate bytes exist, decode, match the requested aspect/alpha contract, and have prompt/provenance/hash metadata. Human quality approval is separate.

### Asset A03 — Dr. Genie “Eureka” pose

**Master target:** `1536×1536`, transparent background preferred/required when supported.

**Base prompt — preserve meaning:**

```text
Same approved Dr. Genie character and exact wardrobe as the approved master reference. Create an excited but controlled scientific discovery pose: leaning slightly forward, one hand pointing toward an invisible chart to the left, eyes focused, delighted “I found the pattern” expression, subtle cyan holographic particles around the pointing hand, professional and credible rather than cartoonishly explosive. Transparent background, full torso, lighting and proportions matching the master asset, no text, no logo, no watermark.
```

Append exactly one candidate variation:

```text
A03-C01 — clearest canonical three-quarter Eureka pose, strong leftward point, calm delighted expression, generous transparent space around silhouette.
A03-C02 — slightly more frontal torso, leftward pointing gesture at mid-height, eyebrows/eyes emphasize recognition without manic expression.
A03-C03 — slightly stronger forward lean and scientist energy, pointing hand extended farther left, restrained cyan particles only around hand.
A03-C04 — more compact centered torso with extra negative space on the left for the invisible chart/UI, subtle delighted half-smile.
A03-C05 — confident “pattern found” gesture with shoulders relaxed and pointing line visually clean at small UI size; avoid oversized hands.
A03-C06 — most understated enterprise-friendly Eureka variation, strong identity match, minimal particles, optimized for repeated use beside analytical UI.
```

A03 rejection criteria:

- face/hair/goggles/coat identity materially differs from approved A02;
- fantasy-genie traits or magical smoke/lamp symbolism;
- manic/comedic expression that undermines credibility;
- pointing direction conflicts with intended left-side analytical canvas;
- cropped hand/head at the production-safe crop;
- halo/particles obscure face or UI;
- generated text/chart labels appear;
- opaque/fake transparent checkerboard background;
- anatomy defect visible at in-app size.

**Production derivative:** transparent PNG/WebP with alpha; preserve source master outside deployment when large. Target deployment file <= `1.0 MB` unless a measured/human-approved exception is documented.

### Asset A06 — Laboratory entrance background

**Master target:** `2560×1440`, exact 16:9.

**Base prompt — preserve meaning:**

```text
Wide establishing shot of MAD DATA LAB, a premium retro-futurist data analytics laboratory designed for a modern enterprise game interface. Large central analytical chamber, modular scientific consoles, transparent data tubes carrying glowing abstract points and lines, one large empty wall area suitable for overlaying KPI cards, several recognizable but fictional instruments: a decomposition chamber, snapshot reactor, data microscope, lineage telescope. Dark navy architecture, cyan instrument light, restrained coral status lights, violet evidence glow. Cinematic depth, clean and sophisticated, subtle humor through unusual data-science machinery, not cluttered. No people, no readable text, no numbers, no logos, no watermarks. Keep center-left and top-right regions visually quiet for UI overlays.
```

Append exactly one candidate variation:

```text
A06-C01 — balanced near-symmetrical lab entrance; strongest large quiet center-left wall and restrained instrument silhouettes.
A06-C02 — gentle three-quarter perspective into the lab; deeper cinematic corridor while preserving broad calm overlay zones.
A06-C03 — cleanest enterprise/UI-first variant; fewer decorative machines, stronger negative space, precise cyan/violet guidance lights.
A06-C04 — slightly more dramatic analytical chamber depth with clearly fictional decomposition/snapshot/microscope/lineage machinery, but no fake controls or readable displays.
```

A06 rejection criteria:

- more than roughly one-third of the frame becomes unusable foreground decoration;
- central UI-safe zones are high-contrast/noisy;
- machinery resembles clickable application controls;
- baked-in charts/text/numbers/logos;
- fantasy magic/alchemy imagery dominates analytics;
- image reads as pixel-art board/game map rather than modern laboratory environment;
- perspective makes a normal 1440×900 application overlay look physically implausible;
- prominent people/characters appear;
- dark values crush legibility behind HTML cards.

**Production derivative:** optimized WebP, exact 16:9. Target deployment file <= `1.5 MB`. Preserve master/source outside deployment when larger.

### Generation request packets and provenance

Create:

```text
assets/review/MDL-4/art-generation-plan.json
assets/review/MDL-4/A03/requests/A03-C01.md ... A03-C06.md
assets/review/MDL-4/A06/requests/A06-C01.md ... A06-C04.md
```

Every generated candidate record contains:

```text
asset_id
candidate_id
revision
full_prompt_sha256
reference_asset_ids + reference_sha256 values
generator/tool
model/version when exposed; otherwise UNKNOWN_NOT_EXPOSED
generation timestamp
source filename
width
height
format
alpha present/absent
source sha256
rights/licensing basis sufficient for challenge submission
technical preflight status
human source-selection status
```

If a technical regeneration is needed, keep the same candidate ID with `r2`, `r3`, etc.; never overwrite rejected bytes/provenance.

If Codex cannot call an image generator, it must generate all 10 exact copy/paste request packets and set:

```text
BLOCKED_HUMAN_ART_GENERATION
```

Non-art engineering may continue, but MDL-4 cannot close.

### Automated candidate preflight

Before human source selection, automatically verify every candidate:

- file decodes;
- expected dimensions/aspect ratio;
- A03 alpha/transparency contract when required;
- no accidental EXIF rotation dependence;
- no zero-byte/truncated image;
- candidate hash recorded;
- no candidate file exceeds review-source safety limit unexpectedly;
- candidate is independent, not a crop alias/duplicate of another slot (use perceptual hash/similarity as a warning, exact hash as hard failure);
- no production candidate is itself a collage/contact sheet;
- manifest references resolve to approved predecessor asset hashes.

Automated tooling cannot reliably prove “no AI text” or character identity quality; those remain mandatory human review questions.

### Deterministic contact sheets

Create:

```text
assets/review/MDL-4/contact-sheets/A03-contact-sheet.png
assets/review/MDL-4/contact-sheets/A06-contact-sheet.png
```

Rules:

- equal visual scale per candidate;
- candidate aspect ratio preserved;
- neutral review background;
- labels are added by deterministic review tooling outside candidate pixels;
- label includes candidate ID + short SHA prefix;
- include approved A02 reference thumbnail beside A03 candidates;
- include approved MDL-1 visual reference thumbnail beside A06 when useful;
- contact-sheet SHA recorded in the generation plan.

### Human source selection — stage 1

A human selects exactly one source candidate for A03 and one for A06. Record:

```text
status = SOURCE_SELECTED
selected_candidate_id
selected_source_sha256
review_evidence_url_or_reference
selected_by
selected_at
notes
```

Codex cannot set `SOURCE_SELECTED` on behalf of the human.

If rejected, regenerate only the rejected asset/slot set, preserve rejected provenance, rebuild its contact sheet, and repeat human source selection.

### Production derivatives and integration previews

After `SOURCE_SELECTED`, create production derivatives and deterministic representative previews.

Required previews:

```text
assets/review/MDL-4/previews/A03-experiment-result-1440x900.png
assets/review/MDL-4/previews/A03-scientific-verdict-1440x900.png
assets/review/MDL-4/previews/A06-case-board-or-lab-entry-1440x900.png
assets/review/MDL-4/previews/A06-case-briefing-1440x900.png
```

Preview UI overlays must be rendered by deterministic application/review tooling, never generated into the illustration. Use representative real Case #042 HTML/SVG labels to test visual quietness.

A03 preview checks:

- face and gesture legible at actual Genie-panel size;
- pointing direction supports the analytical canvas;
- transparent edges clean against dark navy surfaces;
- pose does not cover evidence/primary action;
- repeated pose does not feel visually huge or childish.

A06 preview checks:

- Case Board/Briefing functional content remains dominant;
- at least ~65% of useful viewport area remains available to actual interaction/content;
- overlay cards remain readable without opaque emergency blocks everywhere;
- no machinery is mistaken for a button/tab/filter;
- critical content fits 1440×900 at 100% browser zoom.

### Human exact-byte approval — stage 2

Create/update:

```text
docs/approvals/MDL-4-art.md
```

Required record structure:

```yaml
iteration: MDL-4
status: PENDING
assets:
  - id: A03
    selected_candidate_id: null
    source_sha256: null
    production_sha256: null
    preview_sha256s: []
  - id: A06
    selected_candidate_id: null
    source_sha256: null
    production_sha256: null
    preview_sha256s: []
approved_by: null
approved_at: null
external_approval_evidence: null
notes: null
```

Preferred human evidence is an authenticated GitHub PR review/comment by the designated human that names:

```text
MDL-4
A03/A06
candidate ID
production SHA-256
review preview SHA-256(s)
APPROVED or REJECTED
```

CI resolves that evidence and verifies the actor/reference where tooling permits. Merely editing Markdown to `APPROVED` is insufficient evidence when external review evidence is available.

Final human questions:

- Does A06 leave enough genuine interaction space and feel like a real app background rather than a fixed board?
- Does A06 match the already-approved MAD DATA LAB universe?
- Does A03 unmistakably match A02 Dr. Genie?
- Is A03 excited but still credible/enterprise-appropriate?
- Are there any generated text, numbers, logos, watermarks, anatomy defects, or false controls?
- Do both assets work in the exact 1440×900 integration previews?

Any byte change to the approved production derivative or required preview invalidates approval until the corresponding human re-approves the new hash.

### Runtime asset cleanup

Once A06 is approved and integrated:

- no production route may use the obsolete pixel-art `board.png` as the functional lab/game backdrop;
- no production route may use the obsolete fantasy-genie hero as Dr. Genie;
- old assets may be retained only in explicitly non-production archival/reference paths excluded from the build, or removed;
- static CI scans runtime imports/manifest references for obsolete asset filenames/known hashes.

### Artwork tests

In addition to candidate-slot `MDL4-ART-001..010`, define:

```text
MDL4-ART-011 — A03 contact sheet references all six candidate hashes
MDL4-ART-012 — A06 contact sheet references all four candidate hashes
MDL4-ART-013 — A03 approved predecessor A02 hash resolves
MDL4-ART-014 — A03 selected production derivative has clean alpha and correct target bounds
MDL4-ART-015 — A06 selected production derivative is exact 16:9 and within target deployment budget
MDL4-ART-016 — all four required 1440x900 integration previews exist and hash
MDL4-ART-017 — approval record production/preview hashes equal current bytes
MDL4-ART-018 — external human approval evidence resolves or closure remains blocked
MDL4-ART-019 — obsolete pixel-art/fantasy-genie runtime references absent
MDL4-ART-020 — changed approved bytes invalidate approval automatically
```

No art approval -> MDL-4 cannot close.

## Databricks staging deployment and one complete live integrated session

Deploy the exact accepted `implementation_sha`/runtime-content identity through the inherited GitHub -> Databricks workflow. Do not deploy an uncommitted local tree.

### Deployment identity preconditions

Record/verify:

```text
implementation_sha
implementation_tree_sha
game_contract_digest
mdl2_data_contract_digest
canonical_case_hash
mdl3_genie_contract_digest
mdl3_live_config_sha256
A03 production sha256
A06 production sha256
Databricks target/app resource
resolved deployed commit/content identity
```

The deployed app must use:

```text
ENABLE_OFFLINE_DEMO=false
production fixture/fake Genie disabled
CHALLENGE_REVIEW_MODE=false unless the test explicitly validates review mode separately
single application worker while sessions are process-local
real configured Genie Agent resource
real curated Case #042 evidence data
```

### Authenticated deployed smoke

Use the inherited Databricks App API authentication path to verify at minimum:

```text
GET /api/health
GET /api/config
GET /api/cases
GET /api/cases/CASE_0042
POST /api/sessions
GET /api/sessions/{id}
```

Verify:

- Case #042 available;
- secondary Cases follow release/availability flags;
- health/config disclose no secrets;
- score is not exposed on a fresh/active Investigation;
- offline/fake mode not enabled;
- runtime/session-store topology matches single-worker requirement;
- approved A03/A06 production assets are present in the deployed static manifest and obsolete runtime assets are absent.

### Mandatory one-run live Case #042 integration harness

Before MDL-4 can close, execute **one complete automated live staging Investigation from session creation through Debrief using real Genie**, not fake/offline fixtures.

Implement `scripts/run_mdl4_live_session.py` or an equivalent CI harness that drives only public application APIs as a scripted player. It may know player choices/test expectations, but it must not inject hidden truth into Genie or bypass server completion rules.

Required algorithm:

1. create Case #042 session;
2. start Investigation against the real Genie Agent;
3. assert H1/H2/H3 public hypotheses and one valid pending/next Genie decision;
4. submit `PRED_SOURCE_VALUES_CHANGED` without observing correctness/score;
5. repeatedly call legal `/next`, consuming Genie-selected decisions until the server projection says analytical completion requirements are satisfied;
6. accept legal order variation for DQ vs formula and legal optional Experiments; **never substitute the golden next Experiment in the harness**;
7. bound the live loop to a fail-closed maximum of 8 completed Experiments and an overall configured timeout; exceeding the bound fails the run rather than forcing conclusion;
8. after snapshot evidence unlocks, inspect `CASE_0042:RECORD:TX-004291`;
9. open/inspect the required V2 lineage capability;
10. use zero hints for this closure run;
11. submit `FINAL_CHANGED_V2_SOURCE_RECORDS`;
12. call normal `/conclude` and validate the accepted public Scientific Verdict;
13. call `/debrief`;
14. verify final score is exactly **1000**;
15. verify expected earned #042 badges for this path according to the locked predicates;
16. return to/read Case Board progression and verify Case #042 completed/best score 1000 without directly mutating progression;
17. archive a sanitized run artifact.

The harness must assert throughout:

- every Experiment selection originates from a validated Genie decision/pending decision;
- no scripted decision substitution event occurred;
- trusted SQL fallback, if used, occurs only after a valid Genie selection and is recorded;
- no private truth/score correctness leaks before verdict;
- DQ remains real/non-primary and overlapping;
- formula final status is `RULED_OUT`;
- H1 broad status is `SUPPORTED` while narrow direct evidence may be confirmed;
- residual is `0.00` within tolerance;
- initial/final predictions are distinct immutable events;
- event sequence/state revision is strictly increasing;
- Debrief is the event that produces final +125/progression mutation.

Required sanitized `release-report/MDL-4/live-session.json` fields:

```text
workflow_run_id / run URL
implementation_sha
game_contract_digest
mdl2_data_contract_digest
mdl3_genie_contract_digest
genie_live_config_sha256
case_id
session_id hashed/redacted as appropriate
experiment_sequence[]
instrument_sequence[]
fallback_count + fallback categories
hints_used
high_value_evidence_inspected
required_lineage_opened
score_before_debrief
final_score
final_hypothesis_statuses
reconciliation_residual
badges_earned
started_at/completed_at/duration_ms
PASS/FAIL + stable diagnostic codes
```

Do not archive raw Genie chain-of-thought, OAuth tokens, private truth payload, or unnecessary raw chat/messages.

### Relationship to MDL-7 soak

This single integrated live run proves the game loop is wired correctly in MDL-4. It does **not** replace MDL-7's required repeated live Genie evaluation/10-run soak and final acceptance.

If Free Edition quota or a Databricks outage prevents the required live integrated run, record `BLOCKED_EXTERNAL_QUOTA`/appropriate blocker and preserve all deterministic green evidence. **Do not waive the live run and call MDL-4 COMPLETE.** Resume the one live run when the external condition clears.

### Negative deployed checks

Also verify through automated requests/config inspection:

- invalid/locked Case cannot create a session;
- illegal early conclusion returns `CONCLUSION_NOT_READY`;
- evidence from another Case cannot be requested;
- score/client truth fields are absent before verdict;
- offline fixture route/mode unavailable in production;
- unknown `/api/*` is JSON error/404, never SPA HTML;
- direct browser/static path cannot fetch private truth fixtures;
- Genie-facing principal still has no private truth permission after MDL-4's App-backend oracle permission transition.

## Manual deployment inspection

After automation is green:

- inspect Case Board -> Briefing -> Hypothesis transition visually;
- confirm experiment number/progress is dynamic, not `/3`;
- confirm approved lab art and Dr. Genie pose work in context;
- confirm prediction UI is understandable;
- inspect one score/debrief fixture visually;
- inspect browser console and app logs.

Do not rely on the human to determine whether scoring/status logic is correct; automated tests are authoritative.

## GitHub and merge closure

Run:

```bash
gh run list --branch MDL-4 --limit 20
gh pr checks --watch
```

All required checks green.

Merge only after:

- artwork approved;
- automated E2E green;
- staging deploy green;
- manual visual/runtime inspection accepted.

Then verify `main` CI and deployment.

## Required iteration report

Create `docs/iterations/MDL-4-report.md` as an `IN_PROGRESS` skeleton immediately after branch creation. It is the PR body source and must not claim `COMPLETE` until every closure gate below resolves to immutable evidence.

Required top-level fields/sections:

```yaml
iteration: MDL-4
status: IN_PROGRESS  # or BLOCKED / COMPLETE only under the rules below
branch: MDL-4
base_main_sha: null
implementation_sha: null
implementation_tree_sha: null
report_commit_sha: null
game_contract_digest: null
v3_source_sha256: null
mdl2_data_contract_digest: null
mdl2_canonical_case_hash: null
mdl3_genie_contract_digest: null
mdl3_live_config_sha256: null
pr_url: null
main_merge_sha: null
```

Then record, at minimum:

### Source/predecessor evidence

- definitive V3 source fingerprint;
- MDL-1/2/3 accepted predecessor references needed by MDL-4;
- MDL-3 artwork approval state/hash references;
- MDL-2 canonical Case/data identities;
- MDL-3 Genie contract/live configuration identities;
- any approved ADR/addendum that changes an inherited assumption.

### Implementation identity

- `implementation_sha` and Git tree SHA;
- runtime/game-content digest;
- classified report-only commit(s), if any;
- proof `origin/main` was an ancestor/fresh at final implementation acceptance;
- dependency lock hashes where captured by inherited evidence tooling.

### Server/gameplay model

- final phase/state/event vocabulary;
- session-store/TTL/capacity/single-worker policy;
- state-revision and idempotency behavior;
- pending Genie-decision handoff behavior;
- Case #042 completion-contract version and exact five blocking Experiment families;
- required-lineage and optional-high-value-record semantics;
- exact prediction IDs and statement that correctness mapping is private.

### API contract

List every implemented V3 endpoint plus MDL-4 extensions:

```text
GET  /api/sessions/{session_id}
POST /api/sessions/{session_id}/evidence/inspect
POST /api/sessions/{session_id}/debrief
```

Include OpenAPI/client-schema hash/evidence, error-registry version, idempotency policy and any backward-compatible API reconciliation decision.

### Scientific-verdict and truth-boundary evidence

- private-oracle interface used;
- App-runtime private validation permission proof;
- Genie-private-deny proof;
- static import/package leak scan result;
- exact accepted Case #042 verdict semantics;
- reconciliation residual evidence;
- proof the backend did not author/substitute the expected Genie conclusion after protocol failure.

Do not publish the complete `CASE_TRUTH` object in the report.

### Scoring, hints, badges, progression

Include a machine-generated score-golden summary containing at least:

```text
PERFECT                       1000
WRONG_INITIAL_CORRECT_FINAL   900
ONE_HINT                       950
ALL_THREE_HINTS                850
SKIP_HIGH_VALUE_RECORD         900
EARLY_REVEAL_CORRECT_INITIAL   650
EARLY_REVEAL_WRONG_INITIAL     550
```

Record:

- pre-verdict score-privacy test result;
- hint prerequisite/idempotency results;
- all seven badge predicate results;
- Case #042 actually attainable badge results;
- progression/unlock/best-score tests;
- restart/profile-loss limitation if the challenge MVP remains process/local-first.

### Automated test/CI evidence

Record immutable references for:

- one-command local gate output;
- canonical V3 test-coverage artifact;
- custom MDL4 test-registry result;
- API/OpenAPI result;
- fake-Genie Playwright result;
- production-package smoke;
- private-truth/security result;
- GitHub required-check run IDs/URLs;
- discovered/passed/failed/skipped counts;
- approved skip/xfail inventory, which must contain no skipped mandatory closure test.

### Live Databricks integration evidence

Record:

- staging deployment/run identity;
- deployed source/runtime identity;
- one complete automated live Case #042 session artifact;
- Experiment sequence actually selected by Genie;
- whether trusted SQL fallback occurred and, if so, the preceding valid Genie decision;
- final verdict/reconciliation/result status;
- final Debrief score and progression result;
- proof offline/fake Genie mode was disabled;
- non-sensitive permission checks;
- platform/quota blocker if the live run could not execute. A blocker means MDL-4 is not complete.

### Artwork evidence

For A03 and A06 include:

- all candidate IDs/revision hashes;
- generation prompt/source/reference hashes;
- generation tool/model/provenance/rights metadata where available;
- contact-sheet hashes;
- selected source candidate IDs/hashes;
- production derivative hashes/dimensions/sizes;
- four 1440x900 integration-preview hashes;
- external human source-selection evidence;
- external human exact-byte approval evidence;
- obsolete runtime-art scan result.

### Decisions, limitations and deferrals

- only spec-preserving implementation substitutions;
- blockers encountered and how resolved;
- work explicitly deferred to MDL-5/6/7;
- no ambiguous “later” without an owner iteration.

### Report status semantics

`COMPLETE` is legal only when:

1. all deterministic/local/CI gates are green on accepted implementation content;
2. A03/A06 exact production bytes are human-approved;
3. staging deployment/smoke is green;
4. one complete automated real-Genie Case #042 session reaches Debrief successfully;
5. no mandatory evidence reference is stale;
6. the PR is merged and `main` post-merge checks are green, or the report is clearly still `READY_TO_MERGE` before merge.

A report-only post-deployment commit may fill immutable run/merge references under the inherited two-identity closure model. It must not mutate runtime-affecting content or create a new untested implementation identity.


## Content contract and Dr. Genie dialogue guardrails

The game text is part of the functional specification because it communicates epistemic certainty. Do not let generated copy or implementation convenience weaken the scientific meaning.

### Canonical dialogue beats

Use these canonical lines at the corresponding beats unless a later human-approved copy revision explicitly changes them:

```text
Case start:
“Wonderful. Something is wrong.”

Hypotheses ready:
“Three explanations survive first contact with the data.”

Before evidence / challenge:
“An opinion without evidence? In my laboratory?”

V2 decomposition:
“Aha. V2 is carrying most of the anomaly.”

DQ materiality:
“Tempting. But science requires magnitude.”

Insufficient evidence outcome/help:
“Insufficient evidence. A perfectly respectable scientific answer.”

Conclusion:
“The hypothesis survived the experiments. Now we can explain why.”

Closing:
“We did not ask for an answer. We ran an investigation.”
```

Minor punctuation/localization changes are acceptable; changing the scientific meaning is not.

### Dialogue-length and tone rules

During active play:

- Dr. Genie dialogue is at most two short sentences per beat;
- tone is curious, precise, intelligent, mildly theatrical, and respectful;
- humor decorates rigor and never substitutes for evidence;
- a wrong prediction must never mock or shame the player;
- never joke about real financial loss, layoffs, individuals being blamed, protected groups, or dangerous laboratory accidents;
- do not use unsupported probability percentages such as `92% likely`;
- do not say `confirmed` when the canonical status is only `SUPPORTED` or `POSSIBLE`;
- do not call a DQ warning “the cause” before quantified evidence/reconciliation;
- do not imply the fictional/synthetic Case is a real customer incident.

Generated free-form Dr. Genie answers must follow the same epistemic vocabulary even though their exact wording is not snapshotted.

### Required debrief teaching cards

The Case #042 Debrief must communicate all five V3 concepts, with HTML text derived from the approved copy rather than bitmap text:

1. **Start with a baseline** — an anomaly is meaningful relative to an expectation/control.
2. **Keep explanations separate** — multiple hypotheses may remain plausible simultaneously.
3. **Test the largest signal first** — decomposition identifies V2 as the best next target.
4. **Reconcile evidence** — V2 record changes reconcile to the V2 movement.
5. **Warnings are not causes** — the DQ issue exists but does not have enough materiality to explain the anomaly.

The displayed content may be shortened for layout, but all five concepts must remain present and testable.

### Content regression tests — iteration-specific

Add:

- `MDL4-COPY-001` — canonical Case start and closing lines appear at the correct beats;
- `MDL4-COPY-002` — no prototype retail hypothesis vocabulary remains in production UI/API fixtures;
- `MDL4-COPY-003` — no unsupported probability percentage is displayed for hypothesis certainty;
- `MDL4-COPY-004` — DQ copy never says it is primary cause in the golden path;
- `MDL4-COPY-005` — all five debrief learning concepts are present;
- `MDL4-COPY-006` — wrong-prediction path uses neutral/respectful copy and still reaches completion;
- `MDL4-COPY-007` — active-play fixed dialogue entries respect the two-short-sentence maximum;
- `MDL4-COPY-008` — Case #042 is labeled fictional/synthetic wherever submission/user context could otherwise imply real financial data.

## API schema compatibility and frontend contract generation

The frontend and backend must not drift through separately hand-maintained interfaces.

### OpenAPI as executable API contract

FastAPI's generated OpenAPI document must be stable enough to use as an integration contract. Add a deterministic contract step that:

1. boots/imports the application in test mode without contacting live Databricks;
2. exports normalized OpenAPI JSON;
3. validates required endpoints, status/error envelopes, and model schemas;
4. compares against an intentional checked-in contract snapshot or uses generated frontend types from that OpenAPI document;
5. fails CI when backend contract changes without the corresponding frontend/test update.

Do not snapshot irrelevant ordering/timestamps that create noise.

### One source for client schemas

Choose one of these acceptable approaches and document it:

- generate TypeScript API types from normalized OpenAPI in CI/build; or
- maintain TypeScript schemas with an automated bidirectional compatibility test against OpenAPI.

Do not rely solely on `as Type` casts in frontend code.

For runtime-untrusted JSON, validate the response shape before analytical rendering when the client boundary can receive malformed/unexpected data.

### Contract invariants

At minimum assert:

- all JSON endpoints use the agreed top-level `ok/data/error/request_id` envelope where the definitive API contract requires it;
- `case_id`, session IDs, enums, numeric fields, and pagination shapes match the domain model;
- error codes are closed/known for critical paths;
- hidden/private truth fields are absent from public OpenAPI response schemas;
- `/api/config`, `/api/health`, and build-info schemas contain no secrets;
- the final frontend production build consumes the same schema version validated by CI.

### API compatibility tests — iteration-specific

Add:

- `MDL4-CONTRACT-001` — normalized OpenAPI can be generated offline/deterministically;
- `MDL4-CONTRACT-002` — checked-in/generated client types match current OpenAPI;
- `MDL4-CONTRACT-003` — public response schemas contain no hidden truth fields;
- `MDL4-CONTRACT-004` — unknown/removed enum value is rejected instead of silently cast;
- `MDL4-CONTRACT-005` — frontend build fails on an intentional contract mismatch fixture;
- `MDL4-CONTRACT-006` — API contract version/build identity is observable in test/release metadata.


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

Rules:

1. Every stable test ID from V3 §44 must appear exactly once as an **owner**. Rerun references in later iterations do not create a second owner.
2. `release_applicability` is one of `MANDATORY`, `CONDITIONAL_CASE`, or `RERUN_ONLY`.
3. `CONDITIONAL_CASE` is allowed only for a Case whose server-owned release state is not enabled in the challenge build. It is not a waiver. The moment that Case becomes enabled, its conditional tests become blocking.
4. No row may disappear because the implementation was simplified. If a V3 requirement is intentionally superseded by a higher-precedence challenge/platform rule, record an ADR and keep the row with the disposition and rationale.
5. A CI validator must fail when there is an unknown test ID, duplicate owner, missing owner, invalid applicability, missing implementation path for a mandatory implemented test, or a mandatory test whose latest result is not green.
6. Test code should carry the canonical ID in the test name, marker, docstring, metadata, or generated JUnit property so CI reports are traceable without reading prose.
7. The traceability ledger itself must be reviewed in every iteration because moving code between layers can change the correct implementation path or CI job without changing the product requirement.

### Iteration evidence manifest

Create or update `release-report/MDL-4/manifest.json`. The final manifest must be generated by automation after the last content-changing commit rather than hand-edited to claim success.

Minimum schema:

```json
{
  "iteration": "MDL-4",
  "branch": "MDL-4",
  "base_commit_sha": "...",
  "base_tree_sha": "...",
  "accepted_head_commit_sha": "...",
  "accepted_head_tree_sha": "...",
  "pull_request_number": 0,
  "required_ci_checks": [],
  "github_workflow_run_ids": [],
  "test_report_sha256": {},
  "build_artifact_sha256": "...",
  "databricks_deployment": {
    "app_name": "...",
    "deployment_or_run_id": "...",
    "reported_build_sha": "...",
    "reported_tree_sha": "...",
    "post_deploy_smoke": "PASS"
  },
  "data_schema_version": "...",
  "genie_config_sha256": "...",
  "asset_sha256": {},
  "human_art_approval_files": [],
  "open_blockers": []
}
```

Use `null` for fields that genuinely do not apply yet; do not invent values. `open_blockers` must be empty to close the iteration.

The manifest must never contain credentials, OAuth material, PATs, raw hidden-truth payloads, authorization headers, private user identifiers, or unredacted sensitive logs.

### Release-contract validation

Before MDL-4 can close, run the reusable validators introduced in MDL-1:

```bash
python scripts/validate_traceability.py
python scripts/validate_human_approvals.py --iteration MDL-4
python scripts/validate_iteration_manifest.py release-report/MDL-4/manifest.json --require-complete
```

The required GitHub `release-contract` check must run the same closure validation against the exact PR head. Do not manually edit the generated manifest merely to satisfy the schema; fix the missing evidence/gate and regenerate it.

### Exact deployed-content proof

A successful deployment is not enough. The application must expose safe build metadata (for example through `/api/health` or a non-sensitive build-info endpoint) containing at least the application version and accepted Git commit/tree identity. The post-deployment smoke test must compare that value with the content accepted by CI.

If the deployment mechanism rebuilds the project and a byte-for-byte source artifact comparison is impossible, generate a deterministic build metadata file before packaging and verify the deployed server reports it. Never infer deployment provenance from deployment time alone.

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
- PR number/link if available;
- accepted head commit SHA and tree SHA;
- exact local commands run and their exit status;
- required GitHub check names and final states;
- workflow/run IDs when available;
- deployment/run identifier and safe deployed build identity;
- automated deployed smoke result;
- traceability validator result;
- artwork candidate paths, production asset hash(es), and human approval file/status;
- known limitations or blockers;
- paths to `release-report/MDL-4/` evidence.

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
python scripts/validate_human_approvals.py --iteration MDL-4
```

The validator must fail unless:

- every artwork/audio asset required by MDL-4 exists in the production asset manifest;
- each required production file hashes to the SHA-256 recorded in its approval record;
- approval status is exactly `APPROVED`;
- `approved_by` and `approved_at` are present and were supplied as the result of an explicit human decision;
- no required asset is still `PENDING`, `REJECTED`, `AWAITING_GENERATION`, or missing;
- a replaced/recompressed asset has obtained fresh approval for its new bytes.

The required GitHub merge check should expose a stable name such as `human-approval-gate`. It is expected to remain red while approval is pending. Do not bypass or mark it optional merely to keep the PR visually green during development. A human approval in chat/PR review is not enough by itself until its exact asset hash has been recorded in the repository approval file; conversely, Codex must not write `APPROVED` without an explicit human decision.



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

Primary V3 sections whose closure belongs to MDL-4:

| V3 section | Title | Required result |
|---:|---|---|
| §11 | Core Game Loop | Close complete player/Genie investigation loop; MDL-1 only bootstraps domain types. |
| §12 | Full Player Journey | Implement full Case #042 journey. |
| §13 | Game State Machine | Close event-driven authoritative state machine; MDL-1 only creates skeleton. |
| §14 | Gamification and Scoring | Implement exact score/hints/badges. |
| §15 | Case System, Difficulty, Catalog, and Progression | Close availability/progression/session behavior; MDL-1 bootstraps catalog. |
| §17 | Educational Model and Debrief | Implement concepts and calibrated debrief. |
| §35 | Backend API Contract | Implement full API. |
| §36 | Frontend Architecture and State Model | Implement authoritative state/client separation. |

Sections not listed above may still be touched or rerun in MDL-4; that does not transfer their primary closure ownership.

### Platform-drift verification gate

The definitive V3 hierarchy gives current challenge/platform rules precedence over older implementation assumptions. Therefore, at both **iteration start** and **iteration closure**, create/update `docs/iterations/MDL-4-platform-verification.md` with:

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

### V3 §44 exact test ownership ledger for MDL-4

This is the self-contained ownership view for the definitive V3 §44 catalog. The repository `docs/traceability/v3-test-coverage.csv` must contain the same ownership at individual-ID granularity. A row here does not mean the test already exists: it means MDL-4 cannot close until a `MANDATORY` row has an implementation/evidence path and a green result.

| Canonical ID | Applicability | Source-spec requirement |
|---|---|---|
| `API-003` | MANDATORY | create session valid case |
| `API-004` | MANDATORY | create session invalid case |
| `API-005` | MANDATORY | start investigation legal state |
| `API-006` | MANDATORY | start duplicate idempotent/rejected consistently |
| `API-007` | MANDATORY | prediction legal stage |
| `API-008` | MANDATORY | invalid hypothesis ID 422/400 |
| `API-009` | MANDATORY | next endpoint happy path |
| `API-010` | MANDATORY | next endpoint illegal state |
| `API-011` | MANDATORY | evidence pagination |
| `API-012` | MANDATORY | evidence hard limit 100 |
| `API-013` | MANDATORY | business-key search sanitized |
| `API-014` | MANDATORY | hint progression |
| `API-015` | MANDATORY | hint 4 does not exist |
| `API-016` | MANDATORY | conclusion blocked before required evidence |
| `API-017` | MANDATORY | conclusion succeeds at correct state |
| `API-018` | MANDATORY | request_id always present |
| `API-019` | MANDATORY | internal stack trace absent from response |
| `API-020` | MANDATORY | malformed request returns stable error envelope |
| `API-021` | MANDATORY | concurrent duplicate `/next` requests do not duplicate experiment |
| `API-022` | MANDATORY | session IDs unguessable UUID-like values |
| `API-023` | MANDATORY | chat max length enforced |
| `API-024` | MANDATORY | chat scopes to case |
| `API-025` | MANDATORY | chat response control logic separated from chat prose |
| `API-026` | MANDATORY | Case catalog returns only public metadata |
| `API-027` | MANDATORY | unreleased Case cannot create a production session |
| `API-028` | MANDATORY | review mode availability is server-controlled |
| `API-029` | MANDATORY | Case detail does not expose expected path or hidden truth |
| `API-030` | MANDATORY | progression best score keeps max |
| `API-031` | MANDATORY | invalid Case completion cannot unlock dependent Case |
| `API-032` | MANDATORY | session Case ID immutable after creation |
| `API-033` | MANDATORY | evidence request cannot cross session Case boundary |
| `CASE107-001` | CONDITIONAL_CASE | expected 42.0, observed 43.8, deviation +1.8 |
| `CASE107-002` | CONDITIONAL_CASE | row-count delta +255 |
| `CASE107-003` | CONDITIONAL_CASE | exactly 255 causal duplicate rows |
| `CASE107-004` | CONDITIONAL_CASE | duplicate impact +1.8 |
| `CASE107-005` | CONDITIONAL_CASE | replay run references original run |
| `CASE107-006` | CONDITIONAL_CASE | source values excluding duplicates reconcile to zero anomaly contribution |
| `CASE107-007` | CONDITIONAL_CASE | expected route starts ROW_COUNT_ANALYSIS or DUPLICATE_KEY_ANALYSIS and must include both before conclusion |
| `CASE213-001` | CONDITIONAL_CASE | expected 41.2, observed 34.7, deviation -6.5 |
| `CASE213-002` | CONDITIONAL_CASE | source totals before filtering unchanged |
| `CASE213-003` | CONDITIONAL_CASE | filter hash changes |
| `CASE213-004` | CONDITIONAL_CASE | 74 excluded records |
| `CASE213-005` | CONDITIONAL_CASE | excluded impact -6.5 |
| `CASE213-006` | CONDITIONAL_CASE | formula expression hash unchanged |
| `CASE213-007` | CONDITIONAL_CASE | conclusion blocked until FILTER_VALIDATION evidence exists |
| `CASE314-001` | CONDITIONAL_CASE | row-count delta -383 |
| `CASE314-002` | CONDITIONAL_CASE | total missing impact -5.2 |
| `CASE314-003` | CONDITIONAL_CASE | 17 high-impact missing rows total -4.9 |
| `CASE441-001` | CONDITIONAL_CASE | DQ affected count 1248 |
| `CASE441-002` | CONDITIONAL_CASE | DQ impact -0.08 and cannot become primary cause |
| `CASE441-003` | CONDITIONAL_CASE | primary source-change contribution -6.9 |
| `CASE520-001` | CONDITIONAL_CASE | observed 83.0 versus expected-center 46.0 |
| `CASE520-002` | CONDITIONAL_CASE | join cardinality impact +36.8 |
| `CASE520-003` | CONDITIONAL_CASE | technical/value lineage reaches problematic relationship |
| `CASE812-001` | CONDITIONAL_CASE | total deviation -6.2 |
| `CASE812-002` | CONDITIONAL_CASE | source-change impact -4.1 |
| `CASE812-003` | CONDITIONAL_CASE | filter-change impact -2.3 |
| `CASE812-004` | CONDITIONAL_CASE | other effect +0.2 |
| `CASE812-005` | CONDITIONAL_CASE | all contributions sum exactly -6.2 |
| `CASE812-006` | CONDITIONAL_CASE | verdict cannot collapse to one cause with material residual |
| `CAT-007` | MANDATORY | every template references registered Experiments |
| `CAT-008` | MANDATORY | every template references registered Instruments through legal mappings |
| `CAT-009` | MANDATORY | every learning-objective ID exists |
| `DU-004` | MANDATORY | score starts at zero |
| `DU-005` | MANDATORY | score clamps to 0 minimum |
| `DU-006` | MANDATORY | score clamps to 1000 maximum |
| `DU-007` | MANDATORY | hint deduction |
| `DU-008` | MANDATORY | duplicate hint request idempotency |
| `DU-009` | MANDATORY | early reveal penalty |
| `DU-010` | MANDATORY | badge Data Apprentice |
| `DU-011` | MANDATORY | badge Metric Scientist threshold |
| `DU-012` | MANDATORY | badge Evidence Analyst requirements |
| `DU-013` | MANDATORY | badge Skeptical Scientist requirements |
| `DU-021` | MANDATORY | app state event append-only |
| `DU-022` | MANDATORY | evidence status monotonicity is not assumed |
| `DU-023` | MANDATORY | RULED_OUT requires evidence reason |
| `DU-024` | MANDATORY | CONFIRMED requires reconciliation marker or direct validation |
| `E2E-001` | MANDATORY | complete perfect-score path |
| `E2E-002` | MANDATORY | wrong initial prediction still completes |
| `E2E-003` | MANDATORY | one hint path |
| `E2E-004` | MANDATORY | all hints path |
| `E2E-005` | MANDATORY | early reveal penalty path |
| `E2E-006` | MANDATORY | skip optional record inspection |
| `E2E-007` | MANDATORY | evidence filter MODIFIED |
| `E2E-008` | MANDATORY | search TX-004291 |
| `E2E-011` | MANDATORY | browser refresh behavior at lab entry |
| `E2E-019` | MANDATORY | SQL reconciliation failure blocks false conclusion |
| `E2E-020` | MANDATORY | unknown case friendly error |
| `E2E-027` | MANDATORY | double-click next does not duplicate experiment |
| `E2E-028` | MANDATORY | browser back button does not corrupt state |
| `E2E-MC-001` | MANDATORY | Case Board → #042 → verdict → back to board |
| `E2E-MC-002` | MANDATORY | completion state visible on board |
| `E2E-MC-003` | CONDITIONAL_CASE | #107 full path with fake Genie |
| `E2E-MC-004` | CONDITIONAL_CASE | #213 full path with fake Genie |
| `E2E-MC-005` | MANDATORY | open #042, abandon, start #107; no cross-case state |
| `E2E-MC-006` | MANDATORY | locked Case user experience |
| `E2E-MC-007` | CONDITIONAL_CASE | review mode exposes TARGET Cases |
| `E2E-MC-008` | MANDATORY | Level 3 fixture supports >2 Experiments and multiple causes |
| `E2E-MC-009` | MANDATORY | generic Experiment Result screen renders three different Instrument families without Case-specific routing |
| `E2E-MC-010` | MANDATORY | browser refresh on Case Board preserves progression/preferences |
| `FE-003` | MANDATORY | hypothesis board renders priorities |
| `FE-019` | MANDATORY | score updates only from server response |
| `FE-020` | MANDATORY | primary action disabled during active request |
| `FE-021` | MANDATORY | no double submit |
| `FE-026` | MANDATORY | Case Board renders CORE/TARGET/LOCKED/COMING_SOON states |
| `FE-027` | MANDATORY | Case card accessible name includes Case number and title |
| `FE-028` | MANDATORY | completed Case shows best score without color-only status |
| `FE-029` | MANDATORY | Case Briefing uses selected Case metadata rather than hardcoded #042 copy |
| `FE-030` | MANDATORY | Experiment Result component renders an arbitrary registered Instrument model |
| `FE-031` | MANDATORY | Level 3 verdict renders two causal contributions |
| `FE-032` | MANDATORY | unavailable Case screen has deterministic navigation back to board |
| `ISO-001` | MANDATORY | evidence endpoint cannot request a different Case than the session |
| `ISO-002` | MANDATORY | Genie prompt always scopes to session Case ID |
| `ISO-003` | MANDATORY | switching Cases creates a new conversation/session |
| `ISO-004` | MANDATORY | evidence IDs are namespaced/validated against Case |
| `ISO-005` | MANDATORY | no hypothesis/event history from Case A appears in Case B |
| `PRG-002` | MANDATORY | Case #107 unlock condition after #042 completion |
| `PRG-003` | MANDATORY | challenge review mode exposes shipped target Cases without mutating persisted progression |
| `PRG-004` | MANDATORY | invalid completion payload cannot unlock a Case |
| `PRG-005` | MANDATORY | best score monotonically keeps maximum |
| `PRG-006` | MANDATORY | badge Case Collector after three unique completions |
| `PRG-007` | MANDATORY | replaying same Case does not increment unique-completion count |
| `PRG-008` | MANDATORY | locked Case deep link returns `CASE_UNAVAILABLE` |

### MDL-4 additional closure requirements

#### Server-authoritative replay oracle

Add a test helper capable of replaying an Investigation event log from the initial Case/session state and deriving the same authoritative state, score, predictions, evidence flags, and completion eligibility. Event replay must not require hidden browser-local state.

Use this to catch accidental state mutation and scoring drift.

#### Idempotency model

For every state-changing endpoint, define whether retries are `idempotent`, `idempotent-with-key`, or `reject-duplicate`. Tests must cover response-loss/retry, double-click, and concurrent request cases. The decision must be documented in the API schema rather than inferred from frontend disabling.

#### Score golden scenarios

In addition to individual scoring unit tests, define at least five named full-session score fixtures with exact expected totals: perfect path, wrong-initial/correct-final, one-hint, all-hints, and early-reveal. A change to the score formula must intentionally update both the domain tests and the documented canonical score fixtures.

#### Conditional Case enforcement

The server must derive Case availability from release configuration. A disabled/locked secondary Case is not a reason to delete its V3 traceability rows. CI should prove disabled Cases cannot accidentally become available through frontend constants, direct deep links, or review-mode leakage.

## MDL-4 strict maturity and repository self-audit

Implement `scripts/validate_mdl4_contract.py` and require:

```bash
python scripts/validate_mdl4_contract.py --strict
```

before MDL-4 can close.

The validator is not a substitute for tests; it verifies that the repository, iteration contract and closure evidence still agree. It must fail closed when required evidence cannot be resolved.

Minimum strict checks:

### Specification/source integrity

- definitive V3 source fingerprint matches the accepted source record or an explicit approved addendum exists;
- MDL-1/2/3 predecessor references and required approval/digest identities resolve;
- Markdown fences in the canonical MDL-4 implementation contract are balanced;
- no duplicate full Markdown headings;
- no unresolved `TODO`, `TBD`, `FIXME`, fake `PASS`, literal metavariable or placeholder credential exists in executable code/config;
- `Document maturity` may be `READY_TO_IMPLEMENT` without closure, but the iteration report may not say `COMPLETE` while any mandatory gate is pending.

### Test traceability

- every canonical MDL-4-owned V3 ID in `docs/traceability/v3-test-coverage.csv` has exactly one primary owner and an implementation/evidence mapping;
- every custom `MDL4-*` ID has one canonical definition; later references resolve to it rather than redefining it;
- canonical mandatory IDs cannot be classified as skipped/xfail for closure;
- `CONDITIONAL_CASE` IDs stay present even while their Cases remain unavailable;
- zero discovered tests in any required suite is failure.

### Game/domain contract

- the public state machine has no Case-specific result phases such as `RESULT_1`, `RESULT_2`, `DQ_STAGE`;
- event types, score-event types, prediction IDs, error codes and badge IDs are closed/versioned;
- Case #042 blocking Experiment families are exactly:

```text
COMPONENT_DECOMPOSITION
SNAPSHOT_DIFF
DQ_MATERIALITY
FORMULA_VALIDATION
RECONCILIATION
```

- `SOURCE_RECORD_INSPECTION` is not accidentally made a blocking Case #042 Experiment;
- required V2 lineage/comparison inspection remains a completion prerequisite;
- TX-004291 detail inspection remains optional for completion but rewarding for score/badge;
- no source path assumes a fixed Experiment count such as `3` or `/3` for Case completion.

### Prediction/scoring privacy

- initial and final prediction IDs are separate closed sets;
- private correct-answer keys do not appear in browser/static Case metadata;
- public session projection contains no initial-prediction correctness bit or score delta before verdict;
- final score fixtures match the seven locked MDL-4 golden scenarios;
- Experiment completion points cap at +300 even though Case #042 has five blocking Experiment families;
- Debrief is the only path that awards the +125 Debrief event;
- early reveal skips final prediction and awards exactly one -150 event only after analytical completion;
- score reducer is replay-deterministic and clamp is `[0,1000]`.

### API/state authority

- OpenAPI exposes the V3 endpoints plus MDL-4 `GET session`, `evidence/inspect`, and `debrief` extensions;
- generated frontend API schemas are current with backend OpenAPI;
- state-changing APIs implement documented idempotency/revision semantics;
- evidence-inspection scoring eligibility is server-resolved;
- session Case identity is immutable;
- process-local store plus production worker configuration satisfies the single-worker guard;
- chat cannot mutate gameplay state or score.

### Scientific-verdict/truth boundary

- Genie modules cannot import private oracle modules;
- normal evidence/Experiment execution cannot read private truth;
- App backend has only the narrow private validation path required by this iteration;
- Genie remains unable to read private truth;
- browser/static package contains no private truth/oracle fixture;
- accepted #042 verdict requires H1 broad `SUPPORTED`, H2 `RULED_OUT`, H3 `POSSIBLE`, V2 `-5.90`, other effects `-0.90`, DQ overlap `-0.30` non-additive, residual `0.00`;
- backend cannot silently substitute a canned final answer for failed Genie output.

### CI/evidence freshness

- the ten required `mdl4/*` check contexts in this document match the version-controlled branch-protection/ruleset contract exactly;
- `game_contract_digest` algorithm/path policy is present and deterministic;
- fake-E2E, live-session, deploy and art evidence all reference current accepted identities;
- unknown changed paths classify fail-closed as runtime/game-affecting;
- report-only evidence reuse follows the inherited two-identity closure policy;
- report cannot claim `COMPLETE` with stale/missing immutable workflow references.

### Artwork

- generation plan contains exactly 10 required independent slots: A03 C01-C06 and A06 C01-C04;
- each candidate has prompt/provenance/hash metadata and is not merely a crop from a collage;
- A03 selected source references the approved A02 master identity when generator capability permits;
- contact sheets include every candidate/revision under review;
- selected assets have required production derivatives and exactly four required 1440x900 integration previews in total;
- final approval references exact production and preview hashes plus external human evidence;
- self-authored/`PENDING`/`REJECTED`/stale approval fails closure;
- approved A06 runtime path has no obsolete `board.png`/fantasy-genie background dependency.

### Live deployment

- closure evidence contains one automated complete real-Genie Case #042 run through `/debrief`;
- fake/offline mode is proven disabled;
- live session artifact matches current `implementation_sha`, `game_contract_digest`, MDL-2 data identity and MDL-3 Genie identity;
- live run reaches all five blocking families within the documented safety bound without application-side expected-path substitution;
- final live perfect-path score is 1000;
- permission checks still prove Genie-private denial.

Add/maintain custom self-audit tests:

- `MDL4-CONTRACT-007` — required CI context list is single-source and exact;
- `MDL4-CONTRACT-008` — exact Case #042 completion/scoring contract is structurally present;
- `MDL4-CONTRACT-009` — all custom-ID definitions are unique and references resolve;
- `MDL4-CONTRACT-010` — final report cannot claim COMPLETE with pending/stale live/art/CI evidence;
- `MDL4-CONTRACT-011` — production package has no obsolete board/fantasy runtime dependency after approved integration;
- `MDL4-CONTRACT-012` — live artifact and game digest/predecessor identities all agree.

## Codex first-hour runbook — mandatory implementation start

Codex should begin MDL-4 in this order rather than starting with cosmetic pages:

1. Read the definitive V3 source and this entire MDL-4 implementation contract.
2. Run the inherited MDL-3 predecessor/approval/digest verification on merged `main`; stop with `BLOCKED_PREDECESSOR_MDL_3` if it fails.
3. Fetch/prune Git, fast-forward `main`, verify a clean tree and create/continue `MDL-4` without deleting existing remote history.
4. Create `docs/iterations/MDL-4-report.md` immediately with `status: IN_PROGRESS`; push the branch and open/update the PR early.
5. Record the current MDL-2 data/canonical Case identities and MDL-3 Genie/live-config identities used by the game digest.
6. Generate `assets/review/MDL-4/art-generation-plan.json` and the ten A03/A06 copy/paste generation packets. Start candidate generation in parallel with engineering; do not wait for final UI to begin art review.
7. Capture a baseline result from inherited MDL-1/2/3 deterministic gates before large changes.
8. Implement/finalize the event vocabulary, state reducer/replay oracle, session store, state revision, idempotency and pending-Genie-decision handoff **before** building UI controls around them.
9. Implement the exact Case #042 completion predicate/evidence entitlements and prove the five blocking families + required-lineage/optional-record behavior with domain tests.
10. Implement scoring/hints/badges/progression as pure/event-driven server logic and make the seven golden scoring scenarios green before exposing score UI.
11. Implement the narrow private oracle/verdict validator boundary and its import/permission/leak tests.
12. Complete API routes/OpenAPI/generated client, including session read, evidence inspect and Debrief extensions.
13. Build the functional frontend shell from server projections; do not implement Case #042 result pages as hardcoded routes.
14. Make the fake-Genie full Case #042 Playwright path green, then add wrong-prediction, hints, early-reveal, refresh/back, race and failure paths.
15. Obtain human **source selection** for A03/A06 candidates, build production derivatives/contact sheets/integration previews, then obtain exact-byte human approval.
16. Run `python scripts/run_iteration_gate.py --iteration MDL-4 --mode local`; fix every deterministic failure rather than skipping/rerunning it away.
17. Commit/push the final runtime/art/approval content, declare `implementation_sha`, run all required GitHub checks on that exact head and verify branch freshness against `origin/main`.
18. Deploy that accepted implementation identity to staging, run automated smoke and the one complete real-Genie Case #042 session through Debrief.
19. Perform only the allowed visual/log deployment inspection. A functional defect discovered manually must gain an automated regression test before/with its fix.
20. Finalize immutable evidence/report fields, run closure mode, merge only when all gates are green, then verify post-merge `main` CI/deployment state.

Do not start MDL-5 while MDL-4 is merely “mostly green.” A human/art/platform blocker stays explicit.

## Conditions that reopen the MDL-4 specification

Do **not** casually edit the locked gameplay contract during implementation. Reopen this document/record an ADR only when a material fact invalidates an assumption, including:

- definitive V3 scoring, prediction, completion, badge, progression or verdict semantics change;
- MDL-3 changes the pending-decision/control protocol in a way that makes this handoff incompatible;
- MDL-2 changes the canonical #042 data/evidence identity or completion-relevant evidence semantics;
- a current Databricks platform/API change makes the live integrated path materially different;
- reliable production execution requires multi-worker/process persistence, making the process-local session-store policy unsafe;
- challenge requirements mandate persistent user profiles/authentication rather than the lightweight challenge progression model;
- evidence needed for the intended 1,000-point Case #042 score changes;
- human art direction changes the approved master character/style enough that A03/A06 prompts/references are no longer valid;
- the required one-complete-live-session gate cannot be executed because of a sustained platform limitation. This becomes an explicit external blocker/ADR; it is not silently waived;
- implementation reveals an irreconcilable contradiction between this file and a higher-precedence current challenge/V3 requirement.

Ordinary implementation details, library choices that preserve the contract, code organization refinements and bug fixes do not reopen the specification.

## Definition of Done - MDL-4

Every checkbox is mandatory unless explicitly marked `CONDITIONAL_CASE` in the canonical traceability ledger. If any required item is false, MDL-4 is not complete and MDL-5 must not start.

### Source, branch, and predecessor integrity

- [ ] Definitive V3 source fingerprint/addenda are recorded and valid.
- [ ] Merged MDL-3 predecessor engineering/deployment/art approval gates are green/current.
- [ ] MDL-2 canonical Case/data identities and MDL-3 Genie identities used by MDL-4 are recorded.
- [ ] Branch `MDL-4` was created/continued from green, current `main` with no destructive overwrite of prior branch history.
- [ ] `docs/iterations/MDL-4-report.md` existed as `IN_PROGRESS` from branch start and is the PR evidence source.
- [ ] Final accepted `implementation_sha` contains all runtime-affecting code/config/assets and exact human-approved MDL-4 approval records.
- [ ] Final branch freshness against `origin/main` was verified before acceptance; any rebase/merge invalidation was rerun.
- [ ] Branch was pushed and PR created/updated; required GitHub checks ran on the accepted implementation content.

### Server-authoritative investigation lifecycle

- [ ] Complete Case Board -> Briefing -> Investigation -> Scientific Verdict -> Debrief -> Case Board flow is implemented.
- [ ] No Case #042-specific global result states (`RESULT_1`, `RESULT_2`, `DQ_STAGE`, etc.) exist.
- [ ] Investigation state changes are append-only/replayable; replay reconstructs phase, score, predictions, evidence flags and completion eligibility.
- [ ] Session IDs are unguessable; Case ID is immutable.
- [ ] State revision, idempotency-key behavior, duplicate-request semantics and per-session serialization are implemented/tested.
- [ ] Session TTL/capacity failure is explicit and never silently evicts active Investigations.
- [ ] Production worker topology is compatible with the selected process-local session store, or an approved persistence ADR replaces it.
- [ ] Browser refresh/back/forward recovery follows server projection and cannot roll analytical state backward.
- [ ] MDL-3 pending Genie selection is persisted/consumed exactly once; `/next` never silently reselects the first Experiment.

### Case #042 completion/evidence entitlement

- [ ] Completion contract is versioned and server-authoritative.
- [ ] Blocking Experiment families are exactly `COMPONENT_DECOMPOSITION`, `SNAPSHOT_DIFF`, `DQ_MATERIALITY`, `FORMULA_VALIDATION`, `RECONCILIATION`.
- [ ] DQ and formula validation may occur in either legal Genie-selected order.
- [ ] Completion/progress is derived from events/evidence/contract, never a hardcoded Experiment count or `/3` denominator.
- [ ] Required V2 lineage/comparison inspection blocks final-prediction eligibility until opened.
- [ ] TX-004291 detail inspection is optional for completion but can earn the high-value evidence reward and Evidence Analyst badge condition.
- [ ] Evidence endpoint/inspection only exposes evidence already entitled by the active session.
- [ ] Cross-Case evidence access is impossible.
- [ ] Component, snapshot and final reconciliation residual checks are exact/tolerance-valid and DQ overlap is never additive.

### Predictions and score privacy

- [ ] Initial prediction has exactly four Case #042 choices including `PRED_INSUFFICIENT_EVIDENCE`.
- [ ] Final prediction is a separate field/set and includes `FINAL_INSUFFICIENT_EVIDENCE`.
- [ ] Private correct-answer mappings are not returned in public Case/session/config/OpenAPI/static payloads.
- [ ] Initial-prediction correctness cannot be inferred from a visible score/delta before verdict; score remains hidden during Investigation.
- [ ] Wrong initial prediction never prevents Case completion.

### Scoring, hints, badges, and progression

- [ ] Canonical V3 server-side score-event registry/reducer is implemented and clamps `[0,1000]`.
- [ ] Required-Experiment score is +100 per unique required family, capped at +300 even though #042 has five blocking families.
- [ ] High-value record reward is +100 once; required lineage/comparison reward is +75 once.
- [ ] Debrief is the only path awarding +125 Debrief points and completion/progression mutation.
- [ ] Early reveal is legal only after analytical completion and before final prediction, applies exactly -150 once and records final prediction skipped.
- [ ] `PERFECT` golden score is exactly 1000.
- [ ] `WRONG_INITIAL_CORRECT_FINAL` is exactly 900.
- [ ] `ONE_HINT` is exactly 950.
- [ ] `ALL_THREE_HINTS` is exactly 850.
- [ ] `SKIP_HIGH_VALUE_RECORD` is exactly 900.
- [ ] `EARLY_REVEAL_CORRECT_INITIAL` is exactly 650.
- [ ] `EARLY_REVEAL_WRONG_INITIAL` is exactly 550.
- [ ] Three canonical Case #042 hints use the exact texts/prerequisites and deduct -50 once each.
- [ ] All seven canonical badges are implemented as machine predicates; impossible #042 badges are never falsely awarded.
- [ ] Lightweight progression stores only safe state and server validates completion/unlock/best-score mutation.
- [ ] Replaying #042 does not increment unique-Case completion count; best score keeps the maximum.
- [ ] Unlock state never bypasses server release availability/security.

### API and client contract

- [ ] V3 API endpoint family is implemented with stable envelopes except the documented flat health-probe exception.
- [ ] `GET /api/sessions/{session_id}` returns a safe server projection and performs no unnecessary Genie/SQL mutation.
- [ ] `POST /api/sessions/{session_id}/evidence/inspect` validates entitlement/reward server-side and is idempotent.
- [ ] `POST /api/sessions/{session_id}/debrief` is explicit, idempotent and legal only after an accepted verdict.
- [ ] Error taxonomy/HTTP/retryability semantics are closed and tested.
- [ ] Chat is Case-scoped, length/rate limited, truth-safe and cannot mutate control state/score through model-looking text.
- [ ] OpenAPI and generated frontend API schemas are synchronized.
- [ ] Frontend owns only presentation state; no optimistic analytical/status/score/verdict mutation exists.
- [ ] Generic Experiment Result rendering depends on registered Instrument models, not Case-specific page routing.
- [ ] Unavailable/unknown Case states navigate deterministically without creating a session.

### Scientific Verdict and truth isolation

- [ ] Final synthesis comes from Genie using visible evidence; server independently validates eligibility/numbers/status semantics.
- [ ] Private truth/oracle never enters Genie prompts, instructions, allowed-Experiment selection or ordinary evidence repositories.
- [ ] App backend has only the narrow private validation capability required for scoring/verdict and it is permission-tested.
- [ ] Genie-facing identity remains unable to query private truth.
- [ ] Production frontend/static package contains no private truth fixture/oracle serialization.
- [ ] Case #042 broad H1 final status is `SUPPORTED` while narrow directly reconciled record-impact claims may be `CONFIRMED`.
- [ ] H2 final status is `RULED_OUT` with evidence reason.
- [ ] H3 remains a real `POSSIBLE` signal but is not the primary explanation.
- [ ] V2 source changes reconcile to `-5.90M`, other component effects to `-0.90M`, DQ `-0.30M` is explicitly overlapping/non-additive, residual is `0.00M`.
- [ ] Backend rejects formula-changed/DQ-primary/DQ-absent/V2=-6.8/unsupported-overclaim conclusions.
- [ ] Bounded Genie conclusion repair follows MDL-3; after failure the backend does not fabricate a canned expected answer and present it as Genie.

### Automated testing and CI

- [ ] `python scripts/run_iteration_gate.py --iteration MDL-4 --mode local` passes all deterministic mandatory stages.
- [ ] `scripts/validate_mdl4_contract.py --strict` passes.
- [ ] All MDL-4-owned canonical V3 test IDs have green implementation/evidence mappings.
- [ ] All custom `MDL4-*` required tests are defined once and green.
- [ ] Full fake-Genie Case #042 E2E reaches Debrief with exact score assertions.
- [ ] Wrong initial prediction, one/all hints, early reveal, optional-record skip, refresh/back, double-click/race, reconciliation failure and cross-Case isolation paths are green.
- [ ] Playwright required suite discovers non-zero tests; no mandatory test is skipped/xfail for closure.
- [ ] Required GitHub checks are exactly the ten version-controlled `mdl4/*` contexts and all are green on accepted implementation content.
- [ ] Production package smoke proves unknown `/api/*` never becomes SPA HTML and private/obsolete static assets are not exposed.
- [ ] `game_contract_digest` is current and every reused fake/live/deploy/art evidence artifact resolves to immutable compatible identities.

### Artwork A03/A06

- [ ] MDL-4 artwork generation plan has exactly 10 independent candidate slots: A03 C01-C06 and A06 C01-C04.
- [ ] Every candidate has exact prompt, reference/provenance/tool/model/rights metadata where available, technical preflight and SHA-256.
- [ ] A03 uses the approved A02 master as the identity reference when the generation tool supports references.
- [ ] Deterministic contact sheets include all candidate revisions being reviewed.
- [ ] Human explicitly selects source candidate(s); Codex does not self-select.
- [ ] Production A03 meets the approved transparent portrait convention/size budget.
- [ ] Production A06 is the approved 2560x1440 lab environment derivative/size budget with usable overlay zones.
- [ ] Four required 1440x900 integration previews are generated and reviewed.
- [ ] Human explicitly approves exact production + preview bytes/hashes with external evidence; stale/self-authored/PENDING approval fails.
- [ ] Approved A06 integration does not leave obsolete pixel `board.png` or fantasy-genie hero art as a competing production runtime backdrop.

### Databricks integrated staging proof

- [ ] Accepted implementation identity deploys successfully to the intended staging Databricks App.
- [ ] Offline/fake Genie mode is disabled; the configured live Genie and curated Case #042 data are used.
- [ ] Automated deployed smoke passes health/config/catalog/session shell and negative security/state checks.
- [ ] One complete automated real-Genie Case #042 Investigation reaches Debrief before MDL-4 closure.
- [ ] Live path reaches all five blocking Experiment families in a legal Genie-selected order within the safety bound; application never substitutes the expected path.
- [ ] Any trusted SQL fallback occurs only after a valid Genie Experiment selection and is recorded.
- [ ] Live path inspects TX-004291 and required lineage, uses zero hints, submits correct final prediction, accepts the calibrated verdict and ends with score 1000.
- [ ] Live completion/progression/badge outputs are server-derived and correct.
- [ ] Live artifact contains no raw chain-of-thought, credentials or full private truth and matches current game/data/Genie/deployment identities.
- [ ] Sustained Databricks quota/outage is represented as an explicit external blocker, not a waived live gate.

### Closure and handoff

- [ ] Allowed manual staging inspection is limited to visual/runtime/log review after automation; functional defects acquire automated regression coverage.
- [ ] Iteration report contains all required immutable evidence and no secrets/full private truth.
- [ ] `python scripts/run_iteration_gate.py --iteration MDL-4 --mode closure` passes.
- [ ] PR merges only after exact-head CI, art approval, staging/live proof and report readiness are green.
- [ ] Post-merge `main` CI is green and any main-driven deployment/revalidation is successful.
- [ ] Any post-merge failure follows the inherited recovery-branch protocol rather than being ignored or hidden.
- [ ] Work intentionally deferred to MDL-5/6/7 is explicitly listed with owner iteration.

**If any required checkbox is false, MDL-4 is not closed and MDL-5 must not start.**

