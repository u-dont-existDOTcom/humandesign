#!/usr/bin/env python3
"""Build a chart-blind CF-003 behavioral-classifier packet from frozen source.

The output intentionally excludes the evaluator-only construct-to-planet mapping,
birth/chart metadata, CF-003 predictor values, and astrology labels. It contains
only behavioral source turns, the neutral construct contract, and provenance hashes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

DEFAULT_CONTRACT = Path(
    "reference/empirical_astrology/cf003_behavioral_classifier_contract_v0.json"
)
DEFAULT_PROMPT = Path("reference/empirical_astrology/cf003_behavioral_classifier_prompt_v0.md")

LEAKAGE_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bbirth\s+chart\b",
        r"\bnatal\s+chart\b",
        r"\bascendant\b",
        r"\brising\s+sign\b",
        r"\bsun\s+sign\b",
        r"\bmoon\s+sign\b",
        r"\bhuman\s+design\b",
        r"\bCF-?003\b",
        r"\bdominant\s+planet\b",
    )
)


def _duplicate_guard(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(), object_pairs_hook=_duplicate_guard)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_turns(record: dict[str, Any], *, source_label: str) -> list[dict[str, Any]]:
    raw_turns = record.get("turns")
    if not isinstance(raw_turns, list):
        raise ValueError(f"{source_label} must contain a turns list")

    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_turns, 1):
        if not isinstance(raw, dict):
            continue
        if raw.get("turn_role", "behavioral") != "behavioral" or raw.get("quarantined"):
            continue
        question = raw.get("question_text")
        answer = raw.get("answer_text")
        if not isinstance(question, str) or not isinstance(answer, str):
            continue
        turn_id = str(raw.get("turn_id") or f"{source_label}-{index:04d}")
        if turn_id in seen:
            raise ValueError(f"duplicate turn_id across behavioral source: {turn_id}")
        seen.add(turn_id)

        for pattern in LEAKAGE_PATTERNS:
            if pattern.search(question) or pattern.search(answer):
                raise ValueError(
                    f"possible chart/target leakage in {turn_id}: pattern {pattern.pattern!r}"
                )

        card: dict[str, Any] = {
            "turn_id": turn_id,
            "question_text": question,
            "answer_text": answer,
        }
        for key in (
            "canonical_question_id",
            "question_wording_status",
            "correction_of",
            "conditions",
            "corrections",
            "process_feedback",
            "is_review_correction",
        ):
            value = raw.get(key)
            if value not in (None, [], {}, "", False):
                card[key] = value
        out.append(card)
    return out


def build_packet(
    source_path: Path,
    contract_path: Path,
    *,
    prompt_path: Path = DEFAULT_PROMPT,
    secondary_path: Path | None = None,
) -> dict[str, Any]:
    source_bytes = source_path.read_bytes()
    source = load_json(source_path)
    contract = load_json(contract_path)
    prompt_text = prompt_path.read_text()

    turns = source_turns(source, source_label="primary")
    secondary_hash = None
    if secondary_path is not None:
        secondary_bytes = secondary_path.read_bytes()
        secondary = load_json(secondary_path)
        secondary_turns = source_turns(secondary, source_label="secondary")
        existing = {turn["turn_id"] for turn in turns}
        if existing.intersection(turn["turn_id"] for turn in secondary_turns):
            raise ValueError("primary and secondary source turn IDs must be disjoint")
        turns.extend(secondary_turns)
        secondary_hash = sha256_bytes(secondary_bytes)

    if not turns:
        raise ValueError("no usable behavioral source turns")

    # Defense in depth: classifier-facing contract must not contain planet labels.
    contract_text = (json.dumps(contract, ensure_ascii=False) + "\n" + prompt_text).lower()
    planet_names = {
        "sun",
        "moon",
        "mercury",
        "venus",
        "mars",
        "jupiter",
        "saturn",
        "uranus",
        "neptune",
        "pluto",
    }
    leaked_names = sorted(
        name for name in planet_names if re.search(rf"\b{re.escape(name)}\b", contract_text)
    )
    if leaked_names:
        raise ValueError("classifier contract leaks evaluator labels: " + ", ".join(leaked_names))

    return {
        "schema_version": "cf003-behavioral-classifier-packet-v0",
        "scientific_status": "development_secondary_chart_blind",
        "instructions": [
            "Use only this packet in a fresh tool-free context.",
            "Do not use repository access, web, Memory, connected apps, or other files.",
            "Do not retrieve or infer birth/chart/astrology information.",
            "Apply the neutral ten-construct contract exactly.",
            "Source quote fields must be exact contiguous substrings of answer_text.",
            "Return null rather than force a rating when evidence is insufficient.",
            "Do not infer construct-to-astrology mappings.",
        ],
        "classifier_prompt": prompt_text,
        "contract": contract,
        "source": {
            "primary_sha256": sha256_bytes(source_bytes),
            "secondary_sha256": secondary_hash,
            "contract_sha256": sha256_bytes(contract_path.read_bytes()),
            "prompt_sha256": sha256_bytes(prompt_path.read_bytes()),
            "turn_count": len(turns),
            "source_fidelity": source.get("source_fidelity", "unknown"),
            "collection_mode": source.get("collection_mode", "unknown"),
        },
        "turns": turns,
        "forbidden_context": [
            "birth data",
            "chart data",
            "astrology or Human Design labels",
            "CF-003 predictor scores or ranks",
            "construct-to-planet mapping",
            "prior chart interpretation or expected target",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--secondary", type=Path)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    packet = build_packet(
        args.source.resolve(),
        args.contract.resolve(),
        prompt_path=args.prompt.resolve(),
        secondary_path=args.secondary.resolve() if args.secondary else None,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote chart-blind packet with {len(packet['turns'])} turns to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
