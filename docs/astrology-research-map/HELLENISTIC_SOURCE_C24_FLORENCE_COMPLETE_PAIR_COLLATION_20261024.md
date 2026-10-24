# C24 — Complete provisional 240-glyph collation of Florence's commentary triplicity-monomoiria diagram

**24 October 2026. ROOT OBJECTIVE OPEN:** source-faithful Hellenistic astrology variants as part of the 16-tradition `humandesign` framework, ultimately evaluated prospectively against blinded real-human outcomes. **Zero human predictive validations; zero production-scoring changes.** This is *one additional independent physical manuscript's candidate glyph transcription*, not an ancient author's autograph or a new behavioral accuracy experiment.

## Source provenance and photographic method

C23 recovered the official digitization of a commentary manuscript **Biblioteca Medicea Laurenziana, Firenze, Plut. 28.14**, 14th century, attributed within a composite text to Heliodorus and other astrologers. Handwritten **folio 204v** has the red rubric identifying a **canon of trigon monomoiriai** and four triplicity columns, each with 30 numbered degrees and **two planetary glyph slots for every degree**. The adjacent Greek explanation on f204r and next commentary on f205r were also inspected photographically at C23, but their exact day/night abbreviations have **not** been independently collated.

Original photographed figure, *not included in Git*:

`https://cdm21059.contentdm.oclc.org/iiif/2/plutei:565809/full/full/0/default.jpg`

Source image **2536 × 2572 pixels**, **741,471 bytes**, SHA-256 **`52a1b8b4f8d67514c815a56178d54c1d45e03a991a09b48417f599ff3336128e`**, as originally verified at C23. This exact stored original was reviewed again in C24 with row-by-row crops keyed to the 30 visible red Greek ordinal labels and enlarged four-column band views (degrees 1–10, 11–20, 21–30). Images/crops are temporary study files only, never part of the tracked research corpus.

**Reliability boundary:** The same model reader had already examined the first eight degrees and knew C04/C05 sevenfold sequences before normalizing glyphs 9–30. This is an explicitly **nonblind provisional paleographic reading**. A repeated glyph pattern may have biased ambiguous symbols toward a sevenfold cycle, so exact match rates below measure *our candidate transcription* rather than a separately blinded source validation. The source-image row centers recorded in the machine register are approximate crop coordinates, not an image-processing truth mask. Four first-slot candidates have lower-confidence row-edge flags; they are not declared ancient authoritative readings.

## Full first slot: 120 provisional degree readings

A complete first-column-of-pair candidate planet label was recorded for each of 30 ordinal degrees in all four triplicities. This extends C23's directly read 32 cells to a **120-position source record**, with literal arrays independently stored from the comparison algorithm in [C24 Stage A photo registry](PAULUS_C24_COMMENTARY_120_FIRST_80_SECOND_SOURCE_V1.json). The row-indexed visual classifications are consistent with one seven-planet repetition per triplicity; **that periodicity is a diagnostic discovered in the recorded image labels**, not permission to generate or substitute missing manuscript rows.

Comparing all 120 against the already frozen C05 Greek *day narrative*, C04 Greenbaum *corrected printed day* canon, and the C15 physically distinct Paulus-table family gives:

| Full 120 first-slot comparison | Matching candidate cells |
|---|---:|
| C05 seven-distinct daytime narrative | **104/120** |
| C04 Greenbaum corrected printed daytime table | **102/120** |
| Earlier C15 photographed Paulus-family table | **20/120** |
| Matches neither C04 nor C05 day method | **0/120** |

By triplicity:

| Trigon | C05 narrative | C04 printed | C15 older Paulus physical table |
|---|---:|---:|---:|
| Fire | **30/30** | **30/30** | 6/30 |
| Earth | **30/30** | **30/30** | 4/30 |
| Air | 14/30 | **30/30** | 3/30 |
| Water | **30/30** | 12/30 | 7/30 |

The older **34 C04-versus-C05 disagreement cells** remain exactly **34**. Within that subset, these new manuscript first-slot candidates agree **18 with narrative only, 16 with Greenbaum only and 0 with neither**. The remaining **86** cells agree with both source reconstructions. The observed mixed arrangement is *by trigon*: air matches the **corrected printed** sevenfold ordering, while water matches the **Greek narrative** ordering; fire and earth agree with both. It is a plausible separate *transmitted table convention*, not an independently proven authorial original.

**Critical warning:** Do **not** average or equate these counts with C22's earlier manuscript-family **12 both / 11 narrative-only / 1 corrected-only / 96 neither**. That C22 source refers to **three other photographed codices** with an eight-slot-dominant layout. Their previous candidate readings remain untouched. Both comparisons are within historical source transcriptions, not predictions on 120 people.

## Second slot: preserve an incomplete first pass, then a complete later reading

In an early C24 stage, **80 of the 120 second-slot entries** (degrees 1–8, 11–16 and 25–30 in each trigon) were separately recorded from original photo crops; degrees **9–10 and 17–24** remained explicit `null` and the original Stage A accessor fails closed when asked to supply them. After direct inspection of the remaining corresponding image rows, a **Stage B source register** records the other **40** planetary glyph readings without retroactively changing the Stage A unknowns.

Across the full **120 candidate second-slot** readings, an exact geometric pattern is observed: **swap the planet names of two adjacent first-slot degrees in each 2-degree pair** — (1↔2), (3↔4), … (29↔30). The recorded second-slot values agree with this *pairwise adjacency hypothesis* in **120/120** positions.

But this pattern is **NOT equivalent** to independently running C05's **nighttime narrative reconstruction**: only **48/120** second-slot candidates agree with that method, broken down fire 14/30, earth 14/30, air 6/30 and water 14/30. The concrete negative **fire degree 7** is: first slot Mars; photographed second slot **Sun**; C05 nighttime narrative **Mars**. This prevents treating the new source's second slot as a source-certified implementation of the older nighttime algorithm simply because all four initial night opening rulers matched at d1.

**Day/night remains conditional:** The double-slot structure and the exact pair exchange are visible/table-consistent, but the Greek abbreviations over those two positions and adjacent paragraphs have not been independently deciphered to philological standards. The second position may plausibly represent a night-sect rearrangement but **the underlying text must decide that**, not the 120/120 visual periodicity or fit to any person's chart.

**Two evidence stages remain durable:** [C24 Stage A partial witness](PAULUS_C24_COMMENTARY_120_FIRST_80_SECOND_SOURCE_V1.json) preserves the previously untranscribed 40 as null, while [C24 Stage B second-slot witness](PAULUS_C24_COMMENTARY_FULL_SECOND_120_V1.json) records the later completed provisional reading. [C24 full source comparator](paulus_c24_complete_240_source_comparison.py) refuses to alter Stage A, verifies the 80 agreed historical values, and checks all 120 pairwise slots as a *diagnostic* only.

## Source interpretive limitations

- The first and second slots may be *day* versus *night* but that has not been proved by an original-language abbreviation glossary. We intentionally refer to them as **first/second** in both machine-readable registries.
- Exact identification of the 14th-century physical commentary as autograph of Olympiodorus or Heliodorus is not established; attribution belongs to a **composite textual tradition**.
- Boer 1958 Paulus critical Greek apparatus and Boer 1962 commentator printed Greek diagram/apparatus remain uninspected. Their variants and editorial sigla cannot be invented from this different physical source.
- The photos were read by one unblinded interpreter. A separate **qualified blind palaeographic collation**, ideally source glyphs without C04/C05 predicted ruler sequences, would test whether the striking perfect sevenfold/pair-swap patterns arose from original ink or expectation. This is an *optional source quality refinement*, not an extra barrier arbitrarily imposed on the user's overarching goal.
- The photo may carry literal scribal corrections, abbreviated sign marks or misplaced row numbering; later checking should preserve such deviations even when breaking the detected cycle.
- P.Oxy. LXI 4277's original Oxford images and three scholarly-reported single-degree values remain **1 historical-source match / 2 mismatches** against C05 by-sign ordinal; not retuned. Berlin P. Berol.21347's four conjectural Moon monomoiria positions remain possible and conditional.
- **No human predictive test**, no horoscope interpretation using known lives, no model scoring changes, no cross-tradition research map mechanism changed and no extraction of the purchased Gansten Kindle book via Work.

## Reproducibility and continuation

- [C24 Stage A photo candidate readings, 120 first + 80 second](PAULUS_C24_COMMENTARY_120_FIRST_80_SECOND_SOURCE_V1.json).
- [C24 Stage B later 40 new second-slot readings + preserved original 80](PAULUS_C24_COMMENTARY_FULL_SECOND_120_V1.json).
- [First-slot and sparse-second comparator](paulus_c24_commentary_120_first_80_second.py).
- [Complete 240-candidate-slot comparator](paulus_c24_complete_240_source_comparison.py).
- [Focused source-only regression tests](test_hellenistic_c24_commentary_canon.py) and [second-stage tests](test_hellenistic_c24_second_slot_full.py).
- [Durable C24 handoff](HELLENISTIC_CONTINUATION_C24_20261024.md).

Full historical-source test command:

```sh
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v
```

**Verified C24 complete source-only regression: 228/228 PASSED, exit 0** on isolated C24 worktree (206 inherited and 22 new). This verifies arithmetic and stored source registries, not independent palaeography or human predictive validity.

**Next source work:** check the actual original Greek abbreviations/adjacent text on Florence f204r–205r, then seek Boer 1962's verified critical text or an independently read commentary table. Do not promote the synthetically convenient pairwise exchange rule or the trigon-specific mixed first-slot arrangement into production scoring solely from this unblinded image classification.

## C25 later source-lineage advance — Vienna A is not automatically the same table

**Vienna ÖNB Cod. phil. gr. 115**, official IIIF canvas 418, photographed folio **205v**, was newly located and inspected in C25, in the attributed commentary passage used as a main witness by Boer 1962. It has a visibly different **red-numbered table layout**: provisional degree numerals **1–15 alongside 16–30**, apparently in fifteen paired rows per sign-group section, plus an Aries-marked adjacent panel of unknown function. In C24 Florence Plut.28.14 folio204v, by contrast, two provisional planetary glyphs were read at **each same ordinal degree**, and their day/night meanings were still unverified. **Do not treat Vienna's paired numbers as equivalent to Florence's presumed daytime/nighttime planet slots, or assume this is necessarily the exact same monomoiria canon until original Greek headings are deciphered.** C25 admits **zero Vienna planetary degree–ruler assignments**, preserves all C24 240 provisional annotations, and records conflicting official/scholarly Vienna manuscript datings. [C25 direct primary-source report](HELLENISTIC_SOURCE_C25_VIENNA_BASE_F205V_20261024.md) and [C25 handoff](HELLENISTIC_CONTINUATION_C25_20261024.md).
