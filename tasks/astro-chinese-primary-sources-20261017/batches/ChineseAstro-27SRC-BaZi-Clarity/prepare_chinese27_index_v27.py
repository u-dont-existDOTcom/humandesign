#!/usr/bin/env python3
"""Guarded cumulative Chinese index V27 append; documentary sources != human evidence."""
from pathlib import Path
from hashlib import sha256
import copy,json,subprocess

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V26.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V27.json"
RAW=B/"evidence/DiTianSui_21_oldid844371.wikitext"
PRIOR=T/"batches/ChineseAstro-26SRC-BaZi-Obstruction/BAZI_DITIAN_SUI_20_2_SOURCE_NOTES_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261021_27SRC_BAZI21.md"
REC=B/"recovery"
NOTES=B/"BAZI_DITIAN_SUI_21_4_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_DTS21_4_EXACT_OFFSET_WITNESS_V1.json"
MAN=B/"PINNED_DITIAN_SUI_21_SOURCE_MANIFEST_V1.json"
LEASE=B/"WRITER_LEASE.json"
BR="research/astro-chinese-v27-bazi-dts21-original-source-20261021"
PREV_SHA="f4b69767eb143994766bc9a7c08f7ed1e519bddf234377c9ecc65bcb6080f94f"
RAW_SHA="9ff7673e7a7a8af1cace52457d801d631ca117f5923e8e3433f7b1d05729be0f"
NOTES_SHA="4fa395fafec6883d84957cc70bf1bf72be996d5e4d3fd82c6883272bb546c8ba"
WIT_SHA="b2edd9bf20368dda3ec489341f5e48394c4da1d0725fa492015b91ca3cf598a2"

def sha(p):return sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def git(*args):return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def committed_unchanged(p):
 rel=p.relative_to(ROOT).as_posix()
 if git("rev-parse","HEAD:"+rel)!=git("hash-object",str(p)):
  raise ValueError("Previously accepted original changed: "+rel)

def accept():
 if git("branch","--show-current")!=BR:raise ValueError("Wrong isolated V27 branch")
 if read(LEASE)["status"]!="active" or read(LEASE)["owned_branch"]!=BR:
  raise ValueError("Writer lease inactive or mismatched")
 if any(p.exists() for p in (NEW,LATEST,REC,B/"CANONICAL_PREPARE_RECEIPT_20261021.json")):
  raise ValueError("Interrupted existing V27 admission: inspect rather than overwrite")
 for p,required in ((OLD,PREV_SHA),(RAW,RAW_SHA),(NOTES,NOTES_SHA),(WIT,WIT_SHA)):
  if sha(p)!=required:raise ValueError("Original/source/index SHA changed: "+str(p))
 for p in (OLD,RAW,PRIOR,CURRENT,MAN,NOTES,WIT):
  committed_unchanged(p)
 old=read(OLD);notes=read(NOTES);witness=read(WIT);acc=read(B/"ACCEPTANCE.json")
 arc=read(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
 if (old["sum_source_annotations"],old["original_chinese_source_anchors_checked_against_revision"])!=(1277,1205):
  raise ValueError("Canonical previous V26 source count changed")
 if old["accepted_batches"][-1]["id"]!="ChineseAstro-26SRC-BaZi-Obstruction":
  raise ValueError("Previously accepted source batch unexpectedly differs")
 if [(x["accepted_source_annotations"],x["next_id"]) for x in old["systems"]] !=[(218,"BZI-R0219"),(1059,"ZWD-R1060")]:
  raise ValueError("Previous BaZi/ZiWei source frontier changed")
 if [x["id"] for x in notes["records"]] != [f"BZI-R{i:04d}" for i in range(219,223)]:
  raise ValueError("New historical IDs gaps or duplicates")
 if notes["original_verse_count"]!=2 or notes["complete_original_commentary_paragraphs"]!=2:
  raise ValueError("Whole paired source verse/commentary content not frozen")
 if notes["source_oldid"]!=844371 or notes["next_id"]!="BZI-R0223" or len(witness["quotes"])!=4:
  raise ValueError("Source revision or last record/witness unexpectedly differs")
 if (acc["notes_sha256"],acc["witness_sha256"])!=(NOTES_SHA,WIT_SHA):
  raise ValueError("Previously committed source acceptance SHA changed")
 if not(arc["ZIP_CRC_verified"] and arc["all_members_SHA256_and_bytes_verified"] and arc["independent_cold_source_tests_green"]==10):
  raise ValueError("Independent cold source archive proof missing")
 archive=Path(arc["archive_path"])
 if not archive.is_file() or sha(archive)!=arc["archive_SHA256"]:
  raise ValueError("Owner original source ZIP changed or missing")
 if old["independently_validated_real_human_claims"] or old["runtime_promotions"]:
  raise ValueError("Historical source is not human prediction success")
 if any(x["independent_blinded_human_predictions_validated"] or x["runtime_promotions"] for x in notes["records"]):
  raise ValueError("Human outcome falsely attributed to source")
 REC.mkdir(exist_ok=False)
 for p,name in ((OLD,"CHINESE_V26_BEFORE_27.json"),(CURRENT,"CHINESE_CURRENT_BEFORE_27.md")):
  (REC/name).write_bytes(p.read_bytes())
 new=copy.deepcopy(old)
 new.update({
  "schema":"ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V27",
  "status":"BAZI_DTS21_CLARITY_TURBIDITY_TWO_VERSES_TWO_COMMENTARIES_HISTORICAL_ONLY",
  "as_of_utc":"2026-10-21",
  "prior_index":"CHINESE_SOURCE_AUDIT_INDEX_V26.json",
  "prior_index_sha256":PREV_SHA,
  "sum_source_annotations":1281,
  "original_chinese_source_anchors_checked_against_revision":1209,
  "full_ziwei_original_text_collation_finished":False,
  "ziwei_complete_natal_calendar_engine_verified":False,
  "chinese_bazi_solar_term_engine_verified":False,
  "independently_validated_real_human_claims":0,
  "runtime_promotions":0,
 })
 batch={
  "id":"ChineseAstro-27SRC-BaZi-Clarity",
  "added_bazi_source_annotations":4,
  "added_ziwei_source_annotations":0,
  "start":"BZI-R0219","end":"BZI-R0222",
  "path":NOTES.relative_to(T).as_posix(),"rules_sha256":NOTES_SHA,
  "witness_path":WIT.relative_to(T).as_posix(),"witness_sha256":WIT_SHA,
  "source_manifest_path":MAN.relative_to(T).as_posix(),
  "source_manifest_sha256":sha(MAN),
  "source_online_oldid":844371,
  "source_full_original_SHA256":RAW_SHA,
  "source_original_verses":2,"source_full_commentary_paragraphs":2,
  "online_short_vs_expanded_critical_variants_unresolved":True,
  "ancient_printing_original_critically_authenticated":False,
  "focused_source_tests_green":10,"cold_extracted_source_tests_green":10,
  "independently_validated_real_humans":0,"runtime_rule_promotions":0
 }
 new["accepted_batches"].append(batch)
 bazi=new["systems"][0]
 bazi["accepted_source_annotations"]=222
 bazi["current_ids"]="BZI-R0001–BZI-R0222"
 bazi["next_id"]="BZI-R0223"
 bazi["current_batch"]="ChineseAstro-27SRC-BaZi-Clarity"
 bazi["source_files"].append(NOTES.relative_to(T).as_posix())
 bazi["chapter_coverage"]+=(
  " Pinned original transmitted 滴天髓 section21 清濁論 (oldid844371): "
  "two complete verse lines and two unabridged commentary paragraphs, "
  "historical predicates on clear/muddy vs mixed configurations, "
  "with distinct source textual variants 清神/精神 and 無去取/猶是可 "
  "unresolved and not fitted to known humans."
 )
 new["next"]=(
  "Next original BaZi 滴天髓/22 first BZI-R0223, pin independently actual "
  "revision and complete Chinese source before continuation. Next Zi Wei "
  "ZWD-R1060 requires independently pinned Volume III or authenticated early "
  "woodblock. Independently compute birth chart/calendars and freeze source "
  "predictions before collecting untouched human answers."
 )
 new["historical_glyph_and_translator_limits"]+=(
  " DTS21 short oldid844371 differs from edited extended Chan Wei in "
  "清神/精神, 平生/生平, 生春/回春, and notably 無去取/猶是可. "
  "Neither ancient original printing nor human predictive validity authenticated."
 )
 if new["systems"][1]!=old["systems"][1] or new["accepted_batches"][:-1]!=old["accepted_batches"]:
  raise ValueError("Previously accepted Chinese source history changed")
 if sum(x["accepted_source_annotations"] for x in new["systems"])!=1281:
  raise ValueError("Cumulative Chinese source annotation mismatch")
 write(NEW,new)
 heading=(
  "# Chinese BaZi V27 — Di Tian Sui chapter21 source-first checkpoint\n\n"
  "**Four new historical source annotations BZI-R0219–R0222** from pinned "
  "oldid844371 (two whole verses, two whole commentaries), SHA/CP/UTF8 "
  "proof and 10/10 independent cold source tests. Expanded Chan Wei "
  "variants remain unresolved, particularly 無去取 versus 猶是可. "
  "**BaZi222 + Zi Wei1059 = 1281 historical source records**, not humans. "
  "Next **BZI-R0223 chapter22**, Zi Wei next possible **ZWD-R1060** "
  "only with an independently pinned next source. Ancient printing, chart "
  "engine and human predictive validity remain unverified; genuine human "
  "blinded validations **0**, runtime promotions **0**.\n\n")
 CURRENT.write_text(heading+"## Previous accepted Chinese V26 checkpoint\n\n"+
  (REC/"CHINESE_CURRENT_BEFORE_27.md").read_text(encoding="utf-8"),encoding="utf-8")
 LATEST.write_text(heading+(B/"ORIGINAL_SOURCE_REVIEW_20261021.md").read_text(encoding="utf-8"),encoding="utf-8")
 receipt={
  "batch":"ChineseAstro-27SRC-BaZi-Clarity",
  "status":"GUARDED_DTS21_ORIGINAL_SOURCE_V27_LOCAL_ACCEPTANCE",
  "Chinese_before":1277,"Chinese_after":1281,
  "BaZi_before":218,"BaZi_after":222,"ZiWei_unchanged":1059,
  "first_BZI":"BZI-R0219","last_BZI":"BZI-R0222",
  "next_BZI":"BZI-R0223","next_ZiWei":"ZWD-R1060",
  "old_V26_index_SHA256":PREV_SHA,
  "new_V27_index_SHA256":sha(NEW),
  "source_oldid":844371,"source_full_SHA256":RAW_SHA,
  "notes_SHA256":NOTES_SHA,"witness_SHA256":WIT_SHA,
  "portable_archive_SHA256":arc["archive_SHA256"],
  "cold_source_tests_green":10,
  "ancient_critical_print_authenticity_verified":False,
  "actual_human_blind_predictions_validated":0,"runtime_promotions":0
 }
 write(B/"CANONICAL_PREPARE_RECEIPT_20261021.json",receipt)
 print(json.dumps(receipt,ensure_ascii=False,indent=2))
if __name__=="__main__":accept()
