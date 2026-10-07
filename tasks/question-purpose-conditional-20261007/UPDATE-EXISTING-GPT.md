# Update your existing Life Patterns GPT

Version: 2026-10-07.2-question-purpose-conditional

This supersedes the earlier 2026-10-07 question-purpose packet. Keep the same GPT, saved conversation, and Railway review.

## If you have NOT applied the earlier question-purpose packet
Apply this latest packet only:
1. Replace Instructions with `INSTRUCTIONS-life-patterns-voice-interviewer-v2.md`.
2. Replace only `TENDENCY-FIRST-GUIDE-v1.json` in Knowledge.
3. Reimport `ACTION-life-patterns-submission-openapi.yaml` into the EXISTING Action, keeping its existing Bearer credential.
4. Select Update.

## If you ALREADY applied the earlier question-purpose packet
Only replace Instructions with this packet's `INSTRUCTIONS-life-patterns-voice-interviewer-v2.md`, then select Update. The Knowledge file and Action schema are unchanged from that packet.

## Corrected participant-facing rule
Do not automatically show `What this tests:`. Ask the exact question alone when the tested dimension is already obvious. Use the returned/curated `participant_purpose` only when a scenario, example, or follow-up would otherwise make the purpose unclear. Never add a purpose line that merely paraphrases the question.

Example that should now appear WITHOUT a purpose line:

> Apart from its practical benefits, how important is recognition from other people to you?

Purpose explanations remain neutral and must not reveal answer direction, scoring, chart targets, astrology/Human Design interpretation, or diagnostic/validated-trait claims.
