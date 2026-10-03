# Hale clean-room first-pass verification

Date: 2026-10-03 UTC

- Reproduction script compiled successfully with Python 3.12.
- PROTOCOL.json, CALCULATIONS.json, and FREEZE.json passed JSON parsing.
- Re-running calculate_first_pass.py reproduced CALCULATIONS.json SHA-256 exactly:
  - 80d81cf6ccef3d7daca5d521b205f6060208055f5fc2d028b2b6e02c06c4faa6
- Focused project tests passed with the repository import path:
  - tests/unit/test_astrohd_v14.py
  - tests/unit/test_astrohd_v13b_native.py
  - tests/unit/test_astrohd_v13_traditions.py
  - tests/unit/test_progressions.py
  - Result: 21 passed.
- git diff --check passed.
- The first pytest invocation omitted PYTHONPATH=src:scripts and failed during import collection; rerunning with the repository's correct import path passed all 21 tests. This was an invocation/environment error, not a code-test failure.
