"""Render a read-only review map from the exact checked-in bank and graph.

Requires Graphviz's `dot` for SVG layout. No network or model calls.
Mermaid source and the SVGs use the same node/edge records.
"""
from pathlib import Path
import json, html, subprocess, re, textwrap
ROOT=Path(__file__).resolve().parent
bank=json.loads((ROOT/'interviewer-bank-v6.json').read_text())
graph=json.loads((ROOT/'ROUTING-GRAPH.json').read_text())
q={x['id']:x for x in bank['questions']}; c={x['id']:x for x in graph['routing_contracts']}
labels={
'A0':'Friend asks for company','WHY':'Reason for stated action','G23':'What you notice','CARE-RESPONSIBILITY':'Scope of responsibility','CARE-LIMIT':'Limits on helping','G19':'What matters in a conflict','AFTER-CHOICE':'Living with the choice','F0':'What you would say','G05':'Self-rated influence','PREFER-INFLUENCE':'Wish to persuade','M11':'Explain an arrangement','G06':'Taking a role unasked','R02':'Taking a role when asked','G07':'Usual connection pathway','OUTREACH':'Creating a wanted connection','G08':'Familiarity with excess demands','R03':'Response to excess demands','M07':'How a skill developed','M08':'Requests based on ability','G01':'Organize conflicting details','VERIFY':'Decide what to trust','G02':'Share an understanding','G03':'Unresolved attention','R01':'What permits closure','G04':'A failed guide step','WORKING-METHOD':'A guide that works','D0':'Repetitive practice','PRACTICE-REASON':'Value of practising','G22':'Concentration after interruption','FOCUS-DEPTH':'Uninterrupted concentration','E0':'Next step in a choice','G09':'Early bodily response','CHOICE-TIME':'Clarity over time','R04':'Perceived usefulness','M10':'Within-choice time course','SIGNAL-DEPENDABILITY':'Occurrence across choices','SIGNAL-NOT-FOLLOWED':'When a cue is set aside','M05':'Noticing a warning cue','M06':'Reliance in unfamiliar contexts','G10':'Response to external schedule','ADAPTATION':'Acceptable changes','G20':'Purpose of spare money','STATUS':'Value of recognition','OWNERSHIP':'Value of ownership','M03':'A dull promised task','M04':'Intention when tired','C0':'Reaction to cancellation','G21':'Shape of a free day','ROUTINE-CHANGE':'Familiar versus new','M09':'Keep or change a system','G11':'Room conditions noticed','ROOM-EFFECT':'Effect of the condition','G12':'What starts attraction','G13':'What deepens closeness','R05':'More contact','ROMANCE-FADE':'What weakens closeness','PHYSICAL-CLOSENESS':'Physical affection','G14':'Mood when alone','B0':'Response to another’s worry','R06':'Mood during disagreement','MOOD-AFTER':'Emotional aftermath','M01':'Internal urgency','M02':'After pressure stops','G15':'Ordinary-work energy','R07':'Energy after a burst','R08':'Energy after prolonged overload','R09':'Stopping cues','WORK-RECOVERY':'Energy after stopping','G16':'What makes effort worthwhile','R10':'When to disengage','G18':'After a social day','R11':'Readiness to re-engage','G24':'Earlier-life response','LIFE-PHASE':'When change emerged','R12':'Attributed contributors','G17':'Response to an error','CORRECTION-REASON':'When correction matters','G25':'Trust after missed commitments','R13':'Future reliance'}

def mermaid_id(s):return re.sub('[^A-Za-z0-9_]','_',s)
def quoted(s):return json.dumps(s,ensure_ascii=False)
def dot_svg(nodes,edges,title):
    lines=['digraph G {','graph [rankdir=TB, bgcolor="transparent", pad="0.2", nodesep="0.35", ranksep="0.45"];','node [shape=box, style="rounded", fontname="Arial", fontsize=13, margin="0.14,0.09"];','edge [fontname="Arial", fontsize=10];']
    for nid,label,kind,href in nodes:
        label='\n'.join(textwrap.wrap(label,29))
        attrs=[f'label={quoted(label)}']
        if kind=='information':attrs.extend(['shape=note','style=""'])
        if kind=='external':attrs.append('style="rounded,dashed"')
        if kind=='decision':attrs.extend(['shape=diamond','style=""'])
        if href:attrs.append(f'URL={quoted(href)}')
        lines.append(quoted(nid)+' ['+','.join(attrs)+'];')
    for a,b,kind,label in edges:
        style='dotted' if kind=='may_inform' else 'dashed' if kind=='advisory_context' else 'solid'
        lines.append(f'{quoted(a)} -> {quoted(b)} [style={style},label={quoted(label)}];')
    lines.append('}');p=subprocess.run(['dot','-Tsvg'],input='\n'.join(lines),text=True,capture_output=True,check=True)
    svg=p.stdout[p.stdout.index('<svg'):]
    prefix=re.sub('[^A-Za-z0-9_]','_',title)
    svg=re.sub(r'id="([^"]+)"',lambda m:'id="'+prefix+'_'+m.group(1)+'"',svg)
    svg=svg.replace('<svg ',f'<svg role="img" aria-label="{html.escape(title,quote=True)}" ',1)
    return svg

def mmd(nodes,edges):
    lines=['flowchart TD']
    for nid,label,kind,href in nodes:
        lines.append('    '+mermaid_id(nid)+'["'+label.replace('"','&quot;')+'"]')
    for a,b,kind,label in edges:
        arrow='-.->' if kind in ['may_inform','advisory_context'] else '-->'
        lines.append(f'    {mermaid_id(a)} {arrow}|"{label}"| {mermaid_id(b)}')
    return '\n'.join(lines)

flow_nodes=[('read','Read the whole reply','question',''),('save','Preserve privately; verify or report a save failure','question',''),('stop','Stop requested?','decision',''),('paused','Remain paused; no next question','question',''),('separate','Separate answer, correction and process feedback','question',''),('repair','Resolve process confusion; re-evaluate corrected sources','question',''),('choose','Choose one useful unanswered distinction','question',''),('gate','Context and prerequisites established?','decision',''),('other','Skip this route; choose another or pause','question',''),('ask','Ask one contextualized question','question',''),('meaning','Retain only source-supported meaning','question',''),('information','Partial, unknown and declined stay distinct','information','')]
flow_edges=[('read','save','flow',''),('save','stop','flow','no saved claim without readback'),('stop','paused','flow','yes'),('stop','separate','flow','no'),('separate','repair','flow','when needed'),('repair','choose','flow',''),('separate','choose','flow','otherwise'),('choose','gate','flow',''),('gate','other','flow','no'),('gate','ask','flow','yes'),('other','choose','flow','another useful route'),('other','paused','flow','nothing useful remains'),('ask','read','flow','next actual reply'),('separate','meaning','may_inform','answer clauses'),('meaning','information','may_inform','not a completed-profile score')]
flow_svg=dot_svg(flow_nodes,flow_edges,'Text-only interview flow and preservation boundaries')
# A separate, small motive example avoids a mega-graph.
friend_nodes=[('inv','Friend asks for company','question',''),('act','A reply is given','question',''),('why','Reason still missing?','decision',''),('open','Ask an open reason question','question',''),('keep','Keep stated reason; do not re-ask','question',''),('away','Move to another useful scene','question','')]
friend_edges=[('inv','act','flow',''),('act','why','flow','stop always overrides'),('why','open','flow','yes and useful'),('why','keep','flow','no'),('open','keep','flow','after an actual explanation'),('keep','away','flow','no hidden guilt search')]
friend_svg=dot_svg(friend_nodes,friend_edges,'Friend invitation: action and motive remain separate')
parts=[];md=['# Scenario-first graph index\n','Text-only reviewed design. Graph links do not create a fixed questionnaire or evidence credit.','## Conversation and preservation\n','```mermaid\n'+mmd(flow_nodes,flow_edges)+'\n```','## An invitation and its reason\n','```mermaid\n'+mmd(friend_nodes,friend_edges)+'\n```']
question_md=['# Reviewed scenario bank — v6.0','\nText-only design. 79 available entries; no required question count. One response task per turn. The pilot remains paused.\n',bank['intro'],'\nThe full admission and interpretation rules are in `INTERVIEW-PROTOCOL.md` and `interviewer-bank-v6.json`. Context arrows name possible referents, not a mandatory order.\n']
for family in graph['families']:
    own={'q:'+x for x in family['question_ids']}
    related=[e for e in graph['edges'] if e['to'] in own or (e['from'] in own and e['kind']=='may_inform')]
    included=own|{e[k] for e in related for k in ('from','to')}
    n=[]
    for nid in sorted(included):
        if nid.startswith('q:'):
            qid=nid[2:];n.append((nid,qid+' · '+labels[qid],'question' if nid in own else 'external','#q-'+qid))
        else:n.append((nid,nid[2:].replace('_',' '),'information','#f-'+nid[2:].replace('.','-')))
    ed=[(e['from'],e['to'],e['kind'],'may inform' if e['kind']=='may_inform' else 'related only' if e['kind']=='advisory_context' else 'possible context') for e in related]
    svg=dot_svg(n,ed,family['title'])
    rows=[];question_md.append('\n## '+family['title']+'\n')
    for qid in family['question_ids']:
        node=q[qid];rule=c[qid]
        flags=', '.join(rule['required_annotations']).replace('_',' ') or 'Apply global admission; no reaction-specific antecedent.'
        rows.append(f'<details id="q-{qid}" class="question" data-text="{html.escape((qid+" "+node["question"]).lower(),quote=True)}"><summary><strong>{html.escape(labels[qid])}</strong> <span>{qid}</span></summary><p class="prompt">{html.escape(node["question"])}</p><p><b>Ask only when:</b> {html.escape(node["admission"])}</p><p><b>Interpretation limit:</b> {html.escape(node["interpretation_limit"])}</p><p><b>Graph check:</b> {html.escape(rule["context_mode"]+"; "+flags)}</p></details>')
        question_md+=['### '+labels[qid]+' ('+qid+')',node['question'],'','*Admission:* '+node['admission'],'']
    parts.append(f'<section class="family" id="family-{family["id"]}"><h2>{html.escape(family["title"])}</h2><p>Solid links supply possible context. Dotted links only identify information a response may supply. Dashed outside nodes belong to another family.</p><div class="diagram">{svg}</div>'+''.join(rows)+'</section>')
    md+=['## '+family['title']+'\n','```mermaid\n'+mmd(n,ed)+'\n```']
evidence=json.loads((ROOT/'EVIDENCE-GUIDE-v6.json').read_text())
evidence_html=''.join(f'<details id="f-{e["facet_id"].replace(".","-")}"><summary>{html.escape(e["facet_id"])}</summary><p><b>Fictional illustration:</b> {html.escape(e["fictional_answer"])}</p><p><b>Supports only:</b> {html.escape(e["narrow_supported_reading"])}</p><p><b>Does not support:</b> {html.escape(e["unsupported_extension"])}</p></details>' for e in evidence)
nav=''.join(f'<a href="#family-{f["id"]}">{html.escape(f["title"])}</a>' for f in graph['families'])
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Scenario-first survey — graph review</title><style>
*{box-sizing:border-box}body{font:17px/1.55 system-ui,sans-serif;color:#202020;background:#fff;margin:0}header,main{max-width:1120px;margin:auto;padding:30px 26px}header{border-bottom:2px solid #222}h1{font-size:2rem;line-height:1.2}h2{margin-top:2rem}p{max-width:85ch}.badge{display:inline-block;border:1px solid;padding:4px 10px;font-size:.85rem}nav{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px}a{color:inherit;text-underline-offset:3px}nav a{padding:7px;border-bottom:1px solid #ddd}.diagram{overflow:auto;border:1px solid #ddd;margin:18px 0;padding:12px}.diagram svg{display:block;max-width:100%;height:auto;margin:auto}.family{padding-top:14px;border-top:1px solid #999;margin-top:35px}details{border-bottom:1px solid #ddd;padding:12px 0}summary{cursor:pointer;padding:4px}summary span{font-size:.85rem;margin-left:10px}.prompt{font-size:1.12rem;padding-left:16px;border-left:3px solid}.two{display:block}.two>div{margin-bottom:28px}.note{border-left:3px solid;padding-left:15px}details:target{outline:2px solid;padding:12px}input{font:inherit;padding:10px;width:100%;max-width:600px}button{font:inherit;padding:8px 12px;margin:8px 0}label{display:block;margin:20px 0 6px}footer{margin-top:40px;border-top:1px solid;padding-top:20px}@media(max-width:700px){.diagram svg{max-width:none;min-width:640px}header,main{padding:20px 16px}.two{grid-template-columns:1fr}h1{font-size:1.6rem}}@media print{nav,input,button,label{display:none}.family{break-before:page}details{break-inside:avoid}}
</style></head><body><header><div class="badge">TEXT-ONLY DESIGN · PILOT PAUSED</div><h1>Scenario-first survey<br>Graph review</h1><p>The graph organizes <b>79 question entries</b> in <b>28 families</b>, with <b>73 information-planning labels</b>. These are not required answer counts, a trait score, or proof of AstroHD recovery.</p><p class="note">This is a read-only document. It makes no network requests, collects no responses, and is not the Railway application.</p></header><main><h2>How the conversation works</h2><p>On a narrow screen, scroll each diagram sideways. Every question also has a readable text panel below its topic graph.</p><p>The graph is an index over the protocol. It does not force a path through every scene. Pausing, corrections, privacy and already-answered information control what happens next.</p><div class="two"><div class="diagram">FLOW</div><div><h3>A friend asks for company</h3><div class="diagram">FRIEND</div><p>A bare yes may need one open reason question. A yes with a stated reason does not. Neither a friendly action nor a diagram arrow establishes guilt or responsibility.</p></div></div><h2>Choose a topic</h2><nav>NAV</nav><label for="search">Find a question by wording or identifier</label><input id="search" type="search" placeholder="For example: pressure, practice, M02"><button id="clear" type="button">Clear search</button><p id="result" role="status"></p>FAMILIES<section id="evidence"><h2>What the information labels mean</h2><p>These are fictional illustrations of narrow interpretation. They are not respondent data or automated validation. A single example may support only part of a compound label.</p>EVIDENCE</section><footer><p>Version: scenario-bank-v6.0-20260919. Source: ROUTING-GRAPH.json and interviewer-bank-v6.json. Source-controlled Mermaid views are in SCENARIO-GRAPH.md. The audit model checks explicitly reviewed annotations, not free-text interpretation.</p></footer></main><script>
const search=document.querySelector('#search');const result=document.querySelector('#result');const families=[...document.querySelectorAll('.family')];
function filter(){let n=0;const term=search.value.toLowerCase().trim();for(const f of families){let hits=0;for(const d of f.querySelectorAll('.question')){const ok=!term||d.dataset.text.includes(term);d.hidden=!ok;if(ok){hits++;n++;}if(term&&ok)d.open=true;}f.hidden=hits===0;f.querySelector('.diagram').hidden=Boolean(term);}result.textContent=term?n+' matching questions':'';}
search.addEventListener('input',filter);document.querySelector('#clear').addEventListener('click',()=>{search.value='';filter();});
function jump(){const id=decodeURIComponent(location.hash.slice(1));if(!id)return;const el=document.getElementById(id);if(el){search.value='';filter();if(el.tagName==='DETAILS')el.open=true;requestAnimationFrame(()=>el.scrollIntoView());}}
window.addEventListener('hashchange',jump);jump();
</script></body></html>'''
for key,value in [('FLOW',flow_svg),('FRIEND',friend_svg),('NAV',nav),('FAMILIES',''.join(parts)),('EVIDENCE',evidence_html)]:page=page.replace(key,value)
(ROOT/'GRAPH-EXPLORER.html').write_text(page,encoding='utf-8')
(ROOT/'SCENARIO-GRAPH.md').write_text('\n\n'.join(md)+'\n',encoding='utf-8')
(ROOT/'REVIEWED-QUESTIONS.md').write_text('\n\n'.join(question_md)+'\n',encoding='utf-8')
(ROOT/'overview.svg').write_text(flow_svg,encoding='utf-8')
print('Rendered overview, friend example and',len(parts),'family graphs. No network used.')
