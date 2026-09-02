from __future__ import annotations

import inspect
import json
from collections import defaultdict
from pathlib import Path

import pytest
from pydantic import ValidationError

from hdmatch.evaluation.theory_language_exposure import (
    ExposureSignalLevel,
    TranscriptTurn,
    assess_theory_language_exposure,
    load_theory_language_codebook,
)

ROOT = Path(__file__).parents[2]
CODEBOOK_PATH = ROOT / "reference/research/astrohd_theory_language_codebook_v0_1.json"
FIXTURES_PATH = ROOT / "reference/research/astrohd_theory_language_exposure_fixtures_v0_1.json"


def _assess_cases() -> dict[str, object]:
    codebook, codebook_sha256 = load_theory_language_codebook(CODEBOOK_PATH)
    fixture_payload = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))
    assessments: dict[str, object] = {}
    for case in fixture_payload["cases"]:
        assessment = assess_theory_language_exposure(
            tuple(TranscriptTurn.model_validate(turn) for turn in case["transcript"]),
            codebook=codebook,
            codebook_sha256=codebook_sha256,
        )
        expected = case["expected"]
        assert assessment.signal_level.value == expected["signal_level"]
        assert assessment.language_assessability.value == expected["language_assessability"]
        assert len(assessment.matches) == expected["participant_match_count"]
        assert [match.source.value for match in assessment.matches] == expected["sources"]
        assert [match.stance.value for match in assessment.matches] == expected["stances"]
        assessments[case["case_id"]] = assessment
    return assessments


def test_synthetic_dry_run_cases() -> None:
    assessments = _assess_cases()

    assert (
        assessments["quoted_and_rejected_terminology"].signal_level
        is ExposureSignalLevel.THEORY_SPECIFIC_EXPOSURE_SIGNAL_PRESENT
    )
    assert all(
        match.stance.value == "explicit_rejection"
        for match in assessments["quoted_and_rejected_terminology"].matches
    )


def test_identical_transcript_is_chart_blind_and_deterministic() -> None:
    assessments = _assess_cases()
    copy_a = assessments["chart_isolation_copy_a"]
    copy_b = assessments["chart_isolation_copy_b"]

    assert copy_a == copy_b
    assert copy_a.chart_and_prediction_inputs_absent is True
    assert copy_a.causal_contamination_inference_permitted is False
    parameters = inspect.signature(assess_theory_language_exposure).parameters
    forbidden_names = {
        "birth",
        "chart",
        "prediction",
        "score",
        "result",
        "confidence",
        "hit",
        "miss",
    }
    assert forbidden_names.isdisjoint(parameters)


def test_consequences_are_diagnostic_only() -> None:
    for assessment in _assess_cases().values():
        consequences = assessment.consequences
        assert consequences.diagnostic_or_stratification_only is True
        assert consequences.eligibility_unchanged is True
        assert consequences.questionnaire_flow_unchanged is True
        assert consequences.scoring_unchanged is True
        assert consequences.primary_analysis_unchanged is True


def test_codebook_is_draft_and_rejects_duplicate_expressions() -> None:
    codebook, _ = load_theory_language_codebook(CODEBOOK_PATH)
    assert codebook.status == "draft_evaluation_only_not_validated"
    assert codebook.supported_languages == ("en",)
    assert len(codebook.forbidden_uses) >= 7

    payload = codebook.model_dump(mode="json")
    payload["entries"][1]["expressions"].append(payload["entries"][0]["expressions"][0])
    with pytest.raises(ValidationError, match="expressions must be unique"):
        type(codebook).model_validate(payload)


def test_fixture_comparison_groups_have_identical_assessments() -> None:
    assessments = _assess_cases()
    payload = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))
    groups: dict[str, list[str]] = defaultdict(list)
    for case in payload["cases"]:
        if group := case.get("comparison_group"):
            groups[group].append(case["case_id"])

    assert groups
    for case_ids in groups.values():
        assert len(case_ids) >= 2
        reference = assessments[case_ids[0]]
        assert all(assessments[case_id] == reference for case_id in case_ids[1:])
