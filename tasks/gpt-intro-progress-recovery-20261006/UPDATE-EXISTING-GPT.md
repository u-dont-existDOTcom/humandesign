# Life Patterns: intro, progress and recovery update

Version: 2026-10-06.1-intro-progress-recovery

Update the EXISTING GPT. This fixes collection behavior; the fast-review API, Action schema and credential are unchanged.

## Apply these three replacements

1. Replace Instructions with `INSTRUCTIONS-life-patterns-voice-interviewer-v2.md`.
2. Replace the old Knowledge file `RECOVERY-GUIDE-v2.md` with `knowledge/RECOVERY-GUIDE-v2.md`.
3. Replace the old Knowledge file `ACTION-HANDOFF-GUIDE-v1.md` with `knowledge/ACTION-HANDOFF-GUIDE-v1.md`.

Keep the other FOUR Knowledge files, existing Action and Bearer credential. Keep Code Interpreter & Data Analysis enabled. Select Update. `GPT-BUILDER-CONFIG.md` is owner setup documentation, not a seventh Knowledge file. The previous update changed only one guide; this one changes BOTH. Leaving the old recovery guide installed leaves the conflicting multiple-candidate rule in place.

If an interview is in progress, preserve its exact source-only checkpoint before updating. Keep its saved conversation and review receipt. Do not start a duplicate review or re-answer the interview.

## What changes

The only setup question is research consent when needed. The introduction says, “You are welcome to type or talk.” Useful earlier-life comparisons default to welcome, with skipping and explicit opt-out retained. Defaults are not recorded as something the participant explicitly said. Mode remains unknown unless supported by actual metadata or the participant's statement; no mode confirmation is required at freeze.

Progress now gives estimated remaining QUESTIONS and ANSWERING MINUTES until independent review, not just imported-reply counts or a topic. It uses the current revisable plan and a stated pace assumption when actual pace is unknown. Approximate percentages describe that plan, not scientific completeness, quality or the full study. Service waiting time is separate. A complete recovered interview shows zero new main-interview questions planned; the independent reviewer may still find useful clarifications.

Library recovery searches filename aliases and all canonical schemas, follows relevant pagination, and compares actual source provenance before selecting. Verified duplicates and successors are resolved automatically. Only genuine source conflicts or unrelated plausible lineages require a choice. A newer upload is not necessarily newer evidence; an empty or partial file cannot replace fuller preserved source. Incomplete recovery pauses interviewing instead of spawning new questions. Unrecovered turns remain explicitly unknown.

## Existing data and review

This package contains no participant answers or credentials. The frozen scientific instrument and four unchanged Knowledge files are preserved. CF-003 is **required in this bundle**, after reviewed primary freeze and before chart reveal; development-secondary status does not make it optional. Historical completion does not mean that independent review or final freeze has occurred. Existing review IDs/envelopes still govern any pending review. The previously delivered fast-batch workflow and stage-specific server wait estimates remain in force.

These are changes to the supplied GPT Instructions and Knowledge. Repository tests and isolated model probes cannot prove that an unedited private GPT is already running them. The editor must receive all three replacements above.
