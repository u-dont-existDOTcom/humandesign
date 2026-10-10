"""Index every report paragraph and data-table row for diagnostic claim review."""
import hashlib,json,re
from pathlib import Path
p=Path(__file__).resolve().parent
report=p/'AUDIT_REPORT.md'; text=report.read_text(); claims=[]; section='Title'
for block in re.split(r'\n\s*\n',text.strip()):
    if block.startswith('#'):
        section=block.strip('# ').strip(); continue
    if block.startswith('|'):
        lines=block.splitlines()
        for line in lines[2:]:
            claims.append({'id':f'CL{len(claims)+1:03d}','section':section,'claim_type':'table_figure_or_source_content','claim':line,'table_header':lines[0],'anchor':'Surrounding report source citation and corresponding packet table/register','checked_by_producer':'Source/inventory readback; checker must verify row with surrounding source scope.'})
    else:
        refs=re.findall(r'\[(?:Source|Evidence|Calculation|Figure|Boundary witness|XXXIX|XL|XLII|XLIII|XLI)[^\]]*\]',block)
        claims.append({'id':f'CL{len(claims)+1:03d}','section':section,'claim_type':'source_content_and_explicitly_labelled_inference' if refs else 'artifact_scope_or_release_requirement','claim':block,'anchor':refs or ['Named artifact, source identity or explicit release requirement.'],'checked_by_producer':'Whole paragraph including qualifications. Any false subclaim fails this unit; checker may add omissions.'})
ledger={'batch':'B02j','report':'AUDIT_REPORT.md','report_sha256':hashlib.sha256(report.read_bytes()).hexdigest(),'claim_count':len(claims),'granularity':'Each prose paragraph and each non-header table row is a unit; all propositions inside a paragraph must pass. Rows inherit section and following source citations.','review_instruction':'Return PASS/FAIL for every unit with anchors and add missed claims. Release requirements are not assertions that publication/delivery already occurred.','claims':claims}
(p/'CLAIM_LEDGER.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'claim_units':len(claims),'report_sha256':ledger['report_sha256']}))
