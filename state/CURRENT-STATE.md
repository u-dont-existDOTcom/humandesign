# Current state

## Authoritative branch overlay — Life Patterns recurrence-v2 human calibration — 2026-09-08

This file is the concise current-state overlay for branch
`codex/discover-life-patterns-mvp`, draft PR #24. Historical branch state remains
preserved in Git history and the dated `state/` artifacts; do not infer a current
next action from superseded sections in older commits.

Before substantive continuation, fetch the live PR #24 head and read
`tasks/NEXT-CONVERSATION-HANDOFF-2026-09-07.md` and `tasks/ACTIVE-TASK.json`.

### Scientific/method state

- The owner-identified recurrence-evidence defect was caught **before any human or
  automated Life Patterns annotation pass existed**.
- The corrected additive theory-blind v2 method is implemented at pinned substantive
  head `7b689f3adb49da599abb40ec2bff27ad97d3887f`; hosted CI `34271174611` succeeded.
- Governing recurrence rule: generalized behavioral self-report is direct evidence of
  **reported recurrence**. A concrete example selected after that claim is not an
  independent frequency observation and is not counted as additive frequency support.
  Recurrence strength, exception status/frequency and evidence basis remain separate.
- Historical v1 codebook/package artifacts remain unchanged and reproducible; v2 reuses
  the same theory-blind behavioral base and exact 28-value non-action registry while
  binding the recurrence-corrected manual/policy/response contract.
- No Human Design mapping, chart/birth data, target-model result, automated label or
  expected answer was used to make the recurrence revision.

Primary v2 method artifacts:

- `state/LIFE-PATTERNS-RECURRENCE-EVIDENCE-CORRECTION-2026-09-08.md`
- `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_PRIOR_WORK_SCAN_2026-09-08.md`
- `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
- `state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md`

### Exact private v2 freeze/handoff

The exact recovered v8/v8.1 sources were used in a bounded private execution. The
owner then reuploaded the recurrence-corrected private human handoff to the continuation,
and it was independently reverified before UI work.

- source v8: 54,488 bytes; SHA-256
  `3c37c0c76174c7ba698966155f991f0303cd4f0833d39ff475dfb0e1c5348637`
- source v8.1: 25,844 bytes; SHA-256
  `93f838bb61e6a910ba0dbeb96a66b56c72986350dda5386243b098a738b818e7`
- corpus: `LPDC-F2BBDA6F39040BF41D96`; SHA-256
  `f2bbda6f39040bf41d9612fec322497c8e3fb30d49df913d0c06f0cd26f19172`
- reused historical calibration: `LPCA-5B3E6CFCCE49807050DF`; SHA-256
  `5b3e6cfcce49807050df03f8ab27cbfbb610869dcb9cfa30064cd485d4646140`
- selected human units: **44 episode + 22 repeated-series = 66**, reused without
  resampling after the method revision.
- recurrence-v2 package: `LPKG2-F93D8245B78CD9FDCF5D`; SHA-256
  `f93d8245b78cd9fdcf5dd96f1cc321171f628015ca155b8fae0df4fcb826313a`
- private human handoff: `LPHB2-F34245FAE32B513DDCFE`; SHA-256
  `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- owner-reuploaded transport ZIP: 422,297 bytes, 15 members; SHA-256
  `f038237a6a1ce776bb28846b76ff49339e7a9e7f28d33c5d1ad877e0d916d837`.

All receipt-declared member hashes, all eight LPBP2 packet content addresses and exact
44+22 blank selected-unit coverage were reverified. No participant narrative or private
handoff bytes were committed.

Public-safe verification:
`state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`.

### Offline human calibration UI

A standalone theory-neutral local/offline UI now exists for the exact v2 handoff.
Committed implementation:

- `scripts/build_life_patterns_human_calibration_ui_v2.py`
- `scripts/life_patterns_human_calibration_ui_v2_template.zlib.b64`
- `tests/unit/test_life_patterns_human_calibration_ui_v2.py`
- `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_UI_V2_2026-09-08.md`

Implementation/test-bearing head `aba22fe18f65dcf7cb3f67b494b9cc343b0c752e` passed hosted CI
`34290496491`: **605 passed, 7 expected skips**, Ruff passed, strict mypy passed
for 171 source files.

Exact private generated UI:

- `Life-Patterns-Human-Calibration-V2-OFFLINE.html`
- 3,980,290 bytes
- SHA-256 `63baa191a93c49cbdfb459d4d5e3f96ff541bdddc3dd2183e5af743f48ce987b`.

The generated HTML embeds private participant evidence and is deliberately not in Git.
It is standalone, uses no AI/server/network dependency, re-verifies the embedded handoff
before showing evidence, prevents invalid response combinations, supports receipt-bound
progress save/reload, and exports exactly:

- `episode_responses.completed.jsonl`
- `series_responses.completed.jsonl`
- `auditor_attestation.completed.json`.

Engineering/static verification includes deterministic regeneration, Node JavaScript syntax,
no-network API/static scan and synthetic tamper/fail-closed tests.

**Outstanding UI verification:** a genuine normal-browser visual/interaction smoke pass has
not been completed. The continuation container's Chromium runtime hung even on an empty page,
so this check is explicitly unverified rather than inferred from tests. Public-safe receipt:
`state/LIFE-PATTERNS-HUMAN-CALIBRATION-UI-V2-VERIFIED-2026-09-08.json`.

### Current gate / exact next action

Blocked at human-calibration step 5 pending:

1. open the exact private standalone HTML in a normal local browser;
2. verify the integrity-success screen/first unit renders;
3. navigate units, save one valid response, export and reload progress, confirm the saved
   response returns, and verify final attestation/export controls are present;
4. confirm no external network requests occur;
5. if the smoke pass succeeds, give the same private UI to an **independent theory-blind
   human auditor** who is not the participant/theory-exposed owner;
6. freeze the complete 44 episode + 22 series first pass and v2 attestation before the
   auditor sees any automated output.

The owner may later provide separately identified sensitivity coding, but it cannot be treated
as the independent blind benchmark.

### Still absent / forbidden

- independent human first-pass labels: **absent**
- completed human blinding/independence attestation: **absent**
- automated Life Patterns passes: **not run**
- automated consensus: **absent**
- human-vs-automated comparison: **absent**
- validation-route promotion: **not made**
- target-model scoring/reveal: **not run / unauthorized**
- merge/deploy: **not authorized**
- participant/auditor recruitment or contact: **not authorized**
- spending: **not authorized**

`development_only=true`; `validation_use_forbidden=true`.

Only after the independent human first pass is frozen may the >=3 isolated automated
development passes begin. Consensus and human-vs-automated comparison come after those passes;
target-model comparison remains a later separately authorized/frozen stage.
