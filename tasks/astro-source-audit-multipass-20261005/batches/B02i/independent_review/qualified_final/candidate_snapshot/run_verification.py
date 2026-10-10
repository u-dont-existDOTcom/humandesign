"""Run the declared focused suites and preserve actual receipts, without scoring predictions."""
from pathlib import Path
import hashlib
import argparse
import json
import os
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
PREFIX='tasks/astro-source-audit-multipass-20261005/batches/'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only')
    parser.add_argument('--pytest-deps',type=Path)
    args=parser.parse_args()
    suites=[
        ('B02i',['python3','-B','-m','unittest','discover','-s',PREFIX+'B02i','-p','test_*.py','-v']),
        ('retained_B02h',['python3','-B','-m','unittest','discover','-s',PREFIX+'B02h','-p','test_*.py','-v']),
        ('retained_B02f',['python3','-B','-m','unittest','discover','-s',PREFIX+'B02f','-p','test_*.py','-v']),
        ('retained_methodology',['python3','-B','-m','pytest','-q','tests/test_astrology_deep_analysis_protocol.py','tests/test_astrology_receipt_v2.py']),
    ]
    previous=json.loads((ROOT/'TEST_RUN_SUMMARY.json').read_text()) if (ROOT/'TEST_RUN_SUMMARY.json').exists() else {'runs':[]}
    retained={r['suite']:r for r in previous['runs']}
    runs=[]
    for name,command in suites:
        if args.only and name!=args.only:
            if name not in retained: raise ValueError('No actual retained run for '+name)
            runs.append(retained[name]);continue
        environment=os.environ.copy()
        if name=='retained_methodology' and args.pytest_deps:
            environment['PYTHONPATH']=str(args.pytest_deps)+(os.pathsep+environment['PYTHONPATH'] if environment.get('PYTHONPATH') else '')
        process=subprocess.run(command,cwd=REPO,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=environment)
        output=process.stdout; match=re.search(r'Ran (\d+) tests?',output) or re.search(r'(\d+) passed',output)
        count=int(match.group(1)) if match else None
        path=ROOT/f'TEST_{name}.txt'
        dependency_note='\nPytest dependencies: '+str(args.pytest_deps) if name=='retained_methodology' and args.pytest_deps else ''
        path.write_text('Command: '+repr(command)+dependency_note+'\nExit code: '+str(process.returncode)+'\n'+output)
        runs.append({'suite':name,'distinct_tests':count,'exit_code':process.returncode,'log':path.name,
                     'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    success=all(r['exit_code']==0 and r['distinct_tests'] is not None for r in runs)
    summary={'status':'PASS' if success else 'FAIL','runs':runs,'new_distinct_tests':runs[0]['distinct_tests'],
        'retained_distinct_tests':sum(r['distinct_tests'] or 0 for r in runs[1:]),
        'total_distinct_tests':sum(r['distinct_tests'] or 0 for r in runs),
        'subtests_or_reruns_counted_as_additional':False,
        'scope':'Source/data integrity, deterministic context lookups and static arithmetic; no predictive validation.',
        'methodology_scope_note':'Only general protocol and synthetic receipt suites run; participant catalog/index suites are not needed for this source batch.'}
    (ROOT/'TEST_RUN_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))
    sys.exit(0 if success else 1)


if __name__=='__main__': main()
