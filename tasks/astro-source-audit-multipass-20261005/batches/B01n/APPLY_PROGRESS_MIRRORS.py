"""Refresh the two secondary audit mirrors after restoring the verified B01n archive.

Does not alter source texts, historical batches, runtime or fitted models.
Refuses inconsistent checkpoints; keeps an already-updated mirror unchanged.
"""
from pathlib import Path
import json, subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-source-audit-multipass-20261005"
BASE="fc9b500a21842d1c8f940d8465822f4b0c8b6396"
subprocess.run(["git","merge-base","--is-ancestor",BASE,"HEAD"],cwd=ROOT,check=True)
current=json.loads((T/"CURRENT_PASS.json").read_text())
assert current["counts"]["source_records"]==708 and current["counts"]["ptolemy_read_sections"]==48
rules=json.loads((B/"RULES.json").read_text()); assert rules["records_count"]==78
nxt=current["next_range"]
plan=json.loads((T/"PASS_PLAN.json").read_text())
for p in plan["passes"]:
 if p["id"]=="P2":p["status"]="PTOLEMY_61_INDEXED;48_ENGLISH_SECTIONS_READ_MAPPED"
 elif p["id"]=="P3":p["status"]="ENGLISH_I_III_IV_COMPLETE;708_SOURCE_RECORDS;BOOKII_AND_OTHER_SOURCES_OPEN"
 elif p["id"]=="P4":p["status"]="525_CUMULATIVE_REFERENCE_TEST_INVENTORY;TWENTY_TARGETED_COMPARISONS;LATEST_RUN150_NOT_FULL_SUITE"
b=plan["batches"][0]; assert b["id"]=="B01"
b["next"]=nxt
if not any(x["id"]=="B01n" for x in b["completed_subbatches"]):
 b["completed_subbatches"].append({"id":"B01n","scope":"Full English IV.10 and both endings;Rhetorius46/49 and selected54 comparison","source_records":78,"new_predictions":0,"tests":86,"test_scope":"Exact rational/sign arithmetic, caller-qualified role logic and source integrity; not natal geometry or predictive validity.","targeted_cross_source_comparisons":3})
d=json.loads((T/"SECTION_DISCOVERY.json").read_text())
assert d["read_sections_count"] in (47,48)
sec=json.loads((B/"SECTION_COVERAGE.json").read_text())["sections"][0]
row=next(x for x in d["sections"] if x["book"]=="IV" and x["chapter"]==10)
assert row["status"] in ("INDEXED_NOT_READ","READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE")
row.update(status="READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE",locator_status="ENGLISH_AND_BOTH_ENDINGS_VERIFIED",rule_ids=sec["record_ids"],english_pdf_pages=sec["english_pdf_pages"],reading_receipt="batches/B01n/READING_RECEIPT.json",boundary=sec["boundary"])
d.update(read_sections_count=48,indexed_unread_count=13,body_locators_warning="Full English Books I/III/IV, including both endings, read/extracted; all13 BookII chapters remain unread. II.1-II.3 headings located only.")
for row in d["sections"]:
 if row["book"]=="II" and row["chapter"] in (1,2,3):row["locator_status"]="HEADING_LOCATED_ONLY_NOT_CHAPTER_READ"
for name,obj in [("PASS_PLAN.json",plan),("SECTION_DISCOVERY.json",d)]:
 (T/name).write_text(json.dumps(obj,indent=2)+"\n")
current["secondary_progress_mirrors"]["status"]="REFRESHED_FROM_VERIFIED_B01n_SOURCE_RECORDS"
(T/"CURRENT_PASS.json").write_text(json.dumps(current,indent=2)+"\n")
print("Secondary progress mirrors refreshed; full repository tests still require an actual run.")
