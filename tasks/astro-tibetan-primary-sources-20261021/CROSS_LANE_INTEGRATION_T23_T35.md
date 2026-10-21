# Tibetan astrological source-study integration: T23–T35 (2026-10-21)

**Owner root outcome: OPEN. This is source investigation, not validated astrology.**

## Documentary coverage

Accepted predecessor T01–T22: 220 unique historical source annotations, last TIB-R0220. New T23 (19, R0221–0239), T25 (18, R0240–0257), T27 (24, R0258–0281), T30/Cornu (16, R0282–0297), T32/Henning (15, R0298–0312), T34/consultation hour (12, R0313–0324). **Total: 324 nonduplicated documentary notes**, 104 new this pass. T24,T26,T28,T29,T31,T33,T35 are transcriptions, source-variant comparisons, discrepancy or arithmetic fixtures, NOT additional historical notes. Zero prospective blinded human prediction tests or runtime model promotions.

Witnesses: Gyurme Dorje (2001) *Tibetan Elemental Divination Paintings* English White Beryl and Moonbeams, PDF235–280 (printed234–279) for this pass; Philippe Cornu (1997 English translation) *Tibetan Astrology* printed102–119 (PDF58–66); Edward Henning (2007) *Kalacakra and the Tibetan Calendar*, selected Chapter VI printed296–343 (PDF316–363); Michael Erlewine free *Tibetan Astrology* author-hosted PDF pp308–310 for specific method comparison. User-supplied PDFs remain outside Git.

## Source-grounded method distinctions

**1. Household obstacle years vs natal individual.** White Beryl chap.24 includes a five-fold current year/trigram and mewa set assessed against **majority and minority members of a household**, not merely individual birth. Sex-specific numeric-square gates and "tombs" are distinct. Annual prognostication has a classical 47-pebble scheme (6 basic +24 elemental +4 predictive +7 harshness +4 minor square +2 nine/tomb), also alternatives with 31/37, three times120 =360, and 600 with day/hour. Preserve all as different procedures, not a parameter count predicting evidential accuracy.

**2. Competing age cycles.** White Beryl's umbrella "multiples of nine" includes solitary-sign cycle ages 9,18,27,36,... and separate combined/constitution sequence 9,21,33,45,57,69,81. An exact-year or recurrence scoring contract must say which method. No single "nine-year" interpolation applies to both.

**3. Two independent Papme switch variables.** Cornu printed118–119 explicitly decides changing Papme trajectory by *masculine/feminine birth-YEAR polarity*, and **not subject sex**. Erlewine PDF309–310 explicitly describes Papme for *men/women*, switching by **subject sex**. Source conflict/variant T31 preserves both, including synthetic 1956 masculine Fire Monkey natal8 progression `8,6,2,4` and 1957 feminine Fire Bird natal7 `7,5,6,2` under Cornu. When person's sex and birth-year polarity diverge, outputs diverge from year 3 onward. The same Cornu book separately determines *annual Parkha* by subject sex—these are not interchangeable methods. `T31/papme_variants.py` accepts only an explicit policy and validates both input axes, no generic default.

**4. Cornu mewa numerical identity.** 3×3 Lo Shu base `4 9 2 / 3 5 7 / 8 1 6` sums to fifteen; natal Mewa (center), vitality (southwest), power (northeast), body (= natal). Example 1958 natal White6 yields vitality Blue3 and power Red9. Animal-year signs have three possible natal Mewa values depending on 180-year phase. Chinese numerological inheritance means a good Tibetan vs BaZi score is not independent if inherited input/rule algebra is shared.

**5. Henning calendar policy and independent arithmetic.** Kālacakra karaṇa vs Tibetan siddhānta differ in mean synodic months (29.5305556 vs 29.5305870 days) and solar-year lengths (365.258516 vs 365.270645 days). Phugpa and Tsurphu have genuinely different epoch constants, calendar intercalation interpretation and inferred solstice references; Tsurphu's zero-index new-Moon solar longitude is `0;29,34,5,37` in 27-mansion notation ≈**6.573798 decimal degrees Aries**, versus 0° at a sign boundary for Phugpa/Error Correction. Preserve Sherab Ling experimental option independently. **Newly verified source typo** in Henning p336/PDF356: literal 39,592 lunar months =175,682 weeks, contradicted by his exact monthly length and his subsequent 8,657 week excess. The exact computation gives **167,025 weeks**; T33 and `verify_t30_t33_sources.py` preserve both source and corrected arithmetic. A proposed emendation to Venus 84 units in Henning is explicitly author's hypothesis, not a proven manuscript error.

**6. Consultation-hour vs birth-hour.** White Beryl Part VII permits specific seven dayparts and disallows night queries; it has separate hour destiny-element, trigram and numeric-square sets. The nine-sector, three-generations query chart uses the consultation day's mewa at the center and compares sectors against year mewa **except some use day's mewa**. Paternal, maternal, children's and collateral family targets are distinct, directional elemental inhibition matters; north-west sector 7 instead uses a directional **enhancement** omen. These are consultation-context observations, not pure natal signals.

## Additional edition discrepancies

- **TIB-CONFLICT-004** White Beryl PDF236: five confusions with Mouse/Pig natal and current Khon gives current Sheep alone in Plate9 table, but prose broadens to Ox/Dragon/Sheep/Dog.
- **TIB-CONFLICT-005** PDF253: an Earth-element nine-cycle example prose says Hare/Pig while table says Mouse/Pig.
- **TIB-CONFLICT-006** Henning PDF356: printed 175,682 weeks contradicts exact 167,025.
- **TIB-CONFLICT-007** White Beryl PDF279 intro says sector8 North and sector9 Northeast, while PDF280 printed detailed chart labels sector8 **Northeast** (maternal uncles) and sector9 **North** (daughters). Both orders retained, chart not promoted.

These add to three earlier White Beryl conflicts (Red Seven/Red Two, repeating Zin trigram, Khon/Khen wedding transport). No source disagreement is resolved by fitting a known person's history. Note that White Beryl's 30-row family procedure, ancestors, and query-hour readings need independent additional inputs; a missing input cannot be imputed from interview answers to create a hit.

## Cross-family scientific ablations

- Compare a Tibetan birth-only animal+mewa baseline to Chinese BaZi birth-year/cycle baseline first; incremental Tibetan trigrams/element relations must be tested **after** dependency controls.
- Keep **family** (births, parents, descendants), **electional/consultation** (observed query hour or selected wedding date), **annual timing** (age and year), **natal trait** and **mathematical calendar parity** as distinct scoring domains. Do not pool them.
- Compare Phugpa, Tsurphu, and experimental solar-sector birth/date policies only as preregistered or independent numerical parity arms. Never choose calendar policy after seeing human responses.
- All original human blind evaluation gates from the humandesign project remain OPEN, including untouched participant splits, predictions frozen before questionnaire collection, controls and decoys, and explicit negatives/failures.
- No clinical, relationship-safety or personal mortality guidance from historical divination.

## Next reading

Dorje Part VII consultation-hour PDF **282–293** then ill-health printed294–305, death printed306–357, remaining charts. Continue from **TIB-R0325**. Read Cornu remaining practical chapters, Henning Chapters I–V and remaining VI, complete Erlewine free text and Janson; compare Tibetan original/alternate witnesses for all seven known source discrepancies. Full executable chart engine, astronomical verification and real blind testing **not yet done**.
