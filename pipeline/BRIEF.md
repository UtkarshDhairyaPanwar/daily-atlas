# Content brief: one topic, full depth

You are writing ONE day of Daily Atlas, a phone app Utkarsh uses for 1 to 2 hours a day to learn one topic deeply. The gold standard is Day 1, Andhra Pradesh: `data/days/0001.json` (read a few sections and spotlights of it before you start, to calibrate depth, tone and structure). Every topic gets that depth. Not a summary. A day someone remembers a month later.

Paths below are relative to the repository root (this repo is the live site).

## What makes a great day (in priority order)
1. **The most interesting facts.** Hunt for what is surprising, counter-intuitive, vivid and true. A fact earns its place if a curious adult would repeat it at dinner. Every day has a `best_facts` list of 12 to 20, each scored for surprise and checked against a source.
2. **Visual first.** Every distinct, memorable thing (a person, a place, an object, an artwork, a dish, an experiment, a machine, a ritual, a move in a sport, a logo, a chart) becomes a **spotlight** with real photos. Text alone does not carry a topic. If something has a look, show it.
3. **Depth with structure.** 12 to 20 sections, 40 to 60 spotlights, about 6,000 to 9,000 words total, so reading takes 45 to 60 minutes on a phone.
4. **Honesty.** Every section cites sources. Contested numbers show the range. Anything you could not verify goes in `verification`, never stated as settled. Myths are labelled as myths.
5. **Recall built in.** 45 to 60 flashcards (20 marked `core: true`), 18 to 25 end-of-day quiz items across at least 7 types, 10+ `quiz_bank` items used as section checks, 5 prequestions (guess-before-reading).

## Schema
Follow `pipeline/schema-v2.md` exactly, plus these additions:
- `"schema_version": 2`, `"id": "t0123"` (t + 4-digit queue number), `"day": 123`, `"area": "<area from topics.tsv>"`, `"title"`, `"native_name"` (for places, in the local script; otherwise omit or null), `"as_of": "2026-10-25"`, `"reading_minutes"`.
- `"geo"`: for anything with a place (countries, states, cities, festivals, cuisines, sports with a home, events), give `centroid` [lat, lon] and `bbox` [south, west, north, east]. Otherwise null.
- `"best_facts"`: list of `{ "fact": "one or two sentences", "why_surprising": "one line", "score": 1-10, "spotlight_id": optional, "source_ids": [...] }`, sorted by score, 12 to 20 items.
- `"quiz_bank"`: quiz items used only as section checks (`sections[].check` lists their ids). `quiz` is the end-of-day set. `prequestions` are 5 items asked before reading.
- `"verification"`: list of `{ "claim", "status": "range|unverified|disputed|no_image", "note", "spotlight_id" (for no_image) }`.
- `"side_dish"`: 10 minutes from a different field that connects to the topic (`area`, `title`, `body_md` 150 to 300 words, `image_ids`, `card_ids` of 2 cards that also exist in `cards`).
- `"offline_task"`: one thing to do off the screen today (`kind`: cook | listen | watch | words | find | try | observe, `title`, `body_md`).
- Visual types the app renders: `stat_tiles` (data: list of {label, value, note}), `map` (data: {pins: [{label, lat, lon, spotlight_id}]}), `timeline` (data: list of {year, event}) or dynasty-style bands (data: list of {name, start, end, note}, years as integers, BCE negative), `bar` (data: list of {metric, <seriesA>: number, <seriesB>: number}), `donut` (data: list of {label, value} as percentages), `compare` (data: {left: {label, image_id}, right: {label, image_id}, rows: [{feature, <left>, <right>}]}), `ring` (data: list of {month: 1-12, name}), `progress` (data: list of {label, value 0-100}), `photo_grid` (data: {image_ids}), `table` (data: list of objects). Put 6 to 12 visuals across the day where data genuinely fits.

## Section template
Design sections to fit the topic, but the day must cover these lenses where they apply (name sections in plain words, not these labels):
- **All topics:** the hook (one true scene or paradox), orientation (what it is, why it matters, the 6 to 8 numbers that matter), origins and history, how it actually works, the key people, the key works / cases / examples, variations around the world, the India connection (always look for one: Indian history, practice, people, market, data), myths vs facts, the best facts, what is happening now (dated, 2025 to 2026), recap.
- **India / World (places):** the land, people by numbers, deep history, how the place became what it is, languages, faith and philosophy, arts (dance, music, theatre), crafts and textiles, food and drink, festivals, how people live (customs, etiquette, values, via survey data and sociology; stereotypes only when tested against evidence), people to know, places to go, how it earns, what is happening now. Andhra Pradesh is the exact model.
- **History:** timeline, causes, the people, daily life of ordinary people, turning points, legacy today, how historians know (sources, archaeology), what is disputed.
- **Psychology / Medicine / Climate / Astronomy / Nature / How things work / Money:** the core idea explained simply, the mechanism, the landmark experiments or discoveries (each a spotlight with the scientist, the apparatus, the photo), the numbers, misreadings and replication status, everyday examples, India examples, how to use it or protect yourself, open questions.
- **Art / Music / Film / Type / Fashion:** how to recognise it (spot-it lines are critical here), the key works (each a spotlight with an image of the actual work where licensable, or of the artist, place, instrument), the makers, techniques, influence, where to see or hear it, compare pairs (A vs B side by side).
- **Brands:** the founding story, the product, the business model in numbers, the brand moves (campaigns, logos, slogans as spotlights), the people, the mistakes, the India presence, the lessons for a designer.
- **Sports / Games:** rules made simple, the field or board, the history, legendary players and moments, the culture around it, India's place in it, how to watch or play it.
- **Religion / Myth / Festivals:** the stories, the practices, the places, the objects, the art, regional variations, how people actually observe it today, respectful framing.
- **Crime / Paranormal:** what is established vs claimed, the evidence, the people, how to evaluate it, the real history behind the myth.
- **Internet / Social / Language:** the timeline, the platforms or language families, artefacts as spotlights (screenshots are rarely free; use photos of founders, devices, places, logos on Commons where licensed), mechanics, effects, India's version.

## Spotlights
Each: `id`, `kind` (dance, music, theatre, art, craft, textile, dish, drink, festival, custom, place, monument, person, landscape, wildlife, object, event, plus for non-place topics: experiment, idea, work, machine, building, brand, product, technique, team, match, organism, phenomenon, document), `name`, `native_name` if any, `where` {label, lat, lon} when it has a place, `when`, `image_ids` (1 to 3), `media_ids`, `spot_it` (one line: how to recognise it), `story_md` (60 to 140 words, the concrete surprising detail), `why_it_matters` (one line), `memory_hook` (one vivid line built to stick), optional `compare` {with, image_id, difference}, `source_ids`.

## Images and media (use the tools, do not guess URLs)
- `python3 pipeline/tools/commons.py search "query" --n 8` returns openly licensed Commons candidates with author, licence and a 1280px `thumb_url`. Look at `description` and `title` to make sure it shows the actual thing. Prefer real photos of the actual thing. Try 2 to 4 query phrasings per spotlight (English name, local name, place + thing).
- `python3 pipeline/tools/commons.py verify "File:Name.jpg" ...` returns records for specific files.
- Copy the record into `images`, give it an `id` (img_...), write a plain `alt` and a one-line `caption`. Drop `free`, `title` and `description` fields.
- If no correct image exists, leave `image_ids` empty and add `{status: "no_image", spotlight_id}` to `verification`. Never use a wrong or generic image. No AI images. No drawings by you.
- Video and audio: find 4 to 12 short clips for music, dance, sport, festival, film, craft process, science demos. Prefer official channels (Doordarshan / Prasar Bharati, Sahapedia, Sangeet Natak Akademi, museums, universities, NASA, BBC, national tourism, the brand's own channel) or Commons media. Verify each with `python3 pipeline/tools/yt.py URL`. Use `embed_url` from the tool, add `start`/`end` seconds for the best 20 to 90 seconds when you can tell, `publisher` = channel, `verified_on`.

## Research
Use WebSearch and WebFetch (load them via ToolSearch "select:WebSearch,WebFetch"). Read real sources: Wikipedia for orientation, then primary and authoritative ones (government data, museums, journals, books, reputable news for 2025 to 2026). At least 40 sources, each `{id, title, url, publisher, accessed}`. Cite per section, per spotlight, per best fact, per quiz item. Check numbers twice. For "what is happening now", search for 2026 news and date every item.

## Writing
Plain, concrete, vivid. Short sentences. Numbers with years. No em dashes (use commas, colons, full stops). No emojis. No buzzwords ("rich tapestry", "vibrant", "delve", "nestled", "testament to", "melting pot", "hidden gem", "boasts"). No exclamation marks. Write like a sharp magazine writer who checked every fact.

## How to work
1. Read `pipeline/topics.tsv` line for your topic, then 2 or 3 sections of the Day 1 file.
2. Research, then write a Python build script at `pipeline/build/tNNNN.py` that assembles the dict and writes `data/days/NNNN.json` (4-digit, zero padded) with `ensure_ascii=False`. A script is easier to fix than hand-edited JSON.
3. Run `python3 pipeline/tools/validate.py data/days/NNNN.json`. Fix every ERROR and rerun until it exits 0. Treat warnings seriously.
4. Do not touch any other topic's files, the app code, or shared files.
5. Finish with the summary the caller asks for.
