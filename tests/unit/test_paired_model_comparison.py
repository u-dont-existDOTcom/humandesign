from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from hdmatch.evaluation.behavioral_difference import VerifiedBehavioralDifferenceBinding
from hdmatch.evaluation.metrics import aggregate_rank_metrics, evaluate_ranked_case
from hdmatch.evaluation.paired_model_comparison import (
    PairedModelComparisonError,
    compare_model_a_v2_new_run_dirs,
    load_verified_public_run,
    write_paired_model_comparison_report,
)
from hdmatch.evaluation.report import EvaluationReport
from hdmatch.experiments.answer_key_commitments import (
    generation_seed_commitment,
    revealed_local_date_set_hash,
    revealed_target_set_hash,
)
from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    load_json_bytes,
    sha256_bytes,
    sha256_file,
    sha256_json,
    write_new_canonical_json,
)
from hdmatch.experiments.freeze import FreezeRecord
from hdmatch.experiments.manifest import RunManifest, SoftwareEnvironment
from hdmatch.experiments.paired import (
    create_paired_experiment_plan,
    create_paired_generation_receipt_binding,
    write_paired_experiment_plan,
    write_paired_generation_receipt_binding,
)
from hdmatch.experiments.paired_freeze import (
    PairedFreezeArmArtifacts,
    PairedPredictionFreezeError,
    create_paired_prediction_freeze_receipt,
    write_paired_prediction_freeze_receipt,
)
from hdmatch.experiments.reveal import RevealRecord
from hdmatch.runtime.symbolic_adapter import MODEL_A_ID, MODEL_B_V2_NEW_ID
from hdmatch.synthetic.noise import NoiseTier, noise_parameters_payload
from hdmatch.synthetic.sealing import SealingMetadata, generate_key_file, seal_answer_key

_EPHEMERIS_HASH = "a" * 64
_CACHE_HASH = "b" * 64
_QUESTION_HASH = "e" * 64
_BASE_MAPPING_HASH = "f" * 64
_MODEL_A_HASH = "2" * 64
_MODEL_B_HASH = "3" * 64
_MODEL_B_MAPPING_HASH = "4" * 64
_AUDIT_HASH = "5" * 64
_FREEZE_ARTIFACT_HASH = "6" * 64
_SECRET_SEED = 1_234_567

_AUDITED_AT = datetime(2026, 8, 22, 0, 0, tzinfo=UTC)
_PLANNED_AT = datetime(2026, 8, 22, 0, 0, 30, tzinfo=UTC)
_GENERATED_AT = datetime(2026, 8, 22, 0, 1, tzinfo=UTC)
_MANIFEST_AT = datetime(2026, 8, 22, 0, 2, tzinfo=UTC)
_ISOLATION_AT = datetime(2026, 8, 22, 0, 3, tzinfo=UTC)
_FREEZE_AT = datetime(2026, 8, 22, 0, 4, tzinfo=UTC)
_PAIR_FREEZE_AT = datetime(2026, 8, 22, 0, 4, 30, tzinfo=UTC)
_REVEAL_AT = datetime(2026, 8, 22, 0, 5, tzinfo=UTC)
_EVALUATION_AT = datetime(2026, 8, 22, 0, 6, tzinfo=UTC)


@dataclass(frozen=True)
class PairPaths:
    model_a: Path
    model_b: Path
    plan: Path
    config: Path
    model_a_binding: Path
    model_b_binding: Path
    paired_freeze: Path

    def compare_kwargs(self) -> dict[str, Path]:
        return {
            "paired_plan_path": self.plan,
            "public_config_path": self.config,
            "model_a_generation_binding_path": self.model_a_binding,
            "model_b_generation_binding_path": self.model_b_binding,
            "paired_prediction_freeze_path": self.paired_freeze,
        }


def _difference_gate() -> dict[str, Any]:
    return {
        "schema_version": "model-b-v2-new-verified-difference-binding-v1",
        "audit_file_sha256": _AUDIT_HASH,
        "audited_at_utc": _AUDITED_AT.isoformat().replace("+00:00", "Z"),
        "model_a_sha256": _MODEL_A_HASH,
        "model_a_mapping_sha256": _BASE_MAPPING_HASH,
        "model_b_compiled_file_sha256": _MODEL_B_MAPPING_HASH,
        "model_b_freeze_receipt_file_sha256": _FREEZE_ARTIFACT_HASH,
        "model_b_sha256": _MODEL_B_HASH,
        "question_bank_sha256": _QUESTION_HASH,
        "candidate_cache_file_sha256": _CACHE_HASH,
        "candidate_engine_fingerprint": "7" * 64,
        "candidate_universe_request": {
            "year": 2000,
            "month": 1,
            "timezone_name": "UTC",
        },
        "candidate_universe_sha256": "8" * 64,
        "candidate_state_count": 3,
    }


def _ranking(
    true_date: str,
    *,
    month: int,
    rank: int = 1,
    all_tied: bool = False,
) -> list[dict[str, object]]:
    count = calendar.monthrange(2000, month)[1]
    dates = tuple(f"2000-{month:02d}-{day:02d}" for day in range(1, count + 1))
    remaining = tuple(item for item in dates if item != true_date)
    ordered = (*remaining[: rank - 1], true_date, *remaining[rank - 1 :])
    scores = (
        {item: 0.0 for item in ordered}
        if all_tied
        else {item: float(count - index) for index, item in enumerate(ordered)}
    )
    return [{"local_date": local_date, "date_score": scores[local_date]} for local_date in ordered]


def _prediction_case(
    case_id: str,
    true_date: str,
    *,
    month: int,
    is_v2: bool,
    second_case: bool,
) -> dict[str, Any]:
    if is_v2:
        final = _ranking(true_date, month=month, rank=1 if second_case else 2)
        ablated = _ranking(true_date, month=month, rank=3)
        cluster_id = "DETAILED"
    else:
        final = _ranking(
            true_date,
            month=month,
            rank=3,
            all_tied=second_case,
        )
        ablated = _ranking(true_date, month=month, rank=4)
        cluster_id = "CORE"
    return {
        "case_id": case_id,
        "recovery_status": "completed",
        "ranked_dates": final,
        "aggregation_variants": {"best_state": {"ranked_dates": final}},
        "zero_cluster": {"ranked_dates": _ranking(true_date, month=month, all_tied=True)},
        "random_restoration": [{"cluster_count": 1, "ranked_dates": final}],
        "active_restoration": [{"cluster_count": 1, "ranked_dates": final}],
        "leave_one_cluster_out": [{"cluster_id": cluster_id, "ranked_dates": ablated}],
        "unresolved_mapping_ids": [],
        "prevalence_source": "duration-weighted declared candidate universe",
    }


def _write_config(path: Path) -> None:
    path.write_text(
        "\n".join(
            (
                "experiment_id: PAIRED-75",
                "seed: null",
                "case_count: 2",
                "tier: oracle",
                "universe: known_month",
                "year_start: 2000",
                "year_end: 2000",
                "month: 1",
                "timezone: UTC",
                "birthplace: Synthetic UTC",
                "aggregation: duration_weighted_evidence",
                "threshold_rubric_bits: 0.0",
                "ephemeris_path: null",
                "",
            )
        ),
        encoding="utf-8",
    )


def _write_run(
    root: Path,
    model_id: str,
    *,
    public_config_sha256: str,
    secret_seed: int = _SECRET_SEED,
    target_variant: str = "shared",
    month: int = 1,
    ephemeris_hash: str = _EPHEMERIS_HASH,
    cache_hash: str = _CACHE_HASH,
    workers: int = 1,
) -> Path:
    is_v2 = model_id == MODEL_B_V2_NEW_ID
    label = "model-b" if is_v2 else "model-a"
    run_dir = root / label
    run_dir.mkdir()
    model_sha256 = _MODEL_B_HASH if is_v2 else _MODEL_A_HASH
    mapping_sha256 = _MODEL_B_MAPPING_HASH if is_v2 else _BASE_MAPPING_HASH
    capabilities: dict[str, Any] = (
        {
            "behavioral_scoring": "model-a-plus-prospective-detailed-v2-new",
            "detailed_behavioral_mappings": "scoreable",
            "assignment_scope": "discovery_only",
            "scientific_claim": "engineering-discovery-only-not-holdout-validation",
            "holdout": "frozen-withheld",
            "active_detailed_rule_count": 11,
            "withheld_holdout_rule_count": 5,
            "unresolved_detailed_observation_count": 6,
            "freeze_receipt_sha256": _FREEZE_ARTIFACT_HASH,
        }
        if is_v2
        else {
            "behavioral_scoring": "frozen-core",
            "detailed_behavioral_mappings": "not-applicable",
        }
    )
    gate = _difference_gate()
    true_dates = (f"2000-{month:02d}-01", f"2000-{month:02d}-02")
    case_ids = ("CASE-0001", "CASE-0002")
    blind: dict[str, Any] = {
        "schema_version": "blind-synthetic-v1",
        "generator": "frozen-chart-to-response-model",
        "experiment_id": "PAIRED-75",
        "model_id": model_id,
        "model_sha256": model_sha256,
        "question_bank_sha256": _QUESTION_HASH,
        "mapping_sha256": mapping_sha256,
        "model_capabilities": capabilities,
        "noise_tier": "oracle",
        "noise_parameters": noise_parameters_payload(NoiseTier.ORACLE),
        "candidate_universe": "known_month",
        "cases": [
            {
                "case_id": case_id,
                "candidate_universe": "known_month",
                "known_birth_year": 2000,
                "known_birth_month": month,
                "birthplace": "Synthetic UTC",
                "iana_timezone": "UTC",
                "responses": [],
            }
            for case_id in case_ids
        ],
    }
    if is_v2:
        blind["model_b_v2_difference_gate"] = gate
    blind_path = run_dir / "blind_cases.json"
    write_new_canonical_json(blind_path, blind)
    blind_sha256 = sha256_file(blind_path)

    recovery_config: dict[str, Any] = {
        "aggregation": "duration_weighted_evidence",
        "threshold_rubric_bits": 0.0,
        "workers": workers,
        "cache_policy": "hash-bound exact month universes",
    }
    if is_v2:
        recovery_config["model_b_v2_difference_gate"] = gate
    manifest_inputs = {
        "blind_cases.json": blind_sha256,
        "model_a_mapping_library": _BASE_MAPPING_HASH,
        "ephemeris:sepl_18.se1": ephemeris_hash,
    }
    if is_v2:
        manifest_inputs.update(
            {
                "model_b_v2_compiled_artifact": _MODEL_B_MAPPING_HASH,
                "model_b_v2_freeze_receipt": _FREEZE_ARTIFACT_HASH,
                "model_b_v2_difference_audit": _AUDIT_HASH,
                "model_b_v2_difference_cache": _CACHE_HASH,
                "model_b_v2_model_semantic": _MODEL_B_HASH,
                "model_b_v2_question_bank": _QUESTION_HASH,
                "model_b_v2_difference_candidate_universe": "8" * 64,
            }
        )
    environment = SoftwareEnvironment(
        python_version="3.12.3",
        python_implementation="CPython",
        operating_system="Linux",
        machine="x86_64",
        packages={"hdmatch": "0.1.0", "tzdata": "2026.1"},
    )
    manifest = RunManifest(
        experiment_id="PAIRED-75",
        created_at_utc=_MANIFEST_AT,
        seed=int(blind_sha256[:16], 16),
        software_commit="9" * 40,
        software_dirty=False,
        software_environment=environment,
        candidate_universe="known_month",
        aggregation_rule="duration_weighted_evidence",
        model_id=model_id,
        input_hashes=manifest_inputs,
        config_payload=recovery_config,
        config_sha256=sha256_json(recovery_config),
        declared_outputs=("predictions.json", "prediction.freeze.json"),
    )
    manifest_path = run_dir / "run.manifest.json"
    write_new_canonical_json(manifest_path, manifest)

    prediction_cases = [
        _prediction_case(
            case_id,
            true_date,
            month=month,
            is_v2=is_v2,
            second_case=index == 1,
        )
        for index, (case_id, true_date) in enumerate(zip(case_ids, true_dates, strict=True))
    ]
    predictions: dict[str, Any] = {
        "schema_version": "predictions-v1",
        "experiment_id": "PAIRED-75",
        "model_id": model_id,
        "blind_input_sha256": blind_sha256,
        "model_sha256": model_sha256,
        "question_bank_sha256": _QUESTION_HASH,
        "mapping_sha256": mapping_sha256,
        "aggregation_rule": "duration_weighted_evidence",
        "model_capabilities": capabilities,
        "candidate_cache_sha256": {"month-2000-01-UTC-engine.json": cache_hash},
        "predictions": prediction_cases,
    }
    if is_v2:
        predictions["model_b_v2_difference_gate"] = gate
    predictions_path = run_dir / "predictions.json"
    write_new_canonical_json(predictions_path, predictions)

    freeze = FreezeRecord(
        experiment_id="PAIRED-75",
        prediction_file="predictions.json",
        prediction_sha256=sha256_file(predictions_path),
        prediction_size_bytes=predictions_path.stat().st_size,
        blind_input_sha256=blind_sha256,
        model_sha256=model_sha256,
        question_bank_sha256=_QUESTION_HASH,
        mapping_sha256=mapping_sha256,
        run_manifest_sha256=sha256_file(manifest_path),
        software_commit="9" * 40,
        software_dirty=False,
        software_versions={
            "python": "3.12.3",
            "hdmatch": "0.1.0",
            "tzdata": "2026.1",
        },
        created_at_utc=_FREEZE_AT,
    )
    freeze_path = run_dir / "prediction.freeze.json"
    write_new_canonical_json(freeze_path, freeze)

    answer_key = {
        "schema_version": "answer-key-v1",
        "experiment_id": "PAIRED-75",
        "blind_input_sha256": blind_sha256,
        "generation_seed": secret_seed,
        "cases": [
            {
                "case_id": case_id,
                "true_local_date": true_date,
                "true_utc": f"{true_date}T12:00:00Z",
                "true_chart_features_hash": sha256_bytes(f"{target_variant}-{case_id}".encode()),
            }
            for case_id, true_date in zip(case_ids, true_dates, strict=True)
        ],
    }
    keyed_cases = {item["case_id"]: item for item in answer_key["cases"]}
    target_hash = revealed_target_set_hash(keyed_cases)
    assert target_hash is not None
    local_date_hash = revealed_local_date_set_hash(keyed_cases)
    seed_hash = generation_seed_commitment(secret_seed)
    key_path = root / f".{label}.key"
    generate_key_file(key_path, decoder_root=run_dir)
    envelope_path = run_dir / "answer_key.json.enc"
    seal_answer_key(
        answer_key,
        encrypted_path=envelope_path,
        key_path=key_path,
        metadata=SealingMetadata(
            experiment_id="PAIRED-75",
            blind_input_sha256=blind_sha256,
            model_sha256=model_sha256,
            question_bank_sha256=_QUESTION_HASH,
            mapping_sha256=mapping_sha256,
        ),
        decoder_root=run_dir,
    )
    answer_payload_sha256 = sha256_bytes(canonical_json_bytes(answer_key))
    reveal = RevealRecord(
        schema_version="answer-key-reveal-v3",
        experiment_id="PAIRED-75",
        blind_input_sha256=blind_sha256,
        model_sha256=model_sha256,
        question_bank_sha256=_QUESTION_HASH,
        mapping_sha256=mapping_sha256,
        run_manifest_sha256=sha256_file(manifest_path),
        prediction_sha256=sha256_file(predictions_path),
        freeze_record_sha256=sha256_file(freeze_path),
        encrypted_answer_key_sha256=sha256_file(envelope_path),
        encrypted_answer_key_file="answer_key.json.enc",
        answer_key_payload_sha256=answer_payload_sha256,
        revealed_target_set_sha256=target_hash,
        revealed_local_date_set_sha256=local_date_hash,
        generation_seed_commitment_sha256=seed_hash,
        revealed_at_utc=_REVEAL_AT,
    )
    reveal_path = run_dir / "answer-key.reveal.json"
    write_new_canonical_json(reveal_path, reveal)

    generation: dict[str, Any] = {
        "schema_version": "generation-receipt-v1",
        "experiment_id": "PAIRED-75",
        "model_id": model_id,
        "blind_input_sha256": blind_sha256,
        "encrypted_answer_key_sha256": sha256_file(envelope_path),
        "public_config_sha256": public_config_sha256,
        "model_sha256": model_sha256,
        "question_bank_sha256": _QUESTION_HASH,
        "mapping_sha256": mapping_sha256,
        "case_count": 2,
        "seed_status": "sealed-in-answer-key-only",
        "external_reveal_key_status": "owner-only-key-ready-path-withheld",
        "claim_boundary": "synthetic-engineering-validation-only",
        "generation_started_at_utc": _GENERATED_AT.isoformat().replace("+00:00", "Z"),
    }
    if is_v2:
        generation["model_b_v2_difference_gate"] = gate
        generation["model_freeze_created_at_utc"] = "2026-08-21T00:00:00Z"
    write_new_canonical_json(run_dir / "generation.receipt.json", generation)

    isolation: dict[str, Any] = {
        "schema_version": "keyless-recovery-isolation-receipt-v1",
        "isolation_runtime": {
            "name": "bubblewrap",
            "version": "bubblewrap 0.9.0",
            "executable_sha256": "c" * 64,
        },
        "runtime_controls": {
            "network_namespace": "unshared",
            "user_namespace": "unshared-uid-gid-65534",
            "nested_user_namespaces": "disabled",
            "capabilities": "all-dropped",
            "environment": "cleared-allowlist-only",
            "tracked_decoder_source": "read-only-individual-files",
            "python_environment": "read-only-dedicated-mount",
            "public_inputs": "read-only-individual-files",
            "run_output": "single-read-write-mount",
            "evaluator_secret_mounts": "absent",
            "reveal_or_key_cli_surface": False,
        },
        "mount_contract": {
            "tracked_decoder_source": "read-only",
            "python_environment": "read-only",
            "blind_input": "read-only-single-file",
            "mapping_artifact": "read-only-single-file",
            "question_bank_artifact": "read-only-single-file",
            "model_b_artifact": "absent",
            "model_b_v2_compiled_artifact": ("read-only-single-file" if is_v2 else "absent"),
            "model_b_v2_freeze_receipt": ("read-only-single-file" if is_v2 else "absent"),
            "model_b_v2_difference_audit": ("read-only-single-file" if is_v2 else "absent"),
            "model_b_v2_difference_cache": ("read-only-single-file" if is_v2 else "absent"),
            "ephemeris": "read-only-declared-se1-files",
            "candidate_cache": "read-only-declared-month-files",
            "run_output": "read-write-single-directory",
            "host_parent_directories": "absent",
            "evaluator_key_plaintext_envelope": "absent",
        },
        "command_contract": {
            "entrypoint": "python -m hdmatch.cli recover",
            "workers": workers,
            "aggregation": "duration_weighted_evidence",
            "threshold_rubric_bits": 0.0,
            "exit_status": 0,
            "key_or_reveal_arguments": False,
        },
        "software_commit": "9" * 40,
        "software_tree": "0" * 40,
        "model_id": model_id,
        "blind_input_sha256": blind_sha256,
        "mapping_sha256": _BASE_MAPPING_HASH,
        "question_bank_sha256": _QUESTION_HASH,
        "model_b_artifact_sha256": None,
        "model_b_v2_compiled_sha256": _MODEL_B_MAPPING_HASH if is_v2 else None,
        "model_b_v2_freeze_sha256": _FREEZE_ARTIFACT_HASH if is_v2 else None,
        "model_b_v2_difference_audit_sha256": _AUDIT_HASH if is_v2 else None,
        "model_b_v2_difference_cache_sha256": _CACHE_HASH if is_v2 else None,
        "model_b_v2_difference_gate": gate if is_v2 else None,
        "ephemeris_sha256": {"sepl_18.se1": ephemeris_hash},
        "candidate_cache_sha256": {"month-2000-01-UTC-engine.json": cache_hash},
        "run_manifest_sha256": sha256_file(manifest_path),
        "prediction_sha256": sha256_file(predictions_path),
        "created_at_utc": _ISOLATION_AT.isoformat().replace("+00:00", "Z"),
        "claim_boundary": (
            "OS-isolated synthetic engineering recovery only; this does not validate "
            "Human Design in humans"
        ),
    }
    write_new_canonical_json(run_dir / "keyless-isolation.receipt.json", isolation)

    # These stored metrics are deliberately unrelated to the frozen rankings.  The
    # paired comparator may use their authenticated case/date identities, but must
    # recompute all reported statistics from predictions.json.
    stored_cases = tuple(
        evaluate_ranked_case(
            case_id=case_id,
            candidates=_ranking(true_date, month=month, rank=31),
            true_candidate_id=true_date,
        )
        for case_id, true_date in zip(case_ids, true_dates, strict=True)
    )
    evaluation = EvaluationReport(
        experiment_id="PAIRED-75",
        created_at_utc=_EVALUATION_AT,
        prediction_sha256=sha256_file(predictions_path),
        freeze_sha256=sha256_file(freeze_path),
        reveal_sha256=sha256_file(reveal_path),
        run_manifest_sha256=sha256_file(manifest_path),
        encrypted_answer_key_file="answer_key.json.enc",
        encrypted_answer_key_sha256=sha256_file(envelope_path),
        answer_key_payload_sha256=answer_payload_sha256,
        blind_input_sha256=blind_sha256,
        model_sha256=model_sha256,
        question_bank_sha256=_QUESTION_HASH,
        mapping_sha256=mapping_sha256,
        revealed_target_set_sha256=target_hash,
        revealed_local_date_set_sha256=local_date_hash,
        generation_seed_commitment_sha256=seed_hash,
        aggregate=aggregate_rank_metrics(stored_cases, total_case_count=2),
        cases=stored_cases,
        failures=(),
        failure_counts={},
        restoration_curves=(),
        leave_one_cluster_out=(),
    )
    write_new_canonical_json(run_dir / "evaluation.json", evaluation)
    return run_dir


def _bind_recovery_arm_to_pair(
    *,
    run_dir: Path,
    plan: Any,
    plan_path: Path,
    config_path: Path,
    generation_binding_path: Path,
    arm_id: str,
    run_label: str,
) -> PairedFreezeArmArtifacts:
    arm = plan.arm(arm_id)
    generation_path = run_dir / "generation.receipt.json"
    manifest_path = run_dir / "run.manifest.json"
    manifest = RunManifest.model_validate(load_json_bytes(manifest_path, require_canonical=True))
    paired_binding = {
        "schema_version": "paired-recovery-binding-v1",
        "paired_experiment_id": plan.paired_experiment_id,
        "paired_plan_file_sha256": sha256_file(plan_path),
        "paired_plan_semantic_sha256": plan.plan_sha256,
        "paired_generation_receipt_sha256": sha256_file(generation_path),
        "paired_generation_binding_sha256": sha256_file(generation_binding_path),
        "public_config_file_sha256": sha256_file(config_path),
        "public_config_semantic_sha256": plan.public_config.semantic_sha256,
        "generation_seed_commitment_sha256": plan.generation_seed_commitment_sha256,
        "arm_id": arm.arm_id,
        "arm_role": arm.role,
    }
    config_payload = dict(manifest.config_payload or {})
    config_payload["paired_experiment"] = paired_binding
    input_hashes = dict(manifest.input_hashes)
    input_hashes.update(
        {
            "paired_experiment_plan": sha256_file(plan_path),
            "paired_public_config": sha256_file(config_path),
            "paired_generation_receipt": sha256_file(generation_path),
            "paired_generation_binding": sha256_file(generation_binding_path),
        }
    )
    _rewrite_canonical(
        manifest_path,
        manifest.model_copy(
            update={
                "input_hashes": input_hashes,
                "config_payload": config_payload,
                "config_sha256": sha256_json(config_payload),
            }
        ),
    )

    isolation_path = run_dir / "keyless-isolation.receipt.json"
    isolation = load_json_bytes(isolation_path, require_canonical=True)
    isolation["run_manifest_sha256"] = sha256_file(manifest_path)
    isolation["paired_plan_sha256"] = sha256_file(plan_path)
    isolation["paired_public_config_sha256"] = sha256_file(config_path)
    isolation["paired_generation_receipt_sha256"] = sha256_file(generation_path)
    isolation["paired_generation_binding_sha256"] = sha256_file(generation_binding_path)
    isolation["paired_arm_id"] = arm.arm_id
    for name in (
        "paired_plan",
        "paired_public_config",
        "paired_generation_receipt",
        "paired_generation_binding",
    ):
        isolation["mount_contract"][name] = "read-only-single-file"
    _rewrite_canonical(isolation_path, isolation)

    freeze_path = run_dir / "prediction.freeze.json"
    freeze = FreezeRecord.model_validate(load_json_bytes(freeze_path, require_canonical=True))
    _rewrite_canonical(
        freeze_path,
        freeze.model_copy(update={"run_manifest_sha256": sha256_file(manifest_path)}),
    )
    return PairedFreezeArmArtifacts(
        role=arm.role,
        arm_id=arm.arm_id,
        run_logical_label=run_label,
        run_dir=run_dir,
        generation_receipt_path=generation_path,
        generation_binding_path=generation_binding_path,
        isolation_receipt_path=isolation_path,
    )


def _bind_reveal_to_pair(
    *,
    run_dir: Path,
    plan_path: Path,
    paired_freeze_path: Path,
    arm_id: str,
) -> None:
    manifest_path = run_dir / "run.manifest.json"
    freeze_path = run_dir / "prediction.freeze.json"
    reveal_path = run_dir / "answer-key.reveal.json"
    reveal = load_json_bytes(reveal_path, require_canonical=True)
    reveal["run_manifest_sha256"] = sha256_file(manifest_path)
    reveal["freeze_record_sha256"] = sha256_file(freeze_path)
    reveal["paired_prediction_freeze_sha256"] = sha256_file(paired_freeze_path)
    reveal["paired_plan_sha256"] = sha256_file(plan_path)
    reveal["paired_arm_id"] = arm_id
    _rewrite_canonical(reveal_path, reveal)

    evaluation_path = run_dir / "evaluation.json"
    evaluation = load_json_bytes(evaluation_path, require_canonical=True)
    evaluation["run_manifest_sha256"] = sha256_file(manifest_path)
    evaluation["freeze_sha256"] = sha256_file(freeze_path)
    evaluation["reveal_sha256"] = sha256_file(reveal_path)
    _rewrite_canonical(evaluation_path, evaluation)


def _write_pair(tmp_path: Path, **model_b_overrides: Any) -> PairPaths:
    config_path = tmp_path / "paired.yaml"
    _write_config(config_path)
    gate = VerifiedBehavioralDifferenceBinding.model_validate(_difference_gate())
    plan = create_paired_experiment_plan(
        paired_experiment_id="PAIRED-75",
        verified_v2_audit=gate,
        public_config_path=config_path,
        generation_seed_commitment_sha256=generation_seed_commitment(_SECRET_SEED),
        model_a_arm_id="ARM-MODEL-A",
        model_b_v2_arm_id="ARM-MODEL-B-V2",
        planned_at_utc=_PLANNED_AT,
    )
    plan_path = tmp_path / "paired.plan.json"
    write_paired_experiment_plan(plan, plan_path)
    model_a = _write_run(
        tmp_path,
        MODEL_A_ID,
        public_config_sha256=sha256_file(config_path),
    )
    model_b = _write_run(
        tmp_path,
        MODEL_B_V2_NEW_ID,
        public_config_sha256=sha256_file(config_path),
        **model_b_overrides,
    )
    for run_dir, arm_id in (
        (model_a, "ARM-MODEL-A"),
        (model_b, "ARM-MODEL-B-V2"),
    ):
        receipt_path = run_dir / "generation.receipt.json"
        receipt = load_json_bytes(receipt_path, require_canonical=True)
        manifest = RunManifest.model_validate(
            load_json_bytes(run_dir / "run.manifest.json", require_canonical=True)
        )
        arm = plan.arm(arm_id)
        receipt["paired_experiment"] = {
            "schema_version": "paired-generation-reference-v1",
            "paired_experiment_id": plan.paired_experiment_id,
            "paired_plan_file_sha256": plan.plan_sha256,
            "paired_plan_semantic_sha256": plan.plan_sha256,
            "arm_id": arm.arm_id,
            "arm_role": arm.role,
            "generation_seed_commitment_sha256": (plan.generation_seed_commitment_sha256),
        }
        receipt["generation_software_commit"] = manifest.software_commit
        receipt["generation_software_dirty"] = False
        receipt["generation_software_environment"] = manifest.software_environment.model_dump(
            mode="json"
        )
        receipt["chart_engine_fingerprint"] = plan.verified_v2_audit.candidate_engine_fingerprint
        isolation = load_json_bytes(
            run_dir / "keyless-isolation.receipt.json", require_canonical=True
        )
        receipt["ephemeris_sha256"] = isolation["ephemeris_sha256"]
        _rewrite_canonical(receipt_path, receipt)
    model_a_binding = tmp_path / "model-a.generation-binding.json"
    model_b_binding = tmp_path / "model-b.generation-binding.json"
    write_paired_generation_receipt_binding(
        create_paired_generation_receipt_binding(
            plan_path=plan_path,
            public_config_path=config_path,
            generation_receipt_path=model_a / "generation.receipt.json",
            arm_id="ARM-MODEL-A",
            bound_at_utc=_GENERATED_AT,
        ),
        model_a_binding,
    )
    write_paired_generation_receipt_binding(
        create_paired_generation_receipt_binding(
            plan_path=plan_path,
            public_config_path=config_path,
            generation_receipt_path=model_b / "generation.receipt.json",
            arm_id="ARM-MODEL-B-V2",
            bound_at_utc=_GENERATED_AT,
        ),
        model_b_binding,
    )
    model_a_arm = _bind_recovery_arm_to_pair(
        run_dir=model_a,
        plan=plan,
        plan_path=plan_path,
        config_path=config_path,
        generation_binding_path=model_a_binding,
        arm_id="ARM-MODEL-A",
        run_label="model-a",
    )
    model_b_arm = _bind_recovery_arm_to_pair(
        run_dir=model_b,
        plan=plan,
        plan_path=plan_path,
        config_path=config_path,
        generation_binding_path=model_b_binding,
        arm_id="ARM-MODEL-B-V2",
        run_label="model-b-v2",
    )
    paired_freeze_path = tmp_path / "paired-prediction.freeze.json"
    write_paired_prediction_freeze_receipt(
        create_paired_prediction_freeze_receipt(
            plan_path=plan_path,
            public_config_path=config_path,
            arms=(model_a_arm, model_b_arm),
            created_at_utc=_PAIR_FREEZE_AT,
        ),
        paired_freeze_path,
    )
    _bind_reveal_to_pair(
        run_dir=model_a,
        plan_path=plan_path,
        paired_freeze_path=paired_freeze_path,
        arm_id="ARM-MODEL-A",
    )
    _bind_reveal_to_pair(
        run_dir=model_b,
        plan_path=plan_path,
        paired_freeze_path=paired_freeze_path,
        arm_id="ARM-MODEL-B-V2",
    )
    return PairPaths(
        model_a=model_a,
        model_b=model_b,
        plan=plan_path,
        config=config_path,
        model_a_binding=model_a_binding,
        model_b_binding=model_b_binding,
        paired_freeze=paired_freeze_path,
    )


def _rewrite_canonical(path: Path, payload: Any) -> None:
    path.unlink()
    write_new_canonical_json(path, payload)


def test_complete_pair_recomputes_metrics_and_binds_public_pair_evidence(
    tmp_path: Path,
) -> None:
    paths = _write_pair(tmp_path)

    report = compare_model_a_v2_new_run_dirs(
        paths.model_a,
        paths.model_b,
        **paths.compare_kwargs(),
        created_at_utc=datetime(2026, 8, 22, 1, tzinfo=UTC),
    )

    assert report.claim_boundary == (
        "synthetic-engineering-discovery-only-not-holdout-or-human-validation"
    )
    assert report.assignment_scope == "discovery_only"
    assert report.holdout_status == "frozen-withheld-not-evaluated"
    assert report.paired_experiment_evidence.plan_file_sha256 == sha256_file(paths.plan)
    assert report.paired_experiment_evidence.public_config_file_sha256 == sha256_file(paths.config)
    assert report.outcomes.improved == 2
    assert report.outcomes.worsened == 0
    assert report.cases[0].b_minus_a_midrank == -1.0
    assert report.model_a_aggregate.mean_midrank == pytest.approx(9.5)
    assert report.model_b_aggregate.mean_midrank == pytest.approx(1.5)
    assert report.model_a_aggregate.mean_midrank != 31.0
    assert report.top_1.b_minus_a == pytest.approx(
        report.model_b_aggregate.top_1 - report.model_a_aggregate.top_1
    )
    restored = next(
        item
        for item in report.restoration_differences
        if item.method == "active" and item.cluster_count == 1
    )
    assert restored.mean_midrank.b_minus_a == -8.0
    assert {item.cluster_id for item in report.ablation_differences} == {
        "CORE",
        "DETAILED",
    }
    assert report.model_a_failure_counts["scoring_bug"] == 1
    assert report.model_b_failure_counts["scoring_bug"] == 1
    assert report.chance_calendar_baseline.top_1 == pytest.approx(1.0 / 31.0)
    assert report.chance_calendar_baseline.mean_midrank == 16.0

    output = tmp_path / "paired-comparison.json"
    write_paired_model_comparison_report(report, output)
    assert load_json_bytes(output, require_canonical=True)["case_count"] == 2


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"target_variant": "different"}, "revealed_target_set_sha256"),
        ({"secret_seed": 9}, "seed commitment"),
        ({"month": 2}, "candidate constraints"),
        ({"workers": 2}, "recovery_settings"),
    ],
)
def test_pair_fails_closed_when_shared_identity_differs(
    tmp_path: Path, overrides: dict[str, Any], message: str
) -> None:
    paths = _write_pair(tmp_path, **overrides)

    with pytest.raises(PairedModelComparisonError, match=message):
        compare_model_a_v2_new_run_dirs(
            paths.model_a,
            paths.model_b,
            **paths.compare_kwargs(),
        )


def test_pair_freeze_rejects_different_or_unaudited_candidate_cache(
    tmp_path: Path,
) -> None:
    with pytest.raises(PairedPredictionFreezeError):
        _write_pair(tmp_path, cache_hash="0" * 64)


def test_pair_freeze_rejects_different_ephemeris_bytes(tmp_path: Path) -> None:
    with pytest.raises(PairedPredictionFreezeError):
        _write_pair(tmp_path, ephemeris_hash="0" * 64)


def test_each_arm_chain_is_verified_before_comparison(tmp_path: Path) -> None:
    paths = _write_pair(tmp_path)
    prediction_path = paths.model_a / "predictions.json"
    prediction_path.write_bytes(prediction_path.read_bytes() + b" ")

    with pytest.raises(PairedModelComparisonError, match="canonical predictions"):
        compare_model_a_v2_new_run_dirs(
            paths.model_a,
            paths.model_b,
            **paths.compare_kwargs(),
        )


def test_comparison_timestamp_cannot_precede_evaluation(tmp_path: Path) -> None:
    paths = _write_pair(tmp_path)

    with pytest.raises(PairedModelComparisonError, match="predates arm evaluation"):
        compare_model_a_v2_new_run_dirs(
            paths.model_a,
            paths.model_b,
            **paths.compare_kwargs(),
            created_at_utc=datetime(2026, 8, 22, 0, 5, 30, tzinfo=UTC),
        )


def test_pair_binding_fails_closed_after_generation_receipt_change(tmp_path: Path) -> None:
    paths = _write_pair(tmp_path)
    receipt_path = paths.model_a / "generation.receipt.json"
    receipt = load_json_bytes(receipt_path, require_canonical=True)
    receipt["public_config_sha256"] = "0" * 64
    _rewrite_canonical(receipt_path, receipt)

    with pytest.raises(PairedModelComparisonError, match="paired plan"):
        compare_model_a_v2_new_run_dirs(
            paths.model_a,
            paths.model_b,
            **paths.compare_kwargs(),
        )


def test_reveal_v3_is_mandatory(tmp_path: Path) -> None:
    paths = _write_pair(tmp_path)
    reveal_path = paths.model_a / "answer-key.reveal.json"
    reveal = load_json_bytes(reveal_path, require_canonical=True)
    reveal["schema_version"] = "answer-key-reveal-v2"
    reveal["revealed_target_set_sha256"] = None
    reveal["revealed_local_date_set_sha256"] = None
    reveal["generation_seed_commitment_sha256"] = None
    reveal["paired_prediction_freeze_sha256"] = None
    reveal["paired_plan_sha256"] = None
    reveal["paired_arm_id"] = None
    _rewrite_canonical(reveal_path, reveal)

    with pytest.raises(PairedModelComparisonError, match="reveal v3"):
        compare_model_a_v2_new_run_dirs(
            paths.model_a,
            paths.model_b,
            **paths.compare_kwargs(),
        )


def test_public_local_dates_must_match_reveal_v3_commitment(tmp_path: Path) -> None:
    paths = _write_pair(tmp_path)
    evaluation_path = paths.model_a / "evaluation.json"
    evaluation = load_json_bytes(evaluation_path, require_canonical=True)
    evaluation["cases"][0]["true_candidate_id"] = "2000-01-03"
    _rewrite_canonical(evaluation_path, evaluation)

    with pytest.raises(PairedModelComparisonError, match="authenticated reveal-v3"):
        compare_model_a_v2_new_run_dirs(
            paths.model_a,
            paths.model_b,
            **paths.compare_kwargs(),
        )


def test_loader_rejects_tampered_isolation_evidence(tmp_path: Path) -> None:
    paths = _write_pair(tmp_path)
    receipt_path = paths.model_b / "keyless-isolation.receipt.json"
    receipt = load_json_bytes(receipt_path, require_canonical=True)
    receipt["runtime_controls"]["evaluator_secret_mounts"] = "present"
    _rewrite_canonical(receipt_path, receipt)

    with pytest.raises(PairedModelComparisonError, match="runtime controls"):
        load_verified_public_run(paths.model_b, expected_model_id=MODEL_B_V2_NEW_ID)
