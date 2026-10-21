#!/usr/bin/env python3
"""Source-exact Zi Wei Life-palace overlap of four selected behavior phrases.

Finite PREDECLARED Chinese expressions; no blanket NLP semantic inference.
Exact whole Wikitext/codepoint/UTF8 bytes/accepted note SHA checked.
Original 14-star synthetic chart comparison controls literal main-star
overlap only; it does not calculate auxiliary star positions or validate
any human personality/medical/wealth predictions.
"""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from hashlib import sha256
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017"
RAW = CHINA / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
INDEX = CHINA / "CHINESE_SOURCE_AUDIT_INDEX_V14.json"
CANDIDATE = (
    ROOT / "tasks/astro-source-four-anchor-synthetic-20261020/SOURCE_TO_BEHAVIOR_CANDIDATES_V1.json"
)
ORACLE_SHA = "01efe5181d7c9d07a6c9f780df9d03b557b356baa4ca3770464f38e8552feaa5"
ORACLE_COMMIT = "6f4a75febc1624e44b54d724422804a05f31fd12"
ORACLE_PATH = (
    "tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-12/"
    "IZTRO_2_6_0_FULL_312_CHART_COMPARISON_V1.json"
)
COLD_ORACLE = B / "ORIGINAL_312_SOURCE_ORACLE_SNAPSHOT.json"
RAW_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
INDEX_SHA = "c3a85dd972e010398b671730d86b2eea671db3da313494807bcb42e2c209c770"
CANDIDATE_SHA = "acd1fef1b9764bfac4525785ee1fd42e7dac2727880e829ee038aa9562db8a62"
LIFE_START = 19953
LIFE_END = 37269

SOURCE_GROUPS = {
    "TaiYang": (
        21372,
        22207,
        "ChineseAstro-10SRC-Life/ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json",
    ),
    "WuQu": (
        22207,
        22909,
        "ChineseAstro-10SRC-Life/ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json",
    ),
    "LianZhen": (
        23557,
        24407,
        "ChineseAstro-11SRC-Life/ZIWEI_LIFE_PALACE_NEXT_FOUR_90_SOURCE_NOTES_V1.json",
    ),
    "TianLiang": (
        27995,
        28621,
        "ChineseAstro-12SRC-Life/ZIWEI_LIFE_PALACE_THIRD_FOUR_83_SOURCE_NOTES_V1.json",
    ),
    "PoJun": (
        29332,
        30135,
        "ChineseAstro-13SRC-Life/ZIWEI_LIFE_PALACE_FINAL_TWO_46_SOURCE_NOTES_V1.json",
    ),
    "WenQu": (
        30665,
        31212,
        "ChineseAstro-14SRC-Life/ZIWEI_LIFE_FIRST_FOUR_AUXILIARY_58_SOURCE_NOTES_V1.json",
    ),
    "YouBi": (
        31613,
        31937,
        "ChineseAstro-14SRC-Life/ZIWEI_LIFE_FIRST_FOUR_AUXILIARY_58_SOURCE_NOTES_V1.json",
    ),
    "QingYang": (32650, 33270, None),
}
TARGETS = {
    "resoluteness_lexeme": "果决",
    "generosity_exact": "好济施",
    "generosity_reversed_word_order": "好施济",
    "contention_intro_exact": "好忿争",
    "contention_conditional": "是非日有",
    "competition_intro_exact": "好争强",
    "conflict_adverse_cluster": "争斗疾病",
    "aggression_adjacent_lexeme": "好勇斗狠",
}
EXPECTED_OCCURRENCES = {
    "果决": (("WuQu", "ZWD-R0287"), ("WenQu", "ZWD-R0548"), ("QingYang", None)),
    "好济施": (("TaiYang", "ZWD-R0263"), ("TianLiang", "ZWD-R0464")),
    "好施济": (("YouBi", "ZWD-R0576"),),
    "好忿争": (("LianZhen", "ZWD-R0330"),),
    "是非日有": (("LianZhen", "ZWD-R0331"),),
    "好争强": (("PoJun", "ZWD-R0505"),),
    "争斗疾病": (("PoJun", "ZWD-R0508"),),
    "好勇斗狠": (("QingYang", None),),
}
# Manually reviewed source-local direct conditional wording. The descriptive
# tags merely classify original grammatical context, NOT astrological effect.
QUALIFICATIONS = {
    ("果决", "WuQu"): ("star_intro_general", "武曲性刚果决"),
    ("果决", "WenQu"): ("multiple_stars_and_palace_required", "若与同梁武曲会旺宫，聪明果决"),
    ("果决", "QingYang"): ("star_intro_in_temple_context", "入庙权贵，身旺形粗破相，刚强果决"),
    ("好济施", "TaiYang"): ("star_intro_with_temple_and_day_night_context", "太阳入庙形貌堂堂"),
    ("好济施", "TianLiang"): ("star_intro_general", "心无私曲好济施"),
    ("好施济", "YouBi"): ("star_intro_in_temple_context", "入庙厚重清秀耿直"),
    ("好忿争", "LianZhen"): ("star_intro_general", "性硬浮荡，好忿争"),
    ("是非日有", "LianZhen"): ("with_QingYang_auxiliary_condition", "与擎羊同是非日有"),
    ("好争强", "PoJun"): ("star_intro_general", "性刚寡合，好争强"),
    ("争斗疾病", "PoJun"): (
        "fallen_palace_with_multiple_adverse_stars",
        "遇廉贞羊陀火铃于陷宫，争斗疾病",
    ),
    ("好勇斗狠", "QingYang"): (
        "star_intro_in_temple_context",
        "入庙权贵，身旺形粗破相，刚强果决，好勇斗狠",
    ),
}
OUT = B / "ZIWEI_LIFE_BEHAVIORAL_LEXEME_OVERLAP_SOURCE_AUDIT_V1.json"


def digest(b: bytes) -> str:
    return sha256(b).hexdigest()


def fail(reason: str) -> None:
    raise ValueError("Original ZiWei behavioral lexeme source audit refused: " + reason)


def read(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def accepted_source() -> tuple[bytes, str]:
    raw = RAW.read_bytes()
    if (
        len(raw) != 106736
        or digest(raw) != RAW_SHA
        or digest(INDEX.read_bytes()) != INDEX_SHA
        or digest(CANDIDATE.read_bytes()) != CANDIDATE_SHA
    ):
        fail("accepted raw Wikitext, Chinese V14 source index or four-star hypothesis SHA changed")
    idx = read(INDEX)
    if [x["accepted_source_annotations"] for x in idx["systems"]] != [210, 586] or idx[
        "independently_validated_real_human_claims"
    ] != 0:
        fail("Chinese original source index changed its documentary/human validation boundary")
    m = read(CANDIDATE)
    if (
        m["human_predictive_validation_count"] != 0
        or m["study_has_been_preregistered"] is not False
        or m["score_probabilities_calibrated"] is not False
    ):
        fail("candidate source prompts can only be uncalibrated draft model")
    full = raw.decode("utf-8")
    if not full[LIFE_START:].startswith("===一 命宫===") or not full[LIFE_END:].startswith(
        "===二兄弟==="
    ):
        fail("original Life-palace and Siblings section boundary moved")
    return raw, full


def source_note_record(star: str, line: str, cp: int, bp: int) -> tuple[dict | None, Path | None]:
    start, end, source = SOURCE_GROUPS[star]
    if not start <= cp < end:
        fail("source phrase location is outside its original star-profile text segment")
    if source is None:
        # QingYang original source text is not currently accepted as an
        # annotated first-four auxiliary source batch; archive RAW quote only.
        return None, None
    path = CHINA / "batches" / source
    j = read(path)
    eligible = []
    for r in j["records"]:
        q = r.get("exact_original_Chinese_Wikitext_quote")
        if q is None:
            q = r.get("source_original_exact_Chinese_Wikitext_quote")
        loc = r.get("original_absolute_codepoint_offset", r.get("absolute_codepoint_offset"))
        b = r.get("original_absolute_UTF8_byte_offset", r.get("absolute_UTF8_byte_offset"))
        if q == line and loc == cp and b == bp:
            eligible.append(r)
    if len(eligible) != 1:
        fail("expected exactly one accepted original text annotated note for covered phrase")
    r = eligible[0]
    qsha = r.get("source_quote_sha256_UTF8", r.get("source_quote_sha256"))
    if qsha != digest(line.encode("utf-8")):
        fail("accepted original source note line quote SHA changed")
    oldsha = r.get("original_full_source_sha256", r.get("original_full_source_SHA256"))
    if oldsha != RAW_SHA:
        fail("accepted source note references a different Wikitext original")
    st = r.get("star_group_romanization", r.get("star_roman"))
    if st != star:
        fail("historical star owner mismatch in original accepted source file")
    return r, path


def phrase_inventory() -> list[dict]:
    raw, full = accepted_source()
    lexemes = []
    if set(EXPECTED_OCCURRENCES) != set(TARGETS.values()):
        fail("predetermined literal source phrase universe altered")
    for label, word in TARGETS.items():
        actual = [m.start() for m in re.finditer(re.escape(word), full)]
        expected = EXPECTED_OCCURRENCES[word]
        if len(actual) != len(expected):
            fail("accepted original transmitted Wikitext full-volume phrase frequency drift")
        star_sequence = []
        for pos in actual:
            if not LIFE_START <= pos < LIFE_END:
                fail("target behavior phrase occurs outside first original Life-palace section")
            star_names = [
                star for star, (start, end, _) in SOURCE_GROUPS.items() if start <= pos < end
            ]
            if len(star_names) != 1:
                fail("original behavioral lexical occurrence not in one validated star segment")
            star = star_names[0]
            star_sequence.append(star)
            (kind, qualifier) = QUALIFICATIONS[(word, star)]
            line_start = full.rfind("\n", 0, pos) + 1
            end = full.find("\n", pos)
            if end < 0:
                end = len(full)
            line = full[line_start:end].strip()
            cp = line_start + len(full[line_start:end]) - len(full[line_start:end].lstrip())
            bytepos = len(full[:cp].encode("utf-8"))
            wordbytes = word.encode("utf-8")
            wordbytepos = len(full[:pos].encode("utf-8"))
            rawline = line.encode("utf-8")
            if (
                line.count(word) != 1
                or qualifier not in line
                or full[cp : cp + len(line)] != line
                or raw[bytepos : bytepos + len(rawline)] != rawline
                or raw[wordbytepos : wordbytepos + len(wordbytes)] != wordbytes
            ):
                fail("original behavioral phrase and line codepoint/UTF8 byte offsets drift")
            note, source = source_note_record(star, line, cp, bytepos)
            target = next((rid for expectedstar, rid in expected if expectedstar == star), None)
            if (note["id"] if note else None) != target:
                fail("same original phrase no longer maps to its accepted historical annotation ID")
            lexemes.append(
                {
                    "source_id": f"ZWDS-LEX-{len(lexemes) + 1:03d}",
                    "lexical_construct_bucket": label,
                    "verbatim_narrow_Chinese_phrase": word,
                    "original_occurrence_source_star": star,
                    "original_star_source_section_range_codepoints": [
                        SOURCE_GROUPS[star][0],
                        SOURCE_GROUPS[star][1],
                    ],
                    "original_Chinese_full_context_line": line,
                    "original_full_context_line_sha256_UTF8": digest(rawline),
                    "original_full_context_line_codepoint_offset": cp,
                    "original_full_context_line_UTF8_byte_offset": bytepos,
                    "source_word_exact_codepoint_offset": pos,
                    "source_word_exact_UTF8_byte_offset": wordbytepos,
                    "source_word_exact_sha256_UTF8": digest(wordbytes),
                    "transmitted_full_original_source_oldid": 1963110,
                    "transmitted_full_original_source_SHA256": RAW_SHA,
                    "already_accepted_historical_source_annotation_id": note["id"]
                    if note
                    else None,
                    "source_record_status": "ACCEPTED_SOURCE_NOTE_AND_RAW_WITNESS"
                    if note
                    else "RAW_WIKITEXT_ONLY_NOT_YET_ACCEPTED_AS_SEPARATE_SOURCE_NOTE",
                    "accepted_source_annotation_file": str(source.relative_to(ROOT))
                    if source
                    else None,
                    "accepted_source_annotation_file_SHA256": (
                        digest(source.read_bytes()) if source else None
                    ),
                    "original_phrase_context_tag": kind,
                    "original_qualifier_fragment_used_for_context": qualifier,
                    "expert_full_original_chinese_translation_verified": False,
                    "word_order_or_semantic_equivalence_validated": False,
                    "literal_lexical_source_frequency_is_human_trait_prevalence": False,
                    "human_predictive_validation": 0,
                }
            )
        if tuple(star_sequence) != tuple(x[0] for x in expected):
            fail(f"accepted star identity/order of source lexical hits changed for {word}")
    if len(lexemes) != 11:
        fail("expected exactly 11 original source occurrences in predefined lexeme vocabulary")
    return lexemes


def synthetic_major_star_baseline() -> dict:
    if COLD_ORACLE.is_file():
        content = COLD_ORACLE.read_bytes()
    else:
        content = subprocess.run(
            ["git", "show", f"{ORACLE_COMMIT}:{ORACLE_PATH}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
    if len(content) != 899155 or digest(content) != ORACLE_SHA:
        fail("accepted synthetic original Zi Wei 312-row oracle SHA changed")
    source = read(COLD_ORACLE) if COLD_ORACLE.is_file() else json.loads(content)
    state = {}
    for r in source["all_312_case_records"]:
        s = r["source_case"]
        key = (s["gregorian_reference_date"], s["hour_branch"])
        geometry = (s["life_palace"], tuple(sorted(s["star_palaces"].items())))
        if key in state and geometry != state[key]["geometry"]:
            fail("sex/vendor leap duplicate source chart differs in original geometry")
        state[key] = {"record": s, "geometry": geometry}
    if len(state) != 120:
        fail("source vendor comparison is not 120 unique synthetic chart states")
    total = Counter()
    overlap = []
    for key, p in sorted(state.items()):
        s = p["record"]
        majors = {star for star, loc in s["star_palaces"].items() if loc == s["life_palace"]}
        for star in ("TaiYang", "TianLiang", "WuQu"):
            total[star] += star in majors
        both = {"TaiYang", "TianLiang"} <= majors
        total["TaiYang_or_TianLiang"] += bool(majors & {"TaiYang", "TianLiang"})
        total["TaiYang_and_TianLiang"] += both
        if both:
            overlap.append(
                {
                    "fictional_reference_date": key[0],
                    "fictional_hour_branch": key[1],
                    "source_Life_palace": s["life_palace"],
                    "source_two_stars_with_exact_same_help_lexeme": ["TaiYang", "TianLiang"],
                    "human_survey_answers_collected": 0,
                }
            )
    expected = {
        "TaiYang": 10,
        "TianLiang": 8,
        "WuQu": 9,
        "TaiYang_or_TianLiang": 16,
        "TaiYang_and_TianLiang": 2,
    }
    if dict(total) != expected or len(overlap) != 2:
        fail("source synthetic chart selected-star overlap count drift")
    return {
        "accepted_vendor_synthetic_dataset_git_commit": ORACLE_COMMIT,
        "exact_synthetic_vendor_chart_dataset_sha256": ORACLE_SHA,
        "synthetic_comparator_raw_cases": 312,
        "synthetic_comparator_unique_source_chart_structures": 120,
        "main_star_Life_presence_synthetic_only": dict(total),
        "same_exact_helping_phrase_both_main_stars_in_two_source_charts": overlap,
        "WenQu_YouBi_QingYang_auxiliary_star_positions_computed_here": False,
        "calendar_dates_are_purposefully_selected_not_population": True,
        "synthetic_main_star_overlap_cannot_establish_behavioral_trait_validity": True,
    }


def run() -> dict:
    inventory = phrase_inventory()
    baseline = synthetic_major_star_baseline()
    d = {
        "schema": "HUMANDESIGN_ZIWEI_FOUR_PROVISIONAL_BEHAVIORAL_PHRASE_SOURCE_LEXEME_AUDIT_V1",
        "status": (
            "PINNED_ORIGINAL_CHINESE_LITERAL_LEXEMES_NOT_TRANSCULTURAL_TRAIT_OR_ASTROLOGY_PROOF"
        ),
        "transmitted_source_volume": "紫微斗數全書 卷二",
        "transmitted_source_revision_oldid": 1963110,
        "full_original_raw_sha256": RAW_SHA,
        "original_Life_palace_section_absolute_codepoint_range": [LIFE_START, LIFE_END],
        "source_ming_woodblock_early_printing_independently_authenticated": False,
        "accepted_chinese_V14_source_index_sha256": INDEX_SHA,
        "provisional_previous_four_trait_source_mapping_sha256": CANDIDATE_SHA,
        "original_verbatim_narrow_lexeme_counts_whole_volume": {
            k: len(EXPECTED_OCCURRENCES[k]) for k in EXPECTED_OCCURRENCES
        },
        "exact_occurrences_total_in_predeclared_lexical_set": len(inventory),
        "verbatim_behavior_related_lexical_source_witnesses": inventory,
        "source_only_unannotated_auxiliary_QingYang_raw_lexeme_hits": sum(
            x["source_record_status"].startswith("RAW_WIKITEXT_ONLY") for x in inventory
        ),
        "identical_giving_phrase_in_two_different_principal_stars": ["TaiYang", "TianLiang"],
        "different_order_similar_giving_lexeme_in_auxiliary_YouBi": True,
        "resoluteness_lexeme_in_star_narratives": ["WuQu", "WenQu", "QingYang"],
        "resoluteness_WenQu_requires_named_co_present_stars_and_favourable_house": True,
        "resoluteness_QingYang_auxiliary_chart_engine_not_in_14_main_stars": True,
        (
            "source_same_chinese_lexeme_occurrence_does_NOT_equal_"
            "independent_human_predicted_evidence"
        ): True,
        "source_related_phrases_semantically_synonymous_without_expert_review": False,
        (
            "source_behavior_lexical_uniqueness_not_sufficient_for_discriminative_chart_prediction"
        ): True,
        "quantified_behavior_effect_directions_and_conditional_priority_unresolved": True,
        "source_behavioral_leakage_risk_if_exclusive_star_fingerprint_assumed": True,
        "source_star_placements_only_synthetic": baseline,
        "participant_natal_birth_coordinates_or_answers_included": 0,
        "human_forward_reverse_validations": 0,
        "production_astrological_personality_rules": 0,
    }
    OUT.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return d


if __name__ == "__main__":
    result = run()
    print(
        json.dumps(
            {
                "exact_narrow_original_Chinese_lexical_occurrences": result[
                    "exact_occurrences_total_in_predeclared_lexical_set"
                ],
                "source_annotated": len(
                    result["verbatim_behavior_related_lexical_source_witnesses"]
                )
                - result["source_only_unannotated_auxiliary_QingYang_raw_lexeme_hits"],
                "RAW_only_QingYang": result[
                    "source_only_unannotated_auxiliary_QingYang_raw_lexeme_hits"
                ],
                "identical_giving_wording_stars": result[
                    "identical_giving_phrase_in_two_different_principal_stars"
                ],
                "synthetic_helping_star_Life_chart_overlap_count": result[
                    "source_star_placements_only_synthetic"
                ]["main_star_Life_presence_synthetic_only"]["TaiYang_and_TianLiang"],
                "human_predictive_validations": 0,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
