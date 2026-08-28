# 29 — AstroRRF Dyadic Desire + Commonality V0.3

Status: **retrospective development architecture frozen before Pair 4 birth/chart features are inspected**. Outcomes for Pairs 1–4 informed the target decomposition, so this is not untouched validation. However, Pair 4 provides a useful chart-blind falsification check because its birth-derived astrology was not available when V0.3 was frozen.

## Why V0.2 was still too coarse

The newest relationship observations expose four distinctions that must be represented explicitly:

1. **Actor sexual desire is directional.** A may desire B intensely while B's desire for A is moderate.
2. **Sexual chemistry is dyadic, not reducible to attraction.** High attraction by one actor can coexist with poor chemistry when the other actor has low libido or there is a strong desire discrepancy.
3. **Intellectual stimulation is not intellectual compatibility.** One partner may repeatedly produce mind-expanding novelty while another is the better sustained thinking/conversation partner.
4. **Communication quality is not communication abundance.** A pair can communicate clearly and kindly when there is little shared content to discuss.

The development cases also show that very high mutual love can coexist with poor sex, very low commonality, low intellectual/mystical stimulation, and near-zero drama.

## Relationship-science structure reused

Sexual-desire discrepancy research treats partners' desired sexual frequency/desire as separate variables and associates discrepancies with sexual and relationship outcomes. Dyadic sexual-function studies using actor-partner models outperform individual-only models in explaining sexual satisfaction.

Therefore AstroRRF must preserve at least:

- `A_sexual_desire_for_B`;
- `B_sexual_desire_for_A`;
- `A_baseline_libido`;
- `B_baseline_libido`;
- `dyadic_desire_discrepancy`;
- `dyadic_sexual_responsiveness`;
- `dyadic_sexual_chemistry_satisfaction`.

Astrology may propose predictors for the first four. The dyadic chemistry outcome must be constructed from both persons plus interaction/context; it cannot be inferred from one Venus/Mars signal.

## V0.3 target vector

### Sexual / romantic

- actor-specific physical attraction;
- actor-specific sexual desire;
- actor-specific Eros/in-love state;
- baseline libido / desired frequency;
- dyadic sexual chemistry/satisfaction;
- desire discrepancy;
- romantic-priority sensitivity;
- sexual-exclusivity sensitivity.

### Cognitive / spiritual

Split into five targets:

1. `intellectual_compatibility`
   - sustained reasoning together;
   - mutual comprehension;
   - productive disagreement;
   - ability to build ideas together.
2. `intellectual_stimulation_self_expansion`
   - novelty;
   - surprise;
   - mind-expanding perspectives;
   - catalytic effect on the actor's thinking.
3. `conceptual_comprehension_application`
   - speed/accuracy of grasping difficult concepts;
   - ability to use them effectively.
4. `mystical_spiritual_stimulation`
   - shared contemplative/metaphysical inquiry;
   - intuitive/mystical novelty or resonance.
5. `communication_access_bandwidth`
   - language proficiency;
   - disclosure;
   - response continuity;
   - amount of available conversational data.

Do not infer target 1 from target 5. A poorly observable person may be highly compatible but unmeasured.

### Shared-life content

Add:

- shared interests/commonality;
- values/worldview overlap;
- shared activity supply;
- communication quality;
- communication abundance/volume.

This prevents `good communication but little to talk about` from becoming a contradiction.

### Emotional / autonomy

Preserve state-conditional curves rather than one score:

- baseline visible drama;
- inferred internal emotional ease (may be unknown);
- emotional readability;
- baseline autonomy/space;
- attachment-threat sensitivity;
- sexual-jealousy sensitivity;
- romantic-priority jealousy sensitivity;
- proximity sensitivity;
- pressure/engulfment under low, medium, and high activation.

## Astrology feature families — frozen before Pair 4 chart inspection

These are candidate mappings, not validated meanings.

### A. Actor physical/sexual attraction and Eros

Directional synastry only:

- actor Venus/Mars to partner Sun/Moon/Ascendant/Descendant;
- partner Venus/Mars in actor 5th/7th/8th;
- actor Venus/Mars to partner Pluto as intensity modifiers;
- partner Sun/Moon in actor 5th/7th/8th as secondary activators.

Do not infer dyadic sexual chemistry from this layer.

### B. Baseline libido

Treat as a natal-person hypothesis, not a synastry effect.

Candidate families to compare separately rather than assume:

- natal Mars/Venus condition and angularity;
- 5th/8th-house emphasis where birth time is known;
- selected Human Design sexual/energy mechanics only where sourced;
- non-astrological self-reported baseline libido.

V0.3 deliberately freezes **no numeric natal-libido formula** because the current development set is too small. Pair 4 is especially important because its poor sexual chemistry is reported to arise from partner low libido despite actor attraction.

### C. Sexual chemistry interaction

Candidate functional form for future fitting:

`chemistry = f(A_desire_for_B, B_desire_for_A, A_libido, B_libido, desire_match, responsiveness, context)`

Astrology is successful only if birth-derived features help estimate the upstream actor variables or add held-out information to actual chemistry. A single high Eros score is insufficient.

### D. Intellectual compatibility

Candidate directional/shared features:

- easy Mercury↔Mercury/Sun aspects for comprehension/translation;
- composite Mercury-Sun for shared thought/conversation centrality;
- Mercury house overlays to 3rd/7th/9th where appropriate.

### E. Intellectual stimulation / self-expansion

Prioritize novelty/depth candidates separately:

- actor Mercury ↔ partner Uranus;
- actor Mercury ↔ partner Pluto;
- partner Mercury/Uranus/Pluto activating actor 3rd/9th/11th where exact houses permit;
- composite Mercury-Mars/Uranus/Pluto as shared activation candidates.

Do not equate this with partner IQ or with ease of communication.

### F. Conceptual comprehension/application

Candidate features:

- easy Mercury↔Mercury/Sun;
- Mercury-Jupiter and Mercury-Saturn structure/synthesis candidates;
- HD insight/translation mechanics as a separate ablation layer.

Communication latency/language proficiency are reliability moderators, not evidence against underlying comprehension.

### G. Mystical/spiritual stimulation

Candidate features:

- actor Mercury/Jupiter ↔ partner Neptune/Pluto/Uranus;
- composite Mercury/Jupiter ↔ Neptune/Pluto;
- 9th/12th-house overlays only where exact houses are available;
- relevant HD mystery/inquiry mechanics as a separate layer.

Avoid treating Neptune as inherently positive; it may represent ambiguity/idealization as well as imaginative resonance.

### H. Commonality/shared interests

Do **not** assume broad natal similarity predicts relationship quality. Large studies find personality similarity effects small or inconsistent.

Candidate astrology research target is narrower: shared thematic salience rather than generic chart similarity. Test whether repeated emphasis on the same topical houses/planets predicts actual shared interests better than chance. Until tested, keep commonality primarily empirical/non-symbolic.

### I. Conditional emotional pressure

Preserve:

`pressure(state) = baseline + attachment_activation × latent_conflict + romantic_priority_threat × romantic_jealousy + sexual_threat × sexual_jealousy - autonomy_spacemaker_effects`

Potential astrology inputs:

- Moon-Moon/Moon-Saturn/Moon-Pluto for latent emotional friction/intensity;
- Uranus to relationship angles/personal planets for autonomy/spacemaker hypotheses;
- Pluto/Saturn/8th/12th emphasis for intensity/pressure only in combination with observed activation;
- actor-specific Eros mismatch as an upstream variable.

Context inputs are non-astrological: proximity, cohabitation, contact frequency, dependence, and competing romantic bonds.

## Development-case constraints V0.3 must represent

### Pair 1

- user-side sexual/romantic experience is peak/exceptional;
- strongest intellectual/mystical stimulation to user;
- good but not best intellectual compatibility;
- high engulfment and low emotional ease historically.

### Pair 2

- partner-side sexual desire for user is extreme;
- user-side attraction/desire is positive but substantially lower;
- user experiences strong sexual enjoyment but not peak attraction;
- highest sustained intellectual compatibility;
- high but not peak intellectual/mystical stimulation;
- low pressure/high ease at distance or low attachment threat;
- sharp pressure increase when partner fears loss of romantic priority, despite low sexual exclusivity demands.

### Pair 3

- strong introversion and low communication bandwidth/readability;
- promising rapid grasp/application of difficult contemplative concepts;
- mature intellectual compatibility unresolved;
- internal emotional ease unresolved despite low visible drama;
- low engulfment so far.

### Pair 4 — chart-blind falsification case

At V0.3 freeze, no Pair 4 birth/chart features have been inspected.

Observed target to be scored once birth data are supplied:

- user physical attraction: high;
- partner baseline libido: low relative to user;
- dyadic sexual chemistry: poor despite user attraction;
- mutual love/bond: very high;
- partner commitment/marriage intent: very high;
- shared interests/commonality: very low;
- intellectual stimulation: very low;
- mystical/spiritual stimulation: very low at that stage;
- communication quality: good;
- communication abundance: low because little shared content;
- drama/conflict: near zero;
- user ended relationship because sex and commonality/stimulation were insufficient.

## Pair 4 scoring rule

When Pair 4 birth data arrive:

1. calculate the chart without revising this file;
2. score only the frozen V0.3 feature families;
3. preserve unknown birth-time ranges if necessary;
4. report hits, misses, and unresolved domains;
5. do not add a new aspect meaning because the chart fails to fit;
6. only after the V0.3 result is recorded may a V0.4 be developed.

This is still development evidence because the target helped shape V0.3, but it cleanly tests whether the resulting feature mapping can accommodate a chart it has not yet seen.
