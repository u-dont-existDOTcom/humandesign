# AstroHD rank-semantics correction execution receipt

Receipt date: 2026-09-02

Task mode: execution-only implementation of the verified Extra-High directive

Branch: `codex/astrohd-owner-intake-quality-v1`

Starting HEAD: `f5a967c2efbb0f73a7a56c42a06fe4d7fb7e2b59`

Ending implementation HEAD: `79d32029ee1d22d268ec3f9b32601aa5917d6aa9`

The receipt is committed separately after the implementation boundary, so its
own commit hash is not self-embedded. The pushed draft-PR head is the canonical
documentation boundary.

## Files changed by the implementation commit

- `src/hdmatch/participant/backend.py`
- `src/hdmatch/search/date_aggregator.py`
- `scripts/audit_astrohd_cross_class_core_fit.py`
- `scripts/audit_astrohd_rank_tiebreak_downstream.py`
- `tests/unit/test_participant_ranking_semantics.py`
- `tests/unit/test_date_aggregator.py`
- `tests/unit/test_astrohd_cross_class_core_fit_audit.py`
- `tests/unit/test_astrohd_rank_tiebreak_downstream_audit.py`
- `state/EXTRA-HIGH-ASTROHD-RANK-SEMANTICS-CORRECTION-2026-09-02.md`

This receipt is the only additional file.

## Exact implemented semantics

`AstroHDParticipantBackend._rank_states` now orders states by exactly:

1. descending `net_rubric_bits`;
2. ascending `meaningful_contradictions`;
3. descending `detailed_support`;
4. descending state duration for deterministic display inside a scientific tie;
5. ascending start time for deterministic display inside a scientific tie.

`_evidence_tie_key` contains only rounded `net_rubric_bits`,
`meaningful_contradictions`, and rounded `detailed_support`. It no longer uses
`core_fit`. `_top_net_margin` is unchanged.

Date-level `best_state` selection now uses exactly:

```text
(item.net_rubric_bits, -item.meaningful_contradictions, item.detailed_support, item.state_id)
```

The date-score and date-rank algorithms are unchanged. `core_fit` remains
calculated, serialized, and reportable, but it no longer affects state order,
scientific-rank equality, or date-level `best_state` selection.

Current source hashes after the correction:

- `src/hdmatch/participant/backend.py`:
  `8ceb0b18bcf6d9ddb0573b433c1d88802f5890e3ae4a8d9da53a778da673169f`
- `src/hdmatch/search/date_aggregator.py`:
  `32a328413fcc4b90535e19c4ceda8aedfb2869e9f24db50e325e6c6322892b01`

## Historical-audit preservation

Both pre-patch generators now verify their audited source baseline before
`write_audit` and raise the dedicated `HistoricalAuditSourceMismatch` exception
when current source differs. Their tests preserve the historical content
assertions and now verify this fail-closed behavior instead of assuming the
historical artifacts can be regenerated from changed production semantics.

The historical JSON artifacts were not changed:

- `reference/audits/astrohd_cross_class_core_fit_v1.json`:
  `a113fb53de13f38d5053955975912a1fb194f527c57f610c82d0efc38bc32a70`
- `reference/audits/astrohd_rank_tiebreak_downstream_v1.json`:
  `c9fb9ee6060c4bbb346c7ac6981a543d3d602a60bb1da83e245cea638a680103`

The prior controlled `core_fit` values also remain numerically unchanged:

- A1: `66.66666666666667`
- A2: `78.57142857142857`
- B1: `66.66666666666667`
- B2: `78.57142857142857`

## Frozen mapping and questionnaire invariants

The exact frozen rule-to-prompt mapping source remains
`mappings/mapping_library_v1.json` with SHA-256
`3424672432f7f071ec90ef9ddce52a67ff6794911e92b1a1e04f079262ea6200`.
The mechanical extract remains exactly `27` distinct frozen rules and `23`
distinct mapped questionnaire prompts. Neither count is treated as a
questionnaire-completeness denominator.

The question bank remains `reference/core/question_bank_v1.json` with SHA-256
`31f813efc3da7263569ef010a8336b1b1b0c44801b7aa0f91e33b3fa4587d820`.
The frozen mapping, question bank, PredictionFreeze/schema/model, evidence
semantics, dependency collapse, and `core_fit` calculation were not changed.
Exact code-commit binding continues to prevent an older frozen session from
continuing under the corrected code.

## Tests and checks executed

1. Focused rank, date, and historical-audit tests:

   ```text
   .venv/bin/pytest -q tests/unit/test_participant_ranking_semantics.py tests/unit/test_date_aggregator.py tests/unit/test_astrohd_cross_class_core_fit_audit.py tests/unit/test_astrohd_rank_tiebreak_downstream_audit.py
   ```

   Result: `28 passed`.

2. Affected coverage, scoring-structure, frozen-mapping, questionnaire,
   freeze, participant-session, universe-binding, and runtime tests:

   ```text
   .venv/bin/pytest -q tests/unit/test_astrohd_core_categorical_coverage.py tests/unit/test_astrohd_frozen_mapping_extract.py tests/unit/test_astrohd_frozen_scoring_structure.py tests/unit/test_model_mapping_library.py tests/unit/test_questionnaire_bank.py tests/unit/test_freeze_and_manifest.py tests/unit/test_participant_session.py tests/unit/test_participant_universe_binding.py tests/unit/test_runtime_adapters.py
   ```

   Result: `72 passed`.

3. Full repository suite:

   ```text
   .venv/bin/pytest -q
   ```

   Result: `341 passed, 1 skipped`. The existing environment-dependent skip is
   for unavailable official Swiss Ephemeris files.

4. Strict typing:

   ```text
   .venv/bin/mypy src/hdmatch
   ```

   Result: `Success: no issues found in 120 source files`.

5. Ruff and formatting:

   ```text
   .venv/bin/ruff check src tests --ignore E501,I001
   .venv/bin/ruff check scripts/audit_astrohd_cross_class_core_fit.py scripts/audit_astrohd_rank_tiebreak_downstream.py --ignore E501,I001
   .venv/bin/ruff format --check src/hdmatch/participant/backend.py src/hdmatch/search/date_aggregator.py tests/unit/test_participant_ranking_semantics.py tests/unit/test_date_aggregator.py tests/unit/test_astrohd_cross_class_core_fit_audit.py tests/unit/test_astrohd_rank_tiebreak_downstream_audit.py scripts/audit_astrohd_cross_class_core_fit.py scripts/audit_astrohd_rank_tiebreak_downstream.py
   ```

   Result: all checks passed; all eight Python files are formatted. The first
   format check identified two test files for formatting; the formatter changed
   only layout, after which the final check passed.

6. JSON and repository integrity:

   - `python -m json.tool` passed for both historical audits, the frozen mapping,
     and the question bank.
   - `git diff --check` passed.
   - Exact SHA-256 checks passed for both historical audits, the frozen mapping,
     and the question bank.

## Verification-efficiency telemetry

- observed elapsed task time at summary: `160.77s`
- observed test time: `13.41s` (`8.34%`)
- focused: one run, `1.39s`, no failure-discovering run
- affected: one run, `3.36s`, no failure-discovering run
- full: one run, `8.66s`, no failure-discovering run
- forced redundant green reruns: `0`
- redundant green runs skipped: `0`
- mutation tests: not run; no directive or risk trigger requested them

## Scope confirmations

- The only production semantic change is the authorized exclusion of
  `core_fit` from state ordering, scientific-rank equality, and date-level
  `best_state` selection.
- No production participant flow, prompting, eligibility, stopping,
  EvidenceInput semantics, progress, lock, reveal, primary-analysis,
  deployment, or release file was semantically changed.
- No frozen rule, mapped prompt, questionnaire item, evidence-sufficiency
  policy, dependency behavior, `core_fit` calculation, or replacement metric
  was added or changed.
- No historical audit JSON, receipt, or earlier disposition was altered.
- No real participant data was read or added.
- No real Human Design or astrology theory-language vocabulary was invented or
  added.
- No merge, deployment, invitation/session mutation, participant contact, or
  spending occurred.

The directive's execution boundary is reached. Return this receipt and exact
draft-PR head to the verified Extra-High reasoning chat for review and the next
bounded directive. Do not merge or deploy.
