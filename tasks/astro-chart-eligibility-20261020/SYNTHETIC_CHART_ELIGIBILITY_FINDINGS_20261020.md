# Zi Wei four-source-anchor chart applicability — synthetic feasibility audit (20 Oct 2026)

**Research result: the four-source-anchor toy scoring model is structurally unsuitable as a general natal predictor without a new, prespecified conjunction/precedence policy.** This is a reproducible **synthetic chart coverage finding, NOT human astrology predictive accuracy**.

## Verified data and exact provenance

Read and SHA-verified the **unchanged accepted original-source-engine / Iztro comparison** on historical project branch `research/astro-chinese-iztro-external-chart-parity-20261020` commit `6f4a75febc1624e44b54d724422804a05f31fd12`, JSON `tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-12/IZTRO_2_6_0_FULL_312_CHART_COMPARISON_V1.json` exact SHA `01efe5181d7c9d07a6c9f780df9d03b557b356baa4ca3770464f38e8552feaa5`, byte size899155, retrieved by `git show` without modifying source or another worktree. That **312-row vendor parity benchmark is NOT 312 independent charts or 312 real people**: ten selected officially checked HKO lunar dates 2023–28 × twelve synthetic hour branches × two sex-coded computational options and some duplicate leap-treatment variants.

The four candidate source-phrase IDs and corresponding stars are SHA-locked to the earlier SYNTHETIC-only source mapping `SOURCE_TO_BEHAVIOR_CANDIDATES_V1.json` exact SHA `acd1fef1b9764bfac4525785ee1fd42e7dac2727880e829ee038aa9562db8a62`: WuQu (武曲; resoluteness), LianZhen (廉贞; contentiousness), TianLiang (天梁; helping) and PoJun (破军; striving). Their Life-palace astrological applicability and interpretations are not independently validated. We make no chart-birth or participant DOB inference.

## Deduplicate physical SOURCE charts before evaluating feature coverage

All comparison rows from the same synthetic Gregorian reference date and two-hour Earthly Branch were proven to have identical **SOURCE** Life/Body palace, five-phase bureau and full positions of 14 principal stars even when male/female and vendor leap options differed. Therefore group them into **120 unique synthetic source-chart configurations**, exactly 10 dates × 12 hour branches. Keep all 312 raw vendor comparisons separately: source-vendor raw results 192 agreeing and120 disagreeing, 168/168 nonleap agreements, 24/144 leap-comparator agreements. Some apparent duplicate vendor variants match and others do not: reporting a single `match` for a deduped source chart by taking the first row is scientifically incorrect. Report `all` vs `any` over vendor variants separately, with source leap-month policy **always-next** unchanged.

| Chart-source property | Among 120 unique synthetic configurations |
|---|---:|
| No major star in Life palace | 23 |
| Exactly 1 of 14 major stars in Life | 59 |
| Exactly 2 of 14 major stars in Life | 38 |
| At least one of **four** chosen stars | 34 |
| None of four chosen stars | 86 |
| Exactly 1 selected star (possibly alongside other major star) | 31 |
| Both 2 selected stars in Life | 3 |
| Selected star with any other co-located principal star | 22 |
| **Exactly one selected star, and no other principal star** | **12** |
| Structural abstentions under strict four-star model | **108** |

The 12 strict synthetic eligible states are **PoJun 6, TianLiang 4, LianZhen 2, WuQu 0**. They include **10 nonleap states** where *every* vendor duplicate agrees on the SOURCE placements, and **2 leap states** with **no raw matching vendor case** under the two vendor options tested. The deduplicated raw comparison reports **84/120 all-vendor-matched**, **96/120 some-vendor-matched**, and **24/120 no-vendor-matched** source states. These are strictly software/source school comparisons, not human psychology.

## Consequences for the test and questionnaire design

1. **Abstain rather than make invalid predictions.** A rule of “the Life palace contains precisely the selected main star and nothing else” is satisfied by only **12/120 toy configurations**, of which 10 agree with the independent vendor's raw school policy. Nothing in this 10-date purposive sample licenses estimating a population prevalence or individual diagnostic coverage. No WuQu-only configuration appeared here, but this is not proof there are none in the full calendar.
2. **Co-location and dependencies matter.** Among 34 source charts containing a chosen star, **22** have at least one other principal star in the same Life palace. Three configurations have **two of the chosen stars**. Historical texts discuss combinations/mitigations, so choosing a single trait per chart without a historically supported, *pre-outcome* precedence rule would be cherry-picking. The original source descriptions are broad and their English behavioral translations remain unverified.
3. **No selected star ≠ a negative trait prediction.** The 86 source charts without any of four chosen stars are **unscorable under this source-limited model**, not inverse evidence (e.g., “not helping” or “not competitive”). Do not invent negative-control effects from unmentioned natal features.
4. **Conditional leap convention must be fixed in advance.** The original source always-next leap policy and Iztro alternative `fixLeap` variants produce 120 raw failures. Never choose the method that makes the chart/person fit after looking at their questionnaire.
5. **Metric reuse still only engineering.** The earlier deliberately aligned 4 fake star-token synthetic scorer's top1=1.0 is by construction. It cannot be presented as 4/4 real humans, 312/312 eligible charts or proof of a working birth-derived chart-to-behavior model.

## Immediate recommended next development step

Develop and preregister a **source-condition resolver** across at least main-star conjunction combinations, ideally bounded to historical passages with clear positive and negative branches and independent chart-calculation parity. Retain an explicit `ABSTAIN_UNSUPPORTED_CONTEXT` output for configs lacking a frozen rule. Separately verify the full Gregorian civil timestamp→relevant lunar date/day/time-branch, birthplace historical IANA zone, source leap and traditional apparent-solar conventions. On synthetic cases, compare same preselected school to independent oracle before using any real participant data. Only once chart, source-to-target mapping, psychometric outcomes, score, decoys and consent are actually frozen may G01–G10 be reevaluated. Actual prospectively blinded humans **zero**.

**Source**: machine-readable `SYNTHETIC_CHART_FOUR_ANCHOR_ELIGIBILITY_AUDIT_V1.json`, reproducible `audit_synthetic_natal_feature_coverage.py` and 20 source SHA, dedup, school and malformed case tests. No personal data or original source registry changed.
