## Verdict: **FINDS_ERROR** (narrow; every fix is a text edit)

The repairs for the six original SOURCE_ERRORs (#4, 5, 13, 18, 33, 43) and the five UNRESOLVED items (#8, 12, 20, 23, 34) match the page images. The handling of the #33 erratum meets your requirement. Four defects remain:

1. **#9 and U26** state the #8/#9 overlap as settled fact.
2. **#37** still has, in its prerequisites field, the inference the first review flagged.
3. **Report C10** misstates #13's reception condition.
4. **Report C09/C08** name the wrong person as the one consenting, and overstate #6/#7.

There are also mislabelled qualifier layers and some wording drift. No record reverses the source's polarity, and I found no fabricated quotation.

## Scope actually read
- **Images:** `images/pdf-316.png` through `pdf-320.png` at display resolution, and `images/errata-888.png`, which was shown downscaled from 2217×3000 to 1478×2000. I transcribed all five aphorism pages from the images.
- **Files:** everything listed in `MANIFEST.json`:
  - `RULES.json` in full (3,177 lines; all 43 records; every field)
  - `AUDIT_REPORT.md` and `CLAIM_LEDGER.json`
  - `APHORISM_INDEX.json`, `SECTION_COVERAGE.json`, `UNRESOLVED.json`, `ERRATA_COLLATION.json`
  - `SOURCE_IDENTITY.json`, `TEST_RUN_SUMMARY.json`, `INITIAL_DIAGNOSIS.md`, `REQUEST.md`
- **Depth:** I checked the 25 flagged aphorisms field by field. I compared the other 18 at statement level, and wherever the report cites them.
- **Not in the packet:** `COUNTS.json`, `SOURCE_IMAGE_MANIFEST.json`, `SOURCES.md`, the test code and log, and PDF321–322.
- I used Read only. I edited and ran nothing.

## Requested checks

- **Count and boundary ✓**
  - There are 43 units. #1 has no printed number (it opens with a large initial "IN"); numbers 2–43 are printed in order, with no gaps or duplicates.
  - The section starts on PDF316, below the rule after "…danger of a Dropsie." It ends on PDF320, above the rule before "CHAP. XLV."
  - #9, #30 and #42 cross pages. The "20 If" at the foot of PDF317 is a catchword.
  - All 43 page fields, the IDs R1703–R1745, `APHORISM_INDEX` and `SECTION_COVERAGE` agree.
- **#33 (PDF319, p.285) ✓**
  - Print line 11 reads "…and both times there happens to be". The errata page reads "p 285 l 4 r her, l 11 r therein". Both verified on the images.
  - The original body text is kept separate from the erratum in three places: the witness fragment, `witness_variants.1647_body`, and a bracket in the statement.
  - The record requires an infortune "therein" at both the natal time and the start of the sickness.
  - Its exception requires a Fortune to "cast thither" its rays "at one of those times".
- **#4 vs #30:** both are kept and not harmonised (U19, both records, C07). One overstatement remains in #30 (below).
- **#8 vs #9 ✗:** the #9 statement and report C09 hedge correctly, but #9's exception and U26 state the overlap as fact (below).
- **#12 ✓:** the print's "they" is kept, both the either and both readings are recorded, and "no safety" is restored. U21 stays neutral.
- **#20 ✓:** the target of "under the earth" stays ambiguous, "must needs" is quoted, and the uncertainty flag is true.
- **#23 ✓:**
  - Whether the "if" covers only death or also prolonging stays unresolved.
  - Erratum 284/14 is recorded as EXACT_TARGET_NOT_CERTAIN, and the body text is not altered.
  - Print line 14 already begins with "if"; "of a benevolent" is the only other candidate target.
- **#34 ✓:**
  - The printed "and" between the two conditions is kept, and the clash is noted.
  - The geometry is correct as the record qualifies it ("Literal 180-degree").
  - Optional addition (my own geometric inference, not packet evidence): if "opposite" means the opposite sign, then under quadrant houses that sign can also fall in natal 6th or 8th. Only the 4th and 12th clash outright.
- **#43 ✓:** "beware in the beginning of a sicknesse" is restored. Whether the Mars factors are joint or separate stays open, and the Saturn converse is not spelled out. One problem with prerequisite scope remains (below).
- **Witness fragments ✓:** I checked all 27 fragments, across 24 records, against the images. All match apart from the declared normalisation (long-s, ligatures, joined line-end hyphens). None is fabricated.
- **Quotes inside source statements ✓:** all verified. Three normalisation notes:
  - #30's "difficulty removeable" is the corrected reading; the body prints a mark there.
  - #31 writes "Moon" inside quotation marks where the print has ☽.
  - #43 capitalises "Beware".
- **Locators ✓:** all page and anchor fields are correct, including the fixed anchors for #15 ("in his Fall") and #41 ("Occidentall").

## Remaining record issues

| # | Page | Issue | Minimal repair |
|---|---|---|---|
| **9** | PDF316–317 / 282–283 | The exception at `RULES.json:609` (repeated at `:659`) says the urine-without-consent case "remains a genuine source overlap" and that the closing phrase "supports a consent-only alternative". That settles the "no Urine or consent" question in favour of "either one absent", which is the reading that creates the conflict. In ordinary usage "no A or B" means neither (general knowledge, not from the packet); on that reading there is no overlap. The record's own statement (`:600`) says "may overlap", so the record contradicts itself. | Replace with: "If 'no Urine or consent' means either is absent, urine-without-consent falls under both #8 (ascendant = sick party) and #9 (ascendant = querent). If it means neither, they do not overlap. Unresolved." Add a matching pointer in #8. |
| **37** | PDF319 / 285 | The prerequisite at `:2686` still reads "Author's general rationale following a Sun-based prognosis." That is the inference the first review flagged. It sits in the conditions field and contradicts the record's own statement and exception. | "No printed condition; separately numbered descriptive statement about the Sun." |
| **30** | PDF318–319 / 284–285 | `:2119` says #30 "differs from aphorism4's moveable ending and common varying rule". Only the movable signs conflict. Fixed signs agree ("prolong" vs "long and permanent"). #30's common-sign descriptions ("recidivation", "now here, now there", "much better at one time then at another") fit #4's "vary". Also, #4 ties the sign classes, after a colon, to the fourth house; #30 names no house or significator. The conflict holds only if both refer to the same sign. | "Conflicts with #4 on movable signs only (quick end vs easy variation). Fixed signs agree; common signs are broadly compatible. #4 is in a fourth-house context; #30 names no house or significator." |
| **43** | PDF320 / 286 | Prerequisite 1 (`:3114`) makes "At beginning of a sickness" a condition of the whole aphorism. The print ties it only to the "beware" clause; the Moon's phase statement and the Mars clause are general. The exception at `:3121`, "…beware clause at sickness onset is required" (labelled EDITORIAL), reinforces the misreading. | Split it: "General: the Moon is more afflicted by ♂ when waxing and more oppressed by ♄ when waning. At onset only: 'beware in the beginning of a sicknesse when the ☽ is thus unfortunated'." Reword the exception as a recording instruction ("must be recorded"). |
| **33** | PDF319 / 285 | `:2369` reads "the text manifests death". In the print, "it" (the configuration) does. | Use: "…it 'doth manifest death' UNLESS…" |
| **3** | PDF316 / 282 | The record flags the missing verb in the tenth-house clause but no longer says what condition makes "his Physick … improper". | Add: "[predicate missing in print; most naturally 'be unfortunate', carried from the parallel seventh-house clause]". |
| all | — | Every `source_attribution` (e.g. `:39`) says "printed chapter XLIV". The new scope note (`:72`) says the chapter number is not printed on these leaves. | Change to "chapter XLIV (inferred from adjoining context)". |
| 1 | PDF316 / 282 | Nothing records that #1 has no printed number. | Add a one-line witness note. |

**Trivial wording:**
- #8: "represents" should be the print's directive "let the ascendant represent".
- #9: the print says "presents", not "represents"; "master" is a gloss on "A man".
- #20, fourth prerequisite: "makes it must needs be sooner" is garbled grammar.
- #23 (`:1626`): "A benevolent fourth lord expects the contrary"; in the print it is the reader who is told to expect the contrary.
- #40: "is followed by the allegation" hides the print's conditional ("being unfortunate…, the Patient will…").
- #43: "unfortunate" should be "unfortunated".

## AUDIT_REPORT claims failing

- **C10 (`AUDIT_REPORT.md:19`), material:**
  - The report says "favourable aspects of malefics **with or without reception**". The print (#13, PDF317) says such an aspect does not profit "unlesse that aspect be with Reception". Fix: "…favourable aspects of malefics, which do not profit unless with reception."
  - Also minor: in #20, reception changes ease ("the more easily"), not timing; only the above-Earth clause changes timing.
  - Also minor: #13 is filed under the heading "Lunar conditions" but is not lunar.
- **C09 (`:17`):** the report says "regardless of the **questioner's** consent".
  - #8's print reads "whether the Querent come with consent or no", and #9 calls it "consent of the sick party". The consent belongs to the sick party.
  - Fix: "whether or not the querent comes with the sick party's consent". Also cite U26.
- **C08 (`:15`):**
  - "The source distinguishes first visit from first entering upon a cure" restates the very inference that #6's record now disclaims. Fix: "uses different wording ('first visits' in #5 and #7; 'first enters upon a cure' in #6) without saying whether these are different events."
  - "esteem and payment even when cure fails" extends #7's proviso, which the print limits ("I meane, in point of estimation"). Fix: "good words, esteem and payment; if the cure fails, no prejudice 'in point of estimation'."
- **C07 (`:13`):** the sentence about #30 is cited only to "[PDF316; aphorisms1–4]". Add PDF318–319, R1732 and U19.
- **C15 (`:33`):**
  - "falling/detriment (#26)" should be "fall or detriment"; "falling" can be read as cadent.
  - "stationary and separately combust (#25)" conflicts with the record, which treats combustion as an added condition ("but if he be combust"). Align the two.
- **C18 (`:39`):** the report says the source "asks that the patient's nativity be obtained". The print is conditional: "If the Nativity … may be obtained". Also add U24 and U18 to the citations.
- **C19 (`:41`):**
  - "poetic rationale (#37)" brings back the link to #36 that the record disclaims. Use "solar description".
  - "recovery exception (#38)" upgrades the print's "Fear not the death". Use "'fear not the death' exception".
- **Unverifiable from this packet:**
  - C05 says "43 numbered" (#1 is unnumbered).
  - The figures 1,702, 1,745 and 2,811 rely on `COUNTS.json`, which is not here.
  - C22 says "five PNGs", leaving out the errata image; `SOURCES.md` is not here either.
  - C25's "death on 14 August" cites PDF321–322, which are not in the packet. The May 1645 date is visible on PDF320.
  - The title asserts "Chapter XLIV" without the scope qualifier the records carry.

## Editorial cautions vs printed conditions

The risk that an editorial caution gets read as a printed astrological condition is **low**. Every editorial caution is phrased as a disclaimer about validity ("No verified…", "not diagnosis"), never as a chart condition.

**The real risks:**

1. **The layer labels are swapped in both directions, so filtering by layer gives wrong results.**
   - Editorial cautions labelled SOURCE_CONTEXT_OR_INTERPRETIVE_NOTE:
     - flagged records: #5 (`:350`), #8 (`:559`, and the second half of `:564`), #10 (`:730`), #12 (`:871`), #18 (`:1309`), #26 (`:1881`), #30 (`:2177`), #34 (`:2517`), #40 (`:2931`)
     - unflagged records: #2, #24, #38, #39
   - Printed or errata content labelled EDITORIAL_EVIDENCE_LIMIT: #31's erratum note (`:2267`), #43's beware-clause note (`:3167`), #13's reception attachment (`:948`), and #41's "&c." note (`:3009`). A consumer that drops EDITORIAL layers would lose #31's erratum and #43's onset clause.
2. **No label certifies that a clause is printed.** SOURCE_CONTEXT_OR_INTERPRETIVE_NOTE covers both printed exceptions (such as #33's "thither") and glosses.
3. **Non-printed material in condition fields** occurs only in #37's prerequisite, #43's first prerequisite, and #9's "consent-only alternative".
4. **The per-layer note is boilerplate.** Every layer carries the same note ("Check source image for operative grammar…"), so it is not evidence that each item was checked.

**Minimal repair:** relabel the entries listed above, and fix the #37 and #43 prerequisites.

## The 26 retained uncertainty entries

Twenty-four are neutral. None of U19 (#4/#30), U21 (#12), U22 (#20), U23 (#23), U24 (#34) or U25 (#43) settles its question. Two need repair:

- **U26 (`UNRESOLVED.json:132`) settles the question falsely.** It says "Aphorisms8–9 both address urine-without-consent", which presupposes the conflicting reading, and then says the scope is unresolved. Repair it the same way as #9.
- **U10 (`:52`) is out of date for #33.**
  - It leaves out "therein" and "thither", so its "benefic beams at one of the times" is broader than the print.
  - It calls "both times" a "natal/decumbiture ambiguity". The record treats the two times as natal and sickness onset, and #33 says "beginning of a sicknesse", not decumbiture.
  - Repair: restate it with "therein" and "thither", and cite U18.

## Errata, index and test metadata

- **Errata tokens verified on the image:** "p 284 l 14 r if; l 37 dele semi-colon, p 285 l 4 r her, l 11 r therein". There are no entries for pages 282, 283 or 286; the list jumps from 277 to 284 and from 285 to 291.
- **Line mapping:** counting lines without the running head lands each entry on a plausible target:
  - 318, l.14: #23
  - 318, l.37: #30, "difficulty[mark] re-"
  - 319, l.4: #31, a blotted word before "her"
  - 319, l.11: #33, "there"
- **`ERRATA_COLLATION.json` inconsistencies:**
  - Entries 284/37 and 285/4 say `applied_to_normalized_record: false` (`:21`, `:30`). But #30 quotes the corrected "difficulty removeable" and #31 uses "HER". Either set the flags to true or quote the body text.
  - "CONFIRMED" for 285/11 (`:36`) is a strong inference, since the errata name no target word. The method line (`:44`) still calls the line counting uncertain, and report C21 has the same tension. Harmonise the wording.
  - The source path (`:2`) reads "evidence/errata-888.png and targeted crop". This packet has `images/errata-888.png` and no crop.
- **`APHORISM_INDEX`:** `textual_uncertainty` matches `original_source_wording_uncertain` in all 43 records. The errata flags are set on #23, 30, 31 and 33 only ✓.
- **`TEST_RUN_SUMMARY`:**
  - It is a self-reported JSON. No code, log or `run_verification.py` is in the packet, and I can't check its hashes with Read. I treat it as structural evidence only.
  - It lists `test_18_retained_uncertainties` (`:19`) as passing, while `UNRESOLVED.json` has 26 entries. The name may be stale, or the test may check for at least 18; I can't tell which.
  - The suite passed despite the C10, C09, #9 and #37 defects, which shows its semantic limits.

## Source-reading provenance limits

- **One copy, read at display resolution:** the errata page was downscaled.
- **Glyphs I couldn't resolve:**
  - the mark at 318, line 37
  - the blot before "her" at 319, line 4
  - the superscript mark between "there" and "happens" at 319, line 11. This may be a reader's caret, consistent with "in" being added by hand; I can't confirm it.
  - "ones" in #4 (partly damaged)
  - the blurred "282" page number
- **Errata targets are inferred:** the errata give only page, line and replacement word.
- **Not verified with Read only:** that the PNGs render the hashed PDF, that `errata-888` comes from the same copy, or that it is PDF page 888.
- **Word senses** ("no A or B", "sometimes", "doubtfull") come from general knowledge, not from the packet.
- **Handwriting:** a later handwritten "6th House" sits beside printed pages 283 and 285. It is not the author's text and is still not recorded anywhere (harmless).
- I make no claim of clinical efficacy or predictive validity, and I have added no patient outcomes.