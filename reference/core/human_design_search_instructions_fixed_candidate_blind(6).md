# Human Design Behavioral Reverse-Matching Protocol V3

## Architecture-First, Information-Weighted, Candidate-Blind

## 1. Purpose

Use Human Design as a symbolic pattern-matching framework to rank candidate birth moments against a behavioral target.

V3 is designed to answer three separate questions that must not be collapsed into one percentage:

1. **Core Architecture Fit** — does the chart match the target's strongest high-level predictions about Type/Strategy, Authority, Centers, and Profile?
2. **Detailed Behavioral Support** — how much of the full behavioral target is symbolically supported by the chart across all predeclared levels of structure?
3. **Discriminative Information / Rank** — how unusual is that agreement relative to all chart states in the searched universe?

Human Design is not scientifically validated as a method of recovering birth date from behavior. Scores are symbolic rubric outputs, not probabilities that a chart is the person's true birth chart.

Never say:

> “This chart is 97% likely to be the person's true birth chart.”

Prefer:

> “Core Architecture Fit 100/100; Detailed Support 93.4/100; Net Information 28.6 bits; rank 1/312,418 chart states.”

---

## 2. Why V3 separates fit from uniqueness

A chart can score 100/100 on a coarse architecture test while many other charts also score 100/100.

That is not a paradox. It means every coarse prediction was satisfied, not that the chart is uniquely perfect.

Therefore:

- **100 Core Fit** means all frozen core predictions are supported.
- It does **not** mean no other chart can fit equally well.
- A chart cannot score above 100 on Core Fit or Detailed Support.
- Uniqueness is expressed through **Net Information**, **rank**, **percentile**, and **robustness**, not by allowing percentages above 100.

---

## 3. Search modes

V3 supports:

### Global mode

Search all chart states in an explicitly requested UTC date range, such as the past 100 years.

Human Design planetary architecture is determined by the resolved UTC birth moment. Geographic location matters for converting a supplied local civil time to UTC, but there is no separate planetary chart for Istanbul versus Philadelphia at the same UTC instant.

### Candidate-file mode

Resolve every supplied date, time, place, and historical timezone in the candidate file to UTC, calculate the chart, and score it using exactly the same frozen V3 model.

### Combined mode

When both are requested:

1. run the global search first;
2. freeze global results;
3. run the candidate file independently;
4. report both;
5. compare the candidate-file winner with the global distribution.

Never change V3 because of candidate-file performance.

---

## 4. Candidate-blindness and versioning

Before examining any candidate chart:

1. freeze the behavioral target version;
2. freeze atomic behavioral observations;
3. freeze observation confidence;
4. freeze all allowed HD pathways;
5. freeze structural directness classes;
6. freeze contradiction rules;
7. freeze the search universe;
8. freeze the holdout seed;
9. freeze all formulas.

Every later change creates a new explicit version: V3.1, V3.2, etc.

If the behavioral profile is changed after seeing candidate charts, label the change:

**post-selection behavioral refinement**

Such a change may improve descriptive accuracy, but it is not independent confirmation of the candidate that motivated the question.

For stronger validation after post-selection refinement, use one or more of:

- new behavioral observations collected later;
- a concealed discriminating questionnaire where the user does not know which answer favors which chart;
- a held-out autobiographical source not used to create the rubric;
- prospective predictions frozen before the relevant behavior occurs.

---

## 5. Source hierarchy for Human Design meanings

Mappings should be derived from standard Human Design descriptions rather than improvised after candidate inspection.

Use this source order when possible:

1. official / primary Human Design or Jovian Archive material;
2. established reference material that clearly follows standard HD definitions;
3. independent secondary material only when the primary source does not provide sufficient detail.

Do not create a mapping because a finalist happens to contain a gate or channel.

For every scored pathway, record the textual rationale and source before the candidate search.

---

## 6. Extract atomic behavioral observations

Convert the target into conditional behavioral observations before looking at charts.

Good observation:

> “Important decisions can produce a brief immediate bodily safe/unsafe or correct/misaligned signal before reasoning, and the signal may not repeat.”

Poor observation:

> “Intuitive.”

Good observation:

> “Extended work can produce disproportionate depletion; concentrated high-output bursts require recovery.”

Poor observation:

> “Hard-working.”

Observations should be:

- behaviorally specific;
- conditional where context matters;
- separable from neighboring constructs;
- stated without HD terminology wherever possible;
- supported by the target rather than inferred from a desired chart.

Repeated descriptions of the same underlying behavior form one observation cluster and do not multiply the score.

---

## 7. Behavioral confidence

Assign each atomic observation one confidence value before chart inspection:

| Confidence | Meaning |
|---|---|
| 1.00 | repeated, specific, stable, or explicitly emphasized across contexts/time |
| 0.75 | clear and specific but based on fewer contexts or less repetition |
| 0.50 | moderately supported, context-sensitive, or somewhat interpretive |
| 0.25 | weak, tentative, generic, or newly reported without corroboration |
| 0.00 | unknown / do not score |

Confidence measures confidence in the behavioral description, not confidence in Human Design.

A newly added observation discovered after candidate inspection should normally begin at no more than 0.50 unless it is independently corroborated by pre-existing autobiographical material.

---

## 8. The four core architecture blocks

Core Architecture Fit is intentionally simple and standard.

Use four blocks:

| Block | Weight |
|---|---:|
| Type + Strategy | 30 |
| Authority | 30 |
| Diagnostic Center architecture | 25 |
| Profile | 15 |

Total = 100.

These weights are fixed across targets and are not adjusted because a particular behavioral profile makes one block seem more interesting.

### 8.1 Type + Strategy — 30 points

Infer the most strongly supported Type/Strategy prediction from the target.

Scoring:

- exact predicted Type/Strategy: 30
- behavior genuinely compatible with two types and candidate is one of the frozen alternatives: 24
- partial architectural compatibility without the predicted Strategy: 12
- neutral / insufficiently diagnostic target: exclude this block from the denominator before search
- direct opposite architecture: 0 plus contradiction evidence if warranted

Do not infer Type from generic introversion, productivity, sensitivity, or leadership preference.

### 8.2 Authority — 30 points

Use decision phenomenology only.

Scoring:

- exact frozen Authority prediction: 30
- genuinely predeclared alternative Authority: 24
- compatible but non-diagnostic authority: 12
- target does not describe decision phenomenology: exclude from denominator
- explicitly opposing decision process: 0 plus contradiction evidence

Authority should not be inferred from a single gate when the target directly describes a system-level decision process.

### 8.3 Diagnostic Centers — 25 points

Before search, list only center states that the behavior strongly predicts.

Do not score centers for which the target provides no diagnostic evidence.

If k center predictions are frozen, each receives 25/k points.

For each center prediction:

- exact predicted defined/undefined state: full credit
- explicitly allowed alternative: 75% credit
- neutral/ambiguous: no credit but no contradiction
- behaviorally opposing state: no credit plus contradiction only when the target clearly predicts the opposite process

Unspecified centers remain neutral.

### 8.4 Profile — 15 points

Infer line-level behavior before chart inspection.

If one exact Profile is strongly predicted:

- exact Profile: 15
- one correct line in the correct personality/design role: 7.5
- one correct line but wrong role/order: 5
- neither predicted line: 0

If only one line is genuinely predicted, score that line out of 15 and do not force a second line.

Do not select a Profile because it appears in a finalist.

---

## 9. Core Architecture Fit formula

Let B be the set of included core blocks.

```text
CoreFit = 100 × Σ earned_core_points / Σ available_core_points
```

CoreFit is bounded 0–100.

A 100 means every frozen core prediction was met. It does not imply uniqueness.

Report the exact decomposition.

---

## 10. Detailed behavioral pathways

After the core architecture is frozen, define detailed pathways for every atomic behavioral observation.

Every pathway consists of:

1. one **primary anchor**;
2. zero or more **independent corroborators**.

Alternative mechanisms remain alternatives. Do not require every plausible HD expression of a behavior.

Use:

> strongest coherent pathway + limited independent corroboration

not:

> sum every favorable keyword in the chart

---

## 11. Fixed structural salience classes

The following values are global V3 constants. Do not tune them by behavior or candidate.

| Structural class | Salience S |
|---|---:|
| Direct Type/Strategy architecture | 1.00 |
| Direct Authority architecture | 1.00 |
| Diagnostic center state / center relationship | 0.90 |
| Profile / specific Profile-line behavior | 0.85 |
| Complete channel | 0.80 |
| Personality or Design Sun/Earth gate/line | 0.75 |
| Definition pattern | 0.65 |
| Repeated gate or strongly thematic Node activation | 0.55 |
| Other prominent planetary activation | 0.45 |
| Ordinary hanging gate | 0.35 |
| Generic symbolism | 0.15 |

Incarnation Cross is derived from cardinal activations and must not receive a separate independent score if its component Sun/Earth placements are already scored.

A complete channel and its two component gates cannot all be treated as independent evidence for the same observation.

---

## 12. Fixed mapping-directness classes

For an observation-to-structure mapping, freeze one of four directness values:

| Directness | D | Rule |
|---|---:|---|
| Direct | 1.00 | standard HD meaning closely predicts the specific behavior/process |
| Strong | 0.75 | substantial conceptual fit, but not uniquely diagnostic |
| Plausible | 0.50 | compatible secondary symbolism |
| None | 0.00 | do not score |

Do not use arbitrary values such as 0.68, 0.73, or 0.91 for individual gates/channels.

The only continuous values in V3 should come from empirical prevalence and arithmetic, not hand-tuned symbolic preferences.

---

## 13. Detailed support for one observation

For observation i and pathway p:

```text
primary_support = salience(primary) × directness(primary)
```

For independent corroborators, calculate the same product and take only the strongest corroborator that does not depend on the same underlying structure.

```text
pathway_support = min(1.00,
                      primary_support
                      + 0.15 × strongest_independent_corroborator)
```

For alternative pathways:

```text
support_i = max(pathway_support_i1,
                pathway_support_i2,
                ...)
```

Do not add alternative pathways together.

This preserves the principle that one excellent mechanism can explain a behavior without requiring every synonymous channel/gate.

---

## 14. Detailed Behavioral Support score

For atomic observations i with confidence C_i:

```text
DetailedSupport = 100 × Σ(C_i × support_i) / Σ(C_i)
```

DetailedSupport is bounded 0–100.

It measures coverage, not rarity.

A 100 means every scored behavioral observation has a maximally supported frozen pathway. It does not mean the chart is unique.

---

## 15. Unsupported is not contradiction

For every observation keep support and contradiction separate.

A support value of 0.20 means little predeclared supporting structure was found.

It does not mean 80% contradiction.

Missing gates, channels, centers, or Profiles are neutral unless the chart positively predicts a meaningfully opposing behavioral process.

---

## 16. Contradiction scale

Use only:

| Severity | Meaning |
|---:|---|
| 0.00 | none |
| 0.25 | mild tension |
| 0.50 | meaningful tension |
| 0.75 | strong contradiction |
| 1.00 | direct major contradiction |

Contradiction must be justified in behavioral language.

Examples:

- target repeatedly says important decisions require waiting through an emotional wave, while the candidate's frozen direct-authority prediction is immediate;
- target clearly describes indefinitely sustainable Sacral-style workforce energy while the chart's architecture strongly predicts the opposite;
- target explicitly describes reliable internally generated will while the candidate architecture strongly indicates inconsistent/conditioned will, provided the HD mapping was frozen before search.

Non-examples:

- missing a favored channel;
- missing Gate 57;
- missing Gate 18;
- lacking one of several alternative pathways;
- lacking an incidental supporting gate.

---

## 17. Why rarity is a separate information calculation

A common structural match and a rare structural match can provide equal behavioral support but different discriminative information.

Example:

- matching a broad Type prediction may be behaviorally important but relatively common;
- matching a specific predeclared channel or cardinal configuration may be less foundational but much rarer.

V3 therefore calculates information separately from support.

Do not artificially inflate a match above 100%. Use information and rank to distinguish otherwise excellent charts.

---

## 18. Reference universe for prevalence

All rarity estimates must come from the global search universe, never from the candidate CSV.

For a 100-year search, prevalence is calculated across all chart states in that century.

Prefer **duration-weighted prevalence**:

```text
P(structure) = total UTC duration for which structure is present
               / total searched UTC duration
```

This is better than counting coarse samples because short-lived chart states should contribute proportionally to the amount of time they actually exist.

If exact state segmentation is computationally unavailable, use a sufficiently fine grid plus an exhaustive boundary audit, and label prevalence as approximate.

---

## 19. Exact chart-state segmentation

Preferred global implementation:

1. identify every timestamp at which a scoring-relevant planetary activation crosses a gate or line boundary;
2. include Design-side boundaries resulting from the exact 88° solar-arc Design moment;
3. derive any resulting channel, center, Type, Authority, Profile, or Definition transition;
4. partition the requested century into intervals within which every scoring-relevant chart property is constant;
5. evaluate one midpoint per interval;
6. weight prevalence by interval duration.

This eliminates the risk that a 3-hour or 15-minute grid skips a short high-scoring state.

---

## 20. Predeclared rarity anchors only

Never invent an ultra-specific conjunction after seeing a finalist.

Rarity may be calculated for:

1. an atomic frozen structure; or
2. a conjunction explicitly declared before search because the behavioral observation predicts that conjunction.

Post-search conjunction mining is forbidden.

Example allowed before search:

> “The target jointly predicts non-Sacral architecture, immediate Splenic Authority, and open emotional amplification.”

Example forbidden after search:

> “This finalist happens to have Gates 1, 8, 24, 26, 44, and 61 together, so calculate how rare that exact six-gate combination is.”

---

## 21. Conditional prevalence and dependency control

To avoid counting the same architecture twice, use conditional prevalence when a structure is downstream of an already scored structural block.

Preferred hierarchy:

```text
Type information:       P(Type)
Authority information:  P(Authority | Type)
Center information:     P(center signature | Type, Authority)
Profile information:    P(Profile | Type, Authority)
Channel information:    P(channel | frozen core architecture)
Cardinal information:   P(cardinal activation | frozen higher-level architecture)
Gate information:       P(gate activation | relevant higher-level architecture)
```

The exact parent set must be frozen before search and used for every candidate.

This means a channel receives credit for how much additional information it provides beyond the already-known core architecture rather than re-awarding the same rarity embedded in Type/Authority/Centers.

When a conditional reference group is too small, back off one parent level rather than using an unstable tiny denominator.

Use a minimum effective reference size of 500 duration-weighted state equivalents where possible.

---

## 22. Information bits

For a frozen structural anchor j with reference prevalence p_j:

```text
raw_bits_j = -log2(p_j)
```

Cap single-anchor information at 6 bits:

```text
info_bits_j = min(6, raw_bits_j)
```

The cap prevents extremely short or boundary-sensitive states from dominating the entire ranking.

For observation i using primary anchor j:

```text
evidence_bits_i = C_i × support_i × info_bits_j
```

An independent corroborator may add at most 15% of its own evidence bits, mirroring the support rule.

Alternative pathways are not summed; use the pathway with the highest legitimate evidence bits.

---

## 23. Structural reuse rule

The same exact structural anchor cannot be counted at full information value repeatedly because the behavioral target describes it in several ways.

If one anchor is the best explanation for multiple observations:

- group those observations into one dependency cluster before scoring; or
- give the anchor full information credit only once and allow at most 15% corroborative reuse elsewhere.

Examples:

- Projector Type and “wait for recognition” are one architecture, not two independent discoveries;
- Splenic Authority and a direct description of immediate non-repeating bodily knowing are one primary architecture;
- a complete channel and each of its component gates are not three independent pieces of evidence;
- an Incarnation Cross and its four constituent Sun/Earth gates are not independent evidence.

---

## 24. Contradiction information penalty

Contradictions are penalized in information units rather than arbitrary percentage points.

For observation i:

```text
contradiction_bits_i = C_i × contradiction_severity_i × 4
```

Maximum penalty from one observation = 4 bits.

If a contradiction comes from an especially rare, direct opposing architecture, report that fact qualitatively but do not raise the mechanical 4-bit cap.

This prevents one disputed symbolic interpretation from overwhelming the entire chart.

---

## 25. Net Information score

```text
NetInformation = Σ(evidence_bits_i)
                 - Σ(contradiction_bits_i)
```

NetInformation is measured in **rubric bits**.

It is not a probability and is not bounded by 100.

This is intentional: it is an information quantity, not a percentage.

A candidate with 31.4 rubric bits is not “131% compatible.” It simply accumulated more discriminative evidence than one with 27.8 bits.

---

## 26. Primary ranking rule

Rank candidates primarily by:

1. NetInformation;
2. then fewer meaningful contradictions (>=0.50);
3. then DetailedSupport;
4. then CoreFit;
5. then greater boundary stability.

Do not use an ad hoc coherence bonus.

Coherence should emerge naturally because several independent, correctly predicted structures contribute legitimate information.

---

## 27. Search percentile and ceiling index

After scoring the entire global universe, report empirical rank and percentile.

For N evaluated chart states with midrank r:

```text
SearchPercentile = 100 × (N - r + 0.5) / N
```

Also report duration percentile when exact interval durations are available.

Optionally report:

```text
InformationCeilingIndex = 100 × candidate_NetInformation
                          / highest_observed_NetInformation
```

Only use this if the highest observed NetInformation is positive.

The global winner receives 100 on this **relative index by definition**. Do not call it a 100% behavioral match.

---

## 28. Core-perfect tie handling

If multiple charts have CoreFit = 100:

Do not modify the core weights.

Do not award 101, 105, or 110.

Instead compare:

- DetailedSupport;
- NetInformation;
- contradiction count;
- exact global rank;
- duration of the high-scoring state;
- holdout performance;
- robustness.

This is the intended V3 solution to multiple “perfect” core matches.

---

## 29. Holdout procedure

Before chart search, divide independent behavioral dependency clusters into:

- 75% discovery;
- 25% holdout.

Use a recorded random seed.

Stratify when possible so the holdout contains evidence from more than one structural layer rather than accidentally holding out only gates or only core architecture.

Freeze the finalist set using discovery evidence only.

Then reveal holdout clusters.

Report:

- Discovery CoreFit
- Discovery DetailedSupport
- Discovery NetInformation
- Discovery rank
- Holdout support
- Holdout information
- Full validated score set
- Validated rank

Never alter mappings because of holdout performance.

---

## 30. Prospective discrimination procedure

When two finalists remain close and the existing target is ambiguous:

1. identify behaviors on which their frozen architectures make meaningfully different predictions;
2. write neutral, behavior-first questions without HD terminology;
3. conceal which response favors which chart;
4. collect answers before rescoring;
5. freeze those answers as a new target version;
6. rerun the whole global universe, not only the two finalists.

Do not ask leading questions such as:

> “Are you actually very good at persuasion, like Channel 26-44?”

Prefer:

> “When you deliberately try to persuade someone, how reliably can you identify what they value and adapt the presentation to them? Give concrete examples where it worked and where it failed.”

---

## 31. Newly reported somatic phenomena

Do not automatically reinterpret every bodily sensation as Authority.

When the target reports multiple somatic phenomena, separate them unless evidence shows they are the same process.

For example:

- a brief safe/unsafe or correct/misaligned signal used in decisions;
- a frequent spine-tingle associated with meaning, beauty, resonance, awe, or significance.

The second phenomenon should remain its own observation until its behavioral function is known.

Do not score it as Splenic Authority merely because it is bodily.

---

## 32. Cardinal placements

Personality Sun/Earth and Design Sun/Earth remain higher-salience detailed evidence, but they do not receive bespoke per-gate bonuses.

Use the fixed salience table:

```text
Sun/Earth gate or line salience = 0.75
```

Mapping directness comes from the frozen behavioral mapping.

The empirical rarity calculation then determines how discriminative the placement actually is.

This replaces V2-style manually selected 0.70–0.80 strengths for particular cardinal gates.

---

## 33. Channels and hanging gates

A complete channel:

- may be a strong direct pathway;
- has fixed structural salience 0.80;
- receives empirical information weight from its prevalence;
- is never mandatory merely because a behavior resembles the channel.

A hanging gate:

- may support a behavior;
- has lower fixed salience;
- can become more informative through cardinal placement or repetition;
- does not become a complete channel by interpretive enthusiasm.

Missing a channel remains neutral if another frozen pathway explains the behavior.

---

## 34. No free coherence bonus

V3 eliminates the V2 +3 coherence bonus.

Reason:

If several independent behavioral predictions converge on one chart, that convergence already raises:

- DetailedSupport;
- NetInformation;
- rank;
- robustness.

Adding another manually awarded coherence bonus would count the same success twice and reintroduce discretion.

---

## 35. Robustness tests

For at least the top 20 validated candidates, run:

### Behavioral confidence perturbation

At least 1,000 runs.

Randomly perturb nonzero observation confidence values by ±20%, bounded 0.10–1.00.

Do not perturb structural salience constants.

Report:

- median rank;
- 5th–95th percentile rank;
- % rank 1;
- % top 5;
- % top 10.

### Observation ablation

Remove each dependency cluster one at a time.

Report worst rank and median rank.

### Mapping sensitivity

Predeclare at least three reasonable mapping variants before examining finalists, for example:

- conservative: plausible mappings removed;
- standard: direct + strong + plausible;
- architecture-heavy: hanging-gate evidence capped at half ordinary value.

Do not create a sensitivity variant because it helps a preferred candidate.

### Time sensitivity

Test:

- ±15 minutes;
- ±1 hour;
- ±6 hours;
- ±1 day;
- exact adjacent scoring-state boundaries.

---

## 36. Boundary quality

For every finalist report:

- `boundary_stable`
- `boundary_sensitive`
- `cross_engine_disagreement`

A finalist is boundary-sensitive when a nearby transition materially changes:

- Type;
- Authority;
- Profile;
- defined Centers;
- complete Channels;
- a scored cardinal activation;
- or enough information evidence to change rank materially.

Report the exact stable interval around the candidate when available.

Do not silently average across a boundary.

---

## 37. Independent implementation validation

Before trusting a large V3 search:

verify against at least one independent implementation or calculator:

- local-time to UTC conversion;
- historical timezone handling;
- exact 88° solar-arc Design moment;
- gate and line mapping;
- channels;
- Centers;
- Type;
- Strategy;
- Authority;
- Profile;
- Definition.

Validate random samples and every boundary-sensitive finalist.

Systematic disagreement must be resolved before ranking.

Isolated boundary disagreement must be reported.

---

## 38. Candidate-file integrity

For CSV searches:

- preserve candidate ID and supplied birth information exactly;
- resolve historical timezone independently;
- record UTC;
- flag impossible or ambiguous civil times;
- never infer missing times;
- do not deduplicate two rows merely because they generate the same chart state;
- report both row rank and distinct-chart-state rank when duplicates exist.

Rarity information always comes from the global universe, not the CSV.

---

## 39. Required output for every finalist

Report:

- Rank
- Candidate ID if applicable
- Birth moment as supplied
- Resolved UTC
- Stable scoring interval if known
- Type
- Strategy
- Authority
- Profile
- Definition
- Defined / undefined Centers
- Material complete Channels
- Material hanging gates
- Personality Sun/Earth
- Design Sun/Earth
- Incarnation Cross, descriptive only if its components are already scored
- Core Architecture Fit and decomposition
- Detailed Behavioral Support
- Evidence bits
- Contradiction bits
- Net Information
- Search percentile
- Information Ceiling Index if used
- Discovery metrics
- Holdout metrics
- Strongest supported behavioral observations
- Weakly supported but non-contradictory observations
- Actual contradictions
- Boundary status
- Robustness result

Never summarize “weak support” as “mismatch.”

---

## 40. Minimum comparison table

For the top candidates, show at least:

| Rank | Candidate | CoreFit | DetailedSupport | NetInfo bits | Contradictions | Holdout | Robust rank |
|---:|---|---:|---:|---:|---:|---:|---:|

This prevents a single impressive-looking percentage from hiding why one candidate outranks another.

---

## 41. Interpretation priorities

When interpreting a result, prioritize in this order:

1. validated global rank;
2. NetInformation;
3. holdout performance;
4. robustness;
5. actual contradiction count;
6. DetailedSupport;
7. CoreFit;
8. symbolic narrative.

CoreFit comes late in this list because many charts can share the same broad architecture.

A 100 CoreFit with mediocre detailed rank is less compelling than a 95 CoreFit with exceptionally strong independent detailed information, unless the missing 5 points represent a genuine high-confidence contradiction.

---

## 42. What V3 deliberately removes from V2

V3 removes:

- target-specific family weights such as 5/4/3;
- individually hand-tuned pathway strengths such as 0.73 versus 0.68;
- manually awarded coherence bonuses;
- the assumption that a single 0–100 number can represent both behavioral coverage and uniqueness;
- candidate-set-based rarity;
- post-search conjunction mining.

V3 retains:

- conditional behavioral modeling;
- alternative pathways rather than cumulative requirements;
- direct Authority/Type/Center architecture priority;
- cardinal placements as higher-salience detailed evidence;
- neutral absence versus genuine contradiction;
- holdout validation;
- robustness testing;
- boundary sensitivity;
- independent implementation validation.

---

## 43. V3 validation standard

Do not judge V3 by whether a known preferred candidate rises to rank 1.

Judge it by whether:

- the same rule applies to every candidate;
- high-level architecture is scored mechanically;
- detailed mappings are frozen before search;
- structural salience is fixed rather than hand-tuned;
- rarity comes from the search universe rather than intuition;
- dependent evidence is not double-counted;
- rare conjunctions are predeclared rather than mined;
- holdout behavior predicts finalist performance;
- rank is stable under reasonable perturbations;
- boundary-sensitive results are exposed;
- post-selection behavioral edits are clearly labeled.

If a preferred candidate falls after these safeguards, do not change V3 to rescue it.

---

## 44. Recommended reporting language

Good:

> “Core Architecture Fit: 100/100. Detailed Support: 94.1/100. Net Information: 31.7 rubric bits. Validated rank: 2 of 284,901 distinct chart states. No meaningful contradictions. Rank 1 in 61% and top 5 in 97% of robustness runs.”

Good:

> “Two candidates both achieve 100 Core Fit, but Candidate A contains 4.6 additional bits of predeclared discriminative evidence and ranks higher globally.”

Bad:

> “Candidate A is 104.6% matched.”

Bad:

> “Candidate A is 97% likely to be the true birth chart.”

---

## 45. Freeze declaration

Before any V3 run, create and save a freeze record containing:

- target filename and cryptographic hash;
- rubric version and hash;
- date range;
- source list used for HD mappings;
- atomic observations;
- behavioral confidences;
- dependency clusters;
- allowed pathways;
- directness classes;
- contradiction rules;
- conditional-prevalence parent hierarchy;
- information cap;
- holdout seed;
- discovery/holdout assignment;
- implementation version / commit;
- ephemeris version.

Only after this record exists may candidate charts be calculated.

---

## 46. Default V3 constants

Unless explicitly changed before a run, use:

```text
Core weights:
Type + Strategy          30
Authority                30
Diagnostic Centers       25
Profile                   15

Behavior confidence:
1.00 repeated/specific
0.75 clear
0.50 moderate
0.25 tentative
0.00 excluded

Structural salience:
1.00 Type/Strategy
1.00 Authority
0.90 Center architecture
0.85 Profile
0.80 Complete channel
0.75 P/D Sun or Earth
0.65 Definition
0.55 repeated gate / thematic Node
0.45 other prominent activation
0.35 ordinary hanging gate
0.15 generic symbolism

Mapping directness:
1.00 direct
0.75 strong
0.50 plausible
0.00 none

Independent corroboration cap: 15%
Single-anchor information cap: 6 bits
Contradiction cap per observation: 4 bits
Holdout: 25%
Confidence perturbations: at least 1,000
Confidence perturbation range: ±20%
```

These constants are global defaults, not target-specific tuning knobs.

---

## 47. Primary V3 outputs

Every completed search should end with exactly these headline metrics:

```text
Core Architecture Fit:      __ / 100
Detailed Behavioral Support: __ / 100
Evidence Information:        __ bits
Contradiction Information:   __ bits
Net Information:             __ bits
Validated global rank:       __ / __
Search percentile:           __
Boundary status:             __
Robustness:                  __
```

For a candidate CSV also report:

```text
CSV row rank:                __ / __
Distinct CSV chart-state rank: __ / __
Global rank of CSV winner:   __ / __
```

These metrics replace the idea that one number should simultaneously mean “fit,” “rarity,” and “probability.”
