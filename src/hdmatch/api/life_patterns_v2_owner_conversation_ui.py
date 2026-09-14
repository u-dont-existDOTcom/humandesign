"""Owner-facing conversational UI for the hidden-ledger Life Patterns v2 probe."""

HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Discover Your Unique Life Patterns — owner conversation</title>
<style>
:root{--ink:#20242a;--muted:#667085;--line:#d0d5dd;--soft:#f7f8fa;--accent:#315c5f;--user:#eef6f6;--ai:#f7f3eb;--good:#176b44;--bad:#a61b1b}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);font:16px/1.55 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
main{width:min(58rem,calc(100% - 2rem));margin:2rem auto 5rem}
h1{font-size:clamp(2rem,7vw,3.4rem);line-height:1.02;letter-spacing:-.04em;margin:.2rem 0 .7rem}
h2{margin:.2rem 0 .65rem}.lede{font-size:1.08rem;color:var(--muted);max-width:50rem}
.card{border:1px solid var(--line);border-radius:1rem;padding:1.05rem;margin:1rem 0;background:#fff}
.soft{background:var(--soft)}.chat{display:grid;gap:.8rem;margin:1.2rem 0}
.bubble{padding:.9rem 1rem;border-radius:.85rem;max-width:94%;white-space:pre-wrap}
.bubble.user{background:var(--user);margin-left:auto}.bubble.ai{background:var(--ai)}
.meta{font-size:.82rem;color:var(--muted);margin-bottom:.25rem}
.pill{display:inline-block;font-size:.82rem;border:1px solid var(--line);border-radius:999px;padding:.25rem .6rem;color:var(--muted)}
textarea,button{font:inherit;border:1px solid #98a2b3;border-radius:.6rem;padding:.72rem .8rem}
textarea{width:100%;min-height:7rem;resize:vertical}
button{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:750;cursor:pointer}
button.secondary{background:#fff;color:var(--accent)}button.subtle{background:#fff;color:var(--ink);border-color:var(--line)}
button.danger{background:#fff;color:var(--bad);border-color:#e5a6a6}button:disabled{opacity:.5;cursor:not-allowed}
.row{display:flex;gap:.65rem;flex-wrap:wrap;align-items:center}.hidden{display:none}
.note{font-size:.92rem;color:var(--muted)}.error{color:var(--bad)}
.result{border-left:4px solid var(--accent);padding:.9rem 1rem;background:#f2f8f8;margin:1rem 0}
.topbar{display:flex;justify-content:space-between;gap:1rem;align-items:center;flex-wrap:wrap}
.count{font-size:.88rem;color:var(--muted)}.divider{border:0;border-top:1px solid var(--line);margin:1.1rem 0}
.composer{position:sticky;bottom:0;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);padding:.8rem 0 .2rem}
</style>
</head>
<body><main>
<div class="topbar">
  <div><span class="pill">Owner-only development · hidden evidence ledger</span><h1>Discover Your Unique Life Patterns</h1></div>
  <div id="sessionState" class="count">Starting…</div>
</div>
<p class="lede">This version is meant to feel like a real conversation. The evidence bookkeeping stays underneath. The interviewer should ask only questions that could change the picture, and should surface a pattern only when it adds something beyond repeating you.</p>
<div class="card soft"><strong>What to judge</strong><p class="note">Does the conversation expose a distinction, contrast, boundary, or cross-situation pattern you did not simply hand it verbatim? If it mostly paraphrases you, this version fails too.</p></div>

<div id="configWarning" class="card hidden"><strong>AI runtime is not configured.</strong><p class="note">The browser surface is ready, but the runtime needs its configured model credential.</p></div>

<div id="conversation" class="chat"></div>

<div id="composer" class="composer">
  <textarea id="message" placeholder="Answer in your own words…"></textarea>
  <div class="row"><button id="send">Send</button><span id="status" class="note"></span></div>
</div>

<div id="patternPanel" class="card hidden">
  <h2>Does that synthesis actually fit?</h2>
  <p class="note">This is the one place where your explicit judgment matters. The hidden episode facts are not being shown for routine approval.</p>
  <div class="row">
    <button id="accept">Yes — keep that</button>
    <button id="revise" class="secondary">Close, but change it</button>
    <button id="reject" class="danger">No</button>
    <button id="unresolved" class="subtle">I’m not sure</button>
  </div>
  <div id="reviseBox" class="hidden">
    <hr class="divider">
    <label for="revisedWording"><strong>What is the version that actually fits?</strong></label>
    <textarea id="revisedWording" placeholder="Say it the way you mean it…"></textarea>
    <p><strong>Do the situations we actually discussed show that revised version?</strong></p>
    <div class="row">
      <button class="secondary grounding" data-grounding="examples">Yes, these situations show it</button>
      <button class="secondary grounding" data-grounding="other_situations">It comes from other situations</button>
      <button class="subtle grounding" data-grounding="unsure">I’m not sure</button>
    </div>
    <div id="finalChoice" class="hidden">
      <p><strong>Then should I keep the revised version, reject it, or leave it open?</strong></p>
      <div class="row">
        <button class="final" data-final="accept">Keep it</button>
        <button class="danger final" data-final="reject">Reject it</button>
        <button class="subtle final" data-final="unresolved">Leave it open</button>
      </div>
    </div>
  </div>
  <p id="patternStatus" class="note"></p>
</div>

<div id="result" class="hidden result"></div>
<div id="continuation" class="hidden card">
  <h2>Where next?</h2>
  <p class="note">You can explore another separate pattern thread, or finish for now. This summary does not claim scientific completeness.</p>
  <div class="row">
    <button id="exploreAnother">Explore another pattern</button>
    <button id="finishForNow" class="secondary">Finish for now</button>
    <button id="copyExport" class="subtle">Copy interview summary</button>
  </div>
  <div id="sessionSummary" class="note hidden"></div>
</div>

<script>
let sessionId=null;let groundingChoice=null;let completedResults=[];
const $=id=>document.getElementById(id);
function show(id){$(id).classList.remove('hidden')}function hide(id){$(id).classList.add('hidden')}
function setStatus(text,error=false){$('status').textContent=text;$('status').className=error?'error':'note'}
function escapeHtml(s){return String(s).replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]))}
function bubble(role,text){const el=document.createElement('div');el.className='bubble '+role;el.innerHTML='<div class="meta">'+(role==='user'?'You':'Interviewer')+'</div><div>'+escapeHtml(text)+'</div>';$('conversation').append(el);el.scrollIntoView({behavior:'smooth',block:'end'})}
async function api(path,options={}){const r=await fetch(path,{headers:{'content-type':'application/json',...(options.headers||{})},...options});let p={};try{p=await r.json()}catch{}if(!r.ok)throw new Error(p.detail||'Request failed');return p}

async function start(){
  try{
    const p=await api('/api/owner-v2/conversation/sessions',{method:'POST'});
    sessionId=p.session_id;
    $('sessionState').textContent='Private conversational probe';
    if(!p.model_configured)show('configWarning');
    bubble('ai',p.opening);
    $('message').focus();
  }catch(e){$('sessionState').textContent='Could not start';setStatus(e.message,true)}
}

async function startFreshPattern(){
  const p=await api('/api/owner-v2/conversation/sessions',{method:'POST'});
  sessionId=p.session_id;groundingChoice=null;
  $('sessionState').textContent='Private conversational probe · new pattern thread';
  hide('result');hide('continuation');hide('patternPanel');show('composer');
  $('message').value='';bubble('ai',p.opening);$('message').focus();
}

$('send').onclick=send;
$('message').addEventListener('keydown',e=>{if(e.key==='Enter'&&(e.ctrlKey||e.metaKey))send()});
async function send(){
  const text=$('message').value.trim();
  if(!text||!sessionId)return;
  bubble('user',text);
  $('message').value='';
  $('send').disabled=true;
  setStatus('Thinking…');
  try{
    const p=await api(`/api/owner-v2/conversation/sessions/${encodeURIComponent(sessionId)}/turns`,{method:'POST',body:JSON.stringify({message:text})});
    bubble('ai',p.reply);
    setStatus('');
    if(p.pattern_active){
      hide('composer');
      show('patternPanel');
      $('patternPanel').scrollIntoView({behavior:'smooth'});
    }
  }catch(e){setStatus(e.message,true)}
  finally{$('send').disabled=false}
}

async function decision(decision){
  try{
    const p=await api(`/api/owner-v2/conversation/sessions/${encodeURIComponent(sessionId)}/patterns/adjudicate`,{method:'POST',body:JSON.stringify({decision})});
    renderResult(p);
  }catch(e){$('patternStatus').textContent=e.message;$('patternStatus').className='error'}
}
$('accept').onclick=()=>decision('accept');
$('reject').onclick=()=>decision('reject');
$('unresolved').onclick=()=>decision('unresolved');
$('revise').onclick=()=>show('reviseBox');

document.querySelectorAll('.grounding').forEach(btn=>btn.onclick=()=>{
  const wording=$('revisedWording').value.trim();
  if(!wording){$('patternStatus').textContent='Write the version that fits first.';$('patternStatus').className='error';return}
  groundingChoice=btn.dataset.grounding;
  document.querySelectorAll('.grounding').forEach(b=>b.disabled=true);
  if(groundingChoice==='examples')show('finalChoice');else submitRevision(null);
});
document.querySelectorAll('.final').forEach(btn=>btn.onclick=()=>submitRevision(btn.dataset.final));

async function submitRevision(finalDecision){
  const wording=$('revisedWording').value.trim();
  if(!wording)return;
  try{
    const p=await api(`/api/owner-v2/conversation/sessions/${encodeURIComponent(sessionId)}/patterns/adjudicate`,{
      method:'POST',
      body:JSON.stringify({decision:'revise',revised_wording:wording,grounding_source:groundingChoice,final_decision:finalDecision})
    });
    renderResult(p);
  }catch(e){$('patternStatus').textContent=e.message;$('patternStatus').className='error'}
}

function renderResult(p){
  hide('patternPanel');
  let title=p.status==='accepted'?'Working pattern kept':p.status==='rejected'?'Pattern rejected':'Pattern left open';
  let body='';
  if(p.wording)body+='<p><strong>'+escapeHtml(p.wording)+'</strong></p>';
  if(p.message)body+='<p>'+escapeHtml(p.message)+'</p>';
  body+='<p class="note">This thread is complete. You can continue with another pattern or finish for now.</p>';
  $('result').innerHTML='<div class="meta">Current result</div><h2>'+title+'</h2>'+body;
  completedResults.push({status:p.status,wording:p.wording||null});
  show('result');
  show('continuation');
  $('result').scrollIntoView({behavior:'smooth'});
}

$('exploreAnother').onclick=async()=>{try{await startFreshPattern()}catch(e){$('sessionSummary').textContent=e.message;$('sessionSummary').className='error'}};
$('finishForNow').onclick=()=>{const summary=completedResults.map((r,i)=>`${i+1}. ${r.status}${r.wording?' — '+r.wording:''}`).join('\n');$('sessionSummary').textContent=summary||'No completed pattern threads yet.';show('sessionSummary')};
$('copyExport').onclick=async()=>{const transcript=[...document.querySelectorAll('#conversation .bubble')].map(el=>el.innerText).join('\n\n');const results=completedResults.map((r,i)=>`${i+1}. ${r.status}${r.wording?' — '+r.wording:''}`).join('\n');const text=`Life Patterns owner interview\n\n${transcript}\n\nCompleted results\n${results}`;try{await navigator.clipboard.writeText(text);$('sessionSummary').textContent='Interview summary copied to your clipboard.'}catch(e){$('sessionSummary').textContent=text}show('sessionSummary')};

start();
</script>
</main></body></html>'''
