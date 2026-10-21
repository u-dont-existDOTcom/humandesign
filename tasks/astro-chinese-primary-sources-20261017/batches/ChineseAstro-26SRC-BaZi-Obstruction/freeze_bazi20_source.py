#!/usr/bin/env python3
"""Original Chinese BaZi section20 verse/full commentary; exact byte source only."""
from __future__ import annotations
from hashlib import sha256
import json,re
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=B/"evidence/DiTianSui_20_oldid844370.wikitext"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V25.json"
MAN=B/"PINNED_DITIAN_SUI_20_SOURCE_MANIFEST_V1.json"
OLD_SHA="f5d2c95d6225bddc4b8a99fc5ddd923d61424a2002d5bb146c8693f72644c0df"
SRC_SHA="f646b66d51d6cd69a376e2b4e754c0b872ccbe24879772954579e03ae3639022"
def sha(blob):return sha256(blob).hexdigest()
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def wr(name,obj):(B/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def main():
 raw=RAW.read_bytes()
 if (len(raw),sha(raw))!=(577,SRC_SHA):raise ValueError("Pinned original raw bytes changed")
 idx=rd(OLD);manifest=rd(MAN)
 if sha(OLD.read_bytes())!=OLD_SHA or idx["sum_source_annotations"]!=1275 or idx["systems"][0]["next_id"]!="BZI-R0217":
  raise ValueError("Old accepted Chinese source frontier changed")
 if (manifest["oldid"],manifest["source_UTF8_bytes"],manifest["sha256"])!=(844370,577,SRC_SHA):
  raise ValueError("Source manifest oldid/binary identity changed")
 s=raw.decode("utf-8")
 if len(s)!=259 or not s.startswith("{{Novel|滴天髓|通隔論|19|21|論}}"):
  raise ValueError("Original source title/codepoints changed")
 verse=re.findall(r"\{\{color\|red\|\{\{\+\|(.+?)\}\}\}\}",s,flags=re.S)
 commentary=re.findall(r"(?m)^:　　(.+)$",s)
 if verse!=["兩意本相通，中間有關隔，此關若通也，到處歡相得。"] or len(commentary)!=1:
  raise ValueError("Source original verse and one full commentary not preserved")
 if "木土而得火" not in commentary[0] or "水火而得木" not in commentary[0] or "關通則滿局皆順遂矣" not in commentary[0]:
  raise ValueError("Flow-connection original commentary clauses changed")
 records=[]
 for layer,q in [("transmitted_verse",verse[0]),("original_full_commentary",commentary[0])]:
  if s.count(q)!=1:raise ValueError("Quote not unique in original Wikitext")
  cp=s.index(q);bp=len(s[:cp].encode("utf-8"));enc=q.encode("utf-8")
  if raw[bp:bp+len(enc)]!=enc:raise ValueError("Original Chinese CP/UTF8 mismatch")
  records.append({"id":f"BZI-R{217+len(records):04d}",
   "batch":"ChineseAstro-26SRC-BaZi-Obstruction",
   "source":"BAZI-DTS-WIKISOURCE-TRANSMITTED",
   "source_chapter":"滴天髓/20","source_oldid":844370,
   "original_full_source_sha256":SRC_SHA,"source_layer":layer,
   "original_exact_Chinese_quote":q,"quote_SHA256":sha(enc),
   "quote_UTF8_bytes":len(enc),"original_source_codepoint_offset":cp,
   "original_source_utf8_byte_offset":bp,
   "original_early_print_authority_authenticated":False,
   "real_human_predictions_validated":0,"runtime_astrology_promotions":0})
 if [x["id"] for x in records]!=["BZI-R0217","BZI-R0218"]:
  raise ValueError("Original source annotation count wrong")
 notes={"schema":"BAZI_DTS20_ONE_VERSE_FULL_COMMENTARY_SOURCE_ONLY_V1",
  "batch":"ChineseAstro-26SRC-BaZi-Obstruction",
  "source_oldid":844370,"source_full_sha256":SRC_SHA,
  "source_raw_bytes":577,"source_original_codepoints":259,
  "original_verse_count":1,"full_original_commentary_paragraphs":1,
  "new_historical_documentary_records":2,"first_id":"BZI-R0217",
  "last_id":"BZI-R0218","next_id":"BZI-R0219",
  "next_ZiWei_source_unchanged":"ZWD-R1060",
  "original_ancient_book_critically_authenticated":False,
  "source_hidden_stems_and_chart_engine_independently_verified":False,
  "real_human_blind_predictions_validated":0,"runtime_astrological_promotions":0,
  "records":records}
 note_path=B/"BAZI_DITIAN_SUI_20_2_SOURCE_NOTES_V1.json"
 wr(note_path.name,notes)
 wit_path=B/"SOURCE_DTS20_2_EXACT_OFFSET_WITNESS_V1.json"
 wr(wit_path.name,{"source_oldid":844370,"original_full_source_sha256":SRC_SHA,
   "source_quotes":[{"id":r["id"],"codepoint":r["original_source_codepoint_offset"],
   "utf8_byte_offset":r["original_source_utf8_byte_offset"],
   "quote_sha256":r["quote_SHA256"],"quote_utf8_bytes":r["quote_UTF8_bytes"]} for r in records],
   "actual_human_predictive_evaluations":0})
 wr("ACCEPTANCE.json",{"batch":"ChineseAstro-26SRC-BaZi-Obstruction",
  "prior_index_V25_sha256":OLD_SHA,"Chinese_before":1275,
  "BaZi_before":216,"ZiWei_unchanged":1059,
  "new_original_source_notes":2,"Chinese_after_if_accepted":1277,
  "BaZi_after_if_accepted":218,"first_id":"BZI-R0217",
  "last_id":"BZI-R0218","next_id":"BZI-R0219",
  "source_oldid":844370,"source_raw_sha256":SRC_SHA,
  "source_note_sha256":sha(note_path.read_bytes()),
  "source_witness_sha256":sha(wit_path.read_bytes()),
  "real_human_blind_predictive_validations":0,"runtime_promotions":0})
 print(json.dumps({"new_source_records":len(records),"next":notes["next_id"],
  "raw_source_sha256":SRC_SHA},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
