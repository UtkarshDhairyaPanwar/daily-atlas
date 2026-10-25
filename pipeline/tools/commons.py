#!/usr/bin/env python3
"""Find and verify openly licensed images on Wikimedia Commons.

  python3 commons.py search "Kuchipudi dance" [--n 8]      -> candidates with size, licence, author, thumb
  python3 commons.py verify "File:A.jpg" "File:B.jpg" ...  -> image records ready for a day JSON (id left blank)

Only free licences pass (CC0, PD, CC BY, CC BY-SA). Prints JSON.
"""
import json, re, sys, urllib.parse, urllib.request, time
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "DailyAtlas/1.0 (personal learning app; ux.utkarsh)"}
FREE = re.compile(r"^(cc0|public domain|pd|cc by(-sa)?( \d\.\d)?( [a-z]{2,})?|attribution|no restrictions)", re.I)

def call(params):
    params.update(format="json", formatversion="2")
    url = API + "?" + urllib.parse.urlencode(params)
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except Exception as e:
            time.sleep(2 * (i + 1)); err = e
    raise SystemExit(f"commons api failed: {err}")

def clean(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()

def record(p):
    ii = (p.get("imageinfo") or [{}])[0]
    m = ii.get("extmetadata", {})
    lic = clean(m.get("LicenseShortName", {}).get("value", ""))
    author = clean(m.get("Artist", {}).get("value", "")) or "Unknown"
    if len(author) > 80: author = author[:77] + "..."
    thumb = (ii.get("thumburl") or ii.get("url") or "").split("?")[0]
    return {
        "id": "", "file_page": ii.get("descriptionurl", ""), "url": ii.get("url", "").split("?")[0], "thumb_url": thumb,
        "width": ii.get("width"), "height": ii.get("height"), "author": author, "license": lic,
        "license_url": m.get("LicenseUrl", {}).get("value", ""),
        "attribution": f"Photo: {author}, {lic}, via Wikimedia Commons",
        "description": clean(m.get("ImageDescription", {}).get("value", ""))[:200],
        "free": bool(FREE.match(lic)), "title": p.get("title"), "verified_on": time.strftime("%Y-%m-%d"),
    }

def search(q, n=8):
    d = call({"action": "query", "generator": "search", "gsrsearch": q + " filetype:bitmap", "gsrnamespace": 6, "gsrlimit": n,
              "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1280})
    out = [record(p) for p in d.get("query", {}).get("pages", [])]
    return [r for r in out if r["free"] and (r["width"] or 0) >= 500]

def verify(titles):
    out = []
    for i in range(0, len(titles), 40):
        chunk = [t if t.startswith("File:") else "File:" + t for t in titles[i:i + 40]]
        d = call({"action": "query", "titles": "|".join(chunk), "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1280})
        for p in d.get("query", {}).get("pages", []):
            if p.get("missing"): out.append({"title": p.get("title"), "error": "missing"}); continue
            out.append(record(p))
    return out

if __name__ == "__main__":
    if len(sys.argv) < 3: print(__doc__); sys.exit(1)
    if sys.argv[1] == "search":
        n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 8
        print(json.dumps(search(sys.argv[2], n), ensure_ascii=False, indent=1))
    elif sys.argv[1] == "verify":
        print(json.dumps(verify(sys.argv[2:]), ensure_ascii=False, indent=1))
