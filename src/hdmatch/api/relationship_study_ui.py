"""Confirmatory participant UI layered over the direct-OpenAI questionnaire UI."""

from __future__ import annotations

from hdmatch.api.relationship_openai_ui import HTML as BASE_HTML


def _replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise RuntimeError(f"expected study UI fragment not found: {old[:100]!r}")
    return text.replace(old, new, 1)


HTML = BASE_HTML
HTML = _replace_once(
    HTML,
    ".consent-line{display:block;margin:9px 0}\n</style>",
    (
        ".consent-line{display:block;margin:9px 0}.birth-panel{bo"
        "rder:1px solid #ddd;border-radius:10px;padding:14px;marg"
        "in:14px 0}.birth-panel input,.birth-panel select{padding"
        ":7px;margin:4px 5px 8px 0;max-width:100%}.birth-panel in"
        "put[type=text],.birth-panel input[type=email]{width:min("
        "480px,100%);box-sizing:border-box}.birth-time-group{disp"
        "lay:flex;align-items:center;gap:5px;margin:4px 0 2px}.bi"
        "rth-time-group label{display:flex;flex-direction:column;"
        "gap:2px}.birth-time-box{width:3.5rem!important;text-alig"
        "n:center}.birth-time-separator{font-size:1.4rem;margin-t"
        "op:17px}.field-error{color:#a40000;font-weight:600;margi"
        "n:2px 0 8px}.place-results button{display:block;text-ali"
        "gn:left;width:100%;margin:6px 0;padding:8px}.study-statu"
        "s{padding:10px;margin:10px 0;background:#f6f6f6}.result-"
        "axis{border-top:1px solid #ddd;padding:10px 0}.technical"
        "{margin-top:16px;color:#555}\n</style>"
    ),
)
HTML = _replace_once(
    HTML,
    '<div id="start" class="card">\n'
    '<div id="llmStatus" class="notice">Checking AI auditor…</div>\n'
    '<label class="consent-line"><input id="storageConsent" t'
    'ype="checkbox"> I consent to storing these responses pri'
    "vately for this research session.</label>\n"
    '<label class="consent-line"><input id="llmConsent" type='
    '"checkbox"> I consent to these questionnaire answers bei'
    "ng sent to OpenAI's API for answer-quality and clarifica"
    "tion analysis. Birth/chart data and Astro/HD predictions"
    " are not sent to this auditor.</label>\n"
    '<button id="beginButton" onclick="begin()" disabled>Begin</button>\n'
    "</div>",
    '<div id="start" class="card">\n'
    "<h2>Start with the birth data</h2>\n"
    "<p>The astrology/Human Design prediction is calculated a"
    "nd cryptographically sealed <strong>before</strong> you "
    "answer anything about the relationship. The questionnair"
    "e AI never sees the birth data or hidden prediction.</p>"
    "\n"
    '<div id="llmStatus" class="notice">Checking AI auditor…</div>\n'
    '<label>Email for this study<br><input id="contactEmail" '
    'type="email" autocomplete="email" placeholder="you@examp'
    'le.com"></label>\n'
    '<p class="hint">We store the email privately for future '
    "result/recovery delivery. Email verification is not conn"
    "ected yet, so for this pilot the private resume credenti"
    "al is still stored in this browser.</p>\n"
    '<div class="birth-panel"><h3>You</h3>\n'
    '<label>Birth date <input id="aBirthDate" type="date"></label><br>\n'
    '<label><input id="aUnknownTime" type="checkbox" onchange'
    "=\"toggleUnknownTime('a')\"> Birth time unknown</label><br"
    ">\n"
    '<div class="birth-time-group" role="group" aria-label="Y'
    'our birth time in 24-hour format"><label>Hour (00–23)<in'
    'put class="birth-time-box" id="aBirthHour" type="text" i'
    'nputmode="numeric" pattern="[0-9]*" maxlength="2" autoco'
    'mplete="off" aria-describedby="aBirthTimeError" oninput='
    '"clearBirthTimeError(\'a\')"></label><span class="birth-ti'
    'me-separator">:</span><label>Minute (00–59)<input class='
    '"birth-time-box" id="aBirthMinute" type="text" inputmode'
    '="numeric" pattern="[0-9]*" maxlength="2" autocomplete="'
    'off" aria-describedby="aBirthTimeError" oninput="clearBi'
    "rthTimeError('a')\"></label><span class=\"birth-time-separ"
    'ator">:</span><label>Second (optional)<input class="birt'
    'h-time-box" id="aBirthSecond" type="text" inputmode="num'
    'eric" pattern="[0-9]*" maxlength="2" autocomplete="off" '
    'placeholder="00" aria-describedby="aBirthTimeError" onin'
    'put="clearBirthTimeError(\'a\')"></label></div><p id="aBir'
    'thTimeError" class="field-error hidden" role="alert" ari'
    'a-live="polite"></p>\n'
    '<label>Time source <select id="aTimeSource"><option valu'
    'e="birth_certificate">Birth certificate</option><option '
    'value="hospital_record">Hospital record</option><option '
    'value="parent_or_family_memory">Parent/family memory</op'
    'tion><option value="personal_memory">Personal memory</op'
    'tion><option value="estimated">Estimated</option></selec'
    "t></label><br>\n"
    '<label>Birthplace <input id="aPlaceQuery" type="text" pl'
    'aceholder="City, region, country"></label><button type="'
    'button" onclick="searchPlace(\'a\')">Search birthplace</bu'
    'tton><div id="aPlaceChosen" class="hint"></div><div id="'
    'aPlaceResults" class="place-results"></div></div>\n'
    '<div class="birth-panel"><h3>The other person</h3>\n'
    '<label>Birth date <input id="bBirthDate" type="date"></label><br>\n'
    '<label><input id="bUnknownTime" type="checkbox" onchange'
    "=\"toggleUnknownTime('b')\"> Birth time unknown</label><br"
    ">\n"
    '<div class="birth-time-group" role="group" aria-label="T'
    "he other person's birth time in 24-hour format\"><label>H"
    'our (00–23)<input class="birth-time-box" id="bBirthHour"'
    ' type="text" inputmode="numeric" pattern="[0-9]*" maxlen'
    'gth="2" autocomplete="off" aria-describedby="bBirthTimeE'
    'rror" oninput="clearBirthTimeError(\'b\')"></label><span c'
    'lass="birth-time-separator">:</span><label>Minute (00–59'
    ')<input class="birth-time-box" id="bBirthMinute" type="t'
    'ext" inputmode="numeric" pattern="[0-9]*" maxlength="2" '
    'autocomplete="off" aria-describedby="bBirthTimeError" on'
    'input="clearBirthTimeError(\'b\')"></label><span class="bi'
    'rth-time-separator">:</span><label>Second (optional)<inp'
    'ut class="birth-time-box" id="bBirthSecond" type="text" '
    'inputmode="numeric" pattern="[0-9]*" maxlength="2" autoc'
    'omplete="off" placeholder="00" aria-describedby="bBirthT'
    'imeError" oninput="clearBirthTimeError(\'b\')"></label></d'
    'iv><p id="bBirthTimeError" class="field-error hidden" ro'
    'le="alert" aria-live="polite"></p>\n'
    '<label>Time source <select id="bTimeSource"><option valu'
    'e="birth_certificate">Birth certificate</option><option '
    'value="hospital_record">Hospital record</option><option '
    'value="parent_or_family_memory">Parent/family memory</op'
    'tion><option value="personal_memory">Personal memory</op'
    'tion><option value="estimated">Estimated</option></selec'
    "t></label><br>\n"
    '<label>Birthplace <input id="bPlaceQuery" type="text" pl'
    'aceholder="City, region, country"></label><button type="'
    'button" onclick="searchPlace(\'b\')">Search birthplace</bu'
    'tton><div id="bPlaceChosen" class="hint"></div><div id="'
    'bPlaceResults" class="place-results"></div></div>\n'
    '<p class="hint">Birthplace search sends only the place t'
    "ext to OpenStreetMap Nominatim. Email, birth date/time, "
    "relationship answers, and hidden predictions are not sen"
    "t to the geocoder. Choose the correct result rather than"
    " relying on an automatic guess.</p>\n"
    '<label class="consent-line"><input id="storageConsent" t'
    'ype="checkbox"> I consent to storing my email, birth dat'
    "a, and relationship responses privately for this researc"
    "h session.</label>\n"
    '<label class="consent-line"><input id="partnerConsent" t'
    'ype="checkbox"> I consent to this study processing the o'
    "ther person's birth data for the relationship calculatio"
    "n.</label>\n"
    '<label class="consent-line"><input id="llmConsent" type='
    '"checkbox"> I consent to my questionnaire answers being '
    "sent to OpenAI's API for answer-quality and clarificatio"
    "n analysis. Birth/chart data and Astro/HD predictions ar"
    "e not sent to this auditor.</label>\n"
    '<div id="studyStatus" class="study-status hidden"></div>'
    '<button id="beginButton" onclick="beginStudy()" disabled'
    ">Seal prediction &amp; begin questionnaire</button>\n"
    "</div>",
)
HTML = _replace_once(
    HTML,
    (
        '<div id="done" class="card hidden"><h2>Responses frozen<'
        '/h2><p id="doneText">Your answers are sealed.</p><p clas'
        's="receipt" id="digest"></p><div id="addendumBox" class='
        '"hidden"><div class="notice">This run was frozen before '
        "the LLM auditor reviewed it. The original receipt will r"
        'emain unchanged.</div><label class="consent-line"><input'
        ' id="addendumConsent" type="checkbox"> I consent to send'
        "ing this frozen survey's questionnaire answers to OpenAI"
        "'s API for a separate LLM audit addendum.</label><button"
        ' id="addendumButton" onclick="startLLMAddendum()">Run LL'
        "M audit addendum</button></div></div>"
    ),
    (
        '<div id="done" class="card hidden"><h2>Responses frozen<'
        '/h2><p id="doneText">Your answers are sealed.</p><div id'
        '="studyResults" class="hidden"><h2>Your relationship fin'
        'gerprint</h2><div id="fingerprint"></div><button id="rev'
        'ealButton" onclick="revealStudy()">Reveal the blinded As'
        'tro/HD prediction</button><div id="predictionReveal" cla'
        'ss="hidden"></div></div><details class="technical"><summ'
        "ary>Technical audit receipt</summary><p>You do not need "
        "to save this hash. It is provenance showing exactly whic"
        'h frozen record was used.</p><p class="receipt" id="dige'
        'st"></p></details><div id="addendumBox" class="hidden"><'
        'div class="notice">This run was frozen before the LLM au'
        "ditor reviewed it. The original receipt will remain unch"
        'anged.</div><label class="consent-line"><input id="adden'
        'dumConsent" type="checkbox"> I consent to sending this f'
        "rozen survey's questionnaire answers to OpenAI's API for"
        ' a separate LLM audit addendum.</label><button id="adden'
        'dumButton" onclick="startLLMAddendum()">Run LLM audit ad'
        "dendum</button></div></div>"
    ),
)
HTML = _replace_once(
    HTML,
    "let llmConfigured=false;",
    (
        "let llmConfigured=false;let isStudySession=false;let sel"
        "ectedPlaces={a:null,b:null};let placeCandidates={a:[],b:"
        "[]};"
    ),
)
_old_begin = (
    "async function begin(){if(!document.getElementById('stor"
    "ageConsent').checked||!document.getElementById('llmConse"
    "nt').checked)return alert('Both storage and LLM-processi"
    "ng consent are required.');const r=await fetch('/api/ada"
    "ptive/sessions',{method:'POST',headers:{'content-type':'"
    "application/json'},body:JSON.stringify({consent_to_store"
    "_responses:true,consent_to_llm_processing:true})});const"
    " d=await r.json();if(!r.ok)return alert(d.detail||'Could"
    " not start');sessionId=d.session_id;token=d.resume_token"
    ";localStorage.setItem('rr_session',sessionId);localStora"
    "ge.setItem('rr_token',token);setProgress(d.progress);sho"
    "wQuestion(d.next_question)}"
)
_new_begin = (
    "const apiFieldLabels={respondent_birth:'Your birth data'"
    ',partner_birth:"The other person\'s birth data",contact_e'
    "mail:'Email',birth_date:'Birth date',local_time:'Birth t"
    "ime',birthplace:'Birthplace',iana_timezone:'Timezone',ti"
    "me_source:'Time source',uncertainty_minutes:'Birth-time "
    "uncertainty',latitude:'Birthplace latitude',longitude:'B"
    "irthplace longitude'};\nfunction apiErrorMessage(problem,"
    "fallback){if(problem&&typeof problem==='object'&&!Array."
    "isArray(problem)&&problem.error)problem=problem.error;if"
    "(problem&&typeof problem==='object'&&!Array.isArray(prob"
    "lem)&&problem.detail!==undefined)problem=problem.detail;"
    "if(typeof problem==='string'&&problem.trim())return prob"
    "lem.trim();const errors=Array.isArray(problem)?problem:["
    "problem];const messages=errors.map(item=>{if(typeof item"
    "==='string')return item.trim();if(!item||typeof item!=='"
    "object')return '';const path=(Array.isArray(item.loc)?it"
    "em.loc:[]).filter(part=>part!=='body'&&part!=='intake')."
    "map(part=>apiFieldLabels[String(part)]||String(part).rep"
    "laceAll('_',' '));const message=typeof item.msg==='strin"
    "g'?item.msg:(typeof item.message==='string'?item.message"
    ":'');return (path.length?path.join(' — ')+': ':'')+messa"
    "ge}).filter(Boolean);return messages.join(' ')||fallback"
    "}\nfunction clearBirthTimeError(role){const error=documen"
    "t.getElementById(role+'BirthTimeError');error.textConten"
    "t='';error.classList.add('hidden')}\nfunction failBirthTi"
    "me(role,message,suffix){const error=document.getElementB"
    "yId(role+'BirthTimeError');error.textContent=message;err"
    "or.classList.remove('hidden');document.getElementById(ro"
    "le+suffix).focus();throw new Error(message)}\nfunction re"
    "adBirthTime(role){const who=role==='a'?'your':\"the other"
    " person's\";const hourText=document.getElementById(role+'"
    "BirthHour').value.trim();const minuteText=document.getEl"
    "ementById(role+'BirthMinute').value.trim();const secondT"
    "ext=document.getElementById(role+'BirthSecond').value.tr"
    "im();if(!hourText&&!minuteText&&!secondText)return failB"
    "irthTime(role,'Enter '+who+' birth hour and minute, or m"
    "ark the time unknown.','BirthHour');if(!/^\\d{1,2}$/.test"
    "(hourText))return failBirthTime(role,'Enter '+who+' birt"
    "h hour as a number from 00 to 23.','BirthHour');if(!/^\\d"
    "{1,2}$/.test(minuteText))return failBirthTime(role,'Ente"
    "r '+who+' birth minute as a number from 00 to 59.','Birt"
    "hMinute');if(secondText&&!/^\\d{1,2}$/.test(secondText))r"
    "eturn failBirthTime(role,'Enter '+who+' birth second as "
    "a number from 00 to 59, or leave it blank.','BirthSecond"
    "');const hour=Number(hourText);const minute=Number(minut"
    "eText);const second=secondText?Number(secondText):0;if(h"
    "our>23)return failBirthTime(role,'Enter '+who+' birth ho"
    "ur from 00 to 23.','BirthHour');if(minute>59)return fail"
    "BirthTime(role,'Enter '+who+' birth minute from 00 to 59"
    ".','BirthMinute');if(second>59)return failBirthTime(role"
    ",'Enter '+who+' birth second from 00 to 59, or leave it "
    "blank.','BirthSecond');clearBirthTimeError(role);return "
    "String(hour).padStart(2,'0')+':'+String(minute).padStart"
    "(2,'0')+':'+String(second).padStart(2,'0')}\nfunction tog"
    "gleUnknownTime(role){const unknown=document.getElementBy"
    "Id(role+'UnknownTime').checked;document.getElementById(r"
    "ole+'BirthHour').disabled=unknown;document.getElementByI"
    "d(role+'BirthMinute').disabled=unknown;document.getEleme"
    "ntById(role+'BirthSecond').disabled=unknown;document.get"
    "ElementById(role+'TimeSource').disabled=unknown;clearBir"
    "thTimeError(role)}\nasync function searchPlace(role){cons"
    "t q=document.getElementById(role+'PlaceQuery').value.tri"
    "m();if(q.length<2)return alert('Enter a city/place to se"
    "arch.');const box=document.getElementById(role+'PlaceRes"
    "ults');box.textContent='Searching…';try{const r=await fe"
    "tch('/api/study/places?q='+encodeURIComponent(q));const "
    "d=await r.json();if(!r.ok){box.textContent=apiErrorMessa"
    "ge(d,'Birthplace search failed.');return}placeCandidates"
    "[role]=d.candidates||[];if(!placeCandidates[role].length"
    "){box.textContent='No matches. Add region/country and tr"
    "y again.';return}box.innerHTML=placeCandidates[role].map"
    "((p,i)=>'<button type=\"button\" onclick=\"choosePlace(\\''+"
    "role+'\\','+i+')\">'+esc(p.display_name)+' · '+esc(p.iana_"
    "timezone)+'</button>').join('')}catch(e){box.textContent"
    "='Birthplace search failed.'}}\nfunction choosePlace(role"
    ",index){const p=placeCandidates[role][index];selectedPla"
    "ces[role]=p;document.getElementById(role+'PlaceChosen')."
    "textContent='Selected: '+p.display_name+' · '+p.iana_tim"
    "ezone;document.getElementById(role+'PlaceResults').inner"
    "HTML=''}\nfunction requireBirthField(role,suffix,message)"
    "{const field=document.getElementById(role+suffix);field."
    "focus();throw new Error(message)}\nfunction birthPayload("
    "role){const who=role==='a'?'your':\"the other person's\";c"
    "onst date=document.getElementById(role+'BirthDate').valu"
    "e;const unknown=document.getElementById(role+'UnknownTim"
    "e').checked;const place=selectedPlaces[role];if(!date)re"
    "quireBirthField(role,'BirthDate','Enter '+who+' birth da"
    "te.');const time=unknown?null:readBirthTime(role);if(!pl"
    "ace)requireBirthField(role,'PlaceQuery','Search and sele"
    "ct '+who+' birthplace.');return {birth_date:date,local_t"
    "ime:time,birthplace:place.display_name,iana_timezone:pla"
    "ce.iana_timezone,time_source:unknown?'unknown':document."
    "getElementById(role+'TimeSource').value,uncertainty_minu"
    "tes:null,latitude:place.latitude,longitude:place.longitu"
    "de}}\nasync function beginStudy(){if(!llmConfigured)retur"
    "n alert('AI auditor is not ready.');const email=document"
    ".getElementById('contactEmail').value.trim();if(!email)r"
    "eturn alert('Enter your email.');if(!document.getElement"
    "ById('storageConsent').checked||!document.getElementById"
    "('partnerConsent').checked||!document.getElementById('ll"
    "mConsent').checked)return alert('All three study consent"
    "s are required.');let a,b;try{a=birthPayload('a');b=birt"
    "hPayload('b')}catch(e){return alert(e.message)}const but"
    "ton=document.getElementById('beginButton');button.disabl"
    "ed=true;button.textContent='Sealing hidden prediction…';"
    "const status=document.getElementById('studyStatus');stat"
    "us.classList.remove('hidden');status.textContent='Calcul"
    "ating and freezing the pre-answer Astro/HD record. No re"
    "lationship answer has been submitted yet.';try{const r=a"
    "wait fetch('/api/study/intake',{method:'POST',headers:{'"
    "content-type':'application/json'},body:JSON.stringify({i"
    "ntake:{contact_email:email,respondent_birth:a,partner_bi"
    "rth:b,consent_to_store_private_research_data:true,consen"
    "t_to_process_partner_birth_data:true,created_at_utc:new "
    "Date().toISOString()},consent_to_llm_processing:true})})"
    ";const d=await r.json();if(!r.ok){status.textContent=api"
    "ErrorMessage(d,'Could not save study intake.');button.di"
    "sabled=false;button.textContent='Seal prediction & begin"
    " questionnaire';return}sessionId=d.session_id;token=d.re"
    "sume_token;isStudySession=true;localStorage.setItem('rr_"
    "session',sessionId);localStorage.setItem('rr_token',toke"
    "n);if(!d.preflight.confirmatory_ready){status.textConten"
    "t=d.participant_message+' Prediction status: '+JSON.stri"
    "ngify(d.preflight.prediction_layer_statuses);button.text"
    "Content='Prediction not ready';return}const state=await "
    "loadState();coreProgress(state.answers.length);if(state."
    "next_question)showQuestion(state.next_question);else sta"
    "rtAudit()}catch(e){status.textContent='Could not initial"
    "ize the study.';button.disabled=false;button.textContent"
    "='Seal prediction & begin questionnaire'}}"
)
HTML = _replace_once(HTML, _old_begin, _new_begin)
_old_freeze = (
    "async function freezeCurrent(){const r=await fetch('/api"
    "/adaptive/sessions/'+sessionId+'/freeze',{method:'POST',"
    "headers:{'content-type':'application/json'},body:JSON.st"
    "ringify({token})});const d=await r.json();if(!r.ok)retur"
    "n alert(d.detail||'Could not freeze');showDone(d.freeze_"
    "sha256,false,false)}"
)
_new_freeze = (
    "async function freezeCurrent(){const r=await fetch('/api"
    "/adaptive/sessions/'+sessionId+'/freeze',{method:'POST',"
    "headers:{'content-type':'application/json'},body:JSON.st"
    "ringify({token})});const d=await r.json();if(!r.ok)retur"
    "n alert(d.detail||'Could not freeze');showDone(d.freeze_"
    "sha256,false,false);if(isStudySession)finishStudyAfterFr"
    "eeze()}\nasync function finishStudyAfterFreeze(){document"
    ".getElementById('doneText').textContent='Your answers ar"
    "e sealed. Building the chart-blind relationship fingerpr"
    "int…';const r=await fetch('/api/study/sessions/'+session"
    "Id+'/phenotype-freeze',{method:'POST',headers:{'content-"
    "type':'application/json'},body:JSON.stringify({token})})"
    ";const d=await r.json();if(!r.ok){document.getElementByI"
    "d('doneText').textContent=d.detail||'Phenotype classific"
    "ation failed; the answers remain safely frozen.';return}"
    "const f=await fetch('/api/study/sessions/'+sessionId+'/f"
    "ingerprint?token='+encodeURIComponent(token));const fp=a"
    "wait f.json();if(!f.ok){document.getElementById('doneTex"
    "t').textContent=fp.detail||'Fingerprint is unavailable.'"
    ";return}renderFingerprint(fp);document.getElementById('s"
    "tudyResults').classList.remove('hidden');document.getEle"
    "mentById('doneText').textContent='Your chart-blind relat"
    "ionship fingerprint is sealed. You can now reveal what t"
    "he pre-answer Astro/HD system actually predicted.'}\nfunc"
    "tion renderFingerprint(fp){const rows=(fp.classified_axe"
    "s||[]).map(a=>'<div class=\"result-axis\"><strong>'+esc(a."
    "axis_id.replaceAll('_',' '))+'</strong> · '+esc(a.direct"
    "ion)+' · <strong>'+esc(a.value||a.status)+'</strong>'+(a"
    ".trajectory&&a.trajectory!=='unknown'?' · '+esc(a.trajec"
    "tory):'')+'<div class=\"hint\">'+esc(a.definition||'')+'</"
    "div></div>').join('');const unresolved=(fp.unresolved_or"
    "_mixed_axes||[]).length;document.getElementById('fingerp"
    "rint').innerHTML=(rows||'<p>No axes met the frozen evide"
    "nce/confidence threshold.</p>')+(unresolved?'<p class=\"h"
    "int\">'+unresolved+' additional axes remain mixed, contex"
    "t-dependent, or insufficiently observed.</p>':'')}\nasync"
    " function revealStudy(){const b=document.getElementById("
    "'revealButton');b.disabled=true;b.textContent='Revealing"
    " frozen prediction…';const r=await fetch('/api/study/ses"
    "sions/'+sessionId+'/reveal',{method:'POST',headers:{'con"
    "tent-type':'application/json'},body:JSON.stringify({toke"
    "n})});const d=await r.json();if(!r.ok){b.disabled=false;"
    "b.textContent='Reveal the blinded Astro/HD prediction';r"
    "eturn alert(d.detail||'Reveal failed')}const target=docu"
    "ment.getElementById('predictionReveal');target.classList"
    ".remove('hidden');target.innerHTML=renderPrediction(d.pr"
    "ediction_reveal);b.classList.add('hidden')}\nfunction ren"
    "derPrediction(p){let html='<h2>What was frozen before yo"
    "ur answers</h2>';for(const layer of (p.layers||[])){html"
    "+='<div class=\"card\"><h3>'+esc(layer.layer_id.replaceAll"
    "('_',' '))+'</h3><p>'+esc(layer.explanation||layer.outco"
    "me_comparison_status)+'</p>';if(layer.layer_id==='human_"
    "design_connection_v1'&&layer.preanswer_payload&&layer.pr"
    "eanswer_payload.connection){const c=layer.preanswer_payl"
    "oad.connection;html+='<p><strong>Connection mechanics:</"
    "strong> '+esc(c.center_configuration||'')+' · '+esc(c.co"
    "mposite_definition||'')+'</p>';if(c.channels)html+='<p c"
    'lass="hint">Channels: \'+esc(c.channels.map(x=>x.channel+'
    "' ('+x.kind+')').join(', '))+'</p>'}if(layer.layer_id==="
    "'astro_rrf_directional_v0_4'&&layer.preanswer_payload&&l"
    "ayer.preanswer_payload.v0_1_raw_scoring){html+='<p><stro"
    "ng>Frozen directional raw signals:</strong></p><ul>'+lay"
    "er.preanswer_payload.v0_1_raw_scoring.directional_scores"
    ".map(x=>'<li>'+esc(x.actor.toUpperCase()+' · '+x.axis.re"
    "placeAll('_',' ')+' = '+x.score)+'</li>').join('')+'</ul"
    ">'}html+='</div>'}if(!p.formal_hit_miss_summary)html+='<"
    'div class="notice"><strong>Why there is not a hit/miss p'
    "ercentage yet:</strong> the raw relationship signals wer"
    "e frozen before your answers, but the ordinal calibratio"
    "n needed to call those scores high/low is not yet frozen"
    ". The study will not invent that threshold after seeing "
    "your relationship.</div>';return html}"
)
HTML = _replace_once(HTML, _old_freeze, _new_freeze)
_old_show_done = (
    "function showDone(receipt,isAddendum,canAddendum){hideAl"
    "l();document.getElementById('progressWrap').classList.ad"
    "d('hidden');document.getElementById('done').classList.re"
    "move('hidden');document.getElementById('doneText').textC"
    "ontent=isAddendum?'Your LLM audit addendum is frozen sep"
    "arately from the original response.':'Your answers are s"
    "ealed.';document.getElementById('digest').textContent=(i"
    "sAddendum?'LLM addendum freeze receipt: ':'Freeze receip"
    "t: ')+receipt;document.getElementById('addendumBox').cla"
    "ssList.toggle('hidden',!canAddendum)}"
)
_new_show_done = (
    "function showDone(receipt,isAddendum,canAddendum){hideAl"
    "l();document.getElementById('progressWrap').classList.ad"
    "d('hidden');document.getElementById('done').classList.re"
    "move('hidden');document.getElementById('doneText').textC"
    "ontent=isAddendum?'Your LLM audit addendum is frozen sep"
    "arately from the original response.':'Your answers are s"
    "ealed.';document.getElementById('digest').textContent=re"
    "ceipt;document.getElementById('addendumBox').classList.t"
    "oggle('hidden',!canAddendum)}"
)
HTML = _replace_once(HTML, _old_show_done, _new_show_done)
_old_resume = (
    "async function resume(){if(!(sessionId&&token))return;tr"
    "y{const d=await loadState();if(d.status==='frozen'){if(d"
    ".llm_addendum&&d.llm_addendum.status==='in_progress'){au"
    "ditMode='addendum';setProgress(d.llm_addendum.progress);"
    "if(d.llm_addendum.next_clarification)showAuditQuestion(d"
    ".llm_addendum.next_clarification);else loadAddendumRevie"
    "w(d.llm_addendum);return}if(d.llm_addendum&&d.llm_addend"
    "um.status==='frozen'){showDone(d.llm_addendum.freeze_sha"
    "256,true,false);return}showDone(d.freeze_sha256,false,d."
    "can_start_llm_addendum);return}coreProgress(d.answers.le"
    "ngth);if(d.next_question)showQuestion(d.next_question);e"
    "lse if(d.semantic_audit&&d.semantic_audit.next_clarifica"
    "tion){auditMode='core';setProgress(d.semantic_audit.prog"
    "ress);showAuditQuestion(d.semantic_audit.next_clarificat"
    "ion)}else if(d.semantic_audit)loadReview(d.semantic_audi"
    "t);else startAudit()}catch(e){}}"
)
_new_resume = (
    "async function resume(){if(!(sessionId&&token))return;tr"
    "y{const pre=await fetch('/api/study/sessions/'+sessionId"
    "+'/preflight?token='+encodeURIComponent(token));if(pre.o"
    "k){isStudySession=true;const pf=await pre.json();if(!pf."
    "confirmatory_ready){hideAll();document.getElementById('s"
    "tart').classList.remove('hidden');const s=document.getEl"
    "ementById('studyStatus');s.classList.remove('hidden');s."
    "textContent='This study intake is saved, but the hidden "
    "prediction is not yet complete. No relationship question"
    "s are unlocked. Prediction status: '+JSON.stringify(pf.p"
    "rediction_layer_statuses);return}}const d=await loadStat"
    "e();if(d.status==='frozen'){if(isStudySession){showDone("
    "d.freeze_sha256,false,false);await finishStudyAfterFreez"
    "e();return}if(d.llm_addendum&&d.llm_addendum.status==='i"
    "n_progress'){auditMode='addendum';setProgress(d.llm_adde"
    "ndum.progress);if(d.llm_addendum.next_clarification)show"
    "AuditQuestion(d.llm_addendum.next_clarification);else lo"
    "adAddendumReview(d.llm_addendum);return}if(d.llm_addendu"
    "m&&d.llm_addendum.status==='frozen'){showDone(d.llm_adde"
    "ndum.freeze_sha256,true,false);return}showDone(d.freeze_"
    "sha256,false,d.can_start_llm_addendum);return}coreProgre"
    "ss(d.answers.length);if(d.next_question)showQuestion(d.n"
    "ext_question);else if(d.semantic_audit&&d.semantic_audit"
    ".next_clarification){auditMode='core';setProgress(d.sema"
    "ntic_audit.progress);showAuditQuestion(d.semantic_audit."
    "next_clarification)}else if(d.semantic_audit)loadReview("
    "d.semantic_audit);else startAudit()}catch(e){}}"
)
HTML = _replace_once(HTML, _old_resume, _new_resume)
