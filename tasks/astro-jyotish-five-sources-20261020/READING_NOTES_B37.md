# Jyotish B37 — correcting a copied aspect-fraction inversion (2026-10-21)

**Source-critical, not human outcome evidence.** B37 adds **three** source-located documentary records in `SOURCE_CANDIDATES_B37.json`, and a twelve-house comparison in `ASPECT_STRENGTH_TRANSLATION_AUDIT_B37.json`. The five-book reader moves from **409 to 412 historical annotations**, with **zero** blinded human predictions and **zero** natal model promotions.

## The original Sanskrit disagrees with the uploaded English Saravali

User-uploaded English *Sārāvalī* Chapter4.32–33, physical PDF11, says ordinary aspects are 1/4 to 3rd/10th, **1/2 to 4th/8th**, **3/4 to 5th/9th**, full seventh. However the [Central Sanskrit University original text](https://www.csu-lucknow.edu.in/e-books/saravali/p5.html), vv32–33, and the [older Jain Sanskrit printing](https://jainqq.org/booktext/Saravali/009887) place the terms in this order:

`त्रिदशत्रिकोणचतुरस्रसप्तमानां फलं क्रमेणैव` — third/tenth, *trikona* (fifth/ninth), *chaturasra* (fourth/eighth), seventh **in order** with quarter-increasing strength. Therefore the source-language order is 1/4 to 3rd/10th; **1/2 to 5th/9th**; **3/4 to 4th/8th**; and full to seventh. Sanskrit Ch4.33 then separately gives Saturn, Jupiter, Mars special full aspects.

This is supported by the user-uploaded V. Subramanya Sastri *Jātaka Pārijāta* **Adhyaya II sloka30–31, physical PDF463/printed66**, where the printed translation has 1/2 fifth/ninth and 3/4 fourth/eighth, and by the CP1252 Portuguese *Parāśara* **line2311**, which enumerates the same order. Those translations may share literary ancestors and are not independent evidence of predictive ability. The discrepancy is most parsimoniously a **mistake in the English Saravali rendering**, not an established disagreement among three ancient schools.

## Downstream test repaired transparently

The B36 research-only `solar_graha_aspect_B36.py` originally encoded the **uploaded English** amounts. It has now been explicitly superseded with a source-versioned data table. Its callable `aspect_fraction(...,version=...)` and `solar_aspect_possible(...,version=...)` **require** either `english_uploaded` or `sanskrit_restored`—no implicit default. The accompanying `test_solar_graha_aspect_B36.py` now has **six passing tests**, including a Venus control, the four fraction-order differences and fail-closed source selection. Both updated GitHub blobs matched the locally executed bytes.

**The B36 geometric conclusion does not change:** the list of aspect-bearing houses remains 3rd, 4th, 5th, 7th, 8th, 9th, 10th, so a Sun-to-Mercury sign aspect still cannot occur while Mercury remains within ~28° of Sun. Only the **fractional strengths**, not the eligible house set, were mistranslated. The earlier English wording remains preserved in the cross-edition matrix rather than silently erased.

The *Parāśara* text **lines2319–2343** has further longitude-sensitive degree-interpolation/Drigbala rules, and Rath's *Jaimini* course gives an entirely different sign-aspect method; those are **not** collapsed into this discrete Saravali fraction code. Historical authorship, relation among printed editions and all predictive claims remain unverified.

## Next

Continue explicit source-variant comparisons of degree-based Drigbala and sign-based graha/rāśi aspects, and unit-test their semantic boundaries without using known human biographies. The new astronomical scan B36 remains a **2.19-million-midnight Moshier sample**, not proof that the six-exaltation condition is universally impossible. Preserve source rights and other reader isolation.
