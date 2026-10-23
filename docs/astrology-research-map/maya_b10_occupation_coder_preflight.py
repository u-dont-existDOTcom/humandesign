#!/usr/bin/env python3
"""Source-specific craft role *coding preflight*, not a natal behavior scorer.

Applies a manually supplied verified ISCO-08 unit code to an occupational
task record. This does not infer codes from free-text or participant identity.
The narrowed codes are investigator-defined for historical Chuen source
alignment; never call this an official ILO birth-day instrument.

No participant date, name, occupation narrative or birth sign is stored.
"""
from __future__ import annotations

from collections.abc import Mapping

CORE_ISCO_08 = frozenset({
    "7115",  # carpenters / joiners
    "7314",  # potters
    "7317",  # handicrafts in wood and basketry
    "7318",  # handicrafts in textile and leather
    "7522",  # cabinet-makers
    "7531",  # tailors and dressmakers
    "7533",  # sewing and embroidery workers
})
VERIFICATION = frozenset({"verified", "uncertain", "unreviewed"})
ROLE_SCOPE = frozenset({"paid_work", "self_employment", "unpaid_apprenticeship",
                        "unpaid_regular_subsistence", "not_an_occupation"})
_ALLOWED = frozenset({"isco_unit_code","code_verification","role_scope"})

class CodingScopeError(ValueError):
    pass

def classify_occupation_candidate(record:Mapping)->dict:
    """Use already task-verified unit code; do NOT auto-label actual humans.

    An ISCO code for unpaid informal making is not officially a job unless
    occupation coding authority is independently justified. Such cases remain
    review-required and outside the core occupation indicator.
    """
    if not isinstance(record,Mapping) or set(record)!=_ALLOWED:
        raise CodingScopeError("Preflight accepts only three anonymous coding metadata fields")
    code=record["isco_unit_code"]
    verification=record["code_verification"]
    scope=record["role_scope"]
    if type(code) is not str or (len(code)!=4 and code!="UNAVAILABLE") or (
        code!="UNAVAILABLE" and not code.isdecimal()
    ):
        raise CodingScopeError("Pass verified four-digit ISCO-08 unit code, or UNAVAILABLE")
    if type(verification) is not str or verification not in VERIFICATION:
        raise CodingScopeError("Unknown independent coder verification status")
    if type(scope) is not str or scope not in ROLE_SCOPE:
        raise CodingScopeError("Unknown occupation participation scope")
    if code=="UNAVAILABLE" and verification=="verified":
        raise CodingScopeError("Uncoded occupational description cannot be verified")
    if verification!="verified" or scope in {"unpaid_apprenticeship","unpaid_regular_subsistence"}:
        state="ABSTAIN_PENDING_MANUAL_CODE_OR_UNPAID_SCOPE_REVIEW"
        core_flag=None
    else:
        # A verified code is still only a candidate role under this instrument.
        core_flag=code in CORE_ISCO_08 and scope in {"paid_work","self_employment"}
        state="PROVISIONAL_NARROW_ISCO_MATCH" if core_flag else "PROVISIONAL_NO_NARROW_ISCO_MATCH"
    return {
        "status":state,
        "narrow_ISCO_candidate_core_role":core_flag,
        "investigator_selected_codes_not_official_ILO_Chuen_measure":True,
        "birth_data_read":False,
        "respondent_craft_score_created":False,
        "validated_natal_prediction":False,
    }
