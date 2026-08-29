"""Build pre-answer relationship prediction freezes without outcome leakage."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from hdmatch.chart.timezone import resolve_local_datetime

from .study import (
    NoisePolicyBinding,
    PredictionLayerFreeze,
    PredictionLayerStatus,
    RelationshipBirthInput,
    RelationshipPredictionFreeze,
    RelationshipStudyIntake,
    canonical_sha256,
    file_sha256,
)

HD_LAYER_ID = "human_design_connection_v1"
ASTRO_RRF_LAYER_ID = "astro_rrf_directional_v0_4"
HD_MODEL_VERSION = "hd-partnership-mechanics-v1"
ASTRO_RRF_MODEL_VERSION = "astro-rrf-v0.1-through-v0.4-frozen-family"

ASTRO_RRF_MODEL_FILES = (
    "reference/development_models/astro_rrf_directional_v0_1.json",
    "reference/development_models/astro_rrf_state_conditional_v0_2.json",
    "reference/development_models/astro_rrf_dyadic_v0_3.json",
    "docs/30_astro_rrf_novelty_habituation_v0_4.md",
)


def build_prediction_freeze(
    *,
    session_id: str,
    intake: RelationshipStudyIntake,
    repo_root: Path,
    questionnaire_path: Path,
    noise_policy: NoisePolicyBinding,
    code_commit: str,
) -> RelationshipPredictionFreeze:
    """Freeze every currently available prediction layer before behavioral capture."""

    hd_layer = _build_hd_layer(intake, repo_root=repo_root)
    astro_layer = _build_astro_rrf_layer(intake, repo_root=repo_root)
    questionnaire_abs = _under_root(repo_root, questionnaire_path)
    return RelationshipPredictionFreeze(
        session_id=session_id,
        created_at_utc=datetime.now(UTC),
        birth_input_sha256=intake.birth_input_sha256,
        layers=(hd_layer, astro_layer),
        noise_policy=noise_policy,
        questionnaire_version="relationship-dynamic-questionnaire-v1",
        questionnaire_sha256=file_sha256(questionnaire_abs),
        code_commit=code_commit,
    )


def _build_hd_layer(
    intake: RelationshipStudyIntake,
    *,
    repo_root: Path,
) -> PredictionLayerFreeze:
    model_path = repo_root / "src/hdmatch/relationship/analysis.py"
    model_hash = file_sha256(model_path)
    unresolved = _exact_birth_limitation(intake.respondent_birth, role="respondent") + (
        _exact_birth_limitation(intake.partner_birth, role="partner")
    )
    if unresolved:
        return PredictionLayerFreeze(
            layer_id=HD_LAYER_ID,
            status=PredictionLayerStatus.INSUFFICIENT_BIRTH_DATA,
            model_version=HD_MODEL_VERSION,
            model_sha256=model_hash,
            limitations=unresolved
            + (
                "Unknown/estimated-time relationship mechanics require the existing "
                "interval-sensitivity adapter to be wired into the public study flow.",
            ),
        )

    ephemeris_path = os.environ.get("HDMATCH_EPHEMERIS_PATH", "").strip()
    if not ephemeris_path:
        return PredictionLayerFreeze(
            layer_id=HD_LAYER_ID,
            status=PredictionLayerStatus.PENDING_ENGINE,
            model_version=HD_MODEL_VERSION,
            model_sha256=model_hash,
            limitations=(
                "HDMATCH_EPHEMERIS_PATH is not configured with verified local Swiss "
                "Ephemeris files; the strict chart engine will not silently use Moshier.",
            ),
        )

    try:
        payload = _calculate_hd_payload(
            intake.respondent_birth,
            intake.partner_birth,
            ephemeris_path=ephemeris_path,
        )
    except Exception as exc:  # fail closed; public layer reports sanitized limitation only
        return PredictionLayerFreeze(
            layer_id=HD_LAYER_ID,
            status=PredictionLayerStatus.UNAVAILABLE,
            model_version=HD_MODEL_VERSION,
            model_sha256=model_hash,
            limitations=(
                f"Strict HD chart calculation failed: {type(exc).__name__}. No fallback was used.",
            ),
        )
    return PredictionLayerFreeze(
        layer_id=HD_LAYER_ID,
        status=PredictionLayerStatus.COMPUTED,
        model_version=HD_MODEL_VERSION,
        model_sha256=model_hash,
        payload=payload,
    )


def _build_astro_rrf_layer(
    intake: RelationshipStudyIntake,
    *,
    repo_root: Path,
) -> PredictionLayerFreeze:
    file_receipts: list[dict[str, str]] = []
    for relative in ASTRO_RRF_MODEL_FILES:
        path = repo_root / relative
        if not path.exists():
            return PredictionLayerFreeze(
                layer_id=ASTRO_RRF_LAYER_ID,
                status=PredictionLayerStatus.UNAVAILABLE,
                model_version=ASTRO_RRF_MODEL_VERSION,
                model_sha256=canonical_sha256({"missing_model_file": relative}),
                limitations=(f"Frozen AstroRRF model artifact is missing: {relative}",),
            )
        file_receipts.append({"path": relative, "sha256": file_sha256(path)})
    model_hash = canonical_sha256(file_receipts)

    unresolved = _western_birth_limitations(intake.respondent_birth, role="respondent") + (
        _western_birth_limitations(intake.partner_birth, role="partner")
    )
    if unresolved:
        return PredictionLayerFreeze(
            layer_id=ASTRO_RRF_LAYER_ID,
            status=PredictionLayerStatus.INSUFFICIENT_BIRTH_DATA,
            model_version=ASTRO_RRF_MODEL_VERSION,
            model_sha256=model_hash,
            payload={"frozen_model_files": file_receipts},
            limitations=unresolved,
        )

    ephemeris_path = os.environ.get("HDMATCH_EPHEMERIS_PATH", "").strip()
    if not ephemeris_path:
        return PredictionLayerFreeze(
            layer_id=ASTRO_RRF_LAYER_ID,
            status=PredictionLayerStatus.PENDING_ENGINE,
            model_version=ASTRO_RRF_MODEL_VERSION,
            model_sha256=model_hash,
            payload={"frozen_model_files": file_receipts},
            limitations=(
                "HDMATCH_EPHEMERIS_PATH is not configured with verified local Swiss "
                "Ephemeris files; Western prediction will not use an unverified fallback.",
            ),
        )

    try:
        payload = _calculate_astro_rrf_payload(
            intake.respondent_birth,
            intake.partner_birth,
            repo_root=repo_root,
            ephemeris_path=ephemeris_path,
            file_receipts=file_receipts,
        )
    except Exception as exc:  # fail closed and preserve the frozen model identity
        return PredictionLayerFreeze(
            layer_id=ASTRO_RRF_LAYER_ID,
            status=PredictionLayerStatus.UNAVAILABLE,
            model_version=ASTRO_RRF_MODEL_VERSION,
            model_sha256=model_hash,
            payload={"frozen_model_files": file_receipts},
            limitations=(
                f"Strict AstroRRF calculation failed: {type(exc).__name__}. No fallback was used.",
            ),
        )
    return PredictionLayerFreeze(
        layer_id=ASTRO_RRF_LAYER_ID,
        status=PredictionLayerStatus.COMPUTED,
        model_version=ASTRO_RRF_MODEL_VERSION,
        model_sha256=model_hash,
        payload=payload,
    )


def _exact_birth_limitation(birth: RelationshipBirthInput, *, role: str) -> tuple[str, ...]:
    limitations: list[str] = []
    if birth.local_time is None:
        limitations.append(f"{role} birth time is unknown")
    if not birth.iana_timezone:
        limitations.append(f"{role} IANA timezone is not resolved")
    return tuple(limitations)


def _western_birth_limitations(
    birth: RelationshipBirthInput,
    *,
    role: str,
) -> tuple[str, ...]:
    limitations = list(_exact_birth_limitation(birth, role=role))
    if birth.latitude is None or birth.longitude is None:
        limitations.append(
            f"{role} birth coordinates are not resolved; frozen AstroRRF house-overlay terms "
            "must not be silently omitted"
        )
    return tuple(limitations)


def _calculate_hd_payload(
    respondent: RelationshipBirthInput,
    partner: RelationshipBirthInput,
    *,
    ephemeris_path: str,
) -> dict[str, Any]:
    from hdmatch.chart import SwissEphemerisProvider, calculate_chart
    from hdmatch.runtime.chart_adapter import declared_ephemeris_files

    from .analysis import analyze_partnership, snapshot_from_chart

    respondent_utc = _birth_utc(respondent)
    partner_utc = _birth_utc(partner)
    provider = SwissEphemerisProvider(declared_ephemeris_files(ephemeris_path))
    chart_a = calculate_chart(provider, respondent_utc)
    chart_b = calculate_chart(provider, partner_utc)
    analysis = analyze_partnership(snapshot_from_chart(chart_a), snapshot_from_chart(chart_b))
    return {
        "respondent_chart_sha256": chart_a.chart_features_sha256,
        "partner_chart_sha256": chart_b.chart_features_sha256,
        "ephemeris": _ephemeris_payload(chart_a),
        "respondent": {
            "type": analysis.partner_a_type.value if analysis.partner_a_type else None,
            "authority": (
                analysis.partner_a_authority.value if analysis.partner_a_authority else None
            ),
            "profile": analysis.partner_a_profile,
        },
        "partner": {
            "type": analysis.partner_b_type.value if analysis.partner_b_type else None,
            "authority": (
                analysis.partner_b_authority.value if analysis.partner_b_authority else None
            ),
            "profile": analysis.partner_b_profile,
        },
        "connection": {
            "center_configuration": (
                analysis.center_configuration.value if analysis.center_configuration else None
            ),
            "composite_definition": analysis.composite_definition.value,
            "defined_centers": [item.value for item in analysis.composite_defined_centers],
            "open_centers": [item.value for item in analysis.composite_open_centers],
            "channels": [
                {
                    "channel": item.channel,
                    "kind": item.kind.value,
                    "dominant_partner": item.dominant_partner,
                    "compromised_partner": item.compromised_partner,
                }
                for item in analysis.channel_connections
            ],
            "shared_gates": list(analysis.shared_gates),
            "sun_earth_node_alignments": [
                {
                    "source_partner": item.source_partner,
                    "source_body": item.source_body.value,
                    "source_side": item.source_side,
                    "target_partner": item.target_partner,
                    "target_body": item.target_body.value,
                    "target_side": item.target_side,
                    "gate": item.gate,
                    "same_line": item.same_line,
                }
                for item in analysis.sun_earth_node_alignments
            ],
            "mechanical_fingerprint_sha256": analysis.fingerprint_sha256,
        },
        "interpretation_policy": (
            "mechanics_only_no_compatibility_scalar_no_relationship_outcome_inference"
        ),
    }


def _calculate_astro_rrf_payload(
    respondent: RelationshipBirthInput,
    partner: RelationshipBirthInput,
    *,
    repo_root: Path,
    ephemeris_path: str,
    file_receipts: list[dict[str, str]],
) -> dict[str, Any]:
    from hdmatch.chart import SwissEphemerisProvider, calculate_chart
    from hdmatch.runtime.chart_adapter import declared_ephemeris_files

    from .astro_rrf import result_payload, score_astro_rrf_v01
    from .western import natal_snapshot, relationship_features

    if respondent.latitude is None or respondent.longitude is None:
        raise ValueError("respondent coordinates are required")
    if partner.latitude is None or partner.longitude is None:
        raise ValueError("partner coordinates are required")
    provider = SwissEphemerisProvider(declared_ephemeris_files(ephemeris_path))
    chart_a = calculate_chart(provider, _birth_utc(respondent))
    chart_b = calculate_chart(provider, _birth_utc(partner))
    natal_a = natal_snapshot(
        chart_a,
        latitude=respondent.latitude,
        longitude=respondent.longitude,
    )
    natal_b = natal_snapshot(
        chart_b,
        latitude=partner.latitude,
        longitude=partner.longitude,
    )
    features = relationship_features(natal_a, natal_b)
    model_path = repo_root / "reference/development_models/astro_rrf_directional_v0_1.json"
    model_raw = json.loads(model_path.read_text(encoding="utf-8"))
    if not isinstance(model_raw, dict):
        raise ValueError("AstroRRF V0.1 model must be a JSON object")
    scored = score_astro_rrf_v01(features, model_raw)
    return {
        "respondent_chart_sha256": chart_a.chart_features_sha256,
        "partner_chart_sha256": chart_b.chart_features_sha256,
        "ephemeris": _ephemeris_payload(chart_a),
        "frozen_model_files": file_receipts,
        "v0_1_raw_scoring": result_payload(scored),
        "birth_geometry": {
            "respondent_houses_available": natal_a.house_cusps is not None,
            "partner_houses_available": natal_b.house_cusps is not None,
        },
        "prediction_boundary": (
            "Only frozen weighted V0.1 axes receive numeric scores here. V0.2–V0.4 "
            "extensions remain feature-family flags unless a separately frozen calibration "
            "defines an outcome mapping. Unmapped questionnaire axes are not predicted."
        ),
    }


def _ephemeris_payload(chart: Any) -> dict[str, Any]:
    return {
        "provider": chart.metadata.ephemeris.provider,
        "library_version": chart.metadata.ephemeris.library_version,
        "files": [
            {
                "name": Path(item.path).name,
                "sha256": item.sha256,
                "size_bytes": item.size_bytes,
            }
            for item in chart.metadata.ephemeris.files
        ],
        "calculation_flags": list(chart.metadata.ephemeris.calculation_flags),
    }


def _birth_utc(birth: RelationshipBirthInput) -> datetime:
    if birth.local_time is None or not birth.iana_timezone:
        raise ValueError("exact birth calculation requires local_time and IANA timezone")
    supplied = datetime.combine(birth.birth_date, birth.local_time)
    resolution = resolve_local_datetime(supplied, birth.iana_timezone)
    return resolution.require_unique().utc


def _under_root(repo_root: Path, path: Path) -> Path:
    if path.is_absolute():
        return path
    return repo_root / path
