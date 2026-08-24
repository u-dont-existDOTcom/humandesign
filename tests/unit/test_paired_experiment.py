from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from pydantic import ValidationError

from hdmatch.evaluation.behavioral_difference import (
    BehavioralDifferenceMonthRequest,
    VerifiedBehavioralDifferenceBinding,
)
from hdmatch.experiments.canonical import sha256_bytes, sha256_file, write_new_canonical_json
from hdmatch.experiments.paired import (
    PairedExperimentBindingError,
    create_paired_experiment_plan,
    create_paired_generation_receipt_binding,
    generation_seed_commitment,
    load_paired_experiment_plan,
    load_paired_generation_receipt_binding,
    verify_generation_seed_commitment,
    verify_paired_experiment_plan,
    verify_paired_generation_receipt_binding,
    write_paired_experiment_plan,
    write_paired_generation_receipt_binding,
)


def _digest(label: str) -> str:
    return sha256_bytes(label.encode("utf-8"))


def _audit() -> VerifiedBehavioralDifferenceBinding:
    return VerifiedBehavioralDifferenceBinding(
        audit_file_sha256=_digest("audit-file"),
        audited_at_utc=datetime(2026, 8, 22, 1, 0, tzinfo=UTC),
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


def _write_config(path: Path, *, experiment_id: str = "PAIRED-ORACLE-75") -> None:
    path.write_text(
        "\n".join(
            (
                f"experiment_id: {experiment_id}",
                "case_count: 75",
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


def _create_plan(tmp_path: Path) -> tuple[Path, Path, str, VerifiedBehavioralDifferenceBinding]:
    config = tmp_path / "paired.yaml"
    _write_config(config)
    audit = _audit()
    commitment = generation_seed_commitment(
        paired_experiment_id="PAIRED-ORACLE-75",
        secret_seed=9_223_372_036_854_770_123,
    )
    plan = create_paired_experiment_plan(
        paired_experiment_id="PAIRED-ORACLE-75",
        verified_v2_audit=audit,
        public_config_path=config,
        generation_seed_commitment_sha256=commitment,
        model_a_arm_id="ARM-MODEL-A",
        model_b_v2_arm_id="ARM-MODEL-B-V2",
        planned_at_utc=audit.audited_at_utc + timedelta(minutes=1),
    )
    plan_path = tmp_path / "paired.plan.json"
    write_paired_experiment_plan(plan, plan_path)
    return plan_path, config, commitment, audit


def _write_generation_receipt(
    path: Path,
    *,
    plan_path: Path,
    arm_id: str,
    generation_started_at_utc: datetime | None = None,
) -> None:
    plan = load_paired_experiment_plan(plan_path)
    arm = plan.arm(arm_id)
    receipt: dict[str, object] = {
        "schema_version": "generation-receipt-v1",
        "experiment_id": plan.paired_experiment_id,
        "model_id": arm.model_id,
        "blind_input_sha256": _digest(f"blind-{arm_id}"),
        "encrypted_answer_key_sha256": _digest(f"envelope-{arm_id}"),
        "public_config_sha256": plan.public_config.file.sha256,
        "model_sha256": arm.model_sha256,
        "question_bank_sha256": arm.question_bank_sha256,
        "mapping_sha256": arm.mapping_sha256,
        "case_count": plan.public_config.payload.case_count,
        "seed_status": "sealed-in-answer-key-only",
        "external_reveal_key_status": "owner-only-key-ready-path-withheld",
        "claim_boundary": "synthetic-engineering-validation-only",
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
        "generation_software_environment": {"python": "test"},
        "chart_engine_fingerprint": plan.verified_v2_audit.candidate_engine_fingerprint,
        "ephemeris_sha256": {"public.se1": _digest("ephemeris")},
    }
    if arm.role == "model_b_v2":
        receipt["model_b_v2_difference_gate"] = plan.verified_v2_audit.model_dump(mode="json")
    if generation_started_at_utc is not None:
        receipt["generation_started_at_utc"] = generation_started_at_utc
    write_new_canonical_json(path, receipt)


def test_plan_binds_audit_config_models_and_secret_commitment_without_seed(
    tmp_path: Path,
) -> None:
    plan_path, config, commitment, audit = _create_plan(tmp_path)
    plan = load_paired_experiment_plan(plan_path)

    assert plan.plan_sha256 == sha256_file(plan_path)
    assert plan.verified_v2_audit == audit
    assert plan.public_config.file.sha256 == sha256_file(config)
    assert plan.generation_seed_commitment_sha256 == commitment
    assert {arm.model_id for arm in plan.arms} == {
        "MODEL-A-CORE-V1",
        "MODEL-B-DETAILED-V2-NEW",
    }
    assert plan.verified_v2_audit.audited_at_utc <= plan.planned_at_utc
    raw = plan_path.read_bytes()
    assert b"9223372036854770123" not in raw
    assert b'"generation_seed"' not in raw
    assert b'"secret_seed"' not in raw
    assert (
        verify_generation_seed_commitment(
            plan,
            secret_seed=9_223_372_036_854_770_123,
        )
        == plan
    )
    with pytest.raises(PairedExperimentBindingError, match="does not match"):
        verify_generation_seed_commitment(plan, secret_seed=123)

    assert (
        verify_paired_experiment_plan(
            plan_path,
            paired_experiment_id="PAIRED-ORACLE-75",
            verified_v2_audit=audit,
            public_config_path=config,
            generation_seed_commitment_sha256=commitment,
            model_a_arm_id="ARM-MODEL-A",
            model_b_v2_arm_id="ARM-MODEL-B-V2",
        )
        == plan
    )
    with pytest.raises(FileExistsError):
        write_paired_experiment_plan(plan, plan_path)


def test_plan_fails_closed_for_time_audit_config_commitment_and_encoding(
    tmp_path: Path,
) -> None:
    plan_path, config, commitment, audit = _create_plan(tmp_path)

    with pytest.raises(ValidationError, match="must not postdate"):
        create_paired_experiment_plan(
            paired_experiment_id="PAIRED-ORACLE-75",
            verified_v2_audit=audit,
            public_config_path=config,
            generation_seed_commitment_sha256=commitment,
            model_a_arm_id="ARM-MODEL-A",
            model_b_v2_arm_id="ARM-MODEL-B-V2",
            planned_at_utc=audit.audited_at_utc - timedelta(seconds=1),
        )
    with pytest.raises(PairedExperimentBindingError, match="stale or mismatched"):
        verify_paired_experiment_plan(
            plan_path,
            paired_experiment_id="PAIRED-ORACLE-75",
            verified_v2_audit=audit,
            public_config_path=config,
            generation_seed_commitment_sha256=_digest("different-commitment"),
            model_a_arm_id="ARM-MODEL-A",
            model_b_v2_arm_id="ARM-MODEL-B-V2",
        )
    stale_audit = audit.model_copy(update={"model_a_sha256": _digest("stale-model-a")})
    with pytest.raises(PairedExperimentBindingError, match="stale or mismatched"):
        verify_paired_experiment_plan(
            plan_path,
            paired_experiment_id="PAIRED-ORACLE-75",
            verified_v2_audit=stale_audit,
            public_config_path=config,
            generation_seed_commitment_sha256=commitment,
            model_a_arm_id="ARM-MODEL-A",
            model_b_v2_arm_id="ARM-MODEL-B-V2",
        )

    config.write_bytes(config.read_bytes() + b"# changed exact bytes\n")
    with pytest.raises(PairedExperimentBindingError, match="stale or mismatched"):
        verify_paired_experiment_plan(
            plan_path,
            paired_experiment_id="PAIRED-ORACLE-75",
            verified_v2_audit=audit,
            public_config_path=config,
            generation_seed_commitment_sha256=commitment,
            model_a_arm_id="ARM-MODEL-A",
            model_b_v2_arm_id="ARM-MODEL-B-V2",
        )

    noncanonical = tmp_path / "noncanonical-plan.json"
    noncanonical.write_bytes(plan_path.read_bytes() + b"\n")
    with pytest.raises(PairedExperimentBindingError, match="non-canonical"):
        load_paired_experiment_plan(noncanonical)


def test_same_exact_plan_sha_binds_both_generation_receipts(tmp_path: Path) -> None:
    plan_path, config, _, _ = _create_plan(tmp_path)
    plan = load_paired_experiment_plan(plan_path)
    model_a_generation = tmp_path / "model-a-generation.receipt.json"
    model_b_generation = tmp_path / "model-b-generation.receipt.json"
    started = plan.planned_at_utc + timedelta(minutes=1)
    _write_generation_receipt(
        model_a_generation,
        plan_path=plan_path,
        arm_id="ARM-MODEL-A",
        generation_started_at_utc=started,
    )
    _write_generation_receipt(
        model_b_generation,
        plan_path=plan_path,
        arm_id="ARM-MODEL-B-V2",
        generation_started_at_utc=started,
    )

    model_a_binding = create_paired_generation_receipt_binding(
        plan_path=plan_path,
        public_config_path=config,
        generation_receipt_path=model_a_generation,
        arm_id="ARM-MODEL-A",
        bound_at_utc=started + timedelta(minutes=1),
    )
    model_b_binding = create_paired_generation_receipt_binding(
        plan_path=plan_path,
        public_config_path=config,
        generation_receipt_path=model_b_generation,
        arm_id="ARM-MODEL-B-V2",
        bound_at_utc=started + timedelta(minutes=1),
    )
    assert model_a_binding.paired_plan.sha256 == model_b_binding.paired_plan.sha256
    assert model_a_binding.paired_plan.sha256 == sha256_file(plan_path)
    assert model_a_binding.paired_plan_semantic_sha256 == plan.plan_sha256
    assert model_b_binding.paired_plan_semantic_sha256 == plan.plan_sha256
    assert (
        model_a_binding.generation_seed_commitment_sha256
        == model_b_binding.generation_seed_commitment_sha256
    )
    assert model_a_binding.arm.arm_id != model_b_binding.arm.arm_id

    a_path = tmp_path / "model-a-paired.receipt.json"
    b_path = tmp_path / "model-b-paired.receipt.json"
    write_paired_generation_receipt_binding(model_a_binding, a_path)
    write_paired_generation_receipt_binding(model_b_binding, b_path)
    assert load_paired_generation_receipt_binding(a_path) == model_a_binding
    assert load_paired_generation_receipt_binding(b_path) == model_b_binding
    assert (
        verify_paired_generation_receipt_binding(
            a_path,
            plan_path=plan_path,
            public_config_path=config,
            generation_receipt_path=model_a_generation,
            expected_arm_id="ARM-MODEL-A",
        )
        == model_a_binding
    )
    assert (
        verify_paired_generation_receipt_binding(
            b_path,
            plan_path=plan_path,
            public_config_path=config,
            generation_receipt_path=model_b_generation,
            expected_arm_id="ARM-MODEL-B-V2",
        )
        == model_b_binding
    )


def test_generation_binding_is_portable_across_keyless_mount_paths(
    tmp_path: Path,
) -> None:
    plan_path, config, _, _ = _create_plan(tmp_path)
    plan = load_paired_experiment_plan(plan_path)
    generation = tmp_path / "generation.receipt.json"
    _write_generation_receipt(
        generation,
        plan_path=plan_path,
        arm_id="ARM-MODEL-A",
        generation_started_at_utc=plan.planned_at_utc + timedelta(seconds=1),
    )
    binding = create_paired_generation_receipt_binding(
        plan_path=plan_path,
        public_config_path=config,
        generation_receipt_path=generation,
        arm_id="ARM-MODEL-A",
        bound_at_utc=plan.planned_at_utc + timedelta(minutes=1),
    )
    binding_path = tmp_path / "paired.receipt.json"
    write_paired_generation_receipt_binding(binding, binding_path)

    sandbox = tmp_path / "relocated-keyless-public"
    sandbox.mkdir()
    relocated_plan = sandbox / "paired_plan.json"
    relocated_generation = sandbox / "generation_receipt.json"
    relocated_plan.write_bytes(plan_path.read_bytes())
    relocated_generation.write_bytes(generation.read_bytes())

    assert (
        verify_paired_generation_receipt_binding(
            binding_path,
            plan_path=relocated_plan,
            public_config_path=config,
            generation_receipt_path=relocated_generation,
            expected_arm_id="ARM-MODEL-A",
        )
        == binding
    )


def test_generation_receipt_binding_rejects_wrong_arm_content_time_and_bytes(
    tmp_path: Path,
) -> None:
    plan_path, config, _, _ = _create_plan(tmp_path)
    plan = load_paired_experiment_plan(plan_path)
    generation = tmp_path / "generation.receipt.json"
    _write_generation_receipt(
        generation,
        plan_path=plan_path,
        arm_id="ARM-MODEL-A",
        generation_started_at_utc=plan.planned_at_utc + timedelta(seconds=1),
    )
    binding = create_paired_generation_receipt_binding(
        plan_path=plan_path,
        public_config_path=config,
        generation_receipt_path=generation,
        arm_id="ARM-MODEL-A",
        bound_at_utc=plan.planned_at_utc + timedelta(minutes=1),
    )
    binding_path = tmp_path / "paired.receipt.json"
    write_paired_generation_receipt_binding(binding, binding_path)

    with pytest.raises(PairedExperimentBindingError, match="model_id"):
        create_paired_generation_receipt_binding(
            plan_path=plan_path,
            public_config_path=config,
            generation_receipt_path=generation,
            arm_id="ARM-MODEL-B-V2",
        )
    with pytest.raises(PairedExperimentBindingError, match="model_id"):
        verify_paired_generation_receipt_binding(
            binding_path,
            plan_path=plan_path,
            public_config_path=config,
            generation_receipt_path=generation,
            expected_arm_id="ARM-MODEL-B-V2",
        )

    early = tmp_path / "early-generation.receipt.json"
    _write_generation_receipt(
        early,
        plan_path=plan_path,
        arm_id="ARM-MODEL-A",
        generation_started_at_utc=plan.planned_at_utc - timedelta(seconds=1),
    )
    with pytest.raises(PairedExperimentBindingError, match="started before"):
        create_paired_generation_receipt_binding(
            plan_path=plan_path,
            public_config_path=config,
            generation_receipt_path=early,
            arm_id="ARM-MODEL-A",
        )

    generation.write_bytes(generation.read_bytes() + b"\n")
    with pytest.raises(PairedExperimentBindingError, match="non-canonical generation"):
        verify_paired_generation_receipt_binding(
            binding_path,
            plan_path=plan_path,
            public_config_path=config,
            generation_receipt_path=generation,
            expected_arm_id="ARM-MODEL-A",
        )

    secret_receipt = tmp_path / "secret-generation.receipt.json"
    _write_generation_receipt(
        secret_receipt,
        plan_path=plan_path,
        arm_id="ARM-MODEL-A",
        generation_started_at_utc=plan.planned_at_utc + timedelta(seconds=1),
    )
    raw_secret_receipt = secret_receipt.read_bytes()
    secret_receipt.unlink()
    exposed = json.loads(raw_secret_receipt)
    exposed["answer_key"] = {"generation_seed": 42}
    write_new_canonical_json(secret_receipt, exposed)
    with pytest.raises(PairedExperimentBindingError, match="answer-key material"):
        create_paired_generation_receipt_binding(
            plan_path=plan_path,
            public_config_path=config,
            generation_receipt_path=secret_receipt,
            arm_id="ARM-MODEL-A",
        )
