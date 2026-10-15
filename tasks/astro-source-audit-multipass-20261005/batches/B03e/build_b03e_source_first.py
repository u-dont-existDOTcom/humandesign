#!/usr/bin/env python3
"""1647 Lilly, Book II, Chapter LIX: source-first historical worked horoscope.
Historical author narrative including retrospective case account NOT blinded prediction.
Graphic planetary degrees are image authority, not guessed ephemeris outputs.
"""
import json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
rows=[];spans=[]
def segment(pages,label,*assertions):
 sid=f'LIX-S{len(spans)+1:03}';ids=[]
 for role,anchor,sense,limits in assertions:
  rid=f'LIX-C{len(rows)+1:03}';ids.append(rid)
  rows.append({'source_local_id':rid,'global_record_number':None,
   'batch':'B03e','book':'II',
   'chapter':'LIX' if role!='next_heading_boundary' else 'LX_HEADING_ONLY',
   'role':role,'original_pdf_pages':list(pages),
   'printed_pages':[x-34 for x in pages],
   'source_short_anchor_not_diplomatic':anchor,
   'historical_author_report_paraphrase':sense,
   'conditions_source_limits_or_chronology':limits,
   'original_scan_is_authority':True,
   'is_independently_blinded_case':False,
   'complete_diplomatic_second_transcription':False,
   'historical_documentation_admitted':False,
   'real_outcome_independently_authenticated':False,
   'empirical_astrology_prediction_validated':False,
   'runtime_model_promoted':False})
 spans.append({'span_id':sid,'original_pdf_pages':list(pages),
  'printed_pages':[x-34 for x in pages],
  'source_label_not_verbatim_transcription':label,
  'mapped_source_local_ids':ids})
segment([419],"chapter LIX heading original divider",
 ("heading","Chap. LIX. A Lady, if marry the Gentleman desired?",
  "This is a worked marriage question, not a fresh general-purpose marriage rule.",
  "Chapter LIX begins beneath Chapter LVIII divider on PDF419 printed385."))
segment([419],"original dated square horoscope figure",
 ("figure","square horoscope drawing, 16 June 1646",
  "The source supplies an original square horoscope and angular house divisions with zodiac and planetary glyphs.",
  "The diagram, not a synthetic ephemeris, is the authority for degree and house readings."),
 ("source_date","16 June 1646, 19:26? P.M. / Hor: astr. Saturn",
  "The center appears to date the figure 16 June 1646 at a written time around 19:26 P.M., with hour-lord annotation.",
  "Exact numerical glyphs and minute convention not adjudicated from one original image; do not compute modern UTC or infer locality."),
 ("graphic_ambiguity","radix/cusp planet glyphs and numbers",
  "Planet symbols, house-cusp signs, degrees, minutes and central aspects are handwritten/printed in the figure.",
  "Do NOT turn manually uncertain symbols and unclear rotated numerals into exact chart coordinates."))
segment([419],"heading below figure",
 ("subheading","Judgment upon the Figure above-said",
  "An explicit subheading introduces Lilly's textual interpretation of the printed chart.",
  "The chart's caption belongs to Chapter LIX and is a source marker."))
segment([419,420],"narrative pre-question history and changed affection",
 ("historical_case_claim","Gentleman ... long time earnest Suitor",
  "Lilly reports that a gentleman had long sought a marriage with the woman.",
  "One retrospective account, not a blinded independent participant."),
 ("historical_case_claim","she ... slighted him continually ... absolute denial",
  "The woman's repeated refusal is described as past history.",
  "Author's post hoc summary; separate from consultation-time predictions."),
 ("historical_case_claim","After which denial ... passionately affectionate",
  "He reports that the woman afterward developed strong affection and regretted the refusal.",
  "Source narrative crosses PDF419 to PDF420 and is not prospective prediction evidence."))
segment([420],"assignment of querent and object of desire",
 ("assignment","ascendant and Sun are for the querent",
  "The ascendant and Sun are assigned as significators of the questioner.",
  "Chart-specific rule; do not mechanically use this same significator in all questions."),
 ("assignment","Saturn Lord of the seventh ... man quesited after",
  "Saturn, as seventh-house lord, is assigned to the gentleman.",
  "Distinguish significant Saturn from other chart planets."))
segment([420],"woman appearance and dignity interpretation",
 ("historical_case_claim","querent ... moderately tall ... round visage ... gray eyed",
  "The author describes the female querent's reported appearance.",
  "No independent verification of the woman's identity or appearance."),
 ("author_inference","Sun Lord of the ascendant in the Terms of Mars",
  "The author offers planetary dignity terminology as his explanation for some physical traits.",
  "Not validated physical-personality inference; exact sign degree remains original image-dependent."))
segment([420],"gentleman's appearance and conceded claim",
 ("author_inference","Saturn in the angle of the South ... with Mars ... both Taurus",
  "Lilly links his description of the man to Saturn, its placement and contact with Mars.",
  "Source scope and aspect notation preserved, no numerical chart reconstruction."),
 ("historical_case_claim","corporeture ... meane ... wan pale ... dark haires",
  "He reports a detailed inferred physical description of the gentleman, including demeanor and gait.",
  "Original source contains physical descriptors, not verified modern phenotyping."),
 ("claimed_confirmation","[this was confessed.]",
  "The printed bracket claims the physical description was confirmed by an informant.",
  "Internal author confirmation, not independent case evidence."))
segment([420],"inferred gentleman's distress and interposed relative",
 ("author_inference","Saturn elevated ... conjunct Mars ... sad, angry",
  "Lilly infers the gentleman's unhappiness and frustration from Saturn/Mars.",
  "Private emotional/intent claims unverified."),
 ("author_inference","Mars ... Lord of the third ... kinsman ... near one another",
  "He infers another male relative or gentleman nearby and a possible neighborhood connection.",
  "Source says an additional gentleman was significant; actor and relation partly ambiguous."),
 ("claimed_confirmation","[and so it was.]",
  "A second bracketed confirmation appears for the author's conjecture.",
  "Not a blind independent verification."))
segment([420],"unfavorable inclination plus Moon transition",
 ("author_inference","Gentleman had no inclination or disposition unto her",
  "The author initially judges the man to lack marriage interest in the woman.",
  "Untested mind-state allegation, not an observed interview with the gentleman."),
 ("condition","Moon separated from voyd of course ... applying to opposition of Sun",
  "The Moon's separation and applying opposition to the first lord are cited as unfavorable conditions.",
  "The original 'separated from voyd of course' phrasing is grammatically difficult; keep source-native."),
 ("historical_prognosis","small hopes of effecting her desire",
  "Lilly says the initial configuration made successful marriage seem unlikely.",
  "Chronology is author-retold, not time-stamped independently frozen prediction."))
segment([420],"questioner discloses details after an initially adverse reading",
 ("historical_case_claim","told me the truth of all, and not before",
  "The woman allegedly disclosed additional relevant facts only after the initial assessment.",
  "This is information contamination within the case, not a prospective blinded test."),
 ("historical_case_claim","implored my directions ... without scandall ... on againe",
  "The questioner asked for concrete help to revive the relationship without public scandal.",
  "Author may have influenced the later outcome; no causal isolation."))
segment([420,421],"Sun to Saturn sextile and initial lack of reception",
 ("condition","Sun applying to sextile of Saturn",
  "The author observes an applying sextile between the Sun and Saturn.",
  "Distinct from the separate reception and intermediary conditions."),
 ("author_inference","woman's desire ... strong affection",
  "He interprets the Sun-to-Saturn aspect as her desire.",
  "One-sided, not direct proof of the man's wishes."),
 ("exception","no Reception betwixt the significators",
  "The lack of reception between the principal significators is an explicit weakening qualification.",
  "Do not turn sextile without reception into certain marriage."))
segment([421],"favorable secondary reception and Moon dispositor",
 ("condition","Reception betwixt Jupiter and Moon, and Sun and Moon",
  "The author contrasts the weak primary condition with receptions involving Jupiter, Moon and Sun.",
  "Identity/direction of each reception relies on exact source wording; no invented algorithm."),
 ("condition","Moon disposed of Saturn in her Exaltation and Jupiter in her House",
  "The printed source invokes Moon's reception/dignity relations to Saturn and Jupiter.",
  "Original technical terms and polarity retained without reconstructing exact degrees."))
segment([421],"Jupiter applying sextile Saturn and mitigation",
 ("condition","Jupiter very near a dexter sextile of Saturn, still applying",
  "Jupiter is said to be very near an applying sextile to Saturn.",
  "Handwritten diagram and prose might differ in exact degrees; no synthetic certainty."),
 ("condition","Jupiter in his Exaltation ... qualifies Saturn",
  "Jupiter's exaltation and fortunate character are described as mitigating Saturn.",
  "Author's evaluative view only, not empirical magnitude."))
segment([421],"person of quality selected as intermediary",
 ("author_inference","quesited ... acquainted with a person of quality ... Jupiter represented",
  "Lilly conjectures that the gentleman knew an influential person symbolized by Jupiter.",
  "The third-party's actual influence is an authorial inference."),
 ("claimed_confirmation","whom I exactly described, and Lady very well knew",
  "He reports that the woman recognized the person described.",
  "Self-reported source agreement, not blinding."),
 ("historical_intervention","directed to addresse her Complaints ... acquaint him",
  "He advised approaching the influential person and explaining her regrets.",
  "An active social intervention that could change the outcome independently of astrology."))
segment([421],"author forecasts resolution and date windows",
 ("historical_prognosis","would ... revive the businesse and bring her to her hearts content",
  "The author reports predicting the intermediary would revive the match.",
  "The outcome may depend on the advised intervention; prediction not independently frozen."),
 ("historical_intervention","Sun and Saturn come to sextile ... 27th same moneth",
  "He directed that matters move before the Sun-Saturn sextile of 27 June.",
  "Date belongs to author narrative; exact astronomical timing unverified."),
 ("historical_intervention","nineteenth of June near upon noon ... should first move",
  "The proposed initial approach was 19 June around noon.",
  "Specific proposed social action; no independently verified record the action occurred at this time."),
 ("condition","Saturn and Jupiter in a perfect sextile ... that day",
  "He associates 19 June with a claimed Saturn-Jupiter sextile.",
  "A distinct claimed time aspect, not a fresh calculated event."))
segment([421],"reported actual outcome, source-internal",
 ("historical_case_outcome","counsell was followed ... Match effected ... within twenty dayes",
  "Lilly says the intermediary was consulted and the marriage match occurred within twenty days.",
  "Historical report from the same source; no independent court/parish marriage documentation."),
 ("limitation","sorrowfull (but as to me unthankfull) Lady",
  "The report includes the author's emotionally colored description of the woman.",
  "Potential retrospective bias and adversarial framing; not an objective case datum."))
segment([421,422],"author's explanation: first/seventh aspect and Moon/first opposition",
 ("author_inference","application of two Significators to sextile ... seventh and first",
  "He later frames the applying sextile between first/seventh lords as part of the account.",
  "Post-outcome astrological explanation, not untouched prediction."),
 ("author_inference","application of Moon to Lord ascendant ... opposition yet with Reception",
  "Moon applying in opposition with reception is reported as a secondary positive factor.",
  "Original opposition/reception exception prevents trivial positive/negative polarity."),
 ("author_inference","main occasion ... application of Jupiter to sextile of Saturn",
  "He explicitly identifies the Jupiter-Saturn sextile as the principal explanatory factor.",
  "Claim of necessity is retrospective author's explanation, not tested causality."))
segment([421,422],"translation process culminating in Jupiter Sun conjunction",
 ("author_inference","Jupiter receiving his vertue which Saturn did render unto him",
  "Lilly describes Jupiter receiving Saturn's virtue and transferring it toward Sun.",
  "No separate astrological mechanism independently validated."),
 ("condition","no Prohibition, Abscission or Frustration",
  "He states the transfer was not obstructed by prohibition, abscission or frustration.",
  "Exact original definitions not supplied here; do not invent.")
)
segment([422],"subsequent Jupiter/Sun timing and potential rival proposed match",
 ("condition","perfect conjunction of Jupiter with Sun ... 29 June",
  "The Jupiter-Sun conjunction is dated 29 June in the author's account.",
  "Keep distinct from June 19 and 27 dates and image chart time."),
 ("historical_case_claim","Sweet-heart ... offered a Match ... Gentlwoman ... Venus",
  "He reports that the desired gentleman was offered another marriage candidate, represented by Venus.",
  "Second-hand story with potentially sensitive third-party information; not independently authenticated."),
 ("author_inference","Mars nearer Venus than Saturn ... interposed",
  "He reasons that Mars's relation to Venus blocked the alternative match.",
  "Retrospective selection; original symbol/aspect details preserved but not recalculated."),
 ("claimed_confirmation","Lady well knew both ... matters then in action",
  "He reports the woman confirmed knowledge of both the man and the other proposed bride.",
  "Case-source confirmation rather than independent observation."))
segment([422],"counterfactual: survival duration",
 ("counterfactual","Had the Quere been Who should have lived longest",
  "The author offers a hypothetical answer about which person would live longer.",
  "Never an observed outcome; should not count as a correct death/longevity prediction."),
 ("author_inference","I should have judged the woman ... Sun to Jupiter ... Mars afflicts Saturn",
  "He bases the hypothetical on different planetary indications.",
  "Not a validated medical/longevity statement."))
segment([422],"counterfactual: wealth",
 ("counterfactual","Had she demanded whether Quesited rich",
  "He considers a hypothetical question about the man's wealth.",
  "This is not the question actually asked."),
 ("author_inference","Jupiter Lord of his second ... Exaltation, Direct, Swift ... Sun beames",
  "He argues that Jupiter's dignities imply considerable wealth despite solar proximity.",
  "Original technical source claim with no wealth evidence."))
segment([422],"counterfactual agreement and jealousy assumptions",
 ("counterfactual","For Agreement ... Sun and Saturn applying sextile",
  "He speculates about long-term agreement using the same Sun-Saturn sextile.",
  "No independently observed marriage longevity or satisfaction outcome."),
 ("author_inference","Saturn jealous without cause ... Jupiter ... represses",
  "The author makes personal temperament and jealousy allegations, partially mitigated by Jupiter.",
  "Speculative character inference, not an assessment of real marital safety."))
segment([422],"counterfactual woman honesty",
 ("counterfactual","Will querent be honest?",
  "He raises a separate hypothetical question about the woman's virtue.",
  "Not an independent validated question."),
 ("historical_allegation","Sun not afflicted ... Leo ... reception ... vertuous woman",
  "He asserts positive morality based on the woman's significator, rising sign and reception.",
  "Historical moral characterization, not a verified personal trait."))
segment([422],"closing general applicability and next chapter transition",
 ("scope","In this nature may you examine any Figure",
  "The author ends by suggesting the method can be applied to similar figures.",
  "General author's assertion, not validated external transferability."))
segment([423],"Chapter LX starts original next page with DIFFERENT chart",
 ("next_heading_boundary","Chap. LX. If she should marry the man desired?",
  "The next numbered Chapter LX opens on PDF423/printed389 with a different dated 11 June 1646 chart.",
  "Navigation marker only; never combine the two cases or chart timings."))
assert [r['source_local_id'] for r in rows]==[f'LIX-C{i:03}' for i in range(1,len(rows)+1)]
assert [s['span_id'] for s in spans]==[f'LIX-S{i:03}' for i in range(1,len(spans)+1)]
assert [s['original_pdf_pages'][0] for s in spans]==sorted(s['original_pdf_pages'][0] for s in spans)
assert rows[-1]['role']=='next_heading_boundary'
def dump(f,obj):(P/f).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
images=[]
for pg in range(419,424):
 p=P/'evidence'/f'pdf_1647-{pg}.jpg';b=p.read_bytes()
 images.append({'pdf_page':pg,'printed_page':pg-34,
 'path':p.relative_to(P).as_posix(),
 'size_bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{'batch':'B03e','status':'PROVISIONAL_SOURCE_FIRST',
 'source_original_pdf_sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b',
 'source_units':len(rows),'original_case_independently_authenticated':False,'rows':rows})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{'batch':'B03e','status':'PROVISIONAL',
 'source_spans':spans,'span_count':len(spans),'mapped_source_units':len(rows),
 'source_window':'PDF419 lower below LVIII divider through PDF422 entire body and PDF423 heading only',
 'empirically_validated_predictions':0})
dump('SOURCE_WINDOW_MANIFEST.json',{'batch':'B03e','status':'PROVISIONAL',
 'source_full_pdf_sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b',
 'source_body_pdf_pages':[419,420,421,422],
 'next_header_pdf_page':423,'previous_accepted_lilly':3360,
 'opening':'PDF419 below LVIII divider; historical marriage chart 16 June 1646',
 'closing':'PDF422 ends Chapter LIX; PDF423 opens Chapter LX different dated chart',
 'images':images,'complete_independent_diplomatic_second_reading':False})
dump('SOURCE_ORDER_DRAFT.json',{'batch':'B03e','status':'PROVISIONAL',
 'ordered_local_ids':[r['source_local_id'] for r in rows],
 'cross_page_ids':[r['source_local_id'] for r in rows if len(r['original_pdf_pages'])>1],
 'next_heading_only':rows[-1]['source_local_id']})
dump('UNRESOLVED_SOURCE_LIMITS.json',{'batch':'B03e','status':'RETAIN_UNRESOLVED',
 'issues':[
 {'id':'B03e-U01','source':'PDF419','note':'The original diagram is authoritative; rotated degree glyphs and exact chart time convention not fully read. No synthetic ephemeris asserted.'},
 {'id':'B03e-U02','source':'PDF419/423','note':'LIX 16 June 1646 chart and LX 11 June 1646 chart are separate cases; never transfer data.'},
 {'id':'B03e-U03','source':'PDF419-420','note':'Pre-question romance narrative is retrospection not prediction.'},
 {'id':'B03e-U04','source':'PDF420','note':'Author gendered physical and temperament descriptions have only source-internal bracketed confirmation.'},
 {'id':'B03e-U05','source':'PDF420','note':'Secret male acquaintances and house-distance claims partly inferred; no independent identification.'},
 {'id':'B03e-U06','source':'PDF420','note':'Moon "separated from voyd of course" syntax and negative prognosis unresolved.'},
 {'id':'B03e-U07','source':'PDF420','note':'The author reports woman revealed facts after his initial negative reading, introducing possible feedback/contamination.'},
 {'id':'B03e-U08','source':'PDF420-421','note':'Sun sextile Saturn with NO reception initially yields weak hopes; do not report unconditional yes.'},
 {'id':'B03e-U09','source':'PDF421','note':'Jupiter-Moon, Sun-Moon receptions and Moon disposing of Saturn use source-specific technical language.'},
 {'id':'B03e-U10','source':'PDF421','note':'Jupiter sextile Saturn near applying and "qualifying malice" are source explanations not measured effects.'},
 {'id':'B03e-U11','source':'PDF421','note':'Advice to contact intermediary was an active intervention; self-reported successful match does not isolate horoscope impact.'},
 {'id':'B03e-U12','source':'PDF421-422','note':'June 19, June 27 and June 29 event/aspect dates must not be conflated or recalc as independently verified.'},
 {'id':'B03e-U13','source':'PDF421','note':'"Within twenty days" outcome source-internal with no independently located 1646 marriage record.'},
 {'id':'B03e-U14','source':'PDF421-422','note':'Astrological translation-of-light mechanism explained after outcome, not registered beforehand.'},
 {'id':'B03e-U15','source':'PDF422','note':'Rival Venus marriage, Mars interposition, family wealth and jealousy are source conjectures about third parties.'},
 {'id':'B03e-U16','source':'PDF422','note':'Who lives longest, who rich, whether they agree and honest are counterfactual question digressions, not observed validation.'},
 {'id':'B03e-U17','source':'PDF423','note':'Chapter LX begins with different diagram; only next heading included in LIX navigation.'},
 {'id':'B03e-U18','source':'PDF419-423','note':'No independent case archival attestation, full blind diplomatic transcription, measured predictive accuracy or live rule promotion.'}]})
dump('CLAIM_LEDGER.json',{'batch':'B03e','status':'PROVISIONAL_SOURCE_CASE_ONLY',
 'source_first_units':len(rows),'original_visual_spans':len(spans),
 'previous_accepted_lilly':3360,'new_globally_accepted':0,
 'independently_confirmed_1646_marriage':0,
 'frozen_pre_outcome_horoscope_forecasts':0,
 'new_empirical_predictions_validated':0,'runtime_model_promotions':0})
print({'batch':'B03e','source_records_draft':len(rows),'source_spans':len(spans),
 'original_body_pages':[419,420,421,422],'next_chapter_header':423,'empirical':0})
