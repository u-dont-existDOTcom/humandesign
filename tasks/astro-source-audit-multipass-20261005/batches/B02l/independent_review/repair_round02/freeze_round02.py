from pathlib import Path
import json,hashlib,datetime
Q=Path('/workspace/scratch/43f75264c32e/b02l-workers/independent/repair_round02');I=Q.parent
P2=Path('/workspace/scratch/43f75264c32e/review-candidate-b02l-02');P3=Path('/workspace/scratch/43f75264c32e/review-candidate-b02l-03')
def bind(base,path):
 b=(base/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(name,o):(Q/name).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
assert bind(P2,'CANDIDATE_MANIFEST.json')['sha256']=='40cbce412a7c1c6266f5fc4e55fa5570fa37ca43631ebb393e9787b96b4237f8'
assert bind(P3,'CANDIDATE_MANIFEST.json')['sha256']=='73955bbb3cd06723d3553f119b61faef6c490547edd058638f369cb4e36a9183'
m2=json.loads((P2/'CANDIDATE_MANIFEST.json').read_text());m3=json.loads((P3/'CANDIDATE_MANIFEST.json').read_text());f2={x['path']:x for x in m2['files']};f3={x['path']:x for x in m3['files']}
filechecks=[]
for f in m3['files']:
 got=bind(P3,f['path']);filechecks.append({**got,'matches_manifest':got['bytes']==f['bytes'] and got['sha256']==f['sha256']})
assert len(filechecks)==47 and all(x['matches_manifest'] for x in filechecks)
priorchecks=[{'path':n,'before':bind(P2,n),'after':bind(P3,n),'bytes_identical':(P2/n).read_bytes()==(P3/n).read_bytes()} for n in f2]
changed=[x['path'] for x in priorchecks if not x['bytes_identical']];added=sorted(set(f3)-set(f2));assert changed==['CLAIM_LEDGER.json'] and added==['BOOTSTRAP_RECEIPT.json','TASK_ENVELOPE.json'] and not(set(f2)-set(f3))
l2=json.loads((P2/'CLAIM_LEDGER.json').read_text());l3=json.loads((P3/'CLAIM_LEDGER.json').read_text());a={x['id']:x for x in l2['items']};b={x['id']:x for x in l3['items']};assert len(a)==len(b)==42 and set(a)==set(b)
assert all(a[k]['text']==b[k]['text'] and a[k]['text_sha256']==b[k]['text_sha256'] for k in a)
for k in a:
 left=json.loads(json.dumps(a[k]));right=json.loads(json.dumps(b[k]))
 if k=='C42':left.pop('evidence_files');right.pop('evidence_files')
 assert left==right,k
left=json.loads(json.dumps(l2));right=json.loads(json.dumps(l3));left['items'][-1]['evidence_files']=right['items'][-1]['evidence_files'];assert left==right
assert b['C42']['evidence_files']==['SECTION_COVERAGE.json','TASK_ENVELOPE.json','BOOTSTRAP_RECEIPT.json']
metadata={'TASK_ENVELOPE.json':{'task_id':json.loads((P3/'TASK_ENVELOPE.json').read_text())['task_id']},'BOOTSTRAP_RECEIPT.json':{'task_start':json.loads((P3/'BOOTSTRAP_RECEIPT.json').read_text())['task_start']}}
assert metadata['TASK_ENVELOPE.json']['task_id'].endswith(':B02l')
assert metadata['BOOTSTRAP_RECEIPT.json']['task_start']=='2026-10-10T19:24:34+00:00'
byline_date=datetime.datetime.fromisoformat(metadata['BOOTSTRAP_RECEIPT.json']['task_start']).strftime('%d %B %Y');assert byline_date=='10 October 2026' and byline_date in b['C42']['text']
refs=[{**bind(P3,n),'available':(P3/n).is_file(),'manifest_bound':n in f3} for n in b['C42']['evidence_files']];assert all(x['available'] and x['manifest_bound'] for x in refs)
assert (P2/'AUDIT_REPORT.md').read_bytes()==(P3/'AUDIT_REPORT.md').read_bytes()
assert (P2/'RULES.json').read_bytes()==(P3/'RULES.json').read_bytes()
rules=json.loads((P3/'RULES.json').read_text());assert len(rules['rules'])==101
report=(P3/'AUDIT_REPORT.md').read_text();assert hashlib.sha256((P3/'AUDIT_REPORT.md').read_bytes()).hexdigest()==l3['report_sha256']
claimbindings=[{'id':k,'text_unchanged':a[k]['text']==b[k]['text'],'text_hash_unchanged':a[k]['text_sha256']==b[k]['text_sha256'],'unique_report_occurrence':report.count(b[k]['text'])==1} for k in b];assert all(x['unique_report_occurrence'] for x in claimbindings)
for n in ['lilly_dariot_reference.py','test_lilly_dariot.py','run_verification.py','TEST_RUN_SUMMARY.json','TEST_RUN.log','LILLY_SOURCE_EXTRACTION_INDEX_SNAPSHOT.json']:
 assert (P2/n).read_bytes()==(P3/n).read_bytes()
t=json.loads((P3/'TEST_RUN_SUMMARY.json').read_text());assert t['tests_run']==t['distinct_test_count']==20 and t['successful']
assert all(bind(P3,x['path'])['sha256']==x['sha256'] for x in t['test_files'])
previousfreezes=[bind(I,'INITIAL_DIAGNOSIS_FREEZE.json'),bind(I/'repair_round01','REPAIR_ROUND01_FREEZE.json')]
assert previousfreezes[0]['sha256']=='25bf2ad16a7a0038d58f6584346a253693b3af0bd666a06ba58a232b99dc734c'
assert previousfreezes[1]['sha256']=='510c032cedc675b412e3be3a07a62129a1734ac72dbff1d478bcf93107147503'
mechanical={'candidate02_manifest':bind(P2,'CANDIDATE_MANIFEST.json'),'candidate03_manifest':bind(P3,'CANDIDATE_MANIFEST.json'),'manifest_checks':filechecks,'all47_manifest_entries_match':True,'prior45_file_comparisons':priorchecks,'only_changed_prior_file':changed,'newly_included_files':added,'only_prior_content_change':{'item':'C42','field':'evidence_files','before':a['C42']['evidence_files'],'after':b['C42']['evidence_files']},'c42_reference_availability_and_binding':refs,'metadata_fields_read':metadata,'task_start_matches_provided_task_metadata':True,'derived_byline_date':byline_date,'date_matches_unchanged_byline':True,'all42_claim_text_bindings':claimbindings,'all101_records_byte_identical':True,'report_prose_byte_identical':True,'helper_test_runner_test_receipt_and_tested_data_unchanged':True,'all_tested_file_hashes_match':True,'test_suite_rerun_this_round':False,'canonical_distinct_tests':20,'new_test_identities':0,'prior_freeze_bindings':previousfreezes,'scope_limit':'Metadata reference availability/date plus mechanical carry-forward only. No source semantics, unchanged bootstrap process claims or previous passed checks were reopened.'}
save('ROUND02_REFERENCE_AND_CARRY_FORWARD.json',mechanical)
result={'stage':'second and final changed-item repair round','target':'RR1-01 only','candidate_manifest':bind(P3,'CANDIDATE_MANIFEST.json'),'disposition':'RR1-01 RESOLVED','basis':'TASK_ENVELOPE.json and BOOTSTRAP_RECEIPT.json are present and included in the47-file manifest. C42 cites both plus the already available SECTION_COVERAGE.json. The task_id identifies B02l; bootstrap task_start 2026-10-10T19:24:34+00:00 supplies the unchanged10 October2026 byline date.','acceptance_recommendation':'Recommend accepting the repaired candidate within the agreed source/claim diagnostic scope, carrying forward the initial and round-one evidence and limitations. No remaining required correction was identified in that scope. Root retains final adjudication.','final_coverage':{'source_first_units':92,'canonical_records':101,'report_ledger_units':42,'table_data_rows':25,'initial_source_corrections_IF01_through_IF06':'Resolved in round1; unchanged in round2.','MC01_metadata_text_binding':'Resolved in round1; unchanged in round2.','RR1_01_metadata_evidence_reference':'Resolved in round2.','remaining_required_corrections':0,'canonical_distinct_tests':20,'new_test_identities_in_repairs':0,'test_suite_reruns_in_this_round':0},'preserved_limits':['SC-01 and SC-02 remain disclosed reviewer source-first corrections; corresponding candidate readings remain correct.','IC-01 remains a nonunique contextual interpretation, not a newly resolved source issue.','Original source-first freeze, initial diagnosis and round-one freeze remain unchanged.','Same-family contextual diagnostic review; no cross-family, expert, clinical, IV&V or empirical accuracy claim.'],'method':'Read task_id and task_start metadata fields only; unrelated bootstrap claims were not evaluated. Verified all manifest hashes and mechanical identity of carried-forward records, texts, code, tested data and receipts. No source-semantic reread or suite rerun.','time_policy':'Date derived from the stored task_start metadata, not a current-clock read. No completion time fabricated.','authority':'Root retains final acceptance. This was the second and last changed-item round under the original policy; no new gate is proposed.','write_scope':str(Q),'candidate_mutations':False,'semantic_result_released_before_freeze':False}
save('ROUND02_FINAL_RESULT.json',result)
md='''# B02l repair round 2 — final bounded result

**RR1-01 is resolved. Recommend accepting candidate03 within the agreed source/claim diagnostic scope.** No remaining required correction was identified in that scope. Root retains final adjudication.

The previously unavailable `TASK_ENVELOPE.json` is now present and manifest-bound. C42 also cites the newly included, manifest-bound `BOOTSTRAP_RECEIPT.json`. Its stored `task_start` is **2026-10-10T19:24:34+00:00**, supplying the unchanged **10 October 2026** byline date. The task-envelope `task_id` identifies the B02l batch. All three C42 evidence references, including `SECTION_COVERAGE.json`, resolve inside the frozen candidate.

## Mechanical carry-forward

- All **47** manifest-listed files match their hashes and byte counts.
- Of the prior 45 files, **44 are byte-identical**. Only `CLAIM_LEDGER.json` changed, solely in **C42.evidence_files**, adding the bootstrap receipt reference.
- All **42 claim texts**, their text hashes, and the complete report prose are unchanged. Every bound text still occurs exactly once.
- All **101 records** are byte-identical as part of unchanged `RULES.json`.
- Helper, test module, runner, tested data, current index, actual test summary and actual test log are unchanged. Their tested-file hashes remain consistent.
- The canonical suite remains **20 distinct tests**. No suite rerun or new test identity was introduced in this round.

The completed review coverage remains **92 source-first units, 101 records, 42 ledger units and 25 table data rows**. IF-01 through IF-06 and MC-01 were resolved in round1 and carry forward unchanged. This round resolves the remaining metadata-reference issue only.

## Scope and preserved limitations

Only the task-envelope identifier and bootstrap task-start metadata were read for the reference check. Unrelated bootstrap process claims were not evaluated. No source interpretation, unchanged content or prior passed check was reopened. The date was derived from stored metadata; no current-clock read or completion timestamp was used.

The original source-first and initial-diagnosis freezes and the round-one freeze remain unchanged. SC-01 and SC-02 remain disclosed corrections to the reviewer’s initial readings. IC-01 remains the previously noted nonunique contextual interpretation. This is same-family contextual diagnostic review, not clinical, cross-family, expert, IV&V or empirical validation.

This is the **second and last** changed-item round under the original policy. No new gate or further review is proposed. Root retains final adjudication.

## Artifacts

- `ROUND02_FINAL_RESULT.json`: final disposition, coverage and recommendation.
- `ROUND02_REFERENCE_AND_CARRY_FORWARD.json`: all manifest, reference, metadata and identity checks.
- `ROUND02_FREEZE.json`: exact hashes and byte counts binding this result.
'''
(Q/'ROUND02_FINAL_RESULT.md').write_text(md)
paths=['ROUND02_FINAL_RESULT.md','ROUND02_FINAL_RESULT.json','ROUND02_REFERENCE_AND_CARRY_FORWARD.json','freeze_round02.py']
freeze={'stage':'second and final changed-item repair round','candidate_manifest':bind(P3,'CANDIDATE_MANIFEST.json'),'previous_freezes':previousfreezes,'files':[bind(Q,n) for n in paths],'result':'RR1-01 resolved; no remaining required correction within agreed scope; recommend acceptance subject to root final adjudication.','final_counts':{'source_units':92,'records':101,'ledger_units':42,'table_rows':25,'canonical_distinct_tests':20,'new_tests':0},'no_source_semantics_reopened':True,'no_test_suite_rerun':True,'semantic_result_sent_before_this_freeze':False,'time_policy':'No completion timestamp asserted; no current-clock read.','policy':'Second and final repair round; no new gate.'}
save('ROUND02_FREEZE.json',freeze)
for f in freeze['files']:assert bind(Q,f['path'])==f
print(json.dumps({'freeze':bind(Q,'ROUND02_FREEZE.json'),'main_artifacts':[bind(Q,n) for n in paths[:3]],'result':'RR1-01 resolved','remaining_required_corrections':0},indent=2))
