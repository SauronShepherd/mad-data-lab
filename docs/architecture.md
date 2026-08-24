# MAD DATA LAB architecture

```text
Player
  -> React/Vite Case Board and Investigation UI
  -> FastAPI session API (authoritative state, score, events)
  -> Genie Conversation API (live) or deterministic fixture fallback
  -> Curated SQL evidence in Databricks
  -> deterministic instruments and evidence explorer
```

The browser never receives `CASE_TRUTH`. The server validates Case availability,
registered Experiment IDs, epistemic statuses, instruments, transitions, and
completion criteria. Genie can choose only from a versioned Experiment Registry;
the UI renders the returned controlled instrument rather than executing model
generated code.

## Case #042 data flow

1. `case_observations` establishes the expected €125.0M and observed €118.2M.
2. `component_deltas` identifies V2 at -€5.9M.
3. `snapshot_changes` reconciles the V2 movement across 23 modified, 2 removed,
   and 5 added records.
4. `evidence_records` exposes TX-004291 (-€4.2M) for record-level inspection.
5. `dq_signals` records the -€0.3M overlapping warning; it is not added again.
6. `formula_versions` proves the formula hash is unchanged.

The private truth contract is application-side only and is excluded from Genie
resources and public projections.
