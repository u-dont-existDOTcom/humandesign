"""One deterministic source-first B02u regression runner with unique identities."""
from pathlib import Path
import unittest,json,io,hashlib,sys
B=Path(__file__).resolve().parent
suite=unittest.defaultTestLoader.discover(str(B),pattern="test_*.py")
def identities(s):
 for x in s:
  if isinstance(x,unittest.TestSuite):yield from identities(x)
  else:yield x.id()
ids=sorted(identities(suite))
assert ids and len(ids)==len(set(ids))
log=io.StringIO()
res=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
(B/"TEST_RUN.log").write_text(log.getvalue())
needed=["RULES.json","DRAFT_CONSOLIDATED.json","SOURCE_IDENTITY.json",
"SOURCE_IMAGE_MANIFEST.json","SOURCE_REPLAY_RECEIPT.json",
"SECTION_COVERAGE.json","SECTION_COVERAGE_DETAILED.json","COUNTS.json",
"UNRESOLVED.json","ERRATA_COLLATION.json",
"READER_OVERLAP_AUDIT.json","OVERLAP_ADJUDICATION.json",
"NEXT_PHASE_PDF381_BOUNDARY_EXCEPTION.json","TABLE_WITNESS_REGISTER.json",
"RETAINED_LILLY_INDEX_BEFORE.json","AUDIT_REPORT.md","CLAIM_LEDGER.json"]+sorted(p.name for p in B.glob("test_*.py"))
report={"batch":"B02u","successful":res.wasSuccessful(),"tests_run":res.testsRun,
        "distinct_test_count":len(ids),"test_ids":ids,"errors":len(res.errors),"failures":len(res.failures),
        "skipped":len(res.skipped),"test_log_sha256":hashlib.sha256(log.getvalue().encode()).hexdigest(),
        "source_file_sha256":{name:hashlib.sha256((B/name).read_bytes()).hexdigest() for name in needed},
        "scope":"Historical documentary regressions, not proof of crime/gender/behavior or astrology validity."}
(B/"TEST_RUN_SUMMARY.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({k:report[k] for k in ("successful","tests_run","distinct_test_count","failures","errors","skipped")}))
if not res.wasSuccessful():print(log.getvalue())
sys.exit(0 if res.wasSuccessful() else 1)
