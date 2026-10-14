"""Link an already verified private guided HTML to the owner's local guide."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


def install(guide: Path, private_html: Path) -> dict:
    if not guide.is_file() or not private_html.is_file():
        raise FileNotFoundError("The local guide and private prefilled HTML must both exist")
    # Only same-folder navigation; never expose a private path to an external website.
    if private_html.parent != guide.parent:
        raise ValueError("Private HTML must be beside the owner's researcher guide")
    source = guide.read_text()
    name = private_html.name
    if name not in source:
        item = (
            '<article><h2><a href="' + name + '">Answer my eight context follow-ups</a></h2>'
            "<p>Ready to start: your earlier 25 answers and unusual behaviors are already loaded. "
            "The questions appear one at a time, with Skip/Previous and Export. "
            "Private local research pilot; not the submitted study.</p></article>"
        )
        if "</body>" not in source:
            raise ValueError("Invalid researcher guide, closing body tag absent")
        tmp = guide.with_suffix(".pending")
        tmp.write_text(source.replace("<body>", "<body>" + item, 1))
        os.replace(tmp, guide)
    if name not in guide.read_text():
        raise AssertionError("Linked private questionnaire is unavailable")
    return {"ready": True, "owner_guide_link": True}


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--guide", type=Path, required=True)
    cli.add_argument("--private-html", type=Path, required=True)
    a = cli.parse_args()
    print(install(a.guide, a.private_html))
