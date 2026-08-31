# Release evidence

`release-report/MDL-4/` and earlier iteration directories contain historical evidence and must not be rewritten with successor-iteration identity. Current local evidence is generated under `release-report/MDL-5/` by `scripts/release_candidate.py` and `scripts/release_gate.py`.

Dynamic reports are source-bound and may become stale after any source or configuration change. Verify the recorded runtime/data digests and dirty-worktree flag before treating them as acceptance evidence. Live Genie, deployed smoke/soak, human artwork approval, and publication evidence are not inferred from local PASS results.

GitHub Actions evidence is intentionally outside this project’s acceptance scope by owner instruction.
