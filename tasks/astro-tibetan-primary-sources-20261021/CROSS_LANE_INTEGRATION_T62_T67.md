# Tibetan astrology T62–T67 — Kālacakra originals, five-planet arithmetic and source-critical variants

**Study date:** 21 October 2026 (Africa/Dakar = UTC). **Parent HumanDesign astrology research status: OPEN.** This document reports bounded, source-anchored historical-text and deterministic mathematical advances. It is NOT an empirical validation of astrological behavior, relationships, personal fate, psychological predictions, mortality, or spiritual outcomes. Zero blinded human predictive observations or source-based model promotions occurred.

## 1. Parent root task, accepted baseline and new coverage

Original owner purpose: “ok then start reading everything you need that's free plus these, in turns, to merge into the other readings we are doing for astro system.” Subsequent directions repeatedly “continue.” The authorized root outcome includes source-grounded comparison of classical Western Lilly/Ptolemy, Jyotish, Chinese BaZi/Zi Wei, Tibetan Buddhist astrology; independent correct calculation; and *frozen*, genuinely blinded out-of-sample human forward/reverse tests versus matched-chart decoys and non-astrology baselines, preserving misses/negatives. Documentary counts and synthetic math checks cannot substitute for that final empirical goal.

Previous accepted Tibetan source checkpoint: `research/astro-tibetan-t57-almanac-janson-20261021`, exact GitHub SHA `645e8e9e9128d5f1c0c8d3602573020625bff37e`, historical source registry **542** records `TIB-R0001–0542`. Present branch `research/astro-tibetan-t62-henning-originals-planets-20261021` is isolated from all other astrology lanes. **53** new documentary notes:
- T62, Henning Chapter V calendrical source and epoch: **16** records `TIB-R0543–0558`.
- T63, Henning planetary and karmic qualification: **16** records `TIB-R0559–0574`.
- T64, Janson Appendix D planetary and lunar-node formulas: **16** records `TIB-R0575–0590`.
- T66, internally inconsistent published solar epoch: **1** record `TIB-R0591`.
- T67, translated name-syllable and year-change textual gaps: **4** records `TIB-R0592–0595`.

**Cumulative: 595 source/documentary annotations.** T65 is *implementation and tests*, adds **zero** source annotations. All prior T01–T61 notes and software remain intact. This worktree uses a small **sparse checkout** on root disk, since the owner's `/mnt/hdd` archival volume was full; there is no need to copy an unrelated Western archive or delete any earlier research. No copyrighted PDF images or private records are committed.

## 2. Source witnesses and independent authority levels

Primary *working edition*: user-uploaded Edward Henning (2007), `Kālacakra and the Tibetan Calendar`, physical PDF **413 pages**, SHA256 `3fa6c44d4c25c4c69937e9575c0653265e1e77bb1b6923a19ef69ec10f539fd5`. The original PDF Chapter V translated `Kālacakra Tantra`/`Vimalaprabhā` calendrical material is printed **pp211–294 (one-based PDF231–314)**. Translated passages, Henning's editorial interpretation, his mathematical reconstructions and his conjectures are separately tagged. Chapter II printed **pp57–87 (PDF77–107)** provides an **independent printed 1 March 1995 worked numerical calculation** for modeled planetary motion. We checked key exact physical pages and separately visually inspected **one-based PDF83/printed63** for the critical solar epoch constant.

Additional mathematical witness: **Svante Janson (2014)**, `Tibetan calendar mathematics`, open author-hosted text `https://arxiv.org/html/1401.6285v1`, Appendix D.1–D.6 including equations D.1–D.20 and source Tables11–13. Janson builds on Henning, Schuh and almanacs. Their computational agreement is **useful engineering/source parity** but not independent observational evidence of ancient accuracy, not a fresh Sanskrit/Tibetan original witness, and certainly not an independent predictive outcome test.

We have NOT independently collated the original Sanskrit manuscript of `Vimalaprabhā`, the purported Mūlatantra, or direct Tibetan original editions for the passages translated by Henning. This matters for disputed letter tables, old-school astronomy and philosophical scope.

## 3. Major theoretical and methodological discovery: ancient critique of strict fatalism

In Henning's translated `Vimalaprabhā`, printed **p249/PDF269**, a passage **attributed within that commentary to the Mūlatantra** explicitly claims that beings born at the same instant may experience different lives and that people with unlike birth horoscopes may share a sudden disaster. It argues the roles of action, virtue and harmful conduct. This is a doctrinal/source-authored argument, not a controlled comparison or demonstrated claim about actual birth-time twins.

Henning separately interprets this as rejecting *rigidly fatalistic astrology*, **not** as denying all astrologically expressed potential. The latter potential-versus-outcome analysis is his interpretation; do not silently attribute it as a literal rule supplied by the ancient passage.

For our scientific test: the prediction must still be *frozen before responses*. The source's philosophical flexibility CANNOT turn a mismatch into a hit after seeing the outcome by invoking karma, lack of awareness, or an unknown person's actions. A proposed behavioral effect must specify an observable outcome, time horizon, reference group, probability/uncertainty and comparators, or be excluded from blind scoring as untestable doctrine.

## 4. Newly implemented historical planetary positions (T65)

`batches/T65/planetary_phugpa_E1927.py` is a new Python `Fraction` reference implementation of Janson **Appendix D**, restricted to the exact source-specified **Phugpa E1927 five-planet** branch. It requires source policy on every call and rejects unsupported Tsurphu/E1987 planet configurations. It independently computes:
- 1995-03-01 civil-day JDN **2449778**, general solar days **24,806** since E1927 JDN **2424972**.
- Particular-day/orbital cycle lengths `R` (Mercury 8797, Venus 2247, Mars 687, Jupiter 4332, Saturn 10766) and respective E1927 offsets (4639, 301, 157, 3964, 6286); inner-planet multipliers **100** for Mercury, **10** for Venus, **1** for the three outer planets.
- Historical heliocentric-like mean longitude, modeled mean Sun, signed slow correction from planet-specific 12-step interpolation (Table12), and fast geocentric-looking correction using 27-step interpolation (Table13). This reproduces the traditional historical mathematical model, **not observed present/ancient astronomical planetary positions**.
- Lunar nodes `Rāhu` as a 6900 **lunar-day** retrograde period, not 6900 solar days, with Moon's ascending Head longitude and descending Tail half a circle apart. E1927 `rd0=187`, E1987 `rd0=10` are independently reproduced, including same-node calculations for the same named Tibetan date under the two valid epochs.

### 4.1 Source epoch discrepancy: `TIB-CONFLICT-012`

Janson Appendix D.3 eqD.9 **prints two mathematically incompatible values** for one modeled mean-Sun epoch:
- Literal rational expression: `s0'=1−458772/6714405`.
- Same source's mixed-radix representation: `25;9,20,0,97440` in radices `(27,60,60,6,149209)` **equals exactly** `1−458672/6714405`.

Henning Chapter II printed p63/PDF83 also uses **458,672** and his worked 1995 calculation `24806×18382−458672` yields its printed quotient/remainder. Difference is `100/6714405` full circle, approximately **19.302 arcseconds** of longitude, which can change last mixed-radix digits after truncation. The error is **Janson's internally contradictory published numerical expression**, not proof of a mistaken Sanskrit original. It is NOT silently corrected: the code requires one of TWO explicit policies:
`janson_D9_literal_458772` or `henning_and_Janson_mixed_radix_458672`.
The latter is better supported by the two printed mathematical representations and independently sourced Henning example, but **neither may be chosen on the basis of personality or life-history fit**.

### 4.2 Independent published example parity

The tested policy with **458,672** reproduces source printed **1 March 1995** three-term mansion/nāḍī/pala values:

| Planet | Particular day | Historical heliocentric mean | True slow | Source-geocentric modeled result |
|---|---:|---|---|---|
| Mercury | 4485 | 13;45,55 | 22;26,16 | **20;49,16** |
| Venus | 1191 | 14;18,39 | 22;52,25 | **19;38,58** |
| Mars | 231 | 9;4,42 | 9;9,23 | **8;58,24** |
| Jupiter | 2778 | 17;18,51 | 16;57,46 | **17;45,33** |
| Saturn | 9560 | 23;58,31 | 23;17,35 | **23;14,23** |

Mean Sun for that example: **22;45,37** from Henning's p63; check is source-truncated three terms, with correct mixed-radix carrying, not physical sky longitudes. The code also reproduces the differences from the literal `458772` source policy, including Mercury `20;49,15` and Mars `8;58,26`, thereby **falsifying** the literal variant against the Henning worked result at the chosen truncation.

Test: `verify_t62_t66_planetary.py` PASS, checking 49 new source records (through R0591), exact epoch identity, source arithmetic contradiction, particular days, modeled mean/slow/fast longitudes, Rāhu cross-epoch equivalence for four synthetic dates, rejected unsupported epochs/policies, and chaining previous accepted 542-ledger source tests. `verify_t67_original_source_discrepancies.py` chains the first and adds the following four source notes.

## 5. Other newly flagged source disagreements — T67

Directly read Henning's printed pp246–251 / PDF266–271.

**`TIB-CONFLICT-013` — 28 versus 27 lunar mansions and 112 versus 108 quarters.** A name-syllable mapping described as 28 mansions ×4 syllables implies **112** quarters. Dividing twelve signs into nine quarters gives **108**, which corresponds to **27** such four-quarter mansions. Henning himself notes the contradiction and says Khedrupje/Mipham do not resolve it. No silent 27/28 conversion.

**`TIB-CONFLICT-014` — English printed list has 24 four-syllable entries despite its claim of 28.** At PDF268 the names visibly run Kṛttikā to Aśvinī, but only **24** groups are enumerated. When compared with the full separate list of 28 mansions the printed name-syllable table lacks four groups including Bharaṇī, Svātī, Viśākhā and Anurādhā. Henning further notes differences between Sanskrit and standard Tibetan Vimalaprabhā readings; he chose the Sanskrit-derived variants because he judged `White Beryl` closely aligned. We have not checked those original manuscripts. Neither missing syllables nor 28→27 assignment may be guessed.

**`TIB-CONFLICT-015` — 2;30 year-change adjustment contested.** Henning's printed pp250–251 discusses Bu-ston, Lochen Dharmaśrī, and Khedrupje assigning different purposes to a 2 weekday/30-nāḍī correction in the karaṇa year-change. Lochen's accumulated arithmetic over 221 years yields roughly 2;38,43,3, **not** the literal 2;30. Henning regards the traditional explanations as unsatisfactory. Preserve commentator identity and incomplete source math rather than choose convenient versions after chart fitting.

These are textual and calculation audit findings, NOT empirical human prediction successes or legitimate astrology chart-fitting options.

## 6. Comparative source and test implications

- Traditional Indian-derived Kālacakra planetary epicyclic models, lunar mansion cycles and Rāhu calculations are **not independent support** for very similar Jyotish astronomical or rule-derived predictions. They are inherited mathematical families; compare TIBETAN *incremental* features over preregistered Jyotish, BaZi/Zi Wei and Lilly/Ptolemy alternatives.
- Earlier Tibetan elemental/numerical Four Pillars/animal/mewa share strong ancestry with Chinese source families; do not multiply correlated claims by number of translated books or named deities/planets.
- Different semantic layers: `Mūlatantra` passage as quoted within Vimalaprabhā; Henning's translation; Henning's inference; Janson's re-expression; our derived Python implementation; traditional output; measured sky; and eventual observed human response. Each is independently labeled; tests of one do not prove another.
- Real person scientific status **zero prospective blinded participants scored; no real-world predictive accuracy demonstrated**. No model promotion, deployment, new interviews, source-fitted psychological narrative, medical or mortality advice.

## 7. Remaining original mission work

Next historical annotation **`TIB-R0596`**. Read further Henning Chapter VI mathematical source editions and original Sanskrit/Tibetan Vimalaprabhā where available; independently verify planetary rules against another physical edition or source numerical table (rather than same Janson derivative). Finish user-uploaded Cornu and freely hosted Erlewine (hundreds of pages) and Janson remaining appendices, collect direct original Tibetan `White Beryl` and `Moonbeams` witnesses, and reconcile full chart/natal/calendar policy **before freezing** predictions for participants. Need independent real modern ephemeris comparison explicitly as a separate **physical sky parity**, as historical model longitudes may be inaccurate. Then preregister source-derived falsifiable predicates and untouched forward/reverse human comparisons with decoy charts and non-astrology baselines, retaining misses and null results.

Branch-specific handoff: `CONTINUATION_HANDOFF_T62_T67_20261021.md`. **Root project remains OPEN.**
