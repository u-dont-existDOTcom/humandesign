"""Update owner's local guide to prioritize completed result and simplified question."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

OLD = "Life-Patterns-V33-Role-Entry-PRIVATE-2026-10-15.html"
NEW = "Life-Patterns-One-Question-Simplified-PRIVATE-2026-10-15.html"
REPORT = ".life-patterns-private-v33-review-20261015/ROLE-REVIEW-PRIVATE.html"
LINK = (
    '<article><h2><a href="' + REPORT + '">'
    "My completed role-entry analysis</a></h2>"
    "<p>Already answered: conditional group and one-to-one helping. No more answers are needed. "
    "Includes the fixed-model development comparison and its limitations.</p></article>"
)


def install(downloads: Path):
    guide = downloads / "Life-Patterns-Researcher-Guide.html"
    for needed in (downloads / NEW, downloads / REPORT):
        if not needed.is_file():
            raise FileNotFoundError(needed)
    s = guide.read_text(encoding="utf-8")
    if OLD not in s and NEW not in s:
        raise ValueError("No existing role-entry guide entry")
    backup = downloads / ".Life-Patterns-Researcher-Guide.pre-one-question-20261015.html"
    if not backup.exists():
        shutil.copy2(guide, backup)
        backup.chmod(0o600)
    if OLD in s:
        s = s.replace(OLD, NEW, 1)
        s = s.replace(
            "Answer the missing group-role question (V3.3, private)",
            "Simplified role question (optional; already answered)",
            1,
        )
    if LINK not in s:
        if s.count("<body>") != 1:
            raise ValueError("Guide body anchor count")
        s = s.replace("<body>", "<body>" + LINK, 1)
    guide.write_text(s, encoding="utf-8")
    assert s == guide.read_text()
    assert NEW in s and REPORT in s
    return {
        "guide_link_fixed": True,
        "completed_report_linked": True,
        "old_source_retained": (downloads / OLD).is_file(),
    }


if __name__ == "__main__":
    d = Path.home() / "Téléchargements"
    p = argparse.ArgumentParser()
    p.add_argument("--downloads", type=Path, default=d)
    print(install(p.parse_args().downloads))
