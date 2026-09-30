#!/usr/bin/env python3
"""Freeze CF-003 seven-factor predictor scores before behavioral classification."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from hdmatch.empirical_astrology.cf003 import (
    CF003_CANDIDATE_BODIES,
    CF003_PUBLISHED_WEIGHTS,
    CF003FactorFlags,
    rank_cf003_planet_scores,
    score_cf003_planet,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPEC = ROOT / "reference/empirical_astrology/cf003_published_predictor_spec_v0.json"


def _duplicate_guard(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(), object_pairs_hook=_duplicate_guard)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--factor-flags", type=Path, required=True)
    parser.add_argument("--predictor-spec", type=Path, default=DEFAULT_SPEC)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source = load_object(args.factor_flags)
    load_object(args.predictor_spec)
    if source.get("schema_version") != "cf003-factor-flags-v0":
        raise ValueError("factor-flags file must use cf003-factor-flags-v0")
    convention_id = source.get("factor_extraction_convention_id")
    if not isinstance(convention_id, str) or not convention_id.strip():
        raise ValueError("factor_extraction_convention_id is required")
    historical = source.get("exact_historical_mastro_factor_extraction_reproduced")
    if not isinstance(historical, bool):
        raise ValueError("exact_historical_mastro_factor_extraction_reproduced must be boolean")
    raw_flags = source.get("factor_flags")
    if not isinstance(raw_flags, dict) or set(raw_flags) != set(CF003_CANDIDATE_BODIES):
        raise ValueError("factor_flags must contain exactly the ten CF-003 candidate bodies")

    expected_flag_names = set(CF003_PUBLISHED_WEIGHTS)
    planet_scores: dict[str, float] = {}
    contributions: dict[str, list[list[object]]] = {}
    for body in CF003_CANDIDATE_BODIES:
        row = raw_flags[body]
        if not isinstance(row, dict) or set(row) != expected_flag_names:
            raise ValueError(f"{body} must contain exactly the seven published factor flags")
        flags = CF003FactorFlags(**row)
        scored = score_cf003_planet(body, flags)
        planet_scores[body] = scored.total
        contributions[body] = [[name, weight] for name, weight in scored.contributions]

    frozen = {
        "schema_version": "cf003-predictor-scores-v0",
        "candidate_id": "CF-003",
        "scientific_status": "development_predictor_commitment",
        "factor_flags_sha256": sha256(args.factor_flags),
        "predictor_spec_sha256": sha256(args.predictor_spec),
        "factor_extraction_convention_id": convention_id.strip(),
        "exact_historical_mastro_factor_extraction_reproduced": historical,
        "planet_scores": planet_scores,
        "rank_groups": rank_cf003_planet_scores(planet_scores),
        "contributions": contributions,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(frozen, indent=2, ensure_ascii=False) + "\n")
    print(f"Frozen CF-003 predictor scores at {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
