#!/usr/bin/env python3
"""Short original 1647 text anchors, not exhaustive original-glyph transcription.

Only first 1647 and independent 1659 original scanned source folios760-762.
All descriptions are hypotheses about an already-known merchant, unverified.
"""
from pathlib import Path
import json

B=Path(__file__).resolve().parent
A=[
(760,"HONOURS_CLXXXIIII_SOURCE_BOUNDARY","SOURCE_CHAPTER_BOUNDARY","Honours, Preferment","Tenth-house distinct heading below Travels divider, original CLXXXIIII.","navigation"),
(760,"PROFESSION_NATURAL_SIGNIFICATORS","SOURCE_ASTRO_RULE","Artists usually consider","Mars, Venus, Mercury are named as generic profession significators.","mechanical"),
(760,"ESSENTIAL_STRENGTH_OR_TENTH_LORD","SOURCE_ASTRO_RULE","essentially strong","Planet strongly placed or lord of tenth can indicate vocation.","mechanical"),
(761,"SEVENTH_HOUSE_COMMERCE","SOURCE_ASTRO_RULE","naturally the house of Commerce","Planets in seventh are used for commercial profession.","mechanical"),
(761,"PARTILE_MOON_ASPECT_PROFESSION","SOURCE_ASTRO_RULE","partill aspect","Near-exact aspect to Moon also counts as occupation significator.","mechanical"),
(761,"SOCIAL_RANK_CONDITION_FOR_PROFESSION","SOCIAL_CONTEXT_NOT_UNIVERSAL_FACT","Kings and Nobility have no professions","Lilly applies stratified seventeenth-century class assumptions, not empirically universal.","context"),
(761,"PROFESSION_RULE_MARS_SELECTED","SOURCE_ASTRO_RULE","Mars is designed for the Native","Mars taken as merchant's occupation significator.","mechanical"),
(761,"MARS_AS_TENTH_LORD","SOURCE_ASTRO_PREDICATE","Mars being Lord of the tenth","Source says Mars rules tenth house.","mechanical"),
(761,"MARS_ASPECTS_MULTIPLE_PLANETS","SOURCE_ASTRO_PREDICATE","pronounce to the Native a Profession","Mars aspects several planets and supports existence of profession.","mechanical"),
(761,"COMPLEX_MULTIPLE_OCCUPATIONS","HISTORICAL_UNVERIFIED_CAREER_CLAIM","Profession shall not be one","Forecast merchant's profession might change, not fixed for whole life.","career_changes"),
(761,"DIRECTIONS_TIMING_OF_PROFESSIONS","EXPLICIT_CONDITIONAL_TIMING","according to the times and directions","Career types said to change with astrological directions; no specific date.","timing_vague"),
(761,"VENUS_SUN_IN_SEVENTH_COMMERCE","SOURCE_ASTRO_PREDICATE","in the seventh","Venus and Sun partnership geometry invoked to support trade.","mechanical"),
(761,"TRADE_IN_USEFUL_THINGS","HISTORICAL_UNVERIFIED_VOCATION","things as are usefull for man","Source suggests occupation with useful commercial goods.","occupation"),
(761,"HUMANE_SIGNS_OF_SIGNIFICATORS","SOURCE_ASTRO_PREDICATE","are in humane Signes","Planet placements in 'humane signs' contribute to trade argument.","mechanical"),
(761,"MARS_LEO_METALS_MINERALS","HISTORICAL_UNVERIFIED_VOCATION","Metals and Minerals","Mars in Leo linked to metals, minerals, martial/solar commodities.","occupation"),
(761,"VENUS_JEWELS_BRACELETS","HISTORICAL_UNVERIFIED_VOCATION","Jewels, Bracelets","Venus said to indicate jewellery and women's ornaments as commercial goods.","occupation"),
(761,"MERCURY_ACCOUNTS_MERCHANDISE","HISTORICAL_UNVERIFIED_VOCATION","Accounts, Merchandize","Mercury said to signify accounting and trade.","occupation"),
(761,"MERCURY_SOLAR_BUSINESS","HISTORICAL_UNVERIFIED_VOCATION","Solar businesses","Mercury-Sun conjunction used to suggest solar goods/business.","occupation"),
(761,"COMMERCE_VOCATION_SELECTION_RULE","SOURCE_ASTRO_PROCEDURE","observe what is signified","Reader directed to choose among many possible merchandise-significator associations.","mechanical"),
(761,"PREFERMENT_HONOR_FROM_TRADE","HISTORICAL_UNVERIFIED_STATUS_FORECAST","Preferment, Honour and estimation","Forecast professional advancement, honour and social esteem.","status"),
(761,"FIXED_STAR_LUCIDA_LANCIS","SOURCE_FIXED_STAR_PREDICATE","Lucida Lancis is neere","Bright star Lucida Lancis near degree culminating invoked for honour.","mechanical"),
(761,"FIXED_STAR_LUCIDA_LYRA","SOURCE_FIXED_STAR_PREDICATE","Lucida Lyre is ascending","Bright star Lucida Lyra near rising invoked for honour.","mechanical"),
(761,"JUPITER_STRONG_ELEVENTH_LORD","SOURCE_ASTRO_PREDICATE","essentially strong","Jupiter is called strong and lord of the eleventh.","mechanical"),
(761,"VENUS_CAZIMI_WITH_SUN_REPEATED","REPEATED_UNVERIFIED_CHART_PREMISE","in Cazimi","This same natal Cazimi premise appeared earlier in Marriage; not independent evidence.","source_dependency"),
(761,"VENUS_CAZIMI_FAME_ARGUMENT","HISTORICAL_UNVERIFIED_STATUS_FORECAST","very splendid, fortunate and famous","Lilly predicts wealth and fame from purported Cazimi and other placements.","status"),
(761,"CONDITIONED_BY_SOCIAL_BIRTH","EXPLICIT_SOURCE_SOCIAL_QUALIFIER","according to the quality of his birth","Predicted honour qualified by native's social origin or profession.","context"),
(761,"MERCHANT_HAS_CALLING_FORECAST","HISTORICAL_UNVERIFIED_CAREER_CLAIM","shall have a Calling","Predicts this merchant will have a vocation; already-known occupational context.","occupation"),
(761,"LIVING_PLENTIFULLY","HISTORICAL_UNVERIFIED_WEALTH_FORECAST","live plentifully of it","Predicts sufficient income from profession.","economic"),
(761,"ESTIMATION_ALL_PLACES","HISTORICAL_UNVERIFIED_STATUS_FORECAST","much estimation in all those places","Expects recognition in places where he resides.","status"),
(761,"LUMINARIES_TRINE","SOURCE_ASTRO_PREDICATE","The Trine which the Luminaries have","Moon-Sun trine is invoked as an additional positive signal.","mechanical"),
(761,"MOON_NEAR_OCULUS_TAURUS","SOURCE_FIXED_STAR_PREDICATE","proximity to Oculus Taurus","Moon near Oculus Taurus used as star evidence.","mechanical"),
(761,"SUDDEN_UNEXPECTED_PREFERMENT","HISTORICAL_UNVERIFIED_STATUS_FORECAST","sudden and unexpected","Predicts sudden unanticipated patronage or advancement.","status"),
]

BROWS=[
(762,"PREFERMENT_FROM_PRINCE","HISTORICAL_UNVERIFIED_SOCIAL_PREDICTION","preferment from some State, King or Prince","Forecast patronage or position from a ruler; not verified.","status"),
(762,"FAVOR_BY_VENERIAN_AGENT","HISTORICAL_UNVERIFIED_SOCIAL_PREDICTION","means of a Venerian creature","Suggests female/Venus-associated person might facilitate patronage; period social claim.","status"),
(762,"VENUS_MOON_MARS_REASONING","SOURCE_ASTRO_PREDICATE","Moon is with oculus tauri","Venus with Sun and Moon by ocular Taurus condition are cited for patronage.","mechanical"),
(762,"JUPITER_PUBLIC_OFFICE_HYPOTHESIS","HISTORICAL_UNVERIFIED_VOCATION","some Office of publique trust","Source predicts possible public office or trust.","occupation"),
(762,"JUPITER_ELEVENTH_SAGITTARIUS","SOURCE_ASTRO_PREDICATE","being Lord of the eleventh","Jupiter Sagittarius placement and eleventh lord underpins office possibility.","mechanical"),
(762,"CHOOSE_PROFESSION_MATERIALS","SOURCE_ASTRO_METHOD","Profession or quality of the Materials","Lilly advises consideration of actual trade goods before predicting advancement.","mechanical"),
(762,"CAUTION_GOOD_DIRECTIONS_TO_MC_SUN","EXPLICIT_CONDITIONAL_FORECAST","good Directions of Medium Coeli","Good directed MC/Sun to benevolent promittors considered auspicious.","timing_vague"),
(762,"FAVORABLE_DIRECTIONS_ACTIVITY","HISTORICAL_UNVERIFIED_BEHAVIOR_FORECAST","be more valiant and active","Forecast native may act more boldly in favourable years.","behavior"),
(762,"UNFAVORABLE_DIRECTIONS_INACTIVE","EXPLICIT_SOURCE_OVERRIDE","e contrario","Opposite unfavourable directions potentially counter supposed success.","timing_vague"),
(762,"INDUSTRY_AFFECTS_OUTCOME","HISTORICAL_PRACTICE_NOT_A_CHART_RESULT","Penny and industry","Merchant urged to use effort and financial resources, a nonastrological determinant.","behavior"),
(762,"OPPORTUNITY_USE_FOR_CREDIT_WEALTH","HISTORICAL_UNVERIFIED_FINANCIAL_FORECAST","esteem and Credit in the World","Favourable timing and personal effort linked to higher esteem and fortune.","economic"),
(762,"NEXT_FRIENDS_CLXXXIII_PRINTED_HEADING","NEXT_SOURCE_CHAPTER_BOUNDARY","Of Friends.","Hard divider: new eleventh-house Friends chapter begins on folio762 with repeated earlier Travels literal Roman CLXXXIII.","navigation"),
]
# Short original text spans retain glyph and spelling uncertainty.
def main():
    import json
    clauses=A+BROWS
    if len({x[1] for x in clauses})!=len(clauses):
        raise ValueError("Duplicated original source semantic role")
    if [x[0] for x in clauses]!=sorted(x[0] for x in clauses):
        raise ValueError("Physical printed folio source order changed")
    result=[dict(folio=f,role=role,kind=kind,anchor=anchor,
                 gloss=gloss,target=target)
            for (f,role,kind,anchor,gloss,target) in clauses]
    (Path(__file__).parent/"HONOURS_CLAUSE_DRAFT_V1.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("WRITTEN HONOURS",len(result),"source roles")

if __name__=="__main__":main()
