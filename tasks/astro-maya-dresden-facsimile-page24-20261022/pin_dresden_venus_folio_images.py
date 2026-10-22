#!/usr/bin/env python3
"""Pin two VISUALLY SEEN Förstemann Dresden facsimile folios separately from
modern scholarly decoded interpretations. No invented Maya natal rules.
"""
from pathlib import Path
from hashlib import sha256
import json,struct,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[1]
HOME=Path("/home/joel/Téléchargements")
PREVIOUS=ROOT/"tasks/astro-maya-dresden-original-folio-20261022/DRESDEN_FOLIO_SOURCE_WINDOWS_V1.json"
MANIFEST=B/"DRESDEN_VENUS_P24_P46_VISUAL_SOURCE_WITNESS_V1.json"
SOURCES=[
 {"id":"MAYA-DRESDEN-P24-FORSTEMANN1892-FACSIMILE",
  "historical_edition_page":"Dresden Codex p.24 (conventional Förstemann folio number)",
  "photographic_source_kind":"printed 1892 Förstemann pre-WWII facsimile via FAMSI, NOT authenticated present SLUB original photograph",
  "original_facsimile_pdf":"Dresden-Codex-Foerstemann-1892-Folios-13-24-FAMSI-reference.pdf",
  "pdf_source_url":"https://www.famsi.org/mayawriting/codices/pdf/2_dresden_fors_schele_pp13-24.pdf",
  "pdf_byte_count":16317460,
  "pdf_sha256":"b9f7cf25adb9fb5979c678443db3c4eff29cbd59119c60afd9571f348d62bfcb",
  "pdf_pages":12,"pdf_page_index_1_based":12,
  "page_png":"Dresden-Codex-Foerstemann-Folio24-Source-Image.png",
  "render_command":"pdftoppm -f 12 -l 12 -r 160 -png -singlefile",
  "rendered_width":828,"rendered_height":1778,"render_dpi":160,
  "render_sha256":"c38357416da0b53a0b4b5f39932e3230677d123840578ffe58a456a1d62fb032",
  "direct_visual_notes":"Tall surviving manuscript facsimile sheet: main hieroglyph columns on left and gridded bar/dot numerals on right with red outlined shapes and some damaged/stained marks. No glyphs deciphered independently.",
  "scholarly_subject_not_direct_glyph_read":"Venus table preface, long-count entry calculations, multiples/corrections to reuse the Venus table.",
  "source_readiness":"FACSIMILE_IMAGE_VISUALLY_INSPECTED_GLYPHS_NOT_DECIPHERED"},
 {"id":"MAYA-DRESDEN-P46-FORSTEMANN1892-FACSIMILE",
  "historical_edition_page":"Dresden Codex p.46 (traditional Förstemann numbering, physically following p.24 in corrected page order)",
  "photographic_source_kind":"printed 1892 Förstemann pre-WWII facsimile via FAMSI, NOT authenticated present SLUB original photograph",
  "original_facsimile_pdf":"Dresden-Codex-Foerstemann-1892-Folios-46-59-FAMSI-reference.pdf",
  "pdf_source_url":"https://www.famsi.org/mayawriting/codices/pdf/5_dresden_fors_schele_pp46-59.pdf",
  "pdf_byte_count":20358953,
  "pdf_sha256":"e99b4c9a5b97fe5c67cdb78e679662a36b06505bb793c8fa1b12d8371952909d",
  "pdf_pages":14,"pdf_page_index_1_based":1,
  "page_png":"Dresden-Codex-Foerstemann-Folio46-Source-Image.png",
  "render_command":"pdftoppm -f 1 -l 1 -r 130 -png -singlefile",
  "rendered_width":673,"rendered_height":1444,"render_dpi":130,
  "render_sha256":"2966d340ede6b20236e606d0e515384ce2729659c8d4808824e9f21119d42098",
  "direct_visual_notes":"Venus table first repeated leaf: left date/glyph and dot-bar number registers; right three stacked colored pictorial scenes with figures and ritual/weapon iconography. No goddess name or glyph passage deciphered independently.",
  "scholarly_subject_not_direct_glyph_read":"One row/calendar station of a multi-page Venus-cycle astronomical and divinatory table, associated with ritual warning imagery.",
  "source_readiness":"FACSIMILE_IMAGE_VISUALLY_INSPECTED_GLYPHS_NOT_DECIPHERED"}
]
def sha(path):return sha256(path.read_bytes()).hexdigest()
def pdf_pages(path):
 p=subprocess.run(["pdfinfo",str(path)],capture_output=True,text=True,check=True)
 for line in p.stdout.splitlines():
  if line.startswith("Pages:"):return int(line.split(":",1)[1].strip())
 raise ValueError("PDF page count not discoverable")
def image_dimensions(file):
 b=file.read_bytes()[:24]
 if b[:8]!=b"\x89PNG\r\n\x1a\n":raise ValueError("Original image PNG signature mismatch")
 return struct.unpack(">II",b[16:24])
def read():
 if MANIFEST.exists():raise ValueError("Existing witness manifest; inspect rather than overwrite")
 previous=json.loads(PREVIOUS.read_text("utf-8"))
 if not previous["candidate_folio_windows"][0]["original_image_canvas_seen"] is False:
  raise ValueError("Previous record already claims an image was seen; reconcile first")
 for x in SOURCES:
  source=HOME/x["original_facsimile_pdf"]
  image=HOME/x["page_png"]
  if not source.is_file() or not image.is_file():raise ValueError("Source media missing for "+x["id"])
  if (source.stat().st_size,sha(source),pdf_pages(source))!=(x["pdf_byte_count"],x["pdf_sha256"],x["pdf_pages"]):
   raise ValueError("Original PDF source witness or page count diverged")
  if (sha(image),*image_dimensions(image))!=(x["render_sha256"],x["rendered_width"],x["rendered_height"]):
   raise ValueError("Original scanned page image SHA/dimensions diverged")
 controls={
  "source_almanac_subject":"Maya historical Venus astronomical/ritual calendar, NOT modern natal personality",
  "traditional_canonical_Venus_period_days":584,
  "five_Venus_periods_per_table_row":5,
  "derived_table_row_days":2920,
  "rows_per_full_cycle":13,
  "derived_full_table_days":37960,
  "sacred_Tzolkin_cycle_days":260,
  "Haab_vague_year_days":365,
  "counts_as_104_Haab_years_not_104_tropical_Gregorian_years":True,
  "Venus_phase_interval_candidate_from_scholarly_reading_days":[236,90,250,8],
  "source_of_phase_intervals":"published academic reading for pages46–50, NOT independent new glyph-decipherment",
  "Maya_GMT_Long_Count_correlation_pinned_or_verified":False,
  "independent_original_Venus_glyph_number_decipherment_completed":False,
  "birth_day_traits_original_to_question_mapping_completed":False,
  "Maya_natal_oracular_rules_promoted":0
 }
 if 584*5!=2920 or 2920*13!=37960 or 584*65!=37960 or 260*146!=37960 or 365*104!=37960 or sum(controls["Venus_phase_interval_candidate_from_scholarly_reading_days"])!=584:
  raise ValueError("Scholarly Venus/Haab/Tzolkin arithmetic is internally inconsistent")
 doc={
  "schema":"MAYA_DRESDEN_VENUS_P24_P46_FOERSTEMANN_1892_VISUAL_WITNESS_V1",
  "as_of":"2026-10-22","parent_original_folio_discovery":"research/astro-maya-dresden-first-folio-20261022",
  "source_witnesses":SOURCES,"source_checked_on_authorized_owner_computer":True,
  "primary_custodian_original":"SLUB Dresden, original historical codex (different from rendered facsimile)",
  "verified_original_held_codex_high_resolution_photographs":False,
  "Förstemann_1892_FAMSI_pdf_original_facsimile_source_verified":True,
  "independently_transcribed_Maya_hieroglyph_signs":0,
  "scholarly_derived_mathematical_claims":controls,
  "independently_authenticated_Maya_natal_personality_claims":0,
  "independent_real_human_blind_predictions":0,
  "runtime_astrology_rules_promoted":0,
  "interpretive_bibliography":[
   {"kind":"original-holder institution interpretive catalog","url":"https://www.slub-dresden.de/en/explore/manuscripts/the-dresden-maya-codex/content"},
   {"kind":"facsimile source catalog with 1892 chronology and historic pagination warnings","url":"https://www.famsi.org/mayawriting/codices/dresden.html"},
   {"kind":"independent journal research original Venus cycle and four phase intervals","url":"https://www.scielo.org.mx/scielo.php?pid=S0185-25742010000100002&script=sci_arttext"},
   {"kind":"Aldana revised reading source-critical disagreement with older reconstruction","url":"https://escholarship.org/uc/item/6cr1s6jd"}
  ],
  "editorial_transmission_risk":"Current codex water-damaged in World War II; faithful 1892 facsimile may preserve visual traces but is not direct extant original photographed today. Historic incorrect bound-page numbering p24 then p46–50 is conventional and must not be naively interpreted as interrupted Venus table.",
  "nonreading_scope":"P47–P50 original glyphs and Venus sequence not individually inspected; no direct original SLUB canvases retrieved; NcodeX RS01 IIIF manifest endpoint timed out; no full manuscript reading; no personal astrology prediction."
 }
 MANIFEST.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"schema":doc["schema"],"facsimiles":len(SOURCES),"source_image_sha256":[x["render_sha256"] for x in SOURCES],"math":controls["derived_full_table_days"],"real_human_predictions":0},indent=2))
if __name__=="__main__":read()
