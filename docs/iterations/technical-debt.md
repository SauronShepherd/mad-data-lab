# Technical-debt ledger

| id | introduced_in | reason | risk | must_close_by | owner | status |
|---|---|---|---|---|---|---|
| TD-001 | MDL-1 | `server/catalog.py` retains a compatibility projection while all cases are not yet canonical YAML-owned. | Projection drift or accidental secondary-case enablement. | MDL-4 | backend | OPEN |
| TD-002 | MDL-1 | `server/genie.py` retains a fixture-space compatibility adapter beside the strict V3 boundary. | Legacy response shape could be used outside migration tests. | MDL-3 | genie | OPEN |
| TD-003 | MDL-1 | GitHub branch-protection and exact-head CI evidence is external to this checkout. | Release identity cannot yet be independently proven. | MDL-1 | release | BLOCKED_EXTERNAL |
| TD-004 | MDL-1 | Human exact-byte approval for production artwork is pending. | Subjective art gate cannot be self-approved. | MDL-1 | product | BLOCKED_HUMAN |
| TD-005 | MDL-1 | Databricks live smoke/evaluation refresh is pending Free Edition quota reset. | Runtime behavior and Genie configuration cannot be closed today. | MDL-3 | platform | BLOCKED_EXTERNAL |
