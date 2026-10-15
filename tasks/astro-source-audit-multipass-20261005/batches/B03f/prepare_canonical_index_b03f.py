#!/usr/bin/env python3
"""Guarded canonical historic-documentary index append; NOT model validation."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03f_CHAPTER_LX_COMPLETE.md'
OLDIDX=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03f_CANONICAL.json'
OLDCUR=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03f.md'
RECEIPT=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json'
assert not any(p.exists() for p in (LATEST,OLDIDX,OLDCUR,RECEIPT))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.run(['git',*args],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()
raw=IDX.read_bytes();j=json.loads(raw)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
E=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').read_text())
assert j['records_count']==3418 and j['batches'][-1]['id']=='B03e'
assert j['next']['chapter']=='LX' and j['next']['pdf_page']==423
assert j['read_numbered_chapters']==list(range(1,60))
assert j['empirical_validations']==j['runtime_promotions']==0
assert not any(x['id']=='B03f' for x in j['batches'])
assert A['documentary_accepted_locally'] and A['whole_chapter_lx_documentary_accepted']
assert A['added_documentary_units']==31 and A['previous_lilly_accepted']==3418
assert A['lilly_if_published']==3449 and A['combined_if_published']==4515
assert A['source_reverse_spans']==13 and A['unresolved_source_issues']==13
assert R['record_count']==31 and R['source_internal_reported_marriage_outcomes']==1
assert R['independently_confirmed_marriage_outcomes']==0
assert [r['record_number'] for r in R['rules']]==list(range(3419,3450))
assert R['rules'][-1]['chapter']=='LXI_NAVIGATION_ONLY'
assert not R['original_case_independently_authenticated']
assert E['zip_crc_pass'] and E['all_member_hashes_pass'] and E['actual_extraction_pass']
assert E['extracted_source_tests_passed']==18 and E['extracted_test_exit_code']==0
assert sha(E['owner_os_download_path'])==E['archive_sha256']
assert sha(B/'RULES.json')==A['rules_sha256']==E['source_rules_sha256']
relpath=str(IDX.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',relpath],cwd=ROOT).returncode==0
previous_git_blob=git('rev-parse','HEAD:'+relpath)
assert previous_git_blob==git('hash-object',str(IDX))
j['batches'].append({'id':'B03f','path':'batches/B03f/RULES.json',
 'records_count':31,'sha256':A['rules_sha256'],
 'scope':'Original 1647 Chapter LX marriage horoscope dated 11 June 1646 at 10:38 AM, original PDF423-424 above LXI divider; 30 original case/diagram/documentary source units and one LXI navigation-only heading; 13 source passage groups and 13 retained ambiguities. Reported marriage is author-internal, not empirically validated.'})
j['records_count']=3449
j['read_numbered_chapters'].append(60)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LX_DOCUMENTARY_SOURCE_ONLY_NEXT_LXI_OPEN'
j['next']={'pdf_page':424,'printed_page':390,'chapter':'LXI',
 'heading':'A Fugitive Servant, which way gone, when returne?',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF424 BELOW divider following Chapter LX marriage report; new servant-fled square horoscope and judgment are exclusively LXI.'}
j['chapter_LX_source_acceptance_note']='31 historical-source editorial units including one LXI boundary, 13 original-image reverse passages and 13 retained unresolved chart/grammar/reception issues. Original 11 June 1646 chart and its author-reported marriage success are documentary, not independently authenticated, prospectively frozen, or counted as astrology predictive validation.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03f_CHAPTER_LX_COMPLETE.md'
assert j['records_count']==sum(b['records_count'] for b in j['batches'])==3449
assert j['read_numbered_chapters']==list(range(1,61))
newstate="""# Lilly 1647 Chapter LX — separate worked marriage horoscope, historically source-admitted

2026-10-15 Africa/Dakar UTC+0. Parent original-astrology-book research OPEN. This report documents original William Lilly Christian Astrology (1647), Wellcome b30338724 PDF SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

Original Book II Chapter LX occupies PDF423 / printed389, and PDF424 / printed390 ABOVE the Chapter LXI divider. The printed horoscope at PDF423 is dated **11 June 1646, 10:38 AM**; it is a DIFFERENT case from Chapter LIX's 16 June 1646 chart. The original square figure has house cusps and planetary glyphs. The author describes querent and quesited appearances, Mercury retrograde and under Sun beams, Jupiter exaltation, a semisextile, Moon separating from Jupiter by square and applying to Mercury by trine, and a Moon-associated mediator. The author narrates that marriage eventually occurred after difficulty; **no independent record proves the outcome, and no prospectively frozen forecast exists**.

Accepted Chapter LX batch B03f: **31 source units R3419–R3449** (30 LX assertions/heading/figure notes plus one Chapter LXI navigation-only marker), 13 visually mapped source passages, 13 unresolved textual/chart limitations. Historical courtship descriptions and person-level conjectures cannot be treated as validated traits or future advice. No blind independent full diplomatic transcription; no ephemeris parity; no known birthplace/timezone in these two scanned pages. A source-internal positive report is counted only as author-reported context.

**After authenticated remote source publication:** 3,449 Lilly + 1,066 retained Ptolemy = 4,515 historical documentary annotations. Zero new verified astrological predictions, independent marriage case outcomes, model/runtime promotions, or blind performance evidence.

The accepted release ZIP on the owner's designated Downloads path is Astrology-Lilly-Chapter-LX-Documentary-20261015.zip; mechanically checked with SHA-256, ZIP integrity, actual extraction and 18 replayed source tests. Original source rows, uncertainties, and acceptance receipt are archived in B03f.

**Next:** Chapter LXI Fugitive Servant, beginning PDF424 printed390 BELOW the chapter divider with a DIFFERENT square horoscope; continue original page images until true next chapter boundary. Preserve case-specific chronology and avoid any human identity/privacy inference. Parent source study remains OPEN.
"""
curprefix="""# Current astrology original-source audit — most recent historical study checkpoint

CURRENT (2026-10-15): Lilly Book II Chapter LX worked marriage horary document study accepted on source research branch, 3,449 Lilly + 1,066 Ptolemy = 4,515 historical annotations after authenticated publication. Next LXI, original PDF424 printed390 BELOW divider; independent empirical astrological predictions validated: zero, runtime promotions: zero. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03f_CHAPTER_LX_COMPLETE.md and B03f source/canonical publication receipts.

---

"""
OLDIDX.parent.mkdir(parents=True,exist_ok=True)
OLDIDX.write_bytes(raw)
OLDCUR.write_bytes(CUR.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CUR.write_text(curprefix+OLDCUR.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(newstate,encoding='utf-8')
receipt={'batch':'B03f','kind':'GUARDED_DOCUMENTARY_SOURCE_INDEX_PREPARED_LOCAL_ONLY',
 'previous_index_git_blob_sha1':previous_git_blob,'old_index_sha256':sha(OLDIDX),
 'new_index_sha256':sha(IDX),'new_state_sha256':sha(CUR),
 'new_latest_source_state_sha256':sha(LATEST),'rules_sha256':A['rules_sha256'],
 'release_zip_sha256':E['archive_sha256'],'source_units_added':31,
 'lilly_if_published':3449,'ptolemy_retained':1066,'combined_if_published':4515,
 'next_chapter':'LXI','next_original_pdf':424,
 'new_empirical_predictions_validated':0,'runtime_promotions':0,'remotely_published':False}
RECEIPT.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
