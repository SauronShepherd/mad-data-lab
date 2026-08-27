"""Fail-closed validation for an iteration evidence manifest."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
REQUIRED={"iteration","branch","base_commit_sha","base_tree_sha","accepted_head_commit_sha","accepted_head_tree_sha","pull_request_number","required_ci_checks","github_workflow_run_ids","test_report_sha256","build_artifact_sha256","databricks_deployment","data_schema_version","genie_config_sha256","asset_sha256","human_art_approval_files","open_blockers"}
def main() -> int:
    path=Path(sys.argv[1]); data=json.loads(path.read_text())
    missing=sorted(REQUIRED-set(data)); blockers=data.get("open_blockers",[])
    complete="--require-complete" in sys.argv
    errors=[f"missing:{x}" for x in missing]
    if data.get("iteration") != "MDL-4": errors.append("iteration:not-MDL-4")
    if data.get("branch") != "MDL-4": errors.append("branch:not-MDL-4")
    for field in ("base_commit_sha", "base_tree_sha", "accepted_head_commit_sha", "accepted_head_tree_sha"):
        if not isinstance(data.get(field), str) or not re.fullmatch(r"[0-9a-f]{40}", data[field]): errors.append(f"malformed:{field}")
    for field in ("asset_sha256", "databricks_deployment"):
        if not isinstance(data.get(field), dict): errors.append(f"malformed:{field}")
    for field in ("required_ci_checks", "github_workflow_run_ids", "human_art_approval_files", "open_blockers"):
        if not isinstance(data.get(field), list): errors.append(f"malformed:{field}")
    if complete and blockers: errors.append("open_blockers:"+",".join(blockers))
    result={"status":"PASS" if not errors else "FAIL","errors":errors,"iteration":data.get("iteration")}
    print(json.dumps(result,sort_keys=True)); return 0 if not errors else 1
if __name__ == "__main__": raise SystemExit(main())
