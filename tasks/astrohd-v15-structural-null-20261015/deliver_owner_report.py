"""Render verified AstroHD structural-null reports locally and update owner guide.

Only public aggregate research reports are used; no private participant source
is read. Reports are placed directly in the owner's Downloads folder.
"""

from __future__ import annotations

import argparse
import html
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUTS = {
    "RESULT.md": "AstroHD-V15-Structural-Null-Audit-2026-10-15",
    "NEXT_UNTOUCHED_HUMAN_TEST.md": "AstroHD-V15-Next-Human-Test-2026-10-15",
}
ARTICLE = (
    '<article><h2><a href="AstroHD-V15-Structural-Null-Audit-2026-10-15.html">'
    "New analysis: why a first-place birth-date score may be automatic</a></h2>"
    "<p>Exact five-domain control enumeration, the frozen 9,999-date null test "
    "and the corrected interpretation of the previous first-place score. "
    '<a href="AstroHD-V15-Next-Human-Test-2026-10-15.html">'
    "Independent new-participant test protocol</a>. "
    "The previously completed owner questionnaire requires no new answer.</p></article>"
)


def report_html(title: str, markdown: str) -> str:
    try:
        from markdown_it import MarkdownIt
    except ImportError:
        body = "<pre>" + html.escape(markdown) + "</pre>"
    else:
        body = MarkdownIt("commonmark", {"html": False}).enable("table").render(markdown)
    stylesheet = (
        "body{font:16px/1.55 system-ui,sans-serif;color:#222d39;max-width:930px;"
        "margin:auto;padding:1.25rem 1.2rem 5rem}h1{font-size:1.7rem}h2{font-size:1.25rem}"
        "table{width:100%;border-collapse:collapse;display:block;overflow-x:auto}"
        "td,th{border:1px solid #c5ced8;padding:.5rem;white-space:normal}"
        "pre,code{white-space:pre-wrap;overflow-wrap:anywhere}code{font-size:.9em}"
        "a{text-decoration:underline}p,li{max-width:80ch}@media(max-width:540px)"
        "{body{font-size:15px;padding:.9rem}}"
    )
    return (
        "<!doctype html><html lang='en'><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>" + html.escape(title) + "</title>"
        "<style>" + stylesheet + "</style><main>" + body + "</main></html>"
    )


def write_new(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(content)
    path.chmod(0o600)
    if path.read_text(encoding="utf-8") != content:
        raise RuntimeError("Local owner delivery bytes did not match intended content")


def deliver(downloads: Path, *, update_guide: bool) -> list[Path]:
    delivered = []
    for filename, prefix in OUTPUTS.items():
        markdown = (HERE / filename).read_text(encoding="utf-8")
        md_path = downloads / (prefix + ".md")
        html_path = downloads / (prefix + ".html")
        write_new(md_path, markdown)
        write_new(html_path, report_html(prefix, markdown))
        delivered.extend((md_path, html_path))
    if update_guide:
        guide = downloads / "Life-Patterns-Researcher-Guide.html"
        previous = guide.read_text(encoding="utf-8")
        if ARTICLE not in previous:
            if previous.count("<body>") != 1:
                raise ValueError("Cannot identify one owner guide body anchor")
            backup = downloads / ".Life-Patterns-Researcher-Guide.pre-v15-null-20261015.html"
            if not backup.exists():
                shutil.copy2(guide, backup)
                backup.chmod(0o600)
            replaced = previous.replace("<body>", "<body>" + ARTICLE, 1)
            write_new(guide, replaced)
        if ARTICLE not in guide.read_text(encoding="utf-8"):
            raise RuntimeError("Local guide link not verified")
    return delivered


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--downloads", type=Path, default=Path.home() / "Téléchargements")
    parser.add_argument("--no-guide", action="store_true")
    args = parser.parse_args()
    paths = deliver(args.downloads, update_guide=not args.no_guide)
    print("DELIVERED_FILES", [p.name for p in paths])
