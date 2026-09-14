# Life Patterns current state — 2026-09-14

V2 independent semantic review: **PASS**.

- Candidate head: `10d57a19b96f38303b2a30abff4281d6abfff83b`
- Blocking semantic findings: `0`
- Semantic change required: `false`
- Adapter-firewall repair head: `75c2fa4366e2721dc257ec839532b10f54f1de20`
- Bounded v2 core implementation verified: `true`
- Prior real-data browser implementation head: `002d6264f05a7e380d4cac7e188f8c9455fbf971`
- Hidden-ledger conversational implementation head: `a642a1f907b20dd3da6d8219430b9b12dd3d3301`
- Hosted CI on hidden-ledger conversational head: `success`
- Railway conversational deployment ID: `aabaaaaf-5178-40a8-afe0-2150a6846f45`
- Railway conversational deployment status: `success`
- Active task: `life-patterns-v2-hidden-ledger-conversational-insight-probe` — OWNER CONVERSATIONAL INSIGHT JUDGMENT REQUIRED

## Owner product judgment and strategy replacement

The first deployed real-data browser produced direct negative strategy evidence. The owner judged the surfaced flow low-value because it mainly showed that the AI could understand/paraphrase an episode and ask the owner to confirm the paraphrase.

That owner-facing strategy is now classified **FAILED / REPLACED**. Correct semantics, green tests, and deployment remain valid supporting work but are not direct evidence of participant value.

Judgment: `state/LIFE-PATTERNS-v2-OWNER-REAL-DATA-PRODUCT-JUDGMENT-2026-09-14.md`.

Replacement implementation receipt: `state/LIFE-PATTERNS-v2-HIDDEN-LEDGER-CONVERSATIONAL-IMPLEMENTATION-2026-09-14.md`.

## Replacement surface

The accepted v2 evidence contract remains internal while the owner experiences a normal attentive conversation:

`episode -> discriminating follow-up -> deeper/contrasting evidence -> informative synthesis -> counterexample/boundary check -> natural correction -> compact pattern/limit judgment`

Implementation:

- `src/hdmatch/api/life_patterns_v2_owner_conversation.py`
- `src/hdmatch/api/life_patterns_v2_owner_conversation_ui.py`
- deployment wrapper `src/hdmatch/api/life_patterns_v2_owner_deployed_app.py`
- `tests/unit/test_life_patterns_v2_owner_conversation.py`

Routine fact checklists and keep/edit/reject controls are hidden. Literal/minimally normalized episode facts remain internal. Participant correction of a load-bearing hidden fact is append-only with correction provenance. Person-level synthesis still requires explicit participant adjudication through the frozen v2 path.

The interviewer asks at most one question per turn and is instructed to choose the next question for information gain rather than comprehension display. A formal cross-episode hypothesis is withheld until a boundary/counterexample check has been answered and must cite operative facts from at least two episodes. Invalid or premature synthesis falls back to more discriminating evidence collection instead of being surfaced.

Genuine absence is not silently inferred by the minimal hidden extractor; the accepted four-gate route remains authoritative. Historical automatic person-level `/map` authority remains superseded and unused.

Focused completion command:

`python -m pytest tests/unit/test_life_patterns_v2_owner_conversation.py tests/unit/test_life_patterns_v2_owner_app.py tests/unit/test_participant_adjudicated_v2.py -q`

## Deployed owner-only probe

Existing authenticated Railway service reused at `life-patterns-owner-production.up.railway.app`.

Deployment `aabaaaaf-5178-40a8-afe0-2150a6846f45` from source head `a642a1f907b20dd3da6d8219430b9b12dd3d3301` is **SUCCESS**. Deployment logs show application startup complete and `/healthz` HTTP `200`. Basic authentication remains on owner-facing routes; model credentials remain Railway references rather than repository secrets.

## Current gate

Replacement direct outcome evidence: **NOT YET MEASURED**.

Next gate: **OWNER CONVERSATIONAL INSIGHT JUDGMENT REQUIRED**. The owner should use the deployed conversation naturally and judge whether it creates a nontrivial distinction, contrast, boundary/counterexample, or cross-situation synthesis that was not simply handed to it verbatim.

If the experience remains primarily paraphrase plus confirmation, fail the replacement strategy rather than polishing the UI.

Authorized: bounded owner-only testing and owner-initiated runtime model use.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

**There was never a completion policy.**
