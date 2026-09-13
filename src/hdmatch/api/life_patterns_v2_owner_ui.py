"""Owner-facing browser UI for the bounded Life Patterns v2 real-data prototype."""

HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Discover Your Unique Life Patterns — owner development</title>
<style>
:root{--ink:#20242a;--muted:#667085;--line:#d0d5dd;--soft:#f7f8fa;--accent:#315c5f;--user:#eef6f6;--ai:#f7f3eb;--good:#176b44;--warn:#8a5a00;--bad:#a61b1b}
*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--ink);font:16px/1.55 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{width:min(58rem,calc(100% - 2rem));margin:2rem auto 5rem}h1{font-size:clamp(2rem,7vw,3.5rem);line-height:1.02;letter-spacing:-.04em;margin:.2rem 0 .7rem}h2,h3{margin:.2rem 0 .65rem}.lede{font-size:1.08rem;color:var(--muted);max-width:48rem}.card{border:1px solid var(--line);border-radius:1rem;padding:1.1rem;margin:1rem 0;background:#fff}.soft{background:var(--soft)}.chat{display:grid;gap:.8rem;margin:1rem 0}.bubble{padding:.9rem 1rem;border-radius:.85rem;max-width:94%;white-space:pre-wrap}.bubble.user{background:var(--user);margin-left:auto}.bubble.ai{background:var(--ai)}.meta{font-size:.82rem;color:var(--muted);margin-bottom:.25rem}.pill{display:inline-block;font-size:.82rem;border:1px solid var(--line);border-radius:999px;padding:.25rem .6rem;color:var(--muted)}textarea,input,button{font:inherit;border:1px solid #98a2b3;border-radius:.55rem;padding:.72rem .8rem}textarea{width:100%;min-height:8rem;resize:vertical}button{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:750;cursor:pointer}button.secondary{background:#fff;color:var(--accent)}button.subtle{background:#fff;color:var(--ink);border-color:var(--line)}button.danger{background:#fff;color:var(--bad);border-color:#e5a6a6}button:disabled{opacity:.5;cursor:not-allowed}.row{display:flex;gap:.65rem;flex-wrap:wrap;align-items:center}.hidden{display:none}.note{font-size:.91rem;color:var(--muted)}.good{color:var(--good)}.warn{color:var(--warn)}.error{color:var(--bad)}.fact{border:1px solid var(--line);border-radius:.8rem;padding:.85rem;margin:.7rem 0}.fact p{margin:.2rem 0 .6rem}.fact .edit{margin-top:.7rem}.smallcaps{font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:750}.result{border-left:4px solid var(--accent);padding:.9rem 1rem;background:#f2f8f8;margin:1rem 0}.topbar{display:flex;justify-content:space-between;gap:1rem;align-items:center;flex-wrap:wrap}.count{font-size:.88rem;color:var(--muted)}.divider{border:0;border-top:1px solid var(--line);margin:1.1rem 0}
</style>
</head>
<body><main>
<div class="topbar"><div><span class="pill">Owner-only development · theory-blind</span><h1>Discover Your Unique Life Patterns</h1></div><div id="sessionState" class="count">Starting…</div></div>
<p class="lede">Use your own real situations. The interviewer first checks what actually happened, then—only after more than one reviewed example—may ask whether those examples suggest a broader pattern. You decide what, if anything, describes you.</p>
<div class="card soft"><strong>Private development boundary</strong><p class="note">This run is for you only. The server keeps narratives in memory for this process and does not write them to Git. No birth data, chart information, or target-model predictions enter this interview.</p></div>

<div id="configWarning" class="card hidden"><strong>AI runtime is not configured.</strong><p class="note">The browser surface is ready, but the local runtime needs an OpenAI-compatible API key in <code>HDMATCH_LLM_API_KEY</code> or <code>OPENAI_API_KEY</code> before it can extract facts or propose a pattern.</p></div>

<div id="conversation" class="chat"></div>

<div id="episodePanel" class="card">
<div class="smallcaps">Add a real example</div>
<h2>Tell me about one specific situation</h2>
<p class="note">Use an actual event rather than a general description of yourself. What happened? What did you do, think, notice, decide, or avoid? A few sentences is enough.</p>
<textarea id="episodeText" placeholder="Example: Last week I had to decide whether to... I first... then... what mattered was..."></textarea>
<div class="row"><button id="analyzeEpisode">Reflect this example back to me</button></div>
<p id="episodeStatus" class="note"></p>
</div>

<div id="factPanel" class="card hidden">
<div class="smallcaps">Check the example</div>
<h2>Here’s what I think happened</h2>
<p class="note">Correct anything that adds meaning you did not give. These are episode facts, not claims about your personality.</p>
<div id="facts"></div>
<div class="row"><button id="saveFacts">Save my review</button></div>
<p id="factStatus" class="note"></p>
</div>

<div id="betweenPanel" class="card hidden">
<h2>Example saved</h2>
<p id="betweenText"></p>
<div class="row"><button id="anotherEpisode">Add another real example</button><button id="lookForPattern" class="secondary hidden">See whether these examples suggest a pattern</button></div>
</div>

<div id="patternPanel" class="hidden">
<div class="chat"><div class="bubble ai"><div class="meta">Interviewer</div><div id="patternQuestion"></div></div></div>
<div class="card">
<p class="note">This is only a hypothesis from the reviewed examples. It is not kept as a pattern unless you endorse it.</p>
<div class="row"><button id="patternAccept">Yes, that fits me</button><button id="patternRevise" class="secondary">Close, but I’d say it differently</button><button id="patternReject" class="danger">No, that’s not a pattern of mine</button><button id="patternUnresolved" class="subtle">I’m not sure</button></div>
<div id="reviseBox" class="hidden">
<hr class="divider"><label for="revisedWording"><strong>How would you say it?</strong></label><textarea id="revisedWording" placeholder="Write the version that actually fits you…"></textarea>
<p><strong>What supports this revised wording?</strong></p>
<p class="note">This keeps two questions separate: whether the wording feels true of you, and whether these particular examples actually show it.</p>
<div class="row"><button class="secondary grounding" data-grounding="examples">These examples show it</button><button class="secondary grounding" data-grounding="other_situations">I know it from other situations</button><button class="subtle grounding" data-grounding="unsure">I’m not sure</button></div>
<div id="finalChoice" class="hidden"><p><strong>Given that, what should we do with the revised pattern?</strong></p><div class="row"><button class="final" data-final="accept">Keep it</button><button class="danger final" data-final="reject">Reject it</button><button class="subtle final" data-final="unresolved">Leave it open</button></div></div>
</div>
<p id="patternStatus" class="note"></p>
</div>
</div>

<div id="resultPanel" class="hidden result"></div>
<div id="postResult" class="hidden row"><button id="addAfterResult" class="secondary">Add another real example</button></div>

<script>
let sessionId=null;let currentEpisodeId=null;let currentFacts=[];let reviewedEpisodes=0;let groundingChoice=null;
const $=id=>document.getElementById(id);
function show(id){$(id).classList.remove('hidden')}function hide(id){$(id).classList.add('hidden')}
function status(id,text,error=false){const el=$(id);el.textContent=text;el.className=error?'error':'note'}
function escapeHtml(s){return String(s).replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]))}
async function api(path,options={}){const r=await fetch(path,{headers:{'content-type':'application/json',...(options.headers||{})},...options});let p={};try{p=await r.json()}catch{}if(!r.ok)throw new Error(p.detail||'Request failed');return p}
function addBubble(role,text){const wrap=document.createElement('div');wrap.className='bubble '+role;wrap.innerHTML='<div class="meta">'+(role==='user'?'You':'Interviewer')+'</div><div>'+escapeHtml(text)+'</div>';$('conversation').append(wrap);wrap.scrollIntoView({behavior:'smooth',block:'end'})}
async function start(){try{const p=await api('/api/owner-v2/sessions',{method:'POST'});sessionId=p.session_id;$('sessionState').textContent='Private runtime session · 0 reviewed examples';if(!p.model_configured)show('configWarning');addBubble('ai','Start with one concrete situation from your life. I’ll first reflect back only what the example supports.')}catch(e){$('sessionState').textContent='Could not start';status('episodeStatus',e.message,true)}}
$('analyzeEpisode').onclick=async()=>{const text=$('episodeText').value.trim();if(!text||!sessionId)return;addBubble('user',text);$('analyzeEpisode').disabled=true;status('episodeStatus','Reading the example…');try{const p=await api(`/api/owner-v2/sessions/${encodeURIComponent(sessionId)}/episodes`,{method:'POST',body:JSON.stringify({text})});currentEpisodeId=p.episode_id;currentFacts=p.proposed_facts;renderFacts(p.neutral_summary,p.proposed_facts);hide('episodePanel');show('factPanel');$('factPanel').scrollIntoView({behavior:'smooth'})}catch(e){status('episodeStatus',e.message,true)}finally{$('analyzeEpisode').disabled=false}}
function renderFacts(summary,facts){$('facts').textContent='';addBubble('ai','Here is my neutral summary of that example: '+summary);for(const fact of facts){const box=document.createElement('div');box.className='fact';box.dataset.factId=fact.fact_id;box.dataset.action='accept';box.innerHTML='<p><strong>'+escapeHtml(fact.proposition)+'</strong></p><div class="row"><button type="button" class="keep">Yes, that is supported</button><button type="button" class="secondary editBtn">Not quite — edit it</button><button type="button" class="danger drop">That is not supported</button></div><div class="edit hidden"><textarea></textarea><div class="row"><button type="button" class="saveEdit">Use this wording</button></div></div><p class="note decision">Currently: keep</p>';$('facts').append(box);wireFact(box)}}
function wireFact(box){box.querySelector('.keep').onclick=()=>{box.dataset.action='accept';box.querySelector('.decision').textContent='Currently: keep';box.querySelector('.edit').classList.add('hidden')};box.querySelector('.drop').onclick=()=>{box.dataset.action='not_supported';box.querySelector('.decision').textContent='Currently: do not use this fact';box.querySelector('.edit').classList.add('hidden')};box.querySelector('.editBtn').onclick=()=>{box.querySelector('.edit').classList.remove('hidden');box.querySelector('textarea').focus()};box.querySelector('.saveEdit').onclick=()=>{const v=box.querySelector('textarea').value.trim();if(!v)return;box.dataset.action='correct';box.dataset.corrected=v;box.querySelector('.decision').textContent='Currently: use your correction — “'+v+'”';box.querySelector('.edit').classList.add('hidden')}}
$('saveFacts').onclick=async()=>{if(!currentEpisodeId)return;const reviews=[...document.querySelectorAll('.fact')].map(box=>({fact_id:box.dataset.factId,action:box.dataset.action,corrected_proposition:box.dataset.action==='correct'?box.dataset.corrected:null}));$('saveFacts').disabled=true;status('factStatus','Saving your review…');try{const p=await api(`/api/owner-v2/sessions/${encodeURIComponent(sessionId)}/episodes/${encodeURIComponent(currentEpisodeId)}/review`,{method:'POST',body:JSON.stringify({reviews})});reviewedEpisodes=p.reviewed_episode_count;$('sessionState').textContent='Private runtime session · '+reviewedEpisodes+' reviewed example'+(reviewedEpisodes===1?'':'s');hide('factPanel');show('betweenPanel');$('betweenText').textContent=p.episode_saved?'This example is now available as reviewed evidence.':'None of the proposed facts were supported, so this example was not used as evidence.';if(p.can_look_for_pattern)show('lookForPattern');$('betweenPanel').scrollIntoView({behavior:'smooth'})}catch(e){status('factStatus',e.message,true)}finally{$('saveFacts').disabled=false}}
function resetEpisode(){currentEpisodeId=null;currentFacts=[];$('episodeText').value='';hide('betweenPanel');hide('patternPanel');hide('resultPanel');hide('postResult');show('episodePanel');$('episodePanel').scrollIntoView({behavior:'smooth'})}
$('anotherEpisode').onclick=resetEpisode;$('addAfterResult').onclick=resetEpisode;
$('lookForPattern').onclick=async()=>{$('lookForPattern').disabled=true;try{const p=await api(`/api/owner-v2/sessions/${encodeURIComponent(sessionId)}/patterns/propose`,{method:'POST'});if(!p.has_candidate){addBubble('ai','I do not see a defensible cross-example pattern yet. That is useful too; add another example rather than forcing one.');resetEpisode();return}$('patternQuestion').textContent=p.question_text;hide('betweenPanel');show('patternPanel');$('patternPanel').scrollIntoView({behavior:'smooth'})}catch(e){status('patternStatus',e.message,true)}finally{$('lookForPattern').disabled=false}}
async function simpleDecision(decision){try{const p=await api(`/api/owner-v2/sessions/${encodeURIComponent(sessionId)}/patterns/adjudicate`,{method:'POST',body:JSON.stringify({decision})});renderResult(p)}catch(e){status('patternStatus',e.message,true)}}
$('patternAccept').onclick=()=>simpleDecision('accept');$('patternReject').onclick=()=>simpleDecision('reject');$('patternUnresolved').onclick=()=>simpleDecision('unresolved');$('patternRevise').onclick=()=>show('reviseBox');
document.querySelectorAll('.grounding').forEach(btn=>btn.onclick=()=>{groundingChoice=btn.dataset.grounding;document.querySelectorAll('.grounding').forEach(b=>b.disabled=true);if(groundingChoice==='examples'){show('finalChoice')}else{submitRevision(null)}})
document.querySelectorAll('.final').forEach(btn=>btn.onclick=()=>submitRevision(btn.dataset.final))
async function submitRevision(finalDecision){const wording=$('revisedWording').value.trim();if(!wording){status('patternStatus','Write the wording that fits you first.',true);return}try{const body={decision:'revise',revised_wording:wording,grounding_source:groundingChoice,final_decision:finalDecision};const p=await api(`/api/owner-v2/sessions/${encodeURIComponent(sessionId)}/patterns/adjudicate`,{method:'POST',body:JSON.stringify(body)});renderResult(p)}catch(e){status('patternStatus',e.message,true)}}
function renderResult(p){hide('patternPanel');const box=$('resultPanel');let title=p.status==='accepted'?'Pattern kept':p.status==='rejected'?'Pattern rejected':'Pattern left open';let body='';if(p.wording)body+='<p><strong>'+escapeHtml(p.wording)+'</strong></p>';if(p.message)body+='<p>'+escapeHtml(p.message)+'</p>';if(p.needs_more_evidence)body+='<p class="note">This preserves your wording as something worth testing without pretending the current examples already establish it.</p>';else body+='<p class="note">The result passed through the participant-adjudicated v2 record validation path.</p>';box.innerHTML='<div class="smallcaps">Current result</div><h2>'+title+'</h2>'+body;show('resultPanel');show('postResult');box.scrollIntoView({behavior:'smooth'})}
start();
</script>
</main></body></html>'''
