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
from hdmatch.evaluation.model_comparison import audit_structural_discrimination
from hdmatch.evaluation.noise_benchmark import NoiseTier
from hdmatch.evaluation.report import evaluate_frozen_run
from hdmatch.experiments import (
    ArtifactBindings,
    create_run_manifest,
    freeze_predictions,
    load_run_manifest,
    sha256_file,
    verify_run_manifest_resume,
    write_run_manifest,
)
from hdmatch.experiments.canonical import load_json_bytes, write_new_canonical_json
from hdmatch.experiments.reveal import reveal_answer_key
from hdmatch.human import (
    fit_development_bundle_artifacts,
    freeze_prediction_artifacts,
    freeze_protocol_artifacts,
    import_human_cases,
    prepare_blind_cohort_artifacts,
    reveal_evaluate_artifacts,
    score_blind_artifacts,
    seal_human_answer_key_artifacts,
    symbolic_reference,
)
from hdmatch.model import compile_mapping_artifacts
from hdmatch.model_b.compiler import compile_model_b_artifacts
from hdmatch.model_b.mapping_library import FrozenModelB
from hdmatch.runtime import (
    MODEL_A_ID,
    MODEL_B_ID,
    ExactChartAdapter,
    RuntimeSymbolicModel,
    declared_ephemeris_files,
    load_runtime_model,
)
from hdmatch.runtime.noise_benchmark import (
    build_noise_benchmark_from_run_dirs,
    write_noise_benchmark_report,
)
from hdmatch.runtime.recovery import RecoverySettings, recover_blind_file
from hdmatch.runtime.universe_cache import MonthRequest, cache_path, load_cached_universe
from hdmatch.schemas import CandidateState
from hdmatch.search import AggregationMode
from hdmatch.synthetic import SyntheticGenerator, generate_key_file, seal_answer_key
from hdmatch.synthetic.sealing import (
    SealingMetadata,
    assert_no_plaintext_answer_keys_in_paths,
    require_external_path,
)

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MAPPING = ROOT / "mappings" / "mapping_library_v1.json"
DEFAULT_MODEL_B_ARTIFACT = ROOT / "mappings" / "model_b_mapping_library_v1.json"


def _load_selected_model(args: argparse.Namespace) -> RuntimeSymbolicModel:
    return load_runtime_model(
        str(args.model),
        model_a_mapping_path=args.mapping,
        model_b_artifact_path=args.model_b_artifact,
    )


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
    model = _load_selected_model(args)
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
        "model_id": model.model_id,
        "blind_input_sha256": sha256_file(blind_path),
        "encrypted_answer_key_sha256": sha256_file(encrypted_path),
        "public_config_sha256": sha256_file(config_path),
        "model_sha256": model.model_sha256,
        "question_bank_sha256": model.question_bank_sha256,
        "mapping_sha256": model.mapping_sha256,
        "case_count": config.case_count,
        "seed_status": "sealed-in-answer-key-only",
        "external_reveal_key_status": "owner-only-key-ready-path-withheld",
        "claim_boundary": "synthetic-engineering-validation-only",
    }
    write_new_canonical_json(receipt_path, receipt)
    print(f"blind experiment: {blind_path}")
    print(f"blind input sha256: {receipt['blind_input_sha256']}")
    print(f"encrypted answer key: {encrypted_path}")
    print(f"external reveal key status: {receipt['external_reveal_key_status']}")
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
    visible_paths: list[str | Path] = [ROOT, run_dir, blind_path, args.mapping]
    if args.cache_dir:
        visible_paths.append(args.cache_dir)
    if str(args.model) == MODEL_B_ID:
        visible_paths.append(args.model_b_artifact)
    assert_no_plaintext_answer_keys_in_paths(visible_paths)
    blind = load_json_bytes(blind_path, require_canonical=True)
    if not isinstance(blind, dict):
        raise ValueError("blind file must contain an object")
    model = _load_selected_model(args)
    input_hashes = {
        "blind_cases.json": sha256_file(blind_path),
        "model_a_mapping_library": sha256_file(args.mapping),
    }
    if model.model_id == MODEL_B_ID:
        input_hashes["model_b_artifact"] = sha256_file(args.model_b_artifact)
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
        verify_run_manifest_resume(
            manifest,
            experiment_id=str(blind["experiment_id"]),
            seed=public_recovery_seed,
            candidate_universe=str(blind["candidate_universe"]),
            aggregation_rule=settings.aggregation.value,
            model_id=model.model_id,
            input_hashes=input_hashes,
            config=manifest_config,
        )
    else:
        manifest = create_run_manifest(
            experiment_id=str(blind["experiment_id"]),
            seed=public_recovery_seed,
            repository_root=ROOT,
            candidate_universe=str(blind["candidate_universe"]),
            aggregation_rule=settings.aggregation.value,
            model_id=model.model_id,
            input_hashes=input_hashes,
            config=manifest_config,
            declared_outputs=("predictions.json", "prediction.freeze.json"),
        )
        write_run_manifest(manifest, manifest_path)
    predictions = recover_blind_file(
        blind_path,
        decoder_root=ROOT,
        model=model,
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
    if args.model == MODEL_A_ID:
        result = compile_mapping_artifacts(args.repository_root)
        print(f"mapping library: {result.mapping_path}")
        print(f"mapping semantic sha256: {result.mapping_model_sha256}")
    else:
        detailed = compile_model_b_artifacts(args.repository_root)
        print(f"mapping library: {detailed.artifact_path}")
        print(f"mapping semantic sha256: {detailed.artifact_semantic_sha256}")
        print(f"unresolved report: {detailed.report_path}")
    return 0


def _command_compare_models(args: argparse.Namespace) -> int:
    """Audit structural partition resolution without responses or answer keys."""

    if args.month_end < args.month_start:
        raise ValueError("month-end must not precede month-start")
    engine = ExactChartAdapter(args.ephemeris)
    artifact_path = Path(args.model_b_artifact)
    selected = load_runtime_model(
        MODEL_B_ID,
        model_a_mapping_path=args.mapping,
        model_b_artifact_path=artifact_path,
    )
    if not isinstance(selected, FrozenModelB):
        raise ValueError("Model B loader returned an incompatible runtime model")
    artifact = selected.artifact
    states: list[CandidateState] = []
    cache_hashes: dict[str, str] = {}
    for month in range(args.month_start, args.month_end + 1):
        request = MonthRequest(args.year, month, args.timezone)
        path = cache_path(args.cache_dir, request, engine.fingerprint)
        cached = load_cached_universe(
            path,
            request=request,
            engine_fingerprint=engine.fingerprint,
        )
        states.extend(cached.states)
        cache_hashes[path.name] = cached.sha256
    audit = audit_structural_discrimination(states, artifact)
    payload = {
        "schema_version": "model-structural-comparison-run-v1",
        "chart_engine_fingerprint": engine.fingerprint,
        "candidate_cache_sha256": dict(sorted(cache_hashes.items())),
        "model_a_mapping_sha256": artifact.base_mapping_sha256,
        "model_b_model_sha256": selected.model_sha256,
        "model_b_artifact_sha256": sha256_file(artifact_path),
        "model_b_artifact_semantic_sha256": artifact.sha256(),
        "answer_keys_used": False,
        "behavioral_recovery_performed": False,
        "audit": audit.model_dump(mode="json"),
    }
    write_new_canonical_json(args.output, payload)
    print(f"structural comparison: {args.output}")
    print(
        json.dumps(
            {
                "interval_count": audit.model_a.interval_count,
                "model_a_unique_signatures": audit.model_a.unique_signature_count,
                "model_b_unique_signatures": audit.model_b.unique_signature_count,
                "signature_count_gain": audit.signature_count_gain,
                "comparison_kind": audit.comparison_kind,
            },
            sort_keys=True,
        )
    )
    return 0


def _command_human_import(args: argparse.Namespace) -> int:
    receipt = import_human_cases(
        args.dataset,
        args.output_dir,
        questionnaire_version=args.questionnaire_version,
        seed=args.seed,
        validation_fraction=args.validation_fraction,
        final_test_fraction=args.final_test_fraction,
        repository_root=ROOT,
    )
    print(f"private human import: {Path(args.output_dir) / 'human.dataset.json'}")
    print(f"person split: {Path(args.output_dir) / 'person.split.json'}")
    print(f"import outputs: {json.dumps(receipt.output_sha256, sort_keys=True)}")
    return 0


def _command_human_prepare_blind(args: argparse.Namespace) -> int:
    blind, _, receipt = prepare_blind_cohort_artifacts(
        args.partition,
        args.candidate_universe,
        args.protocol,
        args.output_dir,
        answer_key_output_path=args.answer_key_out,
        repository_root=ROOT,
    )
    blind_path = Path(args.output_dir) / "human.blind-cohort.json"
    print(f"human blind cohort: {blind_path}")
    print(f"blind input semantic sha256: {blind.blind_input_sha256}")
    print(f"plaintext answer key written outside decoder root: {args.answer_key_out}")
    print(f"preparation inputs: {json.dumps(receipt.input_sha256, sort_keys=True)}")
    return 0


def _command_human_fit(args: argparse.Namespace) -> int:
    runtime = _load_selected_model(args)
    bundle, receipt = fit_development_bundle_artifacts(
        args.dataset,
        args.split_manifest,
        args.output_dir,
        bundle_id=args.bundle_id,
        symbolic_model=symbolic_reference(runtime),
        empirical_feature_names=tuple(args.feature),
        alpha=args.alpha,
        hybrid_symbolic_weight=args.hybrid_symbolic_weight,
        permutation_count=args.permutation_count,
        permutation_seed=args.permutation_seed,
        repository_root=ROOT,
    )
    print(f"human model bundle: {Path(args.output_dir) / 'human-model.bundle.json'}")
    print(f"bundle semantic sha256: {bundle.sha256}")
    print(f"fit inputs: {json.dumps(receipt.input_sha256, sort_keys=True)}")
    return 0


def _command_human_freeze_protocol(args: argparse.Namespace) -> int:
    protocol, receipt = freeze_protocol_artifacts(
        args.bundle,
        args.split_manifest,
        args.output_dir,
        protocol_id=args.protocol_id,
        cohort=args.cohort,
        candidate_universe_rule=args.candidate_universe_rule,
        selected_primary_method=args.selected_primary_method,
        final_test_release_id=args.final_test_release_id,
        release_authorization=args.final_test_release_acknowledgement,
        release_ledger_dir=args.release_ledger,
        repository_root=ROOT,
    )
    print(f"human protocol: {Path(args.output_dir) / 'human-evaluation.protocol.json'}")
    print(f"protocol semantic sha256: {protocol.sha256}")
    print(f"protocol outputs: {json.dumps(receipt.output_sha256, sort_keys=True)}")
    return 0


def _command_human_seal_key(args: argparse.Namespace) -> int:
    receipt = seal_human_answer_key_artifacts(
        args.plaintext_answer_key,
        args.key_file,
        args.bundle,
        args.protocol,
        args.blind_cohort,
        args.output_dir,
        repository_root=ROOT,
    )
    print(f"encrypted human answer key: {Path(args.output_dir) / 'human.answer-key.json.enc'}")
    print(f"key-seal outputs: {json.dumps(receipt.output_sha256, sort_keys=True)}")
    return 0


def _command_human_score(args: argparse.Namespace) -> int:
    runtime = _load_selected_model(args)
    predictions, receipt = score_blind_artifacts(
        args.blind_cohort,
        args.bundle,
        args.protocol,
        args.symbolic_prevalence,
        args.symbolic_prevalence_source,
        args.output_dir,
        runtime_symbolic_model=runtime,
        repository_root=ROOT,
    )
    print(f"human blind predictions: {Path(args.output_dir) / 'human.predictions.json'}")
    prediction_hash = sha256_file(Path(args.output_dir) / "human.predictions.json")
    print(f"prediction file sha256: {prediction_hash}")
    print(f"answer key accessed: {predictions.answer_key_accessed}")
    print(f"score inputs: {json.dumps(receipt.input_sha256, sort_keys=True)}")
    return 0


def _command_human_freeze(args: argparse.Namespace) -> int:
    freeze, receipt = freeze_prediction_artifacts(
        args.predictions,
        args.bundle,
        args.protocol,
        args.output_dir,
        release_ledger_dir=args.release_ledger,
        repository_root=ROOT,
    )
    print(f"human prediction freeze: {Path(args.output_dir) / 'human.prediction.freeze.json'}")
    print(f"prediction sha256: {freeze.prediction_sha256}")
    print(f"freeze outputs: {json.dumps(receipt.output_sha256, sort_keys=True)}")
    return 0


def _command_human_reveal_evaluate(args: argparse.Namespace) -> int:
    report, _, receipt = reveal_evaluate_artifacts(
        args.predictions,
        args.prediction_freeze,
        args.bundle,
        args.protocol,
        args.encrypted_answer_key,
        args.key_file,
        args.output_dir,
        release_ledger_dir=args.release_ledger,
        repository_root=ROOT,
    )
    print(f"human comparison report: {Path(args.output_dir) / 'human.comparison.report.json'}")
    print(f"claim boundary: {report.claim_boundary}")
    print(f"evaluation outputs: {json.dumps(receipt.output_sha256, sort_keys=True)}")
    return 0


def _command_compare_noise_tiers(args: argparse.Namespace) -> int:
    """Aggregate already-revealed public artifacts without reading answer keys."""

    run_dirs = {
        NoiseTier.ORACLE: args.oracle_run_dir,
        NoiseTier.LOW: args.low_run_dir,
        NoiseTier.MEDIUM: args.medium_run_dir,
        NoiseTier.ADVERSARIAL: args.adversarial_run_dir,
    }
    report = build_noise_benchmark_from_run_dirs(run_dirs)
    output = write_noise_benchmark_report(report, args.output)
    print(f"noise benchmark: {output}")
    print(f"noise benchmark sha256: {sha256_file(output)}")
    print(
        json.dumps(
            {
                item.tier.value: {
                    "top_1": item.aggregate.top_1,
                    "top_3": item.aggregate.top_3,
                    "top_5": item.aggregate.top_5,
                    "mrr": item.aggregate.mean_reciprocal_rank,
                    "unevaluable": item.aggregate.unevaluable_case_count,
                }
                for item in report.tiers
            },
            sort_keys=True,
        )
    )
    return 0


def _add_model_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--model",
        choices=(MODEL_A_ID, MODEL_B_ID),
        default=MODEL_A_ID,
    )
    parser.add_argument("--mapping", default=str(DEFAULT_MAPPING))
    parser.add_argument("--model-b-artifact", default=str(DEFAULT_MODEL_B_ARTIFACT))


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
    _add_model_arguments(generate)
    generate.add_argument("--key-file")
    generate.add_argument("--seed-file")
    generate.set_defaults(handler=_command_generate)

    recover = subparsers.add_parser("recover", help="recover using blind input only")
    recover.add_argument("--run-dir", required=True)
    recover.add_argument("--blind-file")
    recover.add_argument("--ephemeris", required=True)
    _add_model_arguments(recover)
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
    compiler.add_argument(
        "--model",
        choices=(MODEL_A_ID, MODEL_B_ID),
        default=MODEL_A_ID,
    )
    compiler.set_defaults(handler=_command_compile_model)

    comparison = subparsers.add_parser(
        "compare-models",
        help="audit Model A/B structural resolution without behavioral recovery",
    )
    comparison.add_argument("--cache-dir", required=True)
    comparison.add_argument("--ephemeris", required=True)
    comparison.add_argument("--output", required=True)
    comparison.add_argument("--year", type=int, required=True)
    comparison.add_argument("--timezone", default="UTC")
    comparison.add_argument("--month-start", type=int, choices=range(1, 13), default=1)
    comparison.add_argument("--month-end", type=int, choices=range(1, 13), default=12)
    comparison.add_argument("--model-b-artifact", default=str(DEFAULT_MODEL_B_ARTIFACT))
    comparison.add_argument("--mapping", default=str(DEFAULT_MAPPING))
    comparison.set_defaults(handler=_command_compare_models)

    human_import = subparsers.add_parser(
        "human-import",
        help="validate and person-split a private human dataset outside the repository",
    )
    human_import.add_argument("--dataset", required=True)
    human_import.add_argument("--questionnaire-version", required=True)
    human_import.add_argument("--output-dir", required=True)
    human_import.add_argument("--seed", type=int, required=True)
    human_import.add_argument("--validation-fraction", type=float, default=0.2)
    human_import.add_argument("--final-test-fraction", type=float, default=0.2)
    human_import.set_defaults(handler=_command_human_import)

    human_prepare = subparsers.add_parser(
        "human-prepare-blind",
        help="strip a private rich partition into a blind cohort and external truth key",
    )
    human_prepare.add_argument("--partition", required=True)
    human_prepare.add_argument("--candidate-universe", required=True)
    human_prepare.add_argument("--protocol", required=True)
    human_prepare.add_argument("--output-dir", required=True)
    human_prepare.add_argument("--answer-key-out", required=True)
    human_prepare.set_defaults(handler=_command_human_prepare_blind)

    human_fit = subparsers.add_parser(
        "human-fit",
        help="validate a full person split and fit development people only",
    )
    human_fit.add_argument("--dataset", required=True)
    human_fit.add_argument("--split-manifest", required=True)
    human_fit.add_argument("--output-dir", required=True)
    human_fit.add_argument("--bundle-id", required=True)
    human_fit.add_argument("--feature", action="append", required=True)
    human_fit.add_argument("--alpha", type=float, default=2.0)
    human_fit.add_argument("--hybrid-symbolic-weight", type=float, default=1.0)
    human_fit.add_argument("--permutation-count", type=int, default=32)
    human_fit.add_argument("--permutation-seed", type=int, default=0)
    _add_model_arguments(human_fit)
    human_fit.set_defaults(handler=_command_human_fit)

    human_protocol = subparsers.add_parser(
        "human-freeze-protocol",
        help="freeze one person-level cohort protocol and optional final release ledger",
    )
    human_protocol.add_argument("--bundle", required=True)
    human_protocol.add_argument("--split-manifest", required=True)
    human_protocol.add_argument("--output-dir", required=True)
    human_protocol.add_argument("--protocol-id", required=True)
    human_protocol.add_argument(
        "--cohort",
        choices=("development", "validation", "final_test"),
        required=True,
    )
    human_protocol.add_argument("--candidate-universe-rule", required=True)
    human_protocol.add_argument("--selected-primary-method", required=True)
    human_protocol.add_argument("--final-test-release-id")
    human_protocol.add_argument("--final-test-release-acknowledgement")
    human_protocol.add_argument("--release-ledger")
    human_protocol.set_defaults(handler=_command_human_freeze_protocol)

    human_seal = subparsers.add_parser(
        "human-seal-key",
        help="seal a human answer key using external owner-only AES key material",
    )
    human_seal.add_argument("--plaintext-answer-key", required=True)
    human_seal.add_argument("--key-file", required=True)
    human_seal.add_argument("--bundle", required=True)
    human_seal.add_argument("--protocol", required=True)
    human_seal.add_argument("--blind-cohort", required=True)
    human_seal.add_argument("--output-dir", required=True)
    human_seal.set_defaults(handler=_command_human_seal_key)

    human_score = subparsers.add_parser(
        "human-score",
        help="blind-score a frozen human cohort without accepting key access",
    )
    human_score.add_argument("--blind-cohort", required=True)
    human_score.add_argument("--bundle", required=True)
    human_score.add_argument("--protocol", required=True)
    human_score.add_argument("--symbolic-prevalence", required=True)
    human_score.add_argument("--symbolic-prevalence-source", required=True)
    human_score.add_argument("--output-dir", required=True)
    _add_model_arguments(human_score)
    human_score.set_defaults(handler=_command_human_score)

    human_freeze = subparsers.add_parser(
        "human-freeze",
        help="freeze exact human prediction bytes before any reveal",
    )
    human_freeze.add_argument("--predictions", required=True)
    human_freeze.add_argument("--bundle", required=True)
    human_freeze.add_argument("--protocol", required=True)
    human_freeze.add_argument("--output-dir", required=True)
    human_freeze.add_argument("--release-ledger")
    human_freeze.set_defaults(handler=_command_human_freeze)

    human_reveal = subparsers.add_parser(
        "human-reveal-evaluate",
        help="verify freeze, decrypt an external-key envelope, reveal, and evaluate",
    )
    human_reveal.add_argument("--predictions", required=True)
    human_reveal.add_argument("--prediction-freeze", required=True)
    human_reveal.add_argument("--bundle", required=True)
    human_reveal.add_argument("--protocol", required=True)
    human_reveal.add_argument("--encrypted-answer-key", required=True)
    human_reveal.add_argument("--key-file", required=True)
    human_reveal.add_argument("--output-dir", required=True)
    human_reveal.add_argument("--release-ledger")
    human_reveal.set_defaults(handler=_command_human_reveal_evaluate)

    noise_comparison = subparsers.add_parser(
        "compare-noise-tiers",
        help="compare four revealed frozen synthetic evaluations without answer keys",
    )
    noise_comparison.add_argument("--oracle-run-dir", required=True)
    noise_comparison.add_argument("--low-run-dir", required=True)
    noise_comparison.add_argument("--medium-run-dir", required=True)
    noise_comparison.add_argument("--adversarial-run-dir", required=True)
    noise_comparison.add_argument("--output", required=True)
    noise_comparison.set_defaults(handler=_command_compare_noise_tiers)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    handler = args.handler
    try:
        return int(handler(args))
    except (
        FileNotFoundError,
        FileExistsError,
        PermissionError,
        RuntimeError,
        ValueError,
        KeyError,
    ) as exc:
        parser.exit(2, f"hdmatch: error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
