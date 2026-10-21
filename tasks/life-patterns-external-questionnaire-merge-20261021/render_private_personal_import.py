"""Render new ODG responses in a private, unscored personal evidence ledger.

No private outputs in Git. No scored conclusions from self-reported outcomes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


def render(master: dict) -> str:
    if master.get("schema") != "life-patterns-private-personal-survey-source-stack-v2":
        raise ValueError("Wrong personal source identity.")
    source = master["external_blinded_questionnaire_addendum"]
    if len(source.get("responses", [])) != 31:
        raise ValueError("The 31 source questions are incomplete.")
    lines = [
        "# Personal Life Patterns survey — appended external questionnaire",
        "",
        "Private readable source. Not an astrology prediction validation report.",
        "Earlier V3.3, 84-turn interview, 3 CF003 answers and 8 EM answers",
        "remain unmodified and independently preserved in the master JSON.",
        "",
        "Missing/unclear and future unanswered are not false responses.",
        "Repeated accounts of the same event are not independent support.",
        "The printed freeze time has not been verified against a separate prediction JSON.",
        "",
        "## Thirty-one questions and observed response states",
        "",
    ]
    for q in source["responses"]:
        lines.extend(
            [
                "### " + q["id"] + " — " + q["state"],
                "",
                q["question"],
                "",
                q["reference_window"],
                "",
                "**Selected label:** "
                + (
                    q["marked_choice"]
                    if q.get("marked_choice") is not None
                    else "No answer marked, future outcome pending"
                ),
                "",
                "**Original respondent clarification:** "
                + (q.get("extracted_note") or "(none supplied)"),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def save(master_path: Path, output: Path) -> dict:
    source = json.loads(master_path.read_bytes())
    text = render(source)
    if output.exists():
        raise FileExistsError(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(output, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    return {
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "bytes": output.stat().st_size,
        "questions": text.count("### Q"),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--master", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(save(args.master, args.output), sort_keys=True))
