from __future__ import annotations
import json, unicodedata
from pathlib import Path

LETTERS={c:(i%9)+1 for i,c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
MASTERS={11,22,33}

def ascii_letters(text:str)->str:
    decomposed=unicodedata.normalize("NFKD",text)
    return "".join(c for c in decomposed if c.isascii())

def reduce_num(n:int,preserve_master:bool=True):
    chain=[n]
    while n>=10 and not (preserve_master and n in MASTERS):
        n=sum(int(x) for x in str(n)); chain.append(n)
    return n,chain

def component(name:str,mode:str):
    rows=[]
    for raw_part in name.split():
        part=ascii_letters(raw_part).upper()
        chars=[c for c in part if c in LETTERS]
        if mode=="vowels": chars=[c for c in chars if c in "AEIOU"]
        elif mode=="consonants": chars=[c for c in chars if c not in "AEIOU"]
        raw=sum(LETTERS[c] for c in chars)
        reduced,chain=reduce_num(raw,True)
        rows.append({"display_part":raw_part,"normalized_part":part,"raw":raw,"reduced":reduced,"chain":chain})
    component_sum=sum(x["reduced"] for x in rows)
    number,final_chain=reduce_num(component_sum,True)
    return {"parts":rows,"component_sum":component_sum,"number":number,"final_chain":final_chain}

def profile(name:str):
    return {"name":name,"expression":component(name,"all"),"soul_urge":component(name,"vowels"),"personality":component(name,"consonants")}

BASE=Path(__file__).resolve().parent
report={
    "schema":"hale-contemplated-name-calculation-v1",
    "normalization":"Unicode NFKD to ASCII base letters for the A-Z project table; display spelling retained.",
    "current":profile("Hale Denizden"),
    "contemplated":profile("Hatice Hâle Denizden"),
    "birth":profile("Hatice Hale Baysan"),
}
(BASE/"CONTEMPLATED_NAME_HATICE_HALE_DENIZDEN_CALC.json").write_text(json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+"\n")
print(json.dumps(report,indent=2,ensure_ascii=False))
