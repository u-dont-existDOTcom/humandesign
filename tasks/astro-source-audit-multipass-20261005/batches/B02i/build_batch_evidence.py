"""Build B02i case/context ledgers and the additive current index checkpoint."""
from pathlib import Path
from copy import deepcopy
import hashlib
import json

ROOT = Path(__file__).resolve().parent
TASK = ROOT.parent.parent
REPO = ROOT.parents[3]


def load(path): return json.loads(path.read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path, value): path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')


def main():
    ids = load(ROOT/'RECORD_ID_MAP.json')
    def refs(*local): return [ids[k] for k in local]
    episode_rows = [
        ('negotiation','Many meetings; seller maintained £530 demand.', ['C006','C011'], 'During negotiation'),
        ('rival','A jovial rival tried to obtain property.', ['C012'], 'After beginning, before conclusion; margin explicit'),
        ('daughter_assistance','Seller daughter supported Lilly and blocked interlopers.', ['C013'], 'During transaction; exact date unstated'),
        ('loan','Friend lent £500.', ['C015'], 'Twelve days after in narrative; antecedent/Mars–Jupiter coordination unresolved'),
        ('bargain','Author bargained for the houses.', ['C017'], '25April of case year'),
        ('completion','Author paid £530 and conveyance was sealed.', ['C018'], '17May of case year'),
        ('financial_evaluation','Hard bargain and financial injury, amount unstated.', ['C026','C027'], 'Retrospective narration'),
        ('satisfaction','Author did not regret it, citing attachment and prior history.', ['C028'], 'At narration in1647'),
    ]
    episodes = [{'id':k,'reported_content':v,'record_ids':refs(*r),'time':t,
                 'independent_case':False,'independent_verification':False} for k,v,r,t in episode_rows]
    save(ROOT/'HISTORICAL_CASES.json', {
        'schema_version':1,'batch':'B02i','dated_enquiry_count':1,'printed_chart_count':1,
        'independently_verified_outcome_count':0,
        'cases':[{'id':'LILLY_PURCHASE_1634','chart_id':'CH01','pdf_pages':[253,254,255,256],
            'question':'Whether to deal with the seller and obtain funds in time to buy Master B houses',
            'record_ids':refs(*[f'C{i:03d}' for i in range(1,30)]),
            'source_date':{'year':1634,'month':3,'day':31,'hour':6,'meridiem':'PM','minute':None,'calendar':None,'timezone':None},
            'prior_known_information':[{'content':'Already desirous and fully resolved to buy','record_ids':refs('C001')},
                {'content':'Own funds required six months notice to call in','record_ids':refs('C001','C014')}],
            'source_presented_judgements':refs('C003','C004','C005','C006','C007','C008','C009','C010','C012','C014','C015','C016'),
            'episodes':episodes,
            'body_mark_records':refs('C020','C021','C022','C023','C024'),
            'body_mark_classification':'Five retrospective self-reports within one account; not independent cases or concealed tests.',
            'not_verified_endpoints':[{'content':'Many-year structural durability','record_ids':refs('C016')},
                {'content':'Many leases outlast author lifetime','record_ids':refs('C026')}],
            'exact_dates_prospectively_frozen':False,'external_event_corroboration':None,
            'evidence_limit':'The narrative presents judgments and subsequent reports; no independently dated prediction document or third-party outcome record has been inspected.'}],
        'unspecified_experience_accounts':[
            {'id':'hidden_objects','record_ids':refs('A014'),'description':'Generic glove/book/other-object experiments, no individual date/chart/trial count.'},
            {'id':'reconciliation','record_ids':refs('A049'),'description':'Repeated good experience asserted, no named enquiry or denominator.'},
            {'id':'relocation','record_ids':refs('B011'),'description':'No remembered regrets and later thanks/rewards; no enumerated cases or denominator.'}],
        'non_case_material':[{'record_ids':refs('B012'),'classification':'Theological explanation and author opinion'},
                             {'record_ids':refs('C029'),'classification':'Autobiographical polemic concerning Wharton'}],
        'case_count_is_predictive_sample_size':False})
    save(ROOT/'APPLICABILITY_AND_RELATIONS.json', {
        'scope':'Historical horary; no natal transfer or present-person use admitted by this batch.',
        'reference_model':'Query type, ownership, actors, source predicates, outcome and timing remain separate.',
        'relations':[
            {'from':refs('A002'),'to':refs('B024','B025','B026'),'relation':'Owned hidden goods versus generic missing goods; XXXVII explicitly returns to XXXII for location after unremoved finding.'},
            {'from':refs('A015','A024','A036'),'relation':'Separate purchase, land-quality and rental frames; tenth is price/timber/profit respectively.'},
            {'from':refs('A009'),'to':refs('A010','A011'),'relation':'Attributed ancient method criticized, then alternative introduced; not equivalent votes.'},
            {'from':refs('A053'),'to':refs('A054','A055'),'relation':'Wait for exit; urgent means exception; explicit limitation on coercing father will.'},
            {'from':refs('B027','B028','B029','B030'),'to':refs('B048','B049','B050'),'relation':'Presence of treasure is distinct from acquisition and difficulty.'},
            {'from':refs('B056','B057','B058','B059','B060','B061','B062'),'relation':'Terminal block expressly attributed to Alkindus, not a separate modern source confirmation.'},
            {'from':refs('C017','C018'),'to':refs('C026','C027','C028'),'relation':'Bargain and completion differ from financial benefit and later satisfaction.'}],
        'not_implemented':['A complete chart engine','Unstated orbs and strength thresholds','An interpretation of ambiguous Boolean scope','Global conflicting-testimony priorities','Precise bearing or physical digging depth','Ephemeris and civil-date conversion','Predictive outcome scoring']})

    # Make derived comparison pointers usable from the delivered batch.
    cmp = load(ROOT/'CROSS_SOURCE_COMPARISONS.json')
    ex = load(ROOT/'RETAINED_SOURCE_EXCERPTS.json')
    cmp.setdefault('root_normalization','Local candidate and note links mapped to included files; source statements are unchanged.')
    paths = {'A':'source_a','B':'source_b','C':'worked_chart'}
    for row in cmp['comparisons']:
        for ev in row.get('b02i_evidence',[]):
            if 'local_id' in ev:
                ev['record_id'] = ids[ev['local_id']]
                ev['candidate_file'] = 'independent_review/source_b/CANDIDATE_RULES.json'
            if 'note_file' in ev:
                ev['note_file'] = f"independent_review/{paths[ev['span']]}/SOURCE_FIRST_NOTES.md"
    supplements = []
    for batch,wanted in [('B02a',['LI.1647.I.04.R033','LI.1647.READER.R007']),
                         ('B02e',['LI.1647.II.XXIII.R625','LI.1647.II.XXIII.R631'])]:
        path = ROOT.parent/batch/'RULES.json'; data = load(path)
        key = 'rules' if 'rules' in data else 'records'
        for i,record in enumerate(data[key]):
            if record['id'] not in wanted: continue
            prior = next((n for n,r in enumerate(ex['retained_records']) if r['record']['id']==record['id']),None)
            if prior is None:
                prior = len(ex['retained_records'])
                ex['retained_records'].append({'retained_record_id':record['id'],'batch':batch,
                    'retained_file':str(path.relative_to(REPO)),'retained_file_sha256':sha(path),
                    'json_pointer':f'/{key}/{i}','copy_status':'EXACT_FULL_RETAINED_RECORD',
                    'record':deepcopy(record)})
            supplements.append({'record_id':record['id'],'batch':batch,
                                'excerpt_pointer':f'/retained_records/{prior}/record',
                                'source_locator':record['source_locator']})
    for key,topic,selected,locals_,statement in [
        ('B02i-CMP11','Geometric house versus near-cusp virtue',['LI.1647.I.04.R033'],['C005'],
         'Mercury lies2°48′ before H8 in geometric H7. The earlier five-degree virtue convention makes an eighth-house interpretation plausible. The later prose does not explicitly explain its Mercury omission, so the reading remains qualified rather than a demonstrated chart error.'),
        ('B02i-CMP12','Printed Fortune versus the earlier selected formula',['LI.1647.II.XXIII.R625','LI.1647.II.XXIII.R631','LI.1647.READER.R007'],['C002','C015'],
         'The earlier selected same-day/night formula gives Pisces3°27′ from the printed purchase inputs, versus Pisces12°27′ printed. The alternate nocturnal formula is not silently substituted. A targeted root read of original errata PDF888 found no printed219 correction; its printed209 last-line other entry does not change the rental paragraph meaning already retained.')]:
        if not any(r['comparison_id']==key for r in cmp['comparisons']):
            cmp['comparisons'].append({'comparison_id':key,'topic':topic,'relation':'qualified_source_comparison',
                'earlier_records':[r for r in supplements if r['record_id'] in selected],
                'b02i_record_ids':refs(*locals_),'comparison_statement':statement,
                'limits':['Earlier records used as retained evidence; only errata888 freshly reread outside the admitted span.','No source coordinate repaired, no definitive printer-error attribution, no empirical validation.']})
    ex['retained_records_count'] = len(ex['retained_records'])
    cmp['retained_excerpt_count'] = len(ex['retained_records']); cmp['comparison_count']=len(cmp['comparisons'])
    save(ROOT/'RETAINED_SOURCE_EXCERPTS.json',ex);save(ROOT/'CROSS_SOURCE_COMPARISONS.json',cmp)
    receipt=load(ROOT/'READING_RECEIPT.json')
    receipt['targeted_outside_span_original_pages_read']=[{'pdf_page':888,'purpose':'Check author errata for current source block and printed Fortune discrepancy','render_dpi':120,
        'image_sha256':sha(Path('/workspace/scratch/bd2460f96de0/b02i-errata-p888.png')),
        'finding':'No printed219 erratum; printed209 last-line other preserves already extracted neither-party-pleased sense. No source values changed.'}]
    save(ROOT/'READING_RECEIPT.json',receipt)
    save(ROOT/'TEXT_IMAGE_CHECKS.json',{'current_span_pages':list(range(236,257)),
        'checks':[
            {'pdf_page':237,'finding':'No chart; withdrawn briefing recollection was unsupported.'},
            {'pdf_page':238,'finding':'Eight slots; exact by-directions; generic glove/book anecdote.'},
            {'pdf_page':242,'finding':'Rental favourable final glyph is Part of Fortune; conjunction of moiety conditions preserved.'},
            {'pdf_page':243,'finding':'Final neither-one-nor-other sense unchanged by author errata other entry.'},
            {'pdf_page':248,'finding':'Rain list Cancer, Leo, Aquarius, Pisces; no Scorpio substitution.'},
            {'pdf_page':251,'finding':'Weak mine paragraph names Saturn, not text-layer Mars-like OCR.'},
            {'pdf_page':253,'finding':'Mars11°6′, Fortune12°27′, and H4/H10 minute omission; body signs inferred from sectors.'},
            {'pdf_page':254,'finding':'Margin dates competitor after beginning/before conclusion.'},
            {'pdf_page':255,'finding':'17May Venus glyph belongs to conjunction clause; separate25April bargain and17May payment.'},
            {'pdf_page':256,'finding':'Final XXXVIII paragraph above divider included; fifth-house heading/XXXIX below not extracted.'},
            {'pdf_page':888,'finding':'Targeted errata read; no printed219 correction supplies an alternate Fortune.'}],
        'source_pdf_sha256':receipt['source_sha256'],'no_new_ocr':True})
    index_path=TASK/'LILLY_SOURCE_EXTRACTION_INDEX_V1.json'; index=load(index_path)
    rows=[r for r in index['batches'] if r['id']!='B02i']
    assert sum(r['records_count'] for r in rows)==1008
    records=load(ROOT/'RULES.json')['records_count']
    rows.append({'id':'B02i','path':'batches/B02i/RULES.json','records_count':records,'sha256':sha(ROOT/'RULES.json'),
                 'scope':'Complete fourth-house heading/preamble and XXXII–XXXVIII, PDF236 through256 top before fifth-house divider; one retrospective purchase figure.'})
    index.update({'status':'BOOK_I_COMPLETE_BOOK_II_THROUGH_XXXVIII_READ_OTHER_SECTIONS_OPEN',
        'records_count':1008+records,'batches':rows,'read_numbered_chapters':list(range(1,39)),
        'read_headed_units_count':39,'current_state':'state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261010_B02i.md',
        'next':{'pdf_page':256,'printed_page':222,'heading':'Of the fifth House, and its Questions.',
                'position':'Below the horizontal divider, include fifth-house heading, then XXXIX If one shall have Children, yea or no? and opening paragraph.',
                'boundary_previewed_but_not_extracted':True}})
    save(index_path,index)
    print(json.dumps({'source_records':records,'Lilly':index['records_count'],'combined_with_Ptolemy':index['records_count']+1066,
                      'comparisons':cmp['comparison_count'],'retained_excerpt_records':ex['retained_records_count']}))


if __name__=='__main__': main()
