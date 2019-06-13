from sqlalchemy.types import (String, Integer, DateTime, Date, Time, Text,
                              Boolean)

ADD_UNIQUE = """ALTER TABLE "{table}"
                ADD CONTRAINT {table}_{column}_key
                UNIQUE ({column});"""
DROP_UNIQUE = """ALTER TABLE "{table}"
                 DROP CONTRAINT {table}_{column}_key;"""

SET_NOT_NULL = """ALTER TABLE "{table}"
                  ALTER COLUMN {column}
                  SET NOT NULL;"""
DROP_NOT_NULL = """ALTER TABLE "{table}"
                   ALTER COLUMN {column}
                   DROP NOT NULL;"""

ADD_COLUMN = """ALTER TABLE "{table}"
                ADD COLUN {column} {type}{constraint}"""

DROP_COLUMN = """ALTER TABLE "{table}" DORP COLUMN {column};"""


class MigrationMaker:
    def __init__(self, table, changed, added, dropped):
        self.table = table

        self.changed = changed
        self.added = added
        self.dropped = dropped

        self.sqls = []

    def make_migration(self):
        tb_name = self.table.name

        for c in self.dropped:
            self.sqls.append(DROP_COLUMN.format(table=tb_name, column=c))

        for name, changed in self.changed.items():
            if "unique" in changed:
                if changed["unique"]:
                    self.sqls.append(ADD_UNIQUE.format(table=tb_name,
                                                       column=name))
                else:
                    self.sqls.append(DROP_UNIQUE.format(table=tb_name,
                                                        column=name))

            if "nullable" in changed:
                if changed["nullable"]:
                    self.sqls.append(SET_NOT_NULL.format(table=tb_name,
                                                         column=name))
                else:
                    self.sqls.append(DROP_NOT_NULL.format(table=tb_name,
                                                          column=name))

        for column in self.added:
            self.sqls.append(ADD_COLUMN.format(
                table=tb_name, column=column.name,
                type=MigrationMaker.get_sql_type_str(column.type),
                contraint=MigrationMaker.get_constraint(column)))

    def update_table(self, conn):
        for sql in self.sqls:
            conn.execute(sql)

    @classmethod
    def table(cls, original, new):
        changed_column = {}
        added_column = []
        dropped_column = []

        for c in original.columns.keys():
            column = original.columns.get(c)

            new_column = new.columns.get(c)
            if new_column is None:
                dropped_column.append(c)
                continue

            com = cls.compare_column(column, new_column)
            if len(com) > 0:
                changed_column[c] = com

        for c in new.columns.keys():
            new_column = new.columns.get(c)

            column = original.columns.get(c)
            if column is None:
                added_column.append(new_column)

        return cls(original, changed_column, added_column, dropped_column)

    @staticmethod
    def compare_column(original, new):
        changed = {}

        if original.nullable != new.nullable:
            changed["nullable"] = new.nullable
        if original.unique != new.unique:
            changed["unique"] = new.unique

        return changed

    @staticmethod
    def get_sql_type_str(type_):
        if isinstance(type_, type):
            if type_ == String:
                return "VARCHAR"
            elif type_ == Integer:
                return "INTEGER"
            elif type_ == DateTime:
                return "TIMESTAMP"
            elif type_ == Date:
                return "DATE"
            elif type_ == Time:
                return "TIME"
            elif type_ == Text:
                return "TEXT"
            elif type_ == Boolean:
                return "BOOLEAN"
            return None

        if isinstance(type_, String):
            if type_.length is None:
                return "VARCHAR"
            return f"VARCHAR({type_.length})"
        elif isinstance(type_, Integer):
            return "INTEGER"
        elif isinstance(type_, DateTime):
            return "TIMESTAMP"
        elif isinstance(type_, Date):
            return "DATE"
        elif isinstance(type_, Time):
            return "TIME"
        elif isinstance(type_, Text):
            return "TEXT"
        elif isinstance(type_, Boolean):
            return "BOOLEAN"

    @staticmethod
    def get_constraint(column):
        con = ""
        if column.nullable:
            con += " NOT NULL"
        if column.unique:
            con += " UNIQUE"
        return con
