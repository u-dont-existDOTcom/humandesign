# Life Patterns exact human-handoff regeneration — execution worker

Use this only in an execution environment with a checkout of `u-dont-existDOTcom/humandesign` and access to the owner-supplied private recovery ZIP. This is a bounded recovery/transport task, not a coding or model-scoring task.

## Canonical bootstrap

1. Fetch current draft PR #24 head on branch `codex/discover-life-patterns-mvp`.
2. Read `tasks/NEXT-CONVERSATION-HANDOFF-2026-09-07.md` and follow its current read order.
3. Confirm `tasks/ACTIVE-TASK.json` still identifies `life-patterns-development-transfer-v1` and still blocks automated coding before the independent human first pass.
4. Do not trust filenames or this dated worker note over newer GitHub-canonical state.

## Private input

Acquire the owner-supplied private recovery archive. The archive name may vary. Do not commit, paste, log, or upload its narrative-bearing contents to GitHub.

The replay helper itself must find and verify both exact byte sequences:

- v8: 54,488 bytes; SHA-256 `3c37c0c76174c7ba698966155f991f0303cd4f0833d39ff475dfb0e1c5348637`
- v8.1: 25,844 bytes; SHA-256 `93f838bb61e6a910ba0dbeb96a66b56c72986350dda5386243b098a738b818e7`

If either exact source is absent or duplicated, fail closed. Do not reconstruct anything.

## Execute exactly one deterministic regeneration

From the current repository checkout, run the helper with the project virtual environment, for example:

```bash
.venv/bin/python scripts/regenerate_life_patterns_human_calibration_from_recovery.py \
  --source-archive /PRIVATE/PATH/Life-Patterns-v8-v8.1-EXACT-SOURCES-VERIFIED-2026-09-07.zip \
  --output-zip /PRIVATE/PATH/Life-Patterns-HUMAN-CALIBRATION-REGENERATED-2026-09-07.zip
```

The helper is required to replay the original preparation using:

- original preparation source binding `5a278d135af4de5190d9b74d8e55489dc92efaf1`;
- original preparation timestamp `2026-09-06T22:10:58.534703Z`;
- existing frozen preparation/export code;
- no model calls and no annotations.

It then must fail closed unless the regenerated package is exactly:

- package `LPKG-18170B8D3EEC8423A523` / `18170b8d3eec8423a523cc2151020a2e2dfead8abf3a9ea5b941fdc9194dd66f`;
- calibration `LPCA-5B3E6CFCCE49807050DF` / `5b3e6cfcce49807050df03f8ab27cbfbb610869dcb9cfa30064cd485d4646140`;
- 44 episode units + 22 exact-source series units;
- all frozen human packet/form/schema/README bytes matching the committed `human_handoff_public_safe_receipt.json` hashes;
- regenerated handoff receipt byte-identical to the committed receipt;
- exactly 15 files including that receipt.

The newly created outer ZIP is a new deterministic transport container. Its outer ZIP hash need not equal the lost historical ZIP hash `a5cba3a3…c83b4`; scientific identity is established by the exact frozen internal bytes and committed handoff receipt. Report the new outer ZIP hash/size/member count separately and do not relabel it as the original archive.

## Required output to owner

Return the actual regenerated ZIP as a user-accessible file attachment/download, not merely a filesystem path.

Also return a concise public-safe receipt containing only:

- source archive SHA-256;
- exact v8/v8.1 hashes;
- frozen package/calibration IDs and hashes;
- frozen human-handoff receipt ID/hash;
- `44 + 22` unit counts;
- `15` member count;
- new transport ZIP SHA-256 and byte size;
- `handoff_internal_files_match_committed_hashes=true`;
- `human_first_pass_received=false`;
- `automated_coding_run=false`;
- `development_only=true`;
- `validation_use_forbidden=true`.

Do not include participant text, private filesystem paths, packet contents, or blank-form rows in a committed receipt.

## GitHub closure

After successful regeneration only:

1. commit a public-safe regeneration receipt under `state/`;
2. update `tasks/ACTIVE-TASK.json` so the recovery/regeneration portion of step 5 is closed and the sole scientific blocker is the independent blind human first pass plus actual exposure/independence attestation;
3. update `tasks/NEXT-CONVERSATION-HANDOFF-2026-09-07.md` and the top Life Patterns section of `state/CURRENT-STATE.md` consistently;
4. run the relevant tests/Ruff/mypy/preflight required by current repo authority and verify hosted CI on the final exact head.

Do **not** commit the regenerated private handoff, source archive, private prepared directory, human responses, or participant narrative.

## Stop boundary

Stop after returning the private auditor ZIP and committing only public-safe recovery state. Do not contact/recruit an auditor, fill any blank response, run an automated coder, expose automated labels, build consensus, compare labels, revise the measurement stack, select a validation route, run target-model scoring/reveal, merge, or deploy unless separately authorized.
