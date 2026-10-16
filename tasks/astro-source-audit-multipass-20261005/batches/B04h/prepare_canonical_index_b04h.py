from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04h_CHAPTER_LXXXVIII_COMPLETE.md'
OLD=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B04h_CANONICAL.json'
OLDCUR=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B04h.md'
REC=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json'
assert not any(p.exists() for p in (LATEST,OLD,OLDCUR,REC))
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
raw=I.read_bytes();j=json.loads(raw)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').read_text())
assert j['records_count']==5113 and j['batches'][-1]['id']=='B04g'
assert j['next']['chapter']=='LXXXVIII' and j['next']['printed_chapter_numeral']=='LXXXVII' and j['next']['pdf_page']==491
assert j['read_numbered_chapters']==list(range(1,88))
assert j['read_numbered_chapters_basis']=='editorial_source_sequence_ordinals_not_literal_1647_headings'
assert j['original_printed_chapter_heading_crosswalk']['duplicate_printed_numeral']=='LXXXV'
assert j['empirical_validations']==j['runtime_promotions']==0
assert j['source_sha256']==A['original_pdf_sha256']
assert A['prior_lilly_accepted']==5113 and A['new_documentary_records']==48
assert A['lilly_if_published']==5161 and A['combined_if_published']==6227
assert R['record_count']==48 and [r['record_number'] for r in R['rules']]==list(range(5114,5162))
assert all(r['original_printed_chapter_numeral']=='LXXXVII' for r in R['rules'][:-2])
assert Z['zip_crc_pass'] and Z['member_hashes_pass'] and Z['full_extraction_pass']
assert Z['extracted_tests_passed']==15 and H(Z['owner_download_path'])==Z['archive_sha256']
assert H(B/'RULES.json')==A['rules_sha256']==Z['accepted_rules_sha256']
rel=str(I.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rel],cwd=ROOT).returncode==0
oldblob=git('rev-parse','HEAD:'+rel)
assert oldblob==git('hash-object',str(I))
j['batches'].append({'id':'B04h','path':'batches/B04h/RULES.json',
 'records_count':48,'sha256':A['rules_sha256'],
 'scope':'Original Lilly first edition printed LXXXVII, stable editorial LXXXVIII, Eleventh House hope/friendship and completeness rules on original PDF491-492 with LXXXVIII following heading PDF493. Forty-six chapter clauses and two next-heading markers, seven page spans, 21 retained limitations; common/movable/fixed and good-hopes versus partial/probability/harm outcomes distinct; no independent validations.'})
j['records_count']=5161
j['read_numbered_chapters'].append(88)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_EDITORIAL_LXXXVIII_PRINTED_LXXXVII_NEXT_EDITORIAL_LXXXIX'
j['next']={'pdf_page':493,'printed_page':459,'chapter':'LXXXIX',
 'printed_chapter_numeral':'LXXXVIII','heading':'Of the agreeing of Friends',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF493/printed459 starts distinct printed LXXXVIII / stable editorial LXXXIX friends agreement case; prior printed LXXXVII ends PDF492.'}
j['chapter_LXXXVIII_source_acceptance_note']='48 historical source clauses R5114–R5161, 46 original Eleventh House hopes and 2 next-heading. Original printed LXXXVII (editorial sequence LXXXVIII) preserves duplicated LXXXV numbering crosswalk. Outcome classes partial/probability/whole/harm after possessing remain separate, with feasibility caveat. No empirical validations.'
j['current_state']=str(LATEST.relative_to(ROOT))
assert j['records_count']==sum(v['records_count'] for v in j['batches'])==5161
assert j['read_numbered_chapters']==list(range(1,89))
REPORT="""# Lilly first edition — Eleventh House Hopes: original printed LXXXVII / editorial LXXXVIII

2026-10-16 — Africa/Dakar UTC+0. Source: William Lilly, Christian Astrology (1647), Wellcome b30338724, full original PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

**Original boundaries and numbering:** Chapter begins on original PDF491/printed457 below the Eleventh House floral divider and continues through PDF492/printed458. Separate *Of the agreeing of Friends* starts at PDF493/printed459. Original printed heading for this chapter is **LXXXVII**; its stable editorial research ordinal is **LXXXVIII** following the 1647 double-printed LXXXV, documented in the source-numbering crosswalk. Next original printed heading is **LXXXVIII**, editorial **LXXXIX**.

**Outcomes and conditions:** A strong, fortunate, well-aspected eleventh ruler can signify receiving a hoped-for thing, or love/concord if friendship is the subject. Other favorable options: good aspects between first/eleventh rulers, reception, translation of light or placing the two lords into each other's houses. If absent, Lilly advises examining the Moon and predicting denial when it lacks favorable relations to eleventh. He separately handles receiving favors from princes, masters or noblemen, predicting easier and faster success under trine/sextile versus laborious but still possible success under square/opposition, even with reception.

**Graded completion:** With the Moon's disposition receiver in a **common** sign, he expects only *part* of the thing; in a **movable** sign, only the name/likelihood or very little; in a **fixed** sign, whole completion. If the receiver is unfortunate, damage may follow **after possession**. Reception of Moon's receiver may signal obtaining more than expected. The apparent promise of obtaining everything hoped for is expressly restricted by Lilly to **feasible and possible** things. These branch differences are preserved as distinct records, not combined into a simple success rule.

**Documentary acceptance:** 48 historical annotations **R5114–R5161**, 46 Eleventh House statements and two following-chapter navigation markers, seven source groups, 21 explicit limitations. Source-original PDF491–493 witnesses independently SHA-256 frozen, source-first and archive extraction tests pass. No identified independent human case, original event outcome or empirical forecast success is provided, no chart recast or runtime promotions claimed.

**After authenticated publication:** cumulative Lilly **5,161** + Ptolemy **1,066** = **6,227 historical documentary records**. New independent empirically validated astrology predictions zero; runtime model changes zero.

Owner archive: Astrology-Lilly-Chapter-LXXXVIII-Printed-LXXXVII-Hopes-Documentary-20261016.zip in laptop Downloads. ZIP CRC, every member SHA-256 and extracted test replay verified (15).

NEXT original printed Chapter LXXXVIII / editorial LXXXIX, *Of the agreeing of Friends*, starts PDF493. The full historical source research remains OPEN.
"""
PREFIX="""# Original Lilly source study — printed LXXXVII / editorial LXXXVIII Eleventh House

2026-10-16: original first-edition Eleventh House source locally admitted, 48 historical documentary R5114–R5161. After authenticated publication total **5,161 Lilly + 1,066 Ptolemy = 6,227**. Original printed chapter **LXXXVII**, stable editorial sequence **LXXXVIII**, established duplicated LXXXV original crosswalk unchanged. Next printed LXXXVIII / editorial LXXXIX *Of agreeing of Friends* starts original PDF493. No verified predictions or model promotions. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04h_CHAPTER_LXXXVIII_COMPLETE.md.

---

"""
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);OLDCUR.write_bytes(CUR.read_bytes())
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CUR.write_text(PREFIX+OLDCUR.read_text(),encoding='utf-8')
LATEST.write_text(REPORT,encoding='utf-8')
receipt={'batch':'B04h','status':'GUARDED_CANONICAL_PREPARED_PENDING_GITHUB',
 'previous_index_git_blob_sha1':oldblob,'previous_index_sha256':H(OLD),
 'new_index_sha256':H(I),'current_state_sha256':H(CUR),
 'latest_state_sha256':H(LATEST),'accepted_source_rules_sha256':A['rules_sha256'],
 'owner_archive_sha256':Z['archive_sha256'],'new_documentary_records':48,
 'lilly_if_published':5161,'ptolemy_retained':1066,'combined_if_published':6227,
 'next_editorial_chapter':'LXXXIX','next_original_printed_chapter':'LXXXVIII',
 'next_original_pdf_page':493,'independently_verified_hopes':0,
 'new_empirical_validations':0,'runtime_promotions':0,'remote_published':False}
REC.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2))
