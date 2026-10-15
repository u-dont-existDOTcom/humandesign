# Lilly II.LII: first-pass original-source image inventory — PROVISIONAL ONLY

**2026-10-15 Africa/Dakar (UTC+0). Batch B02x OPEN. Lilly canonical accepted R1–R3016 unchanged.** The owner task is original-text intake of the full astrology corpus, not successful horoscope, war, court, partnership or safety prediction claims.

## Original 1647 source window

Source: William Lilly, *Christian Astrology* 1647, Wellcome **b30338724** original PDF, previously verified SHA256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`. Original source-image authority is the **scans**, not a modernized text excerpt or generated paraphrase. This batch reuses the already downloaded original physical source and original images; it does not redownload the complete 141 MB PDF.

- PDF403, original printed **369**: starts **CHAP. LII. Who shall doe best in a suit of Law.** near top; includes law-suit contests, a printed margin promise of later seventh-house discussion, comparison of War/Kingdom planet strength (exaltation v. house) and other questions; then unnumbered headings on formation/continuance of **partnership** and **which partner prospers**. Last partner-loss sentence continues on PDF404.
- PDF404, original printed **370**: completes partner-loss sentence; partner/querent second/eighth-house wealth distinction; unnumbered **familiarity between neighbors**, **moving from place to place** and **Another** moving criterion. The word **Of** from a further subsection heading appears at the bottom and continues on PDF405.
- PDF405, original printed **371**, **ABOVE divider only**: completes heading **Of removing from one place to another; or of two Businesses, which is best**; discusses choosing the stronger option by house, planet and Moon separation/application. The final unnumbered subsection is **If it be best to remove or stay in any place, whether Village, Territory, City or House**, with combined fourth/seventh and first-house conditions.
- On PDF405, a **horizontal divider** ends Chapter LII. **CHAP. LIII. Of Hunting** starts **below** the divider and is navigation-only for B02x. Chapter LIII continues on PDF406; its later law-suit passage is **NOT** Chapter LII, even though the topic returns to legal disputes.

## Draft extraction methodology and result

`SOURCE_FIRST_CLAUSES_DRAFT.json` holds **55 provisional source units R3017–R3071**, including **53** headings/claims/roles/converse/marginal annotations within Chapter LII, **one** additional unit for the Chapter LIII boundary and **one** printed marginal forward reference. All remain `accepted=false` and `runtime_promoted=false`. [The exact role counts are machine checked, not assumed in this prose; if inconsistent use the JSON.]

The precise scoped claims deliberately retain (1) conditional AND/OR, (2) separately printed direct, exception and converse clauses, (3) the first/seventh and second/eighth houses' party-direction, (4) Moon separating from one planet versus applying to another, (5) variable strength in war questions versus other questions, and (6) sign modality in the neighbors' duration paragraph. **Three literal `& e contra` phrases** in Chapter LII are preserved as abbreviated printed converses, not expanded algorithms. Two genuine source crossings (403→404 prose and 404→405 heading) are explicit. The printed side-margin promise is a documentary reference, not a separate predictor.

Original scan hashes, rendered-pdf scan hashes, boundary and source classifications are in `SOURCE_WINDOW_MANIFEST.json`. First draft was frozen byte-identically in `recovery/SOURCE_FIRST_CLAUSES_INITIAL_20261015.json` before annotating the margin as a source unit. Exact effect and SHA recorded in `SOURCE_FIRST_CORRECTION_RECEIPT.json`.

## Remaining B02x editorial acceptance gap

This is a *source-first preliminary extraction*, **NOT Chapter LII source acceptance**. The next worker should make a fresh original-page-to-record independent coverage map (including all original clauses and headers/margin), verify complicated p403 legal and p404 moving alternatives, review p405 upper conditions, freeze each new edit's before bytes, run source tests and archive extracted replay before documentary admission. Confirm no Chapter LIII body crossed the printed divider. Then update canonical index non-force only after record completeness is established; user approval not needed for routine source study. Do not use p406's later legal question as justification to retroactively change LII's physical extent.

No empirical cases, out-of-sample astrology validation, predictive model, personal chart, criminal/health/legal claims, runtime chart score or owner survey answers were changed in this draft.
