# Voice-first / Railway clarification cost optimization

Date: 2026-09-28. Assurance lane: Iteration with targeted privacy/data-integrity tests. No paid inference is authorized for development verification.

## Owner outcome

Preserve high-quality long-form answers, including voice input through ChatGPT, while avoiding API costs large enough to consume the owner's daily Venice allowance. Railway should add durable storage, provenance and only genuinely useful clarifications rather than force an hour of typing.

## Supported diagnosis

The current Railway semantic loop sends the complete interview protocol/controller, all 79 route records, all 73 neutral evidence facets and the accumulated transcript to the planner, then sends substantial repeated context to an independent admission call. One private 96-turn development record measured ~175k characters before output/reasoning for one planner call; participant text and identity are excluded from public artifacts.

## Candidate

1. Compile a compact immutable route/evidence catalog from the frozen bank/guide.
2. On imported ChatGPT transcripts, run one source-synthesis call over the exact transcript plus compact catalog. Persist a compact evidence/coverage ledger.
3. On later clarifications, send only:
   - the exact new answer/question and necessary antecedents,
   - compact accepted ledger,
   - a bounded deterministic shortlist of eligible unresolved routes,
   - guide entries for only those routes.
4. Keep full raw turns server-side for deterministic quote/provenance validation; do not resend them unless needed.
5. For exact canonical questions, deterministic admission handles route IDs, repeats and antecedents. Reserve a second semantic admission call for adapted/context-repair questions, bulk import synthesis/final review, or another explicitly ambiguous semantic boundary.
6. Add explicit prompt-budget telemetry and per-session call/token/cost estimates; no hidden paid tests.
7. Add a Codex development-probe runner usable locally or on an existing Railway Cloud Agent so development semantic probes can use the owner's Codex/ChatGPT credentials rather than Venice API credit.
8. Preserve a voice-first ChatGPT intake path and define a descriptive development comparison against Railway typing/clarification. Source mode remains a covariate; no mode is declared scientifically equivalent without data.
9. Port the core claim-integrity checks from PR #42 into the new voice-first interviewer instructions and Railway semantic prompts. Quotes remain exact; absence claims require the checked source; corrections require source re-check; no invented motives/backstory.

## Non-goals

- no astrology scoring/ranking change;
- no claim that ChatGPT Voice and Railway typing are measurement-equivalent;
- no production switch to Railway Agent or subscription-authenticated Codex as a public inference API;
- no Venice credit purchase or OpenRouter spend;
- no forced full-bank completion quota;
- no deletion/rewrite of historical participant source.
