# V4.3 migration Phase 0 — production astronomy validation

Status: **PASS locally; GitHub CI pending for the report commit**

This is astronomy-engine validation only. It is not a verified century cache,
behavioral ranking, Human Design validation, or evidence about any previously
observed candidate.

## Frozen production inputs

- requested/returned engine: `SWIEPH` / `SWIEPH`
- PySwissEph package/library: `2.10.3.2` / `2.10.03`
- upstream repository: `https://github.com/aloistr/swisseph`
- upstream commit: `3fd0f956d73898b91cc4f67cf18b21af656d1342`
- `sepl_18.se1`: `ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66`
- `semo_18.se1`: `1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7`
- path-free file-set SHA-256:
  `f5644c27e3682b805ebdde58d593e5a53abfbaca1dc8c52f29f1cd06f2d5c401`

The pinned fetch helper verifies exact byte counts and hashes before atomic
installation. Runtime calculations explicitly set the local path, request
`FLG_SWIEPH | FLG_SPEED`, derive the ephemeris mask when the Python binding does
not expose `FLG_EPHMASK`, and require exact returned-mode equality with SWIEPH.
Moshier, JPL, missing-mode, mixed-mode, undeclared-file, and unverified-file
results fail closed.

## Representative production probe

The canonical receipt is `phase0_engine_validation.json`, SHA-256
`32a886fa94d307442f8597233288c74ef9102de02148b8ac7c95cec485fd0f7b`.
It was produced from clean software commit `133bd0e` and records:

- 33 direct calculations: 11 bodies at the inclusive start, midpoint, and one
  second before the exclusive end of the 1926–2026 universe;
- returned flags `258`; `(returned_flags & 7) == 2` (SWIEPH) for every calculation;
- the exact declared `.se1` file and hash used for every calculation;
- deterministic Gate/Line derivation;
- three converged exact 88-degree solar-arc Design roots;
- true-node convention.

## Golden and parity evidence

The official-visible-field reference at `1985-01-29T10:25:00Z` matches the
user-confirmed myBodyGraph/Jovian chart for all 26 Personality/Design
activations, Type, Strategy, Authority, Profile, Definition, defined Centers,
and four Channels. The exact Design root is
`1984-11-03T17:15:51.153195Z`; the tests explicitly prove it is not fixed
88-day subtraction.

The three-date longitude table is deterministic regression evidence generated
with the pinned Swiss inputs. It is not a second independent HD implementation.
Direct multi-gigabyte JPL parity was not run because V4.3 defines verified Swiss
`.se1` as canonical production and direct JPL as optional.

## Verification

- full suite with real Swiss files: `358 passed, 2 skipped`
- skips: Bubblewrap namespace availability and an opt-in retained-fixture E2E;
  neither is an astronomy skip
- Ruff: pass
- strict mypy: pass
- golden/engine focused suite: pass

GitHub Actions provisions the same pinned files, runs `hdmatch validate-engine`,
then runs the complete test/lint/type-check pipeline. Phase 0 should be treated
as closed only after that workflow is green for the exact report commit.
