#!/usr/bin/env python3
"""Guarded source-only BaZi Di Tian Sui section 19 append, no human forecast."""
from __future__ import annotations
import copy
from hashlib import sha256
import json
from pathlib import Path
import subprocess

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-chinese-primary-sources-20261017"
OLD = T / "CHINESE_SOURCE_AUDIT_INDEX_V24.json"
NEW = T / "CHINESE_SOURCE_AUDIT_INDEX_V25.json"
RAW = B / "evidence/DiTianSui_19_oldid844368.wikitext"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
PRIOR = T / "batches/ChineseAstro-09/BAZI_DITIAN_SUI_13_18_56_SOURCE_NOTES_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261021_25SRC_BAZI19.md"
REC = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261021.json"
NOTES = B / "BAZI_DITIAN_SUI_19_6_SOURCE_NOTES_V1.json"
WITNESS = B / "SOURCE_DTS19_6_EXACT_OFFSET_WITNESS_V1.json"
MAN = B / "PINNED_DITIAN_SUI_19_SOURCE_MANIFEST_V1.json"
LEASE = B / "WRITER_LEASE.json"
BRANCH = "research/astro-chinese-v25-bazi-dts19-original-source-20261021"
V24_SHA = "ff40d64df1f4d2a5525591c5e4b5fa7e823c9c81e420093413b01cc292a919d1"
RAW_SHA = "032a772c550dedb35aa130b835bb12d09dd3f3e89652aea382d7b00587ccf28d"
WEST_SHA = "c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"

def sha(p: Path) -> str:
    return sha256(p.read_bytes()).hexdigest()
def rd(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))
def wr(p: Path, obj: object) -> None:
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
def unchanged(p: Path) -> None:
    rel=p.relative_to(ROOT).as_posix()
    if git("rev-parse","HEAD:"+rel) != git("hash-object",str(p)):
        raise ValueError("Previously accepted original source data changed: "+rel)

def accept() -> None:
    if git("branch","--show-current")!=BRANCH:
        raise ValueError("Not inside isolated Di Tian Sui section19 writer")
    lease=rd(LEASE)
    if lease["status"]!="active" or lease["owned_branch"]!=BRANCH:
        raise ValueError("Source writer lease missing/inactive")
    if any(p.exists() for p in (NEW,LATEST,REC,RECEIPT)):
        raise ValueError("Existing interrupted V25 index append, reconcile first")
    for p,required in ((OLD,V24_SHA),(RAW,RAW_SHA),(WEST,WEST_SHA)):
        if sha(p)!=required:
            raise ValueError("Pinned accepted original index/source SHA drift: "+str(p))
    for p in (OLD,RAW,WEST,PRIOR,CURRENT,MAN):
        unchanged(p)
    old=rd(OLD)
    notes=rd(NOTES)
    witness=rd(WITNESS)
    accept=rd(B/"ACCEPTANCE.json")
    source_archive=rd(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
    if (old["sum_source_annotations"],
        old["original_chinese_source_anchors_checked_against_revision"])!=(1269,1197):
        raise ValueError("Older accepted V24 original source counters unexpected")
    if old["accepted_batches"][-1]["id"]!="ChineseAstro-24SRC-FinalPalaces":
        raise ValueError("Original previous Chinese batch identity changed")
    if [(r["accepted_source_annotations"],r["next_id"]) for r in old["systems"]] != [
        (210,"BZI-R0211"),(1059,"ZWD-R1060")]:
        raise ValueError("BaZi/ZiWei source frontier moved unexpectedly")
    if len(notes["records"])!=6 or len(witness["record_original_quote_witness"])!=6:
        raise ValueError("Exact original source units/witness count missing")
    if [r["id"] for r in notes["records"]] != [f"BZI-R{x:04d}" for x in range(211,217)]:
        raise ValueError("Original source IDs not exactly consecutive")
    if notes["source_components"]!={"transmitted_original_verse":1,
                                    "transmitted_commentary":3,
                                    "historical_four_pillar_example":2}:
        raise ValueError("Source verse/commentary/example table structural integrity lost")
    if notes["original_source_oldid"]!=844368 or notes["next_id"]!="BZI-R0217":
        raise ValueError("Old manuscript transmission or next source frontier wrong")
    if any(r["real_human_blind_predictive_validations"] or
           r["runtime_astrological_rule_promotions"] for r in notes["records"]):
        raise ValueError("Unverified historical example counted as human prediction")
    digests=(sha(NOTES),sha(WITNESS))
    if (accept["source_notes_sha256"],accept["source_witness_sha256"])!=digests:
        raise ValueError("Original source record hash/witness mismatch")
    if witness["raw_source_SHA256"]!=RAW_SHA or len(witness["original_source_column_order_time_day_month_year"])!=2:
        raise ValueError("Both original hour/day/month/year table headers required")
    if not (source_archive["ZIP_CRC_verified"] and source_archive["member_SHA256_byte_sizes_verified"]
            and source_archive["cold_extracted_source_test_green"]==11):
        raise ValueError("Cold re-extracted source tests must pass")
    archive_path=Path(source_archive["local_archive_path"])
    if not archive_path.is_file() or sha(archive_path)!=source_archive["archive_SHA256"]:
        raise ValueError("Original owner archive missing or changed")
    REC.mkdir(exist_ok=False)
    for p,name in ((OLD,"CHINESE_V24_BEFORE_25.json"),
                   (CURRENT,"CHINESE_CURRENT_BEFORE_25.md"),
                   (WEST,"WESTERN_B07bc_BEFORE_25.json")):
        (REC/name).write_bytes(p.read_bytes())
    new=copy.deepcopy(old)
    new.update({
        "schema":"ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V25",
        "status":"BAZI_DI_TIAN_SUI_19_SOURCE_FLOW_TWO_HISTORICAL_EXAMPLES_DOCUMENTED",
        "prior_index":"CHINESE_SOURCE_AUDIT_INDEX_V24.json",
        "prior_index_sha256":V24_SHA,
        "as_of_utc":"2026-10-21",
        "sum_source_annotations":1275,
        "original_chinese_source_anchors_checked_against_revision":1203,
        "full_ziwei_original_text_collation_finished":False,
        "ziwei_complete_natal_calendar_engine_verified":False,
        "chinese_bazi_solar_term_engine_verified":False,
        "independently_validated_real_human_claims":0,
        "runtime_promotions":0,
    })
    new["accepted_batches"].append({
        "id":"ChineseAstro-25SRC-BaZi-SourceFlow",
        "added_bazi_source_annotations":6,
        "added_ziwei_source_annotations":0,
        "first_id":"BZI-R0211","last_id":"BZI-R0216",
        "start":"BZI-R0211","end":"BZI-R0216",
        "path":NOTES.relative_to(T).as_posix(),"rules_sha256":digests[0],
        "witness_path":WITNESS.relative_to(T).as_posix(),
        "witness_sha256":digests[1],
        "original_source_manifest_path":MAN.relative_to(T).as_posix(),
        "original_source_manifest_sha256":sha(MAN),
        "source_chapter":"滴天髓/19",
        "source_oldid":844368,
        "original_source_raw_SHA256":RAW_SHA,
        "one_source_verse":1,"three_full_source_commentary_paragraphs":3,
        "two_original_hour_day_month_year_example_tables":2,
        "historical_case_outcomes_independently_verified":False,
        "short_vs_ChanWei_transmission_variant_unresolved":True,
        "ancient_original_print_authorship_critical_text_verified":False,
        "portable_cold_original_source_tests_passed":11,
        "human_blind_predictions_validated":0,
        "runtime_astrology_promotions":0,
    })
    bazi=new["systems"][0]
    bazi["accepted_source_annotations"]=216
    bazi["current_ids"]="BZI-R0001–BZI-R0216"
    bazi["next_id"]="BZI-R0217"
    bazi["current_batch"]="ChineseAstro-25SRC-BaZi-SourceFlow"
    bazi["source_files"].append(NOTES.relative_to(T).as_posix())
    bazi["chapter_coverage"]=(
        "Accepted original transmitted Di Tian Sui original online source through "
        "section 19 Source/Flow 源流論, oldid844368, consisting of one verse, "
        "three full original Chinese commentary paragraphs and two literal "
        "four-pillar example rows in hour/day/month/year order. Traditional "
        "text asserts historical wealth and monkhood results but the biographies "
        "and sample subjects have no independent identification/outcome "
        "verification. Short versus expanded Chan Wei variants in elemental "
        "support polarity and 僧/憎 unresolved. Early printed authorship, "
        "calendar time engine and real human accuracy not verified."
    )
    new["next"]=(
        "Next Di Tian Sui original source chapter20 通隔論, first BaZi BZI-R0217; "
        "pin original Wikitext oldid/UTF8 SHA before reading. Next historical "
        "Zi Wei after completed online Volume II is potential ZWD-R1060 "
        "only on separately pinned Volume III. Verify early-print variants, "
        "independent lunar/leap-month chart calculations and preregistered "
        "untouched real-human prediction baselines."
    )
    new["historical_glyph_and_translator_limits"]=(
        "Original BaZi 滴天髓/19 pinned short transmitted online Wikitext oldid844368 "
        "not authenticated printed early work; expanded 滴天髓闡微 different "
        "verse 流到何方住 vs short 流向可方住, different 得從引助 vs 無從引助, "
        "and 憎 vs 僧, which can change reading of historical example. "
        "Neither old text's claimed career, wealth or monkhood outcomes are "
        "independent real human observations."
    )
    if new["systems"][1]!=old["systems"][1] or new["accepted_batches"][:-1]!=old["accepted_batches"]:
        raise ValueError("Previously accepted Zi Wei source batches or whole history changed")
    if sum(x["accepted_source_annotations"] for x in new["systems"])!=1275:
        raise ValueError("New Chinese source count arithmetic mismatch")
    wr(NEW,new)
    intro=(
        "# Chinese BaZi V25 — transmitted Di Tian Sui section19 Source and Flow\n\n"
        "**6 new original historical source documentary annotations BZI-R0211–BZI-R0216** "
        "from pinned Wikisource oldid844368, 1 exact verse, 3 full commentary "
        "paragraphs, 2 four-pillar example rows with time/day/month/year columns. "
        "Short text and expanded Chan Wei transmit incompatible glyphs "
        "(流向可方住 vs 流到何方住; 無從引助 vs 得從引助; 僧 vs 憎); "
        "keep separate until older printed critical edition verified. "
        "**216 BaZi +1059 Zi Wei =1275 Chinese historical text annotations**, "
        "not real people. Next **BZI-R0217 Di Tian Sui section20 通隔論**; "
        "Zi Wei next potential ZWD-R1060 requires separate Volume III source. "
        "No independent natal calendar/birth-engine validation or human forecast "
        "data; genuine blinded human validations **0**, runtime promotions **0**.\n\n"
    )
    CURRENT.write_text(intro+"## Prior accepted Chinese V24 source checkpoint\n\n"+
        (REC/"CHINESE_CURRENT_BEFORE_25.md").read_text(encoding="utf-8"),
        encoding="utf-8")
    LATEST.write_text(intro+(B/"ORIGINAL_SOURCE_REVIEW_20261021.md").read_text(encoding="utf-8"),
        encoding="utf-8")
    receipt={
        "batch":"ChineseAstro-25SRC-BaZi-SourceFlow",
        "status":"GUARDED_BAZI_DITIAN_SUI_SECTION19_SOURCE_ONLY_ACCEPTED_LOCALLY",
        "Chinese_before":1269,"Chinese_after":1275,
        "BaZi_before":210,"BaZi_after":216,
        "ZiWei_unchanged":1059,
        "first_BZI":"BZI-R0211","last_BZI":"BZI-R0216",
        "next_BZI":"BZI-R0217","next_ZiWei":"ZWD-R1060",
        "prior_V24_index_SHA256":V24_SHA,
        "new_V25_index_SHA256":sha(NEW),
        "source_oldid":844368,
        "raw_original_SHA256":RAW_SHA,
        "new_source_notes_SHA256":digests[0],
        "new_source_witness_SHA256":digests[1],
        "portable_archive_SHA256":source_archive["archive_SHA256"],
        "cold_source_tests_green":11,
        "older_inherited_Western_B07bc_SHA256":WEST_SHA,
        "two_historical_case_outcomes_not_blinded_verified":True,
        "authentic_original_print_edition_verified":False,
        "human_blind_predictive_validations":0,
        "runtime_astrology_promotions":0,
    }
    wr(RECEIPT,receipt)
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=="__main__":
    accept()
