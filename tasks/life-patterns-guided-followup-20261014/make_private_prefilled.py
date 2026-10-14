"""Create an OWNER-PRIVATE offline follow-up file from an existing V3 export.

Never commit the resulting HTML; it embeds personal source responses.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def prefill(source_html: Path, source_json: Path, destination: Path) -> dict:
    html = source_html.read_text(encoding="utf-8")
    stored = json.loads(source_json.read_text(encoding="utf-8"))
    if stored.get("schema") != "local_life_patterns_v3_pilot_unsubmitted":
        raise ValueError("Expected a compatible local V3 pilot export")
    if not isinstance(stored.get("answers"), dict) or len(stored["answers"]) != 25:
        raise ValueError("Expected 25 answered routes, cannot safely prefill")
    if not isinstance(stored.get("unique_behaviors"), list):
        raise ValueError("Expected the optional unusual-behavior list")
    opening = '<script id="pilot-data" type="application/json">'
    start = html.index(opening) + len(opening)
    end = html.index("</script>", start)
    data = json.loads(html[start:end])
    if not isinstance(data.get("questions"), list) or len(data["questions"]) != 25:
        raise ValueError("Invalid public pilot question bank")
    ids = {q["id"] for q in data["questions"]}
    if set(stored["answers"]) != ids:
        raise ValueError("Saved answer routes do not match the pilot questions")
    options = {q["id"]: set(q["example_answer_paths"]) for q in data["questions"]}
    for route, record in stored["answers"].items():
        if not isinstance(record, dict) or not isinstance(record.get("selected"), list):
            raise ValueError(f"Malformed answer for {route}")
        if not all(
            isinstance(choice, str) and choice in options[route] for choice in record["selected"]
        ):
            raise ValueError(f"Unrecognized answer choice for {route}")
    data["prefilled_export"] = stored
    # Encode hostile markup as JSON escapes so personal free text cannot close the script.
    encoded = (
        json.dumps(data, ensure_ascii=False)
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )
    html = html[:start] + encoded + html[end:]
    html = html.replace(
        "</header>",
        '<p class="notice"><strong>Private prefilled file:</strong> this copy contains your saved answers. Do not share this HTML file. Nothing is transmitted; download an updated JSON after your follow-ups.</p></header>',
        1,
    )
    destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as out:
        out.write(html)
    destination.chmod(0o600)
    assert "prefilled_export" in destination.read_text()
    return {
        "ready": True,
        "questions": len(stored["answers"]),
        "behavior_items": len(stored["unique_behaviors"]),
        "file_mode": "0600",
    }


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--html", type=Path, required=True)
    cli.add_argument("--source", type=Path, required=True)
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    print(prefill(args.html, args.source, args.output))
