# ruff: noqa: E501  # Source-specific descriptions kept intact in source code.
"""Extend frozen source-to-survey coverage without rewriting the accepted v1 audit.

The 92/46/16 baseline is immutable. New documentary entries retain exact
witness class, source limits and a separate list of 7 optional candidate topics.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TASK = Path(__file__).resolve().parent
PRIOR = ROOT / "tasks/life-patterns-source-first-audit-20261018"
OUTPUT = TASK / "EXPANDED-DOMAIN-AND-QUESTION-COVERAGE-v2.json"
ALLOWED_TYPES = {
    "existing_domain_no_new_question",
    "new_domain_candidate",
    "refines_existing_domain",
    "source_meaning_ambiguous",
    "source_interpretation_disagreement",
}
NEW_DOMAIN_STATUS = [
    (
        "formative_caregiving_arrangements",
        "Early-life caregiving setting and household changes",
        "actual_life_history_sensitive",
        "absent",
        "absent",
        "HOME;KINSHIP;TIMELINE",
    ),
    (
        "education_learning_history",
        "Actual education, training, skills and enduring study subjects",
        "real_activity_life_history",
        "proxy_only",
        "proxy_only",
        "MYSTERY;VOCATION",
    ),
    (
        "giving_receiving_help",
        "Giving and accepting practical/emotional support in real life",
        "habitual_behavior",
        "proxy_only",
        "proxy_only",
        "PARENTING;BELIEF",
    ),
    (
        "grievance_duration_repair",
        "Duration of anger and separate forgiveness/reconnection",
        "first_person_emotional_process",
        "partial",
        "partial",
        "BONDS",
    ),
    (
        "contentment_satisfaction",
        "Contentment with circumstances and desire for change separately",
        "first_person_orientation",
        "absent",
        "absent",
        "EM08",
    ),
    (
        "privacy_self_disclosure",
        "Inner life disclosure and privacy preferences",
        "habitual_communication_style",
        "proxy_only",
        "proxy_only",
        "BONDS",
    ),
    (
        "everyday_sensory_pleasure",
        "Ordinary enjoyment of foods, scents, textures, nature and sensory experience",
        "first_person_experience",
        "partial",
        "absent",
        "ART;PLAY;HOME",
    ),
]


def read(path: Path) -> dict[str, Any]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(doc, dict), path
    return doc


def build() -> dict[str, Any]:
    prior = read(PRIOR / "SOURCE-TO-SURVEY-CROSSWALK-v2.json")
    previous_questions = read(PRIOR / "ADAPTIVE-QUESTION-CANDIDATES-v1.json")
    source = read(TASK / "SOURCE-ANCHORS-v2.json")
    verified = read(TASK / "SOURCE-READBACK-v2.json")
    candidate = read(TASK / "SEVEN-NEW-TOPICS-v2.json")
    assert (
        len(prior["historical_source_claims"]) == 92
        and len(prior["domains"]) == 46
        and len(previous_questions["questions"]) == 16
    )
    assert len(source["source_anchors"]) == len(verified["anchor_readbacks"]) == 28
    assert verified["status"] == "PASS" and verified["counts"]["verified_short_phrase_rows"] == 28
    assert len(candidate["candidates"]) == len(NEW_DOMAIN_STATUS) == 7
    assert len(source["new_sources"]) == verified["counts"]["source_witnesses"] == 9
    earlier_ids = {c["claim_id"] for c in prior["historical_source_claims"]}
    baseline_domains = {c["domain_id"] for c in prior["domains"]}
    fresh_domains = {x[0] for x in NEW_DOMAIN_STATUS}
    candidate_ids = {x["id"] for x in candidate["candidates"]}
    assert len(candidate_ids) == 7
    assert not fresh_domains & baseline_domains
    assert fresh_domains == {x["domain"] for x in candidate["candidates"]}

    readback = {x["anchor_id"]: x for x in verified["anchor_readbacks"]}
    sources = {w["id"]: w for w in source["new_sources"]}
    additional = []
    for row in source["source_anchors"]:
        assert row["id"] not in earlier_ids
        assert row["id"] in readback
        assert row["witness_id"] in sources
        assert row["disposition"] in ALLOWED_TYPES
        assert not row["empirically_validated"]
        assert readback[row["id"]]["short_anchor_present"] is True
        assert row["normalized_domain"] in baseline_domains | fresh_domains
        if row["disposition"] == "new_domain_candidate":
            assert row["normalized_domain"] in fresh_domains
        additional.append(
            {
                "claim_id": row["id"],
                "witness_id": row["witness_id"],
                "reference_locator": row["locator"],
                "historical_claim_paraphrase": row["claim_paraphrase"],
                "normalized_domain_id": row["normalized_domain"],
                "disposition": row["disposition"],
                "source_translation_quality": sources[row["witness_id"]]["status"],
                "interpretation_caution": row["caution"],
                "direct_historical_survey_frequency_rule_proven": False,
                "empirically_validated_predictor": False,
            }
        )
    assert len({x["claim_id"] for x in additional}) == 28
    old_questions = {q["id"]: q for q in previous_questions["questions"]}
    new_questions = {q["id"]: q for q in candidate["candidates"]}
    assert not set(new_questions) & set(old_questions)
    domains_new = []
    for domain_id, label, kind, v7, tf1, adjacent in NEW_DOMAIN_STATUS:
        related = [
            row["claim_id"] for row in additional if row["normalized_domain_id"] == domain_id
        ]
        assert related, domain_id
        question = next(q for q in candidate["candidates"] if q["domain"] == domain_id)
        suggestions = [x for x in adjacent.split(";") if x]
        for referent in suggestions:
            if referent != "EM08":
                assert referent in old_questions, (domain_id, referent)
        assert question["previous_nearest_questions"]
        domains_new.append(
            {
                "domain_id": domain_id,
                "human_outcome": label,
                "measurement_kind": kind,
                "v7_status": v7,
                "tf1_status": tf1,
                "em_v2": "absent",
                "source_claim_ids": related,
                "suggested_optional_new_topic_id": question["id"],
                "existing_16_question_neighbor_ids": suggestions,
                "direct_source_strength": (
                    "historical_translated_topic_only_not_empirical_rule_validation"
                ),
                "original_v1_normalized_domain": False,
            }
        )

    corpus = [
        *prior["historical_source_claims"],
        *additional,
    ]
    assert len(corpus) == 120
    merged_domains = [*prior["domains"], *domains_new]
    assert len(merged_domains) == 53
    assert len({row["domain_id"] for row in merged_domains}) == 53
    detail = {
        "schema": "life-patterns-cross-tradition-expanded-domain-audit-v2",
        "status": "DOCUMENTARY_SOURCE_AUDIT_NOT_QUALITY_CERTIFICATION_OR_PREDICTIVE_TEST",
        "as_of": "2026-10-18",
        "baseline": {
            "source_path": str(PRIOR.relative_to(ROOT)),
            "documented_historical_records": 92,
            "normalized_domains": 46,
            "unactivated_optional_topic_candidates": 16,
            "sha256": hashlib.sha256(
                (PRIOR / "SOURCE-TO-SURVEY-CROSSWALK-v2.json").read_bytes()
            ).hexdigest(),
        },
        "added_witnesses": [
            {
                "id": source_witness["id"],
                "url": source_witness["url"],
                "witness_class": source_witness["type"],
                "translation_caution": source_witness["status"],
                "content_sha256_on_observed_readback": verified["source_files_or_pages"][
                    source_witness["id"]
                ]["content_sha256"],
                "git_commit_if_applicable": source_witness.get("git_commit"),
            }
            for source_witness in source["new_sources"]
        ],
        "counts": {
            "baseline_source_rows": 92,
            "new_translated_source_anchors": 28,
            "cumulative_doc_entries": 120,
            "baseline_human_domains": 46,
            "distinct_new_human_domains": 7,
            "cumulative_domains": 53,
            "baseline_optional_candidate_topics": 16,
            "new_optional_topic_candidates": 7,
            "total_candidate_topics_not_active": 23,
            "new_witnesses": 9,
            "source_dispositions": dict(Counter(x["disposition"] for x in additional)),
            "new_direct_validated_chart_rules": 0,
            "new_scored_survey_questions": 0,
        },
        "new_domains": domains_new,
        "source_anchor_dispositions": additional,
        "decision": {
            "recommended_first_survey_pilot_subset": [
                "LEARNING_HISTORY",
                "ANGER_REPAIR",
                "CONTENTMENT",
                "RECIPROCITY",
            ],
            "recommended_privacy_screen": ["UPBRINGING", "PRIVACY"],
            "probably_conditional_followup": ["SENSORY_ENJOYMENT"],
            "why_not_all": "Respondent burden and existing ART/PLAY/HOME/MYSTERY overlap; only selected, previously unmeasured topical distinctions justify new questions.",
        },
        "scope_limits": [
            "The nine verified translated witness files/pages are not the entirety of their books' conditional natal predictions.",
            "Earlier source entries and translated themes can be thematically duplicate, not independent predictive observations.",
            "Riley explicitly called his Valens English translation preliminary; a named ambiguity in the Book II ninth-house clause is preserved.",
            "Dorotheus Pingree English is from a later Middle Eastern transmission; no original Greek version was checked.",
            "The Brihat Jataka online Sanskrit/English version contains marked translator ambiguities and authorial disagreement on some rules.",
            "No live GPT, Railway, frozen participant answer or astrology scorer is changed in this design audit.",
        ],
        "chart_scorer_rule_mapping": "Unresolved: chart configurations in these traditions are conditional and cannot be read as the existing one-planet CF003 Human-Design-derived role map.",
    }
    return detail


if __name__ == "__main__":
    result = build()
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result["counts"], sort_keys=True))
