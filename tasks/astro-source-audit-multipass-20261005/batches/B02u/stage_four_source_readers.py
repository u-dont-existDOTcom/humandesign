"""Parallel read-only source transcription windows for Lilly Chapter L B02u.
Draft agents receive original images only, NOT producer summaries or previous findings.
"""
from pathlib import Path
import json,hashlib,shutil,os
B=Path(__file__).resolve().parent
OUT=Path(os.environ.get("LILLY_REVIEW_STAGING_DIR",str(Path.home()/"ai-source-review")))
ranges={"A":(364,369),"B":(369,373),"C":(373,377),"D":(377,381)}
assert (B/"SOURCE_IMAGE_MANIFEST.json").is_file()
base=json.loads((B/"SOURCE_IMAGE_MANIFEST.json").read_text())
assert len(base["original_images"])==20
for name,(lo,hi) in ranges.items():
 target=OUT/f"b02u-draft-{name.lower()}-20261013"
 assert not target.exists(),("Existing source-author stage; inspect first",target)
 (target/"source_images").mkdir(parents=True)
 for n in range(lo,hi+1):
  f=B/"evidence"/f"pdf-{n}.png"
  assert f.is_file()
  shutil.copy2(f,target/"source_images"/f.name)
 shutil.copy2(B/"evidence/errata-888.png",target/"source_images/errata-888.png")
 prompt=f"""# Original 1647 page-level source transcription — window {name} of B02u

Read ALL original source_images/pdf-{lo}.png through pdf-{hi}.png IN SEQUENCE, plus original errata-888.png, as an independent source reader. You are preparing a **source-exhaustive documentary outline**, not giving modern astrology advice or judging crime. Original printed text outranks your memory, modern sources and OCR. Do not consult any other files or past report. Do not change any files.

Context: William Lilly, Christian Astrology (1647), Book II, Chapter L (printed p330–366). This pass concerns thief-and-theft material printed p{lo-34}–p{hi-34}, original PDF{lo}–{hi}. Phase B02t previously extracted only text ABOVE the heading *Of a Thief and Theft* on PDF364. If this window includes PDF364, start BELOW that heading; exclude *Of a Woman flying from her Husband*. The source project still needs remainder through PDF400 above Chapter LI. If this window includes PDF381, include *Which way the Thief is gone* and stop immediately BEFORE the distinct heading *Of the house of the Thiefe, and the mark thereof*. Pages {369 if name=="B" else 373 if name=="C" else 377 if name=="D" else 364} are shared with adjacent windows, so label source positions accurately rather than discarding overlapping text.

First, inspect every page including left margins, printed headings, catchwords and page continuation. For each logically distinct **source rule OR section heading** produce an entry with all necessary conditions: subject/significator, direction of application/separation, relevant lord or cusp, positive/negative polarity, aspect and sign glyph, exact qualifier, alternative, exception, author uncertainty, page number. Do not collapse opposing/competing methods. Do not invent original glyph or a clinical/criminal finding. Source claims are historical testimony, NOT evidence that people stole goods, commit crimes, have certain bodies, or are recoverable by astrology.

Return one UTF-8 JSON object only (no Markdown fences), shape:
{{
 "window":"{name}",
 "original_pdf_pages_read":[{",".join(str(x) for x in range(lo,hi+1))}],
 "status":"DRAFT_SOURCE_ONLY",
 "complete_page_outline":[{{"pdf_page":364,"printed_page":330,"headings":["exact source heading"],"page_end_catchword":"...","continuation_from_previous":false}}],
 "units":[{{
  "local_id":"{name}001",
  "pdf_pages":[364],
  "section_heading":"exact printed current subsection",
  "kind":"heading|source_conditional|source_exception|source_example|source_worked_chart|source_table|source_quotation",
  "short_original_anchor":"5-18 consecutive words from original source, quote EXACTLY if confident",
  "normalized_historical_statement":"source-only paraphrase retaining subject, polarity and scope",
  "preconditions":["..."],
  "exceptions_and_uncertainty":["..."],
  "confidence":"high|medium|low"
 }}],
 "unresolved_glyphs_or_source_conflicts":[{{"page":364,"issue":"...","importance":"..."}}],
 "stop_boundary_observed":"..."
}}

Target full clause-coverage, even unnumbered headings and historical examples. Avoid brevity that omits conditionals: 30–65 units per 5–6-page window is acceptable. Keep whole units page-local unless a sentence visibly continues across pages; use both pages in those cases. Do not fill in missing words from guessed modern astrology. Keep claims about physical appearance, names, gender and theft explicitly as author conjecture, not identification. Print the exact page count and first/last source headings inspected.
"""
 (target/"REQUEST.md").write_text(prompt)
 files=[p for p in target.rglob("*") if p.is_file()]
 receipt={"batch":"B02u","window":name,"pages":[lo,hi],"review_kind":"FRESH_SOURCE_IMAGE_FIRST_OUTLINE",
          "source_original_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
          "files":[{"name":str(x.relative_to(target)),"bytes":x.stat().st_size,"sha256":hashlib.sha256(x.read_bytes()).hexdigest()} for x in sorted(files)]}
 (B/f"SOURCE_READER_INPUT_{name}.json").write_text(json.dumps(receipt,indent=2)+"\n")
 print(json.dumps({"window":name,"image_count":hi-lo+2,"bytes":sum(x.stat().st_size for x in files)}))
