# Lilly first edition (1647) — reciprocal reception and angular direction conventions

**Scope:** literal source-attributed features; the root owner objective of predictive out-of-sample comparison across astrology traditions remains **OPEN**. This study consumes no human natal data, questionnaire responses, or event outcomes. Primary witnesses: William Lilly's *Christian Astrology*, London 1647, Wellcome b30338724, newly saved original printed pp.112, 510, 511, 515, and 517, plus parent-source pp.101–105,115,654–655,670. Five original image bytes and SHA-256s are retained under `witness_pages/`.

## Reception source audit

**Printed p.112:** Lilly defines reception among two significator planets as each planet occupying some dignity ruled by the other. Three distinct worked examples are verified against the original plate, not a later summary:

1. **Domicile ('by Houses')**: Sun in Aries / Mars in Leo. Here *Houses* means signs ruled by the planets (Sun rules Leo; Mars rules Aries), NOT the astronomical Ascendant/MC houses or a country's houses.
2. **Day triplicity**: Venus in Aries / Sun in Taurus when the chart is **by day**; each occupies the other's element triplicity. At night the same example is not a mutual triplicity reception.
3. **Term**: Venus in the 24th degree of Aries / Mars in the 16th degree of Gemini, mutually placed in each other's degrees of terms. Note the Aries placement also lies in Mars's domicile **one way**. Only the *term* hosting is reciprocal; a one-sided domicile relationship is not an extra domicile mutual reception.

The source also admits reception by other essential dignities. Original p.115 additionally presents mutual reception by domicile as an **alternative** to own domicile for the +5 essential dignity slot, and reception by exaltation as an **alternative** to own exaltation for +4. They must **not** be stacked twice with an existing same-slot own dignity. Reciprocal triplicity, term and face are source-labelable relationships, but p.115 gives no new numerical award explicitly to *reciprocal* triplicity/term/face beyond a planet's ordinary own dignities; the current code assigns these **zero new points** rather than inventing extra rewards.

Mixed-kind reciprocal hosting (e.g. one planet in another's term and the second in the first planet's sign) is preserved as a distinct `mixed_only` diagnostic **without counting it as an authenticated same-class reception**. We cannot derive from p.112's three worked examples whether an arbitrary mixed pair would qualify for the same effects or scores. Nor can 'received' automatically erase an otherwise peregrine debility or the unresolved afflictions/reception effects in the full radix score.

The p.112 passage concerns reciprocal *planet* significators in a judgment. Applying it directly as a complete natal-strength condition for the **angular** significator in a primary direction would be an additional inference. The full directed-Asc/MC strength (and Jupiter's p.670 'strong in radix' qualification) therefore remain **UNRESOLVED** even where a synthetic Jupiter has a source-defined reception relationship.

## Arithmetic of specific angular directions: direct evidence, narrow geometry

**Original p.510–511:** The forward/backward (direct/converse) wording in these paragraphs is applied to **zodiacal ray points placed ahead/behind a planet in the Speculum**, including sinister and dexter aspects; it is not by itself a proof of the mathematical time-rotation orientation for every planetary/lot/hylegial direction. Preserve raw source words and p.511 examples rather than silently reinterpreting as modern converse rotation.

**Original p.515:** Lilly's worked Midheaven direction uses **RA(promissor) minus RA(Midheaven)**. His given RAMC is 222°10′ and Mercury-term RA is 229°35′. Subtracting gives 7°25′, *which he explicitly obtains in the worked calculation*. The adjacent printed intermediate list apparently gives 7°45′ for that row. This is a real discrepancy **within the original 1647 printing**; the executable witness parity uses the explicit two operands and final 7°25′, records the 7°45′ intermediate as conflicting witness evidence, and must never silently 'correct' a historical transcription. Another source row 222°31′ −222°10′ = 0°21′.

**Original p.517:** Lilly's Ascendant progression uses **oblique ascension** values, not the right ascension of the ecliptic Ascendant. Ascendant baseline OA 312°10′; a subsequent point OA 313°34′ gives arc 1°24′; OA 332°02′ gives arc 19°52′. The source-scope implementation accepts oblique ascensions as input; it does not claim to have reconstructed the whole original oblique-ascension table or its pole/latitude conventions.

A contemporary secondary research analysis by **Rumen Kolev (1998)**, *William Lilly and His Method of Primary Directions* (download at `https://babylonianastrology.com/downloads/Lilly1.pdf`, pp.5–7 and 14–22), argues that Lilly's example directions were direct according to the technique as then practiced. The analysis also documents mismatches in historical term boundaries and uses its own later Placidus program. This is useful triangulation but is **not an independent original 1647 witness** and its historical interpretation is not automatically a mathematically proven universal attribution.

**Limit:** the project has authenticated these **two specific ascending-coordinate subtractions**, not every aspect, latitude prescription, secondary motion, fixed-significator role choice, converse scheme, or Argolus's complete method. The previous engine still labels shortest-signed-angle `direct` and `converse` as modern diagnostic variants only. The new source functions preserve the full 0–360° forward arc and do not convert a long forward 357° progression into an allegedly historical 3° converse contact.

## Research disposition

Use the established source and source tables to **compose** a partial reception/ray-arithmetic feature record. Do **not** invent a global Boolean 'Jupiter strong', retune event windows on any known lives, import a different dignity table under the same 'Ptolemaic' name, or treat synthetic mathematical agreement as predictive validation. The next human study still requires an untouched cohort, objective event definitions/denominators, frozen prediction packages and proper alternative-chart/null controls.
