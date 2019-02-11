from django.contrib.gis.db.backends.postgis.base import DatabaseWrapper as PostgisDatabaseWrapper
from django.contrib.gis.db.backends.postgis.schema import PostGISSchemaEditor


class DatabaseSchemaEditor(PostGISSchemaEditor):
    # https://www.postgresql.org/docs/current/non-durability.html
    # https://www.postgresql.org/docs/current/sql-createtable.html#SQL-CREATETABLE-UNLOGGED
    sql_create_table = "CREATE UNLOGGED TABLE %(table)s (%(definition)s)"


class DatabaseWrapper(PostgisDatabaseWrapper):
    SchemaEditorClass = DatabaseSchemaEditor
