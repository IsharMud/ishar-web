"""Build the sqlite verification database: every game-owned (managed=False)
table, then the Fated fixture from the prompt plus the knot menu and the
Tension achievements straight from the ishar-mud migrations."""
import os, re, sys, datetime as dt
sys.path.insert(0, "/home/user/ishar-web")
sys.path.insert(0, os.path.dirname(__file__))
os.environ["DJANGO_SETTINGS_MODULE"] = "verify_settings"
import django
django.setup()
from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.db import connection
from django.utils import timezone

db = settings.DATABASES["default"]["NAME"]
if os.path.exists(db):
    os.remove(db)
connection.features.supports_foreign_keys = False
connection.features.can_create_inline_fk = False
call_command("migrate", run_syncdb=True, verbosity=0)

connection.features.supports_foreign_keys = False
connection.features.can_create_inline_fk = False
unmanaged = [m for m in apps.get_models(include_auto_created=True) if not m._meta.managed]
with connection.schema_editor() as editor:
    for model in unmanaged:
        if model._meta.db_table in connection.introspection.table_names():
            continue
        for f in model._meta.local_fields:
            if not f.primary_key:
                f.null = True
        editor.create_model(model)
print("created", len(unmanaged), "unmanaged tables")

MUD = "/home/user/ishar-mud"
def run_sql(path, skip=("ALTER TABLE", "CREATE TABLE")):
    import sqlite3
    text = re.sub(r"^\s*--[^\n]*", "", open(path, encoding="utf-8").read(), flags=re.M)
    buf = ""
    for line in text.splitlines(keepends=True):
        buf += line
        if sqlite3.complete_statement(buf):
            stmt = buf.strip().rstrip(";").strip()
            buf = ""
            if not stmt or any(stmt.startswith(s) for s in skip):
                continue
            with connection.cursor() as c:
                c.execute(stmt)

run_sql(f"{MUD}/rust-interop/migrations/20260718000200_tension_modifiers/up.sql")
run_sql(f"{MUD}/rust-interop/migrations/20261004000000_weave_watches_secondary_effect/up.sql")
run_sql(f"{MUD}/rust-interop/migrations/20260718000300_tension_achievements/up.sql")

with connection.cursor() as c:
    c.execute("PRAGMA foreign_keys = OFF")
from apps.accounts.models import Account, AccountAchievement
from apps.achievements.models.achievement import Achievement
from apps.achievements.models.reward import AchievementReward
from apps.classes.models.cls import Class
from apps.fated.models import AccountFatedSkill, TensionModifier
from apps.players.models import Player, PlayerCommon, PlayerStat
from apps.races.models.race import Race
from apps.seasons.models.enigma import SeasonalEnigma
from apps.seasons.models.season import Season
from apps.skills.models import Skill

now = timezone.now()
SeasonalEnigma.objects.create(seasonal_enigma_id=1, enigma_name="The Unbroken Cycle")
SeasonalEnigma.objects.create(seasonal_enigma_id=2, enigma_name="Fractured Threads")
Season.objects.create(season_id=16, is_active=True, effective_date=now - dt.timedelta(days=3),
                      expiration_date=now + dt.timedelta(days=25), enigma_id=2, game_state=0,
                      last_challenge_cycle=now - dt.timedelta(days=1), average_essence_gain=0,
                      average_remorts=0, max_essence_gain=0, max_remorts=0, max_renown=0,
                      avg_renown=0, total_remorts=0, auto_cycle=True)
Class.objects.create(class_id=17, class_name="Fated", class_display="an enigmatic fated",
                     class_description="Shapers of destiny.", is_playable=False)
Class.objects.create(class_id=1, class_name="Rogue", class_display="a stealthy rogue", is_playable=True)
Race.objects.create(race_id=1, symbol="HUMAN", display_name="Human", folk_name="Human", is_playable=True)
Skill.objects.create(id=51, enum_symbol="SPELL_FROSTBITE", skill_name="Frostbite", skill_type=2, rarity=2, passive_tiers=1, parent_skill_id=-1)
Skill.objects.create(id=164, enum_symbol="SKILL_DIVINE_PURPOSE", skill_name="Divine Purpose", skill_type=5, rarity=0, passive_tiers=5, parent_skill_id=-1)
Skill.objects.create(id=7, enum_symbol="SPELL_BLESS", skill_name="Bless", skill_type=2, rarity=1, passive_tiers=1, parent_skill_id=-1)
Skill.objects.create(id=9, enum_symbol="SPELL_INFERNO", skill_name="Inferno", skill_type=2, rarity=4, passive_tiers=1, parent_skill_id=-1)

def account(pk, name, achievement_points=0, is_private=0, immortal_level=0, **kw):
    a = Account(account_id=pk, account_name=name, email=f"{name.lower()}@example.com", created_at=now - dt.timedelta(days=400),
                current_essence=120, earned_essence=900, password="x", immortal_level=immortal_level, is_private=is_private,
                create_isp="", last_isp="", create_ident="", last_ident="", create_haddr=0, last_haddr=0, account_gift=now, bugs_reported=0, achievement_points=achievement_points, **kw)
    a.save()
    return a

tyrell = account(1, "Tyrell", season_woven_essence=28, season_loose_essence=2, season_max_tension=4, max_tension=4, achievement_points=10)
boric = account(2, "Boric", season_woven_essence=16, season_loose_essence=5, season_max_tension=4, max_tension=6, achievement_points=35)
selra = account(3, "Selra", season_woven_essence=41, season_loose_essence=0, season_max_tension=3, max_tension=8, is_private=1)
nobody = account(4, "Nobody", season_woven_essence=0, season_loose_essence=0, season_max_tension=0, max_tension=0)
staff = account(5, "Eternal", immortal_level=3)

AccountFatedSkill.objects.create(account=tyrell, skill_id=51, skill_level=50)      # Frostbite, rare: 0.5
AccountFatedSkill.objects.create(account=tyrell, skill_id=7, skill_level=255)      # Bless, severed: 0
AccountFatedSkill.objects.create(account=boric, skill_id=164, skill_level=3)       # passive common tier 3: 0.6
AccountFatedSkill.objects.create(account=boric, skill_id=9, skill_level=60)        # legendary: 1.5

def player(pk, name, acct, class_id=17, locked=4, mask=65, remorts=3, deleted=0, game_type=1, level=15):
    p = Player(id=pk, account=acct, name=name, title="%s the Fated", remorts=remorts, true_level=level,
               renown=10, favors=0, online=7200, bankacc=100, deaths=0, total_renown=30, quests_completed=1,
               challenges_completed=0, game_type=game_type, birth=now - dt.timedelta(days=2),
               logon=now - dt.timedelta(hours=3), logout=now - dt.timedelta(hours=1), is_deleted=deleted,
               tension_locked=locked, knots_mask=mask, create_ident="", last_isp="", logon_delay=0,
               bound_room=3001, load_room=3001, login_failures=0, create_haddr=0, inn_limit=0, poofin="", poofout="")
    p.save()
    PlayerCommon.objects.create(player=p, player_class_id=class_id, race_id=1, sex=1, level=level, weight=150, height=70,
                                comm_points=0, alignment=0, strength=15, agility=15, endurance=15, perception=15, focus=15,
                                willpower=15, init_strength=15, init_agility=15, init_endurance=15, init_perception=15,
                                init_focus=15, init_willpower=15, perm_hit_pts=100, perm_move_pts=100, perm_spell_pts=100,
                                perm_favor_pts=0, curr_hit_pts=100, curr_move_pts=100, curr_spell_pts=100, curr_favor_pts=0,
                                experience=1000, gold=50, karma=0)
    PlayerStat.objects.create(player=p, total_play_time=7200, total_deaths=0, total_renown=30, total_challenges=0, total_quests=1,
                              hardcore_remorts=remorts, hardcore_level=level, hardcore_deaths=0)
    return p

player(1, "Aelwyn", tyrell)                                          # the prompt's fixture: locked 4, Weave Watches + Exposed
player(2, "Rook", tyrell, class_id=1, locked=-1, mask=0, remorts=2, game_type=0)   # not Fated: no panels
player(3, "Lanya", boric, locked=-1, mask=0, remorts=0)              # the loom is asking for knots
player(4, "Tam", boric, locked=2, mask=4, remorts=10, deleted=1)     # between lives
player(5, "Wren", selra, locked=7, mask=2+32+128+8192, remorts=10)   # at the summit

tight = Achievement.objects.get(name="The First Tightening")
equal = Achievement.objects.get(name="The Loom's Equal")
Achievement.objects.create(name="Welcome to Ishar!", description="Create your first character.", is_hidden=0, category="GENERAL", ordinal=-1, criteria_type="PlayerOnly", created_at=now, updated_at=now)
chal = Achievement.objects.create(name="Challenge Novice", description="Complete your first challenge.", is_hidden=0, category="GENERAL", parent_category="CHALLENGES", ordinal=1, criteria_type="PlayerOnly", created_at=now, updated_at=now)
AchievementReward.objects.create(achievement=chal, reward_type=1, reward_value=100)
AchievementReward.objects.create(achievement=chal, reward_type=0, reward_value=10)
AccountAchievement.objects.create(account=tyrell, achievement=tight, is_completed=1, completion_date=now - dt.timedelta(days=1), completed_by="Aelwyn")
AccountAchievement.objects.create(account=selra, achievement=equal, is_completed=1, completion_date=now - dt.timedelta(days=1), completed_by="Wren")
print("knots:", TensionModifier.objects.count(), "achievements:", Achievement.objects.count())
