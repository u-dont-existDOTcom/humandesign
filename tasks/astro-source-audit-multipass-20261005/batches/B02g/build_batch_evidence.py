"""Build the bounded source-audit context, ambiguity and case-evidence records."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
SOURCE = "LILLY1647_WELLCOME_B30338724"
SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"


def rid(number):
    return f"LI.1647.II.{'XXVII' if number <= 843 else 'XXVIII'}.R{number}"


def save(name, data):
    (ROOT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def build():
    endpoints = [
        ("competent_estate", [216], "Estate and competent fortune with labour and care", "Author says the querent has this up to the time of writing", "AUTHOR_REPORTED_UP_TO_WRITING", "No amount or independently documented outcome; does not isolate wealth without marriage."),
        ("wife_money_and_land", [216, 217], "Wife brings a good, fixed fortune beyond expectation", "Man reports a good fortune with his wife, both money and land", "SUBJECT_REPORT_RELAYED_BY_AUTHOR", "No independent valuation; not a separate case."),
        ("successful_trade", [217], "Competent estate through diligence in his profession", "Trading said to have been very good", "AUTHOR_REPORTED_GENERAL_OUTCOME", "Broad trade report does not verify every date, mechanism or cause."),
        ("wife_portion_about_two_years", [217], "About two years from roughly two degrees Ascendant–Mars", "Author says he had a portion with his wife at that time", "AUTHOR_REPORTED_APPROXIMATE_TIMING", "No exact event date, monetary amount, calendar conversion or original prediction freeze."),
        ("about_1640_trade_reputation_friends", [217, 218], "Very great trade, excellent repute and helpful friends about 1640", None, "JUDGEMENT_WITHOUT_SEPARATE_ENDPOINT_CONFIRMATION_IN_SCOPE", "The general good-trade report does not independently verify this dated cluster."),
        ("lasting_competence", [220], "Competent fortune continues without poverty or want", None, "JUDGEMENT_WITHOUT_FULL_LIFETIME_OUTCOME", "No full-life follow-up; rich does not mean constant increase or an unchanging asset balance."),
        ("kin_and_servants", [221], "Poor unity with kin/siblings and trouble or behavioural blemishes in servants", None, "SOURCE_JUDGEMENT_ONLY", "Do not treat the author's moralized character language as verified personal facts."),
        ("solar_friends", [221], "Caution about engagements with or confidence in solar men, even friends", None, "SOURCE_CAUTION_ONLY", "Neither an observed loss nor a retraction of all earlier helpful-friend testimony is reported."),
    ]
    save("HISTORICAL_CASES.json", {
        "source_id": SOURCE, "source_sha256": SHA,
        "cases": {"tradesman_1634": {
            "identity": "Unnamed city tradesman in Lilly's selected retrospective example",
            "source_pages": list(range(211, 222)),
            "figure_date_text": "16. Iuly 1634", "chart_minute_reading": "0 versus 6 unresolved; not used",
            "question_endpoints": ["rich or subsist without marriage", "means", "when", "continuation"],
            "query_record": rid(843), "chart_record": rid(844),
            "chart_inputs_file": "WORKED_NUMERIC_TABLES.json", "static_arithmetic_file": "ARITHMETIC_CHECKS.json",
            "marriage_qualification": "The author says the man would subsist less well without marriage; the reported married outcome does not validate the unmarried counterfactual.",
            "outcome_records": [{"endpoint": key, "source_pages": pages, "source_judgement": prediction,
                                 "reported_result": report, "evidence_type": evidence, "limit": limit}
                                for key, pages, prediction, report, evidence, limit in endpoints],
            "selected_historical_case_count": 1, "independent_validation_cases": 0,
            "full_lifetime_observation": False, "original_prediction_freeze_available": False,
            "modern_participant_data_used": False, "natal_transfer_admitted": False,
        }},
        "notice": "Multiple statements about one chart/person remain dependent. No predictive accuracy is computed."
    })

    issues = [
        ([204, 205, 208, 209], [800, 804, 822, 829], "witness_pagination", "Four visible folios depart from sequential PDF order", "Visible labels are preserved; cause of the anomaly is not established and prose is not reordered."),
        ([201, 202], [778, 779, 780, 791], "undefined_synthesis", "Good houses, moderate dignity and major testimonies have no complete numerical rule here", "Do not convert testimony inventory into probabilities or an automatic wealth verdict."),
        ([202], [781, 782, 783], "clause_grouping", "Conjunction/benefic alternatives have nonformal coordination", "Keep printed and/or distinctions; exact multi-planet Boolean grouping remains unresolved."),
        ([202, 215], [788, 858], "unspecified_proximity", "Near fixed stars lacks a complete local coordinate/tolerance specification", "Spica is given at Libra18 without minutes; do not insert zero minutes. Regulus has no exact coordinate in this span."),
        ([203], [794], "source_selection", "Aspect-source house or Moon lordship offers alternatives without a tie-breaker", "No new priority or independent-evidence count assigned between these alternatives."),
        ([204], [800, 801], "qualification_scope", "How far sixth-house human-sign/occupancy conditions extend over later occupations", "Opening occupancy retained; later attachment remains explicit rather than silently broadened."),
        ([204, 205], [804, 805], "qualification_scope", "Ninth-house aquatic condition and later personal-intermediary alternatives", "Cancer/Pisces and lord therein preserved; the later alternatives' condition scope is not made certain."),
        ([206], [810], "relational_topology", "Three significators, reception and listed houses in strongest continued-wealth rule", "No invented all-pairs relation, house override or numeric confidence."),
        ([206], [812], "undefined_severity", "Most afflicting planet has no complete severity/tie rule", "Obstructer selection cannot be optimized after the outcome."),
        ([208], [823], "reception_direction", "Have reception of in the negative ordinary-party clause", "Keep direction unresolved where the source is less explicit; do not reverse clear receiving clauses elsewhere."),
        ([209], [829], "qualification_scope", "Scope of unimpeded/benefic conditions across superior-payment alternatives", "Preserve distinct lord and occupant clauses instead of pretending a unique parse."),
        ([209, 210], [833, 834], "astronomy_vs_symbolism", "Distance to perfection and actual time to moving contact differ", "Static degrees alone cannot yield an astronomical encounter or civil date."),
        ([209, 210, 217, 218], [834, 835, 873, 875, 877], "timing_discretion", "Business duration may replace months with years without an objective threshold", "Separate timing profiles; no after-outcome choice of unit or universal degree/year rule."),
        ([210], [836, 837, 838], "pronoun_and_branch", "His own houses and angular exception in the attributed ancient conjunction route", "Same sign at question is required; pronoun ownership and one/both planet scope remain unresolved."),
        ([210], [842], "incomplete_lookup", "Ascendant-distance route supplies no complete sign-to-unit table", "Movable/capable-of-days branch retained; no invented common/fixed months/years mapping."),
        ([211], [844], "reader_disagreement", "Chart minute glyph read as 0 by root/XXVIII reader and as 6-like by XXVII checker", "Retain 0-versus-6 ambiguity; no calculation or calendar claim uses the chart time."),
        ([211], [844], "unresolved_shorthand", "Compact final chart-centre aspect shorthand not fully secure", "Printed positions are retained, but the unresolved shorthand is not promoted as another rule."),
        ([211], [844], "historical_time_convention", "Historical calendar, local time convention and modern UTC conversion unresolved", "No modern sky recomputation or parity claim."),
        ([212, 217], [845, 872], "source_discrepancy", "Four swift planets in motion rows versus five in timing prose", "Both source readings preserved; count mismatch is not repaired in the witness."),
        ([213, 215, 221], [848, 857, 895], "qualitative_vs_numeric", "Jupiter's qualitative afflictions are not numerical debits in the printed tally", "Retain the table and the separate affliction claims; no invented combined score."),
        ([214], [854], "case_specific_exception", "Fortune admitted to second despite being 6 degrees25 minutes before its cusp", "No general replacement threshold follows; a strict universal five-degree rule is not admitted."),
        ([220, 221], [894, 895], "contact_tolerance", "Exact antiscia criterion coexists with near Saturn contra-antiscion to Jupiter", "Computed residual is2 degrees50 minutes; no universal near cutoff is supplied."),
        ([219], [882], "internal_syntax", "Receives followed by neither receiving nor received in one sentence", "No silent emendation or runtime formalization; potentially different senses remain an interpretation."),
        ([218, 219], [879, 883], "missing_relation", "Nested obstruction chains contain unclear pronouns or an omitted joining relation", "Record provisional editorial relation mapping, not a proven executable graph."),
        ([218, 219], [880], "condition_grouping", "Ill-disposition list and cadency/non-beholding attachment", "No invented conjunction/disjunction over every item or additive score."),
        ([219, 220], [885, 886], "reception_role", "A planet in hard-aspect rejection lacks a fully explicit role in its first clause", "Keep the well-disposed-receiver exception and received-planet impediment distinct."),
        ([220], [889], "missing_receiver", "Impedited malefic in translation must be received again, but receiver unnamed", "Do not assign the receiving agent by convenience."),
        ([217, 218], [873, 875], "approximate_timing", "About-two-year and about1640 statements are not exact date formulas", "Printed distances reproduced without inventing event dates or precise forecast windows."),
        ([211, 216, 217, 218, 220, 221], [843, 863, 870, 873, 875, 893, 895, 896], "evidence_limit", "Reported outcomes do not document every endpoint or full lifetime", "One selected retrospective case; no independent accuracy rate, counterfactual success, or lifelong verification."),
        ([221], [896], "enumeration", "Two things in the closing caution lacks an unambiguous numbered pair", "Do not manufacture two independently confirmed warnings."),
        ([214, 215, 216, 217, 220], [854, 855, 862, 874, 893], "synthesis_missing", "No complete rule combines net score, dignity, office, reception and fixed-sign testimony", "Positive/negative totals are not a complete engine and repeated roles are dependent."),
        ([215], [855], "tie_rule_missing", "Subtract-lesser-from-greater rule gives no tied-score interpretation", "Exact arithmetic is reproducible; zero-score semantic outcome remains unspecified."),
    ]
    save("UNRESOLVED.json", {"source_id": SOURCE, "batch": "B02g", "issues_count": len(issues),
        "issues": [{"id": f"B02g.U{i:03d}", "source_pages": pages, "record_ids": [rid(n) for n in numbers],
                    "kind": kind, "issue": issue, "disposition": disposition, "status": "OPEN_PRESERVED"}
                   for i, (pages, numbers, kind, issue, disposition) in enumerate(issues, 1)],
        "notice": "Open includes source discretion and evidence limits, not only transcription defects; these are not repaired by fitting the outcome."})

    groups = [
        ("general_wealth", 775, 791, "General question with no named source of fortune", "General testimonies require synthesis and the querent's condition; no calibrated score."),
        ("means_after_positive_judgement", 792, 810, "Prior judgement that wealth/subsistence is promised", "Choose the actual helping significator; do not pool every house narrative."),
        ("obstruction_after_adverse_judgement", 811, 818, "No great fortune shown and cause requested", "Keep mutually conditioned explanatory branches distinct."),
        ("ordinary_counterparty", 819, 827, "Comparable ordinary parties; other party7, money8", "Do not transplant to powerful superiors; receiving malefic is not the same as received malefic."),
        ("superior_payment", 828, 832, "Querent much inferior to payment source; source10, money11", "Source relation chosen before evaluating the chart."),
        ("general_wealth_timing", 833, 842, "Selected effecting significator and source route", "House pairs, same-sign conjunction and Ascendant-distance routes remain separate."),
        ("one_worked_case", 843, 877, "Tradesman1634, one dependent chart/person", "Case facts do not become independent sufficient rules or untouched validation."),
        ("hindrance_and_perfection_context", 878, 892, "General horary insertion; include its full exception chain", "No individual reception/abscission clause may erase applying, condition, direction or later exceptions."),
        ("case_continuation_and_cautions", 893, 896, "Returns to the same tradesman case", "Competence, kin/servants and solar-friend cautions have distinct evidence scope."),
    ]
    save("APPLICABILITY_AND_RELATIONS.json", {
        "source_id": SOURCE, "status": "SOURCE_CONTEXT_LINKS_NOT_RUNTIME_DECISION_ENGINE",
        "groups": [{"id": key, "record_ids": [rid(n) for n in range(first, last+1)], "applicability": context, "guard": guard}
                   for key, first, last, context, guard in groups],
        "exception_links": [
            {"rule": rid(837), "must_carry": [rid(836), rid(838), rid(839)], "why": "Same-sign query-time condition and nonreception exceptions."},
            {"rule": rid(881), "must_carry": [rid(885), rid(886), rid(887)], "why": "General reception rescue is qualified by aspect, condition and application."},
            {"rule": rid(885), "must_carry": [rid(886)], "why": "Ill-conditioned hard-aspect rejection has a well-disposed-receiver exception."},
            {"rule": rid(884), "must_carry": [rid(878), rid(879)], "why": "Interruption removes the harmful contact here; abscission's polarity follows what it interrupts."},
            {"rule": rid(891), "must_carry": [rid(892)], "why": "The paragraph's Moon/other-aspect reservation accompanies both directions."},
        ],
        "ordered_lunar_transfer": {"record": rid(860), "source_pages": [215, 216, 217],
            "sequence": ["Moon separates Mars sextile", "Moon then separates Mercury conjunction", "Moon applies Venus conjunction"],
            "transferred_from": ["Mars", "Mercury"], "transferred_to": "Venus", "physical_times_computed": False},
        "role_overlap_in_case": {"Venus": ["querent Ascendant lord", "wife-money eighth lord", "Mars dispositor"],
            "Mars": ["second lord", "seventh lord", "Fortune dispositor"], "Moon": ["general cosignificator", "tenth lord", "translator"],
            "independent_evidence_count": None},
        "point_semantics": {"Fortune_and_nodes_emit_rays": False, "planetary_aspects_received_by_points": True,
                            "source_record": rid(777), "geometry_symmetry_is_not_semantic_symmetry": True}
    })

    comparisons = [
        ("question_frame", [rid(775), rid(819), rid(828)], ["B02f/QUERY_FRAMES.json"],
         "The declared question and relationship select significators", "Wealth frames use1/2,7/8 or10/11; the retained absent-person/presence distinctions provide another context-specific use. No universal other-person house is inferred."),
        ("timing_profiles", [rid(834), rid(835), rid(842), rid(873), rid(875)], ["B02e/RULES.json:R575,R619,R620", "B02f/RULES.json:R706"],
         "Timing tables belong to particular questions and source routes", "Current house-pair days/weeks/months is separate from retained sign-modality health/news scales and the worked years choice. No combined choose-the-best scale."),
        ("fortune_formula_and_genre", [rid(844)], ["B02e/RULES.json:Fortune section", "B01j/RULES.json:PT.R64.IV.02.R335-R338"],
         "Same algebra can appear in different interpretive genres", "The retained Lilly and Ptolemy formulas agree on Ascendant+Moon−Sun without sect reversal; Robbins questions the authenticity of the Ptolemy formula clause, and that textual qualification remains. Shared algebra does not transfer horary wealth outcomes to the natal context. This comparison uses retained audited records, not a fresh full-source read."),
        ("cusp_assignment", [rid(854)], ["B02f/RULES.json:LI.1647.II.XXV.R714", "B02f/lilly_presence_ship_reference.py:beyond_cusp_window"],
         "Preserve case-specific house attribution against a universal cutoff", "The retained negative example distinguishes a beyond-five-degree exclusion; current Fortune is expressly admitted despite6d25m. Do not rewrite either witness or promote one universal5d predicate."),
        ("long_ascension_square", [rid(859)], ["B02f/lilly_presence_ship_reference.py:square_equivalence_reference"],
         "Interpretive square/trine comparison leaves longitude geometry unchanged", "Both retained references describe a long-ascension valuation. The geometric aspect remains90degrees; no latitude limit, numerical conversion or replacement orb is supplied here."),
        ("natural_character_vs_office", [rid(816), rid(817), rid(874)], ["B01j/RULES.json:PT.R64.IV.02.R339"],
         "Planetary office and context qualify a simple benefic/malefic label", "Lilly expressly allows an Infortune to produce the matter through its office. Retained Ptolemy natal wealth channels include Saturn-related routes. This is a limited conceptual comparison, not a merged rule or identical mechanism."),
        ("case_and_endpoint_dependence", [rid(843), rid(870), rid(873), rid(875), rid(893)], ["B02f/HISTORICAL_CASES.json"],
         "One chart and its linked claims do not create multiple independent validations", "Current four questions and eight evidence entries refer to one selected case. Prior hypothetical chart reuses likewise remain dependent; outcome precision must match the particular claim."),
    ]
    save("CROSS_SOURCE_COMPARISONS.json", {"status": "REFERENCE_COMPARISONS_NOT_MODEL_MERGER", "comparisons": [
        {"id": f"B02g.C{i:02d}", "topic": topic, "current_records": current, "retained_anchors": old,
         "finding": finding, "limit": limit, "retained_source_material_reread_as_new_book_pages": False}
        for i, (topic, current, old, finding, limit) in enumerate(comparisons, 1)]})

    sections = [
        ([201, 202], 775, 791, "General wealth inputs and favourable testimonies"),
        ([202, 203, 204, 205, 206], 792, 810, "Conditional means, all twelve house channels, continued-wealth configuration"),
        ([206, 207], 811, 818, "Adverse wealth branch and obstructions"),
        ([207, 208], 819, 827, "Ordinary other-party money and scope exception"),
        ([208, 209], 828, 832, "Payment from a much superior person"),
        ([209, 210], 833, 842, "Timing methods and reception qualifications"),
        ([211], 843, 844, "One case introduction and printed figure"),
        ([212, 213, 214, 215], 845, 856, "Motion, all strength rows, Fortune and antiscia table"),
        ([215, 216], 857, 864, "Wealth reasoning and marriage qualification"),
        ([216, 217], 865, 871, "Means and reported results"),
        ([217, 218], 872, 877, "Approximate timing and reason/art qualification"),
        ([218, 219, 220], 878, 892, "Hindrance, reception, abscission, translation, collection and direction"),
        ([220, 221], 893, 896, "Persistence, antiscia and concluding cautions"),
    ]
    save("SECTION_COVERAGE.json", {"source_id": SOURCE, "scope_status": "SECOND_HOUSE_XXVII_XXVIII_EXTRACTED",
        "sections": [{"pages": pages, "record_ids": [rid(n) for n in range(start,end+1)], "heading_or_function": title}
                     for pages,start,end,title in sections],
        "first_boundary": "PDF201 XXVII heading after already-completed self-question paragraph",
        "last_boundary": "PDF221 after see page71, before horizontal rule and third-house heading",
        "next_source_to_extract": {"pdf_page":221,"printed_page":187,"position":"third-house heading and preamble below horizontal rule", "following_chapter":"XXIX at PDF222/printed188"},
        "boundary_preview_is_not_extraction": True, "records_total": 122})

    labels = {204:"174",205:"175",208:"170",209:"171"}
    save("READING_RECEIPT.json", {"source_id": SOURCE,"source_sha256":SHA,"source_page_count":894,
        "source_size_bytes":141842963,"source_url":"https://archive.org/download/b30338724/b30338724.pdf",
        "original_witness_matches_predecessor":True,"independent_local_download_hash_matched":True,
        "root_actually_viewed_pdf_pages":list(range(201,222)),
        "separate_xxvii_checker_actually_viewed":list(range(201,212)),
        "separate_xxviii_reader_actually_viewed":list(range(211,223)),
        "viewed_page_count_in_extraction_span":21,
        "page_labels":[{"pdf_page":p,"printed_sequence_expected":p-34,"visible_folio":labels.get(p,str(p-34))} for p in range(201,222)],
        "method":"Original whole-page images alongside existing PDF text; no new OCR. Original images, PDF and full raw text kept outside repository.",
        "third_house_exposure":"Heading/preamble on221 and XXIX heading on222 previewed for boundary only; not yet extracted as source records.",
        "image_production_is_not_reading_claim":True,
        "chart_minute_disagreement":"0 versus6 unresolved; no chart-time calculation admitted",
        "reader_evidence":["review/XXVII_SOURCE_NOTES.md","review/XXVIII_READING_RECEIPT.json","review/XXVIII_READER_FINDINGS.md"],
        "natal_or_current_personal_analysis":False,"runtime_model_promoted":False,"predictive_validation":False})
    print(json.dumps({"source_records":122,"unresolved_issues":len(issues),"historical_cases":1,"comparisons":len(comparisons)}))


if __name__ == "__main__":
    build()
