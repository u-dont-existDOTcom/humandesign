# Hale clean-room first-pass V2 verification

Date: 2026-10-03 UTC

The V2 freeze was completed before any Hale outcome/personality/history reveal.

## Deterministic calculation checks

- `calculate_first_pass.py` compiled successfully under Python 3.12.
- Re-running the final natal/numerology calculation reproduced `CALCULATIONS.json` SHA-256:
  - `8ff727409b9c655a2c919575d4b7a9c52db6afbc6b6105cd7bc28e2506cd559f`
- Re-running the target-blind domain inspection reproduced `ASTRO_DOMAIN_VOTES.json` SHA-256:
  - `988b5896e3bff8cfe3d5399f733d3c6d4e1cad525884dda4e8306f96eb0fdb55`
- A clean outcome-blind evaluation of the full V1.4 registry produced exactly **390 rules** in `ASTRO_V14_FULL_RULE_VECTOR_CLEAN.json` SHA-256:
  - `7f5687ee52ce389dffb420431d3bc547f73ab74558d88af6228049e8213bdf97`
- The current project-native timing generator was rerun independently over 2020-01-01 through 2041-12-31. It again returned exactly **500 transit events** and **71 secondary-progression events**, reproducing:
  - `PROJECT_TIMING_2020_2041.json` SHA-256 `c069a70313831796d2ef537430d2e298a71eb6cac53f2d07f2aaf381e3ecfadb`
- Rebuilding the outcome-blind timing-window summary reproduced:
  - `TIMING_WINDOWS_V2.json` SHA-256 `6cf81fe16b9332b07154936bbab7bdb9477ef13197406087dc1e365f5a40c5f2`

## Project checks

Focused tests:
```
PYTHONPATH=src:scripts /home/joel/humandesign/.venv/bin/python -m pytest   tests/unit/test_astrohd_v14.py   tests/unit/test_astrohd_v13b_native.py   tests/unit/test_astrohd_v13_traditions.py   tests/unit/test_progressions.py -q
```

Result: **21 passed in 0.68s**.

JSON parsing passed for:
- `PROTOCOL.json`
- `CALCULATIONS.json`
- `ASTRO_DOMAIN_VOTES.json`
- `PROJECT_TIMING_2020_2041.json`
- `TIMING_WINDOWS_V2.json`
- `FREEZE_V2.json`

All task scripts used for the V2 calculation/timing path passed `py_compile`.

## Review checks

- Blind cross-family first-pass review completed with Claude Opus using only the outcome-blind calculation packet.
- A single reconciliation round separated real method fixes from reviewer suggestions inconsistent with the frozen project conventions.
- Adopted fixes are recorded in `CROSS_FAMILY_RECONCILIATION.md`.
- No Vimshottari dasha, alternative ayanamsha, Lot of Fortune, Hale biography, prior survey, Memory or known life event was added to V2.

## Frozen identities before publication

- First-pass report: `740208a21bceea4d8d82ce1024e4fae229e06dc0ba5bb73f409a4f8544ef5289`
- V2 freeze manifest: `d5bef45f9e2687b7e52a66e553d639eb79995e8291346b9543000248c019879f`
- Calculation: `8ff727409b9c655a2c919575d4b7a9c52db6afbc6b6105cd7bc28e2506cd559f`
- Project-native timing: `c069a70313831796d2ef537430d2e298a71eb6cac53f2d07f2aaf381e3ecfadb`

The earlier V1 same-day freeze at commit `165506e8bb4de7ac52504683cbe2382b38334813` is retained only as superseded pre-reveal provenance and must not be scored.
