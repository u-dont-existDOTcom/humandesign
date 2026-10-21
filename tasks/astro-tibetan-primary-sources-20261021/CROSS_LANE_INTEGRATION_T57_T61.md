# Tibetan astrology research T57–T61: Janson almanac and Henning reconciliation

**Date:** 21 October 2026. **Root HumanDesign owner outcome: OPEN.** The owner asked to read the free and three supplied Tibetan astrology/calendar books in successive turns and integrate them with Western Lilly/Ptolemy, Indian Jyotish and Chinese BaZi/Zi Wei; only afterward freeze a computational model and run truly blinded human forward/reverse comparisons against matched decoys and non-astrology baselines. **Documentary source content is not evidence that the predictions work.** There have been **zero** successful or unsuccessful real-person blinded Tibetan predictive tests because **zero** have been performed.

## Durable research baseline and advances

- Exact previously accepted Tibetan source branch `research/astro-tibetan-t54-janson-true-dates-20261021` at `ae5108c154b223a5aa79022bc227c0ddba6fb286`; cumulative prior documentary notes **500**, TIB-R0001–0500. Earlier Phugpa/Tsurphu date engine and two independently authored software comparisons were verified (4,386 date comparisons across both systems, 2,193 overlapping Phugpa comparisons in JavaScript, no disagreements). This pass does NOT add them again.
- This pass adds **42 new unique source annotations**: **T57 22 Janson notes** TIB-R0501–0522, and **T59 20 Henning notes** TIB-R0523–0542. **Cumulative: 542 historical/documentary annotations**, not 542 people or predictions. T58/T60/T61 add code/derived tables/source fixtures **zero** additional historical notes.
- New isolated branch: `research/astro-tibetan-t57-almanac-janson-20261021` (actual accepted HEAD to be read from remote after final commit). The worktree is a narrow **sparse checkout** of only the Tibetan research lane, `/tmp/hd-tibetan-t57-20261021`. This avoided copying thousands of unrelated archival Lilly images onto the owner laptop's nearly full `/mnt/hdd` disk. Previous accepted notes, Western/Chinese/Jyotish source indices, and participants were **not modified**. The failed initial complete checkout was superseded by a sparse checkout; no owner action required.
- Sources directly studied: Svante Janson (2014), *Tibetan calendar mathematics*, §§7, 9, 10 and 10.1, `https://arxiv.org/html/1401.6285v1`; and the **actual user-uploaded PDF** Edward Henning (2007), *Kālacakra and the Tibetan Calendar*, **PDF pp221–228 (printed 201–208) and PDF pp376–382 (printed 356–362)**, read and checked. Henning witness SHA256 `3fa6c44d4c25c4c69937e9575c0653265e1e77bb1b6923a19ef69ec10f539fd5`. Janson is a secondary mathematical reconstruction explicitly indebted to Henning/Schuh and published almanacs, not a separate ancient source witness; Henning is a modern specialist's account and translates/interprets historical rules. Do not count apparent agreement between these authors as independent anthropological predictive evidence.

## T58: source-derived five-component almanac implementation

New runnable Python `batches/T58/tibetan_almanac.py` reuses the **unchanged** T54 exact-rational traditional calendar engine, with required explicit **Phugpa or Tsurphu**, epoch (Phugpa 806/1927/1987; Tsurphu 1732/1852) and anomaly method (`rounded` or `dharmashri_exact`).

The five-component computation preserves:
- **True weekday** of the **tithi ending** as `(true_date+2) mod7`, potentially fractional and different from the integer weekday of its civil day.
- **True Sun**, computed for **the end of that tithi** using Janson 7.23. The source carries that Sun into the day box without correcting it back to daybreak.
- **Moon at end of tithi** = `true_sun + lunar_day/30` (mod 1). **Moon at beginning of the civil day** = `Moon_end − frac(true_date)/27`; this assumes a convenient constant 27-day Moon orbit, not an observed geocentric position.
- **Lunar mansion** index `floor(27 * Moon_at_civil_day_start)`, numbered 0–26. **Angular yoga** index `floor(27*((Moon_at_day_start + Sun_at_tithi_end) mod 1))`. **Important non-simultaneity**: Sun and Moon are evaluated at different source-defined moments. Neither angular yoga nor apparent conjunction is a physically simultaneous astronomical measurement.
- **Half-tithi karaṇa** positions H1–60: four fixed H1, H58, H59, H60 and seven changing classes H2–57 repeating eight times. Janson explicitly says the exact time splitting the tithi is not definitively established in his presentation. T58 therefore returns **no karaṇa-at-daybreak by default**, unless a caller explicitly selects the provisional Henning **equal-duration halves** policy. This is source-bound engineering variant, not proven universal traditional practice.
- **Skipped lunar-day label:** no civil day, no date-specific Moon/mansion/yoga or karaṇa at dawn; true theoretical tithi-ending weekday/Sun remain available. **First duplicated day:** Moon_start uses `Moon_end−1/27` rather than the second day's fractional correction, with Janson's special weekday `weekday;60,0` display; the two days share the same tithi-ending Sun but have different Moons and yogas. Preserve source's mixed-radix truncation rather than decimal rounding.

The earlier T54 converter already distinguished **local civil-day JDN** from a UTC birth instant and its unsupported 05:00-mean-solar world-extension (T55) from authentic historical source. T58 does not change or override this. No physical new Moon or physical sunrise is calculated.

**Focused source integrity test**: `verify_t57_t58_almanac.py` **PASS**:
- All 60 half-tithi positions and four fixed markers; exact signed/fractional 27-mansion and 12-yoga numerics; rejected malformed policy arguments.
- **3,066 sampled source-almanac calendar entries** from 1985, 2000, 2024, 2026 across Phugpa/Tsurphu, including skipped labels and first/second repeated days. All circle fractions, tithi identities, mixed-radix truncation, date flags and mansion/yoga identities satisfied. This is **internal mathematical/source consistency**, not independent numerical image-column comparison or human validation.
- Chains previously accepted 500-source ledger/partial-calendar test suite.

## T59–T60: Henning's three different yogas and named karaṇas

T59 source notes and T60 `batches/T60/henning_almanac_names.py` preserve a distinction easily lost when merging this source with Jyotish and Chinese almanacs:

| Source term | Count/definition | Independent restrictions |
|---|---|---|
| **Elemental yoga** (khams kyi sbyor ba / 'byung 'phrod) | **10** unordered combinations of *weekday element* and *lunar mansion element* using **earth, water, fire and wind**. Henning printed p204: Earth+Earth Siddhi; Water+Water Amṛta; Earth+Water Yauvana; Fire+Fire Pragati; Wind+Wind Sampanna; Fire+Wind Balayukta; Earth+Wind Alābha; Water+Wind Pratikūla; Earth+Fire Dahana; Fire+Water Maraṇa. | No relation to the **Chinese five-element** production cycle unless a distinct rule is sourced. Example directly from Henning p203: **Saturday Earth + Rohiṇī mansion Earth = Siddhi**. These are names/omens, not independently observed successful activities. |
| **Angular yoga** (sbyor ba) | **27** indices from a traditional sum of non-contemporaneous modeled Sun and Moon longitudes, computed in Janson §10.4. | Henning Appendix I p360: **Phugpa yoga0 Viṣkambha**, **Tsurphu yoga0 Vaidhṛti** (shift). Do not use the same name index for both or conflate with ten-elemental yoga. |
| **Other weekday–mansion yoga** ('phrod 'byor) | Henning explicitly reports **28** named categories (p204) combining weekday and mansion identities, rather than just their elements. | The **full 28-class name/rule mapping is not supplied in the material read**, so this module returns unknown instead of inventing classifications. |
| **Karaṇa half-tithi names** | **11 types**: fixed H1 Kintughna, H58 Śakuni, H59 Catuṣpada, H60 Nāga, plus 7 changing Vava, Valava, Kaulava, Taitila, Gara, Vaṇija, Viṣṭi from H2–57. | Henning Appendix I pp360–362 and Janson §10 support **half-position -> named class**. This does **not** on its own establish the exact instant when the half-tithi changes. Separately, *karaṇa* names another Kālacakra astronomical computation **system**, not the same entity as the eleven half-day categories. |

Henning's Appendix I also distinguishes **Indian vs Tibetan index21** in the 27 lunar mansions (**Indian convention Abhijit**, **Tibetan convention Śravaṇa**) and the separate **28 Chinese mansion** series beginning **Citrā** at index0. The 27-index names, mansion elements and weekday elements were transcribed (one-based physical PDF pp376–382), separately from the source-derived Janson almanac arithmetic. Source Sanskrit spellings/diacritics may vary in ancient editions and are not automatic orthographic corrections.

**Focused verification**: `verify_t59_t60_henning.py` **PASS**: 20 new grounded notes, 27 lunar-mansion names/elements, weekday elements, all 10 unordered elemental yogas, all 27 angular yoga names with correct Phugpa/Tsurphu shift, all 60 named karaṇa positions and a source-level *Saturday + Rohiṇī = Siddhi* example; cross-check with T58 computed test dates; chains prior suites. No false physical sky claims or predictive successes.

## T61 independent caption example—what is and is not verified

The original **2003 Lhasa almanac snippet reproduced by Henning in Chapter IV printed p203/PDF223** has a legible English caption: **8 June 2003 = Water Sheep year, Tibetan lunar month4, tithi8**. Our prior independently implemented Janson calendar gives exactly that date (JDN **2452799**); the known-year attributes give **Water Sheep**. `batches/T61/HENNING_CAPTION_2003_JUNE8_SOURCE_FIXTURE_V1.json`, `verify_t61_henning_caption.py` **PASS**.

The source image's small handwritten Tibetan numerals for weekday fraction, Moon, Sun and yoga were **not independently decoded**, so **no independent almanac-numeric parity is claimed** for those columns. Janson-derived model values for that day (mansion index10, angular yoga index13, weekday Sunday, elemental yoga Pragati) remain **computed outputs**, not verified readings of the photograph.

This is an independent **published calendar-date label** check, not an independent evaluation of astrology's predictions.

## Overall limitations and next useful source reading

**Source/documentary count at this checkpoint: 542 Tibetan source notes** (500 accepted +22 Janson T57+20 Henning T59); no duplicates or model promotion; **no real-human blinded tests**. Neither traditional calendar agreement nor historical source cataloguing establishes predictive accuracy. Current new code is useful for the future Tibetan natal/annual feature arm, but must not be silently merged into production HumanDesign scores or used for health, funeral, relationship-safety or death guidance.

**Next historical source ID TIB-R0543.** Continue by reading Henning's original Sanskrit Kālacakra/Vimalaprabhā Chapter V and its planetary methods, Janson Appendix D on the planets and Rahu, Cornu's remaining sections and the free Erlewine manual. Resolve source-dependent lunar mansion zero-points, rare Tibetan manuscripts and other recorded textual contradictions independently. Independently test any new astronomical module against source arithmetic and actual published almanacs; distinguish traditional model positions from modern observational ephemeris. Eventually freeze actual Tibetan chart features and conduct untouched **prospective, blinded** forward/reverse human testing with decoys and baselines. Parent owner outcome remains OPEN.
