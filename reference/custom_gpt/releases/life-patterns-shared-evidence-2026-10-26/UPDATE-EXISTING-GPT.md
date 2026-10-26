# Update the existing Life Patterns GPT — 26 October 2026

This package updates the same GPT using the installed instructions supplied by the owner on October 26. That supplied text already includes fast-batch review, completed-interview reuse, source accuracy and source-preserving submission. It is not treated as wholly outdated.

## Install

1. If an interview is open, first have the existing GPT create its unfrozen recovery checkpoint and real downloadable backup. Updating configuration is not research storage; preserve an active interview before leaving it.
2. Open the existing GPT's editor. Replace the whole Instructions field with **INSTRUCTIONS-life-patterns-2026-10-26.txt**. Do not append it to the old instructions. The checked text fits the strict 8,000-character limit, including CRLF line endings.
3. In Knowledge, replace **TENDENCY-FIRST-GUIDE-v1.json** with the version in this package, and add **SHARED-EVIDENCE-CAPTURE-GUIDE-v1.md**. The tendency-first change affects only when a question-purpose explanation is shown; its question objects are unchanged.
4. Make sure the other nine Knowledge files match the included complete set. In particular, include both **EXPERIENCE-MEANING-OPTIONAL-v2.md** and **experience-meaning-v2.json** if absent. There are **eleven Knowledge files in total**. Replace same-name obsolete versions rather than retaining contradictory duplicates. Upload the files inside `knowledge/`, not this ZIP itself, the manifest, this installation note or any participant record.
5. The existing Action must use version **1.9.0**. If it already matches **ACTION-life-patterns-submission-openapi.yaml**, leave it as is; otherwise replace its schema with the included file. Keep the existing Action URL and private bearer authentication. The live public schema was retrieved on October 26 and matched the included schema byte for byte. A Railway CLI login does not replace the GPT Action credential.
6. Save/update the existing GPT. This file package has not edited the private GPT for you. Keep all real interviews in saved conversations, not Builder Preview.

## What changes for participants

- Event accounts retain their actual date/age/range wording, uncertainty, context and coverage. No exact date, total or absent event is invented from incomplete answers.
- An adequate earlier answer remains adequate; no new required event history or repeated main interview is introduced.
- The purpose explanation appears only when a scenario, example or follow-up needs clarification, matching the owner's installed instructions.
- Once a consented review has actually been saved, the participant can choose private Railway continuation while it is still queued or processing. Independent `ready` remains necessary for final confirmation and storage. GPT and Railway must not run duplicate interviews/submissions.
- If finishing in GPT, the existing optional, separately consented Experience & Meaning v2 section is offered after CF003. Declining it adds no record and no extra submission call. Railway handles that section when the participant has transferred there.

## Preserved research boundaries

The current tendency-first question objects, legacy question bank, exact three CF003 behavioral questions, eight Experience & Meaning items and Action schema are preserved. No new participant question wording, construct definition, scoring rule or runtime question-policy identity is introduced.

Birth-time quality belongs in the separate trusted intake, outside this blind GPT. Familiarity stays in the currently specified post-freeze metadata; a broader per-system extension is not silently added. The earlier 23-topic/seven-probe adaptive candidate remains a design candidate, not a new active runtime menu. This update does not promote it or claim that all additional systems are ready to score.

## Verification and actual limits

The package was checked against the supplied installed text and the verified v1.9 release. Checks cover the instruction size limit, all file references, exact question preservation, unchanged API schema, package hashes and independent semantic/scenario review. These checks do not prove that the GPT follows every instruction in every conversation.

Public `/healthz` and `/action-openapi.yaml` both returned HTTP 200 on October 26. The schema was exactly v1.9.0; health reported GPT submission, review queue, fast review and ready-review finishing enabled. These flags are not proof of a current worker heartbeat or a completed private end-to-end submission. The standalone web-interview route was reported disabled and its direct provider unconfigured; that is distinct from the configured GPT review/queue path.

The last inspected backend can misclassify text containing both a numeric date and clock time as possible target exposure. The new guide preserves the source and requires an honest diagnostic instead of silent editing or a false contamination claim. That software filter is not repaired by this instruction update.

The owner's successful CLI login is accepted as reported. This package does not rotate credentials, change Railway settings, redeploy a service or access participant records. The remaining installation step is replacing the existing GPT's Instructions/Knowledge and verifying its existing Action schema as above.
