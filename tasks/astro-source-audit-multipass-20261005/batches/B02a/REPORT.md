# Lilly: foundations, chart construction and twelve houses

7 October 2026 · B02a · HumanDesign source audit

## Result
The exact previously acquired 1647 three-book witness is recovered and rehashed. **Book I chapters I-VII are now read and extracted**, printed 25-56/PDF 59-90. The methodological preface, student-practice guidance and 12-page contents have also been read. There are **91 new source records**, twelve structured house descriptions, four quadrants and 61 hourly-motion table rows. All **105 new reference tests and 34 retained methodology/index tests passed** on the owner computer; the 105 reference tests also passed in the conversation container. The repeated run is not counted as additional distinct tests. Tests concern source arithmetic, table contents and boundaries, not predictive validity.

Ptolemy remains complete in the declared English reading scope: 61/61 sections, 1066 records. These new records start the second foundation source; they do not alter any prior personal prediction or fitted ruleset.

## 1. Horary approximation is not natal precision
At printed 44/PDF 78 Lilly expressly limits his whole-degree tolerance to questions. For nativities he requires degrees and minutes, and the Sun to minutes and seconds because it determines annual revolutions. His later fast-calculation examples cannot faithfully become the exact natal-chart method. Our verified Swiss Ephemeris path remains untouched.

At printed 46-47/PDF 80-81 the example first obtains 2 h 20 m after the source-meridian correction, but then calculates just two hours, rounds the hourly motion, and explicitly omits the remaining 20 minutes. We now retain both results:

| Body | Printed worked result | Exact arithmetic using all stated linear-model inputs | Difference |
|---|---|---|---|
| Sun | Capricorn 26°44′04″ | Capricorn 26°44′55⅚″ | 51⅚ arcseconds |
| Moon | Capricorn 21°54′00″ | Capricorn 22°04′40⅚″ | 10′40⅚″ |

The more exact column is **not modern astronomical parity**: it evaluates Lilly’s linear noon-to-noon model without discarding the supplied time or fractional units.

## 2. One word can conceal several different planetary roles
Printed 49/PDF 83 distinguishes a house almuten from the whole-figure almuten. The first is attached to the relevant cusp-sign dignities; the second concerns essential and accidental power across the figure. The same page defines a relational co-significator, whereas the next chapter assigns natural planetary co-significators and joys to houses.

For example, the first house has Saturn as natural planetary co-significator and Mercury as its joy. Neither is automatically the planet ruling the sign on the actual first cusp. These fields are separate in the new table. This prevents a fluent reading from substituting a generic dominant planet for a topic-specific ruler.

## 3. Physical placement and cusp influence are separate
Printed 33/PDF 67 assigns a planet to the space between cusps, then discusses assigning its virtue to a nearby cusp within five degrees. In the first worked chart, Mars at Capricorn 13°55′ is physically in the seventh house, 3°15′ before the eighth cusp at Capricorn 17°10′.

The reference helper preserves **seventh-house placement plus a candidate eighth-house virtue connection**. It does not overwrite the first with the second or claim the complete later cusp rule is implemented. Exact-boundary and later-qualification issues remain explicit.

## 4. Strength is conditional and is not a universal favourable score
At printed 48/PDF 82 the house-order comparison requires planets to be **equally dignified**. Its explicit order is 1, 10, 7, 4, 11, 5, 9, 3, 2, 8, 6, 12. Ninth and third therefore precede second and eighth in this finer list, despite the broader angular/succedent/cadent summary nearby. Printed 56/PDF 90 additionally calls the eleventh equivalent in virtue to seventh or fourth. Both source statements survive; no convenient numerical reconciliation has been invented.

The twelve-house descriptions preserve mixed and conditional indications. Moderately fortified Saturn in the first with the specified benevolent aspect receives a favourable branch; Mars in the third is not very unfortunate unless joined to Saturn. These are historical claims with prerequisites, not unconditional modern personality or health rules.

## 5. Image checking prevented false source errors
The text layer rendered the Moon’s 3°01′ as 2°01′ in one explanatory line and 50 minutes as 30 minutes in another. Original pages 43 and 47 confirm 3 and 50. Those were extraction errors, not contradictions in Lilly’s arithmetic.

The original hourly table and first-house/physician glyphs were also checked. At printed 54/PDF 88, the sixth-house physician combination is **Mars and Venus**; Mercury is named nearby as the house’s natural co-significator. Confusing the adjacent roles changes the rule.

The printed Apogaeon/Perigaeon wording at printed 31 remains a separate witness issue rather than a silent correction. The surviving errata on PDF 888 is recorded; uncertain page/line targets are not guessed.

## Witness and coverage
Source: William Lilly, *Christian Astrology*, 1647, Wellcome b30338724. PDF 894 pages; 141842963 bytes; SHA256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`. The public catalog says the last leaf is wanting and describes the final leaf as possibly blank. The surviving alphabetical ending and errata were located. We **have not established what was on the missing leaf** or proved this witness physically complete. This does not block the verified opening chapters.

Book I begins PDF 59; Book II’s question material begins PDF 163; Book III has its own title on PDF 521 and the introductory natal tables begin PDF 523. All twelve contents pages are navigation evidence, not proof that their referenced body chapters were read. The complete book’s chapter-label and page-error collation remains open.

## Reproducible artifacts
`RULES.json`, `TABLES.json`, `CALCULATION_CASES.json`, `WITNESS_AND_PAGE_MAP.json`, `TEXT_IMAGE_CHECKS.json`, `READING_RECEIPT.json`, `UNRESOLVED.json`, `lilly_foundation_reference.py`, and `test_lilly_foundation_reference.py` contain the substance. Run locally in this directory:

```sh
python3 -m unittest discover -s . -p 'test_lilly_foundation_reference.py' -v
```

There are 20 declared unresolved issues; no fresh OCR, independent semantic reviewer, empirical validation, model promotion, or personal outcome matching occurred. Repository and delivery receipts identify what was actually published and placed on the owner computer.

**Next: Lilly VIII-XIV, the seven planetary descriptions**, starting PDF 91/printed 57 and stopping before the brief-description subsection on PDF 118/printed 84. The wider multi-source audit, reconciliation and executable-model evaluation remain open.
