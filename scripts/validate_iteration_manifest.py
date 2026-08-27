"""Fail-closed validation for an iteration evidence manifest."""
from __future__ import annotations
import json, sys
from pathlib import Path
REQUIRED={"iteration","branch","base_commit_sha","base_tree_sha","accepted_head_commit_sha","accepted_head_tree_sha","pull_request_number","required_ci_checks","github_workflow_run_ids","test_report_sha256","build_artifact_sha256","databricks_deployment","data_schema_version","genie_config_sha256","asset_sha256","human_art_approval_files","open_blockers"}
def main() -> int:
    path=Path(sys.argv[1]); data=json.loads(path.read_text())
    missing=sorted(REQUIRED-set(data)); blockers=data.get("open_blockers",[])
    complete="--require-complete" in sys.argv
    errors=[f"missing:{x}" for x in missing]
    if complete and blockers: errors.append("open_blockers:"+",".join(blockers))
    result={"status":"PASS" if not errors else "FAIL","errors":errors,"iteration":data.get("iteration")}
    print(json.dumps(result,sort_keys=True)); return 0 if not errors else 1
if __name__ == "__main__": raise SystemExit(main())
