"""Run the bounded B02j suite and record actual process evidence."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

HERE=Path(__file__).resolve().parent
args=[sys.executable,'-m','unittest','-v','test_lilly_fifth_house']
run=subprocess.run(args,cwd=HERE,capture_output=True,text=True)
log=run.stdout+run.stderr
(HERE/'TEST_B02j.txt').write_text(log)
match=re.search(r'Ran (\d+) tests?',log)
files=['RULES.json','UNRESOLVED.json','SECTION_COVERAGE.json','WORKED_NUMERIC_TABLES.json','HISTORICAL_CASES.json','lilly_fifth_house_reference.py','test_lilly_fifth_house.py']
receipt={'batch':'B02j','command':['python3','-m','unittest','-v','test_lilly_fifth_house'],'actual_process_exit_code':run.returncode,'tests_run':int(match.group(1)) if match else None,'result':'PASS' if run.returncode==0 and match else 'FAIL','tested_files':[{ 'file':f,'sha256':hashlib.sha256((HERE/f).read_bytes()).hexdigest()} for f in files],'scope':'Data integrity and bounded source arithmetic only. No app/runtime/ephemeris/clinical/predictive validation.','retained_test_count_claimed':0,'log':'TEST_B02j.txt','log_sha256':hashlib.sha256(log.encode()).hexdigest()}
(HERE/'TEST_RUN_SUMMARY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(log)
print(json.dumps({k:v for k,v in receipt.items() if k not in ['tested_files']},indent=2))
sys.exit(run.returncode)
