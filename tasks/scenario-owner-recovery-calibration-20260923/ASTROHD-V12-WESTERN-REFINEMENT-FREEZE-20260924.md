# AstroHD V1.2 Western-only refinement freeze — 2026-09-24

Status: **FROZEN AFTER HOURLY V1.2 RANK, BEFORE MINUTE REFINEMENT / POST-RESULT DEVELOPMENT / NOT VALIDATION**.

## Trigger

The transparent V1.2 Western-only hourly scan passed the known development regression and placed the exact recorded moment at rank #3–#4 versus the 876,601-state hourly universe. Minute refinement is therefore admitted.

## Frozen refinement procedure

1. Take the **top 10 hourly candidates** from the frozen Western-only V1.2 century ranking.
2. Around each top-10 hour, create a symmetric **±12 hour** window.
3. Merge overlapping windows before evaluation.
4. Evaluate every UTC minute in the merged windows using:
   - the exact frozen V1.2 Western predicate registry;
   - direct file-backed Swiss Ephemeris SWIEPH calculations;
   - fixed Philadelphia coordinates already frozen in the registry;
   - the exact feature prevalence from the frozen hourly century universe;
   - the frozen current 19-domain behavioral confidences;
   - the frozen Western feature salience/directness weights.
5. No orb, feature, house, location, weight, prevalence, behavioral translation, or scoring rule may change after this freeze.
6. Rank minute states by Western score only. Exact score ties remain ties; do not use distance to the known birth time as a tie-break.
7. Report:
   - each distinct refined peak/plateau among the top-hour windows;
   - whether the recorded 1985-01-29 10:25 UTC moment lies in a top refined plateau/neighborhood;
   - the local Jan 29 best minute/plateau and its distance from the recorded moment;
   - any higher-scoring refined neighborhoods.

This rule refines the highest-scoring hourly neighborhoods generically; it is not restricted to the recorded date.

## Interpretation

If the recorded moment remains inside a leading refined neighborhood, V1.2 Western-only records **DEV_PASS_NONVALIDATING** on this owner case.

If refinement materially displaces the recorded neighborhood, preserve the hourly improvement but classify exact-time recovery as unresolved/failed accordingly.

A development pass does not establish prospective validity.
