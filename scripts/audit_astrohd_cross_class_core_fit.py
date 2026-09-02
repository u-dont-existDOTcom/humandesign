#!/usr/bin/env python3
"""Generate the mechanical AstroHD cross-class core-fit diagnostic artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from hdmatch.model.dependencies import ClusterContribution, collapse_dependency_clusters
from hdmatch.model.mapping_library import MappingLibrary, StructuralClass, load_mapping_library
from hdmatch.model.symbolic_score import information_bits, score_symbolic
from hdmatch.participant.backend import AstroHDParticipantBackend
from hdmatch.questionnaire.response import NormalizedResponse
from hdmatch.schemas import (
    CandidateState,
    LocalDateOverlap,
    ScoredState,
    StructuralChartFeatures,
)

ROOT = Path(__file__).resolve().parents[1]
MAPPING_LIBRARY_PATH = Path("mappings/mapping_library_v1.json")
DEPENDENCIES_PATH = Path("src/hdmatch/model/dependencies.py")
SYMBOLIC_SCORE_PATH = Path("src/hdmatch/model/symbolic_score.py")
PARTICIPANT_BACKEND_PATH = Path("src/hdmatch/participant/backend.py")
OUTPUT_PATH = Path("reference/audits/astrohd_cross_class_core_fit_v1.json")

JsonObject = dict[str, Any]
Chart = Mapping[str, Any]

BLOCK_FOR_CLASS = (
    (StructuralClass.TYPE_STRATEGY, "type_strategy"),
    (StructuralClass.AUTHORITY, "authority"),
    (StructuralClass.DIAGNOSTIC_CENTER, "diagnostic_centers"),
    (StructuralClass.PROFILE, "profile"),
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_json(payload: JsonObject) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def _source_metadata(repository_root: Path) -> JsonObject:
    return {
        "dependency_control": {
            "path": DEPENDENCIES_PATH.as_posix(),
            "sha256": sha256_file(repository_root / DEPENDENCIES_PATH),
        },
        "mapping_library": {
            "path": MAPPING_LIBRARY_PATH.as_posix(),
            "sha256": sha256_file(repository_root / MAPPING_LIBRARY_PATH),
        },
        "participant_ranking": {
            "path": PARTICIPANT_BACKEND_PATH.as_posix(),
            "sha256": sha256_file(repository_root / PARTICIPANT_BACKEND_PATH),
        },
        "symbolic_scorer": {
            "path": SYMBOLIC_SCORE_PATH.as_posix(),
            "sha256": sha256_file(repository_root / SYMBOLIC_SCORE_PATH),
        },
    }


def _response(question_id: str, answer_token: str) -> NormalizedResponse:
    return NormalizedResponse(
        question_id=question_id,
        answer_token=answer_token,
        behavioral_confidence=1.0,
        measurement_reliability=1.0,
    )


def _cluster_inventory(library: MappingLibrary) -> tuple[list[JsonObject], list[str]]:
    rows: list[JsonObject] = []
    cluster_ids = sorted({mapping.dependency_cluster for mapping in library.frozen_mappings})
    for cluster_id in cluster_ids:
        mappings = [
            mapping
            for mapping in library.frozen_mappings
            if mapping.dependency_cluster == cluster_id
        ]
        structural_classes: list[str] = []
        for mapping in mappings:
            assert mapping.structural_class is not None
            structural_classes.append(mapping.structural_class.value)
        rows.append(
            {
                "cluster_id": cluster_id,
                "mapping_ids": sorted(mapping.mapping_id for mapping in mappings),
                "observation_ids": sorted({mapping.observation_id for mapping in mappings}),
                "question_ids": sorted(
                    {question_id for mapping in mappings for question_id in mapping.question_ids}
                ),
                "structural_class_count": len(set(structural_classes)),
                "structural_classes": sorted(set(structural_classes)),
            }
        )
    cross_class = [row["cluster_id"] for row in rows if row["structural_class_count"] > 1]
    return rows, cross_class


def _raw_contributions(
    chart: Chart,
    responses: Sequence[NormalizedResponse],
    library: MappingLibrary,
    prevalence_by_anchor: Mapping[str, float],
) -> tuple[ClusterContribution, ...]:
    mappings_by_question: dict[str, list[Any]] = defaultdict(list)
    for mapping in library.frozen_mappings:
        for question_id in mapping.question_ids:
            mappings_by_question[question_id].append(mapping)

    values: list[ClusterContribution] = []
    for response in responses:
        for mapping in mappings_by_question.get(response.question_id, []):
            assert mapping.chart_feature_predicate is not None
            assert mapping.predicted_response is not None
            assert mapping.structural_salience is not None
            assert mapping.mapping_directness is not None
            predicate_matches = mapping.chart_feature_predicate.matches(chart)
            support = 0.0
            evidence = 0.0
            contradiction_severity = 0.0
            contradiction = 0.0
            if predicate_matches:
                if response.answer_token in mapping.predicted_response.support_answer_tokens:
                    support = min(1.0, mapping.structural_salience * mapping.mapping_directness)
                    evidence = (
                        response.effective_confidence
                        * support
                        * information_bits(
                            prevalence_by_anchor[mapping.anchor_id],
                            cap=library.constants.information_cap_rubric_bits,
                        )
                    )
                if (
                    mapping.contradiction_rule is not None
                    and response.answer_token in mapping.contradiction_rule.answer_tokens
                ):
                    contradiction_severity = float(mapping.contradiction_rule.severity)
                    contradiction = (
                        response.effective_confidence
                        * contradiction_severity
                        * library.constants.contradiction_cap_rubric_bits
                    )
            values.append(
                ClusterContribution(
                    cluster_id=mapping.dependency_cluster,
                    mapping_id=mapping.mapping_id,
                    anchor_id=mapping.anchor_id,
                    effective_confidence=response.effective_confidence,
                    support=support,
                    evidence_rubric_bits=evidence,
                    contradiction_severity=contradiction_severity,
                    contradiction_rubric_bits=contradiction,
                )
            )
    return tuple(values)


def _core_fit_block_arithmetic(
    chart: Chart,
    responses: Sequence[NormalizedResponse],
    library: MappingLibrary,
) -> JsonObject:
    mappings_by_question: dict[str, list[Any]] = defaultdict(list)
    for mapping in library.frozen_mappings:
        for question_id in mapping.question_ids:
            mappings_by_question[question_id].append(mapping)

    class_values: dict[StructuralClass, list[tuple[str, float, float]]] = defaultdict(list)
    for response in responses:
        for mapping in mappings_by_question.get(response.question_id, []):
            assert mapping.chart_feature_predicate is not None
            assert mapping.predicted_response is not None
            assert mapping.structural_class is not None
            assert mapping.mapping_directness is not None
            support = 0.0
            if (
                mapping.chart_feature_predicate.matches(chart)
                and response.answer_token in mapping.predicted_response.support_answer_tokens
            ):
                support = mapping.mapping_directness
            class_values[mapping.structural_class].append(
                (mapping.dependency_cluster, support, response.effective_confidence)
            )

    blocks: list[JsonObject] = []
    earned_total = 0.0
    available_total = 0.0
    for structural_class, block_name in BLOCK_FOR_CLASS:
        values = class_values.get(structural_class, [])
        if not values:
            continue
        by_cluster: dict[str, tuple[float, float]] = {}
        for cluster_id, support, confidence in values:
            current = by_cluster.get(cluster_id, (0.0, 0.0))
            by_cluster[cluster_id] = (max(current[0], support), max(current[1], confidence))
        confidence_total = sum(confidence for _, confidence in by_cluster.values())
        if confidence_total == 0.0:
            continue
        weighted_support = sum(support * confidence for support, confidence in by_cluster.values())
        fraction = weighted_support / confidence_total
        weight = library.constants.core_weights[block_name]
        earned_weight = weight * fraction
        earned_total += earned_weight
        available_total += weight
        blocks.append(
            {
                "available_weight": weight,
                "block_name": block_name,
                "confidence_total": confidence_total,
                "dependency_cluster_ids": sorted(by_cluster),
                "earned_weight": earned_weight,
                "fraction": fraction,
                "structural_class": structural_class.value,
                "support_times_confidence_total": weighted_support,
            }
        )
    return {
        "available_weight_total": available_total,
        "blocks": blocks,
        "core_fit": 100.0 * earned_total / available_total if available_total else 0.0,
        "earned_weight_total": earned_total,
    }


def _collapse_contrast(
    chart: Chart,
    responses: Sequence[NormalizedResponse],
    library: MappingLibrary,
    prevalence_by_anchor: Mapping[str, float],
    cluster_id: str,
) -> JsonObject:
    raw = _raw_contributions(chart, responses, library, prevalence_by_anchor)
    raw_relevant = [item for item in raw if item.cluster_id == cluster_id]
    collapsed = collapse_dependency_clusters(raw)
    collapsed_relevant = [item for item in collapsed if item.cluster_id == cluster_id]
    if len(collapsed_relevant) != 1:
        raise ValueError(
            f"expected one collapsed contribution for {cluster_id}, got {len(collapsed_relevant)}"
        )
    winner = collapsed_relevant[0]
    return {
        "collapsed_contribution_count": len(collapsed_relevant),
        "dependency_cluster_id": cluster_id,
        "raw_contribution_count": len(raw_relevant),
        "raw_mapping_ids": sorted(item.mapping_id for item in raw_relevant),
        "resulting_evidence_rubric_bits": sum(item.evidence_rubric_bits for item in collapsed),
        "winning_evidence_rubric_bits": winner.evidence_rubric_bits,
        "winning_mapping_id": winner.mapping_id,
        "winning_support": winner.support,
    }


def _scorer_case(
    *,
    chart: Chart,
    responses: Sequence[NormalizedResponse],
    library: MappingLibrary,
    prevalence_by_anchor: Mapping[str, float],
    cluster_id: str,
) -> JsonObject:
    score = score_symbolic(chart, responses, library, prevalence_by_anchor)
    return {
        "chart": {
            key: list(value) if isinstance(value, tuple) else value for key, value in chart.items()
        },
        "core_fit_block_arithmetic": _core_fit_block_arithmetic(chart, responses, library),
        "global_dependency_collapse": _collapse_contrast(
            chart,
            responses,
            library,
            prevalence_by_anchor,
            cluster_id,
        ),
        "responses": [response.model_dump(mode="json") for response in responses],
        "score": score.model_dump(mode="json"),
    }


def _rank_state(state_id: str, start: datetime) -> CandidateState:
    end = start + timedelta(minutes=1)
    features = StructuralChartFeatures(
        type="Generator",
        strategy="Wait to Respond",
        authority="Sacral",
        profile="1/4",
        definition="Single",
        defined_centers=("Sacral",),
    )
    return CandidateState(
        state_id=state_id,
        start_utc=start,
        end_utc=end,
        chart_features_hash=hashlib.sha256(state_id.encode()).hexdigest(),
        chart_features=features,
        local_date_overlaps=(
            LocalDateOverlap(date=start.date(), seconds=(end - start).total_seconds()),
        ),
    )


def _ranking_case() -> JsonObject:
    start = datetime(2000, 1, 1, tzinfo=UTC)
    states = (
        _rank_state("LOW", start),
        _rank_state("HIGH", start + timedelta(minutes=1)),
    )
    scores = {
        "LOW": ScoredState(
            state_id="LOW",
            net_rubric_bits=1.0,
            evidence_rubric_bits=1.0,
            contradiction_rubric_bits=0.0,
            meaningful_contradictions=0,
            detailed_support=50.0,
            core_fit=66.66666666666667,
        ),
        "HIGH": ScoredState(
            state_id="HIGH",
            net_rubric_bits=1.0,
            evidence_rubric_bits=1.0,
            contradiction_rubric_bits=0.0,
            meaningful_contradictions=0,
            detailed_support=50.0,
            core_fit=78.57142857142857,
        ),
    }
    backend = object.__new__(AstroHDParticipantBackend)
    ranked = backend._rank_states(states, scores)
    return {
        "better_scientific_rank_state_id": ranked[0].state.state_id,
        "held_equal_fields": [
            "net_rubric_bits",
            "evidence_rubric_bits",
            "contradiction_rubric_bits",
            "meaningful_contradictions",
            "detailed_support",
        ],
        "only_differing_score_field": "core_fit",
        "ordered_state_ids": [item.state.state_id for item in ranked],
        "scientific_rank_by_state_id": {item.state.state_id: item.rank for item in ranked},
        "scores": {state_id: score.model_dump(mode="json") for state_id, score in scores.items()},
    }


def _directed_mapping_facts(library: MappingLibrary) -> list[JsonObject]:
    expected_mapping_ids = {
        "MAP-AUTH-EMOTIONAL-D03",
        "MAP-CENTER-SACRAL-DEFINED-C08",
        "MAP-CENTER-SOLARPLEXUS-DEFINED-C02",
        "MAP-TYPE-GENERATOR-S02",
    }
    rows: list[JsonObject] = []
    for mapping in library.frozen_mappings:
        if mapping.mapping_id not in expected_mapping_ids:
            continue
        assert mapping.structural_class is not None
        rows.append(
            {
                "dependency_cluster": mapping.dependency_cluster,
                "mapping_id": mapping.mapping_id,
                "question_ids": sorted(mapping.question_ids),
                "structural_class": mapping.structural_class.value,
            }
        )
    if {row["mapping_id"] for row in rows} != expected_mapping_ids:
        raise ValueError("directed scorer mapping set does not match current frozen source")
    return sorted(rows, key=lambda row: row["mapping_id"])


def build_audit(repository_root: Path = ROOT) -> JsonObject:
    library = load_mapping_library(repository_root / MAPPING_LIBRARY_PATH)
    prevalence_by_anchor = {mapping.anchor_id: 0.5 for mapping in library.frozen_mappings}
    clusters, cross_class = _cluster_inventory(library)

    chart_a: Chart = {
        "authority": "Emotional",
        "defined_centers": ("Solar Plexus",),
        "profile": "1/4",
        "strategy": "Wait for the Invitation",
        "type": "Projector",
    }
    responses_a1 = (
        _response("D03", "fluctuate_with_emotional_highs_and_lows"),
        _response("P01", "never"),
    )
    responses_a2 = (*responses_a1, _response("C02", "wave_like"))

    chart_b: Chart = {
        "authority": "Sacral",
        "defined_centers": ("Sacral",),
        "profile": "1/4",
        "strategy": "Wait to Respond",
        "type": "Generator",
    }
    responses_b1 = (_response("S02", "very_often"), _response("P01", "never"))
    responses_b2 = (
        *responses_b1,
        _response("C08", "physical_energy_renew_through_doing_the_right_work"),
    )

    return {
        "controlled_scorer_cases": {
            "A1": _scorer_case(
                chart=chart_a,
                responses=responses_a1,
                library=library,
                prevalence_by_anchor=prevalence_by_anchor,
                cluster_id="AUTHORITY_DECISION",
            ),
            "A2": _scorer_case(
                chart=chart_a,
                responses=responses_a2,
                library=library,
                prevalence_by_anchor=prevalence_by_anchor,
                cluster_id="AUTHORITY_DECISION",
            ),
            "B1": _scorer_case(
                chart=chart_b,
                responses=responses_b1,
                library=library,
                prevalence_by_anchor=prevalence_by_anchor,
                cluster_id="TYPE_STRATEGY_ARCHITECTURE",
            ),
            "B2": _scorer_case(
                chart=chart_b,
                responses=responses_b2,
                library=library,
                prevalence_by_anchor=prevalence_by_anchor,
                cluster_id="TYPE_STRATEGY_ARCHITECTURE",
            ),
        },
        "cross_class_dependency_cluster_ids": cross_class,
        "dependency_clusters": clusters,
        "directed_mapping_facts": _directed_mapping_facts(library),
        "ranking_case": _ranking_case(),
        "schema_version": "astrohd-cross-class-core-fit-audit-v1",
        "source": _source_metadata(repository_root),
        "source_behavior": {
            "core_fit_support_basis": "mapping_directness_when_mapping_support_is_nonzero",
            "ordinary_evidence_support_basis": ("structural_salience_times_mapping_directness"),
        },
        "status": "mechanical_diagnostic_only_no_runtime_effect",
        "synthetic_prevalence_for_every_frozen_anchor": 0.5,
    }


def write_audit(
    repository_root: Path = ROOT,
    *,
    output: Path | None = None,
) -> Path:
    output_path = output or repository_root / OUTPUT_PATH
    output_path.write_bytes(render_json(build_audit(repository_root)))
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    repository_root = arguments.repository_root.resolve()
    output = arguments.output.resolve() if arguments.output else None
    output_path = write_audit(repository_root, output=output)
    audit = json.loads(output_path.read_text(encoding="utf-8"))
    print(
        json.dumps(
            {
                "cross_class_dependency_cluster_ids": audit["cross_class_dependency_cluster_ids"],
                "output": output_path.as_posix(),
                "ranking_order": audit["ranking_case"]["ordered_state_ids"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
