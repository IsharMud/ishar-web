from datetime import datetime

from ninja import Schema


class PlayerAccountSchema(Schema):
    """Player account schema."""
    account_id: int
    account_name: str


class PlayerSchema(Schema):
    """Player schema."""
    id: int
    name: str
    account: PlayerAccountSchema
    is_deleted: bool
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


class ImmortalSchema(Schema):
    """Immortal schema."""
    id: int
    name: str
    account: PlayerAccountSchema
    player_type: str
