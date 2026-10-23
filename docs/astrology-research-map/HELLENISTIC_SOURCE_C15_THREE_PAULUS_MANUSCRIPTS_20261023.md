# Hellenistic source C15 — third authentic Paulus manuscript grid, Vatican 1542 versus Florence and Munich

**Date:** 2026-10-23. **Scope:** primary-source transmission, not empirical astrology validation. **Zero human predictive validations; no production model changes.** Continues directly from C14 (base `2786d31048850e2c246029a77041813f8f523c23`) without restarting earlier source work.

## 1. Newly opened primary material

The **Biblioteca Apostolica Vaticana** preserves a 1542 Greek codex **Vat. gr. 1444**, with the Paulus Alexandrinus *Introductio in apotelesmaticam artem* catalogued on folios **176–207** (Pinakes). Its 286-opening public digitization has IIIF manifest:

`https://digi.vatlib.it/iiif/MSS_Vat.gr.1444/manifest.json`

Inspected **digital opening 0202**, whose **left-hand page** has the four-triplicity monomoiria table and accompanying Greek text; the right-hand page is visually numbered **202**. This is a **digital opening identifier**, not an independently verified left-side manuscript folio number.

Exact Vatican image request and photographic integrity:
- Source image: `https://digi.vatlib.it/iiifimage/MSS_Vat.gr.1444/Vat.gr.1444_0202.jp2/full/full/0/default.jpg`
- IIIF image metadata: **2368 × 1814 px**.
- Returned source JPEG: **609,948 bytes**, SHA-256 **`de6fc8f48e57b4b339037805618743e151945e505e162fd3b2168a4a6f9c9f1e`**, HTTP 200 on the authorized machine.
- Source inspection: high-resolution original study image, focused enlarged crops for **degree bands 1–10, 11–20, 21–30**. I also fetched and viewed a 41-opening contact-sheet study window (Vatican images 174–214) to locate the figure without mistaking another tabulation for it.
- **No source photographs saved to Git.** BAV restricts reproduction; original consulted for personal study and new manually derived numerical observations only.

This establishes a **third physical handwritten witness** to compare with: (a) fourteenth-century Florence BML **Plut. 28.7 folio 168v**, whose full-colour diagram was directly examined in C14, and (b) sixteenth-century Munich BSB **Cod. graec. 170 manuscript p65**, whose printed-photo glyphs were read in C13. Distinct **physical** copies must not be conflated with independent ancestral textual traditions.

## 2. Source-first manual Vatican transcription and three-way agreement

Independently recorded **120 provisional degree → planetary glyph assignments** from the Vatican photographed table into [C15 image-only witness](PAULUS_C15_VATICAN_120_POSITION_SOURCE_WITNESS_V1.json). Manuscript groups are the four **fire/earth/air/water trigons**, each listing the same three zodiac signs per column as the prior manuscripts; the planet key uses shapes on the image. No source cells were invented by a sevenfold or eightfold model; reproduction is limited to manually annotated planetary labels and provenance, not images or extended text.

Independent comparison code loads the original unaltered C13 Munich and C14 Florence source registers and computes:

| Source-fidelity comparison | Count |
|---|---:|
| Vatican photographed positions provisionally read | **120/120** |
| Vatican vs Florence matching positions | **120/120** |
| Vatican vs Munich matching *readable* positions | **119/119** |
| Contradictory readable Vatican–Munich positions | **0** |
| Munich unresolved source glyph (must remain null) | **Earth degree 28** |
| Vatican & Florence at that corresponding location | **Mars** |

The earlier Munich unknown is **not** upgraded retroactively. It is possible, but not independently established, that the Vatican 1542 scribe and Munich's sixteenth-century scribe drew upon Florence's lineage or another shared exemplar. The extreme concordance actually makes **textual-family independence less obvious**, not more. No ancient author autograph or originally intended planetary assignment algorithm has been proven.

## 3. Negative cases and the 34 discordances remain

The Vatican table preserves the same specific counterexamples seen in Florence:

- Fire and air: **0** deviations from simply repeating each column's first eight values.
- Earth: **degrees 28–30** depart from that naïve extrapolation, with the directly read Vatican values **Mars, Mars, Jupiter** (including consecutive Mars labels).
- Water: **all degrees 9–30** depart from the naïve extrapolation; notably Vatican water d8 = **Mercury**, d9 = **Mars**, d10 = **Sun**.
- Total differences from naïve eight-position repetition: **25 of 120**. A repeated eightfold formula is therefore **not** an acceptable stand-in for the literal table, even though its first octet looked promising.

Within the **34 pre-existing** C05 Greek-narrative-sevenfold versus C04 Greenbaum-corrected-day discrepancies, the source-only Vatican reading gives **11 aligning with narrative only; 1 aligning with Greenbaum only; 22 aligning with neither**. The same distribution appears in both Florence and Munich. The one corrected-print-only source cell remains **air degree 27 Venus**; the source negative **water degree 8 Mercury** agrees with neither the C05 Venus nor Greenbaum Mars. **These are internal textual classifications, not success/failure predictions of people.**

Three concordant manuscripts indicate **a stable transmitted diagram** in this family; they do NOT resolve which competing *intended method* Paulus originally prescribed or whether the hand-copied table reflects later adaptation, an annotation or a misinterpreted eight-position sequence. Critically, the Greek rubric's sect is **still inferred**, not securely established by a separate palaeographic transcription. No variant is promoted into production scoring.

## 4. Additional access investigations and exact limitations

- **13th-century Paris BnF Grec 2506** is catalogued as including Paulus, in part on ff. 177–184 (Biblissima/Pinakes) with Gallica object `https://gallica.bnf.fr/ark:/12148/btv1b10722216r`. Direct IIIF `.../manifest.json` and public page requests returned **HTTP 403** on the authorized research machine; a distinct BnF presentation API route returned **HTTP 404**. **No images inspected; no claim that a monomoiria table exists in that excerpt.** The date and content are catalogue evidence, not a textual witness read. Do not treat a 403 as proof that the user lacks general access via an interactive authorised library browser.
- Vatican **Vat. gr. 1314** (catalogued fragment from **1449**, ff. 140v–145v), its actual official IIIF manifest was obtained. **17 double-page thumbnails covering digital openings 136–152** were visually inspected. No clearly recognizable complete four-trigon ×30 table was seen in that inspected window; this is **not** evidence it does not appear elsewhere or that its excerpt contradicts the longer manuscripts. No source-value comparisons admitted.
- **Boer 1958 Paulus critical edition** and **Boer 1962 attributed Heliodorus commentary**: specific Greek plates/editorial apparatus remain **uninspected** in C15. Bibliographic confirmation/Greek digital corpus indices are leads only; the figure is not magically reconstructed from secondary catalogues. Keep their manuscript-siglum lineage unresolved.
- **P.Oxy. LXI 4277**: the official Oxford SDS portal identifies its papyrus imaging collection, but the portal's automated public search returned unavailable/HTTP202 empty-body from the research machine (the browser-oriented search returned HTTP403). No verified **full original object photograph** inspected. Cristian Tolsa's 2017 paper reports selected EES-authorized closeup photographs in figures 1–3; that bibliographic fact does **not** imply this session visually inspected the whole papyrus, and no source-level upgrade is claimed. Retain C05's printed scholarly interpretation **1/3 matching monomoiria allocations and 2 negatives**.

## 5. Reproduction and restrictions

- [C15 Vatican 120-cell visual source witness](PAULUS_C15_VATICAN_120_POSITION_SOURCE_WITNESS_V1.json).
- [C15 triple witness comparison](paulus_c15_three_manuscript_comparison.py): separately loads C13/C14 source records; source comparison is not source selection.
- [C15 source regression tests](test_hellenistic_c15_vatican_third_witness.py): exact image provenance, first-eight fixtures, 120/120, 119/119 and retained Munich null, 25 negatives, 34 positions and zero production/human predictions.
- See [durable C15 handoff](HELLENISTIC_CONTINUATION_C15_20261023.md).

Command: `python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v`. **C15 verified historical-source regression: 122/122 PASSED (exit 0)** from the isolated C15 worktree, after adding 12 C15 tests to the prior 110. These remain *source/transcription arithmetic tests only*, not untouched human prediction tests. Even green tests cannot independently authenticate the photographs' hand-transcribed glyphs; a fourth differently descended manuscript or Boer variant apparatus is needed before choosing an ancient rule. No Amazon *Primary Directions* purchased Kindle extraction using Work, no biographies, production scoring, paid actions, copyrighted full image redistribution or cross-tradition map replacement.

**Next source frontier:** actually examine Boer 1958/1962 apparatus for Florence/Vatican/Munich families or a differently descended Greek manuscript, verify a standalone BnF Grec 2506 original image through lawful access where available, and recover the exact authenticated Oxford P.Oxy. 4277 image. Preserve unknowns and original historical negatives.
