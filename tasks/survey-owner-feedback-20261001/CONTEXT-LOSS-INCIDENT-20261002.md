# Custom GPT context-loss incident — 2026-10-02

## Observed failure

After the owner updated the Custom GPT during an in-progress test, the next recovery candidate contained zero behavioral turns and marked consent as unrecovered. That candidate describes only the post-update chat context; it is not evidence that earlier answers never existed.

The owner had already completed a separate historical 79-answer scenario interview. That source remains privately recovered and must not be replaced by an empty candidate. Two exact Q&A pairs from the newer test are also preserved privately from the owner-provided screenshot; other missing newer turns were not reconstructed.

## Product boundary

OpenAI currently documents that Custom GPTs do not use previous conversations and each conversation starts fresh. On web, bringing a GPT into an existing conversation with @ preserves that conversation's current context. Sidebar search can search saved/archived chat message text. The editor Preview is a test surface; project workflow must not treat Preview or a newly opened chat as durable participant storage.

## Repair

- Owner/substantive tests use a normal saved GPT conversation, not Builder Preview.
- Before clicking Update during an in-progress interview, create and verify `life-patterns-live-recovery-checkpoint.json`.
- The checkpoint uses the canonical recovery schema, preserves exact source Q&A only, is explicitly UNFROZEN, and requires consent reconfirmation after context loss.
- After context loss, an empty candidate is diagnostic only. Recovery must come from the same saved conversation, explicit attachment, or explicit canonical Library fallback.
- Missing later turns remain missing; no reconstruction from Memory, summaries, likely route content or model inference.

## Scope

This is context-resilience and owner-testing workflow repair. It does not alter frozen v7 questions, the hybrid question trial, Railway review semantics, consent requirements, CF-003 ordering, or provider/inference settings.
