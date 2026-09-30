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

SIGN_NAMES = (
    "aries|taurus|gemini|cancer|leo|virgo|libra|scorpio|sagittarius|capricorn|aquarius|pisces"
)
PLANET_NAMES = "mercury|venus|mars|jupiter|saturn|uranus|neptune|pluto"

LEAKAGE_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bastrolog(?:y|er|ical)\b",
        r"\bhoroscope\b",
        r"\bzodiac\b",
        r"\b(?:birth|natal)\s+chart\b",
        r"\bmy\s+chart\b",
        r"\bascendant\b",
        r"\brising(?:\s+sign)?\b",
        r"\b(?:sun|moon)\s+sign\b",
        rf"\b(?:{SIGN_NAMES})\s+(?:rising|sun|moon)\b",
        rf"\btypical\s+(?:{SIGN_NAMES})\b",
        rf"\b(?:sun|moon|{PLANET_NAMES})\s+(?:is\s+)?in\s+(?:{SIGN_NAMES})\b",
        r"\bsaturn\s+return\b",
        rf"\b(?:{PLANET_NAMES})\b",
        r"\bhuman\s+design\b",
        r"\b(?:projector|manifestor|manifesting\s+generator|generator|reflector)\b",
        r"\b\d\s*/\s*\d\s+profile\b",
        r"\bCF-?003\b",
        r"\bdominant\s+planet\b",
    )
)

FORBIDDEN_RECORD_KEY = re.compile(
    r"(?:^|_)(?:birth(?:_?date|_?time|_?place)?|chart|planet|predictor|"
    r"astrolog(?:y|ical)|zodiac|human_?design)(?:_|$)",
    re.IGNORECASE,
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


def _reject_forbidden_record_keys(value: Any, *, path: str = "record") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            if FORBIDDEN_RECORD_KEY.search(key_text):
                raise ValueError(f"source contains forbidden profile field at {path}.{key_text}")
            _reject_forbidden_record_keys(child, path=f"{path}.{key_text}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_forbidden_record_keys(child, path=f"{path}[{index}]")


def _scan_classifier_strings(value: Any, *, path: str) -> None:
    if isinstance(value, str):
        for pattern in LEAKAGE_PATTERNS:
            if pattern.search(value):
                raise ValueError(
                    "possible external-profile leakage requiring chart-blind redaction "
                    f"at {path}: pattern {pattern.pattern!r}"
                )
    elif isinstance(value, dict):
        for key, child in value.items():
            _scan_classifier_strings(child, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _scan_classifier_strings(child, path=f"{path}[{index}]")


def _check_record_exposure(record: dict[str, Any], *, source_label: str) -> None:
    blinding = record.get("blinding")
    if not isinstance(blinding, dict):
        return
    notes = blinding.get("contamination_notes")
    if notes not in (None, "", [], {}):
        raise ValueError(f"{source_label} has non-empty contamination_notes")
    result = blinding.get("target_check_result")
    if isinstance(result, str) and result.strip().lower() not in {
        "",
        "pass",
        "clean",
        "no_exposure",
        "not_exposed",
    }:
        raise ValueError(f"{source_label} has non-clean target_check_result: {result!r}")


def source_turns(record: dict[str, Any], *, source_label: str) -> list[dict[str, Any]]:
    raw_turns = record.get("turns")
    if not isinstance(raw_turns, list):
        raise ValueError(f"{source_label} must contain a turns list")

    out: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_turns, 1):
        if not isinstance(raw, dict):
            raise ValueError(f"{source_label} turn {index} must be an object")
        if "turn_role" not in raw:
            raise ValueError(f"{source_label} turn {index} is missing explicit turn_role")
        if raw.get("turn_role") != "behavioral" or raw.get("quarantined"):
            continue

        question = raw.get("question_text")
        answer = raw.get("answer_text")
        if not isinstance(question, str) or not isinstance(answer, str):
            raise ValueError(
                f"{source_label} behavioral turn {index} needs string question_text and answer_text"
            )

        card: dict[str, Any] = {
            "turn_id": f"{source_label}-{len(out) + 1:04d}",
            "question_text": question,
            "answer_text": answer,
        }
        for key in ("conditions", "corrections", "process_feedback"):
            value = raw.get(key)
            if value not in (None, [], {}, "", False):
                card[key] = value

        _scan_classifier_strings(card, path=f"{source_label}.turns[{index - 1}]")
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

    _reject_forbidden_record_keys(source, path="primary")
    _check_record_exposure(source, source_label="primary")
    turns = source_turns(source, source_label="primary")
    primary_hash = sha256_bytes(source_bytes)

    secondary_hash = None
    if secondary_path is not None:
        secondary_bytes = secondary_path.read_bytes()
        secondary = load_json(secondary_path)
        _reject_forbidden_record_keys(secondary, path="secondary")
        _check_record_exposure(secondary, source_label="secondary")
        if secondary.get("primary_record_sha256") != primary_hash:
            raise ValueError("secondary source must carry the exact primary_record_sha256 linkage")
        turns.extend(source_turns(secondary, source_label="secondary"))
        secondary_hash = sha256_bytes(secondary_bytes)

    if not turns:
        raise ValueError("no usable behavioral source turns")

    classifier_material = {"contract": contract, "prompt": prompt_text}
    _scan_classifier_strings(classifier_material, path="classifier_material")
    contract_text = (json.dumps(contract, ensure_ascii=False) + "\n" + prompt_text).lower()
    hidden_label_names = {
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
        name for name in hidden_label_names if re.search(rf"\b{re.escape(name)}\b", contract_text)
    )
    if leaked_names:
        raise ValueError(
            "classifier material leaks hidden evaluator labels: " + ", ".join(leaked_names)
        )

    memory_status = source.get("chatgpt_memory_enabled", source.get("memory_enabled", "unknown"))
    if not isinstance(memory_status, bool):
        memory_status = "unknown"

    return {
        "schema_version": "independent-behavioral-classifier-packet-v0",
        "scientific_status": "development_secondary_independent_behavioral",
        "instructions": [
            "Use only this packet in a fresh tool-free context.",
            "Do not use repository access, web, Memory, connected apps, or other files.",
            "Use no information about the participant beyond the supplied behavioral source.",
            "Apply the neutral ten-construct contract exactly.",
            "Source quote fields must be exact contiguous substrings of answer_text.",
            "Return null rather than force a rating when evidence is insufficient.",
            "Do not infer or reconstruct any hidden framework behind the construct IDs.",
        ],
        "classifier_prompt": prompt_text,
        "contract": contract,
        "source": {
            "primary_sha256": primary_hash,
            "secondary_sha256": secondary_hash,
            "contract_sha256": sha256_bytes(contract_path.read_bytes()),
            "prompt_sha256": sha256_bytes(prompt_path.read_bytes()),
            "turn_count": len(turns),
            "source_fidelity": source.get("source_fidelity", "unknown"),
            "collection_mode": source.get("collection_mode", "unknown"),
            "chatgpt_memory_enabled": memory_status,
        },
        "turns": turns,
        "outside_context_rule": (
            "Any information not contained in the supplied behavioral source and contract "
            "is prohibited."
        ),
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
