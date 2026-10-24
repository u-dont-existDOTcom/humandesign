# C22 — durable Hellenistic source-reconciliation continuation

**2026-10-24. Main user outcome OPEN.** Continue original-source research toward an accurate, source-typed 16-tradition `humandesign` astrology framework, and later independently freeze and prospectively evaluate predictions on untouched real humans. **Human predictive validations: 0; source arithmetic/provenance tests are only engineering/historical evidence.** No production scorer changes, no known-biography variant selection.

## Recover live authority and checked branch

Read live `u-dont-existDOTcom/universal-dev-architecture/AGENTS.md`, `LESSON-INDEX.md`, then `u-dont-existDOTcom/humandesign/AGENTS.md`, then this and [C22 full research report](HELLENISTIC_SOURCE_C22_FULL_120_RECONCILIATION_20261024.md).

- Base accepted **C21**: `643290a22ec7084cd61b26a352e90f7abc9e8a73` on branch `research/astro-hellenistic-c21-paulus-greek-20261024`.
- C22 isolated worker branch: `research/astro-hellenistic-c22-full120-comparison-20261024`. Do not merge directly to production or take over the integrator-owned `research/astro-missing-book-audit-20261022` branch.
- C22 files: [original-source review](HELLENISTIC_SOURCE_C22_FULL_120_RECONCILIATION_20261024.md), [machine-readable provenance and category expectations](PAULUS_C22_COMPLETE_120_SOURCE_COMPARISON_PROVENANCE_V1.json), [fully deterministic 120-row comparison](paulus_c22_120cell_source_comparison.py), [12 source-only tests](test_hellenistic_c22_full_120_source.py), and updated `README.md`. English original PDF study image not redistributed.

## Actual new evidence and corrected framing

1. **Directly rendered and inspected owner's Greenbaum translated source PDF leaves 82–86 (print pp66–70)**, original SHA256 `dffa2a86e2a8c13135b1fc9e68b798224a25464e617fa221a7551b5be08b605a`. Ch32 translation note says Greek edited diagrams have errors and that duplicate Venus must not be assigned before other planets. The 30×4 **editorially corrected diurnal table** on printed p67 was directly checked in sample cells. Pp68–70 provide positive contradiction evidence: one version uses **Mars-first fourth trigon**, a conflicting **Olympiodoran scholion has Venus at Cancer ordinal d8** while corrected canon has Mars, and some scholion numbers differ (Moon in Virgo **19 vs 23**, earth d22 Venus vs Mars). These are translation/editor notes and different witnesses, not an authenticated original Boer 1958 apparatus.
2. **Full 120-position source comparison** corrects narrow prior reporting: **34/120** means the two day sevenfold reconstructions disagree *with one another* at 34 cells; it is NOT all observed manuscript discordance. Against previously stored 120-value Vatican/Florence glyph family, counts by category are **both 12, narrative only 11, Greenbaum corrected D only 1, neither 96**. Thus **day narrative agreement 23/120**, **printed Greenbaum agreement 13/120**; *night narrative diagnostic* also **13/120**. Unchanged old disputed-34 subset **11/1/22**; remaining 86 shared day predictions **only 12 match both / 74 match neither**.
3. **Manuscript reliability caveat:** Three photographed physical books are not shown to descend from distinct stemmata. The later planetary-symbol labels were coded in the same research context after earlier patterns were visible, **not independently blinded by separate palaeographers**. The 120-values are candidate photographic transcriptions (Munich only 119 legible, earth 28 null). Their perfect 120/120 shared labels cannot be treated as proven blind photographic accuracy. The manuscript's own unambiguous **day/night table rubric** remains not independently deciphered; all Sect comparisons are exploratory.
4. **Numerical chronology/papyrus evidence unchanged:** Oxford P.Oxy.4277 original photographs authenticated C17, 3 scholar-reported monomoiria comparisons remain **1 match / 2 mismatches**; original three name glyphs not independently recollated against Jones 1999. Berlin P. Berol.21347 four reconstructed degrees (2/9/16/23) not uniquely decided from ink. Hephaistio §37/44 corrupt numbers preserved. No source variant promoted by known biography.

## Exactly what is still OPEN

- Obtain **Boer 1958 critical Greek page 85 and chapter-32 diagram/apparatus** to trace the *actual edited source literal* and Greek manuscript variants. This pass did **not** read that critical apparatus. The public DOKUMEN page returns a title-page/preface OCR fragment but not the chapter-32 apparatus; the Greek Library listing has Boer TLG 2053.001 but site timed out on authorized workstation in C22. A URL timeout is not proof the actual edition has no readable pages.
- Obtain **Boer 1962 Greek Olympiodorus chapter34** and the complete unabridged Greenbaum translation's commentator/addendum; the available local **93-leaf** PDF ends with printed p77 and omits that later commentator section. Do not claim translation or source lacks it.
- Inspect Paris **Z** and **Y** genuinely independent manuscript readings, or engage independent qualified palaeographic reading of source diagrams, and correlate with the printed apparatus. Do not replace the three original photographed witnesses with modern mathematically generated values.
- Complete Jones 1999 vol II pp421–427 papyrus Greek editorial restoration checks using existing Oxford photographs.
- After rule versions are separately frozen and comparisons pre-registered, apply prospective blinded human validation. There are **ZERO untouched human predictive results** in this Hellenistic lane.

## Verification commands

```sh
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_c22_*.py' -v
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v
```

**Verified C22 full historical-source suite: 194/194 PASSED, exit 0** on the isolated C22 research worktree (182 retained source regressions + 12 new source-only checks); focused 12/12 also passed. **0 real-human predictive validations.** The production scorer/cross-tradition map remains untouched.

**Next precise action:** independently collate the original Boer 1958 Greek chapter-32 chart/apparatus and qualified manuscript readings; do not claim resolving the 120 source divergences merely by increasing test counts. Do not use Work to extract the owner's purchased Gansten `Primary Directions` Kindle ebook.

## Later C23 original commentary manuscript advance

The next source batch directly located an *additional*, different **fourteenth-century Greek commentary manuscript** rather than reopening the three C13–C15 Paulus-source photos: **Florence BML Plut.28.14, folio 204v**, photographed original and surrounding f204r/f205r examined through official IIIF. Its red rubric names a *canon of trigon monomoiriai*, with **four triplicity columns and two glyph assignments per ordinal degree**. The first **eight** provisional first-slot planet names per triplicity are separately recorded in [C23 witness](PAULUS_C23_FLORENCE_COMMENTARY_204V_FIRST_EIGHT_V1.json) and [C23 report](HELLENISTIC_SOURCE_C23_COMMENTARY_GREEK_CANON_20261024.md). In those *32 new, unblinded provisional* commentary cells the C05 narrative matches **28**, Greenbaum's corrected D **27**, and the older C15 manuscript family **16**. Of the nine previously disputed early cells, four air positions favor the corrected D reading and five water positions favor narrative; the commentator's Cancer ordinal degree 8 first slot looks like **Venus**, whereas C22's earlier Paulus-table family gave **Mercury** and Greenbaum's corrected canon gave **Mars**. C22's original **120-cell** results remain unchanged, and the new commentary's unread **9–30** positions must not be generated from a formula. Boer critical apparatus and manuscript sect/glyph authentication still OPEN; zero human predictions.
