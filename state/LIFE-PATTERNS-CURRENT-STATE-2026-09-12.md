# Life Patterns current state — 2026-09-14

V2 independent semantic review: **PASS**.

- Candidate head: `10d57a19b96f38303b2a30abff4281d6abfff83b`
- Blocking semantic findings: `0`
- Semantic change required: `false`
- Adapter-firewall repair head: `75c2fa4366e2721dc257ec839532b10f54f1de20`
- Bounded v2 core implementation verified: `true`
- Hidden-ledger conversational base head: `a642a1f907b20dd3da6d8219430b9b12dd3d3301`
- Pattern-first runtime repair head: `67b038b27d62b941b6beb224c6e89efd0d165bb4`
- Hosted CI on pattern-first repair head: `success`
- Railway owner-only deployment ID: `842b13f2-66b2-435e-a918-dbc81cde00e7`
- Railway owner-only deployment status: `success`
- Active task: `life-patterns-v2-hidden-ledger-conversational-insight-probe` — OWNER CONVERSATIONAL INSIGHT JUDGMENT REQUIRED

## Owner product judgment and strategy history

The first deployed real-data browser produced direct negative strategy evidence. The owner judged the surfaced fact-review flow low-value because it mainly showed that the AI could understand/paraphrase what the owner said and ask the owner to certify the paraphrase.

That owner-facing strategy is **FAILED / REPLACED**. Correct semantics, green tests, and deployment remain supporting work but are not direct evidence of participant value.

The replacement hidden-ledger conversation correctly removed routine annotation work. Owner testing then exposed a live structured-output validation failure and recalled an earlier product-design decision that had been partially lost: the participant-facing interview had already been corrected to **pattern-first**, with concrete episodes serving as evidence anchors rather than as the primary object of the experience.

Continuity finding: `state/LIFE-PATTERNS-INTERACTIVE-INTERVIEW-CONTINUITY-FINDING-2026-09-14.md`.

## Current participant-facing method

Current architecture:

`participant-reported pattern -> minimal concrete anchor(s) / contrasts / life-phase evidence -> hidden v2 evidence ledger -> discriminating follow-up / boundary check -> informative synthesis -> participant authority -> immutable freeze`

The first participant pattern description is conversational context only. It does not create an `EpisodeV2`, episode fact, or source-provenance record. The interviewer then requests a representative real situation so evidence anchoring begins only when a real bounded situation is supplied.

Concrete situations may be used to clarify, challenge, distinguish, or falsify the reported pattern. The interviewer should ask one main question per turn and seek useful context boundaries, developmental change, exceptions, and contrasts rather than exhaustively mining detail.

The historical v8 pattern-first insight is restored without restoring a closed fixed taxonomy. Historical domains may be optional coverage scaffolding only. The accepted v2 open-world evidence contract remains authoritative.

Repair implementation receipt: `state/LIFE-PATTERNS-v2-PATTERN-FIRST-RUNTIME-REPAIR-IMPLEMENTATION-2026-09-14.md`.

Implementation:

- `src/hdmatch/api/life_patterns_v2_owner_pattern_first.py`
- base hidden-ledger conversation `src/hdmatch/api/life_patterns_v2_owner_conversation.py`
- UI `src/hdmatch/api/life_patterns_v2_owner_conversation_ui.py`
- deployment wrapper `src/hdmatch/api/life_patterns_v2_owner_deployed_app.py`
- regressions `tests/unit/test_life_patterns_v2_owner_pattern_first.py`

## Runtime repairs

The provider boundary now normalizes `hypothesis_proposition=null` and `evidence_fact_ids=[]` for `follow_up`, `request_contrast`, and `boundary_question` before strict `ConversationMove` validation. A real `surface_hypothesis` remains strict and still requires a proposition and evidence IDs.

Model-driven participant turns are now transactional. If extraction, planning, move validation, or post-processing fails, pre-turn conversation, hidden v2 record, episode/boundary flags, proposal-support state, and active-proposal state are restored.

Successful participant corrections remain append-only with lineage/provenance. Genuine absence is not silently inferred; the accepted absence route remains authoritative. Historical automatic person-level `/map` authority remains superseded and unused.

Focused completion command:

`python -m pytest tests/unit/test_life_patterns_v2_owner_pattern_first.py tests/unit/test_life_patterns_v2_owner_conversation.py tests/unit/test_life_patterns_v2_owner_app.py tests/unit/test_participant_adjudicated_v2.py -q`

## Verification / deployed owner-only probe

Exact code head `67b038b27d62b941b6beb224c6e89efd0d165bb4` passed GitHub Actions run `34854800932`: unit/integration tests, Ruff, and strict mypy all succeeded.

Existing authenticated Railway service reused at `life-patterns-owner-production.up.railway.app`.

Deployment `842b13f2-66b2-435e-a918-dbc81cde00e7` from source head `67b038b27d62b941b6beb224c6e89efd0d165bb4` is **SUCCESS**. Deployment logs show application startup complete and Railway's `/healthz` request returned HTTP `200`. Basic authentication remains on owner-facing routes; runtime model credentials remain Railway references rather than repository secrets.

## Current gate

Repaired-surface direct outcome evidence: **NOT YET MEASURED**.

Next gate: **OWNER CONVERSATIONAL INSIGHT JUDGMENT REQUIRED**. Start a fresh owner-only browser session and judge whether the repaired interviewer creates a nontrivial context distinction, developmental change, counterexample/boundary, contrast, or synthesis that was not simply handed to it verbatim.

If the experience remains primarily paraphrase plus confirmation, fail the strategy rather than polishing the UI.

Authorized: bounded owner-only testing and owner-initiated runtime model use.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

**There was never a completion policy.**
