# Astrology source audit: natal method, parents and siblings

Date: 2026-10-06. Batches B01d and B01e. Source: Ptolemy, *Tetrabiblos*, F. E. Robbins translation, supplied 1964 reprint of the 1940 edition.

## Completed work

The exact saved continuation, Book III.1–III.3, is complete. The reading then continued through III.4–III.5, so this pass includes the first five natal chapters rather than stopping after the methodological introduction.

The English main text was read on PDF pages 245–279 (odd-numbered pages), printed pages 221–255, stopping immediately before the III.6 heading on the final shared page. English translator notes were included; notes starting on facing pages 254 and 258 were followed across their continuation. The facing Greek was not independently translated and the entire critical apparatus was not collated.

| Scope | New source records |
|---|---:|
| III.1–III.3: beginning, birth-time/horoscopic degree, topic selection and synthesis | 27 |
| III.4–III.5: parents and siblings, modifiers and derived reference frames | 28 |
| This pass | 55 |
| Cumulative with Book I | 164 |

The source inventory now has **29 read sections out of 61**, with **32 still unread**. Book I remains 24/24; Book III is now 5/14. Book II's thirteen general/mundane chapters remain explicitly deferred, not treated as completed or discarded. Book IV remains unread.

These counts are organizational records, not independent predictions or a measure of empirical effectiveness. The parent multi-pass corpus audit remains open.

## 1. Ptolemy supplies a topical method, not a universal personality score

III.1 explains his decision not to enumerate a nearly unlimited list of combinations of all or most stars. That is not a refusal to synthesize: he gives the places and powers relevant to each subject, then explicitly leaves their combined judgement to the investigator (PDF 251–253, printed 227–229).

III.3 makes the order operational:

**Question → relevant place → planets with rulership claims → quality → magnitude → timing.**

His examples are the Midheaven for action and the Sun's place for the father (PDF 261, printed 237). The following paragraph assigns rulership through the stated forms of familiarity, allowing multiple rulers rather than selecting one planet as the answer to everything.

This matters to the research architecture. A chart-wide dominant planet, even accurately calculated, does not automatically become the ruler of work, parents, relationships and every other question. The new `TOPICAL_SYNTHESIS_SPEC.json` preserves this source-defined structure for later compilation. It does not modify the existing prediction engine.

## 2. Five forms must not become six—or a different five

III.2 lists **trine, house, exaltation, term, and phase or aspect** (PDF 257, printed 233). Phase/aspect occupies one of the five categories. It is not a license to substitute face/decan as the fifth item, nor to award two independent category votes because both phase and aspect are present.

The bounded fixture counts lower/upper numbers of distinct supported forms, retaining unknown evidence. It does not impose a universal weighted dignity table or complete the author's unspecified priority rules. Equal claim counts remain ties; incomplete claims remain unresolved where they could change the ordering.

The terminology itself still needs the declared source profile: the translation's “trine” and the phase/aspect alternative are preserved rather than silently turned into a favorite modern implementation.

## 3. The birth-time correction method is recorded, but not presented as verified birth data

III.2 begins with an approximate time and its ascensional rising degree, then selects the last preceding new or full moon. It examines the relevant syzygy degree and its rulers, transfers a ruler's **degree within its sign** to the appropriate nearby rising sign, uses degree proximity among co-rulers, and then invokes centres and sect for close candidates. It also permits the Midheaven to become the reference when the corresponding degree is nearer it (PDF 253–259, printed 229–235).

Several important choices remain unspecified or disputed: the moment at which the full-moon luminary's above-horizon status is assessed; the precise phase/aspect condition; what counts as “close”; conflicts between centre and sect; ordinal versus continuous degrees; and the inversion from proposed degree to time.

Robbins's note is particularly important: the adopted text evaluates rulership at birth, while the note expresses a preference about the luminary at conjunction rather than nativity. The note says “conjunction”; that wording is retained even though the preceding selection also includes opposition. It would be misleading to hide this issue behind an apparently precise corrected birth minute.

The new code therefore implements only transparent fragments: ordering already supplied new/full-moon instants, preserving a coincident-event ambiguity, and projecting a degree into an already admitted sign. It does not calculate a full rectification and has not changed anybody's birth time.

## 4. Nature, force and timing are different outputs

III.3 derives the **quality** of a judgement from the rulers and relevant sign natures. It derives **magnitude** from their ability to act in cosmic and natal conditions. General earlier/later action then depends on orientation and angular/succedent situation (PDF 263–265, printed 239–241).

A strong configuration is therefore not automatically a pleasant result. Nor does a statement about acting early specify a calendar year. Robbins also explains “increasing in numbers” as direct motion, not acceleration; the extraction keeps that gloss separate from the author's wording.

The source provides no universal numeric scale that converts all these conditions into a single certainty percentage. Unspecified aggregation remains explicit rather than being filled with arbitrary weights.

## 5. Contradictions can indicate dominance, mixture or a sequence

III.4 says to compare competing rulers' power. Where claims are equal, rulers together are interpreted as a mixture; separated rulers can produce their different results at successive times, first the more oriental and then the occidental (PDF 273–275, printed 249–251).

This is more informative than always averaging “good” and “bad” to neutral, or keeping only the interpretation that fits a known life. But the terms together/separated and the timing scale are not a complete numerical algorithm in this passage, so the record does not pretend they are.

The same passage adds an important timing dependency: a planet without original familiarity with the queried place has **no great influence** on it. That is a qualified claim about major topical influence, not literally zero possible effect. Timing itself is then distinguished from the initial rulership. We retain the qualification and do not use this passage to retroactively revise any fitted event model.

## 6. Parent rules are more conditional than a list of hard aspects

III.4 retains two natural significators per parent: Sun/Saturn for father, Moon/Venus for mother. It then emphasizes Sun/Venus by day and Saturn/Moon by night. The preferred significator does not erase its partner (PDF 265 and 273, printed 241 and 249).

The chapter separates parental status, inheritance reaching the child, health/longevity, and the kind of an adverse event. In particular, **parental wealth and receiving the inheritance are not the same outcome**: the latter is additionally related to the Lot of Fortune and the attendants (PDF 267, printed 243).

A useful explicit negative rule occurs in the paternal longevity passage. A favorable configuration qualified by adequate power supports its stated longevity testimony. When weak, it does not signify the same thing, **but that weakness does not itself indicate a short life** (PDF 269, printed 245). Absence of support is not support for the opposite.

Historically medical and mortality descriptions are retained faithfully as research-only source material, with their alternatives, qualifiers and uncertain referents. They are not converted into modern diagnoses or presented as reliable forecasts about living parents. No participant's parental history was consulted in this extraction.

## 7. The sibling chapter contains a real unresolved reference problem

III.5 describes the culminating sign and maternal place, associated with Venus by day and Moon by night, then also the succeeding sign. Robbins explicitly says that both the adopted manuscript reading and Camerarius's alternative are difficult to understand (PDF 275–277, printed 251–253).

The extraction does not “repair” this into a generic third-house rule. A later implementation must either name and justify an interpretation or retain the reference as unresolved. The general sibling-quantity testimony likewise does not supply an exact count recipe; the author expressly cautions against demanding exact numbers.

Other distinctions are preserved: first-born versus first-reared, sibling status versus friendliness, and friendship versus living together. The last of those has an additional Fortune relation in the source (PDF 277–279, printed 253–255). Derived parent/sibling horoscopes are labelled as significator-based reference frames, not independently observed birth charts of those relatives.

## 8. A qualified rejection must survive later context

III.3 rejects lots and numbers **for which no reasonable explanation is given**. III.4 nevertheless uses Fortune for inheritance, and III.5 uses it for sibling co-residence. The correct extraction is not “Ptolemy prohibits every Lot.” It also is not a judgement about the empirical effectiveness of modern numerology. The actual Fortune calculation remains for its later chapter.

## Verification and preservation

The new source-definition/integrity suite has **23 passing checks**, including grouped phase/aspect counting, unresolved evidence, ties, invalid inputs, supplied-syzygy ordering, coincident times, equivalent timezone instants, degree projection, retained parent significators, source-ID continuity and preservation of adverse-rule qualifications. The integration receipt records the combined run with earlier source and methodology tests.

These are engineering/definition checks, not independent translation, real-world prediction tests or proof of source correctness. The source helper does not calculate birth charts, prescribe remedies, predict mortality or perform the full topical synthesis.

Raw books, complete extracted text and source-page images remain outside Git. The prior 109 source records, existing fitted candidate rulesets, numerology methods, participant freezes and production chart code remain unchanged. The accepted Rhetorius OCR and copy-specific missing-page qualifications are unchanged; no repeat upload is required.

## Continuation

The next indexed source batch is **III.6–III.9**, starting at the III.6 heading on PDF279 / printed255 and ending immediately before III.10 on PDF295 / printed271. These historical birth-related chapters will be source-audited without turning their classifications into modern medical or identity claims. The later length-of-life chapter is a separate unit; nothing about it is counted as read here merely because its boundary was located.

No unattended/background work is claimed. The repository checkpoint resumes at this exact first unfinished section under the owner's multi-pass authorization.
