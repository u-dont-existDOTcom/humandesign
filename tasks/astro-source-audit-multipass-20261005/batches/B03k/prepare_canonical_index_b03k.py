#!/usr/bin/env python3
"""Guarded source-only Lilly LXV canonical index append; no validated forecast."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CURRENT=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03k_CHAPTER_LXV_COMPLETE.md'
OLDI=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03k_CANONICAL.json'
OLDC=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03k.md'
REC=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json'
assert not any(x.exists() for x in (LATEST,OLDI,OLDC,REC))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
original=IDX.read_bytes();j=json.loads(original)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').read_text())
assert j['records_count']==3630 and j['batches'][-1]['id']=='B03j'
assert j['next']['chapter']=='LXV' and j['next']['pdf_page']==433
assert j['read_numbered_chapters']==list(range(1,65))
assert j['empirical_validations']==j['runtime_promotions']==0
assert j['source_sha256']==A['original_pdf_sha256']
assert A['documentary_accepted_locally'] and A['whole_chapter_lxv_complete']
assert A['new_documentary_records']==40 and A['previous_lilly_accepted']==3630
assert A['lilly_if_published']==3670 and A['combined_if_published']==4736
assert A['source_reverse_passages']==10 and A['source_uncertainties_retained']==18
assert R['record_count']==40 and R['independent_letter_arrival_time_verified'] is False
assert [x['record_number'] for x in R['rules']]==list(range(3631,3671))
assert R['rules'][-1]['chapter']=='LXVI_NAVIGATION_ONLY'
assert not R['independent_battle_prediction_outcome_verified']
assert Z['zip_crc_pass'] and Z['member_hashes_match'] and Z['actual_extraction_pass']
assert Z['extracted_test_count']==19 and Z['extracted_test_exit_code']==0
assert sha(Z['download_path'])==Z['zip_sha256']
assert sha(B/'RULES.json')==A['rules_sha256']==Z['original_source_rules_sha256']
p=str(IDX.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',p],cwd=ROOT).returncode==0
oldblob=git('rev-parse','HEAD:'+p)
assert oldblob==git('hash-object',str(IDX))
assert not any(b['id']=='B03k' for b in j['batches'])
j['batches'].append({
 'id':'B03k','path':'batches/B03k/RULES.json',
 'records_count':40,'sha256':A['rules_sha256'],
 'scope':'Original Lilly 1647 Book II Chapter LXV Waller/Hopton case, PDF433 below Fish Stolen divider to PDF434 bottom, next Chapter LXVI heading PDF435. Square horoscope heading and figure both 29 March 1644, 10:12 AM. 39 source clauses plus one next heading, ten original-image passage groups, eighteen uncertainties. Author claims favorable news within 11–12h and a Friday letter; arrival time unverified, victory qualified incomplete.'})
j['records_count']=3670
j['read_numbered_chapters'].append(65)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LXV_DOCUMENTARY_SOURCE_ONLY_NEXT_LXVI_OPEN'
j['next']={'pdf_page':435,'printed_page':401,'chapter':'LXVI',
 'printed_chapter_numeral':'LXVI',
 'heading':'If his Excellency Robert Earl of Essex should take Reading, having it surrounded with his army',
 'include_opening_paragraph':True,'extracted':False,
 'boundary_image_read':True,
 'position':'Original PDF435/printed401 starts a new numbered chapter at page top; original Chapter LXV ends bottom PDF434. Reading siege figure dated 17 April 1643 is a separate case.'}
j['chapter_LXV_source_acceptance_note']='40 historical editorial source units (39 LXV and one LXVI heading), 10 visual-source passages and 18 limitations. Enlarged original reads 29 Mar 1644, 10:12 AM, not May. Author-predicted 11–12 hour favorable news is not verified because letter arrival clock is unreported. Outcome letter and prisoner counts are source-internal, with explicit incomplete victory qualification.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03k_CHAPTER_LXV_COMPLETE.md'
assert sum(b['records_count'] for b in j['batches'])==j['records_count']==3670
assert j['read_numbered_chapters']==list(range(1,66))
state="""# Lilly 1647 Chapter LXV — Waller/Hopton original wartime horary, documentary acceptance

2026-10-15 Africa/Dakar UTC+0. Original William Lilly Christian Astrology 1647 Wellcome b30338724, complete original PDF SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

Chapter LXV begins on original PDF433/printed399 BELOW the Fish Stolen divider and runs through PDF434/printed400. Chapter LXVI on Essex taking Reading begins at original PDF435/printed401, a separate worked case. The enlarged original battle chart unequivocally reads **29 March 1644, 10:12 AM**; the heading also dates 29 March, not May.

Lilly assigns the ascendant to his parliamentary army, Moon/Jupiter/Venus to Waller and Major General Browne, and seventh-house Saturn to Ralph Hopton. He favors his own side but expressly qualifies that victory could be incomplete. The Moon is said to apply to Venus and then by sextile to Mercury; the author reports predicting favorable news within **eleven or twelve hours**. He next narrates a Friday army letter referring to Thursday capture of 120 commanders, 560 soldiers and ammunition. The source gives no independently verified letter arrival CLOCK TIME, no authenticated letter copy and no independent frozen prediction, so **precise timing success is NOT established**. Alleged prior achievements from Moon-Jupiter separation are also not prospective forecasts.

**B03k source acceptance:** 40 historical documentary units R3631–R3670 (39 Chapter LXV source assertions plus one Chapter LXVI navigation marker), ten primary-source reverse passages and eighteen original chart/provenance limits. No full second blind diplomatic transcription, no independently checked ephemeris, and no combat advice.

**After authenticated publication:** Lilly **3,670** + retained Ptolemy **1,066** = **4,736** historical documentary records. Independently validated astrology forecasts added: zero. Runtime model promotions: zero. The accepted ZIP has original scans, maps, hash manifest and 19 extracted replay tests: Astrology-Lilly-Chapter-LXV-Waller-Hopton-Documentary-20261015.zip in the owner's designated Downloads folder.

**NEXT:** Book II Chapter LXVI, Essex and Reading siege, begins PDF435/printed401 at the chapter heading. Separate original figure dated 17 April 1643 with outcome reported on 27 April must be historically sourced, not folded into LXV. Parent multi-author astrology source research remains OPEN.
"""
prefix="""# Original source audit current — Chapter LXV

Lilly Chapter LXV historical source accepted: 3,670 Lilly plus 1,066 Ptolemy, combined 4,736 after publication. Next Chapter LXVI begins original PDF435/printed401. No independently validated forecast; research continues.

---

"""
OLDI.parent.mkdir(parents=True,exist_ok=True)
OLDI.write_bytes(original)
OLDC.write_bytes(CURRENT.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CURRENT.write_text(prefix+OLDC.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(state,encoding='utf-8')
receipt={'batch':'B03k',
 'kind':'GUARDED_LOCAL_HISTORICAL_SOURCE_INDEX_PREPARED',
 'previous_index_git_blob_sha1':oldblob,
 'old_index_sha256':sha(OLDI),'new_index_sha256':sha(IDX),
 'new_current_sha256':sha(CURRENT),'new_latest_sha256':sha(LATEST),
 'rules_sha256':A['rules_sha256'],
 'release_archive_sha256':Z['zip_sha256'],
 'new_documentary_units':40,'lilly_if_published':3670,
 'ptolemy_retained':1066,'combined_if_published':4736,
 'next_chapter':'LXVI','next_pdf_page':435,
 'independent_news_timing_validations':0,
 'empirical_predictions_validated':0,'runtime_promotions':0,
 'remote_published':False}
REC.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
