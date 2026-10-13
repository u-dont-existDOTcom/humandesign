"""Read-only, source-image-first changed-item review stages A and B.

These are NOT blind first passes: prior independent reports are deliberately
provided only after original-image reinspection and corrected rules.
"""
from pathlib import Path
import json,shutil,hashlib
B=Path(__file__).resolve().parents[1]
OUT=Path("/mnt/hdd/home/joel/ai-source-review")
R=json.loads((B/"RULES.json").read_text())
assert R["record_count"]>=200
for label,lo,hi in (("A",336,345),("B",344,353)):
    stage=OUT/f"b02s-changed-{label.lower()}-20261013"
    assert not stage.exists(),("stage exists, do not duplicate review",stage)
    (stage/"source_images").mkdir(parents=True)
    for pg in range(lo,hi+1):
        shutil.copy2(B/"evidence"/f"pdf-{pg}.png",stage/"source_images"/f"pdf-{pg}.png")
    shutil.copy2(B/"evidence/errata-888.png",stage/"source_images/errata-888.png")
    subset=[x for x in R["rules"] if any(lo<=z<=hi for z in x["source_locator"]["pdf_pages"])]
    (stage/"CORRECTED_RULES.json").write_text(json.dumps({"pages":[lo,hi],"records":subset},ensure_ascii=False,indent=2)+"\n")
    shutil.copy2(B/"independent_review"/f"OPUS_{label}_INITIAL.md",stage/"INITIAL_INDEPENDENT_REVIEW.md")
    shutil.copy2(B/"ERRATA_COLLATION.json",stage/"ERRATA_COLLATION.json")
    shutil.copy2(B/"RULES_SOURCE_ORDER.json",stage/"RULES_SOURCE_ORDER.json")
    request=f"""This is a SECOND-PASS SOURCE-FIDELITY review after your initial independent image review. In this run the historical 1647 printed pages are PRIMARY authority; this is not a study of predictive validity.

1. Inspect all original images source_images/pdf-{lo}.png through pdf-{hi}.png and errata-888.png FIRST, before reading the corrected rules. Rebuild the major headings, conditions, exceptions and negations from the images.
2. Read CORRECTED_RULES.json, {len(subset)} source-localized records covering this page span. Do not assume the corrections are right merely because they were labelled repairs. Read the record text and pages. Source IDs may appear out of numerical order because newly detected original clauses have added end-of-batch IDs; source reading order is in RULES_SOURCE_ORDER.json.
3. Read INITIAL_INDEPENDENT_REVIEW.md (your first review findings) and check every material error you previously reported. Classify each original issue as CORRECTED, STILL_WRONG or UNVERIFIABLE, citing a short printed phrase and exact PDF/printed page where material. Check for NEW major misreadings that slipped through. The original text contains sensitive historical norms, but you are evaluating their accuracy, not endorsing or recommending them.
4. Check original-volume ERRATA_COLLATION.json. Printed305 line22 deletes a conjunction glyph; printed306 line26 'undertaken'; printed307 line28 'for Sun and Mars'; printed312 line17 'it is no good'; printed315 line7 South Node and line10 'seventh'. Distinguish verified print vs ambiguous body/glyph and avoid invented certainty.
5. Pay particular attention to negation, forced vs voluntary relations, free will, false-accusation exceptions, house/gender directions, original word 'unwillingly' p304, opposite love direction p305 vs p317, p311 Capricorn glyph, temporal lunar aspect, and missing original clauses/headings. Report ALL outstanding HIGH/MEDIUM errors in this source window with record ID and narrow source-cited correction, plus new errors. Do not re-write records directly.
Return: images/pages inspected, number corrected records inspected, FIRST-REVIEW FINDINGS RESOLUTION TABLE (group if numerous but name all unresolved IDs), new source issues, strongest remaining risk, and final label REPAIR_REQUIRED or SOURCE_FIDELITY_ACCEPTABLE_WITH_RETAINED_UNCERTAINTY or REVIEW_INCOMPLETE. The first review is independent; this follow-up is an informed changed-item audit, do not describe it as a second blind independent first pass."""
    (stage/"REQUEST.md").write_text(request)
    hashes=[{"file":str(p.relative_to(stage)),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(stage.rglob("*")) if p.is_file()]
    doc={"review":"B02s changed-item adjudication","window":label,"pages":[lo,hi],"records":len(subset),
         "model":"claude-opus","effort":"max","max_budget_usd":4,
         "initial_reviewer_report":f"OPUS_{label}_INITIAL.md",
         "inputs":hashes}
    (B/"independent_review"/f"CHANGED_INPUT_{label}.json").write_text(json.dumps(doc,indent=2)+"\n")
    print("STAGED",label,len(hashes),"files",len(subset),"records")
