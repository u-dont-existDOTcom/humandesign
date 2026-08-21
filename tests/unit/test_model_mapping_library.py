from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import pytest
from pydantic import ValidationError

from hdmatch.model.compiler import build_mapping_library, compile_mapping_artifacts
from hdmatch.model.mapping_library import (
    DirectnessClass,
    MappingStatus,
    ModelConstants,
    StructuralClass,
    load_mapping_library,
)
from hdmatch.questionnaire.bank import load_question_bank

ROOT = Path(__file__).parents[2]


def test_compiled_library_covers_every_question_conservatively() -> None:
    library = build_mapping_library(ROOT)
    bank = load_question_bank(ROOT / "reference/core/question_bank_v1.json")

    library.validate_against_question_bank(bank)
    covered = {question_id for mapping in library.mappings for question_id in mapping.question_ids}
    assert covered == bank.question_ids
    assert len(library.frozen_mappings) == 27
    assert Counter(mapping.status.value for mapping in library.mappings) == {
        "frozen": 27,
        "unresolved": 52,
        "empirical_only": 3,
    }
    empirical_questions = {
        question_id
        for mapping in library.mappings
        if mapping.status is MappingStatus.EMPIRICAL_ONLY
        for question_id in mapping.question_ids
    }
    assert empirical_questions == {"A05", "A06", "A07", "T02", "T03", "T10"}


def test_every_formal_answer_token_is_verbatim_frozen_wording() -> None:
    library = build_mapping_library(ROOT)
    bank = load_question_bank(ROOT / "reference/core/question_bank_v1.json")

    library.validate_against_question_bank(bank)
    assert all(
        option.token for answer_spec in library.answer_specs for option in answer_spec.options
    )


def test_committed_artifacts_recompile_byte_for_byte(tmp_path: Path) -> None:
    result = compile_mapping_artifacts(
        ROOT,
        mapping_path=tmp_path / "mapping.json",
        report_path=tmp_path / "report.json",
    )

    assert (tmp_path / "mapping.json").read_bytes() == (
        ROOT / "mappings/mapping_library_v1.json"
    ).read_bytes()
    assert (tmp_path / "report.json").read_bytes() == (
        ROOT / "mappings/unresolved_mapping_report_v1.json"
    ).read_bytes()
    assert (
        result.mapping_file_sha256
        == hashlib.sha256((tmp_path / "mapping.json").read_bytes()).hexdigest()
    )


def test_artifact_hash_is_semantic_and_stable() -> None:
    committed = load_mapping_library(ROOT / "mappings/mapping_library_v1.json")
    rebuilt = build_mapping_library(ROOT)

    assert committed == rebuilt
    assert committed.sha256() == rebuilt.sha256()
    report = json.loads(
        (ROOT / "mappings/unresolved_mapping_report_v1.json").read_text(encoding="utf-8")
    )
    assert report["mapping_model_sha256"] == committed.sha256()


def test_only_frozen_v3_salience_and_directness_values_are_allowed() -> None:
    with pytest.raises(ValidationError, match="information cap"):
        ModelConstants(information_cap_rubric_bits=7.0)

    library = build_mapping_library(ROOT)
    for mapping in library.frozen_mappings:
        assert mapping.structural_class in {
            StructuralClass.TYPE_STRATEGY,
            StructuralClass.AUTHORITY,
            StructuralClass.DIAGNOSTIC_CENTER,
            StructuralClass.PROFILE,
        }
        assert mapping.mapping_directness_class in {
            DirectnessClass.DIRECT,
            DirectnessClass.STRONG,
        }


def test_canonical_answers_omit_unresolved_and_conflicting_predictions() -> None:
    library = build_mapping_library(ROOT)
    chart = {
        "type": "Projector",
        "strategy": "Wait for the Invitation",
        "authority": "Splenic",
        "profile": "2/4",
        "defined_centers": ("G", "Spleen", "Throat"),
    }

    answers = library.canonical_answers(chart)

    assert answers["D01"] == "an_immediate_quiet_sense"
    assert answers["D02"] == "brief_and_nonrepeating"
    assert answers["S04"].startswith("function_better_after_a_clear_mutual_opening")
    assert answers["P09"] == "relief_and_mobilization"
    assert answers["P10"] == "extremely"
    assert "T01" not in answers
    assert "A05" not in answers


def test_mapping_predicates_accept_chart_engine_enum_values() -> None:
    library = build_mapping_library(ROOT)
    chart = {
        "type": "projector",
        "strategy": "wait_for_invitation",
        "authority": "emotional_solar_plexus",
        "profile": "5/1",
        "defined_centers": ("solar_plexus", "heart_ego", "g"),
    }

    answers = library.canonical_answers(chart)

    assert answers["D01"] == "clarity_that_changes_over_hours_or_days"
    assert answers["C02"] == "wave_like"
    assert "C03" not in answers
