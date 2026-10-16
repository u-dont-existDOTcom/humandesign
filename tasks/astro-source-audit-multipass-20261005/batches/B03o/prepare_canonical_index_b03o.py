#!/usr/bin/env python3
"""Guarded original-source index append: one-page Lilly Chapter LXIX."""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03o_CHAPTER_LXIX_COMPLETE.md'
OLDI=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03o_CANONICAL.json'
OLDC=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03o.md'
REC=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json'
assert not any(x.exists() for x in (LATEST,OLDI,OLDC,REC))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
run=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
original=IDX.read_bytes()
j=json.loads(original)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').read_text())
assert j['records_count']==3976 and j['batches'][-1]['id']=='B03n'
assert j['next']['chapter']=='LXIX' and j['next']['pdf_page']==448
assert j['read_numbered_chapters']==list(range(1,69))
assert j['empirical_validations']==j['runtime_promotions']==0
assert j['source_sha256']==A['source_full_pdf_sha256']
assert A['documentary_accepted_locally'] and A['new_documentary_records']==31
assert A['lilly_if_published']==4007 and A['combined_if_published']==5073
assert R['record_count']==31 and [r['record_number'] for r in R['rules']]==list(range(3977,4008))
assert R['independently_verified_danger_cases']==0
assert R['rules'][-1]['chapter']=='LXX_NAVIGATION_ONLY'
assert Z['zip_crc_pass'] and Z['member_hash_pass'] and Z['full_extraction_pass']
assert Z['replayed_tests_passed']==17 and Z['replay_exit_code']==0
assert H(Z['owner_local_path'])==Z['zip_sha256']
assert H(B/'RULES.json')==A['rules_sha256']==Z['accepted_rules_sha256']
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rel],cwd=ROOT).returncode==0
previous_blob=run('rev-parse','HEAD:'+rel)
assert previous_blob==run('hash-object',str(IDX))
assert not any(x['id']=='B03o' for x in j['batches'])
j['batches'].append({'id':'B03o','path':'batches/B03o/RULES.json',
 'records_count':31,'sha256':A['rules_sha256'],
 'scope':'Lilly original 1647 Book II LXIX fear/danger on PDF448 printed414, generic one-page conditions and attributed cadent-rumor theory; 30 historical clauses + one LXX navigation heading PDF449, 12 source passages, 14 uncertainty limits. No source worked chart and zero independently verified risk outcomes.'})
j['records_count']=4007
j['read_numbered_chapters'].append(69)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LXIX_DOCUMENTARY_SOURCE_ONLY_NEXT_LXX_OPEN'
j['next']={'pdf_page':449,'printed_page':415,'chapter':'LXX',
 'heading':'Whether Man or Wife shall dye first?',
 'include_opening_paragraph':True,'extracted':False,
 'boundary_image_read':True,'position':'Original PDF449/printed415 at top: separate worked 6 February 1644 9:10 PM spouse mortality figure, distinct from generic one-page LXIX.'}
j['chapter_LXIX_source_acceptance_note']='31 historical source units R3977-R4007; generic source doctrine only, no dated figure, 12 reverse original-image passages and 14 uncertainties. Different conditions for unwarranted fear versus harm, benefics, infortunes, rumors and Moon-Sun disclosure; zero verified person outcomes.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03o_CHAPTER_LXIX_COMPLETE.md'
assert j['records_count']==sum(b['records_count'] for b in j['batches'])==4007
assert j['read_numbered_chapters']==list(range(1,70))
state="""# Lilly Chapter LXIX — original 1647 source documentary acceptance

Source: original William Lilly Christian Astrology, Wellcome b30338724, full source PDF SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

Chapter LXIX on original PDF448/printed414 examines whether a feared danger is warranted. It is a generic one-page conditional text without a dated worked horoscope. Chapter LXX starts separately on original PDF449/printed415.

Batch B03o contains 31 historical documentary units R3977–R4007, twelve original-image passage groups and fourteen retained uncertainties. The material distinguishes adversity, benefic mitigation, fear, burdens, accusations, rumors and disclosure. One cadent-Moon reading is attributed to other astrologers. No observed person case, predictive success or live rule is established.

After authenticated source publication: Lilly 4,007 + Ptolemy 1,066 = 5,073 historical documentary annotations. The accepted ZIP Astrology-Lilly-Chapter-LXIX-Fear-Documentary-20261016.zip in Downloads passes archive extraction and 17 replay tests.

Next: Chapter LXX original worked spouse comparison starts PDF449 with a distinct dated chart. Parent source research OPEN.
"""
prefix="""# Lilly original historical source research — LXIX

CURRENT 2026-10-16: Chapter LXIX source intake accepted. After research-branch publication Lilly 4,007 + Ptolemy 1,066 = 5,073 documentary units. Next LXX original PDF449. No predictive validation or runtime promotion. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03o_CHAPTER_LXIX_COMPLETE.md.

---

"""
OLDI.parent.mkdir(parents=True,exist_ok=True)
OLDI.write_bytes(original)
OLDC.write_bytes(CUR.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
CUR.write_text(prefix+OLDC.read_text())
LATEST.write_text(state)
receipt={'batch':'B03o','status':'LOCAL_GUARDED_INDEX_PREPARED_PENDING_GITHUB',
 'old_git_blob_sha1':previous_blob,
 'previous_index_sha256':H(OLDI),'new_index_sha256':H(IDX),
 'new_current_sha256':H(CUR),'new_latest_sha256':H(LATEST),
 'rules_sha256':A['rules_sha256'],
 'archive_sha256':Z['zip_sha256'],'new_documentary_units':31,
 'lilly_if_published':4007,'ptolemy':1066,'combined_if_published':5073,
 'next_chapter':'LXX','next_pdf':449,
 'empirical_predictions':0,'runtime_promotions':0,'remote_published':False}
REC.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
