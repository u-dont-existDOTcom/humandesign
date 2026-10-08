# HumanDesign astrology source audit — new-conversation handoff

## Instruction to the next conversation
Continue the source-complete astrology/numerology methodology work in `u-dont-existDOTcom/humandesign`, integration branch `research/six-rule-life-timing-20261001`. GitHub is canonical. This handoff follows the owner's explicit request to continue and provide a conversation handoff after interrupted turns. Continue substantive execution; do not ask for personality data or repeat completed reading.

First fetch the LIVE DEFAULT-BRANCH `AGENTS.md` and `LESSON-INDEX.md` from `u-dont-existDOTcom/universal-dev-architecture`. Activate only applicable current patterns. Then fetch HumanDesign's current `AGENTS.md`, relevant `ARCHITECTURE.md`, and **`state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md` on the integration branch**. Reconcile this handoff with newer repository evidence; newer verified work takes precedence. Use the current UDA timestamp/clock and delivery rules. Do not assume a previously failed transport is currently unavailable.

## Parent goal and current state
The owner wants a deep, source-grounded framework that stops discovering consequential rules only after seeing someone's outcomes. All important retained rule families must remain discoverable. Source-complete extraction, cross-source reconciliation, reproducible computation, development fitting and untouched validation are distinct stages. The owner permits multiple passes and later development fitting; fitting is not independent validation.

Task root: `tasks/astro-source-audit-multipass-20261005/`.

Completed and retained:
- **Ptolemy, Tetrabiblos, Robbins English edition:61/61 sections, 1,066 source records**, including both Book IV endings and identified English notes. Nineteen batches are located by `PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json`. Do not restart it. This is English reading/extraction, not a complete executable predictive system.
- **Lilly, Christian Astrology1647, Book I chaptersI–VII:B02a,91 records**, printed 25–56/PDF 59–90; preface method and opening contents also read. Prior research revision67673a9; subsequent receipt commits are retained.
- **Lilly Book I chaptersVIII–XIV:B02b,139 additional records**, printed 57–83/PDF 91–117, including the final Head/Tail passage. Seven planet profiles, fourteen conditional manners branches, sixty raw term rows and thirty-six raw face rows. **Lilly cumulative 230; Ptolemy + Lilly 1,296.** Records include definitions, catalogues, qualifications and audit observations; they are not independent predictions.
- Previous failed B02b turns had left a clean worktree and reusable source text/images but no published B02b extraction. This continuation recovered those assets, completed the extraction and tests, and prepared this handoff. Read current publication receipt for exact commit/status rather than assuming a prepublication label is current.

## Exact next reading action
**Start Lilly chapter XV: “Another briefe Description of the shapes and formes of the Planets,” PDF 118 / printed 84.** The heading was located, but XV has not been extracted or counted complete. Continue through the remaining Book I foundation material in coherent source batches. Use actual headings and page images: later XVI numbering is duplicated/ambiguous, so numerical chapter increments alone are unsafe.

Do not rereadI–XIV except for a named cross-reference or correction. Keep Book II horary and Book III natal rules separate. An I–II-only derivative cannot replace the full three-book witness. The five selected Lilly rules in the old six-rule model do not constitute a full Lilly audit.

## Source identity and recovery
Active source basename: `Lilly-1647-Christian-Astrology-I-III.pdf`.
- William Lilly,1647, Wellcome witness `b30338724`.
-894 PDF pages;141,842,963 bytes.
-SHA256:`2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`.

The authorized owner-computer astrology source directory contains this already downloaded file. Recover its route from the existing source-acquisition/file-verification receipts and authorized filesystem tools; verify the hash. Existing searchable text plus original page renders worked. No new OCR was needed. Some existing text loses lines, glyphs and digits; verify load-bearing tables and ambiguous text against images rather than trusting OCR.

`reference/research/ASTROLOGY_SOURCE_ACQUISITION_V2.json` contains the qualified acquisition identity and public source route. Prefer the existing local copy, not another download. The catalog's missing-final-leaf warning remains unresolved; do not equate this with a missing opening chapter. Rhetorius's copy-specific missing pages are already acknowledged by the owner; retain the supplement/OCR aid and do not restart that dispute or request another upload.

## B02b artifacts and crucial findings
All paths below are relative to the task root; B02b files are ordinary inspectable files, not only archive chunks.

`batches/B02b/RULES.json`, `PLANETS.json`, `TABLE_AUDIT.json`, `READING_RECEIPT.json`, `TEXT_IMAGE_CHECKS.json`, `UNRESOLVED.json`, `CROSS_SOURCE_COMPARISONS.json`, `lilly_planet_reference.py`, its tests and `REPORT.md`. `LILLY_SOURCE_EXTRACTION_INDEX_V1.json` links both Lilly batches and their hashes. `CURRENT_PASS.json` and `PASS_PLAN.json` now agree with the primary state, including formerly stale Ptolemy-only next-step fields.

Preserve these distinctions:
1. **Well dignified is not uniformly pleasant or morally good.** Mars's well branch remains contentious; the Moon's remains timorous/prodigal; Venus's retains aversion to labour. Relevance and condition are external requirements, not determined merely by a planet being present.
2. **Raw degree lists conflict with the later table.** Gemini21 has no term owner; Mercury's Leo/Virgo labels create more gaps/overlaps. Venus's final face is printed Pisces1–10, overlapping Saturn and leaving Aquarius1–10 empty. There are25 problematic term cells and20 problematic face cells. LaterPDF 138 differs, but was only targeted for comparison—not fully audited or silently substituted. Ordinal1–30 and modern exact angular endpoints remain distinct.
3. **Nodes: author versus reported tradition.** Lilly's preferred Head lessens malefic harm; preferred Tail increases it. The doctrine he attributes to ancients instead makes Head evil with malefics and Tail good with malefics. Holden's Latin-supplied sixth consideration of Rhetorius 54 resembles the latter; it is not Greek-source unanimity or independent empirical confirmation. Tail-benefic obstacles are not guaranteed failure; angularity AND essential fortification qualifies the failure report. No calibrated multiplier follows from “doubled and trebled.”
4. **Slow Moon is an analogy, not physical retrograde.** Strictly below 13°10′/day is the cited threshold; stated mean 13°10′36″ is different. Preserve physical direction.
5. **Distinct roles and frames.** Mercury gender follows conjunction; broader assimilation uses aspects. Solar orientality refers to the figure, not Sun relative to itself. Four year categories, gestational months, age analogies and orb radii are not one timing system. Per-planet orbs here do not define pair aggregation.
6. **Source discrepancies are recorded, not repaired from memory.** Mars printed age 41–56; mean-motion body/erratum differ. Venus latitude2°02′ versus8°36′ occurs in one paragraph. Saturn mean 43½ in the table versus43 in the prose. Natural friendship declarations can be asymmetric.

## Verification and boundaries
New B02b reference suite:46 tests; retained B02a suite:105 tests. Check `VERIFICATION.json` and host logs for the additionally executed methodology tests and exact aggregate. Duplicate reruns are not new distinct checks. These tests cover source data, caller-qualified lookups, three-valued unknown handling, strict thresholds, raw table conflicts and record integrity—not astronomical parity, independent semantic review or predictive validity.

Portable batch command:
```sh
python3 -m unittest discover -s . -p 'test_lilly_planet_reference.py' -v
```
Run from the B02b directory. No third-party dependency is required.

## Research safeguards and next stages
Do not inspect Hale's history, personality, surveys or LifePatterns answers during source extraction. Earlier person predictions remain frozen; no model or runtime has been promoted by these source batches. Source-specific medical, sexual, religious, ethnic and moral classifications are historical claims, not modern diagnoses or facts about a person. Keep source wording, paraphrase, translator explanations and analyst inference distinct.

Before any later person-specific reading, load the current person-life index AND consolidated catalog, give every must-consider family a disposition, and apply the V2 deep-analysis protocol. The six-rule model was selected on Joel's case and is not a validated generic personality score. Numerology must retain its frozen conventions. Any strong fitted ruleset must be retained with misses, false positives, transfer results and exposure status; never alter an old freeze in place.

Remaining corpus order is in PASS_PLAN: complete Lilly; Hellenistic Valens/Dorotheus; medieval definitions and annual synthesis; Phaladeepika/BPHS-Sharma/BrihatJataka; timing companions and other available books. Missing optional books do not block available ones. Reconciliation must distinguish agreement, contradiction and dependent reuse before executable model changes and later untouched evaluation.

Save each meaningful completion in humandesign with source anchors, actual tests, an exact next checkpoint and an ordinary-file handoff. Use an isolated workspace and nonforce integration; never reset another worker's checkout. Source books stay outside Git. No background execution or automatic Downloads placement is implied by this handoff.
