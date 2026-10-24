"""Traceable, source-attested historical EVENT-claim candidates (NOT predictions).

Evidence: FIRST-EDITION William Lilly, Christian Astrology (1647),
printed pp654,657,659,661,669,670,683,684, visually checked in
independent Wellcome photos during 2026-10-24 research. Page images and
sha256 receipts accompany the packet.

Every source excerpt is a short exact local phrase and NOT a guarantee.
Historical claim scope, astronomical contact, interpretive preconditions,
and proposed modern test proxy are different fields.

No actual participant, natal event history, human survey answer or hidden
scoring key is consulted here. No time-key / birth-to-event age chosen.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

PHOTO_SHA256 = {
    654: "1c7366889c7669b1a05970bac529812333ad75e61e1fb1c1c2fc012c5cc159d3",
    657: "238d772975b36a9d57085199434bfda910250cf466d6e127538d5287fb51881a",
    659: "556ff2d970a59d132e9afcb459cedb37a4882ddf3cecc4cf22976e9f94fd76f5",
    661: "407d9b9cf0b9d9c6f20e14fab144a63c8a9dcb5e0eeadff04174b2d644d40d87",
    669: "1d2c95ce9025e2a496901d5f58de75453863c09eba5aa7ecad9574d885bc2772",
    670: "54ea8ddd29c1fd3f8dc1d0f0f5df787764b453604dfbbf7aaad03a6c5016f2f9",
    683: "f6227c352be2b40b71f103af9085fddb83c3bced3da87b801503e40aadbb61fc",
    684: "b30411f6c0cbf6ea1aafb67b80d6efd0fec81930cd28182130f90267659cc348",
}

# A source quotation is neither an empirical label nor a scoring predicate.
COMMON_SOURCE_CONDITIONS = [
    {
        "ref": "Lilly 1647 printed p654, Chapter CLVII",
        "historical_claim": (
            "Planets have their own general significations, but house "
            "placement and natal lordship can change the specific topic."
        ),
        "requirements_not_yet_fully_implemented": [
            "natal house rulership",
            "source-specific allowed significators",
        ],
    },
    {
        "ref": "Lilly 1647 printed p654, Chapter CLVII",
        "historical_claim": (
            "Power, weakness, natal essential dignity and angularity "
            "affect the magnitude and manifestation of directions."
        ),
        "requirements_not_yet_fully_implemented": [
            "essential dignities",
            "natal angularity and debility",
            "profections and revolution context where source requires",
        ],
    },
]


def _source(pages: tuple[int, ...], excerpt: str) -> dict[str, Any]:
    return {
        "author": "William Lilly",
        "book": "Christian Astrology, Book III",
        "first_edition": 1647,
        "original_photo_repository": "Wellcome Collection, work s7z7c46y",
        "iiif_manifest": "https://iiif.wellcomecollection.org/presentation/v2/b30338724",
        "printed_pages": list(pages),
        "zero_based_canvas_indices": [page + 34 for page in pages],
        "photos": [
            {
                "path": ("source_page_images/lilly_1647_printed_" + str(page) + ".jpg"),
                "sha256": PHOTO_SHA256[page],
            }
            for page in pages
        ],
        "verbatim_short_original_excerpt": excerpt,
        "excerpt_status": "checked_directly_in_1647_photo",
    }


def _claim(
    claim_id: str,
    label: str,
    source: dict[str, Any],
    historical_paraphrase: str,
    promissor: str,
    significator: str,
    construction: str,
    aspects: tuple[str, ...],
    proposed_event: str,
    observer_definition: str,
    required_historical_conditions: tuple[str, ...],
    modern_eligibility_proposal: str,
    *,
    outcome_group: str,
    unresolved_source_disjunction: bool = False,
) -> dict[str, Any]:
    return {
        "claim_id": claim_id,
        "label": label,
        "source": source,
        "historical_claim_paraphrase": historical_paraphrase,
        "historical_conditions": list(required_historical_conditions),
        "astronomical_proxy": {
            "moving_promissor": promissor,
            "natal_significator": significator,
            "construction": construction,
            "rotation_regime": "direct_primary_motion",
            "allowed_aspects": list(aspects),
            "latitude_treatment": (
                "body" if construction == "bodily_conjunction" else "constructed_ecliptic_beta_zero"
            ),
            "matchable_in_existing_role_timeline": True,
            "claim_of_complete_Lilly_original_1647_geometry": False,
        },
        "analyst_modern_test_candidate": {
            "event_code": proposed_event,
            "operational_definition_PROPOSED_NOT_SOURCE": observer_definition,
            "eligibility_PROPOSED_NOT_SOURCE": modern_eligibility_proposal,
            "time_window_status": "NOT_DEFINED",
            "observation_period_status": "NOT_DEFINED",
            "base_rate_and_control_group_status": "NOT_DEFINED",
            "questionnaire_option_status": "NOT_DEFINED",
        },
        "multiplicity": {
            "outcome_dependency_group": outcome_group,
            "alternative_outcomes_unresolved": unresolved_source_disjunction,
            "no_multiple_claim_success_credit": True,
        },
        "status": "SOURCE_ATTEMPTED_UNFROZEN_EVENT_INTERPRETATION",
        "not_a_prediction": True,
        "scored_people": 0,
        "reported_empirical_success": False,
    }


def claims() -> list[dict[str, Any]]:
    return [
        _claim(
            "LIL-E01",
            "Ascendant directed to Jupiter's body",
            _source((657,), "enriched in Fortune by the Gifts or Patronage"),
            "The direction is associated with gifts or patronage from eminent "
            "people and improved public estimation, with other good outcomes.",
            "jupiter",
            "asc",
            "bodily_conjunction",
            ("conjunction",),
            "external_patronage_or_award",
            "Third-party documented substantial gift, award or formal patronage "
            "obtained during a defined reporting period; threshold unresolved.",
            ("Jupiter's natal house and rulership", "source-defined benefic condition"),
            "Eligibility and materiality threshold would need independent definition.",
            outcome_group="institutional_benefit",
        ),
        _claim(
            "LIL-E02",
            "Ascendant directed to Mars's body",
            _source((659,), "in many Controversies and Law-suits"),
            "The source associates the direction with conflict, controversy, "
            "litigation and other often severe alternative misfortunes.",
            "mars",
            "asc",
            "bodily_conjunction",
            ("conjunction",),
            "formal_litigation_involvement",
            "Filed civil suit, criminal prosecution or named party to formal legal "
            "proceedings recorded independently. A mere disagreement is not a filing.",
            ("Mars natal sign, house and condition", "other chart mitigating influences"),
            "Define qualifying participation and jurisdiction consistently beforehand.",
            outcome_group="legal_conflict",
            unresolved_source_disjunction=True,
        ),
        _claim(
            "LIL-E03",
            "Ascendant directed to Venus's body",
            _source((661,), "if age and the condition of his Life permit, he will marry"),
            "The source describes affection and relationships and conditionally "
            "mentions marriage when age and circumstances permit.",
            "venus",
            "asc",
            "bodily_conjunction",
            ("conjunction",),
            "civil_marriage_registration",
            "Dated civil marriage registration, not merely romantic affection "
            "or a claimed feeling of relationship significance.",
            ("age and condition of life", "Venus's natal dignity/rulership"),
            "Eligible population and previously married status must be specified.",
            outcome_group="relationship_union",
            unresolved_source_disjunction=True,
        ),
        _claim(
            "LIL-E04",
            "Midheaven directed to hard aspect of Saturn",
            _source(
                (669,),
                "deprives him of his former Honour, Office, Magistracy, Employment or Reputation",
            ),
            "The source associates hard Saturn directions to MC with losses "
            "of office, employment, standing and other difficulties.",
            "saturn",
            "mc",
            "zodiacal_promissor_ray",
            ("square", "opposition"),
            "loss_of_formal_employment_or_held_office",
            "Dated involuntary removal from a formal employment role or "
            "held appointment; reputational feelings are a separate outcome.",
            (
                "Saturn's natal standing",
                "person previously holds relevant role",
                "source-specific hard-aspect ray treatment",
            ),
            "Person must hold a defined position at risk before the prospective interval.",
            outcome_group="career_office",
            unresolved_source_disjunction=True,
        ),
        _claim(
            "LIL-E05",
            "Midheaven directed to Jupiter's body",
            _source((669, 670), "preferred to Dignity and Honour"),
            "The direction is associated with honor, office or advancement "
            "adapted to the person's circumstances and social station.",
            "jupiter",
            "mc",
            "bodily_conjunction",
            ("conjunction",),
            "documented_promotion_or_office_appointment",
            "Formal role promotion, appointment or leadership office entered "
            "into an employment or institution record.",
            (
                "Jupiter's natal house/rulership",
                "source says preferment depends on the person's capacity and situation",
            ),
            "Define which appointments count and whether the participant is eligible.",
            outcome_group="career_office",
        ),
        _claim(
            "LIL-E06",
            "Sun directed to Venus's body",
            _source((683, 684), "an apt time for Marriage"),
            "The source describes romantic activity and potential marriage, "
            "with happiness explicitly conditional on Venus's radix strength.",
            "venus",
            "sun",
            "bodily_conjunction",
            ("conjunction",),
            "civil_marriage_registration",
            "Civil marriage during an independently declared future period.",
            (
                "radically strong Venus for happy marriage",
                "source also allows other social and recreational outcomes",
            ),
            "Specify unmarried/eligible cohort and avoid retrospective alternative outcomes.",
            outcome_group="relationship_union",
            unresolved_source_disjunction=True,
        ),
        _claim(
            "LIL-E07",
            "Sun directed to sextile/trine of Venus",
            _source(
                (684,),
                "Marriage, where none is before, or the Native to have a Son or Daughter borne",
            ),
            "The source proposes alternatives of marriage or childbirth "
            "depending on circumstances, plus wider beneficial themes.",
            "venus",
            "sun",
            "zodiacal_promissor_ray",
            ("sextile", "trine"),
            "marriage_or_birth_ALTERNATIVES_NOT_FROZEN",
            "Two distinct proposed candidate events: registered marriage "
            "or documented birth of a child. NEVER score either-or after outcomes.",
            (
                "Venus's natal condition",
                "existing marriage/offspring context",
                "historical signification may concern different persons",
            ),
            "Choose one primary outcome or a prospectively frozen joint scoring "
            "rule and eligibility criteria without seeing any target responses.",
            outcome_group="relationship_union",
            unresolved_source_disjunction=True,
        ),
    ]


def matches_role_contact(claim: dict[str, Any], record: dict[str, Any]) -> bool:
    """Match formal geometric ingredients, NOT a human outcome prediction.

    Source's old directional wording does not certify numerical parity of the
    modern role engine with every historical geometry or alternate time key.
    """
    proxy = claim["astronomical_proxy"]
    return (
        record.get("rotation_regime") == "direct_primary_motion"
        and record.get("construction") == proxy["construction"]
        and record.get("promissor") == proxy["moving_promissor"]
        and record.get("significator") == proxy["natal_significator"]
        and (
            (record.get("aspect") is None and proxy["allowed_aspects"] == ["conjunction"])
            if proxy["construction"] == "bodily_conjunction"
            else record.get("aspect") in proxy["allowed_aspects"]
        )
    )


def compile_register() -> dict[str, Any]:
    entries = claims()
    assert len(entries) == 7 and len({r["claim_id"] for r in entries}) == 7
    for row in entries:
        for photo in row["source"]["photos"]:
            assert Path(photo["path"]).name.startswith("lilly_1647_printed_")
        assert row["status"].endswith("UNFROZEN_EVENT_INTERPRETATION")
        assert row["scored_people"] == 0
    return {
        "schema": "LILLY_1647_SOURCE_EVENT_CANDIDATES_UNFROZEN_V1",
        "date": "2026-10-24",
        "status": "UNFROZEN_SOURCE_CLAIM_REGISTER_NO_PROSPECTIVE_PREDICTIONS",
        "source_scope": {
            "author": "William Lilly",
            "book": "Christian Astrology, first edition 1647, Book III",
            "photographic_witness": (
                "Wellcome Collection s7z7c46y, high-resolution photographed "
                "original printed pp654–684 as referenced per claim"
            ),
            "source_form": "short literal excerpt plus independently written paraphrase",
            "source_conditions": COMMON_SOURCE_CONDITIONS,
            "Lilly_radix_context_not_reconstructed_as_complete_engine": True,
            "original_1647_photos_sha256": {str(key): value for key, value in PHOTO_SHA256.items()},
        },
        "interpretation_frozen": False,
        "time_key_selected_for_human_test": False,
        "human_birth_or_event_records_used": False,
        "actual_prospective_human_outcomes_scored": 0,
        "standard": {
            "historical_source_statement": "ATTESSED_CONDITIONAL_CLAIM",
            "geometric_proxy": "ANALYTIC_IMPLEMENTATION_NOT_HISTORICAL_PARITY",
            "modern_event_operationalization": "ANALYST_PROPOSAL_NOT_SOURCE",
            "promisor_house_rulership_essential_dignity": "NOT_FULLY_CALCULATED",
            "future_window_and_baselines": "NOT_SELECTED",
        },
        "interpretation_dependency_groups": {
            "relationship_union": ["LIL-E03", "LIL-E06", "LIL-E07"],
            "career_office": ["LIL-E04", "LIL-E05"],
            "institutional_benefit": ["LIL-E01"],
            "legal_conflict": ["LIL-E02"],
        },
        "do_not_double_count": (
            "Do not score several alternative outcomes for one contact or "
            "correlated marriage claims as independent confirmations."
        ),
        "entries": entries,
    }


def save() -> None:
    data = compile_register()
    HERE.mkdir(exist_ok=True)
    (HERE / "LILLY_1647_EVENT_CLAIM_CANDIDATES.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    with (HERE / "LILLY_1647_EVENT_CLAIM_CANDIDATES.csv").open(
        "w", encoding="utf-8", newline=""
    ) as stream:
        fields = [
            "claim_id",
            "label",
            "printed_pages",
            "promissor",
            "significator",
            "construction",
            "allowed_aspects",
            "historical_excerpt",
            "modern_outcome_proposal",
            "outcome_dependency_group",
            "time_window_frozen",
            "human_predictive_validity",
        ]
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for item in data["entries"]:
            p = item["astronomical_proxy"]
            writer.writerow(
                {
                    "claim_id": item["claim_id"],
                    "label": item["label"],
                    "printed_pages": "+".join(map(str, item["source"]["printed_pages"])),
                    "promissor": p["moving_promissor"],
                    "significator": p["natal_significator"],
                    "construction": p["construction"],
                    "allowed_aspects": "+".join(p["allowed_aspects"]),
                    "historical_excerpt": item["source"]["verbatim_short_original_excerpt"],
                    "modern_outcome_proposal": item["analyst_modern_test_candidate"]["event_code"],
                    "outcome_dependency_group": item["multiplicity"]["outcome_dependency_group"],
                    "time_window_frozen": False,
                    "human_predictive_validity": "UNTESTED",
                }
            )
    print("7 original-source conditional claim candidates; 0 human predictions.")


if __name__ == "__main__":
    save()
