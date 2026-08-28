# 31 — Dynamic Relationship Questionnaire

Status: development architecture for the separate relationship-validation track. This questionnaire does not alter natal V4.3 scoring or claim that Human Design/astrology predicts relationship outcomes.

**Noise-policy dependency (2026-08-28):** the core narrative/EIG architecture is intentionally inherited from Survey-v2, but relationship-specific retry, corroboration, stopping, reliability, and error-recovery policy remains provisional until the authoritative `SURVEY-V2-NOISE-AUDIT` is complete. Preliminary checkpointed Survey-v2 results supplied during development are strong (perfect answers: 100% top-1; one wrong classification: 98.344% top-1; 5% wrong: 96.555% top-1 with 99.104% true-candidate survival), but only completed checkpointed scenarios are authoritative. Do not copy unfinalized thresholds into the relationship module. The relationship outcome space also differs from natal birth-state recovery, so final Survey-v2 noise findings are an upstream design input, not automatic validation of relationship performance.

## Purpose

The earlier relationship work showed that a single `compatibility` or `chemistry` score destroys the distinctions needed to evaluate symbolic relationship models. Development cases required separate measurement of:

- physical attraction;
- partner-specific sexual desire;
- baseline libido;
- actual sexual satisfaction and dyadic chemistry;
- sexual habituation/novelty dependence;
- love/attachment versus Eros/in-love versus Storge;
- intellectual compatibility versus intellectual stimulation/self-expansion;
- conceptual comprehension/application;
- knowledge complementarity;
- communication quality versus communication abundance;
- mystical/spiritual salience, curiosity, and stimulation;
- visible theatrical drama versus serious conflict;
- repair difficulty;
- emotional readability versus internal emotional ease;
- autonomy versus engulfment;
- sexual jealousy versus romantic-priority jealousy;
- state changes with distance, cohabitation, attachment threat, or third parties;
- commitment and practical life fit.

The questionnaire converts those lessons into a reusable, chart-blind phenotype-capture instrument.

Normative files:

- `reference/relationship/relationship_outcome_rubrics_v1.json`
- `reference/relationship/relationship_dynamic_questionnaire_v1.json`
- `reference/relationship/relationship_blind_classifier_protocol_v1.json`
- `src/hdmatch/relationship/questionnaire.py`

## Reuse of the current dynamic Survey-v2 architecture

The natal Survey-v2 architecture uses narrative evidence rather than long fixed multiple-choice blocks, preserves `Other`/mixed/context/uncertainty, and uses frozen candidate-blind expected information gain for adaptive tie-breakers.

The relationship questionnaire reuses the same principles:

1. **Narrative first.** Ask what actually happened and preserve the answer verbatim.
2. **Frozen phenotype vocabulary.** A separate blind classifier maps narrative evidence to the complete relationship-outcome rubric rather than to whichever label would help the chart.
3. **Unknown remains unknown.** Low observability, religious/sexual constraints, language barriers, early relationship stage, or one-sided knowledge reduce confidence rather than being forced to neutral.
4. **Negative contrasts matter.** `Love was high but sex was poor`, `communication was good but there was little to talk about`, or `drama was high but serious conflict was rare` are deliberately preserved rather than averaged away.
5. **Adaptive questions.** Detailed modules are asked only when needed in development capture, or selected by frozen expected-information gain in validation mode.
6. **No true-chart access for the selector/classifier.** The selector receives anonymous prediction likelihoods; the classifier receives narrative plus the full rubric. Neither receives birth metadata or true-candidate identity.

The existing utility remains authoritative:

```python
hdmatch.search.adaptive.select_next_question
```

Its utility is:

```text
adjusted_utility = expected_information_gain * expected_reliability - burden
```

The relationship wrapper only filters the frozen question bank and supplies each question's default reliability/burden.

Until the upstream Survey-v2 noise audit is finalized, those default relationship reliabilities are **development placeholders**, not empirically calibrated error rates. Do not interpret `0.85`, `0.90`, etc. as measured classifier accuracy.

## Two operating modes

### 1. Development capture

Use this for retrospective development relationships or before inspecting a new partner's chart.

**Hard rule:** do not inspect the pair's chart/model predictions until the response record is frozen if the case is intended to be chart-blind development evidence.

Ask six broad anchors in this order:

1. `RRQ_TRAJECTORY_CONTEXT`
2. `RRQ_LOVE_EROS_DIRECTION`
3. `RRQ_SEXUAL_SYSTEM`
4. `RRQ_MIND_COMMUNICATION`
5. `RRQ_EMOTIONAL_AUTONOMY`
6. `RRQ_PRACTICAL_FUTURE`

These six questions are deliberately broad. One narrative answer can supply evidence for many axes, but the classifier scores only axes directly supported by the answer.

After the six anchors, `select_next_capture_question` asks only a follow-up whose target axes remain unresolved or whose frozen non-scored applicability flag was triggered.

Examples:

- sexual desire declined with familiarity -> `RRQ_SEX_HABITUATION`;
- virginity/religion/opportunity constrains behavior -> `RRQ_SEX_CONSTRAINTS`;
- love is strong but only one person is in love -> `RRQ_EROS_ASYMMETRY`;
- open relationship / jealousy / third party -> `RRQ_JEALOUSY_EXCLUSIVITY`;
- relationship easy at distance but difficult when close -> `RRQ_CLOSENESS_STATE_CURVE`;
- `intellectual compatibility` remains ambiguous -> `RRQ_COGNITIVE_DECOMPOSITION`;
- partner is quiet/opaque/language-limited -> `RRQ_DISCLOSURE_READABILITY`;
- high `drama` could mean playfulness or hostility -> `RRQ_DRAMA_CONFLICT_REPAIR`;
- trust/care/intimacy need separation -> `RRQ_TRUST_CARE`;
- ended relationship with several simultaneous strengths/weaknesses -> `RRQ_BREAKUP_COUNTERFACTUAL`.

This routing is chart-blind. It uses only question completion, unresolved axes, and non-scored applicability metadata.

### 2. Validation adaptive

Use this only after a relationship model and its anonymous candidate/decoy predictions have been frozen.

The adaptive selector may receive:

- anonymous candidate weights;
- frozen answer likelihoods for each unanswered eligible question;
- per-question expected reliability;
- per-question burden;
- frozen non-scored applicability flags.

It may not receive:

- either partner's birth metadata;
- true candidate identity;
- candidate rank;
- participant prose;
- classifier rationale/evidence spans;
- operator preference for which chart should win.

`select_next_validation_question` delegates to the existing general EIG selector. It does not implement a relationship-specific information-gain formula.

The upstream Survey-v2 noise audit determines the default policy family for handling noisy evidence (for example, whether/when corroboration, retry, backtracking, or altered stopping rules are justified). Relationship validation must then run its **own** noise simulation because relationship axes, candidate predictions, missingness, and classifier reliability are different.

## Why six broad anchors instead of 30 fixed questions

The development histories showed that a single answer often resolves multiple dimensions if the interviewer asks for direction and time course explicitly.

For example, one sexual-system narrative can distinguish:

- high physical attraction but low partner libido;
- extreme one-sided desire with decent mutual sex;
- high libido plus familiar-partner habituation;
- low initiation caused by religious/virginity constraints;
- good initial chemistry that deteriorates longitudinally.

A fixed 30-item block would repeatedly ask paraphrases of the same evidence and increase burden. The adaptive architecture instead spends follow-up questions on unresolved distinctions.

## Actor-specific structure

For every construct that can differ by person, preserve direction:

```text
A -> B
B -> A
```

This is mandatory for at least:

- physical attraction;
- sexual desire;
- sexual initiation/satisfaction;
- Eros/in-love;
- love/attachment;
- Storge;
- commitment intent;
- psychological intimacy/confiding;
- perceived responsiveness;
- internal emotional ease;
- autonomy/engulfment;
- sexual jealousy;
- romantic-priority jealousy.

Dyadic axes such as actual sexual chemistry, communication quality, shared interests, conflict, repair, and practical-life fit remain pair-level outcomes.

## Time and context are first-class

Do not score a relationship only at its remembered peak or average.

Preserve phase/context where material:

- early attraction;
- typical relationship phase;
- late/end-state;
- distance;
- reunion;
- cohabitation;
- high attachment activation;
- third-party sexual threat;
- third-party romantic-priority threat;
- religious/sexual constraint;
- economic/geographic stress.

A state-dependent curve is preferable to an average when the pair changes sharply with proximity or attachment threat.

## Sexual measurement rule

Never use `attraction` as a synonym for `sexual chemistry`.

At minimum separate:

```text
A physical attraction to B
A partner-specific desire for B
A baseline libido
B physical attraction to A
B partner-specific desire for A
B baseline libido
actual sexual satisfaction for A
actual sexual satisfaction for B
desire discrepancy
longitudinal desire stability
novelty/habituation when present
```

This allows a relationship to contain high attraction but poor sex, or asymmetrically extreme desire but mutually enjoyable sex.

## Cognitive measurement rule

Never score one `intellectual compatibility` axis from all mental observations.

Keep separate:

- reasoning compatibility;
- intellectual stimulation/self-expansion;
- conceptual comprehension/application;
- knowledge complementarity;
- communication quality;
- communication abundance;
- shared interests/commonality;
- mystical/spiritual salience;
- mystical/spiritual curiosity;
- mystical/spiritual stimulation.

Low output due to introversion/language/silence is an observability limitation, not proof of low comprehension or compatibility.

## Emotional/autonomy measurement rule

Keep separate:

- visible drama/theatricality;
- serious conflict/hostility;
- isolated aggression episodes;
- repair difficulty;
- emotional readability;
- internal emotional ease;
- baseline autonomy;
- engulfment pressure;
- sexual jealousy;
- romantic-priority jealousy;
- proximity/attachment sensitivity.

A single unusual episode must not redefine a generally peaceful relationship. The classifier preserves observed behavior separately from a respondent's causal explanation, whether that explanation is supernatural, psychiatric, medical, cultural, or otherwise.

## Classifier discipline

The blind classifier sees:

- the verbatim answer;
- frozen target axes;
- complete outcome rubric;
- minimum-evidence rule;
- relationship phase/context tags.

It does **not** see astrology or HD predictions.

Minimum classifier confidence is currently `0.65`, matching Survey-v2's existing development convention. Until the final Survey-v2 noise audit and a relationship-specific classifier reliability study are complete, this is a provisional inherited threshold rather than a calibrated optimum. Below threshold, or when direct evidence is inadequate, the axis remains unscored.

`unknown` is not `moderate`.

## Validation use

The relationship questionnaire can support several experiments without mixing their claims:

### R1 — retrospective development

Capture known histories consistently and refine model hypotheses. Performance on these same cases is training fit only.

### R2 — unknown-time relationship discrimination

Freeze predicted outcome labels for every stable partner-time state. The candidate-blind selector may adaptively choose questions that best split the anonymous surviving intervals.

### R3 — untouched pair prediction

Freeze HD/Western/AstroRRF and baseline predictions before an untouched pair answers. Classify the relationship phenotype blind, then score domain-level predictions.

### R4 — prospective state/context

Freeze a current pair's Time-0 profile and specific context-dependent predictions, then repeat selected axes at later windows without changing the initial predictions.

## Required freezes for validation

Before scored answers:

- questionnaire hash;
- outcome-rubric hash;
- classifier-protocol hash;
- classifier model/version/settings;
- confidence threshold;
- adaptive utility rule;
- per-question burden/reliability defaults;
- candidate/decoy prediction likelihood matrix;
- relationship-model hashes;
- birth-input/chart-feature hashes where applicable.

Before reveal/evaluation:

- verbatim response record hash;
- classifier output hash;
- selected-question sequence and utility log.

## No compatibility scalar

The output of this questionnaire is a **relationship phenotype vector**, not a score.

If an overall ranking is ever required for a separate user-facing decision task, explicit user weights must be supplied and sensitivity reported. That weighted decision layer is not part of relationship-model validation.
