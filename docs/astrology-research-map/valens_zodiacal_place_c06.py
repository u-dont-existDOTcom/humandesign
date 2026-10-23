"""Source-only comparison: 'zodiacal place' (topos zodiakos), not monomoiria.

Primary/witnessed attestations:
* Vettius Valens, Anthologies VIII.7 example, Riley translation,
  owned PDF p145: the table at Leo 22 degrees gives Virgo.
* P.Oxy. LXI 4277, columns i 23-25 as discussed by Cristian Tolsa,
  ZPE 203 (2017) p192: the ascendant at Leo 22°11' is accompanied by
  a zodiacal-place label Virgo.
* Same papyrus Mercury Capricorn 6°22' labelled Sagittarius: no matching
  attested Valens entry located here; therefore *do not* "validate" it.

These are text-evidence records, not a recovered full Valens table,
an ancient biography, or a forecast. The integer 22 in Valens and the
papyrus' 22°11' are not assumed to share a settled ordinal convention.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class PlaceAttestation:
    id: str
    document: str
    sign: str
    longitude: str
    assigned_place: str
    locator: str

WITNESSES = (
    PlaceAttestation("VALENS_VIII_7_LEO22", "Valens Anthologies",
        "Leo","22°","Virgo", "Riley translation Book VIII, PDF p145"),
    PlaceAttestation("POXY_4277_ASC_LEO22_11", "P.Oxy. LXI 4277",
        "Leo","22°11'","Virgo", "Tolsa 2017 p192, col. i 23-25"),
    PlaceAttestation("POXY_4277_MERC_CAP6_22", "P.Oxy. LXI 4277",
        "Capricorn","6°22'","Sagittarius", "Tolsa 2017 p192, col. i 13-14"),
)

def witnessed_assignment(witness_id: str) -> str:
    """Only exact identifiers from independently read attestation records."""
    matches = [w for w in WITNESSES if w.id == witness_id]
    if len(matches) != 1:
        raise ValueError("no individually authenticated historical attestation")
    return matches[0].assigned_place

def cross_document_concordance() -> dict:
    entries = [w for w in WITNESSES if w.sign == "Leo"]
    return {
        "historical_texts_compared":len(entries),
        "leo_place_overlap":len(set(w.assigned_place for w in entries))==1,
        "common_place":"Virgo",
        "papyrus_capricorn_entry_independently_reconstructed":False,
        "same_degree_notation_proven":False,
        "prediction_or_human_success":False,
        "outcome":"SHARED_ZODIACAL_PLACE_TEXT_ALLOCATION_ONLY"
    }

if __name__=="__main__":
    import json
    print(json.dumps(cross_document_concordance(),indent=2))
