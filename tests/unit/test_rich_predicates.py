from __future__ import annotations

from pathlib import Path

from hdmatch.model.mapping_library import (
    MAPPING_DIRECTNESS,
    STRUCTURAL_SALIENCE,
    AnswerOption,
    DirectnessClass,
    MappingStatus,
    PredictedResponse,
    QuestionAnswerSpec,
    SourceArtifact,
    SourceCitation,
    StructuralClass,
    load_mapping_library,
)
from hdmatch.model.rich_mapping_library import RichMappingLibrary, RichMappingRule
from hdmatch.model.rich_predicate import (
    ActivationGatePredicate,
    ChannelPredicate,
    DefinitionPredicate,
    EqualityPredicateOperator,
    SetPredicateOperator,
)

ROOT = Path(__file__).resolve().parents[2]
LEGACY_MAPPING_LIBRARY_SHA256 = (
    "e4b1ed725f0310b5434ca58745972b23902ee9e23a10ac795ea420ce0de8d69e"
)


def test_activation_gate_predicates_support_scope_and_set_semantics() -> None:
    chart = {
        "activation_gates": {
            "personality:sun": 1,
            "personality:moon": 7,
            "design:moon": 15,
            "design:mars": 21,
        }
    }

    assert ActivationGatePredicate(
        operator=SetPredicateOperator.CONTAINS_ANY,
        gates=(7,),
    ).matches(chart)
    assert ActivationGatePredicate(
        operator=SetPredicateOperator.CONTAINS_ALL,
        gates=(1, 7, 15),
    ).matches(chart)
    assert ActivationGatePredicate(
        operator=SetPredicateOperator.CONTAINS_ANY,
        gates=(7,),
        side="personality",
        bodies=("moon",),
    ).matches(chart)
    assert not ActivationGatePredicate(
        operator=SetPredicateOperator.CONTAINS_ANY,
        gates=(7,),
        side="design",
        bodies=("moon",),
    ).matches(chart)
    assert ActivationGatePredicate(
        operator=SetPredicateOperator.NOT_CONTAINS_ANY,
        gates=(64,),
    ).matches(chart)


def test_activation_gate_anchor_is_scope_explicit_and_canonical() -> None:
    predicate = ActivationGatePredicate(
        operator=SetPredicateOperator.CONTAINS_ANY,
        gates=(7, 1, 7),
        side="personality",
        bodies=("sun", "moon", "sun"),
    )

    assert predicate.gates == (1, 7)
    assert predicate.bodies == ("moon", "sun")
    assert predicate.anchor_id_fragment() == (
        "activation_gate:contains_any:side=personality:bodies=moon,sun:gates=1,7"
    )


def test_channel_predicate_canonicalizes_orientation_and_supports_all() -> None:
    chart = {"channels": ("8-1", "14/2", "29-46")}
    predicate = ChannelPredicate(
        operator=SetPredicateOperator.CONTAINS_ALL,
        channels=("1-8", "14-2"),
    )

    assert predicate.channels == ("1-8", "2-14")
    assert predicate.matches(chart)
    assert ChannelPredicate(
        operator=SetPredicateOperator.NOT_CONTAINS_ANY,
        channels=("10-20",),
    ).matches(chart)


def test_definition_predicate_normalizes_definition_labels() -> None:
    predicate = DefinitionPredicate(
        operator=EqualityPredicateOperator.EQUALS_ANY,
        definitions=("Split Definition", "Single"),
    )

    assert predicate.matches({"definition": "split-definition"})
    assert predicate.matches({"definition": "single"})
    assert not predicate.matches({"definition": "triple split"})


def test_rich_mapping_library_matches_gate_predicate_without_behavioral_defaults() -> None:
    mapping = RichMappingRule(
        mapping_id="MAP-RICH-TEST",
        observation_id="OBS-RICH-TEST",
        behavioral_statement="Synthetic schema-integration test only.",
        dependency_cluster="TEST",
        question_ids=("Q1",),
        status=MappingStatus.FROZEN,
        chart_feature_predicate=ActivationGatePredicate(
            operator=SetPredicateOperator.CONTAINS_ANY,
            gates=(7,),
            side="personality",
            bodies=("moon",),
        ),
        predicted_response=PredictedResponse(
            canonical_answer_token="yes",
            support_answer_tokens=("yes",),
        ),
        structural_class=StructuralClass.REPEATED_GATE_OR_NODE,
        structural_salience=STRUCTURAL_SALIENCE[StructuralClass.REPEATED_GATE_OR_NODE],
        mapping_directness_class=DirectnessClass.DIRECT,
        mapping_directness=MAPPING_DIRECTNESS[DirectnessClass.DIRECT],
        sources=(
            SourceCitation(
                path="tests/unit/test_rich_predicates.py",
                locator="synthetic fixture",
                rationale="Exercises schema integration only; not a behavioral source.",
            ),
        ),
    )
    library = RichMappingLibrary(
        question_bank_version="synthetic",
        question_bank_sha256="0" * 64,
        source_artifacts=(
            SourceArtifact(path="synthetic", sha256="1" * 64),
        ),
        answer_specs=(
            QuestionAnswerSpec(
                question_id="Q1",
                options=(
                    AnswerOption(token="yes", label="Yes", source="response_format"),
                    AnswerOption(token="no", label="No", source="response_format"),
                ),
            ),
        ),
        mappings=(mapping,),
    )
    chart = {"activation_gates": {"personality:moon": 7}}

    assert library.schema_version == "mapping-library-v2"
    assert library.matching_mappings(chart) == (mapping,)
    assert library.canonical_answers(chart) == {"Q1": "yes"}
    assert mapping.anchor_id == (
        "activation_gate:contains_any:side=personality:bodies=moon:gates=7"
    )


def test_legacy_mapping_library_canonical_hash_is_unchanged() -> None:
    legacy = load_mapping_library(ROOT / "mappings" / "mapping_library_v1.json")

    assert legacy.sha256() == LEGACY_MAPPING_LIBRARY_SHA256
