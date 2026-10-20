#!/usr/bin/env python3
"""Build four *provisional* behavior questions from exact original source lines.

No actual human data, no production astrology predictive rule and no birth
chart. The original passage is historical transmitted Chinese Wikitext, not
a critically authenticated first Ming-era printed edition or empirical truth.
"""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

TASK = Path(__file__).resolve().parent
ROOT = TASK.parents[1]
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017"
RAW = CHINA / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
INDEX = CHINA / "CHINESE_SOURCE_AUDIT_INDEX_V14.json"
OUT = TASK / "SOURCE_TO_BEHAVIOR_CANDIDATES_V1.json"
RAW_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
INDEX_SHA = "c3a85dd972e010398b671730d86b2eea671db3da313494807bcb42e2c209c770"
BATCH_ROOT = CHINA / "batches"

SOURCE = [
    {
        "id": "AZ-WUQU-DECISIVENESS",
        "source": "ChineseAstro-10SRC-Life/ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json",
        "record_id": "ZWD-R0287",
        "native_star": "武曲",
        "roman_star": "WuQu",
        "exact_fragment": "性刚果决",
        "working_gloss": "Firm/resolute decision-making",
        "target_question_id": "Q_DECISIVE",
        "question": (
            "During the past month, when you had enough information to make a "
            "routine decision, how often did you settle on a choice without "
            "repeatedly reopening it?"
        ),
        "construct": "decision commitment",
        "domain": "everyday decisions",
        "instrument_issue": (
            "Choice consistency may reflect habit, confidence or task difficulty; "
            "not a validated pure decisiveness measure."
        ),
    },
    {
        "id": "AZ-LIANZHEN-ARGUMENT",
        "source": "ChineseAstro-11SRC-Life/ZIWEI_LIFE_PALACE_NEXT_FOUR_90_SOURCE_NOTES_V1.json",
        "record_id": "ZWD-R0330",
        "native_star": "廉贞",
        "roman_star": "LianZhen",
        "exact_fragment": "好忿争",
        "working_gloss": "Inclination to contentious disagreement",
        "target_question_id": "Q_ARGUMENT",
        "question": (
            "During the past three months, when you disagreed with another person, "
            "how often did that disagreement become a verbal argument?"
        ),
        "construct": "disagreement escalation",
        "domain": "social interaction",
        "instrument_issue": (
            "Needs sufficient disagreements to be applicable; retrospective conflict "
            "reports differ by setting and culture."
        ),
    },
    {
        "id": "AZ-TIANLIANG-HELP",
        "source": "ChineseAstro-12SRC-Life/ZIWEI_LIFE_PALACE_THIRD_FOUR_83_SOURCE_NOTES_V1.json",
        "record_id": "ZWD-R0464",
        "native_star": "天梁",
        "roman_star": "TianLiang",
        "exact_fragment": "好济施",
        "working_gloss": "Inclination to help/give",
        "target_question_id": "Q_HELPING",
        "question": (
            "During the past month, when you noticed someone outside your household "
            "needed help, how often did you help voluntarily without expecting "
            "anything in return?"
        ),
        "construct": "uncompensated helping",
        "domain": "prosocial action",
        "instrument_issue": (
            "Social desirability, opportunities, income and culture likely affect "
            "reports; neutral validated instrument needed."
        ),
    },
    {
        "id": "AZ-POJUN-COMPETE",
        "source": "ChineseAstro-13SRC-Life/ZIWEI_LIFE_PALACE_FINAL_TWO_46_SOURCE_NOTES_V1.json",
        "record_id": "ZWD-R0505",
        "native_star": "破军",
        "roman_star": "PoJun",
        "exact_fragment": "好争强",
        "working_gloss": "Competitive drive",
        "target_question_id": "Q_COMPETE",
        "question": (
            "During the past three months, when taking part in a game, shared task "
            "or skill activity with others, how often did you deliberately try to "
            "outperform them?"
        ),
        "construct": "competition seeking",
        "domain": "group tasks/games",
        "instrument_issue": (
            "Requires opportunity to compete, separates hobby/sport context poorly "
            "and may not cover status striving."
        ),
    },
]
SCALE = ["never", "rarely", "sometimes", "often", "almost_always"]


def sha(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def dump(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build() -> dict:
    if sha(RAW.read_bytes()) != RAW_SHA or sha(INDEX.read_bytes()) != INDEX_SHA:
        raise ValueError("Original Chinese Wikitext or accepted canonical V14 index SHA drift")
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    if [(e["accepted_source_annotations"], e["next_id"]) for e in index["systems"]] != [
        (210, "BZI-R0211"),
        (586, "ZWD-R0587"),
    ] or index["independently_validated_real_human_claims"] != 0:
        raise ValueError("Wrong Chinese accepted original-source frontier")
    raw = RAW.read_bytes()
    full = raw.decode("utf-8")
    anchors = []
    for rec in SOURCE:
        src = BATCH_ROOT / rec["source"]
        data = json.loads(src.read_text(encoding="utf-8"))
        row = next((r for r in data["records"] if r["id"] == rec["record_id"]), None)
        if row is None:
            raise ValueError("Source record missing: " + rec["record_id"])
        quote = row["exact_original_Chinese_Wikitext_quote"]
        fragment = rec["exact_fragment"]
        cp = row["original_absolute_codepoint_offset"]
        byteoffset = row["original_absolute_UTF8_byte_offset"]
        qbytes = quote.encode("utf-8")
        if (
            row["source_line_type"] != "star_profile_intro"
            or row["star_group_native"] != rec["native_star"]
            or row["star_group_romanization"] != rec["roman_star"]
            or quote.count(fragment) != 1
            or full[cp : cp + len(quote)] != quote
            or raw[byteoffset : byteoffset + len(qbytes)] != qbytes
            or row["source_quote_sha256_UTF8"] != sha(qbytes)
            or row["original_full_source_sha256"] != RAW_SHA
        ):
            raise ValueError("Exact source intro phrase, original byte location or SHA mismatch")
        phrase_cp = cp + quote.index(fragment)
        phrase_byte = len(full[:phrase_cp].encode("utf-8"))
        phrase_utf = fragment.encode("utf-8")
        if raw[phrase_byte : phrase_byte + len(phrase_utf)] != phrase_utf:
            raise ValueError("Source target phrase UTF8 byte-offset not exact")
        anchors.append(
            {
                "candidate_id": rec["id"],
                "star_native": rec["native_star"],
                "star_roman": rec["roman_star"],
                "source_note_id": rec["record_id"],
                "source_line_file": str(src.relative_to(ROOT)),
                "source_line_file_sha256": sha(src.read_bytes()),
                "source_original_Chinese_fragment": fragment,
                "source_original_fragment_SHA256": sha(phrase_utf),
                "source_original_fragment_codepoint_offset": phrase_cp,
                "source_original_fragment_UTF8_byte_offset": phrase_byte,
                "source_full_line_SHA256": row["source_quote_sha256_UTF8"],
                "source_full_line_codepoint_offset": cp,
                "source_full_line_UTF8_byte_offset": byteoffset,
                "working_semantic_gloss_NOT_independent_translation": rec["working_gloss"],
                "draft_concealed_question_id": rec["target_question_id"],
                "draft_concealed_behavior_first_question": rec["question"],
                "behavioral_construct_candidate": rec["construct"],
                "ordinary_observation_domain": rec["domain"],
                "psychometric_construct_and_opportunity_confound": rec["instrument_issue"],
                "hypothetical_source_natal_condition": (
                    "star occupies Life palace; interpretation branch conflicts unresolved"
                ),
                "test_direction_source_hypothesis": (
                    "higher ordinal frequency, not calibrated probability"
                ),
                "original_birth_chart_calculator_for_this_condition_verified": False,
                "source_phrase_expert_translation_verified": False,
                "conditional_planetary_star_mitigations_resolved": False,
                "human_forward_reverse_validation": 0,
                "production_rule_approved": False,
            }
        )
    document = {
        "schema": "HUMANDESIGN_CHINESE_ZIWEI_SOURCE_FOUR_BEHAVIOR_CANDIDATES_V1",
        "status": "HISTORICAL_SOURCE_GROUNDED_DRAFT_NOT_FROZEN_OR_AUTHORIZED_FOR_HUMANS",
        "question_pool_item_count": 4,
        "original_Wikitext_oldid": 1963110,
        "original_Wikitext_source_path": str(RAW.relative_to(ROOT)),
        "original_Wikitext_raw_SHA256": RAW_SHA,
        "accepted_V14_index_path": str(INDEX.relative_to(ROOT)),
        "accepted_V14_index_SHA256": INDEX_SHA,
        "source_research_audit_scope": (
            "Original individual Life-palace first-paragraph claims only"
        ),
        "questionnaire_item_observability_status": "PROVISIONAL_NOT_PSYCHOMETRICALLY_VALIDATED",
        "response_categories_ordinal_0_to_4": SCALE,
        "responses_can_be_missing_or_not_applicable": True,
        "human_chart_applicability_policy": (
            "UNRESOLVED. Synthetic single-star tokens only; no birth date or natal "
            "star position accepted."
        ),
        "synthetic_chart_feature_policy": (
            "Only artificial labels with exactly one of WuQu LianZhen TianLiang "
            "PoJun, no real birth input."
        ),
        "single_source_history_for_each_hypothesis": True,
        "source_line_behavior_direction_magnitude_unquantified": True,
        "score_probabilities_calibrated": False,
        "source_excerpt_is_not_verified_Ming_printed_edition": True,
        "study_has_been_preregistered": False,
        "scored_real_human_recruitment_authorized": False,
        "scored_real_human_responses_collected": 0,
        "human_predictive_validation_count": 0,
        "production_astrological_rule_promotions": 0,
        "candidates": anchors,
    }
    dump(OUT, document)
    return document


if __name__ == "__main__":
    doc = build()
    print(
        json.dumps(
            {
                "stage": doc["status"],
                "source_count": len(doc["candidates"]),
                "source_ids": [r["source_note_id"] for r in doc["candidates"]],
                "source_hash": sha(OUT.read_bytes()),
                "verified_real_humans": 0,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
