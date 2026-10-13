"""Install a private, immutable crosswalk beside the owner's local researcher guide.

Source must already have been independently produced in the private owner-only
workspace. Never write source text or personal routes to GitHub.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install(source: Path, downloads: Path) -> dict:
    output = {}
    for extension, label in (("html", "HTML"), ("md", "Markdown")):
        name = f"My-Life-Patterns-V3-vs-Historical-Survey.{extension}"
        src = source / name
        if not src.is_file():
            raise FileNotFoundError(f"Private source missing: {extension}")
        dst = downloads / f"Life-Patterns-New-vs-Old-Answers-2026-10-13.{extension}"
        if dst.exists() and digest(src) != digest(dst):
            backup = dst.with_name(dst.stem + "-previous" + dst.suffix)
            if not backup.exists():
                shutil.copy2(dst, backup)
                backup.chmod(0o600)
        shutil.copy2(src, dst)
        dst.chmod(0o600)
        assert digest(src) == digest(dst)
        output[f"{label.lower()}_bytes"] = dst.stat().st_size

    guide = downloads / "Life-Patterns-Researcher-Guide.html"
    relative = "Life-Patterns-New-vs-Old-Answers-2026-10-13.html"
    changed = False
    if guide.exists():
        existing = guide.read_text()
        if relative not in existing:
            if "</body>" not in existing:
                raise RuntimeError("Cannot locate end of existing guide")
            block = (
                '<article><h2><a href="'
                + relative
                + '">Your new guided answers compared with the old interview</a></h2>'
                "<p>Private same-person development comparison: 25 new question"
                " routes, 24 direct older route links and six independent-review"
                " findings classified as partial/different targets. This is not"
                " a natal-chart validation or a new submitted survey.</p></article>"
            )
            staged = guide.with_name(guide.name + ".pending")
            staged.write_text(existing.replace("</body>", block + "</body>"))
            os.replace(staged, guide)
            changed = True
        assert relative in guide.read_text()
    return {
        "report_installed": True,
        "guide_link_present": guide.exists() and relative in guide.read_text(),
        "guide_modified": changed,
        **output,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-source", required=True, type=Path)
    parser.add_argument("--downloads", required=True, type=Path)
    args = parser.parse_args()
    print(install(args.private_source, args.downloads))
