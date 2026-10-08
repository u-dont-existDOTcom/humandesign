# Update the existing Life Patterns GPT — question feedback return path

Version: `2026-10-08.1-question-feedback-inbox`. This is cumulative; it supersedes the earlier 2026-10-07 updates. Keep the same GPT, saved conversation, consent settings, Railway review and Action credential. Do not create a replacement interview.

## In Edit GPT / Configure

1. Replace Instructions with `INSTRUCTIONS-life-patterns-voice-interviewer-v2.md`.
2. Replace the three Knowledge files with the versions in this packet: `ACTION-HANDOFF-GUIDE-v1.md`, `TENDENCY-FIRST-GUIDE-v1.json`, and `cf003_secondary_question_module_v0.json`. Keep other Knowledge files unchanged.
3. Reimport `ACTION-life-patterns-submission-openapi.yaml` into the existing Action, keeping the existing Bearer credential. The Action schema itself has not changed since the previous closeout release.
4. Select **Update**.

## What is newly included

If someone calls a question unclear, redundant, obvious, or not genuinely informative, the GPT preserves the exact complaint as `process_feedback` linked to the question/route. With research consent and the existing Railway review submission, the comment becomes available in the private researcher Question feedback panel without any additional participant Allow card. It is not coded as personality and does not rewrite a question automatically. The researcher can inspect the route and exact objection and use them to propose a separately versioned improvement.

All previous fixes remain: phase-local Allow forecasts; final-review measured labels; the obsolete Memory question removed; and JSON-string final submission.

## Actual question wording revision status

Nine question texts have been revised in a **separate development candidate** plus three legacy routes proposed for retirement. That candidate is deliberately NOT in this participant-facing Knowledge file and not deployed. The active v1 questionnaire remains pinned so existing saved reviews are not modified midstream. See the separately supplied question revision crosswalk for what changed and why.

## Resume a saved review

Use the same chat. If final submission was previously rejected for missing record fields, request retry from the exact frozen primary and CF-003 JSON records; do not re-interview, reconstruct or redo the independent review. The real submission is confirmed only by its service receipt.
