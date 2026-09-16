"""UI overlay that makes transcript-only recovery an explicit workflow state."""

from __future__ import annotations

from .life_patterns_v2_owner_persistent_ui import PERSISTENT_RECOVERABILITY_HTML


def _build_import_resume_html() -> str:
    html = PERSISTENT_RECOVERABILITY_HTML

    marker = '<div id="conversation" class="chat"></div>'
    panel = """
<div id="recoveredTranscriptActions" class="card hidden">
  <h2>Recovered transcript</h2>
  <p class="note">This older file restored what you said, but it never contained the original hidden ledger. You do not need to retype the interview. Continue from the recovered answers using a newly reconstructed development ledger, or start a clean scientific interview. The reconstructed route is for development continuity only and cannot become the clean scientific freeze.</p>
  <div class="row">
    <button id="resumeRecoveredTranscript">Continue from this recovered interview</button>
    <button id="startCleanFromRecovery" class="secondary">Start a clean scientific interview</button>
  </div>
  <p id="recoveredTranscriptStatus" class="note"></p>
</div>
""".strip()
    if marker not in html:
        raise RuntimeError("recovered-transcript action insertion point not found")
    html = html.replace(marker, panel + "\n\n" + marker, 1)

    old_scroll = (
        "if($('patternPanel')&&!$('patternPanel').classList.contains('hidden'))target=$('patternPanel');\n"
        "    else if($('composer')&&!$('composer').classList.contains('hidden'))target=$('composer');"
    )
    new_scroll = (
        "if($('patternPanel')&&!$('patternPanel').classList.contains('hidden'))target=$('patternPanel');\n"
        "    else if($('recoveredTranscriptActions')&&!$('recoveredTranscriptActions').classList.contains('hidden'))target=$('recoveredTranscriptActions');\n"
        "    else if($('composer')&&!$('composer').classList.contains('hidden'))target=$('composer');"
    )
    if old_scroll not in html:
        raise RuntimeError("recovered-transcript scroll priority insertion point not found")
    html = html.replace(old_scroll, new_scroll, 1)

    old_quality = "window.__lifePatternsTranscriptOnlyRecovery=p.recovery_quality==='visible_transcript_only';"
    new_quality = "window.__lifePatternsTranscriptOnlyRecovery=p.recovery_quality!=='exact_hidden_ledger';"
    if old_quality not in html:
        raise RuntimeError("recovery-quality UI insertion point not found")
    html = html.replace(old_quality, new_quality, 1)

    old_exact_pattern = "if(p.pattern_active){show('patternPanel');show('composer')}"
    new_exact_pattern = (
        "if(p.pattern_active){show('patternPanel');show('composer')}\n"
        "  if(p.recovery_quality!=='exact_hidden_ledger')showRecoveredTranscriptActions();else hide('recoveredTranscriptActions');"
    )
    if old_exact_pattern not in html:
        raise RuntimeError("exact restore action-state insertion point not found")
    html = html.replace(old_exact_pattern, new_exact_pattern, 1)

    old_visible_state = (
        "renderRecoveredConversation(p.conversation||turns);\n"
        "  $('sessionState').textContent='Recovered visible transcript · hidden ledger unavailable';"
    )
    new_visible_state = (
        "renderRecoveredConversation(p.conversation||turns);\n"
        "  showRecoveredTranscriptActions();\n"
        "  $('sessionState').textContent='Recovered visible transcript · hidden ledger unavailable';"
    )
    if old_visible_state not in html:
        raise RuntimeError("visible restore action-state insertion point not found")
    html = html.replace(old_visible_state, new_visible_state, 1)

    startup = "resumeOrStart();"
    if startup not in html:
        raise RuntimeError("import-resume JS insertion point not found")
    action_js = r'''
function showRecoveredTranscriptActions(){
  show('recoveredTranscriptActions');
  show('composer');
  $('recoveredTranscriptStatus').textContent='';
  scrollToNextAction();
}

$('resumeRecoveredTranscript').onclick=async()=>{
  if(!sessionId)return;
  const btn=$('resumeRecoveredTranscript');btn.disabled=true;
  $('recoveredTranscriptStatus').textContent='Rebuilding an audit-only working ledger from your recovered answers…';
  try{
    const r=await fetch(`/api/owner-v2/conversation/sessions/${encodeURIComponent(sessionId)}/reconstruct-visible`,{method:'POST',headers:{'content-type':'application/json'}});
    let p={};try{p=await r.json()}catch{}
    if(!r.ok)throw new Error(p.detail||'Could not continue from the recovered transcript.');
    hide('recoveredTranscriptActions');
    window.__lifePatternsTranscriptOnlyRecovery=true;
    if(p.coverage){mergeCoverage(p.coverage);renderCoverageStatus()}
    if(p.reply)bubble('ai',p.reply);
    show('composer');
    if(p.pattern_active)show('patternPanel');else hide('patternPanel');
    $('sessionState').textContent='Recovered transcript · reconstructed development ledger';
    $('sessionSummary').textContent='Continued from your recovered answers using a newly reconstructed working ledger. This is useful for development/audit continuity, but it is not the lost original ledger and cannot become the clean scientific freeze.';
    $('sessionSummary').className='note';show('sessionSummary');
    scheduleExactRecovery();scrollToNextAction();
  }catch(e){
    $('recoveredTranscriptStatus').textContent=e.message;
    $('recoveredTranscriptStatus').className='error';
  }finally{btn.disabled=false}
};

$('startCleanFromRecovery').onclick=async()=>{
  localStorage.removeItem(EXACT_RECOVERY_KEY);
  completedResults=[];coverageAggregate={};
  window.__lifePatternsTranscriptOnlyRecovery=false;
  hide('recoveredTranscriptActions');
  resetVisibleInterview();
  $('sessionSummary').textContent='';$('sessionSummary').className='note';hide('sessionSummary');
  try{
    await start();
    renderCoverageStatus();
    scheduleExactRecovery();
    scrollToNextAction();
  }catch(e){
    $('sessionState').textContent='Could not start clean interview';
    setStatus(e.message,true);
  }
};
'''.strip()
    return html.replace(startup, action_js + "\n\n" + startup, 1)


IMPORT_RESUME_RECOVERABILITY_HTML = _build_import_resume_html()
