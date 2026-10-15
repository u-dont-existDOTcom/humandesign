#!/usr/bin/env python3
"""Guarded canonical research index admission of original-source Chapter LVII."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03c_CHAPTER_LVII_COMPLETE.md'
OLDI=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03c_CANONICAL.json'
OLDC=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03c.md'
PREP=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json'
assert not any(x.exists() for x in (LATEST,OLDI,OLDC,PREP))
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
G=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
raw=I.read_bytes()
idx=json.loads(raw)
a=json.loads((B/'ACCEPTANCE.json').read_text())
rules=json.loads((B/'RULES.json').read_text())
release=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').read_text())
assert idx['records_count']==3248 and idx['batches'][-1]['id']=='B03b'
assert idx['next']['chapter']=='LVII' and idx['next']['pdf_page']==414
assert idx['read_numbered_chapters']==list(range(1,57))
assert idx['runtime_promotions']==idx['empirical_validations']==0
assert all(b['id']!='B03c' for b in idx['batches'])
assert a['documentary_accepted_locally'] and a['whole_chapter_lvii_source_intake_complete']
assert a['added_documentary_units']==74 and a['previous_accepted_lilly']==3248
assert a['source_reverse_spans']==26 and a['retained_source_issues']==19
assert rules['record_count']==74 and rules['rules'][-1]['chapter']=='LVIII_HEADING_ONLY'
assert [r['record_number'] for r in rules['rules']]==list(range(3249,3323))
assert all(r['chapter']=='LVII' for r in rules['rules'][:-1])
assert rules['empirically_validated_predictions']==rules['runtime_model_promotions']==0
assert release['zip_crc_pass'] and release['member_sha256_pass'] and release['actual_extraction_pass']
assert release['extracted_test_count']==17 and release['extracted_17_tests_exit_code']==0
assert H(release['archive_on_laptop'])==release['archive_sha256']
assert a['rules_sha256']==release['accepted_rules_sha256']==H(B/'RULES.json')
rel=str(I.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rel],cwd=ROOT).returncode==0
prior_blob=G('rev-parse','HEAD:'+rel)
assert prior_blob==G('hash-object',str(I))
idx['batches'].append({
 'id':'B03c','path':'batches/B03c/RULES.json',
 'records_count':74,'sha256':a['rules_sha256'],
 'scope':'Original William Lilly 1647 Book II Chapter LVII commanders/army roles and unnumbered whether-armies-fight section, PDF414 below LVI divider through PDF417 above LVIII divider; 73 chapter documentary annotations + one LVIII navigation marker, 26 reverse source spans and 19 textual limits; zero verified cases or runtime rules.'})
idx['records_count']=3322
idx['read_numbered_chapters'].append(57)
idx['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LVII_DOCUMENTARY_SOURCE_ONLY_NEXT_LVIII_OPEN'
idx['next']={
 'pdf_page':417,'printed_page':383,'chapter':'LVIII',
 'heading':'If the Querent have open Enemies, or any Adversaries or many that doe envy him.',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF417 BELOW horizontal divider following final LVII no-fight reception exception; continue into PDF418 and subsequent pages to LVIII end.'}
idx['chapter_LVII_source_acceptance_note']='74 source-only 1647 historical annotations, including next chapter navigation; four scan pages, 26 one-to-many reverse original-source passage maps, 19 retained text and interpretation limits. Includes unnumbered if-the-armies-shall-fight subsection. Source review not full blinded independent diplomatic transcription. 17 extracted tests passed, no known independent real cases, blind predictions or runtime promotions.'
idx['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03c_CHAPTER_LVII_COMPLETE.md'
assert idx['read_numbered_chapters']==list(range(1,58))
assert idx['records_count']==sum(b['records_count'] for b in idx['batches'])==3322
latest_text="""# Original Lilly Book II Chapter LVII — source documentary acceptance

2026-10-15 Africa/Dakar UTC+0. Original William Lilly Christian Astrology, Wellcome 1647 b30338724; original complete 894-page PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b. Not a modern advice source or proof of prediction.

Chapter LVII begins original PDF414/printed380 BELOW the prior chapter divider, continues through PDF415/381 and PDF416/382, and ends original PDF417/383 ABOVE the LVIII divider. It includes the general twelve-house/turned-opponent comparison and a separate unnumbered *If the Armies shall fight* passage. The latter concludes with a historical condition changing a fight forecast into a settlement when the weightier planet receives the translator, without a specified modern weight/orb formula.

**B03c 74 historical source units R3249–R3322** (73 original LVII authorial annotations and one LVIII heading-only navigation marker). The 26 manually reviewed original-image source passage groups map without duplicate or unassigned editorial records; 19 original grammar, glyph, actor/polarity, or inference limits are preserved. Scans from four original pages are hash-frozen and included in the release packet. An independent blind complete diplomatic re-transcription is not claimed.

**After verified source publication:** accepted Lilly 3,322 + retained Ptolemy 1,066 = 4,388 historical documentary units. Zero observed war outcomes, real-person accusations, empirical astrology predictions, or runtime model changes; no combat tactics or advice follow from this material. The owner-facing ZIP Astrology-Lilly-Chapter-LVII-Documentary-20261015.zip in the laptop's French Telechargements passed ZIP CRC, individual SHA-256, complete extraction and 17 source-only tests replayed.

Next original Chapter LVIII *If the Querent have open Enemies*, beginning PDF417/printed383 BELOW the divider. The broad historical astrology source-and-empirical project remains OPEN.
"""
prepend="""# Current astrology original-source research checkpoint

2026-10-15 Africa/Dakar UTC+0. Original Lilly 1647 Chapter LVII locally source-accepted for documentary evidence, 3,322 Lilly + 1,066 Ptolemy = 4,388 historical units after authenticated publication. Next Chapter LVIII, original PDF417/printed383 BELOW divider. Zero new empirically demonstrated astrological outcomes or active model changes. Details state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03c_CHAPTER_LVII_COMPLETE.md plus B03c source-first evidence and publication receipts.

---

"""
OLDI.parent.mkdir(parents=True,exist_ok=True)
OLDI.write_bytes(raw)
OLDC.write_bytes(CUR.read_bytes())
I.write_text(json.dumps(idx,indent=2,ensure_ascii=False)+'\n')
CUR.write_text(prepend+OLDC.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(latest_text,encoding='utf-8')
preprec={
 'batch':'B03c',
 'kind':'CANONICAL_HISTORICAL_SOURCE_INDEX_PREPARED_NOT_REMOTE_PUBLISHED',
 'previous_index_blob_sha1':prior_blob,
 'previous_index_sha256':H(OLDI),
 'new_index_sha256':H(I),
 'new_current_state_sha256':H(CUR),
 'new_latest_state_sha256':H(LATEST),
 'accepted_historical_rules_sha256':a['rules_sha256'],
 'owner_zip_sha256':release['archive_sha256'],
 'new_locally_accepted_documentary_source_units':74,
 'lilly_if_published':3322,'retained_ptolemy':1066,
 'combined_if_published':4388,'next_chapter':'LVIII',
 'next_original_pdf':417,'new_empirical_predictions':0,
 'new_runtime_rules':0,'remote_published':False}
PREP.write_text(json.dumps(preprec,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(preprec,indent=2,ensure_ascii=False))
