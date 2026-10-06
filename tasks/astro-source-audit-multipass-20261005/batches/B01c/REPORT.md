# Astrology source audit: Book I completed; owner OCR integrated

Date: 2026-10-06. This completes the declared English Book I reading/extraction batch, not the full Tetrabiblos, the entire corpus, or a validated prediction model.

## The supplied Rhetorius OCR

The owner-provided `rhetorius.txt` is now an accepted searchable reading aid. Its exact bytes were found in the owner's Downloads directory, hash-matched to the uploaded attachment, and copied beside the private books as `RHETORIUS_HOLDEN_OWNER_OCR_20261006.txt`. The raw text stays outside Git; the repository stores provenance and a reconciliation record.

The correction prompted two separate checks rather than an automatic concession or defense of the old result:

* **Extraction failure is not page absence.** A simple numeric-footer parser misses ten labels in this OCR—printed pages 1–9 and 192—even though their corresponding segments contain text. Those must not be counted as missing pages. The limited Files image surface also exposes only 150 pages while this actual PDF has 198. Neither limitation defines the book's completeness.
* **Some continuity gaps remain visible in the exact supplied copy.** Re-rendering PDF pages 100 and 101 shows printed 103 followed by 105, with interrupted main-text continuations. The new OCR has the same transition. PDF pages 108 and 109 likewise show printed 112 followed by 114. This is evidence about these exact supplied bytes, not an assertion about every copy of the edition or a conclusion from OCR failure alone.

The earlier 23-gap list remains a **copy-specific page-sequence audit**, with the six recovered pages kept in their separate supplement. This turn does not re-certify a complete paragraph-by-paragraph collation of all 222 numbered pages. Available Rhetorius material can be studied now; obtaining another copy is not a prerequisite for the current work. No new OCR was run.

Evidence: `../../RHETORIUS_OCR_RECHECK_20261006.json`; original PDF SHA-256 `fa587dd2b04245c63198c9438c9edd9f8164b0a165b824f386e4c890f3dd5e86`; owner OCR SHA-256 `40e9079274d6ced431a8b48d8105ad3d0b830a877acfedd54c73dcff8362d599`.

## Reading completed

Ptolemy I.17–I.24 was read in source order, beginning at the I.17 heading on PDF 103 / printed 79 and ending above the Book II heading on PDF 141 / printed 117. The final page is shared: stopping at PDF 139 would have omitted the concluding hierarchy of angular strength.

All **24 Book I chapters** now have English main-text reading and extraction records. Across the three batches this gives **109 source records**, including **53 new records** here. The earlier 95 descriptive fixed-star groups remain a separate table. Record counts are organizational units, not independent predictions or measures of predictive accuracy.

Two five-planet term tables were transcribed from the rendered English pages: **60 cells each**, Egyptian and Ptolemaic. The Chaldean construction was implemented separately in its day/night variants. Its 120 generated assignments are calculated derivatives of the source recipe, not another 120 independently observed rules.

The scope includes the identified Robbins explanations and translator variants. It does not claim an independent translation of the facing Greek, an exhaustive Greek/Latin critical-apparatus collation, or a full audit of the historical introduction.

## Findings that materially change implementation

### 1. Matching aggregate totals can hide a different rule table

The adopted Egyptian table (I.20, PDF 121 / printed 97) and adopted Ptolemaic table (I.21, PDF 131 / printed 107) both sum to the same planetary allocations:

| Planet | Degrees across all twelve signs |
|---|---:|
| Saturn | 57 |
| Jupiter | 79 |
| Mars | 66 |
| Venus | 82 |
| Mercury | 76 |

Nevertheless, their term rulers differ over **153 of 360 degrees, or 42.5% of the zodiac's arc length**. This is an exact comparison of these transcribed tables, not an accuracy estimate or observed population rate. At continuous Aries 13 degrees, for example, the Egyptian table assigns Mercury and the Ptolemaic table Venus.

Ptolemy himself argues in I.20 that the same totals can survive different local allocations. Therefore an implementation test that checks only 30 degrees per sign and the global totals can pass while using the wrong table. The records bind the adopted edition-specific rows, preserve apparatus uncertainty, and test local boundaries as well as totals.

### 2. Chaldean terms require a group-level rotation

I.21 (PDF 123–125 / printed 99–101) rotates the rulers of four triplicity groups. Saturn and Mercury form one two-ruler group; Saturn comes first by day and Mercury by night. Rotating a flat five-planet list can split that pair and silently create the wrong system.

The source's lengths are 8, 7, 6, 5 and 4 degrees in order. The reconstructed day/night totals agree with the printed values: Saturn/Mercury exchange 78/66 degrees; Jupiter remains 72, Mars 69 and Venus 75. This is a definition check, not an endorsement of Chaldean predictions.

### 3. A described technique is not necessarily an endorsed technique

Ptolemy I.22 (PDF 133 / printed 109) describes 2.5-degree twelfth-parts and planetary degree assignments, then explicitly declines them as inadequately grounded.

Rhetorius chapter 18 (printed 17–18; OCR segments 20–21) instead calls dodecatemories necessary, discusses multiplication by 12 versus 13, and cites Ptolemy in favor of the 2.5-degree construction. Agreement about a mathematical description is not agreement about whether to use the technique.

Both positions are retained. Rhetorius's method remains available for his own future source profile; it is not smuggled into a supposedly unanimous Ptolemaic baseline, nor discarded simply because Ptolemy objects.

### 4. Shared labels can conceal different rules

**Triplicities.** Ptolemy I.18 retains Mars for Cancer/Scorpio/Pisces with Venus as co-ruler by day and Moon by night. Rhetorius chapter 9 uses day/night/third-common roles, with Venus/Mars/Moon for that triangle. These roles must not be flattened into an unlabeled list.

**Chariots.** Ptolemy I.23 requires two or more familiarities with the containing place. Rhetorius chapter 43 speaks of a planet in its own domicile, exaltation **or** terms and adds a qualification about remaining effective under the Sun's beams. These are different thresholds and different consequences.

**Proper face.** Ptolemy I.23 relates a planet to a luminary using the corresponding domicile relation and orientation; the Venus example is not just “any sextile.” It is not a generic synonym for a ten-degree decan. Robbins also reports a stricter scholiast interpretation requiring own domicile and a relation to both luminaries. Rhetorius uses face in more than one context as well. The extraction preserves the definitions rather than assigning one convenient universal meaning.

These are four targeted cross-source comparisons, not a claim that Rhetorius has received a full chapter audit.

### 5. Application, latitude and power remain conditional

I.24 distinguishes bodily conjunctions from configurations by aspect. Bodily passages require an additional same-side-of-the-ecliptic check; the author says this restriction is unnecessary for aspect rays. Robbins's further expression “same latitude” is not automatically equivalent to exact numerical equality. The fixture implements only the minimal same-side check and leaves zero latitude and equality tolerance unresolved.

The author's “interval not great” does not supply a single numeric orb. Robbins reports both planet-specific orbs attributed to Ashmand and a 15-degree maximum from the anonymous commentator. These are alternatives with separate attribution, not an author-supplied universal setting.

The closing power assessment combines phase/motion and horizon relations. It must not be reduced to retrograde versus direct motion alone or an imported whole-house strength table. The exact approach-to-midheaven interval and numerical weights remain unspecified.

## Verification and preservation

The new bounded definition suite contains **36 passing tests**. It checks the twelve domiciles, exaltation/depression oppositions, explicit triplicity roles, both term tables and their boundaries, the Chaldean grouped construction and totals, unknown/invalid inputs, the two-familiarity threshold, latitude-side handling, and source-record/non-adoption attribution. The integration result is recorded in `VERIFICATION.json`.

The earlier source records, fixed-star table, historical prediction freezes, fitted event models, numerology methods and production chart engine are not changed. No person-level prediction has been added or re-scored. Source reading, code-definition checks and empirical validation remain different stages.

## Resume point

Following the existing life-analysis reading plan, the next batch is **Book III.1–III.3**, starting at PDF 245 / printed 221: introduction to nativities, the horoscopic degree, and the subdivision of natal inquiry. It continues through the end of III.3 before III.4 on the shared PDF 265 / printed 241. Only the starting headings/boundaries were inspected in this turn; those chapters remain unread for audit-count purposes.

Book II's 13 mundane/general chapters remain explicitly indexed and deferred to their separate pass. They have not been silently omitted. The Ptolemy inventory stands at **24 read and 37 unread sections**. The wider corpus audit remains open under the owner's multi-pass authorization.
