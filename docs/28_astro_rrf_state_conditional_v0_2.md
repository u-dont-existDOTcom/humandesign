# 28 — AstroRRF State-Conditional Model V0.2

Status: **retrospective development model fitted after additional outcome exposure**. V0.1 remains frozen and unchanged. V0.2 exists because subsequent user clarification falsified several V0.1 target definitions even where an ordinal score happened to look correct.

## Why V0.2 is necessary

V0.1 still collapsed distinct processes:

- `communication_intellectual_fit` mixed shared intellectual compatibility with one-way intellectual stimulation;
- `emotional_ease` treated a dynamic state as a trait;
- `engulfment_pressure` ignored threshold/context effects;
- low visible conflict could be mistaken for internal emotional ease when the partner was difficult to read;
- jealousy/possessiveness was not split into sexual versus romantic/attention exclusivity.

The criterion correction is stored in `reference/development_cases/relationship_phenotype_directional_addendum_v2.json`.

## Outcome architecture

### Cognitive domain

AstroRRF V0.2 predicts four separate variables.

#### 1. Shared intellectual compatibility

Definition: sustained two-way fit in reasoning, vocabulary, pace, conversation depth, productive disagreement, and feeling mentally met.

Primary candidate astrology layer: **shared relationship field**, especially midpoint-composite Mercury configurations, plus reciprocal Mercury synastry.

Do not equate novelty with compatibility.

Development examples:

- Pair 2 has midpoint-composite Mercury conjunct Sun at about 0.8°, a candidate for a relationship identity strongly organized around thought/conversation.
- Pair 1 instead has midpoint-composite Mercury sextile Mars at roughly 1.1–1.3° across the partner's entire unknown civil birth day, a candidate for mental activation/energy rather than necessarily the smoothest intellectual fit.
- Pair 3 has midpoint-composite Mercury sextile Neptune at about 0.6° and actor Mercury trines to partner Sun/Mercury; this may support intuitive/conceptual understanding when communication is available, but does not predict access frequency.

These interpretations are post-hoc training hypotheses and require held-out testing.

#### 2. Directional intellectual stimulation / self-expansion

Definition: how much Person B expands Person A's perspective, generates surprising insight, novelty, fascination, intuitive leaps, or a `mind-blowing` subjective effect.

This is conceptually related to the relationship self-expansion literature, which treats novelty/interesting challenge and expansion of knowledge/perspective as distinct from ordinary compatibility.

Candidate astrology features:

- partner Mercury in actor 5th/8th or strongly activating actor identity/cognitive points;
- Uranus/Pluto/Neptune contacts that are actor-specific rather than merely generational;
- composite Mercury-Mars/Uranus/Pluto as shared activation candidates;
- Human Design electromagnetics/mental-channel interactions as a separately testable AstroHD layer.

Do not force this axis to use the same weights as intellectual compatibility.

#### 3. Conceptual comprehension/application

Definition: how quickly the partner grasps and correctly applies difficult ideas once communicated.

Candidate astrology features:

- easy Mercury-Sun/Mercury contacts;
- Mercury-Jupiter/Saturn contacts as separately evaluated comprehension/structure candidates;
- HD cognitive-channel/gate interactions where source-backed mappings exist.

This axis is currently promising but under-observed for Pair 3.

#### 4. Communication access/bandwidth

Definition: how much of the partner's cognition and inner state is actually observable to the actor.

This is **not primarily a synastry intelligence variable**. Preserve non-astrological measurement constraints:

- language proficiency;
- disclosure;
- communication latency/contact continuity;
- introversion/social appetite;
- willingness/ability to articulate emotion;
- medium and distance.

The interpersonal-process model of intimacy supports treating disclosure and perceived responsiveness as distinct mechanisms rather than assuming latent understanding is visible in conversation.

Natal astrology/HD may generate hypotheses about withdrawal/disclosure style, but real language/contact constraints must remain explicit moderators and measurement-reliability factors.

## Emotional/engulfment domain becomes state-conditional

### Separate observed and latent emotional ease

`observed_outward_ease` = visible ease/low conflict.

`latent_emotional_ease` = internal regulation/ease. Do not infer this when observability is poor.

Use repository effective-confidence logic:

`effective_confidence = behavioral_confidence × measurement_reliability`.

Low disclosure, sparse contact, language constraints, or strong opacity reduce reliability; they do not create evidence for emotional ease.

### Contextual pressure function

Replace one scalar engulfment score with a response surface.

Development form:

`pressure(t) = baseline_pressure + attachment_activation(t) × latent_conflict_load + exclusivity_threat(t) × jealousy_sensitivity + dependence(t) × enclosure_sensitivity`

where attachment activation can depend on:

- physical proximity/co-presence;
- contact intensity;
- cohabitation;
- dependence/shared resources;
- actor/partner Eros mismatch;
- perceived risk of losing specialness/priority.

This is intentionally a functional architecture rather than a fitted universal equation.

### Split jealousy/exclusivity by target

Preserve separately:

- `sexual_exclusivity_sensitivity`;
- `romantic_exclusivity_sensitivity`;
- `attention_priority_sensitivity`.

Consensual-nonmonogamy research shows that emotional versus sexual extra-pair involvement can produce different jealousy responses; therefore a person can tolerate sexual sharing while reacting strongly to romantic attachment or priority shifts.

Astrology may eventually predict these separately, but no sign/aspect mapping is promoted yet from the three development cases alone.

## Revised three-pair retrospective map

### Pair 1

Observed:

- highest actor-side erotic/romantic passion;
- highest actor-side intellectual stimulation/self-expansion;
- good intellect/compatibility but below Pair 2 on sustained intellectual compatibility;
- highest historical engulfment;
- lowest historical emotional ease.

Retrospective astro candidates:

- directional Venus/Mars and 7th-house activations remain strong actor-Eros candidates;
- near-exact actor Moon–partner Pluto remains a strong pressure/engulfment candidate;
- partner Mercury in actor 5th and robust composite Mercury sextile Mars are now candidates for **stimulating/creative mental activation**, not for highest shared intellectual compatibility;
- unknown partner birth time prevents full reciprocal house/angle interpretation.

### Pair 2

Observed:

- highest sustained intellectual compatibility;
- high but below Pair 1 intellectual stimulation;
- actor is Storge-dominant while partner remains Eros/in-love;
- emotional ease and autonomy are very good at distance/low attachment threat;
- pressure/drama can become very high with proximity or when the partner fears actor romantic love/attention shifting to another person;
- sexual nonexclusivity is tolerated much better than romantic/attention nonexclusivity.

Retrospective astro candidates:

- composite Mercury conjunct Sun (~0.8°) becomes the strongest candidate for shared intellectual centrality/compatibility;
- actor Mercury conjunct partner Uranus and sextile partner Pluto remain strong novelty/depth candidates, but are no longer required to explain why Pair 2 is *more stimulating* than Pair 1;
- exact Moon–Moon hard aspect is reclassified as **latent conflict load**, which may be gated by attachment activation rather than causing constant low emotional ease;
- directional Eros asymmetry remains as in V0.1;
- context explains why the same pair can be easy at distance and difficult when emotional exclusivity/priority is threatened.

### Pair 3

Observed:

- strong introversion is corroborated across contexts;
- communication/access bandwidth is currently low;
- difficult concepts can be grasped and applied quickly when communicated;
- outward drama is low so far, but latent emotional ease is unknown because emotional observability is poor;
- engulfment is low so far, with limited exposure.

Retrospective astro candidates:

- actor Mercury trine partner Sun/Mercury remains a candidate for **comprehension when communication occurs**;
- composite Mercury sextile Neptune (~0.6°) becomes a candidate for intuitive/mystical conceptual resonance **and** ambiguity rather than simple communication quality;
- Uranian axis contacts remain autonomy/space candidates;
- no current astrology score may convert low visible conflict into high latent emotional ease.

## V0.2 feature-family freeze for the next held-out case

The following distinctions are now frozen as **feature families**, not final numerical weights:

1. Directional Eros/Passion — directional synastry + house overlays.
2. Shared intellectual compatibility — composite Mercury/Sun/Mercury/Jupiter/Saturn structure + reciprocal Mercury ease.
3. Directional intellectual stimulation/self-expansion — actor-specific Uranus/Pluto/Neptune/Mercury activations + creative/intimacy house context; evaluate HD separately.
4. Conceptual comprehension/application — Mercury-Sun/Mercury/Jupiter/Saturn ease/structure candidates.
5. Communication access/bandwidth — measured context first; natal symbolic moderators only as secondary hypotheses.
6. Latent conflict load — Moon/Pluto/Saturn and composite emotional configurations.
7. Attachment-triggered pressure — latent conflict × proximity/Eros mismatch/exclusivity threat; context is mandatory.
8. Sexual versus romantic/attention jealousy — separate outcomes; mappings unresolved until more cases.

Do not add new aspect families/minor aspects merely because one of these three cases remains unexplained.

## Validation boundary

V0.2 fits additional revealed outcomes and is therefore **more contaminated than V0.1**, not more validated.

Use it to define better variables and candidate feature families. The next evidence must come from:

- an historical relationship whose outcome profile is rated before its chart is inspected; or
- a genuinely prospective relationship outcome frozen before maturation.

V0.1 remains a preserved earlier checkpoint and must never be overwritten by V0.2.
