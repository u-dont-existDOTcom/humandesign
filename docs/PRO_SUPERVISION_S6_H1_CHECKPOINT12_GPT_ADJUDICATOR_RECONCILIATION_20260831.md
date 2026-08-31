# Pro supervision — checkpoint 12 GPT-adjudicator reconciliation

Date captured: 2026-08-31

## Direct owner ruling

> GPT itself will be adjudicating, there are no human authors who could adjudicate better than GPT currently.

The exact direct-owner bytes are preserved in
`state/NATAL-TIME-OWNER-GPT-ADJUDICATION-SOURCE-EPOCH7-20260831.json`; their SHA-256 is
`1b5b66c0e3dafb6ea0a0e2c109b3cf88ad764d40d1c34d9179cc3ce4d437a826`.

The worker relayed this owner correction verbatim to the existing Pro supervisor chat rather than
mapping it onto a human-adjudicator option. The Pro chat is `Scientific Audit Checkpoint` at
`https://chatgpt.com/c/6a937fe2-68a4-83e9-b92d-3b0f82799513`.

## Pro's leading decision

`OWNER DECISION REQUIRED: YES`

Pro ruled that the owner statement resolves the adjudicator actor class:

> Eligibility adjudication will be performed by GPT, not by human adjudicators.

This supersedes the checkpoint-12 owner-choice framing that treated `J1` and `J2` as human-staffing
choices. Those codes must not be applied unchanged. Checkpoint 12 itself remains accepted because
its neutral architecture assigned no real person or adjudicator; the defect was limited to the
subsequent owner-choice framing.

The ruling does not change:

- P1's three eligibility outcomes or five process states;
- the requirement that screened chart-blind humans create clean H1 construct content;
- the separation among evidence custody, adjudication, clean authorship, content custody,
  reliability evaluation, and later mapping;
- the prohibition on AstroHD-exposed model contexts authoring or revising clean constructs; or
- the later separately frozen AstroHD mapping lane and preservation of null, weak, unstable, or
  nonreplicating results.

The owner statement does not select a provider, model family/version, number of GPT runs, shared or
isolated contexts, evidence-access rules, prompt, evidence standard, threshold, disagreement rule,
or final-reconciliation procedure.

## GPT adjudication topology

Pro ruled that shared versus separated adjudication remains scientifically meaningful, but should
be expressed as **run and context independence**, not human staffing.

The central distinction is between one stateful GPT context producing a decision and several fresh
contexts that cannot see each other's reasoning or decisions, share no conversation memory,
receive independently provisioned but identically canonicalized admissible evidence, and commit
their initial outputs before reconciliation. Several contexts using the same model are separate
runs under a common model identity; they are not independent models.

Each future adjudication context must receive only evidence allowed by a separately frozen
adjudication contract. It must not receive another adjudicator output, construct content, AstroHD
mapping or chart information, outcome/progression information, or owner preferences about the
desired eligibility result. Evidence packets, prompt contract, model identity, run configuration,
access events, and committed outputs require provenance binding.

Reconciliation must be a separate post-commit stage that preserves every initial judgment and any
disagreement. The initial contexts may not edit their judgments after comparison. A future contract
must distinguish agreement, disagreement, unresolved evidence, and procedural invalidity, then use
a separately frozen rule or isolated reconciliation context.

Pro's scientific recommendation is:

> At least two independently blinded GPT contexts producing sealed initial judgments, followed by a separate reconciliation stage.

This is a later bounded implementation choice for Pro and Codex unless it creates a material cost,
latency, vendor, or operational commitment requiring the owner. It does not eliminate correlated
model error and is not evidence that GPT is task-specifically valid, reliable, unbiased, or superior.

## Only remaining owner choice

The direct owner statement decides who adjudicates eligibility but not how many screened
chart-blind humans independently create the initial construct conceptions. Pro therefore requires
only one of these choices:

### `A1` — one clean human author

One screened chart-blind person creates the initial conception. This is simplest and least
expensive, but most vulnerable to one person's vocabulary, culture, assumptions, and framing. It
provides no independent human conception for comparison.

### `A2` — two independent clean human authors

Two screened chart-blind people independently create separate conceptions without seeing or
discussing each other's work before both are frozen. This supplies a real independence check,
preserves convergence and disagreement, and avoids dependence on one author while remaining
manageable. Divergent conceptions require later governed handling.

### `A3` — an independent human panel

Several screened chart-blind people create separate frozen conceptions before synthesis. This
offers the most diversity and resilience to an atypical author, but has the greatest recruitment,
custody, coordination, compensation, and synthesis burden and more opportunities for protocol
deviation.

Pro recommends `A2` as the best balance of scientific independence and operational feasibility.
The exact number of GPT contexts, their model identity, and reconciliation mechanics do not need an
owner decision now.

**No next implementation child is authorized before Joel selects `A1`, `A2`, or `A3`.**

## Separate supervisory states

```text
worker_to_contract_alignment: GREEN
bounded_GPT_adjudicator_ruling_to_owner_alignment: MATCH
contract_to_owner_alignment: PARTIAL
completion_claim: BLOCKED_OWNER_DECISION
parent_outcome: OPEN
root_completion: false
operational_alignment: PASS
scientific_adequacy: WARN
release_adequacy: NOT_APPLICABLE
release_permission: false
```

No release, deployment, recruitment, human contact, construct work, reliability work, mapping, or
public action is authorized.
