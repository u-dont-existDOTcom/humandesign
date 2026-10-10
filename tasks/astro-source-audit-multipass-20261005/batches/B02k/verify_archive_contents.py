"""Verify original packet bytes before rerunning tests changes execution logs."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    manifest = json.loads((ROOT / "ARCHIVE_CONTENT_MANIFEST.json").read_text())
    checked = []
    errors = []
    for entry in manifest["files"]:
        path = ROOT / entry["path"]
        if not path.is_file():
            errors.append({"path": entry["path"], "error": "missing"})
            continue
        data = path.read_bytes()
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            errors.append({"path": entry["path"], "error": "content mismatch"})
        else:
            checked.append(entry["path"])
    print(json.dumps({"payload_files_checked": len(checked), "errors": errors,
                      "manifest_does_not_hash_itself": True,
                      "success": not errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
