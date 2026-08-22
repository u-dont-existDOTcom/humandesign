# CODEX MASTER PROMPT

Build the full research harness described by this repository.

Start by reading `AGENTS.md` and `ARCHITECTURE.md`, then `reference/core/v4_3_scoring_algorithm.md`, `reference/core/behavioral_target_combined_v3_5.md`, `docs/16_ephemeris_bootstrap.md`, and the numbered docs in `docs/`.

The current codebase was originally implemented against V4.1/V3.2. That implementation is now a migration source, NOT the normative model. Do not preserve a simplification merely because existing tests encode it.

## Mandatory execution order

Do not run another 100-year behavioral ranking until the following sequence is complete:

1. provision and verify the production Swiss Ephemeris `.se1` files with `scripts/fetch_swisseph_ephemeris.py`;
2. make the engine request SWIEPH explicitly and hard-fail if returned ephemeris flags indicate Moshier or another fallback;
3. implement the complete cacheable M0-M2 candidate feature registry and exact boundary engine;
4. build and verify the reusable 1926-2026 century cache once;
5. complete the V4.3 mapping/scoring migration and compliance tests;
6. rerun the full universe FROM THE VERIFIED CACHE rather than recalculating astronomy.

Direct multi-gigabyte JPL files are optional parity inputs. Verified Swiss `.se1` files are the normal production path.

## Objective

Deliver a reproducible Python project and CLI that can:

1. calculate exact HD chart-state intervals with historical timezone handling and exact Design moment;
2. compile the full V4.3 symbolic behavioral model into machine-readable rules;
3. calculate the required M0-M2 feature registry, including Gate/Line/Channel/planetary-carrier distinctions referenced by frozen mappings;
4. apply flexibility penalties, dependency control, corroboration caps, and duration-weighted conditional prevalence exactly as specified;
5. generate blinded synthetic questionnaire cases from that same frozen model;
6. recover hidden birth day/time from known month/year and broader candidate universes;
7. restore/ablate independent response clusters and run adaptive information-gain questioning;
8. cryptographically freeze predictions before answer-key reveal;
9. evaluate synthetic recovery;
10. import known human development cases;
11. fit empirical chart→response models post hoc on development humans;
12. compare symbolic, empirical, and hybrid decoders;
13. perform person-level validation and preserve an untouched final test pathway;
14. build, verify, and reuse a versioned precomputed 100-year exact-state cache;
15. produce transparent reports including failures/ties/unresolved intervals and `v4_3_compliant` status.

## Immediate migration task

Before new feature work, migrate the existing symbolic implementation from V4.1/V3.2 to V4.3/V3.5.

Required minimum changes:

- extend the mapping schema with `flexibility_class` and `flexibility_factor`;
- add predicates for complete Channels, Gate+Line, planetary carrier, cardinal activation, Definition, and predeclared conjunctions;
- compile and enforce a `required_feature_registry`;
- treat a missing required feature as a hard error, never as a non-match;
- implement the V4.3 evidence formula including flexibility;
- implement conditional duration-weighted prevalence with deterministic backoff;
- keep CoreFit, DetailedSupport, and NetInformation separate;
- rank exactly by the V4.3 lexicographic rule;
- forbid `CoreFit + NetInformation` or any comparable convenience scalar;
- rerun the complete universe after accepted target revisions;
- preserve revision provenance and distinguish frozen-independent from best-current-descriptive outputs;
- add the anti-simplification mutation tests in `docs/13_v4_3_migration_and_century_cache.md`.

Do not claim migration complete until those tests pass.

## Precomputed century database

Implement a reusable exact-state store covering initially:

```text
1926-08-22T00:00:00Z <= t < 2026-08-23T00:00:00Z
```

Use verified Zstandard-compressed Parquet shards plus a cryptographic manifest. Cache duration-weighted prevalence tables keyed by universe hash and prevalence-policy version.

Normal broad searches must load the verified cache rather than regenerate 100 years of astronomy every run. Rebuild only on explicit cache build/extension or when engine/feature-policy provenance is incompatible.

The cache manifest must record requested and actually returned ephemeris mode for representative and build-time calculations. A cache is non-canonical if Moshier fallback occurs anywhere.

If the resulting binary dataset is impractical for ordinary Git history, use Git LFS or versioned GitHub Release assets for the shards, while keeping the manifest, schema, build code, and verification code in the repository.

## Use parallel agents/worktrees

Delegate separable work to parallel agents:
- exact chart engine + ephemeris validation + century cache,
- V4.3 mapping/schema compiler,
- V4.3 symbolic scorer + conditional prevalence,
- synthetic harness,
- search/adaptive questioning,
- human empirical modeling,
- evaluation/audit + anti-simplification mutation tests,
- API integration.

Keep interfaces explicit and merge only after tests.

## Critical scientific constraints

- Post-hoc fitting on development humans is ALLOWED.
- Do not present development-set performance as predictive validation.
- Never let decoder/evaluator see answer keys before prediction freeze.
- Do not silently invent missing HD mappings.
- Do not silently simplify V4.3 because some detailed mappings are harder to implement.
- A reduced implementation must identify itself as reduced and set `v4_3_compliant: false`.
- Never accept a plausible coordinate result as proof that SWIEPH was used; inspect returned flags.
- Do not use coarse time grids as proof of minute precision.
- Report stable intervals.
- Split human data by person.
- Include chance/permutation and calendar/season baselines.
- Preserve all failures.
- Rubric bits are not probabilities.
- Unknown/context-dependent answers may remain unscored.
- Human Design is treated as an experimental symbolic hypothesis.

## First post-migration deliverable

Keep the known-month synthetic oracle benchmark, but run it only after V4.3 compliance passes:

- generator uses the same frozen V4.3 model as decoder;
- 1,000 blinded cases;
- exact candidate intervals for all days in each month;
- blind decoder;
- prediction freeze;
- answer-key reveal;
- top-1/top-3/top-5/MRR report;
- ablation/restoration curves;
- leakage audit;
- anti-simplification compliance report.

Then add noise tiers, known-date time rectification, and cached broad-universe recovery.

## Definition of done for this migration

The repository has:
- installable package;
- documented environment;
- V4.3 schema/scorer implementation;
- production SWIEPH bootstrap/probe with no silent fallback;
- exact run manifests/hashes;
- verified century-cache build/verify/load path;
- tests that fail under deliberate scoring simplifications;
- one command to generate a blind experiment;
- one command to recover it without key access;
- one command to freeze;
- one command to reveal/evaluate;
- a report explaining every oracle failure;
- no code path that labels an architecture-only or V4.1 scorer as V4.3.

When a requirement is underspecified, mark it unresolved rather than choosing whatever improves recovery.
