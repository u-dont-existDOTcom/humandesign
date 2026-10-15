"""Idempotently link local/private V3.2 artifacts into the existing owner researcher guide."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ARTICLE = (
    '<article><h2><a href="Life-Patterns-V32-PRIVATE-2026-10-15.html">'
    "V3.2 revised questionnaire (private and prefilled)</a></h2>"
    "<p>Eight newly worded cognitive prompts, your 25 original V3 answers, "
    "three unusual behaviors and all completed guided context preserved. "
    "The revised wording is development-only and not chart-scored. "
    'See <a href=".life-patterns-private-v32-20261015/'
    'Life-Patterns-V32-vs-V3-vs-Old-PRIVATE.html">'
    "private comparison to your historical survey and DOB scoring results</a>.</p></article>"
)


def install(guide: Path, local_dir: Path) -> str:
    expected = [
        local_dir / "Life-Patterns-V32-PRIVATE-2026-10-15.html",
        local_dir
        / ".life-patterns-private-v32-20261015"
        / "Life-Patterns-V32-vs-V3-vs-Old-PRIVATE.html",
    ]
    for p in expected:
        if not p.is_file():
            raise FileNotFoundError(str(p))
    html = guide.read_text(encoding="utf-8")
    if ARTICLE in html:
        return "ALREADY_INSTALLED"
    if "Life-Patterns-V32-PRIVATE-2026-10-15.html" in html:
        raise RuntimeError("Found conflicting V3.2 guide entry; manual review needed")
    if html.count("</body>") != 1:
        raise RuntimeError("Guide closing tag not found exactly once")
    backup = guide.with_name("." + guide.name + ".pre-v32-20261015.bak")
    if not backup.exists():
        shutil.copy2(guide, backup)
        backup.chmod(0o600)
    guide.write_text(html.replace("</body>", ARTICLE + "</body>", 1), encoding="utf-8")
    assert ARTICLE in guide.read_text()
    return "GUIDE_LINK_ADDED"


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    download = Path.home() / "Téléchargements"
    p.add_argument("--guide", type=Path, default=download / "Life-Patterns-Researcher-Guide.html")
    p.add_argument("--local-dir", type=Path, default=download)
    args = p.parse_args()
    print(install(args.guide, args.local_dir))
