#!/usr/bin/env python3
"""Validate and freeze an independent CF-003 behavioral target before predictor reveal."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict
from pathlib import Path
from typing import Any

from hdmatch.empirical_astrology.cf003_target import (
    CF003_CONSTRUCT_TO_PLANET,
    construct_scores_to_planets,
    rank_score_groups,
    support_quote_reuse,
    validate_behavioral_classifier_result,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAPPING = ROOT / "reference/empirical_astrology/cf003_behavioral_planet_map_v0.json"
DEFAULT_MANIFEST = (
    ROOT / "reference/empirical_astrology/cf003_independent_behavioral_target_manifest_v0.json"
)


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


def _require_sha256(value: str | None, *, name: str) -> str | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if not re.fullmatch(r"[0-9a-f]{64}", normalized):
        raise ValueError(f"{name} must be a 64-character lowercase/uppercase SHA-256")
    return normalized


def verify_manifest_files(manifest: dict[str, Any]) -> None:
    for group_name in ("files", "implementation_files"):
        group = manifest.get(group_name)
        if not isinstance(group, dict):
            raise ValueError(f"manifest {group_name} must be an object")
        for key, item in group.items():
            if group_name == "files":
                if not isinstance(item, dict):
                    raise ValueError(f"manifest file entry {key} must be an object")
                relative = item.get("path")
                expected = item.get("sha256")
            else:
                relative = key
                expected = item
            if not isinstance(relative, str) or not isinstance(expected, str):
                raise ValueError(f"manifest entry {key} is malformed")
            path = ROOT / relative
            if sha256(path) != expected:
                raise ValueError(f"manifest-pinned file hash mismatch: {relative}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--classifier-output", type=Path, required=True)
    parser.add_argument("--classifier-model", required=True)
    parser.add_argument("--classifier-run-id")
    parser.add_argument("--predictor-sha256")
    parser.add_argument("--mapping", type=Path, default=DEFAULT_MAPPING)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    packet = load_object(args.packet)
    classifier = load_object(args.classifier_output)
    mapping = load_object(args.mapping)
    manifest = load_object(args.manifest)
    verify_manifest_files(manifest)

    if packet.get("schema_version") != "independent-behavioral-classifier-packet-v0":
        raise ValueError("unexpected classifier packet schema")
    source_meta = packet.get("source")
    if not isinstance(source_meta, dict):
        raise ValueError("classifier packet lacks source provenance")

    manifest_files = manifest["files"]
    expected_contract = manifest_files["classifier_contract"]["sha256"]
    expected_prompt = manifest_files["classifier_prompt"]["sha256"]
    if source_meta.get("contract_sha256") != expected_contract:
        raise ValueError("packet contract hash does not match the frozen manifest")
    if source_meta.get("prompt_sha256") != expected_prompt:
        raise ValueError("packet prompt hash does not match the frozen manifest")
    if sha256(args.mapping) != manifest_files["planet_map"]["sha256"]:
        raise ValueError("mapping hash does not match the frozen manifest")

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
    predictor_commitment = _require_sha256(args.predictor_sha256, name="predictor-sha256")
    reuse = support_quote_reuse(scores)

    if not args.classifier_model.strip():
        raise ValueError("classifier-model must be non-empty")
    if complete and predictor_commitment:
        status = "development_complete_target_with_predictor_commitment"
    elif complete:
        status = "development_complete_unpaired_target"
    else:
        status = "development_incomplete_target"

    frozen = {
        "schema_version": "cf003-frozen-behavioral-target-v0",
        "scientific_status": status,
        "classifier_packet_sha256": sha256(args.packet),
        "classifier_run": {
            "model": args.classifier_model.strip(),
            "run_id": args.classifier_run_id,
            "raw_response_sha256": sha256(args.classifier_output),
        },
        "manifest_sha256": sha256(args.manifest),
        "evaluator_mapping_sha256": sha256(args.mapping),
        "predictor_commitment_sha256": predictor_commitment,
        "source": source_meta,
        "construct_scores": [
            {
                **asdict(score),
                "support_quotes": [asdict(quote) for quote in score.support_quotes],
                "counterevidence_quotes": [asdict(quote) for quote in score.counterevidence_quotes],
            }
            for score in scores
        ],
        "quote_reuse": {key: list(construct_ids) for key, construct_ids in reuse.items()},
        "behavioral_target_complete": complete,
        "planet_scores": planet_scores,
        "behavioral_rank_groups": rank_groups,
        "tie_rule": "equal dominance ratings remain tied; no tie-breaker",
        "notes": [
            "The behavioral classifier ran without the evaluator mapping or predictor scores.",
            "A non-null predictor_commitment_sha256 is required before comparison.",
            "Existing development participants remain exploratory.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(frozen, indent=2, ensure_ascii=False) + "\n")
    print(f"Frozen behavioral target ({status}) at {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
