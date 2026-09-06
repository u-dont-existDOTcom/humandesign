from __future__ import annotations

from datetime import UTC, datetime

import pytest

from hdmatch.evaluation.development_calibration_sampling import (
    build_development_calibration_sample,
    development_calibration_integrity_errors,
    episode_unit_universe,
    human_episode_calibration_tasks,
    human_series_calibration_tasks,
    series_unit_universe,
)
from hdmatch.evaluation.development_series_evidence import DevelopmentSeriesCodingTask
from hdmatch.evaluation.development_transfer_corpus import (
    DevelopmentEpisodeCodingTask,
    DevelopmentSourceSegment,
)


NOW = datetime(2026, 9, 6, 20, 30, tzinfo=UTC)
SEED = "a" * 64
CORPUS_ID = "LPDC-1234567890ABCDEF1234"
CORPUS_SHA = "1" * 64
OBSERVABLES = ("NBM-R01", "NBM-R02", "NBM-R03")


def _segment(prefix: str) -> DevelopmentSourceSegment:
    return DevelopmentSourceSegment(
        segment_id=f"{prefix}-SEG-01",
        exact_text=f"exact source text for {prefix}",
        provenance_refs=(f"SRC-{prefix}",),
    )


def _episode_tasks() -> tuple[DevelopmentEpisodeCodingTask, ...]:
    output = []
    for index in range(1, 5):
        episode_id = f"EP-{index:03d}"
        output.append(
            DevelopmentEpisodeCodingTask(
                task_id=f"LPDT-{index:020X}",
                corpus_id=CORPUS_ID,
                corpus_sha256=CORPUS_SHA,
                episode_id=episode_id,
                domain_id="P01",
                approximate_age_life_phase="adult",
                episode_narrative=f"Synthetic narrative {index}.",
                exact_source_segments=(_segment(episode_id),),
                source_completeness="partial_exact_segments_plus_transfer_summary",
                observable_ids=OBSERVABLES,
                participant_theory_exposure="prior_exposure_possible",
            )
        )
    return tuple(output)


def _series_tasks() -> tuple[DevelopmentSeriesCodingTask, ...]:
    output = []
    for index in range(1, 3):
        series_id = f"SER-{index:03d}"
        output.append(
            DevelopmentSeriesCodingTask(
                task_id=f"LPST-{index:020X}",
                corpus_id=CORPUS_ID,
                corpus_sha256=CORPUS_SHA,
                series_id=series_id,
                domain_id="P01",
                bounded_period_context=f"Synthetic series period {index}.",
                approximate_age_life_phase="adult",
                recurrence_language="many times",
                rough_opportunity_count="at least 3",
                behavior_reportedly_recurred="Synthetic repeated action.",
                exact_source_segments=(_segment(series_id),),
                observable_ids=OBSERVABLES,
                participant_theory_exposure="prior_exposure_possible",
            )
        )
    return tuple(output)


def test_unit_universes_keep_episode_and_series_strata_separate() -> None:
    episode_units = episode_unit_universe(_episode_tasks())
    series_units = series_unit_universe(_series_tasks())
    assert len(episode_units) == 12
    assert len(series_units) == 6
    assert {unit.evidence_kind for unit in episode_units} == {"episode"}
    assert {unit.evidence_kind for unit in series_units} == {"series"}


def test_balanced_sample_is_deterministic_and_covers_each_observable() -> None:
    kwargs = dict(
        episode_tasks=_episode_tasks(),
        series_tasks=_series_tasks(),
        episode_sample_size=6,
        series_sample_size=3,
        episode_per_observable_floor=1,
        series_per_observable_floor=1,
        seed_sha256=SEED,
        created_at_utc=NOW,
    )
    first = build_development_calibration_sample(**kwargs)
    second = build_development_calibration_sample(**kwargs)
    assert first == second
    assert first.payload.selected_before_automated_labels is True
    assert first.payload.no_automated_labels_used_for_selection is True
    assert first.payload.target_model_information_used_for_selection is False
    assert first.payload.validation_use_forbidden is True
    assert len(first.payload.representative_episode_units) == 6
    assert len(first.payload.representative_series_units) == 3
    assert {unit.observable_id for unit in first.payload.representative_episode_units} == set(
        OBSERVABLES
    )
    assert {unit.observable_id for unit in first.payload.representative_series_units} == set(
        OBSERVABLES
    )
    assert development_calibration_integrity_errors(
        first,
        episode_tasks=_episode_tasks(),
        series_tasks=_series_tasks(),
    ) == ()


def test_sample_floor_fails_when_requested_size_is_too_small() -> None:
    with pytest.raises(ValueError, match="too small"):
        build_development_calibration_sample(
            episode_tasks=_episode_tasks(),
            episode_sample_size=2,
            episode_per_observable_floor=1,
            seed_sha256=SEED,
            created_at_utc=NOW,
        )


def test_series_tasks_require_nonzero_series_sample() -> None:
    with pytest.raises(ValueError, match="nonzero"):
        build_development_calibration_sample(
            episode_tasks=_episode_tasks(),
            series_tasks=_series_tasks(),
            episode_sample_size=3,
            series_sample_size=0,
            seed_sha256=SEED,
            created_at_utc=NOW,
        )


def test_invalid_seed_fails_closed() -> None:
    with pytest.raises(ValueError, match="lowercase SHA-256"):
        build_development_calibration_sample(
            episode_tasks=_episode_tasks(),
            episode_sample_size=3,
            seed_sha256="NOT-A-DIGEST",
            created_at_utc=NOW,
        )


def test_human_task_views_contain_only_preselected_units() -> None:
    episode_tasks = _episode_tasks()
    series_tasks = _series_tasks()
    manifest = build_development_calibration_sample(
        episode_tasks=episode_tasks,
        series_tasks=series_tasks,
        episode_sample_size=6,
        series_sample_size=3,
        episode_per_observable_floor=1,
        series_per_observable_floor=1,
        seed_sha256=SEED,
        created_at_utc=NOW,
    )
    episode_view = human_episode_calibration_tasks(episode_tasks, manifest)
    series_view = human_series_calibration_tasks(episode_tasks, series_tasks, manifest)
    episode_units = {
        (task.episode_id, observable_id)
        for task in episode_view
        for observable_id in task.observable_ids
    }
    selected_episode_units = {
        (unit.evidence_id, unit.observable_id)
        for unit in manifest.payload.representative_episode_units
    }
    assert episode_units == selected_episode_units

    series_units = {
        (task.series_id, observable_id)
        for task in series_view
        for observable_id in task.observable_ids
    }
    selected_series_units = {
        (unit.evidence_id, unit.observable_id)
        for unit in manifest.payload.representative_series_units
    }
    assert series_units == selected_series_units


def test_manifest_detects_changed_task_set() -> None:
    episode_tasks = _episode_tasks()
    manifest = build_development_calibration_sample(
        episode_tasks=episode_tasks,
        episode_sample_size=3,
        episode_per_observable_floor=1,
        seed_sha256=SEED,
        created_at_utc=NOW,
    )
    changed = episode_tasks[:-1]
    errors = development_calibration_integrity_errors(
        manifest,
        episode_tasks=changed,
    )
    assert "development calibration manifest does not bind episode task set" in errors
