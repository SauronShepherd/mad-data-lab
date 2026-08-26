# MDL-3 iteration report

status: IN_PROGRESS
implementation_sha: NOT_FROZEN
runtime_digest: 4974aae717af547977175723fdfbe4e0642cbadb279f1cfa1604186574bce19e
genie_contract_digest: 8e78b74e39bd9cd4936a2cc5b8b950cc3ebecee9b0a94890313b0277dc1ab9aa
genie_live_config_sha256: ad8418446a24e0d1e17768ff981141027f75f9cfea4c183b030e17e6bedd8fef
mdl2_data_contract_digest: 41f8e307c2420eb4b9e2627575572f32a0791e39e6ddedea5ed5199416cad471
benchmark_batch_id: mdl3-accepted-baseline

## Implemented local evidence

- Strict Pydantic protocol and exact control-object extraction: `backend/genie/protocol.py`.
- One-repair lifecycle and safe protocol/query failure separation: `backend/genie/lifecycle.py`.
- Pending first-Experiment decision persistence/consumption: `backend/genie/decisions.py`, `server/main.py`.
- Closed Experiment registry and permanent instructions: `genie/registry.json`, `genie/instructions.md`.
- Frozen 30-attempt corpus: `genie/benchmarks/mdl3-live.yaml`.
- Local contract gate: `release-report/MDL-3/contract-validation.json`.
- Local fixture benchmark JSON/JUnit: `release-report/MDL-3/benchmark.json`, `release-report/MDL-3/benchmark.junit.xml`.

## Pending closure evidence

- [ ] Exact accepted implementation SHA after all runtime-affecting changes.
- [x] Authenticated Genie Agent configuration export/read-back and `genie_live_config_sha256` (`release-report/MDL-3/genie-live-config.json`).
- [ ] Protected 30-attempt live batch with immutable workflow artifact and JUnit result.
- [ ] Databricks deployed smoke/soak against the same implementation/data/config digests (snapshot `01f1a0f6e3c013a3bc127c26e992a56b` is RUNNING; smoke records the external Genie V3 configuration failure in `release-report/deployed-smoke.json`).
- [ ] A05/A07 artwork candidates, production-byte hashes, and previews (implementation gate; final human revision is reserved for pre-submission polish and is not a closure blocker).
- [ ] Final-head CI and post-merge verification.

The report must not be changed to `COMPLETE` until every pending item has immutable evidence bound to the same accepted implementation identity.
