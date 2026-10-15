"""Exact null audit for the retained five-domain/six-clause AstroHD V1.5 bridge.

Pure, exhaustive 5^5 response-state and 2^6 feature-mask enumeration; no dates,
participant data, astronomy scans, or retrospective score-fitting are needed.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path

from hdmatch.evaluation import astrohd_v15_decoder as decoder

ROOT = Path(__file__).resolve().parents[2]
SIX_SCAN = (
    ROOT
    / "tasks/scenario-owner-recovery-calibration-20260923"
    / "ASTROHD-V14-EXACT-CENTURY-RESULT-20260925.json"
)
MODEL_PATH = decoder.MODEL_PATH
BRIDGE_PATH = decoder.BRIDGE_PATH
BINARY_MASKS = tuple(range(64))
DOMAIN_STATES = ("supported", "contradicted", "mixed", "unknown", "not_applicable")
OWNER_PROVISIONAL_PROFILE = {
    "insight_translation": "supported",
    "retreat_privacy": "supported",
    "romantic_attachment": "supported",
    "persuasion_strategy": "mixed",
    "recognition_entry": "mixed",
}


def signature_stats(signs: tuple[int, ...], target_mask: int = 63) -> dict:
    """Use every possible *feature mask*, not an astronomical population prior."""
    if len(signs) != 6 or any(x not in (-1, 0, 1) for x in signs):
        raise ValueError("Six signed source-grounded clause states required")
    if not 0 <= target_mask < 64:
        raise ValueError("Not a 6-bit feature mask")
    scores = tuple(decoder.score_mask(mask, signs) for mask in BINARY_MASKS)
    target_score = scores[target_mask]
    maximum = max(scores)
    top_masks = tuple(i for i, value in enumerate(scores) if value == maximum)
    nonnegative = not any(s < 0 for s in signs)
    is_scorable = any(signs)
    # Score 0 and all unknown must be inadmissible, even if the raw rank is 1.
    guaranteed_first = is_scorable and nonnegative and target_mask == 63
    return {
        "target_score": target_score,
        "maximum_score_any_six_bit_mask": maximum,
        "target_best_rank_in_complete_mask_space": 1 + sum(v > target_score for v in scores),
        "target_ties_in_complete_mask_space": scores.count(target_score),
        "winning_masks": top_masks,
        "scoreable": is_scorable,
        "guaranteed_joint_first_with_any_candidate_panel": guaranteed_first,
        "positive_clauses": sum(v == 1 for v in signs),
        "negative_clauses": sum(v == -1 for v in signs),
        "abstained_clauses": sum(v == 0 for v in signs),
    }


def enumerate_profiles() -> dict:
    """Enumerate neutral domain states, then apply the *frozen* bridge unchanged."""
    domain_ids = tuple(sorted(row["id"] for row in decoder.load_model()[2]["domains"]))
    assert len(domain_ids) == 5
    distribution = Counter()
    vectors = Counter()
    for values in itertools.product(DOMAIN_STATES, repeat=len(domain_ids)):
        profile = dict(zip(domain_ids, values, strict=True))
        signs = decoder.answer_signs(profile)
        vectors[signs] += 1
        result = signature_stats(signs)
        if not result["scoreable"]:
            distribution["unscorable_zero_evidence"] += 1
        elif result["guaranteed_joint_first_with_any_candidate_panel"]:
            distribution["scorable_forced_first"] += 1
        else:
            distribution["not_guaranteed_first"] += 1
        if any(x < 0 for x in signs):
            distribution["includes_contradictory_clause"] += 1
        if all(x >= 0 for x in signs):
            distribution["nonnegative_including_unscorable"] += 1
        distribution["total_profiles"] += 1
    expected = len(DOMAIN_STATES) ** len(domain_ids)
    assert distribution["total_profiles"] == expected
    assert (
        sum(
            distribution[k]
            for k in ("unscorable_zero_evidence", "scorable_forced_first", "not_guaranteed_first")
        )
        == expected
    )
    return {
        **dict(distribution),
        "distinct_reachable_clause_vectors": len(vectors),
        "uniform_profile_enumeration_not_a_human_population": True,
        "forced_first_fraction_of_all_profiles": distribution["scorable_forced_first"] / expected,
        "forced_first_fraction_of_scorable_profiles": distribution["scorable_forced_first"]
        / (expected - distribution["unscorable_zero_evidence"]),
        "profile_domain_count": len(domain_ids),
        "profile_state_count_per_domain": len(DOMAIN_STATES),
    }


def no_tie_probability(
    *, other_minutes: int, comparison_minutes: int, candidate_pool_without_target: int
) -> float:
    """Exact without-replacement P(no tied minutes in a uniformly drawn panel)."""
    if not 0 <= other_minutes <= candidate_pool_without_target:
        raise ValueError("Invalid number of tied minutes")
    if not 0 <= comparison_minutes <= candidate_pool_without_target:
        raise ValueError("Invalid size of comparison")
    if comparison_minutes > candidate_pool_without_target - other_minutes:
        return 0.0
    log_p = math.fsum(
        math.log1p(-other_minutes / (candidate_pool_without_target - step))
        for step in range(comparison_minutes)
    )
    return math.exp(log_p)


def century_bounds(scan_result: dict, panel_size: int = 9999) -> dict:
    """Reuse the verified C scan rejection histogram, not another century scan.

    Native check order: clause 3, 4, 2, 1, 5, 6. For the new (+,+,+,+,0,+)
    signature, maxima must satisfy the first four and the sixth clause.
    Previous fast-prune bin 4 failed clause 5; it may pass clause 6.
    Bin 5 failed clause 6 and cannot be a maximum. Bin 6 passed everything.
    """
    counts = scan_result["verification"]["aggregate_rejection_and_maximum_counts"]
    count = scan_result["exact_grid_count"]
    if (
        scan_result["status"] != "COMPLETE"
        or len(counts) != 7
        or sum(counts) != count
        or scan_result["maximum_count"] != counts[6]
        or scan_result["maximum_score"] != 6
        or scan_result["target_rank_best"] != 1
        or not scan_result["unique_offsets_verified"]
    ):
        raise ValueError("Frozen century audit not admissible for this bound")
    if count < panel_size + 2:
        raise ValueError("Insufficient declared century universe")
    lower = counts[6]
    upper = counts[6] + counts[4]
    assert lower > 0 and upper <= count
    alternatives_min = lower - 1
    alternatives_max = upper - 1
    # These are bounds over the century's 1-minute grid, not exact five-rule winners.
    return {
        "source_verified_total_minute_grid": count,
        "source_verified_six_clause_maxima": counts[6],
        "five_active_clause_winner_count_lower_bound": lower,
        "five_active_clause_winner_count_upper_bound": upper,
        "minimum_other_tied_minutes": alternatives_min,
        "maximum_other_tied_minutes": alternatives_max,
        "comparison_decoys": panel_size,
        "probability_no_ties_if_uniform_sample_lower_bound": no_tie_probability(
            other_minutes=alternatives_max,
            comparison_minutes=panel_size,
            candidate_pool_without_target=count - 1,
        ),
        "probability_no_ties_if_uniform_sample_upper_bound": no_tie_probability(
            other_minutes=alternatives_min,
            comparison_minutes=panel_size,
            candidate_pool_without_target=count - 1,
        ),
        "proof_boundary": ("Verified original fast-pruning bins; not a new five-rule century scan"),
        "source_scan_complete": True,
    }


def report() -> dict:
    model = decoder.load_model()[0]
    model_sha = hashlib.sha256(MODEL_PATH.read_bytes()).hexdigest()
    scan = json.loads(SIX_SCAN.read_text())
    if model["version"] != "1.4d" or scan["model_sha256"] != model_sha:
        raise ValueError("Accepted six-rule model and frozen century result disagree")
    owner_signs = decoder.answer_signs(OWNER_PROVISIONAL_PROFILE)
    if owner_signs != (1, 1, 1, 1, 0, 1):
        raise ValueError("The provisional development profile changed; stop")
    signature = signature_stats(owner_signs)
    assert signature["winning_masks"] == (47, 63)
    assert signature["target_best_rank_in_complete_mask_space"] == 1
    controls = {
        "all_positive": signature_stats(
            decoder.answer_signs({k: "supported" for k in OWNER_PROVISIONAL_PROFILE})
        ),
        "all_unknown": signature_stats(
            decoder.answer_signs({k: "unknown" for k in OWNER_PROVISIONAL_PROFILE})
        ),
        "explicit_contradiction": signature_stats(
            decoder.answer_signs(
                {**OWNER_PROVISIONAL_PROFILE, "insight_translation": "contradicted"}
            )
        ),
    }
    assert controls["all_positive"]["guaranteed_joint_first_with_any_candidate_panel"]
    assert not controls["all_unknown"]["scoreable"]
    assert controls["explicit_contradiction"]["target_best_rank_in_complete_mask_space"] > 1
    return {
        "schema": "astrohd-v15-structural-null-v1",
        "classification": "EXACT_COMBINATORIAL_DEVELOPMENT_AUDIT_NOT_HUMAN_VALIDATION",
        "model_version": model["version"],
        "model_hash_matches_frozen_century": True,
        "model_changed": False,
        "bridge_changed": False,
        "target_feature_mask": "full_six_bit_signature",
        "provisional_signs": list(owner_signs),
        "provisional_profile_participant_confirmed": False,
        "distinct_supported_domains_in_provisional_profile": sum(
            value == "supported" for value in OWNER_PROVISIONAL_PROFILE.values()
        ),
        "target_signature_statistics": {
            **{key: value for key, value in signature.items() if key != "winning_masks"},
            "winning_six_bit_masks": list(signature["winning_masks"]),
        },
        "all_profile_enumeration": enumerate_profiles(),
        "controls": {
            name: {
                "target_score": values["target_score"],
                "best_rank_in_64_mask_space": values["target_best_rank_in_complete_mask_space"],
                "guaranteed_first": values["guaranteed_joint_first_with_any_candidate_panel"],
                "scorable": values["scoreable"],
            }
            for name, values in controls.items()
        },
        "century_tie_bounds_for_five_positive_one_abstention": century_bounds(scan),
        "zero_extra_astro_scans": True,
        "no_personal_data_in_artifact": True,
        "prospective_boundary": (
            "Human reverse matching requires a person whose birth chart did not select "
            "these six rules; retain declared decoy universe, true-rank and ties and "
            "compare against independent unconditioned profiles before claiming prediction."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "profile_space": output["all_profile_enumeration"],
                "target_six_bit_best_rank": output["target_signature_statistics"][
                    "target_best_rank_in_complete_mask_space"
                ],
                "five_active_win_min": output[
                    "century_tie_bounds_for_five_positive_one_abstention"
                ]["five_active_clause_winner_count_lower_bound"],
                "five_active_win_max": output[
                    "century_tie_bounds_for_five_positive_one_abstention"
                ]["five_active_clause_winner_count_upper_bound"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
