from __future__ import annotations

from copy import deepcopy
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest

from hdmatch.evaluation.report import EvaluationInputError
from hdmatch.evaluation.report import _evaluate_frozen_payloads as evaluate_frozen_payloads
from hdmatch.experiments.canonical import write_new_canonical_json
from hdmatch.experiments.freeze import FreezeRecord
from hdmatch.model.mapping_library import PredicateOperator
from hdmatch.runtime import recovery
from hdmatch.runtime.recovery import (
    BroadOnDemandRecoveryError,
    RecoverySettings,
    recover_blind_file,
)
from hdmatch.runtime.symbolic_adapter import FrozenSymbolicModel
from hdmatch.schemas import Activation, BlindCase, CandidateState, ChartFeatures
from hdmatch.search import AggregationMode
from hdmatch.search.candidate_universe import split_interval_by_local_date
from hdmatch.synthetic.noise import NoiseTier, noise_parameters_payload
from hdmatch.util import sha256_json

ROOT = Path(__file__).resolve().parents[2]
_HASH = "a" * 64


def _reveal_provenance(answer_key: dict[str, object]) -> dict[str, str]:
    return {
        "encrypted_answer_key_file": "answer_key.json.enc",
        "encrypted_answer_key_sha256": "f" * 64,
        "answer_key_payload_sha256": sha256_json(answer_key),
        "run_manifest_sha256": "c" * 64,
    }


def _chart(chart_type: str, moment: datetime) -> ChartFeatures:
    activation = Activation(
        body="sun", side="personality", longitude=0.0, gate=41, line=1
    )
    return ChartFeatures(
        personality_utc=moment,
        design_utc=moment - timedelta(days=88),
        type=chart_type,
        strategy="wait_to_respond" if chart_type == "generator" else "wait_for_invitation",
        authority="sacral" if chart_type == "generator" else "splenic",
        profile="1/3",
        definition="single_definition",
        defined_centers=("sacral",) if chart_type == "generator" else ("spleen",),
        activations={"personality:sun": activation},
    )


def _state(
    state_id: str,
    start: datetime,
    end: datetime,
    chart_type: str,
) -> CandidateState:
    chart = _chart(chart_type, start)
    return CandidateState(
        state_id=state_id,
        start_utc=start,
        end_utc=end,
        chart_features_hash=sha256_json(chart),
        chart_features=chart,
        local_date_overlaps=split_interval_by_local_date(start, end, "UTC"),
    )


def _cached_states() -> tuple[CandidateState, ...]:
    return (
        _state(
            "OUTSIDE-BEFORE",
            datetime(2000, 1, 1, tzinfo=UTC),
            datetime(2000, 1, 1, 20, tzinfo=UTC),
            "projector",
        ),
        _state(
            "CROSS-IN",
            datetime(2000, 1, 1, 20, tzinfo=UTC),
            datetime(2000, 1, 2, 8, tzinfo=UTC),
            "generator",
        ),
        _state(
            "CROSS-OUT",
            datetime(2000, 1, 2, 8, tzinfo=UTC),
            datetime(2000, 1, 3, 4, tzinfo=UTC),
            "projector",
        ),
        _state(
            "OUTSIDE-AFTER",
            datetime(2000, 1, 3, 4, tzinfo=UTC),
            datetime(2000, 1, 4, tzinfo=UTC),
            "generator",
        ),
    )


def _blind_payload(
    model: FrozenSymbolicModel,
    *,
    known_day: int = 2,
) -> dict[str, object]:
    target_chart = _chart("projector", datetime(2000, 1, known_day, 8, tzinfo=UTC))
    return {
        "schema_version": "blind-synthetic-v1",
        "experiment_id": "KNOWN-DATE-1",
        "generator": "frozen-chart-to-response-model",
        "model_id": model.model_id,
        "model_sha256": model.model_sha256,
        "question_bank_sha256": model.question_bank_sha256,
        "mapping_sha256": model.mapping_sha256,
        "model_capabilities": dict(model.capability_metadata),
        "noise_tier": "oracle",
        "noise_parameters": noise_parameters_payload(NoiseTier.ORACLE),
        "candidate_universe": "known_date",
        "cases": [
            {
                "case_id": "DATE-CASE",
                "known_birth_year": 2000,
                "known_birth_month": 1,
                "known_birth_day": known_day,
                "birthplace": "Synthetic UTC",
                "iana_timezone": "UTC",
                "responses": [
                    response.model_dump(mode="json")
                    for response in model.oracle_responses(target_chart)
                ],
                "candidate_universe": "known_date",
            }
        ],
    }


def _blind_payload_for_months(
    model: FrozenSymbolicModel,
    months: tuple[tuple[int, int], ...],
) -> dict[str, object]:
    payload = _blind_payload(model)
    template = payload["cases"]
    assert isinstance(template, list)
    base = template[0]
    assert isinstance(base, dict)
    payload["candidate_universe"] = "known_month"
    payload["cases"] = [
        {
            **deepcopy(base),
            "case_id": f"SCOPE-{index:04d}",
            "known_birth_year": year,
            "known_birth_month": month,
            "candidate_universe": "known_month",
        }
        for index, (year, month) in enumerate(months, start=1)
    ]
    for case in payload["cases"]:
        assert isinstance(case, dict)
        case.pop("known_birth_day", None)
    return payload


@pytest.mark.parametrize(
    ("months", "message"),
    [
        (((2000, 1), (2025, 1)), "calendar-year span=25"),
        (
            tuple((2000 + index // 12, index % 12 + 1) for index in range(121)),
            "distinct month universes=121",
        ),
    ],
)
def test_broad_recovery_fails_before_adapter_cache_writes_or_scoring(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    months: tuple[tuple[int, int], ...],
    message: str,
) -> None:
    model = FrozenSymbolicModel(ROOT / "mappings" / "mapping_library_v1.json")
    blind_path = tmp_path / "blind.json"
    cache_dir = tmp_path / "candidate-cache"
    write_new_canonical_json(blind_path, _blind_payload_for_months(model, months))

    def forbidden(*_args: object, **_kwargs: object) -> None:
        pytest.fail("broad-scope rejection occurred after recovery work began")

    monkeypatch.setattr(recovery, "ExactChartAdapter", forbidden)
    monkeypatch.setattr(recovery, "ensure_month_caches", forbidden)
    monkeypatch.setattr(recovery, "_score_states", forbidden)

    with pytest.raises(BroadOnDemandRecoveryError, match=message):
        recover_blind_file(
            blind_path,
            decoder_root=tmp_path,
            model=model,
            ephemeris_path=tmp_path / "ephemeris",
            cache_dir=cache_dir,
            settings=RecoverySettings(
                aggregation=AggregationMode.DURATION_WEIGHTED_MEAN,
                threshold_rubric_bits=0.0,
            ),
        )

    assert not cache_dir.exists()


def test_on_demand_recovery_scope_preserves_requests_below_both_limits() -> None:
    model = FrozenSymbolicModel(ROOT / "mappings" / "mapping_library_v1.json")
    months = tuple((2000 + index // 12, index % 12 + 1) for index in range(120))
    payload = _blind_payload_for_months(model, months)
    raw_cases = payload["cases"]
    assert isinstance(raw_cases, list)
    cases = tuple(BlindCase.model_validate(item) for item in raw_cases)

    requests = recovery._guard_on_demand_recovery_scope(cases)

    assert len(set(requests)) == 120


def _recover_known_date(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    known_day: int = 2,
) -> tuple[dict[str, object], FrozenSymbolicModel, tuple[CandidateState, ...]]:
    model = FrozenSymbolicModel(ROOT / "mappings" / "mapping_library_v1.json")
    states = _cached_states()
    blind_path = tmp_path / "blind.json"
    write_new_canonical_json(blind_path, _blind_payload(model, known_day=known_day))

    class _Engine:
        fingerprint = "engine-fingerprint"

        def __init__(self, _path: str | Path) -> None:
            pass

    monkeypatch.setattr(recovery, "ExactChartAdapter", _Engine)
    monkeypatch.setattr(recovery, "ensure_month_caches", lambda *args, **kwargs: ())
    monkeypatch.setattr(
        recovery,
        "cache_path",
        lambda *args, **kwargs: tmp_path / "exact-month-cache.json",
    )
    monkeypatch.setattr(
        recovery,
        "load_cached_universe",
        lambda *args, **kwargs: SimpleNamespace(states=states, sha256="c" * 64),
    )
    predictions = recover_blind_file(
        blind_path,
        decoder_root=tmp_path,
        model=model,
        ephemeris_path=tmp_path,
        cache_dir=tmp_path / "cache",
        settings=RecoverySettings(
            aggregation=AggregationMode.DURATION_WEIGHTED_MEAN,
            threshold_rubric_bits=0.0,
        ),
    )
    return predictions, model, states


def _freeze(predictions: dict[str, object], *, experiment_id: str) -> FreezeRecord:
    return FreezeRecord(
        experiment_id=experiment_id,
        prediction_file="predictions.json",
        prediction_sha256="d" * 64,
        prediction_size_bytes=1,
        blind_input_sha256=str(predictions["blind_input_sha256"]),
        model_sha256=str(predictions["model_sha256"]),
        question_bank_sha256=str(predictions["question_bank_sha256"]),
        mapping_sha256=str(predictions["mapping_sha256"]),
        software_commit="test",
        software_dirty=False,
        software_versions={"python": "test"},
        created_at_utc=datetime(2026, 8, 21, tzinfo=UTC),
    )


def _answer_key(
    predictions: dict[str, object],
    *,
    experiment_id: str = "KNOWN-DATE-1",
    true_utc: str = "2000-01-02T08:00:00Z",
    true_local_date: str = "2000-01-02",
) -> dict[str, object]:
    return {
        "schema_version": "answer-key-v1",
        "experiment_id": experiment_id,
        "blind_input_sha256": predictions["blind_input_sha256"],
        "cases": [
            {
                "case_id": "DATE-CASE",
                "true_utc": true_utc,
                "true_local_date": true_local_date,
                "true_chart_features_hash": "b" * 64,
                "true_state_id": "SYNTHETIC-KEY-ID",
            }
        ],
    }


def test_blind_known_date_recovery_filters_exact_cache_and_uses_interval_curves(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    predictions, model, states = _recover_known_date(tmp_path, monkeypatch)
    cases = predictions["predictions"]
    assert isinstance(cases, list)
    case = cases[0]
    assert isinstance(case, dict)

    assert case["candidate_universe"] == "known_date"
    assert case["interval_semantics"] == "half-open-[start,end)"
    assert case["point_estimate_utc"] is None
    ranked = case["ranked_intervals"]
    assert isinstance(ranked, list)
    assert {record["state_id"] for record in ranked} == {"CROSS-IN", "CROSS-OUT"}
    by_id = {record["state_id"]: record for record in ranked}
    assert by_id["CROSS-IN"]["source_interval_width_seconds"] == 12 * 3600
    assert by_id["CROSS-IN"]["eligible_width_seconds"] == 8 * 3600
    assert by_id["CROSS-OUT"]["source_interval_width_seconds"] == 20 * 3600
    assert by_id["CROSS-OUT"]["eligible_width_seconds"] == 16 * 3600
    assert case["prevalence_source"].startswith("eligible-duration-weighted")
    assert case["adaptive_prior_source"].startswith("eligible-duration-weighted")
    assert all("ranked_intervals" in point for point in case["random_restoration"])
    assert all("ranked_intervals" in point for point in case["active_restoration"])
    assert all("ranked_intervals" in point for point in case["leave_one_cluster_out"])

    date_states = recovery._known_date_states(states, date(2000, 1, 2))
    prevalence = recovery._known_date_prevalence(date_states, model, date(2000, 1, 2), "UTC")
    generator_anchors = {
        mapping.anchor_id
        for mapping in model.library.frozen_mappings
        if mapping.chart_feature_predicate is not None
        and mapping.chart_feature_predicate.feature == "type"
        and mapping.chart_feature_predicate.operator is PredicateOperator.EQUALS_ANY
        and mapping.chart_feature_predicate.matches(_chart("generator", states[1].start_utc))
    }
    assert generator_anchors
    assert all(prevalence[anchor] == pytest.approx(1 / 3) for anchor in generator_anchors)


def test_post_reveal_interval_evaluation_uses_boundary_containment_and_target_hash(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    predictions, _, _ = _recover_known_date(tmp_path, monkeypatch)
    freeze = _freeze(predictions, experiment_id="KNOWN-DATE-1")
    answer_key = _answer_key(predictions)
    report = evaluate_frozen_payloads(
        predictions=predictions,
        answer_key=answer_key,
        freeze=freeze,
        freeze_sha256=_HASH,
        reveal_sha256="e" * 64,
        **_reveal_provenance(answer_key),
        created_at_utc=datetime(2026, 8, 21, tzinfo=UTC),
    )

    assert report.evaluation_target == "stable_interval"
    assert report.revealed_target_set_sha256 is not None
    assert report.aggregate.case_count == 1
    assert report.cases[0].candidate_count == 2
    interval = report.rectification_cases[0]
    assert interval.matched_state_id == "CROSS-OUT"
    assert interval.true_utc == datetime(2000, 1, 2, 8, tzinfo=UTC)
    assert interval.start_utc == datetime(2000, 1, 2, 8, tzinfo=UTC)
    assert interval.end_utc == datetime(2000, 1, 3, 4, tzinfo=UTC)
    assert interval.eligible_end_utc == datetime(2000, 1, 3, tzinfo=UTC)
    assert interval.point_estimate_utc is None
    assert interval.universe_boundary_truncated is False
    assert interval.interval_resolution_status == "stable_interval"
    assert interval.resolution_semantics == "source-half-open-interval-not-point"
    assert report.restoration_curves
    assert report.leave_one_cluster_out

    shifted = _answer_key(predictions, true_utc="2000-01-02T09:00:00Z")
    shifted_report = evaluate_frozen_payloads(
        predictions=predictions,
        answer_key=shifted,
        freeze=freeze,
        freeze_sha256=_HASH,
        reveal_sha256="e" * 64,
        **_reveal_provenance(shifted),
    )
    assert shifted_report.revealed_target_set_sha256 != report.revealed_target_set_sha256

    renamed_predictions = deepcopy(predictions)
    renamed_predictions["experiment_id"] = "RENAMED-EXPERIMENT"
    renamed_key = _answer_key(predictions, experiment_id="RENAMED-EXPERIMENT")
    renamed_freeze = _freeze(renamed_predictions, experiment_id="RENAMED-EXPERIMENT")
    renamed_report = evaluate_frozen_payloads(
        predictions=renamed_predictions,
        answer_key=renamed_key,
        freeze=renamed_freeze,
        freeze_sha256=_HASH,
        reveal_sha256="e" * 64,
        **_reveal_provenance(renamed_key),
    )
    assert renamed_report.revealed_target_set_sha256 == report.revealed_target_set_sha256


def test_month_boundary_candidate_is_reported_as_unresolved_clipped(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    predictions, _, _ = _recover_known_date(tmp_path, monkeypatch, known_day=1)
    cases = predictions["predictions"]
    assert isinstance(cases, list)
    case = cases[0]
    assert isinstance(case, dict)
    records = case["ranked_intervals"]
    assert isinstance(records, list)
    by_id = {record["state_id"]: record for record in records}
    assert by_id["OUTSIDE-BEFORE"]["universe_boundary_truncated"] is True
    assert by_id["OUTSIDE-BEFORE"]["source_interval_width_seconds"] == 20 * 3600
    assert by_id["CROSS-IN"]["universe_boundary_truncated"] is False

    answer_key = _answer_key(
        predictions,
        true_utc="2000-01-01T00:00:00Z",
        true_local_date="2000-01-01",
    )
    report = evaluate_frozen_payloads(
        predictions=predictions,
        answer_key=answer_key,
        freeze=_freeze(predictions, experiment_id="KNOWN-DATE-1"),
        freeze_sha256=_HASH,
        reveal_sha256="e" * 64,
        **_reveal_provenance(answer_key),
    )
    interval = report.rectification_cases[0]
    assert interval.matched_state_id == "OUTSIDE-BEFORE"
    assert interval.universe_boundary_truncated is True
    assert interval.interval_resolution_status == "unresolved_universe_boundary_clipped"
    assert interval.source_interval_width_seconds == 20 * 3600
    assert interval.point_estimate_utc is None


def test_evaluator_rejects_mixed_candidate_universes_before_metrics(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    predictions, _, _ = _recover_known_date(tmp_path, monkeypatch)
    cases = predictions["predictions"]
    assert isinstance(cases, list)
    cases.append({"case_id": "MONTH-CASE", "candidate_universe": "known_month"})
    answer_key = _answer_key(predictions)
    keyed_cases = answer_key["cases"]
    assert isinstance(keyed_cases, list)
    keyed_cases.append({"case_id": "MONTH-CASE", "true_local_date": "2000-01-03"})

    with pytest.raises(EvaluationInputError, match="mixed candidate-universe"):
        evaluate_frozen_payloads(
            predictions=predictions,
            answer_key=answer_key,
            freeze=_freeze(predictions, experiment_id="KNOWN-DATE-1"),
            freeze_sha256=_HASH,
            reveal_sha256="e" * 64,
            **_reveal_provenance(answer_key),
        )
