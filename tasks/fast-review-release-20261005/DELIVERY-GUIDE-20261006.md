# Update your existing Life Patterns GPT

Version: **2026-10-05.1-fast-review-stages**
Release deployed and read back on October 6, 2026.

## Files already delivered to your computer

The archive and extracted folder are already in your Downloads directory:

`/mnt/hdd/home/joel/Téléchargements/Life-Patterns-GPT-fast-review-update-2026-10-05.zip`

`/mnt/hdd/home/joel/Téléchargements/Life-Patterns-GPT-fast-review-update-2026-10-05/`

Archive SHA-256: `810ecf7f4b937eef72db5572399a07cba40d82dec3d5afdff92aac5ef231c7a9`.

This is an update to the existing GPT, not a new GPT or a request to repeat the interview. The archive, its manifest, and its extracted files have been checked. No participant records or credentials are included.

## Before updating during an active interview

Ask the GPT to create its source-only live recovery checkpoint and verify the answer count. Keep the existing saved conversation and private review receipt. Do not create a second review simply to obtain the speedup.

## Three replacements in Edit GPT / Configure

| Location | Replacement |
|---|---|
| Instructions | Replace the existing text with the contents of `INSTRUCTIONS-life-patterns-voice-interviewer-v2.md`. |
| Knowledge | Remove the old `ACTION-HANDOFF-GUIDE-v1.md`, then upload `knowledge/ACTION-HANDOFF-GUIDE-v1.md` from the extracted update folder. Keep the other five Knowledge files unchanged. |
| Existing Action | Import `ACTION-life-patterns-submission-openapi.yaml`, or reimport the existing schema URL. Keep the existing Bearer API credential. Do not create a duplicate Action. |

Keep **Code Interpreter & Data Analysis** enabled, then select **Update**. `GPT-BUILDER-CONFIG.md` is setup documentation, not a Knowledge file. Do not paste credentials into chat.

## Participant timing guidance

| Current review stage | Planning duration from stage start | Initial check-back target |
|---|---:|---:|
| Checking for useful clarifications | 1–3 minutes | About 3 minutes |
| Independently checking proposed clarifications | 15–90 seconds | About 1 minute |
| Preparing and checking question wording | 15–90 seconds | About 1 minute |
| Rechecking clarification answers | Provisionally 1–4 minutes | About 3 minutes |
| Checking for overlooked or conflicting answers | Provisionally 2–8 minutes | About 5 minutes |
| Preparing the full evidence review | Provisionally 5–12 minutes | About 10 minutes |
| Independently checking the evidence review | Provisionally 1–3 minutes | About 3 minutes |

The server provides the actual stage, elapsed time, estimate basis, and adjusted check-back interval. These are limited-pilot planning estimates, not guaranteed deadlines or calibrated service-level percentiles. They are not a fixed end-to-end total to add mechanically. Some stages may recur after new answers or retries. Queue time is excluded and unknown.

The pilot reviewer requires the researcher's computer online. A stale heartbeat removes the numeric remaining-time estimate. An overrun is reported honestly with another check-back interval. Paused and error states are not presented as active progress.

Participants return to the **same saved conversation** and send a message to check the same review. This workflow does not send automatic notifications.

## Review flow

Independently useful clarifications arrive in a small batch. The GPT asks them one at a time locally, then sends exact answers or explicit skips in one Action. There is no remote review wait between independent questions already in that batch. A changed premise can trigger early reconciliation rather than asking a now-invalid remainder.

A first clarification batch is not a completed final review. The full omission check, evidence synthesis, and independent evidence admission still run before final-ready. There is no fixed lifetime clarification cap.

Existing review jobs retain their legacy protocol; this update does not restart or duplicate their records. New review requests can use the fast protocol. No re-interview is required merely because the GPT was updated.

All participant-data and state-changing Actions remain consequential. The status GET remains read-only; availability of persistent permission depends on the ChatGPT interface. The approval sentence is: “Please click Allow on this tool call to continue.” It should occur once per Action, not twice.

## Verified release evidence

The recorded release passed 170 participant tests and 1,013 repository tests, with six astronomy-data-dependent tests skipped. A complete synthetic 79-turn live test observed a two-question batch after 81.05 seconds and final-ready after 428.18 seconds, including polling. It exercised batch submission, explicit skips, reconciliation, omission checking, evidence synthesis, and independent admission. The synthetic record was withdrawn; no research submission or participant freeze was performed.

A subsequent read-only verification confirmed the public API advertises `fast-batch-v1`, the live Action schema matches the delivered package, and all 22 installed worker files match the tested release. No paid API inference was enabled.

The backend and package are deployed. The GPT editor itself has not been changed; applying the three replacements and selecting Update is the remaining installation step.

## Provenance

Canonical repository: `u-dont-existDOTcom/humandesign`.
Integration commit: `c06713febb1de31b51e8241469e9271a92a66b14`.
Runtime source commit: `499ee11611a929b8653f8f326d324f26ae482336`.
Release report: `tasks/fast-review-release-20261005/RELEASE-RESULT-20261006.md`.
Current readback: `tasks/fast-review-release-20261005/DELIVERY-READBACK-20261006-0127.json` on `audit/fast-review-delivery-20261006-0127`.
