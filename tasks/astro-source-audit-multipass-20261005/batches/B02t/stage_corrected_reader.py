"""Isolate a NEW blind source-reading pass after first review corrections.

This is diagnostic source fidelity, not medical/astral prediction validation.
Prior review findings and authoring report are withheld from this evaluator.
"""
from pathlib import Path
import hashlib,json,os,shutil
B=Path(__file__).resolve().parent
D=json.loads((B/"PHASE1_RULES_DRAFT.json").read_text())
assert D["record_count"]==162 and D["provisional_end"]=="R2299"
root=Path(os.environ.get("LILLY_REVIEW_STAGING_DIR",str(Path.home()/"ai-source-review")))
for k,lo,hi in (("A",353,359),("B",359,364)):
 stage=root/f"b02t-phase1-recheck-{k.lower()}-20261013"
 assert not stage.exists(),("Stage exists; do not overwrite",stage)
 images=stage/"source_images"
 images.mkdir(parents=True)
 for n in list(range(lo,hi+1))+[888]:
  name=f"pdf-{n}.png" if n!=888 else "errata-888.png"
  shutil.copy2(B/"evidence"/name,images/name)
 subset=[r for r in D["rules"] if any(lo<=x<=hi for x in r["source_locator"]["pdf_pages"])]
 ids=sorted({x["record_number"] for x in subset})
 payload={"batch":"B02t","phase":"1_OF_CHAPTER_L","review_window":k,
          "expected_original_pdf_pages":list(range(lo,hi+1)),
          "candidate_record_count":len(subset),"records":subset,
          "source_only":True,"all_chapter_l_complete":False}
 (stage/"CANDIDATE_RULES.json").write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n")
 prompt=f"""# New, clean-context post-correction source-fidelity review B02t window {k}

First independently read EVERY original 1647 source image in source_images/ (PDF{lo} through PDF{hi} plus original errata-888). These are authoritative. Build a COMPLETE clause-by-clause outline, with each heading, margin note, planet/house glyph, application/separation direction, conditions, alternatives, exceptions, modality, and page-continuing phrase, before opening CANDIDATE_RULES.json. This is a new fresh reviewer, not to be informed of any previous model reviews. No authoring report, prior findings or discussion is provided.

Then check all {len(subset)} candidate source units in CANDIDATE_RULES.json. They are normalized editorial paraphrases, not original 1647 quotations, based on William Lilly's Christian Astrology chapter L. Note exactly which page and record each original argument supports, flag duplicate content, wrong actor, changed polarity, added/dropped premises, errata contradictions, missing printed headings or meaning-changing omissions. Give conservative source-bound corrections, including short direct original wording/glyph and line as visible where material. Note any missing source units not in candidate. If a body line is ambiguous, label that ambiguity rather than fixing it from guess.

The *complete* Chapter L extends PDF353 BELOW XLIX divider through PDF400 ABOVE LI divider. This B02t first phase includes ONLY PDF353 lower through PDF364 immediately ABOVE the distinct 'Of a Thief and Theft' heading. PDF364 physical original image is needed for second-phase continuation; do not count its theft body in first phase. Original same-volume errata leaf PDF888 provides printed p324 and p330 corrections, separate from source body. Leave original source pages unchanged. No observed persons, ownership, captivity, animal recovery, health, theft or forecasts may be inferred from rules.

Report material findings with ID, severity, PDF and printed page, original phrase, candidate ID and precise repair. Confirm count {len(subset)} actually checked and {hi-lo+1} original content images plus errata read. Distinguish potentially redundant metadata from a new independent rule. End with FINDS_ERROR / NO_MATERIAL_ERRORS_FOUND / REVIEW_INCOMPLETE. Independent source fidelity only, not predictive validity.
"""
 (stage/"REQUEST.md").write_text(prompt)
 files=[p for p in stage.rglob("*") if p.is_file()]
 m={"batch":"B02t","window":k,"type":"FRESH_NEW_CONTEXT_POST_CORRECTION_SOURCE_REVIEW",
    "not_informed_about_previous_findings":True,"count":len(subset),"id_min":min(ids),"id_max":max(ids),
    "inputs":[{"path":str(p.relative_to(stage)),"bytes":p.stat().st_size,
               "sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]}
 (B/"independent_review"/f"RECHECK_INPUT_{k}.json").write_text(json.dumps(m,indent=2)+"\n")
 print(json.dumps({"window":k,"records":len(subset),"files":len(files),"images":hi-lo+2,
                   "reviewer_no_producer_or_old_finding_context":True}))
