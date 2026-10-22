"""B59 synthetic text-transmission diagnostics. No personal-chart scoring."""
from dataclasses import dataclass

def h(reference,sign):
    if any(type(i) is not int or not 0 <= i < 12 for i in (reference,sign)):
        raise ValueError("Synthetic signs must be integers 0..11")
    return (sign-reference)%12+1

def v27(al,ul,planet,synthetic=False):
    if not synthetic:
        raise ValueError("synthetic-only")
    sanskrit=h(al,planet)==2
    portuguese=h(ul,planet)==2
    return {"SANSKRIT_AL_2":sanskrit, "PORTUGUESE_UL_2":portuguese,
            "source_selected":None, "score_allowed":False}

def v12(aspect11,aspect12,synthetic=False):
    if not synthetic:
        raise ValueError("synthetic-only")
    if type(aspect11) is not bool or type(aspect12) is not bool:
        raise TypeError("Aspects must be boolean")
    return {"SANSKRIT":aspect11 and not aspect12,
            "PORTUGUESE_LITERAL":aspect12 and not aspect12,
            "score_allowed":False}

def v15(aspect12,malefic_association12,synthetic=False):
    if not synthetic:
        raise ValueError("synthetic-only")
    if type(aspect12) is not bool or type(malefic_association12) is not bool:
        raise TypeError("Predicates must be booleans")
    return {"SANSKRIT_NO_ASPECT":not aspect12,
            "PORTUGUESE_NO_MALEFIC_ASSOCIATION":not malefic_association12,
            "score_allowed":False}

KIN={"mother","father","sibling","child","spouse","family","relative"}
def v29(target):
    if not isinstance(target,str) or not target:
        raise ValueError("Named target required")
    return {"SANSKRIT_KARAKAMSHA_TRANSFER":target not in KIN,
            "PORTUGUESE_KIN_EXCLUSION_OMITTED":True,
            "score_allowed":False}

@dataclass(frozen=True)
class ParentRule:
    verse:str
    original_house:int
    target:str

def v22_transfer(parent):
    if parent.verse not in {"29.16","29.17","29.18","29.19","29.20","29.21"} or parent.original_house != 12:
        raise ValueError("Transfer only documented source 29.16-21")
    return {"verse":"29.22","derived_house":11,
            "parent":parent.verse,"target":"SOURCE_OF_GAIN",
            "independent_source":False,"score_allowed":False}

def v35_transfer(parent_rule,pada):
    if not parent_rule or pada not in {"child","wealth","other"}:
        raise ValueError("Explicit family and target required")
    return {"verse":"29.35","inherited_from":parent_rule,"destination":pada,
            "independent_source":False,"score_allowed":False}
