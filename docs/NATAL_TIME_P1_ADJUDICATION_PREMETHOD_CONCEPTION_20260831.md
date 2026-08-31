# P1 adjudication pre-method conception

Status: frozen before checkpoint-12-specific search

## Problem boundary

P1 permits prior exposure to the target symbolic domain and rejects exposure alone as an
eligibility decision. It distinguishes exposure provenance from the risk that a prospective clean
author could reproduce the target ontology through semantic familiarity, technical familiarity,
self-concept integration, or intentional derivation.

The unresolved design problem is how a future process could represent evidence about those
different risks, preserve uncertainty and disagreement, and prevent contaminated access—without
turning belief, skepticism, reported accuracy, mismatch, curiosity, usefulness, or product interest
into automatic rules.

This conception does not classify a person, select an evidence standard, select an adjudication
process, or authorize human-facing work.

## Exposure and semantic contamination are different variables

Exposure records whether and how contact with the target domain occurred. Semantic contamination
concerns whether that contact may shape the concepts a person would generate independently.
Neither can be inferred reliably from the other without additional evidence.

Shallow contact may have little semantic effect. Deep technical knowledge may permit ontology
reproduction even when the person rejects the domain. Identity-defining integration or intentional
derivation is a distinct ineligibility basis. Missing or conflicting evidence is an unresolved
process condition, not proof of either eligibility or ineligibility.

## Role of blind adjudication

Blind adjudication is a holding boundary for cases with substantial semantic, technical, or
ontology-reproducing familiarity when no separate ineligibility basis has been established. It
must prevent such a case from receiving clean-author access unless a later authorized decision
receipt exists.

The eventual design may vary the information hidden from adjudicators, the independence of initial
judgments, the treatment of disagreement, and the separation between evidence custody and role
assignment. No variant is selected here.

## Candidate classification errors and biases

- Treating contact history as equivalent to semantic influence.
- Treating absence of a recorded exposure event as evidence of eligibility.
- Treating belief or disbelief as a proxy for ontology-reproduction capability.
- Treating a reported accuracy percentage as a decision rule.
- Overweighting polished self-description or familiarity with expected answers.
- Allowing adjudicators to infer identity, social relationship, or desired outcome from metadata.
- Applying different evidentiary standards to believers, skeptics, experts, or negative cases.
- Converting incomplete or conflicting evidence into a forced substantive outcome.
- Allowing a later reviewer to erase earlier evidence, access, recusal, or disagreement history.
- Allowing group discussion to create convergence before independent conceptions are frozen.
- Allowing role reassignment to conceal prior access to protected content.
- Allowing later knowledge of mapping outcomes to alter the original eligibility record.

## Candidate author-independence configurations

The architecture should be capable of representing, without selecting:

- one isolated conception source;
- multiple conception sources working independently in parallel;
- multiple independently frozen conceptions followed by a separately governed synthesis stage;
- separate or shared eligibility-adjudication structures; and
- replacement or recusal paths that preserve the complete earlier history.

These are option families only. No author count, adjudicator count, preferred configuration,
default, ranking, population, language, recruitment route, workload, compensation, budget, or
schedule is selected.

## Proposed role and evidence separation

The design should distinguish at least:

- eligibility-evidence custody;
- blind adjudication;
- clean construct authorship;
- protected-content custody;
- reliability evaluation; and
- later mapping evaluation.

Evidence collection, evidence custody, decision recording, role assignment, content access, and
later outcome evaluation should have separate provenance. A role change must append history rather
than replace it.

## Candidate structural mechanisms

- Closed metadata with explicit source, completeness, conflict, and supersession states.
- Append-only evidence, access, decision, recusal, replacement, and deviation events.
- Separate initial judgment and later resolution states.
- Masking dimensions represented explicitly rather than implied by a role label.
- Fail-closed access when an adjudication receipt is absent or internally inconsistent.
- Distinct preservation of negative, disputed, replaced, and unresolved determinations.
- Hash-bound custody and version records for every state transition.
- A neutral registry of author and adjudication configurations with no selected default.

These are candidate architecture elements, not a selected human process or classification
algorithm.

## Constraints and prohibited actions

- No human-facing question, prompt, interview guide, instruction, or consent text.
- No evidence threshold, cutoff, weighting rule, adjudication algorithm, appeal rule, or exception.
- No real identity, contact detail, narrative response, or person-level assessment.
- No role assignment, recruitment, burden, compensation, budget, or schedule.
- No construct, item, category, response choice, manual, or scoring rule.
- No target-domain mapping hypothesis, chart, birth time, relationship datum, or candidate interval.
- No production, external-system, publication, or release action.
- No model or repository context exposed to the target domain may author protected constructs.

## Independent candidate insights

1. Eligibility evidence and role access should be separate state machines; a substantive outcome
   alone should not silently grant access.
2. The object being adjudicated should be an evidence package version, not an informal impression
   of a person.
3. Disagreement is evidence about process uncertainty and should remain visible after resolution.
4. Independence is temporal as well as organizational: conception must freeze before synthesis or
   exposure to other authors' content.
5. Recusal and replacement reduce current conflict but do not erase earlier access or influence.
6. Negative and unresolved cases are scientifically informative and should not disappear from
   feasibility accounting.
7. Data minimization and auditability can conflict; the architecture should represent retention
   choices explicitly rather than assume maximal collection.
8. A configuration with more roles or judgments may improve separation while increasing cost,
   burden, coordination leakage, and feasibility risk.

## Open design decision points

- Eligible evidence-source classes and the minimum completeness needed for later adjudication.
- Masking boundaries for identity, belief-related metadata, exposure detail, and desired role.
- Independence requirements for initial judgments and any later synthesis.
- Permitted resolution states for disagreement, conflict, recusal, replacement, and deviation.
- Versioning and retention boundaries for evidence and decision records.
- Future author and adjudicator configuration.
- Population, language, geography, accessibility, recruitment, burden, compensation, budget, and
  schedule.
- Human-facing wording and evidence standards, which require later owner and Pro authorization.

All decision points remain unselected.
