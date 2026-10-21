# Pinned Zi Wei source charts: fictional uncertain local clocks, DST folds and gaps

**21 October 2026. Historical-textual and computational research only.** Neither source passages nor clock-calculation agreement demonstrate a measurable correlation between Zi Wei chart placements and real human behavior. No participant, actual birth record, clinical claim or calibrated prediction appears here.

## New engineering capability

The earlier source-engine calculation required a fictional *already-known UTC instant interval*, which is not the typical input for a birth record. This extension instead accepts exactly defined **fictional, local civil wall-clock center ± a bounded integer-second margin**, plus an explicit IANA timezone and longitude. It checks **each local wall-clock second** with Python's IANA `zoneinfo` conversion and both PEP-495 DST fold candidates. A candidate UTC instant is kept only if converting it back recovers **both the exact local civil wall clock AND fold**. The solution is independently checked against the original accepted Zi Wei natal-time bridge; no arbitrary fold selection, no silent gap-forward shifting. Accepted wall seconds may map to one or **two** UTC instants; nonexistent wall seconds map to zero. Distinct candidates are SHA/source-lock validated, sorted into contiguous nonoverlapping UTC components and passed through the previously accepted original Chinese traditional 14-principal-star calculator with **all four declared** reference-calendar and Earthly-hour policies. The traditional source leap always-as-next method is held fixed rather than chosen after seeing answers.

Every synthetic local clock was hardcoded before results were evaluated. The input schema refuses unspecified zones, negative/oversized margins, extra personal DOB/identity fields and source status changes. This does **not** implement uncertainty distributions for actual people's birth records or support historical apparent solar hour, alternate Zi-day23:00 or Chinese astrological time interpretation disputes. Those remain explicit gates.

## Six original-source synthetic wall-clock tests

| Completely fictional local-clock window | Local wall seconds | Valid possible UTC seconds | Nonexistent wall seconds | Source-chart states |
|---|---:|---:|---:|---:|
| New York 2026-11-01 01:30 ±90s (fall DST fold) | 181 | **362** | 0 | **2** |
| New York 2026-03-08 02:00 ±90s (spring gap overlap) | 181 | 90 | **91** | 1 (unusable: gap) |
| New York 2026-03-08 02:30 ±60s (wholly nonexistent) | 121 | **0** | **121** | 0 (rejected) |
| Dakar 2026-02-16 21:00 ±90s (Lunar New Year/local hour) | 181 | 181 | 0 | 4 |
| Hong Kong 1965-07-01 00:59:30 ±90s (historical DST) | 181 | 181 | 0 | 3 |
| Hong Kong 2023-03-22 12:59:30 ±90s (leap month) | 181 | 181 | 0 | 2 |

Total **1,026 local wall seconds** represent **995 distinct possible UTC instants** after all valid fold candidates and gap rejection. Each valid UTC instant is retained exactly once in source outputs. For fall New York, all 181 local seconds are repeated, and the algorithm returns TWO disjoint contiguous UTC components: **05:28:30–05:31:30 UTC** (DST UTC−4) and **06:28:30–06:31:30 UTC** (standard UTC−5). The same recorded local **01:30** maps to 05:30 fold0 and 06:30 fold1, and *both* remain eligible geometrically.

Even though civil recorded Earthly hour remains Chou in both repeated 01:30 clocks, longitude-based **mean-solar hour** differs between the two possible instants: Zi for the earlier possible UTC interval and Chou for the later. The source 14-star Life layout consequently differs: in the specific fictional New York input, local mean yields `TanLang` on the earlier fold and **no principal star in Life** on the later fold, while recorded civil yields no principal star. None of the four tested behavioral source anchors appears in either: **no affirmative human trait prediction**, despite the structural chart uncertainty.

The partly invalid spring gap is classified **ABSTAIN_PARTIAL_LOCAL_WALL_CLOCK_GAP**, even though its 90 valid seconds can be charted for diagnostics. The wholly nonexistent spring clock is explicitly **REJECT_ALL_LOCAL_WALL_TIMES_NONEXISTENT**, with no imagined birth instant or natal chart. No gap correction by shifting to 03:00 or selecting an outside UTC time.

The Dakar/Lunar New Year clock, 1965 Hong Kong historical daylight time and 2023 first leap-month hour examples preserve their multiple source-chart states and original source/transmitted lunar policy uncertainty, while never declaring behavioral conclusions. The original 2057-09-28 two-software lunar disagreement is also rejected as a **whole source date**, with no fallback to an astrology school selected on personal responses.

## Correct scientific interpretation

The original transmitted `紫微斗數全書 卷二` is not independently authenticated ancient printed Ming material or an independently translated personal chart rule. An algorithmically consistent star position under **some** specified civil clock/calendar school is NOT an empirically verified individual prediction. Choosing either DST fold because it better matches a participant is prohibited outcome leakage. When an uncertain clock includes nonexistent local seconds, the source panel reports unusable rather than inventing an imputed timestamp. A chart-invariant status such as *none of the four nominated source stars are present* is still **an abstention**, not evidence a person lacks generosity, competitiveness, etc.

Source co-star conjunctions/benefic-malefic mitigations, auxiliary stars, other eleven house domains, traditional apparent solar time, birth data validity, cross-cultural psychometric questionnaire, calibrated score distributions, matched natal decoy charts, consent/ethics and actual blinded human predictions remain OPEN. Existing owner's and Hale's exposed questionnaires are development examples, not an untouched final confirmation cohort.

## Provenance and tests

The existing original 14-star/pinned two-calendar/IANA source-engine work from accepted exact Git commit `fb6b30b1ca67ff62fecc0c4ea7f3e4d0553640d4` and last 22 source file hashes remains unmodified. The parent original finite UTC interval checker/report are pinned by exact Git commits/hashes: original accepted checker `dae5ebe7a519405b0f0572d6cc79db4d41d17f5d`, parent worker SHA `8fdcea04b516770df41ce2bff48ccbcb9ef5c8491dcbc09f67abf737caba84d4`, parent check script SHA `75f33c16e98f9fc09e6d00318465a9741a32f09c9b0155f43add99d77166f92d`, parent report SHA `717ebb5a1020aa275e495b6f42ac534229346b52607eb142d293556aec1b118f`. The existing independently computed HKO original date/source bins and lunar_python1.4.8 + sxtwl2.0.7 software/binary tree SHAs are retained; no compiled third-party native package is redistributed.

`worker_synthetic_local_wall_clock_to_UTC_set.py` enumerates all valid local-wall-clock fold and gap mappings and groups exact UTC instants. `run_source_pinned_local_wall_UTC_union.py` reconstructs an isolated accepted source-engine tree without modifying it. `PINNED_SOURCE_SYNTHETIC_WALL_CLOCK_UTC_FOLD_UNION_V1.json` preserves 995 possible UTC mappings, seven source rejection checks and all source-chart state/abstention outputs. `test_synthetic_wall_clock_UTC_union.py` 20 source and negative-control tests pass, including direct original `zoneinfo` fold/gap tests. Ruff lint clean.

**Next action**: finish immutable cold portable source archive, accepted Git readback, then prioritize the **original-source conjunction/mitigation resolution rules**, not fabricate co-present star meanings from the four introductory snippets. Prior 120 distinct source-chart toy states had 22 with co-located selected stars; a source-true conditional chart-to-question interpretation still needs much more than synthetically preserving clocks. No real human astrology predictive validity yet.
