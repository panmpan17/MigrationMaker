import unittest

from migrationmaker import MigrationMaker
from sqlalchemy import Table, Column, MetaData
from sqlalchemy.types import (String, Integer, DateTime, Date, Time, Text,
                              Boolean)


TYPES = [String, Integer, DateTime, Date, Time, Text, Boolean]


class TestBasicMigration(unittest.TestCase):
    def test_column_type(self):
        c = Column(String)
        self.assertEqual(MigrationMaker.get_sql_type_str(c.type), "VARCHAR")
        c = Column(Integer)
        self.assertEqual(MigrationMaker.get_sql_type_str(c.type), "INTEGER")
        c = Column(DateTime)
        self.assertEqual(MigrationMaker.get_sql_type_str(c.type), "TIMESTAMP")
        c = Column(Date)
        self.assertEqual(MigrationMaker.get_sql_type_str(c.type), "DATE")
        c = Column(Time)
        self.assertEqual(MigrationMaker.get_sql_type_str(c.type), "TIME")
        c = Column(Text)
        self.assertEqual(MigrationMaker.get_sql_type_str(c.type), "TEXT")
        c = Column(Boolean)
        self.assertEqual(MigrationMaker.get_sql_type_str(c.type), "BOOLEAN")
        c = Column(String(20))
        self.assertEqual(MigrationMaker.get_sql_type_str(c.type),
                         "VARCHAR(20)")

    def test_compare_table(self):
        meta1 = MetaData()
        meta2 = MetaData()

        table1 = Table(
            "user", meta1,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("name", String, nullable=False, unique=False),
            Column("email", String, nullable=True, unique=True),
            Column("data", String))

        table2 = Table(
            "user", meta2,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("name", String, nullable=True, unique=True, default="123"),
            Column("email", String, nullable=False, unique=False),
            Column("password", String(32), nullable=True, default="123"))

        self.compare = MigrationMaker.compare_table(table1, table2)
        new_column = self.compare.added[0]
        type_ = new_column.type
        self.assertEqual(new_column.name, "password")
        self.assertTrue(isinstance(type_, String))
        self.assertEqual(type_.length, 32)
        self.assertTrue(new_column.nullable)
        self.assertEqual(new_column.default.arg, "123")


if __name__ == "__main__":
    unittest.main()
