# Lilly: sign synthesis, antiscia and essential dignities

8 October 2026 · B02c · HumanDesign source audit

## Completed scope

**Lilly Book I is now read and extracted through XVIII**, including both consecutive sections actually labelled XVI. This batch covers PDF 118–139, from the XV heading through the end of the dignity-table explanation, stopping before XIX. The five headed units contain **161 new source records**: R231–R391. Lilly now has 391 retained records; Ptolemy's1066 records and 61 completed English sections remain unchanged. Combined source inventory: 1457 records. These are definitions, conditional claims, catalogues, qualifications and examples, not 1457 independent predictions.

The batch preserves seven brief planetary portraits, twelve detailed sign profiles, 26 sign-classification groups, 19 colour entries, six antiscion pairs, 45 degree/minute reference rows, 60 term cells and 36 face cells. All 22 relevant whole-page images were inspected alongside the existing text layer. No new OCR was used. No person-specific chart, outcome, survey or fitted prediction was inspected or changed.

## 1. Two tables labelled according to Ptolemy differ over 66 degree cells

Lilly's table on printed 104/PDF 138 is not identical to the adopted Ptolemaic table in Robbins's *Tetrabiblos* I.21, printed 107/PDF 131. The Robbins page image was reopened for this comparison; its retained extraction supplies the row lengths and cumulative endpoints.

After aligning the degree allocations, the assigned planet differs in **66 of 360 numbered one-degree cells**, distributed across seven signs. Five complete rows agree: Aries, Cancer, Virgo, Sagittarius and Aquarius. For example, the first six degrees of Leo belong to **Saturn in Lilly's table but Jupiter in Robbins's adopted table**. Capricorn's final two blocks also exchange Saturn and Mars.

This is a difference in source allocations—not an 18.3% error rate, a prevalence estimate, or evidence that either table predicts better. Different transmitted readings and editorial choices remain unadjudicated. The practical implication for our software is explicit source selection: a label such as `Ptolemy terms` is insufficient provenance for a uniquely reproducible calculation.

`DIGNITY_TABLE_P104.json`, `COMPARISON_INPUTS.json` and `TABLE_COMPARISONS.json` retain both sides. The helper requires the specific Lilly table profile; it cannot silently choose a table from whichever historical label sounds familiar.

## 2. The later Lilly table resolves assignments without rewriting his earlier lists

The new table supplies a unique ruler for every numbered term and face degree. Comparison with the earlier planet-by-planet enumerations in VIII–XIV finds:

| Comparison | Cells differing from later table | Explanation |
|---|---:|---|
| Terms |26|The 25 previously unassigned/multiply assigned cells, plus one otherwise unambiguous difference|
| Faces |20|The 20 previously unassigned/multiply assigned cells|

The additional term difference is the **20th numbered degree of Sagittarius**: Mercury in the earlier list, Saturn in the later table. This is not automatically the same question as a planet exactly at20°00′ in a continuous longitude convention.

Earlier lists and tests remain unchanged. The table gives a separately labelled usable reference, not permission to erase evidence of disagreements or declare one reading empirically superior.

## 3. Essential strength and the interpretation of circumstances remain separate

XVIII assigns five points to domicile, four to exaltation, three to the appropriate triplicity, two to term and one to face. It then gives different and qualified analogies for them.

Domicile is compared with secure control of one's affairs, **unless retrograde, combust or otherwise afflicted**. Exaltation throughout the whole sign earns four points irrespective of closeness to its special degree; an **unimpeded, angular** exalted significator can nevertheless describe **arrogance and claiming more than one's due**. Term-only fortification primarily concerns bodily constitution/temper rather than exceptional abundance or eminence. Face prevents calling the planet peregrine but can coexist with a picture of barely maintained credit and security. (Printed101–103/PDF 135–137.)

The new reference code returns the five positive essential components separately. It supplies neither a whole-chart net score nor a moral assessment. Eligibility for the stated domicile and exaltation analogies is checked separately and retains unknown conditions as unknown. The unsigned 5/4 under detriment/fall on the table are preserved; a complete signed debility model is not manufactured before the later chapter is audited.

Lilly's explicit example also matters: the **Sun in Aries at night retains exaltation but receives no fire-triplicity dignity**; Jupiter receives that triplicity dignity at night. Mars receives the water-triplicity component by both day and night in this declared source profile. (Printed102/PDF 136 and 105/PDF 139.)

## 4. Combination rules have specific logical prerequisites

The modality descriptions require **both the Ascendant sign and its ruler's sign** to have the same classification. Fixed/fixed means perseverance in what was said or done, whether good or ill; it is not a moral endorsement. A mixed pair is not specified by these three branches. Another humane-sign rule uses an **OR**, rather than this paired requirement. (Printed89–90/PDF 123–124.)

XVII directs the reader to combine the relevant house sign, its lord's sign and the Moon's sign, judging by the greater testimonies. It also changes the reference places with the actual enquiry: a merchant's trade/stock question uses second-house/Fortune testimony, not simply the personal welfare route. Numerical synthesis weights and a universal tie-breaker are not supplied. (Printed100–101/PDF 134–135.)

A further useful qualification survives in the Capricorn portrait: Lilly reports white-haired Capricorn Ascendants and conjectures that the family, rather than the sign, caused the whiteness. We preserve this as an author observation and causal conjecture, not proof of either heredity or astrology. (Printed98/PDF 132.)

## 5. Antiscia are degree-specific, with limits on their interpretation

Lilly's worked example reflects Saturn at **Leo 20°35′ to Taurus 9°25′**; its contrantiscion is **Scorpio 9°25′**. The code reproduces the subtraction exactly, including borrowing a degree for nonzero minutes. It also preserves the table's six sign pairs and 45 arithmetic rows. The explanatory prose on printed 91 names25 minutes as the amount subtracted despite the 35-minute input; the displayed result is correct. That printed inconsistency is retained separately from the arithmetic. (Printed90–92/PDF 124–126.)

The favourable analogy is explicitly for antiscia **of good planets**; no universal contact orb, probability, event timing or independent-evidence multiplier is supplied. The continuous-coordinate reflection is identified as our mathematical implementation, not a complete judgement engine.

The rising-time examples likewise preserve the actual endpoints: Leo 0°21′ to29°40′ gives2h48m; Aquarius 0°57′ to29°28′ gives1h04m. Those are differences between the stated tabulated positions, not freshly computed exact zero-to-thirty-degree durations for arbitrary latitudes. (Printed92–93/PDF 126–127.)

## Witness issues and verification

The page map records the repeated XVI heading, the 17 label on PDF 121, swapped95/94 labels on PDF 128/129, and incomplete9 on PDF 131. Navigation does not assume that PDF minus34 always equals the printed label. One curl-of-hair token in Jupiter's portrait remains unresolved; it is not admitted as an executable discriminator. Historical medical, social and geographic descriptions remain historical source catalogues, not modern diagnoses or demographic classifications.

**Actual owner-host test run: 246 distinct passing tests**: 61 new B02c, 105 retained B02a, 46 retained B02b, 34 retained methodology/index checks. The 61 new cases also passed in the conversation container; that rerun is not counted twice. The all-arcminute reflection check is one test with many assertions, not thousands of independent tests. No full-application suite, independent semantic review, astronomical ephemeris parity or predictive validation is claimed.

Twenty-four new interpretive/implementation issues are recorded. Prior blocked B02b auxiliary-file and three legacy-checkpoint replacements were not retried. The new batch, source index and dated latest-state checkpoint carry the continuation; this does not falsely mark those older blocked synchronizations complete.

## Reproduction and continuation

From this batch directory, the single test command is:

```sh
python3 -m unittest discover -s . -p 'test_lilly_sign_dignity_reference.py' -v
```

The source-data and comparison builders are included. Original source books stay outside Git. Exact source identities, inputs, file digests and scoped test evidence accompany the packet.

**Next: XIX, beginning at PDF 139/printed 105**, after the table explanation: aspects, technical terms, planetary conditions and related judgement qualifications. Its opening was incidentally retrieved but the chapter is not read/extracted in full. Do not restart XV–XVIII, the earlier Lilly chapters or Ptolemy. The wider multi-source audit, reconciliation, runtime compilation and later untouched evaluation remain open.
