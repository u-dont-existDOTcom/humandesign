# Life Patterns owner-survey recovery — verified engineering closeout

## Scope and verified live state

The exact-source reviewed-submission fallback and researcher-login UX were merged into the canonical integration branch at `bbef9765bb36e08e045def44267bebd8a91c3479`, then deployed from an exact parity-verified ~740 KiB slim build context into the EXISTING Railway participant service. Railway reports deployment `e87656e2-d6ab-4e6b-b2e9-540257528e5c` **SUCCESS** (2026-10-09). Its `/healthz` and `/admin` return HTTP 200; the live Action schema is version 1.6.0, byte-identical to the merged repository schema, and does not require a `review_id` on final submission. The admin page visibly offers the private key unlock, and unauthorized feedback API returns HTTP 401.

Authenticated read-only production check returned **nine** consenting researcher-feedback entries, **one** prior stored submission (the earlier synthetic test), and four stored Railway sessions. These counts are post-deployment; the owner's REAL 84-turn submission has NOT been stored by this continuation. None of the readbacks changed human interview or reviewer data.

## Why the owner's final submission failed, and the prepared repair

The user-visible frozen primary was not a standalone turn list; it referenced an exact 82-turn base in the owner's ChatGPT File Library and appended two further frozen turns. The server correctly rejected the absence of top-level `turns`. The ChatGPT Library base was retrieved in full and compared against one uniquely matching existing ready 81+3 Railway review, preserving every original question/answer, provenance, chronology and a non-answer clarification with a separately recorded question-quality comment. The original frozen primary and CF-003 files were never edited.

A separately versioned derived 84-turn standalone primary and hash-only-relinked CF-003 (three questions unchanged) were created owner-locally. On a disposable copy of the real encrypted production database, the repaired API returned HTTP 200 with a matching reviewed-submission storage receipt and exact idempotent retry. Relevant tests also reject changed answers, partial turn lists, ambiguous ready matches and alterations to original historical process feedback. This local rehearsal IS NOT real production receipt.

When an authorized production POST was attempted through the available Remote Desktop Commander tool, the host returned **blocked by OpenAI safety checks because the safety status was indeterminate**. No child process or service submission resulted. Do not bypass this tool safety boundary or falsely claim the real human record was stored. The current real production readback still shows only the prior synthetic submission.

The 84-turn primary and exact three-turn CF-003 derived copies were copied into the owner's visible OS Downloads with permission mode 0600, ready for the intended authorized route: attach both to the SAME existing Custom GPT conversation, after applying the cumulative GPT packet, and click Allow on the final Action. The new server matches the source to the unique existing ready review; it does not need an opaque review ID and does not repeat the interview. A real receipt is still required.

## Researcher dashboard fix

The old dashboard silently tried unauthorized API calls, displaying empty panels. It now presents a Researcher key unlock screen and labels missing authorization as **no records loaded**, not zero data. It retains bearer-token authorization and allows locking the session. A local launcher script was installed in Downloads and a desktop Applications-menu shortcut was installed; the script resolves the key through the authorized Railway CLI at invocation and copies it to the desktop clipboard, without committing/printing the key. The launcher passed Bash syntax checks, but the real graphical paste flow could not be verified through the headless desktop-relay process; do not claim GUI UX field validation. Manual private key entry remains supported.

## Inspectability and methodological limits

Delivered locally: an interactive question/interpretation atlas covering 79 frozen historical v7 questions, 25 current v1 tendency-first questions, 25 not-live v2 proposals and all 73 historical coding facets (sample answer, narrow supported inference and prohibited extension); a separate private HTML explaining every exact current answer and the six admitted independent-review observations; and the historical-vs-current birth-mapping assessment. Private respondent Q/A stays off Git.

The current source preserves 78/79 exact old Q/A pairs. Of six admitted findings, four depend entirely on old source, two have mixed source and none is wholly new. A known-target six-rule AstroHD development fit is not a blind replication; the independent frozen V4.3 survey crosswalk historically ranked the exact owner birth interval 1,562nd while a 2013 interval was first. The 5-domain V1.5 interface is too compressed to prove new independent birth-date recovery from this record without a newly confirmed frozen profile. Do not pool distinct models or claim the new record successfully decoded DOB/time.

## Automatic feedback review

A daily 8 a.m. local-time conditional ChatGPT task was created (SUCCESS). It will try to inspect the private consented question-feedback queue, make narrowly scoped, safely versioned fixes, preserve old frozen studies and send an anonymized question-choice email to the owner-specified address via the connected Gmail plugin if material ambiguity arises. The task has NOT run yet, and no email was sent. This is a future scheduled workflow, not a deployed always-running Railway feedback agent. No automatic current-question edits or established scientific validation are claimed.

## Verification scope

- Participant-service suite: 220 passed.
- Repository suite: 1,021 passed / six astronomy-data skips.
- Hosted GitHub verify/browser checks passed; pull request merged.
- Scoped changed-code Ruff passed with documented legacy exclusions; Node admin JS syntax and local launcher Bash syntax passed.
- Test-only real-source rehearsal on disposable DB: exact record match, encrypted submission success, idempotent retry. No private payload was committed to Git.
- Railway deployment healthy, live Action schema SHA-256 matches source; 401 unauthorized and 200 authenticated readback verified.
- Cumulative same-GPT ZIP delivered and SHA-256 verified; two derived JSONs verified in Downloads.

## Remaining last-mile human/platform boundary

Owner must apply cumulative GPT editor update, attach the two exact derived JSONs from Downloads in their SAME saved survey chat, and approve the single final Action if prompted. Record submission success only after the actual Railway receipt. The desktop launcher clipboard paste still needs human GUI validation; dashboard alternative is manual private-key unlock.
