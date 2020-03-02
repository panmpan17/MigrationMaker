from .migration import MetaDataMigration, MetaDataTool

from datetime import datetime
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.sql import select


def connect_db(f):
    def wrapper(self, *args, **kwargs):
        self._connect()
        resault = f(self, *args, kwargs)
        self._close()
        return resault
    return wrapper


class VersionControl(MetaDataMigration):
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        self.verison_ctl_t = None
        self.conn = None

        self._old_metadata = None
        self._new_metadata = None
        self._tables = {}

        self.altered_tables = []
        self.new_tables = []
        self.dropped_table = []

    def _connect(self):
        if self.conn is None:
            self.conn = self.engine.connect()

    def _close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def check_version_ctl_exist(self):
        self.verison_ctl_t = Table(
            "version_ctl", MetaData(),
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("tablename", String),
            Column("columns", String),
            Column("create_at", DateTime, default=datetime.utcnow))

        self.verison_ctl_t.create(self.engine)

    def report_status(self):
        print("-" * 10, "Status", "-" * 10)
        if len(self.dropped_table) > 0:
            print("Table dropped:")
            for tb in self.dropped_table:
                print(" -", tb)
            print()

        if len(self.new_tables) > 0:
            print("Table added:")
            for tb in self.new_tables:
                print(" -", tb)
            print()

        if len(self.altered_tables) > 0:
            print("Table altered:")
            for tb in self.altered_tables:
                print(" -", tb.name)
                tb.report_status(prefix="  ")
            print()

        print("-" * 28)

    def assign_metadata(self, metadata):
        self._old_metadata = metadata
        self._tables = dict(metadata.tables)

    def new_version(self, new_metadata):
        if self._new_metadata is not None:
            self._old_metadata = self._new_metadata
            self._tables = dict(self._old_metadata.tables)

        self._new_metadata = new_metadata

        super().scan_new_metadata(new_metadata)

    @connect_db
    def migrate(self, *args, **kwargs):
        super().migrate(self.conn, self.engine)

        table_strings = MetaDataTool.to_strings(self._new_metadata)
        datas = []

        for table_name, column_data in table_strings.items():
            datas.append({"tablename": table_name, "columns": column_data})

        for table_name in self.dropped_table:
            datas.append({"tablename": table_name, "columns": "DROP"})

        rst = self.conn.execute(self.verison_ctl_t.insert(), datas)

        if rst.is_insert:
            return True
        return False

    @connect_db
    def get_latest_version(self, is_old_metadata=False, *args, **kwargs):
        rows = self.conn.execute(select([self.verison_ctl_t])).fetchall()

        datas = {}

        for row in rows:
            if row["tablename"] in datas:
                if row["create_at"] < datas[row["tablename"]]["create_at"]:
                    continue

            datas[row["tablename"]] = {
                "columns": row["columns"],
                "create_at": row["create_at"],
            }

        dropped_table = []
        for key, value in datas.items():
            datas[key] = value["columns"]
            if value["columns"] == "DROP":
                dropped_table.append(key)
        
        for tablename in dropped_table:
            datas.pop(tablename)

        if is_old_metadata:
            self.assign_metadata(MetaDataTool.strings_to_metadata(datas))
        return datas
