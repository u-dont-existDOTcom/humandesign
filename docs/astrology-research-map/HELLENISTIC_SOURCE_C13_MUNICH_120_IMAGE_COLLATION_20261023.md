# C13 — full visual collation of the Munich Paulus 120-position monomoiria table, with retained exceptions

**23 October 2026. Status: SOURCE-CRITICAL ONLY. Real-human predictive validations: 0.** Continues C12 without repeating C01–C11 book research. This is a **single early-modern manuscript** and not an ancient original, independent outcome study, or accepted birth-chart scoring algorithm.

## Source and exact review conditions

Direct digital photograph of **Bayerische Staatsbibliothek, Cod. graec. 170, handwritten p65, IIIF image 81** (Paulus's trigon monomoiria figure). Original BSB source URL:
`https://api.digitale-sammlungen.de/iiif/image/v3/bsb00131007_00081/full/max/0/default.jpg`.

Fetched via the library's public IIIF service on authorized owner's workstation. Full-source JPEG SHA-256 **`371149ee4b769979977935a2c45496bb6065aef4229f2e1168dfac12a89d52fb`**, **1831×2400 px**. Individually reviewed manuscript bands for degrees **1–10**, **11–20**, **21–30**, enlarged locally 3×. Precisely recorded pixel boundaries between two-degree manuscript bands: **[1036,1108,1181,1251,1324,1395,1467,1539,1616,1683,1753,1828,1896,1969,2038,2109]**. The images stay outside Git and are **not redistributed**; the repo contains the new manual labels, image coordinates, uncertainty and diagnostics only.

The four groups are source-labelled **fire, earth, air, water triplicities** (three signs each), and 30 consecutive numbered degree labels appear under each heading. The seven planetary glyph classes follow their recurrent shapes on the same page; a second blinded palaeographer has not verified the classifications, and Greek text giving unambiguous *day vs night* scope has not been authoritatively transcribed. The inference of day uses the fire Sun/Jupiter and earth Venus/Moon opening pairs, **not** an attested explicit handwritten day rubric.

## Actually transcribed, not mathematically imputed

**119 of 120 positions** were assigned tentative planetary labels by direct image inspection. **Earth degree 28** remains `null`/unresolved with manuscript-image alternatives **Mercury or Mars**. Other unusual late entries carry lower-confidence audit flags. The complete *literal source reading* is the independent fixture [C13 image-only source transcription](PAULUS_C13_MUNICH_120_POSITION_IMAGE_TRANSCRIPTION_V1.json); subsequent comparisons read it as data, never reverse-engineer entries from a selected mathematical period. The first eight degrees of each column reproduce the previously inspected C12 octets.

This is a genuine improvement over C12's 32 positions. However, the classification is still provisional at the scholarly edition-adjudication boundary: a visual reading **is not** a second manuscript witness or a proven planetary glyph key for a lost ancient autograph.

## A tempting single eight-position cycle **fails** against the original page

An intentionally segregated, falsifiable *modern diagnostic* repeats the visually read first eight glyphs; it was not used to fill any source values.

| Manuscript triplicity | Actually read | Differences against naive 8-position repetition | Unread |
|---|---:|---|---:|
| Fire | 30 | **0** | 0 |
| Earth | 29 | **2 (degrees 29 and 30)** | **degree 28** |
| Air | 30 | **0** | 0 |
| Water | 30 | **22 (degrees 9–30)** | 0 |
| **Total** | **119** | **24 mismatches** | **1** |

- **Water:** the first eight are Venus, Mars, Sun, Jupiter, Venus, Moon, Saturn, Mercury. But original **degree 9 is Mars, not a repeated Venus**, and **degree 10 is Sun, not Mars**. Degrees 9–30 then follow an **offset** eight-position sequence (one place ahead relative to naive repetition). This is an *observed descriptive regularity*, not authority to modify an ancient algorithm or infer scribal intention. The source still contains duplicated Venus.
- **Earth:** d28 is difficult to distinguish; d29 appears **Mars**, d30 **Jupiter**, whereas simply repeating its first eight would predict Venus and Mars respectively. Both unusual end entries were retained even though they break regularity. Earth d29/d30 carry medium–low visual confidence, so source-critical review must check these before generalization.
- **Fire and air:** all 30 visually read entries match their respective eight-position descriptive repetition, but that agreement alone does not show the formula was intended as the authentic ancient algorithm.

This **directly overturns** any temptation after C12 to program an eightfold cycle for the entire table. It also demonstrates why positive periodicity tests do not certify literal transcription correctness.

## Comparison of the formerly disputed 34 of 120 day-canon cells

The C04/C05 comparison froze **34** differences between (A) a reconstructed Greek narrative **seven-distinct-planet day** sequence and (B) the Greenbaum **corrected printed diurnal sevenfold table**. All 34 of those specific positions are now **individually represented in the C13 manuscript image reading** (the one ambiguous earth cell is *not* among them). Results compare **three historical/textual objects**, not effects on any person:

| Among the 34 pre-existing disagreements | Munich manuscript glyph agreement |
|---|---:|
| Matches **narrative only** | **11** |
| Matches **Greenbaum corrected table only** | **1** |
| Matches **neither** | **22** |
| Source glyph unavailable | **0** |
| **Total directly compared** | **34** |

The one **corrected-only** cell is air triplicity **degree 27: Venus** (narrative Jupiter, corrected Venus). The previously isolated negative **water degree 8** remains **Mercury** (narrative Venus, corrected Mars). Among other negative cells, water degree 22 reads **Saturn**, agreeing with neither earlier candidate. The historical **34-point source controversy is now fully *compared* against one more witness but NOT *adjudicated*:** C13 does not prove a lost 4th-century autograph's preferred sequence, a global diurnal canon, or that Greenbaum's declared corrections were wrong. It finds much more variation than C12's first-octet count of 8 narrative / 0 corrected / 1 neither would imply for the entire page.

### Important anti-leakage boundary

No DOB, named biography, life event, client data, or scoring weights were consulted. No candidate was chosen because an owner's chart would fit. No canonical feature/rule was admitted. Astrology's power to predict real humans remains **unvalidated (0 untouched human studies)** in this research lane. The source tests check the numerals, provenance, negative results and fail-closed unknowns, **not** whether astrology works.

## Separate access frontiers not falsely marked complete

- **Boer 1958** Paulus *Elementa apotelesmatica*, and **Boer 1962** attributed Heliodorus commentary: external catalogue records still identify them, but no verified digital copy of their relevant Greek diagram was obtained/read during C13. A catalogue/snippet is not a plate.
- **P.Oxy. LXI 4277:** no *identified authentic original papyrus photograph* yet inspected. Oxford's public images portal may list eligible EES papyri but a general portal is not an image of 4277. Preserve older C05 **1/3** match and its two negative outcomes from Jones/Tolsa printed textual readings, without image-level promotion.
- The other source variants—Hephaistio main vs Epitome, corrupt 40 / calculated 140 / main 150, and Sun-parent 83 C11 correction—remain unchanged. No Amazon purchased Gansten *Primary Directions* ebook extraction (including Work).

## Reproduction and follow-up

Files: [C13 raw independent visual witness](PAULUS_C13_MUNICH_120_POSITION_IMAGE_TRANSCRIPTION_V1.json) · [source-only tri-model comparison](paulus_munich_full_c13.py) · [12 exact witness/negative tests](test_hellenistic_c13_munich_full_source.py).

Exact test:
```sh
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v
```
C13 inspected branch receipt **98/98 PASS** (86 previous tests + 12 C13, exit 0). Again, this verifies the internally recorded primary-image observation registry and comparison computations, **not independent Greek palaeography, ancient authorship, or human prediction**.

**Next source research:** second independent page-image reading of earth degrees **28–30** and problematic water positions, reliable Greek manuscript rubric/day-night classification, and Boer 1958/1962 apparatus to determine the lineage/status of this late table. Keep the original P.Oxy. 4277 image hunt separate, and preserve every negative case.
