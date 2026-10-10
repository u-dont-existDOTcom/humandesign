# B02i independent claim diagnosis

**Frozen first diagnosis.** This evaluates the exact report and ledger named below, before any reconciliation. It is diagnostic only and grants no edit, merge, publication or delivery authority.

## Result

All 55 ledger claims were checked: **50 pass, 1 fail, 4 unresolved**. Five missed checkable claims were added. The failing ledger claim and two report passages concern the same optional-input wording issue; one additional quotation-fidelity defect is distinct. Unresolved outcomes identify the admitted evidence boundary and are not findings that the underlying actions did not happen.

No substantive current-span source-transcription or arithmetic error established in the report. The Fortune 9-degree discrepancy, conditions, chronology and author qualifications survive direct checking.

## Exact target and source identities

| Item | SHA256 |
|---|---|
| AUDIT_REPORT.md | `9b1b6d5c3ed53aee4d584215b3443d356e8b65fdca8f06820a79605e36aaab44` |
| CLAIM_LEDGER.json | `dc2dfc48e7723a1782e609d3a26bfe30a0242737a2a2bfb7b4e0ee2d5939f442` |
| Lilly original PDF | `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b` |

The admitted source is PDF236 / printed202 through the final fourth-house paragraph above the divider on PDF256 / printed222. The fifth-house heading and XXXIX below that divider are the next source unit. Original PDF888 was read only for the targeted errata question. The original contains 894 pages.

## Material findings and narrow resolutions

### F01: confirmed_report_overstatement (moderate)

Affected claims: CL014.

Shared physical bodies are exposed only when optional body identities are supplied. Both report passages omit that prerequisite. CL050 passes because its narrower ledger wording does not contain this extra assertion.

Qualify the two report passages and CL014 with when body identifiers are supplied. No wider implementation or test expansion is required for that wording repair.

### F02: quotation_fidelity (low)

Affected claims: ADD001.

One continuous source quotation is shortened without marking the omission.

Use a paraphrase without quotation marks or the exact contiguous source wording.

### L01: evidence_boundary (scope_limit)

Affected claims: CL006, CL052, CL054, CL055, ADD003, ADD004.

Certain earlier process, whole-turn negative, preservation and delivery assertions go beyond what the permitted receipts independently prove.

Attribute these statements explicitly to their receipts, or bind an already existing authoritative comparator/chronology/delivery receipt. This diagnosis does not request new suites, participant reads, another complete source pass or a new approval gate.

### A01: anchor_precision (low)

Affected claims: CL030, CL036.

Coal example needs PDF251/R1107; the seller-daughter episode needs PDF255. The report substantive claims are correct and its broader chapter citations contain the evidence.

Add the missing precise ledger page/record anchors.

## Claim-by-claim dispositions

### CL001 - PASS

**Claim:** B02i completes the fourth-house heading/preamble and XXXII–XXXVIII on PDF236–256 above the divider; the fifth-house heading and XXXIX below it are next.

Original PDF236 begins the fourth-house heading/preamble and XXXII. Original PDF256 ends XXXVIII above the divider, then prints the fifth-house heading and XXXIX. All intervening headings and subsection passage anchors are represented in the 148-record coverage inventory. This establishes the report boundary, not an exhaustive validation of every nested record field.

**Evidence:** Original PDF236-256, especially 236,238,244,246,248,249,253,256; RULES.json passage anchors R1009-R1156; SECTION_COVERAGE.json; LILLY_SOURCE_EXTRACTION_INDEX_V1.json next.

### CL002 - PASS

**Claim:** There are 148 new records R1009–R1156:119 general/method/illustrative and29 worked-narrative; cumulative Lilly1156 plus retained Ptolemy1066 equals2222.

Counted 148 unique contiguous IDs R1009-R1156. Exactly 29 have chapter XXXVIII IDs; the other 119 are the general/methodological/illustrative block. The current Lilly index says 1156 and the retained Ptolemy index says 1066; their sum is 2222. These are inventory totals.

**Evidence:** RULES.json; LILLY_SOURCE_EXTRACTION_INDEX_V1.json; PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json; MECHANICAL_EVIDENCE.json /inventory.

### CL003 - PASS

**Claim:** The issue ledger preserves50 unresolved limits and6 separately source-resolved readings; these are not50 demonstrated author errors.

The actual issue arrays contain 50 unresolved items and 6 separately resolved readings. Their contents include missing definitions, grammar, source conventions, retrospective evidence limits and one Fortune discrepancy; interpreting all 50 as demonstrated author errors would be false, and the report explicitly avoids that.

**Evidence:** UNRESOLVED.json /issues and /resolved_readings.

### CL004 - PASS

**Claim:** There is one printed chart/one dated enquiry,22 transcribed coordinate entries,21 extraction-page images read and an additional PDF888 errata check.

The admitted original span contains one chart, dated to one enquiry on PDF253, with 12 cusps, 7 planets, 2 nodes and Fortune. I inspected all 21 admitted page images and the separate PDF888 image. Their hashes match the reading receipt. The receipt also documents the producer inspection; my observation does not independently prove every earlier viewing action.

**Evidence:** Original PDF236-256 and PDF888; WORKED_NUMERIC_TABLES.json /charts/0; READING_RECEIPT.json; MECHANICAL_EVIDENCE.json /images_match_receipt.

### CL005 - PASS

**Claim:** The retained original has894 pages; its full SHA256 was recomputed this turn and matched2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b.

pdfinfo reports 894 pages and 141842963 bytes. My complete SHA256 recomputation matches the supplied original identity. Thus the current source identity and current-turn recomputation are directly established; the producer earlier act remains described by its receipt.

**Evidence:** Original Lilly PDF; READING_RECEIPT.json; Initial evaluator SHA256 command and pdfinfo output.

### CL006 - UNRESOLVED

**Claim:** Root read236–255 fully and256 fourth-house ending against original images, using existing text only as aid; no new OCR/source edit; three readers froze source-first notes before candidate production.

The reading receipt declares the page-reading boundary and no new OCR; the actual original remains hash-identical. The saved test verifies three expected note hashes and candidate-copy equality. None of those checks proves that three separate reader contexts froze their notes before candidate production, and the permitted information boundary excluded the underlying reader records and chronology. The earlier viewing/OCR history and source-first chronology are therefore documentary assertions, not independently established events in this gate.

**Evidence:** READING_RECEIPT.json; test_lilly_fourth_house_audit.py source-note hash and candidate-copy tests; TEST_B02i.txt.

| Component | Disposition | Reason |
|---|---|---|
| Current original source identity and declared reading scope | PASS | Current hash and page-image identities are verified. |
| Actual earlier viewing sequence and absence of all new OCR | UNRESOLVED | Declared by receipt; underlying execution history excluded. |
| Three separate contexts froze notes before candidates | UNRESOLVED | Hash equality demonstrates retained bytes, not temporal order or context independence. |

### CL007 - PASS

**Claim:** Root received the chart reader coordinate summary before its chart reread; that reread is verification after exposure, not a second independent transcription.

The report accurately discloses the exposure stated in READING_RECEIPT.json and conservatively refuses to count the root chart reread as a second independent transcription. This passes as a documented self-disclosure and appropriate evidence classification; I did not independently reconstruct the message chronology.

**Evidence:** READING_RECEIPT.json /exposure; AUDIT_REPORT.md How the source was checked.

### CL008 - PASS

**Claim:** Inventory records may contain multiple branches or methods and are not148 independent predictions/cases.

The record kinds include method instructions, conditional doctrine, a figure, aggregate accounts and dependent episodes. Every record has independent_evidence_unit=false. The original has one actual chart, not 148 independent predictions or cases.

**Evidence:** RULES.json kinds and independent_evidence_unit; Original PDF236-256; HISTORICAL_CASES.json; MECHANICAL_EVIDENCE.json /inventory.

### CL009 - PASS

**Claim:** Own goods useL2, sibling goodsL4, father goodsL5, mother goodsL11; later literalL2 wording does not restate a complete substitution algorithm.

PDF236 explicitly gives own goods to lord 2, sibling goods to lord 4, father goods to lord 5 and mother goods to lord 11, followed by continuation according to the party. The subsequent location text returns to literal lord-of-second wording and supplies no fully restated recursive substitution procedure.

**Evidence:** Original PDF236-238, XXXII opening and continuation; RULES.json R1010.

### CL010 - PASS

**Claim:** Tenth-house object locations vary with occupation; elemental descriptions have conditions, including outside placement already indicated and strong former significators for the watery clause.

PDF236 differentiates mechanic, gentleman and husbandman for a tenth-house location. PDF237 attaches the raised-ground/tree and bridge/stile alternatives to an already outside location and expressly requires the former significators to be strong for the watery branch. The report preserves these restrictions.

**Evidence:** Original PDF236-237; RULES.json R1011-R1016.

### CL011 - PASS

**Claim:** The earlier-astrologer hour-lord method startsH10/H11, leavesH12 unspecified, and Lilly criticizes its exactness.

The first old hour-lord branch literally names houses 10 and 11; house 12 is not named. The remaining branches use between-house language without an endpoint policy. Lilly immediately says he has not found this judgment very exact.

**Evidence:** Original PDF237, hour-lord paragraph and following criticism; QUERY_REFERENCES.json ancient_hour_lord_rule.

### CL012 - PASS

**Claim:** The eight-slot method is introduced for mislaid things inside a house, not stolen:ASC,L1,H4,L4,Moon,H2,L2,Fortune; greater number picks quarter; ties and weights are not defined.

The introduction spans PDF237-238 and restricts the new procedure to things missing in a house and not stolen. The printed list has exactly Ascendant, Ascendant lord, fourth cusp, fourth lord, Moon, second cusp, second lord and Fortune. Greater number of testimonies selects the quarter; no weights or tie rule are supplied in the entire local passage.

**Evidence:** Original PDF237-238; RULES.json R1018-R1019; QUERY_REFERENCES.json /mislaid_slots.

### CL013 - PASS

**Claim:** The sign-direction table gives AriesE,LeoEbyN,SagittariusEbyS,LibraW,GeminiWbyS,AquariusWbyN,CancerN,ScorpioNbyE,PiscesNbyW,CapricornS,TaurusSbyE,VirgoSbyW; it also explicitly mentions fugitives.

All twelve directions match the original four-line table: Aries east; Leo east by north; Sagittarius east by south; Libra west; Gemini west by south; Aquarius west by north; Cancer north; Scorpio north by east; Pisces north by west; Capricorn south; Taurus south by east; Virgo south by west. Its introduction expressly includes fugitives.

**Evidence:** Original PDF238 direction table; QUERY_REFERENCES.json /directions.

### CL014 - FAIL

**Claim:** No exact azimuths or tie-break are supplied; reference tally exposes repeated planetary roles without treating slots as independent evidence.

The no-azimuth, no-tie-break and no-independent-evidence claims pass. The unconditional claim that repeated physical bodies are exposed needs an input qualifier: body identifiers are optional in mislaid_direction_tally. With all eight signs supplied and no body IDs, shared_body_slots is empty; adding Moon as the body for AscendantLord and Moon reveals the duplicate without changing the tally. The report should say repeated roles are exposed when body identifiers are supplied. This is a wording/input-boundary defect, not a false numeric count or a predictive claim.

**Evidence:** AUDIT_REPORT.md section 1, paragraph following direction table; lilly_fourth_house_reference.py mislaid_direction_tally; test_lilly_fourth_house_reference.py TestimonyTests; MECHANICAL_EVIDENCE.json /repeated_body_identifier_reproduction.

| Component | Disposition | Reason |
|---|---|---|
| No exact azimuth or invented tie-break | PASS | Both absent in source and helper. |
| Repeated body visibility without any input qualification | FAIL | body is optional; omitted IDs yield an empty shared_body_slots object. |
| No independent-evidence relabeling | PASS | independent_evidence_count remains null in both reproductions. |

### CL015 - PASS

**Claim:** Glove/book experiments are an unspecified experience account lacking individual dates/charts, attempt denominator and failures.

The original ends the procedure with an occasional glove/book experience account, not enumerated dated trials. No individual chart, denominator, failure tally or dated attempt appears in the complete XXXII passage.

**Evidence:** Original PDF236-238, especially PDF238 final XXXII paragraph; HISTORICAL_CASES.json unspecified_experience_accounts.

### CL016 - PASS

**Claim:** Purchase frame:H1buyer,H4property,H7seller,H10price; Moon separation/application planets additionally buyer/seller, Moon also property.

The four purchase assignments span PDF238-239: first/buyer, seventh/seller, fourth/property, tenth/price. The source explicitly adds the planet from which Moon separates to buyer, the planet to which it applies to seller, and Moon to property.

**Evidence:** Original PDF238-239, XXXIII opening assignments; RULES.json R1023; QUERY_REFERENCES.json /property_frames/purchase.

### CL017 - PASS

**Claim:** Land quality frame:H1tenants/farmers,H4soil/land/buildings,H7herbage/plants/crops,H10timber. Rental:H1tenant,H4end,H7lessor,H10profit.

Land quality gives first to tenants/farmers, fourth to soil/buildings, seventh to herbage and later smaller plants/crops, and tenth to wood/trees. Rental gives first to hirer, seventh to lessor, tenth to profit and fourth to the end. The report table preserves the context changes.

**Evidence:** Original PDF240-243; RULES.json R1032,R1044; QUERY_REFERENCES.json /property_frames.

### CL018 - PASS

**Claim:** Hard-aspect purchase application/translation may conclude with argument, breakdown threats and delay; Moon placement/reception alternatives remain textually compressed; broker path has vacancy and transfer prerequisites.

PDF239 allows final bargaining through square/opposition with many words, threatened breaking off and time. Its next paragraph compresses reception and placement alternatives and leaves the isolated Moon placement elliptical. The broker clause explicitly requires the stated house occupations to be absent and Moon to transfer fourth lord light to first lord. The source, record R1027 and linked issues preserve ambiguity rather than settling a unique Boolean rule.

**Evidence:** Original PDF239; RULES.json R1026-R1029; UNRESOLVED.json B02i-A-U01 and B02i-A-U15.

### CL019 - PASS

**Claim:** Timber usesL10 only ifH10empty; motion matters; own house viz fourth denotes mundaneH4; sea-bank concern adds proximity to sea.

The semantic claims match the originals: tenth-lord timber assessment follows an empty Midheaven; direction/retrogradation distinguish wood and tenant outcomes; the own-house gloss explicitly identifies the fourth mundane house; and sea-bank concern is conditional on proximity to sea. A separate added finding below concerns the report exact-quotation formatting of the own-house phrase, not this semantic reading.

**Evidence:** Original PDF240-242; RULES.json R1031,R1033-R1042; ADD001.

### CL020 - PASS

**Claim:** Rental favourableL1 aspect uses a moiety of its own orbs, preferably actualASCdegree; final favourableASCglyph is unimpededFortune, unlike northnode in earlier property list.

The source says within a moiety of the first lord own orbs and prefers the actual ascending degree. The final favorable Ascendant glyph on PDF242 is a circled cross, Fortune, with not-impedited condition. The earlier PDF240 property-success glyph is the ascending/north node. They are distinct in the originals.

**Evidence:** Original PDF240 and PDF242-243; RULES.json R1031,R1045.

### CL021 - PASS

**Claim:** AdverseH7occupant clause excludesL7 itself; already-rented regret, not-yet-rented refusal and taking/passing-on differ.

PDF243 expressly exempts an occupant that is lord 7 from the adverse seventh-house occupant clause. The first-house infortune passage separately distinguishes regret after taking, unwillingness before taking and taking followed by promptly passing the bargain on.

**Evidence:** Original PDF243; RULES.json R1046-R1051.

### CL022 - PASS

**Claim:** Father isH4; his movable/personal estateH5; reception statement includes exchange of second/fifth-lord house placements.

PDF244 gives the father to house 4 and his personal estate/movable goods to house 5. It states reception together with lord 5 in house 2 and lord 2 in house 5; the record retains all three rather than replacing them with arbitrary mutual reception.

**Evidence:** Original PDF244; RULES.json R1052-R1053.

### CL023 - PASS

**Claim:** Wait for relevant planet to leave sign when father reluctant; urgent alternative requires direct/swift/oriental and specified contacts.

The wait/urgent alternatives on PDF245 are accurately summarized. Their context is an undignified infortune in house 4; the urgent alternative keeps directness, swiftness, oriental position and sextile/trine to Jupiter, Venus or first lord. R1062 explicitly preserves the present-means and cannot-wait prerequisites.

**Evidence:** Original PDF245; RULES.json R1061-R1062.

### CL024 - PASS

**Claim:** Observing times does not itself enforce father will; Lilly instead claims more benevolent inclination.

Immediately after the urgent timing advice Lilly expressly denies that observing the times by themselves enforces the father mind or will, then asserts more benevolent inclinations. Both propositions are preserved.

**Evidence:** Original PDF245; RULES.json R1063.

### CL025 - PASS

**Claim:** RetrogradeL5 may indicate intended provision wasted/assigned elsewhere; retrograde applicationL2/L5 may indicate sudden receipt, with actor grammar unresolved.

PDF244 associates retrograde lord 5 with some intended provision wasted or disposed otherwise. PDF245 associates good-aspect application by retrogradation between lords 2 and 5 with unexpected receipt. The latter sentence does not resolve which actor or both actors supply retrogradation; retaining that uncertainty is faithful.

**Evidence:** Original PDF244-245; RULES.json R1054,R1064; UNRESOLVED.json B02i-A-U07.

### CL026 - PASS

**Claim:** Relocation reasons differ by lord, including illness/servants, slander, finances, trade/reputation, house and rivals; marginal practical trade-location explanation remains.

The original gives sixth-lord sickness/servants, twelfth-lord slander, second-lord/part-of-Fortune financial decline, tenth-lord trade/reputation, fourth-house bad-house/repair issues and seventh-lord competitors. The starred margin on PDF247 explicitly adds inconvenient trade location.

**Evidence:** Original PDF246-247; RULES.json R1066-R1075.

### CL027 - PASS

**Claim:** No-regret/thanks/rewards memory is aggregate without sample or independent confirmations; angels/curses/expiation are historical theological explanation, not empirical evidence.

Lilly presents no-regret/thanks/rewards as his memory, without an enumerated denominator or independent confirmations. The angels, curses, expiation and families material is explicitly author opinion and claimed experience. The report correctly treats these as historical explanation/testimony rather than empirical validation or a new remedy.

**Evidence:** Original PDF247-248; RULES.json R1076-R1077; HISTORICAL_CASES.json.

### CL028 - PASS

**Claim:** Waterwork opening favourable conditions include Saturndirect/swift/oriental, specifiedMoonhouses and noMarsaspect; ascending in latitude has no locally specified numeric convention.

The favorable combination explicitly includes direct, swift, oriental Saturn, Moon in 3/11/5 and no good or evil Mars aspect. The report does not settle the no-Mars subject. The receiving fortune ascending in his latitude is printed; the local chapter does not define a numerical convention. R1082 and the issue ledger preserve the subject/definition limits.

**Evidence:** Original PDF248-249, complete XXXVI; RULES.json R1082,R1084; UNRESOLVED.json B02i-B-I06,B02i-B-I08.

### CL029 - PASS

**Claim:** Rain list is Cancer,Leo,Aquarius,Pisces; replacingLeo withScorpio would alter source. AdverseH10 waterworks sentence continues onto249 and concerns pipes/banks,flow and design.

The four rain glyphs are Cancer, Leo, Aquarius, Pisces. The adverse tenth-house sentence crosses the page break and concerns broken pipes/banks, interrupted running and an ill-laid plan. Both clauses are verified directly; Scorpio is not in this printed list.

**Evidence:** Original PDF248-249; RULES.json R1086-R1087.

### CL030 - PASS

**Claim:** Treasure questions distinguish own hidden goods, owner/relation, unidentified treasure and specified mineral; coal specified in question cannot be treated as chart-discovered identity.

The opening treasure passage differentiates owner, hider relationship, unspecified treasure and a specified mineral question. The coal-specific example is actually on PDF251, and supports the report inference that coal named in the question is prior input rather than a chart-discovered identity. The ledger should add PDF251/R1107 to its anchors; its current PDF249/R1088 anchor alone does not contain that example.

**Evidence:** Original PDF249 and PDF251; RULES.json R1088,R1107; APPLICABILITY_AND_RELATIONS.json.

### CL031 - PASS

**Claim:** Qualified Saturn/Mars may indicate treasure; full maxim says own-house/essentially-dignified significator is not unfortunate; nearby directness/impediment conditions and earlier qualifications remain.

PDF250 explicitly permits Saturn/Mars in their own houses, direct, unimpeded and in the fourth, then gives the broad own-house/essentially-dignified-significator maxim. The current record preserves that broad assertion and adjacent limits. Earlier retrograde/combust/afflicted qualifications are present in the retained R365 record; that earlier original was not independently reopened here.

**Evidence:** Original PDF249-250; RULES.json R1092-R1096; UNRESOLVED.json B02i-B-I11; Retained R365 in RETAINED_SOURCE_EXCERPTS.json.

### CL032 - PASS

**Claim:** Treasurequality initially combines significator withL7when distinct, then offers absoluteL7alternative with ambiguous negation/affinity; both preserved.

The original first combines a separate treasure significator with lord 7, then directs absolute use of lord 7 under the unclear not/or-affinity wording. R1097/R1098 and the issue ledger retain both and do not manufacture unique precedence.

**Evidence:** Original PDF250; RULES.json R1097-R1098; UNRESOLVED.json B02i-B-I10.

### CL033 - PASS

**Claim:** Material lists distinguish dignified/weak cases; original weak-mining glyph isSaturn despite misleading text-layer rendering.

The original material list distinguishes some dignified and weak cases without universally repeating identical prerequisites. In the weak mine paragraph on PDF251 the glyph is Saturn, confirmed by its shape and preceding Saturn context; the supplied text aid renders that glyph misleadingly. The report correctly avoids making that rendering authoritative.

**Evidence:** Original PDF250-251; Text aid p251.txt; RULES.json R1099-R1112.

### CL034 - PASS

**Claim:** Terminal treasure group is attributed toAlkindus and includes presence/acquisition/location/depth/diggingtime. Depth is ordinal sign progress with no physical units or equal-bin scale.

The actual attribution begins with Alkindus on PDF252/R1121. Records R1116-R1120 remain attributed to Lilly; the terminal R1121-R1127 group is attributed to Alkindus or its continuing passage. It covers presence, acquisition, location, depth and digging setup. Depth is shallow near entry and deeper farther through the sign; no physical length, equal bins or ratio appears in the complete local passage.

**Evidence:** Original PDF251-252; RULES.json R1116-R1127 source_attribution; QUERY_REFERENCES.json and lilly_fourth_house_reference.py depth_order.

### CL035 - PASS

**Claim:** Single figure is31March1634,6HorPM; minutes/seconds/latitude/timezone unspecified; author says he lives in one house in1647 and already intended purchase/knew sixmonthnotice requirement.

The diagram shows 31 Mar: 1634 and 6 Hor: P M, without minute, second, latitude or timezone. The prose explicitly says the author lives in one house in 1647, was fully resolved to buy, and knew his own money required six months notice. The report does not turn these into unknown predictions.

**Evidence:** Original PDF253; WORKED_NUMERIC_TABLES.json /charts/0 central and omitted labels; HISTORICAL_CASES.json.

### CL036 - PASS

**Claim:** Negotiation had many meetings and£530noabatement; rival and seller daughter are episodes in same enquiry; margin places rival after beginning/beforeconclusion.

The source reports many meetings and no reduction from 530 pounds. Its rival-purchaser margin says after beginning and before conclusion; the seller daughter episode continues on PDF255. All are within the same enquiry. The ledger should add PDF255 because its current page list has only 254 although it includes R1140.

**Evidence:** Original PDF254-255; RULES.json R1138-R1140; HISTORICAL_CASES.json.

### CL037 - PASS

**Claim:** Friend loan£500 twelve days after as narrated; Mars/Jupiter timing antecedent is qualified, not independently computed.

PDF255 says a friend lent 500 pounds twelve days after in the narrated sequence. The nearest which-he-did antecedent is Mars becoming direct, while Jupiter entering Cancer is in the same preceding sentence. The report and issue ledger keep this qualified and do not claim an independently computed station/ingress date.

**Evidence:** Original PDF255; RULES.json R1142; UNRESOLVED.json B02i-C-U07.

### CL038 - PASS

**Claim:** Bargain25April linkedtoVenusSun;£530payment and sealedconveyance17May linkedtoVenusMoon; separate endpoints with no independent advance-date freeze in these pages.

The same paragraph reports bargaining on 25 April when Venus and Sun conjoined, and payment of 530 pounds with sealed conveyance on 17 May when Venus and Moon conjoined. These are distinct endpoints. Across the complete worked narrative, the source supplies retrospective associations, not an independently preserved advance prediction package.

**Evidence:** Original PDF253-256, specifically PDF255 transaction paragraph; RULES.json R1144-R1145; HISTORICAL_CASES.json.

### CL039 - PASS

**Claim:** Financialinjury but no regret dueattachment/priorhistory are separate outcomes; five marks are selfreports in onecase; oldstronghouses and futurelease/lifetimeexpectations are not all confirmedfutureendpoints.

The narrative identifies exactly five bodily marks, calls the houses old but strong, anticipates leases outlasting his life, says the bargain injured him financially and nevertheless expresses no regret because of his attachment and history. These are correctly separated; the future durability and lifetime expectations have no confirming endpoint in this span.

**Evidence:** Original PDF255-256; RULES.json R1143,R1147-R1155; HISTORICAL_CASES.json.

### CL040 - PASS

**Claim:** Final Wharton employment/marital denials are polemicalautobiography; underlying dispute not adjudicated.

The final paragraph denies occupational and marital claims attributed to Wharton. Classifying this as polemical autobiography rather than resolving the underlying historical dispute is supported by the original; no external adjudication was undertaken in this gate.

**Evidence:** Original PDF256 top paragraph; RULES.json R1156.

### CL041 - PASS

**Claim:** Coordinate table has12cusps,7planets,2nodes,Fortune; body signs inferred from sectors/cuspintervals; Mars/SaturnexplicitRx; absentmarks not verifieddirect;H4/H10minutesnull.

All 22 coordinates are accounted for. The 12 cusp signs are printed; the 10 body/point signs are inferred from sectors and surrounding cusp intervals. The original explicitly marks Mars and Saturn retrograde; other absent marks remain null. H4 and H10 print 18 without a minute. Targeted original-image crops independently resolve Jupiter 25:32, south node Virgo27:48, north node Pisces27:48 and Fortune Pisces12:27.

**Evidence:** Original PDF253; Evaluator crops in crops/; WORKED_NUMERIC_TABLES.json /charts/0.

### CL042 - PASS

**Claim:** Earlier selected Fortune formula usesASC+Moon−Sun bydayandnight; alternate nocturnal convention is distinct, not automaticrepair.

Retained R625 explicitly records Ascendant+Moon-Sun by day and night, while R631 distinguishes the reported reverse nocturnal convention. The report correctly identifies these as retained earlier evidence. This pass is for correspondence with those retained transcriptions, not a new original-page collation of PDF177-178.

**Evidence:** RETAINED_SOURCE_EXCERPTS.json retained R625,R631; CROSS_SOURCE_COMPARISONS.json CMP12.

### CL043 - PASS

**Claim:** Libra13:45+Virgo10:38−Aries20:56 reduces toPisces3:27; printedFortunePisces12:27 differs9degrees/540minutes; inputsunchanged,causeunresolved.

Independent integer-arcminute arithmetic from the visually checked inputs yields 20007 arcminutes = Pisces3:27. Printed Pisces12:27 is 540 arcminutes, or 9 degrees, farther. The current table keeps the printed input and no cause is established. Candidate calculation code is not used as the authority for this independent recomputation.

**Evidence:** Original PDF253; WORKED_NUMERIC_TABLES.json; MECHANICAL_EVIDENCE.json /independent_arithmetic.

### CL044 - PASS

**Claim:** Targeted originalerrataPDF888 supplies no printed219Fortune correction.

I visually inspected the complete errata listing on original PDF888. Its sequence has no printed219 entry and no correction to this Fortune coordinate. This is a targeted errata-page absence claim, not a claim that no correction exists anywhere in any edition.

**Evidence:** Original PDF888, supplied image b02i-errata-p888.png.

### CL045 - PASS

**Claim:** VenusSun separation6:21 versus sixdegreesprose; SunSaturn119:31 leaves29minutes fromtrine, with perfect/orb interpretationqualified; MoonMars28minutes.

Independent differences are Venus-Sun381 arcminutes =6:21, Sun-Saturn7171 =119:31 with 29 arcminutes residual from120 degrees, and Moon-Mars28 arcminutes. The original prose says six degrees and perfect trine. The report preserves rather than resolves the meaning of perfect and does not infer contact times.

**Evidence:** Original PDF253-255; ARITHMETIC_CHECKS.json; MECHANICAL_EVIDENCE.json /independent_arithmetic.

### CL046 - PASS

**Claim:** Mercury is2:48beforeH8 and withingeometricH7; Venus50minutesafterH7; fifthfrom7is11.

Mercury Taurus3:38 is 168 arcminutes before H8 Taurus6:26 and lies inside the H7 Aries13:45 to H8 arc. Venus Aries14:35 is 50 arcminutes after H7. Inclusive fifth-from-seventh counting gives radical house11, matching the seller-daughter statement.

**Evidence:** Original PDF253-255; MECHANICAL_EVIDENCE.json /independent_arithmetic.

### CL047 - PASS

**Claim:** Sameyear/calendardeltas:March31→April25=25days;April25→May17=22days;total47days=6weeks5days; nohistoricalephemeriscalendarsynchronization claimed.

Under the stated same-year/same-calendar assumption the intervals are25,22,47 days;47 is6 weeks5 days. Only bounded March-May calendar subtraction is required. Neither the report nor the helper claims Julian/Gregorian synchronization or ephemeris contact reconstruction.

**Evidence:** Original PDF253 and PDF255 dates; lilly_fourth_house_arithmetic.py calendar_intervals; MECHANICAL_EVIDENCE.json /independent_arithmetic.

### CL048 - PASS

**Claim:** Earlier5degreecuspvirtuerule offers plausibleH8interpretation ofMercury, but currentchapterdoesnotstateexplanation; notsettledauthorerror.

The retained R033 record gives a five-degree cusp-virtue convention, and Mercury is geometrically2:48 before cusp8. This supports a possible interpretive eighth-house treatment. The complete local worked narrative never explicitly supplies that explanation; the report correctly leaves it plausible rather than settled. Earlier original PDF67 was not reopened.

**Evidence:** Original PDF253-256; Retained R033 in RETAINED_SOURCE_EXCERPTS.json; CROSS_SOURCE_COMPARISONS.json CMP11.

### CL049 - PASS

**Claim:** Sun seller assignmentviaH7placement thenlord7wording coexists withAriesH7cusp; tensionpreservedwithoutchangingchart.

PDF254 first assigns the Sun by its local seventh-house placement and subsequently calls it lord of the seventh. The chart actually has Aries on cusp7. Preserving both the assignment and wording without changing the diagram is accurate; the report does not resolve the terminology tension.

**Evidence:** Original PDF253-254; RULES.json R1131-R1132; UNRESOLVED.json B02i-C-U04.

### CL050 - PASS

**Claim:** Newhelper implements onlyexplicitgoodsframes,propertycontexts,verbaldirections,8slottally/rainlist/ordinaldepth; arithmeticusesunchangedB02fgeometry and completeinputs.

The listed finite lookup, context, direction, rain and ordinal-depth functions exist, and the arithmetic imports the retained B02f integer geometry whose current hash matches the recorded hash. Required exact inputs are rejected when incomplete. This exact ledger claim does not assert unconditional shared-body visibility. The extra assertion in report section8 is another occurrence of the CL014 defect; it does not invalidate this narrower ledger claim.

**Evidence:** AUDIT_REPORT.md section8 first paragraph; lilly_fourth_house_reference.py; lilly_fourth_house_arithmetic.py; MECHANICAL_EVIDENCE.json.

### CL051 - PASS

**Claim:** Actual distinct focused tests111=29new+24retainedB02h+31retainedB02f+27methodology; subtests/rerunsnotextra.

All four saved log hashes match the summary and record successful runs of29,24,31,27 cases, totaling111, with82 retained. The new code has9+12+8 test methods. The methodology source has13 test functions, including one15-case pytest parametrization, yielding27 distinct pytest cases; these are not27 independent test functions. This is consistent with the report wording tests and its refusal to add unittest subtests or reruns. No suite was rerun by this checker.

**Evidence:** TEST_B02i.txt; TEST_retained_B02h.txt; TEST_retained_B02f.txt; TEST_retained_methodology.txt; TEST_RUN_SUMMARY.json; Test source AST/decorators.

### CL052 - UNRESOLVED

**Claim:** Methodology firstattempt lackedpytestondefaultpath; existingdependencydirectory resolved it; environmentattemptpreserved; nonewpackage ormodel fitted.

The preserved failed attempt explicitly reports no module named pytest, and the successful run records use of the named dependency directory. The runner supplies that path through PYTHONPATH and contains no install or model-fit operation. These prove the recorded environment route. They do not independently prove the whole-turn negative assertion that no package was newly installed, or the historical origin of that dependency directory; those broader provenance assertions remain unresolved within this gate.

**Evidence:** TEST_methodology_environment_attempt.txt; TEST_retained_methodology.txt; run_verification.py; Source-only helper code.

| Component | Disposition | Reason |
|---|---|---|
| Failed pytest default-path attempt | PASS | Preserved log states No module named pytest. |
| Successful existing-path route | PASS | Success log names dependency directory and runner sets PYTHONPATH. |
| No whole-turn new package installation | UNRESOLVED | The logs/runner are not a complete installation-history receipt. |
| No fitted prediction model in the inspected helpers | PASS | Finite lookups and arithmetic; no fitting path. |

### CL053 - PASS

**Claim:** Tests cover source-data/codeboundaries, notpredictiveaccuracy, historicalephemerides,eventcorroboration orcompleteengine.

The actual new tests check omissions, geometry, endpoint separation, frozen source-data identities, inventory/issue links and reference bookkeeping. The code imports no historical ephemeris and performs no outcome corroboration or predictive evaluation. Test success cannot establish semantic completeness, historical event truth or astrological predictive accuracy; the report accurately limits it.

**Evidence:** All three B02i test source files; lilly_fourth_house_reference.py; lilly_fourth_house_arithmetic.py; TEST_RUN_SUMMARY.json.

### CL054 - UNRESOLVED

**Claim:** Twelve retainedLillycomparisons with29fullretainedrecords are included; not12independent-source confirmations; Ptolemy1066retainedwithoutnewreading.

The inventory portions pass: there are12 comparisons and29 full retained records, every copied record equals its referenced current earlier-source record, and all are Lilly. The Ptolemy index retains1066 records and the documented B02i comparison work does not use Ptolemy. A whole-history claim that Ptolemy artifacts were unchanged or never opened cannot be independently certified without the excluded preservation/history evidence. This unresolved remainder overlaps CL055 and does not undermine the29-copy check.

**Evidence:** CROSS_SOURCE_COMPARISONS.json; RETAINED_SOURCE_EXCERPTS.json; PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json; MECHANICAL_EVIDENCE.json /retained_copy_equality and /retained_input_hashes.

| Component | Disposition | Reason |
|---|---|---|
| Twelve Lilly comparisons | PASS | Count and source identity checked. |
| Twenty-nine complete retained copies | PASS | All29 structural comparisons against referenced source objects passed. |
| Not twelve independent-source confirmations | PASS | All comparisons use the same author/source. |
| Ptolemy current count1066 | PASS | Retained index reports1066. |
| All Ptolemy artifacts unchanged and no new reading occurred | UNRESOLVED | Before/after and access-history proof not admitted. |

### CL055 - UNRESOLVED

**Claim:** Earlierbatches,datedstates,personalinputs,models andpredictionfreezes arepreserved; remainingLilly/authors/formalization/predictiveevaluationremainopen.

The remaining Lilly source boundary is directly established by original PDF256 and the current index. Broader author coverage, formalization and predictive evaluation are not closed by this source audit. Six referenced retained Lilly source files still match their recorded hashes. The claimed preservation of all earlier batches, dated states, personal inputs, fitted models and prediction freezes requires a separate before/after preservation comparator. I did not inspect participant data, model/prediction files or excluded Git/repair history, so that broad preservation claim is not independently resolved here.

**Evidence:** Original PDF256; LILLY_SOURCE_EXTRACTION_INDEX_V1.json; MECHANICAL_EVIDENCE.json /retained_input_hashes; Excluded preservation evidence explicitly named in task boundary.

| Component | Disposition | Reason |
|---|---|---|
| Current source frontier and remaining work open | PASS | Original boundary and current index agree. |
| Six retained Lilly source-file hashes preserved | PASS | Matches current files to retained-input receipt. |
| All batches, dated states, personal inputs, models and prediction freezes preserved | UNRESOLVED | Complete historical comparator and protected-file coverage excluded from this independent pass. |

## Checkable claims missing from the submitted ledger

### ADD001 - FAIL

**Claim:** The words in quotation marks in the section2 own-house sentence are exact source wording.

The report quotes "own house, viz. the fourth". The original PDF240 reads "in his owne house, viz. in the fourth". Beyond modern spelling, the report silently removes the second in inside a continuous quotation. The underlying mundane-house interpretation is correct. Remove the quotation marks and keep it as a paraphrase, or use the contiguous original wording. This is a quotation-fidelity repair, not a doctrinal correction.

**Evidence:** AUDIT_REPORT.md section2 own-house sentence; Original PDF240 / printed206.

### ADD002 - PASS

**Claim:** The later rival does not itself contradict the source statement that there was no other purchaser at the original question moment.

The margin on PDF254 expressly places the rival after beginning and before conclusion. This temporal distinction makes the report limited inference valid; it does not independently prove that no rival existed earlier.

**Evidence:** Original PDF254 body and starred margin; AUDIT_REPORT.md section6 paragraph after stage table.

### ADD003 - UNRESOLVED

**Claim:** Publication and owner-copy verification are documented separately.

A separate draft-publication receipt exists. It describes a draft remote checkpoint and explicitly says the canonical branch was not changed. It does not establish owner-copy verification, and no owner-copy receipt was in the inspected evidence. The report must not be read as my verification of final publication or delivery. This is outside the source gate, not a recommendation to inspect more source pages.

**Evidence:** AUDIT_REPORT.md final sentence; DRAFT_PUBLICATION_RECEIPT.json.

### ADD004 - UNRESOLVED

**Claim:** The producer reconciled the readers records against its own reading after their source-first notes, and the original notes/raw candidates remain in the packet.

The source-data test log supports recorded candidate-copy and note-hash checks. The task intentionally barred the producer reconciliation and independent_review directory, so the full sequencing/reconciliation claim and current raw-packet retention were not independently re-inspected. Source/candidate equality tests alone do not prove those historical acts.

**Evidence:** AUDIT_REPORT.md How the source was checked; test_lilly_fourth_house_audit.py; TEST_B02i.txt.

### ADD005 - PASS

**Claim:** A separate final checker assesses this exact report and claim ledger.

This independent diagnostic pass checks the exact named hashes, all55 ledger items, the complete current source span and added checkable claims. This is fresh-context independence with the disclosed incidental metadata exposure, not a different-model-family or separate-organization claim.

**Evidence:** DIAGNOSIS_FIRST.json; FREEZE_RECEIPT.json.

## Information exposure and independence limits

Fresh evaluator task with the exact artifact identities, allowed evidence, admitted source span and governance. No role in producing this report or ledger.

Live UDA root AGENTS.md and docs/INDEX.md fetched from u-dont-existDOTcom/universal-dev-architecture with matching supplied blobs; project root AGENTS.md, task-relevant lesson-index entries, independent-evaluation-separation and source-interpretation-provenance read. PDF skill read and applied.

Original SHA-identified PDF; all original rendered pages236-256 inspected, with fifth-house text on256 boundary-only; PDF888 complete errata inspected. Existing p236-p256 text aids were used alongside images. Three evaluator-generated rotated crops of original page253 resolved small chart labels.

Exact report and ledger; source inventory/issue/coverage/case/coordinate/calculation/reference files; allowed retained comparisons and29 copied source records, including selected retained prose; six retained-file hashes; live local index snapshots; helpers, test source and saved logs; reading/text-check/draft-publication receipts.

**Not opened:** independent_review/ contents; ROOT_SOURCE_CHECKS.md; PRODUCER_RECONCILIATION.json; raw source-first notes; raw candidate files; prior independent review verdicts; sibling-agent summaries; Git log, commit diffs or repair-history traversal; participant data; personal input files; fitted model files; prediction freeze files.

**Embedded process annotations encountered in otherwise permitted evidence:**

- After my own original PDF237 check, TEXT_IMAGE_CHECKS.json revealed a producer note that a prior recollection of a chart there had been withdrawn.
- Allowed RULES.json qualifications contain narrow process annotations: R1045 describes source-first glyph confirmation; R1096 says a prior raw wording was narrowed and normalization restored the printed assertion. These were encountered only after my direct original-page checks of242 and250, and were not used as evidence of source correctness.
- WORKED_NUMERIC_TABLES.json includes a rejected small-rendering Mars reading in its transcription metadata; the actual current glyph was independently checked. The allowed draft-publication receipt contains commit identities and a local alignment description; none was traversed or treated as source-review authority.

This is a fresh diagnostic context and independent current-source/arithmetic check. It is not a claim of absolutely zero producer metadata exposure: the narrow embedded annotations above were disclosed. No raw earlier diagnosis or producer reconciliation was consumed. Source conclusions rest on the original images; the order of the specific embedded annotations is disclosed above. The report, ledger and chart table are the objects of evaluation, so this is not a claim to a blind chart transcription.

## Strongest remaining weakness

The report mixes strong directly checked source/calculation statements with some process and preservation assertions that the permitted packet only declares. Its main concrete wording defect is unconditional shared-body visibility despite optional identities. The report should keep each evidential basis explicit.

## Areas not evaluated

- Original prior Lilly pages outside236-256 and888; retained earlier records remain retained transcriptions, not new collations.
- Every nested field of all148 structured source records; the gate checks every report/ledger claim, inventory coverage and selected exact condition/attribution fields supporting those claims.
- Independent transaction, loan, bodily-mark or autobiographical corroboration.
- Historical ephemeris, calendar conversion, station/contact times or predictive accuracy.
- All-repository preservation against a historical base, personal data or model/prediction state.
- Final remote publication, canonical branch state or actual owner file delivery.

## Verification budget and freeze

One complete pass over 21 source-page images and the single errata page; three original-image chart crops for legibility. No test suite reruns. All four log hashes matched; the 111 total is supported by the logs, with methodology pytest parametrization distinguished from function count. Independent arithmetic and one bounded optional-body-ID reproduction are recorded in MECHANICAL_EVIDENCE.json. All 29 retained full-record copies match their current referenced source objects; the six recorded retained-input file hashes also match.

The final JSON preserves every submitted claim verbatim with its disposition, reasons and evidence. FREEZE_RECEIPT.json binds the diagnostic artifact hashes, target hashes, source identity, inspected evidence and information boundary. This diagnosis will not be edited during reconciliation; any focused repair check belongs in a separately identified addendum.
