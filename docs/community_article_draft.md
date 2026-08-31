# MAD DATA LAB — Community Article Draft

## The missing €6.8M

MAD DATA LAB turns an unexpected metric into a reproducible scientific investigation. In Case #042, expected revenue is €125.0M, observed revenue is €118.2M, and the deviation is -€6.8M.

The player begins with competing hypotheses: source values changed, the formula changed, or a data-quality issue explains the anomaly. Dr. Genie is central to the loop: it selects the next legal Experiment from the trusted catalog, explains why that experiment is useful, and updates the investigation as evidence arrives.

## Evidence, not an answer

Component decomposition identifies V2 at -€5.9M / 87%. Snapshot comparison reconciles 23 modified, 2 removed, and 5 added records. The representative record `TX-004291` changes from €4.2M to €0.0M, an impact of -€4.2M. A DQ warning contributes -€0.3M but overlaps the primary signal, so it is a tempting red herring rather than an additive cause. Formula validation shows the formula is unchanged. The final reconciliation residual is €0.0M.

## Trust boundary and engineering

The browser receives curated evidence and public investigation state. Private Case truth and scoring-oracle internals remain server-side. The application has deterministic local fixture behavior for reproducible development and explicit failure/recovery behavior when live Genie is unavailable; fixture output is not presented as live Genie success.

The repository includes contract validation, hidden-truth isolation tests, security and accessibility gates, responsive browser coverage, deterministic data checks, visual/asset preflight, and a local release-candidate command. The current acceptance evidence is stored under `release-report/` and must be regenerated after source changes.

## Limitations and next actions

This draft does not invent a public app URL, article URL, video URL, CI result, deployed identity, live Genie result, or artwork approval. Those remain explicit owner/external actions in [Known limitations](KNOWN_LIMITATIONS.md) and [Testing and release](TESTING_AND_RELEASE.md).
