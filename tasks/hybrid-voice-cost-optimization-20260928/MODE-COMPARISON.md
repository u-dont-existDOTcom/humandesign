# Voice-first versus Railway collection — development comparison

Date: 2026-09-28. This is a product/measurement comparison, not a validation study.

## Question

Does voice-first ChatGPT collection preserve richer, better-scoped behavioral evidence with lower participant burden, while leaving Railway useful mainly for durable provenance and a small number of unresolved clarifications?

Do not assume either collection mode is superior or equivalent before observing records.

## Modes

- `chatgpt_voice`: participant primarily speaks to the Life Patterns voice GPT.
- `chatgpt_text`: participant primarily types in the same ChatGPT collector.
- `mixed`: material use of both voice and typing in that ChatGPT collector.
- `railway_text`: participant answers directly in the Railway app.

A ChatGPT record imported into Railway retains its original mode. Later Railway questions count as clarification turns rather than changing the source mode.

## What to measure

For each frozen record, preserve:

- total answered turns and participant word count;
- median/interquartile answer length;
- structured conditions and correction links;
- collector-unverified evidence separately from Railway-admitted evidence/facets; never pool them as one score;
- how many additional Railway clarification turns were required;
- participant review/finish status;
- Railway model calls and prompt/completion tokens where applicable.

Use `apps/life-patterns-participant/scripts/analyze_collection_modes.py` to create CSV/JSON summaries. Supply token prices explicitly only when estimating cost; the script does not hard-code mutable provider pricing.

## Interpretation

These measurements are descriptive whole-pipeline comparisons. Mode can be confounded with participant, order, device, familiarity with ChatGPT, speaking style, interviewer/model version, and the different admission/coding steps used by each pipeline. Do not call a difference a pure voice-versus-text effect.

For the practical product decision, favor the lower-burden surface if it preserves usable source scope and does not systematically require many corrective clarifications. Do not require exact equality of word counts or facet counts.

A same-person repeat in both modes may be useful for finding concrete omissions or friction, but it is not an independent reliability test because the first interview teaches the participant the questions and constructs. If paired repeats are used, record order and treat carryover as a limitation.

## Decision path

1. Run the next development records with explicit collection mode.
2. Import voice/text ChatGPT records into Railway without discarding exact source.
3. Ask only genuinely unresolved high-value clarifications.
4. Compare descriptive richness, correction/clarification burden and cost.
5. If voice-first records routinely need few clarifications, keep ChatGPT voice as the long interview surface and Railway as clarification/provenance backend.
6. If specific neutral distinctions are systematically weak in voice collection, repair those routes or reserve only those distinctions for Railway rather than moving the entire interview to typing.

No fixed participant count or clarification-count threshold is declared in advance merely to force a decision.
