#!/usr/bin/env python3
"""Guarded original-source index transition: Lilly Chapter LXII."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03h_CHAPTER_LXII_COMPLETE.md'
OLDI=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03h_CANONICAL.json'
OLDC=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03h.md'
REC=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json'
assert LATEST.is_file() and not any(p.exists() for p in (OLDI,OLDC,REC))
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
run=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
raw=I.read_bytes();j=json.loads(raw)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').read_text())
assert j['records_count']==3484 and j['batches'][-1]['id']=='B03g'
assert j['next']['chapter']=='LXII' and j['next']['pdf_page']==426
assert j['read_numbered_chapters']==list(range(1,62))
assert j['empirical_validations']==j['runtime_promotions']==0
assert j['source_sha256']==A['source_full_pdf_sha256']
assert A['documentary_accepted_locally'] and A['added_documentary_records']==43
assert A['source_reverse_passages']==14 and A['unresolved_source_issues']==17
assert R['record_count']==43 and R['independently_verified_dog_returns']==0
assert [r['record_number'] for r in R['rules']]==list(range(3485,3528))
assert R['rules'][-1]['chapter']=='LXIII_BOUNDARY_ONLY'
assert Z['zip_crc_pass'] and Z['members_sha256_pass']
assert Z['extracted_test_count']==17 and Z['extracted_test_exit_code']==0
assert sha(Z['download_path'])==Z['zip_sha256']
assert sha(B/'RULES.json')==A['rules_sha256']==Z['rules_sha256']
rpath=str(I.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rpath],cwd=ROOT).returncode==0
oldblob=run('rev-parse','HEAD:'+rpath)
assert oldblob==run('hash-object',str(I))
assert not any(b['id']=='B03h' for b in j['batches'])
j['batches'].append({'id':'B03h','path':'batches/B03h/RULES.json',
 'records_count':43,'sha256':A['rules_sha256'],
 'scope':'Lilly original 1647 Chapter LXII missing dog worked case, PDF426 below LXI divider to PDF428 above LXIII divider; 42 LXII source annotations plus next heading, 14 mapped spans, 17 unresolved issues; dog recovery claimed by same author, upper-room forecast not established.'})
j['records_count']=3527
j['read_numbered_chapters'].append(62)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LXII_DOCUMENTARY_SOURCE_ONLY_NEXT_LXIII_OPEN'
j['next']={'pdf_page':428,'printed_page':394,'chapter':'LXIII',
 'heading':'Of Theft.','include_opening_paragraph':True,
 'extracted':False,'boundary_image_read':True,
 'position':'Original PDF428 below horizontal divider; all post-divider theft text excluded from LXII.'}
j['chapter_LXII_source_acceptance_note']='43 historical documentary units including LXIII navigation, 14 source passages, 17 source issues. Author-reported Monday dog recovery and Long-acre finding are not independent validation; floor/upper-room prediction unresolved. Unnumbered fugitive maxims preserved before LXIII divider.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03h_CHAPTER_LXII_COMPLETE.md'
assert j['records_count']==sum(x['records_count'] for x in j['batches'])==3527
assert j['read_numbered_chapters']==list(range(1,63))
prefix="""# Current astrology source audit — Chapter LXII original documentary checkpoint

CURRENT 2026-10-15: Lilly Chapter LXII (missing dog) original documentary source intake accepted, cumulative 3,527 Lilly + 1,066 Ptolemy = 4,593 source records after authenticated research-branch publication. Next Chapter LXIII Theft starts PDF428/printed394 BELOW divider. No empirical prediction confirmations, no model/runtime promotions. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03h_CHAPTER_LXII_COMPLETE.md and B03h source, acceptance and publication receipts.

---

"""
OLDI.parent.mkdir(parents=True,exist_ok=True)
OLDI.write_bytes(raw)
OLDC.write_bytes(CUR.read_bytes())
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
CUR.write_text(prefix+OLDC.read_text())
rec={'batch':'B03h','status':'GUARDED_CANONICAL_SOURCE_INDEX_PREPARED_NOT_REMOTE_PUBLISHED',
 'previous_index_git_blob_sha1':oldblob,'old_index_sha256':sha(OLDI),
 'new_index_sha256':sha(I),'new_current_sha256':sha(CUR),
 'new_latest_sha256':sha(LATEST),'rules_sha256':A['rules_sha256'],
 'source_zip_sha256':Z['zip_sha256'],'new_documentary_records':43,
 'lilly_if_published':3527,'retained_ptolemy':1066,'combined_if_published':4593,
 'empirical_predictions_validated':0,'runtime_promotions':0,
 'next_chapter':'LXIII','next_pdf':428,'remote_published':False}
REC.write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2))
