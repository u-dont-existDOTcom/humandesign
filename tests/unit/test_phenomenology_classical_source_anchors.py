"""First primary-source claim audit: tradition text != modern birth prediction."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "tasks/astrology-phenomenology-source-anchors-20261017"
SURVEY = ROOT / "tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json"
PILOT = (
    ROOT / "tasks/life-patterns-early-review-and-experience-20261017/"
    "EXPERIENCE-MEANING-PILOT-v0.json"
)


def test_each_anchor_is_located_in_a_named_historical_source_and_v7_family():
    d = json.loads((AUDIT / "PRIMARY-SOURCE-CLAIM-ANCHORS-v1.json").read_text())
    bank = json.loads(SURVEY.read_text())
    sources = {row["id"]: row for row in d["sources"]}
    ids = [claim["id"] for claim in d["claim_anchors"]]
    assert len(d["sources"]) == 2
    assert len(ids) == len(set(ids)) == 17
    assert all(x["url"].startswith("https://") for x in sources.values())
    for claim in d["claim_anchors"]:
        assert claim["source_id"] in sources
        assert claim["section_locator"]
        assert claim["traditional_chart_condition_or_topic"]
        assert claim["source_claim_paraphrase"]
        assert claim["existing_v7_coverage"] in {"partial", "proxy_only", "absent"}
        assert set(claim["existing_v7_families"]) <= set(bank["families"])
        assert claim["source_relation"].startswith("explicit_text_about_traditional")
        assert claim["frequency_or_intensity_rule_explicit"] is False
    assert "not a validated" not in d["status"].lower()  # status is a typed contract
    assert d["scope_limits"]["chart_directness"].startswith("Distinguish")


def test_awe_surprise_synchronicity_and_guidance_are_not_fabricated_classical_rules():
    d = json.loads((AUDIT / "PRIMARY-SOURCE-CLAIM-ANCHORS-v1.json").read_text())
    pilot = json.loads(PILOT.read_text())
    domain_ids = {row["id"] for row in d["claim_anchors"]}
    pilot_ids = {row["id"] for row in pilot["items"]}
    gaps = {row["construct"]: row for row in d["proposed_modern_phenomenology"]}
    assert len(gaps) == 6
    assert set(gaps) == {
        "frequency_of_awe_and_wonder",
        "frequency_of_being_shocked_by_self_or_world",
        "sudden_self_revelation_and_behavioral_revision",
        "felt_guidance_by_higher_power",
        "noticing_meaningful_coincidences_synchronicities",
        "felt_personal_meaning_and_contribution",
    }
    for row in gaps.values():
        assert row["direct_explicit_rule_in_these_sources"] is False
        assert set(row["related_claim_ids"]).issubset(domain_ids)
        assert set(row["pilot_ids"]).issubset(pilot_ids)
        assert row["source_relation"] in {"modern_extrapolation", "indirect_topic_bridge_only"}
    assert d["migration_plan"]["do_not_recode_current_interviews"] is True


def test_readback_receipt_fences_scope_and_transcription_uncertainty():
    receipt = json.loads((AUDIT / "SOURCE-HTML-CHECK-RECEIPT-v1.json").read_text())
    assert receipt["claims_count"] == 17
    assert receipt["explicit_modern_phenomenology_gaps"] == 6
    assert receipt["original_v7_question_text_unchanged"] is True
    assert receipt["owner_or_participant_answers_used"] is False
    assert receipt["neither_source_demonstrates_astrological_predictive_validity"]
    assert len(receipt["source_checks"]) == 2
    for check in receipt["source_checks"]:
        assert len(check["sha256_html"]) == 64
        assert check["downloaded_html_bytes"] >= 40000
        assert len(check["checks_passed"]) >= 4
        assert check["caveat"]
    lilly = next(x for x in receipt["source_checks"] if x["id"].startswith("LILLY"))
    assert "not proofread" in lilly["caveat"]


def test_ptolemy_book_four_expands_the_audit_without_modifying_live_questionnaire():
    new = json.loads((AUDIT / "PTOLEMY-BOOK-IV-LIFE-DOMAINS-v1.json").read_text())
    survey = json.loads(SURVEY.read_text())
    assert len(new["source_pages"]) == 3
    assert len(new["domains"]) == 9
    assert all(row["do_not_add_as_compulsory_question"] for row in new["domains"])
    assert all(set(row["v7_families"]) <= set(survey["families"]) for row in new["domains"])
    assert all(
        row["source_page_id"] in {s["id"] for s in new["source_pages"]} for row in new["domains"]
    )
    assert new["scope_control"]["survey_boundary"].startswith("All current V7")
