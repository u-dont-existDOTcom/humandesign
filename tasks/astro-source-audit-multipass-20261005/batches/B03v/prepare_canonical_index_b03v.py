#!/usr/bin/env python3
"""Guarded original historical Lilly LXXVI source index append."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
INDEX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CURRENT=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03v_CHAPTER_LXXVI_COMPLETE.md'
PRIOR=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03v_CANONICAL.json'
PRIOR_STATE=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03v.md'
RECEIPT=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json'
assert not any(f.exists() for f in (LATEST,PRIOR,PRIOR_STATE,RECEIPT))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
original=INDEX.read_bytes();idx=json.loads(original)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').read_text())
assert idx['records_count']==4384 and idx['batches'][-1]['id']=='B03u'
assert idx['next']['chapter']=='LXXVI' and idx['next']['pdf_page']==466
assert idx['read_numbered_chapters']==list(range(1,76))
assert idx['empirical_validations']==idx['runtime_promotions']==0
assert idx['source_sha256']==A['original_full_pdf_sha256']
assert not any(v['id']=='B03v' for v in idx['batches'])
assert A['documentary_accepted_locally'] and A['prior_accepted_lilly']==4384
assert A['new_documentary_records']==62 and A['lilly_if_published']==4446
assert A['combined_if_published']==5512
assert R['record_count']==62 and R['independently_verified_clerical_appointments']==0
assert [r['record_number'] for r in R['rules']]==list(range(4385,4447))
assert all(r['chapter']=='LXXVII_NAVIGATION_ONLY' for r in R['rules'][-2:])
assert Z['zip_crc_pass'] and Z['member_sha256_pass'] and Z['actual_extraction_pass']
assert Z['replayed_tests_passed']==18 and Z['test_exit_code']==0
assert sha(Z['owner_download_path'])==Z['archive_sha256']
assert sha(B/'RULES.json')==A['rules_sha256']==Z['rules_sha256']
rel=str(INDEX.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rel],cwd=ROOT).returncode==0
old_blob=git('rev-parse','HEAD:'+rel)
assert old_blob==git('hash-object',str(INDEX))
idx['batches'].append({'id':'B03v','path':'batches/B03v/RULES.json',
 'records_count':62,'sha256':A['rules_sha256'],
 'scope':'Original Lilly 1647 Book II LXXVI ecclesiastical appointment, PDF466-468 before LXXVII dream divider. 60 substantive historical clauses plus two LXXVII next navigation; 16 visual source passages, two physical page seams and 20 uncertainties. Outcome branches include admission, delay, loss, alleged payment, competition, and benefice value; no verified appointment or misconduct case.'})
idx['records_count']=4446
idx['read_numbered_chapters'].append(76)
idx['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LXXVI_ORIGINAL_HISTORICAL_SOURCE_ONLY_NEXT_LXXVII_OPEN'
idx['next']={'pdf_page':468,'printed_page':434,'chapter':'LXXVII',
 'printed_chapter_numeral':'LXXVII',
 'heading':'Of Dreames; whether they signifie any thing or not?',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF468/printed434 below LXXVI ecclesiastical appointment divider; following historical interpretation of dreams.'}
idx['chapter_LXXVI_source_acceptance_note']='62 historical documentary records R4385-R4446 (60 substantive plus two LXXVII navigation), 16 visual image passages, two physical cross-page seams and 20 source uncertainties; no independently documented job appointment or financial impropriety, no predictive validation and zero runtime changes.'
idx['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03v_CHAPTER_LXXVI_COMPLETE.md'
assert idx['records_count']==sum(v['records_count'] for v in idx['batches'])==4446
assert idx['read_numbered_chapters']==list(range(1,77))
REPORT="""# Original Lilly 1647 Chapter LXXVI — ecclesiastical benefice historical source

2026-10-16 Africa/Dakar UTC+0. Primary original witness: William Lilly *Christian Astrology* (1647), Wellcome b30338724, full original PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

**Physical source boundaries:** Chapter LXXVI begins original PDF466/printed432 beneath the divider concluding Chapter LXXV, continues PDF467/printed433 and finishes on PDF468/printed434 above the ornamental divider for **Chapter LXXVII (Dreams)**. All three original pages are individually SHA256 frozen.

The original asks whether a cleric obtains an ecclesiastical benefice or parsonage. The querent is signified by first-house ruler and Moon; the ninth lord represents the position. The source considers ninth occupancy, favorable applications, reception, translation of light, third-party competitors and obstructions. It differentiates successful appointment with or without lengthy solicitation, possible difficulty or payment, failure despite near-completion, lost appointment to another applicant, and reception or beneficial transfer mitigating otherwise adverse conditions. Angular, succedent and cadent placements affect alleged timing or failure. A separate tenth-house section asks whether an appointment is valuable rather than simply whether it will be attained.

The chapter finishes with Lilly's polemical criticism of clergy who oppose astrology and his denial that he promotes simony. Those are attributed authorial positions, not verified descriptions of actual conduct. No particular applicant, appointment date, corrupt intermediary, payment or employment result is independently identified, so these statements are historical astrology, not empirical predictive successes.

**Source acceptance B03v:** 62 original documentary annotations R4385-R4446 (60 LXXVI historical claims + two LXXVII navigation units), 16 primary-source passage groups and 20 retained ambiguities/negative conditions. No complete blind second diplomatic transcription, independent modern planetary geometry check or externally authenticated prediction is claimed.

**After authenticated research publication:** Lilly **4,446** and retained Ptolemy **1,066** = **5,512 historical documentary units**. Independent empirical predictive validations **zero**, model-runtime promotions **zero**.

Accepted owner-local ZIP: Astrology-Lilly-Chapter-LXXVI-Parsonage-Documentary-20261016.zip in designated Downloads. Every member SHA256/size verified, ZIP CRC, full extraction and 18 focused source/admission replay tests pass.

NEXT: LXXVII *Of Dreams; whether they signify any thing or not?* beginning original PDF468 below divider. Review original page images through the next true chapter boundary; source study remains OPEN.
"""
PREFIX="""# Current original Lilly astrology historical source study — Chapter LXXVI

CURRENT 2026-10-16: LXXVI ecclesiastical appointment source accepted; after authenticated publication Lilly 4,446 + Ptolemy 1,066 = 5,512 historical documentary annotations. LXXVI runs PDF466–468 above the dreams divider. Next LXXVII begins PDF468/printed434. Zero independent empirical predictions or runtime model promotion. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03v_CHAPTER_LXXVI_COMPLETE.md and batch B03v proof.

---

"""
PRIOR.parent.mkdir(parents=True,exist_ok=True)
PRIOR.write_bytes(original)
PRIOR_STATE.write_bytes(CURRENT.read_bytes())
INDEX.write_text(json.dumps(idx,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CURRENT.write_text(PREFIX+PRIOR_STATE.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(REPORT,encoding='utf-8')
receipt={'batch':'B03v','status':'GUARDED_LOCAL_HISTORICAL_DOCUMENTARY_INDEX_PREPARED_NOT_GITHUB',
 'prior_index_git_blob_sha1':old_blob,
 'prior_index_sha256':sha(PRIOR),'new_index_sha256':sha(INDEX),
 'current_state_sha256':sha(CURRENT),'latest_source_state_sha256':sha(LATEST),
 'accepted_rules_sha256':A['rules_sha256'],
 'owner_zip_sha256':Z['archive_sha256'],
 'new_historical_documentary_records':62,
 'lilly_if_published':4446,'ptolemy_retained':1066,'combined_if_published':5512,
 'next_original_chapter':'LXXVII','next_source_pdf':468,
 'independent_ecclesiastical_outcomes_validated':0,
 'empirically_validated_predictions':0,'runtime_promotions':0,
 'remote_published':False}
RECEIPT.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
