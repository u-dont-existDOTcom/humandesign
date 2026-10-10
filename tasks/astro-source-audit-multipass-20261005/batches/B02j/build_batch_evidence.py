"""Assemble bounded provenance, comparisons and the new cumulative index."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

HERE=Path(__file__).resolve().parent
TASK=HERE.parent.parent
REPO=TASK.parent.parent
ROOT=Path('/workspace/scratch/43f75264c32e')
SOURCE='LILLY1647_WELLCOME_B30338724'
SHA='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'

def read(p): return json.loads(p.read_text())
def write(name,data): (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

mapping=read(HERE/'RECORD_ID_MAP.json')['map']
records=read(HERE/'RULES.json')
# Preserve exact original-reader products, not a reconstructed description.
implementation=HERE/'implementation_review'; implementation.mkdir(exist_ok=True)
for name in ['IMPLEMENTATION_CHECK.md','IMPLEMENTATION_CHECK_RECEIPT.json','IMPLEMENTATION_CHECK_EVIDENCE.json','IMPLEMENTATION_TEST_OUTPUT.txt']:
    shutil.copyfile(ROOT/'reader-b'/name,implementation/name)
write('IMPLEMENTATION_RECONCILIATION.json',{'initial_diagnosis':'implementation_review/IMPLEMENTATION_CHECK.md','initial_snapshot_32_tests_passed':True,'current_fixture_results_affected':False,'repairs':[
 {'finding':'String dependencies silently disappear from body grouping','disposition':'CONFIRMED_AND_REPAIRED','change':'Explicit nonempty list/tuple of nonempty names required by tally and grouping; regression subcase rejects a string.'},
 {'finding':'Boolean aspect ray and absent target bypass intended validation','disposition':'CONFIRMED_AND_REPAIRED','change':'Validate four integer inputs before arithmetic; regressions reject True and None.'},
 {'finding':'Generic same-calendar label hides Gregorian leap convention','disposition':'CONFIRMED_SCOPE_GAP_REPAIRED','change':'Helper restricted to same-year date labels both after February, where Gregorian/Julian month lengths agree; 1700 February ambiguity is rejected. April–July1645 remains95days.'}],
 'final_verification':'TEST_RUN_SUMMARY.json','unique_tests_in_final_suite':36,'earlier32_are_subset_not_additional_tests':True,'independence':'Collaborative implementation check by source reader B; distinct from fresh-context final claim diagnosis.'})
retained=[]
for batch,tails in [('B02a',['R033']),('B02c',['R265','R266']),('B02e',['R625'])]:
    path=TASK/'batches'/batch/'RULES.json'; data=read(path)
    rows=data if isinstance(data,list) else data.get('rules',data.get('records',[]))
    for row in rows:
        if any(row['id'].endswith(t) for t in tails): retained.append({'source_batch':batch,'original_file_sha256':sha(path),'record':row})
write('RETAINED_SOURCE_EXCERPTS.json',{'purpose':'Exact four retained records used for targeted comparison; no rewriting or new retained-record credit.','original_images_reopened_this_turn':[67,123,177,178],'records':retained})
write('CROSS_SOURCE_COMPARISONS.json',{'scope':'Targeted within-Lilly comparison with retained source records; Ptolemy registry retained, not reread or validated in this batch.','comparisons':[
 {'id':'X01','retained':['LI.1647.I.XVI.divisions.R265'],'new':[mapping['A001'],mapping['A012']],'relation':'SAME_NAMED_CLASS','finding':'Cancer, Scorpio, Pisces match the earlier fruitful group. Preserve the new question-specific antecedents.'},
 {'id':'X02','retained':['LI.1647.I.XVI.divisions.R266'],'new':[mapping['A013'],mapping['C002']],'relation':'CONTEXTUAL_SUBSET_AND_WORKED_LANGUAGE','finding':'Earlier barren class is Gemini, Leo, Virgo; one local recipe names only Leo/Virgo, while the worked narrative calls Sagittarius/Gemini rather barren. No global replacement or missing-sign insertion is made.'},
 {'id':'X03','retained':['LI.1647.II.XXIII.R625'],'new':[mapping['C001'],mapping['C018'],mapping['B028']],'relation':'DISTINCT_PARTS_SHARED_PROJECTION_CONVENTION','finding':'Fortune uses Asc+Moon−Sun; Part of Children uses Asc+Jupiter−Mars with explicit same-day/night instruction. Static checks against both figures are conditional on declared sign readings.'},
 {'id':'X04','retained':['LI.1647.I.04.R033'],'new':[mapping['C027'],mapping['C028']],'relation':'POSSIBLE_CUSP_VIRTUE_QUALIFICATION','finding':'Moon and Saturn are geometrically in sectors4/8 but4°11′/0°43′ before cusps5/9. Earlier five-degree cusp virtue may matter to the source masculine-house votes; it is not an explicitly stated resolution here.'}
]})
# Errata are source-supplied readings, separate from new doctrine and open edits.
a=read(HERE/'source_readers/a/SECTION_COVERAGE.json')
b=read(HERE/'source_readers/b/ERRATA_CHECK.json')
write('ERRATA_CHECKS.json',{'source_id':SOURCE,'same_witness_pdf_page':888,'scope':'Targeted original-edition errata check, not a new textual witness or full-book collation.','entries':[
 {'id':'AE001','target_printed_page':224,'target_pdf_page':258,'line':10,'reading':'consideration','status':'SOURCE_RESOLVED_LEXICAL_CORRECTION','effect':'Wording only; no timing operator, house or value changed.','evidence':'source_readers/a/AFTER_FREEZE_SOURCE_SUPPLEMENT.md'},*b['entries']],
 'worked_pages_238_240_241_242':'No targeted entry identified in the inspected errata page; the hour-lord, cusp and solar mismatches remain unresolved.'})
checks=[
 ('T01',[258],'Second house in time map','The original says second house→second year; the unusual map is preserved.','source_readers/a/SECTION_COVERAGE.json'),
 ('T02',[263],'Adverse sign list','Aries, Cancer, Libra, Capricorn are retained exactly as named by glyphs.','source_readers/b/SOURCE_FIRST_NOTES.md'),
 ('T03',[265],'Delivery conjunction planets','Mars and Sun, not a replacement pair, begin the conjunction prescription.','source_readers/b/SOURCE_FIRST_NOTES.md'),
 ('T04',[266],'Part of Children direction','Mars to Jupiter projected from ascendant, day and night.','source_readers/b/SOURCE_FIRST_NOTES.md'),
 ('T05',[274,275],'Conflicting hour ruler','Figure labels day/hour with Moon; table names Jupiter as hour lord. No repair selected.','evidence/chart2-center.png'),
 ('T06',[274,276],'Solar minutes','Levelled original figure detail reads27°52′; later prose says27°48′ Cancer in perfect square. Both remain.','evidence/chart2-sun-level.png'),
 ('T07',[272],'Opposite cusp minutes','Third19°20′ and ninth19°10′ are transcribed; no opposite-cusp repair.','evidence/chart1-opposite-cusps.png'),
 ('T08',[274,276],'Missing versus supplied Mercury minutes','Figure11 with omitted minutes; later table11°00′. Separate witnesses retained.','WORKED_NUMERIC_TABLES.json'),
 ('T09',[888],'Erratum page target','The entry near this material is209, not229; it is outside the new span.','source_readers/b/ERRATA_CHECK.json')]
write('TEXT_IMAGE_CHECKS.json',{'checks':[{'id':i,'pdf_pages':p,'subject':s,'finding':f,'evidence':e} for i,p,s,f,e in checks],'policy':'Resolved glyph readings do not resolve the cause of source conflicts. Reconstructed prose anchors are not represented as diplomatic quotations.'})
evidence=HERE/'evidence'; evidence.mkdir(exist_ok=True)
for name in ['chart2-sun-level.png','chart1-opposite-cusps.png','chart2-center.png']:
    shutil.copyfile(ROOT/'source-pages'/name,evidence/name)
# Full worked pages are already read; include compact witnesses for both figures/tables.
import fitz
pdf=fitz.open('/workspace/scratch/bd2460f96de0/Lilly-1647-Christian-Astrology-I-III.pdf')
for n in [272,274,275,276]:
    pdf[n-1].get_pixmap(matrix=fitz.Matrix(1,1)).save(evidence/f'original-pdf{n}.png')
reading={'batch':'B02j','source_id':SOURCE,'original_pdf_sha256':SHA,'original_pdf_bytes':141842963,'original_pdf_pages':894,'hash_recomputed_this_turn_by_root_and_independent_reader':True,
 'root_full_admitted_page_images_read':list(range(256,277)),
 'number_of_distinct_admitted_pages':21,
 'boundary_only_page':{'pdf':277,'printed':243,'extracted':False},
 'targeted_retained_source_comparison_images_read':[67,123,177,178],
 'targeted_original_errata_page_read':888,
 'producer_source_reading':{'A':{'pages':list(range(256,264)),'notes':'source_readers/a/SOURCE_FIRST_NOTES.md','sha256':sha(HERE/'source_readers/a/SOURCE_FIRST_NOTES.md')},'B':{'pages':list(range(263,273)),'notes':'source_readers/b/SOURCE_FIRST_NOTES.md','sha256':sha(HERE/'source_readers/b/SOURCE_FIRST_NOTES.md')},'root':{'worked_pages':list(range(272,277)),'notes':'ROOT_SOURCE_FIRST_NOTES.md','sha256':sha(HERE/'ROOT_SOURCE_FIRST_NOTES.md'),'later_full_span_review':True}},
 'independent_reader':{'fresh_context':True,'source_pages':list(range(256,277)),'notes_sha256':'68dacb1f4342ffcffbac1f2fa9fe50c1180d337113a373bb3dff4682d5b6b69a','source_before_candidates':True,'independence_limit':'Same model, separate source-first context; no cross-family or external-expert claim.'},
 'source_image_manifest':[{'path':'evidence/'+p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(evidence.iterdir())],
 'evidence_limits':'Original-source inspection is not ephemeris verification, clinical validation or predictive accuracy. Inferred diagram signs remain labelled; no participant-data reads or model fits.'}
write('READING_RECEIPT.json',reading)
# Preserve all earlier index entries exactly as parsed from the base revision.
index_path='tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json'
old_bytes=subprocess.check_output(['git','show','220b2e9:'+index_path],cwd=REPO)
(HERE/'RETAINED_LILLY_INDEX_BEFORE.json').write_bytes(old_bytes)
idx=json.loads(old_bytes)
idx['records_count']+=records['records_count']
idx['status']='BOOK_I_COMPLETE_BOOK_II_THROUGH_XLIII_READ_OTHER_SECTIONS_OPEN'
idx['read_numbered_chapters']+=list(range(39,44))
idx['read_headed_units_count']+=5
idx['batches'].append({'id':'B02j','path':'batches/B02j/RULES.json','records_count':records['records_count'],'sha256':sha(HERE/'RULES.json'),'scope':records['scope']})
idx['next']=read(HERE/'SECTION_COVERAGE.json')['next']
idx['current_state']='state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261010_B02j.md'
(TASK/'LILLY_SOURCE_EXTRACTION_INDEX_V1.json').write_text(json.dumps(idx,ensure_ascii=False,indent=2)+'\n')
write('LILLY_SOURCE_EXTRACTION_INDEX_SNAPSHOT.json',idx)
ptolemy=read(TASK/'PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json')
write('COUNTS.json',{'new_source_records':records['records_count'],'first_record_number':1157,'last_record_number':1156+records['records_count'],'new_general_methodological_illustrative_records':records['general_records_count'],'new_worked_case_records':records['worked_example_records_count'],'cumulative_lilly_records':idx['records_count'],'retained_ptolemy_records':ptolemy['source_records'],'combined_source_records':idx['records_count']+ptolemy['source_records'],'typed_limit_entries':read(HERE/'UNRESOLVED.json')['issues_count'],'coverage_units':27,'new_numbered_chapters':5,'historical_enquiries':2,'dated_enquiries':2,'printed_charts':2,'coordinate_entries':45,'sex_testimony_rows':12,'final_focused_tests':36,'retained_tests_newly_claimed':0,'runtime_promotions':0,'predictive_accuracy_evaluated':False})
print(json.dumps(read(HERE/'COUNTS.json')))
