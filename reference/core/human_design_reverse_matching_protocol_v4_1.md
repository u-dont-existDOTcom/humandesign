# Human Design Behavioral Reverse-Matching Protocol V4

## Iterative, Candidate-Blind, Trauma-Aware, Boundary-Exact

## 1. Purpose

Use Human Design as an experimental symbolic pattern-matching framework to rank candidate birth moments against a carefully constructed behavioral profile.

The intended long-term test is demanding: a person who provides a highly accurate, behaviorally specific profile should have their real birth moment rank unusually high within a declared candidate universe. The system must be designed so that this outcome cannot be manufactured by showing the person candidate charts and then editing the profile until one favored chart wins.

V4 therefore separates five tasks that must never be collapsed:

1. measuring whether the person can currently report relevant inner and bodily processes reliably;
2. constructing a holistic behavioral profile without seeing candidate charts;
3. calculating exact chart states and historical local-to-UTC conversions;
4. ranking candidate birth moments with frozen rules;
5. validating the result with concealed questions, holdout material, independent evidence, and prospective observations.

Human Design has not been scientifically validated as a method for recovering birth data from personality. Every output is an experimental rubric result, not proof of a person's true birth moment and not a probability unless empirical calibration has actually been completed.

## 2. What V4 fixes

V4 addresses six major failure modes.

### 2.1 Rank-guided profile correction

A person sees that their known or preferred date ranks lower than expected, is shown traits that would improve it, agrees with some of them, and the target is revised until the preferred date rises. Some corrections may be genuine, but the process is no longer independent.

V4 prevents this by hiding all dates, charts, candidate identities, and directional scoring effects until a profile version is frozen.

### 2.2 Trait conflation

Generic questions often confuse:

- capacity with motivation;
- participation with identification;
- behavior with outcome;
- state with trait;
- expertise with a desire for mastery;
- material competence with ambition;
- sensitivity with decision authority;
- introversion with Type;
- trauma responses with native decision phenomenology.

V4 forces these distinctions into separate observations.

### 2.3 False minute precision

A search can report a timestamp to the second even when every minute in a six-hour interval has the same scored chart. The displayed midpoint is then computationally precise but behaviorally arbitrary.

V4 reports exact stable intervals. It names a single minute only when a scored boundary or a validated finer-grained discriminator justifies that resolution.

### 2.4 Missed chart transitions

Sampling every few hours and refining only when bracket endpoints differ can miss short interior states or changes that cancel before the next sample.

V4 uses explicit boundary-event generation and root solving rather than relying solely on coarse endpoint comparison.

### 2.5 Trauma as a universal rescue explanation

It is plausible that dissociation, hyperarousal, fawning, or cognitive override can disrupt access to bodily signals. It is not legitimate to explain every mismatch as conditioning or trauma.

V4 uses trauma-related information only as a predeclared measurement-reliability modifier for questions that genuinely depend on present access to bodily or emotional signals. It never converts a mismatch into a match merely by invoking trauma.

### 2.6 Timezone non-identifiability

A Human Design chart is determined by the resolved UTC moment. Place is used to determine the historical civil-time offset. The same UTC instant produces the same planetary chart in every location.

Therefore an unbounded behavioral search can identify, at best, a UTC moment or interval. It cannot independently recover a unique timezone from personality. A local timezone can be reported only when:

- birthplace or location is supplied;
- a finite list of candidate zones is declared;
- or the timezone is part of a supplied candidate tuple.

If two local date/time/timezone tuples resolve to the same UTC instant, Human Design cannot distinguish them and they must tie.

## 3. Required epistemic language

Never say:

> This is your true birth date.

> The model is 98% sure this is your chart.

> Trauma proves why the chart seems wrong.

Prefer:

> Under the frozen symbolic model, this UTC interval ranks first among 1,000 blinded candidate tuples.

> The top result remains first in 94% of confidence-perturbation runs, but Human Design itself is not scientifically validated for birth-time recovery.

> Current dissociation or threat activation may make this particular body-signal question hard to answer, so it was marked unscorable rather than counted as a mismatch.

## 4. Search modes

### 4.1 Bounded candidate mode

Rank a supplied candidate file. This is the recommended prototype.

Minimum fields:

- opaque candidate ID;
- local date;
- local time;
- IANA timezone name;
- resolved UTC timestamp;
- ambiguity/nonexistent-time flags;
- optional stated time uncertainty.

The GPT must not know which candidate is real.

### 4.2 Blinded 1,000-candidate challenge

Create 999 decoys and insert one true tuple through an external blinding script. Shuffle all rows, normalize formatting, and keep the answer key outside the GPT conversation until ranking is frozen.

Use three difficulty levels:

1. **Uniform challenge:** decoys sampled uniformly across the declared UTC range.
2. **Architecture-matched challenge:** decoys enriched for the same broad Type, Authority, Profile, or center architecture as the true candidate.
3. **Near-neighbor challenge:** decoys concentrated around adjacent chart states on the true date and nearby dates, testing hour- and minute-level discrimination.

A random 1,000-candidate success tests broad discrimination. It does not by itself demonstrate minute precision. Near-neighbor and architecture-matched challenges are required for that claim.

### 4.3 Known-date rectification mode

When the person knows their date and place but not time, search every exact chart-state interval across the local civil day, including both folds of an ambiguous daylight-saving time.

### 4.4 Global UTC mode

Search every distinct chart state in a declared UTC range, such as the past 100 years.

A 100-year minute grid contains about 52.6 million minutes. This is computationally feasible with precomputation, but exact state segmentation is preferable because it is both faster and more accurate around boundaries.

### 4.5 Combined mode

Run the global search first, freeze it, then score any known or supplied candidate list independently. Never adjust mappings because the known birth data performs poorly.

## 5. The V4 state machine

The system must track an explicit phase and may not skip forward.

```text
PHASE 0  Scope, consent, and blinding setup
PHASE 1  Somatic-reporting readiness
PHASE 2  Open autobiographical collection
PHASE 3  Structured behavioral interview
PHASE 4  Contradiction audit and profile synthesis
PHASE 5  Freeze discovery target, holdout, mappings, and search universe
PHASE 6  Deterministic chart calculation and search
PHASE 7  Concealed active-discrimination questions
PHASE 8  Freeze finalists, reveal holdout, rerun full universe
PHASE 9  Robustness, boundary audit, independent-engine validation
PHASE 10 Result reveal and practical low-stakes experiment
PHASE 11 Claimed-birth-data disagreement procedure, if needed
```

A phase transition must be written to the audit record with a timestamp, profile hash, question-bank version, scoring-model version, and search-universe hash.

## 6. Phase 0: scope, consent, and blinding

Explain before questioning:

- this is an experimental symbolic reverse-matching exercise;
- the person may answer “unknown,” “varies,” or “not currently accessible”;
- they should not reveal known birth data if they want a genuinely blind test;
- the system will not diagnose trauma or mental illness;
- high-stakes medical, legal, financial, or safety decisions must not be based on the result;
- timezone cannot be inferred independently from UTC unless location or zone candidates are supplied.

Choose the search mode and create the candidate-universe commitment before profile scoring begins.

For a blinded challenge, store:

- candidate-file SHA-256;
- answer-key SHA-256 without exposing the answer;
- generation seed or cryptographic commitment;
- date range;
- candidate count;
- decoy sampling method;
- duplicate-state policy.

## 7. Phase 1: somatic-reporting readiness

### 7.1 Purpose

This phase does not determine the chart. It estimates whether current answers about bodily timing, emotional waves, gut responses, fear, tension, and immediate safety signals are likely to reflect a stable process or a state-distorted report.

The system must distinguish:

- signal absent;
- signal present but inaccessible;
- signal present but overwhelmed by threat noise;
- signal noticed only retrospectively;
- signal accessible in safety but not under interpersonal pressure;
- signal overridden by appeasement, urgency, or mental argument;
- genuinely inconsistent process.

### 7.2 Readiness domains

Ask non-graphic questions about the past month and about the person's calm baseline.

1. **Body access:** ability to notice hunger, fatigue, tension, warmth, contraction, expansion, or impulse before interpretation.
2. **Dissociative distance:** feeling unreal, detached, absent, outside the body, or noticing events only afterward.
3. **Threat amplification:** ordinary bodily cues frequently feeling like danger or urgency.
4. **Social survival override:** fawning, freezing, appeasing, or saying yes while the body appears to resist.
5. **Cognitive override:** a bodily response occurs, but reasoning repeatedly talks the person out of it.
6. **State stability:** the answer changes drastically with sleep, substances, conflict, pain, medication, or environment.
7. **Retrospective access:** the person can identify the body signal only after consequences occur.
8. **Low-stakes detectability:** the person can test signals on ordinary choices without danger or major cost.

### 7.3 Rating

Use a five-level measurement-reliability value, separate from behavioral confidence:

| Reliability | Meaning |
|---:|---|
| 1.00 | accessible, repeatably described, and supported by concrete examples |
| 0.75 | generally accessible with occasional noise or override |
| 0.50 | mixed access; usable only in some contexts |
| 0.25 | severe ambiguity, dissociation, threat noise, or retrospective-only access |
| 0.00 | currently unreportable; exclude from scoring |

Do not label these values as trauma severity.

### 7.4 Consequences

- Low reliability downweights or excludes only the affected observations.
- It does not add points to any chart.
- It does not excuse unrelated contradictions.
- It does not prevent the rest of the profile from being built.
- Authority may remain unresolved until prospective low-stakes observation is possible.

When severe distress, frequent depersonalization/derealization, danger, or functional impairment is reported, encourage evaluation by a qualified trauma-informed clinician. Do not state that Somatic Experiencing is required or uniquely indicated. Evidence-supported PTSD options may include CPT, PE, EMDR, and other clinician-selected treatments; body-oriented work may be an adjunct for some people, but evidence that it reliably restores interoceptive accuracy is limited.

## 8. Phase 2: open autobiographical collection

Before presenting structured trait alternatives, ask for unprompted material:

- childhood behavior before major adaptation;
- how important decisions were actually made;
- work and energy patterns;
- social entry and opportunity patterns;
- conflict and betrayal responses;
- learning and expertise development;
- money, status, comfort, and autonomy motivations;
- relationships;
- major life phases;
- bodily signals;
- times a self-description failed.

Ask for concrete episodes, not labels.

Good:

> Tell me about two major opportunities that worked and two that did not. Who initiated each one, what did you notice first, and what happened next?

Poor:

> Are you a Projector who needs invitations?

Good:

> Describe a field in which other people consider you highly knowledgeable. Did you intentionally pursue expert status, practice the skill for its own sake, or keep following a question until expertise accumulated accidentally?

Poor:

> Are you naturally talented?

## 9. Phase 3: structured behavioral interview

### 9.1 Question-writing rules

Every question must:

- use ordinary behavioral language, not Human Design terms;
- distinguish motivation, capacity, behavior, and outcome;
- specify context and timescale;
- permit “unknown,” “both,” and “context-dependent” when warranted;
- ask for at least one example before assigning confidence above 0.50;
- ask for examples from more than one life period before assigning 1.00;
- seek a counterexample or failure mode;
- avoid flattering, morally loaded, or obviously superior answer options;
- randomize answer-option order when possible;
- conceal which candidates or structures benefit.

### 9.2 Required distinctions

The interviewer must explicitly test these common confounds:

#### Capacity versus motivation

Someone may be persuasive without wanting to persuade, skilled without valuing mastery, able to lead without wanting leadership, or commercially effective without seeking advancement.

#### Participation versus identification

Someone may work inside a pharmacy, military, university, religion, or corporation without deriving identity or influence from conforming to that system.

#### Trait versus state

Ask separately about calm baseline, severe stress, intimate relationships, unfamiliar groups, work roles, and childhood.

#### Recognition versus passivity

Waiting for a clear opening is not the same as chronic avoidance, social fear, indecision, or learned helplessness.

#### Immediate body signal versus anxiety

A brief, quiet, nonrepeating signal must be distinguished from persistent worry, panic, urgency, attraction, spine tingling, or later rationalization.

#### Emotional wave versus mood instability

Time-dependent emotional clarity must be distinguished from dysregulation, trauma activation, bipolar symptoms, ordinary indecision, or changing facts.

#### Resources versus ambition

Valuing money, comfort, bargaining, enterprise, or strategic leverage is not automatically a drive for rank, prestige, promotion, or material ascent.

### 9.3 Repeated-form consistency checks

Revisit important constructs later using a different scenario. Record inconsistency rather than pressuring the person to choose a single identity.

## 10. Phase 4: profile synthesis and contradiction audit

Convert the interview into atomic observations. Each observation record must contain:

```json
{
  "observation_id": "OBS-0001",
  "behavioral_statement": "...",
  "contexts_where_true": ["..."],
  "exceptions": ["..."],
  "examples": ["..."],
  "counterexamples": ["..."],
  "life_periods": ["childhood", "adult"],
  "source_types": ["self_report", "independent_source", "prospective"],
  "behavioral_confidence": 0.75,
  "measurement_reliability": 1.00,
  "dependency_cluster": "CL-07",
  "state_sensitive": false,
  "body_access_sensitive": false,
  "holdout_eligible": true,
  "status": "discovery"
}
```

### 10.1 Behavioral confidence

Use the existing fixed levels:

| Confidence | Meaning |
|---:|---|
| 1.00 | repeated, specific, stable across periods or independently corroborated |
| 0.75 | clear and specific with more limited repetition |
| 0.50 | moderately supported, context-sensitive, or newly clarified |
| 0.25 | weak, tentative, generic, or single-example |
| 0.00 | unknown or excluded |

### 10.2 Effective confidence

For observations whose reporting is vulnerable to current state distortion:

```text
effective_confidence_i = behavioral_confidence_i × measurement_reliability_i
```

For ordinary externally observable behavior, measurement reliability normally remains 1.00.

### 10.3 Dependency control

Repeated descriptions of the same underlying mechanism belong to one cluster. Examples:

- original contribution, nonconformity, and influence through personal work may overlap;
- immediate bodily knowing and Splenic Authority cannot be counted as separate discoveries;
- expertise, depth, practice, and skill must not be multiplied without behavioral separation;
- social network, referrals, and relationship-mediated opportunity may form one cluster.

### 10.4 Profile audit

Before freeze, present the profile without any chart interpretation. Ask the person to mark each observation:

- accurate;
- inaccurate;
- incomplete;
- context-dependent;
- unsure.

For every correction, ask what concrete behavior was misrepresented. Do not suggest a chart-favoring replacement.

## 11. Phase 5: freeze record

Freeze before any candidate chart is inspected:

- target filename and hash;
- all atomic observations;
- confidence and reliability values;
- dependency clusters;
- discovery/holdout assignment;
- source hierarchy;
- allowed chart pathways;
- mapping directness;
- contradiction rules;
- prevalence parent hierarchy;
- search universe and hash;
- question-bank version;
- ephemeris version and files;
- timezone-database version;
- chart-engine version and commit;
- holdout seed;
- active-question policy;
- stopping rules.

Any later change creates a new version and requires a full rerun.

## 12. Discovery and holdout

Assign independent dependency clusters, not individual repeated sentences:

- 70–75% discovery;
- 25–30% holdout.

Stratify the holdout across architecture, decision phenomenology, social behavior, energy, profile-line behavior, and detailed structures.

The holdout must remain hidden until:

1. the profile is frozen;
2. the search has run on discovery evidence;
3. a finalist set and stopping rule have been frozen.

If the holdout was viewed before finalists were frozen, label it descriptive rather than confirmatory.

## 13. Chart meaning sources and mapping freeze

Use sources in this order:

1. primary or official Ra Uru Hu, Jovian Archive, or IHDS material;
2. established references that clearly follow standard definitions;
3. secondary sources only when the primary material is insufficient.

For every allowed mapping, save before search:

- exact behavioral observation;
- structural anchor;
- whether it is primary or corroborative;
- directness class;
- contradiction condition;
- source and quotation or paraphrase;
- dependency cluster.

Never create a mapping because a finalist happens to contain a gate, line, channel, Color, Tone, or Base.

## 14. Core architecture

Retain the V3 fixed core blocks unless a future preregistered study replaces them:

| Block | Weight |
|---|---:|
| Type + Strategy | 30 |
| Authority | 30 |
| Diagnostic Centers | 25 |
| Profile | 15 |

Authority is included only when decision phenomenology is reportable. If body-signal reliability is too low, mark the block unresolved and remove it from the denominator rather than guessing.

## 15. Detailed support and contradiction

Retain the V3 separation:

- support is not rarity;
- unsupported is not contradiction;
- missing a favored structure is neutral;
- direct opposing behavior may be penalized;
- alternative mechanisms are not added together;
- a channel and its component gates are not independent evidence;
- Incarnation Cross and its four cardinal activations are not independent evidence.

Use fixed salience and directness classes from the frozen protocol. Do not tune decimals for a preferred candidate.

For body-sensitive observations, replace `C_i` with effective confidence.

## 16. Symbolic information score

Until empirical calibration exists, the system may continue using rubric bits:

```text
raw_bits_j = -log2(prevalence_j)
info_bits_j = min(6, raw_bits_j)

evidence_bits_i = effective_confidence_i
                  × support_i
                  × info_bits_primary_anchor

contradiction_bits_i = effective_confidence_i
                       × contradiction_severity_i
                       × 4

NetInformation = Σ evidence_bits_i - Σ contradiction_bits_i
```

Call these **rubric bits**, never probabilities.

### 16.1 Important limitation

Rarity of a chart structure is not the same as predictive validity. A rare structure can earn many rubric bits even if the behavior-to-structure mapping has never been empirically tested.

## 17. Empirically calibrated scoring tier

The ultimate system should replace symbolic rarity weighting with blinded behavioral likelihoods learned from a preregistered dataset.

For answer or observation `a_i` and candidate structure `c`:

```text
LLR_i(c) = log2[P(a_i | c) / P(a_i | reference universe)]

CalibratedScore(c) = Σ effective_confidence_i × LLR_i(c)
```

Requirements:

- HD-naive participants;
- birth data recorded before interpretation;
- concealed chart assignments;
- independent train, validation, and test sets;
- regularization for rare structures;
- hierarchical modeling for dependent gates/channels/centers;
- out-of-sample calibration;
- publication of null and negative results.

Only this tier can support posterior probabilities, and only after explicit priors are declared.

## 18. Exact time and timezone engine

### 18.1 Civil time conversion

Use the current IANA timezone database with a recorded version.

For every supplied local time:

- require an IANA name such as `Europe/Istanbul`, not an ambiguous abbreviation such as `CST`;
- resolve the historical UTC offset;
- detect nonexistent spring-forward times;
- detect ambiguous fall-back times;
- evaluate both folds when the fold is unknown;
- preserve the exact supplied tuple and the resolved UTC result;
- flag uncertain pre-standard-time data.

### 18.2 Ephemeris

Use a high-precision ephemeris with local data files, not an undocumented fallback.

Recommended production standard:

- Swiss Ephemeris files based on JPL DE431 or a declared JPL ephemeris;
- recorded calculation flags;
- true/mean Node choice explicitly frozen;
- geocentric tropical longitude settings explicitly frozen;
- tests against an independent engine and official Human Design software.

Do not silently fall back to Moshier if the intended Swiss/JPL files are missing.

### 18.3 Design moment

Solve the Design timestamp by root finding the exact 88-degree solar-arc condition. Do not approximate it as a fixed number of days before birth.

Conceptually:

```text
find d < t such that
unwrap(SunLongitude(t) - SunLongitude(d)) = 88 degrees
```

Record root tolerance and verify the result independently.

### 18.4 Gate and substructure mapping

Freeze:

- zodiac-to-Rave-Mandala offset;
- gate order;
- gate boundaries;
- line boundaries;
- Color, Tone, and Base subdivisions if used;
- boundary inclusivity convention;
- planetary bodies included;
- Node convention;
- fixing rules;
- channel, center, Type, Authority, Profile, and Definition derivation.

### 18.5 Independent validation

Validate random samples and every finalist against at least one independent implementation. Compare:

- local-to-UTC conversion;
- Design timestamp;
- every planetary gate and line;
- substructure if scored;
- channels;
- centers;
- Type;
- Strategy;
- Authority;
- Profile;
- Definition.

Systematic disagreement invalidates the ranking until resolved.

## 19. Exact boundary segmentation

### 19.1 Why a minute grid is not enough

Evaluating every minute can miss a transition inside a minute and wastes computation during long stable periods. It also encourages arbitrary single-minute reporting.

### 19.2 Event-based method

For every scoring-relevant body and every required subdivision boundary:

1. construct a continuous unwrapped longitude function;
2. predict all possible crossings in the search interval;
3. bracket each crossing using maximum angular velocity bounds;
4. solve each crossing with a robust root finder;
5. include Design-side events induced through the exact 88-degree Design-time function;
6. union and sort all events;
7. evaluate a midpoint in each resulting interval;
8. merge adjacent intervals only when the complete frozen feature vector is identical.

### 19.3 Boundary completeness audit

Independently scan with a sufficiently fine grid and confirm that every detected feature change falls on the event list. Also test random interior points and intervals surrounding high-scoring candidates.

Do not rely on the rule “refine only if the endpoints differ.” Two or more interior changes can occur while endpoints appear identical.

## 20. What “to the minute” must mean

The system must report one of four statuses:

1. **Minute-stable:** every second within the reported minute has the same complete scored state.
2. **Minute-boundary:** a relevant transition occurs within the minute; report the exact second-level boundary and both adjacent states.
3. **Wider stable interval:** many minutes are behaviorally indistinguishable under the frozen model; report the full interval and do not pick a privileged midpoint.
4. **Substructure-sensitive:** finer Color/Tone/Base or other predeclared features change within the interval and have validated discriminating questions.

A chart may be mathematically calculable to a fraction of a second while the behavioral evidence supports only a six-hour interval. Report the weaker resolution.

## 21. Minute-level discrimination layers

Use layers in order. Do not jump to extremely flexible symbolism merely to force an exact minute.

### Layer 1: architecture transitions

Type, Authority, Centers, Profile, Definition, and complete Channels.

### Layer 2: activation transitions

Personality and Design gate/line changes, cardinal placements, Nodes, repeated gates, and material planetary activations.

### Layer 3: predeclared line-level behavioral distinctions

Only standard, sourced, behaviorally specific line meanings that were frozen before candidate inspection.

### Layer 4: advanced substructure

Color, Tone, Base, Variable, PHS, and Rave Psychology may provide finer time resolution. They may be used only when:

- the chart engine is independently verified to Base level;
- mappings are sourced and frozen;
- questions are concrete and concealed;
- the added layer improves held-out or prospective prediction;
- dependence on existing line/gate evidence is controlled;
- no post-search narrative mining occurs.

Adding thousands of subline labels without empirical calibration can make almost any person sound uniquely matched. Complexity is not validation.

## 22. Active question selection

After the discovery search, do not reveal candidate dates. Generate neutral questions that distinguish the leading candidate states.

### 22.1 Expected information gain

When calibrated answer likelihoods exist:

```text
IG(question) = H(current candidate distribution)
               - Σ_answer P(answer)
                 × H(candidate distribution | answer)
```

Choose the question with the greatest expected information gain after multiplying by expected answer reliability and subtracting burden.

Without calibrated likelihoods, approximate utility using:

- number of top candidates separated;
- rarity and independence of the differing structure;
- mapping directness;
- answerability;
- current measurement reliability;
- whether the question duplicates an existing cluster.

### 22.2 Eligibility rules

A discriminating question must:

- be written before the answer is known;
- conceal candidate direction;
- not mention dates, gates, channels, profiles, or chart labels;
- have behaviorally distinct answer options;
- ask for examples;
- allow uncertainty;
- be discarded if the person cannot reliably observe the construct.

### 22.3 Iterative loop

```text
score frozen candidates
→ identify unresolved high-value distinctions
→ ask one small neutral question set
→ freeze answers as a new version
→ rerun the entire declared universe
→ test robustness
→ repeat until stopping rule is met
```

Never rescore only the two favored finalists after adding an answer.

## 23. Stopping rules

Stop questioning when one of these occurs:

- no eligible unanswered question has material information value;
- the person is fatigued, dysregulated, or no longer giving reliable examples;
- the top result is robust and further questions only add dependent evidence;
- the remaining candidates are behaviorally indistinguishable under the current theory;
- the search cannot justify finer time resolution.

A defensible result may be a cluster or interval rather than one minute.

## 24. Robustness

For at least the top 20 candidates or all candidates in a small bounded pool, run:

### 24.1 Confidence perturbation

At least 1,000 runs, perturbing nonzero behavioral confidence and measurement reliability by a preregistered range.

### 24.2 Cluster ablation

Remove one dependency cluster at a time.

### 24.3 Mapping sensitivity

Predeclare conservative, standard, and architecture-heavy variants.

### 24.4 Source ablation

Compare self-report only, independently corroborated only, and prospective evidence.

### 24.5 Time sensitivity

Test:

- every adjacent exact boundary;
- ±1 minute;
- ±15 minutes;
- ±1 hour;
- ±6 hours;
- ±1 day.

### 24.6 Trauma-reliability sensitivity

Repeat with body-sensitive observations removed entirely. A result that exists only because one uncertain body-signal answer was heavily weighted is fragile.

## 25. Candidate-blind disagreement procedure

If the person later says, “My actual birth data is different,” do not immediately edit the profile to rescue it.

Follow this sequence:

1. lock and archive the original result;
2. verify the claimed record, place, historical timezone, and transcription;
3. add the claimed actual chart to a concealed comparison set under an opaque ID;
4. identify predeclared behavioral differences between the original winner and claimed chart;
5. ask neutral, behavior-first questions without revealing direction;
6. seek independent autobiographical or prospective evidence;
7. freeze a new target version;
8. rerun the entire original universe;
9. report whether the claimed chart rose, why, and how much post-selection information was introduced;
10. preserve both versions and do not erase the failed prediction.

Possible outcomes:

- genuine profile correction improves the actual chart on held-out evidence;
- birth record or timezone was wrong;
- the model remains wrong;
- several states remain indistinguishable;
- the known chart fits descriptively but was not recoverable prospectively.

All are legitimate findings.

## 26. Falsifiability protections

The system must never use these as automatic explanations of a miss:

- conditioning;
- Not-Self;
- trauma;
- unconscious Design;
- insufficient deconditioning;
- misunderstanding Strategy;
- wrong birth time.

Each explanation requires independent evidence and must make a new testable prediction. A miss remains a miss until the new prediction succeeds prospectively or on concealed holdout material.

## 27. Practical use after a result

After revealing the top chart, keep practical guidance simple.

1. Explain Type, Strategy, and Authority in ordinary language.
2. Present them as an experiment, not doctrine.
3. Begin with low-stakes, reversible decisions.
4. Ask the person to log the situation, initial body response, mental story, action, and later outcome before interpreting it.
5. Do not advise abrupt changes to medication, medical care, legal obligations, finances, housing, or relationships based on Human Design.
6. If body access is poor, focus first on safety, grounding, sleep, ordinary interoceptive literacy, and professional support rather than forcing an Authority signal.
7. Reassess prospectively after a declared period without rewriting failed predictions.

The official Human Design emphasis on Strategy and Authority can be preserved while adding the safety rule that a person who is dissociated or chronically threat-activated may need help distinguishing present-moment bodily information from trauma responses.

## 28. Output format

Every completed run must report:

```text
Search mode:
Candidate universe and hash:
Profile version and hash:
Ephemeris / timezone / engine versions:
Discovery rank:
Holdout rank:
Validated rank:
Core Architecture Fit:
Detailed Behavioral Support:
Evidence rubric bits:
Contradiction rubric bits:
Net rubric bits:
Meaningful contradictions:
Stable UTC interval:
Minute-resolution status:
Possible local-time representations:
Timezone identifiability status:
Boundary sensitivity:
Independent-engine status:
Confidence-perturbation rank:
Worst ablation rank:
Unresolved observations:
Post-selection revisions:
```

For a blinded candidate file also report:

```text
Row rank:
Distinct chart-state rank:
Duplicate UTC-state count:
Answer key still concealed: yes/no
```

Do not call a result validated if the holdout or answer key was exposed prematurely.

## 29. Recommended bounded pilot

The fastest credible prototype is:

1. generate a 1,000-row blinded candidate file with one sealed true tuple;
2. build the profile without birth data;
3. reserve 25% of dependency clusters as holdout;
4. score all candidates through a deterministic backend;
5. freeze the top 20;
6. ask 5–15 concealed high-information questions;
7. rerun all 1,000 candidates after every frozen batch;
8. reveal holdout;
9. perform robustness and exact boundary audit;
10. reveal the answer key.

Then repeat with architecture-matched and near-neighbor decoys. Only after repeated success should the project expand toward a full 100-year search.

## 30. Research roadmap

### Stage A: engineering validation

- reproduce official charts;
- pass exact boundary tests;
- verify timezone conversion;
- verify 88-degree Design root;
- establish deterministic outputs across platforms.

### Stage B: blinded candidate recovery

- HD-naive participants;
- 1,000-candidate pools;
- preregistered profiles and question banks;
- hidden answer keys;
- report rank distribution, not only successes.

### Stage C: minute rectification

- participants with documented minute-level birth records;
- near-neighbor candidates from the same day;
- line and substructure questions frozen before answers;
- exact-time recovery rate compared with chance.

### Stage D: global recovery

- full 100-year UTC universe;
- held-out participants;
- no chart-guided profile editing;
- independent replication.

### Stage E: practical decision experiment

Randomize HD-naive participants to actual Strategy/Authority, plausible mismatched Strategy/Authority, or generic embodied decision training. Track prospective outcomes and test whether trauma/dissociation moderates access without being used as a post hoc excuse.

## 31. Default V4 principle

The goal is not to make the known birthday win.

The goal is to create a procedure under which a true birth moment can win before anyone knows which candidate it is, while false results, unresolved intervals, and model failure remain possible and visible.

---

# V4.1 Addendum: Authority Scope, Transits, and Scheduled Delivery

Use `authority_and_transit_guardrails.md` as a normative extension of this protocol.

## Authority scope

Authority is a proposed decision process, not a long-range outcome predictor. A decision that is experienced as correct at the relevant time does not guarantee that a job, relationship, location, treatment, or commitment will remain favorable for years. When circumstances materially change, that is a new decision.

Do not describe all Authority as acute. Splenic and Sacral processes are present-oriented; Emotional Authority requires waiting for clarity; Lunar Authority requires its longer sampling process; other Authorities have their own mechanics. Teach the specific timing and never reduce every form to “trust your gut.”

All practical guidance must preserve ordinary due diligence, consent, contracts, medical care, legal duties, and safety. Begin with low-stakes, reversible prospective experiments and retain failed predictions.

## Transit interpretation

Transits are temporary symbolic conditioning or “weather,” not fate, instructions, or a replacement for natal Strategy and Authority. A transit brief requires deterministic timestamped data and must distinguish natal definition from temporary activation. If the data cannot be verified, give no chart interpretation.

## Scheduled delivery

The Custom GPT may respond manually to `TODAY` when its deterministic backend is available. It cannot itself run Scheduled Tasks. Supply the user with the regular-ChatGPT handoff prompts in `daily_hd_transit_task_prompts_v2.md`. Default to reminder-only mode unless a deterministic live transit source is available to the scheduled chat.
