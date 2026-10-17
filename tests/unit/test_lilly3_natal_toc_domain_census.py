"""Verify original-source-anchored Lilly III subject census, not astrology scores."""

from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "tasks/lilly-book3-domain-census-20261017"
CENSUS = TASK / "LILLY3-NATAL-DOMAIN-CENSUS-v1.json"
BANK = ROOT / "tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json"


def test_original_book_three_contents_are_source_anchored():
    data = json.loads(CENSUS.read_text())
    assert data["schema"] == "lilly3-natal-original-contents-domain-census-v1"
    assert data["status"] == "CONTENTS_ONLY_NOT_RULE_LEVEL_OR_PREDICTIVE_VALIDATION"
    source = data["source"]
    assert source["original_full_ocr_size_bytes"] == 2005702
    assert source["original_full_ocr_sha256"] == (
        "7c08b55359c41049c5d43901b8da869a326f8eb852e4a30603a4b698533626aa"
    )
    assert source["contents_section_char_start"] == 86275
    assert source["contents_section_char_end"] == 96952
    rows = data["records"]
    assert len(rows) == data["counts"]["source_topics"] == 29
    assert len({r["id"] for r in rows}) == len(rows)
    assert all(
        source["contents_section_char_start"]
        <= row["original_ocr_character_offset"]
        < source["contents_section_char_end"]
        for row in rows
    )
    for row in rows:
        assert row["original_contents_heading_ocr_exact"] in row["original_ocr_excerpt"]
        assert row["original_ocr_excerpt"]
        assert row["printed_page_fidelity"].startswith("approximate_original_OCR")
        assert row["actual_chart_rule_checked"] is False
        assert row["this_record_predictive_scoring_authorized"] is False
        assert row["rule_not_to_be_inferred_from_index"] is True


def test_groups_match_current_v7_bank_without_conflating_life_outcomes_and_scenarios():
    data = json.loads(CENSUS.read_text())
    bank = json.loads(BANK.read_text())
    assert bank["version"] == data["survey"]["version"]
    assert bank["node_count"] == 79
    rows = data["records"]
    families = set(bank["families"])
    assert all(
        set(row["v7_families_with_partial_or_proxy_relevance_only"]) <= families for row in rows
    )
    coverage = Counter(row["v7_coverage_category"] for row in rows)
    assert dict(coverage) == data["counts"]["v7_coverage_category"]
    assert coverage["absent"] == 6
    assert coverage["proxy_only"] == 6
    assert coverage["partial"] == 4
    assert coverage["not_a_participant_trait"] == 7
    assert coverage["exclude_from_routine_survey"] == 4
    assert coverage["outside_behavioral_survey_scope"] == 2
    assert sum(coverage.values()) == 29
    assert data["counts"]["complete_original_page_folio_adjudication"] is False


def test_preregistered_conceptual_boundaries_and_prior_accepted_chapters():
    data = json.loads(CENSUS.read_text())
    assert all(
        not flag
        for key, flag in data["gates"].items()
        if isinstance(flag, bool) and key != "no_birth_data_accessed"
    )
    assert data["gates"]["no_birth_data_accessed"] is True
    rows = {r["id"]: r for r in data["records"]}
    for old in ("L3-TOC-018", "L3-TOC-019"):
        assert rows[old]["already_independently_audited"]
    for risk in ("L3-TOC-003", "L3-TOC-013", "L3-TOC-024", "L3-TOC-025"):
        assert rows[risk]["v7_coverage_category"] == "exclude_from_routine_survey"
    for technique in ("L3-TOC-001", "L3-TOC-026", "L3-TOC-027", "L3-TOC-028"):
        assert rows[technique]["v7_coverage_category"] == "not_a_participant_trait"


def test_source_generator_fails_closed_on_invalid_or_drifted_witness():
    spec = importlib.util.spec_from_file_location(
        "lilly3_toc_census_builder", TASK / "build_toc_census.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert json.loads(CENSUS.read_text())["source"]["original_full_ocr_sha256"] == module.SHA
    assert len(module.ROWS) == 29
    with pytest.raises(ValueError, match="source OCR bytes/hash mismatch"):
        module.compile_census(b"reconstructed from memory instead of original")
