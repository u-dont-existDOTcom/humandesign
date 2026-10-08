# Questionnaire feedback and wording revision — implementation result

## Answer to owner

Before this task, the user-experienced feedback loop was incomplete. The collector/reviewer could preserve process feedback, and the 2026-10-07 pilot generated a public-safe quality audit and stronger question-admission rules, but the researcher admin had no dedicated question objection inbox. Also, the specific latest audit did not change active question text: original v7 was frozen, and the prospective TF1 replacements already predated the latest audit. The earlier answer over-described rule/presentation changes as if they themselves fixed the questions.

## Implemented return path

A researcher-authenticated `/api/admin/question-feedback` endpoint reads explicit instrument objections from already consented, encrypted Railway reviews (even while queued), their clarification histories, final submissions and consented direct Railway sessions. No additional participant Action is needed. The private `/admin` page now lists exact associated question wording, best-known route ID, issue hint, and the reported objection, with a private JSON export for researcher triage. Each item can also be marked New, Investigating, Revision proposed (with version identifier), Resolved or Dismissed; this disposition is persisted separately without changing the participant's interview or review. Unknown routes are labeled unmapped rather than guessed. An intentionally narrow detector catches clear objections that appear directly in answers; generic 'it depends' responses are not complaints. Researcher triage hints are not definitive verdicts. Withdrawn source reviews and synthetic canaries do not appear. The endpoint is admin-token protected and is not in the public GPT Action schema.

The GPT handoff instructions require preserving verbatim question objections as `process_feedback` in the corresponding turn, separate from any behavioral answer. They are sent only with the participant's existing consented review submission. A participant who abandons the interview before consenting/transmitting a review has no automatic server-side feedback report. The inbox is visible when the researcher opens or refreshes the private admin; there is not yet a push/email alert or automatic GitHub issue. New comments never silently revise an instrument.

## Actual question-text changes

Nine TF1 question wordings have been rewritten in `tendency-first-v2-development.json` and individually compared with their v1 wording in `QUESTION-REVISION-CROSSWALK.md`. The proposal also retires three weak legacy options (ROMANCE-FADE, ROOM-EFFECT, CORRECTION-REASON). The v2 draft has deliberately **not** been activated: existing v1 review-state identities and frozen v7 wording remain unchanged. Prospective promotion requires a version-pinned new cohort/cognitive trial, not re-evaluation of the owner's already seen responses as if untouched validation.

## What counts as done vs not done

- Backend inbox, status tracking and private admin UI: implemented, merged and deployed; production authenticated readback returned 9 existing feedback items. See LIVE-DEPLOYMENT-RECEIPT.json.
- Exact complaint capture on new GPT conversations: requires applying the cumulative private GPT update; the server cannot force a GPT to follow textual instructions before that editor update.
- Nine versioned wording revisions: actual files exist, tested structurally, but not live. Do not claim participant use or predictive validity.
- Automatic feedback-to-question-change: intentionally not implemented; changes require research review, versioning and validation.

## Assurance

Focused tests cover authorization, consent, queued review (not only successful final submissions), mixed complaint/behavior distinction, untagged explicit objection detection, synthetic exclusions, withdrawal behavior, UI safely escaped rendering and v2 frozen-v1 preservation. Broader suite and deployment outcome are tracked in RELEASE-GATE-STATUS.json.

## Live closeout

The Railway deployment succeeded with exact tested merged source. Both public health and researcher admin UI returned 200; unauthorized feedback endpoint returned 401; authorized feedback returned 200 with 9 entries. Remaining user work: private GPT editor application. New v2 wording is not active. See CLOSEOUT.md and deployment/delivery receipts.
