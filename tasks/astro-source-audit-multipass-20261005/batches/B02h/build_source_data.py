"""Build Lilly's third-house source inventory; no predictive model is deployed."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
SOURCE_ID = "LILLY1647_WELLCOME_B30338724"
SOURCE_SHA256 = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
RULES = []
GROUP = "third_house_scope"


def rec(title, pages, anchor, statement, requires=(), limits=(), kind="conditional_source_rule",
        section="XXIX", attribution="Lilly", temporal="Not specified locally", issues=()):
    number = 897 + len(RULES)
    RULES.append({
        "id": f"LI.1647.II.{section}.R{number}", "title": title, "kind": kind,
        "source_locator": {
            "source_id": SOURCE_ID, "source_sha256": SOURCE_SHA256, "book": "II",
            "section_key": f"II.{section}", "pdf_pages": list(pages),
            "printed_sequence_expected": [p - 34 for p in pages],
            "visible_printed_labels": [str(p - 34) for p in pages],
            "passage_anchor": anchor,
            "anchor_note": "Locating incipit/topic; long-s, spacing and glyph names normalized. Not a diplomatic quotation."
        },
        "genre": "horary", "statement_type": "editor_normalized_paraphrase",
        "source_attribution": attribution, "scope_group": GROUP,
        "source_statement": statement, "prerequisites": list(requires),
        "qualifications_and_limits": list(limits), "temporal_target": temporal,
        "unresolved_ids": list(issues),
        "runtime_status": "REFERENCE_ONLY_NOT_PROMOTED", "independent_evidence_unit": False
    })


rec("Third-house topics and scope", [221], "Of the third House, viz. Of Brethren, Sisters, Kinred, short Journeys",
    ["brothers, sisters and kindred", "unity and concord with them", "peace with neighbours", "their good or bad condition", "prosperity of a short journey"],
    kind="section_scope", section="THIRD_HOUSE_PREAMBLE",
    limits=["Begins below the divider on PDF221. The preceding wealth-example paragraph belongs to B02g."])

GROUP = "agreement"
rec("Agreement enquiry: the two parties", [222], "The Lord of the Ascendant is for him that asks",
    {"querent": "Ascendant lord", "brother_sister_neighbour_asked_about": "third lord"}, kind="query_frame")
rec("Alternative testimonies of concord", [222], "If a benevolent Planet be in the third",
    {"any_of": ["third lord is a benevolent planet", "third lord in Ascendant", "a fortunate planet in third", "third lord and Ascendant lord in sextile or trine within the orbs of either planet", "mutual reception of third lord and Ascendant lord", "third lord casts sextile or trine to Ascendant cusp", "Ascendant lord casts sextile or trine to third house"], "outcome": "unity and concord between the querent and the specified brother, sister, neighbour or kinsman"},
    limits=["Alternatives are not all-required. The explicit orb qualification belongs to the two-lord planetary aspect branch; no new numerical orb or global conflict-resolution rule is supplied."], issues=["B02h-U01"])
rec("Asymmetric contact and attribution of the defect", [222], "if a Fortune be in the Ascendant or the Lord of the Ascendant behold the cusp of the third",
    "A Fortune in Ascendant or Ascendant lord beholding third cusp, together with third lord not aspecting either Ascendant or its lord, attributes good condition/no default to querent and the defect to the other party.",
    limits=["The source's compound punctuation is not a formal Boolean expression; the natural conjunction with absent reciprocal contact is preserved. Behold is not narrowed to a favourable aspect. This is historical fault attribution, not an established fact about actual people."], issues=["B02h-U02"])
rec("Ascendant malefics and fault", [222], "Saturn, Mars or South Node in the Ascendant",
    "Saturn, Mars or South Node in Ascendant is assigned to fault or ill condition of the querent.",
    limits=["No essential-dignity exception is stated for this Ascendant clause. Historical characterization only."])
rec("Third-house adverse bodies and dignity exception", [222], "if they be in the third, unlesse in their own essentiall dignities",
    "Saturn, Mars or South Node in third gives little good from the other party unless in own essential dignities; worse if peregrine, retrograde, combust or in any malevolent configuration with another planet.",
    limits=["Worsening predicates are alternatives. The node's inclusion in the dignity-qualified phrase does not supply it an invented domicile or dignity table."], issues=["B02h-U03"])
rec("Adverse third-house context: present unity will not continue", [222], "although at present there be unity",
    "In the preceding adverse third-house configuration, Lilly says apparent present unity will not continue; hatred or grumbling usually follows.",
    requires=["The preceding adverse third-house context applies."], temporal="Present unity versus later continuation; no duration", limits=["Usually qualifies subsequent hatred/grumbling. No interval or claim outside this adverse source context is supplied."])
rec("Saturn or South Node character attribution", [222], "Saturn or South Node in the third",
    "Saturn or South Node in third characterizes neighbours as clowns and kin as covetous or sparing, most assuredly out of essential dignities.",
    limits=["Historical moral attribution, not an observed personal trait. Source dignity language is retained without inventing node dignities."], issues=["B02h-U03"])
rec("Mars character attribution", [222], "Mars, then your Kindred are treacherous",
    "Mars in third characterizes kin as treacherous and neighbours as thievish, most assuredly when out of essential dignities.",
    limits=["Historical moral attribution, not an observed personal trait."])

GROUP = "absent_relative"
rec("Absent brother: house frame", [223], "Of a Brother that is absent",
    {"querent": ["question Ascendant", "its lord"], "absent_brother_ascendant": 3, "absent_brother_substance": 4, "continuation": "proceed in order through the other houses"},
    kind="query_frame", limits=["The following house numbers are preserved as the source writes them. Read with the explicit original-figure sixth/eighth/twelfth qualification on PDF226 and the dual-eighth worked example on PDF231."], issues=["B02h-U04"])
rec("Inspect the brother's significator and contacts", [223], "consider the Lord of the third, in what condition he is",
    ["condition of third lord", "house occupied", "aspect from good or evil planets", "which aspect", "whether a corporal conjunction"], kind="reference_inputs")
rec("Third lord in third without malefic square or opposition", [223], "If the Lord of the third be in the third",
    "Third lord in third with no square or opposition from unfortunate planets signifies the brother in health.",
    limits=["The glyph after square is opposition in the original; not conjunction."])
rec("Third-house malefic contact without reception: distress while healthy", [223], "malignant Planets have a square or opposition unto him, without reception",
    "Malignant planets square or opposite the significator without reception signify that he lives and is in health, but in great perplexity, discontent and sorrow.",
    requires=["Retain the opening third-house placement/aspect-reading context before the text moves to fourth."],
    limits=["Distress is not silently recoded as illness. No direction or mutuality of reception is supplied."], issues=["B02h-U05"])
rec("Third-house malefic contact with reception: escape from distress", [223], "if the same Infortunes have reception with him",
    "The same malignant square/opposition with reception signifies great distress which he will evade with ease, freeing himself from the present sad condition.",
    requires=["Opening third-house context and the preceding malignant-contact branch."], temporal="Present distress and subsequent escape; no duration",
    limits=["Reception does not erase the distress premise. Direction and mutuality unspecified."], issues=["B02h-U05"])
rec("Benefic alternatives for health and contentment", [223], "fortunate Planets be in sextile or trine with him, without reception",
    "Fortunate planets sextile/trine the significator without reception, OR square/opposite him with reception, signify health and contentment to remain where he is.",
    requires=["Opening third-house placement/aspect context."], limits=["The aspect/reception pairings are not interchangeable; not a generic any-benefic-contact rule."], issues=["B02h-U05"])
rec("Benefic soft aspect with reception: stronger well-being claim", [223], "sextile or trine with him, and with reception",
    "Fortunate planets sextile/trine the significator with reception signify health and lack of nothing needed for happiness.",
    requires=["Opening third-house context."], limits=["Stronger historical claim than mere contentment; no measured probability."], issues=["B02h-U05"])
rec("Fourth placement and effort to obtain substance", [223], "If the Lord of the third be in the fourth",
    "Third lord in fourth, explicitly the brother's own second, without aspect of malignant planets signifies endeavour to obtain estate or fortune in the country where he is when the figure is erected.",
    limits=["Endeavour is not completed acquisition. Without aspect is not narrowed to square/opposition."], temporal="Current activity at question time")
rec("Fifth placement with its lord", [223], "If he be in the fifth, and joyned with the Lord of the fifth",
    "Third lord in fifth, joined with fifth lord, 'with reception of a Fortune or not', provided fifth lord is not grievously impedited, signifies health, merriment and pleasure in the local company.",
    limits=["The unusual reception-of-a-Fortune wording is retained. It does not unambiguously identify fifth lord as a Fortune or require reception."], issues=["B02h-U06"])
rec("Fifth-placement benefic mitigation and confidence", [223,224], "if the Lord of the fifth be a Fortune",
    "In the local fifth-house discussion, a Fortune as the body with which the significator is conjunct, or a sextile/trine with reception, permits the favourable condition to be said more safely.",
    requires=["Fifth-placement context and the preceding qualification on the fifth lord."],
    limits=["The punctuation does not settle whether reception qualifies the conjunction as well as the sextile/trine alternative. No mutuality or confidence scale is invented."], issues=["B02h-U06"])
rec("Fifth-placement void course or impedited malefic conjunction", [224], "if the Lord of the third be in the fifth, voyd of course",
    "Third lord in fifth void of course, OR in perfect conjunction with an unfortunate planet without reception and that planet itself impedited, argues indisposition in health, 'crazy', and discontent with the place.",
    limits=["Keep the fifth-house context and the two alternatives. Crazy is an archaic source word, not an established modern psychiatric diagnosis."])
rec("Obscured qualification of naturally ill houses", [224], "other houses which are [cancelled word] naturally ill",
    "A following statement places the significator in other houses 'which are [obscured/cancelled word] naturally ill (as the sixth, eighth and twelfth houses are)' and says he is not well pleased, yet no hurt will come of it.",
    kind="textually_unresolved_rule", limits=["The inked word could materially change the condition. Neither restoring 'not' nor deleting it is admitted as a clean source condition."], issues=["B02h-U07"])
rec("Eighth placement with a Fortune: qualified indisposition", [224], "If the Significator be in the eighth, and corporally joyned to a Fortune",
    "Significator in eighth, corporally joined or joined by sextile/trine to a Fortune, is not very well but not so ill as to doubt well-being; still indisposed.",
    limits=["Reception is not stated as a requirement in this clause. Retain eighth placement for each contact alternative."])
rec("Affliction out of the sixth", [224], "joyned to evill Planets by bad aspects, and out of the sixt house",
    "Joining evil planets by bad aspects 'and out of the sixth house' signifies infirmity.",
    limits=["Out of is not translated as outside the sixth. Its attachment to the afflicting body or aspect origin remains unresolved; no geometry is silently supplied."], issues=["B02h-U08"])
rec("Sixth lord in third: dignity exception", [224], "if the Lord of the sixth be in the third",
    "Sixth lord in third gives the same infirmity judgement unless that lord has dignities in the sign and is in those dignities.",
    limits=["The exception requires possession and occupation of the relevant dignities. Radical/turned source context remains explicit."], issues=["B02h-U04"])
rec("Mortality claim requires an already ill brother", [224], "if you find the Brother is ill",
    "If the brother has already been found ill, third lord conjunct eighth lord OR entering combustion makes it likely, in Lilly's judgement, that he will die of that infirmity.",
    requires=["Prior illness judgement; do not infer illness from this conditional alone."], temporal="Likely future death from the specified existing illness; no date",
    limits=["Historical source claim, not an actual-person medical judgement; likely is not certainty."], issues=["B02h-U04"])
rec("Seventh placement: continued sojourn", [224], "If the Significator be in the seventh",
    "Significator in seventh signifies remaining in the country to which he went, a stranger/sojourner, neither well nor ill.",
    limits=["A cancelled short word before went is not reconstructed; it supplies no extra destination or date."], temporal="Current location and condition")
rec("Eighth placement: fear of death", [224], "If he be in the eighth, he feares he shall dye",
    "Significator in eighth signifies his fear that he will die; greater fear if combust, OR conjunct eighth lord in eighth, OR square/opposite the Infortunes 'out of the eighth'.",
    limits=["Fear is the outcome here, not death. Preserve the eighth context and old aspect-origin phrase."], issues=["B02h-U04","B02h-U08"])
rec("Ninth placement: alternative places and employments", [224], "If he be in the ninth",
    "Significator in ninth signifies a further country; OR, if capable, entry into a religious order; OR employment by religious men; OR possibly a journey far from the former abode according to his quality.",
    limits=["Alternatives and personal capacity/status qualifiers remain; no single automatic occupation or location."])
rec("Tenth placement with Fortunes", [224,225], "If he be in the tenth, and joyned with Fortunes",
    "Significator in tenth conjunct or sextile/trine Fortunes, especially with reception, signifies office, employment or command, good estimation and credible living in that country.",
    limits=["Reception strengthens rather than exclusively gates the stated good contact alternatives."])
rec("Adverse tenth placement: feared death", [225], "joyned to Infortunes, or in square or opposition",
    "In tenth, joining Infortunes, square/opposing them, being otherwise impedited by them, OR combustion leads Lilly to say it may be feared he is dead.",
    requires=["Tenth-placement context."], temporal="Tentative concern that death has already occurred",
    limits=["Do not equate may be feared with a confirmed death, the absent person's own fear, or the preceding likely future death conditional."])
rec("Eleventh placement: friends and safety", [225], "If he be in the eleventh house",
    "Significator in eleventh joined to Fortunes by a good aspect, OR conjunct eleventh lord, signifies safety at a friend's house, pleasant and merry.",
    limits=["Eleventh placement applies to the surrounding alternatives."])
rec("Afflicted eleventh placement", [225], "if evill Planets afflict him in that house",
    "Bad planets afflicting the significator in eleventh or casting malevolent beams to him signify discontent with his present condition.")
rec("Twelfth placement with received unimpeded Fortunes", [225], "joyned to Fortunes with reception, and those Fortunes not impedited",
    "Significator in twelfth joined to Fortunes with reception, those Fortunes unimpeded, signifies dealings with horses or great cattle: grazier, master of horse, hostler, drover and similar alternatives according to his quality.",
    limits=["Reception, unimpeded Fortunes, placement and personal-quality qualifications are all retained; not every occupation simultaneously."])
rec("Adverse twelfth placement: discontent, fear and probable death there", [225], "unfortunate in the twelfth, or in bad aspect with the infortunes",
    "In the twelfth-house paragraph, being unfortunate, in bad aspect with Infortunes, in aspect with eighth lord, OR combust signifies discontent, fear of never seeing home again, and a probable death there.",
    requires=["Twelfth-house paragraph context; not an any-house combustion rule."],
    limits=["Eighth-lord aspect is not narrowed to bad aspect. Fear, discontent and author's qualified death claim remain separate endpoints."], issues=["B02h-U04"])
rec("First placement: pleasure and respect", [225], "If he be in the first",
    "Significator in first signifies pleasure where he is and being loved and respected there.")
rec("Second placement: probable impediment to leaving", [225], "If he be in the second",
    "Significator in second signifies probable inability to come away: imprisonment or an act preventing departure.",
    limits=["Alternative causes; probable is not certain imprisonment."])
rec("Retrograde second-placement significator: effort to escape", [225], "if he be Retrograde",
    "With the preceding impediment to leaving, retrogradation signifies strenuous effort to escape when opportunity appears.",
    requires=["Second-placement impediment context."], limits=["Effort and opportunity do not guarantee successful escape."])
rec("Absent father and extension round the houses", [225,226], "the fourth house is the Ascendant of that party",
    "For an absent father, use fourth as his Ascendant and proceed round twelve houses. The paragraph calls the second house from 'the Ascendant of your Question' the quesited's substance, the third from that his brethren and the fourth his father.",
    kind="query_frame_extension", limits=["The quoted reference phrase is awkward beside the explicit derived Ascendant. Preserve it; the later child/servant examples make inclusive turning explicit without erasing the wording ambiguity."], issues=["B02h-U09"])
rec("Absent child frame", [226], "if one aske of his childe, son or daughter",
    {"child_ascendant": 5, "child_second": 6, "child_third": 7, "continuation": "so proceed in order"}, kind="query_frame_extension")
rec("Absent servant frame", [226], "If one aske of a Servant",
    {"servant_ascendant": 6, "servant_substance": 7, "continuation": "so proceed in order"}, kind="query_frame_extension")
rec("Original figure sixth, eighth and twelfth retained", [226], "yet in every one quesited after, the sixt House of the figure",
    "Although every house has its own sixth, eighth and twelfth, Lilly explicitly retains sixth of the figure for the absent person's infirmity, eighth for death and twelfth for imprisonment.",
    kind="reference_frame_qualification", limits=["This statement coexists with the turning instructions and the worked dual-eighth check on PDF231. It neither deletes derived houses nor supplies a universal numerical precedence rule."], issues=["B02h-U04"])
rec("Variation is required but not formalized", [226], "you must know how to vary your Rules",
    "Lilly calls varying the rules the masterpiece of the art and expects a judicious practitioner to do so.",
    kind="method_qualification", limits=["No new discretion score, tie-breaker, or retrospective permission to choose whichever interpretation fits is implemented."], issues=["B02h-U01"])

GROUP = "reports_lilly_wartime"
rec("Alternative ancient frames for intelligence", [226], "The Ancients placed these judgments variously",
    "Some Ancients use fifth; others use triplicity lords of signs ascending/descending on third or fifth cusps for reports, news, intelligence and fears.",
    kind="attributed_method_plurality", attribution="Ancients as reported by Lilly",
    limits=["The text reports alternatives rather than choosing a single fully specified algorithm."], issues=["B02h-U10"])
rec("Lilly's wartime report truth and parliamentary benefit", [226], "I have ever found by experience",
    "Moon in first, tenth, eleventh or third, separated by a benevolent aspect from any planet regardless of its house lordship, then applying by sextile, trine or conjunction to Ascendant lord, is reported by Lilly as true news which always tended to Parliament's good, whether the report sounded good or ill.",
    kind="author_experience_claim", attribution="Lilly's declared late Civil War experience",
    limits=["Placement, separation, application and recipient are conjunctive conditions; three application types are visible in the original. Truth, tone and beneficiary are distinct. The historical partisan claim is not a generic prediction of querent victory."])
rec("Lilly's wartime enemy-benefit alternative", [226], "if the Moon applyed to the Lord of the seventh",
    "Moon applying to seventh lord by any good aspect at figure erection made Lilly judge his side had the worst and the enemies the victory.",
    kind="author_experience_claim", attribution="Lilly's partisan wartime judgement",
    limits=["Does not by itself state that the report is false; political benefit and report truth are different targets."])
rec("Void-of-course Moon and inconsequential reports", [226], "Moon was voyd of course",
    "Lilly reports that with void-of-course Moon the news proved of no moment, usually vain or mere lies and soon contradicted.",
    kind="author_experience_claim", limits=["Usually is retained. Inconsequence and falsity are not equivalent outcomes."], temporal="Near-term contradiction claimed; no fixed interval")
rec("Moon-Mercury hard aspect plus absent favourable Ascendant contact", [226], "Moon and Mercury in square or opposition",
    "Moon and Mercury square/opposite, with neither Moon nor Mercury casting a favourable sextile/trine to the Ascendant degree, is interpreted as false news deliberately reported to frighten Lilly's side.",
    limits=["Meaning: neither body supplies such a favourable contact; it is not merely that both fail to do so jointly. The degree target and missing-favourable-contact condition are necessary."])
rec("News question time depends on who asks", [227], "the houre when I first heard the newes",
    {"self_heard_news": "moment of first hearing the news or rumour", "another_person_proposes_question": "exact moment the question is proposed"},
    kind="question_time_convention", limits=["Historical procedural convention, not a modern message-delivery or automated-interview rule."])
rec("Whether news harms the asker: favourable alternatives", [227], "see whether Jupiter or Venus be in the Ascendant",
    "Jupiter or Venus in Ascendant, OR Moon or Mercury in their essential dignities with trine/sextile to eleventh lord, signifies no detriment to the person enquiring.",
    requires=["The enquiry is whether the report will be prejudicial to the asker."],
    limits=["Original first pair is Jupiter/Venus, not Moon/Mercury. Dignity-plus-aspect belongs to the Moon/Mercury branch; no-detriment is not necessarily report falsity."])
rec("Harm from news: relevance and planetary conditions", [227], "Lord of the sixth, eighth or twelfth houses in the Ascendant",
    "Sixth, eighth or twelfth lord in Ascendant or in bad aspect to Ascendant lord; OR Mars/Saturn retrograde in Ascendant, in evil aspect to Ascendant lord, or casting square/opposition to Ascendant degree, signifies harm to querent if the matter concerns that person, or damage to ministers/parties if it concerns the Commonwealth.",
    limits=["Relevance and target are required. The reach of retrograde into the later Mars/Saturn alternatives is less than formally explicit; preserve its printed position."], issues=["B02h-U11"])
rec("Wartime damage examples by actual significator", [227], "if Saturn signifie the mischiefe",
    {"Saturn": "country friends plundered; corn and cattle lost", "Mars": "straggling parties cut off", "Mercury": "letters miscarried or intercepted", "Sun": "chief officer or commander in distress", "Jupiter_or_Venus": "harm to gentlemen, friends or supporters"},
    kind="conditional_reference_table", requires=["The harm/Commonwealth context applies and the named planet actually signifies the mischief."],
    limits=["Not a claim about every occurrence of these planets; Lilly explicitly says to vary by the question."])

GROUP = "rumours_ancients"
rec("Ancients' angularity, fixity and favourable-contact alternatives", [227,228], "Consider the Lord of the Ascendant and the Moon",
    "Consider Ascendant lord and Moon and which is angular; OR Moon's dispositor angular and fixed; OR any of these succedent and fixed; OR in sextile/trine to Jupiter, Venus or Sun: the rumours are judged true and very good.",
    attribution="Ancients as reported by Lilly", limits=["The reach of fixed sign across the opening angular alternatives is not formally unambiguous. Sun is explicitly in the favourable list."], issues=["B02h-U12"])
rec("Afflicted or cadent first lord overrides sign strength here", [227,228], "if you find the Lord of the Ascendant afflicted",
    "Ascendant lord afflicted by Infortunes OR cadent gives the contrary judgement, though strong in its sign.",
    attribution="Ancients as reported by Lilly", limits=["Do not erase the contrary clause by selecting sign strength alone."])
rec("Fixed angles and applying Moon/Mercury", [228], "Rumours are for the most part true",
    "Rumours are for the most part true with fixed angles (Taurus, Leo, Scorpio, Aquarius), Moon and Mercury in fixed signs separating from Infortunes and applying to a fortunate planet in an angle.",
    attribution="Ancients as reported by Lilly", limits=["All configuration components, including the angular recipient and movement sequence, are retained; for the most part is not certainty."])
rec("Ill report partly verified with fixed fourth/tenth", [228], "Ill Rumours hold true",
    "Ill rumours with fourth and tenth angles fixed and Moon 'received in them' will in some sort be verified.",
    attribution="Ancients as reported by Lilly", limits=["In some sort does not certify every detail. Received in them is not a fully defined mutual-reception or placement formula."], issues=["B02h-U13"])
rec("Ill news turns good: Fortune branch and uncertain Moon word", [228], "if either of the Fortunes be in the Ascendant, or the Moon ufortunate",
    "For evil news or unlucky intelligence, either Fortune in Ascendant OR Moon described by the visibly printed 'ufortunate' is called strong evidence that rumours are false and will turn to good.",
    attribution="Ancients as reported by Lilly", kind="partly_textually_unresolved_rule",
    limits=["The Fortune-in-Ascendant alternative is legible. The Moon word is not silently normalized to fortunate or unfortunate; the uncertain alternative is not executable."], issues=["B02h-U14"])
rec("Retrogradation or affliction in ill-rumour judgement", [228], "The Retrogradation of Mercury, or he any other way afflicted",
    "The passage names Mercury's retrogradation or other affliction, or that of the planet Moon applies to, or Mercury applies to; especially 'if either of those two' rules Ascendant, ill rumours vanish and convert to good.",
    attribution="Ancients as reported by Lilly", limits=["Shared affliction/retrogradation scope and 'those two' antecedent are not uniquely formalized. Topic remains ill rumours."], issues=["B02h-U15"])
rec("Combust first lord: truth kept secret", [228], "Lord of the Ascendant be under the Sun Beames or Combust",
    "Ascendant lord under Sun's beams or combust signifies secrecy: few will ever know the truth of the matter.",
    attribution="Ancients as reported by Lilly", limits=["An epistemic/secrecy claim, not a verdict of true or false."])

GROUP = "advice_intention"
rec("Advice visit: frame and timing", [228], "when first they begin to break their minds unto you",
    "For a neighbour, kinsman or friend visiting to advise or persuade, erect the figure when they first begin disclosing the matter.",
    kind="question_time_convention", limits=["Target is intention in giving advice, not demonstrated usefulness, accuracy or safety of the advice."])
rec("Favourable advice-intention alternatives include north node", [228], "a fortunate Planet, viz. Sun or Jupiter or Venus, or else North Node",
    "Sun, Jupiter or Venus in Midheaven/tenth, OR North Node there, OR Moon applying to Ascendant lord, signifies honest intent and advice intended for the recipient's good.",
    limits=["Moon's application is a separate alternative, with no specified aspect or reception here. Node is retained and is not a planet; intention is distinct from benefit actually delivered."])
rec("Adverse advice-intention bodies include south node", [228], "If an Infortune, viz. Saturn or Mars or South Node",
    "Saturn, Mars or South Node in the corresponding Midheaven/tenth context signifies deceitful intent and lying.",
    limits=["Placement context and node identity are required. Historical source characterization, not a present person's verified intent."])
rec("Haly's three movable-sign conditions", [228], "Haly doth further affirm",
    "Haly is said to affirm that a movable Ascendant sign, Ascendant lord in a movable sign, and Moon in a movable sign signify a deceitful visitor seeking to entrap.",
    attribution="Haly as reported by Lilly", limits=["All three conditions retained; distinct attribution and no modern personal inference."])

GROUP = "siblings"
rec("Sibling enquiry: natal preference and horary caveat", [229], "better resolved from the proper Nativity",
    "Lilly prefers the querent's proper nativity for whether siblings exist, but supplies horary rules claimed true in his experience.",
    kind="genre_and_evidence_qualification", limits=["A claimed observation, not independent validation or conversion of these local rules into a natal module."])
rec("Local fruitful-sign list for third cusp", [229], "a fruitfull Sign, as Cancer Scorpio Pisces",
    {"third_cusp_more_fruitful": ["Cancer","Scorpio","Pisces"], "third_cusp_less_fruitful_but_included": ["Aquarius","Sagittarius","Gemini"], "outcome": "may judge brethren or sisters"},
    kind="conditional_reference_table", limits=["Read from the original glyphs, not replaced with a presumed standard list. Degrees of fruitfulness are source categories, not measured fertility."])
rec("Brother indicators use sign or house, not hour", [229], "a Masculine Signe or house",
    "A masculine sign on third cusp, with its lord in a masculine sign or house, or aspecting a masculine planet, is used to judge a brother or brothers.",
    limits=["Original reads house; no planetary-hour rule. Exact conjunction/alternative punctuation is preserved as prose; local masculine-house classification is not fully specified."], issues=["B02h-U16"])
rec("Sister indicators and configuration alternatives", [229], "Sister or Sisters",
    "A feminine sign and planet in third; OR significators in feminine signs or houses and conjunct/applying to feminine planets, are used to judge a sister or sisters.",
    limits=["Preserve the alternatives, source plurals and feminine-planet qualification. No aspect type is supplied for application."], issues=["B02h-U16"])
rec("Sibling-count doctrine attributed and rejected", [229], "some say, so many Planets as are in the house",
    "Some count planets in the house or planets aspected by third lord as the number of siblings. Lilly regards demanding such particulars from a question as too scrupulous.",
    kind="attributed_rejected_method", attribution="Unnamed others; explicitly rejected by Lilly",
    limits=["Not an endorsed Lilly count algorithm; do not add it to a prediction engine."])
rec("Last aspect and unity", [229], "the last aspect the Lord of the third, and Lord of the Ascendant were in",
    "Present or future unity is judged from the last aspect of third lord and Ascendant lord, or the posture of benevolent or malignant planets in Ascendant or third.",
    limits=["Last aspect is not silently replaced with next application. No timing scale supplied."], temporal="Present or future unity, unspecified interval")
rec("Which party supplies concord", [229], "where the Fortunes are placed",
    {"Fortunes_in_Ascendant": "concord expected from querent", "Fortunes_in_third": "concord from brother, sister or kindred"}, kind="conditional_reference_table")
rec("Discord in third with separate node alternative", [229], "Saturn or Mars out of their essentiall Dignities in the third, or South Node therein",
    "Saturn or Mars out of essential dignities in third, OR South Node there, is a strong argument of untoward relatives, no unity, and continual discord and wrangling.",
    limits=["Unlike the earlier compound dignity phrase, the South Node is a separate alternative here. Historical characterization, not actual observation."])

GROUP = "short_journey"
rec("Short-journey practical scope", [229], "twenty, thirty or forty miles",
    "A short journey means twenty, thirty or forty miles, or a distance one may go and return in a day or at latest the next.",
    kind="query_scope", limits=["Examples of distance and duration, not an exact universal 20–40-mile interval or a requirement that both be satisfied."])
rec("First-lord speed is inspected", [229,230], "see if he be swift or slow in motion",
    "Consider Ascendant lord at question proposal and inspect whether swift or slow; the text then proceeds into favourable alternatives.",
    kind="reference_input_with_ambiguous_transition", limits=["The printed transition does not establish that either speed is itself favourable; do not delete slow from a supposed transcription or turn the inspection instruction into a clean verdict."], issues=["B02h-U17"])
rec("Alternative favourable short-journey configurations", [230], "all, or any of these are arguments",
    {"any_of": ["Ascendant lord in any dignities of third lord", "Ascendant lord in third", "Ascendant lord sextile/trine/conjunct third lord", "Ascendant lord sextile/trine/conjunct a benevolent planet in third", "Moon applies to third lord", "Moon applies to any planet in third", "Moon in third", "Moon sextiles the ascending sign", "Moon square in signs of short ascensions, in any house whatsoever", "Moon swift in motion"], "outcome": "party will go on the short journey, with good success"},
    limits=["Dignity direction is first lord in third lord's dignities. The Moon's third-house recipient need not be benevolent. All or any is explicit. Square target is not restated after the Ascendant sextile branch and hemisphere convention is not given."], issues=["B02h-U18"])
rec("Direction selectors and missing ranking procedure", [230], "consider the Signe of the third house",
    "Consider third-cusp sign, third lord's sign and Moon's sign; judge by which is strongest in essential dignities where it is.",
    kind="selection_instruction", limits=["The candidates mix a cusp sign and planetary placements. A complete strength ranking, tie rule or compass lookup is not supplied here."], issues=["B02h-U19"])
rec("Principal significator's directional sign", [230], "if the principall Significator be in a Northerne Signe",
    "Principal significator in a northern sign signifies intended travel north; analogize the other directions with their due limitations.",
    requires=["Principal significator selected under preceding instruction."], limits=["No new complete sign-compass or hemisphere rule. Ends above the PDF230 divider; the chart below belongs to XXX."], issues=["B02h-U19"])


def save(name, obj):
    (ROOT / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    general_count = len(RULES)
    candidate = ROOT / "EXAMPLE_RULES_RECONCILED.json"
    if candidate.exists():
        for item in json.loads(candidate.read_text())["rules"]:
            item = dict(item)
            number = 897 + len(RULES)
            item["id"] = f"LI.1647.II.{item['source_locator']['section_key'].removeprefix('II.')}.R{number}"
            RULES.append(item)
    data = {
        "schema_version": 1, "batch": "B02h", "source_id": SOURCE_ID,
        "source_sha256": SOURCE_SHA256, "status": "SOURCE_ONLY_NOT_RUNTIME_OR_VALIDATION",
        "scope": "Third-house preamble below PDF221 divider through PDF235; XXIX–XXXI including unnumbered sections and example preambles.",
        "general_records_count": general_count, "records_count": len(RULES), "rules": RULES
    }
    save("RULES.json", data)
    print(json.dumps({"records_count": len(RULES), "general_records_count": general_count, "first": RULES[0]["id"], "last": RULES[-1]["id"]}))
