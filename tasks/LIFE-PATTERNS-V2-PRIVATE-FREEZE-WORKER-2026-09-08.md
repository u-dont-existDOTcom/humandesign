# Life Patterns recurrence-corrected v2 private freeze — execution-only worker instructions

Use these instructions for **bounded private execution only**. Methodology and scientific decisions have already been made by the reasoning chat. Do not redesign, reinterpret, resample, or continue to later coding stages.

## Goal

Using the exact recovered private v8/v8.1 source bytes, execute the already-implemented recurrence-corrected v2 preparation on the pinned green implementation head, reproduce the historical pre-label calibration selection **without resampling**, export the new private human-calibration handoff v2, verify it, return the actual private ZIP to the owner, and commit only public-safe receipts/state updates.

## Canonical repository

- repository: `u-dont-existDOTcom/humandesign`
- working branch for public-safe receipts/state: `codex/discover-life-patterns-mvp`
- draft PR: `#24`
- pinned recurrence-v2 implementation head: `7b689f3adb49da599abb40ec2bff27ad97d3887f`
- CI run on that exact head: `34271174611` — success

The private preparation itself must execute against that exact implementation head, even if the branch has later receipt/instruction-only commits.

## Historical v1 chronology that must be replayed exactly for selection

- historical source commit: `5a278d135af4de5190d9b74d8e55489dc92efaf1`
- historical preparation timestamp: `2026-09-06T22:10:58.534703Z`
- historical corpus: `LPDC-F2BBDA6F39040BF41D96`
- historical calibration selection: `LPCA-5B3E6CFCCE49807050DF`
- historical calibration SHA-256: `5b3e6cfcce49807050df03f8ab27cbfbb610869dcb9cfa30064cd485d4646140`
- expected selected units: 44 episode + 22 series

The v2 implementation deliberately reconstructs this historical selection before binding new v2 semantics. **Do not draw a new sample.**

## Exact private input identities

The owner-supplied recovery archive expected for this execution has:

- SHA-256: `7b6e2d4e901093cfd0bf54b6ab8eab66d0cdc28e2feaba720672a38452d8a450`

It contains the two authoritative source byte sequences:

### v8

- bytes: `54488`
- SHA-256: `3c37c0c76174c7ba698966155f991f0303cd4f0833d39ff475dfb0e1c5348637`

### v8.1

- bytes: `25844`
- SHA-256: `93f838bb61e6a910ba0dbeb96a66b56c72986350dda5386243b098a738b818e7`

Verify exact hashes before processing. Do not reconstruct source text from GitHub receipts, summaries, chat history, or memory.

## Hard constraints

- Keep all participant-bearing source, corpus, tasks, packets, forms, and outputs private/gitignored.
- Never stage, force-add, paste, or commit private participant text.
- Do not modify historical v1 artifacts.
- Do not resample the human calibration selection.
- Do not run any human or automated annotation.
- Do not run consensus, human-vs-LLM comparison, target-model scoring/reveal, birth/chart analysis, merge, deploy, recruit/contact, or spend money.
- Do not use target-model information to inspect or judge the recurrence revision.
- Do not ask the owner questions unless exact execution evidence reveals a genuinely nonrecoverable tradeoff. Fail closed instead of improvising.

## Required execution

Use an isolated clean checkout/worktree at exact commit `7b689f3adb49da599abb40ec2bff27ad97d3887f` for the private preparation.

Place verified exact sources under a temporary/private ignored path, for example:

- `experiments/private/life-patterns/v8.json`
- `experiments/private/life-patterns/v8.1.json`

Choose a fresh immutable private output directory. Record the **actual UTC execution timestamp** and use that same timestamp consistently as `--created-at-utc` for the v2 freeze.

Run:

```bash
.venv/bin/python scripts/prepare_life_patterns_development_package_v2.py \
  --v8-record experiments/private/life-patterns/v8.json \
  --v8-1-supplement experiments/private/life-patterns/v8.1.json \
  --output-dir experiments/private/life-patterns/prepared-v2-2026-09-08 \
  --repo-root . \
  --historical-source-commit 5a278d135af4de5190d9b74d8e55489dc92efaf1 \
  --historical-created-at-utc 2026-09-06T22:10:58.534703Z \
  --source-commit 7b689f3adb49da599abb40ec2bff27ad97d3887f \
  --created-at-utc <ACTUAL_UTC_EXECUTION_TIMESTAMP> \
  --render-blind-packets
```

Then export the private human handoff:

```bash
.venv/bin/python scripts/export_life_patterns_human_calibration_bundle_v2.py \
  --prepared-dir experiments/private/life-patterns/prepared-v2-2026-09-08 \
  --output-dir experiments/private/life-patterns/human-calibration-v2-2026-09-08
```

Do not overwrite an existing output directory. If a path already exists, choose a clearly versioned/replay path and preserve the first output.

## Required verification before success

The run must fail closed unless all of the following are true:

1. exact v8/v8.1 file hashes match the identities above;
2. corpus ID/hash and episode/series task sets reproduce the historical private corpus/task universe;
3. calibration manifest is exactly historical `LPCA-5B3E6CFCCE49807050DF` with SHA-256 `5b3e6cfcce49807050df03f8ab27cbfbb610869dcb9cfa30064cd485d4646140`;
4. selected coverage remains exactly 44 episode + 22 series units;
5. no calibration resampling occurred;
6. a new content-addressed recurrence-corrected `LPKG2-*` package exists;
7. package binds coding manual v2, recurrence policy v2, series response schema v2, series prompt v2, human calibration prompt v2, exact 22-observable theory-blind base, and exact 28-value non-action registry;
8. package declares confirming episodes are not frequency counts, target-model information was not used for revision, target scoring unauthorized, development-only, validation-use-forbidden;
9. human packets bind the same frozen v2 package/policy/manual/prompt and reused calibration selection;
10. the private handoff receipt is `LPHB2-*`, selected-unit coverage is verified, blank templates are not annotations, and readiness is `awaiting_human_ui`;
11. handoff contains no automated labels or consensus;
12. public-safe receipts contain no participant narrative.

Read back every handoff member after export and verify its hash against the handoff receipt. Also verify the handoff receipt's own content address.

## Private ZIP delivery

Create a ZIP of the verified private human handoff directory. The outer ZIP is a transport container, so record rather than predict its:

- SHA-256
- byte size
- member count

Return/attach the **actual ZIP bytes to the owner**. A private filesystem path alone is not completion.

## Public-safe execution receipt

After successful private execution, return to the current branch and commit only a public-safe receipt, for example:

`state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`

It should record at minimum:

- exact source archive and source-file hashes/sizes;
- pinned v2 implementation head and successful CI run;
- actual v2 freeze timestamp;
- historical corpus/task identities;
- historical calibration ID/hash and exact 44+22 counts;
- explicit `calibration_selection_reused_without_resampling=true` and `calibration_resampled_after_method_revision=false`;
- new `LPKG2-*` ID/hash;
- v2 ontology/procedure/manual/recurrence-policy/prompt hashes;
- v2 episode/series schema versions;
- new `LPHB2-*` handoff receipt ID/hash and packet hashes/counts;
- private transport ZIP hash/size/member count;
- `contains_private_participant_text=false` for the public receipt itself;
- `human_first_pass_received=false`;
- `automated_coding_run=false`;
- `target_model_scoring_run=false`;
- `development_only=true`, `validation_use_forbidden=true`.

Update `tasks/ACTIVE-TASK.json`, `state/CURRENT-STATE.md`, and `tasks/NEXT-CONVERSATION-HANDOFF-2026-09-07.md` to show that recurrence-v2 method implementation and private freeze/handoff are complete and the next operational prerequisite is the theory-neutral local/offline human calibration UI before the independent human first pass.

## Stop boundary

Stop after:

1. verified private v2 handoff ZIP is attached/delivered to the owner;
2. public-safe receipt/state updates are committed;
3. branch CI on those public-safe changes is reported.

Do **not** implement the UI in this worker, contact an auditor, fill forms, run automated coding, or advance to later scientific stages.
