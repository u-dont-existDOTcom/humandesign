# Lilly’s fifth-house questions: children, pregnancy, parent–child relations and messengers

## Result and exact scope

The source extraction of **Lilly, Book II, Chapters XXXIX–XLIII is complete**, including the fifth-house heading and every intervening unnumbered passage. The admitted span begins **below the horizontal divider on PDF256 / printed222** and ends at the bottom of **PDF276 / printed242**. The preceding fourth-house paragraph remains in the earlier batch. The sixth-house heading and Chapter XLIV on PDF277 / printed243 were inspected only to establish the next boundary; they have not been extracted in this batch. [Source: original PDF256–277; `SECTION_COVERAGE.json`.]

This is a historical source audit. It reconstructs Lilly’s statements, qualifications, worked examples and arithmetic. **Predictive accuracy remains unevaluated.** No modern fertility, pregnancy, health or child-sex assessment follows from these records. The reference helpers do not make such assessments. [Evidence: `RULES.json`, `HISTORICAL_CASES.json`, `lilly_fifth_house_reference.py`.]

| Measure | Verified inventory |
|---|---:|
| New source records | 201, R1157–R1357 |
| General, methodological, qualifying or illustrative records | 166 |
| Records belonging to the two worked enquiries | 35 |
| Cumulative Lilly records | 1,357 |
| Retained Ptolemy records | 1,066 |
| Combined source records | 2,423 |
| Typed source, implementation, variant and evidence-limit entries | 64 |
| Editorial coverage units | 27 |
| Dated enquiries / printed charts | 2 / 2 |
| Transcribed chart-coordinate entries | 45 |
| Printed child-sex testimony rows | 12 |
| Unique focused tests in the final source suite | 36 |

These are inventory counts, not counts of independent predictions. A limit-register entry can group related questions; further inline qualifications remain attached to individual records. The earlier 32-test implementation check is a subset of the final 36-test suite. Repeating the suite in the extracted delivery archive does not add new tests to the total. [Evidence: `COUNTS.json`, `UNRESOLVED.json`, `TEST_RUN_SUMMARY.json`, `IMPLEMENTATION_RECONCILIATION.json`; archive execution has its separate usability receipt.]

| Chapter | New records | Printed pages | Material covered |
|---|---:|---|---|
| XXXIX | 76 | 222–229 | Lifetime prospects, future and current conception, timing, a specified partner, survival, sex and twins |
| XL | 58 | 229–235 | Further conception rules, multiple births, gestational stage, delivery, day/night, maternal and infant outcomes, parent–child relations |
| XLI | 28 | 235–238 | Ambassadors, money messengers, foot-posts, reception, return and news |
| XLII | 17 | 238–240 | The 1635 negative example, bodily marks, nativity comparison and first-question resemblance |
| XLIII | 22 | 240–242 | The 1645 child-sex table, delivery arithmetic and reported birth |

The record granularity follows source claims and qualifications. The 27 coverage units are an editorial audit aid, not a claim that Lilly printed 27 numbered chapters or 27 distinct headings. [Evidence: `RULES.json`, `SECTION_COVERAGE.json`.]

## 1. The question and its known inputs govern the rule

The opening question can be asked long before marriage, or by an older unmarried person, about ever having children. A neighbouring passage addresses a married woman long without children. Other passages concern a specified partner, suspicion of an existing pregnancy, or a man asking without the woman’s knowledge. These contexts remain attached to their rules. They are not interchangeable input descriptions. [XXXIX, printed222–228 / PDF256–262; records A001, A009, A031, A043, A066. Temporary-to-canonical mapping is supplied in `RECORD_ID_MAP.json`.]

Lilly also separates conception from what follows it. In several adverse branches, stronger testimony or prior assurance of conception changes the interpretation from absence of conception to danger of loss. The record therefore preserves both the astronomical condition and what was already believed or known when the question was asked. [XXXIX, printed226,228 / PDF260,262; XL, printed232–233 / PDF266–267; A039–A040, A069, B039–B042.]

The multiple-birth discussion expressly requires inquiry into whether bearing more than one child at a birth is usual in the woman’s family. That family history is prior information. The text does not provide a numerical weight for it. In the worked 1645 enquiry, the question already presupposes being with child; the reported male birth cannot also count as a newly discovered pregnancy. [XL, printed230 / PDF264, B013; XLIII, printed240–242 / PDF274–276, C018–C039.]

For a later evaluation, lifetime childbearing, present conception, future conception, child survival, fetal movement, number of children, sex, maternal condition and delivery date would need separately defined endpoints. The source itself changes among these targets. Combining them into a single success label would conceal what each passage actually claims. This is the audit’s evaluation implication, not a scoring system supplied by Lilly. [Source distinctions: `RULES.json`; case decomposition: `HISTORICAL_CASES.json`.]

## 2. Qualifications that change the force of a rule

Before one timing recipe, Lilly first asks whether natural causes allow children. Elsewhere he directs the astrologer to consider age and natural or hereditary infirmity and to conclude **seldom** without two testimonies. “Seldom” remains a qualification; it is not rewritten as an absolute prohibition. Nor does the passage define statistically independent testimonies or a calibrated confidence scale. [XXXIX, printed223–225 / PDF257–259, A015, A029–A030.]

The treatment of affliction depends on the actual house roles. A planet ruling the sixth, eighth or twelfth can afflict the first-house ruler, fifth-house ruler or Moon through square or opposition, whatever that planet’s usual benefic or malefic classification. In another passage, accidental dignity supplies hope while essential fortification is required for the stated assurance in the lunar-reception route. These conditions remain part of the records. [XXXIX, printed226–227 / PDF260–261, A046–A051.]

One reciprocal dignity recipe even gives unequal lists: house, triplicity or exaltation on one side, with term also named on the receiver’s side. The extraction preserves that asymmetry instead of adding term or face everywhere. The named roles can also coincide in a single physical planet—for example, Jupiter and a triplicity ruler. Role overlap is an input/dependency issue, not evidence of two independent observations. [XXXIX, printed224,227 / PDF258,261, A018, A053; `UNRESOLVED.json` U-A18.]

Lilly uses “cadent from its own house” in a sign-relative explanation. Mars in Aries is angular in that sense regardless of mundane house, Mars in Taurus is succeeding, and Mars in Gemini is cadent. The paragraph says a planet is angular in any of its own houses. This must remain distinct from ordinary house placement. The local illustration does not enumerate all choices among multiple domiciles and exaltation references. [XXXIX, printed227 / PDF261, A055–A057.]

Anonymous alternatives remain attributed. The angular-receiver exception is introduced as something some say; another Jupiter testimony is attributed to others. A later run begins with “Some say” and has no sharply marked endpoint before Lilly resumes describing his own practice. These are preserved as source variants and attribution questions, not harmonized into one universal rule. [XXXIX, printed223,225 / PDF257,259; XL, printed232–233 / PDF266–267; A008, A027, B034–B044.]

## 3. Timing has several separate methods

### The unusual house-to-year table

For the future-child timing question, after the natural-possibility qualification, the printed map is:

| House occupied by the fifth-house ruler | Source year |
|---|---|
| First / Ascendant | First year |
| Second | Second year |
| Tenth | Third year |
| Seventh | Fourth year |
| Fourth | Fifth year |

“Second house” was checked in the original image. The other seven houses have no entry in this local map. The start point for counting those years is not specified with modern precision. Movable, double-bodied and fixed signs modify speed in the stated ways; a swift, direct significator hastens accomplishment whatever sign it occupies. No numerical adjustment is supplied. [XXXIX, printed223–224 / PDF257–258, A015–A017.]

### Gestational stage is a different inquiry

The source selects among Moon, the fifth-house ruler and the hour ruler by the nearest separation from another planet, then uses the separating aspect:

| Aspect | Source wording of the stage or duration |
|---|---|
| Trine | Fifth or third month of conception |
| Sextile | Second or sixth month of conception |
| Square | Fourth month of conception |
| Opposition | Has been conceived seven months |
| Conjunction | Has been conceived one month |

The two alternatives for trine and sextile are retained. The source does not say which one to select here. The change from an ordinal month to elapsed months is also preserved. Neither a preferred alternative nor a retrospective best-fitting interpretation is selected by the helper. [XL, printed231 / PDF265, B019–B020; `lilly_fifth_house_reference.py`.]

### Delivery methods must keep their own units

The Part of Children is taken **from Mars to Jupiter and projected from the Ascendant, both by day and by night**. In cyclic longitude notation the reference expression is `(Ascendant + Jupiter − Mars) mod 360°`. This is distinct from the retained Part of Fortune formula, `(Ascendant + Moon − Sun) mod 360°`. The former’s ordered planets and unchanged day/night construction are explicit here; the cyclic notation expresses the projection convention. [XL, printed232 / PDF266, B028; retained XXIII, printed143–144 / PDF177–178, R625.]

For directions of the Part of Children, the passage refers to ascensions, the fifth-house degree, Jupiter and its aspects, and gives one day per degree. It supplies no complete local algorithm for the direction, path or orbs. A neighbouring method gives one month per sign of the fifth ruler’s distance from the fifth cusp. The conjunction method begins with Mars and Sun. Majority and near concurrence are invoked to help judge among timing testimonies, but no complete numerical arbitration rule appears in these paragraphs. [XL, printed231–232 / PDF265–266, B021–B028.]

The 1645 example instead assigns one week per degree to two printed gaps. The reference code therefore requires both a named timing method and the corresponding angular measure; it rejects exchanging a static longitude gap with an ascensional direction arc. This prevents an implementation from silently applying a single degree-to-time rule across the chapter. It does not supply a missing historical direction algorithm. [XLIII, printed242 / PDF276; `lilly_fifth_house_reference.py`, `TEST_B02j.txt`.]

## 4. The 1635 example gives a judgment without a lifetime endpoint

The first figure is dated **11 June 1635, 2:30 P.M.**, with Jupiter named for the day and hour. Its question is whether the querent should ever have children. Lilly treats Virgo rising and the Moon’s Virgo sign as barren, Capricorn on the fifth as indifferent in this question, and Sagittarius/Gemini as rather barren than fruitful for Saturn and Mercury. Saturn rules both the fifth and sixth in this figure. [XLII, printed238–239 / PDF272–273, C001–C003.]

He judges both past nonconception and future lifelong nonconception. But he also describes counterfactual conditions that would have made him less categorical: Jupiter strengthening the fifth cusp or making the relevant contacts, specified receptions, or reception-qualified collection of light. These alternatives did not occur according to his account. The negative judgment is not accompanied by an independently verified reproductive history or a lifetime follow-up in the admitted pages. [XLII, printed239 / PDF273, C004–C007; U-C01.]

The account includes symptoms and **five bodily-mark reports**: near the navel, right ankle, near the right knee on the inner thigh, an unnamed member associated with the Moon in Virgo, and a scar or mole on the outside of the right arm. They are narrated as the querent’s confirmation within this one retrospective encounter. The first navel item is not given a separate explicit astrological cause in that sentence. These reports remain dependent observations within one case, not five additional prediction cases. [XLII, printed239 / PDF273, C008–C013.]

After the example, Lilly advises casting the nativity when a question is so categorically negative. He states that natal barrenness takes precedence over a promising horary figure. He then reports that a person’s first question usually has the same rising triplicity as the nativity and often the same sign and degree; Gemini with Libra or Aquarius illustrates the triplicity claim. No counted series accompanies that experience claim, and no nativity for the 1635 querent is supplied in this passage. [XLII, printed240 / PDF274, C014–C017.]

## 5. The 1645 child-sex table has an unresolved hour-ruler conflict

The second enquiry is dated **7 April 1645, 2:15 P.M.** Its figure puts the Moon beside the paired day/hour labels. The subsequent table instead counts **Jupiter as lord of the hour**. Both witnesses remain in the data. [XLIII, printed240–241 / PDF274–275, C018–C032; U-C05; `evidence/chart2-center.png`.]

The printed table contains these twelve rows:

| Direction | Testimony |
|---|---|
| Female | Virgo on the Ascendant |
| Female | Capricorn on the fifth |
| Female | Moon in a feminine sign |
| Female | Mercury with Venus, a feminine planet |
| Male | Mercury in a masculine sign |
| Male | Saturn, fifth ruler, a masculine planet |
| Male | Saturn in a masculine sign |
| Male | Moon in a masculine house |
| Male | Saturn in a masculine house |
| Male | Jupiter, hour ruler, masculine |
| Male | Jupiter in a masculine sign |
| Male | Mercury applying to square Mars, a masculine planet |

Lilly counts **eight male and four female** testimonies, judges male, and reports that it proved so. Mercury, Saturn, Moon and Jupiter recur across rows. The 8:4 count is a literal plurality in this table; it is not an 8-in-12 empirical success rate or a calibrated probability. [XLIII, printed241 / PDF275, C019–C032; `WORKED_NUMERIC_TABLES.json`.]

A conditional sensitivity check shows why the hour discrepancy matters. **If** both Jupiter rows are treated as an hour-ruler chain, **and if** the figure’s Moon is taken as the intended hour ruler, replacing the masculine Jupiter and Gemini entries with feminine Moon and Capricorn entries yields **6:6**. That calculation is the audit’s counterfactual. It is not a correction proved by the source, not an alternative judgment printed by Lilly, and not a basis for choosing whichever tally matches the reported birth. [Calculation: `ARITHMETIC_CHECKS.json`; assumptions: U-C05.]

The masculine-house rows require another distinction. From the printed coordinates, Moon and Saturn lie in geometric sectors four and eight, respectively. They stand **4°11′ before the fifth cusp** and **0°43′ before the ninth cusp**. Lilly’s earlier five-degree cusp-virtue instruction could be relevant. This remains a possible interpretive qualification: the worked paragraph does not explicitly cite that rule as its explanation. Geometry, source testimony and the inference are separately retained. [Figure: printed240 / PDF274; earlier rule: printed33 / PDF67, R033; U-C10; `CROSS_SOURCE_COMPARISONS.json`.]

## 6. Delivery arithmetic is reproducible; the outcome claim has limits

Lilly considers the movable signs but gives substantial weight to slow Saturn. His two tables supply:

| Calculation | Printed inputs | Remaining gap |
|---|---|---|
| Moon to Saturn’s square | Moon Capricorn9°50′; Saturn Aries24°37′ | 14°47′ |
| Mercury to Saturn’s conjunction | Mercury Aries11°00′; Saturn Aries24°37′ | 13°37′ |
| Difference between gaps | 14°47′ minus13°37′ | 1°10′ |

The static arithmetic reproduces all three values. The Moon’s square requires the appropriate square ray; it is not obtained by treating Capricorn and Aries as the same sign. The figure omits Mercury’s minutes, while the later table explicitly supplies 00. The figure’s missing field remains `null`; the calculation uses the separately identified table witness. [XLIII, printed240,242 / PDF274,276; C034–C036; U-C08; `ARITHMETIC_CHECKS.json`.]

Lilly gives one week per degree and judges delivery **about fourteen weeks** after the question. He reports delivery on **11 July following**. From 7 April to 11 July in the same calendar is **95 days, or 13 weeks 4 days**. Fourteen weeks is 98 days; the reported date is therefore three days earlier than that point. This date subtraction does not convert the historical date labels into modern Gregorian dates or UTC. [XLIII, printed242 / PDF276; C036–C037; `ARITHMETIC_CHECKS.json`.]

The source gives no formal rule here for averaging, rounding or selecting between the two angular estimates, and no advance tolerance defining “about.” The known date therefore cannot supply a retroactive fitting rule. The exact gap fractions are retained for reproducibility, not optimized to improve the narrative’s apparent performance. [Source: printed242 / PDF276; U-C12.]

Lilly adds Mars, Mercury, Sun and Moon transit observations after stating the birth date. These remain retrospective support in the same account; they are not separately frozen advance predictions or four new outcome cases. An independent historical ephemeris reconstruction has not been performed. The admitted pages do not give a modern timezone, an exact birth time or a complete set of modern astronomical inputs. [XLIII, printed240–242 / PDF274–276; C038–C039; U-C11, U-C13.]

## 7. Printed coordinates are preserved even when inconsistent

The 1635 figure’s third cusp reads **Libra19°20′**, while its ninth reads **Aries19°10′**. Their opposition has a ten-minute mismatch. Neither cusp has been repaired by assuming the other must be right. Some planetary signs are inferred from their diagram placement or narrative context and are labelled accordingly. [XLII, printed238 / PDF272; `WORKED_NUMERIC_TABLES.json`, U-C07.]

Using the declared figure readings, the retained Fortune formula gives **Sagittarius3°08′** for the first chart, matching its printed Fortune. The Part-of-Children formula gives **Libra20°16′**, matching the recorded part under the declared Libra placement inference. These matches are conditional arithmetic consistency checks; they do not independently prove those inferred signs. [Figure: printed238 / PDF272; formula: printed232 / PDF266 and retained printed143–144 / PDF177–178; `ARITHMETIC_CHECKS.json`.]

For the 1645 figure, the enlarged, levelled Sun detail reads **Aries27°52′**. With Ascendant Virgo8°50′ and Moon Capricorn9°50′, Fortune calculates to **Taurus20°48′**, matching the figure. The later birth-day account gives Sun **Cancer27°48′** and calls this a perfect square to the question Sun. The two source values leave a **4′ mismatch**. Substituting 27°48′ into the question chart would change calculated Fortune to Taurus20°52′, four minutes from its printed value. Both source readings and the conditional comparisons remain visible. [XLIII, printed240,242 / PDF274,276; U-C06; `evidence/chart2-sun-level.png`, `ARITHMETIC_CHECKS.json`, `TEST_B02j.txt`.]

The targeted original-edition errata check does not supply a correction for the worked pages 238, 240, 241 or 242. It does supply the wording “consideration” for printed 224 line 10. The entry initially suspected to concern printed 229 actually refers to 209. The printed233 “practice” correction is lexical; other entries involving “and if I” and printed235 “house” do not demonstrate unique substantive edits. No timing value or judgment predicate was changed through those uncertain entries. [Original PDF888; `ERRATA_CHECKS.json`, source-reader supplements.]

## 8. Parent–child reconciliation and messenger outcomes need their own evidence treatment

For parent–child relations, Lilly prefers a nativity but offers horary because, in his stated setting, few can judge a nativity. His rules can attribute fault to the child or the parent. He explicitly asks for fair, truthful dealing whichever side bears fault, and reports using the approach to reconcile parents and children. That reconciliation is an intervention described by the author. It cannot automatically be treated as an untouched future outcome predicted from a chart. [XL, printed234–235 / PDF268–269, B049–B058.]

The messenger material changes role assignments with context:

| Context | Source assignments or distinction |
|---|---|
| Ambassador | Fifth ruler; Moon also admitted |
| Money messenger | First ruler = sender; seventh ruler = recipient; Moon = message; fifth ruler = messenger/business |
| Foot-posts / lackeys arrival paragraph | Explicitly uses first ruler or Moon in the seventh or applying to its ruler |
| Receiving news | Distinguished from the messenger’s physical return |

The foot-post use of the first ruler is preserved even though it differs from the preceding fifth-ruler messenger assignment. One money rule also says the messenger brings money after separation from the second ruler whether that ruler is a Fortune or an Infortune. Reception with square/opposition can mean being welcomed while the recipient offers an excuse or defence concerning the request. Welcome, completion of an errand, money obtained, safe travel, news and physical return are different possible outcomes. [XLI, printed235–238 / PDF269–272, B059–B086.]

For return timing, Lilly directs consideration of journey length and sign quality when converting degrees to days, weeks or months; this paragraph gives no universal fixed/common/movable-to-unit table. His news claim allows the indicated day **or near it**. These qualifications remain in the record rather than being sharpened into exact-date guarantees. [XLI, printed237–238 / PDF271–272, B081–B086.]

## 9. What the verification establishes

Every admitted original page image was read, with additional detail inspection for difficult chart entries and the targeted errata. Source-reader notes were frozen before their candidate rows were produced. The final diagnostic reader also read the complete admitted source block in a fresh context before receiving the frozen report and records. This is separation of model context and information state; it is not a claim of a different model family or an outside expert. The later diagnostic findings and their dispositions must remain separate artifacts. [Evidence: `READING_RECEIPT.json`, source-reader freezes, independent-review receipts.]

The final source/reference suite contains 36 actual tests and passes with exit code 0. It checks ID continuity, source anchors and issue references, inventory, missing minutes, separate source witnesses, modular arithmetic, the local time models, dependency inputs, the conditional vote replay and the calendar restriction. The collaborative implementation review’s three reproduced interface problems are retained with the repairs. [Evidence: `TEST_B02j.txt`, `TEST_RUN_SUMMARY.json`, `implementation_review/`, `IMPLEMENTATION_RECONCILIATION.json`.]

Release acceptance requires separate archive, publication and delivery receipts. The archive must actually be extracted, matched against its manifest and used to run its bounded tests; published and delivered bytes must also match. These checks concern artifact integrity and usability. Earlier Lilly and Ptolemy material, participant inputs, fitted models and prediction freezes are outside this batch’s mutation scope. Exact preservation must be established by a repository comparison. None of these checks validates astrology. [Evidence: `PACKET_USABILITY.json`, publication/delivery receipts, `PRESERVATION_CHECKS.json`.]

## 10. Continuation

The next unextracted passage is **PDF277 / printed243**, starting at the top with **“Of the sixt House, and its Questions.”**, its topic list **“Sicknesse, Servants, small Cattle.”**, and **Chapter XLIV, “Judgment of Sicknesse by ASTROLOGY.”** Include the opening paragraph. The fifth-house block is complete; the wider multi-author, multipass audit remains open. [Boundary witness: original PDF277; `SECTION_COVERAGE.json`; cumulative extraction index.]

The records, coordinate table, source limitations, bounded reference code, tests, source-reading provenance and continuation handoff accompany this report. The original 894-page source PDF is identified by its hash and page anchors; it is not duplicated inside the delivery ZIP. Selected original-page witnesses are included for the worked figures, testimony table and arithmetic. The packet README explains how to inspect the records and run the standalone suite.

**Original source identity:** William Lilly, *Christian Astrology*, 1647, Wellcome witness `b30338724`; 894-page PDF, 141,842,963 bytes; SHA256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`.
