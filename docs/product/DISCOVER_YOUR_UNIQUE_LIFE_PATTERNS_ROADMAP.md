# Discover Your Unique Life Patterns — Product & Research Roadmap

Status: active product direction, development branch only. No merge/deployment authorization.

Parent baseline: PR #23 repaired AstroHD branch at `40154251534cffebaf7f2b78b48c5a97c707b629`.

## North star

Build an intrinsically useful, theory-blind behavioral interview that people want to complete because it gives them a high-resolution, evidence-backed map of how they actually operate across contexts. Birth-derived models are downstream consumers of the locked behavioral evidence; they never guide the pre-lock interview.

Participant-facing name: **Discover Your Unique Life Patterns**.

The product should feel like an unusually attentive interview, not a personality quiz. It should reward specificity, nuance, counterexamples, developmental change, and context differences rather than rewarding consistency or resemblance to Human Design, astrology, or any other theory.

## Core scientific separation

1. **Behavioral elicitation** — no birth/chart/model access.
2. **Neutral behavioral coding** — no birth/chart/model access.
3. **Participant review and behavioral-profile lock** — no birth/chart/model access.
4. **Independent model tournament** — only after lock.

The interviewer may know the neutral measurement ontology and the union of evidence requirements needed by candidate model families, but it may not know which model/chart prediction would benefit from a particular answer.

## Unit of evidence

Primary unit:

`person -> domain -> episode -> observed mechanism/context -> counterexample -> participant-confirmed summary`

Avoid global forced categories such as one universal decision style. Sample concrete episodes and explicitly preserve cross-domain differences.

### Episode reconstruction

Capture, where applicable:

- what became possible or happened;
- realistic alternatives;
- first reaction before deliberate interpretation;
- timeline from first reaction to commitment/action;
- information gathering and explicit reasoning;
- bodily sensations/energy;
- emotional changes and settling;
- conversations, advice, listening, and speaking aloud;
- environment changes;
- values/identity considerations;
- will/commitment;
- external opportunity/request/invitation;
- social obligations, decision rights, permission and coordination;
- urgency, stakes, reversibility, novelty and uncertainty;
- who was affected;
- final tipping factor, if any;
- outcome recorded separately from pre-decision evidence;
- counterexamples and exceptions;
- retrospective confidence/observability limits.

## Interviewer behavior

Allowed and encouraged:

- warm curiosity;
- reflect the participant's experience accurately;
- validate specificity and nuance;
- explicitly reward useful counterexamples;
- notice differences between contexts;
- periodically summarize and ask the participant to correct overgeneralizations;
- ask how patterns changed across life phases;
- say that inconsistency across situations is useful data.

Examples:

- “That's an important distinction. Let's keep the business example separate from the relationship example.”
- “That's useful detail. What was different about that period of your life?”
- “You just gave me a counterexample to the earlier generalization; those exceptions are valuable here.”
- “I think I may be making this too simple. Let me reflect it back and you tell me what is wrong.”

Forbidden before behavioral lock:

- mentioning or hinting at the participant's HD/astrology/chart classification;
- praising an answer because it resembles a candidate theory;
- statements such as “your gut knows what's best,” “that's very Projector,” or equivalent mechanism reinforcement;
- selecting the next prompt because it would discriminate the hidden birth candidates;
- retroactively treating good outcomes as proof the preceding mechanism was correct.

## Participant value proposition

The interview should provide useful value even if every birth-derived model fails.

### Personal Life Patterns Map

A participant-reviewed report containing evidence-linked sections such as:

- stable recurring patterns;
- context-dependent patterns;
- decision tendencies;
- work/project conditions;
- relationship needs and interaction patterns;
- conflict/stress responses;
- learning/adaptation patterns;
- developmental changes;
- strengths and reliable strategies;
- recurring friction points;
- counterexamples/limits;
- potentially underused strengths or strategies that transfer across domains;
- current hypotheses/experiments;
- confidence and episode provenance for each claim.

The profile must treat patterns as historical tendencies, not destiny.

### Pattern Transfer

Identify successful strategies already used in one domain that may be underused elsewhere. Example: someone handles career uncertainty through reversible experiments but handles relationship uncertainty through rumination. Suggest testing the already-demonstrated strategy rather than prescribing a generic personality solution.

### Situation sense-making

For later coaching mode, compare a current problem with prior evidence-linked patterns. Example: identify that direct commands from close partners repeatedly trigger autonomy conflict, then help separate the practical request from the interaction pattern.

Prefer evidence-backed explanations over unverifiable causal stories.

### Personalized experiments

Prefer reversible experiments over fixed identity advice. Track whether an intervention changes outcomes and propose profile updates rather than silently changing the locked research record.

### Portable profile

User-controlled exports:

- human-readable report;
- structured JSON;
- compact AI coaching-context Markdown;
- later: consented API/export for InnerSignal or other coaching/journaling tools.

Exports should be granular. Participants may export only selected domains rather than their entire life-history transcript.

## UX and completion

### Product copy

Lead with **Discover Your Unique Life Patterns**, not AstroHD.

Explain that this is a deep interview, not a quick personality quiz; concrete examples, differences and contradictions are valuable.

### Voice

Voice is the preferred eventual mode because it may support more spontaneous, less polished narratives, but modality is itself a measurement variable and must not be assumed superior without data.

Store `input_modality = voice | typed` for research.

Current Custom GPT voice cannot be the long-term primary architecture because voice conversations do not support the custom Actions needed for reliable incremental saving. Target architecture: dedicated web interviewer using modular STT -> text reasoning -> TTS initially, with optional Realtime later if benefits justify cost.

Cost target: approximately $1–$2 per 75–120 minute modular voice interview initially; measure real billing during pilots.

### Pause/resume

Non-negotiable:

- autosave every finalized participant turn;
- visible Saved/Saving state;
- explicit Pause for now action;
- cross-device resume;
- durable recovery that does not depend on remembering one secret session key;
- target: email OTP plus optional backup recovery code;
- email/recovery identity stored separately from behavioral research payload;
- secure HTTP-only browser session after authentication;
- resume at exact unfinished interview point.

### Progress

Never display a questionnaire-completion denominator such as `37/81 questions`.

Show neutral evidence areas, for example:

- Major decisions
- Work & projects
- Relationships
- Self-initiated actions
- Learning & adaptation
- Conflict/stress
- Life phases/transitions
- Counterexamples & exceptions
- Final pattern review

States: `not_started`, `developing`, `strong`, `needs_counterexample`, `review_ready`.

Progress is guidance, not a claim that a fixed number of prompts scientifically completes a person.

After enough interaction, show an empirical remaining-time range based on the participant's observed pace. Do not promise a fixed time until pilot data exist.

## Model-requirements manifest

Theory-blind does not mean theory-ignorant instrument design.

Each candidate model family declares neutral observables it requires. The interview targets the union of those observables without seeing the participant's model predictions.

Flow:

`model family requirements -> neutral measurement ontology -> chart-blind interview -> behavioral lock -> model scoring`

Maintain an open residual prompt for important recurring patterns not anticipated by any model.

## Model tournament roadmap

Every model has a manifest status:

- `confirmatory_predeclared`
- `development_only`
- `exploratory_posthoc`

Candidate families:

1. context-only/non-birth baseline;
2. Human Design;
3. conventional astrology;
4. current AstroHD synthesis;
5. alternative HD + astrology combinations;
6. continuous/raw astronomy representation;
7. HD + continuous astronomy;
8. astrology + continuous astronomy;
9. empirical birth-derived model;
10. larger hybrid models after appropriate regularized development.

Possible astronomy-first inputs include continuous planetary longitudes/latitudes, declinations, angular separations, velocities, retrograde/direct motion, local sidereal/horizon geometry and smooth periodic transformations. Avoid granting traditional sign/house/aspect discretizations privileged status merely because they are conventional.

Model evaluation should include:

- predictive accuracy;
- reverse-match discrimination/ranking;
- behavioral coverage (how much meaningful evidence the model can even address);
- calibration where applicable;
- complexity/overfitting penalty;
- untouched-person validation after model development.

## Research participant boundaries

The owner's case is a development/stress-test case because the owner is helping design the instrument. Do not describe it as untouched human-validity evidence. This does not assume the owner knows their chart.

Perform contextual refinement before model reveal for every participant, not only after a model mismatch. Model-guided mismatch exploration belongs only after the confirmatory behavioral lock and is explicitly exploratory.

## Product roadmap

### MVP 0.1 — intrinsically useful text-first product

Goal: prove that people value the behavioral product before voice/model scoring.

Build:

- participant-facing Discover Your Unique Life Patterns web surface;
- chart/birth-independent session creation;
- conversational text interview with chart-blind interviewer policy;
- durable turn saving;
- evidence-area progress;
- pause/resume using current secure token mechanics, with browser persistence and backup recovery affordance while email OTP is built;
- periodic neutral reflective summaries;
- on-demand/current-profile Life Patterns Map from accumulated evidence;
- evidence-linked claims and counterexamples;
- JSON export;
- Markdown coaching-context export;
- no birth/chart/model scoring or model-driven next-question selection.

### MVP 0.2 — recovery and voice

- email OTP recovery and token rotation;
- modular STT -> text interviewer -> TTS;
- transcript review/correction;
- modality metadata;
- empirical time-remaining estimates;
- voice/text switching within the same session.

### MVP 0.3 — participant-reviewed behavioral lock

- episode-level structured coding;
- coverage/counterexample auditor;
- cross-context synthesis;
- participant correction interface;
- immutable behavioral-profile freeze;
- pre-lock vs post-lock provenance.

### MVP 0.4 — coaching value

- Pattern Transfer suggestions;
- “What am I not seeing?” discrepancy analysis between self-story and episode evidence;
- current-situation comparison against past episodes;
- reversible personal experiments;
- experiment outcome tracking;
- separate mutable coaching profile layered over immutable research freeze.

### MVP 0.5 — portability / InnerSignal

- granular user-controlled exports;
- compact AI coaching context;
- explicit import contract for InnerSignal;
- later bidirectional proposed-pattern updates with user approval;
- no silent cross-product data sharing.

### MVP 0.6 — relationship/couple mode

With both people's consent, compare independently derived Pattern Models and identify interaction loops, complementary needs, conflict triggers and negotiated protocols. Keep this evidence-grounded rather than deterministic compatibility typing.

### Research 1.0 — model tournament

Only after the behavioral measurement system is stable enough to freeze:

- model-requirements manifests;
- predeclared model roster;
- HD, astrology, AstroHD, astronomy-first and baseline adapters;
- development/validation split;
- locked reveal comparison;
- prospective real-world decision logging/EMA layer.

## Commercial hypothesis

The participant should pay for or eagerly complete the experience because the Life Patterns Map and coaching utility are useful by themselves. Birth-model reveal becomes an additional curiosity/research payoff rather than the sole incentive.

Potential paid offerings:

- deep Life Patterns interview + permanent report;
- ongoing Life Patterns Coach;
- periodic profile update interviews;
- relationship/couple Pattern Map;
- InnerSignal integration;
- model-tournament/birth-model reveal as an optional research feature.

## Immediate implementation boundary

Current implementation branch: `codex/discover-life-patterns-mvp`.

PR #23 remains untouched, draft and unmerged. Nothing on this roadmap authorizes merge, deployment, participant recruitment, spending, or use of real participant data.
