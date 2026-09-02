# AstroHD PR #23 final convergence audit execution receipt

Receipt date: 2026-09-02

Task mode: execution-only mechanical final PR convergence audit

Branch: `codex/astrohd-owner-intake-quality-v1`

Starting HEAD: `b3da97274c161a31e44cee3ef4159ca0d1d9a0dd`

PR base commit: `afc0bb82de0e481ae5a5d3453e0bcaf82b2a0286`

Audit implementation commit: `ede426902d922614bdff30070df68ce423bf71e1`

The receipt is committed separately after the audit implementation boundary,
so its own commit hash is not self-embedded. The pushed draft-PR head is the
canonical documentary boundary.

## Exact four files added

- `scripts/audit_astrohd_pr23_convergence.py`
- `reference/audits/astrohd_pr23_convergence_v1.json`
- `tests/unit/test_astrohd_pr23_convergence.py`
- `state/ASTROHD-PR23-CONVERGENCE-AUDIT-EXECUTION-RECEIPT-2026-09-02.md`

No existing file was modified by this task.

Generated audit SHA-256:
`952565c9da16d683711f2bdae1fc8cae974f9c17ce98166a2de00b54d6856e73`.

## Mechanical PR-delta inventory

The audit reads the exact Git range:

```text
afc0bb82de0e481ae5a5d3453e0bcaf82b2a0286...b3da97274c161a31e44cee3ef4159ca0d1d9a0dd
```

It records `59` changed paths with Git status, literal path category, and the
SHA-256 of the file at the audited head when the path exists.

Literal category counts:

- `src`: `9`
- `tests`: `10`
- `scripts`: `6`
- `reference`: `13`
- `docs`: `3`
- `state`: `17`
- repository root/other: `1`

These counts are descriptive only.

## Owner-correction remnant and runtime-symbol observations

The exact case-insensitive literal scan found:

- current non-historical active surfaces: `14` occurrences;
- `state/**`: `34` occurrences, recorded separately as
  `historical_or_state_records_not_runtime_scan`.

The active-surface occurrences consist mechanically of owner-correction wording
in `CURRENT_PLAN.md` and `docs/36_astrohd_owner_pilot.md`, plus the exact
`required_question_count` token in two Custom GPT OpenAPI files and current
participant runtime source. No interpretation or edit was made.

The AST runtime-identifier scan had an expected production occurrence count of
zero and mechanically observed `5` definition/reference nodes, all named
`required_question_count`:

1. `src/hdmatch/participant/models.py:366` — `name_definition`
2. `src/hdmatch/participant/models.py:388` — `attribute_reference`
3. `src/hdmatch/participant/models.py:388` — `keyword_reference`
4. `src/hdmatch/participant/models.py:406` — `name_definition`
5. `src/hdmatch/participant/service.py:397` — `keyword_reference`

The directive required a zero-occurrence regression assertion and separately
required nonzero source to be reported without editing or interpretation. The
new test therefore fails deterministically with observed `5 != 0`. That
subtask was not repaired; all independent audit work continued.

## Rank and `core_fit` convergence

The current participant rank-ordering expressions are mechanically:

1. `-scores[state.state_id].net_rubric_bits`
2. `scores[state.state_id].meaningful_contradictions`
3. `-scores[state.state_id].detailed_support`
4. `-(state.end_utc - state.start_utc).total_seconds()`
5. `state.start_utc`

The current scientific equality expressions are mechanically:

1. `round(score.net_rubric_bits, 12)`
2. `score.meaningful_contradictions`
3. `round(score.detailed_support, 12)`

The current date `best_state` key is mechanically:

1. `item.net_rubric_bits`
2. `-item.meaningful_contradictions`
3. `item.detailed_support`
4. `item.state_id`

The `_top_net_margin` source segment is byte-identical at the rank-correction
start and audited head, with SHA-256
`d3b1ff9e93ab8a10ffc35424e25c1a8243420c29de5b1ddb48041c8568a0b172`.
The date-aggregator file differs from rank-correction starting HEAD only by the
directed removal of `item.core_fit` from the `best_state` key.

The full production `core_fit` textual inventory contains `10` occurrences.
Mechanically observed occurrences inside a sort key, max/min key, or rank
equality key: `0`.

## Theory-language runtime isolation

The defining module and its thirteen public class/function symbols are recorded
mechanically. Outside
`src/hdmatch/evaluation/theory_language_exposure.py`, the production source has:

- importer count: `0`
- call-site count: `0`

No inference was made about future wiring.

## Future-core authorization invariant

The candidate matrix contains exactly seven target IDs:

- `authority.ego_manifested`
- `authority.ego_projected`
- `authority.lunar`
- `authority.mental_environmental`
- `authority.self_projected`
- `type_strategy.manifestor`
- `type_strategy.reflector`

Every row mechanically retains:

- `runtime_authorized: false`
- `mapping_authorized: false`
- `question_change_authorized: false`
- `owner_policy: false`

## Frozen mapping/question-bank invariants

- `mappings/mapping_library_v1.json` SHA-256:
  `3424672432f7f071ec90ef9ddce52a67ff6794911e92b1a1e04f079262ea6200`
- `reference/core/question_bank_v1.json` SHA-256:
  `31f813efc3da7263569ef010a8336b1b1b0c44801b7aa0f91e33b3fa4587d820`
- stored frozen mappings: `27`
- distinct frozen rule IDs: `27`
- distinct frozen-mapped prompt IDs: `23`
- interpretation marker:
  `descriptive_only_not_a_completeness_denominator`

No target questionnaire count was derived.

## Historical-audit invariants

- `reference/audits/astrohd_cross_class_core_fit_v1.json` SHA-256:
  `a113fb53de13f38d5053955975912a1fb194f527c57f610c82d0efc38bc32a70`
- `reference/audits/astrohd_rank_tiebreak_downstream_v1.json` SHA-256:
  `c9fb9ee6060c4bbb346c7ac6981a543d3d602a60bb1da83e245cea638a680103`

Mechanical invocation of both historical generators against current source
raised `HistoricalAuditSourceMismatch`; neither temporary output was created.
Neither historical JSON file was rewritten.

## Freeze/runtime binding

`assert_freeze_compatible` still compares active runtime values against all of
the following frozen values:

- source commit
- chart engine
- model version
- model bytes
- mapping bytes
- question-bank version
- question-bank bytes

The exact source-commit comparison remains `self.code_commit` against
`freeze.code_commit`. The freeze schema was not changed.

## Coordination-document heading inventory

The generated audit records the first H1, every H2, and exact SHA-256 for:

- `CURRENT_PLAN.md`
- `docs/36_astrohd_owner_pilot.md`
- `state/CURRENT-STATE.md`
- `state/OWNER-CORRECTION-2026-09-02.md`

No judgment about the text and no document edit was made.

## Verification executed

1. New convergence tests:

   ```text
   .venv/bin/pytest -q tests/unit/test_astrohd_pr23_convergence.py
   ```

   Result: `13 passed, 1 failed`. The sole failure is the directed
   zero-runtime-symbol assertion observing five `required_question_count` AST
   nodes.

2. Independent rank, date, historical-audit, theory-language, coverage,
   scoring-structure, frozen-mapping, and freeze/runtime tests:

   ```text
   .venv/bin/pytest -q tests/unit/test_participant_ranking_semantics.py tests/unit/test_date_aggregator.py tests/unit/test_astrohd_cross_class_core_fit_audit.py tests/unit/test_astrohd_rank_tiebreak_downstream_audit.py tests/unit/test_theory_language_exposure.py tests/unit/test_astrohd_core_categorical_coverage.py tests/unit/test_astrohd_frozen_scoring_structure.py tests/unit/test_astrohd_frozen_mapping_extract.py tests/unit/test_freeze_and_manifest.py tests/unit/test_participant_universe_binding.py tests/unit/test_runtime_adapters.py
   ```

   Result: `71 passed`.

3. Full repository suite:

   ```text
   .venv/bin/pytest -q
   ```

   Result: `354 passed, 1 failed, 1 skipped`. The sole failure is the same
   runtime-symbol assertion. The existing environment-dependent skip is for
   unavailable official Swiss Ephemeris files.

4. Strict typing:

   ```text
   .venv/bin/mypy src/hdmatch scripts/audit_astrohd_pr23_convergence.py
   ```

   Result: `Success: no issues found in 121 source files`.

5. New-file lint and formatting:

   ```text
   .venv/bin/ruff check scripts/audit_astrohd_pr23_convergence.py tests/unit/test_astrohd_pr23_convergence.py --ignore E501,I001
   .venv/bin/ruff format --check scripts/audit_astrohd_pr23_convergence.py tests/unit/test_astrohd_pr23_convergence.py
   ```

   Result: all checks passed; both files are formatted.

6. Artifact and diff checks:

   - `python -m json.tool reference/audits/astrohd_pr23_convergence_v1.json`:
     `PASS`
   - byte-identical regeneration: `PASS`
   - no production/source mutation during regeneration: `PASS`
   - `git diff --check`: `PASS`

## Verification-efficiency telemetry

- observed elapsed task time at summary: `499.02s`
- observed test time: `26.05s` (`5.22%`)
- focused: one run, `6.98s`, one failure-discovering run
- affected: one run, `2.47s`, no failure-discovering run
- full: one run, `16.61s`, one failure-discovering run
- forced redundant green reruns: `0`
- redundant green runs skipped: `0`
- mutation tests: not run; no directive or risk trigger requested them

## Scope confirmations

- No production file or existing documentation/state file was changed.
- No production behavior, methodology, mapping, question, scoring, ranking,
  owner policy, PR metadata, deployment state, invitation, or participant
  session was changed.
- No historical JSON was rewritten.
- No real participant data was read or added.
- Codex made no scientific, methodological, merge, release, or owner-policy
  decision.
- No merge, deployment, invitation rotation, participant contact, or spending
  occurred.

The directive's execution boundary is reached with one exact mechanical
mismatch. Return the audit, this receipt, and failing assertion to the verified
Extra-High/Pro reasoning chat. Do not update the PR body, mark the PR ready,
merge, or deploy.
