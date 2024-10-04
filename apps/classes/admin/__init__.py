from django.contrib.admin import site

from ..models.cls import Class
from ..models.level import ClassLevel
from ..models.race import ClassRace
from ..models.skill import ClassSkill

from .cls import ClassAdmin
from .level import ClassLevelAdmin
from .race import ClassRaceAdmin
from .skill import ClassSkillAdmin


site.register(Class, ClassAdmin)
site.register(ClassLevel, ClassLevelAdmin)
site.register(ClassRace, ClassRaceAdmin)
site.register(ClassSkill, ClassSkillAdmin)
