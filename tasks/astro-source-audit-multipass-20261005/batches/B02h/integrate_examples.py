"""Normalize the separately extracted examples without adding new source claims."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
SOURCE_ID = "LILLY1647_WELLCOME_B30338724"
SOURCE_SHA256 = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
TITLES = [
    "Absent brother: one historical figure and conditional questions",
    "Asker's physique: source description and rationale",
    "Absent brother: Taurus third cusp and Venus",
    "Moon excluded only from description of the parties",
    "Living and healthy judgement checks both eighth lords",
    "Living judgement closes only the conditional killing enquiry",
    "Mutual application includes retrograde Saturn",
    "Eichstadius timing and London-meridian reduction are source reports",
    "Same-day news forecast is qualified as probable",
    "Practical advice to seek information from carriers",
    "One reported carrier episode: time, life and health news",
    "Southeast location is within the already known destination county",
    "Distance expressed as one or two days of travel",
    "Sign change interpreted as return to property at home",
    "One degree and a week: question-specific timing judgement",
    "Reported homecoming the following Tuesday",
    "Author's testimony of existing brotherly concord",
    "Vary third-house judgement with the actual question",
    "Cambridge rumour: historical enquiry and second figure",
    "Cambridge capture report judged false",
    "Future non-capture is an additional forecast",
    "Movable angles plus afflicted cusps: combined first argument",
    "Cadent Moon in Gemini: second argument",
    "Cambridge political sides and significators",
    "North node described on Ascendant: benefit to Parliament",
    "Side comparison: Venus exalted, Mars in fall and squared",
    "Moon carries Jupiter's light to Venus: benefit expectation",
    "Mars-Saturn square interpreted as enemy division",
    "Same chart hypothetically reused for siblings",
    "Hypothetical sibling chain: third-cusp Scorpio",
    "Hypothetical sibling chain: Mars in Cancer",
    "Hypothetical sibling chain: Moon applies to Venus in Pisces",
    "Hypothetical abundance of siblings or kindred",
    "Hypothetical female predominance and its local sign context",
    "Masculine indications still permit brothers",
    "Exact sibling count expressly withheld",
    "Hypothetical concord includes a qualified applying square",
]
ISSUES = {
    1:[24],5:[20,21,23],8:[24],12:[25],13:[25],15:[26],16:[24],
    19:[21,24],21:[27],22:[23],25:[23],27:[22,24],32:[21],
    34:[28],35:[23],37:[22,23,29]
}
TEMPORAL = {
    5:"Alive and healthy at enquiry; no casualty judged",
    8:"Five in the afternoon, reduced to a little after four; source-reported clock conventions",
    9:"Probably that same day", 11:"About four on the question day, source-reported",
    12:"Current location within the visited county",13:"Distance as one or two days' travel",
    15:"Less than one week forecast",16:"Tuesday following, source-relative weekday only",
    17:"Always did and still do, author's relationship description",
    20:"Alleged prior/current capture",21:"Future non-capture, horizon unspecified",
    37:"Hypothetical current/future kin and future siblings; no interval"
}


def main():
    raw = json.loads((ROOT/'independent_review/examples/CANDIDATE_RULES.json').read_text())
    assert len(raw['candidates']) == len(TITLES) == 37
    idmap = {f'C{n:03d}':f'LI.1647.II.{"XXX" if n<=18 else "XXXI"}.R{971+n}' for n in range(1,38)}
    rules = []
    for n,c in enumerate(raw['candidates'],1):
        assert c['id'] == f'C{n:03d}'
        section = 'XXX' if n <= 18 else 'XXXI'
        group = 'worked_absent_brother' if n<=18 else ('worked_cambridge_rumour' if n<=28 else 'hypothetical_siblings')
        limits = list(c['modifiers_and_exceptions'])
        limits += c['unresolved_items']
        limits += ['Historical worked judgement or source testimony only; not an independently verified outcome or an automatic universal rule.']
        if n>=29:
            limits += ['Explicit hypothetical reuse of Cambridge chart; no additional actual enquiry, chart or reported sibling outcome.']
        r = {
            'id':idmap[c['id']], 'title':TITLES[n-1], 'kind':c['source_assertion_type'],
            'source_locator':{
                'source_id':SOURCE_ID,'source_sha256':SOURCE_SHA256,'book':'II',
                'section_key':f'II.{section}','pdf_pages':c['pdf_pages'],
                'printed_sequence_expected':[p-34 for p in c['pdf_pages']],
                'visible_printed_labels':c['literal_visible_folios'],
                'passage_anchor':c['evidence'][0]['passage_anchor'],
                'anchor_note':'Locating incipit/topic; normalized glyph names and spelling, not a diplomatic quotation.',
                'specific_passages':c['evidence']
            },
            'genre':'horary','statement_type':'editor_normalized_paraphrase',
            'source_attribution':'Lilly; historical example' if n<29 else 'Lilly; explicit hypothetical reinterpretation',
            'scope_group':group,'source_statement':c['faithful_paraphrase'],
            'prerequisites':c['prerequisites_and_alternatives']['prerequisites'],
            'source_alternatives':c['prerequisites_and_alternatives']['alternatives'],
            'qualifications_and_limits':limits,'temporal_target':TEMPORAL.get(n,'Not specified locally'),
            'unresolved_ids':[f'B02h-U{x:02d}' for x in ISSUES.get(n,[])],
            'runtime_status':'REFERENCE_ONLY_NOT_PROMOTED','independent_evidence_unit':False,
            'candidate_origin':f'B02h.examples.{c["id"]}',
            'case_id': 'EX01' if n<=18 else ('EX02' if n<=28 else 'HY01'),
            'house_numbering_and_roles':c['house_numbering_and_roles'],
            'source_defined_calculations':c['source_defined_calculations'],
            'numeric_table_references':c['numeric_table_references'],
            'evidence_status':c['reported_outcome_vs_forecast_inference_author_testimony'],
            'dependency_rules':[idmap[x] for x in c['depends_on_candidates']],
            'generality':c['generality']
        }
        rules.append(r)
    (ROOT/'EXAMPLE_RULES_RECONCILED.json').write_text(json.dumps({'source_id':SOURCE_ID,'source_sha256':SOURCE_SHA256,'rules':rules},indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'examples':len(rules),'first':rules[0]['id'],'last':rules[-1]['id']}))

if __name__=='__main__': main()
