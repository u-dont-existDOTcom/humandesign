"""Source-first natal astrology domain coverage gates (research, not predictions)."""

from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "tasks/life-patterns-source-first-audit-20261018"
SPEC = importlib.util.spec_from_file_location("chart_audit", TASK / "build_crosswalk.py")
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


def read(filename: str) -> dict:
    return json.loads((TASK / filename).read_text(encoding="utf-8"))


def test_every_original_source_claim_is_accounted_for_exactly_once():
    record = AUDIT.assemble()
    ids = [r["claim_id"] for r in record["historical_source_claims"]]
    assert len(ids) == len(set(ids)) == 92
    assert Counter(r["source_type"] for r in record["historical_source_claims"]) == {
        "lilly_book3_1647_natal_contents": 29,
        "lilly_book3_1647_religion_dreams": 31,
        "ptolemy_book3_natal_soul_quality": 15,
        "ptolemy_book4_natal_life_topic": 9,
        "lilly_house_topic_horary_intro": 4,
        "brihat_jataka_ch15_natal_yoga": 4,
    }
    assert len(record["domains"]) == 46
    assert all(not r["prediction_validated"] for r in record["historical_source_claims"])
    assert all(
        r["evidence_level"] != "passage_anchored_natal"
        for r in record["historical_source_claims"]
        if r["source_type"] == "lilly_book3_1647_natal_contents"
    )
    assert all(
        r["evidence_level"] == "house_topic_only_nonnatal"
        for r in record["historical_source_claims"]
        if r["source_type"] == "lilly_house_topic_horary_intro"
    )


def test_statuses_and_specific_questionnaire_non_equivalence():
    audit = read("SOURCE-TO-SURVEY-CROSSWALK-v2.json")
    domains = {d["domain_id"]: d for d in audit["domains"]}
    assert audit["counts"]["historically_attested_domains"] == 32
    assert audit["counts"]["domains_only_modern_extrapolation"] == 14
    assert audit["counts"]["survey_v7_domain_counts"] == {
        "absent": 18,
        "partial": 9,
        "proxy_only": 13,
        "outside_scope": 6,
    }
    untouched = {
        "religious_spiritual_disposition",
        "spiritual_or_ritual_practice",
        "ascetic_renunciation_and_initiation",
        "belief_conversion_or_worldview_change",
        "esoteric_interests_omens_divination",
        "dream_content_and_tone",
        "dream_interpretation_and_beliefs",
        "creative_production",
        "aesthetic_music_engagement",
        "play_humor_spontaneous_enjoyment",
        "kinship_siblings",
        "parents_home_roots",
        "parenthood_caregiving",
    }
    assert len(untouched) == 13
    for key in untouched:
        d = domains[key]
        assert d["historically_attested_in_this_snapshot"]
        assert d["v7_questionnaire_coverage"] == "absent"
        assert d["tf1_questionnaire_coverage"] == "absent"
        assert d["em_v2_direct_question_ids"] == []
    assert domains["personal_life_meaning"]["em_v2_direct_question_ids"] == ["EM08"]
    assert domains["perceived_contribution"]["em_v2_direct_question_ids"] == ["EM08"]
    assert domains["actual_occupation_and_vocation"]["v7_questionnaire_coverage"] == "proxy_only"
    assert (
        domains["actual_marriage_partnership_history"]["v7_questionnaire_coverage"] == "proxy_only"
    )
    assert domains["actual_life_turning_points"]["v7_questionnaire_coverage"] == "proxy_only"


def test_only_attested_source_claims_support_historical_domain_conclusions():
    record = read("SOURCE-TO-SURVEY-CROSSWALK-v2.json")
    records = {r["claim_id"]: r for r in record["historical_source_claims"]}
    assert records["PT-III-MARS-VENUS-PLAY"]["evidence_level"] == (
        "new_direct_primary_passage_check"
    )
    assert records["L3-TOC-019"]["evidence_level"] == "contents_heading_only"
    assert (
        records["BJ-15.1"]["evidence_level"] == "online_secondary_translation_with_sanskrit_verse"
    )
    assert records["BJ-15.4"]["domain_id"] == "ascetic_renunciation_and_initiation"
    assert records["LILLY3-D05"]["evidence_level"].endswith("pending_v1")
    assert records["PT-IV-10"]["evidence_level"] == "chapter_level_life_domain_summary"
    assert records["LILLY-NINTH-RELIGION"]["source_type"] == ("lilly_house_topic_horary_intro")
    assert records["LILLY3-R20"]["domain_id"] == ("interpretive_freedom_and_non_determinism")
    assert not record["counts"]["predictive_accuracy_established"]


def test_ten_planet_development_mapping_not_classical_rule_replacement():
    source = read("CF003-PLANET-MAPPING-GAPS-v1.json")
    originals = json.loads(
        (ROOT / "reference/empirical_astrology/cf003_behavioral_planet_map_v0.json").read_text()
    )
    assert len(source["rows"]) == len(originals["mapping"]) == 10
    by_planet = {row["planet"]: row for row in source["rows"]}
    assert set(by_planet) == {m["planet"] for m in originals["mapping"]}
    for ref in originals["mapping"]:
        assert (
            by_planet[ref["planet"]]["actual_development_contract"]
            == (ref["target_contract_definition"])
        )
        assert not by_planet[ref["planet"]]["translation_into_computational_natal_rule_admitted"]
    assert {
        k
        for k, r in by_planet.items()
        if r["relationship_to_checked_classical_sources"].startswith("not_derived")
    } == {"pluto", "uranus", "neptune"}
    assert source["counts"]["classical_natal_predicates_replaced"] == 0


def test_fifteen_candidate_questions_are_all_optional_and_map_to_domains():
    bank = read("ADAPTIVE-QUESTION-CANDIDATES-v1.json")
    domain_rows = read("SOURCE-TO-SURVEY-CROSSWALK-v2.json")["domains"]
    domain_ids = {row["domain_id"] for row in domain_rows}
    ids = [q["id"] for q in bank["questions"]]
    assert len(ids) == len(set(ids)) == 16
    assert bank["routing"]["core_required_count"] == 0
    assert bank["routing"]["max_questions_initial"] == 0
    assert bank["routing"]["max_optional_topics_per_session"] == 5
    for item in bank["questions"]:
        assert item["question"].strip()
        assert set(item["source_domains"]) <= domain_ids
        assert item["interpretation_limit"]
        assert item["sensitivity"]
    assert "TIMELINE" in ids and "DREAM" in ids
    assert "BELIEF" in ids and "ART" in ids
    assert "RENUNCIATION" in ids
    assert "PARENTING" in ids and "RESOURCES" in ids
    assert bank["status"] == "SURVEY_DESIGN_CANDIDATE_NOT_LIVE_NOT_SCORED"


def test_reproducible_serialized_crosswalk_without_mutating_live_sources():
    expected_cross = read("SOURCE-TO-SURVEY-CROSSWALK-v2.json")
    expected_planets = read("CF003-PLANET-MAPPING-GAPS-v1.json")
    generated = AUDIT.assemble()
    assert generated == expected_cross
    assert AUDIT.planet_audit(generated) == expected_planets
    assert not any(
        r["source_type"] == "horary_question_rule_as_natal_trait"
        for r in generated["historical_source_claims"]
    )
