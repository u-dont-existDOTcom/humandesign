# Codex Task: Migrate HD Matcher from V4.1/V3.2 to Hardened V4.3/V3.5

Work in the existing `u-dont-existDOTcom/humandesign` repository.

## Source of truth

Before changing code, read in this order:

1. `AGENTS.md`
2. `ARCHITECTURE.md`
3. `reference/core/v4_3_scoring_algorithm.md`
4. `reference/core/behavioral_target_combined_v3_5.md`
5. `docs/02_scoring_and_model_policy.md`
6. `docs/13_v4_3_migration_and_century_cache.md`
7. `docs/16_ephemeris_bootstrap.md`
8. `docs/14_month_first_blind_validation.md`
9. the remaining numbered docs

Do not continue using `human_design_reverse_matching_protocol_v4_1.md`, V3.2 scoring, or `mapping_library_v1.json` as the current canonical model. Preserve them as historical regression fixtures only.

## Mandatory execution order

This order is part of the task, not a suggestion.

### Phase 0 — provision and prove the astronomy engine

Before any new century scan:

1. run `python scripts/fetch_swisseph_ephemeris.py` if the production `.se1` files are missing;
2. point PySwissEph explicitly at `data/ephemeris`;
3. request `FLG_SWIEPH` for production calculations;
4. inspect the returned ephemeris flag from every representative calculation;
5. abort if the returned mode is Moshier or otherwise differs from the requested production mode;
6. record local ephemeris SHA-256 hashes and the upstream source commit in the run/cache manifest;
7. pass engine parity/golden tests.

Direct multi-gigabyte JPL files are NOT required for the normal production path. Verified compressed Swiss Ephemeris `.se1` files are the normal production engine. Direct JPL may be used as an additional parity check.

### Phase 1 — implement the full cacheable candidate feature registry

Implement the complete M0-M2 chart serialization and exact boundary engine needed by V4.3. Do not run another 100-year behavioral search yet.

### Phase 2 — build and verify the reusable century cache

Build the canonical exact-state cache once, verify its manifest, boundary audit, engine flags, and feature coverage, and make global recovery read it by default.

**Do not run another full 100-year ranking before this cache path exists and passes verification.**

### Phase 3 — complete V4.3 scorer/mapping migration

Implement mapping-library-v2, flexibility penalties, conditional prevalence, dependency/corroboration controls, and the exact rank tuple. This work may proceed in parallel with Phase 1/2, but the final full-universe ranking must use the verified cache.

### Phase 4 — rerun the full universe from the cache

Only after Phases 0-3 pass compliance tests, run the new full-universe V4.3/V3.5 ranking from cached exact states. Do not regenerate the solar-system state matrix during ordinary reruns.

## Why this migration is required

The current implementation is a simplified subset of the intended protocol. In particular, the current symbolic predicate schema is largely limited to Type/Strategy/Authority/Profile/defined Centers, and the current evidence formula omits the V4.2/V4.3 interpretive-flexibility factor. V4.3 must fail closed rather than silently dropping deeper mappings.

## Required implementation changes

### A. Versioned mapping schema V2

Create `mapping-library-v2` / `V4.3/V3.5-symbolic-v2`.

Each frozen mapping must include:

- structural anchor capable of addressing Type, Strategy, Authority, Centers, Profile, Definition, Channel, Gate, Line, side (Personality/Design), planetary carrier, Nodes, cardinal activations, circuitry, and enabled advanced substructure;
- structural salience;
- mapping directness;
- `flexibility_class` and exact frozen factor;
- dependency cluster;
- optional independent corroborator with a 15% cap;
- contradiction rule;
- prevalence parent hierarchy;
- source/rationale;
- status.

Compile a `required_feature_registry` and hash it.

### B. Full candidate feature registry

Extend candidate/chart serialization so every exact state exposes the complete M0-M2 registry. Do not infer missing fields as absent.

At runtime, scoring must abort if `required_feature_coverage != 1.0`.

### C. Exact V4.3 scoring

Implement exactly `reference/core/v4_3_scoring_algorithm.md`:

```text
Ceff = behavioral_confidence * measurement_reliability
raw_bits = -log2(duration_weighted_prevalence)
info_bits = min(6, raw_bits)

E_primary = Ceff * primary_support * flexibility_factor * info_bits
E_corr = 0.15 * Ceff * corr_support * corr_flexibility * corr_info_bits

contradiction = Ceff * contradiction_severity * 4
NetInformation = sum(E) - sum(contradiction)
```

Retain CoreFit and DetailedSupport as separate metrics.

Primary candidate rank MUST be:

1. NetInformation descending
2. meaningful contradictions ascending
3. DetailedSupport descending
4. CoreFit descending
5. exact stable duration descending

Never rank by `CoreFit + NetInformation`, `100 + rubric_bits`, or an ad hoc coherence score.

### D. Conditional prevalence

Implement duration-weighted prevalence from the global universe and the frozen parent/backoff hierarchy. Candidate-file frequencies are forbidden as prevalence estimates.

### E. Precomputed 100-year state store

Build the exact-state universe once and reuse it.

Initial canonical range:

```text
1926-08-22T00:00:00Z <= t < 2026-08-23T00:00:00Z
```

Use Zstandard-compressed Parquet and shard by decade or another size that keeps every Git object comfortably below GitHub's normal file limit.

Add:

```text
data/century_cache/v1/manifest.json
data/century_cache/v1/*.parquet.zst
data/century_cache/v1/prevalence-v4_3.json.zst
```

Manifest must record range, schema, engine, local ephemeris hashes, flags requested, flags actually returned, Node convention, Mandala version, Design-root tolerance, shard hashes/row counts, logical universe hash, parity status, and boundary-audit status.

Important: do not publish an authoritative cache generated through silent Moshier fallback. Production cache generation must use verified Swiss `.se1` files and fail closed if the returned calculation flags indicate Moshier. Direct JPL is optional, not a prerequisite for production.

Normal global searches must default to this cache. Add an explicit rebuild command rather than regenerating the century automatically.

Suggested CLI:

```bash
python scripts/fetch_swisseph_ephemeris.py
hdmatch validate-engine --ephemeris-mode swiss --ephemeris-path data/ephemeris
hdmatch build-century-cache --start 1926-08-22T00:00:00Z --end-exclusive 2026-08-23T00:00:00Z --output data/century_cache/v1
hdmatch verify-century-cache data/century_cache/v1
hdmatch recover-global --cache data/century_cache/v1 --target ...
```

### F. V3.5 behavioral target

Compile the latest target without forcing the two `depends/unknown` discriminator answers into either side.

Key new distinctions:

- strong selective care capacity is not the same as generalized nourishment as an independent driver;
- care action depends strongly on salience, accepted responsibility, relationship, and feeling uniquely suited/needed;
- important existential/structural questions can recur; ordinary questions need not;
- childhood had stronger difficulty releasing consequential puzzles/errors; adult tolerance for unresolved mystery increased;
- chess/programming/straight-A achievement shows deliberate skill improvement, but reported motive is learning/intrinsic excellence rather than status, rank, credential identity, or generalized expert identity.

Mark these latest refinements post-selection and not independent confirmation.

### G. Hardening against simplification

Add tests that intentionally construct reduced candidate vectors and reduced mapping libraries. A V4.3 run must fail rather than silently proceed if frozen mappings cannot be evaluated.

Add a compliance object to every report:

```json
{
  "protocol_version": "V4.3",
  "calculation_tier": "M2",
  "scoring_tier": "M2",
  "required_feature_coverage": 1.0,
  "simplified": false,
  "cache_verified": true,
  "ephemeris_requested": "SWIEPH",
  "ephemeris_returned": "SWIEPH",
  "flexibility_penalty_enabled": true,
  "conditional_prevalence_enabled": true,
  "v4_3_compliant": true
}
```

If any value is false/incomplete, the report must label itself `partial/non-compliant` and may not be called the canonical V4.3 result.

## Acceptance tests

At minimum add tests proving failure if:

1. flexibility factor is omitted;
2. any frozen mapping-required feature is missing;
3. M0-only chart data claims V4.3;
4. Channel + component Gates double-count;
5. alternative pathways sum;
6. corroboration exceeds 15%;
7. candidate pool is used for prevalence;
8. conditional prevalence/backoff is bypassed;
9. CoreFit is added to NetInformation;
10. unknown/depends is coerced into a scored answer;
11. only finalists are rescored after a revision;
12. fixed-day Design subtraction is used;
13. an interior boundary is missed;
14. ephemeris fallback is silent or returned flags differ from requested SWIEPH;
15. century-cache manifest/hash mismatch is accepted;
16. `required_feature_coverage < 1.0` can still emit a V4.3-compliant report;
17. an ordinary global rerun regenerates the century instead of using the verified cache;
18. a full 100-year ranking begins before the production cache is verified.

Run the existing unit/integration/blind suites and new migration tests. Preserve old V4.1/V3.2 fixtures so regression behavior can still be reproduced explicitly under a legacy model flag.

## Deliverables

- mapping schema/library V2;
- full candidate feature registry;
- corrected scorer + exact rank tuple;
- conditional prevalence implementation;
- Swiss ephemeris fetch/probe/fail-closed path;
- century-cache build/verify/read path;
- V3.5 target compiler support;
- hardening/compliance tests;
- updated docs/manifests;
- migration report showing exactly which old V4.1/V3.2 behaviors changed;
- one full-universe V4.3 rerun only after the production state cache passes engine parity and boundary audits.

Do not optimize the model to preserve any previously observed finalist. The new full-universe rerun is allowed to change the ranking.
