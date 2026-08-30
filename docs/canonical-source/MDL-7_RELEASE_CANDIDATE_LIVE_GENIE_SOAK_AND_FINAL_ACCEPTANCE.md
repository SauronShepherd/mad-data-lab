# MDL-7 - Release Candidate, Full Live Genie Evaluation, Deployed Soak, Release Report, and Final Functional Acceptance

## Purpose

MDL-7 is the release-candidate hardening iteration. No new product features are allowed unless they are necessary to fix a release blocker. The objective is to prove that the complete Case #042 experience works repeatedly with real Databricks resources, real Genie conversations, real curated SQL evidence, and the production build deployed on Databricks Free Edition.

This iteration converts the application from "feature complete" to "recordable release candidate".

The decisive requirements are:

- full release pipeline green;
- 40-80 live Genie benchmark prompts at release quality;
- 10 consecutive full live Case #042 Investigations on the deployed application;
- critical numeric answers 100% correct;
- hidden-truth leakage 0;
- formula hypothesis never falsely promoted;
- DQ warning never incorrectly promoted to primary cause;
- reconciliation residual always zero for the golden Case;
- fallback rate within release threshold;
- first complete manual functional acceptance performed only after automated R1-R7 gates pass;
- final in-app character pose/polish art human-approved;
- branch, PR, GitHub CI, deployed smoke, release report, and merge all green.

## Preconditions

Do not start MDL-7 unless:

- MDL-6 merged to `main`;
- `main` CI green;
- Case #042 complete fake-Genie E2E green;
- curated SQL integration green;
- live Genie critical smoke green;
- all required Instruments present;
- no serious/critical accessibility issue;
- security/chaos/media gates green;
- production offline mode disabled;
- MDL-6 art/audio approval recorded;
- there are no planned feature additions required for the demo narrative.

## Branch and Git workflow - mandatory

```bash
git fetch origin --prune
git checkout main
git pull --ff-only origin main
test -z "$(git status --porcelain)"
git checkout -b MDL-7
```

Recommended commits are intentionally limited:

```text
MDL-7: expand release Genie benchmarks and deployed soak harness
MDL-7: fix release blockers found by automated RC gates
MDL-7: finalize approved skeptical Dr Genie pose and visual consistency
MDL-7: generate complete release report
MDL-7: record final manual acceptance results
```

Every bug fix discovered in MDL-7 must include an automated regression test before or alongside the fix.

Push and PR:

```bash
git push -u origin MDL-7
gh pr create --base main --head MDL-7 --title "MDL-7 Release candidate and live soak" --body-file docs/iterations/MDL-7-report.md
```

Do not merge until the full release-candidate gates and manual acceptance in this file pass.

## Feature freeze rules

Allowed:

- reliability fixes;
- benchmark/prompt curation;
- SQL performance/correctness fixes;
- accessibility defects;
- obvious visual defects;
- telemetry/logging fixes;
- copy corrections;
- release/reporting scripts;
- demo-critical art consistency fixes.

Forbidden without explicit human approval:

- new playable Case;
- new Experiment family;
- new persistence architecture;
- new framework/library with broad impact;
- changing Case #042 truth;
- visual redesign unrelated to a defect;
- replacing the core Genie integration model;
- weakening tests or thresholds to force a green result.

If a secondary Case is currently enabled and does not meet its release gates, disable it through server-owned release state rather than spending RC time rewriting it.

## Release-candidate test environments

Use all relevant V3 tiers:

```text
E0 - pure local unit
E1 - local full-stack fake Genie / fixture data
E2 - local/staging real SQL, fake Genie
E3 - real Genie + real SQL
E4 - deployed Databricks App release candidate
```

The E4 deployed result is the authoritative challenge candidate.

## Full release pipeline

By MDL-7, the GitHub release workflow must run the equivalent of:

1. validate repository;
2. install locked dependencies;
3. static checks;
4. unit/component tests;
5. property/data tests;
6. G42 golden suite;
7. frontend production build;
8. image/audio asset preflight;
9. backend integration with fakes;
10. full fake-Genie E2E suite;
11. visual regression;
12. accessibility;
13. dependency/security audit;
14. real Databricks SQL integration;
15. live Genie evaluation;
16. deploy release candidate;
17. wait for app RUNNING;
18. deployed API/browser smoke;
19. deployed live Case #042 soak;
20. release report generation.

No mandatory stage may be silently skipped.

## GitHub Actions release workflow

Create or finalize a workflow such as:

```text
.github/workflows/release-candidate.yml
```

Use a protected GitHub Environment for the Databricks target.

Preferred auth: workload identity federation / OIDC.

Required permissions should be minimal, for example:

```text
id-token: write
contents: read
```

If the release workflow needs to write a GitHub release or PR comment, add only the exact required permission.

### Deployment behavior

The workflow must:

```text
databricks bundle validate --target <rc/prod>
databricks bundle deploy --target <rc/prod>
databricks bundle run <app-resource> --target <rc/prod>
```

Then poll app state until RUNNING or timeout/fail.

A successful `bundle deploy` without `bundle run` is not sufficient because the app process can continue serving old code.

Record deployed Git commit SHA/version in a safe application version endpoint or release metadata.

## Release Gate R1 - Build integrity

Required:

- frontend production build green;
- backend imports/starts;
- no lint/type blockers;
- lockfiles valid;
- no missing production assets;
- no unapproved generated source assets packaged;
- no file over platform limit;
- no obsolete fantasy-genie/board asset referenced by production.

## Release Gate R2 - Data integrity

Required:

- 100% G42 golden tests;
- generator deterministic hash matches expected;
- property/data suite green;
- reconciliation residual zero;
- curated/private truth isolation green;
- real SQL integration green;
- every enabled secondary Case has 100% of its own golden contract or is disabled.

## Release Gate R3 - Guided flow integrity

Required:

- full Case Board/progression fixture E2E green;
- complete fake-Genie Case #042 E2E green;
- no illegal transitions;
- no duplicate-action bugs;
- initial/final predictions separate;
- scoring/badges deterministic;
- final conclusion blocked until completion contract.

## Release Gate R4 - UX integrity

Required:

- visual regression approved;
- no serious/critical axe findings;
- 1280x720 fully usable;
- 1440x900 demo viewport clean;
- reduced motion works;
- keyboard-only flow works;
- conclusion understandable with sound off.

## Release Gate R5 - Asset integrity

Required:

- image manifest green;
- audio technical preflight green;
- final audio human-approved from MDL-6;
- no individual file over platform limit;
- no missing asset;
- current MDL-7 art approval green.

## Release Gate R6 - Genie quality

This is a release blocker.

### Expand benchmark suite to 40-80 prompts

The suite must include multiple phrasings across at least these intents:

```text
I01 observation
I02 dominant component
I03 component decomposition
I04 V2 snapshot changes
I05 top source record
I06 DQ issue existence
I07 DQ materiality
I08 formula change
I09 value lineage
I10 next Experiment after observation
I11 next Experiment after component evidence
I12 final hypothesis states
I13 final summary
I14 explicit insufficient-evidence behavior
I15 hidden-truth attack
```

Add cross-Case generic benchmark prompts only for Cases actually enabled in production.

### Grading rules

Do not grade prose exactness.

Fail for:

- wrong Experiment;
- wrong target component;
- wrong numeric evidence;
- invalid status;
- invented cause;
- missing required reconciliation;
- hidden truth disclosure;
- invalid protocol after repair;
- DQ overlap double-counted;
- formula falsely said changed.

### Release thresholds

Required:

```text
>=95% overall good live responses
100% critical deterministic numeric prompts
100% hidden-truth/security prompts safe
100% allowed-enum/control validity after at most one repair
<=5% safe fallback across release benchmark, preferably 0 on demo-critical path
```

For the canonical guided first/second Experiment prompts, target 100% correct selection.

If a required threshold is not met, do not lower the threshold. Improve curation/prompt/schema/data and rerun.

## Release Gate R7 - Deployed app and live soak

### Automated deployed smoke

Before full soak, verify on the deployed RC:

- root app loads;
- `/api/health` green;
- safe config/version visible;
- Genie resource configured;
- warehouse resource configured;
- Case #042 public data correct;
- one live Genie start succeeds;
- one live Experiment succeeds;
- no production offline mode;
- no hidden truth in responses;
- no browser console error on critical path.

### Ten-run full live Case #042 soak

Automate 10 consecutive full Investigations against the deployed application.

Each run must:

1. create a new session;
2. start a new Genie conversation;
3. obtain H1/H2/H3;
4. submit an initial prediction through the API or browser harness;
5. allow Genie to choose Experiment(s);
6. obtain/validate component evidence;
7. obtain/validate snapshot evidence;
8. obtain/validate DQ materiality;
9. obtain/validate formula evidence;
10. obtain/inspect required source/lineage evidence;
11. reconcile to zero residual;
12. submit final prediction;
13. conclude;
14. verify final formula status RULED_OUT;
15. verify DQ is not primary;
16. verify source-change explanation supported/confirmed at correct granularity;
17. reach Debrief;
18. record every Genie/fallback event and latency.

### Soak acceptance

Required overall:

```text
10/10 complete successfully
10/10 correct final evidence
10/10 formula unchanged / formula hypothesis ruled out
10/10 DQ not promoted to primary cause
10/10 zero material unreconciled amount
```

Preferred:

```text
10/10 without safe fallback
```

Absolute release minimum from V3:

```text
>=9/10 without fallback
10/10 successful overall
```

If the 10-run result fails:

- treat as release blocker;
- diagnose by experiment/message ID;
- add regression/evaluation coverage;
- tune prompts/metadata/data;
- redeploy;
- restart the 10-run release soak from run 1.

Do not count partial earlier runs toward a new post-fix soak.

## Enabled secondary Cases

If any secondary Case is enabled for challenge production, it must pass its own specified gates before MDL-7 closes:

- deterministic/golden contract;
- fake Genie E2E;
- live Genie benchmarks;
- 5 consecutive deployed full Investigations;
- zero material residual;
- hidden-truth safe;
- visual/accessibility coverage for any unique Instrument.

If not green, mark the Case `COMING_SOON`/unavailable and remove it from live release scope. Do not jeopardize #042.

## Release report generation

Finalize `scripts/release_gate.py` to write:

```text
release-report/MDL-7/
  summary.md
  test-results.xml
  genie-eval.json
  golden-case.json
  asset-preflight.json
  audio-preflight.json
  accessibility-summary.json
  security-summary.json
  performance-summary.json
  visual-diff-summary.json
  deployed-smoke.json
  live-soak.json
```

`summary.md` must show every release gate as PASS/FAIL with evidence links/paths.

Never include credentials or raw hidden truth payloads in public CI artifacts. A golden oracle report may include the known synthetic expected values needed for validation but must not be shipped to the browser/app.

## Artwork checkpoint - mandatory before iteration closure

MDL-7 creates the final skeptical Dr. Genie pose used for the DQ false-lead segment and performs a complete in-app character consistency review.

### MDL7-A04 - Dr. Genie skeptical pose

Use the approved MDL-1 master character reference.

Prompt intent:

```text
Same approved Dr. Genie character and exact wardrobe. Skeptical analytical pose, arms lightly crossed, head slightly tilted, one eyebrow raised, examining an invisible warning panel as if questioning whether a data-quality alert is actually material. Calm, intelligent, mildly humorous expression. Transparent background. Same premium stylized 3D rendering and proportions. No text, logo, watermark, fantasy-genie traits, lamp, smoke body, or magical costume.
```

Target: match the established portrait production size and transparent-background conventions.

### Art consistency audit

Create an automated/contact-sheet review containing all approved Dr. Genie poses:

```text
master
thinking
eureka
skeptical
```

Review for:

- same face/hair/goggles/coat;
- same proportions;
- same rendering style;
- no pose suddenly becomes a fantasy genie;
- no generated text;
- transparent edges clean;
- consistent scale/crop in UI.

### Human approval

Create `docs/approvals/MDL-7-art.md` with status `PENDING`.

A human must explicitly approve:

- MDL7-A04 skeptical pose;
- the full Dr. Genie character consistency sheet;
- the final in-app crop/placement of all Dr. Genie poses.

Codex cannot self-approve.

## Manual functional acceptance - first required full human playthrough

This happens only AFTER R1-R7 and the ten-run soak are green.

Use a clean browser session against the exact deployed RC commit.

Perform the V3 manual checklist:

1. open deployed app;
2. confirm MAD DATA LAB and Case #042 visible;
3. enable music and confirm low volume;
4. start Investigation;
5. confirm hypotheses readable/credible;
6. make one prediction;
7. run Genie's next Experiment;
8. confirm V2 Waterfall immediately understandable;
9. run/observe Snapshot comparison;
10. confirm counts/impacts readable;
11. open TX-004291;
12. open DQ panel and confirm no overclaim;
13. open lineage and confirm legible;
14. complete required formula/reconciliation evidence;
15. make final prediction;
16. reveal/obtain Scientific Verdict;
17. confirm final explanation matches visible evidence;
18. confirm formula RULED_OUT;
19. confirm DQ not primary;
20. confirm score/debrief;
21. mute/unmute music;
22. reload once and verify documented restart/recovery behavior;
23. check no debug IDs/secrets visible;
24. check no generated image contains accidental text in a prominent area;
25. confirm the complete interaction fits the planned 2-3 minute narrative.

### Pass/fail rule

If the human discovers any functional defect:

1. stop acceptance;
2. add an automated regression test;
3. fix defect in `MDL-7`;
4. rerun all affected release gates;
5. redeploy;
6. rerun the full ten-run soak if the change can affect Genie/data/state/conclusion behavior;
7. repeat the relevant manual step only after green.

Do not waive a bug because the demo recorder can avoid it.

## GitHub CI verification

Use:

```bash
gh run list --branch MDL-7 --limit 50
gh pr checks --watch
```

Also verify manually-triggered release jobs:

```text
real SQL integration
live Genie evaluation
Databricks deploy
live soak
```

Record workflow run IDs and URLs in the iteration report.

A green local environment is insufficient.

## RC tagging and rollback

After all gates and human acceptance pass, create a release candidate tag only if repository policy permits:

```text
submission-rc1
```

Tag the exact commit that passed the automated and manual gates.

Do not retag a different commit with the same tag.

Record previous known-good deployment version/commit for rollback.

## Merge and post-merge verification

Merge `MDL-7` only after all gates including human acceptance.

After merge:

1. verify `main` CI green;
2. verify the deployed app still corresponds to the accepted commit or redeploy the merge commit if required;
3. rerun a short deployed smoke if merge commit differs from RC branch commit;
4. do not make new feature changes on `main`.

## Required iteration report

Create `docs/iterations/MDL-7-report.md` with:

- branch/PR/base/final/merge commit SHAs;
- RC tag;
- GitHub CI workflow IDs;
- real SQL integration result;
- live Genie benchmark totals/pass rates;
- list of any repaired protocol responses;
- safe fallback count/rate;
- ten-run soak table per run;
- p50/p95 Genie and SQL latency if measured;
- R1-R7 PASS summary;
- manual acceptance checklist result;
- art approval record;
- exact Databricks deployment/version;
- rollback reference;
- remaining items limited strictly to submission packaging in MDL-8.

## Definition of Done - MDL-7

- [ ] Branch `MDL-7` created from green merged MDL-6 `main`.
- [ ] Feature freeze respected.
- [ ] Full release GitHub workflow exists and executes all mandatory tiers.
- [ ] R1 Build integrity PASS.
- [ ] R2 Data integrity PASS.
- [ ] R3 Guided flow integrity PASS.
- [ ] R4 UX integrity PASS.
- [ ] R5 Asset integrity PASS.
- [ ] R6 Genie quality PASS.
- [ ] R7 Deployed app PASS.
- [ ] Live Genie suite contains 40-80 prompts.
- [ ] Overall live quality >=95%.
- [ ] Critical numeric prompts 100% correct.
- [ ] Hidden-truth prompts 100% safe.
- [ ] Protocol valid after at most one repair for all critical prompts.
- [ ] Ten consecutive full deployed Case #042 runs completed successfully.
- [ ] All ten runs produce zero material reconciliation residual.
- [ ] All ten runs rule out formula change.
- [ ] All ten runs do not promote DQ to primary cause.
- [ ] At least 9/10 runs have no safe fallback; target 10/10.
- [ ] Any enabled secondary Case passes its own release gates or is disabled.
- [ ] Complete release report generated and archived.
- [ ] MDL7-A04 skeptical Dr. Genie generated/preflighted.
- [ ] Full Dr. Genie consistency sheet reviewed.
- [ ] Human explicitly approves MDL-7 artwork.
- [ ] First complete manual functional acceptance passes after automated gates.
- [ ] GitHub CI and all protected release jobs green.
- [ ] Databricks RC deployment is the accepted build.
- [ ] `submission-rc1` or equivalent exact accepted version recorded.
- [ ] Branch pushed and PR merged only after all gates.
- [ ] `main` CI green after merge.
- [ ] Iteration report complete.

If any item is false, do not start the final submission freeze in MDL-8.
