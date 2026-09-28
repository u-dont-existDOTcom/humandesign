# Voice-first / Railway clarification pilot

Date: 2026-09-28. Development measurement only.

## Question

Does the long participant interview need to happen inside Railway, or can ChatGPT voice/text collect an equally useful source record while Railway is restricted to durable storage, source auditing and a small number of unresolved clarifications?

The pilot does not assume the modes are equivalent. Collection mode is recorded as chatgpt_voice, chatgpt_text, mixed, railway_text or unknown so mode can remain an explicit measurement/source-format covariate.

## Candidate participant flow

1. Long-form intake: use the Life Patterns Voice Interviewer v2 in ChatGPT. Voice is encouraged when typing burden would shorten answers. Record collection mode and whether optional earlier-life comparisons are welcome as nonbehavioral metadata. Birth/chart/target information stays outside the interview.
2. Freeze: ChatGPT performs a neutral source review, then creates one exact behavioral JSON record. The transcript text is the source; audio itself is not treated as verified evidence.
3. Import: Railway stores that complete record exactly with its source type and collection mode.
4. Compact synthesis: Railway performs one semantic source review over the imported record, creating a small evidence/coverage ledger. It does not repeatedly resend the full survey authority after this step.
5. Clarification only: Railway asks only unresolved, material canonical distinctions. Routine prompt context is limited to the new answer, necessary antecedents, accepted evidence ledger, a bounded route shortlist and route-specific evidence guidance.
6. Final review: corrections append to history. The server freezes the structured continuation before any target reveal.

A participant is never asked to redo the whole survey in Railway merely because ChatGPT collected the first record.

## Development measurements

Use apps/life-patterns-participant/scripts/analyze_collection_modes.py. Compare source modes descriptively; do not call a small development sample psychometric equivalence.

Per record:
- total and median participant answer words;
- imported versus Railway clarification turns;
- evidence item and unique-facet counts;
- correction links and structured conditions;
- canonical routes actually represented;
- participant-review completion;
- model call, prompt-token and completion-token totals;
- optional cost estimate only when explicit input/output prices are supplied.

The most decision-relevant measure for the hybrid design is clarification delta: after a complete ChatGPT record is imported, how many Railway clarification answers materially alter/add scoped evidence or correct the neutral review?

Interpretation:
- If ChatGPT-first records usually need zero or a few clarifications and final review rarely changes material evidence, keep the long interview voice-first and use Railway as the source/provenance/clarification backend.
- If Railway repeatedly uncovers material missing distinctions or corrections that affect the shared-model input, keep those specific clarifier functions. This still does not imply an hour-long Railway duplicate survey.
- If collection mode appears associated with answer richness or correction burden, retain mode as a covariate and gather more data. Do not erase the mode effect by pooling.

## Avoiding a contaminated paired comparison

Do not make one participant complete the entire survey once by voice and then immediately complete the same full survey again by typing just to compare the modes. Repetition, memory and fatigue would contaminate the comparison.

For the current development phase, prefer ChatGPT long-form source plus Railway clarification delta. Later, if mode equivalence matters scientifically, compare separate development participants or use a counterbalanced design before making a general claim.

## Inference-cost contract

Development semantic probes use subscription-authenticated Codex CLI where available; no Venice call is needed to test prompt/schema behavior. A Railway Cloud Agent may host Codex for development when its connection works, but it is not the public participant backend.

Production remains API-backed only when needed and after prompt-cost measurement. The implementation must fail closed on prompt-budget regression rather than silently returning to full-bank/full-transcript calls.

Current initial budget:
- bulk import model context <= 110,000 serialized characters;
- ordinary clarification model context <= 35,000 serialized characters;
- ordinary route shortlist <= 12, mixing fresh self-contained scenes with eligible follow-ups;
- optional-retrospective routes are absent unless the participant explicitly welcomed them;
- ordinary evidence guide is limited to the route just answered;
- reviewer receives the selected route and cited facet guidance, not all alternative routes;
- model-call telemetry records context/request characters and token usage when the provider returns it;
- default model-call ceiling is 12 actual semantic model calls per session, reserving two Plan+Admission pairs so a later review correction still has its one permitted repair;
- low experimental output-token caps are not enabled until Venice/XHigh truncation behavior can be tested without spending scarce development credit.

These are engineering cost ceilings, not survey quotas or evidence sufficiency criteria.

## Accuracy / claim integrity

The voice interviewer and Railway planner/reviewer both carry the core PR #42 protections:
- claims about the participant require their supplied words and scope;
- quotation marks contain exact transcript/source substrings;
- absence claims require checking the claimed source scope;
- participant corrections trigger source re-check rather than automatic defense or concession;
- prompt/editor premises do not become participant evidence;
- uncertainty and context remain explicit.

The full PR #42 block is not pasted wholesale into the older deployable AstroHD owner-pilot instructions because that file is already near its builder limit and belongs to a different Action-based runtime. The core rules are ported into the new voice-first instrument instead.
