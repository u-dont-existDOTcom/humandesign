"""Standalone standard-library test runner; report the actual discovered identities."""
from pathlib import Path
import hashlib,io,json,sys,unittest
ROOT=Path(__file__).resolve().parent
suite=unittest.defaultTestLoader.discover(str(ROOT),pattern='test_lilly_hermes.py')
def walk(x):
    for y in x:
        if isinstance(y,unittest.TestSuite):yield from walk(y)
        else:yield y.id()
ids=sorted(walk(suite))
log=io.StringIO()
result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
text=log.getvalue()
(ROOT/'TEST_RUN.log').write_text(text)
summary={'batch':'B02m','command':'python run_verification.py',
 'discovered_test_ids':ids,'distinct_test_count':len(set(ids)),
 'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
 'skipped':len(result.skipped),'successful':result.wasSuccessful(),
 'log_sha256':hashlib.sha256(text.encode()).hexdigest(),
 'source_hashes':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['RULES.json','COUNTS.json','REFERENCE_TABLES.json','MATERIA_MEDICA_TABLES.json','SECTION_COVERAGE.json','SOURCE_IMAGE_MANIFEST.json','UNRESOLVED.json']},
 'scope':'Source data and portable hash integrity only; no source semantic certification, medical efficacy or predictive evaluation.'}
(ROOT/'TEST_RUN_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k in ['tests_run','distinct_test_count','failures','errors','skipped','successful']}))
sys.exit(0 if result.wasSuccessful() else 1)
