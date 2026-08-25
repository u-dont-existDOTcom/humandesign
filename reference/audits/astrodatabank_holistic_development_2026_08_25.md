# Astro-Databank holistic positive-evidence development audit

**PHASE: DEVELOPMENT**

Date: 2026-08-25

This audit records unrestricted/post-hoc methodological development on the user-supplied official Astro-Databank `c_sample.zip`. It is not independent validation. Results here may influence the next model version; therefore they cannot establish generalization.

## Data boundary

The uploaded export contains the Astro-Databank C sample. The conservative person filter was:

- Rodden rating A or AA;
- timed record with `jd_ut`;
- `Public Figure` data type;
- no alternative birth tuple.

The current parser yields approximately 4,750 such public figures. The archive is sparse and heterogeneous: personality labels are recorded for only a small minority, while vocation and other biography categories are much more common. Absence of a category is therefore not a reliable behavioral negative.

Exploratory calculations in the development notebook used the repository's mechanically parity-checked Moshier path. They are **not canonical V4.3/Swiss-file results**. The committed runner now requires verified local Swiss Ephemeris files before a reproducible archive report can be generated.

## Why the research question changed

Earlier one-feature/one-trait tests did not reproduce the apparent specificity seen in rich individual case analyses. A whole-profile test was therefore added:

> Given the positive behavioral/life-pattern evidence actually observed for a person, does their complete birth-derived chart rank above matched decoy charts?

The first implementation correctly ignored unrecorded labels while scoring but still made two subtler mistakes discovered during adversarial development:

1. people with no annotation in an ontology branch could enter that label's training background;
2. people with no annotation opportunity could occupy nearest-neighbor slots and crowd out people for whom that construct was actually observed.

Both are forms of positive-unlabeled/annotation-selection leakage. The durable model now conditions both the denominator and neighborhood on the label's observation opportunity.

## Dependency control

Behavioral labels were clustered so multiple related archive tags could not multiply evidence. Examples:

- all `Vocation` sublabels share one evidence opportunity/dependency branch;
- `Traits : Personality` labels share a branch;
- `Family : Relationship`, `Family : Parenting`, etc. are kept separate from one another but internally clustered.

Chart encodings were also tested in separate families rather than assuming that adding Type + centers + channels + gates + carriers must help.

## Additive whole-chart development results

A first additive, person-level cross-fitted scorer showed only small gains. Which feature family looked best was unstable across splits: gates, channels, or small architecture combinations could win depending on the split. Carrier identities/lines often harmed the additive model.

This supported testing genuinely nonlinear whole-chart similarity rather than continuing to sum marginal feature enrichments.

## Nonlinear chart-neighborhood development

A nearest-neighbor model compares a candidate chart with structurally similar DEVELOPMENT charts and asks whether people with those charts carry the held-out person's observed positive labels more often than the relevant background.

### Unordered gates/channels

With sex + decade + country matched decoys, an unordered gates+channels representation produced a small positive cross-fitted rank signal. Tightening the conventional control to **exact birth year + country** reduced the result to approximately chance.

Interpretation: the loose result was largely explainable by cohort/year structure, plausibly slow-planet patterns tracking historical occupation/biography changes.

### Planet-specific fast-body carriers

The analysis then preserved which body carried which gate/line rather than treating the chart as an unordered set. The development representation used Personality + Design gate/line tokens for:

- Sun;
- Moon;
- Mercury;
- Venus;
- Mars.

A deterministic development holdout initially produced a large exact-year+country-controlled result (about the 54.6th mean true-chart percentile for one selected neighborhood setting), but five-fold cross-fitting reduced it substantially. Neighborhood-size development showed a smoother positive pattern at larger K, with K=200 eventually preferred inside DEVELOPMENT.

This was interesting enough to justify a deeper missingness/source audit, not strong enough to claim validation.

## Opportunity-conditioned model

After fixing training-time missingness completely, the fixed fast-body gate+line neighborhood model remained positive in the pooled archive under exact-year+country candidate matching. Representative exploratory five-fold results were approximately:

| phenotype scope | evaluable people | mean true-chart percentile | candidate-exchange status |
|---|---:|---:|---|
| personality/lifestyle | 294 | 55.25% | positive development tail |
| behavior + vocation | 3,107 | 55.11% | strong development tail |
| broader life patterns | 3,219 | 56.51% | strong development tail |

These numbers are DEVELOPMENT model-selection evidence only. They triggered a mandatory transport/source audit rather than a validity claim.

## Country transport failure

The same opportunity-conditioned nonlinear model was then trained and evaluated **within country**, with exact birth-year/sex candidate matching.

Representative exploratory results:

| country | evaluable people | mean true-chart percentile | direction |
|---|---:|---:|---|
| France | ~780 | ~66.7% | very strong positive |
| United States | ~1,199 | ~50.0% | null |
| Italy | ~199 | ~41.3% | opposite |
| United Kingdom | sparse | ~49.6% | null/indeterminate |

This is decisive against describing the pooled archive result as a universal Human Design effect. A real general person↔chart signal should not be declared from an effect that is huge in one country/source ecosystem, null in another large ecosystem, and reversed in another.

## French archive provenance

French eligible records are unusually concentrated in specific collector/source corpora. Exploratory counts found roughly:

- Didier Geslain: ~713 French records;
- Gauquelin listed as collector: ~117;
- additional large collector groups from Steinbrecher, Scholfield, Mandl, de Jabrun, and others;
- source notes explicitly mentioning Gauquelin for ~187 French records.

Source-specific training changed the French effect dramatically. Geslain-only training was close to chance, while heterogeneous pooled French training could produce very large apparent identification effects.

Matching candidate decoys by collector did **not** remove the large pooled-French result. This exposed a more subtle leakage route: a model trained across collector corpora can use a candidate chart's similarity to other collectors' training charts as a proxy for archive provenance even when every candidate in the comparison has the same collector label.

Therefore source control must block the **training neighborhood/model fit itself**, not merely the decoy set.

## Durable methodological changes

The repository now requires the following for sparse archive holistic analysis:

1. **Opportunity-conditioned labels** — a label is learned only among people with that ontology branch observed.
2. **Opportunity-conditioned neighborhoods** — people without that observation opportunity cannot occupy the label's K nearest-neighbor slots.
3. **Behavior dependency caps** — correlated archive tags cannot multiply evidence without limit.
4. **Person-level cross-fitting** — development ranks used for model selection come from models that did not train on that person.
5. **Exact-year controls** for long historical archives when cohort effects are plausible.
6. **Training-source blocking** — candidate matching by collector/site is insufficient if TRAIN can still mix source corpora.
7. **Transport reporting** across materially large countries/sites/sources before any generalization claim.
8. **Independent external validation** remains required for scientific confirmation.

See `docs/21_holistic_positive_evidence_identification.md` and `src/hdmatch/human/holistic_opportunity.py`.

## Current interpretation

The Astro-Databank development work demonstrates that holistic nonlinear chart matching is methodologically different from marginal one-feature correlations and can produce apparently substantial rank effects. It also demonstrates how easily a flexible model can exploit archive/cohort/source structure.

The current Astro-Databank result is therefore best classified as:

> **promising as a method-development signal, but nontransportable and source-confounded as evidence for a general Human Design effect.**

The next scientifically weight-bearing result must come from either:

- the source-blocked canonical Swiss rerun showing stable direction across genuinely distinct archive sources; or
- a frozen holistic model tested on an independent, astrology-naive cohort with sufficiently rich behavioral data.
