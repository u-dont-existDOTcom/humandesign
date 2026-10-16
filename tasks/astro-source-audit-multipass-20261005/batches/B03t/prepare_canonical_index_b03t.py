#!/usr/bin/env python3
"""Guarded source-only Lilly LXXIV canonical index append, original 1647."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03t_CHAPTER_LXXIV_COMPLETE.md'
PRIOR=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03t_CANONICAL.json'
PRIOR_CUR=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03t.md'
PREP=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json'
assert not any(p.exists() for p in (LATEST,PRIOR,PRIOR_CUR,PREP))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes();j=json.loads(raw)
A=json.loads((B/'ACCEPTANCE.json').read_text(encoding='utf-8'))
R=json.loads((B/'RULES.json').read_text(encoding='utf-8'))
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').read_text(encoding='utf-8'))
assert j['records_count']==4170 and j['batches'][-1]['id']=='B03s'
assert j['next']['chapter']=='LXXIV' and j['next']['pdf_page']==456
assert j['read_numbered_chapters']==list(range(1,74))
assert j['empirical_validations']==0 and j['runtime_promotions']==0
assert j['source_sha256']==A['original_full_pdf_sha256']
assert not any(b['id']=='B03t' for b in j['batches'])
assert A['documentary_accepted_locally']
assert A['prior_accepted_lilly']==4170 and A['new_documentary_records']==153
assert A['lilly_if_published']==4323 and A['combined_if_published']==5389
assert A['original_image_reverse_passages']==28 and A['retained_source_uncertainties']==32
assert R['record_count']==153 and R['independently_verified_journey_cases']==0
assert [r['record_number'] for r in R['rules']]==list(range(4171,4324))
assert R['rules'][-1]['chapter']==R['rules'][-2]['chapter']=='LXXV_NAVIGATION_ONLY'
assert Z['crc_pass'] and Z['every_member_hash_pass'] and Z['actual_extraction_pass']
assert Z['extracted_tests_passed']==19 and Z['extracted_test_exit_code']==0
assert H(Z['owner_download_path'])==Z['archive_sha256']
assert H(B/'RULES.json')==A['rules_sha256']==Z['accepted_rules_sha256']
relative=str(IDX.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',relative],cwd=ROOT).returncode==0
old_git_blob=git('rev-parse','HEAD:'+relative)
assert old_git_blob==git('hash-object',str(IDX))
j['batches'].append({'id':'B03t','path':'batches/B03t/RULES.json',
 'records_count':153,'sha256':A['rules_sha256'],
 'scope':'Lilly original 1647 Book II LXXIV complete ninth-house general doctrine and voyage subsections, original PDF456-463 above LXXV divider. 151 original source clauses + 2 LXXV navigation labels, 28 primary visual passages with six two-page seams, 32 retained uncertainties. Storm/wind, voyage, return, correspondence truth, purposes, duration are source doctrines with no independently verified human cases.'})
j['records_count']=4323
j['read_numbered_chapters'].append(74)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LXXIV_HISTORICAL_DOCUMENTARY_ONLY_NEXT_LXXV_OPEN'
j['next']={'pdf_page':463,'printed_page':429,'chapter':'LXXV',
 'printed_chapter_numeral':'LXXV',
 'heading':'If one shall profit by his Knowledge, be it in what kind it will; Chymistry, Chyrurgery, etc. or if he be perfect',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF463 printed429 BELOW chapter LXXIV journey-length section and horizontal divider; LXXV knowledge/profession chapter begins here.'}
j['chapter_LXXIV_source_acceptance_note']='153 source documentary records R4171-R4323 (151 substantive + 2 LXXV navigation), 28 original image passages, 32 unresolved source limitations and six physical page seams, original PDF456-463. No independently checked voyage, weather, news or safe return cases; zero empirical predictive validations or runtime promotions.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03t_CHAPTER_LXXIV_COMPLETE.md'
assert j['records_count']==sum(b['records_count'] for b in j['batches'])==4323
assert j['read_numbered_chapters']==list(range(1,75))
REPORT="""# Original Lilly (1647) Chapter LXXIV — ninth-house and voyages documentary acceptance

2026-10-16 Africa/Dakar UTC+0. Primary witness: William Lilly, *Christian Astrology* first edition 1647, Wellcome b30338724, full original PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

Complete original Chapter LXXIV begins on PDF456/printed422, after ninth-house introduction and Chapter LXXIII divider, and ends partway through PDF463/printed429 before new numbered LXXV knowledge/learning chapter. The original eight pages PDF456–463 are visually examined and frozen by individual SHA-256 hashes.

**Original body subsections retained:** initial ninth-house good/bad testimony; sea voyages and alleged success, theft, goods and profit; weather and favorable/adverse wind; journey phases by first/tenth/seventh/fourth houses; help via planet/occupation classes; short versus slow return; return of an absent person from a long journey; application/separation as alleged past/present/future, and sign ingress; adverse combustion, detention and fatal conjectures; Mercury/Moon as sources of news and letters; truth or mixture of letters by Mercury-sign modality; planetary reasons for journey; and destination, return and duration conditions.

**Important interpretive limits:** A short journey can still be difficult. Good reports are not physical reunions. Angles and sign modality can indicate length, delay or success depending on distinct aspects and role choices; general conditions cannot become one deterministic predictive classifier. Alleged thieves, imprisonment, death or sickness are seventeenth-century astrological assertions, not factual judgments about people or clinical evidence.

**B03t historical documentary acceptance:** 153 original source units R4171–R4323 (151 substantive clauses plus two LXXV navigation entries), 28 original-image source passages, six physical cross-page spans and 32 preserved uncertainties. No completely independent diplomatic second reader and no independently authenticated individual trip, weather, person status or letter outcome.

**After authenticated research publication:** Lilly **4,323** + retained Ptolemy **1,066** = **5,389 historical documentary source records**. Zero new empirically validated astrology predictions and zero runtime model promotions.

Owner ZIP: Astrology-Lilly-Chapter-LXXIV-Ninth-House-Documentary-20261016.zip in designated Downloads, CRC/hash checks, full extraction and 19 source/admission test replay passed.

**NEXT** original numbered LXXV: If one shall profit by his knowledge or specialty (Chymistry, Chyrurgery, etc.), begins original PDF463/printed429 below the divider. Source study OPEN.
"""
PREFIX="""# Current original astrology source-study checkpoint: Chapter LXXIV

CURRENT 2026-10-16: Lilly Chapter LXXIV full ninth-house/voyage source accepted as 153 historical documentary records, after authenticated publication Lilly 4,323 + Ptolemy 1,066 = 5,389. Next LXXV starts original PDF463 after divider. No independently verified voyage predictions and zero runtime model promotions. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03t_CHAPTER_LXXIV_COMPLETE.md.

---

"""
PRIOR.parent.mkdir(parents=True,exist_ok=True)
PRIOR.write_bytes(raw)
PRIOR_CUR.write_bytes(CUR.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CUR.write_text(PREFIX+PRIOR_CUR.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(REPORT,encoding='utf-8')
receipt={'batch':'B03t','status':'GUARDED_LOCAL_ORIGINAL_DOCUMENTARY_INDEX_PREPARED',
 'prior_canonical_index_git_blob_sha1':old_git_blob,
 'prior_index_sha256':H(PRIOR),'new_index_sha256':H(IDX),
 'current_state_sha256':H(CUR),'latest_source_state_sha256':H(LATEST),
 'accepted_rules_sha256':A['rules_sha256'],'accepted_owner_zip_sha256':Z['archive_sha256'],
 'new_historical_documentary_units':153,
 'lilly_if_published':4323,'ptolemy_retained':1066,'combined_if_published':5389,
 'next_original_chapter':'LXXV','next_pdf_page':463,
 'independently_validated_journey_outcomes':0,
 'new_empirical_predictions':0,'runtime_promotions':0,'remotely_published':False}
PREP.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
