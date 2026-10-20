#!/usr/bin/env python3
"""Guarded append-only source admission for original CLXXXIII Travels.

Fail if parent source/index or Chinese V7 changed, source photos/portable ZIP
drift, or interrupted recovery exists. No actual human predictions validated.
"""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import subprocess

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-source-audit-multipass-20261005"
INDEX=T/"LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07bf_TRAVELS.md"
RECOVERY=B/"recovery"
RECEIPT=B/"CANONICAL_PREPARE_RECEIPT_20261020.json"
BRANCH="research/astro-b07bf-clxxxiii-travels-source-20261020"
SHA_1647="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
SHA_CHINA="bb73f28bf74a1ccb3a0a0e76b91c45f647128733047b8145094f28c9a4ae9d84"

def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def digest(p):return sha256(p.read_bytes()).hexdigest()
def wr(p,obj):p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
def git(*args):return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def old_file_unchanged(p):
    rel=str(p.relative_to(ROOT))
    if git("rev-parse","HEAD:"+rel)!=git("hash-object",str(p)):
        raise ValueError("Previously accepted source changed: "+rel)

def admit():
    if git("branch","--show-current")!=BRANCH:
        raise ValueError("Not intended research worktree branch")
    if any(p.exists() for p in (RECOVERY,RECEIPT,LATEST)):
        raise ValueError("Prior interrupted source acceptance: reconcile existing recovery")
    index=rd(INDEX)
    source=rd(B/"ORIGINAL_1647_1659_TRAVELS_SOURCE_V1.json")
    rules=rd(B/"RULES.json")
    accept=rd(B/"ACCEPTANCE.json")
    archive=rd(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")
    if (index["records_count"],index["batches"][-1]["id"],
        index["next"]["chapter"],index["next"]["pdf_page"],index["next"]["printed_page"])!=(
         13131,"B07be","CLXXXIII",792,758
    ):
        raise ValueError("Verified original Children B07be source frontier changed")
    if index["read_numbered_chapters"]!=list(range(1,183)) or index["read_headed_units_count"]!=98:
        raise ValueError("Original numbered or headed chapters are not accepted through182")
    if index["partial_numbered_chapters"]!=[] or index["source_sha256"]!=SHA_1647:
        raise ValueError("Old original source primary index root unexpectedly changed")
    if index["empirical_validations"]!=0 or index["runtime_promotions"]!=0:
        raise ValueError("Documentary source index unexpectedly contains human validation")
    if digest(CHINA)!=SHA_CHINA or rd(CHINA)["sum_source_annotations"]!=355:
        raise ValueError("Distinct frozen original Chinese V7 source index changed")
    if (len(source["records"]),len(rules["rules"]),accept["new_source_only_historical_notes"])!=(61,61,61):
        raise ValueError("Expected 61 source historical notes, no more and no less")
    if rules["rules"]!=source["records"] or [r["id"] for r in source["records"]] !=[
        f"R{i}" for i in range(13132,13193)
    ]:
        raise ValueError("The original source IDs/order and rule bundle disagree")
    if (accept["Lilly_before"],accept["Lilly_after_if_accepted"],
        accept["Western_after_if_accepted"],accept["next_R"])!=(
        13131,13192,14258,"R13193"
    ):
        raise ValueError("Expected next accepted source count changed")
    if (digest(B/"ORIGINAL_1647_1659_TRAVELS_SOURCE_V1.json"),
        digest(B/"RULES.json"))!=(accept["source_sha256"],accept["rules_sha256"]):
        raise ValueError("Previously tested historical source/rules modified")
    if not archive["zip_CRC_verified"] or not archive["all_portable_members_independently_SHA_checked"]:
        raise ValueError("Portable archive missing independent source SHA/CRC verification")
    if (archive["fresh_cold_extraction_source_tests_executed"],
        archive["fresh_cold_extraction_source_tests_green"])!=(11,11):
        raise ValueError("Cold independent source replay did not pass all cases")
    fp=Path(archive["owner_local_portable_path"])
    if not fp.is_file() or digest(fp)!=archive["archive_sha256"]:
        raise ValueError("Original source archive not found/changed")
    from build_b07bf_travels_source import original_witnesses
    if source["four_source_page_first_second_photo_witnesses"]!=original_witnesses():
        raise ValueError("Exact original printed first/second photos changed")
    prior=[
        INDEX,CHINA,
        T/"batches/B07be/RULES.json",
        T/"batches/B07be/ORIGINAL_1647_1659_CLXXXII_CHILDREN_SOURCE_V1.json",
        T/"batches/B07be/evidence/1659-original-folio758-next-travel-thumbnail.jpg",
        T/"batches/B07bd/next_children_1647_photo_prefetch/1647-original-folio758-iiif.jpg",
        T/"batches/B07bd/next_children_1647_photo_prefetch/1647-original-folio759-iiif.jpg",
    ]
    for p in prior:old_file_unchanged(p)
    if any(r["independently_blind_real_human_prediction"] or
           r["astrological_runtime_rule_promoted"] or
           r["historic_recommendation_allowed_as_current_person_advice"]
           for r in source["records"]):
        raise ValueError("Historical claims cannot be marked human-validated or adopted advice")
    RECOVERY.mkdir(exist_ok=False)
    for path,name in ((INDEX,"LILLY_INDEX_BEFORE_B07bf.json"),
                      (CURRENT,"CURRENT_BEFORE_B07bf.md"),
                      (CHINA,"CHINESE_V7_BEFORE_B07bf.json")):
        (RECOVERY/name).write_bytes(path.read_bytes())

    index["batches"].append({
        "id":"B07bf","path":"batches/B07bf/RULES.json",
        "records_count":61,"sha256":digest(B/"RULES.json"),
        "scope":(
            "Original Lilly independent 1647 and separately typeset 1659 "
            "CLXXXIII Ninth-house Of Travels printed folios758-760/first PDF792-794 "
            "(next CLXXXIIII Honours begins below divider on p760). "
            "61 source-only R13132-R13192 including author-disclosed past sea "
            "voyages two Barbary and one Holland (NOT blind forecasts), "
            "nonvalidated directional, business success, conditional shipping/"
            "fire/robbery hazard, benevolent direction mitigation and zodiac-"
            "country associations; no merchant travel documentation, no "
            "actual human predictive results and no runtime promoted rules."
        )
    })
    index["records_count"]=13192
    index["status"]="BOOK_III_CLXXXIII_TRAVELS_PHYSICAL_SOURCE_COVERED_NEXT_CLXXXIIII_HONOURS"
    index["read_numbered_chapters"].append(183)
    index["read_headed_units_count"]=99
    index["completed_original_source_units_with_uncertainty"].append({
        "printed_chapter":"CLXXXIII","editorial_ordinal":183,
        "heading":"Of Travels",
        "source_start_original_pdf":792,"accepted_through_original_pdf":794,
        "printed_folios":[758,759,760],
        "next_chapter_first_source_folio":760,
        "next_chapter_printed_Roman":"CLXXXIIII",
        "source_batch":"B07bf",
        "historical_start":"R13132","historical_end":"R13192",
        "complete":True,"physical_source_span_covered":True,
        "original_source_photos_from_both_printings_SHA_verified":True,
        "all_original_glyphs_second_blind_expert_collated":False,
        "author_past_voyages_already_disclosed_prior_to_rule_interpretation":True,
        "authentic_real_merchant_past_voyages_independently_verified":False,
        "historical_predicted_disasters_are_conditional_not_dated":True,
        "benevolent_directions_can_override_source_bad_travel_inference":True,
        "actual_real_human_predictive_test_count":0,
        "runtime_astrological_promotions":0
    })
    index["next"]={
        "pdf_page":794,"printed_page":760,
        "chapter":"CLXXXIIII",
        "printed_chapter_numeral":"CLXXXIIII",
        "editorial_source_sequence_ordinal":184,
        "heading":"Honours, Preferment, Magistery, and with what repute",
        "include_opening_paragraph":True,"extracted":False,
        "boundary_image_read":True,
        "position":(
            "First 1647 original p760/PDF794 begins CLXXXIIII Honours below "
            "a horizontal divider after CLXXXIII Travels, continuing p761; "
            "first next source annotation R13193. The 1659 original similarly "
            "has a physically separate tenth-house chapter."
        ),
        "research_scope":(
            "Known native vocational standing and honours interpreted by "
            "Mars tenth, Venus/Mercury/Sun and fixed stars, not blind real "
            "human career/fame validation."
        )
    }
    index["current_state"]="state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07bf_TRAVELS.md"
    index["chapter_CLXXXIII_source_leakage_and_conditions_note"]=(
        "Lilly's original 1647/1659 CLXXXIII printed marginal report says "
        "his already-known merchant previously travelled by sea three times, "
        "twice Barbary and once Holland. This is preknown narrative data, "
        "not a successful chart inference or verified travel manifest. "
        "Other travel directions/fortune/disasters are conditional on mutable "
        "astrological directions and some can be cancelled; no merchant "
        "real-life events or prospective forecast validity authenticated."
    )
    if (index["read_numbered_chapters"]!=list(range(1,184))
        or index["records_count"]!=sum(b["records_count"] for b in index["batches"])
        or index["empirical_validations"]!=0 or index["runtime_promotions"]!=0):
        raise ValueError("Proposed new canonical historical source index inconsistent")
    wr(INDEX,index)
    summary=(
        "# Original Lilly CLXXXIII Travels — 1647/1659 source covered B07bf\n\n"
        "**61 historical source-only R13132–R13192** from original printed "
        "758–760/PDF792–794 with eight SHA-verified first1647/separate1659 "
        "page images through next-chapter p761 boundary. The merchant's "
        "already-disclosed **three past sea journeys (two Barbary, one Holland)** "
        "are NOT independently corroborated and cannot count as blind "
        "astrological predictions. Travel-related wealth, southwest directions, "
        "symbolic countries, conditional shipwreck/fire/theft and overriding "
        "benevolent directions are historical *unverified* interpretations, "
        "not modern travel or shipping guidance. **13,192 Lilly +1,066 "
        "Ptolemy =14,258 Western** original historic annotations; independent "
        "Chinese accepted V9 **430** in another branch, aggregate source docs "
        "**14,688**, not a single merged registry. Next **R13193 CLXXXIIII "
        "(editorial184) Honours, Preferment**, original p760/PDF794 "
        "below physical divider. Human predictive validations **0**, "
        "runtime promotions **0**.\n\n"
    )
    CURRENT.write_text(summary+"## Previous accepted historical checkpoint retained\n\n"+
                       CURRENT.read_text(encoding="utf-8"),encoding="utf-8")
    LATEST.write_text(summary+(B/"ORIGINAL_SOURCE_REVIEW_20261020.md").read_text(encoding="utf-8"),
                      encoding="utf-8")
    receipt={
        "batch":"B07bf",
        "status":"GUARDED_CLXXXIII_61_NOTES_ACCEPTED_LOCAL_REMOTE_PENDING",
        "Lilly_before":13131,"Lilly_after":13192,
        "Ptolemy_retained":1066,"Western_after":14258,
        "Chinese_V7_exact_unchanged":355,
        "Chinese_V9_accepted_in_separate_branch":430,
        "new_historical_source_only_records":61,
        "original_8_page_images_checked":True,
        "next_R":"R13193","next_chapter":"CLXXXIIII",
        "next_original_first_1647_PDF_frame":794,
        "old_index_SHA256":digest(RECOVERY/"LILLY_INDEX_BEFORE_B07bf.json"),
        "new_index_SHA256":digest(INDEX),
        "original_source_SHA256":accept["source_sha256"],
        "original_rules_SHA256":accept["rules_sha256"],
        "portable_source_archive_SHA256":archive["archive_sha256"],
        "portable_cold_source_tests_green":11,
        "Chinese_V7_source_SHA256":digest(CHINA),
        "known_trip_outcomes_disclosed_before_astrological_judgment":True,
        "real_human_predictive_validations":0,
        "astrological_rules_promoted":0,
    }
    wr(RECEIPT,receipt)
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=="__main__":
    admit()
