from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from hdmatch.human.dataset import HumanCase, HumanDataset
from hdmatch.human.empirical import EmpiricalChartResponseModel
from hdmatch.human.protocol import (
    FINAL_TEST_RELEASE_ACKNOWLEDGEMENT,
    BoundSymbolicScorer,
    HumanBlindCase,
    HumanCandidate,
    HumanCohortAnswerKey,
    SymbolicModelReference,
    fit_development_model_bundle,
    freeze_final_test_protocol,
    freeze_human_evaluation_protocol,
    freeze_human_predictions,
    reveal_and_evaluate_human_cohort,
    score_blind_human_cohort,
)
from hdmatch.human.splits import create_person_splits, select_partition

NOW = datetime(2026, 8, 21, 12, 0, tzinfo=UTC)


def _human(
    participant_id: str,
    cohort: str,
    *,
    answer: str,
    chart_type: str,
    month: int,
    day: int,
) -> HumanCase:
    return HumanCase(
        participant_id=participant_id,
        cohort=cohort,
        responses={"Q1": answer},
        chart_features={"type": chart_type},
        birth_year=2000,
        birth_month=month,
        birth_day=day,
    )


def _dataset() -> HumanDataset:
    return HumanDataset(
        questionnaire_version="Q1",
        cases=(
            _human("D1", "development", answer="yes", chart_type="G", month=1, day=2),
            _human("D2", "development", answer="yes", chart_type="G", month=1, day=3),
            _human("D3", "development", answer="no", chart_type="P", month=7, day=2),
            _human("D4", "development", answer="no", chart_type="P", month=7, day=3),
            _human("V1", "validation", answer="yes", chart_type="G", month=2, day=1),
            _human("V2", "validation", answer="no", chart_type="P", month=8, day=1),
            _human("F1", "final_test", answer="yes", chart_type="G", month=3, day=1),
            _human("F2", "final_test", answer="no", chart_type="P", month=9, day=1),
        ),
    )


def _symbolic_reference() -> SymbolicModelReference:
    return SymbolicModelReference(
        model_id="MODEL-A-CORE-V1",
        model_sha256="1" * 64,
        mapping_sha256="2" * 64,
    )


def _symbolic_score(
    responses: dict[str, str] | object,
    chart_features: dict[str, object] | object,
    _reliability: dict[str, float] | object,
) -> float:
    assert isinstance(responses, dict)
    assert isinstance(chart_features, dict)
    expected = "yes" if chart_features.get("type") == "G" else "no"
    return 2.0 if responses.get("Q1") == expected else -2.0


def _bundle_and_manifest():  # type: ignore[no-untyped-def]
    dataset = _dataset()
    manifest = create_person_splits(dataset, seed=9)
    bundle = fit_development_model_bundle(
        select_partition(dataset, manifest, "development"),
        manifest=manifest,
        bundle_id="HUMAN-MODELS-1",
        questionnaire_version="Q1",
        symbolic_model=_symbolic_reference(),
        empirical_feature_names=("type",),
        permutation_count=3,
        permutation_seed=17,
        created_at_utc=NOW,
    )
    return bundle, manifest


def _blind_case(participant_id: str, cohort: str, answer: str) -> HumanBlindCase:
    return HumanBlindCase(
        participant_id=participant_id,
        cohort=cohort,
        questionnaire_version="Q1",
        responses={"Q1": answer},
        response_reliability={"Q1": 1.0},
        candidates=(
            HumanCandidate(
                candidate_id="G-CANDIDATE",
                chart_features={"type": "G"},
                local_year=2000,
                local_month=2,
                local_day=1,
            ),
            HumanCandidate(
                candidate_id="P-CANDIDATE",
                chart_features={"type": "P"},
                local_year=2000,
                local_month=8,
                local_day=1,
            ),
        ),
    )


def _validation_protocol():  # type: ignore[no-untyped-def]
    bundle, manifest = _bundle_and_manifest()
    protocol = freeze_human_evaluation_protocol(
        bundle,
        manifest,
        protocol_id="VALIDATION-1",
        cohort="validation",
        candidate_universe_rule="two fixed candidates in this test fixture",
        selected_primary_method="hybrid_hd",
        created_at_utc=NOW,
    )
    return bundle, protocol


def test_model_bundle_fits_development_only_and_freezes_all_controls() -> None:
    bundle, manifest = _bundle_and_manifest()
    assert bundle.development_participant_ids == manifest.development_ids
    assert bundle.calendar_season_model is not None
    assert len(bundle.permuted_hd_models) == 3
    assert bundle.claim_scope == "development-fitted-models-not-predictive-validation"

    with pytest.raises(ValueError, match="development"):
        fit_development_model_bundle(
            select_partition(_dataset(), manifest, "validation"),
            manifest=manifest,
            bundle_id="LEAK",
            questionnaire_version="Q1",
            symbolic_model=_symbolic_reference(),
            empirical_feature_names=("type",),
            created_at_utc=NOW,
        )


def test_model_bundle_requires_exact_development_people() -> None:
    dataset = _dataset()
    manifest = create_person_splits(dataset, seed=9)
    development = select_partition(dataset, manifest, "development")
    with pytest.raises(ValueError, match="exactly"):
        fit_development_model_bundle(
            development[:-1],
            manifest=manifest,
            bundle_id="INCOMPLETE",
            questionnaire_version="Q1",
            symbolic_model=_symbolic_reference(),
            empirical_feature_names=("type",),
            created_at_utc=NOW,
        )


def test_theory_priors_are_normalized_and_frozen_in_empirical_artifact() -> None:
    dataset = _dataset()
    manifest = create_person_splits(dataset, seed=9)
    model = EmpiricalChartResponseModel.fit(
        select_partition(dataset, manifest, "development"),
        model_id="HYBRID-PRIOR",
        questionnaire_version="Q1",
        split_manifest_hash="0" * 64,
        feature_names=("type",),
        theory_priors={"Q1": {"yes": 3.0, "no": 1.0}},
        theory_strength=0.5,
        created_at_utc=NOW,
    )
    assert model.artifact.theory_priors["Q1"] == {"no": 0.25, "yes": 0.75}
    reloaded = EmpiricalChartResponseModel(model.artifact)
    assert reloaded.theory_priors == model.artifact.theory_priors
    with pytest.raises(ValueError, match="do not match"):
        EmpiricalChartResponseModel(
            model.artifact,
            theory_priors={"Q1": {"yes": 1.0, "no": 1.0}},
        )


def test_development_reliability_only_downweights_empirical_counts() -> None:
    cases = (
        HumanCase(
            participant_id="R1",
            cohort="development",
            responses={"Q1": "yes"},
            response_reliability={"Q1": 0.0},
            chart_features={"type": "G"},
        ),
        HumanCase(
            participant_id="R2",
            cohort="development",
            responses={"Q1": "no"},
            response_reliability={"Q1": 1.0},
            chart_features={"type": "G"},
        ),
    )
    model = EmpiricalChartResponseModel.fit(
        cases,
        model_id="RELIABILITY",
        questionnaire_version="Q1",
        split_manifest_hash="0" * 64,
        feature_names=("type",),
        created_at_utc=NOW,
    )
    assert model.artifact.marginal_counts["Q1"] == {"yes": 0.0, "no": 1.0}
    distribution = model.response_distribution("Q1", {"type": "G"})
    assert distribution["no"] > distribution["yes"]


def test_blind_schema_rejects_truth_fields() -> None:
    payload = _blind_case("V1", "validation", "yes").model_dump(mode="json")
    payload["true_candidate_id"] = "G-CANDIDATE"
    with pytest.raises(ValidationError, match="true_candidate_id"):
        HumanBlindCase.model_validate(payload)


def test_validation_comparison_requires_freeze_and_reports_all_baselines() -> None:
    bundle, protocol = _validation_protocol()
    cases = (
        _blind_case("V1", "validation", "yes"),
        _blind_case("V2", "validation", "no"),
    )
    predictions = score_blind_human_cohort(
        cases,
        bundle=bundle,
        protocol=protocol,
        symbolic_scorer=BoundSymbolicScorer(_symbolic_reference(), _symbolic_score),
        created_at_utc=NOW,
    )
    freeze = freeze_human_predictions(
        predictions,
        bundle=bundle,
        protocol=protocol,
        created_at_utc=NOW,
    )
    key = HumanCohortAnswerKey(
        cohort="validation",
        protocol_sha256=protocol.sha256,
        true_candidate_ids={"V1": "G-CANDIDATE", "V2": "P-CANDIDATE"},
    )
    report = reveal_and_evaluate_human_cohort(
        predictions,
        freeze,
        key,
        bundle=bundle,
        protocol=protocol,
        evaluated_at_utc=NOW,
    )
    by_method = {item.method_id: item for item in report.method_evaluations}
    assert {
        "symbolic_v4",
        "empirical_hd",
        "hybrid_hd",
        "calendar_season",
        "uniform_chance",
        "permuted_hd_000",
    } <= set(by_method)
    assert by_method["symbolic_v4"].metrics.top_1 == 1.0
    assert by_method["uniform_chance"].metrics.top_1 == 0.5
    assert report.permutation_baseline.null_mean_reciprocal_ranks
    assert report.permutation_baseline.permutation_count == 3
    assert report.permutation_baseline.minimum_attainable_p_value == 0.25
    assert "internal validation" in report.claim_boundary
    for artifact, timestamp_field in (
        (predictions, "created_at_utc"),
        (freeze, "created_at_utc"),
        (report, "evaluated_at_utc"),
    ):
        payload = artifact.model_dump(mode="python")
        payload[timestamp_field] = datetime(2026, 8, 21, 12, 0)
        with pytest.raises(ValidationError, match="timezone-aware"):
            type(artifact).model_validate(payload)


def test_predictions_changed_after_freeze_are_rejected() -> None:
    bundle, protocol = _validation_protocol()
    predictions = score_blind_human_cohort(
        (
            _blind_case("V1", "validation", "yes"),
            _blind_case("V2", "validation", "no"),
        ),
        bundle=bundle,
        protocol=protocol,
        symbolic_scorer=BoundSymbolicScorer(_symbolic_reference(), _symbolic_score),
        created_at_utc=NOW,
    )
    freeze = freeze_human_predictions(
        predictions, bundle=bundle, protocol=protocol, created_at_utc=NOW
    )
    changed = predictions.model_copy(update={"created_at_utc": NOW + timedelta(seconds=1)})
    key = HumanCohortAnswerKey(
        cohort="validation",
        protocol_sha256=protocol.sha256,
        true_candidate_ids={"V1": "G-CANDIDATE", "V2": "P-CANDIDATE"},
    )
    with pytest.raises(ValueError, match="changed after freeze"):
        reveal_and_evaluate_human_cohort(changed, freeze, key, bundle=bundle, protocol=protocol)


def test_final_test_requires_explicit_one_time_release_and_matching_key() -> None:
    bundle, manifest = _bundle_and_manifest()
    with pytest.raises(PermissionError, match="explicit"):
        freeze_final_test_protocol(
            bundle,
            manifest,
            protocol_id="FINAL-1",
            candidate_universe_rule="two fixed candidates in this test fixture",
            selected_primary_method="hybrid_hd",
            final_test_release_id="RELEASE-1",
            release_authorization="not-authorized",
            created_at_utc=NOW,
        )
    protocol = freeze_final_test_protocol(
        bundle,
        manifest,
        protocol_id="FINAL-1",
        candidate_universe_rule="two fixed candidates in this test fixture",
        selected_primary_method="hybrid_hd",
        final_test_release_id="RELEASE-1",
        release_authorization=FINAL_TEST_RELEASE_ACKNOWLEDGEMENT,
        created_at_utc=NOW,
    )
    assert protocol.final_test_release_acknowledgement == FINAL_TEST_RELEASE_ACKNOWLEDGEMENT
    predictions = score_blind_human_cohort(
        (
            _blind_case("F1", "final_test", "yes"),
            _blind_case("F2", "final_test", "no"),
        ),
        bundle=bundle,
        protocol=protocol,
        symbolic_scorer=BoundSymbolicScorer(_symbolic_reference(), _symbolic_score),
        created_at_utc=NOW,
    )
    freeze = freeze_human_predictions(
        predictions, bundle=bundle, protocol=protocol, created_at_utc=NOW
    )
    wrong_key = HumanCohortAnswerKey(
        cohort="final_test",
        protocol_sha256=protocol.sha256,
        true_candidate_ids={"F1": "G-CANDIDATE", "F2": "P-CANDIDATE"},
        final_test_release_id="WRONG-RELEASE",
    )
    with pytest.raises(ValueError, match="release"):
        reveal_and_evaluate_human_cohort(
            predictions, freeze, wrong_key, bundle=bundle, protocol=protocol
        )
    correct_key = wrong_key.model_copy(update={"final_test_release_id": "RELEASE-1"})
    report = reveal_and_evaluate_human_cohort(
        predictions,
        freeze,
        correct_key,
        bundle=bundle,
        protocol=protocol,
        evaluated_at_utc=NOW,
    )
    assert "untouched" in report.claim_boundary
    assert any("cannot enforce global one-time use" in warning for warning in report.warnings)


def test_unevaluable_methods_and_missing_truth_remain_in_denominator() -> None:
    bundle, protocol = _validation_protocol()
    no_calendar = HumanBlindCase(
        participant_id="V1",
        cohort="validation",
        questionnaire_version="Q1",
        responses={"Q1": "yes"},
        candidates=(
            HumanCandidate(candidate_id="G-CANDIDATE", chart_features={"type": "G"}),
            HumanCandidate(candidate_id="P-CANDIDATE", chart_features={"type": "P"}),
        ),
    )
    predictions = score_blind_human_cohort(
        (no_calendar, _blind_case("V2", "validation", "no")),
        bundle=bundle,
        protocol=protocol,
        symbolic_scorer=BoundSymbolicScorer(_symbolic_reference(), _symbolic_score),
        created_at_utc=NOW,
    )
    freeze = freeze_human_predictions(
        predictions, bundle=bundle, protocol=protocol, created_at_utc=NOW
    )
    key = HumanCohortAnswerKey(
        cohort="validation",
        protocol_sha256=protocol.sha256,
        true_candidate_ids={"V1": "G-CANDIDATE"},
    )
    report = reveal_and_evaluate_human_cohort(
        predictions, freeze, key, bundle=bundle, protocol=protocol, evaluated_at_utc=NOW
    )
    calendar = next(
        item for item in report.method_evaluations if item.method_id == "calendar_season"
    )
    assert calendar.metrics.case_count == 2
    assert calendar.metrics.evaluated_case_count == 0
    assert calendar.metrics.unevaluable_case_count == 2
    assert {failure.reason for failure in calendar.failures} == {
        "method_unevaluable",
        "answer_key_missing_truth",
    }


def test_symbolic_binding_must_match_frozen_artifact() -> None:
    bundle, protocol = _validation_protocol()
    wrong_reference = _symbolic_reference().model_copy(update={"mapping_sha256": "9" * 64})
    with pytest.raises(ValueError, match="does not match"):
        score_blind_human_cohort(
            (
                _blind_case("V1", "validation", "yes"),
                _blind_case("V2", "validation", "no"),
            ),
            bundle=bundle,
            protocol=protocol,
            symbolic_scorer=BoundSymbolicScorer(wrong_reference, _symbolic_score),
            created_at_utc=NOW,
        )
