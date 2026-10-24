# C24 Hellenistic source-research continuation — Florence commentary paired glyphs

**Checkpoint date: 2026-10-24. Main owner outcome OPEN.** Continue reconstructing ancient/early Byzantine astrology texts and comparing source-defined variants as part of the cross-tradition `humandesign` research map. Later freeze admissible models *before* collecting untouched, blinded human response data. **Human predictive validations: 0.** Unit tests count source-code invariants, not scientific accuracy on people.

## Mandatory authority recovery and branch constraints

Read the live current default branch `u-dont-existDOTcom/universal-dev-architecture/AGENTS.md` and `LESSON-INDEX.md`, then `u-dont-existDOTcom/humandesign/AGENTS.md`, then this checkpoint and [C24 primary-source report](HELLENISTIC_SOURCE_C24_FLORENCE_COMPLETE_PAIR_COLLATION_20261024.md). Do **not** re-acquire/redo C01–C23 research or overwrite previous negative cases. Never use Work to extract the owner's purchased Gansten `Primary Directions` Kindle edition, fit a source reading to known life events, or merge disputed rules into production scoring.

- Parent research C23 `research/astro-hellenistic-c23-commentary-ms-20261024`, SHA `139f980041e16ab2710cc85b8c3eb7180576aba6`.
- C24 **isolated worker branch** `research/astro-hellenistic-c24-commentary-collation-20261024`, writer-owned only. The original integration branch `research/astro-missing-book-audit-20261022` remains the integrator's, not a shared mutable writer target.
- All work saved to `docs/astrology-research-map/`; top `README.md` points to C24. No image files or copyrighted manuscript photographs committed.

## New C24 original manuscript source work

Re-examined the same **fourteenth-century Florence BML Plut. 28.14, handwritten folio 204v**, which C23 first located. Official original image `https://cdm21059.contentdm.oclc.org/iiif/2/plutei:565809/full/full/0/default.jpg`, **2536×2572**, **741,471 bytes**, SHA256 `52a1b8b4f8d67514c815a56178d54c1d45e03a991a09b48417f599ff3336128e`. Manuscript rubric: *canon of triplicity monomoiriai* (Greek approximate normalized lettering). Four zodiac triplicity columns with **30 red-numbered ordinal-degree rows each and two paired planet symbols per row**. Surrounding original Greek source photographed f204r and f205r was inspected at C23 but no definite independent day/night abbreviation gloss was established at C24.

C24 cropped *every degree row* with its red ordinal index and four column originals; linked approximate y-centers in source register, and manually normalized planet glyphs across all rows. **240 provisional values** (120 first slot, 120 second slot) are preserved as two stages, retaining source uncertainty:

- **Stage A** [120 first + 80 second, with 40 original nulls](PAULUS_C24_COMMENTARY_120_FIRST_80_SECOND_SOURCE_V1.json).
- **Stage B** [remaining 40 second glyphs, source literal arrays stored separately](PAULUS_C24_COMMENTARY_FULL_SECOND_120_V1.json). Stage A data/unknowns are preserved as an historical bounded read; the separate Stage B comparator verifies continuity without silently filling earlier nulls.
- Both were visually normalized by the **same reader with prior C04/C05 model patterns already known**. Thus the striking perfect matches are **NOT blind independent palaeography**; use the counts as *candidate glyph read consistency*, not as demonstrated textual authenticity or ancient authorship. Selected row seams flagged with low confidence.

## Main finding 1: first-slot whole 120 favors a source-specific mixed trigon arrangement

The fully entered first slot exhibits **sevenfold recurrence in each trigon**, but different first-seven orders. Comparing to unchanged frozen C04 Greenbaum editor-corrected day, C05 Greek day narrative, and the separately photographed C15 Paulus manuscript family:

| First-slot provisional photo table vs source model | Agreement |
|---|---:|
| C05 narrative day | **104/120** |
| C04 Greenbaum corrected D | **102/120** |
| Older photographed Paulus table family | **20/120** |
| First-slot cell matching neither C04 nor C05 day | **0** |

**Fire and earth first slots: 30/30 agree with both C04/C05. Air: 30/30 matches C04, only 14/30 C05. Water: 30/30 matches C05, only 12/30 C04.** Thus the 34 original *disagreements between C04/C05* split across this commentary source **18 C05-only + 16 C04-only + 0 neither**. This is a manuscript-family variant, not an invitation to build a trigon-hybrid predictive model or a demonstration of historical correctness.

The older C22 first-source comparison was **12 both/11 narrative/1 corrected/96 neither**, covering a different 120-cell *Paulus* manuscript family; it remains unchanged. Its stronger disagreement must not be averaged with C24's 120 candidate commentary labels. Neither is human validation.

## Main finding 2: second slot pairwise exchange across all 120 entered symbols

**120/120** candidate second-slot values equal the neighboring first-slot value in each ordinal **degree pair** (1↔2),(3↔4),…,(29↔30). The coding checks that *after* reading registered literals rather than using this formula to fill nulls. It is a **manuscript-description hypothesis** that may explain paired source notation; the physical table's own precise day/night abbreviations have **not** been unequivocally translated.

The second slot matches C05's separately reconstructed **nighttime sevenfold narrative only 48/120** (fire 14/30, earth 14/30, air 6/30, water 14/30). Example negative: Fire degree 7 manuscript first Mars, second **Sun**, while C05 night narrative would require **Mars**. Hence night-sect attribution of the second slot cannot be assumed to license production use of the old C05 night function, and conversely the pair-swap formula cannot be promoted as a new night model.

Crucially, Stage A retained 40 second-slot unknowns during initial collation and did **not** fill them algorithmically. Stage B separately entered those rows from visually examined original image strips. All 240 labels remain **provisional** and subject to independent verification; some late rows have lower glyph confidence.

## Technical artifacts and exact verification

- [C24 source research report](HELLENISTIC_SOURCE_C24_FLORENCE_COMPLETE_PAIR_COLLATION_20261024.md).
- [Stage A 120 first/80 second](PAULUS_C24_COMMENTARY_120_FIRST_80_SECOND_SOURCE_V1.json).
- [Stage B 120 second slot readings](PAULUS_C24_COMMENTARY_FULL_SECOND_120_V1.json).
- [Stage A research-only compare](paulus_c24_commentary_120_first_80_second.py).
- [Stage B research-only full 240 compare](paulus_c24_complete_240_source_comparison.py).
- [13 Stage A tests](test_hellenistic_c24_commentary_canon.py) and [9 Stage B tests](test_hellenistic_c24_second_slot_full.py).
- `README.md` most recent checkpoint.

Run:

```sh
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_c24_*.py' -v
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v
```

**C24 full historical-source suite VERIFIED: 228/228 PASS, exit 0**, on isolated C24 branch (206 prior and 22 new). The 22 focused tests passed as well. **0 human predictive validations.**

## What is still scientifically open — exact next executable actions

1. Independently decipher the **f204r introductory explanation and f205r following Greek**, especially abbreviations identifying the two within-row planets. Confirm if the table means day/night, sex/sect light, paired alternatives, or other notation. Verify glyph classification via independent blind palaeography if feasible; ordinary source tests only check *our* stored readings.
2. Check actual **Boer 1962 critical Greek commentator figure and apparatus** against this photographed original and its siglum. Original printed edition not yet opened; adjacent translation/excerpts or a library catalogue are not a substitute.
3. Compare with at least one genuinely distinct *commentary* manuscript rather than treating three previous dependent Paulus tables as independent authorial evidence. Source candidates: Leeds Brotherton MS 31; Madrid Mss.27 catalogued in Pinakes, subject to legitimate access and section identity.
4. Check **Jones 1999 vol II pp421–427** for the original Oxford P.Oxy.4277 Greek monomoiria letter forms; original two Oxford images are already authenticated in C17 and need not be fetched again. Maintain the prior **1/3 match, 2 mismatches** without retuning.
5. Keep Epitome §37/44 Greek variant corrupt numerals open. Preserve zero untouched human prediction status until real preregistered concealed questions/predictions/answer freeze.

**Resume one-liner:** C24 has 240 provisional paired glyphs from Florence commentary Plut.28.14 f204v; first120 appears mixed sevenfold by trigon (C05=104, C04=102), paired second120 exhibits adjacent-degree exchange 120/120 but does NOT reproduce independent C05 night (48/120); no source-night rubric or blind glyph certification yet. All old sources and negative cases preserved; no scoring promotion.

## C25 later source-lineage advance — Vienna A is not automatically the same table

**Vienna ÖNB Cod. phil. gr. 115**, official IIIF canvas 418, photographed folio **205v**, was newly located and inspected in C25, in the attributed commentary passage used as a main witness by Boer 1962. It has a visibly different **red-numbered table layout**: provisional degree numerals **1–15 alongside 16–30**, apparently in fifteen paired rows per sign-group section, plus an Aries-marked adjacent panel of unknown function. In C24 Florence Plut.28.14 folio204v, by contrast, two provisional planetary glyphs were read at **each same ordinal degree**, and their day/night meanings were still unverified. **Do not treat Vienna's paired numbers as equivalent to Florence's presumed daytime/nighttime planet slots, or assume this is necessarily the exact same monomoiria canon until original Greek headings are deciphered.** C25 admits **zero Vienna planetary degree–ruler assignments**, preserves all C24 240 provisional annotations, and records conflicting official/scholarly Vienna manuscript datings. [C25 direct primary-source report](HELLENISTIC_SOURCE_C25_VIENNA_BASE_F205V_20261024.md) and [C25 handoff](HELLENISTIC_CONTINUATION_C25_20261024.md).
