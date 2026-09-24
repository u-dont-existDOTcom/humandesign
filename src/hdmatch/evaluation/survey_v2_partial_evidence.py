"""Partial-evidence scorer for Survey-v2 candidate universes.

This module is for development diagnostics. It scores only explicitly observed
fields, macro-averages repeated probes within a field, and then macro-averages
fields within each declared dependency cluster.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Hashable, Mapping
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from hdmatch.evaluation.holistic_profile_information import predicate_matches
from hdmatch.schemas import StructuralChartFeatures


@dataclass(frozen=True)
class EvidenceProbe:
    probe_id: str
    labels: tuple[Hashable, ...]
    reliability: Fraction


@dataclass(frozen=True)
class CompiledField:
    field_id: str
    cluster_id: str
    source_mapping_ids: tuple[str, ...]
    source_predicates: tuple[str, ...]
    predicates: tuple[Mapping[str, Any], ...]
    probes: tuple[EvidenceProbe, ...]


@dataclass(frozen=True)
class CompiledPartialEvidence:
    fields: tuple[CompiledField, ...]



def compile_partial_evidence(
    *,
    evidence: Mapping[str, Any],
    field_dependency_map: Mapping[str, Any],
    model: Mapping[str, Any],
) -> CompiledPartialEvidence:
    dependencies = {
        str(item["field_id"]): item for item in field_dependency_map["field_dependencies"]
    }
    by_mapping_id = {
        str(item["id"]): item for item in model.get("mappings", ())
    } | {
        str(item["id"]): item for item in model.get("contradictions", ())
    }
    known_mapping_ids = set(by_mapping_id)
    grouped: dict[str, list[EvidenceProbe]] = defaultdict(list)
    seen_probe_ids: set[str] = set()

    for raw in evidence.get("observations", ()):
        field_id = str(raw["field_id"])
        probe_id = str(raw["probe_id"])
        if field_id not in dependencies:
            raise ValueError(f"unknown Survey-v2 field_id: {field_id}")
        if probe_id in seen_probe_ids:
            raise ValueError(f"duplicate probe_id: {probe_id}")
        seen_probe_ids.add(probe_id)
        labels = tuple(raw["labels"])
        if not labels or len(set(labels)) != len(labels):
            raise ValueError(f"labels must be non-empty and unique: {probe_id}")
        reliability = Fraction(str(raw["reliability"]))
        if not 0 <= reliability <= 1:
            raise ValueError(f"reliability must be in [0, 1]: {probe_id}")
        grouped[field_id].append(EvidenceProbe(probe_id, labels, reliability))

    fields: list[CompiledField] = []
    for field_id in sorted(grouped):
        dependency = dependencies[field_id]
        source_mapping_ids = tuple(str(value) for value in dependency["source_mapping_ids"])
        missing = tuple(value for value in source_mapping_ids if value not in known_mapping_ids)
        if missing and field_id.startswith("baseline:"):
            raise ValueError(f"missing source mappings for {field_id}: {missing}")
        fields.append(
            CompiledField(
                field_id=field_id,
                cluster_id=str(dependency["dependency_cluster_id"]),
                source_mapping_ids=source_mapping_ids,
                source_predicates=tuple(
                    str(value) for value in dependency.get("source_predicates", ())
                ),
                predicates=tuple(
                    by_mapping_id[value]["predicate"] for value in source_mapping_ids
                ),
                probes=tuple(grouped[field_id]),
            )
        )
    if not fields:
        raise ValueError("partial evidence requires at least one observation")
    return CompiledPartialEvidence(fields=tuple(fields))


def score_candidate(
    features: StructuralChartFeatures,
    compiled: CompiledPartialEvidence,
) -> Fraction:
    cluster_scores: dict[str, list[Fraction]] = defaultdict(list)
    for field in compiled.fields:
        value = candidate_field_value(features, field)
        probe_scores = tuple(_probe_score(value, probe) for probe in field.probes)
        cluster_scores[field.cluster_id].append(
            sum(probe_scores, Fraction()) / len(probe_scores)
        )
    return sum(
        (sum(scores, Fraction()) / len(scores) for scores in cluster_scores.values()),
        Fraction(),
    )


def candidate_field_value(
    features: StructuralChartFeatures,
    field: CompiledField,
) -> Hashable:
    if field.field_id.startswith("baseline:"):
        if not field.predicates:
            raise ValueError(f"baseline field has no predicates: {field.field_id}")
        return int(any(predicate_matches(features, predicate) for predicate in field.predicates))

    if field.field_id.startswith("channel:"):
        channel = field.field_id.removeprefix("channel:")
        return int(channel in features.channels or _reverse_channel(channel) in features.channels)

    if field.field_id == "profile":
        return f"profile:{features.profile}"

    if len(field.source_predicates) == 1 and "=gate:<label>" in field.source_predicates[0]:
        left = field.source_predicates[0].split("=gate:<label>", 1)[0]
        key = left.removeprefix("activation:")
        gate = features.activation_gates.get(key)
        if gate is None:
            raise ValueError(f"missing activation value for {field.field_id}: {key}")
        return f"gate:{gate}"

    raise ValueError(f"unsupported Survey-v2 field resolver: {field.field_id}")


def _probe_score(value: Hashable, probe: EvidenceProbe) -> Fraction:
    if value not in probe.labels:
        return Fraction()
    return probe.reliability / len(probe.labels)


def _reverse_channel(channel: str) -> str:
    left, right = channel.split("-", 1)
    return f"{right}-{left}"
