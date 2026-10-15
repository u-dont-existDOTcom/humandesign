#!/usr/bin/env python3
"""Guarded original historical source B03i index append, preserving printed typo."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03i_CHAPTER_LXIII_COMPLETE.md'
OLDI=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03i_CANONICAL.json'
OLDC=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03i.md'
REC=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json'
assert LATEST.is_file() and not any(x.exists() for x in (OLDI,OLDC,REC))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
run=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes();j=json.loads(raw)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').read_text())
assert j['records_count']==3527 and j['batches'][-1]['id']=='B03h'
assert j['next']['chapter']=='LXIII' and j['next']['pdf_page']==428
assert j['read_numbered_chapters']==list(range(1,63))
assert j['runtime_promotions']==j['empirical_validations']==0
assert j['source_sha256']==A['source_full_pdf_sha256']
assert A['documentary_accepted_locally'] and A['new_documentary_records']==44
assert A['previous_accepted_lilly']==3527
assert A['lilly_if_published']==3571 and A['combined_if_published']==4637
assert A['source_reverse_spans']==15 and A['unresolved_source_issues']==16
assert R['record_count']==44 and R['independent_thief_convictions_verified']==0
assert [r['record_number'] for r in R['rules']]==list(range(3528,3572))
assert R['rules'][-1]['chapter']=='NEXT_PRINTED_LIV_FISH_STOLEN_NAVIGATION_ONLY'
assert Z['crc_pass'] and Z['member_sha256_pass']
assert Z['extracted_focused_tests_passed']==19 and Z['extracted_test_exit_code']==0
assert sha(Z['download_path'])==Z['zip_sha256']
assert sha(B/'RULES.json')==A['rules_sha256']==Z['accepted_rules_sha256']
path=str(IDX.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',path],cwd=ROOT).returncode==0
prevblob=run('rev-parse','HEAD:'+path)
assert prevblob==run('hash-object',str(IDX))
assert not any(x['id']=='B03i' for x in j['batches'])
j['batches'].append({'id':'B03i','path':'batches/B03i/RULES.json',
 'records_count':44,'sha256':A['rules_sha256'],
 'scope':'Original Lilly 1647 Book II Chapter LXIII Of Theft, PDF428 below divider through PDF430 bottom; 43 historical theft/doctrine/money-case source notes and one next fish-case heading. PDF431 next prints CHAP LIV, logical sequential LXIV, misprint retained; 15 original-image passages, 16 limits. Money recovered within three days author reported, no independent case validation.'})
j['records_count']=3571
j['read_numbered_chapters'].append(63)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LXIII_DOCUMENTARY_SOURCE_ONLY_NEXT_LXIV_LOGICAL_PRINTED_LIV_OPEN'
j['next']={'pdf_page':431,'printed_page':397,'chapter':'LXIV',
 'printed_chapter_numeral':'LIV',
 'heading':'Fish Stolen.','include_opening_paragraph':True,
 'extracted':False,'boundary_image_read':True,
 'position':'Original PDF431 printed397 top new distinct Fish Stolen worked example. Printed CHAP LIV is a numbering anomaly after Chapter LXIII; logical next LXIV, not earlier buying/selling LIV.'}
j['chapter_LXIII_source_acceptance_note']='44 historical editorial units including next fish-case navigation marker, 15 reverse original-image source passages, 16 limits. Master Allen and Lilly differing thief signification methods preserved; 24 May 1647 stolen-money case author reports return within 3 days, no independent evidence. Printed next Chap LIV is a misnumbering; preserve original and chronological LXIV separately.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03i_CHAPTER_LXIII_COMPLETE.md'
assert j['records_count']==sum(b['records_count'] for b in j['batches'])==3571
assert j['read_numbered_chapters']==list(range(1,64))
prefix="""# Current historical astrology source checkpoint — Lilly Chapter LXIII

Current 2026-10-15: Original Lilly Chapter LXIII Of Theft source accepted, 3,571 Lilly + retained Ptolemy 1,066 = 4,637 original documentary records after authenticated publication. Next distinct case is Fish Stolen at original PDF431/printed397, printed literal CHAP LIV though sequentially Chapter LXIV. Preserve misnumbering and distinguish from earlier LIV Buying/Selling. Historical author money-recovery case is NOT independent predictive validation; empirical count zero, runtime promotion zero. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03i_CHAPTER_LXIII_COMPLETE.md and B03i publication receipt.

---

"""
OLDI.parent.mkdir(parents=True,exist_ok=True)
OLDI.write_bytes(raw)
OLDC.write_bytes(CUR.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
CUR.write_text(prefix+OLDC.read_text())
proof={'batch':'B03i','kind':'GUARDED_CANONICAL_SOURCE_INDEX_PREPARED_NOT_PUBLISHED',
 'previous_index_git_blob_sha1':prevblob,'old_index_sha256':sha(OLDI),
 'new_index_sha256':sha(IDX),'new_current_sha256':sha(CUR),
 'new_latest_sha256':sha(LATEST),'accepted_rules_sha256':A['rules_sha256'],
 'release_zip_sha256':Z['zip_sha256'],'accepted_source_units':44,
 'lilly_if_published':3571,'ptolemy_retained':1066,'combined_if_published':4637,
 'next_chapter_logical':'LXIV','next_heading_original_print':'LIV',
 'new_empirical_predictions_validated':0,'runtime_promotions':0,'remote_published':False}
REC.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(proof,indent=2))
