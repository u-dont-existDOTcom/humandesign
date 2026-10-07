"""Restore the complete B01p/B01q research records without overwriting conflicts.

Run this script in its published repository location. Every part, member and
existing destination is checked before any missing file is written. No raw
source books, astronomy runtime, fitted model or progress mirror is changed.
"""
from __future__ import annotations

import base64
import hashlib
import json
import lzma
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ALLOWED = (
    "tasks/astro-source-audit-multipass-20261005/batches/B01p/",
    "tasks/astro-source-audit-multipass-20261005/batches/B01q/",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def main() -> None:
    manifest_path = HERE / "ARCHIVE_MANIFEST.json"
    require(not manifest_path.is_symlink(), "Unsafe manifest path")
    manifest = json.loads(manifest_path.read_text(), object_pairs_hook=unique_object)
    encoded: list[bytes] = []
    for part in manifest["parts"]:
        name = part["path"]
        require(Path(name).name == name, "Unsafe part name")
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), "Missing or unsafe part")
        data = path.read_bytes()
        require(len(data) == part["bytes"] and digest(data) == part["sha256"], "Part digest mismatch")
        encoded.append(data)
    raw = base64.b64decode(b"".join(encoded), validate=True)
    require(len(raw) == manifest["archive_bytes"], "Archive length mismatch")
    require(digest(raw) == manifest["archive_sha256"], "Archive digest mismatch")
    files = json.loads(lzma.decompress(raw).decode("utf-8"), object_pairs_hook=unique_object)
    require(set(files) == set(manifest["members"]), "Archive member set mismatch")
    pending: list[tuple[Path, bytes]] = []
    for name, text in files.items():
        rel = Path(name)
        require(not rel.is_absolute() and ".." not in rel.parts and name.startswith(ALLOWED), "Out-of-scope member")
        dest = ROOT / rel
        require(not any(p.is_symlink() for p in (dest, *dest.parents) if p != ROOT.parent), "Symlink destination")
        require(dest.resolve().is_relative_to(ROOT.resolve()), "Destination outside root")
        require(isinstance(text, str), "Non-text research member")
        body = text.encode("utf-8")
        spec = manifest["members"][name]
        require(len(body) == spec["bytes"] and digest(body) == spec["sha256"], "Member digest mismatch: " + name)
        if dest.exists():
            require(dest.is_file() and dest.read_bytes() == body, "Preserve conflicting file: " + name)
        else:
            pending.append((dest, body))
    for dest, body in pending:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("xb") as output:
            output.write(body)
    print(f"Verified {len(files)} research members; restored {len(pending)} missing files. No runtime or progress changes.")


if __name__ == "__main__":
    main()
