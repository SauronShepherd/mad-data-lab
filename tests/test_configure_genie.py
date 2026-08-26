import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_configure_genie_renders_only_validated_source_identifiers(tmp_path: Path):
    output = tmp_path / "source.json"
    result = subprocess.run([sys.executable, "scripts/configure_genie.py", "--catalog", "sda_dev", "--schema", "mad_data_lab", "--output", str(output)], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    source = json.loads(output.read_text(encoding="utf-8"))
    assert all("${" not in item["identifier"] for item in source["curated_sources"])
    assert all(item["identifier"].startswith("sda_dev.mad_data_lab_curated.") for item in source["curated_sources"])


def test_configure_genie_rejects_sql_identifier_injection(tmp_path: Path):
    result = subprocess.run([sys.executable, "scripts/configure_genie.py", "--catalog", "sda_dev;DROP", "--schema", "mad_data_lab", "--output", str(tmp_path / "bad.json")], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode != 0
