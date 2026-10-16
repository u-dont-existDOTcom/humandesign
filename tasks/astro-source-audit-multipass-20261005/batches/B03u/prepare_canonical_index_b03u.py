#!/usr/bin/env python3
"""Guarded original Lilly LXXV historical source integration; printed folios 430/431 transposed."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
INDEX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CURRENT=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03u_CHAPTER_LXXV_COMPLETE.md'
PRIOR=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03u_CANONICAL.json'
PRIOR_STATE=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03u.md'
RECEIPT=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json'
assert not any(f.exists() for f in [LATEST,PRIOR,PRIOR_STATE,RECEIPT]),'Existing canonical packet, do not overwrite'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
original=INDEX.read_bytes()
index=json.loads(original)
A=json.loads((B/'ACCEPTANCE.json').read_text(encoding='utf-8'))
R=json.loads((B/'RULES.json').read_text(encoding='utf-8'))
W=json.loads((B/'SOURCE_WINDOW_MANIFEST.json').read_text(encoding='utf-8'))
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').read_text(encoding='utf-8'))
assert index['records_count']==4323 and index['batches'][-1]['id']=='B03t'
assert index['next']['chapter']=='LXXV' and index['next']['pdf_page']==463
assert index['read_numbered_chapters']==list(range(1,75))
assert index['empirical_validations']==index['runtime_promotions']==0
assert index['source_sha256']==W['original_full_pdf_sha256']
assert all(b['id']!='B03u' for b in index['batches'])
assert A['documentary_accepted_locally'] and A['prior_lilly_accepted']==4323
assert A['new_documentary_records']==61 and A['lilly_if_published']==4384
assert A['combined_if_published']==5450
assert A['original_pdf_text_order']==[463,464,465,466]
assert A['original_imprinted_folio_numbers']==[429,431,430,432]
assert R['record_count']==61 and [r['record_number'] for r in R['rules']]==list(range(4324,4385))
assert all(r['chapter']=='LXXVI_NAVIGATION_ONLY' for r in R['rules'][-2:])
assert R.get('empirically_validated_predictive_cases',0)==0 and R['runtime_promotions']==0
assert Z['zip_crc_pass'] and Z['every_member_sha256_and_size_match'] and Z['actual_extraction_pass']
assert Z['extracted_source_tests_passed']==20 and Z['extracted_test_exit_code']==0
assert sha(Z['owner_download_path'])==Z['archive_sha256']
assert sha(B/'RULES.json')==A['rules_sha256']==Z['accepted_rules_sha256']
rel=str(INDEX.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rel],cwd=ROOT).returncode==0
old_blob=git('rev-parse','HEAD:'+rel)
assert old_blob==git('hash-object',str(INDEX))
index['batches'].append({
 'id':'B03u','path':'batches/B03u/RULES.json',
 'records_count':61,'sha256':A['rules_sha256'],
 'scope':'Original Lilly 1647 Book II Chapter LXXV knowledge/skill, actual wisdom, multiple absent people, and journey directions/wealth. Physical PDF463-466 text order, but ORIGINAL PRINTED NUMERALS 429,431,430,432 transposed at middle. 59 LXXV source clauses plus two LXXVI heading markers; 16 source passages and 20 retained interpretive limits. No independent person, competence, or travel case outcome.'
})
index['records_count']=4384
index['read_numbered_chapters'].append(75)
index['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LXXV_HISTORICAL_DOCUMENTARY_ONLY_NEXT_LXXVI_OPEN'
index['next']={
 'pdf_page':466,'printed_page':432,'chapter':'LXXVI',
 'printed_chapter_numeral':'LXXVI',
 'heading':'If an idle covetous Priest upon his Question propounded shall Obtain a good Parsonage, yea or no?',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF466/printed432 below divider after knowledge/traveler chapter LXXV. Scan order 463,464,465,466 is authoritative despite earlier reversal of imprinted folios 430 and 431.'
}
index['chapter_LXXV_source_acceptance_note']=(
 '61 historical editorial source annotations R4324-R4384 including two next-chapter navigation markers, '
 '16 original-image source passages and 20 textual issues. ORIGINAL IMPRENTED FOLIOS 429,431,430,432 '
 'follow physically sequential scans 463,464,465,466. Do not reorder scans numerically by printed folio. '
 'No independent skilled-person/traveler observations and no empirical forecast or runtime promotion.'
)
index['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03u_CHAPTER_LXXV_COMPLETE.md'
assert index['records_count']==sum(b['records_count'] for b in index['batches'])==4384
assert index['read_numbered_chapters']==list(range(1,76))
REPORT="""# Original William Lilly Chapter LXXV: science, knowledge, absent persons, best travel direction

2026-10-16 Africa/Dakar UTC+0. Original primary witness: Lilly, *Christian Astrology* first edition (1647), Wellcome b30338724 complete original PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

**Source pagination anomaly:** Authoritative physical scans PDF463, PDF464, PDF465, PDF466 have literal **printed folio numerals 429, 431, 430, 432**. Printed 430 and 431 are reversed in the original edition. Reading the actual sentences confirms source-text order follows physical scan order, not monotonically ordered printed folio numerals. PDF463 ends with transition to *Of Science*; PDF464 (printed431) begins that unnumbered science subsection and ends with an ongoing sequential Moon-application account; PDF465 (printed430) continues the account and transitions to journey-direction judgments; PDF466 (printed432) closes the journey paragraph, before a clear horizontal divider for Chapter LXXVI. Never reorder images or assign printed numeral by PDF-34 for these pages.

**Complete Chapter LXXV content:** (a) opening rule whether a subject profits from science/learning, distinguishing possession of knowledge from beneficial application; (b) *Of Science, Cunning or Wisdom in a man, whether it be true or not*; (c) *Of many Persons absent or travelling, in what Condition they are*, based on an ordered group of names and successive Moon applications, with source caveats and no independent traveler data; (d) *To what part of Heaven the Traveller shall best direct his Journey*, using claimed favorable quadrant positions and distinct second/eighth house success at destination versus homecoming.

**Documentary acceptance:** 61 original historical editorial annotations R4324–R4384 (59 Chapter LXXV plus two next-section navigation entries); 16 original-image source passages including three physical page seams; 20 retained source limitations. All four image bytes are separately hashed. No complete independent blinded second diplomatic reading, measured competency/travel outcome, medical/missing-person corroboration, or prospective chart-test validation.

**After authenticated research-branch publication:** Lilly 4,384 and retained Ptolemy 1,066 = **5,450 historical documentary source annotations**, with zero new empirical astrological prediction successes and zero model/runtime promotions.

**Owner release:** Astrology-Lilly-Chapter-LXXV-Original-Folio-Correction-Documentary-20261016.zip in OS Downloads. Archive CRC, individual member SHA-256/size, extraction, and twenty original-source acceptance tests replay verified.

**NEXT:** Original PDF466/printed432 beneath the divider begins numbered Chapter LXXVI on whether a minister obtains a parsonage or ecclesiastical appointment. Its source body may run beyond PDF466; inspect the true subsequent original chapter boundary. Research remains OPEN.
"""
PREFIX="""# Current original astrology source study: Chapter LXXV

CURRENT 2026-10-16: William Lilly original 1647 Chapter LXXV historical text accepted on isolated research branch. After authenticated publication Lilly **4,384** + retained Ptolemy **1,066** = **5,450** historical documentary annotations. Printed 430 and 431 are transposed between physically sequential PDF464 and PDF465: preserve original scan order. Next Chapter LXXVI starts on original PDF466 printed432. No empirical predictive validations and zero runtime changes. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03u_CHAPTER_LXXV_COMPLETE.md and B03u source-admission receipts.

---

"""
PRIOR.parent.mkdir(parents=True,exist_ok=True)
PRIOR.write_bytes(original)
PRIOR_STATE.write_bytes(CURRENT.read_bytes())
INDEX.write_text(json.dumps(index,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CURRENT.write_text(PREFIX+PRIOR_STATE.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(REPORT,encoding='utf-8')
receipt={'batch':'B03u','status':'GUARDED_ORIGINAL_HISTORICAL_SOURCE_INDEX_PREPARED_LOCAL_PENDING_GITHUB',
 'previous_index_git_blob_sha1':old_blob,
 'previous_index_sha256':sha(PRIOR),'new_index_sha256':sha(INDEX),
 'new_current_state_sha256':sha(CURRENT),'new_latest_state_sha256':sha(LATEST),
 'accepted_rules_sha256':A['rules_sha256'],
 'owner_release_archive_sha256':Z['archive_sha256'],
 'new_original_documentary_records':61,
 'lilly_if_published':4384,'retained_ptolemy':1066,'combined_if_published':5450,
 'original_scan_order':[463,464,465,466],
 'literal_printed_folio_numbers':[429,431,430,432],
 'next_chapter':'LXXVI','next_pdf_page':466,
 'independent_empirical_astrology_validations':0,'runtime_promotions':0,
 'remote_published':False}
RECEIPT.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
