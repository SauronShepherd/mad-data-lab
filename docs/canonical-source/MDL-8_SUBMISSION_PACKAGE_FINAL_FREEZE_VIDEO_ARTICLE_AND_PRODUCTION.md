# MDL-8 - Submission Package, Final Freeze, Demo Video, Community Article, Production Deployment, and Challenge Submission

## Purpose

MDL-8 turns the accepted release candidate into the final Databricks Genie-Powered App Challenge submission. Product development is effectively over. This iteration is about preserving the accepted technical build, preparing the public demonstration/story, completing final production artwork, validating all public links, and submitting before the internal deadline.

Current challenge requirements verified for the 2026 contest include:

- build a Databricks App on Free Edition;
- configure and connect a Genie Agent;
- put Genie at the core of the main experience;
- choose a track; MAD DATA LAB uses Track B - Creative Thinking;
- deploy the app;
- create a public demo;
- publish the required Community Article/story;
- submit before the official August 31, 2026 close.

The challenge scoring emphasis remains:

```text
Genie at the Core: 20 points
Track execution / Creative Thinking: 10 points
App Experience: 10 points
Total: 40 points
```

MDL-8 is complete only when the final production commit is frozen, GitHub CI is green, the production Databricks app is healthy, the 2-3 minute demo is public and verified, the Community Article is public and verified, the final social/article artwork is human-approved, the submission form is complete, and all links are validated from a clean/incognito context as far as access rules permit.

## Preconditions

Do not start MDL-8 unless:

- MDL-7 merged to `main`;
- `main` CI green;
- accepted RC commit/version recorded;
- R1-R7 green;
- 40-80 live Genie release benchmark green;
- 10-run deployed Case #042 soak green;
- manual functional acceptance green;
- all in-app artwork/audio approved;
- no known release blocker remains.

## Branch and Git workflow - mandatory

Even though this iteration is mostly submission work, use a final branch so submission-specific documentation/assets do not bypass CI.

```bash
git fetch origin --prune
git checkout main
git pull --ff-only origin main
test -z "$(git status --porcelain)"
git checkout -b MDL-8
```

Recommended commits:

```text
MDL-8: add final submission hero and public media assets
MDL-8: finalize challenge article and demo documentation
MDL-8: finalize production deployment and submission checks
MDL-8: record final submission evidence and freeze report
```

Push and PR:

```bash
git push -u origin MDL-8
gh pr create --base main --head MDL-8 --title "MDL-8 Final challenge submission" --body-file docs/iterations/MDL-8-report.md
```

No feature code should be introduced in MDL-8 except a release blocker fix. Any code fix requires regression tests and rerunning the complete relevant release gates.

## Final freeze policy

Allowed changes:

- typo/copy fixes;
- public article/video docs;
- social/hero artwork integration;
- broken-link fixes;
- deployment configuration corrections;
- accessibility/reliability release blockers;
- final secret/privacy cleanup;
- release metadata/version fixes.

Forbidden:

- new Case;
- new gameplay mechanic;
- new Experiment/Instrument family;
- new data source unrelated to release blocker;
- architecture rewrite;
- scoring changes;
- Case #042 analytical number changes;
- visual redesign of accepted screens;
- relaxing a test or benchmark threshold because of deadline pressure.

Treat August 30 as the internal feature-complete/submission preparation deadline. August 31 is buffer for submission corrections only.

## Final production branch verification

Before changing anything in MDL-8, confirm the accepted MDL-7 RC and `main` state are aligned.

Record:

```text
accepted RC tag
accepted RC commit
main HEAD
production deployment commit
```

If they differ, explain why before proceeding.

Do not accidentally overwrite the accepted production app with an untested submission-doc commit if that commit changes only repository documentation and does not need redeployment.

## Final application requirements checklist

Before recording video or publishing article, automatically verify:

### Product

- MAD DATA LAB Case Board loads;
- Case #042 card/briefing loads;
- no unreleased Case starts unless explicitly enabled;
- Start Investigation works;
- H1/H2/H3 appear;
- Genie chooses Experiment 1;
- Waterfall evidence correct;
- Genie chooses/continues snapshot investigation;
- snapshot counts/impacts correct;
- source Evidence Explorer works;
- DQ materiality correct;
- formula change ruled out;
- lineage works;
- final verdict correct;
- score/debrief work;
- music control works;
- reduced motion works;
- no hidden truth exposed;
- offline demo mode disabled.

### Automated QA

- static checks green;
- unit/component green;
- data properties green;
- G42 golden green;
- protocol tests green;
- E2E green;
- visual regression green;
- accessibility green;
- security green;
- asset preflight green;
- real SQL integration green;
- live Genie release evaluation green;
- 10-run Case #042 soak green;
- cross-Case isolation green;
- release report archived.

## Final production deployment

### Deployment workflow

Use the already-proven GitHub Actions + Databricks deployment path from MDL-7.

Prefer a protected `prod` environment with required reviewer approval.

The workflow must:

1. validate the bundle/config;
2. deploy the exact accepted source;
3. restart/run the Databricks App resource;
4. poll until RUNNING;
5. run health/config/public Case smoke;
6. run one deployed browser smoke;
7. record exact Git commit/version.

Do not manually upload a different local folder after CI has accepted a Git commit.

### Final production smoke

After deploy:

- root app 200;
- `/api/health` 200;
- app version/commit expected;
- Genie resource available;
- warehouse available;
- Case #042 public values correct;
- one live Genie guided request correct;
- no fixture/offline banner;
- approved assets load;
- no console errors;
- no secrets/debug information visible.

If this smoke fails, do not record or submit. Fix with regression coverage, rerun relevant RC gates, and redeploy.

## Demo video requirements

### Length

Target:

```text
2:30 to 2:45
```

The official challenge allows a short public demo; stay within the V3 target because it communicates the experience efficiently.

### Technical recording requirements

- 16:9;
- 1080p minimum;
- browser zoom 100%;
- no developer tools visible;
- no personal email/workspace secrets;
- no debug IDs;
- music low beneath narration;
- deliberate cursor movement;
- do not edit in a way that falsely implies a non-live analytical capability;
- waiting time may be shortened in edit if behavior is not misrepresented;
- show at least one unmistakable Genie-driven experiment-selection transition.

## Required demo narrative

The video must visibly prove the challenge value proposition, not only show a polished UI.

### 0:00-0:08 - Case universe

Show Case Board briefly.

Narration concept:

```text
MAD DATA LAB is a collection of data investigations. Every Case can require a different analytical path.
```

Open Case #042.

### 0:08-0:18 - Observation

Show:

```text
Expected 125.0M
Observed 118.2M
Deviation -6.8M
```

Narration concept:

```text
Dashboards tell us what the number is. MAD DATA LAB asks why it changed.
```

### 0:18-0:34 - Competing hypotheses

Show Dr. Genie generating/returning H1/H2/H3 from the curated evidence context.

Narration:

```text
Genie acts as the data scientist. It forms competing explanations from curated data.
```

Make initial prediction.

### 0:34-1:02 - Genie chooses Experiment 1

Visibly show:

```text
GENIE IS CHOOSING THE NEXT EXPERIMENT
```

Then component decomposition.

Show:

```text
V2 -5.9M
87% of anomaly
```

Narration:

```text
Instead of waiting for another question, Genie chooses the next analytical experiment.
```

### 1:02-1:31 - Snapshot evidence

Show:

```text
23 modified -5.2M
2 removed -0.8M
5 added +0.1M
net -5.9M
```

Narration:

```text
V2 is the strongest lead, so Genie compares its source snapshots.
```

### 1:31-1:52 - DQ false lead

Show DQ panel:

```text
5 affected rows
-0.3M overlapping impact
not additive
insufficient as primary explanation
```

Narration:

```text
There is a real data-quality warning, but Genie checks magnitude instead of declaring it the cause.
```

### 1:52-2:12 - Evidence and lineage

Open TX-004291 and trace the lineage.

Show enough path to demonstrate auditability.

Narration:

```text
The conclusion is auditable down to changed records, calculation lineage, snapshots, and source.
```

### 2:12-2:34 - Formula/reconciliation/verdict

Show:

- formula unchanged / RULED_OUT;
- source record change supported/confirmed at correct granularity;
- DQ real but not primary;
- reconciliation zero residual.

Narration:

```text
The formula is ruled out. V2 source changes reconcile to -5.9M. The evidence supports the primary explanation.
```

### 2:34-2:44 - Close

Use canonical closing line:

```text
We did not ask for an answer. We ran an investigation.
```

Narration close:

```text
That is Genie at the core.
```

## Demo truthfulness checklist

The recorded run must:

- use the production/deployed live Genie path unless Databricks platform itself is unavailable;
- not use a hidden offline fixture without visible disclosure;
- not splice together contradictory experiment outputs;
- not claim technical lineage is live Unity Catalog lineage if it is a synthetic fallback; label accurately;
- not imply DQ is fully absent; it exists but is not sufficient as primary explanation;
- not overstate `CONFIRMED` beyond the evidence granularity;
- not show a different Case truth than the deployed application.

## Community Article requirements

Create the final article draft in version control, for example:

```text
docs/submission/community-article.md
```

The published article should cover:

1. Title and hook.
2. Creative idea.
3. Target audience and learning objective.
4. Why Genie is central.
5. Architecture.
6. Data flow.
7. Hypothesis/Experiment loop.
8. Value lineage versus technical lineage.
9. Deterministic synthetic Case generation.
10. Controlled adaptive Instruments.
11. Automated testing approach.
12. What users can ask Genie.
13. Demo link.
14. Lessons learned.
15. Limitations and safe fallbacks.
16. Repository/app link if challenge rules allow/require it.

## Required challenge framing in article

Be explicit:

### Track

```text
Track B - Creative Thinking
```

### One-sentence pitch

Use the V3 concept:

```text
MAD DATA LAB turns an unexpected metric into a reproducible scientific investigation: Dr. Genie forms hypotheses, chooses the next experiment, queries trusted evidence, selects the right analytical instrument, updates its beliefs, and explains what the data supports.
```

### Genie centrality

Explain concretely that Genie:

- forms competing hypotheses;
- chooses the next Experiment;
- queries curated evidence;
- selects an Instrument from a closed allowlist;
- updates epistemic status;
- synthesizes the conclusion.

Also explain what the app, not Genie, controls:

- state machine;
- safe rendering;
- Experiment/Instrument validation;
- scoring;
- hidden truth;
- deterministic SQL fallback;
- security and release gates.

This demonstrates both creativity and engineering rigor.

### Hidden truth / scientific integrity

Explain that `CASE_TRUTH` exists only as a private backend/test oracle and is not available to Genie.

### Safe fallback

Explain accurately:

- deterministic SQL fallback can execute after Genie has already chosen a valid Experiment but a query attachment fails;
- offline fixture mode is a catastrophic-outage/development tool, not normal challenge behavior.

### Synthetic data

State clearly that Case #042 uses synthetic data and does not represent real company/client financial data.

## Architecture diagram

Create a controlled architecture diagram in HTML/SVG or a diagram source that is deterministic and readable. It should show:

```text
Browser / React Game
  -> FastAPI application
      -> Case/session/state/scoring
      -> Genie orchestration + protocol validator
      -> Genie Agent resource
          -> curated Unity Catalog views
      -> trusted SQL adapter
          -> curated views/evidence
      -> private CASE_TRUTH validator (backend only)
```

Do not create a diagram that visually implies Genie can directly access private truth.

Export a high-resolution PNG/SVG for article use if needed.

## Final artwork checkpoint - mandatory before submission

### MDL8-A15 - Social / article hero

Use the approved Dr. Genie master/pose identity.

Prompt intent from V3:

```text
Cinematic social-card illustration for MAD DATA LAB. Approved Dr. Genie stands on the right, pointing toward a large glowing analytical machine on the left where one bright metric orb splits into hypothesis paths and evidence traces. Dark navy lab, cyan analytical glow, violet evidence accents, restrained coral anomaly energy. Clear negative space upper-left for the real title added later in HTML/design tooling. Premium, memorable, professional, playful scientific energy. No readable text, numbers, logos, or watermark.
```

Target:

```text
1200 x 630
```

The actual `MAD DATA LAB` title/tagline should be added as real typography outside the generated image if the publishing surface requires text baked into a final export.

### Demo thumbnail / cover crop

Create a derived thumbnail/crop from approved production art, or compose a controlled cover using:

- approved MDL8-A15 hero;
- real HTML/design-tool wordmark;
- optional short tagline;
- no AI-generated readable title text.

Do not generate a new unapproved fantasy/pixel Genie cover merely for social media.

### Automated preflight

- exact 1200x630 hero dimensions;
- image decode;
- file-size budget;
- no generated readable text/logos/watermark;
- Dr. Genie identity consistent;
- title safe area works;
- thumbnail safe at common small sizes;
- source/production files named in manifest;
- SHA-256 recorded.

### Human approval gate

Create `docs/approvals/MDL-8-art.md` with `PENDING` status.

Human must approve:

- MDL8-A15 social/article hero;
- final demo thumbnail/cover composition;
- final architecture diagram readability/accuracy;
- final app screenshots selected for article.

Codex cannot self-approve.

No submission is allowed while MDL-8 artwork approval is pending.

## Final screenshots

Capture clean production screenshots at 1440x900 or 1600x900:

- Case Board;
- Case #042 briefing;
- Genie selecting an Experiment;
- Waterfall;
- Snapshot Reactor;
- DQ panel;
- Evidence Microscope / TX-004291;
- Lineage;
- Scientific Verdict / reconciliation;
- Debrief.

Screenshots must:

- contain no personal workspace identifiers;
- contain no secrets/debug IDs;
- represent current production build;
- use approved art;
- not show stale fixture banners;
- not show unsupported claims.

## Public link validation

Create a final checklist script/document that verifies all submission destinations.

At minimum:

```text
Databricks App link
Community Article link
Demo video link
Repository link if included
```

Where programmatic access is possible, check HTTP status. Where login/auth makes a public check impossible, manually validate from incognito/logged-out context as appropriate.

The video must be publicly accessible according to challenge rules, not restricted to a private account group.

## Final GitHub CI gate

Run all mandatory CI after the final MDL-8 commit.

Required:

- no code/test regressions;
- asset preflight includes final hero;
- article Markdown link checker if implemented;
- secret scan includes docs/screenshots metadata paths;
- production build still green.

Use:

```bash
gh run list --branch MDL-8 --limit 30
gh pr checks --watch
```

If a docs-only commit unexpectedly breaks CI, fix the real issue; do not bypass required checks.

## Final release gate after any code change

If MDL-8 changes application code, dependencies, data, prompt/configuration, or production assets used by the app:

- rerun all affected MDL-7 release gates;
- redeploy;
- rerun deployed smoke;
- rerun full ten-run soak if the change can affect Genie/data/state/conclusion behavior;
- repeat manual acceptance for the affected path.

Do not assume a "small" prompt or data change cannot affect the live Genie path.

## Merge gate

Merge `MDL-8` only when:

- final CI green;
- final submission artwork human-approved;
- production deployment/smoke green;
- article draft complete;
- demo recording complete and reviewed;
- public links verified;
- no release blocker open.

After merge:

1. verify `main` CI green;
2. if the app needs the merge commit, deploy it through GitHub Actions;
3. verify production commit/version;
4. create final immutable tag if repository policy permits, for example:

```text
submission-2026
```

Do not move the final tag after submission.

## Final manual submission acceptance

Perform one short final acceptance against the exact production URL, primarily to catch publication/deployment issues rather than rediscover functional logic.

Check:

- MAD DATA LAB loads;
- approved hero/brand visual present where expected;
- Case #042 playable;
- live Genie clearly central;
- no offline fixture banner;
- final conclusion readable with sound off;
- music can be muted;
- no debug/secret data;
- article/video links resolve;
- video is correct final version;
- article references correct app/demo links;
- track is stated as Creative Thinking;
- no stale screenshot from the obsolete fantasy-genie/board design.

## Submission form checklist

Before pressing final submit, confirm:

- correct challenge selected;
- correct track: Creative Thinking;
- app link entered;
- article link entered;
- demo video link entered;
- any requested registration/contact fields completed;
- project title exactly `MAD DATA LAB`;
- links open successfully;
- submission completed before the internal deadline, leaving August 31 as buffer.

Save a non-sensitive confirmation reference/screenshot if appropriate.

## Final submission report

Create `docs/iterations/MDL-8-report.md` containing:

- branch/PR/base/final/merge commit SHAs;
- final release tag;
- final GitHub CI run ID;
- final Databricks deployment/version;
- final release report path;
- MDL-7 RC/soak reference;
- final art approval record;
- demo video filename/link status;
- Community Article link/status;
- app link/status;
- submission timestamp/status;
- any last-minute blocker fixes and regression tests;
- final known limitations disclosed in article;
- final rollback reference.

Do not store personal contact details or credentials in the report.

## Definition of Done - MDL-8

- [ ] Branch `MDL-8` created from green accepted MDL-7 `main`.
- [ ] No new non-blocker feature development introduced.
- [ ] Final production app remains on Databricks Free Edition.
- [ ] Genie Agent is connected and visibly powers the main investigation.
- [ ] Track B - Creative Thinking stated consistently.
- [ ] Final production deploy is green.
- [ ] Final production smoke is green.
- [ ] Exact production Git commit/version recorded.
- [ ] All application automated gates remain green.
- [ ] GitHub CI green on `MDL-8`.
- [ ] Final `main` CI green after merge.
- [ ] Demo video is 2-3 minutes, 16:9, 1080p+, and publicly accessible.
- [ ] Video visibly shows Genie forming/maintaining hypotheses, choosing an Experiment, trusted evidence, a ruled-out/insufficient competing signal, source/lineage evidence, and Scientific Verdict.
- [ ] Video does not misrepresent fixture mode as live Genie.
- [ ] Community Article covers idea, audience, architecture/data flow, Genie centrality, user questions, testing, lessons, and limitations.
- [ ] Article states synthetic data and hidden-truth isolation accurately.
- [ ] Architecture diagram accurately isolates private truth from Genie.
- [ ] MDL8-A15 social/article hero generated and preflighted.
- [ ] Final demo thumbnail/cover prepared from approved assets.
- [ ] Human explicitly approves final hero, thumbnail, architecture diagram, and selected screenshots.
- [ ] No obsolete fantasy-genie/board artwork appears in submission materials.
- [ ] App/article/video links verified.
- [ ] Submission form complete with correct track and links.
- [ ] Submission completed before internal deadline.
- [ ] Final immutable release tag recorded.
- [ ] Final MDL-8 report complete.

When every checkbox is true, MAD DATA LAB is ready-to-submit and the implementation roadmap is closed.
