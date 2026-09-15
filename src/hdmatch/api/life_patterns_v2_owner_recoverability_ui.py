"""Client-only freeze/export overlay for the recoverability interview."""

from __future__ import annotations

from .life_patterns_v2_owner_coverage import COVERAGE_HTML


def _build_html() -> str:
    html = COVERAGE_HTML
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
