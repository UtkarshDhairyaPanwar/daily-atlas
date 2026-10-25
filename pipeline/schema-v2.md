# Day schema v2: visual first

Change from v1 (Utkarsh, 2026-10-25): text alone cannot carry a state. Every distinct, memorable thing (a dance, an art style, a craft, a dish, a drink, a custom, a monument, a person, a landscape) becomes a **spotlight**: its own picture-led card with a "how to spot it" line. Text sections shrink to short connecting intros. Sections become stacks of spotlights.

## Top level
```json
{
  "schema_version": 2,
  "id": "in-andhra-pradesh", "day": 1, "area": "india", "title": "Andhra Pradesh", "native_name": "ఆంధ్ర ప్రదేశ్",
  "as_of": "2026-10-25", "reading_minutes": 50,
  "hero": { "image_id": "...", "kicker": "Day 1 · South India", "headline": "..." },
  "geo": { "centroid": [lat, lon], "bbox": [s, w, n, e], "neighbours": [], "regions": [{ "id", "name", "note" }] },
  "stats": [{ "key", "label", "value", "unit", "year", "rank_in_india", "source_ids" }],
  "prequestions": [ /* 5 quiz items, guess before reading */ ],
  "sections": [ Section ],
  "cards": [ Card ],
  "quiz": [ QuizItem ],
  "images": [ Image ],
  "media": [ Media ],
  "sources": [{ "id", "title", "url", "publisher", "accessed" }],
  "verification": [{ "claim", "status": "range|unverified|disputed", "note" }],
  "side_dish": { "area", "title", "body_md", "image_ids", "card_ids" },
  "offline_task": { "kind": "cook|listen|watch|words|find", "title", "body_md" }
}
```

## Section
```json
{
  "id": "performing_arts", "order": 9, "title": "Dance, music, theatre",
  "intro_md": "80 to 200 words. Connective tissue only. The detail lives in spotlights.",
  "visual": { "type": "map|timeline|bar|donut|ring|compare|stat_tiles|photo_grid", "title", "data": {} },
  "spotlights": [ Spotlight ],
  "check": ["quiz ids shown after this section, 2 to 3"],
  "source_ids": []
}
```

## Spotlight (the core unit)
```json
{
  "id": "kuchipudi",
  "kind": "dance|music|theatre|art|craft|textile|dish|drink|festival|custom|place|monument|person|landscape|wildlife|object|event",
  "name": "Kuchipudi", "native_name": "కూచిపూడి",
  "where": { "label": "Kuchipudi village, Krishna district", "lat": 16.25, "lon": 80.9 },
  "when": "17th century codified",
  "image_ids": ["img_kuchipudi_1", "img_kuchipudi_2"],
  "media_ids": ["vid_kuchipudi_tarangam"],
  "spot_it": "One line: how to recognise it on sight or sound. Springy footwork, dancer on the rim of a brass plate.",
  "story_md": "60 to 140 words. The concrete, surprising detail.",
  "why_it_matters": "One line.",
  "memory_hook": "One vivid line built to stick.",
  "compare": { "with": "Bharatanatyam", "image_id": "...", "difference": "..." },
  "gi_tag": { "year": 2008, "status": "verified|unverified" },
  "source_ids": []
}
```
Rules: every spotlight has at least one image. Kinds that are seen (dance, art, craft, textile, dish, monument, place, person, custom) need a real photo. Kinds that are heard (music, theatre) get audio or video if any reliable source exists. `custom` covers behaviour: how people greet, eat, dress, celebrate (eating on a banana leaf, muggulu drawn at the door each dawn, Sankranti cockfights).

## Card
```json
{ "id", "type": "fact|cloze|image|map|why|compare", "front", "back", "image_id", "spotlight_id", "section_id", "core": true, "source_ids" }
```
`core: true` cards (about 20 per day) are the daily minimum. The rest are bonus and still schedulable when the learner goes ahead.
Type `image` is the default for any spotlight with a strong photo: show picture, ask the name. Type `compare`: two images, "which is Kuchipudi?"

## QuizItem
As v1: `mcq | true_false | order | map_pin | image_id | match | higher_lower | odd_one_out`, plus `guess_clues` (3 to 5 clues revealed one at a time) and `listen_id` (play audio, name it). Each has `explanation`.

## Image
`{ id, url, thumb_url (≈1280px), width, height, author, license, license_url, file_page, alt, caption, attribution, verified_on }`. Wikimedia Commons or other openly licensed sources only. Verified to load.

## Media
`{ id, kind: "video|audio", provider: "youtube|commons|archive", url, embed_url, start, end, title, publisher, license, duration_s, verified_on }`. Prefer official channels (Sahapedia, Doordarshan / Prasar Bharati, Sangeet Natak Akademi, state tourism, Ministry of Culture, IGNCA) or Commons. Clip to the 20 to 90 seconds that show the thing. Online only; app degrades gracefully offline.
