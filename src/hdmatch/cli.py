"""Command-line boundary for reproducible blind experiments."""

from __future__ import annotations

import argparse
import json
import secrets
import stat
from collections.abc import Sequence
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from hdmatch.century_cache import (
    CANONICAL_CENTURY_END_EXCLUSIVE_UTC,
    CANONICAL_CENTURY_START_UTC,
    PublishedCenturyBuild,
    assemble_and_publish_century_cache,
    build_all_missing_century_jobs,
    build_century_staged_job,
    finalize_century_cache_publication,
    preflight_century_cache_publication_paths,
    prepare_century_build,
    verify_century_cache_against_trust_lock,
)
from hdmatch.chart import validate_production_engine
from hdmatch.config import load_synthetic_config
from hdmatch.evaluation.behavioral_difference import (
    VerifiedBehavioralDifferenceBinding,
    audit_behavioral_difference,
    load_behavioral_difference_audit,
    require_behavioral_difference,
    verify_behavioral_difference_audit,
)
from hdmatch.evaluation.leakage import assert_no_blind_leakage
from hdmatch.evaluation.model_comparison import audit_structural_discrimination
from hdmatch.evaluation.noise_benchmark import NoiseTier
from hdmatch.evaluation.paired_model_comparison import (
    compare_model_a_v2_new_run_dirs,
    write_paired_model_comparison_report,
)
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
from hdmatch.experiments.manifest import capture_software_environment, git_revision
from hdmatch.experiments.paired import (
    PairedExperimentPlan,
    create_paired_experiment_plan,
    create_paired_generation_receipt_binding,
    generation_seed_commitment,
    load_paired_experiment_plan,
    verify_generation_seed_commitment,
    verify_paired_experiment_plan,
    verify_paired_generation_receipt_binding,
    write_paired_experiment_plan,
    write_paired_generation_receipt_binding,
)
from hdmatch.experiments.paired_freeze import (
    PairedFreezeArmArtifacts,
    create_paired_prediction_freeze_receipt,
    verify_paired_prediction_freeze_receipt,
    write_paired_prediction_freeze_receipt,
)
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
from hdmatch.model.v4_3_prevalence import (
    build_v4_3_prevalence_artifact,
    derive_v4_3_prevalence_plan,
    verify_v4_3_prevalence_artifact,
    write_v4_3_prevalence_artifact_new,
    write_v4_3_prevalence_plan_new,
)
from hdmatch.model.v4_3_profile_mapping import (
    BEST_CURRENT_COMPILED_PATH,
    BEST_CURRENT_SOURCE_PATH,
)
from hdmatch.model.v4_3_responses import BEST_CURRENT_RESPONSE_PATH
from hdmatch.model.v4_3_run import run_verified_v4_3_cache, verify_v4_3_run
from hdmatch.model_b.compiler import compile_model_b_artifacts
from hdmatch.model_b.mapping_library import FrozenModelB
from hdmatch.model_b_v2_new import (
    FrozenModelBV2New,
    compile_model_b_v2_new,
    freeze_model_b_v2_new,
)
from hdmatch.provenance import verify_ephemeris_directory
from hdmatch.runtime import (
    MODEL_A_ID,
    MODEL_B_ID,
    MODEL_B_V2_NEW_ID,
    ExactChartAdapter,
    FrozenSymbolicModel,
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
DEFAULT_EPHEMERIS_SOURCE_MANIFEST = ROOT / "data" / "ephemeris" / "manifest.json"
DEFAULT_EPHEMERIS_DIRECTORY = ROOT / "data" / "ephemeris"
DEFAULT_ENGINE_VALIDATION = (
    ROOT / "reports" / "v4_3_migration" / "phase0_engine_validation.json"
)
DEFAULT_SWIEPH_GOLDEN_REFERENCE = (
    ROOT / "tests" / "golden" / "fixtures" / "swieph_phase0_golden_v1.json"
)
DEFAULT_CENTURY_BUILD_DIRECTORY = ROOT / "data" / "century_cache" / "build-v1"
DEFAULT_CENTURY_PLAN = DEFAULT_CENTURY_BUILD_DIRECTORY / "plan.json"
DEFAULT_CENTURY_PARITY_REPORT = (
    DEFAULT_CENTURY_BUILD_DIRECTORY / "parity-report.json"
)
DEFAULT_CENTURY_STAGING_DIRECTORY = DEFAULT_CENTURY_BUILD_DIRECTORY / "staged"
DEFAULT_CENTURY_BUILD_EVIDENCE_DIRECTORY = (
    DEFAULT_CENTURY_BUILD_DIRECTORY / "evidence"
)
DEFAULT_CENTURY_CACHE_DIRECTORY = ROOT / "data" / "century_cache" / "v1"
DEFAULT_CENTURY_CACHE_TRUST_LOCK = (
    ROOT / "data" / "century_cache" / "v1.trust-lock.json"
)
DEFAULT_CENTURY_CACHE_LOCATOR = "data/century_cache/v1"
DEFAULT_V43_MAPPING_LIBRARY = ROOT / BEST_CURRENT_COMPILED_PATH
DEFAULT_V43_MAPPING_SOURCE_LIBRARY = ROOT / BEST_CURRENT_SOURCE_PATH
DEFAULT_V43_RESPONSE_ARTIFACT = ROOT / BEST_CURRENT_RESPONSE_PATH
DEFAULT_V43_PREVALENCE_DIRECTORY = ROOT / "data" / "v4_3_prevalence" / "best-current"
DEFAULT_V43_PREVALENCE_PLAN = DEFAULT_V43_PREVALENCE_DIRECTORY / "plan.json"
DEFAULT_V43_PREVALENCE_ARTIFACT = DEFAULT_V43_PREVALENCE_DIRECTORY / "artifact.json"


def _command_validate_engine(args: argparse.Namespace) -> int:
    """Prove the canonical local Swiss-file engine without permitting fallback."""

    ephemeris_path = Path(args.ephemeris_path)
    verified_files = verify_ephemeris_directory(
        source_manifest_path=args.source_manifest,
        ephemeris_directory=ephemeris_path,
    )
    adapter = ExactChartAdapter(ephemeris_path)
    validation = validate_production_engine(adapter.provider)
    if validation.ephemeris_requested.value != "SWIEPH":
        raise ValueError("production engine validation did not request SWIEPH")
    if validation.ephemeris_returned.value != "SWIEPH":
        raise ValueError("production engine validation did not return SWIEPH")

    validation_payload = asdict(validation)
    validation_payload.pop("ephemeris_path", None)
    validation_payload["node_convention"] = adapter.provider.metadata.node_convention.value
    validation_payload["files"] = [
        {
            "name": Path(record.path).name,
            "sha256": record.sha256,
            "size_bytes": record.size_bytes,
        }
        for record in validation.files
    ]
    software_commit, software_dirty = git_revision(ROOT)
    receipt = {
        "schema_version": "production-engine-validation-receipt-v1",
        "validation_status": "pass",
        "software_commit": software_commit,
        "software_dirty": software_dirty,
        "software_environment": capture_software_environment().model_dump(mode="json"),
        "ephemeris_mode_argument": "SWIEPH",
        "ephemeris_provenance": verified_files.manifest_binding(),
        "engine_validation": validation_payload,
        "claim_boundary": (
            "astronomy-engine-phase-0-only-not-a-v4-3-cache-or-behavioral-result"
        ),
    }
    output_arg = getattr(args, "output", None)
    if output_arg:
        output = write_new_canonical_json(output_arg, receipt)
        print(f"engine validation receipt: {output}")
        print(f"engine validation sha256: {sha256_file(output)}")
    print(
        json.dumps(
            {
                "validation_status": "pass",
                "ephemeris_requested": validation.ephemeris_requested.value,
                "ephemeris_returned": validation.ephemeris_returned.value,
                "representative_calculations": len(validation.calculation_probes),
                "design_roots": len(validation.design_root_probes),
                "source_commit": verified_files.source_commit,
                "ephemeris_file_set_sha256": (
                    verified_files.ephemeris_file_set_sha256
                ),
            },
            sort_keys=True,
        )
    )
    return 0


def _parse_utc_timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"invalid ISO-8601 timestamp: {value}"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise argparse.ArgumentTypeError("timestamp must include a UTC offset")
    return parsed.astimezone(UTC)


def _command_prepare_century_cache(args: argparse.Namespace) -> int:
    prepared = prepare_century_build(
        repository_root=args.repository_root,
        utc_start=args.start,
        utc_end_exclusive=args.end_exclusive,
        ephemeris_directory=args.ephemeris_path,
        ephemeris_source_manifest_path=args.source_manifest,
        engine_validation_path=args.engine_validation,
        golden_reference_path=args.golden_reference,
        reference_source_locator=args.reference_source_locator,
        parity_report_path=args.parity_report,
        plan_path=args.plan,
    )
    print(
        json.dumps(
            {
                "job_count": prepared.job_count,
                "parity_report_sha256": prepared.parity_report_sha256,
                "plan_sha256": prepared.plan_sha256,
                "status": "prepared",
            },
            sort_keys=True,
        )
    )
    return 0


def _command_build_century_cache_job(args: argparse.Namespace) -> int:
    receipt = build_century_staged_job(
        plan_path=args.plan,
        job_id=args.job_id,
        staging_directory=args.staging_dir,
        ephemeris_directory=args.ephemeris_path,
        ephemeris_source_manifest_path=args.source_manifest,
    )
    print(
        json.dumps(
            {
                "artifact_sha256": receipt.artifact_sha256,
                "interval_count": receipt.interval_count,
                "job_id": receipt.job_id,
                "status": receipt.verification_status,
            },
            sort_keys=True,
        )
    )
    return 0


def _published_cache_summary(published: PublishedCenturyBuild) -> dict[str, object]:
    # Kept as a small boundary helper so the command handlers expose no row data.
    verified = published.verified_cache
    return {
        "cache_manifest_sha256": verified.manifest_sha256,
        "interval_count": verified.manifest.interval_count,
        "logical_universe_sha256": verified.manifest.logical_universe_sha256,
        "status": verified.manifest.verification_status,
        "trust_lock_sha256": sha256_file(published.trust_lock_path),
    }


def _assemble_century_cache_from_args(
    args: argparse.Namespace,
) -> PublishedCenturyBuild:
    return assemble_and_publish_century_cache(
        plan_path=args.plan,
        staging_directory=args.staging_dir,
        cache_directory=args.output,
        cache_locator=args.cache_locator,
        trust_lock_path=args.trust_lock,
        build_evidence_directory=args.build_evidence_dir,
        ephemeris_directory=args.ephemeris_path,
        ephemeris_source_manifest_path=args.source_manifest,
        engine_validation_path=args.engine_validation,
        parity_report_path=args.parity_report,
        parity_reference_source_path=args.golden_reference,
    )


def _command_assemble_century_cache(args: argparse.Namespace) -> int:
    print(
        json.dumps(
            _published_cache_summary(_assemble_century_cache_from_args(args)),
            sort_keys=True,
        )
    )
    return 0


def _command_build_century_cache(args: argparse.Namespace) -> int:
    publication_state = preflight_century_cache_publication_paths(
        cache_directory=args.output,
        trust_lock_path=args.trust_lock,
    )
    if publication_state != "new":
        print(
            json.dumps(
                _published_cache_summary(_assemble_century_cache_from_args(args)),
                sort_keys=True,
            )
        )
        return 0
    receipts = build_all_missing_century_jobs(
        plan_path=args.plan,
        staging_directory=args.staging_dir,
        ephemeris_directory=args.ephemeris_path,
        ephemeris_source_manifest_path=args.source_manifest,
    )
    published = _assemble_century_cache_from_args(args)
    summary = _published_cache_summary(published)
    summary["staged_job_count"] = len(receipts)
    print(json.dumps(summary, sort_keys=True))
    return 0


def _command_finalize_century_cache_publication(args: argparse.Namespace) -> int:
    published = finalize_century_cache_publication(
        plan_path=args.plan,
        cache_directory=args.output,
        cache_locator=args.cache_locator,
        trust_lock_path=args.trust_lock,
        build_evidence_directory=args.build_evidence_dir,
        ephemeris_directory=args.ephemeris_path,
        ephemeris_source_manifest_path=args.source_manifest,
        engine_validation_path=args.engine_validation,
        parity_report_path=args.parity_report,
        parity_reference_source_path=args.golden_reference,
    )
    print(json.dumps(_published_cache_summary(published), sort_keys=True))
    return 0


def _command_verify_century_cache(args: argparse.Namespace) -> int:
    verified = verify_century_cache_against_trust_lock(
        args.cache_directory,
        trust_lock_path=args.trust_lock,
    )
    print(
        json.dumps(
            {
                "cache_manifest_sha256": verified.manifest_sha256,
                "interval_count": verified.manifest.interval_count,
                "logical_universe_sha256": (
                    verified.manifest.logical_universe_sha256
                ),
                "status": verified.manifest.verification_status,
            },
            sort_keys=True,
        )
    )
    return 0


def _v4_3_mapping_kwargs(args: argparse.Namespace) -> dict[str, str]:
    return {
        "mapping_library_path": str(args.mapping_library),
        "mapping_source_library_path": str(args.mapping_source_library),
        "mapping_repository_root": str(args.repository_root),
    }


def _command_build_v4_3_prevalence(args: argparse.Namespace) -> int:
    mapping_kwargs = _v4_3_mapping_kwargs(args)
    plan = derive_v4_3_prevalence_plan(
        args.cache,
        trust_lock_path=args.trust_lock,
        **mapping_kwargs,
    )
    plan_path = write_v4_3_prevalence_plan_new(args.plan_output, plan)
    artifact = build_v4_3_prevalence_artifact(
        args.cache,
        trust_lock_path=args.trust_lock,
        prevalence_plan_path=plan_path,
        **mapping_kwargs,
    )
    artifact_path = write_v4_3_prevalence_artifact_new(
        args.artifact_output,
        artifact,
    )
    provider = verify_v4_3_prevalence_artifact(
        artifact_path,
        cache_directory=args.cache,
        trust_lock_path=args.trust_lock,
        prevalence_plan_path=plan_path,
        **mapping_kwargs,
    )
    print(
        json.dumps(
            {
                "artifact_sha256": provider.provenance.artifact_sha256,
                "logical_universe_sha256": provider.provenance.universe_sha256,
                "plan_sha256": provider.provenance.plan_sha256,
                "status": "verified",
            },
            sort_keys=True,
        )
    )
    return 0


def _command_verify_v4_3_prevalence(args: argparse.Namespace) -> int:
    provider = verify_v4_3_prevalence_artifact(
        args.artifact,
        cache_directory=args.cache,
        trust_lock_path=args.trust_lock,
        prevalence_plan_path=args.plan,
        **_v4_3_mapping_kwargs(args),
    )
    print(
        json.dumps(
            {
                "anchor_count": len(provider.provenance.anchor_ids),
                "artifact_sha256": provider.provenance.artifact_sha256,
                "logical_universe_sha256": provider.provenance.universe_sha256,
                "status": "verified",
            },
            sort_keys=True,
        )
    )
    return 0


def _v4_3_run_kwargs(args: argparse.Namespace) -> dict[str, str]:
    return {
        "repository_root": str(args.repository_root),
        "cache_directory": str(args.cache),
        "trust_lock_path": str(args.trust_lock),
        "mapping_library_path": str(args.mapping_library),
        "mapping_source_library_path": str(args.mapping_source_library),
        "prevalence_plan_path": str(args.prevalence_plan),
        "prevalence_artifact_path": str(args.prevalence_artifact),
        "response_artifact_path": str(args.responses),
    }


def _command_run_v4_3_cache(args: argparse.Namespace) -> int:
    verified = run_verified_v4_3_cache(
        output_directory=args.output,
        detail_limit=args.detail_limit,
        **_v4_3_run_kwargs(args),
    )
    print(
        json.dumps(
            {
                "manifest_sha256": verified.manifest_sha256,
                "ranked_row_count": verified.manifest.successfully_scored_count,
                "run_status": verified.manifest.run_status,
                "v4_3_compliant": bool(
                    verified.manifest.compliance
                    and verified.manifest.compliance.v4_3_compliant
                ),
            },
            sort_keys=True,
        )
    )
    return 0


def _command_verify_v4_3_run(args: argparse.Namespace) -> int:
    verified = verify_v4_3_run(
        args.run_directory,
        **_v4_3_run_kwargs(args),
    )
    print(
        json.dumps(
            {
                "manifest_sha256": verified.manifest_sha256,
                "run_status": verified.manifest.run_status,
                "status": "verified",
            },
            sort_keys=True,
        )
    )
    return 0


def _load_selected_model(args: argparse.Namespace) -> RuntimeSymbolicModel:
    return load_runtime_model(
        str(args.model),
        model_a_mapping_path=args.mapping,
        model_b_artifact_path=args.model_b_artifact,
        model_b_v2_compiled_path=args.model_b_v2_compiled,
        model_b_v2_freeze_path=args.model_b_v2_freeze,
    )


def _require_v2_public_inputs(args: argparse.Namespace) -> tuple[str, str]:
    compiled = args.model_b_v2_compiled
    freeze = args.model_b_v2_freeze
    if not compiled or not freeze:
        raise ValueError(
            "MODEL-B-DETAILED-V2-NEW requires --model-b-v2-compiled and --model-b-v2-freeze"
        )
    return str(compiled), str(freeze)


def _require_v2_difference_inputs(args: argparse.Namespace) -> tuple[str, str]:
    audit = getattr(args, "model_b_v2_difference_audit", None)
    cache = getattr(args, "model_b_v2_difference_cache", None)
    if not audit or not cache:
        raise ValueError(
            "MODEL-B-DETAILED-V2-NEW requires --model-b-v2-difference-audit and "
            "--model-b-v2-difference-cache"
        )
    return str(audit), str(cache)


def _reject_inapplicable_v2_difference_inputs(args: argparse.Namespace) -> None:
    if getattr(args, "model_b_v2_difference_audit", None) or getattr(
        args, "model_b_v2_difference_cache", None
    ):
        raise ValueError("behavioral-difference inputs are only valid for MODEL-B-DETAILED-V2-NEW")


def _verify_v2_difference_gate(
    args: argparse.Namespace,
    *,
    model: FrozenModelBV2New,
    ephemeris_path: str | Path,
    expected_binding: VerifiedBehavioralDifferenceBinding | None = None,
) -> VerifiedBehavioralDifferenceBinding:
    audit_path, cache_path_value = _require_v2_difference_inputs(args)
    audit = load_behavioral_difference_audit(audit_path)
    request = audit.candidate_universe_request.to_runtime()
    engine = ExactChartAdapter(ephemeris_path)
    model_a = load_runtime_model(MODEL_A_ID, model_a_mapping_path=args.mapping)
    if not isinstance(model_a, FrozenSymbolicModel):
        raise TypeError("V2 difference verification requires the frozen Model A runtime")
    binding = verify_behavioral_difference_audit(
        audit_path,
        model_a=model_a,
        model_b=model,
        candidate_cache_path=cache_path_value,
        candidate_request=request,
        engine_fingerprint=engine.fingerprint,
        expected_binding=expected_binding,
    )
    if binding.audited_at_utc < model.freeze_receipt.frozen_at_utc:
        raise ValueError("behavioral-difference audit must follow the V2 model freeze")
    return binding


def _require_generation_scope_matches_gate(
    config: Any,
    binding: VerifiedBehavioralDifferenceBinding,
) -> None:
    request = binding.candidate_universe_request
    if (
        config.year_start != request.year
        or config.year_end != request.year
        or config.month != request.month
        or config.timezone != request.timezone_name
    ):
        raise ValueError(
            "V2 generation must be restricted to the exact audited month/year/timezone"
        )


def _require_recovery_cache_matches_gate(
    args: argparse.Namespace,
    *,
    ephemeris_path: str | Path,
    binding: VerifiedBehavioralDifferenceBinding,
) -> None:
    if not args.cache_dir:
        raise ValueError("V2 recovery requires the retained audited candidate-cache directory")
    _, audited_cache_value = _require_v2_difference_inputs(args)
    request = binding.candidate_universe_request.to_runtime()
    engine = ExactChartAdapter(ephemeris_path)
    recovery_cache = cache_path(args.cache_dir, request, engine.fingerprint).resolve()
    audited_cache = Path(audited_cache_value).resolve()
    if recovery_cache != audited_cache:
        raise ValueError("V2 recovery cache must be the exact cache bound by the audit")


def _verify_v2_freeze_precedes_manifest(
    model: RuntimeSymbolicModel,
    manifest: Any,
) -> None:
    if (
        isinstance(model, FrozenModelBV2New)
        and model.freeze_receipt.frozen_at_utc > manifest.created_at_utc
    ):
        raise ValueError("V2 model freeze must predate the blind recovery run manifest")


def _generation_timing(
    model: RuntimeSymbolicModel,
    generation_started_at_utc: datetime,
) -> dict[str, datetime]:
    result = {"generation_started_at_utc": generation_started_at_utc}
    if isinstance(model, FrozenModelBV2New):
        if model.freeze_receipt.frozen_at_utc > generation_started_at_utc:
            raise ValueError("V2 model freeze must predate synthetic generation")
        result["model_freeze_created_at_utc"] = model.freeze_receipt.frozen_at_utc
    return result


def _v2_generation_timing(
    model: RuntimeSymbolicModel,
    generation_started_at_utc: datetime,
) -> dict[str, datetime]:
    """Backward-compatible helper retained for focused V2 timing tests."""

    if not isinstance(model, FrozenModelBV2New):
        return {}
    return _generation_timing(model, generation_started_at_utc)


def _paired_arguments(args: argparse.Namespace) -> tuple[str, str] | None:
    plan = getattr(args, "paired_plan", None)
    arm_id = getattr(args, "paired_arm_id", None)
    if (plan is None) != (arm_id is None):
        raise ValueError("--paired-plan and --paired-arm-id must be supplied together")
    return (str(plan), str(arm_id)) if plan is not None else None


def _paired_recovery_arguments(
    args: argparse.Namespace,
) -> tuple[str, str, str, str, str] | None:
    values = (
        getattr(args, "paired_plan", None),
        getattr(args, "paired_public_config", None),
        getattr(args, "paired_generation_receipt", None),
        getattr(args, "paired_generation_binding", None),
        getattr(args, "paired_arm_id", None),
    )
    if not any(value is not None for value in values):
        return None
    if not all(value is not None for value in values):
        raise ValueError(
            "paired recovery requires plan, public config, generation receipt, "
            "generation binding, and arm ID"
        )
    return tuple(str(value) for value in values)  # type: ignore[return-value]


def _verify_generation_pair(
    args: argparse.Namespace,
    *,
    config_path: Path,
    model: RuntimeSymbolicModel,
    secret_seed: int,
    difference_gate: VerifiedBehavioralDifferenceBinding | None,
) -> tuple[PairedExperimentPlan, str] | None:
    paired = _paired_arguments(args)
    if paired is None:
        return None
    plan_path, arm_id = paired
    loaded = load_paired_experiment_plan(plan_path)
    arm_ids = {arm.role: arm.arm_id for arm in loaded.arms}
    audit_binding = difference_gate or loaded.verified_v2_audit
    plan = verify_paired_experiment_plan(
        plan_path,
        paired_experiment_id=loaded.paired_experiment_id,
        verified_v2_audit=audit_binding,
        public_config_path=config_path,
        generation_seed_commitment_sha256=generation_seed_commitment(
            paired_experiment_id=loaded.paired_experiment_id,
            secret_seed=secret_seed,
        ),
        model_a_arm_id=arm_ids["model_a"],
        model_b_v2_arm_id=arm_ids["model_b_v2"],
    )
    verify_generation_seed_commitment(plan, secret_seed=secret_seed)
    arm = plan.arm(arm_id)
    if (
        arm.model_id != model.model_id
        or arm.model_sha256 != model.model_sha256
        or arm.mapping_sha256 != model.mapping_sha256
        or arm.question_bank_sha256 != model.question_bank_sha256
    ):
        raise ValueError("selected runtime model does not match the paired-plan arm")
    if isinstance(model, FrozenModelBV2New):
        if difference_gate is None or difference_gate != plan.verified_v2_audit:
            raise ValueError("V2 generation gate does not match the paired experiment plan")
    elif arm.role != "model_a":
        raise ValueError("only Model A or Model B V2 may use the paired oracle plan")
    return plan, arm_id


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
    model = _load_selected_model(args)
    difference_gate: VerifiedBehavioralDifferenceBinding | None = None
    if isinstance(model, FrozenModelBV2New):
        audit_path, audit_cache_path = _require_v2_difference_inputs(args)
        compiled_path, freeze_path = _require_v2_public_inputs(args)
        assert_no_plaintext_answer_keys_in_paths(
            (
                args.mapping,
                compiled_path,
                freeze_path,
                audit_path,
                audit_cache_path,
                ephemeris_path,
            )
        )
        difference_gate = _verify_v2_difference_gate(
            args,
            model=model,
            ephemeris_path=ephemeris_path,
        )
        _require_generation_scope_matches_gate(config, difference_gate)
    else:
        _reject_inapplicable_v2_difference_inputs(args)

    generation_started_at_utc = datetime.now(UTC)
    if difference_gate is not None and difference_gate.audited_at_utc > generation_started_at_utc:
        raise ValueError("behavioral-difference audit cannot postdate V2 generation")
    generation_timing = _generation_timing(model, generation_started_at_utc)
    seed = _read_secret_seed(args.seed_file)
    paired_generation = _verify_generation_pair(
        args,
        config_path=config_path,
        model=model,
        secret_seed=seed,
        difference_gate=difference_gate,
    )
    generation_commit, generation_dirty = git_revision(ROOT)
    if paired_generation is not None and generation_dirty:
        raise ValueError("paired generation requires a clean committed source tree")
    generation_environment = capture_software_environment()
    run_dir = Path(args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    blind_path = run_dir / "blind_cases.json"
    encrypted_path = run_dir / "answer_key.json.enc"
    leakage_path = run_dir / "leakage_audit.json"
    receipt_path = run_dir / "generation.receipt.json"
    paired_binding_path = run_dir / "paired-generation.binding.json"
    destinations = [blind_path, encrypted_path, leakage_path, receipt_path]
    if paired_generation is not None:
        destinations.append(paired_binding_path)
    for destination in destinations:
        if destination.exists():
            raise FileExistsError(f"refusing to replace experiment artifact: {destination}")

    resolved = config.model_copy(update={"seed": seed, "ephemeris_path": str(ephemeris_path)})
    chart = ExactChartAdapter(ephemeris_path)
    bundle = SyntheticGenerator(chart, model).generate(
        resolved,
        model_b_v2_difference_gate=difference_gate,
    )
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
        "generation_software_commit": generation_commit,
        "generation_software_dirty": generation_dirty,
        "generation_software_environment": generation_environment.model_dump(mode="json"),
        "chart_engine_fingerprint": chart.fingerprint,
        "ephemeris_sha256": {
            file.name: sha256_file(file) for file in declared_ephemeris_files(ephemeris_path)
        },
    }
    if difference_gate is not None:
        receipt["model_b_v2_difference_gate"] = difference_gate.model_dump(mode="json")
    if paired_generation is not None:
        plan, arm_id = paired_generation
        arm = plan.arm(arm_id)
        receipt["paired_experiment"] = {
            "schema_version": "paired-generation-reference-v1",
            "paired_experiment_id": plan.paired_experiment_id,
            "paired_plan_file_sha256": sha256_file(args.paired_plan),
            "paired_plan_semantic_sha256": plan.plan_sha256,
            "arm_id": arm.arm_id,
            "arm_role": arm.role,
            "generation_seed_commitment_sha256": (plan.generation_seed_commitment_sha256),
        }
    receipt.update(generation_timing)
    write_new_canonical_json(receipt_path, receipt)
    if paired_generation is not None:
        _, arm_id = paired_generation
        binding = create_paired_generation_receipt_binding(
            plan_path=args.paired_plan,
            public_config_path=config_path,
            generation_receipt_path=receipt_path,
            arm_id=arm_id,
        )
        write_paired_generation_receipt_binding(binding, paired_binding_path)
    print(f"blind experiment: {blind_path}")
    print(f"blind input sha256: {receipt['blind_input_sha256']}")
    print(f"encrypted answer key: {encrypted_path}")
    print(f"external reveal key status: {receipt['external_reveal_key_status']}")
    if paired_generation is not None:
        print(f"paired generation binding: {paired_binding_path}")
    return 0


def _command_plan_paired_model_a_v2_new(args: argparse.Namespace) -> int:
    """Freeze the public paired design and a commitment to one owner-held seed."""

    config_path = Path(args.config)
    config = load_synthetic_config(config_path)
    if config.seed is not None:
        raise ValueError("paired public config must not contain a generation seed")
    seed = _read_secret_seed(args.seed_file)
    model = _load_selected_model(args)
    if not isinstance(model, FrozenModelBV2New):
        raise TypeError("paired plan requires the frozen Model B V2 runtime")
    gate = _verify_v2_difference_gate(
        args,
        model=model,
        ephemeris_path=args.ephemeris,
    )
    _require_generation_scope_matches_gate(config, gate)
    plan = create_paired_experiment_plan(
        paired_experiment_id=config.experiment_id,
        verified_v2_audit=gate,
        public_config_path=config_path,
        generation_seed_commitment_sha256=generation_seed_commitment(
            paired_experiment_id=config.experiment_id,
            secret_seed=seed,
        ),
        model_a_arm_id="MODEL-A",
        model_b_v2_arm_id="MODEL-B-V2",
    )
    output = write_paired_experiment_plan(plan, args.output)
    print(f"paired experiment plan: {output}")
    print(f"paired plan sha256: {sha256_file(output)}")
    print("generation seed status: owner-held commitment only")
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
    visible_paths: list[str | Path] = [
        ROOT,
        run_dir,
        blind_path,
        args.mapping,
        args.ephemeris,
    ]
    paired_inputs = _paired_recovery_arguments(args)
    if paired_inputs is not None:
        visible_paths.extend(paired_inputs[:4])
    if args.cache_dir:
        visible_paths.append(args.cache_dir)
    if str(args.model) == MODEL_B_ID:
        visible_paths.append(args.model_b_artifact)
    if str(args.model) == MODEL_B_V2_NEW_ID:
        compiled, freeze = _require_v2_public_inputs(args)
        difference_audit, difference_cache = _require_v2_difference_inputs(args)
        visible_paths.extend((compiled, freeze, difference_audit, difference_cache))
    else:
        _reject_inapplicable_v2_difference_inputs(args)
    assert_no_plaintext_answer_keys_in_paths(visible_paths)
    blind = load_json_bytes(blind_path, require_canonical=True)
    if not isinstance(blind, dict):
        raise ValueError("blind file must contain an object")
    model = _load_selected_model(args)
    difference_gate: VerifiedBehavioralDifferenceBinding | None = None
    if isinstance(model, FrozenModelBV2New):
        try:
            expected_gate = VerifiedBehavioralDifferenceBinding.model_validate(
                blind.get("model_b_v2_difference_gate")
            )
        except ValueError as exc:
            raise ValueError("V2 blind input lacks a valid behavioral-difference binding") from exc
        difference_gate = _verify_v2_difference_gate(
            args,
            model=model,
            ephemeris_path=args.ephemeris,
            expected_binding=expected_gate,
        )
        _require_recovery_cache_matches_gate(
            args,
            ephemeris_path=args.ephemeris,
            binding=difference_gate,
        )
    paired_manifest_binding: dict[str, Any] | None = None
    if paired_inputs is not None:
        (
            paired_plan_path,
            paired_config_path,
            paired_generation_receipt_path,
            paired_generation_binding_path,
            paired_arm_id,
        ) = paired_inputs
        paired_plan = load_paired_experiment_plan(paired_plan_path)
        paired_receipt = verify_paired_generation_receipt_binding(
            paired_generation_binding_path,
            plan_path=paired_plan_path,
            public_config_path=paired_config_path,
            generation_receipt_path=paired_generation_receipt_path,
            expected_arm_id=paired_arm_id,
        )
        arm = paired_plan.arm(paired_arm_id)
        if (
            arm.model_id != model.model_id
            or arm.model_sha256 != model.model_sha256
            or arm.mapping_sha256 != model.mapping_sha256
            or arm.question_bank_sha256 != model.question_bank_sha256
        ):
            raise ValueError("recovery runtime does not match the paired arm")
        if paired_receipt.blind_input_sha256 != sha256_file(blind_path):
            raise ValueError("blind input does not match the paired generation binding")
        if isinstance(model, FrozenModelBV2New) and (
            difference_gate is None or difference_gate != paired_plan.verified_v2_audit
        ):
            raise ValueError("V2 recovery gate does not match the paired plan")
        paired_manifest_binding = {
            "schema_version": "paired-recovery-binding-v1",
            "paired_experiment_id": paired_plan.paired_experiment_id,
            "paired_plan_file_sha256": sha256_file(paired_plan_path),
            "paired_plan_semantic_sha256": paired_plan.plan_sha256,
            "paired_generation_receipt_sha256": sha256_file(paired_generation_receipt_path),
            "paired_generation_binding_sha256": sha256_file(paired_generation_binding_path),
            "public_config_file_sha256": sha256_file(paired_config_path),
            "public_config_semantic_sha256": (paired_plan.public_config.semantic_sha256),
            "generation_seed_commitment_sha256": (paired_plan.generation_seed_commitment_sha256),
            "arm_id": arm.arm_id,
            "arm_role": arm.role,
        }
    input_hashes = {
        "blind_cases.json": sha256_file(blind_path),
        "model_a_mapping_library": sha256_file(args.mapping),
    }
    if paired_inputs is not None:
        input_hashes.update(
            {
                "paired_experiment_plan": sha256_file(paired_inputs[0]),
                "paired_public_config": sha256_file(paired_inputs[1]),
                "paired_generation_receipt": sha256_file(paired_inputs[2]),
                "paired_generation_binding": sha256_file(paired_inputs[3]),
            }
        )
    if model.model_id == MODEL_B_ID:
        input_hashes["model_b_artifact"] = sha256_file(args.model_b_artifact)
    if model.model_id == MODEL_B_V2_NEW_ID:
        compiled, freeze = _require_v2_public_inputs(args)
        input_hashes["model_b_v2_compiled_artifact"] = sha256_file(compiled)
        input_hashes["model_b_v2_freeze_receipt"] = sha256_file(freeze)
        assert difference_gate is not None
        input_hashes.update(
            {
                "model_b_v2_difference_audit": difference_gate.audit_file_sha256,
                "model_b_v2_difference_cache": (difference_gate.candidate_cache_file_sha256),
                "model_b_v2_model_semantic": difference_gate.model_b_sha256,
                "model_b_v2_question_bank": difference_gate.question_bank_sha256,
                "model_b_v2_difference_candidate_universe": (
                    difference_gate.candidate_universe_sha256
                ),
            }
        )
    for file in declared_ephemeris_files(args.ephemeris):
        input_hashes[f"ephemeris:{file.name}"] = sha256_file(file)
    public_recovery_seed = int(input_hashes["blind_cases.json"][:16], 16)
    settings = RecoverySettings(
        aggregation=AggregationMode(args.aggregation),
        threshold_rubric_bits=args.threshold,
        workers=args.workers,
    )
    manifest_config: dict[str, Any] = {
        "aggregation": settings.aggregation.value,
        "threshold_rubric_bits": settings.threshold_rubric_bits,
        "workers": settings.workers,
        "cache_policy": "hash-bound exact month universes",
    }
    if difference_gate is not None:
        manifest_config["model_b_v2_difference_gate"] = difference_gate.model_dump(mode="json")
    if paired_manifest_binding is not None:
        manifest_config["paired_experiment"] = paired_manifest_binding
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
        _verify_v2_freeze_precedes_manifest(model, manifest)
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
        _verify_v2_freeze_precedes_manifest(model, manifest)
    if difference_gate is not None and difference_gate.audited_at_utc > manifest.created_at_utc:
        raise ValueError("V2 behavioral-difference audit must predate recovery manifest")
    if not manifest_path.exists():
        write_run_manifest(manifest, manifest_path)
    predictions = recover_blind_file(
        blind_path,
        decoder_root=ROOT,
        model=model,
        ephemeris_path=args.ephemeris,
        cache_dir=args.cache_dir or run_dir / "candidate_cache",
        settings=settings,
        model_b_v2_difference_gate=difference_gate,
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


def _paired_freeze_arms(
    args: argparse.Namespace,
) -> tuple[PairedFreezeArmArtifacts, PairedFreezeArmArtifacts]:
    required = (
        "paired_plan",
        "paired_public_config",
        "paired_model_a_run_dir",
        "paired_model_a_generation_receipt",
        "paired_model_a_generation_binding",
        "paired_model_b_run_dir",
        "paired_model_b_generation_receipt",
        "paired_model_b_generation_binding",
    )
    missing = [name for name in required if not getattr(args, name, None)]
    if missing:
        raise ValueError(
            "paired operation requires the complete two-arm artifact set: "
            + ", ".join(sorted(missing))
        )
    return (
        PairedFreezeArmArtifacts(
            role="model_a",
            arm_id="MODEL-A",
            run_logical_label="model-a",
            run_dir=Path(args.paired_model_a_run_dir),
            generation_receipt_path=Path(args.paired_model_a_generation_receipt),
            generation_binding_path=Path(args.paired_model_a_generation_binding),
            isolation_receipt_path=(
                Path(args.paired_model_a_run_dir) / "keyless-isolation.receipt.json"
            ),
        ),
        PairedFreezeArmArtifacts(
            role="model_b_v2",
            arm_id="MODEL-B-V2",
            run_logical_label="model-b-v2",
            run_dir=Path(args.paired_model_b_run_dir),
            generation_receipt_path=Path(args.paired_model_b_generation_receipt),
            generation_binding_path=Path(args.paired_model_b_generation_binding),
            isolation_receipt_path=(
                Path(args.paired_model_b_run_dir) / "keyless-isolation.receipt.json"
            ),
        ),
    )


def _command_freeze_paired_experiment(args: argparse.Namespace) -> int:
    receipt = create_paired_prediction_freeze_receipt(
        plan_path=args.paired_plan,
        public_config_path=args.paired_public_config,
        arms=_paired_freeze_arms(args),
    )
    output = write_paired_prediction_freeze_receipt(receipt, args.output)
    print(f"paired prediction freeze: {output}")
    print(f"paired freeze sha256: {sha256_file(output)}")
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
    manifest = load_run_manifest(run_dir / "run.manifest.json")
    paired_manifest = (
        manifest.config_payload.get("paired_experiment")
        if manifest.config_payload is not None
        else None
    )
    paired_freeze = None
    paired_arm_id: str | None = None
    paired_freeze_path = getattr(args, "paired_freeze", None)
    if paired_manifest is not None:
        if not isinstance(paired_manifest, dict):
            raise ValueError("run manifest has an invalid paired recovery binding")
        if paired_freeze_path is None:
            raise ValueError("paired recovery cannot be revealed without the two-arm paired freeze")
        paired_freeze = verify_paired_prediction_freeze_receipt(
            paired_freeze_path,
            plan_path=args.paired_plan,
            public_config_path=args.paired_public_config,
            arms=_paired_freeze_arms(args),
        )
        arm_id = str(paired_manifest.get("arm_id"))
        paired_arm_id = arm_id
        expected_run = (
            Path(args.paired_model_a_run_dir)
            if arm_id == "MODEL-A"
            else Path(args.paired_model_b_run_dir)
        )
        if expected_run.resolve() != run_dir.resolve():
            raise ValueError("reveal run directory does not match its paired arm")
    elif paired_freeze_path is not None:
        raise ValueError("unpaired recovery cannot claim a paired prediction freeze")
    encrypted = Path(args.encrypted_key) if args.encrypted_key else run_dir / "answer_key.json.enc"
    key_file = _resolve_key_file(run_dir, args.key_file)
    revealed = reveal_answer_key(
        run_dir,
        encrypted_answer_key_path=encrypted,
        key_path=key_file,
        decoder_root=ROOT,
        paired_prediction_freeze_path=paired_freeze_path,
        paired_plan_path=(args.paired_plan if paired_freeze is not None else None),
        paired_arm_id=paired_arm_id,
        expected_generation_seed_commitment_sha256=(
            paired_freeze.generation_seed_commitment_sha256 if paired_freeze is not None else None
        ),
        reveal_not_before_utc=(paired_freeze.created_at_utc if paired_freeze is not None else None),
    )
    evaluation = evaluate_frozen_run(run_dir, revealed=revealed)
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


def _command_audit_model_b_v2_new_difference(args: argparse.Namespace) -> int:
    """Write the answer-key-free behavioral difference gate, including failures."""

    visible_paths = (
        ROOT,
        args.cache_dir,
        args.ephemeris,
        args.mapping,
        args.model_b_v2_compiled,
        args.model_b_v2_freeze,
        Path(args.output).parent,
    )
    assert_no_plaintext_answer_keys_in_paths(visible_paths)
    engine = ExactChartAdapter(args.ephemeris)
    request = MonthRequest(args.year, args.month, args.timezone)
    cached = load_cached_universe(
        cache_path(args.cache_dir, request, engine.fingerprint),
        request=request,
        engine_fingerprint=engine.fingerprint,
    )
    model_a = load_runtime_model(
        MODEL_A_ID,
        model_a_mapping_path=args.mapping,
    )
    model_b = load_runtime_model(
        MODEL_B_V2_NEW_ID,
        model_a_mapping_path=args.mapping,
        model_b_v2_compiled_path=args.model_b_v2_compiled,
        model_b_v2_freeze_path=args.model_b_v2_freeze,
    )
    if not isinstance(model_a, FrozenSymbolicModel) or not isinstance(model_b, FrozenModelBV2New):
        raise TypeError("behavioral difference audit loaded incompatible model runtimes")
    audit = audit_behavioral_difference(
        cached,
        model_a,
        model_b,
        engine_fingerprint=engine.fingerprint,
    )
    write_new_canonical_json(args.output, audit)
    require_behavioral_difference(audit)
    print(f"behavioral difference audit: {args.output}")
    print(
        json.dumps(
            {
                "status": audit.status,
                "witnesses": len(audit.witnesses),
                "source_favoring_groups": (audit.groups_with_source_favoring_tie_split),
                "adverse_groups": audit.groups_with_adverse_tie_split,
            },
            sort_keys=True,
        )
    )
    return 0


def _command_compile_model_b_v2_new(args: argparse.Namespace) -> int:
    artifact = compile_model_b_v2_new(
        repository_root=args.repository_root,
        preregistration_path=args.preregistration,
        compiled_output_path=args.output,
    )
    print(f"compiled V2 model: {args.output}")
    print(f"compiled semantic sha256: {artifact.sha256()}")
    print(f"compiled file sha256: {sha256_file(args.output)}")
    return 0


def _command_freeze_model_b_v2_new(args: argparse.Namespace) -> int:
    receipt = freeze_model_b_v2_new(
        repository_root=args.repository_root,
        preregistration_path=args.preregistration,
        compiled_artifact_path=args.compiled,
        freeze_receipt_output_path=args.output,
        source_software_commit=args.source_software_commit,
        source_software_tree=args.source_software_tree,
    )
    print(f"V2 model freeze: {args.output}")
    print(f"freeze receipt sha256: {sha256_file(args.output)}")
    print(f"model frozen at UTC: {receipt.frozen_at_utc.isoformat()}")
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


def _command_compare_paired_model_a_v2_new(args: argparse.Namespace) -> int:
    """Verify and compare the two frozen paired runs without key access."""

    arms = _paired_freeze_arms(args)
    for artifacts in arms:
        staged_receipt = artifacts.run_dir / "generation.receipt.json"
        if sha256_file(artifacts.generation_receipt_path) != sha256_file(staged_receipt):
            raise ValueError(
                f"{artifacts.role} supplied generation receipt differs from the "
                "receipt staged by keyless recovery"
            )
    report = compare_model_a_v2_new_run_dirs(
        args.paired_model_a_run_dir,
        args.paired_model_b_run_dir,
        paired_plan_path=args.paired_plan,
        public_config_path=args.paired_public_config,
        model_a_generation_binding_path=args.paired_model_a_generation_binding,
        model_b_generation_binding_path=args.paired_model_b_generation_binding,
        paired_prediction_freeze_path=args.paired_freeze,
    )
    output = write_paired_model_comparison_report(report, args.output)
    print(f"paired Model A/V2 comparison: {output}")
    print(f"paired comparison sha256: {sha256_file(output)}")
    print(
        json.dumps(
            {
                "top_1_a": report.top_1.model_a,
                "top_1_b": report.top_1.model_b,
                "top_3_a": report.top_3.model_a,
                "top_3_b": report.top_3.model_b,
                "top_5_a": report.top_5.model_a,
                "top_5_b": report.top_5.model_b,
                "mrr_a": report.mean_reciprocal_rank.model_a,
                "mrr_b": report.mean_reciprocal_rank.model_b,
                "improved": report.outcomes.improved,
                "unchanged": report.outcomes.unchanged,
                "worsened": report.outcomes.worsened,
                "unevaluable": report.outcomes.unevaluable,
            },
            sort_keys=True,
        )
    )
    return 0


def _add_model_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--model",
        choices=(MODEL_A_ID, MODEL_B_ID, MODEL_B_V2_NEW_ID),
        default=MODEL_A_ID,
    )
    parser.add_argument("--mapping", default=str(DEFAULT_MAPPING))
    parser.add_argument("--model-b-artifact", default=str(DEFAULT_MODEL_B_ARTIFACT))
    parser.add_argument("--model-b-v2-compiled")
    parser.add_argument("--model-b-v2-freeze")
    parser.add_argument("--model-b-v2-difference-audit")
    parser.add_argument("--model-b-v2-difference-cache")


def _add_paired_freeze_arguments(parser: argparse.ArgumentParser, *, required: bool = True) -> None:
    parser.add_argument("--paired-plan", required=required)
    parser.add_argument("--paired-public-config", required=required)
    parser.add_argument("--paired-model-a-run-dir", required=required)
    parser.add_argument("--paired-model-a-generation-receipt", required=required)
    parser.add_argument("--paired-model-a-generation-binding", required=required)
    parser.add_argument("--paired-model-b-run-dir", required=required)
    parser.add_argument("--paired-model-b-generation-receipt", required=required)
    parser.add_argument("--paired-model-b-generation-binding", required=required)


def _add_century_engine_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--ephemeris-path",
        default=str(DEFAULT_EPHEMERIS_DIRECTORY),
    )
    parser.add_argument(
        "--source-manifest",
        default=str(DEFAULT_EPHEMERIS_SOURCE_MANIFEST),
    )


def _add_century_assembly_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--plan", default=str(DEFAULT_CENTURY_PLAN))
    parser.add_argument(
        "--staging-dir",
        default=str(DEFAULT_CENTURY_STAGING_DIRECTORY),
    )
    parser.add_argument("--output", default=str(DEFAULT_CENTURY_CACHE_DIRECTORY))
    parser.add_argument(
        "--cache-locator",
        default=DEFAULT_CENTURY_CACHE_LOCATOR,
    )
    parser.add_argument(
        "--trust-lock",
        default=str(DEFAULT_CENTURY_CACHE_TRUST_LOCK),
    )
    parser.add_argument(
        "--build-evidence-dir",
        default=str(DEFAULT_CENTURY_BUILD_EVIDENCE_DIRECTORY),
    )
    parser.add_argument(
        "--engine-validation",
        default=str(DEFAULT_ENGINE_VALIDATION),
    )
    parser.add_argument(
        "--parity-report",
        default=str(DEFAULT_CENTURY_PARITY_REPORT),
    )
    parser.add_argument(
        "--golden-reference",
        default=str(DEFAULT_SWIEPH_GOLDEN_REFERENCE),
    )
    _add_century_engine_arguments(parser)


def _add_v4_3_cache_only_inputs(parser: argparse.ArgumentParser) -> None:
    """Add verified-artifact inputs only; never expose an astronomy callback."""

    parser.add_argument("--repository-root", default=str(ROOT))
    parser.add_argument("--cache", default=str(DEFAULT_CENTURY_CACHE_DIRECTORY))
    parser.add_argument("--trust-lock", default=str(DEFAULT_CENTURY_CACHE_TRUST_LOCK))
    parser.add_argument("--mapping-library", default=str(DEFAULT_V43_MAPPING_LIBRARY))
    parser.add_argument(
        "--mapping-source-library",
        default=str(DEFAULT_V43_MAPPING_SOURCE_LIBRARY),
    )


def _add_v4_3_run_inputs(parser: argparse.ArgumentParser) -> None:
    _add_v4_3_cache_only_inputs(parser)
    parser.add_argument("--prevalence-plan", default=str(DEFAULT_V43_PREVALENCE_PLAN))
    parser.add_argument(
        "--prevalence-artifact",
        default=str(DEFAULT_V43_PREVALENCE_ARTIFACT),
    )
    parser.add_argument("--responses", default=str(DEFAULT_V43_RESPONSE_ARTIFACT))


def _add_century_finalization_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--plan", default=str(DEFAULT_CENTURY_PLAN))
    parser.add_argument("--output", default=str(DEFAULT_CENTURY_CACHE_DIRECTORY))
    parser.add_argument(
        "--cache-locator",
        default=DEFAULT_CENTURY_CACHE_LOCATOR,
    )
    parser.add_argument(
        "--trust-lock",
        default=str(DEFAULT_CENTURY_CACHE_TRUST_LOCK),
    )
    parser.add_argument(
        "--build-evidence-dir",
        default=str(DEFAULT_CENTURY_BUILD_EVIDENCE_DIRECTORY),
    )
    parser.add_argument(
        "--engine-validation",
        default=str(DEFAULT_ENGINE_VALIDATION),
    )
    parser.add_argument(
        "--parity-report",
        default=str(DEFAULT_CENTURY_PARITY_REPORT),
    )
    parser.add_argument(
        "--golden-reference",
        default=str(DEFAULT_SWIEPH_GOLDEN_REFERENCE),
    )
    _add_century_engine_arguments(parser)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hdmatch",
        description=(
            "Blinded Human Design reverse-matching research harness; symbolic scores "
            "are experimental rubric values, not probabilities."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_engine = subparsers.add_parser(
        "validate-engine",
        help="prove the pinned local Swiss-file engine and reject fallback",
    )
    validate_engine.add_argument(
        "--ephemeris-mode",
        choices=("swiss",),
        default="swiss",
    )
    validate_engine.add_argument("--ephemeris-path", required=True)
    validate_engine.add_argument(
        "--source-manifest",
        default=str(DEFAULT_EPHEMERIS_SOURCE_MANIFEST),
    )
    validate_engine.add_argument("--output")
    validate_engine.set_defaults(handler=_command_validate_engine)

    prepare_century = subparsers.add_parser(
        "prepare-century-cache",
        help="freeze SWIEPH parity evidence and an immutable exact-state build plan",
    )
    prepare_century.add_argument("--repository-root", default=str(ROOT))
    prepare_century.add_argument(
        "--start",
        type=_parse_utc_timestamp,
        default=CANONICAL_CENTURY_START_UTC,
    )
    prepare_century.add_argument(
        "--end-exclusive",
        type=_parse_utc_timestamp,
        default=CANONICAL_CENTURY_END_EXCLUSIVE_UTC,
    )
    _add_century_engine_arguments(prepare_century)
    prepare_century.add_argument(
        "--engine-validation",
        default=str(DEFAULT_ENGINE_VALIDATION),
    )
    prepare_century.add_argument(
        "--golden-reference",
        default=str(DEFAULT_SWIEPH_GOLDEN_REFERENCE),
    )
    prepare_century.add_argument(
        "--reference-source-locator",
        default="tests/golden/fixtures/swieph_phase0_golden_v1.json",
    )
    prepare_century.add_argument(
        "--parity-report",
        default=str(DEFAULT_CENTURY_PARITY_REPORT),
    )
    prepare_century.add_argument("--plan", default=str(DEFAULT_CENTURY_PLAN))
    prepare_century.set_defaults(handler=_command_prepare_century_cache)

    build_century_job = subparsers.add_parser(
        "build-century-cache-job",
        help="build or retain one replay-verifiable job from an immutable plan",
    )
    build_century_job.add_argument("--plan", default=str(DEFAULT_CENTURY_PLAN))
    build_century_job.add_argument("--job-id", required=True)
    build_century_job.add_argument(
        "--staging-dir",
        default=str(DEFAULT_CENTURY_STAGING_DIRECTORY),
    )
    _add_century_engine_arguments(build_century_job)
    build_century_job.set_defaults(handler=_command_build_century_cache_job)

    assemble_century = subparsers.add_parser(
        "assemble-century-cache",
        help="replay, reconcile, publish, lock, and independently verify staged jobs",
    )
    _add_century_assembly_arguments(assemble_century)
    assemble_century.set_defaults(handler=_command_assemble_century_cache)

    build_century = subparsers.add_parser(
        "build-century-cache",
        help="explicitly build missing plan jobs and publish the verified cache",
    )
    _add_century_assembly_arguments(build_century)
    build_century.set_defaults(handler=_command_build_century_cache)

    finalize_century = subparsers.add_parser(
        "finalize-century-cache-publication",
        help=(
            "verify and trust-lock an already-published cache without replaying jobs"
        ),
    )
    _add_century_finalization_arguments(finalize_century)
    finalize_century.set_defaults(
        handler=_command_finalize_century_cache_publication
    )

    verify_century = subparsers.add_parser(
        "verify-century-cache",
        help="independently verify a published cache against its trust lock",
    )
    verify_century.add_argument("cache_directory")
    verify_century.add_argument(
        "--trust-lock",
        default=str(DEFAULT_CENTURY_CACHE_TRUST_LOCK),
    )
    verify_century.set_defaults(handler=_command_verify_century_cache)

    build_prevalence = subparsers.add_parser(
        "build-v4-3-prevalence",
        help="build duration-weighted prevalence from a verified exact-state cache",
    )
    _add_v4_3_cache_only_inputs(build_prevalence)
    build_prevalence.add_argument(
        "--plan-output",
        default=str(DEFAULT_V43_PREVALENCE_PLAN),
    )
    build_prevalence.add_argument(
        "--artifact-output",
        default=str(DEFAULT_V43_PREVALENCE_ARTIFACT),
    )
    build_prevalence.set_defaults(handler=_command_build_v4_3_prevalence)

    verify_prevalence = subparsers.add_parser(
        "verify-v4-3-prevalence",
        help="replay and verify a cache-bound V4.3 prevalence artifact",
    )
    _add_v4_3_cache_only_inputs(verify_prevalence)
    verify_prevalence.add_argument("--plan", default=str(DEFAULT_V43_PREVALENCE_PLAN))
    verify_prevalence.add_argument(
        "--artifact",
        default=str(DEFAULT_V43_PREVALENCE_ARTIFACT),
    )
    verify_prevalence.set_defaults(handler=_command_verify_v4_3_prevalence)

    run_v4_3 = subparsers.add_parser(
        "run-v4-3-cache",
        help="score and rank the complete verified cache without astronomy",
    )
    _add_v4_3_run_inputs(run_v4_3)
    run_v4_3.add_argument("--output", required=True)
    run_v4_3.add_argument("--detail-limit", type=int, default=100)
    run_v4_3.set_defaults(handler=_command_run_v4_3_cache)

    verify_v4_3 = subparsers.add_parser(
        "verify-v4-3-run",
        help="recompute cache-only scores/ranks and verify a Phase-4 run",
    )
    _add_v4_3_run_inputs(verify_v4_3)
    verify_v4_3.add_argument("run_directory")
    verify_v4_3.set_defaults(handler=_command_verify_v4_3_run)

    generate = subparsers.add_parser("generate-blind", help="generate and seal blind cases")
    generate.add_argument("--config", required=True)
    generate.add_argument("--run-dir", required=True)
    generate.add_argument("--ephemeris")
    _add_model_arguments(generate)
    generate.add_argument("--key-file")
    generate.add_argument("--seed-file")
    generate.add_argument("--paired-plan")
    generate.add_argument("--paired-arm-id")
    generate.set_defaults(handler=_command_generate)

    paired_plan = subparsers.add_parser(
        "plan-paired-model-a-v2-new",
        help="freeze a paired Model A/V2 oracle design before either arm is generated",
    )
    paired_plan.add_argument("--config", required=True)
    paired_plan.add_argument("--seed-file", required=True)
    paired_plan.add_argument("--ephemeris", required=True)
    paired_plan.add_argument("--output", required=True)
    paired_plan.add_argument("--mapping", default=str(DEFAULT_MAPPING))
    paired_plan.add_argument("--model-b-artifact", default=str(DEFAULT_MODEL_B_ARTIFACT))
    paired_plan.add_argument("--model-b-v2-compiled", required=True)
    paired_plan.add_argument("--model-b-v2-freeze", required=True)
    paired_plan.add_argument("--model-b-v2-difference-audit", required=True)
    paired_plan.add_argument("--model-b-v2-difference-cache", required=True)
    paired_plan.set_defaults(
        handler=_command_plan_paired_model_a_v2_new,
        model=MODEL_B_V2_NEW_ID,
    )

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
    recover.add_argument("--paired-plan")
    recover.add_argument("--paired-public-config")
    recover.add_argument("--paired-generation-receipt")
    recover.add_argument("--paired-generation-binding")
    recover.add_argument("--paired-arm-id")
    recover.set_defaults(handler=_command_recover)

    freeze = subparsers.add_parser("freeze", help="cryptographically freeze predictions")
    freeze.add_argument("--run-dir", required=True)
    freeze.set_defaults(handler=_command_freeze)

    paired_freeze = subparsers.add_parser(
        "freeze-paired-model-a-v2-new",
        help="freeze both paired prediction chains before either answer-key reveal",
    )
    _add_paired_freeze_arguments(paired_freeze)
    paired_freeze.add_argument("--output", required=True)
    paired_freeze.set_defaults(handler=_command_freeze_paired_experiment)

    reveal = subparsers.add_parser(
        "reveal-evaluate", help="reveal only after freeze and write evaluation reports"
    )
    reveal.add_argument("--run-dir", required=True)
    reveal.add_argument("--encrypted-key")
    reveal.add_argument("--key-file")
    reveal.add_argument("--paired-freeze")
    _add_paired_freeze_arguments(reveal, required=False)
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

    difference = subparsers.add_parser(
        "audit-model-b-v2-new-difference",
        help="prove prospective V2 changes non-unknown responses and splits a Model A tie",
    )
    difference.add_argument("--cache-dir", required=True)
    difference.add_argument("--ephemeris", required=True)
    difference.add_argument("--output", required=True)
    difference.add_argument("--year", type=int, required=True)
    difference.add_argument("--month", type=int, choices=range(1, 13), required=True)
    difference.add_argument("--timezone", default="UTC")
    difference.add_argument("--mapping", default=str(DEFAULT_MAPPING))
    difference.add_argument("--model-b-v2-compiled", required=True)
    difference.add_argument("--model-b-v2-freeze", required=True)
    difference.set_defaults(handler=_command_audit_model_b_v2_new_difference)

    compile_v2 = subparsers.add_parser(
        "compile-model-b-v2-new",
        help="deterministically compile the prospective V2 preregistration",
    )
    compile_v2.add_argument("--repository-root", default=str(ROOT))
    compile_v2.add_argument("--preregistration", required=True)
    compile_v2.add_argument("--output", required=True)
    compile_v2.set_defaults(handler=_command_compile_model_b_v2_new)

    freeze_v2 = subparsers.add_parser(
        "freeze-model-b-v2-new",
        help="freeze the prospective V2 compiled model before generation",
    )
    freeze_v2.add_argument("--repository-root", default=str(ROOT))
    freeze_v2.add_argument("--preregistration", required=True)
    freeze_v2.add_argument("--compiled", required=True)
    freeze_v2.add_argument("--output", required=True)
    freeze_v2.add_argument("--source-software-commit", required=True)
    freeze_v2.add_argument("--source-software-tree", required=True)
    freeze_v2.set_defaults(handler=_command_freeze_model_b_v2_new)

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

    paired_comparison = subparsers.add_parser(
        "compare-paired-model-a-v2-new",
        help="verify and compare a small paired Model A/V2 oracle experiment",
    )
    _add_paired_freeze_arguments(paired_comparison)
    paired_comparison.add_argument("--paired-freeze", required=True)
    paired_comparison.add_argument("--output", required=True)
    paired_comparison.set_defaults(handler=_command_compare_paired_model_a_v2_new)
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
