import json,hashlib
from pathlib import Path
Q=Path('/workspace/scratch/43f75264c32e/b02l-workers/independent')
P=Path('/workspace/scratch/43f75264c32e/review-candidate-b02l-01')
def write(name,value):
 (Q/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def digest(path):
 b=path.read_bytes();return {'path':str(path),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
sf=json.loads((Q/'SOURCE_FIRST_MAP.json').read_text())
rules=json.loads((P/'RULES.json').read_text())['rules']
byid={int(r['id'].rsplit('R',1)[1]):r for r in rules}
findings=[
 {'id':'IF-01','classification':'source_record_grammatical_number_mismatch','importance':'substantive source fidelity repair','candidate_locations':['RULES.json: R1560/A011 title, source_statement, prerequisites[0].source_clauses[1], qualifications_and_limits[0], and duplicated source_fields proposition/conditions/uncertainties'],'source_units':['SF-011'],'report_claims':[],'pdf_pages':[294],'printed_pages':[260],'source_anchor':'or from the principall Significators in the Figure','candidate_reading':'principal significator / principal Significator (singular)','diagnosis':'The original visibly prints Significators, plural. The candidate narrows that named source group to a singular significator. The repeated from and its grammatical ambiguity are otherwise retained.','repair':'Restore plural significators in every affected canonical field and its duplicate, while preserving the existing uncertainty about how the alternatives attach. The plural does not establish a new all-of-group or vote-count rule.','evidence_files':['diagnostic_pdf294_principal_number.png'],'certainty':'The printed plural s is directly legible in an enlarged original-PDF crop.'},
 {'id':'IF-02','classification':'report_quantifier_and_exclusion_drift','importance':'substantive source meaning repair','candidate_locations':['AUDIT_REPORT.md: outward-cause paragraph','CLAIM_LEDGER.json: C10 text and regenerated hash'],'source_units':['SF-013'],'report_claims':['C10'],'pdf_pages':[294],'printed_pages':[260],'source_anchor':'either Saturn or Mars ... and neither of them be Lords of the sixt, or Dispositors of the Moon','candidate_reading':"the afflicting planet is neither the sixth lord nor the Moon's dispositor",'diagnosis':'The report restricts the exclusions to the actual afflictor. The source says neither of the two planets. A case where Mars afflicts but Saturn rules the sixth would pass the report paraphrase while failing the printed exclusions. R1562 correctly preserves neither of those two, so this is report/ledger drift.','repair':'Say that neither Saturn nor Mars is lord of the sixth or dispositor of the Moon. Retain the strength and square/opposition conditions and the unwell/yet-not-perfectly-sick distinction. R1562 does not need alteration.','evidence_files':['/workspace/scratch/43f75264c32e/source-work/pdf294.png'],'certainty':'Explicit neither of them after the Saturn/Mars pair.'},
 {'id':'IF-03','classification':'report_callback_referent_error','importance':'substantive source meaning repair','candidate_locations':['AUDIT_REPORT.md: earlier timing callback paragraph','CLAIM_LEDGER.json: C35 text and regenerated hash'],'source_units':['CX02 (earlier original source context)'],'report_claims':['C35'],'pdf_pages':[283,301],'printed_pages':[249,267],'source_anchor':'according to the nature and quality of the Signe','candidate_reading':"The earlier timing passage on printed249 ... left a choice among months, weeks and days to the disease's nature.",'diagnosis':'Printed249 attaches the selector to the sign, not the disease. The later printed267 discussion does use disease quality/nature and discretion. The report conflates these distinct selectors. The retained R1438 excerpt is already correct.','repair':"Describe the earlier callback as referring to the sign's nature and quality; distinguish the later disease-quality/discretion qualifications. Preserve the conclusion that these passages do not supply a new combined numerical algorithm.",'evidence_files':['pdf283_earlier_context.png','/workspace/scratch/43f75264c32e/source-work/pdf301.png'],'certainty':'The earlier original clause explicitly names the Signe.'},
 {'id':'IF-04','classification':'point_of_use_source_locator_incomplete','importance':'citation repair','candidate_locations':['AUDIT_REPORT.md: inward-cause paragraph source citation','CLAIM_LEDGER.json: C09 original_pdf_pages and bound text as needed'],'source_units':['SF-009','SF-010'],'report_claims':['C09'],'pdf_pages':[293,294],'printed_pages':[259,260],'source_anchor':'any Planet may in [page break] this case be malignant, if he be Lord of the eighth, twelfth or sixt','candidate_reading':'C09 cites only Original PDF293/printed259.','diagnosis':'The semantic statement is supported, but the sixth/eighth/twelfth lordship list is on PDF294/printed260 after the page break. R1559 correctly locates the two-page span.','repair':'Add PDF294/printed260 to the report citation and ledger page list.','evidence_files':['/workspace/scratch/43f75264c32e/source-work/pdf293.png','/workspace/scratch/43f75264c32e/source-work/pdf294.png'],'certainty':'Visible physical page break.'},
 {'id':'IF-05','classification':'report_reference_frame_precision','importance':'wording precision repair','candidate_locations':['AUDIT_REPORT.md: natal/mundane callback paragraph','CLAIM_LEDGER.json: C24 text and regenerated hash'],'source_units':['SF-073'],'report_claims':['C24'],'pdf_pages':[300],'printed_pages':[266],'source_anchor':'the Signe of the eighth House of the yearly revolution of the World','candidate_reading':'the eighth sign of the yearly revolution of the World','diagnosis':'The report drops House from the source relationship. In context it likely intends the right frame, and R1629 is correct, but eighth sign is less precise and can be mistaken for an ordinal zodiac sign. This review does not claim the report explicitly says Scorpio.','repair':'Use the sign of the eighth house of the yearly revolution of the World.','evidence_files':['/workspace/scratch/43f75264c32e/source-work/pdf300.png'],'certainty':'Explicit eighth House in the source; the risk lies in the report abbreviation.'},
 {'id':'IF-06','classification':'report_consequence_connector_precision','importance':'wording precision repair','candidate_locations':['AUDIT_REPORT.md: no-sickness chain paragraph','CLAIM_LEDGER.json: C08 text and regenerated hash'],'source_units':['SF-006','SF-007','SF-008'],'report_claims':['C08'],'pdf_pages':[293],'printed_pages':[259],'source_anchor':'they were not sick, or that no sicknesse would succeed upon this Quere, but that their mistrust ... was grounded upon some sudden distemper of Body','candidate_reading':'distinct conclusions—no sickness, no following sickness, or a present distemper soon rectified','diagnosis':'The final or makes the explanatory transient-distemper clause look like a third alternative. The source gives alternative no-sickness judgments followed by an explanation of the suspicion. R1557 preserves that connection correctly.','repair':'Describe the alternative judgments of no present or ensuing sickness together with the explanation that suspicion arose from a sudden bodily distemper soon rectified. Keep the opening negative-scope uncertainty.','evidence_files':['/workspace/scratch/43f75264c32e/source-work/pdf293.png'],'certainty':'The conjunction is visible; this is a report relationship/precision correction, not a claim that an extra patient outcome has been fabricated.'}
]
self_corrections=[
 {'id':'SC-01','source_unit':'SF-026','frozen_reading':'viscous','source_adjudicated_reading':'vitious','candidate_locations':['R1578','C14'],'disposition':'The candidate is correct. The frozen source-first anchor and assertion misread the word. Preserve the freeze unchanged and use vitious in this diagnosis.','evidence_file':'diagnostic_pdf295_vitious_reading.png','pdf':295,'printed':261},
 {'id':'SC-02','source_unit':'SF-019','frozen_reading':'the man he longs after','source_adjudicated_reading':'the man she longs after','candidate_locations':['R1569'],'disposition':'The candidate is correct. The error is in the source-first anchor; the source-first paraphrase was mostly neutral. Preserve the freeze unchanged and use the printed she.','evidence_file':'diagnostic_pdf295_youth_pronoun.png','pdf':295,'printed':261}
]
interpretations=[{'id':'IC-01','source_units':['SF-045'],'candidate_records':['R1600','R1601'],'issue':'Fire-sign context in the Venus/Mars continuation','source_anchor':'Venus in fiery Signes ... but if Mars joyne in signification','assessment':'The candidate explicitly identifies the fiery condition as inherited from the preceding description, a plausible connected reading. The source-first map left its inheritance unresolved because the condition is not repeated. I do not treat the candidate as having silently invented a condition, but neither does the source explicitly repeat it.','retained_uncertainty':'Whether the fiery condition is intended to govern the Mars branch. No one-day duration is transferred; no physical conjunction is asserted.','could_settle':'A corresponding directly inspected authorial source or explicit textual clarification. This is not an additional acceptance gate.','optional_precision':'The qualification could state that the fire-sign context is inherited rather than separately repeated.','definite_candidate_defect':False}]
write('DIAGNOSTIC_FINDINGS.json',{'candidate_manifest_sha256':'41a5d97ba5c0a560c16fedbcfd24d8bd09a185b116d5d884374881f5194cbf48','findings':findings,'self_corrections':self_corrections,'interpretive_differences':interpretations,'clinical_accuracy_claim':False})
map_nums=[
[1550],list(range(1551,1558)),[1551,1552,1553],[1554,1555],[1556],[1557],[1557],[1557],[1558],[1559],[1560],[1561],[1562],[1563],[1564,1565],[1566],[1567],[1568],[1569],[1570],[1571,1572],[1573],[1574,1575],[1576],[1577,1578],[1578],[1579],[1580],[1581],[1582],[1583],[1584],[1585],[1586],[1587],[1588],[1589,1590],[1591],[1592,1593],[1594],[1595],[1596],[1597,1598],[1599],[1600,1601],[1602],[1603],list(range(1604,1610)),[1604],[1605,1606],[1607],[1608],[1609],[1610],[1611],[1612,1610],[1613],[1614],[1615],[1616],[1617],[1618],[1619],[1620],[1621],[1622],[1623],[1624],[1625],[1626],[1627],[1628],[1629],[1630],[1631,1632],[1633],[1634],[1635],[1636,1637],[1638],[1639],[1640],[1641],[1642],[1643],[1644],[1645],[1646],[1647],[1648],[1649],[1650]]
notes=[
'Heading, full italic introduction, abridgement claim and shorter-method comparison are retained in R1550.',
'The sickness-question heading is retained in section metadata and the coverage unit; it need not be a separate claim record.',
'Querent significator, contrary nature, Mars/hot-dry versus Cancer/cold-moist illustration, separate cadency alternative and emphasis on sixth are all retained across three records.',
'Diurnal significator below earth, adverse predicate cluster and qualified nocturnal transfer are preserved without forcing a Boolean grouping or an inversion.',
'Lilly first-person practice, questions with or without urine and prior figure erection are retained.',
'Full opening adverse/negative chain is present; no added negative; sixth-lord object/role ambiguity remains.',
'All later favourable or unafflicted alternatives are retained, including node, Sun, Moon/ascendant-lord, benefics and cusp targets.',
'R1557 has the alternative no-sickness conclusions plus explanatory distemper/rectification. Report C08 needs connector precision (IF-06).',
'Inward disposition, sign, house/place and good-or-ill configuration with malevolents are retained, without narrowing to bad aspects only.',
'Any-planet MAY malignancy and eighth/twelfth/sixth lordships retained across page break. C09 citation needs PDF294 (IF-04).',
'Outward-source alternatives and repeated-from ambiguity are preserved, but principal Significators has been made singular (IF-01).',
'Essential strength, swiftness and good house remain conjunctive context; accidentally/outwardly afflicted versus naturally ill remains distinct.',
'R1562 keeps either Saturn/Mars square/opposition, prior strength, neither planet holding either excluded role, MAY, outward cause and not-perfectly-sick. C10 weakens the exclusions (IF-02).',
'Occupied or ruled house of the afflictor and reliance on house judgments are retained.',
'Second-lord affliction and absence of inward cause retained; application=current want, separation=recent harm/loss remain separate.',
'Magnitude depends on afflictor strength and aspect quality; opposition worse than square or conjunction is retained as local, not a universal weight.',
'Fifth lord good or ill, evil diet/surfeit, games capacity, father/pension alternative and youth/distemper parenthesis with uncertain reach are retained.',
'Seventh-lord affliction, spouse reciprocity, lawsuit, neighbour contention or partner alternatives are retained as general examples.',
'Youth, the like seventh-to-first configuration, friend/maid/man alternatives, discontent and no-following-sickness conclusion retained. Candidate correctly prints she; see SC-02.',
'First-person usual/accustomed practice statement remains an experience claim without case count or endpoint.',
'Prior explanation callback, didactic aim, figure erection and disease-significator selection are retained; catalogue context is explicit.',
'Saturn disease-author context and tedious/protracted diseases are retained with historical terms.',
'Leo/Scorpio, both node glyphs, unresolved reach of with, combustion/violent-star alternatives, and suspicion-conditioned poison inference are retained.',
'Fire-sign examples and usually hectick-fever modality are retained; original body and errata agree on usually.',
'Water-sign cold/moist cause, more-assured qualifier and Venus/Moon co-signification are retained; continuation attachment remains open.',
'The symptom sequence, long paroxysms, ebb/flow, almost-overwhelmed qualifier, fear and cold are retained. Candidate vitious is correct; source-first viscous was wrong (SC-01).',
'Fixed class with exactly the three printed examples, durable/long-continued fevers, pectoral rottenness or dry coughs, joint gout, leprosy or general scabbiness, and all manner of gout are retained without inserting Scorpio.',
'Saturn in moveable signs, the four named examples in source order, general flux throughout the body and PRINCIPALLY dropsy or tympanical humours are retained.',
'Saturn in common signs: NOT one humour alone, many changes/receding/reverting, YET long continuation; no retrograde condition or numerical duration is added.',
'Jupiter disease-author context, liver and blood source terminology are retained.',
'Jupiter as disease author in Cancer OR a moist sign gives waterish OR too-thin blood; the named sign and qualitative alternative are retained.',
'Jupiter as disease author in Aries, Leo or Sagittarius gives overheated blood from excess heat OR choler; all three signs and alternatives are retained.',
'Jupiter as disease author in Aquarius, Libra or Gemini gives too much/overflowing blood; opening a vein OR sweating as necessary is retained as historical documentary language.',
'Jupiter as disease author in Taurus, Capricorn or Virgo gives melancholy-infected, too-gross AND not-fluent blood; no Saturn-placement condition is added.',
'Jupiter fiery-sign fevers proceed from blood YET without rottenness OR much putrefaction; the negative qualification is retained.',
'Mars joined with the Sun gives a distempered fever from putrefaction of blood; joined remains the printed relation, with no precise orb supplied.',
'Mars hot/dry choleric account retained; Saturn mixture qualifies melancholy; the his dignities possessive stays uncertain.',
'Common-sign Mars recurrence/apparent departure and lack of stable course are retained.',
'At apparent departure, Saturn signification plus aspect with good PLANETS is preserved; no extra good-ASPECT requirement. Sixth/eighth-lord alternative says MAY expect death, not observed death.',
'Usually, common-sign Mars, many ACUTE infirmities, returning at expected amendment, sudden motions and quicker critical days toward good OR ill according to the significator are retained; returning agrees with errata.',
'Mars under-beams/local-house/fire conditions and fever intensification remain attached to their alternatives.',
'Opening PDF297 planet is Mars; fever cause AND Leo, boiling humours, continual burning fevers and origin in great veins near the heart are retained.',
'First lying-down time, Sun relations to Saturn including antiscion, and Mars aforesaid-aspects callback are retained without silently settling Mars antiscion scope.',
'Venus general disease-author/cause context and awkward Gluttony of connector are retained without unauthorised emendation.',
'One-day Venus fiery fever and Mars co-signification variant are separated; no duration or physical conjunction is imported. Fire-condition inheritance is explicit contextual reading, with IC-01 retained.',
'Mercury must be unfortunate AND disease author; consequences retained as historical descriptions.',
'Ninth lord in sixth plus existing mistrust are retained; occult-cause reading is not treated as independent proof.',
'The right/left/member heading is retained in section metadata and the coverage unit.',
'Sixth lord unfortunate/afflicted above earth gives right and upper parts; later masculine requirement is not imported backwards.',
'Under-earth OR vitiated diurnal-sign case visibly superiour/fore-part; nocturnal continuation retained with inherited-scope uncertainty.',
'Feminine disease significator and separate feminine aspected planet in feminine sign OR house are retained; feminine-house definition remains dependency.',
'First-person masculine/above-earth experience claim retains its distinct extra condition and source modality, without case count.',
'Few/middle/lower degrees refer to member regions; no numerical bins, whole-body scale or silent inherited-condition certainty is supplied.',
'Introductory spirit/member role allocation and explanation are retained; Sun-house lord is distinct from Sun itself.',
'All-afflicted ascendant, Sun and Moon role group gives disease throughout the whole body, with no place free; the whole-body quantifier is retained.',
'Sun/Moon dispositors OR ascendant lord OR two at least, spirit disease and some mental indisposition are retained with raw counting ambiguity and the ascendant-lord/Moon-dispositor animal-faculty explanation; no global reconciliation is imposed.',
'Ascendant, Moon, Sun-house lord all-or-two impedance quantifier is retained as a different group.',
'Both ascendant AND Moon unfortunate, with ascendant lord AND Moon dispositor free, gives mental and NOT bodily indisposition; all four local conditions and polarity are retained.',
'Many astrologians attribution, Saturn foreshows OR causes melancholy and role branches are retained as reported historical claims.',
'Saturn sequence of relevant lordships/placements/conjunctions/infortunes and mind/soul consequences is preserved, including alternatives.',
'Jupiter glyph, contrary-hereof reference and never-mind/but-body polarity retained; antecedent transfer not fabricated.',
'Plural ruler/dispositor affliction alternatives and unclear distribution retained without requiring an invented mixed-condition rule.',
'Ascendant-lord dispositor and Moon dispositor comparative case remain second-order/local roles, not substituted ascendant lord or Moon.',
'Mars sextile/square/opposition and twelfth-house attachment uncertainty are retained, not repaired to conventional malefic aspect list.',
'Malevolent ascendant aspect AND not-to-Moon exclusion AND afflicted Sun-sign lord are retained.',
'More-afflicted degrees versus their lords and reversed comparison are both retained; no weights, tie or score supplied.',
'Exalted Sun/ascendant lord versus Moon-dispositor debility context is retained with all local conditions.',
'Compound debility clauses and freedom-from-Saturn/Mars phrase retain unresolved grouping and omitted subject.',
'Compressed Sun/ascendant/hour/twelfth roles and usually character account are retained; candidate preserves appositional/rulership uncertainty.',
'Venus role and character account retained without adding an affliction requirement absent from this sentence.',
'Mercury explicit affliction and role/pronoun shifts are retained without converting to a modern character diagnosis.',
'Optional nativity, birth degrees, eclipse/great conjunction and near-sickness matching remain conditional with no invented match/tolerance.',
'Eclipse/conjunction sign and eighth-HOUSE sign of yearly WORLD revolution in natal angles, especially ascendant, retained. C24 drops House (IF-05).',
'Ascendant sign at first sickness OR patient demand matched to natal infortune sign is kept separate from crisis hierarchy.',
'Inclusive six plus applying/not-yet-perfect phase and Aries/Leo mitigation retained; separate exact-twelve little-danger wording not made >=12/no-danger.',
'Other astrologians and excellent works/public availability are authorial reference claims, not proof that any particular external work was collated.',
'Nearest obtainable first-bed hour, only-if-unavailable physician-request fallback, and Moon rectification retained; earlier urine/access hierarchy remains distinct.',
'Acute NOT chronic, near times and only 45/90/135-degree displacements retained; no date, tolerance or 180-degree completion invented.',
'Good aspect AND benevolent planet versus ill aspect of eighth/sixth lord retained; latter worsening/pain/medicine continuation crosses page break.',
'Lilly usual/no-remembered-failure recollection retains all hard-aspect targets and medicine qualifiers; no numerator, denominator or case endpoints inferred.',
'Pronouncing comfort/relaxation or interval of ease for Moon trine/sextile to first/eleventh/ninth/tenth lords is kept as prognostic act, not verified cure.',
'Ascendant-lord good Sun aspect, NOT(power OR dominion) with pronoun uncertainty and mental-relief outcome retained.',
'Recovery already judged and timing requested precede degree count, both bodies houses/signs and discretion/disease quality; exact distance operation remains unspecified.',
'Moveable-sign days ordinarily and greater certainty if swift AND angular retained; event is amendment, not necessarily cure.',
'Common-sign application declines mechanical month/week/day judgment, using disease nature and feasible duration with discretion.',
'Ancients attributed mapping: moveable days, common weeks OR months, fixed months OR years; alternatives retained.',
'Angular/moveable, succedent/common, cadent/fixed equivalences retained with no priority over conflicting actual signs.',
'Moon speed, sign and quality together with principal significators; mix all considerations, without numerical formula.',
'Ascendant lord leaves sign at question time into sign giving essential dignity; recovery OR sensible benefit retained; no extra outgoing-debility rule.',
'Exactly 28 degrees AND common sixth cusp, vary, strictly less than two weeks; no >=28, exact date, recovery guarantee or observed case.',
'Forward promise of one or two practical figures retained as future dependency; no charts from that promise counted here.',
'Full final Hermes bridge retained through Judgments of this House: variety, sickness burden, health delight, endeavoured Englishing/insertion, esteem and house relevance; lower heading excluded.'
]
assert len(map_nums)==92 and len(notes)==92,(len(map_nums),len(notes))
coverage=[]
for unit,nums,note in zip(sf['source_units'],map_nums,notes):
 u=json.loads(json.dumps(unit));status='represented_with_conditions_and_qualifications'
 if u['id']=='SF-011':status='represented_but_source_number_repair_required'
 if u['id'] in ['SF-002','SF-048']:status='heading_represented_in_metadata'
 if u['id']=='SF-019':u['point_of_use']['anchor_excerpt']=u['point_of_use']['anchor_excerpt'].replace('the man he longs after','the man she longs after')
 if u['id']=='SF-026':
  u['point_of_use']['anchor_excerpt']=u['point_of_use']['anchor_excerpt'].replace('viscous','vitious');u['source_assertion']=u['source_assertion'].replace('viscous','vitious')
 coverage.append({'source_unit':u,'source_first_freeze_unchanged':True,'candidate_records':[byid[n]['id'] for n in nums],'candidate_point_of_use':[{'id':byid[n]['id'],'pdf_pages':byid[n]['source_locator']['pdf_pages'],'anchor':byid[n]['source_locator']['passage_anchor']} for n in nums],'diagnostic_status':status,'clause_and_qualification_check':note,'finding_ids':[x['id'] for x in findings if u['id'] in x['source_units']],'self_correction_ids':[x['id'] for x in self_corrections if x['source_unit']==u['id']]})
reverse=[]
for r in rules:
 num=int(r['id'].rsplit('R',1)[1]);linked=[c['source_unit']['id'] for c in coverage if r['id'] in c['candidate_records']]
 reverse.append({'record_id':r['id'],'local_id':r['local_id'],'source_units':linked,'pdf_pages':r['source_locator']['pdf_pages'],'anchor':r['source_locator']['passage_anchor'],'fields_reviewed':['title/source_statement','prerequisites','consequent','exceptions_and_modifiers','qualifications_and_limits','attribution/evidence','dependencies','implementation limits','source_fields duplicates'],'status':'source_number_repair_required' if num==1560 else 'represented_and_source_compared','finding_ids':['IF-01'] if num==1560 else []})
assert len(reverse)==101 and all(r['source_units'] for r in reverse)
write('SOURCE_RECORD_COVERAGE.json',{'candidate_manifest_sha256':'41a5d97ba5c0a560c16fedbcfd24d8bd09a185b116d5d884374881f5194cbf48','source_first_map_sha256':digest(Q/'SOURCE_FIRST_MAP.json')['sha256'],'source_unit_count':92,'candidate_record_count':101,'units_without_candidate_representation':[],'candidate_records_without_source_mapping':[],'segmentation_note':'The 92 source-first units and 101 candidate records are different editorial segmentations, not independent prediction counts. Two source headings are represented by metadata; several source units are split into adjacent records.','source_to_records':coverage,'records_to_source':reverse,'self_corrections':self_corrections,'interpretive_differences':interpretations,'local_argument_architecture':sf['local_argument_architecture'],'actual_evidence_inventory':sf['actual_evidence_inventory'],'earlier_callback_diagnosis':{'CX01':'Original PDF277 timing hierarchy compared to retained R1359-R1361 and kept distinct from the local PDF300 method.','CX02':'Original PDF283 and retained R1438 agree on sign nature/quality; report C35 misattributes that selector to disease nature (IF-03).'},'overall':'Every local source unit has candidate representation. One record-level plural/singular mismatch needs repair; report-level issues are separately identified. This is not an unqualified clean-fidelity or accuracy finding.'})
ledger=json.loads((P/'CLAIM_LEDGER.json').read_text())
claim_checks={
'C01':[
('Exact start at DARIOT Abridged and the complete italic introduction on PDF292/printed258','supported'),
('Complete upper ending through Judgments of this House on PDF302/printed268, stopping above divider','supported'),
('Every intervening local section has representation','supported; one represented record has IF-01 number repair'),
('Chapter XLIV incomplete and lower Hermes heading next','supported')],
'C02':[
('New inventory is 101 contiguous records, R1550-R1650','supported'),
('Cumulative Lilly inventory is 1650, from prior1549 plus101','supported against retained/new indexes'),
('Retained Ptolemy inventory is1066','supported against supplied numeric snapshot/hash; no new Ptolemy source audit'),
('Combined 1650+1066=2716','supported by independent arithmetic'),
('All101 are general/method/illustrative rather than worked narrative','supported by kinds and source inventory'),
('Worked-narrative/dated-enquiry/horoscope-figure counts are0/0/0','supported by the entire original local span'),
('Nine editorial units and eleven main-span pages','supported'),
('42 typed register entries','supported by actual item count'),
('36 retained limits/anomalies and6 source-resolved entries','supported by actual status count'),
('20 actual distinct focused tests passed','supported by receipt, source code and private repeat'),
('Record counts are not independent predictions; register counts are not source errors','supported evidence classification'),
('Confirmed glyphs can coexist with unresolved grammar','supported by node and Mars-sextile cases')],
'C03':[
('Nine coverage-table rows have correct page spans and record ranges','supported; row checks below'),
('The units divide a continuous span and are not nine numbered chapters','supported'),
('Four earlier timing records are retained without new counting','supported: R1359-R1361 andR1438')],
'C04':[
('Historical source audit, no assessed patient, treatment, survival probability or personal forecast in this bundle','supported by content inspection'),
('Historical disease/humour/spirit/mind terminology not mapped to modern diagnoses','supported by records and helper limits'),
('Data and helper marked reference-only outside prediction runtime','supported as candidate flags and bounded code; external deployment not independently observed'),
('Predictive accuracy unevaluated','supported by absence of empirical evaluation')],
'C05':[
('Introduction favours Dariot method and offers abridged material','supported'),
('Heading supplies abridgement context, not universal verbatim Dariot attribution','supported'),
('Marginal Dariot/Lilly shifts and first-person contributions occur','supported on original images'),
('Unlabeled sentence-level authorship remains uncertain','supported source limit'),
('Ancients separately attributed and extraction retains author distinctions','supported')],
'C06':[
('Object is Lilly1647 English presentation','supported'),
('No independently selected original Dariot collation is claimed','supported scope statement; no such collation in reviewed evidence'),
('Final upper paragraph announces Hermes material and editorial rationale','supported'),
('Variety, burden of sickness, delight of health, reported esteem and sixth-house relevance all appear','supported'),
('These are reported literary/reception claims, not ancient-authorship or clinical corroboration','supported evidence distinction')],
'C07':[
('Querent significator distinct from later disease significator','supported'),
('Mars ascendant lord hot/dry in cold/moist Cancer','supported'),
('Cadency is separate alternative, sixth emphasized','supported'),
('Diurnal significator below earth and mixed adverse conjunction/alternatives','supported with grouping unresolved'),
('Nocturnal transfer qualified and no mechanical inversion enumerated','supported')],
'C08':[
('Lilly own practice, question with or without urine','supported'),
('Opening explicitly not-afflicted ascendant followed by adverse lord OR clauses','supported'),
('Later favourable or unafflicted alternatives occur','supported'),
('Reach of negative is unsettled; no extra negative or unique executable polarity','supported'),
('No sickness/no following sickness/distemper presented as three alternatives','precision repair IF-06; recordR1557 is correct')],
'C09':[
('Inward disposition, sign, house/place and good OR ill malevolent configuration','supported'),
('Any planet MAY be malignant through sixth/eighth/twelfth lordship','supported'),
('This is role/context sensitive; permanent benefic status or bad-aspects-only loses wording','supported reasoning from source'),
('Point-of-use citation onlyPDF293','citation repair IF-04; house list continuesPDF294')],
'C10':[
('Strong essential dignity, swiftness and good house','supported'),
('Saturn OR Mars square OR opposition retains exclusions','partly supported; restriction to afflicting planet needs IF-02'),
('Neither rule concerns both Saturn and Mars holding sixth/Moon-dispositor roles','candidate report insufficient; correct inR1562'),
('Unwell but not perfectly sick, then occupied OR ruled house inquiry','supported'),
('Second-house example requires no inward cause','supported'),
('Application=current money want; separation=recent loss','supported'),
('Opposition worse belongs to this local loss example, no universal weight','supported')],
'C11':[
('Fifth/seventh examples add qualifications','supported'),
('Games capacity and uncertain youth/distemper parenthesis reach','supported'),
('Seventh-house alternative causes, reciprocal husband/wife references','supported'),
('Youth continuation predicts no following sickness','supported'),
('Hypothetical/general interpretations plus broad customary-practice claim, not documented individual histories/endpoints','supported')],
'C12':[
('Catalogue follows figure erection and disease-significator choice','supported'),
('Mere planet presence insufficient to transfer every conditional catalogue statement','supported reasoning'),
('Saturn/Jupiter/Mars/Sun/Venus/Mercury retain distinct conditions and local context','supported on mapped records'),
('Bloodletting/sweating and causal language remain historical content','supported'),
('No treatment rule implemented','supported by helper inspection')],
'C13':[
('Leo OR Scorpio followed by SouthNode OR NorthNode glyphs','supported original glyphs'),
('With may attach to Scorpio only or both signs','supported retained uncertainty'),
('Combustion and violent-star alternatives retained','supported'),
('Poison reading is tentative AND prior-suspicion conditioned','supported'),
('No newly established poisoning from chart alone','supported scope distinction')],
'C14':[
('Fire-sign Saturn fevers usually','supported; body/errata agree'),
('Cold/moist case more assured with Venus OR Moon co-signification','supported'),
('Descriptive continuation reach remains open','supported'),
('Word is vitious, not viscous','supported; reviewer source-first correctedSC-01'),
('Fixed class lists Taurus/Leo/Aquarius as examples, no printed Scorpio','supported'),
('As-in list does not exclude Scorpio from named class','supported textual inference')],
'C15':[
('Common-sign Mars apparent departure distinct from eventual outcome','supported'),
('Saturn having signification AND aspect with good planets favourable at that time','supported'),
('No separately stated good-aspect condition','supported'),
('Saturn with eighth OR sixth lord says MAY expect death, no observed death','supported'),
('Melancholy conditional on Saturn involvement; his dignities uncertain','supported'),
('Planet opening printed263 is Mars, continuing sequence','supported original glyph')],
'C16':[
('Sun affliction at first lying down; Saturn antiscion alternative','supported'),
('Mars aforesaid-aspects shorthand retains scope uncertainty','supported'),
('Venus fiery one-day fever and Mars co-signification variant','supported; contextual-inheritance IC-01 retained'),
('No explicit physical conjunction or repeated duration for variant','supported'),
('Mercury misfortune AND disease authorship','supported'),
('Ninth lord in sixth occult-cause sentence requires existing mistrust','supported')],
'C17':[
('Errata has printed261line23 usually and printed262line33 returning','supported by originalPDF888'),
('Corresponding original body readings agree','supported by enlarged original crops'),
('No other identified errata correction within printed258-268 for retained syntax questions','supported targeted range scan'),
('This is targeted errata check, not all-edition collation','supported scope limit')],
'C18':[
('Unfortunate OR afflicted sixth lord above earth gives right/upper parts','supported'),
('Later first-person masculine requirement is distinct and not retroactively imported','supported'),
('Under-earth alternative literally superiour and fore-part','supported original reading'),
('No change to inferior','supported'),
('Nocturnal continuation and inherited conditions uncertain','supported')],
'C19':[
('Two feminine actors and second planet in feminine sign OR house','supported'),
('Feminine-house definition absent locally','supported local-source limit'),
('Few/middle/lower degrees refer to member upper/middle/lower parts','supported'),
('No numerical bins, decans or whole-body scale supplied','supported'),
('Inherited conditions and meaning of lower remain open','supported')],
'C20':[
('Intro spirit group: ascending sign, Moon, Sun-house lord','supported'),
('Member group: ascendant lord, Moon dispositor','supported'),
('Later all-afflicted group uses Sun itself with ascendant/Moon','supported'),
('Different all-or-two group uses Sun-house lord','supported'),
('Further comparison uses ascendant-lord dispositor, a second-order role','supported'),
('Roles not interchangeable and may coincide as physical bodies','supported source distinction plus implementation limit')],
'C21':[
('Many astrologians attribution and Saturn foreshows OR causes melancholy','supported'),
('Saturn role/placement/relation branches retained','supported'),
('Jupiter glyph and NEVER mind BUT body polarity','supported'),
('Amount of preceding Saturn conditions transferred unstated','supported uncertainty'),
('No modern causal/psychiatric claim inferred','supported evidence scope')],
'C22':[
('Mars sextile/square/opposition printed, not conjunction substitution','supported glyph reading'),
('Twelfth-house modifier scope remains uncertain','supported'),
('Malevolent ascendant aspect accompanied by NOT Moon and afflicted Sun-sign lord','supported'),
('Both comparative-affliction directions retained','supported'),
('No strength metric/tie/numerical aggregation in passage','supported local-source limit')],
'C23':[
('Unimpeded rulers alongside afflicted ascendant/Moon','supported'),
('Exalted Sun/ascendant lord with debilitated Moon dispositor','supported'),
('Plural solar-affliction distribution and later freedom-phrase subject uncertain','supported'),
('Usually remains in Sun-related character account','supported'),
('Venus no imported affliction requirement; Mercury explicitly has one','supported'),
('No single harmonized global classifier supplied','supported by code/data limits')],
'C24':[
('Optional nativity; degrees and eclipse/great-conjunction near sickness','supported'),
('No exact degree/sign matching rule or numerical nearness','supported local-source uncertainty'),
('Yearly-world-revolution eighth sign phrasing','precision repair IF-05: sign of eighth HOUSE'),
('Natal angles, especially ascendant; world frame distinct from natal/horary eighth','supported'),
('Separate ascendant-sign callback permits first sickness OR demand','supported'),
('Later crisis hierarchy not stated in that earlier sentence','supported')],
'C25':[
('Not above six inclusive plus not passed/not perfected conjunction','supported'),
('Aries/Leo lessens, does not cancel ill omen','supported'),
('Exactly twelve says little danger','supported'),
('No >=12, no no-danger, no6-to12 interpolation','supported'),
('Phase not restated for12; no clinical-risk threshold implemented','supported')],
'C26':[
('Nearest obtainable first-bed hour preferred','supported'),
('Only if unavailable, first physician-judgment request','supported'),
('Moon motion corrected to selected hour','supported'),
('Earlier printed243 urine/access/contact hierarchy separate','supported originalPDF277 and retainedrecords'),
('No universal overwrite of earlier question contexts','supported interpretive limit')],
'C27':[
('Acute NOT chronic; near times at45/90/135 from first lunar place','supported'),
('No180, all45 multiples, fixed days or near tolerance given','supported local-source limit'),
('Helper returns three angular targets only','supported inspected code/execution'),
('Corrected starting longitude, applicable illness course and selected origin required; unresolved/not-applicable otherwise','supported code including missing-vs-zero distinction')],
'C28':[
('350degrees15minutes is synthetic starting example','supported; absent as source chart'),
('Three arithmetic rows match independent modular calculation','supported; row checks below'),
('Integer arcseconds and zodiac modular arithmetic','supported code/execution'),
('No ephemeris/date; targets not evaluated clinical predictions','supported')],
'C29':[
('Good aspect AND benevolent planet required for favourable crisis statement','supported'),
('Ill aspect sixth OR eighth lord: worse, more pain, little medicine benefit','supported including pagebreak'),
('First-person hard-aspect recollection includes earlier afflictor of relevant places, sixth lord OR planet in sixth','supported'),
('No denominator or fully specified chart endpoints','supported'),
('Reach of earlier acute limit not repeated in later recollection','supported uncertainty')],
'C30':[
('Pronouncing comfort/relaxation or interval of ease for lunar trine/sextile to first/eleventh/ninth/tenth lord','supported'),
('Prognostic act, no verified recovery endpoint','supported'),
('Ascendant-lord/Sun clause mental relief only','supported'),
('Absence of power OR dominion in disease; likelySun pronoun with alternative retained','supported'),
('No unconditional bodily cure','supported')],
'C31':[
('Recovery judged first and timing asked','supported'),
('Degree count between ascendant lord and benevolent aspected planet','supported'),
('Houses/signs of both plus disease quality/discretion','supported'),
('Exact distance/perfected-aspect operation unspecified','supported local-source uncertainty'),
('Favourable aspect alone not used as proof of recovery','supported source dependency')],
'C32':[
('Moveable days ordinarily','supported'),
('Greater certainty with significators swift AND angular','supported'),
('Event amendment, not necessarily complete cure','supported lexical scope'),
('Common-sign time unit not mechanically fixed; disease nature and feasibility considered','supported'),
('Ancients provide options, not universal unique scale','supported')],
'C33':[
('Three source-category/time-option/house-correspondence rows','supported; row checks below'),
('Ancients sign associations followed by house equivalences','supported'),
('No stated priority for conflicting actual sign/house rows','supported local-source limit'),
('Moon speed/sign/quality together with principal significators, mixed considerations','supported'),
('Helper returns separate sign/house options and no selected unit/date','supported code/execution')],
'C34':[
('Ascendant lord leaves question-time sign for sign giving essential dignities','supported'),
('Recovery OR sensible improvement, no outgoing debility prerequisite','supported'),
('28 degrees AND common sixth cusp','supported exact illustration'),
('Vary in strictly less than2weeks','supported'),
('No>=28, recovery substitution or dated-case claim','supported')],
'C35':[
('Earlier printed249 choice is to disease nature','source referent repair IF-03: sign nature/quality'),
('Retained callback/new discussion keep local selectors explicit and do not yield new combined formula','supported after selector repair'),
('Figure or two is forward promise','supported'),
('No promised figures inside this span; no two charts/cases added','supported full-source evidence inventory')],
'C36':[
('894-page primary PDF and exact SHA256','independently recomputed/confirmed; historical assertion that root recomputed it not separately observed'),
('14-page window =11 main+errata+2 callbacks','supported'),
('Every corresponding original/window page has matching rendered dimensions and pixels','supported independent14-page comparison'),
('Full boundary context visible but preceding paragraph/lowerHermes excluded fromnewrecords','supported'),
('Eleven selected PNG crops present','supported inventory/hash check'),
('Does not duplicate every producer redundant render','documentary scope statement only; separate producer inventories were not opened')],
'C37':[
('Source-reader tags split54/47 in101records','supported by actual canonical tags'),
('Two readers produced frozen records; root read whole span/checks before compilation','process claim recorded, not independently observed and not proved by a file hash; separate narrative receipts were not opened'),
('Fresh-context evaluator froze full-span source-only notes before candidate exposure','directly known from this evaluator sequence and bound freeze'),
('One exhaustive pass then at most2 changed-item repairs','supported by root task instructions'),
('Same-family separated review, not cross-family/expert/empirical validation','supported limitation of actual method'),
('Reviewer assignment is not final diagnosis; dispositions must be retained','supported procedural principle, not an outcome claim')],
'C38':[
('20 tests, no failure/error/skip','supported receipt and private repeat'),
('Suite covers stated ID/pages/sections/index/link/input/origin/geometry/course/timing cases','supported test-source inspection'),
('Receipt binds tested files byhash','supported independent file-hash comparison'),
('Establishes bounded data-check/program behavior, no clinical efficacy','supported with limit: syntactic tests do not establish source semantics'),
('Required extracted-archive run repeats suite with0 newdistincttests','prospective instruction; private repeat itself added0')],
'C39':[
('Listed attribution/scope/vocabulary/role/counting/metric/tolerance/unit/evidence limits occur','supported original span and register'),
('Six resolved =2 constructions+4 root glyph/errata entries','supported exact registerIDs and source readings'),
('A reading resolution limited to that issue; no wider repair/empirical truth licensed','supported evidence distinction')],
'C40':[
('RULES contains101records with listed source/condition/outcome/dependency/limit fields','supported structural inventory; IF-01 remains a content defect in one record'),
('Reference tables and issue register serve stated documentary roles','supported'),
('Source-window verification maps originals','supported independent mapping'),
('run_verification is standalone standard-library suite','supported code and private execution'),
('Publication/preservation/archive/delivery receipts are separate operations evidence, not source/prediction validation','supported scope principle; those external operations are outside this review')],
'C41':[
('Next belowdividerPDF302/printed268 exactHermesheading','supported originalpage'),
('Include full opening heavenlyRayes paragraph thenPDF303','supported originalphysicalcontinuation and prospective instruction'),
('Upper bridge already represented fully','supported'),
('Next record number1651','supported1650+1'),
('ChapterXLIV remains incomplete','supported scope'),
('Rest ofLilly/multiauthoraudit open','supported as supplied index/task scope, not a new exhaustive audit of those works')]
}
claim_source_units={
'C01':['SF-001','SF-002','SF-048','SF-092'],'C02':['whole_span_evidence_inventory'],'C03':['whole_span_architecture'],'C04':['whole_span_evidence_inventory'],'C05':['SF-001','SF-005','SF-020','SF-021','SF-086'],'C06':['SF-091','SF-092'],'C07':['SF-003','SF-004'],'C08':['SF-005','SF-006','SF-007','SF-008'],'C09':['SF-009','SF-010'],'C10':['SF-011','SF-012','SF-013','SF-014','SF-015','SF-016'],'C11':['SF-017','SF-018','SF-019','SF-020'],'C12':['SF-021','SF-022','SF-030','SF-033','SF-036','SF-037','SF-043','SF-044','SF-046'],'C13':['SF-023'],'C14':['SF-024','SF-025','SF-026','SF-027'],'C15':['SF-037','SF-038','SF-039','SF-040','SF-042'],'C16':['SF-043','SF-044','SF-045','SF-046','SF-047'],'C17':['original_errata','SF-024','SF-040'],'C18':['SF-049','SF-050','SF-052'],'C19':['SF-051','SF-053'],'C20':['SF-054','SF-055','SF-056','SF-057','SF-063'],'C21':['SF-059','SF-060','SF-061'],'C22':['SF-064','SF-065','SF-066'],'C23':['SF-058','SF-062','SF-067','SF-068','SF-069','SF-070','SF-071'],'C24':['SF-072','SF-073','SF-074'],'C25':['SF-075'],'C26':['SF-076','SF-077','CX01'],'C27':['SF-077','SF-078'],'C28':['SF-078'],'C29':['SF-079','SF-080'],'C30':['SF-081','SF-082'],'C31':['SF-083'],'C32':['SF-084','SF-085','SF-086'],'C33':['SF-086','SF-087','SF-088'],'C34':['SF-089','SF-090'],'C35':['CX02','SF-083','SF-085','SF-088','SF-091'],'C36':['source_identity','whole_span_boundaries','original_errata','CX01','CX02'],'C37':['method_exposure'],'C38':['helper_and_test_evidence'],'C39':['whole_span_uncertainties'],'C40':['candidate_file_inventory'],'C41':['SF-092','lower_boundary_context']}
results=[]
for item in ledger['items']:
 cid=item['id'];fis=[f['id'] for f in findings if cid in f['report_claims']]
 status='supported_with_stated_limits'
 if cid in ['C10','C35']:status='source_meaning_repair_required'
 elif cid in ['C08','C24']:status='report_precision_repair'
 elif cid=='C09':status='source_locator_repair'
 elif cid in ['C04','C36','C37','C40','C41']:status='supported_with_documentary_or_observability_limits'
 checks=[{'component_id':f'{cid}.{i+1:02d}','statement_checked':a,'assessment':b} for i,(a,b) in enumerate(claim_checks[cid])]
 rows=[]
 for line in item['text'].splitlines():
  if line.startswith('|') and not line.startswith('|---'):
   cells=[x.strip() for x in line.strip('|').split('|')]
   rows.append(cells)
 table=[]
 if rows:
  for i,cells in enumerate(rows[1:],1):
   table.append({'row_id':f'{cid}.table.{i:02d}','cells':cells,'assessment':'supported','basis':'Actual record/index/register/test inventory counts' if cid=='C02' else 'Independent source-unit/record/page mapping' if cid=='C03' else 'Independent integer-arcsecond modular arithmetic' if cid=='C28' else 'Original PDF301/printed267 sign-unit and house equivalences'})
 results.append({'id':cid,'section':item['section'],'original_candidate_text':item['text'],'text_sha256':item['text_sha256'],'record_ids':item['record_ids'],'ledger_original_pdf_pages':item['original_pdf_pages'],'independent_source_units':claim_source_units[cid],'diagnostic_status':status,'finding_ids':fis,'component_checks':checks,'table_row_checks':table,'full_qualifier_review':'The entire bound paragraph/table, including citations, negative/modal language and following qualifiers, was read. Component checks name distinct factual or methodological assertions; row checks cover every data row.'})
assert len(results)==41 and set(claim_checks)=={x['id'] for x in ledger['items']}
assert sum(len(x['table_row_checks']) for x in results)==25
missed=[{'id':'MC-01','report_location':'Byline immediately below title','text':'Book II, Chapter XLIV continuation — source audit B02l, 10 October 2026.','kind':'unledgered factual metadata','assessment':'Supported by original book/chapter context, batch instruction and provided task-start date. No mid-task clock read used.','significance':'The ledger covers every substantive body paragraph/table but omits this byline metadata.','suggested_disposition':'Add a metadata ledger item or explicitly state that the41 units exclude title/byline metadata. No source-content change needed.'}]
residual=(Q/'REPORT_RESIDUAL_SCAN.txt').read_text()
write('ALL_CLAIM_RESULTS.json',{'candidate_manifest_sha256':'41a5d97ba5c0a560c16fedbcfd24d8bd09a185b116d5d884374881f5194cbf48','report_sha256':hashlib.sha256((P/'AUDIT_REPORT.md').read_bytes()).hexdigest(),'ledger_sha256':hashlib.sha256((P/'CLAIM_LEDGER.json').read_bytes()).hexdigest(),'ledger_items_reviewed':len(results),'component_checks_count':sum(len(x['component_checks']) for x in results),'table_data_rows_reviewed':sum(len(x['table_row_checks']) for x in results),'table_rows_by_item':{x['id']:len(x['table_row_checks']) for x in results if x['table_row_checks']},'results':results,'independent_whole_report_scan':{'method':'Read the complete report separately, verified each ledger text hash and unique occurrence, then masked all41 texts and inspected every remaining title/byline/heading.','all_substantive_body_paragraphs_and_tables_bound':True,'residual_file':'REPORT_RESIDUAL_SCAN.txt','missed_factual_claims':missed,'headings_assessment':'Organizational headings either repeat source/interpretation claims already reviewed in their section or are labels/instructions. No additional unbound substantive body claim was found.'},'evidence_and_observability_limits':['A supplied retained index supports the retained Ptolemy count, not a fresh source audit of Ptolemy.','Own source-first freeze before candidate exposure is directly known. Other workers/root internal reading chronology is not independently observable and was not inferred from hashes.','Reference-only fields and helper behavior are inspected; external prediction-runtime deployment and owner delivery/preservation operations are outside this private review.','Source semantics are adjudicated from original images; passing structural tests is not source-semantic or empirical validation.'],'self_corrections':self_corrections,'interpretive_differences':interpretations,'accuracy_evaluated':False})
method={
'role':'Bounded, same-family contextual independent source/claim diagnostic evaluator; root is sole canonical writer.',
'stage':'Initial exhaustive diagnostic pass, completed before findings are released to root.',
'candidate_directory':str(P),
'candidate_manifest':digest(P/'CANDIDATE_MANIFEST.json'),
'primary_source':{'path':'/workspace/scratch/bd2460f96de0/Lilly-1647-Christian-Astrology-I-III.pdf','sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b','pages':894},
'source_first_outputs_before_candidate_exposure':[digest(Q/n) for n in ['SOURCE_FIRST_NOTES.md','SOURCE_FIRST_MAP.json','SOURCE_FIRST_FREEZE.json']],
'exposure_sequence':['Original full-page images for PDF292-302 were inspected before candidate exposure; direct original PDF crops were used for difficult text/glyphs.','Original errataPDF888 and earlier callbacksPDF277/283 were inspected separately in the source-first stage. PDF889 was checked as blank adjacent errata context.','SOURCE_FIRST_NOTES.md and SOURCE_FIRST_MAP.json were frozen and their exact hashes sent to root before the candidate path was authorized.','Only after that freeze, the authorized candidate records/report/ledger/helper/tests/supporting data and images were inspected.','The full initial diagnosis and all-claim/source-coverage outputs are frozen before any semantic findings are communicated to root.'],
'candidate_material_reviewed':['All101 RULES records including source_fields duplicates, conditions, consequents, exception/qualification, dependency, attribution and implementation fields.','Every41 CLAIM_LEDGER item and the complete AUDIT_REPORT separately; all25 table data rows; remaining unbound metadata/headings after masking.','Canonical UNRESOLVED issue register and REFERENCE_TABLES; retained timing excerpts compared to original source.','Bounded helper, test file, run_verification runner, original test receipt and log; copied files executed only in private directory.','Numeric/count/coverage/image manifests and selected fields of retained/current Lilly and retained Ptolemy indexes.','Candidate original-source window, independently compared pixel-for-pixel to all14 corresponding original pages. Eleven selected candidate crops inspected visually in three contact sheets against the original-page content.'],
'embedded_producer_text_exposure':'After the source-first freeze, canonical records/source_fields and the canonical UNRESOLVED register were read as candidate assertions. They include producer-authored descriptions and embedded issue observations. They were not treated as independent source evidence.',
'not_consulted':['Separate root or producer narrative notes, rationales, reconciliation/confidence summaries or earlier audit narratives.','Other workers communications, summaries or agent inventory.','An original Dariot edition or an all-edition collation.','External clinical outcomes, clinical literature, or runtime/deployment systems.'],
'verification_performed':{'candidate_manifest_files_verified':43,'original_window_pages_pixel_compared':14,'candidate_crops_visually_inspected':11,'source_first_units_mapped':92,'canonical_records_compared':101,'ledger_units_compared':41,'table_data_rows_compared':25,'subclaim_components':sum(len(x['component_checks']) for x in results),'private_copied_canonical_suite_passed':20,'canonical_suite_repeat_new_distinct_tests':0,'additional_focused_manual_helper_probes':15,'manual_probes_added_to_canonical_test_count':0},
'observability_limits':['A hash proves the bound file identity, not that another person actually read a page at a claimed earlier time.','The evaluator directly knows its own separation sequence; root/producer reading chronology is treated as a process claim, not independently observed.','Reference-only statuses and helper code are visible; no independent observation of external deployment, publishing, preservation or owner delivery is asserted.','Ptolemy1066 is a retained numeric-index count with matching snapshot hash, not a fresh Ptolemy source-fidelity evaluation.','No promise of perfect historical interpretation, cross-family independence, expert adjudication, IV&V, predictive accuracy or treatment efficacy.'],
'self_corrections':self_corrections,
'interpretive_difference_policy':'Source-first notes are fallible. The original witness is the arbiter; clear reading corrections are disclosed without altering the prior freeze. Plausible but nonunique contextual readings are distinguished from definite candidate errors.',
'write_scope':str(Q),
'canonical_mutation':False,
'semantic_findings_sent_before_freeze':False,
'continuation_policy':'After this initial diagnosis, at most two changed-item repair checks if root requests them. No extra assurance or research gates are imposed.',
'time_policy':'No mid-task clock reads or fabricated completion time. The date in the report byline was assessed against the provided task-start metadata.'
}
write('EXPOSURE_AND_METHOD.json',method)
summary_status={x['id']:x['diagnostic_status'] for x in results}
lines=[
'# Initial independent diagnosis — Lilly B02l',
'',
'## Outcome',
'',
'The complete admitted source span is represented in the candidate: all 92 independently reconstructed source units map to the 101 canonical records, and every canonical record maps back to the source. The full italic introduction and full upper paragraph ending **Judgments of this House** are included. No missing local section, skipped source unit, or intrusion into the following Hermes text was found.',
'',
'This is **not an unqualified clean-fidelity result**. The initial pass identifies **six bounded candidate corrections**: one plural/singular source-record error, two substantive report meaning errors, two report wording-precision corrections, and one incomplete point-of-use citation. It also identifies one omitted byline-metadata ledger item. Two readings in my own frozen source-first notes were wrong; the candidate is correct on both, and those corrections are disclosed below. One contextual inheritance difference remains nonunique and is not classified as a definite candidate defect.',
'',
'The helper implements only the documented origin selection, three-angle arithmetic and unsynthesized timing options. No bounded-helper behavior defect was found. Its copied 20-test suite passed; rerunning it adds zero distinct tests. Fifteen focused manual probes were also used as diagnostic evidence, without increasing the reported canonical test count. This establishes the inspected arithmetic and code behavior, not the historical method’s predictive accuracy.',
'',
'## Exact source and candidate bindings',
'',
'- Original source: `/workspace/scratch/bd2460f96de0/Lilly-1647-Christian-Astrology-I-III.pdf`, 894 pages; SHA256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`.',
'- Candidate: `/workspace/scratch/43f75264c32e/review-candidate-b02l-01`; manifest SHA256 `41a5d97ba5c0a560c16fedbcfd24d8bd09a185b116d5d884374881f5194cbf48`.',
'- All 43 manifest-listed files matched their declared bytes and SHA256 values. Candidate integrity does not by itself establish source meaning.',
'- Main source: PDF292/printed258, **DARIOT Abridged** and its complete introduction, through PDF302/printed268, the entire upper bridge ending **Judgments of this House**. Preceding **shew death** paragraph and lower Hermes heading/text are outside this batch. Chapter XLIV remains incomplete.',
'- Separate context: original errata PDF888; earlier timing callbacks PDF277/printed243 and PDF283/printed249. These were independently read before candidate exposure and were not counted as new source records.',
'',
'## Candidate corrections',
'']
for f in findings:
 lines.extend([f"### {f['id']} — {f['classification'].replace('_',' ')}",'',f"**Scope:** {f['importance']}. Candidate: {'; '.join(f['candidate_locations'])}.",'',f"**Source:** PDF{f['pdf_pages'][0]}/printed{f['printed_pages'][0]}, “{f['source_anchor']}.”",'',f"**Diagnosis:** {f['diagnosis']}",'',f"**Bounded repair:** {f['repair']}",'',f"**Evidence and uncertainty:** {f['certainty']}",''])
lines.extend([
'## Corrections to the evaluator’s frozen source-first reading',
'',
'The source-first freeze is left byte-for-byte unchanged. The diagnosis uses the original source readings after direct enlarged inspection. These are errors in my initial reading, not candidate errors:',
'',
'| Correction | Original location | Frozen source-first reading | Source-adjudicated reading | Candidate disposition |',
'|---|---|---|---|---|',
'| SC-01 | PDF295/printed261; SF-026 | viscous | **vitious** | R1578 and C14 are correct. |',
'| SC-02 | PDF295/printed261; SF-019 anchor | the man **he** longs after | the man **she** longs after | R1569 is correct. |',
'',
'Enlarged original crops `diagnostic_pdf295_vitious_reading.png` and `diagnostic_pdf295_youth_pronoun.png` support these corrections. The source-first paraphrase of the youth clause was largely neutral, but its anchor had the wrong pronoun. The cold/moist symptom paraphrase as well as its anchor had the wrong lexical reading.',
'',
'The original body words **usually** and **returning** also agree with the two targeted errata entries. The enlarged returning crop shows the crowded **rn** shape; it does not support changing that word to a different spelling. This confirms C17 rather than adding a new candidate defect.',
'',
'## A retained interpretive difference',
'',
'IC-01 concerns the Venus/fire-sign sentence followed by **but if Mars joyne in signification** on PDF297/printed263. My source-first map left the reach of the fiery-sign condition open because it is not repeated. R1601 explicitly calls it inherited context, which is a plausible connected reading. I therefore do not label the candidate as silently inventing a condition. A qualification that this condition is inherited rather than repeated would be precise. No one-day duration is transferred to the Mars variant, and joining in signification is not falsely made a physical conjunction.',
'',
'The exact intended inheritance remains uncertain. A directly inspected corresponding authorial source or explicit textual clarification could settle it. This observation does not impose another research or acceptance gate.',
'',
'## All-claim and whole-report coverage',
'',
'All 41 ledger texts occur exactly once in the frozen report and match their text hashes. I read the full report separately and inspected the residual text after masking those 41 units. Every substantive body paragraph and every table is bound. All **25 data rows** were individually checked: ten inventory rows, nine source-coverage rows, three arithmetic rows and three timing-correspondence rows.',
'',
'`ALL_CLAIM_RESULTS.json` retains each original bound text, every component check, all table rows, the source-unit links, and the exact diagnosis. The table below gives the per-item outcome; a supported status includes the qualifications stated in the corresponding detailed result.',
'',
'| Ledger item | Diagnostic result |',
'|---|---|'])
for x in results:lines.append(f"| {x['id']} | {x['diagnostic_status'].replace('_',' ')}{' — '+', '.join(x['finding_ids']) if x['finding_ids'] else ''} |")
lines.extend([
'',
'**Unledgered metadata MC-01:** the byline **Book II, Chapter XLIV continuation — source audit B02l, 10 October 2026.** is outside the 41 ledger texts. Its facts are supported by the source context, task batch and provided start-date metadata. Add a small metadata item, or explicitly state that the 41 ledger units exclude title/byline metadata. No substantive source text needs changing for this item. The remaining unbound headings are organizational labels or restatements reviewed in their associated sections; no additional unbound substantive body claim was found.',
'',
'## Inventory, arithmetic and source-window checks',
'',
'Counts were recomputed from the supplied data: 101 new records, previous Lilly1549, current Lilly1650, retained Ptolemy1066 and combined2716. Canonical source-reader tags split54/47. Record kinds sum to101: 7 dependency, 67 general rule, 8 illustration, 8 author experience and11 method. These are editorial inventory categories, not independent observations or predictions.',
'',
'The original span contains no individuated dated enquiry, reconstructible worked horoscope, clinical outcome series, independently checked endpoint or denominator from which an accuracy fraction can be computed. It does contain general rules, constructed examples, authorial claims about customary practice, claimed remembered success, prognostic acts and a forward promise of figures. The source-first evidence inventory keeps these categories distinct. The forward promise contributes no chart or completed case inside this span.',
'',
'The42 issue entries consist of36 retained limits/anomalies and6 source-resolved readings. The resolved IDs are SA-I06, B-SI-10 and ROOT-SR01 through ROOT-SR04. Source review supports the fixed-sign example construction, printed Mars sextile, node glyphs, opening Mars glyph, and body/errata usually/returning readings. A resolved glyph does not settle a separate grammatical attachment.',
'',
'The 14-page window was independently rendered page-by-page and compared to the original PDF. All dimensions and all RGB sample bytes matched for main pages292–302, errata888 and callbacks277/283. The eleven selected candidate crops were also visually inspected against the original-page content; this latter inspection is not described as an additional pixel-for-pixel crop provenance proof.',
'',
'The synthetic350°15′ example gives35°15′,80°15′ and125°15′ after45°,90° and135° displacements modulo360°. In integer arcseconds the targets are126900,288900 and450900. No ephemeris, date or clinical prediction is involved.',
'',
'## Helper boundaries and execution evidence',
'',
'The inspected helper retains first-bed-hour priority and permits the first physician-judgment-request fallback only when the bed hour is unavailable. Its distinction between unknown and unavailable is a disclosed conservative implementation choice. Labels pass through unchanged; neither time-zone conversion nor calendar parsing occurs. A known bed hour wins over an available physician hour; unknown bed-hour availability does not authorize fallback.',
'',
'Only acute-course selected-origin inputs with a supplied integer-arcsecond longitude emit the three modular targets. Zero is a valid longitude, while missing longitude is unresolved. Chronic course is not applicable. The caller must supply a longitude already corrected to the chosen hour; the helper does not validate an ephemeris or construct a chart. It supplies no contact tolerance, fourth angle, calendar date, disease outcome or treatment.',
'',
'Timing options preserve moveable→days, common→weeks/months, fixed→months/years and angular/succedent/cadent correspondences as separate input dimensions. Conflicts remain unresolved. The result keeps selected unit and date empty and carries the prior-recovery-judgment requirement. It does not implement the whole illness catalogue, mind/body allocation, six/twelve-degree danger language or a clinical classifier.',
'',
'The original20-test receipt binds the tested files by hash, and all those hashes matched. The copied suite passed20 tests with no failures/errors/skips in the private directory. This is the same20 tests; the repeat contributes0 distinct tests. Fifteen focused manual helper executions corroborated the source-boundary behavior and the displayed arithmetic; they are not added to the canonical count. These mechanical checks are recorded in `INDEPENDENT_INVENTORY_CHECK.json`, `HELPER_BEHAVIOR_CHECKS.json`, and the private test log/summary.',
'',
'## Exposure, independence and practical limits',
'',
'The source-first notes/map were completed and frozen before the candidate was opened. Original page images, rather than OCR, established source readings. OCR was only a navigation aid. The subsequent candidate pass read all canonical record fields, the full report and ledger, supporting source-data tables, the issue register, retained timing excerpts, helper/test code and relevant numeric/image data. Embedded producer descriptions in canonical records and the issue register were read after the source-first freeze as candidate claims, not as independent evidence.',
'',
'I did not open separate root/producer narrative notes, rationales, reconciliation/confidence summaries, other workers’ summaries, or earlier audit narratives. I did not use an agent inventory or contact other workers. I wrote only in the private independent directory and did not change the candidate or canonical files.',
'',
'Own source-first separation is directly known. Other participants’ claimed internal reading chronology is not independently observable. A file hash binds evidence identity; it does not prove that someone read an image at an earlier time. C37 therefore has an explicit observability qualification. Similarly, retained Ptolemy counts are verified against the supplied numeric snapshot and its hash, not by a new Ptolemy source audit. Reference-only flags and code behavior are visible, while external deployment, publishing, preservation and owner-delivery operations remain outside this role.',
'',
'This is same-family contextual separation, not cross-family review, an expert historical edition, clinical review or IV&V. The findings are diagnostic and source-adjudicated. Root retains the authority to apply or reject a flag with source evidence. The agreed continuation is at most two checks of changed items if requested, with no additional assurance gates.',
'',
'## Artifact map',
'',
'- `DIAGNOSTIC_FINDINGS.json`: six candidate corrections, two evaluator corrections, one interpretive difference.',
'- `SOURCE_RECORD_COVERAGE.json`: all92 source units, all101 reverse record mappings, source anchors, conditions/qualification checks and evidence inventory.',
'- `ALL_CLAIM_RESULTS.json`: all41 ledger items, every component and25 table rows, plus the independent missed-claim scan.',
'- `EXPOSURE_AND_METHOD.json`: exact method, exposure sequence, consulted and unconsulted material, observability limits and role scope.',
'- `CANDIDATE_INTEGRITY_CHECK.json`, `CLAIM_TEXT_BINDING_CHECK.json`, `FIELD_CONSISTENCY_CHECK.json`: file/text/duplicate-field bindings.',
'- `INDEPENDENT_SOURCE_WINDOW_CHECK.json`, `INDEPENDENT_INVENTORY_CHECK.json`, `HELPER_BEHAVIOR_CHECKS.json`: independent mechanical checks.',
'- `diagnostic_test_copy/INDEPENDENT_TEST_RUN.log` and `diagnostic_test_copy/TEST_RUN_SUMMARY.json`: actual private repeat of the copied suite.',
'- `INITIAL_DIAGNOSIS_FREEZE.json`: byte counts and SHA256 bindings for this complete initial diagnosis and its supporting evidence.',
''])
md='\n'.join(lines)
for old,new in {
'previous Lilly1549':'previous Lilly 1,549','current Lilly1650':'current Lilly 1,650','retained Ptolemy1066':'retained Ptolemy 1,066','combined2716':'combined 2,716','split54/47':'split 54/47','sum to101':'sum to 101','and11 method':'and 11 method','The42':'The 42','of36':'of 36','and6 source':'and 6 source','pages292':'pages 292','errata888':'errata 888','callbacks277':'callbacks 277','synthetic350':'synthetic 350','gives35':'gives 35','′,80':'′, 80','and125':'and 125','after45':'after 45','°,90':'°, 90','and135':'and 135','modulo360':'modulo 360','are126900,288900 and450900':'are 126,900, 288,900 and 450,900','original20-test':'original 20-test','passed20':'passed 20','same20':'same 20','contributes0':'contributes 0','all92':'all 92','all101':'all 101','all41':'all 41','and25':'and 25'
}.items():md=md.replace(old,new)
(Q/'INITIAL_DIAGNOSIS.md').write_text(md)
print(json.dumps({'source_units':len(coverage),'records':len(reverse),'ledger_items':len(results),'component_checks':sum(len(x['component_checks']) for x in results),'table_rows':sum(len(x['table_row_checks']) for x in results),'candidate_findings':len(findings),'self_corrections':len(self_corrections),'interpretive_differences':len(interpretations),'unledgered_metadata':len(missed)}))
