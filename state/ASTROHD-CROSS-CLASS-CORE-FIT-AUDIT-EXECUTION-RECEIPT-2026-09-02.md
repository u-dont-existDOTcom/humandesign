# AstroHD cross-class core-fit audit execution receipt

Receipt date: 2026-09-02

Task mode: execution-only mechanical diagnostic

Branch: `codex/astrohd-owner-intake-quality-v1`

Starting HEAD: `cf4029dce6bac657c927bb25fee3c537b23c4511`

Ending implementation HEAD: `bf18853afc1bd469cc95d663fe1816fb15338ef1`

## Files added

- `scripts/audit_astrohd_cross_class_core_fit.py`
- `reference/audits/astrohd_cross_class_core_fit_v1.json`
- `tests/unit/test_astrohd_cross_class_core_fit_audit.py`
- `state/ASTROHD-CROSS-CLASS-CORE-FIT-AUDIT-EXECUTION-RECEIPT-2026-09-02.md`

No pre-existing file was changed by this execution slice.

## Exact source artifacts

- `mappings/mapping_library_v1.json`
  - SHA-256: `3424672432f7f071ec90ef9ddce52a67ff6794911e92b1a1e04f079262ea6200`
- `src/hdmatch/model/dependencies.py`
  - SHA-256: `a49672a0edbca3ecbd121d563f7f7758b521a3cdf317c058b42ad9f137504a7d`
- `src/hdmatch/model/symbolic_score.py`
  - SHA-256: `fd1f216c2579aab0ba9aef74249fa5804cb7433b7eb13f452dfe1381b09f0aaa`
- `src/hdmatch/participant/backend.py`
  - SHA-256: `80ad02402ec0ea3a094bcd2977e9843c68d296b198bcfc7e836ef71043313198`

The audit reads the current frozen mapping and calls the current scorer,
dependency collapse, and participant ranking implementation without modifying
any of those source artifacts.

## Source-mismatch stop and revised directive

The first Extra-High directive expected A2/B2 `core_fit` to equal `75.0`, using
a Diagnostic Center block fraction of `0.9`. Execution observed
`78.57142857142857` and stopped that subtask under the directive's explicit
source-mismatch rule.

The mismatch receipt was returned to the same verified signed-in ChatGPT Pro
conversation with visible `Extra High` mode. The supervising Extra-High review
inspected the bound source and revised only the mechanical expectations:

- ordinary evidence support uses structural salience multiplied by mapping
  directness;
- current `_core_fit` receives mapping directness when mapping support is
  nonzero;
- therefore the directed C02/C08 Diagnostic Center block fraction is `1.0`;
- the revised audit records existing behavior and does not change it.

No owner decision was required for resolving that expectation mismatch.

## Mechanically observed dependency inventory

The exact dependency clusters whose frozen mappings span more than one
structural class are:

- `AUTHORITY_DECISION`
  - structural classes: `authority`, `diagnostic_center`
- `TYPE_STRATEGY_ARCHITECTURE`
  - structural classes: `diagnostic_center`, `type_strategy`

The directed source rows record:

- D03 / `MAP-AUTH-EMOTIONAL-D03`: `authority`,
  `AUTHORITY_DECISION`
- C02 / `MAP-CENTER-SOLARPLEXUS-DEFINED-C02`: `diagnostic_center`,
  `AUTHORITY_DECISION`
- S02 / `MAP-TYPE-GENERATOR-S02`: `type_strategy`,
  `TYPE_STRATEGY_ARCHITECTURE`
- C08 / `MAP-CENTER-SACRAL-DEFINED-C08`: `diagnostic_center`,
  `TYPE_STRATEGY_ARCHITECTURE`

## Controlled scorer results

Every synthetic response uses behavioral confidence `1.0`, measurement
reliability `1.0`, and synthetic prevalence `0.5` for every frozen structural
anchor.

### A1 — Authority baseline

- net rubric bits: `1.0`
- contradiction rubric bits: `0.0`
- detailed support: `50.0`
- core fit: `66.66666666666667`
- available core weight: `45.0`
- earned core weight: `30.0`

### A2 — Authority plus same-cluster Diagnostic Center response

- net rubric bits: `1.0`
- contradiction rubric bits: `0.0`
- detailed support: `50.0`
- core fit: `78.57142857142857`
- available core weight: `70.0`
- earned core weight: `55.0`
- Authority fraction/earned weight: `1.0` / `30.0`
- Diagnostic Center fraction/earned weight: `1.0` / `25.0`
- Profile fraction/earned weight: `0.0` / `0.0`

A1 to A2 leaves net rubric bits, contradiction rubric bits, and detailed
support unchanged while the mechanically returned core fit changes from
`66.66666666666667` to `78.57142857142857`.

### B1 — Type/Strategy baseline

- net rubric bits: `1.0`
- contradiction rubric bits: `0.0`
- detailed support: `50.0`
- core fit: `66.66666666666667`
- available core weight: `45.0`
- earned core weight: `30.0`

### B2 — Type/Strategy plus same-cluster Diagnostic Center response

- net rubric bits: `1.0`
- contradiction rubric bits: `0.0`
- detailed support: `50.0`
- core fit: `78.57142857142857`
- available core weight: `70.0`
- earned core weight: `55.0`
- Type/Strategy fraction/earned weight: `1.0` / `30.0`
- Diagnostic Center fraction/earned weight: `1.0` / `25.0`
- Profile fraction/earned weight: `0.0` / `0.0`

B1 to B2 leaves net rubric bits, contradiction rubric bits, and detailed
support unchanged while the mechanically returned core fit changes from
`66.66666666666667` to `78.57142857142857`.

## Global dependency-collapse results

### A2 / `AUTHORITY_DECISION`

- raw relevant-cluster contribution count: `2`
- collapsed relevant-cluster contribution count: `1`
- winning mapping: `MAP-AUTH-EMOTIONAL-D03`
- winning support: `1.0`
- winning/resulting evidence rubric bits: `1.0` / `1.0`

### B2 / `TYPE_STRATEGY_ARCHITECTURE`

- raw relevant-cluster contribution count: `3`
- collapsed relevant-cluster contribution count: `1`
- winning mapping: `MAP-TYPE-GENERATOR-S02`
- winning support: `1.0`
- winning/resulting evidence rubric bits: `1.0` / `1.0`

## Ranking result

Two synthetic scored states held net rubric bits, evidence rubric bits,
contradiction rubric bits, meaningful contradictions, and detailed support
equal. Their only differing score field was:

- `LOW.core_fit`: `66.66666666666667`
- `HIGH.core_fit`: `78.57142857142857`

The current participant `_rank_states` behavior ordered `HIGH` first with
scientific rank `1.0` and `LOW` second with scientific rank `2.0`.

## Verification executed

1. Focused cross-class audit tests:

   ```text
   .venv/bin/pytest -q tests/unit/test_astrohd_cross_class_core_fit_audit.py
   ```

   Result: `13 passed`.

2. Combined cross-class, categorical-coverage, scoring-structure, and frozen
   mapping audit tests:

   ```text
   .venv/bin/pytest -q tests/unit/test_astrohd_cross_class_core_fit_audit.py tests/unit/test_astrohd_core_categorical_coverage.py tests/unit/test_astrohd_frozen_scoring_structure.py tests/unit/test_astrohd_frozen_mapping_extract.py
   ```

   Result: `30 passed`.

3. Full repository unit suite:

   ```text
   .venv/bin/pytest -q
   ```

   Result: `329 passed, 1 skipped`. The existing environment-dependent skip is
   for unavailable official Swiss Ephemeris files.

4. Strict typing:

   ```text
   .venv/bin/mypy src/hdmatch scripts/audit_astrohd_cross_class_core_fit.py
   ```

   Result: `Success: no issues found in 121 source files`.

5. Ruff and format checks:

   ```text
   .venv/bin/ruff check scripts/audit_astrohd_cross_class_core_fit.py tests/unit/test_astrohd_cross_class_core_fit_audit.py
   .venv/bin/ruff format --check scripts/audit_astrohd_cross_class_core_fit.py tests/unit/test_astrohd_cross_class_core_fit_audit.py
   ```

   Result: `PASS`; both files formatted.

6. Generated JSON validation:

   ```text
   .venv/bin/python -m json.tool reference/audits/astrohd_cross_class_core_fit_v1.json
   ```

   Result: `PASS`.

7. Whitespace/error check:

   ```text
   git diff --check
   ```

   Result: `PASS`.

The tests also prove byte-identical regeneration, exact source hashes, exact
cross-class cluster enumeration, the current source support bases, global
dependency collapse, and ranking behavior with all preceding score fields held
equal.

## Scope confirmations

- Codex made no scientific, methodological, interpretive, governance, or
  owner-policy decision.
- No frozen mapping, dependency cluster, source scoring/ranking behavior, core
  weight, mapping status, answer token, question, questionnaire, candidate
  disposition, theory-language exposure behavior, eligibility, stopping,
  evidence sufficiency, lock/reveal behavior, primary analysis, or deployment
  behavior changed.
- No hidden owner chart or participant answers were inspected.
- No real participant data was added.
- No merge, rebase, reset, deployment, invitation rotation, participant-session
  creation, participant contact, or spending occurred.

Return this audit and receipt to the verified supervising Extra-High/Pro
reasoning chat. Do not merge or deploy.
