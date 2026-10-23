# Hellenistic astrology source research — C03 continuation checkpoint

23 October 2026 · Research-only · **Parent objective OPEN** · SOURCE_ONLY, NO real-human predictive validation

## Authority, constraints, and parent objective

The user explicitly requested **"continue"** with reading the primary astrology books already accessible on their connected computer. Continue actual source-first, source-variant, reproducible mathematical research for the cross-tradition astrology project, without forcing a fitted personal narrative or claiming predictive successes. Save durable work to `humandesign`.

Standing owner boundary: they obtained a separate Amazon **Martin Gansten, *Primary Directions*** ebook and **are not using Work mode to extract it**. This ebook was neither read nor copied. Do not ask owner to acquire new files unless a real user choice becomes indispensable. **No copyrighted full-book text** was committed. Do not merge research into production scorer or claim any numerical model predicts a human until an independently calculated, preregistered, untouched cohort actually passes its frozen tests.

## Active GitHub location and root

Research branch: `research/astro-missing-book-audit-20261022`. Canonical cross-tradition map index: `docs/astrology-research-map/README.md`. Older immutable studies belong to their own source branches; do not overwrite other tracks or duplicate the Mermaid map.

Earlier source reader:
- `HELLENISTIC_SOURCE_COMPARISON_C01_20261023.md` — Dorotheus/Ptolemy/Valens/Rhetorius action, dignity and relationship; includes verified Pingree `image [decan]` gloss.
- `HEPHAISTIO_II_TIMELORD_C02_20261023.md` and `HEPHAISTIO_II_TIMELORD_NUMERICAL_WITNESS_V1.json` — time-lord source tables including unresolved printed **360/365/375** sums and 150 vs 140 Saturn→Mercury; confirmed original Firmicus Latin **ten years nine months** vs English typo; Latin Firmicus Saturn→Mars positive, Hephaistio daytime-adverse.
- `HELLENISTIC_CONTINUATION_C01_C02_20261023.md` — older checkpoint; newer C03 findings explicitly override affected action items.

## C03: exactly completed

1. **Rhetorius ch83 page gap verified visually**, not inferred from OCR. Holden 2009 replacement **PDF p129=printed p139**, next **PDF p130=printed p141**: printed **p140 is genuinely absent**. Six-page “recovered supplement” contains only printed **44,45,48,51,52,81**, *not p140*. Other PDF candidate resolves to preview/usage-limit notices, not recoverable chapter text. The missing page interrupts occupation text; surviving p141 Lot-of-Action formula still source-attributable, but no full ch83 rule can be claimed.
2. **Paulus/Olympiodorus file scope corrected**. Its PDF p16 starts Paulus printed p1; PDF p93 ends p77 with “End of Paulus’ Introduction”. The title/TOC lists Olympiodorus commentary and appendices through printed p171, **not in acquired PDF**. Paulus's original chapters **1–37 appear present** (sampled beginning and end) but later commentary is unavailable. No owner additional acquisition requested.
3. **Hephaistio Book I inspected**. Image-only PDF has an appendix at printed p64 (PDF p80), followed by blank/back leaves; TOC matches the visible end, so **appears complete for Book I**. Original ch2 pp25–27, ch19 p36 and ch20 p37 visually read. Ch19's **“own face” geometry refers to aspects to lights in analogy with domicile relations; do not substitute the 10° face/decan dignity or the Arabic “image” translation** without Greek lexical proof.
4. **Paulus ch26 profession**, printed pp57–58 (PDF73–74), visually read. Source specifies Mars/Venus/Mercury, nine effective places, Lot of Fortune, applications and ±7-day heliacal windows; scholia supply some different priority and employment details. Cross-link to Rhetorius but **do not count as independent Greek empirical corroboration**.
5. **Daily timing 3-way discrepancy resolved at primary book-page level**: Paulus `Introductory Matters` **ch31 printed p65/PDF81**, **one sign/day**; Hephaistio II **ch28 p82/PDF47L**, **2½ days/sign**; Ptolemy `Tetrabiblos` IV.10 **Robbins printed p453/PDF477**, **2⅓ days/sign** main Greek/English reading, with Robbins **editorial footnote 3** recording a **2½ variant in two manuscripts**. Ptolemy's main month procedure is **28 days/sign**, a separate 30-day alternative appears in editor discussion. Prior Schmidt fn217 “Ptolemy 2½” is therefore a **variant, not the main printed Ptolemy critical text**. These do not establish a shared origin/month policy.
6. **Paulus ch32, printed pp66–67/PDF82–83**, visually read: separately preserves **monomoiria by trigon**, a 30-degree-by-four-triplicity star table with an editor warning about day/night misalignment, not a 10-degree decan.
7. **Named fractions-only demonstration**, `hellenistic_daily_sign_variants.py`, with `test_hellenistic_daily_sign_variants.py`: for fixed invented same starting sign across neutral 28 integer days, Paulus-vs-Heph **25 differences**, Paulus-vs-main-Ptolemy **25 differences**, Heph-vs-main-Ptolemy **10 differences**, all three match only **2 days**. This is **illustration of rule non-equivalence**, NOT valid natal chart/time computation, historical date conversion or human validation.
8. **Machine variant record**, `HELLENISTIC_SOURCE_C03_VARIANTS_V1.json`, preserves exact primary source editions/page refs, hashed local source identities, file-integrity and candidate statuses. **All variants remain NOT_READY / UNSCORED**.
9. Carried C03 supersession notes into C01/C02, local acquisition register, prior C01/C02 handoff, and canonical `README.md`. No HD model/scorer/source-engine code changed.

## Readback and test receipt

**Exact reproducibility test set, all 9 PASS**, from a fresh temporary extraction of four versioned files using the GitHub contents API (not from previously loaded in-memory code):
```shell
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v
```
- 4 source numeric transcriptions/tests of C02;
- 5 neutral daily-rate parity/boundary tests of C03.

This is a **source data arithmetic/reproducibility receipt**, not an experimental prediction test.

## Next safe research steps, precise and non-duplicative

1. **Hephaistio Greek table witness**: locate permitted original-text critical-source access to David Pingree, *Apotelesmaticorum libri tres* 1973 Book II, chapters 29 & 36; compare its Greek numeric allocations directly to Schmidt English and later fifth-century additions to Valens. Don't infer a 360/365 calendar resolution from arithmetic alone. Avoid bypassing access rights or uploading copyrighted books.
2. **Paulus ch32 monomoiria table**: source-audit original day/night trigon sequence, translator note and any Greek variant, then build a *source-only* exact 30-degree row parity reference if original authorial table is sufficiently clear; separately, continue selected readable pages of Paulus ch23–37. Do not claim unavailable Olympiodorus commentary was read.
3. **Hephaistio Book I ch19 “face”**: map original-language face/prosopon versus angular or phase-dependent own-face dignity versus decan-based rulership. Resolve at lexical/critical text level before merging with `DOR_AR_5_FACE_DECAN`.
4. **Rhetorius p140**: mark `MISSING_PAGE`; compare only unbroken material in ch82 and surviving ch83/ch84, or find an independent authorized original text if available. Do not reconstruct missing text by copying Ptolemy under the wrong name or demand owner purchase.
5. **Methodology**: advance individually computable, historically distinct occupation, relationship and timing claims into a synthetic-only comparison ONLY after semantics and chart-clock conventions are anchored. Keep independent sources and conflicting forecasts separately; absolutely no scoring against known life stories or promoting into human-facing counseling.

Other Chinese, Tibetan, Jyotish and Maya source-reading branches remain authoritative for their traditions; do not treat this Western turn as a combined-test release. **Parent project scientific objective remains OPEN, no newly validated human predictions**.

**One-line resume:** start at Greek-source review of Hephaistio II.29/36 and exact Paulus monomoiria variant, using [C03 source-integrity audit](HELLENISTIC_SOURCE_INTEGRITY_C03_20261023.md) and [C03 source variant record](HELLENISTIC_SOURCE_C03_VARIANTS_V1.json) rather than redoing completed scanning.
