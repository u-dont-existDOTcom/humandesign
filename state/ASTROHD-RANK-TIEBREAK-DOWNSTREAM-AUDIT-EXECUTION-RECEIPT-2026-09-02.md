# AstroHD rank-tiebreak downstream audit execution receipt

Receipt date: 2026-09-02

Task mode: execution-only downstream-impact diagnostic

Branch: `codex/astrohd-owner-intake-quality-v1`

Starting HEAD: `78a0d759540dd4906f98efb21477d67ceb9c4cf4`

Ending implementation HEAD: `f72c62c4b7bf9ec92b6e37d4913d5878d7ca40bf`

## Files added

- `state/EXTRA-HIGH-ASTROHD-CORE-FIT-RANK-DISPOSITION-2026-09-02.md`
- `scripts/audit_astrohd_rank_tiebreak_downstream.py`
- `reference/audits/astrohd_rank_tiebreak_downstream_v1.json`
- `tests/unit/test_astrohd_rank_tiebreak_downstream_audit.py`
- `state/ASTROHD-RANK-TIEBREAK-DOWNSTREAM-AUDIT-EXECUTION-RECEIPT-2026-09-02.md`

No pre-existing file was changed by this execution slice.

## Source hashes

The generated audit records the path and SHA-256 of every Python source file
under `src/hdmatch/**/*.py` read by the mechanical scan: `120` files total.

- Canonical compact JSON digest of the 120-row path/hash inventory:
  `c05202788d2007eea9621684e35de616e96f8e266a406d54985777899c3f0ea6`
- `src/hdmatch/participant/backend.py`:
  `80ad02402ec0ea3a094bcd2977e9843c68d296b198bcfc7e836ef71043313198`
- `src/hdmatch/schemas/core.py`:
  `e2c5a866bca25db25002a8bcd5acfc8607e257d8e852f343185f977d23f65c40`
- Generated audit:
  `c9fb9ee6060c4bbb346c7ac6981a543d3d602a60bb1da83e245cea638a680103`

All 120 source hashes regenerate from current source bytes. No source file was
modified.

## Frozen Extra-High disposition recorded

The no-runtime-effect disposition records, without reinterpretation:

- current cross-class `core_fit` behavior must not split confirmatory
  scientific ranks when dependency-controlled evidence fields tie;
- provisional prospective scientific-rank equivalence uses
  `net_rubric_bits`, `meaningful_contradictions`, and `detailed_support`;
- `core_fit` remains descriptive under this disposition;
- no replacement cross-class allocation formula is authorized;
- the present task authorizes no production change.

The supporting diagnostic is
`reference/audits/astrohd_cross_class_core_fit_v1.json` at starting HEAD
`78a0d759540dd4906f98efb21477d67ceb9c4cf4`.

## Current and research-only comparator results

The equal-evidence fixture uses two equal-duration synthetic states. `LOW`
starts before `HIGH`; all score fields except `core_fit` are identical:

- net rubric bits: `1.0`
- evidence rubric bits: `1.0`
- contradiction rubric bits: `0.0`
- meaningful contradictions: `0`
- detailed support: `50.0`
- `LOW.core_fit`: `66.66666666666667`
- `HIGH.core_fit`: `78.57142857142857`

### Current `_rank_states`

- ordered sequence: `HIGH`, `LOW`
- `HIGH` scientific rank: `1.0`
- `LOW` scientific rank: `2.0`

### Research-only `rank_group_without_core_fit`

- ordered sequence: `HIGH`, `LOW`
- `HIGH` scientific rank: `1.5`
- `LOW` scientific rank: `1.5`

This comparator exists only in the audit script. It keeps the current sequence
ordering and excludes `core_fit` only from the scientific equality/midrank key.

### Research-only `rank_order_without_core_fit`

- ordered sequence: `LOW`, `HIGH`
- `HIGH` scientific rank: `1.5`
- `LOW` scientific rank: `1.5`

This comparator exists only in the audit script. It excludes `core_fit` from
both ordering and the scientific equality/midrank key, then uses equal duration
and ascending start time for deterministic display order.

The production `src/hdmatch` tree contains no reference to either research
comparator.

## Non-tie controls

All three comparators order `PREFERRED` ahead of `OTHER` with ranks `1.0` and
`2.0` when each of the following earlier fields differs in turn:

- higher net rubric bits;
- fewer meaningful contradictions after equal net;
- higher detailed support after equal preceding fields.

In every control, `PREFERRED.core_fit` is deliberately `0.0` and
`OTHER.core_fit` is `100.0`. The reversed core-fit values do not override any
of the three preceding fields in any comparator.

## Exact ordered-sequence consumers

The mechanical scan detected exactly seven downstream locations that consume
position/order from a ranked-state sequence:

1. `src/hdmatch/participant/backend.py:199`,
   `AstroHDParticipantBackend.rank`, `iterate_ranked_states`
2. `src/hdmatch/participant/backend.py:220`,
   `AstroHDParticipantBackend.rank`,
   `iterate_ranked_states_and_index_first_rank`
3. `src/hdmatch/participant/backend.py:232`,
   `AstroHDParticipantBackend.rank`,
   `pass_ranked_states_to_top_net_margin`
4. `src/hdmatch/participant/backend.py:287`,
   `AstroHDParticipantBackend.discrimination`,
   `iterate_ranked_and_index_first_rank`
5. `src/hdmatch/participant/backend.py:288`,
   `AstroHDParticipantBackend.discrimination`,
   `pass_ranked_to_top_net_margin`
6. `src/hdmatch/participant/backend.py:544`,
   `AstroHDParticipantBackend._top_net_margin`,
   `index_first_ranked_state`
7. `src/hdmatch/participant/backend.py:545`,
   `AstroHDParticipantBackend._top_net_margin`,
   `iterate_ranked_tail_slice`

The full source-consumer inventory contains `33` mechanically traceable rows
with exact path, line, enclosing function or method, syntactic category, token,
and source excerpt.

## Helper outputs

- Current `_top_net_margin` for equal-net `LOW`/`HIGH`: `0.0`
- Current top-state tie count: `1`
- Research comparator A top-state tie count: `2`
- Research comparator B top-state tie count: `2`
- Current percentiles: `HIGH 100.0`, `LOW 50.0`
- Research comparator A percentiles: `HIGH 75.0`, `LOW 75.0`
- Research comparator B percentiles: `HIGH 75.0`, `LOW 75.0`

No other downstream helper was invoked where doing so would require participant
state or a methodological assumption; its static source occurrence remains in
the inventory instead.

## Verification executed

1. Focused downstream audit tests:

   ```text
   .venv/bin/pytest -q tests/unit/test_astrohd_rank_tiebreak_downstream_audit.py
   ```

   Result: `9 passed`.

2. Combined downstream, cross-class, categorical-coverage, scoring-structure,
   and frozen-mapping audit tests:

   ```text
   .venv/bin/pytest -q tests/unit/test_astrohd_rank_tiebreak_downstream_audit.py tests/unit/test_astrohd_cross_class_core_fit_audit.py tests/unit/test_astrohd_core_categorical_coverage.py tests/unit/test_astrohd_frozen_scoring_structure.py tests/unit/test_astrohd_frozen_mapping_extract.py
   ```

   Result: `39 passed`.

3. Full repository unit suite:

   ```text
   .venv/bin/pytest -q
   ```

   Result: `338 passed, 1 skipped`. The existing environment-dependent skip is
   for unavailable official Swiss Ephemeris files.

4. Strict typing:

   ```text
   .venv/bin/mypy src/hdmatch scripts/audit_astrohd_rank_tiebreak_downstream.py
   ```

   Result: `Success: no issues found in 121 source files`.

5. Ruff and format checks:

   ```text
   .venv/bin/ruff check scripts/audit_astrohd_rank_tiebreak_downstream.py tests/unit/test_astrohd_rank_tiebreak_downstream_audit.py
   .venv/bin/ruff format --check scripts/audit_astrohd_rank_tiebreak_downstream.py tests/unit/test_astrohd_rank_tiebreak_downstream_audit.py
   ```

   Result: `PASS`; both files formatted.

6. Generated JSON validation:

   ```text
   .venv/bin/python -m json.tool reference/audits/astrohd_rank_tiebreak_downstream_v1.json
   ```

   Result: `PASS`.

7. Whitespace/error check:

   ```text
   git diff --check
   ```

   Result: `PASS`.

The tests also establish deterministic source-consumer inventory, byte-identical
JSON regeneration, all 120 current source hashes, research-comparator isolation
from production source, and synthetic-only inputs.

## Scope confirmations

- Codex made no scientific, methodological, interpretive, governance, or
  owner-policy judgment. The disposition text is the supervising Extra-High
  output.
- No production ranking, scoring, dependency collapse, mapping, question,
  questionnaire, owner-session state, candidate matrix, theory-language
  exposure behavior, eligibility, stopping, evidence sufficiency, lock/reveal,
  primary analysis, or deployment behavior changed.
- No hidden owner chart or participant answers were inspected.
- No real participant data was added.
- No merge, rebase, reset, deployment, invitation rotation, participant-session
  creation, participant contact, or spending occurred.

Return the generated audit and this receipt to the verified supervising
Extra-High/Pro reasoning chat. Do not merge or deploy.
