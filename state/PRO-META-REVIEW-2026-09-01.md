# Verified Pro meta-review — 2026-09-01

Status: `PRO_META_REVIEW_ADMITTED_REVISE`

Scope key: `supervision-architecture/a40d413-authority-provenance-v1`

Packet ID: `PRO-META-A40D413-AUTHORITY-PROVENANCE-20260901-v1`

This is an externally observed UI receipt, not a cryptographic platform attestation.
The response initially required an external completed-response receipt; the matching
same-session receipt below supplies it, so the admitted state is
`PRO_META_REVIEW_ADMITTED_REVISE`.

## Independent receipt

```json
{
  "schemaVersion": 1,
  "assuranceClass": "OBSERVED_UI_RECEIPT",
  "surface": "signed-in ChatGPT Chat via Brave connected extension",
  "accountUi": "u-dont-exist.com Pro",
  "accountReceiptVisible": true,
  "chatSurfaceSelected": true,
  "visibleModePreSubmission": "Pro",
  "visibleModePreSubmissionReceipt": true,
  "conversationUrl": "https://chatgpt.com/c/6a974b8a-31dc-83ea-90b5-f653b825a631",
  "conversationSessionId": "6a974b8a-31dc-83ea-90b5-f653b825a631",
  "inputPayloadSha256": "fb677f21e4dbc31bf1e9b205b5f6858d15a6a8b58b2c20ef2adcd6dd15d2a462",
  "submittedVisiblePayloadSha256": "0b06b1b79b4a88863eb2ceec559905555800bab4f73f53314a6bc90630b1a93a",
  "submittedVisiblePayloadLength": 51980,
  "submittedMessageReceipt": {
    "userTurnCount": 1,
    "markers": {
      "packet1": true,
      "packet2": true,
      "xhDirective": true,
      "browserIncident": true,
      "modeMismatchIncident": true,
      "admission": true
    }
  },
  "completedResponseSha256": "bc2ee36999016e2e1ab5d5768a8b492a95857bf8742c9f46be6e92fed0e1ebb1",
  "completedResponseLength": 33805,
  "completedResponseReceipt": {
    "assistantTurnCount": 1,
    "stopButtonAbsent": true
  },
  "visibleModePostResponse": "Pro",
  "visibleModePostResponseReceipt": true,
  "aggregateState": "VERIFIED_COMPLETE",
  "platformCryptographicAttestation": null
}
```

## Complete response

scopeKey: supervision-architecture/a40d413-authority-provenance-v1
packetId: PRO-META-A40D413-AUTHORITY-PROVENANCE-20260901-v1
verdict: REVISE
reviewContentState: COMPLETE
reviewAdmissionState: PENDING_EXTERNAL_COMPLETED_RESPONSE_RECEIPT
authoritativeStateAfterValidReceipt: PRO_META_REVIEW_ADMITTED_REVISE

The three core controls in the Extra High design are accepted in principle: explicit authority requirements, subject-bound provenance with bounded reproduction, and session-bound reasoning-surface receipts. The design must not be adopted unchanged because authority is not a single ordered “ceiling,” claimTransition cannot safely be a mutable field, and a browser-observed receipt must not be named or treated as cryptographic platform attestation.

An independent GitHub read confirms that Human Design PR #23 remains open, draft, unmerged, and currently bound to 4ccd140b33f8473fa79e91ff6161caaaaa69323e; Mission Control PR #52 remains open, draft, unmerged, and bound to 6ec73802cf9439be7160f9ac2eea58c7bb95e683. The 4ccd140b… commit is a routing/evidence checkpoint whose parent is the Extra High-bound 7156fd61…, so the Human Design directive may be re-bound rather than discarded, but exact-head preflight remains mandatory.

The appropriate architecture choice remains ADAPT + COMPOSE. In-toto’s statement model binds assertions to immutable subjects by digest; SLSA distinguishes tenant-controlled inputs from provenance generated or verified inside a trusted control plane; RATS separates evidence, verifier appraisal, and the relying party’s authorization policy while requiring freshness and replay protection; NIST federation similarly requires a relying party to verify an assertion from the expected identity provider rather than trust a subject’s self-description. These are supporting patterns, not a claim that Mission Control currently conforms to any of those standards. 
NIST Pages
+6
GitHub
+6
SLSA
+6

1. Required Mission Control architecture revision
1.1 Replace scalar authority with scoped, conjunctive authorization

Do not implement authority as an ordered comparison such as:

currentAuthority >= requiredAuthority

There is no generally valid ordering in which a reasoning decision automatically outranks an owner decision, or an artifact fact automatically satisfies a policy requirement. One claim can require several different things simultaneously: verified artifact evidence to establish a fact, owner authority to promote it into policy, and a verified reasoning receipt to issue a supervisory verdict about it.

Use this normative claim record:

JSON
{
  "schemaVersion": 3,
  "claimId": "string",
  "claimVersion": 1,
  "claimDigest": {
    "algorithm": "sha256",
    "canonicalization": "RFC8785_JCS",
    "digestScope": "CLAIM_SEMANTICS",
    "value": "64-lowercase-hex",
    "byteLength": 0
  },
  "claimText": "exact claim text",
  "claimValue": null,
  "claimKind": "FACT",
  "useSiteRefs": [],
  "loadBearingEvaluation": {
    "rulesetVersion": "string",
    "result": true,
    "reasons": []
  },
  "subjectRef": {
    "subjectType": "GIT_COMMIT",
    "repository": "owner/repository",
    "ref": "commit-or-version",
    "version": null,
    "digest": {
      "sha256": null
    }
  },
  "currentAuthorities": [
    {
      "authorityClass": "ARTIFACT_DERIVED_FACT",
      "authoritySourceRef": "string",
      "authorityScope": [
        "ASSERT_FACT"
      ],
      "status": "CURRENT"
    }
  ],
  "requiredAuthorizations": [
    {
      "operation": "PROMOTE_TO_POLICY",
      "requiredIssuerClass": "OWNER_EXPLICIT",
      "scopeRef": "string",
      "authorizationSourceRef": null,
      "status": "MISSING"
    }
  ],
  "evidenceRefs": [],
  "derivation": null,
  "reproductionRequirement": "REQUIRED",
  "reproductionReceiptRefs": [],
  "verificationState": "VERIFIED_FACT_ONLY",
  "decisionUse": "DESCRIPTIVE_ONLY",
  "createdAt": "RFC3339 timestamp",
  "expiresAt": null,
  "supersedesClaimRef": null
}

Required claimKind enum:

FACT
IMPLEMENTATION_DETAIL
SCIENTIFIC_CRITERION
PRODUCT_DECISION
RELEASE_CONDITION
OWNER_ACCEPTANCE_CRITERION
SUPERVISORY_VERDICT
IDENTITY_ASSERTION

Required authorityClass enum:

OWNER_EXPLICIT
OWNER_CORRECTION
REASONING_DECISION
ARTIFACT_DERIVED_FACT
OBSERVED_PLATFORM_STATE
EXECUTOR_PROPOSAL

Required authorization operations:

ASSERT_FACT
PROMOTE_TO_POLICY
AUTHOR_SUPERVISORY_VERDICT
AUTHORIZE_EXECUTION
AUTHORIZE_RELEASE

Required authorization states:

SATISFIED
MISSING
MISMATCH
STALE
REVOKED

Required verificationState enum:

UNVERIFIED
VERIFIED_FACT_ONLY
AUTHORIZED_POLICY
ADVISORY_ONLY
MISMATCH
STALE
REVOKED
REJECTED

Required decisionUse enum:

DESCRIPTIVE_ONLY
ADVISORY_ONLY
POLICY_ELIGIBLE
EXECUTION_ELIGIBLE
FORBIDDEN

For the Human Design completeness question:

claimKind = SCIENTIFIC_CRITERION or OWNER_ACCEPTANCE_CRITERION
operation = PROMOTE_TO_POLICY
requiredIssuerClass = OWNER_EXPLICIT
authorizationSourceRef = null
status = MISSING
decisionUse = FORBIDDEN

That applies equally to 23, 76, or any third denominator.

1.2 Make claim transitions immutable and append-only

Do not add one mutable claimTransition field to the claim row. Use a separate append-only transition ledger:

JSON
{
  "schemaVersion": 1,
  "transitionId": "string",
  "claimId": "string",
  "fromClaimRef": {
    "claimId": "string",
    "claimVersion": 1,
    "claimDigest": "64-lowercase-hex"
  },
  "toClaimRef": {
    "claimId": "string",
    "claimVersion": 2,
    "claimDigest": "64-lowercase-hex"
  },
  "transitionType": "PROMOTED",
  "requestedByRef": "string",
  "requiredAuthorizationRefs": [],
  "authoritySourceRefs": [],
  "evidenceRefs": [],
  "reason": "string",
  "recordedAt": "RFC3339 timestamp",
  "previousTransitionDigest": null,
  "transitionDigest": "64-lowercase-hex",
  "status": "APPLIED"
}

Required transition types:

DERIVED
PROMOTED
REVOKED
SUPERSEDED

Required transition statuses:

APPLIED
REJECTED

A PROMOTED transition must:

Create a new claim version.

Identify a new authority source that authorizes the target policy use.

Satisfy every entry in requiredAuthorizations.

Preserve the artifact-derived fact as a separate descriptive claim.

Fail with UNAUTHORIZED_CLAIM_PROMOTION if the value was merely copied, renamed, placed in a contract, or repeated by a reviewer.

1.3 Bind independent reproduction to the exact subject

Use this reproduction receipt:

JSON
{
  "schemaVersion": 1,
  "reproductionReceiptId": "string",
  "claimRef": {
    "claimId": "string",
    "claimVersion": 1,
    "claimDigest": "64-lowercase-hex"
  },
  "subjectRef": {
    "subjectType": "GIT_COMMIT",
    "repository": "owner/repository",
    "ref": "exact-commit",
    "digest": {
      "sha256": null
    }
  },
  "producerEvidenceRef": "string",
  "reproducer": {
    "identityRef": "string",
    "type": "HUMAN_OR_INDEPENDENT_PROCESS",
    "trustDomain": "string"
  },
  "independenceBasis": "string",
  "methodRef": "string",
  "methodDigest": "64-lowercase-hex",
  "commandOrProcedure": "string",
  "resultValue": null,
  "resultDigest": "64-lowercase-hex",
  "matchState": "MATCH",
  "synthetic": false,
  "reproducedAt": "RFC3339 timestamp",
  "freshnessState": "CURRENT",
  "promotesAuthority": false
}

Required matchState values:

MATCH
MISMATCH
INCONCLUSIVE

Independent reproduction proves only the artifact fact. promotesAuthority must always be false; a separate authorized promotion record is required.

1.4 Rename reasoning “attestation” to an observation receipt

The required template name is:

templates/REASONING-SURFACE-OBSERVATION-RECEIPT.json

Do not use REASONING-SURFACE-ATTESTATION.json for current browser/UI evidence.

Required schema:

JSON
{
  "schemaVersion": 1,
  "receiptId": "string",
  "transactionId": "string",
  "reviewRequirementId": "string",
  "scopeKey": "string",
  "packetId": "string",
  "requiredReviewerRole": "PRO",
  "requirementSourceRef": "string",
  "subjectBinding": {
    "sourcePacketDigest": {
      "algorithm": "sha256",
      "value": "64-lowercase-hex",
      "byteLength": 0,
      "bytesDefinition": "exact UTF-8 bytes"
    },
    "inputPayloadDigest": {
      "algorithm": "sha256",
      "value": "64-lowercase-hex",
      "byteLength": 0,
      "bytesDefinition": "exact UTF-8 source-packet bytes"
    },
    "submittedVisiblePayloadDigest": {
      "algorithm": "sha256",
      "value": "64-lowercase-hex",
      "byteLength": 0,
      "bytesDefinition": "exact UTF-8 composer text submitted to the conversation"
    },
    "submissionTransform": {
      "type": "NONE",
      "description": null,
      "transformDigest": null
    },
    "admissionQuestionDigest": {
      "algorithm": "sha256",
      "value": "64-lowercase-hex",
      "byteLength": 0,
      "bytesDefinition": "exact UTF-8 admission-question bytes"
    },
    "boundRepositoryHeads": []
  },
  "conversation": {
    "surfaceOrigin": "https://chatgpt.com",
    "conversationSessionId": "string"
  },
  "observations": {
    "surface": {
      "requiredValue": "SIGNED_IN_CHATGPT_CHAT",
      "observedValue": null,
      "status": "MISSING",
      "evidenceRef": null,
      "observedAt": null
    },
    "account": {
      "requiredValue": "u-dont-exist.com Pro",
      "observedValue": null,
      "status": "MISSING",
      "evidenceRef": null,
      "observedAt": null
    },
    "visibleModePreSubmission": {
      "requiredValue": "Pro",
      "observedValue": null,
      "status": "MISSING",
      "evidenceRef": null,
      "observedAt": null
    },
    "conversationSession": {
      "requiredValue": "SAME_TRANSACTION_SESSION",
      "observedValue": null,
      "status": "MISSING",
      "evidenceRef": null,
      "observedAt": null
    },
    "submittedMessage": {
      "requiredValue": "EXACT_BOUND_PAYLOAD",
      "observedValue": null,
      "status": "MISSING",
      "evidenceRef": null,
      "observedAt": null
    },
    "completedResponse": {
      "requiredValue": "ONE_COMPLETE_ASSISTANT_RESPONSE",
      "observedValue": null,
      "status": "MISSING",
      "evidenceRef": null,
      "observedAt": null
    },
    "visibleModePostResponse": {
      "requiredValue": "Pro",
      "observedValue": null,
      "status": "MISSING",
      "evidenceRef": null,
      "observedAt": null
    }
  },
  "responsePayloadDigest": {
    "algorithm": "sha256",
    "value": null,
    "byteLength": null,
    "bytesDefinition": "exact UTF-8 completed assistant-response bytes"
  },
  "observer": {
    "observerId": "string",
    "observerType": "ROUTING_EXECUTOR",
    "trustDomain": "string",
    "relationToReviewedWorker": "string"
  },
  "evidenceSourceType": "BROWSER_UI_OBSERVATION",
  "assuranceClass": "OBSERVED_UI_RECEIPT",
  "cryptographicPlatformAttestation": false,
  "observedAt": "RFC3339 timestamp",
  "freshnessPolicyRef": "string",
  "aggregateState": "PARTIAL",
  "mismatchReasons": [],
  "supersedesReceiptRef": null,
  "incidentRefs": [],
  "replayProtection": {
    "singleUse": true,
    "admissionNonce": "string",
    "usedByVerdictRef": null
  }
}

Per-observation status enum:

VERIFIED
MISSING
MISMATCH
UNVERIFIED
STALE

Aggregate state enum:

VERIFIED_COMPLETE
PARTIAL
MISMATCH
UNVERIFIED
STALE
REPLAY_REJECTED

Exact mode equality is required. An account on a Pro plan does not establish that the visible reasoning control was Pro. A visible Extra High control does not satisfy Pro, regardless of the input packet, response quality, model self-description, or account plan.

Where inputPayloadDigest and submittedVisiblePayloadDigest differ, submissionTransform.type must not be NONE. The transformation must be described and reproducible. An unexplained difference fails with REASONING_RECEIPT_PAYLOAD_MISMATCH.

1.5 Bind the verdict content to the observation receipt

A valid surface receipt must not be reusable with a different response. Add:

JSON
{
  "schemaVersion": 1,
  "verdictId": "string",
  "scopeKey": "supervision-architecture/a40d413-authority-provenance-v1",
  "packetId": "PRO-META-A40D413-AUTHORITY-PROVENANCE-20260901-v1",
  "verdict": "REVISE",
  "reviewRole": "PRO",
  "responsePayloadDigest": {
    "algorithm": "sha256",
    "value": "64-lowercase-hex",
    "byteLength": 0,
    "bytesDefinition": "exact UTF-8 completed assistant-response bytes"
  },
  "reasoningSurfaceReceiptRef": "string",
  "boundSubjectRefs": [],
  "admissionState": "PENDING_RECEIPT",
  "authoritative": false,
  "authorizedScope": [
    "SUPERVISION_DESIGN_META_REVIEW"
  ],
  "prohibitedConsequences": [
    "MERGE",
    "DEPLOY",
    "INVITATION_ROTATION",
    "OWNER_SESSION_REPLACEMENT",
    "PARTICIPANT_CONTACT",
    "SPENDING",
    "COMPLETENESS_DENOMINATOR_SELECTION"
  ],
  "issuedAt": "RFC3339 timestamp",
  "admittedAt": null
}

Required admissionState values:

PENDING_RECEIPT
ADMITTED
REJECTED_MISMATCH
REJECTED_REPLAY
REJECTED_RESPONSE_BINDING
STALE

Only ADMITTED permits authoritative: true.

2. Required fail-closed controls

Mission Control must implement these controls as executable admission rules, not prose-only conventions.

Control	Required behavior
AP-01-NO-AUTHORITY-ORDINAL	Reject any schema or evaluator that treats authority classes as a universal numeric hierarchy.
AP-02-CONJUNCTIVE-AUTHORIZATION	Every required authorization for the requested operation must be SATISFIED; one stronger-looking but differently scoped source cannot substitute.
AP-03-APPEND-ONLY-PROMOTION	Policy promotion requires an immutable PROMOTED transition and a new qualifying authority source.
AP-04-SUBJECT-BOUND	A changed commit, directive version, packet digest, session, or source digest marks dependent claims STALE.
AP-05-REPRODUCTION-IS-NOT-AUTHORITY	Reproduction may establish a fact but must never authorize policy use.
AP-06-LOAD-BEARING-AUTO-DETECTION	A claim referenced by acceptance, release, owner-facing definitive rendering, execution authorization, or a supervisory verdict is load-bearing regardless of a worker-set boolean.
AP-07-DEFINITIVE-RENDERING-GATE	Unregistered, stale, advisory-only, or descriptively limited claims cannot be rendered as settled owner-facing conclusions.
AP-08-IMMUTABLE-OWNER-SOURCES	Corrections append a new source/transition; existing exact owner-source blocks are never rewritten.
RS-01-SELF-ASSERTION-ZERO-WEIGHT	Agent names, paths, branch names, prompts, role labels, environment variables, and model self-description cannot satisfy any surface observation.
RS-02-EXACT-MODE	Required and observed visible reasoning mode must match exactly.
RS-03-SAME-SESSION	Surface, account, mode, submission, response, and post-response observations must bind to one transaction and conversation session.
RS-04-SINGLE-USE	A receipt may admit only one response/verdict and cannot be replayed even when the same packet is resubmitted.
RS-05-PAYLOAD-BINDING	Input, submitted-visible, admission-question, and response byte identities must be explicit; unexplained transformations fail.
RS-06-VERDICT-BINDING	The response digest in the verdict record must equal the digest in the completed-response observation.
RS-07-ASSURANCE-HONESTY	Current browser evidence must be labeled OBSERVED_UI_RECEIPT; setting cryptographicPlatformAttestation: true fails.
RS-08-SUPERSESSION-WITHOUT-ERASURE	A corrected receipt creates a new uniquely identified transaction and references the earlier mismatch; it does not overwrite the incident.

Required failure codes:

UNAUTHORIZED_ADDITION
INFERRED_NUMERIC_SCOPE
DERIVATION_UNVERIFIED
DIRECTIVE_SCOPE_EXCEEDED
UNAUTHORIZED_CLAIM_PROMOTION
AUTHORIZATION_REQUIREMENT_UNSATISFIED
SUBJECT_BINDING_STALE
PRODUCTION_REPRODUCTION_MISSING
DEFINITIVE_RENDERING_REJECTED
SELF_ASSERTED_REASONING_IDENTITY_REJECTED
REASONING_SURFACE_MODE_MISMATCH
REASONING_RECEIPT_SESSION_MISMATCH
REASONING_RECEIPT_REPLAY_REJECTED
REASONING_RECEIPT_PAYLOAD_MISMATCH
REASONING_RECEIPT_INCOMPLETE
VERDICT_RECEIPT_BINDING_MISMATCH
ASSURANCE_CLASS_OVERCLAIM
3. Required Mission Control tests

These tests are mandatory additions, in addition to retaining the existing passing tests:

test_required_authorizations_are_conjunctive_not_ranked
test_reasoning_decision_does_not_satisfy_owner_explicit
test_owner_explicit_can_authorize_owner_acceptance_criterion
test_artifact_23_remains_descriptive_only
test_artifact_76_remains_descriptive_only
test_fact_to_policy_copy_requires_promotion_transition
test_field_rename_cannot_bypass_fact_to_policy_transition
test_promotion_requires_new_authority_source
test_reproduction_verifies_fact_but_never_promotes_policy
test_synthetic_fixture_cannot_satisfy_production_reproduction
test_subject_commit_change_marks_claim_stale
test_directive_version_change_marks_claim_stale
test_revoked_or_superseded_source_invalidates_decision_use
test_unregistered_load_bearing_owner_rendering_is_rejected
test_claim_transition_digest_chain_detects_mutation
test_owner_source_correction_is_append_only
test_load_bearing_use_site_overrides_worker_false_flag

test_agent_name_extra_high_has_zero_receipt_weight
test_model_self_description_has_zero_receipt_weight
test_prompt_requested_mode_has_zero_receipt_weight
test_pro_plan_account_does_not_prove_pro_mode
test_pro_requirement_rejects_extra_high_observed_mode
test_valid_pre_mode_without_completed_response_is_partial
test_missing_post_response_mode_is_partial
test_post_response_mode_mismatch_rejects_review
test_surface_account_session_submission_and_response_are_independent
test_session_mismatch_rejects_transplanted_receipt
test_prior_receipt_replay_rejected_for_same_payload
test_receipt_replay_rejected_for_different_payload
test_unexplained_input_to_submitted_digest_change_is_rejected
test_response_digest_mismatch_rejects_verdict_admission
test_valid_ui_receipt_cannot_claim_platform_attestation
test_mismatch_incident_can_never_be_authoritative
test_corrected_transaction_preserves_prior_mismatch_incident
test_valid_receipt_cannot_be_paired_with_another_response

Run and record:

focused authority/provenance tests
full relevant compliance suite
all JSON and JSON-Schema validation
template instantiation validation
hostile-fixture evaluation
git diff --check

Passing fixtures remain bounded regression evidence. They do not prove universal architecture adequacy.

4. Browser-control incident disposition

incidentId: MC-BROWSER-REPO-TAB-SPRAWL-20260901-001
candidateVerdict: REVISE
sameConsolidatedArchitectureKey: YES

It belongs under the same consolidated review key because browser use was part of reasoning-evidence acquisition, and safe cleanup depends on provenance: whether browser use was necessary, which transaction opened a tab, and whether the system has authority to close it. Its durable implementation should also be cross-indexed under the existing browser-hygiene/resource-routing pattern rather than folded into the claim-authority schema.

The proposed control has the right defaults but is incomplete. Add this separate receipt:

JSON
{
  "schemaVersion": 1,
  "browserOperationId": "string",
  "transactionId": "string",
  "taskId": "string",
  "packetId": "string",
  "purposeClass": "CHATGPT_REASONING_SURFACE_OBSERVATION",
  "browserNecessity": "REQUIRED",
  "necessaryCapability": "string",
  "nonBrowserAlternatives": [
    {
      "route": "GITHUB_CLI",
      "availability": "AVAILABLE",
      "satisfiesCapability": true,
      "evidenceRef": "string"
    }
  ],
  "selectedRoute": "BROWSER",
  "decisionRef": "string",
  "browserSessionRef": "string",
  "baselineTabs": [
    {
      "tabId": "string",
      "ownershipClass": "OWNER_EXISTING",
      "protected": true
    }
  ],
  "maxAgentTransientTabs": 1,
  "exceptionRef": null,
  "actions": [],
  "agentOpenedTabIds": [],
  "cleanup": {
    "policy": "CLOSE_ONLY_AGENT_OPENED",
    "attempted": false,
    "results": [],
    "remainingAgentTabIds": []
  },
  "ownerTabsTouched": false,
  "verificationState": "VERIFIED",
  "failureCodes": [],
  "recordedAt": "RFC3339 timestamp"
}

Required enums:

purposeClass:
  CHATGPT_REASONING_SURFACE_OBSERVATION
  INTERACTIVE_AUTHENTICATED_UI
  REPOSITORY_RETRIEVAL
  OTHER

browserNecessity:
  REQUIRED
  NOT_REQUIRED
  UNKNOWN

ownershipClass:
  OWNER_EXISTING
  AGENT_OPENED
  UNKNOWN

action.type:
  OPEN
  REUSE
  NAVIGATE
  CLOSE
  OBSERVE_PRESENT
  OBSERVE_ABSENT
  OBSERVE_STALE

Required controls:

Repository reads default to authenticated CLI/local Git whenever that route satisfies the capability.

Browser navigation is blocked before execution when an available non-browser route satisfies the same capability.

At most one agent-opened transient tab is permitted unless exceptionRef identifies a recorded necessity.

Only tabs proven AGENT_OPENED in the same browser session and transaction may be closed.

UNKNOWN ownership fails closed: leave the tab untouched and report it.

Signed-in reasoning conversations and owner-existing tabs are protected.

Tab IDs from another browser session cannot be reused as ownership proof.

Cleanup failure is reported; it does not authorize closing adjacent or guessed tabs.

Opening, navigating, or closing an owner-session tab without necessity emits UNNECESSARY_OWNER_BROWSER_MUTATION.

Required browser failure codes:

BROWSER_ROUTE_NOT_JUSTIFIED
AGENT_TAB_CAP_EXCEEDED
TAB_OWNERSHIP_UNVERIFIED
TAB_SESSION_MISMATCH
PROTECTED_TAB_MUTATION_ATTEMPT
AGENT_TAB_CLEANUP_INCOMPLETE
UNNECESSARY_OWNER_BROWSER_MUTATION

Required browser tests:

test_repository_retrieval_uses_cli_when_available
test_browser_allowed_for_signed_in_reasoning_surface_observation
test_second_transient_tab_requires_recorded_exception
test_only_same_transaction_agent_tabs_may_be_closed
test_unknown_stale_tab_ownership_fails_closed
test_owner_existing_tabs_are_preserved
test_reasoning_conversation_tabs_are_protected
test_tab_id_from_another_browser_session_is_rejected
test_cleanup_failure_is_reported_without_guessing_other_tabs
test_baseline_and_cleanup_states_are_both_recorded
test_observed_tab_absence_does_not_attribute_closing_actor

For the incident record:

currentTabState = CLOSED_OR_STALE_AS_REPORTED
closedByActor = UNKNOWN
cleanupAttributionState = UNATTRIBUTED

No inference is authorized about which actor closed any stale handle.

5. Pro-mode mismatch incident disposition

incidentId: MC-PRO-MODE-RECEIPT-MISMATCH-20260901-001
incidentDisposition: ACCEPT
priorReviewAuthoritative: false
sameConsolidatedArchitectureKey: YES

The prior session 6a9748cc-3c10-83ea-83dc-d3e3f3d1edad is correctly classified as:

requiredVisibleMode = Pro
observedVisibleMode = Extra High
aggregateState = MISMATCH
failureCode = REASONING_SURFACE_MODE_MISMATCH
proMetaReviewAuthoritative = false

Its input and response hashes may be retained as incident evidence. Its response must not populate proMetaReview, satisfy the current Pro requirement, or be promoted merely because it reviewed the same packet.

The current transaction’s supplied correction reports a separately observed Pro button before submission. That is accepted only as a pre-submission observed UI claim. This response cannot independently record its own conversation URL, current session ID, completed-response digest, or post-response mode. Therefore the present admission state remains:

surface/account/pre-submit-mode = SUPPLIED_OBSERVED_EVIDENCE
conversation/session binding = PENDING_EXTERNAL_RECEIPT
completed response = PENDING_EXTERNAL_RECEIPT
post-response mode = PENDING_EXTERNAL_RECEIPT
aggregateState = PARTIAL

After this response, the routing executor must create a new receipt with a unique transactionId, reference the prior mismatch through incidentRefs or supersedesReceiptRef, and bind the exact completed response to the current session. It must not overwrite the mismatch record.

6. Next bounded Human Design execution directive
directiveId: PRO-HD-PR23-SERVER-BINDING-UNRESOLVED-COMPLETION-20260901
version: 1.0.0
repository: u-dont-existDOTcom/humandesign
pullRequest: 23
branch: codex/astrohd-owner-intake-quality-v1
boundHead: 4ccd140b33f8473fa79e91ff6161caaaaa69323e
boundParent: 7156fd61e0e75a56f66024c65357c1256bf8f4f9
preservedImplementationCheckpoint: 69c2d5796f871fae248f49acfd6778c336d9bf45
productionObserved: afc0bb82de0e481ae5a5d3453e0bcaf82b2a0286
completionDenominatorDecision: UNRESOLVED_OWNER_AUTHORITY
Authorized draft-branch work
HD-1 — Persist this Pro response only after external receipt admission

After the external same-session receipt passes, preserve:

scope key
packet ID
this complete response
response payload SHA-256 and exact byte definition
observation receipt
verdict admission record
prior Pro-mode mismatch incident reference
browser-control incident disposition

Do not write “Pro approved” before admissionState = ADMITTED.

Correct stale PR/state prose that says Extra High can bind the completeness criterion. Extra High and Pro may analyze or recommend it; in this task, promotion to a completeness rule requires OWNER_EXPLICIT.

HD-2 — Separate client evidence from server-resolved evidence

Remove cluster_id from:

reference/custom_gpt/participant_interviewer_action_openapi_v1.yaml
the client-facing EvidenceInput model
all interviewer instructions
all request examples and fixtures

Client request models must reject all of these:

cluster_id
resolved_cluster_id
frozen_cluster_id
frozen_dimension_ref

Do not silently discard them.

Create a server-internal binding equivalent to:

JSON
{
  "questionId": "string",
  "resolvedClusterId": "string",
  "freezeRef": {
    "sessionId": "string",
    "freezeSha256": "64-lowercase-hex"
  },
  "dimensionIndex": 0,
  "resolvedAt": "RFC3339 timestamp"
}

The exact internal field names may follow repository conventions, but this structure must not be client-authored.

HD-3 — Resolve the frozen binding server-side

For natal-ranking-eligible evidence:

If question_id is absent, preserve the narrative as unbound and non-scoreable.

If question_id is supplied, load the session’s immutable PredictionFreeze.

Find dimensions whose question_id exactly matches.

Zero matches: fail FROZEN_QUESTION_BINDING_MISSING.

More than one match: fail FROZEN_QUESTION_BINDING_AMBIGUOUS.

Exactly one match: use its server-owned cluster_id.

Persist the internal binding with the freeze identity.

scoring_response() must consume only the server-resolved binding.

An adequately assessed observation with answer: null may still have a valid server binding and count as assessed evidence; it must not be forced into a scoreable answer.

Do not expose the cluster or hidden prediction merely so the client can echo it.

HD-4 — Replace the implicit mapped-ID policy

Rename the current descriptive backend concept:

required_confirmatory_question_ids

to a non-authoritative artifact name such as:

mapped_scoreable_question_ids

Do not create completion_required_question_ids from that set.

Add a server-owned completion-policy snapshot:

JSON
{
  "schemaVersion": "participant-completion-policy-v1",
  "status": "UNRESOLVED_OWNER_AUTHORITY",
  "policyId": null,
  "authoritySourceRef": null,
  "requiredQuestionIds": null,
  "policyDigest": null
}

Required status enum:

UNRESOLVED_OWNER_AUTHORITY
AUTHORIZED
REVOKED
STALE

For the current task, only UNRESOLVED_OWNER_AUTHORITY is authorized.

HD-5 — Correct the progress contract

Expose descriptive facts without calling them required:

mapped_scoreable_question_count
adequately_assessed_mapped_question_count
completion_policy_status
completion_policy_id
completion_required_question_count
completion_coverage
completion_authority_source_ref

While unresolved:

completion_policy_status = UNRESOLVED_OWNER_AUTHORITY
completion_policy_id = null
completion_required_question_count = null
completion_coverage = null
completion_authority_source_ref = null

Remove or rename owner-facing fields that currently imply policy:

required_confirmatory_question_count
adequately_assessed_coverage
unresolved_question_count

scoreable_coverage may remain only if renamed and documented as descriptive mapped-artifact coverage, not completion.

No owner-facing 100% complete, all required questions, or equivalent statement may be generated.

HD-6 — Fail lock and reveal closed

Remove the require_complete_profile boolean as a policy selector for the repaired protocol. A route-level boolean must not manufacture the missing completion policy.

Before a new conforming confirmatory lock:

load server-owned CompletionPolicySnapshot
require status = AUTHORIZED
require non-null policyId
require non-null authoritySourceRef
require policy digest and source identity to match the session protocol

Until then:

lock failure = SCIENTIFIC_COMPLETENESS_POLICY_UNRESOLVED
new conforming reveal = unavailable

Reveal must require a valid lock bound to an authorized completion-policy digest. It must not infer policy from mapped dimensions.

HD-7 — Preserve the pre-repair session

The existing owner session and evidence must remain:

readable
unaltered
diagnostic
bound to their original protocol/source version
not migrated into a new prospective session
not relabeled as conforming to the repaired protocol

An already-created historical diagnostic result may remain readable through an explicitly diagnostic path. Do not create a new conforming lock or reveal from it while authority is unresolved.

No deletion, answer copying, source-version rewriting, invitation rotation, or replacement session is authorized.

Required Human Design tests
test_action_openapi_has_no_cluster_id
test_client_model_rejects_cluster_id
test_client_model_rejects_resolved_cluster_aliases
test_unbound_narrative_remains_readable_and_nonscoreable
test_server_resolves_cluster_from_session_freeze
test_server_binding_records_exact_freeze_identity
test_missing_frozen_question_binding_fails_closed
test_ambiguous_frozen_question_binding_fails_closed
test_persisted_scoreable_evidence_uses_server_resolved_cluster
test_null_answer_can_be_adequately_assessed_without_becoming_scoreable
test_mapped_counts_are_descriptive_not_required
test_unresolved_policy_has_null_required_count_and_coverage
test_lock_fails_when_completion_policy_is_unresolved
test_reveal_cannot_bypass_unresolved_completion_policy
test_route_boolean_cannot_select_completion_policy
test_neither_23_nor_76_populates_required_question_ids
test_pr_and_state_prose_require_owner_explicit_authority
test_legacy_session_remains_readable_and_diagnostic
test_legacy_evidence_is_not_silently_migrated
test_source_or_protocol_mismatch_blocks_conforming_reuse
test_hidden_cluster_or_prediction_is_not_exposed_to_action

Run and record the exact commands and results for:

focused participant/session tests
focused natal-pilot API tests
full test suite
strict mypy
Ruff on every touched Python file
OpenAPI parse and schema validation
participant JavaScript syntax check if touched
git diff --check
7. Prohibited actions

This review does not authorize:

selection of 23
selection of 76
selection of another denominator
merge of PR #23
merge of PR #52
deployment
Railway mutation
invitation rotation
replacement owner session
migration of owner answers
participant contact
spending
question-bank scientific-content changes
frozen mapping or scoring changes made to force a completeness policy
claiming Human Design or astrology validity
claiming cryptographic platform attestation
closing tabs whose agent ownership is unverified
8. Stop conditions

Stop substantive execution and return to reasoning when any of these occurs:

the current Pro response cannot be bound to a unique current conversation/session
completed-response or post-response Pro-mode receipt is missing
the current receipt reports Extra High or another mode rather than Pro
the response digest does not match the verdict record
the receipt is a replay or belongs to the prior mismatch session
PR #23 is no longer at 4ccd140b33f8473fa79e91ff6161caaaaa69323e before mutation
PR #52 is no longer at 6ec73802cf9439be7160f9ac2eea58c7bb95e683 before its mutation
question_id does not resolve to exactly one frozen dimension
server-side binding would require altering scientific mappings
the client would have to receive hidden cluster or prediction information
implementation would require choosing any completeness denominator
an owner-facing field would imply completeness while policy authority is unresolved
preserving compatibility would require rewriting or migrating the existing owner session
tests expose a substantive scoring/protocol conflict rather than a mechanical defect
a browser tab would need to be closed without same-session agent-ownership evidence
any merge, deployment, session replacement, contact, or spending becomes necessary
9. Completion semantics

For this response:

reviewContentState = COMPLETE
reviewAdmissionState = PENDING_EXTERNAL_COMPLETED_RESPONSE_RECEIPT

After the routing executor captures a matching current-session receipt with:

signed-in Chat surface verified
account verified
visible Pro mode before submission verified
current conversation/session verified
submitted message digest verified
completed response digest verified
visible Pro mode after response verified
no mismatch or replay

the admitted state becomes:

PRO_META_REVIEW_ADMITTED_REVISE

For the subsequent bounded draft implementation, the strongest permitted completion claim is:

SUBTASK_COMPLETE_PARENT_OPEN

It requires:

the admitted Pro receipt and response are durably recorded
the required Mission Control revisions are implemented and tested on the draft branch
the authorized Human Design edits are implemented and tested on PR #23
no prohibited action occurred
23-versus-76 remains explicitly unresolved
the pre-repair owner session remains preserved and diagnostic
remaining owner-authority, release, and deployment blockers are stated

It must not be upgraded to:

READY_FOR_RELEASE
READY_FOR_MERGE
OWNER_OUTCOME_ACHIEVED
SCIENTIFICALLY_COMPLETE
PROTOCOL_VALIDATED
PLATFORM_ATTESTED

