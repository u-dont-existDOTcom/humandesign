#!/usr/bin/env python3
"""Original 1647 Lilly LXXIX, parsonage loss case; historical source only."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent; ROWS=[];SPANS=[]
def add(pages,label,*claims):
    sid=f'LXXIX-S{len(SPANS)+1:03}';ids=[]
    for role,anchor,meaning,limit in claims:
        local=f'LXXIX-C{len(ROWS)+1:03}';ids.append(local)
        ROWS.append({'source_local_id':local,'batch':'B03y','role':role,
         'chapter':'LXXIX' if role!='next_navigation' else 'LXXX_NAVIGATION_ONLY',
         'original_pdf_pages':list(pages),'printed_pages':[n-34 for n in pages],
         'short_original_anchor_not_diplomatic':anchor,'historical_author_paraphrase':meaning,
         'original_source_qualifications':limit,'global_record_number':None,
         'historical_documentary_accepted':False,
         'independently_authenticated_parsonage_case':False,
         'empirically_validated_prediction':False,'runtime_model_promoted':False})
    SPANS.append({'span_id':sid,'original_pdf_pages':list(pages),
      'passage_label':label,'mapped_local_ids':ids})
add([471],'LXXIX original heading and separate circular horoscope',
 ('heading','Chap LXXIX Parsonage','Lilly poses whether the applicant will obtain the desired parsonage.','Distinct worked example from earlier general appointment chapter.'),
 ('chart_timestamp','6 August 1644 8 24 P M','The printed circular question figure is dated 6 August 1644 at 8:24 PM.','Historical local time/calendar not recast independently.'),
 ('case_scope','Judgement upon this Figure','The author supplies a horary judgment for the applicant.','Not a prospectively deposited chart or independent evaluation.'))
add([471,472],'Querent, house and benefit significators',
 ('figure_assignment','querent Sign ascending','The querent is assigned the rising sign.','Chart source assignment only.'),
 ('condition','Saturn therein posited','Saturn is described as positioned within the ascendant.','Exact dignity and geometry remain unrecast.'),
 ('condition','Mars Lord of ascendant in Gemini','Mars is called ascendant ruler and placed in an airy Gemini sign.','Printed authorship, not independently recomputed.'),
 ('condition','Moon in Aquarius triplicity','Moon is called in Aquarius and the same triplicity.','Source triplicity claim; numerical ephemeris not checked.'),
 ('figure_assignment','ninth house Jupiter Lord','Jupiter as lord of ninth is used for the desired benefice.','Distinct from generic public tenth house.'),
 ('figure_assignment','Significators of the Benefice','The ninth lord and its house testimony represent the ecclesiastical benefit.','Outcome endpoint is getting a parsonage, not subjective satisfaction.'))
add([472],'Six enumerated non-perfection or denial factors',
 ('condition','no conjunction Jupiter Mars','Lilly finds no conjunction between Jupiter ninth ruler and Mars ascendant ruler.','First part of printed reason 1.'),
 ('condition','Moon no aspect Jupiter','He also finds no Moon aspect to Jupiter.','Separate lack of perfection testimony in first numbered reason.'),
 ('condition','Mars not placed ninth','Mars is not in the ninth.','Part of second printed reason.'),
 ('condition','Moon not placed ninth','Moon is not in the ninth.','Second part of second printed reason.'),
 ('condition','no weighty Planet translates','No strong planet translates Jupiter light to Mars, according to Lilly.','Printed third reason, distinct from collecting.'),
 ('condition','nor collects the light','No strong planet collects Jupiter light to Mars.','Translation and collection not merged.'),
 ('condition','no reception Jupiter Mars','There is no reception between Jupiter and Mars.','Fourth printed reason.'),
 ('condition','Saturn impedited in ascendant','Saturn in ascendant is impaired and judged unfavorable.','Fifth printed reason; do not treat all Saturn placements as unconditional denial.'),
 ('historical_inference','querent despaire obtaining','Lilly interprets Saturn condition as the applicant losing hope.','Unmeasured sentiment; author interpretation.'))
add([472],'Moon Mercury testimony, neighbor obstruction',
 ('condition','Moon separates trine of Mars','Moon is separating from a trine to Mars.','Sixth printed reason begins with separation.'),
 ('condition','applies opposition Mercury','Moon applies to an opposition to Mercury.','Applying testimony, separate from previous separating trine.'),
 ('condition','Mercury Lord of third','Mercury rules the third house in this judgment.','Historical chart relationship.'),
 ('source_internal_forecast','neighbour letter words information','The author forecasts a neighbor could sabotage the applicant with letter, speech or unfavorable information.','Multiple possible modes of interference, not precise preregistered one.'),
 ('source_internal_forecast','wholly destroy hopes','Lilly predicts the applicant will fail from such information.','Unverified prospective record of when prediction was made.'),
 ('historical_inference','Mercuriall Scholars Divines enemies','He expects scholars or divines to oppose the applicant as Mercury-associated persons.','Broad archetypal category; no verified identification.'),
 ('condition','Venus Libra seventh opposite','Venus is placed in Libra and seventh house opposite the ascendant in the original interpretation.','A separate planetary branch from Moon/Mercury.'),
 ('source_internal_forecast','Women inform or prejudice suit','He forecasts some women may inform against or disadvantage the applicant.','Additional alternative cause, not documented independent informant.'))
add([472],'Advice, application, scandalous letter, retrospective loss',
 ('authorial_recommendation','dehorted proceeding further','Lilly says he discouraged the parson from pursuing the benefice.','Advice recorded only by author; not an external documentary transcript.'),
 ('authorial_characterization','Parson covetous proceed','Lilly calls the applicant covetous and says he proceeded despite advice.','Author judgment about motive, not proven clinical trait.'),
 ('authorial_outcome_claim','thought matter absolutely on his side','The author reports the applicant eventually believed he would succeed.','No external dated application paperwork.'),
 ('authorial_outcome_claim','scurvey Letter some truth Female','He reports a damaging letter concerning a woman surfaced.','No letter copy, authentication or third-party provenance given.'),
 ('authorial_outcome_claim','dasht good Mans hopes','Lilly says the letter ruined the desired appointment.','Retrospective authorial success story; not independent proof.'),
 ('authorial_outcome_claim','and exit','The author reports the man left without the expected benefice.','No separately verified outcome record.'),
 ('authorial_characterization','querent Saturn Mars had wit','He describes the applicant as witty and talkative through a Saturn/Mars analogy.','Symbolic personality impression, not blinded behavioral evidence.'))
add([472],'Unidentified informer and highly conditional speculative suspect',
 ('authorial_uncertainty','could never discover neighbour','Lilly admits the man never discovered which neighbor had worked against him.','The alleged specific culprit was not identified.'),
 ('condition','Mercury under Earth Moon twelfth','The author invokes Mercury below the horizon and Moon in twelfth to account for secrecy.','Printed grammar has referent ambiguity; retain uncertainty.'),
 ('hypothetical_inference','if asked Saturn Lord twelfth','Lilly suggests what he would have inferred if asked about the unknown informer.','Counterfactual later extension, NOT a past correct forecast.'),
 ('hypothetical_inference','Farmer dealer in Cattle','The hypothetical culprit is described as a farmer or cattle trader.','Unsupported post-hoc characterization.'),
 ('hypothetical_inference','North east fifteen Furlongs','The hypothetical culprit is located northeast about fifteen furlongs.','No identified person or independent distance verification.'),
 ('hypothetical_inference','covetous repining Miller Sickly','He conjectures a resentful miller with poor health and other qualities.','Speculative descriptors, not independent evidence.'))
add([473],'Separate following source boundary Chapter LXXX',
 ('next_navigation','Chap LXXX Presbytery','The next chapter asks whether Presbytery shall endure.','Original PDF473 begins distinct political/religious case.'),
 ('next_navigation','11 March 1646 over 7 4:45 PM','The following circular figure prints 11 March 1646/7 at 4:45 PM; the original divides the year over two lines.','Do not import that chart into parsonage case.'))
assert len(SPANS)==7
assert all(r['chapter']=='LXXIX' for r in ROWS[:-2])
assert all(r['chapter']=='LXXX_NAVIGATION_ONLY' for r in ROWS[-2:])
assert [r['source_local_id'] for r in ROWS]==[f'LXXIX-C{i:03}' for i in range(1,len(ROWS)+1)]
def dump(n,j):(B/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
full='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
im=[]
for n in (471,472,473):
    f=B/'evidence'/f'pdf_1647-{n}.jpg';raw=f.read_bytes()
    im.append({'original_pdf_page':n,'printed_page':n-34,
      'path':f.relative_to(B).as_posix(),'bytes':len(raw),
      'sha256':hashlib.sha256(raw).hexdigest()})
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{'batch':'B03y','status':'ORIGINAL_SOURCE_FIRST_NOT_CANONICAL',
 'source_units':len(ROWS),'original_full_pdf_sha256':full,'rows':ROWS})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{'batch':'B03y','span_count':len(SPANS),
 'source_spans':SPANS,'mapped_source_units':len(ROWS),'original_body_pdf_pages':[471,472],
 'next_heading_pdf':473,'independent_diplomatic_second_transcription':False})
dump('SOURCE_WINDOW_MANIFEST.json',{'batch':'B03y','original_full_pdf_sha256':full,
 'original_images':im,'original_body_pdf_pages':[471,472],'following_heading_pdf':473,
 'previous_accepted_lilly':4508,'next_numbered_chapter':'LXXX',
 'chapter_begin':'Original PDF471/printed437 BELOW LXXVIII divider',
 'chapter_end':'Original PDF472/printed438 through last paragraph',
 'independently_authenticated_parsonage_outcome':0})
issues=[
 'LXXIX original begins below LXXVIII divider on PDF471; same page has two distinct charts.',
 'The 6 August 1644 8:24 PM circular horoscope is source-authored, not independently re-cast.',
 'Printed date and calendar conventions, including the next chapter dual-year 1646/7 notation, not independently resolved.',
 'The querent identity and parsonage application have no independent case records.',
 'Jupiter ninth, Mars first and Saturn ascendant require independent chart/method verification to test.',
 'Six numbered adverse conditions are distinct and not a statistical predictive system.',
 'Absence of applying aspect, translation, collection and reception are not interchangeable.',
 'The text contains competing Mercury/neighbors and Venus/women causal possibilities.',
 'The third-house Mercury opponent archetype is not a uniquely identified person.',
 'The author characterizes the querent as covetous, quick-witted and talkative; no blind assessment.',
 'The reported letter has no copy or external witness; do not count as independently verified prediction.',
 'The source says the informer was unknown even to querent, undermining identification claims.',
 'The farmer/miller/northeast fifteen furlong culprit is a counterfactual suggestion made after the case, not a tested prediction.',
 'The Mercury below earth / Moon twelfth secrecy sentence has ambiguities and no independent confirmatory measurement.',
 'The following Chapter LXXX begins PDF473 with new 1646 horoscope, excluded from LXXIX.',
 'No preregistered forecast, contemporaneous documented advice, prospective outcome follow-up, or independent verification.',
 'No runtime model/promoted empirical rule claims follow from this historical source.'
]
dump('UNRESOLVED_SOURCE_LIMITS.json',{'batch':'B03y','issues':[{'id':f'B03y-U{i:02}','issue':x} for i,x in enumerate(issues,1)]})
dump('CLAIM_LEDGER.json',{'batch':'B03y','status':'PROVISIONAL_ORIGINAL_SOURCE',
 'source_annotations':len(ROWS),'source_passages':len(SPANS),
 'retained_limitations':len(issues),'prior_lilly':4508,
 'new_accepted':0,'source_author_self_reported_failure_outcome':1,
 'independent_predictions_validated':0,'independent_authenticated_outcomes':0,
 'runtime_promotions':0})
print(json.dumps({'batch':'B03y','source_annotations':len(ROWS),'spans':len(SPANS),
 'issues':len(issues),'body_pdf_pages':[471,472],
 'next_chapter':'LXXX','next_pdf':473}))
