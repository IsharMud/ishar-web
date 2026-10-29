from django.contrib.admin import site

from ..models import AccountFatedSkill, TensionModifier

from .fated_skill import AccountFatedSkillAdmin
from .modifier import TensionModifierAdmin


site.register(AccountFatedSkill, AccountFatedSkillAdmin)
site.register(TensionModifier, TensionModifierAdmin)
