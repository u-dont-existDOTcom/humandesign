#!/usr/bin/env python3
"""Lilly (1647) Chapter LXVIII wife's portion: historical source-first edition."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
ROWS=[];SPANS=[]
def group(pages,label,*clauses):
    sid=f"LXVIII-S{len(SPANS)+1:03}"
    ids=[]
    for role,anchor,meaning,limitation in clauses:
        local=f"LXVIII-C{len(ROWS)+1:03}"
        ids.append(local)
        ROWS.append({
          "source_local_id":local,"batch":"B03n","book":"II",
          "chapter":"LXVIII" if role!="navigation_boundary" else "LXIX_NAVIGATION_ONLY",
          "role":role,"original_pdf_pages":list(pages),
          "original_printed_pages":[p-34 for p in pages],
          "editorially_shortened_anchor_not_diplomatic":anchor,
          "historical_author_paraphrase":meaning,
          "conditions_scope_and_uncertainty":limitation,
          "global_record_number":None,
          "original_source_witness_authoritative":True,
          "documentary_admitted":False,
          "independent_wealth_outcome_authenticated":False,
          "validated_predictive_case":False,"runtime_model_promoted":False
        })
    SPANS.append({"span_id":sid,"original_pdf_pages":list(pages),
      "source_passage_label":label,"mapped_source_local_ids":ids})
group([446],"Next numbered dowry/wealth chapter below LXVII divider",
 ("heading","CHAP. LXVIII. Whether Portion of Wife be great or easily obtained",
  "Chapter LXVIII concerns the promised portion or dowry of a prospective wife.",
  "Starts PDF446/printed412 below the LXVII horizontal divider."),
 ("heading_detail","whether Woman enquired after rich or not",
  "A related question asks about the woman's wealth.",
  "Question is framed historically, with no independently known wife or estate."))
group([446],"Querent and property/fortune assignments",
 ("scope","vary your ascendant and Question man as woman",
  "The author says the figure must be adapted to whether a man or woman is the subject.",
  "Questioner's sex alone does not dictate whether proposed spouse owns property."),
 ("figure_assignment","querent first house and Lord",
  "The first house and its ruler signify the one asking.",
  "Source-native horary signification, not observed income."),
 ("figure_assignment","his substance and Estate second house and Lord",
  "The second house and ruler stand for the questioner's own estate.",
  "Different from the proposed spouse's portion, assigned to eighth."),
 ("figure_assignment","Planet or Planets in second",
  "Planets placed in the second house supplement the querent's estate appraisal.",
  "Placement is separate from rulership."),
 ("figure_assignment","Lord of Part of Fortune and its place and sign",
  "Lilly also considers the Part of Fortune's ruler, placement and sign.",
  "No independent numerical weighting or personal wealth validation."))
group([446,447],"Where to consider the woman's dowry and eighth-house ruler",
 ("scope","Woman he enquires after ... rich",
  "The paragraph brings the question back to wealth of the proposed partner.",
  "Begins end PDF446 and continues PDF447."),
 ("figure_assignment","Sign of eighth house, Lord, Planet posited",
  "The eighth-house sign, ruler and planets located there are used for the partner's portion.",
  "Eighth is derived second from the seventh; distinct from querent's own second."))
group([447],"Benefic terms/occupancy and dignity with delays",
 ("conditional","cusp eighth Terms of Jupiter or Venus",
  "The terms of Jupiter or Venus on eighth cusp are called favorable testimony.",
  "A favorable cusp alone is not a measured estate outcome."),
 ("conditional","Jupiter or Venus posited eighth",
  "Jupiter or Venus occupying eighth is another favorable alternative.",
  "Occupancy requires subsequent condition of dignity."),
 ("conditional","essentially dignified direct free from Combustion",
  "Lilly qualifies abundant wealth by essential dignity, direct motion and absence of combustion.",
  "These are conjunctive extra conditions, not optional decorative details."),
 ("source_internal_forecast","plenty of Wealth",
  "He predicts an ample portion under strong benefic conditions.",
  "No independently validated marriage or dowry case."),
 ("exception","Retrograde Combust or slow in motion",
  "Retrogradation, combustion or slow motion reduce the favorable conclusion.",
  "The original permits a considerable estate despite these hindrances."),
 ("historical_inference","sufficient large portion with kind of trouble",
  "The author says substantial wealth might still be obtained, but with difficulties.",
  "Amount versus ease of obtaining it must be scored separately."))
group([447],"Eighth lord in eighth and inheritance contingencies",
 ("conditional","Lord eighth in eighth no-ways impedited",
  "An unimpeded eighth lord in its house is linked to the wife's inheritance.",
  "Absence of impediment is explicit."),
 ("historical_inference","inheritance land Legacy estate fall to Wife",
  "Lilly expects land or inherited assets to come to the woman.",
  "Historical conjecture only; cannot establish legal entitlement."),
 ("conditional","fourth or tenth and eighth Lords benevolent aspect",
  "He adds a supportive relationship involving fourth or tenth and eighth lords.",
  "Original allows fourth OR tenth; accompanying angle/succedent qualifiers apply."),
 ("conditional","angles succedent houses or eleventh and eighth",
  "Angular, succedent and particular house placements are listed as corroboration.",
  "Original syntax has alternative placements; do not force simultaneity."),
 ("historical_inference","more certain of inheritance",
  "The author increases confidence in inheritance if those supportive conditions are present.",
  "Qualitative wording, not a calibrated prediction."))
group([447],"Part of Fortune in eighth and benevolent aspects",
 ("conditional","Part of Fortune eighth or select dignified signs",
  "The original adds an eighth-house Part of Fortune and particular planetary-sign testimony to positive dowry indications.",
  "The original glyph sequence around Aquarius/Leo and houses of Jupiter/Venus needs careful source-native reading."),
 ("conditional","Jupiter or Venus trine or sextile Part Fortune",
  "Benefic trine or sextile to the Part of Fortune is used to affirm wealth.",
  "Do not substitute all favorable aspects regardless of source planet."),
 ("historical_inference","estate of quesited party sufficient",
  "Lilly infers an adequate estate for the person inquired about.",
  "No verified estate documents or prospective result."),
 ("conditional","dispositor Part Fortune casts sextile or trine to it",
  "The ruler of the Part of Fortune making trine or sextile to the point is a further favorable alternative.",
  "The source allows a dispositor alternative, not necessarily Jupiter and Venus simultaneously."),
 ("conditional","dispositor in good aspect Jupiter or Venus",
  "A favorable aspect between the fortune-dispositor and benefics is another supportive condition.",
  "Distinct from aspects made directly to the Part of Fortune."),
 ("historical_inference","Woman enquired after to be good Fortune",
  "The author describes the prospective wife as well provided for.",
  "A seventeenth-century property assessment claim, not an individual wealth prediction."))
group([447],"Peregrine malefics in eighth and payment disputes",
 ("conditional","Saturn or Mars Peregrine eighth",
  "Lilly cites Saturn or Mars peregrine in eighth as unfavorable.",
  "It is peregrine status together with eighth location, not just the planet's identity."),
 ("source_internal_forecast","poor or little promised obtained",
  "He conjectures that little of the promised portion might be received.",
  "No observed dowry transfer; negative predictive branch."),
 ("source_internal_forecast","extreame contention about it",
  "He also predicts serious disputes about payment.",
  "Payment and conflict are two different possible outcomes."))
group([447],"Combust eighth lord and south-node shortfall",
 ("conditional","Lord eighth Combust",
  "Combustion of eighth-house lord is a specified obstacle.",
  "Do not make combustion alone prove intentional dishonesty."),
 ("source_internal_forecast","slow performance; parents scarce able perform promises",
  "Lilly expects delayed payment or inability of parents to provide the promised portion.",
  "Ability to pay is distinct from fraud."),
 ("conditional","Cauda Draconis eighth, no Fortune therein",
  "South Node in eighth without beneficial occupancy is another source condition.",
  "Benefic absence explicitly qualifies the scenario."),
 ("historical_allegation","cheating intended, more promised than performed",
  "The author alleges possible cheating or overpromising under that configuration.",
  "Historical suspicion cannot justify accusing actual people of fraud."))
group([447],"Second/eighth house relationship: payment versus opposition",
 ("conditional","Lord eighth in second",
  "An eighth-house lord in the querent's second is linked to receiving the portion.",
  "This is a different house relationship from a direct aspect."),
 ("conditional","Lord eighth sextile or trine Lord second",
  "A favorable aspect between eighth and second lords is another affirmative sign.",
  "Original permits either aspect, not a blanket any-aspect rule."),
 ("source_internal_forecast","querent have what promised",
  "He expects delivery of the promised payment under the favorable versions.",
  "The historical text supplies no independently settled legal transaction."),
 ("conditional","square Lord second",
  "Square aspect is distinguished from sextile/trine.",
  "Square does not guarantee nonpayment; source describes difficulty."),
 ("source_internal_forecast","payment with difficulty",
  "The author predicts difficulty in obtaining it under a square.",
  "Difficulty and permanent nonpayment must not be conflated."),
 ("conditional","opposition Lord second",
  "Opposition supplies a more negative original alternative.",
  "Do not collapse into square."),
 ("source_internal_forecast","never without much wrangling",
  "The source suggests nonpayment or protracted dispute under opposition.",
  "Original clause ambiguous about the attachment of never versus wrangling."),
 ("exception","if no reception hardly at all",
  "Absence of reception is stated as making payment particularly unlikely.",
  "Must retain rather than scoring an opposition without considering reception."))
group([447],"Closing methodological caution",
 ("authorial_limit","impossible to give such generall Rules as always certain",
  "Lilly expressly says such general rules cannot always be certain.",
  "A material limit on deterministic transfer and claims of predictive reliability."),
 ("method","weigh querent Condition and possibility Figure",
  "He advises contextual evaluation of the querent's circumstances and the figure.",
  "This flexibility cannot be converted into a single deterministic scoring formula."))
group([448],"Next numbered LXIX heading boundary",
 ("navigation_boundary","CHAP. LXIX. If one be afraid of a thing",
  "The next numbered chapter asks whether a feared danger will occur.",
  "Heading on original PDF448/printed414; no Chapter LXIX body included."))
assert len({r["source_local_id"] for r in ROWS})==len(ROWS)
assert [r["source_local_id"] for r in ROWS]==[f"LXVIII-C{i:03}" for i in range(1,len(ROWS)+1)]
assert SPANS[0]["original_pdf_pages"]==[446] and SPANS[-1]["original_pdf_pages"]==[448]
assert ROWS[-1]["original_pdf_pages"]==[448]
assert all(r["chapter"]=="LXVIII" for r in ROWS[:-1])
assert ROWS[-1]["chapter"]=="LXIX_NAVIGATION_ONLY"
def dump(name,obj):
    (B/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
images=[]
for n in [446,447,448]:
    img=B/"evidence"/f"pdf_1647-{n}.jpg"
    data=img.read_bytes()
    images.append({"original_pdf_page":n,"printed_page":n-34,
      "path":img.relative_to(B).as_posix(),"bytes":len(data),
      "sha256":hashlib.sha256(data).hexdigest()})
SHA="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
dump("SOURCE_FIRST_CLAUSES_DRAFT.json",{
 "batch":"B03n","status":"ORIGINAL_SOURCE_FIRST_PROVISIONAL",
 "source_original_pdf_sha256":SHA,
 "source_units":len(ROWS),"rows":ROWS,
 "independent_payment_cases_authenticated":False})
dump("ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",{
 "batch":"B03n","status":"ORIGINAL_IMAGE_SOURCE_PASSAGE_MAP_PROVISIONAL",
 "source_spans":SPANS,"span_count":len(SPANS),
 "mapped_source_units":len(ROWS),
 "original_source_pages":[446,447,448],
 "independent_blind_diplomatic_transcription":False})
dump("SOURCE_WINDOW_MANIFEST.json",{
 "batch":"B03n","status":"SOURCE_FIRST_PROVISIONAL_NOT_CANONICAL",
 "source_original_pdf_sha256":SHA,
 "original_pdf_pages":[446,447,448],
 "opening":"PDF446 below Chapter LXVII divider",
 "closing":"PDF447 bottom before separate Chapter LXIX header on PDF448",
 "next_chapter":"LXIX","next_original_pdf_page":448,
 "prior_accepted_lilly":3932,"images":images,
 "independent_payment_outcomes_verified":False,
 "independent_blind_full_diplomatic_transcription":False})
dump("SOURCE_ORDER_DRAFT.json",{
 "batch":"B03n","status":"ORIGINAL_CHAPTER_SOURCE_ORDER_PROVISIONAL",
 "ordered_ids":[r["source_local_id"] for r in ROWS],
 "cross_page_ids":[r["source_local_id"] for r in ROWS if len(r["original_pdf_pages"])>1],
 "next_heading_only":ROWS[-1]["source_local_id"]})
issues=[
 ("PDF446","Dowry/wealth question starts below the LXVII divider; no lifespan/death content is part of LXVIII."),
 ("PDF446-447","Querent estate second versus partner portion eighth are separate derived-house referents."),
 ("PDF447","Source terms/glyphs Jupiter/Venus and Aquarius/Leo near Part Fortune need original visual confirmation before algorithmic use."),
 ("PDF447","Jupiter/Venus in eighth predict wealth only under essential dignity, direct motion and freedom from combustion."),
 ("PDF447","Retrograde/combust/slow motion can still allow a large amount, but with trouble; distinguish amount versus receipt ease."),
 ("PDF447","Eighth-lord inheritance testimony requires unimpeded condition and optional fourth/tenth beneficial corroboration."),
 ("PDF447","Source original angular/succedent/eleventh/eighth placement syntax has possible disjunctions, not all requirements simultaneously."),
 ("PDF447","Part of Fortune's zodiac glyphs, eighth location, beneficiary aspects and its dispositor are separate source testimony."),
 ("PDF447","Peregrine Saturn/Mars in eighth is a negative branch of reduced portion and/or contention."),
 ("PDF447","Combust eighth lord indicates delay/inability to fulfill, distinct from the South Node allegation of fraud."),
 ("PDF447","Alleged cheating or parental inability are historical suspicions, not factual proof about real people."),
 ("PDF447","Eighth lord in querent's second, trine/sextile second lord, square and opposition form separate receipt outcomes."),
 ("PDF447","Reception absence changes opposition result, and author explicitly denies universal certainty."),
 ("PDF448","Chapter LXIX fear and danger begins next printed page and must not be conflated with dowry question."),
 ("PDF446-448","No independent case outcomes, blind experimental forecasts, second diplomatic transcription or runtime model change.")
]
dump("UNRESOLVED_SOURCE_LIMITS.json",{
 "batch":"B03n","status":"HISTORICAL_SOURCE_LIMITS_OPEN",
 "issues":[{"id":f"B03n-U{i:02}","source":src,"issue":v} for i,(src,v) in enumerate(issues,1)]})
dump("CLAIM_LEDGER.json",{
 "batch":"B03n","kind":"HISTORICAL_WIFE_PORTION_AND_PAYMENT_ASSERTIONS_ONLY",
 "status":"PROVISIONAL_UNADMITTED",
 "source_first_units":len(ROWS),"source_visual_passages":len(SPANS),
 "prior_accepted_lilly":3932,"new_globally_accepted_source_units":0,
 "independently_authenticated_dowry_receipts":0,
 "independently_authenticated_dowry_disputes":0,
 "independently_verified_person_fraud_cases":0,
 "empirical_astrology_predictions_validated":0,
 "runtime_promotions":0})
print(json.dumps({"batch":"B03n","source_units":len(ROWS),
 "source_spans":len(SPANS),"unresolved":len(issues),
 "original_body_pdf_pages":[446,447],"next_heading_pdf":448,
 "new_accepted":0}))
