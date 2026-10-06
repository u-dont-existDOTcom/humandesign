"""Guarded source-audit checkpoint update; no prior rule or runtime edits."""
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / 'tasks/astro-source-audit-multipass-20261005'
BASE = 'c1ff514b1ce1a5978ddcf66c6b635abe05881c7c'
HEAD = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
if HEAD != BASE:
    raise SystemExit(f'Wrong base {HEAD}; reconcile before mutation.')

def load(name):
    return json.loads((TASK / name).read_text())

def save(name, obj):
    (TASK / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

current = load('CURRENT_PASS.json')
if current['counts']['ptolemy_read_sections'] != 24 or current['source_rule_records'] != 109:
    raise SystemExit('Checkpoint changed or update already applied; no repeat mutation.')
new = {}
for batch in ['B01d', 'B01e']:
    data = load(f'batches/{batch}/RULES.json')
    for r in data['records']:
        chapter = int(r['source_locator']['chapter_or_verse'].split('.')[1])
        new.setdefault(chapter, []).append(r['id'])
assert {k:len(v) for k,v in new.items()} == {1:8,2:10,3:9,4:18,5:10}
spans = {1:list(range(245,254,2)),2:list(range(253,260,2)),
         3:list(range(259,266,2)),4:list(range(265,276,2)),5:[275,277,279]}
next_range = 'III.6-III.9; start III.6 on English PDF279/printed255; stop before III.10 on shared PDF295/printed271'
sections = load('SECTION_DISCOVERY.json')
for row in sections['sections']:
    if row['book'] == 'III' and row['chapter'] in new:
        ch = row['chapter']
        row.update(status='READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE',
                   locator_status='ENGLISH_SPANS_VERIFIED',
                   rule_ids=new[ch], english_pdf_pages=spans[ch],
                   source_batch='B01d' if ch<=3 else 'B01e')
sections.update(read_sections_count=29, indexed_unread_count=32,
    body_locators_warning='English Book I and III.1-III.5 spans verified. Book II, III.6-III.14 and IV remain unread; boundaries/contents alone do not count as reading.')
assert len(sections['sections']) == 61
assert sum(r['status']=='READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE' for r in sections['sections']) == 29
save('SECTION_DISCOVERY.json', sections)

current.update(completed='Source intake; Ptolemy English I.1-I.24 and III.1-III.5; accepted Rhetorius OCR and copy-specific gap qualification retained',
    current='B01d and B01e complete: natal methodology, parents and siblings; wider source audit OPEN',
    next_batch='B01f', next_source='PTOLEMY1940_REPRINT1964', next_range=next_range,
    last_verified_unit='III.5 ending on English PDF279/printed255 immediately before III.6',
    source_rule_records=164,
    next_actor='Next authorized source-audit continuation; no new upload needed',
    no_background_run=True,
    counting_note='13 current Drive files plus one owner OCR aid; 164 source records, 95 separate star groups, four earlier Rhetorius comparisons. Counts are not independent predictions or validation trials.',
    latest_reports=['batches/B01d/REPORT.md','batches/B01d/VERIFICATION.json'],
    stop_admission={'parent_status':'OPEN','remaining_gap':'Other source sections, later cross-author reconciliation and compilation/evaluation remain.',
                    'next_action':next_range,'authority':'Owner-authorized multiple passes and current continue request.',
                    'executed_this_increment':'Read III.1-III.3 and continued through III.4-III.5; 55 records and 23 new bounded checks.',
                    'delivery_boundary':'Completed source-reading increment under the existing multi-pass plan; not a parent-completion claim.'})
current['counts'].update(ptolemy_read_sections=29,ptolemy_unread_sections=32,source_records=164,
    isolated_definition_tests=108,ptolemy_book_III_read_sections=5)
save('CURRENT_PASS.json',current)

plan=load('PASS_PLAN.json')
for p in plan['passes']:
    if p['id']=='P2':p['status']='PTOLEMY_61_INDEXED; ENGLISH_I24_AND_III5_READ_MAPPED'
    elif p['id']=='P3':p['status']='ENGLISH_I_COMPLETE_AND_III1_III5;164_SOURCE_RECORDS;REMAINDER_OPEN'
    elif p['id']=='P4':p['status']='108_SOURCE_DEFINITION_AND_INTEGRITY_TESTS;FOUR_PRIOR_RHETORIUS_COMPARISONS;FULL_RECONCILIATION_PENDING'
b=next(x for x in plan['batches'] if x['id']=='B01')
b['next']=next_range
existing={x['id'] for x in b['completed_subbatches']}
assert not {'B01d','B01e'} & existing
b['completed_subbatches'] += [
 {'id':'B01d','scope':'English III.1-III.3, identified Robbins notes and scoped definition fragments','source_records':27,'new_predictions':0,'tests':23,'test_scope':'Shared new suite also covers B01e record integrity; count once.'},
 {'id':'B01e','scope':'English III.4-III.5, parental/sibling qualifications and topical mixture','source_records':28,'new_predictions':0,'tests':0,'test_scope':'Covered by B01d shared suite, not an additional 23 tests.'}]
save('PASS_PLAN.json',plan)

state=ROOT/'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
state.write_text('''# Current astrology source audit

**Parent OPEN: owner-authorized multi-pass source audit.** Completed English Ptolemy Book I (24/24) and Book III.1-III.5. No personal predictions, fitted-model changes or runtime promotion.

## Canonical recovery
- `tasks/astro-source-audit-multipass-20261005/CURRENT_PASS.json` — exact next section/counts.
- `tasks/astro-source-audit-multipass-20261005/PASS_PLAN.json` — five passes and all source tracks.
- `tasks/astro-source-audit-multipass-20261005/SECTION_DISCOVERY.json` — 61 Ptolemy sections: 29 read, 32 unread.
- `tasks/astro-source-audit-multipass-20261005/batches/B01d/REPORT.md` — integrated B01d/B01e result.
- `tasks/astro-source-audit-multipass-20261005/batches/B01d/VERIFICATION.json` — tests, source digest, protected files.
- `batches/B01d/RULES.json`, `TOPICAL_SYNTHESIS_SPEC.json`, `READING_RECEIPT.json`, `UNRESOLVED_INTERPRETATIONS.json` under the task — methodology/rectification fragments.
- `batches/B01e/RULES.json`, `READING_RECEIPT.json`, `INTRASOURCE_QUALIFICATIONS.json`, `UNRESOLVED_INTERPRETATIONS.json` — parents, siblings and qualifications.
- `tasks/astro-source-audit-multipass-20261005/RHETORIUS_OCR_RECHECK_20261006.json` — controlling copy-specific qualification; original intake/witness/supplement receipts remain preserved.

## Completed; do not repeat
B01/B01b/B01c/B01d/B01e contain 24+32+53+27+28 = 164 source records. Earlier fixed-star table has 95 descriptive groups. Egyptian and Ptolemaic terms have 120 visually transcribed cells; Chaldean day/night reconstruction has 120 computed cells. Four prior targeted Rhetorius comparisons are not a whole Rhetorius audit. The source-definition/integrity suite now has 108 checks, plus 34 methodology checks; use the latest verification for the actual combined run. None measures predictive validity.

Owner OCR `RHETORIUS_HOLDEN_OWNER_OCR_20261006.txt` is the private searchable aid. Original images govern ambiguous numbers and page continuity; unreadable footer labels are not missing content. The actual replacement has 198 PDF pages versus the limited 150-page preview surface. The earlier 23-gap list concerns the inspected copy plus six-page supplement; transitions including printed103 to105 and112 to114 were rechecked. The owner now acknowledges missing pages. Do not repeat the debate, request another copy, or discard available material. No new OCR run is needed.

BPHS remains Sharma, not Santhanam. Primary Directions remains an excerpt/interview. Missing books do not block the available source tracks.

## Next executable batch
**B01f: English III.6-III.9.** Start at III.6 heading on PDF279/printed255; end before III.10 on shared PDF295/printed271. These chapters remain unread for audit counts. Preserve historical terminology and limitations without turning source descriptions into modern clinical or identity classifications. Book II's thirteen mundane/general chapters remain deferred to their separate pass, and all Book IV remains unread.

## Current implementation cautions
Topical place comes before ruler selection. III.2 lists five forms including phase OR aspect as one category; no imported face/decan or weighted dignity table. Rectification still lacks resolved epoch, closeness, boundary and inversion conventions; helpers are NOT a complete rectifier. Distinguish quality, magnitude and general timing. Equal competing rulers may blend or act successively rather than always cancelling. Original topical familiarity governs major influence, not literally every conceivable effect. Weak positive longevity testimony explicitly does not establish the opposite. Sibling locus has a translator-acknowledged textual ambiguity; do not substitute a generic third house. III.3's rejection of unexplained lots is qualified by Fortune use in III.4/III.5; no blanket rejection or modern numerology verdict follows.

Earlier Book I cautions remain: term tables have equal totals but differ on153/360degrees; Chaldean rotation keeps Saturn/Mercury together; Ptolemy rejects twelfth-parts while Rhetorius adopts them; triplicities, proper face and chariots are author-specific. Unspecified angular thresholds, some term-generation details, latitude zero/equality cases, and Greek/Latin apparatus collation remain open.

Raw books/OCR/full extracted text/source images stay outside Git. Preserve all historical predictions, numerology, retained candidates and prior source batches. This is source audit, not an independently blinded person experiment. No process is scheduled/running after delivery; resume the first unfinished section from this checkpoint.
''')
print('CHECKPOINT_UPDATED:29/61 sections;164 records;B01f next')
