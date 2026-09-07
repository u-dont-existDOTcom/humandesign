# Life Patterns private artifact recovery — 2026-09-07

Status: continuity/recovery record only. This does not alter the frozen v8/v8.1 measurement chain, human calibration selection, coding prompts, codebook, task sets, or scientific gates.

## Problem

The prior execution created a private human-calibration archive and processed the exact private v8/v8.1 source JSONs in a gitignored workspace, while committing only public-safe receipts. In the fresh continuation chat/runtime, those private bytes are not available.

The prior public receipts remain authoritative for identity/integrity:

- v8 exact file bytes: 54,488
- v8 exact file SHA-256: `3c37c0c76174c7ba698966155f991f0303cd4f0833d39ff475dfb0e1c5348637`
- v8.1 exact file bytes: 25,844
- v8.1 exact file SHA-256: `93f838bb61e6a910ba0dbeb96a66b56c72986350dda5386243b098a738b818e7`
- human calibration archive bytes: 379,729
- human calibration archive SHA-256: `a5cba3a33f3103ff9e16f4cff6b82a090e8380b837a21852167c47a0a99c83b4`
- human calibration archive members: 15
- human calibration units: 44 episode + 22 exact-source series

The canonical prior private path was recorded as:

`experiments/private/life-patterns/human-calibration-2026-09-06.zip`

That path described the prior worker/private workspace. It is not evidence that a fresh chat runtime or the owner's current device still has the file.

## Recovery checks performed in the fresh continuation

The fresh continuation checked:

1. the current GitHub handoff/state/receipts;
2. prior-conversation context for the latest Humandesign/Life Patterns handoff;
3. ChatGPT File Library using the exact archive/source names, schema identifiers and hashes;
4. recent File Library uploads around 2026-09-05 through 2026-09-07;
5. connected Google Drive using the exact archive name and source schema identifier;
6. the fresh runtime sandbox.

No exact private source JSON or human-calibration archive was recovered from those surfaces. The File Library contains the recent Humandesign reasoning-instruction file, but no located artifact matched the exact private source schemas/hashes or archive identity. Google Drive likewise returned no exact match. The fresh runtime sandbox contains only artifacts created in the current conversation, not the prior private Life Patterns workspace.

## Scientific consequence

Do not reconstruct the v8/v8.1 source JSONs from handoff prose, summaries, remembered conversation fragments, or public-safe receipts. Such a reconstruction would not be byte-identical to the frozen source and would invalidate the existing content-addressed development package/calibration chronology.

Do not fabricate the auditor bundle from public packet receipts. The committed packet receipts intentionally omit participant narrative and therefore cannot recreate the private human packets.

The existing v8/v8.1 development execution can continue only after recovering either:

1. the exact human calibration archive matching SHA-256 `a5cba3a33f3103ff9e16f4cff6b82a090e8380b837a21852167c47a0a99c83b4`; or
2. both exact source files matching the v8/v8.1 SHA-256 values above, from which the already-documented deterministic preparation/export can be replayed and verified.

If neither exact source nor exact archive can be recovered, the existing v8/v8.1 execution remains blocked. Any new source collection would constitute a new development corpus/version rather than a continuation of the frozen package `LPKG-18170B8D3EEC8423A523`.

## Handoff lesson

A public-safe hash receipt is necessary for integrity but insufficient for cross-conversation continuity of deliberately private artifacts. Future private execution handoffs should leave the owner with a user-accessible private export or explicitly verified durable private storage location, while still keeping participant narrative out of Git.
