# Life Patterns current state — 2026-09-15

V2 independent semantic review: **PASS**. Semantic change required: `false`.

Current active task: `life-patterns-v2-owner-multi-pattern-continuation` — **OWNER REAL-DATA BROWSER JUDGMENT REQUIRED**.

## Scientific substrate

The accepted v2 hidden evidence contract remains unchanged: open-world episode facts, append-only correction/provenance, genuine-absence gating, immutable evidence timing, target-theory blindness, participant authority over person-level patterns, and the episode-fact/person-pattern firewall.

The participant-facing interview is allowed to be simpler and more selective than the internal evidence machinery. The v2 contract does not require a fixed number of episodes, a mandatory counterexample, explanatory novelty, or acceptance of every recurring statement as a useful person-level Life Pattern.

## Direct product evidence and strategy status

Earlier owner testing established:

- surfaced fact/paraphrase review: **FAILED / REPLACED**;
- hidden-ledger pattern-first interview: **GOOD / PASS / PRELIMINARY POSITIVE** at the bounded one-pattern level;
- uncertainty/rejected-synthesis continuation defects: repaired;
- mandatory multi-episode/counterexample/audit scaffold: **SUPERSEDED** after owner testing showed severe over-interrogation;
- adaptive information-gain / burden rule: restored and deployed.

The owner then identified a deeper target error in the adaptive candidate: **a recurring statement can still be useless as a Life Pattern when it is a high-base-rate human regularity that says almost nothing about the individual**.

The prior regression suite explicitly allowed a generic recurring physiological regularity to become a person-level proposal. That encoded the wrong product target and has now been replaced.

## Current specificity-aware adaptive interviewer

Receipts:

- `state/LIFE-PATTERNS-v2-OWNER-ADAPTIVE-STOPPING-REPAIR-2026-09-14.md`
- `state/LIFE-PATTERNS-v2-OWNER-PERSON-SPECIFICITY-GATE-2026-09-15.md`

Participant-facing behavior now follows:

`participant-reported candidate -> person-specificity triage -> enough concrete evidence to clarify/challenge -> only decision-changing follow-ups -> narrow person-specific synthesis -> participant authority`

The key distinction is:

- **recurrence**: the thing repeats;
- **person-specific signal**: the formulation tells us something characteristic of this participant rather than merely describing an obvious human regularity.

Current controls:

- the opening asks for something characteristic of the participant, not merely recurrent;
- clearly generic/high-base-rate candidates with no individual modifier are redirected **before episode evidence collection**;
- redirected generic candidates create no hidden episode/fact records;
- common dimensions remain eligible when timing, threshold, intensity, sequence, context sensitivity, exception structure, developmental change, or another meaningful discriminator makes the pattern person-specific;
- the gate is conservative: uncertain specificity/commonness is admitted rather than rejected;
- no rarity/eccentricity requirement;
- **simple is fine; generic is not**;
- no fixed episode quota;
- no mandatory counterexample/boundary gate;
- a follow-up is justified only if plausible answers can materially change meaning, scope, context, timing, exception structure, uncertainty, or person-specific information value;
- unknown/not remembered/inapplicable/declined can remain unresolved without reopening;
- no restating information already supplied;
- no unobservable internal-state distinctions merely because they are theoretically possible;
- no unsupported factor ranking or cross-context projection;
- explanatory novelty is not required;
- one grounded episode plus an explicit person-specific recurring self-report can support a tentative person-level proposal;
- one isolated occurrence still cannot silently establish recurrence;
- rejected-synthesis recovery remains model-led;
- post-proposal evidence remains post-proposal evidence.

The hidden second-pass hypothesis audit remains disabled because direct owner evidence showed the stricter scaffold increased burden. Person-specificity is handled at first-pattern admission plus the primary planner contract rather than by restoring that second audit.

## Verification / deployment

- specificity-aware code/test head: `1ad5b09cf1ec872bcf7ec3c3dbd05136bca7fbf9`;
- GitHub Actions run `34912457794`: **SUCCESS** — tests, Ruff, strict mypy;
- Railway owner-only deployment: `bc741597-51c1-44ec-be21-17e5495b15af` from application source `5dc35711105c88a681e843558448b2389c758276`: **SUCCESS**;
- application startup complete;
- `/healthz` -> HTTP `200`;
- health contract includes `person_specificity_gate=true`, `adaptive_information_gain_gate=true`, `fixed_episode_quota=false`, `mandatory_counterexample_gate=false`, `hypothesis_support_audit=false`.

Privacy/access boundaries are unchanged: no automatic transcript persistence, no Railway volume, no request-body logging, no broader participant access, and no target-model scoring.

## Current gate

Current strategy: **ADAPTIVE + PERSON-SPECIFICITY GATE — OWNER RETEST REQUIRED**.

1. Submit a deliberately generic/high-base-rate human regularity. It should be redirected immediately before episode collection.
2. Then add a genuinely characteristic qualifier or choose a different nuanced pattern. It should proceed normally.
3. Test a simple but person-specific pattern and confirm the interviewer does not manufacture depth merely because it is simple.
4. Test a genuinely nuanced/context-dependent pattern and confirm it still asks a discriminating question when the answer would change the formulation.
5. Confirm that `I don't know` and unobservable distinctions are not repeatedly reopened.
6. If a synthesis is wrong, use `No — keep investigating` and judge whether recovery is intelligent and low-burden.
7. Judge `Finish for now` summary utility before authorizing durable persistence / a real Life Patterns Map.

Still closed: external participant collection, automated participant coding, target-model activity, broader public deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

**There was never a completion policy.**
