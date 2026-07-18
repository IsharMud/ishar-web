/**
 * Ishar HUD map (isharmud/ishar-web#125).
 *
 * A fog-of-war world map fed by two sources:
 *   - the zone's full exit graph from /connect/map/graph/<vnum>/ (the game's
 *     authoritative rooms/room_exits tables, hidden exits excluded), and
 *   - live Room.Info GMCP for "where am I" + discovery accrual.
 *
 * The world has NO coordinates — it is a directed graph with non-Euclidean
 * geometry (the classic first-zone n→e→s→w loop lands in a *different*
 * room) and free-string named exits ("into", "starboard"). layoutZone()
 * computes a deterministic 3-D grid layout per zone from the complete
 * graph: BFS from the smallest vnum, Mudlet-style edge-stretch when the
 * ideal cell is taken, a fixed outward spiral as the last resort, and
 * dogleg polylines for geometrically contradictory edges. Same graph in,
 * same layout out — no discovery-time redraw churn.
 *
 * Fog: only rooms the account has visited (server-persisted, mirrored in
 * localStorage) render fully; rooms one exit ahead render as dashed stubs;
 * everything else is invisible. Visibility gate: a redacted Room.Info
 * (no `num` — the player can't see) never touches the map: no discovery,
 * no ring, "location unknown" state, autowalk aborts.
 *
 * This file is a sibling IIFE to hud.js, attached through the single
 * IsharHUD.registerMap() seam; hud.js hands it a small context (el/fill/
 * send/openMenu/…) and calls mod.onRoom()/renderMini()/renderOverlay().
 * Missing or stale-cached hud-map.js degrades to the rose-only HUD.
 */
(function () {
    "use strict";

    var H = null;      // context handed over by IsharHUD.registerMap()
    var cfg = { urls: null, csrf: "", authed: false, demo: false };

    // ------------------------------------------------------------------
    // State
    // ------------------------------------------------------------------
    var zones = {};      // zoneId -> {graph, layout, name}
    var vnumZone = {};   // room vnum -> zoneId (from loaded graphs)
    var fog = {};        // zoneId -> {set: {vnum: true}}
    var notes = {};      // zoneId -> {vnum: text}
    var frontierCache = {}; // zoneId -> {stamp, set}
    var fogStamp = 0;    // bumped on any fog/graph change (invalidates caches)
    var cur = { zone: null, vnum: null, z: 0, unseen: false };
    var pendingGraph = {};  // vnum -> true while a graph fetch is in flight
    var lastGraphFail = 0;  // backoff clock for failed graph fetches
    var stateLoaded = {};   // zoneId -> true once /map/state merged
    var dirty = [];         // discovered vnums not yet flushed to the server
    var flushTimer = null;
    var pendingFocus = null; // vnum to refocus the big map on once its zone loads

    // ------------------------------------------------------------------
    // Geometry
    // ------------------------------------------------------------------
    // Unit deltas per compass key. Screen y grows southward; z up/down.
    var DELTA = {
        n: [0, -1, 0], s: [0, 1, 0], e: [1, 0, 0], w: [-1, 0, 0],
        ne: [1, -1, 0], nw: [-1, -1, 0], se: [1, 1, 0], sw: [-1, 1, 0],
        u: [0, 0, 1], d: [0, 0, -1]
    };
    // Fixed expansion order — part of the determinism contract.
    var DIR_ORDER = ["n", "e", "s", "w", "ne", "se", "sw", "nw", "u", "d"];
    var DIR_RANK = {};
    DIR_ORDER.forEach(function (d, i) { DIR_RANK[d] = i; });
    var MAX_STRETCH = 4;   // how far an edge stretches before spiraling
    var SPIRAL_MAX = 6;    // max ring radius for the fallback search

    // ------------------------------------------------------------------
    // Terrain palette — colors live in CSS (--hud-ter-*, tokens.md); read
    // once because canvas needs literals. Fallbacks match hud.css.
    // ------------------------------------------------------------------
    var TERRAIN_VAR = {
        "Indoor": "indoor", "City": "city", "Field": "field",
        "Forest": "forest", "Hill": "hill", "Mountain": "mountain",
        "Shallow Water": "water", "Deep Water": "deep",
        "Underwater": "under", "Desert": "desert", "Beach": "beach",
        "Forest Path": "field", "Mountain Path": "hill", "Swamp": "swamp"
    };
    var palette = null;
    function readPalette() {
        var cs = getComputedStyle(document.documentElement);
        function v(name, fallback) {
            var val = String(cs.getPropertyValue(name) || "").trim();
            return val || fallback;
        }
        palette = {
            accent: v("--ac-accent", "#fa7"),
            border: v("--ac-border-2", "#3a3a44"),
            dim: v("--ac-dim", "#8a8a92"),
            info: v("--ac-info", "#4a86cf"),
            warn: v("--ac-warn", "#f80"),
            danger: v("--ac-danger", "#d64b4b"),
            panel: v("--ac-panel", "#131316"),
            ter: {}
        };
        ["indoor", "city", "field", "forest", "hill", "mountain", "water",
         "deep", "under", "desert", "beach", "swamp"].forEach(function (k) {
            palette.ter[k] = v("--hud-ter-" + k, "#26262c");
        });
    }
    function terrainColor(name) {
        if (!palette) readPalette();
        return palette.ter[TERRAIN_VAR[name] || "indoor"] || palette.ter.indoor;
    }

    // ------------------------------------------------------------------
    // Layout engine — deterministic grid placement from the full graph.
    // ------------------------------------------------------------------
    // Tiny binary min-heap ordered by (depth, vnum): rooms at the same BFS
    // depth are expanded in vnum order no matter which parent found them,
    // so the layout never depends on object-key iteration order.
    function heapPush(h, item) {
        h.push(item);
        var i = h.length - 1;
        while (i > 0) {
            var p = (i - 1) >> 1;
            if (heapLess(h[i], h[p])) {
                var t = h[i]; h[i] = h[p]; h[p] = t; i = p;
            } else break;
        }
    }
    function heapPop(h) {
        var top = h[0], last = h.pop();
        if (h.length) {
            h[0] = last;
            var i = 0;
            for (;;) {
                var l = 2 * i + 1, r = l + 1, m = i;
                if (l < h.length && heapLess(h[l], h[m])) m = l;
                if (r < h.length && heapLess(h[r], h[m])) m = r;
                if (m === i) break;
                var t = h[i]; h[i] = h[m]; h[m] = t; i = m;
            }
        }
        return top;
    }
    function heapLess(a, b) {
        return a.depth !== b.depth ? a.depth < b.depth : a.vnum < b.vnum;
    }

    function key3(x, y, z) { return x + "," + y + "," + z; }

    // Deterministic outward spiral around (bx,by): rings of growing radius,
    // each ring scanned in a fixed order (top row L→R, then sides, then
    // bottom row) — the last-resort placement when stretching fails.
    function spiralFind(cells, bx, by, z) {
        for (var r = 1; r <= SPIRAL_MAX; r++) {
            var ring = [];
            for (var x = bx - r; x <= bx + r; x++) ring.push([x, by - r]);
            for (var y = by - r + 1; y <= by + r - 1; y++) {
                ring.push([bx - r, y]); ring.push([bx + r, y]);
            }
            for (var x2 = bx - r; x2 <= bx + r; x2++) ring.push([x2, by + r]);
            for (var i = 0; i < ring.length; i++) {
                if (!cells[key3(ring[i][0], ring[i][1], z)]) return ring[i];
            }
        }
        return null;
    }

    function layoutZone(graph) {
        var byVnum = {};
        graph.rooms.forEach(function (r) { byVnum[r.v] = r; });
        // Directed exits per room, in deterministic order (dir rank, then
        // destination vnum, then key string for exotic same-dir duplicates).
        var exitsFrom = {};
        graph.exits.forEach(function (e) {
            if (!byVnum[e.f] || !byVnum[e.t]) return;
            (exitsFrom[e.f] = exitsFrom[e.f] || []).push(e);
        });
        Object.keys(exitsFrom).forEach(function (v) {
            exitsFrom[v].sort(function (a, b) {
                var ra = DIR_RANK[a.d], rb = DIR_RANK[b.d];
                ra = ra == null ? 99 : ra; rb = rb == null ? 99 : rb;
                if (ra !== rb) return ra - rb;
                if (a.t !== b.t) return a.t - b.t;
                return a.d < b.d ? -1 : a.d > b.d ? 1 : 0;
            });
        });

        var pos = {}, cells = {};
        var sorted = graph.rooms.map(function (r) { return r.v; })
                                .sort(function (a, b) { return a - b; });
        var globalMaxX = null;

        // One BFS per connected component; components stack left→right.
        for (var s = 0; s < sorted.length; s++) {
            var anchor = sorted[s];
            if (pos[anchor]) continue;
            var compVnums = [anchor];
            var compCells = {};
            var compPos = {};
            compPos[anchor] = { x: 0, y: 0, z: 0 };
            compCells[key3(0, 0, 0)] = anchor;
            var heap = [];
            heapPush(heap, { depth: 0, vnum: anchor });
            while (heap.length) {
                var curN = heapPop(heap);
                var from = compPos[curN.vnum];
                var outs = exitsFrom[curN.vnum] || [];
                for (var i = 0; i < outs.length; i++) {
                    var e = outs[i];
                    var delta = DELTA[e.d];
                    if (!delta) continue;              // named exit: no geometry
                    if (compPos[e.t] || pos[e.t]) continue;
                    var placed = null;
                    // Ideal cell, then stretch the edge 2×..4× — this is what
                    // resolves the classic n→e→s→w collision: the fourth
                    // room's ideal cell is taken by the anchor, so it lands
                    // one cell further with a length-2 edge.
                    for (var step = 1; step <= MAX_STRETCH && !placed; step++) {
                        var cx = from.x + delta[0] * step;
                        var cy = from.y + delta[1] * step;
                        var cz = from.z + delta[2] * step;
                        if (!compCells[key3(cx, cy, cz)]) placed = [cx, cy, cz];
                    }
                    if (!placed) {
                        var near = spiralFind(compCells,
                            from.x + delta[0], from.y + delta[1],
                            from.z + delta[2]);
                        if (near) placed = [near[0], near[1],
                                            from.z + delta[2]];
                    }
                    if (!placed) continue;   // pathological; drawn as portal
                    compPos[e.t] = { x: placed[0], y: placed[1], z: placed[2] };
                    compCells[key3(placed[0], placed[1], placed[2])] = e.t;
                    compVnums.push(e.t);
                    heapPush(heap, { depth: curN.depth + 1, vnum: e.t });
                }
            }
            // Shift this component to the right of everything placed so far.
            var minX = Infinity, maxX = -Infinity;
            compVnums.forEach(function (v) {
                if (compPos[v].x < minX) minX = compPos[v].x;
                if (compPos[v].x > maxX) maxX = compPos[v].x;
            });
            var shift = globalMaxX == null ? 0 : globalMaxX - minX + 2;
            compVnums.forEach(function (v) {
                var p = compPos[v];
                p.x += shift;
                pos[v] = p;
                cells[key3(p.x, p.y, p.z)] = v;
            });
            globalMaxX = globalMaxX == null ? maxX : maxX + shift;
        }

        // ---- classify every directed exit into drawable geometry ----
        // Two-way pairs merge into one drawn edge (key: sorted endpoints).
        var drawn = {};       // "a|b" -> edge object
        var portals = {};     // vnum -> [{d, t, cross}]
        var vert = {};        // vnum -> {u:1, d:1}
        var zsUsed = {};
        graph.rooms.forEach(function (r) {
            if (pos[r.v]) zsUsed[pos[r.v].z] = true;
        });

        function addPortal(v, d, t, cross) {
            (portals[v] = portals[v] || []).push({ d: d, t: t, cross: !!cross });
        }

        graph.exits.forEach(function (e) {
            var pf = pos[e.f], pt = pos[e.t];
            if (!pf || !pt) { addPortal(e.f, e.d, e.t); return; }
            var delta = DELTA[e.d];
            if (!delta) { addPortal(e.f, e.d, e.t); return; }
            if (e.d === "u" || e.d === "d") {
                (vert[e.f] = vert[e.f] || {})[e.d] = e.t;
                return;
            }
            if (pf.z !== pt.z) { addPortal(e.f, e.d, e.t); return; }
            var dx = pt.x - pf.x, dy = pt.y - pf.y;
            var kind;
            // Aligned iff the offset is a positive integer multiple of the
            // unit delta (diagonals need both axes in step).
            var k = null;
            if (delta[0] !== 0 && dx % delta[0] === 0) k = dx / delta[0];
            else if (delta[0] === 0 && dx === 0 && delta[1] !== 0) k = dy / delta[1];
            var aligned = k != null && k >= 1 &&
                dx === delta[0] * k && dy === delta[1] * k;
            // A geometric contradiction between far-apart rooms (e.g. a
            // cross-component link) would draw a dogleg across half the
            // zone; degrade to portal badges instead.
            if (!aligned && Math.abs(dx) + Math.abs(dy) > 6) {
                addPortal(e.f, e.d, e.t);
                return;
            }
            kind = aligned ? (k === 1 ? "grid" : "stretch") : "bent";
            var a = Math.min(e.f, e.t), b = Math.max(e.f, e.t);
            var dk = a + "|" + b;
            var prev = drawn[dk];
            if (prev) {
                // The reverse direction exists: not one-way; merge flags.
                prev.one = 0;
                prev.door = prev.door || e.door || 0;
                prev.locked = prev.locked || e.locked || 0;
                return;
            }
            drawn[dk] = {
                f: e.f, t: e.t, z: pf.z, kind: kind,
                ax: pf.x, ay: pf.y, bx: pt.x, by: pt.y,
                door: e.door || 0, locked: e.locked || 0,
                one: e.one ? 1 : 0
            };
        });

        // Cross-zone exits. `outFrom` is the complete adjacency (every
        // cross-zone exit regardless of geometry) that cross-zone
        // pathfinding walks; `outStubs` is the drawable horizontal subset.
        var outStubs = {};   // vnum -> [{d, zone, zname, t}]  (drawn arrows)
        var outFrom = {};    // vnum -> [{f, d, t, zone, zname}]  (all crosses)
        (graph.out || []).forEach(function (o) {
            (outFrom[o.f] = outFrom[o.f] || []).push(o);
            if (!pos[o.f]) return;
            if (DELTA[o.d] && o.d !== "u" && o.d !== "d") {
                (outStubs[o.f] = outStubs[o.f] || []).push(o);
            } else {
                addPortal(o.f, o.d, o.t, true);
            }
        });

        var edges = Object.keys(drawn).sort().map(function (k) { return drawn[k]; });
        var zList = Object.keys(zsUsed).map(Number).sort(function (a, b) { return a - b; });
        return {
            pos: pos, cells: cells, edges: edges, portals: portals,
            vert: vert, out: outStubs, outFrom: outFrom, zList: zList,
            exitsFrom: exitsFrom, byVnum: byVnum
        };
    }

    // ------------------------------------------------------------------
    // Fog helpers
    // ------------------------------------------------------------------
    function fogSet(zoneId) {
        return (fog[zoneId] = fog[zoneId] || { set: {} }).set;
    }
    function discovered(zoneId, v) { return !!fogSet(zoneId)[v]; }
    // Frontier: undiscovered rooms one directed exit away from a discovered
    // room. Cached per zone until fog/graph changes.
    function frontier(zoneId) {
        var c = frontierCache[zoneId];
        if (c && c.stamp === fogStamp) return c.set;
        var set = {};
        var zone = zones[zoneId];
        if (zone) {
            var fs = fogSet(zoneId);
            Object.keys(fs).forEach(function (v) {
                var outs = zone.layout.exitsFrom[v] || [];
                for (var i = 0; i < outs.length; i++) {
                    if (!fs[outs[i].t]) set[outs[i].t] = true;
                }
                var vv = zone.layout.vert[v];
                if (vv) {
                    if (vv.u && !fs[vv.u]) set[vv.u] = true;
                    if (vv.d && !fs[vv.d]) set[vv.d] = true;
                }
            });
        }
        frontierCache[zoneId] = { stamp: fogStamp, set: set };
        return set;
    }

    // ------------------------------------------------------------------
    // Draw core — one renderer for the minimap and the big map.
    // ------------------------------------------------------------------
    // view = {cx, cy: world-cell center; scale: px per cell; z: plane}
    function drawMap(canvas, zoneId, view, opts) {
        opts = opts || {};
        var zone = zones[zoneId];
        var ctx = canvas.getContext("2d");
        var dpr = window.devicePixelRatio || 1;
        var cssW = canvas.clientWidth, cssH = canvas.clientHeight;
        if (!cssW || !cssH) return;
        if (canvas.width !== Math.round(cssW * dpr) ||
            canvas.height !== Math.round(cssH * dpr)) {
            canvas.width = Math.round(cssW * dpr);
            canvas.height = Math.round(cssH * dpr);
        }
        if (!palette) readPalette();
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx.clearRect(0, 0, cssW, cssH);
        if (!zone) return;

        var L = zone.layout, sc = view.scale;
        var fs = fogSet(zoneId), fr = frontier(zoneId);
        var pathSet = opts.pathVnums || null;
        var pathEdges = opts.pathEdges || null;

        function sx(wx) { return (wx - view.cx) * sc + cssW / 2; }
        function sy(wy) { return (wy - view.cy) * sc + cssH / 2; }
        var pad = 1;   // world-cell cull margin
        var minWX = view.cx - cssW / 2 / sc - pad, maxWX = view.cx + cssW / 2 / sc + pad;
        var minWY = view.cy - cssH / 2 / sc - pad, maxWY = view.cy + cssH / 2 / sc + pad;
        var box = sc * 0.62;                  // room square size in px
        var half = box / 2;

        function visibleRoom(v) {
            return fs[v] || fr[v];
        }

        // ---- edges ----
        ctx.lineWidth = Math.max(1, sc * 0.07);
        for (var i = 0; i < L.edges.length; i++) {
            var e = L.edges[i];
            if (e.z !== view.z) continue;
            if ((e.ax < minWX && e.bx < minWX) || (e.ax > maxWX && e.bx > maxWX) ||
                (e.ay < minWY && e.by < minWY) || (e.ay > maxWY && e.by > maxWY)) continue;
            // An edge shows when one end is discovered and the other is at
            // least frontier — the same knowledge walking there would give.
            var fD = fs[e.f], tD = fs[e.t];
            if (!((fD && visibleRoom(e.t)) || (tD && visibleRoom(e.f)))) continue;
            var onPath = pathEdges && pathEdges[e.f + "|" + e.t];
            ctx.strokeStyle = onPath ? palette.accent : palette.border;
            ctx.globalAlpha = onPath ? 0.9 : 1;
            var x1 = sx(e.ax), y1 = sy(e.ay), x2 = sx(e.bx), y2 = sy(e.by);
            ctx.beginPath();
            if (e.kind === "bent") {
                // Dogleg: bend along the larger axis first — deterministic.
                var mx, my;
                if (Math.abs(e.bx - e.ax) >= Math.abs(e.by - e.ay)) { mx = x2; my = y1; }
                else { mx = x1; my = y2; }
                ctx.moveTo(x1, y1); ctx.lineTo(mx, my); ctx.lineTo(x2, y2);
            } else {
                ctx.moveTo(x1, y1); ctx.lineTo(x2, y2);
            }
            ctx.stroke();
            // Door tick: short perpendicular bar at the midpoint.
            if (e.door && e.kind !== "bent") {
                var mx2 = (x1 + x2) / 2, my2 = (y1 + y2) / 2;
                var ang = Math.atan2(y2 - y1, x2 - x1) + Math.PI / 2;
                var tl = Math.max(3, sc * 0.16);
                ctx.strokeStyle = e.locked ? palette.warn : palette.dim;
                ctx.beginPath();
                ctx.moveTo(mx2 - Math.cos(ang) * tl, my2 - Math.sin(ang) * tl);
                ctx.lineTo(mx2 + Math.cos(ang) * tl, my2 + Math.sin(ang) * tl);
                ctx.stroke();
            }
            // One-way arrowhead at the destination third.
            if (e.one && e.kind !== "bent") {
                var px3 = x1 + (x2 - x1) * 0.68, py3 = y1 + (y2 - y1) * 0.68;
                var a2 = Math.atan2(y2 - y1, x2 - x1);
                var al = Math.max(3, sc * 0.14);
                ctx.strokeStyle = palette.dim;
                ctx.beginPath();
                ctx.moveTo(px3 - Math.cos(a2 - 0.5) * al, py3 - Math.sin(a2 - 0.5) * al);
                ctx.lineTo(px3, py3);
                ctx.lineTo(px3 - Math.cos(a2 + 0.5) * al, py3 - Math.sin(a2 + 0.5) * al);
                ctx.stroke();
            }
        }
        ctx.globalAlpha = 1;

        // ---- cross-zone stubs (from discovered rooms only) ----
        ctx.strokeStyle = palette.dim;
        Object.keys(L.out).forEach(function (v) {
            var p = L.pos[v];
            if (!p || p.z !== view.z || !fs[v]) return;
            if (p.x < minWX || p.x > maxWX || p.y < minWY || p.y > maxWY) return;
            L.out[v].forEach(function (o) {
                var dd = DELTA[o.d];
                if (!dd) return;
                var x1 = sx(p.x) + dd[0] * half, y1 = sy(p.y) + dd[1] * half;
                var x2 = sx(p.x) + dd[0] * sc * 0.55, y2 = sy(p.y) + dd[1] * sc * 0.55;
                ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
                var a3 = Math.atan2(y2 - y1, x2 - x1);
                var al2 = Math.max(3, sc * 0.14);
                ctx.beginPath();
                ctx.moveTo(x2 - Math.cos(a3 - 0.5) * al2, y2 - Math.sin(a3 - 0.5) * al2);
                ctx.lineTo(x2, y2);
                ctx.lineTo(x2 - Math.cos(a3 + 0.5) * al2, y2 - Math.sin(a3 + 0.5) * al2);
                ctx.stroke();
            });
        });

        // ---- rooms ----
        var noteMap = notes[zoneId] || {};
        var rooms = zone.graph.rooms;
        for (var r = 0; r < rooms.length; r++) {
            var v = rooms[r].v;
            var p = L.pos[v];
            if (!p || p.z !== view.z) continue;
            if (p.x < minWX || p.x > maxWX || p.y < minWY || p.y > maxWY) continue;
            var x = sx(p.x), y = sy(p.y);
            if (fs[v]) {
                ctx.fillStyle = terrainColor(rooms[r].t);
                ctx.fillRect(x - half, y - half, box, box);
                ctx.strokeStyle = palette.border;
                ctx.lineWidth = 1;
                ctx.strokeRect(x - half, y - half, box, box);
                // Death corner triangle.
                if (rooms[r].f && rooms[r].f.indexOf("death") !== -1) {
                    ctx.fillStyle = palette.danger;
                    ctx.beginPath();
                    ctx.moveTo(x + half, y - half);
                    ctx.lineTo(x + half, y - half + box * 0.4);
                    ctx.lineTo(x + half - box * 0.4, y - half);
                    ctx.fill();
                }
                // Note dot.
                if (noteMap[v]) {
                    ctx.fillStyle = palette.info;
                    ctx.beginPath();
                    ctx.arc(x - half + box * 0.16, y - half + box * 0.16,
                            Math.max(1.5, box * 0.1), 0, Math.PI * 2);
                    ctx.fill();
                }
                // Up/down chevrons.
                var vv = L.vert[v];
                if (vv) {
                    ctx.fillStyle = palette.dim;
                    var cw = Math.max(2.5, box * 0.16);
                    if (vv.u) {
                        ctx.beginPath();
                        ctx.moveTo(x + half - cw * 1.6, y - half + cw * 1.4);
                        ctx.lineTo(x + half - cw * 0.6, y - half + cw * 1.4);
                        ctx.lineTo(x + half - cw * 1.1, y - half + cw * 0.5);
                        ctx.fill();
                    }
                    if (vv.d) {
                        ctx.beginPath();
                        ctx.moveTo(x + half - cw * 1.6, y + half - cw * 1.4);
                        ctx.lineTo(x + half - cw * 0.6, y + half - cw * 1.4);
                        ctx.lineTo(x + half - cw * 1.1, y + half - cw * 0.5);
                        ctx.fill();
                    }
                }
                // Portal badge (named exit): small diamond on the left edge.
                if (L.portals[v]) {
                    ctx.fillStyle = palette.dim;
                    var pw = Math.max(2, box * 0.14);
                    ctx.beginPath();
                    ctx.moveTo(x - half + pw * 1.1, y);
                    ctx.lineTo(x - half + pw * 2.1, y - pw);
                    ctx.lineTo(x - half + pw * 3.1, y);
                    ctx.lineTo(x - half + pw * 2.1, y + pw);
                    ctx.fill();
                }
                // Path membership ring.
                if (pathSet && pathSet[v] && v !== opts.curVnum) {
                    ctx.strokeStyle = palette.accent;
                    ctx.globalAlpha = 0.6;
                    ctx.lineWidth = Math.max(1, sc * 0.06);
                    ctx.strokeRect(x - half - 1.5, y - half - 1.5, box + 3, box + 3);
                    ctx.globalAlpha = 1;
                }
            } else if (fr[v]) {
                // Frontier stub: dashed dim outline, no fill, no badges —
                // exploration is not spoiled.
                ctx.strokeStyle = palette.border;
                ctx.lineWidth = 1;
                ctx.setLineDash([3, 3]);
                ctx.strokeRect(x - half, y - half, box, box);
                ctx.setLineDash([]);
            }
        }

        // ---- current room ring (never while unseen) ----
        if (opts.curVnum && !opts.unseen) {
            var cp = L.pos[opts.curVnum];
            if (cp && cp.z === view.z) {
                ctx.strokeStyle = palette.accent;
                ctx.lineWidth = 2;
                ctx.strokeRect(sx(cp.x) - half - 2.5, sy(cp.y) - half - 2.5,
                               box + 5, box + 5);
            }
        }

        // ---- search hit ring ----
        if (opts.searchVnum) {
            var sp = L.pos[opts.searchVnum];
            if (sp && sp.z === view.z) {
                ctx.strokeStyle = palette.info;
                ctx.lineWidth = 2;
                ctx.strokeRect(sx(sp.x) - half - 4, sy(sp.y) - half - 4,
                               box + 8, box + 8);
            }
        }
    }

    // Invert a canvas point to a room vnum (grid hit-test).
    function hitTest(zoneId, view, canvas, px, py) {
        var zone = zones[zoneId];
        if (!zone) return null;
        var cssW = canvas.clientWidth, cssH = canvas.clientHeight;
        var wx = Math.round((px - cssW / 2) / view.scale + view.cx);
        var wy = Math.round((py - cssH / 2) / view.scale + view.cy);
        var v = zone.layout.cells[key3(wx, wy, view.z)];
        if (v == null) return null;
        // Only hit visible rooms.
        return (fogSet(zoneId)[v] || frontier(zoneId)[v]) ? v : null;
    }

    // ------------------------------------------------------------------
    // Server I/O
    // ------------------------------------------------------------------
    function graphUrl(vnum) { return cfg.urls.graph.replace(/0\/$/, vnum + "/"); }
    function stateUrl(zoneId) { return cfg.urls.state.replace(/0\/$/, zoneId + "/"); }

    function requestGraph(vnum) {
        if (cfg.demo || !cfg.urls || pendingGraph[vnum]) return;
        // Backoff: after a failure, wait 10s before trying any graph again.
        if (lastGraphFail && (Date.now() - lastGraphFail) < 10000) return;
        pendingGraph[vnum] = true;
        fetch(graphUrl(vnum), { credentials: "same-origin" })
            .then(function (resp) {
                if (!resp.ok) throw new Error("graph " + resp.status);
                return resp.json();
            })
            .then(function (graph) {
                delete pendingGraph[vnum];
                registerGraph(graph);
                loadState(graph.zone.id);
            })
            .catch(function () {
                delete pendingGraph[vnum];
                lastGraphFail = Date.now();
            });
    }

    function registerGraph(graph) {
        if (!graph || !graph.zone || !Array.isArray(graph.rooms)) return;
        var zoneId = graph.zone.id;
        zones[zoneId] = {
            graph: graph,
            layout: layoutZone(graph),
            name: graph.zone.name || ""
        };
        graph.rooms.forEach(function (r) { vnumZone[r.v] = zoneId; });
        fogStamp++;
        // The room that triggered the fetch may be waiting.
        if (cur.vnum != null && vnumZone[cur.vnum] === zoneId) {
            enterZone(zoneId, cur.vnum);
        }
        // A cross-zone "Go to <zone>" awaiting this graph refocuses now.
        if (pendingFocus != null && vnumZone[pendingFocus] === zoneId) {
            var fv = pendingFocus;
            pendingFocus = null;
            focusZone(zoneId, fv);
        }
    }

    function loadState(zoneId) {
        mergeLocalFog(zoneId);
        if (cfg.demo || !cfg.urls || stateLoaded[zoneId]) { redraw(); return; }
        stateLoaded[zoneId] = true;
        fetch(stateUrl(zoneId), { credentials: "same-origin" })
            .then(function (resp) {
                if (!resp.ok) throw new Error("state " + resp.status);
                return resp.json();
            })
            .then(function (state) {
                var fs = fogSet(zoneId);
                (state.discovered || []).forEach(function (v) { fs[v] = true; });
                notes[zoneId] = notes[zoneId] || {};
                Object.keys(state.notes || {}).forEach(function (k) {
                    notes[zoneId][k] = state.notes[k];
                });
                // Local-only discoveries (offline walking) self-heal to the
                // server on the next flush.
                var mirror = localFog(zoneId);
                Object.keys(mirror).forEach(function (v) {
                    v = Number(v);
                    if (!(state.discovered || []).some(function (x) { return x === v; })) {
                        if (dirty.indexOf(v) === -1) dirty.push(v);
                    }
                });
                if (dirty.length) scheduleFlush();
                fogStamp++;
                redraw();
            })
            .catch(function () { stateLoaded[zoneId] = false; });
    }

    // localStorage mirror: fog survives reloads and offline play.
    function localFog(zoneId) {
        try {
            var arr = JSON.parse(localStorage.getItem("ishar.mapSeen." + zoneId));
            var m = {};
            if (Array.isArray(arr)) arr.forEach(function (v) {
                if (typeof v === "number") m[v] = true;
            });
            return m;
        } catch (e) { return {}; }
    }
    function mergeLocalFog(zoneId) {
        var m = localFog(zoneId), fs = fogSet(zoneId), changed = false;
        Object.keys(m).forEach(function (v) {
            if (!fs[v]) { fs[v] = true; changed = true; }
        });
        if (changed) fogStamp++;
    }
    function saveLocalFog(zoneId) {
        try {
            localStorage.setItem("ishar.mapSeen." + zoneId,
                JSON.stringify(Object.keys(fogSet(zoneId)).map(Number)));
        } catch (e) {}
    }

    function scheduleFlush() {
        if (flushTimer || cfg.demo) return;
        flushTimer = setTimeout(function () { flushTimer = null; doFlush(false); }, 30000);
    }
    function doFlush(keepalive) {
        if (!dirty.length || cfg.demo || !cfg.urls) return;
        var batch = dirty.slice(0, 200);
        fetch(cfg.urls.discover, {
            method: "POST",
            credentials: "same-origin",
            keepalive: !!keepalive,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": cfg.csrf
            },
            body: JSON.stringify({ rooms: batch })
        }).then(function (resp) {
            if (!resp.ok) return;
            dirty = dirty.filter(function (v) { return batch.indexOf(v) === -1; });
        }).catch(function () {});
    }

    // ------------------------------------------------------------------
    // Live feed: called by hud.js on every Room.Info.
    // ------------------------------------------------------------------
    function enabled() { return cfg.demo || cfg.authed; }

    function onRoom(room) {
        if (!enabled()) return;
        // Visibility gate: a redacted payload has no num — the player can't
        // see. Nothing accrues, the ring drops, autowalk aborts; the last
        // known view stays put. (telnet.c:572, issue #1699)
        var num = room && room.num;
        if (typeof num !== "number" || !(num > 0)) {
            setUnseen(true);
            return;
        }
        cur.unseen = false;
        cur.vnum = num;
        var zoneId = vnumZone[num];
        if (zoneId == null) {
            requestGraph(num);
            redraw();
            return;
        }
        enterZone(zoneId, num);
    }

    function enterZone(zoneId, vnum) {
        var zoneChanged = cur.zone !== zoneId;
        if (zoneChanged && cur.zone != null) doFlush(false);
        cur.zone = zoneId;
        cur.vnum = vnum;
        var p = zones[zoneId].layout.pos[vnum];
        cur.z = p ? p.z : 0;
        accrue(vnum, zoneId);
        walkOnRoom(vnum);
        shownPathOnRoom(vnum);
        redraw();
    }

    function accrue(vnum, zoneId) {
        var fs = fogSet(zoneId);
        if (fs[vnum]) return;
        fs[vnum] = true;
        fogStamp++;
        saveLocalFog(zoneId);
        if (dirty.indexOf(vnum) === -1) dirty.push(vnum);
        if (dirty.length >= 10) doFlush(false);
        else scheduleFlush();
    }

    function setUnseen(on) {
        var was = cur.unseen;
        cur.unseen = !!on;
        if (on) cancelWalk("darkness");
        if (was !== cur.unseen) redraw();
    }

    function onReset() {
        cancelWalk("reset");
        setShownPath(null);
        cur.vnum = null;
        cur.unseen = false;
        redraw();
    }
    function onConnected(on) {
        if (!on) cancelWalk("disconnected");
    }

    // ------------------------------------------------------------------
    // Minimap — mounted into the Room panel's Map tab by hud.js.
    // ------------------------------------------------------------------
    var mini = null;   // {wrap, canvas, hint}
    var MINI_SCALE = 30;

    function buildMini() {
        var canvas = H.el("canvas", { class: "map-canvas menu-opener" });
        var hint = H.el("div", { class: "map-hint", text: "Location unknown" });
        hint.hidden = true;
        var wrap = H.el("div", { class: "map-mini" }, [canvas, hint]);
        canvas.addEventListener("click", function (ev) {
            if (cur.zone == null || cur.unseen) return;
            var r = canvas.getBoundingClientRect();
            var v = hitTest(cur.zone, miniView(), canvas,
                            ev.clientX - r.left, ev.clientY - r.top);
            if (v == null || v === cur.vnum) return;
            var step = adjacentStep(cur.vnum, v);
            if (step) { H.send(step); return; }
            mapRoomMenu(cur.zone, v, { getBoundingClientRect: function () {
                return { left: ev.clientX, right: ev.clientX,
                         top: ev.clientY, bottom: ev.clientY,
                         width: 0, height: 0 };
            } });
        });
        mini = { wrap: wrap, canvas: canvas, hint: hint };
    }
    function miniView() {
        var c = { cx: 0, cy: 0, scale: MINI_SCALE, z: cur.z };
        if (cur.zone != null && cur.vnum != null) {
            var p = zones[cur.zone].layout.pos[cur.vnum];
            if (p) { c.cx = p.x; c.cy = p.y; c.z = p.z; }
        }
        return c;
    }
    function renderMini(container) {
        if (!mini) buildMini();
        container.appendChild(mini.wrap);
        // Draw after layout so clientWidth is real.
        requestAnimationFrame(redrawMini);
    }
    function redrawMini() {
        if (!mini || !mini.wrap.isConnected) return;
        mini.hint.hidden = !(cur.unseen || cur.zone == null);
        if (cur.zone == null) {
            mini.hint.hidden = false;
            mini.hint.textContent = enabled() ? "Mapping…" : "Map unavailable";
        } else {
            mini.hint.textContent = "Location unknown";
        }
        mini.wrap.classList.toggle("unseen", cur.unseen);
        if (cur.zone != null) {
            drawMap(mini.canvas, cur.zone, miniView(), {
                curVnum: cur.vnum, unseen: cur.unseen,
                pathVnums: walkPathVnums(), pathEdges: walkPathEdges()
            });
        } else {
            var ctx = mini.canvas.getContext("2d");
            ctx && ctx.clearRect(0, 0, mini.canvas.width, mini.canvas.height);
        }
    }

    // If `to` is one exit away from `from`, return the command that walks it.
    function adjacentStep(from, to) {
        if (cur.zone == null) return null;
        var outs = zones[cur.zone].layout.exitsFrom[from] || [];
        for (var i = 0; i < outs.length; i++) {
            if (outs[i].t === to) return stepCmd(outs[i].d);
        }
        return null;
    }
    function stepCmd(d) { return DELTA[d] ? d : "go " + d; }

    // ------------------------------------------------------------------
    // Big map overlay (OVERLAYS app "map", Ctrl+M): pan/zoom/tap canvas
    // with a toolbar (zone name · z-levels · search · zoom · center).
    // ------------------------------------------------------------------
    var big = null;   // {root, canvas, wrap, zoneLabel, zRow, search, count, anchor}
    // `zone` is the zone the big map is *looking at* — normally the player's
    // (cur.zone), but a cross-zone "Go to" or a border tap can point it at an
    // adjacent zone while the player stays put. viewedZone() resolves it.
    var bigView = { cx: 0, cy: 0, scale: 30, z: 0, follow: true, zone: null };
    var BIG_MIN = 12, BIG_MAX = 75;
    var searchState = { q: "", list: [], i: -1 };
    var hoverVnum = null;
    var pendingFocusView = null; // {zone, vnum} to apply once the overlay is up
    var bigZoneShown = null;     // last zone the big map's chrome was built for

    function viewedZone() {
        return bigView.zone != null ? bigView.zone : cur.zone;
    }

    function bigOpen() {
        return !!(big && big.root.isConnected && H && H.overlayVisible("map"));
    }

    function buildBig() {
        var canvas = H.el("canvas", { class: "map-canvas menu-opener" });
        // Synthetic tooltip anchor: an invisible box moved onto the hovered
        // room so hud.js's positionTip has a rect to aim at.
        var anchor = H.el("div", { class: "map-tip-anchor", "aria-hidden": "true" });
        var wrap = H.el("div", { class: "map-big" }, [canvas, anchor]);

        var zoneLabel = H.el("span", { class: "map-zone", text: "" });
        // Cross-zone picker: the discoverable home for "look at / walk to
        // another zone" (the per-room border menu is the shortcut, not the
        // signpost). Lists the neighbors reachable from explored borders.
        var btnZones = H.el("button", {
            type: "button", class: "map-btn map-zones", text: "Zones ▾",
            title: "View or jump to an adjacent zone",
            "aria-label": "View or jump to an adjacent zone",
            onclick: function () { openZoneJump(btnZones); }
        });
        var zRow = H.el("span", { class: "map-z" });
        var search = H.el("input", {
            class: "map-search", type: "search", placeholder: "Find room…",
            "aria-label": "Find a discovered room by name"
        });
        var count = H.el("span", { class: "map-count dim", text: "" });
        var btnOut = H.el("button", { type: "button", class: "map-btn", text: "−",
            title: "Zoom out", "aria-label": "Zoom out",
            onclick: function () { zoomBy(1 / 1.3); } });
        var btnIn = H.el("button", { type: "button", class: "map-btn", text: "+",
            title: "Zoom in", "aria-label": "Zoom in",
            onclick: function () { zoomBy(1.3); } });
        var btnMe = H.el("button", { type: "button", class: "map-btn", text: "◎",
            title: "Center on me", "aria-label": "Center on my room",
            onclick: function () { bigView.follow = true; centerOnMe(); redraw(); } });
        var toolbar = H.el("div", { class: "map-toolbar" },
            [zoneLabel, btnZones, zRow, search, count, btnOut, btnIn, btnMe]);
        var foot = H.el("div", { class: "map-foot" });
        foot.hidden = true;
        var root = H.el("div", { class: "map-app" }, [toolbar, wrap, foot]);
        big = { root: root, canvas: canvas, wrap: wrap, zoneLabel: zoneLabel,
                zRow: zRow, search: search, count: count, anchor: anchor,
                foot: foot, btnMe: btnMe, btnZones: btnZones };

        // --- search: filter discovered rooms, Enter cycles + centers ---
        search.addEventListener("input", function () {
            searchState.q = search.value;
            rebuildSearch();
            updateSearchCount();
            redrawBig();
        });
        search.addEventListener("keydown", function (ev) {
            if (ev.key === "Enter" && searchState.list.length) {
                ev.preventDefault();
                searchState.i = (searchState.i + 1) % searchState.list.length;
                var v = searchState.list[searchState.i];
                var vz = viewedZone();
                var p = vz != null && zones[vz].layout.pos[v];
                if (p) {
                    bigView.follow = false;
                    bigView.cx = p.x; bigView.cy = p.y; bigView.z = p.z;
                    updateZRow();
                }
                updateSearchCount();
                redrawBig();
            }
            // The overlay's Esc handler must not steal a "clear the field".
            if (ev.key === "Escape" && search.value) ev.stopPropagation();
        });

        // --- pan / pinch / tap (pointer events; gestures are enhancement,
        // the zoom buttons are the accessible path) ---
        var pointers = {};
        var pinchDist = null;
        var drag = null;
        canvas.addEventListener("pointerdown", function (ev) {
            canvas.setPointerCapture(ev.pointerId);
            pointers[ev.pointerId] = { x: ev.clientX, y: ev.clientY };
            var keys = Object.keys(pointers);
            if (keys.length === 1) {
                drag = { x: ev.clientX, y: ev.clientY, moved: false };
            } else if (keys.length === 2) {
                var a = pointers[keys[0]], b = pointers[keys[1]];
                pinchDist = Math.hypot(a.x - b.x, a.y - b.y);
                drag = null;
            }
        });
        canvas.addEventListener("pointermove", function (ev) {
            var pt = pointers[ev.pointerId];
            if (!pt) return;
            var keys = Object.keys(pointers);
            if (keys.length === 2) {
                pt.x = ev.clientX; pt.y = ev.clientY;
                var a = pointers[keys[0]], b = pointers[keys[1]];
                var d2 = Math.hypot(a.x - b.x, a.y - b.y);
                if (pinchDist && d2 > 0) zoomBy(d2 / pinchDist);
                pinchDist = d2;
                return;
            }
            if (drag) {
                var dx = ev.clientX - drag.x, dy = ev.clientY - drag.y;
                if (Math.abs(dx) + Math.abs(dy) > 4) drag.moved = true;
                if (drag.moved) {
                    bigView.follow = false;
                    bigView.cx -= dx / bigView.scale;
                    bigView.cy -= dy / bigView.scale;
                    drag.x = ev.clientX; drag.y = ev.clientY;
                    redrawBig();
                }
            }
            pt.x = ev.clientX; pt.y = ev.clientY;
        });
        function endPointer(ev) {
            var wasDrag = drag;
            delete pointers[ev.pointerId];
            if (Object.keys(pointers).length < 2) pinchDist = null;
            if (ev.type === "pointerup" && wasDrag && !wasDrag.moved) {
                var r = canvas.getBoundingClientRect();
                var v = hitTest(viewedZone(), bigView, canvas,
                                ev.clientX - r.left, ev.clientY - r.top);
                if (v != null) mapRoomMenu(viewedZone(), v,
                                           syntheticAnchor(ev.clientX, ev.clientY));
            }
            if (ev.type === "pointerup" || ev.type === "pointercancel") drag = null;
        }
        canvas.addEventListener("pointerup", endPointer);
        canvas.addEventListener("pointercancel", endPointer);

        // Wheel zoom, centered on the cursor.
        canvas.addEventListener("wheel", function (ev) {
            ev.preventDefault();
            var r = canvas.getBoundingClientRect();
            zoomBy(ev.deltaY < 0 ? 1.18 : 1 / 1.18,
                   ev.clientX - r.left, ev.clientY - r.top);
        }, { passive: false });

        // Hover tooltip (hover-capable pointers only; touch taps the menu).
        if (window.matchMedia("(hover: hover)").matches) {
            canvas.addEventListener("mousemove", function (ev) {
                if (Object.keys(pointers).length) return;   // mid-drag
                var r = canvas.getBoundingClientRect();
                var v = hitTest(viewedZone(), bigView, canvas,
                                ev.clientX - r.left, ev.clientY - r.top);
                if (v === hoverVnum) return;
                hoverVnum = v;
                if (v == null) { H.hideTip(); return; }
                showRoomTip(v);
            });
            canvas.addEventListener("mouseleave", function () {
                hoverVnum = null; H.hideTip();
            });
        }
    }

    function syntheticAnchor(cx, cy) {
        return { getBoundingClientRect: function () {
            return { left: cx, right: cx, top: cy, bottom: cy, width: 0, height: 0 };
        } };
    }

    function showRoomTip(v) {
        var zid = viewedZone();
        var zone = zones[zid];
        if (!zone || !big) return;
        var fs = fogSet(zid);
        var room = zone.layout.byVnum[v];
        var p = zone.layout.pos[v];
        if (!p) return;
        // Position the invisible anchor over the room's screen rect.
        var cssW = big.canvas.clientWidth, cssH = big.canvas.clientHeight;
        var sc = bigView.scale, halfBox = sc * 0.31;
        var x = (p.x - bigView.cx) * sc + cssW / 2;
        var y = (p.y - bigView.cy) * sc + cssH / 2;
        big.anchor.style.left = (x - halfBox) + "px";
        big.anchor.style.top = (y - halfBox) + "px";
        big.anchor.style.width = (halfBox * 2) + "px";
        big.anchor.style.height = (halfBox * 2) + "px";
        if (!fs[v]) { H.showTip(big.anchor, { name: "Unexplored" }); return; }
        var note = noteFor(v);
        H.showTip(big.anchor, {
            name: H.stripColor(room.n),
            sub: room.t + (note ? " · " + firstLine(note) : "")
        });
    }
    function firstLine(s) {
        var line = String(s).split("\n")[0];
        return line.length > 60 ? line.slice(0, 57) + "…" : line;
    }

    function zoomBy(factor, px, py) {
        var next = Math.max(BIG_MIN, Math.min(BIG_MAX, bigView.scale * factor));
        if (next === bigView.scale || !big) return;
        // Keep the point under the cursor (or the center) fixed.
        var cssW = big.canvas.clientWidth, cssH = big.canvas.clientHeight;
        if (px == null) { px = cssW / 2; py = cssH / 2; }
        var wx = (px - cssW / 2) / bigView.scale + bigView.cx;
        var wy = (py - cssH / 2) / bigView.scale + bigView.cy;
        bigView.scale = next;
        bigView.cx = wx - (px - cssW / 2) / next;
        bigView.cy = wy - (py - cssH / 2) / next;
        redrawBig();
    }

    function centerOnMe() {
        if (cur.zone == null || cur.vnum == null) return;
        bigView.zone = cur.zone;   // following the player snaps back on-zone
        var p = zones[cur.zone].layout.pos[cur.vnum];
        if (p) { bigView.cx = p.x; bigView.cy = p.y; bigView.z = p.z; }
    }

    // Point the big map at another (already-loaded) zone without moving the
    // player. Opens the overlay if it isn't up yet.
    function focusZone(zoneId, vnum) {
        pendingFocusView = { zone: zoneId, vnum: vnum };
        if (!bigOpen() && H && H.toggleOverlay) H.toggleOverlay("map");
        applyFocus();
    }
    function applyFocus() {
        if (!pendingFocusView || !big) return;
        var f = pendingFocusView;
        if (!zones[f.zone]) return;   // graph not here yet; renderOverlay retries
        pendingFocusView = null;
        mergeLocalFog(f.zone);   // show the neighbor's remembered fog at once
        bigView.zone = f.zone;
        bigView.follow = false;
        var p = zones[f.zone].layout.pos[f.vnum];
        if (p) { bigView.cx = p.x; bigView.cy = p.y; bigView.z = p.z; }
        searchState = { q: "", list: [], i: -1 };
        if (big.search) big.search.value = "";
        bigZoneShown = f.zone;
        updateZoneLabel(); updateZRow(); updateSearchCount(); updateMeButton();
        redrawBig();
    }
    // Toolbar "Zones ▾" menu: every neighbor reachable from an explored
    // border of the viewed zone, plus a "back to my location" when off-zone.
    function openZoneJump(anchor) {
        var zid = viewedZone();
        if (zid == null || !zones[zid]) return;
        var zone = zones[zid], fs = fogSet(zid);
        var acts = [];
        if (cur.zone != null && zid !== cur.zone) {
            acts.push({
                label: "◎ Back to my location",
                fn: function () { bigView.follow = true; centerOnMe(); redraw(); }
            });
        }
        // One entry per adjacent zone, keyed off discovered border rooms so
        // we only surface crossings the player has actually found.
        var byZone = {};
        zone.graph.rooms.forEach(function (r) {
            if (!fs[r.v]) return;
            (zone.layout.outFrom[r.v] || []).forEach(function (o) {
                if (!byZone[o.zone]) byZone[o.zone] = o;
            });
        });
        var keys = Object.keys(byZone);
        keys.sort(function (a, b) {
            var na = byZone[a].zname || "", nb = byZone[b].zname || "";
            return na < nb ? -1 : na > nb ? 1 : 0;
        });
        keys.forEach(function (k) {
            var o = byZone[k];
            acts.push({
                label: "Go to " + (o.zname || "zone " + o.zone) + " →",
                fn: (function (oo) {
                    return function () { goToZone(oo.zone, oo.t, oo.zname); };
                })(o)
            });
        });
        if (!keys.length) {
            acts.push({
                label: "Walk to a zone border to unlock jumps",
                fn: function () {}, keep: true
            });
        }
        H.openMenu("Jump to zone", acts, anchor);
    }

    // Menu action: jump the map to an adjacent zone, loading it if needed.
    function goToZone(zoneId, vnum, zname) {
        if (zones[zoneId]) { focusZone(zoneId, vnum); return; }
        pendingFocus = vnum;
        if (!bigOpen() && H && H.toggleOverlay) H.toggleOverlay("map");
        if (big) big.zoneLabel.textContent = (zname || "Loading") + " …";
        requestGraph(vnum);
    }
    // The ◎ button doubles as "return to my location" when off-zone.
    function updateMeButton() {
        if (!big || !big.btnMe) return;
        var off = cur.zone != null && bigView.zone != null &&
                  bigView.zone !== cur.zone;
        big.btnMe.classList.toggle("active", off);
        big.btnMe.title = off ? "Return to my location" : "Center on me";
        big.btnMe.setAttribute("aria-label", big.btnMe.title);
    }

    function rebuildSearch() {
        searchState.list = [];
        searchState.i = -1;
        var q = searchState.q.trim().toLowerCase();
        var zid = viewedZone();
        if (!q || zid == null) return;
        var zone = zones[zid];
        var fs = fogSet(zid);
        zone.graph.rooms.forEach(function (r) {
            if (fs[r.v] &&
                H.stripColor(r.n).toLowerCase().indexOf(q) !== -1) {
                searchState.list.push(r.v);
            }
        });
    }
    function updateSearchCount() {
        if (!big) return;
        var n = searchState.list.length;
        big.count.textContent = !searchState.q.trim() ? ""
            : n === 0 ? "0" : ((searchState.i + 1) || 1) + "/" + n;
    }

    function updateZRow() {
        var zid = viewedZone();
        if (!big || zid == null) return;
        var zList = zones[zid].layout.zList;
        H.fill(big.zRow, zList.length > 1 ? zList.map(function (z) {
            return H.el("button", {
                type: "button",
                class: "map-btn" + (z === bigView.z ? " active" : ""),
                text: z > 0 ? "+" + z : String(z),
                title: z === 0 ? "Ground level" : (z > 0 ? "Level +" + z : "Level " + z),
                onclick: function () { bigView.z = z; updateZRow(); redrawBig(); }
            });
        }) : []);
    }
    function updateZoneLabel() {
        if (!big) return;
        var zid = viewedZone();
        big.zoneLabel.textContent = zid != null && zones[zid] ? zones[zid].name : "";
        var off = cur.zone != null && zid != null && zid !== cur.zone;
        big.zoneLabel.classList.toggle("offzone", off);
    }

    function renderOverlay() {
        var panel = document.getElementById("panel-map");
        if (!panel || !H) return;
        if (!big) buildBig();
        if (big.root.parentNode !== panel) {
            panel.textContent = "";
            panel.appendChild(big.root);
        }
        if (pendingFocusView) applyFocus();
        else if (bigView.follow) centerOnMe();
        bigZoneShown = viewedZone();
        updateZoneLabel();
        updateZRow();
        updateMeButton();
        rebuildSearch();
        updateSearchCount();
        requestAnimationFrame(redrawBig);
    }

    function redrawBig() {
        var zid = viewedZone();
        if (!bigOpen() || zid == null) return;
        drawMap(big.canvas, zid, bigView, {
            curVnum: cur.vnum, unseen: cur.unseen,
            pathVnums: walkPathVnums(), pathEdges: walkPathEdges(),
            searchVnum: searchState.i >= 0 ? searchState.list[searchState.i] : null
        });
    }

    // Room menu (tap/click a room on either surface). `zoneId` is the zone
    // the tapped room belongs to — the minimap passes cur.zone, the big map
    // passes viewedZone() (which may be an adjacent zone).
    function mapRoomMenu(zoneId, v, anchor) {
        var zone = zones[zoneId];
        if (!zone) return;
        var fs = fogSet(zoneId);
        var room = zone.layout.byVnum[v];
        var name = fs[v] && room ? H.stripColor(room.n) : "Unexplored";
        var acts = [];
        if (v === cur.vnum) {
            acts.push({ label: "You are here", fn: function () {}, keep: true });
        } else if (cur.vnum != null && !cur.unseen) {
            var steps = findPath(cur.vnum, v);
            if (steps) {
                acts.push({
                    label: "Walk here (" + steps.length + " step" +
                        (steps.length === 1 ? "" : "s") + ")",
                    fn: function () { startWalk(steps); }
                });
                acts.push({
                    label: "Show path",
                    fn: function () { setShownPath(steps); }, keep: true
                });
            }
        }
        // Cross-zone jumps: one entry per adjacent zone this room borders.
        if (fs[v]) {
            var seenZone = {};
            (zone.layout.outFrom[v] || []).forEach(function (o) {
                if (seenZone[o.zone]) return;
                seenZone[o.zone] = true;
                acts.push({
                    label: "Go to " + (o.zname || "zone " + o.zone) + " →",
                    fn: (function (oo) {
                        return function () { goToZone(oo.zone, oo.t, oo.zname); };
                    })(o)
                });
            });
        }
        if (fs[v]) {
            acts.push({
                label: noteFor(v) ? "Edit note…" : "Add note…",
                fn: function () { openNoteEditor(v); }, keep: true
            });
        }
        H.openMenu(name, acts, anchor);
    }

    // ------------------------------------------------------------------
    // Room notes — popover editor; server-persisted, optimistic.
    // ------------------------------------------------------------------
    var notePop = null;   // {root, title, ta, vnum}

    function noteFor(v) {
        var zoneId = v == null ? null : vnumZone[v];
        if (zoneId == null) return "";
        var m = notes[zoneId];
        return (m && m[v]) || "";
    }
    function currentNote() { return H ? H.stripColor(noteFor(cur.vnum)) : ""; }
    function editCurrentNote() {
        if (cur.vnum != null) openNoteEditor(cur.vnum);
    }

    function buildNotePop() {
        var title = H.el("div", { class: "note-title" });
        var ta = H.el("textarea", {
            class: "note-text", rows: "5", maxlength: "2000",
            placeholder: "Notes for this room…",
            "aria-label": "Room note"
        });
        ta.addEventListener("keydown", function (ev) {
            if (ev.key === "Escape") { ev.stopPropagation(); closeNoteEditor(); }
        });
        var save = H.el("button", { type: "button", class: "map-btn note-save",
            text: "Save", onclick: function () { commitNote(notePop.vnum, ta.value); } });
        var del = H.el("button", { type: "button", class: "map-btn note-del",
            text: "Delete", onclick: function () { commitNote(notePop.vnum, ""); } });
        var close = H.el("button", { type: "button", class: "map-btn",
            text: "Close", onclick: closeNoteEditor });
        var row = H.el("div", { class: "note-actions" }, [save, del, close]);
        var root = H.el("div", { class: "map-note-pop", role: "dialog",
                                 "aria-label": "Room note" }, [title, ta, row]);
        root.hidden = true;
        document.body.appendChild(root);
        notePop = { root: root, title: title, ta: ta, del: del, vnum: null };
    }
    function openNoteEditor(v) {
        if (!notePop) buildNotePop();
        var zone = zones[vnumZone[v]];
        var room = zone && zone.layout.byVnum[v];
        notePop.vnum = v;
        notePop.title.textContent = room ? H.stripColor(room.n) : "Room note";
        notePop.ta.value = noteFor(v);
        notePop.del.hidden = !noteFor(v);
        notePop.root.hidden = false;
        notePop.ta.focus();
    }
    function closeNoteEditor() {
        if (notePop) notePop.root.hidden = true;
    }
    function commitNote(v, text) {
        text = String(text || "").trim().slice(0, 2000);
        var zoneId = v == null ? null : vnumZone[v];
        if (zoneId == null) { closeNoteEditor(); return; }
        var m = notes[zoneId] = notes[zoneId] || {};
        var prev = m[v] || "";
        if (text) m[v] = text; else delete m[v];
        closeNoteEditor();
        redraw();
        if (H) H.rerenderRoom();
        if (cfg.demo || !cfg.urls) return;
        fetch(cfg.urls.note, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": cfg.csrf
            },
            body: JSON.stringify({ vnum: v, text: text })
        }).then(function (resp) {
            if (!resp.ok) throw new Error("note " + resp.status);
        }).catch(function () {
            // Revert the optimistic write so the map tells the truth.
            if (prev) m[v] = prev; else delete m[v];
            redraw();
            if (H) H.rerenderRoom();
        });
    }

    // ------------------------------------------------------------------
    // Navigation: pathfinding over the DISCOVERED graph, show-path, and
    // the autowalk engine (one confirmed step at a time, abort on any
    // surprise — the player's own commands always win).
    // ------------------------------------------------------------------
    var walk = null;        // {steps, i, timer, label} while autowalking
    var shownPath = null;   // {steps, label} for show-path (no execution)
    var walkChip = null;    // {root, label} cancel chip above the hotbar
    var chipNoteTimer = null;

    var STEP_PAUSE_MS = 250;   // between confirmed steps (server pacing)
    var STEP_TIMEOUT_MS = 5000;

    // Zone-agnostic discovery/frontier tests, so pathfinding can reason
    // about rooms in any loaded zone (a cross-zone destination lives in a
    // different fog set than the one the player is standing in).
    function isSeen(v) {
        var z = vnumZone[v];
        return z != null && !!fogSet(z)[v];
    }
    function isFrontierGlobal(v) {
        var z = vnumZone[v];
        return z != null && !!frontier(z)[v];
    }
    // Every directed exit leaving `v`: in-zone edges plus cross-zone exits
    // (which carry the player across a zone boundary in one step).
    function neighborsOf(v) {
        var z = vnumZone[v];
        if (z == null || !zones[z]) return [];
        var L = zones[z].layout;
        var list = L.exitsFrom[v] || [];
        var cross = L.outFrom[v];
        if (cross && cross.length) {
            list = list.concat(cross.map(function (o) {
                return { t: o.t, d: o.d };
            }));
        }
        return list;
    }

    // BFS shortest path from `from` to `to` over directed exits whose
    // SOURCE is discovered; an undiscovered frontier room is admissible
    // only as the destination. Spans zones via cross-zone exits, so the
    // walker can be routed into an adjacent zone. Deterministic
    // (exitsFrom is pre-sorted; cross exits append in server order).
    function findPath(from, to) {
        if (from == null || to == null || from === to) return null;
        if (!isSeen(from)) return null;
        if (!isSeen(to) && !isFrontierGlobal(to)) return null;
        var prev = {};
        prev[from] = null;
        var queue = [from], head = 0;
        while (head < queue.length) {
            var v = queue[head++];
            if (v === to) break;
            if (!isSeen(v)) continue;   // frontier rooms are terminal
            var outs = neighborsOf(v);
            for (var i = 0; i < outs.length; i++) {
                var t = outs[i].t;
                if (prev[t] !== undefined) continue;
                if (t !== to && !isSeen(t) && !isFrontierGlobal(t)) continue;
                prev[t] = { v: v, d: outs[i].d };
                queue.push(t);
            }
        }
        if (prev[to] === undefined) return null;
        var steps = [];
        var node = to;
        while (prev[node]) {
            steps.unshift({ cmd: stepCmd(prev[node].d), expect: node, from: prev[node].v });
            node = prev[node].v;
        }
        return steps.length ? steps : null;
    }
    function pathLabel(steps) {
        return steps.map(function (s) { return s.cmd; }).join(" · ");
    }

    // --- the cancel chip (above the hotbar; the whole chip cancels) ---
    function buildChip() {
        var label = H.el("span", { class: "walk-label" });
        var root = H.el("button", {
            type: "button", class: "map-walk", onclick: function () {
                if (walk) cancelWalk("cancelled");
                else hideChip();
            }
        }, [label]);
        root.hidden = true;
        var center = document.getElementById("hud-center");
        var actionrow = document.getElementById("hud-actionrow");
        if (center && actionrow) center.insertBefore(root, actionrow);
        else document.body.appendChild(root);
        walkChip = { root: root, label: label };
    }
    function chipSay(text, transientMs) {
        if (!walkChip) buildChip();
        clearTimeout(chipNoteTimer);
        chipNoteTimer = null;
        walkChip.label.textContent = text;
        walkChip.root.hidden = false;
        if (transientMs) {
            chipNoteTimer = setTimeout(hideChip, transientMs);
        }
    }
    function hideChip() {
        clearTimeout(chipNoteTimer);
        chipNoteTimer = null;
        if (walkChip) walkChip.root.hidden = true;
    }
    function updateChip() {
        if (!walk) { hideChip(); return; }
        var step = Math.min(walk.i + 1, walk.steps.length);
        chipSay("Walking… " + step + "/" + walk.steps.length + " — tap to cancel");
    }

    // --- the engine ---
    function startWalk(steps) {
        cancelWalk("replaced");
        shownPath = null;
        walk = { steps: steps, i: 0, timer: null };
        sendStep();
        redraw();
        updateFoot();
    }
    function sendStep() {
        if (!walk) return;
        if (cur.unseen) { cancelWalk("you cannot see"); return; }
        if (H.inCombat()) { cancelWalk("combat"); return; }
        if (!H.connected() && !cfg.demo) { cancelWalk("disconnected"); return; }
        var st = walk.steps[walk.i];
        H.send(st.cmd);
        walk.timer = setTimeout(function () { cancelWalk("no response"); }, STEP_TIMEOUT_MS);
        updateChip();
    }
    // Called from enterZone on every sighted Room.Info.
    function walkOnRoom(vnum) {
        if (!walk) return;
        var st = walk.steps[walk.i];
        if (vnum === st.expect) {
            clearTimeout(walk.timer);
            walk.timer = null;
            walk.i++;
            if (walk.i >= walk.steps.length) {
                walk = null;
                chipSay("Arrived.", 2000);
                updateFoot();
                return;
            }
            walk.timer = setTimeout(sendStep, STEP_PAUSE_MS);
            updateChip();
        } else if (vnum !== st.from) {
            // Somewhere unexpected: a follow, a portal, the player's own
            // command. Their reality wins; stop quietly.
            cancelWalk("off route");
        }
    }
    function cancelWalk(reason) {
        if (!walk) return;
        clearTimeout(walk.timer);
        walk = null;
        if (reason && reason !== "replaced" && reason !== "reset") {
            chipSay("Walk stopped: " + reason, 3000);
        } else {
            hideChip();
        }
        updateFoot();
        redraw();
    }

    // Show-path: highlight without walking; listed in the overlay footer.
    function setShownPath(steps) {
        shownPath = steps ? { steps: steps } : null;
        updateFoot();
        redraw();
    }
    // Called on every sighted room: a shown path resolves (clears) once the
    // player reaches its destination, and trims the leg already walked so the
    // highlight shrinks as they follow it. Wandering off it leaves it intact.
    function shownPathOnRoom(vnum) {
        if (!shownPath || !shownPath.steps.length) return;
        var steps = shownPath.steps;
        if (vnum === steps[steps.length - 1].expect) {
            setShownPath(null);   // arrived — the route is resolved
            return;
        }
        for (var i = 0; i < steps.length; i++) {
            if (steps[i].from === vnum) {
                if (i > 0) { shownPath = { steps: steps.slice(i) }; updateFoot(); }
                return;
            }
        }
    }

    function activePath() { return walk || shownPath; }
    function walkPathVnums() {
        var p = activePath();
        if (!p) return null;
        var s = {};
        p.steps.forEach(function (st) { s[st.from] = true; s[st.expect] = true; });
        return s;
    }
    function walkPathEdges() {
        var p = activePath();
        if (!p) return null;
        var m = {};
        p.steps.forEach(function (st) {
            m[st.from + "|" + st.expect] = true;
            m[st.expect + "|" + st.from] = true;
        });
        return m;
    }

    function updateFoot() {
        if (!big) return;
        if (walk) {
            H.fill(big.foot, [H.el("span", { class: "dim",
                text: "Walking… " + walk.i + "/" + walk.steps.length })]);
        } else if (shownPath) {
            H.fill(big.foot, [
                H.el("span", { text: pathLabel(shownPath.steps) + "  (" +
                    shownPath.steps.length + " step" +
                    (shownPath.steps.length === 1 ? "" : "s") + ")" }),
                H.el("button", { type: "button", class: "map-btn",
                    text: "Clear", onclick: function () { setShownPath(null); } })
            ]);
        } else {
            H.fill(big.foot, []);
        }
        big.foot.hidden = !walk && !shownPath;
    }

    // Player input beats automation: Enter in the command line or Esc
    // anywhere cancels an active walk (capture phase so the overlay's own
    // Esc handling still runs afterwards only when no walk was active).
    function wireWalkCancels() {
        document.addEventListener("keydown", function (ev) {
            if (ev.key === "Escape" && walk) {
                ev.stopImmediatePropagation();
                cancelWalk("cancelled");
            }
        }, true);
        var input = document.getElementById("command-input");
        if (input) input.addEventListener("keydown", function (ev) {
            if (ev.key === "Enter" && walk && input.value.trim()) {
                cancelWalk("your command");
            }
        });
    }

    function redraw() {
        redrawMini();
        if (!bigOpen()) return;
        if (bigView.follow) centerOnMe();
        // Following the player across a zone border rebuilds the per-zone
        // chrome (z-levels, search index) exactly once, not every frame.
        var zid = viewedZone();
        if (zid !== bigZoneShown) {
            bigZoneShown = zid;
            updateZRow();
            rebuildSearch();
            updateSearchCount();
        }
        updateZoneLabel();
        updateMeButton();
        redrawBig();
    }

    // ------------------------------------------------------------------
    // Demo fixture (/connect?demo=1) — a hand-authored zone matching the
    // hud.js demo Room.Info (room 3001, "Ishar Nexus") and exercising the
    // full geometry vocabulary: the n→e→s→w collision quad, a stretch, a
    // bent edge, portals, one-way, doors, u/d levels, a cross-zone stub.
    // ------------------------------------------------------------------
    function demoGraph() {
        var rooms = [
            { v: 3001, n: "The Grand Concourse", t: "City" },
            { v: 3002, n: "Northern Promenade", t: "City" },
            { v: 3005, n: "Eastern Arcade", t: "City" },
            { v: 3008, n: "Southern Steps", t: "City", f: ["peaceful"] },
            { v: 3010, n: "Western Gate", t: "City" },
            { v: 3100, n: "Skywalk Balcony", t: "Indoor" },
            { v: 3101, n: "Bell Tower", t: "Indoor" },
            { v: 3200, n: "Nexus Undercroft", t: "Indoor" },
            { v: 3201, n: "Flooded Cistern", t: "Underwater", f: ["death"] },
            { v: 3500, n: "Heart of the Fountain", t: "Shallow Water" },
            // Collision quad: 3002 n→3011 e→3012 s→3013 w→3014 ≠ 3002.
            { v: 3011, n: "Colonnade North", t: "City" },
            { v: 3012, n: "Colonnade Corner", t: "City" },
            { v: 3013, n: "Colonnade South", t: "City" },
            { v: 3014, n: "Cramped Alcove", t: "Indoor" },
            // Stretch victim east of the arcade.
            { v: 3006, n: "Gilded Row", t: "City" },
            { v: 3007, n: "Silk Bazaar", t: "City" },
            // One-way ledge chain off the south steps.
            { v: 3020, n: "Crumbled Ledge", t: "Hill" },
            { v: 3021, n: "Rubble Slope", t: "Hill" },
            // Forest fringe west, with a door.
            { v: 3030, n: "Verge of the Wood", t: "Forest" },
            { v: 3031, n: "Warded Grove", t: "Forest" }
        ];
        var exits = [
            { f: 3001, d: "n", t: 3002 }, { f: 3002, d: "s", t: 3001 },
            { f: 3001, d: "e", t: 3005 }, { f: 3005, d: "w", t: 3001 },
            { f: 3001, d: "s", t: 3008 }, { f: 3008, d: "n", t: 3001 },
            { f: 3001, d: "w", t: 3010 }, { f: 3010, d: "e", t: 3001 },
            { f: 3001, d: "u", t: 3100 }, { f: 3100, d: "d", t: 3001 },
            { f: 3001, d: "d", t: 3200 }, { f: 3200, d: "u", t: 3001 },
            { f: 3001, d: "Into the Fountain", t: 3500 },
            { f: 3500, d: "out", t: 3001 },
            // Collision quad (3014's ideal cell is 3002's — stretches west).
            { f: 3002, d: "n", t: 3011 }, { f: 3011, d: "s", t: 3002 },
            { f: 3011, d: "e", t: 3012 }, { f: 3012, d: "w", t: 3011 },
            { f: 3012, d: "s", t: 3013 }, { f: 3013, d: "n", t: 3012 },
            { f: 3013, d: "w", t: 3014 }, { f: 3014, d: "e", t: 3013 },
            // A bent edge: the gate claims an "east" exit to Colonnade North
            // even though it sits two rows south of it — geometrically
            // contradictory once both are placed, so it draws as a dogleg.
            // (Both rooms are already placed by the time this edge is
            // classified, so it cannot disturb the BFS placement.)
            { f: 3010, d: "e", t: 3011 }, { f: 3011, d: "w", t: 3010 },
            // Stretch pair east with a locked door.
            { f: 3005, d: "e", t: 3006, door: 1 },
            { f: 3006, d: "w", t: 3005, door: 1 },
            { f: 3006, d: "e", t: 3007, door: 1, locked: 1 },
            { f: 3007, d: "w", t: 3006, door: 1, locked: 1 },
            // One-way drop chain (no return exits).
            { f: 3008, d: "s", t: 3020, one: 1 },
            { f: 3020, d: "s", t: 3021, one: 1 },
            { f: 3021, d: "climb", t: 3008 },
            // Forest with a door.
            { f: 3010, d: "w", t: 3030, door: 1 },
            { f: 3030, d: "e", t: 3010, door: 1 },
            { f: 3030, d: "nw", t: 3031 }, { f: 3031, d: "se", t: 3030 },
            // Upper level.
            { f: 3100, d: "n", t: 3101 }, { f: 3101, d: "s", t: 3100 },
            // Undercroft.
            { f: 3200, d: "e", t: 3201, one: 1 }
        ];
        var out = [
            { f: 3030, d: "w", t: 5001, zone: 91, zname: "Kingdom of Jolnara" }
        ];
        return {
            zone: { id: 90, name: "Ishar Nexus" },
            rooms: rooms, exits: exits, out: out
        };
    }
    // A second, adjacent demo zone reached by the forest's west stub, so
    // cross-zone refocus ("Go to Kingdom of Jolnara →") and a cross-zone
    // walk (3001 → 5003, over the 3030→5001 border) are both demoable.
    function demoGraph2() {
        var rooms = [
            { v: 5001, n: "Jolnaran Border Post", t: "Field" },
            { v: 5002, n: "Dusty Cart Track", t: "Field" },
            { v: 5003, n: "Village Square", t: "City" },
            { v: 5004, n: "Herbalist's Hut", t: "Indoor" },
            { v: 5005, n: "Wildflower Meadow", t: "Field" }
        ];
        var exits = [
            { f: 5001, d: "w", t: 5002 }, { f: 5002, d: "e", t: 5001 },
            { f: 5002, d: "w", t: 5003 }, { f: 5003, d: "e", t: 5002 },
            { f: 5003, d: "n", t: 5004 }, { f: 5004, d: "s", t: 5003 },
            { f: 5003, d: "s", t: 5005 }, { f: 5005, d: "n", t: 5003 }
        ];
        var out = [
            { f: 5001, d: "e", t: 3030, zone: 90, zname: "Ishar Nexus" }
        ];
        return {
            zone: { id: 91, name: "Kingdom of Jolnara" },
            rooms: rooms, exits: exits, out: out
        };
    }
    function seedDemo() {
        cfg.demo = true;
        registerGraph(demoGraph());
        registerGraph(demoGraph2());
        // ~60% explored: the plaza + east + the quad + the forest verge (the
        // border room), not the underlevels/grove.
        var seen = [3001, 3002, 3005, 3006, 3008, 3010, 3011, 3012, 3013,
                    3014, 3100, 3500, 3020, 3030];
        var fs = fogSet(90);
        seen.forEach(function (v) { fs[v] = true; });
        // The near end of the neighbor is explored; its far rooms stay fog.
        var seen2 = [5001, 5002, 5003];
        var fs2 = fogSet(91);
        seen2.forEach(function (v) { fs2[v] = true; });
        notes[90] = {
            3005: "Hadeon buys curios here",
            3014: "stash spot — check after reboot"
        };
        notes[91] = { 5003: "rare reagents restock at dawn" };
        fogStamp++;
    }

    // ------------------------------------------------------------------
    // Public surface
    // ------------------------------------------------------------------
    var mod = {
        attach: function (ctx) { H = ctx; },
        enabled: enabled,
        onRoom: onRoom,
        onReset: onReset,
        onConnected: onConnected,
        renderMini: renderMini,
        renderOverlay: renderOverlay,
        currentNote: currentNote,
        editCurrentNote: editCurrentNote
    };

    window.IsharMap = {
        init: function (opts) {
            opts = opts || {};
            cfg.authed = !!opts.authenticated;
            cfg.csrf = String(opts.csrf || "");
            if (opts.urls && typeof opts.urls === "object") cfg.urls = opts.urls;
            if (/[?&]demo=1/.test(window.location.search)) seedDemo();
            // Discovery must not be lost to a tab close mid-batch.
            window.addEventListener("pagehide", function () { doFlush(true); });
            wireWalkCancels();
            if (H) { H.updateMicro(); H.rerenderRoom(); }
        },
        // Verification hooks (the repo's headless-Chromium harness asserts
        // layout determinism and fog behavior through these). Not API.
        debug: {
            layoutZone: layoutZone,
            zones: zones,
            fog: fog,
            notes: notes,
            cur: cur,
            demoGraph: demoGraph,
            demoGraph2: demoGraph2,
            seedDemo: seedDemo,
            findPath: findPath,
            onRoom: onRoom,
            setShownPath: setShownPath,
            shownPath: function () { return shownPath; },
            viewedZone: viewedZone,
            focusZone: focusZone,
            openZoneJump: openZoneJump,
            walking: function () { return !!walk; }
        }
    };

    if (window.IsharHUD && window.IsharHUD.registerMap) {
        window.IsharHUD.registerMap(mod);
    }
})();
