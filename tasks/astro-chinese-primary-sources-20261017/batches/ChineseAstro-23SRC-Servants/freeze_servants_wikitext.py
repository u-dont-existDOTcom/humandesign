#!/usr/bin/env python3
"""Original transmitted Chinese Zi Wei Servants text, historical only."""
from pathlib import Path
from hashlib import sha256
import json
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V22.json"
SOURCE_SHA="1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
OLD_SHA="3c3d74b9f53d10e7905f026733d902511bf19f2f0f64ae34bed9f4af894bba68"
A,Z=43499,44429
NAMES=["ZiWei","TianJi","TaiYang","WuQu","TianTong","LianZhen","TianFu",
"TaiYin","TanLang","JuMen","TianXiang","TianLiang","QiSha","PoJun",
"WenChang","WenQu","ZuoFu","YouBi","LuCun","QingYang","TuoLuo","HuoXing",
"LingXing","DouJun"]
def sha(x):return sha256(x).hexdigest()
def rd(p):return json.loads(p.read_text("utf-8"))
def save(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def freeze():
 raw=RAW.read_bytes();s=raw.decode("utf-8");old=rd(OLD)
 if (len(raw),sha(raw))!=(106736,SOURCE_SHA) or sha(OLD.read_bytes())!=OLD_SHA:
  raise ValueError("Pinned original or previous index changed")
 if old["sum_source_annotations"]!=1120 or [(x["accepted_source_annotations"],x["next_id"]) for x in old["systems"]] !=[(210,"BZI-R0211"),(910,"ZWD-R0911")]:
  raise ValueError("Unexpected accepted Chinese source sequence")
 if not s[A:].startswith("===八奴仆===") or not s[Z:].startswith("===九官禄==="):
  raise ValueError("Original Servants and Career boundaries missing")
 part=s[A:Z]
 (B/"SOURCE_1963110_SERVANTS_EXACT_EXCERPT.txt").write_bytes(part.encode("utf-8"))
 cp=A;records=[];markup=[]
 for rawline in part.splitlines(keepends=True):
  q=rawline.strip()
  pos=cp+(rawline.index(q) if q else 0)
  cp+=len(rawline)
  if not q:continue
  if q in ("<poem>","</poem>"):
   markup.append([pos,q]);continue
  n=len(records)
  if n>24:raise ValueError("Unexpected number of source lines")
  enc=q.encode("utf-8")
  bpos=len(s[:pos].encode("utf-8"))
  if s[pos:pos+len(q)]!=q or raw[bpos:bpos+len(enc)]!=enc:
   raise ValueError("Original source UTF8/Unicode mismatch")
  records.append({"id":f"ZWD-R{911+n:04d}","source":"ZWDS-CLASSIC-01",
   "batch":"ChineseAstro-23SRC-Servants","online_oldid":1963110,
   "full_Wikitext_source_SHA256":SOURCE_SHA,
   "source_group":"ServantsHeading" if n==0 else NAMES[n-1],
   "source_kind":"SOURCE_HEADING" if n==0 else "HISTORICAL_MASTER_SERVANT_CLAIM",
   "original_Chinese_exact_quote":q,"quote_SHA256":sha(enc),
   "quote_utf8_bytes":len(enc),"absolute_cp":pos,"absolute_utf8_offset":bpos,
   "original_Ming_woodblock_authenticated":False,
   "human_predictive_validations":0,"runtime_promotions":0})
 if (len(records),cp)!=(25,Z) or [x[1] for x in markup]!=["<poem>","</poem>"]:
  raise ValueError("Physical original line/markup boundary mismatch")
 if not any("奴多婢" in x["original_Chinese_exact_quote"] or "奴多" in x["original_Chinese_exact_quote"] for x in records):
  raise ValueError("Historically socially coded text unexpectedly changed")
 nxt="===九官禄==="
 q=nxt.encode("utf-8")
 records.append({"id":"ZWD-R0936","source":"ZWDS-CLASSIC-01",
  "batch":"ChineseAstro-23SRC-Servants","online_oldid":1963110,
  "full_Wikitext_source_SHA256":SOURCE_SHA,
  "source_group":"CareerNext","source_kind":"NEXT_CAREER_HEADING_NAVIGATION_ONLY",
  "original_Chinese_exact_quote":nxt,"quote_SHA256":sha(q),
  "quote_utf8_bytes":len(q),"absolute_cp":Z,
  "absolute_utf8_offset":len(s[:Z].encode("utf-8")),
  "original_Ming_woodblock_authenticated":False,
  "human_predictive_validations":0,"runtime_promotions":0})
 document={"schema":"CHINESE_V23_SERVANTS_ORIGINAL_ONLINE_SOURCE_ONLY",
  "batch":"ChineseAstro-23SRC-Servants","online_oldid":1963110,
  "source_full_sha256":SOURCE_SHA,"source_excerpt_cp_range":[A,Z],
  "source_excerpt_sha256":sha(part.encode("utf-8")),
  "source_nonmarkup_lines_including_heading":25,
  "source_historical_master_servant_lines":24,
  "next_Career_navigation_only":1,"original_poem_markup":markup,
  "historic_class_and_trustworthiness_claims_unverified":True,
  "early_printing_authenticated":False,
  "new_source_only_records":26,"first_id":"ZWD-R0911",
  "last_id":"ZWD-R0936","next_id":"ZWD-R0937",
  "real_human_blind_predictions_validated":0,"runtime_promotions":0,"records":records}
 notes=B/"ZIWEI_SERVANTS_26_SOURCE_NOTES_V1.json";save(notes,document)
 witness=B/"SOURCE_SERVANTS_26_OFFSET_WITNESS_V1.json"
 save(witness,{"source_SHA256":SOURCE_SHA,"excerpt_SHA256":document["source_excerpt_sha256"],
  "original_poem_markup":markup,"records":[{"id":r["id"],"cp":r["absolute_cp"],
  "utf8_offset":r["absolute_utf8_offset"],"quote_SHA256":r["quote_SHA256"]} for r in records]})
 print(json.dumps({"source_records":len(records),"first":records[0]["id"],
  "last":records[-1]["id"],"next":document["next_id"],
  "source_excerpt_sha256":document["source_excerpt_sha256"]},ensure_ascii=False))
if __name__=="__main__":freeze()
