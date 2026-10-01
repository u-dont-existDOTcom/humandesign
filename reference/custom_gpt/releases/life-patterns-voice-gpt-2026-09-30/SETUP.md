# Life Patterns voice-first ChatGPT collector

Version: 2026-10-01.3. Development collection surface.

## Purpose

Use ChatGPT's voice/text conversation as the long-form interview surface so participants can speak naturally rather than type for an hour. Railway remains the durable research/clarification surface, not a mandatory replacement for the whole interview.

This is a collection-mode experiment. A voice record is not assumed equivalent to a Railway-typed record. Preserve `collection_mode` so the modes can be compared descriptively.

## GPT setup

Create/share a GPT using exactly:

- Builder fields: `GPT-BUILDER-CONFIG.md` (name, description, starters, capabilities, Action setup)
- Enable **Code Interpreter & Data Analysis** for downloadable backup JSON files.
- Create the submission Action from `https://life-patterns-participant-production.up.railway.app/action-openapi.yaml`; use API-key Bearer auth with the private submission-only key supplied separately.
- Privacy policy URL: `https://life-patterns-participant-production.up.railway.app/privacy`
- Instructions: `life_patterns_voice_interviewer_v2.md`
- Knowledge:
  - `tasks/scenario-survey-v7-redesign-20260922/INTERVIEW-PROTOCOL-v6.md`
  - `tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json`
  - `tasks/scenario-survey-v7-redesign-20260922/EVIDENCE-GUIDE-v7.json`
  - `reference/custom_gpt/RECOVERY-GUIDE-v2.md`
  - `reference/empirical_astrology/cf003_secondary_question_module_v0.json` (development-secondary only)

Do **not** attach birth data, chart output, scores, candidate ranks, or participant-specific prior interpretation. The manifest `life_patterns_voice_gpt_manifest_v2.json` pins the source hashes and instruction size. The CF-003 secondary module is **required in this bundle**; “development-secondary” describes its scientific status, not optional activation.

The deployable instruction block is below 8,000 characters on the repository's conservative line-break count. The bank/guide are reference material, while the must-follow collection/accuracy rules stay in Instructions.

## Participant workflow

1. Open the shared GPT in a normal persistent chat. A GPT cannot speak first: tap a conversation starter or send a first message.
2. For a new interview, tap **Start my Life Patterns interview.** The GPT gives the consent/privacy/mode framing and begins after the participant answers those setup questions.
3. For an existing interview, use one of three safe paths: (a) tap **Find my Life Patterns record in my Library and continue** to explicitly authorize a narrow Library search for canonical Life Patterns schemas only; (b) on ChatGPT web reopen the old interview, type `@`, select **Life Patterns Interview**, and say **Continue my interview**; or (c) explicitly attach/add the prior response record in a new GPT chat. A generic continue request must not search Library, Memory, prior chats, connected apps, or other account-level sources.
4. Do not provide birth date/time/place or chart information.
5. At natural completion, review the behavior-only summary and correct material errors/conditions.
6. Freeze the main `life-patterns-participant-export.json` first. Then ask all three CF-003 secondary questions before any chart reveal and freeze them separately as `life-patterns-cf003-secondary-v0.json`. None of it alters the primary record or score.
7. At completion, the GPT calls `submitLifePatternsRecords` once with the two exact frozen records if consent is still true. A platform approval prompt may appear. On success it gives the participant the submission ID; on Action failure it falls back to both downloadable/labeled JSON records for manual delivery.
8. New visible-chat turns are model-exported/unverified unless reviewed. Imported records retain their declared source fidelity rather than being mislabeled as verbatim chat. The research coordinator may later use Railway for source-preserving clarification.

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
