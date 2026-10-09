"use strict";
const el=id=>document.getElementById(id);
const suppliedKey=new URLSearchParams(location.hash.slice(1)).get("key");
if(suppliedKey){sessionStorage.setItem("lp_admin",suppliedKey);history.replaceState(null,"","/admin");}
let key=suppliedKey||sessionStorage.getItem("lp_admin")||"";
const headers=()=>({Authorization:`Bearer ${key}`,"Content-Type":"application/json"});
function showAuth(){
  el("researcher-access").hidden=false;
  el("researcher-key-label").hidden=Boolean(key);
  el("researcher-unlock").hidden=Boolean(key);
  el("researcher-lock").hidden=!key;
}
function clearAuth(message){
  key="";sessionStorage.removeItem("lp_admin");showAuth();
  el("status").textContent=message||"Researcher access key required. No record counts have been loaded.";
}

async function request(path,body){
  if(!key)throw new Error("Researcher access required. Enter your private key to load counts.");
  const response=await fetch(path,{method:body===undefined?"GET":"POST",headers:headers(),body:body===undefined?undefined:JSON.stringify(body)});
  const value=await response.json();
  if(response.status===401){clearAuth("Researcher key was rejected. Please unlock again.");throw new Error("Researcher access required.");}
  if(!response.ok)throw new Error(value.detail||"Request failed");
  return value;
}

async function download(path,filename){
  try{
    if(!key)throw new Error("Researcher access required.");
    const response=await fetch(path,{headers:headers()});
    if(!response.ok)throw new Error((await response.json()).detail);
    const blob=await response.blob();
    const url=URL.createObjectURL(blob);
    const a=document.createElement("a");
    a.href=url;a.download=filename;a.click();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }catch(error){el("status").textContent=error.message;}
}

function renderFeedbackItem(item, contextOnly){
  const article=document.createElement("article");
  const heading=document.createElement("h3");
  heading.textContent=(contextOnly?"Context only":"Potential question issue")+` · ${item.route_id}`;
  const question=document.createElement("p");
  const promptLabel=item.source_type==="review_derived"
    ?"Survey prompt associated with the imported record (the remark may refer to a later follow-up)"
    :"Recorded question";
  question.textContent=`${promptLabel}: ${item.question_text||"historical question unavailable"}`;
  const description=document.createElement("p");
  description.textContent=contextOnly
    ?"This remark does not clearly criticize the survey question. It is not an automatic rewrite request."
    :"A reported or reviewer-inferred concern. Its wording is not proof that the question is defective.";
  const quotation=document.createElement("blockquote");
  quotation.textContent=item.feedback_text+(item.feedback_truncated?" [excerpt]":"");
  const origin=document.createElement("small");
  origin.textContent=`${item.provenance_label||"Source annotation"} · ${item.source_type} · Turn ${item.turn_id}`;
  article.append(heading,question,description,quotation,origin);

  const fullAnswer=item.recorded_answer_context||"";
  if(fullAnswer){
    const context=document.createElement("details");
    const trigger=document.createElement("summary");
    trigger.textContent="Show original recorded answer/context";
    const answer=document.createElement("blockquote");
    answer.textContent=fullAnswer+(item.answer_context_truncated?" [truncated]":"");
    const caution=document.createElement("p");
    caution.textContent="This is the preserved answer, not a complete chat transcript. It may omit intervening assistant messages; the isolated remark is not a separate recorded answer.";
    context.append(trigger,answer,caution);
    article.append(context);
  }
  if(!contextOnly){
    const controls=document.createElement("details");
    const toggle=document.createElement("summary");
    const current={new:"New",triaging:"Investigating",revision_proposed:"Revision proposed",resolved:"Resolved",dismissed:"Dismissed"};
    toggle.textContent=`Researcher tracking (optional) — ${current[item.status]||"New"}`;
    const help=document.createElement("p");
    help.textContent="New: not assessed; Investigating: checking source/context; Revision proposed: draft wording exists (not live); Resolved: handled; Dismissed: not an actionable question defect. These labels do not change questions or participant answers. You do not need to select one.";
    const disposition=document.createElement("select");
    for(const [code,label] of [["new","New — awaiting review"],["triaging","Investigating — checking context"],["revision_proposed","Revision proposed — draft only"],["resolved","Resolved — addressed"],["dismissed","Dismissed — not a question defect"]]){
      const option=document.createElement("option");
      option.value=code;option.textContent=label;
      if(item.status===code)option.selected=true;
      disposition.append(option);
    }
    const revision=document.createElement("input");
    revision.placeholder="Draft version ID (only for Revision proposed)";
    revision.value=item.revision_id||"";revision.maxLength=120;
    const save=document.createElement("button");
    save.className="secondary";save.textContent="Save researcher status";
    save.onclick=async()=>{
      try{
        await request(`/api/admin/question-feedback/${encodeURIComponent(item.feedback_id)}/disposition`,{status:disposition.value,revision_id:revision.value});
        await refreshQuestionFeedback();
      }catch(error){el("status").textContent=error.message;}
    };
    controls.append(toggle,help,disposition,revision,save);
    article.append(controls);
  }
  return article;
}

async function refreshQuestionFeedback(){
  try{
    const result=await request("/api/admin/question-feedback");
    const target=el("question-feedback");target.replaceChildren();
    const contextual=el("feedback-contextual");contextual.replaceChildren();
    const notes=result.contextual_notes||[];
    el("feedback-summary").textContent=`${result.total} possible question-design concerns · ${notes.length} other conversational remarks. Tracking is optional; feedback does not automatically change the frozen questionnaire.`;
    for(const item of result.feedback||[])target.append(renderFeedbackItem(item,false));
    for(const item of notes)contextual.append(renderFeedbackItem(item,true));
    el("feedback-contextual-count").textContent=`Other remarks retained for context (${notes.length})`;
    el("feedback-contextual-section").hidden=notes.length===0;
    if(!result.total)target.textContent="No actionable question criticisms currently identified.";
  }catch(error){el("status").textContent=error.message;}
}

async function refreshSubmissions(){
  try{
    const result=await request("/api/admin/gpt-submissions");
    el("submissions").replaceChildren();
    result.submissions.forEach(s=>{
      const p=document.createElement("p");
      p.textContent=`${s.submission_id} · ${s.received_at_utc||"time unavailable"} · ${s.primary_turn_count} primary turns · ${s.cf003_turn_count} CF-003 turns · ${s.collection_mode||"unknown"} `;
      const primary=document.createElement("button");
      primary.textContent="Download primary JSON";primary.className="secondary";
      primary.onclick=()=>download(`/api/admin/gpt-submissions/${encodeURIComponent(s.submission_id)}/primary`,"life-patterns-participant-export.json");
      const cf003=document.createElement("button");
      cf003.textContent="Download CF-003 JSON";cf003.className="secondary";
      cf003.onclick=()=>download(`/api/admin/gpt-submissions/${encodeURIComponent(s.submission_id)}/cf003`,"life-patterns-cf003-secondary-v0.json");
      p.append(primary,cf003);el("submissions").append(p);
    });
  }catch(error){el("status").textContent=error.message;}
}

async function refresh(){
  try{
    const result=await request("/api/admin/sessions");
    el("sessions").replaceChildren();
    result.sessions.forEach(s=>{
      const p=document.createElement("p");
      p.textContent=`${s.session_id} · ${s.phase} · ${s.turn_count} responses · ${s.collection_mode||"unknown"} · ${s.model_calls||0} Venice calls · ${s.prompt_tokens||0} input / ${s.completion_tokens||0} output tokens `;
      const button=document.createElement("button");
      button.textContent="Download consented record";button.className="secondary";
      button.onclick=()=>download(`/api/admin/exports/${encodeURIComponent(s.session_id)}`,"life-patterns-participant-export.json");
      p.append(button);
      if(s.error_code==="provider_http_402"){
        const unblock=document.createElement("button");
        unblock.className="secondary";unblock.textContent="Allow retry after fixing Venice API credit";
        unblock.onclick=async()=>{
          if(!confirm("Confirm that you checked and resolved the Venice API billing issue. This permits this session to retry; it does not purchase credit."))return;
          try{await request(`/api/admin/sessions/${encodeURIComponent(s.session_id)}/resume-provider`,{billing_issue_resolved:true});await refresh();}
          catch(error){el("status").textContent=error.message;}
        };
        p.append(unblock);
      }
      el("sessions").append(p);
    });
    el("status").textContent="Research records loaded. GPT submissions do not run inference.";
  }catch(error){el("status").textContent=error.message;}
}

el("create").onclick=async()=>{
  try{
    const file=el("record").files[0];
    if(file&&file.size>1500000)throw new Error("Record too large.");
    const record_text=file?await file.text():null;
    const result=await request("/api/admin/invitations",{source_type:el("source-type").value,source_mode:el("source-mode").value,record_text});
    el("link").value=location.origin+result.resume_path;
    await refresh();
  }catch(error){el("status").textContent=error.message;}
};
el("copy").onclick=async()=>{
  try{await navigator.clipboard.writeText(el("link").value);el("status").textContent="Invitation copied. Send it only to its participant.";}
  catch{el("link").select();el("status").textContent="Copy the selected invitation link.";}
};
el("researcher-unlock").onclick=async()=>{
  const supplied=el("researcher-key").value.trim();
  if(!supplied){clearAuth("Enter the researcher access key to view records.");return;}
  key=supplied;el("researcher-key").value="";sessionStorage.setItem("lp_admin",key);showAuth();
  await refresh();await refreshSubmissions();await refreshQuestionFeedback();
};
el("researcher-lock").onclick=()=>clearAuth("Researcher session locked. No records have been loaded.");
el("refresh").onclick=refresh;
el("submissions-refresh").onclick=refreshSubmissions;
el("feedback-refresh").onclick=refreshQuestionFeedback;
el("feedback-download").onclick=()=>download("/api/admin/question-feedback","life-patterns-question-feedback.json");
showAuth();
if(key){refresh();refreshSubmissions();refreshQuestionFeedback();}
else{el("status").textContent="Researcher access required. No record counts have been loaded.";}
