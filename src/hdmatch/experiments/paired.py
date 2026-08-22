"""Immutable plan and generation-receipt bindings for paired oracle experiments.

This module has no generation, reveal, decryption, or answer-key interface.  A
plan is created only from an already verified public V2 difference binding, one
exact public config, and a domain-separated commitment to the shared secret
seed.  Separate arm receipts then bind the same exact plan bytes to each exact
generation receipt.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.config import SyntheticConfig, load_synthetic_config
from hdmatch.evaluation.behavioral_difference import VerifiedBehavioralDifferenceBinding

from .answer_key_commitments import generation_seed_commitment as _seed_commitment
from .canonical import (
    load_json_bytes,
    sha256_file,
    sha256_json,
    write_new_canonical_json,
)

SHA256_PATTERN = r"^[a-f0-9]{64}$"
MODEL_A_ID = "MODEL-A-CORE-V1"
MODEL_B_V2_ID = "MODEL-B-DETAILED-V2-NEW"
SEED_COMMITMENT_SCHEME = "sha256-canonical-json-synthetic-generation-seed-v1"


class PairedExperimentBindingError(ValueError):
    """Raised when any plan or generation-receipt binding is stale or mismatched."""


class FrozenPairedModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ExactFileBinding(FrozenPairedModel):
    path: str = Field(min_length=1)
    sha256: str = Field(pattern=SHA256_PATTERN)


class PublicConfigBinding(FrozenPairedModel):
    file: ExactFileBinding
    semantic_sha256: str = Field(pattern=SHA256_PATTERN)
    payload: SyntheticConfig

    @model_validator(mode="after")
    def validate_public_config(self) -> PublicConfigBinding:
        if self.payload.seed is not None:
            raise ValueError("paired public config must not contain a generation seed")
        if sha256_json(self.payload) != self.semantic_sha256:
            raise ValueError("public-config payload does not match its semantic SHA-256")
        return self


class PairedModelArm(FrozenPairedModel):
    arm_id: str = Field(pattern=r"^[A-Z0-9][A-Z0-9_-]*$")
    role: Literal["model_a", "model_b_v2"]
    model_id: Literal["MODEL-A-CORE-V1", "MODEL-B-DETAILED-V2-NEW"]
    model_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_sha256: str = Field(pattern=SHA256_PATTERN)
    question_bank_sha256: str = Field(pattern=SHA256_PATTERN)
    compiled_file_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    freeze_receipt_file_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_role_identity(self) -> PairedModelArm:
        if self.role == "model_a":
            if self.model_id != MODEL_A_ID:
                raise ValueError("Model A arm has the wrong model ID")
            if self.compiled_file_sha256 is not None or self.freeze_receipt_file_sha256 is not None:
                raise ValueError("Model A arm cannot claim V2 compiled/freeze artifacts")
        else:
            if self.model_id != MODEL_B_V2_ID:
                raise ValueError("Model B V2 arm has the wrong model ID")
            if self.compiled_file_sha256 is None or self.freeze_receipt_file_sha256 is None:
                raise ValueError("Model B V2 arm requires compiled and freeze-receipt hashes")
            if self.mapping_sha256 != self.compiled_file_sha256:
                raise ValueError("Model B V2 mapping hash must equal its compiled-file hash")
        return self


class PairedExperimentPlan(FrozenPairedModel):
    schema_version: Literal["paired-experiment-plan-v1"] = "paired-experiment-plan-v1"
    paired_experiment_id: str = Field(min_length=1)
    planned_at_utc: datetime
    verified_v2_audit: VerifiedBehavioralDifferenceBinding
    verified_v2_audit_binding_sha256: str = Field(pattern=SHA256_PATTERN)
    public_config: PublicConfigBinding
    seed_commitment_scheme: Literal["sha256-canonical-json-synthetic-generation-seed-v1"] = (
        "sha256-canonical-json-synthetic-generation-seed-v1"
    )
    generation_seed_commitment_sha256: str = Field(pattern=SHA256_PATTERN)
    arms: tuple[PairedModelArm, PairedModelArm]
    answer_keys_used: Literal[False] = False
    claim_boundary: Literal["synthetic-engineering-paired-comparison-only-not-human-validation"] = (
        "synthetic-engineering-paired-comparison-only-not-human-validation"
    )

    @field_validator("planned_at_utc")
    @classmethod
    def require_plan_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("paired-plan timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_complete_plan(self) -> PairedExperimentPlan:
        if self.verified_v2_audit.audited_at_utc > self.planned_at_utc:
            raise ValueError("verified V2 audit must not postdate the paired plan")
        if sha256_json(self.verified_v2_audit) != self.verified_v2_audit_binding_sha256:
            raise ValueError("verified V2 audit binding hash is mismatched")
        if self.public_config.payload.experiment_id != self.paired_experiment_id:
            raise ValueError("paired experiment ID must equal the public config experiment ID")
        request = self.verified_v2_audit.candidate_universe_request
        config = self.public_config.payload
        if (
            config.universe != "known_month"
            or config.year_start != request.year
            or config.year_end != request.year
            or config.month != request.month
            or config.timezone != request.timezone_name
        ):
            raise ValueError("paired public config does not match the verified audit universe")
        if self.arms[0].arm_id == self.arms[1].arm_id:
            raise ValueError("paired arm IDs must be distinct")
        by_role = {arm.role: arm for arm in self.arms}
        if set(by_role) != {"model_a", "model_b_v2"}:
            raise ValueError("paired plan requires exactly one Model A and one Model B V2 arm")
        audit = self.verified_v2_audit
        model_a = by_role["model_a"]
        model_b = by_role["model_b_v2"]
        expected: tuple[tuple[str, object, object], ...] = (
            ("Model A semantic SHA", model_a.model_sha256, audit.model_a_sha256),
            ("Model A mapping SHA", model_a.mapping_sha256, audit.model_a_mapping_sha256),
            ("Model B semantic SHA", model_b.model_sha256, audit.model_b_sha256),
            (
                "Model B compiled SHA",
                model_b.compiled_file_sha256,
                audit.model_b_compiled_file_sha256,
            ),
            (
                "Model B freeze SHA",
                model_b.freeze_receipt_file_sha256,
                audit.model_b_freeze_receipt_file_sha256,
            ),
            (
                "Model A question-bank SHA",
                model_a.question_bank_sha256,
                audit.question_bank_sha256,
            ),
            (
                "Model B question-bank SHA",
                model_b.question_bank_sha256,
                audit.question_bank_sha256,
            ),
        )
        for label, recorded, audited in expected:
            if recorded != audited:
                raise ValueError(f"{label} does not match the verified V2 audit")
        return self

    @property
    def plan_sha256(self) -> str:
        return sha256_json(self)

    def arm(self, arm_id: str) -> PairedModelArm:
        matches = tuple(item for item in self.arms if item.arm_id == arm_id)
        if len(matches) != 1:
            raise PairedExperimentBindingError(f"unknown paired arm ID: {arm_id}")
        return matches[0]


class PairedGenerationReceiptBinding(FrozenPairedModel):
    schema_version: Literal["paired-generation-receipt-binding-v1"] = (
        "paired-generation-receipt-binding-v1"
    )
    bound_at_utc: datetime
    paired_plan: ExactFileBinding
    paired_plan_semantic_sha256: str = Field(pattern=SHA256_PATTERN)
    paired_experiment_id: str = Field(min_length=1)
    plan_created_at_utc: datetime
    generation_started_at_utc: datetime
    generation_software_commit: str = Field(pattern=r"^[a-f0-9]{40}$")
    generation_software_environment_sha256: str = Field(pattern=SHA256_PATTERN)
    chart_engine_fingerprint: str = Field(pattern=SHA256_PATTERN)
    ephemeris_sha256: dict[str, str]
    arm: PairedModelArm
    generation_receipt: ExactFileBinding
    public_config_file_sha256: str = Field(pattern=SHA256_PATTERN)
    seed_commitment_scheme: Literal["sha256-canonical-json-synthetic-generation-seed-v1"] = (
        "sha256-canonical-json-synthetic-generation-seed-v1"
    )
    generation_seed_commitment_sha256: str = Field(pattern=SHA256_PATTERN)
    blind_input_sha256: str = Field(pattern=SHA256_PATTERN)
    encrypted_answer_key_sha256: str = Field(pattern=SHA256_PATTERN)
    answer_key_opened: Literal[False] = False
    claim_boundary: Literal["synthetic-engineering-paired-generation-binding-only"] = (
        "synthetic-engineering-paired-generation-binding-only"
    )

    @field_validator("bound_at_utc", "plan_created_at_utc", "generation_started_at_utc")
    @classmethod
    def require_receipt_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("paired receipt timestamp must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_timestamp_order(self) -> PairedGenerationReceiptBinding:
        if not (self.plan_created_at_utc <= self.generation_started_at_utc <= self.bound_at_utc):
            raise ValueError("paired generation receipt cannot predate the paired plan")
        return self


def generation_seed_commitment(*, paired_experiment_id: str, secret_seed: int) -> str:
    """Commit to the exact shared seed without placing the seed in public artifacts."""

    if not paired_experiment_id:
        raise ValueError("paired experiment ID must not be empty")
    return _seed_commitment(secret_seed)


def verify_generation_seed_commitment(
    plan: PairedExperimentPlan,
    *,
    secret_seed: int,
) -> PairedExperimentPlan:
    """Verify the owner-held seed against the plan without serializing the seed."""

    expected = generation_seed_commitment(
        paired_experiment_id=plan.paired_experiment_id,
        secret_seed=secret_seed,
    )
    if expected != plan.generation_seed_commitment_sha256:
        raise PairedExperimentBindingError("secret seed does not match the paired plan")
    return plan


def create_paired_experiment_plan(
    *,
    paired_experiment_id: str,
    verified_v2_audit: VerifiedBehavioralDifferenceBinding,
    public_config_path: str | Path,
    generation_seed_commitment_sha256: str,
    model_a_arm_id: str,
    model_b_v2_arm_id: str,
    planned_at_utc: datetime | None = None,
) -> PairedExperimentPlan:
    config_path = Path(public_config_path)
    config = load_synthetic_config(config_path)
    audit = verified_v2_audit
    return PairedExperimentPlan(
        paired_experiment_id=paired_experiment_id,
        planned_at_utc=planned_at_utc or datetime.now(UTC),
        verified_v2_audit=audit,
        verified_v2_audit_binding_sha256=sha256_json(audit),
        public_config=PublicConfigBinding(
            file=ExactFileBinding(path=config_path.as_posix(), sha256=sha256_file(config_path)),
            semantic_sha256=sha256_json(config),
            payload=config,
        ),
        generation_seed_commitment_sha256=generation_seed_commitment_sha256,
        arms=(
            PairedModelArm(
                arm_id=model_a_arm_id,
                role="model_a",
                model_id="MODEL-A-CORE-V1",
                model_sha256=audit.model_a_sha256,
                mapping_sha256=audit.model_a_mapping_sha256,
                question_bank_sha256=audit.question_bank_sha256,
            ),
            PairedModelArm(
                arm_id=model_b_v2_arm_id,
                role="model_b_v2",
                model_id="MODEL-B-DETAILED-V2-NEW",
                model_sha256=audit.model_b_sha256,
                mapping_sha256=audit.model_b_compiled_file_sha256,
                question_bank_sha256=audit.question_bank_sha256,
                compiled_file_sha256=audit.model_b_compiled_file_sha256,
                freeze_receipt_file_sha256=audit.model_b_freeze_receipt_file_sha256,
            ),
        ),
    )


def write_paired_experiment_plan(plan: PairedExperimentPlan, path: str | Path) -> Path:
    return write_new_canonical_json(path, plan)


def load_paired_experiment_plan(path: str | Path) -> PairedExperimentPlan:
    try:
        return PairedExperimentPlan.model_validate(load_json_bytes(path, require_canonical=True))
    except (OSError, ValueError) as exc:
        raise PairedExperimentBindingError(
            f"invalid or non-canonical paired experiment plan: {path}"
        ) from exc


def verify_paired_experiment_plan(
    plan_path: str | Path,
    *,
    paired_experiment_id: str,
    verified_v2_audit: VerifiedBehavioralDifferenceBinding,
    public_config_path: str | Path,
    generation_seed_commitment_sha256: str,
    model_a_arm_id: str,
    model_b_v2_arm_id: str,
) -> PairedExperimentPlan:
    plan = load_paired_experiment_plan(plan_path)
    expected = create_paired_experiment_plan(
        paired_experiment_id=paired_experiment_id,
        verified_v2_audit=verified_v2_audit,
        public_config_path=public_config_path,
        generation_seed_commitment_sha256=generation_seed_commitment_sha256,
        model_a_arm_id=model_a_arm_id,
        model_b_v2_arm_id=model_b_v2_arm_id,
        planned_at_utc=plan.planned_at_utc,
    )
    if plan != expected:
        raise PairedExperimentBindingError("paired experiment plan is stale or mismatched")
    if sha256_file(plan_path) != plan.plan_sha256:
        raise PairedExperimentBindingError("paired experiment plan exact bytes are mismatched")
    return plan


def create_paired_generation_receipt_binding(
    *,
    plan_path: str | Path,
    public_config_path: str | Path,
    generation_receipt_path: str | Path,
    arm_id: str,
    bound_at_utc: datetime | None = None,
) -> PairedGenerationReceiptBinding:
    plan = load_paired_experiment_plan(plan_path)
    _verify_current_public_config(plan, public_config_path)
    generation_path = Path(generation_receipt_path)
    raw = _load_generation_receipt(generation_path)
    arm = plan.arm(arm_id)
    (
        generation_started_at_utc,
        generation_software_commit,
        generation_software_environment_sha256,
        chart_engine_fingerprint,
        ephemeris_sha256,
    ) = _verify_underlying_generation_receipt(plan, arm, raw)
    timestamp = bound_at_utc or datetime.now(UTC)
    return PairedGenerationReceiptBinding(
        bound_at_utc=timestamp,
        paired_plan=ExactFileBinding(
            path=Path(plan_path).as_posix(),
            sha256=sha256_file(plan_path),
        ),
        paired_plan_semantic_sha256=plan.plan_sha256,
        paired_experiment_id=plan.paired_experiment_id,
        plan_created_at_utc=plan.planned_at_utc,
        generation_started_at_utc=generation_started_at_utc,
        generation_software_commit=generation_software_commit,
        generation_software_environment_sha256=(generation_software_environment_sha256),
        chart_engine_fingerprint=chart_engine_fingerprint,
        ephemeris_sha256=ephemeris_sha256,
        arm=arm,
        generation_receipt=ExactFileBinding(
            path=generation_path.as_posix(),
            sha256=sha256_file(generation_path),
        ),
        public_config_file_sha256=plan.public_config.file.sha256,
        generation_seed_commitment_sha256=plan.generation_seed_commitment_sha256,
        blind_input_sha256=str(raw["blind_input_sha256"]),
        encrypted_answer_key_sha256=str(raw["encrypted_answer_key_sha256"]),
    )


def write_paired_generation_receipt_binding(
    receipt: PairedGenerationReceiptBinding,
    path: str | Path,
) -> Path:
    return write_new_canonical_json(path, receipt)


def load_paired_generation_receipt_binding(
    path: str | Path,
) -> PairedGenerationReceiptBinding:
    try:
        return PairedGenerationReceiptBinding.model_validate(
            load_json_bytes(path, require_canonical=True)
        )
    except (OSError, ValueError) as exc:
        raise PairedExperimentBindingError(
            f"invalid or non-canonical paired generation receipt binding: {path}"
        ) from exc


def verify_paired_generation_receipt_binding(
    receipt_binding_path: str | Path,
    *,
    plan_path: str | Path,
    public_config_path: str | Path,
    generation_receipt_path: str | Path,
    expected_arm_id: str,
) -> PairedGenerationReceiptBinding:
    receipt = load_paired_generation_receipt_binding(receipt_binding_path)
    expected = create_paired_generation_receipt_binding(
        plan_path=plan_path,
        public_config_path=public_config_path,
        generation_receipt_path=generation_receipt_path,
        arm_id=expected_arm_id,
        bound_at_utc=receipt.bound_at_utc,
    )
    # The same exact public files are deliberately relocated to fixed paths inside
    # the keyless mount namespace.  Paths are provenance labels only; the SHA-256
    # fields remain authoritative and must still match the current bytes.  Normalize
    # only the two location labels before comparing every scientific/security field.
    normalized = receipt.model_copy(
        update={
            "paired_plan": receipt.paired_plan.model_copy(
                update={"path": expected.paired_plan.path}
            ),
            "generation_receipt": receipt.generation_receipt.model_copy(
                update={"path": expected.generation_receipt.path}
            ),
        }
    )
    if normalized != expected:
        raise PairedExperimentBindingError(
            "paired generation receipt binding is stale or mismatched"
        )
    return receipt


def _verify_current_public_config(
    plan: PairedExperimentPlan,
    public_config_path: str | Path,
) -> None:
    config_path = Path(public_config_path)
    if sha256_file(config_path) != plan.public_config.file.sha256:
        raise PairedExperimentBindingError("public config exact bytes changed after planning")
    current = load_synthetic_config(config_path)
    if current != plan.public_config.payload or sha256_json(current) != (
        plan.public_config.semantic_sha256
    ):
        raise PairedExperimentBindingError("public config semantics changed after planning")


def _load_generation_receipt(path: Path) -> dict[str, Any]:
    try:
        value = load_json_bytes(path, require_canonical=True)
    except (OSError, ValueError) as exc:
        raise PairedExperimentBindingError(
            f"invalid or non-canonical generation receipt: {path}"
        ) from exc
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise PairedExperimentBindingError("generation receipt must be a JSON object")
    return value


def _verify_underlying_generation_receipt(
    plan: PairedExperimentPlan,
    arm: PairedModelArm,
    receipt: dict[str, Any],
) -> tuple[datetime, str, str, str, dict[str, str]]:
    if _contains_secret_material(receipt):
        raise PairedExperimentBindingError("generation receipt exposes answer-key material")
    expected: tuple[tuple[str, object, object], ...] = (
        ("schema_version", receipt.get("schema_version"), "generation-receipt-v1"),
        ("experiment_id", receipt.get("experiment_id"), plan.paired_experiment_id),
        ("model_id", receipt.get("model_id"), arm.model_id),
        ("model_sha256", receipt.get("model_sha256"), arm.model_sha256),
        ("mapping_sha256", receipt.get("mapping_sha256"), arm.mapping_sha256),
        (
            "question_bank_sha256",
            receipt.get("question_bank_sha256"),
            arm.question_bank_sha256,
        ),
        (
            "public_config_sha256",
            receipt.get("public_config_sha256"),
            plan.public_config.file.sha256,
        ),
        ("case_count", receipt.get("case_count"), plan.public_config.payload.case_count),
        ("seed_status", receipt.get("seed_status"), "sealed-in-answer-key-only"),
        (
            "claim_boundary",
            receipt.get("claim_boundary"),
            "synthetic-engineering-validation-only",
        ),
    )
    for label, recorded, planned in expected:
        if recorded != planned:
            raise PairedExperimentBindingError(
                f"generation receipt {label} does not match the paired plan"
            )
    for name in ("blind_input_sha256", "encrypted_answer_key_sha256"):
        value = receipt.get(name)
        if (
            not isinstance(value, str)
            or len(value) != 64
            or any(character not in "0123456789abcdef" for character in value)
        ):
            raise PairedExperimentBindingError(f"generation receipt has invalid {name}")
    recorded_audit = receipt.get("model_b_v2_difference_gate")
    if arm.role == "model_b_v2":
        if recorded_audit != plan.verified_v2_audit.model_dump(mode="json"):
            raise PairedExperimentBindingError(
                "Model B V2 generation receipt has a stale or missing audit binding"
            )
    elif recorded_audit is not None:
        raise PairedExperimentBindingError(
            "Model A generation receipt cannot claim the Model B V2 audit binding"
        )
    expected_pair = {
        "schema_version": "paired-generation-reference-v1",
        "paired_experiment_id": plan.paired_experiment_id,
        "paired_plan_file_sha256": plan.plan_sha256,
        "paired_plan_semantic_sha256": plan.plan_sha256,
        "arm_id": arm.arm_id,
        "arm_role": arm.role,
        "generation_seed_commitment_sha256": (plan.generation_seed_commitment_sha256),
    }
    if receipt.get("paired_experiment") != expected_pair:
        raise PairedExperimentBindingError(
            "generation receipt lacks the exact paired-plan/arm reference"
        )
    generation_commit = receipt.get("generation_software_commit")
    if (
        not isinstance(generation_commit, str)
        or len(generation_commit) != 40
        or any(character not in "0123456789abcdef" for character in generation_commit)
        or receipt.get("generation_software_dirty") is not False
    ):
        raise PairedExperimentBindingError(
            "paired generation must bind a clean committed source tree"
        )
    generation_environment = receipt.get("generation_software_environment")
    if not isinstance(generation_environment, dict):
        raise PairedExperimentBindingError("paired generation lacks software environment")
    engine_fingerprint = receipt.get("chart_engine_fingerprint")
    if (
        not isinstance(engine_fingerprint, str)
        or len(engine_fingerprint) != 64
        or any(character not in "0123456789abcdef" for character in engine_fingerprint)
    ):
        raise PairedExperimentBindingError("paired generation lacks chart-engine identity")
    raw_ephemeris = receipt.get("ephemeris_sha256")
    if (
        not isinstance(raw_ephemeris, dict)
        or not raw_ephemeris
        or not all(
            isinstance(name, str)
            and name
            and isinstance(digest, str)
            and len(digest) == 64
            and not any(character not in "0123456789abcdef" for character in digest)
            for name, digest in raw_ephemeris.items()
        )
    ):
        raise PairedExperimentBindingError("paired generation lacks ephemeris identity")
    started = receipt.get("generation_started_at_utc")
    try:
        started_at = datetime.fromisoformat(str(started).replace("Z", "+00:00"))
    except ValueError as exc:
        raise PairedExperimentBindingError(
            "generation receipt has an invalid generation timestamp"
        ) from exc
    if started_at.tzinfo is None or started_at.astimezone(UTC) < plan.planned_at_utc:
        raise PairedExperimentBindingError("generation started before the paired plan")
    return (
        started_at.astimezone(UTC),
        generation_commit,
        sha256_json(generation_environment),
        engine_fingerprint,
        dict(sorted(raw_ephemeris.items())),
    )


def _contains_secret_material(value: object) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {
                "answer_key",
                "cases",
                "generation_seed",
                "secret_seed",
                "seed",
                "true_chart_features_hash",
                "true_local_datetime",
                "true_state_id",
                "true_utc",
            }:
                return True
            if _contains_secret_material(item):
                return True
    elif isinstance(value, list):
        return any(_contains_secret_material(item) for item in value)
    return False
