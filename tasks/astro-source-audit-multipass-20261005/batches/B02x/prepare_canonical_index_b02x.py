"""Prepare guarded historic-documentary-only B02x canonical index update.

Index mutation is local; atomic Git publication is separate. No replay of OCR,
no new astrology prediction, no personal chart alteration.
"""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
I=ROOT/'tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
CURRENT=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
LATEST=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02x_CHAPTER_LII_COMPLETE.md'
OLDINDEX=B/'recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B02x_CANONICAL.json'
OLDCURRENT=B/'recovery/ASTROLOGY_SOURCE_AUDIT_CURRENT_BEFORE_B02x.md'
RECEIPT=B/'CANONICAL_SOURCE_INDEX_PREPARE_RECEIPT_20261015.json'
assert not any(f.exists() for f in (LATEST,OLDINDEX,OLDCURRENT,RECEIPT))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
raw=I.read_bytes();j=json.loads(raw)
assert raw==(B/'RETAINED_CANONICAL_LILLY_INDEX_BEFORE_B02x.json').read_bytes()
assert j['records_count']==3016 and j['batches'][-1]['id']=='B02w'
assert j['read_numbered_chapters']==list(range(1,52)) and j['next']['chapter']=='LII' and j['next']['pdf_page']==403
assert j['runtime_promotions']==j['empirical_validations']==0
rp=str(I.relative_to(ROOT))
assert subprocess.run(['git','diff','--quiet','HEAD','--',rp],cwd=ROOT).returncode==0
h=lambda *cmd:subprocess.run(['git',*cmd],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
previous_git_blob=h('rev-parse','HEAD:'+rp)
assert h('hash-object',str(I))==previous_git_blob
a=json.loads((B/'ACCEPTANCE.json').read_text());r=json.loads((B/'RULES.json').read_text())
u=json.loads((B/'UNRESOLVED.json').read_text());c=json.loads((B/'CLAIM_LEDGER.json').read_text())
release=json.loads((B/'SOURCE_DOCUMENTARY_RELEASE_PACKET_RECEIPT_20261015.json').read_text())
assert a['documentary_accepted_locally'] and a['whole_chapter_lii_complete_at_documentary_source_level']
assert r['documentary_accepted_locally'] and r['whole_chapter_lii_complete_at_documentary_source_level']
assert r['record_count']==a['new_documentary_records']==55
assert [x['record_number'] for x in r['rules']]==list(range(3017,3072))
assert r['rules'][-1]['chapter']=='LIII_BOUNDARY_NAVIGATION_ONLY'
assert all(x['chapter']=='LII' for x in r['rules'][:-1])
assert len(u['issues'])==a['source_uncertainties_retained']==13
assert a['original_source_reverse_spans']==42 and a['literal_e_contra_abbreviations']==3
assert not r['accepted_as_empirical_astro_prediction'] and r['runtime_promotions']==0
assert c['empirical_predictions_validated']==c['runtime_promotions']==0
for n,k in [('RULES.json','rules_sha256'),('SOURCE_ORDER.json','source_order_sha256'),('UNRESOLVED.json','unresolved_sha256'),('CLAIM_LEDGER.json','claim_ledger_sha256'),('ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json','original_to_record_source_map_sha256'),('LII_SOURCE_FIRST_INVENTORY_NOTES_20261015.md','notes_sha256')]:
 assert sha(B/n)==a[k],n
assert release['extracted_focused_source_test_count']==20 and release['extracted_source_tests_exit_code']==0
assert release['crc_pass'] and release['member_sha256_pass'] and release['extracted_file_sha256_pass']
assert sha(release['archive_os_downloads'])==release['archive_sha256']
assert Path(release['archive_os_downloads']).stat().st_size==release['archive_bytes']
j['batches'].append({'id':'B02x','path':'batches/B02x/RULES.json','records_count':55,'sha256':a['rules_sha256'],
'scope':'Book II Chapter LII litigation, partnership, neighbors, relocation and business choices, original PDF403-405 above LIII divider; 54 chapter source units and one next-chapter navigation marker; 42 visually reviewed source spans, 13 textual issues; zero validated cases.'})
j['records_count']=3071
j['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_LII_DOCUMENTARY_SOURCE_ONLY_NEXT_LIII_OPEN'
j['read_numbered_chapters'].append(52)
j['next']={'pdf_page':405,'printed_page':371,'chapter':'LIII','heading':'Of Hunting.',
'include_opening_paragraph':True,'extracted':False,'boundary_image_read':True,
'position':'Original PDF405 BELOW horizontal divider after final Chapter LII staying/removing clause; continue printed LIII text into PDF406, including unnumbered later law-suit passage.'}
j['chapter_LII_source_acceptance_note']='55 documentary units incl next chapter boundary, 42 source-first reverse original-image spans, 13 retained textual uncertainties, three untranslated abbreviated e-contra, zero blind outcome confirmations or runtime validation. The image reviewer was not a blind independent diplomatic transcription.'
j['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02x_CHAPTER_LII_COMPLETE.md'
assert j['records_count']==sum(x['records_count'] for x in j['batches'])==3071
assert j['read_numbered_chapters']==list(range(1,53))
assert not any(x['id']=='B02x' for x in j['batches'][:-1])
body="""# Latest original astrology source audit: Lilly Chapter LII documentary complete

**2026-10-15 Africa/Dakar UTC+0. Parent multi-author astrology source study OPEN.** Document study only, not birth-chart predictive accuracy, legal-case forecasting, validated human data, or a live scoring change.

William Lilly, `Christian Astrology` original 1647 Wellcome b30338724; full original PDF SHA256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`.

Book II **Chapter LII**, `Who shall doe best in a suit of Law`, has been source-intaken from original PDF403/printed369, PDF404/printed370 and original PDF405/printed371 **above the Chapter LIII divider**. Covers suit-law, partnership, partner profits, neighbor familiarity, travel/relocation, and choose-between-business sections; the later LIII law-suit paragraph is not included.

**New B02x historical documentary units: 55 (R3017–R3071)**, including 54 Chapter LII annotations (eight original section headings and one original marginal reference among them) and one Chapter LIII boundary-only. **Retained text uncertainties: 13**; three literal `& e contra` inverse abbreviations are not silently expanded. Two page-crossing source items 403→404 and 404→405; manually mapped 42 original source spans to all 55 editorial records. Complete blind second diplomatic transcription **not claimed**.

Canonical retained original-source count after publication: **Lilly 3,071 + Ptolemy 1,066 = 4,137 documentary units**. All new units are historical statements and references, not independent horoscope successes. No confirmed real litigant or partner outcome, no verified criminal, financial or safety inference, no personal charts changed, and zero runtime model promotions. 20 tests successfully replayed from an extracted verified owner-release ZIP.

See `tasks/astro-source-audit-multipass-20261005/batches/B02x/HANDOFF_LII_DOCUMENTARY_20261015.md`, `ACCEPTANCE.json`, `RULES.json`, `UNRESOLVED.json`, `ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json` and later `PUBLICATION_RECEIPT.json` to verify actual GitHub readback.

**Next original chapter:** Lilly Book II **LIII Of Hunting**, starts original PDF405/printed371 **BELOW** divider. Continue through PDF406/printed372 and subsequent pages until the true next chapter boundary. Do not import the later unnumbered legal-suit subsection into LII solely by topic. The parent corpus study remains OPEN.
"""
current_before=CURRENT.read_bytes()
prepend="""# Current astrology source audit — authoritative latest chapter checkpoint

**CURRENT (2026-10-15):** Original Lilly **Chapter LII historical documentary intake** complete (B02x), **3,071 Lilly + 1,066 Ptolemy = 4,137** historical documentary units. Next **Chapter LIII Of Hunting** original PDF405/printed371 BELOW divider. No empirical validations or runtime model changes; parent multi-author source study OPEN. See `state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02x_CHAPTER_LII_COMPLETE.md` and the canonical index. Earlier state is retained below as recovery history.

---

"""
OLDINDEX.parent.mkdir(parents=True,exist_ok=True)
OLDINDEX.write_bytes(raw);OLDCURRENT.write_bytes(current_before)
I.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
CURRENT.write_text(prepend+current_before.decode())
LATEST.write_text(body)
rec={'batch':'B02x','kind':'CANONICAL_DOCUMENTARY_SOURCE_INDEX_PREPARED_NOT_PUBLISHED',
'previous_index_git_blob_sha1':previous_git_blob,'previous_index_sha256':sha(OLDINDEX),
'new_index_sha256':sha(I),'new_current_state_sha256':sha(CURRENT),
'new_latest_state_sha256':sha(LATEST),'rules_sha256':a['rules_sha256'],
'owner_release_sha256':release['archive_sha256'],
'accepted_source_units_added':55,'lilly_if_published':3071,'ptolemy_retained':1066,
'combined_if_published':4137,'next_chapter':'LIII','next_original_pdf':405,
'new_empirical_validations':0,'runtime_promotions':0,'canonical_published':False}
RECEIPT.write_text(json.dumps(rec,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(rec,indent=2,ensure_ascii=False))
