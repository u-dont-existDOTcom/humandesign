"""Advance only the four existing source-audit progress files, with guards."""
from pathlib import Path
import json
import subprocess

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
TASK=ROOT/'tasks/astro-source-audit-multipass-20261005'
BASE='52a6abe9aee9bc70b467dbe4802650cd779e3090'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
rules=json.loads((B/'RULES.json').read_text())
assert rules['records_count']==93
current=json.loads((TASK/'CURRENT_PASS.json').read_text())
assert current['counts']['source_records']==407 and current['counts']['ptolemy_read_sections']==42
next_range='IV.7-IV.8; start Of Friends and Enemies on PDF437/printed413; travel starts PDF447/printed423; stop before IV.9 on PDF451/printed427'
counts=current['counts'];counts.update(source_records=500,ptolemy_read_sections=44,ptolemy_unread_sections=17,isolated_definition_tests=311,targeted_cross_source_comparisons=11,ptolemy_book_IV_read_sections=6,spouse_reference_profiles=10,marriage_continuity_quality_cells=4)
current.update(completed='Source intake; English Books I/III and IV.1-IV.6; prior witness/OCR qualifications retained',current='B01k complete: marriage and children; parent corpus audit remains OPEN',source_rule_records=500,next_batch='B01l',next_range=next_range,last_verified_unit='IV.6 turned-reference closing sentence on PDF437/printed413, before IV.7',latest_reports=['batches/B01k/REPORT.md','batches/B01k/VERIFICATION.json'],counting_note='500 Ptolemy source records;10 conditional spouse rows and4 continuity/quality cells are data representations, not independent trials. Eleven targeted cross-source comparisons in total.')
current['stop_admission'].update(remaining_gap='Ptolemy IV.7-IV.10 and BookII; other available books; full cross-author reconciliation, later compilation and evaluation.',next_action=next_range,executed_this_increment='Read/extract IV.5-IV.6:93 records,10 spouse rows,4 continuity/quality cells,3 source comparisons and59 new bounded checks.',delivery_boundary='Completed declared reading increment under the existing explicit multiple-pass pause contract; no claim that the parent goal is complete or that unattended work continues.')
(TASK/'CURRENT_PASS.json').write_text(json.dumps(current,indent=2)+'\n')
plan=json.loads((TASK/'PASS_PLAN.json').read_text())
for p in plan['passes']:
    if p['id']=='P2':p['status']='PTOLEMY_61_INDEXED;44_ENGLISH_SECTIONS_READ_MAPPED'
    elif p['id']=='P3':p['status']='ENGLISH_I_III_COMPLETE_AND_IV1_IV6;500_SOURCE_RECORDS;REMAINDER_OPEN'
    elif p['id']=='P4':p['status']='311_SOURCE_REFERENCE_CHECKS;ELEVEN_TARGETED_RHETORIUS_COMPARISONS;FULL_RECONCILIATION_PENDING'
b=plan['batches'][0];assert b['id']=='B01'
b['next']=next_range
b['completed_subbatches'].append({'id':'B01k','scope':'Full English IV.5-IV.6 and relevant notes; targeted Rhetorius104-106 comparison','source_records':93,'new_predictions':0,'tests':59,'test_scope':'Phase-reference geometry, caller-qualified source lookups, unknown/absent and co-triggered flags, provenance/coverage. Not a natal/fertility or relationship-safety engine.','targeted_cross_source_comparisons':3})
(TASK/'PASS_PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
discovery=json.loads((TASK/'SECTION_DISCOVERY.json').read_text());assert discovery['read_sections_count']==42
coverage=json.loads((B/'SECTION_COVERAGE.json').read_text())['sections']
for sec in coverage:
    chapter=int(sec['chapter'].split('.')[1]);row=next(r for r in discovery['sections'] if r['book']=='IV' and r['chapter']==chapter)
    assert row['status']=='INDEXED_NOT_READ'
    row.update(status='READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE',locator_status='ENGLISH_SPANS_VERIFIED',rule_ids=sec['record_ids'],english_pdf_pages=sec['english_pdf_pages'],reading_receipt='batches/B01k/READING_RECEIPT.json',boundary=sec['boundary'])
for row in discovery['sections']:
    if row['book']=='IV' and row['chapter'] in [7,8,9]:row['locator_status']='HEADING_LOCATED_ONLY_NOT_CHAPTER_READ'
discovery.update(read_sections_count=44,indexed_unread_count=17,body_locators_warning='English Books I/III and IV.1-IV.6 read/extracted; IV.7-IV.9 headings located only. Four BookIV sections and all13 BookII sections remain unaudited.')
(TASK/'SECTION_DISCOVERY.json').write_text(json.dumps(discovery,indent=2)+'\n')
p=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md';s=p.read_text()
s=s.replace('and IV.1-IV.4 are read/extracted.','and IV.1-IV.6 are read/extracted.',1)
s=s.replace('42 read,19 unread.','44 read,17 unread.',1)
s=s.replace('- Task `batches/B01j/REPORT.md`,', '- Task `batches/B01k/REPORT.md`, `VERIFICATION.json`, `RULES.json`, `RELATIONSHIP_FAMILY_TABLES.json`, `CROSS_SOURCE_COMPARISONS.json` and reading/uncertainty receipts — current marriage/children batch.\n- Prior `batches/B01j/REPORT.md`,',1)
s=s.replace('Previous333 source records plus B01j74 =407.','Previous407 source records plus B01k93 =500. B01k has10 conditional spouse profiles,4 continuity/quality cells and3 targeted comparisons (11 total).',1)
s=s.replace('252 source/reference checks plus34 methodology checks','311 source/reference checks plus34 methodology checks',1)
start=s.index('**B01k:');end=s.index('\n\n## New B01j cautions',start)
s=s[:start]+'''**B01l: English IV.7-IV.8.** Start Of Friends and Enemies on PDF437/printed413; travel starts PDF447/printed423; stop before IV.9 on PDF451/printed427. Headings located only. Four BookIV and all13 BookII chapters remain unaudited.

## New B01k cautions
In IV.5, eastern lunar quadrants are phases (new/full to quarters), but eastern solar quadrants are horizon-relative. Do not reuse the lunar formula for the Sun; exact phase endpoints remain unresolved. Age predictions are disjunctions: early marriage OR younger partner, not both. Single/multiple marriage clauses may co-trigger; no priority supplied.

Spouse description uses Moon for the male-native branch and Sun for the female-native branch; native love disposition uses Mars/Venus instead. Historical source sex branches are not an identity classifier. Cross-chart luminary harmony concerns endurance; benefic/malefic testimony separately concerns quality. Lasting and unpleasant, or disrupted and affectionate/recurrent, are explicit possibilities. Mixed testimony stays unresolved. Venus-Saturn can be pleasant/firm here; scope and the Mars exception matter. Saturn/Jupiter variant and the implicit Saturn in the male restraint sequence remain explicit.

IV.6 children starts from MC/Good Daemon and only then opposite-place fallback when primary candidates are absent. Unknown is not absence. Giving/limiting groups are topic-specific, not ordinary sect; Mercury has both phase and association conditions. Bicorporeal AND feminine differs from an invented OR. Childlessness is not equivalent to having children who later suffer; affection, inheritance, survival and sibling relations stay separate. The turned child reference is not the child's independently observed birth chart.

Rhetorius104 expresses numerical caution but still attempts a method. His sibling groups and sterile-sign list in105-106 concern a different topic; neither the changed Moon role nor broader list is treated as a direct contradiction of Ptolemy's child example list. Raw sources remain private; no new personal prediction or runtime promotion.
''' + s[end:]
p.write_text(s)
print('CHECKPOINT_UPDATED:44/61;500 records;B01l next')
