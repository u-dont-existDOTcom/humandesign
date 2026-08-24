"""Canonical, append-only artifacts for leakage-safe human experiments.

This module is deliberately file-oriented.  Fitting consumes only a separately mounted
development partition; blind scoring consumes only response/candidate records and a frozen
symbolic-prevalence artifact; truth enters only the post-freeze reveal function.
"""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.experiments.canonical import load_json_bytes, sha256_file, write_new_canonical_json
from hdmatch.experiments.manifest import (
    SHA256_PATTERN,
    SoftwareEnvironment,
    capture_software_environment,
    git_revision,
)
from hdmatch.human.dataset import HumanDataset
from hdmatch.human.protocol import (
    FINAL_TEST_RELEASE_ACKNOWLEDGEMENT,
    Cohort,
    FrozenHumanEvaluationProtocol,
    FrozenHumanModelBundle,
    HumanBlindCase,
    HumanCandidate,
    HumanCohortAnswerKey,
    HumanComparisonReport,
    HumanPredictionFreeze,
    HumanPredictionSet,
    SymbolicModelReference,
)
from hdmatch.human.splits import PersonSplitManifest
from hdmatch.util import sha256_json


class HumanBlindCohort(BaseModel):
    """Response-only cases bound to one frozen protocol and candidate universe."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-blind-cohort-v1", "human-blind-cohort-v2"] = (
        "human-blind-cohort-v1"
    )
    protocol_id: str = Field(min_length=1)
    protocol_sha256: str = Field(pattern=SHA256_PATTERN)
    cohort: Cohort
    candidate_universe_sha256: str = Field(pattern=SHA256_PATTERN)
    cases: tuple[HumanBlindCase, ...]

    @model_validator(mode="after")
    def validate_cases(self) -> HumanBlindCohort:
        identifiers = [case.participant_id for case in self.cases]
        if not identifiers or len(identifiers) != len(set(identifiers)):
            raise ValueError("blind cohort participants must be nonempty and unique")
        if any(case.cohort != self.cohort for case in self.cases):
            raise ValueError("blind cases must all match the declared cohort")
        if self.schema_version == "human-blind-cohort-v2":
            missing_records = sorted(
                case.participant_id
                for case in self.cases
                if case.responses and not case.response_records
            )
            if missing_records:
                raise ValueError(
                    "v2 blind cohort requires typed response records: " f"{missing_records}"
                )
        elif any(case.response_records for case in self.cases):
            raise ValueError("typed response records require human-blind-cohort-v2")
        if self.candidate_universe_sha256 != candidate_universe_sha256(self.cases):
            raise ValueError("blind cohort candidate-universe hash is incorrect")
        return self

    @property
    def blind_input_sha256(self) -> str:
        return sha256_json(
            [
                case.hash_payload()
                for case in sorted(self.cases, key=lambda item: item.participant_id)
            ]
        )


def candidate_universe_sha256(cases: tuple[HumanBlindCase, ...]) -> str:
    """Hash candidate identities/features without including behavioral responses."""

    return sha256_json(
        [
            {
                "participant_id": case.participant_id,
                "candidates": [candidate.hash_payload() for candidate in case.candidates],
            }
            for case in sorted(cases, key=lambda item: item.participant_id)
        ]
    )


class HumanCandidateSet(BaseModel):
    """One participant's public candidates, with no field capable of declaring truth."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    participant_id: str = Field(min_length=1)
    candidates: tuple[HumanCandidate, ...] = Field(min_length=1)

    @field_validator("participant_id")
    @classmethod
    def reject_blank_participant_id(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("participant_id cannot be blank")
        return normalized

    @model_validator(mode="after")
    def unique_candidates(self) -> HumanCandidateSet:
        identifiers = [candidate.candidate_id for candidate in self.candidates]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("candidate IDs must be unique within each participant universe")
        return self


class HumanCandidateUniverse(BaseModel):
    """Caller-supplied public candidates bound to one already frozen protocol."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-candidate-universe-v1"] = (
        "human-candidate-universe-v1"
    )
    protocol_id: str = Field(min_length=1)
    protocol_sha256: str = Field(pattern=SHA256_PATTERN)
    cohort: Cohort
    cases: tuple[HumanCandidateSet, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def unique_people(self) -> HumanCandidateUniverse:
        identifiers = [case.participant_id for case in self.cases]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("candidate universe participant IDs must be unique")
        return self

    @property
    def candidate_universe_sha256(self) -> str:
        return sha256_json(
            [
                {
                    "participant_id": case.participant_id,
                    "candidates": [candidate.hash_payload() for candidate in case.candidates],
                }
                for case in sorted(self.cases, key=lambda item: item.participant_id)
            ]
        )


class HumanSymbolicPrevalenceArtifact(BaseModel):
    """Frozen symbolic information weights supplied independently of human answers."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-symbolic-prevalence-v1"] = (
        "human-symbolic-prevalence-v1"
    )
    symbolic_model: SymbolicModelReference
    candidate_universe_sha256: str = Field(pattern=SHA256_PATTERN)
    prevalence_by_anchor: dict[str, float] = Field(min_length=1)
    source_artifact_sha256: str = Field(pattern=SHA256_PATTERN)
    prevalence_semantics: Literal[
        "duration-weighted-frozen-candidate-universe",
        "predeclared-external-reference-universe",
    ]
    created_at_utc: datetime

    @field_validator("prevalence_by_anchor")
    @classmethod
    def validate_prevalence(cls, value: dict[str, float]) -> dict[str, float]:
        if any(not anchor or not 0.0 < prevalence <= 1.0 for anchor, prevalence in value.items()):
            raise ValueError("symbolic prevalence values must be within (0, 1]")
        return dict(sorted(value.items()))

    @field_validator("created_at_utc")
    @classmethod
    def normalize_created_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("symbolic prevalence timestamp must be timezone-aware")
        return value.astimezone(UTC)


HumanWorkflowStage = Literal[
    "import",
    "prepare-blind-cohort",
    "fit-development",
    "freeze-protocol",
    "seal-answer-key",
    "blind-score",
    "freeze-predictions",
    "reveal-evaluate",
]


class HumanWorkflowReceipt(BaseModel):
    """Exact input/output hashes and software provenance for one immutable stage."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-workflow-receipt-v1"] = "human-workflow-receipt-v1"
    stage: HumanWorkflowStage
    artifact_id: str = Field(min_length=1)
    input_sha256: dict[str, str] = Field(min_length=1)
    output_sha256: dict[str, str] = Field(min_length=1)
    software_commit: str
    software_dirty: bool
    software_environment: SoftwareEnvironment
    answer_key_accessed: bool
    claim_boundary: str = Field(min_length=1)
    created_at_utc: datetime

    @field_validator("input_sha256", "output_sha256")
    @classmethod
    def validate_hashes(cls, value: dict[str, str]) -> dict[str, str]:
        for name, digest in value.items():
            if not name or len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
                raise ValueError(f"invalid SHA-256 binding for {name!r}")
        return dict(sorted(value.items()))

    @field_validator("created_at_utc")
    @classmethod
    def normalize_created_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("workflow receipt timestamp must be timezone-aware")
        return value.astimezone(UTC)


class FinalTestReleaseReceipt(BaseModel):
    """Durable one-release receipt scoped to the caller's append-only ledger directory."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-final-test-release-receipt-v1"] = (
        "human-final-test-release-receipt-v1"
    )
    final_test_release_id: str = Field(min_length=1)
    protocol_id: str = Field(min_length=1)
    protocol_sha256: str = Field(pattern=SHA256_PATTERN)
    model_bundle_sha256: str = Field(pattern=SHA256_PATTERN)
    split_manifest_sha256: str = Field(pattern=SHA256_PATTERN)
    participant_ids_sha256: str = Field(pattern=SHA256_PATTERN)
    participant_count: int = Field(gt=0)
    release_acknowledgement: Literal[
        "authorize-frozen-model-untouched-final-test-release"
    ] = FINAL_TEST_RELEASE_ACKNOWLEDGEMENT
    created_at_utc: datetime
    warning: Literal[
        "one-time uniqueness is enforced only within this durable ledger directory"
    ] = "one-time uniqueness is enforced only within this durable ledger directory"

    @field_validator("created_at_utc")
    @classmethod
    def normalize_created_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("final-test release timestamp must be timezone-aware")
        return value.astimezone(UTC)


class HumanRevealReceipt(BaseModel):
    """Post-freeze receipt; answer-key content is never copied into the run directory."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-answer-key-reveal-receipt-v1"] = (
        "human-answer-key-reveal-receipt-v1"
    )
    protocol_sha256: str = Field(pattern=SHA256_PATTERN)
    prediction_freeze_sha256: str = Field(pattern=SHA256_PATTERN)
    answer_key_sha256: str = Field(pattern=SHA256_PATTERN)
    report_sha256: str = Field(pattern=SHA256_PATTERN)
    revealed_at_utc: datetime
    answer_key_revealed: Literal[True] = True

    @field_validator("revealed_at_utc")
    @classmethod
    def normalize_revealed_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("human reveal timestamp must be timezone-aware")
        return value.astimezone(UTC)


class FinalTestFreezeLedgerReceipt(BaseModel):
    """Single prediction-freeze claim for one final-test release."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-final-test-freeze-ledger-v1"] = (
        "human-final-test-freeze-ledger-v1"
    )
    final_test_release_id: str = Field(min_length=1)
    protocol_sha256: str = Field(pattern=SHA256_PATTERN)
    prediction_sha256: str = Field(pattern=SHA256_PATTERN)
    prediction_freeze_sha256: str = Field(pattern=SHA256_PATTERN)
    frozen_at_utc: datetime

    @field_validator("frozen_at_utc")
    @classmethod
    def normalize_frozen_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("final-test freeze timestamp must be timezone-aware")
        return value.astimezone(UTC)


class FinalTestRevealLedgerReceipt(BaseModel):
    """Single reveal/evaluation claim for one final-test release."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["human-final-test-reveal-ledger-v1"] = (
        "human-final-test-reveal-ledger-v1"
    )
    final_test_release_id: str = Field(min_length=1)
    protocol_sha256: str = Field(pattern=SHA256_PATTERN)
    prediction_freeze_sha256: str = Field(pattern=SHA256_PATTERN)
    encrypted_answer_key_sha256: str = Field(pattern=SHA256_PATTERN)
    comparison_report_sha256: str = Field(pattern=SHA256_PATTERN)
    revealed_at_utc: datetime

    @field_validator("revealed_at_utc")
    @classmethod
    def normalize_revealed_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("final-test reveal timestamp must be timezone-aware")
        return value.astimezone(UTC)


def load_canonical_model(path: str | Path, model_type: type[BaseModel]) -> BaseModel:
    """Validate a canonical JSON artifact against a strict Pydantic model."""

    return model_type.model_validate(load_json_bytes(path, require_canonical=True))


def load_human_dataset_artifact(path: str | Path) -> HumanDataset:
    return HumanDataset.model_validate(load_json_bytes(path, require_canonical=True))


def load_split_manifest(path: str | Path) -> PersonSplitManifest:
    return PersonSplitManifest.model_validate(load_json_bytes(path, require_canonical=True))


def load_model_bundle(path: str | Path) -> FrozenHumanModelBundle:
    return FrozenHumanModelBundle.model_validate(load_json_bytes(path, require_canonical=True))


def load_evaluation_protocol(path: str | Path) -> FrozenHumanEvaluationProtocol:
    return FrozenHumanEvaluationProtocol.model_validate(
        load_json_bytes(path, require_canonical=True)
    )


def load_blind_cohort(path: str | Path) -> HumanBlindCohort:
    return HumanBlindCohort.model_validate(load_json_bytes(path, require_canonical=True))


def load_candidate_universe(path: str | Path) -> HumanCandidateUniverse:
    return HumanCandidateUniverse.model_validate(load_json_bytes(path, require_canonical=True))


def load_symbolic_prevalence(path: str | Path) -> HumanSymbolicPrevalenceArtifact:
    return HumanSymbolicPrevalenceArtifact.model_validate(
        load_json_bytes(path, require_canonical=True)
    )


def load_human_predictions(path: str | Path) -> HumanPredictionSet:
    return HumanPredictionSet.model_validate(load_json_bytes(path, require_canonical=True))


def load_human_prediction_freeze(path: str | Path) -> HumanPredictionFreeze:
    return HumanPredictionFreeze.model_validate(load_json_bytes(path, require_canonical=True))


def load_human_answer_key(path: str | Path) -> HumanCohortAnswerKey:
    return HumanCohortAnswerKey.model_validate(load_json_bytes(path, require_canonical=True))


def load_comparison_report(path: str | Path) -> HumanComparisonReport:
    return HumanComparisonReport.model_validate(load_json_bytes(path, require_canonical=True))


def write_workflow_receipt(
    path: str | Path,
    *,
    stage: HumanWorkflowStage,
    artifact_id: str,
    input_sha256: dict[str, str],
    output_sha256: dict[str, str],
    repository_root: str | Path,
    answer_key_accessed: bool,
    claim_boundary: str,
    created_at_utc: datetime | None = None,
) -> HumanWorkflowReceipt:
    commit, dirty = git_revision(repository_root)
    receipt = HumanWorkflowReceipt(
        stage=stage,
        artifact_id=artifact_id,
        input_sha256=input_sha256,
        output_sha256=output_sha256,
        software_commit=commit,
        software_dirty=dirty,
        software_environment=capture_software_environment(),
        answer_key_accessed=answer_key_accessed,
        claim_boundary=claim_boundary,
        created_at_utc=created_at_utc or datetime.now(UTC),
    )
    write_new_canonical_json(path, receipt)
    return receipt


def release_receipt_path(ledger_dir: str | Path, release_id: str) -> Path:
    digest = hashlib.sha256(release_id.encode("utf-8")).hexdigest()
    return Path(ledger_dir) / f"{digest}.final-test-release.json"


def final_test_freeze_ledger_path(ledger_dir: str | Path, release_id: str) -> Path:
    digest = hashlib.sha256(release_id.encode("utf-8")).hexdigest()
    return Path(ledger_dir) / f"{digest}.final-test-freeze.json"


def final_test_reveal_ledger_path(ledger_dir: str | Path, release_id: str) -> Path:
    digest = hashlib.sha256(release_id.encode("utf-8")).hexdigest()
    return Path(ledger_dir) / f"{digest}.final-test-reveal.json"


def final_test_cohort_lock_path(
    ledger_dir: str | Path,
    protocol: FrozenHumanEvaluationProtocol,
) -> Path:
    digest = sha256_json(tuple(sorted(protocol.participant_ids)))
    return Path(ledger_dir) / f"{digest}.final-test-cohort-lock.json"


def write_final_test_release_receipt(
    ledger_dir: str | Path,
    protocol: FrozenHumanEvaluationProtocol,
    *,
    created_at_utc: datetime | None = None,
) -> tuple[Path, FinalTestReleaseReceipt]:
    """Claim one release ID in an append-only ledger before final-test scoring."""

    if protocol.cohort != "final_test" or protocol.final_test_release_id is None:
        raise ValueError("release receipts require a final-test protocol")
    timestamp = created_at_utc or datetime.now(UTC)
    if timestamp < protocol.created_at_utc:
        raise ValueError("final-test release receipt cannot predate protocol")
    receipt = FinalTestReleaseReceipt(
        final_test_release_id=protocol.final_test_release_id,
        protocol_id=protocol.protocol_id,
        protocol_sha256=protocol.sha256,
        model_bundle_sha256=protocol.model_bundle_sha256,
        split_manifest_sha256=protocol.split_manifest_sha256,
        participant_ids_sha256=sha256_json(tuple(sorted(protocol.participant_ids))),
        participant_count=len(protocol.participant_ids),
        created_at_utc=timestamp,
    )
    # The cohort lock prevents bypassing single use by renaming the release ID.
    cohort_lock = final_test_cohort_lock_path(ledger_dir, protocol)
    write_new_canonical_json(cohort_lock, receipt)
    destination = release_receipt_path(ledger_dir, protocol.final_test_release_id)
    write_new_canonical_json(destination, receipt)
    return destination, receipt


def verify_final_test_release_receipt(
    ledger_dir: str | Path,
    protocol: FrozenHumanEvaluationProtocol,
) -> FinalTestReleaseReceipt:
    if protocol.cohort != "final_test" or protocol.final_test_release_id is None:
        raise ValueError("final-test release verification requires a final-test protocol")
    destination = release_receipt_path(ledger_dir, protocol.final_test_release_id)
    receipt = FinalTestReleaseReceipt.model_validate(
        load_json_bytes(destination, require_canonical=True)
    )
    cohort_lock = FinalTestReleaseReceipt.model_validate(
        load_json_bytes(
            final_test_cohort_lock_path(ledger_dir, protocol),
            require_canonical=True,
        )
    )
    if cohort_lock != receipt:
        raise ValueError("final-test release and cohort-lock receipts disagree")
    expected = {
        "final_test_release_id": protocol.final_test_release_id,
        "protocol_id": protocol.protocol_id,
        "protocol_sha256": protocol.sha256,
        "model_bundle_sha256": protocol.model_bundle_sha256,
        "split_manifest_sha256": protocol.split_manifest_sha256,
        "participant_ids_sha256": sha256_json(tuple(sorted(protocol.participant_ids))),
        "participant_count": len(protocol.participant_ids),
    }
    for field, value in expected.items():
        if getattr(receipt, field) != value:
            raise ValueError(f"final-test release receipt has mismatched {field}")
    if receipt.created_at_utc < protocol.created_at_utc:
        raise ValueError("final-test release receipt predates protocol")
    return receipt


def write_final_test_freeze_ledger_receipt(
    ledger_dir: str | Path,
    protocol: FrozenHumanEvaluationProtocol,
    freeze: HumanPredictionFreeze,
) -> tuple[Path, FinalTestFreezeLedgerReceipt]:
    release = verify_final_test_release_receipt(ledger_dir, protocol)
    if protocol.final_test_release_id is None:
        raise ValueError("final-test protocol has no release ID")
    if freeze.created_at_utc < release.created_at_utc:
        raise ValueError("final-test freeze cannot predate release receipt")
    receipt = FinalTestFreezeLedgerReceipt(
        final_test_release_id=protocol.final_test_release_id,
        protocol_sha256=protocol.sha256,
        prediction_sha256=freeze.prediction_sha256,
        prediction_freeze_sha256=sha256_json(freeze),
        frozen_at_utc=freeze.created_at_utc,
    )
    destination = final_test_freeze_ledger_path(
        ledger_dir,
        protocol.final_test_release_id,
    )
    write_new_canonical_json(destination, receipt)
    return destination, receipt


def verify_final_test_freeze_ledger_receipt(
    ledger_dir: str | Path,
    protocol: FrozenHumanEvaluationProtocol,
    freeze: HumanPredictionFreeze,
) -> FinalTestFreezeLedgerReceipt:
    verify_final_test_release_receipt(ledger_dir, protocol)
    if protocol.final_test_release_id is None:
        raise ValueError("final-test protocol has no release ID")
    destination = final_test_freeze_ledger_path(
        ledger_dir,
        protocol.final_test_release_id,
    )
    receipt = FinalTestFreezeLedgerReceipt.model_validate(
        load_json_bytes(destination, require_canonical=True)
    )
    if receipt.protocol_sha256 != protocol.sha256:
        raise ValueError("final-test freeze ledger protocol binding is incorrect")
    if receipt.prediction_sha256 != freeze.prediction_sha256:
        raise ValueError("final-test freeze ledger prediction binding is incorrect")
    if receipt.prediction_freeze_sha256 != sha256_json(freeze):
        raise ValueError("final-test freeze ledger freeze binding is incorrect")
    if receipt.frozen_at_utc != freeze.created_at_utc:
        raise ValueError("final-test freeze ledger timestamp is incorrect")
    return receipt


def assert_final_test_reveal_unused(
    ledger_dir: str | Path,
    protocol: FrozenHumanEvaluationProtocol,
) -> None:
    if protocol.final_test_release_id is None:
        raise ValueError("final-test protocol has no release ID")
    path = final_test_reveal_ledger_path(ledger_dir, protocol.final_test_release_id)
    if path.exists():
        raise FileExistsError("final-test release has already been revealed/evaluated")


def write_final_test_reveal_ledger_receipt(
    ledger_dir: str | Path,
    protocol: FrozenHumanEvaluationProtocol,
    freeze: HumanPredictionFreeze,
    *,
    encrypted_answer_key_sha256: str,
    comparison_report_sha256: str,
    revealed_at_utc: datetime,
) -> tuple[Path, FinalTestRevealLedgerReceipt]:
    verify_final_test_freeze_ledger_receipt(ledger_dir, protocol, freeze)
    if protocol.final_test_release_id is None:
        raise ValueError("final-test protocol has no release ID")
    if revealed_at_utc < freeze.created_at_utc:
        raise ValueError("final-test reveal cannot predate freeze")
    receipt = FinalTestRevealLedgerReceipt(
        final_test_release_id=protocol.final_test_release_id,
        protocol_sha256=protocol.sha256,
        prediction_freeze_sha256=sha256_json(freeze),
        encrypted_answer_key_sha256=encrypted_answer_key_sha256,
        comparison_report_sha256=comparison_report_sha256,
        revealed_at_utc=revealed_at_utc,
    )
    destination = final_test_reveal_ledger_path(
        ledger_dir,
        protocol.final_test_release_id,
    )
    write_new_canonical_json(destination, receipt)
    return destination, receipt


def exact_file_hashes(**paths: str | Path) -> dict[str, str]:
    return {name: sha256_file(path) for name, path in paths.items()}
