#!/usr/bin/env python3
"""Verify the chosen Commons files with pipeline/tools/commons.py and write t0803_images.py.
Run once (it calls the Commons API); the day build then reads t0803_images.py offline."""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

# id: (Commons file, alt text, caption)
CHOSEN = {
    "img_wallpaper": ("File:Bundesarchiv Bild 102-00104, Inflation, Tapezieren mit Geldscheinen.jpg",
                      "A man pasting banknotes onto a wall as wallpaper, 1923", "Banknotes as wallpaper during the German hyperinflation, 1923 (Bundesarchiv)."),
    "img_berlin_bank": ("File:In a Berlin Bank LCCN2014716642.jpg",
                        "Bank clerks in Berlin surrounded by stacks and bundles of banknotes", "'In a Berlin bank': bundles of paper marks, early 1920s (Library of Congress, Bain News Service)."),
    "img_notgeld_trier": ("File:Notgeld fritz quant 10 millionen mark.jpg",
                          "A colourful ten-million-mark emergency note from Trier", "Notgeld from Trier, 1923: ten million marks, designed by Fritz Quant."),
    "img_notgeld_essen": ("File:Essen hundert millionen 1923.jpg",
                          "A one-hundred-million-mark emergency note issued by the city of Essen", "Notgeld of the city of Essen, 1923: 100 million marks."),
    "img_notgeld_bochum": ("File:Notgeld der Stadt Bochum 1923 - 500 000 DM - Vorderseite.jpg",
                           "A 500,000-mark emergency note of the city of Bochum", "Notgeld of the city of Bochum, 1923: 500,000 marks."),
    "img_germany_chart": ("File:Germany Hyperinflation.png",
                          "Logarithmic chart of German prices rising from 1914 to 1923", "German price level 1914 to 1923 on a logarithmic scale (after Bresciani-Turroni)."),
    "img_rentenmark": ("File:1 rentenmark 1.11.1923 xx.jpg",
                       "A plain one-Rentenmark note dated 1 November 1923", "One Rentenmark, dated 1 November 1923: worth one trillion paper marks."),
    "img_rentenmark_1000": ("File:1000 Rentenmark 1923-11-1 xx.jpg",
                            "A 1,000-Rentenmark note dated 1 November 1923", "1,000 Rentenmark of 1 November 1923, equal to 1,000 trillion paper marks."),
    "img_overprint": ("File:Eintausend Mark Reichsbanknote 15. Dezember 1922 Eine Milliarde Mark German Weimar Republic 1000 marks bill overprinted overstamped 1 billion inflation period 1923 Portrait mintmaster J Herz (Holocaust exhibition HL-senteret Oslo 20.jpg",
                      "A 1,000-mark note of December 1922 overprinted in red to read one billion marks", "A 1,000-mark Reichsbank note overprinted in 1923 as 'Eine Milliarde Mark', one billion marks."),
    "img_havenstein": ("File:R.E. Havenstein LCCN2014716679.jpg",
                       "Portrait photograph of Rudolf Havenstein, an elderly man with a beard", "Rudolf Havenstein, president of the Reichsbank 1908 to 1923 (Library of Congress)."),
    "img_havenstein_cartoon": ("File:General Geldmarschall Havenstein.jpg",
                               "A caricature of Havenstein titled General Geldmarschall", "'General Geldmarschall Havenstein': a 1915 caricature of the Reichsbank president from the war-loan years."),
    "img_schacht": ("File:Hjalmar Schacht.jpg",
                    "Portrait of Hjalmar Schacht in a high starched collar", "Hjalmar Schacht, currency commissioner from November 1923 and later Reichsbank president."),
    "img_ruhr": ("File:French enter Essen.jpg",
                 "French troops entering the city of Essen in 1923", "French troops enter Essen at the start of the Ruhr occupation, January 1923."),
    "img_zim_100tn": ("File:Zimbabwe $100 trillion 2009 Obverse.jpg",
                      "Zimbabwe 100 trillion dollar banknote, front", "Zimbabwe's 100 trillion dollar note, issued 16 January 2009."),
    "img_zim_range": ("File:Zimbabwe dollar notes 1 to 100 trillion 2007 08 Front.jpg",
                      "Sixteen Zimbabwean banknotes from one dollar to 100 trillion dollars laid out together", "Sixteen Zimbabwe dollar notes of 2007-09, from 1 dollar to 100 trillion."),
    "img_bearer_cheque": ("File:Zimbabwe 100,000 dollar note.jpg",
                          "A Zimbabwean 100,000 dollar bearer cheque", "A Z$100,000 bearer cheque, the 'temporary' money of 2003 to 2008."),
    "img_ven_bolivar_notes": ("File:Billete de 100000 Bolìvares.jpg",
                              "A Venezuelan 100,000 bolivar note", "A 100,000 bolivar fuerte note, the largest of 2017-18."),
    "img_bolivar_soberano": ("File:Billete de 20000 Bolìvares.jpg",
                             "A Venezuelan 20,000 bolivar note", "A 20,000 bolivar fuerte note of 2017, before five zeros were cut in 2018."),
    "img_mugabe": ("File:Robert Mugabe - 2009.jpg",
                   "Robert Mugabe in 2009, wearing glasses and a dark suit", "Robert Mugabe in 2009."),
    "img_chavez": ("File:Hugo Chávez (02-04-2010).jpg",
                   "Hugo Chavez seated behind a microphone", "Hugo Chavez in 2010."),
    "img_maduro": ("File:Nicolás Maduro in 2023 (cropped).jpg",
                   "Nicolas Maduro in 2023", "Nicolas Maduro in May 2023."),
    "img_pengo": ("File:Hungarian One Sextillion Pengő Paper Money in 1946.jpg",
                  "A Hungarian one sextillion pengo note of 1946 in a museum display", "Hungary's one sextillion (milliard b-pengo) note of 1946, printed but never issued (MUFG Bank Currency Museum)."),
    "img_dinar": ("File:500million-dinar-1993-Yugoslav-obverse.jpg",
                  "A Yugoslav 500 million dinar note of 1993", "A 500 million dinar note of 1993; by year's end the top note was 500 billion."),
    "img_putsch": ("File:Hitlerputsch, barricade in Munich (1923).jpg",
                   "Armed men behind a street barricade in Munich, November 1923", "A barricade during the failed Hitler putsch in Munich, November 1923."),
    "img_putsch_odeon": ("File:Bundesarchiv Bild 119-1426, Hitler-Putsch, München, Odeonsplatz.jpg",
                         "Crowds and armed men at the Odeonsplatz in Munich during the 1923 putsch", "Munich's Odeonsplatz during the putsch of 8 to 9 November 1923 (Bundesarchiv)."),
    "img_stinnes": ("File:Hugo Stinnes - LCCN2014711231 (cropped).jpg",
                    "Portrait photograph of the industrialist Hugo Stinnes with a dark beard", "Hugo Stinnes, the industrialist who grew rich on the inflation (Library of Congress)."),
    "img_sargent": ("File:Thomas J. Sargent close-up (cropped).jpg",
                    "Thomas J. Sargent at the 2011 Nobel press conference", "Thomas J. Sargent, Nobel laureate in economics, 2011."),
    "img_keynes": ("File:John Maynard Keynes 1929.jpg",
                   "John Maynard Keynes seated, holding a book", "John Maynard Keynes, author of The Economic Consequences of the Peace (1919)."),
    "img_rbi": ("File:Tower and building of Reserve Bank of India, Mumbai 01.jpg",
                "The Reserve Bank of India tower and building in Mumbai", "The Reserve Bank of India in Mumbai."),
    "img_bengal": ("File:Destitute mother and child Bengal famine 1943.jpg",
                   "A destitute mother and child on a Calcutta pavement in 1943", "A destitute mother and child in Calcutta during the Bengal famine, 1943 (from Bengal Speaks, 1944)."),
    "img_milei": ("File:Javier Milei en el Salón Blanco 2 (cropped).jpg",
                  "Javier Milei speaking in the White Hall of the Casa Rosada", "Javier Milei on the day he took office as president of Argentina, December 2023."),
    "img_bridge": ("File:Bolivarian diaspora - Colombia 2018.jpg",
                   "Colombian police leading Venezuelan migrants across the border bridge", "Venezuelans crossing from San Antonio del Tachira into Colombia, 2018."),
    "img_bridge_2": ("File:Simón Bolívar International Bridge.jpg",
                     "The Simon Bolivar International Bridge between Venezuela and Colombia", "The Simon Bolivar International Bridge, seen from the Venezuelan side."),
    "img_pdvsa": ("File:Edificio PDVSA 5 de Julio.jpg",
                  "The main PDVSA office building on Avenida 5 de Julio in Maracaibo", "PDVSA's main building in Maracaibo, the heart of Venezuela's oil industry."),
    "img_zim_tobacco": ("File:People working among tobacco plants, Rhodesia LCCN89714079.jpg",
                        "Workers standing among tall tobacco plants in a field", "Workers among tobacco plants in Rhodesia, early 20th century (Library of Congress)."),
    "img_assignat": ("File:Assignat de cinquante livres 1792.jpg",
                     "A French assignat for fifty livres, 1792", "An assignat for 50 livres issued by the French Republic in 1792."),
    "img_assignat_fake": ("File:Assignat-faux.jpg",
                          "A forged 300-livre assignat stamped as certified false", "A forged 300-livre assignat, stamped 'certified false': forgeries helped sink the currency."),
    "img_continental": ("File:Continental Currency $55 banknote obverse (January 14, 1779).jpg",
                        "A small Continental Currency note for 55 dollars, 1779", "A Continental Currency 55-dollar note of 14 January 1779."),
    "img_continental_leaf": ("File:Benjamin Franklin nature printed currency sheet 1779.jpg",
                             "An uncut sheet of 1779 Continental notes with leaf prints on the back", "Backs of 1779 Continental notes, printed with real leaf patterns to defeat forgers (Franklin's nature printing)."),
    "img_bayer_note": ("File:Notgeld 1923.jpg",
                       "A 1923 one-million-mark emergency note from Weimar with large sans-serif numerals", "One million marks, Thuringia 1923: emergency money designed by Herbert Bayer of the Bauhaus."),
    "img_rupee": ("File:Indian 50-rupees banknote closeup (68912).jpg",
                  "Close-up of an Indian 50-rupee banknote", "An Indian 50-rupee note."),
    "img_caracas": ("File:Mercado de calle en Caracas.jpg",
                    "Vegetable and fruit sellers at a street market in Caracas", "A street market in Caracas, where prices are worked out in dollars."),
    "img_caracas_2025": ("File:Mercado Mayorista de Coche, Caracas Venezuela 3 de diciembre de 2025.jpg",
                         "The Coche wholesale market in Caracas, December 2025", "Mercado Mayor de Coche, Caracas, December 2025."),
    "img_fisher": ("File:Prof Irving Fisher, noted economist - photo. by Bain News Service, New York. LCCN90711700 (cropped).jpg",
                   "Portrait of the economist Irving Fisher", "Irving Fisher of Yale, who named the 'money illusion' in 1928 (Library of Congress)."),
    "img_gono": ("File:Gideon Gono10.jpg",
                 "Gideon Gono in a dark suit after addressing Zimbabwe's parliament", "Gideon Gono, Reserve Bank of Zimbabwe governor, after a monetary policy statement to parliament, 2008."),
    "img_cholera": ("File:2008 Zimbabwe Cholera Outbreak Cases by District.png",
                    "Map of Zimbabwe shaded by the number of cholera cases in each province and district", "Cholera cases in Zimbabwe by province and district, as of 3 December 2008 (Red Cross data)."),
    "img_maduro_dea": ("File:Nicolás Maduro being escorted by the DEA.jpg",
                       "Nicolas Maduro being escorted by US Drug Enforcement Administration agents", "Nicolas Maduro in US custody, January 2026."),
}

def main():
    extra = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
    chosen = dict(CHOSEN)
    chosen.update({k: tuple(v) for k, v in extra.items()})
    titles = [v[0] for v in chosen.values()]
    out = subprocess.run([sys.executable, os.path.join(ROOT, "pipeline/tools/commons.py"), "verify", *titles], capture_output=True, text=True)
    recs = json.loads(out.stdout)
    by_title = {}
    for r in recs:
        t = r.get("title")
        if t and not r.get("error"):
            by_title[t] = r
    images = {}
    for iid, (title, alt, cap) in chosen.items():
        r = by_title.get(title) or by_title.get(title.replace("_", " "))
        if not r:
            print("MISSING", iid, title)
            continue
        if not r.get("free"):
            print("NOT FREE", iid, title, r.get("license"))
            continue
        rec = {k: r[k] for k in ("url", "thumb_url", "width", "height", "author", "license", "license_url", "file_page", "attribution", "verified_on")}
        rec["alt"] = alt
        rec["caption"] = cap
        images[iid] = rec
    with open(os.path.join(HERE, "t0803_images.py"), "w", encoding="utf-8") as f:
        f.write("# Generated by t0803_mkimages.py from commons.py verify. Do not edit by hand.\n")
        f.write("IMAGE_RECORDS = " + json.dumps(images, ensure_ascii=False, indent=1) + "\n")
    print("wrote", len(images), "images")

if __name__ == "__main__":
    main()
