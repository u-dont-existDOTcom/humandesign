# Life Patterns v2 owner judgment UX finding 002 — 2026-09-13

Status: owner product feedback; no semantic change implied.

## Owner-observed problem

The owner found the prototype grounding check hard to understand after revising a candidate pattern to wording like “it depends how complex the task will be.”

The current prompt asks whether the wording “still stay[s] within what the example actually supports, rather than adding something the example never showed.” This exposes an internal evidentiary concept in abstract language and forces the owner to infer what is being tested.

## Intended distinction

The system is trying to distinguish two questions that should remain separate:

1. Does the revised pattern feel true of the participant?
2. Does this particular pre-proposal episode actually support the revised wording?

For a revision such as “it depends how complex the task will be,” the concrete evidentiary question is whether the episode itself shows that task complexity changed what the participant did. If that relation comes from broader experience instead, the wording may still be a useful participant hypothesis, but this episode alone should not be treated as grounding evidence for that broader relation.

## Required UX repair

Replace abstract grounding language with a concrete question tied to the changed claim. Preferred form for this prototype:

> Does this example actually show that the amount of complexity changes what you do, or is that something you know from other situations?

Owner-facing choices should be ordinary language, for example:

- `This example shows it`
- `That's from other situations`
- `I'm not sure`

If the owner says the broader wording comes from other situations, preserve the participant's wording as a hypothesis/discussion artifact but do not represent this episode as supporting that added relation. Do not imply the owner was wrong to add nuance.

## Product principle

Keep evidence semantics strict internally, but translate them into concrete questions about the actual claim. Do not expose abstract phrases such as “stay within what the example supports” when a direct claim-specific question is possible.
