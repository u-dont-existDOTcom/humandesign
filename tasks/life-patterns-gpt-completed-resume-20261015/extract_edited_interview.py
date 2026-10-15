"""Source-preserving, chart-blind DOCX Q/A extraction for an older Life Patterns interview.

A lightly edited document is not a verbatim original transcript. Output is
source-only and explicitly UNCONSENTED/UNFROZEN, never a ready Action request.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
QUESTION_NUMBER = re.compile(r"^\s*(\d+)\.\s+(.+?)\s*$")
SOURCE_SCHEMA = "life-patterns-edited-interview-source-only-v1"
CHART_MARKERS = re.compile(
    r"\b(date of birth|birth time|born on|natal chart|astrology chart|human design profile)\b",
    re.IGNORECASE,
)


def docx_paragraphs(path: Path) -> list[tuple[str, str]]:
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    records: list[tuple[str, str]] = []
    for node in root.iter(W + "p"):
        pstyle = node.find("./" + W + "pPr/" + W + "pStyle")
        style = pstyle.attrib.get(W + "val", "Normal") if pstyle is not None else "Normal"
        chunks: list[str] = []
        for leaf in node.iter():
            if leaf.tag == W + "t":
                chunks.append(leaf.text or "")
            elif leaf.tag in (W + "tab",):
                chunks.append("\t")
            elif leaf.tag in (W + "br", W + "cr"):
                chunks.append("\n")
        records.append((style, "".join(chunks).strip()))
    return records


def extract(path: Path, *, expected: int | None = None) -> dict[str, Any]:
    paras = docx_paragraphs(path)
    titles = [value for style, value in paras if style == "Title"]
    editorial = next(
        (value for style, value in paras if style == "Normal" and "edited" in value.lower()),
        None,
    )
    if not editorial:
        raise ValueError("Edited-document provenance note not found; inspect document manually")
    current_section = ""
    turns: list[dict[str, Any]] = []
    for style, value in paras:
        if style == "Heading1":
            current_section = value
        elif style == "Question":
            match = QUESTION_NUMBER.fullmatch(value)
            if not match:
                raise ValueError("Unnumbered/ambiguous question in source")
            ordinal = int(match.group(1))
            if ordinal != len(turns) + 1:
                raise ValueError("Numbering gap, duplicate or ordering error")
            turns.append(
                {
                    "turn_id": f"edited-docx-q{ordinal:04d}",
                    "source_question_number": ordinal,
                    "source_section": current_section,
                    "question_text": match.group(2),
                    "answer_text": None,
                    "canonical_question_id": None,
                    "source_kind": "edited_interview_document_not_original_chat",
                }
            )
        elif style == "Answer":
            if not turns or turns[-1]["answer_text"] is not None or not value:
                raise ValueError("Orphan, duplicate or blank answer")
            turns[-1]["answer_text"] = value
    if expected is not None and len(turns) != expected:
        raise ValueError("Expected source-count mismatch; do not make up missing answers")
    if not turns or any(not t["answer_text"] for t in turns):
        raise ValueError("Missing source answers")
    if CHART_MARKERS.search("\n".join(x for _, x in paras)):
        raise ValueError(
            "Potential birth/chart leakage in source; separate target information first"
        )
    return {
        "schema": SOURCE_SCHEMA,
        "source_document_title": titles[0] if titles else "",
        "source_kind": "lightly_edited_interview_document_not_verbatim_chat",
        "source_editorial_notice": editorial,
        "source_file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "question_and_answer_count": len(turns),
        "consent": {
            "research_use_consented": None,
            "reason": (
                "Participant consent cannot be reconstructed from an edited "
                "question/answer document"
            ),
        },
        "original_interviewer_birth_blinding": "unknown_from_this_document",
        "freeze": {
            "state": "unfrozen_source_only_not_reviewed",
            "frozen_before_birth_or_chart_reveal": False,
        },
        "turns": turns,
        "allowed_next_step": (
            "Verify research consent in the participant's authorized chat; recover old "
            "review if already present; otherwise request independent chart-blind "
            "source-wide review and ask only admitted nonredundant clarifications."
        ),
    }


def write_private(output: Path, data: dict[str, Any]) -> None:
    output.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
    fd = os.open(output, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main() -> None:
    cli = argparse.ArgumentParser()
    cli.add_argument("--source", type=Path, required=True)
    cli.add_argument("--private-output", type=Path, required=True)
    cli.add_argument("--expect", type=int)
    args = cli.parse_args()
    result = extract(args.source, expected=args.expect)
    write_private(args.private_output, result)
    print(
        json.dumps(
            {
                "schema": result["schema"],
                "qa_count": len(result["turns"]),
                "source_is_edited": True,
                "consent_known": False,
                "birth_data_included": False,
                "output_permissions": "0600",
            }
        )
    )


if __name__ == "__main__":
    main()
