#!/usr/bin/env python3
"""Guarded BaZi Di Tian Sui 20 original two-note append, not a person evaluator."""
from pathlib import Path
from hashlib import sha256
import copy,json,subprocess

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V25.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V26.json"
RAW=B/"evidence/DiTianSui_20_oldid844370.wikitext"
PRIOR=T/"batches/ChineseAstro-25SRC-BaZi-SourceFlow/BAZI_DITIAN_SUI_19_6_SOURCE_NOTES_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261021_26SRC_BAZI20.md"
NOTES=B/"BAZI_DITIAN_SUI_20_2_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_DTS20_2_EXACT_OFFSET_WITNESS_V1.json"
MAN=B/"PINNED_DITIAN_SUI_20_SOURCE_MANIFEST_V1.json"
REC=B/"recovery"
LEASE=B/"WRITER_LEASE.json"
BR="research/astro-chinese-v26-bazi-dts20-original-source-20261021"
PRIOR_SHA="f5d2c95d6225bddc4b8a99fc5ddd923d61424a2002d5bb146c8693f72644c0df"
RAW_SHA="f646b66d51d6cd69a376e2b4e754c0b872ccbe24879772954579e03ae3639022"
def sha(p):return sha256(p.read_bytes()).hexdigest()
def rd(p):return json.loads(p.read_text("utf-8"))
def wr(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def git(*args):return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def untouched(p):
 rel=p.relative_to(ROOT).as_posix()
 if git("rev-parse","HEAD:"+rel)!=git("hash-object",str(p)):
  raise ValueError("Previously accepted source file changed "+rel)
def main():
 if git("branch","--show-current")!=BR or rd(LEASE)["status"]!="active":
  raise ValueError("V26 source writer branch/lease invalid")
 if any(p.exists() for p in (NEW,LATEST,REC,B/"CANONICAL_PREPARE_RECEIPT_20261021.json")):
  raise ValueError("Interrupted V26 index exists: reconcile before rerun")
 if sha(OLD)!=PRIOR_SHA or sha(RAW)!=RAW_SHA:
  raise ValueError("Previously accepted index or original text SHA changed")
 for p in (OLD,RAW,PRIOR,CURRENT,MAN):untouched(p)
 old=rd(OLD);notes=rd(NOTES);w=rd(WIT);a=rd(B/"ACCEPTANCE.json");arc=rd(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
 if (old["sum_source_annotations"],old["original_chinese_source_anchors_checked_against_revision"])!=(1275,1203):
  raise ValueError("V25 source total shifted")
 if old["accepted_batches"][-1]["id"]!="ChineseAstro-25SRC-BaZi-SourceFlow":
  raise ValueError("Prior BaZi accepted batch unexpected")
 if [(x["accepted_source_annotations"],x["next_id"]) for x in old["systems"]] !=[(216,"BZI-R0217"),(1059,"ZWD-R1060")]:
  raise ValueError("Source frontiers changed")
 if notes["source_oldid"]!=844370 or notes["source_full_sha256"]!=RAW_SHA:
  raise ValueError("Source text not properly pinned")
 if [r["id"] for r in notes["records"]]!=["BZI-R0217","BZI-R0218"]:
  raise ValueError("Source annotation IDs not exact")
 if notes["original_verse_count"]!=1 or notes["full_original_commentary_paragraphs"]!=1:
  raise ValueError("Full verse/commentary source coverage required")
 if (sha(NOTES),sha(WIT)) != (a["source_note_sha256"],a["source_witness_sha256"]):
  raise ValueError("Original notes/witness SHA mismatch")
 if w["original_full_source_sha256"]!=RAW_SHA or len(w["source_quotes"])!=2:
  raise ValueError("Exact quote witness incomplete")
 if not arc["ZIP_CRC_verified"] or not arc["all_members_sha256_size_verified"] or arc["independent_cold_source_test_count"]!=8:
  raise ValueError("Original cold source suite incomplete")
 p=Path(arc["archive_path"])
 if not p.is_file() or sha(p)!=arc["archive_sha256"]:
  raise ValueError("Owner cold archive changed since verified")
 if any(r["real_human_predictions_validated"] or r["runtime_astrology_promotions"] for r in notes["records"]):
  raise ValueError("Unvalidated historical source promoted")
 REC.mkdir(exist_ok=False)
 for p,name in ((OLD,"CHINESE_V25_BEFORE_26.json"),(CURRENT,"CHINESE_CURRENT_BEFORE_26.md")):
  (REC/name).write_bytes(p.read_bytes())
 new=copy.deepcopy(old)
 new.update({"schema":"ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V26",
  "status":"BAZI_DITIAN_SUI_20_CONNECTION_OBSTRUCTION_ORIGINAL_TRANSMITTED_TEXT_ONLY",
  "as_of_utc":"2026-10-21","prior_index":"CHINESE_SOURCE_AUDIT_INDEX_V25.json",
  "prior_index_sha256":PRIOR_SHA,"sum_source_annotations":1277,
  "original_chinese_source_anchors_checked_against_revision":1205,
  "full_ziwei_original_text_collation_finished":False,
  "ziwei_complete_natal_calendar_engine_verified":False,
  "chinese_bazi_solar_term_engine_verified":False,
  "independently_validated_real_human_claims":0,"runtime_promotions":0})
 new["accepted_batches"].append({"id":"ChineseAstro-26SRC-BaZi-Obstruction",
  "added_bazi_source_annotations":2,"added_ziwei_source_annotations":0,
  "start":"BZI-R0217","end":"BZI-R0218",
  "path":NOTES.relative_to(T).as_posix(),"rules_sha256":sha(NOTES),
  "witness_path":WIT.relative_to(T).as_posix(),"witness_sha256":sha(WIT),
  "source_manifest_path":MAN.relative_to(T).as_posix(),"source_manifest_sha256":sha(MAN),
  "original_source_oldid":844370,"original_raw_source_sha256":RAW_SHA,
  "source_original_verse_count":1,"source_complete_commentary_paragraph_count":1,
  "ancient_print_authenticity_unverified":True,"cold_source_test_replays_green":8,
  "actual_human_blind_predictions_validated":0,"runtime_astrological_rule_promotions":0})
 baz=new["systems"][0];baz["accepted_source_annotations"]=218
 baz["current_ids"]="BZI-R0001–BZI-R0218";baz["next_id"]="BZI-R0219"
 baz["current_batch"]="ChineseAstro-26SRC-BaZi-Obstruction"
 baz["source_files"].append(NOTES.relative_to(T).as_posix())
 baz["chapter_coverage"]+=(" Accepted Di Tian Sui section20 通隔論 transmitted online Wikitext oldid844370: one exact original verse and complete original commentary on five-phase connection/obstruction, not a deterministic birth-chart model or real human data.")
 new["next"]=("Next original BaZi 滴天髓/21 pinned independently before BZI-R0219; "
  "Zi Wei next possible ZWD-R1060 requires separately pinned Volume III. "
  "Independent historical printed editions, Chinese natal calendar engine, and blinded human tests remain OPEN.")
 new["historical_glyph_and_translator_limits"]+=(" Section20 通隔論 source oldid844370 transmits symbolical mediation among Five Phases; not early printed authenticated original or empirical human evidence.")
 if new["systems"][1]!=old["systems"][1] or new["accepted_batches"][:-1]!=old["accepted_batches"]:
  raise ValueError("Previously accepted Zi Wei/batches changed")
 if sum(x["accepted_source_annotations"] for x in new["systems"])!=1277:
  raise ValueError("New cumulative source total mismatched")
 wr(NEW,new)
 heading=(
  "# Chinese BaZi V26 — original Di Tian Sui section20 Connection/Obstruction\n\n"
  "**Two new historical source-only notes BZI-R0217–BZI-R0218**, one full verse "
  "and one full commentary paragraph in pinned Chinese Wikitext oldid844370, "
  "exact SHA/CP/UTF8 quote witnesses. Symbolic Five Phase mediating relations "
  "are not five empirically distinct predictions. "
  "**BaZi218+ZiWei1059=1277 historical source annotations**, not humans. "
  "Next **BZI-R0219 Di Tian Sui section21**, pending separately pinned source; "
  "next possible Zi Wei source ZWD-R1060 needs independent Volume III. "
  "Ancient print authenticity, chart/calendar engine and actual blind human tests "
  "still OPEN. Human forecast validations **0**, runtime promotions **0**.\n\n")
 CURRENT.write_text(heading+"## Previous Chinese V25 original checkpoint\n\n"+
  (REC/"CHINESE_CURRENT_BEFORE_26.md").read_text(encoding="utf-8"),encoding="utf-8")
 LATEST.write_text(heading+(B/"ORIGINAL_SOURCE_REVIEW_20261021.md").read_text(encoding="utf-8"),encoding="utf-8")
 receipt={"batch":"ChineseAstro-26SRC-BaZi-Obstruction",
  "status":"GUARDED_DITIAN_SUI20_ORIGINAL_SOURCE_V26_ACCEPTED_LOCALLY",
  "Chinese_before":1275,"Chinese_after":1277,
  "BaZi_before":216,"BaZi_after":218,"ZiWei_preserved":1059,
  "first_BZI":"BZI-R0217","last_BZI":"BZI-R0218",
  "next_BZI":"BZI-R0219","next_ZiWei":"ZWD-R1060",
  "old_index_V25_SHA256":PRIOR_SHA,"new_index_V26_SHA256":sha(NEW),
  "source_raw_oldid":844370,"source_raw_SHA256":RAW_SHA,
  "new_note_SHA256":sha(NOTES),"new_witness_SHA256":sha(WIT),
  "archive_SHA256":arc["archive_sha256"],"cold_original_tests_green":8,
  "original_early_print_authenticity_verified":False,
  "real_human_blind_predictive_validations":0,"runtime_promotions":0}
 wr(B/"CANONICAL_PREPARE_RECEIPT_20261021.json",receipt)
 print(json.dumps(receipt,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
