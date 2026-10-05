"""Freeze synthetic Pro-authored cases and targets before any application-model replay."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
TASK=Path(__file__).resolve().parent
bank=json.loads((ROOT/'tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json').read_text())['questions']
questions={r['id']:r['question'] for r in bank}
def turn(rid,answer,uid):
 return {'turn_id':uid,'canonical_question_id':rid,'question_text':questions[rid],'answer_text':answer}
paraphrase="I'm spending several hours preparing supper for just myself and a friend. I proposed they cover the groceries; they say that cost is too much. What would I say back?"
cases=[
 {'case_id':'PRO1','turns':[
  turn('M09',"The one deciding issue is whether I actually need shared reminders with another person. At present I don't, so I prefer the offline app.",'p1a'),
  turn('G19',"The commitment I made matters most, unless continuing would make me miss another promise. Those are the factors I'd use.",'p1b'),
  turn('M11',"I'd suggest a smaller grocery bill. I normally want to make one alternative offer, but after that I'd rather drop the plan than keep negotiating.",'p1c')]},
 {'case_id':'PRO2','turns':[
  turn('G20',"I'd want the money to take care of that particular matter I've had in mind. That's all I've said about what it would do.",'p2a')]},
 {'case_id':'PRO3','turns':[
  {'turn_id':'p3a','canonical_question_id':None,'question_text':paraphrase,
   'answer_text':"I'd suggest splitting the bill. Sometimes I want to keep negotiating and sometimes I want to abandon it straight away; I haven't said what my usual inclination is or what makes the difference."}]},
 {'case_id':'PRO4','turns':[
  turn('M09',"I'd put a trial copy on my phone and experiment with it before deciding.",'p4a'),
  *[turn('G23',"The first thing I notice is whether anyone is sitting apart and needs company.",f'p4fill{i}') for i in range(6)],
  {'turn_id':'p4z','canonical_question_id':None,'question_text':'Is there anything else about the software change?',
   'answer_text':"Yes. Offline reliability is the only result of the trial that would make me choose one app over the other. I already have all the collaboration I need."}]},
 {'case_id':'PRO5','turns':[
  turn('G20',"It would be for the thing I haven't described.",'p5a'),
  {**turn('G20',"That answer was incomplete. I want a financial buffer so next month's rent does not depend on when a freelance payment arrives.",'p5b'),'correction_of':'p5a'},
  turn('G19',"I cannot give an answer about that situation and would prefer to skip this topic.",'p5c')]},
 {'case_id':'PRO6','turns':[
  turn('G20',"I would use it for a certain purpose, but I have not identified what that purpose is.",'p6a'),
  turn('G19',"Keeping my promise matters most; my own plans would not affect this decision at all.",'p6b'),
  {'turn_id':'p6c','canonical_question_id':None,
   'question_text':"For the same friend's move, with precisely the same conditions, what matters most to you?",
   'answer_text':"Protecting my own planned time is the only thing that matters. The promise would play no part in my decision."}]},
]
expected={'PRO1':[], 'PRO2':['G20'], 'PRO3':['PREFER-EXCHANGE'], 'PRO4':[], 'PRO5':[], 'PRO6':['G20','G19']}
packet={'schema':'life-patterns-pro-review-semantic-cases-v1','synthetic_only':True,
 'method':'Pro-authored, source-requirement tests; complete bank is visible; no addressed-route masking; not a claim of blind independent scientific validation.','cases':cases}
for name,obj in [('PRO-SEMANTIC-CASES-20261005.json',packet),('PRO-SEMANTIC-EXPECTED-20261005.json',{'schema':'life-patterns-pro-review-targets-v1','cases':[{'case_id':cid,'decision':'clarification_needed' if ids else 'review_ready','route_ids':ids} for cid,ids in expected.items()]})]:
 p=TASK/name
 if p.exists():raise SystemExit('Freeze exists; refusing overwrite: '+name)
 p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('FROZEN_SIX_PRO_CASES')
