"""Install full in-place GPT update and separate unscored research pilot locally."""

from __future__ import annotations

import hashlib
import json
import os
import zipfile
from pathlib import Path

from build_gpt_early_review import OUT, TASK

FOLDER = "Life-Patterns-Early-Railway-Review-2026-10-17"
RESEARCH = (
    "EXPERIENCE-MEANING-PILOT-v0.json",
    "CHART-DOMAIN-V7-RECONCILIATION-v0.json",
    "RESULT.md",
)


def checked_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file():
        if path.read_bytes() != payload:
            # Preserve prior draft under a deterministic hidden backup.
            backup = path.with_name("." + path.name + ".pre-v18-release")
            if backup.exists() and backup.read_bytes() != path.read_bytes():
                raise ValueError("Prior owner file changed since original backup")
            if not backup.exists():
                backup.write_bytes(path.read_bytes())
                backup.chmod(0o600)
            path.write_bytes(payload)
    else:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as output:
            output.write(payload)
    path.chmod(0o600)
    if path.read_bytes() != payload:
        raise ValueError("Owner file readback failed")


def install(downloads: Path) -> dict:
    destination = downloads / FOLDER
    with zipfile.ZipFile(OUT) as archive:
        entries = archive.namelist()
        if any(name.startswith("/") or ".." in Path(name).parts for name in entries):
            raise ValueError("Unsafe archive member")
        manifest = json.loads(archive.read("UPDATE-MANIFEST.json"))
        for name in entries:
            payload = archive.read(name)
            if (
                name in manifest["files"]
                and hashlib.sha256(payload).hexdigest() != manifest["files"][name]
            ):
                raise ValueError("Release manifest mismatch")
            checked_write(destination / name, payload)
    checked_write(downloads / OUT.name, OUT.read_bytes())
    for name in RESEARCH:
        checked_write(destination / name, (TASK / name).read_bytes())
    return {
        "destination": str(destination),
        "zip": str(downloads / OUT.name),
        "knowledge_files": manifest["knowledge_files"],
        "action": manifest["action_version"],
        "instructions_strict_characters": manifest["instructions_strict_characters"],
        "verified": True,
        "private_gpt_editor_updated": False,
    }


if __name__ == "__main__":
    print(json.dumps(install(Path.home() / "Téléchargements")))
