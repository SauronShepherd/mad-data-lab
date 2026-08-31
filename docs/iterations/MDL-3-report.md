# MDL-3 iteration report

status: IN_PROGRESS
implementation_sha: fa5b5a4ae79e9cff826387dd4e1a9e2686b62ccb
runtime_digest: 4748d3ea2c32ff12c364e822da5c939e435b1fa3aa15528c20b8cd215bf4cfa4
genie_contract_digest: fdd440feb9db1fa35a048c1b57008bd1b0fdd64bb451611f183f0a57244794e9
genie_live_config_sha256: 0aa19a3f70f0318058f467d9173208b46ec30ec2b2859a96e7ff52b5aef14ebd
mdl2_data_contract_digest: 083e4b26f13427ce24da11832372dc6e3d3c9c02601a3eef600a1fd71ec76e2b
benchmark_batch_id: mdl3-accepted-baseline

## Implemented local evidence

- Strict Pydantic protocol and exact control-object extraction: `backend/genie/protocol.py`.
- One-repair lifecycle and safe protocol/query failure separation: `backend/genie/lifecycle.py`.
- Pending first-Experiment decision persistence/consumption: `backend/genie/decisions.py`, `server/main.py`.
- Closed Experiment registry and permanent instructions: `genie/registry.json`, `genie/instructions.md`.
- Frozen 40-attempt corpus: `genie/benchmarks/mdl3-live.yaml`.
- Local contract gate: `release-report/MDL-3/contract-validation.json`.
- Local fixture benchmark JSON/JUnit: `release-report/MDL-3/benchmark.json`, `release-report/MDL-3/benchmark.junit.xml`.
- Live benchmark harness now binds implementation SHA, runtime digest, Genie config digest, MDL-2 data digest, and public Case #042 hash into its output; live execution still requires authenticated credentials.
- Local release gates are the acceptance authority; GitHub Actions are intentionally out of scope.

## Pending closure evidence

- [ ] Exact accepted implementation SHA after all runtime-affecting changes (requires final repository freeze).
- [x] Authenticated Genie Agent configuration export/read-back and `genie_live_config_sha256` (`release-report/MDL-3/genie-live-config.json`).
- [ ] Protected 40-attempt live batch with immutable authenticated artifact and JUnit result (blocked by unavailable Genie Space).
- [x] Databricks deployed smoke/soak against frozen implementation `9d54ef38786d852d4b42eff4a7dc2c3d02d5d294` and matching runtime/data/config evidence (`release-report/deployed-smoke.json`, `release-report/deployed-soak.json`).
- [x] A05/A07 implementation-owned review candidates, hashes, contact sheets, preflight, and selected production derivatives (`release-report/MDL-3/art-preflight.json`, `release-report/MDL-3/art-contact-sheet.png`, `public/assets/pixelart/dr-genie-mdl3.png`, `public/assets/pixelart/hypothesis-chamber.png`).
- [x] GitHub Actions intentionally excluded by project direction; local verification remains required.

The report must not be changed to `COMPLETE` until every pending item has immutable evidence bound to the same accepted implementation identity.
