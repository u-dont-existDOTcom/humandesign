"""Build the source-only Lilly second-house inventory; not a prediction model."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
SOURCE_ID = "LILLY1647_WELLCOME_B30338724"
SOURCE_SHA256 = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
# These four printed folios are not the sequential p-34 values. Prose continues.
PRINTED_LABELS = {204: "174", 205: "175", 208: "170", 209: "171"}
RULES = []


def rec(title, pages, anchor, statement, requires=(), limits=(), kind="conditional_source_rule", section="XXVII"):
    number = 775 + len(RULES)
    RULES.append({
        "id": f"LI.1647.II.{section}.R{number}", "title": title, "kind": kind,
        "source_locator": {
            "source_id": SOURCE_ID, "source_sha256": SOURCE_SHA256,
            "book": "II", "section_key": f"II.{section}", "pdf_pages": list(pages),
            "printed_sequence_expected": [p - 34 for p in pages],
            "visible_printed_labels": [PRINTED_LABELS.get(p, str(p - 34)) for p in pages],
            "passage_anchor": anchor,
            "anchor_note": "Locating incipit/topic; long-s, spacing and glyph names normalized. Not a diplomatic quotation."
        },
        "genre": "horary", "statement_type": "editor_normalized_paraphrase",
        "source_statement": statement, "prerequisites": list(requires),
        "qualifications_and_limits": list(limits),
        "runtime_status": "REFERENCE_ONLY_NOT_PROMOTED", "independent_evidence_unit": False
    })


rec("General wealth question: scope and querent", [201], "Whoever interrogates; if the Question be in generall termes",
    "Ascendant, its lord and Moon signify the asker regardless of rank. The opening method concerns whether the asker will ever be rich, without reference to a particular person from whom a fortune is expected.",
    limits=["A horary question, not a natal wealth rule or a claim about an actual person's finances."], kind="query_frame")
rec("Wealth significators and their configurations", [201], "Consider the Signe ascending on the Cusp of the second House",
    ["second-cusp sign", "second lord", "second-house occupants", "planets aspecting second lord or cusp", "Fortune's sign and house", "planetary aspects received by Fortune"],
    limits=["Inventory is not a numerical weighting or precedence algorithm."], kind="reference_inputs")
rec("Fortune and the nodes do not emit rays", [201], "for Fortune it selfe emitteth no rayes",
    "Fortune itself casts no aspect to a planet; neither do the north and south nodes.",
    limits=["Receiving a planetary aspect is distinct from emitting one. Do not symmetrize these semantic roles merely because longitude geometry is symmetric."], kind="definition")
rec("All planets angular: general wealth testimony", [201], "if you find the Planets all angular",
    "All planets angular are one good sign of substance.", limits=["The author calls the opening rules general. This is one testimony, not an unconditional calibrated verdict."])
rec("Succedent direct swift planets", [201], "if they be in succedant houses, direct and swift",
    "Planets in succedent houses, direct and swift, are a favourable general testimony.")
rec("Good houses and moderate essential dignity", [201, 202], "If the Planets be in good houses",
    "Planets in good houses, direct and moderately essentially dignified, give hope of an estate.",
    limits=["No local exhaustive definition of good houses or numerical minimum for moderate dignity."])
rec("Union of querent and wealth significators", [202], "If the Lord of the Ascendant, or the Moon, and Lord of the second",
    "The opening favourable alternatives include bodily joining of the Ascendant lord or Moon with the second lord.",
    limits=["The printed coordination is not a formal Boolean expression. Preserve uncertainty over its exact grouping; do not require or exclude a three-body conjunction silently."])
rec("Friendly aspect to the second lord", [202], "or if they, viz. Lord of the Ascendant and Moon",
    "Friendly aspect from the Ascendant lord and Moon to the second lord is another favourable alternative.",
    limits=["The source names both in this clause; do not silently replace and by or. Friendly is not given a new orb here."])
rec("Jupiter or Venus contacting Fortune", [202], "or if Jupiter and Venus cast their trine or sextile",
    "Jupiter and Venus casting trine or sextile to Fortune, or being conjunct it, supply favourable testimony.",
    limits=["The enumerative wording does not settle whether both benefics must act in every application."])
rec("Wealth lord in the first", [202], "or if the Lord of the second be in the Ascendant",
    "The second lord in the Ascendant is a favourable wealth testimony.")
rec("Querent significator in the second", [202], "or the Moon, or Lord of the Ascendant in the second",
    "Moon or Ascendant lord in the second is favourable wealth testimony.")
rec("Translation from wealth lord to querent lord", [202], "if any Planet transfer the light and vertue",
    "A planet translating the second lord's light and virtue to the Ascendant lord supplies favourable wealth testimony.",
    limits=["Direction is retained. The local clause does not restate every prior translation prerequisite."])
rec("Benefic rays to Ascendant cusp or Fortune", [202], "benevolent Planets cast their sextile or trine",
    "Benevolent planets casting sextile or trine to the Ascendant cusp or Fortune are favourable.")
rec("Jupiter-Venus nature fixed stars", [202], "any fixed Starre of the nature of Jupiter and Venus",
    "A fixed star of Jupiter/Venus nature ascending with the second cusp, or Fortune conjunct or near such a star, is favourable.",
    limits=["No list of stars or numerical near/rising threshold is supplied locally."])
rec("Second-house natural benefics and north node", [202], "Jupiter who is naturall significator of substance",
    "Jupiter, naturally signifying substance, Venus, naturally a fortune, or the north node in the second is favourable when no infortune aspects them.",
    limits=["The no-infortune qualification belongs to the clause; node is not misread as a planet."])
rec("Direct swift motion defined against mean", [202], "their daily motion be more then what is assigned",
    "All planets direct and swift are favourable; swift means daily motion greater than the assigned mean motion.",
    limits=["Strictly greater, not greater-or-equal. Printed references are pages57,61,65,69,72,76,80. Retain source means instead of silently using a modern ephemeris average."], kind="definition_and_testimony")
rec("Judgement magnitude and social capacity", [202], "competently rich or have a sufficient fortune to subsist on",
    "The favourable testimonies indicate competent wealth or sufficient subsistence, with greater or lesser estate according to the major relevant testimonies and the capacity/condition of the person asking.",
    limits=["No fixed currency threshold, probability, uniform definition of rich, or numerical majority/weighting formula is supplied."], kind="synthesis_qualification")
rec("Means-of-wealth enquiry is conditional", [202], "When you have sufficiently examined your Figure",
    "Only after judging that subsistence or riches are promised does the discussion ask how, by whom and by what means they are obtained.",
    limits=["A listed house association is not itself proof that wealth is promised."], kind="applicability_gate")
rec("Second lord's placement: labour or unexpected acquisition", [202, 203], "if the Lord of the second house be in the second",
    {"second_lord_in_second": "own labour and industry", "second_lord_in_first": "unexpected fortune or attainment without much labour"},
    requires=["Prior wealth/subsistence judgement."], kind="conditional_reference_table")
rec("Trace the helping aspect before choosing a means", [203], "If that the Lord of the second or the Moon doe promise substance",
    "When second lord or Moon promises substance through their mutual aspect, inspect the house from which the aspect comes or the house ruled by the Moon. If neither promises substance, inspect Fortune's house and its dispositor's house lordship.",
    limits=["These are conditional alternatives, not an instruction to collect every possible house narrative."], kind="source_selection_order")
rec("Helpful first lord: own work", [203], "If the Planet assisting or promising encrease of Fortune be Lord of the Ascendant",
    "A helping Ascendant lord signifies the asker's diligence advancing the estate; for an ordinary artisan, labour, invention, care and pains-taking.", requires=["The planet actually assists or promises increase."])
rec("Helpful second lord: existing capital and commerce", [203], "if the Adjuvant Planet be Lord of the second",
    "A helping second lord signifies increasing and managing one's own stock; buying and selling things to which the person is naturally inclined, which arise in the course of life, or which suit the planet's nature, with its sign considered.", requires=["The planet actually assists or promises increase."])
rec("Helpful third lord: kin, neighbours and journeys", [203], "If the Lord of the third fortunate the Lord of the second",
    "Third lord helping second lord, second cusp or Fortune indicates aid through an honest neighbour, kin, siblings if present, a journey, or removal toward the quarter from which the helpful aspect or conjunction comes.",
    limits=["Siblings are explicitly conditional on having them; the alternatives are not separate independent predictions."])
rec("Helpful fourth-house connection", [203], "If the fortunate Planet or Significator be Lord of the fourth",
    "A fortunate significator ruling or occupying the fourth indicates aid from a living father, grandfather or other older person; farms, land, buildings, inherited stock, or money lent by kin.",
    limits=["Living father is an explicit condition; occupation and lordship are alternative predicates."])
rec("Helpful fifth lord: social-role alternatives", [203, 204], "If the Lord of the fifth doe promise Wealth",
    {"gentleman": "play, cards, dice, sports or pastimes", "capable_courtier": "embassy or message", "ordinary_person": "victualling house, inn, tavern, bowling alley, doorkeeper or porter", "strong_fifth_lord_any_querent": "something from father's estate or making matches"},
    requires=["Fifth lord promises wealth."], limits=["Historical alternatives, not present recommendations or a replacement of the fourth-house inheritance association."], kind="conditional_reference_table")
rec("Sixth and a human sign: service and labour", [204], "If the Lord of the sixth, or Significator, or assistant Planet be in the sixth",
    "The sixth lord, significator or helping planet being in the sixth, with a human sign on the sixth, indicates good servants and profit from their labour; for a king/prince the continuation describes subjects' subsidies and loans.",
    limits=["Grammar leaves the exact scope of the human-sign and occupancy qualifications across the following occupational examples unresolved."])
rec("Sixth-house occupational alternatives", [204], "If a Nobleman or Gentleman enquire",
    {"nobleman_or_gentleman": "leases and discreet estate management by stewards or bailiffs", "farmer": "small cattle including sheep, goats, hogs and rabbits", "scholar": "physician's fees from sick people"},
    requires=["Continues the preceding sixth-house source branch."], limits=["Historical occupational symbolism; no medical-care or career recommendation is admitted."], kind="conditional_reference_table")
rec("Helpful seventh lord: partner, disputes and commerce", [204], "If the Lord of the seventh house fortunate the Lord of the second",
    "Seventh lord helping second lord, cusp, Fortune or second-house occupant points to a rich/good wife or a helpful woman; for a gentleman, war, legal recovery or bargains; for a merchant, ordinary trade acquaintances.",
    limits=["Preserve role-conditioned alternatives; marriage is one possible channel, not an obligatory means for every case."])
rec("Helpful eighth lord: inheritance, portion, unexpected residence", [204], "If the Lord of the eighth be that Planet who fortunates",
    "A helping eighth lord points to a bequest, an unexpected increase in a wife's portion, or voluntary residence in an unplanned country where substance increases.",
    limits=["Do not turn the source association into a forecast of someone's death."])
rec("Helpful ninth lord: sea and personal intermediaries", [204, 205], "If the Lord of the ninth give vertue or fortunate",
    "Ninth lord helping Fortune, second lord or cusp may signify a sea voyage when Cancer or Pisces is on the ninth cusp and its lord is there; other named channels are the wife's brothers/allies, a neighbour near her former home, or a religious person helping the vocation.",
    limits=["Original sign glyphs are Cancer and Pisces. Scope of the aquatic condition over the later personal alternatives is not formally specified."])
rec("Earthy ninth sign and its lord therein", [205], "If an Earthly Signe be on the cusp of the ninth",
    "An earthy ninth-cusp sign with its lord there points to moving toward the sign/quarter and trading the destination's native commodities.", requires=["Continues the wealth-promising ninth-house branch."])
rec("Tenth-house wealth predicates", [205], "If the Lord of the second be fortunate in the tenth house",
    "Second lord fortunate in tenth, reception between tenth and second lords, or tenth lord's benevolent configuration to second lord/cusp/occupant/Fortune signifies gain through service or employment by a superior.",
    limits=["Reception, occupation and aspect are alternative source predicates; no automatic employer-wealth frame is inferred from this general means-of-gain paragraph."])
rec("Tenth-house capacity qualifications", [205], "if one inquires that is young and of small fortune",
    "A young person of small means is assigned a mechanical trade fitting tenth sign and lord, if capable and fit; an educated person seeking advancement is assigned an office or public employment.",
    limits=["The capacity and preference inputs are explicit; this is historical source content, not career advice."], kind="synthesis_qualification")
rec("Helpful eleventh lord: recommendation and unexpected opportunity", [205], "If the Lord of the eleventh be that benevolent Planet",
    "A benevolent eleventh lord acting as the helping significator points to a friend's recommendation, merchant/courtier or servant of a great person, and unexpected advantageous employment or fortune.")
rec("Helpful planet in the twelfth: sign-conditioned channels", [205, 206], "If the Fortunate Planet who casts his Aspect as aforesaid be in the twelfth",
    {"twelfth_occupation": "great cattle or horse races", "human_sign": "imprisonment or imprisoned people", "Taurus_Capricorn_Aries": "cattle", "Virgo": "corn/grain"},
    requires=["The planet is actually fortunate/helping as previously described."],
    limits=["The author adds that judgement must be mixed with reason. Virgo's grain clause must not be merged into the three cattle signs."], kind="conditional_reference_table")
rec("Author's strongest lasting-wealth configuration", [206], "The most assured testimony in Astrology, and upon a Question onely propounded",
    "Lilly calls first lord, second lord and Jupiter together in second, first, tenth, seventh, fourth or eleventh the strongest testimony that a querent will be rich and remain so. If not conjunct, he gives application by sextile/trine with mutual reception; square/opposition with reception may still produce an estate through labour and intervening difficulty, with abundance rather than want.",
    limits=["Author's assurance claim, not measured accuracy. The three-body aspect/reception topology and whether the listed houses constrain all alternatives are not formalized locally."], kind="source_priority_rule")
rec("Obstruction analysis follows an adverse wealth judgement", [206], "When in any Question you find your Figure signifies the querent shall come to an estate",
    "The following obstruction analysis is unnecessary when wealth is already judged; it applies when no great fortune is shown and the asker wants the reason or impediment.",
    limits=["Do not combine opposite applicability branches into simultaneous supportive explanations."], kind="applicability_gate")
rec("Find the main obstructing planet", [206], "carefully observe the Planet obstructing",
    "Inspect the planet most afflicting second lord, Fortune, second cusp, Moon, or Fortune's lord/dispositor.",
    limits=["No complete severity metric or tie-breaker for most afflicting."])
rec("Obstructing first lord", [206], "if the Lord of the first be that Planet",
    "If the first lord is the obstructing planet, Lilly assigns the cause to the querent.",
    requires=["Adverse wealth judgement and that planet is the actual obstructer."], limits=["Historical attribution, not evidence of blame or psychological fact."])
rec("Obstructing second lord", [206], "if the Lord of the second doe with square or opposition behold",
    "Second lord square/opposite Fortune or the second cusp indicates lack of money or stock to establish employment.", requires=["Obstruction branch is applicable."])
rec("Obstructing third lord and continuation through houses", [206], "if Lord of the third, his own Kindred will doe nothing for him",
    "Third-lord obstruction is assigned to unhelpful/burdensome kin or neighbours taking trade or under-selling; the author instructs analogous interpretation through all twelve houses.",
    limits=["Only the first three causes are exemplified here. Do not invent nine additional verbatim source rows."], kind="reference_examples_and_extension_instruction")
rec("Malefics can help acquisition", [206, 207], "if the Lord of the second house, or Dispositor of Fortune be Infortunes",
    "Malefic second lord or Fortune dispositor may signify acquisition when essentially dignified, aspecting good planets, or occupying benevolent houses.",
    limits=["Natural malefic identity alone does not determine the financial testimony."])
rec("Benefics can obstruct acquisition", [207], "both Jupiter and Venus being afflicted or impedited",
    "Jupiter and Venus may obstruct when afflicted, impeded or assigned as the obstructing significators.",
    limits=["Role, condition and natural character remain separate; no universal positive Jupiter/Venus score."])
rec("South node's house-specific impediment", [207], "in what House you find Cauda Draconis",
    "The south node is assigned detriment in the topics of its house: in second, estate consumption by folly/neglect; in third, difficulty through kin; analogize through other houses.",
    limits=["Historical source symbolism, not a supported claim about present people."])
rec("Ordinary recovery/borrowing/pledge frame", [207], "If the Querent shall obtaine the Substance which he demands",
    {"asker": ["Ascendant", "Ascendant lord", "Moon"], "asker_money": [2, "second lord"], "other_party": [7, "seventh lord"], "other_party_money": [8, "eighth lord"]},
    requires=["Recovery, borrowing or pledged goods from the particular other party; ordinary comparable parties, qualified onPDF208."],
    limits=["The eighth is the second counted inclusively from seventh. Powerful superior uses another frame."], kind="query_frame")
rec("Ordinary recovery through eighth-house contact", [207], "See if the Lord of the Ascendant or the Moon be joyned",
    "Ascendant lord or Moon joining eighth lord, or joining/aspecting an eighth-house planet, may obtain desired money, loan or restored pledge when the planet is a fortune or the aspect fortunate; a fortunate eighth-house planet need not be received.",
    limits=["Keep the source's conjunction/aspect and reception alternatives; this is not a generic rule that any eighth-house contact succeeds."])
rec("Ordinary recovery through a malefic receiving the querent", [207], "if an infortunate Planet be in the eighth, or Lord of the eighth",
    "A malefic in or ruling eighth that receives Ascendant lord or Moon can give the desired recovery. Without reception the source predicts hardly ever obtaining it, or such labour that the requester regrets it.",
    limits=["Hardly ever / if ever is not rewritten as an absolute impossibility; reception direction is material."])
rec("Eighth lord enters first/second with second-lord reception", [207, 208], "if the Lord of the eighth be in the first, or in the second",
    "Eighth lord in first or second, received by second lord, makes accomplishment probable.",
    limits=["Source says probable; no numerical probability and no reception reversal."])
rec("Other-party lords in first/second without reception", [208], "if the Lord of the seventh, or of the eighth be in the first or second",
    "Seventh or eighth lord in first or second with no reception involving first lord, second lord or Moon indicates denial or further prejudice.",
    limits=["The phrase have reception of does not unambiguously formalize reception direction; retain rather than silently substitute a direction."])
rec("Joining a benefic dignified in Ascendant signs", [208], "If the Lord of the Ascendant and the Moon be joyned to a Fortune",
    "Ascendant lord and Moon joining a fortune with dignity in the rising sign or a sign intercepted in the Ascendant effects the matter.",
    limits=["Source names both in this clause; intercepted sign is retained."])
rec("Joining an Ascendant-dignified malefic with reception", [208], "if any of them be joyned to an Infortune",
    "Either querent significator joining a malefic with Ascendant dignity succeeds if that malefic receives Ascendant lord or Moon.",
    limits=["Reception and dignity are two requirements, not one favourable keyword."])
rec("Well-placed fortune in tenth or eleventh", [208], "Lord of the Ascendant or the Moon be joyned to a fortunate Planet",
    "Ascendant lord or Moon joining a fortunate planet well placed in tenth or eleventh effects the matter even without reception.",
    limits=["This does not erase reception requirements of the separate malefic branches."])
rec("Ordinary-party rule excludes powerful debtors", [208], "The Judgments of this Chapter shall then have place",
    "The immediately preceding recovery rules concern ordinary comparable parties such as citizen with citizen or tradesman with tradesman. Lilly exempts kings, princes and nobles who pay slowly and are little constrained by law.",
    limits=["Historical scope statement; no new modern social-rank classifier or categorical legal claim is inferred."], kind="scope_exception")
rec("Superior payment frame", [208, 209], "If one shall acquire that Gain or Profit, Wages or Stipend",
    {"asker": ["Ascendant", "Ascendant lord", "Moon"], "asker_money": [2, "second lord"], "superior": [10, "tenth lord"], "superior_money": [11, "eleventh lord"]},
    requires=["The asker is much inferior to the person from whom payment/accomplishment is expected."],
    limits=["The eleventh is the second counted inclusively from tenth. The rule applies to the declared relationship, not any preferred result."], kind="query_frame")
rec("Unimpeded eleventh-house benefic and payment", [209], "Lord of the Ascendant or the Moon joyned to the Lord of the eleventh",
    "Ascendant lord or Moon joining eleventh lord, or an eleventh-house planet that is a fortune unimpeded and not ill disposed, signifies obtaining salary, debt or wages owed by the great person.",
    limits=["Keep the original distinction between the lord clause and the qualified occupant clause; exact scope of the final qualification is a parsing uncertainty."])
rec("Malefic receiving querent significators in superior-payment enquiry", [209], "Moon and Lord of the Ascendant be joyned to an unfortunate Planet",
    "Moon and Ascendant lord joining a malefic that receives them into its essential dignities signify payment after much solicitation, weary approaches, fear and distrust.",
    limits=["Joining, reception, and named querent significators are preserved. The difficult path is separate from whether payment occurs."])
rec("Unreceived malefic in superior-payment enquiry", [209], "any Aspect be betwixt the Significators",
    "An aspect between significators where one is a malefic and reception absent signifies not obtaining the desire.",
    requires=["This is the superior-payment frame."], limits=["Unlike the ordinary recovery clause, this passage is categorical. Do not flatten the two into one outcome rule."])
rec("Reception type must be identified", [209], "be very carefull to observe the Planets true essentiall dignities",
    "Observe true essential dignities and mutual receptions, including which dignity receives the other significator.",
    limits=["Reception is not a single undifferentiated boolean for every downstream rule."], kind="method_instruction")
rec("Timing requires the actual effective significator", [209], "unto what Planet either the Lord of the Ascendant or Moon applyes",
    "Choose the planet to which Ascendant lord or Moon applies or bodily joins and which signifies accomplishment; in a sextile/trine case, whether that planet is a benefic or not, and whether it receives the Ascendant lord or Moon or not, inspect the rays through perfection or the degrees lacking to exact aspect/conjunction at the question.",
    limits=["Time-to-contact astronomy and symbolic distance-to-time are distinct. Static distance does not compute a moving contact date."], kind="timing_prerequisite")
HOUSE_PAIR_UNITS = {
    "cadent|cadent": "days", "succedent|succedent": "weeks", "angular|angular": "months",
    "angular|succedent": "months", "cadent|succedent": "weeks", "angular|cadent": "months"
}
rec("Second-house timing units by both houses", [209, 210], "so many dayes; if they be both in Cadent houses",
    HOUSE_PAIR_UNITS,
    requires=["Both selected significators and their houses known; degrees remaining to the relevant perfection."],
    limits=["These local units are not the sign-modality news scale or a universal Lilly timing rule. Fractional unit/calendar conventions are not defined."], kind="symbolic_unit_table")
rec("Timing units depend on plausible business duration", [209, 210], "the Astrologer must use discretion",
    "Consider whether the business can be completed in days, weeks or months. For a lengthy business, years may replace months, especially when Ascendant lord, Moon and other significators are angular.",
    limits=["No objective long-business threshold or automatic promotion rule is supplied. Do not choose a unit after seeing the outcome."], kind="timing_qualification")
rec("Ancients' same-sign conjunction route: heavier querent lord", [210], "Some of the Ancients have said",
    "Some ancients are reported to time accomplishment to exact degree-and-minute conjunction when the effective planet and Ascendant lord are in the same sign at the hour of the question and Ascendant lord is the more ponderous planet, whether reception exists or not.",
    limits=["Attributed prior view, not silently Lilly's own universal rule; ponderous does not mean merely comparing current daily velocity."], kind="attributed_timing_method")
rec("Ancients' lighter querent lord: reception branch and exceptions", [210], "if the Lord of the Ascendant be the more light Planet",
    "When the lighter Ascendant lord hastens toward conjunction, the effecting planet receiving it signifies accomplishment; the nonreception denial is subject to the following angular/domicile exceptions.",
    requires=["The two planets were in the same sign at the question, under the preceding attributed ancient method."],
    limits=["This is a different branch from the ponderous-lord condition. Read with LI.1647.II.XXVII.R838; the reception branch must not erase those exceptions."], kind="attributed_timing_method")
rec("Conjunction-route exceptions when reception absent", [210], "unlesse the foresaid significators be in an Angle",
    "Without that reception, accomplishment is denied unless the significators are angular at conjunction, or in one of his own houses, especially the house called his joy.",
    limits=["Own houses refers to zodiacal domiciles in the following sign examples. The pronoun his and its scope over the two significators remain ambiguous."], kind="attributed_exception")
rec("Joy means specified zodiac signs here", [210], "Aquarius is the joy of Saturn",
    {"Saturn": "Aquarius", "Jupiter": "Sagittarius", "Mars": "Scorpio", "Venus": "Libra", "Mercury": "Virgo"},
    limits=["Do not substitute the separate mundane-house planetary-joy scheme. Sun/Moon rows are not supplied in this local list."], kind="source_reference_table")
rec("Single exaltation reception alone insufficient in author's observation", [210], "What I have observed; single reception by exaltation",
    "Lilly reports single reception by exaltation without other testimonies does not profit.",
    limits=["Do not change single reception into mutual exaltation reception, or generalize absence of other testimony away."], kind="author_experience_claim")
rec("Domicile reception and benefic significators", [210], "reception by essentiall dignities of House",
    "Domicile reception when benevolent planets are significators usually shows perfection, even by square/opposition and beyond expectation; sextile/trine is treated more confidently.",
    limits=["Usually remains qualified; no numerical likelihood, universal aspect reversal, or dismissal of benefic condition."], kind="author_experience_claim")
rec("Ascendant-cusp distance timing alternative", [210], "And for the time when, I observe",
    "If a fortune, Moon or lord of the thing sought occupies the Ascendant with essential dignity there, degrees from cusp to body denote time: days with a movable sign and a business capable of days, otherwise months or years according to sign and business.",
    limits=["The text does not provide a complete fixed/common months/years lookup here; do not invent it or calculate a civil date."], kind="author_timing_method")
rec("Tradesman's one chart and four linked questions", [211], "A Tradesman of this City in the yeer1634",
    ["whether rich or able to subsist without marriage", "by what means", "when", "whether wealth continues"],
    limits=["Lilly says he has seen experience of his judgment. This is one author-selected retrospective inquiry with four linked endpoints, not four independent validation cases. The diagram belongs to the following worked discussion."], kind="historical_case_introduction")


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def build():
    additions = ROOT / "XXVIII_EXTRACTED.json"
    if additions.exists():
        for row in json.loads(additions.read_text())["records"]:
            rec(row["title"], row["pages"], row["anchor"], row["statement"],
                row.get("requires", []), row.get("limits", []), row.get("kind", "conditional_source_rule"), "XXVIII")
            for field in ("worked_values", "candidate_origin"):
                if field in row:
                    RULES[-1][field] = row[field]
    save("RULES.json", {
        "schema_version": 1, "batch": "B02g", "source_id": SOURCE_ID,
        "source_sha256": SOURCE_SHA256, "records_count": len(RULES), "rules": RULES,
        "first_record_number": 775, "last_record_number": 774 + len(RULES),
        "declared_source_scope": "Book II second-house block: XXVII heading PDF201 through XXVIII ending PDF221 before third-house preamble",
        "scope_status": "XXVII_AND_XXVIII_EXTRACTED_WITH_PRESERVED_UNRESOLVED" if additions.exists() else "XXVII_EXTRACTED_XXVIII_PENDING",
        "statement_notice": "Normalized source claims; not validated financial predictions or practical advice.",
        "runtime_promotions": 0, "empirical_validations": 0
    })
    save("QUERY_FRAMES.json", {
        "general_wealth": {"querent_house": 1, "querent_money_house": 2, "counterparty_house": None, "counterparty_money_house": None, "pages": [201]},
        "ordinary_specific_counterparty": {"querent_house": 1, "querent_money_house": 2, "counterparty_house": 7, "counterparty_money_house": 8, "pages": [207, 208], "precondition": "comparable ordinary parties"},
        "powerful_superior_payment": {"querent_house": 1, "querent_money_house": 2, "counterparty_house": 10, "counterparty_money_house": 11, "pages": [208, 209], "precondition": "querent much inferior to payment source"},
        "note": "Choose the relationship before evaluating chart evidence; these are three separate source questions."
    })
    save("TIMING_REFERENCES.json", {
        "house_pair_profile": "LILLY_II_XXVII_WEALTH_HOUSE_PAIRS",
        "house_pair_units": HOUSE_PAIR_UNITS, "pages": [209, 210],
        "long_business_may_replace_months_by_years": True,
        "long_business_threshold": None,
        "separate_routes": ["symbolic degrees to perfection with house-pair units", "actual exact conjunction under the attributed same-sign method", "degrees from Ascendant cusp to dignified qualifying occupant"],
        "ascendant_cusp_complete_modality_table": None,
        "civil_dates_computed": False, "automatic_forecast": False
    })
    print(json.dumps({"records_count": len(RULES), "first_id": RULES[0]["id"], "last_id": RULES[-1]["id"]}))


if __name__ == "__main__":
    build()
