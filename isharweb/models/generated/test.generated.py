# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountUpgrades(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    cost = models.PositiveIntegerField()
    description = models.CharField(max_length=400)
    name = models.CharField(unique=True, max_length=80)
    max_value = models.PositiveIntegerField()
    scale = models.IntegerField()
    is_disabled = models.IntegerField()
    increment = models.IntegerField()
    amount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'account_upgrades'


class AccountsAccountUpgrades(models.Model):
    account_upgrades = models.OneToOneField(AccountUpgrades, models.DO_NOTHING, primary_key=True)  # The composite primary key (account_upgrades_id, account_id) found, that is not supported. The first column is selected.
    account = models.ForeignKey(Accounts, models.DO_NOTHING)
    amount = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'accounts_account_upgrades'
        unique_together = (('account_upgrades', 'account'),)


class AccountsConfigurationOptions(models.Model):
    account = models.OneToOneField(Accounts, models.DO_NOTHING, primary_key=True)  # The composite primary key (account_id, configuration_option_id) found, that is not supported. The first column is selected.
    configuration_option = models.ForeignKey('ConfigurationOptions', models.DO_NOTHING)
    value = models.CharField(max_length=76)

    class Meta:
        managed = False
        db_table = 'accounts_configuration_options'
        unique_together = (('account', 'configuration_option'),)


class AffectFlags(models.Model):
    flag_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'affect_flags'


class Boards(models.Model):
    board_id = models.PositiveIntegerField(primary_key=True)
    board_name = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'boards'


class Challenges(models.Model):
    challenge_id = models.SmallAutoField(primary_key=True)
    mob_vnum = models.IntegerField()
    orig_level = models.IntegerField()
    orig_people = models.IntegerField()
    orig_tier = models.IntegerField()
    adj_level = models.IntegerField()
    adj_people = models.IntegerField()
    adj_tier = models.IntegerField()
    challenge_desc = models.CharField(max_length=80)
    winner_desc = models.CharField(max_length=80)
    mob_name = models.CharField(max_length=30)
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'challenges'





class Conditions(models.Model):
    condition_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'conditions'


class ConfigurationOptions(models.Model):
    configuration_option_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=20)
    is_display = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'configuration_options'


class Forces(models.Model):
    force_name = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'forces'


class GlobalEvent(models.Model):
    event_type = models.IntegerField(primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_name = models.CharField(max_length=20)
    event_desc = models.CharField(max_length=40)
    xp_bonus = models.IntegerField()
    shop_bonus = models.IntegerField()
    celestial_luck = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'global_event'


class KillMemory(models.Model):
    player = models.ForeignKey('Players', models.DO_NOTHING, blank=True, null=True)
    kill_memory_set = models.IntegerField(blank=True, null=True)
    scratch = models.SmallIntegerField(blank=True, null=True)
    nonzero = models.SmallIntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kill_memory'


class KillMemoryBuckets(models.Model):
    kill_memory = models.ForeignKey(KillMemory, models.DO_NOTHING, blank=True, null=True)
    bucket_index = models.SmallIntegerField(blank=True, null=True)
    value = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kill_memory_buckets'
        unique_together = (('kill_memory', 'bucket_index'),)


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Accounts, models.DO_NOTHING)
    created_at = models.DateTimeField()
    subject = models.CharField(max_length=64)
    body = models.TextField()

    class Meta:
        managed = False
        db_table = 'news'


class Objects(models.Model):
    vnum = models.IntegerField()
    seed = models.SmallIntegerField()
    timer = models.SmallIntegerField()
    otype = models.IntegerField()
    equipped = models.IntegerField()
    size = models.SmallIntegerField()
    weight = models.IntegerField()
    value = models.IntegerField()
    val0 = models.IntegerField()
    val1 = models.IntegerField()
    val2 = models.IntegerField()
    val3 = models.IntegerField()
    state = models.IntegerField()
    min_level = models.IntegerField()
    loaded_on = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'objects'


class PlayerAccounts(models.Model):
    account = models.ForeignKey(Accounts, models.DO_NOTHING)
    player = models.ForeignKey('Players', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'player_accounts'


class PlayerAffectFlags(models.Model):
    affect_flag = models.OneToOneField(AffectFlags, models.DO_NOTHING, primary_key=True)  # The composite primary key (affect_flag_id, player_id) found, that is not supported. The first column is selected.
    expires = models.IntegerField()
    flag_value = models.IntegerField()
    bits = models.IntegerField()
    location_1 = models.IntegerField()
    mod_1 = models.IntegerField()
    location_2 = models.IntegerField()
    mod_2 = models.IntegerField()
    player = models.ForeignKey('Players', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'player_affect_flags'
        unique_together = (('affect_flag', 'player'),)


class PlayerBoards(models.Model):
    player = models.OneToOneField('Players', models.DO_NOTHING, primary_key=True)  # The composite primary key (player_id, board_id) found, that is not supported. The first column is selected.
    board = models.ForeignKey(Boards, models.DO_NOTHING)
    last_read = models.IntegerField()
    last_read_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'player_boards'
        unique_together = (('player', 'board'),)


class PlayerCommon(models.Model):
    player = models.OneToOneField('Players', models.DO_NOTHING)
    class_field = models.ForeignKey(Classes, models.DO_NOTHING, db_column='class_id')  # Field renamed because it was a Python reserved word.
    race_id = models.PositiveIntegerField()
    sex = models.IntegerField()
    level = models.PositiveIntegerField()
    weight = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    comm_points = models.SmallIntegerField()
    alignment = models.SmallIntegerField()
    strength = models.PositiveIntegerField()
    agility = models.PositiveIntegerField()
    endurance = models.PositiveIntegerField()
    perception = models.PositiveIntegerField()
    focus = models.PositiveIntegerField()
    willpower = models.PositiveIntegerField()
    init_strength = models.PositiveIntegerField()
    init_agility = models.PositiveIntegerField()
    init_endurance = models.PositiveIntegerField()
    init_perception = models.PositiveIntegerField()
    init_focus = models.PositiveIntegerField()
    init_willpower = models.PositiveIntegerField()
    perm_hit_pts = models.SmallIntegerField()
    perm_move_pts = models.SmallIntegerField()
    perm_spell_pts = models.SmallIntegerField()
    perm_favor_pts = models.SmallIntegerField()
    curr_hit_pts = models.SmallIntegerField()
    curr_move_pts = models.SmallIntegerField()
    curr_spell_pts = models.SmallIntegerField()
    curr_favor_pts = models.SmallIntegerField()
    experience = models.IntegerField()
    gold = models.IntegerField()
    karma = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'player_common'


class PlayerConditions(models.Model):
    player = models.OneToOneField('Players', models.DO_NOTHING, primary_key=True)  # The composite primary key (player_id, condition_id) found, that is not supported. The first column is selected.
    condition = models.ForeignKey(Conditions, models.DO_NOTHING)
    value = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'player_conditions'
        unique_together = (('player', 'condition'),)


class PlayerConfigurationOptions(models.Model):
    player = models.OneToOneField('Players', models.DO_NOTHING, primary_key=True)  # The composite primary key (player_id, configuration_option_id) found, that is not supported. The first column is selected.
    configuration_option = models.ForeignKey(ConfigurationOptions, models.DO_NOTHING)
    value = models.CharField(max_length=76)

    class Meta:
        managed = False
        db_table = 'player_configuration_options'
        unique_together = (('player', 'configuration_option'),)


class PlayerFlags(models.Model):
    flag_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'player_flags'


class PlayerPlayerFlags(models.Model):
    flag = models.OneToOneField(PlayerFlags, models.DO_NOTHING, primary_key=True)  # The composite primary key (flag_id, player_id) found, that is not supported. The first column is selected.
    player = models.ForeignKey('Players', models.DO_NOTHING)
    value = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'player_player_flags'
        unique_together = (('flag', 'player'),)


class PlayerQuestSteps(models.Model):
    player = models.OneToOneField('Players', models.DO_NOTHING, primary_key=True)  # The composite primary key (player_id, step_id) found, that is not supported. The first column is selected.
    step = models.ForeignKey('QuestSteps', models.DO_NOTHING)
    num_collected = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'player_quest_steps'
        unique_together = (('player', 'step'),)


class PlayerQuests(models.Model):
    quest = models.OneToOneField('Quests', models.DO_NOTHING, primary_key=True)  # The composite primary key (quest_id, player_id) found, that is not supported. The first column is selected.
    player = models.ForeignKey('Players', models.DO_NOTHING)
    status = models.IntegerField()
    last_completed_at = models.DateTimeField()
    num_completed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'player_quests'
        unique_together = (('quest', 'player'), ('quest', 'player'),)


class PlayerRelics(models.Model):
    player = models.ForeignKey('Players', models.DO_NOTHING)
    obj_vnum = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'player_relics'
        unique_together = (('player', 'obj_vnum'),)


class PlayerRemortUpgrades(models.Model):
    upgrade = models.OneToOneField('RemortUpgrades', models.DO_NOTHING, primary_key=True)  # The composite primary key (upgrade_id, player_id) found, that is not supported. The first column is selected.
    player = models.ForeignKey('Players', models.DO_NOTHING)
    value = models.PositiveIntegerField()
    essence_perk = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'player_remort_upgrades'
        unique_together = (('upgrade', 'player'),)


class PlayerSkills(models.Model):
    skill_id = models.PositiveIntegerField(primary_key=True)  # The composite primary key (skill_id, player_id) found, that is not supported. The first column is selected.
    player_id = models.PositiveIntegerField()
    skill_level = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'player_skills'
        unique_together = (('skill_id', 'player_id'),)


class Players(models.Model):
    account = models.ForeignKey(Accounts, models.DO_NOTHING)
    name = models.CharField(unique=True, max_length=15)
    create_ident = models.CharField(max_length=10)
    last_isp = models.CharField(max_length=30)
    description = models.CharField(max_length=240, blank=True, null=True)
    title = models.CharField(max_length=45)
    poofin = models.CharField(max_length=80)
    poofout = models.CharField(max_length=80)
    bankacc = models.PositiveIntegerField()
    logon_delay = models.PositiveSmallIntegerField()
    true_level = models.PositiveIntegerField()
    renown = models.PositiveIntegerField()
    remorts = models.PositiveIntegerField()
    favors = models.PositiveIntegerField()
    online = models.IntegerField(blank=True, null=True)
    bound_room = models.PositiveIntegerField()
    load_room = models.PositiveIntegerField()
    invstart_level = models.IntegerField(blank=True, null=True)
    login_failures = models.PositiveSmallIntegerField()
    create_haddr = models.IntegerField()
    login_fail_haddr = models.IntegerField(blank=True, null=True)
    last_haddr = models.IntegerField(blank=True, null=True)
    last_ident = models.CharField(max_length=10, blank=True, null=True)
    load_room_next = models.PositiveIntegerField(blank=True, null=True)
    load_room_next_expires = models.PositiveIntegerField(blank=True, null=True)
    aggro_until = models.PositiveIntegerField(blank=True, null=True)
    inn_limit = models.PositiveSmallIntegerField()
    held_xp = models.IntegerField(blank=True, null=True)
    last_isp_change = models.PositiveIntegerField(blank=True, null=True)
    is_deleted = models.PositiveIntegerField()
    deaths = models.PositiveSmallIntegerField()
    total_renown = models.PositiveSmallIntegerField()
    quests_completed = models.PositiveSmallIntegerField()
    challenges_completed = models.PositiveSmallIntegerField()
    game_type = models.IntegerField()
    birth = models.DateTimeField()
    logon = models.DateTimeField()
    logout = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'players'


class QuestPrereqs(models.Model):
    quest = models.ForeignKey('Quests', models.DO_NOTHING)
    required_quest = models.ForeignKey('Quests', models.DO_NOTHING, db_column='required_quest', related_name='questprereqs_required_quest_set')

    class Meta:
        managed = False
        db_table = 'quest_prereqs'


class QuestRewards(models.Model):
    reward_num = models.IntegerField(primary_key=True)  # The composite primary key (reward_num, quest_id) found, that is not supported. The first column is selected.
    reward_type = models.IntegerField()
    quest = models.ForeignKey('Quests', models.DO_NOTHING)
    class_restrict = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'quest_rewards'
        unique_together = (('reward_num', 'quest'),)


class QuestSteps(models.Model):
    step_id = models.AutoField(primary_key=True)
    step_type = models.IntegerField()
    target = models.IntegerField()
    num_required = models.IntegerField()
    quest = models.ForeignKey('Quests', models.DO_NOTHING)
    time_limit = models.IntegerField()
    mystify = models.IntegerField()
    mystify_text = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'quest_steps'


class Quests(models.Model):
    quest_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=25)
    display_name = models.CharField(max_length=30)
    completion_message = models.CharField(max_length=700)
    min_level = models.IntegerField()
    max_level = models.IntegerField()
    repeatable = models.IntegerField()
    description = models.CharField(max_length=512)
    prerequisite = models.IntegerField()
    class_restrict = models.IntegerField()
    quest_intro = models.CharField(max_length=2000)
    quest_source = models.PositiveIntegerField(blank=True, null=True)
    quest_return = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quests'


class Races(models.Model):
    race_id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=100, blank=True, null=True)
    display_name = models.CharField(max_length=25, blank=True, null=True)
    folk_name = models.CharField(max_length=25, blank=True, null=True)
    default_movement = models.CharField(max_length=10, blank=True, null=True)
    description = models.CharField(max_length=80, blank=True, null=True)
    default_height = models.SmallIntegerField(blank=True, null=True)
    default_weight = models.SmallIntegerField(blank=True, null=True)
    bonus_fortitude = models.SmallIntegerField(blank=True, null=True)
    bonus_reflex = models.SmallIntegerField(blank=True, null=True)
    bonus_resilience = models.SmallIntegerField(blank=True, null=True)
    listen_sound = models.CharField(max_length=80, blank=True, null=True)
    height_bonus = models.SmallIntegerField(blank=True, null=True)
    weight_bonus = models.SmallIntegerField(blank=True, null=True)
    short_description = models.CharField(max_length=80, blank=True, null=True)
    long_description = models.CharField(max_length=512, blank=True, null=True)
    attack_noun = models.CharField(max_length=25, blank=True, null=True)
    attack_type = models.SmallIntegerField(blank=True, null=True)
    vulnerabilities = models.TextField(blank=True, null=True)
    susceptibilities = models.TextField(blank=True, null=True)
    resistances = models.TextField(blank=True, null=True)
    immunities = models.TextField(blank=True, null=True)
    additional_str = models.SmallIntegerField(blank=True, null=True)
    additional_agi = models.SmallIntegerField(blank=True, null=True)
    additional_end = models.SmallIntegerField(blank=True, null=True)
    additional_per = models.SmallIntegerField(blank=True, null=True)
    additional_foc = models.SmallIntegerField(blank=True, null=True)
    additional_wil = models.SmallIntegerField(blank=True, null=True)
    is_playable = models.IntegerField(blank=True, null=True)
    is_humanoid = models.IntegerField()
    is_invertebrae = models.IntegerField()
    is_flying = models.IntegerField()
    is_swimming = models.IntegerField()
    darkvision = models.IntegerField()
    see_invis = models.IntegerField()
    is_walking = models.IntegerField()
    endure_heat = models.IntegerField()
    endure_cold = models.IntegerField()
    is_undead = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'races'


class RacesSkills(models.Model):
    race = models.ForeignKey(Races, models.DO_NOTHING)
    skill = models.ForeignKey('SpellInfo', models.DO_NOTHING)
    level = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'races_skills'


class RacialAffinities(models.Model):
    race = models.ForeignKey(Races, models.DO_NOTHING)
    force = models.ForeignKey(Forces, models.DO_NOTHING)
    affinity_type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'racial_affinities'


class RemortUpgrades(models.Model):
    upgrade_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=20)
    renown_cost = models.PositiveSmallIntegerField()
    max_value = models.PositiveSmallIntegerField()
    scale = models.IntegerField()
    display_name = models.CharField(max_length=30)
    can_buy = models.IntegerField()
    bonus = models.IntegerField()
    survival_scale = models.IntegerField()
    survival_renown_cost = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'remort_upgrades'


class Seasons(models.Model):
    season_id = models.AutoField(primary_key=True)
    is_active = models.IntegerField()
    effective_date = models.DateTimeField()
    expiration_date = models.DateTimeField()
    last_challenge_cycle = models.DateTimeField()
    average_essence_gain = models.FloatField()
    average_remorts = models.FloatField()
    max_essence_gain = models.IntegerField()
    max_remorts = models.IntegerField()
    season_leader_account = models.IntegerField()
    seasonal_leader_name = models.TextField()
    max_renown = models.IntegerField()
    avg_renown = models.FloatField()

    class Meta:
        managed = False
        db_table = 'seasons'


class Skills(models.Model):
    skill_id = models.PositiveIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'skills'


class SpellFlags(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spell_flags'


class SpellForces(models.Model):
    spell = models.OneToOneField('SpellInfo', models.DO_NOTHING, primary_key=True)  # The composite primary key (spell_id, force_id) found, that is not supported. The first column is selected.
    force = models.ForeignKey(Forces, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'spell_forces'
        unique_together = (('spell', 'force'), ('spell', 'force'),)


class SpellInfo(models.Model):
    enum_symbol = models.CharField(max_length=255)
    func_name = models.CharField(max_length=255, blank=True, null=True)
    skill_name = models.TextField(blank=True, null=True)
    min_posn = models.IntegerField(blank=True, null=True)
    min_use = models.IntegerField(blank=True, null=True)
    spell_breakpoint = models.IntegerField(blank=True, null=True)
    held_cost = models.IntegerField(blank=True, null=True)
    wearoff_msg = models.TextField(blank=True, null=True)
    chant_text = models.TextField(blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)
    rate = models.IntegerField(blank=True, null=True)
    notice_chance = models.IntegerField(blank=True, null=True)
    appearance = models.TextField(blank=True, null=True)
    component_type = models.IntegerField(blank=True, null=True)
    component_value = models.IntegerField(blank=True, null=True)
    scale = models.IntegerField(blank=True, null=True)
    mod_stat_1 = models.IntegerField(blank=True, null=True)
    mod_stat_2 = models.IntegerField(blank=True, null=True)
    is_spell = models.IntegerField(blank=True, null=True)
    is_skill = models.IntegerField(blank=True, null=True)
    is_type = models.IntegerField(blank=True, null=True)
    decide_func = models.TextField()

    class Meta:
        managed = False
        db_table = 'spell_info'


class SpellsSpellFlags(models.Model):
    spell = models.OneToOneField(SpellInfo, models.DO_NOTHING, primary_key=True)  # The composite primary key (spell_id, flag_id) found, that is not supported. The first column is selected.
    flag = models.ForeignKey(SpellFlags, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'spells_spell_flags'
        unique_together = (('spell', 'flag'),)
