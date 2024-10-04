from django.db.models import AutoField


class UnsignedAutoField(AutoField):
    """MariaDB unsigned integer (range 0 to 4294967295)."""

    def db_type(self, connection):
        return "integer UNSIGNED AUTO_INCREMENT"

    def rel_db_type(self, connection):
        return "integer UNSIGNED"
