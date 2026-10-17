# Life Patterns — Railway takes over review immediately

This release fixes the issue in which an already completed GPT interview still required repeated ChatGPT check-ins and never showed a final question count.

The existing GPT now offers **Continue privately on Railway** as soon as Railway has saved the independent review, even if the reviewer is still queued or asking questions. The participant receives one private link; on Railway she can answer/skip exact reviewer questions, see review progress automatically while the page stays open, and choose **Stop further questions** at any time. This records unresolved areas as unknown and requests the independent evidence review to finish with what was already supplied. Its processing time is not guaranteed. Only actual independent ready status enables final evidence confirmation, three CF003 items and encrypted submission.

## Apply to the EXISTING Life Patterns Interview Custom GPT

1. Open the existing GPT in ChatGPT: My GPTs → Life Patterns Interview → Edit GPT → Configure.
2. Replace its **Instructions** with the complete `INSTRUCTIONS-life-patterns-voice-interviewer-v2.md` (strict 7,944 characters).
3. Replace Knowledge file **ACTION-HANDOFF-GUIDE-v1.md** with the copy in this folder. Preserve the other seven Knowledge files. The complete verified set of eight is here if needed.
4. Reimport **ACTION-life-patterns-submission-openapi.yaml** v1.8.0 into the GPT's **same existing Action**. Preserve its existing private Bearer credential, privacy URL and Code Interpreter. Do not create a second Action.
5. Click the editor's **Update** control, then return to the participant's EXISTING saved conversation.

### Test with an existing participant

If that participant's source was already submitted for independent review and Railway returned the saved review ID, tell the GPT: **Give me my private Railway link now for my existing saved review. I do not want more ChatGPT review check-ins.**

The GPT will use one approved Action to issue a link. The one-use link expires in 20 minutes; a redeemed private browser session remains usable for up to seven days. No new main interview, identity lookup, duplicate review, or repeated questionnaire. On Railway, admitted questions and skips are saved to the same record; the progress page checks status while open. No notifications are generated after closing the browser.

**If the participant has never submitted the earlier answers to Railway:** complete the consented source-only review submission in the existing GPT chat once. Then request the portal link; do not restart the old survey. If the review is blocked or the worker offline, the page reports that honestly.

**If the user clicks Stop further questions:** no further questions are admitted. The independent evidence synthesis still has to run and may be blocked or take time; that choice is not falsely shown as completed final storage. Already admitted but unanswered items are explicitly skipped, never hallucinated as evidence.

### Optional research materials, NOT in the live questionnaire

`EXPERIENCE-MEANING-PILOT-v0.json`: eight optional research prompts, four suggested initially, covering surprise, wonder, insight, meaning, guidance and synchronicity. `CHART-DOMAIN-V7-RECONCILIATION-v0.json`: source-anchored initial chart-topic to survey-coverage audit. Neither changes frozen astrology mappings or anyone's existing interview, and neither must be answered by current participants.
