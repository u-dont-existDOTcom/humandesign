from __future__ import annotations
import hashlib, json
from pathlib import Path

BASE=Path(__file__).resolve().parent
LETTERS={c:(i%9)+1 for i,c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
MASTERS={11,22,33}
KARMIC={13,14,16,19}

def reduce_num(n:int,preserve_master:bool=True):
    chain=[n]
    while n>=10 and not (preserve_master and n in MASTERS):
        n=sum(int(x) for x in str(n)); chain.append(n)
    return n,chain

def reduce_single(n:int):
    return reduce_num(n,False)

def component_name(name:str,mode:str):
    rows=[]
    for part in name.upper().split():
        chars=[c for c in part if c in LETTERS]
        if mode=="vowels": chars=[c for c in chars if c in "AEIOU"]
        elif mode=="consonants": chars=[c for c in chars if c not in "AEIOU"]
        raw=sum(LETTERS[c] for c in chars)
        red,chain=reduce_num(raw,True)
        rows.append({"part":part,"letters":chars,"values":[LETTERS[c] for c in chars],"raw":raw,"reduced":red,"chain":chain})
    total=sum(r["reduced"] for r in rows)
    final,chain=reduce_num(total,True)
    return {"parts":rows,"component_sum":total,"number":final,"final_chain":chain}

def profile(name:str):
    return {"name":name,"expression":component_name(name,"all"),"soul_urge":component_name(name,"vowels"),"personality":component_name(name,"consonants")}

def active_letter(component:str,age:int):
    chars=[c for c in component.upper() if c in LETTERS]
    pos=age % sum(LETTERS[c] for c in chars)
    cursor=0
    for c in chars:
        v=LETTERS[c]
        if pos < cursor+v: return c,v
        cursor += v
    raise AssertionError

birth_name="Hatice Hale Baysan"
names=[
  {"label":"birth_to_2016","name":"Hatice Hale Baysan","start":"1994-01-28","end":"2016 (exact transition date unknown)","role":"birth-name core + use-name overlay"},
  {"label":"married_2016_to_2019","name":"Hatice Hale Aru","start":"2016 (exact date unknown)","end":"2019 (exact transition date unknown)","role":"time-stamped changed-name overlay; partner-derived surname"},
  {"label":"2019_to_divorce_2021","name":"Hatice Hale Baysan Aru","start":"2019 (exact date unknown)","end":"2021 divorce transition (exact date unknown)","role":"time-stamped changed-name overlay; includes partner-derived surname"},
  {"label":"post_divorce_2021","name":"Hatice Hale Baysan","start":"2021 after divorce (exact date unknown)","end":"later 2021 name change (exact date unknown)","role":"time-stamped changed-name overlay"},
  {"label":"hale_denizden_2021_onward","name":"Hale Denizden","start":"2021 (exact date unknown)","end":None,"role":"current chosen-name overlay"},
]
for row in names: row["profile"]=profile(row["name"])

life_path=7
expr=names[0]["profile"]["expression"]["number"]
maturity_raw=life_path+expr
maturity,maturity_chain=reduce_num(maturity_raw,True)

transits=[]
for age in range(0,61):
    pl,pv=active_letter("Hatice",age)
    ml,mv=active_letter("Hale",age)
    sl,sv=active_letter("Baysan",age)
    compound=pv+mv+sv
    reduced,_=reduce_single(compound)
    transits.append({
      "age":age,"birthday_start":f"{1994+age}-01-28",
      "physical":{"component":"Hatice","letter":pl,"value":pv},
      "mental":{"component":"Hale","letter":ml,"value":mv},
      "spiritual":{"component":"Baysan","letter":sl,"value":sv},
      "essence":{"compound":compound,"reduced":reduced,
                 "master":compound if compound in MASTERS else None,
                 "karmic_debt":compound if compound in KARMIC else None}
    })

report={
 "schema":"hale-name-input-correction-v3",
 "classification":"post-freeze input correction; no personality/survey outcome data inspected",
 "correction":{
   "previous_birth_name_input":"Hatice Baysan",
   "corrected_birth_name_interpretation":"Hatice Hale Baysan",
   "basis":"User stated the name was Hatice Hale Baysan until 2016.",
   "scope":"Supersedes V2 name-derived numerology and fusion claims that depended on the incomplete birth name. Astrology and birth-date numerology are unchanged."
 },
 "protocol":{
   "system":"frozen Pythagorean/Decoz-style",
   "y_treatment":"consonant",
   "birth_name_primary":True,
   "changed_names":"time-stamped overlays only; never projected backward",
   "birth_name_transits":{"physical":"first name Hatice","mental":"middle name Hale","spiritual":"last name Baysan"},
   "event_validity":"Marriage/divorce/name-change dates are now revealed inputs and cannot be counted as independent timing-validation hits."
 },
 "birth_name_profile":names[0]["profile"],
 "maturity":{"raw":maturity_raw,"number":maturity,"chain":maturity_chain,"karmic_debt":maturity_raw if maturity_raw in KARMIC else None},
 "name_history":names,
 "birth_name_transits_essences":transits,
 "unchanged_date_numbers":{"life_path":7,"birthday":"28/1","attitude":"29/11/2 -> 2","pinnacles":[2,6,8,6],"challenges":[0,4,4,4],"periods":[1,1,5]},
}
out=BASE/"NAME_INPUT_CORRECTION_V3.json"
out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
print(out)
print("sha256",hashlib.sha256(out.read_bytes()).hexdigest())
for row in names:
    p=row["profile"]
    print(row["name"],"=",p["expression"]["number"],p["soul_urge"]["number"],p["personality"]["number"])
print("maturity",maturity_raw,maturity)
