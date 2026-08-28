# 27 — AstroRRF Directional Model V0.1

Status: **retrospective development model fitted after outcome exposure**. It may organize the three known development relationships, but its fit to them is not evidence of predictive validity. Freeze this version before testing additional held-out relationships or later outcomes.

## Why the prior AstroHD relationship layer failed

The prior model treated synastry as a mostly symmetric relationship-level signal and collapsed multiple outcomes into broad labels such as attraction, intensity, integration, and compatibility.

The observed relationship phenotype requires actor-specific and domain-specific outputs:

- Person A may be Eros/in-love toward Person B while Person B is Storge/companionate toward Person A.
- Sexual/romantic passion can be high while emotional ease is low.
- Intellectual/communication intimacy can be high while erotic passion is lower.
- Engulfment can differ from intimacy and can change with physical proximity even when love style remains stable.

The directional clarification in `reference/development_cases/relationship_phenotype_directional_addendum_v1.json` makes a symmetric compatibility score invalid.

## External structure reused

### RRF / Love Styles define the outcomes

Use Davis–Todd RRF dimensions and Lee/Hendrick love styles as criterion axes rather than asking astrology to predict a generic relationship score.

RRF development targets used here:

- Passion: fascination, exclusiveness/specialness, enjoyment, sexual intimacy;
- Intimacy: understanding, confiding, alter-ego/feeling known;
- Viability: acceptance, trust, respect, good influence;
- Support/Care;
- Conflict;
- Ambivalence;
- Stability/Maintenance where historical evidence permits.

Love-style targets:

- Eros;
- Storge;
- Mania/engulfment analogue;
- Agape, Ludus, Pragma only when observed evidence exists.

### Actor–Partner structure

Use an actor/partner architecture conceptually analogous to the Actor–Partner Interdependence Model (APIM): every directional target is indexed by experiencer.

For a pair A/B preserve separately:

- `A_eros_toward_B`;
- `B_eros_toward_A`;
- `A_intimacy_toward_B`;
- `B_intimacy_toward_A`;
- `A_mania_engulfment_toward_B`;
- `B_mania_engulfment_toward_A`;
- actor-specific satisfaction/viability where measured.

Then preserve shared relationship-field variables separately.

This is a conceptual/statistical structure, not evidence that astrology predicts APIM outcomes.

## Astrology layers

### Layer 1 — directional synastry: primary

Synastry is the primary layer for actor-specific RRF/Love Style outputs because house overlays are directional and planet roles can be preserved.

#### A. Actor-side Eros / Passion

Candidate features, in priority order:

1. **Actor Venus/Mars activation by partner luminaries/angles**
   - conjunction/opposition/square are treated as stronger activation candidates than trine/sextile for the development model;
   - preserve actor ownership: `A_Venus -> B_Sun` is evidence for A's romantic response, not automatically B's.
2. **Partner Venus/Mars in actor 5th, 7th, or 8th houses**
   - 5th: romance/erotic play candidate;
   - 7th: partner-recognition/relationship candidate;
   - 8th: sexual/intimacy/depth candidate;
   - house owner's experience is the directional target.
3. Actor Venus/Mars contacts with partner Pluto may intensify sexuality/depth but must not automatically count as love or durability.
4. Partner Sun/Moon in actor 5th/7th/8th are secondary relational activators.

Do not count the reverse overlay unless predicting the reverse actor's outcome.

#### B. Actor-side Intimacy / Understanding

Split `communication ease` from `communication depth/stimulation`.

Candidate features:

- actor Mercury ↔ partner Mercury/Sun easy major aspects: cognitive ease/translation;
- actor Mercury ↔ partner Uranus: novelty, stimulation, unusual ideas;
- actor Mercury ↔ partner Pluto: depth/probing/intense inquiry;
- partner Mercury/Moon in actor 3rd/7th/8th as secondary house-context features.

Development hypothesis: Uranus/Pluto Mercury contacts may predict **interesting/deep intellectual connection** better than merely easy Mercury trines, while easy Mercury contacts may predict comprehension when communication occurs.

Communication continuity/disclosure is a separate target and should not be inferred from Mercury synastry alone.

#### C. Actor-side Mania / Engulfment

Candidate positive features:

- partner Pluto hard/conjunct actor Moon or Venus, especially very tight;
- partner Pluto/Saturn contacts to actor angles or personal planets;
- partner Moon/Pluto/Neptune in actor 8th/12th where exact houses are known;
- repeated 7th/8th activation combined with conflict/uncertainty indicators.

Candidate autonomy/spacemaker features:

- tight Uranus contacts to Ascendant/Descendant or Venus/Moon;
- strong reciprocal Uranian relationship-axis contacts may reduce enclosure even when attraction/depth is high.

Do not equate Pluto or 8th-house emphasis with engulfment by itself.

### Layer 2 — shared relationship field: secondary

Use midpoint composite and/or Davison only for outcomes conceptually belonging to the relationship as a shared system:

- shared conflict/ambivalence climate;
- shared stability/maintenance;
- public/private relationship emphasis;
- timing of relationship-state changes when a real-time Davison chart is available.

Do **not** use composite/Davison to erase actor-specific asymmetry.

Birth-time rule: unknown partner time blocks exact composite angles/houses and Davison timing. Preserve full-day sensitivity rather than inventing a time.

### Layer 3 — natal moderators

Natal chart features can moderate how synastry is expressed without being pair compatibility evidence by themselves.

Examples to test rather than assume:

- social appetite/withdrawal;
- disclosure/communication style;
- autonomy/freedom orientation;
- emotional regulation style.

AstroHD may add HD natal features here, but Western-only and HD-only moderators must remain separately identifiable for ablation.

### Layer 4 — real-world context moderator

The same actor-specific love mismatch can behave differently under different contexts.

Preserve at least:

- physical proximity/co-presence;
- distance;
- cohabitation;
- relationship structure;
- contact frequency;
- dependence/shared resources.

Development interaction:

`mismatch_pressure ≈ |A_Eros - B_Eros| × proximity/exposure × reciprocity_demand`

This is a relationship-process moderator, not an astrological claim. Astrology may predict the directional mismatch; context predicts when it becomes costly.

## Three-pair retrospective development fit

The following is training-set interpretation, not validation.

### Pair 1

Observed target: strongest user-side sex/romance; highest engulfment; lowest emotional ease; communication below Pair 2.

AstroRRF candidate explanation:

- actor Venus and Mars are both tightly hard-aspected to partner Sun -> strong actor-side Eros/sexual activation;
- partner Venus and Mars fall in actor 7th -> strong actor-side partner/romantic recognition;
- actor Moon is almost exactly hard-aspected to partner Pluto -> very strong Mania/engulfment candidate;
- partner Moon falls in actor 12th -> secondary opacity/unconscious-intensity candidate;
- no comparably strong tight Mercury synastry -> does not predict the strongest intellectual fit.

This fits the observed profile substantially better than the prior generic `chemistry` ranking.

### Pair 2

Observed target: partner remains in love/Eros toward actor; actor is Storge-dominant; actor reports strongest communication/intellectual compatibility; engulfment middle; emotional ease middle; proximity increases drama because partner wants reciprocal Eros.

AstroRRF candidate explanation:

- partner Venus tightly contacts actor Sun -> strong **partner-side** Eros candidate;
- actor Venus and Mars fall in partner 5th -> strong **partner-house-owner** romance/sexual activation;
- reverse overlay is not equivalent: partner Venus/Mars do not land in actor 5th/8th, so the old symmetric romance interpretation is rejected;
- actor Mercury tightly contacts partner Uranus and Pluto -> strong intellectual novelty/depth candidate;
- very tight Moon–Moon hard aspect -> emotional-friction candidate;
- actor Pluto tightly contacts partner Ascendant and actor Saturn tightly contacts partner Pluto -> stronger enclosure/pressure than a purely companionate reading, but less direct Mania evidence than Pair 1's near-exact Moon–Pluto contact;
- actor/partner Eros mismatch combined with physical proximity predicts higher mismatch pressure when together; distance can reduce the behavioral cost while leaving partner Eros intact.

### Pair 3

Observed target: strongest outward emotional ease so far; lowest engulfment so far; strong introversion/opacity/intermittent communication; mature Eros/sexual outcome unknown.

AstroRRF candidate explanation/prediction:

- easy Moon–Moon aspect -> relative emotional-ease candidate;
- reciprocal tight Uranus-to-relationship-axis contacts -> autonomy/space candidate that may counterbalance Pluto/8th-house intensity;
- actor Mercury has easy contacts to partner Sun/Mercury -> predicts cognitive comprehension **when communication occurs**, not communication continuity;
- actor Venus/Mars strongly activate partner Sun and actor/partner 8th-house overlays are present -> predicts potentially high eventual erotic/intimacy activation, but this remains prospective because the observed mature outcome is unknown;
- low communication continuity/opacity must currently be explained by natal/context moderators or left unresolved, not rescued by the easy Mercury synastry.

## What V0.1 appears to improve retrospectively

Without assigning a scalar score, V0.1 can represent all currently established directional distinctions:

- Pair 1 > Pair 2 in user-side Passion/Eros;
- Pair 2 partner-side Eros > Pair 2 actor-side Eros;
- Pair 2 > Pair 1 and Pair 2 > Pair 3 in observed communication/intellectual fit through depth/stimulation rather than simple Mercury ease;
- Pair 3 > Pair 2 > Pair 1 in emotional ease using Moon/ease versus high-intensity emotional contacts;
- Pair 1 > Pair 2 > Pair 3 in engulfment by distinguishing Moon–Pluto/pressure from 8th-house depth and by allowing Uranus to act as an autonomy feature.

This is **100% descriptive training fit to the currently encoded order constraints only because the feature meanings and priorities were selected after seeing those outcomes**. It must not be reported as accuracy.

## Critical next test

The next step is not to continue tuning on these three.

1. Freeze V0.1 exactly.
2. Add additional historical relationships/sexual-romantic connections with birth data and independently rated RRF/Love Style outcomes.
3. Hide one relationship at a time and test whether V0.1 ranks its domains correctly (`leave-one-relationship-out`) once there are enough cases.
4. Keep unknown-time partners as full-day ranges; no rectification from relationship outcomes.
5. Compare:
   - Western directional synastry only;
   - composite/Davison shared field only where available;
   - HD directional relationship mechanics only;
   - merged AstroHD;
   - non-symbolic relationship/context baseline.
6. Only retain an astrology layer if it adds held-out domain discrimination beyond the simpler baseline.

With only three outcome-exposed relationships, many different astro mappings can be made to fit. The minimum useful personal retrospective set is roughly 8–12 relationships/major romantic-sexual connections; 15+ is materially better for sparse model selection. Fewer cases can still be informative if predictions are frozen and evaluated one relationship at a time, but they cannot distinguish among many competing feature families.

## Source/concept notes

- Synastry is directional in the sense that each chart is overlaid on the other and planet placements can be read in each person's houses separately.
- Composite and Davison charts are relationship-level techniques and therefore belong primarily to shared-field targets.
- Traditional partnership astrology specifically includes the 5th house when sexuality is being considered.
- APIM supplies the non-astrological conceptual/statistical reason to preserve actor and partner effects separately.
