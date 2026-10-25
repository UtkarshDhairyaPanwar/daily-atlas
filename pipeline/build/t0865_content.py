from t0865_sec_a import S_HOOK, S_WHAT, S_MECH, S_EARLY, S_LIND, S_NAVY, S_LOST
from t0865_sec_b import S_DISC, S_ANCESTORS, S_HYBRIDS, S_TRAVEL
from t0865_sec_c import S_INDIA, S_MYTHS, S_TODAY, S_NOW, S_FACTS, S_RECAP

V = "2026-10-25"
SECTIONS = [S_HOOK, S_WHAT, S_MECH, S_EARLY, S_LIND, S_NAVY, S_LOST, S_DISC, S_ANCESTORS, S_HYBRIDS, S_TRAVEL,
            S_INDIA, S_MYTHS, S_TODAY, S_NOW, S_FACTS, S_RECAP]

# media and image patches applied to spotlights by id
MEDIA_PATCH = {
    "scurvy_body": ["vid_scishow"],
    "ascorbic_acid": ["vid_ted_vitamins"],
    "collagen_rope": ["vid_longnow"],
    "lind_rob": ["vid_vitc_test"],
    "sweet_orange": ["vid_genome"],
}
IMG_PATCH = {
    "limey": ["img_roses", "img_key_lime"],
    "navel_orange": ["img_parent_navel", "img_navel", "img_cec"],
    "bitter_orange": ["img_seville_patio"],
    "citrus_indica": ["img_citrus_indica", "img_citrus_map"],
    "sweet_orange": ["img_orange", "img_arnolfini", "img_orange_blossom"],
    "szent_gyorgyi": ["img_szg", "img_szeged_paprika"],
    "juice_squeeze": ["img_florida", "img_oj"],
    "cook_kraut": ["img_cook", "img_sauerkraut"],
}
for s in SECTIONS:
    for sp in s["spotlights"]:
        if sp["id"] in MEDIA_PATCH:
            sp["media_ids"] = MEDIA_PATCH[sp["id"]] + [m for m in sp["media_ids"] if m not in MEDIA_PATCH[sp["id"]]]
        if sp["id"] in IMG_PATCH:
            sp["image_ids"] = IMG_PATCH[sp["id"]]

HERO = {"image_id": "img_lemon", "kicker": "Day 865 · Food",
        "headline": "Citrus and scurvy: a cure found in 1601, lost, found and lost again, and a fruit born in the hills of north-east India"}

GEO = {"centroid": [26.5, 96.5], "bbox": [20.0, 88.0, 30.0, 102.0], "neighbours": [],
       "regions": [{"id": "cradle", "name": "Citrus cradle", "note": "Eastern Assam, northern Myanmar, western Yunnan (Wu et al. 2018)"},
                   {"id": "garo", "name": "Garo Hills, Meghalaya", "note": "Nokrek National Citrus Gene Sanctuary"}]}

STATS = [
    {"key": "prevent_dose", "label": "Daily vitamin C that prevents scurvy", "value": 10, "unit": "mg", "year": "1940s to 1960s studies", "source_ids": ["wiki_scurvy"]},
    {"key": "us_rda_men", "label": "US adult recommendation, men", "value": 90, "unit": "mg/day", "year": "2000", "source_ids": ["wiki_vitc"]},
    {"key": "gulo_loss", "label": "When our ancestors lost the GULO gene", "value": 63, "unit": "million years ago", "year": "estimate", "source_ids": ["wiki_gulo"]},
    {"key": "lind_trial", "label": "Sailors in Lind's trial", "value": 12, "year": "1747", "source_ids": ["wiki_lind"]},
    {"key": "orange_world", "label": "World orange harvest", "value": 67, "unit": "million tonnes", "year": "2024", "source_ids": ["wiki_orange"]},
    {"key": "india_deficiency_north", "label": "Vitamin C deficiency, north India, age 60+", "value": 73.9, "unit": "%", "year": "2011 study", "source_ids": ["ravindran_2011"]},
    {"key": "florida_oranges", "label": "Florida oranges", "value": 12.95, "unit": "million boxes", "year": "2025-26", "source_ids": ["nass_2026"]},
]

MEDIA = [
    {"id": "vid_scishow", "kind": "video", "provider": "youtube", "url": "https://www.youtube.com/watch?v=rn5I5tfsFN8", "embed_url": "https://www.youtube-nocookie.com/embed/rn5I5tfsFN8", "title": "Why Scurvy Doesn't Make Sense to Science", "publisher": "SciShow", "license": "Standard YouTube licence. Embed only, do not download.", "verified_on": V, "verified_by": "youtube oembed returned 200 with this channel name"},
    {"id": "vid_ted_vitamins", "kind": "video", "provider": "youtube", "url": "https://www.youtube.com/watch?v=ISZLTJH5lYg", "embed_url": "https://www.youtube-nocookie.com/embed/ISZLTJH5lYg", "title": "How do vitamins work? (Ginnie Trinh Nguyen)", "publisher": "TED-Ed", "license": "Standard YouTube licence. Embed only, do not download.", "verified_on": V, "verified_by": "youtube oembed returned 200 with this channel name"},
    {"id": "vid_longnow", "kind": "video", "provider": "youtube", "url": "https://www.youtube.com/watch?v=rb5knx92oww", "embed_url": "https://www.youtube-nocookie.com/embed/rb5knx92oww", "title": "The Science of Scurvy (Scurvy Salon)", "publisher": "The Long Now Foundation", "license": "Standard YouTube licence. Embed only, do not download.", "verified_on": V, "verified_by": "youtube oembed returned 200 with this channel name"},
    {"id": "vid_vitc_test", "kind": "video", "provider": "youtube", "url": "https://www.youtube.com/watch?v=0c-y8wcFiRo", "embed_url": "https://www.youtube-nocookie.com/embed/0c-y8wcFiRo", "title": "How to test Vitamin C levels", "publisher": "BASF Science Club", "license": "Standard YouTube licence. Embed only, do not download.", "verified_on": V, "verified_by": "youtube oembed returned 200 with this channel name"},
    {"id": "vid_terranova", "kind": "video", "provider": "youtube", "url": "https://www.youtube.com/watch?v=RR8aNabrWL8", "embed_url": "https://www.youtube-nocookie.com/embed/RR8aNabrWL8", "title": "The Ship 'Terra Nova' Leaving Harbour Towards the South Pole (1910)", "publisher": "BFI", "license": "Standard YouTube licence. Embed only, do not download.", "verified_on": V, "verified_by": "youtube oembed returned 200 with this channel name"},
    {"id": "vid_genome", "kind": "video", "provider": "youtube", "url": "https://www.youtube.com/watch?v=zch6FwjoVn4", "embed_url": "https://www.youtube-nocookie.com/embed/zch6FwjoVn4", "title": "UF/IFAS Research: Citrus Genome Sequenced", "publisher": "IFAS Video (University of Florida)", "license": "Standard YouTube licence. Embed only, do not download.", "verified_on": V, "verified_by": "youtube oembed returned 200 with this channel name"},
    {"id": "vid_ucr_grove", "kind": "video", "provider": "youtube", "url": "https://www.youtube.com/watch?v=izBdxeWSOL4", "embed_url": "https://www.youtube-nocookie.com/embed/izBdxeWSOL4", "title": "A Sweet Adventure: UC Riverside Citrus Grove Drone Tour", "publisher": "UC Riverside", "license": "Standard YouTube licence. Embed only, do not download.", "verified_on": V, "verified_by": "youtube oembed returned 200 with this channel name"},
    {"id": "vid_greening", "kind": "video", "provider": "youtube", "url": "https://www.youtube.com/watch?v=o2ds3HsYMB0", "embed_url": "https://www.youtube-nocookie.com/embed/o2ds3HsYMB0", "title": "What is Citrus Greening?", "publisher": "UF IFAS Extension Clay County", "license": "Standard YouTube licence. Embed only, do not download.", "verified_on": V, "verified_by": "youtube oembed returned 200 with this channel name"},
    {"id": "vid_psyllid", "kind": "video", "provider": "youtube", "url": "https://www.youtube.com/watch?v=DH2qvyw_BRg", "embed_url": "https://www.youtube-nocookie.com/embed/DH2qvyw_BRg", "title": "UF/IFAS Research: Citrus Psyllid", "publisher": "IFAS Video (University of Florida)", "license": "Standard YouTube licence. Embed only, do not download.", "verified_on": V, "verified_by": "youtube oembed returned 200 with this channel name"},
    {"id": "vid_nagpur", "kind": "video", "provider": "youtube", "url": "https://www.youtube.com/watch?v=f1N4QIUYMwI", "embed_url": "https://www.youtube-nocookie.com/embed/f1N4QIUYMwI", "title": "Nagpur Orange: orange farms at Nagpur (GI-TRIPS)", "publisher": "GI-TRIPS INDIA", "license": "Standard YouTube licence. Embed only, do not download.", "verified_on": V, "verified_by": "youtube oembed returned 200 with this channel name"},
    {"id": "vid_szg", "kind": "video", "provider": "youtube", "url": "https://www.youtube.com/watch?v=djGSrgXZeyY", "embed_url": "https://www.youtube-nocookie.com/embed/djGSrgXZeyY", "title": "Mire valo a fejunk? Szent-Gyorgyi Albert (archive film, Hungarian)", "publisher": "Nemzeti Archivum", "license": "Standard YouTube licence. Embed only, do not download.", "verified_on": V, "verified_by": "youtube oembed returned 200 with this channel name"},
]


def C(i, t, front, back, sec, src, core=False, img=None, spot=None, imgs=None):
    d = {"id": i, "type": t, "front": front, "back": back, "image_id": img, "spotlight_id": spot, "section_id": sec, "core": core, "source_ids": src}
    if imgs:
        d["image_ids"] = imgs
    return d


CARDS = [
    C("c01", "image", "This voyage of 1740 to 1744 lost about 1,400 of 1,900 men, mostly to scurvy. Whose?", "Commodore George Anson's voyage round the world. He still captured a Spanish treasure galleon in 1743.", "hook", ["wiki_anson", "wiki_lind"], True, "img_anson", "anson_voyage"),
    C("c02", "image", "What disease do these gums show?", "Scurvy: swollen, spongy gums that bleed, from lack of vitamin C.", "what_it_is", ["wiki_scurvy"], True, "img_gums", "scurvy_body"),
    C("c03", "cloze", "As little as ___ mg of vitamin C a day prevents and reverses scurvy.", "10 mg.", "what_it_is", ["wiki_scurvy"], True),
    C("c04", "fact", "How long without vitamin C before scurvy symptoms appear?", "At least a month; usually one to three months.", "what_it_is", ["wiki_scurvy"], False),
    C("c05", "why", "Why does vitamin C deficiency make gums bleed and wounds reopen?", "The enzymes that finish collagen (prolyl and lysyl hydroxylase) need vitamin C to keep their iron working. Without it, collagen is weak, so capillaries, gums and scars fail.", "mechanism", ["wiki_scurvy", "wiki_p4h"], True, None, "collagen_rope"),
    C("c06", "why", "Why can a rat make its own vitamin C but a human cannot?", "Humans, apes, monkeys and tarsiers carry a broken GULO gene, disabled about 63 million years ago. Rats still have a working one.", "mechanism", ["wiki_gulo"], True, None, "broken_gene"),
    C("c07", "image", "Which animal, by luck, gave scientists a scurvy model in 1907?", "The guinea pig. Like us, it cannot make vitamin C.", "discovery", ["wiki_holst"], True, "img_guinea_pig", "holst_frolich"),
    C("c08", "fact", "Which primates can still make their own vitamin C?", "Lemurs and lorises (strepsirrhines). Monkeys, apes and humans cannot.", "mechanism", ["wiki_gulo"], False),
    C("c09", "image", "In 1535 to 1536 his men were saved by a tree tea taught by the St Lawrence Iroquoians. Who?", "Jacques Cartier, at Stadacona (Quebec). The tree, annedda, was probably eastern white cedar.", "before_lind", ["wiki_cartier"], True, "img_cartier", "cartier_annedda"),
    C("c10", "fact", "In 1601, how did James Lancaster's ship stay healthy when three others got scurvy?", "Every morning his men on the Red Dragon took three spoonfuls of bottled lemon juice.", "before_lind", ["wiki_lancaster"], False, "img_lancaster", "lancaster_1601"),
    C("c11", "cloze", "John Woodall's 1617 book The ___ told East India Company surgeons to use lemon juice.", "The Surgeon's Mate.", "before_lind", ["wiki_woodall"], False, "img_woodall_scurvy", "woodall"),
    C("c12", "image", "Who ran the twelve-sailor scurvy trial of 1747?", "James Lind, surgeon of HMS Salisbury.", "lind", ["wiki_lind"], True, "img_lind", "lind_trial"),
    C("c13", "fact", "In Lind's trial, which pair recovered fastest?", "The pair given two oranges and a lemon a day. One was fit for duty in six days.", "lind", ["wiki_lind"], False, None, "lind_trial"),
    C("c14", "why", "Why did Lind's 'rob' fail as a scurvy remedy?", "He concentrated fruit juice by heating it for hours. Heat destroys vitamin C.", "lind", ["jll_trohler"], True, "img_treatise_1757", "lind_rob"),
    C("c15", "fact", "Who paid for the 1953 Edinburgh plaque to James Lind?", "The citrus growers of California and Arizona.", "lind", ["wiki_lind"], False, "img_haslar", "haslar"),
    C("c16", "image", "This captain got his crew to eat sauerkraut by serving it at the officers' table. Who?", "James Cook, on the Endeavour, 1768 to 1771.", "navy", ["hektoen_kraut"], True, "img_cook", "cook_kraut"),
    C("c17", "cloze", "The Royal Navy ordered a daily lemon juice ration for every ship in ___.", "1795, after HMS Suffolk reached India scurvy-free.", "navy", ["wiki_scurvy", "wiki_blane"], True),
    C("c18", "image", "Which physician pushed the Admiralty to adopt lemon juice in 1795?", "Gilbert Blane, commissioner of the Sick and Wounded Board.", "navy", ["wiki_blane"], False, "img_blane", "blane"),
    C("c19", "image", "Name this coastal plant, carried dried on ships against scurvy.", "Scurvygrass, Cochlearia officinalis.", "navy", ["wiki_scurvy"], False, "img_scurvygrass", "scurvygrass"),
    C("c20", "why", "Why did the Navy's switch from lemons to limes bring scurvy back?", "West Indian limes have about half the vitamin C of lemons, and the juice was further degraded by air, light, copper pipes and storage.", "lost_again", ["wiki_scurvy", "wiki_limey"], True, None, "limey"),
    C("c21", "image", "What does this bottle explain about the word 'limey'?", "Rose's lime juice (patented 1867). Lime juice rations gave British sailors the nickname lime-juicers, then limeys.", "lost_again", ["wiki_scurvy", "wiki_limey"], False, "img_roses", "limey"),
    C("c22", "image", "This ship's sledge parties were crippled by scurvy in 1876. Name the expedition.", "The British Arctic Expedition under George Nares (HMS Alert).", "lost_again", ["arctic_nares"], False, "img_alert", "nares_1875"),
    C("c23", "fact", "Who walked 35 miles alone in 1912 to save Edward Evans from scurvy?", "Tom Crean, on Scott's Terra Nova expedition.", "lost_again", ["wiki_terranova"], False, "img_evans", "scott_evans"),
    C("c24", "image", "Which Hungarian scientist got vitamin C in bulk from paprika in 1932?", "Albert Szent-Gyorgyi, at Szeged. Nobel Prize in medicine, 1937.", "discovery", ["nlm_szeged", "nobel_szg"], True, "img_szg", "szent_gyorgyi"),
    C("c25", "fact", "What does the name 'ascorbic acid' mean?", "'Against scurvy' (a-scorbic), proposed by Haworth and Szent-Gyorgyi in 1933.", "discovery", ["wiki_vitc"], False),
    C("c26", "image", "Who first synthesised vitamin C, in 1933?", "Norman Haworth, Birmingham. Nobel Prize in Chemistry, 1937.", "discovery", ["wiki_haworth"], False, "img_haworth", "haworth"),
    C("c27", "fact", "Where did citrus originate, according to the 2018 Nature genome study?", "The south-east foothills of the Himalayas: eastern Assam, northern Myanmar, western Yunnan.", "ancestors", ["nature_wu2018"], True),
    C("c28", "fact", "Name the three ancestral species behind most commercial citrus.", "Citron, pomelo and mandarin.", "ancestors", ["wiki_citrus"], False),
    C("c29", "image", "Name this oldest cultivated citrus, the parent of the lemon.", "Citron (Citrus medica).", "ancestors", ["wiki_citron"], False, "img_citron", "citron"),
    C("c30", "image", "The largest citrus fruit and the sweet orange's mother. Name it.", "Pomelo (Citrus maxima).", "ancestors", ["wiki_pomelo", "wiki_orange"], False, "img_pomelo", "pomelo"),
    C("c31", "cloze", "The sweet orange is a cross of pomelo and ___.", "Mandarin (about 42% pomelo, 58% mandarin).", "hybrids", ["wiki_orange"], True),
    C("c32", "cloze", "A true lemon is a hybrid of citron and ___.", "Bitter (Seville) orange.", "hybrids", ["wiki_lemon"], False),
    C("c33", "image", "Name this fingered fruit with no juice inside.", "Buddha's hand, a variety of citron.", "hybrids", ["wiki_buddha"], False, "img_buddha", "buddhas_hand"),
    C("c34", "image", "This knobbly fruit grows on a tree with hourglass-shaped double leaves. Which citrus?", "Makrut (kaffir) lime, Citrus hystrix.", "hybrids", ["wiki_kaffir"], False, "img_kaffir", "kaffir_lime"),
    C("c35", "image", "What is the fruit inside these pearls, nicknamed citrus caviar?", "Australian finger lime, Citrus australasica.", "hybrids", ["wiki_lime"], False, "img_finger_lime", "finger_lime"),
    C("c36", "image", "This tree in Riverside, California, is the parent of which famous fruit?", "The Washington navel orange, a seedless mutant from Bahia, Brazil, planted in 1873.", "travel", ["wiki_navel"], True, "img_parent_navel", "navel_orange"),
    C("c37", "image", "Which festival needs this citron?", "Sukkot. It is the etrog, one of the four species.", "travel", ["wiki_etrog"], False, "img_etrog", "etrog"),
    C("c38", "fact", "Trace the word 'orange' back as far as it goes.", "English from French and Italian, from Arabic naranj, Persian narang, Sanskrit naranga; possibly Dravidian (Tamil naram) or a north-east Indian language such as Garo.", "india", ["lldf_orange"], False),
    C("c39", "image", "Botanically, what is the 'Nagpur orange'?", "A mandarin (Citrus reticulata). GI-tagged in 2014.", "india", ["dte_nagpur_gi"], True, "img_nagpur", "nagpur_orange"),
    C("c40", "image", "This mandarin was bred in California in 1915 and now rules Punjab's citrus. Name it.", "Kinnow (King x Willowleaf), released in 1935. Sirsa Kinnow was registered as a GI in 2026.", "india", ["ucr_kinnow", "theprint_kinnow"], True, "img_kinnow", "kinnow"),
    C("c41", "image", "Which Indian fruit, not a citrus, can carry several times the vitamin C of an orange?", "Amla (Indian gooseberry): about 193 to 720 mg per 100 g across cultivars.", "india", ["newsmed_amla"], False, "img_amla", "amla"),
    C("c42", "fact", "Where is India's National Citrus Gene Sanctuary?", "Nokrek, in the Garo Hills of Meghalaya, home of the Indian wild orange (memang narang).", "india", ["dte_citrus_indica"], False, None, "citrus_indica"),
    C("c43", "image", "Where does the name of this sweet lime come from?", "Mosambi, from Mozambique, via Portuguese traders.", "india", ["wiki_limetta"], False, "img_mosambi", "mosambi"),
    C("c44", "fact", "Why did Indian soldiers at Kut in 1916 get scurvy?", "Food ran short and many refused horsemeat, fearing being shunned at home; without fresh meat or vegetables, scurvy filled the hospital.", "india", ["scroll_kut"], False, "img_kut", "kut_1916"),
    C("c45", "fact", "What did the 2013 Cochrane review find about vitamin C and colds?", "No fewer colds in ordinary people; colds about 8% shorter in adults; risk halved under extreme physical stress.", "myths", ["cochrane_2013"], True, "img_pauling", "pauling"),
    C("c46", "compare", "Which of these two holds more vitamin C, weight for weight?", "Guava (left), about 228 mg per 100 g, against about 53 for an orange (right).", "myths", ["wiki_vitc"], False, "img_guava", "c_champions", ["img_guava", "img_orange"]),
    C("c47", "fact", "How did US child scurvy hospital rates change from 2016 to 2020?", "From 8.2 to 26.7 per 100,000 stays, roughly tripling.", "scurvy_today", ["reikersdorfer_2024"], False),
    C("c48", "image", "This 2 to 3 mm insect spreads which citrus disease?", "The Asian citrus psyllid spreads citrus greening (huanglongbing).", "now", ["wiki_hlb"], True, "img_psyllid", "greening"),
    C("c49", "why", "What made Lind's 1747 experiment a controlled trial and not just an observation?", "He picked patients with similar illness, kept diet and quarters the same, and compared several treatments side by side at the same time.", "lind", ["wiki_lind", "jll_trohler"], False),
    C("c50", "fact", "What was the weak point of Lind's trial, by modern standards?", "Only two patients per treatment, no random allocation, and the fruit ran out after six days; he later diluted his own finding with theory.", "lind", ["jll_trohler"], False),
    C("c51", "compare", "Which picture shows the fruit that actually kept the Navy healthy from 1795?", "Left: the Mediterranean lemon. Right: the West Indian lime, about half the vitamin C.", "lost_again", ["wiki_limey"], False, "img_lemon", "limey", ["img_lemon", "img_key_lime"]),
    C("c52", "map", "Where was Florida's citrus collapse measured, and how big?", "Florida: 244 million boxes of oranges in 1997-98, 12.95 million in 2025-26, and a 10 million box forecast for 2026-27 (October 2026).", "now", ["nass_1999", "nass_2026", "ffp_oct2026"], False),
]

QB = []


def Q(i, t, prompt, answer, expl, src, sec, spot=None, diff=1, **kw):
    d = {"id": i, "type": t, "prompt": prompt, "answer": answer, "explanation": expl, "source_ids": src, "section_id": sec, "spotlight_id": spot, "difficulty": diff}
    d.update(kw)
    return d


QUIZ_BANK = [
    Q("qb_anson", "mcq", "Roughly how many of Anson's 1,900 men died on his 1740 to 1744 voyage?", 2, "About 1,400, mostly of scurvy.", ["wiki_lind"], "hook", "anson_voyage", options=["About 100", "About 500", "About 1,400", "All of them"]),
    Q("qb_10mg", "mcq", "How much vitamin C a day is enough to prevent scurvy?", 0, "About 10 mg. Recommendations are higher, 75 to 90 mg in the US, for other reasons.", ["wiki_scurvy"], "what_it_is", options=["10 mg", "100 mg", "1,000 mg", "10 grams"]),
    Q("qb_onset", "true_false", "Scurvy can appear within a week of stopping vitamin C.", False, "It takes at least a month; the Iowa prison volunteers showed first signs at about four weeks.", ["wiki_scurvy"], "what_it_is"),
    Q("qb_gulo", "odd_one_out", "Which of these can make its own vitamin C?", 2, "Rats have a working GULO gene. Humans, guinea pigs and monkeys do not.", ["wiki_gulo"], "mechanism", "broken_gene", options=["Human", "Guinea pig", "Rat", "Monkey"]),
    Q("qb_lancaster", "true_false", "In 1601 James Lancaster gave lemon juice to the crew of one of his four ships, and that ship stayed healthier.", True, "His Red Dragon crew took three spoonfuls each morning; the other three ships were ravaged.", ["wiki_lancaster"], "before_lind", "lancaster_1601"),
    Q("qb_cartier", "mcq", "What saved Cartier's men in the winter of 1535 to 1536?", 1, "A tea of annedda, probably eastern white cedar, taught by the St Lawrence Iroquoians.", ["wiki_cartier", "wiki_scurvy"], "before_lind", "cartier_annedda", options=["Lemon juice", "A cedar tea", "Sauerkraut", "Seal meat"]),
    Q("qb_lind_pairs", "mcq", "How many sailors were in Lind's 1747 trial?", 1, "Twelve, in six pairs.", ["wiki_lind"], "lind", "lind_trial", options=["Six", "Twelve", "Fifty", "350"]),
    Q("qb_rob", "true_false", "Lind's boiled fruit concentrate, the rob, was a strong scurvy cure.", False, "Heating destroyed the vitamin C.", ["jll_trohler"], "lind", "lind_rob"),
    Q("qb_cook", "mcq", "How did Cook persuade his crew to eat sauerkraut?", 3, "He had it served to the officers; once the men saw their superiors valued it, they wanted it.", ["hektoen_kraut"], "navy", "cook_kraut", options=["Flogging", "Paying them", "Mixing it with rum", "Serving it at the officers' table"]),
    Q("qb_1795", "mcq", "Which ship's scurvy-free voyage to India helped persuade the Admiralty in 1795?", 0, "HMS Suffolk sailed in 1794 with lemon juice and reached Madras healthy after a 23-week non-stop voyage.", ["wiki_scurvy", "wiki_lind"], "navy", options=["HMS Suffolk", "HMS Salisbury", "HMS Centurion", "HMS Alert"]),
    Q("qb_limes", "true_false", "Limes have more vitamin C than lemons, which is why the Navy switched.", False, "Limes have about half as much. The Navy switched for price and supply, and because it wrongly equated sourness with potency.", ["wiki_limey", "wiki_scurvy"], "lost_again", "limey"),
    Q("qb_nares", "mcq", "The 1876 inquiry into the British Arctic Expedition blamed scurvy on what?", 2, "Lime juice was not carried on the sledges; it froze and was hard to use.", ["arctic_nares"], "lost_again", "nares_1875", options=["Bad tinned meat", "Too much exercise", "No lime juice on the sledges", "Cold water"]),
    Q("qb_guinea", "mcq", "Holst and Frolich were studying which disease when they found scurvy in guinea pigs?", 1, "Beriberi in Norwegian fishing crews.", ["wiki_holst"], "discovery", "holst_frolich", options=["Rickets", "Beriberi", "Pellagra", "Typhus"]),
    Q("qb_paprika", "mcq", "Where did Szent-Gyorgyi find a rich, cheap source of vitamin C?", 3, "Paprika peppers in Szeged, Hungary's paprika capital.", ["nlm_szeged"], "discovery", "szent_gyorgyi", options=["Lemons", "Adrenal glands", "Cabbage", "Paprika"]),
    Q("qb_origin", "map_pin", "Tap the region where citrus first evolved.", {"lat": 26.5, "lon": 96.5}, "The south-east foothills of the Himalayas: eastern Assam, northern Myanmar, western Yunnan.", ["nature_wu2018"], "ancestors", target={"lat": 26.5, "lon": 96.5, "tolerance_km": 700, "label": "Assam, Myanmar, Yunnan border region"}),
    Q("qb_orange_parents", "mcq", "The sweet orange is a hybrid of which two?", 1, "Pomelo and mandarin.", ["wiki_orange"], "ancestors", options=["Lemon and lime", "Pomelo and mandarin", "Citron and grapefruit", "Kumquat and lemon"]),
    Q("qb_lemon_parents", "mcq", "A true lemon is a hybrid of citron and what?", 0, "Bitter orange.", ["wiki_lemon"], "hybrids", "lemon", options=["Bitter orange", "Pomelo", "Lime", "Kumquat"]),
    Q("qb_navel", "true_false", "Every navel orange tree is grown from seed.", False, "Navels are seedless; all are propagated by cutting and grafting from the original Bahia mutant.", ["wiki_navel"], "travel", "navel_orange"),
    Q("qb_nagpur", "mcq", "Botanically, the Nagpur 'orange' is a...", 2, "A mandarin, Citrus reticulata.", ["dte_nagpur_gi"], "india", "nagpur_orange", options=["Sweet orange", "Bitter orange", "Mandarin", "Pomelo"]),
    Q("qb_kinnow", "mcq", "Where was the kinnow bred?", 0, "At the University of California Citrus Experiment Station, Riverside, by H. B. Frost around 1915.", ["ucr_kinnow"], "india", "kinnow", options=["Riverside, California", "Abohar, Punjab", "Nagpur", "Valencia, Spain"]),
    Q("qb_cold", "true_false", "Regular vitamin C cuts how often ordinary people catch colds.", False, "Cochrane 2013: risk ratio 0.97 in the general population, essentially no effect.", ["cochrane_2013"], "myths", "pauling"),
    Q("qb_myth_orange", "higher_lower", "Vitamin C per 100 g: is guava higher or lower than orange?", "higher", "Guava about 228 mg, orange about 53 mg.", ["wiki_vitc"], "myths", "c_champions", options=[{"label": "Guava", "value": 228, "unit": "mg/100 g"}, {"label": "Orange", "value": 53, "unit": "mg/100 g"}]),
    Q("qb_us_rise", "higher_lower", "US child hospital scurvy rate per 100,000 stays: was 2020 higher or lower than 2016?", "higher", "8.2 in 2016, 26.7 in 2020.", ["reikersdorfer_2024"], "scurvy_today", options=[{"label": "2016", "value": 8.2, "unit": "per 100,000"}, {"label": "2020", "value": 26.7, "unit": "per 100,000"}]),
    Q("qb_florida", "mcq", "Florida grew 244 million boxes of oranges in 1997-98. About how many in 2025-26?", 1, "12.95 million boxes, about 5% of the peak.", ["nass_1999", "nass_2026"], "now", "juice_squeeze", options=["About 150 million", "About 13 million", "About 60 million", "About 240 million"]),
    Q("qb_hlb", "mcq", "What spreads citrus greening between trees?", 2, "The Asian citrus psyllid (and in Africa, a related psyllid).", ["wiki_hlb"], "now", "greening", options=["Wind", "Bees", "A psyllid insect", "Contaminated water"]),
    Q("qb_recap_order", "order", "Put these in order, earliest first.", ["Lancaster's lemon juice", "Lind's trial", "Navy lemon ration", "Guinea pig model", "Vitamin C synthesised"], "1601, 1747, 1795, 1907, 1933.", ["wiki_lancaster", "wiki_lind", "wiki_scurvy", "wiki_holst", "wiki_vitc"], "recap", items=[{"label": "Lancaster's lemon juice", "year": 1601}, {"label": "Lind's trial", "year": 1747}, {"label": "Navy lemon ration", "year": 1795}, {"label": "Guinea pig model", "year": 1907}, {"label": "Vitamin C synthesised", "year": 1933}]),
]

PREQ = [
    Q("p1", "mcq", "Guess: which fruit has the most vitamin C per 100 g?", 2, "Guava, about 228 mg, against about 53 mg in an orange or lemon.", ["wiki_vitc"], "myths", options=["Orange", "Lemon", "Guava", "Apple"]),
    Q("p2", "true_false", "Guess: most mammals, including rats and dogs, make their own vitamin C.", True, "They do. Humans and other apes, monkeys, guinea pigs and some bats cannot.", ["wiki_gulo", "wiki_vitc"], "mechanism"),
    Q("p3", "mcq", "Guess: where did citrus fruits first evolve?", 3, "The foothills where Assam, Myanmar and Yunnan meet.", ["nature_wu2018"], "ancestors", options=["Spain", "Florida", "Persia", "North-east India, Myanmar and Yunnan"]),
    Q("p4", "mcq", "Guess: when did an English captain first show lemon juice protecting one ship against scurvy?", 0, "1601, James Lancaster, 146 years before Lind's trial.", ["wiki_lancaster"], "before_lind", options=["1601", "1747", "1795", "1907"]),
    Q("p5", "true_false", "Guess: big daily doses of vitamin C stop ordinary people catching colds.", False, "They do not. They shorten colds slightly.", ["cochrane_2013"], "myths"),
]

QUIZ = [
    Q("q01", "image_id", "Whose portrait is this, the surgeon of the 1747 trial?", 1, "James Lind, later chief physician at Haslar.", ["wiki_lind"], "lind", "lind_trial", image_id="img_lind", options=["Gilbert Blane", "James Lind", "James Cook", "John Woodall"]),
    Q("q02", "compare", "Which picture shows the fruit that kept the Royal Navy healthy from 1795?", 0, "Left: lemon. Right: West Indian lime, with about half the vitamin C.", ["wiki_scurvy", "wiki_limey"], "lost_again", "limey", image_ids=["img_lemon", "img_key_lime"], options=["Left", "Right"]),
    Q("q03", "order", "Put these in order, earliest first.", ["Cartier's cedar tea", "Woodall's Surgeon's Mate", "Lind's trial", "Rose's lime juice patent", "Szent-Gyorgyi's paprika"], "1536, 1617, 1747, 1867, 1932.", ["wiki_cartier", "wiki_woodall", "wiki_lind", "wiki_scurvy", "nlm_szeged"], "recap", items=[{"label": "Cartier's cedar tea", "year": 1536}, {"label": "Woodall's Surgeon's Mate", "year": 1617}, {"label": "Lind's trial", "year": 1747}, {"label": "Rose's lime juice patent", "year": 1867}, {"label": "Szent-Gyorgyi's paprika", "year": 1932}]),
    Q("q04", "match", "Match each person to their part in the story.", [["James Lancaster", "Lemon juice on one ship of four, 1601"], ["Gilbert Blane", "Navy lemon ration, 1795"], ["Axel Holst", "Guinea pig scurvy, 1907"], ["Norman Haworth", "First synthesis, 1933"], ["Linus Pauling", "Megadoses for colds, 1970"]], "Each matched to their best-known contribution.", ["wiki_lancaster", "wiki_blane", "wiki_holst", "wiki_haworth", "wiki_pauling"], "recap", pairs=[["James Lancaster", "Lemon juice on one ship of four, 1601"], ["Gilbert Blane", "Navy lemon ration, 1795"], ["Axel Holst", "Guinea pig scurvy, 1907"], ["Norman Haworth", "First synthesis, 1933"], ["Linus Pauling", "Megadoses for colds, 1970"]]),
    Q("q05", "true_false", "Lind's 1753 Treatise immediately persuaded the Navy to issue lemon juice.", False, "The Sick and Hurt Board rejected a fruit juice proposal in 1754; the ration came only in 1795.", ["jll_trohler"], "lind", "lind_trial", diff=2),
    Q("q06", "mcq", "What did limes lack compared with lemons?", 1, "About half the vitamin C; the juice also lost more in processing.", ["wiki_limey"], "lost_again", "limey", options=["Acid", "Vitamin C", "Sugar", "Pectin"]),
    Q("q07", "guess_clues", "Guess the fruit from the clues.", "Pomelo", "The pomelo: the largest citrus and the sweet orange's maternal ancestor.", ["wiki_pomelo", "wiki_orange"], "ancestors", "pomelo", diff=2, clues=["A natural species, not a hybrid.", "The largest citrus fruit.", "Its chloroplast DNA is in every sweet orange.", "It is also an ancestor of the grapefruit."], options=["Citron", "Pomelo", "Mandarin", "Lemon"]),
    Q("q08", "map_pin", "Tap Nokrek, India's National Citrus Gene Sanctuary.", {"lat": 25.68, "lon": 90.32}, "In the Garo Hills of Meghalaya.", ["dte_citrus_indica"], "india", "citrus_indica", diff=2, target={"lat": 25.68, "lon": 90.32, "tolerance_km": 250, "label": "Nokrek, Garo Hills"}),
    Q("q09", "image_id", "Which Indian fruit is this, richer in vitamin C than an orange?", 3, "Amla, the Indian gooseberry.", ["wiki_amla", "newsmed_amla"], "india", "amla", image_id="img_amla", options=["Kinnow", "Bael", "Jamun", "Amla"]),
    Q("q10", "odd_one_out", "Which of these is not a mandarin?", 3, "Mosambi is a sweet lime (or sweet orange). The others are mandarins.", ["wiki_mandarin", "wiki_limetta", "dte_nagpur_gi"], "india", options=["Nagpur orange", "Kinnow", "Khasi mandarin", "Mosambi"]),
    Q("q11", "higher_lower", "Vitamin C deficiency in people aged 60+ (2011 study): was north India higher or lower than south India?", "higher", "North 73.9%, south 45.7%.", ["ravindran_2011"], "india", options=[{"label": "North India", "value": 73.9, "unit": "%"}, {"label": "South India", "value": 45.7, "unit": "%"}]),
    Q("q12", "mcq", "In which city did Szent-Gyorgyi make kilograms of vitamin C from paprika?", 2, "Szeged, the paprika capital of Hungary.", ["nlm_szeged"], "discovery", "szent_gyorgyi", options=["Budapest", "Cambridge", "Szeged", "Pittsburgh"]),
    Q("q13", "true_false", "Fresh raw meat, especially liver, can prevent scurvy.", True, "Raw fresh meat and organs hold enough vitamin C; Arctic peoples and some explorers relied on it.", ["wiki_scurvy"], "lost_again", "stefansson"),
    Q("q14", "image_id", "This bumpy green fruit belongs to which citrus?", 0, "Makrut lime, Citrus hystrix, prized more for its hourglass double leaf than its fruit.", ["wiki_kaffir"], "hybrids", "kaffir_lime", image_id="img_kaffir", options=["Makrut lime", "Key lime", "Lemon", "Yuzu"]),
    Q("q15", "mcq", "Florida's first 2026-27 forecast (October 2026) put the orange crop at about...", 0, "10 million boxes, down 23% after winter freezes.", ["ffp_oct2026"], "now", "juice_squeeze", diff=2, options=["10 million boxes", "50 million boxes", "100 million boxes", "244 million boxes"]),
    Q("q16", "mcq", "Brazil's Fundecitrus forecast in May 2026 for the 2026-27 orange crop was...", 1, "255.2 million boxes, down 12.9% from 292.94 million.", ["fundecitrus_2026"], "now", "juice_squeeze", diff=2, options=["314.6 million boxes", "255.2 million boxes", "400 million boxes", "13 million boxes"]),
    Q("q17", "guess_clues", "Guess the person.", "Linus Pauling", "Pauling, Nobel laureate in chemistry (1954) and peace (1962).", ["wiki_pauling"], "myths", "pauling", clues=["Won two Nobel Prizes.", "Took 3 grams of vitamin C a day.", "Wrote 'Vitamin C and the Common Cold' in 1970.", "Claimed large doses could help late-stage cancer."], options=["Albert Szent-Gyorgyi", "Linus Pauling", "Norman Haworth", "Casimir Funk"]),
    Q("q18", "odd_one_out", "Which of these did NOT help prevent scurvy?", 2, "Elixir of vitriol (dilute sulphuric acid) did nothing. The others contain vitamin C.", ["wiki_lind", "wiki_scurvy"], "lind", options=["Sauerkraut", "Cedar needle tea", "Elixir of vitriol", "Fresh seal meat"]),
    Q("q19", "mcq", "The name of mosambi traces back to which country?", 3, "Mozambique, via the Portuguese.", ["wiki_limetta"], "india", "mosambi", options=["Portugal", "Morocco", "Malaysia", "Mozambique"]),
    Q("q20", "true_false", "Scurvy cases among US children in hospital roughly tripled between 2016 and 2020.", True, "From 8.2 to 26.7 per 100,000 stays.", ["reikersdorfer_2024"], "scurvy_today", "modern_scurvy"),
    Q("q21", "compare", "Which picture shows the seedless orange whose parent tree stands in Riverside?", 0, "Left: navel orange, with its little second fruit at the base. Right: a Seville orange tree courtyard.", ["wiki_navel"], "travel", "navel_orange", image_ids=["img_navel", "img_seville_patio"], options=["Left", "Right"]),
]

BEST_FACTS = [
    {"fact": "The plaque honouring James Lind, unveiled at Edinburgh's medical school in 1953, was paid for by the citrus growers of California and Arizona.", "why_surprising": "The orange industry funded the memorial to its best advertisement.", "score": 9, "spotlight_id": "haslar", "source_ids": ["wiki_lind"]},
    {"fact": "In 1601, 146 years before Lind's trial, James Lancaster gave one ship of four three spoonfuls of lemon juice a day; its crew had to help sail the other three, sick with scurvy, into Table Bay.", "why_surprising": "The 'first' trial had a working precedent.", "score": 9, "spotlight_id": "lancaster_1601", "source_ids": ["wiki_lancaster"]},
    {"fact": "Lind boiled fruit juice for hours to make a portable 'rob', which destroyed the vitamin C that made his oranges work.", "why_surprising": "The discoverer sabotaged his own cure.", "score": 9, "spotlight_id": "lind_rob", "source_ids": ["jll_trohler"]},
    {"fact": "The Royal Navy beat scurvy with lemons in 1795, then swapped to West Indian limes with about half the vitamin C, and scurvy came back on polar expeditions.", "why_surprising": "A solved problem was un-solved by a procurement decision.", "score": 10, "spotlight_id": "limey", "source_ids": ["wiki_scurvy", "wiki_limey"]},
    {"fact": "'Limey' comes from the lime juice ration, the version of the cure that worked worst.", "why_surprising": "The nickname honours the wrong fruit.", "score": 8, "spotlight_id": "limey", "source_ids": ["wiki_limey"]},
    {"fact": "Humans, apes and monkeys cannot make vitamin C because the GULO gene broke about 63 million years ago; its dead remains still sit on human chromosome 8.", "why_surprising": "We carry the corpse of the gene that would have saved the sailors.", "score": 9, "spotlight_id": "broken_gene", "source_ids": ["wiki_gulo"]},
    {"fact": "Guinea pigs became the scurvy test animal by accident in 1907: Norwegian doctors studying beriberi chose them over pigeons, which make their own vitamin C and could never have got scurvy.", "why_surprising": "A lucky choice of lab animal unlocked the vitamin.", "score": 8, "spotlight_id": "holst_frolich", "source_ids": ["wiki_holst", "wiki_scurvy"]},
    {"fact": "Szent-Gyorgyi tested Szeged paprika for vitamin C in autumn 1932 (in his telling, because he did not want to eat it at supper); within a week his lab had made over three pounds of the pure vitamin.", "why_surprising": "A dinner he avoided led to a Nobel Prize.", "score": 9, "spotlight_id": "szent_gyorgyi", "source_ids": ["nlm_szeged", "frontiers_szg"]},
    {"fact": "Vitamin C won two Nobel Prizes in the same year, 1937: medicine for Szent-Gyorgyi and chemistry for Haworth.", "why_surprising": "One small molecule, two prizes.", "score": 7, "spotlight_id": "haworth", "source_ids": ["nobel_szg", "nobel_haworth"]},
    {"fact": "Cook got his crew to eat sauerkraut by serving it only at the officers' table; 'the moment they see their superiors set a value upon it, it becomes the finest stuff in the world'.", "why_surprising": "Behavioural nudging, 1768.", "score": 8, "spotlight_id": "cook_kraut", "source_ids": ["hektoen_kraut"]},
    {"fact": "Every navel orange is a clone of one mutant branch from a monastery tree in Bahia, Brazil; one of the 1873 parent trees still stands in Riverside, California.", "why_surprising": "Billions of oranges, one original tree.", "score": 8, "spotlight_id": "navel_orange", "source_ids": ["wiki_navel"]},
    {"fact": "Citrus evolved in the foothills where Assam, Myanmar and Yunnan meet, and the word 'orange' may trace back to an Indian language, through Sanskrit naranga.", "why_surprising": "The 'Mediterranean' fruit and its name both come from north-east India's neighbourhood.", "score": 9, "spotlight_id": "citrus_indica", "source_ids": ["nature_wu2018", "lldf_orange"]},
    {"fact": "The kinnow that defines a Punjabi winter was bred in Riverside, California, around 1915.", "why_surprising": "A north Indian favourite is a Californian immigrant.", "score": 8, "spotlight_id": "kinnow", "source_ids": ["ucr_kinnow"]},
    {"fact": "Amla can carry 193 to 720 mg of vitamin C per 100 g, several times an orange.", "why_surprising": "India's sourest berry beats the famous citrus.", "score": 7, "spotlight_id": "amla", "source_ids": ["newsmed_amla"]},
    {"fact": "Florida grew 244 million boxes of oranges in 1997-98 and about 13 million in 2025-26, after citrus greening arrived in 2005.", "why_surprising": "A 95% collapse in the home of frozen orange juice.", "score": 8, "spotlight_id": "juice_squeeze", "source_ids": ["nass_1999", "nass_2026"]},
    {"fact": "Hospital scurvy among US children rose from 8.2 to 26.7 per 100,000 stays between 2016 and 2020.", "why_surprising": "A sailors' disease, tripling in the 21st century.", "score": 8, "spotlight_id": "modern_scurvy", "source_ids": ["reikersdorfer_2024"]},
    {"fact": "In WWII American soldiers threw away the lemon drink powder in their rations, which pushed Florida to develop frozen orange juice concentrate.", "why_surprising": "Breakfast juice was a military taste problem.", "score": 7, "spotlight_id": "frozen_oj", "source_ids": ["wiki_oj"]},
]

VERIFICATION = [
    {"claim": "Anson's death toll", "status": "range", "note": "Wikipedia's Lind article gives 1,400 dead out of 1,900; the Scurvy article gives about 1,300 of 2,000 in the first ten months; the Anson article says crews fell from 961 to 335 on the three surviving ships by June 1741. Not every death was scurvy."},
    {"claim": "Da Gama lost 116 of 170 men and Magellan 208 of 230, mainly to scurvy", "status": "range", "note": "Figures quoted from the historian Jonathan Lamb via Wikipedia. Magellan's losses include battle, desertion and execution, so 'mainly to scurvy' is loose."},
    {"claim": "Scurvy killed at least two million sailors, 1500 to 1800", "status": "unverified", "note": "A widely repeated historians' estimate; no primary count exists."},
    {"claim": "India's recommended vitamin C intake", "status": "range", "note": "Wikipedia lists 40 mg a day (older National Institute of Nutrition figure). Secondary sources report ICMR-NIN's 2020 revision to 80 mg (men) and 65 mg (women); the 2020 report itself was not checked."},
    {"claim": "Amla vitamin C content", "status": "range", "note": "A review cites 193 to 720 mg per 100 g across cultivars; Wikipedia's table gives 445 mg. Varies with cultivar, ripeness and storage."},
    {"claim": "Timing of the Australian citrus radiation", "status": "disputed", "note": "Wu et al. (2018) say early Pliocene; Wikipedia's Citrus article says early Pleistocene. The late Miocene date for the first radiation is from the paper; '6 to 8 million years' is from press summaries."},
    {"claim": "Nagpur orange GI registration year", "status": "disputed", "note": "Down To Earth reported the tag in September 2014; an ICAR table lists 2013."},
    {"claim": "Szent-Gyorgyi's paprika supper story", "status": "unverified", "note": "Told in his own autobiography and retold in several versions (supper, sandwiches); the NLM account confirms the paprika and the three pounds but not the supper."},
    {"claim": "Cook served sauerkraut at the officers' table", "status": "unverified", "note": "The quotation is from Cook's journal as cited by Hektoen International; later retellings add flogging, which is not supported here."},
    {"claim": "Mosambi identity", "status": "disputed", "note": "Wikipedia treats mosambi as Citrus limetta (sweet lime); Indian horticulture statistics often count mosambi with sweet oranges."},
    {"claim": "First HLB-resistant orange variety authorised by the USDA", "status": "unverified", "note": "Reported in passing in a July 2026 FreshFruitPortal article without naming the variety; not checked against a USDA notice."},
    {"claim": "GULO lost about 63 million years ago", "status": "range", "note": "Secondary sources give 61 to 63 million years; the split of haplorhine and strepsirrhine primates is often dated 63 to 70 million years ago. The loss is dated only indirectly."},
    {"claim": "Szent-Gyorgyi's gift to Finland, 1940", "status": "disputed", "note": "The University of Szeged exhibition says he handed over the Nobel medal on 9 March 1940; other accounts say he gave the prize money."},
    {"claim": "HMS Suffolk sailing and arrival dates", "status": "unverified", "note": "Sources agree on a 23-week non-stop voyage to India in 1794 with lemon juice; exact sailing and arrival dates vary, so the day text gives none."},
    {"claim": "Brazil 2026-27 orange forecast", "status": "range", "note": "Fundecitrus: 255.2 million boxes in May 2026, revised to 263.15 million on 10 September 2026; further updates due December 2026 to April 2027."},
    {"claim": "Horsemeat and scurvy at Kut", "status": "unverified", "note": "The link comes from a British inquiry's observation that Indians who ate horseflesh were less affected; it is not a controlled comparison."},
    {"claim": "Citrus indica image", "status": "unverified", "note": "The Commons image is a pressed herbarium sheet (Rijksherbarium, Leiden) labelled 'Plants of Assam, India' and 'Citrus cf. indica': the collector's identification is tentative (cf.), and no photo of a wild Nokrek tree was found."},
    {"claim": "Brisbane inquest spotlight", "status": "no_image", "note": "No appropriate open-licence image; a photo of the child or family would not be appropriate. These were non-inquest findings: no inquest was held.", "spotlight_id": "brisbane_inquest"},
]

SIDE_DISH = {
    "area": "Statistics",
    "title": "Why Lind's twelve sailors still matter: the control group",
    "body_md": "Give a sick sailor oranges and he recovers. Did the oranges work? Maybe he would have recovered anyway. One success proves almost nothing.\n\nLind's trick in 1747 was to make the comparison do the work. He chose twelve men with similar scurvy, gave them the same diet, the same quarters and the same time, and changed only one thing per pair. If everything else is equal and one pair gets better, the difference is probably the treatment. That is a **controlled comparison**, and the group that does not get the treatment you care about is the **control group**.\n\nModern trials add three more ideas Lind did not have. **Randomisation**: let chance, not the doctor, decide who gets what, so the doctor cannot unconsciously give the fruit to the strongest men. **Blinding**: where possible, neither patient nor assessor knows who got what. **Size**: two people per treatment can mislead; hundreds or thousands give stable answers. The 2013 Cochrane review of vitamin C and colds pooled 29 comparisons and 11,306 people, which is why its answer is more trustworthy than any single study.\n\nThe lesson of the scurvy story is also humbling. Lind's comparison was right, and his theory was wrong; the Navy trusted theory. When an experiment and an explanation disagree, back the experiment.",
    "image_ids": ["img_treatise", "img_lind"],
    "card_ids": ["c49", "c50"],
    "source_ids": ["wiki_lind", "jll_trohler", "cochrane_2013"],
}

OFFLINE = {
    "kind": "try",
    "title": "Watch heat destroy vitamin C, like Lind's rob",
    "body_md": "**Twenty minutes, kitchen materials. Do not drink any of the test liquids.**\n\n**You need**\n- 1 teaspoon cornflour (or rice starch) and a cup of water\n- Tincture of iodine or povidone-iodine antiseptic (the brown liquid in a first-aid kit)\n- 2 lemons or 3 nimbu, a small pan, a dropper or teaspoon, 3 clear glasses\n\n**Steps**\n1. Boil the cornflour in the water for a minute and let it cool. This is your starch indicator.\n2. Put 3 tablespoons of water and 1 teaspoon of starch solution in each glass. Add iodine a drop at a time until each turns the same deep blue-black.\n3. Squeeze the lemons. Keep half the juice fresh. Boil the other half for 10 minutes, the way Lind made his rob, then cool it.\n4. Add fresh juice to glass 1, one drop at a time, swirling, and count the drops until the blue disappears. Vitamin C turns iodine colourless.\n5. Do the same with the boiled juice in glass 2. Use glass 3 to test bottled lemon juice or juice left out overnight.\n\n**What to notice**: the fewer drops it takes to clear the blue, the more vitamin C the juice holds. Boiled and old juice usually need many more drops. You have just repeated, in miniature, the mistake that cost the Navy decades.\n\nWatch the BASF Science Club demonstration first if you want to see the colour change.",
    "spotlight_id": "lind_rob",
    "media_ids": ["vid_vitc_test"],
    "source_ids": ["jll_trohler", "wiki_vitc"],
}
