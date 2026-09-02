# AstroHD PR #23 final convergence v2 execution receipt

Receipt date: 2026-09-02

Task mode: execution-only semantic-contract cleanup and final convergence rerun

Branch: `codex/astrohd-owner-intake-quality-v1`

Starting HEAD: `7338a66210350e8571a52244bb4cdaa753f3c743`

PR base commit: `afc0bb82de0e481ae5a5d3453e0bcaf82b2a0286`

Semantic-correction commit (`CORRECTION_HEAD`):
`b5fd8b6a8c3e59374c1ac33bd518ed59bd81cdd5`

Final-v2 audit implementation and verified pushed head before this receipt:
`c2a5df99004a422665b7936a43c06a32cf0392b9`

The receipt is committed separately after the verified audit boundary, so its
own commit cannot embed its own SHA. The exact final receipt/current pushed
head is recorded in the GitHub branch pointer and the supervising-chat handoff.

## Resolved semantic-contract cleanup

The Extra-High supervisor resolved a naming/schema ambiguity without changing
the owner-pilot quality gate:

| Superseded PR-branch-only field | Resolved field |
| --- | --- |
| `adequately_assessed_question_count` | `adequately_assessed_mapped_question_count` |
| `required_question_count` | `mapped_scoreable_question_count` |
| `complete_profile_required` | `mapped_question_quality_gate_enforced` |

The exact existing files modified by this cleanup were:

- `src/hdmatch/participant/models.py`
- `src/hdmatch/participant/service.py`
- `reference/custom_gpt/participant_action_openapi_v1.yaml`
- `reference/custom_gpt/participant_interviewer_action_openapi_v1.yaml`
- `tests/unit/test_participant_session.py`
- `tests/unit/test_natal_pilot_app.py`

No compatibility aliases were retained for the superseded PR-branch-only
names. A `participant-confirmatory-lock-v1` payload lacking all new receipt
fields remains readable through the model defaults.

The owner-pilot quality gate is semantically unchanged. When enabled, it still
rejects lock if any frozen mapped scoreable question lacks adequate,
consistency-checked evidence. The same test then proves lock succeeds after all
mapped questions have adequate, consistency-checked evidence. The count is
derived from the frozen mapping and is not a questionnaire-completeness
denominator.

## Final convergence v2 artifact

The v2 audit work modified or added:

- `scripts/audit_astrohd_pr23_convergence.py`
- `tests/unit/test_astrohd_pr23_convergence.py`
- `reference/audits/astrohd_pr23_convergence_v2.json` (new)

Audit binding:

- base: `afc0bb82de0e481ae5a5d3453e0bcaf82b2a0286`
- audited head: `b5fd8b6a8c3e59374c1ac33bd518ed59bd81cdd5`
- schema: `astrohd-pr23-convergence-v2`
- v2 SHA-256:
  `e22adb57da174d6485adfc6a3b193d6117609f1b28ddae3654079d49efc41f26`

The preserved v1 mismatch artifact remains byte-identical:

- path: `reference/audits/astrohd_pr23_convergence_v1.json`
- SHA-256:
  `952565c9da16d683711f2bdae1fc8cae974f9c17ce98166a2de00b54d6856e73`

The mechanical PR-delta inventory at `CORRECTION_HEAD` contains `63` changed
paths: `9` under `src`, `11` under `tests`, `7` under `scripts`, `14` under
`reference`, `3` under `docs`, `18` under `state`, and `1` repository-root or
other path. These are descriptive facts only.

## Mechanical convergence results

- production runtime identifiers containing the forbidden completion-policy
  fragments: `0`
- exact `required_question_count` occurrences under `src/hdmatch/**/*.py`: `0`
- exact `complete_profile_required` occurrences under
  `src/hdmatch/**/*.py`: `0`
- exact `required_question_count` occurrences across both active Custom GPT
  OpenAPI schemas: `0`
- both public lock schemas contain
  `adequately_assessed_mapped_question_count` and
  `mapped_scoreable_question_count`
- internal `ConfirmatoryLock` also contains
  `mapped_question_quality_gate_enforced`; this internal boolean was not added
  to the public response
- active owner-correction literal scan: `7` documentary occurrences; this scan
  was not required to be globally zero
- state/history literal scan: `37` occurrences, classified
  `historical_or_state_records_not_runtime_scan`

The v2 audit mechanically reproduces all other directed invariants:

- participant ordering is net descending, contradictions ascending, detailed
  support descending, duration descending, then start ascending
- scientific rank equality uses rounded net, contradictions, and rounded
  detailed support
- date best-state selection uses net, negative contradictions, detailed
  support, and state ID
- `core_fit` has `10` production textual occurrences and `0` occurrences in a
  sort key, max/min key, or scientific rank-equality key
- theory-language code has `0` production importers and `0` production call
  sites outside its isolated evaluation module
- all seven future-core targets retain all four authorization flags as `false`
- mapping SHA-256 remains
  `3424672432f7f071ec90ef9ddce52a67ff6794911e92b1a1e04f079262ea6200`
- question-bank SHA-256 remains
  `31f813efc3da7263569ef010a8336b1b1b0c44801b7aa0f91e33b3fa4587d820`
- the artifact still records `27` frozen rules and `23` distinct mapped
  prompts with `descriptive_only_not_a_completeness_denominator`
- both historical audit hashes remain unchanged and both generators still fail
  closed against changed source
- exact source-commit freeze binding remains present

No mapping, questionnaire prompt, scoring, ranking, dependency, corroboration,
or `core_fit` methodology was changed by the v2 correction.

## Verification

Focused participant-session and natal-pilot API tests:

```text
.venv/bin/python -m pytest -q tests/unit/test_participant_session.py tests/unit/test_natal_pilot_app.py
```

Result: `49 passed, 1 skipped`. The skip is the environment-dependent official
Swiss Ephemeris smoke.

Focused final convergence-v2 tests:

```text
.venv/bin/python -m pytest -q tests/unit/test_astrohd_pr23_convergence.py
```

Result: `15 passed`.

Directed affected suite covering participant sessions, natal-pilot API,
convergence v2, rank semantics, date aggregation, historical audits,
theory-language isolation, categorical coverage, frozen scoring structure,
frozen mapping, and freeze/runtime compatibility:

```text
.venv/bin/python -m pytest -q tests/unit/test_participant_session.py tests/unit/test_natal_pilot_app.py tests/unit/test_astrohd_pr23_convergence.py tests/unit/test_participant_ranking_semantics.py tests/unit/test_date_aggregator.py tests/unit/test_astrohd_cross_class_core_fit_audit.py tests/unit/test_astrohd_rank_tiebreak_downstream_audit.py tests/unit/test_theory_language_exposure.py tests/unit/test_astrohd_core_categorical_coverage.py tests/unit/test_astrohd_frozen_scoring_structure.py tests/unit/test_astrohd_frozen_mapping_extract.py tests/unit/test_freeze_and_manifest.py tests/unit/test_participant_universe_binding.py tests/unit/test_runtime_adapters.py
```

Result: `135 passed, 1 skipped`.

Full local suite:

```text
.venv/bin/python -m pytest -q
```

Result: `357 passed, 1 skipped`. The skip is the same environment-dependent
official Swiss Ephemeris smoke.

Additional local checks:

- `.venv/bin/mypy src/hdmatch scripts/audit_astrohd_pr23_convergence.py`:
  `Success: no issues found in 121 source files`
- Ruff on all touched Python: `PASS`
- Ruff format check on all touched Python: `PASS`
- YAML parse of both active Custom GPT OpenAPI files: `PASS`
- JSON parse of convergence v1 and v2: `PASS`
- byte-identical v2 regeneration: `PASS`
- v1 SHA preservation: `PASS`
- `git diff --check`: `PASS`

Exact-head hosted verification for
`c2a5df99004a422665b7936a43c06a32cf0392b9`:

- push run `33690590295`: `SUCCESS`
- pull-request run `33690593803`: `SUCCESS`
- hosted test result: `352 passed, 6 skipped`
- hosted lint: `PASS`
- hosted mypy: `Success: no issues found in 120 source files`

Hosted-only skip behavior is limited to three v2 audit reproduction tests whose
bound Git objects are absent from the shallow checkout, plus three existing
official Swiss Ephemeris smoke tests. The v2 content assertions, runtime-symbol
zero assertion, and lock-contract assertions all execute in hosted CI and pass.

Verification-efficiency telemetry recorded four nonredundant runs: two focused,
one affected, and one full. No mutation-test trigger applied and no forced
redundant green rerun occurred.

## Scope and authority confirmations

- No participant session or invitation was created, replaced, or rotated.
- No participant was contacted.
- No participant data or real theory-language vocabulary was added.
- No questionnaire prompt was added, removed, or changed.
- No mapping, scoring, ranking, evidence-sufficiency, lock/reveal sequencing, or
  deployment behavior was changed; only the resolved lock-receipt names changed.
- No PR-body or ready-for-review metadata was changed.
- No merge or deployment occurred.
- No money was spent.
- Codex made no scientific, methodological, governance, interpretive, or owner-
  policy decision.
