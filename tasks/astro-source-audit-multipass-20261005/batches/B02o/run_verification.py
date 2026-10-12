"""Portable focused documentary source suite; test execution does not validate astrology."""
from pathlib import Path
import hashlib,json,unittest,io,sys
B=Path(__file__).resolve().parent
suite=unittest.defaultTestLoader.discover(str(B),pattern='test_*.py')
def collect(group):
 for x in group:
  if isinstance(x,unittest.TestSuite):yield from collect(x)
  else:yield x.id()
ids=sorted(collect(suite))
output=io.StringIO();result=unittest.TextTestRunner(stream=output,verbosity=2).run(suite)
log=output.getvalue();(B/'TEST_RUN.log').write_text(log)
names=['RULES.json','CASE_EVIDENCE.json','CHART_INSCRIPTION.json','COUNTS.json','SOURCE_IDENTITY.json','SOURCE_IMAGE_MANIFEST.json','SECTION_COVERAGE.json','UNRESOLVED.json','AUDIT_REPORT.md','CHART_GLYPH_OBSERVATIONS.json','test_lilly_sick_doctor.py','test_opus_b02o_reconciled.py']
s={'batch':'B02o','tests_run':result.testsRun,'distinct_test_count':len(set(ids)),'discovered_test_ids':ids,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'successful':result.wasSuccessful(),'log_sha256':hashlib.sha256(log.encode()).hexdigest(),'source_file_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in names},'scope':'Documentary structure, source conditions and retained byte hashes only. No source semantic certification, medical or predictive validity.'}
(B/'TEST_RUN_SUMMARY.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:s[k] for k in ['tests_run','distinct_test_count','failures','errors','skipped','successful']}))
if not result.wasSuccessful():print(log[-8000:])
sys.exit(0 if result.wasSuccessful() else 1)
