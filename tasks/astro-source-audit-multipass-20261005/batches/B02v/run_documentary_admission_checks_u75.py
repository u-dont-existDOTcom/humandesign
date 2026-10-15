"""Run and freeze the source-only admission test suites against local source bytes.

No canonical mutation or empirical/predictive acceptance. If any test fails,
do not produce a positive receipt and preserve diagnostics.
"""
from pathlib import Path
import hashlib,json,re,subprocess
B=Path(__file__).resolve().parent
OUT=B/"TEST_RUN_SUMMARY.json"
assert not OUT.exists(),"Existing verification receipt present"
suites=[
 "test_source_integrity_v18.py",
 "test_reverse_20p_u75.py",
 "test_b02v_staging.py",
 "independent_review/test_reconciled_draft.py",
 "test_documentary_admission_u75.py"
]
rows=[]
for name in suites:
 r=subprocess.run(["python3",str(B/name)],capture_output=True,text=True,timeout=90)
 output=r.stdout+"\n"+r.stderr
 match=re.search(r"Ran (\d+) tests? in",output)
 count=int(match.group(1)) if match else None
 record={"suite":name,"exit_code":r.returncode,"tests_run":count,"tail":output.splitlines()[-6:]}
 rows.append(record)
 if r.returncode!=0 or count is None or ("OK" not in record["tail"]):
  print(json.dumps({"failure":record},indent=2))
  raise AssertionError("Tests not passing for source documentary admission")
assert len(rows)==5
assert [x["tests_run"] for x in rows]==[61,6,18,12,12],rows
files=["RULES.json","UNRESOLVED.json","SOURCE_ORDER.json","CLAIM_LEDGER.json","AUDIT_REPORT.md",
"RULES_DRAFT.json","UNRESOLVED_DRAFT.json","SOURCE_IMAGE_MANIFEST.json",
"independent_review/FINITE_HIGH_RISK_SOURCE_PASS_U75_20261015.json",
"independent_review/REVERSE_SOURCE_COVERAGE_20P_U75_20261015.json"]
def sha(path):return hashlib.sha256((B/path).read_bytes()).hexdigest()
o={"batch":"B02v","status":"SUCCESS_SOURCE_DOCUMENTARY_ONLY_NOT_EMPIRICAL",
"successful":True,"suite_results":rows,"distinct_test_count":sum(x["tests_run"] for x in rows),
"failures":0,"errors":0,"skipped":0,
"source_file_sha256":{x:sha(x) for x in files},
"accepted_locally_as_historical_documentary_only":True,"canonical_publication_pending":True,
"verified_astrology_predictions":0,"verified_criminal_identifications":0}
OUT.write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"test_suites":len(rows),"source_only_tests_passed":o["distinct_test_count"],"source_sha256_receipt":sha("TEST_RUN_SUMMARY.json")},indent=2))
