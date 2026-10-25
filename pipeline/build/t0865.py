#!/usr/bin/env python3
"""Build data/days/0865.json: Citrus and scurvy (Food, tier B)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from t0865_sources import SOURCES
from t0865_content import SECTIONS, BEST_FACTS, CARDS, QUIZ, QUIZ_BANK, PREQ, VERIFICATION, SIDE_DISH, OFFLINE, MEDIA, STATS, HERO, GEO

ROOT = os.path.dirname(os.path.dirname(HERE))
IMAGES = json.load(open(os.path.join(HERE, "t0865_images.json")))

d = {
    "schema_version": 2,
    "id": "t0865",
    "day": 865,
    "area": "Food",
    "title": "Citrus and scurvy",
    "native_name": None,
    "as_of": "2026-10-25",
    "reading_minutes": 55,
    "hero": HERO,
    "geo": GEO,
    "stats": STATS,
    "prequestions": PREQ,
    "sections": SECTIONS,
    "cards": CARDS,
    "quiz": QUIZ,
    "quiz_bank": QUIZ_BANK,
    "images": IMAGES,
    "media": MEDIA,
    "sources": SOURCES,
    "verification": VERIFICATION,
    "best_facts": sorted(BEST_FACTS, key=lambda f: -f["score"]),
    "side_dish": SIDE_DISH,
    "offline_task": OFFLINE,
}
out = os.path.join(ROOT, "data", "days", "0865.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
print("wrote", out)
