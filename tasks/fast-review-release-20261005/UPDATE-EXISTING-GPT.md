# Update your existing Life Patterns GPT

Version: 2026-10-05.1-fast-review-stages

This is an UPDATE packet, not a new GPT and not a request to repeat the interview.

Before updating during an interview, ask the GPT to create its source-only live recovery checkpoint and verify its answer count. Keep the existing saved conversation and private review receipt.

## Three replacements in Edit GPT / Configure

1. Replace Instructions with the contents of INSTRUCTIONS-life-patterns-voice-interviewer-v2.md.
2. In Knowledge, remove the previous ACTION-HANDOFF-GUIDE-v1.md and upload knowledge/ACTION-HANDOFF-GUIDE-v1.md from this packet. Keep the other five Knowledge files unchanged.
3. Edit the EXISTING Action and import ACTION-life-patterns-submission-openapi.yaml (or reimport the existing schema URL). Keep its existing Bearer API credential. Do not create a duplicate Action or paste any secret into chat.

Keep Code Interpreter & Data Analysis enabled, then select Update to apply the changes. GPT-BUILDER-CONFIG.md is owner setup documentation, not a Knowledge file.

## What participants will see

New interviews use the reviewed fast first-question path. Independently useful questions arrive in a small batch but are asked one at a time in the chat. Their exact answers/skips go back in one Action. A changed premise can trigger early reconciliation instead of asking a now-invalid question.

Every waiting response must state the actual server stage, its estimated range and when to check back. The first clarification path has a roughly 1–3 minute pilot estimate. Reconciliation is provisionally 1–4 minutes. A broader omission check is provisionally 2–8 minutes. Full evidence preparation is provisionally 5–12 minutes (check after about 10), followed by an independent check provisionally 1–3 minutes. The service supplies more specific intervals for gap admission and wording review.

These are limited-pilot estimates from the start of a stage, not guaranteed total turnaround. Queue time is unknown. If the worker is offline or a stage runs long, the GPT reports that honestly instead of repeatedly promising completion. A blocked/error state needs repair, not more waiting.

Participants may leave and later send any message in the SAME saved conversation to check the same review. This workflow does not send automatic notifications. Existing queued reviews retain the legacy protocol so an update does not restart or duplicate their records.

## Short Preview check (no real participant data)

Verify the opening explains research consent, Railway approvals, and pause/skip/stop. Do not run a long real interview in Builder Preview. Use a normal saved GPT conversation for substantive records. Check that waiting guidance includes a stage, range, and check-back interval, and that the approval sentence occurs once per Action: “Please click Allow on this tool call to continue.”

## Unchanged boundaries

All participant-data/state-changing Actions still require normal consequential approval; the status GET remains read-only. No fixed lifetime clarification cap. No birth/chart data during the interview. Final primary freeze and CF-003 happen only after the independent full review is ready and the participant confirms it. A first question batch is not a completed final review.

The exact frozen behavioral instrument and other five Knowledge files are unchanged. The archive contains no participant records or credentials.
