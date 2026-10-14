"""Freeze independent original-image-first page-window source readers.

The five readers receive original scan PNGs only, not any producer summary,
previous review, accepted record, participant data, or outcome key.
"""
from pathlib import Path
import json,hashlib,shutil,os
B=Path(__file__).resolve().parent
DEST=Path(os.environ.get("LILLY_REVIEW_STAGING_DIR", str(Path.home()/"ai-source-review")))
RANGES={"A":(381,385),"B":(385,389),"C":(389,393),"D":(393,397),"E":(397,400)}
manifest=json.loads((B/"SOURCE_IMAGE_MANIFEST.json").read_text())
assert [x["pdf_page"] for x in manifest["images"] if x["pdf_page"]!=888]==list(range(381,401))
source_sha="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
assert manifest["original_pdf_sha256"]==source_sha
for w,(first,last) in RANGES.items():
    target=DEST/f"b02v-first-{w.lower()}-20261014"
    assert not target.exists(), ("Existing source-reader attempt: do not overwrite",str(target))
    (target/"source_images").mkdir(parents=True)
    for n in range(first,last+1):
        src=B/"evidence"/f"pdf-{n}.png"
        assert src.is_file(),src
        shutil.copy2(src,target/"source_images"/src.name)
    shutil.copy2(B/"evidence/errata-888.png",target/"source_images/errata-888.png")
    note=f"""# Fresh original source-first documentary reader — window {w}

You are independent from every other window and the producer. First read in order ALL original source_images/pdf-{first}.png through pdf-{last}.png and source_images/errata-888.png. This is the **original William Lilly Christian Astrology (1647), Book II Chapter L**, source witness Wellcome b30338724. The source's typographic columns, printed headings, side notes, zodiac/planet glyphs, footnotes, tables, and transitions are the authority. No producer record or prior interpretation is provided.

Scope: the last portion of Chapter L about a thief, locations/doors of houses, missing goods, recovery, suspicion and related historical topics, printed pp{first-34}–{last-34} (original PDF{first}–PDF{last}). The previous accepted B02u ended on original PDF381 **before** the separate heading 'Of the house of the Thiefe, and the mark thereof'; window A MUST begin **below that heading**, not copy above-division 'Which way the Thief is gone' or earlier work. Window E MUST stop on PDF400 **before** the horizontal divider introducing Chapter LI, 'Of Battell, Warre, or other Contentions'. Other windows share one overlapping physical page with a neighbour: preserve accurate source page and line/heading scope so that identical rules can be deduplicated. Do not omit page-spanning sentences.

TASK: produce a source-exhaustive editorial evidence inventory, NOT a clinical, legal, criminal or predictive finding. For each distinct heading, source conditional, exception, alternate method, worked example and original printed table, record every necessary planet/house/aspect/significator, sign modality, direction of application or separation, subject, polarity, reception, temporal qualifiers, exceptions, exact original threshold and any source uncertainty. Treat unqualified claims about a thief's identity, gender, age, name, body, guilt, relationships or property as **historical assertions ONLY, never real-world identification**. Each original numerical table needs a source-image evidence row even if full cellwise diplomatic transcription is not possible. Do not fabricate unreadable glyphs.

OUTPUT exactly a UTF-8 JSON object, with no markdown fences:
{{
 "window":"{w}",
 "original_pdf_pages_read":[{",".join(str(x) for x in range(first,last+1))}],
 "status":"SOURCE_IMAGE_FIRST_DOCUMENTARY_DRAFT",
 "page_outline":[{{"pdf_page":{first},"printed_page":{first-34},"headings":["original printed heading"],"opening": "short anchor", "last_body_or_catchword": "short anchor", "continues_across_page": false}}],
 "units":[{{
    "local_id":"{w}001", "pdf_pages":[{first}], "section_heading":"current printed subsection",
    "kind":"heading|source_conditional|source_exception|source_example|source_table|source_quotation|source_worked_case",
    "short_original_anchor":"5–18 consecutive ORIGINAL words if legible; do not put invented quotes here",
    "normalized_historical_statement":"faithful, complete editorial paraphrase with direction and role",
    "preconditions":["all stated conditions"],
    "exceptions_and_uncertainty":["source limits, exceptions, source glyph uncertainty"],
    "confidence":"high|medium|low"
 }}],
 "unresolved_source_readings":[{{"pdf_page":{first},"issue":"...","consequence":"...","importance":"high|medium|low"}}],
 "boundary":{{"start":"...","stop":"..."}},
 "overall_completeness":"FULL_PAGES_READ"
}}

Inspect all pages; provide every nontrivial source condition rather than reducing to summary. At least one independent unit per materially different sentence/claim; expect roughly 35–75 units per window if source has that density, but fidelity outranks count. Restore real original heading names. Identify editorial or handwritten marginal annotations separately from original printed main text. Do not use external sources or files from earlier sessions. Do not open or mutate Git, secrets, other client files, or user data. No factual claim that astrology works is authorized.
"""
    (target/"REQUEST.md").write_text(note)
    files=[p for p in sorted(target.rglob("*")) if p.is_file()]
    receipt={"batch":"B02v","window":w,"source_window":[first,last],
             "source_original_pdf_sha256":source_sha,
             "review_kind":"FIRST_INDEPENDENT_SOURCE_IMAGE_FIRST_DRAFT",
             "files":[{"path":str(p.relative_to(target)),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
    (B/f"SOURCE_READER_INPUT_{w}.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({"window":w,"images":last-first+2,"frozen_input_bytes":sum(p.stat().st_size for p in files)}))
