# Life Patterns voice-first ChatGPT collector

Version: 2026-09-28. Development collection surface.

## Purpose

Use ChatGPT's voice/text conversation as the long-form interview surface so participants can speak naturally rather than type for an hour. Railway remains the durable research/clarification surface, not a mandatory replacement for the whole interview.

This is a collection-mode experiment. A voice record is not assumed equivalent to a Railway-typed record. Preserve `collection_mode` so the modes can be compared descriptively.

## GPT setup

Create/share a GPT using exactly:

- Instructions: `life_patterns_voice_interviewer_v2.md`
- Knowledge:
  - `tasks/scenario-survey-v7-redesign-20260922/INTERVIEW-PROTOCOL-v6.md`
  - `tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json`
  - `tasks/scenario-survey-v7-redesign-20260922/EVIDENCE-GUIDE-v7.json`

Do **not** attach birth data, chart output, scores, candidate ranks, or participant-specific prior interpretation. The manifest `life_patterns_voice_gpt_manifest_v2.json` pins the source hashes and instruction size.

The deployable instruction block is below 8,000 characters on the repository's conservative line-break count. The bank/guide are reference material, while the must-follow collection/accuracy rules stay in Instructions.

## Participant workflow

1. Open the shared GPT in a normal persistent chat.
2. Use voice, text, or both. Long spoken answers are welcome. The interviewer records whether optional earlier-life comparisons are welcome and confirms the actual voice/text/mixed mode at the end.
3. Do not provide birth date/time/place or chart information.
4. The interviewer asks only useful nonredundant behavioral questions. The bank is not a quota.
5. At natural completion, review the behavior-only summary and correct material errors/conditions.
6. Ask for the frozen `life-patterns-participant-export.json` if the GPT has not already created it. Its transcript fidelity is explicitly model-exported/unverified unless the participant reviewed it, and its evidence is collector-unverified.
7. The research coordinator may import that frozen record into Railway. Railway preserves the upstream record but does not treat GPT-authored evidence as admitted; it should ask only unresolved clarifications and must not make the participant repeat usable voice answers.

## Measurement decision

Use `apps/life-patterns-participant/scripts/analyze_collection_modes.py` on frozen exports. Compare, by explicit source mode:

- answer length distribution;
- number of conditions/corrections;
- collector-unverified evidence separately from Railway-admitted evidence/facet yield;
- Railway clarification burden after import;
- completion/review status;
- model call and token usage where Railway inference occurred.

These are descriptive whole-pipeline signals, not proof that the modes are psychometrically equivalent or that any difference is caused by voice alone. Source mode can be confounded with participant, device, order, speaking style, interviewer version, and downstream admission/coding.

A useful first decision is simpler: if voice-first records require few Railway clarifications and preserve equal-or-better scoped evidence with much lower participant burden, keep Railway as the clarification/provenance backend. If systematic gaps remain, identify which neutral distinctions actually need Railway clarification instead of forcing the entire survey into typing.

## Accuracy-rule lineage

The voice collector includes the core attribution/quotation/absence/correction rules proposed in PR #42, adapted to this collection surface. It does not merge PR #42 into the older AstroHD owner-pilot GPT. Reveal-specific rules are omitted because this collector does not perform the AstroHD reveal.
