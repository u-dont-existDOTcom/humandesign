# Update your existing Life Patterns GPT

Version: 2026-10-05.1-fast-review-stages

This is an UPDATE packet, not a new GPT and not a request to repeat the interview.

The archive and an extracted folder are already in your Downloads directory:

- `Life-Patterns-GPT-fast-review-update-2026-10-05.zip`
- `Life-Patterns-GPT-fast-review-update-2026-10-05/`

Before updating during an interview, ask the GPT to create its source-only live recovery checkpoint and verify its answer count. Keep the existing saved conversation and private review receipt.

## Three replacements in Edit GPT / Configure

1. Replace Instructions with the contents of `INSTRUCTIONS-life-patterns-voice-interviewer-v2.md`.
2. In Knowledge, remove the previous `ACTION-HANDOFF-GUIDE-v1.md` and upload `knowledge/ACTION-HANDOFF-GUIDE-v1.md` from this packet. Keep the other five Knowledge files unchanged.
3. Edit the EXISTING Action and import `ACTION-life-patterns-submission-openapi.yaml` (or reimport the existing schema URL). Keep its existing Bearer API credential. Do not create a duplicate Action or paste any secret into chat.

Keep Code Interpreter & Data Analysis enabled, then select **Update** to apply the changes. `GPT-BUILDER-CONFIG.md` is owner setup documentation, not a Knowledge file.

## Review stages and check-back guidance

| Stage | Estimated duration from stage start | Initial check-back guidance |
|---|---:|---:|
| Initial clarification selection | 1–3 minutes | About 3 minutes |
| Independent clarification admission | 15–90 seconds | About 1 minute |
| Question wording and checking | 15–90 seconds | About 1 minute |
| Reconciliation after clarification answers | Provisionally 1–4 minutes | About 3 minutes |
| Omission/contradiction audit, when required | Provisionally 2–8 minutes | About 5 minutes |
| Full evidence preparation | Provisionally 5–12 minutes | About 10 minutes |
| Independent evidence check | Provisionally 1–3 minutes | About 3 minutes |

The server adjusts the check-back interval using the actual stage and elapsed time. These are limited-pilot planning estimates, not deadlines or measured service-level guarantees. Initial clarification selection and its admission/wording substages are not independent totals to add mechanically. Queue time is excluded and is not predictable. The local pilot reviewer needs the researcher's computer online.

Every waiting response must state the actual server stage, its estimated range and when to check back. If the worker is offline or a stage runs long, the GPT must report that honestly instead of promising completion. A blocked/error state needs repair, not more waiting.

Independently useful questions arrive in a small batch but are asked one at a time in the chat. Their exact answers/skips go back in one Action. A changed premise can trigger early reconciliation instead of asking a now-invalid question. There is no review wait between independent questions already in the batch.

Participants may leave and later send any message in the **same saved conversation** to check the same review. This workflow does not send automatic notifications. Existing queued reviews retain their legacy protocol so an update does not restart or duplicate their records. New review requests can use the fast protocol after the GPT update; no re-interview is required merely to obtain it.

## Unchanged boundaries

All participant-data/state-changing Actions retain normal consequential approval. The status GET remains read-only; persistent permission still depends on the ChatGPT interface. The approval sentence is: “Please click Allow on this tool call to continue.” It should occur once per Action, not twice.

There is no fixed lifetime clarification cap. No birth/chart data enters the interview. Final primary freeze and CF-003 happen only after the independent full review is ready and the participant confirms it. A first clarification batch is not a completed final review.

The frozen behavioral instrument and other five Knowledge files are unchanged. The archive contains no participant records or credentials.
