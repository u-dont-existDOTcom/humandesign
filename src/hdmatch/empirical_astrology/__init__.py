"""Frozen empirical-astrology research implementation and dormant calculators.

``LiteratureModelV1`` is the assembled Pro-authorized surface.  It contains the
theory-neutral TN-001 feature only.  Geometry and karaka helpers remain exposed
as unweighted research primitives; the assembled model never imports or invokes
them and has no astrology feature, mapping, interaction, or coefficient.
"""

from .contract import (
    ContractError,
    FrozenLiteratureContract,
    load_frozen_contract,
    verify_required_git_ancestor,
)
from .features import (
    NUISANCE_COLUMN_NAMES,
    BirthRecord,
    GapBounds,
    PairEligibilityError,
    PairFeatures,
    birth_gap_bounds,
    build_pair_features,
    deterministic_pair_id,
    deterministic_random_feature,
    entity_hash,
    pair_eligibility_errors,
    validate_identifier,
)
from .geometry import (
    AspectPhase,
    aspect_phase_from_forward_step,
    distance_to_aspect,
    minimum_axis_distance,
    near_time_distance_minutes,
    unsigned_angular_separation,
)
from .karaka import (
    KarakaKendraResult,
    karaka_kendra_feature,
    navamsa_sign_index,
    rank_seven_karakas,
    rasi_sign_index,
    within_sign_degree,
)
from .model import LiteratureModelV1
from .outcome import (
    SCALE_ORDER,
    ipip_pair_distance,
    responses_to_pair_distance,
    score_ipip50,
    validate_ipip50_responses,
)
from .pairing import (
    DesignNotLaunchable,
    HospitalPairSelection,
    allocate_networks_to_cohorts,
    greedy_disjoint_pairs,
    retain_one_hospital_per_network,
    retain_one_per_relationship_component,
    select_hospital_pairs,
)
from .protocol import (
    CohortEntities,
    FreezeManifestError,
    ensure_disjoint_cohorts,
    holm_family,
    require_exact_diagnostic_family,
    validate_freeze_manifest,
)

__all__ = [
    "AspectPhase",
    "BirthRecord",
    "CohortEntities",
    "ContractError",
    "DesignNotLaunchable",
    "FreezeManifestError",
    "FrozenLiteratureContract",
    "GapBounds",
    "HospitalPairSelection",
    "KarakaKendraResult",
    "LiteratureModelV1",
    "NUISANCE_COLUMN_NAMES",
    "PairEligibilityError",
    "PairFeatures",
    "SCALE_ORDER",
    "allocate_networks_to_cohorts",
    "aspect_phase_from_forward_step",
    "birth_gap_bounds",
    "build_pair_features",
    "deterministic_pair_id",
    "deterministic_random_feature",
    "distance_to_aspect",
    "ensure_disjoint_cohorts",
    "entity_hash",
    "greedy_disjoint_pairs",
    "holm_family",
    "ipip_pair_distance",
    "karaka_kendra_feature",
    "load_frozen_contract",
    "minimum_axis_distance",
    "navamsa_sign_index",
    "near_time_distance_minutes",
    "pair_eligibility_errors",
    "rank_seven_karakas",
    "require_exact_diagnostic_family",
    "responses_to_pair_distance",
    "retain_one_hospital_per_network",
    "retain_one_per_relationship_component",
    "rasi_sign_index",
    "score_ipip50",
    "select_hospital_pairs",
    "unsigned_angular_separation",
    "validate_freeze_manifest",
    "validate_identifier",
    "validate_ipip50_responses",
    "verify_required_git_ancestor",
    "within_sign_degree",
]
