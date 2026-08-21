"""Command-line boundary for reproducible blind experiments."""

from __future__ import annotations

import argparse
import json
import secrets
import stat
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from hdmatch.config import load_synthetic_config
from hdmatch.evaluation.leakage import assert_no_blind_leakage
from hdmatch.evaluation.report import evaluate_frozen_run
from hdmatch.experiments import (
    ArtifactBindings,
    create_run_manifest,
    freeze_predictions,
    load_run_manifest,
    sha256_file,
    write_run_manifest,
)
from hdmatch.experiments.canonical import load_json_bytes, write_new_canonical_json
from hdmatch.experiments.reveal import reveal_answer_key
from hdmatch.model import compile_mapping_artifacts
from hdmatch.runtime import ExactChartAdapter, FrozenSymbolicModel, declared_ephemeris_files
from hdmatch.runtime.recovery import RecoverySettings, recover_blind_file
from hdmatch.search import AggregationMode
from hdmatch.synthetic import SyntheticGenerator, generate_key_file, seal_answer_key
from hdmatch.synthetic.sealing import SealingMetadata, require_external_path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MAPPING = ROOT / "mappings" / "mapping_library_v1.json"


def _read_secret_seed(path: str | Path | None) -> int:
    if path is None:
        return secrets.randbits(63)
    source = Path(path).expanduser()
    require_external_path(source, ROOT, label="generation seed file")
    if stat.S_IMODE(source.stat().st_mode) & 0o077:
        raise ValueError("generation seed file must have owner-only permissions")
    try:
        value = int(source.read_text(encoding="utf-8").strip())
    except (OSError, ValueError) as exc:
        raise ValueError("generation seed file must contain one integer") from exc
    if value < 0:
        raise ValueError("generation seed must be non-negative")
    return value


def _resolve_key_file(run_dir: Path, configured: str | None) -> Path:
    if configured is not None:
        return Path(configured).expanduser()
    secret_dir = Path("/tmp/hdmatch-secrets")
    return secret_dir / f"{run_dir.name}.aes256.key"


def _command_generate(args: argparse.Namespace) -> int:
    config_path = Path(args.config)
    config = load_synthetic_config(config_path)
    if config.seed is not None:
        raise ValueError(
            "generation seed must not be stored in a public config; use an external "
            "--seed-file or let the command create a sealed random seed"
        )
    ephemeris_path = args.ephemeris or config.ephemeris_path
    if not ephemeris_path:
        raise ValueError("exact generation requires --ephemeris")
    run_dir = Path(args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    blind_path = run_dir / "blind_cases.json"
    encrypted_path = run_dir / "answer_key.json.enc"
    leakage_path = run_dir / "leakage_audit.json"
    receipt_path = run_dir / "generation.receipt.json"
    for destination in (blind_path, encrypted_path, leakage_path, receipt_path):
        if destination.exists():
            raise FileExistsError(f"refusing to replace experiment artifact: {destination}")

    seed = _read_secret_seed(args.seed_file)
    resolved = config.model_copy(update={"seed": seed, "ephemeris_path": str(ephemeris_path)})
    chart = ExactChartAdapter(ephemeris_path)
    model = FrozenSymbolicModel(args.mapping)
    bundle = SyntheticGenerator(chart, model).generate(resolved)
    write_new_canonical_json(blind_path, bundle.blind_document)
    leakage = assert_no_blind_leakage(blind_path)
    write_new_canonical_json(leakage_path, leakage)

    key_file = _resolve_key_file(run_dir, args.key_file)
    require_external_path(key_file, ROOT, label="encryption key file")
    if not key_file.exists():
        generate_key_file(key_file, decoder_root=ROOT)
    metadata = SealingMetadata(
        experiment_id=config.experiment_id,
        blind_input_sha256=bundle.blind_input_sha256,
        model_sha256=model.model_sha256,
        question_bank_sha256=model.question_bank_sha256,
        mapping_sha256=model.mapping_sha256,
    )
    seal_answer_key(
        bundle.answer_key,
        encrypted_path=encrypted_path,
        key_path=key_file,
        metadata=metadata,
        decoder_root=ROOT,
    )
    receipt = {
        "schema_version": "generation-receipt-v1",
        "experiment_id": config.experiment_id,
        "blind_input_sha256": sha256_file(blind_path),
        "encrypted_answer_key_sha256": sha256_file(encrypted_path),
        "public_config_sha256": sha256_file(config_path),
        "model_sha256": model.model_sha256,
        "question_bank_sha256": model.question_bank_sha256,
        "mapping_sha256": model.mapping_sha256,
        "case_count": config.case_count,
        "seed_status": "sealed-in-answer-key-only",
        "claim_boundary": "synthetic-engineering-validation-only",
    }
    write_new_canonical_json(receipt_path, receipt)
    print(f"blind experiment: {blind_path}")
    print(f"blind input sha256: {receipt['blind_input_sha256']}")
    print(f"encrypted answer key: {encrypted_path}")
    print(f"external reveal key: {key_file}")
    return 0


def _prediction_bindings(payload: dict[str, Any]) -> ArtifactBindings:
    return ArtifactBindings(
        blind_input_sha256=str(payload["blind_input_sha256"]),
        model_sha256=str(payload["model_sha256"]),
        question_bank_sha256=str(payload["question_bank_sha256"]),
        mapping_sha256=str(payload["mapping_sha256"]),
    )


def _command_recover(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    blind_path = Path(args.blind_file) if args.blind_file else run_dir / "blind_cases.json"
    predictions_path = run_dir / "predictions.json"
    manifest_path = run_dir / "run.manifest.json"
    if predictions_path.exists():
        raise FileExistsError(f"refusing to replace frozen-intent artifact: {predictions_path}")
    blind = load_json_bytes(blind_path, require_canonical=True)
    if not isinstance(blind, dict):
        raise ValueError("blind file must contain an object")
    model = FrozenSymbolicModel(args.mapping)
    input_hashes = {
        "blind_cases.json": sha256_file(blind_path),
        "mapping_library": sha256_file(args.mapping),
    }
    for file in declared_ephemeris_files(args.ephemeris):
        input_hashes[f"ephemeris:{file.name}"] = sha256_file(file)
    public_recovery_seed = int(input_hashes["blind_cases.json"][:16], 16)
    settings = RecoverySettings(
        aggregation=AggregationMode(args.aggregation),
        threshold_rubric_bits=args.threshold,
        workers=args.workers,
    )
    manifest_config = {
        "aggregation": settings.aggregation.value,
        "threshold_rubric_bits": settings.threshold_rubric_bits,
        "workers": settings.workers,
        "cache_policy": "hash-bound exact month universes",
    }
    if manifest_path.exists():
        manifest = load_run_manifest(manifest_path)
        if manifest.input_hashes != dict(sorted(input_hashes.items())):
            raise ValueError("existing run manifest input bindings do not match this recovery")
    else:
        manifest = create_run_manifest(
            experiment_id=str(blind["experiment_id"]),
            seed=public_recovery_seed,
            repository_root=ROOT,
            candidate_universe=str(blind["candidate_universe"]),
            aggregation_rule=settings.aggregation.value,
            model_id=model.model_sha256,
            input_hashes=input_hashes,
            config=manifest_config,
            declared_outputs=("predictions.json", "prediction.freeze.json"),
        )
        write_run_manifest(manifest, manifest_path)
    predictions = recover_blind_file(
        blind_path,
        mapping_path=args.mapping,
        ephemeris_path=args.ephemeris,
        cache_dir=args.cache_dir or run_dir / "candidate_cache",
        settings=settings,
    )
    write_new_canonical_json(predictions_path, predictions)
    print(f"blind predictions: {predictions_path}")
    print(f"prediction sha256: {sha256_file(predictions_path)}")
    return 0


def _command_freeze(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    predictions = load_json_bytes(run_dir / "predictions.json", require_canonical=True)
    if not isinstance(predictions, dict):
        raise ValueError("predictions must contain an object")
    record = freeze_predictions(
        run_dir,
        experiment_id=str(predictions["experiment_id"]),
        bindings=_prediction_bindings(predictions),
        repository_root=ROOT,
        run_manifest_path=run_dir / "run.manifest.json",
    )
    print(f"prediction freeze: {run_dir / 'prediction.freeze.json'}")
    print(f"prediction sha256: {record.prediction_sha256}")
    return 0


def _write_transparent_reports(run_dir: Path, evaluation: Any) -> None:
    aggregate = evaluation.aggregate
    summary = {
        "schema_version": "transparent-oracle-report-v1",
        "experiment_id": evaluation.experiment_id,
        "case_count": aggregate.case_count,
        "metrics": {
            "top_1": aggregate.top_1,
            "top_3": aggregate.top_3,
            "top_5": aggregate.top_5,
            "mrr": aggregate.mean_reciprocal_rank,
            "mean_percentile": aggregate.mean_percentile,
            "tie_rate": aggregate.tie_rate,
            "unevaluable_case_count": aggregate.unevaluable_case_count,
        },
        "restoration": [item.model_dump(mode="json") for item in evaluation.restoration_curves],
        "ablation": [item.model_dump(mode="json") for item in evaluation.leave_one_cluster_out],
        "failure_counts": evaluation.failure_counts,
        "score_semantics": evaluation.score_semantics,
        "claim_boundary": evaluation.claim_boundary,
    }
    failures = {
        "schema_version": "oracle-failure-report-v1",
        "experiment_id": evaluation.experiment_id,
        "failure_count": len(evaluation.failures),
        "classification_counts": evaluation.failure_counts,
        "failures": [item.model_dump(mode="json") for item in evaluation.failures],
        "note": "No failure or tie is discarded; unresolved causes remain explicit.",
    }
    write_new_canonical_json(run_dir / "report.json", summary)
    write_new_canonical_json(run_dir / "failure_report.json", failures)


def _command_reveal_evaluate(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    encrypted = Path(args.encrypted_key) if args.encrypted_key else run_dir / "answer_key.json.enc"
    key_file = _resolve_key_file(run_dir, args.key_file)
    revealed = reveal_answer_key(
        run_dir,
        encrypted_answer_key_path=encrypted,
        key_path=key_file,
        decoder_root=ROOT,
    )
    evaluation = evaluate_frozen_run(run_dir, answer_key=revealed.answer_key)
    _write_transparent_reports(run_dir, evaluation)
    print(f"evaluation: {run_dir / 'evaluation.json'}")
    print(json.dumps(evaluation.aggregate.model_dump(mode="json"), sort_keys=True))
    return 0


def _command_compile_model(args: argparse.Namespace) -> int:
    result = compile_mapping_artifacts(args.repository_root)
    print(f"mapping library: {result.mapping_path}")
    print(f"mapping semantic sha256: {result.mapping_model_sha256}")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hdmatch",
        description=(
            "Blinded Human Design reverse-matching research harness; symbolic scores "
            "are experimental rubric values, not probabilities."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate-blind", help="generate and seal blind cases")
    generate.add_argument("--config", required=True)
    generate.add_argument("--run-dir", required=True)
    generate.add_argument("--ephemeris")
    generate.add_argument("--mapping", default=str(DEFAULT_MAPPING))
    generate.add_argument("--key-file")
    generate.add_argument("--seed-file")
    generate.set_defaults(handler=_command_generate)

    recover = subparsers.add_parser("recover", help="recover using blind input only")
    recover.add_argument("--run-dir", required=True)
    recover.add_argument("--blind-file")
    recover.add_argument("--ephemeris", required=True)
    recover.add_argument("--mapping", default=str(DEFAULT_MAPPING))
    recover.add_argument("--cache-dir")
    recover.add_argument("--workers", type=int, default=1)
    recover.add_argument(
        "--aggregation",
        choices=[item.value for item in AggregationMode],
        default=AggregationMode.DURATION_WEIGHTED_EVIDENCE.value,
    )
    recover.add_argument("--threshold", type=float, default=0.0)
    recover.set_defaults(handler=_command_recover)

    freeze = subparsers.add_parser("freeze", help="cryptographically freeze predictions")
    freeze.add_argument("--run-dir", required=True)
    freeze.set_defaults(handler=_command_freeze)

    reveal = subparsers.add_parser(
        "reveal-evaluate", help="reveal only after freeze and write evaluation reports"
    )
    reveal.add_argument("--run-dir", required=True)
    reveal.add_argument("--encrypted-key")
    reveal.add_argument("--key-file")
    reveal.set_defaults(handler=_command_reveal_evaluate)

    compiler = subparsers.add_parser("compile-model", help="rebuild frozen mapping artifacts")
    compiler.add_argument("--repository-root", default=str(ROOT))
    compiler.set_defaults(handler=_command_compile_model)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    handler = args.handler
    try:
        return int(handler(args))
    except (FileNotFoundError, FileExistsError, RuntimeError, ValueError, KeyError) as exc:
        parser.exit(2, f"hdmatch: error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
