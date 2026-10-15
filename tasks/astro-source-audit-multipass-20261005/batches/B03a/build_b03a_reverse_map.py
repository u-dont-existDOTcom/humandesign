import json
from pathlib import Path
B=Path(__file__).resolve().parent
rows=json.loads((B/'SOURCE_FIRST_CLAUSES_DRAFT.json').read_text())['rows']
# Original-to-record manual, paragraph/clause-first. Labels are descriptive, not diplomatic quotation.
groups=[
([411],'chapter LV heading',[1]),
([411],'first/7 significator roles',[2,3]),
([411],'seventh-cusp planet descriptively matched',[4]),
([411],'Moon additional role',[5]),
([411],'10th reputation; 4th and Moon applying for outcome',[6,7]),
([411,412],'movable signs and absent reception → contention, mistrust, temporary reconciliation',[8,9]),
([412],'fixed signs; absent reception; commodities on hand',[10,11,12]),
([412],'common signs vs one movable and one fixed',[13,14]),
([412],'malefics aspect both; house cause; wrong actors first/seventh',[15,16,17,18]),
([412],'Moon from fortune to fortune',[19]),
([412],'Moon from fortune to malefic; contrary shorthand; later separate from ill',[20,21,22]),
([412],'good tenth; benefit to querent second and partner seventh',[23,24]),
([412],'malefic second or node-like glyph',[25]),
([412],'positive partnership ending fourth/eleventh aspects or reception or good planets',[26,27,28,29]),
([412],'observe circled-cross glyph',[30]),
([412,413],'seventh/eighth lords square/opposition glyph and common stock loss claim',[31]),
([413],'chapter LVI boundary only',[32])
]
assert len(groups)==17
spans=[]
for i,(pages,span,idxs) in enumerate(groups,1):
 for j in idxs:assert rows[j-1]['original_pdf_pages']==pages,(j,pages)
 spans.append({'span_id':f'LV-S{i:03}','pdf_pages':pages,'original_passage_descriptive_label_not_diplomatic':span,
 'mapped_source_ids':[f'LV-C{j:03}' for j in idxs]})
assert [id for v in spans for id in v['mapped_source_ids']]==[r['source_local_id'] for r in rows]
out={'batch':'B03a','status':'UNACCEPTED_IMAGE_FIRST_SOURCE_TO_DRAFT',
'reviewed_original_pdf_pages':[411,412,413],
'chapter_open':'PDF411 below printed divider',
'chapter_close':'PDF413 above printed divider',
'complete_independent_diplomatic_transcription_claimed':False,
'visual_source_spans':spans,'span_count':len(spans),'draft_record_count':len(rows),
'empirical_case_count':0}
issues=[
('A-U01','Planet near seventh cusp descriptively matching proposed partner can replace seventh lord; source flexibility cannot be treated as a prospectively specified classifier.'),
('A-U02','Moon is described as a partner significator without explicitly specifying how to weigh it against first/seventh lords.'),
('A-U03','Movable first lord AND Moon and reception absence require attention to the named dignity alternatives, not an arbitrary reception condition.'),
('A-U04','Reconciliation after movable-sign discord is qualified by continuing mistrust and weak benefit; not uncomplicated success.'),
('A-U05','Fixed-sign durability, absence-of-reception weak profits and commodities lying long are one conditional passage, not unrelated examples.'),
('A-U06','Common signs, movable signs and fixed signs retain Lilly contextual labels; do not collapse contrary meaning across different significator sets.'),
('A-U07','Malefics affecting BOTH first and seventh lords are distinguished from malefic placement in either first or seventh house.'),
('A-U08','Claims of dishonest querent/partner are only historic authorial character assertions with no authenticated real people.'),
('A-U09','Moon separating from benefic and applying to another benefic is claimed to bring beginning/end well but no wealth; retain simultaneous outcome qualifications.'),
('A-U10','The source prints and so the contrary, without an enumerated inverse decision table.'),
('A-U11','When the Moon separates from an ill planet and applies to another, the adjective for the second planet is not re-stated; do not insert an assumed malefic.'),
('A-U12','Symbol following ill planet in second on PDF412 looks like node-like glyph but exact identity/scope is not independently certified.'),
('A-U13','The circled-cross glyph after observe in PDF412 resembles Part of Fortune; distinguish visual symbol from confident symbol attribution until full witness collated.'),
('A-U14','Benefics casting sextile/trine toward the lords of first/seventh may be a joint or distributive condition; exact quantified AND grouping unresolved.'),
('A-U15','The seventh/eighth-lord square/opposition to the printed glyph clause spans PDF412→413 and implies common-stock loss, not an authenticated embezzlement.'),
('A-U16','LIII and LIV are not both canonically accepted as prerequisites, and copied page JPEGs are source witnesses rather than independently verified pixel identical full-PDF renders.')
]
limit={'batch':'B03a','status':'OPEN_UNRESOLVED_SOURCE_AND_PREDECESSOR_LIMITS',
'issues':[{'id':a,'description':s} for a,s in issues],
'empirical_validation_count':0}
for p,j in [('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',out),('UNRESOLVED_SOURCE_LIMITS.json',limit)]:
 assert not (B/p).exists()
 (B/p).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
print('B03a visual original paragraphs',len(spans),'editorial source records',len(rows),'retained open issues',len(issues))
