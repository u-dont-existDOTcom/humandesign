"""Split original source window A by source-page-turn to avoid transport size failures."""
from pathlib import Path
import hashlib,json,shutil
B=Path(__file__).resolve().parent
STAGE=Path.home()/"ai-source-review"
for name,lo,hi in [("A1",364,366),("A2",366,369)]:
 path=STAGE/f"b02u-draft-{name.lower()}-20261013"
 assert not path.exists()
 (path/"source_images").mkdir(parents=True)
 for n in range(lo,hi+1):
  src=B/"evidence"/f"pdf-{n}.png";assert src.is_file()
  shutil.copy2(src,path/"source_images"/src.name)
 shutil.copy2(B/"evidence/errata-888.png",path/"source_images/errata-888.png")
 prompt=f"""Source-exhaustive read-only transcription of William Lilly, Christian Astrology 1647, original PDF{lo}–{hi} (printed{lo-34}–{hi-34}), plus original errata leaf. This is a subordinate IMAGE ONLY read. Parent already fetched current UDA and HumanDesign AGENTS.md; do not fetch web or reload repository instructions. Read attached ORIGINAL source images in order; original printed page/heading/glyph priority over memory or OCR.

This is window {name}, replacing part of an earlier failed six-page upload. No prior producer notes or model findings are provided. If reading PDF364, begin BELOW the heading 'Of a Thief and Theft' (earlier content already accepted). If reading PDF369, it overlaps an adjacent window, so include text accurately. Every visibly named/unnumbered heading, separate significator priority, planetary aspect and relation, exception, competing method, quoted authority, worked example or table deserves its own source unit. Historical claims about theft, gender, appearance or suspects are not verification of crimes.

Return ONLY one valid JSON object with fields:
{{
 "window":"{name}",
 "original_pdf_pages_read": [{",".join(str(p) for p in range(lo,hi+1))}],
 "status":"DRAFT_SOURCE_ONLY",
 "complete_page_outline":[{{"pdf_page":{lo},"printed_page":{lo-34},"headings":["exact heading"],"page_end_catchword":"...", "continuation_from_previous":false}}],
 "units":[{{"local_id":"{name}001","pdf_pages":[{lo}],"section_heading":"...","kind":"heading|source_conditional|source_exception|source_example|source_worked_chart|source_table|source_quotation",
 "short_original_anchor":"5-18 EXACT consecutive source words where legible",
 "normalized_historical_statement":"Precise historical claim and role/direction/polarity, not a real-world inference",
 "preconditions":["..."],"exceptions_and_uncertainty":["..."],"confidence":"high|medium|low"}}],
 "unresolved_glyphs_or_source_conflicts":[{{"page":{lo},"issue":"...","importance":"..."}}],
 "stop_boundary_observed":"..."
}}
Cover all {hi-lo+1} original body pages COMPLETELY. Include page-overlapping sentences with both source pages when visible; do not invent illegible glyphs. Continuations and all operative conditions are essential. No owner participant data or predictive claim.
"""
 (path/"REQUEST.md").write_text(prompt)
 receipt={"name":name,"type":"SOURCE_IMAGE_FIRST_REPLACEMENT_SPLIT",
          "source_full_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
          "original_pdf_pages":[lo,hi],
          "files":[{"name":str(f.relative_to(path)),"bytes":f.stat().st_size,
                    "sha256":hashlib.sha256(f.read_bytes()).hexdigest()}
                   for f in sorted(path.rglob("*")) if f.is_file()]}
 (B/f"SOURCE_READER_INPUT_{name}.json").write_text(json.dumps(receipt,indent=2)+"\n")
 print(json.dumps({"window":name,"pages":hi-lo+1,"bytes":sum(x["bytes"] for x in receipt["files"])}))
