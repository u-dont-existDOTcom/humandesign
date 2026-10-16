#!/usr/bin/env python3
"""Guarded Chapter LXXVIII canonical index and state integration."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03x_CHAPTER_LXXVIII_COMPLETE.md'
OLD=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03x_CANONICAL.json'
OLDCUR=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03x.md'
REC=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json'
assert not any(p.exists() for p in (LATEST,OLD,OLDCUR,REC))
h=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes();j=json.loads(raw)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').read_text())
assert j['records_count']==4484 and j['batches'][-1]['id']=='B03w'
assert j['next']['chapter']=='LXXVIII' and j['next']['pdf_page']==470
assert j['read_numbered_chapters']==list(range(1,78))
assert j['source_sha256']==A['original_pdf_sha256']
assert j['empirical_validations']==j['runtime_promotions']==0
assert not any(k['id']=='B03x' for k in j['batches'])
assert A['documentary_accepted_locally'] and A['prior_lilly_accepted']==4484
assert A['new_documentary_records']==24 and A['lilly_if_published']==4508
assert A['combined_if_published']==5574
assert R['record_count']==24 and R['independently_verified_dream_outcomes']==0
assert [r['record_number'] for r in R['rules']]==list(range(4485,4509))
assert all(r['chapter']=='LXXIX_NAVIGATION_ONLY' for r in R['rules'][-2:])
assert Z['zip_crc_pass'] and Z['member_hashes_pass'] and Z['full_extraction_pass']
assert Z['extracted_tests_passed']==14 and Z['extracted_exit_code']==0
assert h(Z['owner_download_path'])==Z['archive_sha256']
assert h(B/'RULES.json')==A['rules_sha256']==Z['accepted_rules_sha256']
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rel],cwd=ROOT).returncode==0
old_blob=git('rev-parse','HEAD:'+rel)
assert old_blob==git('hash-object',str(IDX))
j['batches'].append({'id':'B03x','path':'batches/B03x/RULES.json',
 'records_count':24,'sha256':A['rules_sha256'],
 'scope':'Original William Lilly 1647 Book II Chapter LXXVIII terrible dreams dated example on original PDF470 and PDF471 above LXXIX divider. 22 dream-case documentary clauses plus two following-chapter navigation markers, six source passage groups, 14 unresolved limits, one author-asserted unverified retrospective success, zero independent prediction validations.'})
j['records_count']=4508
j['read_numbered_chapters'].append(78)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LXXVIII_HISTORICAL_SOURCE_ONLY_NEXT_LXXIX_OPEN'
j['next']={'pdf_page':471,'printed_page':437,'chapter':'LXXIX',
 'printed_chapter_numeral':'LXXIX','heading':'If he should obtaine the Parsonage desired',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF471/printed437 below dream example ending; separate circular parsonage horoscope dated 6 August 1644 at 8:24 PM.'}
j['chapter_LXXVIII_source_acceptance_note']='24 documentary annotations R4485-R4508, 22 worked dream-case clauses and two following-chapter navigation markers. Author reports bodily safety with financial loss and says the judgment proved true; no independent outcome corroboration, blind prospective prediction or chart recasting. 6 source passages, 14 retained limits.'
j['current_state']=str(LATEST.relative_to(ROOT))
assert j['records_count']==sum(x['records_count'] for x in j['batches'])==4508
assert j['read_numbered_chapters']==list(range(1,79))
REPORT="""# Original William Lilly (1647) Chapter LXXVIII — Terrible Dreams worked case

2026-10-16 — Africa/Dakar (UTC+0). Source: William Lilly, Christian Astrology first edition (1647), Wellcome b30338724, full original PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

**Original boundaries:** Chapter LXXVIII begins PDF470/printed436 with a square horoscope dated **26 January 1648, 9:27 AM**. It concludes at the top of PDF471/printed437, above the divider opening the separate Chapter LXXIX, whose circular horoscope is dated **6 August 1644, 8:24 PM**. The printed 1648 chart date is preserved despite the edition's 1647 title year; calendar/date reconciliation is unresolved.

**Source-first reasoning:** Lilly treats Jupiter and Saturn as ninth-house rulers, their twelfth-house placements and square aspect to ninth as indicators of dreams arising from worldly preoccupation. He then prioritizes angular Mars as lord of the ascendant and disposer of Part Fortune. He offers **two alternative suggested dream causes**, entrusted estate believed lost and a loss of public office/status. He separately forecasts **no personal peril** and **some estate damage**, reporting in his own words that the outcome proved true.

**Epistemic classification:** Author-reported retrospective success only. No independently authenticated querent, verbatim dream, externally checked financial loss or recorded date of predicted outcome; no prospective prediction freeze and no independently recalculated chart. No predictive-validation credit. No runtime scoring or model change.

**Documentary acceptance:** 24 historical source annotations **R4485–R4508**; 22 LXXVIII substantive units plus two distinct LXXIX navigation annotations. Six bidirectional original-page passage groups, 14 source limitations retained. Original JPEG witnesses PDF470 and PDF471 individually SHA-256 frozen. Focused test suite and independently extracted ZIP test replay passed.

**Upon authenticated publication:** cumulative Lilly **4,508** plus retained Ptolemy **1,066** equals **5,574 historical documentary records**. Independent empirical predictive validations **zero**; runtime promotions **zero**.

Owner archive in laptop Downloads: Astrology-Lilly-Chapter-LXXVIII-Terrible-Dreams-Documentary-20261016.zip. CRC, member hashes and fresh full extraction with 14 test replays passed.

**NEXT:** Chapter LXXIX, desired parsonage, begins on original PDF471 below the divider. Research parent OPEN.
"""
PREFIX="""# Original Lilly research current — Chapter LXXVIII

CURRENT 2026-10-16: LXXVIII terrible dreams case documentary source locally admitted and queued for authenticated research-branch publication, cumulative Lilly 4,508 and retained Ptolemy 1,066 = 5,574 historical records after remote confirmation. Next chapter LXXIX begins original PDF471/printed437 below the divider. The author alone claims the separated personal-safety and financial-loss forecast proved true; independent predictive validations remain zero; no runtime promotions. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03x_CHAPTER_LXXVIII_COMPLETE.md.

---

"""
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);OLDCUR.write_bytes(CUR.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CUR.write_text(PREFIX+OLDCUR.read_text(),encoding='utf-8')
LATEST.write_text(REPORT,encoding='utf-8')
receipt={'batch':'B03x','status':'GUARDED_INDEX_PREPARED_PENDING_GITHUB',
 'prior_index_git_blob_sha1':old_blob,'previous_index_sha256':h(OLD),
 'new_index_sha256':h(IDX),'current_state_sha256':h(CUR),
 'latest_state_sha256':h(LATEST),'accepted_source_rules_sha256':A['rules_sha256'],
 'owner_archive_sha256':Z['archive_sha256'],
 'new_documentary_records':24,'lilly_if_published':4508,
 'ptolemy_retained':1066,'combined_if_published':5574,
 'next_chapter':'LXXIX','next_original_pdf_page':471,
 'independently_verified_dream_outcomes':0,
 'new_empirical_predictions':0,'runtime_promotions':0,'remote_published':False}
REC.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2))
