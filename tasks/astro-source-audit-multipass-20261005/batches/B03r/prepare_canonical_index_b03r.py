#!/usr/bin/env python3
"""Guarded canonical original-source index append: Lilly LXXII Canterbury."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03r_CHAPTER_LXXII_COMPLETE.md'
OLDI=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03r_CANONICAL.json'
OLDC=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03r.md'
PREP=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json'
assert not any(p.exists() for p in (LATEST,OLDI,OLDC,PREP))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
old_bytes=IDX.read_bytes(); j=json.loads(old_bytes)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').read_text())
assert j['records_count']==4093 and j['batches'][-1]['id']=='B03q'
assert j['next']['chapter']=='LXXII' and j['next']['pdf_page']==453
assert j['read_numbered_chapters']==list(range(1,72))
assert j['source_sha256']==json.loads((B/'SOURCE_WINDOW_MANIFEST.json').read_text())['original_full_pdf_sha256']
assert j['empirical_validations']==0 and j['runtime_promotions']==0
assert all(x['id']!='B03r' for x in j['batches'])
assert A['new_documentary_records']==43 and A['lilly_if_published']==4136
assert A['combined_if_published']==5202 and A['previous_lilly']==4093
assert R['record_count']==43 and R['independent_historical_execution_event_confirmed']==1
assert R['independent_prospective_astro_forecasts_verified']==0
assert [r['record_number'] for r in R['rules']]==list(range(4094,4137))
assert R['rules'][-1]['chapter']=='LXXIII_NAVIGATION_ONLY'
assert Z['zip_crc_pass'] and Z['member_hashes_pass'] and Z['actual_extraction_pass']
assert Z['extracted_replay_tests_passed']==12 and Z['replay_exit_code']==0
assert H(Z['owner_download_path'])==Z['archive_sha256']
assert H(B/'RULES.json')==A['rules_sha256']==Z['rules_sha256']
relative=str(IDX.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',relative],cwd=ROOT).returncode==0
old_blob=git('rev-parse','HEAD:'+relative)
assert old_blob==git('hash-object',str(IDX))
j['batches'].append({
 'id':'B03r','path':'batches/B03r/RULES.json','records_count':43,
 'sha256':A['rules_sha256'],
 'scope':'Original 1647 Lilly Book II LXXII Archbishop of Canterbury chart printed 3 Dec 1644 2:24 PM; 42 chapter source annotations plus one next LXXIII heading, original PDF453-454 and boundary PDF455, 11 original passage groups, 18 limits. Independent Bodleian confirms execution 10 Jan 1645, but no independent forecast manuscript; source claims not hanging, other noble mode, 6-7 weeks or thereabouts, actual interval 38 days.'})
j['records_count']=4136
j['read_numbered_chapters'].append(72)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LXXII_HISTORICAL_DOCUMENTARY_ONLY_NEXT_LXXIII_OPEN'
j['next']={'pdf_page':455,'printed_page':421,'chapter':'LXXIII',
 'printed_chapter_numeral':'LXXIII',
 'heading':'If have the Portion promised?',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF455/printed421 next distinct numbered source on wife portion with a separate 13 July 1634 6:15 PM horoscope, continuing onto PDF456.'}
j['chapter_LXXII_source_acceptance_note']=(
 '43 source documentary annotations R4094-R4136 (42 substantive plus next heading), '
 '11 original page passages, 18 limits. Bodleian corroborates beheading 10 Jan 1645, '
 'but a prospective December 1644 astrology forecast is NOT independently authenticated; '
 'source gives approximate six/seven weeks or thereabouts while event is 38 elapsed days. '
 'No verified predictions or runtime promotions.')
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03r_CHAPTER_LXXII_COMPLETE.md'
assert j['records_count']==sum(x['records_count'] for x in j['batches'])==4136
assert j['read_numbered_chapters']==list(range(1,73))
report="""# Original Lilly Chapter LXXII — Canterbury historical source

2026-10-16 Africa/Dakar UTC+0. Witness: William Lilly Christian Astrology first edition 1647, Wellcome b30338724, original complete PDF SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

The separate original chapter runs PDF453-454 (printed419-420), with the following distinct Chapter LXXIII on original PDF455. A circular horoscope prints **3 December 1644, 2:24 PM**. Lilly interprets Capricorn on the cleric's derived ascendant, Saturn in fall, the Moon separating Saturn and applying opposition Sun, and Sun applying opposition Mars.

Lilly reports forecasting that the Archbishop of Canterbury would **not be hanged**, would experience another kind of death deemed more noble, approximately **six or seven weeks or thereabouts** later. He then reports beheading around the tenth of January. Oxford Bodleian Archives' Laudian Collection confirms **10 January 1645** as actual beheading date. This is **38 days** after 3 December 1644, short of a strict six-week minimum. His source did not explicitly name beheading in the forecast, and the approximate tolerance is undefined. The book was published after the execution, and no independently frozen December 1644 prediction record or control baseline is supplied.

Chapter LXXII also contains the author's political, moral, and emotional statements about Laud and Parliament. Such statements remain attributed opinions, not verified personal traits or astrological evidence.

Accepted B03r documentary records: **43** (R4094-R4136), 11 original-image passages and 18 unresolved source limitations. Historical execution event independently confirmed: **one**. Independently authenticated prospective astrological forecasts: **zero**. No runtime model promotion.

After authenticated research publication: Lilly **4,136** plus retained Ptolemy **1,066** = **5,202** historical source annotations. Owner-local archive Astrology-Lilly-Chapter-LXXII-Canterbury-Documentary-20261016.zip, CRC, all member hashes, full extraction and 12 original-source tests replayed.

NEXT Chapter LXXIII: If have the Portion promised? Original PDF455/printed421 starts a new 13 July 1634 chart. Research OPEN.
"""
PREFIX="""# Current original astrology source study through Chapter LXXII

CURRENT 2026-10-16: Lilly Chapter LXXII Canterbury historical source accepted, historical beheading independently dated but astrology forecast unverified. After publication Lilly 4,136 + Ptolemy 1,066 = 5,202 documentary units. Next LXXIII original PDF455. Zero empirical validations or runtime promotions. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03r_CHAPTER_LXXII_COMPLETE.md.

---

"""
OLDI.parent.mkdir(parents=True,exist_ok=True)
OLDI.write_bytes(old_bytes)
OLDC.write_bytes(CUR.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
CUR.write_text(PREFIX+OLDC.read_text())
LATEST.write_text(report)
receipt={'batch':'B03r','status':'GUARDED_HISTORICAL_SOURCE_INDEX_PREPARED_NOT_REMOTE',
 'original_predecessor_git_blob':old_blob,
 'old_index_sha256':H(OLDI),'new_index_sha256':H(IDX),
 'new_current_sha256':H(CUR),'new_latest_sha256':H(LATEST),
 'rules_sha256':A['rules_sha256'],
 'owner_archive_sha256':Z['archive_sha256'],
 'new_documentary_records':43,'lilly_if_published':4136,
 'ptolemy_retained':1066,'combined_if_published':5202,
 'next_chapter':'LXXIII','next_original_pdf':455,
 'independent_historical_execution_date_confirmed':True,
 'independent_prospective_forecast_confirmed':False,
 'new_empirical_validations':0,'runtime_promotions':0,
 'remote_published':False}
PREP.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
