"""One-time four-file progress update after the B01m suite succeeds at its exact base."""
from pathlib import Path
import argparse
import json
import subprocess

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = ROOT / 'tasks/astro-source-audit-multipass-20261005'
BASE = '0efe72b0208ce388e261467f0da6c25888521b14'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verified-new-tests', type=int, required=True)
    ap.add_argument('--verified-total-tests', type=int, required=True)
    args = ap.parse_args()
    assert args.verified_new_tests == 64 and args.verified_total_tests == 473
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == BASE
    rules = json.loads((B / 'RULES.json').read_text())
    assert rules['records_count'] == 59
    c = json.loads((TASK / 'CURRENT_PASS.json').read_text())
    assert c['counts']['source_records'] == 571 and c['counts']['ptolemy_read_sections'] == 46
    nxt = 'Full English IV.10 and both transmitted endings: PDF461/printed437 through PDF483/printed459; stop before Index on PDF485/printed461.'
    c['counts'].update(source_records=630, ptolemy_read_sections=47, ptolemy_unread_sections=14,
                       isolated_definition_tests=439, targeted_cross_source_comparisons=17,
                       ptolemy_book_IV_read_sections=9, quality_of_death_planet_spectra=5,
                       quality_of_death_conditional_examples=20)
    c.update(completed='Source intake; English Books I/III and IV.1-IV.9; prior source-witness qualifications retained',
             current='B01m complete: historical quality-of-death procedure; parent audit OPEN',
             source_rule_records=630, next_batch='B01n', next_range=nxt,
             last_verified_unit='IV.9 closing foreign-location paragraph and relevant notes on PDF461/printed437; IV.10 and ending boundaries located only',
             latest_reports=['batches/B01m/REPORT.md', 'batches/B01m/VERIFICATION.json'],
             counting_note='630 Ptolemy source records. Five historical cause spectra and twenty conditional example branches are source representations, not independent personal predictions. Seventeen targeted comparisons in total.')
    c['stop_admission'].update(
        remaining_gap='Full Ptolemy IV.10 including both endings; all thirteen BookII sections; other supplied books; full source reconciliation, compilation and evaluation.',
        next_action=nxt,
        executed_this_increment='Full English IV.9 and identified notes:59 records,5 planet spectra,20 conditional examples,3 targeted Rhetorius comparisons,64 new bounded checks.',
        delivery_boundary='Completed source-reading increment under the existing owner-approved multiple-pass pause contract; parent remains OPEN; no unattended work claimed.')
    (TASK / 'CURRENT_PASS.json').write_text(json.dumps(c, indent=2) + '\n')

    plan = json.loads((TASK / 'PASS_PLAN.json').read_text())
    for p in plan['passes']:
        if p['id'] == 'P2': p['status'] = 'PTOLEMY_61_INDEXED;47_ENGLISH_SECTIONS_READ_MAPPED'
        elif p['id'] == 'P3': p['status'] = 'ENGLISH_I_III_COMPLETE_AND_IV1_IV9;630_SOURCE_RECORDS;REMAINDER_OPEN'
        elif p['id'] == 'P4': p['status'] = '439_SOURCE_REFERENCE_CHECKS;SEVENTEEN_TARGETED_RHETORIUS_COMPARISONS;FULL_RECONCILIATION_PENDING'
    b = plan['batches'][0]
    assert b['id'] == 'B01'
    assert not any(s['id'] == 'B01m' for s in b['completed_subbatches'])
    b['next'] = nxt
    b['completed_subbatches'].append({
        'id':'B01m', 'scope':'Full English IV.9 and identified notes; targeted Rhetorius57/77 paragraphs',
        'source_records':59, 'new_predictions':0, 'tests':64,
        'test_scope':'Source-only typed lookup, caller-qualified logic, selection/fallback handling, role and attribution checks. No mortality, medical, or violence forecast.',
        'targeted_cross_source_comparisons':3})
    (TASK / 'PASS_PLAN.json').write_text(json.dumps(plan, indent=2) + '\n')

    d = json.loads((TASK / 'SECTION_DISCOVERY.json').read_text())
    assert d['read_sections_count'] == 46
    sec = json.loads((B / 'SECTION_COVERAGE.json').read_text())['sections'][0]
    row = next(r for r in d['sections'] if r['book'] == 'IV' and r['chapter'] == 9)
    assert row['status'] == 'INDEXED_NOT_READ'
    row.update(status='READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE', locator_status='ENGLISH_SPANS_VERIFIED',
               rule_ids=sec['record_ids'], english_pdf_pages=sec['english_pdf_pages'],
               reading_receipt='batches/B01m/READING_RECEIPT.json', boundary=sec['boundary'])
    row = next(r for r in d['sections'] if r['book'] == 'IV' and r['chapter'] == 10)
    row['locator_status'] = 'HEADING_AND_BOTH_ENDING_BOUNDARIES_LOCATED_ONLY_NOT_CHAPTER_READ'
    row['ending_english_pdf_page'] = 483
    row['index_starts_pdf_page'] = 485
    d.update(read_sections_count=47, indexed_unread_count=14,
             body_locators_warning='English Books I/III and IV.1-IV.9 read/extracted. IV.10 and both endings located only; IV.10 and all thirteen BookII chapters unaudited.')
    (TASK / 'SECTION_DISCOVERY.json').write_text(json.dumps(d, indent=2) + '\n')

    path = ROOT / 'state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md'
    s = path.read_text()
    for old,new in [
        ('and IV.1-IV.8 are read/extracted.', 'and IV.1-IV.9 are read/extracted.'),
        ('46 read,15 unread.', '47 read,14 unread.'),
        ('- Task `batches/B01l/REPORT.md`,', '- Task `batches/B01m/REPORT.md`, `VERIFICATION.json`, `RULES.json`, `QUALITY_OF_DEATH_TABLES.json` and comparison/reading receipts — current quality-of-death source batch.\n- Prior `batches/B01l/REPORT.md`,'),
        ('Previous500 source records plus B01l71 =571.', 'Previous571 source records plus B01m59 =630. B01m adds5 source cause spectra,20 conditional examples and3 targeted comparisons (17 total).'),
        ('375 source/reference checks plus34 methodology checks', '439 source/reference checks plus34 methodology checks')]:
        assert old in s, old
        s = s.replace(old,new,1)
    start = s.index('**B01m:')
    end = s.index('\n\n## New B01l cautions',start)
    s = s[:start] + '''**B01n: full English IV.10 and both transmitted endings.** Start division of times on PDF461/printed437; both English conclusions occur on PDF483/printed459. Stop before Index on PDF485/printed461. These boundaries are located only, not yet audited. All13 BookII chapters remain separately scheduled.

## New B01m cautions
IV.9 depends on III.10 mechanism/place selection: occourse place or occident, then occupants first and first-approaching fallback only when occupants are known absent. Unknown astronomy is not absence; the eighth-house ruler is not an automatic Ptolemaic substitute. Five cause spectra require topical qualification and remain historical categories, not diagnoses. Generic benefic identity is not a protective override; afflicted Jupiter can modify an adverse example’s publicity.

Natural/own classification has positive conditions and a no-qualifying-overcoming exclusion. Anonymous same-sect-domicile gloss is separate. No branch firing is not evidence of the opposite real-world outcome. Affliction, magnitude, kind, multiplicity, burial and geography remain distinct. Saturn’s prison-locator main text says ASC while Melanchthon’s alternative says occident; neither is selected after observing an outcome. The closing together-AND-opposition clause has an unresolved target; do not emend to conjunction-OR-opposition.

Sign groups, constellation forms, and angular positions are not interchangeable. Intensifiers stay separate from necessities. In the adopted Mars/Venus sentence dying because of women differs from dying as murderers of women; never convert to an unconditional violence/personality label. Rhetorius77 uses an alternative Critodemus terms scheme reportedly including Sun; existing term tables cannot substitute. His same-deaths-not-public and peaceful-only-benefics clauses have different antecedents. Chapter57/77 overlap is source reuse, not independent confirmation. Targeted available paragraphs only; no complete Rhetorius77 audit or new personal forecast.
''' + s[end:]
    path.write_text(s)
    print('CHECKPOINT_UPDATED:47/61;630records;B01nnext')


if __name__ == '__main__':
    main()
