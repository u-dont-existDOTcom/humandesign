# Astrology source audit — Ptolemy I.9–I.16 and replacement Rhetorius

Date: 2026-10-06. Status: completed chapter batch; wider multi-pass source audit remains open.

## Result

The next eight Ptolemy sections have been read and extracted in source order. The batch adds **32 source records** and a separate table covering **95 descriptive fixed-star/asterism groups**. Together with the previous batch, Ptolemy coverage is now **16 of 61 sections**, with **56 source records**. The star table is counted separately; neither its entries nor the rules are independent prediction trials.

The English reading spans PDF pages71,73,…103, corresponding to printed47,49,…79. Shared pages retain precise section boundaries, and reading stops before the I.17 heading on PDF103. Robbins’s relevant notes remain distinct from the translated author text. The facing Greek has not been independently translated, and a complete critical-apparatus collation is not claimed.

## Replacement Rhetorius: improved, but still incomplete

The actual uploaded/private file has **198 PDF pages**, despite the Files reading surface exposing only150. Its copyright page identifies **2009: the fourth translation edition and first published edition**. The third edition mentioned in the filename was the earlier privately circulated2005 version; the page itself governs identification.

Checking the visible printed page sequence found **193 of 222 numbered pages** in the replacement. It omits29 numbered pages. The old preview, though mostly placeholders, retained six that the replacement lacks: **44,45,48,51,52 and81**.

Those six pages have now been extracted into a separate private supplement:

`RHETORIUS_HOLDEN_2009_RECOVERED_SIX_PAGE_SUPPLEMENT.pdf`

Every extracted page was re-rendered and matched its source render, 6/6. Neither original PDF was overwritten. Both witnesses together now cover **199 of 222 numbered pages**, including a continuous printed1–103.

The remaining 23missing printed pages are:

**104,113,115,116,128,129,132,140,148,160,161,170,176,177,178,181,186,191,198,201,214,218,219.**

This is a footer/sequence/readability check, not a claim that every paragraph has been audited or that all frontmatter survives. Missing pages remain marked unavailable. The new book is usable for substantial work without waiting for another upload.

All raw witnesses and the supplement are in the owner's private source directory, outside Git:

`~/Documents/astrology/source-audit-20261005/drive-20261005/`

## What the Ptolemy batch adds

### 1. A fixed-star catalogue must retain local distinctions

I.9 does not give one generic nature to every star in a constellation. It distinguishes heads, mouths, wings, tails and other localized groups, often with different planetary analogues. It also distinguishes unqualified mixtures from cases where one planetary analogy is expressly weaker. For instance, Spica is compared to Venus and, to a lesser degree, Mars; other Virgo groups receive different combinations.

The table retains all 95descriptive groups, their location within the figure, the relevant English page, and any weaker analogue. It does not turn a constellation group into a Sun-sign personality description. Translator identifications, such as a named bright star belonging to a group, are recorded as notes rather than substituted for the entire group.

The chapter does not itself specify a complete modern star-identity catalogue, epoch, natal orb or application trigger. Those remain explicit implementation gaps. Adding such choices later requires separate source support and a frozen convention; it is not part of this reading result.

Source: I.9, PDF71–83 / printed47–59.

### 2. Source definitions differ from familiar shorthand

I.11 separates **solstitial**, **equinoctial**, **solid**, and **bicorporeal** signs. The first two are not collapsed into one modern category in the extraction. The explanation of solid signs also expressly qualifies the claim: seasonal effects are more firmly experienced, not necessarily more extreme weather.

I.12 gives the familiar alternation from Aries, but also reports alternatives beginning with the rising sign or using horizon quadrants. These remain different conventions—not multiple independent confirmations that can all be added to a score.

Source: I.11–I.12, PDF89–95 / printed65–71.

### 3. Aspect classification and its explanation need separate checks

I.13 lists four aspect families: sextile, quartile, trine and opposition. Robbins notes that conjunction is not included in this particular list, while it is treated comparably elsewhere in the work. The fixture therefore distinguishes same-sign co-presence from the four listed aspects; it neither invents a fifth I.13 entry nor deletes conjunctions from other methods.

There is a genuine interpretive issue to preserve. I.13 classifies trine/sextile as harmonious and square/opposition as disharmonious, explaining the latter through opposite kinds. Under the gender-polarity reading supplied by the immediately preceding discussion, opposite signs actually share polarity. The fixture preserves the classification while flagging the explanation for further source work. It does not silently rewrite Ptolemy or claim to have resolved the Greek.

Source: I.12–I.13, PDF93,96–99 / printed69,72–75.

### 4. The source's sign-pair tables should not be silently modernized

Robbins explicitly enumerates five directed commanding/obeying pairs and five unordered equal-power pairs in his notes to I.14–I.15. They are stored as those exact edition-specific tables, with the excluded signs preserved. The author’s broader geometrical/seasonal rationale and the translator's enumeration remain separately attributed.

No modern antiscion or contra-antiscion longitude formula has been inserted to replace those tables. The exact relation between the historical sign descriptions, degrees and astronomical geometry is a matter for the subsequent comparison pass, not an excuse to change the source during extraction.

Source: I.14–I.15, PDF99–101 / printed75–77.

### 5. Units, exclusions and missing conditions matter

Robbins defines seasonal hours as one twelfth of the day or night. A900-minute daylight span therefore gives 75-minute daytime hours and 45-minute nighttime hours. Our fixture is only this unit conversion; it does not invent solar-event or polar-latitude conventions.

I.16 defines disjunct/alien signs by the absence of all the named familiarities, not merely by failing one aspect test. Same-sign co-presence is not declared alien just because it is outside the four-aspect list. Unknown inputs remain unknown rather than false.

Source: I.15–I.16, PDF101–103 / printed77–79.

## Calculations and checks

The new bounded definition module has **31 passing tests**. They cover every ordered pair of the 12signs, source-specific classifications, directionality and exclusions of the pair tables, unknown/invalid inputs, seasonal-hour units, preservation of fixed-star subgroups and qualifiers, and record/hash integrity. These are definition and software checks, not empirical evidence that the doctrine predicts lives.

The combined regression suite passed 83 tests: 31 new definition tests, 18 earlier source-definition tests and 34 methodology tests. The earlier chapter-count assertion was scoped to its own I.1–I.8 batch, so valid later reading no longer makes it fail. The initial failure and test-maintenance change are preserved alongside this report. No historical person prediction, fitted timing model, numerology rule, or live prediction engine was changed. The previously completed I.1–I.8 source batch remains intact.

## Next batch

**B01c: Ptolemy I.17–I.24**, starting at the I.17 heading on English PDF103 / printed79. This covers planetary domiciles, triangles, exaltations, terms and their variants, places/degrees, faces/chariots, and applications/separations. The remaining books the owner could not find are not a prerequisite for this batch.

Canonical companion files: `RULES.json`, `FIXED_STAR_TABLE.json`, `READING_RECEIPT.json`, `UNRESOLVED_TERMS_AND_VARIANTS.json`, and the updated parent source-audit checkpoint. Newly extracted rules are retained for the later compilation/comparison pass, not automatically promoted to a validated merged predictor.
