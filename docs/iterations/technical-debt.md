# Technical-debt ledger

| id | introduced_in | reason | risk | must_close_by | owner | status |
|---|---|---|---|---|---|---|
| TD-001 | MDL-1 | `server/catalog.py` retains a compatibility projection while all cases are not yet canonical YAML-owned; rationale: availability remains server-authoritative and secondary cases are locked. | Projection drift or accidental secondary-case enablement. | MDL-4 | backend | MITIGATED |
| TD-002 | MDL-1 | `server/genie.py` retains a fixture-space compatibility adapter beside the strict V3 boundary; rationale: strict protocol validation and boundary tests prevent legacy shapes from controlling state. | Legacy response shape could be used outside migration tests. | MDL-3 | genie | MITIGATED |
| TD-003 | MDL-1 | rationale: GitHub Actions/branch-protection evidence is intentionally out of scope by owner instruction. | GitHub-hosted release identity is not part of this acceptance run. | MDL-1 | release | DEFERRED_OUT_OF_SCOPE |
| TD-004 | MDL-1 | Human exact-byte approval for production artwork is pending. | Subjective art gate cannot be self-approved. | MDL-1 | product | BLOCKED_HUMAN |
| TD-005 | MDL-1 | rationale: current profile `mdl` has no MAD DATA LAB Genie Space; the listed app is `UNAVAILABLE`/not deployed and returns 502. | Live Genie/runtime behavior and deployed identity cannot be closed from the current workspace. | MDL-3 | platform | BLOCKED_EXTERNAL |
