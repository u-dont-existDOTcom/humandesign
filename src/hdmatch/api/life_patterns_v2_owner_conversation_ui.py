"""Owner-facing conversational UI for the hidden-ledger Life Patterns v2 probe."""

HTML = (
    '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="u'
    'tf-8">\n<meta name="viewport" content="width=device-width'
    ',initial-scale=1">\n<title>Discover Your Unique Life Patt'
    "erns — owner conversation</title>\n<style>\n:root{--ink:#2"
    "0242a;--muted:#667085;--line:#d0d5dd;--soft:#f7f8fa;--ac"
    "cent:#315c5f;--user:#eef6f6;--ai:#f7f3eb;--good:#176b44;"
    "--bad:#a61b1b}\n*{box-sizing:border-box}\nbody{margin:0;ba"
    "ckground:#fff;color:var(--ink);font:16px/1.55 system-ui,"
    '-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}\n'
    "main{width:min(58rem,calc(100% - 2rem));margin:2rem auto"
    " 5rem}\nh1{font-size:clamp(2rem,7vw,3.4rem);line-height:1"
    ".02;letter-spacing:-.04em;margin:.2rem 0 .7rem}\nh2{margi"
    "n:.2rem 0 .65rem}.lede{font-size:1.08rem;color:var(--mut"
    "ed);max-width:50rem}\n.card{border:1px solid var(--line);"
    "border-radius:1rem;padding:1.05rem;margin:1rem 0;backgro"
    "und:#fff}\n.soft{background:var(--soft)}.chat{display:gri"
    "d;gap:.8rem;margin:1.2rem 0}\n.bubble{padding:.9rem 1rem;"
    "border-radius:.85rem;max-width:94%;white-space:pre-wrap}"
    "\n.bubble.user{background:var(--user);margin-left:auto}.b"
    "ubble.ai{background:var(--ai)}\n.meta{font-size:.82rem;co"
    "lor:var(--muted);margin-bottom:.25rem}\n.pill{display:inl"
    "ine-block;font-size:.82rem;border:1px solid var(--line);"
    "border-radius:999px;padding:.25rem .6rem;color:var(--mut"
    "ed)}\ntextarea,button{font:inherit;border:1px solid #98a2"
    "b3;border-radius:.6rem;padding:.72rem .8rem}\ntextarea{wi"
    "dth:100%;min-height:7rem;resize:vertical}\nbutton{backgro"
    "und:var(--accent);border-color:var(--accent);color:#fff;"
    "font-weight:750;cursor:pointer}\nbutton.secondary{backgro"
    "und:#fff;color:var(--accent)}button.subtle{background:#f"
    "ff;color:var(--ink);border-color:var(--line)}\nbutton.dan"
    "ger{background:#fff;color:var(--bad);border-color:#e5a6a"
    "6}button:disabled{opacity:.5;cursor:not-allowed}\n.row{di"
    "splay:flex;gap:.65rem;flex-wrap:wrap;align-items:center}"
    ".hidden{display:none}\n.note{font-size:.92rem;color:var(-"
    "-muted)}.error{color:var(--bad)}\n.result{border-left:4px"
    " solid var(--accent);padding:.9rem 1rem;background:#f2f8"
    "f8;margin:1rem 0}\n.topbar{display:flex;justify-content:s"
    "pace-between;gap:1rem;align-items:center;flex-wrap:wrap}"
    "\n.count{font-size:.88rem;color:var(--muted)}.divider{bor"
    "der:0;border-top:1px solid var(--line);margin:1.1rem 0}\n"
    ".composer{position:sticky;bottom:0;background:rgba(255,2"
    "55,255,.96);backdrop-filter:blur(8px);padding:.8rem 0 .2"
    'rem}\n</style>\n</head>\n<body><main>\n<div class="topbar">\n'
    '  <div><span class="pill">Owner-only development · hidde'
    "n evidence ledger</span><h1>Discover Your Unique Life Pa"
    'tterns</h1></div>\n  <div id="sessionState" class="count"'
    '>Starting…</div>\n</div>\n<p class="lede">This version is '
    "meant to feel like a real conversation. The evidence boo"
    "kkeeping stays underneath. The interviewer should ask on"
    "ly questions that could change the picture, and should s"
    "urface a pattern only when it adds something beyond repe"
    'ating you.</p>\n<div class="card soft"><strong>What to ju'
    'dge</strong><p class="note">Does the conversation expose'
    " a distinction, contrast, boundary, or cross-situation p"
    "attern you did not simply hand it verbatim? If it mostly"
    " paraphrases you, this version fails too.</p></div>\n\n<di"
    'v id="configWarning" class="card hidden"><strong>AI runt'
    'ime is not configured.</strong><p class="note">The brows'
    "er surface is ready, but the runtime needs its configure"
    'd model credential.</p></div>\n\n<div id="conversation" cl'
    'ass="chat"></div>\n\n<div id="composer" class="composer">\n'
    '  <textarea id="message" placeholder="Answer in your own'
    ' words…"></textarea>\n  <div class="row"><button id="send'
    '">Send</button><span id="status" class="note"></span></d'
    'iv>\n</div>\n\n<div id="patternPanel" class="card hidden">\n'
    "  <h2>Does that synthesis actually fit?</h2>\n  <p class="
    '"note">This is the one place where your explicit judgmen'
    "t matters. The hidden episode facts are not being shown "
    'for routine approval.</p>\n  <div class="row">\n    <butto'
    'n id="accept">Yes — keep that</button>\n    <button id="r'
    'evise" class="secondary">Close, but change it</button>\n '
    '   <button id="reject" class="danger">No</button>\n    <b'
    'utton id="unresolved" class="subtle">I’m not sure</butto'
    'n>\n  </div>\n  <div id="reviseBox" class="hidden">\n    <h'
    'r class="divider">\n    <label for="revisedWording"><stro'
    "ng>What is the version that actually fits?</strong></lab"
    'el>\n    <textarea id="revisedWording" placeholder="Say i'
    't the way you mean it…"></textarea>\n    <p><strong>Do th'
    "e situations we actually discussed show that revised ver"
    'sion?</strong></p>\n    <div class="row">\n      <button c'
    'lass="secondary grounding" data-grounding="examples">Yes'
    ", these situations show it</button>\n      <button class="
    '"secondary grounding" data-grounding="other_situations">'
    "It comes from other situations</button>\n      <button cl"
    'ass="subtle grounding" data-grounding="unsure">I’m not s'
    'ure</button>\n    </div>\n    <div id="finalChoice" class='
    '"hidden">\n      <p><strong>Then should I keep the revise'
    "d version, reject it, or leave it open?</strong></p>\n   "
    '   <div class="row">\n        <button class="final" data-'
    'final="accept">Keep it</button>\n        <button class="d'
    'anger final" data-final="reject">Reject it</button>\n    '
    '    <button class="subtle final" data-final="unresolved"'
    ">Leave it open</button>\n      </div>\n    </div>\n  </div>"
    '\n  <p id="patternStatus" class="note"></p>\n</div>\n\n<div '
    'id="result" class="hidden result"></div>\n<div id="contin'
    'uation" class="hidden card">\n  <h2>Where next?</h2>\n  <p'
    ' class="note">You can explore another separate pattern t'
    "hread, or finish for now. This summary does not claim sc"
    'ientific completeness.</p>\n  <div class="row">\n    <butt'
    'on id="exploreAnother">Explore another pattern</button>\n'
    '    <button id="finishForNow" class="secondary">Finish f'
    'or now</button>\n    <button id="copyExport" class="subtl'
    'e">Copy interview summary</button>\n  </div>\n  <div id="s'
    'essionSummary" class="note hidden"></div>\n</div>\n\n<scrip'
    "t>\nlet sessionId=null;let groundingChoice=null;let compl"
    "etedResults=[];\nconst $=id=>document.getElementById(id);"
    "\nfunction show(id){$(id).classList.remove('hidden')}func"
    "tion hide(id){$(id).classList.add('hidden')}\nfunction se"
    "tStatus(text,error=false){$('status').textContent=text;$"
    "('status').className=error?'error':'note'}\nfunction esca"
    "peHtml(s){return String(s).replace(/[&<>\\\"]/g,c=>({'&':'"
    "&amp;','<':'&lt;','>':'&gt;','\\\"':'&quot;'}[c]))}\nfuncti"
    "on bubble(role,text){const el=document.createElement('di"
    "v');el.className='bubble '+role;el.innerHTML='<div class"
    "=\"meta\">'+(role==='user'?'You':'Interviewer')+'</div><di"
    "v>'+escapeHtml(text)+'</div>';$('conversation').append(e"
    "l);el.scrollIntoView({behavior:'smooth',block:'end'})}\na"
    "sync function api(path,options={}){const r=await fetch(p"
    "ath,{headers:{'content-type':'application/json',...(opti"
    "ons.headers||{})},...options});let p={};try{p=await r.js"
    "on()}catch{}if(!r.ok)throw new Error(p.detail||'Request "
    "failed');return p}\n\nasync function start(){\n  try{\n    c"
    "onst p=await api('/api/owner-v2/conversation/sessions',{"
    "method:'POST'});\n    sessionId=p.session_id;\n    $('sess"
    "ionState').textContent='Private conversational probe';\n "
    "   if(!p.model_configured)show('configWarning');\n    bub"
    "ble('ai',p.opening);\n    $('message').focus();\n  }catch("
    "e){$('sessionState').textContent='Could not start';setSt"
    "atus(e.message,true)}\n}\n\nasync function startFreshPatter"
    "n(){\n  const p=await api('/api/owner-v2/conversation/ses"
    "sions',{method:'POST'});\n  sessionId=p.session_id;ground"
    "ingChoice=null;\n  $('sessionState').textContent='Private"
    " conversational probe · new pattern thread';\n  hide('res"
    "ult');hide('continuation');hide('patternPanel');show('co"
    "mposer');\n  $('message').value='';bubble('ai',p.opening)"
    ";$('message').focus();\n}\n\n$('send').onclick=send;\n$('mes"
    "sage').addEventListener('keydown',e=>{if(e.key==='Enter'"
    "&&(e.ctrlKey||e.metaKey))send()});\nasync function send()"
    "{\n  const text=$('message').value.trim();\n  if(!text||!s"
    "essionId)return;\n  bubble('user',text);\n  $('message').v"
    "alue='';\n  $('send').disabled=true;\n  setStatus('Thinkin"
    "g…');\n  try{\n    const p=await api(`/api/owner-v2/conver"
    "sation/sessions/${encodeURIComponent(sessionId)}/turns`,"
    "{method:'POST',body:JSON.stringify({message:text})});\n  "
    "  bubble('ai',p.reply);\n    setStatus('');\n    if(p.patt"
    "ern_active){\n      hide('composer');\n      show('pattern"
    "Panel');\n      $('patternPanel').scrollIntoView({behavio"
    "r:'smooth'});\n    }\n  }catch(e){setStatus(e.message,true"
    ")}\n  finally{$('send').disabled=false}\n}\n\nasync function"
    " decision(decision){\n  try{\n    const p=await api(`/api/"
    "owner-v2/conversation/sessions/${encodeURIComponent(sess"
    "ionId)}/patterns/adjudicate`,{method:'POST',body:JSON.st"
    "ringify({decision})});\n    renderResult(p);\n  }catch(e){"
    "$('patternStatus').textContent=e.message;$('patternStatu"
    "s').className='error'}\n}\n$('accept').onclick=()=>decisio"
    "n('accept');\n$('reject').onclick=()=>decision('reject');"
    "\n$('unresolved').onclick=()=>decision('unresolved');\n$('"
    "revise').onclick=()=>show('reviseBox');\n\ndocument.queryS"
    "electorAll('.grounding').forEach(btn=>btn.onclick=()=>{\n"
    "  const wording=$('revisedWording').value.trim();\n  if(!"
    "wording){$('patternStatus').textContent='Write the versi"
    "on that fits first.';$('patternStatus').className='error"
    "';return}\n  groundingChoice=btn.dataset.grounding;\n  doc"
    "ument.querySelectorAll('.grounding').forEach(b=>b.disabl"
    "ed=true);\n  if(groundingChoice==='examples')show('finalC"
    "hoice');else submitRevision(null);\n});\ndocument.querySel"
    "ectorAll('.final').forEach(btn=>btn.onclick=()=>submitRe"
    "vision(btn.dataset.final));\n\nasync function submitRevisi"
    "on(finalDecision){\n  const wording=$('revisedWording').v"
    "alue.trim();\n  if(!wording)return;\n  try{\n    const p=aw"
    "ait api(`/api/owner-v2/conversation/sessions/${encodeURI"
    "Component(sessionId)}/patterns/adjudicate`,{\n      metho"
    "d:'POST',\n      body:JSON.stringify({decision:'revise',r"
    "evised_wording:wording,grounding_source:groundingChoice,"
    "final_decision:finalDecision})\n    });\n    renderResult("
    "p);\n  }catch(e){$('patternStatus').textContent=e.message"
    ";$('patternStatus').className='error'}\n}\n\nfunction rende"
    "rResult(p){\n  hide('patternPanel');\n  let title=p.status"
    "==='accepted'?'Working pattern kept':p.status==='rejecte"
    "d'?'Pattern rejected':'Pattern left open';\n  let body=''"
    ";\n  if(p.wording)body+='<p><strong>'+escapeHtml(p.wordin"
    "g)+'</strong></p>';\n  if(p.message)body+='<p>'+escapeHtm"
    "l(p.message)+'</p>';\n  body+='<p class=\"note\">This threa"
    "d is complete. You can continue with another pattern or "
    "finish for now.</p>';\n  $('result').innerHTML='<div clas"
    "s=\"meta\">Current result</div><h2>'+title+'</h2>'+body;\n "
    " completedResults.push({status:p.status,wording:p.wordin"
    "g||null});\n  show('result');\n  show('continuation');\n  $"
    "('result').scrollIntoView({behavior:'smooth'});\n}\n\n$('ex"
    "ploreAnother').onclick=async()=>{try{await startFreshPat"
    "tern()}catch(e){$('sessionSummary').textContent=e.messag"
    "e;$('sessionSummary').className='error'}};\n$('finishForN"
    "ow').onclick=()=>{const summary=completedResults.map((r,"
    "i)=>`${i+1}. ${r.status}${r.wording?' — '+r.wording:''}`"
    ").join('\\n');$('sessionSummary').textContent=summary||'N"
    "o completed pattern threads yet.';show('sessionSummary')"
    "};\n$('copyExport').onclick=async()=>{const transcript=[."
    "..document.querySelectorAll('#conversation .bubble')].ma"
    "p(el=>el.innerText).join('\\n\\n');const results=completed"
    "Results.map((r,i)=>`${i+1}. ${r.status}${r.wording?' — '"
    "+r.wording:''}`).join('\\n');const text=`Life Patterns ow"
    "ner interview\\n\\n${transcript}\\n\\nCompleted results\\n${r"
    "esults}`;try{await navigator.clipboard.writeText(text);$"
    "('sessionSummary').textContent='Interview summary copied"
    " to your clipboard.'}catch(e){$('sessionSummary').textCo"
    "ntent=text}show('sessionSummary')};\n\nstart();\n</script>\n"
    "</main></body></html>"
)
