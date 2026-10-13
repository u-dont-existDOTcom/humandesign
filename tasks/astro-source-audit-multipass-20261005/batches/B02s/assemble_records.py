from pathlib import Path
import json
B=Path(__file__).resolve().parent
P=sorted(B.glob("PART_*.json"))
rows=[(p.name,r) for p in P for r in json.loads(p.read_text())["records"]]
assert len(P)>=25 and len(rows)>110,(len(P),len(rows))
seen=set()
result=[]
for i,(part,row) in enumerate(rows):
 n=1921+i
 assert row["kind"] not in seen,row["kind"]
 seen.add(row["kind"])
 assert all(336<=x<=353 for x in row["pages"])
 result.append({
 "id":f"LI.1647.II.XLIX.R{n}","record_number":n,
 "batch":"B02s","chapter":"XLIX","book":"II",
 "source_full_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
 "source_locator":{"pdf_pages":row["pages"],"printed_pages":[p-34 for p in row["pages"]],"page_images":[f"evidence/pdf-{p}.png" for p in row["pages"]],"source_statement_is_verbatim":False},
 "source_record_kind":row["kind"],"source_statement":row["source_statement"],
 "source_statement_type":"NORMALIZED_PARAPHRASE_NOT_VERBATIM",
 "preconditions":["Use the exact conditions embedded in the source statement, without adding modern assumptions."],
 "exceptions_and_evidence_limits":row["limitations"],"draft_part":part,
 "case_evidence_countable":False,"independently_verified_outcome":False,
 "prospective_frozen_forecast":False,"runtime_status":"REFERENCE_ONLY_NOT_PROMOTED"})
doc={"batch":"B02s","status":"DRAFT_SOURCE_ONLY","record_count":len(result),"first_record":"R1921","last_record":f"R{1920+len(result)}","rules":result}
(B/"RULES.json").write_text(json.dumps(doc,indent=2,ensure_ascii=False)+"\n")
print(json.dumps({"source_parts":len(P),"records":len(result),"candidate_lilly":1920+len(result),"candidate_combined":2986+len(result)}))
