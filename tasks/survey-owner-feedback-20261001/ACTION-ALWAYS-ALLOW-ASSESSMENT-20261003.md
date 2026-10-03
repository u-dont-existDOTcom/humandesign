# Action approval / “Always allow” assessment — 2026-10-03

## Owner observation

The owner sometimes sees an **Always allow** option instead of only **Allow once** and asked whether that could make incremental Railway submission practical.

## Current platform evidence

Current OpenAI Help Center documentation for connected apps says approval controls may include:

- Allow / Allow once for the current action;
- Allow low-risk actions for future low-risk actions;
- Always allow for eligible explicitly connected personal accounts, allowing supported future actions without repeated prompts.

It also states that availability depends on the action/account and that some sensitive actions still require approval or may be denied.

Current GPT Actions help documentation confirms that users may be asked to approve custom Actions, but the currently surfaced Help Center page no longer documents the older `x-openai-isConsequential` behavior in detail.

Historical OpenAI Actions documentation, preserved in OpenAI Developer Community quotations, stated:

- `x-openai-isConsequential: true` => always prompt; no Always allow button;
- `x-openai-isConsequential: false` => show Always allow;
- absent flag => GET defaults false, non-GET defaults true.

Because that exact rule is not present in the current official Help Center page, treat it as a **private experiment to re-verify**, not a production guarantee.

## Current Life Patterns schema

- `startLifePatternsReview` POST: explicitly consequential = true.
- `submitLifePatternsClarification` POST: explicitly consequential = true.
- `controlLifePatternsReview` POST: explicitly consequential = true.
- `submitLifePatternsRecords` POST: explicitly consequential = true.
- `getLifePatternsReview` GET: no explicit flag, so it is the natural low-risk/read-only candidate for persistent approval behavior if the legacy/default semantics still apply.

This explains why the owner can plausibly see different approval choices on different calls: the schema and action risk are different.

## Product decision

Do **not** globally relabel the existing participant-data writes as nonconsequential just to remove prompts. They transmit or mutate research records and some controls (withdraw/stop/retry) have real state effects.

Instead:

1. Keep the one-time full-candidate start and final reviewed submission explicitly consequential.
2. Keep participant clarification answer submission consequential in the current GPT until a private test establishes both consent UX and platform behavior.
3. Treat the read-only status check as the first place to exploit persistent/low-risk approval when the UI offers it.
4. For a future incremental-ingestion experiment, create a **separate narrow append/checkpoint operation** whose semantics are append-only, idempotent, encrypted, revocable by withdrawal, and incapable of publication/freeze/final submission. Only then test `x-openai-isConsequential: false` in a private GPT and verify that the UI actually offers Always allow before relying on it.
5. For the plugin, prefer the current app-permissions system. Eligible users can explicitly choose Always allow or Allow low-risk actions for a connected app; this is a stronger long-term fit for background/batched ingestion than repeated Custom GPT Action cards.

## Why this matters for the streaming idea

If a private append operation can legitimately obtain persistent permission, the owner's incremental design becomes much more attractive for the Custom GPT: one explicit permission decision could support batched source checkpoints during the interview rather than a new Allow card for every batch.

If persistent permission is unavailable, keep Custom GPT ingestion end-only or at most one checkpoint. Do not make participants click dozens of approvals.

## Verification requirement

Before changing production:

- add a harmless/private checkpoint endpoint on an experimental schema;
- mark only that operation nonconsequential;
- verify the actual ChatGPT UI on the owner's account shows Always allow;
- verify subsequent same-operation calls do not ask again;
- verify a fresh participant/account does not inherit someone else's permission;
- verify withdraw invalidates/deletes provisional checkpoint material as designed;
- keep final review/freeze/submission actions consequential.
