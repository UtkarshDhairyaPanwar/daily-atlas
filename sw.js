// Daily Atlas service worker: shell precache, day files stale-while-revalidate, photos cache-first.
const SHELL = "atlas-shell-v2", DATA = "atlas-data-v2", IMG = "atlas-img-v1", CARD = "atlas-card-v1";
const SHELL_FILES = ["./", "./index.html", "./styles.css", "./app.js", "./manifest.webmanifest", "./icon.svg", "./icon-192.png", "./icon-512.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(SHELL).then(c => c.addAll(SHELL_FILES))); self.skipWaiting(); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("atlas-") && ![SHELL, DATA, IMG, CARD].includes(k)).map(k => caches.delete(k))))); self.clients.claim(); });
async function trim(name, max) { const c = await caches.open(name), ks = await c.keys(); for (let i = 0; i < ks.length - max; i++) await c.delete(ks[i]); }
self.addEventListener("fetch", e => {
  const r = e.request; if (r.method !== "GET") return;
  const u = new URL(r.url);
  if (/(upload|thumb)\.wikimedia\.org/.test(u.hostname) || /tile\.openstreetmap\.org|server\.arcgisonline\.com/.test(u.hostname)) {
    const name = /\/330px-/.test(u.pathname) ? CARD : IMG;
    e.respondWith(caches.open(name).then(async c => { const hit = await c.match(r); if (hit) return hit; const res = await fetch(r).catch(() => null); if (res && (res.ok || res.type === "opaque")) { c.put(r, res.clone()); if (name === IMG) trim(IMG, 600); } return res || new Response("", { status: 504 }); }));
    return;
  }
  if (u.origin === location.origin && u.pathname.includes("/data/")) {
    e.respondWith(caches.open(DATA).then(async c => { const hit = await c.match(r, { ignoreSearch: true }); const net = fetch(r).then(res => { if (res.ok) c.put(r, res.clone()); return res; }).catch(() => hit); return hit || net; }));
    return;
  }
  if (u.origin === location.origin || /fonts\.(googleapis|gstatic)\.com|cdnjs\.cloudflare\.com/.test(u.hostname)) {
    e.respondWith(fetch(r, u.origin === location.origin ? { cache: "no-cache" } : {}).then(res => { if (res.ok) caches.open(SHELL).then(c => c.put(r, res.clone())); return res; }).catch(() => caches.match(r).then(m => m || caches.match("./index.html"))));
  }
});
