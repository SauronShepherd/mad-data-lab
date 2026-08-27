# ADR: MDL-4 architecture mapping

Status: Accepted for MDL-4

MDL-4 retains the existing runtime boundaries. `server/` is the authoritative
API and session runtime and maps to the specification's proposed
`backend/api/routes/` and `backend/sessions/` modules. `src/` is the browser
runtime and maps to the proposed `frontend/src/pages/` and
`frontend/src/components/` tree.

This is an organizational mapping only. State, scoring, evidence, verdicts,
and progression remain server-authoritative; the client remains presentation-
only. No duplicate implementation is introduced under the proposed paths.
