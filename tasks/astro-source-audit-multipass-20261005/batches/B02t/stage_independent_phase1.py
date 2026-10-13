"""Freeze two separate independent source-image reviews; no producer summary supplied.
Runs only staging. Reviewer itself must be invoked after this.
"""
from pathlib import Path
import json,hashlib,shutil,os
B=Path(__file__).resolve().parent
D=json.loads((B/"PHASE1_RULES_DRAFT.json").read_text())
assert D["record_count"]==129 and D["all_chapter_L_complete"]==False
root=Path(os.environ.get("LILLY_REVIEW_STAGING_DIR",str(Path.home()/"ai-source-review")))
for group,lo,hi in [("A",353,359),("B",359,364)]:
 dest=root/f"b02t-phase1-{group.lower()}-20261013"
 assert not dest.exists(),("Would overwrite frozen review inputs",dest)
 images=dest/"source_images";images.mkdir(parents=True)
 for n in [*range(lo,hi+1),888]:
  name=f"pdf-{n}.png" if n!=888 else "errata-888.png"
  shutil.copy2(B/"evidence"/name,images/name)
 subset=[x for x in D["rules"] if lo<=min(x["source_locator"]["pdf_pages"])<=hi]
 # Includes page359 in both for source-boundary readback.
 assert subset
 j={"batch":"B02t","phase":"1","review_window":group,"pdf_window":[lo,hi],
    "full_1647_source_sha256":D["rules"][0]["source_full_pdf_sha256"],
    "source_count":len(subset),"records":subset,
    "all_source_accepted":False,"predictions_not_tested":True}
 (dest/"CANDIDATE_RULES.json").write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n")
 request=(
  f"# Fresh image-first source review B02t/phase1 window {group}\n\n"
  f"Read all original source PNG images in source_images first, original PDF{lo} through PDF{hi} "
  "(printed pages PDF-34) plus errata-888.png. Reconstruct a complete outline with headings, "
  "clause conditions, exceptions, and continuations *before* opening CANDIDATE_RULES.json. "
  "Then compare each normalized candidate source record to the source page it cites. "
  "The original 1647 source is William Lilly, Christian Astrology (Wellcome b30338724) "
  "and its full scanned PDF SHA256 is 2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b. "
  "No generated report, second-review diagnosis or extraction justification supplied. "
  "No modifications are allowed. This is documentary source fidelity only, not a test of astrological truths.\n\n"
  "Key source priorities: preserve direction of lunar separation/application (self-straying vs theft), "
  "fall-back to alternative house rulers, special exceptions, 12th vs 8th death/custody conditions, "
  "actual sign symbols, source's nonstandard distance units, contradictory sign/timing rules, "
  "and scope of animal vs fugitive vs inert goods. Never claim a prediction worked. "
  "Chapter L begins PDF353 below the Chapter XLIX divider; the bounded first phase ENDS on PDF364 "
  "IMMEDIATELY ABOVE 'Of a Thief and Theft' heading (do not evaluate material below heading except "
  "to confirm boundary). B02t covers only a part of the entire Chapter L; source continues to PDF400 "
  "above the Chapter LI divider. Identify omitted source passages even if candidate has no record. "
  "On errata page look for printed pages319–330; give only original same-volume correction tokens "
  "and do not silently modify body text. Later handwritten margin not authorially authenticated.\n\n"
  f"For each material finding give code, severity, original PDF page, short original wording/glyph, "
  "affected ID or missing source unit, and minimal repair. Distinguish sure error from uncertainty. "
  f"Confirm image pages read and number of candidate units checked (this window has {len(subset)}). "
  "End FINDS_ERROR / NO_MATERIAL_ERRORS_FOUND / REVIEW_INCOMPLETE. "
  "Do not use external outcome histories, internet, or personal astrology case files.\n"
 )
 (dest/"REQUEST.md").write_text(request)
 files=[p for p in dest.rglob("*") if p.is_file()]
 manifest={"review_window":group,"source_page_window":[lo,hi],
           "input_files":[{"path":str(f.relative_to(dest)),"bytes":f.stat().st_size,
                            "sha256":hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(files)],
           "reviewer_mode":"fresh independent read-only original-image-first"}
 (B/"independent_review").mkdir(exist_ok=True)
 (B/"independent_review"/f"INPUT_{group}.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps({"review":group,"pages":hi-lo+1,"source_units":len(subset),"files":len(files),
                   "source_only":True}))
