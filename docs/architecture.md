# Architecture

The Vite/React client in `src/` renders the Investigation Map, Instruments, Evidence Explorer, hypotheses, and verdict flow. The FastAPI service in `server/` owns sessions, progression, validation, scoring, and API contracts. Canonical domain and Genie protocol models live under `backend/`.

Trusted SQL is closed over the registered query set in `backend/data/` and `sql/trusted/`. Public curated fixtures and private truth are separate; private truth is used only by server-side validation and never projected to the client or Genie.

The release gates bind data/runtime evidence to source identity. Secondary Cases remain catalogued but locked unless their own contracts and evidence are complete.
