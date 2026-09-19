# Scenario-first evidence audit and real-answer pilot

19 September 2026. Design-only iteration. Parent outcome OPEN.

The owner asked for the next step and authorized doing it. Selected action: a bounded audit of whether the fictional answers support their information labels, repair the affected wording/routing, then start a one-question-at-a-time owner pilot in Chat. No app implementation, paid inference, VM contact/wake, deployment, recruitment, or real-person chart scoring is authorized by this step.

## Executed results

The unchanged source study at commit `899726ba760e017de54ab5894743ad3a0ebd6848` was verified against its 34-entry manifest. The original labels reproduce 73 information identifiers for each of ten fictional people. Replacing every answer with an explicit non-answer while retaining the original labels still produces 73 each. Keeping the text but removing the labels produces zero. The replay trusts `supported_facets` and `source_kind`; it does not extract semantics from the answer. This is a demonstrated limit of the bookkeeping check, not proof that the original answers are false. The prior report already disclosed the same-author labeling boundary.

With correctly tagged unknown answers, the replay produces zero evidence but still asks all 55 questions. With explicit absence of a bodily response, it still asks R04 and M10 about that response. A study-only prerequisite guard was added and passed eight typed-state checks; it suppresses both inappropriate follow-ups in all ten explicit-absence fixtures. It does not classify natural language or change the deployed app.

Thirty cited information bundles were semantically reviewed across responsibility, decision clarity over time, and depth/interruption of focus. Eighteen support narrow reports; twelve support only part of the compound label. This is a targeted same-context review, not independent evaluation or a complete re-score. Other uncited answers may fill some gaps; no replacement whole-profile percentage is claimed.

The clean interviewer bank contains 55 available questions and neutral targets, with no fictional answers or support keys. Five question texts were repaired. Follow-ups require a reported antecedent and an unanswered distinction; absence, uncertainty, refusal, inapplicability and process confusion remain distinct. Old fictional answers do not validate the revised wording. No shorter survey duration is claimed.

## Use the pilot now

Read `PILOT.md` and deliver its opening question. Continue from the actual owner answer, not an invented one. No fixed question quota, compulsory recent-event retrieval, birth data, chart cues, routine approval of paraphrases, or forced synthesis. Keep actual owner answers and content-derived hashes outside Git. The pilot is a development observation of this Chat, not the sleeping app or independent AstroHD recovery.

## Complete evidence and reproduction

Run `python3 tasks/scenario-evidence-pilot-20260919/RESTORE-ADDENDUM.py` from a checkout. This verifies two 9,888-byte archive parts, the combined SHA-256, and every internal file hash, then restores ten flat files under `materialized/` without replacing different existing bytes. It does not execute extracted code or contact any service.

The full evidence includes REPORT.md, PILOT.md, interviewer-bank.json, CITATION-AUDIT.md, citation-audit.json, stress-results.json, audit_replay.py, build_artifacts.py, CURRENT-STATE.json and MANIFEST.json. The original source study remains intact in the parent task's archive. Its existing RESTORE-STUDY.py supplies the --source-dir input for the diagnostic. The owner-facing download contains both the readable addendum and source study.

Combined archive: 19,776 bytes; SHA-256 `19b174d4f84b6fcb86890b0d5dd9a19441ad8a6be7068a87c3820b6b10f4694f`.

## Completion boundary

The audit and revised pilot candidate are completed, not the product or chart-recovery objective. The next observation belongs to the owner: their first real answer. Do not simulate it, wake inference, or infer deployment permission. Current branch state is in CURRENT-STATE.json. This branch does not overwrite runtime truth on the development or subscription-bridge branches.
