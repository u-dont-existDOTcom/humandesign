from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).resolve().parent
A=Path(__import__("os").environ.get("LILLY_REVIEW_STAGING_DIR", str(Path.home()/"ai-source-review")))
for x in 'ab':
 p=A/f'b02s-changed-{x}-20261013/review.stdout'
 assert p.is_file() and (p.parent/'review.exit').read_text().strip()=='0'
dest=B/'recovery'/'before_changed_reviews'
dest.mkdir(parents=True,exist_ok=True)
for file in ['RULES.json','UNRESOLVED.json','ERRATA_COLLATION.json','AUDIT_REPORT.md','RULES_SOURCE_ORDER.json']:
 src=B/file
 if src.exists() and not (dest/file).exists():shutil.copy2(src,dest/file)
d=json.loads((B/'RULES.json').read_text())
r={q['record_number']:q for q in d['rules']}
def fix(n,s=None,pre=None,limit=None,kind=None):
 x=r[n]
 if s:x['source_statement']=s
 if pre:x['preconditions']=[pre]
 if limit:x['exceptions_and_evidence_limits']=[limit]
 if kind:x['source_record_kind']=kind
def exc(n,s):
 if s not in r[n]['exceptions_and_evidence_limits']:r[n]['exceptions_and_evidence_limits'].append(s)
fix(1992,"For a man's question Lilly describes the woman by the planet the MOON is with (Venus: fair, slender and pleasant); for a woman's question, the MAN is described by the planet the SUN beholds (Saturn: wise, painful/diligent; Jupiter: honest).","Identify who is asking: Moon-related planet for describing woman when man asks, Sun-related planet for describing man when woman asks.")
fix(2010,"If the Moon is in her fall, or at square or opposition with Saturn, Mars or a retrograde planet, AND then beholds the ascendant, Lilly attributes brawling to the woman.","MOON fall OR named bad aspect, plus Moon beholding ascendant in the original text.","Distinct from adjacent Saturn/Mars/Dragon Tail in ascendant and the unclear idem referent; this is a historical allegation, not verified conduct.")
fix(2009,"Original printed clause crossing p309–310: first and seventh lords in square/opposition, or Saturn, Mars or retrograde/combust planet in ascendant, are given as reasons for contention attributed to the querent.","Include Saturn (♄), Mars (♂), retrograde or combust in ascendant, with correct source page join.")
fix(1991,"For a MAN asking about a woman, Lilly directs reading the planet the MOON is with; if Venus, he says she is fair, slender and pleasant; other planets correspond to other qualities.","The general rule is the Moon's joined planet, Venus only one example.")
fix(1931,"Moon applying to Venus, Venus strong, increasing in motion and in her own dignity, and the MOON likewise strong, increasing in motion and dignified, are attributed to Alkindus as completion conditions.","Do not restrict 'and the Moon likewise' to dignity alone; full scope is retained as source reading.")
fix(2007,"Where seventh lord is more weighty AND angular, Lilly says the woman will be master or STRIVE for it. Where NEITHER principal lord is angular, he instead judges which is weightier for the mastery fallback. Separate Sun/Venus/Moon afflictions qualify each.","The seventh-lord angular clause has 'or strive for it'; the neither-angular fallback says the stronger will be master.")
fix(2021,"A HEAVY or ponderous planet receiving the significators' light, if hindered by square or opposition from an ill planet OR cadent, is said to break an otherwise feasible intended marriage.","The receiver must be a heavy planet, and then suffer one of the stated impediments.","'Heavy' does not mean merely heavily afflicted, and no unspecified 'etc.' completes a missing condition.")
fix(1952,"The seventh lord IN THE SEVENTH, ESPECIALLY in his own house, suggests little intention to marry and a source claim concerning the marriage portion.","Location in seventh essential, own domicile intensifies; not an OR alternative.")
fix(1945,"The first lord OR the MOON in seventh, or the seventh lord in first, provides a claimed route for marriage completion.","Keep the bare Moon-in-seventh branch; no extra condition silently added.")
fix(2019,"Moon aspecting Saturn or Mars is said to produce trouble; if the relevant planets are in angles, Lilly speaks of a PROBABILITY of separation or long disagreements. Separate eighth/twelfth or void-of-course passages also qualify.","Moon specifically aspects Saturn or Mars; 'in angles' attachment is textually ambiguous.","Do not convert source probability into certainty or assume which planet the angular clause modifies.")
fix(2041,"Under 'Whether a Damosell be a Maid', first lord/Moon FIXED and well disposed is said by Lilly to signify she is a virgin; movable/common or evil planets in FIXED signs beholding them give other allegations or, in the relevant adverse branch, 'a doubt of Legerdemain'.","Retain positive fixed/well-disposed and adverse evil-planet alternatives rather than applying 'only doubt' to every case.")
fix(2064,"When Mars is with Dragon's Tail, and seventh lord is joined in the previously described manner, Lilly says it diminishes the asserted malice; although the woman may love a martial man, YET HE CANNOT BRING HER UNDER HIS YOAK, though she has been hard pressed and persuaded.","Mars with south node plus earlier seventh lord conjunction.","Do not invent an act or blame the woman; source explicitly denies the man's subjugation.")
fix(2120,"The source distinguishes: if the woman be with Dragon's HEAD, she hath been formerly DELUDED (deceived); with Dragon's TAIL she 'hath formerly offended, and is still guilty, nor will she amend hereafter'; likewise Mars in place of the Tail is claimed to signify this, though with LESS malice.","Distinguish HEAD deception, TAIL ongoing accusation, and MARS replacing Tail rather than softening Tail itself.","Conflicting moral accusations are historical source claims; no factual verification or endorsement.")
fix(2119,"When angles are fixed signs but first lord or Moon is in movable/common signs, Lilly says the woman 'hath been attempted, and is still tempted' but nevertheless may remain honest.","Require BOTH fixed angles and first-lord/Moon movable or common.","Do not replace source's 'still tempted' with declined.")
fix(2067,"If MARS IS THE SEVENTH LORD, or Moon is lady of seventh, in Aries or Scorpio, the text gives a claimed past affection that may now have diminished; separate passages associate lunar planetary combinations and reception with other claims.","Mars is the seventh ruler, not merely with the seventh ruler.")
fix(2126,"Where MARS IS LORD OF THE SEVENTH, or the Moon is lady of the seventh, in Aries or Scorpio, author makes a past-love claim under additional reception and aspect circumstances.","Do not convert 'Mars Lord of seventh' into Mars with seventh lord.")
fix(2075,"Seventh lord void of course, OR with Dragon's Head (source 'or with ☊, idem'), is given as a sign the woman has no other lover in the historical scheme.","The source includes both void course and Head node same-conclusion clauses.")
fix(2066,"Seventh lord or Moon separated from Mars may signify an attachment predating the woman's acquaintance with her husband, now ended or forgotten.","Explicit BEFORE she knew her husband temporal qualification.")
fix(2039,"If Moon and Sun behold themselves AND Mars, Lilly makes an adverse assertion about virginity.","Keep the three-body requirement; historic allegation unverified.")
fix(2044,"The original says Sun OR Moon beholding Mars under named configurations prompts a moral allegation.","Both solar and lunar alternatives essential.")
fix(2047,"Lilly says 'the Maid is a Virgin, and they lye of her' in the relevant sign configuration.","This expressly alleges the accusers are lying; not that every person is truthful.")
fix(2105,"In the named Venus configuration Lilly says 'of her owne accord the woman will returne'.","Source uses an asserted voluntary return, not merely a wish.")
fix(2071,"The planetary arrangement is said to signify that she loveth at present.","The present-tense claim must be kept distinct from past attachment.")
fix(2136,"Any planet IN the seventh except its lord is treated as alleged acquaintance; the next instruction says the matter may have relation to the ELEVENTH HOUSE.","Do not convert 'relation to eleventh house' into a new 'eleventh-house question' or assume solely woman asks.")
fix(2122,"Printed source gives 'made a harlot by violence, OR she was unwillingly drawn' in a relevant condition.","Preserve both printed alternatives with OR and the nonconsent distinction.")
fix(2065,"Mars and seventh-house ruler/Moon in same sign and within one degree are interpreted as a man INSIDE the house, a familiar of the questioner or of her husband.","The exact one-degree closeness is a separate branch.")
for n,k in [(1937,'alkindus_partner_consent'),(1930,'alkindus_favourable_contact'),(2028,'arabic_capricorn_condition'),(2067,'mars_as_seventh_lord_social_class')]:
 r[n]['source_record_kind']=k
d['status']='CORRECTED_AFTER_TWO_CHANGED_ITEM_REVIEWS_NOT_ACCEPTED'
(B/'RULES.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
out=B/'independent_review'
out.mkdir(exist_ok=True)
for x in 'ab':
 src=A/f'b02s-changed-{x}-20261013/review.stdout'
 shutil.copy2(src,out/f'CHANGED_{x.upper()}_DIAGNOSIS.md')
print(json.dumps({'records':len(d['rules']),'corrected_records':26,'reviewer_inputs':2}))
