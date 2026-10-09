"""Install a one-click local index for the Life Patterns researcher's question atlas.

The atlas and a separate report of participant answers are already produced by
research workflows. This script does not invent questions, derive traits, or
copy private responses into Git. It only links verified local files.
"""

from __future__ import annotations

import argparse
import subprocess
from html import escape
from pathlib import Path
from urllib.parse import quote

ATLAS_FOLDER = "Life-Patterns-Full-Question-Interpretation-Guide-2026-10-09"
ATLAS_NAME = "All-Questions-and-How-Answers-Are-Interpreted.html"
ANSWERS_NAME = "Life-Patterns-My-84-Answers-and-Interpretations-2026-10-09.html"
MAPPING_NAME = "Old-vs-Current-Survey-Birth-Mapping-Assessment.md"
INDEX_NAME = "Life-Patterns-Researcher-Guide.html"
DESKTOP_NAME = "life-patterns-question-guide.desktop"


def default_downloads() -> Path:
    try:
        candidate = subprocess.check_output(
            ["xdg-user-dir", "DOWNLOAD"], text=True, timeout=6
        ).strip()
        if candidate:
            return Path(candidate).expanduser()
    except (OSError, subprocess.SubprocessError):
        pass
    return Path.home() / "Downloads"


def make_guide(downloads: Path, applications: Path) -> tuple[Path, Path]:
    entries = [
        (
            "All questions and what they measure",
            Path(ATLAS_FOLDER) / ATLAS_NAME,
            "Search 79 historical questions, 25 current questions, and 25 proposed "
            "versions, with behavioral dimensions, coding examples, and limits.",
        ),
        (
            "Your 84 answers and reviewer interpretations",
            Path(ANSWERS_NAME),
            "Inspect the full responses and the independent review's supported "
            "findings and source quotations.",
        ),
        (
            "Old-versus-current survey birth-mapping assessment",
            Path(ATLAS_FOLDER) / MAPPING_NAME,
            "Understand data overlap and why this cannot serve as a new "
            "independent confirmation of birth-time matching.",
        ),
    ]
    for _, relative, _ in entries:
        if not (downloads / relative).is_file():
            raise FileNotFoundError(downloads / relative)
    cards = "\n".join(
        '<article><h2><a href="'
        + quote(relative.as_posix(), safe="/")
        + '">'
        + escape(title)
        + "</a></h2><p>"
        + escape(description)
        + "</p></article>"
        for title, relative, description in entries
    )
    html = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>Life Patterns — Questions and Interpretations</title>"
        "<style>body{font:16px/1.55 system-ui;max-width:850px;"
        "margin:3rem auto;padding:0 1rem}"
        "article{border:1px solid #ccd2d9;border-radius:12px;"
        "margin:1rem 0;padding:1.1rem 1.5rem}"
        "h1{font-size:1.8rem}h2{font-size:1.15rem}a{color:#245a92}"
        "</style></head><body>"
        "<h1>Life Patterns: Questions, Traits &amp; Interpretations</h1>"
        "<p>These are research questions, not diagnostic tests or proof "
        "of a stable trait. Some historical prompts have no single trait "
        "target; proposed v2 wording is not yet live.</p>" + cards + "</body></html>"
    )
    index = downloads / INDEX_NAME
    index.write_text(html, encoding="utf-8")
    index.chmod(0o600)
    applications.mkdir(parents=True, exist_ok=True)
    desktop = applications / DESKTOP_NAME
    # The generated filename is fixed and contains no whitespace.
    desktop.write_text(
        "[Desktop Entry]\nType=Application\n"
        "Name=Life Patterns Questions and Interpretations\n"
        "Comment=Browse question text, intended distinctions and interpretations\n"
        f'Exec=/usr/bin/xdg-open "{index}"\n'
        "Terminal=false\nStartupNotify=true\n"
        "Categories=Education;\nIcon=accessories-text-editor\n",
        encoding="utf-8",
    )
    desktop.chmod(0o644)
    return index, desktop


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--downloads", type=Path, default=default_downloads())
    parser.add_argument(
        "--applications",
        type=Path,
        default=Path.home() / ".local/share/applications",
    )
    args = parser.parse_args()
    index, desktop = make_guide(args.downloads, args.applications)
    print(f"Question guide: {index}\nApplication entry: {desktop}")


if __name__ == "__main__":
    main()
