#!/usr/bin/env python3
"""Lilly Christian Astrology (1647) Book II Chapter LVI source-first documentary edition.
Original wellcome b30338724 scans are authority, not machine text.
Claims are AUTHORIAL historical assertions; NOT tested, NOT war advice.
"""
import hashlib, json, pathlib
P=pathlib.Path(__file__).resolve().parent
ROWS=[]
SPANS=[]
def segment(pages,label,*units):
    sid=f"LVI-S{len(SPANS)+1:03}"
    ids=[]
    for role,anchor,paraphrase,limits in units:
        rid=f"LVI-C{len(ROWS)+1:03}"
        ids.append(rid)
        ROWS.append({
            "local_id":rid,
            "global_record_number":None,
            "batch":"B03b","book":"II",
            "chapter":"LVI" if role!="next_heading_boundary" else "LVII_HEADING_NAVIGATION_ONLY",
            "role":role,
            "original_pdf_pages":list(pages),
            "original_printed_pages":[p-34 for p in pages],
            "original_source_abbreviated_anchor_not_full_quote":anchor,
            "historical_author_assertion_paraphrase":paraphrase,
            "predicates_and_caveats":limits,
            "original_1647_scan_authoritative":True,
            "complete_diplomatic_transcription":False,
            "source_first_provisional":True,
            "admitted_as_historical_documentation":False,
            "validated_by_real_world_cases":False,
            "runtime_predicate_active":False,
            "real_world_military_use_authorized":False
        })
    SPANS.append({
        "span_id":sid,"original_pdf_pages":list(pages),
        "original_printed_pages":[p-34 for p in pages],
        "source_passage_descriptive_label_not_quote":label,
        "local_source_ids":ids
    })
segment([413],"Chapter LVI begins after LV divider",
    ("heading","Chap. LVI. Whether a City, Towne or Castle ... shall be taken or not.",
     "A numbered question about whether a town, castle or city already under siege or subject to a future siege will be taken.",
     "Heading below physical divider on original PDF413 / printed379; no original Chapter LV business included."))
segment([413],"agents and respective house assignments",
    ("assignment","ascendant and his Lord are for the querent",
     "The author identifies ascendant and its lord with the querent and the besieging party.",
     "This LVI assignment is specific to the besieger's question; do not swap querent with besieged."),
    ("assignment","fourth house shall signifie the Towne, City or Fort besieged",
     "The fourth house signifies the town, city or fort under siege or to be besieged.",
     "The fort's fourth-house role is distinct from its governor."),
    ("assignment","the Lord thereof the Governour",
     "The fourth-house lord is given as the besieged place's governor.",
     "Do not conflate governor with besiegers' first lord."),
    ("assignment","the fift house ... Ammunition, Souldiery and Assistants",
     "The fifth house, its planetary occupants and its lord signify assistance, ammunition and soldiers expected by the governor and town.",
     "These are authorial chart assignments; no real logistics diagnostic is established."))
segment([413],"side margin qualifier for the fifth-house assistance",
    ("margin","in the Towne Garrison.",
     "The original marginal annotation qualifies the help as being in the town garrison.",
     "Marginal text aligned with the fifth-house assistance statement; punctuation and attribution not an independently tested criterion."))
segment([413],"first-house lord fortunate and possible linkage to fourth",
    ("conditional","Lord of the first strong and fortunate",
     "The author names a strong and fortunate first-house lord as an argument in favor of the besieging party.",
     "This appears as one branch of a long conditional with additional placement/reception language; it is not a standalone verified rule."),
    ("conditional","or joyned to the Lord of the fourth ... in the first",
     "He names conjunction with the fourth lord and first-house placement as another configuration in the capture discussion.",
     "Original 'and are in the first' has plural referent uncertainty; avoid inferring which one or both planetary lords must be there."),
    ("conditional","or with the Moon or Lord of the tenth ... except the twelft, eight and sixt",
     "He additionally names the Moon or tenth lord and certain house placements, expressly excluding the twelfth, eighth and sixth.",
     "The exact attachment of 'or with ...' to earlier conditions is grammatically uncertain; house exclusions must not be omitted."))
segment([413],"conditional reception and one-way Moon exception",
    ("conditional","conditionally, that the Lord of the first receive the Lord of the fourth",
     "Reception of the fourth lord by the first lord is identified as a relevant condition favoring capture.",
     "Reception direction is first receives fourth; source conditional ties back to the preceding complex clause."),
    ("conditional","or the Moon receive the Lord of the fourth, though she be not received againe",
     "Alternatively the Moon receives the fourth lord, even without reciprocal reception.",
     "Preserve one-way allowance; do not require mutual reception."),
    ("historical_outcome","it's an argument, the Towne, Fort or Castle shall be taken",
     "The preceding complicated conjunction/placement/reception indications are said to favor capture of the besieged place.",
     "This is historical author assertion only; not evidence or actionable siege advice."))
segment([413],"fourth lord in houses that do not behold fourth, with exception",
    ("conditional","Lord of the fourth be in such houses as behold not the fourth",
     "The text describes the fourth lord's placement in houses without aspect to the fourth as another capture testimony.",
     "Which houses 'behold not' is source-native terminology, not an enumerated set in this paragraph."),
    ("exception","except the Lord of the seventh be in the fourth, then it will not be taken",
     "A seventh-house lord in the fourth is an explicit exception predicting the place is not captured.",
     "The exception must override its immediately preceding fourth-lord condition; do not remove as inconsistent."))
segment([413],"fourth lord afflicted, and governor wounded",
    ("conditional","Lord of the fourth be with the ill Fortunes, and impedited",
     "Lilly considers a fourth lord afflicted together with unfavorable planets as an unfavorable state for the besieged town.",
     "Both contact and impediment appear; no operational definition of 'impedited' supplied."),
    ("historical_outcome","it's probable the City shall be taken, and the Governour wounded",
     "Under this afflicted fourth-lord state he conjectures capture and injury to the governor.",
     "The text uses 'probable', not an empirical calibrated probability."))
segment([413],"malefics in fourth without strong benefic protection",
    ("conditional","Infortunes be in the fourth without some strong aspect of the Fortunes",
     "He conditions another adverse judgment on malefics in the fourth without a strong benefic aspect.",
     "The exception for beneficial aspects is required; malefic occupancy alone is not the recorded full condition."),
    ("historical_outcome","It will be taken, or can it hold out long, or there may be treason in Towne",
     "Capture, inability to hold out, or possibly treason in the town are given as alternative historical forecasts.",
     "Original old-style question syntax 'or can it hold out long' is not silently resolved into a certain outcome."))
segment([413],"uncertain glyph in the fourth, treason claim and subarea",
    ("unresolved_symbol","If [node-like glyph] be in the fourth",
     "An astrological symbol resembling a node in the fourth house is associated with unfavorable town events.",
     "Do not silently normalize the printed glyph into a specific node or planet without independent symbolic adjudication."),
    ("historical_allegation","some goe about to betray or deliver it",
     "Lilly further alleges attempted betrayal or surrender by somebody in the town or a principal work or fort.",
     "A historical conjecture, not evidence that any real governor/inhabitant intends betrayal."),
    ("interpretation","the Signe shewes which part of the Towne",
     "The printed zodiac sign is said to indicate which part of the town the author means.",
     "No fixed mapping of signs to physical fort sectors is given; do not invent one."),
    ("historical_allegation","nor doth the Governour think himself able to preserve it",
     "He also attributes doubt about preserving the place to the governor.",
     "Unverified third-person mental-state claim; cannot be used as a personality diagnosis."))
segment([413],"fallback branch only if earlier configurations absent",
    ("scope","If none of these Accidents or Configurations before rehearsed be",
     "A later set of defensive indications is introduced only after the prior listed conditions have not occurred.",
     "This preceding-conditions-negative prerequisite controls the next fallback sequence."))
segment([413,414],"fourth lord strong and free of specified impediments, crossing page",
    ("conditional","Lord of the fourth ... fourth strong and fortunate",
     "The fallback considers the fourth lord strong and fortunate within the fourth house.",
     "Only in the preceding fallback context; not proof the town can resist."),
    ("exception","not Retrograde or Combust, or besieged of the Infortunes",
     "Retrogradation, combustion and being besieged by malefics are explicit exclusions from this favorable fourth-lord alternative.",
     "Do not treat retrograde/combust/besieged as beneficial conditions."))
segment([413,414],"alternative seventh lord and fortunate planets, page seam",
    ("conditional","Lord of the seventh be there, free from all impediments",
     "The seventh lord in the fourth, free from all impediments, is also named as a favorable holdout configuration.",
     "Keep even if unexpected under the earlier house role assignments; author's alternative remains literal."),
    ("conditional","or if Jupiter or Venus or [node-like glyph] be therein",
     "Jupiter, Venus, or an additional astrological glyph in the fourth house is given as another alternative.",
     "Original page break occurs after 'be'; the glyph may be a lunar node and remains unadjudicated."),
    ("conditional","and no reception between the Lord of the ascendant and fourth",
     "The fallback paragraph adds an absence of reception between the ascendant and fourth lords.",
     "The precise scope of this 'and' over the preceding alternatives is not fully resolved."))
segment([414],"no-surrender claim with no reception and fourth-house defenses",
    ("historical_outcome","shall not be taken or delivered to the Army now besieging it",
     "Under the preceding defensive fallback configurations Lilly predicts that the besieged place will not be taken or surrendered.",
     "This is an outcome conjecture, not confirmation from siege histories."))
segment([414],"both benefic and malefic in fourth, conditional priority",
    ("conditional","both a Fortune and an Infortune in the fourth",
     "Lilly explicitly considers both a benefic and malefic in the fourth, not just a single planet.",
     "Do not assume the mere presence of each resolves the outcome."),
    ("exception","Fortune be neerest to the cusp ... or first ... transit the degree of the fourth",
     "He says a benefic nearer the fourth cusp or first to transit the fourth degree favors the place's resistance.",
     "Retain two original alternatives and degree/transit wording; do not invent a new cusp orb."),
    ("historical_outcome","the Towne shall not be taken",
     "In that priority configuration he predicts that the town will not be taken.",
     "Follows specified cusp/first-transit priority, not any benefic occupation."))
segment([414],"weakened besieger first lord adds confidence",
    ("condition","greater confidence, if the Lord of the ascendant be any thing weak",
     "The author says the previous holdout reading is strengthened when the besieger's first lord is weak.",
     "His 'greater confidence' is qualitative source rhetoric, not a numerical probability."),
    ("condition","or a light Planet and unfortunate",
     "A light and unfortunate first lord is listed as another corroborating condition for holdout.",
     "Do not reverse the polarity of this defensive corroboration."))
segment([414],"fortunate besieger first lord and fortunate fourth house",
    ("conditional","Lord of the ascendant be fortunate, and a Fortune therein",
     "The author next contrasts a fortunate ascendant lord with a benefic in the fourth.",
     "Retain both positions and avoid treating one as sufficient."),
    ("conditional","and he or the Moon behold the fourth house",
     "The favorable besieging scenario also requires the first lord or Moon to aspect the fourth.",
     "The text has an explicit OR between first lord and Moon, plus fourth-house aspect."),
    ("historical_outcome","it notes surrendring or taking the City, Towne or Castle",
     "Under that opposing arrangement he predicts surrender or capture of the besieged place.",
     "Separate prediction from the preceding defensive priority rule."))
segment([414],"besieger first lord unfortunate plus second-house adversities",
    ("conditional","but if he be unfortunate and otherwayes impedited",
     "The subsequent adverse-besieger branch requires the first lord's misfortune and impediment.",
     "Antecedent 'he' refers to the ascendant lord in the preceding clause; keep this conditional."),
    ("conditional","and an Infortune in the second, or the Lord thereof Retrograde",
     "The second-house condition includes either a malefic there or retrogradation of its lord.",
     "Alternatives must not be collapsed to simultaneous requirements."),
    ("conditional","or in square or opposition to the Lord of the ascendant",
     "A hard aspect to the ascendant lord by the second-house lord is also listed.",
     "Scope refers to the just-mentioned second lord; don't infer exact orb, applying/separating status."))
segment([414],"negative consequences for besieging troops; material and pay alternatives",
    ("historical_outcome","querent's Souldiers will desert him, and will not continue the Siege",
     "The author speculates the besieging soldiers will desert or discontinue the siege.",
     "An untested, period-specific prediction, not an actionable forecast of military morale."),
    ("historical_outcome","wants fit instruments or materials ... Ammunition ... not come opportunely",
     "Alternative conjectures include inadequate siege equipment or delayed ammunition.",
     "These are historical descriptions, NOT a checklist for modern attack logistics."),
    ("historical_outcome","Souldiers will depart discontented for their pay ... duties are too hard",
     "The author also speculates pay dissatisfaction or excessive duties as reasons for troops leaving.",
     "No authenticated personnel records or causation is established."),
    ("historical_outcome","he may expect no honour at this Siege",
     "The paragraph concludes the besieger should not expect honor from the undertaking.",
     "Reputational interpretation is historical only; do not apply to present individuals."))
segment([414],"Chapter LVII navigation marker below original divider",
    ("next_heading_boundary","Chap. LVII. Of COMMANDERS in Armies ...",
     "Chapter LVII on army commanders begins below the divider on PDF414/printed380; it is not part of the LVI body.",
     "Navigation-only heading, no LVII source assertions counted."))
assert len({r['local_id'] for r in ROWS})==len(ROWS)
assert [r['local_id'] for r in ROWS]==[f'LVI-C{i:03}' for i in range(1,len(ROWS)+1)]
assert SPANS[0]['original_pdf_pages']==[413] and SPANS[-1]['original_pdf_pages']==[414]
assert all(all(413<=p<=414 for p in s['original_pdf_pages']) for s in SPANS)
assert [s['original_pdf_pages'][0] for s in SPANS]==sorted(s['original_pdf_pages'][0] for s in SPANS)
assert ROWS[-1]['role']=='next_heading_boundary'
def dump(f,o):
 (P/f).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
images=[]
for page in [413,414]:
 f=P/'evidence'/f'pdf_1647-{page}.jpg'
 data=f.read_bytes()
 images.append({'original_pdf_page':page,'printed_page':page-34,
   'path':f.relative_to(P).as_posix(),'bytes':len(data),
   'sha256':hashlib.sha256(data).hexdigest(),
   'witness':'Wellcome 1647 IIIF scan original b30338724'})
dump('SOURCE_FIRST_CLAUSES_DRAFT.json',{
 'batch':'B03b','status':'ORIGINAL_IMAGE_REVIEW_PROVISIONAL_NOT_CANONICAL',
 'source_original_pdf_sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b',
 'source_units':len(ROWS),'independent_full_diplomatic_transcription_claimed':False,
 'rows':ROWS})
dump('ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',{
 'batch':'B03b','status':'SOURCE_FIRST_MANUALLY_COLLATED_PROVISIONAL',
 'span_count':len(SPANS),'source_spans':SPANS,
 'draft_units':len(ROWS),'complete_independent_diplomatic_transcription_claimed':False,
 'source_window':'PDF413 below LVI divider through PDF414 above LVII divider'})
dump('SOURCE_ORDER_DRAFT.json',{
 'batch':'B03b','status':'PROVISIONAL',
 'ordered_local_ids':[r['local_id'] for r in ROWS],
 'cross_page_ids':[r['local_id'] for r in ROWS if len(r['original_pdf_pages'])>1],
 'last_navigation_only':ROWS[-1]['local_id']})
dump('SOURCE_WINDOW_MANIFEST.json',{
 'batch':'B03b','status':'PROVISIONAL_SOURCE_FIRST',
 'complete_original_pdf_sha256':'2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b',
 'source_original_pdf_pages':[413,414],
 'source_printed_pages':[379,380],
 'first_position':'PDF413 below Chapter LV divider',
 'end_position':'PDF414 above Chapter LVII divider',
 'images':images,'full_original_pdf_repacked':False,
 'independent_diplomatic_second_reader':False,
 'prior_accepted_lilly':3203,'next_chapter':'LVII'})
dump('UNRESOLVED_SOURCE_LIMITS.json',{
 'batch':'B03b','status':'RETAINED_OPEN_DO_NOT_INFER',
 'issues':[
 {'id':'B03b-U01','source':'PDF413','issue':'LVI below the LV divider; prior partnership paragraph above must be excluded.'},
 {'id':'B03b-U02','source':'PDF413 margin','issue':'Garrison marginal annotation refers to original fifth-house material; does not certify a military logistics rule.'},
 {'id':'B03b-U03','source':'PDF413','issue':'The original long first-lord fortune/conjunction/placement clause has unclear attachment of some OR branches and plural "are in the first".'},
 {'id':'B03b-U04','source':'PDF413','issue':'Do not remove the express twelfth, eighth and sixth house exclusions.'},
 {'id':'B03b-U05','source':'PDF413','issue':'Moon receiving fourth lord even without reciprocal reception is expressly allowed.'},
 {'id':'B03b-U06','source':'PDF413','issue':'The fourth-lord houses unable to behold fourth are not enumerated and the author gives a seventh-lord-in-fourth exception.'},
 {'id':'B03b-U07','source':'PDF413','issue':'The phrase "or can it hold out long" may be rhetorical or negated by context: preserve unresolved old syntax.'},
 {'id':'B03b-U08','source':'PDF413','issue':'A node-like glyph in fourth is not positively identified from the single 1647 scan.'},
 {'id':'B03b-U09','source':'PDF413','issue':'Original claims about treason/governor intention are unverified allegations and never individual diagnoses.'},
 {'id':'B03b-U10','source':'PDF413-414','issue':'Fallback begins only when prior accidents/configurations absent; fourth lord must avoid retrogradation, combustion, and malefic enclosure.'},
 {'id':'B03b-U11','source':'PDF413-414','issue':'The glyph among Jupiter/Venus/other signs at page seam remains unadjudicated; AND no reception may attach across alternatives.'},
 {'id':'B03b-U12','source':'PDF414','issue':'Benefic in fourth plus malefic is conditioned on benefic nearest cusp or first to transit fourth degree; no orb inferred.'},
 {'id':'B03b-U13','source':'PDF414','issue':'First lord weak gives qualitatively greater confidence to defensive forecast, not numerical confidence.'},
 {'id':'B03b-U14','source':'PDF414','issue':'Second lord square/opposition is source-native with unspecified orb/application; alternatives kept distinct.'},
 {'id':'B03b-U15','source':'PDF414','issue':'Historical troop, pay, siege instruments, ammunition claims are not validated tactical instructions or observed cases.'},
 {'id':'B03b-U16','source':'PDF414','issue':'Chapter LVII commander title begins below divider; none of its body included in LVI.'},
 {'id':'B03b-U17','source':'PDF413-414','issue':'No full blind second diplomatic transcription, independently tested horoscope prediction, case outcome, or live runtime promotion.'}
 ]})
dump('CLAIM_LEDGER.json',{
 'batch':'B03b','status':'PROVISIONAL_HISTORIC_SOURCE_ONLY',
 'new_source_first_units':len(ROWS),'image_reverse_spans':len(SPANS),
 'original_source_images':2,'prior_accepted_lilly':3203,
 'new_canonical_lilly':0,'new_empirical_siege_forecasts':0,
 'new_authenticated_real_conflict_outcomes':0,'new_runtime_predicate_promotions':0,
 'next_numbered_chapter':'LVII'})
print(json.dumps({'batch':'B03b','provisional_editorial_units':len(ROWS),
                  'source_spans':len(SPANS),'source_pdf_pages':[413,414],
                  'new_canonical_records':0}))
