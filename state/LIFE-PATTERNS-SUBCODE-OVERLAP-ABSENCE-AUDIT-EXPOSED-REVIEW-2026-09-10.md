# Life Patterns overlap / absence audit — exposed review

Date: 2026-09-10

Status: public-safe post-freeze review of the complete target-theory-blind audit. This record does **not** revise the neutral codebook. It decides only the next scientific process after the blind audit was frozen.

## Frozen blind audit authority

Audit commit:

`7ea0641e0913815306f8c182be5e7e8b18115fff`

Files:

- `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-RAW-v1-2026-09-10.jsonl`
  - 134 findings
  - worker-reported SHA-256 `37642f31135f3d446488a3a0a6736468b30b6114d5a292bcaf01096d65fb16e6`
  - worker-reported bytes `83030`
- `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-SUMMARY-v1-2026-09-10.json`
  - worker-reported SHA-256 `7184f89a9d6c8fa0560e0ceba07287f101f559ddcf872b3db62e39de34cb7b47`
  - worker-reported bytes `1170`

Mechanical validator: PASS.

GitHub Actions run `34472686547` on the audit commit: SUCCESS.

The failed earlier transport run remains non-authoritative and is not used here.

## Audit result

The frozen summary reports:

- 22 observables reviewed;
- 134 material findings;
- 48 presentation-only findings;
- 5 response-contract limitations;
- 40 substantive-codebook-overlap findings;
- 41 no-change-needed findings;
- 45 blocking findings;
- `human_calibration_safe_to_start_without_revision = false`;
- R05 disposition = `versioned_codebook_clarification`.

The 45 blocking findings affect 16 of the 22 observables:

`R02, R03, R05, R06, R07, R10, R11, R12, R13, R14, R15, R16, R18, R19, R20, R21`.

The six observables with no blocking finding in this audit are:

`R01, R04, R08, R09, R17, R22`.

## Five response-contract blockers

The audit identifies exactly five explicit response-contract limitations:

- `OA-029` — R05;
- `OA-034` — R07;
- `OA-085` — R16;
- `OA-114` — R20;
- `OA-121` — R21.

The common defect is structural: the current top-level relation field (`single / ordered_sequence / unordered_multiple`) applies one relation to an entire selected-value set. It cannot faithfully represent a case where:

- values from separate facets are simultaneously true/co-present; and
- some values within the same episode also have meaningful temporal order.

The next contract therefore needs facet/event-aware representation rather than forcing every selected value into one global relation.

## Representative substantive blockers

This review does not resolve the blind findings itself. The following examples establish why UI-only repair is insufficient:

### R02

`OA-007` / `OA-008`: stopping a search and proceeding (`R02-f`) can overlap with deliberately forgoing further information (`R02-g`), allowing one search-termination decision to be coded twice without a specificity/precedence rule.

### R03

`OA-011`: explicit delay pending information/condition versus no focal action in a feasible window has an unclear boundary. The codebook does not say whether affirmative deferral excludes the no-action value or whether they may both apply to different propositions/windows.

### R05

The owner's UI observation is confirmed and broadened:

- `OA-017`: option-set construction and resolution are distinct facets, but `R05-O2` crosses the facet boundary;
- `OA-019`: `R05-O2`, `R05-R1`, and `R05-R4` materially overlap in default/first-acceptable cases;
- `OA-020`: `R05-R1` includes `without reported comparison`, which can turn missing report content into an apparent behavioral fact;
- `OA-021`: `R05-O2` is affirmative acceptance/selection **plus** the absence condition that no alternative search occurred;
- `OA-026` / `OA-027`: comparison, explicit constraints, and rule/default resolution lack a clear cumulative-versus-specificity rule and can double-count one decision;
- `OA-029`: the current response relation cannot represent facet co-presence plus within-facet sequence.

### R06 / R12

`OA-033` and `OA-065` identify another recurring defect class: wording such as `without a replacement reported` / `replacement unknown` is missingness, not established behavioral absence. Unknown transcript content must remain unknown rather than becoming a substantive non-action claim.

### R07 / R10 / R11

- `OA-037` / `OA-039`: basic material preparation versus prepositioning resources has an underdefined boundary and double-count risk;
- `OA-049` / `OA-050`: finish-current-first, block allocation, alternation, and general sequencing contain nested/overlapping temporal allocation descriptions;
- `OA-058`: stopping pursuit and no-return-within-window can encode one terminal course twice without a precedence/window rule.

### R15

R15 is a major repair area. `OA-076` through `OA-084` show that completion extent, timing, explicitly open elements, stopping/withdrawal, later return, and noncompletion can describe different aspects/stages of one endpoint trajectory. Without explicit event/window/facet and specificity rules, one trajectory can generate several apparent independent observations.

### R16

`OA-085` confirms the response-contract problem: request timing, direct/indirect initiation, acceptance/use, help type, source breadth, and nonrequest are different facets/temporal stages. `OA-092` adds a substantive overlap among indirect signaling, waiting without a direct request, and the general no-request code.

### R18–R21

The audit repeatedly finds composites, nested values and hybrid affirmative-plus-absence codes:

- R18: partial/indirect/selective/withheld communication can overlap and invite inference about omitted content (`OA-103`, `OA-105`, `OA-106`);
- R19: exception-seeking is nested inside negotiation, and composite accept-then-renegotiate/withdraw values duplicate their component actions (`OA-108`, `OA-109`, `OA-113`);
- R20: dialogue content, order, mechanism and escalation cannot share one global relation; repeated-position-without-engagement also requires an explicit absence target (`OA-114`, `OA-118`, `OA-120`);
- R21: repair content, channel, origin, timing and contact disposition require facet-aware representation; resumed contact without discussing rupture and no-repair overlap without a precedence rule (`OA-121`, `OA-124`, `OA-127`, `OA-128`).

## Exposed-review decision

**Do not patch another auditor UI against the existing codebook/response contract.**

The complete blind audit establishes that the problem is broader than presentation. A new versioned target-theory-blind measurement clarification plus response-contract revision is required before any independent human calibration is collected.

The exposed project context must not author the substantive neutral-codebook resolutions. The next substantive repair is delegated to a new target-theory-blind worker using the frozen audit as its problem statement.

## Required repair invariants

The repair must, at minimum:

1. preserve all historical v1/v2 artifacts unchanged;
2. explicitly resolve every one of the 45 blocking OA findings;
3. preserve or explicitly redefine facet membership and whether values are mutually exclusive, co-present, sequential, nested, or specificity alternatives;
4. never convert `not reported` / `unknown` into behavioral nonoccurrence without an exhaustive evidence frame;
5. for every absence-dependent or hybrid code, identify the exact absent proposition and apply the non-action gate only to that proposition;
6. separate affirmative behavior from an attached absence condition;
7. define specificity/precedence rules where general, narrow, and composite values otherwise double-count the same behavioral fact;
8. support facet co-presence and within-event/within-facet temporal sequence without imposing a false global order;
9. preserve exact-source provenance and existing observed/insufficient/not-applicable discipline;
10. make no use of target-model information, birth/chart data, target mappings, or model-fit results.

## Review topology

The next stages are deliberately separated:

1. **Fresh blind repair worker:** proposes the versioned codebook clarification, relation contract, and a 45-row blocker-resolution matrix. It does not implement the UI or run participant coding.
2. **Second fresh blind reviewer:** audits that proposal against the original codebook and all 134 findings, with special attention to all 45 blockers. It must return residual blockers and a pass/fail recommendation.
3. Only after the blind review passes may the exposed engineering context implement the accepted versioned measurement artifacts, regenerate package/handoff/UI, and resume owner usability review.
4. Only after the revised UI is accepted may the independent human first pass begin.

## Current boundary

Human calibration remains paused. All existing auditor kits remain superseded/historical and are not eligible for collection. Automated participant coding remains blocked until the eventual revised human first pass is frozen. Target-model scoring/reveal remains unauthorized.
