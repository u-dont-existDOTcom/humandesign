# JYOT B30 — Five-, six- and seven-body source feasibility, physical sky, and dependent predictions (2026-10-21)

**No new source annotations or scored human outcomes.** The prior accepted source-ledger remains **391**. This is a source-critical + exploratory astronomical methods packet, *not* a canonical SWIEPH engine, not evidence Jyotish predicts personality, and not a test of any respondent.

## 1. Sanskrit: the apparent universal negative rule is actually qualified

The uploaded 150-page English `Sārāvalī` PDF40 (Ch19.8) says five or six planets in conjunction **normally** make their subjects poor, distressed or otherwise impaired; it attributes a similar claim for mutual aspects to **Kandalas**. A Sanskrit e-book witness, [Central Sanskrit University Chapter19 verse8](https://www.csu-lucknow.edu.in/e-books/saravali/p20.html), begins `प्रायो दरिद्रदु:खी ... षट्पञ्चसंयुतैर्विहगै:`. **`prāyo` means generally/usually**, not universally. Thus Ch19.8 can be a source-attributed default *tendency* with exceptions rather than a logically universal contradiction of Ch19.1–7, which gives different specific outcomes (including political service, learning and wealth).

This does **not** settle the scope/precedence. The source's other reference to aspects and to `ekabhavana` (in one house) may employ Bhāva versus 30° rāśi and other conditions. The output of any software choosing one of these definitions is a **versioned model**, not an automatically faithful implementation of all ancient text.

## 2. Independent astronomy: all seven in one 30° sign *does occur*

`SARAVALI_CONJUNCTION_SKY_SUPPORT_B30.json` and `astronomical_sign_support_B30.py` present a full daily **00:00 UTC** Moshier scan for Gregorian dates **1800-01-01 through 2199-12-31**, 146,097 sampled days.

**Method:** seven visible classical bodies Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn; explicit geocentric Lahiri **sidereal** ecliptic longitude via pyswisseph 2.10.03 with `FLG_MOSEPH | FLG_SIDEREAL`, verifying returned bits. For each UTC midnight, group by integer `floor(longitude/30°)`. This represents **same 30° zodiac sign**, *not necessarily within a narrow angular conjunction orb or equal/quadrant Bhāva*. No participant dates, names or survey answers are used.

| Maximum group occupancy | Sampled UTC midnights | Continuous groups with exactly this same planet set, under sampled days |
|---|---:|---:|
| Exactly five | **1,274** | 444 |
| Exactly six | **106** | 42 |
| Exactly seven | **4** | **2** |

The two all-seven same-sign clusters are:
- **1821 April 2–3 UTC 00:00**: all seven in Lahiri **Pisces** (sampled longitudes first day roughly 350.57° Sun, 341.52° Moon, 332.97° Mars, 337.77° Mercury, 346.33° Jupiter, 337.19° Venus, 354.55° Saturn).
- **1962 February 4–5 UTC 00:00**: all seven in Lahiri **Capricorn** (roughly 291.37°, 277.33°, 278.26°, 294.78°, 295.05°, 293.19°, 280.36° in the same order). The 1962 event appears also in contemporary retrospective astrology articles; a separate [non-primary source](https://vedicmystics.com/2020/04/18/all-grahas-in-one-sign/) mentions the 1821 and 1962 occurrences. That is **not** independent ephemeris method parity or evidence of predictive effects.

**Distinguish this from earlier B11:** *All seven planets simultaneously exalted* is **impossible** (Sun in Aries and Mercury in Virgo require at least 120° relative zodiacal separation, physically beyond Mercury's geocentric elongation), whereas *all seven in the same sign* is rare but **possible**. The predicates are not comparable and must not inherit each other's feasibility classification.

## 3. The zodiac definition matters

A separate deliberately **sparse** comparison `ZODIAC_CONVENTION_SENSITIVITY_B30.json` sampled **29,220** UTC midnights, every fifth day over the same 400-year calendar horizon, under tropical versus Lahiri/Fagan–Bradley/Raman sidereal conventions (Moshier):
- Tropical: **275** five-planet sample dates, **16** six-planet, **0** seven.
- Lahiri: **258**, **21**, **0**.
- Fagan–Bradley: **268**, **21**, **0**.
- Raman: **268**, **17**, **0**.

**The sparse grid misses both known two-day all-seven episodes**, even though the full Lahiri daily sweep found them. These are **sample-grid counts**, not complete frequencies. Differences in sign boundaries show why source version and ayanāṃśa choices must be fixed. Under tropical coordinates the 1821 configuration straddles the Aries/Pisces sign border, while the 1962 configuration occupies Aquarius instead of sidereal Capricorn.

## 4. Why source claim counts can massively overstate support

If one uses a same-sign or same-house **inclusive subset** definition, a single seven-planet group automatically contains **21** five-body subsets, **7** six-body subsets and **35** four-body subsets. (It also contains **35** three-body and **21** two-body subsets.) This is a *mathematical dependency*, not 64 distinct pieces of evidence about the person. The astronomical counts report *a single event at a date*, not independent successes from 21 matching horoscope narratives. Source Ch18 itself has one repeated five-body set (verses13 and20), and Ch20 includes larger and smaller spiritual-vocation groups with different narratives.

A credible scoring engine must predeclare **exact-match vs nested-subset semantics**, precise sign/house/orb and timing, and whether more-specific predicates suppress more-general results. All person-level accuracy and source-family correlation weights must be frozen **before** reading respondent results.

## 5. Boundaries and continuation

The scan is **noncanonical Moshier**, not the project-required SWIEPH with pinned .se1 files and exact computed flags. The 400-year **daily** sample can miss events shorter than 24 hours; counts by days are not independent birth-person prevalence or a random historical cohort. All conclusions concern mathematical/astronomical support, **not the truth of any source-predicted outcomes**.

B30 adds **zero documentary source entries**, so the reader stays at **391**. The source books were not republished, no production model or survey changed, and no named person was profiled. A future astronomical proof could use exact sign-ingress interval root isolation with verified SWIEPH mode, then a separate controlled forward/reverse human test with comparison baselines. Keep the isolated PR draft and do not contaminate the other reader lane.
