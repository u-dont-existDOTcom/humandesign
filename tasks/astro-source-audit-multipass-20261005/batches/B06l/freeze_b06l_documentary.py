#!/usr/bin/env python3
"""Freeze original 1647 Lilly spouse appearance/temperament/wealth source history."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def write(name, item):
    (B / name).write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


author = j("SOURCE_FIRST_AUTHORING_20261017.json")
assert author["batch"] == "B06l"
assert author["printed_chapter"] == "CXXXIIII"
assert author["body_original_pdf_frames"] == [627, 628, 629, 630, 631]
assert author["following_printed_chapter"] == "CXXXV"
assert author["next_heading_original_pdf"] == 631
assert len(author["groups"]) == 14

notes, reverse = [], []
for group_no, group in enumerate(author["groups"], 1):
    sid = f"B06l-S{group_no:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {627, 628, 629, 630, 631}
    ids = []
    for claim in group["clauses"]:
        n = 8142 + len(notes)
        rid = f"R{n}"
        assert claim["id"] == rid
        assert len(claim["original_anchor_not_diplomatic"]) >= 6
        assert len(claim["historical_source_meaning"]) >= 45
        assert claim["source_only"]
        assert not claim["empirical_human_accuracy_validated"]
        assert not claim["person_level_sex_morality_disability_or_mortality_claim_authorized"]
        assert not claim["runtime_promoted"]
        notes.append(
            {
                "id": rid,
                "record_number": n,
                "batch": "B06l",
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "source_anchor_not_diplomatic": claim["original_anchor_not_diplomatic"],
                "historical_meaning_only": claim["historical_source_meaning"],
                "qualifier": claim["qualifier"],
                "documentary_source_accepted": True,
                "independent_human_appearance_accuracy_validated": False,
                "independent_human_spouse_personality_validated": False,
                "independent_spouse_wealth_class_validated": False,
                "independent_marital_medical_mortality_validated": False,
                "real_person_moral_intimate_danger_label_authorized": False,
                "original_ptolemy_attribution_independently_verified": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["source_group"],
            "mapped_record_ids": ids,
        }
    )
assert len(notes) == 131
assert [x["record_number"] for x in notes] == list(range(8142, 8273))
assert [x["id"] for x in notes if x["role"] == "next_chapter_navigation"] == ["R8271", "R8272"]
assert len({x["id"] for x in notes}) == 131

images = {}
for frame in range(627, 635):
    path = B / "evidence" / f"pdf_1647-{frame}.jpg"
    raw = path.read_bytes()
    assert len(raw) > 150000 and raw[:2] == bytes.fromhex("ffd8")
    images[str(frame)] = {
        "file": str(path.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(path),
        "printed_folio": str(frame - 34),
        "source_role": "original_cxxxiiii_body" if frame <= 631 else "next_chapter_context",
    }
write(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06l",
        "source": "William Lilly Christian Astrology first edition 1647 Wellcome b30338724",
        "original_pdf_sha256": ("2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"),
        "original_body_pdf_frames": [627, 628, 629, 630, 631],
        "next_printed_CXXXV_heading_frame": 631,
        "original_source_images": images,
    },
)
write(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06l",
        "source_groups": reverse,
        "source_group_count": 14,
        "record_count": 131,
        "substantive": 129,
        "following_navigation": 2,
    },
)
write(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06l",
        "issues": [
            (
                "Original printed CXXXIIII begins as a wife's appearance "
                "question, but multiple substantive unnumbered sections "
                "include supposed temperament, dowry/wealth, moral character "
                "and fortune attributed to marriage before next printed chapter."
            ),
            (
                "Old zodiac-sign names and sign portion glyphs for pulchritude, "
                "mediocrity, deformity have not all been professionally "
                "double-read; no executable sign category allowed."
            ),
            (
                "Saturn affliction, combustion, Venus/Saturn conjunction, "
                "Jupiter-Venus-Moon aspects, and old/widowed spouse are "
                "separate targets and require all printed qualifiers."
            ),
            (
                "Planetary 'well affected' versus 'ill affected' condition "
                "reverses the author's claims for Saturn, Jupiter, Mars, "
                "Venus and Mercury; no unqualified planet-to-person mapping."
            ),
            (
                "The author says Sun and Moon do not directly signify "
                "temperament only in the Conditions of Wife passage, "
                "not in other marriage predictions in same book."
            ),
            (
                "The Venus-position aphorisms conflate legal marriage age "
                "with marital history, sexual conduct, fertility, "
                "class, alleged sorcery, poisoning and spouse character."
            ),
            (
                "Historical accusations about infidelity, prostitution, "
                "dishonesty, poison, magic or dangerous persons must not "
                "be inferred from or applied to real individuals."
            ),
            (
                "Historical infertility and childlessness assertions are "
                "not medical evidence or appropriate treatment advice."
            ),
            (
                "Original spouse beauty/deformity language is discriminatory "
                "and does not establish any person's disability, appearance "
                "or social attractiveness."
            ),
            (
                "Ptolemy, Leovitius, Pezelius, Schoenerus, Garceus and "
                "Origanus are attributed by Lilly; their original texts "
                "have not been independently collated for these rules."
            ),
            (
                "Lilly explicitly says favorable benefics do not automatically "
                "mean an aristocratic spouse: outcome must be relative "
                "to natal social class and actual status baseline."
            ),
            (
                "Strong malefics in seventh can still indicate spouse wealth "
                "according to the source, with alleged scandal or poor "
                "temperament; avoid binary malefic = poor."
            ),
            (
                "Several seventh/sixth/twelfth/eighth house placements "
                "have inverse alternative rulership paths, not both "
                "required in one chart."
            ),
            (
                "Saturn grief and Mars destruction/death old associations "
                "are historical hypotheses, not mortality or danger "
                "predictions; benefic aspects are explicit source exception."
            ),
            (
                "No independently verifiable natal records, spouse body "
                "measurements, marital surveys, wealth documents, "
                "class changes or death dates were evaluated."
            ),
            (
                "No frozen scoring weights, exact dignity/aspect orbs, "
                "clinical definitions, gender-neutral applicability or "
                "ethical target-validation protocol exists for this text."
            ),
            (
                "The following printed CXXXV mutual love and concord "
                "begins lower PDF631 and is a distinct relationship source."
            ),
            (
                "Original photographic sources and concise paraphrases "
                "do not amount to a diplomatic first-edition transcription."
            ),
        ],
        "original_glyph_categories_fully_resolved": False,
        "independent_person_level_accuracy": 0,
        "real_person_spouse_character_moral_or_disability_claim_authorized": False,
        "person_health_or_mortality_forecasts_authorized": False,
        "runtime_promotions": 0,
    },
)
write(
    "RULES.json",
    {
        "batch": "B06l",
        "status": "ORIGINAL_1647_WIFE_APPEARANCE_CONDITION_WEALTH_HISTORICAL_ONLY",
        "printed_chapter": "CXXXIIII",
        "editorial_chapter": "CXXXV",
        "record_count": 131,
        "first_record": "R8142",
        "last_record": "R8272",
        "substantive": 129,
        "next_chapter_navigation": 2,
        "source_groups": 14,
        "original_source_body_frames": [627, 628, 629, 630, 631],
        "following_printed_CXXXV_frame": 631,
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "person_level_character_or_marriage_outcomes_validated": 0,
        "runtime_promotions": 0,
        "rules": notes,
    },
)
write(
    "ACCEPTANCE.json",
    {
        "batch": "B06l",
        "status": "ORIGINAL_SOURCE_WIFE_APPEARANCE_LOCALLY_FROZEN_PENDING_REMOTE",
        "prior_lilly": 8141,
        "new_historical_annotations": 131,
        "lilly_if_published": 8272,
        "ptolemy_retained": 1066,
        "combined_if_published": 9338,
        "substantive": 129,
        "navigation": 2,
        "source_groups": 14,
        "numbered_chapters_added": 1,
        "next_printed_chapter": "CXXXV",
        "next_original_pdf_frame": 631,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "empirical_validations": 0,
        "real_person_results_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B06l 1647 original wife appearance + character/wealth: 131 R8142-R8272")
