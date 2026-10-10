import json, pathlib, hashlib, sys
p=pathlib.Path(sys.argv[1])
out=pathlib.Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True)
oldp='/workspace/scratch/43f75264c32e/review-candidate-01/B02j'
oldout='/workspace/scratch/43f75264c32e/independent-review'
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def find_list(v,n):
 if isinstance(v,list):
  if len(v)==n and all(isinstance(x,dict) for x in v):return v
  for x in v:
   r=find_list(x,n)
   if r is not None:return r
 elif isinstance(v,dict):
  for x in v.values():
   r=find_list(x,n)
   if r is not None:return r
claims=find_list(json.loads((p/'CLAIM_LEDGER.json').read_text()),94)
rules=find_list(json.loads((p/'RULES.json').read_text()),201)
assert [c['id'] for c in claims]==[f'CL{i:03}' for i in range(1,95)]
assert sha(p/'CLAIM_LEDGER.json')=='4547fa0327d55688e8cd7d8b564af444f9a597e19a879a4a9278ce1ad818147f'
assert sha(p/'RULES.json')=='a505ce3f94c3bba095ea1fdfc8ebd310860d63912a60de71d57a8a8e71e9c988'
reasons=[
"All 21 admitted original pages and the complete section sequence were read source first. The PDF256 divider and PDF277 opening delimit the stated block; the two identified wording defects do not establish an omitted section.",
"Correctly distinguishes historical extraction, reference arithmetic and untested predictive accuracy; the helpers do not implement a personal assessment.",
"The candidate has 201 distinct canonical records, consecutively R1157–R1357.",
"Of the 201 records, 166 have no worked-case ID; general methodological statements within the examples remain general records.",
"Exactly 35 candidate records have a worked-case ID; their dependent status is preserved.",
"The retained Lilly index supplies the earlier batch counts and the 201-row continuation; their sum is 1,357. Earlier batches were not semantically re-audited.",
"The packet declares 1,066 retained Ptolemy records, but it does not supply the underlying Ptolemy register or a countable retained index. The claim is unverified within this disclosure boundary, not shown numerically false.",
"1,357 + 1,066 = 2,423 is correct conditional arithmetic. The verified combined-inventory claim inherits the missing independent support for its Ptolemy component.",
"The candidate UNRESOLVED register contains 64 entries; an entry may contain more than one limitation.",
"The coverage register contains 27 editorial coverage units, not 27 numbered chapters.",
"The source presents two dated enquiries and two worked charts in XLII–XLIII.",
"The two coordinate tables contain 45 entries; missing precision and inferred signs remain distinguishable.",
"The printed testimony table contains 12 rows, with four under female and eight under male.",
"The test source contains 36 distinct tests; the independent rerun completed all 36 successfully.",
"Inventory and dependency qualifications are supported. The asserted earlier 32-test subset relationship requires the withheld implementation reconciliation or earlier suite; the final 36-test files alone cannot establish that historical relationship.",
"The 76 XXXIX rows cover the stated material on printed222–229, including unnumbered passages.",
"The 58 XL rows cover conception, sex, multiplicity, birth timing and the additional unnumbered material on printed229–235.",
"The 28 XLI rows cover the parent–child and messenger material on printed235–238.",
"The 17 XLII rows cover the first example and the subsequent general nativity comparison on printed238–240.",
"The 22 XLIII rows cover the second example, its testimony table, timing and retrospective outcome statements on printed240–242.",
"The 27 units correspond to editorial coverage subdivisions; rule granularity does not turn each subdivision into a source chapter or independent case.",
"The different question settings are retained in the relevant conditions and attributions; they are not presented as one context-free conception rule.",
"The major absence-versus-loss branch is preserved, but B039/R1271 adds independently to prior assurance without marking the addition as interpretation. The source requires assurance before the question; it does not specify an independent evidentiary standard. This is a narrow prerequisite-fidelity failure.",
"Family history remains a stated condition in the multiple-child discussion, without a fabricated numerical weight. The second worked enquiry presupposes pregnancy.",
"The report keeps the listed endpoints analytically distinct and labels the evaluation implication as an audit inference rather than Lilly's scoring system.",
"Natural capacity, age and hereditary considerations are retained; seldom two is not normalized to never, and no statistical calibration is attributed to the source.",
"The particular house-lord affliction and essential-versus-accidental fortification qualifications match the admitted passages.",
"The asymmetric dignity lists and the possibility that one planet supplies several roles are retained; no independence is inferred from role count.",
"The zodiac-relative own-house cadence discussion and the Aries/Taurus/Gemini illustration match the source. The packet appropriately does not supply a complete multi-rulership selection algorithm.",
"Anonymous alternative authorities and the unclear endpoint of the Some say voice are marked, rather than silently merged into a universal rule.",
"The year table follows the capacity discussion and retains its local context.",
"The source assigns the first house to the first year.",
"The source assigns the second house to the second year.",
"The source assigns the tenth house to the third year.",
"The source assigns the seventh house to the fourth year.",
"The source assigns the fourth house to the fifth year.",
"The five stated mappings, seven unstated mappings and unquantified epoch/modifiers are represented without completing the table by invention.",
"The relevant rule selects the nearest separation among Moon, fifth lord and hour lord; it is not an arbitrary choice of one.",
"The trine alternatives remain fifth or third month.",
"The sextile alternatives remain second or sixth month.",
"The square correspondence remains fourth month.",
"The opposition wording remains conceived seven months.",
"The conjunction wording remains conceived one month.",
"The candidate preserves the alternative months and ordinal/elapsed distinction, and the helper returns the alternatives without choosing an outcome.",
"The Part of Children direction Mars-to-Jupiter projected from the ascendant, same day/night, matches this block. The separate Fortune formula is supported by the retained exact-source excerpt and is not substituted into the new part. Earlier Fortune page images were not independently certified in the diagnostic phase.",
"The ascensional direction, day/degree rate, neighboring sign/month language, conjunction conditions and majority/concurrence language remain separate; no missing arbitration algorithm is invented.",
"The week/degree conversion is tied to the worked example and the code requires matching method and measure. It does not calculate the unspecified ascensional algorithm.",
"The first chart date, time, day/hour labeling and relevant signs/lords agree with the original figure and ensuing text, subject to explicitly recorded inferred-sign qualifications.",
"The negative judgment and its counterfactual softening conditions are present; the source gives no lifetime follow-up establishing the lifelong prediction.",
"Five marks and their dependent retrospective status are correctly counted, but genital region and the canonical genital member paraphrase add an anatomical identification absent from the cited sentence. It says the member signified by Moon in Virgo. No supporting anatomical identification is supplied; preserve or explicitly qualify the ambiguity.",
"The general preference for the nativity and the same-triplicity/sign/degree observation are reported without turning them into a demonstrated natal case series.",
"The second date and time agree with the original chart. The Moon day/hour chart notation and Jupiter hour table testimony are kept as inconsistent source witnesses.",
"The introductory characterization of the 12 printed testimony rows is accurate.",
"The female table includes Virgo on the ascendant.",
"The female table includes Capricorn on the fifth.",
"The female table includes the Moon in a feminine sign.",
"The female table includes Mercury with Venus.",
"The male table includes Mercury in a masculine sign.",
"The male table includes Saturn as a masculine planet.",
"The male table includes Saturn in a masculine sign.",
"The male table includes the Moon in a masculine house.",
"The male table includes Saturn in a masculine house.",
"The male table includes Jupiter as lord of the hour.",
"The male table includes Jupiter in a masculine sign.",
"The male table includes Mercury applying to the square of Mars.",
"Eight male and four female rows, the male judgment and the author's proved statement match the source. Reused bodies/roles remain dependent and are not a success rate.",
"Replacing both Jupiter-hour-chain votes only under the stated counterfactual produces 6:6. The packet explicitly labels this an audit sensitivity, not a repair or Lilly's own recomputation.",
"The stated geometric sectors and distances are consistent with the coordinates. The earlier five-degree cusp-virtue rule is offered only as a possible explanatory inference, not as Lilly's explicit worked-case explanation. Diagnostic certification of the earlier page image is limited.",
"The movable-sign and slow-Saturn considerations are retained as the source's weighting context, without a numerical weighting scheme.",
"The Moon-to-Saturn square gap is 14 degrees 47 minutes from the stated longitudes and the specified square ray.",
"The Mercury-to-Saturn conjunction gap is 13 degrees 37 minutes from the stated table longitudes.",
"The two stated gaps differ by 1 degree 10 minutes.",
"Static arithmetic and ray choice are correct; the diagram's unprinted Mercury minutes remain null and the later 00-minute table entry remains a distinct source witness.",
"The about-14-weeks reading and reported July11 date are preserved. Same-calendar April7 to July11 is 95 days, or 13 weeks 4 days, three days short of 14 weeks.",
"The source does not supply a rule selecting, averaging or rounding the two arcs into an exact forecast or tolerance. The reference code preserves exact fractions.",
"The birth-day transits are narrated after the reported outcome and are not four additional prospective forecasts. No independent ephemeris verification or missing time/calendar/location input is supplied.",
"The first chart's third/ninth cusp readings preserve the ten-minute discrepancy. Inferred signs remain labeled rather than silently normalized.",
"The first worked parts agree with the stated formulae conditional on the inferred coordinates; the arithmetic cannot establish those uncertain source readings.",
"The second chart and retrospective solar prose preserve the four-minute difference. Both Fortune consequences are conditional arithmetic, not a correction of either source witness.",
"The listed errata distinctions and non-repair policy are supported by the packet's targeted transcription and excerpt records. The independent checker did not obtain a certifiable visual read of PDF888 in the diagnostic phase; no wider errata search was performed.",
"The parent–child argument retains natal preference, the practical horary discussion, fault allocation and reconciliation action. The intervention is not treated as an untouched forecast outcome.",
"The messenger discussion is introduced with differentiated role assignments rather than one universal messenger ruler.",
"The envoy inquiry uses fifth lord and Moon in the stated context.",
"The money-message inquiry preserves sender/first, recipient/seventh, Moon/message and fifth/messenger assignments.",
"The foot-post inquiry preserves its first-lord/Moon-to-seventh conditions.",
"The report correctly separates receipt of news from physical return.",
"The separate money significator and reception/hard-aspect welcome conditions remain contextual; adverse status is not made a blanket refusal of the payment significator.",
"Degree-to-time conversion remains dependent on journey and sign context; near-day language is not upgraded into an exact guarantee.",
"The independent checker's source-first reading and frozen-note hashes are directly verified. The candidate receipt reports producer source reading and pre-candidate freezes, but the producer freeze files/chronology are withheld. That part of the whole paragraph cannot yet be independently verified; no fabrication or chronology violation is established.",
"The 36-test result, coverage of the named interfaces and exit code 0 are independently reproduced. The separate assertion about three reproduced implementation-review problems and their retained repairs requires withheld review/reconciliation evidence and is not adjudicable from the final code alone.",
"These are explicit release requirements, not assertions that publication or delivery already occurred. The distinction between preservation and predictive validation is sound; fulfillment remains outside this diagnostic freeze.",
"The PDF277 opening, topic list and XLIV heading are visually confirmed. They are the next extraction boundary; the fifth-house coverage is complete in extent while the wider audit remains open.",
"Read as the authorized release specification: supplied records/code/witnesses are inspectable, while final ZIP/README and delivery obligations must be checked at release. This is not certification that an unseen archive was already delivered.",
"The original file's page count, byte count and supplied SHA256 identity are consistent with the source and retained identity records; the named Wellcome identifier is retained provenance, not a newly verified remote download."
]
assert len(reasons)==94

failures={
'CL007':('EVIDENCE_NOT_DISCLOSED','Retained Ptolemy register/index unavailable'),
'CL008':('EVIDENCE_NOT_DISCLOSED','Combined verified count depends on CL007'),
'CL015':('EVIDENCE_NOT_DISCLOSED','Earlier 32-test subset history unavailable'),
'CL023':('SOURCE_FIDELITY','Unmarked independently qualifier in B039/R1271'),
'CL050':('SOURCE_FIDELITY','Unmarked genital anatomical interpretation in C012/R1330'),
'CL089':('EVIDENCE_NOT_DISCLOSED','Producer pre-candidate freeze chronology unavailable'),
'CL090':('EVIDENCE_NOT_DISCLOSED','Three-problem implementation repair history unavailable')
}
checks=[]
for i,(c,reason) in enumerate(zip(claims,reasons),1):
 cid=c['id'];fail=cid in failures
 checks.append({
 'id':cid,'verdict':'FAIL' if fail else 'PASS',
 'verdict_kind':failures[cid][0] if fail else 'SUPPORTED_WITHIN_DECLARED_BOUND',
 'literal_candidate_claim':c,
 'reason':reason,
 'source_and_packet_anchors':c.get('anchor'),
 'scope_note':'A FAIL for missing disclosure is not a determination that the proposition is false. A PASS is bounded source/packet support, not empirical predictive validation.'
 })
additional=[
 {'id':'ADD001','verdict':'FAIL','candidate_target':'RULES.json C012 / LI.1647.II.XLII.R1330, title and assertion','reason':'Unqualified genital_region/genital member classification is not present in the cited PDF273/printed239 sentence. The report-level failure CL050 also requires correcting or qualifying the canonical row.','evidence':'Original PDF273 lower body-mark paragraph; diagnostic-pdf273-277-contact.png'},
 {'id':'ADD002','verdict':'FAIL','candidate_target':'RULES.json B039 / LI.1647.II.XL.R1271, source_fields.conditions and prerequisites','reason':'The word independently adds an evidentiary qualifier to prior assurance which the source does not state. Remove it or explicitly mark the interpretation; the source’s temporal before-the-question condition must remain.','evidence':'Original PDF267/printed233; adjacent B040 quotes the assurance condition without the added qualifier.'},
 {'id':'ADD003','verdict':'PASS','candidate_target':'Canonical record IDs, source identity and runtime/evidence flags','reason':'All 201 records form the stated continuous ID range, retain the source hash and reference-only status, and do not claim to be independent evidence units.','evidence':'RULES.json; independent test log; original source identity'},
 {'id':'ADD004','verdict':'PASS','candidate_target':'45 coordinate entries as source witnesses','reason':'Tables keep inferred signs, the first cusp discrepancy and the second chart/table Mercury-minute distinction visible. PASS does not certify an uncertain glyph beyond the qualification printed in the table.','evidence':'WORKED_NUMERIC_TABLES.json; original PDF272 and274; frozen source notes'},
 {'id':'ADD005','verdict':'PASS','candidate_target':'Second-chart Jupiter and fourth/tenth cusp glyphs','reason':'Diagnostic reinspection supports Jupiter Gemini15:20 and the fourth/tenth cusp pair Sagittarius/Gemini2:20. These refine uncertainties in source-first notes; the frozen notes were not overwritten.','evidence':'Original PDF274 high-resolution view; WORKED_NUMERIC_TABLES.json'},
 {'id':'ADD006','verdict':'PASS','candidate_target':'Reference timing and aggregation interfaces','reason':'The code distinguishes static longitude arcs from ascensional directions, requires method/measure compatibility, labels sensitivity changes and rejects duplicate vote IDs or missing dependency inputs. It does not generate a missing astrology algorithm.','evidence':'lilly_fifth_house_reference.py; test_lilly_fifth_house.py; INDEPENDENT_TEST.txt'},
 {'id':'ADD007','verdict':'PASS','candidate_target':'Calendar helper scope','reason':'The helper requires a same-year interval with both months March or later, and performs same-calendar date arithmetic only. It does not select a historical calendar, time zone, birth time or location.','evidence':'lilly_fifth_house_reference.py; INDEPENDENT_TEST.txt'},
 {'id':'ADD008','verdict':'PASS','candidate_target':'Immutable candidate identity','reason':'The supplied candidate manifest hash matched, and the manifest file entries were verified before diagnosis. The manifest hash remains unchanged after the independent test run.','evidence':'CANDIDATE_MANIFEST.json; diagnostic receipt'},
 {'id':'ADD009','verdict':'PASS','candidate_target':'Independent rerun versus new tests or outcomes','reason':'The independent rerun executed the same 36 tests with exit0. It supplies a reproduction receipt, not 36 additional tests or any new historical outcomes.','evidence':'INDEPENDENT_TEST.txt'},
 {'id':'ADD010','verdict':'PASS','candidate_target':'Source aggregation and evidence status','reason':'The 12 sex testimonies, five bodily marks and multiple timing/transit statements remain nested within two enquiries; the source does not supply independent observations for each role or a prospective accuracy denominator.','evidence':'Original PDF272–276; HISTORICAL_CASES.json; RULES.json case and evidence fields'}
]
rule_checks=[]
for r in rules:
 local=r.get('local_id',r.get('source_fields',{}).get('id'))
 fail=local in {'B039','C012'}
 rule_checks.append({'id':r['id'],'local_id':local,'verdict':'FAIL' if fail else 'PASS',
 'check':'Source conditions, conjunction/disjunction scope, attribution, exceptions, uncertainty and case/evidence status compared with the frozen whole-span reading.',
 'finding':'ADD002' if local=='B039' else 'ADD001' if local=='C012' else None,
 'source_locator':r.get('source_locator')})
npass=sum(x['verdict']=='PASS' for x in checks);nfail=94-npass
result={
 'review_id':'B02j-independent-candidate01',
 'candidate_manifest_sha256':'231a5999daa39c7cc14253a3ed6f10b9a78dfe092678685f556443f57a0c32db',
 'status':'FAIL_PENDING_TARGETED_SOURCE_CORRECTION_AND_EVIDENCE_RECONCILIATION',
 'verdict_semantics':{
  'PASS':'The whole ledger unit is supported within the stated source/packet boundary, including its qualifications; not empirical validation.',
  'FAIL_SOURCE_FIDELITY':'A source interpretation or prerequisite has been added without adequate source support or labeling.',
  'FAIL_EVIDENCE_NOT_DISCLOSED':'A checkable part of the unit cannot be established from disclosed evidence; this does not mean it is known false.',
  'release_requirements':'CL091 and CL093 are evaluated as requirements per owner instruction, not as completed publication/delivery assertions.'
 },
 'counts':{'report_claim_units':94,'report_pass':npass,'report_fail':nfail,'source_fidelity_failed_units':2,'missing_disclosure_failed_units':5,'additional_checks':len(additional),'additional_pass':8,'additional_fail':2,'canonical_rows_read':201,'canonical_row_pass':199,'canonical_row_fail':2,'independent_tests_run':36,'independent_test_exit_code':0},
 'claims':checks,'additional_checkable_candidate_assertions':additional,'canonical_rule_checks':rule_checks,
 'global_limits':[
  'Same-model fresh-context independence only; no different-family or external-expert review.',
  'No empirical validation, independently collected outcomes, historical ephemeris rerun or personal prediction.',
  'All original admitted page images PDF256–276 were read before candidate disclosure. Diagnostic reinspection was targeted.',
  'PDF67,177,178,888 diagnostic image emissions were attempted but returned a context-truncated result; they are not claimed as certified diagnostic visual reads. Retained source transcriptions support the corresponding bounded comparisons.',
  'Earlier retained Ptolemy records and producer/reconciliation chronology were withheld or absent; explicit evidence-gap failures are preserved.',
  'No final delivery archive, publication, provider copy, permissions or owner usability run is certified here.',
  'No omitted substantive source section was found; this is a bounded semantic audit, not a new diplomatic edition or exhaustive future proof of completeness.'
 ]
}
(out/'CLAIM_CHECK.json').write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
table='\n'.join('| '+x['id']+' | '+x['verdict']+' | '+x['reason'].replace('|','/')+' |' for x in checks)

diagnosis=f"""# Independent diagnosis: Lilly B02j, candidate 01

## Decision

**FAIL pending two targeted source-fidelity corrections and five bounded evidence reconciliations.** Of 94 literal report claim units, **{npass} PASS and {nfail} FAIL**. Two failed units concern unsupported source normalization. Five concern facts whose supporting records were not disclosed in the independent packet; these are not findings that those facts are false. The canonical semantic review covered all 201 rows: 199 pass within the stated bounds and two require correction or explicit qualification. The independent rerun completed the existing 36 tests with exit code 0.

This diagnosis was frozen before any producer rationale, earlier diagnostic judgment or repair history was disclosed. It is a same-model review in a fresh information state. It is not a different-model-family review, expert adjudication or empirical validation of astrology.

Candidate: /workspace/scratch/43f75264c32e/review-candidate-01/B02j/
Manifest SHA256: 231a5999daa39c7cc14253a3ed6f10b9a78dfe092678685f556443f57a0c32db

## 1. Source-fidelity findings

### F01 — Unqualified anatomical identification

CL050 and C012 / LI.1647.II.XLII.R1330 name a genital region or genital member. The original body-mark sentence on PDF273 / printed239 says **“one in or neer the member signified by the [Moon] in [Virgo]”**. The sentence does not identify that member as genital. The candidate supplies no separate, checked anatomical mapping for this identification and labels the row as a normalized source paraphrase rather than an interpretation.

Preserve the source phrase, or use a neutral body-part formulation and explicitly identify any proposed anatomical interpretation and its evidence. Do not silently replace this with a different specific organ. This is a local classification defect; the count of five reported marks, their placement within one encounter, the querent's reported confirmation and the absence of a separate navel cause in that sentence are supported.

Evidence: original PDF273 lower paragraph, rechecked in independent-review/diagnostic-pdf273-277-contact.png; RULES.json C012 title, source_statement and source_fields.assertion; AUDIT_REPORT.md / CL050. The frozen SOURCE_FIRST_NOTES.md contains no genital identification and remains unchanged.

### F02 — Added evidentiary qualifier for prior assurance

B039 / LI.1647.II.XL.R1271 states that conception has not **independently** been assured before the question. The source on PDF267 / printed233 supplies assurance of conception **before the question**. It does not state an independent-verification requirement. The adjacent B040 correctly preserves the temporal assurance condition without that addition.

Remove independently, or mark and justify it as an interpretation of the source. The important absence-versus-loss branch is otherwise retained. CL023 fails narrowly because it asserts preservation of the actual prior-knowledge condition while the canonical prerequisite adds an unmarked qualifier. This is not a claim that the candidate reversed the branch or that the source requires a modern diagnostic standard.

Evidence: original PDF267 / printed233; RULES.json B039 prerequisites and source_fields.conditions; B040; AUDIT_REPORT.md / CL023.

## 2. Evidence gaps requiring later reconciliation

| Claim | Missing evidence | What is already established |
|---|---|---|
| CL007 | Countable retained Ptolemy registry or retained index supporting 1,066 | The candidate declares this retained count; it was not re-established from underlying records in this packet. |
| CL008 | The component support missing for CL007 | 1,357 + 1,066 = 2,423 is correct arithmetic. |
| CL015 | Earlier 32-test suite or a checkable retained reconciliation showing the subset relationship | The final suite has 36 distinct tests and passes. Repetition creates no new unique tests. |
| CL089 | Producer source-first freeze files and checkable chronology relative to candidate production | This independent reader's complete source-first reading and frozen-note identity are directly established. The packet reports producer freezes, but that chronology is not independently established here. |
| CL090 | Withheld implementation review and reconciliation for the three reproduced problems and retained repairs | All 36 final tests and the listed bounded interfaces were examined; the suite passes in the independent rerun. |

These failures preserve the disclosure boundary. They do not accuse the producer of an incorrect retained count, invented tests or violated chronology. They should be reconciled after this diagnosis is frozen, in a separate disposition artifact. The diagnosis must not be silently rewritten after seeing those materials.

CL091 and CL093 are treated as release requirements, as instructed by the owner. They are not failed merely because final publication, delivery ZIP or delivery receipts are absent from the blind packet. Conversely, their PASS verdicts do not certify that those future actions occurred.

## 3. Whole-source reconstruction and coverage result

The source-first pass read every original page image from PDF256 / printed222 below the horizontal divider through the end of PDF276 / printed242. It included XXXIX–XLIII, every intervening unnumbered passage, both charts, the sex-testimony table and the final retrospective timing/transit discussion. PDF277 was inspected only as the next-section boundary. The candidate's 27 editorial coverage units account for this extent. No materially omitted heading, unnumbered topic or worked example was found.

The argument begins with natural capacity and question context, moves through selected significators and favorable/adverse configurations, preserves distinct authorities and alternatives, and supplies locally scoped timing rules. The parental and messenger sections change subjects and role assignments rather than extending a single pregnancy rule. The two worked enquiries then illustrate different claim and evidence statuses. The candidate generally preserves that structure.

The review compared all 201 rows for conditions, conjunction/disjunction scope, attribution, exceptions, uncertainty and evidence status. It checked the natural-cause and hereditary restrictions; essential versus accidental strength; reciprocal dignity asymmetry; sixth/eighth/twelfth-lord conditions; prior-conception branches; multiple-child family history; anonymous variant attribution; local timing units; separate mother/child endpoints; parent–child reconciliation; and the different envoy, money-message and foot-post roles. Apart from F02's added word, no additional material condition loss or reversal was identified in this bounded reading.

The rule counts are source inventory, not independently observed outcomes. Case reports, general rules embedded in case discussions and several roles of the same planet retain different statuses. A 201-row inventory is not a 201-case dataset. Evidence: frozen SOURCE_FIRST_NOTES.md; SECTION_COVERAGE.json; RULES.json; CLAIM_CHECK.json canonical_rule_checks.

## 4. Worked figures, arithmetic and outcome status

The coordinate audit retained the first figure's unequal third/ninth cusp minutes, inferred signs and conditional part calculations. In the second figure, the chart's unprinted Mercury minutes remain missing, while the later arithmetic table supplies 00 as a separate witness. The chart's Moon hour notation and the sex table's Jupiter-hour rows are preserved as inconsistent witnesses. The solar longitude differs by four minutes between the figure and retrospective prose; both conditional Fortune calculations remain labeled.

Diagnostic reinspection of the original PDF274 supports Jupiter in Gemini at 15:20 and the fourth/tenth cusp pair at Sagittarius/Gemini 2:20. This resolves uncertainty in the earlier low-resolution source reading; it does not change the immutable source notes or repair the candidate.

The printed sex table totals eight male and four female rows. Its roles reuse bodies and derivations. The conditional replacement of both Jupiter-hour-related votes with female votes yields 6:6 only under the explicitly stated dependency assumption. This is a sensitivity calculation, not an authorial correction or an independently weighted probability.

The Moon square gap is 14 degrees47 minutes and the Mercury conjunction gap is 13 degrees37 minutes, differing by 1 degree10 minutes. Degree/week is local to the worked example. It is kept distinct from the Part of Children's ascensional day/degree rule and the neighboring sign/month discussion. The source does not provide an exact averaging, rounding, selection or tolerance rule joining these alternatives.

The reported April7-to-July11 interval is 95 days on the same-calendar assumption, or 13 weeks4 days. No UTC conversion, calendar selection, exact birth time or location is manufactured. Birth-day transit statements are retrospective supporting narration. They are not additional prospective predictions and were not independently regenerated from an ephemeris.

The first enquiry supplies a negative judgment about past and future fertility without a lifetime endpoint demonstrating that prediction. Its five reported marks remain within the same retrospective encounter; F01 concerns the normalization of one mark. The second enquiry supplies the author's male-result statement and a reported delivery date. Neither narrative provides prospective sampling, independent verification or a calibrated error rate.

Evidence: original PDF272–276; WORKED_NUMERIC_TABLES.json; ARITHMETIC_CHECKS.json; HISTORICAL_CASES.json; CROSS_SOURCE_COMPARISONS.json; lilly_fifth_house_reference.py.

## 5. Reference implementation and verification

The complete reference code and test file were read. The code provides bounded arithmetic, named timing conversions, explicit dependency-group inputs and labeled sensitivity calculations. It is not a runtime interpretation engine. Inputs that the source or historical record does not supply are not filled by the helper.

The independent execution ran the same 36 tests in the frozen candidate directory with bytecode writing disabled. Exit code was 0. The output is retained in independent-review/INDEPENDENT_TEST.txt. This verifies the tested interfaces and reproduces the final suite result; it does not establish the withheld earlier repair history, add new tests to the inventory or validate the astrology.

The supplied manifest hash and its declared file entries were checked. The manifest remains unchanged after the independent test run. No candidate, project or git files were edited.

## 6. Remaining weaknesses and unexamined areas

The strongest remaining substantive weakness is the interpretation of seventeenth-century vocabulary, compact glyphs and partly explicit conditions. The audit identifies the two specific unmarked normalizations above, but a same-model reader can share other normalization assumptions with the producer. Preserving qualified source readings is therefore essential.

All admitted source images were read before candidate disclosure, but diagnostic emissions of PDF67, PDF177, PDF178 and PDF888 returned a context-truncated result. Those four earlier/errata pages are not claimed as certified diagnostic visual reads. The corresponding retained-source and errata transcriptions were read and support the bounded comparison claims; the original-page visual certainty of those particular cross-references is a remaining weakness. The PDF273/PDF277 contact image was successfully reopened afterward.

Earlier Ptolemy records, the full semantic accuracy of earlier Lilly batches, producer freeze chronology, prior diagnostics and implementation repair history were not examined. No other edition, independent historical birth record or modern ephemeris was consulted. Final archive bytes, publication, remote access permissions and delivery usability are release-stage checks outside this freeze.

No empirical prediction accuracy, clinical interpretation or personal forecast is offered. Source completeness here means the bounded extent and semantic checks described above; it is not a claim that every possible future textual ambiguity has been exhausted.

## 7. Every literal report claim

The full literal text, verdict category, reason and retained anchors for each unit are in CLAIM_CHECK.json. A FAIL for undisclosed evidence is separate from a source-fidelity failure.

| Unit | Verdict | Reason |
|---|---|---|
{table}

## 8. Additional checkable candidate assertions

CLAIM_CHECK.json adds ten checks beyond the paragraph/table-row ledger: the two canonical normalization defects; canonical identity/runtime/evidence flags; preservation of all45 coordinate witnesses; the disputed second-chart glyph readings; timing/dependency interfaces; calendar scope; immutable candidate identity; independent test reproduction; and dependent aggregation. Eight pass and two fail. These additions make canonical consequences explicit instead of limiting diagnosis to report prose.

## Freeze and disposition rule

SOURCE_FIRST_NOTES.md and SOURCE_FIRST_RECEIPT.json retain their original hashes. DIAGNOSIS.md, CLAIM_CHECK.json and DIAGNOSTIC_RECEIPT.json form this independent freeze. The receipt records their identities, the source and candidate identities, the successful test run and the disclosure boundary. Any producer response, additional evidence or repair should follow in a separate reconciliation artifact.
"""
(out/'DIAGNOSIS.md').write_bytes(diagnosis.encode('utf-8'))
assert sha(out/'DIAGNOSIS.md')=='441e323308ee681a5649fdc90294e3cc388bfd7762c559e4da3cb059e0ddbb9c'
assert sha(out/'CLAIM_CHECK.json')=='043662b0cbaa3ec2a7fdb4f595bca40999adf2beb54ab825595c98fe72bb049b'

critical=['CANDIDATE_MANIFEST.json','AUDIT_REPORT.md','CLAIM_LEDGER.json','RULES.json','SECTION_COVERAGE.json','WORKED_NUMERIC_TABLES.json','lilly_fifth_house_reference.py','test_lilly_fifth_house.py','TEST_RUN_SUMMARY.json','TEST_B02j.txt','READING_RECEIPT.json','ERRATA_CHECKS.json','RETAINED_SOURCE_EXCERPTS.json','COUNTS.json']
manifest_hash='231a5999daa39c7cc14253a3ed6f10b9a78dfe092678685f556443f57a0c32db'
candidate_hashes={f:(manifest_hash if f=='CANDIDATE_MANIFEST.json' else sha(p/f)) for f in critical}
artifacts={}
for f in ['DIAGNOSIS.md','CLAIM_CHECK.json','INDEPENDENT_TEST.txt']:
 artifacts[f]={'path':oldout+'/'+f,'sha256':('5c51f3f95966001bd74435559c3a7fdb700acced1fd4a94d7806bae4d821b333' if f=='INDEPENDENT_TEST.txt' else sha(out/f)),'bytes':(5769 if f=='INDEPENDENT_TEST.txt' else (out/f).stat().st_size)}
receipt={
 'review_id':'B02j-independent-candidate01',
 'freeze_kind':'independent_diagnosis_before_reconciliation',
 'reviewer':'/root/fifth_independent',
 'diagnostic_start_utc':'2026-10-10 12:20:04 UTC',
 'source':{'path':'/workspace/scratch/bd2460f96de0/Lilly-1647-Christian-Astrology-I-III.pdf','sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b','page_count':894,'bytes':141842963,'admitted_pdf_pages':list(range(256,277)),'start_boundary':'PDF256 below divider at Of the fifth House, and its Questions','end_boundary':'end PDF276 before PDF277 sixth-house/XLIV introduction'},
 'source_first_freeze':{'SOURCE_FIRST_NOTES.md':'68dacb1f4342ffcffbac1f2fa9fe50c1180d337113a373bb3dff4682d5b6b69a','SOURCE_FIRST_RECEIPT.json':'119a50307c41ce4aeba1037761912c97763c40e7bb8c2ea8bffd9359b2e3f262'},
 'candidate_directory':oldp,
 'candidate_hashes':candidate_hashes,
 'diagnosis_artifacts':artifacts,
 'image_read_disclosure':{
  'source_first_all_admitted_original_page_images_read':True,
  'source_first_additional_detail_pages':[258,272,274,276],
  'diagnostic_confirmed_reinspections':['original high-resolution PDF274','PDF273 lower body-mark paragraph','PDF277 opening boundary'],
  'diagnostic_context_truncated_image_emissions_not_claimed_as_certified_reads':[67,177,178,888],
  'retained_transcriptions_for_these_cross_references_read':True,
  'no_other_edition_or_external_browsing':True},
 'firewall':{
  'source_first_notes_frozen_before_candidate_access':True,
  'all94_candidate_claims_read':True,'all201_canonical_rows_read':True,
  'producer_rationale_read_before_freeze':False,
  'previous_diagnoses_read_before_freeze':False,
  'implementation_repair_history_read_before_freeze':False,
  'producer_source_note_contents_read_before_freeze':False,
  'same_model_fresh_context_only':True,'cross_family_review':False,'external_expert_review':False,
  'empirical_validation':False,'repo_changes':False,'candidate_changes':False,'publication_performed':False},
 'result_counts':result['counts'],
 'test_result':{'exit_code':0,'tests':36,'independent_log':'INDEPENDENT_TEST.txt','command':'python -m unittest -v test_lilly_fifth_house','bytecode_writing_disabled':True,'same_unique_suite_not_new_tests':True},
 'limits':result['global_limits'],
 'tool_budget_note':'Diagnostic phase bounded to 20 substantive nested tool calls, including the final artifact freeze; source-first phase preceded this budget.',
 'reconciliation_rule':'Keep later evidence, producer response, repairs and dispositions separate; do not overwrite this diagnostic freeze.'
}
receipt['freeze_utc']='2026-10-10 12:31:32 UTC'
receipt['elapsed_seconds']=688.957976
(out/'DIAGNOSTIC_RECEIPT.json').write_bytes((json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
for f in ['DIAGNOSIS.md','CLAIM_CHECK.json','DIAGNOSTIC_RECEIPT.json']:
 print(f,sha(out/f),(out/f).stat().st_size)
assert sha(out/'DIAGNOSTIC_RECEIPT.json')=='3893bf6b680c48686df2aacafbbaf1ef8c452a40dead8adc0c4788805716318a'
