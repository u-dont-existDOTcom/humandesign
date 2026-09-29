from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from hdmatch.empirical_astrology.cf003 import CF003_CANDIDATE_BODIES
from hdmatch.empirical_astrology.cf003_target import (
    CF003_CONSTRUCT_IDS,
    BehavioralConstructScore,
    CF003CohortPair,
    EvidenceQuote,
    apply_global_label_permutation,
    compare_cf003_rankings,
    construct_scores_to_planets,
    inclusive_top_k,
    midranks_descending,
    permutation_test_from_global_label_maps,
    rank_score_groups,
    sample_global_label_permutations,
    validate_behavioral_classifier_result,
)

ROOT = Path(__file__).resolve().parents[2]
REF = ROOT / "reference" / "empirical_astrology"
CONTRACT = REF / "cf003_behavioral_classifier_contract_v0.json"
MAPPING = REF / "cf003_behavioral_planet_map_v0.json"
QUESTIONS = REF / "cf003_secondary_question_module_v0.json"
PROMPT = REF / "cf003_behavioral_classifier_prompt_v0.md"
BUILDER_PATH = ROOT / "scripts" / "build_cf003_behavioral_packet_v0.py"
FREEZER_PATH = ROOT / "scripts" / "freeze_cf003_behavioral_target_v0.py"
COMPARER_PATH = ROOT / "scripts" / "compare_cf003_frozen_target_v0.py"


def _builder_module():
    spec = importlib.util.spec_from_file_location("cf003_packet_builder", BUILDER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _planet_scores(**overrides: float) -> dict[str, float]:
    values = {
        body: float(len(CF003_CANDIDATE_BODIES) - index)
        for index, body in enumerate(CF003_CANDIDATE_BODIES)
    }
    values.update(overrides)
    return values


def _complete_classifier_payload(rating: int | None = 2) -> dict:
    items = []
    for construct_id in CF003_CONSTRUCT_IDS:
        items.append(
            {
                "construct_id": construct_id,
                "dominance_rating": rating,
                "evidence_sufficient": rating is not None,
                "support_quotes": (
                    [{"turn_id": "t1", "quote": "recurring source phrase"}]
                    if rating is not None and rating > 0
                    else []
                ),
                "counterevidence_quotes": (
                    [{"turn_id": "t1", "quote": "not central"}] if rating == 0 else []
                ),
                "conditions": [],
                "time_frame": "current",
                "confidence": "medium",
                "reason": "Synthetic fixture only.",
            }
        )
    return {"construct_scores": items}


def test_classifier_contract_contains_neutral_constructs_and_no_planet_labels() -> None:
    contract = json.loads(CONTRACT.read_text())
    assert [row["construct_id"] for row in contract["constructs"]] == list(CF003_CONSTRUCT_IDS)
    text = json.dumps(contract).lower()
    for body in CF003_CANDIDATE_BODIES:
        assert not re.search(rf"\b{re.escape(body)}\b", text)


def test_evaluator_mapping_is_complete_and_separate_from_classifier_contract() -> None:
    mapping = json.loads(MAPPING.read_text())
    rows = mapping["mapping"]
    assert {row["construct_id"] for row in rows} == set(CF003_CONSTRUCT_IDS)
    assert {row["planet"] for row in rows} == set(CF003_CANDIDATE_BODIES)
    assert mapping["status"] == "evaluator_only_never_send_to_behavioral_classifier"
    assert any(
        row["planet"] == "sun" and row["existing_chart_blind_role_text"] is None for row in rows
    )


def test_secondary_module_is_three_questions_and_never_changes_primary_score() -> None:
    module = json.loads(QUESTIONS.read_text())
    assert len(module["questions"]) == 3
    assert "separate secondary-module record" in module["activation"]
    assert "never alter the primary score" in module["activation"]
    assert all(
        not any(
            re.search(rf"\b{re.escape(body)}\b", question["question"].lower())
            for body in CF003_CANDIDATE_BODIES
        )
        for question in module["questions"]
    )


def test_classifier_result_requires_exact_source_quotes() -> None:
    payload = _complete_classifier_payload()
    scores = validate_behavioral_classifier_result(
        payload,
        answer_text_by_turn_id={
            "t1": "This is a recurring source phrase and it is not central in one context."
        },
    )
    assert len(scores) == 10

    payload["construct_scores"][0]["support_quotes"][0]["quote"] = "invented paraphrase"
    with pytest.raises(ValueError, match="exact answer substring"):
        validate_behavioral_classifier_result(
            payload,
            answer_text_by_turn_id={"t1": "This is a recurring source phrase."},
        )


def test_zero_rating_requires_explicit_source_not_absence() -> None:
    payload = _complete_classifier_payload(0)
    validate_behavioral_classifier_result(
        payload,
        answer_text_by_turn_id={"t1": "This pattern is not central to me."},
    )
    payload["construct_scores"][0]["counterevidence_quotes"] = []
    with pytest.raises(ValueError, match="needs explicit source"):
        validate_behavioral_classifier_result(
            payload,
            answer_text_by_turn_id={"t1": "This pattern is not central to me."},
        )


def test_incomplete_behavioral_target_cannot_be_mapped_to_planets() -> None:
    scores = [
        BehavioralConstructScore(
            construct_id=construct_id,
            dominance_rating=None if construct_id == "T05" else 2,
            evidence_sufficient=construct_id != "T05",
            support_quotes=(
                () if construct_id == "T05" else (EvidenceQuote(turn_id="t1", quote="source"),)
            ),
        )
        for construct_id in CF003_CONSTRUCT_IDS
    ]
    with pytest.raises(ValueError, match="incomplete"):
        construct_scores_to_planets(scores)


def test_ranking_preserves_ties_and_uses_midranks() -> None:
    scores = _planet_scores(mars=100.0, venus=100.0)
    groups = rank_score_groups(scores)
    assert groups[0] == ("venus", "mars")
    midranks = midranks_descending(scores)
    assert midranks["venus"] == 1.5
    assert midranks["mars"] == 1.5


def test_primary_endpoint_reduces_to_predicted_planet_behavioral_rank() -> None:
    predictor = _planet_scores()
    predictor["mars"] = 100.0
    behavioral = _planet_scores()
    behavioral["mars"] = 200.0
    comparison = compare_cf003_rankings(predictor, behavioral)
    assert comparison.predictor_top_set == ("mars",)
    assert comparison.primary_top_set_mean_behavioral_midrank == 1.0


def test_predictor_top_tie_uses_mean_behavioral_midrank_without_tiebreak() -> None:
    predictor = _planet_scores(mars=100.0, venus=100.0)
    behavioral = _planet_scores()
    behavioral["mars"] = 200.0
    behavioral["venus"] = 150.0
    comparison = compare_cf003_rankings(predictor, behavioral)
    assert comparison.predictor_top_set == ("venus", "mars")
    assert comparison.primary_top_set_mean_behavioral_midrank == 1.5


def test_inclusive_top3_keeps_boundary_ties() -> None:
    scores = _planet_scores()
    scores["sun"] = 10.0
    scores["moon"] = 9.0
    scores["mercury"] = 8.0
    scores["venus"] = 8.0
    top = inclusive_top_k(scores, 3)
    assert {"sun", "moon", "mercury", "venus"} <= set(top)


def test_global_label_permutation_is_shared_and_deterministic() -> None:
    behavior = _planet_scores()
    permutation = tuple(reversed(CF003_CANDIDATE_BODIES))
    permuted = apply_global_label_permutation(behavior, permutation)
    assert permuted[CF003_CANDIDATE_BODIES[0]] == behavior[permutation[0]]
    assert permuted[CF003_CANDIDATE_BODIES[-1]] == behavior[permutation[-1]]


def test_permutation_test_uses_same_label_map_for_whole_cohort() -> None:
    predictor = _planet_scores()
    behavior = _planet_scores()
    pairs = [
        CF003CohortPair("p1", predictor, behavior),
        CF003CohortPair("p2", predictor, behavior),
    ]
    identity = tuple(CF003_CANDIDATE_BODIES)
    reverse = tuple(reversed(CF003_CANDIDATE_BODIES))
    result = permutation_test_from_global_label_maps(pairs, [identity, reverse])
    assert result.permutation_count == 2
    assert 0.0 < result.p_value <= 1.0


def test_sampled_global_label_permutations_are_unique_and_seeded() -> None:
    one = sample_global_label_permutations(20, seed=20260929)
    two = sample_global_label_permutations(20, seed=20260929)
    assert one == two
    assert len(one) == len(set(one)) == 20


def test_packet_builder_excludes_mapping_and_rejects_chart_leakage(tmp_path: Path) -> None:
    builder = _builder_module()
    source = tmp_path / "source.json"
    source.write_text(
        json.dumps(
            {
                "collection_mode": "chatgpt_voice",
                "turns": [
                    {
                        "turn_id": "t1",
                        "turn_role": "behavioral",
                        "question_text": "What tends to recur?",
                        "answer_text": "I keep returning to the same problem in several settings.",
                    }
                ],
            }
        )
    )
    packet = builder.build_packet(source, CONTRACT)
    serialized = json.dumps(packet).lower()
    assert "construct_to_planet" not in serialized
    assert "cf003_behavioral_planet_map" not in serialized
    assert packet["turns"][0]["answer_text"].startswith("I keep returning")

    source.write_text(
        json.dumps(
            {
                "turns": [
                    {
                        "turn_id": "t1",
                        "question_text": "What tends to recur?",
                        "answer_text": "My natal chart says this is important.",
                    }
                ]
            }
        )
    )
    with pytest.raises(ValueError, match="possible chart/target leakage"):
        builder.build_packet(source, CONTRACT)


def test_packet_builder_ignores_nonbehavioral_metadata_turns(tmp_path: Path) -> None:
    builder = _builder_module()
    source = tmp_path / "source.json"
    source.write_text(
        json.dumps(
            {
                "turns": [
                    {
                        "turn_id": "meta",
                        "turn_role": "collection_metadata",
                        "question_text": "Voice or text?",
                        "answer_text": "Voice.",
                    },
                    {
                        "turn_id": "behavior",
                        "turn_role": "behavioral",
                        "question_text": "What recurs?",
                        "answer_text": "I repeatedly verify details.",
                    },
                ]
            }
        )
    )
    packet = builder.build_packet(source, CONTRACT)
    assert [turn["turn_id"] for turn in packet["turns"]] == ["behavior"]


def test_classifier_prompt_is_neutral_and_contains_no_planet_labels() -> None:
    text = PROMPT.read_text().lower()
    for body in CF003_CANDIDATE_BODIES:
        assert not re.search(rf"\b{re.escape(body)}\b", text)


def test_mapping_lineage_matches_existing_nine_domain_roles() -> None:
    mapping = json.loads(MAPPING.read_text())
    contract = json.loads(
        (
            ROOT / "reference/core/survey_v2_human_measurement_scoring_contract_v1_0_0.json"
        ).read_text()
    )
    roles = contract["domain_measurement"]["domain_roles"]
    for row in mapping["mapping"]:
        key = row["existing_role_key"]
        if key is None:
            assert row["planet"] == "sun"
            continue
        assert row["existing_chart_blind_role_text"] == roles[key]["role"]


def test_freeze_then_compare_is_two_stage_and_predictor_not_needed_for_target(
    tmp_path: Path,
) -> None:
    builder = _builder_module()
    source = tmp_path / "source.json"
    source.write_text(
        json.dumps(
            {
                "collection_mode": "chatgpt_voice",
                "turns": [
                    {
                        "turn_id": "t1",
                        "turn_role": "behavioral",
                        "question_text": "What recurs?",
                        "answer_text": "This is a recurring source phrase and it matters across settings.",
                    }
                ],
            }
        )
    )
    packet_path = tmp_path / "packet.json"
    packet = builder.build_packet(source, CONTRACT, prompt_path=PROMPT)
    packet_path.write_text(json.dumps(packet))

    classifier_path = tmp_path / "classifier.json"
    classifier_path.write_text(json.dumps(_complete_classifier_payload(2)))
    frozen_path = tmp_path / "target.json"

    subprocess.run(
        [
            sys.executable,
            str(FREEZER_PATH),
            "--packet",
            str(packet_path),
            "--classifier-output",
            str(classifier_path),
            "--mapping",
            str(MAPPING),
            "--output",
            str(frozen_path),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    frozen = json.loads(frozen_path.read_text())
    assert frozen["prediction_opened"] is False
    assert frozen["behavioral_target_complete"] is True
    assert set(frozen["planet_scores"]) == set(CF003_CANDIDATE_BODIES)

    predictor_path = tmp_path / "predictor.json"
    predictor_path.write_text(json.dumps({"planet_scores": _planet_scores(mars=100.0)}))
    comparison_path = tmp_path / "comparison.json"
    subprocess.run(
        [
            sys.executable,
            str(COMPARER_PATH),
            "--target",
            str(frozen_path),
            "--predictor",
            str(predictor_path),
            "--output",
            str(comparison_path),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    comparison = json.loads(comparison_path.read_text())
    assert comparison["prediction_opened_after_target_freeze"] is True
    assert comparison["primary_endpoint"]["name"] == "predicted_top_set_mean_behavioral_midrank"


def test_manifest_hashes_pin_target_and_implementation_files() -> None:
    import hashlib

    manifest = json.loads(
        (REF / "cf003_independent_behavioral_target_manifest_v0.json").read_text()
    )
    for item in manifest["files"].values():
        source = ROOT / item["path"]
        assert hashlib.sha256(source.read_bytes()).hexdigest() == item["sha256"]
    for relative, expected in manifest["implementation_files"].items():
        source = ROOT / relative
        assert hashlib.sha256(source.read_bytes()).hexdigest() == expected
    assert manifest["separation"]["primary_tn001_changed"] is False
    assert manifest["separation"]["main_life_patterns_score_changed"] is False
    assert (
        manifest["chart_predictor_status"]["exact_historical_mastro_factor_extraction_reproduced"]
        is False
    )


def test_sampled_permutation_count_cannot_exceed_universe() -> None:
    import math

    with pytest.raises(ValueError, match="cannot exceed"):
        sample_global_label_permutations(
            math.factorial(len(CF003_CANDIDATE_BODIES)) + 1,
            seed=1,
        )
