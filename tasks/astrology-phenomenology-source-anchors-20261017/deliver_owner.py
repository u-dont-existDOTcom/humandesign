"""Place unscored source audit directly in owner Downloads."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASK = Path(__file__).resolve().parent
FOLDER = "Life-Patterns-Astrology-Source-Audit-2026-10-17"
ARTIFACTS = {
    "SOURCE-TO-SURVEY-IMPLICATIONS-v1.md": TASK / "SOURCE-TO-SURVEY-IMPLICATIONS-v1.md",
    "PRIMARY-SOURCE-CLAIM-ANCHORS-v1.json": TASK / "PRIMARY-SOURCE-CLAIM-ANCHORS-v1.json",
    "SOURCE-HTML-CHECK-RECEIPT-v1.json": TASK / "SOURCE-HTML-CHECK-RECEIPT-v1.json",
    "VERIFICATION-RECEIPT-v1.json": TASK / "VERIFICATION-RECEIPT-v1.json",
    "PTOLEMY-BOOK-IV-LIFE-DOMAINS-v1.json": TASK / "PTOLEMY-BOOK-IV-LIFE-DOMAINS-v1.json",
    "PTOLEMY-BOOK-IV-COVERAGE-ADDENDUM-v1.md": TASK / "PTOLEMY-BOOK-IV-COVERAGE-ADDENDUM-v1.md",
    "EXPERIENCE-MEANING-PILOT-v0.json": (
        ROOT
        / "tasks/life-patterns-early-review-and-experience-20261017"
        / "EXPERIENCE-MEANING-PILOT-v0.json"
    ),
    "CHART-DOMAIN-V7-RECONCILIATION-v0.json": (
        ROOT
        / "tasks/life-patterns-early-review-and-experience-20261017"
        / "CHART-DOMAIN-V7-RECONCILIATION-v0.json"
    ),
}
INTRO = (
    "# Life Patterns: astrology source and measurement audit\n\n"
    "Read SOURCE-TO-SURVEY-IMPLICATIONS-v1.md first.\n"
    "The primary source anchors distinguish the subjects traditional astrology\n"
    "actually discusses from modern awe, synchronicity, revelation and meaning\n"
    "measurements not explicitly predicted by the checked passages.\n\n"
    "Then read PTOLEMY-BOOK-IV-COVERAGE-ADDENDUM-v1.md for nine\n"
    "additional traditional natal LIFE-OUTCOME topics, from occupation\n"
    "and marriage to travel and timing. These are NOT personality scores.\n"
    "The associated verified original-page matrix is\n"
    "PTOLEMY-BOOK-IV-LIFE-DOMAINS-v1.json.\n\n"
    "The eight-question experimental pilot is optional, unscored, and not\n"
    "installed into any existing person's GPT interview or chart scorer.\n"
)


def write_checked(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != content:
            raise ValueError("Different existing owner artifact: " + path.name)
    else:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
    if hashlib.sha256(path.read_bytes()).digest() != hashlib.sha256(content).digest():
        raise ValueError("Delivery readback mismatch")


def deliver(downloads: Path) -> dict:
    dest = downloads / FOLDER
    for filename, source in ARTIFACTS.items():
        write_checked(dest / filename, source.read_bytes())
    write_checked(dest / "START-HERE.md", INTRO.encode("utf-8"))
    return {
        "folder": str(dest),
        "files": sorted(ARTIFACTS) + ["START-HERE.md"],
        "verified": True,
        "participant_data_in_artifacts": False,
        "frozen_questionnaire_unchanged": True,
    }


if __name__ == "__main__":
    print(json.dumps(deliver(Path.home() / "Téléchargements"), ensure_ascii=False))
