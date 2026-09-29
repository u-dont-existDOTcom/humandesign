from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from hdmatch.empirical_astrology.cf003 import CF003_CANDIDATE_BODIES, CF003_PUBLISHED_WEIGHTS
from hdmatch.empirical_astrology.cf003_target import (
    CF003_CONSTRUCT_IDS,
    BehavioralConstructScore,
    CF003CohortPair,
    EvidenceQuote,
    apply_profile_reassignment,
    compare_cf003_rankings,
    construct_scores_to_planets,
    fractional_top_k_membership,
    midranks_descending,
    permutation_test_from_profile_reassignments,
    predictor_scores_to_tenths,
    rank_score_groups,
    sample_profile_reassignments,
    support_quote_reuse,
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
PREDICTOR_FREEZER_PATH = ROOT / "scripts" / "freeze_cf003_predictor_scores_v0.py"
COMPARER_PATH = ROOT / "scripts" / "compare_cf003_frozen_target_v0.py"
MANIFEST = REF / "cf003_independent_behavioral_target_manifest_v0.json"


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
        support_quotes = []
        if rating is not None and rating > 0:
            support_quotes.append(
                {"turn_id": "t1", "quote": "recurring source phrase across settings"}
            )
            if rating >= 3:
                support_quotes.append(
                    {"turn_id": "t2", "quote": "another distinct source phrase across time"}
                )
        items.append(
            {
                "construct_id": construct_id,
                "dominance_rating": rating,
                "evidence_sufficient": rating is not None,
                "support_quotes": support_quotes,
                "counterevidence_quotes": (
                    [{"turn_id": "t1", "quote": "this pattern is not central to me"}]
                    if rating == 0
                    else []
                ),
                "conditions": [],
                "time_frame": "current",
                "confidence": "medium",
                "reason": "Synthetic fixture only.",
            }
        )
    return {"construct_scores": items}


def test_classifier_contract_contains_neutral_constructs_and_no_hidden_framework_labels() -> None:
    contract = json.loads(CONTRACT.read_text())
    assert [row["construct_id"] for row in contract["constructs"]] == list(CF003_CONSTRUCT_IDS)
    text = json.dumps(contract).lower()
    for body in CF003_CANDIDATE_BODIES:
        assert not re.search(rf"\b{re.escape(body)}\b", text)
    for forbidden in ("astrolog", "horoscope", "zodiac", "human design", "cf-003"):
        assert forbidden not in text


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
            "t1": (
                "This is a recurring source phrase across settings, while "
                "this pattern is not central to me in one context."
            )
        },
    )
    assert len(scores) == 10

    payload["construct_scores"][0]["support_quotes"][0]["quote"] = "invented paraphrase"
    with pytest.raises(ValueError, match="exact answer substring"):
        validate_behavioral_classifier_result(
            payload,
            answer_text_by_turn_id={"t1": "This is a recurring source phrase across settings."},
        )


def test_zero_rating_requires_explicit_source_not_absence() -> None:
    payload = _complete_classifier_payload(0)
    validate_behavioral_classifier_result(
        payload,
        answer_text_by_turn_id={"t1": "this pattern is not central to me."},
    )
    payload["construct_scores"][0]["counterevidence_quotes"] = []
    with pytest.raises(ValueError, match="counterevidence"):
        validate_behavioral_classifier_result(
            payload,
            answer_text_by_turn_id={"t1": "this pattern is not central to me."},
        )


def test_classifier_rejects_weak_or_malformed_evidence_contract() -> None:
    source = {
        "t1": "recurring source phrase across settings and this pattern is not central to me.",
        "t2": "another distinct source phrase across time and settings.",
    }

    one_word = _complete_classifier_payload(2)
    one_word["construct_scores"][0]["support_quotes"][0]["quote"] = "recurring"
    with pytest.raises(ValueError, match="at least four words"):
        validate_behavioral_classifier_result(one_word, answer_text_by_turn_id=source)

    string_boolean = _complete_classifier_payload(2)
    string_boolean["construct_scores"][0]["evidence_sufficient"] = "false"
    with pytest.raises(ValueError, match="must be a boolean"):
        validate_behavioral_classifier_result(string_boolean, answer_text_by_turn_id=source)

    one_quote_high = _complete_classifier_payload(3)
    one_quote_high["construct_scores"][0]["support_quotes"] = [
        {"turn_id": "t1", "quote": "recurring source phrase across settings"}
    ]
    with pytest.raises(ValueError, match="at least two distinct support quotes"):
        validate_behavioral_classifier_result(one_quote_high, answer_text_by_turn_id=source)


def test_support_quote_reuse_is_reported_explicitly() -> None:
    scores = validate_behavioral_classifier_result(
        _complete_classifier_payload(2),
        answer_text_by_turn_id={"t1": "recurring source phrase across settings"},
    )
    reuse = support_quote_reuse(scores)
    assert len(reuse) == 1
    assert set(next(iter(reuse.values()))) == set(CF003_CONSTRUCT_IDS)


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


def test_fractional_top3_shares_boundary_ties_and_always_uses_three_slots() -> None:
    scores = _planet_scores()
    scores["sun"] = 10.0
    scores["moon"] = 9.0
    scores["mercury"] = 8.0
    scores["venus"] = 8.0
    membership = fractional_top_k_membership(scores, 3)
    assert membership["sun"] == 1.0
    assert membership["moon"] == 1.0
    assert membership["mercury"] == 0.5
    assert membership["venus"] == 0.5
    assert sum(membership.values()) == pytest.approx(3.0)

    sparse = {body: 0.0 for body in CF003_CANDIDATE_BODIES}
    sparse["sun"] = 8.3
    sparse["moon"] = 7.6
    sparse_membership = fractional_top_k_membership(sparse, 3)
    assert sparse_membership["sun"] == 1.0
    assert sparse_membership["moon"] == 1.0
    for body in CF003_CANDIDATE_BODIES:
        if body not in {"sun", "moon"}:
            assert sparse_membership[body] == pytest.approx(0.125)
    assert sum(sparse_membership.values()) == pytest.approx(3.0)


def test_predictor_scores_quantize_to_published_tenths_before_tie_ranking() -> None:
    scores = {body: 0.0 for body in CF003_CANDIDATE_BODIES}
    scores["venus"] = 18.200000000000003
    scores["mars"] = 18.2
    tenths = predictor_scores_to_tenths(scores)
    assert tenths["venus"] == tenths["mars"] == 182
    comparison = compare_cf003_rankings(scores, _planet_scores(venus=20.0, mars=19.0))
    assert comparison.predictor_top_set == ("venus", "mars")


def test_profile_reassignment_preserves_whole_profiles_and_strata() -> None:
    p1 = CF003CohortPair("p1", _planet_scores(), _planet_scores(sun=99), "young")
    p2 = CF003CohortPair("p2", _planet_scores(), _planet_scores(moon=98), "young")
    p3 = CF003CohortPair("p3", _planet_scores(), _planet_scores(mars=97), "older")
    p4 = CF003CohortPair("p4", _planet_scores(), _planet_scores(venus=96), "older")
    pairs = [p1, p2, p3, p4]
    reassigned = apply_profile_reassignment(pairs, (1, 0, 3, 2))
    assert reassigned[0].behavioral_scores == p2.behavioral_scores
    assert reassigned[1].behavioral_scores == p1.behavioral_scores
    assert reassigned[2].behavioral_scores == p4.behavioral_scores
    assert reassigned[3].behavioral_scores == p3.behavioral_scores
    with pytest.raises(ValueError, match="crossed"):
        apply_profile_reassignment(pairs, (2, 1, 0, 3))


def test_profile_reassignment_null_is_seeded_and_uses_whole_participants() -> None:
    pairs = [
        CF003CohortPair("p1", _planet_scores(sun=20), _planet_scores(sun=30), "a"),
        CF003CohortPair("p2", _planet_scores(moon=20), _planet_scores(moon=30), "a"),
        CF003CohortPair("p3", _planet_scores(mars=20), _planet_scores(mars=30), "b"),
        CF003CohortPair("p4", _planet_scores(venus=20), _planet_scores(venus=30), "b"),
    ]
    one = sample_profile_reassignments(pairs, 4, seed=20260929)
    two = sample_profile_reassignments(pairs, 4, seed=20260929)
    assert one == two
    assert len(one) == len(set(one)) == 4
    result = permutation_test_from_profile_reassignments(pairs, one)
    assert result.permutation_count == 4
    assert 0.0 < result.p_value <= 1.0
    with pytest.raises(ValueError, match="cannot exceed"):
        sample_profile_reassignments(pairs, 5, seed=1)


def _write_behavioral_source(path: Path, answer: str, **record_fields: object) -> None:
    path.write_text(
        json.dumps(
            {
                "collection_mode": "chatgpt_voice",
                **record_fields,
                "turns": [
                    {
                        "turn_id": "source-specific-id",
                        "turn_role": "behavioral",
                        "question_text": "What tends to recur?",
                        "answer_text": answer,
                    }
                ],
            }
        )
    )


def test_packet_builder_excludes_hidden_context_and_sanitizes_turn_ids(tmp_path: Path) -> None:
    builder = _builder_module()
    source = tmp_path / "source.json"
    _write_behavioral_source(
        source,
        "I keep returning to the same problem in several settings.",
    )
    packet = builder.build_packet(source, CONTRACT)
    serialized = json.dumps(packet).lower()
    assert "construct_to_planet" not in serialized
    assert "cf003_behavioral_planet_map" not in serialized
    assert packet["turns"][0]["turn_id"] == "primary-0001"
    assert packet["turns"][0]["answer_text"].startswith("I keep returning")


@pytest.mark.parametrize(
    "answer",
    [
        "I am a typical Scorpio.",
        "Leo rising described me well.",
        "My Mars is in Aries.",
        "My Saturn return changed things.",
        "My chart explains the pattern.",
        "I asked an astrologer about it.",
        "My horoscope said the same thing.",
        "I am a Projector.",
        "I have a 4/6 profile.",
    ],
)
def test_packet_builder_rejects_profile_leakage_examples(tmp_path: Path, answer: str) -> None:
    builder = _builder_module()
    source = tmp_path / "source.json"
    _write_behavioral_source(source, answer)
    with pytest.raises(ValueError, match="external-profile leakage"):
        builder.build_packet(source, CONTRACT)


def test_packet_builder_scans_passthrough_fields_and_forbidden_record_keys(
    tmp_path: Path,
) -> None:
    builder = _builder_module()
    source = tmp_path / "source.json"
    source.write_text(
        json.dumps(
            {
                "turns": [
                    {
                        "turn_role": "behavioral",
                        "question_text": "What recurs?",
                        "answer_text": "I repeatedly verify details across settings.",
                        "conditions": ["only because my natal chart says so"],
                    }
                ]
            }
        )
    )
    with pytest.raises(ValueError, match="external-profile leakage"):
        builder.build_packet(source, CONTRACT)

    _write_behavioral_source(
        source,
        "I repeatedly verify details across settings.",
        birth_date="2000-01-01",
    )
    with pytest.raises(ValueError, match="forbidden profile field"):
        builder.build_packet(source, CONTRACT)


def test_packet_builder_requires_explicit_roles_and_clean_exposure_metadata(
    tmp_path: Path,
) -> None:
    builder = _builder_module()
    source = tmp_path / "source.json"
    source.write_text(
        json.dumps(
            {
                "turns": [
                    {
                        "question_text": "What recurs?",
                        "answer_text": "I repeatedly verify details across settings.",
                    }
                ]
            }
        )
    )
    with pytest.raises(ValueError, match="missing explicit turn_role"):
        builder.build_packet(source, CONTRACT)

    _write_behavioral_source(
        source,
        "I repeatedly verify details across settings.",
        blinding={"contamination_notes": "participant saw prior target"},
    )
    with pytest.raises(ValueError, match="contamination_notes"):
        builder.build_packet(source, CONTRACT)


def test_packet_builder_requires_secondary_to_link_to_exact_primary_hash(
    tmp_path: Path,
) -> None:
    import hashlib

    builder = _builder_module()
    primary = tmp_path / "primary.json"
    secondary = tmp_path / "secondary.json"
    _write_behavioral_source(primary, "I repeatedly verify details across settings.")
    secondary.write_text(
        json.dumps(
            {
                "primary_record_sha256": "0" * 64,
                "turns": [
                    {
                        "turn_role": "behavioral",
                        "question_text": "What stayed consistent?",
                        "answer_text": "I keep the same standards across many settings.",
                    }
                ],
            }
        )
    )
    with pytest.raises(ValueError, match="exact primary_record_sha256 linkage"):
        builder.build_packet(primary, CONTRACT, secondary_path=secondary)

    primary_hash = hashlib.sha256(primary.read_bytes()).hexdigest()
    secondary_data = json.loads(secondary.read_text())
    secondary_data["primary_record_sha256"] = primary_hash
    secondary.write_text(json.dumps(secondary_data))
    packet = builder.build_packet(primary, CONTRACT, secondary_path=secondary)
    assert [turn["turn_id"] for turn in packet["turns"]] == [
        "primary-0001",
        "secondary-0001",
    ]


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
                        "answer_text": "I repeatedly verify details across settings.",
                    },
                ]
            }
        )
    )
    packet = builder.build_packet(source, CONTRACT)
    assert [turn["turn_id"] for turn in packet["turns"]] == ["primary-0001"]


def test_classifier_prompt_is_neutral_and_contains_no_hidden_framework_labels() -> None:
    text = PROMPT.read_text().lower()
    for body in CF003_CANDIDATE_BODIES:
        assert not re.search(rf"\b{re.escape(body)}\b", text)
    for forbidden in ("astrolog", "horoscope", "zodiac", "human design", "cf-003"):
        assert forbidden not in text


def test_mapping_lineage_matches_existing_nine_domain_roles_and_classifier_definitions() -> None:
    mapping = json.loads(MAPPING.read_text())
    hd_contract = json.loads(
        (
            ROOT / "reference/core/survey_v2_human_measurement_scoring_contract_v1_0_0.json"
        ).read_text()
    )
    behavioral_contract = json.loads(CONTRACT.read_text())
    definitions = {
        row["construct_id"]: row["definition"] for row in behavioral_contract["constructs"]
    }
    roles = hd_contract["domain_measurement"]["domain_roles"]
    assert "development_combined_hypothesis" in mapping["hypothesis_scope"]
    for row in mapping["mapping"]:
        assert row["target_contract_definition"] == definitions[row["construct_id"]]
        key = row["existing_role_key"]
        if key is None:
            assert row["planet"] == "sun"
            continue
        assert row["existing_chart_blind_role_text"] == roles[key]["role"]


def test_freeze_then_compare_requires_preclassification_predictor_commitment(
    tmp_path: Path,
) -> None:
    import hashlib

    factor_flags_path = tmp_path / "flags.json"
    factor_flags = {
        body: {name: False for name in CF003_PUBLISHED_WEIGHTS} for body in CF003_CANDIDATE_BODIES
    }
    factor_flags["mars"]["major_aspect_to_moon"] = True
    factor_flags_path.write_text(
        json.dumps(
            {
                "schema_version": "cf003-factor-flags-v0",
                "factor_extraction_convention_id": "development-test-convention-v0",
                "exact_historical_mastro_factor_extraction_reproduced": False,
                "factor_flags": factor_flags,
            }
        )
    )
    predictor_path = tmp_path / "predictor.json"
    subprocess.run(
        [
            sys.executable,
            str(PREDICTOR_FREEZER_PATH),
            "--factor-flags",
            str(factor_flags_path),
            "--output",
            str(predictor_path),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    predictor_hash = hashlib.sha256(predictor_path.read_bytes()).hexdigest()

    builder = _builder_module()
    source = tmp_path / "source.json"
    _write_behavioral_source(
        source,
        "This is a recurring source phrase across settings and it matters to me.",
    )
    packet_path = tmp_path / "packet.json"
    packet = builder.build_packet(source, CONTRACT, prompt_path=PROMPT)
    packet_path.write_text(json.dumps(packet))

    classifier = _complete_classifier_payload(2)
    for item in classifier["construct_scores"]:
        for quote in item["support_quotes"]:
            quote["turn_id"] = "primary-0001"
    classifier_path = tmp_path / "classifier.json"
    classifier_path.write_text(json.dumps(classifier))
    frozen_path = tmp_path / "target.json"

    subprocess.run(
        [
            sys.executable,
            str(FREEZER_PATH),
            "--packet",
            str(packet_path),
            "--classifier-output",
            str(classifier_path),
            "--classifier-model",
            "test-classifier-v0",
            "--predictor-sha256",
            predictor_hash,
            "--mapping",
            str(MAPPING),
            "--manifest",
            str(MANIFEST),
            "--output",
            str(frozen_path),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    frozen = json.loads(frozen_path.read_text())
    assert frozen["predictor_commitment_sha256"] == predictor_hash
    assert frozen["classifier_run"]["model"] == "test-classifier-v0"
    assert frozen["behavioral_target_complete"] is True
    assert set(frozen["planet_scores"]) == set(CF003_CANDIDATE_BODIES)

    comparison_path = tmp_path / "comparison.json"
    subprocess.run(
        [
            sys.executable,
            str(COMPARER_PATH),
            "--target",
            str(frozen_path),
            "--predictor",
            str(predictor_path),
            "--manifest",
            str(MANIFEST),
            "--output",
            str(comparison_path),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    comparison = json.loads(comparison_path.read_text())
    assert comparison["predictor_commitment_verified"] is True
    assert comparison["primary_endpoint"]["name"] == "predicted_top_set_mean_behavioral_midrank"

    predictor = json.loads(predictor_path.read_text())
    predictor["planet_scores"]["venus"] = 41.2
    predictor_path.write_text(json.dumps(predictor))
    failed = subprocess.run(
        [
            sys.executable,
            str(COMPARER_PATH),
            "--target",
            str(frozen_path),
            "--predictor",
            str(predictor_path),
            "--manifest",
            str(MANIFEST),
            "--output",
            str(tmp_path / "should-not-exist.json"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert failed.returncode != 0
    assert "preclassification commitment" in failed.stderr


def test_manifest_hashes_pin_target_and_implementation_files() -> None:
    import hashlib

    manifest = json.loads(MANIFEST.read_text())
    for item in manifest["files"].values():
        source = ROOT / item["path"]
        assert hashlib.sha256(source.read_bytes()).hexdigest() == item["sha256"]
    for relative, expected in manifest["implementation_files"].items():
        source = ROOT / relative
        assert hashlib.sha256(source.read_bytes()).hexdigest() == expected
    assert manifest["separation"]["primary_tn001_changed"] is False
    assert manifest["separation"]["main_life_patterns_score_changed"] is False
    assert manifest["behavioral_target"]["participant_visible_hidden_labels"] is False
    assert manifest["null"]["type"].startswith("complete_behavioral_profile_reassignment")
    assert (
        manifest["chart_predictor_status"]["exact_historical_mastro_factor_extraction_reproduced"]
        is False
    )
