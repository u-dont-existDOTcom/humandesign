# Ptolemy: complete English extraction, eclipse-to-natal conditions, and seasonal methods

7 October 2026 · HumanDesign source audit · B01r–B01s

## Result and scope

All **61 sections of the supplied English Tetrabiblos are now read and extracted**, including both transmitted endings of Book IV and the identified English editorial notes. The final seven Book II chapters add **184 source records**: 100 in II.7–II.8 and 84 in II.9–II.13. The cumulative inventory is **1,066 records**, spread across nineteen preserved batches.

| Book | Sections | Source records | Main scope |
|---|---:|---:|---|
| I | 24 | 109 | Definitions and foundational conditions |
| II | 13 | 358 | General/regional events, eclipses, seasonal and observational methods |
| III | 14 | 224 | Natal method, family, bodily and character enquiries |
| IV | 10 | 375 | Fortune, occupation, relationships, travel and timing |
| Total | 61 | 1,066 | Complete declared English-reading scope |

These are records of rules, definitions, qualifications, source variants and editorial explanations. They are not 1,066 independent predictions, nor a set of calibrated probabilities. The inventory includes historical medical and social claims as attributed source material, not recommendations or modern diagnostic categories.

This finishes the first-source **English reading/extraction stage**, not the entire multi-source methodology audit, an independent Greek collation, or a completely specified predictive program. Unresolved interpretation and implementation choices remain explicit. No personal history was opened to select these records; no existing personal prediction, fitted astrology/numerology model or runtime engine was changed.

## Recovery and preservation

The interrupted work had already produced complete draft records and reference code in the conversation filesystem. These drafts were recovered, checked against the supplied source and page images, and finalized rather than discarded or recreated. Current GitHub still pointed to the preceding geographical/eclipse-timing checkpoint at recovery.

`PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json` now locates all nineteen batches, their counts and content hashes or verified Git blob identifiers. The first 24 records and the 59-record quality-of-death batch were verified in current GitHub because their full files were absent from the partial conversation snapshot. That is a recovery distinction, not missing repository work. Their historical full extraction remains preserved, and this turn does not claim a fresh full re-reading of them.

The section index maps every chapter to its record IDs. Current progress and the pass plan agree on **61 read / 0 unread English Ptolemy sections**. Previous state is retained unchanged as `state/ASTROLOGY_SOURCE_AUDIT_THROUGH_B01q.md`.

## Findings with the greatest relevance to later analysis

### 1. Ptolemy supplies a conditional link from general events to a natal chart

The end of II.8 states that people whose natal luminary or angle places coincide with an eclipse place or its opposite are usually affected by the described general misfortunes. It then gives special emphasis to an exact degree coincidence or opposition involving either natal luminary. This comes **after** deciding the event's region, time, affected class and quality. [II.8, printed 189–191; PDF 213–215.]

This matters in two ways. First, a regional event and the question of which people it affects are separate layers. Second, this is not an instruction to treat every eclipse contact as a personal catastrophe: the chapter explicitly considers favorable as well as unfavorable general outcomes, with planetary mixtures and regional modifiers.

The new helper calculates only exact contact geometry on supplied longitudes and identifies the luminary emphasis. It does not supply an orb, infer the general adverse context, estimate personal risk, or predict an event. A nonexact result under this narrow helper is not evidence of safety or absence under other rules. The input's astronomical uncertainty remains separate from exact rational arithmetic.

### 2. The event's governing planets must be selected before their descriptions are applied

II.7 considers familiarity with the eclipse place and the relevant angle through applications/recessions, aspects, domicile, triplicity, exaltation and terms. When the same planet qualifies for both, it governs alone; when different planets qualify, both are retained, with preference to the eclipse governor. Rival candidates require further comparison. [II.7, printed 169–171; PDF 193–195.]

The English text itself alternates between a preceding and following angle. The critical note and the main-text alternatives are retained, not silently repaired. The nine visible fixed-star configurations are explicitly a reference to the Almagest, as identified by Robbins, not nine ordinary zodiacal aspects calculated here.

The conditional helper requires caller-qualified maximal candidates and a declared angle convention. It retains ties and unknown inputs; it does not invent scores, choose a convenient planet, or silently collapse tied candidate sets to their overlap.

### 3. Repeating a planetary quality in several forms does not automatically add independent evidence

II.8 says its planetary-nature language also applies to fixed stars and zodiacal places of analogous nature. It calls for their mixture with planets as well as mixtures among the planets themselves. Cardanus's term-related gloss is separately attributed through Robbins. [II.8, printed 178–179 and 188–189; PDF 202–203 and 212–213.]

This preserves additional interpretive structure, but the different carriers must remain traceable. Our methodological implication is to distinguish a compound symbolic configuration from several statistically independent confirmations. The text supplies no numerical multiplier, calibrated interaction weight or empirical independence claim.

The regional modifiers also preserve polarity. A benefic that is less helpful is not thereby explicitly harmful; an injurious governor doing less harm is not thereby explicitly beneficial. Familiarity with the subject, lordship of the country, opposite-sect overcoming and overcoming by a locally familiar planet are not silently treated as the same condition. [II.8, printed 189–191; PDF 213–215.]

### 4. The annual seasonal method has four beginnings, and the monthly method retains its phase choice

Although II.10 is titled with the year's new Moon, it explicitly considers **new or full Moons** nearest before the seasonal boundaries. Ptolemy prefers all four seasonal beginnings rather than one absolute starting point. Eclipse emphasis remains part of the text, but no undocumented rule allows selecting an older eclipse instead of the closest preceding syzygy. [II.10, printed 195–201; PDF 219–225.]

II.12 then retains the selected new/full phase for the monthly sequence until the next seasonal quarter. Robbins's example uses new Moons in Aries, Taurus and Gemini when a new Moon supplied the spring reference, and full Moons when it was a full Moon. The reference helper labels the adopted interval convention and requires a complete candidate inventory. It does not compute actual lunations or ingresses. [II.12, printed 206–209; PDF 230–233.]

The deeper sequence is seasonal setting, monthly variation, lunar-phase details, day-to-day stellar appearances and hour-to-hour angular passages. The source makes general causes primary and particular causes subsidiary, with reinforcement when their governors participate together. These are historical weather methods here—not automatically imported into natal event timing. [II.12, printed 207–213; PDF 231–237.]

### 5. Part of the method needs real observations, not merely an ephemeris

II.9 adds observed eclipse colours and comet forms/directions. II.13 uses visible solar/lunar appearances, halos, stellar brightness compared with usual appearance, clusters, clouds and rainbows. Computing a planet's position does not supply those observations. [II.9, printed 191–195; PDF 215–219. II.13, printed 213–219; PDF 237–243.]

The lookups therefore retain an observation requirement. The rainbow example is explicitly conditional on prior weather: the historical interpretation differs after clear weather and after storms. No accuracy claim is made for either branch.

Comet timing remains qualitative in this passage. Its duration/onset remarks are not silently given the eclipse chapter's hours-to-years or hours-to-months multipliers.

## Source tensions preserved instead of repaired

The new batches contain **34 unresolved issues**: 18 in B01r and 16 in B01s. Among them:

- The preceding/following angle wording and incompletely quantified governor/tie selection.
- The difference between the fraction of an affected class and the probability that an event will happen. II.7's minority/half/majority clauses also require eclipse obscuration, with no complete numerical combination formula supplied.
- The printed English labels “autumn solstice” and “winter equinox” in II.7, which conflict with the surrounding seasonal scheme. They are preserved as a witness discrepancy, not corrected silently or implemented as astronomy.
- Leading/middle/following portions versus northern/southern portions in II.11. These do not authorize automatically treating every portion as an equal ten-degree decan.
- II.12's three-day wording and Robbins's conjunction gloss alongside a discussion that includes quarters; II.13 separately names new, full and quarter Moons. No uniform symmetric timing window was invented.
- The possible textual addition involving the two stars called the Asses, noted by Robbins in II.13.

## Verification and limits

The verification receipt records the actual commands and counts. The newly added reference suite covers conditional ruler reconciliation, affected-class extent, regional modifiers, exact contact geometry, phase-consistent chronological selection, source-specific tables, observation requirements and deterministic regeneration.

During final review, two unpublished helper details were corrected: known absence of an eclipse observation now takes precedence over a missing colour field; and a monthly selection cannot claim a valid series for an empty requested sign domain. Tests cover both.

Tests establish bounded code behavior, record integrity and the declared source mappings. They do not certify complete semantic fidelity, astronomical implementation, predictive accuracy, or the full HumanDesign application. No independent model review is claimed. Raw books, their full extracted text, page images and personal case data are excluded from the repository packet.

## Next source and remaining owner outcome

The saved plan proceeds to **William Lilly's Christian Astrology, 1647, Books I–III**, using the already identified full Wellcome witness. The next operation is source recovery and exact contents/page mapping, including the catalogued missing-final-leaf caveat, followed by Book I definitions. Books I–II alone cannot substitute for natal Book III. Already extracted selected Lilly rules remain retained and are not mistaken for a complete Lilly audit.

Ptolemy's source index is a retrieval foundation for the later comparison, not a merged new prediction model. The broader work still requires the other available authors, reconciliation of shared and conflicting conventions, reproducible astronomical implementation, frozen development comparisons and genuinely untouched later validation.
