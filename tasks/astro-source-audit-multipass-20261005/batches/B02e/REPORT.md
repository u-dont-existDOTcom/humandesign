# Lilly's first worked question and the Part of Fortune

9 October 2026 · Source audit B02e · HumanDesign research

## Scope and result

**Lilly Book II, chapters XXII–XXIII, is now read and extracted**, including the first worked question, the Part of Fortune calculation and strength table, and the short recap of that same example. The scope is PDF **163–180**, the printed sequence **129–146**. PDF165 is actually misnumbered **113**; the record distinguishes its printed label from its place in that sequence.

The batch adds **100 source-linked records, R568–R667**, bringing Lilly to **667** and the combined Lilly/Ptolemy inventory to **1,733**. All 61 previously completed English Ptolemy sections and all earlier Lilly source records remain unchanged. The new records include definitions, qualifications, catalogues and worked examples—not 100 independent predictions.

The source is the 894-page Wellcome 1647 witness, SHA256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`. All 18 source page images were inspected alongside the existing text layer; no new OCR was used. The worked chart is Lilly's historical example, not a current participant's nativity. No current participant history, survey, chart or outcome was consulted.

## 1. The same interval receives substantially different possible timing scales

The general example initially associates eight degrees with eight weeks in moveable signs, eight months in common signs, and eight years in fixed signs. The next page explicitly limits this to a general illustration whose measure must be constrained by the other testimonies. (Printed130–131, PDF164–165.)

The worked case then uses several different scales:

| Source relationship | Static interval from stated positions | Time described by Lilly |
|---|---:|---|
| Sun already beyond the ninth cusp | 2°10′ | Departure within two months |
| Moon beyond Mercury's opposition point | 6°21′ | About six months and somewhat more of preceding money shortage |
| Moon short of Jupiter's trine point | 3°06′ | About three years of support or pleasure |
| Sun short of the end of Aries | 25°42′ | Rounded to about 26 months of freedom |
| Moon short of Mars's opposition point | 7°22′ | About three years and three quarters; an alternative of one year per degree is also explicitly mentioned |

Sources: printed137–142, PDF171–176. These computations reproduce static intervals, not the actual time of contact between moving planets.

For the last interval, Lilly chooses a mean between months and years without specifying an exact formula. He then says the general nature of the question could instead justify one year for every degree. The implementation preserves **approximately 3¾ years**, an **unspecified mean formula**, and the separate arithmetic of the one-year-per-degree option: **221/30 years**, approximately **7.37 years**. It does not invent a half-year-per-degree rule or select whichever timing best fits the reported events.

**Methodological implication:** an automated implementation needs a declared scale-selection rule before outcome inspection. A correct angular subtraction alone does not settle the predicted date. This implication is our research conclusion, not an additional rule claimed for Lilly.

## 2. Lilly warns against exact death-date judgments

Lilly distinguishes misfortune associated with other house rulers from death, and warns against pronouncing death rashly or from a single testimony. He asks whether favourable intervention occurs before the adverse encounter and allows that misfortune may be opposed or partly reduced. Even while allowing greater boldness from multiple testimonies, he says he has been wary of, and largely refrained from, judging the absolute time of death. (Printed131–132, PDF165–166.)

Those qualifications are preserved with the adverse passages. They do not establish a medically reliable prognosis, validate concurrence as statistically independent evidence, or authorize a personal death forecast. The chapter's illustrative question concerns people without a known nativity; it does not turn the question chart into a reconstructed birth chart. (Printed129, PDF163.)

## 3. The planet's function can alter a generic favourable label

In the direction-of-affairs discussion, Jupiter and Venus can be accidental infortunes when ruling the sixth, eighth or twelfth, while Mars and Saturn can be friendly with suitable house rulerships and essential strength. The source also uses different starting points for health and estate questions. (Printed133, PDF167.)

Yet in the worked example, Jupiter is both eighth ruler and a tenth-house planet, and Lilly still treats the Moon's approaching trine to it as assistance and honour, with Jupiter intervening before Mars. (Printed136–138, PDF170–172.)

We retain this tension rather than applying a universal eighth-ruler veto or silently claiming to have resolved its full hierarchy. Occupied house, ruled house, relative strength, intervening contact and the precise question remain separately recorded. The source's geographic and medical claims are historical material, not present-day relocation or health advice.

## 4. Fortune is arithmetically clear while its interpretation remains uncertain

Lilly explicitly selects the same calculation by day and night:

**Fortune = Ascendant + Moon − Sun, wrapped into the zodiac.**

In the printed example, Moon Virgo21°18′ minus Sun Aries4°18′ is five completed signs and17°. Adding Ascendant Leo23°27′ produces **Aquarius10°27′**. Ten *completed* signs identify Aquarius, the eleventh sign by name; those indexing conventions must not be interchanged. (Printed143–144, PDF177–178.)

He reports a different nocturnal convention but does not select it. The reference function requires an explicit profile. Fortune receives planetary rays but does not cast its own; the source's phase-to-house mnemonic remains separate from an actual calculation using unequal house cusps.

The full **28-row Fortune table** is preserved. Its entries are not simply the earlier planetary-strength table: for example, conjunction with the North Node receives three points here, while the earlier planetary table gives four; the sixth/eighth-house debilities also differ. This is a comparison of printed reference tables, not an empirical preference between methods. (Printed145/PDF179; earlier printed115/PDF149, retained B02d.)

Despite supplying the detailed table, Lilly says he is still little satisfied concerning Fortune's true effects and intends further investigation. That uncertainty remains attached to the table. We have reproduced its calculation, not established its predictive effect.

## Source integrity and verification limits

The batch preserves **25 unresolved issues**, including timing-scale choice, the unspecified mean, the historical chart's dual day notation, alternative obstacle interpretations, Fortune's symbolic solar conditions, and the phase/house mnemonic. Existing text recognition confused several glyphs; image checks confirm Jupiter terms in the life paragraph, Venus at Taurus16°07′ in the chart, and Spica at Libra18°33′ in the Fortune table. These were resolved before freezing the new records.

The narrative contains reported confirmations, broad alternative explanations, and later statements that something might have been foreseen. These are marked as author-reported or retrospective material. The short recap is the **same case**, not an independent replication. The source's survival report through March1646 is not a completed lifespan observation.

The new 30-test suite checks source-table identity, exact arithmetic, explicit alternatives, retained uncertainty, record integrity and deterministic regeneration. The actual combined run passed **91 distinct checks:30 new B02e,27 retained B02d, and34 retained methodology/index tests**. Repeated runs are not counted again. Logs and exact scope are recorded in `VERIFICATION.json`. No whole-application suite, independent source-semantic review, ephemeris parity or predictive validation is claimed. No model has been promoted or fitted.

## Continuation

Next is **Book II, chapter XXIV**, *If one shall find the Party at home he would speak withall*, at **PDF181 / printed147**. Its opening was retrieved incidentally but is not counted as fully extracted. The wider multi-author audit, reconciliation, implementation and untouched evaluation remain open. Earlier blocked legacy checkpoint replacements were not retried; the current Lilly index and dated source-audit checkpoint carry the latest continuation.
