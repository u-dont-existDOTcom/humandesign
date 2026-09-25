# Lilly horary retrospective — Chapter LXXXII job rule v1 freeze

Status: **POST-v0 DEVELOPMENT REPAIR / FROZEN BEFORE V1 DEVELOPMENT SCORES / NOT VALIDATION**.

## Motivation

The v0 perfection-only classifier produced 0 YES / 7 NO / 2 DEFER and no gain over the covered-set majority baseline. This is a direct model defect because Lilly's own Chapter LXXXII explicitly allows obtaining office/preferment through several configurations other than principal-pair perfection.

## Source boundary

Authority: William Lilly, *Christian Astrology* (1647), Book II, Chapter LXXXII, pp. 444-446, "Of Government, Office, Dignity, Preferment, or any place of Command or Trust, whether attainable or not?"

v1 adds only mechanically unambiguous affirmative clauses that are directly stated there. No empirical weights, fitted coefficients, score thresholds, or outcome-derived priorities are introduced.

## Frozen v1 affirmative clauses

For job/preferment questions: L1 = ruler of Ascendant; Moon = co-significator; L10 = ruler of 10th.

Return YES if **any** of these source clauses is true:

1. **PERFECTION** — Moira's Lilly-1647 engine finds DIRECT, TRANSLATION, or COLLECTION present between L1 and L10.
2. **RECEPTION** — L10 receives either L1 or Moon by any Lilly essential dignity: domicile, exaltation, active triplicity, term, or face.
3. **L10_IN_1_FASTER** — L10 is physically in the 1st house and its absolute daily longitudinal motion is faster than L1.
4. **L10_IN_1_BENEFIC_JOIN** — L10 is physically in the 1st and is currently within the admitted Lilly moiety of a Ptolemaic aspect to Jupiter or Venus.

The Chapter also contains additional success clauses whose finite implementation requires further interpretation (especially "impedited", multi-planet chains, and the detailed Mars/Saturn conditions). They are **not** silently invented here. They remain omitted from v1 and are research debt.

## Verdict

- YES if any frozen affirmative clause is true.
- DEFER if the chart/principal significators are not evaluable or a relevant positive perfection path is indeterminate and no other affirmative clause is true.
- NO otherwise.

No clause stacking or weights: multiple affirmative clauses do not increase a score.

## Repair-admission gate

Run v1 first on the already-revealed v0 development cases. V1 is admitted to a fresh hidden-outcome sample only if it materially improves the direct motivating failure without changing this freeze. At minimum it must:
- generate at least one YES prediction; and
- correctly recover at least one of the known YES development cases that v0 failed to answer/called NO;
- not reduce development covered-set accuracy below the v0 75% baseline.

A development pass remains non-validating.
