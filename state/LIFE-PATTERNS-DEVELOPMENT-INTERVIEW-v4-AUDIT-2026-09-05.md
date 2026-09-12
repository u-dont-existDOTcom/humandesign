# Life Patterns development interview: v3 re-audit and v4 decision

Date: 2026-09-05.
Disposition: use v4 for a short initial **development/pretest block**. Do not present it as a validated replacement for a full behavioral assessment. Preserve v1-v3 and any data already collected under them.

## Canonical input and scope

Fresh GitHub read: PR #24, `codex/discover-life-patterns-mvp`, head `bb0f69b77a1c45eae898be9193d1bec0807d4bbb`.

Audited file: `state/LIFE-PATTERNS-DEVELOPMENT-INTERVIEW-PROMPT-v3-2026-09-05.txt`, Git blob `bc3afa466866cdfb61a459e720cd0ed13c98f79c`.

Binding policy read: `docs/research/LIFE_PATTERNS_THEORY_BLIND_CONTENT_AUTHORITY_POLICY.md`, Git blob `92afaebaf8c70ea7f605ebe1822d1661d62fb7dc`.

This is a theory-exposed methods audit and a generic interview-process revision, not independent substantive construct development. It changes no frozen codebook definition, non-action classification, author-eligibility contract, scoring rule, or validation route. The clean interviewer must receive only the v4 interview packet, not this audit or the surrounding project conversation. The present participant has already seen the codebook and project discussion; a new interviewer context does not erase participant exposure. These data remain development-only.

No new model-performance claim underlies the recommendation. A newer model label does not validate an instrument, establish expected completion time, or prove coding accuracy.

## Independent conception snapshot, preserved before external-methods scan

Problem: reduce burden while keeping autobiographical evidence auditable, without choosing measurements to favor a target model.

Candidate mechanism: a bounded elicitation block followed by factual review; exact questions and participant source turns retained separately from later summaries/corrections. Sampling and source provenance matter more than a guessed episode quota.

Candidate changes recorded before searching: remove named targets; do not hardcode non-exposure; replace 'spontaneous' with an accurate elicitation label; distinguish recent-event sampling from selected autobiographical stories; use a content-independent workload cap; prevent fabricated quotations/approvals/persistence claims; preserve unknowns, partial exports, and withdrawal control. A dedicated text snapshot was written locally before the web scan and is preserved separately with this audit.

## Bounded existing-work scan: adapt and compose, do not reinvent

| Established work | Reusable contribution | Not solved by that work here |
| --- | --- | --- |
| CDC/NCHS cognitive interviewing [1] | Evaluate understanding, recall, response process, and question problems; retain participant feedback. | Does not validate this six-invitation protocol or its codebook. One owner pilot is not a full cognitive-interview study. |
| U.S. Census Bureau Standard A2 [2] | Balance quality and burden; pretest revised instruments with respondents; test wording, skip logic, usability and outputs. | Census operational requirements are not asserted to be legal requirements of this private project. An expert audit alone is not participant pretesting. |
| Pew Research Center question-design guidance and its open-ended burden analysis [3,4] | Open-ended wording and question order matter; avoid presenting response categories before the broad questions; measure burden rather than assume it. | Does not supply a validated duration or optimal number of stories for this interview. |
| Kahneman et al., Day Reconstruction Method (2004) [5] | Anchor some recollection to recent ordinary activity rather than only salient lifetime stories. | The v4 three-part recent-day module is a loose adaptation, not a full DRM, experience-sampling study, or representative time-use sample. |
| W3C PROV [6] and existing repository provenance infrastructure | Distinguish source entities, transformations, responsible agents, and derivations; retain versions. | A prompt or LLM-generated checksum cannot establish machine-verified provenance, consent, historical truth, or immutable storage. No new provenance ontology is needed. |
| Chan et al. witness-interview experiment [7] | Additional reason to prohibit suggested missing details and leading reconstruction. | This experiment used misleading questions after a crime video, not this life interview or GPT-6 Pro. Its numerical effects must not be transferred to this task. |
| Official OpenAI memory/Temporary Chat documentation [8,9] | Context isolation is a product/setup issue, not something a prompt can certify. Preserve output deliberately. | Generic training exposure and limited safety context are not disproved by isolation. Platform behavior can change. |

Decision: **adapt/compose** established elicitation, pretesting, recent-event anchoring, and provenance practices. Reuse the repository's frozen codebook and downstream validation machinery. Do not invent a new trait framework or new agreement metric.

## Findings and changes

### 1. V3 supplied the names it claimed to withhold

V3 explicitly names Human Design and astrology in its prohibition while hardcoding `target_theory_information_available_to_interviewer: false` in the export. An instruction not to use a named theory is not evidence that the name was unavailable. This also conflicts with the policy's stricter authorship/coding blind wording.

V4 removes named target theories from the interviewer-facing packet and replaces automatic non-exposure certification with explicit context-provenance status. It does not claim an independently blinded prompt author or uninformed participant. This fixes an identifiable exposure channel, not all possible contamination.

### 2. 'Spontaneous' was too strong a label

V3's broad section also asks about different periods, other people, ordinary incidents, and unexpected outcomes. These are elicitation cues. More seriously, the interviewer has the entire 13-probe bank in the same prompt before asking broad questions. The 13 event forms overlap heavily with existing codebook prerequisites. Such coverage targeting can be appropriate for a stress test, but is not independent discovery of behavior or a natural-prevalence sample.

V4 labels its first three invitations `broad_invitation`. It then uses three explicitly marked `recent_time_anchor` slots. No situation-specific probe bank is included in the core packet. The original 13 probes remain preserved in v3; they may be used later only as a separately identified extension. Fixed ordering protects the broad block from prior situation probes but does not randomize or causally identify elicitation-mode effects.

### 3. Burden and stopping were unsupported

V3 says 45-75 minutes is typical without observed timing data. Its stopping rule still calls for 7-10 broad episodes plus every fixed probe and a subjective redundancy judgment. 'Redundant' is not a reliable stopping criterion for estimating repeated behavior: it can remove repetition needed to assess within-person variation.

V4 attempts six invitations once each, unless the participant stops earlier. It normally allows no more than two short factual follow-ups per invitation. Missing examples do not trigger replacement slots. These are transparent workload choices, **not empirically optimized thresholds or a claim that six episodes are sufficient**. No new numerical completion-time promise replaces the old one. A participant can impose their own stopping time.

Tradeoff: the first block is intentionally too small to cover all 22 observables or assess 208 subcodes. It tests whether the collection/review/transfer process works before imposing the full workload. Additional participants, contexts, and targeted cases will still be needed for reliability and validation.

### 4. The sample needed some ordinary recent activity

V3 invites memorable lifetime episodes and selected situation examples. V4 adds early/middle/late anchors to the preceding waking day to include ordinary material and make retrieval more concrete. The purpose is to reduce exclusive dependence on salient selected stories, not eliminate recall bias. Unrecallable or uncomfortable periods remain missing. An alternative day supplied by the participant is recorded as an alternative, not silently substituted.

### 5. Source preservation was incomplete

V3 records the main eliciting question and participant segments, but does not explicitly require every follow-up question or the exact approval context. A leading follow-up can change evidence even when the opening question is neutral. 'Yes' cannot be interpreted safely without the question it answered.

V4 retains interviewer questions, participant turns, factual review drafts, and approval/correction references. It separates original elicitation from review-added detail. A quotation can be copied only from accessible text. Unavailable source text stays unavailable rather than being reconstructed. Participant approval establishes that the record reflects the participant's account, not independent historical verification.

### 6. Partial participation and withdrawal needed first-class handling

V3 requires all candidate episodes to be reviewed before final output and requests retention of rejected records. That is not enough for tired participants, partial review, or a request not to include sensitive material.

V4 supports pause/finish/skip, unreviewed partial exports, and a distinct withdrawal marker. Rejection does not become approval. Withdrawal omits the narrative from later exports; the prompt does not pretend to delete earlier copies or platform history. Interview nonresponse is process metadata and never a substitute for real-life non-action evidence.

### 7. Prompt instructions are not an implementation guarantee

V4 deliberately calls the export a transfer copy pending verification. It does not assert canonical bytes, computed hashes, durable storage, automatic schema compatibility, or an immutable research freeze. It uses a new transfer format because provenance and partial-review semantics changed. An importer must be explicitly checked/adapted before accepting v4 data into existing research artifacts; no existing schema is silently widened here.

## What stays unchanged

The evidence remains first-person reported episodes. Follow-ups seek factual gaps, not desired trait values. The non-action safeguard, preservation of participant nuance and uncertainty, prohibition on inferred motives, distinction between chronology and stated influence, and separate factual review remain. No substantive ontology content is rewritten. No human benchmark requirement is newly imposed. No claim is made that repeated LLM agreement proves correctness.

## Pilot acceptance questions, not invented success thresholds

After the first block, inspect whether the participant understood the requests; whether follow-ups repeated answered questions or introduced content; whether source references are recoverable; whether explicit review decisions are preserved; which questions were declined or difficult; and actual participant-reported effort/time. Keep process feedback separate from autobiographical codes.

Mechanical checks can catch missing IDs, incomplete exports, and impossible approval states. They cannot validate the historical account or establish coder agreement. The first real participant run remains necessary. Do not replace it with another speculative prompt-generation cycle.

Any v3 interview already started must be retained with its version and breakpoint. Do not ask the participant to discard or repeat it merely to obtain a cosmetically uniform v4 dataset. Mixed-version and post-review extension material require explicit provenance.

## Scope of this delivery

Prompt and audit artifacts only. No web-app runtime code, deployment, merge, participant records, paid model calls, target-model execution, or calibration results were created. PR #24 remains the work branch. The previous v3 file is retained unchanged.

## Sources (primary/official)

[1] CDC/NCHS, Cognitive Interviewing: https://www.cdc.gov/nchs/ccqder/question-evaluation/cognitive-interviewing.html

[2] U.S. Census Bureau, Statistical Quality Standard A2: https://www.census.gov/about/policies/quality/standards/standarda2.html

[3] Pew Research Center, Writing Survey Questions: https://www.pewresearch.org/writing-survey-questions/

[4] Pew Research Center, Why do some open-ended survey questions result in higher item nonresponse rates than others? (2021): https://www.pewresearch.org/decoded/2021/10/14/why-do-some-open-ended-survey-questions-result-in-higher-item-nonresponse-rates-than-others/

[5] Kahneman D, Krueger AB, Schkade DA, Schwarz N, Stone AA. A survey method for characterizing daily life experience: the day reconstruction method. Science. 2004;306:1776-1780. DOI: 10.1126/science.1103572. https://pubmed.ncbi.nlm.nih.gov/15576620/

[6] W3C PROV-Overview: https://www.w3.org/TR/prov-overview/

[7] Chan S et al. Conversational AI Powered by Large Language Models Amplifies False Memories in Witness Interviews. 2024 preprint. https://arxiv.org/abs/2408.04681

[8] OpenAI, Temporary Chat FAQ, checked 2026-09-05: https://help.openai.com/en/articles/8914046-temporary-chat-faq

[9] OpenAI, Personalizing ChatGPT, checked 2026-09-05: https://openai.com/academy/personalization/
