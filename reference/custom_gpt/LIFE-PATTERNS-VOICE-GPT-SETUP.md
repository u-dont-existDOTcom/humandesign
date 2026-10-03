# Life Patterns voice-first ChatGPT collector

Version: 2026-10-03.4-readonly-status-approval. Development collection surface.

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
5. Before each Action that can show a permission card, say exactly once: **“Please click Allow on this tool call to continue.”** The UI may label the button **Allow once**. Never print that sentence twice for one tool call.
6. When the interview appears naturally saturated, **do not freeze yet**. Build the unfrozen v2 candidate plus the durable review handoff envelope, then call `startLifePatternsReview`. Preserve the request ID before the call and the returned review ID afterward. If a later chat turn loses the review ID, replay the exact saved request envelope so the idempotent server returns the same review instead of creating a duplicate.
7. `queued`/`processing`: use `recommended_check_after_seconds`; otherwise say about **10 minutes** for the initial pass and **3 minutes** after a clarification. They may leave the chat, and any ordinary continuation message checks the saved review. `clarification_needed`: ask the returned question exactly, preserve its route ID, and send its exact answer with `submitLifePatternsClarification`. Another clarification is allowed only when independently admitted as materially useful and nonredundant; there is no arbitrary one-question cap. `ready`: proceed to the neutral participant review. `error`: preserve the candidate and report the error without freezing.
8. After Railway is ready, show the neutral review. A material participant correction creates a new turn and requires a **new independent review** before freeze. With no material correction, freeze `life-patterns-participant-export.json`.
9. Then ask all three CF-003 secondary questions and freeze `life-patterns-cf003-secondary-v0.json` separately. None of it alters the primary record or score.
10. Call `submitLifePatternsRecords` once with the ready review ID plus both exact frozen records. On success show the submission ID; on Action failure fall back to both JSON records for manual delivery.
11. New visible-chat turns are model-exported/unverified until Railway review/admission. Imported records retain their declared source fidelity.

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

## Delivery hotfix 2026-10-01.5

Add `ACTION-HANDOFF-GUIDE-v1.md` as the sixth Knowledge file. Replace Instructions and reimport the existing Action schema (1.2.1); keep the same Bearer credential. This adds exact backup before the first review call, actionable error paths, the explicit approval sentence, honest stage/count progress, and a bottom status footer. Existing five Knowledge files and frozen v7 measurement wording are unchanged. A separate hybrid question candidate is under development; this delivery fix does not silently activate it.

## Owner iteration rule — context resilience

Do not run a substantive owner interview in Builder Preview. Use a normal saved GPT conversation. Before any GPT configuration update during an in-progress test, have that chat create and link `life-patterns-live-recovery-checkpoint.json` under `ACTION-HANDOFF-GUIDE-v1.md`; verify its answer count before clicking Update. An update/new chat may leave the GPT with no prior transcript context. That is context loss, not evidence that the historical interview never existed. Recover from the same saved chat, explicit attachment, or explicit canonical Library fallback; never overwrite a nonempty historical record with an empty candidate.

## Owner hotfix 2026-10-02.2 — approval explanation and durable review handle

The participant must be warned before the first Railway Action that ChatGPT will show one or more external-action permission cards and that **Allow once** is the expected approval for each step they choose to continue. Do not promise an exact count.

Before queueing, create both `life-patterns-candidate-backup.json` and `life-patterns-review-handoff.json`; the latter preserves the exact three-field request including `request_id`. After queue success preserve `life-patterns-review-receipt.json` when file creation is available. If `review_id` is lost later, replay the exact saved handoff body; server idempotency returns the existing review rather than starting another one.

## Owner hotfix 2026-10-02.3 — large recovered-record review

A `resource_limited / model_context_budget_exceeded` result is an execution limit, not a completed independent review. The Railway admission context now source-preservingly compacts planner-only redundancy while retaining every exact imported source turn, evidence item, addressed-route binding, and any proposed next question. The same existing review can be retried after deployment; do not create a replacement review ID.


## Owner hotfix 2026-10-03.1 — review wait UX

The approval prompt is now exactly **“Please click Allow on this tool call to continue.”** and may appear only once per Action call.

The review API returns `recommended_check_after_seconds`. New review passes use a 15-minute check-back target based on observed pilot runtimes; if a pass is still processing after that, the service recommends a shorter follow-up interval. This is a check-back estimate, not a promise of completion.

Custom GPTs cannot proactively notify the participant when an asynchronous review finishes. While a known review is pending, “continue,” “check,” “I'm back,” or another ordinary continuation message should automatically check that saved review. After a clarification answer is submitted, use the returned check-back interval; current owner-pilot metadata is about 1–2 minutes of model work, so the fallback is about 3 minutes rather than 15.


## Owner correction 2026-10-03.3 — restore information-based stopping

The one-clarification cap was an assistant-added latency workaround, not a requirement of the frozen protocol. It is removed. The independent reviewer may ask another clarification only when it remains admissible, nonredundant and materially useful after the newest answer. Coverage alone never justifies another question. A separate redesign is evaluating how to move expensive evidence coding off the clarification-decision critical path rather than reducing question intelligence.
