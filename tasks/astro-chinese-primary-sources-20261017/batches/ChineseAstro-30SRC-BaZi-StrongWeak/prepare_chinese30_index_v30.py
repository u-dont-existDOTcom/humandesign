#!/usr/bin/env python3
"""Guarded original BaZi source23 append; historic text not human evidence."""
from pathlib import Path
from hashlib import sha256
import json,copy,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V29.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V30.json"
RAW=B/"evidence/DiTianSui_24_oldid844375.wikitext"
PRIOR=T/"batches/ChineseAstro-29SRC-BaZi-Hidden/BAZI_DITIAN_SUI_23_2_SOURCE_NOTES_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261021_30SRC_BAZI24.md"
NOTES=B/"BAZI_DITIAN_SUI_24_2_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_DTS24_2_EXACT_OFFSET_WITNESS_V1.json"
MAN=B/"PINNED_DITIAN_SUI_24_SOURCE_MANIFEST_V1.json"
LEASE=B/"WRITER_LEASE.json"
REC=B/"recovery"
BR="research/astro-chinese-v30-bazi-dts24-original-source-20261021"
OLD_SHA="dd692da5d0e1e9918cc2d99eb8935655970275a9151f934976f6647d3cfa205e"
RAW_SHA="a5dc74771a9885e6385ea3201501065a37cb78308dac6449e63f5359babb469e"
def sha(p):return sha256(p.read_bytes()).hexdigest()
def rd(p):return json.loads(p.read_text("utf-8"))
def wr(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def git(*args):return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def unchanged(p):
 rel=p.relative_to(ROOT).as_posix()
 if git("rev-parse","HEAD:"+rel)!=git("hash-object",str(p)):
  raise ValueError("Previously accepted source file changed "+rel)
def accept():
 if git("branch","--show-current")!=BR or rd(LEASE)["status"]!="active":
  raise ValueError("Wrong isolated V30 source branch/lease")
 if any(p.exists() for p in (NEW,LATEST,REC,B/"CANONICAL_PREPARE_RECEIPT_20261021.json")):
  raise ValueError("Existing interrupted V30 admission, reconcile before rerun")
 if sha(OLD)!=OLD_SHA or sha(RAW)!=RAW_SHA:raise ValueError("Source SHA drift")
 for p in (OLD,RAW,PRIOR,CURRENT,MAN,NOTES,WIT):unchanged(p)
 old=rd(OLD);notes=rd(NOTES);wit=rd(WIT);a=rd(B/"ACCEPTANCE.json")
 arc=rd(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
 if (old["sum_source_annotations"],old["original_chinese_source_anchors_checked_against_revision"])!=(1287,1215):
  raise ValueError("Old V29 cumulative source count shifted")
 if old["accepted_batches"][-1]["id"]!="ChineseAstro-29SRC-BaZi-Hidden":
  raise ValueError("Unexpected previous accepted source batch")
 if [(x["accepted_source_annotations"],x["next_id"]) for x in old["systems"]] != [(228,"BZI-R0229"),(1059,"ZWD-R1060")]:
  raise ValueError("Prior BaZi/ZiWei source frontier changed")
 if notes["oldid"]!=844375 or notes["full_original_SHA256"]!=RAW_SHA or notes["source_notes_count"]!=2:
  raise ValueError("Pinned original source scope changed")
 if [x["id"] for x in notes["records"]] != ["BZI-R0229","BZI-R0230"] or len(wit["original_quotes"])!=2:
  raise ValueError("Original note IDs/witness missing")
 if notes["original_verses"]!=1 or notes["complete_original_commentary_paragraphs"]!=1:
  raise ValueError("One complete verse and commentary must be preserved")
 if (sha(NOTES),sha(WIT))!=(a["notes_SHA256"],a["witness_SHA256"]):
  raise ValueError("Source original witness mismatch")
 if not(arc["ZIP_CRC_verified"] and arc["every_member_sha_size_verified"] and arc["independent_cold_source_tests_green"]==9):
  raise ValueError("Independent cold source archive test incomplete")
 archive=Path(arc["owner_archive_path"])
 if not archive.is_file() or sha(archive)!=arc["archive_SHA256"]:
  raise ValueError("Owner source archive missing/changed")
 if notes["human_blind_predictive_validations"] or notes["runtime_promotions"]:
  raise ValueError("Historic source falsely counted real humans")
 REC.mkdir(exist_ok=False)
 for p,n in ((OLD,"CHINESE_V29_BEFORE_30.json"),(CURRENT,"CHINESE_CURRENT_BEFORE_30.md")):
  (REC/n).write_bytes(p.read_bytes())
 new=copy.deepcopy(old)
 new.update({"schema":"ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V30",
  "status":"BAZI_DTS24_MAJOR_MINORITY_ORIGINAL_SOURCE_ONLY",
  "as_of_utc":"2026-10-21","prior_index":"CHINESE_SOURCE_AUDIT_INDEX_V29.json",
  "prior_index_sha256":OLD_SHA,"sum_source_annotations":1289,
  "original_chinese_source_anchors_checked_against_revision":1217,
  "full_ziwei_original_text_collation_finished":False,
  "ziwei_complete_natal_calendar_engine_verified":False,
  "chinese_bazi_solar_term_engine_verified":False,
  "independently_validated_real_human_claims":0,"runtime_promotions":0})
 new["accepted_batches"].append({
  "id":"ChineseAstro-30SRC-BaZi-StrongWeak",
  "added_bazi_source_annotations":2,"added_ziwei_source_annotations":0,
  "start":"BZI-R0229","end":"BZI-R0230",
  "path":NOTES.relative_to(T).as_posix(),"rules_sha256":sha(NOTES),
  "witness_path":WIT.relative_to(T).as_posix(),"witness_sha256":sha(WIT),
  "source_manifest_path":MAN.relative_to(T).as_posix(),"source_manifest_sha256":sha(MAN),
  "original_online_source_oldid":844375,"full_raw_source_SHA256":RAW_SHA,
  "source_full_original_verse_count":1,
  "source_complete_commentary_paragraph_count":1,
  "source_majority_minority_elemental_claims_unverified":True,
  "original_ancient_print_critically_authenticated":False,
  "focused_source_tests_green":9,"cold_source_tests_green":9,
  "independent_human_predictions_validated":0,"runtime_astrology_promotions":0})
 bazi=new["systems"][0]
 bazi["accepted_source_annotations"]=230
 bazi["current_ids"]="BZI-R0001–BZI-R0230"
 bazi["next_id"]="BZI-R0231"
 bazi["current_batch"]="ChineseAstro-30SRC-BaZi-StrongWeak"
 bazi["source_files"].append(NOTES.relative_to(T).as_posix())
 bazi["chapter_coverage"]+=(
  " Original transmitted Di Tian Sui section24 眾寡論 oldid844375: one "
  "whole verse and one full paragraph on relative majority/minority "
  "and supporting strong vs restraining strong; source repeats phrases. Unverified narrative, "
  "not empirical personal risk or deterministic natal-calculation evidence."
 )
 new["next"]=(
  "Next original BaZi Di Tian Sui section25 first BZI-R0231, pin raw "
  "online oldid and source SHA before extracting. Zi Wei next possible "
  "ZWD-R1060 requires separately pinned new Volume III or older physical "
  "witness. Birth engine parity, frozen predictions and untouched-human tests OPEN."
 )
 new["historical_glyph_and_translator_limits"]+=(
  " Di Tian Sui short source 眾寡論 oldid844375 has conditional majority/minority "
  "strong/weak rhetoric and conditional symbolic strength; not authenticated Ming print, "
  "clinical or real-human predictive evidence."
 )
 if new["systems"][1]!=old["systems"][1] or new["accepted_batches"][:-1]!=old["accepted_batches"]:
  raise ValueError("Previously accepted Chinese batches or Zi Wei history altered")
 if sum(x["accepted_source_annotations"] for x in new["systems"])!=1289:
  raise ValueError("Cumulative Chinese source count mismatch")
 wr(NEW,new)
 heading=(
  "# Chinese BaZi V30 — original Di Tian Sui 眾寡論 source-only\n\n"
  "**Two additional original historical source notes BZI-R0229–BZI-R0230** "
  "from pinned Wikitext oldid844375 (one verse and one whole commentary). "
  "CRC/source SHA and 9/9 fresh cold-extracted original tests passed. "
  "**BaZi230 + ZiWei1059 =1289 documentary Chinese annotations**, NOT "
  "verified humans. Next **BZI-R0231 section25**, Zi Wei next possible "
  "ZWD-R1060 only with new Volume III. No authenticated original early "
  "printing, full natal chart calculation or genuine blind human "
  "prediction validation; human wins **0**, runtime promotions **0**.\n\n")
 CURRENT.write_text(heading+"## Previous accepted V29 source checkpoint\n\n"+
  (REC/"CHINESE_CURRENT_BEFORE_30.md").read_text(encoding="utf-8"),encoding="utf-8")
 LATEST.write_text(heading+(B/"ORIGINAL_SOURCE_REVIEW_20261021.md").read_text(encoding="utf-8"),encoding="utf-8")
 receipt={"batch":"ChineseAstro-30SRC-BaZi-StrongWeak",
  "status":"GUARDED_DTS24_ORIGINAL_SOURCE_V30_LOCAL_ACCEPTANCE",
  "Chinese_before":1287,"Chinese_after":1289,
  "BaZi_before":228,"BaZi_after":230,"ZiWei_unchanged":1059,
  "first_BZI":"BZI-R0229","last_BZI":"BZI-R0230",
  "next_BZI":"BZI-R0231","next_ZiWei":"ZWD-R1060",
  "prior_V29_index_SHA256":OLD_SHA,"new_V30_index_SHA256":sha(NEW),
  "source_oldid":844375,"source_full_SHA256":RAW_SHA,
  "notes_SHA256":sha(NOTES),"witness_SHA256":sha(WIT),
  "archive_SHA256":arc["archive_SHA256"],"cold_source_tests_green":9,
  "independent_old_print_authenticated":False,
  "human_blind_predictive_validations":0,"runtime_promotions":0}
 wr(B/"CANONICAL_PREPARE_RECEIPT_20261021.json",receipt)
 print(json.dumps(receipt,ensure_ascii=False,indent=2))
if __name__=="__main__":accept()
