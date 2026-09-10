# Life Patterns R05 facet-overlap / absence-semantics defect — 2026-09-10

Status: **pre-collection measurement/UI blocker**. No qualifying independent human first pass has begun. This record preserves the owner-raised defect before any target-model scoring or reveal.

## Owner-observed defect

In the current direct-choice human calibration UI, NBM-R05 displays a flat list including:

- `R05-O2 accepts one/default option without searching for alternatives`;
- `R05-R1 selects without reported comparison / first acceptable option`;
- `R05-R4 follows an explicit rule, prior commitment, or default`;
- other option-construction and resolution values.

The owner correctly observed two separate problems:

1. several displayed values appear to overlap;
2. `R05-O2` is treated by the generic non-action machinery as a “did not act” code even though the wording explicitly contains an affirmative act: **accepts** one/default option.

## What the frozen source actually says

The reconciled v1 codebook defines R05 as **two facets housed in one observable**:

- **Option-set facet** — how alternatives enter the consideration set (`R05-O1..O6`);
- **Resolution facet** — how selection, deferral, combination, or non-resolution occurs (`R05-R1..R9`).

Its reconciliation note explicitly says option generation and choice procedure remain separate coded facets because their evidence requirements differ.

Therefore the current flat human list suppresses a distinction already present in the frozen source. Some simultaneous selection across facets is expected and is not automatically an error.

However, `R05-O2` itself is structurally hybrid: **“accepts one/default option”** is affirmative selection language, while **“without searching for alternatives”** is an absence claim. That wording can overlap materially with at least:

- `R05-R1` (selects without reported comparison / first acceptable option), and
- `R05-R4` (follows an explicit rule, prior commitment, or default).

Whether this is acceptable complementary facet coding or creates redundant/double-counted measurement is a substantive theory-neutral codebook question and must be audited before human calibration.

## Why R05-O2 appears in the non-action registry

The frozen non-action classification prompt defines `non_action` by **dependency on an absence claim**, not by requiring the entire subcode to describe doing nothing. A subcode is classified non-action when its truth depends on establishing that some relevant action did not occur during a feasible opportunity/window.

`R05-O2` appears in the frozen compact non-action registry because its truth depends on establishing **no search for alternatives**.

So the classification may be defensible at the evidence-rule level, but the UI translation is wrong:

> `R05-O2` does **not** mean “the narrator did not act.” It means an affirmative acceptance/default-selection behavior plus an absence-of-search condition.

The four-part gate, if retained, applies to the **search-for-alternatives component**, not to action in general.

## Human-interface defect

The current generic wording:

> “Extra check for the ‘did not act’ behavior you selected”

is invalid for hybrid subcodes such as R05-O2. Generic gate prompts such as “was the action realistically possible?” are also underspecified because they do not tell the human which absent action must be established.

A human-facing interface must instead identify the precise absence proposition, for example for R05-O2:

- Did the narrator know that looking for other options was possible/relevant?
- Was there a real opportunity to look for alternatives before accepting?
- Was looking for alternatives realistically feasible?
- Does the exact source actually establish that they **did not look for alternatives** before accepting?

The interface must not label the narrator’s affirmative acceptance as non-action.

## Broader scientific concern

The screenshot suggests this is not only a wording defect. Before another auditor kit is produced, the project must audit the full neutral codebook for:

1. **facet suppression** — values from different facets flattened into one apparently mutually exclusive list;
2. **semantic overlap/nesting** — subcodes that may encode the same behavioral fact more than once;
3. **hybrid affirmative+absence values** — affirmative behavior whose truth also requires proving a missing action;
4. **absence-target ambiguity** — non-action gates where the exact absent behavior is not obvious to a human;
5. **sequence vs facet co-occurrence** — multiple values that coexist as different aspects of one episode rather than forming a temporal sequence;
6. **downstream double-count risk** — redundant subcodes potentially treated as independent evidence later.

This audit must be target-theory-blind. The theory-exposed owner/project chat may identify the defect and preserve examples, but it must not silently rewrite substantive neutral subcodes to improve downstream model fit.

## Required disposition before human collection

1. Suspend the current auditor kit for new human collection.
2. Run the frozen theory-blind overlap/absence audit in `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-PROMPT-v1-2026-09-10.txt` against the exact reconciled codebook + resolved non-action amendment.
3. Classify each finding as:
   - presentation-only;
   - response-contract limitation;
   - substantive codebook ambiguity/overlap.
4. For presentation-only findings, repair the human UI without altering frozen measurement semantics.
5. For substantive findings, create a new versioned theory-blind measurement revision before any human/automated labels are collected; preserve all historical artifacts unchanged.
6. Rebuild/re-freeze dependent package/handoff/UI only after the substantive boundary is resolved.

## Immediate design rules preserved from this defect

- Do not expose a multi-facet observable as if every listed value were one mutually exclusive answer set.
- Do not call an affirmative behavior “non-action” merely because the code includes an absence qualifier.
- When a code depends on absence, name the **specific absent action** being tested.
- Human-facing evidence gates must state the concrete proposition the human is evaluating.
- Do not make the human reverse-engineer a schema classification to understand ordinary behavior.

No target-model information was used to identify or characterize this defect.
