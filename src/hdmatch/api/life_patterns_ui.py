# ruff: noqa: E501
"""Participant-facing UI for the text-first Discover Your Unique Life Patterns MVP."""

HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Discover Your Unique Life Patterns</title>
  <style>
    :root { color-scheme:light; --ink:#1f2933; --muted:#52606d; --line:#cbd2d9; --soft:#f5f7fa; --accent:#315c58; --accent2:#e7f1ef; --danger:#a61b1b; }
    * { box-sizing:border-box; }
    body { margin:0; background:#fff; color:var(--ink); font:16px/1.55 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
    main { width:min(54rem,calc(100% - 2rem)); margin:2rem auto 5rem; }
    h1 { margin:.2rem 0 .6rem; font-size:clamp(2.2rem,7vw,4rem); line-height:1.02; letter-spacing:-.045em; }
    h2 { margin:1.7rem 0 .5rem; }
    h3 { margin:1.25rem 0 .35rem; }
    p { margin:.55rem 0; }
    .eyebrow { color:var(--accent); font-weight:800; text-transform:uppercase; letter-spacing:.08em; font-size:.78rem; }
    .lede { color:var(--muted); font-size:1.12rem; max-width:47rem; }
    .card { border:1px solid var(--line); border-radius:.9rem; padding:1rem 1.1rem; margin:1rem 0; background:#fff; }
    .soft { background:var(--soft); }
    .success { background:var(--accent2); border-color:#9fc0ba; }
    .error { color:var(--danger); border-color:#e8a1a1; background:#fff5f5; }
    label { display:block; margin:.9rem 0 .3rem; font-weight:750; }
    input,select,textarea,button { width:100%; padding:.72rem .8rem; border:1px solid #9aa5b1; border-radius:.5rem; font:inherit; background:#fff; color:inherit; }
    textarea { min-height:9rem; resize:vertical; }
    button { cursor:pointer; border-color:var(--accent); background:var(--accent); color:#fff; font-weight:800; margin-top:.75rem; }
    button.secondary { background:#fff; color:var(--accent); }
    button:disabled { opacity:.55; cursor:not-allowed; }
    .row { display:grid; grid-template-columns:1fr 1fr; gap:.75rem; }
    .actions { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.7rem; }
    .hidden { display:none !important; }
    .note { color:var(--muted); font-size:.92rem; }
    code { display:block; padding:.7rem; border:1px solid var(--line); border-radius:.45rem; background:#fff; overflow-wrap:anywhere; user-select:all; }
    .progress-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.6rem; margin-top:.8rem; }
    .progress-item { border:1px solid var(--line); border-radius:.6rem; padding:.65rem .75rem; }
    .progress-item strong { display:block; }
    .tag { display:inline-block; margin-top:.2rem; padding:.12rem .45rem; border-radius:999px; background:var(--soft); font-size:.82rem; }
    .episode { border-top:1px solid var(--line); padding:.75rem 0; }
    .episode:first-child { border-top:0; }
    .pattern { border-left:4px solid var(--accent); padding:.5rem .8rem; margin:.75rem 0; background:var(--soft); }
    .map-meta { color:var(--muted); font-size:.88rem; }
    @media(max-width:42rem){ .row,.actions,.progress-grid{grid-template-columns:1fr;} main{margin-top:1rem;} }
  </style>
</head>
<body>
<main>
  <p class="eyebrow">Private long-form interview · text-first MVP</p>
  <h1>Discover Your Unique Life Patterns</h1>
  <p class="lede">A deep conversation about how you actually make decisions, work, relate, adapt and change across your life. This is not a personality quiz: differences, exceptions and contradictions are useful.</p>

  <div class="card soft">
    <strong>This first MVP is intentionally independent of astrology and Human Design.</strong>
    <p>Your stories are saved as behavioral evidence only. Birth-derived models are not available to the interviewer or the Life Patterns Map generator.</p>
    <p class="note">Voice, email recovery and the full conversational interviewer are next. This slice proves the standalone value first.</p>
  </div>

  <section id="startPanel" class="card">
    <h2>Start or resume</h2>
    <p>Your progress is saved after every episode. You can pause at any time.</p>
    <label><input id="consent" type="checkbox"> I consent to private storage of the life-history material I choose to enter.</label>
    <button id="createSession">Start my Life Patterns interview</button>
    <hr>
    <p class="note">Already started? Paste your recovery details below.</p>
    <label for="resumeId">Session ID</label><input id="resumeId" autocomplete="off">
    <label for="resumeToken">Private resume token</label><input id="resumeToken" type="password" autocomplete="off">
    <button id="resumeSession" class="secondary">Resume</button>
  </section>

  <section id="sessionPanel" class="hidden">
    <div class="card success">
      <strong>Your interview is autosaved.</strong>
      <p id="savedStatus">Saved.</p>
      <div class="actions"><button id="downloadRecovery" class="secondary">Download recovery file</button><button id="pauseNow" class="secondary">Pause for now</button></div>
      <p class="note">The browser also remembers this session locally. Keep the recovery file somewhere private until email recovery is added.</p>
    </div>

    <div class="card">
      <h2>Evidence coverage</h2>
      <p class="note">This is guidance, not a required-question count. A small number of rich, contrasting stories can be more useful than many shallow answers.</p>
      <div id="progressGrid" class="progress-grid"></div>
    </div>

    <div class="card">
      <h2>Add a real episode</h2>
      <p>Choose something that actually happened. Tell the story rather than trying to describe what “type of person” you are.</p>
      <div class="row">
        <div><label for="domain">Area</label><select id="domain"></select></div>
        <div><label for="title">Short title</label><input id="title" maxlength="160" placeholder="Starting my last business"></div>
      </div>
      <label for="narrative">What happened?</label>
      <textarea id="narrative" maxlength="20000" placeholder="Start when this became a real possibility and walk through what happened before you knew the outcome..."></textarea>
      <label for="counterexample">Exception or contrasting example (optional)</label>
      <textarea id="counterexample" maxlength="12000" placeholder="If this story makes you sound more consistent than you really are, tell us what it misses."></textarea>
      <button id="saveEpisode">Save this episode</button>
    </div>

    <div class="card">
      <h2>Your saved episodes</h2>
      <div id="episodeList"></div>
    </div>

    <div class="card">
      <h2>Your Life Patterns Map</h2>
      <p>This map is generated only from the episodes you supplied. It should preserve context differences and counterexamples rather than forcing one personality story.</p>
      <button id="generateMap">Generate / refresh my Life Patterns Map</button>
      <div id="mapPanel"></div>
      <div id="exportActions" class="actions hidden"><button id="downloadJson" class="secondary">Download JSON</button><button id="downloadMarkdown" class="secondary">Download coaching-context Markdown</button></div>
    </div>
  </section>

  <div id="message" class="card hidden" role="status" aria-live="polite"></div>
</main>
<script>
const areas={
  decisions:'Major decisions', work_projects:'Work & projects', relationships:'Relationships',
  self_initiated_actions:'Self-initiated actions', learning_adaptation:'Learning & adaptation',
  conflict_stress:'Conflict & stress', life_transitions:'Life phases & transitions', other:'Something else'
};
let sessionId=null, token=null, current=null;
const $=id=>document.getElementById(id);
Object.entries(areas).forEach(([value,label])=>{const o=document.createElement('option');o.value=value;o.textContent=label;$('domain').append(o)});
function showMessage(text,error=false){const box=$('message');box.classList.remove('hidden','error');if(error)box.classList.add('error');box.textContent=text}
function clearMessage(){$('message').classList.add('hidden');$('message').classList.remove('error')}
async function api(path,options={}){const r=await fetch(path,{...options,headers:{'content-type':'application/json',...(options.headers||{})}});let body={};try{body=await r.json()}catch{}if(!r.ok)throw new Error(body.detail||body.error||'Request failed');return body}
function remember(){localStorage.setItem('lifePatternsSession',JSON.stringify({session_id:sessionId,token}))}
function forget(){localStorage.removeItem('lifePatternsSession')}
function recoveryBlob(){return new Blob([JSON.stringify({product:'Discover Your Unique Life Patterns',session_id:sessionId,resume_token:token},null,2)+'\n'],{type:'application/json'})}
function download(blob,name){const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;document.body.append(a);a.click();URL.revokeObjectURL(a.href);a.remove()}
function renderProgress(progress){const grid=$('progressGrid');grid.textContent='';progress.areas.forEach(row=>{const d=document.createElement('div');d.className='progress-item';const strong=document.createElement('strong');strong.textContent=row.label;const tag=document.createElement('span');tag.className='tag';tag.textContent=row.status.replaceAll('_',' ');const small=document.createElement('div');small.className='note';small.textContent=row.episode_count+' saved episode'+(row.episode_count===1?'':'s');d.append(strong,tag,small);grid.append(d)})}
function renderEpisodes(episodes){const list=$('episodeList');list.textContent='';if(!episodes.length){list.innerHTML='<p class="note">No episodes saved yet.</p>';return}episodes.forEach(ep=>{const d=document.createElement('div');d.className='episode';const h=document.createElement('strong');h.textContent=ep.title;const meta=document.createElement('div');meta.className='note';meta.textContent=areas[ep.domain]+' · '+new Date(ep.created_at_utc).toLocaleString();const p=document.createElement('p');p.textContent=ep.narrative;d.append(h,meta,p);if(ep.counterexample){const c=document.createElement('p');c.className='note';c.textContent='Contrast: '+ep.counterexample;d.append(c)}list.append(d)})}
function renderMap(map){const panel=$('mapPanel');panel.textContent='';if(!map){$('exportActions').classList.add('hidden');return}const intro=document.createElement('p');intro.textContent=map.overall_summary;panel.append(intro);map.patterns.forEach(pattern=>{const d=document.createElement('div');d.className='pattern';const h=document.createElement('strong');h.textContent=pattern.title;const p=document.createElement('p');p.textContent=pattern.summary;const m=document.createElement('div');m.className='map-meta';m.textContent=pattern.status.replaceAll('_',' ')+' · confidence '+Math.round(pattern.confidence*100)+'% · evidence: '+pattern.supporting_episode_ids.join(', ');d.append(h,p,m);panel.append(d)});if(map.transfer_opportunities.length){const h=document.createElement('h3');h.textContent='Patterns you might be able to transfer';panel.append(h);map.transfer_opportunities.forEach(item=>{const p=document.createElement('p');p.textContent=item;panel.append(p)})}if(map.reversible_experiments.length){const h=document.createElement('h3');h.textContent='Small experiments worth considering';panel.append(h);map.reversible_experiments.forEach(item=>{const p=document.createElement('p');p.textContent=item;panel.append(p)})}$('exportActions').classList.remove('hidden')}
async function loadSession(){clearMessage();current=await api('/api/life-patterns/sessions/'+encodeURIComponent(sessionId)+'?token='+encodeURIComponent(token));$('startPanel').classList.add('hidden');$('sessionPanel').classList.remove('hidden');renderProgress(current.progress);renderEpisodes(current.episodes);renderMap(current.life_patterns_map);$('savedStatus').textContent='Saved '+new Date(current.updated_at).toLocaleString()}
$('createSession').onclick=async()=>{try{if(!$('consent').checked)throw new Error('Please confirm private-storage consent first.');const data=await api('/api/life-patterns/sessions',{method:'POST',body:JSON.stringify({consent_to_store_responses:true})});sessionId=data.session_id;token=data.resume_token;remember();await loadSession();showMessage('Session created. Download the recovery file before leaving this device.')}catch(e){showMessage(e.message,true)}};
$('resumeSession').onclick=async()=>{try{sessionId=$('resumeId').value.trim();token=$('resumeToken').value.trim();if(!sessionId||!token)throw new Error('Enter both recovery values.');remember();await loadSession()}catch(e){showMessage(e.message,true)}};
$('downloadRecovery').onclick=()=>download(recoveryBlob(),'life-patterns-recovery.json');
$('pauseNow').onclick=()=>{showMessage('Everything saved. You can close this page and resume later.');window.scrollTo({top:0,behavior:'smooth'})};
$('saveEpisode').onclick=async()=>{try{const title=$('title').value.trim(),narrative=$('narrative').value.trim();if(!title||!narrative)throw new Error('Add a short title and the episode story.');$('savedStatus').textContent='Saving…';await api('/api/life-patterns/sessions/'+encodeURIComponent(sessionId)+'/episodes',{method:'POST',body:JSON.stringify({token,domain:$('domain').value,title,narrative,counterexample:$('counterexample').value.trim()||null,input_modality:'typed'})});$('title').value='';$('narrative').value='';$('counterexample').value='';await loadSession();showMessage('Episode saved. Specific differences and counterexamples are especially useful.')}catch(e){showMessage(e.message,true)}};
$('generateMap').onclick=async()=>{try{$('generateMap').disabled=true;$('generateMap').textContent='Building your map…';const result=await api('/api/life-patterns/sessions/'+encodeURIComponent(sessionId)+'/map',{method:'POST',body:JSON.stringify({token})});await loadSession();renderMap(result.life_patterns_map);showMessage('Life Patterns Map refreshed from your saved evidence.')}catch(e){showMessage(e.message,true)}finally{$('generateMap').disabled=false;$('generateMap').textContent='Generate / refresh my Life Patterns Map'}};
$('downloadJson').onclick=async()=>{try{const data=await api('/api/life-patterns/sessions/'+encodeURIComponent(sessionId)+'/export?token='+encodeURIComponent(token));download(new Blob([JSON.stringify(data.profile_json,null,2)+'\n'],{type:'application/json'}),'life-patterns-profile.json')}catch(e){showMessage(e.message,true)}};
$('downloadMarkdown').onclick=async()=>{try{const data=await api('/api/life-patterns/sessions/'+encodeURIComponent(sessionId)+'/export?token='+encodeURIComponent(token));download(new Blob([data.coaching_markdown+'\n'],{type:'text/markdown'}),'life-patterns-coaching-context.md')}catch(e){showMessage(e.message,true)}};
try{const remembered=JSON.parse(localStorage.getItem('lifePatternsSession')||'null');if(remembered&&remembered.session_id&&remembered.token){sessionId=remembered.session_id;token=remembered.token;loadSession().catch(()=>forget())}}catch{forget()}
</script>
</body>
</html>
"""
