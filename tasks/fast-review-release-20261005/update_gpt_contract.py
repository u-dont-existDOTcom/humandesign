from pathlib import Path
import copy,json
root=Path(__file__).resolve().parents[2]
custom=root/'reference/custom_gpt'
p=root/'apps/life-patterns-participant/participant/static/action-openapi.yaml'
d=json.loads(p.read_text());d['info']['version']='1.3.0'
schemas=d['components']['schemas']
schemas['ReviewStart']['properties']['review_protocol']={
 'type':'string','enum':['legacy-v1','fast-batch-v1'],
 'description':'Use fast-batch-v1 for a new review. Recover an existing request with its unchanged saved body, including an omitted legacy protocol.'}
schemas['ReviewStart']['example']['review_protocol']='fast-batch-v1'
props=copy.deepcopy(schemas['ClarificationAnswer']['properties']);props.pop('operation_id')
schemas['BatchAnswer']={'type':'object','additionalProperties':False,'properties':props,
 'required':['clarification_id','answer_text','skipped']}
schemas['ClarificationBatchAnswers']={'type':'object','additionalProperties':False,'properties':{
 'batch_id':{'type':'string','pattern':'^B-[a-f0-9]{32}$'},
 'operation_id':copy.deepcopy(schemas['ClarificationAnswer']['properties']['operation_id']),
 'answers':{'type':'array','minItems':1,'maxItems':3,'items':{'$ref':'#/components/schemas/BatchAnswer'}}},
 'required':['batch_id','operation_id','answers']}
new=copy.deepcopy(d['paths']['/api/gpt/reviews/{review_id}/clarifications']['post'])
new.update(operationId='submitLifePatternsClarificationBatch',summary='Save an ordered batch of exact answers or skips',description='Ask supplied questions one at a time locally. Send exact answers/skips in batch order with the issued batch_id. An answered prefix may be sent early if a later question no longer fits; unasked remainder is invalidated, not skipped. Reuse operation_id and identical body on retries.')
new['requestBody']['content']['application/json']['schema']={'$ref':'#/components/schemas/ClarificationBatchAnswers'}
d['paths']['/api/gpt/reviews/{review_id}/clarification-batches']={'post':new}
d['paths']['/api/gpt/reviews']['post']['description']='Queue the exact unfrozen candidate with review_protocol fast-batch-v1. Preserve its private review ID. Show the returned stage estimate and recommended_check_after_seconds. First questions and full final review are separate stages; queued is not ready.'
d['paths']['/api/gpt/reviews/{review_id}']['get']['description']='Read the same saved review. Report review_stage_label, wait_guidance and recommended_check_after_seconds. Stage estimates are not deadlines. Queued/offline/overdue work has no reliable remaining-time promise. Do not poll repeatedly.'
p=schemas['ReviewStatus']['properties']
p.update({
 'review_protocol':{'type':'string'},'batch_id':{'type':['string','null']},
 'clarifications':{'anyOf':[{'type':'array','maxItems':3,'items':{'$ref':'#/components/schemas/Clarification'}},{'type':'null'}]},
 'final_review_completed':{'type':'boolean'},'review_stage':{'type':'string'},'review_stage_label':{'type':'string'},
 'estimate_basis':{'type':['string','null']},'stage_elapsed_seconds':{'type':['integer','null']},
 'worker_heartbeat_age_seconds':{'type':['integer','null']},'estimate_exceeded':{'type':'boolean'},
 'worker_status_uncertain':{'type':'boolean'},'wait_guidance':{'type':'string'},
})
for name in ['estimated_stage_seconds','estimated_remaining_seconds']:
 p[name]={'anyOf':[{'type':'object','additionalProperties':False,'properties':{'low':{'type':'integer'},'high':{'type':'integer'}},'required':['low','high']},{'type':'null'}]}
for path in d['paths'].values():
 for op in path.values():
  assert len(op.get('description',''))<=300,(op['operationId'],len(op['description']))
(root/'apps/life-patterns-participant/participant/static/action-openapi.yaml').write_text(json.dumps(d,indent=2)+'\n')

p=custom/'life_patterns_voice_interviewer_v2.md';s=p.read_text();a=s.index('## Railway review before freeze');b=s.index('## Final review and freeze',a)
s=s[:a]+'''## Railway review before freeze

Follow `ACTION-HANDOFF-GUIDE-v1.md`: exact unfrozen backup and real links FIRST; save the consent/request envelope. Say its approval sentence **once only** per Action. On failure give backup + safe diagnostic.

At natural saturation, do not show final review, freeze or ask CF-003. Call `startLifePatternsReview` with genuine consent, random 32-character `request_id` and `review_protocol: fast-batch-v1`. Reuse the saved envelope for retries/recovery, including any legacy omission of protocol. Keep `review_id` private; never truncate source.

For queued/processing, state the returned stage, estimate range and `recommended_check_after_seconds`; follow `wait_guidance`. First questions: roughly 1–3 minutes; full evidence preparation: roughly 5–12 minutes, then independent checking. Estimates start with work, exclude queue time and are not deadlines. Report overdue/offline/blocked states without invented remaining time. They may leave. On return, check the same review once; no repeated polling or promised notification.

Ask returned `clarifications` one at a time, verbatim, with no Action between independent questions. Keep exact Q&A. Send ordered answers/skips once through `submitLifePatternsClarificationBatch` using `batch_id` and fresh `operation_id`. If later questions become invalid, send only the answered prefix; never invent skips. Use the single-answer Action for legacy responses. Skip is null/skipped, never trait evidence. Use guide backups/retries/cancellation. No question-count cap or coverage-only questions.

Only `ready` permits final review. Honor pause/stop/withdraw through the control Action. After error/resource repair, retry that review when asked; blocked is not complete. No replacement job.

''' + s[b:]
assert len(s)+s.count('\n')<=8000,(len(s),s.count('\n'))
p.write_text(s)
print('INSTRUCTION_STRICT',len(s)+s.count('\n'))

p=custom/'ACTION-HANDOFF-GUIDE-v1.md';s=p.read_text()
s=s.replace('the exact three-field request envelope','the exact request envelope').replace('saved three-field body','saved request body')
s=s.replace('The request has THREE required top-level fields;', 'The request has THREE required top-level fields plus `review_protocol: fast-batch-v1` for new fast reviews;')
s=s.replace("        'candidate_record': candidate}","        'candidate_record': candidate,\n        'review_protocol': 'fast-batch-v1'}")
a=s.index('If the participant asks how long remains,');b=s.index('## Explain external-action',a)
s=s[:a]+'''## Review timing: explain every waiting step

When asked how long remains, separate the adaptive interview, first clarifications, further reconciliation, full evidence review, participant confirmation, secondary questions and submission. The interview and human-answer stages have no reliable fixed duration.

For EVERY queued/processing response, show the returned `review_stage_label`, `estimated_stage_seconds` range and `recommended_check_after_seconds` in readable minutes/seconds. Use `wait_guidance` and report a remaining range only when `estimated_remaining_seconds` is non-null. These are limited-pilot estimates, not deadlines or a guaranteed finish time. Use the server's current interval over the fallbacks below.

| Review step | Working estimate from stage start | Default check-back |
|---|---|---|
| Initial gap search / first clarification path | about 1–3 minutes | about 3 minutes |
| Reconciliation after a batch of answers | about 1–4 minutes | about 3 minutes |
| Independent check of proposed gaps | about 15–90 seconds | about 1 minute |
| Question wording and review | about 15–90 seconds | about 1 minute |
| Broader omission/conflict check | about 2–8 minutes | about 5 minutes |
| Full evidence preparation | about 5–12 minutes | about **10 minutes** |
| Independent final evidence check | about 1–3 minutes | about 3 minutes |

The roughly two-minute first-batch observation came from 81-turn pilot records, not from a guarantee for everyone. Reconciliation/full-review ranges remain broad provisional planning guidance. A stage may need repair or another useful clarification. Do not add these rows into a precise total or reset the estimate repeatedly when the same stage is unchanged.

`queued` means saved but not yet started: queue time is unknown and the pilot reviewer needs the researcher's computer online. If heartbeat is stale or the estimate is exceeded, use the server's warning and null remaining estimate; do not keep promising “nearly done.” A delayed active stage normally asks for another check in about two minutes; an uncertain/offline worker about five. Error/resource-limited is blocked, not quietly working; waiting alone will not repair it.

Example: “Your answers are saved. The service is now preparing the full evidence review. The current estimate is about 5–12 minutes from this stage's start; check back in about 10 minutes. You can leave this chat and return with any message. This is an estimate, not a deadline.” Use the ACTUAL returned stage and interval, not this example unconditionally. ChatGPT does not wake itself or send an automatic notification for this workflow.

''' +s[b:]
a=s.index('After `startLifePatternsReview` returns `queued`');b=s.index('While a known review is pending,',a)
s=s[:a]+'''After `startLifePatternsReview` returns `queued` or `processing`, apply the timing section above. Tell the participant the current stage, its estimate and when to check back. Distinguish first questions from the later full review. They need not keep the chat open; work is held by the study service and its worker, not by an open Action request.

''' +s[b:]
a=s.index('- `queued`: saved, awaiting a worker.');b=s.index('- `ready`:',a)
s=s[:a]+'''- `queued` / `processing`: report the exact saved state and stage, range and returned check-back interval; never infer a completion percentage.
- `clarification_needed` with a `batch_id` and `clarifications`: preserve the entire private batch, order and IDs. Ask each returned `question_text` exactly, one question at a time locally; do not call Railway between independent questions. Append each actual Q&A to the local source, using its returned `route_id` as `canonical_question_id`, `turn_role: behavioral`, and empty `conditions`, `corrections`, `process_feedback`; preserve all conditions in the exact answer text. An explicit skip is `answer_text: null` in the local source and `{answer_text: "", skipped: true}` in the batch request. Never invent an answer or treat an unasked question as skipped.
- Before batch submission, create and link an updated source backup and a private `life-patterns-clarification-batch-handoff.json` containing `batch_id`, a random `operation_id` and the ordered `answers` array. Each answer contains only `clarification_id`, exact `answer_text`, and `skipped`. Parse back and verify every string/order. Call `submitLifePatternsClarificationBatch` once. Reuse that body/operation ID on ambiguous retry. A service receipt, not local collection, means those answers are saved on Railway.
- If an answer corrects a premise or makes a later question invalid, do not improvise a replacement or ask it anyway. Submit only the completed ordered prefix immediately. The backend discards the unasked remainder and reconciles the new source before issuing another batch. After a resumed/lost-context chat, fetch current status before asking any saved batch question; an old batch ID cannot be reused for a new batch. Preserve locally collected unsubmitted answers exactly and reconcile their IDs before sending.
- For a legacy response without batch metadata, ask the single returned clarification exactly, then use `submitLifePatternsClarification` with its `clarification_id` and an idempotent fresh `operation_id` as before.
- Another batch is allowed only when independent review finds a still-admissible, nonredundant and materially useful gap. Three is a transport batch maximum, never a lifetime clarification cap. Coverage alone is not a reason to ask more.
''' +s[b:]
p.write_text(s)
print('ACTION_AND_GUIDE_UPDATED')
