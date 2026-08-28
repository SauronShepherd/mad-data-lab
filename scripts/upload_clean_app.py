"""Upload a filtered Apps source tree as RAW Workspace files."""
from __future__ import annotations

import os
from pathlib import Path

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ImportFormat


ROOT = Path(os.environ.get("MDL_CLEAN_SOURCE", r"C:\mdl-source-clean-20260828"))
DEST = os.environ.get("MDL_CLEAN_DEST", "/Workspace/Users/angel.alvarez.pascua@gmail.com/mad-data-lab-clean-20260828")


def main() -> None:
    client = WorkspaceClient(profile="mdl")
    client.workspace.mkdirs(DEST)
    count = 0
    for directory, _, files in os.walk(ROOT):
        relative_directory = Path(directory).relative_to(ROOT).as_posix()
        if relative_directory != ".":
            client.workspace.mkdirs(f"{DEST}/{relative_directory}")
        for filename in files:
            local_path = Path(directory) / filename
            remote_path = f"{DEST}/{local_path.relative_to(ROOT).as_posix()}"
            with local_path.open("rb") as handle:
                client.workspace.upload(remote_path, handle, format=ImportFormat.AUTO, overwrite=True)
            count += 1
    print(f"uploaded {count} files to {DEST}")


if __name__ == "__main__":
    main()
