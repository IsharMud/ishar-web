"""Signup validation rules mirrored from the game's telnet account creation.

Sources (ishar-mud ``src/server/server.c``): ``illegal_account`` (email),
``illegal_name``/``illegal_new_name`` (account name), ``illegal_password``.
Kept dependency-free so a harness can exercise them without Django settings.

Deliberate deltas from the C, recorded here so the two policies are read
side by side:

* Email format uses Django's ``EmailField`` (stricter than the game's
  ``graph+@graph+.graph+`` regex); the game accepts what the web accepts.
* The pronounceability check (``is_valid_name`` — generated trigraph data)
  and live-world name collisions (``mob_name_in_game``/``find_pers_exact``)
  are game-side only.
"""

VOWELS = frozenset("aeiouy")

# server.c newnames[] / quitnames[] / badnames[] — reserved words at the
# game's login prompt; a name matching one would collide with prompt
# keywords or impersonate staff tiers.
RESERVED_NAMES = frozenset((
    "new", "start", "guest", "anonymous",
    "quit", "exit", "logout", "bye", "done",
    "immortal", "artisan", "paragon", "eternal", "logos", "founder",
    "forger", "god", "adept", "wizard", "imm", "art", "ete", "sysop",
    "admin", "persona", "character", "player", "mortal", "mort", "immort",
    "and", "or", "not", "who", "what", "when", "where", "why", "how",
    "you", "your", "the", "they", "them", "room", "here", "around",
    "invisible", "someone", "ishar", "at", "on", "in", "out", "to",
    "spells",
    "north", "south", "east", "west", "up", "down", "into", "go",
    "door", "doors",
    "me", "my", "real", "realname", "name", "myname", "self",
    "gold", "silver", "ivory", "obsidian", "coin", "coins",
    "shop", "list", "help",
    "root", "sh", "enable", "linuxshell", "bin", "busybox", "botnet",
    "bash", "system",
))

# server.c badnamefragments[] — rejected as a substring anywhere in a name.
BAD_NAME_FRAGMENTS = (
    "alien", "angel", "archer", "assassin", "asshole", "awesome", "bastard",
    "bitch", "black", "blade", "blood", "blue", "break", "captain",
    "cheese", "christ", "cock", "cool", "dark", "dead", "death", "demon",
    "destroy", "devil", "dick", "dragon", "dude", "evil", "fighter", "fire",
    "fuck", "golden", "great", "haha", "hunter", "insane", "ishar",
    "killer", "knight", "lame", "little", "lord", "magic", "master",
    "mighty", "monkey", "monster", "mother", "mystic", "newbie", "night",
    "ninja", "penis", "prince", "raven", "satan", "shadow", "shit",
    "silver", "slayer", "smoke", "sniper", "soldier", "storm", "sucks",
    "super", "sword", "test", "theif", "thief", "vampire", "vampyre",
    "warrior", "white", "wizard",
)

# server.c qwerty/ytrewq — a password may not be a substring of either
# keyboard sweep.
KEYBOARD_ROWS = (
    "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./~!@#$%^&*()_=",
    "=_)(*&^%$#@!~/.,mnbvcxz';lkjhgfdsa\\][poiuytrewq=-0987654321`",
)

EMAIL_MIN, EMAIL_MAX = 3, 29
NAME_MIN, NAME_MAX = 3, 13
PASSWORD_MIN, PASSWORD_MAX = 4, 64


def email_error(email):
    """Length/charset rules on top of Django's format validation."""
    if not EMAIL_MIN <= len(email) <= EMAIL_MAX:
        return (
            f"E-mail addresses must be {EMAIL_MIN} to {EMAIL_MAX} "
            "characters long."
        )
    if any(c <= " " or ord(c) >= 127 for c in email):
        return "E-mail addresses may only contain printable characters."
    return None


def account_name_error(name):
    """The game's character/account-name rules, on the lowercased name."""
    if not name.isascii() or not name.isalpha():
        return (
            "Account names may only use letters — no numbers, symbols, "
            "or spaces."
        )
    name = name.lower()
    if len(name) < NAME_MIN:
        return f"Account names must be at least {NAME_MIN} letters long."
    if len(name) > NAME_MAX:
        return f"Account names may not be more than {NAME_MAX} letters long."

    same_letter = same_type = 0
    prev = ""
    for c in name:
        same_letter = same_letter + 1 if c == prev else 1
        if prev and (c in VOWELS) != (prev in VOWELS):
            same_type = 1
        else:
            same_type += 1
        prev = c
        if same_letter > 2:
            return "Account names can't repeat a letter more than twice in a row."
        if same_type > 4:
            return (
                "Account names can't have more than four vowels or four "
                "consonants in a row."
            )

    letters = set(name)
    if not (letters & VOWELS) or not (letters - VOWELS):
        return "Account names need both vowels and consonants."

    if name in RESERVED_NAMES or name.startswith("all") or (
        name.startswith("the") and len(name) > 7
    ):
        return "You may not use that as a name."
    for fragment in BAD_NAME_FRAGMENTS:
        if fragment in name:
            return "You can't use that word in a name."
    return None


def password_error(password, account_name="", email=""):
    if any(c < " " or ord(c) >= 127 for c in password):
        return "Passwords may not contain control keys."
    if not PASSWORD_MIN <= len(password) <= PASSWORD_MAX:
        return (
            f"Passwords must be {PASSWORD_MIN} to {PASSWORD_MAX} "
            "characters long."
        )
    if len(set(password)) == 1:
        return "Passwords can't consist of only one character repeated."
    for row in KEYBOARD_ROWS:
        if password in row:
            return (
                "You can't press a row of keys on the keyboard as your "
                "password."
            )
    lowered = password.lower()
    local_part = email.split("@", 1)[0].lower() if email else ""
    if lowered and lowered in (account_name.lower(), local_part):
        return "Your password can't be your account name or e-mail address."
    return None
