"""Deterministic transparent, source-based atlas of the full instrument and interpretation limits."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASK = Path(__file__).resolve().parent
BANK = json.loads((ROOT / 'tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json').read_text())
GUIDE = json.loads((ROOT / 'tasks/scenario-survey-v7-redesign-20260922/EVIDENCE-GUIDE-v7.json').read_text())
V1 = json.loads((ROOT / 'apps/life-patterns-participant/participant/static/tendency-first-v1.json').read_text())
V2 = json.loads((ROOT / 'tasks/question-feedback-loop-20261008/tendency-first-v2-development.json').read_text())
PURPOSE = json.loads((ROOT / 'apps/life-patterns-participant/participant/static/question-purposes-v1.json').read_text())['purposes']
by_route = {}
for facet in GUIDE:
    for route in facet.get('question_routes') or []:
        by_route.setdefault(route,[]).append(facet)
legacy = {q['id']:q for q in BANK['questions']}
proposed = {q['id']:q for q in V2['questions']}
rows = []
for typ, routes in [('current_tf1_v1',V1['questions']),('historical_v7',BANK['questions']),('proposed_tf1_v2',V2['questions'])]:
    for q in routes:
        source = q.get('source_route_id') or q['id']
        facets = by_route.get(source, [])
        old = legacy.get(source,{})
        active = typ=='current_tf1_v1'
        status = 'CURRENT TF1 V1' if active else ('DEVELOPMENT ONLY: NOT LIVE' if typ=='proposed_tf1_v2' else ('RETIRED FROM NEW QUESTIONS' if q['id'] in V1['retired_from_new_elicitation'] else 'HISTORICAL / POSSIBLE PROBE'))
        rows.append({
            'id':q['id'],'version':typ,'status':status,'question':q['question'],
            'example_if_needed':q.get('example_if_needed'),
            'purpose':PURPOSE.get(q['id']) or PURPOSE.get(source) or '',
            'source_route_id':source,'family':q.get('family',''),
            'planning_targets':q.get('planning_targets') or [],
            'interpretation_limit':q.get('interpretation_limit',''),
            'admission':q.get('admission',''),
            'context_requirement':q.get('context_requirement',''),
            'frozen_v7_facet_examples':[{
                'facet_id':f['facet_id'],
                'fictional_answer':f.get('fictional_answer',''),
                'narrow_supported_reading':f.get('narrow_supported_reading',''),
                'unsupported_extension':f.get('unsupported_extension',''),
            } for f in facets],
            'automatic_old_facet_equivalence':typ=='historical_v7',
            'prospective_changed_text':typ=='proposed_tf1_v2' and q['question'] != next(x['question'] for x in V1['questions'] if x['id']==q['id']),
        })
(TASK/'question-atlas.json').write_text(json.dumps({'schema':'life-patterns-question-atlas-v1','stats':{'historical_v7':len(BANK['questions']),'active_tf1_v1':len(V1['questions']),'prospective_v2':len(V2['questions']),'guide_facets':len(GUIDE)},'questions':rows},ensure_ascii=False,indent=2)+'\n')

def esc(v): return html.escape(str(v or ''),quote=True)
entries=[]
for r in rows:
    supported=''.join('<div class="facet"><b>'+esc(f['facet_id'])+'</b><p>Example answer: '+esc(f['fictional_answer'])+'</p><p>Allowed narrow observation: '+esc(f['narrow_supported_reading'])+'</p><p><b>Not justified:</b> '+esc(f['unsupported_extension'])+'</p></div>' for f in r['frozen_v7_facet_examples'])
    link_note='<p class="note">Those facets describe the historical v7 route. The TF1 response is not automatically interchangeable with old facets or valid for natal scoring; each inference must be independently supported.</p>' if r['version']!='historical_v7' else ''
    entries.append(f'''<article class="entry" data-version="{r['version']}" data-text="{esc(' '.join([r['id'],r['question'],r['purpose'],r['family']]))}"><h3>{esc(r['id'])} <span class="tag">{esc(r['status'])}</span></h3><p class="question">{esc(r['question'])}</p><p><b>What this distinguishes:</b> {esc(r['purpose'] or r['family'])}</p><details><summary>Examples, limits and evidence interpretation</summary><p><b>Optional example:</b> {esc(r['example_if_needed'])}</p><p><b>Admitted inference limit:</b> {esc(r['interpretation_limit'])}</p><p><b>When it is worth asking:</b> {esc(r['admission'])}</p><p><b>Context conditions:</b> {esc(r['context_requirement'])}</p>{link_note}{supported or '<p>No explicit v7 facet example for this route. Do not invent trait scoring.</p>'}</details></article>''')
script='''<script>const filter=document.getElementById('filter'),which=document.getElementById('which'),els=[...document.querySelectorAll('.entry')],number=document.getElementById('count');function update(){const q=filter.value.toLowerCase().trim(),v=which.value;let n=0;for(const item of els){const show=(!v||item.dataset.version===v)&&(!q||item.dataset.text.toLowerCase().includes(q));item.hidden=!show;if(show)n++;}number.textContent=n+' questions shown';}filter.addEventListener('input',update);which.addEventListener('change',update);update();</script>'''
html_doc='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Life Patterns — Questions & interpretation atlas</title><style>body{font-family:system-ui,-apple-system,sans-serif;max-width:980px;margin:0 auto;padding:25px 20px;line-height:1.48;background:#f7f8fa;color:#24262a}header{border-bottom:2px solid #d3d9e0;padding-bottom:18px}h1{font-size:1.65rem}h3{font-size:1.12rem;margin:0}input,select{padding:9px;font:inherit;border:1px solid #a5adba;border-radius:7px;max-width:100%}.tools{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0}.entry{background:white;border:1px solid #dde1e5;border-radius:9px;padding:17px;margin:12px 0;box-shadow:0 1px 2px #ddd}.entry[hidden]{display:none}.question{font-size:1.07rem}.tag{color:#596779;font-size:.76rem;margin-left:6px;letter-spacing:.02em}.facet{border-left:3px solid #aab6c5;padding:4px 14px;margin:13px 0;background:#f6f8fb}details summary{cursor:pointer;font-weight:600;color:#23486c}.note{font-size:.9rem;color:#654623}.meta{color:#596373}#count{font-size:.92rem}</style></head><body><header><h1>Life Patterns: every question and what answers can support</h1><p>All 79 historical v7 questions, the 25 current tendency-first v1 questions and 25 separately proposed v2 versions. Includes the 73 original evidence-guide facets, sample answers, narrow admissible interpretations and prohibited overextensions.</p><p class="meta"><b>Scientific boundary:</b> This is a transparent coding/elicitation reference, not an answer key or proof that the questions identify birth time. New TF1 answers are not automatically scored as historical v7 evidence. Proposed v2 wordings are not live. A short or ordinary answer may legitimately support no trait inference.</p></header><div class="tools"><input id="filter" aria-label="Filter questions" placeholder="Search question, route, purpose…" size="36"><select id="which"><option value="">All versions</option><option value="current_tf1_v1">Current v1 (25)</option><option value="historical_v7">Historical v7 (79)</option><option value="proposed_tf1_v2">Proposed v2 (25, not live)</option></select><span id="count"></span></div>'''+''.join(entries)+script+'</body></html>'
(TASK/'question-atlas.html').write_text(html_doc,encoding='utf-8')
print('question_catalog',len(rows),'html_kb',round(len(html_doc)/1024),'json_kb',round((TASK/'question-atlas.json').stat().st_size/1024))
