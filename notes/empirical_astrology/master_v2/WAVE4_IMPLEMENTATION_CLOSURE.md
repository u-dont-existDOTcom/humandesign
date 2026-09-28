# Wave 4 implementation closure

Date: 2026-09-28

## Outcome

The seven implementation findings in the independent Wave 4 Pro gate are mechanically closed at remote implementation commit `35eb068dd55e5cd3e67910192327765b48bc1dbd`, tree `60ffe26538f9c912e9f7698afe09a4eb43259571`.

This does **not** change the Pro scientific decision or authorize launch. The frozen model remains `literature_model_v1.0.0-wave3b-reaffirmed-20260928`: TN-001 is the only primary birth-derived feature; executable astrology mappings, interactions and weights remain empty. No eligible human data were supplied, so there is still no human effect, null, robustness, power or replication result.

The governing Wave 4 Pro gate is remote decision commit `0f4a1305a26be95cecd473e493a93d640854ac23`. The exact machine-readable closure is `data/empirical_astrology/master_v2/wave4_implementation_closure.json`.

## Findings closed

| Finding | Mechanical closure | Evidence |
| --- | --- | --- |
| W4-F01 | Pair/date counts remain hospital-level; the two exposure fractions are now evaluated across each complete 20-hospital cohort. Selected sites are never replaced after a failure. | Complementary-hospital and integrated 2,000-pair cohort fixtures. |
| W4-F02 | Git commits use real 40-hex object IDs, resolve as commits and satisfy evidence ancestry. File hashes remain 64-hex SHA256 and every strict freeze hash must bind to repository-local bytes. | Real-checkpoint, malformed-ID, missing-object, ancestry and byte-mutation fixtures. |
| W4-F03 | The exact Pro gate bytes and its reviewed decision/registry/model hashes are pinned. Runtime scientific constants and authorization boundaries are checked; comprehensive mutations fail closed. | Seed, scoring-key, nuisance-order, eligibility, null, multiplicity, threshold, permission, feature and gate-rewrite tests. |
| W4-F04 | One mandatory design builder now joins verified eligibility, global relationship retention, one hospital per network, eligible-network determination, seeded A/B allocation, cohort support, lineage logging and development/A/B isolation. | A 41-network adversarial roster leaves exactly 40 eligible networks after a cross-network relationship exclusion and produces disjoint 20-network cohorts. |
| W4-F05 | Raw birth and response envelopes validate provenance, resolution, civil time/DST, age, language, singleton/knowledge exclusions, collection window, questionnaire identity, one immutable complete response, withdrawal and attrition without replacement. | Negative fixtures cover every represented exclusion and preserve a missing selected pair rather than re-pairing. |
| W4-F06 | Full and restricted WLS use stable QR. CR1 covariance uses triangular influence solves, not inverted normal equations. Unresolved rank/numerics fail closed. | At the Pro gate's `epsilon=1e-7` counterexample, beta differs from an explicit fixed-effect QR reference by `3.24e-11` and SE by `1.65e-12`; this is software evidence only. |
| W4-F07 | Gap bounds, all 20 LOO fits and all 21 diagnostics produce complete ordered fit/failure ledgers. A failed bootstrap draw invalidates the run and records its index. | Fixtures force early failures and verify every later prespecified attempt remains present. |

## Verification

- Focused empirical-astrology suite: **69 passed**.
- Full repository suite: **330 passed, 3 skipped, 0 failed**. The three skips require unavailable official Swiss Ephemeris smoke-test files.
- Ruff: passed.
- Focused strict type check: passed.
- Numerical audit: CPython 3.12.14, NumPy 2.5.3, SciPy 1.18.1, OpenBLAS 0.3.34.106.0, float64, one BLAS thread with `OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1`.

The original Wave 4 no-data artifacts were not regenerated or rewritten. Their hashes remain exactly those reviewed by Pro, including result registry `3e91f16171e7925770c18f3edc87a3536e8b08eeb11bae6bd4cf980cc0880409` and original handoff `8e30c07585e307a32f6772fce65893acf6a1d8b3c22a38735daad34ddf39e236`.

## What remains blocked

Mechanical defect closure is not operational readiness. There is still no eligible hash-bound non-owner development reference, no human development result, no actual frozen A/B design, no operational permission/custody package, and no development residual template. Consequently the eight human baselines, empirical robustness and diagnostic families, and the exact 5,000-run-per-cell residual-transfer power/null calibration remain `NOT_EVALUATED`.

The integrated residual-transfer simulator and final two-cohort confirmation gate also remain required before a launch proposal can return to Pro. Synthetic fixtures cannot substitute for these inputs. Recruitment, scored-outcome collection, owner-known fitting, feature/weight revision, production and person-level use remain unauthorized.

The only authorized next direction is outcome-blind acquisition/feasibility and protocol preparation under ordinary data-access authority. If the complete Pro prerequisites can be assembled, they must return for a new explicit launch adjudication before any scored prospective collection.
