import unittest

from migrationmaker import (TableMigrationMaker, MetaDataMigration,
                            ColumnTool, MetaDataTool)
from sqlalchemy import Column, create_engine, inspect
from sqlalchemy.types import (String, Integer, DateTime, Date, Time, Text,
                              Boolean)
from .model import user_t1, user_t2, meta1, meta2, meta3


TYPES = [String, Integer, DateTime, Date, Time, Text, Boolean]


class TestMeta(unittest.TestCase):
    db_uri = "postgresql://testing:testing@localhost:13639/migration_testing"

    def test_column_type(self):
        print("Test SQL type to string")
        c = Column(String)
        self.assertEqual(ColumnTool.get_sql_type_str(c.type),
                         "VARCHAR")
        c = Column(Integer)
        self.assertEqual(ColumnTool.get_sql_type_str(c.type),
                         "INTEGER")
        c = Column(DateTime)
        self.assertEqual(ColumnTool.get_sql_type_str(c.type),
                         "TIMESTAMP")
        c = Column(Date)
        self.assertEqual(ColumnTool.get_sql_type_str(c.type),
                         "DATE")
        c = Column(Time)
        self.assertEqual(ColumnTool.get_sql_type_str(c.type),
                         "TIME")
        c = Column(Text)
        self.assertEqual(ColumnTool.get_sql_type_str(c.type),
                         "TEXT")
        c = Column(Boolean)
        self.assertEqual(ColumnTool.get_sql_type_str(c.type),
                         "BOOLEAN")
        c = Column(String(20))
        self.assertEqual(ColumnTool.get_sql_type_str(c.type),
                         "VARCHAR(20)")

    def test_compare_table(self):
        print("Test two table different")
        self.compare = TableMigrationMaker.compare_table(user_t1, user_t2)
        new_column = self.compare.added[0]
        type_ = new_column.type

        self.assertEqual(new_column.name, "password")
        self.assertTrue(isinstance(type_, String))
        self.assertEqual(type_.length, 32)
        self.assertTrue(new_column.nullable)
        self.assertEqual(new_column.default.arg, "123")

    def test_meta_string_convert(self):
        print("Test meta to strings and strings to meta")
        meta1_strings = MetaDataTool.to_strings(meta1)
        print("Meta 1\n", meta1_strings, "\n")
        
        meta1_reverse = MetaDataTool.strings_to_metadata(meta1_strings)
        
        test_meta_same = MetaDataMigration(meta1)
        test_meta_same.scan_new_metadata(meta1_reverse)
        self.assertTrue(test_meta_same.check_same())


if __name__ == "__main__":
    unittest.main()
