# Phase 2 reusable century-cache implementation

Status: bounded multi-job proof passed; canonical 1926–2026 build not yet
started; no behavioral ranking started.

## Implemented contract

The Phase 2 path is now explicit and cache-only at the recovery boundary:

1. `prepare-century-cache` verifies the pinned local Swiss files and golden
   parity, requires a clean committed source tree, and writes the immutable
   calendar-year/overlap plan last.
2. `build-century-cache-job` creates one provisional Zstandard Parquet artifact
   and writes its passing receipt last. Every calculation is audited and must
   request and return SWIEPH.
3. A persisted job is only a resumability claim. Assembly re-hashes, decodes,
   and deterministically production-replays every job before minting an
   in-memory verified capability.
4. `assemble-century-cache` reconciles overlapping year cuts, recomputes any
   merged representative and exact Design root, streams bounded output shards,
   bundles evidence, publishes `manifest.json` last, writes an independent
   trust lock, and reopens the cache against that lock.
5. `verify-century-cache` independently verifies the complete published cache.
   Ordinary cache recovery has no engine or rebuild callback.

The immutable plan binds the exact clean source commit, Phase 0 receipt, parity
report/reference, Swiss engine/file provenance, M0–M2 registries, Mandala and
BodyGraph identities, boundary policy, Design-root tolerances, overlap policy,
and ordered jobs. The reconciliation aggregate and final trust lock retain that
plan hash.

## Bounded real-SWIEPH proof

The proof deliberately crossed a UTC year boundary:

```text
1999-12-31T18:00:00Z <= t < 2000-01-01T06:00:00Z
```

It produced two calendar-year core jobs with a frozen 90,001-second overlap.
Because this proof horizon is shorter than the overlap, both jobs correctly
scanned the full bounded horizon; their byte-identical provisional artifacts
are therefore expected. Their core ownership differs and was reconciled into a
single 20-interval universe.

Results:

- build-plan SHA-256:
  `bbc681c6f1951f0024ff18cdef771264f0bf26d42073de825e9ed370ab445e01`;
- clean source commit:
  `f0f345371fab1188951e271f2f5fdc2699912e1f`;
- each producer and deterministic replay made 2,889 audited calculations with
  requested/returned flags `258` (`FLG_SWIEPH | FLG_SPEED`);
- reconciliation made 179 audited calculations, all returned SWIEPH;
- 20 exact intervals and 19 retained boundary events;
- zero missing boundaries, gaps, overlaps, or maximality violations;
- required M0–M2 feature coverage `1.0`;
- logical-universe SHA-256:
  `5dd48a851da45e81bca430bd7b35333d73d3894912644cd156c43feca3636db0`;
- manifest SHA-256:
  `14d40a3f58022685e539ece6583ac4483147fcdd331f7465a7e5a6ce061d20bd`;
- trust-lock SHA-256:
  `a3cf30cf393fe3f2e6dbb85547b5792538fb0b8cb24b1ba3f3914297879abb6b`.

The independently reopened cache rows were also compared byte-for-logical-byte
with a direct exact-state build of the same 12-hour horizon. All 20 typed rows
were equal and both canonical row hashes were the logical-universe hash above.
The machine-readable proof is
`reports/v4_3_migration/phase2_bounded_multijob_proof.json`.

## Preserved failed attempt

The first assembly attempt at source commit
`51111602141254d91d883fc4e5510a1315b7a217` failed closed with
`Swiss calculation audit captures cannot be nested`. It published neither a
manifest nor a trust lock. The cause was orchestration using one provider
instance for a staged replay audit nested inside the reconciliation audit.
Commit `f0f345371fab1188951e271f2f5fdc2699912e1f` separates those into two
independently configured and provenance-checked Swiss provider instances and
adds a regression test. The failed attempt is not presented as a completed
proof and its staged files are not eligible for reuse after the source change.

## Remaining mandatory gate

The canonical range remains exactly:

```text
1926-08-22T00:00:00Z <= t < 2026-08-23T00:00:00Z
```

It may now be planned from a clean, tested, CI-green commit and built as 101
resumable jobs. Phase 3 scorer/mapping work remains pending, and Phase 4 ranking
remains forbidden until both the canonical cache and Phase 3 compliance gates
pass. Direct JPL remains optional; verified Swiss `.se1` is the canonical
production engine and Moshier fallback is never accepted.
