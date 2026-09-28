"use strict";
const el=id=>document.getElementById(id);
let state=null, busy=false, writing=false, pendingWrite=null, timer=null;
const show=(id,yes)=>{el(id).hidden=!yes;};
const status=text=>{el("status").textContent=text;};
async function api(path,body){
  const response=await fetch(path,{method:body===undefined?"GET":"POST",credentials:"same-origin",headers:{...(body===undefined?{}:{"Content-Type":"application/json"}),...(state?{"X-Life-Patterns-Session":state.session_id}:{})},body:body===undefined?undefined:JSON.stringify(body)});
  const value=await response.json();
  if(!response.ok){const error=new Error(value.detail||"Request failed.");error.status=response.status;throw error;}
  return value;
}
function node(tag,text,className){const n=document.createElement(tag);n.textContent=text;if(className)n.className=className;return n;}
function render(next){
  if(state&&state.session_id===next.session_id&&next.revision<state.revision)return;
  state=next;document.querySelectorAll('a[href^="/api/export"]').forEach(a=>{a.href=`/api/export?session_id=${encodeURIComponent(state.session_id)}`;});const p=state.phase;show("entry",false);show("consent",p==="consent");show("workspace",!["consent","declined"].includes(p));
  for(const [id,phases] of Object.entries({"question-panel":["awaiting_answer"],"review-panel":["review"],done:["complete","stopped"],"retry-panel":["error"],paused:["paused"]}))show(id,phases.includes(p));
  show("controls",!["complete","stopped","declined"].includes(p));show("correction-panel",["awaiting_answer","review","ready","error","paused"].includes(p)&&state.turns.length>0);
  el("import-notice").textContent=state.turns.length?`${state.turns.length} previous responses are already included. You do not need the old chat.`:"";
  el("agree").disabled=!state.ready;el("question").textContent=state.question?.text||"";el("turn-count").textContent=`(${state.turns.length})`;
  const history=el("history-items");history.replaceChildren();const selection=el("correction-target");const selected=selection.value;selection.replaceChildren();
  state.turns.forEach((t,i)=>{const item=node("div","","history-turn");item.append(node("small",`${i+1} · ${t.turn_id}`),node("p",t.question_text||"No original question recorded."),node("p",t.answer_text??"No answer recorded.","answer-text"));history.append(item);const option=node("option",`${i+1}. ${(t.question_text||t.answer_text||"Response").slice(0,80)}`);option.value=t.turn_id;selection.append(option);});
  if(selected)selection.value=selected;
  const review=el("review-items");review.replaceChildren();state.evidence.forEach(e=>{const item=node("div",e.observation,"evidence");item.append(node("small",`${e.time_frame} · ${e.relationship_context}\n${e.conditions.join("; ")}\n${e.review_status}`));e.source_quotes.forEach(q=>item.append(node("small",`${q.turn_id}: “${q.quote}”`)));review.append(item);});
  el("error-detail").textContent=state.error||"The last operation did not finish. Retry without retyping saved answers.";
  el("done-text").textContent=p==="complete"?"You confirmed this version. Its final file will not change.":"You stopped the interview. Completed answers are saved; unfinished parts remain explicit.";
  status(state.error||(p==="planning"?(state.processing?.message||`Preparing the next step. ${state.turns.length} responses saved.`):p==="consent"&&!state.ready?"The study is not open yet: Venice activation is pending.":p==="declined"?"The interview has stopped. No research export was created.":`${state.turns.length} responses saved · ${p.replaceAll("_"," ")}`));
  show("limited",p==="resource_limited");
  if(p==="review"&&!state.review.summary_shown&&!writing)markReviewSeen();
}
async function refresh(){try{render(await api("/api/session"));}catch(error){status(error.message);}finally{schedule();}}
function schedule(){
  clearTimeout(timer);
  if(!state)return;
  if(state.phase==="ready")timer=setTimeout(pump,500);
  else if(state.phase==="planning")timer=setTimeout(refresh,3000);
}
async function pump(){
  if(busy||!state||state.phase!=="ready")return;
  busy=true;status("Your answers are saved. Starting the next processing step…");
  try{render(await api("/api/next",{}));}catch(error){if(error.status!==409)status(error.message);await refresh();}finally{busy=false;schedule();}
}
async function command(action,text="",target=null){
  if(writing||!state)return false;writing=true;
  const same=pendingWrite&&pendingWrite.action===action&&pendingWrite.text===text&&pendingWrite.target===target;
  const payload=same?pendingWrite:{revision:state.revision,operation_id:crypto.randomUUID(),action,text,target};pendingWrite=payload;
  try{render(await api("/api/operations",payload));pendingWrite=null;return true;}
  catch(error){if(error.status===409){pendingWrite=null;await refresh();}status(error.message+" Your unsent text remains below.");return false;}
  finally{writing=false;schedule();}
}
async function markReviewSeen(){await command("review_seen");}
el("agree").onclick=()=>command("consent");el("decline").onclick=()=>command("decline");
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
