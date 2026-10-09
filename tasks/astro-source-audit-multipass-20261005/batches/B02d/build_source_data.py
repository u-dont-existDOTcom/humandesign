"""Rebuild the separately audited Lilly I.XIX-XXI reference data; no natal inference."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SID = 'LILLY1647_WELLCOME_B30338724'
SHA = '2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
SIGNS = 'Aries Taurus Gemini Cancer Leo Virgo Libra Scorpio Sagittarius Capricorn Aquarius Pisces'.split()
PLANETS = 'Saturn Jupiter Mars Sun Venus Mercury Moon'.split()
RECORDS = []

def rec(title, pages, statement, prerequisites=(), limits=(), section='XIX', kind='conditional_source_rule'):
    n = 392 + len(RECORDS)
    RECORDS.append({'id': f'LI.1647.I.{section}.R{n}', 'title': title, 'kind': kind,
        'source_locator': {'source_id': SID, 'source_sha256': SHA, 'book': 'I',
            'section_key': 'I.' + section, 'pdf_pages': list(pages), 'printed_pages': [p-34 for p in pages]},
        'statement_type': 'editor_normalized_paraphrase', 'source_statement': statement,
        'prerequisites': list(prerequisites), 'qualifications_and_limits': list(limits),
        'runtime_status': 'REFERENCE_ONLY_NOT_PROMOTED', 'independent_evidence_unit': False})

def save(name, obj):
    (ROOT/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

rec('Principal rays and conjunction terminology',[139,140],
    {'sextile':60,'square':90,'trine':120,'opposition':180,'conjunction':'same sign, degree and minute; coition, synod, congress'},
    limits=['Lilly calls conjunction an aspect improperly and refers to other new aspects mentioned earlier; this is not a whole-book absence claim.'],kind='definition')
rec('Reconciliation and the two adverse aspects',[140],
    'Square signifies imperfect enmity: reconciliation remains possible with assistance from the other significators. Opposition signifies perfect hatred: no peace expected before the suit ends or the challenge has been fought.',
    ['Question about reconciling two adversaries; the planets are their main significators.'],
    ['Do not infer innate character or relationship safety from an arbitrary natal square/opposition. Later reception/perfection qualifications are retained separately.'])
rec('Favourable aspects and conjunction polarity',[140],
    'Sextile and trine argue love, unity and friendship, trine more forcibly; conjunctions are good or bad according to friendship/enmity of the planets.',
    ['Relevant significators in the enquiry.'],['No numerical force ratio or independent-evidence multiplier is supplied.'])
rec('Partile definition and examples',[140,141],
    {'definition':'exact separation corresponding to the aspect','examples':['Venus Aries 9, Jupiter Leo 9: trine','Sun Taurus 1, Moon Cancer 1: sextile'],
     'interpretation':'Near completion when signifying good; equally present evil when mischief is threatened.'},
    limits=['Degree-based examples do not specify a universal one-degree orb or settle all minute/second tolerances.'],kind='definition_and_examples')
rec('Platick rays use both planets moieties',[141],
    {'definition':'Within the half-sum of the two planets\' orbs','example':'Venus Taurus 10 and Saturn Virgo 18: eight degrees from trine; moieties four plus five give nine.'},
    ['The planets signify the matter.'],['Two orb columns are printed; select a declared profile, never retrospectively whichever fits.'],kind='definition_and_example')
ORBS = {'source_id':SID,'source_sha256':SHA,'pdf_page':141,'printed_page':107,'units':'arcminutes of the full listed orb, before taking moieties',
 'profiles':{'p107_first_column':dict(zip(PLANETS,[600,720,450,1020,480,420,750])),
             'p107_other_authors_column':dict(zip(PLANETS,[540,540,420,900,420,420,720]))},
 'author_choice':'Lilly says he sometimes uses one column and sometimes the other as his memory remembers them, and describes this as without error.',
 'research_limit':'The author\'s statement is preserved, not evidence of equivalence or empirical accuracy.'}
for planet in PLANETS:
    rec(planet+' orb alternatives',[141],{k:v[planet] for k,v in ORBS['profiles'].items()},limits=['Arcminutes; alternative full orbs, not two corroborating indicators.'],kind='table_row')
rec('Application with both direct',[141],
    'The swifter planet applies to the slower/ponderous one: Mercury Aries 5 to Mars Aries 10.',
    ['Both direct; appropriate relative motion.'],['Positions alone do not prove the future order of encounters.'])
rec('Application with both retrograde',[141],
    'Mercury Aries 10 to Mars Aries 9, Mercury remaining retrograde through conjunction, is an ill application associated with sudden perfection OR breaking off according to their signification.',
    ['Both retrograde and conjunction reached before Mercury turns direct.'],['Do not turn ill application into an unconditional non-occurrence prediction.'])
rec('Mixed-motion application',[141],
    'Direct Mars Aries 15 to retrograde Mercury Aries 17: ill application, great atmospheric change or sudden alteration in a question.',
    ['Direct planet lower, retrograde planet higher.'],['Weather and question outcomes are different reference frames; no exact forecast from these illustrative coordinates.'])
rec('Application and weight hierarchy',[142],
    'Lighter planets apply to more ponderous ones; superior planets do not apply to inferior ones unless retrograde. Saturn Aries 10 receives applications from Mars at degree 7 of Aries, Gemini, Cancer, Leo or Libra by conjunction, sextile, square, trine or opposition respectively.',
    limits=['Exact contact described at matching degree and minute; a complete event calculation requires both trajectories.'],kind='definition_and_examples')
rec('Dexter and sinister rays',[142,143],
    'Sinister rays follow sign succession; dexter run against succession and are described as more forcible.',
    limits=['The direction belongs to the ray-casting source planet. No multiplier is specified.'],kind='definition')
# Manual source-table sign numbers, not a generator substituted for the observed table.
ASPECT_ROWS = [
 [1,[11,10,9],[3,4,5],7],[2,[12,11,10],[4,5,6],8],
 [3,[1,12,11],[5,6,7],9],[4,[2,1,12],[6,7,8],10],
 [5,[3,2,1],[7,8,9],11],[6,[4,3,2],[8,9,10],12],
 [7,[5,4,3],[9,10,11],1],[8,[6,5,4],[10,11,12],2],
 [9,[7,6,5],[11,12,1],3],[10,[8,7,6],[12,1,2],4],
 [11,[9,8,7],[1,2,3],5],[12,[10,9,8],[2,3,4],6]]
INCONJUNCT_RAW = [[2,8],[1,3,7,9],[2,8],[5,11],[4,6,10,12],[5,11],
                 [8,2],[7,9,1,3],[8,2],[5,11],[10,12,4,6],[5,11]]
for sign, dex, sin, opp in ASPECT_ROWS:
    rec(SIGNS[sign-1]+' aspect table',[142],{'dexter_sextile_square_trine':dex,'sinister_sextile_square_trine':sin,'opposition':opp},limits=['Sign numbers 1..12; exact rays require like degrees, not merely any positions in those signs.'],kind='table_row')
for sign, targets in zip(SIGNS,INCONJUNCT_RAW):
    rec(sign+' signs not beholding, raw table',[143],targets,limits=['This is the literal listed subset, not a repaired complete geometric non-aspect list. Unlisted is not automatically aspected.'],kind='table_row')
rec('Initial versus full separation',[144],
    {'initial_example':'Saturn and Jupiter Aries 10:25; Jupiter at 10:31 or 10:32 is separating.',
     'full_clearance_examples':['Saturn 9-degree orb and Jupiter 9-degree orb: total clearance nine degrees.','Sun 15 and Moon 12: clearance thirteen degrees thirty minutes.']},
    limits=['A six-minute initial departure and full moiety clearance are different predicates. These examples use the alternative orb column.'],kind='definition_and_examples')
rec('Separation timing in a marriage question',[144],
    'Recently separated significators suggest a recent chance of marriage now suspended by dislike or rupture. Greater separation accompanies alienation; degrees left to full clearance supply a count of weeks, days, months or years.',
    ['The two planets are the marriage significators at the question time.'],
    ['Unit choice is not specified by this passage. A precise date cannot be obtained by choosing units after seeing an event.'])
rec('Separation timing modifiers',[144],
    'Both significators in moveable signs, angular and swift hasten the time; common signs require longer, fixed signs longer still.',
    limits=['Keep the joint conditions; mixed modalities and absolute duration multipliers are unspecified.'])
rec('Prohibition',[144,145],
    'Before two applying principals perfect their aspect, a third planet interposes body or aspect, hindering and retarding the matter.',
    ['Principals signify completion of the question.','Intervention occurs before perfection.'],['Hindering/retarding is not automatically permanent impossibility.'])
rec('Bodily prohibition example',[145],
    'Mars Aries 7, Saturn Aries 12, Sun Aries 6: the faster Sun reaches Mars and then Saturn before Mars reaches Saturn.',
    ['Asserted encounter order, not just a static three-planet arrangement.'],['The statement that combustion is the greatest misfortune belongs to this explanatory passage.'],kind='worked_example')
rec('Aspect prohibition example',[145],
    'Mars Aries 7, Saturn Aries 15, Sun Gemini 5: the faster Sun reaches dexter sextiles to Mars and Saturn before the principal conjunction; analogous square, trine or opposition intervention.',
    limits=['No numerical speeds are provided. Do not manufacture precise time differences.'],kind='worked_example')
rec('Refranation',[145],
    'Mars Aries 7 approaches Saturn Aries 12 but turns retrograde before reaching degree 10 or 11; Saturn continues direct, and the promised conjunction is not effected.',
    limits=['Reversal before the promised encounter, not mere slowness.'],kind='definition_and_example')
rec('Translation, introductory definition',[145],
    'A light planet separates from a weightier planet and presently joins another weightier one, bodily or by aspect. Mercury Aries 16 takes Mars Aries 15 toward Saturn Aries 20.',
    ['Intermediary is the appropriate lighter carrier.'],['XXI adds explicit reception and no-intervening-contact conditions for its perfection route; retain both scopes.'])
rec('Translation, represented means',[145],
    'The person represented by the translating planet procures the assistance represented by the source planet for the receiving matter; useful in marriage, lawsuits and ordinary questions.',
    limits=['Subject is question-specific mediation, not a generic personality trait.'])
rec('Mutual reception and examples',[146],
    {'definition':'Two relevant planets in each other\'s essential dignities; by domicile is strongest.',
     'examples':['Sun Aries and Mars Leo: domicile.','Venus Aries and Sun Taurus: triplicity if by day.','Venus Aries numbered degree 24 and Mars Gemini numbered degree 16: terms.']},
    ['Planets are significators in the matter.'],['Can involve triplicity, term, face or another essential dignity. Direction and day/night conditions must be preserved.'],kind='definition_and_examples')
rec('Reception despite adverse or missing aspect',[146],
    'Mutual reception of the principal significators can bring the thing to pass suddenly and without great trouble to both parties, despite no aspect, denial by aspects or doubtful square/opposition testimony.',
    limits=['Retain beside XXI\'s much more qualified and often regrettable opposition-perfection description; do not erase the tension.'])
rec('Peregrine definition and examples',[146],
    'No essential dignity in the occupied sign degree. Saturn at Aries 10 is peregrine, but at 27/28 etc. is in its term and not peregrine. The Sun in Cancer has no dignity throughout that sign.',
    limits=['Fall and peregrinity need not be mutually exclusive. Reception versus own-dignity treatment remains separate.'],kind='definition_and_examples')
rec('Peregrine theft heuristic',[146],
    'An angular or second-house peregrine planet very often signifies the thief.',
    ['A theft question.'],['Historical heuristic; do not infer criminality in a person from natal placement.'])
rec('Void of course',[146],
    'A planet has separated from a planet and does not forthwith, while it remains in that sign, apply to another; most commonly observed for the Moon. Business seldom proceeds handsomely.',
    limits=['Apply is not silently replaced by perfect an exact contact. Later strong-significator and sign exceptions are separately retained.'],kind='definition_and_qualification')
rec('Frustration',[146,147],
    'A swift planet would join a heavier one, but that heavier planet joins a third first: Mercury Aries 10, Mars 12, Jupiter 13, with Mars meeting Jupiter before Mercury reaches Mars.',
    limits=['Which encounter comes first requires trajectories or an explicitly supplied event ordering.'],kind='definition_and_example')
rec('Hayz as actually printed',[147],
    {'day_branch':'masculine diurnal planet by day above the earth in a masculine sign',
     'night_branch':'feminine nocturnal planet by night UNDER the earth in a feminine sign',
     'use':'querent content at question time when the significator so qualifies'},
    limits=['The nocturnal below-earth wording was checked on the image and is not replaced with another school\'s above-earth convention.'],kind='definition')
rec('Superior and inferior planets',[147],
    {'superior':['Saturn','Jupiter','Mars'],'inferior':['Venus','Mercury','Moon'],'reference':'geocentric orb of the Sun'},
    limits=['Historical cosmological classification, not a modern physical distance ranking.'],kind='definition')
rec('Combustion definition and contradictory example',[147,148],
    {'condition':'same sign as Sun, no more than eight degrees thirty minutes either side in the stated definition',
     'examples':['Jupiter Aries 10, Sun Aries 18: eight degrees, called combust.','Jupiter Aries 28, Sun Aries 18: ten degrees, also called combust in print.'],
     'restriction':'bodily conjunction in one sign, not sextile/square/trine/opposition; Sun cannot itself be combust'},
    limits=['Second example conflicts with the threshold, confirmed on image. Do not alter 28 to 26 or expand threshold silently. Exact threshold boundary and cazimi precedence remain explicit conventions.'])
rec('Combustion direction, moiety and represented state',[147],
    'The Sun hastening toward a conjunction afflicts more than receding; Lilly uses the Sun\'s moiety, not Jupiter\'s (the latter would be four degrees thirty). He acknowledges disagreement and asks the reader to use what proves truest. Combust querent significator denotes fear and being overpowered by a great person.',
    limits=['Author-endorsed development selection is not untouched validation; no retrospective orb shopping.'])
rec('Under the beams and cazimi',[147],
    {'beams':'until fully seventeen degrees from the Sun either side','cazimi':'within seventeen minutes forward or backward; fortified',
     'example':'Sun Taurus 15:30 and Mercury Taurus 15:25: five minutes'},
    limits=['Same-sign requirement is explicit for combustion, not independently restated for beams. Boundary and overlap policies are not a ready-made signed outcome score.'],kind='definitions_and_example')
rec('Orientality of superior planets',[148],
    'Saturn, Jupiter and Mars are oriental from conjunction to opposition and occidental from opposition to conjunction; oriental rises before the Sun, occidental is visible above the horizon or sets after sunset.',
    limits=['A longitude proxy is not automatically a full observed-visibility calculation.'],kind='definition')
rec('Orientality and elongation of Mercury and Venus',[148],
    'Oriental when in fewer degrees of the Sun\'s sign or its preceding sign, occidental when in more degrees or the next sign. Stated maximum elongations are Mercury 28 degrees, Venus 48, with some allowing a few more; no sextile/square/trine/opposition to Sun.',
    limits=['These are source bounds, not newly verified Swiss Ephemeris results.'],kind='definition')
rec('Moon oriental versus occidental',[148],
    'Oriental from opposition to conjunction, occidental from conjunction to opposition, explained by the Moon\'s greater speed.',
    limits=['Increasing light and occidental are alternative descriptions of one table condition, not two score increments.'],kind='definition')
rec('Bodily besieging',[148],
    'A planet between the bodies of Saturn and Mars: Saturn Aries 15, Mars Aries 10, Venus Aries 13. The adverse represented condition requires Venus to be significatrix in that figure.',
    limits=['The image reads Aries, not the Capricorn inferred by the text layer. This local definition is bodily, unlike the broader Rhetorius aspect-pattern definition.'],kind='definition_and_example')
rec('Selection of ancient accidents',[148],
    'Lilly says he omits other accidents described by the ancients because he regards them as of little purpose in judgement.',
    limits=['This does not identify a complete excluded list or empirically prove the excluded techniques useless.'],kind='methodology')
rec('Direct, retrograde and stationary',[148],
    {'direct':'forward from degree 13 to 14 etc.','retrograde':'backward from 10 to 9,8,7 etc.','stationary':'moves not at all; superior planets said to do so two, three or four days before retrogradation'},
    limits=['An approximate historical stationary interval is not an astronomical exact-zero-speed plateau.'],kind='definitions')

# Magnitudes are printed in separate favourable/adverse columns. Signed values are a research representation.
WEIGHT_ROWS = [
 ('E01','essential_fortitude','own domicile OR mutual reception by domicile',5,'One table row, not five for each alternative.'),
 ('E02','essential_fortitude','exaltation OR reception by exaltation',4,'One table row; do not stack the alternatives.'),
 ('E03','essential_fortitude','own triplicity',3,'Use the declared day/night source profile.'),
 ('E04','essential_fortitude','own term',2,'Use an identified table and degree convention.'),
 ('E05','essential_fortitude','own face',1,'Source calls this sufficient to avoid peregrinity.'),
 ('D01','essential_debility','detriment',5,''),('D02','essential_debility','fall',4,''),('D03','essential_debility','peregrine',5,''),
 ('A01','accidental_fortitude','house 1 OR 10',5,''),('A02','accidental_fortitude','house 7 OR 4 OR 11',4,''),
 ('A03','accidental_fortitude','house 2 OR 5',3,''),('A04','accidental_fortitude','house 9',2,''),('A05','accidental_fortitude','house 3',1,''),
 ('A06','accidental_fortitude','direct',4,'Sun and Moon explicitly excluded: always direct, this row is void for them.'),
 ('A07','accidental_fortitude','swift',2,''),('A08','accidental_fortitude','Saturn/Jupiter/Mars oriental',2,''),
 ('A09','accidental_fortitude','Mercury/Venus occidental',2,''),('A10','accidental_fortitude','Moon increasing OR occidental',2,'Aliases in one row.'),
 ('A11','accidental_fortitude','free of combustion AND Sun beams',5,''),('A12','accidental_fortitude','cazimi',5,'Overlap precedence with combustion is not specified in this table.'),
 ('A13','accidental_fortitude','partile conjunction Jupiter and Venus',5,'Wording does not settle per-contact repetition or both-versus-either universally.'),
 ('A14','accidental_fortitude','partile conjunction North Node',4,''),
 ('A15','accidental_fortitude','partile trine Jupiter and Venus',4,'Do not invent a repeated-contact sum.'),
 ('A16','accidental_fortitude','partile sextile Jupiter and Venus',3,'Do not invent a repeated-contact sum.'),
 ('A17','accidental_fortitude','conjunction Cor Leonis at Leo 24',6,'Historical position, no contemporary precession update or orb invented.'),
 ('A18','accidental_fortitude','conjunction Spica Virginis at Libra 18',5,'Virginis is part of the star name; listed position is Libra.'),
 ('B01','accidental_debility','house 12',5,''),('B02','accidental_debility','house 8 OR 6',2,''),('B03','accidental_debility','retrograde',5,''),
 ('B04','accidental_debility','slow',2,''),('B05','accidental_debility','Saturn/Jupiter/Mars occidental',2,''),
 ('B06','accidental_debility','Mercury/Venus oriental',2,''),('B07','accidental_debility','Moon decreasing',2,''),
 ('B08','accidental_debility','combust',5,''),('B09','accidental_debility','under Sun beams',4,'Nested geometrical zones do not authorize blindly adding both debilities.'),
 ('B10','accidental_debility','partile conjunction Saturn OR Mars',5,''),('B11','accidental_debility','partile conjunction South Node',4,''),
 ('B12','accidental_debility','besieged by Saturn and Mars',5,''),('B13','accidental_debility','partile opposition Saturn OR Mars',4,''),
 ('B14','accidental_debility','partile square Saturn OR Mars',3,''),
 ('B15','accidental_debility','conjunction Caput Algol at Taurus 20 OR within five degrees',5,'The explicit five-degree allowance belongs to this row, not automatically all fixed stars.')]
WEIGHTS = {'source_id':SID,'source_sha256':SHA,'pdf_page':149,'printed_page':115,
 'rows':[dict(zip(['id','column','condition','magnitude','qualification'],r)) for r in WEIGHT_ROWS],
 'aggregation_status':'Row inventory, not a completed net chart scoring algorithm. The next page defers detailed use to a later example.'}
for row in WEIGHTS['rows']:
    rec('Fortitude/debility '+row['id'],[149],row,limits=['Printed magnitude retained; no predictive probability or global sum implied.'],kind='table_row')
rec('Use of strength table deferred',[150],
    'Lilly postpones explaining the table until an example later in the book.',
    limits=['The mere presence of numbers does not settle all stacking, overlap or comparison rules.'],kind='methodology')

SEX_ENDPOINTS = [
 [[8,15,30],[9,22]],[[11,21,30],[5,17,24]],[[16,26],[5,22,30]],[[2,10,23,30],[8,12,27]],
 [[5,15,30],[8,23]],[[12,30],[8,20]],[[5,20,30],[15,27]],[[4,17,30],[14,25]],
 [[2,12,30],[5,24]],[[11,30],[19]],[[5,21,27],[15,25,30]],[[10,23,30],[20,28]]]
LIGHT_RAW = [
 'd3 l8 d16 l20 v24 l29 v30','d3 l7 v12 l15 v20 l28 v30','l4 d7 l12 v16 l22 d27 v30',
 'l12 d14 v18 sm20 l28 v30','d10 sm20 v25 l30','d5 l8 v10 l16 sm22 l27 d30',
 'l5 d10 l18 d21 l27 v30','d3 l8 v14 l22 sm24 v29 d30','l9 d12 l19 sm23 l30',
 'd7 l10 s15 l19 d22 v25 d30','sm4 l9 d13 l21 v25 l30','d6 l12 d18 l22 v25 l28 d30']
PITTED = [[6,11,16,23,29],[5,12,24,25],[2,12,17,26,30],[12,17,23,26,30],[6,13,15,22,23,28],
 [8,13,16,21,22],[1,7,20,30],[9,10,22,23,27],[7,12,15,24,27,30],[7,17,22,24,29],[1,12,17,22,24,29],[4,9,24,27,28]]
LAME = [[],[6,7,8,9,10],[],[9,10,11,12,13,14,15],[18,27,28],[],[],[19,28],[1,7,8,18,19],[26,27,28,29],[18,19],[]]
FORTUNE = [[19],[3,15,27],[11],[1,2,3,4,15],[2,5,7,19],[3,14,20],[3,15,21],[7,18,20],[13,20],[12,13,14,20],[7,16,17,20],[13,20]]
DEGREES = {'source_id':SID,'source_sha256':SHA,'pdf_page':150,'printed_page':116,
 'representation':'Raw terminal ordinal degrees. Sorted endpoint expansion is an explicit mathematical interpretation, not silent conversion to continuous natal longitude.',
 'labels':{'m':'historical masculine','f':'historical feminine','l':'light','d':'dark','sm':'smoky','v':'void','s':'unresolved abbreviation on Capricorn third segment'},
 'uncertainties':['Capricorn s15 is retained as s, not silently mapped to smoky.','Virgo l27 reading is provisional; its damaged letter must not be silently treated as certain.'],
 'rows':{s:{'masculine_endpoints':SEX_ENDPOINTS[i][0],'feminine_endpoints':SEX_ENDPOINTS[i][1],
            'light_dark_raw':LIGHT_RAW[i], 'pitted':PITTED[i],'lame_deficient':LAME[i],'increasing_fortune':FORTUNE[i],
            'blank_policy':'empty means no entry in this table, not universal absence'} for i,s in enumerate(SIGNS)}}
for sign,row in DEGREES['rows'].items():
    rec(sign+' fine-degree table',[150],row,limits=['Historical classifications only; no modern diagnostic, gender-identification or wealth guidance.'],kind='table_row')
rec('Degree sex as a conditional tiebreaker',[151],
    'When angles, planet sex and signs leave equal testimony in the question, inspect the Moon, relevant significator and relevant house cusp in masculine/feminine degrees to poise judgement.',
    ['The preceding testimony is tied.'],['Examples concern fetal sex or sex of a thief; historical claims, not modern identification tools. Do not use as an unrestricted rescue after an observed failure.'])
rec('Light and dark degrees',[151],
    'Light rising degrees describe a fairer appearance; dark degrees an obscurer complexion. Conditional upon already being deformed, dark increases and light moderates the imperfection.',
    ['Relevant ascendant in a nativity or question.'],['Appearance and impairment assertions are historical; no modern diagnostic inference.'])
rec('Void and smoky degrees',[151,152],
    'Moon OR Ascendant in void degrees describes small understanding regardless of appearance; smoky degrees describe mixed complexion, stature and condition, neither extreme.',
    limits=['Void degrees are not void-of-course motion. Historical judgement of intellect is not validated measurement.'])
rec('Aries light-degree worked reading',[152],
    'First three degrees dark, next through eight light, through sixteen dark, through twenty light, through twenty-four void, through twenty-nine light, final degree void.',
    limits=['Endpoint language preserved in the raw table; exact continuous-boundary policy remains a declared implementation choice.'],kind='worked_example')
rec('Pitted degrees and assistance',[152],
    'Sun OR Ascendant degree OR Ascendant lord in a pitted degree describes the questioner at a stand and needing help, like a person unable to leave a ditch without assistance.',
    limits=['Sun is the checked glyph; do not substitute Moon by analogy. This does not certify a psychological state.'])
rec('Azimene search starts from an observed condition',[152],
    'If the person is observed impaired or chronically diseased, and the figure yields no immediate explanation, inspect Ascendant, Moon, Ascendant lord or principal lord in deficient degrees.',
    ['The impairment is already observed; the source proposes explanatory search.'],
    ['This is retrospective selection, not a frozen forward test. Preserve the direction of inference and do not use for clinical advice.'])
rec('Fortune-increasing degrees',[152],
    'Second-house cusp OR second-house lord OR Jupiter OR Lot of Fortune in these degrees is an argument of wealth.',
    limits=['The text names the fifth column; the fortune column is sixth when counting the sign column. No empirical wealth probability follows.'])

# Historical correspondence labels, not a modern anatomical or diagnostic ontology.
BODY_RAW = [
 ['Breast,arms','Neck,throat,heart,belly','Belly,head','Thighs','Reins,feet','Secrets,legs','Knees,head'],
 ['Heart,breast,belly','Shoulders,arms,belly,neck','Reins,throat','Knees','Secret-members,head','Thighs,feet','Legs,throat'],
 ['Belly,heart','Breast,reins,secrets','Secrets,arms,breast','Legs,ankles','Thighs,throat','Knees,head','Feet,shoulders,arms,thighs'],
 ['Reins,belly,secrets','Heart,secrets,thighs','[printed matter obscured; handwriting: Thighs,Breast]','Knees,[two printed tokens obscured]','Knees,shoulders,arms','Legs,throat,eyes','Head,breast,stomach'],
 ['Secrets,reins','Belly,thighs,knees','Knees,[uncertain middle token Hiar/Hair],belly','Head','Legs,breast,heart','Feet,arms,shoulders,throat','Throat,stomach,heart'],
 ['Thighs,secrets,feet','Reins,knees','Legs,belly','Throat','Feet,stomach,heart,belly','Head,breast,heart','Arms,shoulders,bowels'],
 ['Knees,thighs','Secrets,legs,head,eyes','Feet,reins,secrets','Shoulders,arms','Head,mal.guts','Throat,heart,stomach,belly','Breast,reins,heart,belly'],
 ['Knees,legs','Thighs,feet','Head,secrets,arms,thighs','Breast,heart','Throat,reins,secrets','Shoulders,arms,bowels,back','Stomach,heart,secrets,belly'],
 ['Legs,feet','Knees,head,thighs','Throat,thighs,hands,feet','Heart,belly','Shoulders,arms,secrets,thighs','Breast,reins,heart,secrets','Bowels,thighs,back'],
 ['Head,feet','Legs,neck,eyes,knees','Arms,shoulders,knees,legs','Belly,back','Breast,heart,thighs','Stomach,heart,secrets','Reins,knees,thighs'],
 ['Neck,head','Feet,arms,shoulders,breast','Breast,legs,heart','Reins,secrets','Heart,knees','Bowels,thighs,heart','Secrets,legs,ankles'],
 ['Arms,shoulders,neck','Head,breast,heart','Heart,feet,belly,ankles','Secrets,thighs','Belly,legs,neck,throat','Reins,knees,secrets,thighs','Thighs,feet']]
BODY = {'source_id':SID,'source_sha256':SHA,'pdf_pages':[153,154],'planet_order':PLANETS,
 'transcription':'Normalized spelling of visible historical words; uncertain and ink-altered cells retained explicitly, not inferred from the subsequent rationale.',
 'rows':{s:dict(zip(PLANETS,BODY_RAW[i])) for i,s in enumerate(SIGNS)},
 'uncertain_cells':[['Cancer','Mars'],['Cancer','Sun'],['Leo','Mars']],
 'unexpanded_token':{'Libra.Venus':'mal.guts'},'clinical_use':False}
for i,sign in enumerate(SIGNS):
    rec(sign+' planetary body-correspondence row',[153 if i<8 else 154],BODY['rows'][sign],
        limits=['Historical planet-by-sign correspondences. Ink-altered/uncertain cells remain unknown, not completed by a presumed rule.'],kind='table_row')
rec('Attributed Hermes rationale and topical use',[154,155],
    'Lilly reports understanding the body table after reading Hermes aphorism 88: affliction concerns the part assigned to the afflicted sign. In a sickness question find the sick person\'s significator, its sign, and the corresponding part; Saturn in Gemini is the example of belly or heart.',
    limits=['Hermes attribution is reported through Lilly, not independently verified from a Hermes edition; not clinical guidance.'],kind='attribution_and_example')
rec('Domicile-relative anatomical sequence',[155],
    'Planet in own sign governs head, second sign neck, third arms/shoulders, and so successively. Saturn Capricorn/Aquarius/Pisces and Jupiter Sagittarius/Capricorn/Aquarius illustrate the first three positions.',
    limits=['Multiple domiciles and extra table entries are not all derived by this short rationale. Do not overwrite the actual table.'],kind='method_and_examples')
rec('Moon Aries explanation and counting tension',[155],
    'Moon in Aries is assigned head because of Aries and knees because Aries is called the ninth sign from Cancer.',
    limits=['Forward offset is nine signs but inclusive ordinal place is tenth. Preserve source wording and both quantities instead of silently correcting the author.'],kind='example_with_uncertainty')
rec('Severity and proximity',[155],
    'More sign affliction, or proximity to azimene/pitted/deficient degrees, is said to increase the mark, scar or infirmity.',
    limits=['No radius or quantitative dose-response is specified; historical assertion, not a clinical risk scale.'])

rec('Radicality alternatives',[155,156],
    'The hour lord and Ascendant lord are of one triplicity, are the same planet, OR are of the same nature. Examples: Mars hour with a water sign rising; Mars hour with Aries rising; Mars hour with Leo rising, Mars and Sun both hot and dry.',
    ['Horary question at its proposal time.'],['The triplicity wording and example need explicit implementation; not an automatic natal-chart exclusion rule.'])
rec('Early Ascendant caution and exception',[156],
    'At rising degrees 0, 1 or 2, especially short-ascension signs Capricorn through Gemini, avoid judgement unless the querent is very young AND body, complexion, moles/scars agree with the rising sign.',
    limits=['Degree-label boundaries and very young threshold are not specified; bodily agreement is historical interpretive evidence, not verified diagnostic information.'])
rec('Late Ascendant caution and exceptions',[156],
    'At rising degrees 27,28,29 judgement is unsafe, except when the querent\'s age corresponds to the degrees OR the figure uses a certain event time rather than a propounded question.',
    limits=['Do not apply the horary refusal automatically to a timed event or natal chart; exact continuous boundaries remain a declared policy.'])
rec('Late Moon and attributed via-combusta caution',[156],
    'Caution with Moon in late degrees, especially Gemini, Scorpio or Capricorn; some also warn of the last fifteen Libra or first fifteen Scorpio degrees, the via combusta.',
    limits=['No late-degree threshold here. The via-combusta addition is attributed to some, not silently made Lilly\'s categorical universal rule.'])
rec('Void-of-course qualifications',[156],
    'Matters proceed hardly when the Moon is void of course, EXCEPT if principal significators are very strong; she nevertheless performs somewhat in Taurus, Cancer, Sagittarius or Pisces.',
    limits=['These exceptions concern the judgement, not a redefinition of the motion state. They are not a promise that every desired event occurs.'])
rec('Seventh-house artist caution, topic restriction',[156],
    'Afflicted seventh cusp or retrograde/impeded seventh lord suggests the astrologer\'s judgement will give little content, when the matter belongs to another house and NOT the seventh.',
    limits=['Do not erase the topical exception, or equate querent satisfaction with predictive accuracy.'])
for title,pages,statement in [
 ('Saturn rising caution',[156],'Saturn in the Ascendant, especially retrograde: the matter seldom or never comes to good.'),
 ('Saturn seventh alternatives',[157],'Saturn seventh either corrupts the astrologer\'s judgement OR signifies a sequence of misfortunes.'),
 ('Combust Ascendant lord caution',[157],'Combust Ascendant lord: the question will not take or the querent be regulated.'),
 ('Seventh lord impaired',[157],'Unfortunate seventh lord, in fall or malefic terms: astrologer scarcely gives solid judgement.'),
 ('Equal testimony requires deferral',[157],'With equal fortunate and unfortunate testimony, defer opinion until a better-informing question; the balance cannot be known.')]:
    rec(title,pages,statement,['Reported among Arabian rules, Alkindus and others.'],['Horary pre-judgement context; historical prescriptions, not an empirically calibrated abstention rule.'])

rec('Querent, quesited and significator',[157],
    'Querent asks; quesited is the person or thing sought. The topic\'s house ruler signifies its matter; rising sign and its ruler always belong to the asker.',
    limits=['Actor/subject roles matter; an identical planetary arrangement cannot be interpreted without the actual question.'],section='XX',kind='definitions')
rec('Querent appearance and conditions are synthesized',[157],
    'Rising sign contributes bodily form. Conditions mix its lord, the Moon, the planet in the Ascendant, and planets aspecting the Moon or Ascendant lord.',
    limits=['Equally mixed is source wording, not a fully specified numerical weighting or a licence to count one observation repeatedly.'],section='XX')
rec('Topic-first chain and represented helpers',[157,158],
    'Identify the house appropriate to the matter, its sign/ruler, ruler\'s place and dignity, relation to Ascendant lord, helpers and impediments, and their house positions/rulerships. These identify the relations of assisting or hindering people.',
    limits=['Do not substitute a generic strongest planet for a topic-qualified significator.'],section='XX',kind='methodology')
rec('Moon cosignificator and rejected extension',[158],
    'Moon is cosignificator with querent/Ascendant lord in every question. Lilly expressly disapproves adding the planet from which the Moon separated as another querent significator, reporting no truth found in his practice.',
    limits=['The rejection concerns this automatic role assignment, not every use of separation. Author experience is development testimony.'],section='XX',kind='methodology_and_disagreement')
rec('Reported applying-planet quesited extension',[158],
    'Others similarly joined the planet to which the Moon applied with the lord of the quesited house.',
    limits=['Reported practice; the preceding explicit rejection must not be mechanically expanded to this separate sentence or rewritten as endorsement.'],section='XX',kind='reported_alternative')
rec('Separate judgement questions',[158],
    'After positions, applications, separations and aspects are considered, ask whether the matter occurs, by whose means, when, AND whether proceeding is good for the querent.',
    limits=['Occurrence, mechanism, timing and benefit are distinct outputs.'],section='XX',kind='methodology')

rec('Perfection route organisation',[158,159],
    'The chapter announces four means and discusses conjunction, aspect routes, translation and collection, followed by a qualified ancient house-dwelling rule.',
    limits=['Preserve headings and ensuing qualifications rather than use the count to discard a later clause.'],section='XXI',kind='organisation')
rec('Conjunction perfection and angularity',[159],
    'Ascendant lord and topic lord hasten to conjunction in the first house or an angle without prohibition or refranation before perfection: the thing comes to pass without hindrance. Speed and essential or accidental strength hasten it; succedent placement delays, cadent brings much delay, difficulty and struggle.',
    ['Relevant principal significators.','No intervention or reversal before the promised encounter.'],
    ['No numerical duration supplied; cadent is difficulty/delay, not automatic impossibility.'],section='XXI')
rec('Sextile/trine perfection prerequisites',[159],
    'Principals apply by sextile or trine from good houses with essential dignity and no malefic aspect intervening before the partile aspect.',
    limits=['An applying trine alone does not satisfy all conditions. Exact good-house/strength qualification needs an explicit source profile.'],section='XXI')
rec('Square perfection prerequisites',[159],
    'An applying square perfects provided EACH planet has dignity in its occupied degrees and they apply from proper good houses; otherwise not.',
    limits=['Do not reduce to square always prevents completion. The relevant degree convention must be explicit.'],section='XXI')
rec('Opposition perfection, occurrence versus benefit',[159],
    'Sometimes perfected by opposition when there is mutual reception by domicile, friendly houses, and Moon separates from the quesited significator and presently applies to the Ascendant lord. Lilly rarely sees perfection this way without the querent better off had it not happened.',
    ['Mutual reception by HOUSE, friendly houses, directed Moon transfer.'],
    ['Retain the tension with XIX\'s broad easy-reception assertion; no retrospective preferred rule.'],section='XXI')
rec('Opposition regret examples',[159],
    {'marriage':'Perfection can coexist with continual quarrelling and blame for the choice.',
     'money':'A promised debt/portion is obtained, but legal costs exceed its value.'},
    limits=['Examples separate event attainment from net benefit; not relationship-safety or financial advice.'],section='XXI',kind='author_examples')
rec('Translation perfection prerequisites',[159,160],
    'Principals have separated from conjunction, sextile or trine. A third planet separates from one who receives it by domicile, triplicity OR term, then applies to the other before meeting ANY other conjunction or aspect.',
    ['Reception direction is source principal receiving intermediary.','No intervening encounter.'],
    ['Do not silently add face/exaltation to this locally enumerated list or omit reception by borrowing the shorter XIX definition.'],section='XXI')
rec('Translation identifies practical mediator',[160],
    'The translating planet or its represented person brings the matter to perfection; its house rulership identifies means: second lord a purse, third lord kin or neighbour.',
    limits=['The intermediary\'s role is not another independent natal character score.'],section='XXI')
rec('Collection prerequisites and direction',[160],
    'Principals do not behold each other; both cast aspects to a planet heavier than both; BOTH PRINCIPALS RECEIVE THAT COLLECTOR in their essential dignities. The common mediator completes what they cannot arrange themselves.',
    limits=['Do not silently reverse to collector receives principals. Actual application/event order and mixed dignity cases need specified conventions.'],section='XXI')
rec('House dwelling alone rejected',[160,161],
    'Ancients infer attainment when topic significator dwells in Ascendant, such as tenth lord for an office. Lilly rejects this alone unless the Moon also transfers the desired matter\'s light to the Ascendant lord.',
    limits=['Retain rejected claim as attributed/rejected, not an extra positive rule.'],section='XXI',kind='qualified_rejection')
rec('Application inclination versus separation privation',[161],
    'Applying principals show willingness and continued negotiation/probability of perfection; separation generally deprivation/little hope, notwithstanding favourable dwelling.',
    limits=['Inclination or further treaty is not identical to accomplished outcome; translation/collection routes retain their own prerequisites.'],section='XXI')
TOPIC_BASE = ['querent','estate','kindred','father','children','servant/sickness','wife','manner of death','religion/journeys','esteem/honour','friends','secret enemies']
PARTNER_RELATIVE = ['person','estate','brethren/kindred','father','children/fertility','sickness/servants','sweetheart','death','journey','mother','friends','sorrow/care/private enemies']
HOUSE_EXAMPLES = {'base_topics':TOPIC_BASE,'partner_origin':7,'partner_topics':PARTNER_RELATIVE,
 'partner_radical_houses':[7,8,9,10,11,12,1,2,3,4,5,6],
 'minister_or_wifes_brother_origin':9,'king_asked_about_origin':10,'asker_origin_regardless_rank':1,'natal_native_origin_regardless_rank':1}
rec('Querent house topics',[161],dict(enumerate(TOPIC_BASE,1)),limits=['No event or clinical inference from the mapping alone.'],section='XXI',kind='table_row_group')
rec('Seventh-house subject turned topics',[161],HOUSE_EXAMPLES,
    limits=['Relative tenth is called mother in this example, whereas radical tenth above is esteem/honour. Do not assume all semantic labels rotate identically.'],section='XXI',kind='worked_mapping')
rec('General turning and role-dependent origin',[161,162],
    'Subject house becomes first and following houses second etc. Minister or wife\'s brother uses ninth; king asked about tenth. But a king AS ASKER uses the Ascendant, and nativities use the native\'s Ascendant, king or beggar.',
    limits=['Do not turn every royal natal chart from the tenth. Relative indices and ordinal counts must be explicit.'],section='XXI',kind='method_and_examples')
rec('End of introduction and postponed Fortune calculation',[162],
    'Learning is to recognise error and when to judge, not memorize every word. Fortune calculation is postponed to the first example, with author criticism of its treatment elsewhere.',
    limits=['Do not import a Fortune formula and attribute it to this passage; Book II examples remain unread.'],section='XXI',kind='scope_boundary')

ISSUES = [
 ('orb_profiles',[141,144],'Two printed orb columns and worked examples choose differently; no outcome-conditioned switching or merged profile.'),
 ('partile_precision',[140,142],'Exact degree/minute language does not specify a universal numerical tolerance.'),
 ('platick_boundary',[141],'Within at exactly a moiety limit requires an explicit convention.'),
 ('event_order',[141,145,147],'Positions and qualitative speed are not a complete astronomical sequence; no invented velocities.'),
 ('initial_separation',[144],'Six-minute initial separation versus full clearance; sub-six-minute state not resolved.'),
 ('timing_unit',[144],'Remaining degrees can mean days/weeks/months/years; selection and mixed-condition rules missing.'),
 ('reception_tension',[146,159],'Easy sudden reception conclusion versus narrow opposition perfection with regret; retain both.'),
 ('reception_examples',[146],'Use declared degree tables and day/night qualification; ordinal versus continuous conventions separate.'),
 ('void_application',[146,156],'Application within sign versus exact perfection within sign is not automatically equivalent.'),
 ('hayz_night',[147],'Printed nocturnal clause requires below earth; no silent school-based correction.'),
 ('combust_ten_degree',[147],'Second example has ten degrees separation while definition gives eight-and-a-half.'),
 ('solar_boundaries',[147,148],'Threshold equality, sign boundaries for beams/cazimi and nested-zone scoring precedence not fully specified.'),
 ('visibility_proxy',[148],'Orientality language includes rising/visibility; a longitude-only proxy is not full observational astronomy.'),
 ('stationary_duration',[148],'Multi-day stationary language is approximate; no speed tolerance stated.'),
 ('strength_aggregation',[149,150],'OR clauses, both/either benefic contacts, repeated contacts and overlapping conditions lack complete aggregation instructions here.'),
 ('fixed_star_epoch',[149],'Historical positions and Algol-only five-degree clause; contemporary positions and other orbs are not supplied.'),
 ('degree_ordinals',[150,151,152],'Printed terminal ordinal degrees must not silently become continuous longitude bins.'),
 ('capricorn_s15',[150],'Raw s15 light-table label left unresolved, rather than repaired to sm.'),
 ('virgo_l27',[150],'Provisional l27 light-table reading; not accepted as a certain discriminator.'),
 ('azimene_retrosearch',[152],'Observed condition triggers explanatory search; this procedure cannot count as an untouched forward prediction.'),
 ('fortune_column',[152],'Fifth-column reference differs from sixth when counting the sign column.'),
 ('body_ink',[153],'Cancer Mars and Cancer Sun cells are ink-altered; handwriting is not assured author text.'),
 ('body_token',[153],'Leo/Mars middle word and Libra/Venus abbreviated mal.guts not silently normalized.'),
 ('body_rationale',[154,155],'Short domicile sequence does not fully regenerate the 84-cell table or its multiple entries.'),
 ('moon_count',[155],'Aries is called ninth from Cancer: offset nine, inclusive ordinal ten.'),
 ('radicality',[155,156],'Triplicity/nature alternatives and scope need explicit implementation; no automatic natal exclusion.'),
 ('age_exceptions',[156],'Very-young/corresponding-age and degree boundaries are not supplied numerically.'),
 ('seventh_topic',[156,157],'Artist caution has a non-seventh-topic condition; avoid universal misapplication.'),
 ('defer_balance',[157],'Equal testimonies require deferral; no numerical balancing or unqualified tie-breaker provided.'),
 ('cosignificator_attribution',[158],'Explicit rejection of separated planet must not be widened to adjacent reported applying-planet practice.'),
 ('translation_local_scope',[145,160],'XXI locally enumerates domicile/triplicity/term reception and no intervening contact beyond XIX summary.'),
 ('collection_direction',[160],'Printed both receive him fixes direction; do not reverse it to match a familiar summary.'),
 ('dwelling_qualification',[160,161],'Lilly rejects dwelling-only perfection without lunar translation.'),
 ('derived_semantics',[161,162],'House arithmetic rotates; all semantic labels are not identical, and subject versus asker determines origin.'),
 ('inconjunct_omissions',[143],'Raw 32-entry table is smaller than 48 geometric non-aspect directions; omissions preserved, not repaired.'),
 ('source_table_uncertainty',[150,153,154],'A complete inventory of observed cells is not a claim that every damaged character has been resolved.')]
COMPARISONS = [
 {'id':'B02d-C1','source':'Lilly XIX printed114 / Rhetorius Holden ch41 printed24',
  'finding':'Lilly\'s local besieging definition is between malefic bodies; Rhetorius explicitly includes aspect-pattern besieging, no intervening ray and seven-degree front/rear limits.',
  'disposition':'Different locally stated conditions; neither silently substitutes for the other; no empirical independence claim.'},
 {'id':'B02d-C2','source':'Lilly XIX printed110 / Rhetorius Holden ch37 printed23',
  'finding':'Lilly distinguishes initial six-minute separation from total moiety clearance. Rhetorius\'s short definition simply says passing the other degree bodily or by aspect.',
  'disposition':'Difference between these local definitions only, not a claim about the complete Rhetorius chapter109-110 treatment.'}]

if __name__ == '__main__':
    rules={'schema_version':2,'batch_id':'B02d','records_count':len(RECORDS),'first_record_number':392,'last_record_number':391+len(RECORDS),'records':RECORDS}
    aspects={'source_id':SID,'source_sha256':SHA,'pdf_pages':[142,143], 'sign_names':SIGNS,'aspect_rows':ASPECT_ROWS,
             'not_beholding_raw':dict(zip(SIGNS,INCONJUNCT_RAW)), 'raw_directed_entries':sum(map(len,INCONJUNCT_RAW))}
    for name,obj in [('RULES.json',rules),('ORB_PROFILES.json',ORBS),('STRENGTH_ROWS.json',WEIGHTS),('DEGREE_TABLE.json',DEGREES),
                     ('BODY_TABLE.json',BODY),('ASPECT_TABLES.json',aspects),('HOUSE_EXAMPLES.json',HOUSE_EXAMPLES),
                     ('UNRESOLVED.json',{'issues':[{'id':'B02d-U%02d'%i,'topic':k,'pdf_pages':p,'issue':v} for i,(k,p,v) in enumerate(ISSUES,1)]}),
                     ('CROSS_SOURCE_COMPARISONS.json',COMPARISONS)]:
        save(name,obj)
    print('SOURCE_RECORDS',len(RECORDS),'LAST',391+len(RECORDS),'WEIGHT_ROWS',len(WEIGHT_ROWS),'UNRESOLVED',len(ISSUES))
