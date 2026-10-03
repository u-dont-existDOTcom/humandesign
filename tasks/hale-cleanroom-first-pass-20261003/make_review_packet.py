import json
from pathlib import Path

base=Path(__file__).resolve().parent
D=json.loads((base/"CALCULATIONS.json").read_text())
A=json.loads((base/"ASTRO_DOMAIN_VOTES.json").read_text())
out=[]
out.append("# Blind cross-family audit packet — Hale clean-room first pass\n\n")
out.append("## Constraint\nUse ONLY this packet. Do not inspect repository files, web, memory, or prior information about Hale. No outcome/personality/history data are included. Audit calculations/method and independently derive the strongest first-pass predictions.\n\n")
out.append("## Birth/name inputs\n- Birth name: Hatice Baysan\n- Current name overlay: Hale Denizden (adoption date unknown; static minor-name overlay only)\n- Birth: 1994-01-28 00:35 Europe/Istanbul = 1994-01-27 22:35 UTC, historical offset +02:00\n- Istanbul city coordinate proxy: 41.0138429552247 N, 28.9496612548828 E; angle/house claims are coordinate/time-sensitive.\n\n")
out.append("## Astrology framework\nPrimary: source-grounded traditional framework. Hellenistic: tropical whole-sign, sect/joy/domicile/exaltation. Lilly: tropical Regiomontanus, published dignity/house/motion strengths. Jyotish: Lahiri sidereal whole-sign, own/exaltation/kendra/trikona/upachaya/dusthana. Planet significations in source catalog: Mercury reasoning/interpretation/communication/discovery/systematic work; Jupiter counsel/knowledge/religion/justice/authority; Mars action/effort/strength/conflict/craft; Venus love/friendship/pleasure/art/marriage; Saturn necessity/solitude/obstacles/endurance/labour/constancy/confinement; Moon mind/care/movement/common people; Sun honour/authority. Debility = weaker predicted support, not observed contradiction.\n\n")
out.append("## Natal positions and strengths\n")
for p,row in D["natal"]["planets"].items():
    t=row["tropical"]; si=row["sidereal_lahiri"]
    out.append(f"- {p}: tropical {t['degree_in_sign']:.2f} {t['sign']}, Regio H{row['regiomontanus_house']}, tropical WSH{row['tropical_whole_sign_house']}; sidereal {si['degree_in_sign']:.2f} {si['sign']}, WSH{row['sidereal_whole_sign_house']}; Lilly native {row['lilly_native_strength']['total']}; Hellenistic {row['strength_testimonies']['hellenistic']}; Lilly atomic {row['strength_testimonies']['lilly']}; Jyotish {row['strength_testimonies']['parashari']}\n")
ang=D["natal"]["angles"]
out.append(f"- Tropical Ascendant: {ang['placidus_ascendant']['degree_in_sign']:.2f} {ang['placidus_ascendant']['sign']}; MC: {ang['placidus_midheaven']['degree_in_sign']:.2f} {ang['placidus_midheaven']['sign']}; night chart.\n")
out.append("- Tight <=3° body aspects: "+json.dumps(D["natal"]["major_aspects_3deg"])+"\n")
out.append("- Joel-fitted six-rule fingerprint is secondary only: "+json.dumps(D["natal"]["six_rule_secondary_fingerprint"])+"\n\n")
out.append("## Generic chart-to-domain votes from the pre-existing target-blind consensus map\n")
for d in A["domains"]:
    out.append(f"- {d['domain_id']}: {d['votes']}\n")
out.append("\n## Numerology frozen convention/results\n")
n=D["numerology"]
out.append(f"- Life Path {n['life_path']}; Birthday {n['birthday']}; Attitude/Sun {n['attitude_sun']}\n")
out.append(f"- Birth-name Expression {n['birth_name']['expression']['number']}; Soul Urge {n['birth_name']['soul_urge']['number']}; Personality {n['birth_name']['personality']['number']}; Maturity {n['maturity']}\n")
out.append(f"- Current-name minor overlay: Expression {n['current_name_overlay']['expression']['number']}; Soul Urge {n['current_name_overlay']['soul_urge']['number']}; Personality {n['current_name_overlay']['personality']['number']}\n")
out.append(f"- Pinnacles {n['pinnacles']}; Challenges {n['challenges']}; Periods {n['period_cycles']}\n")
out.append("- Personal Years 2021-2036: "+", ".join(f"{x['year']}={x['number']}" for x in n["personal_years"] if 2021<=x["year"]<=2036)+"\n")
out.append("- Birth-name Transit/Essence ages 27-43: "+json.dumps([x for x in n["birth_name_transits_essences"] if 27<=x["age"]<=43])+"\n\n")
out.append("## Timing events to consider (outcome-blind)\n")
for key,label in [("transits_exact_major_aspects_1994_2041","transit"),("secondary_progressions_exact_major_aspects_1994_2041","progression")]:
    out.append(f"### {label}\n")
    for e in D["timing"][key]:
        y=int(e["exact_utc"][:4])
        if 2021<=y<=2035 and e["target"] in {"sun","moon","mercury","venus","mars","ASC","MC"}:
            if label=="transit" and e["body"]=="jupiter":
                continue
            out.append(f"- {e['exact_utc'][:10]} {e['body']} {e['aspect']} natal {e['target']}\n")
out.append("\n## Audit questions\n1. Identify any calculation/method error visible in this packet.\n2. Independently state the 6-10 strongest astrology-only predictions, preserving contradictions/nulls and separating date-stable from angle/house-sensitive claims.\n3. Independently state the 5-8 strongest numerology-only predictions.\n4. Identify genuine convergence, complementarity, contradiction, and double-counting risk between systems.\n5. Rank major outcome-blind timing windows by evidential/symbolic convergence, with reasons.\n6. Flag any interpretation that would be too strong to freeze prospectively.\n")
text="".join(out)
(base/"CROSS_FAMILY_REVIEW_PACKET.md").write_text(text)
Path("/tmp/hale_clean_review_packet.md").write_text(text)
print(len(text))
