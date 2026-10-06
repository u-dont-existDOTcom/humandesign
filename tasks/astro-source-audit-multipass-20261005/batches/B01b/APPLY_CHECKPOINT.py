"""Apply the completed B01b source-audit checkpoint without touching fitted models."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / 'tasks/astro-source-audit-multipass-20261005'
BASE = '07d7e0427cdfdfd53f17eaa1289c7fbb18101cad'


def load(p):
    return json.loads(p.read_text())


def save(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def main():
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == BASE
    # Historical models, old intake and first completed source batch are immutable here.
    protected = [
        'tasks/astro-source-audit-multipass-20261005/DRIVE_INTAKE.json',
        'tasks/astro-source-audit-multipass-20261005/RHETORIUS_PREVIEW_DETECTION.json',
        'tasks/astro-source-audit-multipass-20261005/batches/B01/RULES.json',
        'tasks/astro-source-audit-multipass-20261005/batches/B01/READING_RECEIPT.json',
        'tasks/astro-source-audit-multipass-20261005/batches/B01/definition_reference.py',
        'reference/research/current_merged_timing_candidate_ruleset_v1.json',
        'reference/research/CURRENT_PERSON_LIFE_RULESET_CATALOG_V1.json',
        'reference/research/ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V2.json',
    ]
    hashes = {}
    for path in protected:
        expected = subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=ROOT)
        actual = (ROOT / path).read_bytes()
        assert actual == expected, f'Protected content changed: {path}'
        hashes[path] = hashlib.sha256(actual).hexdigest()
    rules = load(TASK / 'batches/B01b/RULES.json')
    receipt = load(TASK / 'batches/B01b/READING_RECEIPT.json')
    recovery = load(TASK / 'RHETORIUS_SIX_PAGE_RECOVERY.json')
    assert len(rules['records']) == 32
    assert all(p['render_match'] for p in recovery['pages']) and len(recovery['pages']) == 6
    assert recovery['supplement_sha256'] == load(TASK / 'RHETORIUS_REPLACEMENT_AUDIT_20261006.json')['private_supplement']['sha256']
    discovery = load(TASK / 'SECTION_DISCOVERY.json')
    for section in discovery['sections']:
        if section['book'] == 'I' and 9 <= section['chapter'] <= 16:
            chapter = f"I.{section['chapter']}"
            section.update({
                'status': 'READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE',
                'locator_status': 'ENGLISH_SPANS_VERIFIED',
                'english_pdf_pages': receipt['section_spans'][chapter],
                'rule_ids': [r['id'] for r in rules['records'] if r['source_locator']['chapter_or_verse'] == chapter],
                'batch_id': 'B01b',
            })
    discovery['read_sections_count'] = sum(s['status'].startswith('READ_EXTRACTED') for s in discovery['sections'])
    discovery['indexed_unread_count'] = 61 - discovery['read_sections_count']
    assert discovery['read_sections_count'] == 16
    discovery['body_locators_warning'] = 'English spans I.1-I.16 verified. Other sections remain TOC locators, not completed reading. Shared chapter pages remain explicit.'
    save(TASK / 'SECTION_DISCOVERY.json', discovery)
    plan = load(TASK / 'PASS_PLAN.json')
    for p in plan['passes']:
        if p['id'] == 'P1':
            p['status'] = 'COMPLETE_INTAKE_WITH_GAPS; RHETORIUS_REPLACEMENT_AND_SIX_PAGE_SUPPLEMENT_QUALIFIED'
            p['output'] = list(dict.fromkeys(p['output'] + ['SOURCE_WITNESS_UPDATES_20261006.json', 'RHETORIUS_REPLACEMENT_AUDIT_20261006.json', 'RHETORIUS_SIX_PAGE_RECOVERY.json']))
        if p['id'] == 'P2':
            p['status'] = 'PTOLEMY_61_INDEXED; I_1_TO_I_16_READ; 45_UNREAD'
        if p['id'] == 'P3':
            p['status'] = 'B01_AND_B01B_COMPLETE: 56_SOURCE_RECORDS_PLUS_95_STAR_GROUP_TABLE_ENTRIES'
        if p['id'] == 'P4':
            p['status'] = '49_ISOLATED_DEFINITION_TESTS; CROSS_AUTHOR_RECONCILIATION_PENDING'
    for b in plan['batches']:
        if b['id'] == 'B01':
            b['next'] = 'B01c: Ptolemy I.17-I.24, starting English PDF103 / printed79; preserve source tables and variants; stop before BookII.'
            completed = b.setdefault('completed_subbatches', [])
            if not any(x['id'] == 'B01b' for x in completed):
                completed.append({'id':'B01b','scope':'English I.9-I.16 + bounded Robbins notes','source_records':32,'fixed_star_descriptive_groups':95,'new_predictions':0,'tests':31})
        if b['id'] == 'B07':
            b['rhetorius_status'] = '198-page replacement plus six-page old-witness supplement; 199/222 numbered pages available, 23 absent. Available opening1-103 can proceed.'
    save(TASK / 'PASS_PLAN.json', plan)
    current = load(TASK / 'CURRENT_PASS.json')
    current['completed'] = '13-source intake; Ptolemy English I.1-I.16; improved Rhetorius witness qualified and six missing pages recovered from old preview'
    current['current'] = 'B01b source-reading batch complete; larger source audit remains OPEN'
    current['counts'].update({
        'partial_preview_files':0, 'incomplete_book_witnesses':1,
        'retained_old_preview_files':1, 'private_supplement_files':1,
        'ptolemy_read_sections':16, 'ptolemy_unread_sections':45,
        'source_records':56, 'fixed_star_descriptive_group_entries':95,
        'isolated_definition_tests':49,
        'rhetorius_replacement_pdf_pages':198, 'rhetorius_combined_numbered_pages_available':199,
        'rhetorius_numbered_pages_unavailable':23,
    })
    current['next_batch'] = 'B01c'
    current['next_range'] = 'I.17-I.24; start English PDF103 / printed79 at I.17; verify table/section ends and stop before BookII'
    current['last_verified_unit'] = 'PTOLEMY1940_REPRINT1964 I.16; English PDF103 / printed79, before I.17 heading'
    current['source_rule_records'] = 56
    current['fixed_star_table_entries'] = 95
    current['source_witness_updates'] = 'SOURCE_WITNESS_UPDATES_20261006.json'
    current['counting_note'] = 'The13 current Drive files include the replacement, while the superseded preview and six-page supplement are separately retained private witnesses; 95 table groups are not 95 independent predictions.'
    current['next_actor'] = 'Next authorized chapter-batch continuation; no background process remains'
    current['no_background_run'] = True
    save(TASK / 'CURRENT_PASS.json', current)
    save(TASK / 'batches/B01b/PROTECTED_CONTENT_VERIFICATION.json', {'base_commit':BASE,'checked_after_source_batch':True,'sha256':hashes,'claims':'Byte equality only; no new empirical model validation.'})
    save(TASK / 'batches/B01b/WRITER-LEASE.json', {'status':'batch_complete_parent_open','branch':'research/astro-source-audit-b01b-20261006','integration_branch':'research/six-rule-life-timing-20261001','base_commit':BASE,'scope':'Source batch B01b and Rhetorius replacement/recovery only','owner_authority':'Continue source audit in multiple passes and check replacement Rhetorius','stop_boundary':'Completed declared English I.9-I.16 chapter batch; next is I.17','next_action':'Read and extract I.17-I.24; no extra books required for that batch','not_claimed':'Full source audit, person predictions, or runtime promotion'})
    print('CHECKPOINT_UPDATED: Ptolemy16/61sections;56records;95tablegroups;Rhetorius199/222numberedpages')


if __name__ == '__main__':
    main()
