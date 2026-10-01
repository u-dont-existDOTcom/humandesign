# Life Patterns Voice GPT — latest bundle

Built from the current `chat/hybrid-voice-cost-optimization-20260928` parent, with the 2026-10-01.4 asynchronous Railway review loop.

## Configure the GPT builder

Open `GPT-BUILDER-CONFIG.md` and copy its exact:
- Name
- Description
- Conversation starters

Enable **Code Interpreter & Data Analysis** for downloadable backup files. Then create the Action exactly as specified in `GPT-BUILDER-CONFIG.md`; its schema URL and privacy-policy URL are public, but the Bearer API key is supplied separately and is never stored in this ZIP.

A Custom GPT cannot send the first message on its own. Participants start by tapping a conversation starter or sending a message. The Instructions then make the GPT give the consent/privacy/mode orientation and begin.

## Put in GPT Instructions

Copy the entire contents of:
`INSTRUCTIONS-life-patterns-voice-interviewer-v2.md`

## Upload as GPT Knowledge

Upload all five files in `knowledge/`:
1. `INTERVIEW-PROTOCOL-v6.md`
2. `interviewer-bank-v7.json`
3. `EVIDENCE-GUIDE-v7.json`
4. `RECOVERY-GUIDE-v2.md`
5. `cf003_secondary_question_module_v0.json`

The recovery guide carries the detailed Hâle-derived recovery/provenance safeguards. The fifth file is the research-derived CF-003 secondary question module.

## Starting or resuming

For a new participant, tap **Start my Life Patterns interview.**

For an existing interview there are three safe paths:

1. **Library fallback:** tap **Find my Life Patterns record in my Library and continue.** This explicitly authorizes a narrow search for canonical Life Patterns export/recovery schemas only. If exactly one canonical record is found, it may be imported; multiple canonical records require participant selection. Similar generic interview/personality files must be ignored.
2. **Same-chat automatic resume (web):** reopen the old interview, type `@`, select **Life Patterns Interview**, then say **Continue my interview**. The conversation context stays available to the GPT.
3. **Explicit attachment:** in a new GPT chat attach/add the prior response record and use the continue starter.

**Privacy boundary:** a generic “continue my interview” request must never trigger Library, Memory, prior-chat, connected-app, other-user-file, or GPT-Knowledge search. Library lookup requires the explicit Library starter/request above.

## Independent review, freeze, then CF-003

When the GPT thinks the primary interview is saturated, it must **not freeze yet**. It sends an unfrozen v2 candidate through `startLifePatternsReview`, receives a review ID immediately, and lets the participant leave while the independent review runs.

Later, **Check my independent Life Patterns review** calls `getLifePatternsReview`. If one clarification is returned, the GPT asks it exactly and submits only the participant's answer with `submitLifePatternsClarification`. When Railway returns `ready`, the GPT performs the neutral participant review. Any material correction starts a new independent review; otherwise the primary record is frozen.

Only after that reviewed freeze are all three CF-003 questions asked and frozen separately. Final `submitLifePatternsRecords` includes the ready review ID plus both exact frozen records. The server rejects a final primary whose behavioral turns differ from the reviewed record.

## Important status

CF-003 is **required in this bundle**. DEVELOPMENT/SECONDARY describes its scientific status; it does not mean the questions are optional. It is not a prospectively frozen primary endpoint.
The three questions cover:
- lifetime continuity/change;
- which recurring patterns are most central across settings;
- which real patterns are peripheral/situational.

See `MANIFEST.json` and `SETUP.md` for exact hashes and protocol details.
