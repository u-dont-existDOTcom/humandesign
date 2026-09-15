# Life Patterns v2 owner person-specificity gate — 2026-09-15

Status: **IMPLEMENTED / VERIFIED / DEPLOYED — OWNER RETEST REQUIRED**.

## Owner finding

The owner identified a more basic product criterion than adaptive stopping: **recurrence alone does not make something a useful Life Pattern**. A statement such as a routine physiological response can recur reliably while carrying almost no information about what is characteristic of this person.

No private interview narrative is persisted here. The regression is represented only as a generic high-base-rate human-regularity case.

## Product criterion

The participant-facing Life Patterns product is intended to collect **person-specific signal**, not an inventory of everything that repeats.

A candidate pattern may be simple and may concern a common human dimension, but the retained formulation must contain some individual-differentiating structure such as timing, threshold, intensity, sequence, context sensitivity, exception structure, developmental change, or another meaningful discriminator.

Near-universal/high-base-rate human regularities with no such qualifier are low-signal and should not become person-level Life Patterns merely because they recur.

This is not a rarity requirement. When commonness or specificity is uncertain, the interviewer continues rather than filtering the candidate out.

## Causal regression

The immediately preceding adaptive-stopping repair correctly removed forced episode/counterexample quotas, but its regression suite still asserted that a generic recurring physiological pattern could be surfaced as a valid person-level pattern. The product had therefore fixed **burden** without yet fixing **specificity**.

That test encoded the wrong target and has been replaced.

## Repair

The deployed owner interview now adds a conservative person-specificity gate before episode evidence is collected.

- The opening asks for a pattern that seems characteristic of the participant rather than merely recurrent.
- The first candidate pattern is triaged target-theory-blind against ordinary general human regularities.
- Clearly generic/high-base-rate patterns with no individual-specific modifier are redirected immediately.
- Redirected generic candidates create no hidden episode or fact records.
- The participant may supply a genuinely characteristic qualifier or choose a different pattern.
- A common dimension with person-specific timing, threshold, intensity, context sensitivity, sequence, exceptions, or developmental change remains eligible.
- If specificity/commonness is uncertain, the candidate is admitted rather than rejected.
- The ongoing planner also carries the rule: **simple is fine; generic is not**.

The accepted v2 scientific substrate is unchanged. Event-level facts can be ordinary facts; this gate governs which participant-facing recurrence claims are worth elevating into Life Pattern proposals.

## Verification

Implementation:

- `src/hdmatch/api/life_patterns_v2_owner_reasoning.py`
- `tests/unit/test_life_patterns_v2_owner_reasoning.py`

Exact code/test head: `1ad5b09cf1ec872bcf7ec3c3dbd05136bca7fbf9`.

GitHub Actions run `34912457794`: **SUCCESS** — tests, Ruff, and strict mypy all passed.

Focused regression coverage now verifies that:

1. a clearly generic recurring physiological pattern is redirected before any episode/fact evidence is created;
2. a later person-specific qualifier can cleanly become the active pattern focus;
3. one grounded episode plus a genuinely person-specific recurring self-report may still support a tentative pattern;
4. a single isolated occurrence still cannot be silently promoted into recurrence;
5. unknown counterexamples do not force further interrogation.

## Deployment

Existing authenticated owner-only service reused.

- deployment: `bc741597-51c1-44ec-be21-17e5495b15af`
- application source head: `5dc35711105c88a681e843558448b2389c758276`
- status: **SUCCESS**
- application startup complete
- Railway `/healthz`: HTTP `200`
- health contract now includes `person_specificity_gate=true`

No new service, broadened access, persistence layer, target-model activity, or automatic transcript logging was added.

## Next decision-changing evidence

Owner browser retest should start with a deliberately generic high-base-rate regularity. PASS requires immediate low-burden redirection before episode collection. Then test a genuinely characteristic qualifier or a separate nuanced pattern and confirm that the interviewer still probes when additional information can materially change a person-specific formulation.

**There was never a completion policy.**
