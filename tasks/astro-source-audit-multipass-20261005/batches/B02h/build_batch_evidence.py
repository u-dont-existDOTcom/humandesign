"""Build source context, evidence distinctions and unresolved-item ledgers."""
from pathlib import Path
import json
from collections import defaultdict
import lilly_third_house_reference as reference

ROOT=Path(__file__).resolve().parent


def save(name,data):
    (ROOT/(name+'.json')).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')


def main():
    d=json.loads((ROOT/'RULES.json').read_text()); rules=d['rules']
    ids={int(r['id'].rsplit('R',1)[1]):r['id'] for r in rules}
    grouped=defaultdict(list)
    for r in rules:grouped[r['scope_group']].append(r['id'])
    contexts={
        'third_house_scope':'Third-house heading and complete preamble only; preceding wealth continuation excluded.',
        'agreement':'Agreement with named brother, sister, neighbour or kin: first lord versus third lord; historical moral attributions only.',
        'absent_relative':'Absent brother is initial third-house significator; preserve written house placements and both turned and original-figure references; father/child/servant extensions explicit.',
        'reports_lilly_wartime':'Reports, news, intelligence and fears. Keep attributed ancient alternatives distinct from Lilly\'s own wartime experience; truth, tone and beneficiary separate.',
        'rumours_ancients':'Rules expressly headed according to the Ancients; conjunction of predicates and uncertainties retained, not merged into one score.',
        'advice_intention':'Visitor begins communicating advice; target is intention, not demonstrated accuracy or utility of the advice.',
        'siblings':'Horary enquiry despite stated natal preference; existence/composition/concord and rejected exact-count doctrine are different claims.',
        'short_journey':'Practical short journey; question proposal time, explicit application/dignity directions, incomplete direction ranking.',
        'worked_absent_brother':'One author-selected historical enquiry EX01/CH01. Requested outputs and two reported endpoint episodes are dependent; no original pre-outcome freeze.',
        'worked_cambridge_rumour':'One author-selected historical enquiry EX02/CH02. Past capture and future non-capture claims are separate; no separately reported confirmation in the span.',
        'hypothetical_siblings':'HY01 is explicitly hypothetical reuse of CH02; no additional historical enquiry, chart or sibling outcome.'
    }
    links=[
        (899,[898,900,901,902,903],'Scope and adverse alternatives remain visible; no majority-vote conflict algorithm.'),
        (902,[903,904,905],'Dignity exception, subsequent non-continuation and specific attributions.'),
        (909,[906,907,908,910,911,912],'Opening third-house context and aspect/reception alternatives.'),
        (910,[906,909],'Same malefic-contact branch, changed reception; still distress.'),
        (911,[906,908,912],'Do not exchange reception/no-reception pairings.'),
        (914,[906,915,916],'Fifth-house qualifications and alternative adverse branch.'),
        (921,[906,919,920,937],'Prior illness prerequisite and reference-frame qualification.'),
        (923,[906,937],'Fear of death is its own target, not the event.'),
        (926,[925,937],'Tenth-house context; tentative fear he is already dead.'),
        (929,[906,930,937],'Twelfth placement, received unimpeded Fortunes versus adverse alternatives.'),
        (933,[932],'Second-placement impediment and opportunity condition.'),
        (934,[935,936,937,938],'Turning, explicit original houses and unformalized variation coexist.'),
        (940,[939,941,942,943,944],'Historical attribution, full predicates and different report targets.'),
        (947,[946],'Only if planet actually signifies harm in the relevant context.'),
        (948,[949,950,951,952,953,954],'Ancient alternatives, contrary rule and epistemic limit retained.'),
        (956,[955,957,958],'Intention scope, north/south nodes and Haly attribution.'),
        (960,[959,961,962,963],'Natal caveat, composition branches and rejected count doctrine.'),
        (969,[967,968,970,971],'Short-journey scope, speed-transition ambiguity and direction limitations.'),
        (976,[974,975,977,937],'Both eighth lords; Moon excluded only from description; conditional killing query stops.'),
        (980,[978,979,982],'Probable same-day news versus source ephemeris report and later approximate episode.'),
        (986,[985,987],'Question-specific week conversion and reported relative weekday.'),
        (992,[990,991],'Future non-capture separated from past capture question.'),
        (998,[995,997],'Case political role and incomplete Venus minutes; no full translation-event computation.'),
        (1004,[1000,1001,1002,1003,1005,1006,1007],'All hypothetical, female predominance permits brothers, precise count withheld.'),
        (1008,[1000,1006,1007],'Hypothetical concord includes qualified square and platick sextile; no confirmed endpoint.')
    ]
    save('APPLICABILITY_AND_RELATIONS',{
        'status':'SOURCE_CONTEXT_NOT_EXECUTABLE_SCORING',
        'groups':[{'id':g,'context':contexts[g],'record_ids':v} for g,v in grouped.items()],
        'exception_and_context_links':[{'rule':ids[a],'must_carry':[ids[x] for x in bs],'reason':why} for a,bs,why in links],
        'example_dependencies':[{'rule':r['id'],'depends_on':r['dependency_rules']} for r in rules if r.get('dependency_rules')],
        'aggregation_algorithm':None,'orb_or_cusp_threshold_added':None,
        'source_characterizations_are_verified_personal_facts':False
    })
    issues=[
        ('Unspecified combination and precedence',[222,226],'Good and adverse testimonies coexist; varying rules is required without a complete priority/tie algorithm.'),
        ('Asymmetric-contact Boolean punctuation',[222],'The Fortune/first-lord contact and missing reciprocal contact need their compound scope preserved.'),
        ('Node and dignity-clause scope',[222],'The joint Saturn/Mars/node phrasing does not define essential dignities for the node.'),
        ('Turned and original-figure reference frames',[223,224,225,226,231],'Both are explicit and the worked example uses both eighth lords. Their full interaction/precedence is not formalized.'),
        ('Opening third-house context and reception direction',[223],'Inherited placement context and unexpressed reception direction/mutuality must not be silently generalized.'),
        ('Fifth-house reception grammar',[223,224],'Reception of a Fortune or not and the stronger conjunction/soft-aspect clause have uncertain attachment.'),
        ('Cancelled word before naturally ill',[224],'Original ink obscures a condition-changing word. Neither restoring not nor deleting it is admitted.'),
        ('Old aspect-origin phrasing',[224],'Out of the sixth/eighth is not a clean outside-house negation; attachment to body/origin remains uncertain.'),
        ('Father paragraph reference wording',[225,226],'Ascendant of your Question is awkward beside the newly selected fourth-house Ascendant and later explicit turning examples.'),
        ('Ancient intelligence frame plurality',[226],'Fifth-house and triplicity-lord alternatives are attributed without a single chosen complete procedure.'),
        ('Retrograde adjective reach in news harm clause',[227],'Its reach into later Mars/Saturn aspect alternatives is not uniquely formalized.'),
        ('Fixed-sign reach in angular alternatives',[227],'Punctuation does not settle which opening angular branches inherit fixed sign.'),
        ('Moon received in fixed fourth/tenth',[228],'Received in them is not locally expanded into a unique reception/placement predicate.'),
        ('Visibly printed ufortunate',[228],'Moon word could reverse an alternative. Preserve visible spelling and leave that condition unresolved.'),
        ('Retrogradation, affliction and those two',[228],'Shared predicate reach and pronoun antecedent in the ill-rumour rule remain unclear.'),
        ('Sex-classification syntax and house definition',[229],'Masculine/feminine sign, house and contact alternatives need their syntax retained; no new planetary-hour method.'),
        ('Swift or slow transition',[229,230],'Inspection instruction is awkwardly attached to favourable list; not a clean assertion that either speed is favourable.'),
        ('Short-journey square target and hemisphere',[230],'Square target is not repeated and local hemisphere convention is absent.'),
        ('Principal-direction selector',[230],'Cusp sign and planetary placements are mixed in an unspecified dignity ranking; no unique tie procedure.'),
        ('Jupiter degree glyph in first figure',[230,231],'Canonical degree/sign remain null.4/14 remain plausible;24 is provisional and may missegment the Jupiter glyph. Conditional residuals do not decide the print.'),
        ('Coordinate provenance and figure geometry',[230,234],'Some body signs derive from diagram sectors; Sun/MC in first figure share one entry. Do not call these independent printed signs or observations.'),
        ('Omitted coordinate minutes',[230,234,235],'First-figure nodes and second-figure Venus lack minutes. Exact contacts fail closed; optional ranges name assumptions.'),
        ('Qualitative affliction, cusp influence and orbs',[231,234,235],'Vitiate/on/within-orbs language does not specify a new exact-minute threshold; arithmetic neither validates nor invalidates those qualitative effects.'),
        ('Historical clock, calendar and sky parity',[230,232,233,234],'No original Eichstadius parity, exact meridian reduction, modern calendar convention or physical contact trajectory is computed.'),
        ('Direction classes and travel distance',[232],'Southeast is within a known destination county. Sagittarius northeast here versus earlier East classification remains contextual variation; no precise mixing or distance formula.'),
        ('Qualitative one-degree/week conversion',[230,233],'Printed Venus28:53 leaves1:07, while prose uses one degree and less than a week with question-specific discretion; no automatic proportional clock conversion.'),
        ('Cambridge future forecast horizon',[233,235],'Future non-capture has no stated horizon; source gives no separate confirming endpoint for either capture claim.'),
        ('All signs scope in hypothetical gender claim',[235],'Relevant fruitful signs are feminine; next clause calls Moon\'s Gemini masculine. Do not read all as every sign anywhere in the chart.'),
        ('Elliptical negations in hypothetical concord',[235],'No wayes afflicted, or any ill aspect is grammatically elliptical; apparent negation retained, not an ill aspect made favourable.')
    ]
    issue_rows=[]
    for n,(title,pages,detail) in enumerate(issues,1):
        key=f'B02h-U{n:02d}'
        issue_rows.append({'id':key,'title':title,'pdf_pages':pages,'detail':detail,
            'status':'PRESERVED_NOT_SILENTLY_RESOLVED','record_ids':[r['id'] for r in rules if key in r['unresolved_ids']],
            'runtime_disposition':'No predictive branch promoted; retain qualification or incomplete input.'})
    save('UNRESOLVED',{'issues_count':len(issue_rows),'issues':issue_rows,
        'count_note':'Source-specific textual, methodological, precision and evidence limitations; these are not29 independent historical contradictions.'})
    raw=json.loads((ROOT/'WORKED_NUMERIC_TABLES.json').read_text())
    save('HISTORICAL_CASES',{
        'printed_charts':2,'actual_historical_enquiries':2,'explicit_hypothetical_reuses':1,
        'reported_operational_endpoint_episodes':2,'independent_validation_cases':0,
        'counting_note':'One carrier episode contains arrival, approximate time and news of life/health. Homecoming is another episode in the same enquiry. Multiple records are not independent cases.',
        'cases':{
            'EX01':{'chart':'CH01','name':'Absent London brother,1645','source_pages':[230,231,232,233],
                'question_known_information':['Brother went into West of England','No news for many weeks','London home'],
                'requested_endpoints':['alive/dead','soldier killing only if dead','news time if alive','location if alive','return home'],
                'reported_endpoint_episodes':raw['reported_endpoints'],
                'additional_author_descriptions':raw['other_author_descriptions'],
                'location_confirmation':None,'one_or_two_days_distance_confirmation':None,
                'original_prediction_freeze_available':False,'independent_external_verification':False},
            'EX02':{'chart':'CH02','name':'Cambridge capture rumour,1643','source_pages':[233,234,235],
                'judgements':[{'target':'alleged existing capture','claim':'not taken; report false','separate_confirmed_result':None},
                    {'target':'future capture by king or forces','claim':'should not be taken','forecast_horizon':None,'separate_confirmed_result':None},
                    {'target':'beneficiary of the report','claim':'good for Parliament and no benefit for enemies','separate_confirmed_result':None}],
                'reported_endpoint_episodes':[],'original_prediction_freeze_available':False,'independent_external_verification':False}
        },
        'hypothetical':{'HY01':{'reuses_chart':'CH02','source_page':235,'actual_enquiry':False,
            'topics':['sibling abundance','female predominance with brother indications','exact count withheld','concord'],
            'reported_endpoints':[],'independent_case':False}}
    })
    save('QUERY_REFERENCES',{
        'absent_relatives':{name:reference.absent_relative_house_reference(name) for name in ['brother','father','child','servant']},
        'question_times':{name:reference.question_time_reference(name) for name in ['news_heard_by_self','news_proposed_by_another','advice_visit']},
        'worked_dual_eighth':{'source_page':231,'original_eighth_lord':'Mercury','eighth_from_brother_third_is_original_house':10,'that_lord':'Mars'},
        'current_person_judgements':0
    })
    sections=[
        ('THIRD_HOUSE_PREAMBLE',[221],'below divider; complete heading and preamble'),
        ('XXIX_AGREEMENT',[222],'entire chapter opening'),
        ('ABSENT_BROTHER_AND_EXTENSIONS',[223,224,225,226],'to varying-rules paragraph above reports heading'),
        ('REPORTS_NEWS_INTELLIGENCE_FEARS',[226,227],'own wartime experience and prejudice question'),
        ('RUMOURS_ACCORDING_TO_ANCIENTS',[227,228],'heading near bottom227 through secrecy paragraph228'),
        ('COUNSEL_ADVICE',[228],'complete heading and section'),
        ('WHETHER_SIBLINGS',[229],'complete existence, composition, count and concord material'),
        ('SHORT_JOURNEY',[229,230],'ends with due limitations above230 divider'),
        ('XXX_EXAMPLE',[230,231,232,233],'starts heading/chart230; setup precedes XXX heading231; closes above XXXI divider233'),
        ('XXXI_EXAMPLE_AND_HYPOTHETICAL',[233,234,235],'includes case preamble233, chart234 and hypothetical sibling reinterpretation235')
    ]
    save('SECTION_COVERAGE',{'status':'COMPLETE_DECLARED_THIRD_HOUSE_SOURCE_SPAN',
        'sections':[{'key':key,'pdf_pages':pages,'position':position} for key,pages,position in sections],
        'new_numbered_chapters':[29,30,31], 'numbered_chapters_now_read':31,'headed_chapter_units_now_read':32,
        'count_note':'Earlier duplicate XVI headings remain distinct. Unnumbered sections are explicit coverage items, not new numbered chapters.',
        'first_record':rules[0]['id'],'last_record':rules[-1]['id'],'records_count':len(rules),
        'next_source_to_extract':{'pdf_page':236,'printed_page':202,'heading':'Of the fourth House, and the Judgment depending thereupon.',
            'position':'Start with entire heading and preamble, then XXXII To find a thing hid or mislaid on the same page.',
            'boundary_visually_checked':True,'extracted':False}})
    save('CROSS_SOURCE_COMPARISONS',{'scope':'Within Lilly, comparing current original-page reading with previously extracted retained records; no new Ptolemy or other-author extraction.',
        'comparisons':[
            {'topic':'Question selects house frame','retained':['LI.1647.II.XXIV.R668','LI.1647.II.XXIV.R669','LI.1647.II.XXIV.R692'],'current':[ids[x] for x in [906,934,935,936,937,976]],'finding':'At-home stranger7, general absent unrelated person1, absent brother3 and named relative frames are distinct. Both original and turned eighth lords appear in the new example.'},
            {'topic':'Question-time conventions','retained':['LI.1647.II.XXVI.R772','LI.1647.II.XXVI.R773','LI.1647.II.XXVI.R774'],'current':[ids[944],ids[955]],'finding':'Proposal, first hearing, first disclosure of advice, delayed-letter understanding and self-question context remain separate historical conventions.'},
            {'topic':'Sign classifications and explicit cross-references','retained':['LI.1647.I.XVI.divisions.R255','LI.1647.I.XVI.divisions.R256','LI.1647.I.XVI.divisions.R265','LI.1647.I.XVI.divisions.R272'],'current':[ids[x] for x in [960,1001,1002,1003,1005,1008]],'finding':'Core fruitful Cancer/Scorpio/Pisces and gender groups agree with retained pages122–123 (printed88–89); local less-fruitful Aquarius/Sagittarius/Gemini list stays additional. Gemini and Pisces are in retained short-ascension group. Root compared retained source records; did not newly reread these earlier page images.'},
            {'topic':'Direction reference levels','retained':['LI.1647.I.XVI.profiles.R333','LI.1647.II.XXII.R608','LI.1647.II.XXII.R609'],'current':[ids[983],ids[984]],'finding':'Known country/region and within-country direction are separate levels. Sagittarius is East in earlier profile, northeast in this worked passage; preserve both and no universal compass reduction.'},
            {'topic':'Application and retrograde heavier planet','retained':['LI.1647.I.XIX.R406','LI.1647.I.XIX.R407'],'current':[ids[978],ids[979]],'finding':'Slower retrograde Saturn can apply toward Venus; present static residual20arcminutes is not a recomputed contact time.'},
            {'topic':'Translation definition versus full perfection prerequisites','retained':['LI.1647.I.XIX.R440','LI.1647.I.XXI.R559','LI.1647.I.XXI.R560'],'current':[ids[998],ids[1008]],'finding':'New figure describes Moon transferring Jupiter to Venus. Do not infer that abbreviated worked prose erases earlier reception/no-intervening-contact conditions, and do not claim those event conditions were computationally verified.'},
            {'topic':'Timing discretion and units','retained':['LI.1647.II.XXVII.R834','LI.1647.II.XXVII.R835','LI.1647.II.XXVIII.R877'],'current':[ids[979],ids[986],ids[987]],'finding':'Clock contact, symbolic one-degree/week judgement and reported relative weekday are different layers; local house-pair wealth units are not substituted for the common-sign homecoming illustration.'},
            {'topic':'Reception and hard aspects are context-sensitive','retained':['LI.1647.II.XXVIII.R885','LI.1647.II.XXVIII.R886'],'current':[ids[910],ids[911],ids[912],ids[915],ids[1008]],'finding':'Reception and condition qualify hard-aspect outcomes. The new short-ascension square is explicitly favourable in its hypothetical context; no universal positive or negative aspect score follows.'}
        ]})
    print(json.dumps({'context_groups':len(grouped),'issues':len(issues),'records':len(rules),'historical_enquiries':2,'hypothetical_reuses':1}))

if __name__=='__main__':main()
