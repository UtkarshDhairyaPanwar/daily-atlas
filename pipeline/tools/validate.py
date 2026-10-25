#!/usr/bin/env python3
"""Validate a Daily Atlas day file at full (Andhra Pradesh) depth.
  python3 validate.py path/to/NNNN.json [--area India]
Prints stats and every problem. Exit 1 if any ERROR."""
import json, re, sys
p = sys.argv[1]
d = json.load(open(p))
area = d.get("area", "")
india_like = area.lower() in ("india", "world")
visual_area = area.lower() in ("india", "world", "music", "festivals", "sports", "film", "art", "fashion", "cities", "food", "nature", "myth", "religion", "games")
E, W = [], []
def err(m): E.append(m)
def warn(m): W.append(m)
words = lambda s: len(re.findall(r"\w+", s or ""))

for k in ["schema_version", "id", "day", "area", "title", "as_of", "reading_minutes", "hero", "sections", "cards", "quiz", "quiz_bank", "prequestions", "images", "media", "sources", "verification", "best_facts", "side_dish", "offline_task"]:
    if k not in d: err(f"missing top-level key: {k}")
img = {i["id"]: i for i in d.get("images", [])}
med = {m["id"]: m for m in d.get("media", [])}
src = {s["id"]: s for s in d.get("sources", [])}
qall = {q["id"]: q for q in d.get("quiz", []) + d.get("quiz_bank", []) + d.get("prequestions", [])}
cards = {c["id"]: c for c in d.get("cards", [])}
no_image = {v.get("spotlight_id") for v in d.get("verification", []) if v.get("status") == "no_image"}

def refs(obj, where):
    for i in obj.get("image_ids", []) or []:
        if i not in img: err(f"{where}: unknown image_id {i}")
    if obj.get("image_id") and obj["image_id"] not in img: err(f"{where}: unknown image_id {obj['image_id']}")
    for m in obj.get("media_ids", []) or []:
        if m not in med: err(f"{where}: unknown media_id {m}")
    for s in obj.get("source_ids", []) or []:
        if s not in src: err(f"{where}: unknown source_id {s}")

secs = d.get("sections", [])
spots = [sp for s in secs for sp in s.get("spotlights", [])]
total_words = 0
if d.get("hero", {}).get("image_id") not in img: err("hero.image_id missing or unknown")
for s in secs:
    w = words(s.get("intro_md")); total_words += w
    if not 60 <= w <= 260: warn(f"section {s.get('id')}: intro {w} words (aim 80-200)")
    if not s.get("source_ids"): err(f"section {s.get('id')}: no source_ids")
    refs(s, f"section {s.get('id')}")
    for q in s.get("check", []):
        if q not in qall: err(f"section {s.get('id')}: check id {q} not found")
    v = s.get("visual")
    for vv in (v if isinstance(v, list) else [v] if v else []):
        refs(vv, f"visual in {s.get('id')}")
        for i in (vv.get("data") or {}).get("image_ids", []) if isinstance(vv.get("data"), dict) else []:
            if i not in img: err(f"visual in {s.get('id')}: unknown image {i}")
ids = set()
for sp in spots:
    sid = sp.get("id")
    if sid in ids: err(f"duplicate spotlight id {sid}")
    ids.add(sid)
    for k in ["kind", "name", "spot_it", "story_md"]:
        if not sp.get(k): err(f"spotlight {sid}: missing {k}")
    w = words(sp.get("story_md")); total_words += w + words(sp.get("spot_it")) + words(sp.get("memory_hook"))
    if not 50 <= w <= 170: warn(f"spotlight {sid}: story {w} words (aim 60-140)")
    if not sp.get("image_ids") and sid not in no_image: err(f"spotlight {sid}: no image and no 'no_image' verification note")
    refs(sp, f"spotlight {sid}")
    if sp.get("compare", {}).get("image_id") and sp["compare"]["image_id"] not in img: err(f"spotlight {sid}: compare image unknown")

bf = d.get("best_facts", [])
for f in bf:
    refs(f, "best_fact")
    if not f.get("source_ids"): err(f"best_fact without source: {f.get('fact','')[:50]}")
total_words += sum(words(f.get("fact")) for f in bf)
for c in d.get("cards", []):
    if c.get("type") not in ("fact", "cloze", "image", "map", "why", "compare"): err(f"card {c.get('id')}: bad type {c.get('type')}")
    refs(c, f"card {c.get('id')}")
    if c.get("type") in ("image", "compare") and not (c.get("image_id") or c.get("image_ids")): err(f"card {c.get('id')}: picture card without image")
QT = {"mcq", "true_false", "order", "map_pin", "image_id", "match", "higher_lower", "odd_one_out", "guess_clues", "compare", "listen_id"}
for q in qall.values():
    if q.get("type") not in QT: err(f"quiz {q.get('id')}: bad type {q.get('type')}")
    if not q.get("explanation"): err(f"quiz {q.get('id')}: no explanation")
    refs(q, f"quiz {q.get('id')}")
    t = q.get("type")
    if t in ("mcq", "odd_one_out", "image_id") and not (isinstance(q.get("answer"), int) and q.get("options") and q["answer"] < len(q["options"])): err(f"quiz {q.get('id')}: answer index invalid")
    if t == "map_pin" and not (q.get("target") or {}).get("lat"): err(f"quiz {q.get('id')}: map_pin needs target lat/lon/tolerance_km")
    if t == "order" and not isinstance(q.get("answer"), list): err(f"quiz {q.get('id')}: order needs answer list")
    if t == "match" and not isinstance(q.get("answer"), list): err(f"quiz {q.get('id')}: match needs answer pairs")
    if t == "guess_clues" and not q.get("clues"): err(f"quiz {q.get('id')}: guess_clues needs clues")
    if t == "compare" and len(q.get("image_ids") or []) != 2: err(f"quiz {q.get('id')}: compare needs 2 image_ids")
    if t == "image_id" and not q.get("image_id"): err(f"quiz {q.get('id')}: image_id quiz needs image_id")
for i in img.values():
    if not re.match(r"https://(upload|thumb)\.wikimedia\.org/", i.get("thumb_url", "")) and not i.get("thumb_url", "").startswith("https://"): err(f"image {i['id']}: bad thumb_url")
    for k in ["author", "license", "file_page", "alt"]:
        if not i.get(k): err(f"image {i['id']}: missing {k}")
for m in med.values():
    if not m.get("verified_on"): err(f"media {m['id']}: not verified")
for s in src.values():
    if not str(s.get("url", "")).startswith("http"): err(f"source {s['id']}: no url")
raw = json.dumps(d, ensure_ascii=False)
if "—" in raw: err(f"em dash found {raw.count(chr(8212))} times; rewrite those sentences")

core = [c for c in d.get("cards", []) if c.get("core")]
pic = [c for c in d.get("cards", []) if c.get("type") in ("image", "compare")]
qtypes = {q.get("type") for q in d.get("quiz", [])}
TH = [
    ("sections", len(secs), 12), ("spotlights", len(spots), 45 if india_like else 40),
    ("images", len(img), 80 if india_like else (55 if visual_area else 40)),
    ("media", len(med), 6 if visual_area else 2), ("best_facts", len(bf), 12),
    ("cards", len(d.get("cards", [])), 45), ("core cards", len(core), 20), ("picture cards", len(pic), 15 if visual_area else 10),
    ("quiz", len(d.get("quiz", [])), 18), ("quiz types", len(qtypes), 7), ("quiz_bank", len(d.get("quiz_bank", [])), 10),
    ("prequestions", len(d.get("prequestions", [])), 5), ("sources", len(src), 40), ("words", total_words, 5500),
]
for name, have, need in TH:
    (err if have < need else lambda m: None)(f"depth: {name} = {have}, need at least {need}")
if total_words > 10500: warn(f"words = {total_words}, cap is about 9,500")
if len(core) > 22: warn(f"core cards = {len(core)}, keep at 20")
print(json.dumps({"file": p, "area": area, "stats": {n: h for n, h, _ in TH}, "errors": E, "warnings": W[:40]}, ensure_ascii=False, indent=1))
sys.exit(1 if E else 0)
