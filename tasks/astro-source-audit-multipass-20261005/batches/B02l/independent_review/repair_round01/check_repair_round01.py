from pathlib import Path
import json,hashlib
Q=Path('/workspace/scratch/43f75264c32e/b02l-workers/independent/repair_round01')
I=Q.parent
P1=Path('/workspace/scratch/43f75264c32e/review-candidate-b02l-01')
P2=Path('/workspace/scratch/43f75264c32e/review-candidate-b02l-02')
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(base,path):
 b=(base/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b)}
def objsha(o):return sha(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def save(name,o):(Q/name).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def diffs(a,b,path=''):
 if type(a)!=type(b):return [{'path':path,'before':a,'after':b}]
 if isinstance(a,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:out.append({'path':path+'/'+k,'before':a.get(k),'after':b.get(k)})
   else:out.extend(diffs(a[k],b[k],path+'/'+k))
  return out
 if isinstance(a,list):
  if len(a)!=len(b):return [{'path':path,'before':a,'after':b}]
  return [v for n,(x,y) in enumerate(zip(a,b)) for v in diffs(x,y,path+'/'+str(n))]
 return [] if a==b else [{'path':path,'before':a,'after':b}]
assert bind(P1,'CANDIDATE_MANIFEST.json')['sha256']=='41a5d97ba5c0a560c16fedbcfd24d8bd09a185b116d5d884374881f5194cbf48'
assert bind(P2,'CANDIDATE_MANIFEST.json')['sha256']=='40cbce412a7c1c6266f5fc4e55fa5570fa37ca43631ebb393e9787b96b4237f8'
m1=json.loads((P1/'CANDIDATE_MANIFEST.json').read_text());m2=json.loads((P2/'CANDIDATE_MANIFEST.json').read_text())
manifestchecks=[]
for f in m2['files']:
 got=bind(P2,f['path']);manifestchecks.append({'path':f['path'],'bytes':got['bytes'],'sha256':got['sha256'],'matches':got['bytes']==f['bytes'] and got['sha256']==f['sha256']})
assert len(manifestchecks)==45 and all(x['matches'] for x in manifestchecks)
fm1={x['path']:x for x in m1['files']};fm2={x['path']:x for x in m2['files']}
filechanges=[{'path':x,'before':fm1[x],'after':fm2[x]} for x in fm1.keys()&fm2.keys() if fm1[x]!=fm2[x]]
r1=json.loads((P1/'RULES.json').read_text());r2=json.loads((P2/'RULES.json').read_text());a={r['id']:r for r in r1['rules']};b={r['id']:r for r in r2['rules']}
assert set(a)==set(b) and len(b)==101
rec=[{'id':k,'before_normalized_sha256':objsha(a[k]),'after_normalized_sha256':objsha(b[k]),'identical_object':a[k]==b[k]} for k in a]
changedrecords=[x['id'] for x in rec if not x['identical_object']];assert changedrecords==['LI.1647.II.XLIV.R1560']
rd=diffs(a[changedrecords[0]],b[changedrecords[0]])
record=b[changedrecords[0]];f=record['source_fields']
duplicates={'title_equals_source_statement':record['title']==record['source_statement'],'source_statement_equals_proposition':record['source_statement']==f['proposition'],'prerequisites_equal_conditions':record['prerequisites'][0]['source_clauses']==f['conditions'],'qualifications_equal_uncertainties':record['qualifications_and_limits']==f['uncertainties']}
assert all(duplicates.values())
l1=json.loads((P1/'CLAIM_LEDGER.json').read_text());l2=json.loads((P2/'CLAIM_LEDGER.json').read_text());c1={x['id']:x for x in l1['items']};c2={x['id']:x for x in l2['items']}
existingchanged=[k for k in c1 if c1[k]!=c2[k]];added=sorted(set(c2)-set(c1));unchanged=[k for k in c1 if c1[k]==c2[k]]
assert existingchanged==['C08','C09','C10','C24','C35'] and added==['C42'] and len(unchanged)==36
report1=(P1/'AUDIT_REPORT.md').read_text();report2=(P2/'AUDIT_REPORT.md').read_text();bindings=[]
for k,item in c2.items():
 bindings.append({'id':k,'occurrences':report2.count(item['text']),'hash_matches':sha(item['text'].encode())==item['text_sha256'],'identical_to_initial_ledger_object':k in c1 and item==c1[k]})
assert all(x['occurrences']==1 and x['hash_matches'] for x in bindings)
assert sha((P2/'AUDIT_REPORT.md').read_bytes())==l2['report_sha256']
rem1=report1;rem2=report2
for k in existingchanged:
 rem1=rem1.replace(c1[k]['text'],'[CHANGED '+k+']');rem2=rem2.replace(c2[k]['text'],'[CHANGED '+k+']')
assert rem1==rem2
residual=report2
for item in c2.values():residual=residual.replace(item['text'],'[LEDGER '+item['id']+']')
(Q/'REPAIR_REPORT_RESIDUAL.txt').write_text(residual)
codechecks=[{'path':n,'before_sha256':bind(P1,n)['sha256'],'after_sha256':bind(P2,n)['sha256'],'identical':(P1/n).read_bytes()==(P2/n).read_bytes()} for n in ['lilly_dariot_reference.py','test_lilly_dariot.py','run_verification.py']]
assert all(x['identical'] for x in codechecks)
t1=json.loads((P1/'TEST_RUN_SUMMARY.json').read_text());t2=json.loads((P2/'TEST_RUN_SUMMARY.json').read_text())
tfiles=[{'path':x['path'],'reported_sha256':x['sha256'],'actual_sha256':bind(P2,x['path'])['sha256'],'matches':x['sha256']==bind(P2,x['path'])['sha256']} for x in t2['test_files']]
assert all(x['matches'] for x in tfiles)
assert t1['discovered_test_ids']==t2['discovered_test_ids'] and t2['tests_run']==20 and t2['distinct_test_count']==20 and t2['successful'] and not any(t2[k] for k in ['failures','errors','skipped'])
i1=json.loads((P1/'LILLY_SOURCE_EXTRACTION_INDEX_SNAPSHOT.json').read_text());i2=json.loads((P2/'LILLY_SOURCE_EXTRACTION_INDEX_SNAPSHOT.json').read_text());ixdiff=diffs(i1,i2)
assert len(ixdiff)==1 and ixdiff[0]['path'].endswith('/sha256') and ixdiff[0]['after']==bind(P2,'RULES.json')['sha256']
change=json.loads((P2/'REPAIR_ROUND01_CHANGESET.json').read_text());checks=[]
for x in change['semantic_changes']:
 k=x['id'];checks.append({'id':k,'before_matches_original':x['before']==c1.get(k),'after_matches_candidate':x['after']==c2[k]})
assert all(x['before_matches_original'] and x['after_matches_candidate'] for x in checks)
refs=[{'claim_id':'C42','evidence_file':n,'exists_in_frozen_candidate':(P2/n).is_file(),'listed_in_candidate_manifest':n in fm2} for n in c2['C42']['evidence_files']]
oldfreeze=json.loads((I/'INITIAL_DIAGNOSIS_FREEZE.json').read_text());preserve=[]
assert bind(I,'INITIAL_DIAGNOSIS_FREEZE.json')['sha256']=='25bf2ad16a7a0038d58f6584346a253693b3af0bd666a06ba58a232b99dc734c'
for x in oldfreeze['files']+oldfreeze['source_first_outputs_unchanged']:
 got=bind(I,x['path']);preserve.append({'path':x['path'],'matches':got==x})
assert all(x['matches'] for x in preserve)
out={'candidate01_manifest':bind(P1,'CANDIDATE_MANIFEST.json'),'candidate02_manifest':bind(P2,'CANDIDATE_MANIFEST.json'),'candidate02_manifest_file_checks':manifestchecks,'all45_manifest_files_match':True,'manifest_file_changes':sorted(filechanges,key=lambda x:x['path']),'manifest_files_added':sorted(set(fm2)-set(fm1)),'manifest_files_removed':sorted(set(fm1)-set(fm2)),'record_object_hashes':rec,'changed_records':changedrecords,'unchanged_records':100,'changed_record_leaf_differences':rd,'changed_record_duplicate_consistency':duplicates,'claim_bindings':bindings,'changed_existing_claims':existingchanged,'added_claims':added,'unchanged_claims':unchanged,'report_outside_changed_units_identical':True,'report_sha256':bind(P2,'AUDIT_REPORT.md')['sha256'],'ledger_sha256':bind(P2,'CLAIM_LEDGER.json')['sha256'],'changeset_before_after_checks':checks,'unchanged_helper_test_runner':codechecks,'updated_tested_file_hash_checks':tfiles,'test_result':{'tests':20,'failures':0,'errors':0,'skipped':0,'same20_test_ids':True,'new_test_identities':0,'independent_rerun_in_this_repair_round':False,'basis':'Repaired actual run receipt/log plus unchanged helper/test/runner identity and exact tested-file hashes; initial private suite execution carries forward.'},'index_differences':ixdiff,'index_records_count':i2['records_count'],'c42_evidence_reference_availability':refs,'original_freeze_checks':preserve,'scope_note':'Unchanged records and claims were compared mechanically, not reopened for a second exhaustive semantic review. Added ROOT_SOURCE_CORRECTIONS.json was hashed as a manifest file but not read as narrative.'}
save('MECHANICAL_CARRY_FORWARD.json',out)
print(json.dumps({'manifest_files_verified':len(manifestchecks),'changed_records':changedrecords,'unchanged_records':100,'record_leaf_changes':len(rd),'changed_claims':existingchanged,'added_claims':added,'unchanged_claims':len(unchanged),'code_identical':True,'test_hashes_match':True,'same20_test_ids':True,'index_differences':ixdiff,'metadata_references':refs,'prior_freezes_unchanged':True},indent=2))
