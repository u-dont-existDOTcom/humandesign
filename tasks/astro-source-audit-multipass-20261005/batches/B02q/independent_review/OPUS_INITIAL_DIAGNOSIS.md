# Source review: Lilly 1647, Chapter XLVII (B02q), records R1794–R1851

**Verdict: FINDS_ERROR.** I found 13 issues: 1 high, 4 medium and 8 low. The worst is R1806, which credits the chapter (and classes as ancient authority) an objection the page attributes to unnamed "some", and drops the "(except pestilentiall diseases)" exception. Most of the requested checks pass, including the onset/urine/doctor hierarchy, the worked-example values, the hypothetical July 1645 status and the 7/14/21 argument.

I read all eight images before opening any candidate file. Quotations are from the images, with the long s written as s. The research and therapy tools that were connected are out of scope here, so I didn't use them.

## 1. Chapter outline built from the images

**Boundaries:** the chapter starts below the rule on PDF324 (printed p. 290) with "CHAP. XLVII. Of the CRYSIS in Diseases." It ends on PDF330 (p. 296) with "Master BOOKER having promised to undertake that labour, I forbeare." That line sits above the rule that comes before Chap. XLVIII.

1. **Definitions (PDF324–325).** A crisis is a "duell or contention betwixt nature and the infirmity": good if nature overcomes, "pernicious and ill" if the sickness prevails. "Or" it is a sudden alteration of the body tending to health or further sickness. Critical, decretory and chrysmall days "are all one".
2. **Starting-moment hierarchy (PDF325).** First choice is the moment of onset ("best of all"). Next is the hour the Water is first brought to the Doctor ("but not so certainly"). If no Urine comes, use the time the Doctor first speaks with the sick party and is asked for an opinion and a course of cure.
3. **Authorities (PDF325).** Galen: a sudden, vehement motion, "or… not a locall motion altogether". Unattributed: crisis "imports judgment". Hippocrates: "an acute or swift reportation… to recovery or death". Then a "say some" objection containing "(except pestilentiall diseases)". Then Avicenna, in Canticis, "agrees with Galen, and saith" a Latin definition.
4. **Causation dispute (PDF325–326).** "Some" say crises come from inferior causes. Then fevers would each need their own day-reckoning, which "as many learned say, cannot be". The lunar view is "more generally received and concluded". The radix is the Moon's place at falling sick, or rectified to the hour the patient first asks advice.
5. **Phases (PDF326).** Indicative day; semi-quadrate ("halfe Crysis"); true □; ☍ ("full Crysis").
6. **Worked example (PDF326–327).** The Moon in "the later Figure of the 16th of July 1645" is "supposed" to mark the beginning of a disease. 15°42′ ♍ becomes 16 ♍ "in the eighth column". Then: 8°30′ ♎ (first Indicative day), 1 ♏ (semi-quadrate, "as it were, halfe a Crysis"), 23°30′ ♏ (second Indicative day), 16 ♐ (true Crysis). The reader is to continue along the row, and also watch the Moon's transits of the 6th, 7th and 8th house cusps.
7. **Table (PDF328, p. 294).** "The Table followeth.", 30 rows × 16 columns.
8. **Critical-day judgments (PDF329).** A benefic is "very probable (if the party be ordained for life)". An infortune gives "little hopes at present; the Crysis is then ill". The 7th/14th/21st days are former practice, replaced by calculating the Moon's true motion as given in "my Introduction".
9. **Medicine scheme (PDF329).** Four sign groups, each strengthening a virtue in a temperament. Moon in ♋♏♓, in ✶ or △ to ♃ / ♀ / ♂☉, purges melancholy / choler / phlegm. ♄ stirs up the retentive virtue. Six faculties are paired with ♃ ♂ ☉ ♀ ☿ ☽. Four elemental humours, including "Atram Melancholiam".
10. **Close (PDF329–330).** Lilly defers to Booker.

## 2. Findings

**F1 (HIGH): R1806 and UNRESOLVED U04 misattribute the Hippocrates objection and lose its exception.**
- **Source, PDF325 (p. 291):** "But, say some, in regard there are more diseases to terminate in health then in death (except pestilentiall diseases) where the matter and cause is so malignant and poysonous, that nature many times doth not attend a fight or combate with the Disease, whereby it cannot properly be called a Crysis; that definition of Hypocrates will not well hold, unlesse it be in such diseases as doe determine in a recovery of the sick party: So some say."
- **Attribution:** the page presents this as an objection from unnamed "some". R1806 credits "The chapter", its precondition says "as described by the author", and its claim class is ATTRIBUTED_ANCIENT_AUTHORITY. U04 calls it Hippocrates' own "poisonous-disease exception".
- **Lost content:** the exception "pestilentiall diseases" is gone, and "many times" has become an absolute "does not fight". The actual conclusion (the definition holds only in diseases that end in recovery) has become "fails in that class". The premise that more diseases end in health than in death is also gone.
- **Fix:** restate it as a reported objection from "some", keeping all four of those elements, and change the claim class to a reported objection. Fix U04 to match.

**F2 (MEDIUM): R1807 runs Avicenna and Galen together.**
- **Source, PDF325:** "Avicenna, in Canticis, agrees with Galen, and saith, Crysis (est velox motus morbi ad salutem vel ad mortem.)"
- **Problem:** "agreeing with Galen that crisis moves disease swiftly toward health or death" puts the Latin's content on Galen. Galen's definition on the same page is only "Every sudden and vehement motion of the disease". The "toward health or death" part belongs to the Hippocrates report and to Avicenna's own words. "Moves disease" also misreads *motus morbi*, which means the disease's own motion.
- **Fix:** "Lilly says Avicenna, in Canticis, agrees with Galen, and says crisis 'est velox motus morbi ad salutem vel ad mortem'." Keep the Latin verbatim.

**F3 (MEDIUM): TABLE_GEOMETRY.json, R1826 and U13/U14 miss visible places where the print departs from the 22°30′ model.** Details are in §3.
- **Not recorded:** a systematic +1° offset in 60 cells, four isolated misprints, and a misleading input rule.
- **Input rule:** `chart_input` says "rounded to nearest printed table row as author illustrates". The author actually writes "because 42. minutes doe almost make one degree, I enter with 16. degr. under the Signe ♍ in the eighth column". Because of the offset, a nearest-printed-cell rule would choose column 7 row 30 ("15 30" in ♍, 12′ away) over the author's column 8 row 9 ("16", 18′ away).
- **Fix:**
  - add a `printed_exceptions` list flagging these cells as printed ≠ model;
  - note that all nine candidate checks fall outside the affected cells;
  - reword `chart_input` to describe the author's procedure, and mark the nearest-cell rule as editorial and unsafe in the affected cells;
  - replace U14's generic hedge with the specific cells.

**F4 (MEDIUM): R1798 weakens "all one" and attaches "more/lesse" to the wrong thing.**
- **Source, PDF325:** "…are all one, and intend no more then a certaine and more sure judgment of the infirmity afflicting, either more powerfully, or in a lesse measure at those times when the true Chrysis is."
- **Problem:** "Near-synonyms" weakens "all one". "Greater or lesser ascertainment" applies "more powerfully / lesse measure" to how certain the judgment is. On the page it describes how hard the infirmity afflicts, and the judgment itself is "certaine and more sure". The time qualifier ("at those times when the true Chrysis is") is also dropped.

**F5 (MEDIUM): R1808 changes the scope of the rival theory, and R1809/R1810 shift attributions (the latter two are low on their own).**
- **Source, PDF325–326:** "There are some that have contended, That although in diseases there is a Crysis, yet is it not caused by influence of the Celestiall bodies, but from inferiour causes." Later: "as many learned say, cannot be… more generally received and concluded".
- **Scope:** "some crises come from inferior causes" moves "some" from the people holding the view onto the crises. The printed rival theory is about crisis in general.
- **Attributions:** R1809's "The writer rejects…" should credit "many learned". R1810 should present the lunar conclusion as the generally received view, not as Lilly's own description.

**F6 (LOW): R1805 and U04 reframe Hippocrates' definition.** The page (PDF325) gives a definition: crisis is "an acute or swift reportation in diseases". "Acute" describes the crisis motion, not a class of disease. The candidate's "emphasis", "acute outcomes" and "acute-disease" drift toward acute illness as a category.

**F7 (LOW): R1816 adds "approximately".** PDF326 states the Moon's place exactly: "the place of the ☽ is 15. 42. ♍". The only approximation is the rounding to 16.

**F8 (LOW): R1815 wording about the figure and its date.** The hypothetical status is handled correctly. But the precondition says "the earlier question figure" where PDF326 says "the later Figure". The date also has no "as printed; calendar not stated; not converted" label. There is no conversion error.

**F9 (LOW): hedges and qualifiers lost or strengthened.**
- R1818: "some remisnesse" became "remission".
- R1819: "Semi-quadrate to her first place… as it were, halfe a Crysis" became "first semiquadrate", with "as it were" dropped.
- R1827: "very probable" was dropped.
- R1828: "a good indication" became causal ("attributes…to").
- R1829: "at present" and "the Crysis is then ill" were dropped.
- R1830: "formerly men" became "earlier authorities".
- R1839: "stirred up from ♄, by reason of his frigidity" became "attributed to Saturn".

**F10 (LOW): U22 adds a house.** PDF327 names only "the sixt, seventh, and eighth houses". U22 also lists "First". R1824 is correct.

**F11 (LOW): ERRATA_COLLATION entry 2 and U07/U24 under-claim the p. 295 target.** Details are in §3.

**F12 (LOW): source content with no record.**
- The head definition, "a duell or contention betwixt nature and the infirmity" (PDF324). R1795 only implies it.
- The objection's premise about health versus death (PDF325).
- "I have given sufficient direction in my Introduction" (PDF329), missing from R1831.
- What each phase is for: "wherein the Physician might expect how the disease then would shew it selfe" (first Indicative day) and "more fully discerned in one kind or other" (true Crysis).

**F13 (LOW): provenance paths don't resolve.** All 58 records, and TABLE_GEOMETRY's `witness`, cite `evidence/pdf-3xx.png`. `evidence/pdf-324.png` does not exist in this package; the supplied images are under `source_images/`. The status token is also misspelled `DILPOMATIC`.

## 3. Table (PDF328) and errata (PDF888)

**What the formula gets right:**
- **Size and headings:** 30 × 16 is correct, and the headings are ♈ ♈ ♉ ♊ ♋ ♋ ♌ ♍ ♎ ♎ ♏ ♐ ♑ ♑ ♒ ♓.
- **First row:** "0 30 | 23 | 15 30 | 8", repeated four times, fits 22°30′ per column and 1° per row starting at ♈0°30′.
- **Author's row (row 9):** "16" (♍), "8 30" (♎), "1♏", "23 30" (♏) and "16" (♐) match the text. All nine of the candidate's sample cells are correct.

**Systematic departure, 60 cells.** This affects 1-based rows 16–30 of columns 3, 7, 11 and 15 (0-based rows 15–29, columns 2, 6, 10, 14).
- The cells run "29 30" at row 15, then "1♊30" / "1♍30" / "1♐30" / "1♓30" at row 16, up to "15 30" at row 30.
- The formula gives 0°30′ to 14°30′ of the new sign.
- Each of these columns both begins and ends at "15 30", which is 30° of printed range over 29 one-degree steps.
- In row 16, the step from column 3 to column 4 ("23") is 21°30′, not 22°30′.
- I can't tell from the page whether this is an ordinal-degree convention or a calculation slip. Either way, the printed tokens don't match the formula.

**Isolated misprints, 4 cells (1-based):**
| Cell | Printed | Formula |
|---|---|---|
| r6 c10 | "38" | ♎28 |
| r11 c5 | "10 33" | ♋10°30′ |
| r13 c3 | "27 28" | ♉27°30′ |
| r15 c13 | "14 15" | ♑14°30′ |

**Not legible enough to judge:** r7 c1 (looks like "5 30"), r2 c12, and damaged numerals at r28 c6, r29 c2/c6 and r30 c2/c14.

**Notation differences only (same value, different printed form):** 8 cells on a sign boundary print "30" where the formula would give 0° of the next sign. 12 cells carry the sign symbol inside the cell.

**Not printed text:** pen strokes at r4 c1–c2 and r17 c1 belong to this copy, as does the handwritten "6th House" in the margins of PDF325, 327 and 329.

**Cell accounting:** the formula generates 480 cells. The candidate checked 9 values. 64 printed cells differ from the formula, and about 7 are too damaged to read. The remaining cells look consistent with the formula at this resolution, but I checked the pattern, not a certified cell-by-cell transcription.

**Errata (PDF888):** the line "p 291 l 7 r do, p 295 l 34 r atram" is legible, so both correction words are confirmed. No other erratum falls on printed pp. 290–296.
- **p. 295, line 34:** counting printed lines below the running head, line 34 is "Earthly Signes, Black melancholly, or A?ram Melan-". That is the only line with the word the erratum corrects, so the target line is established. The misprinted letters themselves aren't legible: the second letter is irregular and the initial is a capital A, so I can't confirm U24's "atr(a/u)m". `body_target_line_matched` should be true, with the misprint still unresolved and the page left unemended.
- **p. 291, line 7:** on the same count, line 7 is just "overcome." (or "were, betwixt…" if the running head is counted). There's no evident place for "do", so leaving it unmatched is correct.

## 4. Checked with no material problem
- **Starting-moment hierarchy:** onset → urine → first conversation, and the p. 292 restatement (R1799–R1801, R1812).
- **Galen:** R1802.
- **Worked-example values:** 16 ♍, 8°30′ ♎, 1 ♏, 23°30′ ♏, 16 ♐.
- **July 1645 example:** its hypothetical status (R1815 statement, U11).
- **7/14/21 days:** framed as former practice replaced by calculation (R1830/R1831).
- **Sign groups:** the printed fire → attractive/phlegmatic pairings are kept (R1832–R1835).
- **Purging rules:** the shared condition (Moon in ♋♏♓ and ✶/△) is kept (R1836–R1838).
- **Saturn and the six faculties:** paired by row alignment (R1839–R1845).
- **Humours:** R1846–R1849.
- **Chapter boundaries:** R1794, R1850, R1851.

No wrong planet or zodiac symbol, sign name or pronoun reference found. Every record correctly treats the content as 17th-century humoral and astrological theory with no clinical evidence (no cases, counts or outcomes).

## 5. Uncertainties (no fix proposed)
- What p. 291 line 7 "r do" is meant to correct.
- The exact misprinted letters on p. 295.
- Whether "or it is not a locall motion altogether…" in R1803 continues Galen or is a separate definition.
- The cause of the table offset, and the damaged cells.
- U31's 15°43′ reading, which refers to a chart wheel not in the supplied images.
- Whether "♂ ☉" means "and" or "or".
- On p. 292, "3■ min." is blotted, but the surrounding text and the table both support 30.

---
**FINDS_ERROR**: 1 HIGH, 4 MEDIUM, 8 LOW.
- **Images inspected:** PDF324 (below the rule) through PDF330 (above the rule), all seven, plus errata PDF888, including the boundary areas on PDF324 and PDF330.
- **Records inspected:** all 58 (R1794–R1851), plus TABLE_GEOMETRY (the formula and its 9 sample cells), ERRATA_COLLATION (2 entries) and UNRESOLVED (31 items).
- **Limits of this review:**
  - Images were read at the supplied resolution with no zoom.
  - This is one copy with no comparison against other editions, and the Wellcome identifier isn't visible in the images.
  - I couldn't recompute the PDF's SHA-256 or check that the images match the PDF; I had no shell access.
  - The table pass checks consistency, so the list of exceptions may not be complete.
  - The ancient authorities were checked only for what Lilly says about them, not against their own texts.
  - No empirical or clinical validity was assessed or implied.
