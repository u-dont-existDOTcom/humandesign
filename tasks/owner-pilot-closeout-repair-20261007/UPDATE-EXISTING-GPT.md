# Update the existing Life Patterns GPT

Version: `2026-10-07.3-owner-pilot-closeout`

This cumulative update supersedes the earlier 2026-10-07 question-purpose packets. Keep the **same GPT, saved conversation and Railway review**. Do not create a replacement review or repeat the interview.

## Replace these items in Edit GPT / Configure

1. Replace Instructions with `INSTRUCTIONS-life-patterns-voice-interviewer-v2.md`.
2. In Knowledge, replace these three files with the packet copies:
   - `ACTION-HANDOFF-GUIDE-v1.md`
   - `TENDENCY-FIRST-GUIDE-v1.json`
   - `cf003_secondary_question_module_v0.json`
   Keep the other Knowledge files unchanged.
3. Edit the **existing** Action and import `ACTION-life-patterns-submission-openapi.yaml`. Keep the existing Bearer credential; do not create a duplicate Action or paste the key into chat.
4. Select **Update**.

## What this fixes

- Before each consequential Action, the GPT states the current phase's known call sequence and then visibly says: `Please click Allow on this tool call to continue.`
- A clarification round is explained as two service calls: save the answer batch, then retrieve the updated review later. After the first call, the GPT stops and gives a check-back time instead of leaving a surprise second card pending. Final storage is one call/one expected card.
- Final-review entries display `What this measures:` and split unrelated constructs instead of presenting unlabeled or fused observations.
- Direct questions still omit redundant purpose paraphrases; purpose text appears only for unclear scenarios/follow-ups.
- The obsolete “Was ChatGPT Memory enabled?” question is removed. Actual visible birth/chart/HD exposure is logged instead; the participant is not asked to change Memory settings.
- Final submission sends both exact frozen records through `primary_record_json` and `cf003_record_json`, fixing the missing-object-parameter failure while preserving server validation.
- Obvious, tautological, under-specified and question-quality objections are protected from being promoted into trait evidence merely to fill coverage.

## Resume this owner pilot

After updating, return to the same saved survey chat and say:

> Retry the final submission using the exact frozen primary and CF-003 records already created in this chat. Do not repeat the interview, independent review, CF-003 answers or metadata questions.

The GPT should explain that this is **one final storage call and one expected Allow card**, show the exact Allow sentence immediately above the call, and report success only after a submission receipt containing a submission ID.

If either exact frozen file is no longer visible, attach that file rather than reconstructing answers. The existing ready Railway review remains the authority.
