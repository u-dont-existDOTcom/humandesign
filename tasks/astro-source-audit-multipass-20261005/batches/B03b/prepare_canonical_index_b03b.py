#!/usr/bin/env python3
"""Guarded historical documentary index update for Chapter LVI (no model change)."""
import hashlib,json,subprocess
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03b_CHAPTER_LVI_COMPLETE.md'
OLDI=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03b_CANONICAL.json'
OLDC=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03b.md'
REC=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json'
assert not any(x.exists() for x in (LATEST,OLDI,OLDC,REC))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
original=I.read_bytes()
j=json.loads(original)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
release=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').read_text())
assert j['records_count']==3203 and j['batches'][-1]['id']=='B03a'
assert j['next']['chapter']=='LVI' and j['next']['pdf_page']==413
assert j['read_numbered_chapters']==list(range(1,56))
assert j['runtime_promotions']==j['empirical_validations']==0
assert all(b['id']!='B03b' for b in j['batches'])
assert A['documentary_accepted_locally'] and A['whole_chapter_lvi_documentary_intake_complete']
assert A['added_historical_units']==45 and A['previous_lilly_accepted']==3203
assert A['source_reverse_spans']==19 and A['unresolved_source_issues']==17
assert R['record_count']==45 and R['rules'][-1]['chapter']=='LVII_HEADING_NAVIGATION_ONLY'
assert [r['record_number'] for r in R['rules']]==list(range(3204,3249))
assert all(r['chapter']=='LVI' for r in R['rules'][:-1])
assert R['new_empirically_validated_predictions']==R['runtime_promotions']==0
assert release['zip_crc_pass'] and release['member_sha256_pass'] and release['actual_extraction_pass']
assert release['extracted_test_count']==17 and release['extracted_17_tests_exit_code']==0
assert sha(release['archive_on_laptop'])==release['archive_sha256']
assert A['rules_sha256']==release['accepted_rules_sha256']==sha(B/'RULES.json')
p=str(I.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',p],cwd=ROOT).returncode==0
prior_blob=git('rev-parse','HEAD:'+p)
assert prior_blob==git('hash-object',str(I))
j['batches'].append({
  'id':'B03b','path':'batches/B03b/RULES.json',
  'records_count':45,'sha256':A['rules_sha256'],
  'scope':'Original 1647 Book II Chapter LVI city/town/castle siege: PDF413 below LV divider through PDF414 above LVII divider; 44 LVI historical source units plus next-chapter navigation marker; 19 reverse source passages, 17 preserved text limits. No observed efficacy or model promotion.'})
j['records_count']=3248
j['read_numbered_chapters'].append(56)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LVI_DOCUMENTARY_SOURCE_ONLY_NEXT_LVII_OPEN'
j['next']={
 'pdf_page':414,'printed_page':380,'chapter':'LVII',
 'heading':'Of Commanders in Armies, their abilities, fidelity, and whether by them Victory may be had yea or not, &c.',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF414 BELOW divider following last Chapter LVI soldier-retreat statement; continue original source until the next numbered chapter physical divider.'}
j['chapter_LVI_source_acceptance_note']='45 source-only historical annotations R3204–R3248, incl one LVII navigation marker; 19 manually visually mapped original passage groups, 17 limits, 2 original scan hashes. Reproducible extracted archive passed 17 focused source tests. No full blind second diplomatic transcription; no validated historical siege outcome, military claim, astrology predictions or runtime promotion.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03b_CHAPTER_LVI_COMPLETE.md'
assert j['records_count']==sum(x['records_count'] for x in j['batches'])==3248
assert j['read_numbered_chapters']==list(range(1,57))
state="""# Lilly Chapter LVI — city, town or castle siege — documentary 1647 source intake

2026-10-15 Africa/Dakar UTC+0. William Lilly, Christian Astrology original 1647 Wellcome b30338724 (full original 894-page PDF verified previous SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b).

Chapter LVI occupies original PDF413/printed379 BELOW the Chapter LV divider and original PDF414/printed380 ABOVE the Chapter LVII divider. Its 1647 source interprets besiegers' first-house, besieged place's fourth-house, defenders' governor and potential allies, plus multiple qualified and conflicting claims about capture/resistance. Original symbols, receptions, negative cases and grammatical ambiguities are retained rather than invented into deterministic rules.

B03b **45 locally admitted historical documentary source records R3204–R3248** (44 substantive LVI editorial annotations, 1 LVII heading-only navigation marker), mapped to 19 original-image-first source passages with 17 retained limits. Source evidence contains the original two image scans and sha256 manifest. The source text was directly visually reviewed, but NOT completely re-transcribed diplomatically by an independent blind second reader. Claims of betrayal and supply or personnel problems are historical authorial conjectures, not verified military intelligence or advice.

**After authenticated research-branch publication: Lilly 3,248 + Ptolemy retained 1,066 = 4,314 historical documentary units.** No authenticated real siege outcome, prospective astrology hit, military forecast, calibrated probability, or runtime rule change. The accepted owner archive Astrology-Lilly-Chapter-LVI-Documentary-20261015.zip on the owner's laptop passed ZIP integrity, member SHA-256 verification, actual extraction, and 17 source-only tests replayed.

Full source evidence, source-first map, claim ledger, textual uncertainties, original source images, local acceptance and publication receipt are in B03b. This is historical book-study evidence only, not proof of astrology's effectiveness.

**NEXT:** Book II Chapter LVII, *Of Commanders in Armies*, starts original PDF414/printed380 BELOW divider, continues through subsequent original pages until the next numbered chapter heading. Preserve source only, without military advice or actual effectiveness claims. Parent full astrology book-study and empirical evaluation goal OPEN.
"""
prefix="""# Current astrology source audit — latest documentary source checkpoint

2026-10-15 Africa/Dakar UTC+0: Lilly Chapter LVI source admitted for historical original book study, 3,248 Lilly + 1,066 retained Ptolemy = 4,314 documentary source units after authenticated research-branch publication. Next LVII begins original PDF414/printed380 BELOW physical divider. NO new real-world astrology prediction validations or runtime changes. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B03b_CHAPTER_LVI_COMPLETE.md and the B03b source acceptance/publication files.

---

"""
OLDI.parent.mkdir(parents=True,exist_ok=True)
OLDI.write_bytes(original)
OLDC.write_bytes(CUR.read_bytes())
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CUR.write_text(prefix+OLDC.read_text(encoding='utf-8'),encoding='utf-8')
LATEST.write_text(state,encoding='utf-8')
receipt={
 'batch':'B03b','kind':'CANONICAL_HISTORICAL_SOURCE_INDEX_PREPARED_NOT_REMOTE_PUBLISHED',
 'previous_index_blob_sha1':prior_blob,
 'previous_index_sha256':sha(OLDI),
 'new_index_sha256':sha(I),
 'new_current_state_sha256':sha(CUR),
 'new_latest_state_sha256':sha(LATEST),
 'source_rules_sha256':A['rules_sha256'],
 'owner_zip_sha256':release['archive_sha256'],
 'new_local_historical_source_records':45,
 'lilly_if_published':3248,'ptolemy_retained':1066,
 'combined_if_published':4314,'next_chapter':'LVII',
 'next_original_pdf':414,'new_empirical_predictions_validated':0,
 'runtime_predicate_promotions':0,'remote_published':False}
REC.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
