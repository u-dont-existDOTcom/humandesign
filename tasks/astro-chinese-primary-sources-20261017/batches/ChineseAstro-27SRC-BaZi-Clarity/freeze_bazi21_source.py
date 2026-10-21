#!/usr/bin/env python3
"""Read-only independent reconstruction of the pinned DTS21 source.
Never overwrite an already accepted historical text record with a draft schema.
"""
from pathlib import Path
from hashlib import sha256
import json,re

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=B/"evidence/DiTianSui_21_oldid844371.wikitext"
PRIOR=T/"CHINESE_SOURCE_AUDIT_INDEX_V26.json"
NOTES=B/"BAZI_DITIAN_SUI_21_4_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_DTS21_4_EXACT_OFFSET_WITNESS_V1.json"
EXPECTED_SOURCE="9ff7673e7a7a8af1cace52457d801d631ca117f5923e8e3433f7b1d05729be0f"
EXPECTED_PREV="f4b69767eb143994766bc9a7c08f7ed1e519bddf234377c9ecc65bcb6080f94f"
EXPECTED_NOTES="4fa395fafec6883d84957cc70bf1bf72be996d5e4d3fd82c6883272bb546c8ba"
EXPECTED_WIT="b2edd9bf20368dda3ec489341f5e48394c4da1d0725fa492015b91ca3cf598a2"

def sha(b):return sha256(b).hexdigest()
def rd(p):return json.loads(p.read_text(encoding="utf-8"))

def verify():
    raw=RAW.read_bytes();s=raw.decode("utf-8")
    old=rd(PRIOR);notes=rd(NOTES);witness=rd(WIT)
    if (len(raw),len(s),sha(raw))!=(1172,474,EXPECTED_SOURCE):
        raise ValueError("Pinned oldid844371 source changed")
    if sha(PRIOR.read_bytes())!=EXPECTED_PREV or old["sum_source_annotations"]!=1277:
        raise ValueError("Accepted prior Chinese V26 index changed")
    if (sha(NOTES.read_bytes()),sha(WIT.read_bytes()))!=(EXPECTED_NOTES,EXPECTED_WIT):
        raise ValueError("Published note/witness SHA differs; reconcile, do not overwrite")
    verses=[m.group(1) for m in re.finditer(r"\{\{color\|red\|\{\{\+\|(.+?)\}\}\}\}",s,re.S)]
    prose=[m.group(1) for m in re.finditer(r"(?m)^:　　(.+)$",s)]
    if len(verses)!=2 or len(prose)!=2:raise ValueError("Full source verse and paragraphs missing")
    ordered=[verses[0],prose[0],verses[1],prose[1]]
    if len(notes["records"])!=4 or len(witness["quotes"])!=4:
        raise ValueError("Published four source records absent")
    results=[]
    for i,(q,n,w) in enumerate(zip(ordered,notes["records"],witness["quotes"])):
        ident=f"BZI-R{219+i:04d}";cp=s.index(q)
        utf8=len(s[:cp].encode("utf-8"));quoted=q.encode("utf-8")
        if s.count(q)!=1 or raw[utf8:utf8+len(quoted)]!=quoted:
            raise ValueError("Source quote ambiguous or byte mismatch: "+ident)
        actual=(ident,cp,utf8,sha(quoted),len(quoted))
        expected=(n["id"],n["original_codepoint_offset"],n["original_utf8_byte_offset"],
                  n["original_quote_sha256"],n["original_quote_utf8_bytes"])
        independent=(w["id"],w["cp"],w["utf8_byte"],w["quote_sha256"],w["quote_utf8_bytes"])
        if actual!=expected or actual!=independent or n["original_chinese_exact_quote"]!=q:
            raise ValueError("Source annotation/witness mismatch: "+ident)
        if n["independent_blinded_human_predictions_validated"] or n["runtime_promotions"]:
            raise ValueError("Historic commentary not a human forecast")
        results.append({"id":ident,"cp":cp,"utf8_byte":utf8,"sha256":sha(quoted)})
    return {"source_revision":844371,"full_source_SHA256":EXPECTED_SOURCE,
            "full_source_bytes":1172,"verse_count":2,"complete_commentary_count":2,
            "source_record_count":4,"records":results,"real_human_validation":0}

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
