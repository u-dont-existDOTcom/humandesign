"""Deliver only non-live research artifacts to the owner's existing guide."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ATLAS = ROOT / "tasks/survey-recovery-autonomy-20261009/question-atlas.html"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def downloads() -> Path:
    try:
        name = subprocess.check_output(["xdg-user-dir", "DOWNLOAD"], text=True, timeout=5).strip()
        if name:
            return Path(name)
    except (OSError, subprocess.SubprocessError):
        pass
    return Path.home() / "Downloads"


def deliver(base: Path, *, existing_atlas_path: Path | None = None) -> dict:
    folder = base / "Life-Patterns-Idiographic-Pilot-2026-10-10"
    folder.mkdir(parents=True, exist_ok=True)
    names = [
        "LIFE_PATTERNS_V3_OFFLINE_PILOT.html",
        "DESIGN_AND_VALIDATION.md",
        "tendency-first-v3-scaffold-development.json",
        "unusual-behavior-inventory-v0.json",
        "scoped_recognition_ownership_and_solitude-v0.json",
    ]
    for name in names:
        shutil.copy2(HERE / name, folder / name)
    guide = base / "Life-Patterns-Researcher-Guide.html"
    link = "Life-Patterns-Idiographic-Pilot-2026-10-10/LIFE_PATTERNS_V3_OFFLINE_PILOT.html"
    card = (
        '<article><h2><a href="' + link + '">'
        "Experimental guided answers and unusual-behavior inventory (not live)"
        "</a></h2><p>Try 25 example-supported question sets, a separate solitude question,"
        " and a voluntary inventory of distinctive behaviors. No data are transmitted."
        " The historical recognition and ownership interpretation is now split for"
        " clarity in the question atlas.</p></article>"
    )
    index_changed = False
    if guide.is_file():
        text = guide.read_text()
        if link not in text:
            assert "</body>" in text
            temporary = guide.with_name(guide.name + ".tmp")
            temporary.write_text(text.replace("</body>", card + "</body>"))
            os.replace(temporary, guide)
            index_changed = True
    atlas_destination = existing_atlas_path or (
        base
        / "Life-Patterns-Full-Question-Interpretation-Guide-2026-10-09"
        / "All-Questions-and-How-Answers-Are-Interpreted.html"
    )
    atlas_updated = False
    if atlas_destination.is_file() and digest(atlas_destination) != digest(ATLAS):
        backup = atlas_destination.with_name("All-Questions-Previous-Generated-2026-10-10.html")
        if not backup.exists():
            shutil.copy2(atlas_destination, backup)
        shutil.copy2(ATLAS, atlas_destination)
        atlas_updated = True
    return {
        "folder": str(folder),
        "files": len(names),
        "landing_entry_present": guide.exists() and link in guide.read_text(),
        "landing_changed": index_changed,
        "current_atlas_updated": atlas_updated,
        "question_pilot_hashes_match": all(
            digest(folder / name) == digest(HERE / name) for name in names
        ),
        "atlas_hash_matches": not atlas_destination.exists()
        or digest(atlas_destination) == digest(ATLAS),
        "no_live_server_deploy": True,
    }


if __name__ == "__main__":
    print(json.dumps(deliver(downloads()), indent=2))
