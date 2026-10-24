# C25 — Official Vienna codex opens a distinct old-manuscript lineage and a differently numbered astronomical table

**24 October 2026. Main owner outcome: OPEN.** Continue authentic primary-source astronomy/astrology research in the preserved 16-tradition `humandesign` map. The purpose is to distinguish historically attested algorithms *before* any future, preregistered blinded human testing. **Zero human predictive validations.** No rules were promoted to production scoring, no previously known biographies informed readings, and no purchased Gansten Kindle book was extracted.

## 1. New primary manuscript evidence actually recovered

The **Österreichische Nationalbibliothek (Vienna)** makes an original photographed Greek codex accessible under **Cod. phil. gr. 115**, historical *Vindobonensis A*. Its manuscript catalogue title is *Collectio astrologica*. The owner-authorized study machine received HTTP 200 for:

- Official manuscript record: `https://onb.digital/result/1182CE33`
- Library IIIF v3 presentation: `https://api.onb.ac.at/iiif/presentation/v3/manifest/1182CE33` (exactly **468** image canvases).
- Original photograph service of the relevant folio: `https://api.onb.ac.at/iiif/image/v3/1182CE33/uk4nGb4uCinwsqiR`.

The commentary passage catalogued as *In Paulum Alexandrinum commentarium* covers **folios 162r–218v** in the specialist Pinakes record (`https://pinakes-dev.irht.cnrs.fr/notices/cote/71229/`), placing the discovered table within a plausible commentary section. **125 different original page thumbnails** (zero-indexed canvases 325–449 inclusive) were actually obtained and viewed across **six contact sheets** with **zero failed fetches**. This was not just catalog metadata.

A red-ruled tabular page was located at **folio 205v**, official **canvas 418 / zero-based index 417**. I downloaded and inspected a substantial original-image derivative:

- URL `https://api.onb.ac.at/iiif/image/v3/1182CE33/uk4nGb4uCinwsqiR/full/2600,/0/default.jpg`
- Downloaded derivative **2600 × 4070 pixels, 1,533,303 bytes**, local SHA-256 `6b6e01af7442746186c8b7fef15d0687d53d982681ccebeb4106dc9fdde15748`.
- The library's **native full-image dimensions are 4192 × 6562 pixels**, per its official manifest. The preceding and following pages were also directly opened at reduced resolution. The SHA above authenticates the **resized 2600-pixel study derivative**, *not* an unrequested full-resolution original. Do not mislabel the two.
- Source images and contact-sheet crops remain in temporary owner-controlled study storage **outside Git**.

## 2. Substantive observation: Vienna's table structure differs from Florence's

The photographic page shows black/brown planetary-looking symbols, red Greek ordinal numerals and red ruled column divisions. The center/right table visibly groups sign symbols, provisionally read as **four triplicity clusters**. To its left is another Aries-marked section whose purpose remains **unclear**; do not force it into a fifth triplicity.

The degree numerals appear in two *distinct numbered subcolumns* across approximately **fifteen rows** in each grouped section. The visible paired examples that support this provisional structural reading are:

| Row of paired numerals | First numbered column | Second numbered column |
|---|---:|---:|
| First | 1 | 16 |
| Second | 2 | 17 |
| Third | 3 | 18 |
| Fourteenth | 14 | 29 |
| Fifteenth | 15 | 30 |

This is evidence for a **1–15 / 16–30 page layout**. It is *not* an ancient Greek statement that these are day and night counterparts of the same ordinal degree, nor an independently double-read modern Greek table transcription. Exact source Greek heading, abbreviated planet glyphs and how the adjacent Aries-marked panel functions still require philological verification.

### Why this changes the C24 interpretation

The different photographed **Florence Plut. 28.14 folio 204v**, investigated C23/C24, has **two planetary glyph positions associated with each of 30 degree lines per triplicity**. Its 240 readings were provisionally typed as first and second slots, with a perfect adjacent-degree exchange *inside that specific source register*. Those photographic labels were **not blind independently verified**. C24's metrics remain unchanged: first slot vs C05 narrative **104/120**, first slot vs C04 Greenbaum corrected D **102/120**, second-slot swap **120/120**, independent C05 night **48/120**.

By contrast, **Vienna's visible paired columns seem to carry different degree numbers separated by fifteen**, not two rulership assignments for the *same* degree. Therefore it would be a serious source-category error to call Vienna's second numbered subcolumn the “night slot” simply because Florence has two planet names per degree. The two manuscripts might still express related methods in distinct layouts, but this **has not been established** by the original Greek caption or complete planetary-value collation.

**Strict data discipline:** C25 stores *five source-numbering examples* as provisional observations. It stores **zero independently decoded Vienna degree→planet assignments**, and does not generate hypothetical 30×4 rulers by reading back C04/C05 or transplanting C24 arrays. A structural table discovery is not proof the Vienna table is the **same monomoiria canon** as Florence. All conclusions requiring the exact Greek heading/adjacent explanatory prose remain explicitly **OPEN**.

## 3. Strong source-genealogy lead, but dating unresolved

A contemporary review by **Charles Mugler**, *Revue des Études Grecques* 76 (1963), p. 294, reports that **Æ. Boer used Vindobonensis A as the principal source** for her critical edition `Heliodori, ut dicitur, in Paulum Alexandrinum commentarium` (Teubner, **1962**), while missing early commentary chapters 1–8 were replaced using a later Byzantine recension. Scholarly record:
`https://www.persee.fr/doc/reg_0035-2039_1963_num_76_359_3742_t1_0294_0000_2`.

That assessment is valuable **editorial testimony**, but C25 did **not** read Boer’s 1962 **actual critical Greek chapter, apparatus or its diagram comparison**. Nor does the review certify that f205v's drawing itself provided Boer's chosen diagram.

**Dating discrepancy retained rather than resolved:** The ÖNB digital catalogue lists `1200` and discusses a note concerning a **1241 solar eclipse**. Pinakes has a different, earlier **twelfth-century (1111–1169 approx.)** attribution, and an additional specialist reference spans **1169–1241**. These are materially inconsistent catalogue/secondary claims and need actual codicological adjudication. C25 does not relabel Vienna as definitively “from 1200” or definitely “the earliest authorial source”; it remains an older photographed manuscript witness of disputed dating.

## 4. Evidence classes and reproducible check

New source-specific artifacts:

- [C25 manuscript identification, exact image integrity and observed-numbering witness](HELIODORUS_C25_VIENNA_A_F205V_SOURCE_LAYOUT_V1.json).
- [C25 structural comparison helper](heliodorus_c25_vienna_layout_audit.py), which **only** checks the five provisional 15-offset pairs and refuses to treat them as confirmed planetary assignments or day/night canon.
- [C25 source-only regression tests](test_hellenistic_c25_vienna_base_layout.py), covering official IIIF image metadata, 125 inspected pages, typed historical dating conflict, 5 observed numeral pairs, ambiguous Aries panel, *zero* Vienna planetary glyphs decoded and preserved no-prediction gates.
- [C25 durable continuation](HELLENISTIC_CONTINUATION_C25_20261024.md).

Tests verify reproducible source provenance and that the specific encoded *provisional* observations have not silently changed. **They do not establish Greek manuscript transcription accuracy, critical edition superiority or astrology’s capacity to predict people.**

Preserved original negative cases: earlier C22 Paulus manuscript-family **96/120 entries matching neither sevenfold day candidate**, C24 commentary slot **48/120 matches C05 night**, C05 P.Oxy.4277 historical **1/3 matches with two mismatches**, Hephaistio Epitome IV.37 **literal 40 / derived 140 / main 150**, and §44 **365-day parent vs 366-day children**. The 16-tradition research map and production scoring remain unchanged.

## 5. Exact next primary-source question

Next compare the **f205r Greek immediately before the Vienna table**, the **table’s own Greek header**, and **f206r Greek following**, with the same adjacent prose on the Florence f204r–205r. Only after establishing subject (monomoiria versus another kind of degree/term table) and numbering semantics should the planetary glyphs in Vienna be collated against C24 and Boer's actual 1962 textual apparatus. The additional Aries-marked column is a concrete uncertainty to resolve.

Other unresolved sources remain independent: Boer 1958 original Greek chapter-32 table/apparatus, Boer 1962 edition, Paris Z/Y source families and Jones 1999 edition against already-authenticated Oxford P.Oxy.4277 photos.

**Task status: source-research objective OPEN; zero human predictive validation. No model promotion or Gansten Kindle extraction via Work.**
