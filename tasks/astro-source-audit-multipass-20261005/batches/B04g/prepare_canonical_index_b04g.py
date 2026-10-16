from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDX=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CUR=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04g_CHAPTER_LXXXVII_COMPLETE.md'
OLD=B/'recovery/LILLY_INDEX_AFTER_CROSSWALK_BEFORE_B04g_CANONICAL.json'
OLDCUR=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B04g.md'
REC=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261016.json'
assert not any(p.exists() for p in (LATEST,OLD,OLDCUR,REC))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
raw=IDX.read_bytes();j=json.loads(raw)
A=json.loads((B/'ACCEPTANCE.json').read_text())
R=json.loads((B/'RULES.json').read_text())
Z=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').read_text())
P=json.loads((B/'PRINTED_NUMBERING_CORRECTION_RECEIPT_20261016.json').read_text())
C=json.loads((B/'ORIGINAL_1647_PRINTED_NUMBERING_CROSSWALK_20261016.json').read_text())
assert j['records_count']==5080 and j['batches'][-1]['id']=='B04f'
assert j['next']['chapter']=='LXXXVII' and j['next']['printed_chapter_numeral']=='LXXXVI' and j['next']['pdf_page']==490
assert j['read_numbered_chapters']==list(range(1,87))
assert j['read_numbered_chapters_basis']=='editorial_source_sequence_ordinals_not_literal_1647_headings'
assert j['source_sha256']==A['original_pdf_sha256']
assert H(IDX)==P['corrected_index_sha256']
assert j['original_printed_chapter_heading_crosswalk']['sha256']==H(B/'ORIGINAL_1647_PRINTED_NUMBERING_CROSSWALK_20261016.json')
assert j['empirical_validations']==j['runtime_promotions']==0
assert A['prior_lilly_accepted']==5080 and A['new_documentary_records']==33
assert A['lilly_if_published']==5113 and A['combined_if_published']==6179
assert R['record_count']==33 and R['source_original_printed_chapter']=='LXXXVI'
assert [r['record_number'] for r in R['rules']]==list(range(5081,5114))
assert Z['zip_crc_pass'] and Z['member_hashes_pass'] and Z['full_extraction_pass'] and Z['extracted_tests_passed']==14
assert H(Z['owner_download_path'])==Z['archive_sha256']
assert H(B/'RULES.json')==A['rules_sha256']==Z['accepted_rules_sha256']
rel=str(IDX.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rel],cwd=ROOT).returncode==0
oldblob=git('rev-parse','HEAD:'+rel)
assert oldblob==git('hash-object',str(IDX))
assert C['correspondence'][2]['first_edition_heading']=='LXXXVI'
j['batches'].append({'id':'B04g','path':'batches/B04g/RULES.json','records_count':33,
 'sha256':A['rules_sha256'],
 'scope':'First-edition Lilly 1647 desired preferment question printed CHAP LXXXVI (stable editorial sequence LXXXVII) original PDF490-491/printed456-457, 31 substantive clauses including favorable Moon/Saturn testimony, false friend and author-retrospective claimed office within less than three weeks; two next-chapter navigation, 6 passages and 18 unresolved limits, no independently authenticated office outcome.'})
j['records_count']=5113
j['read_numbered_chapters'].append(87)
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_EDITORIAL_LXXXVII_PRINTED_LXXXVI_HISTORICAL_SOURCE_ONLY_NEXT_EDITORIAL_LXXXVIII_OPEN'
j['next']={'pdf_page':491,'printed_page':457,'chapter':'LXXXVIII',
 'printed_chapter_numeral':'LXXXVII','heading':'Of good or ill in questions concerning the Eleventh House',
 'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
 'position':'Original PDF491/printed457 below florid Eleventh House divider. Original CHAP. LXXXVII, stable editorial sequential LXXXVIII following duplicated printed LXXXV.'}
j['chapter_LXXXVII_source_acceptance_note']='33 historical annotations R5081–R5113 from first-edition printed CHAP. LXXXVI, stable editorial LXXXVII. Anonymous querent said to obtain office within three weeks, unverified false friend and earlier petitions. Crosswalk preserves original duplicate LXXXV. Zero independent empirical predictive validations.'
j['current_state']=str(LATEST.relative_to(ROOT))
assert j['records_count']==sum(k['records_count'] for k in j['batches'])==5113
assert j['read_numbered_chapters']==list(range(1,88))
report="""# Lilly first edition — Printed Chapter LXXXVI, editorial LXXXVII — Preferment desired

2026-10-16 — Africa/Dakar (UTC+0). Original William Lilly, Christian Astrology, 1647, Wellcome b30338724. Source full PDF SHA-256 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

**Numeral correction:** The first edition prints CHAP. LXXXV twice for the Prince Rupert/Essex and Irish forces questions. Consequently this following appointment case on original PDF490/printed456 is literally headed **CHAP. LXXXVI**, whereas its stable sequential research alias is **LXXXVII**. The new Eleventh House chapter beginning PDF491/printed457 is originally printed LXXXVII, editorial LXXXVIII. An original-image crosswalk and high-resolution header evidence preserve both numbering systems without modifying any prior R record or batch SHA-256.

**Original chapter boundaries:** The new applicant inquires four or five minutes after the preceding question, which has no clearly printed absolute chart date. LXXXVI's body runs PDF490 below the previous divider and PDF491 through the purported friend evidence. A floral divider then introduces the Eleventh House, followed by the new printed LXXXVII heading.

**Historical source reasoning:** Ascendant and Venus signify the applicant, tenth the desired office. The Moon in tenth and its trine to Saturn exalted in the rising sign, mutually receiving Venus, suggest eventual appointment. Yet the Sun, eleventh lord in seventh and opposite ascendant with south node, is used to characterize an alleged false friend who covertly opposed the applicant. Lilly states the office was gained within **less than three weeks** despite obstacles. He reports the friend had a conspicuous scar, dark coloring, and that earlier petitions were unsuccessful. These are unverified **authorial retrospective outcomes**, not source-independent historical facts, diagnoses, or evidence about ethnicity.

**Documentary acceptance:** 33 original historical annotations R5081–R5113, 31 substantive and two following Eleventh-House navigation markers; six original passage groups, eighteen source limits; original PDF490 and 491 JPEG witness images frozen to SHA-256. The crosswalk is exact-byte traceable and original printed/sequence labels recorded in every source record. The source, archive and index tests pass. No actual applicant/appointment independently authenticated, no absolute figure date verified, no independent astrological prediction validation or runtime rule changes.

**After authenticated research branch publication:** Lilly **5,113** + retained Ptolemy **1,066** = **6,179 historical documentary records**.

Owner ZIP in laptop Downloads: Astrology-Lilly-Chapter-LXXXVII-Printed-LXXXVI-Preferment-Documentary-20261016.zip, with CRC, individual member SHA-256 and full re-extraction replay tests.

**Next:** Original printed Chapter LXXXVII / editorial LXXXVIII — Eleventh House good/ill and hopes, PDF491/printed457 below separator. Parent source study remains OPEN.
"""
prefix="""# Original Lilly research current — Printed LXXXVI / editorial LXXXVII

2026-10-16: Printed original LXXXVI preferment source locally accepted as stable sequential LXXXVII, 33 records R5081–R5113. After authenticated publication: **5,113 Lilly + 1,066 Ptolemy = 6,179** historical records. An original-edition double-printed CHAP. LXXXV is frozen in a source/image crosswalk rather than hidden by renumbering. Next original printed LXXXVII (editorial LXXXVIII) Eleventh House starts PDF491. Zero new empirical predictions or runtime promotions. See state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261016_B04g_CHAPTER_LXXXVII_COMPLETE.md.

---

"""
OLD.parent.mkdir(parents=True,exist_ok=True)
OLD.write_bytes(raw);OLDCUR.write_bytes(CUR.read_bytes())
IDX.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
CUR.write_text(prefix+OLDCUR.read_text(),encoding='utf-8')
LATEST.write_text(report,encoding='utf-8')
receipt={'batch':'B04g','status':'GUARDED_CANONICAL_PREPARED_PENDING_GITHUB',
 'previous_index_git_blob_sha1':oldblob,'previous_index_sha256':H(OLD),
 'new_index_sha256':H(IDX),'current_state_sha256':H(CUR),
 'latest_state_sha256':H(LATEST),'accepted_source_rules_sha256':A['rules_sha256'],
 'printed_numeral_crosswalk_sha256':H(B/'ORIGINAL_1647_PRINTED_NUMBERING_CROSSWALK_20261016.json'),
 'owner_archive_sha256':Z['archive_sha256'],'new_documentary_records':33,
 'lilly_if_published':5113,'ptolemy_retained':1066,'combined_if_published':6179,
 'next_editorial_chapter':'LXXXVIII','next_original_printed_chapter':'LXXXVII','next_original_pdf_page':491,
 'independently_verified_appointments':0,'new_empirical_validations':0,'runtime_promotions':0,
 'remote_published':False}
REC.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
