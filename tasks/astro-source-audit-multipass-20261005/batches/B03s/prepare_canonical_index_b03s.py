#!/usr/bin/env python3
"""Guarded historical original source index transition: Chapter LXXIII to LXXIV."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CURRENT=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03s_CHAPTER_LXXIII_COMPLETE.md'
PRIOR= B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03s_CANONICAL.json'
PRIOR_CURRENT=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03s.md'
PREP=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json'
assert not any(p.exists() for p in (LATEST,PRIOR,PRIOR_CURRENT,PREP))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
old=IDX.read_bytes();j=json.loads(old)
A=json.loads((B/'ACCEPTANCE.json').read_text(encoding='utf-8'))
R=json.loads((B/'RULES.json').read_text(encoding='utf-8'))
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').read_text(encoding='utf-8'))
assert j['records_count']==4136 and j['batches'][-1]['id']=='B03r'
assert j['next']['chapter']=='LXXIII' and j['next']['pdf_page']==455
assert j['read_numbered_chapters']==list(range(1,73))
assert j['empirical_validations']==j['runtime_promotions']==0
assert j['source_sha256']==A['original_pdf_sha256']
assert all(b['id']!='B03s' for b in j['batches'])
assert A['documentary_accepted_locally'] and A['prior_accepted_lilly']==4136
assert A['new_documentary_records']==34
assert A['lilly_if_published']==4170 and A['combined_if_published']==5236
assert A['original_image_source_spans']==10 and A['unresolved_source_issues']==17
assert R['record_count']==34 and R['independently_verified_paid_portion_outcomes']==0
assert [r['record_number'] for r in R['rules']]==list(range(4137,4171))
assert all(r['chapter']=='LXXIV_NAVIGATION_ONLY' for r in R['rules'][-2:])
assert Z['zip_crc_pass'] and Z['every_member_hash_and_size_pass'] and Z['full_extraction_pass']
assert Z['extracted_tests_passed']==17 and Z['extracted_exit_code']==0
assert H(Z['owner_download_path'])==Z['archive_sha256']
assert H(B/'RULES.json')==A['rules_sha256']==Z['rules_sha256']
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rel],cwd=ROOT).returncode==0
original_git_blob=git('rev-parse','HEAD:'+rel)
assert original_git_blob==git('hash-object',str(IDX))
j['batches'].append({'id':'B03s','path':'batches/B03s/RULES.json',
 'records_count':34,'sha256':A['rules_sha256'],
 'scope':'Lilly original 1647 Book II LXXIII If have the Portion promised? 13 July 1634 6:15 PM, PDF455 and early PDF456 before ninth-house section. 32 chapter source units plus 2 LXXIV navigation labels, 10 reverse primary source passages, 17 explicit limitations. Author says payment would be performed and questioner reported all true, but no independently verified payment proof or prospective forecast.'})
j['records_count']=4170
j['read_numbered_chapters'].append(73)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LXXIII_HISTORICAL_DOCUMENTARY_ONLY_NEXT_LXXIV_OPEN'
j['next']={'pdf_page':456,'printed_page':422,'chapter':'LXXIV',
 'printed_chapter_numeral':'LXXIV',
 'heading':'Of good or ill in questions concerning this House',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF456 printed422 below ninth-house general preface Long Journeys, Religion, Pilgrimage and Dreams; LXXIII ends above its ornamental divider. Subsequent unnumbered voyage subsections belong to LXXIV until next true numbered chapter boundary.'}
j['chapter_LXXIII_source_acceptance_note']='34 original-source historical records R4137-R4170, 32 substantive and two following-section navigation, 10 image passages and 17 source limits. The 1634 outcome reported in a 1647 narrative is an unitemized querent self-report; no independent payment outcome or empirical prediction is validated.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03s_CHAPTER_LXXIII_COMPLETE.md'
assert j['records_count']==sum(b['records_count'] for b in j['batches'])==4170
assert j['read_numbered_chapters']==list(range(1,74))
REPORT="""# Lilly original 1647 Chapter LXXIII — promised dowry historical source

2026-10-16 Africa/Dakar (UTC+0). Original source William Lilly, *Christian Astrology* (1647), Wellcome b30338724 complete PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

Chapter LXXIII *If have the Portion promised?* begins original PDF455/printed421 with a separate square horoscope printed **13 July 1634, 6:15 PM**. It finishes on PDF456/printed422 before the ornamental divider introducing the ninth house. The ninth-house general introduction and Chapter LXXIV below the divider are not LXXIII body.

Lilly represents the querent by Saturn, retrograde in the twelfth house, and the woman by Jupiter and Moon. Her wealth is referred to the radical eighth (derived second from her seventh). The source invokes Venus occupying eighth, Sun ruling it in own sign, Moon separating from a sextile of Sun and allegedly transferring influence to Saturn, ruler of the querent ascendant, second and dispositor of the Part of Fortune. He says the promised portion should be fulfilled, but states neither amount nor date.

The **only confirmation in these pages** is a broad report that the querent himself said all the assertions proved true. That wording does not furnish a separate payment receipt or a frozen test of the original forecast. Personality and scar descriptions are other unverified source claims. The event was written up in 1647, after the 1634 figure. Zero independently verified payment outcomes, empirically validated astrological predictions or runtime rule changes are counted.

**B03s historical documentary acceptance:** 34 source annotations R4137-R4170, including 32 substantive LXXIII clauses and two navigation labels for ninth house / LXXIV; ten original-source passage groups including the PDF455–456 cross-page sentence; 17 retained original-source uncertainties. Primary page bytes are SHA-256 frozen; no complete independent blinded diplomatic transcription or modern ephemeris parity is claimed.

**After authenticated research publication:** Lilly **4,170** + retained Ptolemy **1,066** = **5,236** historical documentary units. The verified archive Astrology-Lilly-Chapter-LXXIII-Promised-Portion-Documentary-20261016.zip is in the owner's designated Downloads folder, with CRC, SHA-256 member checks, extraction and 17 focused test replay.

NEXT: Book II Chapter LXXIV *Of good or ill in questions concerning this House*, beginning original PDF456 printed422 after the separate ninth-house preface. Preserve unnumbered voyage sections through the next true numbered heading. Parent original astrology source study OPEN.
"""
PREFIX="""# Current original astrology source study — Lilly Chapter LXXIII

CURRENT 2026-10-16: Chapter LXXIII documentary source accepted; after authenticated publication 4,170 Lilly and 1,066 retained Ptolemy = 5,236 historical records. Original pages PDF455–456, next LXXIV starts PDF456 beneath ninth-house preface. No independently verified payment outcome, empirical astrology validation or runtime model promotion. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03s_CHAPTER_LXXIII_COMPLETE.md and B03s acceptance, release and publication receipts.

---

"""
PRIOR.parent.mkdir(parents=True,exist_ok=True)
PRIOR.write_bytes(old)
PRIOR_CURRENT.write_bytes(CURRENT.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CURRENT.write_text(PREFIX+PRIOR_CURRENT.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(REPORT,encoding='utf-8')
receipt={'batch':'B03s','status':'LOCAL_HISTORICAL_SOURCE_INDEX_PREPARED_PENDING_GITHUB',
 'original_predecessor_git_blob_sha1':original_git_blob,
 'prior_index_sha256':H(PRIOR),'new_index_sha256':H(IDX),
 'new_current_state_sha256':H(CURRENT),'new_latest_state_sha256':H(LATEST),
 'accepted_rules_sha256':A['rules_sha256'],'owner_release_zip_sha256':Z['archive_sha256'],
 'new_documentary_records':34,'lilly_if_published':4170,
 'ptolemy_retained':1066,'combined_if_published':5236,
 'next_chapter':'LXXIV','next_original_pdf_page':456,
 'independently_validated_payment_cases':0,
 'new_empirical_predictions':0,'runtime_promotions':0,'remotely_published':False}
PREP.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
