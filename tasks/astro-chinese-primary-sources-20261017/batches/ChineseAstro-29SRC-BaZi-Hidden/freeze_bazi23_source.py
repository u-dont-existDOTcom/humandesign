#!/usr/bin/env python3
"""Exact Wikitext 23 concealed/exposed factors; no human forecast assertions."""
from pathlib import Path
from hashlib import sha256
import json,re
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=B/"evidence/DiTianSui_23_oldid844373.wikitext"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V28.json"
MAN=B/"PINNED_DITIAN_SUI_23_SOURCE_MANIFEST_V1.json"
OLD_SHA="67fbee144329c39892a004c75213e08a0ca05189e0d5f548bb49927dbb44d4c0"
RAW_SHA="a883ddf8509bda86e3ecadcb9a8d1bfdf7b6cc8901fe20044c64f3b730e54ac1"
def sha(b):return sha256(b).hexdigest()
def rd(p):return json.loads(p.read_text("utf-8"))
def save(name,o):(B/name).write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def freeze():
 raw=RAW.read_bytes();s=raw.decode("utf-8");old=rd(OLD);m=rd(MAN)
 if (len(raw),len(s),sha(raw))!=(391,197,RAW_SHA):
  raise ValueError("Original pinned Wikitext oldid844373 differs")
 if (sha(OLD.read_bytes()),old["sum_source_annotations"])!=(OLD_SHA,1285):
  raise ValueError("Previous V28 accepted source changed")
 if [(x["accepted_source_annotations"],x["next_id"]) for x in old["systems"]] != [(226,"BZI-R0227"),(1059,"ZWD-R1060")]:
  raise ValueError("Expected old source frontier missing")
 if (m["pinned_oldid"],m["raw_bytes"],m["raw_sha256"])!=(844373,391,RAW_SHA):
  raise ValueError("Source pin manifest changed")
 if not s.startswith("{{Novel|滴天髓|隱顯論|22|24|論}}"):
  raise ValueError("Unexpected hidden/visible source title")
 verses=re.findall(r"\{\{color\|red\|\{\{\+\|(.+?)\}\}\}\}",s,re.S)
 comments=re.findall(r"(?m)^:　　(.+)$",s)
 if len(verses)!=1 or len(comments)!=1 or "吉神太露" not in verses[0] or "局中所喜之神" not in comments[0]:
  raise ValueError("Whole original one-verse one-commentary source changed")
 records=[]
 for kind,quote in [("TRANSMITTED_ORIGINAL_VERSE",verses[0]),("COMPLETE_TRANSMITTED_COMMENTARY",comments[0])]:
  if s.count(quote)!=1:raise ValueError("Ambiguous exact original quote")
  cp=s.index(quote);bp=len(s[:cp].encode("utf-8"));b=quote.encode("utf-8")
  if raw[bp:bp+len(b)]!=b:raise ValueError("Original absolute UTF8 witness failed")
  records.append({"id":f"BZI-R{227+len(records):04d}",
   "batch":"ChineseAstro-29SRC-BaZi-Hidden","source":"BAZI-DTS-WIKISOURCE-TRANSMITTED",
   "chapter":"滴天髓/23","original_online_oldid":844373,
   "source_raw_SHA256":RAW_SHA,"source_kind":kind,
   "original_exact_chinese_quote":quote,"original_quote_SHA256":sha(b),
   "original_quote_UTF8_bytes":len(b),"absolute_cp":cp,"absolute_utf8_byte":bp,
   "historic_fortune_threat_claim_not_observed_human_evidence":True,
   "original_early_print_authenticated":False,"blind_human_predictions_validated":0,"runtime_promotions":0})
 if [r["id"] for r in records]!=["BZI-R0227","BZI-R0228"]:
  raise ValueError("Two original source IDs not consecutive")
 notes={"schema":"BAZI_DTS23_EXPOSED_CONCEALED_TWO_ORIGINAL_SOURCE_NOTES_V1",
  "batch":"ChineseAstro-29SRC-BaZi-Hidden","oldid":844373,
  "raw_utf8_bytes":391,"raw_codepoints":197,"full_original_SHA256":RAW_SHA,
  "original_verses":1,"complete_original_commentary_paragraphs":1,
  "source_notes_count":2,"first_id":"BZI-R0227","last_id":"BZI-R0228",
  "next_id":"BZI-R0229","next_ZiWei_id":"ZWD-R1060",
  "ancient_printing_authenticated":False,"independent_natal_engine_parity_verified":False,
  "human_blind_predictive_validations":0,"runtime_promotions":0,"records":records}
 notesfile=B/"BAZI_DITIAN_SUI_23_2_SOURCE_NOTES_V1.json";save(notesfile.name,notes)
 wfile=B/"SOURCE_DTS23_2_EXACT_OFFSET_WITNESS_V1.json"
 save(wfile.name,{"source_oldid":844373,"source_full_SHA256":RAW_SHA,
  "original_quotes":[{"id":r["id"],"cp":r["absolute_cp"],"utf8_byte":r["absolute_utf8_byte"],
  "quote_SHA256":r["original_quote_SHA256"],"UTF8_bytes":r["original_quote_UTF8_bytes"]} for r in records],
  "actual_human_blind_validations":0})
 save("ACCEPTANCE.json",{"batch":"ChineseAstro-29SRC-BaZi-Hidden","Chinese_before":1285,
   "BaZi_before":226,"ZiWei_unchanged":1059,"new_notes":2,
   "Chinese_after_if_accepted":1287,"BaZi_after_if_accepted":228,
   "first":"BZI-R0227","last":"BZI-R0228","next":"BZI-R0229",
   "source_oldid":844373,"source_raw_SHA256":RAW_SHA,
   "notes_SHA256":sha(notesfile.read_bytes()),"witness_SHA256":sha(wfile.read_bytes()),
   "human_predictions_validated":0,"runtime_promotions":0})
 print(json.dumps({"new_records":2,"first":"BZI-R0227","last":"BZI-R0228",
   "full_original_SHA256":RAW_SHA},indent=2))
if __name__=="__main__":freeze()
