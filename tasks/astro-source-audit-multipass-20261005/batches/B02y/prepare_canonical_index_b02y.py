#!/usr/bin/env python3
"""Guarded source-only Chapter LIII index integration in isolated branch."""
from pathlib import Path
import hashlib,json,subprocess

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CURRENT=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02y_CHAPTER_LIII_COMPLETE.md'
OLDINDEX=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B02y_CANONICAL.json'
OLDCURRENT=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B02y.md'
RECEIPT=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json'
assert not any(p.exists() for p in (LATEST,OLDINDEX,OLDCURRENT,RECEIPT))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.run(['git',*args],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()
raw=I.read_bytes();j=json.loads(raw)
a=json.loads((B/'ACCEPTANCE.json').read_text())
r=json.loads((B/'RULES.json').read_text())
p=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_PACKET_RECEIPT_20261015.json').read_text())
assert j['records_count']==3071 and j['batches'][-1]['id']=='B02x'
assert j['read_numbered_chapters']==list(range(1,53))
assert j['next']['chapter']=='LIII' and j['next']['pdf_page']==405
assert j['runtime_promotions']==0 and j['empirical_validations']==0
assert a['documentary_accepted_locally'] and a['whole_chapter_liii_complete_at_documentary_source_level']
assert a['new_documentary_records']==76 and a['lilly_if_published']==3147
assert p['zip_integrity_pass'] and p['extracted_all_file_sha256_pass']
assert p['extracted_focused_source_test_count']==19 and p['extracted_source_tests_exit_code']==0
assert sha(p['archive_os_downloads'])==p['archive_sha256']
assert a['rules_sha256']==sha(B/'RULES.json')==p['source_first_rules_sha256']
assert r['record_count']==76 and [x['record_number'] for x in r['rules']]==list(range(3072,3148))
assert r['rules'][-1]['record_role']=='next_heading_boundary'
assert sum(x['chapter']=='LIII' for x in r['rules'])==75
assert not r['accepted_as_empirical_astro_prediction'] and r['runtime_promotions']==0
rel=str(I.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rel],cwd=ROOT).returncode==0
old_git_blob=git('rev-parse','HEAD:'+rel)
assert git('hash-object',str(I))==old_git_blob
assert all(b['id']!='B02y' for b in j['batches'])
j['batches'].append({
 'id':'B02y','path':'batches/B02y/RULES.json',
 'records_count':76,'sha256':a['rules_sha256'],
 'scope':'Book II Chapter LIII hunting then unnumbered lawsuit/judge/mediation section; original PDF405 below LII divider through PDF410 above LIV divider; 75 LIII source annotations and one LIV navigation marker, 27 reverse source passages, 16 limits; historical text only.'})
j['records_count']=3147
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LIII_DOCUMENTARY_SOURCE_ONLY_NEXT_LIV_OPEN'
j['read_numbered_chapters'].append(53)
j['next']={'pdf_page':410,'printed_page':376,'chapter':'LIV',
           'heading':'Of Buying and Selling Commodities.',
           'include_opening_paragraph':True,'extracted':False,
           'boundary_image_read':True,
           'position':'Original PDF410 BELOW horizontal divider after final LIII Moon application/separation note; complete original chapter continues PDF411 until LV divider.'}
j['chapter_LIII_source_acceptance_note']='76 historical editorial documentary units (75 LIII and one LIV heading marker), six original-page scans, 27 visually reviewed original source spans, 16 retained interpretive limits. Did not conduct independent blind diplomatic second transcription. No real litigant or hunting outcome, astrology prediction, or runtime model validation.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02y_CHAPTER_LIII_COMPLETE.md'
assert j['records_count']==sum(b['records_count'] for b in j['batches'])==3147
assert j['read_numbered_chapters']==list(range(1,54))
body="""# Lilly Book II Chapter LIII — original documentary source accepted

2026-10-15 Africa/Dakar (UTC+0). Parent multi-author astrology source study OPEN.
Only original textual/astrological claims have been documented; this is not empirical confirmation, legal advice, an accusation of actual judicial misconduct, or live prediction-model promotion.

Original 1647 William Lilly Christian Astrology, Wellcome b30338724 PDF SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

LIII begins on original PDF405/printed371 BELOW the LII/LIII divider, continues through PDF406–409, and ends on original PDF410/printed376 ABOVE the LIII/LIV divider. It contains initial hunting rules and a long unnumbered lawsuit or controversy section, including opposing litigants, judge, mediator, reception, Saturn, sign modality, favorable and difficult aspects. Chapter LIV buying/selling starts below the divider.

New B02y locally source-admitted historical documentary units: 76 (R3072–R3147). This includes 75 LIII text/heading/marginal records and one next-chapter navigation marker. The original-to-record source map contains 27 passage groups; 16 unresolved textual or operational limits preserved; three original page crossings. All six source scan hashes are frozen. No independent full diplomatic second-reader transcription is claimed.

Canonical after authenticated publication: 3,147 Lilly + 1,066 retained Ptolemy = 4,213 historical documentary units. Zero empirical predictive confirmations, real hunting cases, authenticated litigation outcomes, accuracy evidence, or runtime model changes.

Archive in owner's French Telechargements: Astrology-Lilly-Chapter-LIII-Documentary-20261015.zip, mechanically re-extracted and its 19 focused source tests replayed. See B02y source-first original scan manifest, correction ledger, source rules, reverse source coverage, local admission and final GitHub publication receipt for identity.

NEXT: Chapter LIV Buying and Selling Commodities from original PDF410 below divider through PDF411 above Chapter LV divider. An existing B02z provisional packet (24 source units) must be read back against these pages, corrected where necessary, then source-admitted. Chapter LV is likewise provisional until LIV is accepted. Do not infer astrology's predictive validity from source study.
"""
prefix="""# Current astrology source audit — latest historical corpus checkpoint

CURRENT (2026-10-15): Lilly Book II Chapter LIII documentary source admission (B02y), 3,147 Lilly + 1,066 Ptolemy = 4,213 historical units after authenticated publication. Next Chapter LIV begins PDF410/printed376 BELOW divider. No empirical prediction verification or runtime promotion; overall research OPEN. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02y_CHAPTER_LIII_COMPLETE.md, B02y acceptance/receipt, and canonical index.

---

"""
OLDINDEX.parent.mkdir(parents=True,exist_ok=True)
OLDINDEX.write_bytes(raw)
OLDCURRENT.write_bytes(CURRENT.read_bytes())
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CURRENT.write_text(prefix+OLDCURRENT.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(body,encoding='utf-8')
rec={'batch':'B02y','kind':'CANONICAL_DOCUMENTARY_SOURCE_INDEX_PREPARED_NOT_YET_REMOTE_PUBLISHED',
     'previous_index_git_blob_sha1':old_git_blob,'previous_index_sha256':sha(OLDINDEX),
     'new_index_sha256':sha(I),'new_current_state_sha256':sha(CURRENT),
     'new_latest_state_sha256':sha(LATEST),'rules_sha256':a['rules_sha256'],
     'owner_release_sha256':p['archive_sha256'],'new_documentary_units':76,
     'lilly_if_published':3147,'ptolemy_retained':1066,'combined_if_published':4213,
     'next_chapter':'LIV','next_original_pdf':410,
     'empirical_predictions_validated':0,'runtime_promotions':0,'remote_published':False}
RECEIPT.write_text(json.dumps(rec,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(rec,indent=2,ensure_ascii=False))
