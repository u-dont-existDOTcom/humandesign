"""Advance only the four source-audit progress documents at the known baseline."""
from pathlib import Path
import json
import re
import subprocess

ROOT=Path.cwd()
T=ROOT/'tasks/astro-source-audit-multipass-20261005'
B=T/'batches/B01j'
BASE='cb5defe17dafc0c7f3e220432609f5eccf8ffaec'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()=='research/astro-source-audit-b01j-20261006'
def load(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
rules=load(B/'RULES.json')['records'];receipt=load(B/'READING_RECEIPT.json')
assert len(rules)==74 and len(receipt['chapter_spans'])==4
nxt='IV.5-IV.6; start Of Marriage on PDF417/printed393; stop before IV.7 Of Friends and Enemies on shared PDF437/printed413'
cp=load(T/'CURRENT_PASS.json')
assert cp['source_rule_records']==333 and cp['counts']['ptolemy_read_sections']==38 and cp['next_batch']=='B01j'
cp.update(completed='Source intake; English Ptolemy Books I/III complete and IV.1-IV.4; prior Rhetorius witness/OCR qualifications retained',current='B01j complete: wealth, status, action and four targeted source comparisons; parent OPEN',next_batch='B01k',next_range=nxt,last_verified_unit='IV.4 closing paragraph and relevant notes on PDF417/printed393 before IV.5',source_rule_records=407,latest_reports=['batches/B01j/REPORT.md','batches/B01j/VERIFICATION.json'],counting_note='407 Ptolemy source records; 19 new occupation branches, five wealth channels, four bases of honour, four action sign classes and four lunar-role groups. Eight targeted cross-source comparisons in total. None is an independent predictive trial.')
cp['counts'].update(ptolemy_read_sections=42,ptolemy_unread_sections=19,source_records=407,isolated_definition_tests=252,ptolemy_book_IV_read_sections=4,targeted_cross_source_comparisons=8,action_occupation_branches=19)
cp['stop_admission']={'parent_status':'OPEN','remaining_gap':'Ptolemy IV.5-IV.10 and BookII; remaining books; full cross-author reconciliation; compilation and person-level evaluation.','next_action':nxt,'authority':'Owner-approved multiple-pass source audit and this continuation.','executed_this_increment':'Completed IV.1-IV.4:74 records,19 occupational branches,four targeted Rhetorius comparisons and61 bounded checks.','delivery_boundary':'Completed declared source-reading batch under the existing explicit multiple-pass pause contract; no parent-completion or background-execution claim.'}
save(T/'CURRENT_PASS.json',cp)
plan=load(T/'PASS_PLAN.json')
for p in plan['passes']:
 if p['id']=='P2':p['status']='PTOLEMY_61_INDEXED;42_ENGLISH_SECTIONS_READ_MAPPED'
 if p['id']=='P3':p['status']='ENGLISH_I_III_COMPLETE_AND_IV1_IV4;407_SOURCE_RECORDS;REMAINDER_OPEN'
 if p['id']=='P4':p['status']='252_SOURCE_REFERENCE_CHECKS;EIGHT_TARGETED_RHETORIUS_COMPARISONS;FULL_RECONCILIATION_PENDING'
track=next(x for x in plan['batches'] if x['id']=='B01')
assert not any(x['id']=='B01j' for x in track['completed_subbatches'])
track['next']=nxt
track['completed_subbatches'].append({'id':'B01j','scope':'Full English IV.1-IV.4 and relevant notes; targeted Rhetorius23-25/82 comparisons','source_records':74,'new_predictions':0,'tests':61,'test_scope':'Caller-qualified route reconciliation, source lookup and record integrity; not a chart or prediction engine.','targeted_cross_source_comparisons':4})
save(T/'PASS_PLAN.json',plan)
d=load(T/'SECTION_DISCOVERY.json');assert d['read_sections_count']==38
for sp in receipt['chapter_spans']:
 chapter=int(sp['chapter'].split('.')[1]);s=next(x for x in d['sections'] if x['book']=='IV' and x['chapter']==chapter)
 assert not s.get('status','').startswith('READ_')
 s.update(status='READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE',locator_status='ENGLISH_SPANS_VERIFIED',rule_ids=sp['record_ids'],english_pdf_pages=sp['english_pdf_pages'],reading_receipt='batches/B01j/READING_RECEIPT.json',boundary=sp['boundary'])
d.update(read_sections_count=42,indexed_unread_count=19,body_locators_warning='English Books I and III and IV.1-IV.4 fully read/extracted. IV.5/IV.6/IV.7 headings located only; remaining six BookIV sections and all13 BookII sections remain unaudited.')
save(T/'SECTION_DISCOVERY.json',d)
p=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md';s=p.read_text()
s=s.replace('Full English Ptolemy Book I (24/24) and Book III (14/14) are read/extracted.','Full English Ptolemy Book I (24/24), Book III (14/14) and IV.1-IV.4 are read/extracted.')
s=s.replace('61 indexed Ptolemy sections,38 read,23 unread.','61 indexed Ptolemy sections,42 read,19 unread.')
s=s.replace('- Task `batches/B01h/REPORT.md` and `VERIFICATION.json` — integrated B01h/B01i report and actual tests.','- Task `batches/B01j/REPORT.md`, `VERIFICATION.json`, `RULES.json`, `EXTERNAL_FORTUNE_TABLES.json`, `CROSS_SOURCE_COMPARISONS.json` and reading/unresolved receipts — current wealth/status/action batch.\n- Prior `batches/B01h/REPORT.md` and `VERIFICATION.json` retain BookIII completion evidence.')
s=s.replace('Previous227 source records plus B01h45 and B01i61 =333.','Previous333 source records plus B01j74 =407. B01j has19 occupation branches, five acquisition-channel rows, four honour-basis rows, four sign-form modifier classes and four Moon-Mercury groups covering ten signs. Four new targeted comparisons bring the total to eight.')
s=s.replace('191 source/reference checks plus34 methodology checks','252 source/reference checks plus34 methodology checks')
start=s.index('## Next executable batch');end=s.index('## New B01h/B01i cautions',start)
s=s[:start]+'''## Next executable batch
**B01k: English IV.5-IV.6.** Start Of Marriage on PDF417/printed393; IV.6 Of Children begins PDF433/printed409; stop before IV.7 Of Friends and Enemies on shared PDF437/printed413. These headings are verified, not audited. Six BookIV sections and all13 BookII mundane/general sections remain unread.

## New B01j cautions
Material acquisition, retention/loss, status level, security, source of power, occupation type, amplitude and time are separate outputs. IV.2 repeats same-formula Fortune but Robbins doubts the clause; the historical formula stays frozen. An inheritance match is not automatically a duration/retention match. Dignity/status here is not essential dignity or moral goodness.

IV.4 has two ruler-selection routes. A shared planet counts once; distinct planets are both retained, with source-grounded precedence when known. Fallback requires two known-absent routes; unknown astronomy is not absence. Only three planets have listed action-quality profiles; a selected Saturn/Jupiter has no invented conversion. The helper only reconciles caller-supplied evidence and retrieves rows; it does not determine astronomical qualification.

Rhetorius23-25 has multiple attendance definitions. Rhetorius82 adds a seven-day before/after appearance window and extra action routes, while expressly reusing Ptolemy for later sign/Moon-Mercury material. Source dependence is not independent corroboration. Aspected versus overcoming is a verified translation/witness-level difference, not a claimed Greek collation. Source terrestrial/quadrupedal class lists are not silently replaced with modern element memberships. Cold/colour-mixture wording remains unresolved. IV.10 timing dependencies remain pending.

'''+s[end:]
p.write_text(s)
print('CHECKPOINT_UPDATED:42/61;407 records;B01k next')
