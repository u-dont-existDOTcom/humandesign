# AstroHD scoring-structure audit execution receipt

Receipt date: 2026-09-02

Task mode: execution only

Branch: `codex/astrohd-owner-intake-quality-v1`

Starting HEAD: `530ccde5c41239dd8fd3317a4c8983547a51e221`

Ending implementation HEAD: `981c4cd4c009e45ba63398e3fb6a727438518a45`

## Files added

- `scripts/extract_astrohd_frozen_scoring_structure.py`
- `reference/audits/astrohd_frozen_scoring_structure_v1.json`
- `reference/audits/astrohd_question_mapping_status_v1.json`
- `tests/unit/test_astrohd_frozen_scoring_structure.py`
- `state/ASTROHD-SCORING-STRUCTURE-AUDIT-EXECUTION-RECEIPT-2026-09-02.md`

No pre-existing file was changed by this execution slice.

## Exact sources

- Mapping library: `mappings/mapping_library_v1.json`
  - SHA-256: `3424672432f7f071ec90ef9ddce52a67ff6794911e92b1a1e04f079262ea6200`
- Question bank: `reference/core/question_bank_v1.json`
  - SHA-256: `31f813efc3da7263569ef010a8336b1b1b0c44801b7aa0f91e33b3fa4587d820`
- Prior mechanical mapping audit:
  `reference/audits/astrohd_frozen_rule_prompt_mapping_v1.json`

The extractor reads those three source artifacts and does not modify them.

## Mechanically observed inventory

- Distinct stored `status == "frozen"` mapping rules: `27`
- Distinct question IDs referenced by frozen mappings: `23`
- Prior mechanical rule-ID set match: `PASS`
- Prior mechanical prompt-ID set match: `PASS`
- Structural classes among frozen mappings: `4`
- Dependency-cluster groups among frozen mappings: `7`
- Observation groups among frozen mappings: `20`
- Question-bank questions inventoried exactly once: `81`
- Question count by phase:
  - `open_autobiography`: `10`
  - `readiness`: `8`
  - `structured`: `58`
  - `validation`: `5`
- Questions with at least one stored frozen mapping: `23`
- Questions with at least one stored empirical-only mapping: `6`
- Questions with at least one stored unresolved mapping: `52`

The question-status aggregate is marked
`descriptive_only_not_a_completeness_denominator`. Neither `23`, `81`, nor any
other observed count was treated as a target or questionnaire-completeness
denominator.

## Verification executed

1. New focused audit tests:

   ```text
   .venv/bin/pytest -q tests/unit/test_astrohd_frozen_scoring_structure.py
   ```

   Result: `6 passed`.

2. Existing frozen-mapping audit tests:

   ```text
   .venv/bin/pytest -q tests/unit/test_astrohd_frozen_mapping_extract.py
   ```

   Result: `3 passed`.

3. Existing theory-language exposure tests:

   ```text
   .venv/bin/pytest -q tests/unit/test_theory_language_exposure.py
   ```

   Result: `9 passed`.

4. Generated JSON validation:

   ```text
   .venv/bin/python -m json.tool reference/audits/astrohd_frozen_scoring_structure_v1.json
   .venv/bin/python -m json.tool reference/audits/astrohd_question_mapping_status_v1.json
   ```

   Result: `PASS` for both files.

5. Full repository unit suite:

   ```text
   .venv/bin/pytest -q
   ```

   Result: `308 passed, 1 skipped`. The existing environment-dependent skip is
   for unavailable official Swiss Ephemeris files.

6. Strict typing:

   ```text
   .venv/bin/mypy src/hdmatch scripts/extract_astrohd_frozen_scoring_structure.py
   ```

   Result: `Success: no issues found in 121 source files`.

7. Ruff:

   ```text
   .venv/bin/ruff check scripts/extract_astrohd_frozen_scoring_structure.py tests/unit/test_astrohd_frozen_scoring_structure.py
   .venv/bin/ruff format --check scripts/extract_astrohd_frozen_scoring_structure.py tests/unit/test_astrohd_frozen_scoring_structure.py
   ```

   Result: `PASS`; both files formatted.

8. Whitespace/error check:

   ```text
   git diff --check
   ```

   Result: `PASS`.

The tests also establish byte-identical regeneration of both committed JSON
audits, exact reconstruction of dependency-cluster and observation groups, exact
question/mapping-reference joins, mechanical status booleans, deterministic
ordering, current-source hashes, and absence of the prohibited interpretive
fields from both outputs.

## Scope confirmations

- No source mapping, mapping status, mapping token, scoring weight, or question
  bank record changed.
- No participant, scoring, questionnaire, eligibility, stopping, progress,
  lock/reveal, primary-analysis, theory-language exposure codebook, or deployment
  behavior changed.
- No question was added, deleted, reworded, ranked, or recommended.
- No construct-coverage, adequacy, reliability, discriminative-value,
  respondent-burden, theory-leakage, or new-question judgment was made.
- No completeness denominator or target questionnaire count was inferred.
- No real participant data or real theory-language vocabulary was added.
- No merge, rebase, reset, deployment, invitation rotation, participant session,
  participant contact, or spending occurred.

Return this receipt and the two generated audit paths to the verified supervising
Extra-High/Pro reasoning chat for interpretation.
