"""Build explicit original source-to-draft map with all recorded interpretive unknowns."""
from pathlib import Path
import json
B=Path(__file__).resolve().parent
rows=json.loads((B/'SOURCE_FIRST_CLAUSES_DRAFT.json').read_text())['rows']
assert len(rows)==24
spec=[
 (410,'chapter LIV heading',[1]),(410,'buyer/seller roles',[2,3]),
 (410,'Moon conjunction with seller',[4]),
 (410,'lighter significator comparison and converse',[5,6]),
 (410,'no direct aspect: translated light: friend',[7,8]),
 (410,'commodity house taxonomies',[9,10,11,12]),
 (410,'seller vs buyer interest from lords in opposite houses',[13,14]),
 (410,'Jupiter/Venus ascendant quick buyer',[15]),
 (410,'Sun ascendant without corporeal conjunction',[16]),
 (410,'Mercury/Moon ascendant uninfected',[17]),
 ([410,411],'Saturn/Mars/node-like glyph in first; difficult/deceit characterization',[18,19]),
 (411,'seventh house malefic and seller characterization',[20]),
 (411,'void of course Moon exception and no-bargain claim',[21]),
 (411,'combustion of Moon-separated planet and former property',[22]),
 (411,'free-from-misfortune Moon-separated planet and possible repurchase',[23]),
 (411,'chapter LV heading across divider',[24])
]
assert len(spec)==16
spans=[]
for i,(page,anchor,idxs) in enumerate(spec,1):
 pages=page if isinstance(page,list) else [page]
 for idx in idxs: assert rows[idx-1]['original_pdf_pages']==pages,(idx,pages)
 spans.append({'span_id':f'LIV-S{i:03}','original_pdf_pages':pages,'source_anchor_as_descriptive_label_not_full_quote':anchor,
 'draft_local_ids':[f'LIV-C{j:03}' for j in idxs]})
assert [i for span in spans for i in span['draft_local_ids']]==[r['local_id'] for r in rows]
coverage={'batch':'B02z','status':'PROVISIONAL_SOURCE_TO_DRAFT_VISUAL_MAP',
'complete_chapter_claimed':False,'independent_diplomatic_transcription_claimed':False,
'source_spans':spans,'span_count':len(spans),'draft_source_units':24,
'source_window':'PDF410 below divider through PDF411 above next divider','empirical_outcomes':0}
issues=[
('Z-U01','Light-planet comparison in sale initiative has no numerical method or universal weight table.'),
('Z-U02','One literal & e contra follows lighter-significator comparison; source does not enumerate a separate prediction algorithm.'),
('Z-U03','Mutually applying significators and translation of light are syntactically separated; do not conflate the no-direct-aspect premise with direct conjunction.'),
('Z-U04','Open-ended goods classification does not supply a complete list; analogical houses for unlisted goods must not be invented.'),
('Z-U05','Glyph after Saturn and Mars on PDF410 could be lunar south node, but original glyph identity requires explicit confirmation before formalizing.'),
('Z-U06','The buyer deceit claim continues a prior conditional across PDF410–411; not an independently observed psychological disposition.'),
('Z-U07','Seller-deception statement is a separate seventh-house condition; no actual seller, fraud, or litigation case is authenticated.'),
('Z-U08','Sun first-house clause explicitly excludes corporeal conjunction; the benefic Mercury/Moon option excludes malefic aspect.'),
('Z-U09','Moon void-of-course has a strong-applying-significators exception, not a universal categorical impossibility.'),
('Z-U10','Entering combustion of Moon-separated planet allegedly prevents property recovery forever; no timescale or real event verified.'),
('Z-U11','The sign whose lord is beheld by the previously separated planet remains referentially ambiguous in the final repurchase clause.'),
('Z-U12','The alternate repurchase outcome is conditional on BOTH planet free-from-misfortune and beholding sign lord.'),
('Z-U13','PDF410–411 are copied original-page images from an earlier active worktree and SHA256-frozen; full-original-PDF pixel parity and blind diplomatic transcription not independently established.'),
('Z-U14','Preceding LIII original-source acceptance remains unresolved; numbering, index integration, final archive admission and canonical promotion must wait.')
]
out={'batch':'B02z','status':'RETAINED_OPEN_SOURCE_LIMITS','issues':[{'id':i,'description':s} for i,s in issues],
'outcome_validation_count':0}
for fn,obj in [('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',coverage),('UNRESOLVED_SOURCE_LIMITS.json',out)]:
 p=B/fn
 assert not p.exists(),p
 p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('reverse source spans',len(spans),'issues',len(issues),'rows',len(rows))
