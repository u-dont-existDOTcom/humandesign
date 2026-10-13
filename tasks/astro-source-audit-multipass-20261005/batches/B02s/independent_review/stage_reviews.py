"""Prepare two blind, read-only original-image-first review windows."""
from pathlib import Path
import json,shutil,hashlib
B=Path(__file__).resolve().parents[1]
D=json.loads((B/"RULES.json").read_text())
OUT=Path(__import__("os").environ.get("LILLY_REVIEW_STAGING_DIR", str(Path.home()/"ai-source-review")))
for label,lo,hi in [("A",336,345),("B",344,353)]:
 stage=OUT/f"b02s-original-first-{label.lower()}-20261013"
 assert not stage.exists(),str(stage)
 (stage/"source_images").mkdir(parents=True)
 for pg in range(lo,hi+1):
  shutil.copy2(B/"evidence"/f"pdf-{pg}.png",stage/"source_images"/f"pdf-{pg}.png")
 shutil.copy2(B/"evidence"/"errata-888.png",stage/"source_images"/"errata-888.png")
 subset=[r for r in D["rules"] if any(lo<=p<=hi for p in r["source_locator"]["pdf_pages"])]
 (stage/"RULES.json").write_text(json.dumps({"batch":"B02s","range":[lo,hi],"records":subset},indent=2,ensure_ascii=False)+"\n")
 prompt=f"""First, inspect all ORIGINAL IMAGES source_images/pdf-{lo}.png through pdf-{hi}.png and errata-888.png, using them as primary evidence, reconstruct the complete original 1647 printed page content and subsection order WITHOUT consulting RULES.json first. Then read RULES.json and review each of its {len(subset)} candidate normalized paraphrases; this is historical source research, NOT clinical or predictive validation. Identify every consequential erroneous/missing premise, negation, direction of lunar application, qualifier, contrast, original-volume erratum, text page-boundary or unnumbered heading that affects semantics. Mark copy glyph uncertainty rather than inventing a repair. Look for missing distinct source clauses not in the extracted records; report page and short exact original phrase for high-confidence findings and indicate any unreviewed regions. Keep apparent questions concerning historical sexuality and gender as unvalidated source claims; preserve explicit consent/force exceptions and warnings about false accusations. Candidate covers Lilly XLIX Marriage only from original PDF336/printed302 BELOW divider through original PDF353/printed319 ABOVE divider. Next Chapter L starts after divider at PDF353. Do not consult author reports or earlier diagnoses. Return independent findings with numbered issue IDs, severity, record IDs, concise source phrases, and proposed narrow correction; end with FINDS_ERROR, NO_MATERIAL_ERRORS_FOUND or REVIEW_INCOMPLETE, explicit number of records and images inspected and limitations. For any missing image or pre-fetched preview, do not pretend to read it."""
 (stage/"REQUEST.md").write_text(prompt)
 manifest={"stage":label,"pages":list(range(lo,hi+1)),"records":len(subset),
   "model_requested":"opus","effort_requested":"max","spend_cap_usd":4,
   "first_pass_independence":"source images before candidate; producer report withheld",
   "files":[{"name":str(f.relative_to(stage)),"sha256":hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(stage.rglob("*")) if f.is_file()]}
 (B/"independent_review"/f"INPUT_{label}.json").write_text(json.dumps(manifest,indent=2)+"\n")
 print(label,"images",hi-lo+2,"records",len(subset),"files",len(manifest["files"]))
