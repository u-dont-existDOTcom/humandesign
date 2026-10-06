"""Advance the four source-audit progress files from the exact B01k base."""
from pathlib import Path
import json
import subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
TASK=ROOT/'tasks/astro-source-audit-multipass-20261005'
BASE='8a5db171e197958adc5d0d44d6585f35b9b5e1ab'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
rules=json.loads((B/'RULES.json').read_text());assert rules['records_count']==71
c=json.loads((TASK/'CURRENT_PASS.json').read_text())
assert c['counts']['source_records']==500 and c['counts']['ptolemy_read_sections']==44
nxt='IV.9; start Of the Quality of Death on PDF451/printed427; stop before IV.10 on PDF461/printed437. Historical source extraction only.'
c['counts'].update(source_records=571,ptolemy_read_sections=46,ptolemy_unread_sections=15,isolated_definition_tests=375,targeted_cross_source_comparisons=14,ptolemy_book_IV_read_sections=8,temporary_association_pair_rows=10)
c.update(completed='Source intake; English Books I/III and IV.1-IV.8; prior source-witness qualifications retained',current='B01l complete: friends/enemies and foreign travel; parent audit OPEN',source_rule_records=571,next_batch='B01m',next_range=nxt,last_verified_unit='IV.8 closing travel sentence and relevant notes on PDF451/printed427; IV.9 heading located only',latest_reports=['batches/B01l/REPORT.md','batches/B01l/VERIFICATION.json'],counting_note='571 Ptolemy source records. Ten temporary cross-chart encounter rows, four relationship bases and six hazard branches are structured source data, not independent human observations. Fourteen targeted comparisons in total.')
c['stop_admission'].update(remaining_gap='Ptolemy IV.9-IV.10 including both endings, all BookII; other supplied books; full source reconciliation, compilation and evaluation.',next_action=nxt,executed_this_increment='Full English IV.7-IV.8 and relevant notes:71 records,10 temporary encounter rows,3 targeted Rhetorius comparisons,64 new bounded checks.',delivery_boundary='Completed source-reading increment under owner-approved multiple-pass pause contract; parent not complete and no unattended work claimed.')
(TASK/'CURRENT_PASS.json').write_text(json.dumps(c,indent=2)+'\n')
plan=json.loads((TASK/'PASS_PLAN.json').read_text())
for p in plan['passes']:
 if p['id']=='P2':p['status']='PTOLEMY_61_INDEXED;46_ENGLISH_SECTIONS_READ_MAPPED'
 elif p['id']=='P3':p['status']='ENGLISH_I_III_COMPLETE_AND_IV1_IV8;571_SOURCE_RECORDS;REMAINDER_OPEN'
 elif p['id']=='P4':p['status']='375_SOURCE_REFERENCE_CHECKS;FOURTEEN_TARGETED_RHETORIUS_COMPARISONS;FULL_RECONCILIATION_PENDING'
b=plan['batches'][0];assert b['id']=='B01';b['next']=nxt
assert not any(s['id']=='B01l' for s in b['completed_subbatches'])
b['completed_subbatches'].append({'id':'B01l','scope':'Full English IV.7-IV.8 and relevant notes; Rhetorius16-17 and57 opening ninth-house comparison','source_records':71,'new_predictions':0,'tests':64,'test_scope':'Source-table lookup, method/role gates, three-valued clauses, declared-frame distance probe, unknown handling and record integrity; not natal/directions or travel-risk engine.','targeted_cross_source_comparisons':3})
(TASK/'PASS_PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
d=json.loads((TASK/'SECTION_DISCOVERY.json').read_text());assert d['read_sections_count']==44
for sec in json.loads((B/'SECTION_COVERAGE.json').read_text())['sections']:
 ch=int(sec['chapter'].split('.')[1]);row=next(r for r in d['sections'] if r['book']=='IV' and r['chapter']==ch)
 assert row['status']=='INDEXED_NOT_READ'
 row.update(status='READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE',locator_status='ENGLISH_SPANS_VERIFIED',rule_ids=sec['record_ids'],english_pdf_pages=sec['english_pdf_pages'],reading_receipt='batches/B01l/READING_RECEIPT.json',boundary=sec['boundary'])
for row in d['sections']:
 if row['book']=='IV' and row['chapter'] in [9,10]:row['locator_status']='HEADING_LOCATED_ONLY_NOT_CHAPTER_READ'
d.update(read_sections_count=46,indexed_unread_count=15,body_locators_warning='English Books I/III and IV.1-IV.8 read/extracted. IV.9-IV.10 headings located only; two BookIV and all13 BookII chapters unaudited.')
(TASK/'SECTION_DISCOVERY.json').write_text(json.dumps(d,indent=2)+'\n')
p=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md';s=p.read_text()
s=s.replace('and IV.1-IV.6 are read/extracted.','and IV.1-IV.8 are read/extracted.',1).replace('44 read,17 unread.','46 read,15 unread.',1)
s=s.replace('- Task `batches/B01k/REPORT.md`,','- Task `batches/B01l/REPORT.md`, `VERIFICATION.json`, `RULES.json`, `ASSOCIATION_TRAVEL_TABLES.json` and comparison/reading receipts — current friendship/travel batch.\n- Prior `batches/B01k/REPORT.md`,',1)
s=s.replace('Previous407 source records plus B01k93 =500.','Previous500 source records plus B01l71 =571. B01l adds10 temporary encounter rows and3 targeted comparisons (14 total).',1)
s=s.replace('311 source/reference checks plus34 methodology checks','375 source/reference checks plus34 methodology checks',1)
start=s.index('**B01l:');end=s.index('\n\n## New B01k cautions',start)
s=s[:start]+'''**B01m: English IV.9.** Start quality of death at PDF451/printed427 and stop before division of times at PDF461/printed437. Historical source analysis only, no personal death or medical predictions. IV.10 and both transmitted endings remain next; all13 BookII chapters remain separately scheduled.

## New B01l cautions
IV.7 separates lasting affinities/enmities from temporary acquaintances/quarrels; both charts require Sun/Moon/ASC/Fortune roles. Choice, need and pleasure/pain are distinct bases; authority over a relationship and benefit from it have separate determinants. Co-sign/exchange and weaker aspect-only routes are not flattened. About17degrees apart in main text and within17 in Robbins’s note remain distinct; no numerical tolerance or full-chart pair aggregation is frozen.

The ten temporary pair descriptions require cross-nativity prorogations. Robbins expressly referencesIII.10 with departure in one chart and arrival in the other. Do not reuse as natal-conjunction or secondary-progression/transit rules. Epoch/latitude/time-key details and duration endpoints remain unresolved. Greater intensity is not automatically greater benefit. The slavery passage is retained in historical context, not converted into employment guidance.

IV.8 starts with luminaries/angles, especially Moon. Mars requires a setting/declining-from-MC condition AND hard relation to luminaries. Fortune extends preceding travel context; no triggered branch is not a no-travel forecast. Residence abroad, activity quality, return, direction, frequency, hazards and timing are different outputs. Robbins’s broad travel-house set3,6,7,9,12 belongs to his note, not a ninth-only substitution. Dominance/mixture applies in every case. Mercury can add gain in benefic context and danger in adverse context. Desert/hard-going alternative has no separately supplied sign class; preserve ambiguity. Ingress target is Robbins’s presumably gloss, not explicit main text.

Rhetorius16-17 retains sympathetic disjunctions and squares; do not silently insert those exceptions into Ptolemy’s different qualified framework or count source reuse as independent evidence. Rhetorius57 ninth-house method is not equivalent to Ptolemy’s angular/cadent enquiry. Source-only helpers do not evaluate real people or travel safety.
''' + s[end:]
p.write_text(s)
print('CHECKPOINT_UPDATED:46/61;571records;B01mnext')
