from __future__ import annotations

import json
import shutil
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any, cast

import pytest
from pydantic import ValidationError

from hdmatch.model_b.scoring import score_detailed_symbolic
from hdmatch.model_b.types import (
    ConditionalPrevalenceProvider,
    EvaluatedPathway,
    StructuralEvidence,
)
from hdmatch.model_b_v2_new.artifacts import (
    CompleteChannelSelector,
    DefinitionSelector,
    ExactActivationSelector,
    ExactNodeSelector,
    ModelFreezeReceipt,
    PreregistrationArtifact,
    ProminentActivationSelector,
    QualifiedHangingPersonalityEdgeSelector,
    RepeatedGateSelector,
    selector_dependency_keys,
)
from hdmatch.model_b_v2_new.compiler import (
    compile_model_b_v2_new,
    freeze_model_b_v2_new,
)
from hdmatch.model_b_v2_new.evaluator import (
    canonical_detailed_answers,
    evaluate_compiled_model,
)
from hdmatch.model_b_v2_new.prevalence import prepare_prevalence
from hdmatch.model_b_v2_new.runtime import FrozenModelBV2New
from hdmatch.model_b_v2_new.selectors import selector_matches
from hdmatch.schemas import (
    Activation,
    BehavioralResponse,
    CandidateState,
    ChartFeatures,
    LocalDateOverlap,
)

PROJECT_ROOT = Path(__file__).parents[2]
PREREG_PATH = Path("reference/prospective/model_b_detailed_v2_new_preregistration_v1.json")


def _copied_repository(tmp_path: Path) -> tuple[Path, Path]:
    raw = json.loads((PROJECT_ROOT / PREREG_PATH).read_text(encoding="utf-8"))
    paths = {
        raw["behavioral_target"]["path"],
        raw["question_bank"]["path"],
        raw["model_a_base"]["path"],
        *(item["path"] for item in raw["local_methods"]),
        *(item["local_path"] for item in raw["source_catalog"]),
    }
    for relative in sorted(paths):
        source = PROJECT_ROOT / relative
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    preregistration = tmp_path / PREREG_PATH
    preregistration.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PROJECT_ROOT / PREREG_PATH, preregistration)
    return tmp_path, preregistration


def _compile_in(root: Path, preregistration: Path, name: str = "compiled.json") -> Path:
    output = root / "mappings" / name
    compile_model_b_v2_new(
        repository_root=root,
        preregistration_path=preregistration,
        compiled_output_path=output,
    )
    return output


def _chart(
    *,
    overrides: dict[str, tuple[int, int]] | None = None,
    channels: tuple[str, ...] = (),
    defined_centers: tuple[str, ...] = (),
    definition: str = "no_definition",
) -> ChartFeatures:
    bodies = (
        "sun",
        "earth",
        "moon",
        "north_node",
        "south_node",
        "mercury",
        "venus",
        "mars",
        "jupiter",
        "saturn",
        "uranus",
        "neptune",
        "pluto",
    )
    replacements = overrides or {}
    activations: dict[str, Activation] = {}
    longitude = 0.0
    for side in ("personality", "design"):
        for body in bodies:
            gate, line = replacements.get(f"{side}:{body}", (64, 1))
            activations[f"{side}:{body}"] = Activation(
                side=side,  # type: ignore[arg-type]
                body=body,
                longitude=longitude,
                gate=gate,
                line=line,
            )
            longitude += 1.0
    return ChartFeatures(
        personality_utc=datetime(2000, 1, 1, tzinfo=UTC),
        design_utc=datetime(1999, 10, 1, tzinfo=UTC),
        type="projector",
        strategy="wait_for_invitation",
        authority="splenic",
        profile="2/4",
        definition=definition,
        defined_centers=defined_centers,
        channels=channels,
        activations=activations,
    )


def _state(chart: ChartFeatures, index: int) -> CandidateState:
    start = datetime(2000, 1, 1, tzinfo=UTC) + timedelta(hours=index)
    end = start + timedelta(hours=1)
    return CandidateState(
        state_id=f"state-{index}",
        start_utc=start,
        end_utc=end,
        chart_features_hash=f"{index + 1:064x}",
        chart_features=chart,
        local_date_overlaps=(LocalDateOverlap(date=date(2000, 1, 1), seconds=3600.0),),
    )


def test_compiler_rejects_outcome_provenance_and_is_byte_deterministic(
    tmp_path: Path,
) -> None:
    root, preregistration = _copied_repository(tmp_path)
    first = _compile_in(root, preregistration, "first.json")
    second = _compile_in(root, preregistration, "second.json")
    assert first.read_bytes() == second.read_bytes()

    raw: dict[str, Any] = json.loads(preregistration.read_text(encoding="utf-8"))
    raw["source_catalog"][0]["local_path"] = "reference/legacy_runs/ranks.json"
    with pytest.raises(ValidationError, match="forbidden outcome-bearing provenance"):
        PreregistrationArtifact.model_validate(raw)

    contradiction_raw: dict[str, Any] = json.loads(preregistration.read_text(encoding="utf-8"))
    contradiction_raw["observations"][1]["prediction"]["contradiction_rationale"] = (
        "The gate is absent from this chart."
    )
    with pytest.raises(ValidationError, match="generic negation or absence"):
        PreregistrationArtifact.model_validate(contradiction_raw)


def test_selector_mechanics_enforce_defined_center_and_personality_scope() -> None:
    chart = _chart(
        overrides={
            "personality:sun": (1, 2),
            "design:earth": (1, 5),
            "personality:north_node": (8, 3),
            "personality:uranus": (8, 4),
        },
        channels=("1-8",),
        defined_centers=("g", "throat"),
        definition="single_definition",
    )
    assert selector_matches(chart, CompleteChannelSelector(channel="1-8"))
    assert selector_matches(
        chart,
        ExactActivationSelector(
            side="personality", body="sun", granularity="gate_line", gate=1, line=2
        ),
    )
    assert selector_matches(chart, DefinitionSelector(definition="single_definition"))
    assert selector_matches(chart, RepeatedGateSelector(gate=1))
    assert selector_matches(
        chart,
        ExactNodeSelector(side="personality", body="north_node", gate=8, line=3),
    )
    assert selector_matches(
        chart,
        ProminentActivationSelector(side="personality", body="uranus", gate=8),
    )
    assert not selector_matches(
        chart.model_copy(update={"defined_centers": ("throat",)}),
        RepeatedGateSelector(gate=1),
    )

    hanging = _chart(
        overrides={"personality:sun": (8, 2)},
        defined_centers=("throat",),
    )
    selector = QualifiedHangingPersonalityEdgeSelector(
        channel="1-8", active_gate=8, missing_complement_gate=1
    )
    assert selector_matches(hanging, selector)
    assert not selector_matches(
        hanging.model_copy(update={"defined_centers": ()}),
        selector,
    )
    complement_present = dict(hanging.activations)
    complement_present["design:earth"] = complement_present["design:earth"].model_copy(
        update={"gate": 1}
    )
    assert not selector_matches(
        hanging.model_copy(update={"activations": complement_present}),
        selector,
    )


def test_complementary_gate_families_fail_closed_across_clusters() -> None:
    chart = _chart(
        overrides={"personality:sun": (32, 2), "personality:earth": (54, 3)},
        defined_centers=("spleen", "root"),
    )
    gate_32 = ExactActivationSelector(side="personality", body="sun", granularity="gate", gate=32)
    gate_54 = ExactActivationSelector(side="personality", body="earth", granularity="gate", gate=54)
    assert selector_matches(chart, gate_32)
    assert selector_matches(chart, gate_54)
    assert "channel-family:32-54" in selector_dependency_keys(gate_32)
    assert "channel-family:32-54" in selector_dependency_keys(gate_54)

    def pathway(
        identifier: str, cluster: str, selector: ExactActivationSelector
    ) -> EvaluatedPathway:
        return EvaluatedPathway(
            rule_id=f"rule-{identifier}",
            dependency_cluster=cluster,
            pathway_id=f"path-{identifier}",
            effective_confidence=1.0,
            primary=StructuralEvidence(
                anchor_id=f"anchor-{identifier}",
                dependency_keys=tuple(sorted(selector_dependency_keys(selector))),
                supports_response=True,
                structural_salience=0.75,
                mapping_directness=0.75,
            ),
        )

    with pytest.raises(ValueError, match="channel-family:32-54"):
        score_detailed_symbolic(
            chart,
            (
                pathway("32", "CL_RESOURCE_CALIBRATION", gate_32),
                pathway("54", "CL_AMBITION_MOTIVES", gate_54),
            ),
            cast(ConditionalPrevalenceProvider, object()),
        )


def test_competing_discovery_predictions_are_unknown_and_score_neutral(tmp_path: Path) -> None:
    root, preregistration = _copied_repository(tmp_path)
    compiled_path = _compile_in(root, preregistration)
    artifact = compile_model_b_v2_new(
        repository_root=root,
        preregistration_path=preregistration,
        compiled_output_path=compiled_path,
    )
    chart = _chart(
        overrides={
            "personality:sun": (5, 2),
            "personality:earth": (35, 3),
            "design:sun": (36, 4),
        },
        channels=("35-36",),
        defined_centers=("sacral", "throat", "solar_plexus"),
    )
    answers = canonical_detailed_answers(artifact, chart)
    assert answers["T18"] == "unknown"
    assert "T11" not in answers
    assert set(answers) == {rule.prediction.question_id for rule in artifact.rules_for_scope()}

    from hdmatch.model import load_mapping_library

    prevalence = prepare_prevalence(
        (_state(chart, 0), _state(chart, 1)),
        load_mapping_library(root / artifact.model_a_base.path),
        artifact,
    )
    responses = (
        BehavioralResponse(
            question_id="T18",
            cluster_id="test",
            answer="seek_novelty_and_variety",
            behavioral_confidence=1.0,
            measurement_reliability=1.0,
        ),
        BehavioralResponse(
            question_id="T11",
            cluster_id="test",
            answer="tell_and_package_the_story",
            behavioral_confidence=1.0,
            measurement_reliability=1.0,
        ),
    )
    pathways = evaluate_compiled_model(artifact, chart, responses)
    assert pathways
    assert all("T11" not in pathway.rule_id for pathway in pathways)
    assert all(not pathway.primary.supports_response for pathway in pathways)
    assert all(pathway.contradiction_severity == 0.0 for pathway in pathways)
    score = score_detailed_symbolic(chart, pathways, prevalence.detailed_context)
    novelty = next(
        item for item in score.clusters if item.dependency_cluster == "CL_NOVELTY_CONTINUITY"
    )
    assert novelty.evidence_rubric_bits == 0.0
    assert novelty.contradiction_rubric_bits == 0.0


def test_prevalence_backs_off_and_dependency_cluster_uses_one_winner(tmp_path: Path) -> None:
    root, preregistration = _copied_repository(tmp_path)
    compiled_path = _compile_in(root, preregistration)
    artifact = compile_model_b_v2_new(
        repository_root=root,
        preregistration_path=preregistration,
        compiled_output_path=compiled_path,
    )
    chart = _chart(
        overrides={"personality:sun": (32, 2)},
        defined_centers=("spleen",),
    )
    states = (_state(chart, 0), _state(chart, 1))
    from hdmatch.model import load_mapping_library

    base = load_mapping_library(root / artifact.model_a_base.path)
    prevalence = prepare_prevalence(states, base, artifact)
    answers = canonical_detailed_answers(artifact, chart)
    responses = tuple(
        BehavioralResponse(
            question_id=question_id,
            cluster_id="test",
            answer=answer,
            behavioral_confidence=1.0,
            measurement_reliability=1.0,
        )
        for question_id, answer in answers.items()
    )
    pathways = evaluate_compiled_model(artifact, chart, responses)
    score = score_detailed_symbolic(chart, pathways, prevalence.detailed_context)
    resource = [
        item for item in score.clusters if item.dependency_cluster == "CL_RESOURCE_AMBITION_32_54"
    ]
    assert len(resource) == 1
    assert resource[0].evidence_rubric_bits == max(
        item.evidence_rubric_bits for item in resource[0].evaluated_pathways
    )
    matching_anchor = next(
        pathway.primary.anchor_id for pathway in pathways if pathway.primary.supports_response
    )
    estimate = prevalence.detailed_context.estimate(matching_anchor, chart)
    assert estimate.duration_weighted is True
    assert estimate.selected_conditioning_values == ()
    assert estimate.backoff_level > 0


def test_freeze_runtime_binds_compiled_base_and_source_software(tmp_path: Path) -> None:
    root, preregistration = _copied_repository(tmp_path)
    compiled_path = _compile_in(root, preregistration)
    receipt_path = root / "mappings" / "freeze.json"
    receipt = freeze_model_b_v2_new(
        repository_root=root,
        preregistration_path=preregistration,
        compiled_artifact_path=compiled_path,
        freeze_receipt_output_path=receipt_path,
        source_software_commit="a" * 40,
        source_software_tree="b" * 40,
        frozen_at_utc=datetime(2026, 8, 22, tzinfo=UTC),
    )
    runtime = FrozenModelBV2New(
        compiled_path,
        receipt_path,
        base_mapping_path=root / receipt.model_a_base.path,
    )
    assert runtime.model_id == "MODEL-B-DETAILED-V2-NEW"
    assert runtime.capability_metadata["assignment_scope"] == "discovery"
    assert runtime.capability_metadata["holdout"] == "frozen-withheld"
    assert runtime.capability_metadata["scientific_claim"] == (
        "engineering-discovery-only-not-holdout-validation"
    )
    assert {"T04", "T06", "T11"}.isdisjoint(runtime.answer_spaces())

    shared = {
        "channels": ("1-8",),
        "defined_centers": ("g", "throat"),
    }
    holdout_a = _chart(
        overrides={"personality:sun": (33, 2)},
        **shared,  # type: ignore[arg-type]
    )
    holdout_b = _chart(
        overrides={"personality:sun": (56, 2)},
        **shared,  # type: ignore[arg-type]
    )
    assert runtime.oracle_responses(holdout_a) == runtime.oracle_responses(holdout_b)
    assert runtime.score_signature(holdout_a) == runtime.score_signature(holdout_b)
    assert all(item.question_id != "T11" for item in runtime.oracle_responses(holdout_a))

    states = (_state(holdout_a, 0), _state(holdout_b, 1))
    prepared = runtime.prepare_prevalence(states)
    responses = runtime.oracle_responses(holdout_a)
    assert (
        runtime.score(states[0], responses, prepared).model_dump()
        == runtime.score(states[1], responses, prepared)
        .model_copy(update={"state_id": states[0].state_id})
        .model_dump()
    )

    unrelated_channel = holdout_a.model_copy(update={"channels": ("1-8", "3-60")})
    assert runtime.score_signature(holdout_a) != runtime.score_signature(unrelated_channel)

    tampered = root / "mappings" / "tampered-compiled.json"
    tampered.write_bytes(compiled_path.read_bytes() + b" ")
    with pytest.raises(ValueError, match="compiled V2 bytes"):
        FrozenModelBV2New(
            tampered,
            receipt_path,
            base_mapping_path=root / receipt.model_a_base.path,
        )

    tampered_base = root / "mappings" / "tampered-base.json"
    tampered_base.write_bytes((root / receipt.model_a_base.path).read_bytes() + b" ")
    with pytest.raises(ValueError, match="Model A mapping bytes"):
        FrozenModelBV2New(
            compiled_path,
            receipt_path,
            base_mapping_path=tampered_base,
        )

    invalid = receipt.model_dump(mode="json")
    invalid["source_software_commit"] = "not-a-commit"
    with pytest.raises(ValidationError):
        ModelFreezeReceipt.model_validate(invalid)
