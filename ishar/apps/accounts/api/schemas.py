from datetime import datetime

from ninja import Schema


class AccountSchema(Schema):
    """Account schema."""
    account_id: int
    account_name: str
    created_at: datetime
    last_login: datetime
    current_essence: int
    earned_essence: int
    seasonal_earned: int
    player_count: int


class AccountPlayerSchema(Schema):
    """Account player schema."""
    id: int
    name: str
    is_deleted: int
    birth: datetime
    logon: datetime
    logout: datetime
    bankacc: int
    deaths: int
    remorts: int
    renown: int
    true_level: int
    favors: int
    total_renown: int
    quests_completed: int
    challenges_completed: int
    game_type: int
    player_stats: dict
    player_type: str


class UpgradeSchema(Schema):
    """Upgrade schema."""
    id: int
    name: str


class AccountUpgradeSchema(Schema):
    """Account Upgrade schema."""
    id: int
    cost: int
    description: str
    name: str
    max_value: int
    scale: int
    is_disabled: bool
    increment: int
    amount: int


class AccountAccountUpgradeSchema(Schema):
    """Account Account Upgrade schema."""
    upgrade: UpgradeSchema
    amount: int
