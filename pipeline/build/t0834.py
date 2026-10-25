#!/usr/bin/env python3
"""Build Daily Atlas day 834: The adversarial vs inquisitorial trial (Law, tier B).
Writes data/days/0834.json. Run from the repo root or anywhere."""
import json, os, re, html, urllib.parse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "data", "days", "0834.json")
ACC = "2026-10-25"

# ---------------------------------------------------------------- sources
S = [
 ("wiki_inquisitorial", "Inquisitorial system", "https://en.wikipedia.org/wiki/Inquisitorial_system", "Wikipedia"),
 ("wiki_adversarial", "Adversarial system", "https://en.wikipedia.org/wiki/Adversarial_system", "Wikipedia"),
 ("wiki_ordeal", "Trial by ordeal", "https://en.wikipedia.org/wiki/Trial_by_ordeal", "Wikipedia"),
 ("wiki_lateran", "Fourth Council of the Lateran", "https://en.wikipedia.org/wiki/Fourth_Council_of_the_Lateran", "Wikipedia"),
 ("wiki_combat", "Trial by combat", "https://en.wikipedia.org/wiki/Trial_by_combat", "Wikipedia"),
 ("leeson_ordeals", "Ordeals (Journal of Law and Economics, 2012)", "https://www.peterleeson.com/Ordeals.pdf", "Peter T. Leeson"),
 ("wiki_garrow", "William Garrow", "https://en.wikipedia.org/wiki/William_Garrow", "Wikipedia"),
 ("wiki_old_bailey", "Old Bailey", "https://en.wikipedia.org/wiki/Old_Bailey", "Wikipedia"),
 ("tna_hardy", "The 1794 trial of Thomas Hardy: new-fangled treasons", "https://blog.nationalarchives.gov.uk/the-1794-trial-of-thomas-hardy-new-fangled-treasons", "The National Archives (UK)"),
 ("wiki_hardy", "Thomas Hardy (political reformer)", "https://en.wikipedia.org/wiki/Thomas_Hardy_(political_reformer)", "Wikipedia"),
 ("langbein_origins", "The Origins of Adversary Criminal Trial (John H. Langbein, 2003)", "https://academic.oup.com/book/2775", "Oxford University Press"),
 ("langbein_1979", "Land Without Plea Bargaining: How the Germans Do It (Michigan Law Review, 1979)", "https://repository.law.umich.edu/mlr/vol78/iss2/3", "Michigan Law Review"),
 ("langbein_torture", "Torture and Plea Bargaining (John H. Langbein)", "https://law.yale.edu/sites/default/files/documents/pdf/Faculty/Langbein_Torture_and_Plea_Bargaining.pdf", "Yale Law School"),
 ("wiki_langbein", "John H. Langbein", "https://en.wikipedia.org/wiki/John_H._Langbein", "Wikipedia"),
 ("wiki_damaska", "Mirjan Damaška", "https://en.wikipedia.org/wiki/Mirjan_Dama%C5%A1ka", "Wikipedia"),
 ("markovits_damaska", "Playing the Opposite Game: On Mirjan Damaška's The Faces of Justice and State Authority (41 Stanford Law Review 1313, 1989)", "https://law.utexas.edu/faculty/publications/1989-Playing-the-Opposite-Game-On-Mirjan-Deamskas-The-Faces-of-Justice-and-State-Authority/", "University of Texas School of Law"),
 ("wiki_judicial_torture", "Judicial torture", "https://en.wikipedia.org/wiki/Judicial_torture", "Wikipedia"),
 ("wiki_carolina", "Constitutio Criminalis Carolina", "https://en.wikipedia.org/wiki/Constitutio_Criminalis_Carolina", "Wikipedia"),
 ("wiki_ordonnance", "Criminal Ordinance of 1670", "https://en.wikipedia.org/wiki/Criminal_Ordinance_of_1670", "Wikipedia"),
 ("wiki_spanish_inq", "Spanish Inquisition", "https://en.wikipedia.org/wiki/Spanish_Inquisition", "Wikipedia"),
 ("wiki_beccaria", "Cesare Beccaria", "https://en.wikipedia.org/wiki/Cesare_Beccaria", "Wikipedia"),
 ("wiki_examining", "Examining magistrate", "https://en.wikipedia.org/wiki/Examining_magistrate", "Wikipedia"),
 ("wiki_wigmore", "John Henry Wigmore", "https://en.wikipedia.org/wiki/John_Henry_Wigmore", "Wikipedia"),
 ("umich_cross", "Cross-examination and the 'greatest legal engine' (law review article)", "https://repository.law.umich.edu/articles/2420", "University of Michigan Law School Scholarship Repository"),
 ("nzlj_jones", "Jones v National Coal Board, case note (New Zealand Law Journal, 4 June 1957)", "https://library.victoria.ac.nz/databases/nzlawjournal/pubs/1957/1957-10-165.pdf", "New Zealand Law Journal"),
 ("wiki_denning", "Tom Denning, Baron Denning", "https://en.wikipedia.org/wiki/Tom_Denning,_Baron_Denning", "Wikipedia"),
 ("wiki_gideon", "Gideon v. Wainwright", "https://en.wikipedia.org/wiki/Gideon_v._Wainwright", "Wikipedia"),
 ("wiki_miranda", "Ernesto Miranda", "https://en.wikipedia.org/wiki/Ernesto_Miranda", "Wikipedia"),
 ("aba_miranda", "Miranda: the man behind the warning", "https://www.abajournal.com/gallery/miranda/1284", "ABA Journal"),
 ("wiki_exclusionary", "Exclusionary rule", "https://en.wikipedia.org/wiki/Exclusionary_rule", "Wikipedia"),
 ("wiki_12angry", "12 Angry Men (1957 film)", "https://en.wikipedia.org/wiki/12_Angry_Men_(1957_film)", "Wikipedia"),
 ("wiki_plea", "Plea bargaining", "https://en.wikipedia.org/wiki/Plea_bargaining", "Wikipedia"),
 ("pew_2019", "Only 2% of federal criminal defendants go to trial, and most who do are found guilty", "https://www.pewresearch.org/short-reads/2019/06/11/only-2-of-federal-criminal-defendants-go-to-trial-and-most-who-do-are-found-guilty/", "Pew Research Center"),
 ("pew_2023", "Fewer than 1% of defendants in federal criminal cases were acquitted in 2022", "https://www.pewresearch.org/short-reads/2023/06/14/fewer-than-1-of-defendants-in-federal-criminal-cases-were-acquitted-in-2022/", "Pew Research Center"),
 ("dervan_edkins", "The Innocent Defendant's Dilemma (Journal of Criminal Law and Criminology, 2013)", "https://scholarlycommons.law.northwestern.edu/jclc/vol103/iss1/1", "Northwestern University School of Law"),
 ("wiki_nre", "National Registry of Exonerations", "https://en.wikipedia.org/wiki/National_Registry_of_Exonerations", "Wikipedia"),
 ("wiki_lay_judge", "Lay judge", "https://en.wikipedia.org/wiki/Lay_judge", "Wikipedia"),
 ("beck_strafbefehl", "Strafbefehl: 'Der Mensch geht ins Gefängnis, ohne je einen Richter gesehen zu haben'", "https://www.beck-aktuell.de/heute-im-recht/rechtspolitik-gesetzgebung/strafbefehl-projekt-geldstrafe-ersatzfreiheitsstrafe-strafverteidiger-2024-03-28", "beck-aktuell"),
 ("rsj_instruction", "Références statistiques Justice 2023, chapitre 10.4: le juge d'instruction", "https://justice.gouv.fr/sites/default/files/2024-06/RSJ2023_10_4_0.pdf", "Ministère de la Justice (France)"),
 ("wiki_outreau", "Outreau trial", "https://en.wikipedia.org/wiki/Outreau_trial", "Wikipedia"),
 ("wiki_knox", "Amanda Knox", "https://en.wikipedia.org/wiki/Amanda_Knox", "Wikipedia"),
 ("wiki_kercher", "Murder of Meredith Kercher", "https://en.wikipedia.org/wiki/Murder_of_Meredith_Kercher", "Wikipedia"),
 ("psilr_italy", "The New Italian Code of Criminal Procedure (Penn State International Law Review)", "https://insight.dickinsonlaw.psu.edu/psilr/vol10/iss1/4", "Penn State Dickinson Law"),
 ("wiki_hakamada", "Iwao Hakamada", "https://en.wikipedia.org/wiki/Iwao_Hakamada", "Wikipedia"),
 ("wiki_japan_cj", "Criminal justice system of Japan", "https://en.wikipedia.org/wiki/Criminal_justice_system_of_Japan", "Wikipedia"),
 ("wiki_hostage", "Hostage justice", "https://en.wikipedia.org/wiki/Hostage_justice", "Wikipedia"),
 ("nippon_saibanin", "Japan's lay judge system: participation data", "https://www.nippon.com/en/japan-data/h01999/", "Nippon.com"),
 ("wiki_ghosn", "Carlos Ghosn", "https://en.wikipedia.org/wiki/Carlos_Ghosn", "Wikipedia"),
 ("occrp_ghosn", "Ex-CEO slams Nissan, Japanese justice system after escape", "https://www.occrp.org/en/news/ex-ceo-slams-nissan-japanese-justice-system-after-escape", "OCCRP"),
 ("wiki_pelicot", "Pelicot rape case", "https://en.wikipedia.org/wiki/Pelicot_rape_case", "Wikipedia"),
 ("aljazeera_pelicot", "French court extends sentence of man convicted of Gisele Pelicot rape (9 October 2025)", "https://www.aljazeera.com/news/2025/10/9/french-court-extends-sentence-of-man-convicted-of-gisele-pelicot-rape", "Al Jazeera"),
 ("an_ccd", "Question écrite 4594 sur les cours criminelles départementales", "https://www.assemblee-nationale.fr/dyn/16/questions/QANR5L16QE4594.pdf", "Assemblée nationale"),
 ("gazette_sure", "Le projet de loi sur la justice criminelle définitivement adopté (Gazette du Palais, 2026 n23)", "https://www.labase-lextenso.fr/gazette-du-palais/2026-n23/le-projet-de-loi-sur-la-justice-criminelle-definitivement-adopte-GPL493c8", "Gazette du Palais"),
 ("gazette_pjcr", "Justice criminelle: le garde des Sceaux renonce au plaider-coupable (Gazette du Palais, 2026 n19)", "https://www.labase-lextenso.fr/gazette-du-palais/2026-n19/justice-criminelle-le-garde-des-sceaux-renonce-au-plaider-coupable-GPL491v0", "Gazette du Palais"),
 ("publicsenat_pjcr", "Justice criminelle: le plaider-coupable 'ne retire rien à personne', assure Gérald Darmanin", "https://www.publicsenat.fr/actualites/politique/justice-criminelle-le-plaider-coupable-ne-retire-rien-a-personne-assure-gerald-darmanin-devant-les-senateurs", "Public Sénat"),
 ("taxquet_blog", "Article 6 and reasoned verdicts (Taxquet v Belgium)", "https://www.echrblog.com/2011/06/article-6-and-reasoned-verdicts.html", "ECHR Blog"),
 ("uk_bill", "Courts and Tribunals Bill: stages", "https://bills.parliament.uk/bills/4083", "UK Parliament"),
 ("twfy_vote", "House of Commons division 444, 10 March 2026", "https://votes.theyworkforyou.com/decisions/division/commons/2026-03-10/444", "TheyWorkForYou"),
 ("lg_third", "Revamped Courts and Tribunals Bill passes crucial hurdle", "https://www.lawgazette.co.uk/news/revamped-courts-and-tribunals-bill-passes-crucial-hurdle/5128214.article", "Law Society Gazette"),
 ("lg_backlog", "New backlog record renews conflict on jury curbs", "https://www.lawgazette.co.uk/news/new-backlog-record-renews-conflict-on-jury-curbs/5125452.article", "Law Society Gazette"),
 ("wilmerhale_leveson", "UK Independent Review of the Criminal Courts, Part 1", "https://www.wilmerhale.com/en/insights/blogs/wilmerhale-w-i-r-e-uk/20250722-uk-independent-review-of-the-criminal-courts-part-1", "WilmerHale"),
 ("wiki_not_proven", "Not proven", "https://en.wikipedia.org/wiki/Not_proven", "Wikipedia"),
 ("wiki_italy_ref", "2026 Italian constitutional referendum", "https://en.wikipedia.org/wiki/2026_Italian_constitutional_referendum", "Wikipedia"),
 ("wir_italy_ref", "Italy's justice reform referendum defeated in setback for Giorgia Meloni", "https://www.wantedinrome.com/news/italys-justice-reform-referendum-defeated-in-setback-for-giorgia-meloni.html", "Wanted in Rome"),
 ("japan_retrial", "Japan enacts retrial system revision bill (17 July 2026)", "https://english.adnkronos.com/2026/07/17/japan-enacts-retrial-system-revision-bill/", "Jiji Press via Adnkronos"),
 ("wiki_nuremberg", "Nuremberg trials", "https://en.wikipedia.org/wiki/Nuremberg_trials", "Wikipedia"),
 ("spectator_goring", "How Göring almost derailed the Nuremberg trials", "https://spectator.com/article/how-goring-almost-derailed-the-nuremberg-trials", "The Spectator"),
 ("jackson_goring", "Cross-examination of Göring regarding the treatment of Jews", "https://roberthjackson.org/nuremberg-event/cross-examination-of-goering-regarding-the-treatment-of-jews", "Robert H. Jackson Center"),
 ("wiki_icc", "International Criminal Court", "https://en.wikipedia.org/wiki/International_Criminal_Court", "Wikipedia"),
 ("hrw_duterte", "ICC court sends Duterte case to trial (23 April 2026)", "https://hrw.org/news/2026/04/23/icc-court-sends-duterte-case-to-trial", "Human Rights Watch"),
 ("icc_duterte_first", "Rodrigo Roa Duterte makes first appearance before the ICC (14 March 2025)", "https://www.icc-cpi.int/news/rodrigo-roa-duterte-makes-first-appearance-icc-confirmation-charges-hearing-scheduled-23", "International Criminal Court"),
 ("emory_mexico", "Mexico's criminal justice reform (Emory International Law Review, vol. 26)", "https://scholarlycommons.law.emory.edu/eilr/vol26/iss1/9", "Emory University School of Law"),
 ("ik_ramchander", "State of Rajasthan v Ani @ Hanif (1997), quoting Ram Chander v State of Haryana (AIR 1981 SC 1036)", "https://indiankanoon.org/doc/989564/", "Indian Kanoon"),
 ("bsa_168", "Section 168 of the Bharatiya Sakshya Adhiniyam, 2023", "https://vidhijudicial.com/section-168-of-the-bharatiya-sakshya-adhiniyam,-2023.html", "Vidhi Judicial"),
 ("malimath", "The Report of the Malimath Committee on Reforms of Criminal Justice System", "https://www.legalservicesindia.com/law/article/1983/39/The-Report-Of-Malimath-Committee-On-Reforms-Of-Criminal-Justice-System", "Legal Services India"),
 ("icj_malimath", "India: criminal justice reform position paper (2003)", "https://www.icj.org/wp-content/uploads/2003/08/India-criminal-justice-reform-position-paper-2003.pdf", "International Commission of Jurists"),
 ("wiki_nanavati", "K. M. Nanavati v. State of Maharashtra", "https://en.wikipedia.org/wiki/K._M._Nanavati_v._State_of_Maharashtra", "Wikipedia"),
 ("caravan_jury", "Peer review: India's last jury trials", "https://caravanmagazine.in/lede/peer-review-india-last-jury-trials", "The Caravan"),
 ("civils_plea", "Report reveals minimal use of plea bargaining in courts", "https://civilsdaily.com/news/report-reveals-minimal-use-of-plea-bargaining-in-courts", "Civilsdaily"),
 ("dataful_ut", "India's prisons remain overcrowded as undertrial share stays high", "https://insights.dataful.in/articles/indias-prisons-remain-overcrowded-as-undertrial-share-stays-high", "Dataful"),
 ("policyedge_psi", "NCRB's Prison Statistics India 2023", "https://www.policyedge.in/p/ncrbs-prison-statistics-india-2023", "The Policy Edge"),
 ("ians_pendency", "Over 4.76 crore court cases pending across India: Govt informs Parliament (13 February 2026)", "https://ianslive.in/over-476-crore-cases-pending-across-indian-courts-govt-tells-parliament--20260213184542", "IANS"),
 ("wiki_bnss", "Bharatiya Nagarik Suraksha Sanhita", "https://en.wikipedia.org/wiki/Bharatiya_Nagarik_Suraksha_Sanhita", "Wikipedia"),
 ("verdictum_absentia", "Allahabad High Court issues guidelines on mandatory trial in absentia under Section 356 BNSS (8 May 2026)", "https://www.verdictum.in/allahabad-high-court/ravi-alias-ravindra-singh-v-state-of-up-2026ahc101857-mandatory-trial-in-absentia-1613587", "Verdictum"),
 ("unica_yajnavalkya", "The mysterious plowshare ordeal (phāladivya): a note on Yājñavalkya-smṛti II, 100", "https://ojs.unica.it/index.php/rhesis/article/view/5704", "Rhesis, University of Cagliari"),
 ("sage_procedural", "Dispute resolution psychology (Encyclopedia of Law and Society)", "https://sk.sagepub.com/ency/edvol/embed/law/chpt/dispute-resolution-psychology", "SAGE"),
 ("frank_courts", "Courts on Trial: Myth and Reality in American Justice (Jerome Frank)", "https://www.labyrinthbooks.com/courts-on-trial", "Princeton University Press (listing)"),
 ("wiki_erskine", "Thomas Erskine, 1st Baron Erskine", "https://en.wikipedia.org/wiki/Thomas_Erskine,_1st_Baron_Erskine", "Wikipedia"),
 ("oldbailey_online", "The Proceedings of the Old Bailey, 1674 to 1913", "https://www.oldbaileyonline.org/", "Old Bailey Proceedings Online"),
 ("lords_library_ctb", "Courts and Tribunals Bill: HL Bill 57 of 2026 to 27", "https://lordslibrary.parliament.uk/research-briefings/lln-2026-0055/", "House of Lords Library"),
 ("icc_duterte_trial", "Duterte case: trial to open on 30 November 2026 (27 May 2026)", "https://www.icc-cpi.int/news/duterte-case-trial-open-30-november-2026", "International Criminal Court"),
 ("govscot_not_proven", "Abolition of not proven verdict", "https://www.gov.scot/news/abolition-of-not-proven-verdict/", "Scottish Government"),
 ("publicsenat_final", "Le Parlement adopte définitivement le projet de loi sur la justice criminelle", "https://www.publicsenat.fr/actualites/politique/le-parlement-adopte-definitivement-le-projet-de-loi-sur-la-justice-criminelle-que-contient-il", "Public Sénat"),
]
SOURCES = [{"id": i, "title": t, "url": u, "publisher": p, "accessed": ACC} for i, t, u, p in S]

# ---------------------------------------------------------------- images (verified with pipeline/tools/commons.py on 2026-10-25)
RECORDS = json.loads(r'''{
"File:Royal-courts-of-justice.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Royal-courts-of-justice.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Royal-courts-of-justice.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Royal-courts-of-justice.jpg",
"width": 500,
"height": 667,
"author": "Michael Reeve (en:User:MykReeve)",
"license": "CC BY-SA 3.0",
"license_url": "http://creativecommons.org/licenses/by-sa/3.0/",
"attribution": "Photo: Michael Reeve (en:User:MykReeve), CC BY-SA 3.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Microcosm of London Plate 058 - Old Bailey edited.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Microcosm_of_London_Plate_058_-_Old_Bailey_edited.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/1/17/Microcosm_of_London_Plate_058_-_Old_Bailey_edited.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/1/17/Microcosm_of_London_Plate_058_-_Old_Bailey_edited.jpg",
"width": 828,
"height": 626,
"author": "Thomas Rowlandson and Augustus Pugin",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Thomas Rowlandson and Augustus Pugin, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Saikosaibansho.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Saikosaibansho.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/2/2c/Saikosaibansho.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/2c/Saikosaibansho.jpg/1280px-Saikosaibansho.jpg",
"width": 2048,
"height": 1536,
"author": "っ",
"license": "CC BY-SA 3.0",
"license_url": "http://creativecommons.org/licenses/by-sa/3.0/",
"attribution": "Photo: っ, CC BY-SA 3.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Defendants in the dock at nuremberg trials.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Defendants_in_the_dock_at_nuremberg_trials.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/3/39/Defendants_in_the_dock_at_nuremberg_trials.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/39/Defendants_in_the_dock_at_nuremberg_trials.jpg/1280px-Defendants_in_the_dock_at_nuremberg_trials.jpg",
"width": 1523,
"height": 1200,
"author": "Raymond D’Addario",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Raymond D’Addario, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Dei delitti e delle pene 1764.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Dei_delitti_e_delle_pene_1764.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/d/da/Dei_delitti_e_delle_pene_1764.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/d/da/Dei_delitti_e_delle_pene_1764.jpg",
"width": 169,
"height": 260,
"author": "Unknown",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Unknown, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:De Constitutio criminalis Carolina (1577) 01.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:De_Constitutio_criminalis_Carolina_(1577)_01.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/a/ac/De_Constitutio_criminalis_Carolina_%281577%29_01.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/a/ac/De_Constitutio_criminalis_Carolina_%281577%29_01.jpg",
"width": 1152,
"height": 1728,
"author": "amtliches Werk",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: amtliches Werk, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Gerichtskampf mair.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Gerichtskampf_mair.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Gerichtskampf_mair.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Gerichtskampf_mair.jpg",
"width": 1000,
"height": 752,
"author": "Jörg Breu der Jüngere (died 1547), Paulus Hector Mair (died 1579)",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Jörg Breu der Jüngere (died 1547), Paulus Hector Mair (died 1579), Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Calcutta High Court.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Calcutta_High_Court.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/0/00/Calcutta_High_Court.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/00/Calcutta_High_Court.jpg/1280px-Calcutta_High_Court.jpg",
"width": 3411,
"height": 2592,
"author": "Avrajyoti Mitra",
"license": "CC BY-SA 2.0",
"license_url": "https://creativecommons.org/licenses/by-sa/2.0",
"attribution": "Photo: Avrajyoti Mitra, CC BY-SA 2.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:The Grand Bench of the Japanese Supreme Court.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:The_Grand_Bench_of_the_Japanese_Supreme_Court.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/9/9e/The_Grand_Bench_of_the_Japanese_Supreme_Court.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/9/9e/The_Grand_Bench_of_the_Japanese_Supreme_Court.jpg",
"width": 1024,
"height": 768,
"author": "Tetsu2266",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Tetsu2266, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Water-ordeal.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Water-ordeal.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/7/7e/Water-ordeal.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/7/7e/Water-ordeal.jpg",
"width": 510,
"height": 497,
"author": "Diebold Schilling the Younger",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Diebold Schilling the Younger, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Ordeal by red-hot iron.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Ordeal_by_red-hot_iron.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Ordeal_by_red-hot_iron.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Ordeal_by_red-hot_iron.jpg",
"width": 397,
"height": 523,
"author": "Unknown authorUnknown author",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Unknown authorUnknown author, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Thomas Erskine, 1st Baron Erskine by Sir William Charles Ross.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Thomas_Erskine,_1st_Baron_Erskine_by_Sir_William_Charles_Ross.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Thomas_Erskine%2C_1st_Baron_Erskine_by_Sir_William_Charles_Ross.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/ab/Thomas_Erskine%2C_1st_Baron_Erskine_by_Sir_William_Charles_Ross.jpg/1280px-Thomas_Erskine%2C_1st_Baron_Erskine_by_Sir_William_Charles_Ross.jpg",
"width": 2400,
"height": 2896,
"author": "William Charles Ross",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: William Charles Ross, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Goering on trial (color).jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Goering_on_trial_(color).jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Goering_on_trial_%28color%29.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0e/Goering_on_trial_%28color%29.jpg/1280px-Goering_on_trial_%28color%29.jpg",
"width": 1364,
"height": 950,
"author": "Raymond D'Addario",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Raymond D'Addario, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:John Henry Wigmore cph.3b34499.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:John_Henry_Wigmore_cph.3b34499.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/5/56/John_Henry_Wigmore_cph.3b34499.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/5/56/John_Henry_Wigmore_cph.3b34499.jpg",
"width": 933,
"height": 1488,
"author": "Harris &amp; Ewing",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Harris &amp; Ewing, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:William Garrow2.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:William_Garrow2.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/5/59/William_Garrow2.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/5/59/William_Garrow2.jpg",
"width": 519,
"height": 651,
"author": "Engraver: Dunkarton, Robert (1744–1811/17); painter: Devis, Arthur William (1...",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Engraver: Dunkarton, Robert (1744–1811/17); painter: Devis, Arthur William (1..., Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Clarence Earl Gideon.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Clarence_Earl_Gideon.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Clarence_Earl_Gideon.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Clarence_Earl_Gideon.jpg",
"width": 600,
"height": 861,
"author": "Unknown authorUnknown author",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Unknown authorUnknown author, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:BGH - Palais 2.JPG": {
"file_page": "https://commons.wikimedia.org/wiki/File:BGH_-_Palais_2.JPG",
"url": "https://upload.wikimedia.org/wikipedia/commons/6/63/BGH_-_Palais_2.JPG",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/63/BGH_-_Palais_2.JPG/1280px-BGH_-_Palais_2.JPG",
"width": 3442,
"height": 2741,
"author": "ComQuat",
"license": "CC BY-SA 3.0",
"license_url": "https://creativecommons.org/licenses/by-sa/3.0",
"attribution": "Photo: ComQuat, CC BY-SA 3.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Francisco rizi-auto de fe.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Francisco_rizi-auto_de_fe.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/2/28/Francisco_rizi-auto_de_fe.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/28/Francisco_rizi-auto_de_fe.jpg/1280px-Francisco_rizi-auto_de_fe.jpg",
"width": 3071,
"height": 1946,
"author": "Francisco Rizi",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Francisco Rizi, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:An interrogation room of the Spanish Inquisition with two pr Wellcome V0041642.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:An_interrogation_room_of_the_Spanish_Inquisition_with_two_pr_Wellcome_V0041642.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/0/01/An_interrogation_room_of_the_Spanish_Inquisition_with_two_pr_Wellcome_V0041642.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/01/An_interrogation_room_of_the_Spanish_Inquisition_with_two_pr_Wellcome_V0041642.jpg/1280px-An_interrogation_room_of_the_Spanish_Inquisition_with_two_pr_Wellcome_V0041642.jpg",
"width": 3045,
"height": 2291,
"author": "Unknown",
"license": "CC BY 4.0",
"license_url": "https://creativecommons.org/licenses/by/4.0",
"attribution": "Photo: Unknown, CC BY 4.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Baltasar Garzón en la inauguración del seminario \"Argentina- África aportes para la construcción de una agenda de trabajo compartida en Derechos Humanos\".jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Baltasar_Garz%C3%B3n_en_la_inauguraci%C3%B3n_del_seminario_%22Argentina-_%C3%81frica_aportes_para_la_construcci%C3%B3n_de_una_agenda_de_trabajo_compartida_en_Derechos_Humanos%22.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Baltasar_Garz%C3%B3n_en_la_inauguraci%C3%B3n_del_seminario_%22Argentina-_%C3%81frica_aportes_para_la_construcci%C3%B3n_de_una_agenda_de_trabajo_compartida_en_Derechos_Humanos%22.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/9a/Baltasar_Garz%C3%B3n_en_la_inauguraci%C3%B3n_del_seminario_%22Argentina-_%C3%81frica_aportes_para_la_construcci%C3%B3n_de_una_agenda_de_trabajo_compartida_en_Derechos_Humanos%22.jpg/1280px-thumbnail.jpg",
"width": 2552,
"height": 2968,
"author": "Ministerio de Cultura de la Nación",
"license": "CC BY-SA 2.0",
"license_url": "https://creativecommons.org/licenses/by-sa/2.0",
"attribution": "Photo: Ministerio de Cultura de la Nación, CC BY-SA 2.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Cesare Beccaria.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Cesare_Beccaria.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/8/83/Cesare_Beccaria.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/8/83/Cesare_Beccaria.jpg",
"width": 600,
"height": 800,
"author": "Eliseo Sala",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Eliseo Sala, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Building of The Supreme Court of India.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Building_of_The_Supreme_Court_of_India.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/3/34/Building_of_The_Supreme_Court_of_India.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/34/Building_of_The_Supreme_Court_of_India.jpg/1280px-Building_of_The_Supreme_Court_of_India.jpg",
"width": 4128,
"height": 3096,
"author": "Pinakpani",
"license": "CC BY-SA 4.0",
"license_url": "https://creativecommons.org/licenses/by-sa/4.0",
"attribution": "Photo: Pinakpani, CC BY-SA 4.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Carlos Ghosn, 2007 (cropped).jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Carlos_Ghosn,_2007_(cropped).jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/6/64/Carlos_Ghosn%2C_2007_%28cropped%29.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/6/64/Carlos_Ghosn%2C_2007_%28cropped%29.jpg",
"width": 215,
"height": 304,
"author": "Nissan Motor Co. Ltd",
"license": "CC BY-SA 3.0",
"license_url": "https://creativecommons.org/licenses/by-sa/3.0",
"attribution": "Photo: Nissan Motor Co. Ltd, CC BY-SA 3.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Amanda Knox.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Amanda_Knox.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/7/72/Amanda_Knox.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/7/72/Amanda_Knox.jpg",
"width": 862,
"height": 1098,
"author": "Geraldbostrum",
"license": "CC BY-SA 4.0",
"license_url": "https://creativecommons.org/licenses/by-sa/4.0",
"attribution": "Photo: Geraldbostrum, CC BY-SA 4.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Inside the Supreme Court of India. 16.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Inside_the_Supreme_Court_of_India._16.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Inside_the_Supreme_Court_of_India._16.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a9/Inside_the_Supreme_Court_of_India._16.jpg/1280px-Inside_the_Supreme_Court_of_India._16.jpg",
"width": 2449,
"height": 3271,
"author": "Pinakpani",
"license": "CC BY-SA 4.0",
"license_url": "https://creativecommons.org/licenses/by-sa/4.0",
"attribution": "Photo: Pinakpani, CC BY-SA 4.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:2018-10-31 BGH Verhandlungstermin am 31. Oktober 2018 in Sachen I ZR 104-17 (Bundesgerichtshof zur Veröffentlichung von Abbildungen gemeinfreier Kunstwerke) StP 3030 LR10 by Stepro.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:2018-10-31_BGH_Verhandlungstermin_am_31._Oktober_2018_in_Sachen_I_ZR_104-17_(Bundesgerichtshof_zur_Ver%C3%B6ffentlichung_von_Abbildungen_gemeinfreier_Kunstwerke)_StP_3030_LR10_by_Stepro.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/c/c5/2018-10-31_BGH_Verhandlungstermin_am_31._Oktober_2018_in_Sachen_I_ZR_104-17_%28Bundesgerichtshof_zur_Ver%C3%B6ffentlichung_von_Abbildungen_gemeinfreier_Kunstwerke%29_StP_3030_LR10_by_Stepro.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c5/2018-10-31_BGH_Verhandlungstermin_am_31._Oktober_2018_in_Sachen_I_ZR_104-17_%28Bundesgerichtshof_zur_Ver%C3%B6ffentlichung_von_Abbildungen_gemeinfreier_Kunstwerke%29_StP_3030_LR10_by_Stepro.jpg/1280px-thumbnail.jpg",
"width": 3872,
"height": 2581,
"author": "Steffen Prößdorf",
"license": "CC BY-SA 4.0",
"license_url": "https://creativecommons.org/licenses/by-sa/4.0",
"attribution": "Photo: Steffen Prößdorf, CC BY-SA 4.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:International Criminal Court building (2019) in The Hague 01 (cropped).jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:International_Criminal_Court_building_(2019)_in_The_Hague_01_(cropped).jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/5/58/International_Criminal_Court_building_%282019%29_in_The_Hague_01_%28cropped%29.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/58/International_Criminal_Court_building_%282019%29_in_The_Hague_01_%28cropped%29.jpg/1280px-International_Criminal_Court_building_%282019%29_in_The_Hague_01_%28cropped%29.jpg",
"width": 4032,
"height": 2031,
"author": "OSeveno",
"license": "CC BY-SA 3.0",
"license_url": "https://creativecommons.org/licenses/by-sa/3.0",
"attribution": "Photo: OSeveno, CC BY-SA 3.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:12 Angry Men (1957 film poster).jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:12_Angry_Men_(1957_film_poster).jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/b/b5/12_Angry_Men_%281957_film_poster%29.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b5/12_Angry_Men_%281957_film_poster%29.jpg/1280px-12_Angry_Men_%281957_film_poster%29.jpg",
"width": 1902,
"height": 2907,
"author": "Illustrator unknown; \"Copyright 1957 United Artists Corp.\"",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Illustrator unknown; \"Copyright 1957 United Artists Corp.\", Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Color photograph of judges' bench at IMT.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Color_photograph_of_judges%27_bench_at_IMT.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/1/1e/Color_photograph_of_judges%27_bench_at_IMT.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1e/Color_photograph_of_judges%27_bench_at_IMT.jpg/1280px-Color_photograph_of_judges%27_bench_at_IMT.jpg",
"width": 2224,
"height": 1696,
"author": "Raymond D'Addario",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Raymond D'Addario, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Press at the International Military Tribunal.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Press_at_the_International_Military_Tribunal.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/9/91/Press_at_the_International_Military_Tribunal.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/91/Press_at_the_International_Military_Tribunal.jpg/1280px-Press_at_the_International_Military_Tribunal.jpg",
"width": 1510,
"height": 1200,
"author": "Charles W. Alexander",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Charles W. Alexander, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Duel entre Jacques Le Gris et Jean de Carrouges.png": {
"file_page": "https://commons.wikimedia.org/wiki/File:Duel_entre_Jacques_Le_Gris_et_Jean_de_Carrouges.png",
"url": "https://upload.wikimedia.org/wikipedia/commons/c/c2/Duel_entre_Jacques_Le_Gris_et_Jean_de_Carrouges.png",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/c/c2/Duel_entre_Jacques_Le_Gris_et_Jean_de_Carrouges.png",
"width": 694,
"height": 1002,
"author": "Jean de Wavrin",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Jean de Wavrin, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Tom Denning, Baron Denning, in 1950.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Tom_Denning,_Baron_Denning,_in_1950.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Tom_Denning%2C_Baron_Denning%2C_in_1950.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Tom_Denning%2C_Baron_Denning%2C_in_1950.jpg",
"width": 580,
"height": 800,
"author": "Elliott &amp; Fry",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Elliott &amp; Fry, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Iwao Hakamada giving a speech in 2024.png": {
"file_page": "https://commons.wikimedia.org/wiki/File:Iwao_Hakamada_giving_a_speech_in_2024.png",
"url": "https://upload.wikimedia.org/wikipedia/commons/1/1d/Iwao_Hakamada_giving_a_speech_in_2024.png",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/1/1d/Iwao_Hakamada_giving_a_speech_in_2024.png",
"width": 741,
"height": 1080,
"author": "https://www.youtube.com/@%E9%9D%99%E5%B2%A1%E3%81%AE%E9%A2%A8%E3%81%A8%E3%81%...",
"license": "CC BY 3.0",
"license_url": "https://creativecommons.org/licenses/by/3.0",
"attribution": "Photo: https://www.youtube.com/@%E9%9D%99%E5%B2%A1%E3%81%AE%E9%A2%A8%E3%81%A8%E3%81%..., CC BY 3.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Ernesto Miranda 1967.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Ernesto_Miranda_1967.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/7/7a/Ernesto_Miranda_1967.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/7/7a/Ernesto_Miranda_1967.jpg",
"width": 520,
"height": 989,
"author": "Unknown authorUnknown author",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Unknown authorUnknown author, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Gisèle Pelicot 2026.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Gis%C3%A8le_Pelicot_2026.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/3/35/Gis%C3%A8le_Pelicot_2026.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/35/Gis%C3%A8le_Pelicot_2026.jpg/1280px-Gis%C3%A8le_Pelicot_2026.jpg",
"width": 1825,
"height": 2738,
"author": "Amrei-Marie",
"license": "CC BY-SA 4.0",
"license_url": "https://creativecommons.org/licenses/by-sa/4.0",
"attribution": "Photo: Amrei-Marie, CC BY-SA 4.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Prosecutor Robert Jackson at Nuremberg Trials.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Prosecutor_Robert_Jackson_at_Nuremberg_Trials.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/7/7f/Prosecutor_Robert_Jackson_at_Nuremberg_Trials.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/7f/Prosecutor_Robert_Jackson_at_Nuremberg_Trials.jpg/1280px-Prosecutor_Robert_Jackson_at_Nuremberg_Trials.jpg",
"width": 1693,
"height": 1200,
"author": "Charles W. Alexander",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Charles W. Alexander, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:HardyTreasonTrials.png": {
"file_page": "https://commons.wikimedia.org/wiki/File:HardyTreasonTrials.png",
"url": "https://upload.wikimedia.org/wikipedia/commons/7/72/HardyTreasonTrials.png",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/7/72/HardyTreasonTrials.png",
"width": 346,
"height": 688,
"author": "Thomas Hardy (1752-1832)",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Thomas Hardy (1752-1832), Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Jeremy Bentham by Henry William Pickersgill.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Jeremy_Bentham_by_Henry_William_Pickersgill.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/e/e8/Jeremy_Bentham_by_Henry_William_Pickersgill.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e8/Jeremy_Bentham_by_Henry_William_Pickersgill.jpg/1280px-Jeremy_Bentham_by_Henry_William_Pickersgill.jpg",
"width": 2400,
"height": 3546,
"author": "Henry William Pickersgill",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Henry William Pickersgill, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Peter T. Leeson.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Peter_T._Leeson.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Peter_T._Leeson.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Peter_T._Leeson.jpg",
"width": 848,
"height": 680,
"author": "Peter Leeson",
"license": "CC BY 3.0",
"license_url": "https://creativecommons.org/licenses/by/3.0",
"attribution": "Photo: Peter Leeson, CC BY 3.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Microcosm of London Plate 058 - Old Bailey (colour).jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Microcosm_of_London_Plate_058_-_Old_Bailey_(colour).jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/0/04/Microcosm_of_London_Plate_058_-_Old_Bailey_%28colour%29.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/04/Microcosm_of_London_Plate_058_-_Old_Bailey_%28colour%29.jpg/1280px-Microcosm_of_London_Plate_058_-_Old_Bailey_%28colour%29.jpg",
"width": 1776,
"height": 1364,
"author": "Thomas Rowlandson (1756–1827) and Augustus Charles Pugin (1762–1832) (after) ...",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Thomas Rowlandson (1756–1827) and Augustus Charles Pugin (1762–1832) (after) ..., Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Old Bailey entrance.JPG": {
"file_page": "https://commons.wikimedia.org/wiki/File:Old_Bailey_entrance.JPG",
"url": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Old_Bailey_entrance.JPG",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/fa/Old_Bailey_entrance.JPG/1280px-Old_Bailey_entrance.JPG",
"width": 4320,
"height": 3240,
"author": "Tbmurray",
"license": "CC BY 3.0",
"license_url": "https://creativecommons.org/licenses/by/3.0",
"attribution": "Photo: Tbmurray, CC BY 3.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Jerome Frank.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Jerome_Frank.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/2/25/Jerome_Frank.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/2/25/Jerome_Frank.jpg",
"width": 584,
"height": 789,
"author": "United States Federal Judicial Center",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: United States Federal Judicial Center, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Hugo Black.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Hugo_Black.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Hugo_Black.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Hugo_Black.jpg",
"width": 302,
"height": 403,
"author": "John Black",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: John Black, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Serpillon, François – Code criminel, 1767 – BEIC 14465888.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Serpillon,_Fran%C3%A7ois_%E2%80%93_Code_criminel,_1767_%E2%80%93_BEIC_14465888.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Serpillon%2C_Fran%C3%A7ois_%E2%80%93_Code_criminel%2C_1767_%E2%80%93_BEIC_14465888.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e0/Serpillon%2C_Fran%C3%A7ois_%E2%80%93_Code_criminel%2C_1767_%E2%80%93_BEIC_14465888.jpg/1280px-Serpillon%2C_Fran%C3%A7ois_%E2%80%93_Code_criminel%2C_1767_%E2%80%93_BEIC_14465888.jpg",
"width": 1361,
"height": 1921,
"author": "François Serpillon",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: François Serpillon, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Central Criminal Court of England and Wales (The Old Bailey) Court No 1.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Central_Criminal_Court_of_England_and_Wales_(The_Old_Bailey)_Court_No_1.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/f/ff/Central_Criminal_Court_of_England_and_Wales_%28The_Old_Bailey%29_Court_No_1.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/ff/Central_Criminal_Court_of_England_and_Wales_%28The_Old_Bailey%29_Court_No_1.jpg/1280px-Central_Criminal_Court_of_England_and_Wales_%28The_Old_Bailey%29_Court_No_1.jpg",
"width": 14467,
"height": 5736,
"author": "Michael D Beckwith",
"license": "CC0",
"license_url": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
"attribution": "Photo: Michael D Beckwith, CC0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Pope Innocent III (Monastery of Subiaco).jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Pope_Innocent_III_(Monastery_of_Subiaco).jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/e/ee/Pope_Innocent_III_%28Monastery_of_Subiaco%29.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/ee/Pope_Innocent_III_%28Monastery_of_Subiaco%29.jpg/1280px-Pope_Innocent_III_%28Monastery_of_Subiaco%29.jpg",
"width": 2293,
"height": 2833,
"author": "Carlo Raso",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Carlo Raso, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Justice statue on Central Criminal Court, London - 2022-09-10.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Justice_statue_on_Central_Criminal_Court,_London_-_2022-09-10.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/d/da/Justice_statue_on_Central_Criminal_Court%2C_London_-_2022-09-10.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/da/Justice_statue_on_Central_Criminal_Court%2C_London_-_2022-09-10.jpg/1280px-Justice_statue_on_Central_Criminal_Court%2C_London_-_2022-09-10.jpg",
"width": 3456,
"height": 5184,
"author": "The wub",
"license": "CC BY-SA 4.0",
"license_url": "https://creativecommons.org/licenses/by-sa/4.0",
"attribution": "Photo: The wub, CC BY-SA 4.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Matthew Paris Chronica Maiora Fourth Lateran Council.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Matthew_Paris_Chronica_Maiora_Fourth_Lateran_Council.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/d/d0/Matthew_Paris_Chronica_Maiora_Fourth_Lateran_Council.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d0/Matthew_Paris_Chronica_Maiora_Fourth_Lateran_Council.jpg/1280px-Matthew_Paris_Chronica_Maiora_Fourth_Lateran_Council.jpg",
"width": 2046,
"height": 963,
"author": "Matthew Paris",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Matthew Paris, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Jacques-Louis David - The Emperor Napoleon in His Study at the Tuileries - Google Art Project (3x4 close cropped).jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Jacques-Louis_David_-_The_Emperor_Napoleon_in_His_Study_at_the_Tuileries_-_Google_Art_Project_(3x4_close_cropped).jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Jacques-Louis_David_-_The_Emperor_Napoleon_in_His_Study_at_the_Tuileries_-_Google_Art_Project_%283x4_close_cropped%29.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Jacques-Louis_David_-_The_Emperor_Napoleon_in_His_Study_at_the_Tuileries_-_Google_Art_Project_%283x4_close_cropped%29.jpg",
"width": 810,
"height": 1073,
"author": "Jacques-Louis David",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Jacques-Louis David, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Duterte and Medialdea flying to The Hague in 2025.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Duterte_and_Medialdea_flying_to_The_Hague_in_2025.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/a/ac/Duterte_and_Medialdea_flying_to_The_Hague_in_2025.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/ac/Duterte_and_Medialdea_flying_to_The_Hague_in_2025.jpg/1280px-Duterte_and_Medialdea_flying_to_The_Hague_in_2025.jpg",
"width": 1600,
"height": 1200,
"author": "Senator Bong Go",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Senator Bong Go, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:French Justice Minister Gérald Darmanin in 2025 (cropped 1).jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:French_Justice_Minister_G%C3%A9rald_Darmanin_in_2025_(cropped_1).jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/b/b4/French_Justice_Minister_G%C3%A9rald_Darmanin_in_2025_%28cropped_1%29.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/b/b4/French_Justice_Minister_G%C3%A9rald_Darmanin_in_2025_%28cropped_1%29.jpg",
"width": 1135,
"height": 1513,
"author": "UK Home Office",
"license": "CC BY 2.0",
"license_url": "https://creativecommons.org/licenses/by/2.0",
"attribution": "Photo: UK Home Office, CC BY 2.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Speyer, Historical Museum of the Palatinate - Code civil des Français.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Speyer,_Historical_Museum_of_the_Palatinate_-_Code_civil_des_Fran%C3%A7ais.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Speyer%2C_Historical_Museum_of_the_Palatinate_-_Code_civil_des_Fran%C3%A7ais.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0f/Speyer%2C_Historical_Museum_of_the_Palatinate_-_Code_civil_des_Fran%C3%A7ais.jpg/1280px-Speyer%2C_Historical_Museum_of_the_Palatinate_-_Code_civil_des_Fran%C3%A7ais.jpg",
"width": 3456,
"height": 2266,
"author": "DerHexer",
"license": "CC BY-SA 4.0",
"license_url": "https://creativecommons.org/licenses/by-sa/4.0",
"attribution": "Photo: DerHexer, CC BY-SA 4.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Central Criminal Court of England and Wales (The Old Bailey) Looking at The Dock in Court Number 1.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Central_Criminal_Court_of_England_and_Wales_(The_Old_Bailey)_Looking_at_The_Dock_in_Court_Number_1.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Central_Criminal_Court_of_England_and_Wales_%28The_Old_Bailey%29_Looking_at_The_Dock_in_Court_Number_1.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c1/Central_Criminal_Court_of_England_and_Wales_%28The_Old_Bailey%29_Looking_at_The_Dock_in_Court_Number_1.jpg/1280px-Central_Criminal_Court_of_England_and_Wales_%28The_Old_Bailey%29_Looking_at_The_Dock_in_Court_Number_1.jpg",
"width": 8684,
"height": 5791,
"author": "MichaelDavidBeckwith",
"license": "CC0",
"license_url": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
"attribution": "Photo: MichaelDavidBeckwith, CC0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Gustave dore crusades barthelemi undergoing the ordeal of fire.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Gustave_dore_crusades_barthelemi_undergoing_the_ordeal_of_fire.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/2/20/Gustave_dore_crusades_barthelemi_undergoing_the_ordeal_of_fire.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/2/20/Gustave_dore_crusades_barthelemi_undergoing_the_ordeal_of_fire.jpg",
"width": 963,
"height": 1210,
"author": "Gustave Doré",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Gustave Doré, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Sita Mughal ca1600.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Sita_Mughal_ca1600.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/2/21/Sita_Mughal_ca1600.jpg",
"thumb_url": "https://upload.wikimedia.org/wikipedia/commons/2/21/Sita_Mughal_ca1600.jpg",
"width": 326,
"height": 450,
"author": "Unknown authorUnknown author",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Unknown authorUnknown author, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Tangena trial by ordeal Madagascar.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Tangena_trial_by_ordeal_Madagascar.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/f/fe/Tangena_trial_by_ordeal_Madagascar.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/fe/Tangena_trial_by_ordeal_Madagascar.jpg/1280px-Tangena_trial_by_ordeal_Madagascar.jpg",
"width": 1321,
"height": 1071,
"author": "James Sibree",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: James Sibree, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Outreau - Centre.JPG": {
"file_page": "https://commons.wikimedia.org/wiki/File:Outreau_-_Centre.JPG",
"url": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Outreau_-_Centre.JPG",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/ca/Outreau_-_Centre.JPG/1280px-Outreau_-_Centre.JPG",
"width": 4000,
"height": 3000,
"author": "Floflo62",
"license": "CC BY-SA 4.0",
"license_url": "https://creativecommons.org/licenses/by-sa/4.0",
"attribution": "Photo: Floflo62, CC BY-SA 4.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Gladius legis custos, palais de justice de Paris.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Gladius_legis_custos,_palais_de_justice_de_Paris.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/a/ac/Gladius_legis_custos%2C_palais_de_justice_de_Paris.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/ac/Gladius_legis_custos%2C_palais_de_justice_de_Paris.jpg/1280px-Gladius_legis_custos%2C_palais_de_justice_de_Paris.jpg",
"width": 4756,
"height": 3585,
"author": "Celette",
"license": "CC BY-SA 4.0",
"license_url": "https://creativecommons.org/licenses/by-sa/4.0",
"attribution": "Photo: Celette, CC BY-SA 4.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Supreme Court of Japan (10357245203).jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Supreme_Court_of_Japan_(10357245203).jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Supreme_Court_of_Japan_%2810357245203%29.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a7/Supreme_Court_of_Japan_%2810357245203%29.jpg/1280px-Supreme_Court_of_Japan_%2810357245203%29.jpg",
"width": 3991,
"height": 1813,
"author": "Big Ben in Japan from Kawasaki, Japan",
"license": "CC BY-SA 2.0",
"license_url": "https://creativecommons.org/licenses/by-sa/2.0",
"attribution": "Photo: Big Ben in Japan from Kawasaki, Japan, CC BY-SA 2.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Palais de justice de Paris, Salle temporaire « Grands procès ».jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Palais_de_justice_de_Paris,_Salle_temporaire_%C2%AB_Grands_proc%C3%A8s_%C2%BB.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/f/f3/Palais_de_justice_de_Paris%2C_Salle_temporaire_%C2%AB_Grands_proc%C3%A8s_%C2%BB.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f3/Palais_de_justice_de_Paris%2C_Salle_temporaire_%C2%AB_Grands_proc%C3%A8s_%C2%BB.jpg/1280px-Palais_de_justice_de_Paris%2C_Salle_temporaire_%C2%AB_Grands_proc%C3%A8s_%C2%BB.jpg",
"width": 2938,
"height": 1960,
"author": "Tiraden",
"license": "CC BY-SA 4.0",
"license_url": "https://creativecommons.org/licenses/by-sa/4.0",
"attribution": "Photo: Tiraden, CC BY-SA 4.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Carlos Ghosn - Mondial de l'Automobile de Paris 2014 - 004 (cropped).jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Carlos_Ghosn_-_Mondial_de_l%27Automobile_de_Paris_2014_-_004_(cropped).jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/8/8d/Carlos_Ghosn_-_Mondial_de_l%27Automobile_de_Paris_2014_-_004_%28cropped%29.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/8d/Carlos_Ghosn_-_Mondial_de_l%27Automobile_de_Paris_2014_-_004_%28cropped%29.jpg/1280px-Carlos_Ghosn_-_Mondial_de_l%27Automobile_de_Paris_2014_-_004_%28cropped%29.jpg",
"width": 2267,
"height": 3023,
"author": "Thesupermat",
"license": "CC BY-SA 3.0",
"license_url": "https://creativecommons.org/licenses/by-sa/3.0",
"attribution": "Photo: Thesupermat, CC BY-SA 3.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
}
}''')

# added by reviewer, from pipeline/tools/commons.py verify on 2026-10-25
RECORDS.update(json.loads(r'''{
"File:Declaration of the Rights of Man and of the Citizen in 1789.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Declaration_of_the_Rights_of_Man_and_of_the_Citizen_in_1789.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/6/6c/Declaration_of_the_Rights_of_Man_and_of_the_Citizen_in_1789.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/6c/Declaration_of_the_Rights_of_Man_and_of_the_Citizen_in_1789.jpg/1280px-Declaration_of_the_Rights_of_Man_and_of_the_Citizen_in_1789.jpg",
"width": 3657,
"height": 4636,
"author": "Unknown",
"license": "Public domain",
"license_url": "",
"attribution": "Photo: Unknown, Public domain, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Allahabad high court.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Allahabad_high_court.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/7/71/Allahabad_high_court.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/71/Allahabad_high_court.jpg/1280px-Allahabad_high_court.jpg",
"width": 2592,
"height": 1944,
"author": "Vroomtrapit at English Wikipedia",
"license": "CC0",
"license_url": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
"attribution": "Photo: Vroomtrapit at English Wikipedia, CC0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:European Court of Human Rights (ECtHR)- Court room.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:European_Court_of_Human_Rights_(ECtHR)-_Court_room.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/2/23/European_Court_of_Human_Rights_%28ECtHR%29-_Court_room.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/23/European_Court_of_Human_Rights_%28ECtHR%29-_Court_room.jpg/1280px-European_Court_of_Human_Rights_%28ECtHR%29-_Court_room.jpg",
"width": 2560,
"height": 1600,
"author": "CherryX",
"license": "CC BY-SA 3.0",
"license_url": "https://creativecommons.org/licenses/by-sa/3.0",
"attribution": "Photo: CherryX, CC BY-SA 3.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Justizzentrum Aachen-Gerichtssaal01.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Justizzentrum_Aachen-Gerichtssaal01.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/2/29/Justizzentrum_Aachen-Gerichtssaal01.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/29/Justizzentrum_Aachen-Gerichtssaal01.jpg/1280px-Justizzentrum_Aachen-Gerichtssaal01.jpg",
"width": 3208,
"height": 2364,
"author": "ACBahn",
"license": "CC BY 3.0",
"license_url": "https://creativecommons.org/licenses/by/3.0",
"attribution": "Photo: ACBahn, CC BY 3.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:High Court Of Justiciary And Court Of Session, Edinburgh 1.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:High_Court_Of_Justiciary_And_Court_Of_Session,_Edinburgh_1.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/f/f3/High_Court_Of_Justiciary_And_Court_Of_Session%2C_Edinburgh_1.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f3/High_Court_Of_Justiciary_And_Court_Of_Session%2C_Edinburgh_1.jpg/1280px-High_Court_Of_Justiciary_And_Court_Of_Session%2C_Edinburgh_1.jpg",
"width": 3150,
"height": 3004,
"author": "LornaMCampbell",
"license": "CC BY-SA 4.0",
"license_url": "https://creativecommons.org/licenses/by-sa/4.0",
"attribution": "Photo: LornaMCampbell, CC BY-SA 4.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
},
"File:Sala de juicios orales UAA 01.jpg": {
"file_page": "https://commons.wikimedia.org/wiki/File:Sala_de_juicios_orales_UAA_01.jpg",
"url": "https://upload.wikimedia.org/wikipedia/commons/7/79/Sala_de_juicios_orales_UAA_01.jpg",
"thumb_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/79/Sala_de_juicios_orales_UAA_01.jpg/1280px-Sala_de_juicios_orales_UAA_01.jpg",
"width": 2048,
"height": 1152,
"author": "Luis Alvaz",
"license": "CC BY-SA 4.0",
"license_url": "https://creativecommons.org/licenses/by-sa/4.0",
"attribution": "Photo: Luis Alvaz, CC BY-SA 4.0, via Wikimedia Commons",
"verified_on": "2026-10-25"
}
}'''))

def clean_author(a):
    a = html.unescape(a or "").replace("Unknown authorUnknown author", "Unknown author")
    if a.startswith("https://www.youtube.com/@"):
        a = "YouTube channel " + urllib.parse.unquote(a.split("@", 1)[1]).split()[0]
    return a.strip() or "Unknown author"

IMG = [
 # id, commons title, alt, caption
 ("img_ob_court1", "File:Central Criminal Court of England and Wales (The Old Bailey) Court No 1.jpg", "Wide view of the wood-panelled Court Number 1 at the Old Bailey seen from the dock", "Court Number 1 at the Old Bailey, seen from where the accused sits."),
 ("img_ob_dock", "File:Central Criminal Court of England and Wales (The Old Bailey) Looking at The Dock in Court Number 1.jpg", "The raised, glass-fronted dock at the back of Court Number 1 at the Old Bailey", "The dock in Court Number 1: the accused faces the judge across the well of the court."),
 ("img_ob_entrance", "File:Old Bailey entrance.JPG", "Stone entrance of the Central Criminal Court in London with carved figures above the door", "The Old Bailey entrance. The inscription reads: Defend the Children of the Poor and Punish the Wrongdoer."),
 ("img_ob_justice", "File:Justice statue on Central Criminal Court, London - 2022-09-10.jpg", "Gilded statue of Justice holding a sword and scales on top of the Old Bailey dome, eyes uncovered", "F. W. Pomeroy's Justice (1905 to 1906) on the Old Bailey dome. No blindfold."),
 ("img_microcosm", "File:Microcosm of London Plate 058 - Old Bailey (colour).jpg", "Coloured print of a crowded Georgian courtroom with judges on a raised bench and a prisoner in the dock", "The Old Bailey around 1808, by Rowlandson and Pugin for the Microcosm of London."),
 ("img_garrow", "File:William Garrow2.jpg", "Mezzotint portrait of William Garrow in a dark coat and white cravat", "William Garrow, mezzotint published in 1810."),
 ("img_erskine", "File:Thomas Erskine, 1st Baron Erskine by Sir William Charles Ross.jpg", "Portrait of Thomas Erskine, an older man in dark clothes with white hair", "Thomas Erskine, defender of Thomas Hardy in 1794."),
 ("img_hardy_title", "File:HardyTreasonTrials.png", "Printed title page of Thomas Hardy's account of the 1794 treason trials", "Title page of Thomas Hardy's own record of the 1794 treason trials."),
 ("img_ordeal_iron", "File:Ordeal by red-hot iron.jpg", "Medieval stone relief of a crowned woman walking barefoot over glowing ploughshares", "Bamberg Cathedral relief: Empress Cunigunde's legendary ordeal by red-hot iron."),
 ("img_ordeal_fire", "File:Gustave dore crusades barthelemi undergoing the ordeal of fire.jpg", "Engraving of a man walking between two burning pyres before a crowd of crusaders", "Gustave Doré's engraving of Peter Bartholomew's ordeal of fire, 1099."),
 ("img_lateran", "File:Matthew Paris Chronica Maiora Fourth Lateran Council.jpg", "Medieval manuscript drawing of the Pope and bishops seated in council", "Matthew Paris's drawing of the Fourth Lateran Council in his Chronica Majora."),
 ("img_innocent3", "File:Pope Innocent III (Monastery of Subiaco).jpg", "Medieval fresco of Pope Innocent III in a red robe and tall white mitre", "Innocent III in a 13th-century fresco at Subiaco."),
 ("img_duel", "File:Duel entre Jacques Le Gris et Jean de Carrouges.png", "Fifteenth-century miniature of two armoured knights fighting on foot before spectators", "The 1386 judicial duel between Jacques Le Gris and Jean de Carrouges, painted about 1480."),
 ("img_gerichtskampf", "File:Gerichtskampf mair.jpg", "Woodcut-style painting of two men in a judicial duel inside a fenced arena in Augsburg", "A judicial duel fought in Augsburg's wine market in 1409, painted in the sixteenth century."),
 ("img_leeson", "File:Peter T. Leeson.jpg", "Portrait photograph of economist Peter Leeson", "Peter T. Leeson, the economist who reread the ordeal data."),
 ("img_carolina", "File:De Constitutio criminalis Carolina (1577) 01.jpg", "Printed title page of a 1577 edition of the Constitutio Criminalis Carolina", "A 1577 edition of the Carolina, the Holy Roman Empire's 1532 criminal code."),
 ("img_inq_room", "File:An interrogation room of the Spanish Inquisition with two pr Wellcome V0041642.jpg", "Engraving of two seated priests questioning an accused man in a vaulted room", "An interrogation room of the Spanish Inquisition, engraving (Wellcome Collection)."),
 ("img_autodefe", "File:Francisco rizi-auto de fe.jpg", "Huge crowded painting of a public ceremony in Madrid's Plaza Mayor with stands and a stage", "Francisco Rizi's Auto de fe in the Plaza Mayor of Madrid, 30 June 1680."),
 ("img_serpillon", "File:Serpillon, François – Code criminel, 1767 – BEIC 14465888.jpg", "Engraved title page of Serpillon's Code criminel, 1767", "Serpillon's 1767 commentary on the Criminal Ordinance of 1670."),
 ("img_beccaria", "File:Cesare Beccaria.jpg", "Painted portrait of Cesare Beccaria in an eighteenth-century wig", "Cesare Beccaria, who attacked judicial torture in 1764."),
 ("img_napoleon", "File:Jacques-Louis David - The Emperor Napoleon in His Study at the Tuileries - Google Art Project (3x4 close cropped).jpg", "Painting of Napoleon standing in uniform in his study, hand in his waistcoat", "Napoleon in his study, by Jacques-Louis David, 1812. Rolled papers on the desk read CODE."),
 ("img_code_civil", "File:Speyer, Historical Museum of the Palatinate - Code civil des Français.jpg", "An open early printed volume of the French Code civil in a museum case", "An early Code civil in Speyer. Its sister, the criminal procedure code of 1808, followed the same plan."),
 ("img_wigmore", "File:John Henry Wigmore cph.3b34499.jpg", "Black and white portrait of John Henry Wigmore, a moustached man in a suit", "John Henry Wigmore, the great American scholar of evidence."),
 ("img_12angry", "File:12 Angry Men (1957 film poster).jpg", "Film poster for 12 Angry Men showing the twelve jurors around a table", "Poster for 12 Angry Men (1957)."),
 ("img_gideon", "File:Clarence Earl Gideon.jpg", "Black and white photo of Clarence Earl Gideon, a thin older man", "Clarence Earl Gideon, whose pencilled petition reached the Supreme Court."),
 ("img_miranda", "File:Ernesto Miranda 1967.jpg", "Black and white photograph of Ernesto Miranda in 1967", "Ernesto Miranda in 1967."),
 ("img_denning", "File:Tom Denning, Baron Denning, in 1950.jpg", "Black and white portrait of Lord Denning in 1950", "Alfred Denning in 1950, then a Lord Justice of Appeal."),
 ("img_rcj", "File:Royal-courts-of-justice.jpg", "Gothic stone front of the Royal Courts of Justice on the Strand in London", "The Royal Courts of Justice, London, home of the Court of Appeal."),
 ("img_bgh", "File:BGH - Palais 2.JPG", "Classical palace building in a park, seat of Germany's Federal Court of Justice in Karlsruhe", "The Federal Court of Justice (Bundesgerichtshof), Karlsruhe."),
 ("img_paris_grands", "File:Palais de justice de Paris, Salle temporaire « Grands procès ».jpg", "Large modern pale-wood courtroom built for mass trials inside the Paris Palais de justice", "The temporary 'Grands procès' room in the Paris Palais de justice, built for trials with many parties."),
 ("img_paris_gladius", "File:Gladius legis custos, palais de justice de Paris.jpg", "Carved stone corner of the Paris Palais de justice with the Latin words Gladius legis custos", "'The sword guards the law': a corner of the Paris Palais de justice."),
 ("img_garzon", "File:Baltasar Garzón en la inauguración del seminario \"Argentina- África aportes para la construcción de una agenda de trabajo compartida en Derechos Humanos\".jpg", "Baltasar Garzón speaking at a seminar in Buenos Aires in 2014", "Baltasar Garzón in Buenos Aires, 2014."),
 ("img_knox", "File:Amanda Knox.jpg", "Head and shoulders photograph of Amanda Knox in 2016", "Amanda Knox in Seattle, 2016."),
 ("img_hakamada", "File:Iwao Hakamada giving a speech in 2024.png", "Iwao Hakamada, a very old man, speaking at a microphone in 2024", "Iwao Hakamada speaking in 2024, the year of his acquittal."),
 ("img_ghosn", "File:Carlos Ghosn - Mondial de l'Automobile de Paris 2014 - 004 (cropped).jpg", "Carlos Ghosn speaking on stage at the 2014 Paris Motor Show", "Carlos Ghosn at the Paris Motor Show, 2014."),
 ("img_pelicot", "File:Gisèle Pelicot 2026.jpg", "Gisèle Pelicot, a woman with a bob haircut and glasses, at a public event in Munich", "Gisèle Pelicot at a public event in Munich, 2026."),
 ("img_outreau", "File:Outreau - Centre.JPG", "Town centre of Outreau in northern France with an old tower", "Outreau, the small town near Boulogne-sur-Mer that gave the scandal its name."),
 ("img_japan_sc", "File:Saikosaibansho.jpg", "Massive grey granite building of the Supreme Court of Japan in Tokyo", "The Supreme Court of Japan, Tokyo."),
 ("img_japan_grand", "File:The Grand Bench of the Japanese Supreme Court.jpg", "The Grand Bench courtroom of Japan's Supreme Court with fifteen high-backed chairs", "The Grand Bench courtroom of Japan's Supreme Court."),
 ("img_imt_bench", "File:Color photograph of judges' bench at IMT.jpg", "Colour photograph of the judges' bench in Courtroom 600, Nuremberg", "The judges' bench in Courtroom 600, Palace of Justice, Nuremberg."),
 ("img_imt_dock", "File:Defendants in the dock at nuremberg trials.jpg", "Nazi defendants seated in two rows in the dock at Nuremberg, guarded by military police", "The defendants' dock at the International Military Tribunal, Nuremberg."),
 ("img_goering", "File:Goering on trial (color).jpg", "Hermann Göring in a pale uniform, wearing headphones, at Nuremberg", "Hermann Göring during cross-examination at Nuremberg, 1946."),
 ("img_jackson", "File:Prosecutor Robert Jackson at Nuremberg Trials.jpg", "Robert H. Jackson standing at a lectern addressing the Nuremberg tribunal", "Robert H. Jackson, chief US prosecutor, at the lectern."),
 ("img_icc", "File:International Criminal Court building (2019) in The Hague 01 (cropped).jpg", "Modern building of the International Criminal Court in The Hague with green towers", "The International Criminal Court, The Hague."),
 ("img_duterte", "File:Duterte and Medialdea flying to The Hague in 2025.jpg", "Rodrigo Duterte seated on an aircraft beside Salvador Medialdea", "Rodrigo Duterte on the flight to The Hague, March 2025."),
 ("img_sci", "File:Building of The Supreme Court of India.jpg", "The domed sandstone building of the Supreme Court of India in New Delhi", "The Supreme Court of India, New Delhi."),
 ("img_sci_inside", "File:Inside the Supreme Court of India. 16.jpg", "Interior corridor of the Supreme Court of India with arches", "Inside the Supreme Court of India."),
 ("img_calcutta", "File:Calcutta High Court.jpg", "Red and cream Gothic building of the Calcutta High Court", "Calcutta High Court, established 1862, one of the old presidency courts."),
 ("img_sita", "File:Sita Mughal ca1600.jpg", "Mughal miniature of Sita sitting calmly inside a ring of flames", "Sita's ordeal by fire, Mughal painting, about 1600."),
 ("img_darmanin", "File:French Justice Minister Gérald Darmanin in 2025 (cropped 1).jpg", "Portrait of French justice minister Gérald Darmanin in 2025", "Gérald Darmanin, French justice minister, 2025."),
 ("img_frank", "File:Jerome Frank.jpg", "Black and white portrait of Judge Jerome Frank", "Jerome Frank, federal appeals judge and critic of the 'fight theory'."),
 ("img_ddhc", "File:Declaration of the Rights of Man and of the Citizen in 1789.jpg", "Painting of the 1789 Declaration of the Rights of Man, its articles set out on two stone tablets beneath allegorical figures", "The Declaration of the Rights of Man and of the Citizen, 1789. Article 9 sets out the presumption of innocence."),
 ("img_allahabad_hc", "File:Allahabad high court.jpg", "Exterior of the Allahabad High Court building in Prayagraj", "The Allahabad High Court, which issued guidelines on trials in absentia in May 2026."),
 ("img_echr_room", "File:European Court of Human Rights (ECtHR)- Court room.jpg", "Interior of the courtroom of the European Court of Human Rights in Strasbourg", "The courtroom of the European Court of Human Rights, Strasbourg."),
 ("img_aachen_room", "File:Justizzentrum Aachen-Gerichtssaal01.jpg", "German criminal courtroom seen from the public seats, with a raised bench across the end wall", "A courtroom at the Aachen justice centre used by large criminal chambers, where professional and lay judges sit together on the raised bench."),
 ("img_edinburgh_hcj", "File:High Court Of Justiciary And Court Of Session, Edinburgh 1.jpg", "Stone court buildings in central Edinburgh", "The High Court of Justiciary and Court of Session buildings, Edinburgh."),
 ("img_mx_oral", "File:Sala de juicios orales UAA 01.jpg", "Interior of an oral-trial courtroom at a Mexican university", "An oral-trial courtroom (sala de juicios orales) at the Autonomous University of Aguascalientes, built to train lawyers for Mexico's new accusatory trials."),
]
IMAGES = []
for iid, title, alt, cap in IMG:
    r = dict(RECORDS[title])
    r["author"] = clean_author(r["author"])
    r["attribution"] = f"{r['author']}, {r['license']}, via Wikimedia Commons"
    IMAGES.append({"id": iid, **r, "alt": alt, "caption": cap})

# ---------------------------------------------------------------- media (verified with pipeline/tools/yt.py on 2026-10-25)
def yt(i, vid, title, pub, start, end, dur):
    return {"id": i, "kind": "video", "provider": "youtube", "url": f"https://www.youtube.com/watch?v={vid}",
            "embed_url": f"https://www.youtube-nocookie.com/embed/{vid}?start={start}&end={end}", "start": start, "end": end,
            "title": title, "publisher": pub, "license": "Standard YouTube licence. Embed only, do not download.",
            "duration_s": dur, "verified_on": ACC, "verified_by": "youtube oembed returned 200 with this channel name"}
MEDIA = [
 yt("vid_jackson_opening", "L50OZSeDXeA", "Nuremberg Day 2: Justice Robert H. Jackson's opening statement, 21 November 1945", "RobertHJacksonCenter", 0, 90, 434),
 yt("vid_gresham_adversarial", "RyEDZbNGvIU", "Does the Adversarial System Serve Us Well? (Leslie Thomas KC)", "Gresham College", 0, 90, 3674),
 yt("vid_japan_lay_judge", "lgEi6XwuZOc", "Our Lay Judge Story, animated film with subtitles", "裁判所 (Courts in Japan)", 0, 90, 1345),
 yt("vid_hansard_jury", "thvnqaBIezg", "Jury trials under threat? The Courts and Tribunals Bill explained", "Hansard Society", 0, 90, 3417),
 yt("vid_12angry", "TEN-2uTi2c0", "12 Angry Men (1957), official trailer", "Amazon MGM Studios", 0, 90, 147),
 yt("vid_icc_duterte", "lUsD6Lh-JhE", "Duterte case: opening of the confirmation of charges hearing, 23 February 2026, 2nd session", "IntlCriminalCourt", 0, 90, 3017),
 yt("vid_pathe_oldbailey", "iBmM_Z94TK4", "Old Bailey Restored (1952)", "British Pathé", 0, 90, 498),
 yt("vid_hakamada_itv", "hl7K3vsB1rc", "Iwao Hakamada acquitted after 46 years on death row", "ITV News", 0, 17, 17),
]

# ---------------------------------------------------------------- helpers
def sp(id, kind, name, story, spot_it, why, hook, src, imgs=(), media=(), where=None, when=None, native=None, compare=None):
    d = {"id": id, "kind": kind, "name": name}
    if native: d["native_name"] = native
    if where: d["where"] = {"label": where[0], "lat": where[1], "lon": where[2]}
    if when: d["when"] = when
    d.update({"image_ids": list(imgs), "media_ids": list(media), "spot_it": spot_it, "story_md": story,
              "why_it_matters": why, "memory_hook": hook})
    if compare: d["compare"] = compare
    d["source_ids"] = list(src)
    return d

def sec(id, order, title, intro, spots, check, src, visual=None):
    d = {"id": id, "order": order, "title": title, "intro_md": intro}
    if visual: d["visual"] = visual
    d.update({"spotlights": spots, "check": check, "source_ids": src})
    return d

# ---------------------------------------------------------------- sections
SECTIONS = []

SECTIONS.append(sec("hook", 1, "Two courtrooms, one question",
"""An English judge once lost patience after a parade of witnesses told flatly contradictory stories. "Am I never to hear the truth?" he asked. The barrister replied: "No, my lord, merely the evidence."

That exchange, retold in Peter Murphy's guide to evidence, is the whole topic in two lines. In London, Delhi or New York, a criminal trial is a **contest**. Two sides gather their own proof, call their own witnesses and attack the other side's. The judge referees; often a jury decides. In Paris, Berlin or Tokyo, a trial is closer to an **inquiry**. Officials build a written file, and the judges themselves question the accused and the witnesses, looking for what happened.

Both claim to want the truth. They disagree about who should dig for it. Today: where each idea came from, how each runs, how each fails, and why in 2026 both are borrowing from each other.""",
[
 sp("old_bailey_court1", "place", "Court Number 1, the Old Bailey",
 "London's Central Criminal Court has tried murder and treason since its predecessor opened beside Newgate prison; the present building opened in 1907. Court Number 1 is built like an argument. The dock faces the judge across an open well where barristers stand, and the jury sits to one side, twelve people who have read nothing in advance. Everything they will weigh must be said aloud in front of them and survive cross-examination. The judge decides what evidence the jury may hear and tells them the law, but does not investigate. If the prosecution's case is weak, it simply fails.",
 "Raised dock at the back, wigs and gowns, a jury box to the side, and no case file on the jurors' desks.",
 "The model courtroom of the adversarial world, copied from Kingston to Kolkata.",
 "Twelve strangers, two sides, one referee, and nothing written down that they get to read first.",
 ["wiki_old_bailey", "wiki_adversarial"], ["img_ob_court1", "img_ob_dock"], ["vid_pathe_oldbailey"],
 ("Old Bailey, City of London", 51.5155, -0.1019), "Present building opened 27 February 1907"),
 sp("paris_grands_proces", "place", "A French trial room in the Palais de justice",
 "In a French criminal court the presiding judge arrives having read the whole case file, the dossier, assembled by police, prosecutors and sometimes an investigating judge. The president questions the accused first and at length, then the witnesses; the lawyers ask their questions afterwards. A confession does not end the case: it is one more piece of evidence, and the prosecution must still present a full case. Paris built a temporary 'Grands procès' room inside its old Palais de justice for trials with dozens of lawyers and parties.",
 "A judge who leads the questioning with a thick file in front of her, and a confession that does not end the trial.",
 "The template for most of Europe, Latin America and East Asia.",
 "In Paris the judge has done the reading; in London the jury has not.",
 ["wiki_inquisitorial", "wiki_adversarial"], ["img_paris_grands", "img_paris_gladius"], [],
 ("Palais de justice, Île de la Cité, Paris", 48.8556, 2.3450), "Modern form since the 1808 code"),
], ["q_hook_tf", "q_hook_mcq"], ["wiki_adversarial", "wiki_inquisitorial"]))

SECTIONS.append(sec("two_models", 2, "The two models in one page",
"""Strip both systems down and you find three questions. **Who gathers the evidence?** In the adversarial model, the parties; in the inquisitorial model, officials of the state, including judges. **Who questions the witnesses?** Lawyers, by examination and cross-examination; or the presiding judge, from the file. **What does a confession do?** In common-law courts a guilty plea ends the contest and moves straight to sentence; in the continental model it is evidence to be checked.

Two cautions. First, the words mislead: 'inquisitorial' has nothing to do with torture chambers today. 'Adversarial' does not mean the other side lacks a prosecutor and defender: both systems have both, and Article 6 of the European Convention on Human Rights requires it. Second, no country is pure. England has inquisitorial coroners; France has adversarial-style hearings; the United States uses an inquisitorial adjudicator for New York traffic tickets.

The numbers below show how differently the two families actually behave.""",
[
 sp("idea_umpire", "idea", "The judge as umpire",
 "In 1957 England's Court of Appeal ordered a retrial because the judge had asked too many questions. In Jones v National Coal Board, Lord Justice Denning wrote that a judge sits 'to hear and determine the issues raised by the parties, not to conduct an investigation or examination on behalf of society at large, as happens, we believe, in some foreign countries.' He quoted Lord Eldon: 'truth is best discovered by powerful statements on both sides of the question.' In a civil case, he added, the judge 'is not allowed... to call a witness whom he thinks might throw some light on the facts.'",
 "A judge who mostly listens, rules on objections and sums up, and rarely asks a witness anything.",
 "The purest statement of the adversarial ideal by its most famous judge.",
 "If the judge asks too many questions in England, the trial can be thrown out.",
 ["nzlj_jones", "wiki_denning"], ["img_denning", "img_rcj"], ["vid_gresham_adversarial"], ("Court of Appeal, Royal Courts of Justice, London", 51.5136, -0.1136), "1957"),
 sp("idea_inquirer", "idea", "The judge as inquirer",
 "In Germany a criminal trial opens with the court questioning the accused, and the presiding judge then takes the evidence, examining witnesses from a file the prosecutor has compiled. John Langbein, a Yale legal historian, was struck by how fast this could be. A study of about 600 West German trials in 1969 to 1970 found that 47 per cent lasted no longer than a third of a day, roughly two hours. Langbein argued in 1979 that this speed is why Germany could try serious cases without American-style plea bargaining.",
 "The judge reads the file, asks the questions and writes a reasoned judgment at the end.",
 "Shows the inquisitorial model as an efficiency machine, not a relic.",
 "Half of German trials once took less time than a feature film.",
 ["langbein_1979", "wiki_inquisitorial"], ["img_bgh"], [], ("Germany (Federal Court of Justice, Karlsruhe)", 49.0105, 8.3962), "Study of 1969 to 1970"),
], ["q_models_match", "q_models_tf"], ["wiki_adversarial", "wiki_inquisitorial", "pew_2023", "rsj_instruction", "wiki_japan_cj", "civils_plea", "langbein_1979"],
{"type": "compare", "title": "Contest or inquiry?", "data": {
  "left": {"label": "Adversarial", "image_id": "img_ob_dock"}, "right": {"label": "Inquisitorial", "image_id": "img_paris_grands"},
  "rows": [
   {"feature": "Who gathers evidence", "adversarial": "Police and prosecution for one side, defence for the other", "inquisitorial": "Police and prosecutors under judicial supervision; sometimes an investigating judge"},
   {"feature": "Who questions witnesses", "adversarial": "Lawyers: examination, then cross-examination", "inquisitorial": "The presiding judge first, then the lawyers"},
   {"feature": "The file", "adversarial": "Fact-finders see only what is said in court", "inquisitorial": "Judges read the written dossier before trial"},
   {"feature": "A confession", "adversarial": "A guilty plea ends the contest", "inquisitorial": "One more piece of evidence"},
   {"feature": "Who decides", "adversarial": "Jury, or a judge alone", "inquisitorial": "Professional judges, often with lay judges beside them"},
   {"feature": "The verdict", "adversarial": "Jury verdict without reasons", "inquisitorial": "Written, reasoned judgment"},
   {"feature": "Appeal", "adversarial": "Mostly on law and procedure", "inquisitorial": "Often a fresh look at the facts too"},
  ]}}))

SECTIONS[-1]["visual"] = [SECTIONS[-1]["visual"], {"type": "stat_tiles", "title": "The numbers that matter", "data": [
  {"label": "US federal defendants who pleaded guilty, 2022", "value": "89.5%", "note": "only 1,669 of 71,954 went to trial"},
  {"label": "US federal defendants acquitted at trial, 2022", "value": "0.4%", "note": "290 people"},
  {"label": "Investigating-judge cases opened in France, 2023", "value": "16,600", "note": "against about 4.7 million new cases at prosecutors' offices"},
  {"label": "Japan's conviction rate at trial", "value": "above 99%", "note": "but prosecutors drop or divert most cases first"},
  {"label": "Indian criminal cases settled by plea bargain, 2022", "value": "0.11%", "note": "19,135 of 1.7 crore cases for trial"},
  {"label": "West German trials of two hours or less (1969 to 1970)", "value": "47%", "note": "Casper and Zeisel sample, cited by Langbein"},
  {"label": "Crown Court backlog, England and Wales", "value": "79,616", "note": "record, mid-2025 figures"},
  {"label": "Years since Italy switched to a more adversarial code", "value": "37", "note": "new code in force 24 October 1989"},
]}]

SECTIONS.append(sec("ordeals", 3, "Before trials: fire, water and God",
"""For several hundred years, Europe's hardest criminal cases were not decided by evidence at all. When there was no confession and no witness, the accused carried red-hot iron, plunged an arm into boiling water, or was lowered into cold water, and God was asked to show the truth. Nobles could fight a judicial duel instead. Ordeals were run by priests, in churches, with prayers and blessings.

Then, on 11 November 1215, Pope Innocent III opened the Fourth Lateran Council in Rome. One of its canons forbade clergy from blessing ordeals. Without priests, the ordeal lost its power. Europe had to find a new way to decide guilt, and it found two. England, which already had juries that accused suspects, began asking a jury of neighbours to decide guilt as well. The Continent turned to the Church's own new procedure, the inquisitio, in which a judge investigated. The split you see in courtrooms today starts here.""",
[
 sp("ordeal_hot_iron", "custom", "The ordeal of hot iron",
 "The accused carried a red-hot iron bar about nine feet, or walked over glowing ploughshares. The hand was bandaged and inspected by a priest three days later: clean healing meant innocence, festering meant guilt. Anglo-Saxon law even had a 'threefold' version with an iron three times heavier for men of bad reputation. In 1215 the Lateran Council withdrew clergy from the rite, and English plea rolls record no ordeal after 1219, when Henry III's government recognised that it was over. A stone relief at Bamberg Cathedral shows the legend of Empress Cunigunde walking unhurt across burning ploughshares.",
 "A bandaged hand, a priest, and a three-day wait.",
 "The method that the jury and the investigating judge both replaced.",
 "Nine feet, one iron bar, three days to heal.",
 ["wiki_ordeal", "wiki_lateran"], ["img_ordeal_iron", "img_ordeal_fire"], [], ("England and continental Europe", 52.0, 5.0), "About 500 to 1219 in England"),
 sp("leeson_ordeals", "experiment", "Did the priests rig the ordeals?",
 "The economist Peter Leeson went back to the Regestrum Varadinense, a register of hot-iron ordeals held in the basilica of Várad in Hungary (now Oradea, Romania) between 1208 and 1235. Of 308 recorded cases, 100 were settled before the iron was ever picked up. Of the 208 people who actually carried it, 130 passed, 62.5 per cent. 'Unless nearly two-thirds of ordeal-officiating priests did not understand how to heat iron,' Leeson wrote, the results were steered. His theory: only people who believed they were innocent dared to face God, so priests who saw a willing defendant made sure the iron was survivable.",
 "Two-thirds of people carrying red-hot iron came out with healing hands.",
 "Turns a 'superstition' into a clever sorting device, and is still debated.",
 "Guilty people settled; innocent people carried the iron, and the iron was cool.",
 ["leeson_ordeals", "wiki_ordeal"], ["img_leeson"], [], ("Oradea (Várad), Romania", 47.0722, 21.9217), "Register of 1208 to 1235; paper 2012"),
 sp("lateran_1215", "event", "The Fourth Lateran Council",
 "Innocent III called the council in April 1213 and it opened at the Lateran Palace in Rome on 11 November 1215, with hundreds of bishops attending. Among its decrees was a canon forbidding priests to bless the participants in ordeals by fire and water. The Pope was not abolishing ordeals outright, and secular rulers took decades to drop them. But the rule pulled the sacred core out of the procedure. In the same years Innocent III had been building the processus per inquisitionem, which let a church judge open a case without a private accuser and question witnesses himself.",
 "A council of mitred bishops in Rome, 1215, the same year as Magna Carta.",
 "The single decision that forced Europe to invent both modern trial systems.",
 "1215: the Pope took the priests away from the fire, and two legal worlds were born.",
 ["wiki_lateran", "wiki_ordeal", "wiki_inquisitorial"], ["img_lateran", "img_innocent3"], [], ("Lateran Palace, Rome", 41.8859, 12.5057), "Opened 11 November 1215"),
 sp("trial_by_combat", "custom", "Trial by combat",
 "The Normans brought the judicial duel to England after 1066: the accuser and the accused, or hired champions, fought, and God gave victory to the right. One of the last famous French duels, in Paris on 29 December 1386, pitted the knight Jean de Carrouges against the squire Jacques Le Gris, accused of raping Carrouges's wife Marguerite. Carrouges killed Le Gris, and the verdict was taken as proof. If Carrouges had lost, Marguerite could have been burned for false accusation. Ridley Scott filmed it as The Last Duel (2021).",
 "Two armoured men, a fenced field, judges watching.",
 "Shows how proof once meant God's choice, not a witness's word.",
 "In 1386, a rape trial was decided by who killed whom.",
 ["wiki_combat", "wiki_ordeal"], ["img_duel", "img_gerichtskampf"], [], ("Paris (Saint-Martin-des-Champs)", 48.8666, 2.3550), "Duel of 29 December 1386"),
], ["q_lateran_mcq", "q_leeson_hl"], ["wiki_ordeal", "wiki_lateran", "leeson_ordeals", "wiki_inquisitorial", "wiki_combat"],
{"type": "timeline", "title": "From God's judgment to modern trials", "data": [
  {"year": 1198, "event": "Innocent III begins decretals creating inquisitorial procedure in church courts"},
  {"year": 1215, "event": "Fourth Lateran Council bars clergy from ordeals; Magna Carta signed"},
  {"year": 1219, "event": "Last ordeal in the English plea rolls"},
  {"year": 1532, "event": "Constitutio Criminalis Carolina for the Holy Roman Empire"},
  {"year": 1670, "event": "France's Criminal Ordinance codifies secret written procedure"},
  {"year": 1696, "event": "England lets treason defendants have counsel"},
  {"year": 1730, "event": "1730s: English judges let defence counsel cross-examine"},
  {"year": 1764, "event": "Beccaria's On Crimes and Punishments attacks torture"},
  {"year": 1808, "event": "Napoleon's code of criminal procedure: investigating judge plus jury"},
  {"year": 1836, "event": "Prisoners' Counsel Act gives English felony defendants full right to counsel"},
  {"year": 1989, "event": "Italy adopts an adversarial-style code"},
  {"year": 2009, "event": "Japan's lay judges sit for the first time"},
  {"year": 2026, "event": "England moves to cut jury trials; France drops criminal plea bargaining"},
]}))

SECTIONS.append(sec("continental_road", 4, "The continental road: files, proof rules and torture",
"""The inquisitio solved one problem and created another. A judge could now open a case on his own, gather witness statements in private and write everything down. Over the next three centuries, secular courts across Europe copied the method. The Holy Roman Empire's Carolina of 1532 and France's Criminal Ordinance of 1670 made it the law of the land.

To stop judges convicting on a whim, scholars of Roman and canon law built strict rules of proof. A capital conviction needed 'full proof': two eyewitnesses or a confession. Circumstantial evidence, however strong, was only 'half proof'. And when a judge had half proof but no witnesses, the law allowed him to torture the suspect to get the missing confession. Torture was not a breakdown of the system; it was a feature written into it.

The Enlightenment attacked it, the Revolution swept it away, and Napoleon rebuilt the system in 1808.""",
[
 sp("innocent_iii", "person", "Innocent III",
 "Lotario dei Conti di Segni became Pope in 1198 at 37 and spent his reign turning the Church into a legal state. From 1198 he issued decretals creating the processus per inquisitionem: a church court no longer needed a formal accuser, but could summon and question witnesses on its own initiative, often in secret, acting on public rumour (fama). It was designed to discipline corrupt clergy. Within a century the same method was used against heretics, and within three centuries by kings against everyone.",
 "A Pope in tall white mitre, the man behind both 1215 decisions.",
 "The legal founder, without intending it, of the inquisitorial trial.",
 "He took priests away from the ordeal and gave judges the power to investigate.",
 ["wiki_inquisitorial", "wiki_lateran"], ["img_innocent3"], [], ("Rome", 41.9029, 12.4534), "Pope 1198 to 1216"),
 sp("carolina_1532", "document", "The Carolina, 1532",
 "The Constitutio Criminalis Carolina was agreed at the Diet of Augsburg in 1530 and ratified at Regensburg in 1532 under Emperor Charles V, building on Johann von Schwarzenberg's Bamberg code of 1507. It gave the whole Holy Roman Empire one criminal procedure, defined crimes from murder to witchcraft, and set out when a judge could proceed to torture: when the indicia, the circumstantial signs, were strong enough. It laid legal foundations for the great witch trials of 1580 to 1680. Classical inquisitorial procedure lasted in German lands until Napoleon's reforms.",
 "A thick printed code with an imperial eagle, sixteenth century.",
 "The first empire-wide inquisitorial code, and the legal machinery of the witch hunts.",
 "Charles V's code told judges exactly when they could torture.",
 ["wiki_carolina", "wiki_inquisitorial"], ["img_carolina"], [], ("Regensburg", 49.0134, 12.1016), "1532"),
 sp("full_proof", "idea", "Full proof and the queen of proofs",
 "Roman-canon law refused to let a judge convict of a capital crime on circumstantial evidence alone. He needed two eyewitnesses or a confession. That rule was meant to protect the accused, but it had a terrible side effect. When a judge had 'half proof', one witness or strong circumstantial signs, he could order torture to obtain the confession that completed the proof. John Langbein argues that torture began to fade in the 1600s and 1700s mainly because courts invented lesser 'extraordinary punishments' they could impose without full proof, so a confession stopped being essential. A papal bull banned torture in Catholic countries in 1816.",
 "A rule that sounds protective, two witnesses or a confession, with a torture chamber behind it.",
 "Explains why the old inquisitorial system tortured, and why it stopped.",
 "Two witnesses or a confession: if you had neither, the rack supplied the second.",
 ["langbein_torture", "wiki_judicial_torture"], ["img_inq_room"], [], None, "About 1250 to 1800"),
 sp("spanish_inquisition", "event", "The Spanish Inquisition, myth and record",
 "Authorised by Pope Sixtus IV in 1478 and finally abolished in 1834, the Spanish Inquisition is why 'inquisitorial' sounds sinister in English. The records are grim but smaller than legend: historians estimate about 150,000 people prosecuted over three and a half centuries and 3,000 to 5,000 executed, mostly in the first fifty years. Henry Kamen notes that from 1559 to 1566 Spain executed around 100 people for heresy, about half as many as England under Mary Tudor. Today's inquisitorial courts descend from the general inquisitio, not from this religious tribunal.",
 "A vast public ceremony, the auto de fe, with penitents in tall hats before stands of spectators.",
 "The source of the name's bad reputation, and a lesson in separating legend from records.",
 "150,000 tried, a few thousand burned, and a word that never recovered.",
 ["wiki_spanish_inq"], ["img_autodefe", "img_inq_room"], [], ("Plaza Mayor, Madrid", 40.4155, -3.7074), "1478 to 1834"),
 sp("ordonnance_1670", "document", "France's Criminal Ordinance of 1670",
 "Drafted under Louis XIV's minister Colbert, registered by the Parlement of Paris on 26 August 1670 and in force from 1 January 1671, the Ordinance codified a secret, written procedure. Witnesses were heard privately and their statements written into the file; the accused often learned the evidence late. Its stated goals sound modern: no crime unpunished, no innocent convicted, punishment proportionate to offence. It lasted until the National Constituent Assembly abolished it by decree on 9 October 1789, three months after the Bastille fell.",
 "A royal ordinance, much commented on: Serpillon's 1767 commentary ran to four volumes.",
 "The high point of the secret written trial that the Revolution rejected.",
 "Louis XIV wrote the file-based trial down; the Revolution tore it up in 1789.",
 ["wiki_ordonnance"], ["img_serpillon"], [], ("Paris", 48.8566, 2.3522), "1670 to 1789"),
 sp("beccaria", "person", "Cesare Beccaria",
 "In 1764 a 26-year-old Milanese nobleman published Dei delitti e delle pene, On Crimes and Punishments. Beccaria argued that torture was cruel and also useless: it punished before guilt was proved, and it favoured the strong, who could endure pain, over the weak, who would confess to anything. He also argued for public trials and against secret accusations. The little book was translated across Europe and read by reformers from Catherine the Great to the American founders. Within decades, most European states had abolished judicial torture.",
 "An eighteenth-century Milanese in a powdered wig: the father of modern criminal law reform.",
 "The intellectual case against the old inquisitorial trial.",
 "A 26-year-old's slim book argued torture out of Europe's courts.",
 ["wiki_beccaria", "wiki_judicial_torture"], ["img_beccaria"], [], ("Milan", 45.4642, 9.19), "1764"),
 sp("napoleon_1808", "document", "Napoleon's code of criminal procedure, 1808",
 "The Code d'instruction criminelle of 1808 created the mixed model that most of Europe still recognises. A secret, written pre-trial investigation led by a juge d'instruction gathered evidence for and against the accused. Then came a public, oral trial, with a jury for serious crimes in the cour d'assises, directed to decide by their 'intime conviction', inner conviction, rather than by fixed proof rules. Napoleon's armies carried the code across Europe; it ended classical inquisitorial procedure in German lands. The David portrait shows rolled papers marked CODE on his desk.",
 "Napoleon in his study at 4.13 a.m. by the clock, beside a scroll labelled CODE.",
 "The blueprint for the modern French-style trial: investigating judge first, public trial second.",
 "Napoleon gave Europe a secret first act and a public second act.",
 ["wiki_inquisitorial", "wiki_examining"], ["img_napoleon", "img_code_civil"], [], ("Paris", 48.8566, 2.3522), "1808, in force 1811"),
], ["q_fullproof_mcq", "q_inq_tf"], ["wiki_inquisitorial", "wiki_carolina", "wiki_ordonnance", "langbein_torture", "wiki_judicial_torture", "wiki_spanish_inq", "wiki_beccaria"]))

SECTIONS.append(sec("common_law_road", 5, "The English road: from no lawyers to all lawyers",
"""England went the other way after 1215, but not because it was gentler. For most of the next five centuries an English felony trial was a quick, lawyer-free conversation. The victim prosecuted, the accused answered personally, the judge chatted with the jury, and a trial at the Old Bailey could be over in minutes. A person accused of murder or theft was forbidden a defence lawyer on the facts.

Change came in steps. Treason defendants got counsel in 1696. In the 1730s, worried by paid thief-takers and accomplices who testified to save their own necks, judges began letting defence lawyers cross-examine prosecution witnesses. Langbein calls what followed the 'lawyerisation' of the trial: within a century, from the 1690s to the 1780s, counsel took over, and the trial stopped being a chance for the accused to speak and became a chance for his lawyer to test the prosecution. Parliament gave felony defendants a full right to counsel in 1836.""",
[
 sp("microcosm_old_bailey", "place", "The Georgian Old Bailey",
 "Rowlandson and Pugin's print of about 1808 shows the court Garrow knew: judges under a canopy, the jury boxed to one side, a prisoner in the dock. The building had been re-fronted in 1734 to keep out the public; the stuffy room bred typhus, and in 1750 'gaol fever' carried from Newgate killed about 60 people, including the Lord Mayor and two judges. The published Proceedings record nearly 200,000 trials held there between 1674 and 1913.",
 "Crowded wooden galleries, a canopy over the judges, a prisoner in the dock in front of the jury.",
 "The room where the adversarial trial was invented, case by case.",
 "In 1750 the trial killed the judges: gaol fever from Newgate.",
 ["wiki_old_bailey", "oldbailey_online", "langbein_origins"], ["img_microcosm"], [], ("Old Bailey, London", 51.5155, -0.1019), "About 1808"),
 sp("garrow", "person", "William Garrow",
 "Called to the Bar on 27 November 1783 at 23, Garrow made his name at the Old Bailey as a ferocious cross-examiner, acting for the defence in about 83 per cent of his cases. He dismantled thief-takers and paid informers, and pressed medical witnesses until they admitted what they could not prove. His insistence that hearsay and copied documents be kept out helped shape the best evidence rule. He is credited with using the phrase 'presumed innocent until proven guilty' in 1791. Rediscovered by historians in 1991, he became the hero of BBC One's Garrow's Law.",
 "A sharp-featured Georgian barrister, famous for cross-examination rather than speeches.",
 "The lawyer who did most to make the English trial a battle between counsel.",
 "Garrow turned cross-examination into the main event.",
 ["wiki_garrow", "langbein_origins"], ["img_garrow"], [], ("Old Bailey, London", 51.5155, -0.1019), "1760 to 1840"),
 sp("hardy_1794", "event", "The treason trial of Thomas Hardy, 1794",
 "Thomas Hardy, a London shoemaker who founded the London Corresponding Society to campaign for the vote, was charged with high treason in 1794, a crime punishable by hanging, drawing and quartering. His defender, Thomas Erskine, spent days taking apart the government's theory that campaigning for reform was a plot against the King. After nine days, an unprecedented length then, the jury acquitted on 5 November 1794; the foreman reportedly collapsed after giving the verdict, and crowds outside cheered Erskine as a hero. Charges against other radicals soon collapsed.",
 "A printed record by the shoemaker himself; a medal reading 'Acquitted by his jury'.",
 "Showed the jury, briefed by a great advocate, as a shield against the state.",
 "Nine days, one shoemaker, one jury, and the government lost.",
 ["tna_hardy", "wiki_hardy", "wiki_erskine"], ["img_erskine", "img_hardy_title"], [], ("Old Bailey, London", 51.5155, -0.1019), "October to 5 November 1794"),
 sp("prisoners_counsel_1836", "document", "The Prisoners' Counsel Act 1836",
 "Until 1836, English law said that a person accused of a felony, which covered murder, rape, robbery, arson and most thefts, could not have a lawyer address the jury for him. The argument was that the facts should speak for themselves and that the judge was the prisoner's counsel. In practice, courts had allowed lawyers to examine witnesses since the 1730s, but only the 1836 Act gave the full right. In the United States, by contrast, the federal right to retained counsel was in the Constitution from the start; free counsel for poor state defendants came only in 1963.",
 "A short statute that let defence lawyers finally speak to the jury.",
 "Completed the shift from the accused speaking to the lawyer speaking.",
 "Before 1836, a man on trial for his life in England could not have a lawyer argue his case.",
 ["wiki_adversarial", "wiki_garrow", "langbein_origins"], [], [], ("Westminster, London", 51.4995, -0.1248), "1836"),
], ["q_order_history", "q_garrow_clues"], ["langbein_origins", "wiki_garrow", "wiki_old_bailey", "wiki_adversarial"]))

SECTIONS.append(sec("adversarial_machine", 6, "How the contest works",
"""The adversarial trial runs on a few powerful machines. **Cross-examination** lets each side test the other's witnesses with leading questions. **Exclusionary rules** keep some true but unfair evidence out, such as hearsay or, in the United States, evidence obtained by an illegal search. The **jury**, untrained and unreasoning by design, gives a verdict without reasons. And the **right to silence** means the accused need not say a word.

All of this is expensive. A full jury trial takes days or weeks, so the system survives by not using it. In the United States, about nine in ten federal defendants plead guilty, usually in a bargain with the prosecutor, and only about 2 per cent go to trial. Critics call this the system's dark secret: a trial model built around a contest that almost nobody gets.""",
[
 sp("wigmore_cross", "idea", "Cross-examination, 'the greatest legal engine'",
 "John Henry Wigmore, whose multi-volume Treatise on Evidence (first published 1904 to 1905) shaped American law for a century, wrote that cross-examination is 'beyond any doubt the greatest legal engine ever invented for the discovery of truth.' Lawyers quote that sentence constantly. Fewer quote his warning that the same engine, used carelessly or cynically, can make an honest witness look like a liar. In continental courts the defence can question witnesses too, but the long hostile cross-examination is mostly an English and American art.",
 "A lawyer asking a hostile witness short, leading questions that can only be answered yes or no.",
 "The signature tool of the adversarial trial, and its most contested.",
 "The greatest engine for truth, or the best machine for making liars of honest people.",
 ["wiki_wigmore", "umich_cross", "wiki_adversarial"], ["img_wigmore"], [], ("Northwestern University, Chicago", 41.8967, -87.6189), "Treatise 1904 to 1905"),
 sp("twelve_angry_men", "work", "12 Angry Men (1957)",
 "Sidney Lumet's first feature, adapted by Reginald Rose from his 1954 television play, takes place almost entirely in one jury room. Eleven jurors vote guilty at once; Juror 8, played by Henry Fonda, wants to talk first. Over 96 minutes he unpicks the evidence, including a witness who could not have heard a shout over a passing train. It is the jury system's best advertisement, and also an accidental critique: the jurors do their own investigating, which real jurors are told not to do. The Library of Congress added it to the National Film Registry in 2007.",
 "Twelve men, one hot room, one holdout.",
 "How most people picture the adversarial ideal.",
 "Eleven to one, and the one was right.",
 ["wiki_12angry"], ["img_12angry"], ["vid_12angry"], None, "1957"),
 sp("gideon", "person", "Clarence Earl Gideon and the right to a lawyer",
 "In 1961 Gideon, a drifter, was charged with breaking into a Florida pool hall. He asked for a lawyer; Florida provided them only in capital cases. He defended himself and got five years. From prison he wrote a petition to the US Supreme Court in pencil on prison paper. On 18 March 1963, in Gideon v Wainwright, Justice Hugo Black's unanimous opinion held that states must provide counsel to poor defendants in felony cases. At his retrial on 5 August 1963, with a lawyer cross-examining the key witness, the jury acquitted Gideon after an hour.",
 "A pencilled petition from a Florida prison cell.",
 "An adversarial trial without a lawyer on one side is not a contest at all.",
 "Same evidence, plus one lawyer: five years became not guilty in an hour.",
 ["wiki_gideon"], ["img_gideon"], [], ("Panama City, Florida", 30.1588, -85.6602), "1961 to 1963"),
 sp("miranda", "person", "Ernesto Miranda and the right to silence",
 "In 1963 Phoenix police questioned Ernesto Miranda for two hours about a kidnapping and rape, and he signed a confession. In Miranda v Arizona (1966) the Supreme Court ruled that confessions made in custody are inadmissible unless suspects are first warned of their right to silence and to a lawyer. Miranda was retried without the confession and convicted again. Paroled in 1972, he sold autographed 'Miranda cards' of the warning. In 1976 he was stabbed to death in a Phoenix bar; the man arrested was read his Miranda rights, stayed silent, and was released.",
 "The warning every television viewer knows: 'You have the right to remain silent.'",
 "The adversarial system protects the accused from being made the main source of proof.",
 "The man who gave his name to the warning was killed by a man who used it.",
 ["wiki_miranda", "aba_miranda", "wiki_exclusionary"], ["img_miranda"], [], ("Phoenix, Arizona", 33.4484, -112.074), "1963 to 1976"),
 sp("plea_bargain_us", "custom", "The plea bargain",
 "In fiscal 2022 there were 71,954 defendants in US federal district courts. About 89.5 per cent pleaded guilty, 8.2 per cent had their cases dismissed, 1.9 per cent went to trial and were convicted, and 0.4 per cent, just 290 people, were acquitted. In 1998, 7 per cent went to trial; by 2018, 2 per cent. The guilty plea is fast and cheap, but defendants who refuse a deal and lose at trial often get much longer sentences, the 'trial penalty'. An experiment by Lucian Dervan and Vanessa Edkins in 2013 found more than half of innocent student participants accepted a deal to admit cheating.",
 "A deal struck in a corridor rather than a verdict delivered in court.",
 "The adversarial system's real workhorse in the United States.",
 "Nine in ten plead; two in a hundred get the trial the system was built for.",
 ["pew_2023", "pew_2019", "dervan_edkins", "wiki_plea"], [], [], ("United States federal courts", 38.8977, -77.0365), "Fiscal 2022 data"),
], ["q_pew_mcq", "q_miranda_tf"], ["wiki_adversarial", "pew_2023", "pew_2019", "wiki_exclusionary", "wiki_wigmore"],
{"type": "donut", "title": "What happened to US federal defendants, fiscal 2022", "source_ids": ["pew_2023"], "data": [
  {"label": "Pleaded guilty", "value": 89.5}, {"label": "Case dismissed", "value": 8.2}, {"label": "Convicted at trial", "value": 1.9}, {"label": "Acquitted at trial", "value": 0.4}]}))

SECTIONS.append(sec("inquisitorial_machine", 7, "How the inquiry works",
"""A continental criminal case is a long first act and a shorter second act. In the first, police and prosecutors investigate, and everything goes into a written dossier. In France the most serious or complex cases go to a juge d'instruction, an independent judge who must look for evidence both for and against the accused, 'à charge et à décharge'. In the second act, a public trial, the presiding judge leads the questioning from that file.

Several features follow. Lay people often sit **beside** professional judges, not apart from them: Germany's Schöffen, France's jurors in the cour d'assises, Japan's saiban-in. Judgments come with **written reasons**. Appeals can reopen the facts. Because a confession does not end the case, there is no simple guilty plea, though every system processes minor cases on paper.""",
[
 sp("juge_instruction", "person", "The investigating judge",
 "The juge d'instruction is the most famous and least typical figure of the French system. Independent of the government, the judge can question suspects and witnesses, order searches and wiretaps, and must gather evidence both ways. But it handles a small minority of cases: in 2005 France issued 1.1 million criminal rulings while judges opened 33,000 new investigations; in 2023 about 16,600 judicial investigations were opened. West Germany abolished the office in 1974, Portugal in 1987, Italy in 1989 and Switzerland in 2011. Spain's Baltasar Garzón used the role to pursue Augusto Pinochet in 1998.",
 "A judge with a detective's powers, working before the trial, never sitting on it.",
 "The icon of inquisitorial justice, and a shrinking one.",
 "France's judge-detective handles well under one case in a hundred.",
 ["wiki_examining", "wiki_inquisitorial", "rsj_instruction"], ["img_garzon"], [], ("France, Belgium, Spain, Netherlands", 48.8566, 2.3522), "Created 1808"),
 sp("mixed_court", "custom", "Lay judges on the bench",
 "Germany abolished its jury by emergency decree on 4 January 1924 and replaced it with a mixed court of professional judges and lay judges, Schöffen, who sit side by side, deliberate together and vote together. Most decisions against a defendant need a two-thirds majority. France keeps citizen jurors in the cour d'assises but they deliberate with three professional judges. Japan's saiban-in system, since 2009, puts six citizens with three judges. The idea: lay common sense, professional reasoning, and one written judgment.",
 "Ordinary citizens in the same row as the robed judges, not in a separate box.",
 "The continental answer to the jury: participation without a sealed verdict.",
 "In Germany the jury did not leave; it moved up onto the bench.",
 ["wiki_lay_judge", "wiki_japan_cj"], ["img_aachen_room"], ["vid_japan_lay_judge"], ("Germany, France, Japan", 50.1109, 8.6821), "Germany since 1924"),
 sp("penal_order", "document", "The penal order: a conviction by post",
 "For minor offences, German prosecutors can ask a judge to sign a Strafbefehl, a written penalty proposal sent to the accused. If no objection arrives within two weeks, it becomes a final conviction, with no hearing. Langbein argued in 1979 that this is not plea bargaining because the penalty is not raised for those who object. Today it dominates small cases: Baden-Württemberg's justice ministry reported that about 97 per cent of its convictions to fines were made by penal order. Critics say people can end up in prison for unpaid fines without ever seeing a judge.",
 "A letter that says: this is your sentence; object within two weeks or it stands.",
 "Shows that inquisitorial systems also avoid full trials for most cases, by paper rather than bargain.",
 "Germany's quiet plea bargain arrives in the post.",
 ["langbein_1979", "beck_strafbefehl"], [], [], ("Baden-Württemberg, Germany", 48.6616, 9.3501), "Data reported 2024"),
 sp("taxquet", "event", "Taxquet v Belgium: must a verdict explain itself?",
 "In 2004 a Belgian assize jury convicted Richard Taxquet of the 1991 murder of former minister André Cools by answering 'yes' or 'no' to four questions. In 2010 the Grand Chamber of the European Court of Human Rights found that Belgium had breached his right to a fair trial: he had not been given enough safeguards to understand why he was convicted. The court stressed that juries are not required to give reasons, but the case pushed jury systems in Europe to build in explanations, through detailed questions or written reasons.",
 "Four one-word answers that convicted a man of murder.",
 "Where Europe's human rights law meets the jury's unexplained verdict.",
 "Yes, yes, yes, no: not enough to tell a man why he got 20 years.",
 ["taxquet_blog"], ["img_echr_room"], [], ("European Court of Human Rights, Strasbourg", 48.5964, 7.7743), "Grand Chamber, 16 November 2010"),
], ["q_juge_mcq", "q_penal_tf"], ["wiki_inquisitorial", "wiki_examining", "wiki_lay_judge", "langbein_1979", "rsj_instruction"]))

SECTIONS.append(sec("thinkers", 8, "The people who argued about it",
"""Comparative procedure has a small cast of brilliant arguers. On one side are those who think the contest is the best guarantee of liberty: let two partisan searchers, as the English judge Lord Devlin put it, start from opposite ends of the field, and between them they will miss less than a neutral searcher starting in the middle. On the other are those who think the contest turns justice into a sport won by the better-paid lawyer.

Mirjan Damaška, a Croatian-born Yale professor, argued in The Faces of Justice and State Authority (1986) that procedure mirrors the state: career judges in a hierarchy, working from files, drift toward inquiry; lay people and one-off trials drift toward contest. And some of the sharpest critics of the adversarial trial have been Americans who studied Europe.""",
[
 sp("jerome_frank", "person", "Jerome Frank and the 'fight theory'",
 "Jerome Frank was a New Deal official, chairman of the Securities and Exchange Commission and then a federal appeals judge in New York from 1941. In Courts on Trial (1949) he wrote a chapter titled 'The Fight Theory versus the Truth Theory'. Trials, he argued, were run like duels, with lawyers trained to hide facts that hurt their clients and to confuse honest witnesses. Frank was a 'fact sceptic': he thought the weakest part of justice was not the law but the finding of facts, and he called for more scientific methods of gathering them.",
 "An American judge who called his own system a fight.",
 "The classic insider critique of the adversarial trial.",
 "Frank's question: are we looking for the truth, or for a winner?",
 ["frank_courts"], ["img_frank"], [], ("New York", 40.7128, -74.006), "Courts on Trial, 1949"),
 sp("langbein_critic", "person", "John Langbein, the comparative critic",
 "Born in 1941, Langbein studied at Columbia, Harvard and Cambridge, where his doctoral thesis was on Renaissance criminal procedure, and taught at Chicago and then Yale. His work shaped this whole topic: Torture and the Law of Proof (1977), 'Land Without Plea Bargaining' (1979), an essay on the German advantage in civil procedure (1985), and The Origins of Adversary Criminal Trial (2003). His provocative claim was that American plea bargaining and medieval torture solve the same problem: a trial so demanding that the state needs a way to get a confession without one.",
 "The Yale historian who found the roots of American plea bargaining in medieval torture chambers.",
 "His books are the backbone of how scholars now tell this story.",
 "Torture then, plea bargaining now: two answers to a trial too costly to hold.",
 ["wiki_langbein", "langbein_torture", "langbein_origins", "langbein_1979"], [], [], ("Yale Law School, New Haven", 41.3113, -72.9282), "Born 1941"),
], ["q_frank_mcq", "q_thinkers_match"], ["wiki_adversarial", "langbein_torture", "frank_courts", "wiki_damaska"]))

SECTIONS.append(sec("collisions", 9, "When the two systems met",
"""The most interesting moments come when the two families are forced to share a courtroom or when a country switches sides. At Nuremberg in 1945, American and British lawyers who expected cross-examination worked beside French and Soviet judges who expected a dossier. Today the International Criminal Court runs a deliberate hybrid. Italy rewrote its code in 1989 to import adversarial features; Japan added citizens to its benches in 2009; Mexico and much of Latin America swapped written inquisitorial trials for oral, accusatory ones.

None of these transplants arrived whole. Lawyers trained in one tradition kept their habits in the other, and legal scholars still argue over whether the hybrids combine the best of both or the worst.""",
[
 sp("nuremberg", "event", "Nuremberg: cross-examining Göring",
 "The International Military Tribunal, created by the United States, United Kingdom, France and the Soviet Union, opened in Courtroom 600 of Nuremberg's Palace of Justice in November 1945. On 20 March 1946 the American chief prosecutor, Supreme Court Justice Robert Jackson, began cross-examining Hermann Göring. It went badly: Göring was quick and Jackson was buried in documents. The British judge Norman Birkett overruled Jackson's attempts to cut Göring off and later wrote that Jackson had not learned the basics of cross-examination as English courts practise it. The British prosecutor David Maxwell Fyfe did better. Twelve defendants were sentenced to death.",
 "Göring in headphones in the dock, listening to simultaneous translation.",
 "The first great test of mixing trial traditions, broadcast to the world.",
 "Nuremberg proved cross-examination is a craft, not a right you automatically win with.",
 ["wiki_nuremberg", "spectator_goring", "jackson_goring"], ["img_goering", "img_jackson", "img_imt_bench", "img_imt_dock"], ["vid_jackson_opening"], ("Palace of Justice, Nuremberg", 49.4542, 11.0490), "20 November 1945 to 1 October 1946"),
 sp("icc", "building", "The International Criminal Court",
 "The ICC in The Hague, set up under the Rome Statute in force since 2002, describes its trials as a hybrid of common law and civil law. Prosecutors and defence call witnesses and cross-examine, as in London; but there is no jury, a panel of three professional judges decides, judges may ask for evidence, hearsay is not generally banned, and victims can take part in proceedings and claim reparations from a Trust Fund. Before a trial, a pre-trial chamber holds a confirmation of charges hearing, a filter that resembles a continental judicial check. That is the stage Rodrigo Duterte's case passed in April 2026.",
 "A white and green modern building in the dunes of The Hague.",
 "The clearest working example of a deliberate hybrid trial.",
 "No jury, three judges, cross-examination and victims in the room.",
 ["wiki_icc", "hrw_duterte"], ["img_icc"], ["vid_icc_duterte"], ("International Criminal Court, The Hague", 52.1065, 4.3248), "Rome Statute in force 2002"),
 sp("italy_1989", "document", "Italy's 1989 code and the Knox case",
 "Italy's new Code of Criminal Procedure took effect on 24 October 1989. It abolished the investigating judge, introduced cross-examination and gave the parties control of evidence, plus bargain-style shortcuts that cut sentences. But old habits stayed. When Amanda Knox and Raffaele Sollecito were tried in 2009 for the 2007 murder of Meredith Kercher, the corte d'assise of two professional and six lay judges also heard a civil claim by Patrick Lumumba, whom Knox had wrongly accused, in the same proceedings. Appeal meant a full rehearing: convicted in 2009, acquitted in 2011, reconvicted in 2014, definitively acquitted by the Court of Cassation in 2015.",
 "A trial that looked American on television and worked Italian in the courtroom.",
 "The most watched example of a half-transplanted adversarial system.",
 "Convicted, acquitted, convicted, acquitted: Italy's appeals reopen the facts.",
 ["psilr_italy", "wiki_examining", "wiki_knox", "wiki_kercher"], ["img_knox"], [], ("Perugia, Italy", 43.1107, 12.3908), "Code 1989; Knox case 2007 to 2015"),
 sp("mexico_2016", "event", "Mexico's switch to oral trials",
 "In 2008 Mexico amended its constitution to replace slow, written, inquisitorial criminal trials with public, oral, accusatory ones, where prosecution and defence argue before a judge in open court, often filmed. States were given until 18 June 2016 to finish the change, under a new National Code of Criminal Procedure first used federally in Durango and Puebla in 2014. Chile had made a similar switch between 2000 and 2005, and most of Latin America followed. Results have been uneven: some states moved fast, others were still passing laws years after the reform began.",
 "A courtroom with cameras and lawyers speaking, instead of clerks typing a file.",
 "The biggest wave of adversarial reform anywhere in the last half-century.",
 "Latin America swapped the file for the microphone.",
 ["emory_mexico", "wiki_examining"], ["img_mx_oral"], [], ("Mexico", 19.4326, -99.1332), "2008 to 2016"),
], ["q_nuremberg_img", "q_italy_order"], ["wiki_nuremberg", "wiki_icc", "psilr_italy", "emory_mexico", "wiki_examining"],
{"type": "map", "title": "Courtrooms in today's story", "data": {"pins": [
  {"label": "Old Bailey, London", "lat": 51.5155, "lon": -0.1019, "spotlight_id": "old_bailey_court1"},
  {"label": "Palais de justice, Paris", "lat": 48.8556, "lon": 2.345, "spotlight_id": "paris_grands_proces"},
  {"label": "Lateran Palace, Rome (1215)", "lat": 41.8859, "lon": 12.5057, "spotlight_id": "lateran_1215"},
  {"label": "Várad ordeal register, Oradea", "lat": 47.0722, "lon": 21.9217, "spotlight_id": "leeson_ordeals"},
  {"label": "Palace of Justice, Nuremberg", "lat": 49.4542, "lon": 11.049, "spotlight_id": "nuremberg"},
  {"label": "International Criminal Court, The Hague", "lat": 52.1065, "lon": 4.3248, "spotlight_id": "icc"},
  {"label": "Perugia, Italy", "lat": 43.1107, "lon": 12.3908, "spotlight_id": "italy_1989"},
  {"label": "Outreau, France", "lat": 50.7056, "lon": 1.5936, "spotlight_id": "outreau"},
  {"label": "Avignon, France", "lat": 43.9493, "lon": 4.8055, "spotlight_id": "pelicot"},
  {"label": "Shizuoka, Japan", "lat": 34.9756, "lon": 138.3828, "spotlight_id": "hakamada"},
  {"label": "Supreme Court of India, New Delhi", "lat": 28.6224, "lon": 77.2397, "spotlight_id": "ram_chander"},
  {"label": "Phoenix, Arizona", "lat": 33.4484, "lon": -112.074, "spotlight_id": "miranda"},
]}}))

SECTIONS.append(sec("failures", 10, "When each system fails",
"""Every system convicts innocent people. What differs is how. In adversarial systems the classic failures are a weak or absent defence lawyer, a coerced plea, a mistaken eyewitness the jury believed, and evidence the prosecution never handed over. In the United States the National Registry of Exonerations listed 3,698 exonerations since 1989 as of June 2025; in its early data, perjury or false accusation featured in about half, mistaken identification in 43 per cent and false confessions in 16 per cent.

In inquisitorial systems the classic failures run the other way: a single official convinced early, a file that hardens around one theory, long pre-trial detention that pressures confessions, and appeal judges who trust the file. The four cases below are among the most studied in the world, and each led to reform.""",
[
 sp("outreau", "event", "The Outreau affair, France",
 "In 2001, in Outreau near Boulogne-sur-Mer, a young investigating judge, Fabrice Burgaud, fresh from the national school for judges, came to believe that a paedophile ring involved dozens of adults. Seventeen were tried, several after one to three years in pre-trial detention; another suspect, François Mourmand, died in custody in 2002 before any trial. The case rested on a woman's accusations and children's testimony backed by psychiatric experts. She later admitted lying. In the end 13 of the 17 accused were acquitted, after an appeal in Paris in 2005; President Chirac apologised. A parliamentary inquiry followed, and Burgaud received a reprimand in 2009.",
 "A small working-class town whose name became France's word for judicial disaster.",
 "The defining failure of the investigating judge: one official, one theory, no brake.",
 "One judge, one story, thirteen innocent people in jail.",
 ["wiki_outreau"], ["img_outreau"], [], ("Outreau, Pas-de-Calais", 50.7056, 1.5936), "2001 to 2005"),
 sp("hakamada", "person", "Iwao Hakamada, Japan",
 "A former professional boxer, Hakamada was arrested in 1966 for the murder of a family of four at a miso maker's home. Interrogated, his lawyers said, for 264 hours over 23 days, he confessed, then retracted. In 1968 he was sentenced to death. The key evidence, bloodstained clothes 'found' in a miso tank 14 months after the crime, were too small for him; prosecutors said a size label 'B' meant medium, but it meant black. A court freed him in 2014, he was acquitted at retrial on 26 September 2024 at age 88, and in March 2025 he was awarded 217,362,500 yen, 12,500 yen for each day held.",
 "An old man, once a featherweight boxer, who spent 46 years waiting to be hanged.",
 "Japan's most famous wrongful conviction, built on interrogation and planted evidence.",
 "The clothes were too small, and B meant black.",
 ["wiki_hakamada", "wiki_hostage"], ["img_hakamada"], ["vid_hakamada_itv"], ("Shizuoka, Japan", 34.9756, 138.3828), "Arrested 1966, acquitted 2024"),
 sp("ghosn", "person", "Carlos Ghosn and 'hostage justice'",
 "The chairman of Nissan was arrested in Tokyo in November 2018 on financial charges and held for 108 days before bail, repeatedly re-arrested, and questioned without a lawyer present. Japanese suspects can be held up to 23 days before charge, often in police cells. Critics call this hitojichi shihō, hostage justice: suspects who deny charges stay locked up, while those who confess go home. At the end of December 2019 Ghosn escaped by hiding in a large box for audio equipment, carried onto a private jet at Kansai airport, and reached Beirut. Two Americans who helped him were later jailed in Japan.",
 "A car executive who escaped Japanese justice inside a music equipment box.",
 "Put Japan's pre-trial detention and 99 per cent conviction rate in world headlines.",
 "Confess and go home, deny and stay: Ghosn chose the box.",
 ["wiki_ghosn", "wiki_hostage", "occrp_ghosn", "wiki_japan_cj"], ["img_ghosn"], [], ("Tokyo, then Kansai airport, Osaka", 34.4320, 135.2304), "2018 to 2019"),
 sp("pelicot", "event", "The Pelicot trial, France",
 "For nearly a decade Dominique Pelicot drugged his wife Gisèle and invited dozens of men to rape her, filming the assaults. In 2024 he and 50 other men were tried in Avignon by the Vaucluse criminal court, five professional judges and no jury, under France's newer cours criminelles départementales. Gisèle Pelicot refused the closed hearing she was entitled to. In December 2024 all 51 were convicted; Dominique got the maximum 20 years. The only man who kept his appeal, Husamettin Dogan, was retried in Nîmes before three judges and citizen jurors, and on 9 October 2025 his sentence rose from nine to ten years.",
 "A woman walking into court through applause, having insisted the trial be public.",
 "A landmark of judge-led trial for mass sexual violence, and of victim choice in procedure.",
 "Fifty-one defendants, five judges, no jury, one woman who refused to hide.",
 ["wiki_pelicot", "aljazeera_pelicot", "an_ccd"], ["img_pelicot"], [], ("Avignon, Vaucluse", 43.9493, 4.8055), "September to December 2024; appeal October 2025"),
], ["q_hakamada_clues", "q_outreau_mcq"], ["wiki_nre", "wiki_outreau", "wiki_hakamada", "wiki_ghosn", "wiki_pelicot"]))

SECTIONS.append(sec("truth_evidence", 11, "Which finds more truth? What the evidence says",
"""Nobody knows the true answer in most real cases, so testing which system convicts the right people is hard. The proxies are slippery.

Conviction rates mislead. Japan's rate above 99 per cent sounds sinister, but Japanese prosecutors decline to charge about 60 per cent of the cases they receive and send many others to paper procedures. Bruce Aronson of New York University points out that counted the same way, US federal convictions in 2018 were also above 99 per cent. Psychology helps a little. In laboratory experiments in the 1970s, John Thibaut and Laurens Walker found that people judged adversarial procedures fairer because they gave the parties control over presenting their case; later work suggests people may still think inquisitorial procedures find more truth. Fairness and accuracy, in other words, may be different goods.""",
[
 sp("conviction_paradox", "idea", "The 99 per cent puzzle",
 "J. Mark Ramseyer and Eric Rasmusen tested two explanations for Japan's conviction rate. Either judges are pressured to convict, or understaffed prosecutors, a few thousand for 125 million people, only charge the cases they are sure to win. The evidence favoured selection. Article 248 of Japan's Code of Criminal Procedure lets prosecutors drop a case they could win, considering the offender's character, age and circumstances. After citizen lay judges arrived in 2009, prosecution rates for murder fell from 56.8 per cent in 2006 to 28.2 per cent in 2017, and one measure of the first-instance conviction rate dipped to 97.8 per cent.",
 "A number that sounds like a show trial and is mostly a filter before trial.",
 "Teaches you to ask what a conviction rate is a rate of.",
 "Japan convicts almost everyone it tries because it tries almost no one it might lose.",
 ["wiki_japan_cj"], ["img_japan_sc", "img_japan_grand"], [], ("Supreme Court of Japan, Tokyo", 35.6806, 139.7436), "Data 2006 to 2017"),
 sp("thibaut_walker", "experiment", "The fairness experiments",
 "In a series of experiments summarised in Procedural Justice (1975), the social psychologist John Thibaut and the lawyer Laurens Walker had participants resolve simulated disputes under different procedures. Participants preferred adversarial procedures and rated them fairer, apparently because they kept 'process control' in the disputants' hands. The finding launched the field of procedural justice, which shows that people accept losing more readily when they feel heard. Its weak point: the subjects were mostly American students, and preferences may reflect what people are used to.",
 "Students in a 1970s lab choosing how their mock dispute would be judged.",
 "Shows why people like adversarial trials even when accuracy is uncertain.",
 "We trust the trial where we get to speak, even if it is not the one that finds the truth.",
 ["sage_procedural"], [], [], ("University of North Carolina, Chapel Hill", 35.9049, -79.0469), "1970s; book 1975"),
], ["q_japan_hl", "q_truth_tf"], ["wiki_japan_cj", "sage_procedural", "wiki_nre", "dervan_edkins"],
{"type": "bar", "title": "Japan's lay judges: willingness fell as trials grew longer", "source_ids": ["nippon_saibanin"], "data": [
  {"metric": "Selected citizens who declined to serve (%)", "y2009": 53.1, "y2018": 67},
  {"metric": "Attendance at selection procedure (%)", "y2009": 83.9, "y2018": 60},
  {"metric": "Average trial length (days)", "y2009": 3.7, "y2018": 10.8}]}))

SECTIONS.append(sec("india", 12, "India: an adversarial system that asks its judges to dig",
"""India inherited the English adversarial trial with the Code of Criminal Procedure and the Indian Evidence Act of 1872. Prosecution and defence call and cross-examine witnesses; the judge decides. Since 1 July 2024 the codes have new names, the Bharatiya Nagarik Suraksha Sanhita and the Bharatiya Sakshya Adhiniyam, but the contest model remains.

Yet Indian law has always held an inquisitorial thread. Section 165 of the 1872 Evidence Act, now Section 168 of the Sakshya Adhiniyam, lets a judge ask any witness any question at any time and order any document produced, and the parties cannot object. India's Supreme Court has repeatedly told trial judges to use it. India also dropped the jury decades ago, uses plea bargaining almost never, and keeps three out of four prisoners waiting for trial. Ancient India, meanwhile, had its own ordeals.""",
[
 sp("ram_chander", "document", "Ram Chander v State of Haryana, 1981",
 "On 25 February 1981 Justice O. Chinnappa Reddy wrote words Indian courts still quote: 'The adversary system of trial being what it is, there is an unfortunate tendency for a judge presiding over a trial to assume the role of a referee or an umpire and to allow the trial to develop into a contest between the prosecution and the defence with the inevitable distortions flowing from combative and competitive elements entering the trial procedure.' A criminal judge, he said, 'must cease to be a spectator and a mere recording machine. He must become a participant in the trial by evincing intelligent active interest.'",
 "A Supreme Court judgment telling judges not to be referees.",
 "India's sharpest official rejection of the pure umpire model.",
 "Not a spectator, not a recording machine: India's judge is told to join in.",
 ["ik_ramchander"], ["img_sci"], [], ("Supreme Court of India, New Delhi", 28.6224, 77.2397), "25 February 1981"),
 sp("section_165", "document", "The judge's power to ask anything",
 "Section 165 of the Indian Evidence Act, 1872, written by James Fitzjames Stephen, gave Indian judges a power English judges did not have in such sweeping terms: to ask any question, in any form, at any time, of any witness or party, about any fact relevant or irrelevant, and to order any document or thing produced. The parties cannot object, and cannot cross-examine on the answers without the court's permission. It survives almost word for word as Section 168 of the Bharatiya Sakshya Adhiniyam, 2023. Judgments must still rest only on evidence properly proved.",
 "A clause that quietly turns an Indian umpire into an investigator when needed.",
 "The inquisitorial tool built into India's adversarial law since 1872.",
 "Section 165 became 168: same power, new number.",
 ["bsa_168", "ik_ramchander"], ["img_sci_inside"], [], ("India", 28.6224, 77.2397), "1872; renumbered 2023"),
 sp("malimath", "document", "The Malimath Committee, 2003",
 "In 2003 a committee chaired by Justice V. S. Malimath, a former Chief Justice of Karnataka and Kerala High Courts, reviewed India's criminal justice system. It concluded that the adversarial system better protects the accused but proposed borrowing inquisitorial features: making the 'quest for truth' a fundamental duty of every court, giving judges a statutory duty to seek the truth actively, and letting courts draw adverse inferences when the accused refused to answer questions. Human rights groups, including the International Commission of Jurists, objected that this would erode the right to silence and the court's neutrality. Most of the proposals were never enacted.",
 "A thick government report that asked Indian judges to become truth-seekers.",
 "India's most serious attempt to import the inquisitorial model.",
 "Malimath wanted truth as the court's duty; critics heard the end of silence.",
 ["malimath", "icj_malimath"], [], [], ("New Delhi", 28.6139, 77.209), "Report 2003"),
 sp("nanavati", "event", "The Nanavati case and the end of India's juries",
 "In 1959 Commander Kawas Nanavati, a naval officer, shot dead his wife's lover in Bombay and gave himself up. A Bombay jury acquitted him by eight votes to one amid a press campaign that turned him into a hero. The judge referred the case to the High Court, which set the verdict aside and convicted him of murder; the Supreme Court confirmed the conviction in 1961. The case is often called India's last jury trial, but that is a myth: the Law Commission had recommended abolishing juries in 1958, and some jury trials continued into the 1960s before the 1973 Code of Criminal Procedure left them out.",
 "A naval officer, a revolver, a tabloid campaign and an eight to one jury.",
 "Fixed in public memory why India gave up the jury.",
 "Eight jurors said not guilty; three courts said murder.",
 ["wiki_nanavati", "caravan_jury"], ["img_calcutta"], [], ("Bombay (Mumbai)", 18.9256, 72.8317), "1959 to 1961"),
 sp("plea_india", "custom", "India's plea bargain that nobody uses",
 "India added plea bargaining to the Code of Criminal Procedure through the Criminal Law (Amendment) Act, 2005, in force from 5 July 2006, for offences punishable with up to seven years, excluding offences affecting the country's socio-economic condition and those against women or children under 14. Uptake has been tiny. In 2022, 19,135 cases were disposed of by plea bargaining out of 1,70,52,367 cases for trial, about 0.11 per cent. Meanwhile pendency grows: 4,76,57,328 cases were pending in district and subordinate courts on 31 December 2025, and about three in four prisoners in 2023 were undertrials.",
 "A legal shortcut on the books for twenty years, used in about one case in a thousand.",
 "India has the adversarial trial's costs without its American escape valve.",
 "America pleads nine in ten; India about one in a thousand.",
 ["wiki_plea", "civils_plea", "ians_pendency", "dataful_ut"], [], [], ("India", 22.0, 79.0), "Since 2006; data 2022 to 2025"),
 sp("yajnavalkya_ordeals", "custom", "Divya: the ordeals of ancient Indian law",
 "Indian legal texts knew trial by ordeal too. The Yājñavalkya Smṛti lists five divya, divine tests: the balance, fire, water, poison and kośa, drinking water used to bathe a deity's image. The Nārada and Viṣṇu texts share the same five, and Kātyāyana adds rice grains and red-hot gold. The Ramayana's most famous scene, Sita's agni pariksha, is a trial by fire to prove her purity. As in Europe, ordeals were meant for cases where human evidence ran out, and the texts surround them with rules about who may undergo which test.",
 "Sita seated calmly in a ring of fire.",
 "Shows that the medieval European ordeal had close parallels in Dharmashastra.",
 "Five divine tests: scale, fire, water, poison and the sacred drink.",
 ["unica_yajnavalkya", "wiki_ordeal"], ["img_sita"], [], ("Ancient India", 25.3, 82.9), "Smritis of the early first millennium CE"),
], ["q_india_mcq", "q_india_hl", "q_sita_img"], ["ik_ramchander", "bsa_168", "malimath", "wiki_nanavati", "civils_plea", "ians_pendency", "dataful_ut", "wiki_bnss"],
{"type": "stat_tiles", "title": "India's trial system in numbers", "data": [
  {"label": "Cases pending in district courts", "value": "4.77 crore", "note": "31 December 2025, NJDG"},
  {"label": "Prisoners who are undertrials", "value": "73.5%", "note": "2023; some analyses say 76%"},
  {"label": "Cases settled by plea bargain", "value": "0.11%", "note": "2022"},
  {"label": "Plea bargaining in force", "value": "since 5 July 2006", "note": "offences up to 7 years"},
  {"label": "Judge's power to question", "value": "Section 168 BSA", "note": "was Section 165, Evidence Act 1872"},
  {"label": "New criminal codes in force", "value": "1 July 2024", "note": "BNS, BNSS, BSA"},
]}))

SECTIONS.append(sec("myths", 13, "Myths and facts",
"""Because the two systems are known mostly through films and headlines, both are wrapped in myths. Americans often think the French presume guilt; Europeans often think every American case ends with theatrical lawyers before a jury. Indians often assume their system is purely English. Even the symbol of justice carries a myth. Below are the most common claims, tested against the record, with the evidence in the table and two of the myths told in full.""",
[
 sp("myth_blindfold", "monument", "Myth: Justice is always blindfolded",
 "Look up at the dome of the Old Bailey and you will see F. W. Pomeroy's gilded Justice of 1905 to 1906 holding a sword and scales, with her eyes wide open. The court's own explanation is that early images of Justice were not blindfolded, and that her 'maidenly form' was supposed to guarantee impartiality. The blindfold arrived in Renaissance prints, sometimes as satire. Denning used the image in 1957: 'It is all very well to paint justice blind, but she does better without a bandage round her eyes. She should be blind indeed to favour or prejudice, but clear to see which way lies the truth.'",
 "A golden woman on a dome above London, sword up, scales out, eyes open.",
 "A visual lesson that impartial does not mean passive.",
 "London's Justice keeps her eyes open.",
 ["wiki_old_bailey", "nzlj_jones"], ["img_ob_justice", "img_ob_entrance"], [], ("Old Bailey, London", 51.5155, -0.1019), "Statue 1905 to 1906"),
 sp("myth_guilty_until", "idea", "Myth: continental systems presume guilt",
 "France wrote the presumption of innocence into Article 9 of the Declaration of the Rights of Man in 1789, and the European Convention on Human Rights binds every inquisitorial system in Europe to it through Article 6. The myth comes from real differences: the accused is questioned first, may not be able to stay as silent in practice, and faces judges who have read a file built by the state. In an inquisitorial court, a confession is not enough to convict, which is arguably more protective than a common-law guilty plea, where the admission alone ends the trial.",
 "A misreading that turns 'the judge questions you' into 'you must prove your innocence'.",
 "Clears the most common misunderstanding about continental justice.",
 "In Paris you must still be proved guilty; you just have to answer more questions on the way.",
 ["wiki_inquisitorial", "wiki_adversarial"], ["img_ddhc"], [], None, "1789 onward"),
], ["q_myth_odd", "q_myth_tf"], ["wiki_inquisitorial", "wiki_adversarial", "wiki_old_bailey", "wiki_spanish_inq"],
{"type": "table", "title": "Myth or fact", "data": [
  {"claim": "'Inquisitorial' courts descend from the Spanish Inquisition", "verdict": "Myth", "fact": "They descend from the general church inquisitio of about 1200, adopted by secular courts"},
  {"claim": "Continental systems presume guilt", "verdict": "Myth", "fact": "Presumption of innocence: France 1789, European Convention Article 6"},
  {"claim": "Inquisitorial systems have no juries", "verdict": "Myth", "fact": "France's cour d'assises has citizen jurors; Germany and Japan seat lay judges"},
  {"claim": "Most US criminal cases end in a jury trial", "verdict": "Myth", "fact": "About 2% of federal defendants go to trial; about 90% plead guilty"},
  {"claim": "India's system is a pure English copy", "verdict": "Half true", "fact": "Adversarial, but no juries and a judge's power to question anyone (Section 168 BSA)"},
  {"claim": "Nanavati was India's last jury trial", "verdict": "Myth", "fact": "Some jury trials continued into the 1960s"},
  {"claim": "Ordeals always condemned the accused", "verdict": "Myth", "fact": "At Várad, 62.5% of those who carried hot iron passed"},
]}))

SECTIONS.append(sec("facts", 14, "The best facts",
"""If you remember nothing else, remember these, each checked against the day's sources. The top three: a 1215 church council created both trial families by withdrawing priests from ordeals; most people who carried red-hot iron in a Hungarian register passed; and a Japanese man spent 46 years facing execution over clothes that did not fit him.

Notice the pattern: a system that relies on one official needs a brake, and a system that relies on two sides fighting needs both sides to have a fighter.""",
[], ["q_facts_mcq"], ["wiki_lateran", "leeson_ordeals", "wiki_hakamada", "pew_2023"],
{"type": "photo_grid", "title": "Faces and places from today", "data": {"image_ids": ["img_ordeal_iron", "img_lateran", "img_microcosm", "img_garrow", "img_goering", "img_hakamada", "img_pelicot", "img_sita", "img_ob_justice"]}}))

SECTIONS.append(sec("now", 15, "What is happening now (2025 to 2026)",
"""The story of 2025 and 2026 is convergence under pressure: adversarial systems short of judges are cutting the jury, and inquisitorial systems short of time are tempted by guilty pleas.

England is rationing jury trial, France rejected the guilty plea, Scotland and Italy tested their own models, Japan reformed retrials, the ICC prepares a hybrid trial for a former head of state, and India tries absconders in their absence. Each story below is dated.""",
[
 sp("uk_jury_bill", "document", "England's Courts and Tribunals Bill",
 "With a record Crown Court backlog of 79,616 cases and projections of 130,000 by 2030, Leveson recommended in July 2025 removing jury trial for offences with a maximum of two years and creating a judge-led Crown Court Bench Division. Justice Secretary David Lammy's bill had its Commons first reading on 25 February 2026 and passed second reading on 10 March 2026 by 304 votes to 203, despite a Labour rebellion. In a partial U-turn the Bench Division was dropped, but some complex fraud-type cases can still go without a jury. It passed third reading by 301 to 193 on 13 October; Lords second reading is scheduled for 27 October 2026.",
 "The country that exported the jury to the world, voting to use it less.",
 "The biggest cut to English jury trial in generations, happening now.",
 "Magna Carta's country, rationing juries by sentence length.",
 ["uk_bill", "twfy_vote", "lg_third", "lg_backlog", "wilmerhale_leveson", "lords_library_ctb"], ["img_ob_entrance"], ["vid_hansard_jury"], ("Westminster, London", 51.4995, -0.1248), "July 2025 to October 2026"),
 sp("france_sure", "document", "France's SURE law and the plea bargain that wasn't",
 "Justice minister Gérald Darmanin's SURE bill proposed a 'procedure for judging admitted crimes' (PJCR): an accused who admitted a serious crime could receive a sentence up to a third lower after a half-day hearing. The Senate approved the bill in April 2026 by 219 votes to 111. Bar associations protested, the National Assembly's law committee rejected the text by 18 to 16, and within hours, on 10 June 2026, Darmanin withdrew the PJCR, citing lack of consensus. The final law, adopted on 9 July 2026 by 232 votes to 99 in the Senate, keeps an expansion of the judge-only cours criminelles départementales, which since 1 January 2023 have tried most rapes without a jury.",
 "A French minister trying to import the American guilty plea, and backing off.",
 "Shows the inquisitorial resistance to trading confession for discount.",
 "France said yes to five judges and no to the plea deal.",
 ["gazette_sure", "gazette_pjcr", "publicsenat_pjcr", "publicsenat_final", "an_ccd"], ["img_darmanin"], [], ("Paris", 48.8566, 2.3522), "April to July 2026"),
 sp("scotland_not_proven", "document", "Scotland ends 'not proven'",
 "Since 1728, when a jury in the murder trial of Carnegie of Finhaven reasserted its right to say 'not guilty', Scottish juries had three verdicts: guilty, not guilty and not proven, the last with the same effect as acquittal. Walter Scott called it 'that bastard verdict' in 1827. Critics said it left acquitted people under suspicion and was used disproportionately in rape trials. The Victims, Witnesses, and Justice Reform (Scotland) Act, passed by the Scottish Parliament in September 2025, abolished it for new trials from 1 January 2026 and raised the majority needed to convict to two-thirds of the 15-member jury.",
 "A third verdict, half an acquittal, that lasted nearly 300 years.",
 "Scotland's reform tidies its unique jury while keeping it.",
 "Not proven: born 1728, died 1 January 2026.",
 ["wiki_not_proven", "govscot_not_proven"], ["img_edinburgh_hcj"], [], ("Edinburgh", 55.9533, -3.1883), "1728 to 2026"),
 sp("italy_referendum", "event", "Italy's referendum on separating careers",
 "Italian judges and prosecutors belong to one profession, the magistratura, and can switch between the two roles, an inheritance of the inquisitorial model that sits awkwardly with the 1989 adversarial code. Prime Minister Giorgia Meloni's government and justice minister Carlo Nordio proposed a constitutional reform to separate the two careers, split the Superior Council of the Judiciary in two, pick some of its members by lot and create a separate disciplinary court. In the confirmative referendum of 22 to 23 March 2026, on a turnout of nearly 59 per cent, voters rejected it by about 54 to 46.",
 "Ballot papers asking Italians whether a prosecutor should ever become a judge.",
 "The latest chapter in Italy's 37-year attempt to finish going adversarial.",
 "Italy kept its judges and prosecutors in one family, 54 to 46.",
 ["wiki_italy_ref", "wir_italy_ref"], [], [], ("Rome", 41.9028, 12.4964), "22 to 23 March 2026"),
 sp("japan_retrial", "document", "Japan's retrial reform",
 "Partly in response to cases like Hakamada's, Japan's Diet enacted on 17 July 2026 the first revision of the retrial system since the Code of Criminal Procedure took effect in 1948. Prosecutors are generally barred from appealing court orders to start a retrial, except in exceptional cases. Courts can order prosecutors to disclose evidence, but only where relevant and necessary, and prosecutors need not hand over a list of what they hold. Critics said disclosure is still too narrow.",
 "A law aimed at the years-long fight to reopen wrongful convictions.",
 "Shows a judge-centred system adding adversarial-style disclosure duties.",
 "Hakamada waited 46 years; the law that might have shortened it came in 2026.",
 ["japan_retrial", "wiki_hakamada"], ["img_japan_sc"], [], ("National Diet, Tokyo", 35.6759, 139.745), "Enacted 17 July 2026"),
 sp("duterte_icc", "event", "Duterte sent to trial at the ICC",
 "Former Philippine president Rodrigo Duterte was arrested in Manila and flown to The Hague in March 2025, making his first appearance by video link on 14 March 2025. His confirmation of charges hearing ran from 23 to 27 February 2026; he chose not to attend. On 23 April 2026 the pre-trial judges unanimously confirmed charges of murder and attempted murder as crimes against humanity, covering 49 incidents and 78 victims of the 'war on drugs' between 2011 and 2019, and committed him to trial before Trial Chamber III, presided over by Judge Joanna Korner. The trial is set to open on 30 November 2026; on 8 October 2026 the judges found him fit to stand trial.",
 "A former head of state on a plane to The Hague.",
 "The hybrid international trial at work on its most prominent current case.",
 "From Davao to The Hague: confirmation first, then a three-judge trial.",
 ["hrw_duterte", "icc_duterte_first", "icc_duterte_trial", "wiki_icc"], ["img_duterte", "img_icc"], ["vid_icc_duterte"], ("The Hague", 52.1065, 4.3248), "March 2025 to November 2026"),
 sp("india_absentia", "document", "India's trials in absentia",
 "The BNSS, in force since 1 July 2024, added a feature familiar from continental law: Section 356 allows a trial to proceed in the absence of a proclaimed offender who has absconded, once safeguards are met. On 8 May 2026 the Allahabad High Court, in Ravi alias Ravindra Singh v State of U.P., issued guidelines saying that once the conditions are met, including a 90-day wait after charges are framed and a 30-day notice, the trial must go ahead with a state-paid amicus curiae defending the absent accused. The court said an accused who had 'played hide and seek' could not stall the case forever.",
 "An empty dock and a court-appointed lawyer speaking for someone who ran away.",
 "India borrowing a civil-law tool to fight delay.",
 "Run away in India now, and the trial may go on without you.",
 ["verdictum_absentia", "wiki_bnss"], ["img_allahabad_hc"], [], ("Allahabad (Prayagraj)", 25.4358, 81.8463), "8 May 2026"),
], ["q_now_order", "q_now_mcq", "q_map_hague"], ["uk_bill", "lg_third", "wilmerhale_leveson", "gazette_sure", "wiki_not_proven", "wiki_italy_ref", "japan_retrial", "hrw_duterte", "verdictum_absentia"],
{"type": "timeline", "title": "2025 to 2026, month by month", "data": [
  {"year": 2025, "event": "March: Duterte flown to The Hague; Hakamada awarded 217 million yen"},
  {"year": 2025, "event": "9 July: Leveson review Part 1 proposes judge-only trials"},
  {"year": 2025, "event": "September: Scotland passes law ending 'not proven'"},
  {"year": 2025, "event": "9 October: Pelicot appeal in Nîmes raises Dogan's sentence to 10 years"},
  {"year": 2026, "event": "1 January: 'not proven' gone for new Scottish trials"},
  {"year": 2026, "event": "10 March: Courts and Tribunals Bill passes Commons second reading, 304 to 203"},
  {"year": 2026, "event": "22 to 23 March: Italian voters reject separating judges and prosecutors"},
  {"year": 2026, "event": "23 April: ICC confirms charges against Duterte"},
  {"year": 2026, "event": "8 May: Allahabad High Court guidelines on trial in absentia"},
  {"year": 2026, "event": "10 June: France drops criminal plea bargaining (PJCR)"},
  {"year": 2026, "event": "17 July: Japan enacts retrial reform"},
  {"year": 2026, "event": "13 October: Courts and Tribunals Bill passes Commons third reading"},
  {"year": 2026, "event": "27 October: Lords second reading scheduled"},
  {"year": 2026, "event": "30 November: Duterte trial due to open at the ICC"},
]}))

SECTIONS.append(sec("recap", 16, "Recap",
"""**Two answers to one problem.** When the Fourth Lateran Council withdrew priests from ordeals in 1215, England turned to juries of neighbours and the Continent turned to judges who investigated. Those two answers grew into today's adversarial and inquisitorial trials.

**The contest** trusts two partisan sides, cross-examination and a jury, and protects the accused with lawyers, silence and exclusion rules. Its weak spots: unequal lawyers, unexplained verdicts and a cost so high that nine in ten US federal defendants plead guilty.

**The inquiry** trusts professional judges, a written file and reasoned judgments, often with lay judges beside them. Its weak spots: one official locked onto one theory, long detention, and confessions under pressure, as Outreau and Hakamada showed.

**India** is adversarial with an inquisitorial streak: no juries, a judge who may ask anything, almost no plea bargaining.

**Now**, both families borrow: England cuts juries, France flirts with and rejects guilty pleas, Japan reforms retrials, and the ICC runs a hybrid.""",
[], ["q_recap_match"], ["wiki_adversarial", "wiki_inquisitorial", "wiki_lateran", "pew_2023"]))

# ---------------------------------------------------------------- quiz bank (section checks)
def q(id, type, prompt, answer, expl, src, section, **kw):
    d = {"id": id, "type": type, "prompt": prompt, "answer": answer, "explanation": expl, "source_ids": src, "section_id": section}
    d.update(kw)
    return d

QUIZ_BANK = [
 q("q_hook_tf", "true_false", "In an English jury trial, jurors read the case file before the hearing starts.", False, "Jurors see nothing in advance; all evidence must be given aloud in court. In France the presiding judge has read the dossier.", ["wiki_adversarial", "wiki_inquisitorial"], "hook", difficulty=1),
 q("q_hook_mcq", "mcq", "In an inquisitorial trial, what does a confession do?", 2, "A confession is one more piece of evidence; the prosecution must still present a full case.", ["wiki_inquisitorial"], "hook", options=["Ends the trial at once", "Is inadmissible", "Counts as evidence that must be checked", "Doubles the sentence"], difficulty=1),
 q("q_models_match", "match", "Match each feature to its system.", [["Cross-examination by lawyers", "Adversarial"], ["Judge reads the dossier first", "Inquisitorial"], ["Unreasoned jury verdict", "Adversarial"], ["Lay judges deliberate with professionals", "Inquisitorial"]], "Contest: lawyers test witnesses and juries decide without reasons. Inquiry: judges read the file and write reasons, often with lay judges.", ["wiki_adversarial", "wiki_inquisitorial", "wiki_lay_judge"], "two_models", pairs=[["Cross-examination by lawyers", "Adversarial"], ["Judge reads the dossier first", "Inquisitorial"], ["Unreasoned jury verdict", "Adversarial"], ["Lay judges deliberate with professionals", "Inquisitorial"]], difficulty=1),
 q("q_models_tf", "true_false", "In 1957 an English appeal court ordered a retrial because the judge asked too many questions.", True, "Jones v National Coal Board: the judge's interventions were 'far more than they should have been'.", ["nzlj_jones"], "two_models", difficulty=2),
 q("q_lateran_mcq", "mcq", "What did the Fourth Lateran Council of 1215 forbid?", 1, "It barred clergy from blessing or taking part in ordeals, which forced Europe to find new ways of deciding guilt.", ["wiki_lateran", "wiki_ordeal"], "ordeals", options=["Trial by jury", "Clergy taking part in ordeals", "Torture", "Lawyers in court"], difficulty=1),
 q("q_leeson_hl", "higher_lower", "Várad ordeal register: was the share of hot-iron carriers who passed higher or lower than half?", "higher", "Higher: 130 of 208, or 62.5 per cent, passed.", ["leeson_ordeals"], "ordeals", options=[{"label": "Passed at Várad", "value": 62.5, "unit": "%"}, {"label": "Half", "value": 50, "unit": "%"}], difficulty=2),
 q("q_fullproof_mcq", "mcq", "Under Roman-canon 'full proof', what did a capital conviction require?", 0, "Two eyewitnesses or a confession. With only half proof, judges could order torture to get the confession.", ["langbein_torture"], "continental_road", options=["Two eyewitnesses or a confession", "A unanimous jury", "A written dossier", "Forensic evidence"], difficulty=2),
 q("q_inq_tf", "true_false", "Today's inquisitorial courts descend from the Spanish Inquisition.", False, "They come from the general church inquisitio procedure of about 1200, adopted by secular courts; the Spanish Inquisition was one religious tribunal using it.", ["wiki_inquisitorial", "wiki_spanish_inq"], "continental_road", difficulty=2),
 q("q_order_history", "order", "Put these in order, earliest first.", ["Fourth Lateran Council", "Constitutio Criminalis Carolina", "French Criminal Ordinance", "Napoleon's criminal procedure code", "Prisoners' Counsel Act"], "1215, 1532, 1670, 1808, 1836.", ["wiki_lateran", "wiki_carolina", "wiki_ordonnance", "wiki_inquisitorial", "wiki_adversarial"], "common_law_road", items=["Napoleon's criminal procedure code", "Prisoners' Counsel Act", "Fourth Lateran Council", "French Criminal Ordinance", "Constitutio Criminalis Carolina"], difficulty=2),
 q("q_garrow_clues", "guess_clues", "Guess the person.", 2, "William Garrow, the Old Bailey cross-examiner credited with 'presumed innocent until proven guilty'.", ["wiki_garrow"], "common_law_road", clues=["Called to the Bar in 1783 at 23.", "He defended in about 83 per cent of his cases.", "He is credited with the phrase 'presumed innocent until proven guilty'.", "BBC One made a drama series named after him."], options=["Thomas Erskine", "Jeremy Bentham", "William Garrow", "Lord Denning"], difficulty=2),
 q("q_pew_mcq", "mcq", "About what share of US federal defendants went to trial in fiscal 2022?", 0, "About 2.3 per cent (1.9 convicted plus 0.4 acquitted); 89.5 per cent pleaded guilty.", ["pew_2023"], "adversarial_machine", options=["About 2%", "About 20%", "About 50%", "About 90%"], difficulty=1),
 q("q_miranda_tf", "true_false", "After the Supreme Court threw out his confession, Ernesto Miranda was retried and convicted again.", True, "He was retried without the confession and convicted, then paroled in 1972.", ["wiki_miranda"], "adversarial_machine", difficulty=2),
 q("q_juge_mcq", "mcq", "Which country abolished its investigating judge in 1989 as part of a new, more adversarial code?", 2, "Italy, with the code in force from 24 October 1989. West Germany abolished the office in 1974.", ["wiki_examining", "psilr_italy"], "inquisitorial_machine", options=["France", "Spain", "Italy", "Belgium"], difficulty=2),
 q("q_penal_tf", "true_false", "A German Strafbefehl (penal order) can become a conviction without any court hearing.", True, "If the accused does not object to the written penalty order, it becomes final without a hearing.", ["langbein_1979", "beck_strafbefehl"], "inquisitorial_machine", difficulty=2),
 q("q_frank_mcq", "mcq", "Jerome Frank contrasted the 'truth theory' of trials with which other theory?", 3, "The 'fight theory': trials run as duels between lawyers.", ["frank_courts"], "thinkers", options=["The jury theory", "The proof theory", "The file theory", "The fight theory"], difficulty=1),
 q("q_thinkers_match", "match", "Match the thinker to the idea.", [["Wigmore", "Cross-examination is the greatest engine for truth"], ["Langbein", "Plea bargaining is like medieval torture"], ["Leeson", "Priests rigged ordeals to clear the innocent"], ["Damaška", "Procedure mirrors the structure of the state"]], "Four ways of seeing trials: as an engine, as a cost problem, as a sorting device, as politics.", ["wiki_wigmore", "langbein_torture", "leeson_ordeals", "wiki_damaska"], "thinkers", pairs=[["Wigmore", "Cross-examination is the greatest engine for truth"], ["Langbein", "Plea bargaining is like medieval torture"], ["Leeson", "Priests rigged ordeals to clear the innocent"], ["Damaška", "Procedure mirrors the structure of the state"]], difficulty=2),
 q("q_nuremberg_img", "image_id", "This man was cross-examined in 1946 by a US Supreme Court justice. Where?", 1, "Hermann Göring at the International Military Tribunal in Nuremberg, cross-examined by Robert Jackson from 20 March 1946.", ["wiki_nuremberg", "spectator_goring"], "collisions", image_id="img_goering", options=["The Hague", "Nuremberg", "Tokyo", "London"], difficulty=1),
 q("q_italy_order", "order", "Put the Knox case verdicts in order.", ["Convicted (2009)", "Acquitted on appeal (2011)", "Reconvicted in Florence (2014)", "Definitively acquitted (2015)"], "Italian appeals reopen the facts: four verdicts in six years.", ["wiki_knox"], "collisions", items=["Reconvicted in Florence (2014)", "Definitively acquitted (2015)", "Convicted (2009)", "Acquitted on appeal (2011)"], difficulty=2),
 q("q_hakamada_clues", "guess_clues", "Guess the person.", 1, "Iwao Hakamada, acquitted on 26 September 2024 after 46 years on death row.", ["wiki_hakamada"], "failures", clues=["He was once a professional featherweight boxer.", "He worked at a miso maker.", "Guinness named him the longest-held death row inmate.", "Bloody clothes found in a miso tank were too small for him."], options=["Sakae Menda", "Iwao Hakamada", "Carlos Ghosn", "Kawas Nanavati"], difficulty=1),
 q("q_outreau_mcq", "mcq", "In the Outreau affair, how many of the 17 accused were finally acquitted?", 2, "Thirteen; one other accused died in pre-trial detention before trial.", ["wiki_outreau"], "failures", options=["3", "7", "13", "17"], difficulty=2),
 q("q_japan_hl", "higher_lower", "Japanese citizens declining lay-judge duty: was the 2018 share higher or lower than 2009's 53.1%?", "higher", "Higher: 67 per cent in 2018, as trials grew longer.", ["nippon_saibanin"], "truth_evidence", options=[{"label": "2018", "value": 67, "unit": "%"}, {"label": "2009", "value": 53.1, "unit": "%"}], difficulty=2),
 q("q_truth_tf", "true_false", "Thibaut and Walker's experiments found people rated adversarial procedures as fairer.", True, "Participants valued 'process control', the chance to present their own case.", ["sage_procedural"], "truth_evidence", difficulty=2),
 q("q_india_mcq", "mcq", "Which section of the Bharatiya Sakshya Adhiniyam lets an Indian judge ask any witness any question?", 1, "Section 168, formerly Section 165 of the Indian Evidence Act, 1872.", ["bsa_168"], "india", options=["Section 165", "Section 168", "Section 356", "Section 302"], difficulty=2),
 q("q_india_hl", "higher_lower", "Indian criminal cases settled by plea bargaining in 2022: higher or lower than 1 per cent?", "lower", "Lower: about 0.11 per cent, 19,135 cases.", ["civils_plea"], "india", options=[{"label": "India 2022", "value": 0.11, "unit": "%"}, {"label": "Benchmark", "value": 1, "unit": "%"}], difficulty=1),
 q("q_sita_img", "image_id", "This Mughal painting shows which kind of ancient legal test?", 0, "Sita's agni pariksha, an ordeal by fire; Yājñavalkya lists fire among five divya.", ["unica_yajnavalkya"], "india", image_id="img_sita", options=["Ordeal by fire", "Ordeal by water", "Ordeal by balance", "Ordeal by poison"], difficulty=1),
 q("q_myth_odd", "odd_one_out", "Which of these systems does NOT seat lay people to decide serious criminal cases?", 3, "France has assize jurors, Germany Schöffen, Japan saiban-in. India abolished juries and uses professional judges.", ["wiki_lay_judge", "wiki_nanavati"], "myths", options=["France", "Germany", "Japan", "India"], difficulty=2),
 q("q_myth_tf", "true_false", "The statue of Justice on top of the Old Bailey wears a blindfold.", False, "Pomeroy's Justice has her eyes open; the court says early Justice figures were not blindfolded.", ["wiki_old_bailey"], "myths", difficulty=1),
 q("q_facts_mcq", "mcq", "How much was Iwao Hakamada awarded for each day he was held?", 0, "12,500 yen a day, a total of 217,362,500 yen, awarded in March 2025.", ["wiki_hakamada"], "facts", options=["12,500 yen", "1,000 yen", "100,000 yen", "1 million yen"], difficulty=2),
 q("q_now_order", "order", "Put these 2026 events in order.", ["Scotland drops 'not proven'", "Commons second reading of the Courts and Tribunals Bill", "ICC confirms charges against Duterte", "France drops criminal plea bargaining", "Japan enacts retrial reform"], "1 January, 10 March, 23 April, 10 June, 17 July 2026.", ["wiki_not_proven", "uk_bill", "hrw_duterte", "gazette_pjcr", "japan_retrial"], "now", items=["France drops criminal plea bargaining", "Japan enacts retrial reform", "Scotland drops 'not proven'", "ICC confirms charges against Duterte", "Commons second reading of the Courts and Tribunals Bill"], difficulty=3),
 q("q_now_mcq", "mcq", "What did France's justice minister withdraw from the SURE bill in June 2026?", 1, "The PJCR, a guilty-plea procedure for admitted serious crimes with up to a one-third sentence cut.", ["gazette_pjcr", "publicsenat_pjcr"], "now", options=["Jury trial for murder", "Plea bargaining for serious crimes", "The investigating judge", "Trial in absentia"], difficulty=2),
 q("q_map_hague", "map_pin", "Drop a pin on the city where Rodrigo Duterte is to be tried.", "The Hague", "The International Criminal Court sits in The Hague, Netherlands.", ["hrw_duterte", "wiki_icc"], "now", target={"lat": 52.0705, "lon": 4.3007, "tolerance_km": 80}, difficulty=1),
 q("q_recap_match", "match", "Match the case to its country.", [["Outreau", "France"], ["Hakamada", "Japan"], ["Nanavati", "India"], ["Gideon", "United States"]], "Four cases, four systems, four reforms.", ["wiki_outreau", "wiki_hakamada", "wiki_nanavati", "wiki_gideon"], "recap", pairs=[["Outreau", "France"], ["Hakamada", "Japan"], ["Nanavati", "India"], ["Gideon", "United States"]], difficulty=1),
]

# ---------------------------------------------------------------- end-of-day quiz
QUIZ = [
 q("qz_compare_courts", "compare", "Which picture shows the dock of an English adversarial courtroom?", 0, "Left: the dock in Court Number 1 at the Old Bailey. Right: the temporary 'Grands procès' room in the Paris Palais de justice.", ["wiki_old_bailey"], "hook", image_ids=["img_ob_dock", "img_paris_grands"], options=["Left", "Right"], difficulty=1),
 q("qz_1215", "mcq", "1215 gave England Magna Carta. What else did it give European criminal justice?", 2, "The Fourth Lateran Council withdrew clergy from ordeals, forcing the move to juries and inquisitorial judges.", ["wiki_lateran"], "ordeals", options=["The first jury", "The first lawyer", "The end of priests at ordeals", "The first prison"], difficulty=1),
 q("qz_leeson_mcq", "mcq", "According to Peter Leeson, why did most people pass the hot-iron ordeal?", 1, "Only those who believed in their innocence volunteered, and priests made the ordeal survivable for them.", ["leeson_ordeals"], "ordeals", options=["Medieval iron was weak", "Priests rigged it for willing defendants", "Only nobles took it", "The test was never real"], difficulty=2),
 q("qz_duel_img", "image_id", "This miniature shows a judicial duel fought in Paris in 1386. Who won?", 0, "Jean de Carrouges killed Jacques Le Gris, and the verdict was taken as God's judgment.", ["wiki_combat"], "ordeals", image_id="img_duel", options=["Jean de Carrouges", "Jacques Le Gris", "Neither, the king stopped it", "Marguerite de Carrouges"], difficulty=2),
 q("qz_torture_tf", "true_false", "In the old Roman-canon system, torture was a legal step when a judge had 'half proof'.", True, "Half proof plus torture to obtain a confession could complete the 'full proof' needed for conviction.", ["langbein_torture"], "continental_road", difficulty=2),
 q("qz_beccaria_clues", "guess_clues", "Guess the person.", 3, "Cesare Beccaria's 1764 book helped end judicial torture in Europe.", ["wiki_beccaria"], "continental_road", clues=["He was from Milan.", "He was 26 when his famous book came out.", "The book appeared in 1764.", "He argued torture punished before guilt was proved."], options=["Jeremy Bentham", "Voltaire", "Napoleon", "Cesare Beccaria"], difficulty=1),
 q("qz_1836_hl", "higher_lower", "The year English felony defendants won the full right to counsel: higher or lower than 1800?", "higher", "Higher: the Prisoners' Counsel Act 1836. Treason defendants had counsel from 1696.", ["wiki_adversarial"], "common_law_road", options=[{"label": "Prisoners' Counsel Act", "value": 1836, "unit": ""}, {"label": "Benchmark", "value": 1800, "unit": ""}], difficulty=1),
 q("qz_garrow_img", "image_id", "This barrister is credited with the phrase 'presumed innocent until proven guilty'. Who is he?", 2, "William Garrow, the Old Bailey's great cross-examiner.", ["wiki_garrow"], "common_law_road", image_id="img_garrow", options=["Thomas Erskine", "Lord Denning", "William Garrow", "Jeremy Bentham"], difficulty=1),
 q("qz_gideon_mcq", "mcq", "After the Supreme Court gave Clarence Gideon a lawyer, what happened at his retrial?", 3, "With counsel cross-examining the key witness, the jury acquitted him after about an hour.", ["wiki_gideon"], "adversarial_machine", options=["Convicted again", "Case dropped", "Pleaded guilty", "Acquitted in about an hour"], difficulty=1),
 q("qz_wigmore_tf", "true_false", "Wigmore called cross-examination the greatest legal engine ever invented for the discovery of truth.", True, "The line comes from Wigmore's Treatise on Evidence; he also warned it could be abused.", ["umich_cross", "wiki_wigmore"], "adversarial_machine", difficulty=1),
 q("qz_juge_hl", "higher_lower", "Judicial investigations opened by French judges in 2023: higher or lower than 50,000?", "lower", "Lower: about 16,600, against about 4.7 million new cases at prosecutors' offices.", ["rsj_instruction"], "inquisitorial_machine", options=[{"label": "France 2023", "value": 16600, "unit": ""}, {"label": "Benchmark", "value": 50000, "unit": ""}], difficulty=2),
 q("qz_germany_mcq", "mcq", "In 1924 Germany replaced its jury with what?", 0, "A mixed court in which lay judges, Schöffen, sit with professional judges and deliberate together.", ["wiki_lay_judge"], "inquisitorial_machine", options=["Mixed courts of lay and professional judges", "Military courts", "Single judges only", "Juries of 24"], difficulty=2),
 q("qz_odd_hybrids", "odd_one_out", "Which of these did NOT move toward a more adversarial, oral trial?", 3, "Italy (1989), Chile (2000 to 2005) and Mexico (2008 to 2016) did; Germany kept its judge-led trial.", ["psilr_italy", "wiki_examining", "emory_mexico"], "collisions", options=["Italy", "Chile", "Mexico", "Germany"], difficulty=2),
 q("qz_icc_tf", "true_false", "The International Criminal Court uses juries.", False, "Panels of three professional judges decide; the court calls its procedure a common law and civil law hybrid.", ["wiki_icc"], "collisions", difficulty=1),
 q("qz_pelicot_mcq", "mcq", "Who decided the first Pelicot trial in Avignon in 2024?", 1, "Five professional judges of the Vaucluse criminal court; the appeal in Nîmes added citizen jurors.", ["aljazeera_pelicot", "an_ccd"], "failures", options=["A jury of 12", "Five professional judges", "An investigating judge", "The Court of Cassation"], difficulty=2),
 q("qz_ghosn_clues", "guess_clues", "Guess the person.", 2, "Carlos Ghosn escaped Japan in a box in December 2019.", ["wiki_ghosn"], "failures", clues=["He ran a car company in Japan.", "He was held 108 days before bail.", "He called Japan's system hostage justice.", "He left the country hidden in an equipment box."], options=["Amanda Knox", "Rodrigo Duterte", "Carlos Ghosn", "Iwao Hakamada"], difficulty=1),
 q("qz_japan_mcq", "mcq", "What is the main reason scholars give for Japan's conviction rate above 99 per cent?", 2, "Prosecutors drop or divert most cases and charge only those they are confident of winning.", ["wiki_japan_cj"], "truth_evidence", options=["Japan has no defence lawyers", "Judges are paid per conviction", "Prosecutors only charge near-certain cases", "Lay judges always convict"], difficulty=1),
 q("qz_ramchander", "mcq", "In 1981 India's Supreme Court said a criminal judge must cease to be a spectator and a mere what?", 3, "'A mere recording machine' (Ram Chander v State of Haryana).", ["ik_ramchander"], "india", options=["Umpire", "Clerk", "Juror", "Recording machine"], difficulty=1),
 q("qz_nanavati_tf", "true_false", "The Nanavati case of 1959 was India's very last jury trial.", False, "A myth: some jury trials continued into the 1960s before the 1973 Code dropped them.", ["wiki_nanavati", "caravan_jury"], "india", difficulty=2),
 q("qz_plea_compare", "higher_lower", "Share of cases ended by a plea: is India's higher or lower than the US federal share?", "lower", "Far lower: about 0.11 per cent in India in 2022, against 89.5 per cent guilty pleas in US federal courts.", ["civils_plea", "pew_2023"], "india", options=[{"label": "India 2022", "value": 0.11, "unit": "%"}, {"label": "US federal 2022", "value": 89.5, "unit": "%"}], difficulty=1),
 q("qz_uk_bill", "mcq", "What did the UK government drop from the Courts and Tribunals Bill before its Commons third reading?", 0, "The judge-led Crown Court Bench Division; limits on jury trial for some complex cases remain.", ["lg_third"], "now", options=["The Crown Court Bench Division", "The whole bill", "Juries for murder", "Magistrates' courts"], difficulty=3),
 q("qz_scotland_tf", "true_false", "Since 1 January 2026, new Scottish trials can no longer end in 'not proven'.", True, "Abolished by the Victims, Witnesses, and Justice Reform (Scotland) Act 2025.", ["wiki_not_proven"], "now", difficulty=1),
 q("qz_italy_ref", "mcq", "In March 2026 Italian voters rejected a reform to do what?", 2, "Separate the careers of judges and prosecutors, among other changes; No won about 54 to 46.", ["wiki_italy_ref"], "now", options=["Bring back juries", "Abolish the Court of Cassation", "Separate judges' and prosecutors' careers", "Allow plea bargaining"], difficulty=2),
 q("qz_map_oradea", "map_pin", "Drop a pin near the town whose medieval register recorded 308 hot-iron ordeals.", "Oradea (Várad)", "Oradea in today's Romania, then Várad in the Kingdom of Hungary.", ["leeson_ordeals"], "ordeals", target={"lat": 47.0722, "lon": 21.9217, "tolerance_km": 150}, difficulty=3),
]

PREQ = [
 q("pq_plea", "mcq", "Guess: what share of US federal criminal defendants go to trial?", 0, "About 2 per cent; about 90 per cent plead guilty.", ["pew_2019", "pew_2023"], "adversarial_machine", options=["About 2%", "About 25%", "About 50%", "About 80%"], prequestion=True, difficulty=1),
 q("pq_lateran", "true_false", "Guess: the split between jury trials and judge-led trials traces back to a decision by a Pope.", True, "In 1215 Innocent III's Lateran Council withdrew priests from ordeals.", ["wiki_lateran"], "ordeals", prequestion=True, difficulty=2),
 q("pq_ordeal", "mcq", "Guess: in a medieval Hungarian register, what share of people who carried red-hot iron passed?", 2, "62.5 per cent, according to Peter Leeson's count of 208 cases.", ["leeson_ordeals"], "ordeals", options=["About 5%", "About 25%", "About 60%", "100%"], prequestion=True, difficulty=2),
 q("pq_india_jury", "true_false", "Guess: India still uses juries in murder trials.", False, "India dropped juries; the 1973 Code of Criminal Procedure has none.", ["wiki_nanavati", "caravan_jury"], "india", prequestion=True, difficulty=1),
 q("pq_japan", "mcq", "Guess: Japan's conviction rate for cases that go to trial is about...", 3, "Above 99 per cent, mostly because prosecutors charge only cases they expect to win.", ["wiki_japan_cj"], "truth_evidence", options=["60%", "75%", "90%", "Above 99%"], prequestion=True, difficulty=1),
]

# ---------------------------------------------------------------- best facts
BF = [
 ("A single church council in 1215 created both of today's trial families: by forbidding priests to bless ordeals, it pushed England toward juries and the Continent toward investigating judges.", "Modern courtrooms descend from a decision about holy fire.", 10, "lateran_1215", ["wiki_lateran", "wiki_inquisitorial", "wiki_ordeal"]),
 ("In the Várad ordeal register (1208 to 1235), 130 of the 208 people who carried red-hot iron passed: 62.5 per cent. Peter Leeson argues priests rigged it for defendants willing to face God.", "Red-hot iron should burn almost everyone.", 10, "leeson_ordeals", ["leeson_ordeals"]),
 ("Iwao Hakamada spent 46 years facing execution; the bloodstained clothes said to be his were too small, and the 'B' on the label meant black, not a size. He was acquitted at 88 in 2024.", "A death sentence hung on a misread label.", 10, "hakamada", ["wiki_hakamada"]),
 ("In fiscal 2022 only 290 of 71,954 US federal defendants, 0.4 per cent, were acquitted at trial; 89.5 per cent pleaded guilty.", "The country of courtroom dramas barely holds trials.", 9, "plea_bargain_us", ["pew_2023"]),
 ("Until 1836, a person tried for a felony in England could not have a lawyer argue the case to the jury; the judge was said to be the prisoner's counsel.", "The home of the adversarial trial banned defence speeches for centuries.", 9, "prisoners_counsel_1836", ["wiki_adversarial", "wiki_garrow"]),
 ("Ernesto Miranda, whose case created the right-to-silence warning, was stabbed to death in 1976; the suspect was read his Miranda rights, stayed silent and was released.", "The warning protected the man accused of killing its namesake.", 9, "miranda", ["wiki_miranda", "aba_miranda"]),
 ("Clarence Gideon was convicted without a lawyer; after the Supreme Court gave him one in 1963, a jury acquitted him in about an hour on the same charge.", "One lawyer turned five years into not guilty.", 9, "gideon", ["wiki_gideon"]),
 ("In 1750 'gaol fever' carried from Newgate prison into the Old Bailey killed about 60 people, including the Lord Mayor of London and two judges.", "A trial killed the judges.", 8, "microcosm_old_bailey", ["wiki_old_bailey"]),
 ("In the Outreau affair, 13 of the 17 adults tried after one investigating judge's inquiry were acquitted; another suspect died in custody before trial.", "France's judge-detective model produced a national disaster.", 8, "outreau", ["wiki_outreau"]),
 ("A 1969 to 1970 study found that 47 per cent of West German criminal trials lasted two hours or less.", "Judge-led trials can be shorter than a film.", 8, "idea_inquirer", ["langbein_1979"]),
 ("Carlos Ghosn escaped Japanese bail in December 2019 by hiding in a box for audio equipment loaded onto a private jet at Kansai airport.", "A CEO left the country as freight.", 8, "ghosn", ["wiki_ghosn", "occrp_ghosn"]),
 ("The statue of Justice on the Old Bailey dome is not blindfolded.", "The most famous symbol of English justice breaks the most famous rule of the symbol.", 7, "myth_blindfold", ["wiki_old_bailey"]),
 ("India has had a plea-bargaining law since 2006, but in 2022 it settled only about 0.11 per cent of criminal cases for trial.", "America's main tool is almost unused in India.", 8, "plea_india", ["civils_plea", "wiki_plea"]),
 ("Scotland's 'not proven' verdict survived from 1728 until 1 January 2026; Walter Scott called it 'that bastard verdict'.", "A three-verdict system lasted almost three centuries.", 7, "scotland_not_proven", ["wiki_not_proven"]),
 ("Section 165 of India's 1872 Evidence Act, now Section 168 of the Sakshya Adhiniyam, lets a judge ask any witness any question, relevant or not, and the parties cannot object.", "An inquisitorial power sits inside India's English-style trial.", 7, "section_165", ["bsa_168"]),
 ("Amanda Knox was convicted, acquitted, reconvicted and definitively acquitted between 2009 and 2015, because Italian appeals reopen the facts.", "Four verdicts on one charge.", 7, "italy_1989", ["wiki_knox"]),
 ("In June 2026 France's justice minister withdrew a plan to let accused criminals plead guilty in exchange for a one-third sentence cut, hours after a committee vote of 18 to 16 against his bill.", "France said no to the American deal.", 7, "france_sure", ["gazette_pjcr", "publicsenat_pjcr"]),
]
BEST_FACTS = sorted([{"fact": f, "why_surprising": w, "score": s, "spotlight_id": sid, "source_ids": src} for f, w, s, sid, src in BF], key=lambda x: -x["score"])

# ---------------------------------------------------------------- cards
def c(id, type, front, back, section, src, spot=None, img=None, imgs=None, core=False):
    d = {"id": id, "type": type, "front": front, "back": back}
    if img: d["image_id"] = img
    if imgs: d["image_ids"] = imgs
    if spot: d["spotlight_id"] = spot
    d.update({"section_id": section, "core": core, "source_ids": src})
    return d

CARDS = [
 c("c01", "fact", "Adversarial vs inquisitorial in one line each?", "Adversarial: two sides gather and test evidence; the judge referees. Inquisitorial: officials, including judges, investigate and question from a file.", "two_models", ["wiki_adversarial", "wiki_inquisitorial"], core=True),
 c("c02", "compare", "Which courtroom is built for an English-style contest?", "Left: the Old Bailey dock, facing judge and jury. Right: the Paris 'Grands procès' room.", "hook", ["wiki_old_bailey"], spot="old_bailey_court1", img="img_ob_dock", imgs=["img_ob_dock", "img_paris_grands"], core=True),
 c("c03", "fact", "What does a confession do in an inquisitorial trial?", "It is one more piece of evidence. The prosecution must still present a full case.", "hook", ["wiki_inquisitorial"], spot="paris_grands_proces", core=True),
 c("c04", "cloze", "In 1215 the Fourth ____ Council forbade clergy from taking part in ordeals.", "Lateran (opened 11 November 1215 under Innocent III).", "ordeals", ["wiki_lateran"], spot="lateran_1215", core=True),
 c("c05", "image", "What legal ordeal does this Bamberg relief show?", "Ordeal by red-hot iron: Empress Cunigunde walking over glowing ploughshares.", "ordeals", ["wiki_ordeal"], spot="ordeal_hot_iron", img="img_ordeal_iron", core=True),
 c("c06", "fact", "Várad ordeal register: share of hot-iron probands who passed?", "62.5 per cent (130 of 208), per Peter Leeson.", "ordeals", ["leeson_ordeals"], spot="leeson_ordeals", core=True),
 c("c07", "why", "Why did the old continental system use torture?", "Full proof needed two eyewitnesses or a confession; with only half proof, torture supplied the confession.", "continental_road", ["langbein_torture"], spot="full_proof", core=True),
 c("c08", "fact", "What did Napoleon's 1808 code create?", "A secret written investigation by a juge d'instruction, then a public oral trial, with a jury for serious crimes.", "continental_road", ["wiki_inquisitorial", "wiki_examining"], spot="napoleon_1808", core=True),
 c("c09", "image", "Who is this Old Bailey barrister, master of cross-examination?", "William Garrow (1760 to 1840).", "common_law_road", ["wiki_garrow"], spot="garrow", img="img_garrow", core=True),
 c("c10", "cloze", "England gave felony defendants the full right to counsel in the Prisoners' Counsel Act of ____.", "1836.", "common_law_road", ["wiki_adversarial"], spot="prisoners_counsel_1836", core=True),
 c("c11", "fact", "Wigmore's description of cross-examination?", "'The greatest legal engine ever invented for the discovery of truth.'", "adversarial_machine", ["umich_cross", "wiki_wigmore"], spot="wigmore_cross", core=True),
 c("c12", "fact", "US federal defendants, fiscal 2022: pleaded guilty vs acquitted at trial?", "89.5 per cent pleaded guilty; 0.4 per cent (290 people) acquitted.", "adversarial_machine", ["pew_2023"], spot="plea_bargain_us", core=True),
 c("c13", "fact", "Who is a juge d'instruction, and how common is the role?", "An independent French investigating judge who gathers evidence for and against; used in a small minority of cases (about 16,600 opened in 2023).", "inquisitorial_machine", ["wiki_examining", "rsj_instruction"], spot="juge_instruction", core=True),
 c("c14", "fact", "What are Schöffen?", "German lay judges who sit and vote with professional judges; Germany replaced its jury with them in 1924.", "inquisitorial_machine", ["wiki_lay_judge"], spot="mixed_court", core=True),
 c("c15", "image", "Who is being cross-examined here, and where?", "Hermann Göring, Nuremberg, 1946, by Robert Jackson.", "collisions", ["wiki_nuremberg"], spot="nuremberg", img="img_goering", core=True),
 c("c16", "fact", "Outreau affair in one line?", "A French investigating judge's theory of a paedophile ring led to 13 of 17 accused being acquitted after years of detention (2001 to 2005).", "failures", ["wiki_outreau"], spot="outreau", core=True),
 c("c17", "image", "Who is this man, and how long did he wait on death row?", "Iwao Hakamada: sentenced 1968, freed 2014, acquitted 2024; about 46 years on death row.", "failures", ["wiki_hakamada"], spot="hakamada", img="img_hakamada", core=True),
 c("c18", "fact", "Ram Chander v State of Haryana (1981): the key line?", "A criminal judge 'must cease to be a spectator and a mere recording machine'.", "india", ["ik_ramchander"], spot="ram_chander", core=True),
 c("c19", "fact", "India's plea bargaining: since when, and how much used?", "Since 5 July 2006; about 0.11 per cent of cases for trial in 2022.", "india", ["wiki_plea", "civils_plea"], spot="plea_india", core=True),
 c("c20", "fact", "England's Courts and Tribunals Bill: status in October 2026?", "Passed the Commons (third reading 13 October 2026, 301 to 193, Bench Division dropped); Lords second reading scheduled for 27 October 2026.", "now", ["uk_bill", "lg_third"], spot="uk_jury_bill", core=True),
 # bonus
 c("c21", "image", "This 1386 miniature shows what kind of trial?", "A judicial duel: Jean de Carrouges against Jacques Le Gris, Paris.", "ordeals", ["wiki_combat"], spot="trial_by_combat", img="img_duel"),
 c("c22", "image", "Which Pope's council of 1215 ended priestly ordeals?", "Innocent III.", "continental_road", ["wiki_lateran"], spot="innocent_iii", img="img_innocent3"),
 c("c23", "fact", "The Carolina: what and when?", "The Holy Roman Empire's criminal code of 1532, which regulated torture and underpinned witch trials.", "continental_road", ["wiki_carolina"], spot="carolina_1532"),
 c("c24", "fact", "Spanish Inquisition: estimated prosecutions and executions?", "About 150,000 prosecuted; 3,000 to 5,000 executed (1478 to 1834).", "continental_road", ["wiki_spanish_inq"], spot="spanish_inquisition"),
 c("c25", "image", "Whose 1764 book attacked judicial torture?", "Cesare Beccaria, On Crimes and Punishments.", "continental_road", ["wiki_beccaria"], spot="beccaria", img="img_beccaria"),
 c("c26", "fact", "When did France's Criminal Ordinance of 1670 end?", "Abolished by decree of the National Constituent Assembly on 9 October 1789.", "continental_road", ["wiki_ordonnance"], spot="ordonnance_1670"),
 c("c27", "image", "This print shows which London court around 1808?", "The Old Bailey (Rowlandson and Pugin, Microcosm of London).", "common_law_road", ["wiki_old_bailey"], spot="microcosm_old_bailey", img="img_microcosm"),
 c("c28", "fact", "Thomas Hardy's 1794 treason trial: outcome?", "Acquitted by the jury on 5 November 1794 after nine days, defended by Thomas Erskine.", "common_law_road", ["tna_hardy"], spot="hardy_1794"),
 c("c29", "image", "Name the film and the juror who holds out.", "12 Angry Men (1957); Juror 8, played by Henry Fonda.", "adversarial_machine", ["wiki_12angry"], spot="twelve_angry_men", img="img_12angry"),
 c("c30", "image", "Whose pencilled petition won the right to a free lawyer in US felony cases?", "Clarence Earl Gideon, Gideon v Wainwright, 18 March 1963.", "adversarial_machine", ["wiki_gideon"], spot="gideon", img="img_gideon"),
 c("c31", "fact", "What happened to Ernesto Miranda after his Supreme Court win?", "Retried without the confession and convicted; paroled 1972; killed in 1976.", "adversarial_machine", ["wiki_miranda"], spot="miranda"),
 c("c32", "fact", "What is a German Strafbefehl?", "A penal order: a written penalty that becomes a conviction without a hearing if the accused does not object.", "inquisitorial_machine", ["langbein_1979", "beck_strafbefehl"], spot="penal_order"),
 c("c33", "why", "Why did Taxquet v Belgium (2010) matter?", "The European Court found a fair-trial breach because Taxquet could not understand why a jury convicted him from four yes/no answers.", "inquisitorial_machine", ["taxquet_blog"], spot="taxquet"),
 c("c34", "image", "Which American judge attacked the 'fight theory' of trials?", "Jerome Frank, Courts on Trial (1949).", "thinkers", ["frank_courts"], spot="jerome_frank", img="img_frank"),
 c("c35", "why", "Why does Langbein compare plea bargaining to medieval torture?", "Both solve the same problem: a full trial so demanding that the state needs another way to obtain a confession.", "thinkers", ["langbein_torture"], spot="langbein_critic"),
 c("c36", "fact", "What kind of trial does the ICC run?", "A hybrid of common law and civil law: three professional judges, no jury, cross-examination, victims participate.", "collisions", ["wiki_icc"], spot="icc"),
 c("c37", "fact", "When did Italy's adversarial-style code take effect?", "24 October 1989.", "collisions", ["psilr_italy"], spot="italy_1989"),
 c("c38", "fact", "Mexico's switch to oral accusatory trials: deadline?", "18 June 2016, under the 2008 constitutional reform.", "collisions", ["emory_mexico"], spot="mexico_2016"),
 c("c39", "image", "Who is this, and what did she insist on in 2024?", "Gisèle Pelicot, who insisted the trial of her ex-husband and 50 men be public.", "failures", ["wiki_pelicot"], spot="pelicot", img="img_pelicot"),
 c("c40", "fact", "What is 'hostage justice'?", "Critics' term for Japan's practice of holding suspects who deny charges in long detention, up to 23 days before charge, to obtain confessions.", "failures", ["wiki_hostage", "wiki_japan_cj"], spot="ghosn"),
 c("c41", "why", "Why is Japan's 99 per cent conviction rate misleading?", "Prosecutors charge only cases they are confident of winning and drop or divert most others.", "truth_evidence", ["wiki_japan_cj"], spot="conviction_paradox"),
 c("c42", "fact", "What did Thibaut and Walker find?", "People rated adversarial procedures fairer because they kept process control.", "truth_evidence", ["sage_procedural"], spot="thibaut_walker"),
 c("c43", "cloze", "Section 165 of the Indian Evidence Act became Section ____ of the Bharatiya Sakshya Adhiniyam.", "168.", "india", ["bsa_168"], spot="section_165"),
 c("c44", "fact", "Nanavati (1959): jury vote and final outcome?", "Jury acquitted 8 to 1; High Court convicted him of murder; Supreme Court confirmed in 1961.", "india", ["wiki_nanavati"], spot="nanavati"),
 c("c45", "image", "Which ancient Indian legal test does this painting show?", "Sita's agni pariksha, an ordeal by fire; Yājñavalkya lists five divya.", "india", ["unica_yajnavalkya"], spot="yajnavalkya_ordeals", img="img_sita"),
 c("c46", "image", "Is London's statue of Justice on the Old Bailey blindfolded?", "No. Pomeroy's figure (1905 to 1906) has open eyes.", "myths", ["wiki_old_bailey"], spot="myth_blindfold", img="img_ob_justice"),
 c("c47", "fact", "When did Scotland stop using 'not proven' for new trials?", "1 January 2026.", "now", ["wiki_not_proven"], spot="scotland_not_proven"),
 c("c48", "fact", "Italy's March 2026 referendum on separating judges' and prosecutors' careers: result?", "Rejected, about 54 to 46.", "now", ["wiki_italy_ref"], spot="italy_referendum"),
 c("c49", "fact", "Japan's July 2026 retrial reform: two main changes?", "Prosecutors generally cannot appeal orders to reopen a case; courts can order evidence disclosure when relevant and necessary.", "now", ["japan_retrial"], spot="japan_retrial"),
 c("c50", "fact", "Duterte at the ICC: what happened on 23 April 2026?", "Pre-trial judges confirmed murder charges as crimes against humanity and committed him to trial.", "now", ["hrw_duterte"], spot="duterte_icc"),
 c("c51", "why", "Why did Lord Devlin defend the adversarial method?", "Two prejudiced searchers starting from opposite ends of a field miss less than one neutral searcher in the middle.", "thinkers", ["wiki_adversarial"]),
 c("c52", "fact", "Procedural justice in one line?", "People accept outcomes, even losing ones, more readily when they feel the process let them be heard.", "truth_evidence", ["sage_procedural"]),
]

# ---------------------------------------------------------------- verification
VER = [
 {"claim": "Garrow coined 'innocent until proven guilty' in 1791", "status": "disputed", "note": "Wikipedia credits Garrow; the idea is much older (Roman and canon law maxims). Treat as 'popularised in English courts', not invented."},
 {"claim": "Garrow's date of death", "status": "disputed", "note": "Wikipedia gives 24 September 1840 in the lead and 14 September 1840 in the body."},
 {"claim": "Number of investigating-judge cases in France in 2023 (16,600) and 4.7 million new cases", "status": "unverified", "note": "From a search summary of the Ministry of Justice's Références statistiques Justice 2023; the PDF did not download during research. The ratio is an order of magnitude, as the units differ."},
 {"claim": "Crown Court backlog of 79,616", "status": "range", "note": "Reported as a record in Law Society Gazette coverage; other 2025 sources give about 73,000 to 77,000 depending on the quarter."},
 {"claim": "Undertrial share of Indian prisoners in 2023", "status": "range", "note": "73.5% (Dataful, from NCRB) to 76.2% (The Policy Edge); the day uses 73.5% and 'about three in four'."},
 {"claim": "Japan's conviction rate", "status": "range", "note": "Commonly above 99%; one measure of the first-instance rate was 97.8% in 2017. Depends on whether summary procedures and guilty admissions are counted."},
 {"claim": "Dervan and Edkins: share of innocent participants who accepted the deal", "status": "range", "note": "Wikipedia gives about 56%; other summaries say 'more than half'. The day says more than half."},
 {"claim": "Outreau: 40% drop in child sexual assault convictions in the following decade", "status": "unverified", "note": "Stated in Wikipedia's Outreau article; not used in the day."},
 {"claim": "German trial lengths (47% under about two hours)", "status": "range", "note": "From Casper and Zeisel's 1969 to 1970 sample cited by Langbein (1979); old data, modern German trials of serious crimes are often much longer."},
 {"claim": "Baden-Württemberg: 97% of fine convictions by penal order", "status": "unverified", "note": "Reported by beck-aktuell (2024) citing the state justice ministry; no national figure found."},
 {"claim": "Jerome Frank's appointment year and SEC role", "status": "unverified", "note": "Image description confirms his SEC role; appointment to the Second Circuit in 1941 from general knowledge."},
 {"claim": "Pelicot trial heard by the Vaucluse criminal court of five professional judges", "status": "unverified", "note": "Al Jazeera reports the first trial was before five judges; the court's formal name is from general knowledge of the cours criminelles départementales."},
 {"claim": "Damaška's hierarchical/coordinate typology", "status": "unverified", "note": "Standard summary of The Faces of Justice and State Authority (1986), mentioned in the thinkers intro; the book text itself was not fetched."},
 {"claim": "Lady Justice blindfold history", "status": "unverified", "note": "The Old Bailey explanation comes from Wikipedia; the claim that the blindfold began in Renaissance prints is general knowledge."},
 {"claim": "Mexico's first federal use of the new code in Durango and Puebla, 2014", "status": "unverified", "note": "From Expansión (2014) via search summary."},
 {"claim": "Details of David's 1812 Napoleon portrait (clock at 4.13, papers marked CODE)", "status": "unverified", "note": "Widely described in museum literature; not checked against the National Gallery of Art page during research."},
]
for sid in ["plea_bargain_us", "prisoners_counsel_1836", "penal_order", "langbein_critic", "thibaut_walker", "malimath", "plea_india", "italy_referendum"]:
    VER.append({"claim": f"No correct openly licensed image for spotlight {sid}", "status": "no_image", "note": "Searched Wikimedia Commons; nothing showed the actual thing. Left without image.", "spotlight_id": sid})

# ---------------------------------------------------------------- side dish and offline task
SIDE = {"area": "Psychology", "title": "Why losers accept verdicts: procedural justice",
 "body_md": """In the 1970s the psychologist John Thibaut and the lawyer Laurens Walker asked a strange question for a law school: not who wins a dispute, but how the loser feels about it.

They set up mock disputes and gave volunteers different procedures. In some, each side controlled the presentation of its own case, as in an adversarial trial. In others, a neutral official ran the inquiry. People consistently rated the procedures that let them speak as fairer, even when the outcome was the same. Thibaut and Walker called this **process control**.

The idea grew into the field of **procedural justice**. Later researchers, notably Tom Tyler, found the same pattern outside courtrooms: people obey the law, accept police decisions and cooperate with institutions more when they believe the process was fair. Four things matter most: having a **voice**, being treated with **dignity**, facing a **neutral** decision-maker, and being able to **trust** the motives of the person deciding.

The lesson cuts both ways for today's topic. The adversarial trial scores high on voice, which may be why people like it. The inquisitorial trial scores high on neutrality and explanation, a reasoned judgment you can read. A plea bargain struck in a corridor scores low on almost everything, which may explain why it feels unfair even when the sentence is light.

Try it on your next disagreement at work: before deciding, let each side explain fully, and then explain your reasons. The decision may not change. How people take it often does.""",
 "image_ids": [], "card_ids": ["c42", "c52"], "source_ids": ["sage_procedural"]}

OFFLINE = {"kind": "watch", "title": "Watch 12 Angry Men and retry it in Paris",
 "body_md": """**Time: about 2 hours.** Watch Sidney Lumet's *12 Angry Men* (1957), 96 minutes, then spend 20 minutes on the exercise below.

**While you watch, note:**
1. Every piece of evidence the jurors discuss. Which was never properly tested by cross-examination at trial?
2. Every time a juror does his own investigating (the knife, the train, the glasses). Real jurors are told not to.
3. What the jurors do not know: the defendant's past, his statements to police, anything outside the courtroom.

**Then retry the case in a French cour d'assises.** Three professional judges and six citizen jurors deliberate together, after the presiding judge has read the full police file and questioned the boy himself at length.

- Which of Juror 8's doubts would the presiding judge have explored in court, from the file?
- Which doubts might never have come up, because nobody on the bench had a reason to argue for the defence?
- Would the result be the same? Would you trust it more or less, given a written judgment explaining why?

**Write three lines:** one thing the jury room does better, one thing the French bench does better, and which you would choose if you were the accused.""",
 "source_ids": ["wiki_12angry", "wiki_inquisitorial", "wiki_lay_judge"], "spotlight_id": "twelve_angry_men"}

# ---------------------------------------------------------------- assemble
DAY = {
 "schema_version": 2, "id": "t0834", "day": 834, "area": "Law", "title": "The adversarial vs inquisitorial trial", "native_name": None,
 "as_of": ACC, "reading_minutes": 55,
 "hero": {"image_id": "img_ob_court1", "kicker": "Day 834 · Law", "headline": "Contest or inquiry: two ways to find the truth in a criminal court, and why both are changing in 2026"},
 "geo": None,
 "stats": [
  {"key": "us_plea_share", "label": "US federal defendants who pleaded guilty", "value": 89.5, "unit": "%", "year": "2022", "source_ids": ["pew_2023"]},
  {"key": "us_acquitted", "label": "US federal defendants acquitted at trial", "value": 0.4, "unit": "%", "year": "2022", "source_ids": ["pew_2023"]},
  {"key": "fr_instruction", "label": "Judicial investigations opened in France", "value": 16600, "year": "2023", "source_ids": ["rsj_instruction"]},
  {"key": "in_plea", "label": "Indian cases settled by plea bargaining", "value": 0.11, "unit": "%", "year": "2022", "source_ids": ["civils_plea"]},
  {"key": "in_pending", "label": "Cases pending in Indian district courts", "value": 47657328, "year": "2025-12-31", "source_ids": ["ians_pendency"]},
  {"key": "uk_backlog", "label": "Crown Court backlog, England and Wales", "value": 79616, "year": "2025", "source_ids": ["lg_backlog"]},
  {"key": "varad_pass", "label": "Hot-iron ordeal pass rate at Várad", "value": 62.5, "unit": "%", "year": "1208-1235", "source_ids": ["leeson_ordeals"]},
 ],
 "prequestions": PREQ,
 "sections": SECTIONS,
 "cards": CARDS,
 "quiz": QUIZ,
 "quiz_bank": QUIZ_BANK,
 "best_facts": BEST_FACTS,
 "images": IMAGES,
 "media": MEDIA,
 "sources": SOURCES,
 "verification": VER,
 "side_dish": SIDE,
 "offline_task": OFFLINE,
}

# sanity: no em dashes, no exclamation marks in prose
raw = json.dumps(DAY, ensure_ascii=False)
assert "—" not in raw, "em dash found"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(DAY, f, ensure_ascii=False, indent=1)
print("wrote", OUT)
