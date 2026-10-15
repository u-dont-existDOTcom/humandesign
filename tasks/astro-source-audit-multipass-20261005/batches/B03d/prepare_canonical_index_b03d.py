#!/usr/bin/env python3
"""Guarded source-only admission for original Lilly 1647 Chapter LVIII."""
import hashlib,json,subprocess
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CURRENT=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03d_CHAPTER_LVIII_COMPLETE.md'
OLDI=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03d_CANONICAL.json'
OLDC=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03d.md'
PREP=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json'
assert not any(p.exists() for p in (LATEST,OLDI,OLDC,PREP))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
G=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
original=I.read_bytes()
j=json.loads(original)
a=json.loads((B/'ACCEPTANCE.json').read_text())
rules=json.loads((B/'RULES.json').read_text())
archive=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').read_text())
assert j['records_count']==3322 and j['batches'][-1]['id']=='B03c'
assert j['next']['chapter']=='LVIII' and j['next']['pdf_page']==417
assert j['read_numbered_chapters']==list(range(1,58))
assert j['source_sha256']==a['original_full_pdf_sha256']
assert j['empirical_validations']==j['runtime_promotions']==0
assert all(x['id']!='B03d' for x in j['batches'])
assert a['documentary_accepted_locally'] and a['whole_chapter_lviii_documentary_source_accepted']
assert a['previous_accepted_lilly']==3322 and a['new_historical_documentary_units']==38
assert a['source_reverse_passages']==18 and a['retained_text_uncertainties']==14
assert rules['record_count']==38 and rules['rules'][-1]['chapter']=='LIX_HEADING_ONLY'
assert [r['record_number'] for r in rules['rules']]==list(range(3323,3361))
assert all(r['chapter']=='LVIII' for r in rules['rules'][:-1])
assert rules['new_predictive_accuracy_validation']==rules['runtime_model_promotions']==0
assert archive['zip_crc_pass'] and archive['member_sha256_pass'] and archive['actual_extraction_pass']
assert archive['extracted_test_count']==15 and archive['extracted_15_tests_exit_code']==0
assert H(archive['archive_on_laptop'])==archive['archive_sha256']
assert H(B/'RULES.json')==a['rules_sha256']==archive['accepted_rules_sha256']
rel=str(I.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rel],cwd=ROOT).returncode==0
original_blob=G('rev-parse','HEAD:'+rel)
assert original_blob==G('hash-object',str(I))
j['batches'].append({
 'id':'B03d','path':'batches/B03d/RULES.json',
 'records_count':38,'sha256':a['rules_sha256'],
 'scope':'Book II Chapter LVIII on general versus specific suspected enemies, original PDF417 below LVII divider through PDF419 above LIX divider; 37 LVIII documentary units and LIX heading-only marker; 18 original-image reverse source passages, 14 preserved uncertainties; no real person or empirical validation.'})
j['records_count']=3360
j['read_numbered_chapters'].append(58)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LVIII_DOCUMENTARY_SOURCE_ONLY_NEXT_LIX_OPEN'
j['next']={
 'pdf_page':419,'printed_page':385,'chapter':'LIX',
 'heading':'A Lady, if marry the Gentleman desired?',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF419 BELOW horizontal divider after final LVIII square/opposition reception statement; worked marriage horary diagram and accompanying prose require direct original image mapping.'}
j['chapter_LVIII_source_acceptance_note']='38 historical source annotations including a LIX navigation marker; 18 reverse original-image passages, 14 retained concerns. 15 source tests replayed from a CRC-and-hash-verified archive. No independent complete blind diplomatic transcription, real-world detection of enemies, empirical predictions or model runtime changes.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03d_CHAPTER_LVIII_COMPLETE.md'
assert j['records_count']==sum(x['records_count'] for x in j['batches'])==3360
assert j['read_numbered_chapters']==list(range(1,59))
body="""# Lilly Book II Chapter LVIII — documentary 1647 source acceptance

2026-10-15 Africa/Dakar UTC+0. Historical original-source study only, not reliable identification of actual people's intentions or evidence that astrology predicts.

William Lilly Christian Astrology (1647), Wellcome b30338724 original 894-page PDF verified SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

Chapter LVIII starts original PDF417/printed383 BELOW the divider following Chapter LVII and ends PDF419/printed385 ABOVE the divider beginning Chapter LIX. It distinguishes a general question about unnamed enemies from a question about a specifically nominated person, with different houses and relationship-specific qualifications, hard-aspect/application/separation timings and reception cases. The original author conjectures concealed enemies and disguised friendship; these are NOT independent psychological evidence. His first-person margin "Often and ever by me found true" is not an audited historical sample.

Accepted source-only B03d 38 editorial documentary units R3323–R3360, including 37 substantive LVIII annotations and one LIX heading-only navigation marker. Eighteen original source-image passage groups map to 38 unique units. Fourteen uncertainty/disclaimer entries remain. Original PDF417–419 scans and hashes accompany the packet. No complete independent blinded word-for-word second transcription.

**After authenticated research branch publication**: 3,360 Lilly + retained Ptolemy 1,066 = 4,426 documentary units. Source ZIP Astrology-Lilly-Chapter-LVIII-Documentary-20261015.zip is in owner's laptop Telechargements and passed ZIP integrity, SHA-256, actual extraction and replay of 15 source tests. Zero validated predictions, authenticated real hidden-enemy cases, or runtime model promotions.

**NEXT:** Chapter LIX, *A Lady, if marry the Gentleman desired?*, begins original PDF419/printed385 BELOW divider and contains a large chart dated June 1646 and explanatory prose. Read the diagram directly with original graphic symbols and prose; do not infer ephemeris fields or chart outcomes from OCR. Overall multi-author source study and separate prospective empirical evaluation remain OPEN.
"""
prefix="""# Current astrology source audit — latest original documentary checkpoint

2026-10-15 Africa/Dakar UTC+0. Lilly Book II Chapter LVIII accepted as historical original source in B03d, 3,360 Lilly + 1,066 Ptolemy = 4,426 documentary units after authenticated research publication. Next Chapter LIX is a worked marriage horoscope from original PDF419/printed385 below divider; source chart illustration is essential. Zero empirically demonstrated astrology predictions or runtime model promotions. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03d_CHAPTER_LVIII_COMPLETE.md and B03d source and publication receipts.

---

"""
OLDI.parent.mkdir(parents=True,exist_ok=True)
OLDI.write_bytes(original)
OLDC.write_bytes(CURRENT.read_bytes())
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CURRENT.write_text(prefix+OLDC.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(body,encoding='utf-8')
receipt={
 'batch':'B03d','kind':'CANONICAL_HISTORICAL_SOURCE_INDEX_PREPARED_NOT_REMOTE_PUBLISHED',
 'prior_index_blob_sha1':original_blob,
 'prior_index_sha256':H(OLDI),
 'new_index_sha256':H(I),'new_current_sha256':H(CURRENT),
 'new_latest_sha256':H(LATEST),'rules_sha256':a['rules_sha256'],
 'owner_zip_sha256':archive['archive_sha256'],
 'new_historical_source_units':38,'lilly_if_published':3360,'ptolemy_retained':1066,
 'combined_if_published':4426,'next_chapter':'LIX','next_original_pdf':419,
 'new_empirical_validations':0,'new_runtime_models':0,'remote_published':False}
PREP.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
