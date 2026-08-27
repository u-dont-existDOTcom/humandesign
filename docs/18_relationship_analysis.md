# 18 — Relationship / Connection Analysis Module

## Purpose

Add a second, explicitly separate Human Design research module for pair relationships.

This module asks a different question from natal reverse matching:

> Given two independently calculated natal charts, do the deterministic connection-chart mechanics describe observed relationship dynamics with useful specificity?

It MUST NOT add points to the natal V4.3 `NetInformation` score. Relationship evidence is a separate output and a separate validation track.

## Primary source

The initial symbolic mechanics are based on Ra Uru Hu's 2005 IHDS course **Partnership Analysis**.

The source emphasizes the observable/surface connection mechanics first. It does not provide a scientifically calibrated compatibility probability and does not justify a generic soulmate score.

## V1 analysis hierarchy

### 1. Know each individual chart first

Preserve for each partner:

- Type;
- Authority;
- Profile;
- Definition;
- all active Gates;
- complete Channels;
- Sun/Earth and Node activations needed for higher-level context.

Do not infer a partner's entire psychology from the connection chart.

### 2. Combined Center configuration

Build the connection chart from the union of both partners' active Gates and derive complete Channels and defined Centers.

Preserve Ra's five named surface configurations exactly as labels, not numerical quality scores:

| Defined + open Centers | Ra shorthand |
|---|---|
| 9 + 0 | `Nowhere to go` |
| 8 + 1 | `Have some fun` |
| 7 + 2 | `Work to do` |
| 6 + 3 | `Better to be free` |
| 5 + 4 | `Not a relationship anymore` |

If a composite falls outside a sourced named configuration, report the actual Center count and leave the keynote unresolved rather than inventing one.

### 3. Composite Definition / splits

Derive the connection chart's connected Center components exactly.

Report:

- single definition;
- split definition;
- triple split;
- quadruple split;
- or no definition where mechanically applicable.

Do not hide a split because other relationship features look favorable.

### 4. Four connection modes

For every canonical Channel, classify the relationship mechanically:

**Electromagnetic**

- neither partner has the whole Channel;
- each supplies the opposite Gate;
- completes a Channel only in connection.

This is attraction/spark in Ra's framework, not proof of long-term compatibility.

**Dominance**

- one partner has the whole Channel;
- the other partner has neither Gate;
- the complete definition comes from one side.

**Compromise**

- one partner has the whole Channel;
- the other carries one Gate of that same Channel;
- preserve which partner has the whole Channel and which is compromised.

**Companionship**

- both partners independently have the whole Channel.

Also preserve shared individual Gates because Ra notes that shared Gates can carry companionship value even when a complete shared Channel is absent. Do not inflate them into additional independent Channels.

### 5. Type / Authority / Profile communication context

Report the two natal Types, Authorities, Profiles, and Definitions alongside the connection mechanics.

Do not turn Type-pair descriptions into deterministic relationship outcomes. Ra repeatedly returns partnership work to the two individuals operating according to their own mechanics.

### 6. Nodes and Sun/Earth context

Retain mechanically detectable Sun/Earth-to-Node Gate alignments and whether the Line also matches.

Treat these as higher-level geometry/context. In the source, a Sun/Earth-to-Node alignment can indicate that somebody belongs in another person's landscape; Ra explicitly warns that this does **not** imply that the person must be a lover or ideal partner.

Additional Nodal harmony/resonance rules should be added only after the exact source rules are frozen and tested.

## No compatibility scalar in V1

The V1 module MUST NOT emit:

- soulmate probability;
- percent compatibility;
- `good/bad relationship` score;
- a weighted sum chosen after inspecting a known couple.

Ra's system contains favorable and difficult mechanics simultaneously. A single scalar would silently add weighting assumptions that the source does not supply.

A future empirical track may learn predictive likelihoods from development couples, but those parameters must be frozen and evaluated on different couples.

## Unknown birth time

When one partner's date/location is known but birth time is not:

1. enumerate every exact natal chart-state interval intersecting that local civil day;
2. calculate the relationship analysis for every interval;
3. merge adjacent intervals only when the complete relationship fingerprint is identical;
4. report relationship mechanics invariant across the whole day separately from time-dependent mechanics;
5. never choose the birth time that produces the nicest relationship narrative;
6. if rectifying the partner's time, freeze concealed behavior-first discriminators before answers and rescore every interval.

This is the relationship analogue of the natal exact-state/blinding rule.

## Conflicting birth metadata

When supplied birth metadata contradicts itself — for example, an explicit civil date paired with a weekday that belongs to the adjacent date — do not silently repair the input or choose the variant that produces the most favorable relationship narrative.

1. preserve the explicit fields and identify the contradiction;
2. choose a primary interpretation only by a declared non-outcome rule, normally treating the explicit numeric date/time as primary over an auxiliary weekday label;
3. enumerate the smallest plausible alternative set implied by the contradiction;
4. calculate both natal and relationship mechanics for every plausible interpretation;
5. report invariant relationship mechanics separately from natal or pair features that change across interpretations;
6. keep the conflict unresolved until independent birth-record evidence settles it.

This is an uncertainty analysis, not rectification. Observed relationship fit must not be used to choose between contradictory birth records unless a separate blinded rectification protocol was frozen in advance.

## Privacy / third-party rule

Ra explicitly expressed concern about giving revealing partnership information about a partner who was not present.

Therefore:

- pair mechanics may be calculated from supplied data;
- when only one partner participates, emphasize how the connection affects the participating person's experience and the mechanics of the pair;
- avoid presenting speculative private psychological claims about the absent partner as established facts;
- do not publish partner birth data or relationship records without permission.

## Validation tracks

Keep these claims distinct:

### R0 — Engineering

Does the implementation classify Center configuration, splits, and connection modes correctly from known chart fixtures?

### R1 — Retrospective development

For known development couples, compare pre-existing relationship history with source-derived mechanics. This can improve questions and mappings but is not validation on those same couples.

### R2 — Unknown-time discrimination

Given one known chart and one partner with documented date/place but concealed time, can a frozen relationship questionnaire rank the true stable interval above alternatives?

### R3 — Untouched pair prediction

Freeze the relationship model on development couples, then test it once on untouched couples whose birth data and relationship outcomes were not used in fitting.

### R4 — Prospective state/context tests

Where a relationship mechanism makes a concrete context-dependent prediction, preregister the context/window and preserve misses.

## Implementation

The initial code lives under:

```text
src/hdmatch/relationship/
    analysis.py
    uncertain_time.py
```

`analysis.py` provides deterministic connection mechanics.

`uncertain_time.py` aggregates exact partner-time states and reports stable versus variable relationship mechanics.

Unit tests include a synthetic 8+1 split relationship with reciprocal Compromise, Dominance, and an Electromagnetic connection, plus an unknown-time state in which an extra Electromagnetic becomes time-dependent.

## Separation from natal V4.3

Relationship outputs MUST NOT modify the natal reverse-match target, mapping library, prevalence tables, or `NetInformation` ranking unless a future protocol explicitly defines a new independent validation experiment.

If relationship observations are ever used to rectify an unknown natal time, use a separate relationship model/version/hash and report the result as relationship-based rectification rather than natal behavioral recovery.
