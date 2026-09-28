"""Fail-closed loader for the frozen Wave 3B empirical-astrology contract."""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DECISION_RELATIVE_PATH = Path("reference/empirical_astrology/literature_model_v1b_decision.json")
FEATURE_REGISTRY_RELATIVE_PATH = Path(
    "reference/empirical_astrology/literature_feature_registry_v1.json"
)
MODEL_RELATIVE_PATH = Path("reference/empirical_astrology/literature_model_v1.json")

EXPECTED_VERDICT = "REAFFIRM_WAVE3_AUTHORIZE_EXACT_IMPLEMENTATION_AND_DEVELOPMENT_ONLY"
EXPECTED_PRIMARY_FEATURE = "TN-001"


class ContractError(ValueError):
    """Raised when a frozen artifact is absent, changed, or internally inconsistent."""


def _reject_constant(value: str) -> None:
    raise ContractError(f"non-finite JSON value is prohibited: {value}")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"duplicate JSON key is prohibited: {key!r}")
        result[key] = value
    return result


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot read frozen artifact {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"frozen artifact must contain one JSON object: {path}")
    return value


def sha256_file(path: Path) -> str:
    """Return lowercase SHA256 for an artifact."""

    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise ContractError(f"cannot hash frozen artifact {path}: {exc}") from exc


def default_repository_root() -> Path:
    """Locate the repository from this installed source checkout."""

    return Path(__file__).resolve().parents[3]


@dataclass(frozen=True, slots=True)
class FrozenLiteratureContract:
    """Validated Wave 3B decision, feature registry, and executable model."""

    repository_root: Path
    decision: dict[str, Any]
    feature_registry: dict[str, Any]
    model: dict[str, Any]
    decision_sha256: str
    feature_registry_sha256: str
    model_sha256: str

    @property
    def protocol_version(self) -> str:
        return str(self.model["prospective_protocol_version"])

    @property
    def base_seed(self) -> int:
        return int(self.model["randomness_and_determinism"]["base_seed"])


def _require_empty_astrology_surface(name: str, value: dict[str, Any]) -> None:
    expected_empty_sequences = (
        "executable_astrology_features",
        "aspect_to_trait_mappings",
        "executable_moderator_interactions",
    )
    for field in expected_empty_sequences:
        if value.get(field) != []:
            raise ContractError(f"{name}.{field} must remain an empty list")
    if value.get("astrology_weights") != {}:
        raise ContractError(f"{name}.astrology_weights must remain an empty object")
    if value.get("astrology_coefficient_vector_length") != 0:
        raise ContractError(f"{name}.astrology_coefficient_vector_length must be zero")


def load_frozen_contract(
    repository_root: Path | str | None = None,
) -> FrozenLiteratureContract:
    """Load and verify the exact Pro-authorized v1b implementation artifacts.

    This loader intentionally rejects silent edits, added astrology columns, version
    drift, unauthorized prospective collection, and missing evidence ancestry.
    """

    root = Path(repository_root) if repository_root is not None else default_repository_root()
    root = root.resolve()
    decision_path = root / DECISION_RELATIVE_PATH
    feature_path = root / FEATURE_REGISTRY_RELATIVE_PATH
    model_path = root / MODEL_RELATIVE_PATH
    decision = _load_json(decision_path)
    registry = _load_json(feature_path)
    model = _load_json(model_path)
    decision_sha = sha256_file(decision_path)
    feature_sha = sha256_file(feature_path)
    model_sha = sha256_file(model_path)

    if decision.get("verdict") != EXPECTED_VERDICT:
        raise ContractError("the Pro verdict does not authorize this implementation")
    authorization = decision.get("work_authorization")
    if not isinstance(authorization, dict):
        raise ContractError("decision.work_authorization is missing")
    if authorization.get("implementation_authorized") is not True:
        raise ContractError("implementation is not authorized")
    if authorization.get("development_evaluation_authorized") is not True:
        raise ContractError("development evaluation is not authorized")
    if authorization.get("prospective_recruitment_or_outcome_collection_authorized") is not False:
        raise ContractError("prospective collection boundary changed")
    if authorization.get("production_or_person_level_use_authorized") is not False:
        raise ContractError("production/person-level boundary changed")

    source_decision = model.get("source_decision")
    if not isinstance(source_decision, dict) or source_decision.get("sha256") != decision_sha:
        raise ContractError("model decision hash does not match the frozen decision")
    source_registry = model.get("feature_registry")
    if not isinstance(source_registry, dict) or source_registry.get("sha256") != feature_sha:
        raise ContractError("model feature-registry hash does not match the frozen registry")
    registry_source = registry.get("source_decision")
    if not isinstance(registry_source, dict) or registry_source.get("sha256") != decision_sha:
        raise ContractError("feature registry decision hash does not match")

    version = decision.get("frozen_version_identifier")
    if registry.get("registry_version") != version or model.get("model_version") != version:
        raise ContractError("decision, feature-registry, and model versions differ")
    if model.get("prospective_protocol_version") != decision.get("prospective_protocol_version"):
        raise ContractError("prospective protocol version differs from the Pro decision")
    if model.get("primary_feature_id") != EXPECTED_PRIMARY_FEATURE:
        raise ContractError("TN-001 must remain the sole primary feature")
    primary = registry.get("primary_features")
    if not isinstance(primary, list) or len(primary) != 1:
        raise ContractError("feature registry must contain exactly one primary feature")
    if primary[0].get("feature_id") != EXPECTED_PRIMARY_FEATURE:
        raise ContractError("feature registry primary feature must be TN-001")

    _require_empty_astrology_surface("feature_registry", registry)
    _require_empty_astrology_surface("model", model)
    terms = decision.get("exact_moderator_interaction_terms")
    weights = decision.get("weighting_policy")
    if not isinstance(terms, dict) or terms.get("v1b_executable_terms") != []:
        raise ContractError("decision executable moderator list is not empty")
    if terms.get("aspect_to_trait_mappings") != []:
        raise ContractError("decision aspect-to-trait mappings are not empty")
    if not isinstance(weights, dict) or weights.get("astrology_weights") != {}:
        raise ContractError("decision astrology weights are not empty")
    if weights.get("astrology_coefficient_vector_length") != 0:
        raise ContractError("decision astrology coefficient vector is not empty")

    review_base = decision.get("review_base_commit")
    if source_decision.get("review_base_commit") != review_base:
        raise ContractError("model and decision evidence checkpoints differ")
    if registry_source.get("review_base_commit") != review_base:
        raise ContractError("registry and decision evidence checkpoints differ")
    if authorization.get("required_evidence_ancestor") != review_base:
        raise ContractError("authorization evidence ancestor differs from the review base")

    return FrozenLiteratureContract(
        repository_root=root,
        decision=decision,
        feature_registry=registry,
        model=model,
        decision_sha256=decision_sha,
        feature_registry_sha256=feature_sha,
        model_sha256=model_sha,
    )


def verify_required_git_ancestor(contract: FrozenLiteratureContract) -> None:
    """Fail unless the checked-out commit descends from the reviewed evidence commit."""

    required = str(contract.decision["work_authorization"]["required_evidence_ancestor"])
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", required, "HEAD"],
        cwd=contract.repository_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or "required commit is not an ancestor of HEAD"
        raise ContractError(f"evidence ancestry check failed: {detail}")
