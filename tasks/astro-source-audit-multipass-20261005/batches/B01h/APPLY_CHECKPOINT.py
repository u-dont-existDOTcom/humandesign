"""Update only the four existing source-audit checkpoint files at the pinned base."""
from __future__ import annotations
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
TASK=ROOT/'tasks/astro-source-audit-multipass-20261005'
BASE='e3b523ebb6d5839be5b976d9c526ca6c70d16cd5'

def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def main():
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    if head != BASE:raise RuntimeError(f'Baseline changed: {head}')
    cur=read(TASK/'CURRENT_PASS.json')
    if cur['counts']['source_records'] != 227:raise RuntimeError('Checkpoint already advanced or changed')
    h=read(TASK/'batches/B01h/RULES.json')['records']
    i=read(TASK/'batches/B01i/RULES.json')['records']
    assert len(h)==45 and len(i)==61
    nxt='IV.1-IV.4; Book IV heading on PDF397/printed373 through before IV.5 on shared PDF417/printed393'
    cur['completed']='Source intake; full English Ptolemy Book I and Book III; prior source and Rhetorius witness/OCR qualifications retained'
    cur['current']='B01h/B01i complete: bodily and psychic constitution source audit; parent corpus audit OPEN'
    c=cur['counts'];c.update(ptolemy_read_sections=38,ptolemy_unread_sections=23,source_records=333,isolated_definition_tests=191,ptolemy_book_III_read_sections=14)
    c['ptolemy_english_natal_books_completed']=1
    c['psychic_single_pair_profiles']=15;c['psychic_placement_branches']=30
    cur.update(next_batch='B01j',next_range=nxt,last_verified_unit='III.14 closing sentence on PDF397/printed373 before Book IV',source_rule_records=333)
    cur['latest_reports']=['batches/B01h/REPORT.md','batches/B01h/VERIFICATION.json']
    cur['counting_note']='333 source records; 15 psychic single/pair profiles with 30 condition branches; 95 earlier separate star groups and four earlier Rhetorius comparisons. Counts are not independent predictions or validation trials.'
    cur['stop_admission']={'parent_status':'OPEN','remaining_gap':'Ptolemy II/IV and other books; fuller cross-author reconciliation; later compilation/evaluation.','next_action':nxt,'authority':'Owner-approved multi-pass audit and current continue request.','executed_this_increment':'Read/extract III.11-III.14:106 records, complete15/30 profile inventory and44 new bounded checks.','delivery_boundary':'Completed source-reading increment under the existing multiple-pass pause contract; no parent-completion or background-work claim.'}
    write(TASK/'CURRENT_PASS.json',cur)
    discovery=read(TASK/'SECTION_DISCOVERY.json')
    # Preserve the existing schema; locate its section list without changing unrelated metadata.
    candidates=[(k,v) for k,v in discovery.items() if isinstance(v,list) and v and isinstance(v[0],dict) and 'book' in v[0] and 'chapter' in v[0]]
    if len(candidates)!=1:raise RuntimeError(f'Unexpected section schema: {[k for k,v in candidates]}')
    key,sections=candidates[0]
    spans={11:(331,341),12:(341,357),13:(357,387),14:(387,397)}
    for s in sections:
        ch=s.get('chapter')
        if s.get('book')=='III' and ch in spans:
            if s['status']!='INDEXED_NOT_READ':raise RuntimeError('Section was already audited')
            a,b=spans[ch];rs=h if ch<13 else i
            s.update(status='READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE',locator_status='ENGLISH_SPANS_VERIFIED',english_pdf_pages=list(range(a,b+1,2)),source_batch='B01h' if ch<13 else 'B01i',rule_ids=[r['id'] for r in rs if r['source_locator']['chapter_or_verse']==f'III.{ch}'])
    discovery['read_sections_count']=38
    discovery['indexed_unread_count']=23
    discovery['body_locators_warning']='English Books I and III spans read/extracted. Book IV start and IV.5 boundary located, not counted as chapter reading. Book II and all Book IV remain unaudited.'
    write(TASK/'SECTION_DISCOVERY.json',discovery)
    plan=read(TASK/'PASS_PLAN.json')
    for p in plan['passes']:
        if p['id']=='P2':p['status']='PTOLEMY_61_INDEXED;ENGLISH_I24_AND_III14_READ_MAPPED'
        if p['id']=='P3':p['status']='ENGLISH_BOOKS_I_AND_III_COMPLETE;333_SOURCE_RECORDS;REMAINDER_OPEN'
        if p['id']=='P4':p['status']='191_SOURCE_REFERENCE_AND_INTEGRITY_CHECKS;FOUR_PRIOR_RHETORIUS_COMPARISONS;FULL_RECONCILIATION_PENDING'
    p=next(x for x in plan['batches'] if x['id']=='B01');p['next']=nxt
    p['completed_subbatches'] += [
      {'id':'B01h','scope':'English III.11-III.12 and identified notes; body/temperament and historical disease doctrines','source_records':45,'new_predictions':0,'tests':0,'test_scope':'Shared44-check suite counted under B01i.'},
      {'id':'B01i','scope':'English III.13-III.14 and identified notes;15 single/pair profiles with30 placement branches','source_records':61,'new_predictions':0,'tests':44,'test_scope':'Table/lookup/geometry and B01h/B01i integrity; no complete personality or clinical engine.'}]
    write(TASK/'PASS_PLAN.json',plan)
    s=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
    old=s.read_text()
    # Keep earlier cautions verbatim in a history subsection; replace the stale opening/recovery summary.
    idx=old.find('## New source implementation cautions')
    if idx<0:raise RuntimeError('Expected previous cautions section not found')
    previous=old[idx:]
    new='''# Current astrology source audit

**Parent OPEN: owner-authorized multi-pass source audit.** Full English Ptolemy Book I (24/24) and Book III (14/14) are read/extracted. No personal predictions, fitted-model changes or runtime promotion.

## Canonical recovery
- `tasks/astro-source-audit-multipass-20261005/CURRENT_PASS.json` — exact next section and counts.
- Task `PASS_PLAN.json` and `SECTION_DISCOVERY.json` — five passes;61 indexed Ptolemy sections,38 read,23 unread.
- Task `batches/B01h/REPORT.md` and `VERIFICATION.json` — integrated B01h/B01i report and actual tests.
- `batches/B01h/RULES.json`, `BODY_REFERENCE_TABLES.json`, `SECTION_COVERAGE.json` and reading/unresolved receipts.
- `batches/B01i/RULES.json`, `SOUL_PROFILE_TABLES.json`, `INTRASOURCE_QUALIFICATIONS.json`, reference helper/tests and reading/unresolved receipts.
- Prior batches and Rhetorius OCR/witness receipts are preserved unchanged.

## Completed; do not repeat
Previous227 source records plus B01h45 and B01i61 =333. There are15 psychic single/pair profiles with30 placement branches. Nine bodily-description rows, five phase modifiers, four quadrants and seven planetary body-correspondence rows are structured source tables, not independent observations. Earlier95 fixed-star groups, term tables and four targeted Rhetorius comparisons remain separate.191 source/reference checks plus34 methodology checks are expected; the latest verification records the actual run. No predictive validity follows.

Rhetorius copy-specific gaps are acknowledged and retained: do not reopen the debate or require another upload. Owner OCR is the private searchable aid; original images govern ambiguous text. BPHS remains Sharma; Primary Directions remains an excerpt/interview. Missing books do not block available tracks. No new OCR is needed.

## Next executable batch
**B01j: English IV.1-IV.4.** Start at Book IV heading on PDF397/printed373; stop before IV.5 on shared PDF417/printed393. These are introduction, material fortune, status/dignity and action/occupation. The headings are located, not counted as audited. All13 BookII mundane/general chapters remain deferred to their separate pass; all10 BookIV sections remain unaudited.

## New B01h/B01i cautions
Bodily constitutional temperament is not a modern personality scale. Source bodily enquiry uses Ascendant/Moon/rulers, and psychic enquiry Mercury/Moon/rulers plus contextual modifiers. The15 single/pair profiles require source-topical domination; bare conjunction is insufficient. Honourable does not mean morally good; contrary does not delete every talent or virtue. Keep both branches and their mixed traits. The helper only retrieves caller-qualified source references and abstains on unknown/mixed or three-plus conditions; it does not establish qualification.

The III.11 forward-motion note and III.13 precessions note must not become one unexamined signed-speed rule. The III.13 solstitial label's exact membership remains unresolved. Robbins's detailed dignity checklist is commentary reporting Bouché-Leclercq, not a direct new weighted rule. Context can reverse a shared word's character meaning. Five actual planetary rulers and two luminary referents/assistants are distinct roles.

Injuries/disease terminology and sexual-role categories remain historical, not modern identity/clinical classifications. Mitigation, visibility, cure, social reproach, concealment and benefit are different outcomes. The adopted III.14 text is curable but noticeable; the alternate reading is preserved separately. Mars has a conditional speech-relief branch. Geometric bendings are quadrature to the nodes, without a supplied near-point orb or medical implication. No individual is assessed.

'''
    s.write_text(new+previous.replace('## New source implementation cautions','## Prior B01f/B01g cautions retained',1))
    print('CHECKPOINT_UPDATED:38/61;333 source records;BookIII14/14;B01j next')

if __name__=='__main__':main()
