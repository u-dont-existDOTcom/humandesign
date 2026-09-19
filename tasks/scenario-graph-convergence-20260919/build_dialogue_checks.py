"""Write authored review cases, not simulated respondents or model executions."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
B=json.loads((P/'interviewer-bank-v6.json').read_text());Q={x['id']:x for x in B['questions']}
rows=[
('T01','A0',"Yes, I'd go.",'What would make you say yes?', 'Going is the anticipated action; the reason is still unknown.','Do not infer guilt or generosity from agreement.'),
('T02','A0',"Yes, because I enjoy seeing them. Let's stop here.",None,'Save both the action and the stated enjoyment, and honor the stop.','No next question, even a relevant one, after an explicit stop.'),
('T03','A0',"I'd suggest tomorrow. Today I want to finish the book.",None,'Negotiation and its reason are already supplied. Choose another useful scene only if continuing is welcome.','Do not apply the yes template or ask the reason again.'),
('T04','G06',"I'd chop vegetables. If someone asked me to coordinate, I'd do that instead.",None,'One message supplies both action branches with invitation as the named condition.','Do not require a second turn or ask R02 just to obtain another record.'),
('T05','G24',"When I was younger I'd go immediately; these days I'd suggest later.",'What do you think contributed to that change?','A current-versus-earlier contrast is explicit. The contributor probe is optional if still useful and welcome.','Do not reject a declared time-perspective change as accidental context drift.'),
('T06','G09',"Actually, that tightness was about being late, not whether the class suited me.",None,'Append the correction; withdraw any previous interpretation as a choice-suitability signal.','R04 and M10 must not continue from the superseded signal interpretation. Generic choice questions remain separate.'),
('T07','G09',"I don't notice anything in my body. I might still be unsure tomorrow.",None,'Record no noticed sensation and continuing uncertainty; the temporal-clarity point is already answered.','No sensation-specific probes, and no duplicate CHOICE-TIME question.'),
('T08','G09',"It is brief and happens on similar choices. I haven't said whether it helps me decide.",'How useful is that reaction when you are deciding whether a choice suits you?','Duration and occurrence have been supplied, but perceived usefulness is still missing.','Do not ask M10 or SIGNAL-DEPENDABILITY again.'),
('T09','B0',"I'd be concerned for them but stay calm myself.",'Once that conversation is over, what usually happens to that concern?','Concern and calmness coexist; the aftermath question names the specific reported concern.','Do not erase concern by coding completely unchanged emotion, or call it emotional contagion.'),
('T10','B0',"I'd get tense, but I don't want to discuss this relationship further.",None,'Preserve the reported tension; close this relationship topic.','Neither generic MOOD-AFTER nor WHY may bypass the source-topic refusal.'),
('T11','M01',"I'd feel hurried even though the deadline was unchanged.",'Returning to the task where someone was urging you to hurry: that person leaves and the pressure stops, while the task and deadline stay the same. What would usually change for you?','After an intervening money discussion, name the original pressure scene in the actual utterance.','Do not let the bare phrase that person refer to the last unrelated topic.'),
('T12','R08',"After weeks of that I'd feel depleted and need several quiet days to recover.",None,'Retain depletion plus the stated recovery pattern under prolonged overload.','No claim about manageable workload, and no redundant WORK-RECOVERY probe.'),
('T13','M07',"I can't think of an ability to discuss.",None,'Leave this information unknown and move on if another topic is useful.','Do not ask M08 about an ability the person never named.'),
('T14','G20',"I'd use the extra money to work less, not to buy impressive things.",None,'Retain the resource purpose and the volunteered rejection of that spending motive, each at its scope.','Do not infer all status/ownership motives or automatically ask every remaining money prompt.'),
('T15','G25',"I'd rely on them less for tasks, but still trust them with private things. No need to explore repair.",None,'Save the task-specific trust distinction and honor the narrower repair refusal.','R13 must not reopen the closed repair topic; this is not a global stop.'),
('T16','G23',"I'd notice the food. Your question doesn't tell me anyone needs help.",None,'Retain the noticing response and process feedback separately.','No need or responsibility is established, so CARE-RESPONSIBILITY is not admitted.')]
out=[]
for id,qid,answer,nxt,retained,rejected in rows:
 out.append({'id':id,'question_id':qid,'question':Q[qid]['question'],'fictional_reply':answer,'next_utterance':nxt,'retained_reading':retained,'reject':rejected,'case_note':'T11 explicitly assumes a topic change after the displayed reply.' if id=='T11' else '', 'review_class':'authored same-context semantic design review; not independent data or NLP execution'})
(P/'DIALOGUE-CHECKS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
s=['# Graph-focused dialogue checks','', 'All 16 cases are authored review examples, not actual participants, independent evaluations or live interviewer runs. A null next utterance means no further probe is required by this example; it means STOP only where explicitly stated.','']
for x in out:
 s += [f"## {x['id']} — {x['question_id']}",'', '**Question:** '+x['question'],'', '**Fictional reply:** '+x['fictional_reply'],'','**Next:** '+(x['next_utterance'] or 'No dependent probe required; respect the stated scope or stop.'),'','**Retain:** '+x['retained_reading'],'','**Reject:** '+x['reject'],'',x['case_note'],'']
(P/'DIALOGUE-CHECKS.md').write_text('\n'.join(s))
