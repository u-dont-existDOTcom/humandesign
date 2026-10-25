# Research checkpoint — private natal-to-direction adapter

Date: 25 October 2026. Task: `western-private-natal-bridge-20261025`.
Research branch: `research/western-private-natal-bridge-20261025`.
Parent: `research/western-primary-direction-blind-pilot-20261025`, commit `c228948bcac71c9f275b3e3e057b190ea1891d55`.

**Root owner outcome OPEN:** construct historically auditable, source-differentiated Western, Hellenistic, Jyotish, Chinese and Human Design techniques and compare preregistered, prospective/out-of-sample chart-derived predictions against truly untouched human outcomes with matched/null controls. Passing source and synthetic tests does not validate prediction.

## This turn's bounded executable contribution

Connect the already verified Swiss Ephemeris `DirectionBirthSnapshot` to the eight originally enumerated Lilly source-associated candidate directions and the separate modern prospective scaffold; calculate contacts at **all integer-minute offsets** from a *synthetic or externally normalized private UTC birth tuple*. Build only a **pseudonymized, keyed-HMAC commitment** of the private input and natal features, plus source/code/ephemeris digests, sanitized contact windows and unresolved source statuses. Do not use the owner's own birth chart or any person's observed events as a trial case.

A plain SHA-256 of DOB/time/location is potentially brute-forceable; use HMAC-SHA256 with an externally stored high-entropy key and never write the key or raw natal tuple to Git. This is **engineering hardening**, not proof of secure human consent, preregistration or out-of-sample accuracy.

### Boundaries
- **Modern diagnostic** method only: `regiomontanian_position_circle`, current engine software `direct` convention and one symbolic arc-degree/year, modern source ray β=0°; do not label authentic complete Lilly or Argoli.
- Preserve all eight source families, including source conditions and six not-yet-scoreable event domains. Distinguish this Regiomontanian adapter from the 96-chart *proportional semi-arc* development occupancy analysis; the published 0.4233% cannot be reused as this adapter's population incidence.
- Model time uncertainty with the complete integer-minute grid, not a falsely certified continuous interval; candidate absent at any offset has `timing=null`, not cherry-picked.
- Require already normalized offset-aware UTC time; **no** invented historic timezone/DST resolution.
- No real human birth records, names, personal events, secrets, consent flags or participant responses are to be committed, logged or delivered.
- Do not call an in-memory receipt an externally timestamped human prediction freeze; actual intake, secure write-once approval and independent outcome coding remain separate human study gates.

### Acceptance for this scoped iteration
- A production-engine-connected research adapter and optional private input CLI, verified against the pinned `sepl_18.se1`/`semo_18.se1` hashes and returned strict SWIEPH mode.
- Synthetic-only integration, invalid-input, unsanitized-output, wrong-ephemeris, and privacy-failure tests; prior Western primary-direction test suite remains green.
- Git-committed code/provenance, source-visible reporting of remaining human-test gaps, local direct artifact handoff with runnable test commands.

**Completion of this engineering slice does not satisfy the original owner research goal.**


## Executed technical result

- Implemented `src/hdmatch/astrology/western_private_natal_bridge.py`: normalized-UTC-only private input, exact eight primary-source source IDs checked against original JSON SHA-256s, strict Swiss 1800–2399 local `.se1` source checking and returned SWIEPH flag, separate named modern Regiomontanian position-circle direction engine and one-degree-per-symbolic-year rule. It recalculates every integer-minute offset, joins source body/ray branches, and marks unqualified or disappearing candidates **unscoreable** rather than searching for a favorable minute.
- Enforced keyed **HMAC-SHA256** of normalized private input and full birth-time-sampled natal features, using a separate high-entropy key outside Git. Plain SHA-256 of birth tuples is not treated as private. A local write-once private receipt requires external absolute paths and permissions 0600; real birth and sky coordinates/calendar dates never enter the receipt or terminal output. Source and implementation digests remain inspectable. The key and real private input were not created or committed.
- An explicitly fictional UTC 2000-01-01 test natal input was processed through the real verified Swiss files with −1/0/+1 minute offsets. Exact replay of the full sanitized result passed; the bad Swiss hash, insecure file permissions, symlinked key file, paths inside Git, duplicate writes, raw-field inclusion, bad normalized UTC, out-of-range latitude, unqualified historical conditions and incomplete uncertainty grids all failed safely in tests.
- The historical 96-chart **proportional semi-arc** developmental 0.4233% occupational-age occupancy figure is **not** transferred to this new Regiomontanian adapter. All eight source families remain in the receipt, six not eligible for modern outcome scoring. No source-conditional Jupiter/ASC claims were silently made.
- 14 focused tests pass excluding the filesystem-integrity manifest test until the final checkpoint/documentation bytes are frozen. Ruff format/lint and mypy pass. The complete suite and final file/package SHA-256 receipt follow as a single verified step.

## Required next actual research contribution

This source adapter is **engineering-complete** once the final GitHub packet and tests are verified. It does **not** create an authorized live human trial or an externally timestamped preregistration. The next owner-aligned gap is independently verified privacy/consent/timezone normalization for real birth data, secure external prediction sealing before outcome ascertainment, a preregistered observable eligibility/event scoring policy, and a genuine untouched cohort and separate astrological arms. These steps require actual independently held data and human-participant authorization, not invented files. Do not keep treating additional synthetic tests as empirical validation or presenting this adapter's receipt as a real outcome forecast.


## Final source/engineering regression receipt

The 15 focused tests passed using the actual verified local Swiss ephemeris on a **fictional** birth-time tuple. The complete inherited Western primary-directions, Lilly, Argoli, Naibod and modern-pilot regression suite passed **235/235** in this isolated research checkout. Ruff formatting/lint and mypy passed for both new Python modules. The synthetic natal run was repeated and the complete sanitized result reproduced deterministically. Negative privacy tests proved that guessed/unkeyed SHA, group-readable key files, symlink paths, raw birth-data fields, duplicate outputs, bad UTC inputs, missing Swiss source files and altered ephemeris SHA records cannot enter the accepted receipt.

**Study boundary still OPEN:** this is a useful private *engineering bridge* that integrates source and Swiss calculations; it is not a participant-enrolled study, an approved external consent protocol, an independent historical-timezone resolver or independently timestamped prediction freeze. No real individual's birth records or events have been examined. A genuinely untouched human comparison still requires external consent, validated birth-time provenance, independent opportunity/outcome coding, cross-tradition precommitted scoring and blinded controls. Do not repeat the 96-chart synthetic occupancy calculation as human predictive evidence.

Exact next continuation: resume from this branch's `README.md`, `METHOD_SCOPE.json`, `VERIFICATION.json`, the module and tests; check current remote commit/worktree; then connect actual permissioned intake/evidence infrastructure only when such a route and participant authority are verified. Continue other astrology source/coding lanes independently without making the 1644 Argoli printing a prerequisite to the named modern diagnostic.
