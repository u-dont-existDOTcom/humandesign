# B02m independent check: Lilly 1647, Hermes section (PDF302 below the divider to PDF316 above it)

## 1. Diagnosis

**FINDS_ERROR. The errors are minor and localized.** I found 8 minor fidelity defects and a cluster of trivial ones. None changes a rule's polarity, prerequisites, exceptions, timing quantifiers, prognosis attribution, coverage or counts.

- **AGREES on:**
  - **Coverage:** every admitted paragraph, all 24 sign rows, all 74 list entries and the 7 sensory lines map to the 52 records, each record assigned once.
  - **Counts:** `kind_counts` sum to 52; 1,650 + 52 = 1,702; 1,702 + 1,066 = 2,768.
  - **R1684:** retains "no retention of Urine" (PDF310).
  - **Timing table:** all six rows are correct.
  - **Errata claim:** checked against `evidence/errata-888.png`. The only entries for printed 268–282 are p272 l26 "Blackberry", p274 l5 "Præcordiacks" and p277 l7 "for your r the".
  - **Page labels:** PDF312 visibly prints 279 and PDF313 prints "29", as recorded.
  - **U15:** the opposed remedy recommendations are retained.
  - **CLAIM_LEDGER:** its 30 blocks reproduce the whole report verbatim (compared by reading, not by hash).
  - **No validation claims:** no clinical or predictive validation is claimed anywhere.
- **UNCERTAIN, one possible polarity issue:** PDF306 line 3 probably prints "as **not** calefactive". R1672 records the sentence without a negative and without a flag (see §4).
- **UNVERIFIED inside the boundary:** the draft-history statements, the extracted-archive rerun, the raster pixel-match, and every SHA-256 value.

## 2. What I read, and what I did not

- **Page images:** `evidence/pdf-302.png` to `pdf-316.png`, all 15, every line. I viewed 304, 306, 307, 310, 311 and 312 twice.
- **Supplementary images:** `evidence/pdf306-table-crop.png` and `evidence/errata-888.png`. The errata file is not listed in any manifest and not cited by path in the report. I found it by trying file names.
- **Records:** `RULES.json` in full (lines 1–2951, R1651–R1702, every field).
- **Report and support files:** `AUDIT_REPORT.md`, `CLAIM_LEDGER.json`, `SECTION_COVERAGE.json`, `TEXTUAL_CHECKS.json`, `UNRESOLVED.json` (U01–U21), `REFERENCE_TABLES.json`, `MATERIA_MEDICA_TABLES.json`, `COUNTS.json`, `SOURCE_IMAGE_MANIFEST.json`, `SOURCE_IDENTITY.json`, `SOURCE_REVIEW_STATUS.json`, `CONTINUE_HANDOFF.md`.
- **Test evidence:** `TEST_RUN_SUMMARY.json`, `TEST_RUN.log`, `test_lilly_hermes.py`, `run_verification.py`.
- **Absent from the boundary:** `PACKET_USABILITY.json`, `recovery/RASTER_PROVENANCE_CHECK.json`, `recovery/ROOT_REPAIR_LEDGER.json`, `recovery/ORIGINAL_DRAFT_MANIFEST.json`, `recovery/original_draft/RULES.json`.
- **Not done:** no hashes were recomputed (no shell), no tests were executed, and the canonical PDF was not opened. I could not list directories, so other files inside the boundary may exist unseen.

## 3. Demonstrated defects

**Minor (a clause's meaning is changed):**

1. **R1662 `source_details[1]`** (PDF304/p270, "To him therefore…")
   - Printed: "without the congresse and influence of these in humane and worldly affaires, nothing is either infirme or sound."
   - Record: "no worldly affair is firm without these influences."
   - The infirm/sound pair (sickness and health) is lost.
   - Fix: "…nothing in human and worldly affairs is either infirm or sound."
2. **R1677 `source_details[0]`** (PDF307/p273, Aries row line 2)
   - Printed: "ſtuffing in the Head". Record: "snuffing in the head".
   - Fix: "stuffing".
3. **R1686 `source_details[0]`** (PDF310/p276, Capricorn row)
   - Printed: "in-/tended Feavers". Record: "inward fever".
   - R1696 glosses the same word on PDF313 as "intense fevers", so the two records are inconsistent.
   - Fix: "intended (intensified) fevers".
4. **R1690 `source_details[2]`** (PDF312, label 279/sequence 278)
   - Printed: "occasioned by chollericke obstructions". Record: "from colic obstruction".
   - This turns a humoral cause (choler) into a symptom (colic).
   - Fix: "choleric obstructions".
5. **R1671 `source_statement`** (PDF305–306)
   - The printed remedies are: "let Blood untill the fifth day, or prescribe such Medicines as evacuate and Purge … and to administer such other Remedies as the necessity of nature further requires."
   - The statement adds "or cooling", which this passage does not contain. The details are correct.
   - Fix: delete "or cooling". The cooling rule for Solar/Martial diseases is R1675 on PDF307.
6. **R1656 `source_statement` and `source_details`** (PDF303/p269)
   - Printed: "convenient Medicines are to be applyed, and we must resist the Diseases proceeding from influence of the Planets, by other Planets of contrary nature and power to the Planet afflicting."
   - The statement makes the *medicines* contrary to the planet; the details make the *planet* (not the diseases) the thing resisted.
   - Fix: restate it as two steps: apply convenient medicines; resist the diseases arising from planetary influence by other planets contrary in nature and power to the afflicting planet.
7. **R1697 `source_details[1]` and prerequisites** (PDF314/p280)
   - Printed: "Let a modest party propound the Question; there's cause to distrust foule play, &c. if a Man propound, the Wife may be faulty, &c. in Contrario." The row opens "with the party inquiring".
   - Record: "foul play or spouse fault when a modest person asks". This attaches spouse fault to the wrong condition and drops the sex-specific condition and its reversal. The prerequisites give only illness onset, omitting the enquiry context.
   - Fix: separate the three conditions (modest querent; male querent; the converse) and add the enquiry context.
8. **R1701 `exceptions_and_modifiers[2]`**
   - Record: "Dariot/Hermes material ends before the horizontal divider".
   - No admitted page (PDF302–316) names Dariot; the only heading is "Hermes Trismegistus upon the first Decumbiture of the Sick".
   - Fix: say "Hermes-headed material", or mark Dariot as an external, unverified attribution.

**Trivial:**

| Item | Evidence | Correction |
|---|---|---|
| Cooling list spellings | Print reads "Pomegranet." and "Bull-rushes." (crop). The table has "Pomegranete" and "Bul-rushes", which are neither print nor a declared normalization. ("Sumach" is an acceptable normalization.) | Restore the print spellings |
| Locators R1665, R1667, R1672 | R1665 and R1667 sit wholly on PDF304 (PDF305 opens with R1668). R1672 sits wholly on PDF306; it reaches PDF307 only by cross-reference. | Use [304], [304], [306] |
| R1663 statement and prerequisite | Print: "when judgment is required of the Physitian"; "cannnot exquisitely be knowne". The record adds "first asked", and its "unavailable" is stricter than "not known precisely". | Drop "first"; say "cannot be known precisely" |
| Dropped or softened qualifiers | R1670 "commonly", and "or molested" became "and"; R1677 "without doubt…will dye"; R1679 "I ever find…much"; R1680 and R1682 "many times"; R1684 "usually", "botch" became "blotch", "too much aboundance"; R1685 "many times" became "sometimes"; R1686 "still"; R1692 "a necessity there is" became "advocated" (and "hot" was added to the first-person blood list); R1694 "probability" became "possible"; R1695 "Usually"; R1696 "many times…all over the Body"; R1697 "now necessary" became "recommends"; R1698 "daily"; R1701 "Usually" and "or enquiring" | Restore the printed wording |
| Statements drifting from correct details | R1687 "said to improve" (print: "is recoverable"); R1700 "violent symptoms" (print gives these as *causes*) and "a benefic" (print: "any favourable Planet"); R1693 "diarrhoea" (print: "loosenesse") | Align each statement with its details |

## 4. Uncertain reading and unresolved interpretations (not defects)

- **PDF306/p272, line 3 (the uncertain item):** "…are repugnant to ♄ as [not | hot] calefactive, emollient, or mollifying and dissolving obstructions."
  - At the supplied resolution the word reads "not" to me. It shows no ascender, unlike "hot" in "calefactive or hot" further down the same page.
  - If confirmed, R1672 silently repairs a printed negative, the same failure class as the Scorpio correction. `TEXTUAL_CHECKS` disclaims "semantic repair by doctrine".
  - Required: an enlarged crop of that line. If it reads "not", keep it as printed and add an UNRESOLVED entry with both parses: a misprint for "hot", or "as [Saturn is] not calefactive". If it reads "hot", no change is needed.
- **U15** (PDF306 cooling vs PDF307 heating for Saturn/Mercury): correctly preserved.
- **"Purcel and":** in the crop, "Purcel" is italic and "and" is roman, which points to a connective. The reading is still honestly unresolved, but the lexical note omits this evidence, and the regression test hard-codes the split reading.
- **PDF309, Saturn/Virgo "things which mollifie heat and dissolve":** R1682 reads three verbs (mollify, heat, dissolve), which fits PDF307. The other parse, "mollify [temper] heat", would reverse the remedy direction. This choice is not flagged.
- **PDF310, Saturn/Sagittarius "what mitigates heat gently":** another local departure from the PDF307 heating rule, retained in R1685. Report §5 does not claim to be exhaustive.
- **PDF311 transition** ("or indeed by ☿"; "from ♂ or the ☉") against margins that name only ♄/♂: whether the rows apply to Mercury or Sun afflictions is unresolved. R1689 handles this correctly.
- **PDF314 "or know properly that day":** normalized as "or more properly" in R1698 and in timing-table row 5. The sense is preserved.
- **Errata "p 277 l 7":** the handwritten "the" sits on body line 6, under the line count that makes the l26 and l5 entries match. The errata's own count is off by one, but the target word is unambiguous and C23 reports the errata faithfully.
- **Honest uncertainties, correctly left open:** R1667 pronoun scope, "number" (R1669), "califie" (R1688), "Patomagitum", "Pirapirastra", and the twenty-day chronology (U20).

## 5. Verdicts

**Records:**
- **PASS, no change (26):** R1651–R1655, R1657–R1661, R1664, R1666, R1668, R1669, R1673–R1676, R1678, R1681, R1683, R1688, R1689, R1691, R1699, R1702.
- **PASS with trivial fixes (17):** R1663, R1665, R1667, R1670, R1679, R1680, R1682, R1684 (polarity correct), R1685, R1687, R1692, R1693, R1694, R1695, R1696, R1698, R1700.
- **Minor defect (8):** R1656, R1662, R1671, R1677, R1686, R1690, R1697, R1701.
- **UNCERTAIN (1):** R1672.

**Claim blocks:**
- **PASS (25):** C01–C05, C07, C09–C20, C22–C26, C29, C30.
  - C16: all six timing rows match the pages.
  - C23: verified against the errata image.
  - C20: correct, but it does not cover the PDF306 line-3 question.
- **PARTIAL (4):**
  - C08: the source sentence is verified; the draft-history sentence is not.
  - C21: "Purcel and", "Patomagitum" and white lead are verified; the draft's "Petonagium" is not; the spelling slips above are not mentioned.
  - C27: 28 tests with 0 failures is confirmed by the summary and log, and the code description is accurate; the extracted-archive rerun is unverified.
  - C28: the pixel-match is unverified (accepted only as your stated premise); the receipts sentence passes and is consistent with `SOURCE_REVIEW_STATUS`.
- **UNVERIFIED (1):** C06.

## 6. Coverage, weakest step, limitations

- **Tests:** all 28 are structural or substring checks on the producer's own JSON, plus PNG-against-manifest hashing. None compares anything to page content. Some names overstate what they check:
  - `test_source_hash_equals_replayed_manifest` compares stored strings and never hashes the PDF.
  - `test_speed_states_are_not_silently_equated` passes on a "DECREASING" in R1700 that refers to light, not motion.
  - `test_unresolved_ambiguous_authorship` only checks that the unresolved count is at least 12.
  - None would catch the defects above or the line-3 question.
  - Reading the files, 27 of the 28 assertions hold; the image-hash test needs hashing.
- **Weakest step:** reading single 1647 glyphs from roughly 1331×1800 renders. Only the table and the errata page have larger crops. PDF306 line 3 is the decisive case.
- **Limitations:** no hashes recomputed (`report_sha256`, the per-block hashes, PNG, PDF and log hashes); possible unseen files because I could not list directories; draft and provenance claims rest on files outside the boundary. Publication, independent-review completion and owner delivery are not asserted here. Chapter XLIV and the parent audit remain open.