# Content for day 803. Imported by t0803.py.
from t0803_sections_a import SECTIONS_A
from t0803_sections_b import SECTIONS_B
from t0803_recall import BEST_FACTS, CARDS, QUIZ, QUIZ_BANK, PREQ

def S(id, title, url, publisher):
    return {"id": id, "title": title, "url": url, "publisher": publisher}

SOURCES = [
    S("wiki_weimar", "Hyperinflation in the Weimar Republic", "https://en.wikipedia.org/wiki/Hyperinflation_in_the_Weimar_Republic", "Wikipedia"),
    S("wiki_hyper", "Hyperinflation", "https://en.wikipedia.org/wiki/Hyperinflation", "Wikipedia"),
    S("wiki_zim_hyper", "Hyperinflation in Zimbabwe", "https://en.wikipedia.org/wiki/Hyperinflation_in_Zimbabwe", "Wikipedia"),
    S("wiki_ven_hyper", "Hyperinflation in Venezuela", "https://en.wikipedia.org/wiki/Hyperinflation_in_Venezuela", "Wikipedia"),
    S("wiki_bolivar", "Venezuelan bolivar", "https://en.wikipedia.org/wiki/Venezuelan_bol%C3%ADvar", "Wikipedia"),
    S("wiki_zig", "Zimbabwe Gold", "https://en.wikipedia.org/wiki/Zimbabwe_Gold", "Wikipedia"),
    S("wiki_100tn", "Zimbabwean one hundred trillion dollar note", "https://en.wikipedia.org/wiki/Zimbabwean_one_hundred_trillion_dollar_note", "Wikipedia"),
    S("wiki_gono", "Gideon Gono", "https://en.wikipedia.org/wiki/Gideon_Gono", "Wikipedia"),
    S("wiki_rentenmark", "Rentenmark", "https://en.wikipedia.org/wiki/Rentenmark", "Wikipedia"),
    S("wiki_schacht", "Hjalmar Schacht", "https://en.wikipedia.org/wiki/Hjalmar_Schacht", "Wikipedia"),
    S("wiki_ruhr", "Occupation of the Ruhr", "https://en.wikipedia.org/wiki/Occupation_of_the_Ruhr", "Wikipedia"),
    S("wiki_assignat", "Assignat", "https://en.wikipedia.org/wiki/Assignat", "Wikipedia"),
    S("wiki_continental", "Continental currency", "https://en.wikipedia.org/wiki/Continental_currency", "Wikipedia"),
    S("wiki_dinar", "Yugoslav dinar", "https://en.wikipedia.org/wiki/Yugoslav_dinar", "Wikipedia"),
    S("wiki_qtm", "Quantity theory of money", "https://en.wikipedia.org/wiki/Quantity_theory_of_money", "Wikipedia"),
    S("wiki_petro", "Petro (token)", "https://en.wikipedia.org/wiki/Petro_(token)", "Wikipedia"),
    S("wiki_ven_refugee", "Venezuelan refugee crisis", "https://en.wikipedia.org/wiki/Venezuelan_refugee_crisis", "Wikipedia"),
    S("wiki_1991", "1991 Indian economic crisis", "https://en.wikipedia.org/wiki/1991_Indian_economic_crisis", "Wikipedia"),
    S("wiki_demon", "2016 Indian banknote demonetisation", "https://en.wikipedia.org/wiki/2016_Indian_banknote_demonetisation", "Wikipedia"),
    S("wiki_bengal", "Bengal famine of 1943", "https://en.wikipedia.org/wiki/Bengal_famine_of_1943", "Wikipedia"),
    S("wiki_trillion_campaign", "The Trillion Dollar Campaign", "https://en.wikipedia.org/wiki/The_Trillion_Dollar_Campaign", "Wikipedia"),
    S("dhm_inflation", "Die Inflation 1923 (LeMO)", "https://www.dhm.de/lemo/kapitel/weimarer-republik/innenpolitik/inflation-1923.html", "Deutsches Historisches Museum"),
    S("hm_frankfurt", "Inflation 1923. Krieg, Geld, Trauma (exhibition booklet)", "https://historisches-museum-frankfurt.de/files/PDF/2023-Inflation-1923-Krieg-Geld-Trauma.pdf", "Historisches Museum Frankfurt"),
    S("cato_hanke_krus", "World Hyperinflations (Hanke and Krus working paper and table)", "https://www.cato.org/working-paper/world-hyperinflations", "Cato Institute"),
    S("nber_sargent", "The Ends of Four Big Inflations (Thomas J. Sargent, 1982)", "https://www.nber.org/chapters/c11452", "National Bureau of Economic Research"),
    S("nber_austerity", "Austerity and the Rise of the Nazi Party (Galofre-Vila, Meissner, McKee, Stuckler)", "https://www.nber.org/system/files/working_papers/w24106/revisions/w24106.rev2.pdf", "National Bureau of Economic Research"),
    S("voxeu_austerity", "Fiscal austerity and the rise of the Nazis", "https://cepr.org/voxeu/columns/fiscal-austerity-and-rise-nazis", "CEPR VoxEU"),
    S("gutenberg_keynes", "The Economic Consequences of the Peace (J. M. Keynes, 1919)", "https://www.gutenberg.org/ebooks/15776", "Project Gutenberg"),
    S("vam_bayer", "Emergency banknote for the Thuringische Staatsbank, 1923, designed by Herbert Bayer", "https://collections.vam.ac.uk/item/O1035784", "Victoria and Albert Museum"),
    S("mdd_bayer", "Emergency Money (Herbert Bayer's Notgeld)", "https://museumderdinge.org/?p=4226", "Museum der Dinge, Berlin"),
    S("aljazeera_zig", "Zimbabwe's gold-backed currency loses half its value: Why and what's next?", "https://www.aljazeera.com/news/2024/10/24/zimbabwes-gold-backed-currency-loses-half-its-value-why-and-whats-next", "Al Jazeera"),
    S("allafrica_zim_jan26", "Zimbabwe Hits Single-Digit Inflation Milestone (27 January 2026)", "https://allafrica.com/stories/202601270279.html", "263Chat via AllAfrica"),
    S("allafrica_zim_jul26", "ZWG Annual Inflation Rate Drops to 3,2 Percent in July (2026)", "https://allafrica.com/stories/202607280059.html", "The Herald via AllAfrica"),
    S("daba_zig2030", "Zimbabwe ZiG currency targets 2030", "https://www.dabafinance.com/en/news/zimbabwe-zig-currency-targets-2030", "Daba Finance"),
    S("bs_rupee_zim", "Zimbabwe allows trade in rupee, yen and Australian dollar (2014)", "https://www.business-standard.com/article/pti-stories/zimbabwe-allows-trade-in-rupee-yen-and-australian-dollar-114012901286_1.html", "Business Standard (AFP/PTI)"),
    S("nehanda_rupee", "Indian Rupee to be legal tender in Zimbabwe (2014)", "https://nehandaradio.com/2014/01/30/indian-rupee-to-be-legal-tender-in-zimbabwe/", "Nehanda Radio"),
    S("mg_tobacco", "Zimbabwe's tobacco sector fizzles out (2008)", "https://mg.co.za/article/2008-07-02-zimbabwes-tobacco-sector-fizzles-out", "Mail & Guardian"),
    S("mg_cholera", "UN: Cholera kills nearly 400 in Zimbabwe (2008)", "https://mg.co.za/article/2008-11-28-un-cholera-kills-nearly-400-in-zimbabwe/", "Mail & Guardian"),
    S("irin_gono", "Zimbabwe: cash shortages and new bearer cheques (2008)", "https://www.thenewhumanitarian.org/node/239842", "IRIN / The New Humanitarian"),
    S("improbable_ig", "Ig Nobel Prize winners (2009 Mathematics: Gideon Gono)", "https://improbable.com/ig/winners/", "Improbable Research"),
    S("creative_review", "The Zimbabwean's Trillion Dollar Campaign", "https://www.creativereview.co.uk/the-zimbabweans-trillion-dollar-campaign/", "Creative Review"),
    S("mru_zim", "Zimbabwe and Hyperinflation: Who Wants to Be a Trillionaire?", "https://www.youtube.com/watch?v=78-BlZXm7wA", "Marginal Revolution University"),
    S("npr_ven_2026", "Dollars trickle into Venezuela's economy after first sales of country's oil by U.S. (23 January 2026)", "https://www.wshu.org/2026-01-23/dollars-trickle-into-venezuelas-economy-after-first-sales-of-countrys-oil-by-u-s", "NPR via WSHU"),
    S("enca_ven_475", "Venezuela inflation hit 475% in 2025, the world's highest level (7 March 2026)", "https://www.enca.com/business/venezuela-inflation-hit-475-2025-worlds-highest-level", "eNCA (AFP)"),
    S("eldiario_may26", "Venezuela reporto en mayo la inflacion mas baja en 19 meses (6 June 2026)", "https://eldiario.com/2026/06/06/inflacion-venezuela-mayo-2026/", "El Diario"),
    S("ntn24_sep26", "Dolar a 827,73 bolivares a tasa BCV (September 2026)", "https://www.ntn24.com/noticias-economia/mientras-el-dolar-se-situa-en-827-73-bolivares-a-tasa-bcv-delcy-rodriguez-afirma-que-venezuela-lidera-el-crecimiento-economico-en-america-latina-649350", "NTN24"),
    S("nbc_chicken", "See how many bills it took to buy a chicken in Venezuela (2018)", "https://www.nbcnews.com/slideshow/see-how-many-bills-it-took-buy-chicken-venezuela-n902491", "NBC News (Reuters photo)"),
    S("arkansas_bags", "Venezuela's bolivar used for handbags (2018)", "https://www.arkansasonline.com/news/2018/jun/25/venezuelas-bolivar-used-handbags/", "Arkansas Democrat-Gazette"),
    S("csm_bills", "As inflation devastates Venezuela, artists make purses and paintings out of bills (2018)", "https://www.csmonitor.com/World/Americas/2018/0510/As-inflation-devastates-Venezuela-artists-make-purses-and-paintings-out-of-bills", "Christian Science Monitor"),
    S("atalayar_2021", "Venezuela eliminates 6 more zeros from its currency (2021)", "https://atalayar.com/en/content/venezuela-eliminates-6-more-zeros-its-currency-save-bolivar", "Atalayar"),
    S("rpp_maduro", "Maduro dice que dolarizacion de facto es valvula de escape (2019)", "https://rpp.pe/mundo/actualidad/venezuela-nicolas-maduro-dice-que-dolarizacion-de-facto-es-valvula-de-escape-para-la-economia-noticia-1230336", "RPP Noticias (Reuters/EFE)"),
    S("cc_encovi", "ENCOVI 2017: A Staggering Hunger Crisis, in Cold, Hard Numbers", "https://caracaschronicles.com/2018/02/21/encovi-2017", "Caracas Chronicles"),
    S("bbg_oil_1945", "Venezuela's oil production plunges to lowest level since 1945 (2020)", "https://www.bloombergquint.com/markets/venezuela-s-oil-production-plunges-to-lowest-level-since-1945", "Bloomberg"),
    S("cointelegraph_petro", "Venezuela Petro coin shut down Jan. 15 after six years", "https://cointelegraph.com/news/venezuela-petro-coin-shut-down-jan-15-after-six-years-report", "Cointelegraph"),
    S("r4v_rmrp", "Venezuela Regional Refugee and Migrant Response Plan", "https://humanitarianaction.info/plan/1525/article/venezuela-rmrp-3", "R4V / OCHA Humanitarian Action"),
    S("baherald_arg", "Argentina's inflation in 2025 fell to 31.5%, the lowest in 8 years", "https://buenosairesherald.com/economics/argentinas-inflation-in-2025-fell-to-31-5-the-lowest-in-8-years", "Buenos Aires Herald"),
    S("iranintl_rial", "Iran's rial falls to record low as dollar nears 1.92 million (17 July 2026)", "https://www.iranintl.com/en/202607174145", "Iran International"),
    S("te_india", "India inflation falls to record low (October 2025)", "https://tradingeconomics.com/india/inflation-cpi/news/501327", "Trading Economics"),
    S("outlook_target", "RBI to maintain 4 per cent inflation target until 2031: Centre (March 2026)", "https://www.outlookmoney.com/banking/rbi-to-maintain-4-per-cent-inflation-target-until-2031-centre", "Outlook Money"),
    S("banglapedia_famine", "Famine, 1943", "https://en.banglapedia.org/index.php/Famine,_1943", "Banglapedia"),
    S("vam_trillion", "Trillion Dollar Campaign poster printed on a Zimbabwean banknote", "https://collections.vam.ac.uk/item/O1274867", "Victoria and Albert Museum"),
    S("hmf_trailer", "Inflation 1923. Krieg, Geld, Trauma (exhibition trailer)", "https://www.youtube.com/watch?v=uJHNFDC8VvI", "Historisches Museum Frankfurt"),
]

SOURCES += [
    S("wiki_money_illusion", "Money illusion", "https://en.wikipedia.org/wiki/Money_illusion", "Wikipedia"),
    S("wiki_fisher", "Irving Fisher", "https://en.wikipedia.org/wiki/Irving_Fisher", "Wikipedia"),
]

SECTIONS = SECTIONS_A + SECTIONS_B

HERO = {"image_id": "img_wallpaper", "kicker": "Day 803 · Money",
        "headline": "How money dies: Weimar 1923, Zimbabwe 2008, Venezuela 2018, and what each one teaches"}

STATS = [
    {"key": "cagan", "label": "Hyperinflation threshold", "value": 50, "unit": "% a month", "year": "1956", "source_ids": ["wiki_hyper"]},
    {"key": "episodes", "label": "Hyperinflations on record", "value": 57, "unit": "episodes", "year": "2016", "source_ids": ["cato_hanke_krus"]},
    {"key": "weimar_rate", "label": "Marks per US dollar, Nov 1923", "value": 4210500000000, "unit": "marks", "year": "1923", "source_ids": ["wiki_weimar"]},
    {"key": "zim_doubling", "label": "Zimbabwe price doubling time at peak", "value": 24.7, "unit": "hours", "year": "2008", "source_ids": ["wiki_hyper"]},
    {"key": "ven_2018", "label": "Venezuela inflation 2018 (BCV)", "value": 130060, "unit": "%", "year": "2018", "source_ids": ["wiki_ven_hyper"]},
    {"key": "ven_2025", "label": "Venezuela inflation 2025 (BCV)", "value": 475, "unit": "%", "year": "2025", "source_ids": ["enca_ven_475"]},
    {"key": "zim_2026", "label": "Zimbabwe ZiG inflation, Jan 2026", "value": 4.1, "unit": "%", "year": "2026", "source_ids": ["allafrica_zim_jan26"]},
]

MEDIA = [
    {"id": "vid_mru_zim", "kind": "video", "provider": "youtube", "url": "https://www.youtube.com/watch?v=78-BlZXm7wA",
     "embed_url": "https://www.youtube-nocookie.com/embed/78-BlZXm7wA?start=0&end=90", "start": 0, "end": 90,
     "title": "Zimbabwe and Hyperinflation: Who Wants to Be a Trillionaire?", "publisher": "Marginal Revolution University",
     "license": "Standard YouTube licence. Embed only, do not download.", "duration_s": 260, "verified_on": "2026-10-25",
     "verified_by": "youtube oembed returned 200 with this channel name"},
    {"id": "vid_hmf_1923", "kind": "video", "provider": "youtube", "url": "https://www.youtube.com/watch?v=uJHNFDC8VvI",
     "embed_url": "https://www.youtube-nocookie.com/embed/uJHNFDC8VvI?start=0&end=60", "start": 0, "end": 60,
     "title": "Inflation 1923. Krieg, Geld, Trauma (exhibition trailer, German)", "publisher": "Historisches Museum Frankfurt",
     "license": "Standard YouTube licence. Embed only, do not download.", "duration_s": None, "verified_on": "2026-10-25",
     "verified_by": "youtube oembed returned 200 with this channel name"},
]

VERIFICATION = [
    {"claim": "Germany's peak monthly inflation (October 1923)", "status": "range",
     "note": "The Hanke-Krus table gives about 29,500% for October 1923 (doubling about 3.7 days, wholesale prices). Wikipedia's Hyperinflation article quotes 3.25 million percent per month in 1923 (doubling about every two days) on a different series. The day uses the Hanke-Krus figure and shows the range in the comparison table."},
    {"claim": "Venezuela's 2018 inflation", "status": "range",
     "note": "Central bank: 130,060%. IMF: about 929,790%. Opposition-led National Assembly: about 1.7 million percent. Peak monthly rate given as roughly 150% to 234% depending on source and month (the higher figure from the National Assembly and Hanke). Doubling time of about 415 hours is computed from 234% a month."},
    {"claim": "Number of printing firms and presses in autumn 1923", "status": "range",
     "note": "The DHM gives 133 firms with 1,783 presses; a museum catalogue elsewhere gives 1,723 machines in 133 print shops."},
    {"claim": "Zimbabwe tobacco output 2000 and 2008", "status": "range",
     "note": "2000 record given as 237 million kg (TIMB) or about 267 million kg (Zimbabwe Tobacco Association); 2008 as 48 to 49 million kg."},
    {"claim": "Number of large commercial farms before land reform (about 4,000)", "status": "range",
     "note": "Commonly cited as 4,000 to 4,500 mostly white-owned commercial farms; not checked against a primary census."},
    {"claim": "Bond notes backed by a 200 million dollar Afreximbank facility", "status": "unverified",
     "note": "Widely reported at the time; not checked against a Reserve Bank of Zimbabwe document for this day."},
    {"claim": "Length of each hyperinflation above Cagan's line (16, 20, about 50 months)", "status": "range",
     "note": "Approximate. Start and end dates differ between the Hanke-Krus table and national sources; Venezuela's end is usually dated to late 2021 or early 2022."},
    {"claim": "India's worst inflation years (38% in 1943-44, 25% in 1974-75, about 14% in 1991-92)", "status": "range",
     "note": "1943-44 figure from an academic WPI series; 1974 is often quoted as about 25% annual and 34.7% at the September 1974 year-on-year peak; 1991-92 rounded."},
    {"claim": "Bengal famine death toll", "status": "range",
     "note": "Estimates run from about 0.8 to 3.8 million; 2 to 3 million is the range most often cited."},
    {"claim": "ENCOVI 2017 average weight loss of 11 kg", "status": "disputed",
     "note": "Reuters reported an average loss of 11 kg; a UCV analysis describes six in ten Venezuelans losing about 11 kg. The denominator differs."},
    {"claim": "Iran: rial at 1,918,000 per dollar on 17 July 2026; inflation near 69 percent", "status": "unverified",
     "note": "Rate from Iran International and other press reports of the open market; inflation is the IMF projection for 2026 as quoted in press reports (a monthly reading of about 88 percent was also reported). Not checked against Central Bank of Iran data."},
    {"claim": "Venezuela 2026 figures (monthly peak 32.6% in January, 6.3% in May, 827.73 bolivars per dollar on 10 September)", "status": "unverified",
     "note": "Taken from press reports of BCV releases (El Diario, Finanzas Digital, NTN24, AFP); the BCV site itself was not checked. The 2025 annual 475% figure is from AFP reporting of the BCV release of March 2026. Monthly inflation was reported to have risen again in June 2026."},
    {"claim": "Zimbabwe ZiG inflation of 2.9% in August and about 3.7% in September 2026", "status": "unverified",
     "note": "From press reports of ZIMSTAT releases and the Reserve Bank's Monetary Policy Committee (2.9% in August described as the lowest since 1980; 3.7% in September also cited by the IMF); ZIMSTAT's own tables not checked."},
    {"claim": "Venezuelan oil output of about 3 million barrels a day in the late 1990s", "status": "range",
     "note": "Commonly cited as 3 to 3.5 million barrels a day; not checked against OPEC or EIA series. Later figures (2.4 million in 2015, 1.34 million end-2018, 374,000 in mid-2020) are from Rystad and Bloomberg reports."},
    {"claim": "Date the Rentenmark was introduced (15 or 16 November 1923)", "status": "range",
     "note": "The DHM and Wikipedia's Rentenmark article give 15 November 1923; Wikipedia's Weimar hyperinflation article gives 16 November. The day uses 15 November."},
    {"claim": "Zimbabwe annual inflation 2004 and 2006", "status": "range",
     "note": "Annual averages of 133% (2004) and 1,281% (2006) follow Wikipedia's table; year-on-year peaks within those years were much higher (over 600% in early 2004)."},
    {"claim": "India's 1991 gold shipments", "status": "range",
     "note": "Two operations: about 20 tonnes to UBS in May 1991 (a sale with repurchase option) and 46.91 tonnes to the Bank of England in July, pledged to it and the Bank of Japan. Some accounts merge them into one 67-tonne May airlift."},
    {"claim": "The wheelbarrow-thief story", "status": "unverified",
     "note": "A joke told about Weimar and other hyperinflations; no documented case found."},
    {"claim": "Lenin's remark about debauching the currency", "status": "disputed",
     "note": "Keynes wrote in 1919 that Lenin 'is said to have declared' it. No source in Lenin's writings is known."},
]

SIDE_DISH = {
    "area": "Psychology",
    "title": "Money illusion: why the number on the note fools us",
    "body_md": "In 1928 the Yale economist **Irving Fisher** published a small book called *The Money Illusion*. His point was simple: people think in the number printed on money, not in what it buys. A worker given a 10 percent raise in a year of 12 percent inflation often feels richer, though he is poorer.\n\nIn 1997 the psychologists Eldar Shafir and Amos Tversky, with the economist Peter Diamond, tested this with simple stories. Two people get the same real deal: one a 2 percent raise with no inflation, the other a 5 percent raise with 4 percent inflation. Most people judged the second one happier, even after agreeing the first was better off. The nominal number pulls at us.\n\nHyperinflation is where money illusion breaks. When prices double in a day, nobody can keep thinking in marks or bolivars. People switch, almost overnight, to a stable unit: dollars, rand, cigarettes, kilos of rice. Venezuelan market sellers in 2026 still price in bolivars, but buyers do the sums in dollars.\n\nThe illusion is strongest at low inflation, exactly where central banks like the RBI aim to keep us. That is one reason a stable 4 percent feels like nothing at all, and one reason why its slow effect on savings is so easy to ignore.\n\nTry it: what was your salary, or your pocket money, ten years ago? Now ask what it would buy today.",
    "image_ids": ["img_fisher"],
    "card_ids": ["c51", "c52"],
    "source_ids": ["wiki_money_illusion", "wiki_fisher"],
}

OFFLINE = {
    "kind": "try",
    "title": "Live one day at 24.7 hours",
    "body_md": "**Ten minutes with a pen and today's grocery bill.**\n\n1. Write down what you spent on food today, in rupees. Call it P.\n2. Zimbabwe in November 2008: prices doubled about once a day (every 24.7 hours). Write P, 2P, 4P, 8P... for each day of one week. On day 7 the same food costs about 128 times as much. After 30 days it costs roughly half a billion times as much.\n3. Weimar in October 1923: doubling every 3.7 days. Work out the price after 30 days (about 2 to the power 8, so about 270 times).\n4. India at the RBI's 4 percent target: use the **rule of 70**. Divide 70 by the inflation rate to get the years for prices to double. 70 / 4 = about **17.5 years**.\n5. Now look at the oldest banknote or coin you can find at home, or ask an older relative what a cup of tea, a cinema ticket or a bus fare cost when they were your age. Work out the yearly inflation that turns that price into today's.\n\n**Notice**: at 4 percent the doubling takes half a generation, so we barely see it. At 50 percent a month it takes under two months. The mathematics is the same; only the speed changes.",
    "source_ids": ["wiki_hyper", "outlook_target"],
}
