#!/usr/bin/env python3
"""Freeze 真假論 complete historical source units without claiming human outcomes."""
from pathlib import Path
from hashlib import sha256
import json,re
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=B/"evidence/DiTianSui_22_oldid844372.wikitext"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V27.json"
MAN=B/"PINNED_DITIAN_SUI_22_SOURCE_MANIFEST_V1.json"
OLD_SHA="00de501124cfba8167a52e0fc294ed3a25d1bc90bb98a8ae039c8627301f9d39"
SRC_SHA="50779be0d79b31711371bca6669a85c36110d4f5c25937d5e794c5c8c7515333"
def sha(b):return sha256(b).hexdigest()
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def wr(name,obj):(B/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def freeze():
 raw=RAW.read_bytes();s=raw.decode("utf-8")
 old=rd(OLD);m=rd(MAN)
 if (sha(raw),len(raw),len(s))!=(SRC_SHA,1121,457):
  raise ValueError("Pinned Wikisource chapter22 original bytes changed")
 if (sha(OLD.read_bytes()),old["sum_source_annotations"])!=(OLD_SHA,1281):
  raise ValueError("Accepted Chinese V27 predecessor index SHA/count changed")
 if [(x["accepted_source_annotations"],x["next_id"]) for x in old["systems"]] != [(222,"BZI-R0223"),(1059,"ZWD-R1060")]:
  raise ValueError("Prior BaZi and Zi Wei source frontiers changed")
 if (m["online_oldid"],m["raw_UTF8_bytes"],m["raw_SHA256"])!=(844372,1121,SRC_SHA):
  raise ValueError("Source oldid/hash manifest changed")
 if not s.startswith("{{Novel|滴天髓|真假論|21|23|論}}"):
  raise ValueError("Source title/current short page changed")
 verses=re.findall(r"\{\{color\|red\|\{\{\+\|(.+?)\}\}\}\}",s,re.S)
 paras=re.findall(r"(?m)^:　　(.+)$",s)
 if len(verses)!=2 or len(paras)!=2:
  raise ValueError("Both whole verses and commentaries required")
 if not verses[0].startswith("令上尋真聚得真") or not verses[1].startswith("真假參差難辨論"):
  raise ValueError("Expected original verse source variant missing")
 if "不要金水亂之" not in paras[0] or "不能辨其勝負" not in paras[1] or "得巳丑暗邀" not in paras[1]:
  raise ValueError("Original seasonal/exception conditions missing")
 matched=[("TRANSMITTED_ORIGINAL_VERSE",verses[0]),("COMPLETE_TRANSMITTED_COMMENTARY",paras[0]),
          ("TRANSMITTED_ORIGINAL_VERSE",verses[1]),("COMPLETE_TRANSMITTED_COMMENTARY",paras[1])]
 records=[]
 for kind,q in matched:
  if s.count(q)!=1:raise ValueError("Source unit ambiguous/repeated")
  cp=s.index(q);bp=len(s[:cp].encode("utf-8"));encoded=q.encode("utf-8")
  if raw[bp:bp+len(encoded)]!=encoded:
   raise ValueError("Original CP/UTF8 source quote mismatch")
  records.append({"id":f"BZI-R{223+len(records):04d}","source":"BAZI-DTS-WIKISOURCE-TRANSMITTED",
    "batch":"ChineseAstro-28SRC-BaZi-Truth","source_chapter":"滴天髓/22",
    "source_oldid":844372,"full_original_source_sha256":SRC_SHA,
    "source_kind":kind,"original_chinese_exact_quote":q,
    "original_quote_sha256":sha(encoded),"original_quote_utf8_bytes":len(encoded),
    "original_codepoint_offset":cp,"original_utf8_byte_offset":bp,
    "historical_nobility_wealth_moral_outcome_not_independently_verified":True,
    "early_original_print_authenticated":False,
    "independently_blinded_human_predictions_validated":0,"runtime_promotions":0})
 notes={"schema":"BAZI_DTS22_TRUTH_FALSEHOOD_FOUR_SOURCE_NOTES_V1","batch":"ChineseAstro-28SRC-BaZi-Truth",
  "source_oldid":844372,"raw_source_utf8_bytes":1121,"raw_source_codepoints":457,
  "raw_source_sha256":SRC_SHA,"original_verse_count":2,
  "complete_original_commentary_paragraphs":2,"new_historical_documentary_notes":4,
  "first_id":"BZI-R0223","last_id":"BZI-R0226","next_id":"BZI-R0227",
  "next_ZiWei_id":"ZWD-R1060","short_source_seasonal_and_hidden_exceptions_preserved":True,
  "original_printed_critical_edition_authenticated":False,
  "calendar_and_natal_computation_independently_validated":False,
  "human_blind_predictive_validations":0,"runtime_astrology_promotions":0,"records":records}
 notes_file=B/"BAZI_DITIAN_SUI_22_4_SOURCE_NOTES_V1.json";wr(notes_file.name,notes)
 witness={"schema":"BAZI_DTS22_SOURCE_CP_UTF8_WITNESS_V1","source_oldid":844372,
  "source_full_SHA256":SRC_SHA,"source_raw_utf8_bytes":1121,
  "quotes":[{"id":r["id"],"cp":r["original_codepoint_offset"],
     "utf8_byte":r["original_utf8_byte_offset"],
     "quote_sha256":r["original_quote_sha256"],
     "quote_utf8_bytes":r["original_quote_utf8_bytes"]} for r in records],
  "human_predictive_validations":0}
 witness_file=B/"SOURCE_DTS22_4_EXACT_OFFSET_WITNESS_V1.json";wr(witness_file.name,witness)
 wr("ACCEPTANCE.json",{"batch":"ChineseAstro-28SRC-BaZi-Truth",
   "Chinese_before":1281,"new_records":4,"Chinese_after":1285,
   "BaZi_before":222,"BaZi_after":226,"ZiWei_unchanged":1059,
   "first":"BZI-R0223","last":"BZI-R0226","next":"BZI-R0227",
   "old_index_V27_SHA256":OLD_SHA,"source_oldid":844372,"source_SHA256":SRC_SHA,
   "notes_sha256":sha(notes_file.read_bytes()),
   "witness_sha256":sha(witness_file.read_bytes()),
   "human_blind_predictions_validated":0,"runtime_promotions":0})
 print(json.dumps({"records":4,"first":"BZI-R0223","last":"BZI-R0226",
   "source_sha256":SRC_SHA},ensure_ascii=False,indent=2))
if __name__=="__main__":freeze()
