# Life Patterns participant co-coding architecture — 2026-09-11

Status: owner-directed development architecture correction. Public-safe; contains no private participant text.

## Core correction

The final person-level Life Pattern is not to be inferred solely by an external human or automated classifier from a set of elicited episodes. The participant is the primary authority on whether a proposed recurring pattern actually characterizes them.

The classifier's role is narrower and more useful:

1. decompose concrete episodes into minimally inferential behavioral facts, reported appraisals, transitions, and outcomes;
2. notice potentially meaningful recurring structures or unanswered distinctions;
3. formulate precise, non-leading candidate-pattern questions for the participant;
4. preserve participant corrections, qualifications, exceptions, and alternative formulations;
5. recursively update the candidate pattern until the participant accepts, rejects, or leaves it unresolved.

This is collaborative pattern construction / co-coding, not unilateral trait inference.

## Episodes are elicitation anchors, not a frequency sample

Episodes collected because the system asked about a domain are selected evidence. Their repeated appearance is not intrinsically interesting as empirical frequency evidence and must not be treated as an unbiased estimate of recurrence.

Additional examples requested after a candidate pattern is proposed serve mainly to:

- clarify what the participant means;
- reveal conditions, mechanisms, exceptions, and sequence;
- test whether the proposed formulation matches remembered experience;
- generate better subsequent questions;
- expose contradictions or overgeneralization that the participant can adjudicate.

Producing several examples does not by itself make the pattern more important or establish population/opportunity frequency.

## Failure to produce examples can be informative

If a participant endorses a generalization but cannot produce any concrete example, preserve that discrepancy rather than forcing either the pattern or its rejection.

Possible explanations include weak episodic retrieval, a vague identity belief, low salience, privacy/reluctance, recency effects, misunderstanding, or limited self-observation. Do not infer 'lack of self-awareness' from one failure.

The system may probe the discrepancy directly, for example by asking whether the participant becomes less confident in the generalization, whether the pattern feels diffuse rather than episodic, or whether examples are simply hard to retrieve. If similar retrieval/awareness discrepancies recur across domains, that itself may become a candidate meta-pattern, but only through the same participant-adjudicated process.

## Recursive pattern loop

Preferred development loop:

`episode -> minimal factual decomposition -> candidate pattern hypothesis -> participant adjudication -> nuance/examples/counterexamples -> revised hypothesis -> participant adjudication -> ... -> accepted/rejected/unresolved pattern`

A candidate may therefore be refined recursively. A newly exposed nuance can itself be proposed back to the participant: 'I noticed X in the way you described these situations. Is X actually a recurring pattern for you?' The answer, not the classifier's inference, determines whether the person-level pattern is retained.

## Evidence roles

Keep separate:

- `episode_fact`: concrete fact supported by a bounded source episode;
- `reported_appraisal`: what the participant says they perceived, believed, wanted, feared, considered difficult/infeasible, etc.; do not convert this into an objective condition;
- `participant_pattern_endorsement`: direct self-report that a proposed generalized pattern is typical, conditional, exceptional, false, or uncertain;
- `example_or_counterexample`: participant-supplied instance used to refine meaning and boundaries, not automatically an independent frequency observation;
- `pattern_revision_history`: successive candidate formulations and participant corrections;
- `unresolved_discrepancy`: e.g. endorsement without retrievable examples, conflicting examples, or uncertain scope.

## Consequence for the codebook

The episode-level codebook should be only as complex as needed to preserve useful factual distinctions and generate good follow-up questions. It is not intended to be a complete taxonomy of personality traits.

Where possible, prefer decomposable factual dimensions such as:

- what happened / what action or choice state occurred;
- timing or sequence;
- reported appraisal or reason, explicitly attributed to the narrator;
- outcome or resolution;
- contextual qualifiers;
- absence claims only when the required opportunity/feasibility/nonoccurrence conditions are actually established.

Do not force an episode into an absence-dependent category merely because it is the closest named option. Preserve clear positive facts even when a stronger absence/counterfactual claim is not justified.

## Consequence for R05-type cases

A case may legitimately contain facts such as:

- choice was delayed or repeatedly delayed;
- narrator considered the proposed course too difficult, impractical, risky, costly, undesirable, etc.;
- narrator later accepted, rejected, revised, delegated, or otherwise resolved the choice.

The reported appraisal is a positive report about the narrator's perception and does not require an absence gate. A claim such as 'no resolution occurred despite a feasible opportunity' is stronger and does require the absence gate.

The downstream pattern question may then ask whether the participant generally delays choices under that kind of appraisal, what they normally do during the delay, what resolves it, and what exceptions exist.

## Calibration target changes

Human calibration should not be framed primarily as 'can an external human recover the one true person-level pattern label from stories.' Instead it should evaluate whether the system:

- extracts episode facts faithfully;
- separates reported appraisals from objective conditions;
- generates useful, non-leading candidate-pattern questions;
- preserves uncertainty rather than forcing labels;
- incorporates participant corrections exactly;
- distinguishes examples used for nuance from genuine generalized self-report;
- retains counterexamples and exceptions;
- produces a final pattern summary that the participant recognizes as accurate and properly scoped.

External human/automated coding can still be calibrated at the episode-fact layer. Person-level recurring-pattern authority is participant-adjudicated.

## Scientific boundary

This architecture remains theory-neutral. Candidate Human Design/AstroHD/astrology information must not influence episode decomposition, candidate-pattern generation, participant adjudication, or revision. Target-model comparison occurs only after the neutral participant-grounded pattern representation is frozen under the project's separate validation gates.
