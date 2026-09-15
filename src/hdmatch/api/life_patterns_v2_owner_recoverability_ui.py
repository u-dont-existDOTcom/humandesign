"""Client-only freeze/export and synthesis-review UX overlay for the recoverability interview."""

from __future__ import annotations

from .life_patterns_v2_owner_coverage import COVERAGE_HTML


def _build_html() -> str:
    html = COVERAGE_HTML

    # The synthesis buttons are shortcuts, not a forced-response form. Keep free-form
    # conversation available while a proposal is active so a participant can explain
    # a nuance that none of the buttons captures.
    html = html.replace(
        "if(refiningPattern){show('composer')}else{hide('composer')}",
        "show('composer');$('message').placeholder='Or explain what fits, what does not, or what the buttons miss…'",
        1,
    )
    html = html.replace(
        "The hidden episode facts are not being shown for routine approval.</p>",
        "The hidden episode facts are not being shown for routine approval. "
        "The buttons are shortcuts; if none says what you mean, type it in the chat box below.</p>",
        1,
    )

    # Split two different intents that the old single 'Close, but change it' button
    # conflated: conversational feedback versus authoring exact replacement wording.
    html = html.replace(
        '<button id="revise" class="secondary">Close, but change it</button>',
        '<button id="revise" class="secondary">Close — I’ll explain what needs changing</button>\n'
        '    <button id="editExactWording" class="secondary">Edit exact wording myself</button>',
        1,
    )
    html = html.replace(
        '<div id="reviseBox" class="hidden">',
        '<div id="reviseBox" class="hidden">\n'
        '    <button id="backFromRevise" type="button" class="subtle">← Back to synthesis choices</button>\n'
        '    <p class="note">Use this editor only if you want to write the exact replacement pattern yourself. '
        'If you only want to explain what is missing, too broad, or otherwise wrong, use the chat box below instead.</p>',
        1,
    )
    html = html.replace(
        "<strong>What is the version that actually fits?</strong>",
        "<strong>What exact replacement wording should be recorded?</strong>",
        1,
    )
    html = html.replace(
        "<strong>Do the situations we actually discussed show that revised version?</strong>",
        "<strong>Does the evidence already discussed in this thread support that exact wording?</strong>",
        1,
    )
    html = html.replace(
        "Yes, these situations show it",
        "Yes — the discussed evidence supports it",
        1,
    )
    html = html.replace(
        "It comes from other situations",
        "No — this wording also uses other situations",
        1,
    )
    html = html.replace(
        "<strong>Then should I keep the revised version, reject it, or leave it open?</strong>",
        "<strong>You are about to record the exact wording above. What status should it have?</strong>",
        1,
    )
    html = html.replace(
        'data-final="accept">Keep it</button>',
        'data-final="accept">Accept this wording</button>',
        1,
    )
    html = html.replace(
        'data-final="reject">Reject it</button>',
        'data-final="reject">Reject this wording</button>',
        1,
    )
    html = html.replace(
        'data-final="unresolved">Leave it open</button>',
        'data-final="unresolved">Leave this wording unresolved</button>',
        1,
    )

    # 'Close — explain' now routes attention to ordinary chat. Exact-wording editing
    # remains available as an explicit separate action. Back restores the prior choice
    # state without discarding anything typed into the exact-wording box.
    html = html.replace(
        "$('revise').onclick=()=>show('reviseBox');",
        "$('revise').onclick=()=>{hide('reviseBox');hide('finalChoice');groundingChoice=null;document.querySelectorAll('.grounding').forEach(b=>b.disabled=false);show('composer');$('patternStatus').textContent='Tell me what fits and what needs changing in your own words below.';$('patternStatus').className='note';$('message').placeholder='Explain what the synthesis gets right, what it misses, or what is too broad…';$('message').focus()};\n"
        "$('editExactWording').onclick=()=>{show('reviseBox');show('composer');$('patternStatus').textContent='';$('revisedWording').focus()};\n"
        "$('backFromRevise').onclick=()=>{hide('reviseBox');hide('finalChoice');groundingChoice=null;document.querySelectorAll('.grounding').forEach(b=>b.disabled=false);$('patternStatus').textContent='';show('composer');$('message').focus()};",
        1,
    )

    # A revision that depends on un-discussed situations is not a terminal state. The
    # old UI immediately submitted it as unresolved. Keep the inquiry executable and
    # invite the participant to describe the missing evidence in ordinary chat instead.
    html = html.replace(
        "if(groundingChoice==='examples')show('finalChoice');else submitRevision(null);",
        "if(groundingChoice==='examples'){show('finalChoice')}else{hide('finalChoice');document.querySelectorAll('.grounding').forEach(b=>b.disabled=false);show('composer');$('patternStatus').className='note';$('patternStatus').textContent=groundingChoice==='other_situations'?'Tell me about the other situation or pattern in the chat box below so we can investigate it before recording the revision.':'If you are not sure, you can explain what is uncertain in the chat box below, or use Leave it unresolved for now.';$('message').focus()}",
        1,
    )

    # If the participant starts talking instead of using the exact-wording form, close
    # that form and return its controls to a clean state. The backend keeps the same
    # active proposal open and treats the typed message as refinement evidence.
    html = html.replace(
        "bubble('user',text);\n  $('message').value='';",
        "bubble('user',text);\n  if(!$('patternPanel').classList.contains('hidden')){hide('reviseBox');hide('finalChoice');groundingChoice=null;document.querySelectorAll('.grounding').forEach(b=>b.disabled=false)}\n  $('message').value='';",
        1,
    )

    html = html.replace(
        '<button id="finishForNow" class="secondary">Finish for now</button>',
        '<button id="freezeMeasurement" class="secondary">Freeze/export measurement</button>\n'
        '    <button id="finishForNow" class="secondary">Finish for now</button>',
        1,
    )
    html = html.replace(
        "completedResults.push({status:p.status,wording:p.wording||null,coverage:p.coverage||null});",
        "completedResults.push({status:p.status,wording:p.wording||null,freeze_payload_sha256:p.freeze_payload_sha256||null,coverage:p.coverage||null});",
        1,
    )
    marker = "$('finishForNow').onclick=()=>{"
    freeze_js = r'''
function stableJson(value){
  if(Array.isArray(value))return '['+value.map(stableJson).join(',')+']';
  if(value&&typeof value==='object')return '{'+Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+stableJson(value[k])).join(',')+'}';
  return JSON.stringify(value);
}
async function sha256Hex(text){
  const bytes=new TextEncoder().encode(text);
  const digest=await crypto.subtle.digest('SHA-256',bytes);
  return Array.from(new Uint8Array(digest)).map(b=>b.toString(16).padStart(2,'0')).join('');
}
$('freezeMeasurement').onclick=async()=>{
  const bundle={
    schema:'life-patterns-owner-measurement-bundle-v1',
    blueprint_version:coverageBlueprint.length?(completedResults.find(r=>r.coverage&&r.coverage.blueprint_version)?.coverage.blueprint_version||null):null,
    blueprint_sha256:coverageBlueprint.length?(completedResults.find(r=>r.coverage&&r.coverage.blueprint_sha256)?.coverage.blueprint_sha256||null):null,
    frozen_at:new Date().toISOString(),
    completed_results:completedResults,
    aggregate_coverage:coverageAggregate
  };
  const material=stableJson(bundle);
  const digest=await sha256Hex(material);
  const frozen={...bundle,measurement_bundle_sha256:digest};
  const blob=new Blob([JSON.stringify(frozen,null,2)+'\n'],{type:'application/json'});
  const url=URL.createObjectURL(blob);
  const a=document.createElement('a');a.href=url;a.download=`life-patterns-measurement-${digest.slice(0,12)}.json`;
  document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(url);
  $('sessionSummary').textContent=`Frozen measurement exported locally. SHA-256: ${digest}. Keep this file unchanged for post-freeze recovery scoring.`;
  show('sessionSummary');
};
'''
    if marker not in html:
        raise RuntimeError("recoverability freeze insertion point not found")
    return html.replace(marker, freeze_js + marker, 1)


RECOVERABILITY_HTML = _build_html()
