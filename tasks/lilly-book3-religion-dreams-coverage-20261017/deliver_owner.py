"""Deliver source-audit files locally without overwriting the older study."""

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = [
    "SOURCE-TO-SURVEY-RESULT-v1.md",
    "LILLY-BOOK3-RELIGION-DREAMS-CLAIMS-v1.json",
    "WITNESS-AND-V7-CHECK-v1.json",
    "OPTIONAL-RELIGION-DREAM-QUESTIONS-v0.json",
    "VERIFICATION-RECEIPT-v1.json",
]


def save(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != payload:
            raise ValueError("Owner artifact conflict: " + path.name)
    else:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
    path.chmod(0o600)
    assert hashlib.sha256(path.read_bytes()).digest() == hashlib.sha256(payload).digest()


def deliver(downloads):
    parent = downloads / "Life-Patterns-Astrology-Source-Audit-2026-10-17"
    target = parent / "Lilly-Book-III"
    for name in FILES:
        save(target / name, (HERE / name).read_bytes())
    intro = (
        "# Lilly Book III religion and dream audit\n\n"
        "Read Lilly-Book-III/SOURCE-TO-SURVEY-RESULT-v1.md.\n"
        "This adds 31 historical source units; not 31 validated predictors.\n"
        "Original planetary symbols still require scan-image checking.\n"
        "The new five-item research pilot is optional and not in live interviews.\n"
    )
    save(parent / "LILLY-BOOK-III-START-HERE.md", intro.encode())
    return {"files_verified": len(FILES) + 1, "target": str(target)}


if __name__ == "__main__":
    print(json.dumps(deliver(Path.home() / "Téléchargements")))
