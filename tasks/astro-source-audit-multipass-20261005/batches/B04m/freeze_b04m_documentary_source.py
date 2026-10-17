#!/usr/bin/env python3
"""Historical first-edition source admission for printed XCII / editorial XCIII."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
J=lambda n:json.loads((B/n).read_text(encoding="utf-8"))
H=lambda n:hashlib.sha256((B/n).read_bytes()).hexdigest()
def put(n,x):(B/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
outputs=["RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
         "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
assert not any((B/n).exists() for n in outputs)
I=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
D=J("SOURCE_FIRST_CLAUSES_DRAFT.json");M=J("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json")
W=J("SOURCE_WINDOW_MANIFEST.json");U=J("UNRESOLVED_SOURCE_LIMITS.json")
assert I["records_count"]==5338 and I["batches"][-1]["id"]=="B04l"
assert I["next"]["chapter"]=="XCIII" and I["next"]["pdf_page"]==498
assert I["read_numbered_chapters"]==list(range(1,93))
assert I["source_sha256"]==W["original_full_pdf_sha256"]
assert I["empirical_validations"]==I["runtime_promotions"]==0
assert D["source_units"]==75 and M["span_count"]==11
assert len(U["issues"])==28
assert (B/"SOURCE_FIRST_IMAGE_AUDIT_20261017.md").is_file()
for w in W["original_images"]:
 assert H(w["path"])==w["sha256"] and (B/w["path"]).stat().st_size==w["bytes"]
ids=[r["source_local_id"] for r in D["rows"]]
mapped=[k for s in M["source_spans"] for k in s["mapped_local_ids"]]
assert len(mapped)==len(set(mapped))==75 and sorted(mapped)==sorted(ids)
rby={r["source_local_id"]:r for r in D["rows"]}
assert all(set(rby[k]["original_pdf_pages"]).issubset(set(s["original_pdf_pages"]))
           for s in M["source_spans"] for k in s["mapped_local_ids"])
assert all(r["chapter"]=="XCIII" for r in D["rows"][:-3])
assert all(r["chapter"]=="XCIV_NAVIGATION_ONLY" for r in D["rows"][-3:])
rules=[]
for n,r in enumerate(D["rows"],start=5339):
 rules.append({**r,"id":f"R{n}","record_number":n,"global_record_number":n,
  "historical_documentary_accepted":True,
  "accepted_for_primary_historical_text_reference":True,
  "independently_authenticated_occult_causation":False,
  "independently_authenticated_treatment_success":False,
  "empirically_validated_prediction":False,"runtime_model_promoted":False})
assert [r["record_number"] for r in rules]==list(range(5339,5414))
R={"batch":"B04m",
 "kind":"FIRST_EDITION_UNVERIFIED_WITCHCRAFT_AND_HISTORICAL_RITUAL_SOURCE",
 "status":"LOCALLY_ADMITTED_PENDING_GITHUB",
 "documentary_accepted_locally":True,
 "record_count":75,"first_record":5339,"last_record":5413,
 "chapter_substantive_source_annotations":72,"next_heading_navigation_only":3,
 "original_pdf_pages":[498,499,500,501],
 "source_reverse_passages":11,"source_unresolved_limits":28,
 "unnumbered_remedies_part_of_current_chapter":True,
 "printed_chapter":"XCII","editorial_chapter":"XCIII",
 "independent_verified_witchcraft_cases":0,
 "independent_medical_diagnoses":0,
 "independent_verified_remedy_outcomes":0,
 "new_empirically_validated_predictions":0,"runtime_promotions":0,
 "rules":rules}
put("RULES.json",R)
idmap={r["source_local_id"]:r["id"] for r in rules}
put("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",{
 "batch":"B04m","span_count":11,
 "source_spans":[{**s,"accepted_global_record_ids":[idmap[k] for k in s["mapped_local_ids"]]}
                  for s in M["source_spans"]],
 "mapped_source_records":75})
put("SOURCE_ORDER.json",{"batch":"B04m","first_record":5339,
 "last_record":5413,"record_count":75,"original_pdf_pages":[498,499,500,501],
 "records":[{"record_number":r["record_number"],"role":r["role"],
             "pdf_pages":r["original_pdf_pages"],"span_id":r["source_span_id"]}
            for r in rules],
 "empirically_validated_predictions":0})
U["status"]="ORIGINAL_FIRST_EDITION_UNCERTAINTIES_RETAINED"
put("UNRESOLVED.json",U)
rolecounts={}
for r in rules:rolecounts[r["role"]]=rolecounts.get(r["role"],0)+1
put("CLAIM_LEDGER.json",{"batch":"B04m","source_unit_count":75,
 "source_passages":11,"retained_source_limitations":28,
 "role_counts":rolecounts,
 "authorial_unverified_experiment_assertions":1,
 "independent_verified_supernatural_causes":0,
 "independent_medical_diagnoses":0,
 "independent_treatment_successes":0,
 "empirical_prediction_validations":0,"runtime_promotions":0})
A={"batch":"B04m","status":"DOCUMENTARY_ADMITTED_LOCAL_PENDING_ARCHIVE_AND_REMOTE",
 "prior_lilly_accepted":5338,"new_documentary_records":75,
 "first_record":"R5339","last_record":"R5413",
 "lilly_if_published":5413,"retained_ptolemy":1066,
 "combined_if_published":6479,"original_pdf_sha256":W["original_full_pdf_sha256"],
 "original_body_pdf_pages":[498,499,500],"following_heading_pdf":501,
 "next_chapter":"XCIV","next_printed_chapter":"XCIII",
 "source_reverse_passages":11,"source_unresolved_limits":28,
 "independent_occult_causes_verified":0,"independent_diagnoses":0,
 "independent_remedy_successes":0,"new_empirical_validations":0,
 "runtime_model_promotions":0,"independent_diplomatic_transcription":False,
 "remote_canonical_published":False}
for f,k in [("RULES.json","rules_sha256"),("SOURCE_ORDER.json","source_order_sha256"),
 ("UNRESOLVED.json","unresolved_sha256"),
 ("ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","reverse_map_sha256"),
 ("SOURCE_FIRST_IMAGE_AUDIT_20261017.md","source_audit_sha256")]:
 A[k]=H(f)
put("ACCEPTANCE.json",A)
print(json.dumps({"batch":"B04m","locally_accepted":75,
 "lilly_if_published":5413,"combined_if_published":6479,
 "new_empirical_validations":0}))
