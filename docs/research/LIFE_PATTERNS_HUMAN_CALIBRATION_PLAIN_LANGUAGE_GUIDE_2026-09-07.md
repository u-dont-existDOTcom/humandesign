# Life Patterns Human Calibration — Plain-Language Guide

Status: explanatory guide for the development-only blind human calibration workflow. This guide does not overwrite any frozen measurement artifact. As of 2026-09-08, human calibration on the existing episode-centric recurrence rule is paused pending the versioned recurrence-evidence correction in `state/LIFE-PATTERNS-RECURRENCE-EVIDENCE-CORRECTION-2026-09-08.md`.

## The most important distinction

**The independent human is not auditing the scoring of the owner's Survey-v2 answers.**

There are two separate measurement systems in this repository:

1. **Survey-v2 / natal reverse matching** — a frozen questionnaire/classifier/scoring system intended to test whether human narrative can identify or rank birth-derived Human Design states.
2. **Life Patterns neutral coding** — a theory-blind behavioral measurement system that converts autobiographical evidence into neutral behavioral observables before any Human Design target-model comparison.

The current `44 episode units + 22 series units` historical calibration bundle belongs to **#2, Life Patterns neutral coding**.

## What the independent human is actually checking

The automated Life Patterns coder and independent human are intended to apply the same neutral coding rules to the same selected evidence without the human seeing automated answers. The human judgment task is not the problem; the recurrence-evidence policy and machine-oriented delivery format both require correction before collection.

## The auditor should not edit JSON directly

The verified private handoff is a machine interchange artifact, not an appropriate default user interface. JSON/JSONL exists so the result can be deterministically validated and frozen. A theory-neutral local/offline annotation UI is required before eventual first-pass collection, but UI implementation is now downstream of the recurrence-evidence revision.

## Recurrence self-report and concrete incidents

A behavioral self-report such as **“I always X” is direct recurrence evidence**. Preserve it as such.

The critical correction is that a concrete incident elicited after that claim does **not** automatically add support for the frequency proposition. A selected example is conditioned on the participant already asserting the pattern; it is not an independent sample of opportunities.

Concrete incidents are useful when they add information about:

- what the participant means by `X`;
- behavioral sequence or process;
- prerequisites such as awareness/opportunity/feasibility;
- context dependence;
- consequences;
- exceptions or counterexamples;
- distinctions between competing interpretations.

A concrete counterexample can be especially informative because it can falsify a literal universal claim or reveal a boundary condition.

If the scientific target is the actual opportunity-level frequency of X, the appropriate evidence is a sampling design that is informative about opportunities — for example prospective diary sampling, structured/random opportunity sampling, or a bounded exhaustive opportunity set — not one or several volunteered confirming anecdotes.

Therefore **do not ask for concrete incidents merely to corroborate a generalized recurrence statement or satisfy an episode quota**.

There is also an important difference between:

- **behavioral recurrence:** “I always checked the door before leaving”; and
- **trait interpretation:** “I am always cautious.”

The first directly reports recurring behavior. The second primarily reports an interpretation/label and requires behavioral content if the target construct is behavior.

## Why the current calibration is paused

The current reconciled codebook's person-level recurrence rule requires multiple qualifying episodes or an episode plus an anchored repeated-series report. That is too episode-centric for generalized behavioral recurrence self-report.

Because no human first pass and no automated coding pass have yet occurred, the project should not spend a human calibration pass on a rule already recognized as conceptually defective. Preserve the old artifacts unchanged, create a new versioned theory-blind recurrence-evidence policy, regenerate the development package/handoff, then collect the human pass through a usable UI.

## What the eventual human receives

The eventual private bundle/interface must present only the revised frozen neutral behavioral evidence and rules, without Human Design/chart/birth/target-model information, expected answers, automated labels, or consensus.

## Blinding requirement

Before and during the first pass, the human must not have access to automated coding outputs, automated consensus, expected answers, Human Design/chart/birth information, target-model mappings/scores/rankings, or reveal results. Relevant prior exposure must be disclosed honestly.

## Relationship to Survey-v2

Survey-v2 remains separate. Life Patterns calibration never audits Survey-v2 scoring.
