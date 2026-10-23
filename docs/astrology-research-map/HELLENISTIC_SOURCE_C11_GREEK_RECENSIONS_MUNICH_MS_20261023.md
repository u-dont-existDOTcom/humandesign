# Hellenistic source C11 — corrected Epitome Sun numeral, compared seven Greek parent tables and discovered a manuscript Paulus grid

**Research date:** 2026-10-23. **Scope:** exact-source / historical-calculation research; **0 human predictive validations**, **no changes to scoring or broader 16-family map**. This is a C10 successor, not a repeat of C01–C10 acquisition or a historical prediction trial.

## 1. Major new source-integrity repair: a C10 test passed an incorrect Greek Sun reading

Directly re-rendered the **same** inspected critical Greek editions at higher resolution, without OCR:

- Main Hephaistio II.29, Pingree *Apotelesmaticorum Libri Tres* **Vol. I, 1973**, printed pp200–201 / PDF pp230–231. Authorized local file SHA-256 `f2f803c457b7ba62df23f5c51d6f49ffff3644e17723c6673f5795298514ecae`.
- Related recensional **Epitome IV §37**, Pingree *Epitomae Quattuor* **Vol. II, 1974**, printed pp240–241 / PDF pp270–271. Authorized local file SHA-256 `6ee168a3a39d414620b7c820145c1ffe06dd437617bf79fdc6c9842f51c47f8a`.
- Both PDFs were examined visually on an authorized device. Neither copyrighted edition or its images is committed to Git.

**C10 erroneous transcribed Epitome Sun→Sun `πν=130`** was falsely certified by C10's source-arithmetic tests. Actual enlarged edited Epitome text **p241** prints **`πγ=83`**; main II.29 also prints **83** for Sun→Sun. The correct Epitome IV.37 Sun recipient vector is `[104,52,64,83,30,80,118]` (order Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon). Its sum is **531**, not the false C10 **578**; parent 19 × 30 = **570**, so deviation is **−39**, not **+8**.

**Change completed:** surgically corrected the C10 JSON, C10 test, C10 report and C10 continuation note **on the isolated C11 child branch**; explicit C11 supersession annotations preserve Git provenance. The previous C10 commit remains intact as a historical failed transcription. C10 existing tests re-run after repair **67/67 passed**. This green result checks corrected fixture consistency, not independent manuscript authenticity.

A provisional C11 suggestion that Epitome Venus→Sun **36** was false was **rejected** after higher-resolution and parent/recipient-direction checking: both edited Greek texts give **Venus→Sun 36**. A nearby **Sun→Venus 35** in main Book II.29 had been confused with the opposite directed cell. Epitome Venus's row remains **213**, and the main Greek Venus row is **243** because its Moon recipient has 47 days rather than Epitome's 17. Neither a conjectural correction nor a new same-cell recension conflict is supported.

## 2. New complete paired critical-Greek table comparison, not an algorithm selection

Each row below is a **printed edition** normalized to recipient order **Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon**. Totals are mechanical sums, *not proposed sound algorithms*. The 1974 apparatus explicitly cautions that some §37 numerals are corrupt, applying p240–p241 l14.

| Parent | 1973 main Greek II.29 children (sum) | 1974 Epitome IV.37 children (sum) | Epitome − main |
|---|---|---|---:|
| Saturn | `210,84,105,133,57,150,175` (**914**) | `210,84,105,133,57,40,105` (**734**) | −180 |
| Jupiter | `85,34,42,54,22,57,71` (**365**) | same (**365**) | 0 |
| Mars | `105,42,52,66,28,70,87` (**450**) | `105,52,52,66,28,70,87` (**460**) | +10 |
| Sun | `130,52,64,83,35,87,118` (**569**) | `104,52,64,83,30,80,118` (**531**) | −38 |
| Venus | `57,22,28,36,15,38,47` (**243**) | `57,22,28,36,15,38,17` (**213**) | −30 |
| Mercury | `141,56,70,90,36,96,117` (**606**) | `141,57,70,90,36,96,117` (**607**) | +1 |
| Moon | `177,71,87,115,47,119,148` (**764**) | `177,71,87,{115/145},47,119,148` (**764/794**) | 0 or +30 |

Three high-value separations follow: (i) the Epitome **Mars→Jupiter 52** has a specific differing main reading **42** rather than an unanchored alternate guessed to close the sum; (ii) its **Sun own 83** correction removes the C10 false 130; (iii) the main **Moon→Sun 115** is visually attested, but the Epitome's glyph remains ambiguous between **115/145**; do not declare it resolved in Epitome by consulting the main. **Main Saturn→Mercury 150, Epitome literal 40, calculated approximation 140** all remain distinct. The Greek main Saturn sum **914**, not the 913 of Schmidt's separate English witness, since edited Greek prints **57** where that English list used **56**. C02 Schmidt English witness is retained unchanged.

**Historical independence boundary:** These are two textual versions of related material edited by the same modern scholar, *not two independent ancient astrologers* and certainly not separate human validation samples. A matched number cannot be counted as predictive success.

## 3. Major manuscript-access advance: Bayerische Staatsbibliothek Cod. graec. 170

**New genuine original manuscript image directly opened**, whereas C10 had only nineteenth/twentieth-century scholarly edition leads for Paulus:

- Repository: **Bayerische Staatsbibliothek, Munich**; shelfmark **Cod. graec. 170**, catalogued between mid-15th and 16th century sections, Paulus text dated **16th century**.
- **Pinakes work catalogue** explicitly lists Paulus Alexandrinus *Introductio in apotelesmaticam artem* on manuscript pp**27–73**, `Cum scholiis et figuris` (with scholia and figures). Catalogue URL: `https://pinakes.irht.cnrs.fr/notices/oeuvre/8855/`.
- BSB machine-verifiable IIIF presentation manifest `https://api.digitale-sammlungen.de/iiif/presentation/v3/bsb00131007/manifest` returned HTTP200 and **274 digital images**. **Digital image number 81** is visibly handwritten **page 65** and contains a four-column astronomical/monomoiria table with sign headings **Aries, Taurus, Gemini, Cancer**, degree numbers and planetary glyphs.
- Direct **original photograph**: `https://api.digitale-sammlungen.de/iiif/image/v3/bsb00131007_00081/full/max/0/default.jpg`. This exact original 1831×2400-pixel image and its upscaled regional crops were inspected visually through the library's public IIIF service. Adjacent handwritten **p64** (BSB image 80) and **p66** (BSB image 82) were also actually opened; their Greek methodological rubric and day/night rule were **not deciphered to reliable transcription standard**. Images are not copied into Git or delivered separately.
- Biblissima manuscript catalogue: `https://portail.biblissima.fr/fr/ark%3A/43093/mdatac4494ac51c3bdba3277e290d1ff2815608dcb12f`. It independently corroborates the shelfmark, date range and Paulus contents; independent *metadata* is not independent testimony about each glyph.

**Preliminary paleographic notes (NOT yet an admitted 120-cell transcription):** Aries degree-1 symbol resembles a Mars glyph, Taurus degree-1 a Venus sign, Gemini degree-1 Saturn-like, Cancer degree-1 Venus-like. These descriptions are **tentative**; not verified against manuscript's own sect/title explanation and planetary-glyph alphabet. The four sign headings and overall table layout are clear. The MS may preserve a different recension or a nighttime/alternative procedure: **do not** compare apparently differently conditioned cells to the Greenbaum *daytime* table yet. Explicit admission: **0 of the 34/120** disputed day-vs-narrative cells resolved by this C11 pass. The source is **a sixteenth-century handwritten witness**, *not* a late-antique authorial autograph.

**Recommended next source step:** Inspect p64–66's handwritten headings and scholia, determine the table's actual method and sect from Greek words rather than inferred planet symbols. Establish the scribe's seven-glyph key using repeated occurrences and independent printed/transcribed Greek. Then transcribe the 4×30 grid with row-to-degree provenance, uncertain cells recorded as sets, compare the 34 disputed day cells only when sect concordance is established. The accessible historical scan removes the *missing original manuscript image* blocker, **not** the textual-adjudication gate.

## 4. Other original evidence not upgraded

- **Boer 1958/1962**: The relevant Teubner diagrams are not yet directly read/collated; their printed editorial choices still must be checked against this newly located original Munich MS, plus other witnesses if practical.
- **P.Oxy. LXI 4277**: Oxford's public images portal was inspected for catalog/collections but the exact authenticated 4277 photograph was **not** retrieved. Prior C05 **1/3 monomoiria reconstruction agreement** and **2 mismatches** from Tolsa/Jones remain; no original image claim.
- No biographies, user birth data, purchased Kindle Gansten extraction, cross-tradition map changes, scoring or human performance tests.

## 5. Reproduction / durable files

[C11 paired Greek/manuscript register](HEPHAISTIO_C11_MAIN_EPITOME_AND_MUNICH_MANUSCRIPT_WITNESS_V1.json) has direct-source hashes, the seven row-pairs, corrected Greek numeral, first-degree manuscript glyph *tentatives*, exact image locators and explicit untouched/unresolved status.

[C11 tests](test_hellenistic_c11_recensions_and_munich_manuscript.py) add **10** source-integrity tests. Regression:
```sh
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v
```
**77/77 passed, exit 0** (67 old including corrected C10 and 10 C11). Passing arithmetic tests do **not** authenticate ancient transmission or validate chart predictions. **Human predictive validations: 0**.

The source-critical work is still **OPEN**: uncompleted Boer diagram collation, Munich sect and glyphs, Moon numeral, exact papyrus photo; no new rules are promoted. See [C11 durable continuation](HELLENISTIC_CONTINUATION_C11_20261023.md).
