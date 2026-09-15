# Current state

## Life Patterns — 2026-09-15

Active task: `life-patterns-v2-owner-multi-pattern-continuation` — **OWNER REAL-DATA BROWSER JUDGMENT REQUIRED**.

PR #24 remains **draft / open / unmerged**.

## Accepted scientific substrate

V2 independent semantic review remains **PASS** with zero blockers and `semantic_change_required=false`.

The accepted substrate is unchanged: open-world episode facts plus participant-adjudicated person-level patterns, append-only correction/provenance, genuine-absence gating, immutable evidence timing, target-theory blindness, and the episode-fact/person-pattern firewall. The participant-facing interview may be changed without weakening these internal semantics.

## Product strategy history

The surfaced fact-review/paraphrase workflow is **FAILED / REPLACED**.

The hidden-ledger pattern-first replacement completed a bounded real owner session successfully and was judged **GOOD / PASS / PRELIMINARY POSITIVE**. Multi-pattern continuation was added. Two later liveness defects were repaired: uncertainty after a synthesis no longer forces terminal unresolved, and `No` no longer terminates the entire inquiry unless the owner explicitly chooses `Reject and stop this thread`.

A later reasoning repair addressed unsupported comparative/cross-context synthesis. Direct owner testing then exposed a more fundamental regression: the interviewer had become severely over-interrogative even after the useful formulation was already clear. Repository comparison showed that later mandatory episode/counterexample/audit scaffolding had overridden the historical adaptive burden rules, so that scaffold was removed and adaptive stopping was restored.

The owner then identified an even more basic target error: **recurrence is not sufficient for a useful Life Pattern**. A high-base-rate human regularity can repeat perfectly while carrying almost no information about what is characteristic of this person.

No private owner interview narrative is committed; only abstract product findings are preserved.

## Current product criterion: person-specific signal

Repair receipt:

`state/LIFE-PATTERNS-v2-OWNER-PERSON-SPECIFICITY-GATE-2026-09-15.md`

The participant-facing product now distinguishes:

- **recurrence** — whether something happens repeatedly; from
- **person-specific information** — whether the formulation tells us something meaningfully characteristic of this participant rather than merely describing an obvious common human regularity.

A pattern may be simple and may concern a common human dimension. It does **not** have to be rare, unusual, dramatic, or surprising. But a retained Life Pattern should contain individual-differentiating structure such as timing, threshold, intensity, sequence, context sensitivity, exception structure, developmental change, or another meaningful discriminator.

Clearly high-base-rate physiological/situational regularities with no such modifier are low-signal and are redirected rather than elevated into person-level Life Patterns. If commonness/specificity is uncertain, the interviewer continues rather than filtering the candidate out.

The hidden evidence substrate remains open-world: ordinary event facts may still be valid facts. This is a participant-facing admission/synthesis criterion for what is worth treating as a Life Pattern.

## Current participant-facing strategy

The deployed owner interview now combines **person-specificity admission** with the restored adaptive information-gain / burden rule.

Current rules:

- opening asks for something characteristic of the participant, not merely recurrent;
- a first-turn target-theory-blind specificity gate runs **before episode evidence collection**;
- clearly generic/high-base-rate candidates are redirected immediately and create no hidden episode/fact records;
- the participant can add a characteristic qualifier or choose a different pattern;
- common dimensions with person-specific timing/threshold/intensity/context/sequence/exceptions/developmental change remain eligible;
- uncertain specificity is admitted rather than rejected;
- **no fixed episode quota**;
- **no mandatory counterexample/boundary gate**;
- another question is admitted only when plausible answers can materially change the retained person-specific pattern's meaning, scope, context, timing, exceptions, uncertainty, or information value;
- unknown, not remembered, inapplicable, or declined may remain unresolved without repeated drilling;
- do not ask participants to distinguish internal states they could not reasonably observe;
- do not restate or re-ask supplied information;
- additive factors remain additive unless comparative evidence exists;
- context-specific factors are not projected across contexts without support;
- explanatory novelty is not required;
- **simple is fine; generic is not**;
- one grounded episode may be sufficient when paired with an explicit participant-reported recurring, person-specific self-description;
- one isolated occurrence still cannot be silently promoted to recurrence;
- rejected-synthesis recovery remains model-led;
- post-proposal evidence timing and all accepted v2 scientific/privacy invariants remain unchanged.

## Verification / deployment

Specificity-aware adaptive implementation:

- `src/hdmatch/api/life_patterns_v2_owner_reasoning.py`
- `tests/unit/test_life_patterns_v2_owner_reasoning.py`

Exact code/test head: `1ad5b09cf1ec872bcf7ec3c3dbd05136bca7fbf9`.

GitHub Actions run `34912457794`: **SUCCESS** — tests, Ruff, and strict mypy all passed.

Regression coverage now includes the exact conceptual correction: a clearly generic recurring physiological regularity is redirected before any episode/fact evidence is created, while a subsequent genuinely characteristic qualifier can become the active pattern focus. It also retains protection against silently promoting one isolated event into recurrence and against reopening unknown counterexamples indefinitely.

Existing authenticated owner-only Railway service reused:

- deployment: `bc741597-51c1-44ec-be21-17e5495b15af`;
- application source head: `5dc35711105c88a681e843558448b2389c758276`;
- status: **SUCCESS**;
- application startup complete;
- `/healthz` -> HTTP `200`;
- health contract includes `person_specificity_gate=true`, `adaptive_information_gain_gate=true`, `fixed_episode_quota=false`, `mandatory_counterexample_gate=false`, `hypothesis_support_audit=false`.

No new service, broadened access, persistence layer, target-model activity, or private transcript logging was introduced.

## Current outcome / next gate

Outcome advancement: **PRELIMINARY POSITIVE, WITH RECURRENCE-VS-SPECIFICITY TARGET ERROR REPAIRED IN THE CURRENT OWNER CANDIDATE**.

Strategy efficacy: **ADAPTIVE + PERSON-SPECIFICITY CANDIDATE VIABLE; OWNER RETEST REQUIRED**.

Next owner test:

1. Submit a deliberately generic/high-base-rate human regularity. The interviewer should immediately explain that it carries little person-specific information and redirect **before collecting episode evidence**.
2. Then add a genuinely characteristic qualifier or choose a separate nuanced pattern. It should proceed normally.
3. For a simple but person-specific pattern, it should not manufacture depth merely because the formulation is simple.
4. For a nuanced/context-dependent pattern, it should still ask a discriminating question when different answers could materially change the formulation.
5. Confirm that `I don't know` and unobservable distinctions are not repeatedly reopened.
6. If a synthesis is wrong, use `No — keep investigating` and judge whether it repairs intelligently without requiring obvious restatement.
7. Use `Finish for now` and judge whether the session summary is useful enough to justify durable persistence / a real Life Patterns Map.

Owner-triggered copy/export remains available. Automatic transcript logging remains out of scope.

Authorized: bounded owner-only testing and owner-initiated runtime model use.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

**There was never a completion policy.**
