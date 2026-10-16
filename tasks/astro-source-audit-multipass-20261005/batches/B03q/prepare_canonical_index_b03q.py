from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03q_CHAPTER_LXXI_COMPLETE.md'
OLDI=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B03q_CANONICAL.json'
OLDC=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B03q.md'
REC=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json'
assert not any(x.exists() for x in (LATEST,OLDI,OLDC,REC))
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
raw=I.read_bytes();j=json.loads(raw)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').read_text())
assert j['records_count']==4052 and j['batches'][-1]['id']=='B03p'
assert j['next']['chapter']=='LXXI' and j['next']['pdf_page']==451
assert j['read_numbered_chapters']==list(range(1,71))
assert j['empirical_validations']==j['runtime_promotions']==0
assert j['source_sha256']==A['source_full_pdf_sha256']
assert not any(x['id']=='B03q' for x in j['batches'])
assert A['documentary_accepted_locally'] and A['new_documentary_records']==41
assert A['lilly_if_published']==4093 and A['combined_if_published']==5159
assert R['record_count']==41 and [r['record_number'] for r in R['rules']]==list(range(4053,4094))
assert R['independently_verified_outcomes']==0
assert R['rules'][-1]['chapter']=='LXXII_NAVIGATION_ONLY'
assert Z['zip_crc_pass'] and Z['member_sha256_pass'] and Z['full_extraction_pass']
assert Z['tests_replayed']==10 and Z['test_exit_code']==0
assert H(Z['local_owner_path'])==Z['archive_sha256']
assert H(B/'RULES.json')==A['rules_sha256']==Z['rules_sha256']
rel=str(I.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rel],cwd=ROOT).returncode==0
before=git('rev-parse','HEAD:'+rel)
assert before==git('hash-object',str(I))
j['batches'].append({'id':'B03q','path':'batches/B03q/RULES.json',
 'records_count':41,'sha256':A['rules_sha256'],
 'scope':'Lilly original 1647 LXXI wife enquires about husband at sea, 15 April 1645 1:10 PM square figure, original PDF451-452 with LXXII heading PDF453. 40 historical clauses plus one navigation, 10 visual source passages and 18 limits; early false rumor in 2-3 days, later news in second week May rather than exactly May 5, physical return only July, retrospective Barnstable location. No independently verified predictions.'})
j['records_count']=4093
j['read_numbered_chapters'].append(71)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LXXI_DOCUMENTARY_SOURCE_ONLY_NEXT_LXXII_OPEN'
j['next']={'pdf_page':453,'printed_page':419,'chapter':'LXXII',
 'heading':'What manner of Death Canterbury should dye?',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF453 begins separate chapter on Archbishop of Canterbury, own circular horoscope dated 3 December 1644.'}
j['chapter_LXXI_source_acceptance_note']='41 original source annotations R4053-R4093, 10 original passage groups and 18 limits. The early report of husband in town was false; later reliable news in May and actual return in July are distinct. Later claimed Barnstable location not independently verified; zero empirical successes.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03q_CHAPTER_LXXI_COMPLETE.md'
assert j['records_count']==sum(x['records_count'] for x in j['batches'])==4093
assert j['read_numbered_chapters']==list(range(1,72))
STATE="""# Original Lilly Chapter LXXI — missing husband-at-sea case documentary acceptance

Original William Lilly Christian Astrology 1647 Wellcome b30338724, full original PDF SHA256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

Chapter LXXI begins original PDF451/printed417 with a square figure dated 15 April 1645 at 1:10 PM, and ends PDF452/printed418. The next Chapter LXXII on Canterbury begins PDF453/printed419.

Lilly reports the wife heard a FALSE rumor after a 2–3-day forecast of hearing news. Later he forecast certain news OR return about 5 May; she reportedly received definite news in the second week of May, but her husband did not return physically until the second week of July. This must not count as return by May. His supposed presence near southwest England/Barnstable and previous Royalist captivity are retrospective source claims without external verification.

B03q accepts 41 historical documentary source units R4053–R4093, 40 Chapter LXXI annotations and one LXXII navigation marker, ten original-source passages, 18 uncertainties. No independently validated alive/status, rumor, correspondence, location or physical homecoming case and no runtime model promotions.

After authenticated research publication the corpus would contain Lilly 4,093 plus Ptolemy 1,066 = 5,159 historical source annotations. The owner-local archive Astrology-Lilly-Chapter-LXXI-Husband-at-Sea-Documentary-20261016.zip was extracted, hashed and passed ten replayed focused tests.

NEXT LXXII Archbishop of Canterbury date/mode-of-death case; original figure on PDF453. The historical source-study and separate empirically blinded testing remain OPEN.
"""
PREFIX="""# Current astrology original-source research through Chapter LXXI

CURRENT 2026-10-16: Lilly LXXI source-only historical documentary case, 4,093 Lilly + 1,066 Ptolemy = 5,159 after publication. Next LXXII original PDF453. First rumor false; news in May, actual return only July. No independent validations. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B03q_CHAPTER_LXXI_COMPLETE.md.

---

"""
OLDI.parent.mkdir(parents=True,exist_ok=True)
OLDI.write_bytes(raw)
OLDC.write_bytes(CUR.read_bytes())
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
CUR.write_text(PREFIX+OLDC.read_text())
LATEST.write_text(STATE)
rec={'batch':'B03q','status':'GUARDED_LOCAL_SOURCE_INDEX_PREPARED',
 'previous_git_blob':before,'old_index_sha256':H(OLDI),
 'new_index_sha256':H(I),'new_current_sha256':H(CUR),'new_latest_sha256':H(LATEST),
 'source_rules_sha256':A['rules_sha256'],'accepted_zip_sha256':Z['archive_sha256'],
 'new_documentary_source_units':41,'lilly_if_published':4093,'combined_if_published':5159,
 'next_chapter':'LXXII','next_original_pdf_page':453,
 'empirically_validated_cases':0,'runtime_promotions':0,
 'remote_published':False}
REC.write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2))
