#!/usr/bin/env python3
"""Guarded source-only Lilly tenth-house Honours original accepted append."""
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
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07bg_HONOURS.md"
OLD=B/"recovery"
RECEIPT=B/"CANONICAL_PREPARE_RECEIPT_20261020.json"
BRANCH="research/astro-b07bg-clxxxiiii-honours-source-20261020"
SHA_1647="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
SHA_CHINESE_V7="bb73f28bf74a1ccb3a0a0e76b91c45f647128733047b8145094f28c9a4ae9d84"

def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def sh(p):return sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def git(*args):return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def unchanged(p):
    rel=str(p.relative_to(ROOT))
    if git("rev-parse","HEAD:"+rel)!=git("hash-object",str(p)):
        raise ValueError("Refuse modified previously accepted original source "+rel)

def main():
    if git("branch","--show-current")!=BRANCH:
        raise ValueError("Not correct isolated source branch")
    if any(p.exists() for p in (OLD,RECEIPT,LATEST)):
        raise ValueError("Existing interrupted source admission: reconcile first")
    idx=rd(INDEX)
    china=rd(CHINA)
    src=rd(B/"ORIGINAL_1647_1659_HONOURS_SOURCE_V1.json")
    rules=rd(B/"RULES.json")
    accept=rd(B/"ACCEPTANCE.json")
    zipdata=rd(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")
    if (idx["records_count"],idx["batches"][-1]["id"],
        idx["next"]["chapter"],idx["next"]["printed_page"],idx["next"]["pdf_page"])!=(
        13192,"B07bf","CLXXXIIII",760,794
    ):
        raise ValueError("Lilly CLXXXIII previous accepted source frontier no longer matches")
    if idx["read_numbered_chapters"]!=list(range(1,184)) or idx["read_headed_units_count"]!=99:
        raise ValueError("Original accepted source headings through editorial183 not present")
    if idx["partial_numbered_chapters"]!=[] or idx["source_sha256"]!=SHA_1647:
        raise ValueError("Original source root and complete printed previous chapters changed")
    if idx["empirical_validations"] or idx["runtime_promotions"]:
        raise ValueError("Historical source index cannot carry inflated predictive validation")
    if sh(CHINA)!=SHA_CHINESE_V7 or china["sum_source_annotations"]!=355:
        raise ValueError("Frozen accepted Chinese V7 source data unexpectedly differs")
    if (len(src["records"]),len(rules["rules"]),
        accept["new_historical_source_only_annotations"])!=(44,44,44):
        raise ValueError("Unexpected original Honours count")
    if src["records"]!=rules["rules"] or [x["id"] for x in src["records"]] !=[
        f"R{i}" for i in range(13193,13237)
    ]:
        raise ValueError("Historical annotation ID/order or exact source notes changed")
    if (accept["Lilly_before"],accept["Lilly_after_if_accepted"],
        accept["Western_after_if_accepted"],accept["next_R"])!=(
        13192,13236,14302,"R13237"
    ):
        raise ValueError("Historical source expected next count changed")
    if (sh(B/"ORIGINAL_1647_1659_HONOURS_SOURCE_V1.json"),
        sh(B/"RULES.json"))!=(accept["source_SHA256"],accept["rules_SHA256"]):
        raise ValueError("Original source/reviewed RULES content modified")
    if not zipdata["zip_CRC_check_passed"] or not zipdata["all_members_exact_SHA_and_bytes_check_passed"]:
        raise ValueError("Independent portable original source archive missing SHA/CRC")
    if (zipdata["independent_cold_source_tests_executed"],
        zipdata["independent_cold_source_tests_green"])!=(13,13):
        raise ValueError("Independent extracted original source tests not green")
    archive=Path(zipdata["archive_path_on_owner_machine"])
    if not archive.is_file() or sh(archive)!=zipdata["archive_sha256"]:
        raise ValueError("Original source archive SHA drift from receipt")
    from build_b07bg_honours_source import original_photos
    if src["source_photo_witnesses"]!=original_photos():
        raise ValueError("Eight printed original source photos no longer verify")
    for p in (
        INDEX,CHINA,
        T/"batches/B07bf/RULES.json",
        T/"batches/B07bf/ORIGINAL_1647_1659_TRAVELS_SOURCE_V1.json",
        T/"batches/B07bf/evidence/1647-original-folio760-IIIF.jpg",
        T/"batches/B07bf/evidence/1659-original-folio760-DjVu.jpg",
        T/"batches/B07bf/evidence/1647-original-folio761-IIIF.jpg",
        T/"batches/B07bf/evidence/1659-original-folio761-DjVu.jpg",
    ):
        unchanged(p)
    if any(r["historical_original_actual_career_verified"] or
           r["independent_human_blind_forecast_tested"] or
           r["runtime_astrological_rule_promoted"] for r in src["records"]):
        raise ValueError("Source records falsely promoted into real-person validations")
    OLD.mkdir(exist_ok=False)
    for source,name in ((INDEX,"LILLY_INDEX_BEFORE_B07bg.json"),
                        (CURRENT,"CURRENT_BEFORE_B07bg.md"),
                        (CHINA,"CHINESE_V7_BEFORE_B07bg.json")):
        (OLD/name).write_bytes(source.read_bytes())
    idx["batches"].append({
        "id":"B07bg","path":"batches/B07bg/RULES.json",
        "records_count":44,"sha256":sh(B/"RULES.json"),
        "scope":(
            "Original Lilly independent 1647/1659 tenth-house literal Chap "
            "CLXXXIIII (editorial184), Honours, Preferment, Magistery p760–762/"
            "PDF794–796, 44 historical source-only R13193–R13236. "
            "Profession/career choices and trades Mars/metal, Venus/jewels, "
            "Mercury/accounts, class and effort qualifications, conditional "
            "directed advancement, possible fame and office. Reuses old same "
            "Venus Cazimi natal premise from Marriage and is not independent "
            "human evidence. Next eleventh-house Friends original p762 is "
            "printed CLXXXIII, repeated from earlier Travels and numerically "
            "backwards after CLXXXIIII; editorial sequence ordinal185. "
            "No actual merchant career records/honours corroborated, "
            "no prospective human predictive study, no runtime promotion."
        )
    })
    idx["records_count"]=13236
    idx["status"]="BOOK_III_CLXXXIIII_HONOURS_SOURCE_COVERED_NEXT_FRIENDS_PRINTED_CLXXXIII"
    idx["read_numbered_chapters"].append(184)
    idx["read_headed_units_count"]=100
    idx["completed_original_source_units_with_uncertainty"].append({
        "printed_chapter":"CLXXXIIII","editorial_ordinal":184,
        "heading":"Honours, Preferment, Magistery",
        "original_source_start_pdf":794,"accepted_through_original_pdf":796,
        "printed_folios":[760,761,762],
        "source_batch":"B07bg",
        "historical_start":"R13193","historical_end":"R13236",
        "physical_source_span_covered":True,"complete":True,
        "original_printings_two_edition_page_SHA_and_bytes_verified":True,
        "original_birth_Sun_Venus_Cazimi_reused_from_prior_marriage":True,
        "source_epoch_birth_UT_and_cazimi_independent_astronomy_verified":False,
        "printed_next_Friends_Roman_CLXXXIII_regresses_to_earlier_Travels_label":True,
        "expert_blinded_diplomatic_edition_all_astro_glyphs_finished":False,
        "actual_known_merchant_occupation_reputation_verified":False,
        "human_predictive_accuracy_validations":0,
        "runtime_astrological_promotions":0
    })
    idx["next"]={
        "pdf_page":796,"printed_page":762,
        "chapter":"CLXXXIII","printed_chapter_numeral":"CLXXXIII",
        "editorial_source_sequence_ordinal":185,
        "heading":"Of Friends","include_opening_paragraph":True,
        "extracted":False,"boundary_image_read":True,
        "position":(
            "1647 first original p762/PDF796 below hard divider from source "
            "CLXXXIIII Honours contains new eleventh-house printed "
            "CLXXXIII Of Friends, repeating prior Travels roman heading. "
            "The separately printed 1659 edition has the same source anomaly. "
            "First next historic source note R13237. Folio763 already "
            "photographed first/second for physical next chapter boundary."
        ),
        "research_scope":(
            "Original source relations/friends and social standing for known "
            "merchant, not modern friend-selection or empirically validated "
            "relationship or business partner predictions."
        )
    }
    idx["current_state"]="state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07bg_HONOURS.md"
    idx["chapter_CLXXXIIII_printed_roman_regression_and_cazimi_source_warning"]=(
        "Original first+second edition Honours literally CLXXXIIII but next "
        "Friends literally CLXXXIII even though editorially numbered185, "
        "reusing earlier Travels literal. Source again cites Venus Cazimi "
        "from same old chart as Marriage: nominal printed17 arcminute "
        "Sun-Venus vs independent modern Swiss ~75 arcminute at uncertain "
        "Julian UT, not second independent chart support. Broad multiple "
        "professions/wealth/honours are not real-person blind predictions."
    )
    if idx["read_numbered_chapters"]!=list(range(1,185)) or idx["records_count"]!=sum(
        x["records_count"] for x in idx["batches"]
    ) or idx["empirical_validations"] or idx["runtime_promotions"]:
        raise ValueError("New accepted original historic source index inconsistent")
    wr(INDEX,idx)
    intro=(
        "# Original Lilly CLXXXIIII Honours — physical original source covered B07bg\n\n"
        "**44 source-only historical R13193–R13236** cover first1647 and "
        "separate1659 printed p760–762/PDF794–796 Honours, with 8 original "
        "folio760–763 page-photo SHA/byte witnesses. Career/commerce, metals, "
        "jewels, accounts, fame, possible public office, fixed stars and "
        "qualifying class/effort/directions are historic claims about an "
        "already-known merchant, no verified actual job or honours. "
        "Venus Cazimi reused from Marriage's unverified natal premise "
        "(printed Sun/Venus17' vs modern ~75' under hypothetical historical UT); "
        "it is NOT independent chart evidence. Original printed numeral "
        "changes backwards from Honours **CLXXXIIII** to next **CLXXXIII** "
        "Friends on p762/PDF796, despite editorial ordinal185. "
        "**13,236 Lilly +1,066 Ptolemy=14,302 Western** historic annotations; "
        "independent Chinese accepted V9 **430** in separate lane (aggregate "
        "**14,732** source docs), not verified predictions. Next **R13237 "
        "Of Friends**, printed p762/PDF796. Human predictive validations "
        "**0**, runtime promotions **0**.\n\n"
    )
    CURRENT.write_text(intro+"## Previous accepted historical checkpoint retained\n\n"+
                       CURRENT.read_text(encoding="utf-8"),encoding="utf-8")
    LATEST.write_text(intro+(B/"ORIGINAL_SOURCE_REVIEW_20261020.md").read_text(encoding="utf-8"),
                      encoding="utf-8")
    receipt={
      "batch":"B07bg",
      "status":"GUARDED_ORIGINAL_1647_1659_HONOURS_44_ACCEPTED_LOCAL_REMOTE_PENDING",
      "Lilly_before":13192,"Lilly_after":13236,
      "Ptolemy_retained":1066,"Western_after":14302,
      "Chinese_V7_frozen":355,"Chinese_V9_distinct_accepted_lane":430,
      "new_historical_annotations":44,
      "eight_original_source_edition_photos_verified":True,
      "next_R":"R13237","next_printed_roman":"CLXXXIII",
      "next_editorial_ordinal":185,"next_printed_folio":762,
      "next_original_first_1647_pdf_frame":796,
      "old_index_sha256":sh(OLD/"LILLY_INDEX_BEFORE_B07bg.json"),
      "new_index_sha256":sh(INDEX),
      "original_source_notes_sha256":accept["source_SHA256"],
      "original_rules_sha256":accept["rules_SHA256"],
      "portable_source_archive_sha256":zipdata["archive_sha256"],
      "independent_cold_source_tests_passed":13,
      "Chinese_V7_sha256":sh(CHINA),
      "career_biographical_facts_licensed_or_validated":False,
      "human_blind_predictive_validation_count":0,
      "runtime_astrological_promotions":0
    }
    wr(RECEIPT,receipt)
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
