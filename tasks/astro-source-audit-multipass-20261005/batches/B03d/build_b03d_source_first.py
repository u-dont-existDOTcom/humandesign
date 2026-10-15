#!/usr/bin/env python3
"""Source-first historical text annotations, Lilly 1647 Book II Chapter LVIII.
No true person-level hidden hostility assessment or validated predictive accuracy.
"""
import pathlib,json,hashlib
P=pathlib.Path(__file__).resolve().parent
R=[];S=[]
def segment(pages,label,*units):
 sid=f'LVIII-S{len(S)+1:03}'
 ids=[]
 for role,anchor,sense,limits in units:
  rid=f'LVIII-C{len(R)+1:03}';ids.append(rid)
  R.append({'source_local_id':rid,'global_record_number':None,
   'batch':'B03d','book':'II',
   'chapter':'LVIII' if role!='next_heading_boundary' else 'LIX_HEADING_ONLY',
   'role':role,
   'original_pdf_pages':list(pages),
   'printed_pages':[p-34 for p in pages],
   'source_short_anchor_not_diplomatic':anchor,
   'historical_claim_paraphrase':sense,
   'conditions_and_limits':limits,
   'original_image_authority':True,
   'source_first_provisional':True,
   'independently_blind_diplomatic_transcription':False,
   'historical_documentation_accepted':False,
   'observed_real_adversary_cases':0,
   'empirical_predictive_validation':False,
   'active_personality_or_honesty_classifier':False,
   'runtime_model_promoted':False})
 S.append({'span_id':sid,'original_pdf_pages':list(pages),
  'printed_pages':[p-34 for p in pages],
  'source_passage_label_not_quote':label,
  'mapped_source_local_ids':ids})
segment([417],"numbered chapter LVIII below preceding physical divider",
 ('heading','Chap. LVIII. If the Querent have open Enemies, or any Adversaries or many that doe envy him.',
  "The chapter heading asks whether the querent has enemies or adversaries, including people alleged to envy them.",
  "Original PDF417/printed383 below the LVII/LVIII divider; previous section on potential fighting belongs to LVII."))
segment([417,418],"original opening separates absolute question from named individual suspicion",
 ('scope','difficult Question, and yet by Astrologie responsible',
  "The author presents the question as difficult but in his view answerable through astrology.",
  "An author assertion, not empirical verification."),
 ('scope','Have I enemies or not?',
  "He explicitly distinguishes the general existence-of-enemies question.",
  "Source paragraph begins on PDF417 and continues on PDF418."),
 ('scope','Whether is such a man my adversary?',
  "He also distinguishes the question about a particular nominated person.",
  "Do not use the broad twelfth-house test as a shortcut for the named-person case."))
segment([418],"marginal source note for family/servant nominees",
 ('margin','But if the querent doubt his Brother, Father, or Servant',
  "Original marginal note distinguishes suspected relatives or a servant from an arbitrary nominated party.",
  "This is part of the historical classification only, not proof of anyone's hostility."),
 ('assignment','take Signification from each particular House',
  "The author says to consider each named relationship's own house.",
  "Do not default every relative to the ordinary seventh-house stranger assignment."))
segment([418],"nominated person assessed by seventh house and Lord",
 ('assignment','If any be nominated, require judgment from the seventh house and Lord',
  "A specifically nominated person is first evaluated by the seventh and its lord.",
  "The margin qualifies family/servant cases separately."),
 ('condition','Lord of the seventh aspect the Lord of the ascendant ... square or opposition',
  "A hard square/opposition from seventh lord to ascendant lord is one original source test.",
  "Explicit aspect to first lord; not any seventh-house placement."),
 ('condition','or be in like aspect with the Moon',
  "A corresponding square/opposition to Moon is an alternative.",
  "Preserve the OR alternative."))
segment([418],"named person envy assertion from hard aspect",
 ('historical_allegation','party enquired after doth envy the Querent, and wishes him no good',
  "Under the hard-aspect branches the author attributes ill will to a nominated person.",
  "This is NOT a demonstrated fact about that person or any present-day relationship."))
segment([418],"separating/applying distinguishes timeline",
 ('condition','if the aspect be separated',
  "The original differentiates a separating aspect from an applying one.",
  "Applies to the preceding hard-aspect test."),
 ('historical_allegation','they have lately been in some contest',
  "With separation the author speculates about recent disagreement.",
  "No case outcome independently authenticated."),
 ('condition','if ... applying to a square or opposition',
  "An applying hard aspect is a separate condition.",
  "Do not treat as the same tense as separating."),
 ('historical_allegation','enmity ... approaching ... grow to a greater height',
  "He conjectures that conflict continues or worsens under application.",
  "Untested future-event assertion and mind-reading allegation."))
segment([418],"named nominee twelfth-placement alternatives",
 ('conditional','Lord of the seventh be in the twelfth from the ascendant',
  "The author names the seventh lord in the twelfth house as another source condition.",
  "Do not conflate with relative sign positions."),
 ('conditional','in the twelft signe from the place wherein the Lord of the ascendant is',
  "He also considers the twelfth sign reckoned from the ascendant lord's position.",
  "Original turned-sign counting convention not formalized here."),
 ('conditional','or from the place wherein the Moon is',
  "The twelfth-sign placement relative to Moon is a further alternative.",
  "Not the same as the direct twelfth house."))
segment([418],"intermediary planet connections, negative reception",
 ('conditional','Lord of the seventh be in conjunction with any Planet',
  "A conjunction involving the seventh lord and another planet begins a longer alternative.",
  "The relevance depends on what other planet connects to the first lord or Moon."),
 ('conditional','or in any aspect with a Planet ... conjunction or square to the Lord of the ascendant or the Moon',
  "The text also describes an intermediary planet connecting to the first lord or Moon by conjunction or square.",
  "Grammar of conjunction/aspect alternation retained without inventing a scored graph."),
 ('condition','without Reception',
  "The text explicitly excludes reception for the intermediary hard-aspect branch.",
  "Scope over every preceding OR is uncertain; do not remove this condition."))
segment([418],"conclusion for named person; otherwise no enemy",
 ('historical_allegation','then the Quesited ... is averse, and an enemy',
  "Under the preceding named-person configurations the author labels the nominee hostile.",
  "Unverified allegation; never use as real accusation of an identifiable person."),
 ('limitation','but if it be not so ... no enemy',
  "The text supplies a negative conclusion if the specified configurations are absent.",
  "Do not treat silence, other charts, or unknown responses as positive evidence."))
segment([418],"general un-nominated inquiry uses twelfth",
 ('scope','If the Question be absolute ... Whether have I enemies, yea or no?',
  "The author returns to the general, unnamed-enemies question.",
  "This distinct branch excludes nominated-person readings."),
 ('assignment','require judgment herein from the twelfth house',
  "The twelfth and its lord signify hidden opposition in the author's general-question framework.",
  "Source-native house meaning only."))
segment([418],"twelfth lord and Moon hard aspects with or without reception",
 ('conditional','Lord of [twelfth] be in square or opposition to the Moon',
  "The twelfth lord aspecting Moon by square/opposition is offered as a general-question condition.",
  "Requires the specific two signs/lords, not all twelfth-house aspects."),
 ('condition','with or without Reception',
  "Unlike the nominated intermediary branch, the source allows the aspect with OR without reception.",
  "Preserve the distinct reception rule."),
 ('historical_allegation','he hath enemies that watch for an opportunity against him',
  "The author conjectures concealed adversaries.",
  "Never applied to a current person's real safety or suspicions."))
segment([418],"clandestine acts and possibility of disguising enmity",
 ('historical_allegation','they doe all things clandestinely and cunningly',
  "Lilly elaborates that the supposed enemies may act covertly.",
  "Not evidence of a conspiracy."),
 ('historical_allegation','still goe under the notion of Friends',
  "He conjectures disguised friendship as another interpretation.",
  "Unverified claim and especially vulnerable to unfalsifiable retrospective fitting."))
segment([418],"where twelfth lord falls and how many planets seventh",
 ('scope','Consider also where and in what house the Lord of the twelfth is',
  "The author proposes considering the house placement of the twelfth lord to describe alleged adversaries.",
  "No fixed verified psychological profiler."),
 ('historical_outcome','Many Planets in the seventh, denotes many enemies',
  "He equates many seventh-house planets with many adversaries.",
  "No count threshold or independent population-base-rate data supplied."))
segment([418],"original author's first-person anecdotal note",
 ('marginal_author_claim','Often and ever by me found true.',
  "The original margin contains a first-person assertion of repeated success.",
  "Anecdotal author claim; NOT an audited empirical test or reproducible case count."))
segment([418],"second-house planet count and money lack",
 ('conditional','many Planets in the second',
  "The author includes a separate multiple-planet-second-house observation.",
  "Do not confuse this with seventh-house enemy-count rule."),
 ('historical_outcome','much want of money, if they are ill dignified',
  "He associates an ill-dignified second-house cluster with financial lack.",
  "Explicit ill-dignity condition; no actual financial case evidence."))
segment([418,419],"next-page continuation of house-person descriptions",
 ('scope','what houses they are Lords of ... quality of people',
  "Planets in the seventh and the houses those planets rule are used to conjecture descriptions of supposed adversaries.",
  "Source passage continues from PDF418 to PDF419; no person-specific profiling is validated."))
segment([419],"square and opposition contrasts and possibility of reconciliation",
 ('conditional','square aspect shewes envy and malice, yet possible to be reconciled',
  "The author treats square as alleging ill will yet permitting reconciliation.",
  "Only a literal source claim; not advice about identifying hostile relationships."),
 ('conditional','opposition aspects without Reception, never',
  "Without reception, opposition is described as an enduring obstacle to reconciliation.",
  "Reception absence is explicit. A categorical 'never' is the author's rhetoric, not observed certainty."))
segment([419],"physical heading-only boundary for next chapter",
 ('next_heading_boundary','Chap. LIX. A Lady, if marry the Gentleman desired?',
  "Chapter LIX begins below the original divider on PDF419/printed385 and contains a worked chart.",
  "Navigation marker only; the chart and its analysis are for the next source batch."))
assert len({r['source_local_id'] for r in R})==len(R)
assert [r['source_local_id'] for r in R]==[f'LVIII-C{i:03}' for i in range(1,len(R)+1)]
assert S[0]['original_pdf_pages']==[417] and S[-1]['original_pdf_pages']==[419]
assert [s['original_pdf_pages'][0] for s in S]==sorted(s['original_pdf_pages'][0] for s in S)
assert R[-1]['role']=='next_heading_boundary'
def dump(p,v):(P/p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
imgs=[]
for pdf in (417,418,419):
 p=P/'evidence'/f'pdf_1647-{pdf}.jpg';b=p.read_bytes()
 imgs.append({'original_pdf_page':pdf,'printed_page':pdf-34,
 'relative_path':p.relative_to(P).as_posix(),
 'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{'batch':'B03d','status':'PROVISIONAL_SOURCE_FIRST',
 'original_pdf_sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b',
 'units':len(R),'independent_diplomatic_full_transcription_claimed':False,'rows':R})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{'batch':'B03d','status':'PROVISIONAL',
 'source_spans':S,'span_count':len(S),'editorial_units':len(R),
 'original_window':'PDF417 below prior divider to PDF419 above next divider',
 'empirically_verified_people':0})
dump('SOURCE_WINDOW_MANIFEST.json',{'batch':'B03d','status':'PROVISIONAL',
 'source_full_pdf_sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b',
 'source_original_pdf_pages':[417,418,419],
 'opening':'PDF417 below Chapter LVII divider',
 'closing':'PDF419 above Chapter LIX divider',
 'images':imgs,'previous_accepted_lilly_count':3322,'next_numbered_chapter':'LIX',
 'complete_independent_diplomatic_reading':False})
dump('SOURCE_ORDER_DRAFT.json',{'batch':'B03d','status':'PROVISIONAL',
 'ordered_ids':[r['source_local_id'] for r in R],
 'cross_page_ids':[r['source_local_id'] for r in R if len(r['original_pdf_pages'])>1],
 'next_navigation_only_id':R[-1]['source_local_id']})
dump('UNRESOLVED_SOURCE_LIMITS.json',{'batch':'B03d','status':'RETAIN_UNRESOLVED',
 'issues':[
 {'id':'B03d-U01','source':'PDF417','note':'LVII section above divider excluded; LVIII opens after divider.'},
 {'id':'B03d-U02','source':'PDF417-418','note':'Named nominee and unnamed/general enemies are two distinct questions with different house roles.'},
 {'id':'B03d-U03','source':'PDF418 margin','note':'Brother, father, servant suspected require their relation-specific house, not automatically seventh.'},
 {'id':'B03d-U04','source':'PDF418','note':'Separation of square/opposition alleges past dispute; application alleges potential future escalation. Neither verified.'},
 {'id':'B03d-U05','source':'PDF418','note':'Twelfth house, twelfth sign from first lord, and twelfth sign from Moon are distinct alternatives.'},
 {'id':'B03d-U06','source':'PDF418','note':'Intermediary planet wording is ambiguous over multiple conjunction/aspect branches; do not invent algorithm.'},
 {'id':'B03d-U07','source':'PDF418','note':'Absence of reception in named-person condition vs with-or-without in general question must remain separate.'},
 {'id':'B03d-U08','source':'PDF418','note':'Claims that people are enemies, hateful or disguised as friends are unverified, risky to apply to real persons.'},
 {'id':'B03d-U09','source':'PDF418 margin','note':'Authors "often and ever by me found true" is not independent case evidence or validation.'},
 {'id':'B03d-U10','source':'PDF418','note':'Financial lack second-house reading requires ill-dignified condition; is another topic in LVIII.'},
 {'id':'B03d-U11','source':'PDF418-419','note':'House lord descriptions of alleged enemies have no fixed validated person profile.'},
 {'id':'B03d-U12','source':'PDF419','note':'Square says reconciliation possible, opposition without reception uses "never"; no calibrated probability.'},
 {'id':'B03d-U13','source':'PDF419','note':'LIX marriage worked chart begins below divider and chart data are not included in LVIII.'},
 {'id':'B03d-U14','source':'PDF417-419','note':'Historical authorial claims are not independent real-world cases, predictive validation, or runtime scoring rules.'}]})
dump('CLAIM_LEDGER.json',{'batch':'B03d','status':'PROVISIONAL_SOURCE_FIRST',
 'provisional_editorial_units':len(R),'source_spans':len(S),
 'previous_accepted_lilly_count':3322,'new_globally_accepted':0,
 'independent_confirmations_of_hidden_adversaries':0,
 'new_predictive_validations':0,'runtime_promotions':0})
print({'batch':'B03d','draft_source_units':len(R),'passages':len(S),'next':'LIX'})
