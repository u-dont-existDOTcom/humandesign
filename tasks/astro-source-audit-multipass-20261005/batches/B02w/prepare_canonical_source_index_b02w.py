"""Guarded non-destructive canonical research-index update for documentary B02w."""
import json,hashlib,subprocess
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CURRENT=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02w_CHAPTER_LI_COMPLETE.md'
BACK=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B02w_CANONICAL_20261015.json'
CURBACK=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B02w_20261015.md'
receipt=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json'
assert not (BACK.exists() or CURBACK.exists() or LATEST.exists() or receipt.exists())
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
j=json.loads(I.read_bytes())
pre=json.loads((B/'RETAINED_LILLY_INDEX_BEFORE_B02w.json').read_bytes())
assert j==pre,'Accepted predecessor differs from frozen B02v index. Must reconcile before writing'
assert j['records_count']==2974 and j['batches'][-1]['id']=='B02v'
assert j['read_numbered_chapters']==list(range(1,51))
assert j['next']['chapter']=='LI' and j['next']['pdf_page']==400
assert j['runtime_promotions']==0 and j['empirical_validations']==0
index_path=str(I.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',index_path],cwd=ROOT).returncode==0
blob=subprocess.run(['git','rev-parse','HEAD:'+index_path],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
raw_sha=subprocess.run(['git','hash-object',str(I)],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
assert blob==raw_sha
a=json.loads((B/'ACCEPTANCE.json').read_text())
r=json.loads((B/'RULES.json').read_text())
u=json.loads((B/'UNRESOLVED.json').read_text())
d=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_PACKET_RECEIPT_20261015.json').read_text())
claim=json.loads((B/'CLAIM_LEDGER.json').read_text())
assert a['accepted'] and a['kind']=='HISTORICAL_SOURCE_DOCUMENTARY_ONLY'
assert len(r['rules'])==a['new_documentary_source_units']==42
assert r['whole_chapter_li_complete_at_documentary_source_level']
assert [x['record_number'] for x in r['rules']]==list(range(2975,3017))
assert a['prior_accepted_lilly']==2974 and a['uncertainties_retained']==len(u['issues'])==11
assert a['literal_e_contra_count']==5 and a['other_contrary_statement_count']==1
assert all(not x['case_evidence_countable'] for x in r['rules'])
assert all(x['runtime_status']=='REFERENCE_ONLY_NOT_PROMOTED' for x in r['rules'])
assert not r['accepted_as_empirical_astro_prediction']
assert claim['empirical_predictive_outcomes']==claim['runtime_promotions']==0
for fname,key in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),('UNRESOLVED.json','unresolved_sha256'),('CLAIM_LEDGER.json','claim_ledger_sha256'),('INDEPENDENT_IMAGE_FIRST_REVIEW_20261015.md','audit_report_sha256'),('ORIGINAL_TO_RECORD_COVERAGE_V1.json','coverage_sha256')]:
 assert sha(B/fname)==a[key],fname
assert d['extracted_original_source_test_count']==22 and d['actual_extraction_pass'] and d['zip_crc_pass'] and d['per_file_sha256_pass']
archive=Path(d['archive_os_downloads'])
assert archive.is_file() and sha(archive)==d['archive_sha256']
assert archive.stat().st_size==d['archive_bytes']
j['batches'].append({'id':'B02w','path':'batches/B02w/RULES.json','records_count':42,
'sha256':a['rules_sha256'],
'scope':'Book II Chapter LI Battle/Warre/Contentions: original PDF400 below divider through PDF402 bottom; 41 original Chapter LI editorial source annotations and one next-chapter boundary; 35 visual reverse source spans, 11 retained limits; historical text ONLY.'})
j['records_count']=3016
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LI_DOCUMENTARY_SOURCE_ONLY_NEXT_LII_OPEN'
j['read_numbered_chapters'].append(51)
j['next']={'pdf_page':403,'printed_page':369,'chapter':'LII',
'heading':'Who shall doe best in a suit of Law.',
'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
'position':'First chapter heading near top of original PDF403/printed369. Begin LII body directly below; do not import into Chapter LI.'}
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02w_CHAPTER_LI_COMPLETE.md'
j['chapter_LI_source_acceptance_note']='42 historical editorial source units (one LII boundary), manual reverse original-image-first 35 passages, 22 extracted-archive source-only tests, 11 retained uncertainties including 5 literal e-contra and 1 differently phrased contrary; no diplomatic source certification, no empirical or runtime validation.'
assert j['records_count']==sum(x['records_count'] for x in j['batches'])==3016
assert len(j['read_numbered_chapters'])==51 and j['read_numbered_chapters'][-1]==51
body="""# Latest astrology source audit — Chapter LI historical-documentary accepted

**2026-10-15 Africa/Dakar (UTC+0). PARENT MULTI-AUTHOR ASTROLOGY SOURCE STUDY OPEN.**

Chapter LI of original 1647 William Lilly *Christian Astrology* is accepted **only as historical documentary source**, not as experimentally supported war forecasts, danger assessments, mortality predictors or legal/medical advice.

The accepted Lilly count is **3,016** units (earlier 2,974 + B02w **42** newly reviewed editorial units, of which one is the Chapter LII boundary). Retained Ptolemy **1,066**, combined historical-documentary **4,082**. Original text scope: PDF400/printed366 below divider; PDF401/printed367; PDF402/printed368 through last war-outcome clause; next chapter begins PDF403/printed369. The full original Wellcome b30338724 SHA256 is `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`.

Documentary verification: 35 independently selected original-image source spans mapped to 42 records, 11 retained textual issues, 22 source-only tests replayed **after actual ZIP extraction**, original-page image hash checks, archive CRC/hash verification, and owner Downloads local copy hash. Distinguish **5 literal e-contra abbreviations** plus **1 differently worded contrary** (6 converse editorial units). No complete independent diplomatic transcription, real patient/participant case, war outcome check, empirical predictive validation, or runtime chart promotion.

Read `tasks/astro-source-audit-multipass-20261005/batches/B02w/HANDOFF_AFTER_DOCUMENTARY_ADMISSION_20261015.md`, `batches/B02w/INDEPENDENT_IMAGE_FIRST_REVIEW_20261015.md`, `ORIGINAL_TO_RECORD_COVERAGE_V1.json`, and `ACCEPTANCE.json`. Check **PUBLICATION_RECEIPT.json** for actual post-GitHub publication verification; local acceptance predates remote push.

**Next original source:** William Lilly Book II Chapter **LII**, heading `Who shall doe best in a suit of Law.`, beginning PDF403/printed369; proceed through all unnumbered ensuing sections and next physical divider. Continue remaining authors afterward. Parent study OPEN; no user decision needed.
"""
old_curr=CURRENT.read_bytes()
preface="""# Current astrology source audit — latest checkpoint

**CURRENT (2026-10-15):** Lilly historical documentary Chapter LI accepted: **3,016 Lilly + 1,066 Ptolemy = 4,082** source-only units. 42 new source units include the next-chapter boundary; 11 retained textual issues, zero empirical validations or runtime changes. Next **Chapter LII**, original PDF403/printed369. See `state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02w_CHAPTER_LI_COMPLETE.md` and the canonical source index. Details below preserve earlier historical state.

---

"""
BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(I.read_bytes())
CURBACK.write_bytes(old_curr)
I.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
LATEST.write_text(body)
CURRENT.write_text(preface+old_curr.decode())
rec={'kind':'PREPARED_DOCUMENTARY_CANONICAL_INDEX_NO_REMOTE_PUSH_YET','batch':'B02w',
'index_previous_git_blob_sha1':blob,'index_previous_sha256':sha(BACK),
'index_new_sha256':sha(I),'latest_state_sha256':sha(LATEST),'current_state_sha256':sha(CURRENT),
'accepted_rules_sha256':a['rules_sha256'],'archive_sha256':d['archive_sha256'],
'archive_verified_in_owner_downloads':True,'new_documentary_units':42,'lilly_after':3016,
'ptolemy_retained':1066,'combined_documentary':4082,'empirical_cases':0,'runtime_promotions':0,
'next_pdf':403,'next_chapter':'LII','canonical_published':False}
receipt.write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2))
