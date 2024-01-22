from datetime import datetime

from ninja import Schema


class PlayerAccountSchema(Schema):
    """Player account schema."""
    account_id: int
    account_name: str


class BasePlayerSchema(Schema):
    """Base player schema."""
    id: int
    name: str
    account: PlayerAccountSchema
    remorts: int
    true_level: int
    player_type: str


class PlayerSchema(BasePlayerSchema):
    """Player schema."""
    game_type: int
    is_deleted: bool
    birth: datetime
    logon: datetime
    logout: datetime
    bankacc: int
    deaths: int
    renown: int
    favors: int
    total_renown: int
    quests_completed: int
    challenges_completed: int
    player_stats: dict


class ImmortalSchema(Schema):
    """Immortal schema."""
    id: int
    name: str
    account: PlayerAccountSchema
    player_type: str
