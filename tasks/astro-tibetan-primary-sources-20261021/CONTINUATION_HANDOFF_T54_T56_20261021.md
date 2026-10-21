# Tibetan astrology continuing source study — T54–T56 handoff (21 October 2026)

**Root owner request (verbatim):** “ok then start reading everything you need that's free plus these, in turns, to merge into the other readings we are doing for astro system”; successive “continue.” **ROOT STATUS OPEN**: read Tibetan and free mathematical sources; merge with Lilly/Ptolemy, Jyotish, BaZi and Zi Wei source studies; independently calculate complete natal/annual/event-timing features; freeze and test real untouched human forward/reverse predictions versus matched decoys and non-astrology baselines. Source counts and synthetic calendar agreement do not satisfy this goal.

## Accepted parent and new branch

Previous accepted T51–T53 branch `research/astro-tibetan-t51-cornu-janson-math-20261021`, exact remote and laptop commit `4110a30342f05dd58a4167634370db52b1baa436`. Accepted documentary notes TIB-R0001–0488 (488). New current branch `research/astro-tibetan-t54-janson-true-dates-20261021` created from exact previous commit, with isolated laptop worktree `/mnt/hdd/storage/joel/development-worktrees/humandesign/astro-tibetan-t54-true-dates-20261021`. Actual final remote HEAD to be verified on resume; not inferred here. All edits are confined to `tasks/astro-tibetan-primary-sources-20261021/`.

New historical source annotations T54 = **12** Janson mathematical source points, IDs **TIB-R0489–0500** (cumulative 500). T55/T56 add **0** historic counts (respectively an explicit assistant inference/policy experiment and a code sensitivity measurement). No changes to prior source registries, participants, Western/Chinese/Jyotish accepted model files.

## Source, algorithms, artifacts

`batches/T54/tibetan_true_dates.py`: Original MIT-licensed source-formula implementation of Svante Janson's *Tibetan calendar mathematics* (2014 arXiv:1401.6285v1), §§5–9, Appendix A.2. Exact `Fraction` source rates; Phugpa epochs 806/1927/1987; Tsurphu 1732/1852; explicit Janson rounded lunar anomaly vs Dharmashri/Henning exact option. Calculates true tithi-end JDN, leap months, skipped/repeated days, two-way Gregorian civil date-label ↔ Tibetan date-label and Losar. **DOES NOT convert a precise UTC instant to physical sunrise, modern ephemeris or true physical Moon.**

`batches/T54/README.md`: full methods, scope, mathematical vs empirical validity and source reuse boundaries.

`batches/T54/JANSON_TRUE_DATE_12_SOURCE_NOTES_V1.json`: 12 new source-based Janson notes R0489–0500.

`verify_t54_true_dates.py`: 10 published Janson Losar dates, five source epoch parity, full-calendar days across 12 Tibetan years with skip/duplicate continuity and independent roundtrips, Cornu 1950 tithi parity, source policy validation; chains previous T53 verification.

`compare_t54_independent_tibcal.py`: independent external MIT Python reference `dorjeduck/tibcal` pinned SHA `01591b5bf03d038b864c4138fde3cc4285ca8001`, **4386 date comparisons across both Phugpa+Tsurphu and six years, 0 mismatches**. Upstream clone stays in `/tmp/hd-tibcal-ref-20261021`, not committed/vendor-copied. Receipt saved in `batches/T54/DIFFERENTIAL_PYTHON_RECEIPT_V1.json`.

`compare_t54_independent_javascript.py`: independent MIT JavaScript `hnw/date-tibetan`, pinned `7651b8b579c8332442198cc0d9ca14d0b0e8b3a8`, **2193 Phugpa date comparisons, 0 mismatches** (subset of the prior 4386 dates, NOT disjoint additive sample). JS clone in `/tmp/hd-date-tibetan-ref-20261021` with npm production dependencies installed using `npm ci --omit=dev --ignore-scripts`. Receipt saved in `batches/T54/DIFFERENTIAL_JAVASCRIPT_RECEIPT_V1.json`.

`batches/T55/natal_mean_dawn_candidate.py` and `EXPLICIT_BIRTH_MEAN_DAWN_POLICY_V1.json`: optional **ASSISTANT_INFERENCE / BOUNDED EXPERIMENT** to use Janson theoretical 05:00 LMT dawn at independently supplied longitude for an UTC-aware birth instant (NOT verified universally authentic outside Tibet). Requires explicit policy and no default. Cornu Paris 1950-11-15 17:00 civil time (16:00 UTC) at 2.3522° E converts to LMT 16:09:24.528 and Iron Tiger year / Water Ox month / Wood Ox lunar day / Fire Monkey hour, with mewa/five forces matched. Source clock labels conflict was previously audited in T53. No patient or actual user birth data used. `verify_t55_birth_policy.py` tests author example, sunrise-free theoretical dawn boundary, Losar flip, longitude, invalid time/zone or policy. Local mean solar clock output deliberately has **no UTC timezone suffix**.

`batches/T56/compare_anomaly_policies.py` and `ANOMALY_POLICY_SENSITIVITY_1987_2051.json`: over 65 Tibetan-year labels, 24,120 tithi-end dates per calendar, **6 Phugpa and 5 Tsurphu** tithi-end **JDN differences** between rounded and Dharmashri exact lunar-anomaly increment, **0 Losar differences**. Not 11 unique participant birthdates, not predictive accuracy. Keep source variants separate before human testing.

`verify_t54_t56_all.py` verifies 500 continuous source IDs across accepted 447 old +41 T51–T52 +12 T54, fixed Python/JS source SHA receipts and 0 differences, T55 experimental source status, T56 sensitivity, and chains all earlier Tibetan verification scripts. **Actual human validation: ZERO.**

`CROSS_LANE_INTEGRATION_T54_T56.md`: full research methods, source/inference boundary and comparative astrology integration.

## Safe next frontier, no repeated accepted work

**Next TIB-R0501**. Implement and independently check Janson §10's lunar mansion (0–26), yoga (0–26), karana, theoretical true Sun/Moon coordinates and Tsurphu-specific variants, then reconcile with Indian Jyotish and Chinese Zi Wei dependencies. Reuse independent verified third-party calendars instead of rewriting astronomy unnecessarily; additional independent candidates `lscalendars/tibcalendar` (GPL, evaluate read-only) and `gantemur/caltib` (check API/version/license and source parity). Finish Cornu remaining practical/electional text, Henning I–V/remaining VI, free Erlewine manual and original Tibetan witnesses resolving numbered source issues. **Do not silently resolve** source contradictions, Papme subject-sex vs birth-year-polarity, calendar year convention, or astronomic/mean-solar day boundary. No participants recruited, no anonymous profiles scored, no medical/mortality/ritual advice or paid/public action taken. Root OPEN.

## Validation/remote acceptance

Run (from task dir) `python3 verify_t54_t56_all.py`. Optional independent parity requires exact source clones via CLI as documented in T54 README and is already receipted. Fetch current remote branch head; verify no changes outside Tibetan task folder, confirm exact tests PASS and handoff is present on remote. Deliver owner report locally in OS-designated `~/Téléchargements/` (linked to HDD) if owner device remains authorized and online. On subsequent “continue,” start at TIB-R0501; **do not repeat T01–T56 successful calls**.
