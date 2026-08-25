## MAD DATA LAB change review

### Source and scope

- [ ] The PR branch is the intended iteration branch (`MDL-*`).
- [ ] The checked-out `HEAD` is the exact commit reviewed by this PR.
- [ ] The change does not expose private Case truth in public fixtures, SQL, or the built frontend.
- [ ] Secondary Cases remain locked unless their complete contracts are present.

### Evidence

- [ ] `python -m pytest -q` result is attached or available in CI.
- [ ] Typecheck, frontend build, security, architecture, and contract-gate results are attached.
- [ ] Docker smoke/shutdown results are attached when runtime or packaging changes.
- [ ] Any Databricks evidence names the profile/environment, deployment identity, and source SHA.

### Release blockers

- Human artwork approvals: `docs/approvals/MDL-1-art.md` and `docs/approvals/MDL-2-art.md`.
- MDL-1 predecessor closure: `docs/traceability/MDL-2-predecessor.json`.
- Live/deployed evidence freshness: `release-report/{genie-eval,deployed-smoke,deployed-soak}.json`.

Do not mark a blocker complete without the corresponding external evidence.
