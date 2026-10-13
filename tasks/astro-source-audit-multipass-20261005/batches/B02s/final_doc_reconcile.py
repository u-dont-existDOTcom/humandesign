"""Reconcile downstream prose and tests after source review and omitted p318 scope."""
from pathlib import Path
B=Path(__file__).resolve().parent
def sub(name,old,new):
 p=B/name;s=p.read_text()
 assert old in s,(name,old[:75])
 p.write_text(s.replace(old,new))
sub("test_b02s_original_review_regressions.py","test_29_added_recovered_source_clauses","test_30_added_recovered_source_clauses")
sub("test_b02s_original_review_regressions.py",'d["added_missed_original_units"],29','d["added_missed_original_units"],30')
sub("test_b02s_source_structure.py",'U["retained_count"],64','U["retained_count"],68')
sub("README.md","216 units","217 units")
sub("README.md","R1921–R2136","R1921–R2137")
sub("README.md","29 formerly omitted","30 formerly omitted")
sub("CONTINUE_HANDOFF.md","Lilly 2,136","Lilly 2,137")
sub("CONTINUE_HANDOFF.md","R1921–R2136, 216 documentary units","R1921–R2137, 217 documentary units")
sub("CONTINUE_HANDOFF.md","combined **3,202**","combined **3,203**")
sub("CONTINUE_HANDOFF.md","Next candidate ID **R2137","Next candidate ID **R2138")
sub("AUDIT_REPORT.md","**216 source-only units**, R1921–R2136","**217 source-only units**, R1921–R2137")
sub("AUDIT_REPORT.md","**29 separately indexed clauses/sections recovered**","**30 separately indexed clauses/sections recovered**, including the additional printed p318 mistress-or-sweetheart scope")
sub("AUDIT_REPORT.md","Changed-item source review remains a separate final acceptance boundary.","Two informed changed-item source reviews returned errors that have now received further source-specific repairs; final documentary acceptance still requires exact tests and source-provenance receipts.")
report=B/"AUDIT_REPORT.md"
s=report.read_text()
marker="## Same-volume errata and admitted limitations\n"
assert s.count(marker)==1
insert="""## Informed changed-item reviews and subsequent corrections

The two informed source-window reviews examined changes to the original 187-unit draft and additional recovered clauses, rather than constituting fresh blind replications. Their interim verdict was **REPAIR_REQUIRED**. On p310 the first revision had inadvertently deleted a Moon-in-fall / square-or-opposition-with-Saturn-Mars-or-retrograde clause qualified by the Moon beholding the ascendant; it is restored. The man-versus-woman signification on p308 has been repaired, including **Moon with Venus** as only one example for a male querent and **Sun beholding Saturn/Jupiter** when judging the man. The source's p310 **heavy planet** means a ponderous receiver of light, not merely any afflicted receiver. [PDF342,344; R1991,R1992,R2010,R2021; original independent changed-item reviews]

In the text's more sensitive p313–315 allegations, the correction retains an unambiguously **nonconsensual** source alternative, specifies when someone was **deceived** rather than blaming her, and restores the passage saying the hypothetical other man **could not bring her under his yoke**. A further p313 case expressly says a woman **gave no credit** to a tempting advance and that a circulated allegation was **false**. Mars appearing **as lord of the seventh** differs from Mars merely joining the seventh lord. We retain the author's source claims without endorsing them or inferring any actual conduct or relationship. [PDF347–349; R2047,R2064,R2067,R2119,R2120,R2122,R2126]

The source prints on p318 that the separated-partner question may also concern a **mistress or sweetheart**, now separately indexed as R2137 with its source-reading order after the heading R2095. **Neither changed-item reviewer was a blind third review of the final corrected packet.** The original reviewer outputs and each informed readback are separately preserved, and uncertain original glyphs and typographic errata remain stated as limitations; textual acceptance is not predictive validation.

"""
s=s.replace(marker,insert+marker)
report.write_text(s)
p=B/"SOURCE_FIRST_NOTES.md"
p.write_text(p.read_text()+"\n## Two 2026-10-13 informed changed-item review corrections\n\nBoth changed-item Opus reviews finished and independently described residual source-level issues, with no claim they were blind third reviews. The local controller restored omitted lunar-affliction wording, corrected roles of male/female signifiers, retained the printed denial of forced conduct and warnings about false rumours, and distinguished heavy receiving planet from merely afflicted. Original p318 scope is separately R2137. Errata witnesses remain unmodified; no actual marriage or person was verified.\n")
p=B/"WORKING_CHECKPOINT.md"
s=p.read_text()
s=s.replace("29 missing original clauses","30 missing original clauses").replace("216 proposed source-only units R1921–R2136","217 proposed source-only units R1921–R2137").replace("64 explicit uncertainty/limitation records","68 explicit uncertainty/limitation records")
s=s.replace("Two changed-item source reviews in", "Two completed changed-item source reviews in")
s=s.replace("were launched. Do not duplicate a running model call; look for", "completed successfully, were source-reconciled; do not duplicate. Their")
s+= "\n**2026-10-13 continuation:** Both review exit files are 0, corrections are locally applied; source-specific suite after original repairs was 260/260 green. A newly recovered p318 scope unit R2137 increases candidate to 217, and final source regession/claim-ledger/acceptance gates remain in progress. No third blind final model review has occurred. Never claim canonical update before GitHub readback.\n"
p.write_text(s)
print("Reconciled report, continuation and source tests for 217 source units.")
