#!/usr/bin/env python3
"""Guarded original-source index append: Chapter LXI only."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03g_CHAPTER_LXI_COMPLETE.md'
OLDI=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03g_CANONICAL.json'
OLDC=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03g.md'
PREP=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json'
assert LATEST.is_file() and not any(p.exists() for p in (OLDI,OLDC,PREP))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
run=lambda *xs:subprocess.check_output(['git',*xs],cwd=ROOT,text=True).strip()
raw=I.read_bytes();j=json.loads(raw)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').read_text())
assert j['records_count']==3449 and j['batches'][-1]['id']=='B03f'
assert j['next']['chapter']=='LXI' and j['next']['pdf_page']==424
assert j['read_numbered_chapters']==list(range(1,61))
assert j['empirical_validations']==0 and j['runtime_promotions']==0
assert j['source_sha256']==A['source_pdf_sha256']
assert A['documentary_accepted_locally'] and A['new_documentary_records']==35
assert A['source_reverse_spans']==15 and A['retained_source_uncertainties']==16
assert R['record_count']==35 and R['independently_authenticated_servant_outcomes']==0
assert R['claim_one_or_two_days_not_scoreable_without_question_date']
assert [r['record_number'] for r in R['rules']]==list(range(3450,3485))
assert R['rules'][-1]['chapter']=='LXII_NAVIGATION_ONLY'
assert Z['zip_crc_pass'] and Z['member_sha256_pass'] and Z['actual_extraction_pass']
assert Z['extracted_source_tests_passed']==21 and Z['extracted_test_exit_code']==0
assert sha(Z['owner_designated_download_path'])==Z['archive_sha256']
assert sha(B/'RULES.json')==A['rules_sha256']==Z['source_rules_sha256']
index_path=str(I.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',index_path],cwd=ROOT).returncode==0
oldblob=run('rev-parse','HEAD:'+index_path)
assert oldblob==run('hash-object',str(I))
assert not any(b['id']=='B03g' for b in j['batches'])
j['batches'].append({
 'id':'B03g','path':'batches/B03g/RULES.json',
 'records_count':35,'sha256':A['rules_sha256'],
 'scope':'Lilly 1647 Book II Chapter LXI original fugitive-servant worked case PDF424 after LX divider to PDF426 before LXII divider. 34 source notes plus LXII navigation marker, 15 image passages, 16 unresolved issues; reported Friday return and conditional Kingston claim are not independently verified.'})
j['records_count']=3484
j['read_numbered_chapters'].append(61)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LXI_DOCUMENTARY_SOURCE_ONLY_NEXT_LXII_OPEN'
j['next']={'pdf_page':426,'printed_page':392,'chapter':'LXII',
 'heading':'A Dogge missing, where?',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF426 BELOW divider after LXI servant account; separate dog figure and its interpretation extend to PDF428 ABOVE LXIII divider.'}
j['chapter_LXI_source_acceptance_note']='35 historical source annotations including one LXII heading; 15 mapped original passages and 16 preserved uncertainties. Source-internal Friday return and conditional Kingston claim not independently documented; question date and one/two-day forecast timing unscored.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03g_CHAPTER_LXI_COMPLETE.md'
assert j['records_count']==sum(x['records_count'] for x in j['batches'])==3484
assert j['read_numbered_chapters']==list(range(1,62))
prefix="""# Latest original astrology source audit — Chapter LXI

Current (2026-10-15): Lilly Book II Chapter LXI, a worked fugitive-servant case, accepted as 35 historical documentary units. Lilly 3,484 + retained Ptolemy 1,066 = 4,550 combined after authenticated publication. Next: Chapter LXII missing dog on original PDF426/printed392 BELOW divider. Independent predictive validations added: zero; runtime promotions: zero. Source, ZIP and acceptance checkpoint: state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03g_CHAPTER_LXI_COMPLETE.md and B03g source receipts.

---

"""
OLDI.parent.mkdir(parents=True,exist_ok=True)
OLDI.write_bytes(raw)
OLDC.write_bytes(CUR.read_bytes())
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CUR.write_text(prefix+OLDC.read_text(encoding='utf-8'),encoding='utf-8')
receipt={
 'batch':'B03g',
 'kind':'SOURCE_INDEX_PREPARED_NOT_REMOTE_PUBLISHED',
 'previous_index_git_blob_sha1':oldblob,
 'old_index_sha256':sha(OLDI),
 'new_index_sha256':sha(I),
 'new_current_state_sha256':sha(CUR),
 'new_latest_source_state_sha256':sha(LATEST),
 'rules_sha256':A['rules_sha256'],
 'owner_release_zip_sha256':Z['archive_sha256'],
 'new_documentary_units':35,
 'lilly_if_published':3484,
 'ptolemy_retained':1066,
 'combined_if_published':4550,
 'next_chapter':'LXII',
 'next_original_pdf':426,
 'independently_verified_case_outcomes':0,
 'empirically_validated_predictions':0,
 'runtime_promotions':0,
 'remotely_published':False
}
PREP.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
