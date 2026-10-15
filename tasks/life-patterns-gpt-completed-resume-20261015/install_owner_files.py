"""Copy the verified non-secret Custom GPT update directly to owner Downloads."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PACKAGE = (
    ROOT
    / "reference/custom_gpt/releases/Life-Patterns-GPT-completed-interview-update-2026-10-15.zip"
)
FOLDER = "Life-Patterns-GPT-Ready-2026-10-15"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install(downloads: Path) -> dict:
    downloads.mkdir(parents=True, exist_ok=True)
    archive = downloads / PACKAGE.name
    if archive.exists() and digest(archive) != digest(PACKAGE):
        raise ValueError("Existing owner download has different bytes; refuse overwrite")
    if not archive.exists():
        shutil.copy2(PACKAGE, archive)
    if digest(archive) != digest(PACKAGE):
        raise ValueError("Owner download copy/hash mismatch")

    directory = downloads / FOLDER
    directory.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(PACKAGE) as z:
        names = sorted(z.namelist())
        if any(name.startswith("/") or ".." in Path(name).parts for name in names):
            raise ValueError("Unsafe ZIP extraction path")
        manifest = json.loads(z.read("UPDATE-MANIFEST.json"))
        for name in names:
            item = directory / name
            item.parent.mkdir(parents=True, exist_ok=True)
            payload = z.read(name)
            if item.exists():
                if item.read_bytes() != payload:
                    raise ValueError("Installed file conflict: " + name)
            else:
                fd = os.open(item, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
                with os.fdopen(fd, "wb") as dest:
                    dest.write(payload)
            if hashlib.sha256(item.read_bytes()).hexdigest() != hashlib.sha256(payload).hexdigest():
                raise ValueError("Owner readback mismatch: " + name)
    if len([n for n in names if n.startswith("knowledge/")]) != 8:
        raise ValueError("Incomplete Knowledge handoff")
    return {
        "verified_update_zip_in_downloads": True,
        "extracted_update_folder": FOLDER,
        "instructions_strict_count": manifest["instructions_strict_linebreak_count"],
        "knowledge_files": 8,
        "gpt_editor_updated": False,
        "private_data_in_package": False,
    }


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--downloads", type=Path, default=Path.home() / "Téléchargements")
    print(json.dumps(install(cli.parse_args().downloads)))
