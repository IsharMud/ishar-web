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


class Accounts(models.Model):
    account_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField()
    current_essence = models.PositiveIntegerField()
    email = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=36)
    create_isp = models.CharField(max_length=25)
    last_isp = models.CharField(max_length=25)
    create_ident = models.CharField(max_length=25)
    last_ident = models.CharField(max_length=25)
    create_haddr = models.IntegerField()
    last_haddr = models.IntegerField()
    account_name = models.CharField(unique=True, max_length=25)
    account_gift = models.DateTimeField()
    banned_until = models.DateTimeField(blank=True, null=True)
    bugs_reported = models.IntegerField()
    earned_essence = models.IntegerField()
    is_private = models.IntegerField(blank=True, null=True)
    immortal_level = models.PositiveSmallIntegerField(blank=True, null=True)
    comm = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts'


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


class AdminInterfaceTheme(models.Model):
    name = models.CharField(unique=True, max_length=50)
    active = models.IntegerField()
    title = models.CharField(max_length=50)
    title_visible = models.IntegerField()
    logo = models.CharField(max_length=100)
    logo_visible = models.IntegerField()
    css_header_background_color = models.CharField(max_length=10)
    title_color = models.CharField(max_length=10)
    css_header_text_color = models.CharField(max_length=10)
    css_header_link_color = models.CharField(max_length=10)
    css_header_link_hover_color = models.CharField(max_length=10)
    css_module_background_color = models.CharField(max_length=10)
    css_module_text_color = models.CharField(max_length=10)
    css_module_link_color = models.CharField(max_length=10)
    css_module_link_hover_color = models.CharField(max_length=10)
    css_module_rounded_corners = models.IntegerField()
    css_generic_link_color = models.CharField(max_length=10)
    css_generic_link_hover_color = models.CharField(max_length=10)
    css_save_button_background_color = models.CharField(max_length=10)
    css_save_button_background_hover_color = models.CharField(max_length=10)
    css_save_button_text_color = models.CharField(max_length=10)
    css_delete_button_background_color = models.CharField(max_length=10)
    css_delete_button_background_hover_color = models.CharField(max_length=10)
    css_delete_button_text_color = models.CharField(max_length=10)
    list_filter_dropdown = models.IntegerField()
    related_modal_active = models.IntegerField()
    related_modal_background_color = models.CharField(max_length=10)
    related_modal_rounded_corners = models.IntegerField()
    logo_color = models.CharField(max_length=10)
    recent_actions_visible = models.IntegerField()
    favicon = models.CharField(max_length=100)
    related_modal_background_opacity = models.CharField(max_length=5)
    env_name = models.CharField(max_length=50)
    env_visible_in_header = models.IntegerField()
    env_color = models.CharField(max_length=10)
    env_visible_in_favicon = models.IntegerField()
    related_modal_close_button_visible = models.IntegerField()
    language_chooser_active = models.IntegerField()
    language_chooser_display = models.CharField(max_length=10)
    list_filter_sticky = models.IntegerField()
    form_pagination_sticky = models.IntegerField()
    form_submit_sticky = models.IntegerField()
    css_module_background_selected_color = models.CharField(max_length=10)
    css_module_link_selected_color = models.CharField(max_length=10)
    logo_max_height = models.PositiveSmallIntegerField()
    logo_max_width = models.PositiveSmallIntegerField()
    foldable_apps = models.IntegerField()
    language_chooser_control = models.CharField(max_length=20)
    list_filter_highlight = models.IntegerField()
    list_filter_removal_links = models.IntegerField()
    show_fieldsets_as_tabs = models.IntegerField()
    show_inlines_as_tabs = models.IntegerField()
    css_generic_link_active_color = models.CharField(max_length=10)
    collapsible_stacked_inlines = models.IntegerField()
    collapsible_stacked_inlines_collapsed = models.IntegerField()
    collapsible_tabular_inlines = models.IntegerField()
    collapsible_tabular_inlines_collapsed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'admin_interface_theme'


class AffectFlags(models.Model):
    flag_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'affect_flags'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(Accounts, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class Boards(models.Model):
    board_id = models.PositiveIntegerField(primary_key=True)
    board_name = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'boards'


class Challenges(models.Model):
    challenge_id = models.SmallAutoField(primary_key=True)
    mob_vnum = models.IntegerField()
    max_level = models.IntegerField()
    max_people = models.IntegerField()
    chall_tier = models.IntegerField()
    challenge_desc = models.CharField(max_length=80)
    winner_desc = models.CharField(max_length=80)
    mob_name = models.CharField(max_length=30)
    is_active = models.IntegerField()
    last_completion = models.DateTimeField()
    num_completed = models.IntegerField()
    num_picked = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'challenges'


class ClassLevels(models.Model):
    class_level_id = models.AutoField(primary_key=True)
    level = models.IntegerField()
    male_title = models.CharField(max_length=80)
    female_title = models.CharField(max_length=80)
    class_field = models.ForeignKey('Classes', models.DO_NOTHING, db_column='class_id')  # Field renamed because it was a Python reserved word.
    experience = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'class_levels'


class ClassSkills(models.Model):
    class_skills_id = models.AutoField(primary_key=True)
    class_field = models.ForeignKey('Classes', models.DO_NOTHING, db_column='class_id')  # Field renamed because it was a Python reserved word.
    skill = models.ForeignKey('Skills', models.DO_NOTHING)
    min_level = models.IntegerField()
    max_learn = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'class_skills'


class Classes(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(unique=True, max_length=15)
    class_display = models.CharField(max_length=32, blank=True, null=True)
    class_description = models.CharField(max_length=80, blank=True, null=True)
    is_playable = models.IntegerField()
    base_hit_pts = models.IntegerField()
    hit_pts_per_level = models.IntegerField()
    attack_per_level = models.IntegerField()
    spell_rate = models.IntegerField()
    class_stat = models.IntegerField()
    class_dc = models.IntegerField()
    base_fortitude = models.IntegerField()
    base_resilience = models.IntegerField()
    base_reflex = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'classes'


class ClassesRaces(models.Model):
    classes_races_id = models.AutoField(primary_key=True)
    race = models.ForeignKey('Races', models.DO_NOTHING)
    class_field = models.ForeignKey(Classes, models.DO_NOTHING, db_column='class_id')  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'classes_races'


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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(Accounts, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoFlatpage(models.Model):
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    content = models.TextField()
    enable_comments = models.IntegerField()
    template_name = models.CharField(max_length=70)
    registration_required = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_flatpage'


class DjangoFlatpageSites(models.Model):
    id = models.BigAutoField(primary_key=True)
    flatpage = models.ForeignKey(DjangoFlatpage, models.DO_NOTHING)
    site = models.ForeignKey('DjangoSite', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_flatpage_sites'
        unique_together = (('flatpage', 'site'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class Faqs(models.Model):
    faq_id = models.AutoField(primary_key=True)
    created = models.DateTimeField()
    question_text = models.TextField()
    question_answer = models.TextField()
    is_visible = models.IntegerField()
    display_order = models.PositiveIntegerField(unique=True)
    account = models.ForeignKey(Accounts, models.DO_NOTHING)
    slug = models.CharField(unique=True, max_length=16)

    class Meta:
        managed = False
        db_table = 'faqs'


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
        unique_together = (('player', 'kill_memory_set'),)


class KillMemoryBuckets(models.Model):
    kill_memory = models.ForeignKey(KillMemory, models.DO_NOTHING, blank=True, null=True)
    bucket_index = models.SmallIntegerField(blank=True, null=True)
    value = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kill_memory_buckets'
        unique_together = (('kill_memory', 'bucket_index'),)


class MudClientCategories(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    is_visible = models.IntegerField()
    display_order = models.PositiveIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'mud_client_categories'


class MudClients(models.Model):
    client_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=64)
    url = models.CharField(max_length=200)
    is_visible = models.IntegerField()
    category = models.ForeignKey(MudClientCategories, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mud_clients'


class MudProcesses(models.Model):
    process_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    user = models.CharField(max_length=32)
    last_updated = models.DateTimeField()
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mud_processes'


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    created = models.DateTimeField()
    subject = models.CharField(max_length=64)
    body = models.TextField()
    is_visible = models.IntegerField()
    account = models.ForeignKey(Accounts, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'news'


class Patches(models.Model):
    patch_id = models.AutoField(primary_key=True)
    patch_date = models.DateTimeField()
    patch_name = models.CharField(unique=True, max_length=64)
    patch_file = models.CharField(max_length=100)
    is_visible = models.IntegerField()
    account = models.ForeignKey(Accounts, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'patches'


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


class PlayerChallenges(models.Model):
    player = models.ForeignKey('Players', models.DO_NOTHING)
    challenge = models.ForeignKey(Challenges, models.DO_NOTHING)
    last_completed = models.DateTimeField()
    player_challenges_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'player_challenges'
        unique_together = (('player', 'challenge'),)


class PlayerCommon(models.Model):
    player = models.OneToOneField('Players', models.DO_NOTHING)
    class_id = models.IntegerField()
    race = models.ForeignKey('Races', models.DO_NOTHING)
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
    player_id = models.PositiveIntegerField(primary_key=True)  # The composite primary key (player_id, step_id) found, that is not supported. The first column is selected.
    step_id = models.IntegerField()
    num_collected = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'player_quest_steps'
        unique_together = (('player_id', 'step_id'),)


class PlayerQuests(models.Model):
    quest = models.OneToOneField('Quests', models.DO_NOTHING, primary_key=True)  # The composite primary key (quest_id, player_id) found, that is not supported. The first column is selected.
    player = models.ForeignKey('Players', models.DO_NOTHING)
    status = models.IntegerField()
    last_completed_at = models.DateTimeField()
    num_completed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'player_quests'
        unique_together = (('quest', 'player'),)


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
    skill = models.OneToOneField('Skills', models.DO_NOTHING, primary_key=True)  # The composite primary key (skill_id, player_id) found, that is not supported. The first column is selected.
    player = models.ForeignKey('Players', models.DO_NOTHING)
    skill_level = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'player_skills'
        unique_together = (('skill', 'player'),)


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
    renown = models.PositiveSmallIntegerField()
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
    quest_prereqs_id = models.AutoField(unique=True)

    class Meta:
        managed = False
        db_table = 'quest_prereqs'
        unique_together = (('quest', 'required_quest'),)


class QuestRewards(models.Model):
    reward_num = models.IntegerField()
    reward_type = models.IntegerField()
    quest = models.ForeignKey('Quests', models.DO_NOTHING)
    class_restrict = models.IntegerField()
    quest_reward_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'quest_rewards'


class QuestSteps(models.Model):
    step_id = models.AutoField(primary_key=True)
    step_type = models.IntegerField()
    target = models.IntegerField()
    num_required = models.IntegerField()
    quest = models.ForeignKey('Quests', models.DO_NOTHING)
    time_limit = models.IntegerField()
    mystify = models.IntegerField()
    mystify_text = models.CharField(max_length=80)
    auto_complete = models.IntegerField(blank=True, null=True)

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
    start_item = models.PositiveIntegerField(blank=True, null=True)

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
    race_skill_id = models.AutoField(primary_key=True)
    race = models.ForeignKey(Races, models.DO_NOTHING)
    skill = models.ForeignKey('Skills', models.DO_NOTHING)
    level = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'races_skills'


class RacialAffinities(models.Model):
    race_affinity_id = models.AutoField(primary_key=True)
    race = models.ForeignKey(Races, models.DO_NOTHING)
    force = models.ForeignKey(Forces, models.DO_NOTHING)
    affinity_type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'racial_affinities'


class RacialDeathload(models.Model):
    racial_deathload_id = models.AutoField(primary_key=True)
    race = models.ForeignKey(Races, models.DO_NOTHING)
    vnum = models.IntegerField()
    percent_chance = models.IntegerField()
    min_level = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'racial_deathload'


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
    average_essence_gain = models.FloatField()
    average_remorts = models.FloatField()
    max_essence_gain = models.IntegerField()
    max_remorts = models.IntegerField()
    season_leader_account = models.IntegerField()
    seasonal_leader_name = models.TextField()
    last_challenge_cycle = models.DateTimeField()
    max_renown = models.IntegerField()
    avg_renown = models.FloatField()
    total_remorts = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'seasons'


class SkillComponents(models.Model):
    skill_components_id = models.AutoField(primary_key=True)
    skill = models.ForeignKey('Skills', models.DO_NOTHING)
    component_type = models.IntegerField()
    component_value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'skill_components'


class SkillForces(models.Model):
    skill = models.ForeignKey('Skills', models.DO_NOTHING)
    force = models.ForeignKey(Forces, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'skill_forces'
        unique_together = (('skill', 'force'),)


class Skills(models.Model):
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
    scale = models.IntegerField(blank=True, null=True)
    mod_stat_1 = models.IntegerField(blank=True, null=True)
    mod_stat_2 = models.IntegerField(blank=True, null=True)
    decide_func = models.TextField()
    skill_type = models.IntegerField()
    parent_skill = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'skills'


class SkillsSpellFlags(models.Model):
    skill = models.ForeignKey(Skills, models.DO_NOTHING)
    flag_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'skills_spell_flags'


class SpellFlags(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spell_flags'
