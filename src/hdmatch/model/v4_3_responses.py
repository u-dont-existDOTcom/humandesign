"""Frozen direct-target response artifacts for canonical V4.3 cache runs.

The compiler is deliberately mechanical: it audits every compiled direct-target
response rule and selects either its support token or its predeclared opposing
token according to the frozen response-rule polarity.  It has no candidate,
rank, score, or outcome input.
"""

from __future__ import annotations

import json
from enum import StrEnum
from pathlib import Path
from typing import Final, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    sha256_bytes,
    sha256_file,
    sha256_json,
    write_new_canonical_json,
)
from hdmatch.model.v4_3.integration import V43ObservedResponse
from hdmatch.model.v4_3_compiler import compile_verified_mapping_library_v2
from hdmatch.model.v4_3_mapping import (
    CompiledMappingRuleV2,
    ContradictionModeV2,
    MappingLibrarySourceV2,
    MappingLibraryV2,
    MappingV2Error,
    ResponseSourceModeV2,
)

SHA256_PATTERN: Final[str] = r"^[a-f0-9]{64}$"
LESS_CONTAMINATED_RESPONSE_PATH: Final[str] = (
    "mappings/v4_3_v3_6_less_contaminated_direct_target_responses_v2.json"
)
BEST_CURRENT_RESPONSE_PATH: Final[str] = (
    "mappings/v4_3_v3_6_best_current_direct_target_responses_v2.json"
)
CANONICAL_VARIANT_SOURCE_SHA256: Final[
    dict[Literal["less_contaminated", "best_current_descriptive"], str]
] = {
    "less_contaminated": (
        "3a380b0de83965e3c46099909f7b5e8d403b47d50e26632ac5bf854fa69d2e05"
    ),
    "best_current_descriptive": (
        "6e2b4317f25f49995e24afc920442de66916f3e91846517793b0abd616a58439"
    ),
}


class V43ResponseArtifactError(ValueError):
    """A response artifact is not a mechanical binding of its frozen sources."""


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class V43ObservedTargetPolarityV2(StrEnum):
    SUPPORT = "support"
    CONTRADICTION = "contradiction"


class V43FrozenObservedTargetResponseV2(_FrozenModel):
    observation_id: str = Field(min_length=1)
    response_dimension_id: str = Field(min_length=1)
    observed_target_response_token: str = Field(min_length=1)
    observed_target_polarity: V43ObservedTargetPolarityV2
    polarity_derivation: Literal["compiled-direct-target-response-rule-v2"] = (
        "compiled-direct-target-response-rule-v2"
    )
    source_rule_id: str = Field(min_length=1)


class V43DirectTargetResponseArtifactV2(_FrozenModel):
    """One immutable direct-target response set bound to one mapping variant."""

    schema_version: Literal["v4-3-direct-target-response-artifact-v2"] = (
        "v4-3-direct-target-response-artifact-v2"
    )
    protocol_version: Literal["V4.3"] = "V4.3"
    behavioral_target_version: Literal["V3.6"] = "V3.6"
    variant: Literal["less_contaminated", "best_current_descriptive"]
    response_source_mode: Literal["direct_behavioral_target"] = (
        "direct_behavioral_target"
    )
    behavioral_target_source_id: str = Field(min_length=1)
    behavioral_target_path: str = Field(min_length=1)
    behavioral_target_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_library_path: str = Field(min_length=1)
    mapping_library_sha256: str = Field(pattern=SHA256_PATTERN)
    mapping_source_library_path: str = Field(min_length=1)
    mapping_source_library_sha256: str = Field(pattern=SHA256_PATTERN)
    question_bank_source_id: None = None
    question_bank_sha256: None = None
    observations: tuple[V43FrozenObservedTargetResponseV2, ...] = Field(
        min_length=1
    )
    support_observation_count: int = Field(ge=0)
    contradiction_observation_count: int = Field(ge=0)
    polarity_audit_sha256: str = Field(pattern=SHA256_PATTERN)
    response_set_sha256: str = Field(pattern=SHA256_PATTERN)
    outcome_data_used: Literal[False] = False

    @model_validator(mode="after")
    def require_mechanical_direct_target_inventory(
        self,
    ) -> V43DirectTargetResponseArtifactV2:
        observation_ids = tuple(item.observation_id for item in self.observations)
        if observation_ids != tuple(sorted(set(observation_ids))):
            raise ValueError("direct-target observations must be sorted and unique")
        if self.response_set_sha256 != _response_set_sha256(self.observations):
            raise ValueError("direct-target response-set hash is inconsistent")
        support_count = sum(
            item.observed_target_polarity is V43ObservedTargetPolarityV2.SUPPORT
            for item in self.observations
        )
        contradiction_count = len(self.observations) - support_count
        if (
            self.support_observation_count != support_count
            or self.contradiction_observation_count != contradiction_count
        ):
            raise ValueError("direct-target polarity counts are inconsistent")
        if self.polarity_audit_sha256 != _polarity_audit_sha256(
            self.observations
        ):
            raise ValueError("direct-target polarity audit hash is inconsistent")
        return self

    def sha256(self) -> str:
        return sha256_json(self.model_dump(mode="json"))

    def observed_responses(self) -> tuple[V43ObservedResponse, ...]:
        return tuple(
            V43ObservedResponse(
                observation_id=item.observation_id,
                response_token=item.observed_target_response_token,
            )
            for item in self.observations
        )


class VerifiedV43DirectTargetResponses:
    """Nominal capability minted only after exact-byte source replay."""

    __slots__ = ("_token", "artifact", "artifact_sha256")

    def __init__(
        self,
        *,
        artifact: V43DirectTargetResponseArtifactV2,
        artifact_sha256: str,
        _token: object,
    ) -> None:
        if _token is not _VERIFIED_RESPONSE_TOKEN:
            raise V43ResponseArtifactError(
                "verified direct-target responses require source replay"
            )
        self.artifact = artifact
        self.artifact_sha256 = artifact_sha256
        self._token = _token


_VERIFIED_RESPONSE_TOKEN: Final[object] = object()


def compile_v4_3_direct_target_responses(
    *,
    repository_root: str | Path,
    mapping_library_path: str | Path,
    mapping_source_library_path: str | Path,
    variant: Literal["less_contaminated", "best_current_descriptive"],
) -> V43DirectTargetResponseArtifactV2:
    """Compile canonical target responses without accepting any outcome input."""

    root = Path(repository_root).resolve()
    compiled_path = _inside_root(root, mapping_library_path)
    source_path = _inside_root(root, mapping_source_library_path)
    compiled_raw = _canonical_bytes(compiled_path, "compiled mapping library")
    source_raw = _canonical_bytes(source_path, "mapping source library")
    source_sha256 = sha256_bytes(source_raw)
    if source_sha256 != CANONICAL_VARIANT_SOURCE_SHA256[variant]:
        raise V43ResponseArtifactError(
            "mapping source bytes do not match the declared canonical V3.6 variant"
        )
    try:
        compiled = MappingLibraryV2.model_validate_json(compiled_raw, strict=True)
        source = MappingLibrarySourceV2.model_validate_json(source_raw, strict=True)
        independently_compiled = compile_verified_mapping_library_v2(
            source,
            repository_root=root,
        )
    except (ValueError, MappingV2Error) as exc:
        raise V43ResponseArtifactError("mapping source replay failed") from exc
    if compiled != independently_compiled:
        raise V43ResponseArtifactError(
            "compiled mapping library differs from verified source replay"
        )
    if compiled.response_source_mode is not ResponseSourceModeV2.DIRECT_BEHAVIORAL_TARGET:
        raise V43ResponseArtifactError(
            "direct-target response compilation rejects questionnaire mode"
        )
    if compiled.question_bank_source_id is not None or any(
        rule.question_ids for rule in compiled.rules
    ):
        raise V43ResponseArtifactError(
            "direct-target mappings cannot claim questionnaire item linkage"
        )
    target_source = next(
        (
            item
            for item in compiled.source_artifacts
            if item.source_id == compiled.behavioral_target_source_id
        ),
        None,
    )
    if target_source is None:
        raise V43ResponseArtifactError("behavioral target source binding is missing")
    target_path = _inside_root(root, target_source.path)
    if sha256_file(target_path) != target_source.sha256:
        raise V43ResponseArtifactError("behavioral target source hash mismatch")
    observations = tuple(
        sorted(
            (
                _compile_observed_target_response(rule)
                for rule in compiled.rules
            ),
            key=lambda item: item.observation_id,
        )
    )
    support_count = sum(
        item.observed_target_polarity is V43ObservedTargetPolarityV2.SUPPORT
        for item in observations
    )
    return V43DirectTargetResponseArtifactV2(
        variant=variant,
        behavioral_target_source_id=compiled.behavioral_target_source_id,
        behavioral_target_path=target_source.path,
        behavioral_target_sha256=target_source.sha256,
        mapping_library_path=compiled_path.relative_to(root).as_posix(),
        mapping_library_sha256=sha256_bytes(compiled_raw),
        mapping_source_library_path=source_path.relative_to(root).as_posix(),
        mapping_source_library_sha256=source_sha256,
        observations=observations,
        support_observation_count=support_count,
        contradiction_observation_count=len(observations) - support_count,
        polarity_audit_sha256=_polarity_audit_sha256(observations),
        response_set_sha256=_response_set_sha256(observations),
    )


def _compile_observed_target_response(
    rule: CompiledMappingRuleV2,
) -> V43FrozenObservedTargetResponseV2:
    """Select polarity solely from the already-compiled direct-target rule."""

    response_rule = rule.response_rule
    if response_rule.contradiction.mode is ContradictionModeV2.DIRECT_OPPOSITION:
        if len(response_rule.contradiction.opposing_response_tokens) != 1:
            raise V43ResponseArtifactError(
                "direct-target contradiction must declare exactly one observed token"
            )
        token = response_rule.contradiction.opposing_response_tokens[0]
        polarity = V43ObservedTargetPolarityV2.CONTRADICTION
    else:
        token = response_rule.canonical_response_token
        polarity = V43ObservedTargetPolarityV2.SUPPORT
    return V43FrozenObservedTargetResponseV2(
        observation_id=rule.observation_id,
        response_dimension_id=response_rule.response_dimension_id,
        observed_target_response_token=token,
        observed_target_polarity=polarity,
        source_rule_id=rule.rule_id,
    )


def write_v4_3_direct_target_responses_new(
    path: str | Path,
    artifact: V43DirectTargetResponseArtifactV2,
) -> Path:
    return write_new_canonical_json(path, artifact)


def verify_v4_3_direct_target_responses(
    artifact_path: str | Path,
    *,
    repository_root: str | Path,
    mapping_library_path: str | Path,
    mapping_source_library_path: str | Path,
) -> VerifiedV43DirectTargetResponses:
    """Replay the mapping and target bytes before minting a response capability."""

    path = Path(artifact_path)
    raw = _canonical_bytes(path, "direct-target response artifact")
    try:
        artifact = V43DirectTargetResponseArtifactV2.model_validate_json(
            raw,
            strict=True,
        )
    except ValueError as exc:
        raise V43ResponseArtifactError("invalid direct-target response artifact") from exc
    expected = compile_v4_3_direct_target_responses(
        repository_root=repository_root,
        mapping_library_path=mapping_library_path,
        mapping_source_library_path=mapping_source_library_path,
        variant=artifact.variant,
    )
    if artifact != expected:
        raise V43ResponseArtifactError(
            "direct-target response artifact differs from source replay"
        )
    if path.read_bytes() != raw:
        raise V43ResponseArtifactError(
            "direct-target response artifact changed during verification"
        )
    return VerifiedV43DirectTargetResponses(
        artifact=artifact,
        artifact_sha256=sha256_bytes(raw),
        _token=_VERIFIED_RESPONSE_TOKEN,
    )


def _response_set_sha256(
    observations: tuple[V43FrozenObservedTargetResponseV2, ...],
) -> str:
    return sha256_json(
        [
            {
                "observation_id": item.observation_id,
                "response_token": item.observed_target_response_token,
            }
            for item in observations
        ]
    )


def _polarity_audit_sha256(
    observations: tuple[V43FrozenObservedTargetResponseV2, ...],
) -> str:
    return sha256_json(
        [
            item.model_dump(mode="json")
            for item in observations
        ]
    )


def _inside_root(root: Path, path: str | Path) -> Path:
    candidate = Path(path)
    resolved = (root / candidate).resolve() if not candidate.is_absolute() else candidate.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise V43ResponseArtifactError(f"artifact escapes repository root: {path}") from exc
    if not resolved.is_file():
        raise V43ResponseArtifactError(f"artifact is missing: {path}")
    return resolved


def _canonical_bytes(path: Path, label: str) -> bytes:
    try:
        raw = path.read_bytes()
        payload = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        raise V43ResponseArtifactError(f"invalid {label}: {path}") from exc
    if canonical_json_bytes(payload) != raw:
        raise V43ResponseArtifactError(f"{label} is not canonically encoded")
    return raw
