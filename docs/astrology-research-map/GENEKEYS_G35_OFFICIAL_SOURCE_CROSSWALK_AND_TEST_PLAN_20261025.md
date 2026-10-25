# G35 — Gene Keys source audit and executable Human Design crosswalk

**25 October 2026. Parent goal OPEN.** The original owner is building a source-faithful comparison of historical and modern chart-based traditions and wants prospective falsifiable claims tested on untouched consenting humans, with held-out respondents and independent nonastrology controls. Gene Keys is relevant to that work. **It was not previously implemented as a separate Gene Keys study lane**, although the existing `src/hdmatch/chart/rave_mandala.py` cited a “Gene Keys by Birth Date” reference for its gate wheel. This checkpoint adds actual Gene Keys source mapping and executable crosswalks **without touching** the Hellenistic C34 read-only study-dry-run, root participant-session task, source interpreters or production chart scorer. **Real human predictive validations: 0.**

## 1. What Gene Keys actually adds

**Gene Keys** is the modern contemplative synthesis developed by **Richard Rudd**. Official primary publisher guidance [How to Read Your Profile](https://genekeys.com/how-to-read-your-profile/) places each of **64 Gene Keys** on a spectrum called **Shadow, Gift, Siddhi**. The Golden Path takes a Hologenetic Profile through three sequences: **Activation**, **Venus** and **Pearl**. Richard Rudd describes the system as contemplation, not a fixed deterministic personality diagnosis. These source claims are interpretive/experiential, not demonstrated molecular or neurobiological “frequencies”.

Official Gene Keys [Astrology resource](https://genekeys.com/resource/astrology/) and [sphere-to-planet FAQ](https://genekeys.com/docs/what-planets-does-each-sphere-of-the-golden-path-profile-correlate-to/) show that **the input planetary positions and 64-wheel geometry significantly overlap with the incumbent Human Design system**. The publisher says each key spans **360°/64 = 5.625°** and each of its six lines spans **0.9375°**, using a **tropical zodiac**, Swiss Ephemeris, and birth/prenatal planetary placements. Gene Keys is therefore a **distinct interpretive tradition**, not an additional independent set of natal astronomical measurements or a scientifically independent confirmation of Human Design simply because it uses different words.

**Statistical consequence:** do **not** count “Human Design says Gate 54” and “Gene Keys says Gene Key 54” as two independent hits. They are a recoding of the same source coordinate. The appropriate possible independent contribution is an **explicitly frozen Gene Keys interpretation** that forecasts observable behavior beyond a matched Human Design interpretation/model and birth-time/seasonality controls, not another vote from the same line number. The Life’s Work/Brand–Evolution and Radiance–Purpose pairs are also **Sun/Earth oppositions**: each pair is geometrically coupled and cannot be treated as two independent variables.

## 2. Verified official profile sphere-to-planet correlations

The official [sphere correlations](https://genekeys.com/docs/what-planets-does-each-sphere-of-the-golden-path-profile-correlate-to/) directly specify:

| Core Golden Path sphere | Existing HD activation used | Core sequence(s) |
|---|---|---|
| Life's Work / Brand | Natal / personality **Sun** | Activation + Pearl |
| Evolution | Natal **Earth** | Activation |
| Radiance | Design / prenatal **Sun** | Activation |
| Purpose | Design **Earth** | Activation + Venus |
| Attraction | Design **Moon** | Venus |
| IQ | Natal **Venus** | Venus |
| EQ | Natal **Mars** | Venus |
| SQ | Design **Venus** | Venus |
| Core / Vocation | Design **Mars** | Venus + Pearl |
| Culture | Design **Jupiter** | Pearl |
| Pearl | Natal **Jupiter** | Pearl |

These are **11 unique spheres**, although counting every sequence reference gives **4 Activation + 6 Venus + 4 Pearl = 14 references** because Purpose, Vocation and Life’s Work recur. The same official page lists **Creativity (Design Uranus)**, **Relating (Natal Mercury)** and **Stability (Design Saturn)** as *additional* spheres; this source register preserves them in a separately requested extension, not as three silently added core Golden Path spheres.

**New executable mapping:** [`genekeys_g35_source_crosswalk.py`](genekeys_g35_source_crosswalk.py) reads the incumbent typed `ChartComputation.activations` from `hdmatch`, not new astronomy. It verifies all required sources, exact typed celestial body and natal/design layer, numeric gate/line label against original longitude, no duplicated inputs, actual tropical 64-sector wheel, the 180° Sun/Earth axes and paired same lines, incumbent local Swiss-source metadata, exact HD 88° design provenance and every original source-record boundary. It emits **numeric Gene Key + line and sphere membership only**. It does **not** copy the 64 proprietary descriptions, assert physiology or DNA causality, or mark any person as living at Shadow/Gift/Siddhi frequency. Full copyrighted interpretive text has not been ingested or republished.

## 3. Public chart-calendar reference checks and a genuine unresolved calculation ambiguity

The official [Gene Keys solar Pulse](https://genekeys.com/resource/astrology/) prints references including **Gene Key 54 starting 6 January 2020**, and autumn 2026 pulses for **Key 32 (14–19 October)**, **50 (19–25 October)** and **28 (25–31 October)**. Actual independent source checks with the project's strict Swiss `.se1` Sun longitude and frozen Rave wheel gave:

| Public solar Pulse test instant (UTC) | Publisher-published key | Existing wheel output |
|---|---:|---:|
| 2020-01-06 12:00 | 54 | **54.1** |
| 2026-10-15 12:00 | 32 | **32.2** |
| 2026-10-20 12:00 | 50 | **50.1** |
| 2026-10-26 12:00 | 28 | **28.2** |

All four gate numbers agree. This corroborates the broad 64-key wheel orientation and sector boundaries at a few actual published transit examples; it does **not** independently authenticate a complete chart or the position of all 64 keys to the publisher’s software.

An important unresolved difference emerged in the **prenatal Design moment**. The Gene Keys official [FAQ is titled “Why 88 degrees?”](https://genekeys.com/docs/whats-a-pre-natal-design-unconscious-planet-why-88-degrees/), yet the text explains prenatal positions as approximately **88 calendar days before birth**. In contrast, the incumbent Human Design chart engine correctly solves the **instant when the Sun was exactly 88° of tropical longitude behind the natal Sun**, which is **not universally 88 days earlier**. This is a real numerical difference, not a notation preference.

To avoid fitting any owner/known participant, [six entirely synthetic research charts](GENEKEYS_G35_SYNTHETIC_SPHERE_CROSSWALK_V1.json) were calculated from 2020–2021 UTC dates with strict Swiss files and the complete existing HD chart engine. Each chart’s numeric 11-sphere core and three supplementary Gene Keys were computed from the exact HD 88° convention and compared to a deliberately naive **birth minus 88 calendar days** alternative *only as a source-ambiguity diagnostic*:

| Synthetic UTC date | Exact HD 88° moment minus naive 88-day time (days) | Of eight tested prenatal planet labels, different **Gene Key numbers** | Different **line numbers** |
|---|---:|---:|---:|
| 2020-01-06 | +0.7360 | 1 | 4 |
| 2020-03-20 | +0.9751 | 1 | 5 |
| 2020-06-21 | −2.7553 | 4 | 7 |
| 2020-09-22 | −3.5639 | 4 | 4 |
| 2020-12-21 | +0.1905 | 1 | 3 |
| 2021-05-15 | −1.1455 | 1 | 5 |

Because these counts include the directly opposed Sun/Earth positions, the differences are **not independent pieces of evidence**. They show that source interpretation matters for correct official output, particularly the prenatal Moon/Attraction sphere and lines. Official Gene Keys likely uses its own exact calculation details; **the full official Free Profile output for these six synthetic timestamps has not been independently retrieved and checked**. Consequently our adapter is labelled an **HD-derived Gene Keys source crosswalk**, **not** a certified reproduction of `genekeys.com`'s profile software. The 88° and 88-calendar-day interpretations are preserved separately and never silently resolved using a known user’s life.

## 4. What can actually be tested on humans (two DIFFERENT hypotheses)

**A. Birth-derived Gene Keys interpretation validity.** First acquire authorized primary interpretive source definitions and freeze specific **observable behavioral statements** tied to each selected Shadow/Gift/line/sphere combination. Avoid open-ended “any resonance counts,” spiritual perfection labels, after-the-fact reclassification of a skeptical person as living in the Shadow, or personalized coaching before scoring. Participants must have independently verified birth-time/birthplace uncertainty, concealed source expectations, a frozen question bank, decoy chart set and a nonastrology baseline. Because exact Gate/Line inputs overlap with HD, the incremental comparison must use the **same participant, same astronomical chart data and the same held-out outcomes**, comparing the *new interpretive model* with a fixed HD baseline, matched chart decoys and meaningful calendar season/time controls. A match to the same Gate 54 in two systems is **one underlying astronomical observation**, not two confirmations. The complete source-to-behavior mapping is **NOT YET FROZEN**, so no human prediction has been generated.

**B. Practical effectiveness of Gene Keys contemplation.** A separate randomized study could ask whether contemplating Gene Keys guidance improves preregistered self-reflection, subjective wellbeing or goal clarity more than an equally engaging generic reflection/journaling program. Match guidance time, expectancy and attention; distinguish philosophical inspiration from measurable benefit. Such an outcome would support or fail to support a **contemplative intervention**. Even a strong benefit would **not validate its natal planetary encoding, epigenetics, genetic mythology or personality prediction**.

[Machine-readable official-source and trial classification](GENEKEYS_G35_SOURCE_STATUS_AND_TEST_PLAN_V1.json) preserves these as distinct scientific targets, neither declared successful. No Gene Keys subscriptions, online profile account accesses, copyrighted books or real human records were used.

## 5. Bounded next research tasks and archive status

1. **Official synthetic Hologenetic Profile parity**: obtain authorized output of `genekeys.com` Free Profile for a small nonpersonal reference set with exact time/place. Confirm design moment, natal/design planet assignments, wheel boundary and line. If access is unavailable, keep `UNVERIFIED` and continue source-reading; do not falsely claim the exact official engine was cloned.
2. **Interpretive completeness before prediction**: read the accessible official descriptions of the 64 Gene Keys and applicable lines/spheres, with copyright-respecting citations and source-id provenance; select only explicit falsifiable behaviors to map. Broad developmental or unconditional mystical promises are not measurements. No blanket model score from generic adjectives.
3. **Incremental vs HD, then contemplation separately**: a genuinely prospective subject cohort with sealed predictions and authentic response records needs explicit participant consent and a separate privacy/ethics gate. Do not use existing owner or third-party biographies as holdout.
4. **Parent astrology research stays open**: Hellenistic C34 remains the accepted independent marriage-count synthetic dry-run checkpoint. Gene Keys is added as a **modern HD-derived interpretive companion** to the cross-tradition map, not as a statistically independent new natal wheel or a replacement for Hellenistic/Lilly/Jyotish/Chinese source work.

**Machine deliverables:** [crosswalk code](genekeys_g35_source_crosswalk.py), [six synthetic charts and exact design-ambiguity comparison](GENEKEYS_G35_SYNTHETIC_SPHERE_CROSSWALK_V1.json), [repeatable synthetic generator](genekeys_g35_synthetic_profiles.py), [source and test registry](GENEKEYS_G35_SOURCE_STATUS_AND_TEST_PLAN_V1.json), [source/geometry/negative regression suite](test_genekeys_g35_source_crosswalk.py), and [durable continuation](GENEKEYS_G35_CONTINUATION_20261025.md).

**No Human Design production module was modified.** All files are in the isolated `humandesign` research branch; the root `participant-session-v1` active exclusive task is untouched. Gene Keys natal predictivity and contemplation benefits remain **unmeasured**.


## G35 executable validation and source-bounded completion

The verified G35 research checkpoint ran `PYTHONPATH=src /home/joel/humandesign/.venv/bin/python -m unittest discover -s docs/astrology-research-map -p 'test_genekeys_g35_*.py'`: **23/23 new source, wheel, supplement/planet mapping, adversarial mutation and non-promotion checks passed**, exit zero. The complete inherited Hellenistic source/engineering suite also passed **367/367**, without skipped ERFA/IERS optional checks using the previously pinned local researcher inputs. These are **390 source/engineering test cases across two suites**, NOT real participants, not 390 independent predictions and not predictive validation.

The entire six-chart synthetic G35 source-only generator was independently rerun from the unchanged pinned local Swiss `.se1` source files and its JSON output compared **byte-for-byte** to the retained source artifact. Source-only body SHA-256: `e5f47a5debd6101219a33929cbdace2fc7ddf17788ef08bb387c9a13f839a303`. The source wheel SHA-256 is `2712cc761d2a237eb61c1d3536b3fcba9895fc284958510557c25f869d6189ca`. The four official published solar Pulse checks also passed using live strict Swiss planet-file positions.

**Bottom line:** the Gene Keys planet/sphere crosswalk is reconstructed from current official public help material and mechanically reproduces existing HD gate/line values. It is **not** a full official Hologenetic Profile reproduction or an authenticated 64-key interpretation corpus, and no real-person astrology efficacy is claimed. The owner’s broader comparative research objective remains OPEN; the parent Hellenistic C34 mock-freeze is unchanged.
