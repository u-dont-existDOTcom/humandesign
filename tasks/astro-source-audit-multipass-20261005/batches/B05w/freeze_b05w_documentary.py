#!/usr/bin/env python3
"""Original first-edition fourth-house father/patrimony: documentary only."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def load(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, payload):
    (B / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


source = load("SOURCE_FIRST_AUTHORING_20261017.json")
assert source["batch"] == "B05w"
assert source["section"] == "UNNUMBERED_FOURTH_HOUSE_FATHER"
assert source["original_body_pdf_frames"] == [603, 604]
assert len(source["groups"]) == 12
records, mapping = [], []
for gi, group in enumerate(source["groups"], start=1):
    sid = f"B05w-S{gi:03d}"
    assert group["source_span"] == sid
    assert set(group["page_frames"]) <= {603, 604, 605}
    ids = []
    for claim in group["claims"]:
        number = 7296 + len(records)
        rid = f"R{number}"
        assert claim["id"] == rid
        assert len(claim["anchor_not_diplomatic"]) >= 12
        assert len(claim["historical_only_meaning"]) >= 50
        assert not (claim["verified_human_father_outcome"] or claim["runtime_promoted"])
        row = {
            "id": rid,
            "record_number": number,
            "source_span": sid,
            "original_pdf_frames": group["page_frames"],
            "role": claim["role"],
            "printed_chapter": (
                "UNNUMBERED_FOURTH_HOUSE_FATHER"
                if claim["role"] != "next_chapter_navigation"
                else "CXXII_NAVIGATION_ONLY"
            ),
            "original_anchor_not_diplomatic": claim["anchor_not_diplomatic"],
            "meaning_historical_only": claim["historical_only_meaning"],
            "qualification": claim["source_qualification"],
            "historical_documentary_accepted": True,
            "independent_human_parent_status_validated": False,
            "human_lifespan_or_death_cause_validated": False,
            "human_socioeconomic_ancestry_validated": False,
            "modern_medical_legal_utility": False,
            "runtime_model_promoted": False,
        }
        records.append(row)
        ids.append(rid)
    mapping.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["page_frames"],
            "source_group": group["subject"],
            "mapped_record_ids": ids,
        }
    )
assert len(records) == 62
assert [r["record_number"] for r in records] == list(range(7296, 7358))
assert [r["id"] for r in records if r["role"] == "next_chapter_navigation"] == ["R7356", "R7357"]
assert len(set(x["id"] for x in records)) == 62

images = {}
for n in (603, 604, 605):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    data = p.read_bytes()
    assert data[:2] == bytes.fromhex("ffd8") and len(data) > 150000
    images[str(n)] = {
        "path": str(p.relative_to(B)),
        "sha256": sha(p),
        "bytes": len(data),
        "printed_folio": str(n - 34),
        "role": "father_section_body" if n in (603, 604) else "following_mother_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B05w",
        "source": (
            "William Lilly Christian Astrology 1647 original first edition, Wellcome b30338724"
        ),
        "source_pdf_sha256": "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        "father_section_body_frames": [603, 604],
        "mother_printed_chapter_CXXII_start_frame": 604,
        "source_folio_order_continuous": True,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05w",
        "source_groups": mapping,
        "record_count": 62,
        "source_group_count": 12,
        "substantive_historical_records": 60,
        "next_chapter_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05w",
        "issues": [
            (
                "The 1647 father/patrimony claims are not independent human wealth, "
                "lifespan, medical or ancestry observations."
            ),
            (
                "The first 4 categories of father significators are fourth house, "
                "fourth ruler, Sun by day/Saturn by night, and occupants in fourth; "
                "sect matters."
            ),
            (
                "The author's father-own-nativity-preferable caveat limits what "
                "could be inferred from a child's chart and introduces additional "
                "historical birth-data quality conditions."
            ),
            (
                "Good parent conditions involve source agreement between dignities, "
                "angles/succedents, benefic aspects and non-affliction; the variants "
                "are not independent empirical studies."
            ),
            (
                "Mixed fortunate and unfortunate testimony is explicitly allowed, "
                "with discretionary strongest fourth occupant selecting among "
                "multiple candidates."
            ),
            (
                "Jupiter/Venus and Sun/Saturn friendly contact for father longevity "
                "has several conjunction/aspect interpretation alternatives and is "
                "not an observed survival prediction."
            ),
            (
                "The cluster of Sun, Saturn, Mars and Mercury glyphs in fourth on "
                "PDF604 has uncertain AND/OR operator scope; do not encode a "
                "categorical short-life rule."
            ),
            (
                "Sun with lunar node plus Moon in fourth yields both father lineage "
                "and the native's life outcome; these are different target persons."
            ),
            (
                "A masculine-sign/Mars-related glyph in the Sun/Moon paragraph is "
                "not securely adjudicated and must not enter a scoring algorithm."
            ),
            (
                "The Sun/Saturn cadent/malefic clause contains a disputed glyph, "
                "potentially modifying a death prediction; preserve uncertainty."
            ),
            (
                "The asserted death-by-melancholy is premodern medical language, "
                "never a diagnosis or a claim about an actual person's cause of "
                "death."
            ),
            (
                "The chapter's father/mother relative descent comparison is "
                "historical social-class stereotyping; not evidence of ancestry, "
                "ethnicity or family standing."
            ),
            (
                "No measured parent survival, income, residence, inheritance, age "
                "adjustments, pre-registered prediction window, cohort or "
                "class-matched control is provided."
            ),
            (
                "The next printed CHAP CXXII mother section begins midway original "
                "PDF604; its substantive clauses must be extracted separately."
            ),
            (
                "Only source images and selective anchored paraphrases are retained; "
                "no full diplomatic glyph-by-glyph transcription is certified."
            ),
        ],
        "original_diplomatic_transcription_complete": False,
        "independent_human_parent_predictions": 0,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B05w",
        "status": "FIRST_EDITION_UNNUMBERED_FATHER_PATRIMONY_HISTORICAL_ONLY",
        "source_section": "UNNUMBERED_FOURTH_HOUSE_FATHER",
        "record_count": 62,
        "first_record": "R7296",
        "last_record": "R7357",
        "source_passages": 12,
        "substantive_source_records": 60,
        "next_printed_chapter_navigation": 2,
        "body_original_pdf_frames": [603, 604],
        "following_CXXII_heading_pdf_frame": 604,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "independent_parent_predictions": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B05w",
        "status": "SOURCE_ONLY_LOCALLY_ACCEPTED_PENDING_REMOTE",
        "previous_lilly": 7295,
        "new_records": 62,
        "lilly_if_published": 7357,
        "ptolemy_retained": 1066,
        "combined_if_published": 8423,
        "substantive_records": 60,
        "navigation": 2,
        "source_groups": 12,
        "numbered_chapters_added": 0,
        "next_printed_chapter": "CXXII",
        "next_original_pdf_frame": 604,
        "rules_sha256": sha(B / "RULES.json"),
        "source_author_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "empirical_validations": 0,
        "human_mortality_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B05w source-only 62 historical records R7296-R7357; 0 empirical")
