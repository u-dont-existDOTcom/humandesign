# Life Patterns current state — 2026-09-14

V2 independent semantic review: **PASS**.

- Candidate head: `10d57a19b96f38303b2a30abff4281d6abfff83b`
- Blocking semantic findings: `0`
- Semantic change required: `false`
- Adapter-firewall repair head: `75c2fa4366e2721dc257ec839532b10f54f1de20`
- Bounded v2 core implementation verified: `true`
- Hidden-ledger conversational base head: `a642a1f907b20dd3da6d8219430b9b12dd3d3301`
- Pattern-first runtime repair head: `67b038b27d62b941b6beb224c6e89efd0d165bb4`
- Multi-pattern continuation head: `da3c5f58101d8cc10421e480d44b5162bd12ec78`
- Hosted continuation CI: `34864954177` — `success`
- Railway continuation deployment: `4ed43b5a-7249-4cc3-ad2e-1e1401ea0788` — `success`
- Unresolved-thread continuation repair head: `21d6a4addfd5549ef2d81ce694e8e127bd3eecce`
- Hosted unresolved-thread repair CI: `34872101510` — `success`
- Railway unresolved-thread repair deployment: `a1aa5bdf-82f9-4e71-b7c9-9268eecea894` — `success`
- Rejected-synthesis continuation repair head: `3536bf88f422551abfb9ff41f63e5690ecdb77e4`
- Hosted rejected-synthesis repair CI: `34876597710` — `success`
- Railway rejected-synthesis repair deployment: `28e06edc-3266-435d-8830-8adceabfe281` — `success`
- Active task: `life-patterns-v2-owner-multi-pattern-continuation` — OWNER REAL-DATA BROWSER JUDGMENT REQUIRED

## Owner product judgment and strategy history

The first deployed real-data browser produced direct negative strategy evidence. The owner judged the surfaced fact-review flow low-value because it mainly showed that the AI could understand/paraphrase what the owner said and ask the owner to certify the paraphrase. That owner-facing strategy is **FAILED / REPLACED**; the accepted v2 evidence contract remains valid internally.

The replacement hidden-ledger conversation was then repaired back to a **pattern-first** interview with concrete episodes serving as evidence anchors. A full bounded real owner session later produced useful non-parroting information gain and was judged **GOOD / PASS / PRELIMINARY POSITIVE**.

Repeated-thread testing has since exposed two state-machine/liveness defects rather than a demonstrated failure of the pattern-first strategy:

1. uncertainty after a tentative synthesis was terminalized as `unresolved` instead of allowing same-thread continuation;
2. an explicitly wrong tentative synthesis was terminalized by `No` as a final rejection instead of allowing the underlying pattern inquiry to continue.

Both recovery defects are now repaired on the owner-only surface and await direct owner retest.

## Current participant-facing method

Current architecture:

`participant-reported pattern -> minimal concrete anchor(s) / contrasts / life-phase evidence -> hidden v2 evidence ledger -> discriminating follow-up / boundary check -> informative synthesis -> participant authority -> immutable freeze`

The first participant pattern description is conversational context only. It does not fabricate an episode/fact/provenance record. Concrete situations may clarify, challenge, distinguish, or falsify the reported pattern.

The current synthesis panel distinguishes:

- `Yes — keep that`;
- `Close, but change it`;
- `No — keep investigating`;
- `Keep trying to pin it down`;
- `Leave it unresolved for now`;
- `Reject and stop this thread`.

`No — keep investigating` is a nonterminal disagreement with the current synthesis. It preserves the same backend session/proposal inquiry and asks what the synthesis gets wrong or misses. `Reject and stop this thread` is the explicit terminal rejection action.

Post-proposal participant material remains post-proposal evidence. It may guide continued questioning but may not silently become immutable preproposal support. Neither uncertainty continuation nor rejected-synthesis continuation automatically creates a replacement person-level proposal. Changed participant-authoritative wording still uses the explicit revision/adjudication route.

Target-theory blindness remains binding: no astrology or predictive-power language appears before behavioral lock. Private narrative remains process-memory/browser-local; no automatic transcript persistence or request-body logging has been added.

## Verification / deployment

Rejected-synthesis recovery implementation head: `3536bf88f422551abfb9ff41f63e5690ecdb77e4`.

GitHub Actions run `34876597710`: **SUCCESS** — unit/integration tests, Ruff, and strict mypy passed.

The committed source was inspected at the consumer seam: `No — keep investigating` calls the nonterminal `/patterns/disagree` endpoint, while `Reject and stop this thread` alone invokes terminal `decision('reject')`.

A dedicated new reject-path regression file could not be committed because the GitHub write interface blocked the attempted test-file writes. This remains explicit targeted verification debt rather than being treated as covered by the full-suite green result.

Existing authenticated owner-only Railway service reused. Deployment `28e06edc-3266-435d-8830-8adceabfe281` from application source head `3536bf88f422551abfb9ff41f63e5690ecdb77e4` is **SUCCESS**. Runtime startup completed and `/healthz` returned HTTP `200`; the deployed health contract includes `rejected_synthesis_continuation=true`.

No new service, broadened access, persistence layer, or target-model activity was introduced.

## Current gate

One-pattern repaired strategy evidence: **GOOD / PASS / PRELIMINARY POSITIVE**.

Repeated-thread recovery: **TWO LIVENESS DEFECTS FOUND AND REPAIRED; OWNER RETEST REQUIRED**.

Next gate: **OWNER REAL-DATA BROWSER JUDGMENT REQUIRED**.

1. Test a thread where the first synthesis is actually wrong and choose `No — keep investigating`.
2. Explain what is wrong or missing and judge whether the interviewer productively stays with the same inquiry.
3. Use a terminal judgment only when genuinely ready to end/settle the thread.
4. Use `Finish for now` and judge whether the summary is useful enough to justify durable persistence / a real Life Patterns Map.

Optional copy/export remains owner-triggered. Automatic transcript logging remains out of scope.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

**There was never a completion policy.**
