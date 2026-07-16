/*
 * Ishar browser-client HUD.
 *
 * A small vanilla state store fed by GMCP messages (forwarded by the telnet
 * bridge on the "\x00GMCP <Package.Message> {json}" channel) that renders a
 * heads-up display around the xterm terminal. It consumes the same GMCP feeds
 * the Mudlet package does, but leans on the browser to go past what Lua/Geyser
 * can offer: touch-first context menus, a scroll-bounded Abilities browser (so
 * an immortal's 400-skill list can't bury the screen), a room-Occupants panel
 * with click-to-attack and default hostile/beneficial targets that make the
 * hotbar target-aware, collapsible panels, and a translucent tap-to-move
 * compass rose on phones.
 *
 * All player actions remain plain-text commands sent over the existing
 * WebSocket — the game server ignores inbound GMCP — so widgets only ever call
 * api.send()/api.prefill(). The terminal stream is never touched here.
 *
 * XSS discipline: every data-derived node is built with createElement +
 * textContent (the el() helper). No innerHTML anywhere in this file.
 *
 * Public surface (window.IsharHUD):
 *   init({ send, prefill, onLayoutChange, onComm })  wire to the connect page
 *   onGmcp(name, jsonBody)                            feed a GMCP message
 *   reset()                                           clear state on (re)connect
 *   setConnected(bool) / completions() / demo()
 */
(function () {
    "use strict";

    var CHAT_MAX = 200;
    var QUICKBAR_MAX = 12;   // backfill target for the auto quick-bar
    var FAV_CAP = 30;        // ceiling on pinned favorites shown in the quick-bar
    // (the bar is single-row horizontal-scroll, so it never grows vertically)

    // ------------------------------------------------------------------
    // State
    // ------------------------------------------------------------------
    var S = {
        vitals: null, status: null, time: null, room: null,
        equipment: [], inventory: null, train: null,
        affects: null, group: null, who: null, occupants: [],
        skills: [], cooldownExpiry: {}, usable: {},
        chat: [], connected: false,
        // Default targets (from Room.Occupants) that make the hotbar
        // target-aware: offensive spells → hostile, defensive → beneficial.
        tgtHostile: null, tgtFriendly: null
    };

    // Persisted client prefs (localStorage): pinned abilities + collapsed
    // panels + Abilities-browser filters.
    var favorites = loadSet("ishar.favs");
    var collapsed = loadSet("ishar.collapsed");
    var abilityFilter = { q: "", type: "all", usableOnly: false };
    try {
        var af = JSON.parse(localStorage.getItem("ishar.abilityFilter"));
        if (af && typeof af === "object") {
            if (typeof af.type === "string") abilityFilter.type = af.type;
            if (typeof af.usableOnly === "boolean") abilityFilter.usableOnly = af.usableOnly;
        }
    } catch (e) {}

    var api = { send: function () {}, prefill: function () {}, onLayoutChange: function () {}, onComm: function () {} };
    var dom = {};
    var hudOn = false;
    var activeTab = "status";
    var sheetName = null;
    var roseOverlayOn = true;

    // Phone layout = dock + bottom sheet; desktop = columns + tabs.
    var mqMobile = window.matchMedia("(max-width: 767.98px)");
    var mqWide = window.matchMedia("(min-width: 1200px)");

    // Panel homes for desktop; sheet order for phones (matches the dock).
    // The compass rose (room) is pinned to the bottom of the left column, so
    // its desktop home is #hud-left itself (a flex footer) while the scrolling
    // panels live in #hud-left-scroll (placePanels re-homes them in THIS order).
    // Occupants sits last in the scroll — directly above the pinned rose — so
    // the movement (rose) and interaction (occupants) surfaces are together at
    // the bottom, nearest the input.
    var PANELS = ["equipment", "inventory", "train", "group", "occupants", "room",
                  "status", "abilities", "chat", "who"];
    var PANEL_HOME = {
        occupants: "hud-left-scroll", equipment: "hud-left-scroll",
        inventory: "hud-left-scroll", train: "hud-left-scroll",
        group: "hud-left-scroll",
        room: "hud-left",
        status: "hud-right", abilities: "hud-right", chat: "hud-right", who: "hud-right"
    };

    // Position capability ranking (index = capability), from the game's
    // posn_names[] (constants.c). Higher rank = more capable; a skill whose
    // min_position outranks the player's current position is greyed.
    var POS_RANK = {
        dead: 0, mortal: 1, stunned: 2, paralyzed: 3, sleeping: 4,
        grappled: 5, resting: 6, sitting: 7, riding: 8, standing: 10,
        fighting: 10   // upright in combat: treat as Standing
    };
    function posRank(name) {
        var r = POS_RANK[String(name || "").toLowerCase()];
        return r == null ? 10 : r;   // unknown → lenient (server re-validates)
    }

    // Item type → "use" verb (mirrors the Mudlet itemVerb table). A null verb
    // means the type has no primary use action (only examine/drop).
    var TYPE_VERB = {
        potion: "quaff", scroll: "recite", food: "eat", drink: "drink",
        weapon: "wield", armor: "wear", wand: "use", staff: "use", light: "hold"
    };
    var TYPE_VERB_LABEL = {
        quaff: "Quaff", recite: "Recite", eat: "Eat", drink: "Drink",
        wield: "Wield", wear: "Wear", use: "Use", hold: "Hold"
    };

    // ------------------------------------------------------------------
    // Helpers
    // ------------------------------------------------------------------
    function loadSet(key) {
        var s = {};
        try {
            var arr = JSON.parse(localStorage.getItem(key));
            if (Array.isArray(arr)) arr.forEach(function (k) { if (typeof k === "string") s[k] = true; });
        } catch (e) {}
        return s;
    }
    function saveSet(key, s) {
        try { localStorage.setItem(key, JSON.stringify(Object.keys(s))); } catch (e) {}
    }

    // DOM builder — the ONLY way data-derived nodes are created here. Values
    // reach the DOM as text/attributes, never parsed as markup.
    function el(tag, attrs, kids) {
        var n = document.createElement(tag);
        if (attrs) Object.keys(attrs).forEach(function (k) {
            var v = attrs[k];
            if (v == null || v === false) return;
            if (k === "class") n.className = v;
            else if (k === "text") n.textContent = v;
            else if (k.indexOf("on") === 0 && typeof v === "function") n.addEventListener(k.slice(2), v);
            else n.setAttribute(k, v === true ? "" : v);
        });
        if (kids != null) {
            if (!Array.isArray(kids)) kids = [kids];
            kids.forEach(function (c) {
                if (c == null || c === false) return;
                n.appendChild(typeof c === "object" ? c : document.createTextNode(String(c)));
            });
        }
        return n;
    }
    // Replace a container's children with new nodes in one shot.
    function fill(container, kids) {
        while (container.firstChild) container.removeChild(container.firstChild);
        if (kids == null) return;
        if (!Array.isArray(kids)) kids = [kids];
        kids.forEach(function (c) { if (c != null && c !== false) container.appendChild(c); });
    }

    // Strip Ishar "@x" color codes for plain HUD panels. @@ is a literal @.
    function stripColor(s) {
        if (s == null) return "";
        return String(s).replace(/@@/g, "\x00").replace(/@./g, "").replace(/\x00/g, "@");
    }
    function clamp(n, a, b) { n = Number(n) || 0; return Math.max(a, Math.min(b, n)); }
    function pct(cur, max) { max = Number(max) || 0; if (max <= 0) return 0; return clamp(Math.round((Number(cur) || 0) / max * 100), 0, 100); }
    function now() { return Date.now() / 1000; }

    function fmtDur(s) {
        if (s == null) return "";
        s = Math.floor(Number(s));
        if (s <= 0) return "—";
        if (s >= 86400) return "∞";
        if (s < 60) return s + "s";
        var m = Math.floor(s / 60), ss = s % 60;
        if (m < 60) return m + "m" + (ss < 10 ? "0" : "") + ss;
        var h = Math.floor(m / 60); m = m % 60;
        return h + "h" + (m < 10 ? "0" : "") + m;
    }

    // Build a dotted keyword target ("leather cap" -> "leather.cap"), the
    // conjunction syntax the game accepts for examine/wear/get/etc.
    function targetOf(kw) {
        if (!kw) return "";
        return String(kw).toLowerCase().split(/\s+/)
            .map(function (w) { return w.replace(/[^a-z0-9]/g, ""); })
            .filter(Boolean).join(".");
    }
    // First keyword token only (for follow/group/tell, which take a bare name).
    function firstWord(kw) {
        var t = String(kw || "").trim().split(/\s+/)[0] || "";
        return t.replace(/[^A-Za-z0-9]/g, "");
    }
    function nameOf(n) { return n == null ? "" : String(n).replace(/[\r\n']/g, "").trim(); }

    function safeCmd(c) {
        if (c == null) return "";
        // Strip the whole C0 range + DEL (not just newlines): a game-controlled
        // field (mob keyword, handle, skill name) could otherwise carry an ESC
        // that the terminal echo would interpret as an escape sequence.
        return String(c).replace(/[\x00-\x1f\x7f]/g, " ").replace(/\s+/g, " ").trim().slice(0, 200);
    }

    function dirLabel(d) {
        return { n: "N", s: "S", e: "E", w: "W", ne: "NE", nw: "NW", se: "SE", sw: "SW" }[d] || String(d);
    }

    // Moons: per-moon colour (matching the game's @c tints) + an illumination
    // glyph by phase. Ready for a richer Game.Time.moons feed
    // ({name, phase 0-7, phase_name, up}); degrades to a plain glyph for the
    // current name-only payload.
    var MOON_COLOR = { shavar: "#cfd6e6", tregalien: "#e8c14b", fandaro: "#6fce7a", chenchir: "#d05a5a" };
    var MOON_GLYPH = ["○", "◔", "◑", "◕", "●", "◕", "◑", "◔"];   // new → waning crescent
    function moonColor(m) {
        var key = String(m.name || "").toLowerCase().replace(/[^a-z].*$/, "");
        return MOON_COLOR[key] || "var(--hud-moon)";
    }
    function moonGlyph(m) {
        return (typeof m.phase === "number" && m.phase >= 0 && m.phase <= 7) ? MOON_GLYPH[m.phase] : "☽";
    }

    function completions() {
        var out = [];
        function add(w) { if (w) out.push(String(w)); }
        function addKeywords(it) {
            if (!it) return;
            String(it.keywords || "").split(/\s+/).forEach(add);
            (it.contents || []).forEach(addKeywords);
        }
        if (S.room && S.room.exits) Object.keys(S.room.exits).forEach(add);
        (S.skills || []).forEach(function (s) { add(nameOf(s.name)); });
        if (S.who && S.who.players) S.who.players.forEach(function (p) { add(stripColor(p.name)); });
        (S.occupants || []).forEach(function (o) { add(o.keyword); });
        (S.equipment || []).forEach(addKeywords);
        if (S.inventory) {
            (S.inventory.items || []).forEach(addKeywords);
            (S.inventory.components || []).forEach(addKeywords);
        }
        return out;
    }

    // ------------------------------------------------------------------
    // GMCP dispatch
    // ------------------------------------------------------------------
    function onGmcp(name, body) {
        var data = null;
        if (body) {
            try { data = JSON.parse(body); } catch (e) { return; }
        }
        switch (name) {
            case "Char.Vitals":
                if (body === lastVitalsBody) break;
                lastVitalsBody = body;
                S.vitals = data;
                updateVitals();
                tickHotbar();          // mana gate re-evaluates each pulse
                // The Abilities browser bakes the mana/position block state into
                // each row, so it must rebuild when mana changes (combat regen)
                // or a spell stays greyed after you can afford it (issue #1801).
                // Only when it's actually on screen — same guard the cooldown
                // path uses to avoid rebuilding a ~400-row list off-screen.
                if (abilitiesVisible()) renderAbilities();
                break;
            case "Char.Status": S.status = data; renderVitals(); renderStatus(); break;
            case "Game.Time": S.time = data; renderVitals(); break;
            case "Room.Info": S.room = data; renderRoom(); break;
            case "Room.Occupants": applyOccupants(data); break;
            case "Char.Equipment": S.equipment = (data && data.items) || []; renderEquipment(); renderInventory(); break;
            case "Char.Inventory": S.inventory = data; renderInventory(); renderEquipment(); break;
            case "Char.Train": S.train = data; renderTrain(); break;
            case "Char.Affects": S.affects = data; stampAffectExpiry(data); renderStatus(); break;
            case "Group.Update": S.group = data; renderGroup(); break;
            case "Char.Who": S.who = data; renderWho(); break;
            case "Char.Skills": S.skills = (data && data.skills) || []; renderHotbar(); renderAbilities(); break;
            case "Char.Cooldowns":
                applyCooldowns(data); tickHotbar();
                // The Abilities browser can be ~400 rows; only rebuild it for a
                // cooldown tick when it's actually on screen.
                if (abilitiesVisible()) renderAbilities();
                break;
            case "Comm.Channel": {
                var entry = pushChat(data);
                if (entry) {
                    appendChat(entry);
                    if (!chatVisible()) markChatUnread(true);
                    api.onComm(entry.channel, entry.text);
                }
                break;
            }
            default: break;
        }
    }

    function applyCooldowns(data) {
        S.cooldownExpiry = {};
        S.usable = (data && data.usable) || {};
        var list = (data && data.cooldowns) || [];
        var t = now();
        for (var i = 0; i < list.length; i++) {
            S.cooldownExpiry[list[i].id] = t + (Number(list[i].remaining) || 0);
        }
    }

    // Stamp each affect's absolute expiry once, when the feed arrives.
    function stampAffectExpiry(a) {
        if (!a) return;
        var t = now();
        ["buffs", "maintained", "debuffs"].forEach(function (k) {
            (a[k] || []).forEach(function (x) { x._expiry = t + (Number(x.duration) || 0); });
        });
    }

    function pushChat(d) {
        if (!d) return null;
        var entry = { channel: d.channel || "", text: stripColor(d.text || "") };
        S.chat.push(entry);
        if (S.chat.length > CHAT_MAX) S.chat.shift();
        return entry;
    }

    // ------------------------------------------------------------------
    // Vitals (hot path — kept in-place, unchanged behaviour)
    // ------------------------------------------------------------------
    var lastVitalsBody = null;
    var vitalsCache = null;

    function vitalsShape(v) {
        return (v && v.opponent_hp_pct != null ? "t" : "")
            + (v && v.metamagic != null ? "m" : "")
            + (v && v.edge != null ? "e" : "");
    }
    function cacheVitalsRefs() {
        vitalsCache = { shape: vitalsShape(S.vitals), bars: {} };
        ["hp", "mp", "mv", "tgt", "mm", "edge"].forEach(function (cls) {
            var e = dom.vitals.querySelector(".vbar." + cls);
            if (e) vitalsCache.bars[cls] = { fill: e.querySelector(".vbar-fill"), text: e.querySelector(".vbar-text") };
        });
    }
    function updateVitals() {
        var v = S.vitals;
        if (!vitalsCache || vitalsCache.shape !== vitalsShape(v)) { renderVitals(); return; }
        var bars = vitalsCache.bars;
        function upd(cls, cur, max) {
            var n = bars[cls];
            if (!n || !n.fill || !n.text) return;
            var has = cur !== null && cur !== undefined;
            n.fill.style.width = (has ? pct(cur, max) : 0) + "%";
            n.text.textContent = has ? cur + " / " + max : "—";
        }
        upd("hp", v ? v.hp : null, v ? v.maxhp : 0);
        upd("mp", v ? v.mp : null, v ? v.maxmp : 0);
        upd("mv", v ? v.move : null, v ? v.maxmove : 0);
        if (bars.tgt && bars.tgt.fill) {
            bars.tgt.fill.style.width = clamp(v.opponent_hp_pct, 0, 100) + "%";
            bars.tgt.text.textContent = v.opponent_hp_pct + "%";
        }
        upd("mm", v && v.metamagic != null ? v.metamagic : null, v ? v.metamagic_max : 0);
        upd("edge", v && v.edge != null ? v.edge : null, v ? v.edge_max : 0);
    }
    function vbar(label, cur, max, cls) {
        var has = cur !== null && cur !== undefined;
        return el("div", { class: "vbar " + cls }, [
            el("span", { class: "vbar-label", text: label }),
            el("span", { class: "vbar-track" }, [
                el("span", { class: "vbar-fill", style: "width:" + (has ? pct(cur, max) : 0) + "%" }),
                el("span", { class: "vbar-text", text: has ? cur + " / " + max : "—" })
            ])
        ]);
    }
    function renderVitals() {
        var v = S.vitals, st = S.status, tm = S.time;
        var name = st ? String(st.name) : "—";
        var sub = st ? ("L" + st.level + " " + st.race + " " + st["class"])
                     : (S.connected ? "awaiting character data" : "not connected");

        var barKids = [vbar("HP", v ? v.hp : null, v ? v.maxhp : 0, "hp"),
                       vbar("MP", v ? v.mp : null, v ? v.maxmp : 0, "mp"),
                       vbar("MV", v ? v.move : null, v ? v.maxmove : 0, "mv")];
        if (v && v.opponent_hp_pct != null) {
            barKids.push(el("div", { class: "vbar tgt" }, [
                el("span", { class: "vbar-label", text: "Foe" }),
                el("span", { class: "vbar-track" }, [
                    el("span", { class: "vbar-fill", style: "width:" + clamp(v.opponent_hp_pct, 0, 100) + "%" }),
                    el("span", { class: "vbar-text", text: v.opponent_hp_pct + "%" })
                ])
            ]));
            // Target-of-target, derived from the Room.Occupants combat graph:
            // whether your foe is swinging at YOU or someone else is holding
            // it (the tank). Re-rendered by applyOccupants whenever an edge
            // changes; the cheap updateVitals path never touches it.
            var foe = null;
            for (var fi = 0; fi < (S.occupants || []).length; fi++) {
                if (S.occupants[fi].is_your_target) { foe = S.occupants[fi]; break; }
            }
            if (foe) {
                if (foe.fighting_you) {
                    barKids.push(el("span", { class: "v-foe-tgt you", title: "Your target is attacking you", text: "◎ on you" }));
                } else if (foe.fighting) {
                    var tk2 = occByHandle(foe.fighting);
                    if (tk2) {
                        var tname = tk2.is_player ? firstWord(tk2.keyword) : stripColor(tk2.short_desc || tk2.keyword);
                        barKids.push(el("span", { class: "v-foe-tgt", title: "Your target is attacking them (they tank)", text: "◎ tank: " + tname }));
                    }
                }
            }
        }
        if (v && v.metamagic != null) barKids.push(vbar("MM", v.metamagic, v.metamagic_max, "mm"));
        if (v && v.edge != null) barKids.push(vbar("Edge", v.edge, v.edge_max, "edge"));

        var groups = [
            el("div", { class: "v-group v-identity" }, [
                el("span", { class: "v-name", text: name }),
                el("span", { class: "v-sub dim", text: sub })
            ]),
            el("div", { class: "v-group v-bars" }, barKids)
        ];
        // Gold / To-level are intentionally NOT shown here — both live in the
        // Status pane, and dropping them reclaims scarce top-bar space (#1801).
        // Active default targets, so target-aware casting is legible at a glance.
        if (S.tgtHostile || S.tgtFriendly) {
            var tk = [];
            if (S.tgtHostile) tk.push(el("span", { class: "v-tgt hostile", title: "Offensive spells target this", text: "⚔ " + S.tgtHostile.desc }));
            if (S.tgtFriendly) tk.push(el("span", { class: "v-tgt friendly", title: "Beneficial spells target this", text: "✚ " + S.tgtFriendly.desc }));
            groups.push(el("div", { class: "v-group v-targets" }, tk));
        }
        var world = el("div", { class: "v-group v-world" });
        if (tm) {
            world.appendChild(el("span", { class: "v-clock", text:
                (tm.night ? "☾ " : "☀ ") + tm.hour12 + tm.ampm
                + (tm.day_name ? " · " + tm.day_name : "")
                + (tm.month_name ? ", " + tm.month_name : "")
                + (tm.year != null ? " · Yr " + tm.year : "") }));
            if (tm.season_id != null) world.appendChild(el("span", { class: "v-season", text: "Season " + tm.season_id }));
            (tm.events || []).forEach(function (e) {
                world.appendChild(el("span", { class: "v-event", title: "Global event", text: "⚑ " + e.name + (e.seconds ? " (" + fmtDur(e.seconds) + ")" : "") }));
            });
            (tm.moons || []).forEach(function (m) {
                var span = el("span", { class: "v-moon", title: "Moon" + (m.phase_name ? " — " + m.phase_name : "") }, [
                    el("span", { class: "v-moon-icon", style: "color:" + moonColor(m), text: moonGlyph(m) }),
                    " " + m.name + (m.phase_name ? " (" + m.phase_name + ")" : "")
                ]);
                world.appendChild(span);
            });
        } else {
            world.appendChild(el("span", { class: "v-clock dim", text: "☾ —" }));
        }
        groups.push(world);
        fill(dom.vitals, groups);
        cacheVitalsRefs();
    }

    // ------------------------------------------------------------------
    // Collapsible panel header
    // ------------------------------------------------------------------
    // Every side panel opens with a header that toggles its collapsed state
    // (persisted). Optional trailing action nodes sit on the header's right.
    function panelHeader(key, title, defaultCollapsed, actions) {
        if (collapsed[key] === undefined && defaultCollapsed) collapsed[key] = true;
        var isCol = !!collapsed[key];
        // The collapse control is its own button; action buttons sit beside it
        // (never nested inside — that would be invalid, reflowed markup).
        var toggle = el("button", {
            type: "button", class: "panel-h-toggle" + (isCol ? " collapsed" : ""),
            "data-collapse": key, "aria-expanded": isCol ? "false" : "true"
        }, [
            el("span", { class: "panel-caret", "aria-hidden": "true", text: isCol ? "▸" : "▾" }),
            el("span", { class: "panel-h-title", text: title })
        ]);
        var head = el("div", { class: "panel-h" }, [toggle]);
        if (actions && actions.length) head.appendChild(el("span", { class: "panel-h-actions" }, actions));
        return head;
    }
    function isCollapsed(key) { return !!collapsed[key]; }
    function bodyIf(key, node) {
        // Return the body node, or a hidden placeholder when collapsed.
        if (isCollapsed(key)) return null;
        return node;
    }

    // ------------------------------------------------------------------
    // Room / compass rose (bottom-left on desktop; translucent overlay on
    // phones). One renderer feeds both surfaces from Room.Info.exits.
    // ------------------------------------------------------------------
    var STD_DIRS = { n: 1, s: 1, e: 1, w: 1, ne: 1, nw: 1, se: 1, sw: 1, u: 1, d: 1 };
    function exitCmd(dir) {
        // Only named exits reach here (compass cells send the bare direction).
        // "go" resolves single- and multi-word custom exit names alike; a bare
        // single-word name would be misread as a command and silently fail.
        return "go " + dir;
    }
    // Every cardinal cell is always drawn — a live button when the exit exists,
    // a greyed label when it doesn't — so the click target for a direction sits
    // at a fixed spot and never moves as you travel (Mudlet-style stable rose).
    function roseGrid(exits, overlay) {
        function cell(dir) {
            if (exits[dir] == null) return el("span", { class: "exit none", text: dirLabel(dir) });
            return el("button", { class: "exit", "data-cmd": dir, title: dir + " → " + exits[dir], text: dirLabel(dir) });
        }
        return el("div", { class: "compass" + (overlay ? " overlay" : "") }, [
            cell("nw"), cell("n"), cell("ne"),
            cell("w"), el("span", { class: "exit hub", text: "◈" }), cell("e"),
            cell("sw"), cell("s"), cell("se")
        ]);
    }
    function renderRose(container, overlay) {
        var r = S.room, exits = (r && r.exits) || {};
        // Up/Down are also always drawn (greyed when absent), same stability
        // guarantee as the cardinal grid.
        var ud = ["u", "d"].map(function (dir) {
            var lbl = dir === "u" ? "↑ Up" : "↓ Down";
            if (exits[dir] != null) return el("button", { class: "exit ud", "data-cmd": dir, text: lbl });
            return el("span", { class: "exit ud none", text: lbl });
        });
        var kids = [roseGrid(exits, overlay), el("div", { class: "ud-row" }, ud)];
        if (!overlay) {
            var named = [];
            Object.keys(exits).forEach(function (k) {
                if (!STD_DIRS[k]) named.push(el("button", { class: "exit named", "data-cmd": exitCmd(k), text: k }));
            });
            // Always present (a reserved, min-height strip) so a room with named
            // exits and one without don't change the pane height and shift the
            // fixed compass on the bottom-pinned desktop layout.
            kids.push(el("div", { class: "named-row" }, named));
        }
        fill(container, kids);
    }
    function renderRoom() {
        var r = S.room;
        var head = el("div", { class: "rose-head" }, [
            el("span", { class: "rose-name", text: stripColor((r && r.name) || "Somewhere") }),
            r && r.area ? el("span", { class: "rose-area dim", text: stripColor(r.area) + (r.environment ? " · " + stripColor(r.environment) : "") }) : null
        ]);
        var body = el("div", { class: "rose-body" });
        renderRose(body, false);
        fill(dom.room, [head, body]);
        if (dom.roseOverlay) {
            renderRose(dom.roseOverlay, true);
            updateRoseOverlay();
        }
    }
    function updateRoseOverlay() {
        if (!dom.roseOverlay) return;
        var show = hudOn && roseOverlayOn && mqMobile.matches;
        dom.roseOverlay.hidden = !show;
    }

    // ------------------------------------------------------------------
    // Occupants (Room.Occupants) — the room's targetable persons.
    // ------------------------------------------------------------------
    function applyOccupants(data) {
        S.occupants = (data && data.occupants) || [];
        // Keep default targets valid: drop any that left the room; refresh
        // their display name if still present.
        ["tgtHostile", "tgtFriendly"].forEach(function (slot) {
            var t = S[slot];
            if (!t) return;
            var found = null;
            for (var i = 0; i < S.occupants.length; i++) {
                if (S.occupants[i].handle === t.handle && !S.occupants[i].is_dead) { found = S.occupants[i]; break; }
            }
            if (found) t.desc = stripColor(found.short_desc || t.desc);
            else S[slot] = null;
        });
        renderOccupants();
        renderGroup();       // member menus map onto occupant handles
        renderVitals();      // target chip + tank line live near the foe bar
        tickHotbar();        // target-aware labels
    }

    function setTarget(slot, occ) {
        // Toggle off if re-selecting the same handle.
        var cur = S[slot];
        if (cur && cur.handle === occ.handle) S[slot] = null;
        else S[slot] = { handle: occ.handle, desc: stripColor(occ.short_desc || occ.keyword) };
        renderOccupants();
        renderVitals();
        tickHotbar();
    }

    function occHostileClass(o) {
        if (o.is_dead) return "dead";
        return o.hostile_hint === "hostile" ? "hostile"
             : o.hostile_hint === "friendly" ? "friendly" : "neutral";
    }

    // Relationship/position predicates over the Room.Occupants fields
    // (position, is_loyal_follower, is_my_follower, fighting_you,
    // is_your_target, fighting — GMCP 11.2.0). All degrade gracefully when
    // the fields are absent: predicates just return false and the new menu
    // options don't appear.
    function posLower(o) { return String((o && o.position) || "").toLowerCase(); }
    function occSleeping(o) { return posLower(o) === "sleeping"; }
    function occSeated(o) { var p = posLower(o); return p === "sitting" || p === "resting"; }
    function occByHandle(h) {
        if (!h) return null;
        for (var i = 0; i < (S.occupants || []).length; i++) {
            if (S.occupants[i].handle === h) return S.occupants[i];
        }
        return null;
    }
    function anyLoyalFollowerHere() {
        return (S.occupants || []).some(function (o) { return o.is_loyal_follower && !o.is_dead; });
    }
    // Terse label for a fight edge ("⚔ guard"): the keyword reads better in a
    // cramped row than a full short_desc.
    function occFightLabel(o) {
        if (o.fighting_you) return "⚔ you";
        if (!o.fighting) return "";
        var t = occByHandle(o.fighting);
        return "⚔ " + (t ? firstWord(t.keyword) : "…");
    }

    function renderOccupants() {
        var occ = S.occupants || [];
        var hasShop = occ.some(function (o) { return o.is_shopkeeper; });
        // Room-level List (every shop here) only when there's a shop to list.
        var actions = hasShop
            ? [el("button", { type: "button", class: "panel-h-btn", "data-cmd": "list", title: "List every shopkeeper's wares here", text: "List" })]
            : null;
        var head = panelHeader("occupants", "Room (" + occ.length + ")", false, actions);
        var kids = [head];
        if (!isCollapsed("occupants")) {
            if (!occ.length) {
                kids.push(el("div", { class: "panel-empty", text: "No one else here." }));
            } else {
                // Target chips (current defaults) so they're visible at a glance.
                if (S.tgtHostile || S.tgtFriendly) {
                    var chips = [];
                    if (S.tgtHostile) chips.push(el("span", { class: "tgt-chip hostile", title: "Offensive spells target this", text: "⚔ " + S.tgtHostile.desc }));
                    if (S.tgtFriendly) chips.push(el("span", { class: "tgt-chip friendly", title: "Beneficial spells target this", text: "✚ " + S.tgtFriendly.desc }));
                    kids.push(el("div", { class: "tgt-chips" }, chips));
                }
                var list = el("ul", { class: "occ-list" });
                occ.forEach(function (o, i) {
                    var marks = "";
                    if (S.tgtHostile && S.tgtHostile.handle === o.handle) marks += " ⚔";
                    if (S.tgtFriendly && S.tgtFriendly.handle === o.handle) marks += " ✚";
                    // Position tag for anyone not simply standing (the same
                    // cue the room text gives: "is sleeping here").
                    var ptag = (!o.is_dead && o.position && posLower(o) !== "standing")
                        ? posLower(o) : "";
                    var fight = o.is_dead ? "" : occFightLabel(o);
                    var row = el("li", {
                        class: "occ-row " + occHostileClass(o) + (o.is_dead ? " is-dead" : ""),
                        "data-menu": "occupant", "data-idx": i,
                        title: o.is_dead ? "Slain — not targetable" : "Tap for actions"
                    }, [
                        el("span", { class: "occ-icon", "aria-hidden": "true", text: o.is_player ? "☻" : "•" }),
                        el("span", { class: "occ-name", text: stripColor(o.short_desc || o.keyword) }),
                        o.is_loyal_follower ? el("span", { class: "occ-loyal", title: "Loyal follower — takes your orders", text: "⚑" }) : null,
                        o.is_shopkeeper ? el("span", { class: "occ-shop", title: "Sells wares — List", text: "$" }) : null,
                        ptag ? el("span", { class: "occ-pos", text: ptag }) : null,
                        fight ? el("span", { class: "occ-fight" + (o.fighting_you ? " you" : ""), title: o.fighting_you ? "Fighting YOU" : "In combat", text: fight }) : null,
                        marks ? el("span", { class: "occ-marks", "aria-hidden": "true", text: marks }) : null,
                        el("button", { type: "button", class: "row-more", "data-menu": "occupant", "data-idx": i, "aria-label": "Actions", text: "⋯" })
                    ]);
                    list.appendChild(row);
                });
                kids.push(list);
            }
        }
        fill(dom.occupants, kids);
    }

    // ------------------------------------------------------------------
    // Equipment
    // ------------------------------------------------------------------
    function conditionNode(c) {
        if (c == null) return null;
        // Real feed: int 0-100. Older/demo: a word. Colour numeric by value.
        var n = Number(c);
        if (!isNaN(n) && String(c).match(/^\s*\d/)) {
            var cls = n >= 90 ? "cond-ok" : n >= 50 ? "cond-mid" : "cond-low";
            var lbl = n >= 95 ? "pristine" : n >= 75 ? "good" : n >= 40 ? "worn" : n > 0 ? "battered" : "ruined";
            return el("span", { class: "tag " + cls, title: "Condition " + n + "%", text: lbl });
        }
        return el("span", { class: "tag", text: String(c) });
    }
    function itemDataset(it, kind, container) {
        return {
            "data-menu": "item", "data-kind": kind || "item",
            "data-target": targetOf(it.keywords || it.name),
            "data-otype": it.type || "",
            "data-name": stripColor(it.name || ""),
            "data-container": container || "",
            "data-closeable": it.closeable ? "1" : "",
            "data-closed": it.closed ? "1" : ""
        };
    }
    function itemRow(it, kind, container) {
        var ds = itemDataset(it, kind, container);
        var kids = [];
        if (kind === "equip") kids.push(el("span", { class: "slot", text: it.location || it.slot || "" }));
        kids.push(el("span", { class: "row-name", text: stripColor(it.name) }));
        if (it.count && it.count > 1) kids.push(el("span", { class: "tag", text: "×" + it.count }));
        if (kind === "equip") { var cn = conditionNode(it.condition); if (cn) kids.push(cn); }
        if (it.type === "container") kids.push(el("span", { class: "dim", "aria-hidden": "true", text: it.closed ? " 🔒" : " 📦" }));
        kids.push(el("button", { type: "button", class: "row-more", "aria-label": "Actions", text: "⋯" }));
        ds.class = "row" + (kind === "content" ? " sub" : "");
        return el("li", assign(ds, {}), kids);
    }
    function assign(a, b) { Object.keys(b).forEach(function (k) { a[k] = b[k]; }); return a; }

    // A row list where any container row is followed by a sub-list of its (open)
    // contents. Shared by the inventory and equipment panels so a WORN container
    // (a backpack on the back) is inspectable exactly like a carried one — the
    // game already emits worn-container contents in Char.Equipment (#1590); the
    // equipment panel just wasn't rendering them (issue #1801).
    function itemListWithContents(items, kind) {
        var list = el("ul", { class: "row-list" });
        (items || []).forEach(function (it) {
            list.appendChild(itemRow(it, kind));
            if (it.contents && it.contents.length) {
                var sub = el("ul", { class: "row-list sub" });
                var ct = targetOf(it.keywords || it.name);
                it.contents.forEach(function (c) { sub.appendChild(itemRow(c, "content", ct)); });
                list.appendChild(sub);
            }
        });
        return list;
    }

    function renderEquipment() {
        var items = S.equipment || [];
        var head = panelHeader("equipment", "Equipment", false);
        var kids = [head];
        if (!isCollapsed("equipment")) {
            if (!items.length) kids.push(el("div", { class: "panel-empty", text: "Nothing worn." }));
            else kids.push(itemListWithContents(items, "equip"));
        }
        fill(dom.equipment, kids);
    }

    // ------------------------------------------------------------------
    // Inventory (items + containers + components + coins)
    // ------------------------------------------------------------------
    function renderInventory() {
        var inv = S.inventory;
        var head = panelHeader("inventory", "Inventory", false);
        var kids = [head];
        if (!isCollapsed("inventory")) {
            if (!inv) {
                kids.push(el("div", { class: "panel-empty", text: "Empty." }));
            } else {
                var items = inv.items || [], coins = inv.coins || [], comps = inv.components || [];
                if (items.length) {
                    kids.push(itemListWithContents(items, "item"));
                } else {
                    kids.push(el("div", { class: "panel-empty", text: "Empty." }));
                }

                // Components — collapsible on its own and default-collapsed,
                // since a crafter's pouch gets very long. Clicking a component
                // withdraws it from the pouch.
                if (comps.length) {
                    kids.push(componentsSection(comps));
                }
                // Obsidian's worth is already folded into the purse "Gold" total
                // shown in the Status pane (count_inv_coins sums every coin type
                // ×coin_mult), so a separate obsidian line here is redundant —
                // drop it (issue #1801).
                var shownCoins = coins.filter(function (c) { return !/obsidian/i.test(c.name || ""); });
                if (shownCoins.length) {
                    kids.push(el("div", { class: "coins", text: shownCoins.map(function (c) { return c.count + " " + c.name; }).join(" · ") }));
                }
            }
        }
        fill(dom.inventory, kids);
    }

    function componentsSection(comps) {
        var key = "components";
        if (collapsed[key] === undefined) collapsed[key] = true;   // default collapsed
        var isCol = !!collapsed[key];
        var head = el("button", {
            type: "button", class: "sub-h collapse" + (isCol ? " collapsed" : ""),
            "data-collapse": key, "aria-expanded": isCol ? "false" : "true"
        }, [
            el("span", { class: "panel-caret", "aria-hidden": "true", text: isCol ? "▸" : "▾" }),
            "Components (" + comps.length + ")"
        ]);
        var out = [head];
        if (!isCol) {
            var list = el("ul", { class: "row-list" });
            comps.forEach(function (c) {
                var name = stripColor(c.name);
                var li;
                if (c.keywords) {
                    // Real keyword: a tap withdraws from the pouch directly (the
                    // requested behaviour); ⋯ opens deposit/examine.
                    var tgt = targetOf(c.keywords);
                    li = el("li", { class: "row comp", "data-cmd": "get " + tgt + " pouch", title: "Withdraw from pouch — ⋯ for more" }, [
                        el("span", { class: "row-name", text: name }),
                        c.count > 1 ? el("span", { class: "tag", text: "×" + c.count }) : null,
                        el("button", { type: "button", class: "row-more", "data-menu": "component", "data-target": tgt, "data-name": name, "aria-label": "Actions", text: "⋯" })
                    ]);
                } else {
                    // No keywords (pre-deploy of the game field): a name-derived
                    // withdraw wouldn't resolve, so offer examine only.
                    li = el("li", { class: "row comp", "data-cmd": "examine " + targetOf(c.name), title: "Examine" }, [
                        el("span", { class: "row-name", text: name }),
                        c.count > 1 ? el("span", { class: "tag", text: "×" + c.count }) : null
                    ]);
                }
                list.appendChild(li);
            });
            out.push(list);
        }
        return el("div", { class: "comp-section" }, out);
    }

    // ------------------------------------------------------------------
    // Character (train)
    // ------------------------------------------------------------------
    function renderTrain() {
        var t = S.train;
        var head = panelHeader("train", "Character", false);
        var kids = [head];
        if (!isCollapsed("train")) {
            if (!t) kids.push(el("div", { class: "panel-empty", text: "—" }));
            else {
                if (t.xp_pct != null) {
                    kids.push(el("div", { class: "vbar xp" }, [
                        el("span", { class: "vbar-label", text: "XP" }),
                        el("span", { class: "vbar-track" }, [
                            el("span", { class: "vbar-fill", style: "width:" + clamp(t.xp_pct, 0, 100) + "%" }),
                            el("span", { class: "vbar-text", text: clamp(t.xp_pct, 0, 100) + "%" })
                        ])
                    ]));
                }
                if (t.can_advance) kids.push(el("button", { class: "action-btn", "data-cmd": "advance", text: "⬆ Advance available" }));
                var ul = el("ul", { class: "kv" });
                (t.stats || []).forEach(function (s) {
                    ul.appendChild(el("li", {}, [el("span", { text: s.name }), el("span", { text: s.value + (s.add ? " (+" + s.add + ")" : "") })]));
                });
                (t.resources || []).forEach(function (r) {
                    ul.appendChild(el("li", {}, [el("span", { text: r.label || r.name }), el("span", { text: r.value + " / " + r.max })]));
                });
                (t.aux || []).forEach(function (a) {
                    ul.appendChild(el("li", {}, [el("span", { text: a.label || a.name }), el("span", { text: a.value })]));
                });
                kids.push(ul);
            }
        }
        fill(dom.train, kids);
    }

    // ------------------------------------------------------------------
    // Status (resources + affects + group)
    // ------------------------------------------------------------------
    function mini(p, cls) {
        return el("span", { class: "mini " + cls }, el("span", { style: "width:" + clamp(p, 0, 100) + "%" }));
    }
    function renderStatus() {
        var kids = [], st = S.status;
        if (st) {
            var ul = el("ul", { class: "kv" });
            [["Align", st.align], ["Gold", Number(st.gold || 0).toLocaleString()],
             ["To level", Number(st.tnl || 0).toLocaleString()], ["Bank", Number(st.bank || 0).toLocaleString()],
             ["Remort", st.remort]].forEach(function (kvp) {
                ul.appendChild(el("li", {}, [el("span", { text: kvp[0] }), el("span", { text: String(kvp[1]) })]));
            });
            kids.push(ul);
        }
        var a = S.affects;
        function affItems(arr, cls) {
            return (arr || []).map(function (x) {
                // Absolute expiry is stamped once when Char.Affects arrives, so
                // unrelated re-renders (Char.Status, Group.Update) don't snap the
                // countdown back to its full original duration.
                var exp = x._expiry != null ? x._expiry : now() + (Number(x.duration) || 0);
                var right = [el("span", { class: "aff-time", "data-expiry": exp, text: fmtDur(exp - now()) })];
                if (x.releasable && x.skill) {
                    right.unshift(el("button", { type: "button", class: "aff-release", "data-cmd": "release spell " + nameOf(x.skill) + " " + (x.handle || ""), title: "Release", text: "release" }));
                }
                return el("li", { class: "aff " + cls }, [
                    el("span", { class: "aff-name" }, [stripColor(x.name), x.target ? el("span", { class: "dim", text: " › " + stripColor(x.target) }) : null]),
                    el("span", { class: "aff-right" }, right)
                ]);
            });
        }
        if (a) {
            kids.push(el("div", { class: "sub-h", text: "Affects" }));
            var affNodes = affItems(a.buffs, "buff").concat(affItems(a.maintained, "maint"), affItems(a.debuffs, "debuff"));
            kids.push(affNodes.length ? el("ul", { class: "aff-list" }, affNodes) : el("div", { class: "panel-empty", text: "None." }));
        }
        fill(dom.status, kids.length ? kids : [el("div", { class: "panel-empty", text: "—" })]);
    }

    // ------------------------------------------------------------------
    // Group (Group.Update) — the party pane. Members and allies with live
    // vitals, tank/threat state and fight edges; rows map onto Room.Occupants
    // entries (players by name, allies by loyal-follower short_desc) so one
    // tap opens the same action menu the occupants panel uses — heals, wake,
    // yank, orders — without duplicating a menu system.
    // ------------------------------------------------------------------
    function groupMemberOcc(m) {
        // A player member's occupant entry: players' keyword IS their name.
        for (var i = 0; i < (S.occupants || []).length; i++) {
            var o = S.occupants[i];
            if (o.is_player && !o.is_dead
                && firstWord(o.keyword).toLowerCase() === String(m.name || "").toLowerCase()) return o;
        }
        return null;
    }
    function groupAllyOcc(a) {
        // An ally row maps to a loyal-follower occupant with the same display
        // name; prefer own loyal followers so the menu's orders land on OUR
        // wolf when two identical wolves share the room.
        var name = stripColor(String(a.name || ""));
        var loose = null;
        for (var i = 0; i < (S.occupants || []).length; i++) {
            var o = S.occupants[i];
            if (o.is_player || o.is_dead) continue;
            if (stripColor(o.short_desc || "") !== name) continue;
            if (o.is_loyal_follower) return o;
            if (!loose) loose = o;
        }
        return loose;
    }
    function threatChip(x) {
        if (x.threat == null) return null;
        var lvl = x.threat_level || "";
        var txt = "T:" + x.threat + (x.tank_threat != null ? "/" + x.tank_threat : "");
        var title = x.tank_threat != null
            ? "Threat vs the tank's (" + x.tank_threat + ") on their target"
            : "Threat on their target";
        return el("span", { class: "grp-threat" + (lvl ? " threat-" + lvl : ""), title: title, text: txt });
    }
    function groupRow(x, kind, idx, extraName) {
        var chips = [];
        if (x.is_tank) chips.push(el("span", { class: "grp-tank", title: "Tanking — enemies are targeting them", text: "TANK" }));
        var tc = threatChip(x);
        if (tc) chips.push(tc);
        if (x.fighting) chips.push(el("span", { class: "grp-fight", title: "Fighting", text: "⚔ " + stripColor(x.fighting) }));
        var p = String(x.position || "").toLowerCase();
        if (p && p !== "standing") chips.push(el("span", { class: "grp-pos", text: p }));
        if (x.in_room === false) chips.push(el("span", { class: "grp-away", title: "Not in your room", text: "away" }));
        var main = el("div", { class: "grp-main" }, [
            el("div", { class: "grp-line" }, [
                el("span", { class: "grp-name", text: stripColor(String(x.name || "")) + (x.leader ? " ★" : "") }),
                extraName ? el("span", { class: "dim", text: " " + extraName }) : null,
                el("span", { class: "grp-hp-num", text: (x.hp_pct != null ? x.hp_pct + "%" : "") })
            ]),
            chips.length ? el("div", { class: "grp-chips" }, chips) : null,
            el("span", { class: "grp-bars" }, [mini(x.hp_pct, "hp"), mini(x.mp_pct, "mp"), mini(x.mv_pct, "mv")])
        ]);
        return el("li", {
            class: "grp" + (x.is_tank ? " tanking" : ""),
            "data-menu": "grp", "data-gkind": kind, "data-gidx": idx,
            title: "Tap for actions"
        }, [
            main,
            el("button", { type: "button", class: "row-more", "data-menu": "grp", "data-gkind": kind, "data-gidx": idx, "aria-label": "Actions", text: "⋯" })
        ]);
    }
    function renderGroup() {
        if (!dom.group) return;
        var g = S.group;
        var members = (g && g.members) || [];
        var allies = (g && g.allies) || [];
        var head = panelHeader("group", "Group" + (members.length ? " (" + (g.size != null ? g.size : members.length) + ")" : ""), false);
        var kids = [head];
        if (!isCollapsed("group")) {
            if (!members.length && !allies.length) {
                kids.push(el("div", { class: "panel-empty", text: "Not grouped." }));
            } else {
                var gl = el("ul", { class: "grp-list" });
                members.forEach(function (m, i) { gl.appendChild(groupRow(m, "member", i)); });
                kids.push(gl);
                if (allies.length) {
                    kids.push(el("div", { class: "sub-h", text: "Allies" }));
                    var al = el("ul", { class: "grp-list" });
                    allies.forEach(function (a, i) {
                        al.appendChild(groupRow(a, "ally", i, a.owner ? "(" + a.owner + ")" : ""));
                    });
                    kids.push(al);
                }
            }
        }
        fill(dom.group, kids);
    }
    function groupRowActions(x, kind) {
        if (!x) return [];
        var occ = kind === "ally" ? groupAllyOcc(x) : groupMemberOcc(x);
        // In your room: the row is just another face of the occupant — same
        // menu, same handles (heals, wake, yank, orders, targets).
        if (occ) return occupantActions(occ);
        // Out of room (or unseen): only name-keyed, cross-room actions work.
        var acts = [];
        if (kind === "member") {
            var nm = firstWord(String(x.name || ""));
            var self = S.status && String(S.status.name || "").toLowerCase() === nm.toLowerCase();
            if (nm && !self) acts.push({ label: "Tell…", prefill: "tell " + nm + " " });
        }
        return acts;
    }

    // ------------------------------------------------------------------
    // Who (global online players)
    // ------------------------------------------------------------------
    function renderWho() {
        var w = S.who;
        if (!w || !w.players) { fill(dom.who, el("div", { class: "panel-empty", text: "—" })); return; }
        var list = el("ul", { class: "who-list" });
        w.players.forEach(function (p) {
            var nm = firstWord(p.name);
            var flags = (p.is_my_leader ? " ◂leader" : "") + (p.following_me ? " follower▸" : "");
            list.appendChild(el("li", { class: "who-row" }, [
                el("div", { class: "who-main" }, [
                    el("span", { class: "who-name", text: p.name }),
                    el("span", { class: "dim", text: " L" + p.level + " " + p.race + " " + p["class"] }),
                    p.title ? el("div", { class: "who-title", text: p.title }) : null,
                    flags ? el("span", { class: "dim", text: flags }) : null
                ]),
                el("div", { class: "who-act" }, [
                    el("button", { "data-prefill": "tell " + nm + " ", text: "Tell" }),
                    el("button", { "data-cmd": "follow " + nm, text: "Follow" }),
                    el("button", { "data-cmd": "group " + nm, text: "Group" })
                ])
            ]));
        });
        var kids = [list];
        if (w.hidden) kids.push(el("div", { class: "who-hidden", text: "+" + w.hidden + " hidden" }));
        fill(dom.who, kids);
    }

    // ------------------------------------------------------------------
    // Chat (hot path)
    // ------------------------------------------------------------------
    function chatLine(c) {
        return el("div", { class: "chat-line" }, [
            el("span", { class: "chat-ch", text: "[" + c.channel + "]" }), " ",
            el("span", { class: "chat-txt", text: c.text })
        ]);
    }
    function appendChat(c) {
        var empty = dom.chat.querySelector(".panel-empty");
        if (empty) dom.chat.removeChild(empty);
        var stick = dom.chat.scrollTop + dom.chat.clientHeight >= dom.chat.scrollHeight - 40;
        dom.chat.appendChild(chatLine(c));
        while (dom.chat.children.length > CHAT_MAX) dom.chat.removeChild(dom.chat.firstChild);
        if (stick) dom.chat.scrollTop = dom.chat.scrollHeight;
    }
    function renderChat() {
        if (!S.chat.length) fill(dom.chat, el("div", { class: "panel-empty", text: "No messages yet." }));
        else fill(dom.chat, S.chat.map(chatLine));
        dom.chat.scrollTop = dom.chat.scrollHeight;
    }

    // ------------------------------------------------------------------
    // Abilities: the target-aware command + shared usability logic.
    // ------------------------------------------------------------------
    // The exact command to invoke an ability, or null if it can't be actively
    // used (passive / craft / enchant). Mirrors the game's real syntax rather
    // than reconstructing a bare verb from the name.
    function abilityCommand(s) {
        var nm = nameOf(s.name);
        // Metamagic modes: the skill is named "Metamagic: Clarity" but invoked
        // as "metamagic clarity".
        var mm = nm.match(/^Metamagic:\s*(.+)$/i);
        if (mm) return "metamagic " + mm[1].toLowerCase();
        if (s.type === "passive" || s.type === "craft" || s.type === "enchant") return null;
        if (s.type === "spell") {
            var base = "cast '" + nm + "'";
            if (s.target_type === "offensive" && S.tgtHostile) return base + " " + S.tgtHostile.handle;
            if (s.target_type === "defensive" && S.tgtFriendly) return base + " " + S.tgtFriendly.handle;
            return base;
        }
        // Multi-word skills ("Shield Slam") must go through the "action" parser
        // (the one spells use) or they're misread as command "shield" + arg
        // "slam"; single-word skills work as a bare verb.
        return /\s/.test(nm) ? "action " + nm : nm;
    }
    function abilityUsable(s) { return abilityCommand(s) != null; }
    // Why a skill is unusable right now (or null). cd in seconds.
    function abilityBlock(s) {
        var t = now();
        var exp = S.cooldownExpiry[s.id];
        var cd = (exp && exp > t) ? Math.ceil(exp - t) : 0;
        if (cd > 0) return { cd: cd, reason: cd + "s" };
        if (s.usable === false || S.usable[s.id] === false) return { cd: 0, reason: "unavailable" };
        var v = S.vitals;
        if (s.type === "spell" && v && v.mp != null) {
            // The game blocks a cast when current mana (SPTS) < the spell's
            // energy cost, so gate on the actual points (issue #1801). The
            // `mana` field is that exact cost; prefer it. The older `mana_pct`
            // is a rounded cost% compared to a rounded mana% — lossy enough to
            // falsely block a spell the player can afford — so it's only the
            // fallback for the window before the game emits `mana`.
            if (s.mana != null) {
                if (Number(s.mana) > Number(v.mp)) return { cd: 0, reason: "low mana" };
            } else if (v.maxmp > 0 && s.mana_pct != null) {
                var manaPct = Math.round(Number(v.mp) / v.maxmp * 100);
                if (s.mana_pct > manaPct) return { cd: 0, reason: "low mana" };
            }
        }
        if (v && v.position && s.min_position && posRank(v.position) < posRank(s.min_position)) {
            return { cd: 0, reason: s.min_position };
        }
        return null;
    }
    function catClass(s) {
        return "cat-" + String(s.category || (s.type === "spell" ? "misc" : "skill")).replace(/[^a-zA-Z0-9_-]/g, "");
    }

    // The bounded bottom quick-bar. Favorites if any; else a capped default of
    // usable damage/heal so it's useful out-of-box and NEVER unbounded.
    var hotbarNodes = {};
    function quickbarSkills() {
        var skills = (S.skills || []).filter(function (s) { return s.type === "spell" || s.type === "skill"; });
        var out = [], seen = {};
        function push(s, cap) { if (s && !seen[s.id] && out.length < cap) { seen[s.id] = true; out.push(s); } }
        // Favorites first (user-chosen, shown in full up to FAV_CAP)...
        skills.forEach(function (s) { if (favorites[nameOf(s.name).toLowerCase()]) push(s, FAV_CAP); });
        // ...then backfill toward QUICKBAR_MAX with usable damage/heal, so a few
        // pins don't wipe the auto set — the bar stays useful, not empty...
        if (out.length < QUICKBAR_MAX) {
            var rank = { damage: 0, heal: 1, misc: 2 };
            skills.filter(function (s) { return !abilityBlock(s); })
                  .sort(function (a, b) { return (rank[a.category] == null ? 3 : rank[a.category]) - (rank[b.category] == null ? 3 : rank[b.category]); })
                  .forEach(function (s) { push(s, QUICKBAR_MAX); });
        }
        // ...and always surface anything cooling so its timer stays visible.
        skills.forEach(function (s) { if (S.cooldownExpiry[s.id] > now()) push(s, FAV_CAP); });
        return out;
    }
    function renderHotbar() {
        var skills = quickbarSkills();
        hotbarNodes = {};
        while (dom.hotbar.firstChild) dom.hotbar.removeChild(dom.hotbar.firstChild);
        if (!skills.length) { dom.hotbar.classList.add("empty"); return; }
        dom.hotbar.classList.remove("empty");
        skills.forEach(function (s) {
            var btn = el("button", {
                class: "skill " + catClass(s), "data-ability": s.id, "data-menu": "ability",
                title: s.name + " (" + s.percent + "%)"
            }, [
                el("span", { class: "skill-name", text: s.name }),
                el("span", { class: "skill-cd" }),
                el("span", { class: "skill-pct", text: String(s.percent) })
            ]);
            dom.hotbar.appendChild(btn);
            hotbarNodes[s.id] = { btn: btn, cdEl: btn.querySelector(".skill-cd") };
        });
        tickHotbar();
    }
    function tickHotbar() {
        Object.keys(hotbarNodes).forEach(function (id) {
            var n = hotbarNodes[id];
            var s = skillById(id);
            if (!s || !n) return;
            var blk = abilityBlock(s);
            var cd = blk ? blk.cd : 0;
            // Surface a non-cooldown block reason (mana / min-position) in the
            // button and title, so a blocked skill isn't a silent dead tap.
            var reason = (blk && cd === 0)
                ? (blk.reason === "low mana" ? "mana" : blk.reason === "unavailable" ? "" : blk.reason)
                : "";
            n.btn.classList.toggle("off", !!blk);
            n.btn.classList.toggle("cooling", cd > 0);
            n.btn.classList.toggle("blocked", !!(blk && cd === 0 && reason));
            n.cdEl.textContent = cd > 0 ? String(cd) : reason;
            n.btn.title = s.name + " (" + s.percent + "%)" + (blk && cd === 0 ? " — " + blk.reason : "");
        });
    }
    function skillById(id) {
        id = String(id);
        var list = S.skills || [];
        for (var i = 0; i < list.length; i++) if (String(list[i].id) === id) return list[i];
        return null;
    }

    // The full, scroll-bounded Abilities browser: search + type filter +
    // usable-only, so hundreds of skills never grow the layout.
    function renderAbilities() {
        var all = S.skills || [];
        // Preserve the search box's focus + caret across the rebuild (this
        // runs on every keystroke, and on cooldown/skill feeds).
        var hadFocus = document.activeElement && document.activeElement.id === "ab-search";
        var caret = hadFocus ? document.activeElement.selectionStart : null;
        // Preserve scroll position — this rebuilds on every cooldown/skill feed
        // while the tab is open, and would otherwise snap a 400-row list to top.
        var prevScroll = dom.abilities.querySelector(".ab-scroll");
        var savedTop = prevScroll ? prevScroll.scrollTop : 0;
        var kids = [];
        // Controls row.
        var search = el("input", {
            type: "text", class: "ab-search", id: "ab-search",
            placeholder: "Filter abilities…", autocomplete: "off", spellcheck: "false", value: abilityFilter.q
        });
        search.addEventListener("input", function () { abilityFilter.q = search.value; renderAbilities(); persistAbilityFilter(); });
        kids.push(el("div", { class: "ab-controls" }, [search]));

        var typeChips = el("div", { class: "ab-chips" });
        var counts = { all: 0, fav: 0, spell: 0, skill: 0, craft: 0 };
        all.forEach(function (s) {
            counts.all++;
            if (favorites[nameOf(s.name).toLowerCase()]) counts.fav++;
            if (s.type === "spell") counts.spell++;
            else if (s.type === "skill") counts.skill++;
            else if (s.type === "craft" || s.type === "enchant") counts.craft++;
        });
        // "All" and "★ Fav" always show (Fav invites pinning even at 0); the
        // type chips appear only when they have members.
        [["all", "All"], ["fav", "★"], ["spell", "Spells"], ["skill", "Skills"], ["craft", "Crafts"]].forEach(function (tc) {
            if (tc[0] !== "all" && tc[0] !== "fav" && !counts[tc[0]]) return;
            typeChips.appendChild(el("button", {
                type: "button", class: "ab-chip" + (tc[0] === "fav" ? " ab-fav" : "") + (abilityFilter.type === tc[0] ? " on" : ""),
                "data-abtype": tc[0], text: tc[1] + " " + counts[tc[0]]
            }));
        });
        typeChips.appendChild(el("button", {
            type: "button", class: "ab-chip ab-usable" + (abilityFilter.usableOnly ? " on" : ""),
            "data-abusable": "1", text: "✓ Usable"
        }));
        kids.push(typeChips);

        // Filtered list.
        var q = abilityFilter.q.trim().toLowerCase();
        var rows = all.filter(function (s) {
            if (abilityFilter.type === "fav" && !favorites[nameOf(s.name).toLowerCase()]) return false;
            if (abilityFilter.type === "spell" && s.type !== "spell") return false;
            if (abilityFilter.type === "skill" && s.type !== "skill") return false;
            if (abilityFilter.type === "craft" && s.type !== "craft" && s.type !== "enchant") return false;
            if (q && String(s.name).toLowerCase().indexOf(q) === -1) return false;
            if (abilityFilter.usableOnly && abilityBlock(s)) return false;
            return true;
        });
        // Usable first, then alpha.
        rows.sort(function (a, b) {
            var ba = abilityBlock(a) ? 1 : 0, bb = abilityBlock(b) ? 1 : 0;
            if (ba !== bb) return ba - bb;
            return String(a.name).localeCompare(String(b.name));
        });

        var scroller = el("div", { class: "ab-scroll" });
        if (!rows.length) {
            var emptyMsg = !all.length ? "—"
                : abilityFilter.type === "fav" ? "No favorites yet — tap ☆ (or right-click an ability) to add one."
                : "No abilities match.";
            scroller.appendChild(el("div", { class: "panel-empty", text: emptyMsg }));
        } else {
            var ul = el("ul", { class: "ab-list" });
            rows.forEach(function (s) {
                var passive = !abilityUsable(s);   // passive / craft / enchant
                var blk = passive ? null : abilityBlock(s);
                var fav = !!favorites[nameOf(s.name).toLowerCase()];
                var right = [];
                if (blk) right.push(el("span", { class: "ab-block", text: blk.cd > 0 ? blk.cd + "s" : blk.reason }));
                if (passive) right.push(el("span", { class: "ab-type", text: s.type }));
                right.push(el("span", { class: "ab-pct", text: s.percent + "%" }));
                right.push(el("button", { type: "button", class: "ab-star" + (fav ? " on" : ""), "data-fav": nameOf(s.name), "aria-label": fav ? "Remove from favorites" : "Add to favorites", title: fav ? "Remove from favorites" : "Add to favorites", text: fav ? "★" : "☆" }));
                right.push(el("button", { type: "button", class: "row-more", "aria-label": "More actions", text: "⋯" }));
                ul.appendChild(el("li", {
                    class: "ab-row " + catClass(s) + (blk ? " off" : "") + (passive ? " ab-passive" : ""),
                    "data-ability": s.id, "data-menu": "ability",
                    title: passive ? s.name + " — " + s.type + " (not usable)" : castHint(s)
                }, [
                    el("span", { class: "ab-name", text: s.name }),
                    el("span", { class: "ab-right" }, right)
                ]));
            });
            scroller.appendChild(ul);
        }
        kids.push(scroller);
        fill(dom.abilities, kids);
        scroller.scrollTop = savedTop;
        if (hadFocus) {
            var again = document.getElementById("ab-search");
            if (again) { again.focus(); if (caret != null) again.setSelectionRange(caret, caret); }
        }
    }
    function castHint(s) {
        var tt = s.type === "spell" ? "cast" : "use";
        var arrow = "";
        if (s.type === "spell" && s.target_type === "offensive") arrow = S.tgtHostile ? " → " + S.tgtHostile.desc : " (set a ⚔ target)";
        if (s.type === "spell" && s.target_type === "defensive") arrow = S.tgtFriendly ? " → " + S.tgtFriendly.desc : " (set a ✚ target)";
        return tt + " " + s.name + arrow;
    }
    function persistAbilityFilter() {
        try { localStorage.setItem("ishar.abilityFilter", JSON.stringify({ type: abilityFilter.type, usableOnly: abilityFilter.usableOnly })); } catch (e) {}
    }
    function toggleFavorite(name) {
        var k = nameOf(name).toLowerCase();
        if (favorites[k]) delete favorites[k]; else favorites[k] = true;
        saveSet("ishar.favs", favorites);
        renderHotbar(); renderAbilities();
    }

    // ------------------------------------------------------------------
    // Context / action menu (works with mouse + touch)
    // ------------------------------------------------------------------
    // Single guarded exit for every game command a widget builds — strips
    // control chars / newlines so a keyword or server handle can never smuggle
    // a second command onto the line.
    function sendCmd(c) { c = safeCmd(c); if (c) api.send(c); }

    var menuOpen = false;
    function closeMenu() {
        if (!menuOpen) return;
        menuOpen = false;
        dom.menu.hidden = true;
        while (dom.menu.firstChild) dom.menu.removeChild(dom.menu.firstChild);
    }
    // actions: [{label, cmd|prefill|fn, danger}]. Anchored near `anchor`.
    function openMenu(title, actions, anchor) {
        closeMenu();
        actions = actions.filter(Boolean);
        if (!actions.length) return;
        var kids = [el("div", { class: "menu-title", text: title })];
        actions.forEach(function (a) {
            // No data-cmd/data-prefill here on purpose: the delegated app-click
            // handler would fire the command a *second* time. The onclick owns
            // the action outright.
            kids.push(el("button", {
                type: "button", class: "menu-item" + (a.danger ? " danger" : ""),
                text: a.label,
                onclick: function () {
                    if (a.fn) a.fn();
                    else if (a.prefill != null) api.prefill(a.prefill);
                    else if (a.cmd) sendCmd(a.cmd);
                    closeMenu();
                    if (sheetName && mqMobile.matches) setSheet(null);
                }
            }));
        });
        fill(dom.menu, kids);
        dom.menu.hidden = false;
        menuOpen = true;
        positionMenu(anchor);
    }
    function positionMenu(anchor) {
        var m = dom.menu;
        m.style.left = "0px"; m.style.top = "0px";
        var mw = m.offsetWidth, mh = m.offsetHeight;
        var vw = window.innerWidth, vh = window.visualViewport ? window.visualViewport.height : window.innerHeight;
        var x, y;
        if (anchor && anchor.getBoundingClientRect) {
            var r = anchor.getBoundingClientRect();
            x = Math.min(r.left, vw - mw - 8);
            y = r.bottom + 4;
            if (y + mh > vh - 8) y = Math.max(8, r.top - mh - 4);
        } else {
            x = (vw - mw) / 2; y = (vh - mh) / 2;
        }
        m.style.left = Math.max(8, x) + "px";
        m.style.top = Math.max(8, y) + "px";
    }

    // Person-target spells to offer as one-off casts AT a specific occupant —
    // independent of the default ⚔/✚ targets. Filtered by disposition: an
    // allied (friendly) target only gets beneficial (defensive) spells, everyone
    // else only offensive ones. Favorited spells first (keeps it your curated
    // set), else usable ones.
    function occupantCastActions(o) {
        var want = o.hostile_hint === "friendly" ? "defensive" : "offensive";
        var spells = (S.skills || []).filter(function (s) {
            return s.type === "spell" && s.target_type === want;
        });
        var fav = spells.filter(function (s) { return favorites[nameOf(s.name).toLowerCase()]; });
        var pick = fav.length ? fav : spells.filter(function (s) { return !abilityBlock(s); });
        return pick.slice(0, 6).map(function (s) {
            return { label: "Cast " + s.name, cmd: "cast '" + nameOf(s.name) + "' " + o.handle };
        });
    }

    function occupantActions(o) {
        if (!o) return [];
        var acts = [];
        var friendly = o.hostile_hint === "friendly";
        acts.push({ label: "Look", cmd: "look " + o.handle });
        if (o.is_dead) return acts;   // slain — nothing else round-trips
        acts.push({ label: "Consider", cmd: "consider " + o.handle });
        // Cast a chosen spell straight at THIS occupant (not the default target).
        occupantCastActions(o).forEach(function (a) { acts.push(a); });
        if (!friendly) {
            acts.push({ label: "Attack", cmd: "kill " + o.handle, danger: true });
            // Sic your loyal followers on it. Bare keyword, not the handle:
            // each follower resolves ordinals from its OWN perspective, so a
            // viewer-relative "2.thug" could hit the wrong one for them.
            if (anyLoyalFollowerHere()) {
                acts.push({ label: "Order attack", cmd: "order followers kill " + firstWord(o.keyword), danger: true });
            }
        } else {
            // Allies keep Attack available (PK duels, charm gone wrong) but
            // below the fold of ally-flavored actions, still marked danger.
            if (occSleeping(o)) acts.push({ label: "Wake", cmd: "wake " + o.handle });
            if (o.is_my_follower && occSeated(o)) acts.push({ label: "Yank to feet", cmd: "yank " + o.handle });
            acts.push({ label: "Attack", cmd: "kill " + o.handle, danger: true });
        }
        // Posture orders for a loyal follower — only ones that change
        // anything, and none while it sleeps (it can't hear you; Wake first).
        if (o.is_loyal_follower && !occSleeping(o)) {
            ["stand", "rest", "sleep"].forEach(function (p) {
                var current = posLower(o) === (p === "stand" ? "standing" : p === "rest" ? "resting" : "sleeping");
                if (!current) acts.push({ label: "Order: " + p, cmd: "order " + o.handle + " " + p });
            });
        }
        if (!o.is_player) {
            // Only actual vendors get a list action (is_shopkeeper = the mob
            // handles the `list` command, per Room.Occupants).
            if (o.is_shopkeeper) acts.push({ label: "List wares", cmd: "list " + firstWord(o.keyword) });
        } else {
            var nm = firstWord(o.keyword);
            acts.push({ label: "Tell…", prefill: "tell " + nm + " " });
            acts.push({ label: "Follow", cmd: "follow " + nm });
            acts.push({ label: "Group", cmd: "group " + nm });
        }
        acts.push({ label: (S.tgtHostile && S.tgtHostile.handle === o.handle ? "✓ " : "") + "Target ⚔ (offensive)", fn: function () { setTarget("tgtHostile", o); } });
        acts.push({ label: (S.tgtFriendly && S.tgtFriendly.handle === o.handle ? "✓ " : "") + "Target ✚ (beneficial)", fn: function () { setTarget("tgtFriendly", o); } });
        return acts;
    }

    function itemActions(ds) {
        var t = ds.target, name = ds.name || t, otype = ds.otype, kind = ds.kind, container = ds.container;
        var acts = [{ label: "Examine", cmd: "examine " + t }];
        if (kind === "content") {
            acts.push({ label: "Get", cmd: "get " + t + " from " + container });
            return acts;
        }
        if (otype === "container") {
            if (ds.closeable) acts.push(ds.closed ? { label: "Open", cmd: "open " + t } : { label: "Close", cmd: "close " + t });
            if (!ds.closed) acts.push({ label: "Get all from", cmd: "get all from " + t });
        } else {
            var verb = TYPE_VERB[otype];
            if (verb) acts.push({ label: TYPE_VERB_LABEL[verb], cmd: verb + " " + t });
        }
        if (kind === "equip") {
            acts.push({ label: "Remove", cmd: "remove " + t });
        } else {
            // Put into any open, carried container.
            openContainers().forEach(function (c) {
                if (c.target !== t) acts.push({ label: "Put in " + c.shortName, cmd: "put " + t + " into " + c.target });
            });
            acts.push({ label: "Drop", cmd: "drop " + t });
            acts.push({ label: "Sacrifice", cmd: "sacrifice " + t, danger: true });
        }
        return acts;
    }
    function openContainers() {
        var out = [];
        function scan(list) {
            (list || []).forEach(function (it) {
                if (it.type === "container" && !it.closed) {
                    out.push({ target: targetOf(it.keywords || it.name), shortName: (String(it.name).split(/\s+/).pop() || "bag").slice(0, 10) });
                }
            });
        }
        if (S.inventory) scan(S.inventory.items);
        scan(S.equipment);
        return out;
    }
    function componentActions(ds) {
        return [
            { label: "Withdraw from pouch", cmd: "get " + ds.target + " pouch" },
            { label: "Deposit to pouch", cmd: "put " + ds.target + " pouch" },
            { label: "Examine", cmd: "examine " + ds.target }
        ];
    }
    function abilityActions(s) {
        if (!s) return [];
        var fav = !!favorites[nameOf(s.name).toLowerCase()];
        var acts = [];
        var cmd = abilityCommand(s);
        if (cmd) acts.push({ label: s.type === "spell" ? "Cast" : "Use", fn: function () { sendCmd(cmd); } });
        acts.push({ label: "Look up", cmd: "skill search " + nameOf(s.name) });
        acts.push({ label: fav ? "★ Remove from favorites" : "☆ Add to favorites", fn: function () { toggleFavorite(s.name); } });
        return acts;
    }

    // ------------------------------------------------------------------
    // Interaction (delegated)
    // ------------------------------------------------------------------
    function onAppClick(e) {
        // 1) Collapse toggles.
        var col = e.target.closest("[data-collapse]");
        if (col && dom.app.contains(col)) {
            var key = col.getAttribute("data-collapse");
            collapsed[key] = !collapsed[key];
            saveSet("ishar.collapsed", collapsed);
            rerenderPanel(key);
            e.preventDefault();
            return;
        }
        // 2) Ability chip filters + star.
        var chip = e.target.closest("[data-abtype],[data-abusable]");
        if (chip && dom.app.contains(chip)) {
            if (chip.hasAttribute("data-abtype")) abilityFilter.type = chip.getAttribute("data-abtype");
            else abilityFilter.usableOnly = !abilityFilter.usableOnly;
            persistAbilityFilter();
            renderAbilities();
            return;
        }
        var star = e.target.closest("[data-fav]");
        if (star && dom.app.contains(star)) { toggleFavorite(star.getAttribute("data-fav")); return; }

        // 3) Ability cast (hotbar button or abilities row) — not the star.
        var ab = e.target.closest("[data-ability]");
        if (ab && dom.app.contains(ab) && !e.target.closest("[data-fav]") && !e.target.closest(".row-more")) {
            var s = skillById(ab.getAttribute("data-ability"));
            if (s) {
                if (abilityBlock(s) && ab.classList.contains("skill")) return;   // hotbar: inert when blocked
                var acmd = abilityCommand(s);
                if (acmd) { sendCmd(acmd); return; }
                // Not invocable (passive/craft/enchant): fall through to the
                // context menu below rather than firing a dead command.
            } else {
                return;
            }
        }

        // 4) Context-menu openers (row body or its ⋯ button).
        var more = e.target.closest(".row-more");
        var menuHost = e.target.closest("[data-menu]");
        if (menuHost && dom.app.contains(menuHost)) {
            var anchor = more || menuHost;
            openHostMenu(menuHost, anchor);
            e.preventDefault();
            return;
        }

        // 5) Plain data-cmd / data-prefill (exits, group buttons, header List…).
        var t = e.target.closest("[data-cmd],[data-prefill]");
        if (!t || !dom.app.contains(t)) return;
        var fromSheet = sheetName && dom.sheetBody && dom.sheetBody.contains(t);
        if (t.hasAttribute("data-prefill") && t.getAttribute("data-prefill")) {
            api.prefill(t.getAttribute("data-prefill"));
            if (fromSheet) setSheet(null);
            return;
        }
        var cmd = safeCmd(t.getAttribute("data-cmd"));
        if (cmd) { api.send(cmd); if (fromSheet) setSheet(null); }
    }

    function openHostMenu(host, anchor) {
        var kind = host.getAttribute("data-menu");
        if (kind === "occupant") {
            var o = (S.occupants || [])[Number(host.getAttribute("data-idx"))];
            if (o) openMenu(stripColor(o.short_desc || o.keyword), occupantActions(o), anchor);
        } else if (kind === "item") {
            var ds = readDataset(host);
            openMenu(ds.name || ds.target, itemActions(ds), anchor);
        } else if (kind === "component") {
            var cds = readDataset(host);
            openMenu(cds.name || cds.target, componentActions(cds), anchor);
        } else if (kind === "ability") {
            var s2 = skillById(host.getAttribute("data-ability"));
            if (s2) openMenu(s2.name, abilityActions(s2), anchor);
        } else if (kind === "grp") {
            var gkind = host.getAttribute("data-gkind");
            var arr = gkind === "ally" ? (S.group && S.group.allies) : (S.group && S.group.members);
            var x = (arr || [])[Number(host.getAttribute("data-gidx"))];
            if (x) openMenu(stripColor(String(x.name || "")), groupRowActions(x, gkind), anchor);
        }
    }
    function readDataset(host) {
        return {
            target: host.getAttribute("data-target") || "",
            name: host.getAttribute("data-name") || "",
            otype: host.getAttribute("data-otype") || "",
            kind: host.getAttribute("data-kind") || "item",
            container: host.getAttribute("data-container") || "",
            closeable: host.getAttribute("data-closeable") === "1",
            closed: host.getAttribute("data-closed") === "1"
        };
    }
    // Right-click opens the same menu on desktop.
    function onAppContext(e) {
        var host = e.target.closest("[data-menu]");
        if (!host || !dom.app.contains(host)) return;
        e.preventDefault();
        openHostMenu(host, host);
    }

    // Re-render just the panel that owns a collapse key.
    function rerenderPanel(key) {
        switch (key) {
            case "occupants": renderOccupants(); break;
            case "group": renderGroup(); break;
            case "equipment": renderEquipment(); break;
            case "inventory": case "components": renderInventory(); break;
            case "train": renderTrain(); break;
            default: renderAll();
        }
        api.onLayoutChange();
    }

    // ------------------------------------------------------------------
    // Layout modes: panel placement, phone sheet, desktop columns
    // ------------------------------------------------------------------
    function placePanels() {
        var mobile = mqMobile.matches;
        PANELS.forEach(function (n) {
            var p = document.getElementById("panel-" + n);
            if (!p) return;
            var home = mobile ? dom.sheetBody : document.getElementById(PANEL_HOME[n]);
            if (home && p.parentNode !== home) home.appendChild(p);
        });
        if (!mobile && sheetName) setSheet(null);
        updateRoseOverlay();
    }

    function setSheet(name) {
        sheetName = name;
        var title = "";
        PANELS.forEach(function (n) {
            var p = document.getElementById("panel-" + n);
            if (p) p.classList.toggle("sheet-active", n === name);
            var b = dom.dock && dom.dock.querySelector('button[data-panel="' + n + '"]');
            if (b) {
                b.setAttribute("aria-pressed", n === name ? "true" : "false");
                if (n === name) { var l = b.querySelector("span"); title = l ? l.textContent : n; }
            }
        });
        if (dom.sheet) dom.sheet.hidden = !name;
        if (dom.sheetTitle) dom.sheetTitle.textContent = title;
        dom.app.classList.toggle("sheet-open", !!name);
        if (name === "chat") { markChatUnread(false); dom.chat.scrollTop = dom.chat.scrollHeight; }
        if (name === "abilities") renderAbilities();   // refresh cooldown/mana greying on open
    }
    function chatVisible() {
        if (!hudOn) return false;
        return mqMobile.matches ? sheetName === "chat" : activeTab === "chat";
    }
    function abilitiesVisible() {
        if (!hudOn) return false;
        return mqMobile.matches ? sheetName === "abilities" : activeTab === "abilities";
    }
    function markChatUnread(on) {
        ['#hud-dock button[data-panel="chat"]', '#hud-tabs button[data-tab="chat"]'].forEach(function (sel) {
            var b = document.querySelector(sel);
            if (b) b.classList.toggle("unread", !!on);
        });
    }
    function setCol(side, open, persist) {
        dom.app.classList.toggle(side === "left" ? "l-closed" : "r-closed", !open);
        var btn = document.getElementById(side === "left" ? "col-left" : "col-right");
        if (btn) btn.setAttribute("aria-pressed", open ? "true" : "false");
        if (persist !== false) {
            try { localStorage.setItem(side === "left" ? "ishar.colL" : "ishar.colR", open ? "1" : "0"); } catch (e) {}
        }
        api.onLayoutChange();
    }
    function setTab(name) {
        activeTab = name;
        ["status", "abilities", "chat", "who"].forEach(function (n) {
            var p = document.getElementById("panel-" + n);
            if (p) p.classList.toggle("tab-active", n === name);
            var b = document.querySelector('#hud-tabs button[data-tab="' + n + '"]');
            if (b) b.classList.toggle("active", n === name);
        });
        if (name === "chat") { markChatUnread(false); dom.chat.scrollTop = dom.chat.scrollHeight; }
        if (name === "abilities") renderAbilities();   // refresh cooldown/mana greying on open
        try { localStorage.setItem("ishar.tab", name); } catch (e) {}
    }
    function setHud(on, persist) {
        hudOn = on;
        dom.app.classList.toggle("hud-on", on);
        dom.app.classList.toggle("hud-off", !on);
        var btn = document.getElementById("ui-toggle");
        if (btn) {
            btn.setAttribute("aria-pressed", on ? "true" : "false");
            var label = btn.querySelector(".ui-toggle-label") || btn;
            label.textContent = on ? (btn.getAttribute("data-label-on") || "Hide UI") : (btn.getAttribute("data-label-off") || "Show UI");
        }
        if (persist !== false) { try { localStorage.setItem("ishar.hud", on ? "1" : "0"); } catch (e) {} }
        updateRoseOverlay();
        api.onLayoutChange();
    }
    function setConnected(on) { S.connected = !!on; renderVitals(); }

    function restorePrefs() {
        var saved = null, tab = null, colL = null, colR = null, rose = null;
        try {
            saved = localStorage.getItem("ishar.hud");
            tab = localStorage.getItem("ishar.tab");
            colL = localStorage.getItem("ishar.colL");
            colR = localStorage.getItem("ishar.colR");
            rose = localStorage.getItem("ishar.roseOverlay");
        } catch (e) {}
        if (tab && ["status", "abilities", "chat", "who"].indexOf(tab) !== -1) activeTab = tab;
        roseOverlayOn = rose !== "0";
        setHud(saved !== "0");
        setTab(activeTab);
        setCol("left", colL != null ? colL === "1" : mqWide.matches, false);
        setCol("right", colR != null ? colR === "1" : true, false);
    }

    // ------------------------------------------------------------------
    // Lifecycle
    // ------------------------------------------------------------------
    function renderAll() {
        renderVitals(); renderRoom(); renderOccupants(); renderGroup(); renderEquipment(); renderInventory();
        renderTrain(); renderStatus(); renderWho(); renderChat(); renderHotbar(); renderAbilities();
    }
    function reset() {
        S.vitals = null; S.status = null; S.time = null; S.room = null;
        S.equipment = []; S.inventory = null; S.train = null;
        S.affects = null; S.group = null; S.who = null; S.occupants = [];
        S.skills = []; S.cooldownExpiry = {}; S.usable = {};
        S.tgtHostile = null; S.tgtFriendly = null;
        lastVitalsBody = null;
        renderAll();
    }

    function init(opts) {
        opts = opts || {};
        if (opts.send) api.send = opts.send;
        if (opts.prefill) api.prefill = opts.prefill;
        if (opts.onLayoutChange) api.onLayoutChange = opts.onLayoutChange;
        if (opts.onComm) api.onComm = opts.onComm;

        dom.app = document.getElementById("connect-app");
        dom.vitals = document.getElementById("vitals-bar");
        dom.room = document.getElementById("panel-room");
        dom.occupants = document.getElementById("panel-occupants");
        dom.group = document.getElementById("panel-group");
        dom.equipment = document.getElementById("panel-equipment");
        dom.inventory = document.getElementById("panel-inventory");
        dom.train = document.getElementById("panel-train");
        dom.status = document.getElementById("panel-status");
        dom.abilities = document.getElementById("panel-abilities");
        dom.chat = document.getElementById("panel-chat");
        dom.who = document.getElementById("panel-who");
        dom.hotbar = document.getElementById("hud-hotbar");
        dom.dock = document.getElementById("hud-dock");
        dom.sheet = document.getElementById("hud-sheet");
        dom.sheetBody = document.getElementById("hud-sheet-body");
        dom.sheetTitle = document.getElementById("hud-sheet-title");
        dom.menu = document.getElementById("hud-menu");
        dom.roseOverlay = document.getElementById("rose-overlay");

        dom.app.addEventListener("click", onAppClick);
        dom.app.addEventListener("contextmenu", onAppContext);

        var tabs = document.getElementById("hud-tabs");
        if (tabs) tabs.addEventListener("click", function (e) {
            var b = e.target.closest("button[data-tab]");
            if (b) setTab(b.getAttribute("data-tab"));
        });

        var toggle = document.getElementById("ui-toggle");
        if (toggle) toggle.addEventListener("click", function () {
            if (hudOn && sheetName) setSheet(null);
            setHud(!hudOn);
        });

        if (dom.dock) dom.dock.addEventListener("click", function (e) {
            var b = e.target.closest("button[data-panel]");
            if (b) { var n = b.getAttribute("data-panel"); setSheet(n === sheetName ? null : n); }
        });
        var sheetClose = document.getElementById("hud-sheet-close");
        if (sheetClose) sheetClose.addEventListener("click", function () { setSheet(null); });

        // Mobile rose overlay toggle button.
        var roseBtn = document.getElementById("rose-toggle");
        if (roseBtn) roseBtn.addEventListener("click", function () {
            roseOverlayOn = !roseOverlayOn;
            try { localStorage.setItem("ishar.roseOverlay", roseOverlayOn ? "1" : "0"); } catch (e) {}
            roseBtn.setAttribute("aria-pressed", roseOverlayOn ? "true" : "false");
            updateRoseOverlay();
        });

        // Outside tap dismisses the sheet and any open menu.
        document.addEventListener("click", function (e) {
            if (menuOpen && !dom.menu.contains(e.target) && !e.target.closest("[data-menu],.row-more")) closeMenu();
            if (!sheetName || !mqMobile.matches) return;
            if (dom.sheet.contains(e.target) || dom.dock.contains(e.target)) return;
            if (dom.menu.contains(e.target)) return;
            setSheet(null);
        });

        var colBtns = { left: document.getElementById("col-left"), right: document.getElementById("col-right") };
        ["left", "right"].forEach(function (side) {
            if (colBtns[side]) colBtns[side].addEventListener("click", function () {
                setCol(side, colBtns[side].getAttribute("aria-pressed") !== "true");
            });
        });

        placePanels();
        var onMq = function () { placePanels(); api.onLayoutChange(); };
        if (mqMobile.addEventListener) mqMobile.addEventListener("change", onMq);
        else if (mqMobile.addListener) mqMobile.addListener(onMq);

        restorePrefs();
        renderAll();

        setInterval(function () {
            var t = now();
            var times = dom.status.querySelectorAll(".aff-time[data-expiry]");
            if (times.forEach) times.forEach(function (e) {
                e.textContent = fmtDur(parseFloat(e.getAttribute("data-expiry")) - t);
            });
            if (S.skills.length) tickHotbar();
        }, 1000);
    }

    // ------------------------------------------------------------------
    // Demo mode (/connect?demo=1)
    // ------------------------------------------------------------------
    function demo() {
        setHud(true, false);
        // Demo mana costs are % of maxmp (300); the exact `mana` field is what
        // the client now gates on (issue #1801). Demo mp is set below so a few
        // pricier spells (e.g. sanctuary) read as "mana"-blocked.
        var bigSkills = [
            { id: 1, name: "fireball", type: "spell", percent: 91, usable: true, category: "damage", target_type: "offensive", mana_pct: 30, mana: 90, min_position: "Standing" },
            { id: 2, name: "heal", type: "spell", percent: 78, usable: true, category: "heal", target_type: "defensive", mana_pct: 40, mana: 120, min_position: "Standing" },
            { id: 3, name: "kick", type: "skill", percent: 65, usable: false, category: "damage", target_type: "none", min_position: "Fighting" },
            { id: 4, name: "meditate", type: "skill", percent: 50, usable: true, category: "misc", target_type: "none", min_position: "Sitting" },
            { id: 5, name: "lightning bolt", type: "spell", percent: 88, usable: true, category: "damage", target_type: "offensive", mana_pct: 25, mana: 75, min_position: "Standing" },
            { id: 6, name: "cure serious", type: "spell", percent: 82, usable: true, category: "heal", target_type: "defensive", mana_pct: 20, mana: 60, min_position: "Standing" },
            { id: 7, name: "bless", type: "spell", percent: 70, usable: true, category: "misc", target_type: "defensive", mana_pct: 15, mana: 45, min_position: "Standing" },
            { id: 8, name: "sanctuary", type: "spell", percent: 60, usable: true, category: "misc", target_type: "defensive", mana_pct: 50, mana: 150, min_position: "Standing" },
            { id: 9, name: "disarm", type: "skill", percent: 45, usable: true, category: "damage", target_type: "none", min_position: "Fighting" },
            { id: 10, name: "second attack", type: "passive", percent: 75, usable: false, category: "misc", target_type: "none", min_position: "Standing" },
            { id: 91, name: "Metamagic: Clarity", type: "skill", percent: 100, usable: true, category: "misc", target_type: "none", min_position: "Standing" },
            { id: 92, name: "Shield Slam", type: "skill", percent: 72, usable: true, category: "damage", target_type: "none", min_position: "Fighting" }
        ];
        // Pad to demonstrate the immortal overflow the browser now bounds.
        for (var i = 11; i <= 90; i++) bigSkills.push({ id: i, name: "spell " + i, type: (i % 3 ? "spell" : "skill"), percent: 40 + (i % 60), usable: (i % 4 !== 0), category: ["damage", "heal", "misc"][i % 3], target_type: ["offensive", "defensive", "none"][i % 3], mana_pct: 20 + (i % 40), mana: (20 + (i % 40)) * 3, min_position: "Standing" });

        var feeds = {
            "Char.Status": { name: "Aelwyn", "class": "Magician", race: "Elf", position: "Standing", level: 45, align: 350, xp: 1250000, tnl: 48000, gold: 18230, bank: 500000, remort: 3 },
            "Char.Vitals": { hp: 412, maxhp: 480, mp: 130, maxmp: 300, move: 198, maxmove: 240, position: "Standing", opponent_hp_pct: 35, metamagic: 60, metamagic_max: 100, metamagic_regen: 5 },
            "Game.Time": { hour: 21, hour12: 9, ampm: "pm", day: 14, day_name: "Sunday", month: 6, month_name: "the Long Shadows", year: 1247, night: true, season_id: 15, season_end: 0, events: [{ name: "Double Essence", seconds: 5400 }, { name: "Festival of Flames" }], moons: [{ name: "Shavar", phase: 4, phase_name: "full", up: true }, { name: "Chenchir", phase: 6, phase_name: "last quarter", up: true }] },
            "Room.Info": { num: 3001, name: "The Grand Concourse", area: "Ishar Nexus", environment: "City", exits: { n: 3002, e: 3005, s: 3008, w: 3010, u: 3100, d: 3200, into: 3500 } },
            "Room.Occupants": { occupants: [
                { keyword: "guard", short_desc: "a towering city guard", handle: "1.guard", is_player: false, is_dead: false, is_shopkeeper: false, hostile_hint: "neutral", position: "Standing", is_loyal_follower: false, is_my_follower: false, fighting_you: false, is_your_target: false },
                { keyword: "pigeon", short_desc: "a small grey pigeon", handle: "1.pigeon", is_player: false, is_dead: false, is_shopkeeper: false, hostile_hint: "neutral", position: "Standing", is_loyal_follower: false, is_my_follower: false, fighting_you: false, is_your_target: false },
                { keyword: "thug", short_desc: "a scarred alley thug", handle: "1.thug", is_player: false, is_dead: false, is_shopkeeper: false, hostile_hint: "hostile", position: "Standing", is_loyal_follower: false, is_my_follower: false, fighting_you: false, is_your_target: true, fighting: "1.Boric" },
                { keyword: "bandit", short_desc: "a wiry crossroads bandit", handle: "1.bandit", is_player: false, is_dead: false, is_shopkeeper: false, hostile_hint: "hostile", position: "Standing", is_loyal_follower: false, is_my_follower: false, fighting_you: true, is_your_target: false },
                { keyword: "merchant", short_desc: "Hadeon the curio merchant", handle: "1.merchant", is_player: false, is_dead: false, is_shopkeeper: true, hostile_hint: "neutral", position: "Standing", is_loyal_follower: false, is_my_follower: false, fighting_you: false, is_your_target: false },
                { keyword: "Boric", short_desc: "Boric, Shield of the Dawn", handle: "1.Boric", is_player: true, is_dead: false, is_shopkeeper: false, hostile_hint: "friendly", position: "Standing", is_loyal_follower: false, is_my_follower: false, fighting_you: false, is_your_target: false, fighting: "1.thug" },
                { keyword: "Selra", short_desc: "Selra the Quiet", handle: "1.Selra", is_player: true, is_dead: false, is_shopkeeper: false, hostile_hint: "friendly", position: "Sleeping", is_loyal_follower: false, is_my_follower: false, fighting_you: false, is_your_target: false },
                { keyword: "wolf", short_desc: "a large timber wolf", handle: "1.wolf", is_player: false, is_dead: false, is_shopkeeper: false, hostile_hint: "friendly", position: "Resting", is_loyal_follower: true, is_my_follower: true, fighting_you: false, is_your_target: false },
                { keyword: "rat", short_desc: "the corpse of a sewer rat", handle: "1.rat", is_player: false, is_dead: true, is_shopkeeper: false, hostile_hint: "neutral", position: "Dead", is_loyal_follower: false, is_my_follower: false, fighting_you: false, is_your_target: false }
            ] },
            "Char.Equipment": { items: [
                { name: "a magnificent helmet of red dragonscales", keywords: "helmet dragonscales", type: "armor", vnum: 1, location: "Head", condition: 100 },
                { name: "emberforged gauntlets", keywords: "gauntlets emberforged", type: "armor", vnum: 2, location: "Hands", condition: 62 },
                { name: "a talon-barbed whip", keywords: "whip talon", type: "weapon", vnum: 3, location: "Wielding", condition: 35 },
                { name: "a sturdy traveling pack", keywords: "pack traveling", type: "container", vnum: 4, location: "Back", closeable: true, closed: false, contents: [
                    { name: "a flask of lamp oil", keywords: "flask oil", count: 2 },
                    { name: "a coil of silk rope", keywords: "rope silk coil", count: 1 }
                ] },
                { name: "a rune-locked coffer", keywords: "coffer runelocked", type: "container", vnum: 5, location: "Held", closeable: true, closed: true, locked: true }
            ] },
            "Char.Inventory": { items: [
                { name: "a glowing potion", keywords: "potion glowing", type: "potion", vnum: 10, count: 3 },
                { name: "a scroll of recall", keywords: "scroll recall", type: "scroll", vnum: 12, count: 1 },
                { name: "a leather sack", keywords: "sack leather", type: "container", vnum: 11, count: 1, closeable: true, closed: false, contents: [{ name: "a brass key", keywords: "key brass", count: 1 }] }
            ], coins: [{ name: "gold", vnum: 0, count: 18230 }, { name: "silver", vnum: 0, count: 340 }, { name: "obsidian", vnum: 0, count: 12 }], components: [
                { name: "a pinch of sulfur", keywords: "sulfur pinch", count: 7 },
                { name: "a vial of powdered silver", keywords: "silver vial powdered", count: 3 },
                { name: "a sprig of nightshade", keywords: "nightshade sprig", count: 12 },
                { name: "a shard of frost quartz", keywords: "quartz frost shard", count: 5 }
            ] },
            "Char.Affects": { buffs: [{ name: "Stoneskin", id: 101, duration: 1800 }, { name: "Haste", id: 102, duration: 240 }], debuffs: [{ name: "Poison", id: 201, duration: 45 }], maintained: [{ name: "Detect Invisibility", id: 301, duration: 600, target: "self" }, { name: "Shroud", id: 302, duration: 900, target: "Boric", skill: "shroud", handle: "1.boric", releasable: true }] },
            "Group.Update": { leader: "Aelwyn", size: 3, members: [
                { name: "Aelwyn", level: 45, hp_pct: 86, mp_pct: 85, mv_pct: 82, position: "Standing", race: "Elf", "class": "Magician", leader: true, in_room: true, is_tank: false, fighting: "a wiry crossroads bandit", threat: 40, tank_threat: 55, threat_level: "warn" },
                { name: "Boric", level: 43, hp_pct: 60, mp_pct: 40, mv_pct: 75, position: "Standing", race: "Dwarf", "class": "Warrior", leader: false, in_room: true, is_tank: true, fighting: "a scarred alley thug", threat: 120 },
                { name: "Selra", level: 41, hp_pct: 95, mp_pct: 90, mv_pct: 88, position: "Sleeping", race: "Human", "class": "Cleric", leader: false, in_room: true, is_tank: false }
            ], allies: [
                { name: "a large timber wolf", owner: "Aelwyn", hp_pct: 72, mp_pct: 100, mv_pct: 95, position: "Resting", in_room: true, is_tank: false }
            ] },
            "Char.Skills": { skills: bigSkills },
            "Char.Cooldowns": { cooldowns: [{ id: 3, remaining: 8 }], usable: { "3": false } },
            "Char.Train": { stats: [{ name: "Str", value: 18, add: 2 }, { name: "Int", value: 25 }, { name: "Wis", value: 20 }], xp: 1250000, xp_pct: 62, can_advance: true, aux: [{ name: "Crit", value: "12.5% (+2%)" }], resources: [{ name: "Practices", value: 5, max: 10 }, { name: "Trains", value: 2, max: 2 }] }
        };
        Object.keys(feeds).forEach(function (k) { onGmcp(k, JSON.stringify(feeds[k])); });
        [
            { channel: "gossip", text: "Boric: anyone up for a UDN run?" },
            { channel: "auction", text: "WTS dragonscale helm, pst" },
            { channel: "newbie", text: "Mage: how do I cast spells?" }
        ].forEach(function (c) { onGmcp("Comm.Channel", JSON.stringify(c)); });
        setConnected(true);
    }

    window.IsharHUD = { init: init, onGmcp: onGmcp, reset: reset, setConnected: setConnected, completions: completions, demo: demo };
})();
