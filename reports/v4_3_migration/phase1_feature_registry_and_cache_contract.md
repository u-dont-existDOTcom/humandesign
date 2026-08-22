# V4.3 migration Phase 1 — feature registry and exact-state cache contract

Status: **PASS — bounded proof only; no century cache or ranking has been run**

This phase prepares deterministic, reusable M0–M2 chart-state serialization.
It is not a behavioral model, a V4.3 score, a verified century cache, a ranking,
or evidence that Human Design predicts human behavior.

Upstream changed the current behavioral target from V3.5 to V3.6 after the
feature-registry work began. This Phase-1 astronomy/cache contract is target
independent; Phase 3 must use V3.6 and preserve the frozen historical V3.6 audit
as development output rather than an optimization target.

## Integrated components

- Exact Personality and Design Gate/Line boundary enumeration uses the exact
  88-degree Design root and inverse Design-to-Personality mapping. Production
  entry points require verified local Swiss Ephemeris files, request SWIEPH,
  inspect every returned mode, and fail on Moshier/JPL/mixed/no-mode fallback.
- The semantic `required-feature-registry-v1` contains 23 cacheable M0–M2
  feature families. Its SHA-256 is
  `6a081572beec6053fb0af94c70ec47c1389b57da65b08a96603e331992eb23e9`.
- Every vector contains all 26 Personality/Design carrier positions and retains
  Gate, Line, Nodes, cardinal Sun/Earth, architecture, Definition topology,
  complete Channels, repeated Gates, hanging/dormant Gates, possible bridges,
  Cross components, and explicit unavailable capability states. Missing data
  are not converted to false.
- Semantic-registry identity and physical Parquet-column identity are distinct
  mandatory hashes. Exact interval metadata, BodyGraph and Mandala hashes,
  chart-feature identity, Design timestamp, and lossless canonical boundary
  events survive Zstandard Parquet round trips.
- High-volume serialization verifies the exact `.se1` bytes at bounded session
  entry and exit, including exception exits, without re-hashing both files for
  every row. Per-coordinate returned-mode enforcement remains active.
- Canonical cache proof validation re-opens and semantically validates the real
  Phase 0 engine receipt, parity report and exact reference bytes, and boundary
  audit. The explicit writer independently re-hashes the pinned local `.se1`
  files before writing. Ordinary verification rechecks bundled evidence,
  manifest/shard bytes, coverage, identities, interval continuity, and maximal
  stable-state semantics across shard boundaries.
- Ordinary blind recovery fails before adapter creation, cache generation, or
  scoring when an on-demand request spans at least 25 calendar years or more
  than 120 distinct month/timezone universes. Broad recovery must use the
  separately verified reusable-cache path.

## Exact-origin gate

Closed by `d694d75fef0cd794547c77c8e9ffeeab021d3399` and hardened by
`4dce7708afefdaaff4660f44298880fe8ba6b849`.

- The supported writer accepts only a private-token `VerifiedExactShardSet`
  assembled from bounded `build_verified_exact_state_batch` results. That
  factory owns production boundary enumeration, retains the representative
  `ChartComputation`, rechecks the stable-feature hash, and serializes the full
  M2 vector inside one bounded file-integrity session.
- Every bounded batch binds the exact partition hash, canonical rows, boundary
  events, engine/mapping identities, and Design tolerances. Every aggregate
  rederives source hashes, ranges, counts, frozen identities, continuity, and
  cross-batch maximality.
- Factory-private in-process mint bindings detect post-mint provenance
  substitution. They are deliberately not persisted and are not presented as
  cross-process proof. Persisted Phase-2 job receipts will require deterministic
  production replay before canonical assembly.
- Arbitrary physical rows can use only the explicitly noncanonical fixture
  writer. It emits no manifest, returns no `VerifiedCenturyCache`, and cannot be
  opened by ordinary recovery.
- Artificial job cuts through a stable state fail closed in Phase 1. The
  resumable Phase-2 assembler must reconcile overlaps and recompute a merged
  interval's representative chart and exact Design timestamp before minting the
  aggregate universe provenance.

An independent adversarial review reproduced a pre-hardening metadata/tolerance
mutation and overlapping-source bypass. The follow-up validator hardening closed
both; re-review reported no remaining HIGH or MEDIUM finding in this Phase-1
scope.

## Bounded real-SWIEPH proof

The production test `test_real_swieph_bounded_exact_cache_writes_and_reverifies`
ran the complete exact-boundary -> M2 serialization -> evidence-bound Zstandard
Parquet -> independent verifier path over
`1985-01-29T10:00:00Z <= t < 1985-01-29T16:00:00Z`.

- requested/returned engine: SWIEPH;
- exact stable intervals: 9;
- retained exact boundary events: 9;
- logical-universe SHA-256:
  `6d284285408c70ca6ab16e4967016b074fb94ddfa3adc53576d7786dceaad039`;
- semantic registry SHA-256:
  `6a081572beec6053fb0af94c70ec47c1389b57da65b08a96603e331992eb23e9`;
- physical Parquet registry SHA-256:
  `b24791ea04702d87df32be5c8821115f6b0f14819f61cd3b83ad30cca721d3ac`;
- ephemeris file-set SHA-256:
  `f5644c27e3682b805ebdde58d593e5a53abfbaca1dc8c52f29f1cd06f2d5c401`.

This is a small engineering proof fixture, not the canonical century cache and
not a behavioral result.

## Deferred mandatory Phase 3 gates

The independent review also confirmed two scorer-side gaps that are not hidden
or reclassified as Phase 1 work:

1. Mapping V2 compilation must derive and hash the mapping-required feature
   registry, and runtime scoring must require 100% coverage before evaluating
   any predicate.
2. V4.3 selectors/scoring must consume the exact M0–M2 cache vector rather than
   the permissive legacy `ChartFeatures` representation.

Both are mandatory before any V4.3-compliant ranking. Current Model-B V2 and
legacy candidate paths must not claim V4.3 compliance.

## Verification

- Exact-origin branch focused suite: 60 passed.
- Independent broader focused suite after integration: 87 passed.
- Bounded real-SWIEPH cache proof: 1 passed.
- Final stable-tree full suite: 456 passed, 2 environment-dependent skips.
- Ruff over `src`, `tests`, and `scripts`: pass.
- Strict mypy over 103 `src/hdmatch` source files: pass.
- Normal GitHub CI for checkpoint `b94e160ccbb4ce9be5131e57f37630087825f0b2`:
  push run `32564812508` pass; pull-request run `32564814009` pass.
- An inherited historical V3.6 audit workflow run failed before computation;
  its 100-year ranking step was skipped and is not counted as a result.
- No production century-cache construction and no new century behavioral
  ranking has started in this cache-first execution.

## Phase-2 handoff — still required before any century ranking

Phase 1 does not claim the reusable cache exists. Phase 2 must add and verify:

- a frozen resumable build plan and independent job artifacts;
- all-call returned-SWIEPH audit receipts;
- deterministic replay of every persisted job before it receives an in-process
  verified capability;
- overlap reconciliation and natural-boundary maximal-state assembly across
  artificial cuts;
- streaming logical validation and bounded final artifact sizes;
- atomic publish with the manifest written last;
- an independent tracked cache trust lock used by ordinary global recovery;
- production parity/boundary evidence generators and a verified-cache-only
  global recovery entry point.

The canonical `1926-08-22T00:00:00Z <= t < 2026-08-23T00:00:00Z` cache build
remains prohibited until those Phase-2 implementation and bounded multi-job
acceptance gates pass.
