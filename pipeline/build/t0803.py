#!/usr/bin/env python3
"""Build data/days/0803.json: Hyperinflation: Weimar, Zimbabwe, Venezuela."""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from t0803_images import IMAGE_RECORDS  # verified Commons records keyed by our image id
from t0803_content import SECTIONS, SOURCES, BEST_FACTS, CARDS, QUIZ, QUIZ_BANK, PREQ, VERIFICATION, SIDE_DISH, OFFLINE, MEDIA, STATS, HERO

ACC = "2026-10-25"

# Images: keep only ids with a verified record.
images = []
for iid, rec in IMAGE_RECORDS.items():
    r = dict(rec)
    r["id"] = iid
    for k in ("free", "title", "description"):
        r.pop(k, None)
    r.setdefault("verified_on", ACC)
    images.append(r)
have = {i["id"] for i in images}

verification = list(VERIFICATION)
for s in SECTIONS:
    if s.get("visual"):
        v = s["visual"]
        if isinstance(v.get("data"), dict) and "image_ids" in v["data"]:
            v["data"]["image_ids"] = [i for i in v["data"]["image_ids"] if i in have]
        if isinstance(v.get("data"), dict):
            for side in ("left", "right"):
                if side in v["data"] and v["data"][side].get("image_id") not in have:
                    v["data"][side]["image_id"] = None
    for sp in s["spotlights"]:
        sp["image_ids"] = [i for i in sp.get("image_ids", []) if i in have]
        sp.setdefault("media_ids", [])
        if sp.get("compare") and sp["compare"].get("image_id") not in have:
            sp["compare"].pop("image_id", None)
        if not sp["image_ids"]:
            verification.append({"claim": f"Photo for spotlight '{sp['name']}'", "status": "no_image",
                                 "note": "No openly licensed Commons image that clearly shows this subject was found and verified.",
                                 "spotlight_id": sp["id"]})

def fix_imgref(o):
    if o.get("image_id") and o["image_id"] not in have:
        o.pop("image_id")
    if o.get("image_ids"):
        o["image_ids"] = [i for i in o["image_ids"] if i in have]

cards = []
for c in CARDS:
    c = dict(c)
    fix_imgref(c)
    if c["type"] in ("image", "compare") and not c.get("image_id"):
        c["type"] = "fact"
    if c["type"] == "compare" and len(c.get("image_ids") or []) != 2:
        c["type"] = "image" if c.get("image_id") else "fact"
    cards.append(c)

def fix_quiz(lst):
    out = []
    for q in lst:
        q = dict(q)
        fix_imgref(q)
        if q["type"] == "image_id" and not q.get("image_id"):
            q["type"] = "mcq"
        if q["type"] == "compare" and len(q.get("image_ids") or []) != 2:
            continue
        out.append(q)
    return out

hero = dict(HERO)
if hero["image_id"] not in have:
    hero["image_id"] = images[0]["id"]

side = dict(SIDE_DISH)
side["image_ids"] = [i for i in side.get("image_ids", []) if i in have]

day = {
    "schema_version": 2,
    "id": "t0803",
    "day": 803,
    "area": "Money",
    "title": "Hyperinflation: Weimar, Zimbabwe, Venezuela",
    "native_name": None,
    "as_of": ACC,
    "reading_minutes": 55,
    "hero": hero,
    "geo": None,
    "stats": STATS,
    "prequestions": fix_quiz(PREQ),
    "sections": SECTIONS,
    "cards": cards,
    "quiz": fix_quiz(QUIZ),
    "quiz_bank": fix_quiz(QUIZ_BANK),
    "images": images,
    "media": MEDIA,
    "sources": [dict(s, accessed=ACC) for s in SOURCES],
    "verification": verification,
    "best_facts": sorted(BEST_FACTS, key=lambda f: -f["score"]),
    "side_dish": side,
    "offline_task": OFFLINE,
}

raw = json.dumps(day, ensure_ascii=False, indent=1)
bad = [w for w in ["—", "rich tapestry", "vibrant", "delve", "nestled", "testament to", "melting pot", "hidden gem", "boasts"] if w in raw.lower()]
if bad:
    print("WARNING banned:", bad)
txt_only = json.dumps([SECTIONS, BEST_FACTS, CARDS, QUIZ, QUIZ_BANK, PREQ, SIDE_DISH, OFFLINE], ensure_ascii=False)
if "!" in txt_only:
    print("WARNING exclamation marks:", txt_only.count("!"))
out = os.path.join(ROOT, "data", "days", "0803.json")
with open(out, "w", encoding="utf-8") as f:
    f.write(raw)
print("wrote", out, "images", len(images))
