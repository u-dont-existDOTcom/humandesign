"""Install the private V3.3 role-entry launcher in the local researcher guide."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "LIFE_PATTERNS_V33_ROLE_ENTRY_OFFLINE_PILOT.html"
ARTICLE = (
    '<article><h2><a href="Life-Patterns-V33-Role-Entry-PRIVATE-2026-10-15.html">'
    "Answer the missing group-role question (V3.3, private)</a></h2>"
    "<p>Your 25 original answers and eight contextual follow-ups are preloaded. "
    "The only requested new evidence concerns whether you normally take meaningful "
    "roles by initiating them, by invitation, by assignment or depending on context. "
    "One optional guided module, with real examples, skip and export. Not birth-chart scored. "
    'The <a href=".life-patterns-private-v32-20261015/'
    'Life-Patterns-V32-vs-V3-vs-Old-PRIVATE.html">corrected comparison report</a> '
    "uses the accepted V1.4d joint-first reference rather than the discarded V4.3 benchmark."
    "</p></article>"
)


def install(guide: Path, downloads: Path) -> str:
    private = downloads / "Life-Patterns-V33-Role-Entry-PRIVATE-2026-10-15.html"
    report = (
        downloads
        / ".life-patterns-private-v32-20261015"
        / "Life-Patterns-V32-vs-V3-vs-Old-PRIVATE.html"
    )
    if not private.is_file() or not report.is_file():
        raise FileNotFoundError("Private V3.3 questionnaire or corrected report missing")
    if private.stat().st_mode & 0o777 != 0o600:
        raise PermissionError("Private source is not mode 0600")
    clean = downloads / "Life-Patterns-V33-Role-Entry-Blank-2026-10-15.html"
    if not clean.exists() or clean.read_bytes() != SOURCE.read_bytes():
        shutil.copy2(SOURCE, clean)
    clean.chmod(0o600)
    text = guide.read_text()
    if ARTICLE in text:
        return "ALREADY_INSTALLED"
    if private.name in text:
        raise RuntimeError("Conflicting role-entry guide entry")
    if text.count("</body>") != 1:
        raise RuntimeError("Malformed guide")
    backup = downloads / ".Life-Patterns-Researcher-Guide.pre-v33-20261015.html"
    if not backup.exists():
        shutil.copy2(guide, backup)
        backup.chmod(0o600)
    guide.write_text(text.replace("</body>", ARTICLE + "</body>", 1))
    assert ARTICLE in guide.read_text()
    return "INSTALLED_AND_VERIFIED"


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    d = Path.home() / "Téléchargements"
    p.add_argument("--guide", type=Path, default=d / "Life-Patterns-Researcher-Guide.html")
    p.add_argument("--downloads", type=Path, default=d)
    options = p.parse_args()
    print(install(options.guide, options.downloads))
