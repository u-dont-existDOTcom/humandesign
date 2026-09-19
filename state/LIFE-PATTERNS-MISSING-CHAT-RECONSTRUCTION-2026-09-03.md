# Life Patterns Missing-Chat Reconstruction — 2026-09-03

Status: reconstruction from canonical repository evidence. This is **not** a verbatim transcript of the missing ChatGPT/Work messages.

Canonical implementation branch: `codex/discover-life-patterns-mvp`

Canonical PR: #24 — `WIP: Discover Your Unique Life Patterns MVP`

Recovered implementation head before this reconstruction: `342a20d53baaff073d5df11ceeb14ff52fa9ddd2`

Parent baseline: PR #23 repaired AstroHD branch at `40154251534cffebaf7f2b78b48c5a97c707b629`.

## What is known with high confidence

The missing development thread did substantially more than add voice input to an existing Human Design interview. It reframed the participant-facing product into a theory-blind behavioral interview called **Discover Your Unique Life Patterns**.

The core product/scientific decision was:

1. elicit rich behavioral evidence without birth/chart/model access;
2. code and summarize it neutrally;
3. require participant review/correction;
4. later freeze the behavioral profile;
5. only after that allow HD, astrology, AstroHD, raw-astronomy, empirical, or baseline models to score the locked evidence.

The participant-facing experience should feel like a deep attentive interview, not a personality quiz. It should reward concrete episodes, nuance, contradictions, developmental change, context differences, and counterexamples rather than consistency with any theory.

## Likely reconstructed dialogue / decision sequence

The exact wording is unavailable. The sequence below is inferred from the roadmap, implementation commits, tests, and code boundaries.

### 1. Reframe the interview around participant value

The Human Design research interview needed a reason for participants to want to complete it even if the birth-derived theories fail.

The resulting product concept became **Discover Your Unique Life Patterns**.

North-star product value:

- high-resolution map of how a person actually operates across contexts;
- recurring and context-dependent patterns;
- decision tendencies;
- work/project conditions;
- relationship needs and interaction patterns;
- conflict/stress responses;
- learning/adaptation patterns;
- developmental changes;
- strengths and reliable strategies;
- recurring friction points;
- counterexamples and limits;
- transferable strategies already demonstrated elsewhere in the person's life;
- reversible experiments rather than identity prescriptions.

The product should remain useful even if every HD/astrology/birth-derived model fails.

### 2. Stop treating the interview as a fixed questionnaire

The interview should be conversational and adaptive rather than `N / total questions`.

The interviewer asks **one main question at a time** and reconstructs concrete real-life episodes.

Descriptive evidence areas are used instead of a completion denominator:

- Major decisions
- Work & projects
- Relationships
- Self-initiated actions
- Learning & adaptation
- Conflict & stress
- Life phases & transitions
- Counterexamples / exceptions
- Final pattern review

Coverage states are descriptive only (`not_started`, `developing`, `strong`, etc.) and are not a claim that a person can be scientifically completed by a fixed number of prompts.

### 3. Preserve strict scientific blindness

Before behavioral lock, the interviewer, mapper, and coach must receive **no**:

- birth data;
- Human Design chart/classification;
- astrology;
- hidden candidate classification;
- prediction;
- rank;
- model fit.

The interviewer may know a neutral measurement ontology, but must not choose the next question because it would help a hidden chart/model candidate.

Forbidden interviewer behavior includes:

- praising an answer because it resembles a candidate theory;
- mechanism reinforcement such as “your gut knows what's best”;
- pushing the participant toward a coherent self-story;
- treating good outcomes as proof that the preceding mechanism was correct;
- introducing HD, astrology, MBTI, Enneagram, attachment labels, or similar systems before lock.

The interviewer should instead welcome inconsistency, separate contexts, distinguish pre-outcome evidence from hindsight, and invite correction of overgeneralization.

### 4. Make the atomic evidence unit a real episode

The primary evidence unit became approximately:

`person -> domain -> episode -> mechanism/context -> counterexample -> participant-confirmed summary`

Episode capture may include:

- what happened / became possible;
- realistic alternatives;
- first reaction;
- timeline to commitment/action;
- explicit reasoning and information gathering;
- bodily sensations / energy;
- emotional changes and settling;
- speaking, advice, listening, permission, informing;
- self-initiation versus response to opportunity;
- environmental changes;
- values / identity considerations;
- will / commitment;
- urgency, stakes, reversibility, novelty, uncertainty;
- final tipping factor;
- outcome stored separately from pre-decision evidence;
- counterexamples and exceptions;
- observability / retrospective-confidence limits.

### 5. Require participant review before AI extraction counts as evidence

A major late correction in the thread was that AI-generated episode summaries cannot silently become research evidence.

The implemented rule is:

- AI extraction is provisional;
- the participant must **approve, edit, or reject** it;
- only approved episodes count toward evidence progress, Life Patterns Maps, exports, or coaching;
- edits are marked as participant revisions;
- rejected episodes remain auditable but do not count;
- the final fix at `342a20d5` makes review happen before the interview continues past the extracted episode.

### 6. Durable pause/resume and recovery

Pause/resume was treated as non-negotiable for a long interview.

Implemented / specified:

- save participant turns before external AI calls;
- hashed resume-token storage;
- email OTP recovery;
- normalized email used only for delivery;
- only a one-way email lookup hash stored in the research record;
- OTP hashes rather than plaintext OTPs;
- expiry, cooldown, issue-window, and attempt limits;
- successful recovery rotates the resume token;
- recovery responses avoid leaking whether an email/session exists.

### 7. Move toward a dedicated web app rather than Custom GPT as the long-term interview architecture

The roadmap explicitly records why: Custom GPT voice conversations do not support the custom Actions needed for reliable incremental saving.

Therefore the target became a dedicated web interviewer with:

`speech-to-text -> text interviewer -> text-to-speech`

initially, with possible Realtime/full-duplex voice later if pilots justify the complexity/cost.

### 8. Add correction-first voice input

Voice became the preferred eventual modality, but the project explicitly treats modality as a measurement variable rather than assuming voice is scientifically superior.

The implemented MVP is **correction-first push-to-talk**, not realtime duplex voice:

1. browser records audio;
2. authenticated audio is sent for transcription;
3. raw audio is not stored;
4. transcript is placed in the editable answer box;
5. participant reads/corrects it;
6. only then presses Send;
7. the saved turn records `input_modality = voice`.

The web UI also includes optional **browser-local speech synthesis** for interviewer replies, avoiding a paid TTS API for the MVP.

### 9. Build a participant-reviewed Life Patterns Map

The map is evidence-linked and neutral.

It can contain:

- patterns classified as stable, context-dependent, mixed, or tentative;
- confidence reflecting quantity/consistency of supplied evidence rather than certainty about the person;
- supporting episode IDs;
- counterexample episode IDs;
- contexts and limits;
- strengths;
- friction points;
- transfer opportunities;
- reversible experiments;
- important unknowns.

The mapper is forbidden from using HD/astrology/personality-system shortcuts and must not invent evidence episode IDs.

### 10. Add Pattern Transfer and read-only coaching

The missing thread appears to have expanded beyond measurement into immediate participant utility.

**Pattern Transfer** means identifying a strategy that already works in one domain and testing whether it transfers to another, e.g. reversible experiments in work versus rumination in relationships.

The resulting **Ask My Life Patterns Coach** mode is explicitly downstream utility.

Important boundary:

- coach reads the approved map + approved evidence;
- it cannot edit episodes or the map;
- coaching output does not become research evidence;
- the code hashes/compares the session state before and after coaching and raises if the supposedly read-only call mutated the research record.

### 11. Integrate with InnerSignal only through explicit user-controlled boundaries

The initial direction became one-way:

`Life Patterns evidence -> participant-reviewed Personal Pattern Profile -> consented InnerSignal context`

InnerSignal may read selected profile sections with consent, but must not silently write therapeutic interpretations back into research evidence.

Possible future updates from InnerSignal must be proposals requiring explicit participant approval.

The working principle recorded in the repo is:

> The personal model belongs to the participant; applications consume it with permission.

### 12. Preserve portability

The product should export:

- structured JSON profile;
- compact coaching-context Markdown;
- eventually granular domain-level exports / API access.

The interpretation boundary is historical tendencies, not fixed identity or destiny.

### 13. Keep relationship/couple mode and birth-model tournament downstream

Relationship mode was not part of this MVP.

Longer-term couple mode would compare two independently derived Pattern Models with both people's consent and identify interaction loops, complementary needs, conflict triggers, and negotiated protocols without deterministic compatibility typing.

Likewise, HD / astrology / AstroHD / raw astronomy / empirical birth-derived model comparison belongs only after behavioral measurement is stable enough to freeze.

## Exact implementation chronology recovered from PR #24

All times UTC, 2026-09-03.

- `026be220` 14:52:35 — docs: add Discover Your Unique Life Patterns roadmap
- `e0fbc5be` 14:53:53 — feat: add Life Patterns MVP interface
- `c55532f9` 14:54:59 — feat: add Life Patterns MVP backend
- `74737e80` 14:55:15 — feat: mount Life Patterns MVP behind feature flag
- `724bd82f` 14:56:01 — test: cover Life Patterns MVP value flow
- `5aefd577` 14:58:05 — test: mirror Life Patterns map minimum-evidence guard
- `eba48087` 15:19:58 — feat: add Life Patterns OTP recovery
- `cd505379` 15:20:50 — feat: add conversational Life Patterns interview UI
- `4c9b8818` 15:21:50 — feat: add adaptive Life Patterns interviewer
- `b59ee308` 15:22:01 — feat: mount conversational Life Patterns app
- `1d49dd04` 15:22:19 — docs: define Life Patterns and InnerSignal integration boundary
- `506648e3` 15:23:02 — test: cover conversational Life Patterns recovery and isolation
- `78db2901` 15:25:16 — style: fix Life Patterns interviewer lint
- `558e6cba` 15:25:55 — style: simplify Life Patterns interview tests
- `10c08928` 15:28:53 — feat: add participant episode review UI
- `70717f2f` 15:29:53 — feat: require participant review of extracted episodes
- `8dbd07e2` 15:31:14 — test: enforce participant-reviewed Life Patterns evidence
- `5ef81bfd` 15:34:14 — feat: add correction-first voice transcription
- `e1610b7c` 15:34:39 — feat: add push-to-talk Life Patterns UI
- `1e99815c` 15:35:09 — feat: attach voice controls to participant review UI
- `159147fb` 15:35:32 — feat: mount voice-enabled Life Patterns app
- `7a22b589` 15:36:08 — test: cover correction-first Life Patterns voice input
- `6e9ab702` 15:38:19 — feat: add evidence-grounded Life Patterns coach
- `c0adc824` 15:38:38 — feat: add Life Patterns Coach UI
- `57363a63` 15:38:56 — feat: attach coaching controls to Life Patterns UI
- `b90b75b9` 15:39:09 — feat: compose Life Patterns voice and coaching product
- `333d8615` 15:39:23 — feat: mount full Life Patterns product surface
- `2e398f02` 15:39:52 — test: prove Life Patterns coaching is read-only
- `342a20d5` 15:40:31 — fix: review extracted episode before continuing interview

## Current implementation state at reconstructed head

Implemented:

- theory-blind conversational interviewer;
- one-main-question-at-a-time policy;
- turn persistence before AI calls;
- provisional episode extraction with source-turn provenance;
- participant approve/edit/reject gate;
- descriptive evidence-area progress;
- Life Patterns Map;
- evidence-linked provisional reflections;
- hashed resume tokens;
- email OTP recovery and token rotation;
- push-to-talk STT with transcript correction;
- no raw audio storage;
- browser-local spoken interviewer replies;
- read-only Life Patterns Coach;
- JSON + Markdown export;
- InnerSignal one-way integration contract;
- feature flag `HDMATCH_LIFE_PATTERNS_ENABLED=1`;
- separate private store `HDMATCH_LIFE_PATTERNS_STORE`;
- mounted `/patterns` product surface when enabled.

CI at the reconstructed head passed:

- 368 passed, 6 skipped;
- Ruff passed;
- strict mypy passed on 131 source files.

## Deliberately not yet implemented / unresolved

- participant-reviewed immutable behavioral-profile freeze;
- pre-lock versus post-lock frozen provenance layer beyond episode review;
- full model-requirements manifest runtime;
- HD / astrology / AstroHD / raw-astronomy / empirical tournament on the locked profile;
- untouched-person validation design/execution;
- live InnerSignal database/API integration;
- reverse proposed-update flow from InnerSignal;
- relationship/couple mode;
- payment/subscription layer;
- full-duplex realtime speech-to-speech;
- empirical remaining-time prediction;
- production deployment / participant recruitment authorization.

## Scientific status

Development only.

The owner's case is a development/stress-test case, not untouched human-validity evidence.

No merge, deployment, participant recruitment, spending, or birth-model change was authorized by PR #24.

## What should happen next

1. Treat PR #24 / this branch as the canonical continuation point rather than the damaged chat history.
2. Audit the current PR #24 head before further changes.
3. Finish participant-reviewed behavioral-profile freeze and provenance boundaries before any birth-model scoring.
4. Pilot the product value / interview UX separately from claims about HD or astrology.
5. Measure whether voice actually improves evidence quality, spontaneity, completion, and participant satisfaction versus typed input.
6. Preserve every subsequent reasoning checkpoint / handoff in the repository so ChatGPT conversation-history loss cannot become a project-state failure again.

## Reconstruction confidence

**Very high** for implemented features, chronology, architecture, scientific boundaries, and product direction because they are directly encoded in repository commits, tests, docs, and source.

**Moderate** for the conversational ordering and exact user/assistant rationale between commits. That ordering is inferred from the implementation sequence and resulting artifacts.

**Unavailable**: verbatim missing user messages and assistant messages that are no longer exposed by conversation-history retrieval.
