# Hale clean-room first-pass V2 verification

Date: 2026-10-03 UTC

- Clean-room V2 freeze manifest: `FREEZE_V2.json`.
- All artifact hashes declared in `FREEZE_V2.json` were recomputed from disk and matched exactly.
- `FREEZE_V2.json` SHA-256 at verification: `331022cedd00f70c3de316f48da044d4b6a986b7a1d9a79fe37947a271bf7f60`.
- Reproduction helpers compile under Python 3.12.
- Re-running `calculate_first_pass.py`, `calculate_domain_votes.py`, `evaluate_full_v14_library.py`, and `build_timing_windows_v2.py` reproduced the frozen outputs.
- Current `CALCULATIONS.json` SHA-256: `8ff727409b9c655a2c919575d4b7a9c52db6afbc6b6105cd7bc28e2506cd559f`.
- Current full 390-rule V1.4 vector SHA-256: `6aabe0e36dec78c9cea351b811a9a261e9f72ef561212160e700cdc56aedcb97`.
- Current timing-window artifact SHA-256: `6cf81fe16b9332b07154936bbab7bdb9477ef13197406087dc1e365f5a40c5f2`.
- `PROJECT_TIMING_2020_2041.json` records 500 exact transit contacts and 71 secondary-progression contacts.
- Its embedded source-script SHA-256 exactly matches the current `scripts/partner_future_pilot.py`: `f8404d036a53faba6434d25d43afd62cebd8946b442b6b5d7b858ef10429d0b4`.
- Focused project tests passed:
  - `tests/unit/test_astrohd_v14.py`
  - `tests/unit/test_astrohd_v13b_native.py`
  - `tests/unit/test_astrohd_v13_traditions.py`
  - `tests/unit/test_progressions.py`
  - Result: **21 passed**.
- `git diff --check` passed.
- The blind cross-family audit used only the prepared calculation/method packet. No Hale outcome/personality/history data were exposed to the reviewer.
- V1 is explicitly marked superseded pre-reveal. V2 is the sole first-pass record eligible for later Hale scoring.
