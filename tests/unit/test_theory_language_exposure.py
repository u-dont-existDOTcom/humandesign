from __future__ import annotations

import importlib.util
import inspect
import json
from pathlib import Path
from types import ModuleType

from hdmatch.evaluation.theory_language_exposure import (
    LanguageAssessability,
    LexicalSpecificity,
    OccurrenceProvenance,
    ParticipantStance,
    TheoryLanguageExposureAssessment,
    TranscriptTurn,
    assess_theory_language_exposure,
    load_theory_language_codebook,
)

ROOT = Path(__file__).parents[2]
CODEBOOK_PATH = ROOT / "reference/core/astrohd_theory_language_codebook_v1.template.json"
FIXTURE_PATH = ROOT / "reference/core/astrohd_theory_language_exposure_synthetic_fixtures_v1.json"


def _runner() -> ModuleType:
    path = ROOT / "scripts" / "audit_astrohd_theory_language_exposure.py"
    spec = importlib.util.spec_from_file_location("audit_astrohd_theory_language_exposure", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _assessment(case_id: str) -> TheoryLanguageExposureAssessment:
    codebook, codebook_sha256 = load_theory_language_codebook(CODEBOOK_PATH)
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    case = next(case for case in payload["cases"] if case["case_id"] == case_id)
    transcript = tuple(TranscriptTurn.model_validate(turn) for turn in case["transcript"])
    return assess_theory_language_exposure(
        transcript,
        codebook=codebook,
        codebook_sha256=codebook_sha256,
    )


def test_all_nine_synthetic_fixtures_pass() -> None:
    report = _runner().run_synthetic_fixtures(CODEBOOK_PATH, FIXTURE_PATH)

    assert report["case_count"] == 9
    assert report["passed_case_count"] == 9
    assert all(case["expectation_passed"] for case in report["cases"])
    assert all(case["chart_isolation_passed"] for case in report["cases"])


def test_interviewer_first_same_phrase_is_not_spontaneous() -> None:
    assessment = _assessment("interviewer_first_same_term")

    assert len(assessment.occurrences) == 1
    assert (
        assessment.occurrences[0].provenance
        is OccurrenceProvenance.PARTICIPANT_AFTER_INTERVIEWER_SAME_TERM
    )


def test_ordinary_exclusion_and_context_dependent_are_not_promoted() -> None:
    ordinary = _assessment("ordinary_language_excluded")
    context = _assessment("context_dependent_remains_context_dependent")

    assert ordinary.theory_specific_exposure_evidence_present is False
    assert ordinary.occurrences[0].lexical_specificity is (
        LexicalSpecificity.ORDINARY_LANGUAGE_EXCLUDED
    )
    assert context.theory_specific_exposure_evidence_present is False
    assert context.occurrences[0].lexical_specificity is LexicalSpecificity.CONTEXT_DEPENDENT


def test_explicit_stance_is_preserved_independently_from_occurrence() -> None:
    quoted = _assessment("quoted_term_with_explicit_stance")
    rejected = _assessment("rejected_term_with_explicit_stance")

    assert quoted.theory_specific_exposure_evidence_present is True
    assert quoted.occurrences[0].stance is ParticipantStance.NEUTRAL_OR_QUOTED
    assert quoted.occurrences[0].provenance is OccurrenceProvenance.QUOTED_OR_REPORTED_SOURCE
    assert rejected.theory_specific_exposure_evidence_present is True
    assert rejected.occurrences[0].stance is ParticipantStance.REJECTED


def test_runtime_stance_defaults_to_unknown_without_authorized_annotation() -> None:
    spontaneous = _assessment("participant_spontaneous_theoryterm")

    assert spontaneous.occurrences[0].stance is ParticipantStance.STANCE_UNKNOWN


def test_unsupported_and_absent_language_metadata_fail_closed() -> None:
    unsupported = _assessment("supplied_language_has_no_codebook")
    absent = _assessment("response_language_metadata_absent")

    assert unsupported.language_assessability is LanguageAssessability.NOT_ASSESSABLE
    assert unsupported.occurrences == ()
    assert absent.language_assessability is LanguageAssessability.LANGUAGE_UNKNOWN
    assert absent.occurrences == ()


def test_hidden_chart_payload_has_no_input_path_and_cannot_change_output() -> None:
    parameters = inspect.signature(assess_theory_language_exposure).parameters
    forbidden_inputs = {
        "birth_data",
        "target_chart",
        "chart_classifications",
        "predicted_traits",
        "scoring_results",
        "rule_matches",
        "prediction_fit",
        "model_confidence",
        "hit_miss_status",
        "downstream_outcomes",
    }
    assert forbidden_inputs.isdisjoint(parameters)

    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    case = next(case for case in payload["cases"] if case["case_id"] == "hidden_chart_isolation")
    assert len(case["synthetic_hidden_chart_payloads"]) == 2
    assessment = _assessment("hidden_chart_isolation")
    serialized_by_hidden_payload = [
        assessment.model_dump_json() for _hidden_payload in case["synthetic_hidden_chart_payloads"]
    ]
    assert serialized_by_hidden_payload[0] == serialized_by_hidden_payload[1]
    assert assessment.target_chart_and_prediction_inputs_absent is True
    assert assessment.participant_effects == "none_diagnostic_metadata_only"


def test_matching_is_normalized_exact_phrase_only_without_fuzzy_path() -> None:
    codebook, codebook_sha256 = load_theory_language_codebook(CODEBOOK_PATH)

    normalized = assess_theory_language_exposure(
        (
            TranscriptTurn(
                turn_id="TURN-normalized",
                speaker="participant",
                text="ＴＨＥＯＲＹＴＥＲＭ＿ＡＬＰＨＡ\n",
                response_language="x-synthetic",
            ),
        ),
        codebook=codebook,
        codebook_sha256=codebook_sha256,
    )
    near_matches = assess_theory_language_exposure(
        (
            TranscriptTurn(
                turn_id="TURN-near-matches",
                speaker="participant",
                text="XTHEORYTERM_ALPHA THEORYTERM_ALPH THEORYPHRASE_BETA",
                response_language="x-synthetic",
            ),
        ),
        codebook=codebook,
        codebook_sha256=codebook_sha256,
    )
    whitespace_normalized = assess_theory_language_exposure(
        (
            TranscriptTurn(
                turn_id="TURN-whitespace",
                speaker="participant",
                text="theory   phrase\n beta",
                response_language="x-synthetic",
            ),
        ),
        codebook=codebook,
        codebook_sha256=codebook_sha256,
    )

    assert normalized.matching_policy == "frozen_exact_phrase_only"
    assert len(normalized.occurrences) == 1
    assert len(whitespace_normalized.occurrences) == 1
    assert near_matches.occurrences == ()

    source = (
        (ROOT / "src/hdmatch/evaluation/theory_language_exposure.py")
        .read_text(encoding="utf-8")
        .casefold()
    )
    assert all(
        forbidden not in source
        for forbidden in ("embedding", "fuzzy", "stemming", "ontology", "similarity", "llm")
    )


def test_codebook_contains_only_synthetic_placeholders_and_no_score_or_threshold() -> None:
    payload = json.loads(CODEBOOK_PATH.read_text(encoding="utf-8"))

    assert {entry["exact_phrase"] for entry in payload["entries"]} == {
        "THEORYTERM_ALPHA",
        "THEORY PHRASE BETA",
        "CONTEXTTERM_DELTA",
        "COMMONWORD_GAMMA",
    }
    forbidden_fields = {"score", "threshold", "contamination_score"}
    assert all(forbidden_fields.isdisjoint(entry) for entry in payload["entries"])
    assert forbidden_fields.isdisjoint(payload)
