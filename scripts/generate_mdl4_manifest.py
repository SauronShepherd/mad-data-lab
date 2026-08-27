"""Generate the non-secret MDL-4 evidence manifest from current local state."""
from __future__ import annotations
import hashlib, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
def main() -> None:
    head, tree = git("rev-parse", "HEAD"), git("rev-parse", "HEAD^{tree}")
    ref = next((candidate for candidate in ("MDL-3", "origin/MDL-3") if subprocess.run(["git", "rev-parse", "--verify", candidate], cwd=ROOT, capture_output=True).returncode == 0), None)
    base = git("rev-parse", ref) if ref else None
    base_tree = git("rev-parse", f"{ref}^{{tree}}") if ref else None
    assets = {}
    plan = json.loads((ROOT / "assets/review/MDL-4/art-generation-plan.json").read_text())
    for item in plan["sha256"]: assets[item] = plan["sha256"][item]
    payload = {
        "iteration":"MDL-4", "branch":git("branch","--show-current"),
        "base_commit_sha":base, "base_tree_sha":base_tree,
        "accepted_head_commit_sha":head, "accepted_head_tree_sha":tree,
        "pull_request_number":None, "required_ci_checks":[], "github_workflow_run_ids":[],
        "test_report_sha256":{}, "build_artifact_sha256":None,
        "databricks_deployment":{"app_name":None,"deployment_or_run_id":None,"reported_build_sha":None,"reported_tree_sha":None,"post_deploy_smoke":"PENDING"},
        "data_schema_version":None, "genie_config_sha256":None, "asset_sha256":assets,
        "human_art_approval_files":[], "open_blockers":["exact-head-ci","live-deployment"]
    }
    out=ROOT/"release-report/MDL-4/manifest.json"; out.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","path":str(out.relative_to(ROOT))},sort_keys=True))
if __name__ == "__main__": main()
