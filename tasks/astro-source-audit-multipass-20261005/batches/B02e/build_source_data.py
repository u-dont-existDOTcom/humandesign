"""Source-preserving extraction of Lilly 1647 II.XXII-XXIII. Not prediction code."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SID='LILLY1647_WELLCOME_B30338724'
SHA='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
RECORDS=[]

def rec(title,pages,statement,prerequisites=(),limits=(),section='XXII',kind='conditional_source_rule'):
    n=568+len(RECORDS)
    RECORDS.append({'id':f'LI.1647.II.{section}.R{n}','title':title,'kind':kind,
      'source_locator':{'source_id':SID,'source_sha256':SHA,'book':'II','section_key':'II.'+section,'pdf_pages':list(pages),'printed_page_positions':[p-34 for p in pages]},
      'statement_type':'editor_normalized_paraphrase','source_statement':statement,
      'prerequisites':list(prerequisites),'qualifications_and_limits':list(limits),
      'runtime_status':'REFERENCE_ONLY_NOT_PROMOTED','independent_evidence_unit':False})

def save(name,obj):
    (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

rec('Unknown birth time motivates a question, not a repaired nativity',[163],
 'Lilly introduces questions about longevity, approaching illness and happiest life periods for people without a remembered or obtainable nativity.',
 limits=['A horary question is not a natal chart with an estimated birth time. Historical use is not evidence of clinical accuracy.'],kind='scope')
rec('Health and life testimonies require three significators',[163,164],
 'Consider the rising sign, its lord and Moon free of misfortune. The lord is free of solar combustion and square/opposition/conjunction of rulers of houses 8,12,6,4; consider direction, essential dignity, speed, angularity and placement, good aspects and benefic terms.',
 limits=['The prose mixes AND and OR; its whole Boolean aggregation is not resolved into an automatic diagnosis.'],kind='conditional_testimony_set')
rec('Preferred locations and helpful testimony',[164],
 {'preferred_locations':['first particularly','tenth','eleventh','ninth'], 'helpful':['good aspect Jupiter, Venus or Sun','terms of Jupiter and Venus']},
 ['Question concerns life/health; the planet is the Ascendant lord.'],['Do not equate natural planet quality with functional house rulership.'],kind='reference_group')
rec('Contrary testimony and aspecting planet roles',[164],
 'An unfortunate Ascendant or its lord, or an afflicted Moon in bad houses, signifies mischief at hand; freedom from these argues otherwise. Examine aspects to the Ascendant itself and the houses ruled by their casting planets.',
 limits=['Mischief is not automatically death. Apply the later explicit outcome distinctions.'])
rec('Adverse solar and lunar conditions',[164],
 'Generally received adverse conditions include Ascendant lord under beams or approaching combustion (worse than departing), or cadent Moon afflicted by sixth/eighth-house rulers, with the following angular and stellar qualifications.',
 limits=['Preserve source conjunctions; do not detach a single condition from the caution on p132.'])
rec('Angular afflictors and fixed-star qualifications',[164],
 'The South Node, Saturn or Mars in Ascendant or seventh, peregrine, in detriment or retrograde, and violent fixed stars at the rising degree, Ascendant-lord degree, Moon or afflicting planet are examined. Stellar natures may match the afflictor or sixth/eighth ruler.',
 limits=['Scope of the combined AND/OR list is unresolved; retrograde/detriment language is not astronomical motion for the node. No fixed-star orb is supplied.'])
rec('Adverse result is disjunctive and topic-dependent',[164],
 'The stated adverse result may be short life, proximity to danger, or another misfortune according to significator quality and ruled houses.',
 limits=['Do not score these alternatives as three independent correct predictions.'])
rec('First timing route and explicitly general scale',[164,165],
 {'route':'Ascendant lord approaching combustion or opposition/conjunction of eighth/fourth ruler; inspect degrees to the contact and signs.',
  'eight_degree_example':{'common':'eight months','fixed':'eight years','moveable':'eight weeks'}},
 limits=['The next page expressly says this is example and general only; other concurring significators limit the measure. Not a universal sign-to-time law.'],kind='method_and_example')
rec('Second timing route',[165],
 'Also inspect Moon distance from an infortune or sixth/eighth lord, with the signs, their qualities and houses.',
 limits=['No unique weighting or reconciliation with the first route is supplied.'])
rec('Third timing route',[165],
 'For an infortune in the Ascendant, consider distance between cusp and planet; for one in the seventh, distance of Ascendant to its true opposition. Relate timing to moveable/common/fixed signs.',
 limits=['This is not a modern transit or primary-direction engine; no unique frame for every geometry is supplied.'])
rec('Sixth-house outcome branch',[165],
 'When sixth lord chiefly afflicts the Ascendant lord in the sixth, or the latter approaches combustion there, Lilly describes many persistent illnesses. Ascendant lord, eighth lord and Moon together in sixth intensify that claim.',
 limits=['Historical assertion only; not clinical prognosis or treatment advice.'])
rec('Eighth-house outcome branch',[165],
 'Chief affliction of Ascendant lord, rising sign or Moon by eighth lord or a planet afflicting from eighth is related to a present or approaching illness ending life, approaching death or threatened death.',
 limits=['Preserve the alternative threatened wording and subsequent caution; not a personal forecast.'])
rec('Other-house misfortune is explicitly not death',[165],
 'When other house lords chiefly afflict these significators, judge the misfortune from the houses they rule, and its first origin or discovery from what belongs to the house occupied by the afflictor; in this case judge misfortune, not death.',
 limits=['Ruled house and occupied house have distinct explanatory jobs.'])
STAR_SPECTRA={
 'Mars':['sudden bodily disorders','fevers','murders','quarrels'],
 'Saturn':['quartan agues','poverty','accidental injury from falls'],
 'Mercury':['consumptions','madness','deception through false evidence or writings'],
 'Moon':['tumults','commotions','wind-colic','danger through water'],
 'Sun':['envy of magistrates','eye injuries'],
 'Jupiter':['oppression by domineering priests or a gentleman'],
 'Venus':['injury through a woman','pox','cards','dice','wantonness']}
for planet,items in STAR_SPECTRA.items():
 rec('Fixed-star nature catalogue: '+planet,[165,166],items,
 ['The earlier relevant fixed-star/affliction procedure, not any appearance of this planet.'],
 ['Historical catalogue, not modern medical, criminal or demographic inference; open examples, not independent outcomes.'],kind='historical_catalogue')
rec('No death judgment from one testimony',[166],
 'Avoid pronouncing death rashly or on one single testimony; check if Jupiter or Venus sextile/trine the Ascendant lord before perfect combustion or another infortune.',
 limits=['The source explains help as medicine or natural strength opposing or partially removing misfortune. It does not supply a validated protection effect.'])
rec('More testimony does not remove date caution',[166],
 'Two or more preceding rules concurring toward death may warrant more boldness for Lilly, but he says he has been wary of and largely refrained from the absolute time of death.',
 limits=['Do not transform two rules into calibrated probability, empirical independence or a licensed date-of-death forecast.'])
rec('Claimed practical uses and author experience',[166],
 'Lilly reports many verified examples and mentions life leases/offices and prevention of casualties as useful applications.',
 limits=['Author-reported experience, not data independently acquired for this project; not current financial or health advice.'],kind='author_claim')
QUARTERS=[
 {'origin_cusp':1,'end_cusp':10,'houses':[12,11,10],'direction':'East inclining South'},
 {'origin_cusp':10,'end_cusp':7,'houses':[9,8,7],'direction':'South verging West'},
 {'origin_cusp':7,'end_cusp':4,'houses':[6,5,4],'direction':'West tending North'},
 {'origin_cusp':4,'end_cusp':1,'houses':[3,2,1],'direction':'North inclining East'}]
for q in QUARTERS:
 rec('Directional quadrant from cusp '+str(q['origin_cusp']),[166,167],q,
 limits=['Cusps and declining house sequence as stated; not an azimuth or an astrocartographic relocation algorithm.'],kind='table_row')
rec('Choosing a direction requires a relevant promising planet',[167],
 'Find the most promising planet and Jupiter, Venus, Moon or Fortune, especially two or more together; a Moon and Fortune free of combustion and other misfortunes direct the inquiry to the Moon quadrant.',
 limits=['Source literal Fortune/Moon selection retained; pronoun and weighting not forced into a universal Boolean formula.'])
rec('Benefics can function adversely and malefics favourably',[167],
 'Jupiter/Venus ruling eighth, twelfth or sixth can accidentally be infortunes, so their quarter is avoided in this setting; attend instead to Fortune, Moon and Ascendant lord. Mars/Saturn ruling first, second, tenth or eleventh can be friendly when essentially strong.',
 limits=['Source says can for the latter; strength and topical relevance both matter. Later case uses eighth-ruler Jupiter favourably, so this is not an unconditional veto.'])
rec('Health direction and wealth direction are different inquiries',[167],
 {'health':'Ascendant lord and Moon, their sign/quadrant, comparative strength and friendlier aspect to Ascendant degree.',
  'estate':'Second lord, Fortune and its dispositor, or two of them, in their best-fortified quadrant.'},
 limits=['Separate topical starting points; no modern treatment/travel/investment recommendation.'],kind='methodology')
rec('Life-house scale and its explicit flexibility',[168],
 'Usually five years per house, beginning twelfth then eleventh, tenth down to Ascendant; sometimes more or less according to testimonies of life or death. If life significators are very strong and indicate long life, one year may be added to each house.',
 limits=['The chapter supplies a conditional six-year alternative, not automatic selection from a known age or outcome. Neither setting is a calibrated lifespan estimate.'])
AGE_EXAMPLES=[([11,10],5,15),([8,7],20,30),([6,5,4],30,45),([3,2,1],45,60)]
for hs,a,b in AGE_EXAMPLES:
 rec('Reported favourable age group '+str(hs),[168],{'houses':hs,'years':[a,b],'planets':'Jupiter or Venus'},
 ['Fortunate/promising planets in this inquiry.'],['Rounded source ranges; endpoint inclusion is not prescribed.'],kind='worked_group')
rec('Past versus future requires separation versus application',[168],
 'At question time, Ascendant lord and Moon separations indicate preceding events; next applications indicate future events. Aspect quality, ruled house, condition and position identify matter, person, quality, extent and timing.',
 limits=['No outcome data used to select an application; a complete astronomical contact-history computation is not supplied here.'])
CASE={
 'source_pages':[169,170,171,172,173,174,175,176,177,178,180],
 'identity':'Anonymous historical querent; no attempted identity resolution',
 'printed_heading':{'year':'1632','day_raw':'24.14. martij','time_raw':'2h 15m P.M.','calendar_resolution':'UNRESOLVED; no UTC conversion or ephemeris parity asserted'},
 'verified_positions':{'Ascendant':['Leo',23,27],'Sun':['Aries',4,18],'Moon':['Virgo',21,18],
 'Mercury':['Pisces',14,57],'Mars':['Pisces',28,40],'Jupiter':['Taurus',24,24],
 'Venus':['Taurus',16,7],'Fortune':['Aquarius',10,27],'ninth_cusp':['Aries',2,8]},
 'source_rulerships':{'Sun':[1],'Moon':[],'Mercury':[2,11],'Venus':[10],'Mars':[4], 'Jupiter':[5,8],'Saturn':[6,7]},
 'source_occupied_houses':{'Sun':9,'Moon':2,'Mercury':8,'Mars':8,'Jupiter':10,'Venus':10},
 'limits':['Selected image/prose-verified fields only, not a complete reconstructed chart.',
 'House/rulership values here are the author-used roles, not independently regenerated from a full cusp table.',
 'Retrospective source narrative and reported confirmations, not prospectively frozen project evidence.']}
rec('Historical question chart and six inquiries',[169],
 {'chart_data':'CASE_REFERENCE.json','questions':['longevity','best direction','happiest age','preceding events','future events','timing']},
 limits=CASE['limits'],kind='source_case')
rec('Case bodily appearance and fixed-star attribution',[169,170],
 'Leo Ascendant, Cor Leonis at Leo24:34, Ascendant and Sun degrees in Jupiter terms, Moon trines to angular Jupiter/Venus: Lilly describes a comely medium strong body, fair face, reddish hair and right-cheek scars. He notes soldier status and attributes scars to the fixed star.',
 limits=['Physical observations and causal attribution are separate; profession is already known within the narrative.'],kind='case_interpretation')
rec('Case temperament has countervailing and educational qualifications',[170],
 'Fiery Ascendant and lord, hot/dry Sun and exaltation imply valour, choler and high spirit. Moon trines benefics qualify this as sober/modest, education as control over passion; Moon opposition Mercury adds episodes of anger/folly damaging affairs.',
 limits=['Do not retain only flattering character descriptors or relabel education as chart-derived evidence.'],kind='case_interpretation')
rec('Case life judgment and limited follow-up',[170],
 'Unvitiated Ascendant, exalted unimpeded swift Sun in ninth and Jupiter terms, Moon separating Venus trine and applying Jupiter trine with Jupiter intervening before Mars, Sun above earth, benefics angular and stronger than malefics: many years and few illnesses. Lilly reports the man still living in March1646.',
 limits=['Image confirms Jupiter terms; the existing text-layer glyph was ambiguous. Survival to stated follow-up is not completed lifespan validation.'],kind='case_interpretation_and_followup')
rec('Case direction combines quadrant with sign',[171],
 'Sun near ninth cusp and moveable Aries suggest sudden travel; southern quadrant plus eastern sign gives southeast from London. Sun-cusp separation is2:10 and departure is reported within two months.',
 limits=['Direction interpretation and actual reported departure are different evidence fields. Position is after the cusp; no invented forward-cusp contact time.'],kind='case_interpretation')
rec('Case country and within-country direction are separate levels',[171],
 'Aries countries are proposed; staying in England would favour its eastern/southeastern areas. When a sign-associated country lies in another compass direction, conduct affairs within the favourable part of that country; France southwest of London is illustrated with its east/southeast portion.',
 limits=['The country-association and direction criteria are not independent empirical corroboration; fallback scope must be declared before testing.'],kind='case_method')
rec('Ireland recommendation and claimed result',[171,172],
 'Applying Moon trine Jupiter and Jupiter/Venus in Taurus, assigned to Ireland, prompt recommendation of Ireland and honour because Jupiter is in tenth. Lilly reports good service and a notable victory without naming the man.',
 limits=['This uses Jupiter despite its eighth lordship; earlier accidental-infortune caution is not silently made absolute. Author-reported military success, not independently verified.'],kind='case_interpretation_and_followup')
rec('Case age overview and later support',[172],
 'Benefics tenth, node and Sun ninth give pleasant younger years; Mars eighth is related to troubles around age24–26. No fortunate planets in houses7 through3 imply later labour/trouble. Moon almost three degrees from Jupiter trine delays calamities for almost three years through a powerful helper; Jupiter essential strength would have made support more lasting.',
 limits=['The reported age24–26 overlaps beyond the default eighth-house20–25 band; no concealed choice of birthday boundary. Absent benefics is used negatively here by the author, not a universal inference rule.'],kind='case_interpretation')
rec('Historical Sun contacts locate preceding difficulties',[172,173],
 'Lilly directs the reader to that year ephemeris: Sun in Pisces had conjoined Mars, squared Saturn and sextiled Jupiter. Mars fourth lord in eighth plus Moon in second applying Mars opposition is read as disputes over lands or a woman/wife portion; the source reports confirmation.',
 limits=['Prior-ephemeris history is asserted by source, not astronomically recomputed in this batch. Future Moon application is also used in the retrospective interpretation; preserve that exposure.'],kind='case_interpretation_and_followup')
rec('Wife and estate interpretation has multiple specific roles',[173],
 'Sun square Saturn relates to marital variance. Saturn as wife significator disposing his Fortune suggests unwillingness to share her estate; retrograde superior Saturn in a fire sign and fixed seventh describe a strong, unsubmissive character. Source reports confirmation.',
 limits=['Do not infer relationship safety or moral character of a current person. Source terminology is historical.'],kind='case_interpretation_and_followup')
rec('Mediation, willingness and alternative obstacles',[173,174],
 'Sun sextile Jupiter in tenth is read as lawyer/courtier mediation; margin names Lord Coventry. Sun and Saturn applying trine suggest willingness to reconcile. Mercury square Saturn offers alternatives: lawyer/writings, second-lord money refusal or shortage, eleventh-lord false friend/lawyer, or eleventh as fifth from seventh a child of wife. Lilly believes every particular proved true. Venus tenth lord disposing eighth-lord Jupiter is read as entrusting her estate to a nobleman.',
 limits=['Alternatives remain alternatives, not precommitted separate hits. Belief that all proved true is author assertion, not an independent event ledger.'],kind='case_interpretation_and_followup')
rec('Unimpeded strong Sun and travel liberty',[174],
 'Strong Sun without harmful aspect suggests freedom to travel and change affairs, with moveable Aries on ninth; prosperity remains subject to the preceding limitations.',
 limits=['Source parenthesis says no aspect; earlier application Sun–Saturn is also reported. Preserve local scope tension, not universal unaspected-planet rule.'],kind='case_interpretation')
rec('Child education and wife revenue combine several houses',[174],
 'Moon in second applying to Jupiter tenth, ruler of fifth and eighth, is read as negotiation with a nobleman about child education paid from wife annual revenue. The author reports something of this kind was settled before departure.',
 limits=['This is one interdependent topical chain, not four independent matches. Outcome wording is broader than detailed interpretation.'],kind='case_interpretation_and_followup')
rec('Weakness does not erase a smaller dignity',[174,175],
 'Moon Virgo is called peregrine by day, unlike its night triplicity. Mercury Pisces is in detriment yet in its own terms, afflicted by Mars; Moon separated Mercury opposition by6:21 is interpreted as about six months and somewhat more of money shortage, reported confirmed.',
 limits=['The case has signs and topics different from the general units example. No universal past-timing unit inferred.'],kind='case_interpretation_and_example')
rec('One adverse contact is mapped to several dependent outcomes',[175],
 'Moon first reaches Jupiter trine, then Mars opposition before leaving Virgo: pleasure followed by danger to life (Mars eighth), goods (Moon second), lands/inheritance (Mars fourth lord in eighth).',
 limits=['Dependent threatened losses, not separately independent predictions; not all stated as completed events.'],kind='case_interpretation')
rec('Distinct timing layers in one historical chart',[175],
 {'Moon_to_Jupiter':'about three degrees means about three years of pleasure',
  'Sun_to_end_of_Aries':'about26 remaining degrees, one month each, means about26 months of freedom',
  'Moon_to_Mars':'28:40 minus21:18 gives7:22; neither ordinary years nor months selected, but an unspecified mean'},
 limits=['Do not use one unit across all three. Original rounded descriptions and exact arithmetic remain separate.'],kind='worked_timing_examples')
rec('Alternative timing for the same seven-degree interval',[175,176],
 'For Moon–Mars7:22 Lilly reports about three years and three quarters using a mean between years and months. Because the question was general, he says he might instead have allowed one year for each degree.',
 limits=['No exact mean formula is given. A half-year per degree is not explicitly stated. The one-year alternative is retained as an alternative, not added evidence.'],kind='reported_timing_alternatives')
rec('Later outcome, threatened harms and collective override',[176],
 'After or about that time the author reports dangerous actions, intervals of good/ill, later unfavourable fortune, survival and honourable royal employment but public opposition, no notable service, and sentence barring an end of life in England. He says the last might in some measure have been foreseen from fourth-lord Mars. General kingdom fate is said to outweigh an individual nativity or question.',
 limits=['Actual statements include hindsight and a new collective explanation; not a project pre-outcome prediction or a failed-prediction rescue rule. Earlier victory report and later royal-service statement concern different periods.'],kind='retrospective_author_account')
rec('Author method is not identical to every ancient rule',[176],
 'Lilly says very little has failed, explains his extended example as teaching, acknowledges possible variation from common ancient rules, and lets the reader follow their principles while describing his method as developed from their writings.',
 limits=['Neither historical consensus nor out-of-sample validation follows.'],kind='methodological_self_report')

rec('Fortune receives rays but does not cast them',[177],
 'Lilly likens Ptolemy importance of Fortune to a planet, then states Fortune has no aspect of its own while planets may cast their aspects to it.',
 limits=['The importance attribution is Lilly reporting Ptolemy, not an independent cross-source check. A geometric relation must preserve ray direction.'],section='XXIII',kind='definition')
rec('Fortune estate interpretation and stated contrary',[177],
 'Good placement in heaven, good house, benefic aspect, angularity or a sign fortunating Fortune correspond to a firm querent estate; adverse placement is judged contrariwise.',
 limits=['Source research claim, not financial advice. The author later admits uncertainty about its true effects.'],section='XXIII')
rec('Fortune same formula by day and night',[177,178],
 {'procedure':'Subtract Sun sign/degree/minute from Moon, adding twelve signs if needed; add Ascendant and remove twelve signs if needed.',
  'modern_exact_arithmetic_expression':'(Ascendant + Moon - Sun) modulo360 degrees'},
 limits=['Continuous cyclic notation is our implementation of the stated procedure. Day/night does not reverse this author-selected formula.'],section='XXIII',kind='calculation_definition')
rec('Fortune worked example',[177,178],
 {'Moon':'5 signs21:18 (Virgo21:18)','Sun':'0 signs4:18 (Aries4:18)',
  'difference':'5 signs17:00','Ascendant':'4 signs23:27 (Leo23:27)',
  'result':'10 signs10:27 (Aquarius10:27)'},
 limits=['Signs here count completed signs from zero; Aquarius is eleventh named sign but10 completed signs. Do not shift result one sign.'],section='XXIII',kind='worked_example')
PHASE_GUIDE=[
 {'phase':'new Moon','exact_elongation_degrees':0,'author_house':1,'following_interval':'after new before first quarter','author_interval_houses':[1,2,3]},
 {'phase':'first quarter','exact_elongation_degrees':90,'author_house':4,'following_interval':'after first quarter before full','author_interval_houses':[4,5,6]},
 {'phase':'full Moon','exact_elongation_degrees':180,'author_house':7,'following_interval':'after full before last quarter','author_interval_houses':[7,8,9]},
 {'phase':'last quarter','exact_elongation_degrees':270,'author_house':10,'following_interval':'after last quarter before new','author_interval_houses':[10,11,12]}]
for row in PHASE_GUIDE:
 rec('Fortune lunar-phase mnemonic: '+row['phase'],[178],row,
 limits=['The author calls this a beginner error check. Degree offsets and actual unequal house cusps are not equivalent by definition; the helper returns the stated mnemonic, not computed house membership.'],section='XXIII',kind='mnemonic_row')
rec('Alternate nocturnal practice reported but not selected',[178],
 'Some reverse Moon and Sun at night. Lilly repeats his same-day/night method, attributing it to Ptolemy and claiming agreement by all current practitioners.',
 limits=['The selected method and the reported alternative are different. The source glyph in the reversal clause is obscured; its context identifies the intended reversal. Claimed practitioner unanimity is not independently verified.'],section='XXIII',kind='reported_alternative')
FORTUNE_ROWS=[
 ('S01','sign_strength',['Taurus','Pisces'],5,'Unconditional sign row within this table.'),
 ('S02','sign_strength',['Libra','Sagittarius','Leo','Cancer'],4,'One category row.'),
 ('S03','sign_strength',['Gemini'],3,''),
 ('S04','sign_strength',['Virgo'],2,'Only if Fortune in Jupiter OR Venus terms; specific terms table must be named.'),
 ('A01','benefic_contact',['Jupiter OR Venus conjunction'],5,'Fortune receives the planetary ray; not two scores for alternative planets.'),
 ('A02','benefic_contact',['Jupiter OR Venus trine'],4,'No per-contact repetition rule is stated.'),
 ('A03','benefic_contact',['Jupiter OR Venus sextile'],3,''),
 ('A04','node_contact',['North Node conjunction'],3,'This differs from the four-point planetary-table node row in earlier XIX.'),
 ('H01','house_strength',[1,10],5,''),('H02','house_strength',[7,4,11],4,''),
 ('H03','house_strength',[2,5],3,''),('H04','house_strength',[9],2,''),('H05','house_strength',[3],1,''),
 ('F01','fixed_star',['Regulus','Leo',24,34],6,'Historical position; no modern epoch conversion or assumed conjunction orb.'),
 ('F02','fixed_star',['Spica Virginis','Libra',18,33],5,'Original image has33 minutes, not OCR53; Virginis is name, Libra is position.'),
 ('C01','solar_condition',['not combust or under beams'],5,'Wording preserved; exact precedence and coverage unresolved.'),
 ('D01','sign_weakness',['Scorpio','Capricorn','Aquarius'],5,''),
 ('N01','sign_neutral',['Aries'],0,'Explicit neither gain nor loss, not an omitted sign.'),
 ('D02','malefic_contact',['Saturn OR Mars conjunction'],5,''),
 ('D03','node_contact',['South Node conjunction'],3,''),
 ('D04','malefic_contact',['Saturn OR Mars opposition'],4,''),
 ('D05','malefic_contact',['Saturn OR Mars square'],3,''),
 ('D06','malefic_terms',['Saturn OR Mars terms'],2,'Declared term-table profile needed.'),
 ('D07','house_weakness',[12],5,''),('D08','house_weakness',[8],4,''),('D09','house_weakness',[6],4,''),
 ('D10','fixed_star_weakness',['Caput Algol','Taurus',20,54],4,'Historical position; no orb specified here.'),
 ('D11','solar_weakness',['combust'],5,'Fortune is nonphysical; source usage retained without modern physical assertion.')]
for rid,group,condition,mag,limit in FORTUNE_ROWS:
 rec('Fortune strength table '+rid,[179],{'row_id':rid,'category':group,'condition':condition,'magnitude':mag},
 limits=[limit,'Magnitude in strength/debility column, not calibrated probability or automatically additive score.'],section='XXIII',kind='table_row')
rec('Other lots postponed and Fortune effects uncertain',[179],
 'Lilly says Arabic writers use many other Parts little used in his age, promises occasional treatment, notes Fortune may sometimes signify life or illness, and explicitly says he remains little satisfied about its true effects and intends further work.',
 limits=['An elaborate table coexists with an author uncertainty statement. Neither proves predictive validity. No forecast or modern medical guidance derived.'],section='XXIII',kind='source_uncertainty')
SHORT_METHOD=[
 'Unafflicted Ascendant, essentially fortified lord and Moon trining both benefics indicate long life.',
 'Jupiter/Venus southern angle in Taurus southeast; Sun eastern Aries; Moon southern/southwestern Virgo: travel south or a little east.',
 'Benefics Midheaven plus North Node and Sun ninth indicate pleasant youth.',
 'Sun and Moon past good/bad aspects indicate mixed events; more evil aspects and superior planets increase the evil and lessen good.',
 'Applying Moon–Jupiter trine and exalted Sun promise preferment; weak Moon second later opposing Mars indicates danger after some joy.',
 'Smaller degree gap to angular Jupiter indicates near/present happiness; larger gap to Mars indicates later miseries after honour.']
for i,text in enumerate(SHORT_METHOD,1):
 rec('Short-method summary '+str(i),[180],text,
 limits=['Same preceding chart and narrative; no additional independent case. Qualitative near/later labels do not resolve exact time scaling.'],section='XXIII',kind='same_case_summary')
rec('Detailed reasoning before summary; nontechnical client delivery',[180],
 'Beginners should first write judgments with full reasons, then contract the opinion to a narrow compass. Avoid technical terms in delivery unless the querent understands the art.',
 limits=['Pedagogical advice does not validate the conclusions or permit silently dropping conditions in the full research record.'],section='XXIII',kind='pedagogy')

TIMING={
 'source_pages':[164,165,168,171,172,175,176],
 'general_eight_degree_example':{'moveable':'8 weeks','common':'8 months','fixed':'8 years','qualification':'only example and general; bounded by other concurring significators'},
 'house_age':{'order':[12,11,10,9,8,7,6,5,4,3,2,1],'default_years_per_house':5,'long_life_alternative_years_per_house':6,'selection':'extra year only when source life significators very strong; not adjudicated here','explicit_examples':AGE_EXAMPLES},
 'case_intervals':[
 {'id':'T1','pages':[171],'geometry':'Sun4:18 Aries minus ninth cusp2:08 Aries','exact_arcminutes':130,'author_timing':'left within two months','direction':'Sun already past cusp, not future cusp perfection'},
 {'id':'T2','pages':[174,175],'geometry':'Moon21:18 Virgo minus Mercury opposition point14:57 Virgo','exact_arcminutes':381,'author_timing':'about six months and somewhat more before question'},
 {'id':'T3','pages':[172,175],'geometry':'Jupiter trine point24:24 Virgo minus Moon21:18 Virgo','exact_arcminutes':186,'author_timing':'almost/about three years after question','qualification':'printed chart difference slightly over3 degrees; source prose approximate'},
 {'id':'T4','pages':[175],'geometry':'end Aries30:00 minus Sun4:18 Aries','exact_arcminutes':1542,'author_timing':'about26 months, one month for each of about26 degrees','qualification':'exact remainder25:42; author rounds'},
 {'id':'T5','pages':[175,176],'geometry':'Mars opposition point28:40 Virgo minus Moon21:18 Virgo','exact_arcminutes':442,'author_timing':'about3 years and3 quarters','alternative_author_scale':'might allow one year per degree because question general','mean_formula':'UNSPECIFIED; do not replace with an exact half-year rule'}],
 'no_calendar_conversion':'The chart dual day notation and unspecified timing units are not converted to modern dated forecasts.'}
ISSUES=[
 ('health_boolean',[163,164],'Mixed conjunctions and alternatives in health list; no unique automatic conjunction/disjunction circuit.'),
 ('adverse_outcome_disjunction',[164,165,166],'Short life, danger and other misfortune differ; later house-based branches and caution remain binding.'),
 ('fixed_star_scope',[164,166],'No contact orb, precessional epoch update or calibrated stellar effect specified.'),
 ('time_scale_general',[164,165],'Weeks/months/years is expressly general and qualified, not sufficient automatic scale selection.'),
 ('mixed_sign_time',[164,165],'Two significators can be in different modalities; no exhaustive mixed-case lookup supplied.'),
 ('cusp_geometry',[165,171],'Angular distance and event time are separate; Sun already beyond ninth cusp in the case.'),
 ('age_scale_selection',[168],'Five years default, variable and six-year alternative; no exact strength threshold or boundary inclusion supplied.'),
 ('age_case_rounding',[172],'Mars eighth described age24–26 despite default eighth20–25; not silently retuned.'),
 ('direction_hierarchy',[167,171],'House quadrant, sign direction, country correspondence and within-country fallback lack a complete precedence algorithm.'),
 ('functional_benefic',[167,170,171,172],'General eighth-lord caution coexists with favourable eighth-ruler Jupiter case; preserve context rather than veto or automatic reconciliation.'),
 ('case_calendar',[169],'Printed dual date24.14 martij1632 and time2:15PM not resolved to modern calendar/timezone.'),
 ('case_partial_chart',[169],'Selected positions verified; no full cusp chart, exact ephemeris parity or complete astronomical trajectories asserted.'),
 ('hindsight_exposure',[170,173,174,176],'Reported confirmations, author belief and retrospective could-have-foreseen claims are not separate untouched observations.'),
 ('sun_no_aspect',[173,174],'Applying Sun–Saturn trine coexists with local no-aspect language in liberty argument; scope unresolved.'),
 ('multiple_mercury_causes',[173],'Lawyer, writings, money, friend and child alternatives must not all receive independent hit credit.'),
 ('timing_mean',[175,176],'Mean between years and months gives approximate3.75 years; arithmetic defining that mean is not supplied.'),
 ('same_gap_other_scale',[176],'One year per degree is explicitly another option; it must not be chosen after outcome reveal.'),
 ('event_sequence',[170,172,175],'Moon first Jupiter then Mars is the source sequence; computing static gaps does not reproduce exact moving-target encounters.'),
 ('fortune_night_variant',[178],'Source reports but does not select nocturnal reversal; obscured glyph noted separately from contextual interpretation.'),
 ('fortune_phase_houses',[178],'Degree offsets0/90/180/270 from Ascendant are not automatically unequal physical house cusps; mnemonic is retained as source claim.'),
 ('fortune_strength_aggregation',[179],'OR alternatives, overlapping conditions and ray direction do not supply a fully specified net-score algorithm.'),
 ('fortune_solar_predicates',[179],'Combustion of a nonphysical Part is a symbolic source usage; relation to physical-planet thresholds and nested conditions unspecified.'),
 ('fortune_sign_virgo',[179],'Virgo strength depends on benefic terms, unlike unconditional sign rows; term table and exact boundaries must be declared.'),
 ('author_admission',[179],'Author remains uncertain about true effects even after supplying detailed table; no validation implied.'),
 ('summary_vs_full',[180],'Short summary uses near/present language and changed direction emphasis; no extra evidence or alternative exact timing selected.')]

if __name__=='__main__':
    rules={'schema_version':2,'batch_id':'B02e','records_count':len(RECORDS),'first_record_number':568,'last_record_number':567+len(RECORDS),'records':RECORDS}
    fortune={'source_id':SID,'source_sha256':SHA,'pdf_page':179,'printed_page':145,
      'rows':[{'id':i,'category':g,'condition':c,'magnitude':m,'qualification':q} for i,g,c,m,q in FORTUNE_ROWS],
      'phase_guide':PHASE_GUIDE,'row_aggregation':'UNSPECIFIED_NO_AUTOMATIC_NET_SCORE','no_person_inference':True}
    for name,obj in [('RULES.json',rules),('CASE_REFERENCE.json',CASE),('TIMING_CASES.json',TIMING),('FORTUNE_TABLE.json',fortune),('DIRECTIONAL_QUARTERS.json',QUARTERS),('STAR_NATURE_CATALOGUE.json',STAR_SPECTRA),('UNRESOLVED.json',{'issues':[{'id':f'B02e-U{i:02}','topic':t,'pdf_pages':p,'issue':s} for i,(t,p,s) in enumerate(ISSUES,1)]})]:
        save(name,obj)
    print('SOURCE_RECORDS',len(RECORDS),'LAST',rules['last_record_number'],'FORTUNE_ROWS',len(FORTUNE_ROWS),'UNRESOLVED',len(ISSUES))
