"""Curated skill → game-icons mapping — the *standardized* icon set every web
HUD player inherits.

Keyed by the **normalized skill name** (lowercased, apostrophes stripped — the
same key hud.js derives from the `Char.Skills` feed). Each icon name exists in
`apps/connect/static/img/game-icons.svg`.

Resolution order in the client (`hud.js` `iconName`):

    per-player pick  →  server-provided icon  →  THIS map  →  keyword heuristic

So this map overrides the client-side keyword heuristic but yields to a player's
personal choice and to a future authoritative `icon` field the game may emit
(see the 2026-07-16 design decisions). A skill not listed here falls through to
the heuristic, so the map may be partial.

Generated from a `python manage.py dump_skills` dump (462 skills) via the
scratchpad tooling (heuristic + hand-tuned overrides), then reviewed. To refresh
after skills change, re-dump and re-run; keep the `# Skill Name` comments.

Note: the eventual home for this is the game itself (an `icon` column on the
`skills` table, emitted on `Char.Skills`) — the HUD already prefers a server
icon, so that would supersede this map for every client at once.
"""

# "normalized name": "icon",  # Original Skill Name
SKILL_ICONS: dict[str, str] = {
    "acid arrow": "acid",  # Acid Arrow
    "acid breath": "acid",  # Acid Breath
    "acid burn": "fire",  # Acid Burn
    "acid oil": "acid",  # Acid Oil
    "ancestral pact": "totem-head",  # Ancestral Pact
    "angelic reprieve": "angel-wings",  # Angelic Reprieve
    "animists call": "beast-eye",  # Animist's Call
    "arcane barrage": "crossed-swords",  # Arcane Barrage
    "arcane echo": "magic-swirl",  # Arcane Echo
    "arcane prodigy": "magic-swirl",  # Arcane Prodigy
    "arcane sensitivity": "magic-swirl",  # Arcane Sensitivity
    "arctic wind": "wind-hole",  # Arctic Wind
    "armor": "armor-vest",  # Armor
    "armored hide": "armor-vest",  # Armored Hide
    "ashen resolve": "burning-embers",  # Ashen Resolve
    "avow": "prayer",  # Avow
    "backstab": "stiletto",  # Backstab
    "bane of clumsiness": "cursed-star",  # Bane of Clumsiness
    "bane of frailty": "cursed-star",  # Bane of Frailty
    "bane of ineptitude": "cursed-star",  # Bane of Ineptitude
    "bash": "shield-reflect",  # Bash
    "bind": "thorny-vine",  # Bind
    "binding heal": "healing",  # Binding Heal
    "bite": "claw-slashes",  # Bite
    "bleed": "bleeding-wound",  # Bleed
    "bless": "prayer",  # Bless
    "blind": "sight-disabled",  # Blind
    "blink": "magic-gate",  # Blink
    "blizzard": "snowflake-1",  # Blizzard
    "blood frenzy": "muscle-up",  # Blood Frenzy
    "blood loss": "bleeding-wound",  # Blood Loss
    "bone shards": "broken-bone",  # Bone Shards
    "calculated assault": "brain",  # Calculated Assault
    "challenged": "sonic-shout",  # Challenged
    "chaotic immolation": "burning-skull",  # Chaotic Immolation
    "chaotic immolation (passive)": "burning-skull",  # Chaotic Immolation (Passive)
    "charm": "psychic-waves",  # Charm
    "cleansing flames": "fire",  # Cleansing Flames
    "cleansing touch": "holy-water",  # Cleansing Touch
    "cleave": "saber-slash",  # Cleave
    "cleaving strike": "saber-slash",  # Cleaving Strike
    "climb": "walking-boot",  # Climb
    "cobra envenomation": "cobra",  # Cobra Envenomation
    "cobra venom": "cobra",  # Cobra Venom
    "concussive strike": "punch",  # Concussive Strike
    "confusion": "psychic-waves",  # Confusion
    "conjur elemental": "portal",  # Conjur Elemental
    "conjur undead": "portal",  # Conjur Undead
    "consecration": "holy-symbol",  # Consecration
    "consecration (unused)": "holy-symbol",  # Consecration (Unused)
    "corpse explosion": "death-skull",  # Corpse Explosion
    "corpse walk": "death-skull",  # Corpse Walk
    "create food": "hammer-nails",  # Create Food
    "cripple": "broken-bone",  # Cripple
    "crippling blow": "broken-bone",  # Crippling Blow
    "critical specialization": "crossed-swords",  # Critical Specialization
    "cure blindness": "healing",  # Cure Blindness
    "cure disease": "poison-cloud",  # Cure Disease
    "cure poison": "poison-bottle",  # Cure Poison
    "curse": "cursed-star",  # Curse
    "cyclone": "tornado",  # Cyclone
    "dark liberation": "evil-wings",  # Dark Liberation
    "darkness": "evil-wings",  # Darkness
    "dazed": "psychic-waves",  # Dazed
    "deafened": "sonic-shout",  # Deafened
    "death blow": "death-skull",  # Death Blow
    "deaths veil": "death-skull",  # Death's Veil
    "deathstrike": "death-skull",  # Deathstrike
    "detect alignment": "all-seeing-eye",  # Detect Alignment
    "detect invisible": "all-seeing-eye",  # Detect Invisible
    "detect life": "caduceus",  # Detect Life
    "detect magic": "all-seeing-eye",  # Detect Magic
    "detect poison": "poison-bottle",  # Detect Poison
    "detect traps": "all-seeing-eye",  # Detect Traps
    "die hard": "heart-plus",  # Die Hard
    "disarm": "sword-clash",  # Disarm
    "disarming strike": "punch",  # Disarming Strike
    "disease": "poison-cloud",  # Disease
    "disenchant": "rune-stone",  # Disenchant
    "disengage": "sprint",  # Disengage
    "dispel magic": "magic-swirl",  # Dispel Magic
    "dispel undead": "holy-symbol",  # Dispel Undead
    "distract": "psychic-waves",  # Distract
    "distracting blow": "punch",  # Distracting Blow
    "divine aegis": "holy-symbol",  # Divine Aegis
    "divine favor": "holy-symbol",  # Divine Favor
    "divine intervention": "holy-symbol",  # Divine Intervention
    "divine oil": "holy-symbol",  # Divine Oil
    "divine purpose": "holy-symbol",  # Divine Purpose
    "divine radiance": "holy-symbol",  # Divine Radiance
    "double strike": "punch",  # Double Strike
    "draconic rage": "dragon-head",  # Draconic Rage
    "draconic roar": "dragon-head",  # Draconic Roar
    "drain": "death-skull",  # Drain
    "dual heritage: elf": "crossed-swords",  # Dual Heritage: Elf
    "dual heritage: orc": "crossed-swords",  # Dual Heritage: Orc
    "earth spike": "earth-crack",  # Earth Spike
    "earth strike": "earth-crack",  # Earth Strike
    "earthbind": "earth-crack",  # Earthbind
    "earthen step": "earth-crack",  # Earthen Step
    "earthquake": "earth-crack",  # Earthquake
    "eldraens ward": "energy-shield",  # Eldraen's Ward
    "elemental bond": "aura",  # Elemental Bond
    "elemental boon": "prayer",  # Elemental Boon
    "elemental fury": "muscle-up",  # Elemental Fury
    "elemental strike": "punch",  # Elemental Strike
    "elemental strike: water": "water-drop",  # Elemental Strike: Water
    "elemental wrath": "muscle-up",  # Elemental Wrath
    "elven repose": "meditation",  # Elven Repose
    "empower": "rune-stone",  # Empower
    "empowered strike": "punch",  # Empowered Strike
    "enchant": "rune-stone",  # Enchant
    "enchanting": "rune-stone",  # Enchanting
    "endure cold": "ice-bolt",  # Endure Cold
    "endure heat": "fire",  # Endure Heat
    "energy ball": "sparkles",  # Energy Ball
    "energy drain": "death-skull",  # Energy Drain
    "energy infusion": "sparkles",  # Energy Infusion
    "energy lance": "spear-hook",  # Energy Lance
    "energy surge": "sparkles",  # Energy Surge
    "enhance ability": "biceps",  # Enhance Ability
    "enrage": "muscle-up",  # Enrage
    "entropic absoprtion (passive)": "death-zone",  # Entropic Absoprtion (Passive)
    "entropic reclamation": "death-zone",  # Entropic Reclamation
    "ethereal pact": "spectre",  # Ethereal Pact
    "evade": "vibrating-shield",  # Evade
    "evasive maneuvers": "sprint",  # Evasive Maneuvers
    "evil radiance": "sunbeams",  # Evil Radiance
    "exhaust": "hourglass",  # Exhaust
    "expertise": "crossed-swords",  # Expertise
    "exploit weakness": "stiletto",  # Exploit Weakness
    "eyes of the master": "third-eye",  # Eyes of the Master
    "fade": "invisible",  # Fade
    "fatal instinct": "stiletto",  # Fatal Instinct
    "favorable winds": "wind-hole",  # Favorable Winds
    "fear": "spectre",  # Fear
    "fear ward": "spectre",  # Fear Ward
    "feather fall": "angel-wings",  # Feather Fall
    "feint": "sword-clash",  # Feint
    "feint strike": "punch",  # Feint Strike
    "fiery body": "fire",  # Fiery Body
    "fire breath": "fire",  # Fire Breath
    "fire guard": "fire",  # Fire Guard
    "fire strike": "fire",  # Fire Strike
    "fireball": "fireball",  # Fireball
    "fireshield": "fire",  # Fireshield
    "flame enchant": "fire",  # Flame Enchant
    "flamestrike": "fireball",  # Flamestrike
    "flaming": "fire",  # Flaming
    "flaming claw": "fire",  # Flaming Claw
    "flaming hands": "fire",  # Flaming Hands
    "flurry of blows": "crossed-swords",  # Flurry of Blows
    "fly": "angel-wings",  # Fly
    "flying kick": "high-kick",  # Flying Kick
    "foresight": "third-eye",  # Foresight
    "fortified fist": "punch",  # Fortified Fist
    "frenzy": "muscle-up",  # Frenzy
    "frost breath": "ice-bolt",  # Frost Breath
    "frost enchant": "ice-bolt",  # Frost Enchant
    "frostbite": "ice-bolt",  # Frostbite
    "frostspark": "ice-bolt",  # Frostspark
    "fumble": "sword-clash",  # Fumble
    "furious blows": "punch-blast",  # Furious Blows
    "fury of kaelzor": "muscle-up",  # Fury of Kaelzor
    "gate": "magic-gate",  # Gate
    "glacial bite": "ice-bolt",  # Glacial Bite
    "glacial encasement": "ice-bolt",  # Glacial Encasement
    "glyph of striking": "rune-stone",  # Glyph of Striking
    "goading strike": "punch",  # Goading Strike
    "good radiance": "sunbeams",  # Good Radiance
    "graceful step": "footsteps",  # Graceful Step
    "grappled": "claw-slashes",  # Grappled
    "grave bond": "death-skull",  # Grave Bond
    "greater accuracy": "eye-target",  # Greater Accuracy
    "greater arcane font": "magic-swirl",  # Greater Arcane Font
    "greater arcane infusion": "magic-swirl",  # Greater Arcane Infusion
    "greater defense": "shield",  # Greater Defense
    "greater spirit edge": "rune-stone",  # Greater Spirit Edge
    "greater vital infusion": "heart-plus",  # Greater Vital Infusion
    "grim herald": "spectre",  # Grim Herald
    "guardian": "templar-shield",  # Guardian
    "gust of wind": "wind-hole",  # Gust Of Wind
    "hamstring": "bleeding-wound",  # Hamstring
    "harm": "death-skull",  # Harm
    "haste": "sprint",  # Haste
    "haunt": "spectre",  # Haunt
    "heal": "healing",  # Heal
    "heal critical": "healing",  # Heal Critical
    "heal minor": "healing",  # Heal Minor
    "heal serious": "healing",  # Heal Serious
    "heavens wrath": "muscle-up",  # Heaven's Wrath
    "hemlock poison": "poison-bottle",  # Hemlock Poison
    "heroism": "muscle-up",  # Heroism
    "hide": "armor-vest",  # Hide
    "holy smite": "holy-symbol",  # Holy Smite
    "hone": "anvil",  # Hone
    "howling wolf": "wolf-howl",  # Howling Wolf
    "hunt": "footsteps",  # Hunt
    "ice strike": "ice-bolt",  # Ice Strike
    "identify": "all-seeing-eye",  # Identify
    "imbue": "rune-stone",  # Imbue
    "increased experience": "gems",  # Increased Experience
    "infernal scourge": "burning-skull",  # Infernal Scourge
    "inferno": "fire",  # Inferno
    "inferno splash": "fire",  # Inferno Splash
    "infravision": "eye-target",  # Infravision
    "innate cleansing flames": "fire",  # Innate Cleansing Flames
    "innate cyclone": "tornado",  # Innate Cyclone
    "innate earthquake": "earth-crack",  # Innate Earthquake
    "innate earthspike": "earth-crack",  # Innate Earthspike
    "innate fireball": "fireball",  # Innate Fireball
    "innate frostbite": "ice-bolt",  # Innate Frostbite
    "innate inferno": "fire",  # Innate Inferno
    "innate lightning bolt": "lightning-arc",  # Innate Lightning Bolt
    "innate potential": "aura",  # Innate Potential
    "innate water sphere": "water-drop",  # Innate Water Sphere
    "inner fire": "fire",  # Inner Fire
    "inner light": "sunbeams",  # Inner Light
    "invigorate": "regeneration",  # Invigorate
    "invisible": "invisible",  # Invisible
    "item aura": "aura",  # Item Aura
    "jinx": "cursed-star",  # Jinx
    "judgement": "holy-symbol",  # Judgement
    "ki disruption": "psychic-waves",  # Ki Disruption
    "kick": "high-kick",  # Kick
    "knock": "padlock-open",  # Knock
    "legend lore": "spell-book",  # Legend Lore
    "lesser accuracy": "eye-target",  # Lesser Accuracy
    "lesser arcane font": "magic-swirl",  # Lesser Arcane Font
    "lesser arcane infusion": "magic-swirl",  # Lesser Arcane Infusion
    "lesser defense": "shield",  # Lesser Defense
    "lesser gate": "magic-gate",  # Lesser Gate
    "lesser spirit edge": "rune-stone",  # Lesser Spirit Edge
    "lesser vital infusion": "heart-plus",  # Lesser Vital Infusion
    "life transfer": "caduceus",  # Life Transfer
    "light": "sun",  # Light
    "lightning bolt": "lightning-arc",  # Lightning Bolt
    "lightning breath": "lightning-arc",  # Lightning Breath
    "lightning chain": "lightning-arc",  # Lightning Chain
    "lightning strike": "lightning-arc",  # Lightning Strike
    "listen": "third-eye",  # Listen
    "locate corpse": "death-skull",  # Locate Corpse
    "lysandras faith": "prayer",  # Lysandra's Faith
    "magic arrow": "pocket-bow",  # Magic Arrow
    "major enchant": "rune-stone",  # Major Enchant
    "measured frenzy": "muscle-up",  # Measured Frenzy
    "meditate": "meditation",  # Meditate
    "metamagic: clarity": "magic-swirl",  # Metamagic: Clarity
    "metamagic: expand": "magic-swirl",  # Metamagic: Expand
    "metamagic: held spell": "magic-swirl",  # Metamagic: Held Spell
    "metamagic: quicken": "sprint",  # Metamagic: Quicken
    "metamagic: ruinous": "magic-swirl",  # Metamagic: Ruinous
    "meteor swarm": "fireball",  # Meteor Swarm
    "miasma": "poison-cloud",  # Miasma
    "minor enchant": "rune-stone",  # Minor Enchant
    "mirror image": "psychic-waves",  # Mirror Image
    "mist": "wind-hole",  # Mist
    "misty veil": "wind-hole",  # Misty Veil
    "moderate accuracy": "eye-target",  # Moderate Accuracy
    "moderate defense": "shield",  # Moderate Defense
    "moderate enchant": "rune-stone",  # Moderate Enchant
    "moderate spirit edge": "rune-stone",  # Moderate Spirit Edge
    "momentum": "sprint",  # Momentum
    "monk hardened": "armor-vest",  # Monk Hardened
    "mystic eagle": "eagle-head",  # Mystic Eagle
    "nausea": "poison-cloud",  # Nausea
    "necrotic oil": "death-skull",  # Necrotic Oil
    "negative one": "round-star",  # Negative One
    "nerve strike": "punch",  # Nerve Strike
    "neural spike": "brain",  # Neural Spike
    "neutral consecretion": "holy-symbol",  # Neutral Consecretion
    "nightspore poison": "poison-bottle",  # Nightspore Poison
    "nightspore poisoning": "poison-bottle",  # Nightspore Poisoning
    "nightvision": "evil-wings",  # Nightvision
    "overpowering strike": "punch",  # Overpowering Strike
    "pacified": "psychic-waves",  # Pacified
    "paralysis": "cursed-star",  # paralysis
    "parry": "pointy-sword",  # Parry
    "passive: earth strike": "earth-crack",  # Passive: Earth Strike
    "passive: fire strike": "fire",  # Passive: Fire Strike
    "passive: flight": "feathered-wing",  # Passive: Flight
    "passive: ice strike": "ice-bolt",  # Passive: Ice Strike
    "passive: viciousness": "claw-slashes",  # Passive: Viciousness
    "passive: water strike": "water-drop",  # Passive: Water Strike
    "passive: wind strike": "wind-hole",  # Passive: Wind Strike
    "patient defense": "shield",  # Patient Defense
    "perfect self": "aura",  # Perfect Self
    "phase": "invisible",  # Phase
    "phoenix mend": "burning-embers",  # Phoenix Mend
    "pick locks": "padlock-open",  # Pick Locks
    "placeholder": "round-star",  # Placeholder
    "poison": "poison-bottle",  # Poison
    "poison breath": "poison-bottle",  # Poison Breath
    "portal: jrel": "magic-gate",  # Portal: Jrel
    "portal: mareldja": "magic-gate",  # Portal: Mareldja
    "possession": "psychic-waves",  # Possession
    "pouncing blow": "claw-slashes",  # Pouncing Blow
    "prayer": "prayer",  # Prayer
    "predators grasp": "claw-slashes",  # Predator's Grasp
    "preservation": "crystal-shine",  # Preservation
    "pressure point": "punch",  # Pressure Point
    "profane": "cursed-star",  # Profane
    "protection": "shield",  # Protection
    "protection from undead": "shield",  # Protection From Undead
    "psychic hemorrhage": "brain",  # Psychic Hemorrhage
    "purify": "holy-water",  # Purify
    "purity of body": "regeneration",  # Purity of Body
    "rainsoak haste": "sprint",  # Rainsoak Haste
    "raise dead": "caduceus",  # Raise Dead
    "rake": "claw-slashes",  # Rake
    "rallied": "muscle-up",  # Rallied
    "rally": "muscle-up",  # Rally
    "rallying cry": "sonic-shout",  # Rallying Cry
    "razor feathers": "angel-wings",  # Razor Feathers
    "reactive strikes": "shield-reflect",  # Reactive Strikes
    "reanimate": "death-skull",  # Reanimate
    "reave": "saber-slash",  # Reave
    "rebirth strike": "burning-embers",  # Rebirth Strike
    "recall": "magic-gate",  # Recall
    "reeling": "psychic-waves",  # Reeling
    "relentlessness": "muscle-up",  # Relentlessness
    "remembrance of catacombs": "death-skull",  # Remembrance of Catacombs
    "remembrance of eikatos": "rune-stone",  # Remembrance of Eikatos
    "remembrance of evermore": "rune-stone",  # Remembrance of Evermore
    "remembrance of frostreapers chill": "ice-bolt",  # Remembrance of Frostreaper's Chill
    "remembrance of the depths": "octopus",  # Remembrance of the Depths
    "remembrance of the forsaken shadows": "evil-wings",  # Remembrance of the Forsaken Shadows
    "remembrance of the glaciers": "ice-bolt",  # Remembrance of the Glaciers
    "remembrance of the judgement of duality": "crossed-swords",  # Remembrance of the Judgement of Duality
    "remembrance of the kraken": "octopus",  # Remembrance of the Kraken
    "remembrance of the plane caller": "magic-portal",  # Remembrance of the Plane Caller
    "remembrance of the pyrul brothers": "fire",  # Remembrance of the Pyrul Brothers
    "remembrance of the resilient boar": "boar",  # Remembrance of the Resilient Boar
    "remembrance of the riptide": "water-drop",  # Remembrance of the Riptide
    "remembrance of the silent shadow": "evil-wings",  # Remembrance of the Silent Shadow
    "remembrance of the stormshield": "lightning-storm",  # Remembrance of the Stormshield
    "remembrance of the valorous": "templar-shield",  # Remembrance of the Valorous
    "remembrance of the whispering tome": "spell-book",  # Remembrance of the Whispering Tome
    "remembrance of the zephyr": "wind-hole",  # Remembrance of the Zephyr
    "remembrance of unfettered magic": "magic-swirl",  # Remembrance of Unfettered Magic
    "remembrance of white forest": "sprout",  # Remembrance of White Forest
    "remove curse": "cursed-star",  # Remove Curse
    "remove hunger": "cauldron",  # Remove Hunger
    "remove paralysis": "caduceus",  # Remove Paralysis
    "remove thirst": "water-drop",  # Remove Thirst
    "remove traps": "gears",  # Remove Traps
    "rescue": "shield",  # Rescue
    "resilient soul": "death-skull",  # Resilient Soul
    "resolve": "templar-shield",  # Resolve
    "resurrection": "caduceus",  # Resurrection
    "retribution": "holy-symbol",  # Retribution
    "rift banish": "magic-portal",  # Rift Banish
    "rigor": "broken-bone",  # Rigor
    "riposte": "pointy-sword",  # Riposte
    "sacrifice": "ice-bolt",  # Sacrifice
    "sanctified bolt": "holy-symbol",  # Sanctified Bolt
    "sanctuary": "energy-shield",  # Sanctuary
    "sanctuary rend": "energy-shield",  # Sanctuary Rend
    "savage strike": "punch",  # Savage Strike
    "screech": "sonic-shout",  # Screech
    "scry": "third-eye",  # Scry
    "second sight": "third-eye",  # Second Sight
    "second wind": "regeneration",  # Second Wind
    "sentinel": "eye-target",  # Sentinel
    "shatter focus": "shield-reflect",  # Shatter Focus
    "shield": "shield",  # Shield
    "shield block": "shield",  # Shield Block
    "shield slam": "shield",  # Shield Slam
    "shroud": "invisible",  # Shroud
    "silence": "psychic-waves",  # Silence
    "skeletal grasp": "broken-bone",  # Skeletal Grasp
    "slash": "saber-slash",  # Slash
    "sleep": "psychic-waves",  # Sleep
    "sneak": "hidden",  # Sneak
    "soar": "angel-wings",  # Soar
    "soothing rains": "water-drop",  # Soothing Rains
    "soul drain": "death-skull",  # Soul Drain
    "soul rend": "death-skull",  # Soul Rend
    "spatial distortion": "magic-portal",  # Spatial Distortion
    "spectral armaments": "spectre",  # Spectral Armaments
    "spectral blade": "pointy-sword",  # Spectral Blade
    "spectral shield": "shield",  # Spectral Shield
    "spirit aegis": "energy-shield",  # Spirit Aegis
    "spirit sight": "third-eye",  # Spirit Sight
    "spirit ward": "energy-shield",  # Spirit Ward
    "spiritual renewal": "healing",  # Spiritual Renewal
    "steal": "plain-dagger",  # Steal
    "stillness of mind": "psychic-waves",  # Stillness of Mind
    "stone rigid": "earth-crack",  # Stone Rigid
    "stoneskin": "earth-crack",  # Stoneskin
    "strike": "punch",  # Strike
    "stunning blow": "punch-blast",  # Stunning Blow
    "summon": "portal",  # Summon
    "summon corpse": "death-skull",  # Summon Corpse
    "summon elemental": "portal",  # Summon Elemental
    "summon familiar": "portal",  # Summon Familiar
    "summoning rift": "portal",  # Summoning Rift
    "sunburst": "sunbeams",  # Sunburst
    "sundered armor": "shield-reflect",  # Sundered Armor
    "synapse shock": "brain",  # Synapse Shock
    "takedown": "boot-stomp",  # Takedown
    "talon strike": "claw-slashes",  # Talon Strike
    "target": "eye-target",  # Target
    "taunt": "sonic-shout",  # Taunt
    "teleport": "magic-gate",  # Teleport
    "teleport: jrel": "magic-gate",  # Teleport: Jrel
    "teleport: mareldja": "magic-gate",  # Teleport: Mareldja
    "tempest": "lightning-storm",  # Tempest
    "temporal distortion": "hourglass",  # Temporal Distortion
    "temporal recall": "magic-gate",  # Temporal Recall
    "thickened shell": "tortoise",  # Thickened Shell
    "throat strike": "punch",  # Throat Strike
    "thunder clap": "lightning-arc",  # Thunder Clap
    "timeless body": "hourglass",  # Timeless Body
    "torrent": "water-drop",  # Torrent
    "totem carving": "totem-head",  # Totem Carving
    "totem of draconic rage": "dragon-head",  # Totem of Draconic Rage
    "totem of the howling wolf": "wolf-howl",  # Totem of the Howling Wolf
    "totem of the mystic eagle": "eagle-head",  # Totem of the Mystic Eagle
    "totem of the rymaran phoenix": "burning-embers",  # Totem of the Rymaran Phoenix
    "totem: rymaran phoenix": "burning-embers",  # Totem: Rymaran Phoenix
    "totemic call": "totem-head",  # Totemic Call
    "totems": "totem-head",  # Totems
    "tracked": "footsteps",  # Tracked
    "training: armor": "armor-vest",  # Training: Armor
    "training: attack": "crossed-swords",  # Training: Attack
    "training: healing power": "healing",  # Training: Healing Power
    "training: melee damage": "sword-brandish",  # Training: Melee Damage
    "training: speed": "sprint",  # Training: Speed
    "training: spell damage": "magic-swirl",  # Training: Spell Damage
    "trance": "meditation",  # Trance
    "translocate": "magic-gate",  # Translocate
    "trip": "sword-clash",  # Trip
    "type hammerfist": "flat-hammer",  # Type Hammerfist
    "unraveling blow": "sword-clash",  # Unraveling Blow
    "valor": "holy-symbol",  # Valor
    "veyras blessing": "holy-symbol",  # Veyra's Blessing
    "veyras favor": "holy-symbol",  # Veyra's Favor
    "vivisect": "bone-knife",  # Vivisect
    "void pulse": "magic-portal",  # Void Pulse
    "void traversal": "portal",  # Void Traversal
    "wall run": "sprint",  # Wall Run
    "wanderlust": "walking-boot",  # Wanderlust
    "water sphere": "water-drop",  # Water Sphere
    "waterbreath": "water-drop",  # Waterbreath
    "waterwalk": "water-drop",  # Waterwalk
    "way of the crane": "raven",  # Way of the Crane
    "way of the dragon": "dragon-head",  # Way of the Dragon
    "way of the monkey": "monkey",  # Way of the Monkey
    "way of the phoenix": "burning-embers",  # Way of the Phoenix
    "way of the tiger": "tiger-head",  # Way of the Tiger
    "way of the tortoise": "tortoise",  # Way of the Tortoise
    "weakened": "cursed-star",  # Weakened
    "wellspring": "water-drop",  # Wellspring
    "wildfire": "fire",  # Wildfire
    "wind buffet": "wind-hole",  # Wind Buffet
    "wind strike": "wind-hole",  # Wind Strike
    "winds of comfort": "wind-hole",  # Winds of Comfort
    "windstep": "feathered-wing",  # Windstep
    "withering cold": "ice-bolt",  # Withering Cold
    "wizardlock": "magic-swirl",  # WizardLock
    "word of grace": "prayer",  # Word of Grace
}
