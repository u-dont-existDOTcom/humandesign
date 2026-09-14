"""Owner-facing browser UI for the bounded Life Patterns v2 real-data prototype."""

HTML = (
    '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="u'
    'tf-8">\n<meta name="viewport" content="width=device-width'
    ',initial-scale=1">\n<title>Discover Your Unique Life Patt'
    "erns — owner development</title>\n<style>\n:root{--ink:#20"
    "242a;--muted:#667085;--line:#d0d5dd;--soft:#f7f8fa;--acc"
    "ent:#315c5f;--user:#eef6f6;--ai:#f7f3eb;--good:#176b44;-"
    "-warn:#8a5a00;--bad:#a61b1b}\n*{box-sizing:border-box}bod"
    "y{margin:0;background:#fff;color:var(--ink);font:16px/1."
    '55 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI"'
    ",sans-serif}main{width:min(58rem,calc(100% - 2rem));marg"
    "in:2rem auto 5rem}h1{font-size:clamp(2rem,7vw,3.5rem);li"
    "ne-height:1.02;letter-spacing:-.04em;margin:.2rem 0 .7re"
    "m}h2,h3{margin:.2rem 0 .65rem}.lede{font-size:1.08rem;co"
    "lor:var(--muted);max-width:48rem}.card{border:1px solid "
    "var(--line);border-radius:1rem;padding:1.1rem;margin:1re"
    "m 0;background:#fff}.soft{background:var(--soft)}.chat{d"
    "isplay:grid;gap:.8rem;margin:1rem 0}.bubble{padding:.9re"
    "m 1rem;border-radius:.85rem;max-width:94%;white-space:pr"
    "e-wrap}.bubble.user{background:var(--user);margin-left:a"
    "uto}.bubble.ai{background:var(--ai)}.meta{font-size:.82r"
    "em;color:var(--muted);margin-bottom:.25rem}.pill{display"
    ":inline-block;font-size:.82rem;border:1px solid var(--li"
    "ne);border-radius:999px;padding:.25rem .6rem;color:var(-"
    "-muted)}textarea,input,button{font:inherit;border:1px so"
    "lid #98a2b3;border-radius:.55rem;padding:.72rem .8rem}te"
    "xtarea{width:100%;min-height:8rem;resize:vertical}button"
    "{background:var(--accent);border-color:var(--accent);col"
    "or:#fff;font-weight:750;cursor:pointer}button.secondary{"
    "background:#fff;color:var(--accent)}button.subtle{backgr"
    "ound:#fff;color:var(--ink);border-color:var(--line)}butt"
    "on.danger{background:#fff;color:var(--bad);border-color:"
    "#e5a6a6}button:disabled{opacity:.5;cursor:not-allowed}.r"
    "ow{display:flex;gap:.65rem;flex-wrap:wrap;align-items:ce"
    "nter}.hidden{display:none}.note{font-size:.91rem;color:v"
    "ar(--muted)}.good{color:var(--good)}.warn{color:var(--wa"
    "rn)}.error{color:var(--bad)}.fact{border:1px solid var(-"
    "-line);border-radius:.8rem;padding:.85rem;margin:.7rem 0"
    "}.fact p{margin:.2rem 0 .6rem}.fact .edit{margin-top:.7r"
    "em}.smallcaps{font-size:.78rem;letter-spacing:.08em;text"
    "-transform:uppercase;color:var(--muted);font-weight:750}"
    ".result{border-left:4px solid var(--accent);padding:.9re"
    "m 1rem;background:#f2f8f8;margin:1rem 0}.topbar{display:"
    "flex;justify-content:space-between;gap:1rem;align-items:"
    "center;flex-wrap:wrap}.count{font-size:.88rem;color:var("
    "--muted)}.divider{border:0;border-top:1px solid var(--li"
    "ne);margin:1.1rem 0}\n</style>\n</head>\n<body><main>\n<div "
    'class="topbar"><div><span class="pill">Owner-only develo'
    "pment · theory-blind</span><h1>Discover Your Unique Life"
    ' Patterns</h1></div><div id="sessionState" class="count"'
    '>Starting…</div></div>\n<p class="lede">Use your own real'
    " situations. The interviewer first checks what actually "
    "happened, then—only after more than one reviewed example"
    "—may ask whether those examples suggest a broader patter"
    "n. You decide what, if anything, describes you.</p>\n<div"
    ' class="card soft"><strong>Private development boundary<'
    '/strong><p class="note">This run is for you only. The se'
    "rver keeps narratives in memory for this process and doe"
    "s not write them to Git. No birth data, chart informatio"
    "n, or target-model predictions enter this interview.</p>"
    '</div>\n\n<div id="configWarning" class="card hidden"><str'
    'ong>AI runtime is not configured.</strong><p class="note'
    '">The browser surface is ready, but the local runtime ne'
    "eds an OpenAI-compatible API key in <code>HDMATCH_LLM_AP"
    "I_KEY</code> or <code>OPENAI_API_KEY</code> before it ca"
    "n extract facts or propose a pattern.</p></div>\n\n<div id"
    '="conversation" class="chat"></div>\n\n<div id="episodePan'
    'el" class="card">\n<div class="smallcaps">Add a real exam'
    "ple</div>\n<h2>Tell me about one specific situation</h2>\n"
    '<p class="note">Use an actual event rather than a genera'
    "l description of yourself. What happened? What did you d"
    "o, think, notice, decide, or avoid? A few sentences is e"
    'nough.</p>\n<textarea id="episodeText" placeholder="Examp'
    "le: Last week I had to decide whether to... I first... t"
    'hen... what mattered was..."></textarea>\n<div class="row'
    '"><button id="analyzeEpisode">Reflect this example back '
    'to me</button></div>\n<p id="episodeStatus" class="note">'
    '</p>\n</div>\n\n<div id="factPanel" class="card hidden">\n<d'
    'iv class="smallcaps">Check the example</div>\n<h2>Here’s '
    'what I think happened</h2>\n<p class="note">Correct anyth'
    "ing that adds meaning you did not give. These are episod"
    "e facts, not claims about your personality.</p>\n<div id="
    '"facts"></div>\n<div class="row"><button id="saveFacts">S'
    'ave my review</button></div>\n<p id="factStatus" class="n'
    'ote"></p>\n</div>\n\n<div id="betweenPanel" class="card hid'
    'den">\n<h2>Example saved</h2>\n<p id="betweenText"></p>\n<d'
    'iv class="row"><button id="anotherEpisode">Add another r'
    'eal example</button><button id="lookForPattern" class="s'
    'econdary hidden">See whether these examples suggest a pa'
    'ttern</button></div>\n</div>\n\n<div id="patternPanel" clas'
    's="hidden">\n<div class="chat"><div class="bubble ai"><di'
    'v class="meta">Interviewer</div><div id="patternQuestion'
    '"></div></div></div>\n<div class="card">\n<p class="note">'
    "This is only a hypothesis from the reviewed examples. It"
    " is not kept as a pattern unless you endorse it.</p>\n<di"
    'v class="row"><button id="patternAccept">Yes, that fits '
    'me</button><button id="patternRevise" class="secondary">'
    'Close, but I’d say it differently</button><button id="pa'
    'tternReject" class="danger">No, that’s not a pattern of '
    'mine</button><button id="patternUnresolved" class="subtl'
    'e">I’m not sure</button></div>\n<div id="reviseBox" class'
    '="hidden">\n<hr class="divider"><label for="revisedWordin'
    'g"><strong>How would you say it?</strong></label><textar'
    'ea id="revisedWording" placeholder="Write the version th'
    'at actually fits you…"></textarea>\n<p><strong>What suppo'
    'rts this revised wording?</strong></p>\n<p class="note">T'
    "his keeps two questions separate: whether the wording fe"
    "els true of you, and whether these particular examples a"
    'ctually show it.</p>\n<div class="row"><button class="sec'
    'ondary grounding" data-grounding="examples">These exampl'
    'es show it</button><button class="secondary grounding" d'
    'ata-grounding="other_situations">I know it from other si'
    'tuations</button><button class="subtle grounding" data-g'
    'rounding="unsure">I’m not sure</button></div>\n<div id="f'
    'inalChoice" class="hidden"><p><strong>Given that, what s'
    "hould we do with the revised pattern?</strong></p><div c"
    'lass="row"><button class="final" data-final="accept">Kee'
    'p it</button><button class="danger final" data-final="re'
    'ject">Reject it</button><button class="subtle final" dat'
    'a-final="unresolved">Leave it open</button></div></div>\n'
    '</div>\n<p id="patternStatus" class="note"></p>\n</div>\n</'
    'div>\n\n<div id="resultPanel" class="hidden result"></div>'
    '\n<div id="postResult" class="hidden row"><button id="add'
    'AfterResult" class="secondary">Add another real example<'
    "/button></div>\n\n<script>\nlet sessionId=null;let currentE"
    "pisodeId=null;let currentFacts=[];let reviewedEpisodes=0"
    ";let groundingChoice=null;\nconst $=id=>document.getEleme"
    "ntById(id);\nfunction show(id){$(id).classList.remove('hi"
    "dden')}function hide(id){$(id).classList.add('hidden')}\n"
    "function status(id,text,error=false){const el=$(id);el.t"
    "extContent=text;el.className=error?'error':'note'}\nfunct"
    'ion escapeHtml(s){return String(s).replace(/[&<>\\"]/g,c='
    ">({'&':'&amp;','<':'&lt;','>':'&gt;','\\\"':'&quot;'}[c]))"
    "}\nasync function api(path,options={}){const r=await fetc"
    "h(path,{headers:{'content-type':'application/json',...(o"
    "ptions.headers||{})},...options});let p={};try{p=await r"
    ".json()}catch{}if(!r.ok)throw new Error(p.detail||'Reque"
    "st failed');return p}\nfunction addBubble(role,text){cons"
    "t wrap=document.createElement('div');wrap.className='bub"
    "ble '+role;wrap.innerHTML='<div class=\"meta\">'+(role==='"
    "user'?'You':'Interviewer')+'</div><div>'+escapeHtml(text"
    ")+'</div>';$('conversation').append(wrap);wrap.scrollInt"
    "oView({behavior:'smooth',block:'end'})}\nasync function s"
    "tart(){try{const p=await api('/api/owner-v2/sessions',{m"
    "ethod:'POST'});sessionId=p.session_id;$('sessionState')."
    "textContent='Private runtime session · 0 reviewed exampl"
    "es';if(!p.model_configured)show('configWarning');addBubb"
    "le('ai','Start with one concrete situation from your lif"
    "e. I’ll first reflect back only what the example support"
    "s.')}catch(e){$('sessionState').textContent='Could not s"
    "tart';status('episodeStatus',e.message,true)}}\n$('analyz"
    "eEpisode').onclick=async()=>{const text=$('episodeText')"
    ".value.trim();if(!text||!sessionId)return;addBubble('use"
    "r',text);$('analyzeEpisode').disabled=true;status('episo"
    "deStatus','Reading the example…');try{const p=await api("
    "`/api/owner-v2/sessions/${encodeURIComponent(sessionId)}"
    "/episodes`,{method:'POST',body:JSON.stringify({text})});"
    "currentEpisodeId=p.episode_id;currentFacts=p.proposed_fa"
    "cts;renderFacts(p.neutral_summary,p.proposed_facts);hide"
    "('episodePanel');show('factPanel');$('factPanel').scroll"
    "IntoView({behavior:'smooth'})}catch(e){status('episodeSt"
    "atus',e.message,true)}finally{$('analyzeEpisode').disabl"
    "ed=false}}\nfunction renderFacts(summary,facts){$('facts'"
    ").textContent='';addBubble('ai','Here is my neutral summ"
    "ary of that example: '+summary);for(const fact of facts)"
    "{const box=document.createElement('div');box.className='"
    "fact';box.dataset.factId=fact.fact_id;box.dataset.action"
    "='accept';box.innerHTML='<p><strong>'+escapeHtml(fact.pr"
    'oposition)+\'</strong></p><div class="row"><button type="'
    'button" class="keep">Yes, that is supported</button><but'
    'ton type="button" class="secondary editBtn">Not quite — '
    'edit it</button><button type="button" class="danger drop'
    '">That is not supported</button></div><div class="edit h'
    'idden"><textarea></textarea><div class="row"><button typ'
    'e="button" class="saveEdit">Use this wording</button></d'
    'iv></div><p class="note decision">Currently: keep</p>\';$'
    "('facts').append(box);wireFact(box)}}\nfunction wireFact("
    "box){box.querySelector('.keep').onclick=()=>{box.dataset"
    ".action='accept';box.querySelector('.decision').textCont"
    "ent='Currently: keep';box.querySelector('.edit').classLi"
    "st.add('hidden')};box.querySelector('.drop').onclick=()="
    ">{box.dataset.action='not_supported';box.querySelector('"
    ".decision').textContent='Currently: do not use this fact"
    "';box.querySelector('.edit').classList.add('hidden')};bo"
    "x.querySelector('.editBtn').onclick=()=>{box.querySelect"
    "or('.edit').classList.remove('hidden');box.querySelector"
    "('textarea').focus()};box.querySelector('.saveEdit').onc"
    "lick=()=>{const v=box.querySelector('textarea').value.tr"
    "im();if(!v)return;box.dataset.action='correct';box.datas"
    "et.corrected=v;box.querySelector('.decision').textConten"
    "t='Currently: use your correction — “'+v+'”';box.querySe"
    "lector('.edit').classList.add('hidden')}}\n$('saveFacts')"
    ".onclick=async()=>{if(!currentEpisodeId)return;const rev"
    "iews=[...document.querySelectorAll('.fact')].map(box=>({"
    "fact_id:box.dataset.factId,action:box.dataset.action,cor"
    "rected_proposition:box.dataset.action==='correct'?box.da"
    "taset.corrected:null}));$('saveFacts').disabled=true;sta"
    "tus('factStatus','Saving your review…');try{const p=awai"
    "t api(`/api/owner-v2/sessions/${encodeURIComponent(sessi"
    "onId)}/episodes/${encodeURIComponent(currentEpisodeId)}/"
    "review`,{method:'POST',body:JSON.stringify({reviews})});"
    "reviewedEpisodes=p.reviewed_episode_count;$('sessionStat"
    "e').textContent='Private runtime session · '+reviewedEpi"
    "sodes+' reviewed example'+(reviewedEpisodes===1?'':'s');"
    "hide('factPanel');show('betweenPanel');$('betweenText')."
    "textContent=p.episode_saved?'This example is now availab"
    "le as reviewed evidence.':'None of the proposed facts we"
    "re supported, so this example was not used as evidence.'"
    ";if(p.can_look_for_pattern)show('lookForPattern');$('bet"
    "weenPanel').scrollIntoView({behavior:'smooth'})}catch(e)"
    "{status('factStatus',e.message,true)}finally{$('saveFact"
    "s').disabled=false}}\nfunction resetEpisode(){currentEpis"
    "odeId=null;currentFacts=[];$('episodeText').value='';hid"
    "e('betweenPanel');hide('patternPanel');hide('resultPanel"
    "');hide('postResult');show('episodePanel');$('episodePan"
    "el').scrollIntoView({behavior:'smooth'})}\n$('anotherEpis"
    "ode').onclick=resetEpisode;$('addAfterResult').onclick=r"
    "esetEpisode;\n$('lookForPattern').onclick=async()=>{$('lo"
    "okForPattern').disabled=true;try{const p=await api(`/api"
    "/owner-v2/sessions/${encodeURIComponent(sessionId)}/patt"
    "erns/propose`,{method:'POST'});if(!p.has_candidate){addB"
    "ubble('ai','I do not see a defensible cross-example patt"
    "ern yet. That is useful too; add another example rather "
    "than forcing one.');resetEpisode();return}$('patternQues"
    "tion').textContent=p.question_text;hide('betweenPanel');"
    "show('patternPanel');$('patternPanel').scrollIntoView({b"
    "ehavior:'smooth'})}catch(e){status('patternStatus',e.mes"
    "sage,true)}finally{$('lookForPattern').disabled=false}}\n"
    "async function simpleDecision(decision){try{const p=awai"
    "t api(`/api/owner-v2/sessions/${encodeURIComponent(sessi"
    "onId)}/patterns/adjudicate`,{method:'POST',body:JSON.str"
    "ingify({decision})});renderResult(p)}catch(e){status('pa"
    "tternStatus',e.message,true)}}\n$('patternAccept').onclic"
    "k=()=>simpleDecision('accept');$('patternReject').onclic"
    "k=()=>simpleDecision('reject');$('patternUnresolved').on"
    "click=()=>simpleDecision('unresolved');$('patternRevise'"
    ").onclick=()=>show('reviseBox');\ndocument.querySelectorA"
    "ll('.grounding').forEach(btn=>btn.onclick=()=>{grounding"
    "Choice=btn.dataset.grounding;document.querySelectorAll('"
    ".grounding').forEach(b=>b.disabled=true);if(groundingCho"
    "ice==='examples'){show('finalChoice')}else{submitRevisio"
    "n(null)}})\ndocument.querySelectorAll('.final').forEach(b"
    "tn=>btn.onclick=()=>submitRevision(btn.dataset.final))\na"
    "sync function submitRevision(finalDecision){const wordin"
    "g=$('revisedWording').value.trim();if(!wording){status('"
    "patternStatus','Write the wording that fits you first.',"
    "true);return}try{const body={decision:'revise',revised_w"
    "ording:wording,grounding_source:groundingChoice,final_de"
    "cision:finalDecision};const p=await api(`/api/owner-v2/s"
    "essions/${encodeURIComponent(sessionId)}/patterns/adjudi"
    "cate`,{method:'POST',body:JSON.stringify(body)});renderR"
    "esult(p)}catch(e){status('patternStatus',e.message,true)"
    "}}\nfunction renderResult(p){hide('patternPanel');const b"
    "ox=$('resultPanel');let title=p.status==='accepted'?'Pat"
    "tern kept':p.status==='rejected'?'Pattern rejected':'Pat"
    "tern left open';let body='';if(p.wording)body+='<p><stro"
    "ng>'+escapeHtml(p.wording)+'</strong></p>';if(p.message)"
    "body+='<p>'+escapeHtml(p.message)+'</p>';if(p.needs_more"
    '_evidence)body+=\'<p class="note">This preserves your wor'
    "ding as something worth testing without pretending the c"
    "urrent examples already establish it.</p>';else body+='<"
    'p class="note">The result passed through the participant'
    "-adjudicated v2 record validation path.</p>';box.innerHT"
    "ML='<div class=\"smallcaps\">Current result</div><h2>'+tit"
    "le+'</h2>'+body;show('resultPanel');show('postResult');b"
    "ox.scrollIntoView({behavior:'smooth'})}\nstart();\n</scrip"
    "t>\n</main></body></html>"
)
