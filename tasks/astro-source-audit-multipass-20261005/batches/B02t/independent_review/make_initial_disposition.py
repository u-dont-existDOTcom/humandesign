"""Ledger all initial first-review IDs; preserve reviewer content as original witness."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
a=B/"OPUS_A_INITIAL.md";b=B/"OPUS_B_INITIAL.md"
assert hashlib.sha256(a.read_bytes()).hexdigest()=="e30df2b3ce3e6f1b2088919fbb04cce899f392f532fae14944f43e44d719a6fc"
assert hashlib.sha256(b.read_bytes()).hexdigest()=="20de3a61ac25b299d7de909710c05b10201884497e54e260c5b80487635fa455"
AA=["2205","2163,2164,2165","2183","2161,2162","2174,2175",
"2143,2268,2269,2270","2145,2267","2146","2272","2172","2200",
"2202","2151,2152,2153,2154","2186,2197,2207","2179","2192",
"2193,2194,2195","2169","2167,2168,2273","2141","2204",
"2271,2274,2275,2276,2277,2278,2279,2280,2281,2282,2283,2284,2285"]
BB=["2205","2233,2236","2239,2248","2251","2253","2227",
"2226","2225,2288","2287","2200","2202","2212,2213,2214",
"2286","2218,2291","2219,2292,2293,2294","2217","2216",
"2232,2289,2290","2230,2231","2197","2250","2207,2229",
"2236,2237","2233,2234,2252,2254,2255,2258,2259",
"2253","2242","2204"]
assert len(AA)==22 and len(BB)==27
f=[]
for k,ids in (("A",AA),("B",BB)):
 for n,rec in enumerate(ids,1):
  f.append({"source_issue":f"{k}.F{n:02d}","review_reference":f"OPUS_{k}_INITIAL.md",
    "severity_in_original_review":"MAJOR" if k=="A" and n<=7 else
                                  "MODERATE" if k=="A" else
                                  "HIGH" if n<=9 else "MEDIUM",
    "affected_record_ids":[f"R{x}" for x in rec.split(",")],
    "controller_disposition":"SOURCE_CORRECTED_OR_EXPLICITLY_QUALIFIED",
    "independent_final_post_correction_validation_not_implied":True})
d={"batch":"B02t","phase":"1",
   "initial_image_first_reviews":2,"original_pdf_page_windows":{"A":[353,359],"B":[359,364]},
   "source_original_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
   "reviewer_A_sha256":hashlib.sha256(a.read_bytes()).hexdigest(),
   "reviewer_B_sha256":hashlib.sha256(b.read_bytes()).hexdigest(),
   "original_findings_count":len(f),"findings":f,
   "disposition_scope":"Controller repairs source paragraphs and preserves unresolved meanings; reviewers' original diagnoses remain immutable.",
   "separately_staged_clean_post_correction_readbacks":2,
   "no_human_or_animal_prediction_validated":True}
(B/"INITIAL_FINDINGS_DISPOSITION.json").write_text(json.dumps(d,indent=2)+"\n")
print(json.dumps({"initial_independent_windows":2,"findings":len(f),"pinned_original_reviews":2}))
