# MDL-5 - Analytical Instruments, Evidence Explorer, Visual System, Controlled Rendering, and Production Artwork

## Purpose

This iteration makes the Case #042 investigation visually and analytically legible. It replaces the current prototype use of `board.png` as a dim decorative board with real controlled HTML/SVG analytical Instruments backed by validated API data.

The goal is not merely visual polish. The V3 product model defines Instruments as controlled UI components selected by Genie from a closed registry. MDL-5 implements those components and ensures every analytical claim is auditable through text, values, evidence records, and lineage.

This iteration is finished only when:

- every Case #042 analytical Experiment has a production Instrument;
- no generated image contains functional UI, labels, chart numbers, or fake buttons;
- the Evidence Explorer supports record-level auditability;
- the lineage and reconciliation views are deterministic and data-backed;
- visual regression and accessibility coverage exist for every primary screen;
- all required instrument artwork has passed technical preflight and explicit human approval;
- GitHub CI and Databricks staging deployment are green.

## Preconditions

Do not start MDL-5 unless:

- MDL-4 merged to `main`;
- `main` CI green;
- full fake-Genie Case #042 flow reaches Debrief;
- server-authoritative score/verdict work;
- Case #042 curated evidence and live Genie path are still green;
- MDL-4 artwork approval recorded.

## Branch and Git workflow - mandatory

```bash
git fetch origin --prune
git checkout main
git pull --ff-only origin main
test -z "$(git status --porcelain)"
git checkout -b MDL-5
```

Recommended commits:

```text
MDL-5: implement semantic visual design tokens and shell layout
MDL-5: add Case 042 analytical instrument components
MDL-5: add Evidence Explorer and deterministic lineage
MDL-5: add visual accessibility and screenshot regression suite
MDL-5: integrate approved instrument artwork
MDL-5: add iteration completion report
```

Push and PR:

```bash
git push -u origin MDL-5
gh pr create --base main --head MDL-5 --title "MDL-5 Instruments evidence and visual system" --body-file docs/iterations/MDL-5-report.md
```

## Remove obsolete prototype art/UI coupling

The existing prototype assets must no longer be treated as functional UI screenshots.

Specifically:

- remove `board.png` from production UI if it contains Action Points, Round, Caffeine, Move, Test Hypothesis, Collect Evidence, Analyze Data, inventory cells, or other controls not implemented by the actual game;
- remove any CSS that uses the board image as a large blurred/fixed functional backdrop;
- remove the `evidence-polish.css` pseudo-element that injects DQ conclusion/evidence copy;
- remove the fantasy-genie emoji avatar;
- remove hardcoded chart/evidence content from static CSS;
- do not generate new images containing UI buttons, labels, charts, metric values, Case numbers, or important words.

Functional content must be HTML/SVG/React and therefore testable, accessible, responsive, and data-driven.

## Visual design system

### Create semantic tokens

Create `frontend/src/styles/tokens.css` with semantic names. Do not use brand behavior names like `--lime` or `--pink` as the primary system.

At minimum:

```text
--background-deep
--surface-1
--surface-2
--text-primary
--text-secondary
--border-subtle
--accent-science
--accent-energy
--accent-evidence
--status-confirmed
--status-supported
--status-possible
--status-ruled-out
--focus-ring
```

Color intent:

```text
science / main interaction: cyan/teal
energy/anomaly: restrained coral/red
evidence: violet
confirmed: green
possible/warning: amber
ruled out: desaturated gray/red
```

Do not communicate status by color alone.

### Typography

Use a clean freely distributable sans-serif/system sans for:

- body text;
- controls;
- evidence tables;
- Dr. Genie messages;
- hypothesis copy;
- numeric values.

Use tabular numerals for analytical values.

If a decorative display treatment is retained for the wordmark or tiny flavor labels, keep it separate from body/UI typography and ensure it does not introduce an unreliable external runtime dependency.

### Shape language

Use:

- 10-16 px panel radius;
- thin illuminated borders;
- restrained mechanical frame accents;
- clear focus states;
- no excessive glassmorphism;
- no huge decorative panels that consume interaction area.

## Global Investigation layout

Implement the V3 frame:

```text
+----------------------------------------------------------+
| MAD DATA LAB  Case #042 - The Missing EUR 6.8M  Audio   |
+----------------------------------------------------------+
| Main analytical stage                 Dr. Genie panel    |
|                                                          |
+----------------------------------------------------------+
| Hypotheses / evidence progress / primary action          |
+----------------------------------------------------------+
```

Requirements:

- desktop-first 16:9 recording viewport;
- works at 1600x900, 1440x900, and 1280x720 without critical clipping;
- mobile/basic stacking at 390x844;
- remove current `min-width: 1100px` behavior;
- decoration may not consume roughly 30%+ of the screen in a way that reduces playability;
- stage content remains readable with sound off and without narration.

## Instrument rendering architecture

Create a single registry-driven render boundary such as:

```text
InstrumentRenderer
  receives validated InstrumentModel
  chooses only registered React component
  never evals arbitrary model output
```

Do not route by Case number.

Do not let Genie return React component names that are imported dynamically from arbitrary strings.

Suggested registry mapping:

```ts
const instrumentComponents = {
  KPI_DELTA: KpiDelta,
  WATERFALL: Waterfall,
  SNAPSHOT_DIFF: SnapshotDiff,
  EVIDENCE_TABLE: EvidenceTable,
  DQ_PANEL: DqPanel,
  FORMULA_DIFF: FormulaDiff,
  LINEAGE_GRAPH: LineageGraph,
  RECONCILIATION: Reconciliation,
  // future registered instruments
};
```

Validate server payload schema before rendering.

## Instrument 1 - KPI Delta / Case observation

Input contract:

```json
{
  "expected": 125.0,
  "observed": 118.2,
  "deviation": -6.8,
  "unit": "EUR_MILLIONS"
}
```

UI must always show all three values with explicit labels.

Rules:

- do not rely on red/green alone;
- preserve sign;
- use consistent EUR/M formatting;
- provide accessible text equivalent by default because the component is textual.

## Instrument 2 - Deviation Decomposer / WATERFALL

Input:

```json
{
  "expected": 125.0,
  "components": [
    {"id": "V1", "delta": -1.2},
    {"id": "V2", "delta": -5.9},
    {"id": "V3", "delta": 0.3},
    {"id": "V4", "delta": 0.0}
  ],
  "observed": 118.2
}
```

### Validation

Before render:

```text
expected + sum(delta) = observed within 0.01
```

If invalid, render an evidence validation error; do not render a misleading chart.

### Display behavior

- preserve formula order V1, V2, V3, V4;
- visually emphasize V2 as dominant absolute delta without hiding exact values;
- show exact values in an adjacent accessible table;
- show computed `87% of absolute deviation` from data, not static copy;
- keyboard focus can reach the textual summary even if individual SVG bars are not independently interactive.

## Instrument 3 - Snapshot Reactor / SNAPSHOT_DIFF

Input:

```json
{
  "groups": [
    {"change_type": "MODIFIED", "count": 23, "impact": -5.2},
    {"change_type": "REMOVED", "count": 2, "impact": -0.8},
    {"change_type": "ADDED", "count": 5, "impact": 0.1}
  ],
  "net_impact": -5.9
}
```

### Validation

```text
sum(group impacts) = net_impact
```

### Display

Show exact count and impact for each change type plus net.

Avoid animations that imply records are physically moving if reduced motion is enabled.

Provide an action to inspect V2 evidence records.

## Instrument 4 - Evidence Microscope / EVIDENCE_TABLE

Columns for Case #042:

```text
Business key
Change type
Previous amount
Current amount
Impact
Previous snapshot
Current snapshot
Source
```

Default sort:

```text
ABS(impact) DESC, business_key
```

Requirements:

- TX-004291 must appear from API data;
- previous = 4.2M, current = 0.0M, impact = -4.2M;
- table supports keyboard navigation with normal semantic table markup;
- table headers properly associated;
- business-key search;
- change-type filter;
- component filter;
- minimum absolute impact filter if implemented;
- limit/cursor paging via server;
- no edit/delete controls;
- max 100 rows per request.

### Record detail

Show:

```text
Business key
Component
Change type
Previous amount
Current amount
Impact
Previous snapshot
Current snapshot
Source table
Source column
```

The record-detail panel must be driven by selected row/evidence ID, not by the hidden truth fixture.

## Instrument 5 - DQ Contamination Scanner / DQ_PANEL

Input must include:

```text
rule name
severity
affected rows
estimated impact
impact share of deviation
overlap flag
current relevant hypothesis status
```

For Case #042 display:

```text
DUPLICATE_BUSINESS_KEY
Severity MEDIUM
Affected rows 5
Estimated overlapping impact -0.30M
```

When overlap is true, show exact wording or equivalent meaning:

```text
Estimated impact overlaps other evidence and is not additive.
```

Also explain that the magnitude is insufficient to explain the -6.8M anomaly by itself.

Do not label the DQ issue itself `RULED_OUT`; distinguish a real issue from the rejected claim that it is the primary cause.

## Instrument 6 - Formula Validator / FORMULA_DIFF

Show:

```text
previous formula ID
current formula ID
previous normalized hash
current normalized hash
normalized expression or display-safe expression
changed = false
```

Case #042 expression:

```text
V1 + V2 - V3 + V4
```

Requirements:

- same ID/hash must be visibly comparable;
- do not treat formatting-only differences as semantic changes;
- if formula evidence schema is invalid/missing, do not silently mark `RULED_OUT`;
- textual summary must say the formula did not change only after validated evidence.

## Instrument 7 - Lineage Telescope / LINEAGE_GRAPH

Node classes:

```text
METRIC
COMPONENT
SOURCE_COLUMN
SNAPSHOT
RECORD_GROUP
TECHNICAL_OBJECT
```

Use deterministic left-to-right layout. Do not use a force-directed graph for the challenge MVP.

Minimum Case #042 path:

```text
Capital Available
  -> V2 calculation
  -> finance_reporting_source.amount
  -> snapshot(s)
  -> changed V2 records / evidence group
  -> technical object when available
```

Requirements:

- stable node order across renders/tests;
- graph never becomes the only representation; include textual path/list;
- node details are display-safe;
- no private truth node;
- line/edge color is not the only encoding of relationship type;
- can render with synthetic technical-lineage fallback if Unity Catalog technical lineage is unavailable, but must label provenance honestly.

## Instrument 8 - Reconciliation

Show:

```text
Total observed deviation      -6.8M
V2 source changes             -5.9M
Other component effects       -0.9M
Unreconciled                   0.0M
```

Validate before render:

```text
explained + unreconciled = total within tolerance
```

Do not include DQ -0.3M as an extra additive row because it overlaps V2.

For future Level 3 Cases, component should support multiple causal contributions without assuming one primary row.

## Evidence Explorer page

Implement the two-column desktop structure:

```text
left: filters + evidence list/table
right: selected evidence details + lineage/comparison
```

### Drill path

Support:

```text
Scientific Verdict
  -> Hypothesis
  -> Experiment
  -> Evidence group
  -> Record
  -> Calculation/value lineage
  -> Technical lineage
```

### Query/state behavior

- filter UI state stays client-side;
- query parameters validated server-side;
- changing filter cancels/stales previous request safely;
- no per-row N+1 requests;
- selected record cleared or updated safely when filters change;
- empty state explicit;
- backend errors preserve previous evidence where reasonable and show retry.

### Reward tracking

When player inspects the Case's high-value evidence item or required lineage/comparison, send a server event or idempotent API call so scoring can award the appropriate points exactly once.

Do not trust a client boolean such as `evidence_inspected=true` without validating the referenced evidence item belongs to the active Case/session.

## Dr. Genie panel

Replace any fantasy-genie emoji with approved Dr. Genie assets.

Panel should support:

- current short scientist line;
- selected pose based on context, using only approved assets;
- visible live/degraded evidence source label if appropriate;
- optional Ask Dr. Genie drawer;
- no chain-of-thought display.

Active play dialogue lines should stay at most two short sentences.

## Motion

Implement the V3 motion philosophy:

- button feedback 100-160ms;
- card emphasis 180-240ms;
- panel transition 220-320ms;
- experiment selection reveal 700-1200ms;
- chart entrance 500-900ms;
- conclusion reveal 700-1100ms.

Never delay the user more than 1.5 seconds after data is available solely for animation.

Reduced-motion mode:

- no scanning sweeps;
- no pulse loops;
- opacity transitions under 150ms;
- charts appear immediately;
- no parallax.

## Accessibility requirements

Every chart/Instrument must have:

- explicit labels;
- exact values in text;
- non-color encoding;
- a textual evidence summary;
- keyboard-accessible surrounding controls;
- semantic table where tabular data exists.

All controls need accessible names.

Status badges must display words such as `SUPPORTED` and not depend on color.

## Responsive requirements

Target viewports:

```text
1600x900
1440x900
1280x720
390x844
```

At 1280x720:

- no critical action clipped;
- Case title understandable;
- primary Instrument visible without horizontal scrolling;
- Dr. Genie panel may compact but must not hide essential evidence;
- footer action remains reachable.

At mobile width basic operation must remain possible, although the challenge demo is desktop-first.

## Tests required to close MDL-5

### Instrument component tests

Implement/complete:

- FE-001 KPI all three values;
- FE-002 negative deviation sign;
- FE-004 status text not color-only;
- FE-005 Waterfall dominant V2 emphasis;
- FE-006 Waterfall accessible table;
- FE-007 Snapshot counts/impact;
- FE-008 DQ overlap warning;
- FE-009 deterministic lineage ordering;
- FE-010 evidence table sort;
- FE-011 empty evidence state;
- FE-012 loading;
- FE-013 retryable error UI;
- FE-014 non-retryable error UI;
- FE-019 score only server response;
- FE-020 primary action disabled during request;
- FE-022 Dr. Genie image alt/decorative semantics;
- FE-023 focus visible;
- FE-025 no model HTML rendering;
- FE-030 generic Instrument model rendering.

Add explicit schema/validation tests for:

- invalid Waterfall reconciliation -> error;
- invalid Snapshot net -> error;
- invalid Reconciliation -> error;
- DQ overlap true -> non-additive text;
- formula unchanged -> correct status summary;
- lineage private node forbidden;
- no hardcoded `TX-004291` detail if API returns another record in a test fixture.

### Evidence API/E2E

Run:

- E2E-006 optional record inspection behavior;
- E2E-007 filter MODIFIED;
- E2E-008 search TX-004291;
- E2E-019 reconciliation failure blocks false conclusion;
- E2E-022 1440x900 no overflow;
- E2E-023 1280x720 no critical clipping;
- E2E-024 keyboard-only primary flow at least through first Instrument;
- E2E-025 benign free-form chat if UI is integrated;
- E2E-026 hidden-truth chat attempt safe;
- E2E-MC-009 generic Experiment Result renders several Instrument families without Case-specific routing.

### Visual regression

Establish stable screenshot baselines for:

- Case Board;
- Case Briefing;
- Hypothesis Board;
- Experiment Selecting;
- Waterfall result;
- Snapshot result;
- Evidence Explorer;
- DQ panel;
- Formula panel;
- Lineage;
- Reconciliation/Verdict shell;
- Debrief;
- error state;
- reduced-motion variant where visually meaningful.

Viewports:

```text
1600x900
1440x900
1280x720
390x844
```

Add checks equivalent to VR-001 through VR-020 from the V3 catalog.

Do not accept a broad screenshot threshold that allows layout breakage to pass.

### Accessibility automation

Integrate axe-core with Playwright and implement AX-001 through at least AX-015 for the currently available screens.

Required closure threshold:

```text
0 serious violations
0 critical violations
```

Any known moderate issue intentionally deferred must be documented, but critical/serious blocks MDL-5.

### Performance sanity

Measure component rendering for demo-sized data:

- Waterfall under target;
- Evidence table 100 rows no obvious stall;
- no evidence N+1 network pattern.

Full performance hardening remains MDL-6.

## Artwork checkpoint - mandatory before iteration closure

This iteration produces the main analytical Instrument illustrations. These are decorative framing assets only; real data/UI is overlaid in HTML/SVG.

All assets share the approved global art direction:

```text
Premium retro-futurist data science laboratory, sophisticated enterprise analytics meets playful experimentation, dark navy, luminous cyan data traces, restrained coral anomaly energy, subtle violet evidence glow, precision machinery, polished stylized 3D, generous negative space, no readable text, numbers, logos, watermarks, fantasy genie imagery, or fake functional controls.
```

### MDL5-A08 - Deviation Decomposer illustration

Target: 1600x900.

Prompt intent:

```text
A fictional scientific analytics machine that separates one aggregate data beam into four component channels, with the second channel visibly dominant. Transparent precision channels, cyan data particles, subtle coral negative-flow indication, violet analytical glow. Leave a large clean central rectangular region for the real SVG Waterfall. No text, numbers, labels, or controls.
```

### MDL5-A09 - Snapshot Reactor illustration

Target: 1600x900.

Prompt intent:

```text
Two transparent data cylinders representing previous/current states feeding a central comparison chamber. Abstract record tiles move between them; some modified, a few removed, a few added. Dark navy, cyan/violet glow, restrained coral discrepancy accents. Leave a large empty central panel for real HTML summary. No text, numbers, labels, buttons, or watermark.
```

### MDL5-A10 - Data Microscope illustration

Target: 1600x900.

Prompt intent:

```text
High-tech analytical microscope inspecting an abstract rectangular data-record tile. Holographic lens reveals nested fields and lineage paths. Dark navy lab bench, cyan scanning beam, violet evidence markers. Keep the right half visually quiet for the real record detail panel. No biological sample, readable text, numbers, logo, or watermark.
```

### MDL5-A11 - Lineage Telescope illustration

Target: 1600x900.

Prompt intent:

```text
Futuristic analytical telescope looking inward through layered data lineage: metric orb -> calculation nodes -> source-table shapes -> snapshot layers -> record tiles, orderly depth perspective, cyan lines, violet evidence highlights, restrained coral accent. Leave open space for the actual interactive deterministic SVG lineage graph. No text, numbers, logos, watermark.
```

### MDL5-A12 - DQ Contamination Scanner illustration

Target: 1400x800.

Prompt intent:

```text
Data-quality contamination scanner. Abstract duplicate-record tiles pass under a scanning arch; five small warning markers detected, but instrument remains calm rather than catastrophic. Amber warning light, cyan baseline data flow, dark navy machinery, empty real-text panel. Visual meaning: real warning, limited magnitude. No text, numbers, logos, watermark.
```

### MDL5-A13 - Conclusion chamber illustration

Target: 1920x1080.

Prompt intent:

```text
Final scientific conclusion chamber. Three hypothesis vessels converge into one evidence core. One path bright/stable, one mechanically shuttered/dim, one amber path weak but unresolved. Circular reconciliation ring around central core. Restrained triumphant mood. Large foreground space for real verdict content. No text, numbers, people, logos, or watermark.
```

### Automated asset preflight

For every asset:

- dimensions correct;
- image decodes;
- production file size under internal budget;
- no unsupported color profile;
- no accidental portrait rotation;
- no readable generated text/numbers;
- no fake buttons/menus/control labels;
- filename matches manifest;
- SHA-256 recorded;
- WebP/PNG production derivative;
- large source working asset excluded from deployed package if over budget.

Create a contact sheet or HTML review page showing each asset at actual in-app placement plus a standalone thumbnail.

### Human approval gate

Create `docs/approvals/MDL-5-art.md` listing all six assets with independent status.

Human must explicitly approve each asset. One rejected asset keeps the whole MDL-5 art gate open.

Human review checklist:

- visual style consistent with MDL-1 master direction;
- artwork supports, never competes with, actual data;
- negative space matches real overlay placement;
- no fake UI;
- no accidentally legible AI text;
- no fantasy-genie imagery;
- the app remains professional enough for enterprise analytics;
- each Instrument is visually distinct but belongs to the same laboratory.

Codex cannot self-approve or substitute unreviewed stock imagery.

## Asset packaging

Update `assets/art_source_manifest.yaml` with every approved production asset.

Add CI packaging checks so:

- no individual app file exceeds Databricks per-file limit;
- images remain within internal target (normally under 1.5MB each where practical);
- obsolete `board.png` and fantasy-genie cover are not referenced by production code;
- approved source assets are not accidentally duplicated in both `frontend/assets` and public roots unless build requires it.

## GitHub CI requirements

Extend CI with:

- frontend component tests;
- full critical Playwright fixture flow;
- screenshot visual regression;
- axe accessibility suite;
- asset manifest/preflight;
- build-size summary;
- static scan that obsolete assets are not imported/referenced;
- no external runtime font dependency unless explicitly approved and tested offline.

CI must install fonts/assets deterministically so screenshot diffs are stable.

If anti-aliasing variance occurs, solve through deterministic environment or targeted thresholds, not an excessively permissive global diff threshold.

## Databricks deployment gate

Deploy MDL-5 to staging through GitHub Actions.

Automated deployed browser smoke must capture screenshots of at least:

```text
Case Board
Case Briefing
Hypothesis Board
Component Decomposition
Snapshot Diff
Evidence Explorer with TX-004291
DQ panel
Formula validation
Lineage
Verdict/Reconciliation
Debrief
```

Where live Genie cost makes a full deployed run impractical on every branch push, run exactly one full deployed flow after branch CI is green and store the result as release evidence.

Verify:

- no critical asset 404;
- no horizontal overflow at 1280x720;
- all visible analytical numbers match API data;
- no obsolete board artwork or fantasy-genie emoji appears;
- approved asset hashes match deployed build artifact if practical.

## Manual deployment inspection

After automation passes, human performs subjective review at 1440x900 and 1280x720:

- data is visually dominant;
- the first anomaly is understandable within about 10 seconds;
- Dr. Genie panel does not steal too much space;
- Instrument framing is attractive but not misleading;
- DQ panel clearly communicates real warning / limited materiality;
- formula panel clearly communicates unchanged logic;
- lineage is legible;
- evidence table is readable;
- no clickable-looking generated decoration;
- approved artwork matches actual final crop/use;
- conclusion remains understandable with sound muted.

A discovered functional bug requires an automated regression test.

## GitHub and merge closure

Run:

```bash
gh run list --branch MDL-5 --limit 20
gh pr checks --watch
```

Do not merge until:

- all component/E2E/visual/axe/asset checks green;
- artwork explicitly human-approved;
- staging deployed smoke green;
- human visual/runtime inspection accepted.

After merge, verify `main` CI and deployment.

## Required iteration report

Create `docs/iterations/MDL-5-report.md` with:

- branch/PR/commit references;
- implemented Instrument registry mapping;
- screenshot baseline list and hashes/paths;
- axe summary;
- evidence explorer API/UI summary;
- visual performance notes;
- asset IDs/hashes/approval record;
- obsolete asset removal confirmation;
- deployed screenshot/smoke reference;
- known deferred hardening items for MDL-6.

## Definition of Done - MDL-5

- [ ] Branch `MDL-5` created from green merged MDL-4 `main`.
- [ ] Obsolete `board.png` functional-UI representation removed from production experience.
- [ ] Fantasy-genie emoji removed.
- [ ] CSS-generated DQ evidence/conclusion removed.
- [ ] Semantic visual tokens implemented.
- [ ] Clean UI/body typography with tabular numerals implemented.
- [ ] Responsive Investigation shell works at required viewports.
- [ ] `KPI_DELTA` implemented and tested.
- [ ] `WATERFALL` implemented, validates reconciliation, and has textual equivalent.
- [ ] `SNAPSHOT_DIFF` implemented and validates net impact.
- [ ] `EVIDENCE_TABLE` implemented with filters/search/pagination and TX-004291 data.
- [ ] `DQ_PANEL` implemented with overlap/non-additive wording.
- [ ] `FORMULA_DIFF` implemented with unchanged ID/hash evidence.
- [ ] `LINEAGE_GRAPH` deterministic and has textual path.
- [ ] `RECONCILIATION` shows -6.8 / -5.9 / -0.9 / 0.0 correctly.
- [ ] Evidence Explorer drill path works.
- [ ] Instrument rendering is registry-controlled, not arbitrary model code.
- [ ] Visual regression suite covers all main screens/viewports.
- [ ] Axe shows zero serious/critical violations on covered screens.
- [ ] GitHub CI green.
- [ ] Databricks staging deploy green.
- [ ] Deployed browser smoke/screenshots green.
- [ ] MDL5-A08 through MDL5-A13 generated and technically preflighted.
- [ ] Human explicitly approves every MDL-5 artwork asset.
- [ ] Obsolete unapproved art is not referenced by production build.
- [ ] Branch pushed and PR merged only after all gates.
- [ ] `main` CI green after merge.
- [ ] Iteration report complete.

If any item is false, do not start MDL-6.
