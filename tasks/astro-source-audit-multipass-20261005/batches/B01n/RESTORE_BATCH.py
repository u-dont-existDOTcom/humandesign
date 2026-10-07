"""Restore the source-audit packet, checking all bytes before writing any file."""
from pathlib import Path
import base64
import hashlib
import json
import lzma

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PREFIX = "tasks/astro-source-audit-multipass-20261005/batches/B01n/"


def check(condition, message):
    if not condition:
        raise SystemExit(message)


def digest(body):
    return hashlib.sha256(body).hexdigest()


manifest = json.loads((HERE / "ARCHIVE_MANIFEST.json").read_text())
archive = HERE / manifest["archive"]
check(archive.parent == HERE and not archive.is_symlink(), "Unsafe archive path")
if archive.exists():
    raw = archive.read_bytes()
else:
    encoded = []
    for part in manifest["encoded_parts"]:
        path = HERE / part["path"]
        check(path.parent == HERE and not path.is_symlink(), "Unsafe part path")
        body = path.read_bytes()
        check(len(body) == part["bytes"] and digest(body) == part["sha256"], "Encoded part digest mismatch")
        encoded.append(body)
    raw = base64.b64decode(b"".join(encoded), validate=True)
check(len(raw) == manifest["bytes"] and digest(raw) == manifest["sha256"], "Archive digest mismatch")
files = json.loads(lzma.decompress(raw).decode("utf-8"))
check(set(files) == set(manifest["members"]), "Unexpected member set")
staged = []
for name, text in files.items():
    rel = Path(name)
    check(not rel.is_absolute() and ".." not in rel.parts and name.startswith(PREFIX), "Out-of-scope member")
    dest = ROOT / rel
    check(not dest.is_symlink() and dest.resolve().is_relative_to(ROOT.resolve()), "Unsafe destination")
    body = text.encode("utf-8")
    spec = manifest["members"][name]
    check(len(body) == spec["bytes"] and digest(body) == spec["sha256"], "Member digest mismatch: " + name)
    if dest.exists():
        check(dest.is_file() and dest.read_bytes() == body, "Preserve conflicting file: " + name)
    else:
        staged.append((dest, body))
# No output is written until all member digests and existing conflicts are checked.
for dest, body in staged:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("xb") as out:
        out.write(body)
print(f"Verified {len(files)} members; restored {len(staged)} missing files. No runtime/model changes.")
