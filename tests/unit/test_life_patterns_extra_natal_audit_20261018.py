"""Second-stage natal source-to-question audit: actual witnesses versus 46-domain v1."""

from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "tasks/life-patterns-extra-natal-audit-20261018"
SOURCE = TASK / "SOURCE-ANCHORS-v2.json"
READBACK = TASK / "SOURCE-READBACK-v2.json"
EXTENDED = TASK / "EXPANDED-DOMAIN-AND-QUESTION-COVERAGE-v2.json"
BANK = TASK / "SEVEN-NEW-TOPICS-v2.json"
PREVIOUS = ROOT / "tasks/life-patterns-source-first-audit-20261018"

SPEC = importlib.util.spec_from_file_location("extra_natal_audit", TASK / "build_expanded_audit.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def load(path: Path) -> dict:
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(doc, dict)
    return doc


def test_source_readback_completed_and_all_claims_bounded():
    anchors = load(SOURCE)
    proof = load(READBACK)
    assert len(anchors["new_sources"]) == 9
    assert len(anchors["source_anchors"]) == 28
    assert proof["status"] == "PASS"
    assert proof["counts"]["missing_rows"] == 0
    assert proof["counts"]["verified_short_phrase_rows"] == 28
    assert len({x["id"] for x in anchors["source_anchors"]}) == 28
    assert not any(x["empirically_validated"] for x in anchors["source_anchors"])
    by_id = {s["id"]: s for s in anchors["new_sources"]}
    assert by_id["VALENS-I-STARS"]["sha256"] == (
        "fbd9cdb44c4de1f63f718bc74f9a85be3643f125478b8d1ac7b31c16fbf59820"
    )
    assert by_id["VALENS-I-STARS"]["git_commit"].startswith("2d4a8b98")
    assert all(
        proof["source_files_or_pages"][k]["source_translation_status"] == by_id[k]["status"]
        for k in by_id
    )


def test_source_claims_classify_disputes_and_original_transmission():
    anchors = load(SOURCE)
    mapping = {a["id"]: a for a in anchors["source_anchors"]}
    assert mapping["V-II-IX-AMBIGUOUS"]["disposition"] == "source_meaning_ambiguous"
    assert mapping["BJ-XXI-INTERPRETIVE-DISPUTE"]["disposition"] == (
        "source_interpretation_disagreement"
    )
    assert mapping["V-I-SATURN-PRIVACY"]["caution"] == ("do_not_equate_privacy_with_lying")
    assert mapping["D-I-UPBRINGING"]["disposition"] == "new_domain_candidate"
    assert mapping["BJ-XVII-LINGERING-ANGER"]["disposition"] == "new_domain_candidate"
    assert mapping["V-I-VENUS-ART"]["disposition"] == "existing_domain_no_new_question"
    assert all(
        item["proof_fragment"].strip() and item["locator"].strip()
        for item in anchors["source_anchors"]
    )


def test_prior_audit_unchanged_and_expanded_numbers_are_non_pseudovalidation():
    previous = load(PREVIOUS / "SOURCE-TO-SURVEY-CROSSWALK-v2.json")
    assert len(previous["domains"]) == 46
    assert len(previous["historical_source_claims"]) == 92
    generated = MODULE.build()
    actual = load(EXTENDED)
    assert generated == actual
    assert actual["counts"]["baseline_source_rows"] == 92
    assert actual["counts"]["new_translated_source_anchors"] == 28
    assert actual["counts"]["cumulative_doc_entries"] == 120
    assert actual["counts"]["baseline_human_domains"] == 46
    assert actual["counts"]["distinct_new_human_domains"] == 7
    assert actual["counts"]["cumulative_domains"] == 53
    assert actual["counts"]["total_candidate_topics_not_active"] == 23
    assert actual["counts"]["new_scored_survey_questions"] == 0
    assert actual["counts"]["new_direct_validated_chart_rules"] == 0
    assert Counter(row["disposition"] for row in actual["source_anchor_dispositions"]) == {
        "new_domain_candidate": 18,
        "refines_existing_domain": 5,
        "existing_domain_no_new_question": 3,
        "source_meaning_ambiguous": 1,
        "source_interpretation_disagreement": 1,
    }


def test_every_new_domain_has_nonredundant_source_and_optional_question():
    previous_questions = load(PREVIOUS / "ADAPTIVE-QUESTION-CANDIDATES-v1.json")
    old_ids = {q["id"] for q in previous_questions["questions"]}
    old_domains = {
        row["domain_id"] for row in load(PREVIOUS / "SOURCE-TO-SURVEY-CROSSWALK-v2.json")["domains"]
    }
    new = load(BANK)
    assert new["previous_candidate_count"] == 16
    assert len(new["candidates"]) == 7
    new_ids = {q["id"] for q in new["candidates"]}
    assert len(new_ids) == 7 and not new_ids & old_ids
    new_domains = {row["domain"] for row in new["candidates"]}
    assert len(new_domains) == 7 and not new_domains & old_domains
    expanded = load(EXTENDED)
    all_claims = {row["claim_id"] for row in expanded["source_anchor_dispositions"]}
    assert all(q["source_claim_ids"] for q in new["candidates"])
    assert all(set(q["source_claim_ids"]) <= all_claims for q in new["candidates"])
    assert {row["domain_id"] for row in expanded["new_domains"]} == new_domains
    assert {row["suggested_optional_new_topic_id"] for row in expanded["new_domains"]} == new_ids
    assert "LEARNING_HISTORY" in new_ids
    assert "ANGER_REPAIR" in new_ids
    assert "CONTENTMENT" in new_ids
    assert "RECIPROCITY" in new_ids
    assert "UPBRINGING" in new_ids


def test_sensitive_questions_stay_optional_and_prospective_scoring_untouched():
    new = load(BANK)
    assert new["status"] == "RESEARCH_CANDIDATE_DO_NOT_ACTIVATE_LIVE_OR_SCORE"
    assert "not prospectively chart-scored" in new["non_scoring_and_blinding"]
    assert "at most 5 optional topics total" in new["selection"]
    for q in new["candidates"]:
        assert q["question"].strip()
        assert q["caution"].strip()
        assert len(q["dimensions"]) >= 2
        assert q["newness"]
        assert q["previous_nearest_questions"]
    by_id = {q["id"]: q for q in new["candidates"]}
    assert "No assumption" in by_id["UPBRINGING"]["caution"]
    assert "Do not ask what actual secrets are" in by_id["PRIVACY"]["caution"]
    assert "food pleasure" in by_id["SENSORY_ENJOYMENT"]["caution"]


def test_all_nine_valens_book_headings_scanned_but_not_claimed_rule_exhaustive():
    proof = load(READBACK)
    headings = proof["valens_nine_book_section_heading_scan"]
    assert headings["total_headings"] == 252
    assert set(headings["headings_by_book"]) == {str(x) for x in range(1, 10)}
    assert not headings["full_section_contents_exhaustively_reviewed"]
    assert sum(headings["headings_by_book"].values()) == 252


def test_published_anchor_fragments_respect_per_source_quote_limit():
    anchors = load(SOURCE)
    from collections import defaultdict

    words_by_source = defaultdict(int)
    for row in anchors["source_anchors"]:
        words_by_source[row["witness_id"]] += len(row["proof_fragment"].split())
    assert max(words_by_source.values()) <= 25
    assert all(count > 0 for count in words_by_source.values())


def test_generated_source_and_domain_csvs_match_saved_crosswalk():
    import csv
    from io import StringIO

    expanded = load(EXTENDED)
    cases = [
        (
            "FIFTY-THREE-DOMAIN-CROSSWALK.csv",
            expanded["counts"]["cumulative_domains"],
            "domain_id",
        ),
        (
            "TWENTY-EIGHT-NEW-SOURCE-ANCHORS.csv",
            expanded["counts"]["new_translated_source_anchors"],
            "anchor_id",
        ),
    ]
    for filename, n, index_key in cases:
        text = (TASK / filename).read_text(encoding="utf-8")
        rows = list(csv.DictReader(StringIO(text)))
        assert len(rows) == n
        assert len({r[index_key] for r in rows}) == n
    questions = (TASK / "SEVEN-ADDITIONAL-OPTIONAL-QUESTIONS.md").read_text()
    for item in load(BANK)["candidates"]:
        assert "## " + item["id"] in questions
        assert item["question"] in questions
    assert questions.count("**Ask:**") == 7


def test_combined_twenty_three_question_bank_preserves_prior_sixteen_exactly():
    older = load(PREVIOUS / "ADAPTIVE-QUESTION-CANDIDATES-v1.json")
    current = load(BANK)
    combined = load(TASK / "TWENTY-THREE-OPTIONAL-QUESTIONS-v2.json")
    assert combined["status"] == "EXPERIMENTAL_NOT_LIVE_NOT_SCORED"
    assert len(combined["questions"]) == 23
    assert len({x["id"] for x in combined["questions"]}) == 23
    for before, after in zip(older["questions"], combined["questions"][:16], strict=True):
        assert after["id"] == before["id"]
        assert after["question"] == before["question"]
        assert after["optional_followup"] == before["optional_followup"]
        assert after["answer_dimensions"] == before["answer_dimensions"]
        assert after["already_live"] is False
    new_by_id = {x["id"]: x for x in combined["questions"][16:]}
    assert set(new_by_id) == {x["id"] for x in current["candidates"]}
    for before in current["candidates"]:
        after = new_by_id[before["id"]]
        assert after["question"] == before["question"]
        assert after["optional_followup"] == before["followup"]
        assert after["already_live"] is False
    txt = (TASK / "TWENTY-THREE-OPTIONAL-QUESTIONS.md").read_text()
    assert txt.count("**Ask:**") == 23
    assert "at most five" in txt.lower()
