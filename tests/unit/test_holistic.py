from __future__ import annotations

from datetime import UTC, datetime

import pytest

from hdmatch.human.holistic import (
    CandidateChart,
    HolisticPositiveEvidenceModel,
    PositiveEvidenceRecord,
    evaluate_identification,
    greedy_minimize_feature_groups,
)


def _record(
    participant_id: str,
    *,
    cohort: str = "development",
    label: str,
    features: dict[str, object],
    sex: str = "x",
) -> PositiveEvidenceRecord:
    return PositiveEvidenceRecord(
        participant_id=participant_id,
        cohort=cohort,
        observed_labels=(label,),
        chart_features=features,
        match_strata={"sex": sex},
    )


def _training_records() -> list[PositiveEvidenceRecord]:
    records: list[PositiveEvidenceRecord] = []
    for index in range(80):
        signal = "A" if index < 40 else "B"
        label = "L" if signal == "A" else "M"
        records.append(
            _record(
                f"train-{index}",
                label=label,
                features={
                    "signal": signal,
                    "duplicate_signal": signal,
                    "constant_noise": "same",
                },
            )
        )
    return records


def _model() -> HolisticPositiveEvidenceModel:
    return HolisticPositiveEvidenceModel.fit(
        _training_records(),
        model_id="synthetic-holistic-v1",
        feature_names=("signal", "duplicate_signal", "constant_noise"),
        feature_clusters={
            "signal": "signal_cluster",
            "duplicate_signal": "signal_cluster",
            "constant_noise": "noise_cluster",
        },
        alpha=4.0,
        min_label_count=5,
        created_at_utc=datetime(2026, 8, 24, tzinfo=UTC),
    )


def test_fit_is_development_only() -> None:
    validation = _record(
        "v1",
        cohort="validation",
        label="L",
        features={"signal": "A"},
    )
    with pytest.raises(ValueError, match="DEVELOPMENT"):
        HolisticPositiveEvidenceModel.fit(
            [validation],
            model_id="bad",
            feature_names=("signal",),
        )


def test_positive_evidence_scores_matching_chart_above_mismatch() -> None:
    model = _model()
    matching = model.score(("L",), {"signal": "A", "duplicate_signal": "A"})
    mismatch = model.score(("L",), {"signal": "B", "duplicate_signal": "B"})
    assert matching > mismatch


def test_missing_labels_are_unknown_not_negative_evidence() -> None:
    model = _model()
    chart = {
        "signal": "A",
        "duplicate_signal": "A",
        "constant_noise": "same",
    }
    score = model.score(("L",), chart)
    assert score == model.score(("L",), chart, evidence_weights={"L": 1.0})


def test_dependency_cluster_prevents_duplicate_feature_double_counting() -> None:
    model = _model()
    chart = {"signal": "A", "duplicate_signal": "A"}
    one = model.score(("L",), chart, enabled_features=("signal",))
    two = model.score(
        ("L",),
        chart,
        enabled_features=("signal", "duplicate_signal"),
    )
    assert two == pytest.approx(one)


def test_whole_profile_identification_recovers_injected_law() -> None:
    model = _model()
    people: list[PositiveEvidenceRecord] = []
    charts: list[CandidateChart] = []
    for index in range(30):
        signal = "A" if index % 2 == 0 else "B"
        label = "L" if signal == "A" else "M"
        participant_id = f"dev-{index}"
        features = {
            "signal": signal,
            "duplicate_signal": signal,
            "constant_noise": "same",
        }
        people.append(_record(participant_id, label=label, features=features))
        charts.append(
            CandidateChart(
                chart_id=f"chart-{index}",
                owner_participant_id=participant_id,
                chart_features=features,
                match_strata={"sex": "x"},
            )
        )

    result = evaluate_identification(
        model,
        people,
        charts,
        match_fields=("sex",),
        max_decoys=10,
        seed=11,
        randomization_iterations=500,
    )

    assert result.people_evaluated == 30
    assert result.mean_percentile > 0.70
    assert result.randomization_p_value is not None
    assert result.randomization_p_value < 0.05


def test_matched_decoys_hold_declared_strata_fixed() -> None:
    model = _model()
    person = _record(
        "target",
        label="L",
        features={
            "signal": "A",
            "duplicate_signal": "A",
            "constant_noise": "same",
        },
        sex="f",
    )
    true_chart = CandidateChart(
        chart_id="true",
        owner_participant_id="target",
        chart_features=person.chart_features,
        match_strata={"sex": "f"},
    )
    wrong_stratum = CandidateChart(
        chart_id="wrong-sex",
        owner_participant_id="other",
        chart_features={
            "signal": "B",
            "duplicate_signal": "B",
            "constant_noise": "same",
        },
        match_strata={"sex": "m"},
    )
    right_stratum = CandidateChart(
        chart_id="right-sex",
        owner_participant_id="other-2",
        chart_features={
            "signal": "B",
            "duplicate_signal": "B",
            "constant_noise": "same",
        },
        match_strata={"sex": "f"},
    )

    result = evaluate_identification(
        model,
        [person],
        [true_chart, wrong_stratum, right_stratum],
        match_fields=("sex",),
    )
    assert result.results[0].candidate_count == 2


def test_minimization_removes_noninformative_group_without_touching_signal() -> None:
    model = _model()
    people: list[PositiveEvidenceRecord] = []
    charts: list[CandidateChart] = []
    for index in range(24):
        signal = "A" if index % 2 == 0 else "B"
        label = "L" if signal == "A" else "M"
        participant_id = f"dev-{index}"
        features = {
            "signal": signal,
            "duplicate_signal": signal,
            "constant_noise": "same",
        }
        people.append(_record(participant_id, label=label, features=features))
        charts.append(
            CandidateChart(
                chart_id=f"chart-{index}",
                owner_participant_id=participant_id,
                chart_features=features,
                match_strata={"sex": "x"},
            )
        )

    result = greedy_minimize_feature_groups(
        model,
        people,
        charts,
        feature_groups={
            "signal": ("signal", "duplicate_signal"),
            "noise": ("constant_noise",),
        },
        match_fields=("sex",),
        max_decoys=10,
        seed=9,
        max_absolute_percentile_loss=0.001,
    )

    assert result.retained_groups == ("signal",)
    assert set(result.retained_features) == {"signal", "duplicate_signal"}
    assert len(result.path) == 2
