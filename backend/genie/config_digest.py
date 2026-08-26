"""Deterministic hashing and validation for repository-owned Genie config."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]
import re


ROOT = Path(__file__).resolve().parents[2]


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def file_digest(*paths: str | Path) -> str:
    payload = []
    for path in sorted((Path(p) for p in paths), key=lambda item: item.as_posix()):
        try:
            logical_path = path.relative_to(ROOT).as_posix()
        except ValueError:
            logical_path = path.as_posix()
        payload.append({"path": logical_path, "content": path.read_text(encoding="utf-8")})
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def load_benchmark(path: Path | None = None) -> dict[str, Any]:
    source = path or ROOT / "genie/benchmarks/mdl3-live.yaml"
    value = yaml.safe_load(source.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("attempts"), list):
        raise ValueError("invalid benchmark corpus")
    ids = [item.get("id") for item in value["attempts"]]
    expected = [
        *(f"OBS-{i:02d}" for i in range(1, 4)), *(f"CMP-{i:02d}" for i in range(1, 4)),
        *(f"SNP-{i:02d}" for i in range(1, 4)), *(f"DQ-{i:02d}" for i in range(1, 4)),
        *(f"FOR-{i:02d}" for i in range(1, 4)), *(f"LIN-{i:02d}" for i in range(1, 3)),
        *(f"GSTART-{i:02d}" for i in range(1, 6)), *(f"GNEXT-{i:02d}" for i in range(1, 6)),
        *(f"SEC-{i:02d}" for i in range(1, 4)),
    ]
    if ids != expected or len(set(ids)) != 30:
        raise ValueError("benchmark IDs do not match the locked 30-attempt corpus")
    required = {"id", "turn_type", "phrasing_id", "prompt", "critical_grader"}
    if any(not required.issubset(item) for item in value["attempts"]):
        raise ValueError("benchmark row is missing required fields")
    return value


def render_agent_source(*, catalog: str, schema: str) -> dict[str, Any]:
    """Render the repository-owned Agent source for validated deployment config."""
    identifier = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
    if not identifier.fullmatch(catalog) or not identifier.fullmatch(schema):
        raise ValueError("catalog and schema must be closed SQL identifiers")
    source = json.loads((ROOT / "genie/agent.source.json").read_text(encoding="utf-8"))
    rendered = json.loads(canonical_json(source).replace("${CATALOG}", catalog).replace("${SCHEMA}", schema))
    rendered["curated_sources"] = sorted(rendered["curated_sources"], key=lambda item: item["identifier"])
    return rendered


def genie_contract_digest() -> str:
    return file_digest(ROOT / "genie/instructions.md", ROOT / "genie/registry.json", ROOT / "genie/benchmarks/mdl3-live.yaml", ROOT / "genie/agent.source.json")
