#!/usr/bin/env python3
"""Guarded Chapter LXXIX canonical index and source-only state integration."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03y_CHAPTER_LXXIX_COMPLETE.md'
OLD=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03y_CANONICAL.json'
OLDCUR=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03y.md'
REC=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json'
assert not any(p.exists() for p in (LATEST,OLD,OLDCUR,REC))
h=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes();j=json.loads(raw)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').read_text())
assert j['records_count']==4508 and j['batches'][-1]['id']=='B03x'
assert j['next']['chapter']=='LXXIX' and j['next']['pdf_page']==471
assert j['read_numbered_chapters']==list(range(1,79))
assert j['source_sha256']==A['original_pdf_sha256']
assert j['empirical_validations']==j['runtime_promotions']==0
assert not any(k['id']=='B03y' for k in j['batches'])
assert A['documentary_accepted_locally'] and A['prior_lilly_accepted']==4508
assert A['new_documentary_records']==41 and A['lilly_if_published']==4549
assert A['combined_if_published']==5615
assert R['record_count']==41 and R['independently_verified_parsonage_outcomes']==0
assert [r['record_number'] for r in R['rules']]==list(range(4509,4550))
assert all(r['chapter']=='LXXX_NAVIGATION_ONLY' for r in R['rules'][-2:])
assert Z['zip_crc_pass'] and Z['member_hashes_pass'] and Z['full_extraction_pass']
assert Z['extracted_tests_passed']==14 and Z['extracted_exit_code']==0
assert h(Z['owner_download_path'])==Z['archive_sha256']
assert h(B/'RULES.json')==A['rules_sha256']==Z['accepted_rules_sha256']
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rel],cwd=ROOT).returncode==0
old_blob=git('rev-parse','HEAD:'+rel)
assert old_blob==git('hash-object',str(IDX))
j['batches'].append({'id':'B03y','path':'batches/B03y/RULES.json',
 'records_count':41,'sha256':A['rules_sha256'],
 'scope':'Original William Lilly 1647 Book II LXXIX parsonage refusal example on original PDF471 below LXXVIII and PDF472 to end; following LXXX opening on PDF473. 39 substantive historically source-only observations plus two navigation markers, seven original passage groups and 17 unresolved limits, six author negative factors, anecdotal letter with unverified failure and hypothetical unknown informer. No independently validated prediction.'})
j['records_count']=4549
j['read_numbered_chapters'].append(79)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LXXIX_HISTORICAL_SOURCE_ONLY_NEXT_LXXX_OPEN'
j['next']={'pdf_page':473,'printed_page':439,'chapter':'LXXX',
 'printed_chapter_numeral':'LXXX','heading':'If Presbytery shall stand?',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF473/printed439 new circular figure dated 11 March 1646/7 (dual-year printed 1646 over 7), 4:45 PM. LXXIX ends original PDF472/printed438.'}
j['chapter_LXXIX_source_acceptance_note']='41 source-only historical records R4509-R4549 including 39 parsonage appointment case clauses and two LXXX boundary annotations, seven original passage groups, 17 uncertainty items. Author reports letter obstructed his covetous applicant despite advice, with unspecified neighbor and speculative descriptions. Zero independently verified forecast outcome.'
j['current_state']=str(LATEST.relative_to(ROOT))
assert j['records_count']==sum(x['records_count'] for x in j['batches'])==4549
assert j['read_numbered_chapters']==list(range(1,80))
REPORT="""# William Lilly (1647) Book II Chapter LXXIX — parsonage appointment case

2026-10-16 — Africa/Dakar (UTC+0). Original witness: William Lilly, Christian Astrology first edition (1647), Wellcome b30338724, full original PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

**Boundaries:** The separate parsonage question begins PDF471/printed437 *below* the LXXVIII dream ending and new horizontal divider. Its circular chart prints **6 August 1644, 8:24 PM**. The judgment continues through PDF472/printed438 and ends before Chapter LXXX on PDF473/printed439. The next figure prints **11 March 1646/7, 4:45 PM** with the year written on two lines; do not silently simplify the dual year.

**Judgment:** The source names the rising sign, Saturn in ascendant, Mars as ascendant ruler, Moon and Jupiter ninth ruler signifying the benefice. It enumerates six adverse circumstances, keeping absent aspects, absence from ninth, no translation/collection, absent reception, Saturn's impedance, and the Moon-to-Mercury opposition separate. Lilly infers opposition by neighboring scholars/divines and possibly women through Venus in seventh. He says he advised withdrawal; the applicant proceeded, and a damaging letter about a woman allegedly destroyed the hoped-for position.

**Source limitations:** The identity of the informer was expressly never discovered. Lilly's suggested farmer/miller, Northeast location and fifteen furlongs form a *counterfactual untested hypothesis*. Neither the letter nor the refusal, counsel or precise outcome dates have been authenticated independently. The six negative rules and character interpretation are historical claims, not validated statistical predictors or behavioral assessment.

**Documentary acceptance:** 41 historical source annotations **R4509–R4549**, 39 chapter clauses plus two next-chapter navigation records; seven original-source spans, one PDF471–472 seam, and 17 unresolved source limitations. Three original 1600-pixel page witnesses hashed and preserved; no blind diplomatic second transcription or horoscope parity calculation. Focused tests and full independent ZIP extraction verified.

**After authenticated research publication:** cumulative Lilly **4,549** plus retained Ptolemy **1,066** = **5,615 historical documentary units**. New independent empirical forecast validations **zero**, runtime model or scoring changes **zero**.

Owner archive: Astrology-Lilly-Chapter-LXXIX-Parsonage-Documentary-20261016.zip in laptop Downloads. SHA256 ac60d08163b1be0ed07fe72546dfbcf43f7bf3ea1be42559b6a2d03733fe6bc1. ZIP CRC, member SHA256 and extracted 14 test replay passed.

**Next:** Chapter LXXX, the fate of Presbytery, begins original PDF473/printed439. Parent source research OPEN.
"""
PREFIX="""# Original historical Lilly research — Chapter LXXIX

CURRENT 2026-10-16: Chapter LXXIX original parsonage denial case documentary accepted; upon authenticated branch publication **4,549 Lilly + 1,066 retained Ptolemy = 5,615 historical source records**. Next LXXX opens PDF473/printed439. Author-only account of a damaging letter; identity of informer unverified; no empirical validation or runtime promotions. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03y_CHAPTER_LXXIX_COMPLETE.md.

---

"""
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);OLDCUR.write_bytes(CUR.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CUR.write_text(PREFIX+OLDCUR.read_text(),encoding='utf-8')
LATEST.write_text(REPORT,encoding='utf-8')
rec={'batch':'B03y','status':'GUARDED_CANONICAL_INDEX_PREPARED_PENDING_GITHUB',
 'prior_index_git_blob_sha1':old_blob,'previous_index_sha256':h(OLD),
 'new_index_sha256':h(IDX),'current_state_sha256':h(CUR),
 'latest_state_sha256':h(LATEST),'accepted_source_rules_sha256':A['rules_sha256'],
 'owner_archive_sha256':Z['archive_sha256'],
 'new_documentary_records':41,'lilly_if_published':4549,
 'ptolemy_retained':1066,'combined_if_published':5615,
 'next_chapter':'LXXX','next_original_pdf_page':473,
 'independently_verified_parsonage_outcomes':0,'new_empirical_predictions':0,
 'runtime_promotions':0,'remote_published':False}
REC.write_text(json.dumps(rec,indent=2)+'\n',encoding='utf-8')
print(json.dumps(rec,indent=2))
