"""Bring phase1 report and handoff into exact agreement with reviewed source packets."""
from pathlib import Path
B=Path(__file__).resolve().parent
def revise(name, pairs, appendix=""):
 p=B/name;s=p.read_text()
 for old,new in pairs:
  assert old in s,(name,old)
  s=s.replace(old,new)
 p.write_text(s+appendix)
common=[("162","168"),("R2299","R2305"),("2,299","2,305"),("3,365","3,371"),("50 retained","56 retained")]
revise("AUDIT_REPORT.md",common+[
 ("129 initially extracted plus 33 additional","129 initially extracted plus 39 additional"),

 ("not a fresh third blind review","not a final blind rereview of the latest corrected records")
],appendix="""

## Two additional image-first source readbacks

Following the initial original-image readers' 49 findings, two **fresh clean-context source readers** read printed pages319–325 and325–330, respectively. Their raw source assessments are retained as OPUS_A_RECHECK.md and OPUS_B_RECHECK.md; each returned FINDS_ERROR for the then-current 162-unit revision. The second round repaired 8th-from-Moon house assignments, the fifth-not-sixth house recovery placement, the precise lunar-application person roles and direction of news versus repentance, cattle impoundment, and original p330 'read or' erratum. Six additional original clauses recovered in this round are separately indexed R2300–R2305. The **final 168-source-unit controller repair has not itself received a further blind reader evaluation**; structural tests are not independent astrological validation.

Across the two rounds, original glyphs and line-break conditions govern over OCR or earlier summaries. Physical images remain unmodified, with uncertainty about original printing, house ambiguities and manuscript annotations retained. Chapter L continues from PDF364 below the 'Of a Thief and Theft' heading all the way through PDF400 above Chapter LI, so this batch does not claim whole-chapter source completeness.
""")
revise("README.md",[("162","168"),("R2299","R2305"),("3,365","3,371"),("233/233","239/239"),("in progress outside Git","completed outside Git; their source findings have been reconciled locally")])
revise("CONTINUE_HANDOFF.md",[("162","168"),("R2299","R2305")])
revise("WORKING_CHECKPOINT.md",[("162","168"),("R2299","R2305"),("50 open","56 open"),("233 distinct","239 distinct"),("staged and launched; pending outcomes","completed; controller corrections applied and final acceptance pending")])
p=B/"SOURCE_FIRST_NOTES.md";p.write_text(p.read_text()+"\n## Post-correction fresh source readers\n\nReader A/B were frozen new-context source-image-first reviews; both found further errors in the 162-record candidate. Controller repairs include Moon-derived eighth, lunar news direction, heavy pound/custody source conditions, printed p330 'read or', and six recovered source clauses. The corrected source inventory is 168 records, with 56 retained limitations. No third final blind rereview; no empirical validation.\n")
print("Updated source report and continuation text for 168 units.")
