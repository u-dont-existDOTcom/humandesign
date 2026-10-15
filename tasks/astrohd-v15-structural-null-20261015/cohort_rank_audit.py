"""Offline cohort N x N identity test for untouched AstroHD V1.5 participants.

Inputs must be consenting, already-sealed, chart-mask + neutral-profile pairs.
This evaluator never learns DOB/place; exact permutation is calculated when N<=8.
A self-declared "frozen" flag is NOT proof of a prospective evidence freeze.
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import random
from datetime import datetime
from pathlib import Path
from typing import Any

from hdmatch.evaluation import astrohd_v15_decoder as decoder


def _score_matrix(profiles: list[dict[str, str]], masks: list[int]) -> list[list[int]]:
    return [
        [decoder.score_mask(mask, decoder.answer_signs(profile)) for mask in masks]
        for profile in profiles
    ]


def _tail_probability(matrix: list[list[int]], *, seed: int = 150925) -> dict[str, Any]:
    n = len(matrix)
    observed = sum(matrix[i][i] for i in range(n))
    if n <= 8:
        values = (sum(matrix[i][p[i]] for i in range(n)) for p in itertools.permutations(range(n)))
        count = 0
        at_least = 0
        for value in values:
            count += 1
            at_least += value >= observed
        return {
            "method": "EXACT_ALL_N_FACTORIAL_LABEL_PERMUTATIONS",
            "n_assignments_evaluated": count,
            "one_sided_p_ge_observed_including_ties": at_least / count,
            "observed_total_score": observed,
        }
    rng = random.Random(seed)
    trials = 20_000
    at_least = 0
    for _ in range(trials):
        p = list(range(n))
        rng.shuffle(p)
        value = sum(matrix[i][p[i]] for i in range(n))
        at_least += value >= observed
    return {
        "method": "SEEDED_RANDOM_CHART_LABEL_PERMUTATION_MONTE_CARLO",
        "n_assignments_evaluated": trials,
        "seed": seed,
        "one_sided_p_ge_observed_including_ties": (at_least + 1) / (trials + 1),
        "observed_total_score": observed,
        "monte_carlo_adjustment": "plus-one correction",
    }


def evaluate(records: list[dict[str, Any]]) -> dict:
    """Calculate person-by-chart scores, true-chart ranks, and permutation null."""
    if not 2 <= len(records) <= 100:
        raise ValueError("Cohort must have 2 to 100 participants")
    allowed_fields = {
        "pseudonym",
        "consent_to_analysis",
        "chart_known_to_question_coder",
        "neutral_profile",
        "chart_six_bit_mask",
    }
    if any(not isinstance(row, dict) or set(row) != allowed_fields for row in records):
        raise ValueError("Exactly the five declared pseudonymous cohort fields are required")
    pseudonyms = [row["pseudonym"] for row in records]
    if any(not isinstance(pid, str) or not pid or len(pid) > 80 for pid in pseudonyms):
        raise ValueError("Non-empty bounded pseudonym required")
    if len(set(pseudonyms)) != len(pseudonyms):
        raise ValueError("Repeated participant pseudonym")
    if any(row.get("consent_to_analysis") is not True for row in records):
        raise ValueError("Explicit participant consent to analysis required")
    if any(row["chart_known_to_question_coder"] is not False for row in records):
        raise ValueError("Chart leaked or concealment unverified for behavioral coder")
    masks = [row.get("chart_six_bit_mask") for row in records]
    if any(type(mask) is not int or mask < 0 or mask > 63 for mask in masks):
        raise ValueError("Valid six-bit chart mask required")
    profiles = [decoder.normalize_profile(row["neutral_profile"]) for row in records]
    signs = [decoder.answer_signs(profile) for profile in profiles]
    matrix = _score_matrix(profiles, masks)
    ranks = []
    for i in range(len(records)):
        if not any(signs[i]):
            ranks.append(
                {
                    "pseudonym": pseudonyms[i],
                    "status": "UNSCORABLE_NO_INFORMATION",
                    "rank_best": None,
                    "rank_worst": None,
                    "profile_score": None,
                }
            )
            continue
        others = [v for j, v in enumerate(matrix[i]) if j != i]
        metrics = decoder.rank_against(others, matrix[i][i])
        ranks.append(
            {
                "pseudonym": pseudonyms[i],
                "status": "SCORED_BUT_NOT_VALIDATED",
                "rank_best": metrics["rank_best"],
                "rank_worst": metrics["rank_worst"],
                "tied_other_charts": metrics["tied_other_candidates"],
                "profile_score": matrix[i][i],
                "target_first_structurally_guaranteed": (
                    masks[i] == 63 and all(s >= 0 for s in signs[i])
                ),
            }
        )
    completely_scored = all(any(s) for s in signs)
    result = {
        "schema": "astrohd-v15-cohort-identity-matrix-v1",
        "classification": "HUMAN_EVIDENCE_DEPENDS_ON_CONSENT_AND_PRE_RESPONSE_FREEZE",
        "participant_count": len(records),
        "pseudonyms": pseudonyms,
        "score_matrix_rows_profile_columns_chart": matrix,
        "true_chart_ranks": ranks,
        "group_null": (
            _tail_probability(matrix)
            if completely_scored
            else {"status": "NOT_CALCULATED_UNSCORABLE_PARTICIPANT_PRESERVED"}
        ),
        "all_positive_chart_only_control": {
            "group_permutation_p": 1.0,
            "reason": (
                "Chart-only scores are identical across participants, so every "
                "assignment has the same score sum."
            ),
        },
        "no_calibrated_probabilities_claimed": True,
        "manual_provenance_needed": (
            "Verify independently that neutral response profiles were sealed before chart "
            "identities or scores were revealed, with birth-time source quality and "
            "Swiss-ephemeris provenance logged outside this chart-mask dataset."
        ),
    }
    return result


def private_write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    path.chmod(0o600)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-cohort-json", type=Path, required=True)
    parser.add_argument("--private-output-json", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2].resolve()
    for path in (args.private_cohort_json, args.private_output_json):
        if path.resolve().is_relative_to(root):
            raise ValueError("Private participant files must stay outside the Git checkout")
    payload = json.loads(args.private_cohort_json.read_text())
    if payload.get("schema") != "astrohd-v15-consenting-cohort-v1":
        raise ValueError("Unrecognized cohort intake schema")
    result = evaluate(payload["records"])
    result["preexisting_prospective_freeze_receipts_verified_by_this_script"] = False
    result["computed_at_utc"] = datetime.now().astimezone().isoformat()
    private_write(args.private_output_json, result)
    # All participant-specific output remains in the local 0600 file.
    print(
        json.dumps(
            {
                "participant_count": result["participant_count"],
                "scorable_count": sum(
                    r["status"] == "SCORED_BUT_NOT_VALIDATED" for r in result["true_chart_ranks"]
                ),
                "permutation_status": result["group_null"].get(
                    "method", result["group_null"].get("status")
                ),
                "private_report_written": True,
            }
        )
    )


if __name__ == "__main__":
    main()
