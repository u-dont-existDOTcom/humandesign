# 16 — Ephemeris Bootstrap and Fail-Closed Production Policy

## Problem

PySwissEph can return plausible-looking values even when the requested Swiss/JPL data files are absent, because the library may fall back to Moshier. That is unacceptable for an authoritative V4.3 century cache.

The project must not rely on whatever files happen to be installed in the runtime.

## Production default

For the 1926-2026 project universe, use the compressed Swiss Ephemeris data files as the normal production engine:

```text
sepl_18.se1   planetary data, 1800-2399
semo_18.se1   lunar data, 1800-2399
```

The official current Swiss files are based on JPL DE441. Direct JPL files are optional for parity checking; they are not required for the normal production cache.

The repository does not need to vendor the binary ephemeris files. Fetch them from the pinned official upstream commit using:

```bash
python scripts/fetch_swisseph_ephemeris.py
```

The helper writes the files under `data/ephemeris/` and records local SHA-256 hashes plus the immutable upstream source commit.

The repository-controlled trust root is `data/ephemeris/manifest.json`. The fetch
helper validates that manifest against the pinned upstream repository, immutable
commit, and exact required file set. It then verifies the byte length and SHA-256
of each download *before* atomically installing it. It never treats a newly
observed download hash as authoritative.

For an offline/local verification with no network access:

```bash
python scripts/fetch_swisseph_ephemeris.py --verify-only
```

A successful fetch or verification writes the ignored, deterministic local receipt
`data/ephemeris/swisseph_ephemeris_manifest.json`. The receipt binds the exact
source-manifest hash, upstream repository/commit, per-file hashes, and a combined
file-set hash. Runtime and cache creation must still re-hash the actual `.se1`
files; the presence of a prior receipt alone is not proof that local bytes remain
unchanged.

## Required runtime setup

PySwissEph must be initialized explicitly:

```python
import swisseph as swe

swe.set_ephe_path("data/ephemeris")
flags = swe.FLG_SWIEPH | swe.FLG_SPEED
xx, retflags = swe.calc_ut(jd_ut, body, flags)
```

Never infer success merely because `calc_ut()` returned coordinates.

Swiss Ephemeris can change the requested ephemeris internally when data are unavailable. Therefore inspect the returned ephemeris bits:

```python
used_ephemeris = retflags & swe.FLG_EPHMASK
if used_ephemeris != swe.FLG_SWIEPH:
    raise EphemerisFallbackError(
        f"requested SWIEPH but calculation returned flags={retflags}"
    )
```

Implement this check in the engine wrapper, not only in a CLI probe.

## Validation probe

Before cache generation, test representative timestamps near the beginning, middle, and end of the universe for every scored astronomical body that uses the planetary/lunar ephemeris.

At minimum verify:

- requested mode: SWIEPH;
- returned mode: SWIEPH;
- file path exists;
- local file SHA-256 matches the run manifest;
- Gate/Line derivation is deterministic;
- exact 88-degree Design root converges;
- golden/reference chart tests pass.

Node calculations must use the frozen true/mean convention and be validated independently even if their internal computation does not require the same `.se1` file path.

## Cache rule

No `data/century_cache/*` artifact is canonical unless its manifest records:

```text
ephemeris_requested = SWIEPH
ephemeris_returned = SWIEPH
source_repository = aloistr/swisseph
source_commit = <immutable commit>
sepl_18_sha256 = ...
semo_18_sha256 = ...
engine_version = ...
parity_status = pass
boundary_audit_status = pass
```

If a fallback is detected during any cache-building calculation, abort the build and discard the partial cache.

## Why direct JPL is optional

Using `FLG_JPLEPH` with a multi-gigabyte direct JPL file is valid, but operationally unnecessary for this project when verified Swiss `.se1` files are available. The compressed Swiss data are designed to reproduce the underlying JPL ephemeris at very high precision while being much smaller.

A direct JPL run is valuable as an independent parity sample, not as a dependency that blocks ordinary production work.

## Moshier policy

Moshier remains useful only for:

- explicit legacy reproduction;
- non-authoritative exploratory debugging;
- tests that verify fallback detection.

A Moshier-derived result must carry:

```text
v4_3_compliant = false
cache_verified = false  # for a production cache claim
calculation_status = exploratory_or_legacy
```

It must never silently replace SWIEPH in a canonical global ranking.
