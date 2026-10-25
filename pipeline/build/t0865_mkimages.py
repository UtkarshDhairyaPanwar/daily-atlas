#!/usr/bin/env python3
"""Assemble t0865_images.json from records returned by pipeline/tools/commons.py (search / verify).
Usage: python3 t0865_mkimages.py <dir with verres.json, imgres.json, imgres4.json>"""
import json, os, sys

SRC = sys.argv[1]
recs = {}
for fn in ["verres.json", "imgres.json", "imgres4.json"]:
    p = os.path.join(SRC, fn)
    if not os.path.exists(p):
        continue
    d = json.load(open(p))
    items = d.values() if fn == "verres.json" else [r for rs in d.values() for r in rs]
    for r in items:
        if r.get("title") and not r.get("error"):
            recs[r["title"]] = r

# id: (Commons file title, alt, caption)
M = {
    "img_anson": ("File:1stLordAnson.jpg", "Portrait of George Anson in naval dress", "George Anson, whose 1740 to 1744 voyage lost about 1,400 men, mostly to scurvy."),
    "img_covadonga": (None, "Painting of two sailing ships exchanging cannon fire in clouds of smoke", "The Centurion captures the treasure galleon Nuestra Senora de Covadonga, 20 June 1743."),
    "img_gums": ("File:Scorbutic gums.jpg", "Close-up of swollen, discoloured gums around the lower teeth", "Scorbutic gums: swollen and bleeding, a classic sign of vitamin C deficiency."),
    "img_gums_wellcome": ("File:Scurvy, the gums. Wellcome M0002835.jpg", "Medical illustration of a mouth with diseased, swollen gums", "Scurvy's effect on the gums, a historical medical illustration (Wellcome Collection)."),
    "img_ascorbic": ("File:L-Ascorbic acid.svg", "Chemical structure diagram of L-ascorbic acid, a five-membered ring with side chain", "L-ascorbic acid, vitamin C: a small sugar acid most animals make from glucose."),
    "img_peppers": ("File:Green-Yellow-Red-Pepper-2009.jpg", "Green, yellow and red bell peppers side by side", "Capsicum peppers: red ones hold more vitamin C per gram than oranges."),
    "img_szeged_paprika": ("File:Szeged-paprika1.jpg", "Large display of dried red Szeged paprika peppers", "Szeged paprika, the source Szent-Gyorgyi used to make vitamin C by the kilogram."),
    "img_guinea_pig": ("File:George the amazing guinea pig.jpg", "A brown and white guinea pig", "Guinea pigs, like humans, cannot make vitamin C, which made them the first scurvy test animal (1907)."),
    "img_gama": (None, "Painted portrait of a bearded man in dark clothes", "Vasco da Gama, attributed to Gregorio Lopes, c. 1524."),
    "img_cartier": ("File:Jacques Cartier 1851-1852.jpg", "Painting of a bearded explorer in 16th-century dress looking into the distance", "Jacques Cartier, as imagined by Theophile Hamel in the 1840s; no true likeness survives."),
    "img_thuja": ("File:Thuja occidentalis.jpg", "Flat sprays of scale-like evergreen foliage with small yellow-green cones", "Eastern white cedar, Thuja occidentalis: probably Cartier's annedda."),
    "img_lancaster": ("File:Jameslancaster.jpg", "Portrait of an Elizabethan man with beard and ruff", "Sir James Lancaster, commander of the East India Company's first fleet (1601)."),
    "img_woodall": ("File:John Woodall by George Glover detail.jpg", "Engraved portrait of a bearded older man", "John Woodall, first Surgeon General of the East India Company (engraving, 1639)."),
    "img_woodall_scurvy": (None, "Printed page 160 headed 'Of the Scurvy called in Latine Scorbutum', with a decorated initial letter", "The opening page of Woodall's text on scurvy in The Surgeon's Mate, 1639 edition."),
    "img_farfan": ("File:Augustin Farfan. Reproduction of woodcut, 1914. Wellcome V0001865.jpg", "Woodcut portrait of a friar in a habit", "Fray Agustin Farfan, who recommended oranges and lemons for scurvy in 1579."),
    "img_lind": ("File:Portrait of James Lind, 1716-1794, Physician at Haslar Wellcome M0003113.jpg", "Engraved portrait of an 18th-century man in a wig", "James Lind (1716 to 1794), naval surgeon and physician at Haslar."),
    "img_treatise": ("File:J. Lind; A treatise of the scurvy. Wellcome L0019183.jpg", "Title page of an 18th-century book, A Treatise of the Scurvy", "Title page of Lind's A Treatise of the Scurvy (1753)."),
    "img_treatise_1757": ("File:James Lind, A Treatise on the Scurvy, 1757 Wellcome M0013130.jpg", "Title page of the 1757 edition of Lind's treatise", "The 1757 second edition of Lind's treatise."),
    "img_haslar": ("File:Royal Haslar Hospital, 2026 04.jpg", "Long brick hospital building beside a lawn", "The Royal Haslar Hospital at Gosport, where Lind was chief physician from 1758 (photographed 2026)."),
    "img_cook": ("File:Captainjamescookportrait.jpg", "Portrait of Captain James Cook in naval uniform holding a chart", "Captain James Cook, official portrait by Nathaniel Dance."),
    "img_sauerkraut": ("File:Kiszona kapusta.JPG", "Bowl of pale shredded fermented cabbage", "Sauerkraut: Cook's Endeavour carried 7,860 pounds of it."),
    "img_blane": ("File:Sir Gilbert Blane by Martin Archer Shee.jpg", "Portrait of a Georgian gentleman in a dark coat", "Sir Gilbert Blane, who pushed the 1795 lemon juice ration."),
    "img_malaspina": ("File:Alejandro Malaspina.jpg", "Portrait of an 18th-century naval officer", "Alessandro (Alejandro) Malaspina, whose 1789 to 1794 expedition had almost no scurvy."),
    "img_scurvygrass": ("File:Cochlearia officinalis Prague 2012 1.jpg", "Low plant with small white four-petalled flowers", "Common scurvygrass, Cochlearia officinalis."),
    "img_key_lime": ("File:Citrus × aurantiifolia (Christm.) Swingle (51906868474).jpg", "Small round green limes on a branch", "Key or West Indian lime, Citrus x aurantiifolia."),
    "img_persian_lime": ("File:Starr-140117-3997-Citrus latifolia-Tahitian fruit and leaves-Hawea Pl Olinda-Maui (24612312943).jpg", "Larger oval green limes among leaves", "Persian or Tahiti lime, Citrus x latifolia."),
    "img_roses": ("File:Rose's Lime Juice.JPG", "Bottle of Rose's Lime Juice cordial", "Rose's lime juice, patented 1867, the year lime juice became law on British merchant ships."),
    "img_alert": ("File:HMS Alert.jpg", "Three-masted ship held in Arctic pack ice", "HMS Alert in the pack ice, British Arctic Expedition, 1876."),
    "img_belgica": ("File:Belgica1web.jpg", "Small sailing ship anchored below snowy mountains", "The Belgica, whose Antarctic crew suffered scurvy in 1897 to 1899."),
    "img_evans": ("File:Commander Evans 5126121136 99388b2868 o.jpg", "Photograph of a naval officer in uniform and cap", "Edward Evans, nearly killed by scurvy on the Ross Ice Shelf in 1912."),
    "img_scott": ("File:Scott of the Antarctic (bw) (cropped).jpg", "Black and white portrait of Robert Falcon Scott in full naval dress", "Robert Falcon Scott, leader of the Terra Nova expedition."),
    "img_stefansson": ("File:Vilhjalmur Stefansson.jpg", "Portrait photograph of a man in a suit", "Vilhjalmur Stefansson, who ate only meat for a year in 1928."),
    "img_holst": ("File:Axel Holst 02.jpg", "Portrait photograph of a bearded Norwegian man", "Axel Holst (1860 to 1931)."),
    "img_frolich": ("File:Theodor Frolich 01.jpg", "Portrait photograph of a man with a moustache", "Theodor Frolich, Holst's partner in the 1907 guinea pig experiments."),
    "img_szg": ("File:Szent-Györgyi Albert, Nobel-díjas és Kossuth-díjas orvos, biokémikus. Fortepan 74535.jpg", "Black and white photograph of an older scientist", "Albert Szent-Gyorgyi, Nobel Prize in Physiology or Medicine 1937."),
    "img_haworth": ("File:Norman Haworth.jpg", "Portrait photograph of a man in a suit", "Norman Haworth, who synthesised vitamin C in 1933."),
    "img_reichstein": ("File:Thadeus Reichstein ETH-Bib Portr 10137.jpg", "Portrait photograph of a man with glasses", "Tadeus Reichstein, whose 1933 process made vitamin C cheap."),
    "img_pauling": ("File:Linus Pauling in the 1940s.jpg", "Black and white portrait of a smiling man in a suit", "Linus Pauling in the 1940s, long before his vitamin C campaign."),
    "img_citron": ("File:Chinesische Zedrat Zitrone.jpg", "Large lumpy yellow citron fruits on display", "Citron, Citrus medica: thick rind, little juice, the oldest cultivated citrus."),
    "img_pomelo": ("File:Pomelo fruit.jpg", "A large pale pomelo cut to show thick rind and segments", "Pomelo, Citrus maxima, the largest citrus."),
    "img_mandarin": ("File:Citrus reticulata April 2013 Nordbaden.JPG", "Small orange mandarins on a potted tree", "Mandarin, Citrus reticulata, one of the three founding species."),
    "img_orange": ("File:Oranges - whole-halved-segment.jpg", "Whole orange, halved orange and a segment", "Sweet orange, Citrus x sinensis: a pomelo and mandarin hybrid."),
    "img_orange_blossom": ("File:OrangeBloss wb.jpg", "White orange blossoms beside ripe oranges", "Orange blossom and fruit on the same tree."),
    "img_lemon": ("File:P1030323.JPG", "A lemon on the branch beside white flowers", "Lemon, Citrus x limon: a citron and bitter orange hybrid."),
    "img_grapefruit": ("File:Grapefruits - whole-halved-segments.jpg", "Whole and halved red grapefruit with a peeled segment", "Grapefruit, a sweet orange and pomelo backcross."),
    "img_buddha": ("File:Buddhas hand 1.jpg", "Yellow citron split into long finger-like segments", "Buddha's hand, a fingered citron with no juice."),
    "img_kaffir": ("File:Citrus hystrix fruit.jpg", "Bumpy green makrut lime fruits with double leaves", "Makrut lime, Citrus hystrix."),
    "img_finger_lime": ("File:Finger lime with juice vesicles and seeds partially extracted.jpg", "Slender finger limes, one opened to show bead-like juice vesicles", "Australian finger lime: juice vesicles like caviar."),
    "img_etrog": ("File:Etrog5812.jpg", "A yellow citron with a small knob at the tip", "An etrog with its pitam, the knob prized for Sukkot."),
    "img_navel": ("File:Navel orange.jpg", "An orange showing the navel-like second fruit at its base", "A navel orange: seedless, so every tree is grafted."),
    "img_parent_navel": ("File:Parent Washington Navel Orange Tree.JPG", "An orange tree behind a plaque and low fence", "The parent Washington navel orange tree, Riverside, California, a state historical landmark."),
    "img_cec": ("File:Citrus Experiment Station.JPG", "Old stone building of a research station", "Original building of the UC Citrus Experiment Station, Riverside, where the kinnow was bred."),
    "img_seville_patio": ("File:Orange trees courtyard cathedral from Giralda Seville Spain.jpg", "Courtyard planted with rows of orange trees seen from above", "Patio de los Naranjos, Seville Cathedral: a former mosque courtyard of bitter orange trees."),
    "img_oj": ("File:Orangejuice.jpg", "A glass of fresh orange juice", "Orange juice, the 20th century's favourite vitamin C."),
    "img_florida": ("File:Florida orange grove.JPG", "A sandy track between two rows of orange trees", "A Valencia orange grove at Sebring, Florida."),
    "img_citrus_indica": ("File:Citrus indica Tanaka.jpg", "Pressed herbarium specimen: a thorny citrus twig with leaves, with labels reading Plants of Assam, India and Citrus cf. indica", "A herbarium sheet from Assam labelled Citrus cf. indica, the Indian wild orange (Rijksherbarium, Leiden)."),
    "img_citrus_map": (None, "Map of South and South-East Asia with coloured wild ranges of citrus species", "Inferred wild ranges of citrus species, after Fuller et al. (2017): note Citrus indica in north-east India."),
    "img_nagpur": ("File:Nagpur orange article.JPG", "Pile of orange and green-patched mandarins", "Nagpur oranges, botanically mandarins."),
    "img_kinnow": ("File:Harvest Kinnow.jpg", "A single smooth orange kinnow hanging from a stem with one leaf", "A kinnow mandarin (photographed in Pakistan, where it is the most planted mandarin)."),
    "img_mosambi": ("File:(Citrus limetta) Mosambi at a market in Seethammadhara.jpg", "Pale green-yellow sweet limes at a market", "Mosambi at a market in Seethammadhara, Visakhapatnam."),
    "img_amla": ("File:Phyllanthus officinalis.jpg", "Round pale green amla fruits among feathery leaves", "Amla (Indian gooseberry) on the tree."),
    "img_kut": ("File:Townshend, Khalil Pasha after Fall of Kut B.jpg", "Black and white photograph of British and Ottoman officers, some seated, some standing", "General Townshend with the Ottoman commander after the fall of Kut, April 1916."),
    "img_guava": ("File:Guava pink fruit.jpg", "Guava cut open to show pink flesh", "Guava: about 228 mg of vitamin C per 100 g."),
    "img_acerola": ("File:Malpighia glabra blossom and unripe fruits.jpg", "Pink blossoms and green unripe acerola cherries", "Acerola, one of the richest fruit sources of vitamin C."),
    "img_kakadu": ("File:Terminalia ferdinandiana fruit.jpg", "Small green Kakadu plums on a branch", "Kakadu plum, Terminalia ferdinandiana, near Broome, Australia."),
    "img_psyllid": ("File:Asian Citrus Psyllid adult.jpg", "A tiny mottled brown insect on a young leaf", "Adult Asian citrus psyllid, 2 to 3 mm long, the carrier of citrus greening."),
    "img_arnolfini": ("File:Eyck, Jan van - Arnolfini Portrait - NG.jpg", "Van Eyck's painting of a couple in a room, with oranges on the window sill and chest", "The Arnolfini Portrait: the oranges by the window are among the first in Western art."),
}
PREFIX = {
    "img_covadonga": "File:The Capture of the 'Nuestra Señora de Cavadonga'",
    "img_gama": "File:Gregório Lopes - Vasco da Gama",
    "img_woodall_scurvy": "File:John Woodall, 1639; text on scurvy",
    "img_citrus_map": "File:Map of inferred original wild ranges of the main Citrus cultivars, and selected relevant wild taxa (Fuller et al., 2017).png",
}
out, missing = [], []
for iid, (title, alt, cap) in M.items():
    r = recs.get(title) if title else None
    if r is None and iid in PREFIX:
        cands = [t for t in recs if t.startswith(PREFIX[iid]) and not t.endswith("-ar.png")]
        r = recs[cands[0]] if cands else None
    if r is None:
        missing.append(iid)
        continue
    out.append({"id": iid, "url": r["url"], "thumb_url": r["thumb_url"], "width": r["width"], "height": r["height"],
                "author": r["author"].replace(" \u2014 ", ", ").replace("\u2014", ", ").replace("\u2013", "-"), "license": r["license"], "license_url": r.get("license_url", ""),
                "file_page": r["file_page"], "alt": alt, "caption": cap, "attribution": r["attribution"].replace(" \u2014 ", ", ").replace("\u2014", ", ").replace("\u2013", "-"),
                "verified_on": r.get("verified_on", "2026-10-25")})
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "t0865_images.json"), "w"), ensure_ascii=False, indent=1)
print(len(out), "images; missing:", missing)
