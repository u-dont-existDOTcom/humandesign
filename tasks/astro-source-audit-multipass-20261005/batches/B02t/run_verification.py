"""Run every unique B02t source-only regression and freeze artifact hashes."""
import hashlib,json,io,sys,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
suite=unittest.defaultTestLoader.discover(str(B),pattern="test_*.py")
def tests(s):
 for x in s:
  if isinstance(x,unittest.TestSuite):yield from tests(x)
  else:yield x.id()
names=sorted(tests(suite))
assert len(names)==len(set(names)), "duplicate test IDs"
buf=io.StringIO()
res=unittest.TextTestRunner(stream=buf,verbosity=2).run(suite)
log=buf.getvalue()
(B/"TEST_RUN.log").write_text(log)
files=[
 "PHASE1_RULES_DRAFT.json","SOURCE_IDENTITY.json","SOURCE_IMAGE_MANIFEST.json",
 "SOURCE_REPLAY_RECEIPT.json","SECTION_COVERAGE.json","COUNTS.json","ERRATA_COLLATION.json",
 "UNRESOLVED.json","AUDIT_REPORT.md","CLAIM_LEDGER.json",
 "SOURCE_FIRST_NOTES.md","RETAINED_LILLY_INDEX_BEFORE.json"
]+sorted(x.name for x in B.glob("test_*.py"))
summ={"batch":"B02t","phase":"1","successful":res.wasSuccessful(),"tests_run":res.testsRun,
      "distinct_test_count":len(names),"test_ids":names,"failures":len(res.failures),
      "errors":len(res.errors),"skipped":len(res.skipped),
      "test_log_sha256":hashlib.sha256(log.encode()).hexdigest(),
      "source_file_sha256":{x:hashlib.sha256((B/x).read_bytes()).hexdigest() for x in files},
      "scope":"Consistent documentary source description and provenance only. Does not show astrological, clinical, legal or criminal-prediction validity."}
(B/"TEST_RUN_SUMMARY.json").write_text(json.dumps(summ,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({k:summ[k] for k in ("tests_run","distinct_test_count","successful","failures","errors","skipped")}))
if not res.wasSuccessful():print(log)
sys.exit(0 if res.wasSuccessful() else 1)
