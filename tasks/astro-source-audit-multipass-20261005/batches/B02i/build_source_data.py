"""Normalize the frozen, source-ordered reader records without deleting detail.

Run only after independent_review/{source_a,source_b,worked_chart} files are copied.
Raw candidates remain immutable evidence; corrections are explicit producer
dispositions. This file does not alter an older source batch or personal model.
"""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
SOURCE = 'LILLY1647_WELLCOME_B30338724'
SOURCE_SHA = '2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'


def read(path):
    return json.loads((ROOT/path).read_text())


def write(name, value):
    (ROOT/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def main():
    a = read('independent_review/source_a/CANDIDATE_RULES.json')['records']
    b = read('independent_review/source_b/CANDIDATE_RULES.json')['rules']
    c = read('independent_review/worked_chart/CANDIDATE_RULES.json')['candidates']
    rows, mapping = [], {}
    for reader, candidates in [('A', a), ('B', b), ('C', c)]:
        for raw in candidates:
            if reader == 'A':
                local = raw['local_id']; n = int(local[1:])
                chapter = ('FOURTH_HOUSE_PREAMBLE' if n == 1 else
                           'XXXII' if n <= 14 else 'XXXIII' if n <= 43 else 'XXXIV')
                pages = raw['pdf_pages']; anchor = raw['passage_anchor']
                title = raw['target']; kind = raw['genre']
                statement = raw['source_paraphrase']; conditions = raw['antecedent']
                outputs = raw['outputs']; limits = raw['modifiers_exceptions']
                time = raw['time_horizon']; attribution = 'Ancients, reported by Lilly' if n == 9 else 'Lilly'
                source_fields = deepcopy(raw)
            elif reader == 'B':
                local = raw['local_id']; chapter = raw['source']['chapter']
                pages = raw['source']['pdf_pages']; anchor = raw['source']['passage_anchor']
                title = raw['outputs'][0]['target']; kind = raw['evidence']['kind']
                conditions = raw['condition_structure']; outputs = raw['outputs']
                statement = {'conditions': conditions, 'outputs': outputs}
                limits = raw['qualifications']; time = 'Local temporal wording retained in source_fields'
                attribution = raw['evidence']['attribution']; source_fields = deepcopy(raw)
            else:
                local = raw['id']; chapter = 'XXXVIII'
                pages = [p['pdf'] for p in raw['source_pages']]
                anchor = raw['exact_anchor_excerpt']; title = raw['title']; kind = raw['record_type']
                conditions = raw['conditions']; outputs = raw['consequences']
                statement = {'conditions': conditions, 'consequences': outputs,
                             'reported_outcomes': raw['reported_outcomes']}
                limits = raw['modifiers']; time = 'Distinct question, negotiation, loan, bargain, payment and narration stages retained'
                attribution = 'Lilly, retrospective account of his own enquiry'; source_fields = deepcopy(raw)
            rid = f'LI.1647.II.{chapter}.R{1009+len(rows)}'
            mapping[local] = rid
            rows.append({
                'id': rid, 'local_id': local, 'title': title, 'kind': kind,
                'source_locator': {'source_id': SOURCE, 'source_sha256': SOURCE_SHA,
                    'book': 'II', 'section_key': 'II.'+chapter, 'pdf_pages': pages,
                    'printed_sequence_expected': [p-34 for p in pages],
                    'visible_printed_labels': [str(p-34) for p in pages],
                    'passage_anchor': anchor,
                    'anchor_note': 'Locating phrase with long-s, spacing and glyph names normalized; not a diplomatic quotation.'},
                'genre': 'historical_horary_source', 'statement_type': 'editor_normalized_paraphrase',
                'source_attribution': attribution, 'source_statement': statement,
                'prerequisites': conditions if isinstance(conditions, list) else [conditions],
                'outputs': outputs, 'qualifications_and_limits': limits,
                'temporal_target': time, 'source_fields': source_fields,
                'source_reader': reader, 'unresolved_ids': [],
                'runtime_status': 'REFERENCE_ONLY_NOT_PROMOTED',
                'independent_evidence_unit': False,
            })
    by_local = {r['local_id']: r for r in rows}
    # Preserve the source's broad maxim before discussing its contextual limits.
    by_local['B031']['source_statement'] = {
        'conditions': deepcopy(by_local['B031']['source_fields']['condition_structure']),
        'source_maxim': 'No planet is unfortunate when in its own house or essentially dignified and a significator.',
        'scope_note': 'The source assertion is retained literally in sense. Its interaction with accidental affliction and adjacent unimpeded/direct qualifications is not silently resolved.'}
    by_local['B031']['outputs'] = ['The source calls such a dignified significator not unfortunate.']
    by_local['B031']['qualifications_and_limits'] += [
        'Raw reader wording narrowed this to planet identity; normalization restores the broader printed assertion and retains contextual tension.']
    for row in rows:
        raw = row['source_fields']
        dependencies = list(raw.get('dependency_context_ids', []))
        dependencies += [r['id'] for r in raw.get('related_rules', []) if 'id' in r]
        row['related_record_ids'] = [mapping[k] for k in dependencies if k in mapping]
    issues, resolved = [], []

    def issue(key, title, pages, local_ids, details, status='PRESERVED_NOT_SILENTLY_RESOLVED'):
        item = {'id': f'B02i-{key}', 'title': title, 'pdf_pages': sorted(set(pages)),
                'detail': details, 'record_ids': [mapping[k] for k in local_ids],
                'status': status, 'runtime_disposition': 'Reference only; no hidden precision, precedence or validated outcome supplied.'}
        (resolved if status.startswith('RESOLVED') else issues).append(item)
        for k in local_ids:
            by_local[k]['unresolved_ids' if not status.startswith('RESOLVED') else 'resolved_reading_ids'] = (
                by_local[k].get('unresolved_ids' if not status.startswith('RESOLVED') else 'resolved_reading_ids', [])+[item['id']])

    grouped = {}
    for raw in a:
        current = None
        for desc in raw['unresolved_readings']:
            match = re.match(r'(A-U\d+):\s*(.*)', desc)
            if match:
                current, detail = match.groups()
            elif current:
                detail = desc
            else:
                current, detail = 'A-U12', desc
            g = grouped.setdefault(current, {'pages': [], 'ids': [], 'details': []})
            g['pages'] += raw['pdf_pages']
            if raw['local_id'] not in g['ids']: g['ids'].append(raw['local_id'])
            if detail not in g['details']: g['details'].append(detail)
    for key, g in sorted(grouped.items(), key=lambda x: int(x[0].split('U')[1])):
        issue(key, g['details'][0].split(';')[0], g['pages'], g['ids'], g['details'],
              'RESOLVED_EXPLICIT_MUNDANE_HOUSE_GLOSS' if key == 'A-U03' else 'PRESERVED_NOT_SILENTLY_RESOLVED')
    for raw in read('independent_review/source_b/ISSUES_LEDGER.json')['issues']:
        resolved_keys = {'B-I03', 'B-I05', 'B-I07', 'B-I18', 'B-I19'}
        status = 'RESOLVED_SOURCE_READING_OR_SCOPE' if raw['issue_id'] in resolved_keys else 'PRESERVED_NOT_SILENTLY_RESOLVED'
        issue(raw['issue_id'], raw['type'], raw['pdf_pages'], raw['candidate_ids'],
              [raw['source_reading'], raw['downstream_implication'], raw['disposition']], status)

    c_issues = [
        ('C-U01', 'One retrospective author account, with disclosed prior knowledge', [253,254,255,256],
         ['C001','C006','C011','C012','C013','C014','C017','C018','C028'],
         'No independent contemporaneous prediction freeze, comparison group or transaction/loan evidence is supplied. Intention and six-month money restriction are prior inputs. Episodes belong to one enquiry.'),
        ('C-U02', 'Omitted time, latitude and cusp minutes', [253], ['C002'],
         'Time minutes/seconds, latitude, timezone and calendar are unprinted. H4/H10 print18 without minutes. Abbreviation typography is partly uncertain. Retain nulls.'),
        ('C-U03', 'Radix Jupiter equality cannot be checked within the chapter', [254], ['C003'],
         'Lilly states rising degree equals natal Jupiter; the radix and independently checked natal coordinates are absent from this span.'),
        ('C-U04', 'Sun as local seller versus seventh-lord wording', [253,254], ['C004','C007'],
         'Sun is assigned by seventh placement then called lord7. The printed seventh cusp is Aries. Preserve local assignment and terminology without silently substituting a different cusp or lord.'),
        ('C-U05', 'Mercury physical sector and possible cusp convention', [253,254], ['C005'],
         'Mercury is in geometric seventh,2°48′ before cusp8, while prose names only Venus and Sun there. An earlier cusp-influence convention may explain interpretive assignment; no settled source error or adopted rule follows here.'),
        ('C-U06', 'Mixed testimony, qualitative strength and unexpressed considerations', [254,255], ['C006','C007','C008','C009','C015','C025'],
         'No unique weighting, high-price threshold, platick orb, prevention algorithm or complete list of considered testimonies is supplied. Shared planetary roles are not independent evidence.'),
        ('C-U07', 'Future contact sequence and twelve-day antecedent', [253,254,255], ['C008','C010','C015','C017','C018'],
         'Static coordinates do not independently verify later conjunctions, translation, ingress or station dates. The nearest antecedent of which he did twelve days after is Mars becoming direct; joint timing with Jupiter is not settled.'),
        ('C-U08', 'Perfect trine wording versus exact coordinate equality', [253,254], ['C009'],
         'Printed Sun/Saturn coordinates are119°31′ apart,29′ from120°. Perfect may be used with an orb; no claim of exact-minute identity or unusable aspect is made.'),
        ('C-U09', 'Approximate degree-to-week retrospective comparison', [253,255], ['C019'],
         'Printed Venus/Sun gap is6°21′. Six weeks and some days matches47 elapsed calendar days to17May, under same-year/same-calendar assumptions. Fractional-degree conversion and exact advance date forecast are not supplied.'),
        ('C-U10', 'Five body-mark reports are neither new cases nor concealed tests', [255], ['C020','C021','C022','C023','C024'],
         'All marks are self-reports in the same retrospective narrative. No prior concealed record, independent examination or precise general laterality/location calibration is supplied.'),
        ('C-U11', 'Durability and lease-lifetime expectations remain open', [255], ['C016','C026'],
         'Old/strong property description is reported; many-year durability and survival of leases beyond his life lack subsequent endpoint evidence here.'),
        ('C-U12', 'Financial disadvantage and satisfaction are distinct, unquantified endpoints', [255,256], ['C026','C027','C028'],
         'Purchase completed and author says he did not regret it, but calls it financially injurious. No monetary loss amount or comparative valuation is given.'),
        ('C-U13', 'Wharton disagreement is reported, not adjudicated', [256], ['C029'],
         'The passage denies occupational and marital claims attributed to Wharton; his text and independent historical evidence are outside this source block.'),
        ('C-U14', 'Printed Fortune does not match retained Lilly formula', [253], ['C002','C015'],
         'Ascendant13°45′Libra + Moon10°38′Virgo − Sun20°56′Aries yields Pisces3°27′ under the retained same-day/night formula, while the diagram prints Pisces12°27′. Preserve the9° discrepancy without repairing any source input. The cause is unresolved.'),
    ]
    for row in c_issues: issue(*row)

    write('RULES.json', {'schema_version': 1, 'batch': 'B02i', 'source_id': SOURCE,
        'source_sha256': SOURCE_SHA, 'status': 'SOURCE_ONLY_NOT_RUNTIME_OR_VALIDATION',
        'scope': 'Complete fourth-house heading/preamble and XXXII–XXXVIII, PDF236 through256 top above divider.',
        'records_count': len(rows), 'general_records_count': len(a)+len(b),
        'worked_example_records_count': len(c), 'rules': rows})
    write('RECORD_ID_MAP.json', mapping)
    write('UNRESOLVED.json', {'issues_count': len(issues), 'issues': issues,
        'resolved_readings_count': len(resolved), 'resolved_readings': resolved,
        'count_note': 'Unresolved textual/model/evidence limits counted separately from source-resolved readings; not a count of demonstrated author errors.'})

    sections = []
    for r in read('independent_review/source_a/COVERAGE_AND_ISSUES.json')['sections']:
        sections.append({'key': r['section'], 'pdf_pages': r['pages'],
                         'record_ids': [mapping[k] for k in r['ids']]})
    for chapter, ids, pages in [('XXXV_REMOVAL', [r['local_id'] for r in b if r['source']['chapter']=='XXXV'], [246,247,248]),
                              ('XXXVI_WATERWORKS',[r['local_id'] for r in b if r['source']['chapter']=='XXXVI'],[248,249]),
                              ('XXXVII_TREASURE',[r['local_id'] for r in b if r['source']['chapter']=='XXXVII'],[249,250,251,252])]:
        sections.append({'key': chapter, 'pdf_pages': pages, 'record_ids': [mapping[k] for k in ids]})
    sections.append({'key': 'XXXVIII_WORKED_PURCHASE_AND_FINAL_PARAGRAPH', 'pdf_pages': [253,254,255,256],
                     'record_ids': [mapping[r['id']] for r in c]})
    write('SECTION_COVERAGE.json', {'status': 'COMPLETE_DECLARED_FOURTH_HOUSE_SOURCE_SPAN',
        'sections': sections, 'page_coverage': [{'pdf_page': p, 'record_ids': [r['id'] for r in rows if p in r['source_locator']['pdf_pages']]} for p in range(236,257)],
        'boundary': {'first': 'Fourth-house heading/preamble on236',
                     'last': 'Final XXXVIII paragraph ending or my Wife a Scriveners Widdow above divider on256',
                     'next': 'Fifth-house heading and XXXIX on256 / printed222 below divider'},
        'all_local_ids_once': len(mapping)==len(rows), 'root_reading_receipt': 'READING_RECEIPT.json',
        'source_b_detailed_subsections': 'independent_review/source_b/SECTION_COVERAGE.json'})
    write('PRODUCER_RECONCILIATION.json', {'status': 'SOURCE_RECONCILIATION_COMPLETE_PENDING_FINAL_CLAIM_REVIEW',
        'all_raw_candidates_preserved': True, 'admitted_records': len(rows),
        'semantic_dispositions': [
            {'local_id':'B031','disposition':'Restore broader printed dignity maxim; retain raw narrower candidate and contextual tensions.'},
            {'local_id':'A019','disposition':'Retain isolated Moon occupation ambiguity; no supplied house.'},
            {'local_id':'A056','disposition':'Retain uncertainty whether one or both lords provide retrograde application.'},
            {'local_id':'A037','disposition':'Part of Fortune independently read before root corroboration; visible circled cross retained.'},
            {'local_id':'C005','disposition':'Mercury seventh-sector calculation is distinct from interpretive cusp influence; not declared an author error.'},
            {'local_id':'C002','disposition':'One actual chart CH01, no placeholder for canceled briefing recollection. Formula comparison does not alter frozen coordinates.'}],
        'briefing_correction':'Unverified silver-bells recollection withdrawn after original237 inspection. Glove/book anecdote is generic; no added case.',
        'producer_review_is_independent_evaluation':False})
    print(json.dumps({'records':len(rows),'first':rows[0]['id'],'last':rows[-1]['id'],
                      'unresolved':len(issues),'resolved':len(resolved)}))


if __name__ == '__main__': main()
