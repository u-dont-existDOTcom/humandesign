#!/usr/bin/env python3
"""Guarded original-source acceptance for Chapter LV; not an empirical model change."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03a_CHAPTER_LV_COMPLETE.md'
OLDI=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03a_CANONICAL.json'
OLDC=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03a.md'
RECEIPT=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json'
assert not any(x.exists() for x in (LATEST,OLDI,OLDC,RECEIPT))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
original=I.read_bytes()
j=json.loads(original)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
rel=json.loads((B/'SOURCE_DOCUMENTARY_ACCEPTED_RELEASE_RECEIPT_20261015.json').read_text())
assert j['records_count']==3171 and j['batches'][-1]['id']=='B02z'
assert j['next']['chapter']=='LV' and j['next']['pdf_page']==411
assert j['read_numbered_chapters']==list(range(1,55))
assert j['runtime_promotions']==j['empirical_validations']==0
assert all(x['id']!='B03a' for x in j['batches'])
assert A['documentary_accepted_locally'] and A['new_documentary_records']==32
assert A['previous_accepted_lilly']==3171 and A['lilly_if_published']==3203
assert A['source_uncertainties_retained']==16 and A['original_source_reverse_spans']==17
assert R['record_count']==32
assert [r['record_number'] for r in R['rules']]==list(range(3172,3204))
assert R['rules'][-1]['chapter']=='LVI_BOUNDARY_ONLY'
assert all(r['chapter']=='LV' for r in R['rules'][:-1])
assert sha(B/'RULES.json')==A['rules_sha256']==rel['rules_sha256']
assert rel['zip_crc_pass'] and rel['file_sha256_and_bytes_pass']
assert rel['extracted_focused_test_count']==18 and rel['extracted_focused_test_exit_code']==0
assert sha(rel['archive_os_downloads'])==rel['archive_sha256']
assert (B/'ADMISSION_SUPERSESSION_20261015.md').exists()
idx_rel=str(I.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',idx_rel],cwd=ROOT).returncode==0
prevblob=git('rev-parse','HEAD:'+idx_rel)
assert git('hash-object',str(I))==prevblob
j['batches'].append({'id':'B03a','path':'batches/B03a/RULES.json',
 'records_count':32,'sha256':A['rules_sha256'],
 'scope':'Book II Chapter LV Partnership: original PDF411 below LIV divider to PDF413 above LVI divider; 31 original LV source assertions and one next-chapter navigation marker; 17 source spans, 16 retained limits; historical text only.'})
j['records_count']=3203
j['read_numbered_chapters'].append(55)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LV_DOCUMENTARY_SOURCE_ONLY_NEXT_LVI_OPEN'
j['next']={'pdf_page':413,'printed_page':379,'chapter':'LVI',
'heading':'Whether a City, Towne or Castle, besieged, or to be besieged, shall be taken or not.',
'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
'position':'Original PDF413 BELOW divider after final LV partnership condition; siege opening continues through original source pages.'}
j['chapter_LV_source_acceptance_note']='32 historical source units including LVI navigation marker, 17 source passages, 16 original text limits; original three-page scan hashes and original provisional ZIP manifest preserved. No independently blinded full diplomatic transcription, predictive accuracy evidence or model changes.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03a_CHAPTER_LV_COMPLETE.md'
assert sum(b['records_count'] for b in j['batches'])==j['records_count']==3203
assert j['read_numbered_chapters']==list(range(1,56))
state="""# Lilly Chapter LV Partnership — documentary source acceptance

2026-10-15 Africa/Dakar UTC+0. William Lilly 1647 Christian Astrology original Wellcome b30338724, verified full original PDF SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

The original Chapter LV starts after the divider on original PDF411/printed377, continues all of PDF412/printed378 and closes on PDF413/printed379 **above** the divider for Chapter LVI. The source concerns partnership significators, relevant planetary aspects, reception, sign modalities, trust claims, Moon separation/application and economic houses. The original authorial conjectures concerning deceit, unpaid debts and partnership trust are **not** independent observational evidence, legal judgment or personal diagnosis.

**Accepted source batch B03a: 32 historical documentary units R3172–R3203**, including 31 Chapter LV annotations and one LVI next chapter heading marker. Original 17 visually mapped source passages cover all 32 original source assertions, with 16 unresolved grammatical/glyph/interpretive issues preserved. Original unadmitted source-first provisional ZIP from the earlier 3,071 predecessor-held checkpoint was preserved and member-hash verified; its old predecessor note is historical, not the current state. Exact supersession and migration documented in B03a.

**After authenticated remote publication**: 3,203 Lilly + 1,066 retained Ptolemy = 4,269 historical documentary units. The accepted source ZIP, stored in the owner's Telechargements as Astrology-Lilly-Chapter-LV-Documentary-20261015.zip, passed CRC, SHA-256 checks and 18 tests replayed after extraction. Historical source annotation only; zero real partnership forecasts confirmed, zero real honesty/embezzlement claims validated, zero model runtime changes, no full blind independent second diplomatic transcription.

**NEXT:** Chapter LVI, whether a besieged city/town/castle is taken, beginning original PDF413/printed379 BELOW the divider. Source study remains OPEN.
"""
prefix="""# Current astrology source audit — latest source-only historical checkpoint

CURRENT 2026-10-15: Lilly Book II Chapter LV partnership accepted as original 1647 documentary research, 3,203 Lilly + 1,066 Ptolemy = 4,269 historical source units after remote publication. Next LVI siege chapter, PDF413/printed379 BELOW divider. No empirical astrology validations, personal predictions or runtime promotion. Source and acceptance details: state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03a_CHAPTER_LV_COMPLETE.md and B03a publication receipt.

---

"""
OLDI.parent.mkdir(parents=True,exist_ok=True)
OLDI.write_bytes(original)
OLDC.write_bytes(CUR.read_bytes())
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
CUR.write_text(prefix+OLDC.read_text())
LATEST.write_text(state)
re={'batch':'B03a','kind':'CANONICAL_HISTORICAL_SOURCE_INDEX_PREPARED_NOT_REMOTE_PUBLISHED',
 'previous_canonical_index_git_blob_sha1':prevblob,
 'old_index_sha256':sha(OLDI),'new_index_sha256':sha(I),
 'new_current_sha256':sha(CUR),'new_latest_sha256':sha(LATEST),
 'source_rules_sha256':A['rules_sha256'],'accepted_zip_sha256':rel['archive_sha256'],
 'local_documentary_units_added':32,'lilly_if_published':3203,'retained_ptolemy':1066,
 'combined_if_published':4269,'next_chapter':'LVI','next_pdf_page':413,
 'new_empirical_validations':0,'runtime_promotions':0,'remote_published':False}
RECEIPT.write_text(json.dumps(re,indent=2)+'\n')
print(json.dumps(re,indent=2))
