# Gansten × Lilly × Ptolemy — first source reconciliation and geometric verification

**Date:** 23 October 2026 (UTC)  
**Status:** `RESEARCH-ONLY / SOURCE-COMPARISON-PARTIAL / SYNTHETIC-GEOMETRY-TESTED`  
**Parent task:** Continue the completed *Primary Directions* Kindle audit into the existing empirical astrology research framework, preserving distinct historical procedures and avoiding predictive-model promotion.  
**This pass:** 12 focused source-method comparisons, research-only reference implementations, unit/property tests and cross-formula parity. **No human chart predictions, no natal chart tuning, no merger of techniques.**

## 1. Input evidence and authority

- **Purchased Gansten edition:** earlier Work-produced *Primary Directions: Astrology's Old Master Technique* audit, ASIN B0HMRW6T9G. Its 62 disagreements (D01–D62) are **secondary attributions to Gansten**, not independent verification of all writers he cites. The owner's reviewed audit ZIP (local verified SHA-256 `e158ce40922f01f848f92fc9dfa6caf2539545de7b1fd0143160c4191e07a0d3`) is the starting package. Repository audit branch used as the independent readback target: `research/gansten-kindle-audit-completion-20261023`, observed head `f31e1ae5d73f80db928f956d53c3d8216bbe9eb3`.
- **Ptolemy:** existing `tasks/astro-source-audit-multipass-20261005/batches/B01g/RULES.json` and `DIRECTION_REFERENCE.json`, with records `PT.R64.III.10.R194–R227`; plus `PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json`. Read from the separate C07 research checkout at commit `5829f8ba7171872f1b7c4f33617a69ba3bfd40b7`. These are existing *Robbins 1940 English translation* audits, not independent collation of ancient Greek.
- **Fresh independent textual check:** Robbins English *Tetrabiblos* III.10, available as HTML at `https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Ptolemy/Tetrabiblos/3B*.html`. This confirms the published translation's distinctions among horizon/meridian/intermediate directions, the equinoctial-year unit, same-formula Fortune by day/night, and retrospective use of past events in candidate selection. It does **not** establish manuscript authority for every wording.
- **Lilly:** historical original-1647 annotation batches `B07m`, `B07n`, `B07o`, `B07p`, `B07q`, `B07x`, `B07aj`, `B07al`, read by exact Git object from the C07 research checkout. The original photographic pages were audited by prior research workers; **this pass did not reopen or personally collate those scans**. Thus a Lilly claim in the crosswalk is traceable to a precise existing source annotation, not newly independent source examination.
- The 1647 Lilly publication is identified separately by Wellcome Collection (`https://wellcomecollection.org/works/s7z7c46y`). No user biography was accessed or entered into these calculations.

The companion `GANSTEN_LILLY_PTOLEMY_CROSSWALK.csv` contains the specific record IDs, comparison status, technical implications and unverified next checks. The table is an **interpretation of distinct records**, not a copied source corpus.

## 2. Source judgments that already change implementation

| Issue | Source-specific finding | Decision for research registry |
|---|---|---|
| Direction geometry | Ptolemy III.10 restricts the ordinary sign-ascension shortcut to the rising horizon; off-angle relationships use equal normalized temporal positions. Lilly mentions Regiomontanus but delegates complete directional mathematics. Gansten reports that Regiomontanian circles and exact semi-arcs differ. | Distinct `geometry=PROPORTIONAL_SEMI_ARC`, `geometry=REGIO_POSITION_CIRCLE`, `geometry=PLACIDEAN_UNDER_POLE` and separate `SIGN_RISING_TIME_INTERPOLATION`. Names of practitioners are **not** algorithms. |
| Significators | Ptolemy's eligible sky regions, potential life significators and Lilly's five *hylegiacal places* are different categories. | Preserve selection *context* and allowable point type independently. Never equate any two five-item lists by their counts. |
| Lot of Fortune | Ptolemy III.10 as translated by Robbins uses one directed Sun-to-Moon distance from Ascendant day and night. Lilly has Fortune among directed places; this does not tell us which sect formula he uses. | Version Fortune rules; do not silently impose night reversal or claim Lilly used Ptolemy's version. |
| Timing | Ptolemy's one equinoctial time → one symbolic year differs from a modern exact mean-solar constant. Lilly printed Naibod tables contain original cell anomalies and need literal treatment. | Store `time_key` and its actual source/version **separately from** geometry and from the modern 360/365.25 calculation. Never replace a historical table with a rational approximation without labeling it. |
| Latitude/aspects | Ptolemy's latitude exception is scoped to bodily encounters; Gansten reports other historical latitude constructions for aspects. | Define `aspect_provider` and `bodily_vs_projected` separately, with unresolved constructions disabled. |
| Profections and timing confirmation | Lilly source notes preserve 30° annual sign progression, fractional subannual timing, and use of profection figures when directions conflict. | Separate auxiliary forecasting layers and freeze any confirmation criterion before comparing outcomes. |
| Converse | Ptolemy's leading/following-sign directions have scope-dependent roles and do not license treating a modern reversal of time as an exact historical equivalent. | Three distinct modes: direct, documented traditional converse/role swap, modern reverse-time converse. Their complete aspect branches are **not implemented** here. |
| Rectification | Lilly flags large timing shifts from birth-angle uncertainty; Ptolemy III.10 includes retrospective comparison of possible candidates against earlier events. | Do not use events under test for birth-time correction or choice of alternative geometries. |

**Source-bound unresolved:** the cited original Regiomontanus, al-Qabisi, Bianchini, Morin and Placidus examples were not independently opened in this pass. The sampled Lilly annotations do not settle intermediate cusp *point versus locus* mechanics. No unsupported rule was inferred to fill those gaps.

## 3. Synthetic numerical verification — completed

Four calculation families are kept separate. The first three act on the same frozen equatorial test input: northern latitude 45°, RAMC 0°, fixed right ascension 50°/declination +15°, moving right ascension 80°/declination −10°.

| Geometry | Computed arc | Under 1°/year diagnostic |
|---|---:|---:|
| Exact proportional semi-arcs | **42.17434402835045°** | 42.174344 years |
| Placidean under-pole approximation (restricted branch) | **42.20081504892782°** | 42.200815 years |
| Regiomontanian position circle | **46.44911785127838°** | 46.449118 years |

Regiomontanian minus exact semi-arcs = **4.2747738229°**, equivalent to 4.2747738229 *model years* under the deliberately chosen 1°/year key. This is geometry, **not a real forecast**.

The second invented example agrees with the previously audited two latitude-sensitive horizon contacts: **10.6533240674°** (β=0) versus **5.5081832727°** (β=+5). Distinct historical time keys can further separate ages without changing geometry.

### Tests and actual independent checks

- **Nine unit tests passed** for the examples, horizon altitude, equatorial limit, branch rejection, phase inversion, and a sample of historical numerical interpolation (`58→64→70`).
- **20,000 deterministic phase-inversion attempts** in the unit suite across both hemispheres passed where ordinary rising/setting was defined.
- **5,000 further randomized phase/contact trials**: 4,774 admitted; max phase-inversion error ~`1.14e-13`°, max contact-phase difference ~`3.52e-12`°. The other configurations lacked an ordinary rising/setting solution; these are not silent numeric successes.
- **6,000 off-angle cases** within the documented northern/east/above branch: independent Cartesian position-circle intersections agree with independently coded auxiliary-angle pole equations to maximum `1.14e-13`°, with maximum position-circle plane residual `1.79e-15` (unitless).
- Unit tests also reject a clearly circumpolar ordinary semi-arc case and unsupported under-pole hemisphere/segment combinations.

The Cartesian and auxiliary-angle solvers are **distinct mathematical formulations written in the same research pass**. Their agreement validates a restricted spherical construction, **not** external software parity, the historical attribution of every variant, or its capacity to predict life events. Neither implementation takes a birth date, charts a person, computes secondary motion or supports all under-pole quadrants.

### Implementation inventory

- `geometry_reference.py`: pure functions for equatorial inputs; proportional semi-arc phase; independent Cartesian Regiomontanian circle solver with semicircle/root selection; **restricted** Placidean under-pole branch; signed ascensional difference and horizon domain checks; symbolic/mean-solar diagnostics. Nonapplicable combinations return `DomainError`.
- `test_geometry_reference.py`: nine deterministic unit-test methods with synthetic inputs only.
- `run_verification.py`: repeatable randomized parity and numerical receipt generator.
- `VERIFICATION.json`: actual test counts, error envelopes, branch restrictions and nonclaims.

## 4. Consequences for the larger research framework

**Add as research-only evidence, not production predictions:**

1. An orthogonal configuration tuple: `coordinate_frame`, `geometry`, `fixed_point`, `moving_point`, `aspect_provider`, `latitude_policy`, `time_key`, `converse_semantics`, `source_version`, `software_build`, `uncertainty`, and `auxiliary_rule_set`.
2. Each historical rule keeps `Gansten_secondary_claim`, `Ptolemy_Robbins_English`, `Lilly_original_annotation`, and `independent_engine_test` as separate evidence classes. An empty cell means **unverified**, not contradictory.
3. Registration of original source table anomalies (including Lilly's degree/minute rows) without silently repairing the primary text.
4. Interpretation/forecast scoring remains isolated from coordinate math. Existing frozen HD or Western scoring rules are **not modified**, and no human outcome was consulted.

## 5. Precise remaining frontier

**Priority A — Mathematical historical parity.** Run an independent primary-directions application or another trusted engine with explicit matching settings on synthetic inputs; compare nonzero latitude, intermediate house cusps, direct/converse modes, southern quadrants, and arc/time-key conversions. Extend under-pole beyond the current restricted branch only after independently sourcing its full quadrant equations. Compare the *literal* Lilly Naibod tables rather than assuming rational constants are identical.

**Priority B — Primary sources.** Independently examine original Regiomontanus/Placidus/Morin/al-Qabisi procedures and reconcile Gansten's D07/D19/D21/D51 versus the actual formulas. Lilly original cusp-direction examples and Ptolemy's Greek manuscript variants are separate tasks. An uncollated secondary attribution must not become executable historical fact.

**Priority C — Empirical testing.** Only after geometry, historical configuration and interpreting rules are frozen, compare out-of-sample dated events against preregistered nulls, with person-level separation, explicit non-events, a multiplicity cost for adding aspects/keys, and documented unrectified birth time. This phase **has not begun**.

## 6. Completion boundary

**This task's accomplished result:** a specific source-reconciliation matrix and a working, tested, synthetic geometry comparator now exist. This is a bounded material advance beyond the Kindle audit. It does **not** settle all 62 Gansten disputes or integrate a new predictive method into production. The next safe task is historical software parity plus critical-source collation; no personal forecast, religious/medical assertion or re-ranking is supported.