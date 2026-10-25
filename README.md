# Daily Atlas

One place a day, learned like a piano practice session: warm up on old cards, read the place through picture-led spotlights, lock in 20 core cards, play recall games, explain it back, close with a test and a stamp.

## Run locally
```
python3 -m http.server 8766
```
Open http://localhost:8766. On iPhone: open in Safari, Share, Add to Home Screen (keeps progress safe and works offline).

## Files
- `index.html`, `styles.css`, `app.js`: the app. No build step.
- `plan.js`: the route through India (42 days: 36 places + review days). A day appears once it has a `file`.
- `data/day-01.json`: Andhra Pradesh, schema v2 (`../../refs/schema-v2.md`).
- `data/india-states.geojson`: state outlines. DataMeet via geoBoundaries, CC BY 2.5 IN.
- `sw.js`, `manifest.webmanifest`, icons: installable, offline app.

## Adding a day
1. Write `data/day-NN.json` in schema v2.
2. Add `file: "data/day-NN.json"` to that day in `plan.js`.
3. Bump the cache names in `sw.js` if the shell changed.

## Progress
Stored on the phone in IndexedDB. Settings has Export / Import for backups. Every review is logged so the scheduler can move to FSRS later.

## Credits
Photos: Wikimedia Commons (credited per image). Maps: OpenStreetMap, Esri. Video: embedded from YouTube channels named on each clip; nothing is downloaded.
