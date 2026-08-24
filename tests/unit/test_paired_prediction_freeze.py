from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from hdmatch.evaluation.behavioral_difference import (
    BehavioralDifferenceMonthRequest,
    VerifiedBehavioralDifferenceBinding,
)
from hdmatch.experiments.canonical import (
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
    generation_seed_commitment,
    load_paired_experiment_plan,
    write_paired_experiment_plan,
    write_paired_generation_receipt_binding,
)
from hdmatch.experiments.paired_freeze import (
    PairedFreezeArmArtifacts,
    PairedPredictionFreezeError,
    PairedPredictionFreezeReceipt,
    create_paired_prediction_freeze_receipt,
    load_paired_prediction_freeze_receipt,
    verify_paired_prediction_freeze_receipt,
    write_paired_prediction_freeze_receipt,
)

_AUDIT_AT = datetime(2026, 8, 22, 1, 0, tzinfo=UTC)
_PLAN_AT = _AUDIT_AT + timedelta(minutes=1)
_GENERATION_AT = _PLAN_AT + timedelta(minutes=1)
_GENERATION_BOUND_AT = _GENERATION_AT + timedelta(minutes=1)
_MANIFEST_AT = _GENERATION_BOUND_AT + timedelta(minutes=1)
_ISOLATION_AT = _MANIFEST_AT + timedelta(minutes=1)
_FREEZE_AT = _ISOLATION_AT + timedelta(minutes=1)
_PAIR_FREEZE_AT = _FREEZE_AT + timedelta(minutes=1)


def _digest(label: str) -> str:
    return sha256_bytes(label.encode())


def _audit() -> VerifiedBehavioralDifferenceBinding:
    return VerifiedBehavioralDifferenceBinding(
        audit_file_sha256=_digest("audit-file"),
        audited_at_utc=_AUDIT_AT,
        model_a_sha256=_digest("model-a"),
        model_a_mapping_sha256=_digest("model-a-mapping"),
        model_b_compiled_file_sha256=_digest("model-b-compiled"),
        model_b_freeze_receipt_file_sha256=_digest("model-b-freeze"),
        model_b_sha256=_digest("model-b"),
        question_bank_sha256=_digest("question-bank"),
        candidate_cache_file_sha256=_digest("candidate-cache"),
        candidate_engine_fingerprint=_digest("engine"),
        candidate_universe_request=BehavioralDifferenceMonthRequest(
            year=2000,
            month=1,
            timezone_name="UTC",
        ),
        candidate_universe_sha256=_digest("universe"),
        candidate_state_count=100,
    )


def _write_config(path: Path) -> None:
    path.write_text(
        "\n".join(
            (
                "experiment_id: PAIRED-FREEZE-2",
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


def _overwrite_canonical(path: Path, value: object) -> None:
    path.unlink()
    write_new_canonical_json(path, value)


def _write_arm(
    root: Path,
    *,
    plan_path: Path,
    config_path: Path,
    arm_id: str,
    run_label: str,
) -> tuple[PairedFreezeArmArtifacts, dict[str, Path]]:
    plan = load_paired_experiment_plan(plan_path)
    arm = plan.arm(arm_id)
    run_dir = root / run_label
    run_dir.mkdir()
    blind_sha256 = _digest(f"blind-{arm_id}")
    environment = SoftwareEnvironment(
        python_version="3.11.10",
        python_implementation="CPython",
        operating_system="Linux",
        machine="x86_64",
        packages={"hdmatch": "0.1.0"},
    )

    generation_path = run_dir / "generation.receipt.json"
    generation: dict[str, Any] = {
        "schema_version": "generation-receipt-v1",
        "experiment_id": plan.paired_experiment_id,
        "model_id": arm.model_id,
        "blind_input_sha256": blind_sha256,
        "encrypted_answer_key_sha256": _digest(f"envelope-{arm_id}"),
        "public_config_sha256": plan.public_config.file.sha256,
        "model_sha256": arm.model_sha256,
        "question_bank_sha256": arm.question_bank_sha256,
        "mapping_sha256": arm.mapping_sha256,
        "case_count": plan.public_config.payload.case_count,
        "seed_status": "sealed-in-answer-key-only",
        "external_reveal_key_status": "owner-only-key-ready-path-withheld",
        "claim_boundary": "synthetic-engineering-validation-only",
        "generation_started_at_utc": _GENERATION_AT,
        "paired_experiment": {
            "schema_version": "paired-generation-reference-v1",
            "paired_experiment_id": plan.paired_experiment_id,
            "paired_plan_file_sha256": sha256_file(plan_path),
            "paired_plan_semantic_sha256": plan.plan_sha256,
            "arm_id": arm.arm_id,
            "arm_role": arm.role,
            "generation_seed_commitment_sha256": (plan.generation_seed_commitment_sha256),
        },
        "generation_software_commit": "a" * 40,
        "generation_software_dirty": False,
        "generation_software_environment": environment.model_dump(mode="json"),
        "chart_engine_fingerprint": plan.verified_v2_audit.candidate_engine_fingerprint,
        "ephemeris_sha256": {"public.se1": _digest("ephemeris")},
    }
    if arm.role == "model_b_v2":
        generation["model_b_v2_difference_gate"] = plan.verified_v2_audit.model_dump(mode="json")
    write_new_canonical_json(generation_path, generation)

    generation_binding = create_paired_generation_receipt_binding(
        plan_path=plan_path,
        public_config_path=config_path,
        generation_receipt_path=generation_path,
        arm_id=arm_id,
        bound_at_utc=_GENERATION_BOUND_AT,
    )
    generation_binding_path = run_dir / "paired-generation.receipt.json"
    write_paired_generation_receipt_binding(generation_binding, generation_binding_path)

    paired_recovery_binding = {
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
    recovery_config = {
        "aggregation": "duration_weighted_evidence",
        "cache_policy": "hash-bound exact month universes",
        "threshold_rubric_bits": 0.0,
        "workers": 1,
        "paired_experiment": paired_recovery_binding,
    }
    manifest = RunManifest(
        experiment_id=plan.paired_experiment_id,
        created_at_utc=_MANIFEST_AT,
        seed=int(blind_sha256[:16], 16),
        software_commit="a" * 40,
        software_dirty=False,
        software_environment=environment,
        candidate_universe="known_month",
        aggregation_rule="duration_weighted_evidence",
        model_id=arm.model_id,
        input_hashes={
            "blind_cases.json": blind_sha256,
            "paired_experiment_plan": sha256_file(plan_path),
            "paired_public_config": sha256_file(config_path),
            "paired_generation_receipt": sha256_file(generation_path),
            "paired_generation_binding": sha256_file(generation_binding_path),
        },
        config_payload=recovery_config,
        config_sha256=sha256_json(recovery_config),
        declared_outputs=("predictions.json", "prediction.freeze.json"),
    )
    manifest_path = run_dir / "run.manifest.json"
    write_new_canonical_json(manifest_path, manifest)

    predictions = {
        "schema_version": "predictions-v1",
        "experiment_id": plan.paired_experiment_id,
        "model_id": arm.model_id,
        "blind_input_sha256": blind_sha256,
        "model_sha256": arm.model_sha256,
        "question_bank_sha256": arm.question_bank_sha256,
        "mapping_sha256": arm.mapping_sha256,
        "candidate_cache_sha256": {
            "month-2000-01-UTC-test.json": plan.verified_v2_audit.candidate_cache_file_sha256
        },
        "predictions": [{"case_id": "CASE-0001"}, {"case_id": "CASE-0002"}],
    }
    predictions_path = run_dir / "predictions.json"
    write_new_canonical_json(predictions_path, predictions)
    isolation_path = run_dir / "keyless-isolation.receipt.json"
    write_new_canonical_json(
        isolation_path,
        {
            "schema_version": "keyless-recovery-isolation-receipt-v1",
            "model_id": arm.model_id,
            "blind_input_sha256": blind_sha256,
            "run_manifest_sha256": sha256_file(manifest_path),
            "prediction_sha256": sha256_file(predictions_path),
            "paired_plan_sha256": sha256_file(plan_path),
            "paired_generation_receipt_sha256": sha256_file(generation_path),
            "paired_generation_binding_sha256": sha256_file(generation_binding_path),
            "paired_arm_id": arm.arm_id,
            "software_tree": "0" * 40,
            "ephemeris_sha256": generation["ephemeris_sha256"],
            "created_at_utc": _ISOLATION_AT,
        },
    )
    freeze = FreezeRecord(
        experiment_id=plan.paired_experiment_id,
        prediction_file="predictions.json",
        prediction_sha256=sha256_file(predictions_path),
        prediction_size_bytes=predictions_path.stat().st_size,
        blind_input_sha256=blind_sha256,
        model_sha256=arm.model_sha256,
        question_bank_sha256=arm.question_bank_sha256,
        mapping_sha256=arm.mapping_sha256,
        run_manifest_sha256=sha256_file(manifest_path),
        software_commit=manifest.software_commit,
        software_dirty=manifest.software_dirty,
        software_versions=environment.packages | {"python": environment.python_version},
        created_at_utc=_FREEZE_AT,
    )
    freeze_path = run_dir / "prediction.freeze.json"
    write_new_canonical_json(freeze_path, freeze)
    artifacts = PairedFreezeArmArtifacts(
        role=arm.role,
        arm_id=arm.arm_id,
        run_logical_label=run_label,
        run_dir=run_dir,
        generation_receipt_path=generation_path,
        generation_binding_path=generation_binding_path,
        isolation_receipt_path=isolation_path,
    )
    return artifacts, {
        "generation": generation_path,
        "generation_binding": generation_binding_path,
        "manifest": manifest_path,
        "predictions": predictions_path,
        "freeze": freeze_path,
        "isolation": isolation_path,
    }


def _setup_pair(tmp_path: Path) -> dict[str, object]:
    config_path = tmp_path / "paired.yaml"
    _write_config(config_path)
    audit = _audit()
    plan = create_paired_experiment_plan(
        paired_experiment_id="PAIRED-FREEZE-2",
        verified_v2_audit=audit,
        public_config_path=config_path,
        generation_seed_commitment_sha256=generation_seed_commitment(
            paired_experiment_id="PAIRED-FREEZE-2",
            secret_seed=9_223_372_036_854_770_123,
        ),
        model_a_arm_id="ARM-MODEL-A",
        model_b_v2_arm_id="ARM-MODEL-B-V2",
        planned_at_utc=_PLAN_AT,
    )
    plan_path = tmp_path / "paired.plan.json"
    write_paired_experiment_plan(plan, plan_path)
    model_a, model_a_paths = _write_arm(
        tmp_path,
        plan_path=plan_path,
        config_path=config_path,
        arm_id="ARM-MODEL-A",
        run_label="model-a-run",
    )
    model_b, model_b_paths = _write_arm(
        tmp_path,
        plan_path=plan_path,
        config_path=config_path,
        arm_id="ARM-MODEL-B-V2",
        run_label="model-b-v2-run",
    )
    arms = (model_a, model_b)
    receipt = create_paired_prediction_freeze_receipt(
        plan_path=plan_path,
        public_config_path=config_path,
        arms=arms,
        created_at_utc=_PAIR_FREEZE_AT,
    )
    receipt_path = tmp_path / "paired-prediction.freeze.json"
    write_paired_prediction_freeze_receipt(receipt, receipt_path)
    return {
        "plan": plan_path,
        "config": config_path,
        "arms": arms,
        "receipt": receipt,
        "receipt_path": receipt_path,
        "model_a_paths": model_a_paths,
        "model_b_paths": model_b_paths,
    }


def _verify_pair(fixture: dict[str, object]) -> PairedPredictionFreezeReceipt:
    return verify_paired_prediction_freeze_receipt(
        fixture["receipt_path"],
        plan_path=fixture["plan"],
        public_config_path=fixture["config"],
        arms=fixture["arms"],
    )


def test_receipt_binds_both_complete_chains_without_secret_material(tmp_path: Path) -> None:
    fixture = _setup_pair(tmp_path)
    receipt = _verify_pair(fixture)
    assert load_paired_prediction_freeze_receipt(fixture["receipt_path"]) == receipt
    assert receipt.receipt_sha256 == sha256_file(fixture["receipt_path"])
    assert tuple(arm.role for arm in receipt.arms) == ("model_a", "model_b_v2")
    assert len({arm.paired_plan_file_sha256 for arm in receipt.arms}) == 1
    assert len({arm.generation_seed_commitment_sha256 for arm in receipt.arms}) == 1
    assert all(arm.prediction_frozen_at_utc < receipt.created_at_utc for arm in receipt.arms)
    raw = Path(fixture["receipt_path"]).read_bytes()
    assert str(tmp_path).encode() not in raw
    assert b"9223372036854770123" not in raw
    assert b'"generation_seed":' not in raw
    assert b'"secret_seed":' not in raw
    assert b'"answer_key_path":' not in raw
    with pytest.raises(FileExistsError):
        write_paired_prediction_freeze_receipt(receipt, fixture["receipt_path"])


@pytest.mark.parametrize(
    ("group", "name"),
    (
        (None, "plan"),
        (None, "config"),
        ("model_a_paths", "generation"),
        ("model_b_paths", "generation_binding"),
        ("model_a_paths", "manifest"),
        ("model_b_paths", "isolation"),
        ("model_b_paths", "predictions"),
        ("model_a_paths", "freeze"),
    ),
)
def test_verification_rejects_mutated_current_artifact_bytes(
    tmp_path: Path,
    group: str | None,
    name: str,
) -> None:
    fixture = _setup_pair(tmp_path)
    path = Path(fixture[name]) if group is None else fixture[group][name]
    path.write_bytes(path.read_bytes() + b"\n")
    with pytest.raises(PairedPredictionFreezeError):
        _verify_pair(fixture)


def test_creation_rejects_duplicate_roles_labels_and_stale_prediction_binding(
    tmp_path: Path,
) -> None:
    fixture = _setup_pair(tmp_path)
    model_a, model_b = fixture["arms"]
    with pytest.raises(PairedPredictionFreezeError, match="one input per paired arm"):
        create_paired_prediction_freeze_receipt(
            plan_path=fixture["plan"],
            public_config_path=fixture["config"],
            arms=(model_a, model_a),
            created_at_utc=_PAIR_FREEZE_AT,
        )
    with pytest.raises(PairedPredictionFreezeError):
        create_paired_prediction_freeze_receipt(
            plan_path=fixture["plan"],
            public_config_path=fixture["config"],
            arms=(model_a, replace(model_b, run_logical_label=model_a.run_logical_label)),
            created_at_utc=_PAIR_FREEZE_AT,
        )

    prediction_path = fixture["model_b_paths"]["predictions"]
    prediction = load_json_bytes(prediction_path, require_canonical=True)
    prediction["mapping_sha256"] = _digest("wrong-mapping")
    _overwrite_canonical(prediction_path, prediction)
    freeze_path = fixture["model_b_paths"]["freeze"]
    freeze = FreezeRecord.model_validate(load_json_bytes(freeze_path, require_canonical=True))
    _overwrite_canonical(
        freeze_path,
        freeze.model_copy(
            update={
                "prediction_sha256": sha256_file(prediction_path),
                "prediction_size_bytes": prediction_path.stat().st_size,
            }
        ),
    )
    with pytest.raises(PairedPredictionFreezeError, match="mismatched mapping_sha256"):
        create_paired_prediction_freeze_receipt(
            plan_path=fixture["plan"],
            public_config_path=fixture["config"],
            arms=fixture["arms"],
            created_at_utc=_PAIR_FREEZE_AT,
        )


def test_timestamp_order_fails_closed_for_receipt_manifest_and_generation_binding(
    tmp_path: Path,
) -> None:
    fixture = _setup_pair(tmp_path)
    with pytest.raises(PairedPredictionFreezeError):
        create_paired_prediction_freeze_receipt(
            plan_path=fixture["plan"],
            public_config_path=fixture["config"],
            arms=fixture["arms"],
            created_at_utc=_FREEZE_AT,
        )

    receipt = fixture["receipt"]
    with pytest.raises(ValidationError, match="freeze predates"):
        PairedPredictionFreezeReceipt.model_validate(
            receipt.model_copy(
                update={
                    "arms": (
                        receipt.arms[0].model_copy(
                            update={"manifest_created_at_utc": _FREEZE_AT + timedelta(seconds=1)}
                        ),
                        receipt.arms[1],
                    )
                }
            ).model_dump(mode="python")
        )
    with pytest.raises(ValidationError, match="manifest predates"):
        PairedPredictionFreezeReceipt.model_validate(
            receipt.model_copy(
                update={
                    "arms": (
                        receipt.arms[0].model_copy(
                            update={"generation_bound_at_utc": _MANIFEST_AT + timedelta(seconds=1)}
                        ),
                        receipt.arms[1],
                    )
                }
            ).model_dump(mode="python")
        )


def test_receipt_model_rejects_duplicate_role_and_shared_identity_mismatches(
    tmp_path: Path,
) -> None:
    fixture = _setup_pair(tmp_path)
    receipt = fixture["receipt"]
    duplicate_role = receipt.arms[1].model_copy(
        update={"role": "model_a", "model_id": "MODEL-A-CORE-V1"}
    )
    with pytest.raises(ValidationError, match="exactly once"):
        PairedPredictionFreezeReceipt.model_validate(
            receipt.model_copy(update={"arms": (receipt.arms[0], duplicate_role)}).model_dump(
                mode="python"
            )
        )
    mismatched_plan = receipt.arms[0].model_copy(
        update={"paired_plan_file_sha256": _digest("stale-plan")}
    )
    with pytest.raises(ValidationError, match="paired plan file"):
        PairedPredictionFreezeReceipt.model_validate(
            receipt.model_copy(update={"arms": (mismatched_plan, receipt.arms[1])}).model_dump(
                mode="python"
            )
        )
