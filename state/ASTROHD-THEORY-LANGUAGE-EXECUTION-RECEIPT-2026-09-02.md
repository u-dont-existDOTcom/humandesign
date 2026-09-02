# AstroHD theory-language execution receipt

Receipt date: 2026-09-02

Task mode: execution only

Branch: `codex/astrohd-owner-intake-quality-v1`

Starting HEAD: `c0f401aefa8b17b17a00a6b6ef5e1a7362807ed1`

Ending implementation HEAD: `1c5c3175c510b6a55e55138f9b184b7efbe08e40`

## Executed artifacts

Added:

- `docs/research/ASTROHD_THEORY_LANGUAGE_EXPOSURE_SIGNAL_SPEC.md`
- `docs/research/ASTROHD_FUTURE_ITEM_REVIEW_TEMPLATE.md`
- `reference/core/astrohd_theory_language_codebook_v1.template.json`
- `reference/core/astrohd_theory_language_exposure_synthetic_fixtures_v1.json`
- `reference/audits/astrohd_frozen_rule_prompt_mapping_v1.json`
- `scripts/extract_astrohd_frozen_rule_prompt_mapping.py`
- `tests/unit/test_astrohd_frozen_mapping_extract.py`

Changed:

- `src/hdmatch/evaluation/theory_language_exposure.py`
- `scripts/audit_astrohd_theory_language_exposure.py`
- `tests/unit/test_theory_language_exposure.py`
- `CURRENT_PLAN.md`
- `docs/36_astrohd_owner_pilot.md`
- `state/CURRENT-STATE.md`
- `state/EXTRA-HIGH-CONTAMINATION-COVERAGE-REVIEW-2026-09-02.md`

Removed as superseded execution overreach:

- `docs/38_astrohd_theory_language_exposure_and_coverage.md`
- `reference/research/astrohd_current_questionnaire_coverage_audit_v1.json`
- `reference/research/astrohd_future_item_evaluation_template_v1.json`
- `reference/research/astrohd_theory_language_codebook_v0_1.json`
- `reference/research/astrohd_theory_language_exposure_dry_run_v0_1.json`
- `reference/research/astrohd_theory_language_exposure_fixtures_v0_1.json`
- `scripts/audit_astrohd_questionnaire_coverage.py`
- `tests/unit/test_astrohd_questionnaire_coverage.py`

## Frozen mapping extraction

- Exact source path: `mappings/mapping_library_v1.json`
- Exact source SHA-256:
  `3424672432f7f071ec90ef9ddce52a67ff6794911e92b1a1e04f079262ea6200`
- Mechanical filter: stored mapping status equals `frozen`
- Mechanically observed distinct rule count: `27`
- Mechanically observed distinct mapped-prompt count: `23`
- Acceptance check: `PASS`
- Source mapping file changed: `no`
- Question-bank file changed: `no`

The extract records only rule identifiers, prompt identifiers, reciprocal counts/lists,
prompts shared by multiple rules, and rules mapped to multiple prompts. It does not use
a larger question-bank inventory as a denominator and contains no coverage-quality or
new-question classification.

## Verification executed

1. Focused exposure/mapping command:

   ```text
   .venv/bin/pytest -q tests/unit/test_theory_language_exposure.py tests/unit/test_astrohd_frozen_mapping_extract.py tests/unit/test_model_mapping_library.py tests/unit/test_questionnaire_bank.py
   ```

   Result: `22 passed`.

2. Synthetic fixture runner:

   ```text
   .venv/bin/python scripts/audit_astrohd_theory_language_exposure.py
   ```

   Result: `9/9 synthetic cases passed`.

3. Mechanical mapping extractor:

   ```text
   .venv/bin/python scripts/extract_astrohd_frozen_rule_prompt_mapping.py
   ```

   Result: `27` distinct frozen rules, `23` distinct mapped prompts,
   `counts_match=true`.

4. Full repository unit suite:

   ```text
   .venv/bin/pytest -q
   ```

   Result: `302 passed, 1 skipped`. The skip is the existing environment-dependent
   natal-pilot test for unavailable official Swiss Ephemeris files.

5. Strict source typing:

   ```text
   .venv/bin/mypy src/hdmatch
   ```

   Result: `Success: no issues found in 120 source files`.

6. Ruff on all touched Python files: `PASS`.
7. JSON parse checks for the codebook template, fixtures, and mapping extract: `PASS`.
8. `git diff --check`: `PASS`.

## Scope confirmations

- No participant eligibility, interview-flow, prompt, scoring, `EvidenceInput`,
  progress, lock, reveal, primary-analysis, deployment, or workflow file was changed.
- No production module imports or calls the isolated exposure scaffold.
- No current 27-rule mapping or 23 mapped prompt was altered.
- No real participant data was added. All fixture records are explicitly synthetic.
- No real astrology or Human Design theory-language vocabulary was added. The complete
  template phrase inventory is `THEORYTERM_ALPHA`, `THEORY PHRASE BETA`,
  `CONTEXTTERM_DELTA`, and `COMMONWORD_GAMMA`.
- No numerical exposure score, threshold, binary contaminated/clean classification,
  fuzzy matching, embeddings, LLM matching, stemming expansion, ontology inference,
  automatic language inference, translation classification, or chart-fit input exists.
- No merge, rebase, reset, deployment, participant contact, or spending occurred.

## Unresolved authority boundary

The three unresolved items are preserved verbatim in the draft specification and were
not decided by this execution worker. They did not block the requested scaffolding.

Stop trigger reached: bounded implementation and verification complete; return this
receipt and exact GitHub state to the supervising reasoning chat.
