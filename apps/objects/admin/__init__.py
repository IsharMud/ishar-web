from django.contrib.admin import site

from ..models.artifact import Artifact
from ..models.mod import ObjectMod
from ..models.object import Object
from ..models.relic import Relic

from .artifact import ArtifactAdmin
from .mod import ObjectModAdmin
from .object import ObjectAdmin
from .relic import RelicAdmin


site.register(Artifact, ArtifactAdmin)
site.register(ObjectMod, ObjectModAdmin)
site.register(Object, ObjectAdmin)
site.register(Relic, RelicAdmin)
