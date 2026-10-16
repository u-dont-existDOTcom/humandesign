#!/usr/bin/env python3
"""Verify already-mutated local index after final receipt interrupted; never replay mutation."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CURRENT=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03u_CHAPTER_LXXV_COMPLETE.md'
PRIOR=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03u_CANONICAL.json'
PRIOR_STATE=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03u.md'
REC=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json'
assert not REC.exists(),'Never rewrite existing receipt'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *x:subprocess.check_output(['git',*x],cwd=ROOT,text=True).strip()
previous=json.loads(PRIOR.read_text());current=json.loads(IDX.read_text())
R=json.loads((B/'RULES.json').read_text())
A=json.loads((B/'ACCEPTANCE.json').read_text())
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').read_text())
assert previous['records_count']==4323 and previous['batches'][-1]['id']=='B03t'
assert current['records_count']==4384 and current['batches'][-1]['id']=='B03u'
assert current['next']['chapter']=='LXXVI' and current['next']['pdf_page']==466
assert current['read_numbered_chapters']==list(range(1,76))
assert sum(v['records_count'] for v in current['batches'])==4384
assert current['source_sha256']==previous['source_sha256']
assert current['empirical_validations']==current['runtime_promotions']==0
assert len(current['batches'])==len(previous['batches'])+1
assert current['batches'][:-1]==previous['batches']
assert [r['record_number'] for r in R['rules']]==list(range(4324,4385))
assert current['batches'][-1]['sha256']==A['rules_sha256']==sha(B/'RULES.json')
assert [i['printed_page_numerals_as_physically_imprinted'][0]
        for i in R['rules'] if i['source_local_id'] in ('LXXV-C001','LXXV-C023','LXXV-C042','LXXV-C061')]!=[]
assert A['original_pdf_text_order']==[463,464,465,466]
assert A['original_imprinted_folio_numbers']==[429,431,430,432]
assert (CURRENT.read_text()).startswith('# Current original astrology source study: Chapter LXXV')
assert LATEST.read_text().startswith('# Original William Lilly Chapter LXXV')
assert PRIOR_STATE.is_file()
assert Z['zip_crc_pass'] and Z['every_member_sha256_and_size_match'] and Z['actual_extraction_pass']
assert Z['extracted_source_tests_passed']==20 and Z['extracted_test_exit_code']==0
assert sha(Z['owner_download_path'])==Z['archive_sha256']
rel=str(IDX.relative_to(ROOT))
oldblob=git('rev-parse','HEAD:'+rel)
assert oldblob==git('hash-object',str(PRIOR))
receipt={'batch':'B03u','status':'GUARDED_ORIGINAL_HISTORICAL_SOURCE_INDEX_RECOVERED_AND_VERIFIED',
 'previous_index_git_blob_sha1':oldblob,
 'previous_index_sha256':sha(PRIOR),'new_index_sha256':sha(IDX),
 'new_current_state_sha256':sha(CURRENT),'new_latest_state_sha256':sha(LATEST),
 'accepted_rules_sha256':A['rules_sha256'],
 'owner_release_archive_sha256':Z['archive_sha256'],
 'new_original_documentary_records':61,
 'lilly_if_published':4384,'retained_ptolemy':1066,'combined_if_published':5450,
 'original_scan_order':[463,464,465,466],
 'literal_printed_folio_numbers':[429,431,430,432],
 'next_chapter':'LXXVI','next_pdf_page':466,
 'independent_empirical_astrology_validations':0,'runtime_promotions':0,
 'remote_published':False,
 'recovered_after':'initial index preparation completed but receipt creation encountered a variable-name error'}
REC.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
