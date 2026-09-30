# Life Patterns Voice GPT — latest bundle

Built from `chat/hybrid-voice-cost-optimization-20260928` after PRs #47, #48, #45, and #49.

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

## CF-003 timing

The main Life Patterns record is completed and frozen first.
Only then, if the CF-003 development module is enabled, ask its three questions before any chart/predictor reveal.
Freeze those answers separately as `life-patterns-cf003-secondary-v0.json`.
Do not merge them into the primary record or primary score.

## Important status

CF-003 is DEVELOPMENT/SECONDARY, not a prospectively frozen primary endpoint.
The three questions cover:
- lifetime continuity/change;
- which recurring patterns are most central across settings;
- which real patterns are peripheral/situational.

See `MANIFEST.json` and `SETUP.md` for exact hashes and protocol details.
