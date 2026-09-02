# AstroHD core-coverage preparation execution receipt

Receipt date: 2026-09-02

Task mode: execution only

Branch: `codex/astrohd-owner-intake-quality-v1`

Starting HEAD: `61c06a006f0f214b58b3fde0851448495d8abe22`

Ending implementation HEAD: `1a7ef53af1e5561125ce448973a0d37eb2e60bab`

## Files added

- `scripts/extract_astrohd_core_categorical_coverage.py`
- `reference/audits/astrohd_core_categorical_coverage_v1.json`
- `reference/research/astrohd_future_core_coverage_candidate_matrix_v1.json`
- `state/EXTRA-HIGH-ASTROHD-CORE-COVERAGE-DISPOSITION-2026-09-02.md`
- `tests/unit/test_astrohd_core_categorical_coverage.py`
- `state/ASTROHD-CORE-COVERAGE-PREP-EXECUTION-RECEIPT-2026-09-02.md`

No pre-existing file was changed by this execution slice.

## Exact source artifacts

- `src/hdmatch/chart/bodygraph.py`
  - SHA-256: `5bda8c935e7d58521929acb8f8528e87b958a7b92fc171bc11ac3ff8372b960b`
- `mappings/mapping_library_v1.json`
  - SHA-256: `3424672432f7f071ec90ef9ddce52a67ff6794911e92b1a1e04f079262ea6200`
- `reference/core/question_bank_v1.json`
  - SHA-256: `31f813efc3da7263569ef010a8336b1b1b0c44801b7aa0f91e33b3fa4587d820`
- `reference/audits/astrohd_frozen_scoring_structure_v1.json`
  - SHA-256: `28df376c5731905beea6c71104d21523e4a562ca8d36d7d7d47a16e358c2b50c`

The extractor reads those source artifacts and does not modify them.

## Mechanical results

### Type + Strategy frozen paths

- `manifestor`: `0` matching rules; path `false`
- `generator`: `2` matching rules; path `true`
- `manifesting_generator`: `2` matching rules; path `true`
- `projector`: `2` matching rules; path `true`
- `reflector`: `0` matching rules; path `false`

Observed Generator/Manifesting Generator rule IDs:

- `MAP-TYPE-GENERATOR-S02`
- `MAP-TYPE-GENERATOR-S05`

Observed Projector rule IDs:

- `MAP-TYPE-PROJECTOR-S03`
- `MAP-TYPE-PROJECTOR-S04`

### Authority frozen paths

- `emotional_solar_plexus`: `2` matching rules; path `true`
- `sacral`: `1` matching rule; path `true`
- `splenic`: `2` matching rules; path `true`
- `ego_manifested`: `0`; path `false`
- `ego_projected`: `0`; path `false`
- `self_projected`: `0`; path `false`
- `mental_environmental`: `0`; path `false`
- `lunar`: `0`; path `false`

Observed Authority rule IDs:

- Emotional: `MAP-AUTH-EMOTIONAL-D01`, `MAP-AUTH-EMOTIONAL-D03`
- Sacral: `MAP-AUTH-SACRAL-D01`
- Splenic: `MAP-AUTH-SPLENIC-D01`, `MAP-AUTH-SPLENIC-D02`

The path booleans mean only whether at least one current frozen mapping matches
the engine value.

### Profile-line frozen paths

- Line `1`: `1` matching rule
- Line `2`: `2` matching rules
- Line `3`: `2` matching rules
- Line `4`: `1` matching rule
- Line `5`: `1` matching rule
- Line `6`: `2` matching rules

All six path booleans are `true`. These rule counts are not independent evidence
counts.

### D01 declared-token disposition

The declared answer tokens with neither a frozen support rule nor a frozen
contradiction rule are exactly:

- `clarity_from_being_in_the_right_place_or_with_the_right_listener`
- `hearing_your_own_words_reveal_the_answer`
- `no_stable_pattern`

No mapping was created for those tokens.

### Descriptive dependency summary

- Frozen rules: `27`
- Frozen-mapped prompts: `23`
- Observation groups: `20`
- Dependency clusters: `7`
- Interpretation marker: `descriptive_only_not_independent_sample_counts`

None of these is a required denominator or target questionnaire count.

### Candidate matrix

The matrix contains exactly the seven directed target rows:

- `type_strategy.manifestor`
- `type_strategy.reflector`
- `authority.self_projected`
- `authority.mental_environmental`
- `authority.ego_manifested`
- `authority.ego_projected`
- `authority.lunar`

Every row records `runtime_authorized: false`, `mapping_authorized: false`,
`question_change_authorized: false`, and `owner_policy: false`. No proposed
participant-facing wording is present.

## Verification executed

1. New focused categorical tests:

   ```text
   .venv/bin/pytest -q tests/unit/test_astrohd_core_categorical_coverage.py
   ```

   Result: `8 passed`.

2. Combined categorical, scoring-structure, and frozen-mapping audit tests:

   ```text
   .venv/bin/pytest -q tests/unit/test_astrohd_core_categorical_coverage.py tests/unit/test_astrohd_frozen_scoring_structure.py tests/unit/test_astrohd_frozen_mapping_extract.py
   ```

   Result: `17 passed`.

3. New generated JSON validation:

   ```text
   .venv/bin/python -m json.tool reference/audits/astrohd_core_categorical_coverage_v1.json
   .venv/bin/python -m json.tool reference/research/astrohd_future_core_coverage_candidate_matrix_v1.json
   ```

   Result: `PASS` for both files.

4. Full repository unit suite:

   ```text
   .venv/bin/pytest -q
   ```

   Result: `316 passed, 1 skipped`. The existing environment-dependent skip is
   for unavailable official Swiss Ephemeris files.

5. Strict typing:

   ```text
   .venv/bin/mypy src/hdmatch scripts/extract_astrohd_core_categorical_coverage.py
   ```

   Result: `Success: no issues found in 121 source files`.

6. Ruff and format checks:

   ```text
   .venv/bin/ruff check scripts/extract_astrohd_core_categorical_coverage.py tests/unit/test_astrohd_core_categorical_coverage.py
   .venv/bin/ruff format --check scripts/extract_astrohd_core_categorical_coverage.py tests/unit/test_astrohd_core_categorical_coverage.py
   ```

   Result: `PASS`; both files formatted.

7. Whitespace/error check:

   ```text
   git diff --check
   ```

   Result: `PASS`.

The tests additionally establish mechanical enumeration of current engine Type
and Authority values, exact profile-line counts, the exact D01 token set,
byte-identical regeneration of both new JSON artifacts, the exact seven matrix
rows, false authorization fields, unchanged source hashes, and absence of a
required or recommended questionnaire count.

## Scope confirmations

- Codex made no scientific, methodological, governance, interpretive, or
  owner-policy decision. The disposition and candidate matrix copy only the
  resolved Extra-High directive.
- No mapping, mapping status, answer token, contradiction rule, dependency
  cluster, weight, question, prompt wording, minimum-evidence requirement,
  scoring, ranking, theory-language exposure behavior, eligibility, stopping,
  evidence sufficiency, lock/reveal behavior, primary analysis, or deployment
  behavior changed.
- No hidden owner chart or participant answer was inspected to decide coverage.
- No questionnaire-completeness denominator or numeric additional-question
  target was inferred.
- No real participant data was added.
- No merge, rebase, reset, deployment, invitation rotation, participant-session
  creation, participant contact, or spending occurred.

Return this receipt to the verified supervising Extra-High/Pro reasoning chat.
