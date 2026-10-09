# Survey owner recovery, researcher login and model-inspection result

## Owner-requested outcomes

1. Researcher dashboard: the empty-looking `/admin` was actually a bearer-key 401. The private UI now asks for a researcher key, avoids showing zero counts while unauthenticated, and has explicit Unlock/Lock. The owner-local launcher is installed in Downloads and registered in the desktop app menu; it obtains the private admin key at launch from the owner's Railway CLI and offers to paste from the desktop clipboard (desktop-level GUI behavior must be assessed on actual user's desktop). The admin key is not in Git or committed artifacts. Authorization still required.
2. Autonomous feedback triage: a daily 08:00 local-time ChatGPT condition-watch automation was successfully created in the current conversation. It instructs the future assistant to review new consented feedback, commit safe prospective versioned repairs without retroactively changing frozen/in-flight question definitions, and send an anonymized email to the owner's requested address through connected Gmail only for genuine owner decisions. The task has no observed run or sent email yet; it is a scheduled action, not an always-on server daemon. Existing private researcher inbox remains live from the previous task.
3. Inspectability: generated `question-atlas.html` and `question-atlas.json`, covering 79 pinned historical v7, 25 active TF1 v1 and 25 not-live v2 drafts, with 73 historical evidence-guide facet examples, explicit inference limits and source/version status. Delivered to owner OS Downloads. A separate owner-private 84-turn exact answers/accepted interpretations HTML is delivered locally only; not stored or committed to Git. Six admitted reviewer findings are tied to eleven question/answer sources; 84 turns are not 84 independent trait observations.
4. Model mapping: `OLD-VS-CURRENT-SURVEY-MAPPING-REPORT.md` separates known-target six-rule historical fit from failed frozen V4.3 survey crosswalk and V1.5 five-domain pilot. Current source shares 78/79 exact old Q/A pairs; its six nonmatching entries provide no wholly new independent reviewer finding. The current source does not establish a new blind DOB/time recovery; do not claim it does.
5. Final submission: recovered exact 82-turn base from the owner's authorized ChatGPT Library, combined its untouched exact text with two frozen appended turns in a separately versioned private 84-turn file. A separately versioned CF-003 copy retains the exact three responses and relinks only canonical primary hash, preserving the original secondary. The previous original files are unchanged. Read-only Railway snapshot identified one matching ready independent review; a single source-derived clarification-process feedback annotation is explicitly preserved while behavioral text must still match. An isolated exact-real-record local TestClient returned 200 encrypted-storage receipt and passed exact retry/idempotency; **this is not yet production storage**.

## Backend fix

`GptReviewedSubmission` can omit the opaque review ID, and Railway recovers it only when the exact complete frozen primary matches exactly one saved ready review. No guessing by name, DOB, personality, partial record or numerical turn count; zero or multiple matches fail closed. The old explicit-review-ID route remains compatible. Missing `turns` composites are rejected; the GPT handoff now documents how to materialize from an authenticated, exact Library base instead of inventing missing turns. Extra valid process annotations are allowed only for clarification turns, not earlier reviewed interview turns; all behavioral Q/A remain strict.

## Verification

- Participant app suite: 220 passed, 1 Starlette/httpx deprecation warning.
- Repository suite: 1,021 passed, six astronomy-data skips and the same warning.
- Action/schema, missing-handle, ambiguous review, process-note and unauthorized dashboard regression tests passed.
- Scoped changed-file Ruff check passed with project legacy exclusions E501/UP035/SIM105. Admin JS Node syntax check passed.
- Instructions strict count <= 8,000 and cumulative GPT package checked.

## Current remaining boundaries

Merge and deploy exact tested backend/admin UI to Railway, verify 200/401 production and source match. Then submit the separately materialized REAL human record through production using previously recorded genuine research/final-submission consent; verify live receipt and idempotency and preserve all receipts privately. Deliver cumulative Custom GPT update in Downloads; private GPT editor still requires owner. No completed live submitted data claim until proof.
