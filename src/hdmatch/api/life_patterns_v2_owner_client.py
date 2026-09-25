"""Browser state/transport for the consolidated owner interview. No model calls here."""

CLIENT_SCRIPT = r"""
'use strict';
const $=id=>document.getElementById(id);
const KEY='lifePatternsExactRecoveryV2', PREVIOUS=KEY+':previous';
const tabId=crypto.randomUUID();
const S={view:null,snapshot:null,blueprint:null,draft:'',pending:null,busy:false,paused:false,
  loading:true,error:'',restoreError:false,rawBackup:null,savedAt:null,saveFailed:false,
  answerDraft:'',correctionDrafts:{},correction:null,notice:'',epoch:0,follow:true,otherTab:false,renderedConversation:''};
const visibility=(id,visible)=>{$(id).hidden=!visible};
const clone=value=>JSON.parse(JSON.stringify(value));
function nearLatest(){return document.documentElement.scrollHeight-(scrollY+innerHeight)<260}
function scrollLatest(force=false){
  if(!force&&!S.follow){visibility('jumpLatest',true);return;}
  requestAnimationFrame(()=>{$('actionArea').scrollIntoView({block:'end',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});visibility('jumpLatest',false)});
}
window.addEventListener('scroll',()=>{S.follow=nearLatest();if(S.follow)visibility('jumpLatest',false)},{passive:true});
$('jumpLatest').onclick=()=>{S.follow=true;scrollLatest(true)};
function localRead(){return localStorage.getItem(KEY)}
function bundle(){return {schema:'life-patterns-browser-recovery-v2',saved_at:new Date().toISOString(),
  recovery_only:true,audit_checkpoint:true,unvalidated_working_state:true,canonical_measurement:false,not_scientific_freeze:true,
  server_snapshot:S.snapshot,client_state:{workflow_client_version:1,paused:S.paused,draft:S.draft,pending_operation:S.pending,
    correction_target:S.correction,answer_draft:S.answerDraft,correction_drafts:S.correctionDrafts,writer:tabId,completed_results:S.view?.patterns||[],aggregate_coverage:S.view?.aggregate_coverage||{}}};}
function persist(){
  if(!S.snapshot||S.restoreError||S.otherTab)return false;
  try{
    const old=localRead();let prior=null;try{prior=JSON.parse(old||'null')}catch{}
    const priorRev=prior?.server_snapshot?.workflow?.revision||0, revision=S.snapshot.workflow?.revision||0;
    if(prior?.server_snapshot?.session_id===S.snapshot.session_id&&priorRev>revision){S.otherTab=true;throw new Error('A newer checkpoint exists in another tab.');}
    const candidate=bundle();
    if(prior&&JSON.stringify(prior.server_snapshot)===JSON.stringify(candidate.server_snapshot)&&
       JSON.stringify({...prior.client_state,writer:null})===JSON.stringify({...candidate.client_state,writer:null})){
      S.savedAt=prior.saved_at;S.rawBackup=old;S.saveFailed=false;return true;
    }
    const next=JSON.stringify(candidate);
    if(old&&(prior?.server_snapshot?.session_id!==S.snapshot.session_id||priorRev<revision))localStorage.setItem(PREVIOUS,old);
    localStorage.setItem(KEY,next);S.rawBackup=next;S.savedAt=new Date().toISOString();S.saveFailed=false;return true;
  }catch(e){S.saveFailed=true;S.notice='Browser saving failed. Keep this page open and download a backup before leaving.';return false;}
}
function renderSave(){
  $('saveState').textContent=S.saveFailed?'Not saved — download a backup':S.otherTab?'Another tab has newer state':S.restoreError?'Original backup preserved':S.savedAt?'Saved in this browser':'Not yet checkpointed';
}
function appendText(parent,tag,text,className=''){const el=document.createElement(tag);el.textContent=String(text||'');el.className=className;parent.appendChild(el);return el;}
function renderConversation(){
  const rows=S.view?.conversation||[];const signature=JSON.stringify(rows);
  if(signature===S.renderedConversation)return;
  const previous=JSON.parse(S.renderedConversation||'[]');
  const oldHeight=document.documentElement.scrollHeight,oldY=scrollY;
  $('conversation').replaceChildren();
  for(const row of rows){if(String(row.text||'').startsWith('INTERNAL PRIOR CONTEXT'))continue;
    const bubble=appendText($('conversation'),'div','',row.role==='user'?'bubble user':'bubble ai');
    appendText(bubble,'div',row.role==='user'?'You':'Interviewer','meta');appendText(bubble,'div',row.text);
  }
  S.renderedConversation=signature;
  if(previous.length&&!S.follow)window.scrollTo({top:oldY,behavior:'instant'});
  if(rows.length>previous.length)scrollLatest();
}
function renderProgress(){
  const domains=S.blueprint?.domains||[],coverage=S.view?.aggregate_coverage||{};
  let handled=0,evidenced=0;
  $('coverageDetails').replaceChildren();
  for(const d of domains){const status=coverage[d.domain_id]?.status||'unassessed';
    if(['sufficient','unknown','inapplicable','declined'].includes(status))handled++;
    if(status==='sufficient')evidenced++;
    appendText($('coverageDetails'),'div',`${d.title}: ${status==='sufficient'?'supported':status.replaceAll('_',' ')}`);
  }
  appendText($('coverageDetails'),'p',`${handled} of ${domains.length} areas addressed; ${evidenced} supported. Explicitly unknown, declined, or inapplicable areas count as addressed, not as positive evidence.`);
  $('progressBar').value=domains.length?Math.round(100*handled/domains.length):0;
  $('progressText').textContent=domains.length?`≈${Math.round(100*handled/domains.length)}% · ${domains.length-handled} areas still open`:'Loading interview coverage…';
}
function render(){
  const phase=S.view?.phase;const interactive=!!S.view&&!S.loading&&!S.restoreError&&!S.otherTab;
  const paused=S.paused||phase==='paused';
  visibility('intro',!(S.view?.conversation?.length>2));
  visibility('pausedPanel',paused&&!!S.view);
  visibility('boundedPanel',interactive&&!paused&&['bounded','complete'].includes(phase));
  $('boundedTitle').textContent=phase==='complete'?'The planned areas are addressed':'A useful place to stop';
  $('boundedText').textContent=phase==='complete'?'You can review and export the record. Addressed areas include anything explicitly unknown, declined, or inapplicable; this is not a validity score.':'No worthwhile next question was identified. The remaining areas stay open; nothing has been marked complete just to end the interview.';
  visibility('tryAnother',phase==='bounded');
  visibility('patternPanel',interactive&&!paused&&phase==='synthesis_review'&&!S.correction&&!S.view?.draft_needs_review);
  $('formulation').textContent=S.view?.pattern_proposition||'';
  $('inferenceNote').textContent=S.view?.inference_note?`What is being inferred: ${S.view.inference_note}`:'';
  visibility('composer',interactive&&(!!S.correction||(!paused&&['awaiting_answer','synthesis_review','bounded'].includes(phase)))&&S.view?.recovery_quality!=='visible_transcript_only');
  visibility('correctionTarget',!!S.correction);visibility('cancelCorrection',!!S.correction);
  $('correctionTarget').textContent=S.correction?'Adding a correction to a saved pattern. The original stays in its history.':'';
  $('messageLabel').textContent=S.correction?'Your correction':phase==='synthesis_review'?'Your response or correction':'Your response';
  $('message').placeholder=phase==='synthesis_review'?'Say what fits, what is wrong, or what needs qualifying…':'Answer in your own words…';
  if($('message').value!==S.draft)$('message').value=S.draft;
  $('message').readOnly=S.busy;
  $('send').disabled=S.busy||!!S.pending||!S.draft.trim()||S.otherTab;
  for(const id of ['accept','investigate','reject','unresolved','tryAnother','reconstruct'])$(id).disabled=S.busy||!!S.pending||!interactive;
  $('finishForNow').disabled=S.loading||!S.view||paused;
  $('resumeInterview').disabled=S.busy||S.otherTab;
  $('viewPatterns').textContent=`Your patterns (${S.view?.patterns?.length||0})`;
  $('operationStatus').textContent=S.loading?'Restoring your interview…':S.busy?(S.paused?'Pausing here; the in-flight operation can finish safely.':({answer:'Considering your answer…',advance:'Looking for the next useful question…',adjudicate:'Saving your judgment…',investigate:'Checking what is still worth investigating…',annotate:'Saving your correction…',reconstruct:'Reconstructing development context…'}[S.pending?.kind]||'Updating the interview…')):'';
  $('operationStatus').setAttribute('aria-busy',String(S.busy||S.loading));
  visibility('errorArea',!!S.error||S.otherTab);
  $('errorText').textContent=S.otherTab?'This interview changed in another tab. Check the latest state before continuing.':S.error;
  $('retryAction').disabled=S.busy;visibility('retryAction',S.restoreError||!!S.pending);
  $('retryAction').textContent=S.restoreError?'Retry restoration':S.pending?.kind==='advance'?'Retry next question':'Retry saved operation';
  $('freezeMeasurement').disabled=!interactive||S.busy||!!S.pending||S.view?.recovery_quality!=='exact_hidden_ledger';
  visibility('reconstruct',S.view?.recovery_quality==='visible_transcript_only');
  $('qualityNote').textContent=S.view?.recovery_quality==='exact_hidden_ledger'?'The research export includes the exact source archive, current pattern statuses, and explicitly unresolved material. Freezing fixes the bytes; it does not validate their interpretation.':'An older transcript can support development continuity, but is not a clean research freeze.';
  $('statusLine').textContent=S.notice;
  $('buildLabel').textContent=S.blueprint?.build_version||'';
  renderSave();renderConversation();renderProgress();
}
function renderPatterns(){
  const list=$('patternsList');list.replaceChildren();
  const rows=S.view?.patterns||[];
  if(!rows.length)appendText(list,'p','No patterns recorded yet. You do not need to manufacture one to make progress.');
  for(const row of rows){
    const el=appendText(list,'article','','pattern');
    const label=row.origin==='direct_report'?'Directly stated by you':row.origin==='legacy_recovery'?'Recovered from an older interview':row.origin==='source_summary'?'Summary of your reports — not a new inference':'Interviewer connection';
    appendText(el,'div',`${label} · ${row.status}`,'meta');appendText(el,'p',row.wording);
    if(row.scope_note)appendText(el,'p',row.scope_note,'note');
    if(row.exception_note)appendText(el,'p',row.exception_note,'note');
    for(const n of row.corrections||[]){appendText(el,'strong','Your correction');appendText(el,'p',n.text);appendText(el,'p','The earlier wording is disputed, not silently re-accepted.','note');}
    if(row.sources?.length){const details=document.createElement('details');el.appendChild(details);appendText(details,'summary','Source context');for(const source of row.sources)appendText(details,'p',source.text,'source');}
    const b=appendText(el,'button','Add a correction','secondary');b.onclick=()=>{
      if(S.busy||S.pending){S.notice='Finish or reconcile the pending operation before adding a correction.';$('patternsDialog').close();render();return;}
      if(!S.correction)S.answerDraft=S.draft;
      S.correction=row.proposal_id;S.draft=S.correctionDrafts[row.proposal_id]||'';$('patternsDialog').close();persist();render();$('message').focus({preventScroll:true});scrollLatest(true);
    };
  }
}
function showPatterns(){renderPatterns();if(!$('patternsDialog').open)$('patternsDialog').showModal();}
for(const id of ['viewPatterns','pausedPatterns','reviewFinal'])$(id).onclick=showPatterns;
$('closePatterns').onclick=()=>$('patternsDialog').close();
$('message').addEventListener('input',()=>{S.draft=$('message').value;if(S.correction)S.correctionDrafts[S.correction]=S.draft;persist();$('send').disabled=S.busy||!!S.pending||!S.draft.trim();renderSave()});
$('message').addEventListener('keydown',e=>{if(e.key==='Enter'&&(e.ctrlKey||e.metaKey)){e.preventDefault();send()}});
$('cancelCorrection').onclick=()=>{if(S.correction)S.correctionDrafts[S.correction]=S.draft;S.correction=null;S.draft=S.answerDraft;S.answerDraft='';persist();render()};
async function http(path,{method='GET',body,timeout=240000}={}){
  const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),timeout);
  try{const r=await fetch(path,{method,body:body===undefined?undefined:JSON.stringify(body),headers:{'content-type':'application/json','x-life-patterns-client':'workflow-v1'},cache:'no-store',signal:controller.signal});
    let p={};try{p=await r.json()}catch{}
    if(!r.ok){const e=new Error(typeof p.detail==='string'?p.detail:'The request did not finish.');e.status=r.status;throw e;}
    return p;
  }catch(e){if(e.name==='AbortError')throw new Error('This is taking longer than expected. The server may still finish; check the latest state before retrying.');throw e;}finally{clearTimeout(timer)}
}
function accept(p){
  if(!p.view||!p.snapshot||p.view.session_id!==p.snapshot.session_id)throw new Error('The server returned an incomplete checkpoint. Your earlier backup is unchanged.');
  if(S.view&&S.view.session_id===p.view.session_id&&p.view.revision<S.view.revision)throw new Error('An older response was ignored.');
  S.view=p.view;S.snapshot=p.snapshot;
}
function completePending(){
  const pending=S.pending;
  if(pending?.kind==='answer')S.draft='';
  if(pending?.kind==='annotate'){S.correctionDrafts[S.correction]='';S.correction=null;S.draft=S.answerDraft;S.answerDraft='';}
  S.pending=null;
}
async function perform(kind,payload={}){
  if(S.busy||S.pending||S.loading||S.otherTab||!S.view)return;
  if((S.paused||S.view.phase==='paused')&&!['pause','resume','annotate'].includes(kind))return;
  S.pending={session_id:S.view.session_id,operation_id:crypto.randomUUID(),expected_revision:S.view.revision,kind,payload};
  await transmit();
}
async function transmit(){
  if(S.busy||!S.pending||S.otherTab)return;
  S.busy=true;S.error='';S.follow=nearLatest();const request=clone(S.pending),epoch=S.epoch;
  persist();render();
  try{
    const {session_id,...operation}=request;
    const p=await http(`/api/owner-v2/conversation/sessions/${encodeURIComponent(session_id)}/operations`,{method:'POST',body:operation});
    if(epoch!==S.epoch||S.view?.session_id!==session_id)return;
    accept(p);completePending();
    S.notice=p.direct_pattern_recorded?'Saved to your patterns from your own words.':p.reported_summary_recorded?'Summary saved with its original sources.':p.correction_saved?'Your correction is saved; the earlier interpretation is now marked disputed.':p.status==='accepted'?'Connection saved to your patterns.':p.no_useful_question?'No extra question has been added just to fill a gap.':'';
    persist();
  }catch(e){if(epoch===S.epoch){S.error=e.message;persist();}}
  finally{if(epoch===S.epoch){S.busy=false;render();await nextStep();}}
}
async function nextStep(){
  if(S.busy||S.pending||S.loading||S.restoreError||S.otherTab||!S.view)return;
  if(S.paused){if(S.view.phase!=='paused')await perform('pause');return;}
  if(S.view.repair_needs_review){await perform('review_repair');return;}
  if(S.view.draft_needs_review){await perform('review_draft');return;}
  if(S.view.phase==='advancing')await perform('advance');
}
async function send(){
  if(S.busy||S.pending||S.loading||!S.draft.trim()||(!S.correction&&(S.paused||S.view?.phase==='paused')))return;
  await perform(S.correction?'annotate':'answer',S.correction?{proposal_id:S.correction,message:S.draft.trim()}:{message:S.draft.trim()});
}
$('send').onclick=send;
$('finishForNow').onclick=async()=>{S.paused=true;S.notice='';persist();render();await nextStep()};
$('resumeInterview').onclick=async()=>{
  if(S.busy)return;
  S.paused=false;persist();render();
  if(S.pending){await reconcile();return;}
  if(S.view?.phase==='paused')await perform('resume');else await nextStep();
};
$('accept').onclick=()=>perform('adjudicate',{decision:'accept'});
$('reject').onclick=()=>perform('adjudicate',{decision:'reject'});
$('unresolved').onclick=()=>perform('adjudicate',{decision:'unresolved'});
$('investigate').onclick=()=>perform('investigate');
$('tryAnother').onclick=()=>perform('advance');
$('reconstruct').onclick=()=>perform('reconstruct');
async function reconcile(){
  if(S.busy||!S.snapshot)return;
  S.busy=true;S.error='';render();
  try{
    let p;try{p=await http(`/api/owner-v2/conversation/sessions/${encodeURIComponent(S.snapshot.session_id)}/recovery`)}catch(e){if(e.status!==404)throw e;p=await http('/api/owner-v2/conversation/sessions/restore',{method:'POST',body:{snapshot:S.snapshot}})}
    accept(p);S.otherTab=false;
    const receipt=S.pending&&p.snapshot.workflow?.receipts?.[S.pending.operation_id];
    if(receipt){completePending();S.notice='The saved operation already finished. It has not been submitted twice.';}
    else if(S.pending&&p.view.revision!==S.pending.expected_revision){S.error='Another operation changed the interview. The pending response is preserved; download a backup before starting a separate interview or inspecting the conflict.';}
    else if(S.pending){S.error='The operation is not committed yet. Retry the saved operation when ready.';}
    S.restoreError=false;persist();
  }catch(e){S.error=e.message;}
  finally{S.busy=false;render();await nextStep();}
}
$('reconcileAction').onclick=()=>S.restoreError?startup():reconcile();
$('retryAction').onclick=()=>S.restoreError?startup():transmit();
async function startup(imported=null){
  if(S.busy)return;
  S.loading=true;S.error='';S.restoreError=false;S.epoch++;render();
  try{
    S.blueprint=await http('/api/owner-v2/conversation/coverage/blueprint');
    let raw=imported?JSON.stringify(imported):localRead();S.rawBackup=raw;
    const saved=raw?JSON.parse(raw):null;
    if(saved){
      const snapshot=saved.server_snapshot||((saved.schema==='life-patterns-hidden-ledger-session-v2')?saved:null);
      const client=saved.client_state||{};
      S.paused=Boolean(client.paused);S.draft=String(client.draft||'');S.pending=client.pending_operation||null;S.correction=client.correction_target||null;S.answerDraft=String(client.answer_draft||'');S.correctionDrafts=client.correction_drafts||{};
      let p;
      if(snapshot){
        S.snapshot=snapshot;
        try{p=await http(`/api/owner-v2/conversation/sessions/${encodeURIComponent(snapshot.session_id)}/recovery`)}catch(e){if(e.status!==404)throw e;p=await http('/api/owner-v2/conversation/sessions/restore',{method:'POST',body:{snapshot,client_state:client}})}
      }else if(['life-patterns-local-recovery-v1','life-patterns-visible-recovery-v1'].includes(saved.schema)){
        p=await http('/api/owner-v2/conversation/sessions/restore-visible',{method:'POST',body:{turns:saved.turns||[]}});
      }else throw new Error('This backup format is not supported. The original is still preserved.');
      S.view=null;accept(p);
      if(S.pending&&p.snapshot.workflow?.receipts?.[S.pending.operation_id])completePending();
      else if(S.pending)S.error='A saved operation needs reconciliation. Check its latest state or retry it without retyping.';
    }else{
      const p=await http('/api/owner-v2/conversation/sessions',{method:'POST'});accept(p);S.paused=false;S.pending=null;S.draft='';
    }
    S.otherTab=false;persist();
  }catch(e){S.restoreError=true;S.error=`Could not restore or start the interview. ${e.message} No existing checkpoint has been replaced.`;}
  finally{S.loading=false;render();await nextStep();}
}
function download(name,content,type='application/json'){
  const blob=new Blob([content],{type}),url=URL.createObjectURL(blob),a=document.createElement('a');
  a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
function backup(){
  const content=S.restoreError?S.rawBackup:S.snapshot?JSON.stringify(bundle(),null,2):S.rawBackup;
  if(!content){S.error='No backup is available yet.';render();return;}
  download('life-patterns-backup.json',content);S.notice='Backup exported locally. It may contain private interview material.';render();
}
$('downloadRecovery').onclick=backup;$('errorBackup').onclick=backup;
$('downloadPrevious').onclick=()=>{try{const raw=localStorage.getItem(PREVIOUS);if(!raw)throw new Error('No previous checkpoint is available.');download('life-patterns-previous-backup.json',raw);}catch(e){S.error=e.message;render()}};
$('summaryExport').onclick=()=>{
  const rows=S.view?.patterns||[];
  const text=['Life Patterns — working summary',...rows.map((p,i)=>`${i+1}. ${p.wording}
Status: ${p.status}; source: ${p.origin}
${(p.corrections||[]).map(n=>'Your correction: '+n.text).join('\n')}`),
  '\nOpen/unknown areas remain explicitly incomplete. This summary is not a scientific validation.'].join('\n\n');
  download('life-patterns-summary.txt',text,'text/plain');
};
$('freezeMeasurement').onclick=async()=>{
  if(S.busy||S.pending||!S.view)return;
  try{const p=await http(`/api/owner-v2/conversation/sessions/${encodeURIComponent(S.view.session_id)}/measurement`);
    download(`life-patterns-measurement-${p.measurement_bundle_sha256.slice(0,12)}.json`,JSON.stringify(p,null,2));
    S.notice='Research record frozen and exported locally, including the source archive. Keep it unchanged. An unsent draft is not part of this record.';
  }catch(e){S.error=e.message}render();
};
$('importRecovery').onclick=()=>{if(!S.busy)$('importFile').click()};
$('importFile').onchange=async()=>{
  const file=$('importFile').files?.[0];if(!file)return;
  try{const raw=await file.text(),p=JSON.parse(raw);const current=localRead();if(current)localStorage.setItem(PREVIOUS,current);await startup(p)}catch(e){S.error='Import failed; current recovery data was preserved. '+e.message;render()}finally{$('importFile').value=''}
};
$('startSeparate').onclick=async()=>{
  if(S.busy)return;
  if(!confirm('Start a separate interview? The current checkpoint will be retained as the previous backup. Download it first to keep an additional copy.'))return;
  try{const current=localRead();if(current)localStorage.setItem(PREVIOUS,current);
    const p=await http('/api/owner-v2/conversation/sessions',{method:'POST'});
    S.epoch++;S.view=null;S.snapshot=null;S.pending=null;S.draft='';S.answerDraft='';S.correctionDrafts={};S.correction=null;S.paused=false;S.restoreError=false;S.otherTab=false;S.error='';accept(p);persist();render();
  }catch(e){S.error=e.message;render()}
};
window.addEventListener('storage',e=>{
  if(e.key!==KEY||!e.newValue||S.loading)return;
  try{const b=JSON.parse(e.newValue);if(b.client_state?.writer!==tabId&&b.server_snapshot?.session_id===S.view?.session_id&&
    ((b.server_snapshot.workflow?.revision||0)>S.view.revision||b.client_state?.pending_operation)){S.otherTab=true;S.paused=true;render()}}catch{}
});
window.addEventListener('pagehide',()=>persist());
// A narrow inspectable seam for deterministic consumer tests; never authorizes server operations.
window.lifePatternsClient={state:S,send,perform,startup,reconcile,render,persist};
startup();
"""
