# Current state

## Active task override — Issue #18 owner-only release smoke

- As of: `2026-08-31`.
- Controlling task: Human Design issue `#18`, plus the owner's bounded authorization
  to merge/deploy PR `#20` and run one owner-only production questionnaire/recovery
  test. This section supersedes the older `participant-session-v1` next-action state
  below for relationship/AstroHD continuation work.
- Canonical main: `b5c2cc57513d4b5505fd23a8e4c605e4607c11b9` (merged PR `#20`; reviewed head
  `7f24ebc9936cb98db7e69a9ffa8dfbe018008a3c`).
- Canonical production: Railway deployment
  `0c26073a-ff83-449b-a976-7ae4342d7e00`, status `SUCCESS`, sourced from that exact
  main commit.
- Live state: health is green; explicit hour/minute/optional-second birth-time inputs
  for both people are present; magic-link and six-digit-code recovery are configured;
  and the private mounted volume matched exactly across the required same-geography
  Railway region-identifier migration.
- Recovery boundary: an authorized request for the owner's email produced no message
  because no saved study is associated with that address. The private check disclosed
  only a zero match count and status, not participant content. A true round trip is
  pending the owner's first fresh study using that email.
- Human-contact boundary: owner-only test authorized. No friend has been contacted;
  external sharing remains closed until the owner smoke succeeds.
- Spending boundary: `$0` incremental paid spending; no purchase or plan upgrade was
  made.
- Adequacy: operational deployment `PASS`, recovery round trip
  `PENDING_OWNER_SESSION`, scientific validity `NOT_ESTABLISHED`, release
  `OPEN_OWNER_ONLY`.
- Next executable: owner completes the live questionnaire once. Codex then requests
  and verifies a single-use recovery credential, confirms replay rejection, and
  updates the public-safe release receipt.

- As of: `2026-08-27`
- Task ID: `participant-session-v1`
- Goal: ship the first participant-facing AstroHD interview harness with immutable pre-answer predictions, candidate-blind adaptive interviewing, confirmatory reveal, and a separately labeled post-hoc holistic-profile ranking.
- Branch: `participant-session-v1`; PR `#8`.
- Primary scientific claim under test: `natal chart -> persistent trait/behavior fingerprint`.
- Secondary research layers are stored separately: `behavior + environment -> outcomes`, natal outcome increment, progression/transit timing increment, and residual chart prediction after conventional covariates.
- Evidence rule: only `trait` and `behavior` observations with valid frozen response tokens can affect the primary natal rank. Outcome, timing, environment and conventional-covariate records are retained but excluded from that score.
- Blinding rule: scientific participants should submit birth data through trusted external intake and give the conversational interviewer only the opaque `HD-...` session ID. Direct DOB entry is supported only as explicitly precommitted self-discovery.
- Prediction rule: exact chart plus human-readable frozen prediction dimensions and provenance are SHA-256 bound before the first behavioral observation. Prediction-freeze v2 also binds the exact candidate-universe digest, count, UTC range, timezone, ranking scope and engine fingerprint before evidence is accepted.
- Session rule: evidence is append-only/hash-chained; confirmatory lock/reveal artifacts are immutable; post-hoc evidence cannot modify the blind result.
- Participant result: show both the pre-reveal confirmatory rank and the final refined post-hoc rank. The latter is always labeled `posthoc_exploratory_not_independent`, even when it improves substantially.
- Interview rule: prioritize persistent patterns, childhood-to-adult continuity/change, contexts, exceptions, examples and counterexamples. Always permit an Other/free-form answer rather than forcing a category; a later free-form correction may neutralize an earlier scoring token without deleting history.
- Astronomy state: exact Swiss-Ephemeris chart calculation and historical IANA timezone resolution are implemented. A completed 100-year V4.3/V3.6 structural audit exists, and the generic Swiss-backed AstroHD broad-scan ephemeris cache is checked into the repo with provenance.
- Astronomy reference layer: `hdmatch.chart.astronomy_reference` preserves a richer provenance-bearing geocentric state (longitude/latitude/distance, RA/Dec, Cartesian position and velocity) before symbolic projection. It rejects silent non-Swiss fallback. Tropical, explicit-ayanamsa sidereal, and the validated AstroHD gate mapper are implemented as distinct projections. Real IAU constellation lookup still fails closed pending a versioned Delporte/IAU boundary implementation.
- Independent numerical audit: `hdmatch.chart.jpl_ephemeris.JplEphemerisProvider` accepts one explicit local JPL DE file, hashes it, requires `FLG_JPLEPH`, excludes derived lunar-node conventions, and rejects silent SWIEPH/Moshier substitution. `hdmatch.chart.ephemeris_audit` compares providers in arcseconds and separately records whether a discrepancy crosses a symbolic boundary. The first Astropy/DE440s comparison agrees to sub-arcsecond scale for Sun/planets; the Moon still has a convention/frame discrepancy and remains a separate unresolved audit item.
- Astronomy ablation rule: modern numerical ephemeris accuracy and zodiac convention are separate questions. Differential-test pinned Swiss output against a JPL DE-file reference; separately compare preregistered tropical, sidereal, IAU-constellation and AstroHD projections. Never select the winning projection after participant evidence is visible.
- Progression state: `hdmatch.chart.progressions` freezes a secondary `one ephemeris day = one tropical year of elapsed life` convention and can generate age-indexed progressed snapshots through the ordinary ephemeris provider. Progressions remain a hypothesis to test, not a post-hoc repair for natal misses.
- Longitudinal test rule: collect childhood/school/adolescent/adult/current behavioral transitions independently, then compare frozen progression predictions. Planned ablation is M0 natal, M1 natal+progressions, M2 natal+ordinary development/context, M3 natal+progressions+ordinary development/context.
- Angle/house warning: the known Ascendant/MC disagreement must be independently audited before angles/houses enter strong confirmatory claims. Preserve the full civil-time/timezone/location/Earth-rotation/convention chain.
- Ranking state: exact `known_birth_month` ranking remains available. `CenturyCapableParticipantBackend` adds `century_global` only when `HDMATCH_CENTURY_CACHE` points to a verified structural cache whose engine fingerprint matches the deployed chart engine; missing, corrupt, mismatched, old-schema, or out-of-horizon caches fail closed.
- Century cache semantics: cache schema v2 stores a compact `structural-chart-features-v1` record. Structural intervals split on every Personality/Design activation gate transition plus Personality/Design Sun-line transitions (profile). Non-Sun line changes are intentionally not candidate boundaries because they cannot affect type, strategy, authority, definition, centers, channels, activation gates, or profile in the current structural model. A future model that uses non-Sun line/color/tone/base must introduce a new cache version rather than silently reusing v2.
- Century cache integrity: `hdmatch.runtime.century_cache` stores timezone-neutral structural intervals as deterministic canonical JSONL-gzip shards with per-shard SHA-256s, a whole-universe canonical-row hash, structural feature hashes, engine fingerprint, boundary-policy version, Design-root tolerance, generation commit and verified range. Loading dynamically attaches participant-timezone local-date overlaps.
- Century build implementation: the original generic all-lines engine and its decade-sharded variant exceeded the 90-minute Actions limit because they repeatedly solved Design timing while resolving line transitions for every body. `scripts/build_century_candidate_cache_fast.py` now reuses the proven direct Swiss event-generation method: all gate crossings are enumerated once, Sun line crossings are retained, Design events are mapped forward through the exact 88-degree solar-arc root, and incremental structural states are periodically cross-checked against `ExactChartAdapter`.
- Structural smoke result: Actions run `33088220494` successfully built `1985-01-01 <= t < 1985-01-31` in well under one second of astronomy computation, producing 248 verified structural intervals. It compared the incremental state with the production chart engine every 25 intervals and uploaded a verified v2 cache artifact.
- Verified full century artifact: Actions run `33088719809` built all ten decade segments, merged them, re-verified all hashes/partitions, and uploaded final artifact ID `9653492396`. Canonical horizon is `1926-08-22T00:00:00Z <= t < 2026-08-23T00:00:00Z`; interval count is `288938`; engine fingerprint is `09e811ca0fe517975f9718ea7e12b72f66bf3d2509e049bc29f47169adef5397`; canonical logical-universe SHA-256 is `eb58516030f2176d4c136055829a8168ffe33715a35bfe0b4095c83824c88dfa`; uploaded artifact ZIP SHA-256 is `c1db39b07d36ea88d5be95c809168fc8e8717ee416cd29963262b70f9c977237`.
- Prior-audit comparison: the new `288938` interval count is 20 above the older ~`288918` V4.3 audit, but the two jobs did not use identical horizons or numerical grouping policy. The prior audit started/ended about 5h40m later, covered exactly 100 years rather than the new one-day-longer canonical horizon, used looser root tolerance, and coalesced independent close crossings. Treat the close counts as a useful scale check, not equality proof.
- Global runtime acceptance: `scripts/smoke_century_global_backend.py` uses the real frozen production mapping/question-bank pair and a neutral synthetic UTC birth with zero behavioral answers. Baseline run `33089666690` proved the full path worked but took ~185.3s and revealed an invalid duration-based state tie-breaker. That tie-breaker was removed: interval duration may order equal states deterministically but cannot create scientific evidence rank.
- Optimized global acceptance: run `33091045221` succeeded against the exact immutable century artifact. Candidate count remained `288938`; candidate-universe binding SHA-256 was `aa3ae78339494e43d91a99d2f6a15eefb33f86b9f12d7631ce5a5fcc00f61ef8`; zero behavioral answers correctly left all `288938` candidate states tied with margin `0`; current mapping compressed the universe to only `4807` model-visible scoring signatures. Cold backend init was ~0.007s, freeze including verified cache load+digest ~45.32s, zero-answer discrimination ~6.99s, total ~52.32s. Smoke report artifact ID is `9654400365`.
- Global runtime optimization: century cache verification/loading now parses the immutable artifact once; successful candidate-universe digests and prevalence are cached in-process; symbolic prevalence/scoring/canonical answer work collapses exactly by the current model-visible signature `(type, strategy, authority, profile, defined_centers)`. Regression tests enforce that zero evidence does not create duration-based rank and equivalent model-visible states are not redundantly scored.
- Mapping state: the current frozen production predicate schema scores type, strategy, authority, profile and defined-center structure. The v2 century cache retains channels and activation gates too for structural audit/future-compatible extensions, but these extra fields do not currently enter the participant score. The fact that `288938` intervals collapse to only `4807` current scoring signatures makes richer independently supported/discriminative mapping coverage the principal model-quality bottleneck for truly fine global identification.
- API state: participant-safe create/progress/next-question/evidence/lock/reveal/finalize/final-report routes are implemented. Environment-configured deployment is `hdmatch.api.participant_app:create_participant_app_from_env`; optional `HDMATCH_CENTURY_CACHE` activates verified century recovery.
- Custom GPT assets: participant interviewer instructions, Action OpenAPI schema, and same-origin blind scientific intake page are under `reference/custom_gpt/`.
- CI state: current participant branch is green after structural-cache, tie-semantics, and global-runtime changes: run `33091045069` passed unit/integration tests, production/test Ruff, and strict mypy. CI quality-gates `src/` and `tests/`; one-off legacy research scripts remain outside the application lint gate.
- Current verification milestone: the v2 exact structural century universe and real `century_global` backend path are now operational and acceptance-tested. Do not merge PR `#8` without explicit user instruction.
- Next scientific/engineering priorities: (1) implement authentic versioned IAU constellation membership using Delporte/IAU boundaries rather than a longitude offset; (2) finish the Moon frame/convention differential audit; (3) expand the frozen natal/longitudinal mapping so global search distinguishes substantially more than 4807 model-visible signatures; (4) independently audit civil-time/timezone/location/Earth-rotation handling before angles/houses enter strong confirmatory claims; (5) execute the preregistered progression-vs-development ablation on longitudinal participant evidence. Relationship/future ephemeris extensions are not required for this milestone.
