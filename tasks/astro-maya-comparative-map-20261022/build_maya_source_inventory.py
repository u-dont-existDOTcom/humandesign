#!/usr/bin/env python3
"""Read-only owner-supplied Maya book intake; save hashes and roles, never book contents.

The original copyrighted PDF/EPUB files remain outside humandesign. No OCR,
no copying originals into git, and no claiming books have been read in full.
"""
from __future__ import annotations
from pathlib import Path
from hashlib import sha256
from datetime import date
import argparse, json, subprocess, zipfile, re, html

SOURCES=(
  ("MAYA-AVENI-VAIL-MADRID", "Madrid Codex", "The Madrid Codex: New Approaches to Understanding an Ancient Maya Manuscript",
   "Gabrielle Vail and Anthony F. Aveni (editors)", "2004 (catalogue; local filename says 2010)",
   "source_critical_Codex_Madrid_interpretation", "source_criticism_not_verified_natal_prediction",
   "4a75d30f35e0f0832ecf124150fe28123738b2a1428589a9403d8cd3ddfe0f23",461),
  ("MAYA-AVENI-SKYWATCHERS","Skywatchers","Skywatchers: A Revised and Updated Version of Skywatchers of Ancient Mexico",
   "Anthony F. Aveni", "2001 revised edition", "historical_astroarchaeology_and_sky_tables",
   "astronomical_context_not_natal_personality_evidence",
   "1c39aae446dfb6921b44e5f19843a41d014a7bbf9edd0ee959d67284721fce70",428),
  ("MAYA-REINGOLD-DERSHOWITZ-CALENDRICAL","Calendrical calculations",
   "Calendrical Calculations: The Ultimate Edition",
   "Edward M. Reingold and Nachum Dershowitz","2018 fourth/ultimate edition",
   "formal_calendar_conversion_algorithms",
   "math_not_personality_divination_or_original_classical_rulebook",
   "8d1be3796c9265f0f6cfa85a4628ed61c3e3466c1954ec095b998a262782f48f",663),
  ("MAYA-TEDLOCK-HIGHLAND-DAYKEEPERS","Time and the Highland Maya",
   "Time and the Highland Maya","Barbara Tedlock","1992 revised edition",
   "living_Maya_daykeeper_260_day_ethnography",
   "regional_living_practice_not_universal_historic_classic_code",
   "95c88db1d7310e2b247a7ed5b8f15136abb27064ed49b3c3a33949ce7e607081",None),
  ("EXCLUDE-WHEELER-FICTION","Doomsday Match",
   "Doomsday Match (The Dresden Codex, Book 1)","Jeff Wheeler","2023",
   "FICTION_NOT_THE_DRESDEN_CODEX",
   "excluded_from_historical_source_evidence",
   "498cd6e83b30c0ef35dc9c511d13ae1db55d46d81558c92a4faae4fedb73d1f2",None)
)

SOURCE_WINDOWS={
 "MAYA-AVENI-VAIL-MADRID":[{"source":"The Madrid Codex","pdf_index_start":170,"topic":"Chapter 5: Maya Calendars and Dates (Tzolk'in, almanacs)"},
                           {"source":"The Madrid Codex","pdf_index_start":186,"topic":"Chapter 6: Intervallic Structure"},
                           {"source":"The Madrid Codex","pdf_index_start":210,"topic":"Chapter 7: Haab dates in Codex"}],
 "MAYA-AVENI-SKYWATCHERS":[{"pdf_index_start":141,"topic":"Maya astronomy/history, calendar and codices"},
                            {"pdf_index_start":153,"topic":"Tzolk'in / ritual almanac"},
                            {"pdf_index_start":175,"topic":"Lunar eclipse and Venus astronomy (first read historical terminology)"}],
 "MAYA-REINGOLD-DERSHOWITZ-CALENDRICAL":[{"pdf_index_start":214,"topic":"Chapter 11 Mayan Long Count, Haab, Tzolkin, Aztec calendars (printed pp169–184)"}],
 "MAYA-TEDLOCK-HIGHLAND-DAYKEEPERS":[{"ebook_page_label":"1","topic":"Introduction to Maya time study"},
                                  {"ebook_page_label":"91–99","topic":"260-day count, ritual/calendar ethnography"},
                                  {"ebook_page_label":"200","topic":"260-day cycle and Year-bearer relationship"}],
 "EXCLUDE-WHEELER-FICTION":[]
}

PRIMARY_FACSIMILES=[
 {"id":"DRESDEN-CODEX-DIGITAL","title":"Dresden Maya Codex (original manuscript digitization)",
  "url":"https://www.slub-dresden.de/en/explore/manuscripts/the-dresden-maya-codex","status":"official_online_retrieval_available_unchanged"},
 {"id":"MADRID-CODEX-FAMSI","title":"Madrid Codex facsimile digital reproductions",
  "url":"https://www.famsi.org/mayawriting/codices/madrid.html","status":"historic_facsimile_links_retrievable_review_permissions_quality"},
 {"id":"CODEX-MAYA-MEXICO","title":"Códice Maya de México (formerly Grolier; official INAH edition/exhibition)",
  "url":"https://codicemayademexico.inah.gob.mx/","status":"official_historic_manuscript_context_available"},
]

def sha(path:Path)->str:
    h=sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""):
            h.update(chunk)
    return h.hexdigest()

def pages(path:Path)->int:
    p=subprocess.run(["pdfinfo",str(path)],capture_output=True,text=True,timeout=30)
    if p.returncode:raise RuntimeError("Original PDF cannot be inspected")
    m=re.search(r"(?m)^Pages:\s*(\d+)",p.stdout)
    if not m:raise RuntimeError("PDF page count absent")
    return int(m.group(1))

def epub_scan(path:Path)->dict:
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        xmlpages=[n for n in names if re.search(r"content/page_\d+\.xml$",n)]
        htmlfiles=[n for n in names if n.lower().endswith((".xhtml",".html",".htm"))]
        proof=False
        if xmlpages:
            samples=[n for n in xmlpages if n in ("content/page_1.xml","content/page_200.xml")]
            joined=" ".join(html.unescape(re.sub(r"<[^>]*>"," ",z.read(n).decode("utf-8",errors="replace"))) for n in samples)
            proof="Momostec" in joined or "Maya" in joined
        if not proof and htmlfiles:
            proof=any("fiction" in z.read(n).decode("utf-8",errors="replace").lower() or "Doomsday" in z.read(n).decode("utf-8",errors="replace") for n in htmlfiles[:10])
        if not proof:raise ValueError("EPUB claimed contents could not be distinguished")
        opf=next(n for n in names if n.endswith(".opf"))
        data=z.read(opf).decode("utf-8",errors="replace")
        titles=re.findall(r"<dc:title[^>]*>(.*?)</dc:title>",data,re.S)
        return {"epub_xml_page_files":len(xmlpages),"epub_html_section_files":len(htmlfiles),
                "epub_package_metadata_title":titles[0] if titles else None,
                "actual_chapter_content_checked":proof,
                "test_metadata_anomaly":titles==["test"]}
                
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--library",type=Path,default=Path.home()/"Documents/astrology")
    parser.add_argument("--out",type=Path,default=Path(__file__).resolve().parent/"MAYA_LOCAL_SOURCE_INVENTORY_V1.json")
    args=parser.parse_args()
    if args.out.exists():raise ValueError("Source inventory exists; verify before overwriting")
    records=[]
    for code,token,title,authors,edition,role,limitation,expected_sha,page_expect in SOURCES:
        paths=list(args.library.glob("*"+token+"*"))
        if len(paths)!=1:raise ValueError(f"Expected exactly one local source {code}; found {len(paths)}")
        p=paths[0]
        actual=sha(p)
        if actual!=expected_sha:raise ValueError(f"Owner original source hash changed {code}")
        record={"id":code,"title":title,"authors_or_editors":authors,
          "edition":edition,"input_file_type":p.suffix.lower(),"owner_document_basename":p.name,
          "source_bytes":p.stat().st_size,"source_sha256":actual,
          "intake_role":role,"interpretation_restriction":limitation,
          "availability":"verified_readable_owner_local_not_redistributed",
          "has_been_read_in_full":False,
          "source_provenance_next_reading_windows":SOURCE_WINDOWS[code],
          "actual_forward_blinded_real_human_predictions":0}
        if p.suffix.lower()==".pdf":
            n=pages(p)
            if n!=page_expect:raise ValueError(f"Original PDF page count changed: {code} {n}")
            record["PDF_pages"]=n
            record["text_layer_verification"]="pdftotext extracted: short targeted source window only"
        else:
            record["epub_structure"]=epub_scan(p)
        if role=="FICTION_NOT_THE_DRESDEN_CODEX":
            record["include_in_scholarly_original_source_counts"]=False
            record["availability"]="verified_owner_local_fiction_EXCLUDED_from_source"
        else:
            record["include_in_scholarly_original_source_counts"]=False # not read/extracted yet
        records.append(record)
    doc={
      "schema":"MAYA_OWNER_LOCAL_BOOK_SOURCE_INTAKE_V1",
      "date":"2026-10-22","parent_root_goal_status":"OPEN",
      "source_library_location_hint":"~/Documents/astrology; no user-specific absolute locator committed",
      "copyright_originals_in_Git_or_archive":False,
      "total_input_files":len(records),"research_sources_usable_for_next_reading":4,
      "fiction_omitted_from_original_sources":1,
      "books_fully_read_or_complete":0,
      "published_original_Maya_predicate_rules":0,
      "Maya_date_conversion_algorithm_verified_against_independent_oracle":False,
      "Maya_regional_daykeeper_meaning_collated":False,
      "correlation_policy":"UNDECIDED: compare GMT 584283, 584285 (plus documented alternatives); no retrofit using participant",
      "source_regions_not_interchangeable":["lowland Postclassic Yucatec codices","K'iche' Momostenango contemporary practice",
                                        "Mesoamerican general astronomy","Mesoamerican Aztec calendar"],
      "historical_source_claims_not_real_human_data":True,
      "input_sources":records,
      "online_original_manuscript_facsimiles_to_consult":PRIMARY_FACSIMILES,
      "real_human_blinded_predictive_validations":0,
      "runtime_astrology_rule_promotions":0
    }
    args.out.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"inventory_path":str(args.out),"files":len(records),"research_files":4,
          "fiction_excluded":1,"SHA256":sha(args.out)},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
