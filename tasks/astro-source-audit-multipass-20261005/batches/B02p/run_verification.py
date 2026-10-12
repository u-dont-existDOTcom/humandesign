from pathlib import Path
import json,hashlib,unittest,io,sys
B=Path(__file__).resolve().parent
suite=unittest.defaultTestLoader.discover(str(B),pattern='test_*.py')
def ids(s):
 for x in s:
  if isinstance(x,unittest.TestSuite):yield from ids(x)
  else:yield x.id()
allids=sorted(ids(suite)); log=io.StringIO()
res=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
msg=log.getvalue();(B/'TEST_RUN.log').write_text(msg)
sources=['RULES.json','COUNTS.json','CASE_EVIDENCE.json','CHART_INSCRIPTION.json','SOURCE_IDENTITY.json','SOURCE_IMAGE_MANIFEST.json','SECTION_COVERAGE.json','UNRESOLVED.json','AUDIT_REPORT.md','test_lilly_xlvi.py']
summary={'batch':'B02p','distinct_test_count':len(set(allids)),'tests_run':res.testsRun,'discovered_test_ids':allids,'failures':len(res.failures),'errors':len(res.errors),'skipped':len(res.skipped),'successful':res.wasSuccessful(),'log_sha256':hashlib.sha256(msg.encode()).hexdigest(),'source_file_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in sources},'scope':'Structural and source-condition regression only, not astrology/medicine predictive validation.'}
(B/'TEST_RUN_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:summary[k] for k in ['distinct_test_count','tests_run','failures','errors','skipped','successful']}))
if not res.wasSuccessful():print(msg)
sys.exit(0 if res.wasSuccessful() else 1)
