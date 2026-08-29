"""Participant-safe relationship fingerprint and conservative prediction reveal."""

from __future__ import annotations

from typing import Any, cast

from .phenotype import RelationshipPhenotypeFreeze
from .study import RelationshipPredictionFreeze


def relationship_fingerprint(
    phenotype: RelationshipPhenotypeFreeze,
    rubric: dict[str, Any],
) -> dict[str, Any]:
    """Render the sealed phenotype without astrology or an overall compatibility score."""

    definitions = {
        str(item["id"]): str(item.get("definition", ""))
        for item in cast(list[dict[str, Any]], rubric.get("axes", []))
        if isinstance(item.get("id"), str)
    }
    axes: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    for question in phenotype.output.question_results:
        for axis in question.axis_results:
            row = {
                "question_id": question.question_id,
                "axis_id": axis.axis_id,
                "definition": definitions.get(axis.axis_id, ""),
                "direction": axis.direction,
                "status": axis.status,
                "value": axis.ordinal_value,
                "trajectory": axis.trajectory,
                "confidence": axis.confidence,
                "context_conditions": list(axis.context_conditions),
                "observability_limits": list(axis.observability_limits),
            }
            if axis.status == "classified":
                axes.append(row)
            else:
                unresolved.append(row)
    return {
        "schema_version": "relationship-fingerprint-v1",
        "phenotype_freeze_sha256": phenotype.freeze_sha256,
        "classified_axes": axes,
        "unresolved_or_mixed_axes": unresolved,
        "overall_compatibility_score": None,
        "note": (
            "This is a chart-blind map of the relationship evidence. It deliberately "
            "does not collapse the relationship into one compatibility number."
        ),
    }


def conservative_prediction_reveal(
    prediction: RelationshipPredictionFreeze,
    phenotype: RelationshipPhenotypeFreeze,
) -> dict[str, Any]:
    """Reveal pre-answer predictions without retroactively inventing outcome thresholds."""

    layers: list[dict[str, Any]] = []
    for layer in prediction.layers:
        if layer.layer_id == "human_design_connection_v1":
            layers.append(
                {
                    "layer_id": layer.layer_id,
                    "status": layer.status.value,
                    "model_version": layer.model_version,
                    "preanswer_payload": layer.payload if layer.status.value == "computed" else {},
                    "outcome_comparison_status": "not_mapped_to_phenotype_axes",
                    "explanation": (
                        "The frozen HD layer is a mechanical connection surface. No frozen "
                        "rule currently converts connection density or channel categories "
                        "into an overall relationship outcome, so those mechanics are not "
                        "counted as confirmatory hits by themselves."
                    ),
                }
            )
            continue
        if layer.layer_id == "astro_rrf_directional_v0_4":
            layers.append(
                {
                    "layer_id": layer.layer_id,
                    "status": layer.status.value,
                    "model_version": layer.model_version,
                    "preanswer_payload": layer.payload if layer.status.value == "computed" else {},
                    "outcome_comparison_status": "raw_signal_frozen_calibration_pending",
                    "explanation": (
                        "The V0.1 weighted directional scores and V0.2–V0.4 feature-family "
                        "flags were frozen before the questionnaire. No post-answer high/low "
                        "cutoff is being invented. A separately frozen calibration is needed "
                        "before these raw signals can receive formal hit/miss labels."
                    ),
                }
            )
            continue
        layers.append(
            {
                "layer_id": layer.layer_id,
                "status": layer.status.value,
                "model_version": layer.model_version,
                "preanswer_payload": {},
                "outcome_comparison_status": "unmapped_layer",
            }
        )
    return {
        "schema_version": "relationship-prediction-reveal-v1",
        "prediction_freeze_sha256": prediction.freeze_sha256,
        "phenotype_freeze_sha256": phenotype.freeze_sha256,
        "layers": layers,
        "formal_hit_miss_summary": None,
        "scientific_boundary": (
            "Only prediction-to-outcome mappings frozen before behavioral evidence may be "
            "scored. Raw pre-answer features can be shown but are not retroactively labeled "
            "successful because they resemble the observed relationship."
        ),
    }
