"""Historical Lilly III source-topic audit contracts; no natal validation claims."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "tasks/lilly-book3-religion-dreams-coverage-20261017"


def read_json(name):
    return json.loads((TASK / name).read_text())


def test_31_historical_claims_and_chapter_divisions():
    d = read_json("LILLY-BOOK3-RELIGION-DREAMS-CLAIMS-v1.json")
    entries = d["records"]
    assert len(entries) == d["count"] == 31
    assert d["sections"] == {"religion": 20, "dreams": 11}
    assert len({x["id"] for x in entries}) == 31
    assert set(x["original_printed_page"] for x in entries) <= {"611", "612", "613", "614"}
    assert all(x["original_edition"] == 1647 for x in entries)
    assert all(x["stage"] == "SOURCE_TOPIC_NOT_A_VERIFIED_CHART_PREDICTION" for x in entries)
    assert all(x["mapping_to_existing_astrohd"] == "unmapped" for x in entries)
    assert d["source"]["primary_page_image_comparison_completed"] is False
    assert d["accepted_scoring_rule_changes"] == 0


def test_original_author_qualifications_and_dream_content_categories():
    d = read_json("LILLY-BOOK3-RELIGION-DREAMS-CLAIMS-v1.json")
    records = {x["id"]: x for x in d["records"]}
    assert records["LILLY3-R20"]["claim_class"] == "author_caveat"
    assert records["LILLY3-R20"]["astrological_condition_class"] == "not_chart_predicate"
    assert records["LILLY3-R07"]["astrological_condition_class"] == "unresolved_cazimi_phrase"
    assert records["LILLY3-R06"]["source_caveat"].startswith("'Spice Virgo'")
    assert any(x["claim_class"] == "stigmatizing_historical_claim" for x in d["records"])
    assert all(
        records[f"LILLY3-D{i:02d}"]["claim_class"] == "dream_credibility_claim" for i in range(1, 4)
    )
    assert all(
        records[f"LILLY3-D{i:02d}"]["claim_class"] == "dream_content_category" for i in range(5, 12)
    )


def test_full_question_bank_direct_word_scan_and_original_ocr_receipt():
    d = read_json("WITNESS-AND-V7-CHECK-v1.json")
    bank = json.loads(
        (ROOT / "tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json").read_text()
    )
    assert d["v7_question_count"] == len(bank["questions"]) == 79
    assert d["v7_bank_version"] == bank["version"]
    assert d["textual_check_pass_count"] == d["textual_check_total"] == 12
    assert all(all(v) for v in d["original_ocr_phrase_checks"].values())
    assert all(not hits for hits in d["v7_direct_question_word_hits"].values())
    assert d["lexical_absence_is_not_semantic_absence"]
    assert not d["original_page_facsimile_glyph_check_completed"]
    assert not d["historical_chart_rules_validated_on_humans"]


def test_five_optional_probes_do_not_change_current_interviews():
    d = read_json("OPTIONAL-RELIGION-DREAM-QUESTIONS-v0.json")
    assert d["status"] == "RESEARCH_DRAFT_UNSCORED_NOT_INSTALLED"
    assert len(d["items"]) == 5
    assert len({x["id"] for x in d["items"]}) == 5
    assert all(x["none_allowed"] for x in d["items"])
    assert d["methodological_guards"]["do_not_ask_current_completed_participants"]
    assert d["methodological_guards"]["no_model_prediction_mapping_authorized"]
