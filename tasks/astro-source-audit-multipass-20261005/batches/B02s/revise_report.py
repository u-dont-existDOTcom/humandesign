"""Reconcile historical report with the corrected source and original-volume errata."""
from pathlib import Path
B=Path(__file__).resolve().parent
s=(B/"recovery/original_draft/AUDIT_REPORT.md").read_text()
def change(old,new):
 global s
 if s.count(old)!=1:raise AssertionError((old[:100],s.count(old)))
 s=s.replace(old,new)
change("B02s historical source-documentary audit draft, 13 October 2026.",
       "B02s corrected historical source-documentary candidate, 13 October 2026. Initial drafts were NOT accepted.")
change("whereas seventh lord applying to first is treated as more voluntary/easy for the sought party.",
       "whereas a subsequent printed p304 passage calls the sought party's assent **'unwillingly'**. That word conflicts with p303's goodwill language; the original volume supplies no p304 erratum. The original reading is retained rather than silently changed to 'willingly'.")
change("They separately consider seventh/first application by sextile/trine, Moon–Venus with dignity and swift lunar movement, Venus–Sun configurations, and the difference between cadent lack of regard (early hope but failure) and angular aspect relationships that may overcome initial difficulties.",
       "They begin with an ascendant-lord application to seventh lord **without a stated aspect-type restriction** (and a printed marginal reverse-application alternative). The Moon–Venus rule makes **Venus strong, increasing in motion and dignified**, with the Moon likewise dignified. Venus beholding Sun, Sun dignified in ascendant **AND Sun beholding its own dispositor** form a three-part compound rule. Another passage describes **an existing application with BOTH the applying and applied-to planets cadent** and possibly unseen by their own lords—hope at first, then delay and failure. The angular case separately preserves named Sun, Venus, Moon, both house lords and consent.")
change("The source also distinguishes **trine/sextile and other easy connections** from conjunction, square and opposition involving much ado, and repeatedly gives reception a moderating role.",
       "The source also distinguishes **trine/sextile** from harder **square or opposition** and repeatedly gives reception a moderating role. **The original printed p305 conjunction glyph in that difficulty list is explicitly DELETED by the same-volume erratum.** The primary source image remains unchanged; the correction is recorded in ERRATA_COLLATION.json.")
change("the alleged disposition of a partner through Moon/Venus/Mars/Jupiter",
       "the attributed disposition of a partner through Moon/Venus and **Sun trine/sextile Saturn (wise and painstaking/diligent) versus Sun with Jupiter (honest)**")
change("whether either ruler is afflicted or near an eighth house",
       "and whether either ruler is afflicted or near the **lord of the eighth house**")
change("It quotes an *Arabick Aphorisme* with specific zodiacal degree rules but includes a prominent marginal caution **not to credit it without the consent/concurrence of other significators**.",
       "It quotes an *Arabick Aphorisme* with an explicitly scoped **17° Sagittarius to the beginning of Capricorn** range, and another referring to the **first twelve degrees of Capricorn**, NOT Virgo; that latter one offers three extreme alternative outcomes without a case observation. The original printed margin warns **not to credit it without the consent/concurrence of other significators**.")
change("The late **'If a Marriage shall be perfected or no'** subsection restates the first-house lord/Moon and seventh lord.",
       "The late **'If a Marriage shall be perfected or no'** subsection restates the first-house lord/Moon and seventh lord, expressly adding **'if the querent please' and 'we doe suppose a freedome of will in this nature'** to the claimed completion. Nothing in a horoscope substitutes for actual, free consent.")
change("These are **unvalidated and potentially harmful allegations**, no substitute for genetic testing or evidence about a child's actual parentage.",
       "The source gives these as **unvalidated, potentially harmful allegations**, explicitly limited to a fallback **'if none of these things be'** before mere BEHOLDING of fifth house/lord and hedged as **'there may be just suspition'**, with original word **'stuprated'** not silently translated to a modern legal category. Nothing substitutes for genetic evidence of actual parentage.")
change("Their body-line targets and some printed planetary-glyph tokens are not yet confidently resolved.",
       "They have been collated as six specific directions: **p305 delete conjunction**, p306 read *undertaken*, p307 read *for Sun and Mars* (copy-glyph uncertainty retained), **p312 read 'it is no good'**, **p315 read South Node** (body glyph blotted), and **p315 read 'seventh'**. Several body-line identifications are qualified; none authorizes altering original image bytes.")
needle="## Same-volume errata and admitted limitations"
section="""## Two independent first-pass source reviews and corrected units

Separate fresh image-first reviewers examined original PDF336–345 and PDF344–353 respectively, with errata888 in both stages. Their page ranges overlap deliberately but **neither reviewer read the entire 18-page chapter alone**. They reported 38 and 53 issues respectively. The defects included a wrong **'unwillingly' vs 'willingly'** word on printed304, Moon in **tenth rather than seventh**, the erased conjunction symbol on printed305, a false Sun/Mars personality pairing instead of **Sun–Saturn/Sun–Jupiter**, the Capricorn-vs-Virgo Arabic sign mistake, and several missing source **denials**, **non-consent qualifications**, a warning about **slander**, and a **free-will** proviso. The draft also wrongly substituted benevolent translation of light for the *evil* interposing/prohibiting planet in the marriage-hindrance passage. All high-priority issues have source-localized corrective records. The two reviewers' raw diagnostic files, original draft and a machine-readable patch ledger are preserved separately.

This corrected candidate contains **216 source-only units**, R1921–R2136: 187 original draft IDs retained for audit traceability, **82 distinct original records repaired**, and **29 separately indexed clauses/sections recovered**. Because recovered clauses were assigned later IDs, RULES_SOURCE_ORDER.json establishes actual source reading sequence. These numbers are **documentary units**, not historical couples, observed successes or predictive confidence. Some source contradictions remain unresolved: the wording about assent on pp303–304 and Lilly's later reversal of who loves more on printed305 versus317 are both preserved, not harmonized. The historical partner-role, power, paternity and personal-conduct assumptions are not endorsed. Changed-item source review remains a separate final acceptance boundary.

"""
if s.count(needle)!=1:raise AssertionError("marker")
s=s.replace(needle,section+needle)
s=s.replace("The original body witnesses and errata instructions are therefore preserved **separately**; none is silently rewritten.",
            "The original body witnesses and errata instructions are preserved **separately**; none is silently rewritten.")
(B/"AUDIT_REPORT.md").write_text(s)
print("REPORT_REVISED",len(s.split()),"words",len(s),"bytes")
