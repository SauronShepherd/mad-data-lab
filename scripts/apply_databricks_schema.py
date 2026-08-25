"""Apply the repository-controlled MDL-2 schemas, tables, and curated views."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.data.sql_client import connect_from_env, execute_native, SqlAdapterError

ROOT = Path(__file__).resolve().parents[1]
IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

def render(text: str, catalog: str) -> str:
    if not IDENTIFIER.fullmatch(catalog):
        raise ValueError("catalog must be a closed identifier")
    return text.replace("{{PUBLIC}}", f"{catalog}.mad_data_lab_public").replace("{{PRIVATE}}", f"{catalog}.mad_data_lab_private").replace("{{CURATED}}", f"{catalog}.mad_data_lab_curated")

def statements(text: str) -> list[str]:
    return [part.strip() for part in text.split(";") if part.strip()]

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", default=os.getenv("MDL_CATALOG", ""))
    parser.add_argument("--target", choices=("plan", "staging"), default="plan")
    args = parser.parse_args()
    if not args.catalog:
        raise SystemExit("--catalog is required")
    paths = sorted((ROOT / "data/ddl").glob("*.sql")) + sorted((ROOT / "data/views").glob("*.sql"))
    rendered = []
    for path in paths:
        text = render(path.read_text(encoding="utf-8"), args.catalog)
        if path.parent.name == "views":
            view_name = re.sub(r"^\d+_", "", path.stem)
            text = f"CREATE OR REPLACE VIEW {args.catalog}.mad_data_lab_curated.{view_name} AS\n{text}"
        rendered.append((path, text))
    digest = hashlib.sha256(b"".join(path.relative_to(ROOT).as_posix().encode() + b"\0" + text.encode() + b"\0" for path, text in rendered)).hexdigest()
    payload = {"status": "PLAN", "target": args.target, "catalog": args.catalog, "ddl_files": len(paths), "source_digest": digest}
    if args.target == "staging":
        try:
            with connect_from_env() as connection:
                with connection.cursor() as cursor:
                    for _, text in rendered:
                        for statement in statements(text):
                            execute_native(cursor, statement, ())
            payload["status"] = "PASS"
        except SqlAdapterError as exc:
            raise SystemExit(f"schema apply: NOT RUN ({exc})") from exc
    out = ROOT / "release-report/MDL-2/schema-apply.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))

if __name__ == "__main__":
    main()
