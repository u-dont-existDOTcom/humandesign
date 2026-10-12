# Recheck: Lilly 1647, Ch. XLV (B02o, R1746–R1769)

**Verdict: not acceptable as it stands.**
- **Caption:** handled correctly.
- **E-repairs:** 10 pass; 3 need small wording fixes.
- **Records:** 19 pass, 4 need minor wording fixes, 1 stays unresolved.
- **Two blockers:**
  - `CLAIM_LEDGER.json` comes from an earlier draft of the report and still states errors the report has since fixed (D1).
  - I couldn't open any PDF323 image, so R1769 and C7 stay UNRESOLVED (D2).

I changed no files.

## Scope
- **Page images read:** `evidence/pdf-320.png`, `pdf-321.png`, `pdf-322.png`, `case_xlv_date_caption_verified.jpg`, `case_xlv_full_chart_detail.png`.
- **Files read:**
  - All 24 records in RULES.json (all 1,111 lines).
  - All 13 paragraphs of AUDIT_REPORT.md and all of CLAIM_LEDGER.json (C01–C15).
  - INITIAL_DIAGNOSIS, REVIEW_REQUEST, CHART_INSCRIPTION, CHART_GLYPH_OBSERVATIONS, CASE_EVIDENCE, SECTION_COVERAGE, UNRESOLVED (U01–U27), COUNTS, SOURCE_IDENTITY, SOURCE_IMAGE_MANIFEST and TEST_RUN_SUMMARY.
- **Not read:**
  - **PDF323:** 47 candidate paths failed. The manifest lists only PDF320–322, and Read can't list directories.
  - **NEXT_CHAPTER_SOURCE_NAVIGATION.md:** the report cites it, but it isn't in the directory.
  - **Producer notes:** I treated these as excluded external notes.
  - **Pages 113/244/245/248.**
- **Not checked:** I didn't check any hash, byte count or test. The "53 run / 0 failed" result is the producer's summary. My only calculation was weekday arithmetic.

## Caption: PASS
- **Literal text (PDF320, chart centre):** `1645` / `♃ 8°. Maij.` / `6: 15′. P·M.` / `hor: aſtr :`
- **♃ is not "24":** it is one Jupiter glyph. Where the wheel prints "24", it uses two separate digits.
- **Weekday arithmetic:**
  - Julian 8 May 1645 was a Thursday.
  - Gregorian 8 May 1645 was a Monday, which conflicts with ♃.
  - Julian 8 May is Gregorian 18 May, also a Thursday.
- **Julian is inferred, not printed.** That is stated correctly in AUDIT_REPORT.md:9, U02 and CHART_INSCRIPTION (`inferred_calendar` and its basis). What's left is in D7 and D1.

## E1–E13

| E | Record | Verdict | Source anchor and basis |
|---|---|---|---|
| E1 | R1747 (RULES.json:71) | PASS | PDF320 centre `♀ ☽ a △ ☿ / ad □ ⊙ / et ✶ ♄` is quoted; how ♀ attaches and what a/ad/et mean are left open |
| E2 | R1748 (:115) | PASS | PDF321 "by the evill poſition or preſence of any evill Planet"; italic "Chelæ" (PDF320) |
| E3 | R1749 (:157) | PASS | PDF321 "…part or member of the Body afflicted or moſt grieved, as you may read page 244." |
| E4 | R1751 (:241) | PASS | PDF321 "♄ in ♈ ſignifieth the Breſt, as page 113."; the handwritten cross and "119+" are logged as copy-specific |
| E5 | R1756 (:452) | **CORRECTION_REQUIRED (minor)** | Original problems (a)–(d) are fixed, but the repair adds a new gloss (D4) |
| E6 | R1757 (:499) | PASS | PDF321 "the ☽ out of his Termes … and he in ♂ his Termes"; both ambiguities kept open (U22) |
| E7 | R1758 (:546) | PASS | "and indeed when I came to ſpeak with him"; no invented "later" |
| E8 | R1759 (:589) | PASS | "dull" restored; only "complained of great weakneſſe and paine in his Breſt, and at the Heart" is tagged as the patient's complaint |
| E9 | R1760 (:647) | PASS | "as if there was inclination to the Jaundies" is treated as the author's hedge |
| E10 | R1762 (:747) | **CORRECTION_REQUIRED (minor)** | The statement now has PDF322 "☽ in ♒ … therein, &c.", but an exception still contradicts it (D5) |
| E11 | R1765 (:876) | PASS | Two components (inference / italic reported outcome), linked to R1764 |
| E12 | R1766 (:941) | PASS | Saturn "ſhewed it would be permanent … as page 248"; fixed angles come after "beſides" |
| E13 | R1767 (:990) | **CORRECTION_REQUIRED (minor)** | "longitude" now means duration and "out of Angles" is left open; but the scope of "all these" is over-resolved (D3) |

## C1–C7

| C | Verdict | Basis |
|---|---|---|
| C1 claim classes | CORRECTION_REQUIRED (minor) | `claim_class` and components are in place; R1761 is still missing one component (D6) |
| C2 subheadings | PASS | All three printed subheadings are carried, and record order matches the print |
| C3 order | PASS | R1766–R1768 notes, U19, U24, CASE_EVIDENCE, COUNTS and AUDIT_REPORT.md:31 all record that the duration paragraph follows the death report |
| C4 page refs | PASS | 244 ×2, 245, 113 and 248 are all carried, and U09 is fixed. The ledger is still wrong (D1) |
| C5 marginalia | PASS | U25 and R1751 match "6th Houſe" by "287" and "119+" by the page-113 line |
| C6 diagram | PASS | Checked on the detail crop: ♏11/♉11, ♎21.36/♈21.36, ♄28.32 in the sixth-house sector. ♂ "2.6" is not ingested |
| C7 PDF323 / manifest | **UNRESOLVED** | D2 |

## Remaining defects and minimal fixes

**D1 (blocking): CLAIM_LEDGER.json is stale.**
- None of items C04–C15 matches a current report paragraph.
- Its `report_sha256` (87df02…) differs from the report hash in TEST_RUN_SUMMARY.json:74 (6e3675…). I compared the strings only; I didn't compute either hash.
- It still states errors the report has fixed:
  - C06: "captioned Thursday 8 May 1645 Julian"
  - C08: "Chele" and "corporeal presence"
  - C09: "principal source of melancholy", "Moon outside his terms", and "page113/244/245 … retained" with no 248
  - C10: "reports of headache" and "wasting"
  - C13: "angular position", and the antiscion listed among the duration testimonies
  - C14: cites SOURCE_FIRST_NOTES.md
  - C15: "accepted R1769"
- **Fix:** regenerate the ledger from the current report, or mark it SUPERSEDED.

**D2 (blocks R1769 and C7): PDF323 is not in the packet as far as I can find.**
- REVIEW_REQUEST.md:2 says it is supplied. SOURCE_IMAGE_MANIFEST.json:4–26 lists only PDF320–322, and doesn't list the two crops either.
- What I can confirm on PDF322:
  - the text ends "…being the *Luminary* of the time.";
  - then a blank band, a rule, and the catchword "CHAP."
- That only shows a chapter starts on the next page.
- These rest on the controller's word alone:
  - the "CHAP. XLVI…" title and the "July1645" chart (RULES.json:1085);
  - U18 and AUDIT_REPORT.md:7 and :39;
  - "a separate following-boundary image" (AUDIT_REPORT.md:35).
- **Fix:** either
  - put the PDF323 image in `evidence/` with a manifest entry (path, bytes, sha256), and add the two crops; or
  - cut these claims back to the catchword plus U26.
- In both cases, record in AUDIT_REPORT.md:35 and in U26 that this recheck also couldn't open PDF323.

**D3: R1767 over-resolves "all these" (RULES.json:990, :996).**
- On PDF322 the Saturn clause has its own verb: "♄ … ſhewed it would be permanent…".
- After it: "beſides, … ; all theſe portended the longitude of the Diſeaſe".
- So "all these" certainly covers the "besides" items, including the fixed angles. Whether it also takes in Saturn is open.
- :990 says "INCLUDING Saturn's slow nature" as fact, and :996 can be read as covering R1766 only.
- **Fix:** "covers at least the 'besides' items (fixed angles [R1766]; luminaries and Mars [R1767]); whether it also takes in Saturn is unresolved."
- This partly comes from INITIAL_DIAGNOSIS E13(b), which overstated the Saturn point.

**D4: R1756 glosses the physician deferral (RULES.json:452).**
- The record says "defers medicine preparation and the likely ailments".
- PDF321 prints "how to make a right mixture, your Phyſicians beſt know, and what Diſeaſes man may be ſubject unto in thoſe parts".
- The sense of "mixture" isn't stated: it could be a compounded medicine or a combining of significations. And "may be subject unto" is not "likely".
- **Fix:** "defers to physicians 'how to make a right mixture' (sense not stated) and 'what Diseases man may be subject unto…'".

**D5: R1762's exception is out of date (RULES.json:752).**
- It says the Moon-sign glyph still needs image-level checking, which contradicts the record's own statement and U15.
- **Fix:** "♒ checked legible on PDF322; the body correspondence is still the author's claim."

**D6: R1761 is missing a component (RULES.json:714–721).**
- PDF322 gives a reason: "for the ☽ is in an ayery Signe". The record has no component for it.
- **Fix:** add an AUDIT_ASTROLOGICAL_INFERENCE component with that text.

**D7: two Julian date fields lack the `inferred_` prefix.**
- CHART_INSCRIPTION.json:9 `julian_calendar_date`
- CASE_EVIDENCE.json:7 `julian_question_date`
- **Fix:** rename or drop both. Optionally, also mark Julian as "not printed" in R1746's precondition (:31).

**D8: report wording.**
- AUDIT_REPORT.md:21 "head or breast": the page prints "Head and Breſt".
- :25 "Later he adds" → "He further adds" (avoids invented chronology).
- :25 and R1763 at :792 "red gravels": the page prints "red gravell".
- :29 "These substances" → "These suggested remedies".
- :39 "accepted R1769" → "if R1769 is accepted". The same paragraph's PDF324/XLVII claims cite a file that isn't in the packet.

**D9 (trivial): the `source_witness_fragments` aren't literal.**
- They normalize glyphs and spelling (☽→Moon, ♒→Aquarius, untill→until).
- **Fix:** restore the printed forms, or rename the field `normalized_…`.

**D10 (nits):**
- R1768 :1061 calls the antiscion a "duration interpretation", but it sits after the "all these" summary.
- R1769 :1085 calls the death a "death testimony"; it is an author-reported death.
- R1749 :159 has the typo "six-house".
- R1765 :876 says "hope"; the text gives a purpose ("whereby he might…"), not a hope.
- U18 should cross-reference U26.

## Per-record verdicts
- **PASS (19):** R1746, R1747, R1748, R1749, R1750, R1751, R1752, R1753, R1754, R1755, R1757, R1758, R1759, R1760, R1763, R1764, R1765, R1766, R1768.
- **CORRECTION_REQUIRED, minor (4):** R1756 (D4), R1761 (D6), R1762 (D5), R1767 (D3).
- **UNRESOLVED (1):** R1769 (D2). The PDF322 half is confirmed.

## Report paragraphs and required preservations
- **Report paragraphs:**
  - **Pass:** AUDIT_REPORT.md:9, :11, :15, :17, :23, :31 and :37. The count arithmetic (1,769; 2,835) checks out.
  - **Minor wording (D8):** :21, :25 and :29.
  - **Also affected by D2:** :7, :35 and :39.
  - **Earlier findings:** the report fixes A1–A7 from the initial review; A8 (PDF323) is still open.
- **Preservations you asked for:** all present in the records and report:
  - "out of his Termes" and "out of Angles" left open
  - the uncertain attachment of ♀ in the chart centre
  - Saturn's testimony kept separate from the fixed angles (R1766), apart from D3
  - partial chart glyphs not over-read
  - the split between what the author states and what the patient complained of
  - both physician deferrals
  - the duration paragraph placed after the death report
  - the 14 August death recorded as author-reported, with no claim of clinical or predictive validity
- The stale ledger (D1) breaks several of these.
- **Two notes from my own reasoning outside the source** (not evidence; don't ingest):
  - Assuming London latitude, 6:15 PM falls in the planetary hour of ♀. So the leading ♀ may not be part of the aspect string at all, which is a reason to keep U21 open.
  - From my unverified memory of Lilly's table of terms, two readings of "out of his Termes" fit the chart:
    - "his" = ♂ with "out of" = "from";
    - "his" = ♄ with "out of" = "outside".
  - So U22 has to stay open.

## Weakest uncertainty
- **Is PDF323 really absent, or just under a name I didn't guess?** Read can't list directories, so D2 could be a limit of my tools rather than a packet defect. Read did suggest the correct name for a mistyped `CLAIM_LEDGER.md`, but gave no suggestion for any `pdf-323` variant. That only weakly suggests the image isn't there.
- **D3 and D4** depend on my reading of 17th-century syntax and word sense. That's why both fixes leave the question open rather than pick an answer.
- **Glyph-level readings** on images about 1,330 px wide: italic "Chelæ", singular "gravell", and the marginal "119+".