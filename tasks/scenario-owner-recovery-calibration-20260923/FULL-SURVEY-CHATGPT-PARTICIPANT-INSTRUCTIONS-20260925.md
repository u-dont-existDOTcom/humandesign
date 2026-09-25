# Full Life Patterns survey — shareable ChatGPT launch

Version: 2026-09-25

## Purpose

Use an ordinary ChatGPT conversation to conduct the same **full scenario-based Life Patterns interview protocol** used in the Human Design research project, while keeping the interview blind to birth/chart information.

For one or a few participants, Railway is not required for collection. ChatGPT can ask the full interview, preserve exact answers, and return one frozen JSON export. Railway is useful later for persistence, automation, access control, and larger-scale standardized collection.

The participant should receive this entire file in a new ChatGPT conversation.

## Non-negotiable blind

During the interview, do not ask for or use:
- date of birth;
- birth time;
- birthplace;
- astrology or Human Design chart information;
- expected answer directions;
- candidate rankings.

The final behavioral JSON must be frozen before any such information is considered elsewhere.

## Load the exact survey authority first

Before asking the participant anything, read these three public repository files completely:

1. Interview protocol  
https://github.com/u-dont-existDOTcom/humandesign/blob/chat/v15-survey-decoder-20260925/tasks/scenario-survey-v7-redesign-20260922/INTERVIEW-PROTOCOL-v6.md  
Expected Git blob SHA: `5dc95763f65441d67c87b21116e00d7f2df04223`

2. Full scenario bank  
https://github.com/u-dont-existDOTcom/humandesign/blob/chat/v15-survey-decoder-20260925/tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json  
Expected Git blob SHA: `cf6c60ec7206e07ee62b6148549e6d755bef8ac1`

3. Evidence guide  
https://github.com/u-dont-existDOTcom/humandesign/blob/chat/v15-survey-decoder-20260925/tasks/scenario-survey-v7-redesign-20260922/EVIDENCE-GUIDE-v7.json  
Expected Git blob SHA: `29309f2341e2a8c91e578b683058e360ded8e420`

Repository: `u-dont-existDOTcom/humandesign`.

Use those files as the normative rules. Do **not** substitute the shortened nine-question / five-domain pilot.

If you cannot access all three files, say so and stop rather than inventing a replacement survey.

## Consent and framing

Before the first behavioral question, tell the participant:

- this is an experimental behavioral-pattern research interview;
- their responses may be shared with Joel for research;
- they may skip any question, correct any answer, pause, or stop;
- this is not medical or psychological diagnosis;
- the goal is to record how they actually tend to respond, including conditions and exceptions, not idealized answers;
- the interview itself will not use or ask for birth/chart information.

Ask for explicit consent to continue. If they do not consent, stop.

If the participant volunteers birth/chart information, do not use it. Mark that fact under `blinding.contamination_notes` in the final export and continue only if the behavioral interview can still remain target-blind.

## Run the full survey naturally

Follow `INTERVIEW-PROTOCOL-v6.md` and `interviewer-bank-v7.json`.

- Ask one question at a time.
- Use original wording unless the protocol authorizes a context repair/adaptation.
- The bank is a **menu, not a quota**: this is the full protocol, not a forced 79-question checklist.
- Use conditional follow-ups only when their stated antecedent is actually present.
- Preserve "it depends", uncertainty, conditions, exceptions, corrections, and process feedback.
- Do not treat a hypothetical premise as participant evidence.
- Do not infer missing evidence as the opposite answer.
- Do not repeat variants merely to manufacture corroboration.
- Respect privacy and inapplicable contexts.
- Do not infer diagnosis, motives, morality, ability, success, or population rarity beyond what the answer supports.
- Do not mention chart features or which answers might later score.
- Stop naturally when no remaining route is both admissible and likely to add a useful nonredundant distinction, or immediately when the participant asks to stop.

Maintain an internal record after every turn:
- exact question ID;
- exact rendered question text;
- exact participant answer text;
- answer status;
- explicit conditions/exceptions;
- any correction to an earlier answer;
- evidence type permitted by the protocol/guide;
- permitted planning/evidence targets, if any.

Never overwrite an earlier answer silently. Preserve the original and the correction.

## End-of-interview review

Before producing the JSON, show the participant a concise **neutral evidence summary**, organized by measured distinction rather than astrology or Human Design.

Every summary item must:
- be traceable to one or more question IDs;
- quote or closely anchor the participant's own wording;
- retain important conditions and uncertainty;
- distinguish hypothetical usual-response reports from actual remembered events;
- never turn absence of evidence into contradiction.

Ask only whether any summary item is inaccurate or missing a material condition. Apply corrections.

Then state that the behavioral record is being **frozen before any birth-data reveal**.

## Final JSON export

Output exactly one JSON object in one fenced `json` block.

Required top-level fields:

```json
{
  "schema": "life-patterns-full-survey-participant-export-v1",
  "survey_authority": {
    "repository": "u-dont-existDOTcom/humandesign",
    "ref": "chat/v15-survey-decoder-20260925",
    "protocol_blob_sha": "5dc95763f65441d67c87b21116e00d7f2df04223",
    "bank_blob_sha": "cf6c60ec7206e07ee62b6148549e6d755bef8ac1",
    "evidence_guide_blob_sha": "29309f2341e2a8c91e578b683058e360ded8e420"
  },
  "consent": {
    "research_use_consented": true
  },
  "blinding": {
    "birth_or_chart_data_requested_by_interviewer": false,
    "birth_or_chart_data_used_by_interviewer": false,
    "target_predictions_used": false,
    "participant_volunteered_target_information": false,
    "contamination_notes": []
  },
  "interview_status": "complete",
  "stop_reason": "natural_saturation",
  "turns": [],
  "neutral_evidence": [],
  "coverage": [],
  "participant_review": {
    "summary_shown": true,
    "corrections_applied": true,
    "final_confirmation_text": ""
  },
  "freeze": {
    "frozen_before_birth_or_chart_reveal": true,
    "birth_or_chart_data_in_this_export": false,
    "do_not_recode_after_target_reveal_without_versioning": true
  }
}
```

Each `turns` record must contain:
- `sequence`
- `question_id`
- `question_text`
- `answer_text`
- `answer_status`
- `conditions`
- `corrections`
- `process_feedback`

Each `neutral_evidence` record must contain:
- `evidence_id`
- `question_ids`
- `source_quotes`
- `observation`
- `evidence_type`
- `conditions`
- `certainty`
- `target_ids`
- `limits`

Each `coverage` record must contain:
- `question_id`
- `status`
- `reason`

Allowed `interview_status` values:
- `complete`
- `partial`
- `stopped_by_participant`

Allowed coverage statuses:
- `answered`
- `suppressed_not_admissible`
- `skipped`
- `not_applicable`
- `not_reached_after_natural_stop`

If the interview ends early, still export all completed turns with the appropriate status.

## After export

End the behavioral interview after the JSON is frozen.

Tell the participant only to copy the complete JSON to Joel. Do not score the interview, guess a birth date/time, or revise the frozen JSON based on later target information.

The research team will handle any later comparison separately.
