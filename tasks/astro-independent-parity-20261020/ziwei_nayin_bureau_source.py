#!/usr/bin/env python3
"""Strict transmitted Zi Wei sexagenary NaYin -> elemental bureau, with gaps.

Source: transmitted Chinese Wikisource Zi Wei Quan Shu Volume II, oldid1963110.
The five-element bureau for a PROVIDED year heavenly stem and Life-palace
earthly branch is derived from the original year-stem/Yin-palace rule and the
original 60-jiazi NaYin poem. The poem includes TWO malformed original labels
(甲戊 for 甲戌 and 已亥 for 己亥). Preserve these exact and refuse to silently
repair. Physical Ming edition/third-party horoscope parity remain unknown.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = ROOT / "tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
ORIGINAL_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
TRAD = ROOT / "tasks/astro-chinese-primary-sources-20261017"
sys.path.insert(0, str(TRAD))
from ziwei.ziwei_source_mechanics import palace_stem_from_yin  # noqa: E402

STEMS_CH = "甲乙丙丁戊己庚辛壬癸"
STEMS_ROMAN = ("Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui")
BRANCHES_CH = "子丑寅卯辰巳午未申酉戌亥"
BRANCHES_ROMAN = ("Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai")
PHASE_TO_BUREAU = {"水": "水二局", "木": "木三局", "金": "金四局", "土": "土五局", "火": "火六局"}
EXPECTED_LITERAL_ANOMALIES = {
    6: ("甲戊", "甲戌"),
    18: ("已亥", "己亥"),
}

@dataclass(frozen=True)
class Bureau:
    source_input_birth_year_stem: str
    source_input_life_palace_branch: str
    derived_source_palace_sexagenary_name: str
    original_nayin_source_poem_pair_ordinal: int
    original_nayin_source_chinese_verse: str
    original_chinese_pair_as_printed: str
    expected_canonical_cycle_pair_as_COMPUTED_not_source_emendation: str
    original_source_glyph_permitted_for_queried_natal_pillar: bool
    original_literal_status: str
    source_conditional_element_Chinese: str | None
    source_conditional_bureau_Chinese: str | None
    glyph_that_prevents_strict_source_acceptance: str | None
    derived_cycle_name_if_source_were_emended_not_adopted: str | None
    original_early_woodblock_and_editorial_authority_verified: bool
    human_chart_engine_and_person_prediction_validated: bool

def read_source_poem() -> list[dict]:
    raw = ORIGINAL.read_bytes()
    if hashlib.sha256(raw).hexdigest() != ORIGINAL_SHA:
        raise ValueError("Original frozen transmitted Zi Wei volume II source hash changed")
    text = raw.decode("utf-8")
    headline = "'''六十花甲子纳音歌'''"
    if text.count(headline) != 1:
        raise ValueError("Original NaYin section not uniquely identified")
    start = text.index(headline)
    # The introduction and the Five Yin palace stem instructions are preserved
    # in the same pinned immutable source; no new transcription substituted.
    preface = "甲己之岁起丙寅，乙庚之岁起戊寅，丙辛之岁起庚寅，丁壬之岁起壬寅，戊癸之岁起甲寅。"
    worked_example = "如甲生人安命在寅却起甲己之年丙为首，是丙寅丁卯炉中火，却去火局寻某日生期起紫微帝王"
    if text.count(preface) != 1 or text.count(worked_example) != 1:
        raise ValueError("Original source palace setup and worked chart example unavailable")
    assert text.index(preface) < start and text.index(worked_example) < start
    a = text.index("<poem>", start) + len("<poem>")
    b = text.index("</poem>", a)
    printed = text[a:b].strip()
    phrases = [x.strip(" \r\t。") for x in re.split(r"[，,\n]", printed) if x.strip(" \r\t。")]
    if len(phrases) != 30:
        raise ValueError(f"Expected 30 pairs in transmitted NaYin song, found {len(phrases)}")
    rows = []
    anomaly_set = []
    for idx,phrase in enumerate(phrases):
        ord_=idx+1
        if len(phrase) < 6 or phrase[-1] not in PHASE_TO_BUREAU:
            raise ValueError(f"Unrecognized element or truncated original NaYin phrase: {phrase}")
        expected_pair = "".join(STEMS_CH[n%10]+BRANCHES_CH[n%12] for n in (2*idx,2*idx+1))
        actual_pair = phrase[:4]
        discrepancies = []
        for j in (0,1):
            if actual_pair[2*j:2*j+2] != expected_pair[2*j:2*j+2]:
                discrepancies.append({"pair_member": j+1,
                  "transmitted_glyphs": actual_pair[2*j:2*j+2],
                  "computed_sexagenary_expected": expected_pair[2*j:2*j+2]})
        if discrepancies:
            anomaly_set.append((ord_,discrepancies[0]["transmitted_glyphs"],discrepancies[0]["computed_sexagenary_expected"]))
        rows.append({
            "poem_pair_ordinal": ord_,
            "original_phrase_exact":phrase,
            "original_phrase_source_character_offset":text.index(phrase,a,b),
            "original_phrase_UTF8_SHA256":hashlib.sha256(phrase.encode("utf-8")).hexdigest(),
            "original_written_stem_branch_pair":actual_pair,
            "cycle_expected_stem_branch_pair_NOT_original":expected_pair,
            "source_Chinese_element":phrase[-1],
            "source_elemental_bureau":PHASE_TO_BUREAU[phrase[-1]],
            "literal_mismatches_with_60_cycle":discrepancies,
            "both_original_labels_match_generated_60_cycle":not bool(discrepancies),
        })
    if anomaly_set != [(k,*v) for k,v in EXPECTED_LITERAL_ANOMALIES.items()]:
        raise ValueError(f"Source anomaly ledger drifted: {anomaly_set}")
    return rows

def conditional_source_bureau(year_stem: str, life_palace_branch: str) -> Bureau:
    if year_stem not in STEMS_ROMAN or life_palace_branch not in BRANCHES_ROMAN:
        raise ValueError("Explicit known romanized year stem and life palace branch required")
    branch_idx = BRANCHES_ROMAN.index(life_palace_branch)
    stem_roman = palace_stem_from_yin(year_stem, life_palace_branch)
    stem_idx = STEMS_ROMAN.index(stem_roman)
    # A valid sexagenary stem+branch has equal yin/yang parity, giving one
    # occurrence in the 60-cycle. Reject if source implementation changes.
    pair_matches = [i for i in range(60) if i%10 == stem_idx and i%12 == branch_idx]
    if len(pair_matches) != 1:
        raise ValueError(f"Source palace stem+branch not a unique 60-cycle pillar: {stem_roman}/{life_palace_branch}")
    n = pair_matches[0]
    pair = read_source_poem()[n//2]
    expected = pair["cycle_expected_stem_branch_pair_NOT_original"][2*(n%2):2*(n%2)+2]
    literal = pair["original_written_stem_branch_pair"][2*(n%2):2*(n%2)+2]
    if expected == literal:
        status = "EXACT_TRANSMITTED_NAYIN_SOURCE_LABEL_NOT_BIRTH_CHART_VALIDATION"
        elem = pair["source_Chinese_element"]
        bureau = pair["source_elemental_bureau"]
        failed_glyph = None
        proposed = None
    else:
        status = "UNRESOLVED_ORIGINAL_NAYIN_GLYPH_CONFLICT_NO_BUREAU_ASSIGNED"
        elem=bureau=None
        failed_glyph=literal
        proposed=expected
    return Bureau(year_stem,life_palace_branch,expected,pair["poem_pair_ordinal"],pair["original_phrase_exact"],
        pair["original_written_stem_branch_pair"],pair["cycle_expected_stem_branch_pair_NOT_original"],
        expected==literal,status,elem,bureau,failed_glyph,proposed,False,False)

def source_conditional_120():
    from collections import Counter
    rows = [asdict(conditional_source_bureau(year_stem,branch)) for year_stem in STEMS_ROMAN for branch in BRANCHES_ROMAN]
    counts = dict(sorted(Counter(x["original_literal_status"] for x in rows).items()))
    return {
        "schema":"ZIWEI_ORIGINAL_NAYIN_FIVE_BUREAU_120_CONDITIONAL_SOURCE_LABELS_V1",
        "original_source_version":"Wikisource transmitted Zi Wei Quan Shu volume II revision 1963110; early woodblock not verified",
        "source_raw_full_SHA256":ORIGINAL_SHA,
        "original_30_na_yin_couplets":[r for r in read_source_poem()],
        "source_poem_30_pairs":30,
        "computed_60_sexagenary_entries":60,
        "source_glyph_conflicts":[r for r in read_source_poem() if r["literal_mismatches_with_60_cycle"]],
        "input_year_stem_count":10,
        "input_life_palace_branch_count":12,
        "all_120_source_conditionals_kept":120,
        "conditional_source_status_counts":counts,
        "source_odd_glyphs_not_silently_emended":True,
        "verified_Gregorian_to_lunar_and_birthyear_convention":False,
        "independent_early_classical_paper_source_witness":False,
        "complete_birth_natal_fourteen_stars_and_timing_verified":False,
        "real_person_predictions_validated":0,
        "runtime_promotions":0,
        "conditional_year_stem_plus_life_palace_lookup":rows,
    }

def main():
    data=source_conditional_120()
    out=Path(__file__).resolve().parent / "ZIWEI_ORIGINAL_NAYIN_120_CONDITIONALS_20261020.json"
    out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"poem_pairs":30,"original_literal_glyph_anomalies":len(data["source_glyph_conflicts"]),
          "source_statuses":data["conditional_source_status_counts"],
          "JiaYin":asdict(conditional_source_bureau("Jia","Yin")),
          "Bazi_initial_natal_pillar_parity_and_predictive_validation":"OPEN"},ensure_ascii=False,indent=2))
if __name__ == "__main__":
    main()
