# Life Patterns human UI — direct-choice correction — 2026-09-09

Status: controlling presentation correction before any qualifying independent human first pass.

## Owner-observed defect

After the earlier state-label clarification, the UI asked whether there was **“Enough information to code”** before showing the human what concrete behavioral values they would be coding.

That is still backwards. A human cannot judge whether the source contains enough information **for an unspecified downstream choice**.

This is the same class of defect exposed by earlier review: the interface was asking the human to reason about the annotation machinery rather than simply make the behavioral judgment.

## Correct human task

Do not ask a meta-applicability question first.

Show the actual behavioral choices immediately and ask:

> **Which behavior or behaviors does the exact source clearly show?**

The human can then:

- select one or more concrete behaviors that are clearly supported;
- choose **Doesn't apply to this story** when the behavioral question's prerequisite situation is clearly absent;
- choose **Not enough information** when some pieces may fit but the exact source is incomplete or unclear enough that no behavioral value can be selected reliably.

The machine-facing state is derived:

- one or more selected behaviors -> `observed`;
- Doesn't apply -> `not_applicable`;
- Not enough information -> `insufficient`.

The auditor should not have to know or reason about those machine state names.

## Why there is no generic Partially state

A generic `Partially` category conflates distinct cases:

1. the source clearly supports only some of several possible behavioral values — select those supported values;
2. the prerequisite/situation is only partially established or the source is incomplete — use Not enough information;
3. multiple behaviors clearly occur — select multiple values and, only then, answer the conditional order question;
4. the question's prerequisite is absent — Doesn't apply.

Those cases have different measurement meanings. A single Partially state would lose information rather than add it.

## Human-first rule

**Never ask whether evidence is sufficient for a downstream coding choice before showing the human the actual choice.**

Whenever possible, ask the substantive judgment directly and derive transport/schema state from that answer.

## Scientific boundary

This is presentation/control-flow correction only. It does not change:

- the exact private handoff;
- the 44 episode + 22 repeated-series selected units;
- any behavioral value or observable definition;
- `observed / insufficient / not_applicable` response semantics;
- recurrence-v2 semantics;
- calibration selection;
- response schemas;
- target-theory blindness;
- no-network requirement.

No human calibration labels existed when this correction was made.
