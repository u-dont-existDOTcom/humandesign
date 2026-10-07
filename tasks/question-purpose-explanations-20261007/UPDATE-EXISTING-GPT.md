# Update your existing Life Patterns GPT

Version: 2026-10-07.1-question-purpose

This is an UPDATE to the same GPT. Keep the same saved conversation and the same Railway review. Do not create a replacement GPT or review.

## Three replacements in Edit GPT / Configure

1. Replace Instructions with `INSTRUCTIONS-life-patterns-voice-interviewer-v2.md` from this packet.
2. In Knowledge, replace only `TENDENCY-FIRST-GUIDE-v1.json` with `knowledge/TENDENCY-FIRST-GUIDE-v1.json` from this packet. Keep the other Knowledge files unchanged.
3. Edit the EXISTING Action and import `ACTION-life-patterns-submission-openapi.yaml` (or reimport the live schema URL after the Railway deployment). Keep the existing Bearer API credential. Do not create a duplicate Action or paste any secret into chat.

Select Update to apply the changes.

## Required participant-facing behavior

Before every behavioral question, show a short line beginning `What this tests:` that names the neutral person-level pattern or distinction being checked. Then ask the exact question separately.

For Railway review clarifications, use the returned `participant_purpose` for that line and ask returned `question_text` verbatim. For main-interview questions, use the curated `participant_purpose` when present; for a legacy probe, explain its planning target/family in plain English.

The purpose line must not reveal answer direction, scoring, chart targets, astrology/Human Design interpretation, or claim diagnostic/validated-trait status.

The exact question remains separate from the explanation so source wording, route matching, and historical provenance remain intact.

## Existing reviews

The Railway service enriches already-saved pending clarifications on read. It does not replace the review, change the clarification ID/question text, add an answer/skip, or alter clarification history. Continue in the same saved chat.
