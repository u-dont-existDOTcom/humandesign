"""Same-volume errata and retained limits after two split independent source reviews."""
from pathlib import Path
import json
B=Path(__file__).resolve().parent
def save(p,x):(B/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n")
E=[
  {"printed_page":305,"pdf_page":339,"line":22,"erratum":"dele [conjunction glyph]","original_reading":"Conjunction, square, opposition in marriage-hard-aspect list","corrected_reading":"Square or opposition, not conjunction","body_match":"MATCHED by sole conjunction symbol in that source clause; counted body text line possibly one different","used_in":["R1961"],"source_image":"evidence/pdf-339.png"},
  {"printed_page":306,"pdf_page":340,"line":26,"erratum":"read undertaken","original_reading":"Source text/copy word in journey branch","corrected_reading":"undertaken","body_match":"REQUIRES EXACT BODY LINE RECHECK; no silent emendation","used_in":["R1971"],"source_image":"evidence/pdf-340.png"},
  {"printed_page":307,"pdf_page":341,"line":28,"erratum":"read for [Sun glyph] and [Mars glyph]","original_reading":"Hand mark/overprint appears near plurality-of-husbands rule","corrected_reading":"for Sun and Mars, subject to copy legibility","body_match":"ORIGINAL GLYPH UNCERTAIN; original-volume erratum directs reading and marginal handwritten mark is secondary","used_in":["R1986"],"source_image":"evidence/pdf-341.png"},
  {"printed_page":312,"pdf_page":346,"line":17,"erratum":"read it is no good","original_reading":"it is not to trust alwayes to this judgment","corrected_reading":"it is no good to trust alwayes to this judgment","body_match":"MATCHED against source moral-character confidence caveat","used_in":["R2040"],"source_image":"evidence/pdf-346.png"},
  {"printed_page":315,"pdf_page":349,"line":7,"erratum":"read [Dragon's Tail / South Node glyph]","original_reading":"blotted original seventh-lord/Mars/node clause","corrected_reading":"South Node glyph in conditional clause","body_match":"MATCHED with blotted body glyph; handwritten marginal correction not presumed 1647 authorial","used_in":["R2062"],"source_image":"evidence/pdf-349.png"},
  {"printed_page":315,"pdf_page":349,"line":10,"erratum":"read seventh","original_reading":"abbreviated or malformed seventh in source print","corrected_reading":"seventh","body_match":"MATCHED source seventh-lord clause; original page number appears misprinted 215","used_in":["R2064"],"source_image":"evidence/pdf-349.png"},
]
save("ERRATA_COLLATION.json",{"batch":"B02s","original_errata_image":"evidence/errata-888.png","source_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
 "entries":E,"count":len(E),"original_body_unchanged":True,"line_number_ambiguity":"Errata printer's line number may differ from modern image line count; direct target wording is stronger than arithmetic line alignment."})
U=json.loads((B/"recovery/original_draft/UNRESOLVED.json").read_text())
old=len(U["limits"]);assert U["retained_count"]==old==34
issues=[
 "p304 first/unwilling consent reading contradicts p303 goodwill; original volume supplies no p304 erratum. Do not emend to willing.",
 "p303 Alkindus first/seventh lord application not explicitly restricted to sextile or trine in its first rule.",
 "p303 Venus-Sun rule has three AND-linked conditions; Sun must behold its own dispositor, not necessarily ascendant lord.",
 "p304 Moon in tenth, not seventh, for first mediation claim; copy image reviewed independently.",
 "p305 original-volume erratum deletes conjunction symbol from difficulty list, leaving square and opposition.",
 "p305 two alternative sources for who loves more are reversed by Lilly at p317 explicitly 'contrary to ancients'; neither is privileged for empirical truth.",
 "p305 hindrance method concerns evil planet prohibiting/reception/interjecting rays, separate from beneficial translation of light.",
 "p306 allegations about children, past relations, perceived infertility etc are described as others' objections/scandal/fears, not established facts.",
 "p307 p28 original-volume erratum for Sun/Mars has uncertain nearby body and handwritten letters; retain source correction separately.",
 "p308 person-type rule Sun trine/sextile Saturn means diligent/wise ('painfull'), not painful or Moon/Mars.",
 "p309 legitimacy affliction requires Saturn/Mars not themselves the question's significators; South Node is alternative.",
 "p310 Moon square good planets interpreted 'by dead men'; conjunction good planets 'by own industry'; no source opposition branch.",
 "p311 Arabic aphorism Moon early CAPRICORN (not Virgo) carries three extreme alternative outcomes; never treat as evidence.",
 "p311 Arabic aphorisms have printed caution not to credit without corroborating significators.",
 "p312 confidence caveat original erratum reads 'it is no good to trust always', while gendered authorial stereotype remains printed.",
 "p312 author's dissent includes Mars in Leo/Scorpio ascending with 'querent' printed; exact damaged glyph/word remains qualified.",
 "p313 source expressly says woman accused in some cases was not involved, gave no admittance, or was the subject of slander.",
 "p314 one source alternative describes conduct through force or unwilling involvement, not a voluntary choice or proven wrongdoing.",
 "p315 page number print appears 215, but sequential original PDF349 maps to printed315; errata for p315 applies there.",
 "p315 original body glyph blotted; original erratum supplies South Node while handwriting in margin is reader annotation.",
 "p316 'tardy' may mean blameworthy/at fault rather than a temporal delay; no dictionary independently checked.",
 "p316 many planet-in-seventh rules deny current physical involvement or actual alleged infidelity; source distinctions matter.",
 "p317 marriage completion expressly assumes the querent's free will and consent; source astrology cannot supply consent.",
 "p317 mediator third-planet gender identification is generic masculine/diurnal versus feminine/nocturnal, not specified Sun/Mars.",
 "p318 fatherhood suspicion only when prior supportive conditions absent, with source hedge and word 'stuprated' not modernized.",
 "p319 reconciliation source may describe abuse/estrangement and lack of later respect; not current relationship-safety advice.",
 "The two source-image reviewers worked overlapping ranges PDF336–345 and PDF344–353; neither alone audited all eighteen text pages.",
 "Initial review stage paths source_images/ are isolated copies; canonical evidence paths are evidence/ and verified by manifest.",
 "The 187 draft IDs are preserved, with independently recovered missing original clauses appended and a separate reading-order manifest.",
 "Historical marriage/gender, death, paternity and intimate-history claims have no independently authenticated outcome records.",
]
for i,description in enumerate(issues,old+1):
 U["limits"].append({"id":f"U{i:02d}","description":description,"status":"RETAINED"})
U["retained_count"]=len(U["limits"])
U["status"]="CORRECTED_SOURCE_REVIEW_UNCERTAINTIES_RETAINED"
save("UNRESOLVED.json",U)
print(json.dumps({"same_volume_errata":len(E),"original_limits":old,"new_limits":len(issues),"retained_total":U["retained_count"]}))
