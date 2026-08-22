# Current state

- Task ID: `v4-3-v3-5-migration`.
- Goal: migrate the reproducible blinded Human Design research harness to the
  fail-closed V4.3/V3.5 contract while keeping synthetic engineering validation
  separate from human validation.
- Integration worktree/branch:
  `/tmp/hdmatch-integration` on `codex/harness-integration`.
- Latest upstream `main` commit merged:
  `c3c0b51ea40346534dc40361ce5f49d651a80cc3`.
- Current published checkpoint:
  `2b5c1f80d1ee20f96a5470660e84327f0c767544`.
- Exact-head GitHub Actions are green for both push run `32560209894` and
  pull-request run `32560212364`.

## Mandatory execution position

Phase 0 is complete. Phase 1 is in progress. No production century-cache build
and no full-century behavioral ranking have started.

The mandatory sequence remains:

1. prove canonical SWIEPH astronomy;
2. implement the complete cacheable M0-M2 feature registry and exact boundary
   serialization;
3. build and verify the reusable 1926-2026 exact-state cache;
4. complete the V4.3/V3.5 mapping, scorer, prevalence, and compliance migration;
5. run one full-universe ranking from the verified cache only.

The temporary `SWIEPH profile A-B rerun` workflow and its direct century runner
were removed from the integration tree in `f895f6d` because they bypassed the
mandatory reusable-cache gate. They remain recoverable from Git history. The
GitHub workflow is disabled. It was never accepted as a canonical cache or
ranking.

## Phase 0 evidence

- Canonical engine: verified Swiss Ephemeris `.se1`, requested and returned
  mode `SWIEPH`; Moshier/JPL/mixed/no-mode fallback fails closed.
- Upstream Swiss repository commit:
  `3fd0f956d73898b91cc4f67cf18b21af656d1342`.
- `sepl_18.se1` SHA-256:
  `ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66`.
- `semo_18.se1` SHA-256:
  `1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7`.
- Path-free file-set SHA-256:
  `f5644c27e3682b805ebdde58d593e5a53abfbaca1dc8c52f29f1cd06f2d5c401`.
- Canonical Phase 0 receipt SHA-256:
  `32a886fa94d307442f8597233288c74ef9102de02148b8ac7c95cec485fd0f7b`.
- Production probe: 33 direct body calculations across the declared century
  horizon plus three exact Design roots; every returned mode is SWIEPH.
- Verified Joel baseline at `1985-01-29T10:25:00Z`: 26 activations and visible
  BodyGraph fields match the user-confirmed chart; exact Design timestamp is
  `1984-11-03T17:15:51.153195Z`.
- Local full suite: `358 passed, 2 skipped`; Ruff and strict mypy pass.
- Detailed report:
  `reports/v4_3_migration/phase0_engine_validation.md`.

Direct JPL was not run because it is optional. The canonical production engine
is the verified Swiss `.se1` path.

## Preserved earlier work

The blind-boundary hardening, frozen Model A, prospective
`MODEL-B-DETAILED-V2-NEW`, retained public month caches, and interrupted paired
experiment artifacts remain preserved. The paired 75-case benchmark was stopped
before Model B prediction/freeze/reveal when the V4.3 migration superseded it.
It is not a completed benchmark and must not resume ahead of the mandatory
cache-first sequence.

The earlier Model A 75-case baseline remains the only completed core-only
baseline: Top-1 `0.453333`, Top-3 `0.746667`, Top-5 `0.826667`, MRR
`0.625680`. Do not rerun an expensive Model A-only benchmark.

## Current Phase 1 workstreams

- exact Personality/Design boundary-event enumeration and completeness audit;
- complete M0-M2 feature registry and deterministic chart-state serialization;
- typed century-cache manifest/shard/verification contracts exercised only on
  small fixtures.

These workstreams may merge only after focused tests and integration review.
They are not authorized to generate the century cache or rank candidates.
