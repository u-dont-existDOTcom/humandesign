"""Single deterministic B02s runner with unique test identities and file-hash receipt."""
from pathlib import Path
import hashlib,io,json,sys,unittest
B=Path(__file__).resolve().parent
suite=unittest.defaultTestLoader.discover(str(B),pattern="test_*.py")
def ids(obj):
 for x in obj:
  if isinstance(x,unittest.TestSuite):yield from ids(x)
  else:yield x.id()
names=sorted(ids(suite))
assert len(names)==len(set(names)),("duplicate tests",names)
log=io.StringIO()
r=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
(B/"TEST_RUN.log").write_text(log.getvalue())
need=["RULES.json","SOURCE_IDENTITY.json","SOURCE_IMAGE_MANIFEST.json",
      "COUNTS.json","SECTION_COVERAGE.json","UNRESOLVED.json","ERRATA_COLLATION.json",
      "AUDIT_REPORT.md","CLAIM_LEDGER.json","SOURCE_FIRST_NOTES.md"]
need+=sorted(p.name for p in B.glob("test_*.py"))
s={"batch":"B02s","tests_run":r.testsRun,"distinct_test_count":len(names),
 "discovered_test_ids":names,"successful":r.wasSuccessful(),
 "failures":len(r.failures),"errors":len(r.errors),"skipped":len(r.skipped),
 "log_sha256":hashlib.sha256(log.getvalue().encode()).hexdigest(),
 "source_file_sha256":{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in need},
 "scope":"Source-documentary and structural tests only; not empirical predictions, legal or clinical validation."}
(B/"TEST_RUN_SUMMARY.json").write_text(json.dumps(s,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({x:s[x] for x in ("tests_run","distinct_test_count","successful","failures","errors","skipped")}))
if not r.wasSuccessful():print(log.getvalue())
sys.exit(0 if r.wasSuccessful() else 1)
