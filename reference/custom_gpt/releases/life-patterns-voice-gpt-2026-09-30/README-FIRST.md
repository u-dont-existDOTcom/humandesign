# Life Patterns Voice GPT — latest bundle

Built from the current `chat/hybrid-voice-cost-optimization-20260928` parent, with the 2026-10-01.3 explicit canonical-Library resume fallback.

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

## CF-003 timing

The main Life Patterns record is completed and frozen first.
Then ask all three CF-003 questions before any chart/predictor reveal.
Freeze those answers separately as `life-patterns-cf003-secondary-v0.json`.
Do not merge them into the primary record or primary score. At the end, the GPT sends both frozen records through the authenticated `submitLifePatternsRecords` Action. On success it shows a submission receipt ID; if the Action is unavailable or fails, it falls back to both JSON files/objects for manual delivery.

## Important status

CF-003 is **required in this bundle**. DEVELOPMENT/SECONDARY describes its scientific status; it does not mean the questions are optional. It is not a prospectively frozen primary endpoint.
The three questions cover:
- lifetime continuity/change;
- which recurring patterns are most central across settings;
- which real patterns are peripheral/situational.

See `MANIFEST.json` and `SETUP.md` for exact hashes and protocol details.
