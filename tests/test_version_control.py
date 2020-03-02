import unittest

from pprint import pprint
from migrationmaker import (TableMigrationMaker, MetaDataMigration,
                            ColumnTool, MetaDataTool, VersionControl)
from sqlalchemy import Column, create_engine, inspect
from sqlalchemy.types import (String, Integer, DateTime, Date, Time, Text,
                              Boolean)
from .model import user_t1, user_t2, meta1, meta2, meta3


TYPES = [String, Integer, DateTime, Date, Time, Text, Boolean]


class TestVersionCtrlMigration(unittest.TestCase):
    db_uri = "postgresql://testing:testing@localhost:13639/migration_testing"

    def test_meta(self):
        engine = create_engine(self.db_uri)
        conn = engine.connect()

        print("Preparing ...")
        table_names = inspect(engine).get_table_names()
        for table in table_names:
            conn.execute(f"""DROP TABLE "{table}";""")

        print("Migrate with new model")
        meta_migration = MetaDataMigration(meta1)
        meta_migration.scan_new_metadata(meta2)

        self.assertEqual(len(meta_migration.altered_tables), 1)
        self.assertEqual(len(meta_migration.dropped_table), 1)
        self.assertEqual(len(meta_migration.new_tables), 1)

        self.assertFalse(meta_migration.check_same())
    
    def test_version_ctl(self):
        version_ctl = VersionControl(self.db_uri)
        version_ctl.check_version_ctl_exist()

        meta1_str = MetaDataTool.to_strings(meta1)
        meta2_str = MetaDataTool.to_strings(meta2)

        # Insert first version
        version_ctl.new_version(meta1)
        version_ctl.report_status()
        version_ctl.migrate()

        # retreive lastest version
        latest_version = version_ctl.get_latest_version(is_old_metadata=True)
        self.assertEqual(meta1_str, latest_version)

        version_ctl.new_version(meta2)
        version_ctl.report_status()
        version_ctl.migrate()

        latest_version = version_ctl.get_latest_version(is_old_metadata=True)
        self.assertEqual(meta2_str, latest_version)

        version_ctl.new_version(meta3)
        version_ctl.report_status()
        version_ctl.migrate()

        latest_version = version_ctl.get_latest_version()
        self.assertEqual(MetaDataTool.to_strings(meta3),
                         latest_version)


if __name__ == "__main__":
    unittest.main()
