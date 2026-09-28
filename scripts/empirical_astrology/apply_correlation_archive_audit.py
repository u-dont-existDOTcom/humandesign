"""Mechanically merge the source-verified Correlation audit into the v2 ledgers.

This is evidence bookkeeping, not a scientific gate or model revision. Paid PDFs stay
in the owner's authenticated archive; no article text or owner's outcomes are loaded.
Run at the repository root with: python scripts/empirical_astrology/apply_correlation_archive_audit.py
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "data/empirical_astrology"
AUDIT = ROOT / "notes/empirical_astrology/fulltexts/CORRELATION_ARCHIVE_AUDIT_20260928.md"
ARCHIVE = "/home/joel/Documents/astrology/correlations journal/"

# SHA-256 of the *complete issue PDF*, verified on the owner's authenticated machine.
FILES = {
    "c19850501.pdf": "0cc4ec7aa902db2f96aa4b870f5943053ba07c1c2b05ef6f6cd0152a9e5b8ffe",
    "1985 Vol 5.2 c19850502.pdf": "9b750518c770acff354822a3f541d16bd8c557a6534e5b2031ea1a81dc298776",
    "c19880801.pdf": "c2e93ac4feca60288d8ea81bc91f72d53e695f1c3dd1d412fc270a1fca8fae0d",
    "c19880802.pdf": "b4cb099182522d6ce01d98ec31631ccaf21f16e601cebbf43e9e7c14ff7369c4",
    "1995 Vol 14.1 c19951401.pdf": "5e4a5324ab51dca9562499b465fa44dbefca207898742fc1f84db67eed897b01",
    "c19951402.pdf": "16295a3ea295b639b446e5f8cc31a165df86520f8bc7c6b46fcb4502781463d5",
    "c19971602.pdf": "1b43a809f619c5a771c40225f6910bb9237d923a90f72b004bc4a3e90fc0e12d",
    "c20022002.pdf": "1301c789114522c6f79a1ee03223df98d3425450e07dcbb563120f7bfe13e198",
    "Ruis 2008 Correlation 25.2 author copy.pdf": "601a9eee27f9c7628fd631cb455b167eb0e26ce2085be589eba20131b6153c46",
    "c20122802.pdf": "0bf4e572a1a81175063a8471b4aad69fe6c26a6dc242048cc17074aeff07aa68",
    "c20132901.pdf": "6beb41077dd2fe14c006e0160ee6d85b9da0bfc5557aed63926a863477c69abe",
    "c20142902.pdf": "21db747d590fb19e9e28511bbddcdc56a3842090f37a8d6d5336b2566e6eee25",
    "c20153001.pdf": "9490fca498d8c2ef69227088ff8d207946ba41283ef60091d3b7258b3e1efe31",
    "c20163002.pdf": "30e3b2e601a8385c62ae2b9945ed728480ba889af43f29a740b276ea2eb318ca",
    "c20173101.pdf": "18805d7403a855f0a8d07345e8a6a703bf0029263ff2f4f88acf09e5e930d99c",
    "c20183102.pdf": "86f60ab1090abe40e2bead74c72f719f49d98452edd94e9ab94bfa6946e28b72",
    "c20183201.pdf": "0ded30ac717411012f820f4f53e8165f886975cf8b9221d6795b621da3d43061",
    "2021 Vol 34 01 c20213401.pdf": "4fe9903d30cbe6c6c27c9bffee599ec6bfc396ef146666573184369e6eb99d9b",
    "2022 Vol 35 01 c20223501.pdf": "b9351c36831eecff8f5a199a5b04bae35720a0879d7723760247f93b61e09205",
    "2023 Vol 35 02 c20233502v2.pdf": "780b8422d77059892b57c395d9cf3c2b40f828706b0c2ed51a7bcabb0b03aac6",
    "2023 Vol 36 01 c20233601.pdf": "a4c0da056639aa0833dd96229a4efc3817395729b26c361875f24322f5092f44",
    "2024 Vol 36 02 c20243602.pdf": "d50048c5a6f34c06ef6eaa0cc77439243c55137c514149d8f09b304d5862195d",
    "2024 Vol 37 01 c20243701.pdf": "bf402a46d5f9fa1ea19cf8be6627b167b37982d62f0f22cb5abf237da2188d5b",
    "2026 Vol 38 01c20263801.pdf": "e3ad72ee69c213ebe79739c025c91357fd7c112eefc8468bbdb43911ee9e8e73",
    "2026 Vol 38 02 c20263802.pdf": "5d6a87dc0e5aff058d007a66b2104035a27b639a566fa078ab1e0539d7af1024",
}


def row(id, authors, year, title, issue, file, n, ds, feature, outcome, controls, result, failure, lineage, birth, role="original_empirical_report"):
    return dict(id=id, authors=authors, year=year, title=title, issue=issue, file=file, n=n,
                ds=ds, feature=feature, outcome=outcome, controls=controls, result=result,
                failure=failure, lineage=lineage, birth=birth, role=role)


ARTICLES = [
    row("SRC-9BD900BE058818", ["Geoffrey Dean"], 1985, "Can Astrology Predict E and N? 1. Individual Factors", "Correlation 5(1), 3–17", "c19850501.pdf", 1198, "DS-1B2E876C2D16", "132 tropical/sidereal sign, decan, element, aspect, 75-factor discriminant, midpoint ±2°, aspect ±7.5°, angularity ±10°", "extreme EPI extraversion and neuroticism", "opposing extreme groups/replicate subsets; chance predictions", "58/132 directional confirmations; 12 p<.1 versus 13 expected; no replicated candidate", "isolated sign self-attribution; many predictors", "Shared 1,198 volunteers with Part 2; internal split is not independent cohort", "recorded birth times; Eysenck questionnaire"),
    row("SRC-6B50EC5034D723", ["Michel Gauquelin"], 1985, "Astrological Aspects at the Birth of Eminent People", "Correlation 5(1), 25–35", "c19850501.pdf", 15334, "DS-29D424AA5761", "five VE/MA/JU/SA planetary pairs, 0/60/90/120/180° ±5°", "eminent occupational group", "other Gauquelin profession groups", "mean aspect departure ~1.4%; selected cells near chance and no sector linkage", "no stable aspect association", "Gauquelin profession program; overlaps Ertel and Tarvainen", "historical birth records with variable time precision"),
    row("SRC-36A24656EBF177", ["Geoffrey Dean"], 1985, "Can Astrology Predict E and N? 2. The Whole Chart", "Correlation 5(2), 2–24", "1985 Vol 5.2 c19850502.pdf", 160, "DS-E9E0C5CFBB82", "45 astrologers interpret whole charts; 45 no-chart guessers", "binary extreme E/N personality", "no-chart guesses, chance, cue test", "5,400 judgments/dimension; astrologers 50.3%, no-chart 51.0%, chance 50%", "no skill by confidence/experience/time; cue-information pathway", "Same volunteers as Part 1; rater rows not independent", "timed birth charts; EPI"),
    row("SRC-97B1D36F3A34B6", ["Suitbert Ertel"], 1988, "Relating Planetary Aspects to Human Birth: Improved Method Yields Negative Results", "Correlation 8(1), 5–21", "c19880801.pdf", 20528, "DS-8937B9A5AFE9", "5 planet pairs × 0/90/180° ±5°; 15 aspect windows", "observed birth counts in aspect windows", "neighbor windows and ±266-day shifted birth dates", "165 tests: two nominal p<.05 versus five/six in shifted controls, zero p<.01", "negative aspect replication; non-independent windows", "Reanalysis of Gauquelin profession records", "historical timed birth records"),
    row("SRC-21918CDBF05EE1", ["Mavis Klein"], 1988, "The Accuracy of Relationship Description as a Test of Astrology", "Correlation 8(2), 5–17", "c19880802.pdf", 122, "DS-02EB46BDA8BC", "rank authentic interchart-aspect relationship description among five", "partner description recognition", "random or same-Sun-sign constructed partner controls", "author reports aggregate p<.01; 54 responding couples dependent", "instructions changed during collection; some controls contrived", "Partner responses clustered by couple; no separate replication", "unknown birth times; aspects only, no angles/houses"),
    row("SRC-FCBB0829EE54D3", ["Suitbert Ertel"], 1995, "Birth Time Precision and the Gauquelin Effect", "Correlation 14(1), 30–37", "1995 Vol 14.1 c19951401.pdf", 27198, "DS-5C8C7B17E752", "nonrounded versus rounded birth hour crossed with planetary G-sectors", "G-sector excess by precision/era/planet", "era/profession/planet strata", "nonrounded ~1.02 percentage points LOWER overall; post-1880 ~1.52 points, p≈.03; Saturn exception", "precision hypothesis direction fails; planet heterogeneity", "Gauquelin professions reused, some subjects counted for multiple planets", "nonrounded 8,388; rounded 19,010 planet-specific observations"),
    row("SRC-41C1A14D8EDB9B", ["Geoffrey Dean"], 1995, "A Re-Assessment of Jung’s Astrological Experiment", "Correlation 14(2), 12–22", "c19951402.pdf", 483, "DS-E1A97CA49DC0", "Jung's 50 interchart marriage contacts ±~8°", "contact frequency in marriage pairs", "32,220 cross-pair controls in first 180-set; 50-contact multiple-test null", "first leading 18/180 p=.00232 single contact but ~.11 over 50; only one common top-four across sets", "Jung published only subsets of contacts in later sets", "Reanalysis of original Jung 180+220+83 couples, not 19 new studies", "historical chart times not fully available", "reanalysis"),
    row("SRC-C5D64810AF636C", ["Geoffrey Dean"], 1997, "John Addey’s Dream: Planetary Harmonics and the Character Trait Hypothesis", "Correlation 16(2), 10–39", "c19971602.pdf", 1980, "DS-1405304BC645", "158 selected biography traits × planetary sectors × 20 harmonics × duplicate counts", "character traits in biographies", "person-based rather than trait-count-based sector expectancies", "~12,000 amplitudes pass loose cutoffs by chance; sector-8 example exp10.9 by traits vs8.2 by persons", "trait/person dependence and author-selected labels", "Reanalysis of existing Gauquelin biographies, ~1,980 trait subsamples from 5,944 professionals", "historic timed births; biographical trait coding", "reanalysis"),
    row("SRC-CB1D87C64AF1FA", ["Bernadette Brady"], 2002, "The Australian Parent-Child Astrological Research Project", "Correlation 20(2), 4–38", "c20022002.pdf", 1250, "DS-91EB1D56800E", "eight families: ±9° angularity/Moon conjunction, old/new rulership, nodding, matching signs, exaltation, double signs", "parent–child chart correspondence and birth order", "500 simulated ASC frequencies, shuffled unrelated families, Gauquelin subsample", "338 tests: 18 p<.05 vs16.9 expected; new rulers zero/42; parental Moon nodding failed Gauquelin 630-parent comparison", "families and siblings dependent; nominal p not familywise", "Australian recruited families; separate Gauquelin subset not success replication", "immediate-family/hospital times ≤10-minute uncertainty; ~20% excluded"),
    row("SRC-7C6A67F3AEE43C", ["Jan Ruis"], 2008, "The Birth Charts of Male Serial Killers: Evidence of Astrological Effects?", "Correlation 25(2), 7–44", "Ruis 2008 Correlation 25.2 author copy.pdf", 293, "DS-1AFC0CF1EB5E", "mutable signs, Moon-aspect omnibus, 12th principle, Neptune hard aspects, Mars-slow and Chiron nulls", "male serial-killer case status", "~6,000 matched-era/region ADB, shuffled birth components, coupled month/day", "timed mutable 235 vs203 p=.002; untimed Moon aspects p=.27; Mars-slow p≈.83 and Chiron families p≈.50–.87", "five declared families Bonferroni .01 but correlated tests and selection", "77 timed and 216 date-only male cases; this article is represented by two old IDs, count once", "Rodden-rated times 77; 216 noon imputed with Moon ±~6°"),
    row("SRC-0813AC1D0A13E0", ["Jan Ruis"], 2012, "The Birth Charts of Male Serial Killers: Evidence of Astrological Effects? (follow-up)", "Correlation 28(2), 8–27", "c20122802.pdf", 293, "DS-17023E74E89B", "retest mutable, Moon aspects, Neptune and search sign/house/sector omnibus", "serial-killer birth-chart distributions", "same ~6,000 ADB comparator and additional date/year simulations", "54/77 vs41 and 122/216 vs94 mutable indicators; untimed Moon aspect null, new signs p=.0002", "many new outcome-fitted tests; nonsignificant untimed Moon result", "Same 77+216 people as Ruis 2008; NOT independent replication", "77 timed and 216 noon-imputed date-only", "reanalysis_followup"),
    row("SRC-DDE4F1E896DDEC", ["Kyösti Tarvainen"], 2013, "Favourable Astrological Factors for Mathematicians", "Correlation 29(1), 39–51", "c20132901.pdf", 2759, "DS-243B52739478", "25 astrologer/author favorable factors, major aspects scanned then ±8° and sextile ±5°", "mathematician/technical-author membership", "1000 date/year shuffles and ±90-day temporal perturbations", "1.847 vs1.783 factors/person, p=.001 combined; 3-factor subset p=.08; no individual factor survives Bonferroni", "post outcome orb scanning; 99 award-winners nested in 1,849", "910 technical authors +1849 MacTutor, 99 subset of latter", "date only, chart noon GMT"),
    row("SRC-6E9960E2B91CEE", ["Kyösti Tarvainen"], 2014, "Effects of Venus/Saturn Aspects in Marriages", "Correlation 29(2), 7–14", "c20142902.pdf", 20892, "DS-45E578306732", "Venus–Saturn 0/60/90/120/180°, major ±7° sextile ±5°", "marriage occurrence proxy and ages at first recorded child", "100 shuffled family controls", "marriage frequency male +0.7% p=.5, female +0.5% p=.6; father age +92d p=.008", "marriage incidence fails; first child not wedding date", "Same Gauquelin hereditary couples reused 2016 and 2022", "historical timed family records"),
    row("SRC-0EB50F77399474", ["Kyösti Tarvainen"], 2015, "A Study of Major and Minor Aspects in Theologians’ Charts", "Correlation 30(1), 29–36", "c20153001.pdf", 6285, "DS-06DBDF652031", "11 prior Jupiter aspects widened to 25 selected aspects; 12 selected minor harmonics", "Finnish theologian membership", "1000 shuffled time/calendar controls", "prior 11 p=.035; selected 25 p=.003; selected 12 minors p=.01; several individual aspect/orb cases fail", "Jupiter/orb/minor family chosen after inspecting same data", "Own theologian cohort; mathematician comparison reuses 2013", "date-only/noon"),
    row("SRC-C333F5C1E0E0AD", ["Kyösti Tarvainen"], 2016, "The Moon’s Nodes in the Synastry of the Gauquelins’ Couples", "Correlation 30(2), 29–37", "c20163002.pdf", 20895, "DS-98318D8CAD", "7 classical planets at spouse mean North/South Node ±10°, stratify natal Node conjunctions", "marriage-couple synastry", "500 generated controls/couples from ±1-year windows; method-injection simulation", "husband NN 8318 vs8164 p=.05; SN 7973 vs8080 p=.12; wife NN 8083 vs8141 p=.70; four-family p=.07", "female and pooled primary contrasts fail; orbs selected on same cases", "Same Gauquelin hereditary-family dataset as 2014 and 2022", "timed family records; noon sensitivity analysis"),
    row("SRC-FD04109B827059", ["Kyösti Tarvainen"], 2017, "Planets Are Strong by Ordinary Astrology in Gauquelins’ Groups", "Correlation 31(1), 34–42", "c20173101.pdf", 23231, "DS-EA74ED29927F", "26 proposed group rulers scored by conjunction, angular houses, sign/house rulership", "15 Gauquelin occupation and other groups", "1000 separately shuffled dates, years, hours, places", "overall +0.8% p=.008; actors, aviators, politicians, murderers and multiple rulers negative", "Koch/Whole Sign tie; ruler and orb alternatives after result", "Gauquelin historical program; overlaps 1985/1988/2018/2021", "historic timed births"),
    row("SRC-0BD0B1C566B115", ["Kyösti Tarvainen"], 2018, "Chart Rulers Work in the Gauquelins’ Data", "Correlation 31(2), 67–74", "c20183102.pdf", 20394, "DS-883DFA23367C", "ASC-sign ruler or focal-house ruler in predetermined profession house, Koch houses", "10 Gauquelin profession groups", "1000 shuffled date/year/time/place groups", "pooled ASC-ruler p=.005, focal-house-ruler p=.003; only politicians individual p=.01, writers p=.50", "most group-specific tests fail; later proposed mapping substitutions", "Same Gauquelin cohort reanalysed 2021; overlaps 2017", "historic timed births"),
    row("SRC-3087A4AD9810B5", ["Kyösti Tarvainen"], 2018, "Dean’s Serial Correlation Method Doesn’t Work in Time Twin Studies", "Correlation 32(1), 75–79", "c20183201.pdf", 2100, "DS-FBDA897AF8EC", "synthetic Mercury-first-house ~2-hour pulse and injected +5 IQ points", "power of serial correlation vs t test", "100000 synthetic simulations", "mean p=.003 regular test versus mean p≈.48 serial correlation", "synthetic SD conflict in text (15 vs5); no actual subject replication", "Not an analysis of Dean's 2,101 real London births", "simulated times and simulated IQ", "methodological_simulation"),
    row("SRC-5B6E8914B4FF9F", ["Robert Currey"], 2021, "The New York Suicide Study: Reconsidered and Reversed", "Correlation 34(1), 31–57", "2021 Vol 34 01 c20213401.pdf", 311, "DS-61DA91385E5B", "ten planets/signs/Koch houses and 5 aspects; unaspected Saturn excludes 0/90/120/180 ±8°", "past suicide case–control status; never person-level risk", "311 birth-certificate matched controls; prior Press split", "Saturn unaspected 31 vs17 p=.001; all unaspected 244 vs228 p=.151; square p=.141 and trine p=.201", "post-null reanalysis and uncorrected correlated aspects/events", "Exact 311 NYC cases and 311 controls from Press study reused", "timed NYC birth certificates for ~14% of 2250 certified suicides", "reanalysis"),
    row("SRC-POST-TARVAINEN2021", ["Kyösti Tarvainen"], 2021, "Confirmation of Ptolemy’s 5-degree Rule for Koch and Equal Houses", "Correlation 34(1), 9–16", "2021 Vol 34 01 c20213401.pdf", 20394, "DS-POST-TARVAINEN2021", "profession-associated focal ruler shifted 0–10° across house cusp", "same Gauquelin group match", "1000 shuffled charts and compared house systems", "Koch original p=.005, fitted shift5° p≈4e-7; 1853 vs1670 shifted", "selected best shift on evaluated records", "Exactly reanalyses Tarvainen 2018 20,394 persons", "historic timed births", "reanalysis"),
    row("SRC-POST-TARVAINEN2022", ["Kyösti Tarvainen"], 2022, "On the Strength of Tight versus Wide and Applying versus Separating Aspects", "Correlation 35(1), 17–23", "2022 Vol 35 01 c20223501.pdf", 50828, "DS-POST-TARVAINEN2022", "continuous/tuned aspect orb and applying-vs-separating curves", "mathematician/theologian prevalence, Gauquelin parents' first-child ages", "controls reused from 2013/2014/2015; noon imputation", "tightness inconsistent in 3/4; wife applying 7° +44d vs separating 5° +76d", "same-cohort threshold optimization and sex reversal", "2759 mathematicians +6285 theologians + two paired views of ~20892 spouses; NOT 50828 independent births", "two date-only noon cohorts, historical timed family cohort", "multi_dataset_reanalysis"),
    row("SRC-POST-GODBOUTCORON2023", ["Vincent Godbout", "Vital Coron"], 2023, "Replication of the Adjusted Planetary Dominance Model: Testing an Independent Sample of 61 Biographies", "Correlation 36(1), 49–60", "2023 Vol 36 01 c20233601.pdf", 61, "DS-POST-GODBOUTCORON2023", "7 training-optimized weighted dominance features in fixed Mastro/semantic keyword pipeline; 3 rank × 3 tries", "biography-derived planetary semantic target", "30,000 permutations anchored to 189 training people", "rank≤2/2 tries 39/61 vs23.8 p≈3.17e-5; rank≤3/3 tries 47 vs43.8 p=.182", "nine rank/tries tests; pipeline/label leakage unknown; one table/prose conflict", "61 person-disjoint versus 189 training, but same authors/software/endpoints", "ADB Rodden AA/A, rounded xx:00 excluded", "person_disjoint_pipeline_reuse"),
    row("SRC-POST-GODBOUT2024", ["Vincent Godbout"], 2024, "Testing Twelve Models of Planetary Dominance", "Correlation 36(2), 33–48", "2024 Vol 36 02 c20243602.pdf", 250, "DS-POST-GODBOUT2024", "12 dominance schemes with multiple ranks/tries on semantic biography targets", "biography keyword identification", "matched-model permutations; all 12 on same persons", "best alternative Lenoble 76/250 vs51.6 p<6.75e-5; several models null", "model and rank multiplicity; no untouched third cohort", "189 training + exact same 61 prior replication; Astrotheme comparator N246", "historically timed public figures", "comparative_reanalysis"),
    row("SRC-POST-GODBOUTBRUN2026", ["Vincent Godbout", "Hubert Brun"], 2026, "Should the Tropical Zodiac Signs Be Inverted to Their Opposites in the Southern Hemisphere?", "Correlation 38(1), 39–56", "2026 Vol 38 01c20263801.pdf", 141, "DS-POST-GODBOUTBRUN2026", "180° ayanamsa reverses every planet/angle sign; Mastro combined sign-aspect/midpoint scores matched to named-person GPT-generated 150-word trait lists", "inversion wins over unmodified chart within person", "73 northern vs68 southern public figures; nominal 50/50 binomial", "south 48/68 vs north 26/73 p≈1.627e-5/h=.716; latitude trend null", "Table 1/4 score subtraction inconsistent; Fig6 June-Sun sign labels reversed; names/biographies known to LLM; unmatched cohorts", "73 northern Le Monde biographies reused from 2020 and 2023; 68 new southern ADB people", "Rodden AA/A/B; south selected for available ChatGPT biography"),
    row("SRC-POST-DAIGNO2026", ["Serge Daigno"], 2026, "Physical Violence and Mars Aspects to the Fastest Moving Planets", "Correlation 38(2), 13–28", "2026 Vol 38 02 c20263802.pdf", 620, "DS-POST-DAIGNO620", "MA conjunct/opposite MO/SO/ME/VE ±2°, 8 individual tests", "historical murderer/serial-killer ascertainment (research only)", "calendar-day ephemeris; shifted permutation supplementary", "French ME–MA conj21/105 vs772/7472 p=.00231; Wiki27/122 vs1329/12891 p=.00010; French final third p=.210", "event/person dependence, demographic controls, multiple subsets and date-only birth quality", "620 Gauquelin historical murderers plus 751 Wikidata serial killers; two cross-set duplicates removed", "French timed; Wikidata date-only/noon"),
    row("SRC-POST-GODBOUTCORON2023PARENT", ["Vincent Godbout", "Vital Coron"], 2023, "A Model for Planetary Dominance: Convincing Evidence from Biographical Analysis", "Correlation 35(2), 11–29", "2023 Vol 35 02 c20233502v2.pdf", 189, "DS-POST-GODBOUT-189", "42 scanned dominance factors; retain 18 then Excel Solver selects 7 weighted factors; Mastro semantic biography target", "selected planetary dominance agrees with biography keyword target", "in-sample 30,000 shuffles of 189 biographies", "in-sample exploratory significance only; no independent test in this article", "data-fitted weights and semantic-target derivation", "73 Le Monde portraits reused from Godbout 2020, plus116 new ADB; training for 2023 N61", "Rodden-rated well-timed historical public figures", "training_original"),
    row("SRC-POST-GODBOUTBRUN2024BOOKS", ["Vincent Godbout", "Hubert Brun"], 2024, "Validating the Tropical Zodiac?", "Correlation 37(1), 73–84", "2024 Vol 37 01 c20243701.pdf", 313368, "DS-POST-GODBOUTBRUN2024BOOKS", "sign-wise sales of German 1991–94 zodiac-paperback titles and 70 astrologer sign ratings", "books sold by zodiac title, NOT buyer's birth sign/personality", "expected birth distribution and 320k seasonal permutations", "sign omnibus r≈.055; four seasons p=.0522 null; hemisphere inversion not tested", "sales/demand and shared cultural stereotypes; post hoc contrasts", "Independent book sales sample; ancillary precursor, NOT a CF004 replication", "no buyer birth inputs; ecological sales aggregate", "ecological_adjacent"),
]

# Structured measurement and method notes supplement (and do not replace) the
# complete-original audit. Do not silently turn an unreported design choice into
# an exact reproducible mapping.
MEASUREMENT = {
    "SRC-9BD900BE058818": "Eysenck Personality Inventory extreme E/N scores",
    "SRC-36A24656EBF177": "Eysenck Personality Inventory groups; blinded chart/no-chart judgments",
    "SRC-21918CDBF05EE1": "partner's rank/identification of relationship description among five",
    "SRC-41C1A14D8EDB9B": "historical marriage-couple interchart contact frequency",
    "SRC-C5D64810AF636C": "biographical character-trait mentions; repeated mentions per person",
    "SRC-DDE4F1E896DDEC": "occupational bibliographic lists; published mathematician/technical-author status",
    "SRC-6E9960E2B91CEE": "age at first recorded child as a proxy, NOT marriage date",
    "SRC-0EB50F77399474": "theologian occupational list, birth dates imputed to noon",
    "SRC-C333F5C1E0E0AD": "historic Gauquelin couple chart records",
    "SRC-3087A4AD9810B5": "synthetically injected IQ scores and Mercury-window birth times; not real participant outcomes",
    "SRC-5B6E8914B4FF9F": "historical suicide certificate case/control status; not individual prediction",
    "SRC-POST-TARVAINEN2022": "reused occupational lists and parental first-child ages, with paired spouses",
    "SRC-POST-GODBOUTCORON2023PARENT": "Mastro biography-keyword target; seven weighted factors fitted to 189 biographies",
    "SRC-POST-GODBOUTCORON2023": "Mastro semantic biography-keyword target; rank/tries nine-cell grid",
    "SRC-POST-GODBOUT2024": "same semantic biography targets for 189 training plus 61 prior replication people",
    "SRC-POST-GODBOUTBRUN2026": "named-person ChatGPT ~150-word profiles; exact Mastro dictionary matches, NOT measured traits",
    "SRC-POST-GODBOUTBRUN2024BOOKS": "sales of zodiac-labeled paperbacks, NOT buyers' natal signs or personality",
    "SRC-POST-DAIGNO2026": "historical case-group selection; aspect events per person, not independent persons",
}

METHODS = {
    "SRC-9BD900BE058818": "many factor-level observed-versus-chance tests and discriminant analysis, with internal split samples; control: opposing E/N groups",
    "SRC-6B50EC5034D723": "observed-minus-expected aspect-window departures by occupational group; five planetary pairs and five aspects; sector comparison descriptive",
    "SRC-36A24656EBF177": "blinded chart-reader versus no-chart accuracy and chance contrasts; dependent rater judgments",
    "SRC-97B1D36F3A34B6": "165 aspect-window significance comparisons against equal-duration neighbors and ±266-day shifted controls; repeated windows dependent",
    "SRC-21918CDBF05EE1": "ranking/recognition comparison to five description options; reported aggregate p<.01, partner responses clustered in 54 couples",
    "SRC-FCBB0829EE54D3": "stratified G-sector prevalence by rounded/non-rounded birth time and era/planet; duplicate planet-level records",
    "SRC-41C1A14D8EDB9B": "historical interchart contact-frequency reanalysis; selected minimum-p contact corrected for 50 tests",
    "SRC-C5D64810AF636C": "compare trait-mention versus independent-person expected sector counts; harmonic amplitude threshold search",
    "SRC-CB1D87C64AF1FA": "338 reported chi-square tests, simulations for ascendant/control frequencies and separate Gauquelin 630-parent check",
    "SRC-7C6A67F3AEE43C": "five named hypothesis families, author Bonferroni .01; AstroDatabank matched and shuffled controls, multiple nested comparisons",
    "SRC-0813AC1D0A13E0": "same 2008 case/control material reanalysed with additional simulations and sign/house/sector omnibus tests",
    "SRC-DDE4F1E896DDEC": "25 factor tests and combined count contrasts against date/year shuffle and ±90-day calendar controls; author reports p-values",
    "SRC-6E9960E2B91CEE": "five Venus–Saturn aspect comparisons using shuffled family controls; subgroup age differences and reported p-values",
    "SRC-0EB50F77399474": "expanded 11→25 Jupiter aspects and 12 minor harmonics; shuffled time/calendar controls with same-data feature/orb selection",
    "SRC-C333F5C1E0E0AD": "four spouse/Node contrasts and natal-Node strata against generated fake couples; method-injection simulation is not a replication",
    "SRC-FD04109B827059": "occupational ruler-score observed-minus-shuffle contrasts using 1,000 separate date/year/hour/place shuffles",
    "SRC-0BD0B1C566B115": "combined and ten group-specific ruler counts versus 1,000 shuffled controls; some groups reverse",
    "SRC-3087A4AD9810B5": "100,000 synthetic Monte Carlo datasets comparing adjacent-birth serial correlation to two-group test under one injected +5 IQ pulse",
    "SRC-5B6E8914B4FF9F": "case–control count comparisons, selected planet/aspect/element strata; counts of aspect events violate person-level independence",
    "SRC-POST-TARVAINEN2021": "in-sample 0–10° house-cusp sweep with multiple house systems and shuffled control charts; best shift is selected",
    "SRC-POST-TARVAINEN2022": "four reused sex/cohort applications of outcome-inspected tightness/applying curves; matched original controls, no independent four-way replication",
    "SRC-POST-GODBOUTCORON2023": "nine rank-by-tries binomial-style observed/expected tests, 30,000 training-based shuffles; semantic pipeline not rerun under null",
    "SRC-POST-GODBOUT2024": "twelve model/rank/tries comparisons on 189+61 reused biographies; matched-model shuffle controls",
    "SRC-POST-GODBOUTBRUN2026": "paired within-person original/inverted scores then one-sided N/S win-rate z test (48/68 vs26/73); separate binomials and latitude trend checks",
    "SRC-POST-DAIGNO2026": "eight one-sided aspect tests with Bonferroni .00625 and calendar-day ephemeris controls; correlated event counts and birth-third strata",
    "SRC-POST-GODBOUTCORON2023PARENT": "in-sample 42→18→7 indicator/weight selection with Excel Solver, training-sample permutations, no held-out test in this original",
    "SRC-POST-GODBOUTBRUN2024BOOKS": "German zodiac-title sales versus expected birth-season counts; sign and season contrasts, permutations and astrologer-ranking correlation",
}
assert set(METHODS) == {a["id"] for a in ARTICLES}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))


def citation(a: dict) -> str:
    punctuation = "" if a["title"].endswith((".", "?", "!")) else "."
    return f"{', '.join(a['authors'])}. {a['year']}. {a['title']}{punctuation} {a['issue']}"


def merge() -> None:
    audit_text = AUDIT.read_text()
    assert len(ARTICLES) == 27 and len({(a['title'], a['issue']) for a in ARTICLES}) == 27
    existing = [a for a in ARTICLES if not a['id'].endswith(("PARENT", "2024BOOKS"))]
    assert len(existing) == 25 and len({a['id'] for a in existing}) == 25
    historical_gap = (ROOT / "notes/empirical_astrology/fulltexts/CORRELATION_ACCESS_GAP.md").read_text()
    gap_ids = re.findall(r"^\| `(SRC-[^`]+)`", historical_gap, flags=re.MULTILINE)
    assert len(gap_ids) == 25 and set(gap_ids) == {a["id"] for a in existing}
    audit_paragraphs = {}
    for line in audit_text.splitlines():
        match = re.match(r"^(\d+)\. \*\*(.+)$", line)
        if match:
            audit_paragraphs[int(match.group(1))] = match.group(2)
    assert set(audit_paragraphs) == set(range(1, 26))
    extraction_path = EVIDENCE / "fulltexts_v2/primary_feature_extractions.jsonl"
    original_extractions = [x for x in read_jsonl(extraction_path) if not x["extraction_id"].startswith("PFE-ARCH-")]
    new_extractions = []
    for index, a in enumerate(ARTICLES, 1):
        risk = audit_paragraphs.get(index) if index <= 25 else a["failure"]
        new_extractions.append({
            "source_document_id": a["id"], "dataset_id": a["ds"],
            "study_family_id": "SF-CORRELATION-ARCHIVE-REVIEW", "citation": citation(a),
            "sample_n": a["n"], "population": a["outcome"],
            "birth_data_source_and_precision": a["birth"], "inclusion_exclusion_rules": a["lineage"],
            "exact_predictor_family": a["feature"], "exact_predictor_definition": a["feature"],
            "zodiac_reference_frame": ("tropical original versus 180° inverted all-planet/angle signs" if a["id"] == "SRC-POST-GODBOUTBRUN2026"
                else "source-dependent, not harmonized across studies; see complete original"),
            "house_system": ("houses excluded; angle aspects retained" if a["id"] == "SRC-POST-GODBOUTBRUN2026"
                else "source-dependent; any exact named house system is recorded in the complete-original audit"),
            "aspect_definition": a["feature"] if any(w in a["feature"].lower() for w in ("aspect", "conjunct", "orb")) else None,
            "orb_definition": a["feature"] if any(x in a["feature"].lower() for x in ("orb", "±")) else None,
            "applying_separating_handling": a["feature"] if "applying" in a["feature"].lower() else None,
            "angularity_sector_definition": a["feature"] if any(w in a["feature"].lower() for w in ("angular", "sector", "cusp")) else None,
            "exact_outcome": a["outcome"],
            "measurement_instrument": MEASUREMENT.get(a["id"], "See original outcome definition and complete-source audit; no new participant measure inferred"),
            "statistical_method": METHODS[a["id"]], "control_construction": a["controls"],
            "multiplicity_handling": a["failure"], "effect_size": a["result"],
            "uncertainty_ci": "not jointly published for all tested cells; consult complete article and audit",
            "p_value_bayes_factor": a["result"], "raw_counts_sufficient_statistics": a["result"],
            "hypothesis_status": a["role"],
            "original_author_conclusion": "see primary article; the audit records successes AND failures",
            "replication_reanalysis_relation": a["lineage"],
            "methodological_risk_notes": risk, "algorithmic_candidate_or_negative_constraint": "Evidence only; PRO scientific gate required; no model change",
            "independent_of_earlier_datasets": (True if a["id"] == "SRC-POST-GODBOUTCORON2023" else
                False if any(w in a["lineage"].lower() for w in ("same", "reuse", "reanalysis", "overlap", "parent", "training")) else None),
            "pipeline_independent_of_earlier_studies": False if a["id"] in
                {"SRC-POST-GODBOUTCORON2023", "SRC-POST-GODBOUT2024", "SRC-POST-GODBOUTBRUN2026"} else None,
            "archive_full_issue_sha256": FILES[a["file"]],
            "archive_audit_path": str(AUDIT.relative_to(ROOT)),
            "extraction_id": f"PFE-ARCH-{index:02d}",
        })
    daigno_wiki = dict(next(r for r in new_extractions if r["source_document_id"] == "SRC-POST-DAIGNO2026"))
    daigno_wiki.update(dataset_id="DS-POST-DAIGNO751", sample_n=751,
        birth_data_source_and_precision="Wikidata serial killers: dates only, chart noon; within-source birth-record accuracy unverified",
        raw_counts_sufficient_statistics="ME–MA conjunction 27/122 vs1329/12891, p=.00010; pooled aspects 101/630 vs6241/64496, p≈4.3e-8; first birth third ME conjunction p=.06739 fails",
        effect_size="serial killer event-based pooled h=.191; event counts within person correlated",
        replication_reanalysis_relation="Person sources mostly separate from 620 Gauquelin French murderers; two cross-cohort duplicate persons removed; 751 Wikidata cases are date-only",
        extraction_id="PFE-ARCH-25B")
    new_extractions.append(daigno_wiki)
    write_jsonl(extraction_path, original_extractions + new_extractions)

    manifest_path = EVIDENCE / "fulltexts_v2/fulltext_manifest.jsonl"
    manifest = read_jsonl(manifest_path)
    by_id = {a["id"]: a for a in ARTICLES}
    for r in manifest:
        a = by_id.get(r["source_document_id"])
        if a is None:
            continue
        r.update(citation=citation(a), full_text_status="full_text_retrieved_and_read",
                 access_url="https://www.nvwoa.nl/txt/ruisen.pdf" if a["id"] == "SRC-7C6A67F3AEE43C" else None,
                 file_or_source_provenance=("complete author-hosted copy; " if a["id"] == "SRC-7C6A67F3AEE43C" else "owner-provided authenticated complete issue PDF; ") + ARCHIVE + a["file"],
                 pages_or_sections_actually_inspected=a["issue"] + "; relevant abstract, methods, results/tables and discussion inspected from complete PDF; older OCR ambiguities flagged in audit",
                 missing_material_note=None, local_file_committed=False,
                 local_read_copy_sha256=FILES[a["file"]], accessed_on="2026-09-28",
                 archive_audit_path=str(AUDIT.relative_to(ROOT)))
        r["retrieval_attempts"] = list(dict.fromkeys(r.get("retrieval_attempts", []) + ["owner_authenticated_archive", "complete_pdf_inspection"]))
        if a["id"] == "SRC-0813AC1D0A13E0":
            r["archive_additional_article"] = "Ruis 2008, Correlation 25(2), 7–44; separate 2012 reanalysis shares the 77+216 people"
            r["archive_additional_article_sha256"] = FILES["Ruis 2008 Correlation 25.2 author copy.pdf"]
    for a in ARTICLES[-2:]:
        if a["id"] not in {r["source_document_id"] for r in manifest}:
            manifest.append({"source_document_id": a["id"], "citation": citation(a), "priority": "A", "access_url": None,
                "full_text_status": "full_text_retrieved_and_read", "file_or_source_provenance": "owner-provided authenticated complete issue PDF; " + ARCHIVE + a["file"],
                "document_role": [a["role"]], "pages_or_sections_actually_inspected": a["issue"] + "; complete article",
                "missing_material_note": None, "retrieval_attempts": ["owner_authenticated_archive", "complete_pdf_inspection"],
                "candidate_urls": [], "local_file_committed": False, "local_read_copy_sha256": FILES[a["file"]],
                "accessed_on": "2026-09-28", "archive_audit_path": str(AUDIT.relative_to(ROOT))})
    resolved = [r for r in manifest if r["source_document_id"] in set(gap_ids)]
    assert len(resolved) == 25 and all(r["full_text_status"] == "full_text_retrieved_and_read" for r in resolved)
    write_jsonl(manifest_path, manifest)

    sources_path = EVIDENCE / "master_v2/source_registry.jsonl"
    sources = read_jsonl(sources_path)
    for s in sources:
        a = by_id.get(s["source_document_id"])
        if a is None:
            continue
        c = s["canonical_citation"]
        c.update(authors=a["authors"], year=a["year"], title=a["title"], source_or_journal=a["issue"],
                 volume_issue_pages_raw=a["issue"], citation_display=citation(a))
        c["urls"] = ["https://www.nvwoa.nl/txt/ruisen.pdf"] if a["id"] == "SRC-7C6A67F3AEE43C" else []
        c["doi"] = None
        s["archive_full_text_verified"] = True
        s["archive_full_issue_sha256"] = FILES[a["file"]]
        s["archive_citation_correction_note"] = "Verified against complete issue PDF; previous summary-derived metadata retained in git history."
        if a["id"] == "SRC-0813AC1D0A13E0":
            s["archive_article_components"] = ["Correlation 25(2), 2008, 7–44 (same original as SRC-7C6A67F3AEE43C)", a["issue"]]
        if a["id"] == "SRC-POST-GODBOUTBRUN2026":
            s["identity_conflict"] = False
            s["identity_conflict_note"] = "Direct 38(1) complete original located; the 37(1) 2024 zodiac-sales paper is a separate article."
        s["current_screen_status"] = "complete_original_source_read"
    for a in ARTICLES[-2:]:
        if a["id"] not in {s["source_document_id"] for s in sources}:
            sources.append({"source_document_id": a["id"], "canonical_citation": {"authors": a["authors"], "year": a["year"], "title": a["title"], "source_or_journal": a["issue"], "volume_issue_pages_raw": a["issue"], "doi": None, "urls": [], "citation_display": citation(a)},
                "source_type": "complete journal article", "empirical_source_document": True,
                "commentary_or_review_only": False, "document_roles": [a["role"]],
                "study_family_id": "SF-CORRELATION-ARCHIVE-REVIEW", "study_family_label": "archive_parent_or_adjacent",
                "feature_record_count": 1, "original_record_ids": [], "worker_ids": [], "ua_section_ids": [], "ua_book_pages": [],
                "chapter7_coverage": False, "chapter8_coverage": False, "chapter7_chapter8_duplicate_coverage": False,
                "canonicalization_method": "complete issue PDF and checked citation", "identity_conflict": False,
                "identity_conflict_note": None, "full_text_priority": "A", "information_value_score": 180,
                "information_value_reasons": ["direct predecessor or comparator; dataset-lineage audit"],
                "wave1_full_text_statuses": [], "wave1_primary_urls": [], "archive_full_text_verified": True,
                "archive_full_issue_sha256": FILES[a["file"]]})
    write_jsonl(sources_path, sources)

    datasets_path = EVIDENCE / "master_v2/dataset_registry.jsonl"
    datasets = read_jsonl(datasets_path)
    groups = {
        "SRC-9BD900BE058818": "dean_extreme_en_1198", "SRC-36A24656EBF177": "dean_extreme_en_1198",
        "SRC-6B50EC5034D723": "gauquelin_profession_partial_overlap", "SRC-97B1D36F3A34B6": "gauquelin_profession_partial_overlap",
        "SRC-FCBB0829EE54D3": "gauquelin_profession_partial_overlap", "SRC-C5D64810AF636C": "gauquelin_profession_partial_overlap",
        "SRC-FD04109B827059": "gauquelin_profession_partial_overlap", "SRC-0BD0B1C566B115": "gauquelin_profession_20394_exact",
        "SRC-POST-TARVAINEN2021": "gauquelin_profession_20394_exact", "SRC-6E9960E2B91CEE": "gauquelin_heredity_couples_20895",
        "SRC-C333F5C1E0E0AD": "gauquelin_heredity_couples_20895", "SRC-POST-TARVAINEN2022": "mixed_reuse_math_theology_heredity",
        "SRC-7C6A67F3AEE43C": "ruis_serial_77_plus_216", "SRC-0813AC1D0A13E0": "ruis_serial_77_plus_216",
        "SRC-DDE4F1E896DDEC": "tarvainen_mathematicians_2759", "SRC-0EB50F77399474": "tarvainen_theologians_6285",
        "SRC-POST-GODBOUTCORON2023": "godbout_pipeline_new_61_people", "SRC-POST-GODBOUT2024": "godbout_189_plus_61_reuse",
        "SRC-POST-GODBOUTBRUN2026": "godbout_73_north_reused_plus_68_new_south", "SRC-5B6E8914B4FF9F": "press_nyc_suicide_311_reanalysis",
    }
    for ds in datasets:
        links = {groups[x] for x in ds.get("source_document_ids", []) if x in groups}
        if links:
            ds["archive_cohort_lineage_groups"] = sorted(links)
            ds["archive_lineage_review_path"] = str(AUDIT.relative_to(ROOT))
            if any(x in ds.get("source_document_ids", []) for x in ("SRC-POST-GODBOUTBRUN2026", "SRC-POST-GODBOUT2024")):
                ds["independence_note"] = "See archive audit: known reuse of people/pipeline; prior independent_dataset_unit was insufficient for this exact claim."
        if "SRC-POST-GODBOUTBRUN2026" in ds.get("source_document_ids", []):
            ds["canonical_dataset_label"] = "68 southern ADB public figures and 73 reused northern Le Monde portraits; GPT-named biographies"
            ds["sample_n_values"] = ["141", "68 south", "73 north"]
            ds["population_values"] = ["named public figures with biography coverage"]
            ds["birth_data_sources"] = ["AstroDatabank south", "reused Le Monde north"]
            ds["birth_time_quality_values"] = ["Rodden AA/A/B"]
            ds["identity_certainty"] = "high_source_verified_partial_cohort_reuse"
            ds["likely_reused"] = True
            ds["independent_dataset_unit"] = False
            ds["feature_record_count"] = 1
        if "SRC-41C1A14D8EDB9B" in ds.get("source_document_ids", []):
            ds["canonical_dataset_label"] = "Jung's three historical marriage sets: 180+220+83 couples (reanalysis)"
            ds["sample_n_values"] = ["483", "180", "220", "83"]
            ds["population_values"] = ["Jung married pairs; cross-pair controls for first set"]
            ds["independent_dataset_unit"] = False
            ds["likely_reused"] = True
            ds["identity_certainty"] = "high_source_verified_reanalysis"
            ds["independence_note"] = "This source is Dean's reanalysis of Jung; the old '19 studies excluding Jung' label misidentified the linked article."
        if "SRC-6B50EC5034D723" in ds.get("source_document_ids", []) and "parent-child" in ds.get("canonical_dataset_label", "").lower():
            ds["archive_source_dataset_link_mismatch"] = "The linked 5(1), 25–35 original analyses 15,334 eminent professionals' aspects, not these parent–child comparison samples; preserve historical row but do not count it as direct study data."
            ds["identity_certainty"] = "conflicting_wave1_link_source_checked"
            ds["independent_dataset_unit"] = False
        if any(x in ds.get("source_document_ids", []) for x in ("SRC-POST-TARVAINEN2021", "SRC-POST-TARVAINEN2022", "SRC-POST-GODBOUT2024", "SRC-0813AC1D0A13E0")):
            ds["likely_reused"] = True
            ds["independent_dataset_unit"] = False
            ds["independence_note"] = "Source-verified reanalysis/composite of earlier persons; see post-archive cohort audit."
        if "SRC-POST-TARVAINEN2022" in ds.get("source_document_ids", []):
            ds["canonical_dataset_label"] = "Repeated mathematicians N2759, theologians N6285, paired Gauquelin fathers/wives ~20892 each"
            ds["sample_n_values"] = ["2759", "6285", "20892 paired fathers", "20892 paired mothers"]
        if "SRC-POST-GODBOUT2024" in ds.get("source_document_ids", []):
            ds["canonical_dataset_label"] = "2023 dominance training N189 plus exact 2023 person-disjoint replication N61"
            ds["sample_n_values"] = ["250", "189 reused training", "61 reused replication"]
        if "SRC-0813AC1D0A13E0" in ds.get("source_document_ids", []):
            ds["archive_reused_with_source_document_ids"] = ["SRC-7C6A67F3AEE43C"]
    for a in ARTICLES[-2:]:
        if a["ds"] not in {d["dataset_id"] for d in datasets}:
            datasets.append({"dataset_id": a["ds"], "canonical_dataset_label": a["lineage"],
                "identity_certainty": "medium", "source_document_ids": [a["id"]], "original_record_ids": [],
                "study_family_ids": ["SF-CORRELATION-ARCHIVE-REVIEW"], "sample_n_values": [str(a["n"])],
                "population_values": [a["outcome"]], "birth_data_sources": [a["birth"]],
                "birth_time_quality_values": [a["birth"]], "source_document_count": 1, "feature_record_count": 1,
                "likely_reused": a["id"].endswith("PARENT"), "independent_dataset_unit": False,
                "independence_note": a["lineage"], "archive_cohort_lineage_groups": ["godbout_189_training"] if a["id"].endswith("PARENT") else ["german_zodiac_book_sales_ecological"]})
    write_jsonl(datasets_path, datasets)

    candidates_path = EVIDENCE / "master_v2/candidate_feature_registry.jsonl"
    candidates = read_jsonl(candidates_path)
    notes = {
        "CF-001": "No direct Correlation replication of the exact karaka-kendra claim located in these 25 articles.",
        "CF-002": "2022 complete article reuses 2013 mathematics, 2015 theology and paired 2014 hereditary couples; 4-case tightness fails consistency, female applying example reverses.",
        "CF-003": "2023 parent N189 fits weights; person-disjoint N61 replication inherits semantic pipeline and nine rank/try settings, one p=.182 null; 2024 N250 combines both prior groups rather than adding a third.",
        "CF-004": "Direct 38(1) N141 original: 48/68 south vs26/73 north inverted-chart wins, but reused 73 northern subjects, name-conditioned GPT biographies, absent end-to-end null and impossible-to-reconcile printed subtraction/hemisphere labels.",
        "CF-005": "Direct 38(2) aspect event counts include corrected individual ME-MA conjunction in two sources, several failed birth thirds, date-only Wikidata and mismatched calendar-day controls; never forensic/person-level.",
        "CF-006": "Historical Gauquelin cohorts repeatedly reanalysed: 1985 aspect null, 1988 aspect-window null, 1995 timing paradox, 1997 trait-expectancy critique, 2017/18/21 mapping reuses. Not six independent cohorts.",
        "CF-007": "2013/15 orb scans, 2014/16 paired families, 2021 post-outcome cusp shift and 2022 tightness inconsistency; 1988 negative aspect test directly available. No same-hospital held-out trait replication established by these articles.",
        "CF-008": "No directly responsive Correlation original among the 25; preserve prior missing exact mapping and validation concern.",
    }
    new_links = {"CF-002": ["SRC-POST-TARVAINEN2022"], "CF-003": ["SRC-POST-GODBOUTCORON2023PARENT", "SRC-POST-GODBOUT2024"],
                 "CF-004": ["SRC-POST-GODBOUTBRUN2026", "SRC-POST-GODBOUTBRUN2024BOOKS"],
                 "CF-005": ["SRC-POST-DAIGNO2026", "SRC-7C6A67F3AEE43C"],
                 "CF-006": ["SRC-6B50EC5034D723", "SRC-FCBB0829EE54D3", "SRC-FD04109B827059", "SRC-0BD0B1C566B115", "SRC-POST-TARVAINEN2021"],
                 "CF-007": ["SRC-97B1D36F3A34B6", "SRC-DDE4F1E896DDEC", "SRC-0EB50F77399474", "SRC-POST-TARVAINEN2022", "SRC-3087A4AD9810B5"]}
    for c in candidates:
        key = c["candidate_feature_id"]
        c["post_archive_evidence_note"] = notes[key]
        c["post_archive_gate_status"] = "PRO_ADJUDICATION_REQUIRED_NO_MODEL_REVISION_BY_EVIDENCE_WORKER"
        c["post_archive_source_audit_path"] = str(AUDIT.relative_to(ROOT))
        c["evidence_source_ids"] = list(dict.fromkeys(c["evidence_source_ids"] + new_links.get(key, [])))
        if key == "CF-004":
            c["replication_status"] = "complete single direct 2026 study, no person-independent validation; 73 northern biographies reused from 2020; exact table arithmetic/labels conflict"
            c["effect_summary"] = "direct 38(1) reports 48/68 southern vs26/73 northern inverted-chart wins; z4.155, p≈1.627e-5, h=.716; printed score examples do not reproduce"
            c["definition_risk"] = "full Mastro 2885-word corpus, GPT 150-noun outputs/prompt/model version, exact lexical scoring, ambiguous table labels and end-to-end permutation must be frozen and corrected before outcomes"
            c["confounds"] = list(dict.fromkeys(c["confounds"] + ["73 reused northern biographies", "named-person LLM-label leakage", "unmatched north/south ascertainment", "printed table arithmetic contradictions"]))
        if key == "CF-003":
            c["replication_status"] = "N61 new people verified; nine tested rank/tries cells, same semantic pipeline and authors; 2024 N250 reused"
            c["definition_risk"] = "7 weighted factors documented in 35(2) original; Mastro/biography semantic target, nine settings and full end-to-end null remain necessary"
        if key == "CF-002":
            c["replication_status"] = "direct original audited: 4 reported applications are reused prior cohorts, female direction and three tightness comparisons do not consistently confirm"
    write_jsonl(candidates_path, candidates)

    negatives_path = EVIDENCE / "master_v2/negative_constraint_registry.jsonl"
    negatives = read_jsonl(negatives_path)
    evidence = {
        "NC-004": ["SRC-3087A4AD9810B5"], "NC-005": ["SRC-6B50EC5034D723", "SRC-97B1D36F3A34B6", "SRC-POST-TARVAINEN2022"],
        "NC-007": ["SRC-CB1D87C64AF1FA", "SRC-41C1A14D8EDB9B", "SRC-POST-GODBOUTCORON2023"],
        "NC-008": ["SRC-0813AC1D0A13E0", "SRC-POST-TARVAINEN2021", "SRC-POST-GODBOUT2024"],
        "NC-009": ["SRC-FCBB0829EE54D3", "SRC-POST-DAIGNO2026"],
        "NC-011": ["SRC-C333F5C1E0E0AD", "SRC-POST-DAIGNO2026"],
        "NC-012": ["SRC-5B6E8914B4FF9F", "SRC-POST-DAIGNO2026"],
        "NC-013": ["SRC-3087A4AD9810B5"],
        "NC-016": ["SRC-POST-GODBOUTCORON2023", "SRC-POST-GODBOUTBRUN2026"],
        "NC-017": ["SRC-POST-TARVAINEN2021", "SRC-POST-TARVAINEN2022"],
        "NC-018": ["SRC-POST-GODBOUTCORON2023PARENT", "SRC-POST-GODBOUTCORON2023", "SRC-POST-GODBOUT2024"],
        "NC-019": ["SRC-CB1D87C64AF1FA", "SRC-POST-TARVAINEN2022", "SRC-POST-DAIGNO2026"],
    }
    for neg in negatives:
        neg["evidence_source_ids"] = list(dict.fromkeys(neg["evidence_source_ids"] + evidence.get(neg["constraint_id"], [])))
        if neg["constraint_id"] in evidence:
            neg["post_archive_audit_path"] = str(AUDIT.relative_to(ROOT))
    write_jsonl(negatives_path, negatives)

    counts = {"manifest": len(manifest), "extractions": len(original_extractions + new_extractions), "sources": len(sources), "datasets": len(datasets), "candidates": len(candidates), "negative_constraints": len(negatives)}
    packet = {"schema_version": "1.0.0", "packet_type": "empirical_astrology_post_paid_correlation_archive_pro_handoff",
        "generated_on": "2026-09-28", "role_boundary": "Source retrieval, exact citation correction, results/failures extraction and cohort accounting. Scientific adjudication expressly reserved for Pro.",
        "frozen_prior_decision_branch": "worker/empirical-astrology-pro-decisions",
        "frozen_wave3_pro_commit": "ccdeaa9d563e243bfce2349b10d6c932e7f3bc57",
        "current_prior_pro_decision_paths": ["reference/empirical_astrology/literature_model_v1b_decision.json", "notes/empirical_astrology/master_v2/PRO_DECISION_WAVE4.md"],
        "archive_article_count": 25, "gap_source_record_count": 25, "additional_parent_and_adjacent_article_count": 2,
        "complete_article_pdfs_committed": 0, "full_article_audit_path": str(AUDIT.relative_to(ROOT)),
        "full_article_audit_sha256": hashlib.sha256(audit_text.encode()).hexdigest(),
        "full_text_issue_sha256": FILES, "counts": counts,
        "article_extractions": [{"source_document_id": a["id"], "citation": citation(a), "issue_pdf": a["file"], "sha256": FILES[a["file"]],
                                 "sample_n": [620, 751] if a["id"] == "SRC-POST-DAIGNO2026" else a["n"], "cohort": a["lineage"], "feature": a["feature"], "control": a["controls"],
                                 "observed_and_failed_results": a["result"] + "; " + a["failure"]} for a in ARTICLES],
        "candidate_family_delta": notes,
        "critical_corrections": ["CF004 direct 38(1) 2026 article found and distinct from 37(1) 2024 book-sales precursor",
            "CF004 reported effect is non-reproducible from printed Table 1/4 score examples; Figure 6 has contradictory sign labels",
            "CF003 61-person sample is person-disjoint but reuses semantic target, authors and optimized model; 2024 N250 reuses all 189+61",
            "CF002 N50828 sums reused date-only cohorts and paired husbands/wives, tightness inconsistency",
            "CF006 repeated historic Gauquelin cohorts, negative aspect tests and timing precision paradox",
            "Ruis 2012 is reanalysis of 77+216, not new serial killers; Brady Gauquelin nodding comparison fails",
            "Tarvainen 2018 time-twin critique is simulation, not real outcome reanalysis"],
        "pro_questions": ["adjudicate robustness, ablations, complete-pipeline nulls, leakage, person/family/cohort dependence, multiplicity, reuse and contradictions",
            "decide whether any versioned revision is justified without fitting to owner-known outcomes",
            "freeze exact mappings before outcomes and require independent held-out replication; report all failures",
            "preserve same-hospital near-time primary theory-neutral and aspect/orb tightness plus angularity secondary unless Pro explicitly versions the decision"],
        "pro_decision_written_here": False, "prospective_recruitment_or_outcome_collection": False}
    packet_path = ROOT / "reference/empirical_astrology/pro_reasoning_packet_post_correlation_archive.json"
    packet_path.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(counts, sort_keys=True))


if __name__ == "__main__":
    merge()
