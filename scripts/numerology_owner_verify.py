#!/usr/bin/env python3
"""Acceptance for the scoped owner-development result, not predictive validation."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
BASE='experiments/numerology/owner_comparison_20261004/'
REQUIRED=['manifest.json','OWNER_COMPARISON_REPORT.md','LAYER_COVERAGE_AND_SOURCE_NOTES.md','core_charts.json','event_feature_comparison.json','coarse_adapter_combinations.json','posthoc_context_checks.json','transparency_controls.json','ancillary_chart_context.json','REVIEW.md','review_receipt.json']


def main():
 errors=[]
 lock=json.loads((ROOT/'tasks/ACTIVE-TASK.json').read_text())
 branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
 if lock.get('taskId')!='NUMEROLOGY-OWNER-COMPARISON-20261004' or branch!='research/six-rule-life-timing-20261001':errors.append('TASK_OR_BRANCH_MISMATCH')
 for f in REQUIRED:
  if not (ROOT/BASE/f).is_file():errors.append('MISSING:'+f)
 if not errors:
  review=json.loads((ROOT/BASE/'review_receipt.json').read_text())
  if review.get('status') not in ['CHECKED_WITH_RECONCILIATION','CHECKED_NO_MATERIAL_FINDINGS','UNAVAILABLE_SCOPED'] or review.get('unresolved_blocking_findings')!=[]:errors.append('REVIEW_DISPOSITION_INCOMPLETE')
  if review.get('full_author_predictive_superiority_established') is not False:errors.append('SUPERIORITY_OVERCLAIM')
  if review.get('full_primary_corpus_reviewed') is not False:errors.append('REVIEW_SCOPE_OVERCLAIM')
  d=json.loads((ROOT/BASE/'coarse_adapter_combinations.json').read_text());t=json.loads((ROOT/BASE/'transparency_controls.json').read_text())
  if len(d['results'])!=36 or not d['unlabelled_years_are_unknown'] or t['distinct_flag_sets']!=22:errors.append('SCREEN_SCOPE_CHANGED')
 results=[]
 for pattern in ['test_numerology_owner*.py','test_numerology_book_*.py']:
  p=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p',pattern],cwd=ROOT,capture_output=True,text=True)
  results.append({'pattern':pattern,'status':'PASS' if p.returncode==0 else 'FAIL','output':(p.stdout+p.stderr).strip()})
  if p.returncode:errors.append('TEST_FAILURE:'+pattern)
 report={'task_id':'NUMEROLOGY-OWNER-COMPARISON-20261004','status':'FAIL' if errors else 'PASS','head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'findings':errors,'tests':results,'files_sha256':{BASE+f:hashlib.sha256((ROOT/BASE/f).read_bytes()).hexdigest() for f in REQUIRED if (ROOT/BASE/f).is_file()},'accepted_scope':'Reproducible retrospective arithmetic, declared limited combination tests, reconciled contextual report and explicit evidence limits.','full_five_author_forecast_comparison_complete':False,'predictive_validation':False,'unknown_years_are_negatives':False,'external_actions':'No merge/deployment/trial authorized or claimed.'}
 print(json.dumps(report,indent=2));return bool(errors)

if __name__=='__main__':sys.exit(main())
