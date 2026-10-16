"""Install complete existing-GPT Railway finish release in owner Downloads."""

from __future__ import annotations

import hashlib
import json
import os
import zipfile
from pathlib import Path

from build_finish_gpt_release import OUT

FOLDER = "Life-Patterns-Railway-Finish-2026-10-16"


def exact_copy(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if hashlib.sha256(path.read_bytes()).digest() != hashlib.sha256(data).digest():
            raise ValueError("Owner file already exists with different content: " + path.name)
    else:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
    if path.read_bytes() != data:
        raise ValueError("Owner file readback mismatch: " + path.name)


def install(downloads: Path) -> dict:
    with zipfile.ZipFile(OUT) as archive:
        names = archive.namelist()
        if any(name.startswith("/") or ".." in Path(name).parts for name in names):
            raise ValueError("Bad packaged path")
        manifest = json.loads(archive.read("UPDATE-MANIFEST.json"))
        if any(
            hashlib.sha256(archive.read(name)).hexdigest() != expected
            for name, expected in manifest["files"].items()
        ):
            raise ValueError("Release signature mismatch")
        for name in names:
            exact_copy(downloads / FOLDER / name, archive.read(name))
    exact_copy(downloads / OUT.name, OUT.read_bytes())
    return {
        "download_folder": FOLDER,
        "zip_filename": OUT.name,
        "knowledge_count": manifest["knowledge_files"],
        "schema_version": manifest["action_version"],
        "owner_file_bytes_verified": True,
        "private_editor_updated": False,
    }


if __name__ == "__main__":
    print(json.dumps(install(Path.home() / "Téléchargements")))
