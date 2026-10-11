# B02m changed-item readback

**Overall: the corrections hold, with trivial wording problems left (FINDS_ERROR, trivial only).**
- All eight minor defects are fixed and match the page images.
- The PDF306 negative is now kept word-for-word, and its meaning is explicitly left open.
- What remains:
  - six small wording defects in changed records, three of them created by the corrections themselves (R1680, R1682, R1684);
  - a few more dropped qualifiers the first review did not list;
  - two citation faults in the report around the new §5 paragraph.
- The "36 distinct tests" figure matches the test summary. I could not check that the tests actually ran: the test code, log and hashes are not in this directory.

Quotations from the print show long s as "s".

## 1. Verdicts on each corrected matter

### The eight minor defects and the uncertain negative

| Record | Page | Verdict | What the page image shows |
|---|---|---|---|
| R1656 | PDF303/p269 | AGREES | Statement and details now give the two printed steps: "convenient Medicines are to be applyed", then resist "the Diseases proceeding from influence of the Planets, by other Planets of contrary nature and power to the Planet afflicting". |
| R1662 | PDF304/p270 | AGREES | "either infirm OR sound" restores "nothing is either infirme or sound". "of the stars" for the print's "of these" (meaning the planets) is an acceptable gloss. |
| R1671 | PDF305–306 | AGREES | "or cooling" is gone from the statement. The remedies match the print: let blood until the fifth day, evacuate/purge, other remedies as nature requires. |
| R1672 | PDF306/p272 | AGREES (one wording residual, D7) | See the paragraph below. |
| R1677 | PDF307/p273 | AGREES | "stuffing in the head" matches "stuffing in the Head"; "without doubt" restored. |
| R1686 | PDF310/p276 | AGREES | "intended (intensified) fevers" matches "in-/tended Feavers"; "still complaining" restored. |
| R1690 | PDF312 (label 279) | AGREES | "choleric obstructions" matches "chollericke obstructions". |
| R1697 | PDF314/p280 | AGREES (small residual, D6) | The modest querent, the male querent and *in Contrario* are now separate. The querent context is added to the prerequisites, and "now necessary" is restored. |
| R1701 | PDF315–316 | AGREES | Dariot is replaced by "Hermes-headed material ends before the horizontal divider on PDF316". "Usually" and "or enquiring" restored. "Dariot" no longer appears anywhere in RULES.json. |

**R1672, the PDF306 negative.** In `evidence/PDF306_LINE3_ENLARGED.png`, line 3 reads "repugnant to ♄ as not calefactive, emollient, or mollifying" and continues "and dissolving obstructions." The first letter of "not" is short, with no ascender, unlike the "h" in "which", "the" and "those" on nearby lines. I read the same word on `pdf-306.png`. The crop's line breaks and blemishes match lines 1–10 of `pdf-306.png`, so it shows the same page. I can't confirm how it was produced: no hash or manifest entry for it is in this directory.

The record keeps the word and leaves its meaning open:
- `source_quote_exact` matches the print exactly, apart from normalizing long s and the ct ligature.
- The statement calls the sentence "semantically ambiguous".
- The exception forbids emending it to "hot" or inferring which way the remedy works.
- details[0] marks the reading as UNRESOLVED.
- U22 records both readings: a misprint for "hot", or a shorthand meaning "as [Saturn is] not calefactive".
- The page locator is now [306].

### The 17 trivial items, and the table words

| Record | Verdict | Note |
|---|---|---|
| R1663 | FINDS_ERROR (trivial, partly fixed) | "first" is removed, and the prerequisite and details now say the hour cannot be known precisely. The statement still says "cannot be obtained" (D1). |
| R1665, R1667 | AGREES | Locator [304]; both passages are wholly on PDF304. |
| R1670 | AGREES | "commonly" and "or molested" restored. |
| R1679 | AGREES | "'I ever find' the vitals much afflicted" restored. |
| R1680 | FINDS_ERROR (trivial) | "many times" is back but in the wrong place (D2). |
| R1682 | FINDS_ERROR (trivial; the fix introduced it) | The fix wrote "many-times recurrent suffering" (D3). The Virgo two-reading flag is now present (exception and U23). |
| R1684 | FINDS_ERROR (trivial) | "botch" and "too much abundance" restored, but "usually" is not reattached to its clause (D4). "no retention of Urine" is still correct. |
| R1685 | AGREES | "many times excessive pains-taking" restored; "for the most part" kept; U24 added. |
| R1687 | AGREES | Now "recoverable". |
| R1692 | AGREES | "a necessity there is of emission of blood" quoted; the added "hot" removed. |
| R1693 | AGREES | Now "looseness". |
| R1694 | AGREES | "probability of pleurisy" restored. One dropped word not on the first list (D8). |
| R1695 | AGREES | "Usually" restored. One spelling slip (D8). |
| R1696 | AGREES on the listed item; FINDS_ERROR (trivial) | "many times a disease all over the body" restored, but it still says "intense fevers" (D5). |
| R1698 | AGREES | "daily found" restored. Other dropped frequency words (D8). |
| R1700 | AGREES | Now gives causes, not symptoms, and "any favourable planet". |
| Cooling table | AGREES | "Pomegranet" and "Bull-rushes" match the print. "Patomagitum" and the separate "Purcel and" row match `pdf-306.png`. "Sumach" (print "Summach") and "Blackberry-Tree" (the errata form; the body prints "Blackbeery" with a handwritten caret) fall under the table's stated spelling normalization. |
| "Purcel and" note | AGREES | Italic "Purcel" next to roman "and" is visible on `pdf-306.png`. The new note was added as a second entry for the same word instead of being merged (`MATERIA_MEDICA_TABLES.json:122-141`). The two entries agree; it's just redundant. |

### Report and ledgers

| Item | Verdict |
|---|---|
| Report C21, the "as not calefactive" paragraph | AGREES with R1672 and U22. |
| Report C20/C21 citations | FINDS_ERROR (minor, reporting) (D9). |
| Report C22, the table words | AGREES. Its cited `evidence/pdf306-table-crop.png` is not in this directory, so I checked against `pdf-306.png` instead. |
| Report C10, C16, C18, C27 against the corrected records | AGREES. C10 matches the print; only R1663's statement lags. C18's "recoverable" matches R1687. C27 matches R1697's three separate conditions. |
| Report C28, 36 distinct tests | Count AGREES with `TEST_RUN_SUMMARY.json`. Whether the tests ran is UNCERTAIN (see below). |
| Report C29, the pixel match | UNCERTAIN; can't be checked here. It covers "fifteen retained PNG pages", which does not include the enlarged crop. |
| CLAIM_LEDGER.json | AGREES: blocks C01–C31 match the report word for word, checked by reading, including the misplaced citation. Hashes not checked. |
| RECONCILIATION.json | AGREES: 26 IDs (8 minor + 17 trivial + 1 uncertain), 52 records, and the reading "not calefactive". Its claim "printed wording repaired" goes too far (D2–D5, D8). Its `review_file` path `independent_review/OPUS_INITIAL_DIAGNOSIS.md` differs from this directory's `INITIAL_DIAGNOSIS.md`; that is only a packaging difference. |

## 2. Remaining defects

**D1. R1663 statement** (PDF304/p270, `RULES.json:672`)
- Print: "If the certaine hour of the parties first falling sick cannnot exquisitely be knowne".
- Record: "When the certain illness-onset hour cannot be obtained".
- The prerequisite and details were fixed. The statement keeps the stricter "not available" sense.
- Fix: "cannot be known precisely".

**D2. R1680 details[0]** (PDF308–309/p274–275, `RULES.json:1655`)
- Print: "their Pipes are narrow and obstructed, small Feavers, and many times feare of a Quo-|tidian Ague, but usually a Quartan Ague followes, holding a long time".
- Record: "narrow obstructed pipes, many times, small fevers, fear of quotidian but usually a long quartan ague".
- "Many times" now sits before "small fevers"; in the print it describes the fear of a quotidian ague.
- Fix: "…small fevers, and many times fear of a quotidian ague, but usually a quartan ague follows, holding a long time".

**D3. R1682 details[1]** (PDF309/p275, `RULES.json:1771`)
- Print: "many times I find the sick afflicted when the ☽ is in ♍ in aspect of ♄ with the Wind-chollick, with extreame Melancholly, with the Gout or aches in the Thighes and Feet, &c."
- Record: "wind-colic and many-times recurrent suffering, extreme melancholy, gout…"
- "Recurrent suffering" is not printed. "Many times" is how often the author finds these conditions, not a symptom.
- Fix: "Many times the author finds the sick … afflicted with wind-colic, extreme melancholy, gout or aches in thighs and feet."

**D4. R1684 details[0–1]** (PDF310/p276, `RULES.json:1889-1890`)
- Print: "the Disease is in Ano … usually an Ulcer there, or the Hemorroids or Piles, or some Exulceration or Bubo, [Anglice] a botch in the Privy-members."
- Record: details[0] has no "usually"; details[1] only says "with 'usually' elsewhere in the same row".
- Fix: "usually an ulcer there, or haemorrhoids/piles, or some exulceration or bubo ([in English] a botch)…", and delete the floating phrase in details[1].
- The urine negative is unaffected.

**D5. R1696 details[0]** (PDF313, label "29"/p279, `RULES.json:2588`)
- Print: "from that cause hath intended Feavers". Record: "intense fevers", while R1686 now says "intended (intensified)".
- The meaning is close, but the printed word is lost and the two records still differ.
- Fix: "intended (intensified) fevers".

**D6. R1697 details[0–1]** (PDF314/p280, `RULES.json:2645-2646`)
- Print: "Its neither better or worse with the party inquiring…"; "many times I find the party scabby…"; "if a Man propound, the Wife may be faulty, &c. in Contrario".
- Record: "if a MAN propounds the question he insinuates the WIFE may be at fault".
- Three remaining problems:
  - "he" can be read as the man asking the question, but the print states the judgment impersonally.
  - "with the party inquiring" appears nowhere in the record. That makes "In a separate question context" imply that the rest of the row isn't about a person inquiring.
  - "many times" before "scabby" is dropped.
- Fix: "if a man propounds, the text says the wife may be faulty"; restore "with the party inquiring" and "many times".

**D7. R1672 details[0] and U22 wording** (PDF306/p272, `RULES.json:1188`, `UNRESOLVED.json:111`)
- Record: the "not" is "hard to reconcile with the immediately adjacent assignment of heating medicines to Mars".
- That location is wrong. The sentence right after it assigns cooling medicines to ♄ ("Medicaments which naturally are concurring with ♄ … refrigerating or cooling…"). The Mars heating assignments are elsewhere:
  - PDF304: "To ♂ such as are calefactive, warme and impletive";
  - lower on PDF306: "Such Medicines as are naturally calefactive or hot, are assigned to the dominion of Mars and the Sunne".
- The tension exists only if "not calefactive…" describes the Mars medicines. Under U22's other reading ("as [♄ is] not calefactive") there is no conflict. So the sentence treats one reading as the problem.
- U22 says "authorial typo" while R1672 says "printing error"; nothing shows who made the error.
- Fix: replace the sentence with U22's two-reading wording, and say "misprint" without naming who made it.
- This does not settle the meaning, so R1672 stays AGREES.

**D8. Dropped qualifiers not on the first list, plus one spelling slip** (all trivial)
- R1694 (PDF313): "I evermore feare" became "particularly fears".
- R1695 (PDF313): the print reads "miseraicks" at page resolution; the record has "miseriacks" in both statement and details.
- R1698 (PDF314): "many times offended with the Hand and Foot-gout … sometimes with sore Throats" lost both frequency words.

**D9. Report §5 citations** (`AUDIT_REPORT.md:46,48`)
- The C20 paragraph on opposing remedies now ends with no citation. Its bracket "[PDF306–307,314; R1672, R1675, R1697; U15.]" sits after C21's own bracket.
- C21's citation for the "eight minor source-fidelity faults" leaves out R1701 (PDF315–316, the Dariot fault).
- Fix: move the U15 bracket back to line 46 and add R1701 / PDF315–316 to C21.
- CLAIM_LEDGER blocks C20 and C21 copy the same layout and need the same edit.

### The 36-test claim and its limits

- **Count:** `TEST_RUN_SUMMARY.json` lists 36 unique test IDs, matching the report's 20 + 8 + 8. Adding the 8 new tests to the 28 reported earlier gives 36.

  | Test class | Tests | Report's category |
  |---|---|---|
  | Catalogues | 10 | retained (20) |
  | RecordIntegrity | 10 | retained (20) |
  | RecoveryRegressions | 8 | earlier source-recovery regressions |
  | IndependentReviewRegressions | 8 | independent-review regressions |

- **Result:** the summary reports 36 run, 0 failures, 0 errors, 0 skipped.
- **Limits:** the report's "do not certify historical meaning, treatment efficacy or predictive performance" matches the summary's scope string.
- **Can't be checked from this directory:**
  - the cited files `test_lilly_hermes.py`, `TEST_RUN.log` and `PACKET_USABILITY.json` are absent;
  - the "subject to the final extraction run" condition;
  - the extracted-archive rerun;
  - `log_sha256` and the per-file hashes;
  - whether the run used the `RULES.json` I read.
- **For the adjudicator (not a new requirement):** going by their names, the eight new tests check the producer's JSON, not the page images. Defects D1–D8 would therefore pass the suite. That is consistent with the report's disclaimer.

## 3. Are the initial eight and the negative resolved?

- **The eight minor defects: resolved.** Each fix matches the page (R1656, R1662, R1671, R1677, R1686, R1690, R1697, R1701). The leftovers attached to two of them (R1696's wording, D5; R1697's pronoun and framing, D6) are trivial and don't reopen the original faults.
- **The negative: resolved.**
  - The print says "not", on both the enlarged crop and the standard page image.
  - R1672 keeps it word-for-word, flags it in its statement, exceptions and details, and points to U22, which records both readings.
  - Report C21 agrees.
  - Nothing emends it to "hot" or derives which way the remedy works.
  - R1684's "no retention of Urine" is still correct.

## 4. What I actually read

- **Read in full:** `RECONCILIATION.json`, `INITIAL_DIAGNOSIS.md`, `AUDIT_REPORT.md`, `CLAIM_LEDGER.json` (C01–C31), `TEST_RUN_SUMMARY.json`, `MATERIA_MEDICA_TABLES.json`, `UNRESOLVED.json` (U01–U24), and all 2,948 lines of `RULES.json`.
  - I checked only the 26 changed records against the images. The 26 unchanged records were read as text but not re-checked.
- **Images, each viewed once:** `evidence/PDF306_LINE3_ENLARGED.png` and `evidence/pdf-303.png` through `pdf-316.png` (14 pages).
- **Not viewed:** `pdf-302.png` (no changed record on it) and `errata-888.png` (no correction depends on it).
- **Tried but not present:**
  - `evidence/pdf306-table-crop.png`, `evidence/pdf306-line3-crop.png`
  - `test_lilly_hermes.py`, `TEST_RUN.log`, `run_verification.py`
  - `SOURCE_IMAGE_MANIFEST.json`, `PACKET_USABILITY.json`, `TEXTUAL_CHECKS.json`
  - `COUNTS.json`, `SOURCE_REVIEW_STATUS.json`, `README.md`
- **Not attempted:** `SECTION_COVERAGE.json`, `REFERENCE_TABLES.json`, `SOURCE_IDENTITY.json`, `CONTINUE_HANDOFF.md`, `recovery/*`.
- **Not done:**
  - no directory listing, so other files may exist unseen;
  - no hashes computed, no tests run, no PDF opened;
  - no files written and no provider changes;
  - no reread of the prior corpus.