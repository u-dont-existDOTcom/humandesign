# Life Patterns v2 hidden-ledger conversational insight probe — implementation receipt — 2026-09-14

Status: **IMPLEMENTED / DEPLOYED / OWNER CONVERSATIONAL INSIGHT JUDGMENT REQUIRED**.

## Why this replacement was made

The prior owner-facing fact-review workflow produced direct negative product evidence: it mainly demonstrated AI comprehension/paraphrase and made the owner certify internal evidence bookkeeping. That strategy is retained only as supporting research plumbing and regression coverage; it is no longer the owner-facing product method.

Controlling judgment: `state/LIFE-PATTERNS-v2-OWNER-REAL-DATA-PRODUCT-JUDGMENT-2026-09-14.md`.

## Exact implementation

- conversation backend: `src/hdmatch/api/life_patterns_v2_owner_conversation.py`
- conversational UI: `src/hdmatch/api/life_patterns_v2_owner_conversation_ui.py`
- authenticated deployment wrapper: `src/hdmatch/api/life_patterns_v2_owner_deployed_app.py`
- focused tests: `tests/unit/test_life_patterns_v2_owner_conversation.py`
- deployed source head: `a642a1f907b20dd3da6d8219430b9b12dd3d3301`
- GitHub Actions CI on that exact head: **SUCCESS** (tests, Ruff, mypy)

## Owner-facing behavior

The replacement surface exposes a normal free-text conversation rather than a fact checklist.

The interviewer:

- asks at most one question per turn;
- selects follow-ups for information gain rather than form completion;
- preferentially probes distinctions that could change the interpretation: mechanism, timing, alternatives, context, developmental change, exceptions, and contrasts;
- does not paraphrase merely to prove comprehension;
- can request a contrasting real situation instead of mining trivial detail from one example;
- requires a boundary/counterexample check before a formal cross-episode hypothesis is surfaced;
- surfaces a person-level hypothesis only when grounded hidden facts from at least two episodes support it and the proposition is not an exact restatement of a cited fact;
- leaves explicit participant judgment for the consequential person-level synthesis rather than routine ledger entries.

The UI explicitly tells the owner that if the experience still mostly paraphrases them, the strategy has failed again.

## Hidden v2 evidence ledger

Participant turns can create literal/minimally normalized `EpisodeFactV2` records internally. The participant is not required to certify them one by one.

When a later participant message explicitly makes an operative fact materially wrong or too broad, the correction is append-only: a new fact revision preserves `fact_lineage_id`, increments `revision_index`, references the immediate predecessor with `supersedes_fact_id`, and carries participant-correction provenance. Originals remain audit history.

This bounded conversational probe deliberately does not admit genuine absence facts through the hidden extractor. The accepted four-gate absence route remains authoritative rather than silently misclassifying absence.

## Person-level pattern boundary

A surfaced synthesis is converted into the existing frozen-v2 `PatternProposalV2` / `PatternEvidenceLinkV2` structure only after the conversational boundary check. Evidence links must cite operative facts from at least two episodes. Participant accept/revise/reject/unresolved judgment remains authoritative, and final accepted/rejected/unresolved records still run through the existing v2 validation/freeze/projection path.

The historical automatic `/map` / `OpenAILifePatternsMapper` person-level authority is not used.

## Target-theory blindness

The conversational module and its focused regression tests exclude Human Design, astrology, birth/chart, and historical mapping authority from interviewer context. The model receives only conversation and neutral hidden evidence relevant to the owner interview.

## Deployment

Existing owner-only Railway service reused; no new service was created.

- service: `life-patterns-owner`
- domain: `life-patterns-owner-production.up.railway.app`
- deployment ID: `aabaaaaf-5178-40a8-afe0-2150a6846f45`
- deployment source: `a642a1f907b20dd3da6d8219430b9b12dd3d3301`
- deployment status: **SUCCESS**
- deployment log: application startup completed and `/healthz` returned HTTP `200`
- owner-facing routes retain HTTP Basic authentication
- runtime model credential remains supplied through Railway references; no API secret is committed

## Verification boundary

Technical green status proves the replacement is executable and preserves the tested constraints. It does **not** prove owner-facing information gain.

Direct outcome evidence under the replacement strategy is therefore **NOT YET MEASURED** until the owner uses the deployed conversation. The next decision-changing evidence is the owner judgment: does the interviewer produce at least one useful distinction, contrast, boundary/counterexample, or cross-situation synthesis that was not merely handed to it verbatim?

If the answer is still essentially paraphrase plus confirmation, classify this replacement strategy as failed rather than polishing the UI.

## Authorization boundary

Authorized: this bounded authenticated owner-only conversational probe and owner-initiated runtime model use.

Still closed: external participant collection, automated participant coding, target-model activity, broader public participant deployment, recruitment/contact, merge/release, production auth/recovery/voice expansion, and unapproved spending.

**There was never a completion policy.**
