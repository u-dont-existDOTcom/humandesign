#!/usr/bin/env python3
"""Guarded canonical original-source index transition: logical LXIV / printed LIV."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CURRENT=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03j_FISH_STOLEN_COMPLETE.md'
PREVIOUS= B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03j_CANONICAL.json'
PREVIOUS_CURRENT=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03j.md'
PREPARE=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json'
assert not any(x.exists() for x in (LATEST,PREVIOUS,PREVIOUS_CURRENT,PREPARE))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes()
j=json.loads(raw)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').read_text())
assert j['records_count']==3571 and j['batches'][-1]['id']=='B03i'
assert j['next']['chapter']=='LXIV' and j['next']['printed_chapter_numeral']=='LIV'
assert j['next']['pdf_page']==431
assert j['read_numbered_chapters']==list(range(1,64))
assert j['empirical_validations']==0 and j['runtime_promotions']==0
assert j['source_sha256']==A['source_full_pdf_sha256']
assert not any(x['id']=='B03j' for x in j['batches'])
assert A['documentary_accepted_locally'] and A['whole_chapter_lxiv_source_intake_complete']
assert A['new_documentary_records']==59 and A['previous_accepted_lilly']==3571
assert A['lilly_if_published']==3630 and A['combined_if_published']==4696
assert A['retained_source_uncertainties']==20 and A['source_reverse_spans']==18
assert R['record_count']==59
assert [r['record_number'] for r in R['rules']]==list(range(3572,3631))
assert R['rules'][-1]['chapter_logical']=='LXV_NAVIGATION_ONLY'
assert R['author_reported_partial_fish_recovery_cases']==1
assert R['author_reported_full_fish_recovery_cases']==0
assert not R['independent_blind_full_diplomatic_transcription_done']
assert Z['zip_crc_pass'] and Z['all_member_hashes_match'] and Z['actual_extraction_pass']
assert Z['extracted_focused_tests_passed']==21 and Z['extracted_test_exit_code']==0
assert sha(Z['owner_os_download_path'])==Z['release_zip_sha256']
assert sha(B/'RULES.json')==A['rules_sha256']==Z['accepted_rules_sha256']
rel_path=str(IDX.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rel_path],cwd=ROOT).returncode==0
old_blob=git('rev-parse','HEAD:'+rel_path)
assert git('hash-object',str(IDX))==old_blob
j['batches'].append({
 'id':'B03j','path':'batches/B03j/RULES.json',
 'records_count':59,'sha256':A['rules_sha256'],
 'scope':'Lilly 1647 Book II Fish Stolen printed CHAP LIV but sequential LXIV. Original PDF431-433 above LXV divider, own dated 10 February 1638 square chart; 58 Fish Stolen original editorial source units plus one LXV heading, 18 reverse-image source passages, 20 source uncertainties. Original author reports partial fish recovery, remainder relinquished; no independently verified predictive case.'})
j['records_count']=3630
j['read_numbered_chapters'].append(64)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LOGICAL_LXIV_DOCUMENTARY_SOURCE_ONLY_NEXT_LXV_OPEN'
j['next']={
 'pdf_page':433,'printed_page':399,'chapter':'LXV',
 'printed_chapter_numeral':'LXV',
 'heading':'A Figure erected to know whether Sir William Waller or Sir Ralph Hopton should overcome',
 'include_opening_paragraph':True,'extracted':False,
 'boundary_image_read':True,
 'position':'Original PDF433 printed399 BELOW horizontal divider following Fish Stolen conclusion. Preserve preceding printed CHAP LIV numbering anomaly as logical LXIV. Next battle horoscope printed date/figure require separate original diagram review.'}
j['chapter_LXIV_source_acceptance_note']='Source printed CHAP LIV Fish Stolen after LXIII; logically LXIV, distinct from earlier Book II LIV buying/selling. 59 historical source units including one LXV heading, 18 source-image passages, 20 source limitations. Author reported partial fish recovery, remainder relinquished; negative discovery-without-recovery rule retained. No independent case authentication or runtime algorithm promotion.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03j_FISH_STOLEN_COMPLETE.md'
assert j['records_count']==sum(b['records_count'] for b in j['batches'])==3630
assert j['read_numbered_chapters']==list(range(1,65))
newstate="""# William Lilly Chapter Fish Stolen — original documentary source accepted

2026-10-15 Africa/Dakar UTC+0. Original witness: William Lilly, Christian Astrology (1647), Wellcome b30338724 original full PDF SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

**ORIGINAL HEADING NUMBER ANOMALY:** The section is printed CHAP. LIV. Fish Stolen. at PDF431/printed397 after Chapter LXIII, so its logical sequential identity is LXIV. The earlier true LIV Buying/Selling is completely different; neither is silently renumbered. Source section ends on original PDF433/printed399 ABOVE the next Chapter LXV divider.

A separate original square figure is dated **10 February 1638, 8:45 AM** as printed. Source prose describes fish ordered in London for Lent, warehoused in Walton, reported stolen and investigated after a consultation figure. The author describes watery signs and a predicted boatman/fisherman occupation, finds no fitting boatman initially, then targets a fisherman with an alleged change of residence, obtains a warrant, searches one house on 18 February, and reports **PARTIAL fish recovery**: fish in water, fish eaten, fish remaining, plus disputes about the sack and onions. He says he waived the remaining fish. No independent witness, inventory, confession or case record is authenticated.

Before the Chapter LXV divider the text also gives a three-way conditional distinction: full recovery with essential dignity of both Moon and second-house lord, partial recovery with accidental fortification, and discovery-without-recovery if both are peregrine. These are historical source assertions, not empirically confirmed astrological laws.

**B03j admission:** 59 editorial source records R3572–R3630 (58 Fish Stolen body records plus one LXV navigation-only marker); 18 original visual passage groups including two cross-page groups; 20 original-source limitations retained. No independently blind complete diplomatic second transcription and no ephemeris parity. The personal descriptions and claims about wrongdoing are not factual allegations certified by this project.

**After authenticated GitHub research branch publication:** Lilly **3,630** + retained Ptolemy **1,066** = **4,696 historical documentary source annotations**. No new independently authenticated theft cases, validated astrology predictions or runtime model promotions.

Release ZIP in owner's designated Downloads: Astrology-Lilly-Chapter-LXIV-Fish-Stolen-Documentary-20261015.zip. Its CRC, all-member SHA256, actual extraction and 21 focused tests were replayed before source-index integration.

**NEXT:** Book II Chapter LXV, historical Waller/Hopton battle figure and judgment, starts PDF433/printed399 BELOW Fish Stolen divider. Original figure and chronology need a separate source-first audit. Parent book-source/empirical study remains OPEN.
"""
prefix="""# Astrology source audit — latest original historical text checkpoint

CURRENT 2026-10-15: Lilly Book II *Fish Stolen*, originally PRINTED Chapter LIV but logically LXIV, admitted as original-source documentary research. After authenticated publication: 3,630 Lilly + 1,066 retained Ptolemy = 4,696 source annotations. Following Chapter LXV battle figure begins original PDF433/printed399 below the Fish Stolen divider. Zero empirically validated predictions and zero runtime rule changes. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03j_FISH_STOLEN_COMPLETE.md and B03j source/release/publication evidence.

---

"""
PREVIOUS.parent.mkdir(parents=True,exist_ok=True)
PREVIOUS.write_bytes(raw)
PREVIOUS_CURRENT.write_bytes(CURRENT.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CURRENT.write_text(prefix+PREVIOUS_CURRENT.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(newstate,encoding='utf-8')
receipt={
 'batch':'B03j',
 'kind':'GUARDED_HISTORICAL_SOURCE_INDEX_PREPARED_NOT_REMOTELY_PUBLISHED',
 'previous_source_index_git_blob_sha1':old_blob,
 'original_parent_index_sha256':sha(PREVIOUS),
 'new_source_index_sha256':sha(IDX),
 'new_current_state_sha256':sha(CURRENT),
 'new_latest_state_sha256':sha(LATEST),
 'accepted_source_rules_sha256':A['rules_sha256'],
 'owner_release_zip_sha256':Z['release_zip_sha256'],
 'documentary_source_units_added':59,
 'lilly_if_published':3630,'retained_ptolemy':1066,
 'combined_if_published':4696,
 'next_logical_chapter':'LXV','next_original_pdf':433,
 'printed_original_chapter_number':'LIV',
 'new_empirical_predictions_validated':0,
 'runtime_model_promotions':0,
 'remotely_published':False}
PREPARE.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
