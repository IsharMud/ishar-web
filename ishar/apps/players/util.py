from django.conf import settings


def get_immortal_level(immortal_type: str = "Immortal") -> (int, None):
    if immortal_type and isinstance(immortal_type, str):
        for (imm_level, imm_type) in settings.IMMORTAL_LEVELS:
            if immortal_type == imm_type:
                return imm_level
    return None


def get_immortal_type(level: int = None) -> (str, None):
    if level and isinstance(level, int):
        for (imm_level, imm_type) in settings.IMMORTAL_LEVELS:
            if level == imm_level:
                return imm_type
    return None
