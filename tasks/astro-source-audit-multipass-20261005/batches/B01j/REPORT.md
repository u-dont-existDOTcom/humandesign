# Astrology source audit: wealth, status and occupation

Date: 2026-10-06. Batch B01j. Source: Ptolemy, *Tetrabiblos*, F. E. Robbins translation, supplied 1964 reprint of the 1940 edition. Targeted comparison: Rhetorius, Holden's published 2009 translation, using the supplied PDF and owner OCR.

## Completed scope and direct progress

Ptolemy IV.1-IV.4 is read and extracted in the declared English scope, from the Book IV heading on PDF397/printed373 through the close of IV.4 before marriage on PDF417/printed393. Relevant English notes, including those below the shared closing page, are included. All eleven English pages in this span were visually inspected. Greek main text and the full textual apparatus were not independently translated or collated.

| Section | Source records |
|---|---:|
| IV.1: transition to external circumstances | 1 |
| IV.2: material fortune | 14 |
| IV.3: fortune of dignity/status | 18 |
| IV.4: quality of action/occupation | 41 |
| New Ptolemy records | **74** |
| Cumulative Ptolemy records | **407** |

The completed Ptolemy section count is now **42 of 61**. Books I and III remain complete; four of ten Book IV sections are complete. Six Book IV sections and thirteen Book II sections remain unread. This is not completion of the whole book/corpus, an empirical validation result or runtime model promotion.

The structured tables include **19 conditional occupation branches**, five acquisition-channel rows, four bases of honour, four sign-form modifier classes and four special Moon-Mercury groups covering ten signs. These are representations of source statements, not independent observations or predictions.

## 1. Wealth, rank and work must not be treated as one success score

IV.2 starts material acquisition from the Lot of Fortune and its relevant rulers, then considers strength, familiarity, testimony, retention and loss. IV.3 starts status from the luminaries and their attendance. IV.4 separately addresses action and occupation. The source's Saturnian acquisition channels include building, agriculture and shipping ventures; a later statement about power based on accumulated wealth is not another independent measurement of the same outcome (PDF397-405/printed373-381).

Within each topic, keep the outcome distinctions. Receiving an inheritance, retaining it and the period over which wealth lasts are different predictions. Likewise, rank, its security, the basis of power, type of work, independence in that work and its profitability are not interchangeable. IV.4 explicitly separates the species of action from its amplitude (PDF415/printed391).

Project implication: a later scoring layer should not credit a vague success prediction for any favourable result in any of these domains. This is a source-informed design implication, not an implemented or validated scoring change.

## 2. The occupation method can retain two rulers

IV.4 instructs the reader to inspect two routes: the planet making its morning appearance nearest the Sun and the planet associated with culmination, particularly with the Moon's application. If the same planet satisfies both, use it once. If two different planets satisfy the routes, retain both and give preference according to the earlier strength/rulership method. Only when neither route supplies a planet does the chapter fall back to the ruler of the culminating region for occasional pursuits (PDF405-407/printed381-383).

The new reference helper preserves these branches. It does not turn a tie into a winner or a missing calculation into known absence. Crucially, its inputs are **caller-established conditions**: it does not calculate visibility, define nearest appearance, choose a house system, or select rulers from an actual natal chart.

There is an unresolved transition in the text: the selection method is broadly phrased, while the detailed action-quality lists concern Mercury, Venus and Mars. No standalone Saturn/Jupiter action-quality profile or automatic conversion into one of the three is supplied in this passage. The helper marks that gap rather than filling it.

## 3. The Rhetorius comparison prevents a silent rule substitution

Rhetorius 82 includes additional relevant houses, Fortune, lunar application and a **seven-day before/after appearance window**, including an evening-rising option (printed134). That window is not stated in Ptolemy's corresponding two-route selection passage. It is preserved as part of the Rhetorius method, not inserted silently into the Ptolemy profile.

Later in the same chapter, Rhetorius explicitly identifies material as Ptolemy's teaching, and closely repeats the sign-form and Moon-Mercury groups (printed135-136). This is **explicit source reuse**, not independent empirical confirmation. Four targeted comparisons now record admission differences, attendance definitions, reuse with variants, and translation-level predicate differences. The wider Rhetorius audit is not being counted as complete.

One concrete predicate difference: Robbins has benefics or malefics **overcoming** the action rulers; Holden's corresponding Rhetorius passage is rendered as **aspected**. The difference is verified at the supplied English-witness level. It is not a claim that the underlying Greek disagreement has been independently established.

## 4. Historical class labels cannot be replaced by familiar modern labels

The action chapter's sign forms are not simply a modern element table. Robbins's Hephaestion-derived notes list terrestrial signs as Aries, Taurus, Scorpio and Sagittarius, distinguish aquatic Pisces from amphibious Cancer and Capricorn, and give partly human Sagittarius in another list (PDF413-415/printed389-391). The quadrupedal list printed in the note contains Leo and Sagittarius. Its omissions are preserved, not silently filled from a different classification.

The special Moon-Mercury role list names ten signs in four groups. Gemini and Aquarius receive no assignment in that particular list. A missing assignment remains missing, rather than being invented from symmetry.

The occupational tables also retain historically uncomfortable entries and mixed branches. They are source descriptions with prerequisites, not accusations or identity classifications about anyone.

## 5. Explicit uncertainties are retained

IV.2 repeats the same Fortune calculation by day and night, but Robbins questions the authenticity of the clause (PDF397/printed373). This is new transmission context, not permission to alter the already frozen formula.

The closing Saturn phrase, cold and mixtures of colours, remains obscure. Robbins reports commentator explanations; Holden labels the related Rhetorius phrase corrupt. Neither is smoothed into a convenient generic prediction of career delay, depression or illness (Ptolemy PDF417/printed393; Rhetorius printed137).

Fourteen unresolved items are saved, including appearance geometry, angular criteria, mixed sect/benefic testimony, tied rulers, translation variants, modern occupational targets and timing. The angular timing descriptions do not by themselves supply exact event dates; IV.10 remains pending.

## Verification and preservation

The new isolated suite passes **61 checks**. They exercise caller-qualified route reconciliation, all 19 source-row lookups, order invariance, unknown versus absent evidence, tied precedence, invalid inputs, unsupported ruler combinations, table/reference completeness and reading-receipt hashes. They do not establish source-semantic independence, actual chart qualification or empirical accuracy. The combined integration run passed **286 checks**: these 61 new checks plus the 225 retained checks. Its exact command, exit code and measured test time are recorded in `VERIFICATION.json`.

All earlier source batches, retained astrology/numerology candidates, runtime code and personal prediction freezes remain unchanged. Only four existing source-progress documents are advanced. Source PDFs, full text and page images remain outside Git. No new OCR, paid acquisition or personal analysis was performed.

## Next saved batch

**B01k: IV.5-IV.6**, marriage and children. Start the marriage heading on **PDF417/printed393**; children begins on **PDF433/printed409**. Stop before IV.7, friends and enemies, on **PDF437/printed413**. These later headings have been located, not counted as chapter reading.

This completes the declared increment under the owner-authorized multiple-pass plan. The parent source audit remains OPEN; no unattended work is claimed after delivery.
