"""Participant-facing audit/recovery, import, progress-label, and scrolling overlay."""

from __future__ import annotations

from .life_patterns_v2_owner_resilient_ui import RESILIENT_RECOVERABILITY_HTML


def _build_persistent_html() -> str:
    html = RESILIENT_RECOVERABILITY_HTML

    # Always expose a vertical scrollbar and leave enough scroll padding for the sticky
    # composer. The prior bubble-level scrollIntoView could strand the actual next action
    # below the viewport, especially at interview start.
    css = """
html{overflow-y:scroll;scroll-behavior:smooth;scroll-padding-bottom:12rem}
body{min-height:100vh}
#composer,#patternPanel,#continuation{scroll-margin-bottom:2rem}
""".strip()
    if "</style>" not in html:
        raise RuntimeError("persistent UI style insertion point not found")
    html = html.replace("</style>", css + "\n</style>", 1)

    # The number is a count of still-open measurement areas, not a literal number of
    # questions. One natural answer may close several areas at once.
    html = html.replace(
        "return m.remaining?`Interview progress: about ${m.pct}% through required coverage. Roughly ${m.lowQ}–${m.highQ} substantive questions remain.`:`Interview coverage is complete.`;",
        "return m.remaining?`Interview progress: about ${m.pct}% through required coverage. ${incompleteCoverage().length} measurement areas are still open.`:`Interview coverage is complete.`;",
        1,
    )
    html = html.replace(
        "text.textContent=`≈${m.pct}% · roughly ${m.lowQ}–${m.highQ} questions left`;",
        "text.textContent=`≈${m.pct}% · ${incompleteCoverage().length} measurement areas still open`;",
        1,
    )
    html = html.replace(
        "note.textContent=`Very rough time estimate: about ${m.lowMin}–${m.highMin} minutes, depending on answer length. One answer can cover several areas, so this can shrink faster than a fixed questionnaire.`;",
        "note.textContent=`These are measurement areas, not a question count. One answer can cover several. Very rough remaining time: about ${m.lowMin}–${m.highMin} minutes, depending on answer length.`;",
        1,
    )

    # Preserve the exact *working* ledger as a browser-local audit/recovery checkpoint.
    # This is intentionally not called a valid/final ledger: exactness means the state
    # can be audited and resumed without loss, not that its extraction or semantics are correct.
    old_button = (
        '<button id="downloadLocalRecovery" type="button" class="subtle" style="margin-top:.55rem">'
        'Download local recovery copy</button>'
    )
    new_buttons = (
        '<button id="downloadLocalRecovery" type="button" class="subtle" style="margin-top:.55rem">'
        'Download audit/recovery snapshot</button>\n'
        '  <button id="importRecovery" type="button" class="subtle" style="margin-top:.55rem">'
        'Import audit/recovery snapshot</button>\n'
        '  <input id="importRecoveryFile" type="file" accept="application/json,.json" class="hidden">'
    )
    if old_button not in html:
        raise RuntimeError("exact recovery controls insertion point not found")
    html = html.replace(old_button, new_buttons, 1)
    html = html.replace(
        " Browser-local transcript backup only; not the scientific freeze.",
        " The browser automatically checkpoints the current working hidden ledger so bugs can be audited and a crash does not erase evidence. A checkpoint may itself contain ledger mistakes; it is not accepted/canonical data and is not the scientific freeze.",
        1,
    )

    # Scrolling should follow the next interactive surface, not merely the most recently
    # appended bubble. This also makes the opening textarea visible without requiring a
    # manual mouse-wheel nudge.
    html = html.replace(
        "el.scrollIntoView({behavior:'smooth',block:'end'})",
        "scrollToNextAction()",
    )
    html = html.replace(
        "$('patternPanel').scrollIntoView({behavior:'smooth'});",
        "scrollToNextAction();",
    )

    # A transcript-only legacy recovery must never be exported as the clean scientific
    # freeze. Exact hidden-ledger recovery is still only an unvalidated working checkpoint;
    # scientific acceptance happens through the later participant/semantic freeze path.
    freeze_marker = "$('freezeMeasurement').onclick=async()=>{"
    freeze_guard = (
        "$('freezeMeasurement').onclick=async()=>{"
        "if(window.__lifePatternsTranscriptOnlyRecovery){"
        "$('sessionSummary').textContent='This imported file restored only the visible transcript; its original hidden ledger was never saved. Use it for development continuity, not as the clean scientific measurement freeze.';"
        "$('sessionSummary').className='error';show('sessionSummary');return}"
    )
    if freeze_marker not in html:
        raise RuntimeError("scientific-freeze recovery guard insertion point not found")
    html = html.replace(freeze_marker, freeze_guard, 1)

    start_marker = "\nstart();"
    if start_marker not in html:
        raise RuntimeError("persistent recovery startup insertion point not found")

    recovery_js = r'''
const EXACT_RECOVERY_KEY='lifePatternsExactRecoveryV2';
let __exactRecoveryTimer=null;

function scrollToNextAction(){
  requestAnimationFrame(()=>requestAnimationFrame(()=>{
    let target=null;
    if($('patternPanel')&&!$('patternPanel').classList.contains('hidden'))target=$('patternPanel');
    else if($('composer')&&!$('composer').classList.contains('hidden'))target=$('composer');
    else if($('continuation')&&!$('continuation').classList.contains('hidden'))target=$('continuation');
    else target=$('conversation')&&$('conversation').lastElementChild;
    if(target)target.scrollIntoView({behavior:'smooth',block:'end'});
    else window.scrollTo({top:document.documentElement.scrollHeight,behavior:'smooth'});
  }));
}

function currentClientRecoveryState(){
  return {
    completed_results:completedResults,
    aggregate_coverage:coverageAggregate,
    transcript_only:Boolean(window.__lifePatternsTranscriptOnlyRecovery)
  };
}

async function syncExactRecovery(){
  if(!sessionId)return null;
  try{
    const r=await fetch(`/api/owner-v2/conversation/sessions/${encodeURIComponent(sessionId)}/recovery`);
    if(!r.ok)return null;
    const serverSnapshot=await r.json();
    const bundle={
      schema:'life-patterns-browser-recovery-v2',
      saved_at:new Date().toISOString(),
      recovery_only:true,
      audit_checkpoint:true,
      unvalidated_working_state:true,
      canonical_measurement:false,
      not_scientific_freeze:true,
      server_snapshot:serverSnapshot,
      client_state:currentClientRecoveryState()
    };
    localStorage.setItem(EXACT_RECOVERY_KEY,JSON.stringify(bundle));
    return bundle;
  }catch(_e){return null}
}

function scheduleExactRecovery(){
  clearTimeout(__exactRecoveryTimer);
  __exactRecoveryTimer=setTimeout(()=>{syncExactRecovery()},180);
}

function resetVisibleInterview(){
  $('conversation').innerHTML='';
  hide('patternPanel');hide('result');hide('continuation');show('composer');
  $('patternStatus').textContent='';$('patternStatus').className='note';
  $('message').value='';
}

function restoreClientState(bundle){
  const state=(bundle&&bundle.client_state)||{};
  completedResults=Array.isArray(state.completed_results)?state.completed_results:[];
  coverageAggregate=(state.aggregate_coverage&&typeof state.aggregate_coverage==='object')?state.aggregate_coverage:{};
  window.__lifePatternsTranscriptOnlyRecovery=Boolean(state.transcript_only);
  renderCoverageStatus();
}

function renderRecoveredConversation(rows){
  $('conversation').innerHTML='';
  for(const row of rows||[]){
    if(!row||!row.text)continue;
    const role=row.role==='user'?'user':'ai';
    bubble(role,row.text);
  }
}

async function restoreExactBundle(bundle){
  const snapshot=bundle&&bundle.server_snapshot?bundle.server_snapshot:bundle;
  const r=await fetch('/api/owner-v2/conversation/sessions/restore',{
    method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({snapshot})
  });
  let p={};try{p=await r.json()}catch{}
  if(!r.ok)throw new Error(p.detail||'Could not restore hidden-ledger audit/recovery snapshot.');
  sessionId=p.session_id;
  resetVisibleInterview();
  restoreClientState(bundle&&bundle.server_snapshot?bundle:{client_state:{}});
  window.__lifePatternsTranscriptOnlyRecovery=p.recovery_quality==='visible_transcript_only';
  renderRecoveredConversation(p.conversation||snapshot.conversation||[]);
  if(p.coverage){mergeCoverage(p.coverage);renderCoverageStatus()}
  if(p.pattern_active){show('patternPanel');show('composer')}
  $('sessionState').textContent=p.exact_hidden_ledger_restored?'Recovered working ledger snapshot · unvalidated':'Recovered transcript-only session';
  $('sessionSummary').textContent=p.exact_hidden_ledger_restored?'Recovered the exact working hidden ledger and conversation. This preserves the state for continuation/audit but does not certify that the ledger is correct.':'Recovered visible transcript context only; the old hidden ledger was not present in this file.';
  $('sessionSummary').className=p.exact_hidden_ledger_restored?'note':'error';show('sessionSummary');
  scheduleExactRecovery();scrollToNextAction();
  return p;
}

async function restoreVisibleBundle(payload){
  const turns=Array.isArray(payload.turns)?payload.turns:[];
  const r=await fetch('/api/owner-v2/conversation/sessions/restore-visible',{
    method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({turns})
  });
  let p={};try{p=await r.json()}catch{}
  if(!r.ok)throw new Error(p.detail||'Could not import visible recovery transcript.');
  sessionId=p.session_id;
  resetVisibleInterview();
  completedResults=[];coverageAggregate={};
  window.__lifePatternsTranscriptOnlyRecovery=true;
  renderRecoveredConversation(p.conversation||turns);
  $('sessionState').textContent='Recovered visible transcript · hidden ledger unavailable';
  $('sessionSummary').textContent='Imported the saved visible transcript. Because that older file never contained the server hidden ledger, this is development continuity only; future sessions preserve the exact working ledger as an audit/recovery checkpoint.';
  $('sessionSummary').className='error';show('sessionSummary');
  scheduleExactRecovery();scrollToNextAction();
}

async function importRecoveryPayload(payload){
  if(!payload||typeof payload!=='object')throw new Error('That file is not a valid recovery JSON object.');
  if(payload.schema==='life-patterns-browser-recovery-v2')return restoreExactBundle(payload);
  if(payload.schema==='life-patterns-hidden-ledger-session-v2')return restoreExactBundle(payload);
  if(payload.schema==='life-patterns-visible-recovery-v1'||payload.schema==='life-patterns-local-recovery-v1')return restoreVisibleBundle(payload);
  throw new Error('Unrecognized Life Patterns recovery JSON format.');
}

$('downloadLocalRecovery').textContent='Download audit/recovery snapshot';
$('downloadLocalRecovery').onclick=async()=>{
  let bundle=await syncExactRecovery();
  if(!bundle){try{bundle=JSON.parse(localStorage.getItem(EXACT_RECOVERY_KEY)||'null')}catch(_e){bundle=null}}
  if(!bundle){$('sessionSummary').textContent='No exact working-ledger audit snapshot is available yet.';$('sessionSummary').className='error';show('sessionSummary');return}
  const blob=new Blob([JSON.stringify(bundle,null,2)+'\n'],{type:'application/json'});
  const url=URL.createObjectURL(blob);const a=document.createElement('a');
  a.href=url;a.download=`life-patterns-audit-recovery-${String(sessionId||'session').slice(-12)}.json`;
  document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(url);
  $('sessionSummary').textContent='Audit/recovery snapshot downloaded. It preserves the current working hidden ledger plus visible conversation for inspection or crash recovery; it does not certify the ledger as correct.';
  $('sessionSummary').className='note';show('sessionSummary');
};

$('importRecovery').textContent='Import audit/recovery snapshot';
$('importRecovery').onclick=()=>$('importRecoveryFile').click();
$('importRecoveryFile').onchange=async()=>{
  const file=$('importRecoveryFile').files&&$('importRecoveryFile').files[0];
  if(!file)return;
  try{
    const payload=JSON.parse(await file.text());
    await importRecoveryPayload(payload);
  }catch(e){$('sessionSummary').textContent='Import failed: '+e.message;$('sessionSummary').className='error';show('sessionSummary')}
  finally{$('importRecoveryFile').value=''}
};

async function resumeOrStart(){
  let saved=null;
  try{saved=JSON.parse(localStorage.getItem(EXACT_RECOVERY_KEY)||'null')}catch(_e){}
  if(saved&&saved.schema==='life-patterns-browser-recovery-v2'&&saved.server_snapshot){
    try{await restoreExactBundle(saved);return}catch(_e){}
  }
  await start();
  scheduleExactRecovery();
  scrollToNextAction();
}

const __recoveryObserver=new MutationObserver(()=>scheduleExactRecovery());
__recoveryObserver.observe(document.body,{childList:true,subtree:true,characterData:true});
window.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden')syncExactRecovery()});
setInterval(()=>{syncExactRecovery()},10000);

resumeOrStart();'''.strip()

    return html.replace(start_marker, "\n" + recovery_js, 1)


PERSISTENT_RECOVERABILITY_HTML = _build_persistent_html()
