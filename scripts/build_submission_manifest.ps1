$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$files = @(
  'app.yaml','app.yml','requirements.txt','pyproject.toml','uv.lock',
  'src/main.jsx','server/main.py','server/genie.py',
  'docs/MDL-8-build-plan.md','docs/iterations/MDL-8-report.md',
  'release-report/MDL-8/final-acceptance-matrix.md',
  'release-report/MDL-8/ui-diagnostic.json',
  'release-report/MDL-8/databricks-remote-verification.json',
  'release-report/MDL-8/databricks-app-deployment.json',
  'release-report/MDL-8/deployed-soak-live.json',
  'release-report/MDL-8/demo-video-narrated-verification.json',
  'release-report/MDL-8/MDL-8-demo-narrated.mp4'
)
$files += (Get-ChildItem 'release-report/MDL-8/screenshots' -File | ForEach-Object { $_.FullName.Substring($root.Length + 1) })
$files += (Get-ChildItem 'docs/canonical-source' -File | ForEach-Object { $_.FullName.Substring($root.Length + 1) })
$entries = foreach ($relative in $files | Sort-Object -Unique) {
  $full = Join-Path $root $relative
  if (Test-Path -LiteralPath $full -PathType Leaf) {
    $hash = Get-FileHash -LiteralPath $full -Algorithm SHA256
    [ordered]@{ path = $relative.Replace('\','/'); sha256 = $hash.Hash.ToLowerInvariant(); bytes = (Get-Item -LiteralPath $full).Length }
  }
}
$manifest = [ordered]@{
  status = 'ENGINEERING_COMPLETE_EXTERNAL_GATES_PENDING'
  generated_at_utc = (Get-Date).ToUniversalTime().ToString('o')
  ci_scope = 'excluded_by_owner_instruction'
  file_count = @($entries).Count
  files = @($entries)
  pending_external = @('final public-link confirmation','submission-form acceptance')
}
$manifest | ConvertTo-Json -Depth 8 | Set-Content 'release-report/MDL-8/submission-manifest.json'
Get-Content 'release-report/MDL-8/submission-manifest.json'
