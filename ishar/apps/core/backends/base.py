from django.db.backends.mysql.base import (
    DatabaseWrapper as BaseDatabaseWrapper
)
from django.db.backends.mysql.features import (
    DatabaseFeatures as BaseDatabaseFeatures
)


class DatabaseFeatures(BaseDatabaseFeatures):
    allows_auto_pk_0 = True


class DatabaseWrapper(BaseDatabaseWrapper):
    features_class = DatabaseFeatures
