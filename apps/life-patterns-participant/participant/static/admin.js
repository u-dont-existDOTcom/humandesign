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

async function refreshQuestionFeedback(){
  try{
    const result=await request("/api/admin/question-feedback");
    const target=el("question-feedback");target.replaceChildren();
    const routes=Object.entries(result.by_route||{}).map(([r,n])=>`${r}: ${n}`).join(" · ");
    el("feedback-summary").textContent=`${result.total} question feedback item(s). ${routes}`;
    result.feedback.forEach(item=>{
      const article=document.createElement("article");
      const heading=document.createElement("h3");
      heading.textContent=`${item.route_id} · ${item.issue_hint} · ${item.capture_method}`;
      const question=document.createElement("p");
      question.textContent=`Question: ${item.question_text||"unmapped historical prompt"}`;
      const comment=document.createElement("blockquote");
      comment.textContent=item.feedback_text+(item.feedback_truncated?" [excerpt]":"");
      const origin=document.createElement("small");
      origin.textContent=`Source: ${item.source_type} · Turn: ${item.turn_id}`;
      const disposition=document.createElement("select");
      for(const [code,label] of [["new","New"],["triaging","Investigating"],["revision_proposed","Revision proposed"],["resolved","Resolved"],["dismissed","Dismissed"]]){
        const option=document.createElement("option");option.value=code;option.textContent=label;
        if(item.status===code)option.selected=true;disposition.append(option);
      }
      const revision=document.createElement("input");
      revision.placeholder="Proposed question-version ID (when applicable)";
      revision.value=item.revision_id||"";revision.maxLength=120;
      const save=document.createElement("button");save.textContent="Save review status";save.className="secondary";
      save.onclick=async()=>{
        try{
          await request(`/api/admin/question-feedback/${encodeURIComponent(item.feedback_id)}/disposition`,{status:disposition.value,revision_id:revision.value});
          await refreshQuestionFeedback();
        }catch(error){el("status").textContent=error.message;}
      };
      article.append(heading,question,comment,origin,disposition,revision,save);
      target.append(article);
    });
    if(!result.total)target.textContent="No consenting records with identified question feedback yet.";
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
