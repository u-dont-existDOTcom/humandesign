"""Deterministically compile the separate detailed symbolic Model B policy."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from hdmatch.chart.bodygraph import CHANNELS
from hdmatch.model_b.artifacts import (
    SALIENCE_BY_LAYER,
    ConditionalPrevalencePolicy,
    DependencyPolicy,
    DetailedLayer,
    FeatureStatus,
    ModelBArtifact,
    ModelBUnresolvedReport,
    SourceArtifact,
    SourceCitation,
    StructuralFamily,
    UnresolvedBehaviorMapping,
)
from hdmatch.questionnaire.bank import load_question_bank
from hdmatch.util import sha256_file

QUESTION_BANK = "reference/core/question_bank_v1.json"
V4_PROTOCOL = "reference/core/human_design_reverse_matching_protocol_v4_1.md"
V3_PROTOCOL = "reference/core/human_design_search_instructions_fixed_candidate_blind(6).md"
V32_PROFILE = "reference/core/updated_behavioral_profile_v3_2.md"
V32_DELTA = "reference/core/v3_2_scoring_delta.md"
MAPPING_TODO = "reference/core/MAPPING_LIBRARY_TODO.md"
BACKEND_CONTRACT = "reference/core/search_backend_contract.md"
BODYGRAPH_IMPLEMENTATION = "src/hdmatch/chart/bodygraph.py"
MODEL_A_MAPPING = "mappings/mapping_library_v1.json"

NORMATIVE_SOURCES = (
    QUESTION_BANK,
    V4_PROTOCOL,
    V3_PROTOCOL,
    V32_PROFILE,
    V32_DELTA,
    MAPPING_TODO,
    BACKEND_CONTRACT,
)


class CompilationResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    artifact_path: str
    report_path: str
    artifact_semantic_sha256: str
    artifact_file_sha256: str
    frozen_feature_family_count: int
    unresolved_feature_family_count: int
    unresolved_behavior_mapping_count: int


def _source(path: str, locator: str, rationale: str) -> SourceCitation:
    return SourceCitation(path=path, locator=locator, rationale=rationale)


def _core_backoff() -> tuple[tuple[str, ...], ...]:
    """Frozen expansion of V3's four named core architecture blocks."""

    return (
        ("type", "strategy", "authority", "defined_centers", "profile"),
        ("type", "authority"),
        ("type",),
        (),
    )


def _unresolved_higher_architecture_backoff() -> tuple[tuple[str, ...], ...]:
    """Represent the protocol phrase without pretending its exact parent set is known."""

    return (("frozen_higher_level_architecture",), ())


def _unresolved_gate_parent_backoff() -> tuple[tuple[str, ...], ...]:
    return (("relevant_higher_level_architecture",), ())


def _family(
    family_id: str,
    layer: DetailedLayer,
    *,
    extractor: str,
    feature_status: FeatureStatus,
    parents: tuple[tuple[str, ...], ...],
    parent_status: FeatureStatus,
    policies: tuple[str, ...],
    sources: tuple[SourceCitation, ...],
    unresolved_reason: str | None = None,
    parent_unresolved_reason: str | None = None,
) -> StructuralFamily:
    return StructuralFamily(
        family_id=family_id,
        layer=layer,
        feature_status=feature_status,
        structural_salience=SALIENCE_BY_LAYER[layer],
        extractor=extractor,
        conditional_parent_levels=parents,
        conditional_parent_status=parent_status,
        conditional_parent_unresolved_reason=parent_unresolved_reason,
        dependency_policy_ids=policies,
        sources=sources,
        unresolved_reason=unresolved_reason,
    )


def _structural_families() -> tuple[StructuralFamily, ...]:
    salience_source = _source(
        V3_PROTOCOL,
        "§11 Fixed structural salience classes and §46 Default V3 constants",
        "The detailed structural layers have global salience constants and may not be "
        "candidate-tuned.",
    )
    layer_source = _source(
        V4_PROTOCOL,
        "§21 Minute-level discrimination layers",
        "Layer 1 includes Definition and complete Channels; Layer 2 includes cardinal, "
        "Node, repeated-gate, and material activation transitions.",
    )
    core_parent_source = _source(
        V3_PROTOCOL,
        "§21 Conditional prevalence and dependency control",
        "Channel prevalence is conditional on frozen core architecture, whose four "
        "blocks are enumerated in §8.",
    )
    ambiguous_parent = (
        "The protocol names a higher-level parent category but does not freeze its exact "
        "feature fields; Model B records the category and must not choose a favorable set."
    )
    return (
        _family(
            "MBF-COMPLETE-CHANNEL",
            DetailedLayer.COMPLETE_CHANNEL,
            extractor="extract_complete_channels",
            feature_status=FeatureStatus.FROZEN,
            parents=_core_backoff(),
            parent_status=FeatureStatus.UNRESOLVED,
            policies=("MBD-CHANNEL-GATE", "MBD-ANCHOR-REUSE", "MBD-ALTERNATIVES"),
            sources=(
                salience_source,
                layer_source,
                _source(
                    V3_PROTOCOL,
                    "§33 Channels and hanging gates",
                    "A complete channel has salience 0.80 and missing it is neutral.",
                ),
                core_parent_source,
            ),
            parent_unresolved_reason=(
                "V3 freezes the full channel parent as core architecture but only says to "
                "back off one parent level when small; it does not freeze which block is "
                "removed first. The displayed fallback sequence is a non-scoring placeholder "
                "that must be explicitly frozen per run before conditional scoring."
            ),
        ),
        _family(
            "MBF-CARDINAL-ACTIVATION",
            DetailedLayer.CARDINAL_ACTIVATION,
            extractor="extract_cardinal_activations",
            feature_status=FeatureStatus.FROZEN,
            parents=_unresolved_higher_architecture_backoff(),
            parent_status=FeatureStatus.UNRESOLVED,
            policies=(
                "MBD-CARDINAL-CROSS",
                "MBD-PROFILE-CARDINAL-LINE",
                "MBD-ANCHOR-REUSE",
                "MBD-ALTERNATIVES",
            ),
            sources=(
                salience_source,
                layer_source,
                _source(
                    V3_PROTOCOL,
                    "§32 Cardinal placements",
                    "Personality/Design Sun and Earth gate or line placements have "
                    "salience 0.75 without bespoke per-gate bonuses.",
                ),
            ),
            parent_unresolved_reason=ambiguous_parent,
        ),
        _family(
            "MBF-DEFINITION",
            DetailedLayer.DEFINITION,
            extractor="extract_definition",
            feature_status=FeatureStatus.FROZEN,
            parents=((),),
            parent_status=FeatureStatus.UNRESOLVED,
            policies=("MBD-ANCHOR-REUSE", "MBD-ALTERNATIVES"),
            sources=(salience_source, layer_source),
            parent_unresolved_reason=(
                "V3 freezes Definition salience but supplies no conditional-prevalence "
                "parent for Definition. Only unconditional prevalence is currently defined."
            ),
        ),
        _family(
            "MBF-REPEATED-GATE",
            DetailedLayer.REPEATED_GATE,
            extractor="extract_repeated_gate_candidates",
            feature_status=FeatureStatus.UNRESOLVED,
            parents=_unresolved_gate_parent_backoff(),
            parent_status=FeatureStatus.UNRESOLVED,
            policies=("MBD-CHANNEL-GATE", "MBD-ANCHOR-REUSE", "MBD-ALTERNATIVES"),
            sources=(salience_source, layer_source),
            unresolved_reason=(
                "The protocol names repeated gates but does not freeze occurrence counting, "
                "side/body treatment, or a behavioral directness rule. The extractor emits "
                "mechanics-only candidates at count >=2; they are not scoreable."
            ),
            parent_unresolved_reason=ambiguous_parent,
        ),
        _family(
            "MBF-THEMATIC-NODE",
            DetailedLayer.THEMATIC_NODE,
            extractor="extract_node_activation_candidates",
            feature_status=FeatureStatus.UNRESOLVED,
            parents=_unresolved_gate_parent_backoff(),
            parent_status=FeatureStatus.UNRESOLVED,
            policies=("MBD-CHANNEL-GATE", "MBD-ANCHOR-REUSE", "MBD-ALTERNATIVES"),
            sources=(salience_source, layer_source),
            unresolved_reason=(
                "All Personality/Design Node positions are mechanically available, but the "
                "protocol does not define when one is strongly thematic or map it to an answer."
            ),
            parent_unresolved_reason=ambiguous_parent,
        ),
        _family(
            "MBF-PROMINENT-ACTIVATION",
            DetailedLayer.PROMINENT_ACTIVATION,
            extractor="extract_prominent_activations",
            feature_status=FeatureStatus.UNRESOLVED,
            parents=_unresolved_gate_parent_backoff(),
            parent_status=FeatureStatus.UNRESOLVED,
            policies=("MBD-CHANNEL-GATE", "MBD-ANCHOR-REUSE", "MBD-ALTERNATIVES"),
            sources=(salience_source, layer_source),
            unresolved_reason=(
                "The normative sources do not predeclare which non-cardinal planets count as "
                "prominent; the allowlist is therefore empty and no anchors are emitted."
            ),
            parent_unresolved_reason=ambiguous_parent,
        ),
        _family(
            "MBF-HANGING-GATE",
            DetailedLayer.HANGING_GATE,
            extractor="extract_hanging_gate_candidates",
            feature_status=FeatureStatus.UNRESOLVED,
            parents=_unresolved_gate_parent_backoff(),
            parent_status=FeatureStatus.UNRESOLVED,
            policies=("MBD-CHANNEL-GATE", "MBD-ANCHOR-REUSE", "MBD-ALTERNATIVES"),
            sources=(
                salience_source,
                layer_source,
                _source(
                    V3_PROTOCOL,
                    "§33 Channels and hanging gates",
                    "A hanging gate has salience 0.35, may support behavior, and does not "
                    "become a complete channel without its counterpart.",
                ),
            ),
            unresolved_reason=(
                "The protocol does not freeze whether hanging is gate-level or channel-edge "
                "specific and supplies no justified behavior mapping. The extractor emits "
                "edge-specific mechanics-only candidates; they are not scoreable."
            ),
            parent_unresolved_reason=ambiguous_parent,
        ),
    )


def _dependency_policies() -> tuple[DependencyPolicy, ...]:
    source = _source(
        V3_PROTOCOL,
        "§10 Detailed behavioral pathways, §13, and §23 Structural reuse rule",
        "Alternative pathways compete; reuse of an exact structural anchor is controlled.",
    )
    return (
        DependencyPolicy(
            policy_id="MBD-CHANNEL-GATE",
            rule=(
                "A complete channel and either component gate share dependency keys and may "
                "not receive independent full information credit for one observation."
            ),
            sources=(
                source,
                _source(
                    V4_PROTOCOL,
                    "§15 Detailed support and contradiction",
                    "A channel and its component gates are not independent evidence.",
                ),
            ),
        ),
        DependencyPolicy(
            policy_id="MBD-CARDINAL-CROSS",
            rule=(
                "Incarnation Cross receives no separate anchor when its Personality/Design "
                "Sun/Earth cardinal activations are represented; cardinal gate and line "
                "additivity remains unresolved."
            ),
            sources=(
                _source(
                    V3_PROTOCOL,
                    "§11 Fixed structural salience classes and §23 Structural reuse rule",
                    "Cross and four constituent cardinal activations are dependent.",
                ),
            ),
        ),
        DependencyPolicy(
            policy_id="MBD-PROFILE-CARDINAL-LINE",
            rule=(
                "Personality and Design Profile roles derive mechanically from their "
                "respective Sun lines. A Profile-role line and a cardinal activation line "
                "with the same side/line share a dependency key and cannot stack full "
                "information for the same observation."
            ),
            sources=(
                _source(
                    V3_PROTOCOL,
                    "§21 Conditional prevalence and §23 Structural reuse rule",
                    "Downstream structures are conditionally weighted and reused anchors "
                    "cannot receive repeated full credit.",
                ),
                _source(
                    BODYGRAPH_IMPLEMENTATION,
                    "derive_bodygraph / _derive_profile",
                    "The deterministic engine derives Profile from Personality and Design "
                    "Sun lines.",
                ),
            ),
        ),
        DependencyPolicy(
            policy_id="MBD-ANCHOR-REUSE",
            rule=(
                "The same exact anchor receives full information once; only the strongest "
                "independent corroborator can add at most 15 percent."
            ),
            sources=(source,),
        ),
        DependencyPolicy(
            policy_id="MBD-ALTERNATIVES",
            rule=(
                "Alternative mechanisms compete by maximum supported pathway rather than "
                "summing; unsupported absence is neutral."
            ),
            sources=(
                source,
                _source(
                    V3_PROTOCOL,
                    "§15 Unsupported is not contradiction",
                    "Missing a favored detailed structure is neutral without an explicit "
                    "opposing prediction.",
                ),
            ),
        ),
    )


def _behavioral_mappings() -> tuple[UnresolvedBehaviorMapping, ...]:
    generic_source = _source(
        QUESTION_BANK,
        "purpose and rules (top-level fields)",
        "The question bank explicitly contains no chart mappings; those require a separately "
        "frozen server-side library.",
    )
    missing_directness = (
        "The repository does not freeze a predicted answer distribution, mapping-directness "
        "class, or contradiction rule for this detailed selector. It cannot score until those "
        "items are sourced and versioned or learned in a separate empirical model."
    )
    return (
        UnresolvedBehaviorMapping(
            mapping_id="MBM-CHANNEL-26-44-T08",
            structural_selector="complete_channel == 26-44",
            question_ids=("T08",),
            dependency_cluster="STRATEGIC_PERSUASION",
            sources=(
                _source(
                    V3_PROTOCOL,
                    "§30 Prospective discrimination procedure",
                    "The protocol associates Channel 26-44 with a persuasion distinction, "
                    "then requires a neutral behavior-first question.",
                ),
                _source(
                    QUESTION_BANK,
                    "question T08",
                    "T08 supplies the corresponding neutral strategic-persuasion question.",
                ),
            ),
            unresolved_reason=(
                "The association is concrete, but neither source assigns directness, a "
                "canonical answer token/distribution, or contradiction semantics. It remains "
                "unresolved rather than receiving a favorable default."
            ),
        ),
        *(
            UnresolvedBehaviorMapping(
                mapping_id=mapping_id,
                structural_selector=selector,
                dependency_cluster=cluster,
                sources=(generic_source, source),
                unresolved_reason=reason,
            )
            for mapping_id, selector, cluster, source, reason in (
                (
                    "MBM-COMPLETE-CHANNELS",
                    "any complete_channel except separately declared associations",
                    "UNRESOLVED_COMPLETE_CHANNEL",
                    _source(
                        V3_PROTOCOL,
                        "§33 Channels and hanging gates",
                        "Complete channels are an allowed structural layer, not a behavior "
                        "dictionary.",
                    ),
                    missing_directness,
                ),
                (
                    "MBM-CARDINAL-ACTIVATIONS",
                    "any Personality/Design Sun/Earth gate or line",
                    "UNRESOLVED_CARDINAL",
                    _source(
                        V3_PROTOCOL,
                        "§32 Cardinal placements",
                        "Cardinals are allowed at fixed salience without bespoke per-gate "
                        "bonuses.",
                    ),
                    missing_directness,
                ),
                (
                    "MBM-DEFINITION",
                    "any definition pattern",
                    "UNRESOLVED_DEFINITION",
                    _source(
                        V4_PROTOCOL,
                        "§21 Layer 1",
                        "Definition is scoring-relevant architecture, but no behavioral key is "
                        "provided.",
                    ),
                    missing_directness,
                ),
                (
                    "MBM-REPEATED-GATES",
                    "any repeated-gate candidate",
                    "UNRESOLVED_REPEATED_GATE",
                    _source(
                        V4_PROTOCOL,
                        "§21 Layer 2",
                        "Repeated gates are activation transitions, not a supplied behavior map.",
                    ),
                    missing_directness,
                ),
                (
                    "MBM-THEMATIC-NODES",
                    "any Personality/Design Node activation candidate",
                    "UNRESOLVED_THEMATIC_NODE",
                    _source(
                        V4_PROTOCOL,
                        "§21 Layer 2",
                        "Nodes are activation transitions, not a supplied behavior map.",
                    ),
                    missing_directness,
                ),
                (
                    "MBM-PROMINENT-ACTIVATIONS",
                    "any other prominent planetary activation",
                    "UNRESOLVED_PROMINENT_ACTIVATION",
                    _source(
                        V3_PROTOCOL,
                        "§11 Fixed structural salience classes",
                        "Other prominent activations are named, but prominence is not defined.",
                    ),
                    missing_directness,
                ),
                (
                    "MBM-HANGING-GATES",
                    "any justified hanging-gate candidate",
                    "UNRESOLVED_HANGING_GATE",
                    _source(
                        V3_PROTOCOL,
                        "§33 Channels and hanging gates",
                        "Hanging gates may support behavior only through a frozen mapping.",
                    ),
                    missing_directness,
                ),
            )
        ),
    )


def build_model_b_artifact(project_root: str | Path) -> ModelBArtifact:
    root = Path(project_root)
    bank = load_question_bank(root / QUESTION_BANK)
    sources = tuple(
        SourceArtifact(path=path, sha256=sha256_file(root / path))
        for path in (*NORMATIVE_SOURCES, BODYGRAPH_IMPLEMENTATION, MODEL_A_MAPPING)
    )
    channels = tuple(
        sorted(
            (channel.identifier for channel in CHANNELS),
            key=lambda item: tuple(int(part) for part in item.split("-")),
        )
    )
    return ModelBArtifact(
        base_mapping_sha256=sha256_file(root / MODEL_A_MAPPING),
        question_bank_version=bank.version,
        question_bank_sha256=sha256_file(root / QUESTION_BANK),
        source_artifacts=sources,
        channel_catalog=channels,
        structural_families=_structural_families(),
        dependency_policies=_dependency_policies(),
        prevalence_policy=ConditionalPrevalencePolicy(
            sources=(
                _source(
                    V3_PROTOCOL,
                    "§18 Reference universe for prevalence",
                    "Prevalence is duration weighted over the global reference universe and "
                    "never estimated from a candidate CSV.",
                ),
                _source(
                    V3_PROTOCOL,
                    "§21 Conditional prevalence and dependency control",
                    "Use the frozen hierarchy, back off when the parent group is too small, "
                    "and target 500 duration-weighted state equivalents.",
                ),
            )
        ),
        behavioral_mappings=_behavioral_mappings(),
    )


def compile_model_b_artifacts(
    project_root: str | Path,
    *,
    artifact_path: str | Path | None = None,
    report_path: str | Path | None = None,
) -> CompilationResult:
    root = Path(project_root)
    output = (
        Path(artifact_path)
        if artifact_path
        else root / "mappings/model_b_mapping_library_v1.json"
    )
    report_output = (
        Path(report_path)
        if report_path
        else root / "mappings/model_b_unresolved_mapping_report_v1.json"
    )
    artifact = build_model_b_artifact(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            artifact.model_dump(mode="json", exclude_none=False),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    file_hash = hashlib.sha256(output.read_bytes()).hexdigest()
    frozen_count = sum(
        item.feature_status is FeatureStatus.FROZEN for item in artifact.structural_families
    )
    unresolved_count = len(artifact.structural_families) - frozen_count
    report = ModelBUnresolvedReport(
        artifact_semantic_sha256=artifact.sha256(),
        artifact_file_sha256=file_hash,
        frozen_feature_family_count=frozen_count,
        unresolved_feature_family_count=unresolved_count,
        unresolved_behavior_mapping_count=len(artifact.behavioral_mappings),
        limitations=(
            "No detailed behavioral mapping is scoreable: the normative sources do not "
            "freeze directness and predicted response semantics for any detailed anchor.",
            "Channel 26-44 and T08 are associated, but directness and answer direction remain "
            "unresolved.",
            "Gate 57 and Gate 18 are only neutral-absence examples, not behavioral mappings.",
            "Gates 1, 8, 24, 26, 44, and 61 occur only in a forbidden post-search conjunction "
            "example and are not compiled as a rule.",
            "Repeated-gate threshold semantics, thematic-Node criteria, prominent-body "
            "allowlist, hanging-gate eligibility, cardinal gate-versus-line additivity, and "
            "several exact conditional parent sets remain unresolved.",
            "Model B therefore emits and hashes detailed feature anchors for audit and future "
            "prevalence work, but currently delegates canonical questionnaire answers to the "
            "unchanged Model A core library.",
        ),
    )
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(
        json.dumps(report.model_dump(mode="json"), ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    return CompilationResult(
        artifact_path=str(output),
        report_path=str(report_output),
        artifact_semantic_sha256=artifact.sha256(),
        artifact_file_sha256=file_hash,
        frozen_feature_family_count=frozen_count,
        unresolved_feature_family_count=unresolved_count,
        unresolved_behavior_mapping_count=len(artifact.behavioral_mappings),
    )
