#!/usr/bin/env python3
"""Validate and freeze a chart-blind CF-003 behavioral target before prediction reveal."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from hdmatch.empirical_astrology.cf003_target import (
    CF003_CONSTRUCT_TO_PLANET,
    construct_scores_to_planets,
    rank_score_groups,
    validate_behavioral_classifier_result,
)

DEFAULT_MAPPING = Path("reference/empirical_astrology/cf003_behavioral_planet_map_v0.json")


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--classifier-output", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, default=DEFAULT_MAPPING)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    packet = load_object(args.packet)
    classifier = load_object(args.classifier_output)
    mapping = load_object(args.mapping)

    file_mapping = {
        str(row["construct_id"]): str(row["planet"]) for row in mapping.get("mapping", [])
    }
    if file_mapping != dict(CF003_CONSTRUCT_TO_PLANET):
        raise ValueError("evaluator mapping file does not match frozen implementation")

    turns = packet.get("turns")
    if not isinstance(turns, list):
        raise ValueError("classifier packet must contain turns")
    answers = {
        str(turn["turn_id"]): str(turn["answer_text"])
        for turn in turns
        if isinstance(turn, dict)
        and turn.get("turn_id") is not None
        and isinstance(turn.get("answer_text"), str)
    }
    scores = validate_behavioral_classifier_result(
        classifier,
        answer_text_by_turn_id=answers,
    )

    complete = all(score.dominance_rating is not None for score in scores)
    planet_scores = construct_scores_to_planets(scores) if complete else None
    rank_groups = rank_score_groups(planet_scores) if planet_scores is not None else None

    frozen = {
        "schema_version": "cf003-frozen-behavioral-target-v0",
        "scientific_status": "development" if not complete else "development_complete_target",
        "prediction_opened": False,
        "classifier_packet_sha256": sha256(args.packet),
        "classifier_output_sha256": sha256(args.classifier_output),
        "evaluator_mapping_sha256": sha256(args.mapping),
        "source": packet.get("source"),
        "construct_scores": [
            {
                **asdict(score),
                "support_quotes": [asdict(quote) for quote in score.support_quotes],
                "counterevidence_quotes": [asdict(quote) for quote in score.counterevidence_quotes],
            }
            for score in scores
        ],
        "behavioral_target_complete": complete,
        "planet_scores": planet_scores,
        "behavioral_rank_groups": rank_groups,
        "tie_rule": "equal dominance ratings remain tied; no tie-breaker",
        "notes": [
            "This target was frozen without CF-003 predictor scores.",
            "Existing development participants remain exploratory.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(frozen, indent=2, ensure_ascii=False) + "\n")
    print(f"Frozen behavioral target ({'complete' if complete else 'incomplete'}) at {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
