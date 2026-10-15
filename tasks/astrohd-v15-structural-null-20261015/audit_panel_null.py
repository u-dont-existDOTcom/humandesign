"""Frozen-panel structural null: score every possible neutral profile against actual decoys.

This is a *development diagnostic* for a chart signature selected using the
known subject. Private chart features, coordinates and candidate timestamps
remain in a local mode-0600 artifact; only aggregate audit data go to Git.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
from collections import Counter
from pathlib import Path

from audit_structural_null import (
    BINARY_MASKS,
    DOMAIN_STATES,
    OWNER_PROVISIONAL_PROFILE,
    signature_stats,
)

from hdmatch.evaluation import astrohd_v15_decoder as decoder


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def private_write(path: Path, contents: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(contents, handle, indent=2, sort_keys=True)
        handle.write("\n")


def audit_sample(mask_counts: Counter[int]) -> dict:
    """Apply the frozen model to every possible coded profile on the same panel."""
    for mask in mask_counts:
        if not 0 <= mask < 64:
            raise ValueError("Invalid astronomical feature mask")
        if not mask_counts[mask] >= 0:
            raise ValueError("Invalid chart feature count")
    assert sum(mask_counts.values()) > 0
    domains = tuple(sorted(d["id"] for d in decoder.load_model()[2]["domains"]))
    sign_profile_freq = Counter(
        decoder.answer_signs(dict(zip(domains, states, strict=True)))
        for states in itertools.product(DOMAIN_STATES, repeat=len(domains))
    )
    assert sum(sign_profile_freq.values()) == 3125
    summary = Counter()
    for signs, freq in sign_profile_freq.items():
        base = signature_stats(signs)
        if not base["scoreable"]:
            summary["unscorable_zero_evidence"] += freq
            continue
        target_score = base["target_score"]
        higher = sum(
            n for mask, n in mask_counts.items() if decoder.score_mask(mask, signs) > target_score
        )
        ties = sum(
            n for mask, n in mask_counts.items() if decoder.score_mask(mask, signs) == target_score
        )
        summary["scorable_profiles"] += freq
        if higher == 0:
            summary["sample_rank_best_first_profiles"] += freq
            if ties == 0:
                summary["sample_unique_first_profiles"] += freq
            if any(value == -1 for value in signs):
                summary["sample_first_despite_negative_profiles"] += freq
        if base["guaranteed_joint_first_with_any_candidate_panel"]:
            summary["mathematically_forced_first_profiles"] += freq
    assert summary["scorable_profiles"] == 3125 - summary["unscorable_zero_evidence"]
    assert (
        summary["sample_rank_best_first_profiles"]
        >= summary["mathematically_forced_first_profiles"]
    )
    user_signs = decoder.answer_signs(OWNER_PROVISIONAL_PROFILE)
    target_score = decoder.score_mask(63, user_signs)
    higher = sum(
        n for mask, n in mask_counts.items() if decoder.score_mask(mask, user_signs) > target_score
    )
    ties = sum(
        n for mask, n in mask_counts.items() if decoder.score_mask(mask, user_signs) == target_score
    )
    baseline = decoder.answer_signs({key: "supported" for key in domains})
    baseline_score = decoder.score_mask(63, baseline)
    baseline_ties = sum(
        n for mask, n in mask_counts.items() if decoder.score_mask(mask, baseline) == baseline_score
    )
    return {
        "schema": "astrohd-v15-structural-null-panel-v1",
        "classification": "SAME_PERSON_DEVELOPMENT_NULL_DIAGNOSTIC_NOT_PREDICTIVE_VALIDATION",
        "panel_decoys": sum(mask_counts.values()),
        "seed": 150925,
        "all_coded_profile_combinations": 3125,
        **dict(summary),
        "provisional_owner_development": {
            "rule_vote_signs": list(user_signs),
            "three_supported_behavior_domains": True,
            "rank_best": 1 + higher,
            "other_candidate_ties": ties,
            "structural_forced_first": True,
        },
        "all_supported_control": {
            "score": baseline_score,
            "other_candidate_ties": baseline_ties,
            "structural_forced_first": True,
        },
        "neutral_profile_count_is_not_population_prevalence": True,
        "not_a_full_century_scan": True,
        "no_private_birth_input_in_public_result": True,
    }


def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ephemeris-root", type=Path, required=True)
    parser.add_argument("--latitude", type=float, required=True)
    parser.add_argument("--longitude", type=float, required=True)
    parser.add_argument("--decoys", type=int, choices=(99, 999, 9999), default=9999)
    parser.add_argument("--private-output-dir", type=Path, required=True)
    parser.add_argument("--public-aggregate-output", type=Path, required=True)
    options = parser.parse_args()
    decoder.validate_location(options.latitude, options.longitude)
    for name in ("sepl_18.se1", "semo_18.se1"):
        if not (options.ephemeris_root / name).is_file():
            raise FileNotFoundError(f"Required Swiss ephemeris file missing: {name}")
    if options.private_output_dir.exists() and any(options.private_output_dir.iterdir()):
        raise FileExistsError(
            "Use a fresh private result directory; frozen receipts cannot be overwritten"
        )
    manifest = {
        "version": 1,
        "status": "PREDECLARED_BEFORE_DECOY_PANEL",
        "model_sha256": sha(decoder.MODEL_PATH),
        "bridge_sha256": sha(decoder.BRIDGE_PATH),
        "scorer_sha256": sha(Path(decoder.__file__)),
        "audit_sha256": sha(Path(__file__)),
        "decoy_seed": 150925,
        "decoy_count": options.decoys,
        "coordinates_private": [options.latitude, options.longitude],
        "ephemeris_sha256": {
            name: sha(options.ephemeris_root / name) for name in ("sepl_18.se1", "semo_18.se1")
        },
        "target_feature_mask": "preselected_six_of_six_fitted_signature",
        "profile_enumeration_states": list(DOMAIN_STATES),
        "no_participant_inputs_processed": True,
    }
    private_write(options.private_output_dir / "FROZEN-BEFORE-PANEL.json", manifest)
    masks = decoder.panel_masks(
        options.decoys, options.latitude, options.longitude, str(options.ephemeris_root.resolve())
    )
    counts = Counter(masks)
    private_write(
        options.private_output_dir / "MASK-FREQUENCIES-PRIVATE.json",
        {
            "panel_sha256": decoder.content_hash(
                [time.isoformat() for time in decoder.candidate_times(options.decoys)]
            ),
            "counts": {str(mask): counts[mask] for mask in BINARY_MASKS if counts[mask]},
            "no_personally_identifying_birth_key_stored": True,
        },
    )
    result = audit_sample(counts)
    options.public_aggregate_output.parent.mkdir(parents=True, exist_ok=True)
    options.public_aggregate_output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    run()
