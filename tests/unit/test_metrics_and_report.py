from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.evaluation.ablation import (
    CurveObservation,
    LeaveOneClusterOutObservation,
    aggregate_leave_one_cluster_out,
    aggregate_restoration_curves,
)
from hdmatch.evaluation.failures import FailureClassification, classify_oracle_failure
from hdmatch.evaluation.metrics import (
    aggregate_rank_metrics,
    evaluate_ranked_case,
    tie_aware_rank,
)
from hdmatch.evaluation.report import EvaluationInputError, evaluate_frozen_run
from hdmatch.evaluation.robustness import (
    RobustnessObservation,
    aggregate_robustness,
    paired_changes_from_baseline,
)
from hdmatch.experiments.canonical import (
    sha256_bytes,
    write_new_canonical_json,
)
from hdmatch.experiments.freeze import ArtifactBindings, freeze_predictions
from hdmatch.experiments.manifest import create_run_manifest, write_run_manifest
from hdmatch.experiments.reveal import RevealResult, reveal_answer_key
from hdmatch.synthetic.sealing import SealingMetadata, generate_key_file, seal_answer_key


def _digest(label: str) -> str:
    return sha256_bytes(label.encode())


def _bindings() -> ArtifactBindings:
    return ArtifactBindings(
        blind_input_sha256=_digest("blind"),
        model_sha256=_digest("model"),
        question_bank_sha256=_digest("questions"),
        mapping_sha256=_digest("mapping"),
    )


def test_tie_aware_rank_reports_interval_fractional_top_k_and_percentile() -> None:
    rank = tie_aware_rank([10.0, 10.0, 4.0], true_index=1)
    assert (rank.best_rank, rank.worst_rank, rank.midrank, rank.tie_size) == (1, 2, 1.5, 2)
    assert rank.top_k_credit(1) == 0.5
    assert rank.top_k_credit(3) == 1.0

    metrics = evaluate_ranked_case(
        case_id="C1",
        candidates=[
            {"local_date": "2000-01-01", "date_score": 10.0},
            {"local_date": "2000-01-02", "date_score": 10.0},
            {"local_date": "2000-01-03", "date_score": 4.0},
        ],
        true_candidate_id="2000-01-02",
    )
    assert metrics.reciprocal_rank == pytest.approx(2 / 3)
    assert metrics.percentile == pytest.approx(0.75)
    assert metrics.top_1_credit == 0.5
    assert metrics.tied is True


def test_rank_metrics_reject_duplicate_and_missing_candidates() -> None:
    with pytest.raises(ValueError, match="duplicate"):
        evaluate_ranked_case(
            case_id="C",
            candidates=[
                {"local_date": "2000-01-01", "date_score": 1},
                {"local_date": "2000-01-01", "date_score": 2},
            ],
            true_candidate_id="2000-01-01",
        )
    with pytest.raises(ValueError, match="absent"):
        evaluate_ranked_case(
            case_id="C",
            candidates=[{"local_date": "2000-01-01", "date_score": 1}],
            true_candidate_id="2000-01-02",
        )


def test_aggregate_penalizes_unevaluable_cases_in_top_k_and_mrr() -> None:
    case = evaluate_ranked_case(
        case_id="C1",
        candidates=[{"local_date": "2000-01-01", "date_score": 1}],
        true_candidate_id="2000-01-01",
    )
    result = aggregate_rank_metrics([case], total_case_count=2)
    assert result.case_count == 2
    assert result.evaluated_case_count == 1
    assert result.unevaluable_case_count == 1
    assert result.top_1 == 0.5
    assert result.mean_reciprocal_rank == 0.5


@pytest.mark.parametrize(
    ("kwargs", "classification"),
    [
        ({"true_candidate_present": False}, FailureClassification.SEARCH_BUG),
        (
            {"true_candidate_present": True, "unresolved_mapping_ids": ("M1",)},
            FailureClassification.MISSING_MAPPING,
        ),
        (
            {"true_candidate_present": True, "structurally_identical_top_candidate": True},
            FailureClassification.STRUCTURALLY_INDISTINGUISHABLE,
        ),
        (
            {"true_candidate_present": True, "state_winner_but_date_loser": True},
            FailureClassification.AGGREGATION_AMBIGUITY,
        ),
        ({"true_candidate_present": True}, FailureClassification.SCORING_BUG),
    ],
)
def test_all_protocol_failure_classifications_are_reachable(
    kwargs: dict[str, object], classification: FailureClassification
) -> None:
    record = classify_oracle_failure(case_id="C", **kwargs)  # type: ignore[arg-type]
    assert record.classification is classification


def test_restoration_and_leave_one_out_aggregation() -> None:
    curves = aggregate_restoration_curves(
        [
            CurveObservation(
                case_id="C1", method="active", cluster_count=1, midrank=1, candidate_count=31
            ),
            CurveObservation(
                case_id="C2", method="active", cluster_count=1, midrank=3, candidate_count=31
            ),
        ]
    )
    assert len(curves) == 1
    assert curves[0].mean_midrank == 2
    assert curves[0].mean_reciprocal_rank == pytest.approx(2 / 3)
    ablation = aggregate_leave_one_cluster_out(
        [
            LeaveOneClusterOutObservation(
                case_id="C1", cluster_id="A", full_midrank=1, ablated_midrank=4
            ),
            LeaveOneClusterOutObservation(
                case_id="C2", cluster_id="A", full_midrank=2, ablated_midrank=1
            ),
        ]
    )
    assert ablation[0].mean_rank_change == 1
    assert ablation[0].worsened_fraction == 0.5


def test_robustness_aggregation_keeps_declared_levels_and_paired_changes() -> None:
    baseline = evaluate_ranked_case(
        case_id="C1",
        candidates=[
            {"local_date": "A", "date_score": 2},
            {"local_date": "B", "date_score": 1},
        ],
        true_candidate_id="A",
    )
    noisy = evaluate_ranked_case(
        case_id="C1",
        candidates=[
            {"local_date": "A", "date_score": 1},
            {"local_date": "B", "date_score": 2},
        ],
        true_candidate_id="A",
    )
    observations = [
        RobustnessObservation(
            perturbation="answer_flip_rate", level="baseline", metrics=baseline
        ),
        RobustnessObservation(
            perturbation="answer_flip_rate", level="0.10", metrics=noisy
        ),
    ]
    points = aggregate_robustness(observations)
    assert [point.level for point in points] == ["0.10", "baseline"]
    change = paired_changes_from_baseline(observations)[0]
    assert change.mean_midrank_change == 1
    assert change.worsened_fraction == 1


def _predictions() -> dict[str, object]:
    return {
        "schema_version": "predictions-v1",
        "experiment_id": "EXP-1",
        **_bindings().model_dump(),
        "predictions": [
            {
                "case_id": "C1",
                "ranked_dates": [
                    {"local_date": "2000-01-01", "date_rank": 1, "date_score": 8.0},
                    {"local_date": "2000-01-02", "date_rank": 2, "date_score": 5.0},
                ],
                "aggregation_variants": {
                    "best_state": {
                        "ranked_dates": [
                            {"local_date": "2000-01-01", "date_score": 8.0},
                            {"local_date": "2000-01-02", "date_score": 5.0},
                        ]
                    }
                },
                "zero_cluster": {
                    "ranked_dates": [
                        {"local_date": "2000-01-01", "date_score": 0.0},
                        {"local_date": "2000-01-02", "date_score": 0.0},
                    ]
                },
                "random_restoration": [
                    {
                        "cluster_count": 1,
                        "ranked_dates": [
                            {"local_date": "2000-01-01", "date_score": 8.0},
                            {"local_date": "2000-01-02", "date_score": 5.0},
                        ],
                    }
                ],
                "active_restoration": [
                    {
                        "cluster_count": 1,
                        "ranked_dates": [
                            {"local_date": "2000-01-01", "date_score": 8.0},
                            {"local_date": "2000-01-02", "date_score": 5.0},
                        ],
                    }
                ],
                "leave_one_cluster_out": [
                    {
                        "cluster_id": "A",
                        "ranked_dates": [
                            {"local_date": "2000-01-01", "date_score": 5.0},
                            {"local_date": "2000-01-02", "date_score": 8.0},
                        ],
                    }
                ],
                "unresolved_mapping_ids": [],
            },
            {
                "case_id": "C2",
                "ranked_dates": [
                    {"local_date": "2000-01-01", "date_rank": 1, "date_score": 8.0}
                ],
                "zero_cluster": {
                    "ranked_dates": [
                        {"local_date": "2000-01-01", "date_score": 0.0}
                    ]
                },
                "random_restoration": [],
                "active_restoration": [],
                "leave_one_cluster_out": [],
                "unresolved_mapping_ids": [],
            },
        ],
    }


def _answer_key() -> dict[str, object]:
    return {
        "schema_version": "answer-key-v1",
        "experiment_id": "EXP-1",
        "blind_input_sha256": _digest("blind"),
        "cases": [
            {"case_id": "C1", "true_local_date": "2000-01-01", "true_state_id": "S1"},
            {"case_id": "C2", "true_local_date": "2000-01-02", "true_state_id": "S2"},
        ],
    }


def _frozen_run(tmp_path: Path, predictions: dict[str, object]) -> tuple[Path, RevealResult]:
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True)
    write_new_canonical_json(run_dir / "predictions.json", predictions)
    manifest_path = run_dir / "run.manifest.json"
    manifest = create_run_manifest(
        experiment_id="EXP-1",
        seed=42,
        repository_root=Path(__file__).parents[2],
        candidate_universe="known_month",
        aggregation_rule="duration_weighted_evidence",
        model_id="MODEL-A-CORE-V1",
        input_hashes={"blind_cases.json": _bindings().blind_input_sha256},
        config={
            "aggregation": "duration_weighted_evidence",
            "threshold_rubric_bits": 0.0,
            "workers": 1,
            "cache_policy": "hash-bound exact month universes",
        },
        created_at_utc=datetime(2026, 8, 20, 23, 59, tzinfo=UTC),
    )
    write_run_manifest(manifest, manifest_path)
    freeze = freeze_predictions(
        run_dir,
        experiment_id="EXP-1",
        bindings=_bindings(),
        repository_root=Path(__file__).parents[2],
        run_manifest_path=manifest_path,
        created_at_utc=datetime(2026, 8, 21, tzinfo=UTC),
    )
    key_path = tmp_path / "evaluation.key"
    envelope_path = run_dir / "answer_key.json.enc"
    generate_key_file(key_path, decoder_root=run_dir)
    seal_answer_key(
        _answer_key(),
        encrypted_path=envelope_path,
        key_path=key_path,
        metadata=SealingMetadata(
            experiment_id=freeze.experiment_id,
            blind_input_sha256=freeze.blind_input_sha256,
            model_sha256=freeze.model_sha256,
            question_bank_sha256=freeze.question_bank_sha256,
            mapping_sha256=freeze.mapping_sha256,
        ),
        decoder_root=run_dir,
    )
    revealed = reveal_answer_key(
        run_dir,
        encrypted_answer_key_path=envelope_path,
        key_path=key_path,
        decoder_root=run_dir,
        revealed_at_utc=datetime(2026, 8, 21, 0, 1, tzinfo=UTC),
    )
    return run_dir, revealed


def test_frozen_run_evaluator_preserves_search_failure_and_transparent_metadata(
    tmp_path: Path,
) -> None:
    run_dir, revealed = _frozen_run(tmp_path, _predictions())
    report = evaluate_frozen_run(
        run_dir,
        revealed=revealed,
        created_at_utc=datetime(2026, 8, 21, 0, 2, tzinfo=UTC),
    )
    assert report.aggregate.case_count == 2
    assert report.aggregate.evaluated_case_count == 1
    assert report.aggregate.top_1 == 0.5
    assert report.failure_counts["search_bug"] == 1
    assert set(report.failure_counts) == {item.value for item in FailureClassification}
    assert report.claim_boundary == "synthetic-engineering-validation-only"
    assert report.score_semantics == "rubric-bits-not-probabilities"
    assert report.evaluation_target == "local_date"
    assert report.revealed_target_set_sha256 is None
    assert report.restoration_curves
    zero_active = next(
        point
        for point in report.restoration_curves
        if point.method == "active" and point.cluster_count == 0
    )
    assert zero_active.case_count == 2
    assert zero_active.evaluated_case_count == 1
    assert zero_active.unevaluable_case_count == 1
    assert zero_active.mean_midrank == 1.5
    assert zero_active.top_1 == 0.25
    assert report.leave_one_cluster_out[0].cluster_id == "A"
    stored = json.loads((run_dir / "evaluation.json").read_bytes())
    assert stored["prediction_sha256"] == report.prediction_sha256


def test_evaluator_classifies_date_loss_reversed_by_best_state_aggregation(
    tmp_path: Path,
) -> None:
    predictions = _predictions()
    assert isinstance(predictions["predictions"], list)
    first = predictions["predictions"][0]
    assert isinstance(first, dict)
    first["ranked_dates"] = [
        {"local_date": "2000-01-02", "date_score": 9.0},
        {"local_date": "2000-01-01", "date_score": 8.0},
    ]
    run_dir, revealed = _frozen_run(tmp_path, predictions)
    report = evaluate_frozen_run(
        run_dir,
        revealed=revealed,
        created_at_utc=datetime(2026, 8, 21, 0, 2, tzinfo=UTC),
    )
    assert report.failure_counts["aggregation_ambiguity"] == 1
    assert report.failure_counts["scoring_bug"] == 0


def test_evaluator_refuses_duplicate_cases_and_binding_mismatch(tmp_path: Path) -> None:
    predictions = _predictions()
    assert isinstance(predictions["predictions"], list)
    predictions["predictions"].append(predictions["predictions"][0])
    run_dir, revealed = _frozen_run(tmp_path, predictions)
    with pytest.raises(EvaluationInputError, match="duplicate"):
        evaluate_frozen_run(run_dir, revealed=revealed)

    other_path = tmp_path / "other"
    mismatched = _predictions()
    mismatched["model_sha256"] = _digest("other-model")
    run_dir, revealed = _frozen_run(other_path, mismatched)
    with pytest.raises(EvaluationInputError, match="model_sha256"):
        evaluate_frozen_run(run_dir, revealed=revealed)


def test_claim_grade_evaluator_accepts_no_independent_plaintext_key(tmp_path: Path) -> None:
    run_dir, _ = _frozen_run(tmp_path, _predictions())

    with pytest.raises(TypeError, match="unexpected keyword argument 'answer_key'"):
        evaluate_frozen_run(run_dir, answer_key=_answer_key())  # type: ignore[call-arg]


def test_evaluator_refuses_mutated_in_memory_reveal_key(tmp_path: Path) -> None:
    run_dir, revealed = _frozen_run(tmp_path, _predictions())
    changed_key = _answer_key()
    assert isinstance(changed_key["cases"], list)
    changed_key["cases"][0]["true_local_date"] = "2000-01-03"
    assert isinstance(revealed.answer_key, dict)
    revealed.answer_key.clear()
    revealed.answer_key.update(changed_key)

    with pytest.raises(EvaluationInputError, match="does not match the reveal binding"):
        evaluate_frozen_run(run_dir, revealed=revealed)


def test_evaluator_refuses_envelope_tampered_after_reveal(tmp_path: Path) -> None:
    run_dir, revealed = _frozen_run(tmp_path, _predictions())
    envelope_path = run_dir / "answer_key.json.enc"
    envelope_path.write_bytes(envelope_path.read_bytes() + b"\n")

    with pytest.raises(Exception, match="envelope bytes changed"):
        evaluate_frozen_run(run_dir, revealed=revealed)


def test_evaluator_refuses_run_manifest_tampered_after_freeze(tmp_path: Path) -> None:
    run_dir, revealed = _frozen_run(tmp_path, _predictions())
    manifest_path = run_dir / "run.manifest.json"
    manifest_path.write_bytes(manifest_path.read_bytes() + b"\n")

    with pytest.raises(Exception, match="run-manifest bytes changed"):
        evaluate_frozen_run(run_dir, revealed=revealed)


def test_evaluator_refuses_reveal_receipt_direct_binding_mismatch(tmp_path: Path) -> None:
    run_dir, revealed = _frozen_run(tmp_path, _predictions())
    reveal_path = run_dir / "answer-key.reveal.json"
    raw = json.loads(reveal_path.read_bytes())
    raw["mapping_sha256"] = _digest("different-mapping")
    reveal_path.unlink()
    write_new_canonical_json(reveal_path, raw)

    with pytest.raises(Exception, match="reveal mapping_sha256"):
        evaluate_frozen_run(run_dir, revealed=revealed)


def test_evaluator_rejects_legacy_incomplete_reveal(tmp_path: Path) -> None:
    run_dir, revealed = _frozen_run(tmp_path, _predictions())
    reveal_path = run_dir / "answer-key.reveal.json"
    raw = json.loads(reveal_path.read_bytes())
    del raw["encrypted_answer_key_file"]
    del raw["answer_key_payload_sha256"]
    reveal_path.unlink()
    write_new_canonical_json(reveal_path, raw)

    with pytest.raises(Exception, match="invalid or missing answer-key reveal record"):
        evaluate_frozen_run(run_dir, revealed=revealed)


def test_evaluator_refuses_before_reveal_record_exists(tmp_path: Path) -> None:
    run_dir, revealed = _frozen_run(tmp_path, _predictions())
    (run_dir / "answer-key.reveal.json").unlink()
    with pytest.raises(Exception, match="reveal"):
        evaluate_frozen_run(run_dir, revealed=revealed)


def test_evaluator_refuses_timestamp_before_reveal(tmp_path: Path) -> None:
    run_dir, revealed = _frozen_run(tmp_path, _predictions())

    with pytest.raises(EvaluationInputError, match="cannot predate answer-key reveal"):
        evaluate_frozen_run(
            run_dir,
            revealed=revealed,
            created_at_utc=datetime(2026, 8, 21, tzinfo=UTC),
        )
