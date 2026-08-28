# 24 — Empirical Relationship Phenotype Model

Status: reusable descriptive/evaluation architecture; composition of established relationship-science constructs. Not a diagnostic model and not a validated predictor of relationship outcome in this repository.

## Why this exists

AstroHD and Human Design pair mechanics can generate symbolic hypotheses, but partner comparison requires a target that preserves distinct observed domains rather than collapsing them into a single compatibility score.

A relationship can simultaneously have:

- exceptional sexual chemistry;
- exceptional romantic attachment;
- weak communication;
- poor emotional ease;
- high engulfment;
- strong commitment;
- high autonomy;
- or the reverse pattern.

Any model that averages these too early can rank a relationship incorrectly while still matching a few salient features.

## Prior-work scan and reuse decision

This model is an adaptation/composition of established work rather than a new psychological theory.

### Perceived Relationship Quality Components (PRQC)

Fletcher, Simpson & Thomas (2000) support six separable first-order relationship-quality factors: satisfaction, commitment, intimacy, trust, passion, and love, which can also load on a higher-order relationship-quality factor.

DOI: 10.1177/0146167200265007

Reuse: keep the six domains separate for partner comparison; compute an overall score only if the user explicitly supplies weights.

### Interpersonal Process Model of Intimacy

Reis & Shaver's process model, tested by Laurenceau, Barrett & Pietromonaco (1998), treats intimacy as an interactional process involving self-disclosure, partner disclosure, and perceived partner responsiveness. Daily-diary work also supports perceived responsiveness as a central mediator/process variable.

DOI: 10.1037/0022-3514.74.5.1238

Reuse: distinguish intellectual/communication compatibility from emotional accessibility and from intimacy. A highly intelligent conversational partner can still be difficult to read emotionally.

### Relationship-specific attachment

The ECR-R/ECR-RS framework separates attachment anxiety and avoidance and permits relationship-specific attachment representations. Relationship-specific measures can predict intra/interpersonal outcomes better than broad trait attachment for the particular relationship.

Fraley et al. ECR-RS DOI: 10.1037/a0022898

Reuse: model pursuit, distancing, reassurance-seeking, withdrawal, and fear/discomfort with closeness as pair-specific process variables; do not infer attachment style from one behavior such as delayed texting.

### Autonomy / differentiation

Self-determination and differentiation research shows that closeness and autonomy are not opposites. Lower felt autonomy can help explain lower relationship satisfaction associated with attachment insecurity; differentiation is associated with relationship quality/stability in longitudinal work.

Reuse: measure closeness and autonomy separately. `Engulfment` is operationalized as high relational intensity/closeness combined with low felt autonomy or high pressure/merging, not simply as high intimacy.

### Sexual relationship science

The New Sexual Satisfaction Scale (NSSS) treats sexual satisfaction as multidimensional. Desire discrepancy, sexual communication quality, sexual autonomy support, sexual ideals, and partner responsiveness each contribute information not reducible to general relationship satisfaction.

NSSS DOI: 10.1080/00224490903100561
Sexual communication meta-analysis DOI: 10.1037/fam0000946

Reuse: sexual chemistry/satisfaction must be its own primary domain rather than inferred from general romantic attraction.

### Ideal Standards Model

Fletcher and colleagues distinguish warmth/trustworthiness, vitality/attractiveness, and status/resources as partner ideals, and intimacy/loyalty and passion as relationship ideals. Fit to a person's own ideals predicts relationship evaluations.

DOI: 10.1037/0022-3514.76.1.72

Reuse: compatibility is partly observer-specific. Do not assume a universal ranking when the user has unusual or strongly weighted partner ideals.

### Big Five / Extraversion aspects

For social-orientation questions, use observed behavior or a validated Big Five measure. Extraversion is not equivalent to sociability alone and can be decomposed into at least Assertiveness and Enthusiasm aspects.

DeYoung, Quilty & Peterson (2007), DOI: 10.1037/0022-3514.93.5.880

Reuse: distinguish social initiation/assertiveness, sociability/enthusiasm, emotional expressiveness, and need for solitude. A person can be expressive or socially competent while strongly introverted in social appetite.

## Relationship Phenotype Vector (RPV)

For each relationship preserve the following dimensions separately.

### A. Erotic / romantic

1. `sexual_chemistry_satisfaction`
   - subjective quality of sex;
   - attraction/arousal;
   - sexual ease/flow;
   - mutual responsiveness;
   - sexual communication;
   - desire discrepancy;
   - sexual autonomy.

2. `romantic_connection_passion`
   - infatuation/passion;
   - romantic longing;
   - felt specialness;
   - excitement/self-expansion;
   - desire for romantic contact independent of sex.

3. `love_attachment_bond`
   - felt love;
   - attachment/bond strength;
   - separation distress;
   - durability of affection across conflict/distance.

### B. Intimacy / understanding

4. `communication_intellectual_fit`
   - conversational depth;
   - ease of reasoning together;
   - shared concepts/interests;
   - feeling mentally understood;
   - productive disagreement.

5. `emotional_accessibility_transparency`
   - ability to know what the partner is feeling/thinking;
   - disclosure;
   - predictability of availability;
   - response latency/withdrawal only as observed behavior, not as an inferred diagnosis.

6. `perceived_partner_responsiveness`
   - felt understanding;
   - validation;
   - caring;
   - attentive listening and appropriate response.

7. `emotional_ease_regulation`
   - ease of being around one another's emotions;
   - conflict arousal;
   - recovery after conflict;
   - emotional volatility or steadiness;
   - distinguish outward ease from internal transparency.

### C. Closeness / autonomy

8. `closeness_interdependence`
   - felt inclusion/merging;
   - frequency and breadth of shared life;
   - dependence/interdependence.

9. `autonomy_space`
   - freedom to remain oneself;
   - ability to spend time apart without coercion;
   - freedom of goals, friendships, work, and inner life.

10. `engulfment_pressure`
    - felt pressure to merge, attend, reassure, sacrifice, or organize life around the relationship beyond what is freely wanted;
    - score separately from closeness so `high closeness + high autonomy` is possible.

11. `pursue_withdraw_dynamics`
    - frequency/intensity of demand-withdraw, withdraw-withdraw, or demand-demand cycles;
    - identify direction and context.

### D. Long-term functioning

12. `trust_safety`
13. `commitment_intent`
14. `practical_life_fit`
    - daily routines;
    - finances/resources;
    - geography;
    - children/family;
    - work/lifestyle;
    - relationship structure;
    - values.
15. `repair_conflict_skill`
16. `growth_self_expansion`

## Person-level social phenotype

Do not infer `introvert/extrovert` from astrology or HD. Separate:

- `sociability_appetite` — how much social contact the person wants;
- `social_initiation_assertiveness` — how readily they approach/lead;
- `social_expressiveness` — how visibly expressive/animated they are;
- `one_to_one_vs_group_preference`;
- `need_for_solitude_recovery`;
- `communication_latency` — how long they may disappear between contacts;
- `emotional_disclosure` — how readable they are to close others.

A person may be low in sociability appetite and high in expressiveness/assertiveness, or highly sociable but emotionally opaque.

## Scoring policy

1. Do not assign a total compatibility score by default.
2. Preserve observed, inferred, and unknown values separately.
3. User-reported repeated lived experience outranks astrology/HD symbolic predictions for the same target.
4. Do not treat post-hoc reinterpretation as a successful prediction.
5. Relationship duration/exposure matters: early-stage unknowns should remain unknown rather than be scored neutral.
6. When comparing partners, use the same domains and evidence standard for every partner.
7. If the user wants an overall ranking, elicit or infer explicit user weights only from stated values/preferences; report sensitivity to those weights.
8. Historical relationships may be rated from remembered peak, typical, and end-state values separately where those differ materially.

## Model comparison / validation

For future research compare:

- `R-AstroHD`: frozen symbolic AstroHD pair predictions;
- `R-HD`: HD pair mechanics only;
- `R-RPV`: observed/questionnaire Relationship Phenotype Vector;
- `R-BASIC`: simple baseline using relationship duration, age/life-stage alignment, distance/cohabitation and shared goals.

Do not evaluate `R-RPV` as a prediction of the same observations used to construct it. It is the phenotype/criterion model. AstroHD/HD should predict held-out RPV domains if they are to claim relationship validity.

The most informative test is domain-level discrimination rather than a global compatibility correlation. For example, a model should separately predict which relationship has highest sexual satisfaction, strongest communication/intellectual fit, highest emotional ease, and greatest engulfment pressure.
