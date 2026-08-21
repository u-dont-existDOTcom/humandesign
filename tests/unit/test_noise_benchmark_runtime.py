from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.cli import main
from hdmatch.evaluation.failures import FailureClassification, FailureRecord
from hdmatch.evaluation.metrics import aggregate_rank_metrics, evaluate_ranked_case
from hdmatch.evaluation.noise_benchmark import NoiseBenchmarkInputError, NoiseTier
from hdmatch.evaluation.report import EvaluationReport
from hdmatch.experiments.canonical import (
    load_json_bytes,
    sha256_file,
    write_new_canonical_json,
)
from hdmatch.experiments.manifest import RunManifest, SoftwareEnvironment
from hdmatch.runtime.noise_benchmark import (
    build_noise_benchmark_from_run_dirs,
    load_revealed_noise_tier_run,
)
from hdmatch.synthetic.noise import NoiseTier as GeneratorNoiseTier
from hdmatch.synthetic.noise import noise_parameters_payload

_HASH_A = "a" * 64
_HASH_B = "b" * 64
_HASH_C = "c" * 64
_HASH_D = "d" * 64
_HASH_E = "e" * 64
_HASH_F = "f" * 64


def _evaluation(
    tier: NoiseTier,
    *,
    blind_sha256: str,
    true_rank: int,
    revealed_target_set_sha256: str | None = _HASH_C,
) -> EvaluationReport:
    ranked_ids = [
        *(f"D{index}" for index in range(2, true_rank + 1)),
        "D1",
        *(f"D{index}" for index in range(true_rank + 1, 7)),
    ]
    candidates = [
        {"local_date": candidate_id, "date_score": float(6 - index)}
        for index, candidate_id in enumerate(ranked_ids)
    ]
    case = evaluate_ranked_case(
        case_id="C1",
        candidates=candidates,
        true_candidate_id="D1",
    )
    failure = FailureRecord(
        case_id="C2",
        classification=FailureClassification.SEARCH_BUG,
        explanation="The true candidate was absent.",
        evidence={},
    )
    return EvaluationReport(
        experiment_id=f"EXP-{tier.value}",
        created_at_utc=datetime(2026, 8, 21, 1, tzinfo=UTC),
        prediction_sha256=_HASH_A,
        freeze_sha256=_HASH_B,
        reveal_sha256=_HASH_C,
        blind_input_sha256=blind_sha256,
        model_sha256=_HASH_D,
        question_bank_sha256=_HASH_E,
        mapping_sha256=_HASH_F,
        revealed_target_set_sha256=revealed_target_set_sha256,
        aggregate=aggregate_rank_metrics([case], total_case_count=2),
        cases=(case,),
        failures=(failure,),
        failure_counts={"search_bug": 1},
        restoration_curves=(),
        leave_one_cluster_out=(),
    )


def _write_run(
    root: Path,
    tier: NoiseTier,
    *,
    true_rank: int,
    noise_payload: object | None = None,
    software_dirty: bool = False,
    revealed_target_set_sha256: str | None = _HASH_C,
    tzdata_version: str = "2026.1",
) -> Path:
    run_dir = root / tier.value
    run_dir.mkdir()
    blind = {
        "schema_version": "blind-synthetic-v1",
        "experiment_id": f"EXP-{tier.value}",
        "model_id": "MODEL-A-CORE-V1",
        "model_sha256": _HASH_D,
        "question_bank_sha256": _HASH_E,
        "mapping_sha256": _HASH_F,
        "noise_tier": tier.value,
        "noise_parameters": (
            noise_payload
            if noise_payload is not None
            else noise_parameters_payload(GeneratorNoiseTier(tier.value))
        ),
        "candidate_universe": "known_month",
        "cases": [
            {
                "case_id": case_id,
                "candidate_universe": "known_month",
                "known_birth_year": 2000,
                "known_birth_month": 1,
                "iana_timezone": "UTC",
                "responses": [],
            }
            for case_id in ("C1", "C2")
        ],
    }
    blind_path = run_dir / "blind_cases.json"
    write_new_canonical_json(blind_path, blind)
    blind_sha256 = sha256_file(blind_path)
    manifest = RunManifest(
        experiment_id=f"EXP-{tier.value}",
        created_at_utc=datetime(2026, 8, 21, tzinfo=UTC),
        seed=123,
        software_commit="same-frozen-engine-commit",
        software_dirty=software_dirty,
        software_environment=SoftwareEnvironment(
            python_version="3.12.3",
            python_implementation="CPython",
            operating_system="Linux",
            machine="x86_64",
            packages={"hdmatch": "0.1.0", "tzdata": tzdata_version},
        ),
        candidate_universe="known_month",
        aggregation_rule="duration_weighted_evidence",
        model_id="MODEL-A-CORE-V1",
        input_hashes={
            "blind_cases.json": blind_sha256,
            "ephemeris:sepl_18.se1": _HASH_A,
        },
        config_sha256=_HASH_B,
    )
    write_new_canonical_json(run_dir / "run.manifest.json", manifest)
    write_new_canonical_json(
        run_dir / "evaluation.json",
        _evaluation(
            tier,
            blind_sha256=blind_sha256,
            true_rank=true_rank,
            revealed_target_set_sha256=revealed_target_set_sha256,
        ),
    )
    # This intentionally malformed secret-named file proves the loader does not need it.
    (run_dir / "answer_key.json.enc").write_bytes(b"not-read-by-noise-comparison")
    return run_dir


def _run_dirs(tmp_path: Path) -> dict[NoiseTier, Path]:
    return {
        NoiseTier.ORACLE: _write_run(tmp_path, NoiseTier.ORACLE, true_rank=1),
        NoiseTier.LOW: _write_run(tmp_path, NoiseTier.LOW, true_rank=1),
        NoiseTier.MEDIUM: _write_run(tmp_path, NoiseTier.MEDIUM, true_rank=1),
        NoiseTier.ADVERSARIAL: _write_run(
            tmp_path,
            NoiseTier.ADVERSARIAL,
            true_rank=1,
        ),
    }


def test_runtime_builds_metadata_from_public_bound_artifacts(tmp_path: Path) -> None:
    run_dirs = _run_dirs(tmp_path)

    report = build_noise_benchmark_from_run_dirs(run_dirs)

    assert report.case_count == 2
    assert report.candidate_universe == "known_month"
    medium = report.tiers[2]
    assert medium.declared_noise.behavioral_confidence_values == (0.5, 0.75, 1.0)
    assert medium.declared_noise.measurement_reliability_values == (0.5, 0.75, 1.0)
    assert medium.source.metadata.run_manifest_sha256 == sha256_file(
        run_dirs[NoiseTier.MEDIUM] / "run.manifest.json"
    )


def test_runtime_rejects_noise_payload_not_equal_to_frozen_generator(tmp_path: Path) -> None:
    altered = noise_parameters_payload(GeneratorNoiseTier.LOW)
    altered["reliability_values"] = [1.0]
    run_dir = _write_run(
        tmp_path,
        NoiseTier.LOW,
        true_rank=1,
        noise_payload=altered,
    )

    with pytest.raises(NoiseBenchmarkInputError, match="frozen generator values"):
        load_revealed_noise_tier_run(run_dir, expected_tier=NoiseTier.LOW)


def test_runtime_rejects_manifest_that_does_not_bind_blind_input(tmp_path: Path) -> None:
    run_dir = _write_run(tmp_path, NoiseTier.ORACLE, true_rank=1)
    raw = load_json_bytes(run_dir / "run.manifest.json", require_canonical=True)
    assert isinstance(raw, dict)
    raw["input_hashes"]["blind_cases.json"] = _HASH_C
    (run_dir / "run.manifest.json").unlink()
    write_new_canonical_json(run_dir / "run.manifest.json", raw)

    with pytest.raises(NoiseBenchmarkInputError, match="does not bind"):
        load_revealed_noise_tier_run(run_dir, expected_tier=NoiseTier.ORACLE)


def test_runtime_rejects_dirty_recovery_manifest(tmp_path: Path) -> None:
    run_dir = _write_run(
        tmp_path,
        NoiseTier.ORACLE,
        true_rank=1,
        software_dirty=True,
    )

    with pytest.raises(NoiseBenchmarkInputError, match="clean committed"):
        load_revealed_noise_tier_run(run_dir, expected_tier=NoiseTier.ORACLE)


def test_runtime_rejects_legacy_report_without_revealed_target_hash(tmp_path: Path) -> None:
    run_dir = _write_run(
        tmp_path,
        NoiseTier.ORACLE,
        true_rank=1,
        revealed_target_set_sha256=None,
    )

    with pytest.raises(NoiseBenchmarkInputError, match="post-reveal target-set hash"):
        load_revealed_noise_tier_run(run_dir, expected_tier=NoiseTier.ORACLE)


def test_comparison_rejects_different_revealed_cohort_hash(tmp_path: Path) -> None:
    run_dirs = _run_dirs(tmp_path)
    changed_root = tmp_path / "changed-target"
    changed_root.mkdir()
    run_dirs[NoiseTier.ADVERSARIAL] = _write_run(
        changed_root,
        NoiseTier.ADVERSARIAL,
        true_rank=1,
        revealed_target_set_sha256=_HASH_D,
    )

    with pytest.raises(NoiseBenchmarkInputError, match="case_set_sha256"):
        build_noise_benchmark_from_run_dirs(run_dirs)


def test_comparison_binds_timezone_environment_into_candidate_universe(
    tmp_path: Path,
) -> None:
    run_dirs = _run_dirs(tmp_path)
    changed_root = tmp_path / "changed-environment"
    changed_root.mkdir()
    run_dirs[NoiseTier.MEDIUM] = _write_run(
        changed_root,
        NoiseTier.MEDIUM,
        true_rank=1,
        tzdata_version="2027.1",
    )

    with pytest.raises(NoiseBenchmarkInputError, match="candidate_universe_sha256"):
        build_noise_benchmark_from_run_dirs(run_dirs)


def test_cli_writes_canonical_comparison_and_refuses_overwrite(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    run_dirs = _run_dirs(tmp_path)
    output = tmp_path / "noise-comparison.json"
    arguments = [
        "compare-noise-tiers",
        "--oracle-run-dir",
        str(run_dirs[NoiseTier.ORACLE]),
        "--low-run-dir",
        str(run_dirs[NoiseTier.LOW]),
        "--medium-run-dir",
        str(run_dirs[NoiseTier.MEDIUM]),
        "--adversarial-run-dir",
        str(run_dirs[NoiseTier.ADVERSARIAL]),
        "--output",
        str(output),
    ]

    assert main(arguments) == 0
    assert load_json_bytes(output, require_canonical=True)["schema_version"] == (
        "noise-benchmark-report-v1"
    )
    assert "noise benchmark sha256" in capsys.readouterr().out
    with pytest.raises(SystemExit) as error:
        main(arguments)
    assert error.value.code == 2
