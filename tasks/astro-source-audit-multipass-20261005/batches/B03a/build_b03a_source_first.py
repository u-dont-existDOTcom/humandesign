"""Visual original-source-first staging for Lilly Chapter LV: NO admission/index mutation."""
import hashlib,json
from pathlib import Path
B=Path(__file__).resolve().parent
PDF='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# role, PDF pages, shortened source anchor (NOT full diplomatic transcript),
# historical author claim paraphrase, conjunction/alternative/antecedent, retained source uncertainty.
data=[
('heading',[411],'CHAP. LV. Of Partnership.','Chapter LV begins after the printed horizontal divider on PDF411.','new source chapter only',''),
('assignment',[411],'The Lord of the ascendant is for the querent','For this partnership question, the ascendant lord signifies the querent.','first-house lord assigned to querent',''),
('assignment',[411],'Lord of the seventh for the Partner intended','The seventh-house lord represents the intended partner, subject to the described in-house-planet qualification.','seventh lord is default, NOT invariably fixed',''),
('exception',[411],'observe what Planet is in the seventh, and neer the cusp','If another planet lies in or near the seventh cusp and better fits the description of the person asked about, that planet can be chosen as the partner significator.','planet in/nearing seventh AND descriptor-match compared with seventh lord','Source selection by observed description creates substantial retrospective degrees of freedom.'),
('assignment',[411],'Let the Moon be partner in signification','Moon is also included as an additional significator in the partnership reading.','Moon additional source role','Do not assume Moon replaces first/seventh lord.'),
('scope',[411],'the tenth house shall shew what credit there may come','The tenth house is said to show credit or reputation accruing to the partnership.','tenth house: reputation or credit',''),
('scope',[411],'whether Partnership will extend to good or ill ... fourth ... Moon applies','To judge whether a partnership will end well, examine the fourth house, its lord, planets therein and the planet Moon applies to.','fourth house AND fourth lord AND its planets AND Moon applying planet','No quantitative weights supplied.'),
('conditional',[411,412],'Lord of the ascendant and Moon be in movable Signs; without Reception','First lord AND Moon in movable signs without reception by house, exaltation, triplicity or term is given as a contention/disagreement condition.','both first lord and Moon movable AND absent reception in named dignity modes',''),
('outcome',[411,412],'matters will againe be reconciled ... Partnership will hold ... mistrustfull','After the movable/no-reception disagreement, the author says reconciliation and partnership continuation may occur but with mistrust and little benefit.','depends on previous movable signs and missing reception; not a separate success case',''),
('conditional',[412],'Significators be in fixed Signes, their society will continue long','Partners significators in fixed signs are said to favor long duration of the association.','both relevant significators in fixed signs',''),
('exception',[412],'but if no Reception be, little profit will ... accrue','The prolonged fixed-sign partnership is said to yield little profit when the required reception is absent.','fixed signs AND no reception','Reception form/scope unspecified.'),
('outcome',[412],'if they buy any thing, Commodities will lye long on their hands','Purchases are said to remain unsold for a long time under the preceding fixed/no-reception condition.','depends on fixed signs and no reception (immediate paragraph antecedent)',''),
('conditional',[412],'Significators be in common Signes ... gainfull Partnership','In common (mutable) signs the text predicts a gainful partnership and mutual faithfulness.','both relevant significators in common signs','Do not confuse with first-lord+Moon movable-sign rule.'),
('conditional',[412],'one Significator ... movable ... other ... fixed ... disturbance ... lesse','One movable and one fixed significator are said to produce less disturbance than initially feared.','one movable AND the other fixed',''),
('conditional',[412],'ill Planets aspect both the significators viz Lord ... ascendant ... seventh','Malefic aspects to BOTH first- and seventh-lord are said to make the partnership unfair to both.','malefic planets aspect both first AND seventh lords',''),
('scope',[412],'see where, and in what house or houses ... evill Planets ... cause','The author instructs readers to consider the malefics house locations when attributing causes, without a complete causal rule.','diagnostic source advice, not empirical identification',''),
('conditional',[412],'evill Planet in the ascendant ... querent false companion','An ill planet in the first is claimed to indicate the querent is an untrustworthy companion.','malefic planet in first house','Historical character attribution, no person-level confirmation.'),
('conditional',[412],'judge the like if an evill Planet be in the seventh','Likewise a malefic in the seventh is alleged to indicate the partner is untrustworthy.','malefic planet in seventh house','Not independent evidence of dishonesty.'),
('conditional',[412],'Moon separate from one Fortune and apply to another','Moon separating from one benefic and applying to another is said to make the partnership begin and end well but without wealth.','Moon separates benefic A AND applies benefic B','Start/end and no wealth must remain together.'),
('conditional',[412],'separated from a good Planet, and apply to an ill','Moon separating from a benefic and applying to a malefic is said to begin well but end in conflict and hatred.','Moon separates benefic AND applies malefic',''),
('converse',[412],'and so the contrary','The passage includes an abbreviated converse for previous lunar applications but does not print a full inverse condition-to-outcome table.','converse shorthand only; inverse not algorithmically expanded',''),
('conditional',[412],'Moon separated from an ill Planet and apply to another','Moon separating from a malefic and applying to another planet (whose quality is not expressly re-specified here) is said to begin with complaints, continue in fear/jealousy and end in lawsuits.','Moon separates malefic AND applies to another planet (quality unspecified)','Do not silently assume another malefic from absent adjective.'),
('conditional',[412],'good Planet in the tenth ... reputation ... rejoice','A benefic in the tenth is claimed to bring reputation and mutual pleasure from the partnership.','benefic in tenth',''),
('conditional',[412],'good Planet in second best for querent ... seventh for Partner','A benefic in second favors the querent; a benefic in seventh favors the partner; directional source assignments differ.','second benefic -> querent; seventh benefic -> partner',''),
('conditional',[412],'ill Planet in the second, or node-like glyph ... querent get little','An ill planet in the second OR printed node-like glyph is said to imply little return for the querent, possible cheating and debts.','second-house malefic OR source glyph; position/scope of glyph remains unresolved','Not measured fraud or losses.'),
('conditional',[412],'Lord of the fourth apply ... eleventh by sextile or trine','Applying fourth lord to eleventh lord by sextile OR trine is offered as one favorable partnership-ending testimony.','fourth lord applies eleventh lord AND aspect sextile OR trine',''),
('conditional',[412],'or if a good Planet be in the fourth','A benefic located in the fourth is listed as an ALTERNATIVE favorable ending condition.','good planet fourth; OR with prior conditions',''),
('conditional',[412],'Lords of eleventh and fourth be in Reception','A reception relationship between eleventh lord and fourth lord is another alternative positive ending condition.','reception between eleventh and fourth lords',''),
('conditional',[412],'good Planets cast sextile or trine to Lords of ascendant and seventh','Benefics casting sextile or trine aspects to the first and seventh lords are an additional favorable end-of-partnership condition.','good planet aspects by sextile OR trine toward BOTH lords first and seventh',''),
('scope',[412],'observe Part of Fortune glyph, how dignified, how aspected','The scanned symbol appears to be the Part of Fortune; Lilly asks readers to inspect its dignities/aspects before the following negative qualification.','inspect printed circled-cross glyph condition; identity held provisional','Glyph visually resolved only to circled-cross appearance, not a universal referent.'),
('conditional',[412,413],'Lord of the seventh or eighth cast square or opposition to it','The seventh OR eighth lord squaring or opposing that printed point is claimed to indicate little good from a partner and possible embezzlement of property/common stock.','seventh OR eighth lord square OR opposition to circled-cross point','Historical forecast only; cross-page; precise symbolic referent remains flagged.'),
('boundary',[413],'CHAP. LVI. Whether a City, Towne or Castle ... shall be taken or not','Chapter LV ends above the printed divider on PDF413; Chapter LVI siege heading begins below and its body is excluded.','boundary only; no Chapter LVI siege claims','')
]
if len(data)!=32:raise AssertionError(len(data))
files=[]
for n in (411,412,413):
 p=B/f'evidence/pdf_1647-{n}.jpg'
 assert p.is_file() and p.stat().st_size>120000
 files.append({'original_pdf_page':n,'printed_page':n-34,'relative_path':str(p.relative_to(B)),'bytes':p.stat().st_size,'sha256':sha(p)})
window={'batch':'B03a','source_id':'LILLY1647_WELLCOME_B30338724','complete_original_pdf_sha256':PDF,
'status':'UNACCEPTED_SOURCE_FIRST_PREDECESSORS_LIII_AND_LIV_PENDING',
'chapter':'LV','last_accepted_lilly_at_source_snapshot':3071,
'prerequisites_before_global_numbering':['LIII acceptance','LIV acceptance and frozen R range'],
'physical_start':{'pdf_page':411,'printed_page':377,'position':'BELOW Chapter LIV divider'},
'physical_end':{'pdf_page':413,'printed_page':379,'position':'ABOVE Chapter LVI divider'},
'original_images_cached_no_download':True,'original_images':files,
'original_image_pixels_parity_to_full_pdf_not_claimed':True,
'full_independent_diplomatic_transcription_claimed':False,'empirical_cases':0}
rows=[]
for i,(role,pages,anchor,statement,conditions,uncertain) in enumerate(data,1):
 rows.append({'source_local_id':f'LV-C{i:03}','global_record_number':None,'chapter':'LV' if role!='boundary' else 'LVI_BOUNDARY_ONLY',
'book':'II','original_pdf_pages':pages,'printed_pages':[p-34 for p in pages],
'role':role,'anchor_editorially_shortened_not_diplomatic':anchor,
'conditional_statement_author_claim_not_empirical':statement,
'preconditions_and_disjunctions':conditions,'exception_or_ambiguity':uncertain,
'original_scan_authoritative':True,'new_independent_real_world_cases':0,
'validated_predictive_results':0,'historical_documentary_admitted':False,
'runtime_promoted':False})
for fname,obj in [
('SOURCE_WINDOW_MANIFEST.json',window),
('SOURCE_FIRST_CLAUSES_DRAFT.json',{'batch':'B03a','status':'PREDECESSOR_HELD_PROVISIONAL','source_units':len(rows),'source_original_pdf_sha256':PDF,'rows':rows}),
('SOURCE_ORDER_DRAFT.json',{'batch':'B03a','ordered_ids':[x['source_local_id'] for x in rows],'cross_page_ids':['LV-C008','LV-C009','LV-C031'],'next_chapter_marker':'LV-C032'})]:
 f=B/fname
 assert not f.exists()
 f.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('Provisional Chapter LV source-first records',len(rows),'span pages',[x['original_pdf_page'] for x in files])
