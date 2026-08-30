
# MDL-2 — Case #042 Deterministic Data, Evidence Model, Curated SQL, Lineage, Truth Isolation, and Data Deployment

**Document status:** READY TO IMPLEMENT  
**Iteration:** MDL-2  
**Branch:** `MDL-2`  
**Primary engineering owner:** Case #042 analytical/data contract  
**Predecessor:** MDL-1 must be closed on `main`  
**Definitive source:** `MAD_DATA_LAB_Complete_Game_Specification_and_Manual.md`, Version 3.0, 2026-08-23  
**Accepted V3 source SHA-256:** `237570e5d62cee11e78ecced43c8449f62f53e7b547e9fe1bfbf4ed54eb0cc44`  
**Input draft SHA-256 used for this hardening pass:** `d6a6d15f4fef8c714282617c35968066549a5c24fea35a194a2bfc769ca419a7`  
**Internal deadline policy:** optional scope is reduced before any mandatory data, security, CI, deployment, or human-art gate is weakened.

---

## 0. Purpose

MDL-2 makes **Case #042 — The Missing €6.8M** analytically complete, deterministic, reproducible, auditable, and safe to expose later through Genie.

By the end of this iteration:

- every Case #042 number used by later gameplay is produced from one deterministic source-of-truth data package rather than frontend constants or CSS;
- the same accepted Case template version + generator version + seed produces the same canonical Case package;
- the Case reconciles exactly at metric, component, source-snapshot, and formula levels;
- the misleading DQ signal exists, is numerically quantified, and is explicitly overlapping rather than additive;
- record-level evidence contains the canonical `TX-004291` example;
- value lineage and a clearly labeled technical-lineage representation exist;
- Unity Catalog/Databricks SQL contains public, private, and curated logical surfaces with least-privilege access;
- `CASE_TRUTH` exists for private validation but cannot be read by the browser, ordinary app evidence repository, curated views, or Genie-facing configuration;
- the eight canonical trusted SQL analytical paths are version-controlled, parameterized where application SQL is used, typed, tested, and validated against live Databricks SQL;
- the seed/migration process is idempotent, rollback-capable, and never depends on manual SQL edits;
- GitHub CI proves the deterministic/golden/data/security contracts on the exact accepted branch head;
- the accepted implementation identity is deployed to the staging Databricks App and the deployed data path is smoke-tested;
- the MDL-2-owned analytical instrument artwork is generated, preflighted, explicitly selected by a human, converted to approved production derivatives, and hash-bound to human approval;
- closure evidence is sufficient for MDL-3 to verify MDL-2 without trusting a prose checkbox.

**MDL-2 is a data/evidence iteration.** It does not make Genie choose experiments, does not implement scoring/verdict, and does not build the final Evidence Explorer UI.

---

## 1. Non-negotiable exit conditions

MDL-2 is `COMPLETE` only if all of the following are simultaneously true:

1. MDL-1 predecessor evidence is valid and still matches merged `main`.
2. `MDL-2` was created/continued from current green `main`, with no unrelated dirty work.
3. Case #042 has one schema-valid public template and one isolated private generation/oracle specification.
4. generator output for production seed `42` is deterministic and canonicalized.
5. the canonical generated package passes all Case #042 invariants before persistence.
6. G42-001 through G42-027 pass 100%.
7. required generator/property tests pass, including the required PR/release sample volumes.
8. exact public/private/curated Databricks objects exist in the staging target.
9. all required Case #042 curated queries return the canonical results.
10. application SQL uses native parameters rather than string interpolation.
11. app runtime service principal can read only the required public/curated surfaces and cannot read private truth during MDL-2.
12. no curated view references private truth.
13. no production frontend bundle contains private truth values/fixtures.
14. no public API allows arbitrary table names, SQL, or premature access to not-yet-earned evidence.
15. data seeding is reproducible from repository source and no manual workspace edit is required.
16. data migration/seed rollback evidence exists before closure.
17. required MDL-2 artwork candidates were actually generated; prompt text alone is not completion.
18. exact final art bytes were explicitly approved by a human and CI verifies their hashes.
19. all required GitHub checks are green on the accepted implementation head.
20. real Databricks SQL integration is green.
21. staging deployment and deployed evidence smoke are green.
22. the merged `main` runtime-content digest matches the accepted MDL-2 implementation content.
23. the iteration report/manifest/traceability outputs are complete and non-self-referential.

If one item is false, MDL-2 is not closed and MDL-3 must not begin.

---

## 2. Scope boundaries

### 2.1 MDL-2 owns

MDL-2 owns implementation closure for:

- definitive Case #042 analytical values and reconciliation;
- public Case #042 data template;
- private Case #042 mutation/truth generation specification;
- deterministic generator contract;
- canonical serialization and golden Case package;
- Case #042 mutation implementation;
- data dictionaries and Delta/Unity Catalog objects needed for #042;
- curated Case #042 Genie-facing data model;
- trusted Case #042 SQL paths Q1–Q8;
- SQL repository and typed result schemas;
- Case #042 value/calculation lineage data;
- technical-lineage fallback representation;
- data seeding/migration/verification/rollback;
- data-layer truth isolation;
- generator/property/golden/SQL integration tests;
- MDL-2 analytical-instrument illustration pack defined later in this file.

### 2.2 MDL-2 explicitly does **not** own

Do not implement these as production behavior in MDL-2:

- live Genie orchestration/protocol repair — MDL-3;
- Genie experiment selection — MDL-3;
- Genie benchmark/soak acceptance — MDL-3/MDL-7;
- final player prediction/scoring/badges/verdict — MDL-4;
- full Evidence Explorer entitlement/UI flow — MDL-4/MDL-5;
- final chart/Instrument React implementation and visual regression acceptance — MDL-5;
- final security/chaos/accessibility/performance closure — MDL-6;
- final RC soak/manual functional acceptance — MDL-7;
- final submission package — MDL-8.

### 2.3 No fake completion

The following do **not** count as implementation:

- hardcoding `125.0`, `118.2`, `-6.8`, `-5.9`, `23/2/5`, `TX-004291`, or verdict text inside frontend production components;
- using CSS pseudo-elements to inject DQ evidence;
- creating a static JSON response endpoint that bypasses the generator/repository;
- writing SQL manually in Databricks but not version-controlling it;
- making a private truth endpoint and merely hiding its button;
- granting broad `SELECT` on the private schema because it is “synthetic”;
- creating empty schemas/views that do not contain the golden data;
- generating art prompts without generating candidates;
- marking human approval in Markdown without human evidence.

---

## 3. Source-of-truth and reconciliation decisions

Use this precedence:

1. current challenge/platform constraints;
2. accepted V3 source and approved addenda/ADRs;
3. this MDL-2 implementation contract as a detailed execution mapping;
4. current repository only as migration input;
5. implementation convenience.

### 3.1 V3 sections primarily closed by MDL-2

Primary closure ownership in the eight-iteration ledger:

| V3 section | Subject | MDL-2 closure |
|---|---|---|
| §16 | Definitive Demo Case — Case #042 | exact generated analytical contract |
| §27 | Data Architecture and Data Dictionary | public/private data structures required by #042 |
| §28 | Curated Genie Data Model | #042-relevant curated views |
| §29 | Deterministic Case Generator | generator + canonical serialization |
| §30 | Mutation Engine | shared operator contract + #042 operators |
| §33 | Trusted SQL and Canonical Analytical Paths | Q1–Q8 |
| Appendix A | Reference DDL/views | staging-compatible implementation |
| relevant §40 | truth isolation subset | implemented now; broad security closure remains MDL-6 |
| relevant §44 | generator/data/golden/SQL tests | canonical data-tier ownership |

Do not transfer primary ownership of unrelated V3 sections merely because their tests are rerun here.

### 3.2 Explicit source reconciliations

These are intentional clarifications, not silent edits to V3:

**R2-001 — no `hidden_truth_ref` in the public Case template.**  
The public Case template must not contain a field that directly points a browser/Genie-facing loader toward `CASE_TRUTH`. The private generation/oracle spec is resolved server/deployment-side by validated `case_id` through a separate registry.

**R2-002 — Case #042 does not allow an `INSUFFICIENT_EVIDENCE` scientific verdict.**  
The player must later be offered “Insufficient evidence” as a **prediction option**, but the canonical Case #042 generated evidence is intentionally sufficient. Therefore:
- prediction option may exist later;
- `case_0042_v1` completion/oracle contract sets `allows_insufficient_evidence_verdict: false`.

**R2-003 — no final-prediction requirement is encoded in the data template.**  
MDL-4 owns the final prediction / early-reveal scoring behavior. The data template encodes analytical completion requirements, not UI sequencing.

**R2-004 — V3’s `58d7...demo` formula hash is demonstrative, not a literal production hash.**  
MDL-2 locks a canonical normalized formula string and SHA-256 algorithm. The production hash for:

```text
V1 + V2 - V3 + V4
```

is:

```text
d1b885360649e8a8cd7322d54a221a9041459b709e49f8444f140c1727fcaf65
```

Previous/current formula hashes must equal this value unless an approved source addendum later changes normalization.

**R2-005 — Case #042 key art A21 is predecessor-owned.**  
The hardened MDL-1 already generated/approved A21. MDL-2 must verify and reuse its approved hash; it must **not** silently regenerate the Case card art. MDL-2 artwork instead covers analytical instruments A08–A12, which correspond directly to the evidence built here.

**R2-006 — existence of evidence is not browser entitlement to evidence.**  
MDL-2 builds the data and repository. It does not expose all future evidence through an unrestricted production endpoint. The player-facing evidence route becomes fully active only after MDL-4 provides server-authoritative evidence entitlements.

**R2-007 — app runtime does not need private truth in MDL-2.**  
MDL-2 therefore denies app runtime `SELECT` on the private schema. A staging deployment/test identity may read private truth only for generator/release validation. MDL-4 must explicitly justify any later runtime access.

Record these decisions in `docs/decisions/` or the existing ADR mechanism established by MDL-1.

---

## 4. Mandatory execution order

Codex must execute MDL-2 in this order. Engineering and art generation may overlap after the predecessor/branch gates, but closure order is strict.

| Phase | Required action | Exit condition |
|---:|---|---|
| 0 | Read this whole file, accepted V3 source/addenda, MDL-1 closure evidence, repository `main`, and current Databricks platform verification. | No unresolved predecessor/source ambiguity. |
| 1 | Verify MDL-1 closure hashes/approval/main CI/runtime digest and clean current `main`. | Predecessor gate green. |
| 2 | Create or safely continue `MDL-2`; create `MDL-2-report.md` as `IN_PROGRESS`; push branch and create/update PR. | Branch/base/PR identity recorded. |
| 3 | Start A08–A12 artwork generation from locked prompts/candidate slots. | Generation plan + first candidate jobs recorded. |
| 4 | Implement public/private Case specs, generator, mutations, canonical package, validators, fixtures. | Local deterministic + G42 data contract green. |
| 5 | Implement DDL/views/SQL repository/typed result models/seed scripts. | Static SQL/schema/privacy tests green. |
| 6 | Run local full data gate + required 500-sample PR property suite; produce machine-readable reports. | Local/PR deterministic gates green. |
| 7 | Deploy/seed staging data with controlled migration workflow; run real SQL integration. | Live SQL + privilege/truth-isolation gates green. |
| 8 | Human selects/approves exact A08–A12 production bytes; CI validates evidence/hashes. | Human art gate green. |
| 9 | Commit all runtime/data/art changes, refresh against `origin/main`, rerun required GitHub CI on exact head, declare `implementation_sha`, deploy accepted identity and smoke-test. | Exact-head CI + deploy green. |
| 10 | Perform allowed manual inspection, finalize closure evidence, merge, verify `main`, and produce predecessor record for MDL-3. | MDL-2 `COMPLETE`. |

Do not defer live SQL integration, private-access denial, human art approval, or post-merge verification as “administrative follow-up.”

---

## 5. Predecessor entry gate — MDL-1 must be provably closed

Before touching production code/data:

```bash
git fetch origin --prune
git checkout main
git pull --ff-only origin main
test -z "$(git status --porcelain)"
```

Verify and record:

- MDL-1 PR merged;
- current `main` contains the accepted MDL-1 runtime content;
- `main` required CI is green;
- MDL-1 staging deployment evidence is green;
- MDL-1 runtime-content digest equals the accepted predecessor digest;
- MDL-1 source baseline points to accepted V3 SHA/addenda;
- A01/A02/A21/A28 approval records are `APPROVED`;
- exact approved A21 hash still matches the bytes;
- the human approval evidence references the expected human reviewer;
- no later runtime-affecting commit invalidated MDL-1 without rerunning its gates.

Create/update:

```text
docs/traceability/MDL-2-predecessor.json
```

Minimum fields:

```json
{
  "predecessor": "MDL-1",
  "main_sha": "...",
  "main_tree_sha": "...",
  "runtime_digest": "...",
  "mdl1_pr": "...",
  "mdl1_ci_evidence": ["..."],
  "mdl1_deployment_evidence": ["..."],
  "v3_source_sha256": "237570e5d62cee11e78ecced43c8449f62f53e7b547e9fe1bfbf4ed54eb0cc44",
  "a21_sha256": "...",
  "a21_human_approval_evidence": "...",
  "verified_at_utc": "...",
  "status": "PASS"
}
```

If the predecessor evidence cannot be proven, stop with an explicit `BLOCKED_PREDECESSOR_*` state. Do not recreate or reinterpret MDL-1 evidence inside MDL-2.

---

## 6. Git branch, PR, and closure identity

### 6.1 Create/continue branch safely

```bash
git fetch origin --prune
git checkout main
git pull --ff-only origin main
test -z "$(git status --porcelain)"
git rev-parse HEAD
git rev-parse HEAD^{tree}
git checkout -b MDL-2
```

If `MDL-2` exists:

```bash
git branch -vv
git log --oneline --decorate --graph --max-count=40 --all
git merge-base origin/main MDL-2
```

Never delete/recreate or force-push the branch merely because it is inconvenient.

### 6.2 Create the iteration report skeleton immediately

Before opening the PR:

```text
docs/iterations/MDL-2-report.md
```

Initial fields:

```text
status: IN_PROGRESS
iteration: MDL-2
base_main_sha
base_main_tree
v3_source_sha
predecessor_record
scope
known_blockers
art_status: GENERATION_PENDING
sql_integration_status: NOT_RUN
deployment_status: NOT_RUN
```

The file must exist before using it as a PR body.

### 6.3 Recommended commit sequence

Small reviewable commits, for example:

```text
MDL-2: add Case 042 public/private generation contracts
MDL-2: implement deterministic generator and canonical fixture
MDL-2: add Delta schemas and curated evidence views
MDL-2: add trusted SQL repository and typed results
MDL-2: add truth-isolation and data migration controls
MDL-2: add golden property and SQL integration coverage
MDL-2: add approved analytical instrument artwork
MDL-2: finalize iteration closure evidence
```

Before commits:

```bash
git diff --check
```

### 6.4 Push and PR

```bash
git push -u origin MDL-2
gh pr create \
  --base main \
  --head MDL-2 \
  --title "MDL-2 Case 042 deterministic evidence and curated SQL" \
  --body-file docs/iterations/MDL-2-report.md
```

If a PR already exists, update it.

### 6.5 Final branch freshness

Immediately before designating `implementation_sha`:

```bash
git fetch origin --prune
git merge-base --is-ancestor origin/main HEAD
git status --porcelain
```

The working tree must be clean and current `origin/main` must be an ancestor. If not, refresh the branch and rerun every invalidated gate.

### 6.6 Closure identity

Use the MDL-1 inherited two-identity model:

- `implementation_sha`: final runtime/data/art-affecting accepted commit;
- optional later `report_commit_sha`: documentation-only closeout commit;
- `implementation_runtime_digest`: deterministic digest of runtime-affecting paths;
- `merge_sha`: recorded externally after merge.

Unknown paths are runtime-affecting until the shared `classify_change.py` says otherwise.

Data/SQL/schema/Case/private-spec/fixture/art-manifest changes are always runtime-affecting in MDL-2.

---

## 7. Target repository changes

MDL-2 must result in this data/evidence surface, using equivalent paths only when the MDL-1 repository architecture differs and the mapping is recorded:

```text
cases/
  templates/
    case_0042.yaml
    case_0107.yaml
    case_0213.yaml
    case_0314.yaml
    case_0441.yaml
    case_0520.yaml
    case_0812.yaml
  completion_contracts/
    case_0042_v1.yaml
  schemas/
    case_template.schema.json
    completion_contract.schema.json

data/
  ddl/
    001_schemas.sql
    010_case_definition.sql
    011_datapoint_result.sql
    012_calculation_trace.sql
    013_source_snapshot.sql
    014_source_record.sql
    015_snapshot_diff.sql
    016_quality_issue.sql
    017_pipeline_run_evidence.sql
    018_semantic_change_evidence.sql
    019_technical_lineage_curated.sql
    020_private_case_truth.sql
  views/
    100_case_summary.sql
    110_component_evidence.sql
    120_snapshot_evidence.sql
    130_quality_evidence.sql
    140_semantic_evidence.sql
    150_pipeline_evidence.sql
    160_population_evidence.sql
    170_lineage_evidence.sql
  generation/
    __init__.py
    models.py
    canonical.py
    stable_rng.py
    generator.py
    mutations.py
    validators.py
    case_0042.py
    private_specs/
      case_0042_v1.yaml
    property_templates/
      level1_clean.yaml
      level2_noisy.yaml
  fixtures/
    public/
      case_0042.bundle.json
      case_0042_public.json
      case_0042_component_evidence.json
      case_0042_snapshot_evidence.json
      case_0042_quality_evidence.json
      case_0042_semantic_evidence.json
      case_0042_lineage_evidence.json
    hashes/
      case_0042.sha256
  validation/
    case_0042.py
    schema_privacy.py
    sql_contracts.py

backend/
  data/
    models.py
    sql_client.py
    repositories.py
    queries.py
    validators.py
    private_truth_repository.py
  api/
    # production Evidence Explorer route remains entitlement-gated/incomplete
    # until MDL-4; no debug/private route

sql/
  trusted/
    observation.sql
    component_decomposition.sql
    snapshot_summary.sql
    highest_impact_records.sql
    dq_materiality.sql
    formula_validation.sql
    value_lineage.sql
    reconciliation.sql

tests/
  data/
  contracts/
  security/
  fixtures/
    private/
      case_0042_truth.json

scripts/
  generate_cases.py
  validate_cases.py
  seed_databricks.py
  verify_databricks_data.py
  snapshot_case_data.py
  restore_case_data.py
  compute_mdl2_data_digest.py
  fingerprint_databricks_objects.py
  verify_databricks_permissions.py
  build_mdl2_art_review.py
  validate_mdl2_contract.py
  run_iteration_gate.py   # extend MDL-1 shared runner

assets/
  review/MDL-2/
    A08/
    A09/
    A10/
    A11/
    A12/
    contact-sheets/
    previews/
    art-generation-plan.json
  production/images/instruments/
  image_prompts.md
  art_source_manifest.yaml

docs/
  approvals/
    MDL-2-art.md
  iterations/
    MDL-2-report.md
  traceability/
    MDL-2-predecessor.json
    mdl2-tests.csv
    mdl2-platform-verification.md
    mdl2-data-contract.json

release-report/
  MDL-2/
    golden-case.json
    generator.json
    privacy-static.json
    schema-fingerprint.json
    data-contract-digest.json
    art-preflight.json
    sql-integration.json
    deployed-smoke.json
    # generated/CI artifact outputs; do not create self-referential commit loops
```

Private fixtures must never be copied into `frontend/`, Vite `public/`, or static production output.

---


## 8. Canonical Case #042 public template

Create `cases/templates/case_0042.yaml` with this logical contract. Exact serialization can differ only if the shared schema requires it.

```yaml
case_id: CASE_0042
public_number: 42
slug: the-missing-6-8m
title: "The Missing €6.8M"
hook: "€6.8M vanished from Capital Available."
difficulty: LEVEL_2
seed: 42
generator_version: 1
case_template_version: 1
release_state: CORE
status: ACTIVE
sort_order: 10

primary_metric: CAPITAL_AVAILABLE
learning_objectives:
  - DECOMPOSITION
  - SNAPSHOT_DIFF
  - DQ_MATERIALITY
  - LINEAGE

observation_contract:
  datapoint_id: CAPITAL_AVAILABLE
  metric_label: Capital Available
  entity_id: PT001
  period_id: "2026-07"
  currency: EUR
  scale: MILLIONS
  expected_value: "125.00"
  observed_value: "118.20"
  deviation: "-6.80"

hypothesis_families:
  - SOURCE_VALUES_CHANGED
  - FORMULA_CHANGED
  - DATA_QUALITY_ISSUE

expected_experiment_families:
  - COMPONENT_DECOMPOSITION
  - SNAPSHOT_DIFF
  - DQ_MATERIALITY
  - FORMULA_VALIDATION
  - RECONCILIATION

required_evidence_tags:
  - COMPONENT_IMPACT
  - SNAPSHOT_IMPACT
  - FORMULA_VERSION

encouraged_evidence_actions:
  - SOURCE_RECORD_INSPECTION
  - VALUE_LINEAGE
  - TECHNICAL_LINEAGE

completion_contract: case_0042_v1
art_asset_id: CASE_0042_KEY_ART
```

Rules:

- numeric story values are stored as decimal-safe strings in YAML/schema loading, never binary floats;
- the generator must independently recompute and validate them;
- the browser never reads this YAML file directly;
- there is no `hidden_truth_ref`, `primary_cause`, expected final status, or path oracle field;
- there is no final-prediction UI rule here;
- `case_id`, release state, and learning objectives agree with the catalog created in MDL-1.

### 8.1 Completion contract

Create `cases/completion_contracts/case_0042_v1.yaml`:

```yaml
contract_id: case_0042_v1
case_id: CASE_0042
version: 1

required_experiment_families:
  - COMPONENT_DECOMPOSITION
  - SNAPSHOT_DIFF
  - DQ_MATERIALITY
  - FORMULA_VALIDATION
  - RECONCILIATION

required_evidence_tags:
  - COMPONENT_IMPACT
  - SNAPSHOT_IMPACT
  - FORMULA_VERSION

required_reconciliation:
  metric_tolerance_abs: "0.01"
  primary_component_tolerance_abs: "0.01"
  final_unreconciled_tolerance_abs: "0.01"

allows_insufficient_evidence_verdict: false
```

The later game flow may additionally reward source-record and lineage inspection. Do not make the completion data contract dictate MDL-4 scoring mechanics.

---

## 9. Private generation/oracle specification

Create a non-browser, non-Genie-loaded spec such as:

```text
data/generation/private_specs/case_0042_v1.yaml
```

This is **private in the application architecture**, not a secret credential. It may be committed because all data is synthetic, but:

- frontend build cannot import it;
- ordinary public API cannot return it;
- Genie data configuration cannot reference it;
- app runtime has no private-table access in MDL-2;
- only generation/release test code loads it.

Logical content:

```yaml
case_id: CASE_0042
case_template_version: 1
generator_version: 1

primary_mutation:
  family: SOURCE_RECORD_CHANGE
  target_component: V2

secondary_signal:
  family: DUPLICATE_BUSINESS_KEY
  causal_role: OVERLAPPING_SECONDARY_SIGNAL
  affected_row_count: 5
  estimated_overlapping_impact: "-0.30"

expected_truth:
  primary_component: V2
  primary_source: finance_reporting_source
  primary_cause: SOURCE_RECORD_CHANGE
  secondary_cause: DUPLICATE_BUSINESS_KEY
  expected_primary_impact: "-5.90"
  expected_total_deviation: "-6.80"
  formula_changed: false
  confidence: HIGH

expected_path_oracle:
  must_include:
    - COMPONENT_DECOMPOSITION
    - SNAPSHOT_DIFF
    - DQ_MATERIALITY
    - FORMULA_VALIDATION
    - RECONCILIATION
```

MDL-3 may refine the permitted path/orchestration oracle. MDL-2 only stores the private analytical expectation needed for tests.

---

## 10. Deterministic generator contract

### 10.1 Public interface

Implement:

```python
generate_case(
    case_template_id: str,
    seed: int | None = None,
    generator_version: int | None = None,
    *,
    mode: Literal["release", "property_test"] = "release",
) -> GeneratedCase
```

Release behavior:

- shipping Case #042 defaults to template seed `42`;
- production/release code must reject accidental non-42 override unless a specifically named test/development override is used;
- `mode="property_test"` may exercise derived seeds/templates without changing the canonical release artifact.

This prevents a test feature from accidentally changing the challenge story.

### 10.2 Required generator phases

The generator must be a pipeline with observable phase failures:

```text
LOAD_TEMPLATE
VALIDATE_TEMPLATE
LOAD_PRIVATE_SPEC
RESOLVE_VERSIONS_AND_SEED
BUILD_BASELINE_RECORDS
COMPUTE_PREVIOUS_METRIC
APPLY_PRIMARY_MUTATION
APPLY_SECONDARY_SIGNAL
MATERIALIZE_CURRENT_RECORDS
COMPUTE_CURRENT_METRIC
BUILD_SNAPSHOT_DIFF
BUILD_DQ_EVIDENCE
BUILD_SEMANTIC_EVIDENCE
BUILD_CALCULATION_LINEAGE
BUILD_TECHNICAL_LINEAGE_FALLBACK
BUILD_PRIVATE_TRUTH
VALIDATE_GLOBAL_INVARIANTS
VALIDATE_CASE_0042_INVARIANTS
CANONICALIZE
HASH
PERSIST_FIXTURES
```

`PERSIST_FIXTURES` may execute only after every validation phase passes.

### 10.3 Stable PRNG

Do not rely on:

- Python process hash randomization;
- set iteration;
- filesystem ordering;
- locale;
- wall clock;
- default UUID randomness;
- implicit library sampling behavior.

Preferred portable stable RNG for generated IDs/selection:

```text
digest = SHA256(
  f"{case_id}|{case_template_version}|{generator_version}|{seed}|{namespace}|{counter}"
)
```

Map digest bytes deterministically to the desired choice/range.

A standard explicitly seeded PRNG is allowed only if its algorithm/version is frozen by tests and documented. Hash-derived deterministic selection is preferred because it is portable across Python versions.

### 10.4 Monetary arithmetic

Use Python `Decimal`, never `float`, for generation and validation.

Canonical quantum:

```python
MONEY_QUANTUM = Decimal("0.01")
```

Rules:

- convert from strings;
- quantize explicitly;
- define rounding mode even where no rounding is expected;
- SQL uses `DECIMAL(18,2)`;
- JSON uses decimal strings for canonical fixtures;
- API models may serialize numbers later, but canonical hashes never depend on binary float rendering.

### 10.5 Time determinism

Canonical Case #042 timestamps are template-owned constants:

```text
previous_run_ts = 2026-08-02T09:00:00Z
current_run_ts  = 2026-08-03T09:00:00Z
```

`generated_at` or CI timestamps are metadata and must be excluded from the canonical Case content hash.

### 10.6 Deterministic creation metadata

`case_definition.created_at` must not use the wall clock for the canonical release Case. Set it deterministically from the Case contract, preferably:

```text
created_at = current_run_ts = 2026-08-03T09:00:00Z
```

If operational seed/deploy time is useful, record it in the seed/deployment evidence manifest, not inside the canonical Case payload.

This ensures Databricks rows can be re-seeded without changing the canonical Case hash merely because the job ran on another day.

### 10.7 ID determinism

Case #042 stable IDs include:

```text
CASE_0042
CAPITAL_AVAILABLE
RUN_0042_PREVIOUS
RUN_0042_CURRENT
SNAP_20260802_0900
SNAP_20260803_0900
DQ_0042_01
```

No UUID is required for canonical data rows.

---


## 11. Mutation engine registry and semantics

MDL-2 closes the shared mutation-engine contract without implementing full secondary Cases.

Create a closed operator enum/registry:

```text
VALUE_CHANGE
MISSING_ROWS
NEW_ROWS
DUPLICATE_KEYS
PIPELINE_REPLAY
FORMULA_CHANGE
FILTER_CHANGE
ENTITY_MIX
JOIN_CARDINALITY
MULTI_CAUSE
```

Each operator must define:

```text
operator_id
input preconditions
deterministic selection namespace
mutation payload schema
affected-record semantics
impact calculation semantics
private truth contribution
public evidence emitted
validation function
whether it can be primary/secondary
```

### 11.1 Operator implementation status in MDL-2

| Operator | MDL-2 requirement |
|---|---|
| `VALUE_CHANGE` | fully implemented and used by Case #042 |
| `MISSING_ROWS` | fully implemented and used by Case #042 |
| `NEW_ROWS` | fully implemented and used by Case #042 |
| `DUPLICATE_KEYS` | engine semantics implemented/tested with property template; Case #042 uses only its DQ warning/output semantics so it does not alter locked metric totals |
| `PIPELINE_REPLAY` | typed contract + deterministic unit/property implementation sufficient for later #107; not enabled in a released Case |
| `FORMULA_CHANGE` | typed contract + deterministic property implementation; not enabled for #042 |
| `FILTER_CHANGE` | typed contract + deterministic property implementation; not enabled for #042 |
| `ENTITY_MIX` | typed contract + deterministic property implementation; not enabled for #042 |
| `JOIN_CARDINALITY` | typed contract + deterministic property implementation; not enabled for #042 |
| `MULTI_CAUSE` | composition contract + property tests proving independent attribution; no released multi-cause Case yet |

This work is deliberately data-engine-only. It does not enable #107–#812.

### 11.2 Mutation budgets

Property templates must enforce the V3 difficulty semantics:

**Level 1**

```text
one causal family
primary causal signal normally >= 90% of anomaly
2-3 experiments likely sufficient later
little/no misleading noise
```

**Level 2**

```text
one primary cause
0-1 misleading secondary signal
primary contribution normally 65-100% of anomaly, according to template
all remaining contribution explicitly reconciled
```

**Level 3**

MDL-2 only implements the composition semantics/tests; it does not need a released Level 3 Case.

### 11.3 Test-only property templates

Create:

```text
data/generation/property_templates/level1_clean.yaml
data/generation/property_templates/level2_noisy.yaml
```

These are not Case Board content and not release Cases. They exist only so DG/DP property suites exercise:

- seed variation;
- one-cause clean behavior;
- one-cause + secondary-noise behavior;
- DQ causal vs non-causal semantics;
- formula/filter/join operator invariants;
- multi-cause attribution composition where applicable.

They must be unmistakably marked without inventing a new MDL-1 release-state enum value:

```text
release_state: ARCHIVED
test_only: true
public_case: false
```

If property templates use a dedicated schema rather than the production Case-template schema, `release_state` may be omitted entirely; `test_only: true` and exclusion from the Case catalog remain mandatory.

No test-only template may appear in `/api/cases` or the frontend build.

### 11.4 Case #042 and `DUPLICATE_KEYS`

The V3 Case/operator mapping calls the DQ issue a duplicate-key warning. MDL-2 preserves the locked numeric story by treating the five Case #042 affected keys as the deterministic **quality-rule evidence** associated with the duplicate-key operator semantics, not as additional physical current-snapshot rows that would change V2 from `24.10`.

The full physical duplicate-row operator is still implemented/tested through property templates and later powers Case #107.

Do not create hidden extra rows in Case #042 merely to make the word “duplicate” literal; doing so would either double-count the anomaly or create a second incompatible source-of-truth.

### 11.5 Operator purity

Mutation functions must:

- accept immutable/copy-safe input;
- return new deterministic output/evidence;
- not mutate global RNG state;
- not read wall clock;
- not perform Databricks I/O;
- not persist partial output;
- not inspect hidden truth to decide what evidence should say.

Truth is produced from the applied mutation, not used to fake it.

---

## 12. Exact Case #042 deterministic source-record plan

The implementation must generate the following analytical result **from source records**, not merely insert the aggregate results.

### 12.1 Component-level targets

```text
Formula: Capital Available = V1 + V2 - V3 + V4

PREVIOUS
V1 = 100.10
V2 =  30.00
V3 =   5.10
V4 =   0.00
metric = 125.00

CURRENT
V1 =  98.90
V2 =  24.10
V3 =   4.80
V4 =   0.00
metric = 118.20
```

Metric contribution deltas:

```text
V1  -1.20
V2  -5.90
V3  +0.30   # raw V3 source changed -0.30, but V3 is subtracted
V4   0.00
------------
    -6.80
```

### 12.2 Exact V2 business-key plan

Use the canonical V2 key plan below unless a human-approved addendum replaces it.

#### MODIFIED — 23 rows, total source impact `-5.20`

| Keys | Count | Previous each | Current each | Impact each | Total impact |
|---|---:|---:|---:|---:|---:|
| `TX-004291` | 1 | 4.20 | 0.00 | -4.20 | -4.20 |
| `TX-004292`..`TX-004296` | 5 | 0.50 | 0.44 | -0.06 | -0.30 |
| `TX-004297`..`TX-004311` | 15 | 0.50 | 0.46 | -0.04 | -0.60 |
| `TX-004312`..`TX-004313` | 2 | 0.50 | 0.45 | -0.05 | -0.10 |
| **Total** | **23** |  |  |  | **-5.20** |

#### REMOVED — 2 rows, total `-0.80`

```text
TX-004314  previous 0.50 -> absent/current null   impact -0.50
TX-004315  previous 0.30 -> absent/current null   impact -0.30
```

#### ADDED — 5 rows, total `+0.10`

```text
TX-004316..TX-004320
previous null -> current 0.02 each
5 * 0.02 = +0.10
```

#### UNCHANGED V2 — 14 rows

```text
TX-004321..TX-004334
previous 1.00
current 1.00
```

Check:

```text
previous V2:
modified previous 15.20
+ removed previous 0.80
+ unchanged 14.00
= 30.00

current V2:
modified current 10.00
+ added 0.10
+ unchanged 14.00
= 24.10
```

### 12.3 Exact DQ overlap keys

The DQ signal affects exactly these five modified rows:

```text
TX-004292
TX-004293
TX-004294
TX-004295
TX-004296
```

Their source impacts sum to:

```text
5 * -0.06 = -0.30
```

Therefore the quality issue may truthfully report:

```text
affected_row_count = 5
estimated_impact = -0.30
impact_is_overlapping = true
```

This `-0.30` is a **subset of the already counted V2 `-5.90` source movement**. It must never be added again to the metric reconciliation.

The DQ rule result is stored in `quality_issue`; source records do not manufacture extra physical duplicates that would change the component total. The quality rule represents deterministic upstream-scanner metadata over the five affected keys. This distinction must be explicit in developer documentation so a future maintainer does not “fix” the warning by inserting duplicate source rows and thereby break the golden Case.

### 12.4 Simple canonical records for other components

At minimum produce source records whose totals are exact:

```text
V1-BASE-001: 100.10 -> 98.90
V3-BASE-001:   5.10 ->  4.80
V4-BASE-001:   0.00 ->  0.00
```

All are:

```text
entity_id = PT001
period_id = 2026-07
source_table = finance_reporting_source
source_column = amount
```

The generator may split these totals into multiple deterministic rows later, but changing the canonical release fixture requires a deliberate golden update because record-level evidence would change.

### 12.5 Snapshot row counts

With the canonical plan:

```text
previous V2 rows = 23 modified + 2 removed + 14 unchanged = 39
current  V2 rows = 23 modified + 5 added  + 14 unchanged = 42

plus one V1, one V3, one V4 row:
previous source snapshot row_count = 42
current source snapshot row_count  = 45
```

Do not include the DQ diagnostic as extra physical rows.

### 12.6 Exact `source_record` field semantics

Case #042 release fixtures must use one unambiguous row-state convention so local fixtures, Delta rows, population hashes, and SQL integration cannot disagree.

For every Case #042 `source_record` row:

```text
entity_id = PT001
period_id = 2026-07
segment_id = NULL
record_status = ACTIVE
included_by_filter = true
source_table = finance_reporting_source
source_column = amount
```

`changed_from_previous` means **whether this row in the represented snapshot differs from the immediately previous Case snapshot**, not whether the business key ever changed historically.

Therefore:

```text
PREVIOUS snapshot rows:
  changed_from_previous = false for every row

CURRENT snapshot:
  MODIFIED rows = true
  ADDED rows    = true
  UNCHANGED rows = false
```

Removed rows do not exist in the CURRENT `source_record` snapshot; their removal is represented in `snapshot_diff`.

For Case #042:

```text
V1-BASE-001 current changed_from_previous = true
V3-BASE-001 current changed_from_previous = true
V4-BASE-001 current changed_from_previous = false
```

The five DQ-affected V2 business keys do **not** create physical duplicate rows in this curated source snapshot. `duplicate_group_id` is `NULL` for Case #042 release `source_record` rows.

This is deliberate. `DQ_0042_01` represents deterministic **upstream DQ scanner metadata** about those five business keys. It is a real warning that overlaps the V2 changed-record evidence, but the curated evidence snapshot has already normalized the population and must not manufacture extra rows that would alter the locked 23/2/5 counts or V2 totals.

### 12.7 Exact pipeline/run evidence for Case #042

Even though pipeline replay is not causal in Case #042, populate deterministic run evidence so the shared schema is non-empty and future Cases do not need a different shape.

Use:

```text
previous pipeline_run_id = RUN_0042_20260802_0900
current  pipeline_run_id = RUN_0042_20260803_0900

previous run_ts = 2026-08-02T09:00:00Z
current  run_ts = 2026-08-03T09:00:00Z

execution_status = SUCCESS
replay_of_run_id = NULL
previous rows_written = 42
current  rows_written = 45
duplicate_rows_written = 0 for both runs
```

`source_snapshot.pipeline_run_id` must reference the corresponding deterministic run ID.

The DQ warning must **not** cause `duplicate_rows_written > 0` in Case #042 because it is diagnostic metadata, not the causal pipeline-replay operator used by Case #107.

### 12.8 Canonical DQ row representation

Store `quality_issue.affected_keys` as canonical JSON text with sorted keys and no insignificant whitespace:

```json
["TX-004292","TX-004293","TX-004294","TX-004295","TX-004296"]
```

Required row values:

```text
issue_id = DQ_0042_01
rule_name = DUPLICATE_BUSINESS_KEY
severity = MEDIUM
affected_row_count = 5
estimated_impact = -0.30
impact_is_overlapping = true
status = OPEN
```

`OPEN` here is the DQ issue lifecycle status, **not** an epistemic hypothesis status.

Use a stable evidence note whose semantics are equivalent to:

```text
Five V2 business keys are flagged by the upstream duplicate-key quality rule.
Their estimated -0.30M impact overlaps V2 snapshot evidence and is not additive.
```

The note is evidence metadata, not a causal verdict.

### 12.9 Canonical population-hash algorithm

`datapoint_result.population_hash` must be reproducible and must not depend on Spark/SQL row order.

For each snapshot:

1. take only `source_record` rows with `included_by_filter = true`;
2. sort by `(component, business_key)`;
3. serialize each row with UTF-8 and the exact field order below;
4. format monetary amounts with exactly two decimal places;
5. encode booleans as lowercase `true`/`false`;
6. encode `NULL` as the empty string;
7. join fields with `|`;
8. join rows with `\n` and **no trailing newline**;
9. SHA-256 the resulting UTF-8 bytes;
10. store lowercase hexadecimal digest.

Field order:

```text
business_key
component
amount
entity_id
period_id
record_status
changed_from_previous
included_by_filter
duplicate_group_id
source_table
source_column
```

The previous and current Case #042 population hashes must differ. Re-running the generator for the same template/generator/seed must reproduce each exact hash.

Create one shared implementation for this algorithm; do not duplicate hash logic independently in Python tests and SQL seed code.

---

## 13. Snapshot-diff semantics

Lock the meaning of fields to avoid later sign bugs:

- `snapshot_diff.old_value` and `new_value` are **source values**;
- `snapshot_diff.impact` is `new_value - old_value` using added/removed null conventions;
- `component_evidence.contribution_delta` is the **formula-signed effect on the final metric**;
- for V1/V2/V4 the source-delta sign equals metric contribution sign;
- for V3, because the metric subtracts V3, raw source impact `-0.30` corresponds to metric contribution `+0.30`.

For Case #042’s V2 snapshot evidence, source impact and metric contribution are identical because V2 is added.

Later visual/Genie layers must not confuse these two concepts.

---

## 14. Formula and semantic evidence

Canonical normalized formula text:

```text
V1 + V2 - V3 + V4
```

Hash algorithm:

```text
SHA-256 over UTF-8 bytes of the exact normalized expression
```

Expected:

```text
formula_id = CAPITAL_AVAILABLE_V1
formula_hash = d1b885360649e8a8cd7322d54a221a9041459b709e49f8444f140c1727fcaf65
formula_changed = false
```

Case #042 also locks one display-safe semantic filter identity so `case_summary` cannot vary by implementation choice:

```text
filter_id = CAPITAL_AVAILABLE_FILTER_V1
normalized_filter = entity_id = 'PT001' AND period_id = '2026-07'
filter_hash = 4021e03fab325c8d9a6b80a4bf67c9ca0521e89454991dce6e42ded143348a16
```

`filter_hash` is SHA-256 over the UTF-8 bytes of the **exact** normalized filter string above. Previous/current filter IDs and hashes are equal for Case #042. Do not introduce a second whitespace/case normalization algorithm in this iteration.

---

## 15. Calculation/value lineage contract

Create a deterministic acyclic graph.

Minimum logical chain:

```text
CAPITAL_AVAILABLE (METRIC)
  ├── V1 (COMPONENT, ADD)
  │    └── finance_reporting_source.amount
  ├── V2 (COMPONENT, ADD)
  │    └── finance_reporting_source.amount
  │         └── SNAP_20260802_0900 / SNAP_20260803_0900
  │              └── changed V2 business-key evidence
  ├── V3 (COMPONENT, SUBTRACT)
  │    └── finance_reporting_source.amount
  └── V4 (COMPONENT, ADD)
       └── finance_reporting_source.amount
```

Required graph properties:

- exactly one metric root;
- all component nodes reach a source;
- no cycles;
- no orphan nodes;
- stable `sequence_no`;
- deterministic node IDs;
- no hidden truth node;
- display-safe labels;
- current/previous source snapshots resolvable.

### 15.1 Technical lineage

If actual Unity Catalog system lineage is not available/reliable in the Free Edition target, materialize the spec’s curated fallback:

```text
lineage_source = SYNTHETIC_FALLBACK
```

Do not label it `UNITY_CATALOG` unless it is truly derived from Unity Catalog lineage.

Minimum fallback relation:

```text
finance_reporting_source.amount
  -> capital_available.metric_value
```

The combined curated lineage view labels value lineage separately from technical fallback provenance.

---

## 16. Canonical serialization and Case package hash

### 16.1 Canonical package

Generate one aggregate canonical file:

```text
data/fixtures/public/case_0042.bundle.json
```

It contains only public/generated evidence required to reproduce later gameplay. Private truth is excluded.

Logical top-level order is irrelevant because canonical serialization sorts object keys, but required top-level domains are:

```text
schema_version
case_definition
datapoint_results
calculation_trace
source_snapshots
source_records
snapshot_diff
quality_issues
semantic_evidence
pipeline_evidence
technical_lineage
curated_expected_outputs
```

### 16.2 Serialization rules

Canonical serialization must:

- UTF-8;
- newline `\n`;
- JSON object keys lexicographically sorted;
- no insignificant whitespace;
- all strings Unicode-normalized to NFC before JSON serialization;
- decimals serialized as fixed two-decimal strings where monetary;
- UTC timestamps serialized as `YYYY-MM-DDTHH:MM:SSZ`;
- arrays sorted by explicit stable keys, never insertion luck;
- booleans lowercase JSON values;
- null represented as JSON `null`;
- exclude generation time, machine path, username, CI run ID, and other environment metadata.

Required stable array sort keys:

```text
case_definition: case_id
datapoint_results: (case_id, run_ts, run_id)
calculation_trace: (case_id, sequence_no, node_id)
source_snapshots: (case_id, as_of_ts, snapshot_id)
source_records: (case_id, snapshot_id, component, business_key)
snapshot_diff: (case_id, component, business_key, change_type)
quality_issues: (case_id, issue_id)
semantic_evidence: (case_id, semantic_type, previous_id, current_id)
technical_lineage: (case_id, source_table, source_column, target_table, target_column)
```

### 16.3 Hash

```text
case_0042.sha256 = SHA256(canonical_bytes(case_0042.bundle.json))
```

The hash is generated by code and committed only after the intended golden fixture is reviewed by tests. Do not type a guessed hash into this document.

Any later hash change requires:

1. failing golden test;
2. explicit review of the canonical diff;
3. an ADR/addendum if story truth changed;
4. deliberate golden update;
5. rerun of all dependent data/Genie/UI tests.

---


## 17. Databricks data architecture

### 17.1 Three-level naming

Use one configured Unity Catalog catalog plus three logical schemas:

```text
${MDL_CATALOG}.mad_data_lab_public
${MDL_CATALOG}.mad_data_lab_private
${MDL_CATALOG}.mad_data_lab_curated
```

Do not assume the unqualified two-level examples from V3 will resolve identically in every workspace.

`MDL_CATALOG` is environment configuration/deployment metadata, not business logic.

Do not create a new catalog automatically if the Free Edition workspace already supplies an appropriate workspace catalog. Select the target during MDL-1/MDL-2 platform setup and record it in sanitized environment documentation.

### 17.2 Runtime versus deployment identity

Separate privileges:

| Identity | Intended role |
|---|---|
| GitHub/Databricks deployment identity | create/alter/seed/verify staging schemas/tables/views; read private truth for release validation |
| Databricks App runtime service principal | `CAN USE` warehouse + `USE CATALOG`/`USE SCHEMA` + `SELECT` only on required public/curated objects |
| Genie Agent | MDL-3 config; curated data only, never private |
| Browser user | no direct warehouse/table credentials |
| Local fixture tests | no Databricks access |

During MDL-2, **do not grant the App runtime service principal `SELECT` on `mad_data_lab_private`**.

Current Databricks authorization requires `USE CATALOG`, `USE SCHEMA`, and `SELECT` to read Unity Catalog objects. The app resource also needs `CAN USE` on the SQL warehouse. Keep the grants object-specific/schema-specific rather than granting broad catalog access.

### 17.3 Public tables

Implement the V3 logical data dictionary.

#### `case_definition`

Required columns:

```text
case_id STRING
public_number INT
slug STRING
seed BIGINT
generator_version INT
case_template_version INT
title STRING
hook STRING
datapoint_id STRING
entity_id STRING
period_id STRING
expected_value DECIMAL(18,2)
observed_value DECIMAL(18,2)
deviation DECIMAL(18,2)
currency STRING
scale STRING
difficulty STRING
release_state STRING
sort_order INT
required_case_ids STRING
learning_objectives STRING
status STRING
created_at TIMESTAMP
```

#### `datapoint_result`

```text
case_id STRING
datapoint_id STRING
entity_id STRING
period_id STRING
run_id STRING
run_ts TIMESTAMP
run_role STRING
value DECIMAL(18,2)
expected_value DECIMAL(18,2)
deviation DECIMAL(18,2)
formula_id STRING
formula_hash STRING
filter_id STRING
filter_hash STRING
population_hash STRING
```

Case #042:

```text
PREVIOUS value=125.00 expected_value=125.00 deviation=0.00
CURRENT  value=118.20 expected_value=125.00 deviation=-6.80
```

#### `calculation_trace`

```text
case_id STRING
datapoint_id STRING
run_id STRING
parent_node_id STRING
node_id STRING
node_type STRING
label STRING
operation STRING
formula STRING
value DECIMAL(18,2)
previous_value DECIMAL(18,2)
contribution_delta DECIMAL(18,2)
source_table STRING
source_column STRING
filters_json STRING
join_json STRING
snapshot_id STRING
sequence_no INT
```

#### `source_snapshot`

```text
snapshot_id STRING
case_id STRING
source_table STRING
as_of_ts TIMESTAMP
row_count BIGINT
status STRING
snapshot_role STRING
pipeline_run_id STRING
```

#### `source_record`

```text
case_id STRING
snapshot_id STRING
business_key STRING
entity_id STRING
period_id STRING
component STRING
segment_id STRING
amount DECIMAL(18,2)
record_status STRING
changed_from_previous BOOLEAN
duplicate_group_id STRING
included_by_filter BOOLEAN
source_table STRING
source_column STRING
```

#### `snapshot_diff`

```text
case_id STRING
component STRING
business_key STRING
entity_id STRING
segment_id STRING
change_type STRING
old_value DECIMAL(18,2)
new_value DECIMAL(18,2)
impact DECIMAL(18,2)
duplicate_group_id STRING
pipeline_run_id STRING
previous_snapshot_id STRING
current_snapshot_id STRING
```

Allowed `change_type` values for the current generator:

```text
MODIFIED
REMOVED
ADDED
UNCHANGED
DUPLICATED
```

Case #042 canonical `snapshot_diff` need not store `UNCHANGED` rows unless the repository has an explicit use for them. The source snapshots retain unchanged rows.

#### `quality_issue`

```text
case_id STRING
issue_id STRING
rule_name STRING
severity STRING
affected_keys STRING
affected_row_count INT
estimated_impact DECIMAL(18,2)
impact_is_overlapping BOOLEAN
status STRING
evidence_note STRING
```

For DQ_0042_01, `status=OPEN` is a **DQ lifecycle status**, not an epistemic hypothesis status.

#### `pipeline_run_evidence`

Create the shared table now even though pipeline replay is not causal in Case #042:

```text
case_id STRING
pipeline_run_id STRING
run_ts TIMESTAMP
source_snapshot_id STRING
execution_status STRING
replay_of_run_id STRING
rows_written BIGINT
duplicate_rows_written BIGINT
note STRING
```

Case #042 may store ordinary previous/current run records with `duplicate_rows_written=0`; do not invent a replay.

#### `semantic_change_evidence`

```text
case_id STRING
semantic_type STRING
previous_id STRING
current_id STRING
previous_hash STRING
current_hash STRING
affected_population_count INT
estimated_impact DECIMAL(18,2)
details_json STRING
```

Case #042 creates one `FORMULA` row with unchanged ID/hash and zero affected population.

#### `technical_lineage_curated`

```text
case_id STRING
source_table STRING
source_column STRING
target_table STRING
target_column STRING
entity_type STRING
event_time TIMESTAMP
lineage_source STRING
```

### 17.4 Private table

`mad_data_lab_private.case_truth`:

```text
case_id STRING
primary_component STRING
primary_source STRING
primary_cause STRING
secondary_cause STRING
affected_rows INT
expected_impact DECIMAL(18,2)
secondary_expected_impact DECIMAL(18,2)
expected_total_deviation DECIMAL(18,2)
confidence STRING
allowed_final_status_json STRING
expected_path_json STRING
truth_json STRING
```

No curated view may select from this table.

---

## 18. Exact DDL implementation rules

Use V3 Appendix A as the semantic reference and materialize each object in version-controlled SQL.

Rules:

- `USING DELTA` for tables;
- schema creation is idempotent;
- table creation is idempotent;
- view creation is `CREATE OR REPLACE VIEW`;
- the catalog name is applied by the deployment/SQL templating layer;
- do not rely on session current catalog/schema without a test;
- if `SELECT * EXCEPT` syntax varies in the target, enumerate columns explicitly;
- every SQL file has a deterministic execution order prefix;
- DDL runner stops on first error;
- partial application is recorded as failure, never green;
- app runtime does not execute schema DDL at normal request startup.

### 18.1 View `case_summary`

Must expose only safe Case/run metadata:

```text
case_id
public_number
slug
title
datapoint_id
entity_id
period_id
expected_value
observed_value
deviation
currency
scale
difficulty
current_run_id
previous_run_id
current_formula_id
previous_formula_id
current_formula_hash
previous_formula_hash
current_filter_id
previous_filter_id
current_filter_hash
previous_filter_hash
current_population_hash
previous_population_hash
```

No cause/oracle/truth/path fields.

### 18.2 View `component_evidence`

One row per component:

```text
case_id
component
label
previous_value
current_value
contribution_delta
abs_contribution
share_of_abs_deviation
abs_contribution_rank
source_table
source_column
sequence_no
```

For Case #042:

```text
V2 abs_contribution_rank = 1
V2 share_of_abs_deviation = 5.90 / 6.80
```

### 18.3 View `snapshot_evidence`

Use `snapshot_diff` plus group/window totals.

The V2 subset must yield exactly:

```text
MODIFIED count 23 total -5.20
REMOVED   count  2 total -0.80
ADDED     count  5 total +0.10
component total              -5.90
```

### 18.4 View `quality_evidence`

Must expose:

```text
case_id
issue_id
rule_name
severity
affected_keys
affected_row_count
estimated_impact
impact_is_overlapping
status
evidence_note
total_deviation
deviation_share
```

Case #042 deviation share:

```text
abs(-0.30) / abs(-6.80) ~= 0.0441176471
```

Never calculate final anomaly as `component_total + dq_impact`.

### 18.5 View `semantic_evidence`

Case #042 `FORMULA` row:

```text
changed = false
estimated_impact = 0.00
```

### 18.6 View `pipeline_evidence`

Shared forward-compatible view over `pipeline_run_evidence`.

### 18.7 View `population_evidence`

Create the V3 shared population view even if #042 does not use it in the challenge flow. It proves the multi-Case data architecture and prepares #107/#213 without enabling those Cases.

### 18.8 View `lineage_evidence`

Union:

- value/calculation lineage from `calculation_trace`;
- technical lineage rows from `technical_lineage_curated`.

Required safe columns:

```text
case_id
depth
node_type
node_id
parent_node_id
component
source_table
source_column
snapshot_id
target_table
target_column
lineage_source
```

Ensure deterministic ordering in application queries rather than trusting union order.

---

## 19. Trusted SQL application repository

Create fixed query templates under `sql/trusted/` and map them through a closed code registry.


### 19.1 Connection/authentication helper

Use the Databricks App **runtime service principal** through Databricks unified authentication. Do not introduce a PAT for the application.

The runtime App receives its own service-principal credentials, and the SQL warehouse is referenced through the App resource binding (`SQL_WAREHOUSE_ID` or the normalized MDL-1 config name).

Preferred pattern:

1. create `databricks.sdk.core.Config()` so runtime-injected App credentials are used;
2. resolve the configured SQL warehouse’s HTTP path from the warehouse metadata/API or another documented non-secret configuration path;
3. open the Databricks SQL Connector with the documented OAuth credentials provider derived from `Config`;
4. close cursor/connection deterministically;
5. set query timeout/cancellation behavior in the shared adapter;
6. never log client secret, access token, or authorization headers.

Conceptual form:

```python
from databricks import sql
from databricks.sdk import WorkspaceClient
from databricks.sdk.core import Config

cfg = Config()
w = WorkspaceClient(config=cfg)

warehouse = w.warehouses.get(settings.sql_warehouse_id)
http_path = warehouse.odbc_params.path

connection = sql.connect(
    server_hostname=cfg.host,
    http_path=http_path,
    credentials_provider=lambda: cfg.authenticate,
)
```

Adapt exact SDK field names to the pinned SDK version and verify them with an integration test; do not hardcode an HTTP path copied from a developer’s browser.

The connection factory must be injectable so unit tests do not require live Databricks.

### 19.2 Native parameters are mandatory

Pin `databricks-sql-connector` to a tested release **>= 3.0.0** so native parameter execution is available. Do not accept an older transitive version.

Current Databricks SQL Connector 3.0+ supports native parameterized execution. Application SQL must use native parameters, e.g.:

```python
cursor.execute(
    "SELECT ... FROM ... WHERE case_id = ?",
    [case_id],
)
```

Do not format or concatenate `case_id`, `business_key`, limit, or filters into SQL strings.

Identifiers such as catalog/schema/table cannot be bound as ordinary value parameters. They must come from validated configuration/closed query templates, never user input.

### 19.3 Closed query IDs

Use closed IDs such as:

```text
observation
component_decomposition
snapshot_summary
highest_impact_records
dq_materiality
formula_validation
value_lineage
reconciliation
```

The API/model cannot submit an arbitrary SQL string.

### 19.4 Q1 — observation

Application template:

```sql
SELECT
  case_id,
  datapoint_id,
  entity_id,
  period_id,
  expected_value,
  observed_value,
  deviation,
  current_formula_id AS formula_id,
  current_formula_hash AS formula_hash
FROM ${CURATED}.case_summary
WHERE case_id = ?
```

Expected #042:

```text
125.00 / 118.20 / -6.80
```

`${CURATED}` is resolved only from validated environment configuration before execution; it is not user data.

### 19.5 Q2 — component decomposition

```sql
SELECT
  component,
  previous_value,
  current_value,
  contribution_delta,
  abs_contribution,
  share_of_abs_deviation,
  abs_contribution_rank
FROM ${CURATED}.component_evidence
WHERE case_id = ?
ORDER BY abs_contribution DESC, sequence_no, component
```

Expected top row:

```text
V2 / -5.90 / rank 1
```

### 19.6 Q3 — V2 snapshot summary

```sql
SELECT
  change_type,
  COUNT(*) AS record_count,
  SUM(impact) AS total_impact
FROM ${CURATED}.snapshot_evidence
WHERE case_id = ?
  AND component = ?
GROUP BY change_type
ORDER BY change_type
```

Parameters:

```text
CASE_0042
V2
```

### 19.7 Q4 — highest-impact source records

```sql
SELECT
  business_key,
  change_type,
  old_value,
  new_value,
  impact,
  previous_snapshot_id,
  current_snapshot_id
FROM ${CURATED}.snapshot_evidence
WHERE case_id = ?
  AND component = ?
ORDER BY ABS(impact) DESC, business_key
LIMIT ?
```

Server enforces:

```text
1 <= limit <= 100
```

Expected first Case #042 V2 row:

```text
TX-004291 / MODIFIED / 4.20 / 0.00 / -4.20
```

### 19.8 Q5 — DQ materiality

```sql
SELECT
  issue_id,
  rule_name,
  severity,
  affected_row_count,
  estimated_impact,
  impact_is_overlapping,
  deviation_share
FROM ${CURATED}.quality_evidence
WHERE case_id = ?
ORDER BY issue_id
```

### 19.9 Q6 — formula validation

```sql
SELECT
  case_id,
  previous_formula_id,
  current_formula_id,
  previous_formula_hash,
  current_formula_hash,
  CASE
    WHEN previous_formula_id = current_formula_id
     AND previous_formula_hash = current_formula_hash
    THEN false
    ELSE true
  END AS formula_changed
FROM ${CURATED}.case_summary
WHERE case_id = ?
```

### 19.10 Q7 — value/technical lineage

```sql
SELECT
  depth,
  node_type,
  node_id,
  parent_node_id,
  component,
  source_table,
  source_column,
  snapshot_id,
  target_table,
  target_column,
  lineage_source
FROM ${CURATED}.lineage_evidence
WHERE case_id = ?
ORDER BY depth, node_id, source_table, source_column
```

### 19.11 Q8 — total reconciliation

```sql
WITH component_total AS (
  SELECT SUM(contribution_delta) AS component_delta
  FROM ${CURATED}.component_evidence
  WHERE case_id = ?
),
case_total AS (
  SELECT deviation
  FROM ${CURATED}.case_summary
  WHERE case_id = ?
)
SELECT
  c.component_delta,
  t.deviation,
  c.component_delta - t.deviation AS unreconciled_amount
FROM component_total c
CROSS JOIN case_total t
```

Pass `CASE_0042` for both parameters.

Expected:

```text
component_delta = -6.80
deviation = -6.80
unreconciled_amount = 0.00
```

---

## 20. Typed SQL result contracts

Create Pydantic/domain models for every trusted query result.

Examples:

```python
class ObservationResult(BaseModel):
    case_id: CaseId
    datapoint_id: str
    entity_id: str
    period_id: str
    expected_value: Decimal
    observed_value: Decimal
    deviation: Decimal
    formula_id: str
    formula_hash: str

class ComponentRow(BaseModel):
    component: str
    previous_value: Decimal
    current_value: Decimal
    contribution_delta: Decimal
    abs_contribution: Decimal
    share_of_abs_deviation: Decimal
    abs_contribution_rank: int

class SnapshotGroup(BaseModel):
    change_type: SnapshotChangeType
    record_count: int
    total_impact: Decimal

class EvidenceRecord(BaseModel):
    business_key: str
    change_type: SnapshotChangeType
    old_value: Decimal | None
    new_value: Decimal | None
    impact: Decimal
    previous_snapshot_id: str | None
    current_snapshot_id: str

class DqMaterialityResult(BaseModel):
    issue_id: str
    rule_name: str
    severity: str
    affected_row_count: int
    estimated_impact: Decimal | None
    impact_is_overlapping: bool
    deviation_share: Decimal | None

class FormulaValidationResult(BaseModel):
    case_id: CaseId
    previous_formula_id: str
    current_formula_id: str
    previous_formula_hash: str
    current_formula_hash: str
    formula_changed: bool
```

Unknown/missing required columns are errors, not silently ignored success.

DECIMAL conversion must not pass through float.

Precision boundary:

- SQL Connector result -> Python `Decimal`;
- Pydantic/domain validation -> `Decimal`;
- canonical fixtures/release JSON -> fixed decimal strings (`"125.00"`, `"-6.80"`) so hashes cannot depend on JSON floating-point formatting;
- later browser-facing render/API DTOs may use numeric JSON only when their serializer is separately tested to preserve the Case's cent-level values and generated frontend schemas agree;
- no MDL-2 test converts monetary truth through binary `float` merely for convenience.

Add `MDL2-SQL-013` to prove representative SQL DECIMAL values survive connector -> Pydantic -> release-artifact serialization exactly.

---

## 21. Repository boundary

Use separate repositories/interfaces:

```text
CaseEvidenceRepository
TrustedSqlRepository
PrivateTruthRepository
```

Rules:

- ordinary evidence service depends on `CaseEvidenceRepository`;
- only private validation/release code can depend on `PrivateTruthRepository`;
- no public route directly imports private repository;
- no frontend code imports backend fixture files;
- query results are validated before entering domain/render models;
- all repository methods require validated `CaseId`;
- unknown Case IDs fail before query construction;
- max rows are enforced server-side;
- deterministic sort order is part of the contract.

---

## 22. Evidence API boundary — do not leak future evidence

MDL-2 may define request/response models for:

```text
GET /api/sessions/{session_id}/evidence
```

but **must not expose unrestricted production evidence before MDL-4 establishes server-authoritative evidence entitlements**.

Allowed MDL-2 implementations:

1. route not registered in production yet; repository/service tested directly; or
2. route registered but requires an `available_evidence_ids/tags` entitlement set from authoritative session state and returns no unearned evidence.

Forbidden:

- `GET /api/evidence?case_id=CASE_0042` returning all evidence;
- client-supplied `experiment_id` treated as permission;
- arbitrary `table`, `view`, or `sql` request parameters;
- query flag such as `include_private=true`;
- production-only “debug evidence” endpoint.

Deployed MDL-2 evidence smoke uses trusted backend/script authentication to query the data layer, not a browser backdoor.

---


## 23. Seed, migration, and rollback contract

### 23.1 No manual SQL drift

All DDL, view creation, data write, grants, validation, and rollback operations must be repository-controlled scripts/workflows.

A human may inspect Catalog Explorer/SQL results but must not make undocumented manual mutations and then mark MDL-2 green.

### 23.2 `seed_databricks.py`

Required modes:

```bash
python scripts/seed_databricks.py --target staging --case CASE_0042 --plan
python scripts/seed_databricks.py --target staging --case CASE_0042 --apply
python scripts/seed_databricks.py --target staging --case CASE_0042 --verify
```

Optional explicit recovery:

```bash
python scripts/restore_case_data.py --target staging --manifest <verified-backup-manifest>
```

### 23.3 Apply sequence

Before any mutation:

1. validate target name against closed environment config;
2. reject production unless explicitly allowed by the workflow/environment;
3. verify clean accepted Git identity;
4. run local canonical generation;
5. run all generator/Case validators;
6. compute canonical hash;
7. query current deployed schema/object versions;
8. snapshot existing Case #042 rows/row counts/hashes into a rollback manifest;
9. validate required DDL privileges;
10. apply schemas/tables/views in deterministic order;
11. replace only Case #042 rows needed by the seed;
12. insert private truth using deployment/test identity;
13. apply least-privilege grants;
14. run server-side verification queries;
15. write deployment/seed evidence manifest.

### 23.4 No broad destructive reset

Default seed behavior must not:

```text
DROP CATALOG
DROP all schemas
TRUNCATE unrelated Cases
DELETE all public data
replace unrelated Case rows
grant SELECT on entire catalog to app runtime
```

A full synthetic-environment rebuild may exist behind an explicit destructive flag for disposable staging only, requiring human/workflow confirmation and producing evidence. It is not the default.

### 23.5 Case-scoped replacement

For Case #042, replacement must be idempotent:

- running apply twice yields the same final rows;
- row counts do not double;
- old Case #042 rows from the previous generator version do not remain orphaned;
- unrelated Case rows are unchanged.

Where multi-table atomicity is unavailable, the workflow treats the entire seed as failed until post-write verification succeeds. On failure, restore the pre-seed snapshot/manifest or keep the prior known-good app/data target active.

### 23.6 Rollback manifest

Record sanitized metadata:

```json
{
  "target": "staging",
  "catalog": "...",
  "case_id": "CASE_0042",
  "before_generator_version": 1,
  "before_case_template_version": 1,
  "before_public_row_hashes": {},
  "before_private_row_hash": "...",
  "before_view_definition_hashes": {},
  "captured_at_utc": "...",
  "source_implementation_sha": "..."
}
```

Never write credentials or private truth payload values to the public iteration report.

Rollback is recovery, not a pass: the new MDL-2 implementation itself must eventually seed and verify successfully.

---

## 24. Permission and truth-isolation contract

### 24.1 App runtime service principal — MDL-2

Minimum intended privileges:

```text
CAN USE on SQL warehouse
USE CATALOG on MDL_CATALOG
USE SCHEMA on mad_data_lab_public
USE SCHEMA on mad_data_lab_curated
SELECT on required public/curated objects
```

No:

```text
USE SCHEMA / SELECT on mad_data_lab_private
MODIFY on evidence tables
CREATE TABLE / CREATE VIEW
ownership of Case schemas
```

If `USE CATALOG` on the workspace catalog is inherited by platform policy, record that fact; do not add broader permissions unnecessarily.

### 24.2 Deployment/test identity

May receive the DDL/MODIFY/private read privileges needed to create/seed/verify staging. This identity is not the runtime data path and must not be exposed to application users.

### 24.3 Effective privilege verification

Provision privileges through repository-controlled deployment/admin automation or a recorded human-admin step; do not rely on an undocumented Catalog Explorer click.

The exact principal name/application service-principal ID is environment-specific and must not be hardcoded in business logic.

For the MDL-2 app runtime principal, verify effective access equivalent to:

```text
SQL warehouse: CAN USE
configured catalog: USE CATALOG
mad_data_lab_public schema: USE SCHEMA + SELECT on required objects
mad_data_lab_curated schema: USE SCHEMA + SELECT on required views
mad_data_lab_private schema/table: no SELECT
```

The test/deployment identity may have temporary DDL/MODIFY/SELECT rights needed to seed/validate staging, but those rights do not prove the App runtime is least-privilege.

Record effective privilege evidence as sanitized principal/object/privilege tuples. Never archive OAuth tokens or client secrets.

If permissions are changed manually because Free Edition administration cannot be automated safely, record the exact human-admin action and then run the same live positive/negative permission tests. Manual provisioning is not a substitute for automated verification.

### 24.4 Genie

MDL-3 owns actual Agent curation. MDL-2 nevertheless guarantees:

- curated views contain no truth columns;
- no SQL/view definition references private truth;
- any serialized/staged Genie config left in the repo contains no `case_truth` reference;
- eventual Genie access matrix is curated-only.

### 24.5 Static truth leak scan

Scan at least:

```text
frontend source
frontend production bundle
frontend public/static assets
Genie configuration/instructions/example SQL
curated view SQL
public API schemas/examples
public fixture package
production documentation generated for the browser
```

Sensitive-to-product fields include:

```text
expected_path_json
truth_json
allowed_final_status_json
private Case truth payload
```

Do not globally ban generic strings such as `SOURCE_RECORD_CHANGE` from backend source because the domain may legitimately define a cause enum. The leak test targets **forbidden locations**, not all repository text.

### 24.6 Production-package private-fixture denylist

The frontend/static application package and any public downloadable asset must exclude private/oracle material by **path and content**, not merely by naming convention.

At minimum deny production packaging of:

```text
data/generation/private_specs/**
data/fixtures/private/**
data/seeds/private/**
**/case_truth*.json
**/*truth_oracle*
**/*expected_path*
```

Also scan built frontend/static bytes for forbidden private field names and the full canonical private truth serialization.

The backend source package may contain private repository code and migration definitions when required to operate the service, but it must not contain a browser-served static mapping to private fixture bytes.

Add:

- `MDL2-PRIV-008` — frontend/static manifest has no private/oracle path;
- `MDL2-PRIV-009` — built frontend/static bytes contain no private Case #042 oracle serialization;
- `MDL2-PRIV-010` — private fixture path cannot be fetched through static SPA fallback;
- `MDL2-PRIV-011` — normal evidence repository imports do not depend on the private truth fixture/module.

### 24.7 Negative live privilege test

Using the **App runtime service principal identity**, issue:

```text
SELECT * FROM <catalog>.mad_data_lab_private.case_truth WHERE case_id = 'CASE_0042'
```

Expected: permission denied.

Using the App runtime identity, issue read queries against required curated views.

Expected: success.

Capture sanitized pass/fail evidence. Do not log returned private truth if a misconfiguration accidentally permits the first query; treat it as a critical failure and immediately correct grants.

---

## 25. Current Databricks platform assumptions to verify at iteration start

Record verification date and links in:

```text
docs/traceability/mdl2-platform-verification.md
```

As of 2026-08-24, current Databricks documentation supports these assumptions:

Reference URLs to store in the verification record:

```text
https://docs.databricks.com/aws/en/dev-tools/databricks-apps/resources
https://docs.databricks.com/aws/en/dev-tools/databricks-apps/sql-warehouse
https://docs.databricks.com/aws/en/dev-tools/databricks-apps/auth
https://docs.databricks.com/aws/en/dev-tools/databricks-apps/genie
https://docs.databricks.com/aws/en/data-governance/unity-catalog/access-control/privileges-reference
https://docs.databricks.com/aws/en/dev-tools/python-sql-connector
```

Verified assumptions:

1. Databricks Apps have a dedicated service principal and should use least privilege.
2. an App that queries a SQL warehouse normally needs `CAN USE`;
3. Unity Catalog reads require `USE CATALOG`, `USE SCHEMA`, and `SELECT`;
4. Genie Agent integration similarly requires appropriate underlying UC permissions;
5. Databricks SQL Connector for Python 3.0+ supports native parameterized execution;
6. Apps resource bindings should be used instead of hardcoded warehouse/resource IDs.

If official docs materially change before implementation, update the platform-verification record and create a source addendum/ADR only where needed. Do not silently rewrite V3.

---

## 26. Complete Case #042 machine validators

Generation must fail if any validator fails.

### 26.1 Metric

```text
observed - expected = -6.80
118.20 - 125.00 = -6.80
```

### 26.2 Formula

```text
previous: 100.10 + 30.00 - 5.10 + 0.00 = 125.00
current:   98.90 + 24.10 - 4.80 + 0.00 = 118.20
```

### 26.3 Component contribution

```text
-1.20 + -5.90 + +0.30 + 0.00 = -6.80
```

### 26.4 V2 source changes

```text
-5.20 + -0.80 + +0.10 = -5.90
```

### 26.5 Count reconciliation

```text
23 modified + 2 removed + 5 added = 30 changed logical records
```

### 26.6 Representative record

```text
TX-004291 exists exactly once in each applicable logical snapshot/diff context
previous = 4.20
current = 0.00
impact = -4.20
change_type = MODIFIED
```

### 26.7 DQ

```text
issue_id = DQ_0042_01
rule = DUPLICATE_BUSINESS_KEY
severity = MEDIUM
affected_row_count = 5
affected keys = TX-004292..TX-004296
estimated_impact = -0.30
impact_is_overlapping = true
status = OPEN
```

DQ affected keys must be a subset of Case #042 V2 changed evidence.

### 26.8 Formula unchanged

```text
previous_formula_id == current_formula_id
previous_formula_hash == current_formula_hash
formula_changed == false
```

### 26.9 Truth

Private truth must match actual mutation, not merely expected constants.

### 26.10 Lineage

- one root;
- acyclic;
- V2 reaches `finance_reporting_source.amount`;
- required snapshots resolvable;
- source records resolvable;
- no private node/edge;
- technical fallback honestly labeled.

### 26.11 Curated privacy

Projection of curated/public outputs contains none of the private oracle fields.

### 26.12 No unintentional duplicates

The source business-key uniqueness expectation must be explicit by snapshot/component. The DQ diagnostic does not create hidden extra rows that alter the metric.

---

## 27. Generator and property-based test ownership

MDL-2 is the primary closure owner for the V3 deterministic generator/data property tier.

### DG suite

Required:

- `DG-001` same seed + versions => same canonical output;
- `DG-002` property-test seeds vary procedural elements when the generic generator/fuzz template is exercised;
- `DG-003` generator version stored;
- `DG-004` stable business-key ordering;
- `DG-005` no wall-clock dependency in canonical output;
- `DG-006` canonical serialization stable;
- `DG-007` Case #042 golden hash stable;
- `DG-008` generated IDs unique where required;
- `DG-009` referenced snapshots/runs exist;
- `DG-010` Case #042 component count exactly four.

`DG-002` does **not** permit changing the release seed of Case #042.

### DP suite

Implement the full V3 property/data set applicable to the generator:

- `DP-001` metric formula reconciliation;
- `DP-002` deviation reconciliation;
- `DP-003` primary snapshot reconciliation;
- `DP-004` mutation truth alignment;
- `DP-005` no unintentional duplicate keys;
- `DP-006` added rows have null old value;
- `DP-007` removed rows have null new value;
- `DP-008` modified rows have both old/new values;
- `DP-009` impact definition consistent;
- `DP-010` DQ materiality bounds;
- `DP-011` primary cause signal strength obeys difficulty/template contract where property templates use that rule;
- `DP-012` no orphan calculation nodes;
- `DP-013` single metric root;
- `DP-014` lineage acyclic;
- `DP-015` every component reaches a source;
- `DP-016` previous/current snapshots exist;
- `DP-017` decimal precision/no float drift;
- `DP-018` truth absent from curated projection;
- `DP-019` release/nightly suite executes at least **10,000 generated cases/seeds across both the Level 1 clean and Level 2 noisy property templates**;
- `DP-020` PR suite executes at least **500 generated cases/seeds or a documented time-bounded equivalent that still proves meaningful generator coverage**.

For this week’s narrow challenge scope, property seeds may use test-only template clones/operators; they must not alter the canonical Case #042 golden artifact.

If Hypothesis shrinks a failure, record/reproduce the minimized example deterministically.

---

## 28. Complete Case #042 golden suite

MDL-2 must make all of these green:

```text
G42-001 expected = 125.00
G42-002 observed = 118.20
G42-003 deviation = -6.80
G42-004 V1 previous/current = 100.10/98.90
G42-005 V2 previous/current = 30.00/24.10
G42-006 V3 previous/current = 5.10/4.80
G42-007 V4 previous/current = 0.00/0.00
G42-008 component deltas = -1.20,-5.90,+0.30,0.00
G42-009 component total = -6.80
G42-010 modified count = 23
G42-011 modified impact = -5.20
G42-012 removed count = 2
G42-013 removed impact = -0.80
G42-014 added count = 5
G42-015 added impact = +0.10
G42-016 snapshot total = -5.90
G42-017 TX-004291 exists
G42-018 TX-004291 impact = -4.20
G42-019 DQ affected rows = 5
G42-020 DQ estimated impact = -0.30
G42-021 DQ overlap = true
G42-022 formula IDs equal
G42-023 formula hashes equal
G42-024 private truth primary component = V2
G42-025 private truth primary cause = SOURCE_RECORD_CHANGE
G42-026 curated outputs exclude truth
G42-027 final numeric reconciliation residual = 0.00
```

The following canonical tests remain deliberately **deferred, not skipped**, because their behavior belongs to Genie/gameplay iterations:

```text
G42-028 — expected first Genie experiment = component decomposition — owner MDL-3
G42-029 — expected second Genie experiment = snapshot diff — owner MDL-3
G42-030 — final formula hypothesis expected RULED_OUT — owner MDL-3/MDL-4 according to the global primary-ownership ledger
```

MDL-2 records their traceability status but must not fake Genie/gameplay behavior to make them green. The global eight-iteration ledger remains the authority for the single primary owner when MDL-3/MDL-4 both exercise a later test.

---

## 29. Real Databricks SQL integration suite

Run against staging using the appropriate identity.

Required:

- `SQ-001` Case summary one row for CASE_0042;
- `SQ-002` component view exactly four component rows;
- `SQ-003` V2 top absolute contributor;
- `SQ-004` V2 snapshot groups/counts/totals correct;
- `SQ-005` TX-004291 exists;
- `SQ-006` DQ issue exists;
- `SQ-007` formula validation false for changed;
- `SQ-008` lineage contains required node classes/path;
- `SQ-009` reconciliation residual zero;
- `SQ-010` unknown Case produces empty repository result then stable domain not-found behavior;
- `SQ-011` row limit capped/enforced;
- `SQ-012` deterministic sort;
- `SQ-013` null handling serializes correctly;
- `SQ-014` DECIMAL values preserve precision;
- `SQ-015` curated views expose no private columns;
- `SQ-016` app runtime SP can query required curated views;
- `SQ-017` app runtime SP cannot query private truth; later Genie-specific denial is rerun/extended in MDL-3;
- `SQ-018` trusted SQL registry can execute only approved query templates;
- `SQ-019` query duration recorded for warm runs;
- `SQ-020` pending/unavailable warehouse is handled as an adapter/platform error rather than malformed evidence.

No integration test may substitute a local SQLite/DuckDB success for the required live Databricks SQL run.

---

## 30. MDL-2 custom test set

Add iteration-specific tests beyond canonical V3 IDs.

### Contract/data

```text
MDL2-CONTRACT-001 public template contains no hidden_truth_ref/primary_cause
MDL2-CONTRACT-002 completion contract does not encode final-prediction UI sequencing
MDL2-CONTRACT-003 Case #042 insufficient-evidence verdict flag is false
MDL2-CONTRACT-004 private generation spec cannot be imported by frontend build graph
MDL2-CONTRACT-005 required SQL file/query IDs exist exactly once
MDL2-CONTRACT-006 query registry maps to typed result model
MDL2-CONTRACT-007 all table/view names resolve through configured catalog, not user input
MDL2-CONTRACT-008 A21 predecessor hash unchanged
```

### Exact fixture

Additional exact fixture checks:

- `MDL2-FIX-011` — all Case #042 source records use `record_status=ACTIVE`, `included_by_filter=true`, safe source table/column metadata and the locked change-flag semantics;
- `MDL2-FIX-012` — no Case #042 release source row has a physical `duplicate_group_id`; DQ signal remains diagnostic metadata;
- `MDL2-FIX-013` — pipeline-run IDs/timestamps/42-to-45 row counts are exact and replay/duplicate counts are zero;
- `MDL2-FIX-014` — `affected_keys` canonical JSON is exactly the five DQ keys in sorted order;
- `MDL2-FIX-015` — previous/current population hashes reproduce using the single canonical algorithm and differ from each other;
- `MDL2-FIX-016` — previous/current filter ID/hash equal the locked `CAPITAL_AVAILABLE_FILTER_V1` contract;

```text
MDL2-FIX-001 modified key ranges/counts exact
MDL2-FIX-002 modified impacts exact by key group
MDL2-FIX-003 removed keys/impacts exact
MDL2-FIX-004 added keys/impacts exact
MDL2-FIX-005 unchanged V2 residue makes previous/current totals exact
MDL2-FIX-006 DQ affected keys exactly TX-004292..TX-004296
MDL2-FIX-007 DQ affected-key impacts sum -0.30
MDL2-FIX-008 snapshot row_count previous/current = 42/45
MDL2-FIX-009 V3 raw source delta -0.30 maps to metric contribution +0.30
MDL2-FIX-010 formula normalized hash exact
```

### SQL safety

```text
MDL2-SQL-001 app query execution uses native parameter API
MDL2-SQL-002 injected business_key payload never changes SQL structure
MDL2-SQL-003 invalid case_id rejected before query
MDL2-SQL-004 invalid limit rejected/clamped per API contract
MDL2-SQL-005 arbitrary table/view identifier input is impossible
MDL2-SQL-006 query result missing required column fails schema validation
MDL2-SQL-007 unexpected extra columns follow explicit strict/ignore policy consistently
MDL2-SQL-008 no private repository reachable from ordinary evidence service dependency graph
```

### Seed/migration

```text
MDL2-SEED-001 plan mode makes no workspace mutation
MDL2-SEED-002 apply twice is idempotent
MDL2-SEED-003 unrelated Case rows unchanged
MDL2-SEED-004 partial failure is non-zero and not marked verified
MDL2-SEED-005 verify compares canonical and deployed hashes/counts
MDL2-SEED-006 destructive reset requires explicit protected flag
MDL2-SEED-007 rollback requires exact captured manifest
MDL2-SEED-008 rollback restores prior verified Case state
MDL2-SEED-009 target=unknown fails closed
MDL2-SEED-010 production target cannot be mutated by default staging command
```

### Privacy

```text
MDL2-PRIV-001 curated SQL definitions contain no private schema reference
MDL2-PRIV-002 frontend dist contains no private fixture/oracle payload
MDL2-PRIV-003 app runtime private SELECT is denied live
MDL2-PRIV-004 app runtime curated SELECT succeeds live
MDL2-PRIV-005 no public API schema contains truth fields
MDL2-PRIV-006 no Genie config/example SQL references case_truth
MDL2-PRIV-007 accidental private query result is redacted from test logs
```

### Deployment/provenance

```text
MDL2-DEP-001 data seed evidence references implementation_sha
MDL2-DEP-002 deployed Case hash equals accepted canonical Case hash
MDL2-DEP-003 deployed view definition hashes match repository SQL
MDL2-DEP-004 app deployment/runtime digest matches accepted implementation content
MDL2-DEP-005 rollback source resolves to known-good prior data/app identity
```

---

## 31. Data-contract digest and stale-evidence invalidation

MDL-2 has expensive live SQL validation and later art-only/report-only commits. A live SQL run is valid only for the exact **data contract** it tested; it must never be reused merely because the branch name is unchanged.

Create `scripts/compute_mdl2_data_digest.py` or an equivalent deterministic helper.

The MDL-2 data-contract digest includes, fail-closed, at least:

```text
cases/templates/**
cases/completion_contracts/**
data/ddl/**
data/views/**
data/generation/**
data/validation/**
data/seeds/**
sql/trusted/**
backend/data/**
scripts/generate_cases.py
scripts/validate_cases.py
scripts/seed_databricks.py
scripts/verify_databricks_case.py
scripts/snapshot_case_data.py
scripts/restore_case_data.py
pyproject.toml
uv.lock or the selected frozen Python lock
```

If the implementation adds another file that can alter generated Case bytes, SQL text, data validation, seeding behavior, SQL connector behavior, or effective Case #042 query results, the classifier must treat it as data-contract-affecting until explicitly reviewed.

The digest is:

```text
SHA-256(
  for every included path sorted lexicographically:
    UTF8(path) + NUL + raw_file_bytes + NUL
)
```

Paths are repository-relative POSIX paths. The implementation must normalize path separators to `/`, reject duplicate normalized paths, and hash the raw committed bytes exactly as stored by Git after checkout. Generated reports, local caches, review contact sheets, and deployment observations are excluded unless they can alter the data contract.

Required artifact fields:

```text
v3_source_sha256
implementation_sha
data_contract_digest
canonical_case_hash
ddl_source_digest
curated_view_source_digest
trusted_query_source_digest
warehouse_resource_key
target
workflow_run_id
workflow_run_url
workflow_conclusion
artifact_sha256
status
```

Rules:

- a staging SQL integration result is reusable on a later branch head **only** when the final-head CI proves `data_contract_digest` and `canonical_case_hash` are unchanged;
- changing artwork alone does not force expensive SQL reruns, but final-head CI must still verify the referenced SQL artifact/digest;
- changing any data-contract path invalidates the SQL integration artifact and requires reseed/live SQL rerun;
- changing approved art bytes invalidates art approval regardless of data digest;
- changing runtime/app code after deployment invalidates deployed smoke under the inherited MDL-1 runtime-digest rules;
- no artifact may claim `PASS` if its recorded source digest cannot be recomputed from the accepted head.

Add:

- `MDL2-EVIDENCE-001` — SQL artifact rejected when `data_contract_digest` differs;
- `MDL2-EVIDENCE-002` — canonical fixture artifact rejected when `canonical_case_hash` differs;
- `MDL2-EVIDENCE-003` — art-only diff may reuse live SQL evidence only when data digest is exactly unchanged;
- `MDL2-EVIDENCE-004` — data/SQL/seed diff invalidates live SQL evidence;
- `MDL2-EVIDENCE-005` — workflow artifact with missing/unknown commit or digest is not closure evidence;
- `MDL2-EVIDENCE-006` — final-head release contract resolves every reused artifact to an immutable GitHub run/artifact reference.

## 32. CI contract

MDL-1’s shared CI remains mandatory. MDL-2 adds stable semantic checks.

Required MDL-2 checks on the accepted PR head:

```text
mdl2/repository-contract
mdl2/generator-property
mdl2/golden-case
mdl2/sql-static-privacy
mdl2/art-preflight
mdl2/human-approval-gate
mdl2/sql-integration-staging
mdl2/deployed-evidence-smoke
mdl2/release-contract
```

The MDL-1 required checks remain required and green. MDL-2 checks are **additive**, not replacements. Update the GitHub ruleset/branch-protection policy so a merge cannot bypass either the inherited baseline or the MDL-2 data gates. If admin permission is missing, this is a blocker rather than a documentation-only exception.

Responsibilities:

- `repository-contract` — predecessor/source/branch/template/schema/query/traceability structural contract;
- `generator-property` — DG + DP PR sample, zero-test detection, deterministic reproduction evidence;
- `golden-case` — G42-001..027 + custom fixture invariants;
- `sql-static-privacy` — DDL/view parsing/privacy/query-registry/native-parameter/static bundle scans;
- `art-preflight` — candidate/manifest/production derivative/hashes/dimensions/packaging checks;
- `human-approval-gate` — verifies external human selection/approval evidence against exact bytes;
- `sql-integration-staging` — OIDC/protected staging job running SQ suite under the correct identities;
- `deployed-evidence-smoke` — verifies seeded data and app-facing Case briefing/trusted repository path after deployment;
- `release-contract` — strict iteration report/evidence/runtime-digest/deferral/closure validator.

If GitHub ruleset admin permission is unavailable, record `BLOCKED_GITHUB_ADMIN_CONFIGURATION`; a workflow file alone does not prove checks are required before merge.

### 32.1 No rerun-until-green laundering

- deterministic failure must be fixed, not hidden by rerun;
- no new skip/xfail without explicit reason/owner/traceability;
- zero collected tests is failure;
- SQL integration may retry only documented transient platform conditions, not wrong results;
- a quota outage is a blocker, not a pass.

### 32.2 Live SQL quota awareness

The full real SQL suite need not run on every local edit, but **must run green before MDL-2 closure**. Use protected environment/OIDC and avoid repeated unnecessary calls.

---

## 33. One-command MDL-2 gate

Extend the shared iteration runner:

```bash
python scripts/run_iteration_gate.py --iteration MDL-2 --profile local
python scripts/run_iteration_gate.py --iteration MDL-2 --profile pr
python scripts/run_iteration_gate.py --iteration MDL-2 --profile sql-staging
python scripts/run_iteration_gate.py --iteration MDL-2 --profile deploy-preflight
python scripts/run_iteration_gate.py --iteration MDL-2 --profile closure
```

Required properties:

- each profile declares non-empty checks;
- one underlying failure => non-zero exit;
- secret values redacted;
- evidence JSON + Markdown generated under `release-report/MDL-2/`;
- `local` includes inherited MDL-1 static/build + MDL-2 deterministic/golden/static privacy/art preflight;
- `pr` includes 500-sample property tier;
- `sql-staging` runs real SQL/privilege verification;
- `deploy-preflight` validates exact SHA,target,catalog,feature flags, canonical hash;
- `closure` requires human art approval, SQL integration, deployed smoke, exact-head CI, and no unresolved blockers.

---

## 34. MDL-2 repository contract self-audit

Create `scripts/validate_mdl2_contract.py`.

It must fail strict closure mode if:

- V3 source/predecessor fingerprint missing/stale;
- `case_0042.yaml` contains private truth fields;
- private Case spec missing;
- canonical fixture/hash missing;
- any required DDL/view/query file missing;
- any trusted query bypasses registry/parameters;
- public/curated view SQL references private schema;
- required DG/DP/G42/SQ ownership rows absent;
- A21 predecessor hash changed;
- A08–A12 art prompt/candidate/manifest/approval records incomplete;
- required CI names disagree with workflow/policy;
- SQL integration evidence is stale for an older SHA/data hash;
- report says `COMPLETE` while a blocker/gate is pending;
- `TODO`/`TBD`/fake PASS leaks into executable configs;
- runtime digest changed after accepted deployment without gate invalidation;
- private fixture appears in frontend production package.

Support `--allow-in-progress` during implementation. Strict closure is mandatory for merge.

---

## 35. Artwork production — MDL-2-owned analytical instrument pack

### 35.1 Ownership clarification

MDL-1 already owns/approves:

```text
A01 app icon
A02 master Dr. Genie
A21 Case #042 key art
A28 Case Board hub
```

MDL-2 must verify those hashes but **must not regenerate them** unless a human explicitly reopens the predecessor art decision.

MDL-2 owns early production of the five analytical illustration assets most directly tied to its evidence surfaces:

```text
A08 Deviation Decomposer
A09 Snapshot Reactor
A10 Data Microscope
A11 Lineage Telescope
A12 DQ Contamination Scanner
```

MDL-5 remains responsible for final React Instrument layout, visual-regression integration, and any integration-driven derivative reapproval. Starting these assets now parallelizes the challenge schedule and gives the data contracts a stable visual target.

### 35.2 Global prompt prefix

Prepend this exact direction to every A08–A12 candidate:

> Premium retro-futurist data science laboratory, sophisticated enterprise analytics meets playful scientific experimentation, dark navy research environment, luminous cyan data traces, restrained coral energy accents, subtle violet evidence glow, precision instruments, clean geometric forms, cinematic but not photorealistic, polished 3D illustration with lightly stylized proportions, trustworthy and intelligent, high detail in machinery but generous negative space for UI overlays, no readable text, no numbers, no logos, no watermarks, no brand marks, no horror, no dangerous chemical imagery.

Hard negatives for all MDL-2 assets:

```text
no fake UI buttons
no readable labels
no currency symbols
no charts with baked-in numeric axes
no fantasy genie/lamp
no people
no Databricks logo
no watermark/signature
no dangerous chemical scene
no microscopic biological specimen
no answer-revealing text
```

### 35.3 Candidate count

Generate **three independent full-image candidates per asset**:

```text
A08 C01-C03
A09 C01-C03
A10 C01-C03
A11 C01-C03
A12 C01-C03
TOTAL = 15 independent candidates
```

Stable candidate-slot test IDs:

```text
MDL2-ART-001 = A08-C01
MDL2-ART-002 = A08-C02
MDL2-ART-003 = A08-C03
MDL2-ART-004 = A09-C01
MDL2-ART-005 = A09-C02
MDL2-ART-006 = A09-C03
MDL2-ART-007 = A10-C01
MDL2-ART-008 = A10-C02
MDL2-ART-009 = A10-C03
MDL2-ART-010 = A11-C01
MDL2-ART-011 = A11-C02
MDL2-ART-012 = A11-C03
MDL2-ART-013 = A12-C01
MDL2-ART-014 = A12-C02
MDL2-ART-015 = A12-C03
```

Each ID verifies that its slot has a generated candidate revision with complete prompt/provenance/hash metadata and a technically valid review image. Human quality approval is separate.

A single collage cropped into three files is not 3 candidates.

### 35.4 A08 — Deviation Decomposer

Target:

```text
1600x900 minimum, 16:9
production WebP
normally <1.5 MB
```

Base prompt:

> A fictional scientific analytics machine that visually separates one glowing aggregate data beam into four component channels of different lengths, with the second channel clearly dominant. Elegant precision machinery, transparent glass channels, cyan data particles, subtle coral negative-flow indication and violet analytical glow. Leave a large clean rectangular region for a real SVG waterfall chart overlay. Premium enterprise-lab aesthetic. No readable text, no numbers, no logo, no watermark.

Candidate suffixes:

```text
C01 — instrument frame concentrated on the right and lower edges; broad quiet center-left chart canvas.
C02 — symmetrical four-channel machine with a compact mechanical header and very clean central chart window.
C03 — side-elevation decomposer with channels framing, not occupying, the chart area; maximize 16:9 overlay safety.
```

### 35.5 A09 — Snapshot Reactor

Target:

```text
1600x900 minimum, 16:9
```

Base prompt:

> A futuristic snapshot comparison reactor: two transparent data cylinders representing previous and current data states feed into a central comparison chamber. Abstract record tiles move between the cylinders, with some tiles modified, a few removed, and a few newly appearing. Sophisticated clean scientific machine, dark navy, cyan and violet data glow, restrained coral discrepancy markers. Leave a large empty central panel for real HTML summary content. No readable text, no numbers, no logos, no watermark.

Suffixes:

```text
C01 — previous/current cylinders on far left/right, broad quiet central evidence canvas.
C02 — compact reactor on the right third with visual record flow; large quiet left/center region for data.
C03 — slightly elevated chamber perspective; record tiles remain secondary and never resemble clickable UI.
```

### 35.6 A10 — Data Microscope

Target:

```text
1600x900 minimum, 16:9
```

Base prompt:

> A high-tech analytical microscope designed to inspect data records rather than biological samples. A single abstract rectangular record tile sits on a glass stage while a holographic lens reveals nested fields and lineage paths around it. Dark navy lab bench, cyan scanning beam, tiny violet evidence markers, professional polished 3D illustration. Keep the right half visually quiet for a real record-detail panel. No biological specimens, no readable text, no numbers, no logos, no watermark.

Suffixes:

```text
C01 — microscope on left third, right 55% extremely quiet for HTML record details.
C02 — lower-left instrument with a floating abstract record tile; broad upper-right evidence space.
C03 — compact microscope frame surrounding only the left edge; clean enterprise panel-compatible background elsewhere.
```

### 35.7 A11 — Lineage Telescope

Target:

```text
1600x900 minimum, 16:9
```

Base prompt:

> A futuristic analytical telescope that looks inward through layers of data lineage. The viewing path moves from one glowing metric orb through calculation nodes, source-table shapes, snapshot layers, and individual record tiles, forming a clear branching but orderly depth perspective. Enterprise data architecture expressed as scientific instrumentation, dark navy, cyan lines, violet evidence highlights, restrained coral node accent. Leave open space for a real interactive SVG lineage graph overlay. No readable text, no numbers, no logos, no watermark.

Suffixes:

```text
C01 — telescope mechanism around outer perimeter; central 65% is a quiet deterministic graph canvas.
C02 — telescope on right edge pointing into a subtle left-to-right depth path; graph overlay remains primary.
C03 — architectural tunnel framing with very faint abstract lineage depth only; avoid baked-in graph nodes that could conflict with SVG.
```

### 35.8 A12 — DQ Contamination Scanner

Target:

```text
1400x800 minimum
```

Base prompt:

> A fictional data-quality contamination scanner in a premium data laboratory. Several abstract duplicate-like record tiles pass under a scanning arch; five small warning markers are detected, but the overall instrument remains calm rather than alarmist. Amber warning light, cyan baseline data flow, dark navy machinery, clean scientific interface framing with an empty panel for real text. The visual message is real warning, limited magnitude, not catastrophe. No readable text, no numbers, no logos, no watermark.

Suffixes:

```text
C01 — scanner on left third, quiet right evidence panel; warning markers subtle and low-salience.
C02 — horizontal conveyor low in the composition; broad upper evidence space; amber accent restrained.
C03 — compact centered scanner with large side margins; emphasize calm diagnostic inspection, not danger.
```

### 35.9 Generation plan artifact

Before generating, create:

```text
assets/review/MDL-2/art-generation-plan.json
```

For all 15 slots record:

```text
asset_id
candidate_id
prompt_version
full_prompt_sha256
generator/tool
model/version when exposed by the generator; otherwise the literal `UNKNOWN_NOT_EXPOSED` plus generator/tool evidence
reference_asset_ids
status
output_path
output_sha256
width
height
rights_basis
generated_at
```

If Codex cannot call an image generator in its environment, it must produce exact copy/paste generation packets and set:

```text
BLOCKED_HUMAN_ART_GENERATION
```

It may continue non-art engineering but cannot close MDL-2.

Candidate-generation rules:

- each C01/C02/C03 is a separate full generation, not a crop from one collage;
- prompt text is the exact global prefix + exact asset base prompt + exactly one candidate suffix + hard negatives;
- a technical regeneration of one failed slot retains the same candidate ID plus a recorded revision (`r2`, `r3`, ...); rejected bytes are never overwritten;
- no candidate may use an unapproved third-party character/image reference;
- if A02/other MDL-1 approved assets are supplied as a visual reference, record the exact approved reference SHA-256;
- record the generation service/tool and model identifier when exposed by the tool;
- record the rights/licensing basis sufficient for challenge submission;
- review/source files may remain outside the deployment package; only approved production derivatives are packaged.

### 35.10 Human review artifacts: contact sheets and overlay previews

Human review must not require opening 15 unrelated image files manually.

Create deterministic review artifacts under:

```text
assets/review/MDL-2/contact-sheets/
assets/review/MDL-2/previews/
```

For each A08–A12 asset:

1. produce one contact sheet containing C01–C03 at equal visual scale;
2. label the **review sheet**, not the candidate image itself, with candidate ID and source SHA prefix;
3. preserve candidate aspect ratio; never crop away a defect to make a candidate look better;
4. use a neutral review background;
5. include the approved MDL-1 palette/reference thumbnail only as a separate comparison panel when useful;
6. record the contact-sheet SHA-256 in the generation plan.

After `SOURCE_SELECTED`, create a deterministic overlay preview for the selected candidate:

```text
1440x900 representative Experiment Result frame
real HTML/UI-safe-zone rectangles or an equivalent deterministic review overlay
no fake production data baked into the art
```

The preview must demonstrate that:

- the primary analytical canvas remains unobstructed;
- a right-side Dr. Genie/evidence panel can coexist where applicable;
- known chart/table labels have sufficient contrast/background quietness;
- the art still works with the exact Case #042 instrument dimensions;
- no decorative machinery creates a false button/control affordance.

The overlay preview is a **review artifact**, not the production illustration. It may contain labels/guides because those are generated by deterministic review tooling, not by the image model.

Human source selection must reference the contact sheet. Final exact-byte approval must reference the production derivative **and** its overlay preview.

Add:

- `MDL2-ART-016` — five deterministic contact sheets exist and reference all 15 candidate hashes;
- `MDL2-ART-017` — contact-sheet generation does not mutate/crop source candidates deceptively;
- `MDL2-ART-018` — every selected candidate has a 1440x900 overlay preview;
- `MDL2-ART-019` — approval evidence references candidate hash, production hash, and preview hash;
- `MDL2-ART-020` — changing a production derivative or preview invalidates final approval.

### 35.10 Automated art preflight

For every candidate:

- decodes;
- dimensions sufficient;
- valid PNG/WebP review format;
- no orientation issue;
- no unsupported profile;
- prompt/hash/provenance record complete.

For selected production derivative:

- expected dimensions/crop;
- WebP/PNG;
- normally <1.5 MB;
- no generated text/numbers/logos/watermark;
- no fake controls;
- approved negative-space region survives crop;
- SHA-256 recorded;
- source candidate reference recorded;
- no oversized source working file accidentally included in frontend build.

### 35.11 Human selection and exact-byte approval

Create:

```text
docs/approvals/MDL-2-art.md
```

Two stages:

```text
SOURCE_SELECTED
FINAL_APPROVED
```

Example structure:

```yaml
iteration: MDL-2
status: PENDING
assets:
  - asset_id: A08
    selected_candidate: null
    source_sha256: null
    production_path: null
    production_sha256: null
    source_selection_evidence: null
    final_approval_evidence: null
  - asset_id: A09
  - asset_id: A10
  - asset_id: A11
  - asset_id: A12
approved_by: null
approved_at: null
notes: null
```

Preferred approval evidence is a GitHub PR review/comment by the designated human that identifies:

```text
iteration
asset ID
candidate ID
production SHA-256
APPROVED / REJECTED
```

CI verifies the evidence actor and exact hash where API access permits.

Codex must never self-approve.

Human review questions:

- matches A01/A02/A21/A28 visual system;
- feels premium/enterprise rather than childish;
- leaves sufficient real data/UI canvas;
- does not bake in false UI/data;
- does not accidentally reveal Case #042 answer;
- remains useful even if chart labels/values change;
- no accidental text/watermark;
- no visual contradiction with scientific rigor.

Any post-approval byte change invalidates approval.

---

## 36. Local completion gate

From a clean environment, execute the inherited MDL-1 gate plus MDL-2.

At minimum:

```text
repository/source/predecessor contract
npm ci
frontend typecheck/lint/unit/build
Python frozen install
Ruff
Python typecheck
backend tests
DG suite
DP PR sample (>=500/equivalent)
G42-001..027
MDL2 custom tests
SQL static/parse/privacy checks
canonical fixture regeneration --check
frontend private-truth bundle scan
art candidate/production preflight
```

Generate:

```text
release-report/MDL-2/golden-case.json
release-report/MDL-2/golden-case.md
release-report/MDL-2/generator.json
release-report/MDL-2/privacy-static.json
release-report/MDL-2/schema-fingerprint.json
release-report/MDL-2/data-contract-digest.json
release-report/MDL-2/art-preflight.json
```

`golden-case.json` includes at least:

```json
{
  "case_id": "CASE_0042",
  "case_template_version": 1,
  "generator_version": 1,
  "seed": 42,
  "canonical_sha256": "...",
  "expected": "125.00",
  "observed": "118.20",
  "deviation": "-6.80",
  "component_total": "-6.80",
  "v2_impact": "-5.90",
  "snapshot_v2_total": "-5.90",
  "dq_impact": "-0.30",
  "dq_overlapping": true,
  "formula_changed": false,
  "unreconciled": "0.00",
  "status": "PASS"
}
```

---

## 37. SQL source, object, and deployment fingerprints

Do not rely on a fragile byte-for-byte comparison of Databricks `SHOW CREATE VIEW` output, because the platform may canonicalize whitespace/qualification while preserving the same view.

Use three complementary proofs:

### 37.1 Repository source digest

Hash the exact rendered DDL/view SQL **before execution**, after replacing only the closed catalog/schema placeholders and normalizing line endings to LF. Record each migration/view source SHA-256 in the seed/deploy manifest.

### 37.2 Live structural fingerprint

After deployment, retrieve live object metadata and compute a structural fingerprint from:

```text
fully-qualified object name
object kind: TABLE | VIEW
ordered column names
ordered normalized data types
nullability where exposed reliably
```

For views, also record normalized `SHOW CREATE`/definition text **when the current workspace exposes it reliably**, but do not make cosmetic platform rewriting the sole acceptance criterion.

### 37.3 Behavioral fingerprint

Q1–Q8 plus SQ-001..020 are the behavioral proof. A structurally correct view that returns the wrong Case #042 evidence is a failure.

Required equality at closure:

```text
repository migration source hashes == hashes recorded by the seed/apply run
expected schema fingerprint == live schema fingerprint
canonical result contracts == live Q1-Q8/SQ results
```

Add:

- `MDL2-SQL-009` — migration manifest source hash matches repository-rendered SQL;
- `MDL2-SQL-010` — live table/view structural fingerprints match expected schemas;
- `MDL2-SQL-011` — qualification/whitespace differences in platform-rendered view SQL do not create a false failure when structure/results match;
- `MDL2-SQL-012` — source SQL change invalidates prior deployment/source-hash evidence.

## 38. Staging data deployment and live SQL gate

### 38.1 Preflight

Verify:

- target=`staging`;
- Free Edition target matches predecessor platform attestation;
- exact `implementation_sha` or current candidate SHA recorded;
- correct `MDL_CATALOG`;
- SQL warehouse resource/ID comes from environment/resource binding;
- deployment identity has expected seed privileges;
- app runtime identity is separately identifiable;
- effective app-runtime public/curated grants and private denial are captured before seeding;
- canonical fixture hash is green;
- rollback snapshot has been captured.

### 38.2 Apply

Execute repository DDL/view/seed workflow.

No success message before post-write verification.

### 38.3 Live verification

Run Q1–Q8 and SQ-001..020.

The live SQL harness must begin by reading the deployed `case_definition.generator_version`, `case_template_version`, and `seed`, then compare them with the accepted canonical package. If those identities differ, fail before grading downstream analytical values.

The seed/apply run and SQL-integration run must both record the same:

```text
implementation_sha
data_contract_digest
canonical_case_hash
case_template_version
generator_version
seed
target
catalog
```

A query result from the right workspace but wrong Case version is not acceptable evidence.

Also compare:

- deployed Case data hash/counts to canonical fixture;
- deployed view definition normalized hashes to repository SQL;
- app runtime curated access succeeds;
- app runtime private access denied.

### 38.4 Timing

Record query durations. Do not fail a correct result solely for a one-off noisy latency unless it violates an explicit timeout; performance closure is MDL-6.

### 38.5 Evidence artifact

Generate sanitized:

```text
release-report/MDL-2/sql-integration.json
```

Fields:

```text
target
catalog
warehouse_resource_key
implementation_sha
data_contract_digest
canonical_case_hash
ddl_source_hashes
view_source_hashes
live_object_structural_fingerprints
query_ids
result_contract_status
query_durations_ms
app_runtime_curated_access
app_runtime_private_access_denied
seed_run_id
rollback_manifest_ref
status
```

Never include OAuth/PAT/client secret or private truth payload.

---

## 39. App deployment and deployed smoke

After data is verified, deploy the exact accepted branch implementation using the MDL-1 source-provenance mechanism.

Automated deployed checks:

1. `/api/health` succeeds through supported Apps API authentication;
2. `/api/config` exposes no secret/private data;
3. `/api/cases/CASE_0042` returns public briefing values `125.00`, `118.20`, `-6.80`;
4. the backend trusted repository can query Case summary;
5. component path yields V2 `-5.90`;
6. V2 snapshot path yields 23/2/5 and `-5.90`;
7. DQ path yields 5 / `-0.30` / overlap true;
8. formula path yields unchanged;
9. lineage path reaches safe source/snapshot records;
10. reconciliation path yields zero residual;
11. app runtime cannot query private truth;
12. no frontend/static response contains private truth fixture;
13. no new public route exposes all unearned evidence;
14. deployed source identity/runtime digest corresponds to accepted implementation.

The browser root itself is inspected through the normal human App-access flow if headless UI auth is not supported; do not invent an insecure bypass.

---

## 40. Allowed manual inspection

After all automated checks pass, a human may:

- open Case #042 card/briefing and verify displayed data corresponds to automated result;
- inspect a representative curated query in Databricks;
- inspect grants/objects in Catalog Explorer;
- inspect logs for schema/query errors;
- inspect approved A08–A12 art/contact sheet/production derivatives;
- confirm A21 predecessor art remains unchanged;
- confirm no accidental generated text is visible.

Manual inspection is not the numerical oracle. If a functional/data defect is noticed manually:

1. add/extend an automated regression test;
2. fix the defect;
3. invalidate affected hashes/gates;
4. rerun affected CI/SQL/deploy/art approval as necessary.

---

## 41. GitHub merge closure

Before merge:

```bash
git fetch origin --prune
git merge-base --is-ancestor origin/main HEAD
git status --porcelain
git rev-parse HEAD
git rev-parse HEAD^{tree}
gh pr checks --watch
```

Require:

- branch fresh against current main;
- all shared MDL-1 checks green;
- all required MDL-2 checks green;
- human A08–A12 approval green;
- A21 predecessor hash unchanged;
- SQL integration green on the accepted data/code identity;
- deployment smoke green;
- runtime digest recorded;
- no unresolved required deferral/blocker.

Then designate:

```text
implementation_sha
implementation_tree_sha
implementation_runtime_digest
canonical_case_hash
```

If a later report-only commit is needed, the shared change classifier must prove runtime digest unchanged.

After merge:

- `main` CI green;
- merged runtime digest equals accepted implementation digest;
- if main-driven deployment runs, it is green;
- merge SHA/tree recorded in immutable CI/PR metadata;
- create MDL-3 predecessor evidence without creating a self-referential “update report with merge SHA” loop.

---

## 42. Required iteration report

`docs/iterations/MDL-2-report.md` must contain:

```text
status
iteration objective
base main SHA/tree
predecessor evidence reference
accepted V3 source SHA/addenda
branch and PR
implementation SHA/tree/runtime digest
case template version
generator version
release seed
canonical Case #042 hash
canonical fixture diff status
full reconciliation summary
DDL/view/query source hashes
actual catalog/schema mapping
seed run ID
rollback manifest/reference
SQL integration run/workflow ID
app runtime privilege verification
private truth denial evidence
deployment run/source identity
deployed smoke status
A21 predecessor hash verification
A08-A12 generation-plan reference
A08-A12 selected candidate + production hashes
A08-A12 contact-sheet hashes
A08-A12 overlay-preview hashes
human approval evidence
known limitations/deferred owner
decision/addendum references
```

Do not include:

```text
credentials
client secrets
OAuth tokens
PATs
private truth payload
full hidden path oracle
```

---

## 43. Definition of Done — MDL-2

All must be true:

### Predecessor / Git

- [ ] MDL-1 predecessor verification record is PASS.
- [ ] Accepted V3 source fingerprint/addenda are unchanged or explicitly approved.
- [ ] Branch `MDL-2` exists from current green `main`.
- [ ] `MDL-2-report.md` began as `IN_PROGRESS`.
- [ ] Branch pushed and PR created/updated.
- [ ] Final branch refreshed against current `origin/main`.

### Case/generator

- [ ] Public Case #042 template schema-valid and contains no truth pointer.
- [ ] Private generation/oracle spec isolated from frontend/Genie.
- [ ] Completion contract versioned.
- [ ] Generator interface and release/property modes implemented.
- [ ] Stable RNG/selection algorithm documented and tested.
- [ ] Monetary generation uses Decimal, not float.
- [ ] Canonical timestamps, `created_at`, run IDs and object IDs deterministic.
- [ ] Production seed fixed to 42.
- [ ] Canonical bundle serialization deterministic.
- [ ] Canonical Case #042 SHA generated and committed.
- [ ] Running generation twice produces identical canonical bytes.
- [ ] shared mutation operator registry is closed/versioned.
- [ ] VALUE_CHANGE/MISSING_ROWS/NEW_ROWS fully implemented for #042.
- [ ] remaining V3 operators have deterministic typed implementations/property coverage without enabling unreleased Cases.
- [ ] Level 1 and Level 2 test-only property templates exist and cannot appear in public catalog/API.

### Exact evidence

- [ ] `source_record` field semantics (`ACTIVE`, change flags, filter inclusion, no physical DQ duplicates) match the locked MDL-2 convention.
- [ ] deterministic pipeline-run rows exist with 42/45 rows written and zero replay/duplicate rows.
- [ ] `quality_issue.affected_keys` canonical JSON is exactly the five locked DQ keys.
- [ ] previous/current `population_hash` use the one canonical algorithm and are reproducible/different.

- [ ] Expected 125.00 / observed 118.20 / deviation -6.80 data-derived.
- [ ] V1/V2/V3/V4 values exact.
- [ ] component contribution deltas exact.
- [ ] V2 share derives to ~86.76% and presentation contract can round to 87%.
- [ ] V2 modified rows exactly 23 / -5.20.
- [ ] V2 removed rows exactly 2 / -0.80.
- [ ] V2 added rows exactly 5 / +0.10.
- [ ] V2 snapshot net exactly -5.90.
- [ ] TX-004291 exactly 4.20 -> 0.00 / -4.20.
- [ ] DQ affected keys exactly TX-004292..TX-004296.
- [ ] DQ affected row count 5 and overlapping impact -0.30.
- [ ] DQ is not independently additive.
- [ ] Formula IDs/hash unchanged.
- [ ] canonical full formula hash matches locked normalization.
- [ ] lineage acyclic and reaches source/snapshot/record evidence.
- [ ] technical lineage fallback honestly labeled if used.
- [ ] final reconciliation residual exactly 0.00 within tolerance.

### Databricks objects / repository

- [ ] Configured catalog + public/private/curated schemas exist.
- [ ] required public Delta tables exist.
- [ ] private `case_truth` exists.
- [ ] Case summary/component/snapshot/quality/semantic/pipeline/population/lineage views exist.
- [ ] view definitions are repository-controlled.
- [ ] data-contract digest and live-object fingerprint tooling exists and is used by CI.
- [ ] effective-permission verification tooling proves public/curated allow + private deny.
- [ ] Q1–Q8 fixed query templates exist.
- [ ] app SQL uses native parameters.
- [ ] typed SQL results reject schema mismatch.
- [ ] ordinary evidence repository cannot read private truth.
- [ ] no production arbitrary SQL/table API exists.
- [ ] no unrestricted evidence browser route leaks future evidence.

### Security / permissions

- [ ] app runtime has `CAN USE` warehouse as needed.
- [ ] app runtime has least-privilege public/curated UC access.
- [ ] app runtime does not have private truth SELECT in MDL-2.
- [ ] live app-runtime private SELECT test is denied.
- [ ] curated views contain no truth reference/column.
- [ ] frontend production bundle contains no private fixture/oracle.
- [ ] production static-package denylist/path/content scan is green.
- [ ] Genie-related repo config contains no `case_truth`.
- [ ] private-denial test logs do not leak truth payload.

### Tests

- [ ] DG-001..010 green.
- [ ] DP-001..020 applicable suite green.
- [ ] PR property tier meets ≥500/equivalent requirement.
- [ ] release/nightly property tier meets ≥10,000 requirement before closure.
- [ ] G42-001..027 100% green.
- [ ] SQ-001..020 real Databricks suite green.
- [ ] all required MDL2 custom tests green.
- [ ] zero skipped mandatory test caused a false pass.

### Seed/deploy

- [ ] seed plan mode non-mutating.
- [ ] seed apply idempotent.
- [ ] unrelated Case rows unchanged.
- [ ] rollback manifest captured.
- [ ] live seeded Case hash/counts match canonical package.
- [ ] repository SQL source hashes, live structural fingerprints, and behavioral Q1-Q8 contracts all match deployment evidence.
- [ ] final SQL integration artifact matches the final-head `data_contract_digest` and canonical Case hash.
- [ ] staging app deployed from accepted implementation identity.
- [ ] deployed evidence smoke green.
- [ ] no public evidence bypass added.

### Artwork

- [ ] A21 predecessor art hash unchanged and MDL-1 approval still valid.
- [ ] A08 generation plan has C01-C03 generated and MDL2-ART-001..003 green.
- [ ] A09 generation plan has C01-C03 generated and MDL2-ART-004..006 green.
- [ ] A10 generation plan has C01-C03 generated and MDL2-ART-007..009 green.
- [ ] A11 generation plan has C01-C03 generated and MDL2-ART-010..012 green.
- [ ] A12 generation plan has C01-C03 generated and MDL2-ART-013..015 green.
- [ ] all 15 candidates have prompt/provenance/hashes.
- [ ] deterministic A08-A12 contact sheets cover all candidate hashes and MDL2-ART-016..017 are green.
- [ ] every selected A08-A12 candidate has a 1440x900 overlay preview used in human review and MDL2-ART-018..020 are green.
- [ ] selected candidates pass technical preflight.
- [ ] production derivatives meet size/dimension/layout requirements.
- [ ] human explicitly selected/approved exact A08–A12 production bytes.
- [ ] human evidence actor/hash is verifiable.
- [ ] Codex did not self-approve.
- [ ] approval invalidation on byte change is tested.

### CI/closure

- [ ] required MDL-2 GitHub checks green on `implementation_sha`.
- [ ] SQL staging job green on correct head/data hash.
- [ ] `mdl2/human-approval-gate` green for real human evidence.
- [ ] release contract strict mode green.
- [ ] manual deployment/data/art inspection accepted.
- [ ] PR merged through protected flow.
- [ ] `main` CI green after merge.
- [ ] merged runtime digest matches accepted implementation digest.
- [ ] MDL-2 report complete without self-referential commit loop.
- [ ] MDL-3 predecessor evidence can be produced from immutable closure records.

If any box is false, MDL-2 is not closed.

---

## 44. Specification/repository maturity self-audit

Before MDL-2 can be declared `READY_TO_CLOSE`, `scripts/validate_mdl2_contract.py --strict` must additionally verify the implementation contract itself has not drifted.

At minimum:

- Markdown fences in the canonical MDL-2 contract are balanced;
- no duplicate Markdown headings at the same full heading text;
- every required canonical DG/DP/G42/SQ test ID assigned to MDL-2 appears exactly once in the traceability ledger;
- every custom `MDL2-*` test ID has exactly one canonical definition; later DoD/report references may repeat the ID but must resolve to that single definition, including ART-001..020;
- the Case #042 canonical record plan sums to all locked totals;
- DQ affected keys are exactly the documented five-key subset and sum to `-0.30`;
- source snapshot row counts derive to 42/45;
- public Case template contains no private truth pointer;
- release-state enums stay compatible with MDL-1; test templates use `test_only`, not a new public enum;
- Q1–Q8 query IDs all map to one SQL source and one typed result contract;
- DDL/views/trusted-query/source-generation/seed files exist and are included in `data_contract_digest`;
- `docs/traceability/mdl2-data-contract.json` records the current digest algorithm/version and included path policy;
- required live-SQL artifact references the current `data_contract_digest`;
- all 15 A08–A12 generation slots exist with independent candidate evidence;
- contact sheets and overlay previews resolve to the selected hashes;
- final art approval is not `APPROVED` without external human evidence;
- no `TODO`, `TBD`, fake `PASS`, placeholder credential, or unresolved catalog principal appears in executable SQL/YAML/code;
- MDL-2 report cannot be `COMPLETE` while a required gate/evidence/approval field is pending.

The validator may support `--allow-in-progress` during development; strict closure mode must fail closed.

Add:

- `MDL2-CONTRACT-009` — canonical record arithmetic is internally self-consistent;
- `MDL2-CONTRACT-010` — all mandatory test IDs/custom-ID **definitions** are unique and all references resolve to one definition;
- `MDL2-CONTRACT-011` — required data-contract paths all participate in digest calculation;
- `MDL2-CONTRACT-012` — closure report cannot claim COMPLETE with stale SQL/art/deploy evidence;
- `MDL2-CONTRACT-013` — target repository tree, one-command gate, CI jobs, and strict contract validator reference the same required MDL-2 scripts/artifact paths.

## 45. Codex first-hour runbook

The first implementation session should do only this sequence before writing substantive generator code:

1. read this file fully;
2. read the accepted V3 source sections/Appendix A;
3. inspect MDL-1 predecessor report/manifest/approvals/runtime digest;
4. run predecessor verifier;
5. verify clean, current `main`;
6. create/continue `MDL-2`;
7. create `MDL-2-report.md` with `IN_PROGRESS`;
8. push branch and open/update PR;
9. verify existing MDL-1 CI still runs on the branch;
10. create public/private Case #042 schema files without truth leakage;
11. create `art-generation-plan.json`;
12. launch A08–A12 candidate generation or produce explicit human generation packets if tool access is unavailable;
13. implement the generator in the order: Decimal/canonical/RNG -> records -> mutations -> validators -> fixtures;
14. do not touch live Databricks data until local G42/data validators are green.

If any external prerequisite blocks steps 1–9, report the exact blocker rather than bypassing it.

---

## 46. What should cause the specification to be reopened

Do **not** continue editing MDL-2 during implementation for ordinary coding choices.

Reopen/approve an addendum only if one of these occurs:

- current Databricks SQL/Apps/Unity Catalog behavior materially conflicts with the locked deployment or permission contract;
- exact V3 Case #042 values are found internally inconsistent;
- the accepted MDL-1 architecture materially differs from the assumptions here and cannot implement the same trust boundary;
- human intentionally changes the Case #042 story/data;
- human rejects the entire A08–A12 visual direction rather than an individual candidate;
- a security requirement cannot be satisfied with the available Free Edition model;
- a source-level contradiction cannot be resolved without changing intended product behavior.

Ordinary library/API implementation details belong in code/ADR, not a rewrite of the iteration contract.

---


# Appendix A — Executable DDL baseline

The migration runner resolves these logical placeholders from closed environment configuration:

```text
{{PUBLIC}}  = <MDL_CATALOG>.mad_data_lab_public
{{PRIVATE}} = <MDL_CATALOG>.mad_data_lab_private
{{CURATED}} = <MDL_CATALOG>.mad_data_lab_curated
```

The placeholders are **not** user input.

## A.1 Schemas

```sql
CREATE SCHEMA IF NOT EXISTS <MDL_CATALOG>.mad_data_lab_public;
CREATE SCHEMA IF NOT EXISTS <MDL_CATALOG>.mad_data_lab_private;
CREATE SCHEMA IF NOT EXISTS <MDL_CATALOG>.mad_data_lab_curated;
```

## A.2 Public tables

```sql
CREATE TABLE IF NOT EXISTS {{PUBLIC}}.case_definition (
  case_id STRING NOT NULL,
  public_number INT NOT NULL,
  slug STRING NOT NULL,
  seed BIGINT NOT NULL,
  generator_version INT NOT NULL,
  case_template_version INT NOT NULL,
  title STRING NOT NULL,
  hook STRING NOT NULL,
  datapoint_id STRING NOT NULL,
  entity_id STRING,
  period_id STRING,
  expected_value DECIMAL(18,2) NOT NULL,
  observed_value DECIMAL(18,2) NOT NULL,
  deviation DECIMAL(18,2) NOT NULL,
  currency STRING,
  scale STRING NOT NULL,
  difficulty STRING NOT NULL,
  release_state STRING NOT NULL,
  sort_order INT NOT NULL,
  required_case_ids STRING,
  learning_objectives STRING NOT NULL,
  status STRING NOT NULL,
  created_at TIMESTAMP NOT NULL
)
USING DELTA;
```

```sql
CREATE TABLE IF NOT EXISTS {{PUBLIC}}.datapoint_result (
  case_id STRING NOT NULL,
  datapoint_id STRING NOT NULL,
  entity_id STRING,
  period_id STRING,
  run_id STRING NOT NULL,
  run_ts TIMESTAMP NOT NULL,
  run_role STRING NOT NULL,
  value DECIMAL(18,2) NOT NULL,
  expected_value DECIMAL(18,2) NOT NULL,
  deviation DECIMAL(18,2) NOT NULL,
  formula_id STRING,
  formula_hash STRING,
  filter_id STRING,
  filter_hash STRING,
  population_hash STRING
)
USING DELTA;
```

```sql
CREATE TABLE IF NOT EXISTS {{PUBLIC}}.calculation_trace (
  case_id STRING NOT NULL,
  datapoint_id STRING NOT NULL,
  run_id STRING NOT NULL,
  parent_node_id STRING,
  node_id STRING NOT NULL,
  node_type STRING NOT NULL,
  label STRING NOT NULL,
  operation STRING NOT NULL,
  formula STRING,
  value DECIMAL(18,2),
  previous_value DECIMAL(18,2),
  contribution_delta DECIMAL(18,2),
  source_table STRING,
  source_column STRING,
  filters_json STRING,
  join_json STRING,
  snapshot_id STRING,
  sequence_no INT NOT NULL
)
USING DELTA;
```

```sql
CREATE TABLE IF NOT EXISTS {{PUBLIC}}.source_snapshot (
  snapshot_id STRING NOT NULL,
  case_id STRING NOT NULL,
  source_table STRING NOT NULL,
  as_of_ts TIMESTAMP NOT NULL,
  row_count BIGINT NOT NULL,
  status STRING NOT NULL,
  snapshot_role STRING NOT NULL,
  pipeline_run_id STRING
)
USING DELTA;
```

```sql
CREATE TABLE IF NOT EXISTS {{PUBLIC}}.source_record (
  case_id STRING NOT NULL,
  snapshot_id STRING NOT NULL,
  business_key STRING NOT NULL,
  entity_id STRING,
  period_id STRING,
  component STRING,
  segment_id STRING,
  amount DECIMAL(18,2),
  record_status STRING NOT NULL,
  changed_from_previous BOOLEAN NOT NULL,
  duplicate_group_id STRING,
  included_by_filter BOOLEAN,
  source_table STRING NOT NULL,
  source_column STRING
)
USING DELTA;
```

```sql
CREATE TABLE IF NOT EXISTS {{PUBLIC}}.snapshot_diff (
  case_id STRING NOT NULL,
  component STRING,
  business_key STRING NOT NULL,
  entity_id STRING,
  segment_id STRING,
  change_type STRING NOT NULL,
  old_value DECIMAL(18,2),
  new_value DECIMAL(18,2),
  impact DECIMAL(18,2) NOT NULL,
  duplicate_group_id STRING,
  pipeline_run_id STRING,
  previous_snapshot_id STRING,
  current_snapshot_id STRING NOT NULL
)
USING DELTA;
```

```sql
CREATE TABLE IF NOT EXISTS {{PUBLIC}}.quality_issue (
  case_id STRING NOT NULL,
  issue_id STRING NOT NULL,
  rule_name STRING NOT NULL,
  severity STRING NOT NULL,
  affected_keys STRING,
  affected_row_count INT NOT NULL,
  estimated_impact DECIMAL(18,2),
  impact_is_overlapping BOOLEAN NOT NULL,
  status STRING NOT NULL,
  evidence_note STRING
)
USING DELTA;
```

```sql
CREATE TABLE IF NOT EXISTS {{PUBLIC}}.pipeline_run_evidence (
  case_id STRING NOT NULL,
  pipeline_run_id STRING NOT NULL,
  run_ts TIMESTAMP NOT NULL,
  source_snapshot_id STRING,
  execution_status STRING NOT NULL,
  replay_of_run_id STRING,
  rows_written BIGINT NOT NULL,
  duplicate_rows_written BIGINT NOT NULL,
  note STRING
)
USING DELTA;
```

```sql
CREATE TABLE IF NOT EXISTS {{PUBLIC}}.semantic_change_evidence (
  case_id STRING NOT NULL,
  semantic_type STRING NOT NULL,
  previous_id STRING,
  current_id STRING,
  previous_hash STRING,
  current_hash STRING,
  affected_population_count INT,
  estimated_impact DECIMAL(18,2),
  details_json STRING
)
USING DELTA;
```

```sql
CREATE TABLE IF NOT EXISTS {{PUBLIC}}.technical_lineage_curated (
  case_id STRING NOT NULL,
  source_table STRING NOT NULL,
  source_column STRING,
  target_table STRING NOT NULL,
  target_column STRING,
  entity_type STRING NOT NULL,
  event_time TIMESTAMP,
  lineage_source STRING NOT NULL
)
USING DELTA;
```

## A.3 Private table

```sql
CREATE TABLE IF NOT EXISTS {{PRIVATE}}.case_truth (
  case_id STRING NOT NULL,
  primary_component STRING,
  primary_source STRING,
  primary_cause STRING NOT NULL,
  secondary_cause STRING,
  affected_rows INT,
  expected_impact DECIMAL(18,2),
  secondary_expected_impact DECIMAL(18,2),
  expected_total_deviation DECIMAL(18,2) NOT NULL,
  confidence STRING NOT NULL,
  allowed_final_status_json STRING,
  expected_path_json STRING,
  truth_json STRING
)
USING DELTA;
```

If later runtime validation requires a narrower private projection, create a dedicated backend-only view/table with only the fields needed; do not broaden the public/curated surface.

---

# Appendix B — Executable curated-view baseline

Implement these definitions or a target-workspace-equivalent whose normalized output schema and results are identical.

## B.1 Case summary

```sql
CREATE OR REPLACE VIEW {{CURATED}}.case_summary AS
WITH runs AS (
  SELECT
    case_id,
    MAX(CASE WHEN run_role = 'CURRENT' THEN run_id END) AS current_run_id,
    MAX(CASE WHEN run_role = 'PREVIOUS' THEN run_id END) AS previous_run_id,
    MAX(CASE WHEN run_role = 'CURRENT' THEN formula_id END) AS current_formula_id,
    MAX(CASE WHEN run_role = 'PREVIOUS' THEN formula_id END) AS previous_formula_id,
    MAX(CASE WHEN run_role = 'CURRENT' THEN formula_hash END) AS current_formula_hash,
    MAX(CASE WHEN run_role = 'PREVIOUS' THEN formula_hash END) AS previous_formula_hash,
    MAX(CASE WHEN run_role = 'CURRENT' THEN filter_id END) AS current_filter_id,
    MAX(CASE WHEN run_role = 'PREVIOUS' THEN filter_id END) AS previous_filter_id,
    MAX(CASE WHEN run_role = 'CURRENT' THEN filter_hash END) AS current_filter_hash,
    MAX(CASE WHEN run_role = 'PREVIOUS' THEN filter_hash END) AS previous_filter_hash,
    MAX(CASE WHEN run_role = 'CURRENT' THEN population_hash END) AS current_population_hash,
    MAX(CASE WHEN run_role = 'PREVIOUS' THEN population_hash END) AS previous_population_hash
  FROM {{PUBLIC}}.datapoint_result
  GROUP BY case_id
)
SELECT
  c.case_id,
  c.public_number,
  c.slug,
  c.title,
  c.datapoint_id,
  c.entity_id,
  c.period_id,
  c.expected_value,
  c.observed_value,
  c.deviation,
  c.currency,
  c.scale,
  c.difficulty,
  r.current_run_id,
  r.previous_run_id,
  r.current_formula_id,
  r.previous_formula_id,
  r.current_formula_hash,
  r.previous_formula_hash,
  r.current_filter_id,
  r.previous_filter_id,
  r.current_filter_hash,
  r.previous_filter_hash,
  r.current_population_hash,
  r.previous_population_hash
FROM {{PUBLIC}}.case_definition c
JOIN runs r ON r.case_id = c.case_id
WHERE c.status = 'ACTIVE';
```

## B.2 Component evidence

```sql
CREATE OR REPLACE VIEW {{CURATED}}.component_evidence AS
WITH component_nodes AS (
  SELECT
    case_id,
    node_id AS component,
    label,
    value AS current_value,
    previous_value,
    contribution_delta,
    source_table,
    source_column,
    sequence_no
  FROM {{PUBLIC}}.calculation_trace
  WHERE node_type = 'COMPONENT'
),
totals AS (
  SELECT
    case_id,
    ABS(deviation) AS abs_total_deviation
  FROM {{PUBLIC}}.case_definition
)
SELECT
  c.case_id,
  c.component,
  c.label,
  c.previous_value,
  c.current_value,
  c.contribution_delta,
  ABS(c.contribution_delta) AS abs_contribution,
  CASE
    WHEN t.abs_total_deviation = 0 THEN 0
    ELSE ABS(c.contribution_delta) / t.abs_total_deviation
  END AS share_of_abs_deviation,
  DENSE_RANK() OVER (
    PARTITION BY c.case_id
    ORDER BY ABS(c.contribution_delta) DESC, c.sequence_no
  ) AS abs_contribution_rank,
  c.source_table,
  c.source_column,
  c.sequence_no
FROM component_nodes c
JOIN totals t ON t.case_id = c.case_id;
```

## B.3 Snapshot evidence

```sql
CREATE OR REPLACE VIEW {{CURATED}}.snapshot_evidence AS
SELECT
  d.case_id,
  d.component,
  d.business_key,
  d.entity_id,
  d.segment_id,
  d.change_type,
  d.old_value,
  d.new_value,
  d.impact,
  d.duplicate_group_id,
  d.pipeline_run_id,
  d.previous_snapshot_id,
  d.current_snapshot_id,
  COUNT(*) OVER (
    PARTITION BY d.case_id, d.change_type
  ) AS change_type_count,
  SUM(d.impact) OVER (
    PARTITION BY d.case_id, d.change_type
  ) AS change_type_total_impact,
  SUM(d.impact) OVER (
    PARTITION BY d.case_id, d.component
  ) AS component_total_impact
FROM {{PUBLIC}}.snapshot_diff d;
```

## B.4 Quality evidence

```sql
CREATE OR REPLACE VIEW {{CURATED}}.quality_evidence AS
SELECT
  q.case_id,
  q.issue_id,
  q.rule_name,
  q.severity,
  q.affected_keys,
  q.affected_row_count,
  q.estimated_impact,
  q.impact_is_overlapping,
  q.status,
  q.evidence_note,
  c.deviation AS total_deviation,
  CASE
    WHEN c.deviation = 0 OR q.estimated_impact IS NULL THEN NULL
    ELSE ABS(q.estimated_impact) / ABS(c.deviation)
  END AS deviation_share
FROM {{PUBLIC}}.quality_issue q
JOIN {{PUBLIC}}.case_definition c
  ON c.case_id = q.case_id;
```

## B.5 Semantic evidence

```sql
CREATE OR REPLACE VIEW {{CURATED}}.semantic_evidence AS
SELECT
  case_id,
  semantic_type,
  previous_id,
  current_id,
  previous_hash,
  current_hash,
  CASE
    WHEN COALESCE(previous_hash, '') <> COALESCE(current_hash, '')
      OR COALESCE(previous_id, '') <> COALESCE(current_id, '')
    THEN true
    ELSE false
  END AS changed,
  affected_population_count,
  estimated_impact,
  details_json
FROM {{PUBLIC}}.semantic_change_evidence;
```

## B.6 Pipeline evidence

```sql
CREATE OR REPLACE VIEW {{CURATED}}.pipeline_evidence AS
SELECT
  case_id,
  pipeline_run_id,
  run_ts,
  source_snapshot_id,
  execution_status,
  replay_of_run_id,
  rows_written,
  duplicate_rows_written,
  note
FROM {{PUBLIC}}.pipeline_run_evidence;
```

## B.7 Population evidence

```sql
CREATE OR REPLACE VIEW {{CURATED}}.population_evidence AS
SELECT
  r.case_id,
  s.snapshot_role,
  r.entity_id,
  r.segment_id,
  COUNT(*) AS row_count,
  SUM(COALESCE(r.amount, 0)) AS total_amount,
  SUM(CASE WHEN r.duplicate_group_id IS NOT NULL THEN 1 ELSE 0 END) AS duplicate_row_count,
  SUM(CASE WHEN r.included_by_filter = true THEN 1 ELSE 0 END) AS included_row_count,
  SUM(CASE WHEN r.included_by_filter = false THEN 1 ELSE 0 END) AS excluded_row_count
FROM {{PUBLIC}}.source_record r
JOIN {{PUBLIC}}.source_snapshot s
  ON s.case_id = r.case_id
 AND s.snapshot_id = r.snapshot_id
GROUP BY
  r.case_id,
  s.snapshot_role,
  r.entity_id,
  r.segment_id;
```

## B.8 Lineage evidence

```sql
CREATE OR REPLACE VIEW {{CURATED}}.lineage_evidence AS
SELECT
  c.case_id,
  c.sequence_no AS depth,
  c.node_type,
  c.node_id,
  c.parent_node_id,
  CASE WHEN c.node_type = 'COMPONENT' THEN c.node_id END AS component,
  c.source_table,
  c.source_column,
  c.snapshot_id,
  CAST(NULL AS STRING) AS target_table,
  CAST(NULL AS STRING) AS target_column,
  'VALUE_LINEAGE' AS lineage_source
FROM {{PUBLIC}}.calculation_trace c

UNION ALL

SELECT
  t.case_id,
  100 AS depth,
  'TECHNICAL_OBJECT' AS node_type,
  CONCAT(t.source_table, ':', COALESCE(t.source_column, '*')) AS node_id,
  CAST(NULL AS STRING) AS parent_node_id,
  CAST(NULL AS STRING) AS component,
  t.source_table,
  t.source_column,
  CAST(NULL AS STRING) AS snapshot_id,
  t.target_table,
  t.target_column,
  t.lineage_source
FROM {{PUBLIC}}.technical_lineage_curated t;
```

---

# Appendix C — Required data invariants in SQL

The release verification script must also execute zero-row failure queries, including:

```sql
-- Case deviation must equal observed - expected.
SELECT case_id
FROM {{PUBLIC}}.case_definition
WHERE ABS(deviation - (observed_value - expected_value)) > 0.01;
```

Expected: zero rows.

```sql
-- Case #042 component contribution reconciliation.
SELECT case_id
FROM (
  SELECT
    case_id,
    SUM(contribution_delta) AS component_delta
  FROM {{CURATED}}.component_evidence
  WHERE case_id = 'CASE_0042'
  GROUP BY case_id
) c
JOIN {{CURATED}}.case_summary s USING (case_id)
WHERE ABS(c.component_delta - s.deviation) > 0.01;
```

Expected: zero rows.

```sql
-- Case #042 V2 snapshot reconciliation.
SELECT case_id
FROM (
  SELECT
    case_id,
    SUM(impact) AS snapshot_delta
  FROM {{CURATED}}.snapshot_evidence
  WHERE case_id = 'CASE_0042'
    AND component = 'V2'
  GROUP BY case_id
) d
JOIN {{CURATED}}.component_evidence c
  ON c.case_id = d.case_id
 AND c.component = 'V2'
WHERE ABS(d.snapshot_delta - c.contribution_delta) > 0.01;
```

Expected: zero rows.

Curated-view privacy verification must inspect view definitions/metadata and fail if any contains:

```text
mad_data_lab_private
case_truth
expected_path_json
truth_json
allowed_final_status_json
```

The validator must distinguish an intentional test string from an actual deployed view definition.

---


# Final MDL-2 execution statement

**MDL-2 is complete only when Case #042 is no longer a collection of hardcoded demo facts but a deterministic, reconciled, queryable, least-privilege evidence package whose public and curated outputs exactly support the later Genie investigation while its private truth remains isolated. The accepted data, SQL, deployment, tests, and analytical artwork must all be traceable to the same implementation identity and human approvals before MDL-3 begins.**
