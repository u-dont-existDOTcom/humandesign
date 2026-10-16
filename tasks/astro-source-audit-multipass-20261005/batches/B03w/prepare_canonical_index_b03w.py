#!/usr/bin/env python3
"""Guarded Lilly original historical dream source integration."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03w_CHAPTER_LXXVII_COMPLETE.md'
OLD=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03w_CANONICAL.json'
OLDCUR=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03w.md'
REC=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json'
assert not any(p.exists() for p in (LATEST,OLD,OLDCUR,REC))
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes();j=json.loads(raw)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').read_text())
assert j['records_count']==4446 and j['batches'][-1]['id']=='B03v'
assert j['next']['chapter']=='LXXVII' and j['next']['pdf_page']==468
assert j['read_numbered_chapters']==list(range(1,77))
assert j['source_sha256']==A['source_original_pdf_sha256']
assert j['empirical_validations']==j['runtime_promotions']==0
assert not any(k['id']=='B03w' for k in j['batches'])
assert A['documentary_accepted_locally'] and A['prior_lilly_accepted']==4446
assert A['new_documentary_records']==38 and A['lilly_if_published']==4484
assert A['combined_if_published']==5550
assert R['record_count']==38 and R['independently_verified_dream_outcomes']==0
assert [r['record_number'] for r in R['rules']]==list(range(4447,4485))
assert all(r['chapter']=='LXXVIII_NAVIGATION_ONLY' for r in R['rules'][-2:])
assert Z['zip_crc_pass'] and Z['member_hashes_pass'] and Z['full_extraction_pass']
assert Z['extracted_tests_passed']==15 and Z['extracted_exit_code']==0
assert sha(Z['owner_download_path'])==Z['archive_sha256']
assert sha(B/'RULES.json')==A['rules_sha256']==Z['accepted_rules_sha256']
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rel],cwd=ROOT).returncode==0
old_blob=git('rev-parse','HEAD:'+rel)
assert old_blob==git('hash-object',str(IDX))
j['batches'].append({'id':'B03w','path':'batches/B03w/RULES.json',
 'records_count':38,'sha256':A['rules_sha256'],
 'scope':'Original William Lilly 1647 Book II LXXVII generic dream interpretation on original PDF468 lower part through PDF469; next LXXVIII dated worked dream starts PDF470. 36 substantive historical dream clauses plus two following-chapter navigation markers, eight original source passages, fifteen unresolved source limits. No independently authenticated dream/harm/psychological prediction.'})
j['records_count']=4484
j['read_numbered_chapters'].append(77)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LXXVII_HISTORICAL_SOURCE_ONLY_NEXT_LXXVIII_OPEN'
j['next']={'pdf_page':470,'printed_page':436,'chapter':'LXXVIII',
 'printed_chapter_numeral':'LXXVIII','heading':'Terrible Dreams',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF470/printed436 new square horoscope dated 26 January 1648 at 9:27 AM. LXXVII closes end of original PDF469/printed435.'}
j['chapter_LXXVII_source_acceptance_note']='38 original source annotations R4447-R4484 (36 LXXVII substantive plus two LXXVIII next-heading navigation), eight original source passages with one page seam and 15 textual uncertainties. Generic dreams source only; no independently verified dream event or validated prediction.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03w_CHAPTER_LXXVII_COMPLETE.md'
assert j['records_count']==sum(x['records_count'] for x in j['batches'])==4484
assert j['read_numbered_chapters']==list(range(1,78))
REPORT="""# William Lilly (1647) Chapter LXXVII — dream interpretation original-source study

2026-10-16 Africa/Dakar UTC+0. Original witness: William Lilly *Christian Astrology* (1647), Wellcome b30338724, source full PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

Original Chapter LXXVII *Of Dreams; whether they signifie any thing or not?* begins **below** the divider on PDF468/printed434. It continues on PDF469/printed435, ending before the separate **Chapter LXXVIII Terrible Dreams**, which begins PDF470/printed436 with a square horoscope dated 26 January 1648 at 9:27 AM.

The source offers historical dream interpretation based on ninth-house planets, Saturn and lunar-node symbolism, Capricorn/Aquarius positions, and derived house themes such as money, relatives, and neighbors. If ninth is empty it prescribes a particular sequence of fallback houses. It separately asserts possible bodily trouble from an adverse ninth-to-first-lord aspect, financial trouble from adverse ninth-to-second-lord aspects, and allegedly protective benefics in ninth or first or favorable aspects from first lord.

These are historical astrological claims, not independent evidence of physical threat, future harm, or psychological states. No prospectively frozen identifiable dream case or independently authenticated outcome appears in this generic chapter. The distinct LXXVIII dated worked case is not imported.

**Documentary acceptance:** 38 source annotations R4447-R4484 (36 chapter clauses plus two LXXVIII navigation markers), eight original-image source passage groups including one page seam and fifteen retained interpretive limits. The three original JPEG witnesses are separately SHA256 frozen; no complete independent diplomatic transcription or modern chart recalculation claimed.

**After authenticated publication:** Lilly **4,484** and retained Ptolemy **1,066** = **5,550 combined historical documentary records**. New independent empirical astrological predictions **zero**; runtime model changes **zero**.

Owner ZIP: Astrology-Lilly-Chapter-LXXVII-Dreams-Documentary-20261016.zip in Downloads, CRC, member SHA-256 and full extraction with 15 replayed focused tests passed. Parent research OPEN.

**NEXT:** Chapter LXXVIII *Terrible Dreams*, separate square figure dated 26 January 1648 9:27 AM on original PDF470, continues through true following chapter divider to be located from original images.
"""
PREFIX="""# Current original Lilly source study — Chapter LXXVII

CURRENT 2026-10-16: Chapter LXXVII generic dreams source accepted. After authenticated publication Lilly 4,484 + retained Ptolemy 1,066 = 5,550 historical documentary source units. Next LXXVIII worked dream case begins original PDF470/printed436. No independently verified dream case or empirical prediction; zero runtime rule promotions. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03w_CHAPTER_LXXVII_COMPLETE.md.

---

"""
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw)
OLDCUR.write_bytes(CUR.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CUR.write_text(PREFIX+OLDCUR.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(REPORT,encoding='utf-8')
receipt={'batch':'B03w','status':'GUARDED_HISTORICAL_SOURCE_INDEX_PREPARED_NOT_REMOTE',
 'prior_index_git_blob_sha1':old_blob,
 'previous_index_sha256':sha(OLD),'new_index_sha256':sha(IDX),
 'current_state_sha256':sha(CUR),'latest_state_sha256':sha(LATEST),
 'accepted_source_rules_sha256':A['rules_sha256'],
 'owner_archive_sha256':Z['archive_sha256'],
 'new_documentary_records':38,'lilly_if_published':4484,
 'ptolemy_retained':1066,'combined_if_published':5550,
 'next_chapter':'LXXVIII','next_original_pdf_page':470,
 'independently_verified_dream_outcomes':0,
 'new_empirical_predictions':0,'runtime_promotions':0,
 'remote_published':False}
REC.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
