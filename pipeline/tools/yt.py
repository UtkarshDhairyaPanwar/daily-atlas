#!/usr/bin/env python3
"""Verify YouTube videos exist and are embeddable.  python3 yt.py URL_OR_ID [...]  -> JSON list"""
import json, re, sys, urllib.parse, urllib.request
UA = {"User-Agent": "DailyAtlas/1.0"}
out = []
for a in sys.argv[1:]:
    m = re.search(r"(?:v=|youtu\.be/|embed/|shorts/)([\w-]{11})", a); vid = m.group(1) if m else a
    url = f"https://www.youtube.com/watch?v={vid}"
    try:
        with urllib.request.urlopen(urllib.request.Request("https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(url), headers=UA), timeout=20) as r:
            j = json.load(r)
        out.append({"id": vid, "ok": True, "title": j.get("title"), "channel": j.get("author_name"), "url": url, "embed_url": f"https://www.youtube-nocookie.com/embed/{vid}"})
    except Exception as e:
        out.append({"id": vid, "ok": False, "error": str(e)})
print(json.dumps(out, ensure_ascii=False, indent=1))
