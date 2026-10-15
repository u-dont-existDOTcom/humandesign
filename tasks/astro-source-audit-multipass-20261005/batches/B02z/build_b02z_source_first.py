"""Deterministically assemble bounded, PREDECESSOR-HELD Lilly LIV documentary notes.

Never accepts, numbers globally, changes models, or pushes any Git ref.
All anchors are editorial abbreviations checked on scanned 1647 images.
"""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
P=ROOT/'evidence'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
SOURCE='LILLY1647_WELLCOME_B30338724'
ORIGINAL_SHA='2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
INPUT=[
# role, page refs, short source anchor, conditional statement, source conditions/limits
('heading',[410],'CHAP. LIV. Of Buying and Selling Commodities.','Chapter LIV begins below the printed divider following Chapter LIII.',''),
('assignment',[410],'The Buyer is signified by the Lord of the ascendant and the Moon','Lilly assigns the buyer to the ascendant lord AND Moon in this buying/selling question.','source-defined buyer: Lord of first + Moon'),
('assignment',[410],'the Seller by the Lord of the seventh','Lilly assigns the seller to the seventh-house lord.','source-defined seller: Lord of seventh'),
('conditional',[410],'Moon be joyned with the Lord of the seventh','A Moon/seventh-lord conjunction is given as a testimony that the querent may buy the desired commodity quickly.','Moon conjunct seventh lord'),
('conditional',[410],'Lord of the ascendant be a more light Planet then the Lord of the seventh','A lighter first-house lord than seventh-house lord is said to give the querent the initiative in occasioning the sale.','first lord lighter than seventh lord'),
('converse',[410],'& e contra, if the Lord of the seventh be the lighter Planet','The text gives a converse for a lighter seventh-house lord, without an independently enumerated full inverse algorithm.','seventh lord lighter than first lord; do not infer numeric strengths or timing'),
('conditional',[410],'preceding Significators have no aspect ... Moon or some other Planet transferre ... light','If the preceding significators lack an aspect but the Moon or another planet transfers light between them, an intermediary is predicted.','NO direct aspect AND translation of light via Moon OR another planet'),
('outcome',[410],'a Friend shall then appear ... drive on the bargaine for them both','The intermediary in the immediately preceding light-translation condition is said to bring the bargain to completion for both parties.','depends on condition of C007; not independent testimony'),
('taxonomy',[410],'Servant or Sheep, Hogges, Coneys ... the sixt house and his Lord','For servants or sheep, pigs, rabbits and similar goods, consult the sixth house and its lord.','commodity is servant OR sheep OR hog OR rabbit etc.'),
('taxonomy',[410],'Horses, Asses, Camels, Oxen or Cowes ... twelfth house and the ascendant','For horses, asses, camels, oxen or cows, Lilly assigns the twelfth house and ascendant.','commodity is horse OR ass OR camel OR ox OR cow'),
('taxonomy',[410],'House, Towne or Castle ... fourth house and his Lord','For houses, towns or castles, consult the fourth house and its lord.','commodity is house OR town OR castle'),
('scope',[410],'and so consider in any other Commodity','The author tells the reader to adapt house-signification to other commodities; no complete commodity list or general exhaustive classifier is supplied.','open-ended authorial instruction; no added associations'),
('conditional',[410],'Lord of the seventh be in the ascendant ... Seller will importune','Seventh lord in the ascendant is said to mean the seller presses the querent to buy.','seventh-house lord located in the first'),
('conditional',[410],'Lord of the ascendant be in the seventh ... querent hath most mind to buy','First lord in the seventh is said to show the querent most inclined to buy.','first-house lord located in seventh; not same as C013'),
('conditional',[410],'either Jupiter or Venus be in the ascendant ... Buyer performes ... suddenly','Either Jupiter OR Venus in the ascendant is said to permit sudden buyer completion without labor.','Jupiter OR Venus in first house'),
('conditional',[410],'so if the Sun be in the ascendant and not corporally joyned','Sun in ascendant is offered as an alternative quick-buyer condition only when NOT corporally conjunct another planet.','Sun first AND not corporally conjunct any other planet'),
('conditional',[410],'Mercury or Moon in ascendant, not infected ... evill aspect of an Infortune','Mercury OR Moon in the first, without an evil malefic aspect, is said to favor the buyer completing the intended bargain.','Mercury OR Moon first AND no evil aspect from malefic'),
('conditional',[410,411],'Saturn Mars or node-like glyph in the ascendant ... labour and difficulty','The printed Saturn/Mars/node-like first-house condition predicts labor and difficulty, with its final words continuing on printed page 377.','Saturn OR Mars OR printed node-like glyph in first; glyph interpretation retained'),
('outcome',[410,411],'Buyer is a cunning companion ... deceive the Seller if possible','Following the first-house malefic condition, Lilly further claims the buyer will act deceitfully toward the seller; this is a historical allegation not evidence of any real buyer.','depends on preceding malefic first-house premise C018'),
('conditional',[411],'Infortunes be in the seventh ... Seller ... delude the Buyer','Malefics in seventh are said to warn of seller deception toward the buyer.','malefic planet(s) located in seventh house'),
('conditional',[411],'Moon be voyd of course, unlesse the Significators apply strongly','Moon void-of-course is said to hinder conclusion or purchase and produce pointless bargaining, unless the significators apply strongly.','Moon VOC AND no strong significator application; the exception is essential'),
('conditional',[411],'Planet from whom the Moon separates enters Combustion','The author claims sellers of land or house will never recover the property if the planet Moon separated from enters combustion.','sale of land OR house AND Moon previous separating planet enters combustion'),
('conditional',[411],'Moon did last separate ... free from misfortune ... beholds the Lord of that Sign','If Moon last separated from a planet free of misfortune that beholds the relevant sign-lord, the author says the seller might later repurchase property or goods of equivalent value.','Moon former separating planet free from misfortune AND beholds relevant sign lord; referent uncertain'),
('boundary',[411],'CHAP. LV. Of Partnership.','Chapter LIV ends immediately above the horizontal divider; the Chapter LV partnership heading appears below it, with its body excluded.','navigation marker only; no Chapter LV claims')
]
manifest={'batch':'B02z','status':'PROVISIONAL_PREDECESSOR_CHAPTER_LIII_NOT_YET_ADMITTED',
'source_id':SOURCE,'original_full_pdf_sha256':ORIGINAL_SHA,
'prior_accepted_lilly_at_frozen_start':3071,'last_accepted_chapter':'LII',
'predecessor_still_open':'LIII','own_chapter':'LIV',
'original_pages':[410,411],'original_printed_pages':[376,377],
'opening':'PDF410 below horizontal divider after Chapter LIII','closing':'PDF411 above divider before Chapter LV',
'witness_kind':'EARLIER_AVAILABLE_1647_SOURCE_IMAGE_COPIES_NOT_FULL_PDF',
'images':[],'complete_full_diplomatic_second_transcription_claimed':False}
for n in (410,411):
 p=P/f'pdf_1647-{n}.jpg'
 assert p.is_file() and p.stat().st_size>100000
 manifest['images'].append({'pdf_page':n,'printed_page':n-34,'path':str(p.relative_to(ROOT)),'size_bytes':p.stat().st_size,'sha256':sha(p)})
if len(INPUT)!=24:raise AssertionError(('draft rows changed',len(INPUT)))
rows=[]
for i,(role,pages,anchor,statement,predicates) in enumerate(INPUT,1):
 assert anchor and statement and all(p in (410,411) for p in pages)
 rows.append({'local_id':f'LIV-C{i:03}','global_record_number':None,'batch':'B02z','source':'William Lilly Christian Astrology 1647 original Wellcome b30338724',
 'book':'II','chapter':'LIV' if role!='boundary' else 'LV_HEADING_NAVIGATION_ONLY',
 'original_pdf_pages':pages,'original_printed_pages':[p-34 for p in pages],
 'source_anchor_editorial_abbreviation':anchor,
 'source_anchor_claimed_word_for_word_complete':False,
 'source_statement_paraphrase':statement,'source_predicates_and_qualifiers':predicates,
 'record_role':role,'source_original_image_is_authoritative':True,
 'is_provisional':True,'accepted_historical_documentary':False,
 'empirically_verified_case':False,'model_runtime_promotion':False,'safe_for_real_person_prognosis':False})
for name,obj in [('SOURCE_WINDOW_MANIFEST.json',manifest),('SOURCE_FIRST_CLAUSES_DRAFT.json',{'batch':'B02z','status':'UNACCEPTED_SOURCE_FIRST','rows':rows,'record_count':len(rows),'source_id':SOURCE,'authoring_method':'Independent direct visual reading of three original typographical regions across two printed pages; no OCR, no empirical validation'}),('SOURCE_ORDER_DRAFT.json',{'batch':'B02z','status':'PROVISIONAL','ordered_local_ids':[r['local_id'] for r in rows],'cross_page_local_ids':['LIV-C018','LIV-C019'],'chapter_LV_heading_boundary_only':'LIV-C024'})]:
 p=ROOT/name
 assert not p.exists(),p
 p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('B02z source-first provisional',len(rows),'units; original image sha',*[z['sha256'] for z in manifest['images']])
