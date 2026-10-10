# Source reader A: initial frozen observations

## Boundary and source

Read only the assigned passage of William Lilly, *Christian Astrology* (1647): PDF292/printed258, beginning at **DARIOT Abridged.**, through PDF297/printed263, ending with **this is, when mistrust is of such like chances.** The immediately following right/left-body heading is excluded. The preceding paragraph ending **shew death.** is excluded. Reader B owns the right/left heading onward.

Original PDF: `/workspace/scratch/bd2460f96de0/Lilly-1647-Christian-Astrology-I-III.pdf`.

Verified SHA-256: `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`.

Verified page count: 894. The printed/PDF offset in this span is 34 pages.

All six pages were freshly rendered from that PDF using `pdftoppm -f 292 -l 297 -r 180 -png`, then visually inspected. Original render size is 1883 by 2548 pixels. Existing `source-work/pdf292.png` through `pdf297.png` were inspected first as navigation conveniences, then checked against original-PDF renders. Source crops were made only for close visual inspection. No OCR or text extraction supplied the source wording.

## Complete italic introduction

The following is the complete introductory paragraph, with long s normalised to s and physical line-break hyphenation joined. Original spelling is retained.

> In regard I have ever affected Dariot his Method of judgment in sicknesses, I have with some abbreviation annexed it, in a farre more short way and method then heretofore published.

The speaker is Lilly, who distinguishes his attachment/abbreviation from Dariot's method. The introductory preference, abbreviation, annexation, and comparison with earlier publication all remain in A001. This introduction is not a sickness rule and supplies no patient case.

## Inventory and whole-passage reconstruction

The inventory has 54 source records and 23 source units. SECTION_MAP.json accounts for every owned heading and paragraph, including both cross-page paragraphs and italic first-person closures. Record splitting follows changes in conditions, outcomes, chronology, actor, or evidence class, not a record-count target.

The argument moves from whether the queried party is sick, to distinguishing inward and outward causes, then to the quality and nature of disease as described by the relevant planet. The outward-cause passage is necessary context for the second-, fifth-, and seventh-house examples; those examples must not be detached into unconditional financial or relationship forecasts. The planetary sequence presupposes a disease-judgement figure and selected disease significator. Saturn, Jupiter, Mars, Sun, Venus, Mercury, and the final ninth-house-lord sentence have all been retained with their variants. The Moon and nodes occur in conditions but there is no separate Moon disease paragraph in this owned span.

The full argument preserves illness versus transient bodily distemper; inward versus accidental/outward affliction; applying versus separated significators; recent spouse difference versus youth's present discontent; merely melancholy versus no later sickness; usual versus categorical wording; qualified poison/occult suspicion; and the moment when a disease only seems to leave. The Sun's first-lying-down judgement is not the same time anchor as Lilly's general question/urine method.

## Attribution and evidentiary status

Marginal **Dariot.** marks the first sickness block and the inward-cause block at printed259. Its continuation into the outward-cause method is retained until the new **Lilly.** marginal mark at printed260. **Lilly.** also marks the earlier urine/question-practice block. Lilly's long outward-cause illustration ends at the top of printed261 with the italic declaration that this is the method he ever observed and freely communicates.

The new quality/nature subsection opens with a first-person editorial statement, attributed here to Lilly's continuing voice. The following planetary rules have no fresh marginal name. They are labelled **ambiguous** with precise evidence: likely Lilly's exposition, within an acknowledged abridgment of Dariot. No independent original Dariot edition was consulted, so this reader cannot certify sentence-level original authorship.

No individuated patient enquiry, dated/reconstructible patient chart, or observed patient endpoint is supplied within the assigned span. Lilly refers to enquiry practice in general, and says he ever observed the method. Those broad author-experience statements are preserved in A001, A007, A008 and A021; they do not produce a case denominator or verified outcomes. The money, diet, games, pension, marital and youth examples are schematic illustrations. Promised recovery, no future sickness, death expectation, or one-day duration is an asserted outcome, not a recorded follow-up.

## Source-preserving normalisation

- Long s is rendered s. Physical line-break hyphens are joined when they divide a single word. Meaningful compounds remain as printed when quoted. Small-capital opening words and letter-spaced headings may use ordinary word case and spacing in anchors.
- Planet glyphs are transcribed as Saturn ♄, Jupiter ♃, Mars ♂, Sun ☉, Venus ♀, Mercury ☿, Moon ☽. Node glyphs are North Node ☊ and South Node ☋. In the critical printed261 phrase the visual order is South Node then North Node.
- Aspect glyphs use conjunction ☌, square □, opposition ☍, trine △ and sextile ✶. Familiar sign glyphs use their Unicode equivalents. In prose propositions and condition lists, their names replace the glyphs transparently.
- Short source anchors preserve wording and grammar after these declared display normalisations. A normalised symbol is not evidence of a different symbol in the original.
- Historical spellings and categories remain source content. **Vitious** is read as **vitious** in the Saturn water-sign paragraph, not silently changed to viscous. The apparent **of** after Gluttony is retained and flagged for reinspection. No historical disease label has been mapped to a modern diagnosis.
- **&c.**, **the like**, **as in**, **may**, **usually**, **chiefly**, **principally**, **almost**, **then**, **lately**, and **presently** remain meaningful scope or modality markers; unspecified list extensions, times, thresholds and weights are not invented.

## Important unresolved points

SOURCE_ISSUES.json preserves eleven issues/dependencies. The most consequential are the opening NOT scope in Lilly's no-sickness chain; combination logic in the diurnal list and the unstated nocturnal adjustments; authorship of the planetary sequence; the Leo/Scorpio node-modifier attachment; the reach of the Saturn water/co-significator description; the fifth-house youth parenthesis; Saturn/Mars dignity ownership; and the scope of the Sun/Mars phrase aforesaid Aspects. These are local source/implementation uncertainties. They do not justify discarding the source unit or silently repairing it.

Several clear qualifiers need particular care in downstream transformations: both the poison statement and the final occult-cause sentence require existing suspicion; Jupiter's fire-sign fevers are without rottenness **or store of** putrefaction; Mars/common signs plus Saturn **in aspect with good planets** does not say a good aspect; Mars joining Venus **in signification** does not necessarily mean conjunction; under the Sun's beams is not silently equated with combustion; and the fixed-sign example names exactly Taurus, Leo and Aquarius after the general class.

The Jupiter air-sign branch contains a historical recommendation about breathing a vein or sweating. It is captured as source content, not current medical guidance or a successfully observed intervention. This handoff contains no personal forecast, diagnosis, or treatment recommendation.

## Task-time activation and application receipt

Parent directive: source reader A only; root is sole repository writer, integrator, publisher and final-delivery owner. Parent audit remains OPEN. Output here is a local handoff for root's exact-hash acceptance and durable publication.

The task start supplied by the parent is **2026-10-10T19:24:34+00:00**. It is task metadata, not a fabricated observation-freeze or issuance time. No clock was read during source reading.

Current default-branch UDA AGENTS.md and LESSON-INDEX.md were fetched with the GitHub connector in this worker turn. Returned blob SHAs were `c27948c88cf7553f95241cbae7edab27f87689d2` and `9055c85c1278c3775b2fdb440f2725e8d4ef030d`. Parent reported current UDA root commit `af8d29833f9e1e03156c0df5487160aa8316c896`. The loaded source-interpretation-provenance and whole-argument-reconstruction blobs were `bb58d19c1999afcfdb39a134f24402ed4784926a` and `9a0ef18ba93c6f3a3c5578522b6e36463c777e96`. Task-time activation guidance was also loaded.

Active contract and application evidence:

| Obligation | Required behaviour | Evidence / disposition |
| --- | --- | --- |
| Exact source provenance | Use original PDF renders; keep quotation separate from interpretation | Verified PDF hash/page count; six original renders and critical crops; per-record exact short anchors and separate propositions. Applied. |
| Whole-argument reconstruction | Account for every owned unit and retain cross-page qualifications | SECTION_MAP.json maps all 23 headings/paragraph units to 54 records; temporal, authorial and logical dependencies retained. Applied, subject to listed ambiguities. |
| Conditional and polarity fidelity | Preserve AND/OR, negatives, variants, actor and modality | A005-A006, A008, A025-A029, A040-A044, A048-A052 explicitly retain unresolved scope; no silent repairs. Applied. |
| Evidence-class integrity | Separate general rule, illustration, method and author experience; no invented cases | Every record declares kind and case_evidence; zero admissible individuated cases from this span. Applied. |
| Reader isolation | Freeze observations before consulting any other producer result | No other worker/candidate output was inspected; freeze is the exact deliverable set bound by HASH_MANIFEST.json. Applied. |
| Write isolation | Write only under source_a; no Git/canonical mutations | All worker-created files, renders, crops and builder are under the assigned source_a directory. Applied. |
| Parent continuation | Do not claim parent completion or runtime promotion | This is source extraction handed to root for integration/review; audit remains OPEN. Applied. |

This is the producing reader's source inventory and semantic application assertion, not independent evaluation. Hashes establish exact bytes, not correctness of interpretation. Any post-freeze reconciliation must preserve this initial observation set and produce a separately labelled delta.
