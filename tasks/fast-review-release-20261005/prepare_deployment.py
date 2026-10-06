"""Prepare explicit, private-data-free service and local worker release trees."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUTHORITY = {
    "INTERVIEW-PROTOCOL-v6.md": "tasks/scenario-survey-v7-redesign-20260922/INTERVIEW-PROTOCOL-v6.md",
    "interviewer-bank-v7.json": "tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json",
    "EVIDENCE-GUIDE-v7.json": "tasks/scenario-survey-v7-redesign-20260922/EVIDENCE-GUIDE-v7.json",
    "INTERVIEW-CONTROLLER-v2.md": "tasks/full-survey-participant-v2-20260927/INTERVIEW-CONTROLLER-v2.md",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    if subprocess.check_output(["git", "-C", str(ROOT), "diff", "HEAD", "--",
                                "apps/life-patterns-participant"], text=True):
        raise RuntimeError("Commit the tested application before staging its release.")
    output = args.destination.resolve()
    output.mkdir(parents=True, exist_ok=False)
    upload, worker = output/"upload", output/"worker"
    participant = ROOT/"apps/life-patterns-participant/participant"
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc")
    shutil.copytree(participant, upload/"apps/life-patterns-participant/participant", ignore=ignore)
    shutil.copytree(participant, worker/"participant", ignore=ignore)
    for name in ["Dockerfile", "requirements.txt"]:
        shutil.copy2(ROOT/"apps/life-patterns-participant"/name,
                     upload/"apps/life-patterns-participant"/name)
    shutil.copy2(ROOT/"apps/life-patterns-participant/scripts/gpt_review_worker.py",
                 worker/"gpt_review_worker.py")
    (worker/"authority").mkdir()
    for name, rel in AUTHORITY.items():
        dst = upload/rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT/rel, dst)
        shutil.copy2(ROOT/rel, worker/"authority"/name)
    manifest = {"source_commit": head, "contains_participant_data": False,
                "contains_credentials": False, "files": {}}
    for f in sorted(output.rglob("*")):
        if f.is_file():
            manifest["files"][str(f.relative_to(output))] = hashlib.sha256(f.read_bytes()).hexdigest()
    (output/"MANIFEST.json").write_text(json.dumps(manifest, indent=2)+'\n')
    Path(__file__).with_name("DEPLOYMENT-FILES.json").write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps({"source_commit": head, "file_count": len(manifest["files"]), "staged": True}))


if __name__ == "__main__":
    main()
