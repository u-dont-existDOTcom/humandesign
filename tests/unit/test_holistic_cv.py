from __future__ import annotations

from datetime import UTC, datetime

import pytest

from hdmatch.human.holistic import CandidateChart, PositiveEvidenceRecord
from hdmatch.human.holistic_cv import (
    cross_fitted_identification,
    deterministic_person_fold,
    greedy_cross_fitted_minimize_feature_groups,
)


def _dataset(count: int = 60) -> tuple[list[PositiveEvidenceRecord], list[CandidateChart]]:
    records: list[PositiveEvidenceRecord] = []
    charts: list[CandidateChart] = []
    for index in range(count):
        signal = "A" if index % 2 == 0 else "B"
        label = "L" if signal == "A" else "M"
        participant_id = f"p-{index}"
        features = {"signal": signal, "noise": "same"}
        records.append(
            PositiveEvidenceRecord(
                participant_id=participant_id,
                cohort="development",
                observed_labels=(label,),
                chart_features=features,
                match_strata={"sex": "x"},
            )
        )
        charts.append(
            CandidateChart(
                chart_id=f"chart-{index}",
                owner_participant_id=participant_id,
                chart_features=features,
                match_strata={"sex": "x"},
            )
        )
    return records, charts


def test_deterministic_person_fold_is_stable_and_bounded() -> None:
    first = deterministic_person_fold("person-1", folds=5, seed=7)
    second = deterministic_person_fold("person-1", folds=5, seed=7)
    assert first == second
    assert 0 <= first < 5


def test_cross_fitted_identification_recovers_injected_signal() -> None:
    records, charts = _dataset()
    result = cross_fitted_identification(
        records,
        charts,
        model_id="crossfit-test",
        feature_names=("signal", "noise"),
        feature_clusters={"signal": "signal", "noise": "noise"},
        alpha=4.0,
        min_label_count=5,
        folds=5,
        fold_seed=3,
        match_fields=("sex",),
        max_decoys=15,
        decoy_seed=9,
        created_at_utc=datetime(2026, 8, 24, tzinfo=UTC),
    )
    assert result.people_evaluated == 60
    assert len(result.fold_people_evaluated) == 5
    assert result.mean_percentile > 0.70


def test_cross_fitted_identification_rejects_validation_people() -> None:
    records, charts = _dataset(20)
    records[0] = records[0].model_copy(update={"cohort": "validation"})
    with pytest.raises(ValueError, match="DEVELOPMENT-only"):
        cross_fitted_identification(
            records,
            charts,
            model_id="bad",
            feature_names=("signal", "noise"),
            min_label_count=2,
        )


def test_cross_fitted_minimization_removes_noise() -> None:
    records, charts = _dataset()
    result = greedy_cross_fitted_minimize_feature_groups(
        records,
        charts,
        model_id="crossfit-minimize",
        feature_names=("signal", "noise"),
        feature_groups={"signal": ("signal",), "noise": ("noise",)},
        feature_clusters={"signal": "signal", "noise": "noise"},
        alpha=4.0,
        min_label_count=5,
        folds=5,
        fold_seed=3,
        match_fields=("sex",),
        max_decoys=15,
        decoy_seed=9,
        max_absolute_percentile_loss=0.001,
        created_at_utc=datetime(2026, 8, 24, tzinfo=UTC),
    )
    assert result.retained_groups == ("signal",)
    assert result.retained_features == ("signal",)
    assert len(result.path) == 2
