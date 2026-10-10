"""Verify protected Git objects and retained source-index entries."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

BATCH = Path(__file__).resolve().parent
REPO = BATCH.parents[3]
PREFIX = "tasks/astro-source-audit-multipass-20261005/batches/B02k/"
INDEX = "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
STATE = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261010_B02k.md"


def allowed(path):
    return path.startswith(PREFIX) or path in {INDEX, STATE}


def git(*arguments):
    return subprocess.check_output(["git", *arguments], cwd=REPO)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", default="HEAD")
    parser.add_argument("--working-index", action="store_true")
    parser.add_argument("--output", default="PRESERVATION_CHECKS.json")
    args = parser.parse_args()
    baseline = json.loads((BATCH / "PROTECTED_BASELINE.json").read_text())
    commit = git("rev-parse", args.commit).decode().strip()
    tree = {}
    for raw in git("ls-tree", "-r", "-z", commit).split(b"\0"):
        if not raw:
            continue
        meta, path = raw.split(b"\t", 1)
        mode, kind, sha = meta.decode().split()
        tree[path.decode()] = {"mode": mode, "type": kind, "git_sha": sha}
    mismatches = []
    for item in baseline["entries"]:
        expected = {k: item[k] for k in ["mode", "type", "git_sha"]}
        if tree.get(item["path"]) != expected:
            mismatches.append(item["path"])
    changed = [x.decode() for x in git("diff", "--name-only", "-z", baseline["base_commit"], commit).split(b"\0") if x]
    outside = [p for p in changed if not allowed(p)]
    before = json.loads((BATCH / "RETAINED_LILLY_INDEX_BEFORE.json").read_text())
    current_raw = (REPO / INDEX).read_bytes() if args.working_index else git("show", f"{commit}:{INDEX}")
    current = json.loads(current_raw)
    original_batches_retained = current["batches"][:len(before["batches"])] == before["batches"]
    original_chapters_retained = current["read_numbered_chapters"] == before["read_numbered_chapters"]
    receipt = {"base_commit": baseline["base_commit"], "checked_commit": commit,
        "protected_git_files_checked": len(baseline["entries"]), "protected_mismatches": mismatches,
        "changed_paths": changed, "changes_outside_allowlist": outside,
        "retained_prior_lilly_batch_entries": len(before["batches"]),
        "prior_batch_entries_unchanged": original_batches_retained,
        "completed_numbered_chapters_unchanged": original_chapters_retained,
        "index_basis": "local working index" if args.working_index else "fetched commit index",
        "index_sha256": hashlib.sha256(current_raw).hexdigest(),
        "verified": not mismatches and not outside and original_batches_retained and original_chapters_retained,
        "limits": "Git object preservation and inventory equality, not empirical validation."}
    (BATCH / args.output).write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({k: v for k, v in receipt.items() if k != "changed_paths"}))
    return 0 if receipt["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
