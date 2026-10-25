# Daily Atlas curriculum

The queue now covers every top-level branch of the four knowledge maps checked below. It has 2,581 topics outside the India 36, up from 1,874, in 45 areas instead of 27.

- File: `curriculum.tsv` (columns: area, title, tier). Rows are grouped by area. Within an area, foundations come first and niche topics last.
- Tiers: A means essential, B means valuable, C means niche or fun. There are 581 A, 1,526 B and 474 C topics.
- The India 36 are not in the file and have not changed.
- Weights run from 0.6 to 1.6 and feed the mixer in `reorder.py`. A higher weight means the area shows up more often early in the queue.

## Totals

| | Count |
|---|---|
| Original non-India topics | 1,874 |
| Removed (duplicates, merges, thin days) | 96 |
| Added | 803 |
| of which carried over from your Philosophy and Science drafts | 67 |
| of which new | 736 |
| Moved between areas (kept, not counted as added or removed) | 58 |
| Renamed to absorb a merge or remove a duplicate | 11 |
| **Final, not counting the India 36** | **2,581** |
| Final including the India 36 | 2,617 |

At one topic a day, A tier alone takes about 1.6 years and the full list about 7. Use the tiers to filter.

## Areas

| Area | Weight | Topics | A | B | C | Was | Description |
|---|---|---|---|---|---|---|---|
| History | 1.5 | 68 | 39 | 29 | 0 | 85 | World history from human origins to the present, the spine everything else hangs on. |
| Science | 1.5 | 37 | 11 | 21 | 5 | new | Physics, chemistry and biology from first principles: atoms, energy, light, cells and genes. |
| Politics | 1.45 | 69 | 20 | 44 | 5 | new | How power works: ideologies, constitutions, India's democracy and the world order. |
| Philosophy | 1.4 | 66 | 17 | 40 | 9 | new | The big questions and the people who asked them, East and West, ethics included. |
| Economics | 1.35 | 53 | 12 | 38 | 3 | new | How economies work: markets, trade, growth, development and the Indian economy. |
| Indian history | 1.35 | 52 | 13 | 35 | 4 | new | India from Bhimbetka to the 1990s, beyond the headline empires. |
| Thinking | 1.3 | 35 | 6 | 26 | 3 | new | Skills for thinking and communicating: learning, reasoning, writing, speaking, negotiating. |
| Computing | 1.3 | 53 | 11 | 37 | 5 | new | How computers, software, the internet and AI actually work, and where they came from. |
| Psychology | 1.3 | 77 | 24 | 46 | 7 | 77 | How minds work and fail: biases, memory, motivation, emotion and mental health. |
| Human body | 1.25 | 44 | 12 | 27 | 5 | new | Your own body system by system, plus nutrition, exercise and how to read it. |
| Literature | 1.25 | 81 | 16 | 54 | 11 | new | The world's great writing, with Indian literature across its many languages. |
| Mathematics | 1.2 | 43 | 13 | 18 | 12 | new | The ideas behind numbers, proof, probability and statistics, with India's role in them. |
| World | 1.2 | 165 | 36 | 98 | 31 | 152 | Countries and regions, one culture at a time. |
| How things work | 1.2 | 78 | 20 | 47 | 11 | 77 | Materials, machines, infrastructure and engineering behind daily life. |
| Society | 1.15 | 46 | 7 | 35 | 4 | new | Sociology and anthropology: class, caste, family, gender, demography, education and media. |
| Law | 1.1 | 44 | 6 | 31 | 7 | new | What law is, how courts and constitutions work, India's legal system and international law. |
| Geography | 1.1 | 36 | 11 | 20 | 5 | new | The physical Earth and the human map: landforms, rivers, oceans, borders and India's terrain. |
| Money | 1.1 | 55 | 15 | 35 | 5 | 60 | Money, banking, markets and financial history. |
| Personal finance | 1.1 | 26 | 7 | 17 | 2 | new | Practical money skills for an Indian earner: saving, investing, insurance and tax. |
| Medicine | 1.1 | 59 | 19 | 37 | 3 | 61 | How medicine learned what it knows, and the diseases and treatments that matter. |
| Climate | 1.1 | 51 | 14 | 35 | 2 | 51 | Climate science, energy transition and environmental problems, with India's stakes. |
| Nature | 1.1 | 68 | 16 | 42 | 10 | 76 | Evolution, ecosystems and the living world. |
| War | 1.0 | 43 | 4 | 35 | 4 | new | Military history and strategy: why wars happen, how they are fought and how they end. |
| Business | 1.0 | 35 | 5 | 27 | 3 | new | How companies work: strategy, models, management and India's business history. |
| Religion | 1.0 | 49 | 16 | 30 | 3 | 57 | The world's religions, their texts, practices and how to compare them. |
| Art | 1.0 | 76 | 18 | 45 | 13 | 76 | Visual art across cultures and movements, and how to look at it. |
| Astronomy | 1.0 | 53 | 17 | 30 | 6 | 56 | The solar system, stars, galaxies, cosmology and spaceflight. |
| Language | 0.95 | 46 | 14 | 23 | 9 | 46 | Where languages come from, how they change and how writing began. |
| Architecture | 0.9 | 33 | 10 | 18 | 5 | new | How buildings work and the styles and architects that shaped them. |
| Cities | 0.9 | 69 | 16 | 44 | 9 | 100 | Great cities and urban planning: how places get built, grow and break. |
| Music | 0.9 | 89 | 16 | 52 | 21 | 73 | Music traditions of the world, Indian and Western classical to modern genres. |
| Film | 0.9 | 66 | 16 | 40 | 10 | 66 | Cinema history, national cinemas and the craft of filmmaking. |
| Food | 0.9 | 54 | 16 | 29 | 9 | 57 | Food as world history: crops, spices, drinks and the modern food system. |
| Myth | 0.85 | 49 | 11 | 27 | 11 | 51 | Myths and folklore of the world and why humans tell them. |
| Design | 0.8 | 22 | 2 | 13 | 7 | new | Design history and principles beyond type: graphic, industrial, UX and Indian design. |
| Type | 0.8 | 52 | 13 | 26 | 13 | 54 | Typography: history, craft and the scripts of the world. |
| Brands | 0.8 | 87 | 10 | 61 | 16 | 90 | How brands are built, through case studies of companies that did it well or badly. |
| Crime | 0.8 | 44 | 10 | 25 | 9 | 59 | Crime, forensics and organised crime; how evidence is found and gets it wrong. |
| Festivals | 0.8 | 58 | 8 | 29 | 21 | 62 | Why humans celebrate, through India's and the world's festivals. |
| Social media | 0.8 | 47 | 11 | 28 | 8 | 50 | Platforms, algorithms and what social media does to people and politics. |
| Fashion | 0.75 | 50 | 8 | 23 | 19 | 50 | Dress through history, textiles and the fashion industry. |
| Games | 0.75 | 56 | 5 | 31 | 20 | 57 | Board, card and video games: history, design and industry. |
| Internet | 0.7 | 42 | 2 | 20 | 20 | 50 | Internet culture: memes, fandoms, subcultures and online life. |
| Sports | 0.65 | 105 | 6 | 33 | 66 | 123 | The world's sports: rules, history and culture. |
| Paranormal | 0.6 | 50 | 2 | 25 | 23 | 58 | Conspiracies, cryptids and the unexplained, read sceptically. |
| **Total** | | **2581** | 581 | 1526 | 474 | 1874 | |
The weights add the new core areas near the top. History, Science, Politics, Philosophy, Economics and Indian history get the most early slots. Sports and Paranormal are still in the queue but appear rarely.

**Area rename:** "Social" is now called "Social media". This stops it being confused with the new Society area. If the app keys on area names, update `W` in `reorder.py`, or rename the area back.

## Gaps found, and the framework that showed them

Frameworks checked:
- Britannica Propaedia: the Outline of Knowledge, 10 parts and 41 divisions.
- Wikipedia Vital Articles, levels 2 and 3.
- The Dewey Decimal top 10 classes and their 100 divisions.
- The Columbia Core: Literature Humanities, Contemporary Civilization, Music Humanities, Art Humanities and Frontiers of Science.

| Gap | Shown by | Fix |
|---|---|---|
| Philosophy and ethics: no area at all | Propaedia Part 10 (Philosophy, Logic); Vital L2 "Philosophy and religion" (Knowledge, Ethics, Logic); Dewey 100; Columbia Contemporary Civilization (Stoics, the social contract, Kant, Mill, Marx) | **Philosophy** (66). Builds on your draft. Adds epistemology, metaethics, the three big ethical theories, bioethics, aesthetics, philosophy of religion and more Indian and Chinese schools |
| Politics and government, democracy, ideologies, the UN, geopolitics | Propaedia 5 (Politics and Government); Vital L3 "Politics and government" (Democracy, Ideology, Liberalism, Conservatism, Nationalism, the UN, the EU, Diplomacy); Dewey 320 | **Politics** (69). About 20 of these are on Indian topics: the Constitution, Parliament, the Election Commission, federalism, reservation, secularism and foreign policy |
| Economics as a discipline (Money only covered finance history) | Propaedia 5 (Production, Distribution and Utilization of Wealth); Vital L3 (Macroeconomics, Microeconomics, Trade, Tax); Dewey 330 | **Economics** (53). Micro, macro, trade, growth, development, the economic thinkers and 10 days on India's economy |
| Law beyond crime: constitutions, contracts, property, IP, international law | Propaedia 5 (Law); Vital L3 (Law, Constitution, Justice, Property); Dewey 340 | **Law** (44). Takes in the 13 legal-system days from Crime and adds Indian constitutional law, including Kesavananda, PILs and the BNS |
| Mathematics | Propaedia 10 (Mathematics); Vital L2 (Mathematics, Algebra, Arithmetic, Geometry, Statistics); Dewey 510 | **Mathematics** (43). Takes the maths days from your Science draft and adds proof, algebra, functions, logarithms, Bayes and the Indian mathematicians |
| Physics, chemistry and core biology | Propaedia 1 and 3; Vital L2 (Matter, Energy, Chemistry, Cell, Physics); Dewey 530 to 570; Columbia Frontiers of Science | **Science** (37). Your draft, minus the maths and the brain, plus gravity, general relativity, chemistry basics, heredity, ecology and Indian science |
| Computing and AI (How things work covered hardware, not software, logic or AI) | Dewey 000 (Computer science); Propaedia 7 (Technology); Vital L3 "Computing and information technology" | **Computing** (53). How computers work, algorithms, the history of computing, how the internet works, AI and ML, security and India Stack |
| Literature: no area at all | Propaedia 6 (Particular Arts: literature); Vital L2 (Literature); Dewey 800; Columbia Literature Humanities (Homer, Greek tragedy, Dante, Shakespeare, Cervantes, Austen, Dostoevsky, Woolf) | **Literature** (81). The Western canon, plus Sanskrit, Tamil, Persian, Chinese and Japanese classics. About 20 days on Indian literature across Bengali, Hindi-Urdu, Tamil, Malayalam, Kannada, Telugu, Marathi, Punjabi, Dalit and Partition writing, and Indian English |
| The human body (Medicine covered disease and treatment, not normal anatomy and physiology) | Propaedia 4 (The Human Body: Health and Disease); Vital L3 (Human body, Reproduction) | **Human body** (44). System by system, then nutrition, exercise and reading your own blood tests |
| Physical geography: landforms, oceans, maps | Propaedia 2 (The Earth); Vital L2 Geography (Land, Ocean, Atmosphere); Dewey 550 and 910 | **Geography** (36). Takes the six geology days from Nature and adds maps, the Himalaya, Indian river systems, the monsoon, oceans, borders and chokepoints |
| Society: sociology, anthropology, caste, family, demography, education | Propaedia 5 (Social Groups, Social Organization, Education); Vital L3 (Social class, Ethnicity, Family, Feminism, Human migration, Poverty); Dewey 300 and 370 | **Society** (46) |
| Business and strategy | Dewey 650 (Management); Vital L3 (Business, Corporation, Management, Marketing) | **Business** (35). Brands stays as the case-study area. Business holds the fundamentals |
| War and strategy | Vital L3 (War, Military, Peace, Genocide); Dewey 355 (Military science) | **War** (43). Strategy classics, famous battles, deterrence, and India's wars from Panipat to Kargil. It avoids repeating the wars already in History |
| Architecture (it existed only as 28 days inside Cities) | Vital L2 (Architecture); Dewey 720 | **Architecture** (33). Takes the 21 style days out of Cities and adds foundations and Indian architects (Doshi, Correa, Baker, Kahn in India) |
| Indian history beyond the headline empires | Propaedia 9 (East, Central, South and Southeast Asia) | **Indian history** (52). Takes the 13 Indian days from History and fills the gaps: Sangam, the Pallavas, the Ahoms, the Sikh Gurus, Tipu Sultan, the national movement and post-1947 India |
| Thinking and communication skills | Dewey 160 (Logic) and 808 (Rhetoric); the trivium behind the liberal arts core | **Thinking** (35). Learning, reasoning, rhetoric, writing, speaking and negotiation |
| Personal finance | Dewey 640 (Home and family management) | **Personal finance** (26), written for an Indian earner (SIPs, EPF, PPF, NPS, the tax regimes, term insurance) |
| Design beyond typography | Dewey 740 (Graphic and decorative arts); Propaedia 6 (Art in General) | **Design** (22). Graphic, industrial, UX and Indian design history |
| Western classical music | Columbia Music Humanities; Vital L3 Music | Added 10 days to Music: chant, Bach, Mozart and Haydn, Beethoven, the Romantics, opera, the orchestra, Debussy and Stravinsky, the avant-garde. Also 6 popular-music days the area was missing (the Beatles, soul and Motown, disco, pop superstars, Ilaiyaraaja and Rahman, and a foundation day) |
| Environment beyond climate | Vital L3 (Pollution) | Added 4 days to Climate: air pollution in Indian cities, plastics, the Ganga, the ozone hole |
| Engineering as a discipline | Propaedia 7; Dewey 620 | Added to How things work: the branches of engineering, dams, engineering failures, India's engineering feats. A separate area would have duplicated How things work |
| World coverage holes | Vital L2 Geography (continents) | 13 regions added: the Gulf states (Qatar, Kuwait, Bahrain), Libya, the Sahel, Benin and Togo, Mauritius, Slovenia, Montenegro and Kosovo, Moldova, Europe's microstates, Central America, the US Midwest, California, Greenland |
| Area foundations missing | general | Sports: the Olympics. Brands: what a brand is, and positioning. Sports also gets doping, league economics and the IPL, and analytics |

Not added as separate areas: Engineering (it lives in How things work), Environment (it lives in Climate) and Ethics (it lives in Philosophy). Education, demography and urbanisation sit in Society.

## What was removed or merged, and why

Four rules guided the cleanup:
1. Where two areas covered the same topic, it stays in the area that goes deeper.
2. Repeated days on one idea were merged into one day.
3. A day was cut only if it could not fill 1 to 2 hours, for example a single hoax, a tourism event or a sport variant.
4. Topics were never cut just for being niche. Kalaripayattu, sepak takraw, buzkashi, numbers stations, Skinwalker Ranch and the like all stay, mostly at tier C.

**Sports**
- Racquetball: thin; covered by Squash
- Handball (American/wall): thin and confusable with Handball
- Korfball: thin
- Dodgeball: thin
- Tug of war: thin
- Underwater hockey: folded into Wife carrying, chess boxing and other odd sports
- Quidditch / quadball: thin
- Bossaball: folded into Wife carrying, chess boxing and other odd sports
- Chess boxing: folded into Wife carrying, chess boxing and other odd sports
- Bo-taoshi: folded into Wife carrying, chess boxing and other odd sports
- Hornussen: folded into Wife carrying, chess boxing and other odd sports
- Pesäpallo: thin; a baseball variant
- Gaelic football: merged into Gaelic games: hurling, Gaelic football and shinty
- Shinty: merged into Gaelic games: hurling, Gaelic football and shinty
- Greco-Roman wrestling: merged into Freestyle and Greco-Roman wrestling
- Powerlifting: merged into Weightlifting and powerlifting
- Pickleball: merged into Padel and pickleball
- Beach volleyball: merged into Volleyball
- Artistic swimming: thin; folded into Swimming
- Trampoline: thin; folded into Artistic gymnastics
- Esports: duplicate of Games: The esports industry
- Sledge & para sports: merged into The Paralympic movement

**Cities**
- Chandigarh: duplicate of the India day for Chandigarh
- Delhi: seven cities in one: duplicate of the India day for Delhi (NCT)
- Istanbul's informal growth: merged into Constantinople / Istanbul and Slums and informal settlements worldwide
- New towns and garden cities: merged into Ebenezer Howard and the garden city movement
- Venice's sinking and climate-threatened cities: merged into Venice, Climate: Sea level rise and Adaptation and resilient cities
- Street food and urban informality: duplicate of Food: Street food worldwide
- Singapore as planned city-state: merged into World: Singapore (a city-state gets one day)
- Hong Kong and vertical density: merged into World: Hong Kong & Macau
- The Bauhaus: third Bauhaus day; kept Art: The Bauhaus as an art school and Type: The Bauhaus and universal type
- The Arts and Crafts movement: duplicate of Type: The Arts and Crafts revival and William Morris

**Brands**
- Vercel: DX as marketing: thin; the DX-as-marketing idea is covered by Stripe and Twilio
- Bosch: overlapping industrial-brand day; Siemens carries the idea
- Honeywell: overlapping industrial-brand day; Siemens carries the idea
- ABB & Schneider Electric: overlapping industrial-brand day; Siemens carries the idea
- Nestlé: the house of brands: merged into Unilever, P&G and Nestlé: the FMCG portfolio game

**History**
- The 2008 financial crisis: duplicate of Money: The 2008 financial crisis
- Pandemics through history: covered by Medicine: Influenza and pandemics, History: The Black Death and the disease days in Medicine
- The internet era as history: thin; covered by Computing (ARPANET, the Web) and Social media
- The printing revolution: duplicate of Type: Gutenberg and movable type

**How things work**
- Vaccines: how they are made: merged into Medicine: Vaccination: how it works
- Antibiotics: discovery and manufacture: duplicate of Medicine: Antibiotics and Fleming

**Nature**
- Human evolution: duplicate of History: Human origins and out of Africa
- Glaciers and ice: duplicate of Climate: Glaciers and ice sheets

**Festivals**
- Eid al-Fitr: merged into Ramadan and Eid al-Fitr
- Mardi Gras: merged into Lent, Carnival and Mardi Gras
- Boryeong Mud Festival: thin; a tourism event, not a 1 to 2 hour subject
- La Tomatina: thin; a single tomato fight

**Medicine**
- The Black Death and its consequences: duplicate of History: The Black Death
- Clinical trials and drug approval: merged into How medicine learned to test itself: the trial

**Money**
- Financial fraud: famous cases: duplicate of Crime: Enron, Theranos and corporate fraud and Ponzi and pyramid schemes

**Crime**
- Eyewitness error: duplicate of Psychology: Eyewitness testimony
- Islamic law systems: duplicate of Religion: Islamic law and the schools of fiqh

**Paranormal**
- Vampire and werewolf folklore: duplicate of Myth: Vampires, werewolves and the undead
- Djinn, bhoot and folk spirits: duplicate of Myth: Bhoot, pret and Indian ghost lore
- Modern misinformation and how it spreads: duplicate of Social media: Misinformation and how it spreads
- Denver International Airport: thin; a meme more than a subject
- Bohemian Grove: merged into Bilderberg, Bohemian Grove and elite-meeting theories
- Men in Black folklore: thin; folded into Roswell and the birth of UFO culture
- John Titor and time travel claims: thin; one forum hoax, not a full day
- The Phoenix Lights: thin; one sighting, covered inside Roswell and Rendlesham days

**Food**
- The Columbian Exchange on the plate: duplicate of History: The Columbian Exchange
- Refrigeration and what it did to eating: duplicate of How things work: Refrigeration and the cold chain
- Canning and preserved food: duplicate of How things work: Food preservation: canning to freeze-drying

**Games**
- Loot boxes and regulation: merged into Gacha, loot boxes and monetisation ethics

**Religion**
- Norse mythology and religion: duplicate of Myth: Norse mythology and Ragnarök
- Comparative: creation myths: duplicate of Myth: Creation myths compared
- Aboriginal Australian Dreaming: duplicate of Myth: Aboriginal Dreaming stories
- Mesoamerican religion: duplicate of Myth: Mesoamerican myth and the Popol Vuh
- Ancient Egyptian religion: duplicate of Myth: Egyptian myth
- Celtic and druidic traditions: duplicate of Myth: Celtic myth and the Mabinogion
- The Ramayana and Mahabharata as living texts: merged into Myth: The Ramayana as story and The Mahabharata as story
- Religion, food and dietary law: duplicate of Food: Food taboos and Fasting traditions

**Astronomy**
- Relativity for astronomy: covered by Science: Special relativity, simply and General relativity and curved spacetime
- The Drake Equation: merged into SETI and the Fermi Paradox
- Meteor showers: merged into Asteroids, meteors and comets

**Type**
- Emoji as typography: duplicate of Internet: Emoji: history and semantics
- The International Typographic Style: duplicate of Helvetica and the Swiss style

**Climate**
- Solar power: duplicate of How things work: Solar cells
- Wind power: duplicate of How things work: Wind turbines
- Livestock, meat and diet: duplicate of Food: Meat, livestock and its footprint
- Climate denial and its funding: duplicate of The fossil fuel industry and its history of denial

**Myth**
- Cryptids as folklore: duplicate of the Paranormal cryptid days (Loch Ness, Bigfoot, Chupacabra)
- Yoruba orisha stories: duplicate of Religion: Yoruba religion and the orishas

**Internet**
- The rise of the podcast bro: thin; covered by Social media: Podcasting
- K-pop stans as an internet force: merged into Stan culture and fandom warfare
- Callout culture and internet justice: merged into Cancel culture and online discourse norms
- Crypto and NFT culture: covered by Money: Bitcoin and blockchains, Crypto crashes and frauds and Art: NFTs and the art market
- AI art discourse and the anti-AI backlash: duplicate of Art: AI art and the debate
- Deep-fried memes and irony layers: thin; folded into The evolution of the meme format
- Reaction images and GIF culture: thin; folded into The evolution of the meme format
- Where internet culture is heading: speculative and thin; overlaps Social media: What comes after the feed

**Social media**
- Engagement-optimised design and dark patterns: duplicate of Psychology: Dark patterns and how they exploit psychology
- Reddit: duplicate of Internet: Reddit's culture and its subreddit ecosystems
- Short-form video and the attention crunch: merged into TikTok and the algorithmic feed and The attention economy

### Moved between areas (kept, same wording)

- History to Indian history (13): The Indus Valley Civilisation, Vedic India, The Mauryan Empire and Ashoka, The Gupta Empire, The Cholas and maritime South India, The Delhi Sultanate, Vijayanagara, The Mughal Empire, The Maratha Empire, The British Raj, 1857 and the Indian rebellion, Indian independence and Partition, The Emergency in India
- Crime to Law (13): Legal systems: common law, Legal systems: civil law, Customary and tribal law, The Indian legal system, Juries and how they work, The adversarial vs inquisitorial trial, Sentencing and punishment philosophy, Prisons and incarceration compared, The death penalty worldwide, Restorative justice, Drug policy and decriminalisation, Policing reform debates, International courts and war crimes
- Money to Economics (4): GDP and what it misses, Inequality and how it is measured, Universal basic income, Tax systems compared
- How things work to Computing (1): Cryptographic keys and how HTTPS works
- Nature to Geography (6): Geology: plate tectonics, Volcanoes, Earthquakes, Caves and karst, Rivers and how they shape land, The water cycle
- Cities to Architecture (21): Ancient Greek and Roman architecture, Gothic architecture, Islamic architecture, Indian temple architecture, Indo-Islamic and Mughal architecture, Chinese and Japanese traditional architecture, Renaissance architecture, Baroque architecture, Neoclassical architecture, Art Nouveau architecture, International Style and modernism, Brutalism, Metabolism in Japan, Postmodern architecture, Deconstructivism, Vernacular and earth architecture, Sustainable and passive architecture, Parametric design and computational architecture, Interior architecture and the modern home, Landscape architecture, Adaptive reuse and preserving buildings
"Neoclassicism" and "Art Nouveau" from Cities became "Neoclassical architecture" and "Art Nouveau architecture". The new titles stop them clashing with the Art and Type days on the same movements.

### Renamed to absorb a merge or fix a duplicate

- Sports: "Padel" became "Padel and pickleball"
- Sports: "Freestyle wrestling" became "Freestyle and Greco-Roman wrestling"
- Sports: "Hurling" became "Gaelic games: hurling, Gaelic football and shinty"
- Sports: "Weightlifting" became "Weightlifting and powerlifting"
- Sports: "Wife carrying & odd sports" became "Wife carrying, chess boxing and other odd sports"
- Brands: "Unilever & P&G: the FMCG portfolio game" became "Unilever, P&G and Nestlé: the FMCG portfolio game"
- How things work: "Ships and container logistics" became "Ships: hulls, propulsion and why they float"
- Festivals: "Ramadan as a cultural season" became "Ramadan and Eid al-Fitr"
- Festivals: "Lent and Carnival" became "Lent, Carnival and Mardi Gras"
- Paranormal: "Bilderberg, Davos and elite-meeting theories" became "Bilderberg, Bohemian Grove and elite-meeting theories"
- Games: "Gacha mechanics and monetisation ethics" became "Gacha, loot boxes and monetisation ethics"
- Language: "Undeciphered scripts: Indus, Linear A, Voynich" became "Undeciphered scripts: Indus, Linear A and rongorongo"
### Wording fixes applied to every title

- Every em dash was replaced. Where the dash came before "and", it was dropped. Every other dash became a colon. Example: "Salesforce: inventing enterprise SaaS".
- Arrows were replaced with "to". Example: "Sanskrit to Prakrit to the modern Indo-Aryan languages".
- No other wording on kept topics was changed.

### Overlaps kept on purpose

These pairs look similar but come at the subject from different angles:
- History: The Columbian Exchange, and Food: Why food history is world history.
- Social media: TikTok and the algorithmic feed (the platform), and Internet: TikTok culture and trend cycles (the culture).
- Climate: The nuclear debate (policy), and How things work: Nuclear reactors (engineering).
- Psychology: Sleep and memory, and Medicine: Sleep and its biology.
- Myth: The Ramayana as story, and Literature: Tulsidas and the Ramcharitmanas.
- Paranormal: The Voynich Manuscript. Language now covers rongorongo in its undeciphered-scripts day instead.

## Next step

`reorder.py` still reads `topics_original.tsv`. To use the new curriculum, point it at `curriculum.tsv`. Then replace `EXTRA` and `W` with the weights in the Areas table above, and optionally filter or boost by tier. That script has not been touched.
