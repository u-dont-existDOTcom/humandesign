from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).parents[2]


def _coverage_runner() -> ModuleType:
    path = ROOT / "scripts" / "audit_astrohd_questionnaire_coverage.py"
    spec = importlib.util.spec_from_file_location("audit_astrohd_questionnaire_coverage", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _exposure_runner() -> ModuleType:
    path = ROOT / "scripts" / "audit_astrohd_theory_language_exposure.py"
    spec = importlib.util.spec_from_file_location("audit_astrohd_theory_language_exposure", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_current_coverage_is_descriptive_and_has_no_expansion_target() -> None:
    runner = _coverage_runner()
    report = runner.build_report(
        ROOT / "reference/core/question_bank_v1.json",
        ROOT / "mappings/mapping_library_v1.json",
        ROOT / "reference/research/astrohd_theory_language_codebook_v0_1.json",
    )

    assert report["counts"] == {
        "question_bank_total": 81,
        "nonvalidation_question_records": 76,
        "validation_question_records": 5,
        "mapping_rules_total": 82,
        "frozen_mapping_rules": 27,
        "unique_frozen_question_records": 23,
        "unique_empirical_only_question_records": 6,
        "unique_unresolved_question_records": 52,
    }
    assert report["scope"]["questionnaire_expansion_authorized"] is False
    assert report["scope"]["required_additional_question_count"] is None
    assert report["scope"]["numeric_target_prohibited"] is True
    stored = json.loads(
        (
            ROOT / "reference/research/astrohd_current_questionnaire_coverage_audit_v1.json"
        ).read_text(encoding="utf-8")
    )
    assert stored == report


def test_coverage_preserves_dependencies_and_prompt_leakage_boundary() -> None:
    runner = _coverage_runner()
    report = runner.build_report(
        ROOT / "reference/core/question_bank_v1.json",
        ROOT / "mappings/mapping_library_v1.json",
        ROOT / "reference/research/astrohd_theory_language_codebook_v0_1.json",
    )

    characteristics = report["frozen_rule_characteristics"]
    assert characteristics["mapping_directness_counts"] == {"direct": 22, "strong": 5}
    assert characteristics["repeated_dependency_clusters"]
    assert characteristics["questions_shared_by_multiple_frozen_rules"]
    assert (
        report["prompt_language_scan"]["theory_specific_occurrence_requires_prompt_echo_handling"]
        is False
    )
    assert report["prompt_language_scan"]["not_a_measure_of_participant_exposure"] is True


def test_exposure_dry_run_report_passes_every_acceptance_check() -> None:
    runner = _exposure_runner()
    report = runner.run_dry_run(
        ROOT / "reference/research/astrohd_theory_language_codebook_v0_1.json",
        ROOT / "reference/research/astrohd_theory_language_exposure_fixtures_v0_1.json",
    )

    assert report["case_count"] == 10
    assert report["passed_case_count"] == 10
    assert all(report["acceptance_checks"].values())
    stored = json.loads(
        (ROOT / "reference/research/astrohd_theory_language_exposure_dry_run_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    assert stored == report
