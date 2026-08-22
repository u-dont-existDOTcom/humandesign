"""Pre-reveal freeze gate for a paired Model A / Model B V2 experiment.

The artifact defined here is deliberately answer-key free.  It proves that both
arms were generated from the same exact paired plan and that each arm's current
manifest, prediction bytes, and prediction-freeze record form one intact chain.
Callers can require :func:`verify_paired_prediction_freeze_receipt` before either
reveal or comparison without gaining any key, truth, or secret-path interface.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .canonical import load_json_bytes, sha256_file, sha256_json, write_new_canonical_json
from .freeze import ArtifactBindings, FreezeVerificationError, verify_frozen_predictions
from .manifest import SHA256_PATTERN, load_run_manifest
from .paired import (
    PairedExperimentBindingError,
    PairedExperimentPlan,
    PairedModelArm,
    load_paired_experiment_plan,
    verify_paired_generation_receipt_binding,
)

ArmRole = Literal["model_a", "model_b_v2"]


class PairedPredictionFreezeError(ValueError):
    """A paired freeze receipt or one of its public inputs is stale or invalid."""


class FrozenPairedFreezeModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


@dataclass(frozen=True)
class PairedFreezeArmArtifacts:
    """Caller-supplied public artifact locations; never serialized in the receipt."""

    role: ArmRole
    arm_id: str
    run_logical_label: str
    run_dir: Path
    generation_receipt_path: Path
    generation_binding_path: Path
    isolation_receipt_path: Path
    run_manifest_path: Path | None = None
    prediction_freeze_path: Path | None = None


class FrozenArmChain(FrozenPairedFreezeModel):
    role: ArmRole
    arm_id: str = Field(pattern=r"^[A-Z0-9][A-Z0-9_-]*$")
    run_logical_label: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
    model_id: Literal["MODEL-A-CORE-V1", "MODEL-B-DETAILED-V2-NEW"]
    blind_input_sha256: str = Field(pattern=SHA256_PATTERN)
    model_sha256: str = Field(pattern=SHA256_PATTERN)
    question_bank_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    paired_plan_file_sha256: str = Field(pattern=SHA256_PATTERN)
    paired_plan_semantic_sha256: str = Field(pattern=SHA256_PATTERN)
    public_config_file_sha256: str = Field(pattern=SHA256_PATTERN)
    public_config_semantic_sha256: str = Field(pattern=SHA256_PATTERN)
    generation_seed_commitment_sha256: str = Field(pattern=SHA256_PATTERN)
    generation_receipt_sha256: str = Field(pattern=SHA256_PATTERN)
    generation_binding_sha256: str = Field(pattern=SHA256_PATTERN)
    run_manifest_sha256: str = Field(pattern=SHA256_PATTERN)
    prediction_sha256: str = Field(pattern=SHA256_PATTERN)
    prediction_freeze_sha256: str = Field(pattern=SHA256_PATTERN)
    isolation_receipt_sha256: str = Field(pattern=SHA256_PATTERN)
    candidate_cache_sha256: dict[str, str]
    generation_software_commit: str = Field(pattern=r"^[a-f0-9]{40}$")
    generation_software_environment_sha256: str = Field(pattern=SHA256_PATTERN)
    chart_engine_fingerprint: str = Field(pattern=SHA256_PATTERN)
    ephemeris_sha256: dict[str, str]
    isolation_software_tree: str = Field(pattern=r"^[a-f0-9]{40}$")
    software_commit: str = Field(pattern=r"^[a-f0-9]{40}$")
    software_environment_sha256: str = Field(pattern=SHA256_PATTERN)
    generation_bound_at_utc: datetime
    manifest_created_at_utc: datetime
    isolation_created_at_utc: datetime
    prediction_frozen_at_utc: datetime

    @field_validator(
        "generation_bound_at_utc",
        "manifest_created_at_utc",
        "isolation_created_at_utc",
        "prediction_frozen_at_utc",
    )
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("paired arm timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_arm_chain(self) -> FrozenArmChain:
        expected_model = "MODEL-A-CORE-V1" if self.role == "model_a" else "MODEL-B-DETAILED-V2-NEW"
        if self.model_id != expected_model:
            raise ValueError("paired frozen arm role and model ID disagree")
        if self.generation_bound_at_utc > self.manifest_created_at_utc:
            raise ValueError("run manifest predates its paired generation binding")
        if not (
            self.manifest_created_at_utc
            <= self.isolation_created_at_utc
            <= self.prediction_frozen_at_utc
        ):
            raise ValueError("prediction freeze predates its run manifest")
        if len(self.candidate_cache_sha256) != 1 or any(
            not name
            or len(digest) != 64
            or any(character not in "0123456789abcdef" for character in digest)
            for name, digest in self.candidate_cache_sha256.items()
        ):
            raise ValueError("paired arm must bind exactly one canonical month cache")
        return self


class PairedPredictionFreezeReceipt(FrozenPairedFreezeModel):
    schema_version: Literal["paired-prediction-freeze-receipt-v1"] = (
        "paired-prediction-freeze-receipt-v1"
    )
    paired_experiment_id: str = Field(min_length=1)
    created_at_utc: datetime
    paired_plan_file_sha256: str = Field(pattern=SHA256_PATTERN)
    paired_plan_semantic_sha256: str = Field(pattern=SHA256_PATTERN)
    paired_plan_created_at_utc: datetime
    verified_v2_audit_binding_sha256: str = Field(pattern=SHA256_PATTERN)
    verified_v2_audit_file_sha256: str = Field(pattern=SHA256_PATTERN)
    verified_v2_candidate_cache_file_sha256: str = Field(pattern=SHA256_PATTERN)
    verified_v2_candidate_engine_fingerprint: str = Field(pattern=SHA256_PATTERN)
    public_config_file_sha256: str = Field(pattern=SHA256_PATTERN)
    public_config_semantic_sha256: str = Field(pattern=SHA256_PATTERN)
    seed_commitment_scheme: Literal["sha256-canonical-json-synthetic-generation-seed-v1"] = (
        "sha256-canonical-json-synthetic-generation-seed-v1"
    )
    generation_seed_commitment_sha256: str = Field(pattern=SHA256_PATTERN)
    arms: tuple[FrozenArmChain, FrozenArmChain]
    answer_keys_used: Literal[False] = False
    answer_key_revealed: Literal[False] = False
    claim_boundary: Literal[
        "paired-predictions-frozen-before-reveal-synthetic-engineering-only"
    ] = "paired-predictions-frozen-before-reveal-synthetic-engineering-only"

    @field_validator("created_at_utc", "paired_plan_created_at_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("paired freeze timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_complete_pair(self) -> PairedPredictionFreezeReceipt:
        if self.paired_plan_created_at_utc > self.created_at_utc:
            raise ValueError("paired prediction-freeze receipt predates its plan")
        if tuple(arm.role for arm in self.arms) != ("model_a", "model_b_v2"):
            raise ValueError("receipt requires Model A then Model B V2 exactly once")
        if len({arm.arm_id for arm in self.arms}) != 2:
            raise ValueError("paired prediction-freeze arm IDs must be distinct")
        if len({arm.run_logical_label for arm in self.arms}) != 2:
            raise ValueError("paired prediction-freeze run labels must be distinct")
        for arm in self.arms:
            shared = (
                ("paired plan file", arm.paired_plan_file_sha256, self.paired_plan_file_sha256),
                (
                    "paired plan semantic",
                    arm.paired_plan_semantic_sha256,
                    self.paired_plan_semantic_sha256,
                ),
                (
                    "public config file",
                    arm.public_config_file_sha256,
                    self.public_config_file_sha256,
                ),
                (
                    "public config semantic",
                    arm.public_config_semantic_sha256,
                    self.public_config_semantic_sha256,
                ),
                (
                    "generation seed commitment",
                    arm.generation_seed_commitment_sha256,
                    self.generation_seed_commitment_sha256,
                ),
            )
            for label, recorded, expected in shared:
                if recorded != expected:
                    raise ValueError(f"paired arm has a mismatched {label} hash")
            if self.paired_plan_created_at_utc > arm.generation_bound_at_utc:
                raise ValueError("paired generation binding predates the paired plan")
            if arm.prediction_frozen_at_utc >= self.created_at_utc:
                raise ValueError("both prediction freezes must predate the paired receipt")
        if self.arms[0].candidate_cache_sha256 != self.arms[1].candidate_cache_sha256:
            raise ValueError("paired arms used different candidate-cache bytes")
        if set(self.arms[0].candidate_cache_sha256.values()) != {
            self.verified_v2_candidate_cache_file_sha256
        }:
            raise ValueError("paired candidate cache is not the exact audited cache")
        if len({arm.software_commit for arm in self.arms}) != 1:
            raise ValueError("paired arms used different software commits")
        if len({arm.software_environment_sha256 for arm in self.arms}) != 1:
            raise ValueError("paired arms used different software environments")
        if len({arm.isolation_software_tree for arm in self.arms}) != 1:
            raise ValueError("paired arms used different isolated source trees")
        if any(arm.generation_software_commit != arm.software_commit for arm in self.arms):
            raise ValueError("generation and recovery used different software commits")
        if any(
            arm.generation_software_environment_sha256 != arm.software_environment_sha256
            for arm in self.arms
        ):
            raise ValueError("generation and recovery used different software environments")
        if len({arm.chart_engine_fingerprint for arm in self.arms}) != 1 or (
            self.arms[0].chart_engine_fingerprint != self.verified_v2_candidate_engine_fingerprint
        ):
            raise ValueError("paired arms used a different chart engine from the audit")
        if self.arms[0].ephemeris_sha256 != self.arms[1].ephemeris_sha256:
            raise ValueError("paired arms used different generation ephemeris bytes")
        return self

    @property
    def receipt_sha256(self) -> str:
        return sha256_json(self)


def _expected_arm_bindings(arm: PairedModelArm, blind_input_sha256: str) -> ArtifactBindings:
    return ArtifactBindings(
        blind_input_sha256=blind_input_sha256,
        model_sha256=arm.model_sha256,
        question_bank_sha256=arm.question_bank_sha256,
        mapping_sha256=arm.mapping_sha256,
    )


def _load_prediction_object(path: Path) -> dict[str, object]:
    try:
        value = load_json_bytes(path, require_canonical=True)
    except (OSError, ValueError) as exc:
        raise PairedPredictionFreezeError("invalid or non-canonical predictions") from exc
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise PairedPredictionFreezeError("predictions must be a canonical JSON object")
    return value


def _load_isolation_receipt(path: Path) -> dict[str, object]:
    try:
        value = load_json_bytes(path, require_canonical=True)
    except (OSError, ValueError) as exc:
        raise PairedPredictionFreezeError(
            "invalid or non-canonical keyless isolation receipt"
        ) from exc
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise PairedPredictionFreezeError("keyless isolation receipt must be an object")
    return value


def _parse_utc(value: object, *, label: str) -> datetime:
    if not isinstance(value, str):
        raise PairedPredictionFreezeError(f"{label} must be a UTC timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PairedPredictionFreezeError(f"{label} is invalid") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise PairedPredictionFreezeError(f"{label} must be timezone-aware")
    return parsed.astimezone(UTC)


def _require_prediction_bindings(
    predictions: dict[str, object],
    *,
    plan: PairedExperimentPlan,
    arm: PairedModelArm,
    blind_input_sha256: str,
) -> None:
    expected: tuple[tuple[str, object, object], ...] = (
        ("experiment_id", predictions.get("experiment_id"), plan.paired_experiment_id),
        ("model_id", predictions.get("model_id"), arm.model_id),
        ("blind_input_sha256", predictions.get("blind_input_sha256"), blind_input_sha256),
        ("model_sha256", predictions.get("model_sha256"), arm.model_sha256),
        (
            "question_bank_sha256",
            predictions.get("question_bank_sha256"),
            arm.question_bank_sha256,
        ),
        ("mapping_sha256", predictions.get("mapping_sha256"), arm.mapping_sha256),
    )
    for label, recorded, required in expected:
        if recorded != required:
            raise PairedPredictionFreezeError(f"predictions have a mismatched {label}")


def _verify_arm_chain(
    *,
    plan: PairedExperimentPlan,
    plan_path: Path,
    public_config_path: Path,
    artifacts: PairedFreezeArmArtifacts,
) -> FrozenArmChain:
    arm = plan.arm(artifacts.arm_id)
    if arm.role != artifacts.role:
        raise PairedPredictionFreezeError("paired arm role does not match its planned arm ID")
    generation = verify_paired_generation_receipt_binding(
        artifacts.generation_binding_path,
        plan_path=plan_path,
        public_config_path=public_config_path,
        generation_receipt_path=artifacts.generation_receipt_path,
        expected_arm_id=artifacts.arm_id,
    )
    run_dir = artifacts.run_dir
    manifest_path = artifacts.run_manifest_path or run_dir / "run.manifest.json"
    freeze_path = artifacts.prediction_freeze_path or run_dir / "prediction.freeze.json"
    bindings = _expected_arm_bindings(arm, generation.blind_input_sha256)
    freeze = verify_frozen_predictions(
        run_dir,
        freeze_path=freeze_path,
        expected_bindings=bindings,
        expected_experiment_id=plan.paired_experiment_id,
        run_manifest_path=manifest_path,
        require_run_manifest=True,
    )
    manifest = load_run_manifest(manifest_path)
    if manifest.model_id != arm.model_id:
        raise PairedPredictionFreezeError("run manifest model ID differs from the paired arm")
    if manifest.experiment_id != plan.paired_experiment_id:
        raise PairedPredictionFreezeError("run manifest experiment differs from the paired plan")
    prediction_path = run_dir / freeze.prediction_file
    predictions = _load_prediction_object(prediction_path)
    _require_prediction_bindings(
        predictions,
        plan=plan,
        arm=arm,
        blind_input_sha256=generation.blind_input_sha256,
    )
    expected_input_hashes = {
        "paired_experiment_plan": sha256_file(plan_path),
        "paired_public_config": sha256_file(public_config_path),
        "paired_generation_receipt": sha256_file(artifacts.generation_receipt_path),
        "paired_generation_binding": sha256_file(artifacts.generation_binding_path),
    }
    for name, expected in expected_input_hashes.items():
        if manifest.input_hashes.get(name) != expected:
            raise PairedPredictionFreezeError(f"run manifest lacks exact {name} binding")
    expected_paired_config = {
        "schema_version": "paired-recovery-binding-v1",
        "paired_experiment_id": plan.paired_experiment_id,
        "paired_plan_file_sha256": sha256_file(plan_path),
        "paired_plan_semantic_sha256": plan.plan_sha256,
        "paired_generation_receipt_sha256": sha256_file(artifacts.generation_receipt_path),
        "paired_generation_binding_sha256": sha256_file(artifacts.generation_binding_path),
        "public_config_file_sha256": sha256_file(public_config_path),
        "public_config_semantic_sha256": plan.public_config.semantic_sha256,
        "generation_seed_commitment_sha256": plan.generation_seed_commitment_sha256,
        "arm_id": arm.arm_id,
        "arm_role": arm.role,
    }
    if (
        manifest.config_payload is None
        or manifest.config_payload.get("paired_experiment") != expected_paired_config
    ):
        raise PairedPredictionFreezeError("run manifest lacks the exact paired recovery binding")
    raw_cache = predictions.get("candidate_cache_sha256")
    if not isinstance(raw_cache, dict) or not all(
        isinstance(name, str) and isinstance(digest, str) for name, digest in raw_cache.items()
    ):
        raise PairedPredictionFreezeError("predictions lack candidate-cache hashes")
    candidate_cache_sha256 = dict(sorted(raw_cache.items()))

    isolation = _load_isolation_receipt(artifacts.isolation_receipt_path)
    isolation_expected: tuple[tuple[str, object, object], ...] = (
        (
            "schema_version",
            isolation.get("schema_version"),
            "keyless-recovery-isolation-receipt-v1",
        ),
        ("model_id", isolation.get("model_id"), arm.model_id),
        ("blind_input_sha256", isolation.get("blind_input_sha256"), generation.blind_input_sha256),
        ("run_manifest_sha256", isolation.get("run_manifest_sha256"), sha256_file(manifest_path)),
        ("prediction_sha256", isolation.get("prediction_sha256"), sha256_file(prediction_path)),
        ("paired_plan_sha256", isolation.get("paired_plan_sha256"), sha256_file(plan_path)),
        (
            "paired_generation_receipt_sha256",
            isolation.get("paired_generation_receipt_sha256"),
            sha256_file(artifacts.generation_receipt_path),
        ),
        (
            "paired_generation_binding_sha256",
            isolation.get("paired_generation_binding_sha256"),
            sha256_file(artifacts.generation_binding_path),
        ),
        ("paired_arm_id", isolation.get("paired_arm_id"), arm.arm_id),
    )
    for label, recorded, required_value in isolation_expected:
        if recorded != required_value:
            raise PairedPredictionFreezeError(f"keyless isolation receipt has mismatched {label}")
    isolation_created_at_utc = _parse_utc(
        isolation.get("created_at_utc"), label="isolation receipt timestamp"
    )
    isolation_tree = isolation.get("software_tree")
    if (
        not isinstance(isolation_tree, str)
        or len(isolation_tree) != 40
        or any(character not in "0123456789abcdef" for character in isolation_tree)
    ):
        raise PairedPredictionFreezeError(
            "keyless isolation receipt lacks an exact source-tree identity"
        )
    isolation_ephemeris = isolation.get("ephemeris_sha256")
    if isolation_ephemeris != generation.ephemeris_sha256:
        raise PairedPredictionFreezeError(
            "generation and isolated recovery used different ephemeris bytes"
        )
    return FrozenArmChain(
        role=arm.role,
        arm_id=arm.arm_id,
        run_logical_label=artifacts.run_logical_label,
        model_id=arm.model_id,
        blind_input_sha256=generation.blind_input_sha256,
        model_sha256=arm.model_sha256,
        question_bank_sha256=arm.question_bank_sha256,
        mapping_sha256=arm.mapping_sha256,
        paired_plan_file_sha256=sha256_file(plan_path),
        paired_plan_semantic_sha256=plan.plan_sha256,
        public_config_file_sha256=plan.public_config.file.sha256,
        public_config_semantic_sha256=plan.public_config.semantic_sha256,
        generation_seed_commitment_sha256=plan.generation_seed_commitment_sha256,
        generation_receipt_sha256=sha256_file(artifacts.generation_receipt_path),
        generation_binding_sha256=sha256_file(artifacts.generation_binding_path),
        run_manifest_sha256=sha256_file(manifest_path),
        prediction_sha256=sha256_file(prediction_path),
        prediction_freeze_sha256=sha256_file(freeze_path),
        isolation_receipt_sha256=sha256_file(artifacts.isolation_receipt_path),
        candidate_cache_sha256=candidate_cache_sha256,
        generation_software_commit=generation.generation_software_commit,
        generation_software_environment_sha256=(generation.generation_software_environment_sha256),
        chart_engine_fingerprint=generation.chart_engine_fingerprint,
        ephemeris_sha256=generation.ephemeris_sha256,
        isolation_software_tree=isolation_tree,
        software_commit=manifest.software_commit,
        software_environment_sha256=sha256_json(manifest.software_environment),
        generation_bound_at_utc=generation.bound_at_utc,
        manifest_created_at_utc=manifest.created_at_utc,
        isolation_created_at_utc=isolation_created_at_utc,
        prediction_frozen_at_utc=freeze.created_at_utc,
    )


def create_paired_prediction_freeze_receipt(
    *,
    plan_path: str | Path,
    public_config_path: str | Path,
    arms: tuple[PairedFreezeArmArtifacts, PairedFreezeArmArtifacts],
    created_at_utc: datetime | None = None,
) -> PairedPredictionFreezeReceipt:
    """Verify both current public chains and build an answer-key-free pair receipt."""

    exact_plan_path = Path(plan_path)
    exact_config_path = Path(public_config_path)
    try:
        plan = load_paired_experiment_plan(exact_plan_path)
        if sha256_file(exact_plan_path) != plan.plan_sha256:
            raise PairedPredictionFreezeError("paired plan exact bytes are mismatched")
        by_role = {item.role: item for item in arms}
        if len(by_role) != 2 or set(by_role) != {"model_a", "model_b_v2"}:
            raise PairedPredictionFreezeError("exactly one input per paired arm role is required")
        roles: tuple[ArmRole, ArmRole] = ("model_a", "model_b_v2")
        frozen_arms = tuple(
            _verify_arm_chain(
                plan=plan,
                plan_path=exact_plan_path,
                public_config_path=exact_config_path,
                artifacts=by_role[role],
            )
            for role in roles
        )
        return PairedPredictionFreezeReceipt(
            paired_experiment_id=plan.paired_experiment_id,
            created_at_utc=created_at_utc or datetime.now(UTC),
            paired_plan_file_sha256=sha256_file(exact_plan_path),
            paired_plan_semantic_sha256=plan.plan_sha256,
            paired_plan_created_at_utc=plan.planned_at_utc,
            verified_v2_audit_binding_sha256=plan.verified_v2_audit_binding_sha256,
            verified_v2_audit_file_sha256=plan.verified_v2_audit.audit_file_sha256,
            verified_v2_candidate_cache_file_sha256=(
                plan.verified_v2_audit.candidate_cache_file_sha256
            ),
            verified_v2_candidate_engine_fingerprint=(
                plan.verified_v2_audit.candidate_engine_fingerprint
            ),
            public_config_file_sha256=plan.public_config.file.sha256,
            public_config_semantic_sha256=plan.public_config.semantic_sha256,
            generation_seed_commitment_sha256=plan.generation_seed_commitment_sha256,
            arms=(frozen_arms[0], frozen_arms[1]),
        )
    except PairedPredictionFreezeError:
        raise
    except (
        FileNotFoundError,
        FreezeVerificationError,
        OSError,
        PairedExperimentBindingError,
        ValueError,
    ) as exc:
        raise PairedPredictionFreezeError("paired prediction-freeze chain is invalid") from exc


def write_paired_prediction_freeze_receipt(
    receipt: PairedPredictionFreezeReceipt,
    path: str | Path,
) -> Path:
    return write_new_canonical_json(path, receipt)


def load_paired_prediction_freeze_receipt(
    path: str | Path,
) -> PairedPredictionFreezeReceipt:
    try:
        return PairedPredictionFreezeReceipt.model_validate(
            load_json_bytes(path, require_canonical=True)
        )
    except (OSError, ValueError) as exc:
        raise PairedPredictionFreezeError(
            "invalid or non-canonical paired prediction-freeze receipt"
        ) from exc


def verify_paired_prediction_freeze_receipt(
    receipt_path: str | Path,
    *,
    plan_path: str | Path,
    public_config_path: str | Path,
    arms: tuple[PairedFreezeArmArtifacts, PairedFreezeArmArtifacts],
) -> PairedPredictionFreezeReceipt:
    """Re-verify every current public byte before reveal or paired comparison."""

    receipt = load_paired_prediction_freeze_receipt(receipt_path)
    expected = create_paired_prediction_freeze_receipt(
        plan_path=plan_path,
        public_config_path=public_config_path,
        arms=arms,
        created_at_utc=receipt.created_at_utc,
    )
    if receipt != expected:
        raise PairedPredictionFreezeError("paired prediction-freeze receipt is stale or mismatched")
    if sha256_file(receipt_path) != receipt.receipt_sha256:
        raise PairedPredictionFreezeError("paired prediction-freeze receipt bytes changed")
    return receipt
