"""Read source-bound II.1-II.2 definitions and records; never classify people.

This module accepts only source identifiers and chapter-note contexts, not birth
coordinates, nationalities, names or observed personal outcomes. It is a research
reference reader, not an executable version of Ptolemy's physical theory.
"""
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
_TABLES = json.loads((HERE / "GENERAL_CONTEXT_TABLES.json").read_text(encoding="utf-8"))
_RECORDS = json.loads((HERE / "RULES.json").read_text(encoding="utf-8"))["records"]
_BY_ID = {row["id"]: row for row in _RECORDS}


def _key(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a nonempty exact source key")
    return value


def definition(term: str, context: str) -> dict[str, Any]:
    """Retrieve a definition only in its explicitly requested source context.

    Unknown contexts are not filled with another chapter's use of the same word.
    """
    term, context = _key(term, "term"), _key(context, "context")
    for row in _TABLES["glossary"]:
        if row["term"] == term and row["context"] == context:
            return deepcopy(row)
    raise KeyError(f"No extracted definition for {term!r} in {context!r}")


def source_record(record_id: str) -> dict[str, Any]:
    """Retrieve a historical statement, keeping its attribution and limitations."""
    record_id = _key(record_id, "record_id")
    if record_id not in _BY_ID:
        raise KeyError(f"Unknown B01o record: {record_id}")
    return deepcopy(_BY_ID[record_id])


def general_inquiry_axes() -> dict[str, Any]:
    """Return separate spatial and circumstance axes, including the variant."""
    return deepcopy(_TABLES["general_enquiry_axes"])
