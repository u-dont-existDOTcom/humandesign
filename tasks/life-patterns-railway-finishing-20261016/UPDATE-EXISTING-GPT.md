# Existing Life Patterns GPT — add secure Railway finishing

This is a cumulative update for the **existing** Life Patterns Interview GPT. It preserves the original 96-answer import, previous clarifications, the independent review and all eight Knowledge files.

In Edit GPT → Configure: replace Instructions with INSTRUCTIONS-life-patterns-voice-interviewer-v2.md; replace Knowledge/ACTION-HANDOFF-GUIDE-v1.md; retain the other seven Knowledge files. Reimport ACTION-life-patterns-submission-openapi.yaml (v1.7.0) into the **same existing Action**, retaining its private Bearer credential and privacy-policy URL. Do not create another Action or paste a secret into chat. Click **Update**; repository changes alone do not edit a private GPT.

**The finishing link is offered only after the existing Railway review reaches status ready.** When the participant chooses that route, the GPT obtains explicit tool approval once to invoke issueLifePatternsFinishLink, then shows the returned private short-lived link. The GPT must not perform its own final freeze, CF003 or storage on that same review after handing off.

The participant opens that link, confirms the independent reviewed evidence (or returns to their original GPT chat for a correction), answers the three exact CF003 questions and short research-familiarity metadata, and submits. The browser page reports success only when the same encrypted backend returns an actual submission receipt.

No repeated main interview, no arbitrary lifetime clarification cap, no DOB/chart material. If the review is still queued or another useful clarification is pending, the GPT must continue the existing review and must not fabricate a finishing link.

Railway deployment and actual private GPT editor update are different actions. The release remains unverified for real participant use until both are confirmed against the exact live service and an already-ready test review.
