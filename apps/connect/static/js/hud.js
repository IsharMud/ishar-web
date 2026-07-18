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
    var QUICKBAR_MAX = 12;   // suggestions shown in "auto" mode (nothing pinned yet)
    // WoW-style action bar: fixed, numbered, hotkey-addressable slots. Two pages
    // of ten (Alt/Ctrl+1..0 fire the visible page); slot 10 is keyed "0".
    var SLOTS_PER_PAGE = 10;
    var SLOT_PAGES = 2;
    var SLOT_MAX = SLOTS_PER_PAGE * SLOT_PAGES;   // 20 assignable slots
    var SVGNS = "http://www.w3.org/2000/svg";
    var XLINKNS = "http://www.w3.org/1999/xlink";

    // ------------------------------------------------------------------
    // State
    // ------------------------------------------------------------------
    var S = {
        vitals: null, status: null, time: null, room: null,
        equipment: [], inventory: null, train: null,
        affects: null, group: null, who: null, occupants: [],
        // Room.Contents — ground objects (corpses, drops, containers) and
        // active harvest nodes; rendered under the occupants in the Room panel.
        roomItems: [], roomNodes: [],
        skills: [], cooldownExpiry: {}, cooldownTotal: {}, usable: {},
        professions: [], recipes: [], craft: null,
        chat: [], connected: false,
        // Default targets (from Room.Occupants) that make the hotbar
        // target-aware: offensive spells → hostile, defensive → beneficial.
        tgtHostile: null, tgtFriendly: null
    };

    // Persisted client prefs (localStorage): the action-bar slot assignments,
    // per-skill icon overrides, collapsed panels, and Abilities-browser filters.
    var slots = loadSlots();                  // sparse array, index 0..SLOT_MAX-1 -> skill key
    var iconOverrides = loadMap("ishar.icons"); // per-player pick: skill key -> game-icons name
    var curatedIcons = {};                     // site-shipped standardized map: skill id -> icon (set in init)
    var hotbarPage = 0;                        // which page of ten is visible
    // Action-bar lock (WoW-style): locked (default) fires on tap/hotkey and can't
    // be dragged; unlocked is edit mode — taps rearrange instead of firing.
    var barLocked = localStorage.getItem("ishar.barUnlocked") !== "1";
    var pickedSlot = null;                     // tap-to-swap source (edit mode)
    var spriteUrl = "";                        // game-icons sprite URL (set in init)
    var biUrl = "";                            // Bootstrap Icons sprite URL (set in init)
    var collapsed = loadSet("ishar.collapsed");
    // Which containers the player has expanded to view. Packs start COLLAPSED
    // (default absent = closed): a carried bag shouldn't spill its whole
    // contents into the inventory view unasked.
    var expanded = loadSet("ishar.itemsExpanded");
    var abilityFilter = { q: "", type: "all", usableOnly: false };
    try {
        var af = JSON.parse(localStorage.getItem("ishar.abilityFilter"));
        if (af && typeof af === "object") {
            // Legacy "fav" filter is now "bar" (on the action bar).
            if (typeof af.type === "string") abilityFilter.type = (af.type === "fav" ? "bar" : af.type);
            if (typeof af.usableOnly === "boolean") abilityFilter.usableOnly = af.usableOnly;
        }
    } catch (e) {}

    var api = { send: function () {}, prefill: function () {}, onLayoutChange: function () {}, onComm: function () {}, onVitals: function () {} };
    var dom = {};
    // The map subsystem (hud-map.js) plugs in through registerMap() — the
    // whole mapper stays behind this one seam so a missing/stale-cached
    // hud-map.js degrades to the rose-only HUD.
    var mapMod = null;
    var roseTab = "rose";   // "rose" | "map" — pinned Room-panel tab
    try { if (localStorage.getItem("ishar.roseTab") === "map") roseTab = "map"; } catch (e) {}
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
                  "status", "abilities", "chat", "who", "professions", "map"];
    var PANEL_HOME = {
        occupants: "hud-left-scroll", equipment: "hud-left-scroll",
        inventory: "hud-left-scroll", train: "hud-left-scroll",
        group: "hud-left-scroll",
        room: "hud-left",
        status: "hud-right", abilities: "hud-right", chat: "hud-right", who: "hud-right",
        professions: "hud-overlay-body", map: "hud-overlay-body"
    };

    // ------------------------------------------------------------------
    // Overlay apps — the micro-menu registry, THE single point of extension
    // for transient HUD surfaces (docs/design/decisions.md 2026-07-17: the
    // HUD extension model). Each entry needs: a [data-overlay=key] button in
    // #hud-micro, a [data-panel=key] dock button, a #panel-<key> node inside
    // #hud-overlay-body, and PANELS/PANEL_HOME entries. Desktop opens the
    // #hud-overlay window; phones open the same panel in the bottom sheet.
    // Hotkeys are Ctrl+<letter>, strict single-modifier.
    // ------------------------------------------------------------------
    // Reserved hotkey letters (never register these): "l" (Ctrl+L clears the
    // terminal — bound in connect.html and would be silently shadowed since
    // this handler runs first). Ctrl+<letter> may shadow a browser default
    // (Ctrl+P = print) — deliberate, and only while the app is available.
    var OVERLAYS = [
        { key: "professions", title: "Professions", hotkey: "p",
          render: function () { renderProfessions(); },
          // The activity bar must stay reachable even in the (theoretical)
          // no-professions-but-harvesting state.
          available: function () { return (S.professions || []).length > 0 || !!S.craft; } },
        { key: "map", title: "Map", hotkey: "m",
          render: function () { if (mapMod) mapMod.renderOverlay(); },
          // Account-gated: guests map nothing, so they get no launcher.
          available: function () { return !!(mapMod && mapMod.enabled()); } }
    ];
    var overlayName = null;   // open overlay app key (desktop), or null

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
        weapon: "wield", armor: "wear", wand: "use", staff: "use", light: "hold",
        // `use <tome>` learns the recipe/skill it holds; `draw <deck>` pulls a
        // card from the Fateweaver's Deck. Both resolve from inventory.
        tome: "use", deck: "draw"
    };
    var TYPE_VERB_LABEL = {
        quaff: "Quaff", recite: "Recite", eat: "Eat", drink: "Drink",
        wield: "Wield", wear: "Wear", use: "Use", hold: "Hold", draw: "Draw"
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
    function loadMap(key) {
        try { var m = JSON.parse(localStorage.getItem(key)); if (m && typeof m === "object" && !Array.isArray(m)) return m; } catch (e) {}
        return {};
    }
    function saveMap(key, m) { try { localStorage.setItem(key, JSON.stringify(m)); } catch (e) {} }

    // Action-bar slots persist as an array of skill keys (null = empty). On first
    // run we migrate the legacy unordered favorites set into ordered slots so a
    // returning player keeps their pins.
    function loadSlots() {
        try {
            var raw = localStorage.getItem("ishar.slots");
            if (raw != null) {
                var a = JSON.parse(raw);
                if (Array.isArray(a)) return a.slice(0, SLOT_MAX).map(function (x) { return (typeof x === "string" && x) ? x : null; });
            }
            var fav = JSON.parse(localStorage.getItem("ishar.favs"));
            if (Array.isArray(fav)) {
                var m = fav.filter(function (x) { return typeof x === "string" && x; })
                           .map(function (x) { return x.toLowerCase(); }).slice(0, SLOT_MAX);
                localStorage.setItem("ishar.slots", JSON.stringify(m));
                return m;
            }
        } catch (e) {}
        return [];
    }
    function saveSlots() {
        try { localStorage.setItem("ishar.slots", JSON.stringify(slots.map(function (x) { return x || null; }))); } catch (e) {}
    }
    function slotKeyOf(s) { return nameOf(s && s.name).toLowerCase(); }
    function slotIndexOf(key) { for (var i = 0; i < slots.length; i++) if (slots[i] === key) return i; return -1; }
    function onBar(key) { return slotIndexOf(key) !== -1; }
    function firstEmptySlot() { for (var i = 0; i < SLOT_MAX; i++) if (!slots[i]) return i; return -1; }
    // The human "1..0" label for a slot index on its page.
    function slotLabel(i) { var n = (i % SLOTS_PER_PAGE) + 1; return n === 10 ? "0" : String(n); }
    function pageOfIndex(i) { return Math.floor(i / SLOTS_PER_PAGE); }
    function anyAssigned() { for (var i = 0; i < slots.length; i++) if (slots[i]) return true; return false; }

    // Pin/unpin a skill on the bar (toggle its presence).
    function toggleSlot(name) {
        var key = nameOf(name).toLowerCase();
        var cur = slotIndexOf(key);
        if (cur !== -1) { slots[cur] = null; }
        else { var e = firstEmptySlot(); if (e !== -1) slots[e] = key; else if (slots.length < SLOT_MAX) slots.push(key); else return; }
        saveSlots(); renderHotbar(); renderAbilities();
    }
    // Drop a skill onto an explicit slot index (drag, or "Assign to slot N").
    function assignSlot(idx, key) {
        if (idx < 0 || idx >= SLOT_MAX || !key) return;
        var cur = slotIndexOf(key);
        var occupant = slots[idx] || null;
        if (cur !== -1) slots[cur] = occupant;   // swap if the source was already on the bar
        slots[idx] = key;
        saveSlots(); renderHotbar(); renderAbilities();
    }
    function clearSlot(idx) { if (slots[idx]) { slots[idx] = null; saveSlots(); renderHotbar(); renderAbilities(); } }
    // Nudge a slot left/right within the bar (swaps with the neighbour).
    function moveSlot(idx, dir) {
        var j = idx + dir;
        if (j < 0 || j >= SLOT_MAX) return;
        var tmp = slots[idx]; slots[idx] = slots[j] || null; slots[j] = tmp;
        saveSlots(); renderHotbar(); renderAbilities();
    }

    // ------------------------------------------------------------------
    // Skill icons (game-icons.net, CC BY 3.0, self-hosted sprite)
    // ------------------------------------------------------------------
    // The game sends no icon metadata, so we map client-side: a user override
    // wins, else the first keyword rule to match the (color-stripped, lowercased)
    // skill name, else a type/category fallback. This SAME table is mirrored by
    // scratchpad/iconset.js, which the sprite generator reads — every name below
    // is guaranteed present in game-icons.svg.
    var ICON_RULES = [
        [/fireball|meteor|fire ?storm|flame ?strike|firewall/, "fireball"],
        [/frost ?fire/, "frostfire"],
        [/fire|flame|flaming|burn|blaz|inferno|pyro|scorch|ignit|ember|cinder|combust/, "fire"],
        [/blizzard|snow/, "snowflake-1"],
        [/ice|frost|freez|cold|glaci|chill|hail|winter|rime|frigid/, "ice-bolt"],
        [/chain ?light/, "chain-lightning"],
        [/storm|tempest/, "lightning-storm"],
        [/lightn|shock|thunder|electr|volt|spark|static|arc\b/, "lightning-arc"],
        [/acid|corros|melt|dissolve/, "acid"],
        [/disease|plague|infect|\brot\b|pestilence|contagi|fester/, "poison-cloud"],
        [/poison|venom|toxic|toxin|noxious|virulen/, "poison-bottle"],
        [/water|wave|tide|aqua|drown|tsunami|deluge|torrent/, "water-drop"],
        [/tornado|cyclone|whirlwind|vortex|hurricane/, "tornado"],
        [/wind|\bair\b|gust|gale|breeze|zephyr/, "wind-hole"],
        [/earth|stone|\brock\b|quake|boulder|tremor|seismic|granite/, "earth-crack"],
        [/regen|rejuven|regrow|sustain/, "regeneration"],
        [/heal|cure|mend|renew|restor|recover|salv|remedy|soothe/, "healing"],
        [/resurrect|revive|raise dead|\blife\b|vitalit|\bres\b/, "caduceus"],
        [/bless|blessing|benedict|\bboon\b/, "prayer"],
        [/holy|divine|sacred|consecrat|sanctif|celestial|righteous|hallow/, "holy-symbol"],
        [/\bsun\b|sunlight|radian|dawn|solar|lumin|\bglow\b/, "sunbeams"],
        [/curse|hex|doom|blight|wither|decay|afflict|malediction/, "cursed-star"],
        [/necro|death|\bdead\b|grave|corpse|\bsoul\b|drain|siphon|leech|vampir|\breap/, "death-skull"],
        [/dark|shadow|night|umbral|gloom|\bblack\b/, "evil-wings"],
        [/fear|terror|horror|dread|panic|scare|fright/, "spectre"],
        [/mind|psych|psion|charm|dominat|hypno|mesmer|confus|sleep|slumber|daze|beguile|enthrall/, "psychic-waves"],
        [/stone ?skin|bark ?skin|iron ?skin/, "aura"],
        [/sanctuar|globe|barrier|\bward\b|aegis|bulwark/, "energy-shield"],
        [/armor|armour|\bplate\b|carapace|\bhide\b|toughness|hardskin/, "armor-vest"],
        [/shield|protect|\bguard\b|defen|shelter/, "shield"],
        [/haste|speed|swift|quick|celerity|hasten|fleet|nimble/, "sprint"],
        [/\bfly\b|levit|feather|soar|\bwing/, "angel-wings"],
        [/teleport|blink|recall|\bgate\b|dimension|translocat|portal/, "magic-gate"],
        [/summon|conjur|beckon/, "portal"],
        [/detect|scry|\bsense\b|reveal|truesight|identif|locate|farsight|clairvoy|augury/, "all-seeing-eye"],
        [/invis|vanish|shroud|unseen/, "invisible"],
        [/hide|sneak|stealth|camoufl|prowl|conceal/, "hidden"],
        [/backstab|assassin|ambush|garrote/, "stiletto"],
        [/steal|pick ?pocket|pilfer|thiev|filch|purloin|palm/, "plain-dagger"],
        [/dual|whirl|flurry|\bcombo\b|multi ?(hit|attack)|barrage/, "crossed-swords"],
        [/slash|slice|cleav|\bhack\b|\brend\b|lacerat/, "saber-slash"],
        [/sword|blade|parry|riposte|fenc|thrust|pierce|\bstab\b|impale|lunge|skewer/, "pointy-sword"],
        [/\baxe\b|chop|\bhew\b/, "sharp-axe"],
        [/hammer|\bmace\b|blunt|smash|crush|\bmaul\b|pound|pulver/, "flat-hammer"],
        [/bash|\bslam\b|shatter/, "shield-reflect"],
        [/spear|lance|polearm|halberd|\bpike\b|javelin|glaive/, "spear-hook"],
        [/crossbow/, "crossbow"],
        [/\bbow\b|arrow|shoot|archer|ranged|volley|snipe|marksman|fletch/, "pocket-bow"],
        [/dagger|knife|\bdirk\b/, "plain-dagger"],
        [/kick|roundhouse|stomp/, "high-kick"],
        [/punch|\bjab\b|fist|martial|brawl|pummel|uppercut|\bstrike\b/, "punch"],
        [/dodge|evade|deflect|\bblock\b/, "vibrating-shield"],
        [/rage|berserk|fury|frenzy|enrage|bloodlust|\bwrath\b/, "muscle-up"],
        [/shout|\byell\b|war ?cry|battle ?cry|\broar\b|\bhowl\b|bellow|scream|taunt/, "sonic-shout"],
        [/disarm|\btrip\b|feint|sunder|\bbreak\b/, "sword-clash"],
        [/thorn|\bvine\b|entangle|\broot\b|bramble/, "thorny-vine"],
        [/nature|\bplant\b|druid|grove|forest|\bbloom\b|sprout|\bseed\b/, "sprout"],
        [/\bleaf\b|petal|pollen|\bspore/, "leaf-swirl"],
        [/beast|animal|\bpet\b|companion|\btame\b|feral/, "wolf-howl"],
        [/\bwolf\b|\bbear\b|\bhawk\b|falcon|serpent/, "beast-eye"],
        [/\bclaw|talon|\bbite\b|\bfang/, "claw-slashes"],
        [/bleed|hemorrh|\bwound\b|\bgash\b/, "bleeding-wound"],
        [/\bbone\b|skeleton|marrow/, "broken-bone"],
        [/enchant|imbue|inscri|\brune\b|glyph|sigil|empower|augment/, "rune-stone"],
        [/brew|alchem|potion|distil|concoct|elixir|philter/, "bubbling-flask"],
        [/forge|smith|anvil|temper|reforge/, "anvil"],
        [/craft|\bmake\b|create|\bbuild\b|construct|assemble|fashion/, "hammer-nails"],
        [/\bsew\b|tailor|weav|stitch|\bknit\b|leatherwork/, "sewing-needle"],
        [/\bmine\b|\bdig\b|excavat|prospect|\bore\b/, "gold-nuggets"],
        [/cook|bake|roast/, "cauldron"],
        [/\bgem\b|jewel|crystal|prism|facet/, "gems"],
        [/scroll|scribe|transcri/, "scroll-unfurled"],
        [/meditat|focus|concentrat|trance|commune|contemplat|\bcenter\b/, "meditation"],
        [/spell ?book|\bstudy\b|\blore\b|grimoire|\btome\b|research/, "spell-book"],
        [/track|hunt|forage|surviv|scout|\btrail\b/, "footsteps"],
        [/magic|arcane|mystic|arcana|sorcer|wizard|\bmana\b|\bspell\b/, "magic-swirl"]
    ];
    function iconFallback(s) {
        var t = s.type, c = s.category;
        if (t === "craft") return "hammer-nails";
        if (t === "enchant") return "rune-stone";
        if (t === "passive") return "aura";
        if (t === "spell") return c === "damage" ? "magic-swirl" : c === "heal" ? "healing" : "sparkles";
        if (t === "skill") return c === "damage" ? "crossed-swords" : c === "heal" ? "bandage-roll" : "sword-brandish";
        return "round-star";
    }
    // The manual icon picker palette (themed groups). Every name ships in the sprite.
    var ICON_PALETTE = [
        ["Fire", ["fire", "fireball", "fire-bomb", "flaming-arrow", "celebration-fire", "burning-skull", "fire-ray"]],
        ["Ice & water", ["ice-bolt", "frozen-orb", "snowflake-1", "ice-cube", "frostfire", "water-drop"]],
        ["Storm & air", ["lightning-arc", "lightning-storm", "chain-lightning", "lightning-helix", "tornado", "wind-hole"]],
        ["Earth", ["earth-crack", "rock", "stone-spear"]],
        ["Poison & death", ["poison-bottle", "poison-gas", "poison-cloud", "acid", "acid-blob", "death-skull", "skull-crossed-bones", "crossed-bones", "cursed-star", "death-zone"]],
        ["Arcane", ["magic-swirl", "sparkles", "star-swirl", "wizard-staff", "magic-palm", "fairy-wand", "magick-trick", "rune-stone"]],
        ["Holy & shadow", ["holy-symbol", "sunbeams", "sun", "angel-wings", "prayer", "sun-priest", "evil-wings", "spectre", "psychic-waves"]],
        ["Healing", ["healing", "health-potion", "heart-plus", "first-aid-kit", "bandage-roll", "caduceus", "life-support", "holy-water", "health-normal", "heart-bottle", "regeneration", "meditation"]],
        ["Defense", ["shield", "checked-shield", "edged-shield", "armor-vest", "aura", "magic-shield", "energy-shield", "barrier", "shield-reflect", "vibrating-shield"]],
        ["Blades & weapons", ["pointy-sword", "sword-wound", "sword-brandish", "crossed-swords", "broadsword", "saber-slash", "sword-clash", "sharp-axe", "battle-axe", "flat-hammer", "gavel", "spear-hook", "thrown-spear", "pocket-bow", "high-shot", "crossbow", "plain-dagger", "stiletto", "bone-knife"]],
        ["Unarmed & fury", ["fist", "punch", "punch-blast", "high-kick", "boot-stomp", "muscle-up", "biceps", "sonic-shout"]],
        ["Stealth & travel", ["hidden", "ninja-mask", "cloak", "invisible", "sprint", "run", "walking-boot", "footsteps", "eye-target", "magnifying-glass", "all-seeing-eye", "sight-disabled", "portal", "teleport", "magic-gate"]],
        ["Nature & beast", ["sprout", "leaf-swirl", "thorny-vine", "vine-whip", "wolf-howl", "beast-eye", "claw-slashes", "bleeding-wound", "broken-bone"]],
        ["Craft & enchant", ["hammer-nails", "anvil", "anvil-impact", "blacksmith", "gears", "sewing-needle", "cauldron", "bubbling-flask", "potion-ball", "drink-me", "mortar", "gold-nuggets", "gems", "crystal-shine", "scroll-unfurled", "spell-book", "open-book"]],
        ["Creatures & forms", ["dragon-head", "dragon-breath", "tiger-head", "monkey", "eagle-head", "raven", "owl", "tortoise", "boar", "octopus", "cobra", "snake", "bear-head", "totem-head"]],
        ["Mind, time & spirit", ["brain", "third-eye", "psychic-waves", "hourglass", "burning-embers", "feathered-wing", "magic-portal", "shadow-follower", "prayer-beads", "templar-shield", "trident"]],
        ["Generic", ["round-star", "sparkles", "gears"]]
    ];
    // The set of icon names that actually ship in the sprite (derived from the
    // same rules/palette the generator reads), so a stale override, a curated-map
    // typo, or a future server value can be validated before it renders blank.
    var SPRITE_ICONS = (function () {
        var set = {};
        ICON_RULES.forEach(function (r) { set[r[1]] = true; });
        ["hammer-nails", "rune-stone", "aura", "magic-swirl", "healing", "sparkles",
         "crossed-swords", "bandage-roll", "sword-brandish", "round-star"].forEach(function (n) { set[n] = true; });
        ICON_PALETTE.forEach(function (g) { g[1].forEach(function (n) { set[n] = true; }); });
        return set;
    })();
    function hasIcon(n) { return !!(n && SPRITE_ICONS[n]); }

    // The keyword heuristic — the client-side fallback when nothing more
    // authoritative names the icon.
    function heuristicIcon(s) {
        var nm = nameOf(s.name).toLowerCase();
        for (var i = 0; i < ICON_RULES.length; i++) if (ICON_RULES[i][0].test(nm)) return ICON_RULES[i][1];
        return iconFallback(s);
    }
    // The standardized icon every player inherits, before any personal override.
    // Precedence: server-provided (future Char.Skills `icon` field, the eventual
    // authority) → the curated id-keyed map shipped by the site → keyword
    // heuristic → type/category fallback. See the 2026-07-16 decision.
    function standardIcon(s) {
        if (hasIcon(s.icon)) return s.icon;
        var cur = curatedIcons[slotKeyOf(s)];   // curated map keyed by normalized name
        if (hasIcon(cur)) return cur;
        return heuristicIcon(s);
    }
    // The final icon for a skill: a personal pick wins over everything, else the
    // standardized icon above.
    function iconName(s) {
        var ov = iconOverrides[slotKeyOf(s)];
        return hasIcon(ov) ? ov : standardIcon(s);
    }
    // Build an <svg><use> referencing the sprite. `name` is a fixed vocabulary
    // (rules/palette/fallback), but sanitize anyway so a stray value can't smuggle
    // markup into the href.
    function iconSvg(name, cls) {
        name = String(name || "").replace(/[^a-z0-9-]/g, "");
        var svg = document.createElementNS(SVGNS, "svg");
        svg.setAttribute("class", cls || "gi");
        svg.setAttribute("viewBox", "0 0 512 512");
        svg.setAttribute("aria-hidden", "true");
        var use = document.createElementNS(SVGNS, "use");
        var href = spriteUrl + "#gi-" + name;
        use.setAttributeNS(XLINKNS, "xlink:href", href);
        use.setAttribute("href", href);
        svg.appendChild(use);
        return svg;
    }

    // Build an <svg><use> referencing the self-hosted Bootstrap Icons sprite
    // (the same sprite the page chrome uses via {% bi %}). `name` is a fixed
    // vocabulary from this file, but sanitize anyway so a stray value can't
    // smuggle markup into the href. The symbol carries its own 0 0 16 16
    // viewBox, so — like {% bi %} — the wrapper sets none.
    function biSvg(name, cls) {
        name = String(name || "").replace(/[^a-z0-9-]/g, "");
        var svg = document.createElementNS(SVGNS, "svg");
        svg.setAttribute("class", cls || "bi");
        svg.setAttribute("aria-hidden", "true");
        var use = document.createElementNS(SVGNS, "use");
        var href = biUrl + "#" + name;
        use.setAttributeNS(XLINKNS, "xlink:href", href);
        use.setAttribute("href", href);
        svg.appendChild(use);
        return svg;
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
        (S.roomItems || []).forEach(addKeywords);
        (S.roomNodes || []).forEach(function (n) { String(n.keywords || "").split(/\s+/).forEach(add); });
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
                // Let the page decide on HP-based notifications (damage taken /
                // low-health) — it owns the tab-visibility + settings state.
                api.onVitals(data);
                tickHotbar();          // mana gate re-evaluates each pulse
                // The Abilities browser bakes the mana/position block state into
                // each row, so it must rebuild when mana changes (combat regen)
                // or a spell stays greyed after you can afford it (issue #1801).
                // Only when it's actually on screen — same guard the cooldown
                // path uses to avoid rebuilding a ~400-row list off-screen.
                if (abilitiesVisible()) renderAbilities();
                break;
            case "Char.Status": S.status = data; renderVitals(); renderStatus(); renderGroup(); break;
            case "Game.Time": S.time = data; renderVitals(); break;
            case "Room.Info":
                S.room = data; renderRoom();
                // Discovery accrual, zone-graph fetch, autowalk confirmation
                // and the visibility gate all hang off this one call.
                if (mapMod) mapMod.onRoom(data);
                break;
            case "Room.Occupants": applyOccupants(data); break;
            case "Room.Contents":
                S.roomItems = (data && data.items) || [];
                S.roomNodes = (data && data.nodes) || [];
                renderOccupants();
                break;
            case "Char.Equipment":
                S.equipment = (data && data.items) || []; renderEquipment(); renderInventory();
                // Craftable-now marks join against carried items.
                if (overlayVisible("professions")) renderProfessions();
                break;
            case "Char.Inventory":
                S.inventory = data; renderInventory(); renderEquipment();
                if (overlayVisible("professions")) renderProfessions();
                break;
            case "Char.Train": S.train = data; renderTrain(); break;
            case "Char.Affects": S.affects = data; stampAffectExpiry(data); renderStatus(); break;
            case "Group.Update":
                S.group = data; renderGroup();
                if (mapMod && mapMod.onGroup) mapMod.onGroup(data);
                break;
            case "Char.Death":
                if (mapMod && mapMod.onDeath) mapMod.onDeath(data);
                break;
            case "Char.Who": S.who = data; renderWho(); break;
            case "Char.Skills": S.skills = (data && data.skills) || []; renderHotbar(); renderAbilities(); break;
            case "Char.Professions": applyProfessions(data); break;
            case "Char.Recipes": S.recipes = (data && data.recipes) || []; renderProfessions(); break;
            case "Char.Craft": applyCraft(data); break;
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
        var prevExp = S.cooldownExpiry || {};
        var prevTot = S.cooldownTotal || {};
        S.cooldownExpiry = {};
        S.cooldownTotal = {};
        S.usable = (data && data.usable) || {};
        var list = (data && data.cooldowns) || [];
        var t = now();
        for (var i = 0; i < list.length; i++) {
            var id = list[i].id, rem = Number(list[i].remaining) || 0;
            S.cooldownExpiry[id] = t + rem;
            // Total duration for the radial sweep: the game only sends `remaining`,
            // so we take the first value seen this episode as the full length. If
            // the id was already cooling, keep the earlier (larger) total so the
            // ring keeps draining smoothly rather than snapping to a new full.
            S.cooldownTotal[id] = (prevExp[id] && prevExp[id] > t && prevTot[id]) ? prevTot[id] : rem;
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
            + (v && v.edge != null ? "e" : "")
            + (v && v.food != null ? "f" : "")
            + (v && v.water != null ? "w" : "");
    }

    // Hunger / thirst reserves ride the HP and MV bars (food fuels HP regen,
    // water fuels move regen — eating/drinking refill those pools). `food` and
    // `water` are a 0-100 percentage of the max reserve; the game omits them
    // when hunger/thirst doesn't apply (immortals), so the indicator is absent.
    // The state thresholds mirror the game's `score` warnings: <= PHPT/2 of the
    // pool (≈16%) is "very hungry/thirsty", <= PHPT (≈33%) is "getting…".
    function reserveState(pct) {
        if (pct == null) return "ok";
        if (pct <= 16) return "crit";
        if (pct <= 33) return "low";
        return "ok";
    }
    function reserveTitle(kind, pct) {
        var food = kind === "food";
        var word = pct == null ? "" : (pct <= 16 ? (food ? "very hungry" : "very thirsty")
            : pct <= 33 ? (food ? "getting hungry" : "getting thirsty")
            : (food ? "well fed" : "hydrated"));
        return (food ? "Food" : "Water") + " reserve: " + (pct == null ? "—" : pct + "%")
            + (word ? " — " + word : "");
    }
    // A small state-tinted icon appended to the HP (food) / MV (water) bar.
    function reserveEl(kind, pct) {
        return el("span", {
            class: "vbar-reserve " + kind,
            "data-state": reserveState(pct),
            title: reserveTitle(kind, pct),
            "aria-label": reserveTitle(kind, pct),
            role: "img"
        }, [biSvg(kind === "food" ? "apple" : "droplet-fill", "bi vbar-reserve-icon")]);
    }

    function cacheVitalsRefs() {
        vitalsCache = { shape: vitalsShape(S.vitals), bars: {}, reserves: {} };
        ["hp", "mp", "mv", "tgt", "mm", "edge"].forEach(function (cls) {
            var e = dom.vitals.querySelector(".vbar." + cls);
            if (e) vitalsCache.bars[cls] = { fill: e.querySelector(".vbar-fill"), text: e.querySelector(".vbar-text") };
        });
        ["food", "water"].forEach(function (k) {
            var e = dom.vitals.querySelector(".vbar-reserve." + k);
            if (e) vitalsCache.reserves[k] = e;
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
        updReserve("food", v && v.food != null ? v.food : null);
        updReserve("water", v && v.water != null ? v.water : null);
    }
    function updReserve(kind, pct) {
        var n = vitalsCache.reserves[kind];
        if (!n || pct == null) return;
        n.setAttribute("data-state", reserveState(pct));
        var t = reserveTitle(kind, pct);
        n.setAttribute("title", t);
        n.setAttribute("aria-label", t);
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

        var hpBar = vbar("HP", v ? v.hp : null, v ? v.maxhp : 0, "hp");
        var mvBar = vbar("MV", v ? v.move : null, v ? v.maxmove : 0, "mv");
        // Food rides the HP bar, water the MV bar — that's the pool each one
        // refills. Present only when the game sends them (mortals with hunger).
        if (v && v.food != null) hpBar.appendChild(reserveEl("food", v.food));
        if (v && v.water != null) mvBar.appendChild(reserveEl("water", v.water));
        var barKids = [hpBar,
                       vbar("MP", v ? v.mp : null, v ? v.maxmp : 0, "mp"),
                       mvBar];
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
            var foe = null, onYou = 0;
            for (var fi = 0; fi < (S.occupants || []).length; fi++) {
                if (S.occupants[fi].is_your_target) foe = S.occupants[fi];
                if (S.occupants[fi].fighting_you && !S.occupants[fi].is_dead) onYou++;
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
            // Attacker count — the multi-combatant tally the row-by-row "⚔
            // you" tags don't add up for you. Skipped when it would repeat
            // the "on you" chip's information (exactly one attacker = foe).
            if (onYou > 0 && !(onYou === 1 && foe && foe.fighting_you)) {
                barKids.push(el("span", { class: "v-foe-tgt you", title: "Enemies attacking you", text: "⚠ " + onYou + " on you" }));
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
    function setRoseTab(t) {
        roseTab = t === "map" ? "map" : "rose";
        try { localStorage.setItem("ishar.roseTab", roseTab); } catch (e) {}
        renderRoom();
    }
    function renderRoom() {
        var r = S.room;
        var titles = el("div", { class: "rose-titles" }, [
            el("span", { class: "rose-name", text: stripColor((r && r.name) || "Somewhere") }),
            r && r.area ? el("span", { class: "rose-area dim", text: stripColor(r.area) + (r.environment ? " · " + stripColor(r.environment) : "") }) : null
        ]);
        // The pinned Room panel is a two-tab micro-group (Rose | Map) once the
        // map module is live; rose-only otherwise. The phone rose overlay is
        // untouched — its job is tap-to-move, the big map serves phones.
        var mapOn = !!(mapMod && mapMod.enabled());
        var tab = mapOn ? roseTab : "rose";
        var tabs = null;
        if (mapOn) {
            tabs = el("div", { class: "rose-tabs" }, [
                el("button", {
                    type: "button", class: tab === "rose" ? "active" : "",
                    "aria-pressed": tab === "rose" ? "true" : "false",
                    text: "Rose", onclick: function () { setRoseTab("rose"); }
                }),
                el("button", {
                    type: "button", class: tab === "map" ? "active" : "",
                    "aria-pressed": tab === "map" ? "true" : "false",
                    text: "Map", onclick: function () { setRoseTab("map"); }
                }),
                tab === "map" ? el("button", {
                    type: "button", class: "rose-expand", text: "⤢",
                    title: "Open map (Ctrl+M)", "aria-label": "Open map window",
                    onclick: function () { toggleOverlay("map"); }
                }) : null
            ]);
        }
        var head = el("div", { class: "rose-head" }, [titles, tabs]);
        var body = el("div", { class: "rose-body" });
        if (tab === "map") mapMod.renderMini(body);
        else renderRose(body, false);
        // The current room's note (map feature) rides the Room panel in both
        // tabs — one quiet clamped line; tap to edit.
        var note = mapOn && mapMod.currentNote ? mapMod.currentNote() : "";
        var noteRow = note ? el("button", {
            type: "button", class: "rose-note", text: note,
            title: "Edit room note",
            onclick: function () { mapMod.editCurrentNote(); }
        }) : null;
        fill(dom.room, [head, body, noteRow]);
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
        // Sleeping followers can't hear an order — offering "Order attack"
        // with only a sleeping pet present would send a command the game
        // rejects ("None of your loyal followers can hear you.").
        return (S.occupants || []).some(function (o) {
            return o.is_loyal_follower && !o.is_dead && !occSleeping(o);
        });
    }
    // Triage tint for a group member's hp readout — the game's condition-
    // color breakpoints (get_condition_color), coarsened to three tiers:
    // ≤40 danger, ≤60 warn, else ok.
    function hpTintClass(p) {
        if (p == null) return "";
        return p <= 40 ? " cond-low" : p <= 60 ? " cond-mid" : " cond-ok";
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
        // Slain occupants stay in the FEED (they hold parser ordinal slots,
        // #1679) but not in the PANEL: the corpse object in Room.Contents is
        // the single representation of a body — two rows for one corpse was
        // the panel's most confusing moment (post-kill).
        var occ = (S.occupants || []).filter(function (o) { return !o.is_dead; });
        var items = S.roomItems || [];
        var nodes = S.roomNodes || [];
        var hasShop = occ.some(function (o) { return o.is_shopkeeper; });
        // Room-level List (every shop here) only when there's a shop to list.
        var actions = hasShop
            ? [el("button", { type: "button", class: "panel-h-btn", "data-cmd": "list", title: "List every shopkeeper's wares here", text: "List" })]
            : null;
        var head = panelHeader("occupants", "Room (" + (occ.length + items.length + nodes.length) + ")", false, actions);
        var kids = [head];
        if (!isCollapsed("occupants")) {
            if (!occ.length && !items.length && !nodes.length) {
                kids.push(el("div", { class: "panel-empty", text: "Nothing else here." }));
            } else if (occ.length) {
                // Target chips (current defaults) so they're visible at a glance.
                if (S.tgtHostile || S.tgtFriendly) {
                    var chips = [];
                    if (S.tgtHostile) chips.push(el("span", { class: "tgt-chip hostile", title: "Offensive spells target this", text: "⚔ " + S.tgtHostile.desc }));
                    if (S.tgtFriendly) chips.push(el("span", { class: "tgt-chip friendly", title: "Beneficial spells target this", text: "✚ " + S.tgtFriendly.desc }));
                    kids.push(el("div", { class: "tgt-chips" }, chips));
                }
                var list = el("ul", { class: "occ-list" });
                // Iterate the UNFILTERED list: data-idx must index S.occupants
                // (openHostMenu reads it back); dead entries just skip.
                (S.occupants || []).forEach(function (o, i) {
                    if (o.is_dead) return;
                    var marks = "";
                    if (S.tgtHostile && S.tgtHostile.handle === o.handle) marks += " ⚔";
                    if (S.tgtFriendly && S.tgtFriendly.handle === o.handle) marks += " ✚";
                    // Position tag for anyone not simply standing (the same
                    // cue the room text gives: "is sleeping here").
                    var ptag = (o.position && posLower(o) !== "standing")
                        ? posLower(o) : "";
                    var fight = occFightLabel(o);
                    var row = el("li", {
                        class: "occ-row " + occHostileClass(o),
                        "data-menu": "occupant", "data-idx": i,
                        title: "Tap for actions"
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
            // Ground objects and harvest nodes (Room.Contents) share the panel:
            // the room's whole interaction surface lives in one place.
            if (items.length) {
                kids.push(el("div", { class: "sub-h", text: "On the ground" }));
                kids.push(groundList(items));
            }
            if (nodes.length) {
                kids.push(el("div", { class: "sub-h", text: "Nodes" }));
                kids.push(nodeList(nodes));
            }
        }
        fill(dom.occupants, kids);
    }

    // ------------------------------------------------------------------
    // Ground items + nodes (Room.Contents) — rendered inside the Room panel.
    // ------------------------------------------------------------------
    // Client-side eligibility join for a harvest source (a node, or a corpse's
    // `harvest` object): mirrors the game's gate — must hold the profession,
    // and harvest_rank_allows (rank + 5 >= required, i.e. tier != "blocked").
    // A profession-less source is open to everyone.
    function harvestStanding(hv) {
        var req = Math.max(1, Number(hv.required_rank) || 1);
        if (!hv.profession_id) return { ok: true, tier: null, req: req };
        var prof = professionById(hv.profession_id);
        if (!prof) return { ok: false, tier: "blocked", untrained: true, req: req };
        var rank = Number(prof.rank) || 0;
        var tier = profTier(req - rank);
        // rank 0 = held but never practiced: harvest_rank_allows hard-fails
        // rank <= 0 server-side regardless of the delta.
        return { ok: rank > 0 && tier !== "blocked", tier: tier, prof: prof, req: req };
    }
    function harvestChip(hv) {
        var hs = harvestStanding(hv);
        var profName = hs.prof ? hs.prof.name : (hv.profession || "");
        var title = hs.untrained ? "Harvestable — requires " + (profName || "a profession you lack")
            : hs.ok ? "Harvestable — requires rank " + hs.req + (profName ? " " + profName : "")
            : "Harvestable — " + (profName ? profName + " " : "") + "rank " + hs.req + " needed (yours: " + (hs.prof ? hs.prof.rank : 0) + ")";
        return el("span", {
            class: "tag harvest tier-" + (hs.tier || "open"),
            title: title, text: "⛏ r" + hs.req
        });
    }
    // Server-computed handle first (exact instance), keyword join as fallback.
    function groundTarget(it) { return it.handle || targetOf(it.keywords || it.name); }
    // Nodes are matched by exact keyword token (or name substring) game-side —
    // NOT the object parser — so send one bare token, never a dotted join.
    function nodeTarget(n) {
        var k = firstWord(n.keywords);
        if (k) return k;
        var w = String(stripColor(n.name || "")).trim().split(/\s+/);
        return (w[w.length - 1] || "").replace(/[^A-Za-z0-9]/g, "");
    }

    function groundList(items) {
        var list = el("ul", { class: "row-list ground" });
        items.forEach(function (it, i) {
            var isContainer = it.type === "container";
            var hasContents = !!(it.contents && it.contents.length);
            var open = isContainer && !it.closed;
            // Expand-state key WITHOUT the handle's ordinal: "2.corpse.rat"
            // becomes "1.corpse.rat" when an earlier duplicate goes away, and
            // an ordinal-bearing key would silently drop the expansion (and
            // accrete stale variants in localStorage). Same-keyword duplicates
            // sharing one expand state is the lesser wart.
            var ekey = "g" + targetOf(it.keywords || it.name);
            var canExpand = open && hasContents;
            var isOpen = canExpand && !!expanded[ekey];
            var kids = [];
            if (canExpand) {
                kids.push(el("button", {
                    type: "button", class: "row-caret", "data-expand": ekey,
                    "aria-expanded": isOpen ? "true" : "false",
                    "aria-label": (isOpen ? "Collapse contents of " : "Expand contents of ") + stripColor(it.name || "container"),
                    text: isOpen ? "▾" : "▸"
                }));
            }
            if (it.is_corpse) kids.push(el("span", { class: "gnd-icon corpse", title: "Corpse", "aria-hidden": "true", text: "☠" }));
            kids.push(el("span", { class: "row-name", text: stripColor(it.name) }));
            if (it.count && it.count > 1) kids.push(el("span", { class: "tag", text: "×" + it.count }));
            // Glanceable loot count while the contents are folded.
            if (canExpand && !isOpen) kids.push(el("span", { class: "tag dim", text: it.contents.length + " inside" }));
            if (it.harvest) kids.push(harvestChip(it.harvest));
            // Closed/empty container state glyph (same language as inventory).
            if (isContainer && !it.is_corpse && (it.closed || !hasContents)) {
                kids.push(el("span", {
                    class: "row-glyph", "aria-hidden": "true",
                    title: it.locked ? "Locked" : it.closed ? "Closed — Open to see inside" : "Empty container",
                    text: it.closed || it.locked ? "🔒" : "📦"
                }));
            }
            kids.push(el("button", { type: "button", class: "row-more", "data-menu": "grounditem", "data-idx": i, "aria-label": "Actions", text: "⋯" }));
            list.appendChild(el("li", {
                class: "item-row ground" + (it.is_corpse ? " corpse" : ""),
                "data-menu": "grounditem", "data-idx": i, title: "Tap for actions"
            }, kids));
            if (isOpen) {
                var sub = el("ul", { class: "row-list sub" });
                var ct = groundTarget(it);
                groupStackables(it.contents).forEach(function (c) {
                    var tgt = targetOf(c.keywords || c.name);
                    // Row tap loots the item directly (the corpse-looting hot
                    // path); ⋯ opens the menu.
                    sub.appendChild(el("li", {
                        class: "item-row sub", "data-cmd": "get " + tgt + " from " + ct,
                        title: "Take from " + stripColor(it.name || "container") + " — ⋯ for more"
                    }, [
                        el("span", { class: "row-name", text: stripColor(c.name) }),
                        (c.count && c.count > 1) ? el("span", { class: "tag", text: "×" + c.count }) : null,
                        el("button", {
                            type: "button", class: "row-more", "data-menu": "groundcontent",
                            "data-target": tgt, "data-name": stripColor(c.name || ""), "data-container": ct,
                            "aria-label": "Actions", text: "⋯"
                        })
                    ]));
                });
                list.appendChild(sub);
            }
        });
        return list;
    }

    function nodeList(nodes) {
        var list = el("ul", { class: "row-list ground" });
        nodes.forEach(function (n, i) {
            var hs = harvestStanding(n);
            list.appendChild(el("li", {
                class: "item-row ground node", "data-menu": "node", "data-idx": i, title: "Tap for actions"
            }, [
                el("span", { class: "gnd-icon node" + (hs.tier ? " tier-" + hs.tier : ""), "aria-hidden": "true", text: "✦" }),
                el("span", { class: "row-name", text: stripColor(n.name) }),
                harvestChip(n),
                el("button", { type: "button", class: "row-more", "data-menu": "node", "data-idx": i, "aria-label": "Actions", text: "⋯" })
            ]));
        });
        return list;
    }

    // ------------------------------------------------------------------
    // Equipment
    // ------------------------------------------------------------------
    // Condition as one colour-coded dot — the numeric % and its word
    // ("pristine"/"worn"/…) ride in the title rather than eating a whole row.
    function conditionDot(c) {
        if (c == null) return null;
        // Real feed: int 0-100. Older/demo: a word. Colour numeric by value.
        var n = Number(c);
        if (!isNaN(n) && String(c).match(/^\s*\d/)) {
            var cls = n >= 90 ? "cond-ok" : n >= 50 ? "cond-mid" : "cond-low";
            var lbl = n >= 95 ? "pristine" : n >= 75 ? "good" : n >= 40 ? "worn" : n > 0 ? "battered" : "ruined";
            return el("span", { class: "cond-dot " + cls, title: "Condition " + n + "% — " + lbl, "aria-hidden": "true", text: "●" });
        }
        return el("span", { class: "cond-dot", title: "Condition " + String(c), "aria-hidden": "true", text: "●" });
    }
    // A stable key for a container's expand state (vnum when the game sends
    // one, else its target keyword).
    function containerKey(it) {
        return it.vnum != null ? "v" + it.vnum : "k" + targetOf(it.keywords || it.name);
    }
    // Fold identical stackable items into one row with a ×count. The game
    // often emits duplicate rows instead of a count (two "a glyph of
    // teleportation"), so we default to stacking: same name + type +
    // condition merges. Containers are always distinct (each may hold
    // different things) and are never merged.
    function groupStackables(items) {
        var out = [], seen = {};
        (items || []).forEach(function (it) {
            if (it.type === "container" || (it.contents && it.contents.length)) { out.push(it); return; }
            var key = stripColor(it.name || "") + "\x1f" + (it.type || "") + "\x1f" + (it.condition == null ? "" : it.condition);
            var qty = Number(it.count) || 1;
            if (seen[key] != null) { out[seen[key]].count += qty; return; }
            var copy = {};
            for (var k in it) if (Object.prototype.hasOwnProperty.call(it, k)) copy[k] = it[k];
            copy.count = qty;
            seen[key] = out.length;
            out.push(copy);
        });
        return out;
    }
    function itemDataset(it, kind, container) {
        return {
            "data-menu": "item", "data-kind": kind || "item",
            "data-target": targetOf(it.keywords || it.name),
            "data-otype": it.type || "",
            "data-name": stripColor(it.name || ""),
            "data-container": container || "",
            "data-closeable": it.closeable ? "1" : "",
            "data-closed": it.closed ? "1" : "",
            "data-disen": (Number(it.disenchant_rank) > 0) ? String(it.disenchant_rank) : ""
        };
    }
    // One inventory/equipment row. Everything stays on a single line: an
    // optional lead cell (an expand caret for an open container, else a
    // condition dot), the name, a ×count, a container state glyph, and the
    // ⋯ actions button.
    function itemRow(it, kind, container) {
        var ds = itemDataset(it, kind, container);
        var isContainer = it.type === "container";
        var hasContents = !!(it.contents && it.contents.length);
        var kids = [];
        if (kind === "equip") kids.push(el("span", { class: "slot", text: it.location || it.slot || "" }));
        // Lead cell (fixed-width so names align): caret for an expandable
        // container, otherwise the condition dot.
        if (isContainer && hasContents) {
            var ck = containerKey(it), isOpen = !!expanded[ck];
            kids.push(el("button", {
                type: "button", class: "row-caret", "data-expand": ck,
                "aria-expanded": isOpen ? "true" : "false",
                "aria-label": (isOpen ? "Collapse contents of " : "Expand contents of ") + stripColor(it.name || "container"),
                text: isOpen ? "▾" : "▸"
            }));
        } else if (!isContainer) {
            var dot = conditionDot(it.condition);
            if (dot) kids.push(dot);
        }
        kids.push(el("span", { class: "row-name", text: stripColor(it.name) }));
        if (it.count && it.count > 1) kids.push(el("span", { class: "tag", text: "×" + it.count }));
        // A closed/locked (or empty) container can't be searched inline — mark
        // its state with a glyph instead of a caret.
        if (isContainer && (it.closed || !hasContents)) {
            kids.push(el("span", {
                class: "row-glyph", "aria-hidden": "true",
                title: it.locked ? "Locked" : it.closed ? "Closed" : "Container",
                text: it.closed || it.locked ? "🔒" : "📦"
            }));
        }
        kids.push(el("button", { type: "button", class: "row-more", "aria-label": "Actions", text: "⋯" }));
        ds.class = "item-row" + (kind === "content" ? " sub" : "");
        return el("li", assign(ds, {}), kids);
    }
    function assign(a, b) { Object.keys(b).forEach(function (k) { a[k] = b[k]; }); return a; }

    // A row list where an open, expanded container row is followed by a
    // sub-list of its contents. Shared by the inventory and equipment panels
    // so a WORN container (a backpack on the back) is inspectable exactly like
    // a carried one — the game already emits worn-container contents in
    // Char.Equipment (#1590); the equipment panel just wasn't rendering them
    // (issue #1801). Contents render only when the container is expanded
    // (packs start collapsed); stackable rows are folded to a ×count.
    function itemListWithContents(items, kind) {
        var list = el("ul", { class: "row-list" });
        // Worn gear occupies distinct slots (Head, Left/Right finger, …) so it
        // is never stacked; carried piles are.
        var top = kind === "equip" ? (items || []) : groupStackables(items);
        top.forEach(function (it) {
            list.appendChild(itemRow(it, kind));
            if (it.type === "container" && it.contents && it.contents.length && expanded[containerKey(it)]) {
                var sub = el("ul", { class: "row-list sub" });
                var ct = targetOf(it.keywords || it.name);
                groupStackables(it.contents).forEach(function (c) { sub.appendChild(itemRow(c, "content", ct)); });
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
                    li = el("li", { class: "item-row comp", "data-cmd": "get " + tgt + " pouch", title: "Withdraw from pouch — ⋯ for more" }, [
                        el("span", { class: "row-name", text: name }),
                        c.count > 1 ? el("span", { class: "tag", text: "×" + c.count }) : null,
                        el("button", { type: "button", class: "row-more", "data-menu": "component", "data-target": tgt, "data-name": name, "aria-label": "Actions", text: "⋯" })
                    ]);
                } else {
                    // No keywords (pre-deploy of the game field): a name-derived
                    // withdraw wouldn't resolve, so offer examine only.
                    li = el("li", { class: "item-row comp", "data-cmd": "examine " + targetOf(c.name), title: "Examine" }, [
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
    function groupRow(x, kind, idx, extraName, hasMenu) {
        var chips = [];
        if (x.is_tank) chips.push(el("span", { class: "grp-tank", title: "Tanking — enemies are targeting them", text: "TANK" }));
        var tc = threatChip(x);
        if (tc) chips.push(tc);
        if (x.fighting_name) chips.push(el("span", { class: "grp-fight", title: "Fighting", text: "⚔ " + stripColor(x.fighting_name) }));
        var p = String(x.position || "").toLowerCase();
        if (p && p !== "standing") chips.push(el("span", { class: "grp-pos", text: p }));
        // Where a mate is when they're not with you. The map owns the reveal
        // rule (exact room only for a zone you've discovered, else the area),
        // so the HUD never shows more than you've earned; fall back to a plain
        // "away" if the mapper isn't loaded.
        if (x.in_room === false) {
            var whereText = (mapMod && mapMod.memberWhere) ? mapMod.memberWhere(x) : "";
            if (!whereText) whereText = "away";
            chips.push(el("span", { class: "grp-away", title: "Not in your room", text: whereText }));
        }
        var main = el("div", { class: "grp-main" }, [
            el("div", { class: "grp-line" }, [
                el("span", { class: "grp-name", text: stripColor(String(x.name || "")) + (x.leader ? " ★" : "") }),
                extraName ? el("span", { class: "dim", text: " " + extraName }) : null,
                el("span", { class: "grp-hp-num" + hpTintClass(x.hp_pct), text: (x.hp_pct != null ? x.hp_pct + "%" : "") })
            ]),
            chips.length ? el("div", { class: "grp-chips" }, chips) : null,
            el("span", { class: "grp-bars" }, [mini(x.hp_pct, "hp"), mini(x.mp_pct, "mp"), mini(x.mv_pct, "mv")])
        ]);
        // A row with nothing to offer (your own row; an out-of-room ally) is
        // information, not a control — no menu affordances, no dead taps.
        if (!hasMenu) return el("li", { class: "grp grp-self" + (x.is_tank ? " tanking" : "") }, [main]);
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
                var selfName = S.status ? String(S.status.name || "").toLowerCase() : "";
                members.forEach(function (m, i) {
                    // Your own row never has actions; other members always
                    // have at least Tell.
                    var isSelf = selfName && String(m.name || "").toLowerCase() === selfName;
                    gl.appendChild(groupRow(m, "member", i, "", !isSelf));
                });
                kids.push(gl);
                if (allies.length) {
                    kids.push(el("div", { class: "sub-h", text: "Allies" }));
                    var al = el("ul", { class: "grp-list" });
                    allies.forEach(function (a, i) {
                        // An ally row is only actionable through its occupant
                        // entry — out of the room there's nothing to offer.
                        al.appendChild(groupRow(a, "ally", i, a.owner ? "(" + a.owner + ")" : "", !!groupAllyOcc(a)));
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
            if (nm && !self) {
                acts.push({ label: "Tell…", prefill: "tell " + nm + " " });
                regroupActions(nm).forEach(function (a) { acts.push(a); });
            }
        }
        return acts;
    }

    // Regroup spells offered on an away mate's menu, only when the caster knows
    // them — the game enforces mana / range / anti-magic / group-bond itself, so
    // a shown action can still be refused in play. translocate moves you to the
    // mate; summon brings the mate to you.
    function knownSpell(name) {
        var hits = (S.skills || []).filter(function (s) {
            return s.type === "spell" && nameOf(s.name).toLowerCase() === name;
        });
        return hits.length ? hits[0] : null;
    }
    function regroupActions(nm) {
        var acts = [];
        [["translocate", "Translocate to "], ["summon", "Summon "]].forEach(function (p) {
            var s = knownSpell(p[0]);
            if (!s) return;
            var blocked = abilityBlock(s);
            acts.push({
                label: p[1] + nm + (blocked ? " (" + blocked.reason + ")" : ""),
                cmd: "cast '" + p[0] + "' " + nm,
                disabled: !!blocked
            });
        });
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

    // ------------------------------------------------------------------
    // The WoW-style action bar (bottom of the HUD)
    // ------------------------------------------------------------------
    // Two modes:
    //   • custom  — the player has pinned at least one skill; the bar shows their
    //               numbered slots (fixed positions, hotkey-addressable), paged.
    //   • auto    — nothing pinned yet; a capped set of usable damage/heal skills
    //               is offered so the bar is useful out of the box. Pinning any
    //               skill (★ / "Add to bar") switches to custom mode.
    var hotbarNodes = {};   // render-key -> { btn, cdEl?, id?, idx?, empty? }
    function skillById(id) {
        id = String(id);
        var list = S.skills || [];
        for (var i = 0; i < list.length; i++) if (String(list[i].id) === id) return list[i];
        return null;
    }
    function skillByKey(key) {
        if (!key) return null;
        var list = S.skills || [];
        for (var i = 0; i < list.length; i++) if (slotKeyOf(list[i]) === key) return list[i];
        return null;
    }
    // Auto mode: usable damage/heal first, then anything cooling, capped to a page.
    function autoSuggestions() {
        var skills = (S.skills || []).filter(function (s) { return s.type === "spell" || s.type === "skill"; });
        var rank = { damage: 0, heal: 1, misc: 2 };
        var out = [], seen = {};
        function push(s) { if (s && !seen[s.id] && out.length < SLOTS_PER_PAGE) { seen[s.id] = true; out.push(s); } }
        skills.filter(function (s) { return !abilityBlock(s); })
              .sort(function (a, b) { return (rank[a.category] == null ? 3 : rank[a.category]) - (rank[b.category] == null ? 3 : rank[b.category]); })
              .forEach(push);
        skills.forEach(function (s) { if (S.cooldownExpiry[s.id] > now()) push(s); });
        return out;
    }
    // How many pages hold at least one assigned slot (custom mode).
    function usedPages() {
        var mx = -1;
        for (var i = 0; i < slots.length; i++) if (slots[i]) mx = Math.max(mx, pageOfIndex(i));
        return mx + 1;
    }
    function renderHotbar() {
        hideTip();                       // a rebuild orphans the tip's anchor
        hotbarNodes = {};
        while (dom.hotbar.firstChild) dom.hotbar.removeChild(dom.hotbar.firstChild);
        var custom = anyAssigned();
        dom.hotbar.classList.toggle("custom", custom);
        // Edit mode only makes sense once there are real slots to move.
        dom.hotbar.classList.toggle("editing", custom && !barLocked);
        if (barLocked) pickedSlot = null;
        var entries = [];   // { s, key, idx, label, empty }

        if (custom) {
            var pages = Math.max(1, usedPages());
            hotbarPage = clamp(hotbarPage, 0, pages - 1);
            dom.hotbar.appendChild(buildLock());
            if (pages > 1) dom.hotbar.appendChild(buildPager(pages));
            var base = hotbarPage * SLOTS_PER_PAGE;
            var last = base;   // render through the last filled slot (trim trailing empties)
            for (var i = base; i < base + SLOTS_PER_PAGE; i++) if (slots[i]) last = i;
            for (var j = base; j <= last; j++) {
                var key = slots[j];
                entries.push({ s: key ? skillByKey(key) : null, key: key, idx: j, label: slotLabel(j), empty: !key });
            }
        } else {
            hotbarPage = 0;
            autoSuggestions().forEach(function (s, i) {
                entries.push({ s: s, key: slotKeyOf(s), idx: i, label: slotLabel(i), empty: false });
            });
        }

        if (!entries.length) { dom.hotbar.classList.add("empty"); return; }
        dom.hotbar.classList.remove("empty");
        entries.forEach(function (e) { dom.hotbar.appendChild(buildSlot(e, custom)); });
        tickHotbar();
    }
    function buildPager(pages) {
        return el("button", {
            type: "button", class: "skill skill--pager", "data-pager": "1",
            "data-tip": "Bar " + (hotbarPage + 1) + "/" + pages + " · switch (Alt+`)",
            "aria-label": "Switch action bar page, currently " + (hotbarPage + 1) + " of " + pages
        }, [
            iconSvg("gears", "gi skill-icon"),
            el("span", { class: "skill-key", text: (hotbarPage + 1) + "/" + pages })
        ]);
    }
    // The lock toggle: locked fires on tap, unlocked is edit mode (rearrange).
    function buildLock() {
        var open = !barLocked;
        return el("button", {
            type: "button", class: "skill skill--lock" + (open ? " on" : ""), "data-lock": "1",
            "data-tip": open ? "Unlocked · drag or tap slots to rearrange" : "Locked · tap to edit the bar",
            "aria-label": open ? "Lock action bar (rearranging enabled)" : "Unlock action bar to rearrange",
            "aria-pressed": open ? "true" : "false"
        }, [iconSvg(open ? "padlock-open" : "padlock", "gi skill-icon")]);
    }
    function buildSlot(e, custom) {
        // Empty numbered placeholder — a visible drop/assign target in custom mode.
        if (e.empty || !e.s) {
            var eb = el("button", {
                type: "button", class: "skill skill--empty", "data-slot": e.idx, "data-menu": "slot",
                "aria-label": "Empty slot " + e.label,
                "data-tip": "Slot " + e.label + " · empty — pin from Abilities or drag here"
            }, [el("span", { class: "skill-key", text: e.label })]);
            hotbarNodes["e" + e.idx] = { btn: eb, empty: true };
            return eb;
        }
        var s = e.s;
        var editing = custom && !barLocked;
        var btn = el("button", {
            type: "button", class: "skill " + catClass(s) + (e.idx === pickedSlot ? " picked" : ""),
            "data-ability": s.id, "data-menu": "ability",
            "data-slot": custom ? e.idx : null, "data-key": e.label, draggable: editing ? "true" : null,
            "aria-label": e.label + ": " + s.name
        }, [
            iconSvg(iconName(s), "gi skill-icon"),
            el("span", { class: "skill-sweep", "aria-hidden": "true" }),
            el("span", { class: "skill-key", text: e.label }),
            el("span", { class: "skill-cd" })
        ]);
        hotbarNodes["s" + e.idx] = {
            btn: btn, cdEl: btn.querySelector(".skill-cd"),
            sweepEl: btn.querySelector(".skill-sweep"), id: String(s.id), idx: e.idx
        };
        return btn;
    }
    function tickHotbar() {
        Object.keys(hotbarNodes).forEach(function (key) {
            var n = hotbarNodes[key];
            if (!n || n.empty) return;
            var s = skillById(n.id);
            if (!s) return;
            var blk = abilityBlock(s);
            var cd = blk ? blk.cd : 0;
            // A non-cooldown block (mana / min-position) shows its reason instead
            // of a timer, so a blocked slot isn't a silent dead tap.
            var reason = (blk && cd === 0)
                ? (blk.reason === "low mana" ? "mana" : blk.reason === "unavailable" ? "" : blk.reason)
                : "";
            n.btn.classList.toggle("off", !!blk);
            n.btn.classList.toggle("cooling", cd > 0);
            n.btn.classList.toggle("blocked", !!(blk && cd === 0 && reason));
            n.cdEl.textContent = cd > 0 ? String(cd) : reason;
            // Radial cooldown sweep: fraction remaining, from the approximate total.
            if (n.sweepEl) {
                var tot = cd > 0 ? Number(S.cooldownTotal[s.id]) || 0 : 0;
                var frac = (tot > 0) ? clamp01((S.cooldownExpiry[s.id] - now()) / tot) : 0;
                n.sweepEl.style.setProperty("--sweep", (frac * 360).toFixed(1) + "deg");
                n.btn.classList.toggle("sweeping", frac > 0);
            }
            // The slot face stays icon + number only; verbose detail lives in the
            // hover/focus tooltip (desktop) and the long-press menu (touch). If the
            // tip is open on this slot, refresh it so a running cooldown ticks.
            if (tipAnchor === n.btn) showTip(n.btn, skillTipData(s, n.btn.getAttribute("data-key")));
        });
    }
    function clamp01(x) { return Math.max(0, Math.min(1, x)); }
    // Cycle to the next used page of the action bar (custom mode only).
    function flipHotbarPage() {
        var pages = Math.max(1, usedPages());
        if (pages < 2) return;
        hotbarPage = (hotbarPage + 1) % pages;
        renderHotbar();
    }
    // Lock ⇄ unlock. Unlocked (edit mode) rearranges on tap/drag instead of firing.
    function toggleBarLock() {
        barLocked = !barLocked;
        try { localStorage.setItem("ishar.barUnlocked", barLocked ? "0" : "1"); } catch (e) {}
        pickedSlot = null;
        renderHotbar();
    }
    // Tap-to-swap (works on mouse + touch): pick a slot, then tap its destination.
    function pickOrPlace(idx) {
        if (pickedSlot == null) {
            if (!slots[idx]) return;            // nothing to pick up in an empty slot
            pickedSlot = idx;
        } else if (pickedSlot === idx) {
            pickedSlot = null;                  // tap the picked slot again to cancel
        } else {
            var key = slots[pickedSlot];
            pickedSlot = null;
            if (key) { assignSlot(idx, key); return; }   // assignSlot swaps + re-renders
        }
        renderHotbar();
    }
    // Fire the Nth visible slot (0-based) as if tapped. Used by the hotkeys.
    function fireSlot(n) {
        if (!barLocked) return false;   // edit mode: hotkeys don't cast
        var node = hotbarNodes["s" + (hotbarPage * SLOTS_PER_PAGE + n)]   // custom mode
                || hotbarNodes["s" + n];                                   // auto mode
        if (!node) return false;
        var s = skillById(node.id);
        if (!s) return false;
        if (abilityBlock(s)) { flashSlot(node.btn); return true; }   // on cooldown / blocked: no-op, but flash
        var cmd = abilityCommand(s);
        if (cmd) { sendCmd(cmd); flashSlot(node.btn); return true; }
        return false;
    }
    // Brief press feedback so a keyboard fire is visible on the bar.
    function flashSlot(btn) {
        if (!btn) return;
        btn.classList.add("fired");
        setTimeout(function () { btn.classList.remove("fired"); }, 180);
    }

    // ------------------------------------------------------------------
    // Tooltip convention (.hud-tip)
    // ------------------------------------------------------------------
    // The HUD's one hover/focus tooltip. Deliberately terse — a title line, an
    // optional right-aligned key chip (the hotkey), and at most one status line.
    // Any element opts in with `data-tip="text"`; the action bar supplies richer
    // structured tips. Hover/focus only: coarse pointers never see it (they use
    // the long-press menu), so nothing load-bearing lives here.
    var tipAnchor = null, tipTimer = null;
    var mqHover = window.matchMedia ? window.matchMedia("(hover: hover)") : { matches: true };
    // The structured tip for a skill slot: name + "Alt+N" chip + one status line.
    function skillTipData(s, keyLabel) {
        var blk = abilityBlock(s);
        var bits = [];
        if (s.type) bits.push(s.type);
        if (s.percent != null) bits.push(s.percent + "%");
        var warn = blk ? (blk.cd > 0 ? blk.cd + "s" : blk.reason) : "";
        return { name: s.name, key: keyLabel ? "Alt+" + keyLabel : "", sub: bits.join(" · "), warn: warn };
    }
    function showTip(anchor, d) {
        if (!dom.tip || !d) return;
        var row = el("div", { class: "tip-row" }, [el("span", { class: "tip-name", text: d.name })]);
        if (d.key) row.appendChild(el("span", { class: "tip-key", text: d.key }));
        var kids = [row];
        if (d.sub || d.warn) {
            var sub = el("div", { class: "tip-sub" });
            if (d.sub) sub.appendChild(el("span", { text: d.sub }));
            if (d.warn) sub.appendChild(el("span", { class: "tip-warn", text: (d.sub ? " · " : "") + d.warn }));
            kids.push(sub);
        }
        fill(dom.tip, kids);
        dom.tip.hidden = false;
        tipAnchor = anchor;
        positionTip(anchor);
    }
    function hideTip() {
        clearTimeout(tipTimer); tipTimer = null; tipAnchor = null;
        if (dom.tip) dom.tip.hidden = true;
    }
    function positionTip(anchor) {
        var m = dom.tip;
        m.style.left = "0px"; m.style.top = "0px";
        var r = anchor.getBoundingClientRect();
        var mw = m.offsetWidth, mh = m.offsetHeight;
        var vw = window.innerWidth, vh = window.visualViewport ? window.visualViewport.height : window.innerHeight;
        var x = r.left + r.width / 2 - mw / 2;
        var y = r.top - mh - 6;                 // above by default
        if (y < 6) y = r.bottom + 6;            // flip below if it would clip the top
        m.style.left = Math.max(6, Math.min(x, vw - mw - 6)) + "px";
        m.style.top = Math.max(6, Math.min(y, vh - mh - 6)) + "px";
    }
    // Resolve the tip payload for a hovered/focused element (or null).
    function tipDataFor(t) {
        var ab = t.closest && t.closest(".skill[data-ability]");
        if (ab) {
            var s = skillById(ab.getAttribute("data-ability"));
            return s ? skillTipData(s, ab.getAttribute("data-key")) : null;
        }
        if (t.getAttribute && t.getAttribute("data-tip")) return { name: t.getAttribute("data-tip") };
        return null;
    }
    function wireTooltips() {
        if (!dom.app) return;
        var SEL = ".skill[data-ability],[data-tip]";
        dom.app.addEventListener("mouseover", function (e) {
            if (!mqHover.matches) return;
            var t = e.target.closest(SEL);
            if (!t || !dom.app.contains(t)) return;
            var d = tipDataFor(t);
            if (!d) return;
            clearTimeout(tipTimer);
            tipTimer = setTimeout(function () { showTip(t, d); }, 320);   // small hover delay
        });
        dom.app.addEventListener("mouseout", function (e) {
            var t = e.target.closest(SEL);
            if (!t) return;
            if (e.relatedTarget && t.contains(e.relatedTarget)) return;   // moving within the same target
            hideTip();
        });
        // Keyboard focus reveals the tip immediately (hotkey discovery).
        dom.app.addEventListener("focusin", function (e) {
            var t = e.target.closest && e.target.closest(SEL);
            if (!t) return;
            var d = tipDataFor(t);
            if (d) showTip(t, d);
        });
        dom.app.addEventListener("focusout", hideTip);
        // A moving/rerendering anchor must not leave a stale tip floating.
        if (dom.hotbar) dom.hotbar.addEventListener("scroll", hideTip, { passive: true });
    }

    // Desktop drag-to-reorder within the bar (custom mode). Dropping A onto B
    // swaps them — the WoW gesture. Touch reorders via the "Move ◄/►" menu items.
    var dragFromSlot = null;
    function wireHotbarDrag() {
        if (!dom.hotbar) return;
        dom.hotbar.addEventListener("dragstart", function (e) {
            if (barLocked) { e.preventDefault(); return; }   // locked: no dragging
            var b = e.target.closest(".skill[data-slot]");
            if (!b || b.classList.contains("skill--empty")) { e.preventDefault(); return; }
            dragFromSlot = Number(b.getAttribute("data-slot"));
            e.dataTransfer.effectAllowed = "move";
            try { e.dataTransfer.setData("text/plain", "slot:" + dragFromSlot); } catch (x) {}
            b.classList.add("dragging");
        });
        dom.hotbar.addEventListener("dragend", function () {
            dragFromSlot = null;
            var els = dom.hotbar.querySelectorAll(".dragging,.drop-target");
            for (var i = 0; i < els.length; i++) els[i].classList.remove("dragging", "drop-target");
        });
        dom.hotbar.addEventListener("dragover", function (e) {
            var b = e.target.closest(".skill[data-slot]");
            if (!b || dragFromSlot == null) return;
            e.preventDefault();
            e.dataTransfer.dropEffect = "move";
            b.classList.add("drop-target");
        });
        dom.hotbar.addEventListener("dragleave", function (e) {
            var b = e.target.closest(".skill[data-slot]");
            if (b) b.classList.remove("drop-target");
        });
        dom.hotbar.addEventListener("drop", function (e) {
            var b = e.target.closest(".skill[data-slot]");
            if (!b || dragFromSlot == null) return;
            e.preventDefault();
            var to = Number(b.getAttribute("data-slot"));
            var key = slots[dragFromSlot];
            if (key != null && to !== dragFromSlot) assignSlot(to, key);
            dragFromSlot = null;
        });
    }

    // Global hotkeys: Alt/Ctrl + 1..0 fire the visible bar's slots; Alt+` pages.
    // Browsers reserve Ctrl+digit for tab-switching and web content usually can't
    // veto that, so Alt+digit is the reliable path (works in Chrome/Chromium/
    // Safari; Firefox reserves Alt+digit too). Ctrl is offered as a bonus that
    // comes fully alive when the HUD runs installed/fullscreen (no tab strip).
    function wireHotkeys() {
        document.addEventListener("keydown", function (e) {
            // Overlay keys are gated on the HUD only, not the connection —
            // browsing a reference window while the link is down is fine.
            if (!hudOn) return;
            // Esc closes the open overlay window before anything else claims
            // it. This listener registers before the page's Esc handler
            // (IsharHUD.init runs first in connect.html), so stop the event
            // here or the same press would also close the page's search /
            // settings / history popovers behind the overlay.
            if (e.key === "Escape" && overlayName && !mqMobile.matches) {
                e.stopImmediatePropagation();
                setOverlay(null);
                return;
            }
            // Overlay hotkeys: Ctrl+<letter> toggles a micro-menu app (e.g.
            // Ctrl+P → Professions). Strict single-modifier, and swallowed
            // only when the app is actually available, so browser defaults
            // survive everywhere else.
            var ctrlOnly = e.ctrlKey && !e.altKey && !e.metaKey && !e.shiftKey;
            if (ctrlOnly && /^[a-z]$/.test(String(e.key || "").toLowerCase())) {
                var letter = String(e.key).toLowerCase();
                for (var oi = 0; oi < OVERLAYS.length; oi++) {
                    var ov = OVERLAYS[oi];
                    if (ov.hotkey === letter && (!ov.available || ov.available())) {
                        e.preventDefault();
                        toggleOverlay(ov.key);
                        return;
                    }
                }
            }
            if (!S.connected) return;
            if (e.key === "`" && e.altKey && !e.ctrlKey && !e.metaKey && !e.shiftKey) {
                if (usedPages() > 1) { e.preventDefault(); flipHotbarPage(); }
                return;
            }
            var m = e.code && /^(Digit|Numpad)([0-9])$/.exec(e.code);
            var digit = m ? m[2] : (/^[0-9]$/.test(e.key) ? e.key : null);
            if (digit == null) return;
            var alt = e.altKey && !e.ctrlKey && !e.metaKey && !e.shiftKey;
            var ctrl = e.ctrlKey && !e.altKey && !e.metaKey && !e.shiftKey;
            if (!alt && !ctrl) return;
            var n = digit === "0" ? 9 : (Number(digit) - 1);   // 1..9 -> 0..8, 0 -> 9 (slot 10)
            if (fireSlot(n)) e.preventDefault();   // only swallow the combo when a slot actually fired
        });
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
        var counts = { all: 0, bar: 0, spell: 0, skill: 0, craft: 0 };
        all.forEach(function (s) {
            counts.all++;
            if (onBar(slotKeyOf(s))) counts.bar++;
            if (s.type === "spell") counts.spell++;
            else if (s.type === "skill") counts.skill++;
            else if (s.type === "craft" || s.type === "enchant") counts.craft++;
        });
        // "All" and "★ Bar" always show (Bar invites pinning even at 0); the
        // type chips appear only when they have members.
        [["all", "All"], ["bar", "★"], ["spell", "Spells"], ["skill", "Skills"], ["craft", "Crafts"]].forEach(function (tc) {
            if (tc[0] !== "all" && tc[0] !== "bar" && !counts[tc[0]]) return;
            typeChips.appendChild(el("button", {
                type: "button", class: "ab-chip" + (tc[0] === "bar" ? " ab-fav" : "") + (abilityFilter.type === tc[0] ? " on" : ""),
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
            if (abilityFilter.type === "bar" && !onBar(slotKeyOf(s))) return false;
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
                : abilityFilter.type === "bar" ? "No skills on your bar yet — tap ☆ to pin one, then fire it with Alt+1…0."
                : "No abilities match.";
            scroller.appendChild(el("div", { class: "panel-empty", text: emptyMsg }));
        } else {
            var ul = el("ul", { class: "ab-list" });
            rows.forEach(function (s) {
                var passive = !abilityUsable(s);   // passive / craft / enchant
                var blk = passive ? null : abilityBlock(s);
                var pinned = onBar(slotKeyOf(s));
                var right = [];
                if (blk) right.push(el("span", { class: "ab-block", text: blk.cd > 0 ? blk.cd + "s" : blk.reason }));
                if (passive) right.push(el("span", { class: "ab-type", text: s.type }));
                right.push(el("span", { class: "ab-pct", text: s.percent + "%" }));
                right.push(el("button", { type: "button", class: "ab-star" + (pinned ? " on" : ""), "data-bar": nameOf(s.name), "aria-label": pinned ? "Remove from action bar" : "Add to action bar", title: pinned ? "Remove from action bar" : "Add to action bar", text: pinned ? "★" : "☆" }));
                right.push(el("button", { type: "button", class: "row-more", "aria-label": "More actions", text: "⋯" }));
                ul.appendChild(el("li", {
                    class: "ab-row " + catClass(s) + (blk ? " off" : "") + (passive ? " ab-passive" : ""),
                    "data-ability": s.id, "data-menu": "ability",
                    title: passive ? s.name + " — " + s.type + " (not usable)" : castHint(s)
                }, [
                    iconSvg(iconName(s), "gi ab-icon"),
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
    // Set (or clear) a per-skill icon override, then repaint.
    function setIcon(name, iconOrNull) {
        var k = nameOf(name).toLowerCase();
        if (iconOrNull) iconOverrides[k] = iconOrNull; else delete iconOverrides[k];
        saveMap("ishar.icons", iconOverrides);
        renderHotbar(); renderAbilities();
    }

    // ------------------------------------------------------------------
    // Overlay apps: micro-menu buttons → #hud-overlay window (desktop) or
    // the bottom sheet (phones). One overlay at a time; Esc, outside-click,
    // the ✕, the hotkey, or the button all dismiss. Registry: OVERLAYS.
    // ------------------------------------------------------------------
    function overlayByKey(key) {
        for (var i = 0; i < OVERLAYS.length; i++) {
            if (OVERLAYS[i].key === key) return OVERLAYS[i];
        }
        return null;
    }
    function setOverlay(name) {
        var prev = overlayName;
        var hadFocus = dom.overlay && dom.overlay.contains(document.activeElement);
        var ov = name ? overlayByKey(name) : null;
        overlayName = ov ? ov.key : null;
        OVERLAYS.forEach(function (o) {
            var p = document.getElementById("panel-" + o.key);
            if (p) p.classList.toggle("overlay-active", o.key === overlayName);
            var b = dom.micro && dom.micro.querySelector('button[data-overlay="' + o.key + '"]');
            if (b) b.setAttribute("aria-pressed", o.key === overlayName ? "true" : "false");
        });
        if (dom.overlay) {
            dom.overlay.hidden = !ov;
            // Lets CSS size the window per app (the map wants more room).
            dom.overlay.setAttribute("data-app", ov ? ov.key : "");
        }
        if (dom.overlayTitle) dom.overlayTitle.textContent = ov ? ov.title : "";
        if (ov) {
            ov.render();
            markOverlayUnread(ov.key, false);
            // Dialog semantics: move focus into the window (tabindex="-1") so
            // keyboard/SR users land where the content is, not behind it.
            if (dom.overlay && dom.overlay.focus) dom.overlay.focus();
        } else if (prev && hadFocus) {
            // Closing with focus inside: hand it back to the launcher.
            var lb = dom.micro && dom.micro.querySelector('button[data-overlay="' + prev + '"]');
            if (lb && !lb.hidden) lb.focus();
        }
    }
    function toggleOverlay(key) {
        if (mqMobile.matches) { setSheet(sheetName === key ? null : key); return; }
        setOverlay(overlayName === key ? null : key);
    }
    function overlayVisible(key) {
        if (!hudOn) return false;
        return mqMobile.matches ? sheetName === key : overlayName === key;
    }
    // Dot badge on the app's launchers (micro button + dock button): the feed
    // changed while its window was closed. Same idiom as the chat unread dot.
    function markOverlayUnread(key, on) {
        ['#hud-micro button[data-overlay="' + key + '"]',
         '#hud-dock button[data-panel="' + key + '"]'].forEach(function (sel) {
            var b = document.querySelector(sel);
            if (b) b.classList.toggle("unread", !!on);
        });
    }
    // Availability gate: an app with nothing to show hides its launchers
    // entirely (a character with no professions never sees the button).
    function updateMicro() {
        OVERLAYS.forEach(function (o) {
            var avail = !o.available || o.available();
            var b = dom.micro && dom.micro.querySelector('button[data-overlay="' + o.key + '"]');
            if (b) b.hidden = !avail;
            var d = dom.dock && dom.dock.querySelector('button[data-panel="' + o.key + '"]');
            if (d) d.hidden = !avail;
            if (!avail) {
                if (overlayName === o.key) setOverlay(null);
                if (sheetName === o.key) setSheet(null);
                markOverlayUnread(o.key, false);
            }
        });
    }

    // ------------------------------------------------------------------
    // Professions (Char.Professions + Char.Craft) — the first overlay app.
    // Standing rows (rank/tier/recipes) plus a live craft/harvest cast bar.
    // ------------------------------------------------------------------
    var lastProfessionsBody = null;
    function applyProfessions(data) {
        var list = (data && data.professions) || [];
        var body = "";
        try { body = JSON.stringify(list); } catch (e) {}
        // Badge only on a *change* after the first snapshot — the login burst
        // shouldn't light the dot.
        var changed = lastProfessionsBody !== null && body !== lastProfessionsBody;
        lastProfessionsBody = body;
        S.professions = list;
        updateMicro();
        renderProfessions();
        if (changed && !overlayVisible("professions")) markOverlayUnread("professions", true);
    }
    function applyCraft(data) {
        if (data && data.active) {
            S.craft = {
                kind: data.kind === "harvest" ? "harvest" : "craft",
                name: String(data.name || ""),
                quantity: Number(data.quantity) || 1,
                chain: Number(data.chain_remaining) || 0,
                // Like cooldowns: store the expiry and tick locally between feeds.
                expiry: now() + (Number(data.remaining) || 0),
                total: Math.max(1, Number(data.duration) || Number(data.remaining) || 1)
            };
        } else {
            S.craft = null;
        }
        updateMicro();   // craft state feeds the availability gate too
        renderProfessions();
        tickCraft();
    }
    // Per-second updates that must not rebuild the panel: the micro button's
    // progress strip and the open panel's cast-bar numbers.
    function tickCraft() {
        var c = S.craft;
        var rem = c ? Math.max(0, c.expiry - now()) : 0;
        var pctW = c ? Math.max(0, Math.min(100, (1 - rem / c.total) * 100)) + "%" : "0%";
        var b = dom.micro && dom.micro.querySelector('button[data-overlay="professions"]');
        if (b) {
            var strip = b.querySelector(".micro-strip");
            if (strip) { strip.hidden = !c; if (c) strip.style.width = pctW; }
        }
        if (c && dom.professions) {
            var fillBar = dom.professions.querySelector(".craft-fill");
            if (fillBar) fillBar.style.width = pctW;
            var t = dom.professions.querySelector(".craft-time");
            if (t) t.textContent = fmtDur(rem);
        }
    }
    // Command builder: alchemy (and any future non-shortcut profession) routes
    // through `craft <profession> …`; enchanting/artificing have their own
    // verbs. `verb` and `name` come from the feed; sendCmd sanitizes.
    function profCmd(p, sub) {
        // First word only: the parser prefix-matches profession names, and a
        // multi-word name would spill its tail into the argument slot.
        var word = String(p.name || "").toLowerCase().split(/\s+/)[0];
        var base = (p.verb && p.verb !== "craft") ? p.verb : "craft " + word;
        return sub ? base + " " + sub : base;
    }
    // Shared profession difficulty buckets (docs/gmcp_feeds.md — part of the
    // GMCP contract; mirrors the game's recipe_skillup_tiers / harvest tiers).
    // delta = required_rank − your rank.
    function profTier(delta) {
        if (delta <= -4) return "trivial";
        if (delta <= -1) return "easy";
        if (delta <= 3) return "medium";
        if (delta <= 5) return "hard";
        return "blocked";
    }
    function professionById(id) {
        var list = S.professions || [];
        for (var i = 0; i < list.length; i++) {
            if (list[i] && list[i].id === id) return list[i];
        }
        return null;
    }
    // The player's Enchanting standing (identified by its command verb), or
    // null — gates the disenchant context-menu entry.
    function enchanterStanding() {
        var list = S.professions || [];
        for (var i = 0; i < list.length; i++) {
            if (list[i] && list[i].verb === "enchant") return list[i];
        }
        return null;
    }
    // Carried vnum→count map for the craftable-now join: inventory items,
    // pouch components, open container contents, and worn gear — the same
    // scope as the game's portable-component check. Entries without a vnum
    // simply don't count (the game re-validates anyway).
    function inventoryVnumCounts() {
        var counts = {};
        function add(list) {
            (list || []).forEach(function (it) {
                if (!it) return;
                if (it.vnum != null) counts[it.vnum] = (counts[it.vnum] || 0) + (Number(it.count) || 1);
                if (it.contents && !it.closed) add(it.contents);
            });
        }
        if (S.inventory) { add(S.inventory.items); add(S.inventory.components); }
        add(S.equipment);
        return counts;
    }
    // How many of a recipe the carried components allow, mirroring the game's
    // recipe_available_count: min over item + treasure components of
    // floor(have / need). Location components are display-only (the in-game
    // `available` filter skips them too — "what could I craft if I traveled
    // there"). Returns Infinity when nothing material bounds it (craftable,
    // but not limited by mats — e.g. a location-only or component-free recipe).
    function recipeCraftCount(r, counts, treasure) {
        var comps = (r && r.components) || [];
        var min = Infinity;
        for (var i = 0; i < comps.length; i++) {
            var comp = comps[i];
            if (!comp) continue;
            if (comp.kind === "item") {
                var need = Number(comp.count) || 1;
                if (need > 0) min = Math.min(min, Math.floor((counts[comp.vnum] || 0) / need));
            } else if (comp.kind === "treasure") {
                var amt = Number(comp.amount) || 0;
                if (amt > 0) min = Math.min(min, Math.floor(treasure / amt));
            }
        }
        return min;
    }
    // Craftable-now: the same portable-components join as the game's `available`
    // filter (≥ 1 of everything material; location requirements ignored).
    function recipeCraftable(r, counts, treasure) {
        return recipeCraftCount(r, counts, treasure) >= 1;
    }
    // One-line component summary for a recipe row's native tooltip.
    function recipeComponentsText(r) {
        return ((r && r.components) || []).map(function (comp) {
            if (!comp) return "";
            if (comp.kind === "item") return (Number(comp.count) || 1) + "× " + stripColor(comp.name || "component");
            if (comp.kind === "treasure") return comp.amount + " gold of treasure";
            if (comp.kind === "location") return "requires " + (comp.label || "a location");
            return "";
        }).filter(Boolean).join(" · ");
    }
    // Inventory items matching an enchant recipe's gear slot — the same join
    // the game performs (get_gear_type(item) == recipe->target_gear_type).
    // Enchant targets resolve from carried items only (the command is FINV).
    function enchantTargets(r) {
        var out = [];
        ((S.inventory && S.inventory.items) || []).forEach(function (it) {
            if (it && it.gear_type != null && it.gear_type === r.target_gear_type) out.push(it);
        });
        return out;
    }
    function dismissProfessionsWindow() {
        // Command output lands in the terminal — get the window out of the
        // way on every form factor.
        if (mqMobile.matches) { if (sheetName) setSheet(null); }
        else if (overlayName) setOverlay(null);
    }
    function profBtn(label, fn, cls) {
        return el("button", { type: "button", class: "prof-btn" + (cls ? " " + cls : ""), text: label, onclick: fn });
    }
    // Session-local recipe-browser UI state.
    var profOpen = {};       // profession id → recipe list unfolded
    var recipeOpen = {};     // recipe id → component/queue detail unfolded
    var catCollapsed = {};   // "pid:category" → section folded
    var recipeQty = {};      // recipe id → chosen craft quantity (queue stepper)
    var profSearch = {};     // profession id → recipe search string
    var profCat = {};        // profession id → selected category ("" = all)
    var profAvailOnly = false;   // global "craftable now" filter (persisted)
    try { profAvailOnly = localStorage.getItem("ishar.profAvailOnly") === "1"; } catch (e) {}
    function persistProfAvail() {
        try { localStorage.setItem("ishar.profAvailOnly", profAvailOnly ? "1" : "0"); } catch (e) {}
    }

    // Category display order. The game lists categories alphabetically; the web
    // browser reads them by paperdoll slot instead — head → feet, with the
    // held items (weapon, shield) in their worn position (below hands/gloves,
    // above the waist) rather than dangling at the end. Any unknown category
    // falls to a middle band (alpha); transmutation / general sink to the
    // bottom. Keeps Enchanting's gear-slot categories in paperdoll order
    // rather than the alphabetical Body → Feet → Head → Shield → …
    var CATEGORY_ORDER = [
        "head", "face", "eyes", "ears", "neck", "throat", "about",
        "shoulders", "back", "body", "torso", "chest",
        "arms", "wrist", "wrists", "hands", "gloves", "finger", "ring",
        "weapon", "shield",
        "waist", "belt", "legs", "feet"
    ];
    var CATEGORY_BOTTOM = { transmutation: 1, general: 2, miscellaneous: 3, misc: 3, other: 4 };
    function categoryRank(name) {
        var key = String(name || "").trim().toLowerCase();
        if (CATEGORY_BOTTOM[key]) return 900 + CATEGORY_BOTTOM[key];
        var i = CATEGORY_ORDER.indexOf(key);
        if (i >= 0) return 100 + i;
        return 500;   // unknown category — ordered alphabetically within its band
    }
    function sortRecipes(list) {
        return list.slice().sort(function (a, b) {
            var ra = categoryRank(a.category), rb = categoryRank(b.category);
            if (ra !== rb) return ra - rb;
            var ca = String(a.category || "").toLowerCase(), cb = String(b.category || "").toLowerCase();
            if (ca !== cb) return ca < cb ? -1 : 1;   // separate same-band categories alpha
            return (Number(a.min_rank) || 0) - (Number(b.min_rank) || 0);
        });
    }

    // The tappable component breakdown under a recipe row — the touch path
    // to "what am I missing?" (the hover title is desktop convenience only).
    function recipeCompsBlock(r, counts, treasure) {
        var block = el("div", { class: "recipe-comps" });
        ((r && r.components) || []).forEach(function (comp) {
            if (!comp) return;
            var ok, text;
            if (comp.kind === "item") {
                var need = Number(comp.count) || 1;
                var have = counts[comp.vnum] || 0;
                ok = have >= need;
                text = need + "× " + stripColor(comp.name || "component") + " (have " + have + ")";
            } else if (comp.kind === "treasure") {
                var amt = Number(comp.amount) || 0;
                ok = treasure >= amt;
                text = amt + " gold of treasure (have " + treasure + ")";
            } else if (comp.kind === "location") {
                ok = null;   // display-only; never blocks craftable
                text = "requires " + (comp.label || "a location");
            } else {
                return;
            }
            block.appendChild(el("div", {
                class: "recipe-comp" + (ok === true ? " ok" : ok === false ? " missing" : " loc"),
                text: text
            }));
        });
        if (!block.firstChild) block.appendChild(el("div", { class: "recipe-comp loc", text: "No components required." }));
        return block;
    }

    // The batch-craft station for a targetless recipe (the game chains crafts
    // with `<verb> <recipe> <count>`, capped at 99). A keyboard-free stepper
    // plus an editable count and a Max shortcut = the components on hand. The
    // −/+/Max buttons and the field update in place (no re-render) so typing
    // stays smooth and focus never drops.
    function recipeQueue(p, r, count) {
        var craftable = count >= 1;
        var maxMake = (count === Infinity) ? 99 : Math.max(1, Math.min(99, count));
        var q = Math.max(1, Math.min(99, Math.floor(Number(recipeQty[r.id]) || 1)));
        recipeQty[r.id] = q;
        var num = el("input", {
            type: "text", inputmode: "numeric", class: "recipe-qty-num",
            value: String(q), "aria-label": "Quantity to craft"
        });
        var craftBtn = profBtn(q > 1 ? "Craft ×" + q : "Craft", function () {
            var n = Math.max(1, Math.min(99, Math.floor(Number(recipeQty[r.id]) || 1)));
            sendCmd(profCmd(p, nameOf(r.name) + (n > 1 ? " " + n : "")));
            dismissProfessionsWindow();
        }, "recipe-queue-craft" + (craftable ? "" : " off"));
        function setQ(v, writeField) {
            v = Math.max(1, Math.min(99, Math.floor(Number(v) || 1)));
            recipeQty[r.id] = v;
            if (writeField) num.value = String(v);
            craftBtn.textContent = v > 1 ? "Craft ×" + v : "Craft";
        }
        num.addEventListener("input", function () { setQ(num.value, false); });
        num.addEventListener("change", function () { num.value = String(recipeQty[r.id]); });
        num.addEventListener("blur", function () { num.value = String(recipeQty[r.id]); });
        return el("div", { class: "recipe-queue" }, [
            el("span", { class: "recipe-queue-label", text: "Make" }),
            profBtn("−", function () { setQ(recipeQty[r.id] - 1, true); }, "recipe-qty-btn"),
            num,
            profBtn("+", function () { setQ(recipeQty[r.id] + 1, true); }, "recipe-qty-btn"),
            profBtn("Max", function () { setQ(maxMake, true); }, "recipe-qty-max"),
            craftBtn
        ]);
    }

    function recipeRow(p, r, counts, treasure) {
        var rank = Number(p.rank) || 0;
        var tier = profTier((Number(r.min_rank) || 1) - rank);
        var count = recipeCraftCount(r, counts, treasure);
        var craftable = count >= 1;
        var targeted = r.target_gear_type != null;
        var isOpen = !!recipeOpen[r.id];
        // Craftable-count badge (#8) — distinct from the rank: a green ×N (how
        // many the components allow) or ✓ (ready, mats-unbounded / targeted),
        // or a red "Missing". Replaces the old bare ✓.
        var availBadge;
        if (!craftable) {
            availBadge = el("span", { class: "tag recipe-avail missing", title: "Missing components", text: "Missing" });
        } else if (targeted || count === Infinity) {
            availBadge = el("span", { class: "tag recipe-avail ok", title: "Components ready", text: "✓" });
        } else {
            availBadge = el("span", { class: "tag recipe-avail ok", title: "You can make " + count + " with your components", text: "×" + count });
        }
        // Inline action. Enchants keep their item picker (single target, no
        // chaining). Targetless crafts get a quick Craft-one here; the batch
        // queue lives in the disclosed detail, so hide this button when open.
        var actions = [];
        if (targeted) {
            var targets = enchantTargets(r);
            actions.push(profBtn("Enchant…", function (e) {
                var opener = e && e.target && e.target.closest(".prof-btn");
                // Second tap on the opener toggles the picker closed.
                if (menuOpen && menuAnchorEl === opener) { closeMenu(); return; }
                var acts = targets.map(function (it) {
                    return {
                        label: stripColor(it.name || "item"),
                        fn: function () {
                            // `enchant <item> <recipe>` (fabricate likewise).
                            sendCmd(profCmd(p, targetOf(it.keywords || it.name) + " " + nameOf(r.name)));
                            dismissProfessionsWindow();
                        }
                    };
                });
                if (!acts.length) acts = [{ label: "No matching item carried", fn: function () {}, keep: true }];
                openMenu("Enchant · " + stripColor(r.name || ""), acts, opener);
            }, "menu-opener" + (targets.length ? "" : " off")));   // .menu-opener: exempt from outside-click dismissal
        } else if (!isOpen) {
            actions.push(profBtn("Craft", function () {
                sendCmd(profCmd(p, nameOf(r.name)));
                dismissProfessionsWindow();
            }, craftable ? "" : "off"));
        }
        var row = el("div", { class: "recipe-row", title: recipeComponentsText(r) || null }, [
            el("button", {
                type: "button", class: "recipe-toggle", "data-focus": "r" + r.id,
                "aria-expanded": isOpen ? "true" : "false",
                onclick: function () { closeMenu(); recipeOpen[r.id] = !recipeOpen[r.id]; renderProfessions(); }
            }, [
                el("span", { class: "recipe-name tier-" + tier, text: stripColor(r.name || "?") })
            ]),
            el("span", { class: "tag recipe-rank tier-" + tier, title: "Minimum rank " + (r.min_rank != null ? r.min_rank : "?"), text: (r.min_rank != null ? String(r.min_rank) : "?") }),
            availBadge,
            el("span", { class: "prof-actions" }, actions)
        ]);
        var wrap = el("div", { class: "recipe-item" }, [row]);
        if (isOpen) {
            wrap.appendChild(recipeCompsBlock(r, counts, treasure));
            if (!targeted) wrap.appendChild(recipeQueue(p, r, count));
        }
        return wrap;
    }

    // The overlay/sheet body that scrolls the panel — saved/restored across
    // rebuilds so a filter/collapse/keystroke doesn't snap a long list to top.
    function profScrollParent() {
        var n = dom.professions && dom.professions.parentElement;
        while (n) {
            var oy = "";
            try { oy = getComputedStyle(n).overflowY; } catch (e) {}
            if ((oy === "auto" || oy === "scroll") && n.scrollHeight > n.clientHeight + 1) return n;
            n = n.parentElement;
        }
        return null;
    }

    function renderProfessions() {
        if (!dom.professions) return;
        // Wholesale rebuilds run on every inventory delta while the overlay is
        // open (and on every search keystroke) — carry keyboard focus + caret
        // across (a11y: don't dump a keyboard/switch user to <body>), and hold
        // the scroll position.
        var focusKey = null, caretPos = null;
        var ae = document.activeElement;
        if (ae && dom.professions.contains(ae) && ae.getAttribute) {
            focusKey = ae.getAttribute("data-focus");
            if (ae.tagName === "INPUT" && ae.selectionStart != null) {
                try { caretPos = ae.selectionStart; } catch (e) {}
            }
        }
        var sc = profScrollParent();
        var savedTop = sc ? sc.scrollTop : 0;
        var kids = [];
        var c = S.craft;
        if (c) {
            var rem = Math.max(0, c.expiry - now());
            var pct = Math.max(0, Math.min(100, (1 - rem / c.total) * 100));
            var label = (c.kind === "harvest" ? "Harvesting" : "Crafting") + " — " + c.name
                + (c.quantity > 1 ? " ×" + c.quantity : "")
                + (c.chain > 0 ? " (+" + c.chain + " queued)" : "");
            kids.push(el("div", { class: "craft-activity" }, [
                el("div", { class: "craft-label", text: label }),
                el("div", { class: "craft-track" }, [
                    el("div", { class: "craft-fill", style: "width:" + pct + "%" }),
                    el("span", { class: "craft-time", text: fmtDur(rem) })
                ])
            ]));
        }
        var profs = S.professions || [];
        if (!profs.length && !c) {
            kids.push(el("div", { class: "prof-empty", text: "No professions yet. Seek out a profession master to learn one." }));
            fill(dom.professions, kids);
            return;
        }
        var counts = inventoryVnumCounts();
        var treasure = (S.inventory && Number(S.inventory.treasure)) || 0;
        profs.forEach(function (p) {
            var rank = Number(p.rank) || 0;
            var maxRank = Number(p.max_rank) || 0;
            var pct = maxRank > 0 ? Math.max(0, Math.min(100, (rank / maxRank) * 100)) : 100;
            var isOpen = !!profOpen[p.id];
            var recipes = (S.recipes || []).filter(function (r) { return r && r.profession_id === p.id; });
            var row = el("div", { class: "prof-row" }, [
                el("button", {
                    type: "button", class: "prof-head", "data-focus": "p" + p.id,
                    "aria-expanded": isOpen ? "true" : "false",
                    onclick: function () { closeMenu(); profOpen[p.id] = !profOpen[p.id]; renderProfessions(); }
                }, [
                    el("span", { class: "prof-caret", "aria-hidden": "true", text: isOpen ? "▾" : "▸" }),
                    el("span", { class: "prof-name", text: p.name || "?" }),
                    p.tier ? el("span", { class: "tag prof-tier", text: p.tier }) : null,
                    el("span", { class: "prof-rank", text: "Rank " + rank + (maxRank ? "/" + maxRank : "") })
                ]),
                el("div", { class: "prof-track", title: maxRank ? rank + " of " + maxRank + " ranks" : "Rank " + rank }, [
                    el("div", { class: "prof-fill", style: "width:" + pct + "%" })
                ]),
                el("div", { class: "prof-foot" }, [
                    el("span", { class: "prof-recipes", text: "Recipes " + (p.recipes_known != null ? p.recipes_known : "–") + "/" + (p.recipes_total != null ? p.recipes_total : "–") })
                ])
            ]);
            if (isOpen) {
                var pid = p.id;
                var sorted = sortRecipes(recipes);
                // The full ordered category set — the chip list, independent of
                // what the active search/filter currently shows.
                var catList = [];
                sorted.forEach(function (r) {
                    var cat = String(r.category || "General");
                    if (catList.indexOf(cat) === -1) catList.push(cat);
                });
                var searchVal = profSearch[pid] || "";
                var q = searchVal.trim().toLowerCase();
                var selCat = profCat[pid] || "";
                if (selCat && catList.indexOf(selCat) === -1) selCat = profCat[pid] = "";   // recipe forgotten → stale category

                // Controls: search + Available toggle + category chips. Only when
                // there's something to browse (a 0-recipe profession skips them).
                if (recipes.length) {
                    var searchInput = el("input", {
                        type: "text", class: "recipe-search", "data-focus": "search-" + pid,
                        placeholder: "Search recipes…", autocomplete: "off", spellcheck: "false",
                        value: searchVal, "aria-label": "Search recipes"
                    });
                    searchInput.addEventListener("input", function () { profSearch[pid] = searchInput.value; renderProfessions(); });
                    var chips = el("div", { class: "recipe-chips" });
                    chips.appendChild(el("button", {
                        type: "button", class: "recipe-chip avail" + (profAvailOnly ? " on" : ""),
                        "data-focus": "avail-" + pid,
                        onclick: function () { profAvailOnly = !profAvailOnly; persistProfAvail(); renderProfessions(); },
                        text: "✓ Available"
                    }));
                    var catChip = function (label, val) {
                        return el("button", {
                            type: "button", class: "recipe-chip" + (selCat === val ? " on" : ""),
                            onclick: function () { profCat[pid] = (selCat === val ? "" : val); renderProfessions(); },
                            text: label
                        });
                    };
                    chips.appendChild(catChip("All", ""));
                    catList.forEach(function (cat) { chips.appendChild(catChip(cat, cat)); });
                    row.appendChild(el("div", { class: "recipe-controls" }, [searchInput, chips]));
                }

                var shown = sorted.filter(function (r) {
                    if (q && stripColor(r.name || "").toLowerCase().indexOf(q) === -1) return false;
                    if (selCat && String(r.category || "General") !== selCat) return false;
                    if (profAvailOnly && !recipeCraftable(r, counts, treasure)) return false;
                    return true;
                });

                var listEl = el("div", { class: "recipe-list" });
                if (!recipes.length) {
                    listEl.appendChild(el("div", { class: "prof-empty", text: "No recipes known yet — trainers and discovery await." }));
                } else if (!shown.length) {
                    listEl.appendChild(el("div", { class: "prof-empty", text: "No recipes match." }));
                } else {
                    var byCat = {}, order = [];
                    shown.forEach(function (r) {
                        var cat = String(r.category || "General");
                        if (!byCat[cat]) { byCat[cat] = []; order.push(cat); }
                        byCat[cat].push(r);
                    });
                    order.forEach(function (cat) {
                        var key = pid + ":" + cat;
                        var collapsed = !!catCollapsed[key];
                        listEl.appendChild(el("button", {
                            type: "button", class: "recipe-cat" + (collapsed ? " collapsed" : ""),
                            "data-focus": "cat-" + pid + "-" + cat.replace(/[^a-z0-9]+/gi, "_"),
                            "aria-expanded": collapsed ? "false" : "true",
                            onclick: (function (k, was) { return function () { closeMenu(); catCollapsed[k] = !was; renderProfessions(); }; })(key, collapsed)
                        }, [
                            el("span", { class: "recipe-cat-caret", "aria-hidden": "true", text: collapsed ? "▸" : "▾" }),
                            el("span", { class: "recipe-cat-name", text: cat }),
                            el("span", { class: "recipe-cat-count", text: String(byCat[cat].length) })
                        ]));
                        if (!collapsed) byCat[cat].forEach(function (r) { listEl.appendChild(recipeRow(p, r, counts, treasure)); });
                    });
                }
                row.appendChild(listEl);
            }
            kids.push(row);
        });
        kids.push(el("div", { class: "prof-hint", text: "profession — overview & trainers · harvest <node> — gather" }));
        fill(dom.professions, kids);
        if (sc) sc.scrollTop = savedTop;
        if (focusKey && /^[a-z0-9_-]+$/i.test(focusKey)) {
            var refocus = dom.professions.querySelector('[data-focus="' + focusKey + '"]');
            if (refocus) {
                refocus.focus();
                if (caretPos != null && refocus.setSelectionRange) {
                    try { refocus.setSelectionRange(caretPos, caretPos); } catch (e) {}
                }
            }
        }
        tickCraft();
    }

    // ------------------------------------------------------------------
    // Context / action menu (works with mouse + touch)
    // ------------------------------------------------------------------
    // Single guarded exit for every game command a widget builds — strips
    // control chars / newlines so a keyword or server handle can never smuggle
    // a second command onto the line.
    function sendCmd(c) { c = safeCmd(c); if (c) api.send(c); }

    var menuOpen = false;
    var menuAnchorEl = null;   // the element the open menu was anchored to
    function closeMenu() {
        if (!menuOpen) return;
        menuOpen = false;
        menuAnchorEl = null;
        dom.menu.hidden = true;
        dom.menu.classList.remove("menu-picker");
        while (dom.menu.firstChild) dom.menu.removeChild(dom.menu.firstChild);
    }
    // The icon picker: a grouped grid of the curated game-icons, plus "Auto"
    // (clear the override). Reuses the menu container with a wider grid layout.
    function openIconPicker(s, anchor) {
        closeMenu();
        var key = slotKeyOf(s);
        var kids = [el("div", { class: "menu-title", text: "Icon · " + s.name })];
        var autoBtn = el("button", { type: "button", class: "picker-auto" + (iconOverrides[key] ? "" : " on"), title: "Use the automatic icon" }, [
            iconSvg(standardIcon(s), "gi"), el("span", { text: "Auto" })
        ]);
        autoBtn.addEventListener("click", function () { setIcon(s.name, null); closeMenu(); });
        kids.push(autoBtn);
        ICON_PALETTE.forEach(function (group) {
            kids.push(el("div", { class: "picker-group", text: group[0] }));
            var grid = el("div", { class: "picker-grid" });
            group[1].forEach(function (nm) {
                var b = el("button", {
                    type: "button", class: "picker-icon" + (iconOverrides[key] === nm ? " on" : ""),
                    title: nm, "aria-label": nm
                }, [iconSvg(nm, "gi")]);
                b.addEventListener("click", function () { setIcon(s.name, nm); closeMenu(); });
                grid.appendChild(b);
            });
            kids.push(grid);
        });
        dom.menu.classList.add("menu-picker");
        fill(dom.menu, kids);
        dom.menu.hidden = false;
        menuOpen = true;
        positionMenu(anchor);
    }
    // actions: [{label, cmd|prefill|fn, danger, tier, disabled}]. Anchored
    // near `anchor`. `disabled` renders an inert greyed row — used for
    // actions that exist but the player can't take yet (harvest rank gates),
    // so the requirement is visible instead of the action silently missing.
    function openMenu(title, actions, anchor) {
        closeMenu();
        hideTip();
        actions = actions.filter(Boolean);
        if (!actions.length) return;
        var kids = [el("div", { class: "menu-title", text: title })];
        actions.forEach(function (a) {
            // No data-cmd/data-prefill here on purpose: the delegated app-click
            // handler would fire the command a *second* time. The onclick owns
            // the action outright.
            kids.push(el("button", {
                type: "button",
                class: "menu-item" + (a.danger ? " danger" : "") + (a.tier ? " tier-" + a.tier : "") + (a.disabled ? " disabled" : ""),
                disabled: a.disabled ? true : null,
                text: a.label,
                onclick: function () {
                    if (a.disabled) return;
                    // Close BEFORE running the action: an fn may open its own
                    // surface (icon picker, a confirm submenu) and a
                    // close-after would immediately dismiss it.
                    closeMenu();
                    if (a.fn) a.fn();
                    else if (a.prefill != null) api.prefill(a.prefill);
                    else if (a.cmd) sendCmd(a.cmd);
                    // `keep`: informational rows shouldn't throw away the
                    // phone sheet the menu was opened from.
                    if (!a.keep && sheetName && mqMobile.matches) setSheet(null);
                }
            }));
        });
        fill(dom.menu, kids);
        dom.menu.hidden = false;
        menuOpen = true;
        menuAnchorEl = anchor || null;
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
    // else only offensive ones. Bar spells first (keeps it your curated set),
    // else usable ones.
    function occupantCastActions(o, max) {
        var want = o.hostile_hint === "friendly" ? "defensive" : "offensive";
        var spells = (S.skills || []).filter(function (s) {
            return s.type === "spell" && s.target_type === want;
        });
        var onbar = spells.filter(function (s) { return onBar(slotKeyOf(s)); });
        var pick = onbar.length ? onbar : spells.filter(function (s) { return !abilityBlock(s); });
        return pick.slice(0, max || 6).map(function (s) {
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
        // State-contingent verbs FIRST — they exist because of the target's
        // current posture, so they outrank the evergreen casts. They key off
        // the relationship fields, NOT the friendly hint: a player following
        // you while un-grouped reads "neutral" but is exactly who yank is
        // for. The game re-validates everything.
        if (occSleeping(o) && (friendly || o.is_my_follower)) {
            acts.push({ label: "Wake", cmd: "wake " + o.handle });
        }
        if (o.is_my_follower && occSeated(o)) {
            acts.push({ label: "Yank to feet", cmd: "yank " + o.handle });
        }
        // Posture orders for a loyal follower — only ones that change
        // anything, and none while it sleeps (can't hear you; Wake first).
        if (o.is_loyal_follower && !occSleeping(o)) {
            ["stand", "rest", "sleep"].forEach(function (p) {
                var current = posLower(o) === (p === "stand" ? "standing" : p === "rest" ? "resting" : "sleeping");
                if (!current) acts.push({ label: "Order: " + p, cmd: "order " + o.handle + " " + p });
            });
        }
        // Cast a chosen spell straight at THIS occupant (not the default
        // target). Capped tighter on allies, whose menus carry state verbs.
        occupantCastActions(o, friendly ? 4 : 6).forEach(function (a) { acts.push(a); });
        if (!friendly) {
            acts.push({ label: "Attack", cmd: "kill " + o.handle, danger: true });
            // Sic your loyal followers on it. Bare keyword, not the handle:
            // each follower resolves ordinals from its OWN perspective, so a
            // viewer-relative "2.thug" could hit the wrong one for them —
            // and with duplicate keywords in the room, say so on the label.
            if (anyLoyalFollowerHere()) {
                var kw = firstWord(o.keyword);
                var dupes = (S.occupants || []).some(function (x) {
                    return x !== o && !x.is_dead && x.hostile_hint !== "friendly"
                        && firstWord(x.keyword).toLowerCase() === kw.toLowerCase();
                });
                acts.push({ label: dupes ? "Order attack (any " + kw + ")" : "Order attack",
                            cmd: "order followers kill " + kw, danger: true });
            }
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
        if (friendly) {
            // Attack on an ally stays possible (PK duels, charm gone wrong)
            // but dead last — never adjacent to Wake/Yank/heals a shaky
            // thumb is aiming for.
            acts.push({ label: "Attack", cmd: "kill " + o.handle, danger: true });
        }
        return acts;
    }

    // Actions for a ground object (Room.Contents item). Commands target the
    // server-computed handle so duplicates ("2.corpse.rat") resolve to the
    // exact instance; the server re-validates everything.
    function groundItemActions(it) {
        var h = groundTarget(it);
        var acts = [{ label: "Look", cmd: "look " + h }];
        var isContainer = it.type === "container";
        var hasContents = !!(it.contents && it.contents.length);
        if (it.is_corpse) {
            if (hasContents) acts.push({ label: "Loot all", cmd: "get all from " + h });
            if (it.harvest) acts.push(harvestAction(it.harvest, h));
        } else if (isContainer) {
            // Offer Open/Close on any closeable container, locked included: a
            // locked coffer is closed, so this reads "Open" and the game
            // refuses it server-side ("It's locked.") — surfacing the verb the
            // player would reach for beats a dead "Locked" row that offers no
            // way to try. Mirrors the inventory container menu.
            if (it.closeable) {
                acts.push(it.closed ? { label: "Open", cmd: "open " + h } : { label: "Close", cmd: "close " + h });
            }
            if (!it.closed && hasContents) acts.push({ label: "Get all from", cmd: "get all from " + h });
        }
        // no_take = scenery ("You can't seem to budge...") — omit dead verbs.
        if (!it.no_take && !it.is_corpse) acts.push({ label: "Get", cmd: "get " + h });
        if (it.is_corpse) {
            // Sacrifice lives HERE and only here (the command takes a corpse
            // on the ground, never a carried item) — last and danger-styled.
            // No confirm, matching the game: sacrificing spills any contents
            // onto the ground and consumes only the corpse itself, so a
            // mis-tap costs nothing but the body.
            acts.push({ label: "Sacrifice", cmd: "sacrifice " + h, danger: true });
        }
        return acts;
    }
    function harvestAction(hv, target) {
        var hs = harvestStanding(hv);
        if (hs.untrained) {
            return { label: "Harvest — requires " + (hv.profession || "training"), disabled: true };
        }
        if (!hs.ok) return { label: "Harvest (r" + hs.req + ") — rank too low", disabled: true };
        return { label: "Harvest (r" + hs.req + ")", cmd: "harvest " + target, tier: hs.tier || undefined };
    }
    function groundContentActions(ds) {
        return [
            { label: "Get", cmd: "get " + ds.target + " from " + ds.container }
        ];
    }
    function nodeActions(n) {
        var t = nodeTarget(n);
        return [
            { label: "Look", cmd: "look " + t },
            harvestAction(n, t)
        ];
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
            // Profession context: enchanters see the disenchant path with the
            // item's rank requirement, colored by the standard difficulty
            // buckets (docs/gmcp_feeds.md). The game re-validates the rank.
            var ench = enchanterStanding();
            if (ench && ds.disen > 0 && kind !== "content") {
                acts.push({
                    label: "Disenchant (r" + ds.disen + ")",
                    cmd: "disenchant " + t,
                    tier: profTier(ds.disen - (Number(ench.rank) || 0))
                });
            }
            // No Sacrifice here: the command only accepts a corpse on the
            // ground, so it lives on the Room panel's corpse menu instead.
            acts.push({ label: "Drop", cmd: "drop " + t });
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
    function abilityActions(s, anchor) {
        if (!s) return [];
        var key = slotKeyOf(s);
        var idx = slotIndexOf(key);
        var pinned = idx !== -1;
        var acts = [];
        var cmd = abilityCommand(s);
        if (cmd) acts.push({ label: s.type === "spell" ? "Cast" : "Use", fn: function () { sendCmd(cmd); } });
        acts.push({ label: pinned ? "★ Remove from bar" : "☆ Add to bar", fn: function () { toggleSlot(s.name); } });
        // Nudge along the bar (only meaningful once it's on the bar).
        if (pinned) {
            if (idx % SLOTS_PER_PAGE > 0) acts.push({ label: "Move ◄ left", fn: function () { moveSlot(idx, -1); } });
            if (idx % SLOTS_PER_PAGE < SLOTS_PER_PAGE - 1 && idx + 1 < SLOT_MAX) acts.push({ label: "Move ► right", fn: function () { moveSlot(idx, 1); } });
        }
        acts.push({ label: "Choose icon…", fn: function () { openIconPicker(s, anchor); } });
        if (iconOverrides[key]) acts.push({ label: "Reset icon", fn: function () { setIcon(s.name, null); } });
        acts.push({ label: "Look up", cmd: "skill search " + nameOf(s.name) });
        return acts;
    }
    // Assign an ability to a specific slot index (used by empty-slot menus).
    function slotAssignActions(idx) {
        var usable = (S.skills || []).filter(function (s) { return s.type === "spell" || s.type === "skill"; });
        // Bar spells/skills first would be redundant here; offer usable ones,
        // alphabetical, capped so the menu stays tap-sized.
        usable.sort(function (a, b) {
            var ba = abilityBlock(a) ? 1 : 0, bb = abilityBlock(b) ? 1 : 0;
            if (ba !== bb) return ba - bb;
            return String(a.name).localeCompare(String(b.name));
        });
        return usable.slice(0, 12).map(function (s) {
            return { label: s.name, fn: function () { assignSlot(idx, slotKeyOf(s)); } };
        });
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
        // 1b) Container expand carets — checked before the row's own action
        // menu so a tap on the caret only toggles its contents.
        var exp = e.target.closest("[data-expand]");
        if (exp && dom.app.contains(exp)) {
            var ekey = exp.getAttribute("data-expand");
            if (expanded[ekey]) delete expanded[ekey]; else expanded[ekey] = true;
            saveSet("ishar.itemsExpanded", expanded);
            renderEquipment();
            renderInventory();
            renderOccupants();   // ground containers expand in the Room panel
            api.onLayoutChange();
            e.preventDefault();
            return;
        }

        // 2) Action-bar page toggle.
        var pager = e.target.closest("[data-pager]");
        if (pager && dom.app.contains(pager)) { flipHotbarPage(); return; }

        // 2a) Lock toggle.
        var lockBtn = e.target.closest("[data-lock]");
        if (lockBtn && dom.app.contains(lockBtn)) { toggleBarLock(); return; }

        // 2b) Edit mode (unlocked): a tap on a slot rearranges instead of firing —
        // pick a slot, then tap where it should go. Prevents accidental casts.
        if (!barLocked) {
            var editSlot = e.target.closest(".skill[data-slot]");
            if (editSlot && dom.hotbar.contains(editSlot)) { pickOrPlace(Number(editSlot.getAttribute("data-slot"))); return; }
        }

        // 2d) Ability chip filters + bar-pin star.
        var chip = e.target.closest("[data-abtype],[data-abusable]");
        if (chip && dom.app.contains(chip)) {
            if (chip.hasAttribute("data-abtype")) abilityFilter.type = chip.getAttribute("data-abtype");
            else abilityFilter.usableOnly = !abilityFilter.usableOnly;
            persistAbilityFilter();
            renderAbilities();
            return;
        }
        var star = e.target.closest("[data-bar]");
        if (star && dom.app.contains(star)) { toggleSlot(star.getAttribute("data-bar")); return; }

        // 3) Ability cast (hotbar button or abilities row) — not the star.
        var ab = e.target.closest("[data-ability]");
        if (ab && dom.app.contains(ab) && !e.target.closest("[data-bar]") && !e.target.closest(".row-more")) {
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
        } else if (kind === "grounditem") {
            var gi = (S.roomItems || [])[Number(host.getAttribute("data-idx"))];
            if (gi) openMenu(stripColor(gi.name || ""), groundItemActions(gi), anchor);
        } else if (kind === "groundcontent") {
            var gds = readDataset(host);
            openMenu(gds.name || gds.target, groundContentActions(gds), anchor);
        } else if (kind === "node") {
            var nd = (S.roomNodes || [])[Number(host.getAttribute("data-idx"))];
            if (nd) openMenu(stripColor(nd.name || ""), nodeActions(nd), anchor);
        } else if (kind === "component") {
            var cds = readDataset(host);
            openMenu(cds.name || cds.target, componentActions(cds), anchor);
        } else if (kind === "ability") {
            var s2 = skillById(host.getAttribute("data-ability"));
            if (s2) openMenu(s2.name, abilityActions(s2, anchor), anchor);
        } else if (kind === "slot") {
            var si = Number(host.getAttribute("data-slot"));
            openMenu("Slot " + slotLabel(si), slotAssignActions(si), anchor);
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
            closed: host.getAttribute("data-closed") === "1",
            disen: Number(host.getAttribute("data-disen")) || 0
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
        if (mobile && overlayName) setOverlay(null);
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
        if (overlayByKey(name)) { overlayByKey(name).render(); markOverlayUnread(name, false); }
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
        if (!on && overlayName) setOverlay(null);   // no orphaned overlay behind a hidden HUD
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
    function setConnected(on) {
        S.connected = !!on;
        renderVitals();
        if (mapMod) mapMod.onConnected(S.connected);
    }

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
        renderProfessions(); updateMicro();
    }
    function reset() {
        S.vitals = null; S.status = null; S.time = null; S.room = null;
        S.equipment = []; S.inventory = null; S.train = null;
        S.affects = null; S.group = null; S.who = null; S.occupants = [];
        S.roomItems = []; S.roomNodes = [];
        S.skills = []; S.cooldownExpiry = {}; S.cooldownTotal = {}; S.usable = {};
        S.professions = []; S.recipes = []; S.craft = null;
        S.tgtHostile = null; S.tgtFriendly = null;
        lastVitalsBody = null;
        lastProfessionsBody = null;
        if (mapMod) mapMod.onReset();
        renderAll();
    }

    function init(opts) {
        opts = opts || {};
        if (opts.send) api.send = opts.send;
        if (opts.prefill) api.prefill = opts.prefill;
        if (opts.onLayoutChange) api.onLayoutChange = opts.onLayoutChange;
        if (opts.onComm) api.onComm = opts.onComm;
        if (opts.onVitals) api.onVitals = opts.onVitals;
        if (opts.spriteUrl) spriteUrl = String(opts.spriteUrl);
        if (opts.biUrl) biUrl = String(opts.biUrl);
        if (opts.skillIcons && typeof opts.skillIcons === "object") curatedIcons = opts.skillIcons;

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
        dom.micro = document.getElementById("hud-micro");
        dom.professions = document.getElementById("panel-professions");
        dom.overlay = document.getElementById("hud-overlay");
        dom.overlayTitle = document.getElementById("hud-overlay-title");
        dom.dock = document.getElementById("hud-dock");
        dom.sheet = document.getElementById("hud-sheet");
        dom.sheetBody = document.getElementById("hud-sheet-body");
        dom.sheetTitle = document.getElementById("hud-sheet-title");
        dom.menu = document.getElementById("hud-menu");
        dom.roseOverlay = document.getElementById("rose-overlay");
        // One shared tooltip element, created here so no template change is needed.
        dom.tip = document.createElement("div");
        dom.tip.id = "hud-tip";
        dom.tip.className = "hud-tip";
        dom.tip.setAttribute("role", "tooltip");
        dom.tip.hidden = true;
        document.body.appendChild(dom.tip);

        dom.app.addEventListener("click", onAppClick);
        dom.app.addEventListener("contextmenu", onAppContext);
        wireHotbarDrag();
        wireHotkeys();
        wireTooltips();

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

        // Micro-menu: each button toggles its overlay app (sheet on phones).
        if (dom.micro) dom.micro.addEventListener("click", function (e) {
            var b = e.target.closest("button[data-overlay]");
            if (b) toggleOverlay(b.getAttribute("data-overlay"));
        });
        var overlayClose = document.getElementById("hud-overlay-close");
        if (overlayClose) overlayClose.addEventListener("click", function () { setOverlay(null); });

        // Mobile rose overlay toggle button.
        var roseBtn = document.getElementById("rose-toggle");
        if (roseBtn) roseBtn.addEventListener("click", function () {
            roseOverlayOn = !roseOverlayOn;
            try { localStorage.setItem("ishar.roseOverlay", roseOverlayOn ? "1" : "0"); } catch (e) {}
            roseBtn.setAttribute("aria-pressed", roseOverlayOn ? "true" : "false");
            updateRoseOverlay();
        });

        // Outside tap dismisses the sheet, the overlay window and any open menu.
        document.addEventListener("click", function (e) {
            // A click that re-renders its own panel (e.g. a recipe-list
            // disclosure) detaches the target before this listener runs —
            // contains() would then read "outside" and close the surface the
            // click was inside. A disconnected target was always handled by
            // its own onclick; never treat it as an outside click.
            if (e.target && e.target.isConnected === false) return;
            if (menuOpen && !dom.menu.contains(e.target) && !e.target.closest("[data-menu],.row-more,.menu-opener")) closeMenu();
            if (overlayName && !mqMobile.matches && dom.overlay &&
                !dom.overlay.contains(e.target) && !e.target.closest("#hud-micro") &&
                !dom.menu.contains(e.target)) {
                setOverlay(null);
            }
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
            if (S.craft) tickCraft();
        }, 1000);
    }

    // ------------------------------------------------------------------
    // Map subsystem seam — hud-map.js registers here and receives a small
    // context so the mapper reuses this file's primitives (el/fill/send/
    // menus/tips) instead of duplicating them. registerMap runs at script
    // load, before init(); every ctx function resolves its state lazily.
    // ------------------------------------------------------------------
    function registerMap(mod) {
        if (!mod || typeof mod.attach !== "function") return;
        mapMod = mod;
        mod.attach({
            el: el, fill: fill, stripColor: stripColor,
            send: sendCmd,
            prefill: function (t) { api.prefill(t); },
            openMenu: openMenu, closeMenu: closeMenu,
            showTip: showTip, hideTip: hideTip,
            toggleOverlay: toggleOverlay,
            overlayVisible: overlayVisible,
            isMobile: function () { return mqMobile.matches; },
            selfName: function () { return S.status ? String(S.status.name || "") : ""; },
            markUnread: function (on) { markOverlayUnread("map", on); },
            updateMicro: updateMicro,
            rerenderRoom: function () { if (dom.room) renderRoom(); },
            connected: function () { return S.connected; },
            // Autowalk's combat brake: an opponent bar or anyone beating on us.
            inCombat: function () {
                if (S.vitals && S.vitals.opponent_hp_pct != null) return true;
                return (S.occupants || []).some(function (o) { return o.fighting_you && !o.is_dead; });
            }
        });
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
            { id: 92, name: "Shield Slam", type: "skill", percent: 72, usable: true, category: "damage", target_type: "none", min_position: "Fighting" },
            { id: 60, name: "translocate", type: "spell", percent: 84, usable: true, category: "misc", target_type: "defensive", mana_pct: 25, mana: 75, min_position: "Standing" },
            { id: 61, name: "summon", type: "spell", percent: 79, usable: true, category: "misc", target_type: "defensive", mana_pct: 33, mana: 100, min_position: "Standing" }
        ];
        // Pad to demonstrate the immortal overflow the browser now bounds.
        for (var i = 11; i <= 90; i++) bigSkills.push({ id: i, name: "spell " + i, type: (i % 3 ? "spell" : "skill"), percent: 40 + (i % 60), usable: (i % 4 !== 0), category: ["damage", "heal", "misc"][i % 3], target_type: ["offensive", "defensive", "none"][i % 3], mana_pct: 20 + (i % 40), mana: (20 + (i % 40)) * 3, min_position: "Standing" });

        var feeds = {
            "Char.Status": { name: "Aelwyn", "class": "Magician", race: "Elf", position: "Standing", level: 45, align: 350, xp: 1250000, tnl: 48000, gold: 18230, bank: 500000, remort: 3 },
            "Char.Vitals": { hp: 412, maxhp: 480, mp: 130, maxmp: 300, move: 198, maxmove: 240, position: "Standing", opponent_hp_pct: 35, metamagic: 60, metamagic_max: 100, metamagic_regen: 5, food: 27, water: 9 },
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
            "Room.Contents": { items: [
                { name: "the corpse of a sewer rat", keywords: "corpse rat", handle: "1.corpse.rat", type: "container", vnum: -1, count: 1, is_corpse: true,
                  harvest: { profession_id: 1, profession: "Alchemy", required_rank: 30 },
                  closeable: false, closed: false, locked: false, contents: [
                    { name: "a pitted short sword", keywords: "sword short pitted", type: "weapon", vnum: 301, count: 1 },
                    { name: "a mangy rat pelt", keywords: "pelt rat mangy", type: "other", vnum: 302, count: 2 }
                ] },
                { name: "the corpse of an alley thug", keywords: "corpse thug", handle: "1.corpse.thug", type: "container", vnum: -1, count: 1, is_corpse: true,
                  closeable: false, closed: false, locked: false, contents: [] },
                { name: "an iron-banded chest", keywords: "chest iron", handle: "1.chest.iron", type: "container", vnum: 310, count: 1, no_take: true,
                  closeable: true, closed: true, locked: false, contents: [] },
                { name: "a crumpled traveling cloak", keywords: "cloak traveling crumpled", handle: "1.cloak.traveling.crumpled", type: "armor", vnum: 311, count: 1 },
                { name: "a glowing potion", keywords: "potion glowing", handle: "1.potion.glowing", type: "potion", vnum: 10, count: 2 },
                { name: "a marble fountain", keywords: "fountain marble", handle: "1.fountain.marble", type: "drink", vnum: 312, count: 1, no_take: true }
            ], nodes: [
                { name: "a vein of glittering ore", keywords: "vein ore", profession_id: 2, profession: "Enchanting", required_rank: 16 },
                { name: "a tangle of silverleaf", keywords: "silverleaf tangle", profession_id: 1, profession: "Alchemy", required_rank: 41 },
                { name: "a seam of rough crystal", keywords: "seam crystal", profession_id: 3, profession: "Artificing", required_rank: 5 }
            ] },
            "Char.Equipment": { items: [
                { name: "a magnificent helmet of red dragonscales", keywords: "helmet dragonscales", type: "armor", vnum: 1, location: "Head", condition: 100 },
                { name: "emberforged gauntlets", keywords: "gauntlets emberforged", type: "armor", vnum: 2, location: "Hands", condition: 62 },
                { name: "a talon-barbed whip", keywords: "whip talon", type: "weapon", vnum: 3, location: "Wielding", condition: 35 },
                { name: "a sturdy traveling pack", keywords: "pack traveling", type: "container", vnum: 4, location: "Back", closeable: true, closed: false, contents: [
                    { name: "a flask of lamp oil", keywords: "flask oil", count: 2 },
                    { name: "a coil of silk rope", keywords: "rope silk coil", count: 1 },
                    // Duplicate rows (no count) — the game emits these; the HUD
                    // folds them to "a glyph of teleportation ×2".
                    { name: "a glyph of teleportation", keywords: "glyph teleportation" },
                    { name: "a glyph of teleportation", keywords: "glyph teleportation" }
                ] },
                { name: "a rune-locked coffer", keywords: "coffer runelocked", type: "container", vnum: 5, location: "Held", closeable: true, closed: true, locked: true }
            ] },
            "Char.Inventory": { items: [
                { name: "a glowing potion", keywords: "potion glowing", type: "potion", vnum: 10, count: 3 },
                // Two separate rows for the same scroll — fold to ×2.
                { name: "a scroll of recall", keywords: "scroll recall", type: "scroll", vnum: 12, count: 1 },
                { name: "a scroll of recall", keywords: "scroll recall", type: "scroll", vnum: 12 },
                // Profession context: gear_type joins enchant targeting;
                // disenchant_rank feeds the enchanter's context-menu entry.
                { name: "a quilted woolen hood", keywords: "hood woolen quilted", type: "armor", vnum: 20, count: 1, gear_type: 6, disenchant_rank: 9 },
                { name: "a tarnished silver band", keywords: "band silver tarnished", type: "armor", vnum: 21, count: 1, gear_type: 4, disenchant_rank: 45 },
                { name: "a leather sack", keywords: "sack leather", type: "container", vnum: 11, count: 1, closeable: true, closed: false, contents: [{ name: "a brass key", keywords: "key brass", count: 1 }] }
            ], coins: [{ name: "gold", vnum: 0, count: 18230 }, { name: "silver", vnum: 0, count: 340 }, { name: "obsidian", vnum: 0, count: 12 }], components: [
                { name: "a pinch of sulfur", keywords: "sulfur pinch", vnum: 9001, count: 7 },
                { name: "a vial of powdered silver", keywords: "silver vial powdered", vnum: 9002, count: 3 },
                { name: "a sprig of nightshade", keywords: "nightshade sprig", vnum: 9003, count: 12 },
                { name: "a shard of frost quartz", keywords: "quartz frost shard", vnum: 9004, count: 5 }
            ], treasure: 620 },
            "Char.Affects": { buffs: [{ name: "Stoneskin", id: 101, duration: 1800 }, { name: "Haste", id: 102, duration: 240 }], debuffs: [{ name: "Poison", id: 201, duration: 45 }], maintained: [{ name: "Detect Invisibility", id: 301, duration: 600, target: "self" }, { name: "Shroud", id: 302, duration: 900, target: "Boric", skill: "shroud", handle: "1.boric", releasable: true }] },
            "Group.Update": { leader: "Aelwyn", size: 5, members: [
                { name: "Aelwyn", level: 45, hp_pct: 86, mp_pct: 85, mv_pct: 82, position: "Standing", race: "Elf", "class": "Magician", leader: true, in_room: true, is_tank: false, fighting_name: "a scarred alley thug", threat: 40, tank_threat: 120, threat_level: "low", room: "The Grand Concourse", vnum: 3001, zone: 90 },
                { name: "Boric", level: 43, hp_pct: 30, mp_pct: 40, mv_pct: 75, position: "Standing", race: "Dwarf", "class": "Warrior", leader: false, in_room: true, is_tank: true, fighting_name: "a scarred alley thug", threat: 120, room: "The Grand Concourse", vnum: 3001, zone: 90 },
                { name: "Selra", level: 41, hp_pct: 95, mp_pct: 90, mv_pct: 88, position: "Sleeping", race: "Human", "class": "Cleric", leader: false, in_room: false, is_tank: false, room: "Cramped Alcove", vnum: 3014, zone: 90 },
                { name: "Kael", level: 39, hp_pct: 72, mp_pct: 60, mv_pct: 80, position: "Standing", race: "Human", "class": "Ranger", leader: false, in_room: false, is_tank: false, room: "Village Square", vnum: 5003, zone: 91, area: "Kingdom of Jolnara" },
                { name: "Doran", level: 44, hp_pct: 88, mp_pct: 55, mv_pct: 66, position: "Standing", race: "Dwarf", "class": "Cleric", leader: false, in_room: false, is_tank: false, room: "Ashen Hollow", vnum: 4210, zone: 99, area: "Shrouded Vale" }
            ], allies: [
                { name: "a large timber wolf", owner: "Aelwyn", hp_pct: 55, mp_pct: 100, mv_pct: 95, position: "Resting", in_room: true, is_tank: false }
            ] },
            "Char.Skills": { skills: bigSkills },
            "Char.Cooldowns": { cooldowns: [{ id: 3, remaining: 8 }], usable: { "3": false } },
            "Char.Train": { stats: [{ name: "Str", value: 18, add: 2 }, { name: "Int", value: 25 }, { name: "Wis", value: 20 }], xp: 1250000, xp_pct: 62, can_advance: true, aux: [{ name: "Crit", value: "12.5% (+2%)" }], resources: [{ name: "Practices", value: 5, max: 10 }, { name: "Trains", value: 2, max: 2 }] },
            "Char.Professions": { professions: [
                { id: 1, name: "Alchemy", verb: "craft", rank: 34, max_rank: 99, tier: "Journeyman", recipes_known: 21, recipes_total: 58 },
                { id: 2, name: "Enchanting", verb: "enchant", rank: 12, max_rank: 99, tier: "Novice", recipes_known: 6, recipes_total: 44 }
            ] },
            "Char.Recipes": { recipes: [
                { id: 101, profession_id: 1, name: "minor healing draught", category: "Draughts", min_rank: 30, duration: 20,
                  components: [{ kind: "item", vnum: 9001, name: "a pinch of sulfur", count: 2 }, { kind: "item", vnum: 9003, name: "a sprig of nightshade", count: 1 }] },
                { id: 102, profession_id: 1, name: "tincture of stone", category: "Draughts", min_rank: 39, duration: 30,
                  components: [{ kind: "item", vnum: 9099, name: "a lump of granite dust", count: 1 }, { kind: "treasure", amount: 500 }] },
                { id: 106, profession_id: 1, name: "weak salve", category: "Draughts", min_rank: 10, duration: 15,
                  components: [{ kind: "item", vnum: 9003, name: "a sprig of nightshade", count: 1 }] },
                { id: 103, profession_id: 1, name: "alchemist's fire", category: "Reagents", min_rank: 22, duration: 25,
                  components: [{ kind: "item", vnum: 9001, name: "a pinch of sulfur", count: 4 }, { kind: "location", label: "a forge" }] },
                { id: 104, profession_id: 1, name: "spark reagent", category: "Reagents", min_rank: 30, duration: 18,
                  components: [{ kind: "item", vnum: 9002, name: "a vial of powdered silver", count: 2 }] },
                { id: 105, profession_id: 1, name: "elixir of vigor", category: "Elixirs", min_rank: 45, duration: 40,
                  components: [{ kind: "item", vnum: 9004, name: "a shard of frost quartz", count: 3 }, { kind: "treasure", amount: 300 }] },
                { id: 201, profession_id: 2, name: "minor soothing", category: "Head", min_rank: 8, duration: 20, target_gear_type: 6,
                  components: [{ kind: "item", vnum: 9002, name: "a vial of powdered silver", count: 1 }] },
                { id: 204, profession_id: 2, name: "warding sigil", category: "Body", min_rank: 10, duration: 22, target_gear_type: 2,
                  components: [{ kind: "item", vnum: 9001, name: "a pinch of sulfur", count: 1 }] },
                { id: 205, profession_id: 2, name: "fleetfoot glyph", category: "Feet", min_rank: 14, duration: 22, target_gear_type: 5,
                  components: [{ kind: "item", vnum: 9004, name: "a shard of frost quartz", count: 1 }] },
                { id: 202, profession_id: 2, name: "keened edge", category: "Weapon", min_rank: 16, duration: 30, target_gear_type: 0,
                  components: [{ kind: "item", vnum: 9004, name: "a shard of frost quartz", count: 2 }, { kind: "treasure", amount: 800 }] },
                { id: 206, profession_id: 2, name: "aegis boon", category: "Shield", min_rank: 22, duration: 28, target_gear_type: 1,
                  components: [{ kind: "item", vnum: 9002, name: "a vial of powdered silver", count: 1 }] },
                { id: 203, profession_id: 2, name: "greater arcane dust", category: "Transmutation", min_rank: 20, duration: 10,
                  components: [{ kind: "item", vnum: 9002, name: "a vial of powdered silver", count: 2 }] }
            ] },
            "Char.Craft": { active: true, kind: "craft", name: "minor healing draught", profession_id: 1, remaining: 14, duration: 20, quantity: 2, chain_remaining: 3 },
            "Char.Death": { vnum: 3020, name: "Crumbled Ledge", zone: "Ishar Nexus", time: Math.floor(Date.now() / 1000) - 240 }
        };
        Object.keys(feeds).forEach(function (k) { onGmcp(k, JSON.stringify(feeds[k])); });
        [
            { channel: "gossip", text: "Boric: anyone up for a UDN run?" },
            { channel: "auction", text: "WTS dragonscale helm, pst" },
            { channel: "newbie", text: "Mage: how do I cast spells?" }
        ].forEach(function (c) { onGmcp("Comm.Channel", JSON.stringify(c)); });
        setConnected(true);
    }

    window.IsharHUD = { init: init, onGmcp: onGmcp, reset: reset, setConnected: setConnected, completions: completions, demo: demo, registerMap: registerMap };
})();
