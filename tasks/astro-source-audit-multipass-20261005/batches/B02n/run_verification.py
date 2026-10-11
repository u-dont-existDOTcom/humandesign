"""Portable source packet structural suite with exact test identities and replay hashes."""
from pathlib import Path
import json,hashlib,unittest,io,sys
B=Path(__file__).resolve().parent
suite=unittest.defaultTestLoader.discover(str(B),pattern='test_lilly_aphorisms.py')
def names(group):
 for item in group:
  if isinstance(item,unittest.TestSuite):yield from names(item)
  else:yield item.id()
ids=sorted(names(suite))
log=io.StringIO()
result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
out=log.getvalue()
(B/'TEST_RUN.log').write_text(out)
src=['RULES.json','COUNTS.json','APHORISM_INDEX.json','SOURCE_IDENTITY.json','SOURCE_IMAGE_MANIFEST.json','SECTION_COVERAGE.json','UNRESOLVED.json','AUDIT_REPORT.md','test_lilly_aphorisms.py']
summary={'batch':'B02n','invocation':'python3 run_verification.py','tests_run':result.testsRun,'distinct_test_count':len(set(ids)),'discovered_test_ids':ids,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'successful':result.wasSuccessful(),'log_sha256':hashlib.sha256(out.encode()).hexdigest(),'source_file_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in src},'scope':'Portable structural, explicit source-condition and replay hashes; not semantic certification, ancient authorship, medical efficacy or predictive evaluation.'}
(B/'TEST_RUN_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:summary[k] for k in ['tests_run','distinct_test_count','failures','errors','skipped','successful']}),flush=True)
if not result.wasSuccessful():print(out)
sys.exit(0 if result.wasSuccessful() else 1)
