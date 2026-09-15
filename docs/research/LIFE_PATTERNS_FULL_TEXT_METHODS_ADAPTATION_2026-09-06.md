# Life Patterns: full-text interviewing-methods review and adaptation

Date: 2026-09-06
Status: development implementation; not a new codebook, validation result, merge, or deployment.
Baseline inspected: PR #24, `codex/discover-life-patterns-mvp`, `0ab5cf12f4c907274da51e75477d7b4410a81d40`.

## Decision and scope

Retain pattern-first, age-aware, evidence-anchored interviewing. Adapt established responsive interviewing, cognitive pretesting cautions, autobiographical-memory methods, and measurement boundaries. Do not invent another behavioral taxonomy or combine every book's recommendations into one interviewing method. The source-availability snapshot is the baseline implementation and prior MI applicability memo, not a claim to independent theoretical invention.

The review inspected relevant full-text sections of four supplied books and one chapter. It did not read all five sources cover to cover. No book text, original book files, participant narratives, identifying details, or private interview exports are included in this repository contribution.

### Sources actually supplied and inspected

1. Herbert J. Rubin and Irene S. Rubin (2012), *Qualitative Interviewing: The Art of Hearing Data*, third edition. Selected sections of chapters 6–10, especially chapters 9–10 on main questions, probes, and follow-up questions; printed pp. 143–169 for sequence, follow-up selection, and explanatory interviewing.
2. Gordon B. Willis (2005 copyright in the supplied edition), *Cognitive Interviewing: A Tool for Improving Questionnaire Design*. Selected introductory/cognitive-model sections, chapter 8, "Avoiding Probing Pitfalls," and sections on analysis and evaluation, including finding versus fixing problems. The filename's 2004 date is not used as the edition copyright date.
3. Roger Tourangeau, Lance J. Rips, and Kenneth Rasinski (2000), *The Psychology of Survey Response*. Selected sections of chapters 1–5 and 7, particularly pp. 23–61 on comprehension and pragmatics; pp. 69–83 on generic/event memory; pp. 93–99 on cues; and the temporal-question and frequency discussions.
4. Ana Lucía Córdova-Cazar and Robert F. Belli (2019), "Calendar and Time Diary Methods," chapter 69 in Pranee Liamputtong (ed.), *Handbook of Research Methods in Health Social Sciences*, pp. 1219–1236. The uploaded PDF is this 18-page chapter, not the entire handbook and not the previously recommended 2009 edited volume. Especially sections 3.1–3.2, pp. 1225–1227.
5. Robert F. DeVellis and Carolyn T. Thorpe (2022 copyright/cataloging date in the supplied edition), *Scale Development: Theory and Applications*, fifth edition. Selected reliability/validity discussions and chapter 7, "The Index," especially pp. 188–191. The filename's 2021 date is not used as the edition copyright date.

PDF/EPUB text was readable without performing new OCR. Some supplied text has extraction artifacts, so chapter/section locators and explicit printed pagination are preferred to fabricated e-reader locations. Findings below are paraphrases; implementation choices are our adaptations, not endorsements or validations by the authors.

## Source findings and bounded adaptations

### 1. Responsive questions are purposeful, not an interrogation checklist

Rubin and Rubin distinguish main questions, probes, and follow-ups. Their follow-up discussion attends to relevance, missing pieces, unclear concepts, overbroad claims, and apparent contradictions, with attention to whether to follow up now or later. [1, chs. 9–10]

Adaptation: select one useful conversational move rather than demand a main answer, example, and exception for every domain. Let a relevant account finish. A follow-up should resolve a material uncertainty in the participant's actual statement. For a conditional claim, evidence for one branch does not support the other. A counterexample must oppose the same scoped proposition; an action and a feeling can coexist.

Not imported: Rubin and Rubin also describe proposing explanations, alternative reasons, and tentative themes for interviewees to react to. [1, pp. 168–169] That may suit their explanatory qualitative work; it is not neutral source generation for this project's first-pass behavioral measurement. The runtime prohibits supplying unreported motives or alternative causal stories and soliciting endorsement. The books' research philosophies are not silently treated as identical.

### 2. Clarification can itself create a problem

Willis warns that speculative probes, demands for definitions/paraphrases, and excessive probing can produce artifacts rather than identify a defect in the original question. He favors selective probing and distinguishes finding a problem from fixing it. [2, ch. 8; evaluation discussion]

Adaptation: distinguish confusing wording, uncertain memory, an inapplicable premise, and a decision not to answer. Simplify a material question or move on rather than make the participant pass a comprehension test. Do not ask them to imagine exceptional cases solely to criticize the instrument. Spontaneous usability feedback remains welcome. No think-aloud or cognitive-testing battery is added to ordinary intake.

A second adaptation is a small process log. A material gap may remain open, be answered, be genuinely unknown, be declined, be left unasked for burden, or be judged immaterial. These are model-reported process states, not diagnoses, psychological codes, or evidence-quality scores. The log makes omissions inspectable; it cannot establish that the model judged a gap correctly.

### 3. Remembering a pattern is not inferior by definition to retrieving an exact incident

Tourangeau and colleagues discuss generic knowledge and event-specific information as distinct parts of autobiographical memory. Generic patterns may be easier to retrieve; the book reports an experiment in which forcing specific-only recall disrupted retrieval. It also describes a converse error: reporting a usual pattern when asked about a particular reference period. [3, pp. 69–83, especially pp. 70 and 78]

Adaptation: preserve remembered series, particular incidents, estimates, general impressions, and secondhand accounts separately. Do not fabricate a bounded episode from an account of what usually happened. Do not demand a date just to upgrade a support label. This does not remove evidence prerequisites from the frozen codebook, establish that self-reports are true, or make one story proof of recurrence.

Pattern-first is also not pattern-assuming. No consistent pattern, variability, uncertainty, and inapplicability must all remain permissible responses.

### 4. Conversational context affects interpretation

Tourangeau and colleagues discuss presuppositions, shared meaning, prior-question effects, and limits of flexible interviewing. Shared agreement does not guarantee the intended concept was measured, and flexibility can increase burden. [3, ch. 2, especially pp. 50–61; ch. 7]

Adaptation: preserve the intended scope when rephrasing rather than substitute a different question. Keep each older answer paired with its actual preceding interviewer turn in bounded working context. An answer such as "sometimes" cannot be interpreted without knowing what it answered. The preceding turn is recorded as context, not automatically labeled the unique eliciting question when several participant turns follow it.

Implementation additionally preserves a separate tail excerpt, original length, offsets, and content hash when a long context entry is clipped. The original transcript is unchanged. A prefix and tail are never represented as a contiguous quote. Omitted text is a context-availability limit, not evidence that the participant omitted a fact. Full text still is not guaranteed to fit the model's context.

### 5. Life landmarks can help without inventing developmental precision

The calendar chapter describes conversational flexibility and top-down, sequential, and parallel autobiographical cues. Tourangeau and colleagues also discuss periods, landmarks, relative order, and uncertain dating. [4, sections 3.1–3.2; 3, chs. 3–4]

Adaptation: reuse a participant-supplied place, relationship, school/work period, or other landmark when a material historical distinction needs clarification. Accept relative ordering and age ranges. Do not assume a universal school age or life sequence. An earliest recalled example does not establish onset. A cue is not independent corroboration.

No exhaustive calendar, new childhood cutoff, recovered-memory exercise, or compulsory recent-day module is added. The reported benefits of full calendar instruments are not attributed to this light conversational adaptation.

### 6. Measurement utility is not the same as pleasant conversation or uniform answers

DeVellis and Thorpe distinguish reflective scales, formative indices, and cases better treated as discrete indicators. They explain why internal-consistency procedures cannot automatically evaluate a heterogeneous index. [5, ch. 7, pp. 188–191]

Adaptation: the existing behavioral codebook is not promoted to a unitary personality scale. No overall score, alpha threshold, weighting, item deletion, or discrimination estimate is introduced. A common-sounding answer is not necessarily useless, nor does a clear answer demonstrate validity. Reproducibility, informative differences, applicability, redundancy, and participant burden still require actual empirical evaluation.

Frequency wording is retained without silently converting "often" or "usually" into numbers. Estimates and enumerated counts are separate, and a few recalled occasions do not supply the full opportunity denominator. [3, chs. 2 and 5]

## Implemented engineering changes

- One consolidated conduct policy replaces the prior inline policy. It retains useful MI-informed neutrality and listening constraints rather than appending incompatible instructions.
- Interviewer-facing policy and fixed opener do not name the external theories. This removes an avoidable clue, not general model knowledge, participant exposure, or developer exposure. Participant-facing study disclosures are not suppressed.
- Source-linked context retains 24 recent full turns and up to 80 participant entries. Each entry includes its actual preceding interviewer turn when available. Prefix limit remains 1,200 characters, with a separate nonoverlapping tail of up to 400 characters and explicit truncation metadata.
- The fixed first question is stored for newly created sessions, so it is not merely invisible UI text. Existing sessions are not backfilled or relabeled.
- Structured clarification notes cite existing participant turns. Unknown, assistant-only, duplicate, and future references are rejected. Notes append to assistant turns; a bounded latest-state view does not rewrite earlier notes.
- Invalid generated note references fail safely after the participant message has been saved. They are not silently repaired into a usable source.
- Notes are available in authenticated session/turn responses and in the next model context. The API labels them `model_reported_interview_process_not_behavioral_evidence`; no new participant-facing note editor is claimed.
- Real provider receipts include the interviewing-method version and prompt hash. Provider model configuration remains unchanged. The generated-output cap increases from 2,200 to 3,200 tokens to accommodate structured notes; actual cost/latency has not been measured.
- New sessions use `life-patterns-conversation-v4`; the standalone v8/v8.1 collection artifacts and their schemas remain unchanged.

## Boundaries that remain

This is a development adaptation authored in the project context, not a retrospectively theory-blind authorship claim or a validation-candidate release. Existing records are not relabeled as collected by the new method.

Participant-approved episodes still exclusively feed the existing map and evidence counts. Repeated-series statements remain in the conversation; this change does not implement a separate reviewed series-to-map pipeline. The research freeze's source selection and frozen schemas are unchanged. The new clarification log is not a comprehensive full-transcript research export and does not certify every important gap was found or answered.

The existing review/map/export flow remains in place. This patch does not implement automatic end-to-end interview termination/export, independently judge semantic note accuracy, provide unlimited history retrieval, or establish how a real LLM will follow every instruction. No live provider calls, recruitment, target-model comparisons, or deployment are needed to run the added tests.

## Verification and evaluation

The two new test files use synthetic content only. Unit tests cover pairing, exact excerpts/hashes, context omissions, distinct dispositions, append-only history, and invalid references. Integration tests exercise real ASGI routes with mock interviewers, new/legacy session behavior, message preservation on failure, evidence separation, and the provider request boundary without a network call. Prompt-invariant tests verify the instructions are present, not that an LLM obeys them.

Local helper verification: 28 tests passed. Full repository CI is recorded separately in the implementation receipt, so this memo does not predeclare success.

For later behavior evaluation, compare the frozen baseline method with this method on the same authorized development or synthetic cases, without inventing participant replies. Review concrete differences: unsupported additions, unnecessary questions, missing clarification, wrong gap disposition, lost qualifiers, false contradictions, and burden. Useful synthetic cases include a clear recurring series with no dated memory, a relative-age statement, a declined detail, an already-answered question, a conditional claim with only one evidenced branch, and a long answer whose final sentence limits the opening generalization. Synthetic/mocked checks alone cannot establish reduced real burden or measurement validity. No new numerical evaluation scale is declared here.

## Repository and privacy disposition

Keep the source books and private extraction files outside the public repository and downloadable implementation bundle. Preserve the completed v8 and v8.1 participant records, original codebook, amendments, and prior interview versions. Save only original implementation, synthetic tests, and this source-located review. No merge, deploy, model scoring, or scientific validation promotion is performed.
