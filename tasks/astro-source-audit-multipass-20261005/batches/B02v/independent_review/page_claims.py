"""Read-only page-keyed listing of provisional B02v editorial claims, for source-image review."""
import json,sys
from pathlib import Path
B=Path(__file__).resolve().parents[1]
doc=json.loads((B/"RULES_DRAFT.json").read_text())
pages={int(s) for s in sys.argv[1:]}
if not pages: raise SystemExit("Usage: page_claims.py PDF_PAGE [PAGE...]")
for r in doc["records"]:
    pg=r["source_locator"]["pdf_pages"]
    if not pages.intersection(pg): continue
    print(r["id"].split(".")[-1]+" | PDF"+",".join(map(str,pg))+" | "+r["source_record_kind"])
    print("  "+r["source_statement"])
    if len(r["preconditions"])>1: print("  IF: "+" ; ".join(r["preconditions"]))
