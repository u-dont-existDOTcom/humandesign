# Lilly’s sixth-house opening: sickness, duration, recovery and death testimonies

## Result and exact scope

The **opening sixth-house sickness block in Lilly’s Book II, Chapter XLIV is extracted**. It begins with the sixth-house heading, topic list, chapter title and opening on **PDF277 / printed243**. It ends with the paragraph concluding “shew death” on **PDF292 / printed258**, immediately before **“DARIOT Abridged.”** Every intervening numbered or unnumbered passage within that span is included. **Chapter XLIV continues beyond this batch and remains incomplete.** [Original PDF277–292; `SECTION_COVERAGE.json`.]

This is a historical source audit of Lilly’s statements, their conditions, their textual witnesses and the limited operations that can be reproduced from them. **Predictive accuracy remains unevaluated.** No patient is assessed, no treatment is selected and no survival probability is calculated. The records and code are reference material, with no promotion into the project’s prediction runtime. [Evidence: `RULES.json`, `COUNTS.json`, `lilly_sixth_opening_reference.py`.]

| Measure | Inventory |
|---|---:|
| New source records | 192, R1358–R1549 |
| Cumulative Lilly records | 1,549 |
| Retained Ptolemy records | 1,066 |
| Combined Lilly and retained Ptolemy records | 2,615 |
| General, methodological or illustrative records in this batch | 192 |
| Worked-narrative records / dated enquiries / horoscope figures | 0 / 0 / 0 |
| Editorial coverage units / admitted PDF pages | 11 / 16 |
| House, sign and planet catalogue rows | 12 + 12 + 7 = 31 |
| Typed limit-register entries | 37 |
| Retained limits or anomalies / source-resolved entries | 33 / 4 |
| Distinct focused tests in the final source suite | 33 |

[Evidence: `COUNTS.json`, `SECTION_COVERAGE.json`, `REFERENCE_TABLES.json`, `UNRESOLVED.json`, `TEST_RUN_SUMMARY.json`, `PTOLEMY_COUNT_RECEIPT.json`.]

The 192 records are an extraction inventory, not 192 independent predictions. One paragraph may supply several conditions, qualifications or alternatives; repeated astronomical carriers do not become independent evidence merely because they occupy separate records. The eleven coverage units are editorial aids, not eleven numbered chapters. Four retained callback records are included for reference without adding them again to the cumulative count. [Evidence: `RULES.json`, `SECTION_COVERAGE.json`, `RETAINED_SOURCE_EXCERPTS.json`.]

## 1. The selected time is part of the method

Lilly gives an ordered sequence for selecting the figure’s time:

| Priority | Source event | Qualification |
|---|---|---|
| First | The first time illness compelled bed or repose | Obtain the hour as nearly as possible |
| Second | The first carrying of the sick person’s urine to someone to enquire about the disease | Used if the first time cannot be obtained; the recipient need not be a physician |
| Third | The physician’s first speaking with the patient, first access to the patient, or first receipt of the urine | Used if the earlier evidence cannot be obtained; the three alternatives have no stated internal ranking |

[XLIV, printed243 / PDF277; R1359–R1361.]

The first slight sensation of illness is expressly excluded from the preferred onset time. Lilly asks for the point when the person was sufficiently oppressed to be forced to bed or rest. After selecting the time, he directs construction of the figure and exact rectification of the Moon’s position to that hour. The selected event therefore needs to remain part of the provenance of any later calculation. [XLIV, printed243 / PDF277; R1359, R1362.]

The time helper distinguishes **unavailable** from **unknown**. It does not silently fall through an earlier stage whose availability is unknown. Within the third stage it retains known alternatives; different supplied time tokens remain an unresolved choice. If another alternative’s availability is unknown, the selection status remains unknown while the known candidates remain visible. These are conservative implementation policies for unresolved evidence, not extra priority rules attributed to Lilly. [Implementation: `select_source_time`; focused time-selection tests.]

Before judging the bodily location, Lilly also requires observations of the ascendant and its occupants, the sixth house and its occupants, the Moon’s sign and house, and the planet affecting the Moon together with that planet’s house and lordship. The records preserve these as required observations. This passage supplies no weighted formula for combining them. [XLIV, printed243 / PDF277; R1363.]

## 2. The correspondence tables must retain their own meanings

The opening block gives three separate catalogues: **twelve houses**, **twelve signs**, and **seven planets**. Their historical disease and bodily correspondences are stored under separate lookup namespaces. A query for a house cannot silently fall back to a sign with a superficially similar association. The list lengths describe the printed catalogues, not evidence that the correspondences are medically valid. [XLIV, printed244–247 / PDF278–281; `REFERENCE_TABLES.json`.]

A fourth structure is relevant because Lilly explicitly refers back to the **planet-in-sign body table on printed page119 / PDF153**. In that retained table, Saturn in Cancer corresponds to **Reins, Belly, Secrets**. This is a different lookup from either the generic Cancer disease list or Saturn’s generic disease list. The current helper admits that one callback cell; it does not fill other cells from an assumed pattern. [XLIV, printed243–244 / PDF277–278; R1364–R1366; retained R523; `CROSS_SOURCE_COMPARISONS.json`.]

Lilly’s Cancer-rising, Saturn-in-Cancer illustration combines the first house’s association with the head and the members signified by Saturn in that sign. He offers alternative ailments and then says the judgment becomes more certain—using “infallible” language—if one of the specified corroborating significators or the sixth sign indicates the same member. The illustration is hypothetical; no dated patient, chart or independently observed endpoint accompanies it. [XLIV, printed244 / PDF278; R1365–R1366.]

A future evaluation would need to distinguish a bodily location inferred from the chart from a symptom already supplied by the questioner, and would need to define what counts as corroboration. That is an evaluation requirement inferred from the source’s use of inputs and overlapping correspondences. It is not a scoring method printed by Lilly. [Source basis: R1363–R1367; evidence classification in `RULES.json`.]

## 3. Mean lunar motion and the retrograde analogy differ

The duration discussion uses the Moon travelling in twenty-four hours **less than her mean motion** while in an aspect or conjunction with the ascendant’s ruler. The numerical mean is not printed in that local sentence. The audit explicitly links it to Lilly’s earlier statement on **printed80 / PDF114**, which gives **13°10′36″**. [XLIV, printed251–252 / PDF285–286; R1467; retained R192; `CROSS_SOURCE_COMPARISONS.json`.]

The earlier page separately calls travel of **less than 13°10′ in twenty-four hours** equivalent to a retrograde planet, while saying the Moon is always direct. The threshold for that analogy is **36 arcseconds lower** than the stated mean. Both comparisons are strict: equality does not satisfy “less than.” [Printed80 / PDF114; retained R195 and R221; `ARITHMETIC_CHECKS.json`.]

| Supplied daily motion | Below stated mean, 13°10′36″? | Below analogy threshold, 13°10′00″? |
|---|---|---|
| 13°09′59″ | Yes | Yes |
| 13°10′00″ | Yes | No |
| 13°10′18″ | Yes | No |
| 13°10′36″ | No | No |

These are controlled arithmetic examples, not reconstructed historical observations. The two threshold comparisons therefore cannot be merged into one boolean without changing at least some results. [Executed calculations: `ARITHMETIC_CHECKS.json`; focused lunar-motion tests.]

The helper returns only those two comparisons. It does not infer physical retrogradation, compute a horoscope, or evaluate the full aspect-qualified illness rule. Nor does it silently equate “below the mean” with the neighbouring phrase “decreases in light and motion”: those are separately stated source conditions. [Printed80 / PDF114 and printed251–252 / PDF285–286; R1467–R1469; `lilly_sixth_opening_reference.py`.]

## 4. Remaining arc does not by itself choose a duration

For an unfortunate planet in the sixth moving from one sign into another, Lilly says the disease will alter. If asked when, he directs counting the degrees remaining before the planet leaves the sign and judging that many **months, weeks or days according to the sign’s nature and quality**. The local passage supplies no complete choice among those units and no rule for rounding a partial degree. The initial alteration is not expressly assigned a favourable or unfavourable direction. [XLIV, printed249 / PDF283; R1437–R1438.]

The reference helper can calculate an exact remaining arc when all coordinate components are supplied. For example, **29°30′00″ leaves ½° in the sign**, while the time unit remains unknown. Omitted minutes or seconds remain missing. The helper also rejects a combined position of 30° or more, even when each fractional component separately lies below its own limit. This domain check is an implementation safeguard, not a data-entry rule attributed to the seventeenth-century text. [Executed example and rejected counterexamples: `ARITHMETIC_CHECKS.json`; `remaining_degrees_in_sign` and its focused tests.]

## 5. Conditions and exceptions change the source’s prognosis

The source distinguishes **present danger, increasing illness, duration, recovery, recovery after delay, relapse, and death**. Some passages describe recovery despite a long or grievous illness. Others express danger or probability rather than certainty. These distinctions remain in the individual records; a future evaluator would need separately defined endpoints instead of a single success label. [XLIV, printed249–258 / PDF283–292; `RULES.json`.]

The benevolent-planet clause on printed250 requires the planet to be **well fortified in the sixth and not the author of the disease**. That last condition is essential to matching the clause. The outcome wording in the image is “the Disease is not, or will be permanent.” The record preserves it without inserting another “not”; whether the first negative has shared scope or a word is absent remains unresolved. The helper checks the prerequisites only and does not resolve this outcome wording. [PDF284; R1444; U-ROOT01; `evidence/pdf284-permanence.png`.]

For the Moon decreasing in light and motion and coming to conjunction, square or opposition of Saturn, Lilly’s adverse statement is qualified **“for the most part”** and excepts a disease already **“in its decrease and leaving the Patient or Querent.”** The helper’s exception input represents that whole phrase. Knowing only that the disease is decreasing does not establish the full exception; an unresolved aggregate remains unknown. A satisfied prerequisite is not a certain prognosis. [Printed252 / PDF286; R1469; `evidence/pdf286-saturn-exception.png`; reference helper.]

Aspect names also need their context. With **Mars ruling the ascendant and placed in the sixth**, Lilly says there is no great danger when Mars is in sextile or trine to Venus, and extends that statement even to square or opposition. Conjunction is not named in this particular sentence. A universal rule that every square or opposition must add danger would misrepresent this passage. [Printed252 / PDF286; R1475.]

Reception can change the outcome without removing duration. One recovery testimony requires reception between the first and eighth rulers and neither being infortunated by malignant planets. A later death-probability passage allows possible escape through reception with the planet in the eighth, while retaining a very long and grievous disease. The exact reach of that later exception across every preceding alternative is not fully restated and remains a scope question. [Printed254,257 / PDF288,291; R1497, R1535.]

Lilly’s common-sign duration statement has an explicit **Pisces-on-the-sixth-cusp exception**. He says he has found that placement equivalent to a movable sign. The final words continue from PDF282 onto the first line of PDF283; that continuation is included in the record. This is Lilly’s generalized first-person experience claim, not a counted or independently checked series. [Printed248–249 / PDF282–283; R1429–R1430.]

A recovery condition on printed255 assigns freedom from misfortune to **the ascendant’s ruler**: after the Moon applies to that ruler by trine or sextile, the text says “and he be cleer of all misfortune,” followed by an alternative absence-of-impediment clause especially concerning the eighth or sixth lord. Both the subject and the printed “or” matter. The freedom condition is not reassigned to the Moon. [PDF289; R1505; `evidence/pdf289-ascendant-lord-pronoun.png`.]

Another passage, with the sixth ruler in the eighth and the eighth ruler in the sixth and a sextile or trine between them, says “you shall not doubt of the death of the Patient at that time,” then explains that Nature is not so overcome or weak that the sick cannot overcome the illness. The historical sense of “doubt” or a possible textual tension remains open. The extraction retains both the phrase and the survival-oriented explanation; it does not silently substitute “life,” “fear,” or “no death.” [Printed249 / PDF283; R1440; U-B01.]

## 6. Printed words, handwriting and errata are separate witnesses

The scan contains ink alterations as well as an authorial errata page. The packet keeps the visible original layer, the observed handwriting and the errata instruction distinct. A legible correction elsewhere in the book does not make an overwritten original phrase fully legible, and an unattributed handwritten alteration does not automatically become Lilly’s wording. [Original PDF288,290,291,888; source-layer fields in `RULES.json`; `TEXTUAL_CHECKS.json`.]

| Errata target | Instruction or reading | Treatment in this batch |
|---|---|---|
| Printed245, penultimate line | Read “scabbinesse” | The Cancer row on PDF279 already reads Scabbinesse; body and errata agree on that word |
| Printed254, lines18–19 | Read “placed” | Retain the placement wording with the separate errata witness |
| Printed256, line8 | Delete “all hopes of escape”; read “feare of danger” | Use the corrected reading in the reception-qualified little-hope clause; preserve the obscured original layer |
| Printed257, line23 | Read “eight” | Preserve the corrected eighth-lord reading in the antiscion clause and the altered original layer |

The errata target for Scabbinesse names the penultimate line; the nearby marginal mark is not treated as a newly supplied line number. The agreement does not establish an otherwise unobserved earlier printing error. [Original PDF279,288,290,291,888; `TEXTUAL_CHECKS.json`; `evidence/pdf888-admitted-errata.png`.]

On PDF280 the visible printed page label is **244**, although its position in the sequence corresponds to **246**. Each affected record retains the visible label and the expected sequence separately. A citation to PDF280 therefore remains unambiguous without rewriting the scan’s pagination. [Original PDF280; `SOURCE_IMAGE_MANIFEST.json`; `evidence/pdf280-visible-page-label.png`; source locators in `RULES.json`.]

Near the end of the admitted span, the combustion passage names **Saturn or Mercury**. The Mercury glyph was checked in an enlarged original image and is not normalized to Mars. The passage also combines eighth-house placement, Leo or Libra, aspects and the Pleiades in a way whose complete AND/OR grouping is not resolved. Its words are retained as source prose, without declaring one executable configuration. [Printed258 / PDF292; R1548; U-B16; `evidence/pdf292-combustion-clause.png`.]

## 7. Historical star labels are not modern exact coordinates

The admitted passages provide these historical labels:

| Source name or preserved spelling | Sign | Source degree wording |
|---|---|---|
| Antares | Sagittarius | Fourth degree |
| Lans/Lanx Australis | Scorpio | About the ninth |
| Palilicium | Gemini | Four |
| Caput Medusae | Taurus | Twenty |
| Pleiades | Taurus | Twenty-four |

The first four are examples in the discussion of a malevolent planet or violent fixed star near the ascending degree. The Pleiades occur in the later combustion passage. The spelling uncertainty in Lans/Lanx Australis remains visible. [Printed257–258 / PDF291–292; R1538, R1548; `REFERENCE_TABLES.json`.]

These labels supply no minutes or seconds, no modern-epoch conversion and no numerical definition of “near.” The wording also does not establish a unique ordinal-to-continuous-degree convention. Those fields remain missing. The helper retrieves the printed label and its uncertainty; it does not turn it into a present-day star position or manufacture an orb. [R1538, R1548; U-B14; `REFERENCE_TABLES.json`, `lilly_sixth_opening_reference.py`.]

## 8. What the evidence supports and what remains open

The block contains historical humoral, moral, sexual and supernatural attributions as well as planetary correspondences. Those statements remain attributed to the historical source. Reproducing them does not establish a modern diagnosis, a cause of illness, a treatment effect or a factual allegation about any person. General descriptions of medicines having worked and Lilly’s generalized claims of experience are not supplied as independently documented patient outcomes. [For examples, printed244–251 / PDF278–285; R1432–R1434, R1441 and surrounding records; `COUNTS.json`.]

The arguments of death invoke natal positions, profection and the five hylegical places. A recovery testimony invokes a later crisis. The records preserve those dependencies, but the local paragraphs do not complete the later nativity or crisis methods. The next “DARIOT Abridged” material is still outside this batch. Those dependencies cannot be treated as implemented merely because their names have been extracted. [Printed255–258 / PDF289–292; `CROSS_SOURCE_COMPARISONS.json`, `UNRESOLVED.json`.]

The unresolved register now contains **37 typed entries**. **33** retain wording, grammar, terminology, implementation, attribution, precision or evidence limits; **4** are separately marked as resolved callbacks or errata readings. These are not 37 alleged errors in Lilly. The original-layer legibility question can remain open even when the errata supplies a usable corrected reading. Further qualifications also remain attached directly to individual records. [Evidence: `UNRESOLVED.json`, `RULES.json`.]

The four resolved register entries concern the targeted printed119 table callback, agreement of the Cancer-row Scabbinesse with the errata, the declared mean-motion reference value, and the retained placement/antiscion errata layer. Resolution here is limited to that source question. It does not validate the associated disease or outcome claim. [U-A02, U-A18, U-B05 and U-B18 in `UNRESOLVED.json`; `RETAINED_SOURCE_EXCERPTS.json`, `TEXTUAL_CHECKS.json`.]

## 9. Verification and reproducibility

The source file is the retained 1647 Wellcome scan, identified as **LILLY1647_WELLCOME_B30338724**: **894 PDF pages, 141,842,963 bytes**, SHA256 **2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b**. Its hash was recomputed this turn. The original PDF remains external to the records packet; locating crops, source identifiers, page anchors and image hashes are included. The catalogue locator is recorded in `SOURCES.md`. [Evidence: `READING_RECEIPT.json`, `SOURCE_IMAGE_MANIFEST.json`.]

Root inspected all sixteen admitted original page images and froze source notes before reading the candidate records or independent findings. The two source readers retained their own source notes and extraction artifacts. A separate evaluator also froze a full-span source-first reading before receiving the candidate report. That separation is within the same model family; no cross-family or external-expert validation is claimed. [Evidence: `ROOT_SOURCE_FIRST_FREEZE.json`, `READING_RECEIPT.json`, retained source-reader receipts and `independent_review/SOURCE_FIRST_RECEIPT.json`.]

The reference implementation is intentionally limited to selecting source-time evidence, preserving three-valued prerequisites, comparing the two declared lunar thresholds, calculating remaining within-sign arc, and routing exact historical lookups. Full rule combination, astronomical reconstruction, clinical interpretation and calibrated prediction are outside it. A source anchor’s presence and record coverage can be checked mechanically; the correctness of the actual wording requires original-image comparison. [Evidence: `lilly_sixth_opening_reference.py`, `test_lilly_sixth_opening.py`, `READING_RECEIPT.json`.]

The actual final focused-suite execution ran **33 tests**, with **0 failures, 0 errors and 0 skips**. It covers eight time-selection tests, five lunar-motion tests, four prerequisite tests, five remaining-arc tests, five lookup tests and six record-integrity tests. The earlier 32-test run is retained as history, not added to the final total. A repeat execution, including one in an extracted archive, likewise reuses existing test identities. [Evidence: `TEST_B02k.txt`, `TEST_RUN_SUMMARY.json`, `test_lilly_sixth_opening.py`; historical execution in `helper_review/INITIAL_TEST_RUN_SUMMARY.json`.]

To reproduce the bounded suite after extracting the packet, run **`python run_verification.py`** from the folder containing this report, the helper and its JSON companions. Python’s standard library is sufficient for that test run. The execution writes its own log and summary. Historical source images require no test-time download, and the test suite does not require the full original PDF. Source-image rendering is a separate provenance operation. [Implementation: `run_verification.py`, `test_lilly_sixth_opening.py`, `lilly_sixth_opening_reference.py`.]

## Continuation

Resume on **PDF292 / printed258**, immediately below the completed “shew death” paragraph, with **“DARIOT Abridged.” Include its full italic introduction**, beginning “In regard I have ever affected Dariot his Method of judgment in sicknesses,” before continuing onto PDF293. The heading and introduction were inspected to establish the boundary but have not been extracted here. The cumulative Lilly inventory is now 1,549; the next new record number is R1550. Chapter XLIV and the wider multi-author, multipass audit remain open. [Evidence: `SECTION_COVERAGE.json`, `LILLY_SOURCE_EXTRACTION_INDEX_SNAPSHOT.json`, `CONTINUE_HANDOFF.md`.]
