"""Build a source-reference inventory, not a natal prediction model.

The prose is an editor-normalized paraphrase of Lilly's specified pages. Modern
sign/planet names are indexing labels; historical geography is not geocoded.
The enumerated earlier lists are NOT overwritten by the later summary table.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_ID = 'LILLY1647_WELLCOME_B30338724'
SOURCE_SHA = '2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b'
SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
PLANETS = ['Saturn','Jupiter','Mars','Sun','Venus','Mercury','Moon']

# A sequence locator is distinct from a printed label: this witness repeats XVI
# and reverses the labels on PDF 128 and 129.
SECTIONS = [
 {'key':'I.XV','label':'XV','title':'Another briefe Description of the shapes and formes of the Planets','pdf':[118,120],'start':'heading','stop':'before first XVI'},
 {'key':'I.XVI.divisions','label':'XVI','title':'Of the twelve Signes of the Zodiack and their manifold Divisions','pdf':[120,127],'start':'first XVI heading','stop':'before second XVI'},
 {'key':'I.XVI.profiles','label':'XVI','title':'The Nature, Place, Countries, generall Description, and Diseases signified by the twelve signes','pdf':[127,133],'start':'second XVI heading','stop':'end of Pisces'},
 {'key':'I.XVII','label':'XVII','title':'Teaching what use may be made of the former Discourse of the twelve Signes','pdf':[134,135],'start':'heading','stop':'before XVIII'},
 {'key':'I.XVIII','label':'XVIII','title':'Of the Essentiall Dignities of the Planets','pdf':[135,139],'start':'heading','stop':'end of The Use of the Table, before XIX'},
]

BRIEF_PROFILES = [
 {'planet':'Saturn','pdf':[118],
  'appearance':'Swarthy, pale like lead, or earthy brown; rough thick hairy skin, small eyes, a black/yellow or jaundice-like complexion; lean, crooked or beetle-browed, thin whay beard, great lips. The original includes a racialized comparison for the lips. Downward gaze, slow movement, bowed legs or knees striking; often bad breath and a cough.',
  'character':'Craft for personal ends; drawing people to his opinion, revenge and malice, little care for Church or religion, slovenliness, sexual/moral disparagement, large appetite, brawling, great shoulders, covetousness despite seldom being rich.',
  'conditions':['The marginal qualification beside the adverse character cluster is: This where he is peregrine or unfortunate.'],
  'limits':['Exact reach of the marginal qualification over the preceding physical description remains unresolved.','Do not replace the qualified adverse portrait with an unconditional Saturn personality.']},
 {'planet':'Jupiter','pdf':[118],
  'appearance':'Comely stature, full face and eyes, sanguine or mixed white/red, wide space between brows; usually flaxen or sandy-flaxen beard, sometimes dark/black when combust; thick hair, non-black eyes, broad well-set teeth with a difference or imperfection in the two front teeth.',
  'character':'Well-spoken, religious or at least morally honest; the description adjusts to the represented person\'s station rather than requiring noble birth in every instance.',
  'conditions':['Moist signs: fleshy or somewhat fat; airy signs: big and strong; earthly signs: usually well-descended.','If representing an ordinary clown, comparatively humane within that stated social frame.','The curl-of-hair parenthesis is provisionally read fiery in the image, whereas the text layer reads Aery; this token is not admitted as an executable discriminator.'],
  'limits':['No modern social-class, ancestry or hair prediction is made.','The unresolved fiery/Aery token is distinct from the clear airy-sign body-size clause.']},
 {'planet':'Mars','pdf':[118,119],
  'appearance':'Often full-faced, sunburnt or raw-tanned-leather colour; fierce, sparkling or sharp yellow eyes; reddish hair with sign/star qualifications. Facial mark or scar, broad shoulders, sturdy strong body.',
  'character':'Bold, proud, mocking, quarrelsome, given to drinking, gaming and sexual pursuits; subsidiary descriptions depend on whose domicile contains Mars.',
  'conditions':['Fire or air signs with fixed stars of Mars\'s nature: deep sandy-red hair.','Water signs with fixed stars of Mars\'s nature: flaxen or whitish bright hair.','Earth signs: dark-brown or chestnut hair.','Domicile-specific character branches are stored separately; no Jupiter branch is supplied.'],
  'limits':['The fixed-star prerequisite is not dispensable in the first two hair clauses.','This is a portrait of the person signified, not every person with Mars in a chart.']},
 {'planet':'Sun','pdf':[119],
  'appearance':'Usually white mixed with red, sometimes between yellow and black; round face, short chin, fair stature/comely body, generally sanguine; curly hair, tender white skin, clear voice, large head and obliquely set teeth.',
  'character':'Bold and resolute, desirous of praise and reputation, slow speech and composed judgment; outward decorum is contrasted with private lasciviousness and inclination to vices.',
  'conditions':['The paragraph is a general significator description in this chapter.'],
  'limits':['The outward/private contrast is retained, not converted into a uniformly favourable portrait.']},
 {'planet':'Venus','pdf':[119],
  'appearance':'For the man or woman signified: fair round face, full/goggle eyes, red lips with the lower larger, dark eyelids but graceful; hair colour varies by sign, including black or light brown; smooth soft hair, well-shaped body, inclined to short rather than tall.',
  'character':'Grace and loveliness are part of the physical presentation; no separate elaborate moral portrait is supplied here.',
  'conditions':['The source expressly includes both man and woman.','Hair is qualified by sign rather than one invariant colour.'],
  'limits':['No missing character traits are filled from the earlier Venus chapter.']},
 {'planet':'Mercury','pdf':[119,120],
  'appearance':'Intermediate dark-brown/yellowish colouring, long face, high forehead, black or grey eyes, thin long sharp nose, sparse or absent dark-auburn beard; slender body and small legs.',
  'character':'Prattling, busy, nimble walking, and wishing to be thought full of action.',
  'conditions':['General portrait of the represented person.'],
  'limits':['The appearance of activity is not rewritten as proven productivity.']},
 {'planet':'Moon','pdf':[120],
  'appearance':'Variable shape; generally round full face, white/red mixture with pallor predominating; in water signs freckles or blub-cheeked appearance; an unhandsome or mudling figure in the source\'s language.',
  'character':'In fiery signs hasty speech; usually an ordinary vulgar person unless very well dignified.',
  'conditions':['Fiery-sign speech and watery-sign appearance are different clauses.','The social description has the explicit very-well-dignified exception.'],
  'limits':['Historical appearance/social categories are not present-day demographic facts.']},
]
MARS_DOMICILE_BRANCHES = [
 {'domicile_lord':'Venus','source_predicate':'sexual pursuit (wencheth)'},
 {'domicile_lord':'Mercury','source_predicate':'stealing'},
 {'domicile_lord':'Mars','source_predicate':'quarrelling'},
 {'domicile_lord':'Saturn','source_predicate':'doggedness'},
 {'domicile_lord':'Sun','source_predicate':'lordliness'},
 {'domicile_lord':'Moon','source_predicate':'drunkenness'},
]
COLOURS = {
 'planets':dict(zip(PLANETS,['black','red mixed with green','red or iron','yellow or yellow-purple','white or purple','sky-colour or bluish','spotted with white and other mixed colours'])),
 'signs':dict(zip(SIGNS,['white mixed with red','white mixed with citrine','white mixed with red','green or russet','red or green','black speckled with blue','black, dark crimson or tawny','brown','yellow or green sanguine','black, russet or swarthy brown','sky-colour with blue','white glistering'])),
 'pdf':120,
 'scope':'Symbolic colour catalogue. Not automatically the complexion/hair of a person or a colour code.'
}
GROUPS = [
 ('spring',['Aries','Taurus','Gemini'],'hot, moist, sanguine; seasonal quadrant',121),
 ('summer',['Cancer','Leo','Virgo'],'hot, dry, choleric; seasonal quadrant',121),
 ('autumn',['Libra','Scorpio','Sagittarius'],'cold, dry, melancholic; seasonal quadrant',121),
 ('winter',['Capricorn','Aquarius','Pisces'],'cold, moist, phlegmatic; seasonal quadrant',121),
 ('fire',['Aries','Leo','Sagittarius'],'hot and dry; elemental triplicity',121),
 ('earth',['Taurus','Virgo','Capricorn'],'cold and dry; elemental triplicity',121),
 ('air',['Gemini','Libra','Aquarius'],'hot and moist; elemental triplicity',121),
 ('water',['Cancer','Scorpio','Pisces'],'cold and moist; elemental triplicity',121),
 ('masculine',['Aries','Gemini','Leo','Libra','Sagittarius','Aquarius'],'diurnal and hot',122),
 ('feminine',['Taurus','Cancer','Virgo','Scorpio','Capricorn','Pisces'],'nocturnal and cold',122),
 ('northern_declination',SIGNS[:6],'Boreal/Septentrional: north of the equinoctial; not the directional triplicity field',122),
 ('southern_declination',SIGNS[6:],'Austral/Meridional: south of the equinoctial; not the directional triplicity field',122),
 ('movable',['Aries','Cancer','Libra','Capricorn'],'cardinal; entry starts seasonal quarters',122),
 ('fixed',['Taurus','Leo','Scorpio','Aquarius'],'season settles; heat/cold/moisture/dryness becomes more evident',122),
 ('common',['Gemini','Virgo','Sagittarius','Pisces'],'bicorporeal/double-bodied; partakes of preceding and following sign',122),
 ('equinoctial',['Aries','Libra'],'spring/autumn boundaries',122),
 ('solstitial',['Cancer','Capricorn'],'tropic summer/winter boundaries',122),
 ('bestial',['Aries','Taurus','Leo','Sagittarius','Capricorn'],'quadrupedian; Sagittarius is included without a partial-sign qualifier in this list',123),
 ('fruitful',['Cancer','Scorpio','Pisces'],'prolific',123),
 ('barren',['Gemini','Leo','Virgo'],'historical fertility category',123),
 ('humane',['Gemini','Virgo','Libra','Aquarius'],'manly/humane/courteous signs',123),
 ('mute',['Cancer','Scorpio','Pisces'],'mute or slow voice',123),
 ('commanding',SIGNS[:6],'separate from the elemental direction table',126),
 ('obeying',SIGNS[6:],'complement of commanding',126),
 ('long_ascension',SIGNS[3:9],'right or long ascension in the stated table context',126),
 ('short_ascension',SIGNS[9:]+SIGNS[:3],'oblique or short ascension in the stated table context',126),
]
SIGN_GROUPS = [{'key':k,'signs':s,'source_description':d,'pdf':p} for k,s,d,p in GROUPS]
FERAL = {'whole_signs':['Leo'],'partial_signs':[{'sign':'Sagittarius','part':'last part','numerical_start_degree':None}],'pdf':123}

# Each long profile preserves all five kinds of content; their application is
# separately qualified by chapter XVII, rather than all being applied at once.
SIGN_PROFILES = [
 {'sign':'Aries','pdf':[127,128],
  'nature':'Masculine, diurnal, movable, cardinal, equinoctial; fiery, hot, dry, choleric, bestial, luxurious, intemperate and violent; Mars\'s diurnal house, fiery triplicity, East.',
  'diseases':'Pushes, whelks and facial pimples; smallpox, hare-lips, polypus, noli me tangere, ringworms, falling-sickness, apoplexies, megrims, toothache, headache and baldness.',
  'places':'Sheep/small-cattle feeding places; sandy hilly ground; unfrequented refuge for thieves; house covering, ceiling or plastering; small-beast stable; newly enclosed/ploughed land; brick- or lime-burning places.',
  'appearance':'Dry, not exceptionally tall, lean/spare yet bony and strong-limbed; long visage, black brows, long neck, thick shoulders, dusky-brown or swarthy complexion.',
  'countries_cities':['Germany','Swevia','Polonia','Burgundy','France','England','Denmark','higher Silesia','Judea','Syria','Florence','Capua','Naples','Ferrara','Verona','Utrecht','Marseilles','Augusta','Caesarea','Padua','Bergamo']},
 {'sign':'Taurus','pdf':[128],
  'nature':'Earthly, cold, dry, melancholic, feminine, nocturnal, fixed, domestic or bestial; earthly triplicity, South; night-house of Venus.',
  'diseases':'King\'s Evil, sore throats, wens, fluxes of rheums into the throat, quinzies and impostumes in that part.',
  'places':'Horse stables, low houses and cattle-implement stores; pastures away from houses, plain ground or recently grubbed bushes with corn sown and small trees nearby; cellars and low rooms.',
  'appearance':'Short, full, strong, well-set; broad forehead, great eyes/face, large strong shoulders, great mouth and thick lips, gross hands, black rugged hair.',
  'countries_cities':['great Polonia','north part of Sweathland','Russia','Ireland','Switzerland','Lorraine','Campania','Persia','Cyprus','Parthia','Novograde','Parma','Bononia','Panormus','Mantua','Sena','Brixia','Carolstad','Nants','Leipsig','Herbipolis']},
 {'sign':'Gemini','pdf':[128,129],
  'nature':'Aerial, hot, moist, sanguine, diurnal, common/double-bodied, human, masculine; Mercury\'s diurnal house, airy triplicity, West.',
  'diseases':'Arms, shoulders and hands; corrupted blood, wind in veins and distempered fancies.',
  'places':'Wainscot rooms, plastering and walls, halls or play places; hills/mountains, barns, corn stores, coffers, chests and high places.',
  'appearance':'Upright, tall, straight body in man or woman; obscure/dark sanguine complexion, long arms but often short fleshy hands and feet; dark nearly black hair; strong active body, piercing hazel eye, wanton and excellent sight, understanding and worldly judgment.',
  'countries_cities':['Lumbardy','Brabant','Flanders','west and southwest of England','Armenia','London','Lovaine','Bruges','Norrimberg','Corduba','Hasford','Mentz','Bamberg','Cesena']},
 {'sign':'Cancer','pdf':[129],
  'nature':'Moon\'s sole house; first of the watery/Northern triplicity; watery, cold, moist, phlegmatic, feminine, nocturnal, movable, solstitial, mute/slow-voiced, fruitful and Northern.',
  'diseases':'Breast, stomach and paps; weak digestion, cold stomach, ptisick, salt phlegms, rotten coughs, dropsical humours, stomach impostumations and cancers in the breast.',
  'places':'Sea, great rivers and navigable waters; inland near rivers, brooks, springs, wells, cellars, wash-houses, marsh, rush/sedge ditches, sea banks, trenches and cisterns.',
  'appearance':'Small/low stature, larger upper than lower parts, round visage, sickly/pale/whitish complexion, dark-brown hair, little eyes; prone to many children if a woman.',
  'countries_cities':['Scotland','Zealand','Holland','Prussia','Tunis','Algier','Constantinople','Venice','Milan','Genoa','Amsterdam','Yorke','Magdeberg','Wittenberg','Saint Lucas','Cadiz']},
 {'sign':'Leo','pdf':[129,130],
  'nature':'Sun\'s sole house; fiery, hot, dry, choleric, diurnal, commanding, bestial, barren, Eastern, fiery triplicity and masculine.',
  'diseases':'Ribs/sides, pleurisies, convulsions, back pain, heart trembling/passion, violent burning fevers, heart weakness/disease, sore eyes, plague, pestilence and yellow jaundice.',
  'places':'Wild-beast haunts, woods, forests, deserts, steep rocks and inaccessible places; royal palaces, castles, forts and parks; house fire places and chimneys.',
  'appearance':'Great round head, staring/goggle eyes and quick sight; large body above medium stature, broad shoulders, narrow sides, yellow/dark-flaxen curling hair; fierce yet ruddy sanguine countenance, strong, valiant, active.',
  'countries_cities':['Italy','Bohemia','Alpes','Turkie','Sicilia','Apulia','Rome','Syracusa','Cremona','Ravenna','Damasco','Prague','Lintz','Confluentia','Bristol']},
 {'sign':'Virgo','pdf':[130],
  'nature':'Earthly, cold, melancholic, barren, feminine, nocturnal, Southerne; Mercury\'s house and exaltation; earthly triplicity. The local directional word is not silently identified with the earlier declination hemisphere.',
  'diseases':'Worms, wind, colic, bowel/mesaraic obstructions, croaking of guts, infirmity in the Stones, and belly diseases. Historical anatomical labels are not diagnostically resolved.',
  'places':'Study with books, closet, dairy-house, corn fields, granaries, malt-houses, hay-ricks/barley/wheat/peas; stores of cheese and butter.',
  'appearance':'Slender medium-height decent body; ruddy-brown, black hair, lovely but not beautiful, small shrill voice, short members; witty, discreet, judicious, eloquent, studious and fond of history in man or woman. Rare understanding with Mercury here and Moon in Cancer, but somewhat unstable.',
  'countries_cities':['southern part of Greece','Croatia','Athenian territory','Mesopotamia','Africa','southwest of France','Paris','Hierusalem','Rhodes','Lyons','Tholous','Basil','Heidelburge','Brundusium']},
 {'sign':'Libra','pdf':[130,131],
  'nature':'Aerial, hot, moist, sanguine, masculine, movable, equinoctial, cardinal, human, diurnal, Western, airy triplicity; chief house of Venus.',
  'diseases':'Stone/gravel in reins/back/kidneys, heat and illness in loins/haunches, ulcers or impostumes in reins/kidneys/bladder, back weakness, corrupted blood.',
  'places':'Near windmills, isolated barns/out-houses, saw-pits, coopers or wood cutting; hill sides/mountain tops, hawking/hunting, sandy/gravelly fields, clear sharp air; upper rooms, chambers, garrets, one chamber inside another.',
  'appearance':'Well-framed, straight, tall, more slender than gross; round lovely beautiful visage, sanguine; balanced white/red in youth, pimples or high colour in age; yellowish smooth long hair.',
  'countries_cities':['higher Austria','Dukedom of Savoy','Alsatia','Livonia','Lisbone in Portugal','Frankeford','Vienna','Placentia','territory in Greece where Thebes formerly stood','Arles','Friburge','Spires']},
 {'sign':'Scorpio','pdf':[131],
  'nature':'Cold, watery, nocturnal, phlegmatic, feminine, fixed and North; watery triplicity, house and joy of Mars; usually subtle/deceitful persons in the source portrait.',
  'diseases':'Gravel/stone in secret parts, bladder, ruptures, fistulae, piles in ano, gonorrheas, priapisms, afflictions of privy parts and defects of the matrix.',
  'places':'Creeping/wingless/poisonous creatures, beetles; gardens, orchards, vineyards, ruined houses near water, muddy/moorish ground, stinking lakes, quagmires, sinks, kitchen, larder, wash-house.',
  'appearance':'Corpulent strong able body; broad/square face, dusky muddy complexion, much dark curling hair, hairy body, somewhat bowed legs, short neck and squat well-trussed figure.',
  'countries_cities':['north Bavaria','wooded Norway','Barbary','Kingdom of Fez','Catalonia in Spain','Valentia','Urbine','Forum Julii in Italy','Vienna','Messina in Italy','Gaunt','Frankeford upon Odar']},
 {'sign':'Sagittarius','pdf':[131,132],
  'nature':'Fiery triplicity, East, fiery/hot/dry, masculine, choleric, diurnal, common/bicorporeal/double-bodied; house and joy of Jupiter.',
  'diseases':'Thighs and buttocks, fistulae or hurts there; heated blood, pestilential fevers, falls from horses or hurts from quadrupeds, injury through fire/heat/excess in sports.',
  'places':'Stable of great/war horses or great quadrupeds; hills, high/rising ground; upper rooms near fire.',
  'appearance':'Well-favoured, somewhat long but full ruddy/sunburnt face, light chestnut hair, above-medium stature, proportioned members and a strong body.',
  'countries_cities':['Spain','Hungary','Slavonia','Moravia','Dalmatia','Buda in Hungary','Toledo','Narbon','Cullen','Stargard']},
 {'sign':'Capricorn','pdf':[132],
  'nature':'Saturn\'s house; nocturnal, cold, dry, melancholic, earthly, feminine, solstitial, cardinal, movable, domestic, quadrupedal, Southern; exaltation of Mars.',
  'diseases':'Knees and their strains/fractures; leprosy, itch and scab.',
  'places':'Ox/cow/calf houses; husbandry tools, old wood, ship sails/material stores; sheep pens/pastures, fallow/barren/bushy/thorny fields, dunghills/soil heaps; low dark house places near ground or threshold.',
  'appearance':'Dry, not tall; long lean slender face, thin beard, black hair, narrow chin, long small neck, narrow breast. Lilly reports often seeing white hair with Capricorn rising but black in the seventh, and conjectures family rather than sign caused the whiteness.',
  'countries_cities':['Thrace','Macedon in Greece now Turkie','Albania','Bulgaria','southwest Saxony','West-Indias','Stiria','Orcades','Hassia','Oxford','Mecklin','Cleve','Brandenburge']},
 {'sign':'Aquarius','pdf':[132,133],
  'nature':'Aerial, hot, moist, airy triplicity, diurnal, sanguine, fixed, rational, human, masculine, Western; principal house of Saturn and where he most rejoices.',
  'diseases':'Legs/ankles and their infirmities; melancholy winds in veins or disturbing blood, cramps.',
  'places':'Hilly/uneven or newly dug ground, stone quarries/mineral diggings; roofs/eaves/upper house parts; vineyards or near a spring/conduit head.',
  'appearance':'Squat/thick/strong well-composed, not tall, long visage and sanguine. Saturn in Capricorn or Aquarius: black hair, sanguine complexion, distorted teeth. Otherwise Lilly reports fair/clear skin and sandy/flaxen hair.',
  'countries_cities':['Tartary','Croatia','Valachia','Muscovia','Westphalia in Germany','Piemont in Savoy','west and south Bavaria','Media','Arabia','Hamborough','Breme','Montferrat','Pisaurum in Italy','Trent','Ingolstad']},
 {'sign':'Pisces','pdf':[133],
  'nature':'Watery triplicity, Northern, cold, moist, phlegmatic, feminine, nocturnal; Jupiter\'s house and Venus\'s exaltation; common/bicorporeal/double-bodied; idle, effeminate, sickly or without action in the source description.',
  'diseases':'Feet, gout, lameness/aches, salt phlegms, scabs, itch, botches, boils, ulcers from putrefied blood, colds and moist diseases.',
  'places':'Water-filled ground, springs and fowl, fish ponds/rivers, former hermitages, moats, water mills; indoors near water/well/pump or standing water.',
  'appearance':'Short, ill-composed/not very decent, large pale face, fleshy/swelling body, somewhat bent head rather than straight.',
  'countries_cities':['Calabria in Sicilia','Portugal','Normandy','north Egypt','Alexandria','Rhemes','Wormes','Ratisbone','Compostella']},
]

ANTISCIA_PAIRS = [('Gemini','Cancer'),('Leo','Taurus'),('Virgo','Aries'),('Libra','Pisces'),('Scorpio','Aquarius'),('Sagittarius','Capricorn')]
TERMS = {
 'Aries':[('Jupiter',6),('Venus',14),('Mercury',21),('Mars',26),('Saturn',30)],
 'Taurus':[('Venus',8),('Mercury',15),('Jupiter',22),('Saturn',26),('Mars',30)],
 'Gemini':[('Mercury',7),('Jupiter',14),('Venus',21),('Saturn',25),('Mars',30)],
 'Cancer':[('Mars',6),('Jupiter',13),('Mercury',20),('Venus',27),('Saturn',30)],
 'Leo':[('Saturn',6),('Mercury',13),('Venus',19),('Jupiter',25),('Mars',30)],
 'Virgo':[('Mercury',7),('Venus',13),('Jupiter',18),('Saturn',24),('Mars',30)],
 'Libra':[('Saturn',6),('Venus',11),('Jupiter',19),('Mercury',24),('Mars',30)],
 'Scorpio':[('Mars',6),('Jupiter',14),('Venus',21),('Mercury',27),('Saturn',30)],
 'Sagittarius':[('Jupiter',8),('Venus',14),('Mercury',19),('Saturn',25),('Mars',30)],
 'Capricorn':[('Venus',6),('Mercury',12),('Jupiter',19),('Mars',25),('Saturn',30)],
 'Aquarius':[('Saturn',6),('Mercury',12),('Venus',20),('Jupiter',25),('Mars',30)],
 'Pisces':[('Venus',8),('Jupiter',14),('Mercury',20),('Mars',26),('Saturn',30)],
}
FACES = dict(zip(SIGNS,[['Mars','Sun','Venus'],['Mercury','Moon','Saturn'],['Jupiter','Mars','Sun'],['Venus','Mercury','Moon'],['Saturn','Jupiter','Mars'],['Sun','Venus','Mercury'],['Moon','Saturn','Jupiter'],['Mars','Sun','Venus'],['Mercury','Moon','Saturn'],['Jupiter','Mars','Sun'],['Venus','Mercury','Moon'],['Saturn','Jupiter','Mars']]))
DOMICILES = dict(zip(SIGNS,['Mars','Venus','Mercury','Moon','Sun','Mercury','Venus','Mars','Jupiter','Saturn','Saturn','Jupiter']))
EXALTATIONS = {'Aries':('Sun',19),'Taurus':('Moon',3),'Gemini':('Ascending Node',3),'Cancer':('Jupiter',15),'Virgo':('Mercury',15),'Libra':('Saturn',21),'Sagittarius':('Descending Node',3),'Capricorn':('Mars',28),'Pisces':('Venus',27)}
TRIPLICITY = {'fire':{'day':'Sun','night':'Jupiter'},'earth':{'day':'Venus','night':'Moon'},'air':{'day':'Saturn','night':'Mercury'},'water':{'day':'Mars','night':'Mars'}}
WEIGHTS = {'domicile':5,'exaltation':4,'triplicity':3,'term':2,'face':1}

RULES: list[dict] = []
def add(section: str, title: str, statement, pages: list[int], kind='conditional_source_rule', requires=None, limits=None):
    n=231+len(RULES)
    RULES.append({
        'id':f'LI.1647.{section}.R{n:03d}', 'title':title, 'kind':kind,
        'source_locator':{'source_id':SOURCE_ID,'source_sha256':SOURCE_SHA,'book':'I','section_key':section,'pdf_pages':pages,'printed_page_policy':'Use READING_RECEIPT page map; original labels are not uniformly PDF minus 34.'},
        'statement_type':'editor_normalized_paraphrase' if not kind.startswith('table') else 'transcribed_table_with_named_glyphs',
        'source_statement':statement,
        'prerequisites':requires or ['Apply only within the stated enquiry and source-selected significator context.'],
        'qualifications_and_limits':limits or ['Historical source claim, not established predictive, clinical or demographic evidence.'],
        'runtime_status':'REFERENCE_ONLY_NOT_PROMOTED','independent_evidence_unit':False,
    })

for x in BRIEF_PROFILES:
    add('I.XV',x['planet']+' brief portrait',{'appearance':x['appearance'],'character':x['character']},x['pdf'],requires=x['conditions'],limits=x['limits'])
for x in MARS_DOMICILE_BRANCHES:
    add('I.XV','Mars in domicile of '+x['domicile_lord'],x['source_predicate'],[119],requires=['Mars is the relevant significator.','Its sign belongs to the specified domicile lord.'],limits=['Historical adverse behaviour catalogue; no observed conduct inferred from a natal position.','Jupiter branch is absent from this six-branch local list.'])
for label,rows in [('planet',COLOURS['planets']),('sign',COLOURS['signs'])]:
    add('I.XV',label.title()+' colour table',rows,[120],kind='table_catalogue',requires=['The actual enquiry calls for colour testimony.'],limits=[COLOURS['scope']])
add('I.XVI.divisions','Zodiac and angular units','Twelve named signs contain thirty degrees each; the whole zodiac 360 degrees; sixty minutes or scruples per degree and sixty seconds per minute. Sign names are explained through creature properties or the appearance of stars.',[120,121],kind='source_definition')
for x in SIGN_GROUPS:
    add('I.XVI.divisions',x['key']+' sign group',x,[x['pdf']],kind='table_classification')
add('I.XVI.divisions','Feral partial sign',FERAL,[123],kind='table_classification',limits=['Last part of Sagittarius has no numerical boundary in this passage.','Do not substitute the whole Sagittarius sign for this partial category.'])
add('I.XVI.divisions','Planetary/sign masculinity','A masculine planet in a masculine sign makes the person represented more manly; in a feminine sign less courageous.',[122],requires=['The represented planet is masculine.','Its sign classification is known.'],limits=['Historical gendered description, explicitly applied to man or woman; not a gender-identity or orientation inference.'])
for mode,outcome in [('movable','Unstable, wavering and readily mutable.'),('fixed','Firm and persevering in what has been said or done, whether good or ill.'),('common','Between great wilfulness and easy variability.')]:
    add('I.XVI.divisions','Matched Ascendant/ruler modality: '+mode,outcome,[123],requires=[f'The Ascendant sign is {mode}.',f'The Ascendant lord is in a {mode} sign.'],limits=['Both prerequisites are required. Mixed modalities and unknown inputs are not specified by these three branches.','Firmness is not moral goodness.'])
add('I.XVI.divisions','Mute-sign intensification','Mute or slow voice is reinforced when Mercury is in one of the three mute signs and conjunct, square or opposite Saturn.',[123],requires=['Mercury in Cancer, Scorpio or Pisces.','Conjunction, square or opposition to Saturn.'],limits=['The chart geometry and orb must be separately qualified; none is chosen here.','Not a speech diagnosis.'])
add('I.XVI.divisions','Animal analogies','Relevant significator or Ascendant lord in a bestial sign has something of that animal\'s nature. Aries is exemplified as rash, hardy and lascivious; Taurus as steadfast/resolved but muddy and with private imperfection.',[123],limits=['Other animal descriptions are not fully specified in this paragraph.','Historical figurative claims are not observed personality facts.'])
add('I.XVI.divisions','Prolific fertility question','In a question about children, strong Moon and principal significators in prolific signs indicate children.',[123],requires=['Question concerns having children.','Moon and principal significators in prolific signs.','Those significators are strong.'],limits=['Not an unconditional water-sign fertility rule or medical advice.'])
add('I.XVI.divisions','Barren-sign question','A barren Ascendant or fifth-house sign generally represents few or no children.',[123],requires=['The enquiry concerns barrenness/children.','Ascendant or fifth house has a barren sign.'],limits=['Generally and few-or-none are not an exact child count or a medical diagnosis.'])
add('I.XVI.divisions','Humane-sign alternative routes','Humane signs rising, or the Ascendant lord in humane signs, indicate civil and affable carriage.',[123,124],requires=['Either humane Ascendant OR its lord in a humane sign.'],limits=['Unlike the modality rule this passage uses alternative routes.'])
add('I.XVI.divisions','Antiscion geometry and influence','Paired places have equal distance from beginnings of Cancer/Capricorn and corresponding solar day/night lengths. Taurus 10 degrees is paired with Leo 20. A planet there, or casting an aspect there, receives virtue/influence.',[124],requires=['Degree-specific antiscion location, not merely a sign pair.'],limits=['No orb or empirical effect size is supplied.','Equal day/night lengths across the paired solar positions does not mean day equals night at each position.'])
add('I.XVI.divisions','Six antiscion sign pairs',ANTISCIA_PAIRS,[124],kind='table_geometry')
add('I.XVI.divisions','Antiscion subtraction','Subtract the within-sign degrees and minutes from thirty degrees in the paired sign. Saturn Leo 20 degrees 35 minutes gives Taurus 9 degrees 25 minutes.',[124,125],kind='worked_calculation',limits=['The result is arithmetically correct. The explanatory sentence names 25 minutes as the subtrahend despite the preceding 35-minute input. Preserve that printed discrepancy.'])
add('I.XVI.divisions','Antiscion degree and minute tables',{'degree_pairs':[[n,30-n] for n in range(1,16)],'minute_pairs':[[n,60-n] for n in range(1,31)]},[125],kind='table_geometry',limits=['A nonzero minute component requires borrowing one degree; independently subtracting degrees from 30 and minutes from 60 overcounts by one degree.'])
add('I.XVI.divisions','Antiscion quality qualification','Antiscia of good planets are thought equivalent in nature to sextile or trine; contrantiscia to square or opposition.',[126],requires=['Good-planet qualification belongs to the favourable antiscion clause.'],limits=['Do not make every antiscion favourable or count the same reflection as independent evidence.'])
add('I.XVI.divisions','Contrantiscion opposition','The contrantiscion is opposite the antiscion in sign and degree; Saturn\'s Taurus 9 degrees 25 minutes antiscion has Scorpio 9 degrees 25 minutes contrantiscion.',[126],kind='worked_calculation')
add('I.XVI.divisions','Rising-time ranges','Long-ascension signs are said to spend two hours or more rising; short signs little over an hour or less. The worked examples use the supplied table, not every latitude.',[126,127],limits=['Retain the source table context; global latitude invariance is not established.','No actual astronomical boundary calculation was done in this extraction.'])
add('I.XVI.divisions','Leo rising example',{'start_ascendant':'Leo 0:21','start_time':'00:18','end_ascendant':'Leo 29:40','end_time':'03:06','difference_minutes':168},[126],kind='worked_calculation',limits=['These are near-boundary tabular endpoints, not exactly Leo 0 and Leo 30.'])
add('I.XVI.divisions','Aquarius rising example',{'start_ascendant':'Aquarius 0:57','start_time':'16:04','end_ascendant':'Aquarius 29:28','end_time':'17:08','difference_minutes':64},[127],kind='worked_calculation',limits=['Exact subtraction of two tabulated times does not make this an exact full-sign rising duration.'])
add('I.XVI.divisions','Stated further use of rising times','Lilly claims this knowledge is needed for natural magic, including gathering herbs, and other rarities.',[127],kind='source_scope_claim',limits=['Historical statement of intended use, not a treatment or harvesting instruction.'])

for x in SIGN_PROFILES:
    for field in ['nature','diseases','places','appearance','countries_cities']:
        add('I.XVI.profiles',x['sign']+': '+field,x[field],x['pdf'],kind='source_catalogue',requires=['Use the relevant-topic selection and combination procedure in XVII.'],limits=['Historical catalogue, not established present-day clinical, demographic or geographical classification.','Country/city spellings are lightly normalized for legibility; territories, qualifiers and surprising assignments are retained, not geocoded.'])
add('I.XVI.profiles','Virgo intellect compound','Rare understanding but somewhat unstable when Mercury is in Virgo and Moon in Cancer.',[130],requires=['Mercury in Virgo.','Moon in Cancer.'],limits=['The Moon glyph is Cancer in the original image.','This compound is not merely the generic Virgo description.'])
add('I.XVI.profiles','Capricorn family alternative','Lilly reports repeated white-haired Capricorn Ascendants but black hair when Capricorn is seventh, and proposes family rather than the sign as the reason for the white hair.',[132],kind='author_observation_and_conjecture',limits=['The causal proposal is the author\'s conjecture, not demonstrated heredity or validation of either astrological branch.'])
add('I.XVI.profiles','Aquarius dispositor modifier','Saturn in Capricorn or Aquarius modifies the Aquarius description to black hair, sanguine complexion and distorted teeth; otherwise Lilly reports clearer fair skin and sandy/flaxen hair.',[133],requires=['Aquarius is the relevant sign.','Saturn\'s sign is established.'],limits=['Do not discard the generic body description or count its restatement as independent testimony.'])

add('I.XVII','Three-place description synthesis','For the condition/quality/stature of the person enquired about, combine the sign of the relevant house, its lord\'s sign, and the Moon\'s sign; judge by greater testimonies.',[134],requires=['Identify the house of the actual person/topic.','Keep house sign, house ruler and Moon distinct.'],limits=['No numerical weights, tie rule, probability or universal dominant-planet replacement is supplied.'])
add('I.XVII','Humane/airy reinforcement example','A humane/airy sign rising or setting, with its lord or Moon in the same triplicity or nature, supports a handsome body and sociable/courteous conditions.',[134],requires=['Specified rising/setting sign condition.','Lord OR Moon has the stated matching nature/triplicity.'],limits=['No requirement for all three to be identical is invented.'])
add('I.XVII','Disease needs concurrence','Aries at the Ascendant cusp or described as descending in the sixth contributes something of Aries to a disease enquiry, but what specifically depends on concurrence of the other significators.',[134],limits=['Descending in the sixth is retained as unresolved wording.','Not a diagnostic mapping from an isolated sign.'])
add('I.XVII','Lost animal versus immovable object','Use the thing\'s significator sign for its appropriate places and quarter of heaven; a stray beast calls for those outside places, while an object that needs human movement calls for corresponding parts of the house.',[134],requires=['Establish the kind of missing thing and its significator.'],limits=['The catalogue is routed by the question, not all places at once.'])
add('I.XVII','Personal travel selection','For health/prosperity in a country or city, use the Ascendant lord\'s sign and favourable condition, with a Jupiter/Venus placement alternative, and the corresponding source place catalogue.',[134],limits=['Historical rule, not contemporary travel/health advice or verified geocoding.'])
add('I.XVII','Malefic-country exception','Countries under signs containing malefics are called unfortunate unless those malefics themselves are significators.',[134,135],requires=['Check the explicit significator-role exception before the adverse reading.'],limits=['Does not make every relevant malefic benefic in all respects.'])
add('I.XVII','Merchant target changes reference places','Where the merchant aims at trade and increasing stock, consider the second-house sign, the Lot of Fortune and the second-house lord, and the strongest, rather than substituting the personal health/jocundity enquiry.',[135],requires=['The question concerns trade/stock, not merely personal welfare.'],limits=['No weights or automatic travel recommendation is given; target-specific source procedure only.'])

add('I.XVIII','Three prerequisites for judgment','Know planetary/sign natures, weigh significator strength/debility and aspect mixtures, and apply natural rather than forced maxims; straining judgment beyond nature increases error.',[135],kind='source_method')
add('I.XVIII','Five essential dignities and weights',WEIGHTS,[135,136,137],kind='table_definition',limits=['Source arithmetic points, not calibrated probabilities, moral worth or a complete outcome model.'])
add('I.XVIII','Domicile quality has exceptions','Domicile is assigned five dignities and likened to a person governing their own estate and fortunate circumstances, unless retrograde, combust or afflicted by a malevolent planet/aspect.',[135,136],requires=['Relevant planet/significator in own domicile.'],limits=['The dignity component and the qualified life-outcome analogy are separate.'])
add('I.XVIII','Whole-sign exaltation','Four dignities for being in the exaltation sign whether near its particular exaltation degree or not.',[136],kind='source_definition',limits=['The exact degree remains separate table information; it is not a prerequisite for these four points.'])
add('I.XVIII','Exalted angular character','An exalted, unimpeded, angular significator describes haughtiness, arrogance and assuming more than one\'s due.',[136],requires=['Relevant significator exalted.','Unimpeded.','Angular.'],limits=['Do not infer moral goodness from greater essential power.'])
add('I.XVIII','Fixed-star explanation is conjecture','Lilly conceives the stronger expression in certain places as due to more same-nature fixed stars nearer the ecliptic.',[136],kind='author_conjecture',limits=['No fixed-star enumeration or causal validation is provided in this extraction.'])
add('I.XVIII','Triplicity depends on time','Triplicity earns three dignities only for the appropriate day/night ruler; Mars alone rules the watery triplicity both day and night under Lilly\'s declared Ptolemy/Naibod profile.',[136,139],limits=['No participating third triplicity lord is silently introduced from another source.','Attribution to Ptolemy is Lilly\'s claim; numerical/source parity must be separately checked.'])
add('I.XVIII','Nocturnal Aries example','Sun in Aries at night retains four exaltation dignities but no triplicity dignity; Jupiter there at night would receive three triplicity dignities.',[136],kind='worked_calculation',limits=['These are the specified components, not a whole-chart total.'])
add('I.XVIII','Triplicity life analogy','Triplicity describes modest possession of goods, good descent and a good present condition, but less than the preceding two dignities.',[136],limits=['No modern socio-economic prediction is established.'])
add('I.XVIII','Terms and their limited implication','Two dignities in one\'s own terms by day or night; a planet fortified only by term primarily indicates its bodily constitution/temper, rather than extraordinary fortune or public eminence.',[136,137],requires=['The only fortification in this interpretive branch is own term.'],limits=['Presence of other fortifications defeats the terms-only antecedent; no inference of poverty from lack of extraordinary abundance.'])
add('I.XVIII','Face and peregrinity','One dignity for own decanate/decurie/face; this prevents calling the planet peregrine. Examples: Mars in first ten Aries degrees, Mercury first ten Taurus degrees.',[137],kind='source_definition',limits=['Exact within-sign boundary representation must be declared.','This is not a full peregrinity definition covering every later complication.'])
add('I.XVIII','Face-only insecurity','Little or no dignity beyond face is compared with a person almost turned out of doors, struggling to keep credit; in genealogies, a family scarcely maintaining itself.',[137],requires=['Face is the little/sole remaining dignity in the source analogy.'],limits=['Face does not imply substantial good fortune merely because it prevents peregrinity.'])
add('I.XVIII','Accidental strength is separate','Directness, swiftness, angularity, trine/sextile to Jupiter or Venus and conjunction with notable fixed stars are examples of accidental fortification.',[137],kind='source_definition',limits=['This list is not a complete numerical accidental-strength engine.'])
add('I.XVIII','Author\'s table provenance claim','Lilly acknowledges differences among Arabian, Greek and Indian traditions, claims subsequent Greek/European adherence to Ptolemy, and labels the table according to Ptolemy.',[137,138],kind='author_attribution',limits=['Preserve as Lilly\'s historical claim, not independently verified unanimity.','Do not overwrite another transmitted table because of the label alone.'])
for s in SIGNS:
    add('I.XVIII',s+' dignity table row',{'domicile':DOMICILES[s],'exaltation':EXALTATIONS.get(s),'triplicity':TRIPLICITY[['fire','earth','air','water'][SIGNS.index(s)%4]],'term_endpoints':TERMS[s],'face_rulers':FACES[s]},[138],kind='table_transcription',requires=['Select the later p104 table witness explicitly.','Ordinal lookup treats 1..30 as numbered degrees, not floating-point longitude bins.'],limits=['Earlier planet-by-planet lists remain independently retained.','No automatic repair of earlier gaps or overlaps.'])
add('I.XVIII','Domicile, detriment and fall definitions','The five planets have two domiciles, Sun and Moon one each. Detriment is in the sign opposite a domicile; fall opposite the exaltation sign. The table distinguishes diurnal/nocturnal domiciles.',[138,139],kind='source_definition',limits=['Luminary day/night lettering is visually ambiguous in this witness; only the unambiguous five-planet markings are normalized.'])
add('I.XVIII','Table endpoint explanation','The first six degrees of Aries are Jupiter\'s terms, then to fourteen Venus\'s; faces are the first ten Mars, next ten Sun and last ten Venus.',[139],kind='source_definition',limits=['The compiler explicitly adopts numbered degrees for integer lookups. Exact continuous boundaries are not silently inferred from ordinal language.'])
add('I.XVIII','Nodes and unsigned debility labels','The table includes the Head at Gemini 3 and Tail at Sagittarius 3 in the exaltation column, and unsigned 5 and 4 below detriment and fall.',[138],kind='table_transcription',limits=['Nodes are not added to the seven-planet score function.','No signed net debility score is created from this table alone; later accidental/debility instructions remain to be read.'])

UNRESOLVED = [
 ('U01','Marginal Saturn qualifier','Scope of the peregrine/unfortunate margin over physical versus character clauses.',[118]),
 ('U02','Jupiter curl parenthesis','Image provisionally suggests fiery; OCR says Aery. Keep both and exclude this token from executable discrimination.',[118]),
 ('U03','Mars absent Jupiter branch','The six domicile branches do not supply Jupiter; do not infer a neutral or favourable seventh case.',[119]),
 ('U04','Feral Sagittarius boundary','Last part is not a numerical starting degree; do not silently set fifteen degrees.',[123]),
 ('U05','Mixed modalities','The three paired Ascendant/ruler rules do not specify mixed categories, ties or missing inputs.',[123]),
 ('U06','Sign gender and medicine','Historical social/gender/illness labels are not modern diagnostic categories.',[122,123,127,133]),
 ('U07','Antiscion latitude/declination interpretation','Degree symmetry is specified; physical declination of a latitude-bearing planet, visibility, and modern astronomical parity are not checked.',[124]),
 ('U08','Antiscion orb and aspect quality','No contact orb, priority, timing scale or independent-evidence weight is supplied.',[124,126]),
 ('U09','Printed subtraction narration','The text says subtract 25 minutes yet obtains 25 from 60; the setup has 35. Retain the error and correct arithmetic as different records.',[125]),
 ('U10','Antiscion edge convention','Zero/30-degree boundaries require an explicit continuous-coordinate or ordinal convention; no unlabelled bin conversion.',[124,125]),
 ('U11','Ascending-time endpoints','Examples sample near-boundary degrees, not exact whole signs; no extrapolated exact durations or universal latitude rule.',[126,127]),
 ('U12','Directional fields','North/South in sign portraits and the earlier equatorial halves must remain context-labelled rather than overwritten to agree.',[122,128,129,130,131,132,133]),
 ('U13','Page and chapter labels','Two XVI headings; printed 17 at PDF121; PDF128/129 labelled95/94; PDF131 incomplete9. Sequence positions remain separate from labels.',[120,121,127,128,129,131]),
 ('U14','Historical place identity','Preserve overlapping and apparently anomalous assignments and qualifiers, including Calabria in Sicilia; no modern country mapping.',[127,128,129,130,131,132,133]),
 ('U15','Disease wording','Descending in the sixth in XVII is not silently replaced with sixth cusp or Descendant.',[134]),
 ('U16','Greater testimonies','No complete weighting, tie handling or conflict-resolution algorithm is specified by this instruction.',[134,135]),
 ('U17','Fortification mixed with impediment','The essential component may remain while its happy-condition analogy is disqualified; a full combined score requires later definitions.',[135,136,137]),
 ('U18','Ptolemy label','A table said to be according to Ptolemy is not proof of equality with every Ptolemaic witness.',[137,138,139]),
 ('U19','Ordinal terms/faces','Earlier enumerations and later table differ; the current comparison reports differences but chooses no validated source winner.',[138,139]),
 ('U20','Solar/lunar domicile lettering','Stacked diurnal/nocturnal markings by luminaries are not normalized beyond what is unambiguous.',[138]),
 ('U21','Debility signs','Bottom 5/4 under detriment/fall are unsigned; a complete signed net score is deferred to the later instructions.',[138]),
 ('U22','Exaltation point and sign','Exaltation points are transcribed separately; the four-point rule is whole sign and does not establish additional exact-degree strength.',[136,138]),
 ('U23','Fixed-star causal conjecture','The proposed explanation for exaltation/strength is an author conjecture, not a tested fixed-star computation.',[136]),
 ('U24','Significator admission','The catalogue cannot determine by itself who/what the planet signifies; later topic-specific procedures remain required.',[118,134,135]),
]

DIGNITY_TABLE = {
 'source_id':SOURCE_ID,'source_sha256':SOURCE_SHA,'pdf_page':138,'printed_label':'104 (written label above table)',
 'witness_profile':'LILLY_1647_P104_TABLE','degree_representation':'numbered degrees 1..30, integer lookup with inclusive endpoints; continuous-coordinate conversion deliberately separate',
 'terms':TERMS,'faces':FACES,'domiciles':DOMICILES,'exaltations':EXALTATIONS,'triplicity':TRIPLICITY,'essential_weights':WEIGHTS,
 'five_planet_domicile_day_night':{'Mars':{'Aries':'day','Scorpio':'night'},'Venus':{'Taurus':'night','Libra':'day'},'Mercury':{'Gemini':'day','Virgo':'night'},'Jupiter':{'Sagittarius':'day','Pisces':'night'},'Saturn':{'Capricorn':'night','Aquarius':'day'}},
 'luminary_domicile_day_night':'not normalized; stacked markings remain ambiguous',
 'detriment_rulers':{s:DOMICILES[SIGNS[(i+6)%12]] for i,s in enumerate(SIGNS)},
 'fall_rulers':{SIGNS[(SIGNS.index(s)+6)%12]:v[0] for s,v in EXALTATIONS.items()},
 'unsigned_bottom_debility_numbers':{'detriment':5,'fall':4},
 'mapping_provenance':'Terms, faces, domicile, exaltation and triplicity transcribed from table. Opposite-sign detriment/fall fields use the table explanation, not an extra predictive rule.',
 'runtime_promoted':False,
}

def write(name, value):
    (ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    write('PORTRAITS_AND_SIGNS.json',{'source_id':SOURCE_ID,'source_sha256':SOURCE_SHA,'brief_planet_profiles':BRIEF_PROFILES,'mars_domicile_branches':MARS_DOMICILE_BRANCHES,'colours':COLOURS,'sign_groups':SIGN_GROUPS,'feral':FERAL,'sign_profiles':SIGN_PROFILES,'historical_status':'Source-reference only. No personal chart or outcome input.'})
    write('DIGNITY_TABLE_P104.json',DIGNITY_TABLE)
    write('ANTISCIA_AND_EXAMPLES.json',{'source_id':SOURCE_ID,'source_sha256':SOURCE_SHA,'pairs':ANTISCIA_PAIRS,'degree_pairs':[[n,30-n] for n in range(1,16)],'minute_pairs':[[n,60-n] for n in range(1,31)],'saturn_example':{'input':'Leo 20:35','antiscion':'Taurus 9:25','contrantiscion':'Scorpio 9:25'},'solar_example':{'input':'Taurus 10:00','antiscion':'Leo 20:00'},'rising_examples':[{'sign':'Leo','start_degree_minute':[0,21],'end_degree_minute':[29,40],'start_time':[0,18],'end_time':[3,6],'duration_minutes':168,'pdf':126},{'sign':'Aquarius','start_degree_minute':[0,57],'end_degree_minute':[29,28],'start_time':[16,4],'end_time':[17,8],'duration_minutes':64,'pdf':127}],'rising_scope':'Near-boundary source table segments; not freshly computed full-sign rising times.'})
    write('RULES.json',{'schema_version':2,'batch_id':'B02c','records_count':len(RULES),'first_record_number':231,'last_record_number':230+len(RULES),'records':RULES})
    write('UNRESOLVED.json',{'batch':'B02c','count':len(UNRESOLVED),'issues':[{'id':'LI.B02c.'+k,'topic':t,'issue':s,'pdf_pages':p,'disposition':'RETAINED_NOT_SILENTLY_RESOLVED'} for k,t,s,p in UNRESOLVED]})
    actual={121:'17',128:'95',129:'94',131:'9 (incomplete label)',138:'104 (written label)'}
    write('READING_RECEIPT.json',{'source_id':SOURCE_ID,'source_sha256':SOURCE_SHA,'source_bytes':141842963,'source_pdf_pages':894,'sections':SECTIONS,'section_units_completed':5,'pdf_pages_text_read':list(range(118,140)),'pdf_pages_images_inspected':list(range(118,140)),'scope_end':'PDF139 before chapter XIX; XIX opening and PDF140 retrieved incidentally but not complete','pages':[{'pdf':p,'expected_sequence_label':p-34,'observed_label':actual.get(p,str(p-34))} for p in range(118,140)],'no_new_ocr':True,'image_process':'Existing PDF text plus 105 dpi page renders; JPEG transfer copies. Full-page originals inspected. Auxiliary crop action was blocked and not retried.','independent_semantic_review':False,'personal_outcomes_inspected':False,'source_file_in_git':False,'next':{'pdf_page':139,'printed_page':105,'heading':'Chap.XIX Of severall Termes, Aspects, words of Art, Accidents...'}})
    write('TEXT_IMAGE_CHECKS.json',{'checks':[
      {'pdf':118,'status':'QUALIFIER_CONFIRMED','detail':'Saturn adverse-character margin says peregrine or unfortunate.'},
      {'pdf':118,'status':'UNRESOLVED_TOKEN','detail':'Jupiter curl parenthesis provisionally fiery versus text Aery; not a scoring predicate.'},
      {'pdf':119,'status':'GLYPHS_CONFIRMED','detail':'Mars domicile branch Venus/Mercury/Mars/Saturn/Sun/Moon; no Jupiter clause.'},
      {'pdf':120,'status':'GLYPHS_CONFIRMED','detail':'All seven planetary and twelve sign colour entries; first XVI heading.'},
      {'pdf':123,'status':'GLYPHS_CONFIRMED','detail':'Sagittarius present in bestial list; feral restricted to last part; Mercury/Saturn in mute qualifier.'},
      {'pdf':124,'status':'TABLE_CONFIRMED','detail':'Six antiscion pairs and Taurus10/Leo20 example.'},
      {'pdf':125,'status':'PRINTED_DISCREPANCY','detail':'Correct 30:00-20:35=9:25 alongside narrative subtract25; 15 degree and30 minute rows seen.'},
      {'pdf':126,'status':'NUMBERS_CONFIRMED','detail':'Leo00:21 at00:18,29:40 at03:06; difference2:48.'},
      {'pdf':127,'status':'NUMBERS_AND_HEADING_CONFIRMED','detail':'Aquarius00:57 at16:04,29:28 at17:08; difference1:04; second XVI.'},
      {'pdf':130,'status':'GLYPHS_CONFIRMED','detail':'Virgo conditional Mercury here plus Moon in Cancer.'},
      {'pdf':132,'status':'AUTHOR_QUALIFICATION_CONFIRMED','detail':'Capricorn white-hair observation and family conjecture.'},
      {'pdf':133,'status':'GLYPHS_CONFIRMED','detail':'Aquarius modifier Saturn in Capricorn/Aquarius; anomalous place labels retained.'},
      {'pdf':135,'status':'GLYPHS_CONFIRMED','detail':'Domicile example Jupiter in Sagittarius, not OCR Capricorn.'},
      {'pdf':136,'status':'CONDITIONS_CONFIRMED','detail':'Whole-sign exaltation; unimpeded angular haughtiness; night Sun/Jupiter example.'},
      {'pdf':137,'status':'GLYPHS_CONFIRMED','detail':'Mars first Aries face and Mercury first Taurus face; accidental strength distinct.'},
      {'pdf':138,'status':'TABLE_TRANSCRIBED','detail':'Twelve dignity rows with60 term and36 face cells; node exaltations kept distinct from7 planets; unsigned debility labels.'},
      {'pdf':139,'status':'BOUNDARY_CONFIRMED','detail':'End of table explanation immediately before XIX; not chapter XIX completion.'}
    ]})
    print('GENERATED',len(RULES),'records;',len(UNRESOLVED),'unresolved issues')
    for name in ['RULES.json','DIGNITY_TABLE_P104.json','PORTRAITS_AND_SIGNS.json']:
        b=(ROOT/name).read_bytes(); print(name,len(b),hashlib.sha256(b).hexdigest())

if __name__=='__main__':
    main()
