"""Produce UNACCEPTED phase1 documentary source records from original-image reading notes."""
import json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
parts=[B/f"PART{i}_SOURCE_DRAFT.json" for i in range(1,5)]
R=[]
for part in parts:
    d=json.loads(part.read_text())
    assert d["batch"]=="B02t"
    for item in d["records"]:
        assert item["pdf_pages"] and item["kind"] and item["statement"] and item["preconditions"]
        R.append((part.name,item))
assert len(R)>100,len(R)
assert len({row["kind"] for _,row in R})==len(R),"Duplicate semantic kind"
print("DRAFT_UNITS",len(R))
prev=json.loads((B.parents[1]/"LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
assert prev["records_count"]==2137 and prev["batches"][-1]["id"]=="B02s"
assert prev["next"]["chapter"]=="L"
source_sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
records=[]
for idx,(file,row) in enumerate(R):
    n=2138+idx
    pages=row["pdf_pages"]
    assert all(353<=x<=364 for x in pages),("out of phase",file,row["kind"],pages)
    records.append({
        "id":f"LI.1647.II.L.PHASE1.R{n}","record_number":n,
        "source_id":"LILLY1647_WELLCOME_B30338724",
        "source_full_pdf_sha256":source_sha,"batch":"B02t",
        "book":"II","chapter":"L","phase":"1_OF_MULTIPHASE",
        "source_locator":{"pdf_pages":pages,"printed_pages":[p-34 for p in pages],
          "page_images":[f"evidence/pdf-{p}.png" for p in pages],
          "source_statement_is_verbatim":False},
        "source_record_kind":row["kind"],
        "source_statement":row["statement"],
        "source_statement_type":"SOURCE_IMAGE_DERIVED_PARAPHRASE_NOT_VERBATIM",
        "preconditions":["Source condition is explicit only insofar as in source_statement; verify historical glyphs and conjunction logic against original image."],
        "exceptions_and_evidence_limits":row["preconditions"],
        "source_draft_part":file,
        "case_evidence_countable":False,
        "independently_authenticated_outcome":False,
        "prospective_blind_prediction":False,
        "clinical_or_criminal_inference_verified":False,
        "runtime_status":"REFERENCE_ONLY_NOT_PROMOTED",
    })
assert [r["record_number"] for r in records]==list(range(2138,2138+len(records)))
doc={"batch":"B02t","phase":"1","status":"SOURCE_PARAPHRASE_DRAFT_INDEPENDENT_REVIEW_NOT_STARTED",
  "source_start":"PDF353 printed319 BELOW opening divider",
  "source_end":"PDF364 printed330 BEFORE 'Of a Thief and Theft' heading",
  "record_count":len(records),
  "provisional_start":"R2138","provisional_end":f"R{records[-1]['record_number']}",
  "new_confirmed_cases":0,"source_only":True,
  "all_chapter_L_complete":False,
  "current_canonical_lilly_before":2137,
  "rules":records}
(B/"PHASE1_RULES_DRAFT.json").write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"draft_records":len(records),"provisional_ids":[records[0]["record_number"],records[-1]["record_number"]],
                  "canonical_source_count_unchanged":2137,
                  "chapter_complete":False}))
