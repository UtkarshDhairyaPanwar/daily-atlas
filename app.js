/* Daily Atlas. One place a day: warm up, read, learn, play, make, close.
   Progress lives in IndexedDB on the phone. Content lives in data/day-NN.json (schema v2). */
(() => {
"use strict";

// ---------- tiny helpers ----------
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const pad2 = n => String(n).padStart(2, "0");
const plural = (n, w) => `${n} ${w}${n === 1 ? "" : "s"}`;
const ICON_X = '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></svg>';
const ICON_BACK = '<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>';

// Markdown, small subset: paragraphs, - lists, **b**, *i*, [a](url), | tables |
function md(src) {
  if (!src) return "";
  const inline = t => esc(t)
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/(^|[^*])\*(?!\s)(.+?)\*/g, "$1<em>$2</em>")
    .replace(/\[(.+?)\]\((https?:[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  return String(src).trim().split(/\n{2,}/).map(block => {
    const lines = block.split("\n");
    if (lines.every(l => /^\s*[-*] /.test(l))) return "<ul>" + lines.map(l => "<li>" + inline(l.replace(/^\s*[-*] /, "")) + "</li>").join("") + "</ul>";
    if (lines.every(l => /^\s*\|/.test(l))) {
      const rows = lines.filter(l => !/^\s*\|[\s:-]+\|/.test(l.replace(/[^|:\-\s]/g, "x")) || /[a-z0-9]/i.test(l))
        .filter(l => !/^\s*\|(\s*:?-+:?\s*\|)+\s*$/.test(l))
        .map(l => l.trim().replace(/^\||\|$/g, "").split("|").map(c => c.trim()));
      const [h, ...b] = rows;
      return '<div class="tbl"><table><thead><tr>' + h.map(c => "<th>" + inline(c) + "</th>").join("") + "</tr></thead><tbody>" +
        b.map(r => "<tr>" + r.map(c => "<td>" + inline(c) + "</td>").join("") + "</tr>").join("") + "</tbody></table></div>";
    }
    return "<p>" + lines.map(inline).join("<br>") + "</p>";
  }).join("");
}

// ---------- dates ----------
const DAY_MS = 864e5;
const dayN = (d = new Date()) => Math.floor((d.getTime() - d.getTimezoneOffset() * 6e4) / DAY_MS);
const nToDate = n => new Date(n * DAY_MS + new Date().getTimezoneOffset() * 6e4);
const dStr = n => { const d = nToDate(n); return `${d.getFullYear()}-${pad2(d.getMonth() + 1)}-${pad2(d.getDate())}`; };
const WD = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

// ---------- storage: IndexedDB with localStorage fallback ----------
const STORE_KEY = "daily-atlas-v1";
const Store = {
  db: null,
  async open() {
    try {
      this.db = await new Promise((res, rej) => {
        const r = indexedDB.open("daily-atlas", 1);
        r.onupgradeneeded = () => r.result.createObjectStore("kv");
        r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error);
      });
    } catch (e) { this.db = null; }
  },
  async get() {
    if (this.db) {
      try {
        return await new Promise((res, rej) => { const t = this.db.transaction("kv").objectStore("kv").get(STORE_KEY); t.onsuccess = () => res(t.result); t.onerror = () => rej(t.error); });
      } catch (e) {}
    }
    try { return JSON.parse(localStorage.getItem(STORE_KEY) || "null"); } catch (e) { return null; }
  },
  async set(v) {
    if (this.db) {
      try { await new Promise((res, rej) => { const t = this.db.transaction("kv", "readwrite"); t.objectStore("kv").put(v, STORE_KEY); t.oncomplete = res; t.onerror = () => rej(t.error); }); return; } catch (e) {}
    }
    try { localStorage.setItem(STORE_KEY, JSON.stringify(v)); } catch (e) {}
  }
};

const fresh = () => ({
  v: 1, created: dayN(),
  progress: {},      // dayId -> { read:{secId:true}, seen:{spotId:true}, steps:{warm,read,learn,play,make,close}, pre:{}, explain:"", whys:{}, offline:false, score, completedOn, learnedAhead }
  cards: {},         // cardId -> { d:dayId, step, due, lapses, reps, added, last }
  days: {},          // "YYYY-MM-DD" -> { dueAtStart, reviews, learned, games, target }
  log: [],           // [dayN, cardId, rating]
  settings: { minNew: 20, cue: "", theme: "auto" }
});
let S = fresh();
let saveT = 0;
const save = () => { clearTimeout(saveT); saveT = setTimeout(() => Store.set(S), 250); };

// ---------- spaced repetition: fixed ladder, log everything for FSRS later ----------
const LADDER = [1, 3, 7, 16, 35, 80, 180];
const now = () => dayN();
function rate(cardId, r) {   // r: 0 again, 1 good, 2 easy
  const c = S.cards[cardId]; if (!c) return;
  const t = now();
  if (r === 0) { c.step = 0; c.lapses = (c.lapses || 0) + 1; c.due = t + 1; }
  else { c.step = Math.min((c.step ?? -1) + r, LADDER.length - 1); c.due = t + LADDER[c.step]; }
  c.reps = (c.reps || 0) + 1; c.last = t;
  S.log.push([t, cardId, r]);
  rec().reviews++;
  save();
}
function addCard(card, dayId) {
  if (S.cards[card.id]) return false;
  S.cards[card.id] = { d: dayId, step: 0, due: now() + LADDER[0], lapses: 0, reps: 0, added: now(), last: now() };
  rec().learned++;
  save(); return true;
}
const dueIds = () => { const t = now(); return Object.keys(S.cards).filter(id => S.cards[id].due <= t).sort((a, b) => S.cards[a].due - S.cards[b].due); };

// Forecast: assume every review is passed. Returns reviews due on each of the next 7 days.
function forecast(extraNew = 0) {
  const t = now(), out = Array(7).fill(0), add = Array(7).fill(0);
  const sim = (step, due, bucket) => {
    if (due <= t) { step = Math.min(step + 1, LADDER.length - 1); due = t + LADDER[step]; }
    while (due <= t + 7) { bucket[due - t - 1]++; step = Math.min(step + 1, LADDER.length - 1); due += LADDER[step]; }
  };
  Object.values(S.cards).forEach(c => sim(c.step, c.due, out));
  for (let i = 0; i < extraNew; i++) sim(0, t + 1, add);
  return { base: out, add };
}

// ---------- day record, floor, streak ----------
function rec(n = now()) {
  const k = dStr(n);
  if (!S.days[k]) S.days[k] = { dueAtStart: n === now() ? dueIds().length : 0, reviews: 0, learned: 0, games: 0, target: currentEntry()?.id };
  return S.days[k];
}
const P = id => (S.progress[id] ||= { read: {}, seen: {}, steps: {}, pre: {}, whys: {} });

function currentEntry() {
  const open = e => !(S.progress[e.id] && S.progress[e.id].completedOn != null);
  return PLAN.find(e => open(e) && e.file) || PLAN.find(open) || PLAN[PLAN.length - 1];
}
function todayTarget() {
  // Today's place stays on screen for the rest of the day once finished; tomorrow moves on.
  const r = rec(); const e = PLAN.find(x => x.id === r.target);
  return (e && (P(e.id).completedOn == null || P(e.id).completedOn === now())) ? e : currentEntry();
}

function floor(entry, data) {
  const r = rec();
  const dueLeft = dueIds().filter(id => S.cards[id].added < now()).length;
  const reviewGoal = Math.max(r.dueAtStart, 0);
  const reviewDone = reviewGoal === 0 ? 1 : clamp(1 - dueLeft / reviewGoal, 0, 1);
  let readDone = 0, cardsDone = 0, coreN = 0, learnedN = 0;
  if (data) {
    const p = P(entry.id);
    const secs = data.sections || [];
    readDone = secs.length ? Object.keys(p.read).filter(k => secs.some(s => s.id === k)).length / secs.length : 0;
    const core = coreCards(data);
    coreN = core.length; learnedN = core.filter(c => S.cards[c.id]).length;
    cardsDone = coreN ? learnedN / coreN : 1;
  } else {
    // No content for this day (review day or still being written): the floor is clearing due reviews.
    return { reviewDone, readDone: 1, cardsDone: 1, dueLeft, reviewGoal, coreN, learnedN, met: reviewGoal > 0 && dueLeft === 0 };
  }
  return { reviewDone, readDone, cardsDone, dueLeft, reviewGoal, coreN, learnedN, met: reviewDone >= 1 && readDone >= .99 && cardsDone >= 1 };
}
function studied(k) {
  const r = S.days[k]; if (!r) return false;
  if (r.floor) return true;
  const shortReviews = Math.min(r.dueAtStart || 0, 60);
  return (r.reviews >= shortReviews && r.reviews > 0 && r.games > 0) || (r.reviews >= 20) || (r.learned >= 10);
}
function streak() {
  // Consecutive studied days, 2 automatic freezes per calendar month.
  let n = now(); const fro = {}; let count = 0, frozen = [];
  if (!studied(dStr(n))) n--;
  for (let i = 0; i < 800; i++, n--) {
    const k = dStr(n);
    if (studied(k)) { count++; continue; }
    if (n < S.created) break;
    const m = k.slice(0, 7);
    if ((fro[m] || 0) < 2 && count > 0) { fro[m] = (fro[m] || 0) + 1; frozen.push(k); continue; }
    break;
  }
  return { count, frozen };
}

// ---------- data ----------
const cache = {};
async function loadDay(entry) {
  if (!entry || !entry.file) return null;
  if (cache[entry.id]) return cache[entry.id];
  try {
    const r = await fetch(entry.file, { cache: "no-cache" });
    if (!r.ok) throw 0;
    const d = await r.json();
    d._img = Object.fromEntries((d.images || []).map(i => [i.id, i]));
    d._media = Object.fromEntries((d.media || []).map(i => [i.id, i]));
    d._src = Object.fromEntries((d.sources || []).map(i => [i.id, i]));
    d._cards = Object.fromEntries((d.cards || []).map(i => [i.id, i]));
    d._q = Object.fromEntries([...(d.quiz_bank || []), ...(d.prequestions || []), ...(d.quiz || [])].map(i => [i.id, i]));
    d._spots = {};
    (d.sections || []).forEach(s => (s.spotlights || []).forEach(sp => { d._spots[sp.id] = sp; sp._sec = s.id; }));
    d._entry = entry;
    cache[entry.id] = d;
    return d;
  } catch (e) { return null; }
}
async function loadDeckDays() {
  const ids = new Set(Object.values(S.cards).map(c => c.d));
  await Promise.all(PLAN.filter(e => ids.has(e.id)).map(loadDay));
}
function cardContent(id) {
  const c = S.cards[id]; if (!c) return null;
  const d = cache[c.d]; if (!d) return null;
  const cc = d._cards[id]; return cc ? { card: cc, data: d } : null;
}
function coreCards(d) {
  const all = d.cards || [];
  const core = all.filter(c => c.core);
  return core.length ? core : all.slice(0, S.settings.minNew);
}

// image url at a Wikimedia standard width
const WIDTHS = [330, 500, 960, 1280];
function imgUrl(img, w = 960) {
  if (!img) return "";
  const t = img.thumb_url || "";
  if (/\/\d+px-/.test(t)) {
    const ow = img.width || 99999;
    const ww = WIDTHS.find(x => x >= w) || 1280;
    if (ww >= ow && img.url && !/\.svg$/i.test(img.url)) return img.url;
    return t.replace(/\/\d+px-/, `/${ww}px-`);
  }
  return t || img.url || "";
}
const credit = img => img ? `<div class="credit">${esc(img.attribution || [img.author, img.license].filter(Boolean).join(", "))}${img.file_page ? ` · <a href="${esc(img.file_page)}" target="_blank" rel="noopener">source</a>` : ""}</div>` : "";

// ---------- UI plumbing ----------
const app = $("#app");
let cleanup = [];
function setView(html, { tab = null, tabbar = true } = {}) {
  cleanup.forEach(f => { try { f(); } catch (e) {} }); cleanup = [];
  document.body.classList.toggle("no-tab", !tabbar);
  $$("#tabbar a").forEach(a => a.classList.toggle("on", a.dataset.tab === tab));
  app.innerHTML = html;
  window.scrollTo(0, 0);
}
function toast(msg, ms = 2200) { const t = $("#toast"); t.textContent = msg; t.hidden = false; clearTimeout(toast.t); toast.t = setTimeout(() => t.hidden = true, ms); }
function sheet(html, bind) {
  const w = $("#sheet"); w.innerHTML = `<div class="sheet" role="dialog" aria-modal="true">${html}</div>`; w.hidden = false;
  const close = () => { w.hidden = true; w.innerHTML = ""; };
  w.onclick = e => { if (e.target === w || e.target.closest("[data-close]")) close(); };
  bind && bind($(".sheet", w), close);
  return close;
}
const topbar = (title, back = "#/today", progress = null, extra = "") =>
  `<div class="topbar lined"><a class="x" href="${back}" aria-label="Close">${ICON_X}</a><div class="title">${esc(title)}</div>${extra}${progress != null ? `<div class="progress"><i style="width:${progress * 100}%"></i></div>` : ""}</div>`;

// full-screen photo viewer
function openViewer(images, start = 0) {
  const v = $("#viewer");
  v.innerHTML = `<button class="vx" aria-label="Close">✕</button><div class="track">${images.map(i => `<div class="slide"><img src="${esc(imgUrl(i, 1280))}" alt="${esc(i.alt)}"></div>`).join("")}</div><div class="vcap"></div>`;
  v.hidden = false; document.body.style.overflow = "hidden";
  const track = $(".track", v), cap = $(".vcap", v);
  const show = k => { const i = images[k]; cap.innerHTML = `<div>${esc(i.caption || i.alt || "")}</div>${credit(i)}<div class="credit">${k + 1} / ${images.length}</div>`; };
  requestAnimationFrame(() => { track.scrollLeft = start * track.clientWidth; show(start); });
  track.onscroll = () => show(Math.round(track.scrollLeft / track.clientWidth));
  const close = () => { v.hidden = true; v.innerHTML = ""; document.body.style.overflow = ""; };
  $(".vx", v).onclick = close;
  let y0 = null; v.ontouchstart = e => { y0 = e.touches.length === 1 ? e.touches[0].clientY : null; };
  v.ontouchend = e => { if (y0 != null && e.changedTouches[0].clientY - y0 > 120) close(); y0 = null; };
}

// ---------- maps (Leaflet) ----------
// Tiles: OpenStreetMap (labels) for reading maps; Esri shaded relief (no labels) for map games.
const TILE_LABELS = "https://tile.openstreetmap.org/{z}/{x}/{y}.png";
const TILE_PLAIN = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}";
const ATTR_OSM = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>';
const ATTR_ESRI = 'Relief &copy; Esri · Boundaries: DataMeet via geoBoundaries, CC BY 2.5 IN';
let STATES = null;
const loadStates = () => STATES || (STATES = fetch("data/india-states.geojson").then(r => r.json()).catch(() => null));
const geoName = t => String(t || "").replace(/&/g, "and").replace(/\s*\(.*\)/, "").trim().toLowerCase();
function makeMap(el, data, { labels = true, interactive = true, fitPts = null } = {}) {
  if (!window.L) { el.innerHTML = '<div class="pad small faint">Map needs internet.</div>'; return null; }
  const m = L.map(el, { zoomSnap: 0.25, zoomControl: false, attributionControl: true, scrollWheelZoom: false, dragging: interactive, touchZoom: interactive, doubleClickZoom: interactive, tap: true });
  L.tileLayer(labels ? TILE_LABELS : TILE_PLAIN, { attribution: labels ? ATTR_OSM : ATTR_ESRI, maxZoom: labels ? 12 : 13 }).addTo(m);
  let b = data?.geo?.bbox; const c = data?.geo?.centroid;
  // schema says [s, w, n, e]; accept [w, s, e, n] too by checking the centroid falls inside
  if (b && b.length === 4 && c && !(c[0] >= b[0] && c[0] <= b[2] && c[1] >= b[1] && c[1] <= b[3])) b = [b[1], b[0], b[3], b[2]];
  if (b && b.length === 4) m.fitBounds([[b[0], b[1]], [b[2], b[3]]], { padding: [10, 10] });
  else if (fitPts && fitPts.length) fitPts.length === 1 ? m.setView([fitPts[0].lat, fitPts[0].lon], 5) : m.fitBounds(fitPts.map(p => [p.lat, p.lon]), { padding: [28, 28], maxZoom: 9 });
  else m.setView(data?.geo?.centroid || [20, 10], data?.geo?.centroid ? 5 : 1.5);
  // state outlines: today's state strong, the rest faint
  loadStates().then(fc => {
    if (!fc || !m._container) return;
    const me = geoName(data?.title);
    L.geoJSON(fc, { interactive: false, style: f => geoName(f.properties.name) === me
      ? { color: "#B4442A", weight: 2.5, fillColor: "#B4442A", fillOpacity: labels ? 0.04 : 0.1 }
      : { color: "#4A443B", weight: 1, opacity: .45, fillOpacity: 0 } }).addTo(m);
  });
  cleanup.push(() => m.remove());
  return m;
}
const dot = (color = "#B4442A") => L.divIcon({ className: "", html: `<div style="width:14px;height:14px;border-radius:7px;background:${color};border:2.5px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.35)"></div>`, iconSize: [14, 14], iconAnchor: [7, 7] });
// Pins that sit on top of earlier ones are nudged sideways so both numbers stay readable.
const numPin = (n, near = 0) => L.divIcon({ className: "", html: `<div class="npin">${n}</div>`, iconSize: [22, 22], iconAnchor: [11 - near * 20, 11 + near * 6] });
function lazyMount(el, fn) {
  const io = new IntersectionObserver(es => { if (es.some(e => e.isIntersecting)) { io.disconnect(); fn(); } }, { rootMargin: "200px" });
  io.observe(el); cleanup.push(() => io.disconnect());
}
const kmBetween = (a, b) => { const R = 6371, r = Math.PI / 180, dLa = (b[0] - a[0]) * r, dLo = (b[1] - a[1]) * r; const h = Math.sin(dLa / 2) ** 2 + Math.cos(a[0] * r) * Math.cos(b[0] * r) * Math.sin(dLo / 2) ** 2; return 2 * R * Math.asin(Math.sqrt(h)); };

// ---------- visuals ----------
const PALETTE = ["#B4442A", "#2B3C6B", "#B8862A", "#2F7D4F", "#7A7266", "#8E5A9B"];
function renderVisual(v, d) {
  if (!v || !v.type) return "";
  const t = v.title ? `<div class="vt">${esc(v.title)}</div>` : "";
  const data = v.data;
  const id = "v" + Math.random().toString(36).slice(2, 8);
  switch (v.type) {
    case "stat_tiles": return `<div class="vis">${t}<div class="tiles">${(data || []).map(x => `<div class="tile"><div class="l">${esc(x.label)}</div><div class="v">${esc(x.value)}</div>${x.note ? `<div class="n">${esc(x.note)}</div>` : ""}</div>`).join("")}</div></div>`;
    case "map": case "map_points": case "map_locator": case "map_regions": {
      const pts = Array.isArray(data) ? data.filter(p => p.lat != null) : (data?.pins || data?.points || []);
      const regs = Array.isArray(data) ? data.filter(p => p.lat == null && p.name) : [];
      const img = (v.image_ids || []).map(i => d._img[i]).filter(Boolean)[0];
      if (!pts.length && img) return `<div class="vis">${t}<button data-view="${esc(img.id)}" style="width:100%;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:10px"><img src="${esc(imgUrl(img, 500))}" alt="${esc(img.alt)}" loading="lazy" style="max-height:340px;margin:0 auto"></button>${credit(img)}</div>`;
      if (regs.length && !pts.length) return `<div class="vis">${t}<div class="stack">${regs.map((r, i) => `<div class="tile"><div class="l" style="color:${PALETTE[i % 6]}">${esc(r.name)}</div><div class="small muted">${esc(r.note || "")}</div></div>`).join("")}</div></div>`;
      const many = pts.length > 3;
      queueMicrotask(() => { const el = document.getElementById(id); if (el) lazyMount(el, () => { const m = makeMap(el, d, { fitPts: pts }); if (!m) return; pts.forEach((p, k) => L.marker([p.lat, p.lon], { icon: many ? numPin(k + 1, pts.slice(0, k).filter(q => Math.abs(q.lat - p.lat) < .35 && Math.abs(q.lon - p.lon) < .35).length) : dot() }).addTo(m).bindTooltip(esc(p.label), { permanent: !many, direction: "top", className: "pin-label", offset: [0, -8] })); }); });
      return `<div class="vis">${t}<div class="map" id="${id}"></div>${many ? `<ol class="pinlist">${pts.map((p, k) => `<li${p.spotlight_id ? ` data-jump="${esc(p.spotlight_id)}"` : ""}><i>${k + 1}</i>${esc(p.label)}</li>`).join("")}</ol>` : ""}</div>`;
    }
    case "timeline": if ((data || [])[0]?.start != null) return renderVisual({ ...v, type: "dynasty_band" }, d);
      return `<div class="vis">${t}<div class="tl">${(data || []).map(x => `<div><b>${esc(x.year ?? x.date)}</b><span>${esc(x.event ?? x.label)}</span></div>`).join("")}</div></div>`;
    case "dynasty_band": {
      const rows = data || []; if (!rows.length) return "";
      const min = Math.min(...rows.map(r => r.start)), max = Math.max(...rows.map(r => r.end));
      const pct = y => ((y - min) / (max - min)) * 100;
      const yr = y => y < 0 ? `${-y} BCE` : `${y}`;
      const step = (max - min) > 1500 ? 500 : 250; const ticks = []; for (let y = Math.ceil(min / step) * step; y < max; y += step) ticks.push(y);
      const tickBg = ticks.map(y => `linear-gradient(var(--line-2),var(--line-2)) ${pct(y)}% 0/1px 100% no-repeat`).join(",");
      const axis = `<span style="left:0">${yr(min)}</span>${ticks.filter(y => pct(y) > 18 && pct(y) < 85).map(y => `<span style="left:${pct(y)}%">${y === 0 ? "1 CE" : yr(y)}</span>`).join("")}<span style="left:100%">${yr(max)}</span>`;
      return `<div class="vis">${t}<div class="gantt" style="--ticks:${tickBg}"><div class="gax top">${axis}</div>${rows.map((r, i) => `<div class="g"><div class="gl"><b>${esc(r.name)}</b><span>${yr(r.start)} to ${yr(r.end)}${r.note ? ` · ${esc(r.note)}` : ""}</span></div><div class="gt"><i style="left:${pct(r.start)}%;width:${Math.max(1.2, pct(r.end) - pct(r.start))}%;"></i></div></div>`).join("")}<div class="gax"><span style="left:0">${yr(min)}</span>${ticks.filter(y => pct(y) > 18 && pct(y) < 85).map(y => `<span style="left:${pct(y)}%">${y === 0 ? "1 CE" : yr(y)}</span>`).join("")}<span style="left:100%">${yr(max)}</span></div></div></div>`;
    }
    case "bar": {
      const rows = data || []; if (!rows.length) return "";
      const keys = Object.keys(rows[0]).filter(k => typeof rows[0][k] === "number");
      const names = { ap: "AP", india: "India" };
      return `<div class="vis">${t}<div class="bars">${rows.map(r => { const mx = Math.max(...keys.map(k => r[k])); return `<div class="b"><div class="lab">${esc(r.metric || r.label)}</div>${keys.map((k, i) => `<div class="tr ${i ? "alt" : ""}"><span>${esc(names[k] || k)}</span><i style="width:${(r[k] / mx) * 70}%"></i>${esc(r[k].toLocaleString("en-IN"))}</div>`).join("")}</div>`; }).join("")}</div></div>`;
    }
    case "donut": {
      const rows = data || []; const tot = rows.reduce((a, r) => a + r.value, 0) || 1; let acc = 0;
      const arcs = rows.map((r, i) => { const a0 = acc / tot * Math.PI * 2, a1 = (acc += r.value) / tot * Math.PI * 2, R = 44, cx = 50, cy = 50; const p = (a) => [cx + R * Math.sin(a), cy - R * Math.cos(a)]; const [x0, y0] = p(a0), [x1, y1] = p(a1 - 0.0001); return `<path d="M${x0} ${y0}A${R} ${R} 0 ${a1 - a0 > Math.PI ? 1 : 0} 1 ${x1} ${y1}" stroke="${PALETTE[i % 6]}" stroke-width="14" fill="none"/>`; }).join("");
      return `<div class="vis">${t}<div class="donut"><svg viewBox="0 0 100 100" width="120" height="120">${arcs}</svg><ul>${rows.map((r, i) => `<li><i style="background:${PALETTE[i % 6]}"></i>${esc(r.label)} <b>${esc(r.value)}%</b></li>`).join("")}</ul></div></div>`;
    }
    case "comparison": {
      const parts = ["before", "after", "reference"].map(k => data?.[k]).filter(Boolean);
      return `<div class="vis">${t}<div class="numcmp">${parts.map(p => `<div><div class="eyebrow">${esc(p.label)}</div><div class="v">${esc(p.value.toLocaleString("en-IN"))} ${esc(p.unit || "")}</div>${p.rank ? `<div class="tiny faint">${esc(p.rank)}</div>` : ""}</div>`).join("")}</div></div>`;
    }
    case "compare": {
      const L0 = data?.a || data?.left, R0 = data?.b || data?.right;
      const a = d._img[L0?.image_id], b = d._img[R0?.image_id];
      if (!a || !b) return "";
      const rows = data.rows || [];
      return `<div class="vis">${t}<div class="cmp"><figure><button data-view="${a.id}"><img src="${esc(imgUrl(a, 500))}" alt="${esc(a.alt)}" loading="lazy"></button><figcaption>${esc(L0.label)}</figcaption></figure><figure><button data-view="${b.id}"><img src="${esc(imgUrl(b, 500))}" alt="${esc(b.alt)}" loading="lazy"></button><figcaption>${esc(R0.label)}</figcaption></figure>${data.difference ? `<div class="diff">${esc(data.difference)}</div>` : ""}</div>${rows.length ? renderVisual({ type: "table", data: rows }, d).replace('class="tbl"', 'class="tbl cmpt"') : ""}</div>`;
    }
    case "table": {
      const rows = data || []; if (!rows.length) return "";
      const keys = Object.keys(rows[0]);
      return `<div class="vis">${t}<div class="tbl"><table><thead><tr>${keys.map(k => `<th>${esc(k.replace(/_/g, " "))}</th>`).join("")}</tr></thead><tbody>${rows.map(r => `<tr>${keys.map(k => `<td>${esc(r[k])}</td>`).join("")}</tr>`).join("")}</tbody></table></div></div>`;
    }
    case "calendar": case "ring": {
      const rows = data || []; const by = {}; rows.forEach(r => (by[r.month] ||= []).push(r.name || r.label));
      return `<div class="vis">${t}<div class="cal">${MON.map((m, i) => `<div class="${by[i + 1] ? "" : "off"}"><b>${m.slice(0, 3)}</b>${(by[i + 1] || []).map(n => `<p>${esc(n)}</p>`).join("")}</div>`).join("")}</div></div>`;
    }
    case "progress": return `<div class="vis">${t}<div class="prog">${(data || []).map(p => `<div class="p"><div><span>${esc(p.label)}</span><b>${esc(p.value)}%</b></div><div class="progress"><i style="width:${clamp(p.value, 0, 100)}%"></i></div></div>`).join("")}</div></div>`;
    case "fact_cards": return `<div class="vis">${t}<div class="tiles">${(data || []).map(x => `<div class="tile"><div class="v" style="font-size:28px">${esc(x.text)}</div><div class="n">${esc(x.label)}</div></div>`).join("")}</div></div>`;
    case "photo_grid": case "portrait_deck": {
      const imgs = (v.image_ids || data?.image_ids || []).map(i => d._img[i]).filter(Boolean);
      if (!imgs.length) return Array.isArray(data) && data.length ? `<div class="vis">${t}<div class="chips">${data.map(x => `<span class="chip">${esc(typeof x === "string" ? x : x.name)}</span>`).join("")}</div></div>` : "";
      return `<div class="vis">${t}<div class="cmp">${imgs.map(i => `<figure><button data-view="${i.id}"><img src="${esc(imgUrl(i, 500))}" alt="${esc(i.alt)}" loading="lazy"></button><figcaption class="small">${esc(i.caption || "")}</figcaption></figure>`).join("")}</div></div>`;
    }
    default: return "";
  }
}

// ---------- spotlight ----------
const KIND = { dance: "Dance", music: "Music", theatre: "Theatre", art: "Art", craft: "Craft", textile: "Textile", dish: "Dish", drink: "Drink", festival: "Festival", custom: "Custom", place: "Place", monument: "Monument", person: "Person", landscape: "Landscape", wildlife: "Wildlife", object: "Object", event: "Event" };
function renderMedia(m, poster) {
  if (!m) return "";
  const len = m.end ? m.end - (m.start || 0) : m.duration_s;
  const meta = [len ? `${Math.floor(len / 60)}:${pad2(len % 60)}${m.end ? " clip" : ""}` : "", m.publisher].filter(Boolean).join(" · ");
  if (m.kind === "audio" && m.provider !== "youtube") return `<div class="media audio"><div class="mt">${esc(m.title)}${meta ? ` · ${esc(meta)}` : ""}</div><audio controls preload="none" src="${esc(m.url)}"></audio><div class="credit">${esc([m.publisher, m.license].filter(Boolean).join(", "))}</div></div>`;
  return `<div class="media" data-media="${esc(m.id)}"><button class="poster" style="${poster ? `background-image:url('${esc(imgUrl(poster, 960))}')` : ""}" aria-label="Play ${esc(m.title)}"><span class="pl"><i></i>${esc(m.title)}<span style="font-weight:500;opacity:.85">${esc(meta)}${navigator.onLine ? "" : " · needs internet"}</span></span></button></div>`;
}
function playMedia(el, m) {
  if (m.provider === "youtube" || /youtube/.test(m.embed_url || m.url || "")) {
    let src = m.embed_url || ""; if (!src) { const idm = (m.url || "").match(/(?:v=|youtu\.be\/|embed\/)([\w-]{11})/); src = idm ? `https://www.youtube-nocookie.com/embed/${idm[1]}` : m.url; }
    const u = new URL(src.replace("www.youtube.com", "www.youtube-nocookie.com"));
    u.searchParams.set("autoplay", "1"); u.searchParams.set("playsinline", "1"); u.searchParams.set("rel", "0");
    if (m.start) u.searchParams.set("start", m.start); if (m.end) u.searchParams.set("end", m.end);
    el.innerHTML = `<iframe src="${esc(u)}" title="${esc(m.title)}" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>`;
  } else {
    el.innerHTML = `<video controls playsinline autoplay preload="metadata" src="${esc(m.url)}${m.start ? `#t=${m.start}${m.end ? "," + m.end : ""}` : ""}"></video>`;
  }
}
function renderSpot(sp, d, eager = false) {
  const imgs = (sp.image_ids || []).map(i => d._img[i]).filter(Boolean);
  const media = (sp.media_ids || []).map(i => d._media[i]).filter(Boolean);
  const wide = ["place", "landscape", "monument", "event"].includes(sp.kind);
  const photos = imgs.length ? `<div class="photos ${wide ? "wide" : ""}" data-n="${imgs.length}">${imgs.map((i, k) => `<button data-view="${esc(i.id)}" data-group="${esc(sp.id)}" data-k="${k}" aria-label="Open photo"><img src="${esc(imgUrl(i, 960))}" alt="${esc(i.alt)}" ${eager && k === 0 ? "" : 'loading="lazy"'} decoding="async" width="${i.width || 4}" height="${i.height || 5}"></button>`).join("")}</div>
    <div class="photo-meta">${credit(imgs[0])}${imgs.length > 1 ? `<span class="count">1 / ${imgs.length}</span>` : ""}</div>` : "";
  const where = sp.where?.label ? ` · ${esc(sp.where.label)}` : "";
  const cmpImg = sp.compare?.image_id && d._img[sp.compare.image_id];
  return `<article class="spot" id="sp-${esc(sp.id)}" data-spot="${esc(sp.id)}">${photos}<div class="body">
    <div class="kind">${esc(KIND[sp.kind] || sp.kind || "")}</div>
    <h3>${esc(sp.name)}${sp.native_name ? `<span class="native">${esc(sp.native_name)}</span>` : ""}</h3>
    ${sp.where?.label ? `<div class="where">${esc(sp.where.label)}${sp.when ? ` · ${esc(sp.when)}` : ""}</div>` : ""}
    ${sp.spot_it ? `<div class="spotit">${esc(sp.spot_it)}</div>` : ""}
    ${sp.story_md ? `<div class="prose">${md(sp.story_md)}</div>` : ""}
    ${sp.memory_hook ? `<div class="hook">${esc(sp.memory_hook)}</div>` : ""}
    ${sp.why_it_matters ? `<div class="why"><b>Why it matters.</b> ${esc(sp.why_it_matters)}</div>` : ""}
    ${media.map(m => renderMedia(m, imgs[0])).join("")}
    ${sp.compare ? `<div class="cmpbox"><div class="eyebrow">Don't confuse it with</div>${cmpImg ? `<div class="cmp" style="margin-top:10px"><figure><button data-view="${esc(imgs[0]?.id || "")}"><img src="${esc(imgUrl(imgs[0], 500))}" alt="" loading="lazy"></button><figcaption>${esc(sp.name)}</figcaption></figure><figure><button data-view="${esc(cmpImg.id)}"><img src="${esc(imgUrl(cmpImg, 500))}" alt="${esc(cmpImg.alt)}" loading="lazy"></button><figcaption>${esc(sp.compare.with)}</figcaption></figure></div>` : `<div class="h3" style="margin-top:4px;font-size:18px">${esc(sp.compare.with)}</div>`}<p class="prose" style="font-size:16px;margin-top:8px">${esc(sp.compare.difference || "")}</p></div>` : ""}
  </div></article>`;
}
function bindImages(root, d) {
  root.addEventListener("click", e => {
    const b = e.target.closest("[data-view]");
    if (b) {
      const g = b.dataset.group;
      if (g && d._spots[g]) { const imgs = d._spots[g].image_ids.map(i => d._img[i]).filter(Boolean); openViewer(imgs, +b.dataset.k || 0); }
      else if (d._img[b.dataset.view]) openViewer([d._img[b.dataset.view]]);
      return;
    }
    const j = e.target.closest("[data-jump]");
    if (j) { document.getElementById("sp-" + j.dataset.jump)?.scrollIntoView({ behavior: "smooth" }); return; }
    const m = e.target.closest("[data-media]");
    if (m && !m.querySelector("iframe,video")) playMedia(m, d._media[m.dataset.media]);
  });
  $$(".photos", root).forEach(p => {
    const c = p.parentElement.querySelector(".count"); if (!c) return;
    p.addEventListener("scroll", () => { const k = Math.round(p.scrollLeft / (p.firstElementChild.clientWidth + 6)); c.textContent = `${k + 1} / ${p.dataset.n}`; }, { passive: true });
  });
}


// ---------- Feel: press state, sound, haptics ----------
const PRESSABLE = ".btn,.press,.opt,.qk,.node,.area-chips button,.gcard,.today-card,.lib-item,.step,.photos button,.cmp button,.tabbar a,[data-surprise]";
let actx = null;
function tone(kind) {
  if (S.settings.sound === false) return;
  try {
    actx ||= new (window.AudioContext || window.webkitAudioContext)();
    const t = actx.currentTime, g = actx.createGain(); g.connect(actx.destination);
    const note = (f1, f2, start, dur, vol, type = "sine") => { const o = actx.createOscillator(), gg = actx.createGain(); o.type = type; o.frequency.setValueAtTime(f1, t + start); o.frequency.exponentialRampToValueAtTime(f2, t + start + dur); gg.gain.setValueAtTime(0.0001, t + start); gg.gain.exponentialRampToValueAtTime(vol, t + start + 0.008); gg.gain.exponentialRampToValueAtTime(0.0001, t + start + dur); o.connect(gg); gg.connect(g); o.start(t + start); o.stop(t + start + dur + 0.02); };
    if (kind === "tap") note(320, 140, 0, 0.05, 0.08, "triangle");
    else if (kind === "right") { note(660, 660, 0, 0.12, 0.12); note(990, 990, 0.09, 0.18, 0.12); }
    else if (kind === "wrong") note(150, 90, 0, 0.22, 0.12, "square");
    else if (kind === "stamp") { note(120, 60, 0, 0.18, 0.2, "triangle"); note(880, 1320, 0.12, 0.25, 0.08); }
  } catch (e) {}
}
// iOS 18+ Safari gives a haptic tick when a switch checkbox toggles; Android uses vibrate.
const hapticLabel = (() => { const l = document.createElement("label"); l.id = "haptic"; l.innerHTML = '<input type="checkbox" switch>'; document.body.appendChild(l); return l; })();
function haptic(ms = 8) {
  if (S.settings.haptics === false) return;
  try { if (navigator.vibrate) navigator.vibrate(ms); else hapticLabel.click(); } catch (e) {}
}
function feel(kind) { tone(kind); haptic(kind === "wrong" ? [12, 40, 12] : kind === "right" ? [10, 30, 18] : 8); }
let pressed = null, pressedAt = 0;
document.addEventListener("pointerdown", e => {
  const el = e.target.closest(PRESSABLE); if (!el || el.disabled) return;
  pressed = el; pressedAt = performance.now(); el.classList.add("is-pressed"); feel("tap");
}, { passive: true });
const release = () => { if (!pressed) return; const el = pressed; pressed = null; const wait = Math.max(0, 70 - (performance.now() - pressedAt)); setTimeout(() => el.classList.remove("is-pressed"), wait); };
["pointerup", "pointercancel", "pointerleave", "scroll"].forEach(ev => document.addEventListener(ev, release, { passive: true, capture: true }));
document.addEventListener("touchstart", () => {}, { passive: true }); // lets :active work on iOS

// ---------- quiz engine ----------
// render(item, d, el, done(correct)) handles every quiz type in the schema.
function quizImg(d, id, w = 960) { const i = d._img[id]; return i ? `<div class="qimg"><img src="${esc(imgUrl(i, w))}" alt="${esc(i.alt)}"></div>${credit(i)}` : ""; }
function feedback(el, ok, item, d, extra = "") {
  const fb = document.createElement("div");
  fb.className = "fb " + (ok ? "ok" : "no");
  fb.innerHTML = `<b>${ok ? "Right." : "Not quite."}</b>${extra}${esc(item.explanation || "")}`;
  el.appendChild(fb);
}
function renderQuiz(item, d, el, done) {
  const type = item.type;
  const head = `<div class="q"><div class="prompt">${esc(item.prompt || item.statement || "")}</div>`;
  let answered = false;
  const finish = (ok, extra) => { if (answered) return; answered = true; feel(ok ? "right" : "wrong"); feedback(el.querySelector(".q"), ok, item, d, extra); done(ok); };

  if (["mcq", "odd_one_out", "image_id", "listen_id"].includes(type) || (type === "guess_clues" && item.options && !item.clues)) {
    const media = type === "listen_id" ? renderMedia(d._media[item.media_id]) : (item.image_id ? quizImg(d, item.image_id) : "");
    const order = item.options.map((o, i) => i);
    el.innerHTML = `${head}${media}<div class="opts">${order.map(i => `<button class="opt press" data-i="${i}">${esc(item.options[i])}</button>`).join("")}</div></div>`;
    if (type === "listen_id") bindImages(el, d);
    $$(".opt", el).forEach(b => b.onclick = () => {
      if (answered) return;
      const i = +b.dataset.i, ok = i === item.answer;
      $$(".opt", el).forEach(x => { const k = +x.dataset.i; x.classList.add(k === item.answer ? "right" : k === i ? "wrong" : "dim"); });
      finish(ok);
    });
  } else if (type === "true_false") {
    el.innerHTML = `${head}<div class="grid2 tx"><button class="opt press" data-v="true">True</button><button class="opt press" data-v="false">False</button></div></div>`;
    $$(".opt", el).forEach(b => b.onclick = () => { if (answered) return; const v = b.dataset.v === "true", ok = v === !!item.answer; $$(".opt", el).forEach(x => x.classList.add((x.dataset.v === "true") === !!item.answer ? "right" : x === b ? "wrong" : "dim")); finish(ok); });
  } else if (type === "higher_lower") {
    const [a, b] = item.options || [];
    el.innerHTML = `${head}<div class="grid2 tx"><button class="opt press" data-v="higher">Higher</button><button class="opt press" data-v="lower">Lower</button></div></div>`;
    $$(".opt", el).forEach(x => x.onclick = () => { if (answered) return; const ok = x.dataset.v === item.answer; $$(".opt", el).forEach(y => y.classList.add(y.dataset.v === item.answer ? "right" : y === x ? "wrong" : "dim")); finish(ok, a && b ? `<span style="font-family:var(--ui);font-size:14px;display:block;margin-bottom:6px">${esc(a.label)}: ${esc(a.value)}${esc(a.unit || "")} · ${esc(b.label)}: ${esc(b.value)}${esc(b.unit || "")}</span>` : ""); });
  } else if (type === "order") {
    const answer = item.answer || [];
    let cur = shuffle(item.items ? item.items.map(x => x.label ?? x) : answer);
    // reshuffle until at least half the items are out of place
    for (let t = 0; t < 12 && cur.filter((x, i) => x === answer[i]).length > answer.length / 2 - 1; t++) cur = shuffle(cur);
    const draw = (state) => {
      el.innerHTML = `${head}<div class="small faint" style="margin-top:6px">Earliest at the top. Use the arrows.</div><ol class="order">${cur.map((x, i) => `<li class="press ${state ? (x === answer[i] ? "right" : "wrong") : ""}"><span>${esc(x)}</span>${state ? "" : `<button data-u="${i}" aria-label="Move up">↑</button><button data-d="${i}" aria-label="Move down">↓</button>`}</li>`).join("")}</ol>${state ? "" : '<button class="btn primary block" style="margin-top:14px" data-check>Check order</button>'}</div>`;
      $$("[data-u]", el).forEach(b => b.onclick = () => { const i = +b.dataset.u; if (i > 0) { [cur[i - 1], cur[i]] = [cur[i], cur[i - 1]]; draw(); } });
      $$("[data-d]", el).forEach(b => b.onclick = () => { const i = +b.dataset.d; if (i < cur.length - 1) { [cur[i + 1], cur[i]] = [cur[i], cur[i + 1]]; draw(); } });
      const c = $("[data-check]", el); if (c) c.onclick = () => { draw(true); finish(cur.join("|") === answer.join("|"), `<span style="font-family:var(--ui);font-size:14px;display:block;margin-bottom:6px">${answer.map((x, i) => `${i + 1}. ${esc(x)}`).join("<br>")}</span>`); };
    };
    draw();
  } else if (type === "match") {
    const pairs = item.answer || item.pairs || [];
    const L_ = shuffle(pairs.map(p => p[0])), R_ = shuffle(pairs.map(p => p[1]));
    let pick = null, wrong = 0, got = 0;
    el.innerHTML = `${head}<div class="small faint" style="margin-top:6px">Tap one on the left, then its match.</div><div class="match">${L_.map((l, i) => `<button class="opt press" data-l="${esc(l)}" style="grid-column:1;grid-row:${i + 1}">${esc(l)}</button>`).join("")}${R_.map((r, i) => `<button class="opt press" data-r="${esc(r)}" style="grid-column:2;grid-row:${i + 1}">${esc(r)}</button>`).join("")}</div></div>`;
    $$("[data-l]", el).forEach(b => b.onclick = () => { $$("[data-l]", el).forEach(x => x.classList.remove("sel")); b.classList.add("sel"); pick = b; });
    $$("[data-r]", el).forEach(b => b.onclick = () => {
      if (!pick) return;
      const ok = pairs.some(p => p[0] === pick.dataset.l && p[1] === b.dataset.r);
      if (ok) { pick.classList.add("done", "right"); b.classList.add("done", "right"); pick.classList.remove("sel"); pick = null; if (++got === pairs.length) finish(wrong === 0); }
      else { wrong++; b.classList.add("wrong"); setTimeout(() => b.classList.remove("wrong"), 500); }
    });
  } else if (type === "map_pin") {
    const tg = item.target || { lat: item.answer.lat, lon: item.answer.lon, tolerance_km: 60 };
    const mid = "m" + Math.random().toString(36).slice(2, 7);
    el.innerHTML = `${head}<div class="map tall" id="${mid}" style="margin-top:14px"></div><button class="btn primary block" style="margin-top:12px" data-check disabled>Drop a pin first</button></div>`;
    let pin = null; const m = makeMap($("#" + mid, el), d, { labels: false });
    if (!m) { done(false); return; }
    m.on("click", e => { if (answered) return; pin ? pin.setLatLng(e.latlng) : (pin = L.marker(e.latlng, { icon: dot("#2B3C6B") }).addTo(m)); const c = $("[data-check]", el); c.disabled = false; c.textContent = "Check"; });
    $("[data-check]", el).onclick = () => {
      if (!pin || answered) return;
      const km = Math.round(kmBetween([pin.getLatLng().lat, pin.getLatLng().lng], [tg.lat, tg.lon]));
      L.marker([tg.lat, tg.lon], { icon: dot("#2F7D4F") }).addTo(m).bindTooltip(esc(tg.label || "Here"), { permanent: true, direction: "top", className: "pin-label", offset: [0, -6] });
      L.polyline([pin.getLatLng(), [tg.lat, tg.lon]], { color: "#7A7266", dashArray: "4 4", weight: 2 }).addTo(m);
      $("[data-check]", el).remove();
      finish(km <= (tg.tolerance_km || 60), `<span style="font-family:var(--ui);font-size:14px;display:block;margin-bottom:6px">You were ${km} km away.</span>`);
    };
  } else if (type === "guess_clues") {
    const clues = item.clues || []; let shown = 1;
    const opts = item.options;
    const draw = () => {
      el.innerHTML = `${head}<ol class="clues">${clues.slice(0, shown).map((c, i) => `<li><span class="eyebrow">Clue ${i + 1}</span><br>${esc(c)}</li>`).join("")}</ol>
        ${opts ? `<div class="opts">${opts.map((o, i) => `<button class="opt press" data-i="${i}">${esc(o)}</button>`).join("")}</div>` : `<input class="txt" style="margin-top:14px" placeholder="Type a guess (optional)" autocomplete="off"><div class="row" style="margin-top:10px"><button class="btn block" data-reveal style="flex:1">Show answer</button><button class="btn primary block" data-go style="flex:1">Guess</button></div>`}
        ${shown < clues.length ? `<button class="linkbtn" data-more>Another clue (${clues.length - shown} left)</button>` : ""}</div>`;
      const more = $("[data-more]", el); if (more) more.onclick = () => { shown++; draw(); };
      if (opts) $$(".opt", el).forEach(b => b.onclick = () => { if (answered) return; const i = +b.dataset.i; $$(".opt", el).forEach(x => x.classList.add(+x.dataset.i === item.answer ? "right" : x === b ? "wrong" : "dim")); more && more.remove(); finish(i === item.answer, `<span style="font-family:var(--ui);font-size:14px;display:block;margin-bottom:6px">${shown} of ${clues.length} clues used.</span>`); });
      else { const go = () => { const v = $(".txt", el).value.trim().toLowerCase(); if (!v) return; const ans = [item.answer, ...(item.accept || [])].map(a => String(a).toLowerCase()); const ok = ans.some(a => a.includes(v) || v.includes(a)); more && more.remove(); finish(ok, `<span style="font-family:var(--ui);font-size:14px;display:block;margin-bottom:6px">Answer: ${esc(item.answer)}</span>`); }; $("[data-go]", el).onclick = go; $(".txt", el).onkeydown = e => e.key === "Enter" && go(); $("[data-reveal]", el).onclick = () => { more && more.remove(); finish(false, `<span style="font-family:var(--ui);font-size:14px;display:block;margin-bottom:6px">Answer: ${esc(item.answer)}</span>`); }; }
    };
    draw();
  } else if (type === "compare") {
    const ids = item.image_ids || [];
    el.innerHTML = `${head}<div class="grid2">${ids.map((id, i) => { const im = d._img[id]; return `<button class="opt press" data-i="${i}"><img src="${esc(imgUrl(im, 500))}" alt=""><span class="lab" hidden>${esc(item.options?.[i] || "")}</span></button>`; }).join("")}</div></div>`;
    $$(".opt", el).forEach(b => b.onclick = () => { if (answered) return; const i = +b.dataset.i; $$(".opt", el).forEach(x => { x.classList.add(+x.dataset.i === item.answer ? "right" : x === b ? "wrong" : "dim"); $(".lab", x).hidden = false; }); finish(i === item.answer); });
  } else {
    el.innerHTML = `${head}</div>`; done(true);
  }
}

// ---------- router ----------
const routes = [];
const route = (re, fn) => routes.push([re, fn]);
async function go() {
  const h = location.hash.slice(1) || "/today";
  for (const [re, fn] of routes) { const m = h.match(re); if (m) { await fn(...m.slice(1)); return; } }
  location.hash = "#/today";
}
window.addEventListener("hashchange", go);
const entryById = id => PLAN.find(e => e.id === id);

// ---------- Today ----------
const STEP_DEF = [
  ["warm", "Warm up", "Due cards, then 5 guesses about today"],
  ["read", "Read", "The place, one spotlight at a time"],
  ["learn", "Learn the cards", "Today's core cards, until each one sticks"],
  ["play", "Play", "Map, clues, timeline, pictures"],
  ["make", "Make", "Explain it back, side dish, one offline task"],
  ["close", "Close", "10 questions, no notes. Then the stamp"]
];
function stepStatus(entry, data) {
  const p = P(entry.id), f = floor(entry, data);
  const s = {
    warm: f.dueLeft === 0 && (!data?.prequestions?.length || Object.keys(p.pre).length >= data.prequestions.length),
    read: f.readDone >= .99, learn: f.cardsDone >= 1,
    play: !!p.steps.play, make: !!p.steps.make, close: p.completedOn != null
  };
  return s;
}
function stepHref(k, entry) {
  return { warm: `#/warm/${entry.id}`, read: `#/read/${entry.id}`, learn: `#/learn/${entry.id}`, play: `#/play/${entry.id}`, make: `#/make/${entry.id}`, close: `#/close/${entry.id}` }[k];
}
function ringSvg(f) {
  const segs = [[f.reviewDone, "var(--blue)"], [f.readDone, "var(--accent)"], [f.cardsDone, "var(--gold)"]];
  const R = [42, 31, 20];
  return `<svg class="ring" viewBox="0 0 100 100">${segs.map(([v, c], i) => { const r = R[i], C = 2 * Math.PI * r; return `<circle class="bg" cx="50" cy="50" r="${r}"/>${v > 0.005 ? `<circle cx="50" cy="50" r="${r}" stroke="${c}" stroke-dasharray="${C * clamp(v, 0, 1)} ${C}" transform="rotate(-90 50 50)"/>` : ""}`; }).join("")}</svg>`;
}
function stampHtml(e, cls = "", w = 330) {
  const p = S.progress[e.id], d = cache[e.id];
  const hero = d && d._img[d.hero?.image_id];
  if (p?.completedOn != null) return `<div class="stamp ${cls}"><div class="in"><div class="pic" style="background-image:url('${esc(imgUrl(hero, w))}')"><span class="pm">DONE<br>${esc(dStr(p.completedOn).slice(5).replace("-", "·"))}</span></div><div class="nm">${esc(e.title)}</div></div><span class="post">DONE<br>${esc(dStr(p.completedOn).slice(5).replace("-", "·"))}</span></div>`;
  return `<div class="stamp empty ${cls}"><div class="in"><div class="nm">${esc(e.title)}</div></div></div>`;
}
// Area colours (Duolingo-like palette), [main, shadow]
const AREA_COL = {
  "India": ["#FF9600", "#E08600"], "World": ["#1CB0F6", "#1899D6"], "Sports": ["#58CC02", "#58A700"], "Cities": ["#CE82FF", "#A568CC"],
  "Brands": ["#FF4B4B", "#EA2B2B"], "History": ["#E5A400", "#C48C00"], "How things work": ["#2B70C9", "#1F5BA8"], "Psychology": ["#FF86D0", "#E06AB4"],
  "Art": ["#CE82FF", "#A568CC"], "Nature": ["#58CC02", "#58A700"], "Music": ["#FF86D0", "#E06AB4"], "Film": ["#4B4B4B", "#2E2E2E"],
  "Festivals": ["#FF9600", "#E08600"], "Medicine": ["#00CD9C", "#00A880"], "Money": ["#58CC02", "#58A700"], "Crime": ["#4B4B4B", "#2E2E2E"],
  "Paranormal": ["#8549BA", "#6A3896"], "Food": ["#FF9600", "#E08600"], "Games": ["#1CB0F6", "#1899D6"], "Religion": ["#E5A400", "#C48C00"],
  "Astronomy": ["#2B70C9", "#1F5BA8"], "Type": ["#4B4B4B", "#2E2E2E"], "Climate": ["#00CD9C", "#00A880"], "Myth": ["#8549BA", "#6A3896"],
  "Fashion": ["#FF86D0", "#E06AB4"], "Social": ["#1CB0F6", "#1899D6"], "Internet": ["#CE82FF", "#A568CC"], "Language": ["#FF4B4B", "#EA2B2B"]
};
const col = a => AREA_COL[a] || ["#58CC02", "#58A700"];
const ICON = {
  star: '<svg viewBox="0 0 24 24"><path d="M12 2.5l2.9 6 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.2 1.3-6.6L2.5 9.3l6.6-.8z"/></svg>',
  check: '<svg viewBox="0 0 24 24"><path d="M9.5 16.2 5.3 12l-1.8 1.8 6 6L21 8.3l-1.8-1.8z"/></svg>',
  lock: '<svg viewBox="0 0 24 24"><path d="M7 10V7a5 5 0 0 1 10 0v3h1.5v11h-13V10zm2 0h6V7a3 3 0 0 0-6 0z"/></svg>',
  book: '<svg viewBox="0 0 24 24"><path d="M4 4h7a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4zM20 4h-4a2 2 0 0 0-2 2v12a2 2 0 0 1 2-2h4z"/></svg>',
  flame: '<svg viewBox="0 0 24 24"><path fill="#FF9600" d="M12 2s5 4.6 5 10a5 5 0 0 1-10 0c0-2.2 1.2-3.8 2.4-5 .2 1.6 1 2.8 2.1 3.2C11 7.6 12 2 12 2z"/></svg>',
  gem: '<svg viewBox="0 0 24 24"><path fill="#1CB0F6" d="M6 3h12l4 6-10 12L2 9z"/></svg>',
  stamp: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="#FFC800"/><path fill="#fff" d="M12 6.5l1.6 3.4 3.7.4-2.8 2.5.8 3.7L12 14.6l-3.3 1.9.8-3.7-2.8-2.5 3.7-.4z"/></svg>'
};
const ZIG = [0, -54, -82, -54, 0, 54, 82, 54];

route(/^\/path$/, async () => {
  await loadDeckDays();
  const entry = todayTarget();
  const data = await loadDay(entry);
  const r = rec(); const f = floor(entry, data);
  if (f.met && !r.floor) { r.floor = true; save(); }
  const st = stepStatus(entry, data);
  const nextK = STEP_DEF.find(([k]) => !st[k])?.[0];
  const sk = streak();
  const known = Object.values(S.cards).filter(c => c.step >= 2).length;
  const done = PLAN.filter(e => S.progress[e.id]?.completedOn != null);
  const isStandalone = matchMedia("(display-mode: standalone)").matches || navigator.standalone;
  const [c, cd] = col(entry.area);
  const idx = PLAN.indexOf(entry);
  const win = PLAN.slice(Math.max(0, idx - 2), idx + 9);
  const stepsDone = STEP_DEF.filter(([k]) => st[k]).length;
  const nextEntry = PLAN.slice(idx + 1).find(e => e.file) || PLAN[idx + 1];
  const t = now(), dt = nToDate(t);

  const nodeHtml = (e, k) => {
    const [ec, ecd] = col(e.area);
    const isDone = S.progress[e.id]?.completedOn != null, isCur = e === entry;
    const cls = isDone ? "done" : isCur ? "cur" : e.file ? "ready" : "locked";
    const icon = isDone ? ICON.check : isCur ? ICON.star : e.file ? ICON.book : ICON.lock;
    const pct = isCur ? stepsDone / STEP_DEF.length : 0;
    const ring = isCur ? `<span class="ringc" style="--clip:${pct >= 1 ? "none" : `conic-gradient(#000 0 ${pct * 360}deg, transparent 0)`}"><i style="${pct ? "" : "display:none"};-webkit-mask:conic-gradient(#000 0 ${pct * 360}deg,transparent 0);mask:conic-gradient(#000 0 ${pct * 360}deg,transparent 0)"></i></span>` : "";
    return `<div class="node-wrap" style="--c:${ec};--cd:${ecd};transform:translateX(${ZIG[k % 8]}px)">
      ${isCur ? `<span class="bubble">${stepsDone ? "CONTINUE" : "START"}</span>` : ""}
      <button class="node ${cls}" data-node="${e.id}" aria-label="Day ${e.n}: ${esc(e.title)}">${ring}${icon}</button>
      <div class="node-lab">${e.n} · ${esc(e.title)}</div>
    </div>`;
  };

  setView(`<div class="wrap" style="--area:${c};--area-d:${cd}">
    <div class="statbar"><span class="s" title="Day streak">${ICON.flame}${sk.count}</span><span class="s" title="Cards you know">${ICON.gem}<span style="color:#1CB0F6">${known}</span></span><span class="s" title="Topics stamped">${ICON.stamp}<span style="color:#E5A400">${done.length}</span></span><span class="s" style="color:var(--ink-3);font-size:13px">${WD[dt.getDay()]} ${dt.getDate()} ${MON[dt.getMonth()].slice(0, 3)}</span></div>
    <div class="unit"><div class="t"><div class="eyebrow">Day ${entry.n} · ${esc(entry.area)}</div><h2>${esc(entry.title)}</h2></div><a class="ub" href="#/library" aria-label="All topics">${ICON.book.replace("<svg", '<svg style="width:26px;height:26px;fill:#fff"')}</a></div>
    ${!isStandalone && !S.settings.hideInstall ? `<div class="banner" style="margin-top:14px"><div><b>Add to your Home Screen</b>Safari: Share, then Add to Home Screen. Keeps progress safe, works offline.</div><button class="bx" data-hideinstall aria-label="Dismiss">✕</button></div>` : ""}
    <div class="path">${win.map((e, k) => {
      const html = nodeHtml(e, k);
      if (e !== entry) return html;
      return html + `<div class="pop" style="--c:${c};--cd:${cd}">
        <h3>${data ? (f.met && !nextK ? "Day complete" : (STEP_DEF.find(([k2]) => k2 === nextK) || STEP_DEF[0])[1]) : "Being written"}</h3>
        <p>${data ? (nextK ? (STEP_DEF.find(([k2]) => k2 === nextK) || [0, 0, ""])[2] : `${esc(entry.title)} is in your passport`) : "This topic is still being researched. Review your cards meanwhile."}</p>
        ${data ? `<div class="steps-mini">${STEP_DEF.map(([k2]) => `<i class="${st[k2] ? "on" : ""}"></i>`).join("")}</div>` : ""}
        <a class="btn" href="${data ? (nextK ? stepHref(nextK, entry) : `#/close/${entry.id}`) : "#/review"}">${data ? (nextK ? (stepsDone ? "Continue" : "Start") : "See ticket") : "Review cards"}</a>
      </div>`;
    }).join("")}</div>

    ${data ? `<div class="card pad">
      <div class="ring-row">${ringSvg(f)}<div class="legend">
        <div><span><i style="background:var(--blue)"></i>Review</span><b>${f.reviewGoal ? `${f.reviewGoal - f.dueLeft}/${f.reviewGoal}` : "none due"}</b></div>
        <div><span><i style="background:var(--accent)"></i>Read</span><b>${Math.round(f.readDone * 100)}%</b></div>
        <div><span><i style="background:var(--gold)"></i>New cards</span><b>${f.learnedN}/${f.coreN}</b></div>
      </div></div><div class="small muted" style="margin-top:10px">Daily minimum: fill the three rings. Everything past them is a bonus.</div></div>` : ""}

    ${f.met ? `<div class="card pad" style="margin-top:16px"><div class="eyebrow accent">${P(entry.id).completedOn != null ? "Day done" : "Minimum done"}</div><h3 style="margin-top:6px">Keep going?</h3>
      <div class="stack" style="margin-top:12px">${nextEntry ? `<button class="btn primary block" data-ahead>Next: ${esc(nextEntry.title)}</button>` : ""}<a class="btn block" href="#/review/extra">Practise pictures</a></div></div>` : ""}

    <div class="section-title"><h3>${MON[dt.getMonth()]}</h3><span class="small faint">${sk.count} day streak</span></div>
    <div class="heat">${monthHeat(t, sk)}</div>
    <div class="tiny faint" style="margin-top:8px">Orange: minimum done. Light: short day. Blue: freeze used.</div>
  </div>`, { tab: "today" });

  $$("[data-node]").forEach(b => b.onclick = () => {
    const e = PLAN.find(x => x.id === b.dataset.node);
    if (e === entry) { location.hash = data ? (nextK ? stepHref(nextK, entry) : `#/close/${entry.id}`) : "#/review"; return; }
    location.hash = e.file ? `#/read/${e.id}` : `#/day/${e.id}`;
  });
  const ah = $("[data-ahead]"); if (ah) ah.onclick = () => aheadSheet(nextEntry);
  const hi = $("[data-hideinstall]"); if (hi) hi.onclick = () => { S.settings.hideInstall = true; save(); hi.parentElement.remove(); };
  const cur = $(".node.cur"); if (cur) cur.scrollIntoView({ block: "center" });
  prefetchNext(entry);
});
// ---------- Home: a gallery, with today's card on top ----------
const card = (e, w = 150) => { const [c] = col(e.area); const pr = S.progress[e.id]; const started = pr && Object.keys(pr.read || {}).length; return `<a class="gcard" href="#/read/${e.id}" style="width:${w}px;--c:${c}"><div class="gimg" style="${e.hero ? `background-image:url('${esc(e.hero)}')` : `background:${c}`}">${pr?.completedOn != null ? '<span class="gbadge">✓</span>' : ""}</div><div class="gt"><span class="garea">${esc(e.area)}</span><b>${esc(e.title)}</b>${started && pr.completedOn == null ? `<div class="progress" style="height:6px;margin-top:6px"><i style="width:${Math.min(100, started / 20 * 100)}%"></i></div>` : ""}</div></a>`; };
route(/^\/today$/, async () => {
  await loadDeckDays();
  const entry = todayTarget();
  const data = await loadDay(entry);
  const r = rec(); const f = floor(entry, data);
  if (f.met && !r.floor) { r.floor = true; save(); }
  const st = stepStatus(entry, data);
  const nextK = STEP_DEF.find(([k]) => !st[k])?.[0];
  const sk = streak();
  const known = Object.values(S.cards).filter(c => c.step >= 2).length;
  const due = dueIds().length;
  const ready = PLAN.filter(e => e.file);
  const started = ready.filter(e => e !== entry && S.progress[e.id] && S.progress[e.id].completedOn == null && Object.keys(S.progress[e.id].read || {}).length);
  const areas = [...new Set(ready.map(e => e.area))];
  const [c, cd] = col(entry.area);
  const isStandalone = matchMedia("(display-mode: standalone)").matches || navigator.standalone;
  const dt = nToDate(now());
  const stepsDone = STEP_DEF.filter(([k]) => st[k]).length;
  setView(`<div class="wrap">
    <div class="statbar"><span class="s">${ICON.flame}${sk.count}</span><span class="s">${ICON.gem}<span style="color:#1CB0F6">${known}</span></span><span class="s">${ICON.stamp}<span style="color:#E5A400">${PLAN.filter(e => S.progress[e.id]?.completedOn != null).length}</span></span><button class="s" data-surprise style="color:var(--blue-d);font-size:13px">SURPRISE ME</button></div>
    <div class="eyebrow" style="margin-top:18px">${WD[dt.getDay()]}, ${dt.getDate()} ${MON[dt.getMonth()]} · Today</div>
    <a class="today-card" href="${data ? (nextK ? stepHref(nextK, entry) : `#/close/${entry.id}`) : `#/day/${entry.id}`}" style="--c:${c};--cd:${cd}">
      <div class="tc-img" style="${entry.hero ? `background-image:url('${esc(entry.hero.replace("/500px-", "/960px-"))}')` : ""}"><div class="tc-cap"><span class="garea" style="background:${c}">Day ${entry.n} · ${esc(entry.area)}</span><h2>${esc(entry.title)}</h2></div></div>
      <div class="tc-body">${data ? `<div class="ring-row">${ringSvg(f)}<div class="legend">
        <div><span><i style="background:var(--blue)"></i>Review</span><b>${f.reviewGoal ? `${f.reviewGoal - f.dueLeft}/${f.reviewGoal}` : "none due"}</b></div>
        <div><span><i style="background:var(--accent)"></i>Read</span><b>${Math.round(f.readDone * 100)}%</b></div>
        <div><span><i style="background:var(--gold)"></i>New cards</span><b>${f.learnedN}/${f.coreN}</b></div></div></div>
        <span class="btn primary block" style="margin-top:14px;background:${c};border-color:${c};box-shadow:0 5px 0 ${cd}">${nextK ? `${stepsDone ? "Continue" : "Start"}: ${(STEP_DEF.find(([k]) => k === nextK) || STEP_DEF[0])[1]}` : "Day complete"}</span>` : `<p class="muted">Being researched. Pick anything below meanwhile.</p>`}</div>
    </a>
    ${!isStandalone && !S.settings.hideInstall ? `<div class="banner" style="margin-top:16px"><div><b>Add to your Home Screen</b>Safari: Share, then Add to Home Screen. Keeps progress safe, works offline.</div><button class="bx" data-hideinstall aria-label="Dismiss">✕</button></div>` : ""}
    <div class="quick">
      <a href="#/review" class="qk"><b>${due}</b><span>cards due</span></a>
      <a href="#/path" class="qk"><b>${entry.n}</b><span>on the path</span></a>
      <a href="#/library?Ready" class="qk"><b>${ready.length}</b><span>topics ready</span></a>
    </div>
    ${started.length ? `<div class="section-title"><h3>Continue reading</h3></div><div class="shelf">${started.slice(0, 12).map(e => card(e)).join("")}</div>` : ""}
    <div class="section-title"><h3>Just added</h3><a class="small" href="#/library?Ready" style="color:var(--blue-d);font-weight:800;text-decoration:none">ALL</a></div>
    <div class="shelf">${ready.slice(-14).reverse().map(e => card(e, 200)).join("")}</div>
    ${areas.map(a => { const list = ready.filter(e => e.area === a); return `<div class="section-title"><h3>${esc(a)}</h3><a class="small" href="#/library?${encodeURIComponent(a)}" style="color:var(--blue-d);font-weight:800;text-decoration:none">${list.length}</a></div><div class="shelf">${list.slice(0, 16).map(e => card(e)).join("")}</div>`; }).join("")}
    ${PLAN.length > ready.length ? `<p class="small faint" style="margin:24px 0 0">${PLAN.length - ready.length} more topics are being researched in queue order. New ones appear here as they pass review.</p>` : ""}
  </div>`, { tab: "today" });
  const sp = $("[data-surprise]"); if (sp) sp.onclick = () => { const pool = ready.filter(e => S.progress[e.id]?.completedOn == null); const e = pool[(now() * 7 + pool.length * 13 + Object.keys(S.cards).length) % Math.max(1, pool.length)]; if (e) location.hash = `#/read/${e.id}`; };
  const hi = $("[data-hideinstall]"); if (hi) hi.onclick = () => { S.settings.hideInstall = true; save(); hi.parentElement.remove(); };
  prefetchNext(entry);
});
function monthHeat(t, sk) {
  const dt = nToDate(t);
  const first = dayN(new Date(dt.getFullYear(), dt.getMonth(), 1)), lead = new Date(dt.getFullYear(), dt.getMonth(), 1).getDay();
  const dim = new Date(dt.getFullYear(), dt.getMonth() + 1, 0).getDate();
  let heat = WD.map(w => `<div class="wd">${w[0]}</div>`).join("") + Array(lead).fill('<div class="pad0"></div>').join("");
  for (let i = 0; i < dim; i++) { const n = first + i, k = dStr(n); const s2 = studied(k), fz = sk.frozen.includes(k); heat += `<div class="${s2 ? (S.days[k]?.floor ? "s2" : "s1") : fz ? "fz" : ""} ${n === t ? "today" : ""}">${i + 1}</div>`; }
  return heat;
}

async function aheadSheet(next) {
  const d = await loadDay(next);
  if (!d) { sheet(`<div class="eyebrow">Day ${next.n}</div><h2 style="margin-top:6px">${esc(next.title)}</h2><p class="muted" style="margin-top:10px">${next.kind === "review" ? "Review days open on their own day." : "This day is still being written. It will appear here as soon as it is ready."}</p><button class="btn block" style="margin-top:18px" data-close>OK</button>`); return; }
  const n = coreCards(d).length;
  const fc = forecast(n), t = now();
  const tot = fc.base.map((b, i) => b + fc.add[i]), mx = Math.max(...tot, 10);
  const hot = tot.findIndex(x => x > 150);
  sheet(`<div class="eyebrow">Learn ahead</div><h2 style="margin-top:6px">${esc(next.title)}</h2>
    <p class="muted" style="margin-top:8px">Adds ${n} cards. About +${fc.add[0]} reviews tomorrow and +${fc.add.reduce((a, b) => a + b, 0)} over the next week.</p>
    <div class="fc">${tot.map((x, i) => `<div><span>${x}</span><i class="${x > 150 ? "hi" : fc.add[i] ? "add" : ""}" style="height:${(x / mx) * 60}px"></i>${WD[nToDate(t + i + 1).getDay()].slice(0, 2)}</div>`).join("")}</div>
    ${hot >= 0 ? `<div class="warn">${WD[nToDate(t + hot + 1).getDay()]} goes past 150 reviews. Fine if you have the time.</div>` : ""}
    <div class="stack" style="margin-top:16px">
      <a class="btn primary block" href="#/read/${next.id}" data-close>Read it and add the cards</a>
      <a class="btn block" href="#/read/${next.id}?nocards" data-close>Just read it, add cards on its own day</a>
    </div>
    <p class="tiny faint" style="margin-top:12px">Going ahead never counts as tomorrow's visit. Tomorrow still needs its reviews.</p>`);
}

// ---------- Warm up: due reviews, then prequestions ----------
route(/^\/warm\/([\w-]+)$/, async id => {
  const entry = entryById(id), d = await loadDay(entry); await loadDeckDays();
  if (dueIds().length) { reviewSession({ ids: dueIds(), title: "Warm up", back: "#/today", after: `#/pre/${id}` }); return; }
  location.replace(`#/pre/${id}`);
});
route(/^\/pre\/([\w-]+)$/, async id => {
  const entry = entryById(id), d = await loadDay(entry);
  const items = d?.prequestions || [];
  const p = P(id);
  const left = items.filter(q => p.pre[q.id] == null);
  if (!left.length) { location.replace(`#/read/${id}`); return; }
  runQuizFlow({ title: `Guess first · ${entry.title}`, intro: `<div class="eyebrow accent">Guess first</div><h2 style="margin-top:6px">${["", "One guess", "Two guesses", "Three guesses", "Four guesses", "Five guesses"][left.length] || left.length + " guesses"} about ${esc(entry.title)}</h2><p class="muted" style="margin-top:8px">You are not meant to know these yet. Guessing first makes the answers stick when you meet them in the reading.</p>`,
    items: left, d, back: "#/today", onAnswer: (q, ok) => { p.pre[q.id] = ok; save(); }, after: `#/read/${id}`, finishLabel: "Start reading" });
});

// ---------- Read ----------
route(/^\/read\/([\w-]+)(\?nocards)?$/, async (id, nocards) => {
  const entry = entryById(id), d = await loadDay(entry);
  if (!d) { location.replace(`#/day/${id}`); return; }
  const p = P(id); if (nocards) p.noCardsUntilDay = true;
  const secs = (d.sections || []).slice().sort((a, b) => a.order - b.order);
  const hero = d._img[d.hero?.image_id];
  const allSpots = secs.flatMap(s => s.spotlights || []);
  const wordsLeft = () => { const unread = secs.filter(s => !p.read[s.id]).length; return Math.max(1, Math.round((d.reading_minutes || 50) * unread / (secs.length || 1))); };
  let firstSpot = true;
  setView(`<div class="wrap" style="--area:${col(entry.area)[0]};--area-d:${col(entry.area)[1]}">${topbar(entry.title, "#/today", 0, `<span class="small faint" id="minleft">${wordsLeft()} min left</span>`)}
    <div class="read-hero">${hero ? `<img src="${esc(imgUrl(hero, 1280))}" alt="${esc(hero.alt)}" fetchpriority="high">` : ""}
      <div class="cap"><div class="eyebrow">${esc(d.hero?.kicker || `Day ${entry.n}`)}</div><h1>${esc(d.title)}${d.native_name ? `<span class="native" style="color:rgba(255,255,255,.75)">${esc(d.native_name)}</span>` : ""}</h1>${d.hero?.headline ? `<p>${esc(d.hero.headline.replace(new RegExp("^" + d.title + ":\\s*"), "").replace(/^./, c => c.toUpperCase()))}</p>` : ""}</div></div>
    ${hero ? credit(hero) : ""}
    <p class="small faint" style="margin-top:16px">${secs.length} sections · ${plural(allSpots.length, "spotlight")} · about ${d.reading_minutes || 50} min. Each section ends with a short check. Tap any photo to see it full screen.</p>
    ${secs.map((s, i) => {
      const checks = (s.check || []).map(qid => d._q[qid]).filter(Boolean);
      const vis = [].concat(s.visual || [], s.visuals || []).map(v => renderVisual(v, d)).join("");
      const html = `<section class="sec" id="sec-${esc(s.id)}" data-sec="${esc(s.id)}">
        <div class="eyebrow">${pad2(i + 1)} · ${esc(s.title)}</div><h2>${esc(s.title)}</h2>
        <div class="prose">${md(s.intro_md || s.body_md || "")}</div>${vis}
        ${(s.spotlights || []).map(sp => { const h = renderSpot(sp, d, firstSpot); firstSpot = false; return h; }).join("")}
        ${checks.length ? `<div class="check" data-checks="${esc(s.id)}"><div class="eyebrow">Check · ${checks.length} question${checks.length > 1 ? "s" : ""}</div><div class="qslot"></div></div>` : `<div class="check" data-checks="${esc(s.id)}" data-empty><button class="btn block sm" data-mark>Done with this section</button></div>`}
      </section>`;
      return html;
    }).join("")}
    ${d.verification?.length ? `<section class="sec"><div class="eyebrow">Honesty box</div><h2>Not settled</h2><p class="small muted" style="margin-bottom:10px">Sources disagree on these, or they could not be confirmed as of ${esc(d.as_of)}.</p><ul class="sources">${d.verification.map(v => `<li><b style="color:var(--ink-2)">${esc(v.claim)}</b>${v.note ? ` · ${esc(v.note)}` : ""}</li>`).join("")}</ul></section>` : ""}
    <section class="sec"><div class="eyebrow">Sources</div><ul class="sources">${(d.sources || []).map(s => `<li><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.title || s.url)}</a>${s.publisher ? ` · ${esc(s.publisher)}` : ""}</li>`).join("")}</ul></section>
    <div style="margin-top:28px">${nocards ? `<a class="btn primary block" href="#/today">Done reading</a>` : `<a class="btn primary block" href="#/learn/${id}" id="readnext">Learn today's cards</a>`}</div>
  </div>`, { tabbar: false });
  bindImages(app, d);

  const bar = $(".topbar .progress i"), ml = $("#minleft");
  const upd = () => { const n = secs.filter(s => p.read[s.id]).length; bar.style.width = (n / secs.length * 100) + "%"; ml.textContent = n === secs.length ? "All read" : `${wordsLeft()} min left`; };
  upd();
  // section checks, run one question at a time inline
  $$("[data-checks]").forEach(box => {
    const sid = box.dataset.checks, s = secs.find(x => x.id === sid);
    if (box.hasAttribute("data-empty")) {
      const mark = () => { p.read[sid] = true; save(); upd(); box.innerHTML = '<div class="small faint">Marked as read.</div>'; };
      if (p.read[sid]) mark(); else $("[data-mark]", box).onclick = mark;
      return;
    }
    const qs = s.check.map(qid => d._q[qid]).filter(Boolean);
    let k = 0; const slot = $(".qslot", box);
    if (p.read[sid]) { slot.innerHTML = '<div class="small faint">Done. <button class="linkbtn" data-redo>Try again</button></div>'; $("[data-redo]", slot).onclick = () => { delete p.read[sid]; run(); }; return; }
    const run = () => { if (k >= qs.length) { p.read[sid] = true; save(); upd(); slot.insertAdjacentHTML("beforeend", '<div class="small faint" style="margin-top:10px">Section done.</div>'); return; }
      const div = document.createElement("div"); div.style.marginTop = k ? "20px" : "0"; slot.appendChild(div);
      renderQuiz(qs[k], d, div, () => { k++; const nb = document.createElement("button"); nb.className = "btn sm"; nb.style.marginTop = "12px"; nb.textContent = k < qs.length ? "Next question" : "Continue"; div.appendChild(nb); nb.onclick = () => { nb.remove(); run(); }; });
    };
    // Start the check when the section's end comes into view, so the questions sit right after the reading.
    lazyMount(box, run);
  });
  // spotlights seen
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { p.seen[e.target.dataset.spot] = true; save(); } }), { threshold: .5 });
  $$("[data-spot]").forEach(el => io.observe(el)); cleanup.push(() => io.disconnect());
});

// ---------- Review sessions (shared) ----------
function cardFront(c, d) {
  const img = c.image_id && d._img[c.image_id];
  const img2 = c.image_ids && c.image_ids.map(i => d._img[i]).filter(Boolean);
  let front = esc(c.front);
  if (c.type === "cloze" && c.cloze) front = esc(c.cloze).replace(/\{\{c\d+::(.+?)\}\}/g, '<span class="blank">$1</span>');
  const pics = img2 && img2.length > 1 ? `<div class="cmp" style="padding:10px">${img2.map(i => `<img src="${esc(imgUrl(i, 500))}" alt="">`).join("")}</div>` : img ? `<div class="fimg"><img src="${esc(imgUrl(img, 960))}" alt="${esc(img.alt)}"></div>${credit(img)}` : "";
  return { pics, front };
}
function cardBack(c) {
  if (c.type === "cloze" && c.cloze) return esc(c.cloze).replace(/\{\{c\d+::(.+?)\}\}/g, '<span class="cz">$1</span>');
  return md(c.back);
}
const TYPE_LABEL = { fact: "Fact", cloze: "Fill the blank", image: "Picture", map: "Map", why: "Why", compare: "Compare" };
function reviewSession({ ids, title, back, after, learning = false, dayId = null }) {
  // learning = new cards: Again puts it back 3 places later; Good adds it to the deck.
  let queue = ids.slice(), done = 0, again = 0;
  const total = queue.length;
  const draw = () => {
    if (!queue.length) {
      setView(`<div class="wrap">${topbar(title, back, 1)}<div class="empty-state"><div class="eyebrow accent">Done</div><h2 style="margin-top:8px">${learning ? `${plural(total, "card")} in your deck` : `${plural(done, "card")} reviewed`}</h2><p class="muted" style="margin-top:8px">${again ? `${plural(again, "card")} came back for a second look. ` : ""}${learning ? "They come back tomorrow, then in 3 days, then a week." : "Next due cards appear tomorrow."}</p><a class="btn primary block" style="margin-top:22px" href="${after || back}">${after ? "Continue" : "Back to today"}</a></div></div>`, { tabbar: false });
      return;
    }
    const id = queue[0];
    const cc = learning ? { card: cache[dayId]._cards[id], data: cache[dayId] } : cardContent(id);
    if (!cc) { queue.shift(); draw(); return; }
    const { card: c, data: d } = cc;
    const { pics, front } = cardFront(c, d);
    setView(`<div class="wrap">${topbar(title, back, done / (total + again))}
      <div class="rv"><div class="counter" style="margin-bottom:10px"><span><b>${queue.length}</b> left</span>${learning ? "<span>new</span>" : ""}<span style="margin-left:auto">${esc(d.title)}</span></div>
      <div class="card flash">${pics}<div class="fbody"><div class="tag">${esc(TYPE_LABEL[c.type] || "Card")}</div><div class="front" style="margin-top:8px">${front}</div>
        <div class="back" hidden>${cardBack(c)}${c.map ? '<div class="map" style="height:200px;margin-top:12px" id="cmap"></div>' : ""}<div class="src">${esc(d.title)}${c.section_id ? ` · ${esc((d.sections.find(s => s.id === c.section_id) || {}).title || "")}` : ""}</div></div></div></div></div>
      <div class="dock"><div class="in" id="dock"><button class="btn primary block" data-show>Show answer</button></div></div></div>`, { tabbar: false });
    const reveal = () => {
      $(".back").hidden = false;
      if (c.map) { const m = makeMap($("#cmap"), d, { interactive: false }); if (m) L.marker([c.map.lat, c.map.lon], { icon: dot() }).addTo(m).bindTooltip(esc(c.map.label || ""), { permanent: true, direction: "top", className: "pin-label", offset: [0, -6] }); }
      $("#dock").innerHTML = `<div class="rate" style="flex:1"><button class="press again" data-r="0">Again<small>${learning ? "soon" : "tomorrow"}</small></button><button class="press good" data-r="1">Good<small>${learning ? "1 day" : `${LADDER[Math.min((S.cards[id]?.step ?? -1) + 1, 6)]} days`}</small></button><button class="press" data-r="2">Easy<small>${learning ? "3 days" : `${LADDER[Math.min((S.cards[id]?.step ?? -1) + 2, 6)]} days`}</small></button></div>`;
      $$("[data-r]").forEach(b => b.onclick = () => grade(+b.dataset.r));
    };
    const grade = r => {
      queue.shift();
      if (learning) {
        if (r === 0) { again++; queue.splice(Math.min(3, queue.length), 0, id); }
        else { addCard(c, dayId); if (r === 2) { S.cards[id].step = 1; S.cards[id].due = now() + LADDER[1]; save(); } done++; }
      } else {
        rate(id, r); if (r === 0) { again++; queue.splice(Math.min(4, queue.length), 0, id); } else done++;
      }
      draw();
    };
    $("[data-show]").onclick = reveal;
    const key = e => { if (e.key === " " || e.key === "Enter") { e.preventDefault(); $(".back").hidden ? reveal() : null; } if (!$(".back").hidden && ["1", "2", "3"].includes(e.key)) grade(+e.key - 1); };
    document.addEventListener("keydown", key); cleanup.push(() => document.removeEventListener("keydown", key));
  };
  draw();
}
route(/^\/review$/, async () => {
  await loadDeckDays();
  const ids = dueIds();
  const total = Object.keys(S.cards).length;
  if (!ids.length) {
    const fc = forecast(0);
    setView(`<div class="wrap"><header class="today-head"><div class="eyebrow">Review</div><h1 style="margin-top:6px">${total ? "Nothing due." : "No cards yet."}</h1><p class="muted" style="margin-top:8px">${total ? `${plural(total, "card")} in your deck. Tomorrow: ${fc.base[0]} due.` : "Cards join your deck after you learn them on a day."}</p></header>
      ${total ? `<div class="stack" style="margin-top:18px"><a class="btn block" href="#/review/extra">Practise pictures (doesn't change the schedule)</a></div>` : ""}</div>`, { tab: "review" });
    return;
  }
  reviewSession({ ids, title: "Review", back: "#/today" });
});
route(/^\/review\/extra$/, async () => {
  // free practice on picture cards, no grading into the schedule
  await loadDeckDays();
  const pool = Object.keys(S.cards).map(cardContent).filter(x => x && x.card.image_id);
  const ids = shuffle(pool).slice(0, 20);
  let k = 0;
  const draw = () => {
    if (k >= ids.length) { location.hash = "#/today"; return; }
    const { card: c, data: d } = ids[k]; const { pics, front } = cardFront(c, d);
    setView(`<div class="wrap">${topbar("Practise pictures", "#/today", k / ids.length, `<span class="small faint">${k + 1} of ${ids.length}</span>`)}<div class="rv"><div class="card flash">${pics}<div class="fbody"><div class="front">${front}</div><div class="back" hidden>${cardBack(c)}</div></div></div></div>
      <div class="dock"><div class="in"><button class="btn primary block" data-n>Show answer</button></div></div></div>`, { tabbar: false });
    $("[data-n]").onclick = e => { if ($(".back").hidden) { $(".back").hidden = false; e.target.textContent = "Next"; } else { k++; draw(); } };
  };
  if (!ids.length) { setView(`<div class="wrap">${topbar("Practise", "#/today")}<div class="empty-state"><h2>No picture cards yet.</h2></div></div>`, { tabbar: false }); return; }
  draw();
});
route(/^\/learn\/([\w-]+)$/, async id => {
  const entry = entryById(id), d = await loadDay(entry);
  if (!d) { location.replace("#/today"); return; }
  const core = coreCards(d).map(c => c.id).filter(cid => !S.cards[cid]);
  const p = P(id);
  if (!core.length) {
    const bonus = (d.cards || []).filter(c => !c.core && !S.cards[c.id]);
    setView(`<div class="wrap">${topbar("Cards", "#/today", 1)}<div class="empty-state"><div class="eyebrow accent">Core cards learned</div><h2 style="margin-top:8px">All ${coreCards(d).length} are in your deck.</h2>
      ${bonus.length ? `<p class="muted" style="margin-top:8px">${bonus.length} bonus cards are left for ${esc(entry.title)}. Add them if you have the appetite.</p><button class="btn block" style="margin-top:18px" data-bonus>Learn ${bonus.length} bonus cards</button>` : ""}
      <a class="btn primary block" style="margin-top:12px" href="#/play/${id}">Play</a></div></div>`, { tabbar: false });
    const b = $("[data-bonus]"); if (b) b.onclick = () => reviewSession({ ids: bonus.map(c => c.id), title: "Bonus cards", back: "#/today", after: `#/play/${id}`, learning: true, dayId: id });
    return;
  }
  reviewSession({ ids: core, title: `New cards · ${entry.title}`, back: "#/today", after: `#/play/${id}`, learning: true, dayId: id });
});

// ---------- generic quiz flow (pre, play, close) ----------
function runQuizFlow({ title, intro, items, d, back, onAnswer, after, finishLabel = "Continue", onFinish }) {
  let k = 0, right = 0;
  const draw = () => {
    if (k >= items.length) { onFinish ? onFinish(right, items.length) : (location.hash = after); return; }
    setView(`<div class="wrap">${topbar(title, back, k / items.length)}<div style="padding-top:18px">${k === 0 && intro ? `<div style="margin-bottom:24px">${intro}</div>` : ""}<div id="qslot"></div></div>
      <div class="dock" id="dock" hidden><div class="in"><button class="btn primary block" data-next>${k === items.length - 1 ? finishLabel : "Next"}</button></div></div></div>`, { tabbar: false });
    renderQuiz(items[k], d, $("#qslot"), ok => { if (ok) right++; onAnswer && onAnswer(items[k], ok); $("#dock").hidden = false; $("#qslot").style.paddingBottom = "110px"; const fb = $("#qslot .fb"); fb && setTimeout(() => fb.scrollIntoView({ behavior: "smooth", block: "nearest" }), 60); });
    $("[data-next]").onclick = () => { k++; draw(); };
  };
  draw();
}

// ---------- Play ----------
const PLAY_TYPES = ["map_pin", "guess_clues", "image_id", "compare", "order", "match", "odd_one_out", "higher_lower", "listen_id"];
route(/^\/play\/([\w-]+)$/, async id => {
  const entry = entryById(id), d = await loadDay(entry); if (!d) { location.replace("#/today"); return; }
  const used = new Set((d.sections || []).flatMap(s => s.check || []));
  let items = (d.quiz || []).filter(q => PLAY_TYPES.includes(q.type) && !used.has(q.id));
  if (items.length < 6) items = items.concat((d.quiz || []).filter(q => PLAY_TYPES.includes(q.type) && used.has(q.id)));
  // one map first, then the rest mixed; cap at 8
  const maps = items.filter(q => q.type === "map_pin"), rest = shuffle(items.filter(q => q.type !== "map_pin"));
  items = [...maps.slice(0, 2), ...rest].slice(0, 8);
  // cross-state game from earlier days
  const earlier = PLAN.filter(e => S.progress[e.id]?.completedOn != null && e.id !== id && cache[e.id]);
  runQuizFlow({ title: `Play · ${entry.title}`, intro: `<div class="eyebrow accent">Play</div><h2 style="margin-top:6px">${items.length} games</h2><p class="muted" style="margin-top:8px">Every one makes you produce the answer: drop the pin, pick the picture, put it in order.${earlier.length ? "" : " Cross-state games start once you have two stamps."}</p>`,
    items, d, back: "#/today", onAnswer: () => { rec().games++; save(); },
    onFinish: (r, n) => { P(id).steps.play = true; save(); resultScreen("Play", r, n, `#/make/${id}`, "Make"); } });
});
function resultScreen(name, r, n, next, label) {
  setView(`<div class="wrap">${topbar(name, "#/today", 1)}<div class="empty-state"><div class="eyebrow accent">${esc(name)} done</div><div class="h1" style="font-size:56px;margin-top:10px">${r}/${n}</div><p class="muted" style="margin-top:6px">${r === n ? "Clean sweep." : r >= n * .7 ? "Solid." : "The misses are the useful part. Each explanation tells you what to reread."}</p><a class="btn primary block" style="margin-top:22px" href="${next}">${esc(label)}</a><a class="btn ghost block" style="margin-top:8px" href="#/today">Back to today</a></div></div>`, { tabbar: false });
}

// ---------- Make ----------
route(/^\/make\/([\w-]+)$/, async id => {
  const entry = entryById(id), d = await loadDay(entry); if (!d) { location.replace("#/today"); return; }
  const p = P(id);
  const whys = (d.cards || []).filter(c => c.type === "why").slice(0, 3);
  const sd = d.side_dish, ot = d.offline_task;
  const sdImg = sd?.image_ids?.map(i => d._img[i]).filter(Boolean)[0];
  setView(`<div class="wrap">${topbar(`Make · ${entry.title}`, "#/today")}
    <section class="sec" style="padding-top:22px"><div class="eyebrow accent">1 · Explain it back · optional</div><h2>${esc(entry.title)} in five lines</h2>
      <p class="muted small" style="margin:6px 0 12px">Type it, or just say it out loud. No scrolling back. Putting it in your own words is what makes it stick.</p>
      <textarea class="txt" id="explain" placeholder="Start with where it is and the one thing you would tell anyone...">${esc(p.explain || "")}</textarea></section>
    <section class="sec"><div class="eyebrow accent">2 · Why?</div><h2>Three why questions</h2><p class="muted small" style="margin-top:6px">Think of your answer, type it if you like, then compare.</p>
      ${whys.map(c => `<div class="card pad" style="margin-top:12px" data-why="${esc(c.id)}"><div class="h3" style="font-size:19px">${esc(c.front)}</div><textarea class="txt" style="min-height:70px;margin-top:10px" placeholder="Your answer (optional)">${esc(p.whys[c.id] || "")}</textarea><button class="linkbtn" data-rv>Compare with the answer</button><div class="prose" style="font-size:16px" hidden>${md(c.back)}</div></div>`).join("")}</section>
    ${sd ? `<section class="sec"><div class="eyebrow accent">3 · Side dish · ${esc(sd.area || "")}</div><h2>${esc(sd.title)}</h2>${sdImg ? `<div style="margin:12px 0"><button data-view="${esc(sdImg.id)}" style="width:100%"><img src="${esc(imgUrl(sdImg, 960))}" alt="${esc(sdImg.alt)}" loading="lazy" style="border-radius:12px;width:100%;max-height:300px;object-fit:cover"></button>${credit(sdImg)}</div>` : ""}<div class="prose">${md(sd.body_md)}</div>
      ${sd.card_ids?.length ? `<button class="btn block" style="margin-top:14px" data-sdcards>Add ${sd.card_ids.length} side dish cards</button>` : ""}</section>` : ""}
    ${ot ? `<section class="sec"><div class="eyebrow accent">4 · Off the screen</div><h2>${esc(ot.title)}</h2><div class="prose">${md(ot.body_md)}</div><label class="row" style="margin-top:14px;font-weight:600"><input type="checkbox" id="offl" ${p.offline ? "checked" : ""} style="width:22px;height:22px;accent-color:var(--accent)"> Done it</label></section>` : ""}
    <div style="margin-top:28px"><button class="btn primary block" data-fin>Finish and close the day</button></div>
  </div>`, { tabbar: false });
  bindImages(app, d);
  $("#explain").oninput = e => { p.explain = e.target.value; save(); };
  $$("[data-why]").forEach(b => { $("textarea", b).oninput = e => { p.whys[b.dataset.why] = e.target.value; save(); }; $("[data-rv]", b).onclick = e => { e.target.nextElementSibling.hidden = false; e.target.remove(); }; });
  const sdb = $("[data-sdcards]"); if (sdb) { const left = sd.card_ids.filter(c => !S.cards[c]); if (!left.length) { sdb.textContent = "Side dish cards are in your deck"; sdb.disabled = true; } sdb.onclick = () => reviewSession({ ids: left, title: "Side dish cards", back: `#/make/${id}`, after: `#/make/${id}`, learning: true, dayId: id }); }
  const o = $("#offl"); if (o) o.onchange = () => { p.offline = o.checked; save(); };
  $("[data-fin]").onclick = () => { p.steps.make = true; save(); location.hash = `#/close/${id}`; };
});

// ---------- Close: the test and the stamp ----------
route(/^\/close\/([\w-]+)$/, async id => {
  const entry = entryById(id), d = await loadDay(entry); if (!d) { location.replace("#/today"); return; }
  const p = P(id);
  if (p.completedOn != null) { ticket(entry, d); return; }
  const items = shuffle((d.quiz || []).filter(q => q.type !== "map_pin" || Math.random() < .5)).slice(0, 10);
  runQuizFlow({ title: `Close · ${entry.title}`, intro: `<div class="eyebrow accent">Close</div><h2 style="margin-top:6px">${items.length} questions, no notes</h2><p class="muted" style="margin-top:8px">The score tells you how much stuck today. Your cards will bring the weak spots back.</p>`,
    items, d, back: "#/today", onAnswer: () => { rec().games++; save(); },
    onFinish: (r, n) => { setTimeout(() => feel("stamp"), 350); p.score = [r, n]; p.completedOn = now(); p.steps.close = true; const f = floor(entry, d); if (f.met) rec().floor = true; save(); ticket(entry, d, true); } });
});
function ticket(entry, d, fresh = false) {
  const p = P(entry.id);
  const learned = (d.cards || []).filter(c => S.cards[c.id]).length;
  const next = PLAN[PLAN.indexOf(entry) + 1];
  const sk = streak();
  setView(`<div class="wrap">${topbar("Day complete", "#/today", 1)}
    <div style="display:flex;justify-content:center;margin-top:26px"><div class="ticket-stamp">${stampHtml(entry, fresh ? "land" : "", 500)}</div></div>
    <div class="ticket"><div class="eyebrow">Day ${entry.n} · ${esc(entry.region)}</div><div class="big" style="margin-top:6px">${esc(entry.title)}</div>
      <div class="perf"></div>
      <div class="kv"><div><b>${p.score ? `${p.score[0]}/${p.score[1]}` : "-"}</b><span>test</span></div><div><b>${learned}</b><span>cards kept</span></div><div><b>${sk.count}</b><span>day streak</span></div></div>
    </div>
    ${next ? `<p class="muted" style="margin-top:20px;text-align:center">Tomorrow: <b style="color:var(--ink)">${esc(next.title)}</b></p>` : ""}
    <a class="btn primary block" style="margin-top:20px" href="#/today">Back to today</a>
    <a class="btn ghost block" style="margin-top:8px" href="#/read/${entry.id}">Read ${esc(entry.title)} again</a>
  </div>`, { tabbar: false });
}

// ---------- Day page for days without content ----------
route(/^\/day\/([\w-]+)$/, async id => {
  const entry = entryById(id), d = await loadDay(entry);
  if (d) { location.replace(`#/read/${id}`); return; }
  setView(`<div class="wrap">${topbar(entry?.title || "Day", "#/library")}<div class="empty-state"><div class="eyebrow">Day ${entry?.n} · ${esc(entry?.region || "")}</div><h2 style="margin-top:8px">${esc(entry?.title || "")}</h2><p class="muted" style="margin-top:10px">${entry?.kind === "review" ? "Review day: mixed cards across the region, Connections-style grouping, guess the state from clues, and a blank map of everything so far." : "Being researched now. Topics are written in queue order and appear in the Library as soon as they pass review."}</p><a class="btn block" style="margin-top:22px" href="#/review">Review your deck</a></div></div>`, { tabbar: false });
});

// ---------- Passport ----------
route(/^\/passport$/, async () => {
  const doneE = PLAN.filter(e => S.progress[e.id]?.completedOn != null);
  await Promise.all(doneE.map(loadDay));
  const areas = [...new Set(PLAN.map(e => e.area))];
  setView(`<div class="wrap"><header class="today-head"><div class="eyebrow">Passport</div><h1 style="margin-top:6px">${doneE.length} of ${PLAN.length} stamped</h1><div class="progress" style="margin-top:14px"><i style="width:${Math.max(1, doneE.length / PLAN.length * 100)}%"></i></div></header>
    ${doneE.length ? `<div class="section-title"><h3>Your stamps</h3></div><div class="stamps">${doneE.map(e => `<a href="#/close/${e.id}" style="text-decoration:none;color:inherit">${stampHtml(e)}</a>`).join("")}</div>` : `<p class="muted" style="margin-top:16px">Finish a day to earn its stamp.</p>`}
    <div class="section-title"><h3>By area</h3></div>
    ${areas.map(a => { const all = PLAN.filter(e => e.area === a), d = all.filter(e => S.progress[e.id]?.completedOn != null).length, [c] = col(a); return `<a class="lib-item" href="#/library?${encodeURIComponent(a)}"><div class="th" style="background:${c};color:#fff">${esc(a[0])}</div><div class="t"><b>${esc(a)}</b><span>${d} of ${all.length} · ${all.filter(e => e.file).length} ready</span><div class="progress" style="height:8px;margin-top:6px"><i style="width:${d / all.length * 100}%;background:${c}"></i></div></div></a>`; }).join("")}
  </div>`, { tab: "passport" });
});

// ---------- Library ----------
route(/^\/library(?:\?(.*))?$/, async (q) => {
  const areas = [...new Set(PLAN.map(e => e.area))];
  const sel = q ? decodeURIComponent(q) : "Ready";
  const list = sel === "Ready" ? PLAN.filter(e => e.file) : sel === "All" ? PLAN : PLAN.filter(e => e.area === sel);
  setView(`<div class="wrap"><header class="today-head"><div class="eyebrow">Library</div><h1 style="margin-top:6px">${PLAN.filter(e => e.file).length} topics ready</h1><p class="muted" style="margin-top:6px">${PLAN.length} in the queue, written in order. New ones appear here as they are finished.</p></header>
    <div class="area-chips">${["Ready", "All", ...areas].map(a => `<button class="${a === sel ? "on" : ""}" data-area="${esc(a)}">${esc(a)}</button>`).join("")}</div>
    <div>${list.slice(0, 400).map(e => { const pr = S.progress[e.id], [c] = col(e.area); return `<a class="lib-item" href="${e.file ? `#/read/${e.id}` : `#/day/${e.id}`}"><div class="th" style="${e.hero ? `background-image:url('${esc(e.hero)}')` : `background:${c};color:#fff`}">${e.hero ? "" : e.n}</div><div class="t"><b>${esc(e.title)}</b><span>Day ${e.n} · ${esc(e.area)}${e.minutes ? ` · ${e.minutes} min` : ""}</span></div>${pr?.completedOn != null ? '<span class="pill ok">Stamped</span>' : e.file ? '<span class="pill">Ready</span>' : '<span class="pill">Soon</span>'}</a>`; }).join("")}
    ${list.length > 400 ? `<p class="small faint" style="margin-top:12px">Showing 400 of ${list.length}. Pick an area to narrow it.</p>` : ""}</div>
  </div>`, { tab: "library" });
  $$("[data-area]").forEach(b => b.onclick = () => { location.hash = `#/library?${encodeURIComponent(b.dataset.area)}`; });
});

// ---------- Settings ----------
route(/^\/settings$/, async () => {
  let est = ""; try { const e = await navigator.storage?.estimate?.(); if (e) est = `${(e.usage / 1048576).toFixed(1)} MB used`; } catch (e) {}
  const persisted = await navigator.storage?.persisted?.().catch(() => false);
  setView(`<div class="wrap"><header class="today-head"><div class="eyebrow">Settings</div><h1 style="margin-top:6px">Your setup</h1></header>
    <div class="set-row"><div class="t"><b>When and where you study</b><span>One line, shown on Today. Planning it like this roughly doubles follow-through.</span></div></div>
    <input class="txt" id="cue" placeholder="After dinner, on the sofa" value="${esc(S.settings.cue)}">
    <div class="set-row"><div class="t"><b>Daily minimum of new cards</b><span>The floor. You can always go past it.</span></div><select id="minnew" class="txt" style="width:90px;min-height:42px">${[10, 15, 20, 25, 30].map(n => `<option ${n === S.settings.minNew ? "selected" : ""}>${n}</option>`).join("")}</select></div>
    <div class="set-row"><div class="t"><b>Theme</b><span>Follows your phone by default</span></div><select id="theme" class="txt" style="width:110px;min-height:42px">${["auto", "light", "dark"].map(n => `<option ${n === S.settings.theme ? "selected" : ""}>${n}</option>`).join("")}</select></div>
    <div class="set-row"><div class="t"><b>Sounds</b><span>Soft taps, a chime when right, a thud when wrong</span></div><select id="snd" class="txt" style="width:90px;min-height:42px"><option value="1" ${S.settings.sound !== false ? "selected" : ""}>On</option><option value="0" ${S.settings.sound === false ? "selected" : ""}>Off</option></select></div>
    <div class="set-row"><div class="t"><b>Vibration</b><span>A small tick on every press (Android, iPhone with iOS 18 or later)</span></div><select id="hap" class="txt" style="width:90px;min-height:42px"><option value="1" ${S.settings.haptics !== false ? "selected" : ""}>On</option><option value="0" ${S.settings.haptics === false ? "selected" : ""}>Off</option></select></div>
    <div class="set-row"><div class="t"><b>Back up progress</b><span>Saves a file you can restore from. Do it weekly.</span></div><button class="btn sm" id="exp">Export</button></div>
    <div class="set-row"><div class="t"><b>Restore</b><span>From an exported file</span></div><label class="btn sm">Import<input type="file" accept="application/json" id="imp" hidden></label></div>
    <div class="set-row"><div class="t"><b>Storage</b><span>${esc(est || "unknown")} · ${persisted ? "protected" : "not yet protected"}</span></div>${persisted ? "" : '<button class="btn sm" id="persist">Protect</button>'}</div>
    <div class="set-row"><div class="t"><b>Deck</b><span>${plural(Object.keys(S.cards).length, "card")} · ${S.log.length} reviews logged</span></div></div>
    <div class="set-row"><div class="t"><b>Start over</b><span>Deletes all progress on this phone</span></div><button class="btn sm" id="reset" style="color:var(--bad)">Reset</button></div>
    <p class="tiny faint" style="margin-top:20px">Photos: Wikimedia Commons and other open licences, credited on each image. Maps: OpenStreetMap, Esri. State boundaries: DataMeet via geoBoundaries (CC BY 2.5 IN).</p>
  </div>`, { tab: "settings" });
  $("#cue").oninput = e => { S.settings.cue = e.target.value; save(); };
  $("#minnew").onchange = e => { S.settings.minNew = +e.target.value; save(); };
  $("#theme").onchange = e => { S.settings.theme = e.target.value; applyTheme(); save(); };
  $("#snd").onchange = e => { S.settings.sound = e.target.value === "1"; save(); };
  $("#hap").onchange = e => { S.settings.haptics = e.target.value === "1"; save(); };
  $("#exp").onclick = () => { const b = new Blob([JSON.stringify(S)], { type: "application/json" }); const a = document.createElement("a"); a.href = URL.createObjectURL(b); a.download = `daily-atlas-backup-${dStr(now())}.json`; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000); };
  $("#imp").onchange = async e => { const f = e.target.files[0]; if (!f) return; try { const j = JSON.parse(await f.text()); if (!j.cards || !j.progress) throw 0; S = Object.assign(fresh(), j); save(); toast("Restored"); go(); } catch (er) { toast("That file is not a Daily Atlas backup"); } };
  const ps = $("#persist"); if (ps) ps.onclick = async () => { const ok = await navigator.storage?.persist?.(); toast(ok ? "Storage protected" : "Your browser said no. Add to Home Screen first."); go(); };
  $("#reset").onclick = () => sheet(`<h2>Start over?</h2><p class="muted" style="margin-top:8px">This deletes every card, stamp and streak on this phone. Export a backup first if you might want it.</p><div class="stack" style="margin-top:18px"><button class="btn block" data-close>Keep my progress</button><button class="btn block" style="color:var(--bad)" id="really">Delete everything</button></div>`, (el, close) => { $("#really", el).onclick = () => { S = fresh(); save(); close(); location.hash = "#/today"; }; });
});

function applyTheme() { const t = S.settings.theme; if (t === "auto") document.documentElement.removeAttribute("data-theme"); else document.documentElement.dataset.theme = t; }

// prefetch tomorrow's photos while today is open (iOS has no background sync)
async function prefetchNext(entry) {
  if (!navigator.onLine || navigator.connection?.saveData) return;
  const next = PLAN[PLAN.indexOf(entry) + 1]; const d = await loadDay(next); if (!d) return;
  const urls = (d.images || []).map(i => imgUrl(i, 960));
  if ("caches" in window) { try { const c = await caches.open("atlas-img-v1"); for (const u of urls) { if (!(await c.match(u))) await c.add(new Request(u, { mode: "cors" })).catch(() => {}); } } catch (e) {} }
}

// ---------- boot ----------
async function loadPlan() {
  const [topics, index] = await Promise.all([
    fetch("data/topics.json").then(r => r.json()),
    fetch("data/index.json", { cache: "no-cache" }).then(r => r.ok ? r.json() : { days: [] }).catch(() => ({ days: [] }))
  ]);
  const ready = Object.fromEntries((index.days || []).map(x => [x.n, x]));
  window.PLAN = topics.map(([n, area, title]) => ({ n, id: "t" + String(n).padStart(4, "0"), area, region: area, title, kind: "topic", file: ready[n]?.file, hero: ready[n]?.hero, minutes: ready[n]?.minutes }));
}
(async () => {
  await loadPlan();
  await Store.open();
  const saved = await Store.get();
  if (saved) S = Object.assign(fresh(), saved, { settings: Object.assign(fresh().settings, saved.settings || {}) });
  applyTheme();
  rec(); save();
  try { navigator.storage?.persist?.(); } catch (e) {}
  if ("serviceWorker" in navigator && location.protocol !== "file:") navigator.serviceWorker.register("sw.js").catch(() => {});
  go();
})();

// debugging hook for tests only
window.__atlas = { get S() { return S; }, set S(v) { S = v; save(); }, forecast, dueIds, go };
})();
