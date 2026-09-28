"use strict";
const el=id=>document.getElementById(id);
let state=null, busy=false, writing=false, pendingWrite=null, timer=null;
let lastSnapshotAt=null, serverAtSnapshot=null;
const show=(id,yes)=>{el(id).hidden=!yes;};
const status=text=>{el("status").textContent=text;};
async function api(path,body){
  const controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),15000);
  try{
    const response=await fetch(path,{method:body===undefined?"GET":"POST",credentials:"same-origin",cache:"no-store",signal:controller.signal,headers:{...(body===undefined?{}:{"Content-Type":"application/json"}),...(state?{"X-Life-Patterns-Session":state.session_id}:{})},body:body===undefined?undefined:JSON.stringify(body)});
    let value;try{value=await response.json();}catch{throw new Error("The server response could not be read. Check the saved status; do not re-enter a saved answer.");}
    if(!response.ok){const error=new Error(value.detail||"Request failed.");error.status=response.status;throw error;}
    return value;
  }catch(error){if(error.name==="AbortError")throw new Error("No server reply within 15 seconds. Connection may be interrupted; your last saved record is not being reset.");throw error;}
  finally{clearTimeout(timeout);}
}

function duration(seconds){const n=Math.max(0,Math.floor(seconds));return `${Math.floor(n/60)}m ${String(n%60).padStart(2,"0")}s`;}
function updateProcessing(){
  const planning=state?.phase==="planning";show("processing-panel",planning);
  if(!planning)return;
  const now=performance.now();const age=lastSnapshotAt===null?Infinity:(now-lastSnapshotAt)/1000;
  const serverNow=Number.isFinite(serverAtSnapshot)?serverAtSnapshot+(now-lastSnapshotAt):null;
  const p=state.processing||{};
  const since=value=>serverNow!==null&&Number.isFinite(Date.parse(value))?Math.max(0,(serverNow-Date.parse(value))/1000):null;
  const total=since(p.started_at),stageTime=since(p.stage_started_at),workerAge=since(p.worker_heartbeat_at),modelAge=since(p.model_activity_at);
  const serverFresh=age<12;const workerFresh=workerAge!==null&&workerAge<20;
  el("processing-title").textContent=p.message||"Preparing the next step";
  el("elapsed-time").textContent=`Elapsed: ${total===null?"awaiting timing data":duration(total)}${stageTime===null?"":` · This stage: ${duration(stageTime)}`}`;
  el("heartbeat-text").textContent=serverFresh?`Server connected · last reply ${Math.floor(age)}s ago`:`Connection delayed · last server reply ${Number.isFinite(age)?duration(age):"not received"}`;
  el("heartbeat-dot").className=serverFresh&&workerFresh?"live":"stale";
  el("worker-status").textContent=!serverFresh?"Worker status cannot be confirmed while the connection is delayed.":workerAge===null?"Waiting for a worker heartbeat.":workerFresh?`Worker heartbeat ${Math.floor(workerAge)}s ago · waiting for or processing the AI response`:`Worker heartbeat is stale (${duration(workerAge)}). This is not confirmation that the AI is still progressing.`;
  el("model-status").textContent=modelAge===null?"No AI response data received for this stage yet.":`Last AI response data ${duration(modelAge)} ago · ${p.stream_events_received||0} stream events received (not a completion percentage).`;
  el("processing-meter").hidden=!(serverFresh&&workerFresh);
  const stage=p.stage;for(const id of ["step-planner","step-admission","step-ready"]){el(id).removeAttribute("aria-current");el(id).classList.remove("completed");}
  if(stage==="planner")el("step-planner").setAttribute("aria-current","step");
  if(stage==="admission"){el("step-planner").classList.add("completed");el("step-admission").setAttribute("aria-current","step");}
  el("processing-note").textContent=(p.attempt>1?`Revision pass ${p.attempt}: checking a revised plan. `:"")+"Stages are not a percentage or an estimate of time remaining. You can close this tab and return with your private link.";
}
setInterval(updateProcessing,1000);

function node(tag,text,className){const n=document.createElement(tag);n.textContent=text;if(className)n.className=className;return n;}
function render(next){
  if(state&&state.session_id===next.session_id&&next.revision<state.revision)return;
  state=next;lastSnapshotAt=performance.now();serverAtSnapshot=Date.parse(next.server_time);document.querySelectorAll('a[href^="/api/export"]').forEach(a=>{a.href=`/api/export?session_id=${encodeURIComponent(state.session_id)}`;});const p=state.phase;show("entry",false);show("consent",p==="consent");show("workspace",!["consent","declined"].includes(p));
  for(const [id,phases] of Object.entries({"question-panel":["awaiting_answer"],"review-panel":["review"],done:["complete","stopped"],"retry-panel":["error"],paused:["paused"]}))show(id,phases.includes(p));
  show("controls",!["complete","stopped","declined"].includes(p));show("correction-panel",["awaiting_answer","review","ready","error","paused"].includes(p)&&state.turns.length>0);
  el("import-notice").textContent=state.turns.length?`${state.turns.length} previous responses are already included. You do not need the old chat.`:"";
  if(p==="consent")el("retrospective-ok").checked=state.collection_preferences?.retrospective_questions_welcome===true;
  if(!["consent","declined"].includes(p))el("retrospective-workspace").checked=state.collection_preferences?.retrospective_questions_welcome===true;
  el("agree").disabled=!state.ready;el("question").textContent=state.question?.text||"";el("turn-count").textContent=`(${state.turns.length})`;
  const history=el("history-items");history.replaceChildren();const selection=el("correction-target");const selected=selection.value;selection.replaceChildren();
  state.turns.forEach((t,i)=>{const item=node("div","","history-turn");item.append(node("small",`${i+1} · ${t.turn_id}`),node("p",t.question_text||"No original question recorded."),node("p",t.answer_text??"No answer recorded.","answer-text"));history.append(item);const option=node("option",`${i+1}. ${(t.question_text||t.answer_text||"Response").slice(0,80)}`);option.value=t.turn_id;selection.append(option);});
  if(selected)selection.value=selected;
  const review=el("review-items");review.replaceChildren();state.evidence.forEach(e=>{const item=node("div",e.observation,"evidence");item.append(node("small",`${e.time_frame} · ${e.relationship_context}\n${e.conditions.join("; ")}\n${e.review_status}`));e.source_quotes.forEach(q=>item.append(node("small",`${q.turn_id}: “${q.quote}”`)));review.append(item);});
  const payment=!["complete","stopped","declined"].includes(p)&&(state.provider_issue?.code==="payment_required"||state.error_code==="provider_http_402"||state.error==="provider_http_402");
  show("provider-blocked",payment);if(payment){show("pause",false);el("provider-title").textContent=state.provider_issue?.title||"Interview paused — AI service needs credit";el("provider-detail").textContent=state.provider_issue?.detail||"The AI provider returned a payment-required response. Your saved answers are safe. The organizer needs to check the API balance before this session can continue.";show("retry-panel",false);}
  if(!payment)show("pause",true);
  updateProcessing();
  el("error-detail").textContent=state.error||"The last operation did not finish. Retry without retyping saved answers.";
  el("done-text").textContent=p==="complete"?"You confirmed this version. Its final file will not change.":"You stopped the interview. Completed answers are saved; unfinished parts remain explicit.";
  status(state.error||(p==="planning"?(state.processing?.message||`Preparing the next step. ${state.turns.length} responses saved.`):p==="consent"&&!state.ready?"The study is not open yet: Venice activation is pending.":p==="declined"?"The interview has stopped. No research export was created.":`${state.turns.length} responses saved · ${p.replaceAll("_"," ")}`));
  show("limited",p==="resource_limited");if(p==="resource_limited"){const oversized=state.error==="model_context_budget_exceeded";el("limited-title").textContent=oversized?"Saved · This record needs researcher-side compaction":"Saved · Study processing limit reached";el("limited-detail").textContent=oversized?"Your answers are safe. This record is larger than the automatic model-context cost guard, so the researcher must prepare a compact continuation before more AI processing. Do not repeat your answers.":"Your record is still partial, not a completed survey or participant stop. The researcher can adjust the study processing allowance; you do not need to repeat your answers.";}
  if(p==="review"&&!state.review.summary_shown&&!writing)markReviewSeen();
}
async function refresh(){try{render(await api("/api/session"));}catch(error){status(error.message);}finally{schedule();}}
function schedule(){
  clearTimeout(timer);
  if(!state)return;
  if(state.phase==="ready")timer=setTimeout(pump,500);
  else if(state.phase==="planning")timer=setTimeout(refresh,3000);
  else if(state.phase==="provider_blocked")timer=setTimeout(refresh,15000);
}
async function pump(){
  if(busy||!state||state.phase!=="ready")return;
  busy=true;status("Your answers are saved. Starting the next processing step…");
  try{render(await api("/api/next",{}));}catch(error){if(error.status!==409)status(error.message);await refresh();}finally{busy=false;schedule();}
}
async function command(action,text="",target=null,retrospectiveQuestionsWelcome=null){
  if(writing||!state)return false;writing=true;
  const same=pendingWrite&&pendingWrite.action===action&&pendingWrite.text===text&&pendingWrite.target===target&&pendingWrite.retrospective_questions_welcome===retrospectiveQuestionsWelcome;
  const payload=same?pendingWrite:{revision:state.revision,operation_id:crypto.randomUUID(),action,text,target,retrospective_questions_welcome:retrospectiveQuestionsWelcome};pendingWrite=payload;
  try{render(await api("/api/operations",payload));pendingWrite=null;return true;}
  catch(error){if(error.status===409){pendingWrite=null;await refresh();}status(error.message+" Your unsent text remains below.");return false;}
  finally{writing=false;schedule();}
}
async function markReviewSeen(){await command("review_seen");}
el("check-status").onclick=refresh;
el("agree").onclick=()=>command("consent","",null,el("retrospective-ok").checked);el("decline").onclick=()=>command("decline");
el("retrospective-workspace").onchange=()=>command("set_retrospective_preference","",null,el("retrospective-workspace").checked);
el("pause").onclick=()=>command("pause");el("stop").onclick=()=>command("stop");el("resume").onclick=()=>command("resume");
el("send").onclick=async()=>{const text=el("answer").value;if(await command("answer",text)&&!state.error)el("answer").value="";};
el("skip").onclick=()=>command("skip");el("retry").onclick=()=>pumpRetry();
async function pumpRetry(){if(!busy&&state?.phase==="error"){busy=true;try{render(await api("/api/next",{}));}catch(error){status(error.message);await refresh();}finally{busy=false;schedule();}}}
el("confirm").onclick=()=>command("confirm");
el("correct-review").onclick=async()=>{if(await command("review_correction",el("review-text").value))el("review-text").value="";};
el("save-correction").onclick=async()=>{if(await command("correct",el("correction-text").value,el("correction-target").value))el("correction-text").value="";};
el("copy-link").onclick=async()=>{if(!location.hash.startsWith("#resume=")){status("Use the private resume link originally sent to you.");return;}try{await navigator.clipboard.writeText(location.href);status("Private resume link copied. Keep it private.");}catch{status("Copy the full address from your browser's address bar. Keep it private.");}};
el("import-button").onclick=async()=>{try{const file=el("import-file").files[0];if(!file)throw new Error("Choose a JSON record first.");if(file.size>1500000)throw new Error("This record is too large; ask Joel to import it.");render(await api("/api/import",{source_type:el("source-type").value,record_text:await file.text()}));}catch(error){status(error.message);}};
async function start(){
  const hash=new URLSearchParams(location.hash.slice(1));
  try{if(hash.has("join")){const data=await api("/api/join",{token:hash.get("join")});history.replaceState(null,"",`/#resume=${data.resume_token}`);render(data);}else if(hash.has("resume")){render(await api("/api/resume",{token:hash.get("resume")}));}else{render(await api("/api/session"));}schedule();}
  catch(error){show("entry",true);status(error.message);}
}
start();
