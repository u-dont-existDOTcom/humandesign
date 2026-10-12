"""Assemble individually source-localized 1647 Lilly XLVIII, seventh-house bridge, 43 general aphorisms.

No predictive or clinical promotion. Input draft paraphrases are never direct source quotations.
"""
from pathlib import Path
import json,hashlib,collections
B=Path(__file__).resolve().parent
SOURCE_SHA="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
def rd(n):return json.loads((B/n).read_text())
def save(n,j):(B/n).write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n")
chap=rd("CHAPTER_AND_BRIDGE_DRAFT.json")["entries"]
aph=rd("APHORISMS_43_DRAFT.json")["records"]
assert len(chap)==25 and len(aph)==43
assert [x["number"] for x in aph]==list(range(1,44))
part=chap[:]+[{
 "kind":"xlix_next_heading","p":[336],
 "source":"Chapter XLIX, Of Marriage, begins BELOW the divider on original PDF336/printed302, immediately after aphorism 43; it is not extracted in this batch.",
 "pre":["Boundary follows the forty-third horary aphorism."],
 "lim":["Marriage chapter arguments on PDF336 lower and PDF337 onward are not part of B02r."],
 "group":"next_boundary",
}]
records=[]
for row in chap:
    records.append((row["p"],row["kind"],row["source"],row["pre"],row["lim"],row["group"],None))
for row in aph:
    records.append((row["p"],"general_horary_aphorism",row["source"],row["preconditions"],
                    row["exceptions_and_evidence_limits"],"general_horary_43",row["number"]))
row=part[-1]
records.append((row["p"],row["kind"],row["source"],row["pre"],row["lim"],row["group"],None))
assert len(records)==25+43+1==69
R=[]
for i,(pages,kind,statement,pre,limits,group,aphno) in enumerate(records):
    n=1852+i
    ref={
      "id":f"LI.1647.II.XLVIII-SEVENTH-HORARY.R{n}",
      "record_number":n,"source_id":"LILLY1647_WELLCOME_B30338724",
      "source_full_pdf_sha256":SOURCE_SHA,"work":"Christian Astrology (1647)",
      "book":"II","batch":"B02r",
      "printed_section":"XLVIII" if i<19 else "SEVENTH_HOUSE_INTRO" if i<25 else "GENERAL_HORARY_APHORISMS" if i<68 else "XLIX_BOUNDARY_ONLY",
      "source_locator":{
        "pdf_pages":pages,
        "printed_pages":[p-34 for p in pages],
        "page_images":[f"evidence/pdf-{p}.png" for p in pages],
        "source_paragraph_number":aphno,
        "source_statement_is_verbatim":False,
      },
      "source_record_kind":kind,
      "source_statement":statement,
      "source_statement_type":"NORMALIZED_PARAPHRASE_NOT_DIPLOMATIC_QUOTE",
      "preconditions":pre,
      "exceptions_and_evidence_limits":limits,
      "dependency_group":group,
      "case_evidence_countable":False,"independently_verified_outcome":False,
      "prospective_blinded_prediction":False,"clinical_efficacy_verified":False,
      "runtime_status":"REFERENCE_ONLY_NOT_PROMOTED",
      "historical_evidence_class":"ONE_ORIGINAL_1647_TEXT_ASSERTION_ONLY",
    }
    if aphno is not None:
        ref["aphorism_number"]=aphno
        ref["source_record_kind"]="general_horary_aphorism_no_"+str(aphno)
    R.append(ref)
assert [r["record_number"] for r in R]==list(range(1852,1921))
assert sum(r.get("aphorism_number") is not None for r in R)==43
assert len({r["aphorism_number"] for r in R if "aphorism_number" in r})==43
assert all(r["source_locator"]["page_images"] for r in R)
save("RULES.json",{
 "batch":"B02r","source_id":"LILLY1647_WELLCOME_B30338724",
 "first_record":"R1852","last_record":"R1920","record_count":len(R),
 "chapter_xlviii_own_units":19,"seventh_house_bridge_units":6,
 "general_horary_aphorism_units":43,"next_heading_boundary_units":1,
 "author_claims_43_in_seventh_intro":True,
 "not_the_previous_physician_43":True,
 "original_pdf_start":330,"original_pdf_end":336,
 "status":"DRAFT_AWAITING_INDEPENDENT_SOURCE_REVIEW",
 "original_cases_or_verified_outcomes_added":0,
 "clinical_or_predictive_validation":False,"rules":R
})
print(json.dumps({"new_units":len(R),"lilly_if_accepted":1851+len(R),
                  "combined_if_accepted":1851+len(R)+1066,
                  "aphorisms":43,"record_end":R[-1]["id"],
                  "kinds":dict(collections.Counter(r["dependency_group"] for r in R))}))
