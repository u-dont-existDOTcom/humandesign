# Life Patterns Voice GPT — latest bundle

Built from the current `chat/hybrid-voice-cost-optimization-20260928` parent through PR #51, with the 2026-09-30.2 onboarding/resume revision.

## Configure the GPT builder

Open `GPT-BUILDER-CONFIG.md` and copy its exact:
- Name
- Description
- Conversation starters

A Custom GPT cannot send the first message on its own. Participants start by tapping a conversation starter or sending a message. The Instructions then make the GPT give the consent/privacy/mode orientation and begin.

## Put in GPT Instructions

Copy the entire contents of:
`INSTRUCTIONS-life-patterns-voice-interviewer-v2.md`

## Upload as GPT Knowledge

Upload all four files in `knowledge/`:
1. `INTERVIEW-PROTOCOL-v6.md`
2. `interviewer-bank-v7.json`
3. `EVIDENCE-GUIDE-v7.json`
4. `cf003_secondary_question_module_v0.json`

The fourth file is the new research-derived CF-003 secondary question module.

## Starting or resuming

For a new participant, tap **Start my Life Patterns interview.**

For somebody with an existing interview, attach their prior response record and tap **Continue my existing interview from the answers I’m attaching.** The GPT must preserve received participant Q&A, avoid restarting or repeating resolved questions, and ask only useful unresolved distinctions.

On ChatGPT web, an existing old interview chat can alternatively bring in this GPT with `@`; the next message goes to the GPT while retaining that conversation's context.

## CF-003 timing

The main Life Patterns record is completed and frozen first.
Then ask all three CF-003 questions before any chart/predictor reveal.
Freeze those answers separately as `life-patterns-cf003-secondary-v0.json`.
Do not merge them into the primary record or primary score.

## Important status

CF-003 is **required in this bundle**. DEVELOPMENT/SECONDARY describes its scientific status; it does not mean the questions are optional. It is not a prospectively frozen primary endpoint.
The three questions cover:
- lifetime continuity/change;
- which recurring patterns are most central across settings;
- which real patterns are peripheral/situational.

See `MANIFEST.json` and `SETUP.md` for exact hashes and protocol details.
