import unittest

from migrationmaker import TableMigrationMaker, MetaDataMigration
from sqlalchemy import Column, create_engine
from sqlalchemy.types import (String, Integer, DateTime, Date, Time, Text,
                              Boolean)
from .model import user_t1, user_t2, meta1, meta2


TYPES = [String, Integer, DateTime, Date, Time, Text, Boolean]


class TestBasicMigration(unittest.TestCase):
    db_uri = "postgresql://website:website@localhost:13639/websitedb"

    def test_column_type(self):
        c = Column(String)
        self.assertEqual(TableMigrationMaker.get_sql_type_str(c.type),
                         "VARCHAR")
        c = Column(Integer)
        self.assertEqual(TableMigrationMaker.get_sql_type_str(c.type),
                         "INTEGER")
        c = Column(DateTime)
        self.assertEqual(TableMigrationMaker.get_sql_type_str(c.type),
                         "TIMESTAMP")
        c = Column(Date)
        self.assertEqual(TableMigrationMaker.get_sql_type_str(c.type),
                         "DATE")
        c = Column(Time)
        self.assertEqual(TableMigrationMaker.get_sql_type_str(c.type),
                         "TIME")
        c = Column(Text)
        self.assertEqual(TableMigrationMaker.get_sql_type_str(c.type),
                         "TEXT")
        c = Column(Boolean)
        self.assertEqual(TableMigrationMaker.get_sql_type_str(c.type),
                         "BOOLEAN")
        c = Column(String(20))
        self.assertEqual(TableMigrationMaker.get_sql_type_str(c.type),
                         "VARCHAR(20)")

    def test_compare_table(self):
        self.compare = TableMigrationMaker.compare_table(user_t1, user_t2)
        new_column = self.compare.added[0]
        type_ = new_column.type
        self.assertEqual(new_column.name, "password")
        self.assertTrue(isinstance(type_, String))
        self.assertEqual(type_.length, 32)
        self.assertTrue(new_column.nullable)
        self.assertEqual(new_column.default.arg, "123")

    def test_meta(self):
        engine = create_engine(TestBasicMigration.db_uri)
        print("Create default model")
        meta1.create_all(engine)

        conn = engine.connect()

        print("Migrate with new model")
        meta_migration = MetaDataMigration(meta1)
        meta_migration.scan_new_metadata(meta2)
        meta_migration.migrate(conn, engine)


if __name__ == "__main__":
    unittest.main()
