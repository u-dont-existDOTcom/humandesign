# Independent source-fidelity check: Lilly 1647, Ch. XLV, B02o (R1746–R1769)

**Result: not acceptable as it stands.** 10 PASS / 13 NEEDS_CORRECTION / 1 UNRESOLVED. This is a diagnosis only; I wrote no files.

## 1. What I examined

- **Page images (pixels):**
  - `evidence/pdf-320.png`, `evidence/pdf-321.png`, `evidence/pdf-322.png`
  - the caption crop `evidence/case_xlv_date_caption_verified.jpg`
- **Files:** RULES.json (all 24 records, one by one), CASE_EVIDENCE.json, CHART_INSCRIPTION.json, AUDIT_REPORT.md, SECTION_COVERAGE.json, UNRESOLVED.json, SOURCE_IDENTITY.json, COUNTS.json.
- **Not examined:**
  - **PDF323 image:** not found. Read can't list directories, and about 35 likely paths failed (`evidence/pdf-323.png/.jpg`, `pdf323`, `pdf_323`, `page-323`, and `pages/`, `images/`, `source-pages/` variants).
  - **Page-image/hash manifest:** not found under any name I tried (MANIFEST.json, SHA256SUMS*, *HASHES.json, *MANIFEST.json variants). So I can't confirm that the PNGs come from the hashed PDF.
  - **Producer notes:** CHAPTER_XLV_DATE_CORRECTION.md and SOURCE_FIRST_NOTES.md, excluded as you instructed.
  - **Back-reference pages** 113, 244, 245 and 248, which are outside the admitted range.
- I did not hash anything or calculate an ephemeris. The only arithmetic I did was ordinary weekday/calendar arithmetic.

## 2. Chart caption: literal reading and calendar reading

**Literal caption** (PDF320, chart centre, four lines):
`1645` / `♃ 8°. Maij.` / `6: 15′. P·M.` / `hor: aſtr:`

- The superscript "o" of `8°` is printed high, between lines 1 and 2. The minute mark `′` after `15` sits between lines 2 and 3.
- `P·M.` has a raised point. `aſtr` uses the long s.
- **♃, not the number 24:** it is a single Jupiter character: a hooked "2" shape joined by a bar to a stem that drops below the line. It stands before the day number. The diagram's own cusp numerals "24" (rotated, in the top and bottom sectors) are printed as two separate digits. Reading "24" as the day would also leave `8°` with no function. Reading ♃ as the weekday (Thursday) is justified.
- **Not printed:** a place, "O.S."/"Julian", a weekday spelled out, or any time zone.

**Calendar reading I consider justified:** Thursday 8 May 1645, Julian (Old Style).

- "Julian" is an inference from English usage in 1645, not printed text. The Lady-Day year start doesn't affect May.
- This equals 18 May 1645 Gregorian.
- The weekday supports the Julian reading: Julian 8 May 1645 was a Thursday. A Gregorian 8 May 1645 would be a Monday, which conflicts with ♃.
- The clock time is 6:15 p.m. "hor: aſtr:" stays unresolved, and no conversion to UT is possible.

**Chart centre below the caption (literal):** `♀ ☽ a △ ☿` / `ad □ ☉` / `et ✶ ♄`. Two things are uncertain:
- The ♀ sits at the left margin directly under "hor:". It could belong to the line above it or to the aspect string.
- I read the glyph after △ as ☿ (horns over a circle), with moderate confidence.

## 3. Verdict map

| ID | Verdict | Basis |
|---|---|---|
| R1746 | PASS | Caption and ♃≠24 confirmed; Julian correctly framed as a precondition, not as printed text |
| R1747 | NEEDS_CORRECTION | E1 |
| R1748 | NEEDS_CORRECTION (minor) | E2 |
| R1749 | NEEDS_CORRECTION | E3 |
| R1750 | PASS | "♈ repreſents the Head, as you may ſee page 245." |
| R1751 | NEEDS_CORRECTION (minor) | E4 |
| R1752 | PASS | "♂ Lord of the aſcendant in ♌ doth ſignifie the Heart."; Leo is the present placement |
| R1753 | PASS | "♂ at time of that □ in ♋"; time split is correct (see note) |
| R1754 | PASS | Faithful; optionally keep "poſitively concluded" and "all his diſeaſe" |
| R1755 | PASS | "principall Significator … in his owne Termes, and the ☽ in his houſe applying unto him" |
| R1756 | NEEDS_CORRECTION | E5 |
| R1757 | NEEDS_CORRECTION | E6 |
| R1758 | NEEDS_CORRECTION | E7 |
| R1759 | NEEDS_CORRECTION | E8 |
| R1760 | NEEDS_CORRECTION (minor) | E9 |
| R1761 | PASS | The break "be-" / "ſides" matches the catchword; the airy-sign explanation is captured |
| R1762 | NEEDS_CORRECTION | E10 |
| R1763 | PASS | Optionally restore the closing "&c." |
| R1764 | PASS | Faithful; correctly framed as a historical suggestion |
| R1765 | NEEDS_CORRECTION | E11 |
| R1766 | NEEDS_CORRECTION | E12 |
| R1767 | NEEDS_CORRECTION | E13 |
| R1768 | PASS | Literal; correctly does not call the antiscion a duration testimony |
| R1769 | UNRESOLVED | PDF322 half verified (divider, catchword "CHAP."); PDF323 image not available to me |

PASS means the record's content is faithful to the page. It does not mean the record is accepted: the cross-cutting issues C1–C4 below still apply to every record.

**Note on R1753 (Mars timing):** the source time-stamps only "♂ at time of that □ in ♋". "Both of them in Cardinall Signes" carries no time stamp. Only the square-time reading is self-consistent, given "in ♌" (PDF321) and "fixt in a fixed Signe" (PDF322). So the record's "cardinal at the square" is a justified inference: Cancer belongs to the earlier square, Leo to now.

## 4. Errors

**E1. R1747, PDF320 chart centre, field `source_statement`**
- **Visible:** "♀ ☽ a △ ☿ / ad □ ☉ / et ✶ ♄"
- **Record:** "depicts Venus and Moon with an aspect string involving triangle, Mercury…"
- **Type:** attribution and omission. It folds ♀ into the Moon's aspect string, whose attachment is uncertain. It drops a/ad/et, the words that carry the separation/application structure. "Triangle" is the shape, not the trine.
- **Repair:** "Below 'hor: aſtr:' the centre prints '♀ ☽ a △ ☿ / ad □ ☉ / et ✶ ♄'. The attachment of the leading ♀ and the sense of a/ad/et (plausibly 'from'/'to'/'and') are UNRESOLVED. The same author's prose says ☽ 'applyed to a □ of ☉' (PDF321) and ☽ 'in ✶ with ♄' (PDF322); this agrees with the diagram but is not independent of it."

**E2. R1748, PDF320–321, field `source_statement`**
- **Visible:** "not affli-" / "cted by the evill poſition or preſence of any evill Planet"
- **Record:** "an evil planet's position or corporeal presence"
- **Type:** an inserted gloss ("corporeal"), and the "evill" before "position" is dropped. The star name prints as italic "Chelæ" (the æ ligature is fairly legible); the record normalises it to "Chele" without saying so.
- **Repair:** quote "not afflicted by the evill position or presence of any evill Planet". Add "printed 'Chelæ' (italic)".

**E3. R1749, PDF321, field `source_statement`**
- **Visible:** "from that houſe I muſt require the part or member of the Body afflicted or moſt grieved, as you may read page 244."
- **Type:** an omitted method clause and an omitted back-reference.
- **Repair:** append "Lilly concludes that the afflicted or most grieved part or member is to be sought from the sixth house (back-reference: page 244)."

**E4. R1751, PDF321, field `preconditions`**
- **Visible:** "♄ in ♈ ſignifieth the Breſt, as page 113."
- **Record:** "Requires the conjunction of Saturn and Aries"
- **Type:** misused technical term. "Conjunction" is an aspect between planets; a planet can't be conjunct a sign.
- **Repair:** "Requires ♄ located in ♈ (planet in sign)."
- **Also:** a handwritten number in the right margin, level with this line, reads roughly "119+". It is matched by an apparent hand-made cross after "113.". Log it as a copy-specific, non-authorial note with an unresolved reading. Do not change "113".

**E5. R1756, PDF321, fields `source_statement` / `exceptions`**
- **Visible:** "ſuch dry Diſeaſes as are occaſioned from melancholly diſtempers… ſee page 244. how to make a right mixture, your Phyſicians beſt know, and what Diſeaſes man may be ſubject unto in thoſe parts…"
- **Type:**
  - (a) Conflation: "Saturn-Moon terms/application". The source says ♄ is in his own terms and the ☽ is in ♄'s house applying to him; it says nothing here about the Moon's terms.
  - (b) The page-244 locator is missing.
  - (c) The "your Physicians best know" sentence is missing entirely. It is Lilly's deferral to physicians on medical matters.
  - (d) The qualifier "occasioned from melancholly distempers" is dropped.
- **Repair:** restate as "♄ (in own Termes) with ☽ (in ♄'s house, applying to ♄) 'did prenote Melancholly, and such dry Diseases as are occasioned from melancholly distempers'… see page 244". Add the deferral clause and label it as author deferral, not advice.

**E6. R1757, PDF321, field `source_statement`**
- **Visible:** "and the ☽ out of his Termes, applyed to a □ of ⊙, and he in ♂ his Termes"
- **Record:** "Moon outside his terms"
- **Type:** an unsupported polarity, plus a silently chosen antecedent ("his" could be ♂ or ♄). Evidence on the same pages:
  - PDF322 uses "out of" again: "in □, out of Angles". Reading that as "not angular" conflicts with "the ☽ in the fourth" on the same page, so this author's "out of" can mean "from".
  - PDF322 says ☽ and ☉ are "both in the Termes of an Infortune".
- **Repair:** quote literally. Mark the sense of "out of" (outside vs. from) and the antecedent of "his" as UNRESOLVED. Note that "he" is most plausibly ☉, using the period possessive "♂ his" = "Mars's". Keep "Choller was a secondary cause" as is.

**E7. R1758, PDF321, field `source_statement`**
- **Visible:** "and indeed when I came to ſpeak with him"
- **Record:** "later came to speak"
- **Type:** invented time order. "Later" implies the judgment was fixed before the meeting, which the text doesn't say. It also loses "and indeed", which is the author framing the symptoms as confirmation.
- **Repair:** "Lilly writes 'and indeed when I came to speak with him' and then describes the doctor's condition. When this meeting happened relative to the chart or its judgment is not stated."

**E8. R1759, PDF321, `source_statement` and class**
- **Visible:** "very ſilent, dull and melancholy … complained of great weakneſſe and paine in his Breſt, and at the Heart"
- **Type:** "dull" is omitted. The self-report marker is flattened: only the breast/heart weakness and pain is explicitly the patient's complaint. The head pain, silence, poor sleep and cough are stated in the author's voice, and the text doesn't say how the author knew them.
- **Repair:** restore "dull". Tag the breast/heart item as `PATIENT_COMPLAINT_AS_RELAYED` and the rest as `AUTHOR_STATED_CONDITION`.

**E9. R1760, PDF321, field `source_statement`**
- **Visible:** "as if there was inclination to the Jaundies"
- **Record:** "alleged inclination"
- **Type:** wrong modality/attribution. "Alleged" implies someone made a claim; the source has the author's own hedged comparison.
- **Repair:** quote "as if there was inclination to the Jaundies" and call it the author's hedged inference from appearance.

**E10. R1762, PDF322, field `source_statement`**
- **Visible:** "ſo doth alſo the ☽ in ♒ ſignifie the Secrets and Diſeaſes therein, &c."
- **Record:** "another Moon placement with diseases of those parts"
- **Type:** a legible source value is left out, and "&c." is dropped. ♒ (two wavy lines) is legible. It agrees with "ayery Signe", with the ☽ being "in his [♄'s] houſe", and with the diagram's ☽ entry in the fourth-house sector next to an Aquarius glyph.
- **Repair:** state "☽ in ♒" and keep "&c.". Narrow U15 accordingly (the glyph is checked; the correspondence is still the author's claim).

**E11. R1765, PDF322, fields `kind` / `source_claim_evidence_class`**
- **Visible:** "for the ☽ in the fourth in ✶ with ♄, argued ſickneſſe untill death: *He dyed the fourteenth of Auguſt following.*" The last sentence is set in italic.
- **Type:** two classes merged in one record: an author's astrological inference and an author-reported death. The italic setting isn't recorded. The "for" link is lost: the clause is given as the reason the remedy could only "for a while prolong his life" (R1764).
- **Repair (keeps the count at 24):** inside R1765, store two components, each with its own class: `inference` and `reported_outcome` (typography: italic). Add a link to R1764. Splitting it into two records would change the count, so that is your call.

**E12. R1766, PDF322, field `source_statement`**
- **Visible:** "♄ Being author of the Diſeaſe, ſhewed it would be permanent, or of ſome continuance, as page 248. for he is a ponderous, ſlow Planet: beſides, the Angles of the Figure are all fixed"
- **Record:** "fixed angles are invoked for an illness of some permanence or continuance"
- **Type:** wrong attribution, and page 248 is omitted. "Permanent, or of some continuance" is Saturn's testimony; the fixed angles are an added ("besides") testimony.
- **Repair:** "♄, as author of the disease, 'shewed it would be permanent, or of some continuance, as page 248', because 'he is a ponderous, slow Planet'. 'Besides', the angles of the figure are all fixed."

**E13. R1767, PDF322, fields `source_statement` / `preconditions`**
- **Visible:** "and in □, out of Angles, both in the Termes of an Infortune; … all theſe portended the longitude of the Diſeaſe"
- **Type:**
  - (a) "Disease longevity" can be misread as the patient's long life. The source says "longitude", meaning length.
  - (b) Scope: "all these" also covers ♄ and the fixed angles (R1766), not just the R1767 items.
  - (c) The precondition "angular status" assumes "out of Angles" means "not angular". That reading clashes with "the ☽ in the fourth" on the same page. (That the fourth is an angle is standard in this tradition but isn't defined on the admitted pages.) It also clashes with the "☉ 28." entry, which I read as sitting in the seventh-house sector.
- **Repair:** quote "portended the longitude of the Disease"; note that the scope of "all these" includes R1766; record "out of Angles" with its sense UNRESOLVED.

**R1769 (UNRESOLVED, not an error).**
- **Confirmed on PDF322:** the text ends at "…being the *Luminary* of the time." There follows a blank band (apparently show-through from the other side of the leaf, not printed text), a horizontal rule, and the catchword "CHAP." bottom right.
- **Not confirmed:** "Chapter XLVI", "another dated horoscope" and printed 289. Either supply the PDF323 image, or cut the statement back to what PDF322 shows.

## 5. Cross-cutting issues and coverage gaps

- **C1. Distinct classes are not encoded.** All 24 records carry the same `source_claim_evidence_class` and `source_statement_class`. Add a per-record `claim_class` from {CHART_INSCRIPTION, AUTHOR_ASTROLOGICAL_INFERENCE, AUTHOR_STATED_CONDITION, PATIENT_COMPLAINT_AS_RELAYED, AUTHOR_THERAPEUTIC_SUGGESTION, AUTHOR_REPORTED_OUTCOME, STRUCTURAL_BOUNDARY}. R1759, R1760, R1761 and R1765 are mixed and need component tags.
- **C2. Two of the three printed subheadings are missing:** "What part of the Body was afflicted." (PDF320) and "From what Cause the Sickneſſe was." (PDF321). Add a `source_subsection` field.
- **C3. The prognosis is printed after the outcome.** The death report (R1765) is printed under the *Cause* subheading. The "long or ſhort?" judgment (R1766–R1768) comes after "He dyed…". So the duration judgment, as printed, was written with knowledge of the outcome. Add this to the R1766–R1768 limits and to U19.
- **C4. Page references are not fully carried.**
  - page 244 appears twice (sixth house → member; Saturn's infirmities) and is in no record.
  - page 248 is in no record.
  - Only 113 (R1751) and 245 (R1750) are carried.
- **C5. Handwritten marginalia on PDF321 are not logged:** "6th Houſe" (approximately) in the top right, next to "287", and the "119+" near the page-113 line (E4).
- **C6. Diagram positions are not extracted.** U04 acknowledges this, but for a source-complete extraction it is a missing genre. My provisional readings, **not to be ingested**:

| Reading | Confidence |
|---|---|
| Ascendant ♏ 11; descendant ♉ 11 | Firm |
| 12th cusp ♎ 21.36; 6th cusp ♈ 21.36 | Firm |
| ♄ 28.32 in the sixth sector | Firm; matches "in his Fall" |
| "☉ 28." in the seventh sector | Moderate |
| ☽ 27.57 just past the ♒ IC | Moderate |
| A top-sector entry "2.6" | Glyph not securely legible to me |

  If that "2.6" is ♂ in ♌, its antiscion falls near the "☉ 28." entry, which would fit R1768. That is my own arithmetic on uncertain glyphs, not verification.
- **C7.** PDF323 and the page-image/hash manifest are unavailable (see §1).

## 6. AUDIT_REPORT: load-bearing paraphrases

- **A1. Wrong.** "captioned **Thursday 8 May 1645 Julian**": the caption prints ♃ and no calendar. Fix to "♃ 8°. Maij 1645; read as Thursday; Julian/O.S. inferred, corroborated by weekday".
- **A2. Narrowed.** "no evil planet afflicting the ascendant by its corporeal presence" drops "evill position" (E2).
- **A3. Wrong polarity.** "the Moon outside his terms" (E6).
- **A4. False.** "page113/244/245 backward references are retained": 244 isn't in RULES, and 248 is omitted (C4).
- **A5. Overreach.** Putting "the antiscion of Mars near Sun" in the duration argument: the antiscion comes after "all these portended the longitude of the Disease:" and only "afflicteth him [☉]".
- **A6. Ambiguous.** "angular position" (E13).
- **A7. Drift.** "principal source of melancholy" for "principall Significator"; "wasting" for "Consumption" modernises the term (contrary to U10).
- **A8. Unverified by me.** PDF323 / printed 289 / "XLVI" / "July1645"; and the B02n supersession, which lives in an excluded producer note.
- **Confirmed:** 24 documentary records, 1 chart, 1 author-reported case; 1,745+24 = 1,769; 1,769+1,066 = 2,835 (internally consistent); Cancer-then vs. Leo-now; choler as secondary.

## 7. Other files

- **CHART_INSCRIPTION:**
  - `source_calendar: "Julian…"` presents an inference as a source fact. Rename it `inferred_calendar` and record the basis.
  - `printed_time` is normalised; store the literal "6: 15′. P·M.".
  - `source_center_aspect_line`: add the uncertainty about where ♀ attaches.
  - The 18 May Gregorian / Thursday cross-check is correct.
- **CASE_EVIDENCE:**
  - `julian_question_date` needs an `inferred_` prefix, like `inferred_reported_julian_date`.
  - All other fields are correctly limited (`documented_prediction_freeze_before_outcome: false`, `outcome_independently_verified: false`).
- **UNRESOLVED:**
  - U02 calls "Thursday 8 May 1645 Julian" a "verified local caption"; reword to keep the Julian part as an inference.
  - U09 wrongly ties page refs to Mars in Leo, which has none.
  - Add entries for: the two "out of" readings and the "his" antecedent; the ♀ attachment; marginalia; C3 retrospective placement; the missing PDF323/manifest.
- **SECTION_COVERAGE:** "complete source matter" for PDF321 overstates; see C2, C4, C5, E3, E5.
- **COUNTS:** consistent. If R1765 is split, the counts change.

## 8. Weakest step and remaining limits

**My weakest verified step** is reading the diagram's small, rotated glyphs from a page image of about 1,330 pixels with no zoom: ☿ in the centre line, where ♀ attaches, "☉ 28." being in the seventh sector, and the "2.6" glyph. I use the ☉ placement only as secondary support for E13; the main support is the printed "☽ in the fourth". The "out of" = "from" possibility depends on my knowledge of Early Modern English usage, which the packet can't confirm. That is why I recommend UNRESOLVED rather than repairing it to "from".

**Remaining source issues:**
1. PDF323 boundary content.
2. Pages 113/244/245/248 and the marginal "119" are unverified.
3. The diagram glyphs and degrees.
4. What "hor: aſtr:" means.
5. The sense of "out of" (twice) and the antecedent of "his".
6. Which stars "Chelæ" refers to.
7. Julian is a contextual inference.
8. Only one copy is checked; there is no collation with the 1659 edition (U01).
9. Image provenance against the hashed PDF.

The endpoint stays retrospective and non-independent: one doctor, one chart, one death reported by the author, and the duration judgment printed after it.