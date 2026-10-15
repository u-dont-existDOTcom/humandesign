#!/usr/bin/env python3
"""B02z guarded historical documentary index transition (source not predictions)."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02z_CHAPTER_LIV_COMPLETE.md'
OLDCUR=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B02z.md'
OLDIDX=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B02z_CANONICAL.json'
RECEIPT=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json'
assert not any(p.exists() for p in (LATEST,OLDCUR,OLDIDX,RECEIPT))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.run(['git',*args],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()
raw=I.read_bytes()
j=json.loads(raw)
a=json.loads((B/'ACCEPTANCE.json').read_text())
rr=json.loads((B/'RULES.json').read_text())
rel=json.loads((B/'SOURCE_DOCUMENTARY_ACCEPTED_RELEASE_RECEIPT_20261015.json').read_text())
assert j['records_count']==3147 and j['batches'][-1]['id']=='B02y'
assert j['next']['chapter']=='LIV' and j['next']['pdf_page']==410
assert j['read_numbered_chapters']==list(range(1,54))
assert j['runtime_promotions']==j['empirical_validations']==0
assert all(k['id']!='B02z' for k in j['batches'])
assert a['documentary_accepted_locally'] and a['whole_chapter_liv_complete_at_documentary_source_level']
assert a['new_documentary_records']==24 and a['previous_accepted_lilly']==3147
assert rr['record_count']==24 and [r['record_number'] for r in rr['rules']]==list(range(3148,3172))
assert rr['rules'][-1]['chapter']=='LV_HEADING_NAVIGATION_ONLY'
assert a['source_uncertainties_retained']==14 and a['original_source_reverse_spans']==16
assert rel['zip_crc_pass'] and rel['file_sha256_and_bytes_pass']
assert rel['extracted_focused_test_count']==19 and rel['extracted_focused_test_exit_code']==0
assert sha(rel['archive_os_downloads'])==rel['archive_sha256']
assert sha(B/'RULES.json')==a['rules_sha256']==rel['rules_sha256']
assert sha(B/'ADMISSION_SUPERSESSION_20261015.md')
rp=str(I.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rp],cwd=ROOT).returncode==0
previous_blob=git('rev-parse','HEAD:'+rp)
assert previous_blob==git('hash-object',str(I))
j['batches'].append({'id':'B02z','path':'batches/B02z/RULES.json',
 'records_count':24,'sha256':a['rules_sha256'],
 'scope':'Book II Chapter LIV Buying and Selling Commodities, original PDF410 below prior divider through PDF411 above LV divider; 23 LIV historical source units and one next-chapter navigation marker; 16 source spans, 14 source limits, no empirical validations.'})
j['records_count']=3171
j['read_numbered_chapters'].append(54)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LIV_DOCUMENTARY_SOURCE_ONLY_NEXT_LV_OPEN'
j['next']={'pdf_page':411,'printed_page':377,'chapter':'LV','heading':'Of Partnership.',
'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
'position':'Original PDF411 BELOW horizontal divider after last Chapter LIV sale/repurchase clause; continue through subsequent pages to next numbered chapter.'}
j['chapter_LIV_source_acceptance_note']='24 original documentary annotations including LV boundary; 16 reverse source image spans and 14 retained unresolved readings. Provisional source packet preserved with former predecessor-held snapshot. 19 source tests replayed in extracted source archive, not empirical predictions.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02z_CHAPTER_LIV_COMPLETE.md'
assert j['records_count']==sum(x['records_count'] for x in j['batches'])
assert j['records_count']==3171 and j['read_numbered_chapters']==list(range(1,55))
body="""# Lilly Chapter LIV Buying and Selling Commodities — documentary original-source acceptance

2026-10-15 Africa/Dakar UTC+0 — historical source research, not confirmed astrological forecasts or financial/legal guidance.

Original 1647 William Lilly Christian Astrology, Wellcome b30338724 original PDF SHA-256: 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

Chapter LIV begins on original PDF410/printed376 BELOW the LIII divider, ends on PDF411/printed377 ABOVE the LV divider. Its original clauses cover buyer ascendant-lord/Moon, seller seventh-lord, conjunction, relative planetary lightness, translation of light, commodity-specific house assignment, benefic/malefic qualifiers, void-of-course exceptions and seller repurchase. Personal dishonesty assertions are historical, not verified.

Accepted source batch B02z: 24 editorial documentary source units (R3148–R3171), 23 from LIV plus one LV navigation marker, mapped to 16 original-page passages with 14 retained ambiguities. Original 24-row provisional draft was archived with a previous 3,071 count when LIII was pending. That earlier snapshot is **preserved, not retroactively edited**. The final B02z acceptance explicitly depends on authenticated prior LIII publication, 3,147 Lilly records.

**After remote acceptance publication:** 3,171 Lilly + 1,066 Ptolemy = 4,237 historical documentary units. 19 source-only tests replayed from verified extracted archive. Zero empirically validated astrological outcomes, trading decisions or runtime model promotions. No independent full diplomatic blind transcription claimed.

Local archive in owner's Telechargements: Astrology-Lilly-Chapter-LIV-Documentary-20261015.zip. Source ordering, archive hashes, original scans, acceptance and supersession documented in B02z.

**Next:** Chapter LV *Of Partnership*, from PDF411/printed377 below divider, using the earlier Chapter LV source-first provisional packet (32 source units) only after verifying its image and branch identity. Overall research remains OPEN.
"""
prefix="""# Current astrology source audit — latest original source checkpoint

CURRENT 2026-10-15: Lilly Chapter LIV source-accepted for documentary historical use; 3,171 Lilly + 1,066 retained Ptolemy = 4,237 original source units after authenticated publication. Next: Chapter LV Partnership original PDF411 below divider. No empirical predictive validations or runtime rule promotion. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02z_CHAPTER_LIV_COMPLETE.md and B02z admission/supersession/publication receipt.

---

"""
OLDIDX.parent.mkdir(parents=True,exist_ok=True)
OLDIDX.write_bytes(raw)
OLDCUR.write_bytes(CUR.read_bytes())
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CUR.write_text(prefix+OLDCUR.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(body,encoding='utf-8')
rec={'batch':'B02z','kind':'CANONICAL_DOCUMENTARY_SOURCE_INDEX_PREPARED_NOT_REMOTE_PUBLISHED',
 'previous_index_git_blob_sha1':previous_blob,'previous_index_sha256':sha(OLDIDX),
 'new_index_sha256':sha(I),'new_current_state_sha256':sha(CUR),
 'new_latest_state_sha256':sha(LATEST),'rules_sha256':sha(B/'RULES.json'),
 'accepted_owner_release_sha256':rel['archive_sha256'],
 'added_historical_source_units':24,'lilly_if_published':3171,
 'ptolemy_retained':1066,'combined_if_published':4237,
 'next_chapter':'LV','next_original_pdf':411,
 'new_empirical_predictive_validations':0,'runtime_promotions':0,'remote_published':False}
RECEIPT.write_text(json.dumps(rec,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(rec,indent=2,ensure_ascii=False))
