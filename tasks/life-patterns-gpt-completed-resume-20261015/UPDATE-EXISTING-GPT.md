# Update the existing Life Patterns Interview GPT

Version: 2026-10-15.1. This replaces the previous Oct 9 update packet without creating a second GPT or restarting any existing interview.

## Owner action in the GPT editor

Open your existing **Life Patterns Interview** in ChatGPT → **Edit GPT** → **Configure**.

1. Replace **Instructions** with the complete contents of **INSTRUCTIONS-life-patterns-voice-interviewer-v2.md** from this ZIP (verified under the strict 8,000-character limit).
2. In **Knowledge**, **ADD only one new file**: knowledge/COMPLETED-INTERVIEW-CONTINUATION-v1.md.
3. Bring existing files up to date **only if not already at the Oct 9 version**: replace ACTION-HANDOFF-GUIDE-v1.md, TENDENCY-FIRST-GUIDE-v1.json and cf003_secondary_question_module_v0.json with the copies in the ZIP. Preserve the other four Knowledge files (INTERVIEW-PROTOCOL-v6.md, interviewer-bank-v7.json, EVIDENCE-GUIDE-v7.json, RECOVERY-GUIDE-v2.md). The archive includes all eight for a full readback.
4. Keep the SAME Action, authenticated Bearer credential, Privacy Policy URL and Code Interpreter/Data Analysis enabled. If the Action has not been updated to schema v1.6.0, import ACTION-life-patterns-submission-openapi.yaml **into that existing Action**. Never create a duplicate Action or ask the owner to paste the credential.
5. Click the GPT editor's **Update** button. A GitHub commit, regenerated ZIP or unsaved editor preview does not update the private GPT. Reopen the GPT as a **normal saved conversation**, not a Builder Preview conversation, for real research use.

The GPT editor click is a private account UI action; the research code cannot mark it complete without a successful editor readback. Preserve the current saved interview and any queued Railway review. Do not start duplicate reviews or discard old answers.

## A participant's completed historical survey

An already completed, lightly edited interview document is the relevant source; **do not put it in GPT Knowledge**. A participant can bring Life Patterns Interview into the existing saved interview chat by typing the @ mention, or attach her original completed DOCX or its source-only JSON in a new saved GPT chat. The existing answers need not be typed again.

The GPT must verify the complete numbered Q&A set and its editorial disclaimer. This document is a lightly edited record, not authenticated word-for-word original speech. If consent to research review and final submission is not documented in the allowed chat, the GPT asks once. Then it proceeds to **independent source-wide review**; zero new main-survey questions are planned. Only substantive, nonduplicative questions actually admitted by the reviewer are asked one at a time. The role-entry three-example exercise and eight cognitive revisions are not mandatory retests.

Nothing in this packet changes astronomical models, the accepted six-rule result, participant records, the Railway review backend, or the original V7 science. Any future chart comparison must preserve first unedited source provenance and classify any previously evaluated person's source appropriately; research already familiar with her chart does not retroactively become blind.

## Safe verification

With a newly started **synthetic** test only, attach a mock complete Q&A excerpt, establish dummy consent, and check that the GPT can count old answers, produce the correct UNFROZEN backup and state "0 new main interview questions planned; next independent review." Do not send actual participant data in Builder Preview. A real reviewer Action is separately approved by the participant. The live backend currently reports the GPT review queue and fast-batch protocol enabled, although a reviewer worker may still be unavailable when a request is queued.

This is a cumulative non-secret update packet. Your current GPT's private Bearer key and any participant source file are deliberately absent.
