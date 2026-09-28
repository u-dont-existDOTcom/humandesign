# Pro handoff — Wave 4 implementation closure

Date: 2026-09-28

## Gate being answered

This handoff answers only the seven mechanical findings in `PRO_DECISION_WAVE4.md`, published on the decision branch at `0f4a1305a26be95cecd473e493a93d640854ac23`. It does not request or make a new scientific-model judgment.

Repaired implementation checkpoint: `35eb068dd55e5cd3e67910192327765b48bc1dbd`  
Repaired tree: `60ffe26538f9c912e9f7698afe09a4eb43259571`  
Machine-readable closure: `data/empirical_astrology/master_v2/wave4_implementation_closure.json`

## Disposition

W4-F01 through W4-F07 are mechanically closed with adversarial tests. The Pro scientific verdict is preserved verbatim in effect: same-hospital, same-local-date TN-001 remains sole primary; all astrology mappings, interactions and weights remain empty; aspect/orb tightness and angularity remain inactive secondary templates. No feature, coefficient, threshold, cohort rule or scientific version was changed.

No human outcome file was opened. Eligible human N, pair count, site count and independent-network count remain zero. The original 36-row Wave 4 registry remains the historical no-data record and was not overwritten.

## Verification record

- focused suite: 69 passed;
- full suite: 330 passed, 3 skipped for missing official Swiss Ephemeris smoke files;
- Ruff and focused strict typing: passed;
- stable numerical counterexample: beta/SE agree with an independent explicit-fixed-effect QR calculation within `3.25e-11` / `1.65e-12`;
- actual single-thread runtime recorded: Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1, OpenBLAS 0.3.34.106.0, float64.

## Remaining gate status

**Prospective launch remains blocked.** Mechanical closure does not supply:

1. the required eligible 20-network × 100-pair non-owner development reference;
2. the eight empirical baselines, human robustness and 21 diagnostic results;
3. actual frozen and independently audited A/B target designs;
4. ethics, consent, data-access, custody, instrument and response-freeze operations;
5. the fixed development residual template and exact design-specific 5,000-run null/power calibration;
6. the integrated final per-cohort and two-cohort success gate; or
7. a separate explicit Pro launch decision.

There is therefore no launch, validation, null, effect, power or replication claim. No owner-known fitting, feature/weight revision, prospective recruitment, scored-outcome collection, production or person-level use is authorized. The next permitted work is outcome-blind data feasibility and protocol readiness under ordinary access authority, with every failure retained.
