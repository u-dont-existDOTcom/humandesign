#!/usr/bin/env python3
"""Guarded V19 online source-only registry append; never a person forecast."""
from __future__ import annotations

import copy
from hashlib import sha256
import json
from pathlib import Path
import subprocess

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V18.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V19.json"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
PRIOR_NOTES=T/"batches/ChineseAstro-18SRC-Spouses/ZIWEI_SPOUSES_25_SOURCE_NOTES_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261021_19SRC_CHILDREN.md"
REC=B/"recovery"
RECEIPT=B/"CANONICAL_PREPARE_RECEIPT_20261021.json"
DOC=B/"ZIWEI_CHILDREN_34_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_CHILDREN_34_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT=B/"SOURCE_1963110_CHILDREN_EXACT_EXCERPT.txt"
BRANCH="research/astro-chinese-v19-ziwei-children-original-source-20261021"
OLD_SHA="d3bdefc69a441140b9b16ef82bd10aad786a3d31e9919e5baec821fbe009e9eb"
RAW_SHA="1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
WEST_SHA="c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"


def sha(p:Path)->str:
    return sha256(p.read_bytes()).hexdigest()


def rd(p:Path)->dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save(p:Path,obj:object)->None:
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def git(*args:str)->str:
    return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()


def untouched(p:Path)->None:
    rel=p.relative_to(ROOT).as_posix()
    if git("rev-parse","HEAD:"+rel)!=git("hash-object",str(p)):
        raise ValueError("Previously accepted file changed: "+rel)


def accept()->None:
    if git("branch","--show-current")!=BRANCH:
        raise ValueError("Wrong child Chinese source writer branch")
    if any(p.exists() for p in (NEW,REC,LATEST,RECEIPT)):
        raise ValueError("Interrupted V19 index append: inspect files, no blind retry")
    for p,s in ((OLD,OLD_SHA),(RAW,RAW_SHA),(WEST,WEST_SHA)):
        if sha(p)!=s:
            raise ValueError("Original text/source index SHA changed: "+str(p))
    for p in (OLD,RAW,WEST,PRIOR_NOTES,CURRENT):
        untouched(p)
    old=rd(OLD)
    doc=rd(DOC)
    wit=rd(WIT)
    meta=rd(B/"ACCEPTANCE.json")
    archive=rd(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
    if (old["sum_source_annotations"],old["original_chinese_source_anchors_checked_against_revision"])!=(1004,932):
        raise ValueError("Unexpected accepted source V18 count")
    if [(s["accepted_source_annotations"],s["next_id"]) for s in old["systems"]] != [
        (210,"BZI-R0211"),(794,"ZWD-R0795")
    ]:
        raise ValueError("BaZi or ZiWei prior source frontier moved")
    if old["accepted_batches"][-1]["id"]!="ChineseAstro-18SRC-Spouses":
        raise ValueError("Previous branch source batch list moved")
    if old["independently_validated_real_human_claims"] or old["runtime_promotions"]:
        raise ValueError("Historical record misclassified as empirical prediction")
    if (len(doc["records"]),len(wit["original_quotes"])) != (34,34):
        raise ValueError("Source/witness notes incomplete")
    if [row["id"] for row in doc["records"]] != [f"ZWD-R{x:04d}" for x in range(795,829)]:
        raise ValueError("Historical source ID gaps")
    if doc["excerpt_span_codepoints"] != [39218,40563] or doc["next_id"] != "ZWD-R0829":
        raise ValueError("Exact original source boundary drift")
    if (doc["source_method_preamble_lines"],doc["source_wrapped_continuation_lines"])!=(4,4):
        raise ValueError("Original source dependencies lost")
    if doc["original_Ming_printing_independently_authenticated"] or doc["human_blind_predictive_validations"] or doc["runtime_astrological_promotions"]:
        raise ValueError("Historical source over-promoted")
    hashes=[sha(DOC),sha(WIT),sha(EXCERPT)]
    if (meta["source_notes_SHA256"],meta["source_excerpt_SHA256"])!=(hashes[0],hashes[2]):
        raise ValueError("Frozen source record hashes changed")
    if wit["source_excerpt_SHA256"]!=hashes[2] or wit["source_full_SHA256"]!=RAW_SHA:
        raise ValueError("Witness differs from original source")
    if (archive["ZIP_CRC_verified"],archive["all_members_SHA256_and_bytes_verified"],
        archive["independent_cold_source_tests_green"])!=(True,True,13):
        raise ValueError("Cold ZIP proof missing")
    p=Path(archive["local_archive_path"])
    if not p.is_file() or sha(p)!=archive["archive_sha256"]:
        raise ValueError("ZIP archive changed after cold-extracted verification")
    for row in doc["records"]:
        if row["independent_human_blind_predictive_validations"] or row["runtime_astrological_promotions"]:
            raise ValueError("Original source incorrectly labeled human success")
    REC.mkdir(exist_ok=False)
    for source,dest in ((OLD,"CHINESE_V18_BEFORE_19.json"),
                        (CURRENT,"CHINESE_CURRENT_BEFORE_19.md"),
                        (WEST,"WESTERN_B07bc_BEFORE_19.json")):
        (REC/dest).write_bytes(source.read_bytes())
    nextidx=copy.deepcopy(old)
    nextidx.update({
        "schema":"ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V19",
        "status":"ZIWEI_CHILDREN_ONLINE_SOURCE_DOCUMENTED_NEXT_WEALTH_ALL_HOUSES_OPEN",
        "prior_index":"CHINESE_SOURCE_AUDIT_INDEX_V18.json",
        "prior_index_sha256":OLD_SHA,
        "as_of_utc":"2026-10-21",
        "sum_source_annotations":1038,
        "original_chinese_source_anchors_checked_against_revision":966,
        "full_ziwei_original_text_collation_finished":False,
        "ziwei_complete_natal_calendar_engine_verified":False,
        "chinese_bazi_solar_term_engine_verified":False,
        "independently_validated_real_human_claims":0,
        "runtime_promotions":0,
    })
    nextidx["accepted_batches"].append({
        "id":"ChineseAstro-19SRC-Children",
        "added_bazi_source_annotations":0,
        "added_ziwei_source_annotations":34,
        "source_heading_lines":1,"source_method_preamble_lines":4,
        "source_wrapped_continuation_lines":4,
        "source_historical_star_or_combination_lines":24,
        "next_wealth_navigation_only":1,
        "start":"ZWD-R0795","end":"ZWD-R0828",
        "path":DOC.relative_to(T).as_posix(),
        "rules_sha256":hashes[0],
        "witness_path":WIT.relative_to(T).as_posix(),
        "witness_sha256":hashes[1],
        "original_excerpt_path":EXCERPT.relative_to(T).as_posix(),
        "original_excerpt_sha256":hashes[2],
        "source_oldid":1963110,"source_raw_SHA256":RAW_SHA,
        "source_original_codepoint_range":[39218,40563],
        "next_original_source_heading":"===五财帛===",
        "historical_sex_fertility_child_welfare_assertions_unverified":True,
        "ancient_Ming_imprint_critical_text_authenticated":False,
        "real_human_blind_predictions_validated":0,
        "runtime_rules_promoted":0,
        "cold_replayed_original_source_tests_green":13,
    })
    ziwei=nextidx["systems"][1]
    ziwei["accepted_source_annotations"]=828
    ziwei["current_ids"]="ZWD-R0001–ZWD-R0828"
    ziwei["next_id"]="ZWD-R0829"
    ziwei["current_batch"]="ChineseAstro-19SRC-Children"
    ziwei["source_files"].append(DOC.relative_to(T).as_posix())
    ziwei["chapter_coverage"]=(
        "Online transmitted Zi Wei Volume II Wikitext oldid1963110 has prior Life-palace, "
        "Brothers, Spouses and now Children (四子女) historical source lines cp39218-40563. "
        "33 literal nonmarkup source lines with one heading, four source methodological preambles, "
        "four physically wrapped earlier-profile continuations, 24 star-group lines, and following "
        "Wealth heading navigation. All are unverified historical fertility/sex/count/survival "
        "claims; no authenticated Ming woodblock, original whole text, accurate chart calculation "
        "or independently blinded person prediction established."
    )
    nextidx["next"]=(
        "Next Zi Wei original Wealth 财帛 source heading cp40563, ZWD-R0829, "
        "then Disease cp41672. BaZi Di Tian Sui section19 BZI-R0211 remains untouched. "
        "Physical early editions, natal calendar engine and prospective human baselines open."
    )
    nextidx["historical_glyph_and_translator_limits"]=(
        "Modern transmitted Wikitext oldid1963110 is source-anchored, but not authenticated "
        "early printed original or critically translated. Children's clause extensions and historical "
        "sex/fertility/survival claims retained without medical advice or real-person validation. "
        "Earlier edition uncertainty about four-transformation chart computation persists."
    )
    if nextidx["systems"][0]!=old["systems"][0] or nextidx["accepted_batches"][:-1]!=old["accepted_batches"]:
        raise ValueError("Historical Chinese index or BaZi prior data changed")
    if sum(x["accepted_source_annotations"] for x in nextidx["systems"])!=1038:
        raise ValueError("New Chinese documentary total is inconsistent")
    save(NEW,nextidx)
    header=(
        "# Chinese V19 — online Zi Wei original Children-palace documentary source\n\n"
        "**34 additional historical text records ZWD-R0795–ZWD-R0828** from pinned Wikitext "
        "oldid1963110 Children cp39218–40563; one heading, four method lines, four actual "
        "source continuations, 24 other historical conditional lines and one next Wealth "
        "navigation marker. Exact CP/UTF8/hash witnesses and independent cold source checks "
        "passed. **BaZi210 + Zi Wei828 =1038 Chinese text annotations**, not humans. "
        "Original early printed editions, historical reproductive/gender/health truth and birth "
        "chart engine remain unverified. Next **ZWD-R0829 Wealth cp40563** and "
        "**BZI-R0211 Di Tian Sui section19**. Actual human predictive validations **0**, "
        "runtime promotions **0**.\n\n"
    )
    CURRENT.write_text(header+"## Previous accepted Chinese source checkpoint\n\n"+
                       (REC/"CHINESE_CURRENT_BEFORE_19.md").read_text(encoding="utf-8"),
                       encoding="utf-8")
    LATEST.write_text(header+(B/"ORIGINAL_SOURCE_REVIEW_20261021.md").read_text(encoding="utf-8"),encoding="utf-8")
    receipt={
        "batch":"ChineseAstro-19SRC-Children",
        "status":"GUARDED_ORIGINAL_WIKITEXT_CHILDREN_V19_ACCEPTED_LOCALLY",
        "Chinese_before":1004,"Chinese_after":1038,"BaZi_retained":210,
        "ZiWei_before":794,"ZiWei_after":828,
        "first_ZWD":"ZWD-R0795","last_ZWD":"ZWD-R0828",
        "next_ZWD":"ZWD-R0829","next_BZI":"BZI-R0211",
        "old_V18_index_SHA256":OLD_SHA,"new_V19_index_SHA256":sha(NEW),
        "original_full_source_SHA256":RAW_SHA,
        "source_notes_SHA256":hashes[0],"source_witness_SHA256":hashes[1],
        "original_excerpt_SHA256":hashes[2],
        "portable_archive_SHA256":archive["archive_sha256"],
        "cold_test_replays_green":13,"Western_B07bc_retained_SHA256":WEST_SHA,
        "real_human_blind_predictions":0,"runtime_astrology_promotions":0,
    }
    save(RECEIPT,receipt)
    print(json.dumps(receipt,ensure_ascii=False,indent=2))


if __name__=="__main__":
    accept()
