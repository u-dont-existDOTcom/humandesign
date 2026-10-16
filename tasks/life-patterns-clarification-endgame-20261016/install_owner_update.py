"""Deliver owner-ready verified GPT progress fix into ordinary Downloads."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import zipfile
from pathlib import Path

from build_gpt_update import OUT

FOLDER = "Life-Patterns-Progress-Fix-2026-10-16"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_checked(path: Path, blob: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != blob:
            raise ValueError("Different existing owner file, refuse overwrite: " + path.name)
    else:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as dest:
            dest.write(blob)
    if sha(path.read_bytes()) != sha(blob):
        raise OSError("Failed to verify delivered owner file " + path.name)


def deliver(downloads: Path) -> dict:
    with zipfile.ZipFile(OUT) as archive:
        names = archive.namelist()
        if any(name.startswith("/") or ".." in Path(name).parts for name in names):
            raise ValueError("Unsafe archive path")
        digest = json.loads(archive.read("UPDATE-MANIFEST.json"))["files"]
        if any(sha(archive.read(k)) != v for k, v in digest.items()):
            raise ValueError("GPT release manifest mismatch")
        for name in names:
            write_checked(downloads / FOLDER / name, archive.read(name))
    write_checked(downloads / OUT.name, OUT.read_bytes())
    write_checked(
        downloads / FOLDER / "RAILWAY-FINISH-HANDOFF-DESIGN.md",
        (Path(__file__).resolve().parent / "RAILWAY-FINISH-HANDOFF-DESIGN.md").read_bytes(),
    )
    return {
        "zip": OUT.name,
        "folder": FOLDER,
        "knowledge_files": len([name for name in names if name.startswith("knowledge/")]),
        "exact_delivery_verified": True,
        "gpt_editor_updated": False,
    }


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--downloads", type=Path, default=Path.home() / "Téléchargements")
    print(json.dumps(deliver(cli.parse_args().downloads)))
