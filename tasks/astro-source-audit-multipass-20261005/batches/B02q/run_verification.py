"""Single test runner: exact distinct IDs, source input hashes and output log."""
from pathlib import Path
import hashlib,io,json,sys,unittest
B=Path(__file__).resolve().parent
suite=unittest.defaultTestLoader.discover(str(B),pattern="test_*.py")
def enumerate_ids(q):
 for x in q:
  if isinstance(x,unittest.TestSuite): yield from enumerate_ids(x)
  else:yield x.id()
test_ids=sorted(enumerate_ids(suite))
assert len(test_ids)==len(set(test_ids)), "duplicate test identities"
out=io.StringIO()
res=unittest.TextTestRunner(stream=out,verbosity=2).run(suite)
log=out.getvalue()
(B/"TEST_RUN.log").write_text(log)
files=["RULES.json","COUNTS.json","SECTION_COVERAGE.json","SOURCE_IDENTITY.json",
       "SOURCE_IMAGE_MANIFEST.json","TABLE_GEOMETRY.json","ERRATA_COLLATION.json",
       "UNRESOLVED.json","AUDIT_REPORT.md","CLAIM_LEDGER.json",
       "SOURCE_FIRST_NOTES.md","test_lilly_crysis.py"]
files+=sorted(p.name for p in B.glob("test_*.py") if p.name not in files)
summary={"batch":"B02q","distinct_test_count":len(test_ids),"tests_run":res.testsRun,
         "discovered_test_ids":test_ids,"failures":len(res.failures),"errors":len(res.errors),
         "skipped":len(res.skipped),"successful":res.wasSuccessful(),
         "log_sha256":hashlib.sha256(log.encode()).hexdigest(),
         "source_file_sha256":{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in files},
         "scope":"Documentary structural/selected source-semantic regressions only; no astrology, clinical or medical predictive validity."}
(B/"TEST_RUN_SUMMARY.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({k:summary[k] for k in ["distinct_test_count","tests_run","failures","errors","skipped","successful"]}))
if not res.wasSuccessful():print(log)
sys.exit(0 if res.wasSuccessful() else 1)
