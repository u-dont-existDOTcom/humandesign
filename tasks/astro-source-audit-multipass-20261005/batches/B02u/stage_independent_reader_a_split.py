"""Fresh, independent image-first reviews of author window A1/A2, no producer report."""
from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).resolve().parent
OUT=Path.home()/"ai-source-review"
for w,lo,hi in [("A1",364,366),("A2",366,369)]:
    src=B/f"SOURCE_READER_{w}.json"
    d=json.loads(src.read_text())
    assert d["window"]==w and d["original_pdf_pages_read"]==list(range(lo,hi+1))
    stage=OUT/f"b02u-independent-{w.lower()}-20261013"
    assert not stage.exists(),f"Existing review, do not overwrite: {stage}"
    (stage/"source_images").mkdir(parents=True)
    for n in list(range(lo,hi+1))+[888]:
        f="errata-888.png" if n==888 else f"pdf-{n}.png"
        shutil.copy2(B/"evidence"/f,stage/"source_images"/f)
    shutil.copy2(src,stage/"CANDIDATE.json")
    prompt=f"""# Independent image-first review of William Lilly 1647, window {w}

Role: external original-source critic. A DIFFERENT model authored CANDIDATE.json. You have only authentic 1647 original page images in source_images/, the candidate, and this prompt. Work sandbox READ-ONLY. Read all {hi-lo+1} page images (PDF{lo} through PDF{hi}, printed {lo-34} through {hi-34}), IN ORDER, including page dividers/marginalia, plus the full errata-888.png image BEFORE reading CANDIDATE.json. Reconstruct your own headings/clauses first. Then check EACH candidate unit, its exact glyph, actor, house/sign, application/separation direction, AND/OR, aspect/reception, source-vs-errata, condition, exception, and later handwritten mark. Catalogue EVERY material omission, not a sample. An original reading on page366 overlaps two subwindows and may be duplicated; this is a source fidelity review, not counting source units.

Special start scope: on PDF364 start BELOW 'Of a Thief and Theft', not the preceding already accepted fugitive material. Special ending: preserve all PDF369 continuations, not material from PDF370. The page-366 turn has antecedents on PDF365; do not invent antecedents for ambiguous 'his' pronouns. Errata PDF888 includes corrections to printed p335,336 and other pages; a damaged page locator must not be asserted definite. No modern real-world criminal identity/custody inference is warranted.

Return one machine-readable JSON object ONLY, no code fencing:
{{"window":"{w}","role":"FRESH_INDEPENDENT_IMAGE_FIRST_REVIEW","pages_read":{list(range(lo,hi+1))},"errata_read":true,
"candidate_units_checked":0,"verdict":"FINDS_ERROR|NO_MATERIAL_ERRORS_FOUND|REVIEW_INCOMPLETE",
"findings":[{{"id":"F1","severity":"HIGH|MEDIUM|LOW","pdf_page":{lo},"candidate_ids":["..."],"source_short_quote":"a genuine short print phrase or glyph","defect":"...","narrow_correction":"...","confidence":"high|medium|low"}}],
"missing_units":[{{"pdf_page":{lo},"source_short_quote":"...","normalized_statement":"...","necessary_prerequisites":"..."}}],
"uncertainties":[{{"pdf_page":{lo},"issue":"...","preserve_unresolved":true}}],
"complete_page_coverage":"which exact pages and source sections were read, and excluded page portions"}}.
If you cannot actually read original images, return REVIEW_INCOMPLETE. Textual sourcing only, NOT a test of whether astrology is true or any person is a thief.
"""
    (stage/"REQUEST.md").write_text(prompt)
    files=[p for p in stage.rglob("*") if p.is_file()]
    meta={"window":w,"review_type":"FRESH_INDEPENDENT_IMAGE_FIRST",
          "full_original_1647_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
          "files":[{"name":str(f.relative_to(stage)),"size":f.stat().st_size,
                    "sha256":hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(files)]}
    (B/f"INDEPENDENT_A_{w}_INPUT.json").write_text(json.dumps(meta,indent=2)+"\n")
    print(json.dumps({"window":w,"pages":list(range(lo,hi+1)),"records":len(d["units"]),"staged":len(files)}))
