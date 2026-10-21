#!/usr/bin/env python3
"""Exact original Zi Wei Life palace co-star clause and 120 synthetic layout audit.

This studies what accepted historical Chinese source text LITERALLY says,
not observed human traits, original Ming woodblock authentication or any
astrological scored predictor. No behavioral reversal/weights are invented.
"""

from __future__ import annotations

import json
import subprocess
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017"
RAW = CHINA / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
INDEX = CHINA / "CHINESE_SOURCE_AUDIT_INDEX_V14.json"
MAP = (
    ROOT / "tasks/astro-source-four-anchor-synthetic-20261020/SOURCE_TO_BEHAVIOR_CANDIDATES_V1.json"
)
SOURCE_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
INDEX_SHA = "c3a85dd972e010398b671730d86b2eea671db3da313494807bcb42e2c209c770"
MAP_SHA = "acd1fef1b9764bfac4525785ee1fd42e7dac2727880e829ee038aa9562db8a62"
ORACLE_COMMIT = "6f4a75febc1624e44b54d724422804a05f31fd12"
ORACLE_FILE = (
    "tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-12/"
    "IZTRO_2_6_0_FULL_312_CHART_COMPARISON_V1.json"
)
ORACLE_SHA = "01efe5181d7c9d07a6c9f780df9d03b557b356baa4ca3770464f38e8552feaa5"
ORACLE_BYTES = 899155
ORACLE_COLD_SNAPSHOT = B / "ORIGINAL_312_SOURCE_ORACLE_SNAPSHOT.json"
SELECTED = ("WuQu", "LianZhen", "TianLiang", "PoJun")
ORIGINAL_SOURCE_FILES = {
    "WuQu": "ChineseAstro-10SRC-Life/ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json",
    "LianZhen": "ChineseAstro-11SRC-Life/ZIWEI_LIFE_PALACE_NEXT_FOUR_90_SOURCE_NOTES_V1.json",
    "TianLiang": "ChineseAstro-12SRC-Life/ZIWEI_LIFE_PALACE_THIRD_FOUR_83_SOURCE_NOTES_V1.json",
    "PoJun": "ChineseAstro-13SRC-Life/ZIWEI_LIFE_PALACE_FINAL_TWO_46_SOURCE_NOTES_V1.json",
}
CN_TO_ROMAN = {
    "子": "Zi",
    "丑": "Chou",
    "寅": "Yin",
    "卯": "Mao",
    "辰": "Chen",
    "巳": "Si",
    "午": "Wu",
    "未": "Wei",
    "申": "Shen",
    "酉": "You",
    "戌": "Xu",
    "亥": "Hai",
}
PAIR_RULES = (
    ("ZWD-R0293", "WuQu", "TianFu", "与天府同度", "子午"),
    ("ZWD-R0294", "WuQu", "QiSha", "与七杀同度", "卯酉"),
    ("ZWD-R0295", "WuQu", "TianXiang", "与天相同度", "寅申"),
    ("ZWD-R0296", "WuQu", "PoJun", "与破军同度", "巳亥"),
    ("ZWD-R0298", "WuQu", "TanLang", "与贪狼同度", "丑未"),
    ("ZWD-R0340", "LianZhen", "TianXiang", "与天相同度", "子午"),
    ("ZWD-R0341", "LianZhen", "PoJun", "与破军同度", "卯酉"),
    ("ZWD-R0344", "LianZhen", "TianFu", "与天府同度", "辰戌"),
    ("ZWD-R0345", "LianZhen", "QiSha", "与七杀同度", "丑未"),
    ("ZWD-R0469", "TianLiang", "TaiYang", "与太阳同度", "卯酉"),
    ("ZWD-R0470", "TianLiang", "TianJi", "与天机同度", "辰戌"),
    ("ZWD-R0472", "TianLiang", "TianTong", "与天同同度", "寅申"),
    ("ZWD-R0511", "PoJun", "LianZhen", "与廉贞同度", "卯酉"),
    ("ZWD-R0513", "PoJun", "ZiWei", "与紫微同度", "丑未"),
    ("ZWD-R0515", "PoJun", "WuQu", "与武曲同度", "巳亥"),
)
CLUSTER_WARNINGS = (
    (
        "ZWD-R0290",
        "WuQu",
        "与府相梁月禄马会主贵",
        "multiple planets/benefics, historical rank not decisiveness",
    ),
    (
        "ZWD-R0291",
        "WuQu",
        "更遇廉贞破军羊忌空劫冲破下局",
        "requires a collection of additional adverse placements, not WuQu+PoJun alone",
    ),
    (
        "ZWD-R0331",
        "LianZhen",
        "与擎羊同是非日有",
        "disputes with QingYang auxiliary; not a general LianZhen+any star argument formula",
    ),
    (
        "ZWD-R0339",
        "LianZhen",
        "天相同宫能化其恶",
        "TianXiang 'moderates adverse' not a quantified reversal of argumentativeness",
    ),
    (
        "ZWD-R0465",
        "TianLiang",
        "与天机同行",
        "TianJi co-occurs in historical military/service status, not a helping rate",
    ),
    (
        "ZWD-R0506",
        "PoJun",
        "天梁天府能制其恶",
        "TianLiang/TianFu mitigations do not explicitly reverse competitive seeking",
    ),
    (
        "ZWD-R0508",
        "PoJun",
        "遇廉贞羊陀火铃于陷宫，争斗疾病",
        "negative conditional multi-star cluster in fallen status; not PoJun+LianZhen pair alone",
    ),
)
OUT = B / "ORIGINAL_FOUR_BEHAVIOR_STAR_COLOCATION_SOURCE_AUDIT_V1.json"


def digest(b: bytes) -> str:
    return sha256(b).hexdigest()


def fail(why: str):
    raise ValueError("Original Chinese four-star source co-location audit rejected: " + why)


def read(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def accepted_text() -> str:
    if (
        digest(RAW.read_bytes()) != SOURCE_SHA
        or RAW.stat().st_size != 106736
        or digest(INDEX.read_bytes()) != INDEX_SHA
        or digest(MAP.read_bytes()) != MAP_SHA
    ):
        fail("accepted original Chinese oldid1963110, V14 registry or candidate map SHA changed")
    index = read(INDEX)
    if [x["accepted_source_annotations"] for x in index["systems"]] != [210, 586]:
        fail("original Chinese source registry canonical totals changed")
    question = read(MAP)
    if (
        question["human_predictive_validation_count"] != 0
        or question["score_probabilities_calibrated"] is not False
        or set(x["star_roman"] for x in question["candidates"]) != set(SELECTED)
    ):
        fail("four original source anchors not provisional or already human validated")
    return RAW.read_text(encoding="utf-8")


def source_notes() -> dict:
    records = {}
    raw = RAW.read_bytes()
    text = raw.decode("utf-8")
    for star, source in ORIGINAL_SOURCE_FILES.items():
        p = CHINA / "batches" / source
        data = read(p)
        for r in data["records"]:
            if r.get("star_group_romanization") != star:
                continue
            q = r["exact_original_Chinese_Wikitext_quote"]
            cp = r["original_absolute_codepoint_offset"]
            bp = r["original_absolute_UTF8_byte_offset"]
            qb = q.encode("utf-8")
            if (
                text[cp : cp + len(q)] != q
                or raw[bp : bp + len(qb)] != qb
                or digest(qb) != r["source_quote_sha256_UTF8"]
                or r["original_full_source_sha256"] != SOURCE_SHA
            ):
                fail("accepted original star source quote bytes/sha/offset changed")
            if r["id"] in records:
                fail("accepted source has duplicated original old text annotation ID")
            records[r["id"]] = {
                **r,
                "documentary_source_file_path": str(p.relative_to(ROOT)),
                "documentary_source_file_SHA256": digest(p.read_bytes()),
            }
    for id_, primary, *_ in PAIR_RULES:
        if id_ not in records or records[id_]["star_group_romanization"] != primary:
            fail("explicit original pair grade source ID/primary star not present")
    for id_, primary, *_ in CLUSTER_WARNINGS:
        if id_ not in records or records[id_]["star_group_romanization"] != primary:
            fail("original conditional cluster line missing")
    return records


def cited(row: dict) -> dict:
    return {
        "accepted_source_id": row["id"],
        "source_primary_star": row["star_group_romanization"],
        "source_original_oldid": 1963110,
        "source_full_original_Wikitext_sha256": SOURCE_SHA,
        "source_file_path": row["documentary_source_file_path"],
        "source_file_sha256": row["documentary_source_file_SHA256"],
        "verbatim_old_Chinese_line": row["exact_original_Chinese_Wikitext_quote"],
        "source_original_line_sha256": row["source_quote_sha256_UTF8"],
        "source_original_line_codepoint_offset": row["original_absolute_codepoint_offset"],
        "source_original_line_UTF8_byte_offset": row["original_absolute_UTF8_byte_offset"],
    }


def original_grade_witnesses(rows: dict) -> list[dict]:
    source = []
    seen = set()
    old_target_words = ("性刚果决", "好忿争", "好济施", "好争强")
    for rid, star, partner, literal, branches in PAIR_RULES:
        row = rows[rid]
        q = row["exact_original_Chinese_Wikitext_quote"]
        if (
            row["source_line_type"] != "natal_branch_condition"
            or q.count(literal) != 1
            or len(branches) != 2
            or any(c not in q for c in branches)
            or any(word in q for word in old_target_words)
        ):
            fail("source literal grade place/pair no longer exact or wrongly a behavioral target")
        key = tuple(sorted((star, partner)))
        if rid in seen:
            fail("same source rule included multiple times")
        seen.add(rid)
        source.append(
            {
                **cited(row),
                "literal_old_chinese_co_location_fragment": literal,
                "secondary_principal_star": partner,
                "mechanical_unordered_principal_star_pair": list(key),
                "source_allowed_palaces_original_Chinese": list(branches),
                "source_allowed_palaces_Earthly_roman": [CN_TO_ROMAN[c] for c in branches],
                "historical_original_scope": (
                    "natal grade/wealth/office/fortune conditional, NOT a psychological interaction"
                ),
                "historical_favourable_year_stem_and_unfavourable_qualifiers_kept_verbatim": True,
                "source_line_contains_exact_one_of_four_behavior_phrases": False,
                "fully_interpreted_year_stem_benefic_malefic_source_policy": False,
                "numerical_behavioral_trait_modifier_justified": False,
                "actual_real_person_behavior_validation": 0,
                "runtime_promotions": 0,
            }
        )
    if len(source) != 15:
        fail("expected fifteen exact original natal palace grade pairing source clauses")
    return source


def narrative_clusters(rows: dict) -> list[dict]:
    result = []
    for rid, primary, fragment, reason in CLUSTER_WARNINGS:
        row = rows[rid]
        q = row["exact_original_Chinese_Wikitext_quote"]
        if (
            row["star_group_romanization"] != primary
            or q.count(fragment) != 1
            or row["source_line_type"] != "natal_narrative_condition"
        ):
            fail("exact conditional cluster not in original accepted Chinese narrative line")
        result.append(
            {
                **cited(row),
                "exact_source_conditional_fragment": fragment,
                "qualification_unverified_English_note": reason,
                "multiple_adverse_or_benefic_conditions_may_apply": True,
                "simple_one_partner_star_behavioral_reversal_is_NOT_defined": True,
                "actual_people_verified": 0,
            }
        )
    return result


def load_external_synthetic() -> dict:
    if ORACLE_COLD_SNAPSHOT.is_file():
        # Archive-only immutable source snapshot for fresh extracted replay.
        blob = ORACLE_COLD_SNAPSHOT.read_bytes()
    else:
        cp = subprocess.run(
            ["git", "show", f"{ORACLE_COMMIT}:{ORACLE_FILE}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        )
        blob = cp.stdout
    if len(blob) != ORACLE_BYTES or digest(blob) != ORACLE_SHA:
        fail("original separately accepted synthetic 312 Iztro comparator source changed")
    data = json.loads(blob)
    if (
        data.get("synthetic_cases") != 312
        or data.get("preregistered_blinded_real_person_tests") != 0
        or len(data["all_312_case_records"]) != 312
    ):
        fail("synthetic source comparator unexpectedly contains humans/malformed data")
    return data


def compare_120_synthetic_rows(witnesses: list[dict], data: dict) -> dict:
    unique = {}
    for row in data["all_312_case_records"]:
        src = row["source_case"]
        key = (src["gregorian_reference_date"], src["hour_branch"])
        geometry = (src["life_palace"], tuple(sorted(src["star_palaces"].items())))
        if key in unique and unique[key]["geometry"] != geometry:
            fail("synthetic male/leap vendor duplicate changes original SOURCE chart")
        unique[key] = {"source": src, "geometry": geometry}
    if len(unique) != 120:
        fail("ten modern dates/twelve hours were not exactly 120 synthetic charts")
    accepted_pairs = defaultdict(list)
    for w in witnesses:
        key = tuple(w["mechanical_unordered_principal_star_pair"])
        accepted_pairs[key].append(w)
    pair_counts = Counter()
    detailed = []
    covered = 0
    for (_, hour), entry in sorted(unique.items()):
        src = entry["source"]
        life = src["life_palace"]
        stars = tuple(sorted(s for s, p in src["star_palaces"].items() if p == life))
        if len(stars) != 2 or not set(stars) & set(SELECTED):
            continue
        pair_counts[stars] += 1
        matches = [
            w
            for w in accepted_pairs.get(stars, [])
            if life in w["source_allowed_palaces_Earthly_roman"]
        ]
        if matches:
            covered += 1
        detailed.append(
            {
                "source_synthetic_reference_date": src["gregorian_reference_date"],
                "source_synthetic_two_hour_Earthly_Branch": hour,
                "source_synthetic_Life_palace": life,
                "source_principal_stars_in_Life": list(stars),
                "source_is_original_lunar_leap_month": bool(src["is_leap_month"]),
                "original_grade_source_clause_ids": [w["accepted_source_id"] for w in matches],
                "pair_and_palace_mentioned_in_original_grade_text": bool(matches),
                "source_grade_text_is_not_psychological_interaction_direction": True,
                "real_human_outcomes_scored": 0,
            }
        )
    if (len(detailed), covered, len(pair_counts)) != (22, 20, 13):
        fail("source synthetics do not match twenty of twenty-two pair/palace literal grade rows")
    unmentioned = [k for k in pair_counts if k not in accepted_pairs]
    if unmentioned != [("LianZhen", "TanLang")]:
        fail("unmentioned original grade subset pair differs from accepted source comparison")
    return {
        "raw_vendor_synthetic_comparisons": 312,
        "structurally_unique_synthetic_source_charts": 120,
        "synthetic_charts_where_selected_four_star_has_any_major_colocation": 22,
        "distinct_colocated_selected_pair_types": len(pair_counts),
        "synthetic_colocated_charts_with_exact_pair_and_life_palace_natal_grade_phrase": covered,
        (
            "synthetic_colocated_charts_with_no_matching_literal_grade_pair_"
            "in_THIS_NARROW_SOURCE_SUBSET"
        ): 22 - covered,
        "unmatched_literal_grade_pair_in_THIS_SUBSET": [list(k) for k in unmentioned],
        "pair_occurrences_in_finite_nonrepresentative_synthetic_comparator": {
            "|".join(k): v for k, v in sorted(pair_counts.items())
        },
        "all_22_explicitly_synthetic_star_pair_and_life_palace_rows": detailed,
        "no_trait_scoring_or_probability_generated": True,
        "qualifying_original_chinese_year_stem_rules_not_mechanically_resolved": True,
    }


def run() -> dict:
    original_text = accepted_text()
    rows = source_notes()
    grade = original_grade_witnesses(rows)
    clauses = narrative_clusters(rows)
    compare = compare_120_synthetic_rows(grade, load_external_synthetic())
    data = {
        "schema": (
            "HUMANDESIGN_ZIWEI_FOUR_PROVISIONAL_BEHAVIOR_STAR_ORIGINAL_CONDITIONAL_SOURCE_AUDIT_V1"
        ),
        "status": "LITERAL_OLD_SOURCE_PALACE_STAR_PAIR_TEXT_NOT_A_HUMAN_BEHAVIOR_SCORING_RULE",
        "original_transmitted_SimplifiedChinese_revision_oldid": 1963110,
        "original_transmitted_Wikitext_SHA256": SOURCE_SHA,
        "original_Wikitext_exact_unicode_codepoints": len(original_text),
        "original_scholarly_critical_early_Ming_printing_verified": False,
        "accepted_chinese_source_index_sha256": INDEX_SHA,
        "accepted_provisional_four_behavior_question_source_sha256": MAP_SHA,
        "original_15_explicit_pair_grade_source_lines": grade,
        "original_7_other_multistar_cluster_and_mitigation_source_lines": clauses,
        "original_15_grade_line_count": len(grade),
        "original_7_multistar_conditional_cluster_line_count": len(clauses),
        "distinct_accepted_original_grade_pair_types": len(
            {tuple(w["mechanical_unordered_principal_star_pair"]) for w in grade}
        ),
        "original_grade_pair_narrative_rarely_addresses_selected_four_behaviors_directly": True,
        "four_behavioral_intro_lines_contain_phrase_but_no_calibrated_effect_weight": True,
        "historical_birth_stem_and_good_bad_aspect_condition_required_to_interpret_rank": True,
        "selected_behavioral_conjunctive_interaction_magnitude_not_established": True,
        "co_star_grade_context_does_NOT_automatically_negate_unconditional_intro_trait": True,
        "sole_star_exclusion_is_a_methodological_choice_not_original_textual_requirement": True,
        (
            "source_only_defensible_frozen_future_hypothesis_might_test_each_"
            "star_presence_but_not_yet_scored"
        ): True,
        "source_absent_selected_star_is_NOT_negative_behavior_prediction": True,
        "source_ancient_gender_health_wealth_status_moral_categories_not_empirical_facts": True,
        "source_matching_against_120_synthetic_original_chart_positions": compare,
        "source_312_comparison_git_commit": ORACLE_COMMIT,
        "source_312_comparison_SHA256": ORACLE_SHA,
        "actual_consented_real_humans_tested": 0,
        "human_predictive_validations": 0,
        "astrology_runtime_model_promotions": 0,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data


if __name__ == "__main__":
    x = run()
    print(
        json.dumps(
            {
                "literal_original_grade_clause_count": x["original_15_grade_line_count"],
                "additional_multi_condition_source_notes": x[
                    "original_7_multistar_conditional_cluster_line_count"
                ],
                "original_distinct_pair_types": x["distinct_accepted_original_grade_pair_types"],
                "synthetic_source_colocated_pairs": x[
                    "source_matching_against_120_synthetic_original_chart_positions"
                ]["synthetic_charts_where_selected_four_star_has_any_major_colocation"],
                "exact_pair_palace_text_covered_synthetic": x[
                    "source_matching_against_120_synthetic_original_chart_positions"
                ]["synthetic_colocated_charts_with_exact_pair_and_life_palace_natal_grade_phrase"],
                "behavioral_interaction_weights_frozen": False,
                "actual_human_predictions": 0,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
