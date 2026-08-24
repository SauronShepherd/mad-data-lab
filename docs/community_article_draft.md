# MAD DATA LAB — community article draft

## The idea

MAD DATA LAB turns an unexplained metric into a reproducible investigation.
Players predict and inspect; Dr. Genie forms competing hypotheses, selects the
next analytical Experiment, queries curated evidence, chooses an instrument, and
updates epistemic status.

## Why Genie is central

The primary flow cannot continue without Genie’s experiment-selection decision.
The application validates that decision against a closed registry and falls back
to verified fixture evidence only when the live service is unavailable.

## Databricks architecture

The Genie Space sees curated public evidence tables and views only. A FastAPI
session service owns transitions, scoring, progression, and the append-only
investigation log. Case truth is private application data used for scoring and
automated validation, never a Genie source.

## Demo questions

- Which component explains most of the deviation?
- What changed in V2 between snapshots?
- Which source record has the largest impact?
- Did the formula change?
- Is the data-quality warning large enough to explain the anomaly?

## Testing and lessons

The repository includes deterministic generator/property checks, protocol and
security contracts, seven-case fixture E2E, visual/static and runtime axe
checks, Docker smoke, live SQL/Genie gates, authenticated deployment smoke, and
a ten-run deployed Case #042 soak. The most important lesson is to keep hidden
truth separate from curated evidence and to validate every model-selected action
before it changes state.

## Limitations

Secondary Cases use deterministic fixture contracts and review-mode E2E; the
production Genie Space is currently curated for Case #042. Free-form chat is
secondary, and live Genie responses can fall back to verified evidence. Video,
article publication, and contest registration links must be completed outside
the repository.
