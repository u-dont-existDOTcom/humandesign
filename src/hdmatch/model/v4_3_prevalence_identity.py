"""Canonical mapping-derived identities shared by prevalence and scoring.

This module deliberately lives beside, rather than inside, the ``v4_3`` package
so the claim-grade scoring adapter can import the nominal verified prevalence
provider without creating an import cycle.
"""

from __future__ import annotations

from hdmatch.experiments.canonical import sha256_json
from hdmatch.model.v4_3_mapping import (
    CompiledMappingRuleV2,
    CompiledPathwayV2,
    MappingLibraryV2,
)


def all_rule_pathways(
    rule: CompiledMappingRuleV2,
) -> tuple[CompiledPathwayV2, ...]:
    """Return every scoreable pathway, including the optional corroborator."""

    pathways = (rule.primary_pathway, *rule.alternative_pathways)
    if rule.corroborating_pathway is not None:
        pathways = (*pathways, rule.corroborating_pathway.pathway)
    return pathways


def unique_prevalence_pathways(
    library: MappingLibraryV2,
) -> tuple[CompiledPathwayV2, ...]:
    """Return the canonical unique anchor inventory sorted by anchor ID."""

    by_anchor: dict[str, CompiledPathwayV2] = {}
    for rule in library.rules:
        for pathway in all_rule_pathways(rule):
            by_anchor.setdefault(pathway.anchor_id, pathway)
    return tuple(by_anchor[item] for item in sorted(by_anchor))


def mapping_prevalence_parent_hierarchy_sha256(library: MappingLibraryV2) -> str:
    """Hash the canonical parent/backoff hierarchy for every unique anchor."""

    pathways = unique_prevalence_pathways(library)
    return sha256_json(
        [
            {
                "anchor_id": pathway.anchor_id,
                "parent_hierarchy": [
                    level.model_dump(mode="json")
                    for level in pathway.prevalence_parent_hierarchy
                ],
            }
            for pathway in pathways
        ]
    )


def mapping_prevalence_plan_sha256(library: MappingLibraryV2) -> str:
    """Hash exact predicates, parents, features, registry, and mapping identity."""

    pathways = unique_prevalence_pathways(library)
    return sha256_json(
        {
            "mapping_library_sha256": library.sha256(),
            "required_feature_registry_sha256": (
                library.required_feature_registry_sha256
            ),
            "anchors": [
                {
                    "anchor_id": pathway.anchor_id,
                    "predicate": pathway.predicate.model_dump(mode="json"),
                    "parent_hierarchy": [
                        level.model_dump(mode="json")
                        for level in pathway.prevalence_parent_hierarchy
                    ],
                    "required_feature_ids": [
                        item.value for item in pathway.required_feature_ids
                    ],
                }
                for pathway in pathways
            ],
        }
    )
