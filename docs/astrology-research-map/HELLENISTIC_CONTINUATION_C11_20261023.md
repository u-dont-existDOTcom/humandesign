# Hellenistic source continuation C11 — durable verified research checkpoint

**Date:** 2026-10-23. **Human predictive validations:** 0. **Research objective:** OPEN. **Source-only arithmetic/provenance regression:** 77/77 PASSED after fixing C10 false-green fixture and adding 10 C11 tests; no merge/release and no scoring changes.

## Rebootstrap and branch topology

Always read live `u-dont-existDOTcom/universal-dev-architecture/AGENTS.md`, `LESSON-INDEX.md`, and `u-dont-existDOTcom/humandesign/AGENTS.md`; then this checkpoint and the C11 report. Do not restart C01–C10, do not infer truth from merely green arithmetic tests, do not use previous personal biographies to choose any historical reading.

Original research parent: `research/astro-missing-book-audit-20261022`; isolated parent C10 branch `research/astro-hellenistic-c10-greek-20261023` commit `f8d7999b3080793b90002ffe935f91e0a3d945c0`. New isolated branch `research/astro-hellenistic-c11-recension-20261023`. Keep writes isolated, review before integrating; preserve all other source lanes and source-to-test maps.

## C11 resolved from previously untouched comparison (source-corrective, not predictive)

1. **C10 FALSE-GREEN TRANSCRIPTION ERROR:** In Pingree Epitome IV §37 edited Greek printed p241, Sun→Sun is **`πγ=83`**, not claimed C10 `πν=130`. Epitome Sun vector `[104,52,64,83,30,80,118]` sums **531**, not 578; nominal 570 gives **−39**, not +8. Corrected C10 JSON + test + report + checkpoint in C11 branch, with explicit supersession; Git preserves C10 earlier wrong commit.
2. **No Venus overcorrection:** Main Pingree Hephaistio II.29 Venus→Sun **36** agrees with Epitome IV §37 **36**; the separate main Sun→Venus **35** was initially mistaken for the opposite direction. No Epitome Venus reduction adopted: Epitome row sum **213**, main Greek sum **243**.
3. **Seven paired Greek rows in one register:** [C11 literal comparison](HEPHAISTIO_C11_MAIN_EPITOME_AND_MUNICH_MANUSCRIPT_WITNESS_V1.json). Main 1973 totals Saturn **914**, Jupiter **365**, Mars **450**, Sun **569**, Venus **243**, Mercury **606**, Moon **764**. Epitome 1974 totals **734, 365, 460, 531, 213, 607, 764/794**. These related recensions are *not independent authors or humans*. The Saturn→Mercury three-way printed **40**, derived **140**, printed main **150** persists; Epitome Moon→Sun **115/145** remains unresolved.
4. **Breakthrough original manuscript photo:** Bayerische Staatsbibliothek **Cod. graec. 170**, catalogued early-modern (Paulus with scholia and figures pp27–73), public IIIF 274-image digitization. **Manuscript handwritten p65 / BSB image 00081** was actually viewed, shows four monomoiria columns with **Aries, Taurus, Gemini, Cancer** headings, degree numbers and planetary signs. Direct photo URI `https://api.digitale-sammlungen.de/iiif/image/v3/bsb00131007_00081/full/max/0/default.jpg`; manifest `https://api.digitale-sammlungen.de/iiif/presentation/v3/bsb00131007/manifest`; Pinakes `https://pinakes.irht.cnrs.fr/notices/oeuvre/8855/`. **First-degree glyph suggestions are provisional**, not certified planet mappings. Greek rubric, **day/night sect**, calendar/unit method, and 120 cells **NOT** collated; **none** of the historical 34/120 Greenbaum-vs-narrative differences admitted resolved yet. A later manuscript is not an ancient author's autograph. Images remain outside Git.
5. P.Oxy. **4277 original image still unavailable/unverified**; C05 published Tolsa/Jones source comparison **1/3** remains, **2 mismatches** preserved. Boer **1958/1962 actual Greek diagram** still not directly examined.

## Saved C11 artifacts and modified files

- `HELLENISTIC_SOURCE_C11_GREEK_RECENSIONS_MUNICH_MS_20261023.md`: full corrected report, source locators, edited-Greek seven parent comparisons, independent manuscript discovery and remaining evidence gates.
- `HEPHAISTIO_C11_MAIN_EPITOME_AND_MUNICH_MANUSCRIPT_WITNESS_V1.json`: machine-readable seven-row comparison, page/hashes/first-degree manuscript ambiguity.
- `test_hellenistic_c11_recensions_and_munich_manuscript.py`: 10 tests.
- Surgically corrected C10 source register/test/report/handoff. The original C10 commit is retained in Git history; every affected source record is annotated. `README.md` has latest checkpoint pointer.

Exact narrow test:
```bash
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v
```
**77 tests OK**, no human performance test or production scoring run.

## Next safe executable source investigation

**First:** BSB original **p64,65,66** (IIIF digital images `00080`, `00081`, `00082`) were **already directly viewed** at original resolution; now rigorously transcribe the handwritten Greek rubric and nearby explanatory passages to determine sect and exact planetary-glyph key (not yet settled). Preserve unknown rather than borrowing Greenbaum day labels. **Second:** independently record all 4×30 grid assignments with cells/page glyph confidence and compare only commensurate 34 disputed entries. **Third:** inspect Boer 1958/1962 critical edition apparatus for Greek textual relation; authentic P.Oxy. 4277 image still needs exact source identification. If source access blocked, continue with feasible collation, don't pretend none exists.

**Standing restrictions:** no Gansten purchased Amazon ebook extraction via Work, no copyright facsimile redistribution, no spending, no human predictive claims, no biographies, no runtime rule promotion, no merges into the 16-family cross-tradition or production scorer.

**One-line resume:** Begin at BSB Cod. graec. 170 p65 manuscript monomoiria figure, first fix glyph/sect then collate 120 cells; corrected Epitome Sun→Sun is 83, source tests 77, 0 humans.
