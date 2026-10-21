#!/usr/bin/env python3
"""Guarded immutable source-only index append, DTS22 真假論. No human outcomes."""
from pathlib import Path
from hashlib import sha256
import json,copy,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V27.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V28.json"
RAW=B/"evidence/DiTianSui_22_oldid844372.wikitext"
PRIOR=T/"batches/ChineseAstro-27SRC-BaZi-Clarity/BAZI_DITIAN_SUI_21_4_SOURCE_NOTES_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261021_28SRC_BAZI22.md"
NOTES=B/"BAZI_DITIAN_SUI_22_4_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_DTS22_4_EXACT_OFFSET_WITNESS_V1.json"
MAN=B/"PINNED_DITIAN_SUI_22_SOURCE_MANIFEST_V1.json"
LEASE=B/"WRITER_LEASE.json"
REC=B/"recovery"
BR="research/astro-chinese-v28-bazi-dts22-original-source-20261021"
OLD_SHA="00de501124cfba8167a52e0fc294ed3a25d1bc90bb98a8ae039c8627301f9d39"
RAW_SHA="50779be0d79b31711371bca6669a85c36110d4f5c25937d5e794c5c8c7515333"
def sha(p):return sha256(p.read_bytes()).hexdigest()
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def wr(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def git(*args):return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def clean_prior(p):
 rel=p.relative_to(ROOT).as_posix()
 if git("rev-parse","HEAD:"+rel)!=git("hash-object",str(p)):
  raise ValueError("Previously accepted source differs: "+rel)
def accept():
 if git("branch","--show-current")!=BR or rd(LEASE)["status"]!="active":
  raise ValueError("Wrong V28 source branch or inactive writer")
 if any(p.exists() for p in (NEW,LATEST,REC,B/"CANONICAL_PREPARE_RECEIPT_20261021.json")):
  raise ValueError("Existing interrupted V28 admission; reconcile before retry")
 if sha(OLD)!=OLD_SHA or sha(RAW)!=RAW_SHA:
  raise ValueError("Original online chapter or accepted predecessor SHA changed")
 for p in (OLD,RAW,PRIOR,CURRENT,MAN,NOTES,WIT):clean_prior(p)
 old=rd(OLD);notes=rd(NOTES);wit=rd(WIT);a=rd(B/"ACCEPTANCE.json")
 arc=rd(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
 if (old["sum_source_annotations"],old["original_chinese_source_anchors_checked_against_revision"])!=(1281,1209):
  raise ValueError("Prior V27 source counters differ")
 if old["accepted_batches"][-1]["id"]!="ChineseAstro-27SRC-BaZi-Clarity":
  raise ValueError("Prior accepted original Chinese batch changed")
 if [(x["accepted_source_annotations"],x["next_id"]) for x in old["systems"]] !=[(222,"BZI-R0223"),(1059,"ZWD-R1060")]:
  raise ValueError("Expected BaZi/ZiWei frontier not found")
 if len(notes["records"])!=4 or len(wit["quotes"])!=4 or [x["id"] for x in notes["records"]] != [f"BZI-R{i:04d}" for i in range(223,227)]:
  raise ValueError("Four full original source unit witnesses incomplete")
 if notes["original_verse_count"]!=2 or notes["complete_original_commentary_paragraphs"]!=2 or notes["source_oldid"]!=844372:
  raise ValueError("Original section22 source structure/revision differs")
 if notes["human_blind_predictive_validations"] or notes["runtime_astrology_promotions"]:
  raise ValueError("Historical source is not empirical human success")
 if (sha(NOTES),sha(WIT))!=(a["notes_sha256"],a["witness_sha256"]):
  raise ValueError("Already-frozen notes/witness SHA changed")
 if not(arc["ZIP_CRC_verified"] and arc["every_member_SHA256_and_bytes_verified"] and arc["cold_extracted_source_tests_green"]==9):
  raise ValueError("Cold independent original text tests required")
 path=Path(arc["owner_archive_path"])
 if not path.is_file() or sha(path)!=arc["archive_SHA256"]:
  raise ValueError("Owner's original-source ZIP differs/missing")
 REC.mkdir(exist_ok=False)
 for p,name in ((OLD,"CHINESE_V27_BEFORE_28.json"),(CURRENT,"CHINESE_CURRENT_BEFORE_28.md")):
  (REC/name).write_bytes(p.read_bytes())
 new=copy.deepcopy(old)
 new.update({"schema":"ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V28",
  "status":"BAZI_DTS22_TRUTH_FALSEHOOD_TWO_VERSES_TWO_COMMENTARIES_HISTORICAL_ONLY",
  "as_of_utc":"2026-10-21","prior_index":"CHINESE_SOURCE_AUDIT_INDEX_V27.json",
  "prior_index_sha256":OLD_SHA,"sum_source_annotations":1285,
  "original_chinese_source_anchors_checked_against_revision":1213,
  "full_ziwei_original_text_collation_finished":False,
  "ziwei_complete_natal_calendar_engine_verified":False,
  "chinese_bazi_solar_term_engine_verified":False,
  "independently_validated_real_human_claims":0,"runtime_promotions":0})
 new["accepted_batches"].append({
  "id":"ChineseAstro-28SRC-BaZi-Truth",
  "added_bazi_source_annotations":4,"added_ziwei_source_annotations":0,
  "start":"BZI-R0223","end":"BZI-R0226",
  "path":NOTES.relative_to(T).as_posix(),"rules_sha256":sha(NOTES),
  "witness_path":WIT.relative_to(T).as_posix(),"witness_sha256":sha(WIT),
  "source_manifest_path":MAN.relative_to(T).as_posix(),
  "source_manifest_sha256":sha(MAN),
  "source_online_oldid":844372,"full_source_raw_SHA256":RAW_SHA,
  "source_complete_verse_count":2,"source_complete_commentary_count":2,
  "historical_fate_wealth_moral_claims_unverified":True,
  "original_critical_print_authenticated":False,
  "source_tests_green":9,"cold_extracted_source_tests_green":9,
  "human_blind_predictive_validations":0,"runtime_promotions":0
 })
 baz=new["systems"][0];baz["accepted_source_annotations"]=226
 baz["current_ids"]="BZI-R0001–BZI-R0226"
 baz["next_id"]="BZI-R0227"
 baz["current_batch"]="ChineseAstro-28SRC-BaZi-Truth"
 baz["source_files"].append(NOTES.relative_to(T).as_posix())
 baz["chapter_coverage"]+=(
  " Pinned traditional Di Tian Sui chapter22 真假論 oldid844372, "
  "two full verses and two complete commentary paragraphs on seasonally "
  "supported true/false phases, clashes and hidden combinations, unverified "
  "authorial nobility/hardship/moral descriptions. No deterministic authentic "
  "old printed text, birth-calculation engine or human predictive results."
 )
 new["next"]=(
  "Next BaZi 滴天髓 chapter23, first BZI-R0227, pin online oldid/SHA "
  "independently first. Zi Wei next ZWD-R1060 requires a separately sourced "
  "Volume III or authenticated early printed edition. "
  "Real-human blind validation and independent calendar/natal engines remain OPEN."
 )
 new["historical_glyph_and_translator_limits"]+=(
  " Short DTS22 transmitted oldid844372 includes broad seasonal "
  "true/false factor categories and source literal 戊巳轉生, "
  "not critically emended. Source-character morality/wealth attributions "
  "are not human observational evidence."
 )
 if new["systems"][1]!=old["systems"][1] or new["accepted_batches"][:-1]!=old["accepted_batches"]:
  raise ValueError("Prior Chinese Zi Wei or historical source batches modified")
 if sum(x["accepted_source_annotations"] for x in new["systems"])!=1285:
  raise ValueError("Chinese cumulative document count arithmetic failed")
 wr(NEW,new)
 intro=(
  "# Chinese BaZi V28 — Di Tian Sui 22 source original text\n\n"
  "**Four new source-only historical notes BZI-R0223–R0226**, short online "
  "Wikitext oldid844372 真假論 (two full verses and two commentaries); "
  "original wording and UTF8/codepoint SHA frozen with 9/9 cold tests. "
  "**BaZi226 + ZiWei1059 =1285 Chinese documentary annotations**, not humans. "
  "Next **BZI-R0227 chapter23** (pin new source), Zi Wei next ZWD-R1060 "
  "requires new Volume III. Old printed original, verified calendar/astrology "
  "chart engine and real human predictive validity remain OPEN; 0 human "
  "validations and 0 runtime promotions.\n\n")
 CURRENT.write_text(intro+"## Previous accepted Chinese V27 checkpoint\n\n"+
  (REC/"CHINESE_CURRENT_BEFORE_28.md").read_text(encoding="utf-8"),encoding="utf-8")
 LATEST.write_text(intro+(B/"ORIGINAL_SOURCE_REVIEW_20261021.md").read_text(encoding="utf-8"),encoding="utf-8")
 receipt={
  "batch":"ChineseAstro-28SRC-BaZi-Truth",
  "status":"GUARDED_DTS22_ORIGINAL_SOURCE_V28_LOCAL_ACCEPTANCE",
  "Chinese_before":1281,"Chinese_after":1285,
  "BaZi_before":222,"BaZi_after":226,"ZiWei_unchanged":1059,
  "first_BZI":"BZI-R0223","last_BZI":"BZI-R0226",
  "next_BZI":"BZI-R0227","next_ZiWei":"ZWD-R1060",
  "prior_V27_index_SHA256":OLD_SHA,
  "new_V28_index_SHA256":sha(NEW),
  "source_oldid":844372,"source_raw_SHA256":RAW_SHA,
  "source_notes_SHA256":sha(NOTES),"source_witness_SHA256":sha(WIT),
  "archive_SHA256":arc["archive_SHA256"],
  "cold_source_tests_green":9,
  "authenticated_early_printed_edition":False,
  "human_blind_predictive_validations":0,"runtime_promotions":0
 }
 wr(B/"CANONICAL_PREPARE_RECEIPT_20261021.json",receipt)
 print(json.dumps(receipt,ensure_ascii=False,indent=2))
if __name__=="__main__":accept()
