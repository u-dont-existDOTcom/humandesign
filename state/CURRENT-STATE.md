# Current state

- Task ID: `v4-3-v3-5-migration`.
- Goal: migrate the reproducible blinded Human Design research harness to the
  fail-closed V4.3/V3.6 contract while keeping synthetic engineering validation
  separate from human validation.
- Integration worktree/branch:
  `/tmp/hdmatch-integration` on `codex/harness-integration`.
- Latest upstream `main` commit merged:
  `a7c24012867e640f2728f40ab342267b12d662e9`.
- Current integrated exact-origin implementation head:
  `4dce7708afefdaaff4660f44298880fe8ba6b849`.
- Current published Phase-1/V3.6 checkpoint:
  `b94e160ccbb4ce9be5131e57f37630087825f0b2`.
- Normal exact-head GitHub CI is green for both push run `32564812508` and
  pull-request run `32564814009`.
- The inherited historical V3.6 audit workflow also triggered during the
  upstream-main synchronization. Run `32564813967` failed during ephemeris
  fetch; its 100-year ranking step was skipped. It is not a cache, completed
  audit, or authorized ranking.

## Mandatory execution position

Phase 0 and Phase 1 are complete and published. Independent review, the bounded
real-SWIEPH proof, final stable-tree local validation, and normal exact-head
GitHub CI are green. No production century-cache build and no new full-century
behavioral ranking have started.

The mandatory sequence remains:

1. prove canonical SWIEPH astronomy;
2. implement the complete cacheable M0-M2 feature registry and exact boundary
   serialization;
3. build and verify the reusable 1926-2026 exact-state cache;
4. complete the V4.3/V3.6 mapping, scorer, prevalence, and compliance migration;
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

Upstream `main` now also preserves the frozen V3.6 one-off NetInformation audit
and its observed 2013/1985 development ordering. That historical audit is not
the reusable production mapping/cache implementation, is not untouched human
validation, and must not be used to retune mappings, weights, prevalence, or
feature definitions. It does not authorize another century scan ahead of the
mandatory cache-first sequence.

## Phase 1 result

- Exact Personality/Design boundary-event enumeration uses the exact 88-degree
  Design root and production SWIEPH-only entry points.
- The complete cacheable M0-M2 registry contains 23 mandatory feature families;
  its semantic SHA-256 is
  `6a081572beec6053fb0af94c70ec47c1389b57da65b08a96603e331992eb23e9`.
- Canonical cache admission now requires factory-minted bounded exact batches
  and aggregate exact-universe provenance. Arbitrary physical rows cannot emit
  or open a verified cache.
- Post-mint provenance, Design-tolerance, overlapping-source, continuity, and
  maximality mutations fail closed. Independent re-review found no remaining
  HIGH or MEDIUM issue in this exact-origin gate.
- A bounded real-SWIEPH six-hour proof produced 9 exact intervals / 9 retained
  events and logical-universe SHA-256
  `6d284285408c70ca6ab16e4967016b074fb94ddfa3adc53576d7786dceaad039`,
  then wrote and independently reverified the evidence-bound Zstandard Parquet
  cache fixture.
- Detailed report:
  `reports/v4_3_migration/phase1_feature_registry_and_cache_contract.md`.
- Final stable-tree verification: 456 passed, 2 environment-dependent skips;
  Ruff passed over `src`, `tests`, and `scripts`; strict mypy passed over 103
  `src/hdmatch` source files.

## Next exact action: Phase 2 reusable century cache

Implement the resumable cache path before starting the century build:

1. freeze a deterministic build plan and one-year overlapping job ranges;
2. persist atomic provisional job rows/receipts with all-call SWIEPH audits;
3. production-replay every persisted job before accepting it for assembly;
4. reconcile artificial cuts and recompute merged representatives/Design roots;
5. stream final validation into bounded shards and publish the manifest last;
6. verify the complete cache against an independent tracked trust lock;
7. make ordinary global recovery cache-only.

No century computation or ranking is authorized before the bounded multi-job
replay/reconciliation tests pass. Phase 3 still must bridge V4.3 selectors to
the exact M0-M2 cache vector and enforce mapping-derived 100% feature coverage
before any V4.3-compliant ranking.
