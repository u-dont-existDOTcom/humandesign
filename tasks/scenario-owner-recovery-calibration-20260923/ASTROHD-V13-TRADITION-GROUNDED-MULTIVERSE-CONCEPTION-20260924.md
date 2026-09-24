# AstroHD V1.3 candidate — tradition-grounded multiverse conception — 2026-09-24

Status: **BOUNDED DESIGN RESPONSE / NOT ACTIVE IMPLEMENTATION / NOT VALIDATION**.

## Owner question

Can owner-case development be grounded in pre-existing astrological traditions rather than in hand-assigned V1.1-style feature salience/directness weights?

Answer: **yes, materially**. The cleanest replacement is not to cherry-pick individual rules from multiple traditions after seeing the owner result. It is to freeze several complete source-grounded interpretation systems independently, run each as its own model, and inspect robustness across the resulting specification multiverse.

## Core anti-cheating principle

Do not ask:

> Which traditional features make the known owner birth time score best?

Ask:

> If we implement several historically/practitioner-established systems as faithfully and mechanically as possible before opening the owner score, do they independently converge on the same owner neighborhood?

This changes the degrees of freedom from hidden hand weighting to explicit published/source-backed model specifications.

## Candidate source-grounded model families

### 1. Hellenistic Western

Possible canonical sources:
- Vettius Valens, *Anthology*;
- Ptolemy, *Tetrabiblos*;
- modern historical reconstruction only where needed to operationalize explicit ancient rules.

Candidate techniques must be frozen from sources, not selected by owner fit:
- seven traditional planets;
- traditional rulerships;
- sect;
- whole-sign/equal-house techniques only in source-appropriate variants;
- sign-based aspects/configurations;
- domicile/exaltation and other source-supported dignity schemes;
- topic rulership / house lord placement.

Different ancient authors or house conventions are separate specifications, not silently blended.

### 2. Medieval / Renaissance Western

Possible canonical source:
- William Lilly, *Christian Astrology*, with earlier sources separated where they disagree.

Candidate techniques:
- essential dignities/debilities;
- accidental strength;
- reception;
- traditional aspects and source-specific orbs;
- angular/succedent/cadent condition;
- house rulership.

If Lilly supplies a numerical dignity table, its historical points may be used **as a secondary faithful-source specification**, not rewritten into project-specific weights.

### 3. Parashari Jyotish

Possible canonical source:
- *Brihat Parashara Hora Shastra* in a declared edition/translation.

Candidate techniques:
- source-declared planetary significations;
- rāśi/sign framework;
- house judgments and lords;
- graha/planetary aspects;
- exaltation/debilitation and source-declared strength measures;
- divisional charts only when the source/edition and birth-time precision rule are frozen.

Sidereal reference/ayanamsha is a material specification choice and must be predeclared; competing established ayanamshas should be treated as separate specifications rather than selected after owner scoring.

### 4. Modern psychological Western — optional later arm

A modern psychological tradition (for example the Liz Greene / Jungian school) is clearly established in practitioner literature, but its rules are substantially more narrative and therefore harder to convert into a deterministic birth-time scorer without reintroducing interpretive freedom. It should be a later arm unless a sufficiently explicit source-backed rule registry can be frozen.

## Do not mix features ad hoc

Do **not** build one score by taking:
- a Hellenistic rule that helps one owner trait;
- a Jyotish rule that helps another;
- a modern psychological interpretation that helps a third;
- then choosing custom numerical weights.

That is another garden of forking paths.

Instead:
1. each tradition is implemented independently;
2. each tradition receives equal status at the comparison layer;
3. disagreement is preserved;
4. no tradition is dropped because it fits the owner poorly after reveal.

## Weighting rule

### Primary no-arbitrary-weight baseline

Within each tradition:
- translate source rules into standardized behavioral domains while target-blind;
- each measured domain contributes at most one unit per tradition;
- multiple source rules that all predict the same domain do not stack;
- explicit counterevidence counts symmetrically;
- unknown/unmeasured domains abstain;
- no project-invented salience/directness coefficient.

This is an **equal-domain vote**, not a probability.

### Source-native-weight sensitivity arms

When a historical tradition itself publishes an explicit weighting/strength scheme, run it as a separate sensitivity specification exactly as published.

Do not call source-native historical weights empirically validated; their value is provenance and independence from this owner case.

### Cross-tradition combination

Primary report should show each tradition separately.

If a single summary is needed, prefer:
- median normalized rank across traditions; or
- count of traditions placing the candidate within predeclared rank bands.

Do not optimize cross-tradition weights on the owner case.

## Source-to-domain translation

This remains the main unavoidable interpretation layer.

Control it by:
1. freeze a behavioral-domain ontology before candidate scoring;
2. provide source excerpts/rules to two independent coders with birth/candidate/owner-target information withheld;
3. map only meanings directly supported by the source;
4. preserve disagreement and abstention;
5. one source rule may map to multiple domains only when the text explicitly supports them;
6. do not infer latent modern psychology absent from the source.

The owner case may be used afterward as development evidence, never as the reason a source rule maps to a domain.

## Specification-curve / multiverse design

Use the research-methodology idea of specification-curve or multiverse analysis:

- enumerate the set of theoretically justified, historically defensible, non-redundant astrology specifications;
- run all of them;
- show the owner rank under every specification;
- identify which legitimate interpretive choices materially move the result;
- do not privilege the best-fitting specification post hoc.

This directly measures whether the owner recovery is robust to astrology's genuine interpretive plurality or depends on one convenient interpretation.

External methodological baselines:
- Simonsohn, Simmons & Nelson (2020), *Specification curve analysis*, Nature Human Behaviour.
- Steegen, Tuerlinckx, Gelman & Vanpaemel (2016), *Increasing Transparency Through a Multiverse Analysis*.

## Owner-case diagnostics before fresh validation

The owner remains development data. Useful internal diagnostics that do not create scientific validation:

1. **Tradition convergence**
   - Does 1985 rank strongly under multiple independently frozen traditions?

2. **Specification robustness**
   - What fraction of all legitimate specifications place 1985 above 2013?
   - What fraction recover the correct local date/time neighborhood?

3. **Leave-one-domain-out**
   - Remove each behavioral domain in turn.
   - Does recovery survive, or does one hand-mapped domain carry the result?

4. **Equal-weight versus source-native-weight**
   - If recovery disappears when the arbitrary V1.1-derived weights are removed, treat that as a warning.
   - If equal-domain and source-native variants converge, the result is less weight-sensitive.

5. **Mapping permutation negative control**
   - Randomly permute source-rule ↔ behavioral-domain assignments while preserving counts/dependency structure.
   - Estimate how often flexible but meaningless mappings can produce ranks as strong as the observed owner rank.
   - This does not validate astrology, but it quantifies how easy the architecture is to overfit.

## Scientific boundary

This architecture is a stronger foundation because it reduces project-authored degrees of freedom and makes astrology's existing interpretive traditions explicit.

It is **not** empirical validation of those traditions.

Scientific predictive validity still requires:
- freeze all traditions/specifications before new cases;
- fresh participants whose birth outcomes did not influence any model choice;
- blinded behavioral translation;
- preregistered evaluation and baselines;
- no dropping poorly performing traditions after reveal.

## Proposed disposition

**COMPOSE + EXPERIMENT.**

Reuse established astrological systems as model specifications; invent only the source-to-domain normalization and cross-model evaluation layer.

The strongest immediate experiment is not another custom V1.2 weighting pass. It is:

> Re-score the owner under a small, predeclared tradition-grounded multiverse, with a primary equal-domain/no-custom-weight baseline, and compare robustness to the existing V1.2 result.

This is a new development objective and is not automatically active merely because the current V1.2 owner target was satisfied.
