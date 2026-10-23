# C14 Hellenistic primary-source comparison — Florence 14th-century Paulus table corroborates Munich glyph sequence

**Date:** 2026-10-23. **Research track:** history of transmission and documentary calculation, not predictive validity. **Human predictive validations: zero.** Continue C13 without redoing older work. Purchased Gansten Amazon *Primary Directions* ebook is not part of this work; do not use Work mode to extract it.

## New original manuscript obtained directly

The **fourteenth-century** paper manuscript **Biblioteca Medicea Laurenziana (Florence), Plut. 28.7**, catalogued as containing Paulus Alexandrinus's *Elementa apotelesmatica* on **ff. 146–172v**, is digitized and publicly viewable. Pinakes lists the Paulus passage, and Biblissima gives the codex date **1301–1400**. This is a materially earlier handwriting witness than the early-sixteenth-century Munich Cod. graec. 170 examined in C11–C13.

**Exact inspected figure:** Florence **folio 168v**, digitization canvas/image **343** in the 372-image IIIF presentation. Image object `https://cdm21059.contentdm.oclc.org/iiif/2/plutei:667740/full/full/0/default.jpg`; presentation `https://cdm21059.contentdm.oclc.org/iiif/plutei:667777/manifest.json`. Original image responded HTTP 200 with image/jpeg, **2910×3779 px, 1,177,330 bytes, SHA-256 `fa84f5499c1131cd148ba5c1461a85d7700d0b793e41b0e23c1fbadc678e2d75`**. Flanking folios **168r** and **169r** were also opened to identify context. The title over the grid can be normalized approximately as *kanonion tōn kata trigōnon monomoir(i)ōn*, a canon/table of monomoiriai by trigon. The image shows the same four grouped fire, earth, air and water sign columns, with 30 numbered red-ink glyphs in each.

A bounded scan of the relevant folios **146v–172v (53 IIIF images)** located the diagram on 168v. This is one historic *physical manuscript witness*; neither source images nor copyrighted modern editions are committed in Git. Short derived numerical transcriptions and image provenance are recorded for reproducibility.

## Direct paired-source result

The new Florence glyphs were inspected at full resolution and by targeted enlarged red-grid bands covering degrees 1–10, 11–20 and 21–30. **120 provisional Florence planetary identifications** were recorded independently as source data in [the Florence witness](PAULUS_C14_FLORENCE_120_POSITION_ORIGINAL_WITNESS_V1.json). An independent, blinded palaeographic second coding has **not** been performed, and these are not judged an ancient author's autograph. The source list was not filled by a Greek narrative algorithm, a convenient periodic formula, or a known birth chart.

Compared against the C13 image-only register of the **sixteenth-century** Munich **Cod. graec. 170, handwritten p. 65**, from a different institutional source photo:

| Source comparison | Count |
|---|---:|
| Florence glyphs provisionally read | **120 of 120** |
| Munich glyphs previously provisionally read | **119 of 120** |
| Exactly concordant corresponding, readable positions | **119 of 119** |
| Contradictory readable positions | **0** |
| Munich's remaining unread glyph | **Earth degree 28** |
| Florence's corresponding reading | **Mars** (medium-high visual confidence) |

**Do not retrospectively overwrite the original Munich unknown.** Two observations must remain independent facts: Munich image *unresolved* between Mercury/Mars; Florence's red ink *Mars*. For the unusual end of the earth column Florence has **degrees 28–30 = Mars, Mars, Jupiter**, retaining the consecutive duplicated Mars; Munich degree 29 Mars, degree 30 Jupiter with degree 28 unknown. This is a useful witness-level alternative for later critical apparatus review, **not sufficient to assert the originally intended calculation or the unread Munich ink**.

**Source independence has two distinct senses:** The codices are separate physical objects and photographs, but their shared text may descend from a common exemplar. Perfect matching of overlapping columns may signal genealogical dependence; **119 agreements cannot be counted as 119 independent attestations by unrelated ancient astrologers**, let alone validation in human outcomes.

## Two independent source photos preserve the counterexamples

A naïve modern eight-slot extrapolation repeats the first octet in each triplicity. Against Florence's directly read table the deviations are:

| Trigon | Deviations from the naïve repeated first octet |
|---|---|
| Fire | none of 30 |
| Earth | **degrees 28, 29, 30** |
| Air | none of 30 |
| Water | **every degree 9–30 (22 values)** |
| **Total** | **25 of 120 deviations** |

Munich C13 had 24 deviations plus an unresolved 28th earth value. Florence now provides a corresponding **Mars**, diverging from naïve **Mercury** at that degree. Thus the discrepancy does **not** disappear in an earlier source: both images preserve the water phase shift and the unusual earth-column ending. Do not convert that observation into a rule that the authentic Paulus system operated on eight slots; it demonstrates *one transmitted diagram family*.

## Comparison with the frozen earlier source algorithms remains negative

Among the previously identified **34** narrative-sevenfold versus Greenbaum-corrected-day disagreements, Florence's table agrees **11 with the C05 narrative reconstruction**, **1 with Greenbaum's corrected print**, and **22 with neither**. These are the same per-cell classification counts as C13 Munich because all 34 positions were already readable in Munich. The one Greenbaum-only match stays **air degree 27 (Venus)**; preserve the **water degree 8 (Mercury)** neither case. These are **textual disagreements**, not human test outcomes. Neither historical reconstruction matches the entirety of these tabulations; the source families and sect context remain incompletely adjudicated.

## Other outstanding primary-source tasks

- **Boer (1958)** Greek Paulus and **Boer (1962)** attributed Heliodorus commentary: authoritative edition bibliographies and reviews exist, but the precise diagrams and apparatus have **not** been visually checked against Munich/Florence in this batch. Florence's exact 168v image and its anomaly set are now usable targets for future manuscript-siglum/source-genealogy collation; do not assert a relationship not found in an apparatus.
- **P.Oxy. LXI 4277:** Oxford's SDS papyri portal documents digital images of held papyri, but the authenticated **specific object photograph** remains unverified. C05's published Greek/source reconstructions provide **1/3** match to a particular monomoiria method, and **two negative cases**; keep them separate from this Paulus manuscript-table agreement.
- **Sect:** The manuscript headings identify the four triplicities; opening planetary pairs support a diurnal attribution, but a fully verified independent original-Greek day/night rubric is not yet established. Do not claim it was.

## Reproducibility and assurance

- [Source-typed Florence figure register](PAULUS_C14_FLORENCE_120_POSITION_ORIGINAL_WITNESS_V1.json), image URI + SHA, 120 manually recorded values, earth 28 visual confidence and anti-promotions.
- [Independent cross-codex comparison code](paulus_florence_munich_comparison_c14.py), retaining Munich null and checking mismatches without imputing.
- [C14 regression tests](test_hellenistic_c14_florence_witness.py), exact original-image metadata, all four literal source arrays, 119 bounded agreements, earth anomalies, previous-34 counts, no source/predictive promotion.

Historical-source check is source fidelity and arithmetic, **not archaeology/palaeography peer review**, not model performance, and not a real-human forward-blind test. Existing cross-tradition research map and all production scoring stay unchanged. **Human predictive validations: 0.**

**Next precise step:** obtain and read the Paulus/Heliodorus Greek apparatus or another materially independent manuscript family to establish how Florence and Munich relate; independently scrutinize earth 28 and the unusual water phase, and locate the authentic P.Oxy. 4277 photo. No source-variant selection based on known biographies.
